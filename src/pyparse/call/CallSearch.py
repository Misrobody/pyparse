import ast, os
from utils import *
from tools.CallContext import *
from tools.Search import *

class CallSearch(Search):
    def __init__(self, source_dir):
        self.source_dir = source_dir
        
        self.all_operations = []
        self.all_calls = []
        self.all_imports = set()
      
    def ops(self):
        return operation_dict(self.all_operations)
    
    def calls(self):
        return self.all_calls
    
    def imports(self):
        return list(self.all_imports)
                                                       
    def _depth_first_search(self, path):
        context = CallContext(path)

        def _walk_search(node, level):
            if not any(ast.iter_child_nodes(node)):  
                return

            if isinstance(node, ast.FunctionDef):
                context.update_func(node, level)
                self.all_operations.append(context.build_operation_definition())
            elif isinstance(node, ast.ClassDef):
                context.update_class(node, level)
                self.all_operations.append(context.build_class_definition())
            elif isinstance(node, ast.Call):
                self.all_calls.append(context.build_call(node, level))
            elif isinstance(node, ast.Import):
                self.all_imports.update(alias.name for alias in node.names)

            for child in ast.iter_child_nodes(node):
                _walk_search(child, level + 1)

        _walk_search(get_ast(path), 0)


