import sys, ast, os
from termcolor import colored
from collections import defaultdict

def get_ast(file):   
    with open(file, "r") as file:
        content = file.read()
    tree = ast.parse(content)
    return tree

def ast_str(tree):
    return ast.dump(tree, indent=4)

def file_name(path):
    base_name = os.path.basename(path)
    file_name, _ = os.path.splitext(base_name)
    return file_name

def dump_list(list):
    for el in list:
        print(el)

def dump_default_dict(ddict):
    max_length = max(len(el) for el in ddict)

    for el in ddict:
        print(f"{el:<{max_length}} : {ddict[el]!r}")
        
'''
Check if ast node is a method
'''
def is_method(node):
    return node.args.args and node.args.args[0].arg == "self"

'''
Check if an AST FunctionDef node is a static method
'''
def is_static_method(node):   
    return any(
        isinstance(decorator, ast.Name) and decorator.id == "staticmethod"
        for decorator in node.decorator_list
    )
    
def depth_first_dump(path):  
    def _walk_dump(node, level=0):
        if gen_empty(ast.iter_child_nodes(node)):
            return
        
        padding = " " * 4 * level
        if isinstance(node, ast.FunctionDef):          
            print(colored(padding + str(node), "red"))
        else:
            print(padding + str(node))
        
        for child in ast.iter_child_nodes(node):
            _walk_dump(child, level+1)
            
    tree = get_ast(path)
    _walk_dump(tree)
    
def operation_dict(op_list):
    dict = defaultdict(list)
    for op in op_list:
        dict[op.name].append(op)
    return dict

def call_dict(datacalls):
    dict = defaultdict(list)
    for call in datacalls:
        dict[call.caller.name].append(call.caller.name)
    return dict