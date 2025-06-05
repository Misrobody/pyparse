import ast, os
from utils import *
from tools.DataflowContext import *
from tools.Search import *

class DataflowSearch(Search):
    def __init__(self, source_dir):
        self.source_dir = source_dir
        
        self.all_datacalls = []
        self.all_common_blocks = []
        
    def datacalls(self):
        return self.all_datacalls
    
    def common_blocks(self):
        return self.all_common_blocks
                                                       
    def _depth_first_search(self, path):
        context = DataflowContext(path)

        def _walk_search(node, level):
            if not any(ast.iter_child_nodes(node)):  
                return

            if isinstance(node, ast.Module):
                self.all_common_blocks.append(context.build_common_block(node))
            elif isinstance(node, ast.FunctionDef):
                context.update_func(node, level)
            elif isinstance(node, ast.ClassDef):
                context.update_class(node, level)
                self.all_common_blocks.append(context.build_common_block(node))
            elif isinstance(node, ast.Assign) or isinstance(node, ast.AnnAssign) or isinstance(node, ast.AugAssign):
                self.all_datacalls.extend(context.build_datacall(node, level))
                
            for child in ast.iter_child_nodes(node):
                _walk_search(child, level + 1)

        _walk_search(get_ast(path), 0)
        
    
        


