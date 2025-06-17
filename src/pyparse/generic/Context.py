from utils import *
from generic.Operation import *
from dataflow.CommonBlock import *
from call.OperationCall import *
from State import *
from generic.ClassInfo import *
from generic.FuncInfo import *
import sys

class Context:
    def __init__(self):   
        self._class = None
        self._func = None     
        self._file = None
    
    def update_func(self, funcNode):
        self._func = funcNode
        
    def update_file(self, fileinfo):
        self._file = fileinfo

    def update_class(self, classInfo):
        self._class = classInfo
        
    @property
    def file(self):
        return self._file
    
    @property
    def cur_class_name(self):
        return self._class.name
                              
    def resolve_datacall_targets(self, datacall):
        if isinstance(datacall, ast.Assign):
            res = []
            for t in datacall.targets:
                if isinstance(t, ast.Subscript):
                    res.append(t.value)  
                elif isinstance(t, ast.Name):  
                    res.append(t)  
                elif isinstance(t, ast.Attribute):  
                    res.append(t)
                elif isinstance(t, ast.Tuple):  
                    res.extend(t.elts)  
                else:
                    res.append(t)
            return res
        if isinstance(datacall.target, (ast.Subscript, ast.Name, ast.Attribute)):
            return [datacall.target]
        return [State.UNRESOLVED]
  
    def resolve_datacall_values(self, node):
        # Handle different collection types with variable references
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            if not node.elts:
                return [ast.Constant(State.EMPTY_COLLECTION)]   
            elements = sum((self.resolve_datacall_values(el) for el in node.elts), [])
            return elements
        elif isinstance(node, ast.Dict):
            if not node.keys:
                return [ast.Constant(State.EMPTY_COLLECTION)]       
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
            return [ast.Constant(State.LAMBDA)]
                
        # Directly return relevant AST objects
        if isinstance(node, (ast.Constant, ast.Name, ast.Attribute, ast.Call, ast.Subscript)):
            return [node]
        
        # Handle operations
        if isinstance(node, ast.BinOp):
            return sum([self.resolve_datacall_values(node.left), self.resolve_datacall_values(node.right)], [])
        if isinstance(node, ast.UnaryOp):
            return sum(self.resolve_datacall_values([node.operand]), [])
        if isinstance(node, ast.Compare):
            left_vals = self.resolve_datacall_values(node.left)
            comparators_vals = sum([self.resolve_datacall_values(c) for c in node.comparators], [])
            return sum([left_vals + comparators_vals], [])
        if isinstance(node, ast.BoolOp):
            return sum([self.resolve_datacall_values(val) for val in node.values], [])

        return [node]
        
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
        if isinstance(node, ast.ListComp):
            return State.COMP
        if not name_parts:
            return State.EMPTY
        return name_parts[0]
       
    def build_datacalls(self, datacall, parent):
        res = []
        values = self.resolve_datacall_values(datacall.value)
        targets = self.resolve_datacall_targets(datacall)

        for name in targets:
            caller = Operation(self._file.full_path, self._file.module, self.resolve_name(name), State.KNOWN)
            
            if isinstance(parent, ast.Module):
                    self._file.add_global_var(caller)          
            if isinstance(parent, ast.ClassDef) or (isinstance(parent, ast.FunctionDef) and "__init__" in parent.name):
                    self._class.add_attr(caller)
                      
            for val in values:
                if not isinstance(val, ast.Constant):
                    name = self.resolve_name(val)
                    if name == State.COMP:
                        continue                 
                    if "self" in name:
                        name = self._class.name
                    callee = Operation(State.UNKNOWN, State.UNKNOWN, name, State.UNKNOWN)
                    
                    res.append(OperationCall(caller, callee))
        return res       
    
    def build_class(self, node):
        return ClassInfo(self._file.full_path, f"{self._file.module}.{node.name}", node.name, node.bases)
    
    def build_func(self, node):
        return FuncInfo(self._file.full_path, self._file.module, node)
    
    def build_call(self, call):
        if self._func == None:
            caller = Operation(self._file.full_path, self._file.module, "FLIP", State.UNKNOWN)
            
        else:
            caller = Operation(self._file.full_path, self._file.module, self._func.name, State.KNOWN)
        callee = Operation(State.UNKNOWN, State.UNKNOWN, self.resolve_name(call), State.UNKNOWN)
        return OperationCall(caller, callee)
    
    def build_import_froms(self, node):
        res = []
        for alias in node.names:
            res.append(Operation(State.IMPORTED, node.module, alias.name, State.IMPORTED))
            if alias.asname:
                res.append(Operation(State.IMPORTED, node.module, alias.asname, State.IMPORTED))
        return res