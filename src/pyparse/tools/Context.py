from utils import *

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