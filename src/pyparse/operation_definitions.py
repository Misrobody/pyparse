import ast
from csv_export import *
from utils import *
from tools.Operation import *
from collections import defaultdict

'''
Collect operation definitions in a given class node
'''
def collect_methods(path, tree):
    methods = []
    current_class = tree.name
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            operation = Operation(path, file_name(path), current_class + "." + node.name)
            methods.append(operation) 
    return methods

'''
Collect function definitions in a given file
'''
def collect_functions(path, tree):
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not is_method(node):
            operation = Operation(path, file_name(path), node.name)
            functions.append(operation) 
    return functions

'''
Convert a class node list to an operation list
'''
def classes_as_operations(path, classes):
    ops = []
    for c in classes:
        ops.append(Operation(path, file_name(path), c.name))
    return ops

'''
Collect operation definitions (functions and methods) in a given file
Classes also count as operations (can be instanciated)
'''
def collect_operations(path):
    tree = get_ast(path)  
    classes = collect_classes(tree)
    class_ops = classes_as_operations(path, classes)
    function_ops = collect_functions(path, tree)
    method_ops = []
    for c in classes:
        method_ops += collect_methods(path, c)
    return function_ops + method_ops + class_ops

'''
Collect operation definitions in a given directory
'''
def operation_list(source_dir): 
    all_operations = []  
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                source_file = os.path.join(root, file)
                all_operations += collect_operations(source_file)                      
    return all_operations

'''
Build an efficient data struct for operation research
'''
def operation_dict(op_list):
    dict = defaultdict(list)
    for op in op_list:
        dict[op.name].append(op)
    return dict

'''
Find an operation in a given operation dict
'''
def find_operations(name, dict):
    return dict.get(name, [])