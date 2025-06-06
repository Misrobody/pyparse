from utils import *
from tools.Operation import *

'''
A class which tracks the context in a depth-first walk in an ast.
Keeps track of:
 - The last seen function definition and its depth in the tree (level)
 - The last seen class definition
'''
class Context:
    def __init__(self, filepath):
        self.filepath = filepath
        self.func_node = None
        self.func_level = 0
        self.class_node = None
        self.class_level = 0

    def update_func(self, func_node, level):
        self.func_node = func_node
        self.func_level = level

    def update_class(self, class_node, class_level):
        self.class_node = class_node
        self.class_level = class_level

    '''
    def resolve_name(self, node):
        name_parts = [] 
        while isinstance(node, (ast.Attribute, ast.Call)):
            if isinstance(node, ast.Attribute):
                name_parts.append(node.attr)
            node = node.value if isinstance(node, ast.Attribute) else node.func    
        if isinstance(node, ast.Name):
            name_parts.append(node.id)   
        return ".".join(reversed(name_parts))
    '''
    
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
        return ".".join(reversed(name_parts))
  
    def resolve_callee_name(self, call):
        name = self.resolve_name(call)
            
        if "self" in name:
            name = name.replace("self", self.class_node.name)
        elif "super" in name and self.class_node.bases:
            name = name.replace("super", self.resolve_name(self.class_node.bases[0]))
        return name
    
    def resolve_operation_name(self):
        if is_method(self.func_node) or is_static_method(self.func_node):
            return f"{self.class_node.name}.{self.func_node.name}"
        return self.func_node.name  
       
    def build_operation_definition(self):
        return Operation(self.filepath, file_name(self.filepath), self.resolve_operation_name())
    
    def build_class_definition(self):
        return Operation(self.filepath, file_name(self.filepath), self.class_node.name)
    