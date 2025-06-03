from tools.Operation import *
from tools.OperationCall import *
import ast
from utils import *

class Context:
    def __init__(self, filepath):
        self.filepath = filepath
        self.func_node = None
        self.level = 0
        self.class_node = ""

    def update(self, func_node, level):
        self.func_node = func_node
        self.level = level

    def update_class(self, class_node):
        self.class_node = class_node

    def get(self, current_level):
        if self.level == current_level:
            self.update(None, 0)

        if self.func_node is None:
            return ""

        return (
            f"{self.class_node.name}.{self.func_node.name}"
            if is_method(self.func_node)
            else self.func_node.name
        )

    '''
    Resolve the name of a given operation call (method or function)
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

    def resolve_super_self(self, name):
        if "self" in name:
            name = name.replace("self", self.class_node.name)
        elif "super" in name and self.class_node.bases:
            name = name.replace("super", self.resolve_name(self.class_node.bases[0]))
        return name

    def get_name(self, call):
        return self.resolve_super_self(self.resolve_name(call))

    def build_call(self, call, call_level):
        caller = Operation(self.filepath, file_name(self.filepath), self.get(call_level))
        callee = Operation("<unknown>", "<unknown>", self.get_name(call))
        return OperationCall(caller, callee)
    
    def build_operation(self, cur_level):
        return Operation(self.filepath, file_name(self.filepath), self.get(cur_level))