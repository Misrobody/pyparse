import ast
from utils import *
from tools.Context import *

def depth_first_search(path):
    calls = []
    context = Context(path)

    def _walk_search(node, level):
        if gen_empty(ast.iter_child_nodes(node)):
            return

        if isinstance(node, ast.ClassDef):
            context.update_class(node)
        elif isinstance(node, ast.FunctionDef):
            context.update(node, level)
        elif isinstance(node, ast.Call):
            calls.append(context.build_call(node, level))

        for child in ast.iter_child_nodes(node):
            _walk_search(child, level + 1)

    _walk_search(get_ast(path), 0)
    return calls

def call_table(source_dir):
    all_calls = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                all_calls.extend(depth_first_search(os.path.join(root, file)))
    return all_calls

def resolve_callees(call_table, operation_dict):
    count = 0
    for opcall in call_table:
        if opcall.callee.name in operation_dict:
            opcall.callee = operation_dict[opcall.callee.name][0]
            count += 1
    return count  

    

