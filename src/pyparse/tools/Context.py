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

    def update_func(self, func_node, level):
        self.func_node = func_node
        self.func_level = level

    def update_class(self, class_node):
        self.class_node = class_node

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