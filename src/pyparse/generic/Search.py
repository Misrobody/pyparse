import os
from utils import *
from generic.Context import *

class Search:
    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.context = Context()
        
        self.all_opcalls = []
        self.all_datacalls = []
        self.all_operations = []
        self.all_imports = set()
        self.all_common_blocks = []
        
    def common_blocks(self):
        return self.all_common_blocks
    
    def ops(self):
        return operation_dict(self.all_operations)
    
    def opcalls(self):
        return self.all_opcalls
    
    def datacalls(self):
        return self.all_datacalls
    
    def imports(self):
        return list(self.all_imports)    
    
    def search(self):                
        for root, _, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith(".py"):
                    self._depth_first_search(os.path.join(root, file))
                                                    
    def _depth_first_search(self, path):
        def _walk_search(node, level):
            if not any(ast.iter_child_nodes(node)):  
                return

            if isinstance(node, ast.Module):
                self.all_common_blocks.append(self.context.build_common_block(node))
            elif isinstance(node, ast.FunctionDef):
                self.context.update_func(node, level)
                self.all_operations.append(self.context.build_operation_definition())
            elif isinstance(node, ast.ClassDef):
                self.context.update_class(node, level)
                self.all_operations.append(self.context.build_class_definition())
                self.all_common_blocks.append(self.context.build_common_block(node))
            elif isinstance(node, ast.Call):
                self.all_opcalls.append(self.context.build_call(node, level))  
            elif isinstance(node, ast.Import):
                self.all_imports.update(alias.name for alias in node.names)   
            elif isinstance(node, ast.Assign) or isinstance(node, ast.AnnAssign) or isinstance(node, ast.AugAssign):
                self.all_datacalls.extend(self.context.build_datacall(node, level))

            for child in ast.iter_child_nodes(node):
                _walk_search(child, level + 1)

        self.context.update_path(path)
        _walk_search(get_ast(path), 0)