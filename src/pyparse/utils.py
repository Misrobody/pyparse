import sys, ast, os

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
Return class nodes for a given ast
'''     
def collect_classes(tree):
    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node)    
    return classes

'''
Check if ast node is a method
'''
def is_method(node):
    return node.args.args and node.args.args[0].arg == "self"

'''
Check if call name is a method
'''
def is_method_call(name):
    return "self" in name or "super" in name
