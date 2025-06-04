import ast
from utils import *
from tools.CallContext import CallContext

class CallSearch:
    def __init__(self, source_dir):
        self.source_dir = source_dir
        
        self.all_operations = []
        self.all_calls = []
        self.all_imports = []

    def search(self):
        self._go_over()
        return operation_dict(self.all_operations), self.all_calls, list(set(self.all_imports))

    def _go_over(self):          
        for root, _, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith(".py"):
                    source_file = os.path.join(root, file)             
                    operations, calls, imports = self._depth_first_search(source_file)
                    self.all_operations += operations
                    self.all_calls += calls
                    self.all_imports += imports
                                                    
    def _depth_first_search(self, path):
        calls = []
        operations = []
        imports = []
        context = CallContext(path)

        def _walk_search(node, level):
            if gen_empty(ast.iter_child_nodes(node)):
                return

            if isinstance(node, ast.FunctionDef):
                context.update_func(node, level)
                operations.append(context.build_operation_definition())
            if isinstance(node, ast.ClassDef):
                context.update_class(node)
                operations.append(context.build_class_definition())
            if isinstance(node, ast.Call):
                calls.append(context.build_call(node, level))
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            for child in ast.iter_child_nodes(node):
                _walk_search(child, level + 1)

        _walk_search(get_ast(path), 0)
        return operations, calls, imports
