import importlib, sys, inspect
from utils import *
from State import *

class ExternalOpsComparator:  
    def __init__(self, imports):
        self._imports = imports
                 
        self._default_imports = list(sys.stdlib_module_names)
        self._default_imports.remove("this")
        self._default_imports.remove("antigravity")
        
        self._all_imports = list(set(self._default_imports) | set(self._imports))
        self._imported = self._import_modules()
      
    def _import_modules(self):
        imported_modules = {}
        for module_name in self._all_imports:       
            try:
                module = importlib.import_module(module_name)  
                imported_modules[module_name] = module           
            except ModuleNotFoundError:
                continue
        return imported_modules
          
    def method_exists_in_module(self, method_name, module):
        for type_name in dir(module):
            cls = getattr(module, type_name, None)
            if isinstance(cls, type):
                methods = [name for name, _ in inspect.getmembers(cls, predicate=inspect.isfunction)]
                if method_name in methods:
                    return True
        return False
            
    def resolve_external_call(self, call):
        for module_name in self._imported:
            m = self._imported[module_name]
            types = [name for name in dir(m) if isinstance(getattr(m, name), type)] 
            if hasattr(m, call.callee.name):
                call.update_callee_origin(m.__name__, m.__name__, State.IMPORTED)
                return
            elif self.method_exists_in_module(call.callee.name, m):
                call.update_callee_origin(module_name, module_name, state=State.METHOD)
                return