import ast
from csv_export import *
from utils import *
from tools.Operation import *
from tools.Link import *

'''
Aux function to resolve_name
'''
def resolve_name_rec(node, name):
    if isinstance(node, ast.Name):
        name.append(node.id)
    elif isinstance(node, ast.Attribute):
        name.append(node.attr)
        return resolve_name_rec(node.value, name)
    elif isinstance(node, ast.Call):
        return resolve_name_rec(node.func, name)
    return name

'''
Resolve the name of a given operation call (method or function)
'''
def resolve_name(node):
    my_list = resolve_name_rec(node, [])
    reversed_list = my_list[::-1]  
    result = ".".join(reversed_list)
    return result

################################################################

'''
Collect function calls in a given file
'''
def collect_function_calls(path, tree):
    calls = []  
    for node in ast.walk(tree):          
        if isinstance(node, ast.Call):
            name = resolve_name(node)
            if not is_method_call(name):
                operation = Operation(path, file_name(path), name)
                link = Link(operation)
                calls.append(link)
    return calls

'''
Collect function calls in a given class node
'''
def collect_method_calls(path, tree):
    calls = []
    for node in ast.walk(tree):          
        if isinstance(node, ast.Call):
            name = resolve_name(node)
            if is_method_call(name):
                if "self" in name:
                    name = name.replace("self", tree.name)
                elif "super" in name:
                    if len(tree.bases) != 0:
                        name = name.replace("super", resolve_name(tree.bases[0]))
                operation = Operation(path, file_name(path), name)
                link = Link(operation)
                calls.append(link)
    return calls

'''
Collect call definitions in a given file
'''
def collect_calls(path):
    tree = get_ast(path)
    function_calls = collect_function_calls(path, tree)
    classes = collect_classes(tree)
    method_calls = []
    for c in classes:
        method_calls += collect_method_calls(path, c)
    return function_calls + method_calls

'''
Collect call definitions in a given directory
'''
def call_table(source_dir): 
    all_calls = []
    
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                source_file = os.path.join(root, file)

                # collect calls
                all_calls += collect_calls(source_file)
                        
    return all_calls

'''
Resolve callees
'''
def resolve_callees(call_table, operation_dict):
    count = 0
    for link in call_table:
        if link.caller.name in operation_dict:
            # @TODO: Resolve conflit when same op name. Don't always take the first one
            link.callee = operation_dict[link.caller.name][0]
            count += 1
    return count
