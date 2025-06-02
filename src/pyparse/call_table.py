import ast
from csv_export import *
from utils import *
#from tools.Operation import *
from tools.Link import *
from termcolor import colored

'''
Resolve the name of a given operation call (method or function)
'''
def resolve_name(node):
    name_parts = [] 
    while isinstance(node, (ast.Attribute, ast.Call)):
        if isinstance(node, ast.Attribute):
            name_parts.append(node.attr)
        node = node.value if isinstance(node, ast.Attribute) else node.func    
    if isinstance(node, ast.Name):
        name_parts.append(node.id)   
    return ".".join(reversed(name_parts))

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

###################################################################################""

class Operation:
    def __init__(self, path, module, name):
        self.path = path
        self.module = module
        self.name = name

    def __repr__(self):
        return f"({repr(self.module)}, {self.name})"

    def export(self):
        return self.module, self.name

class Context:
    def __init__(self, filepath):
        self.filepath = filepath
        self.func_node = None
        self.level = 0
        self.class_node = ""

    def update(self, func_node, level):
        self.func_node = func_node
        self.level = level

    def update_class(self, class_node):
        self.class_node = class_node

    def get(self, current_level):
        if self.level == current_level:
            self.update(None, 0)

        if self.func_node is None:
            return ""

        return (
            f"{self.class_node.name}.{self.func_node.name}"
            if is_method(self.func_node)
            else self.func_node.name
        )

    def resolve_super_self(self, name):
        if "self" in name:
            name = name.replace("self", self.class_node.name)
        elif "super" in name and self.class_node.bases:
            name = name.replace("super", resolve_name(self.class_node.bases[0]))
        return name

    def get_name(self, call):
        return self.resolve_super_self(resolve_name(call))

    def build_call(self, call, call_level):
        caller = Operation(self.filepath, file_name(self.filepath), self.get(call_level))
        callee = Operation("<unknown>", "<unknown>", self.get_name(call))
        return OperationCall(caller, callee)

class OperationCall:
    def __init__(self, caller, callee):
        self.caller = caller
        self.callee = callee

    def __repr__(self):
        return f"{repr(self.caller)} --> {repr(self.callee)}"

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

def call_table_test(source_dir):
    all_calls = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                all_calls.extend(depth_first_search(os.path.join(root, file)))
    return all_calls

###################################################################################""  

def callees(call_table, operation_dict):
    count = 0
    for opcall in call_table:
        if opcall.callee.name in operation_dict:
            opcall.callee = operation_dict[opcall.callee.name][0]
            count += 1
    return count

###################################################################################""  

'''
class Operation:
    def __init__(self, path, module, name):    
        # path representing the module
        self.path = path
        # module name
        self.module = module    
        # caller operation name
        self.name = name
        
    def __repr__(self):
        return "(" + self.module.__repr__() + ", " + self.name + ")"
    
    def export(self):
        return (self.module, self.name)  

class Context:
    def __init__(self, filepath):
        self.filepath = filepath
        self.func_node = None
        self.level = 0
        self.class_node = ""
    
    def update(self, func_node, level):
        self.func_node = func_node
        self.level = level
        
    def update_class(self, class_node):
        self.class_node = class_node
        
    def get(self, current_level):
        if self.level == current_level:
            self.update("", 0)

        if self.func_node == None:
            return ""
        
        print(colored(str(self.func_node), "red"))
        ast.dump(self.func_node, indent=4)
        print(self.func_node.name)
        
        if is_method(self.func_node):
            return self.class_node.name + "." + self.func_node.name
        return self.func_node.name
    
    def resolve_super_self(self, name):
        if "self" in name:
            name = name.replace("self", self.class_node.name)
        elif "super" in name:
            if len(self.class_node.bases) != 0:
                name = name.replace("super", resolve_name(self.class_node.bases[0]))   
        return name           
    
    def get_name(self, call):
        name = resolve_name(call)
        name = self.resolve_super_self(name)
        return name
    
    def build_call(self, call, call_level):
        caller = Operation(self.filepath, file_name(self.filepath), self.get(call_level))
        callee = Operation("<unknown>", "<unknown>", self.get_name(call))
        return OperationCall(caller, callee)

class OperationCall:
    def __init__(self, caller, callee):
        # operation 'context' calls operation 'call'
        self.caller = caller
        self.callee = callee
    
    def __repr__(self):
        return (self.caller.__repr__() + " --> " + self.callee.__repr__())
  
def depth_first_search(path):
    print(path)
    calls = []
    context = Context(path)
    def _walk_search(node, level):
        if gen_empty(ast.iter_child_nodes(node)):
            return
        
        if isinstance(node, ast.ClassDef):
            context.update_class(node)
        
        if isinstance(node, ast.FunctionDef):          
            context.update(node, level)
              
        if isinstance(node, ast.Call):          
            calls.append(context.build_call(node, level))
        
        for child in ast.iter_child_nodes(node):
            _walk_search(child, level+1)
            
    tree = get_ast(path)
    _walk_search(tree, 0) 
    return calls
  
def call_table_test(source_dir): 
    all_calls = []
    
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                source_file = os.path.join(root, file)

                # collect calls
                all_calls += depth_first_search(source_file)
                        
    return all_calls
'''
  
####################################################################


  
'''
def depth_first_dump(path):  
    def _walk_dump(node, level=0):
        if gen_empty(ast.iter_child_nodes(node)):
            return
        
        padding = " " * 4 * level
        if isinstance(node, ast.Call):          
            print(colored(padding + str(node), "red"))
        else:
            print(padding + str(node))
        
        for child in ast.iter_child_nodes(node):
            _walk_dump(child, level+1)
            
    tree = get_ast(path)
    _walk_dump(tree)
''' 
    

