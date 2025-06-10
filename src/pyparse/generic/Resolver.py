import importlib, builtins, sys
from utils import *

class Resolver:  
    def __init__(self, searcher):
        self.ops_dict = searcher.ops()
                
        default_imports = list(sys.stdlib_module_names)
        default_imports.remove("this")
        default_imports.remove("antigravity")
        self.all_imports = list(set(default_imports) | set(searcher.imports()))
        self.imported_modules = self._list_imported_modules()
                  
    def resolved_ops(self):
        return self.ops_dict
    
    def _list_imported_modules(self):
        imported_modules = []
        for module_name in self.all_imports:       
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