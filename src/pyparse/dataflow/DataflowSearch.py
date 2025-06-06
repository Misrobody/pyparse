import ast, os
from generic.Search import *
from dataflow.DataflowContext import *

class DataflowSearch(Search):
    def __init__(self, source_dir):
        super().__init__(source_dir)   
        self.all_common_blocks = []
        
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
                self.all_operations.append(context.build_operation_definition())
            elif isinstance(node, ast.ClassDef):
                context.update_class(node, level)
                self.all_operations.append(context.build_class_definition())
                self.all_common_blocks.append(context.build_common_block(node))
            elif isinstance(node, ast.Assign) or isinstance(node, ast.AnnAssign) or isinstance(node, ast.AugAssign):
                self.all_calls.extend(context.build_datacall(node, level))
            elif isinstance(node, ast.Import):
                self.all_imports.update(alias.name for alias in node.names)
                
            for child in ast.iter_child_nodes(node):
                _walk_search(child, level + 1)

        _walk_search(get_ast(path), 0)
        
    
        


