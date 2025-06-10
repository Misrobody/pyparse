from utils import *
from generic.Operation import *

from dataflow.DataCall import *
from dataflow.CommonBlock import *

from call.OperationCall import *

class Context:
    def __init__(self):
        self.filepath = ""
        
        self.func_node = None
        self.func_level = 0
        
        self.class_node = None
        self.class_level = 0
        
        self.common_block = None
        
    def update_path(self, path):
        self.filepath = path

    def update_func(self, func_node, level):
        self.func_node = func_node
        self.func_level = level

    def update_class(self, class_node, class_level):
        self.class_node = class_node
        self.class_level = class_level
     
    ###############################################################################################################

    def resolve_name(self, node):
        name_parts = [] 
        while isinstance(node, (ast.Attribute, ast.Call, ast.Subscript)):
            if isinstance(node, ast.Attribute):
                name_parts.append(node.attr)
            elif isinstance(node, ast.Subscript):
                name_parts.append(self.resolve_name(node.value))
            node = node.value if isinstance(node, (ast.Attribute, ast.Subscript)) else node.func    
        if isinstance(node, ast.Name):
            name_parts.append(node.id)             
        name = ".".join(reversed(name_parts))           
        if "self" in name:
            name = name.replace("self", self.class_node.name)
        elif "super" in name and self.class_node.bases:
            name = name.replace("super", self.resolve_name(self.class_node.bases[0]))
        return name
    
    def resolve_operation_name(self):
        if is_method(self.func_node) or is_static_method(self.func_node):
            return f"{self.class_node.name}.{self.func_node.name}"
        return self.func_node.name  
         
    def resolve_caller_name(self, current_level):
        if self.func_level == current_level:
            self.update_func(None, 0)
        if self.func_node is None:
            return ""
        return self.resolve_operation_name()
                   
    def resolve_datacall_targets(self, datacall):
        if isinstance(datacall, ast.Assign):
            res = []
            for t in datacall.targets:
                if isinstance(t, ast.Subscript):
                    res.append(t.value)  # Keep the AST object
                elif isinstance(t, ast.Name):  
                    res.append(t)  # Return the actual Name object
                elif isinstance(t, ast.Attribute):  
                    res.append(t)  # Keep the AST Attribute object
                elif isinstance(t, ast.Tuple):  
                    res.extend(t.elts)  # Preserve elements as AST objects
                else:
                    res.append(t)  # Preserve AST object for unknown cases
            return res

        if isinstance(datacall.target, (ast.Subscript, ast.Name, ast.Attribute)):
            return [datacall.target]  # Preserve the AST object

        return ["<unresolved>"]

    def resolve_direction(self, name):
        if isinstance(name.ctx, ast.Load):
            return "READ"
        if isinstance(name.ctx, (ast.Store, ast.Del)):
            return "WRITE"
        return "NONE"
    
    def resolve_datacall_values(self, node):
        # Handle different collection types with variable references
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            if not node.elts:
                return [ast.Constant("<empty-list/tuple/set>")]   
            elements = sum((self.resolve_datacall_values(el) for el in node.elts), [])
            return elements
        elif isinstance(node, ast.Dict):
            if not node.keys:
                return [ast.Constant("<empty-dict>")]       
            keys = sum((self.resolve_datacall_values(key) for key in node.keys), [])
            values = sum((self.resolve_datacall_values(val) for val in node.values), [])
            return keys + values
        
        # Handle structures by comprehension
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):        
            return sum([self.resolve_datacall_values(gen.iter) for gen in node.generators], [])
        
        # Handle if structures
        if isinstance(node, ast.IfExp):
            test_vals = self.resolve_datacall_values(node.test)
            body_vals = self.resolve_datacall_values(node.body)
            orelse_vals = self.resolve_datacall_values(node.orelse)
            return test_vals + body_vals + orelse_vals
        
        # Handle f strings
        if isinstance(node, ast.JoinedStr):
            return sum([self.resolve_datacall_values(val.value) for val in node.values if isinstance(val, ast.FormattedValue)], [])
        
        # Handle lambdas
        if isinstance(node, ast.Lambda):
            return [ast.Constant("<lambda>")]
                
        # Directly return relevant AST objects
        if isinstance(node, (ast.Constant, ast.Name, ast.Attribute, ast.Call, ast.Subscript)):
            return [node]
        
        # Handle operations
        if isinstance(node, ast.BinOp):
            return sum([self.resolve_datacall_values(node.left), self.resolve_datacall_values(node.right)], [])
        if isinstance(node, ast.UnaryOp):
            return sum(self.resolve_datacall_values(node.operand), [])
        if isinstance(node, ast.Compare):
            left_vals = self.resolve_datacall_values(node.left)
            comparators_vals = sum([self.resolve_datacall_values(c) for c in node.comparators], [])
            return sum([left_vals + comparators_vals], [])
        if isinstance(node, ast.BoolOp):
            return sum([self.resolve_datacall_values(val) for val in node.values], [])

        return [node]

    ###############################################################################################################

    def build_datacall(self, datacall, datacall_level):
        res = []
        values = self.resolve_datacall_values(datacall.value)
        targets = self.resolve_datacall_targets(datacall)

        for name in targets:
            caller = Operation(self.filepath, file_name(self.filepath), self.resolve_name(name))
            direction = self.resolve_direction(name)
            
            # Add call to common block if needed
            if self.common_block:
                if datacall_level == 1:
                    self.common_block.addCaller(caller, direction)
                if datacall_level == (self.class_level + 1) or (self.class_node and self.class_node.name in caller.name):
                    self.common_block.addCaller(caller, direction)

            for val in values:
                if not isinstance(val, ast.Constant):
                    callee = Operation("<unknown>", "<unknown>",  self.resolve_name(val))
                    res.append(DataCall(caller, callee, direction))

        return res   
    
    def build_common_block(self, node):
        name = node.name if isinstance(node, ast.ClassDef) else self.filepath
        self.common_block = CommonBlock(name)
        return self.common_block
    
    def build_call(self, call, call_level):
        caller = Operation(self.filepath, file_name(self.filepath), self.resolve_caller_name(call_level))
        callee = Operation("<unknown>", "<unknown>", self.resolve_name(call))
        return OperationCall(caller, callee)
    
    def build_operation_definition(self):
        return Operation(self.filepath, file_name(self.filepath), self.resolve_operation_name())
    
    def build_class_definition(self):
        return Operation(self.filepath, file_name(self.filepath), self.class_node.name)
