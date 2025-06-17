import sys, ast, os
from termcolor import colored
from collections import defaultdict
from difflib import SequenceMatcher


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
        
def dump_dict(dict):
    for el in dict:
        print(str(el) + ":\n" + str(dict[el]))
      
def longest_common_substring(str1: str, str2: str) -> str:
    match = SequenceMatcher(None, str1, str2).find_longest_match(0, len(str1), 0, len(str2))
    return str1[match.a: match.a + match.size].strip("/") if match.size > 0 else ""

'''
def resolve_name_utils(node):
    name_parts = [] 
    while isinstance(node, (ast.Attribute, ast.Call, ast.Subscript)):
        if isinstance(node, ast.Attribute):
            name_parts.append(node.attr)
        elif isinstance(node, ast.Subscript):
            name_parts.append(self.resolve_name(node.value))
        node = node.value if isinstance(node, (ast.Attribute, ast.Subscript)) else node.func    
    if isinstance(node, ast.Name):
        name_parts.append(node.id)          
    return ".".join(reversed(name_parts))
'''