from tools.Operation import *
from tools.OperationCall import *
import ast
from utils import *

class Context:
    def __init__(self, filepath):
        self.filepath = filepath
        self.func_node = None
        self.func_level = 0
        self.class_node = None

    def update_func(self, func_node, level):
        self.func_node = func_node
        self.func_level = level

    def update_class(self, class_node):
        self.class_node = class_node

    def resolve_caller_name(self, current_level):
        if self.func_level == current_level:
            self.update_func(None, 0)
        if self.func_node is None:
            return ""
        return self.resolve_operation_name()
        
    def resolve_operation_name(self):
        if is_method(self.func_node) or is_static_method(self.func_node):
            return f"{self.class_node.name}.{self.func_node.name}"
        return self.func_node.name

    def resolve_name(self, node):
        '''Resolve a multipart name (hello.world)'''
        name_parts = [] 
        while isinstance(node, (ast.Attribute, ast.Call)):
            if isinstance(node, ast.Attribute):
                name_parts.append(node.attr)
            node = node.value if isinstance(node, ast.Attribute) else node.func    
        if isinstance(node, ast.Name):
            name_parts.append(node.id)   
        return ".".join(reversed(name_parts))

    def resolve_callee_name(self, call):
        name = self.resolve_name(call)
            
        if "self" in name:
            name = name.replace("self", self.class_node.name)
        elif "super" in name and self.class_node.bases:
            name = name.replace("super", self.resolve_name(self.class_node.bases[0]))
        return name      
        
    def build_call(self, call, call_level):
        caller = Operation(self.filepath, file_name(self.filepath), self.resolve_caller_name(call_level))
        callee = Operation("<unknown>", "<unknown>", self.resolve_callee_name(call))
        return OperationCall(caller, callee)
    
    def build_operation_definition(self):
        return Operation(self.filepath, file_name(self.filepath), self.resolve_operation_name())
    
    def build_class_definition(self):
        return Operation(self.filepath, file_name(self.filepath), self.class_node.name)