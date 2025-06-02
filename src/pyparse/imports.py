'''
import importlib

import ast
from csv_export import *
from utils import *
from tools.Operation import *


module_name = "ast"
module = importlib.import_module(module_name)

print(module)  # <module 'ast' from '...'>
print(hasattr(module, "dump"))  # True

def collect_modules_aliases(tree):
    modules = []
    operations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):         
            modules += node.names
        if isinstance(node, ast.ImportFrom):
            modules.append(ast.alias(node.module, None))
    return modules

def collect_operations_aliases(tree):
    operations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            operations += node.names
    return operations

def malias_list(source_dir): 
    all_operations = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                source_file = os.path.join(root, file)
                all_operations += collect_modules_aliases(source_file)                      
    return all_operations

def opalias_list(source_dir): 
    all_operations = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                source_file = os.path.join(root, file)
                all_operations += collect_operations_aliases(source_file)                      
    return all_operations
'''