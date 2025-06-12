import importlib, builtins, sys
from utils import *
from State import *

class ExternalOpsComparator:  
    def __init__(self, imports):
        self._imports = imports
                 
        self._default_imports = list(sys.stdlib_module_names)
        self._default_imports.remove("this")
        self._default_imports.remove("antigravity")
        
        self._all_imports = list(set(self._default_imports) | set(self._imports))
        self._imported_modules = self._import_modules()
      
    def _import_modules(self):
        imported_modules = []
        for module_name in self._all_imports:       
            try:
                module = importlib.import_module(module_name)  
                imported_modules.append(module)             
            except ModuleNotFoundError:
                continue  
        return imported_modules
                
    def _find_method_in_builtin(self, method_name):
        builtin_types = [name for name in dir(builtins) if isinstance(getattr(builtins, name), type)]   
        for t in builtin_types:
            try:
                obj = getattr(builtins, t)()
                if hasattr(obj, method_name):
                    return True
            except (TypeError, RuntimeError):
                pass  
        return False
          
    def resolve_external_call(self, call):   
        for m in self._imported_modules:
            if hasattr(m, call.callee.name):
                call.update_callee_origin(m.__name__, m.__name__, state=State.IMPORTED)
                return
        if self._find_method_in_builtin(call.callee.name):
            call.update_callee_origin("builtins", "builtins", state=State.METHOD)
            return