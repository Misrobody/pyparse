import ast
from utils import *
from tools.Context import *
from collections import defaultdict
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

def operation_dict(op_list):
    dict = defaultdict(list)
    for op in op_list:
        dict[op.name].append(op)
    return dict

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

def resolve_callees(call_table, operation_dict):
    count = 0
    for opcall in call_table:
        if opcall.callee.name in operation_dict:
            opcall.callee = operation_dict[opcall.callee.name][0]
            count += 1
    return count
  
def resolve_modules(call_table, imports):
    count = 0
    for module_name in imports:       
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue       
        for opcall in call_table:
            if hasattr(module, opcall.callee.name) and opcall.is_resolved():
                opcall.callee.module = module_name
                count +=1
    return count

    

