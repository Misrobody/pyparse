import importlib, builtins

def _resolve_callees(call_stack, operation_dict):
    unresolved = []   
    for opcall in call_stack:
        if opcall.callee.name in operation_dict:
            opcall.callee = operation_dict[opcall.callee.name][0]
        elif opcall.callee.name.split(".")[-1] in operation_dict:
            opcall.callee = operation_dict[opcall.callee.name.split(".")[-1]][0]
        else:
            unresolved.append(opcall)
    return unresolved
  
def _resolve_modules(call_stack, imports):
    unresolved = []
    for module_name in imports:       
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue       
        for opcall in call_stack:
            if hasattr(module, opcall.callee.name.split(".")[-1]) and opcall.is_unresolved():
                opcall.callee.module = module_name
                opcall.callee.path = "<import>"
            else:
                unresolved.append(opcall)
    return unresolved

def _resolve_default_methods(call_stack):
    unresolved = []   
    for opcall in call_stack:
        if find_method_in_builtin(opcall.callee.name.split(".")[-1]):
            opcall.callee.module = "builtins"
            opcall.callee.path = "<import>"
        else:
            unresolved.append(opcall)
    return unresolved   
   

def find_method_in_builtin(method_name):
    builtin_types = [name for name in dir(builtins) if isinstance(getattr(builtins, name), type)]
    
    for t in builtin_types:
        try:
            obj = getattr(builtins, t)()  # Try creating an instance
            if hasattr(obj, method_name):
                return True  # Method found in a built-in type
        except (TypeError, RuntimeError):
            pass  # Skip types that require arguments or cause instantiation errors
    
    return False  # Method not found in any built-in type  

def resolve_all(call_table, ops_dict, imports):
    _resolve_callees(call_table, ops_dict)
    _resolve_modules(call_table, imports)
    _resolve_default_methods(call_table)

    
    return call_table



'''
def resolve_all(call_table, ops_dict, imports):
    total = len(call_table)
    unresolved_calls = _resolve_callees(call_table, ops_dict)
    internal = total - len(unresolved_calls)
    unresolved_calls = _resolve_modules(unresolved_calls, imports)
    external = total - len(unresolved_calls)
    unresolved = total - (external + internal)
    resolved = total - unresolved
    
    print("[INFO] Resolved " + str(resolved) + " out of " + str(total) + " callees")
    print("[INFO] " + str(internal) + " internal resolution")
    print("[INFO] " + str(external) + " external resolution")
    
    if unresolved == 0:
        print("[INFO] All callees resolved")
    else:
        print("[INFO] Still " + str(unresolved) + " unresolved callees")
        
    return call_table
'''
    