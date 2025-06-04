import ast
from utils import *
from tools.Context import *
import importlib

def go_over(source_dir):   
    all_operations = []
    all_calls = []
    all_imports = []
    
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                source_file = os.path.join(root, file)             
                operations, calls, imports = depth_first_search(source_file)
                all_operations += operations
                all_calls += calls
                all_imports += imports
                                                   
    return operation_dict(all_operations), all_calls, list(set(all_imports))

def depth_first_search(path):
    calls = []
    operations = []
    imports = []
    context = Context(path)

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
