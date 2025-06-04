import importlib, builtins, sys
from utils import *

class CallResolver:
    def __init__(self, ops_dict, calls, imports):
        self.ops_dict = ops_dict
        self.calls = calls
                
        default_imports = list(sys.stdlib_module_names)
        default_imports.remove("this")
        self.all_imports = list(set(default_imports) | set(imports))
        self.imported_modules = self._list_imported_modules()
        
        self.callees = 0
        self.modules = 0
        self.methods = 0
                              
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
                obj = getattr(builtins, t)()  # Try creating an instance
                if hasattr(obj, method_name):
                    return True
            except (TypeError, RuntimeError):
                pass  # Skip types that require arguments or cause instantiation errors   
        return False   

    def resolve_all(self):       
        for opcall in self.calls:
            if opcall.callee.name in self.ops_dict:
                opcall.callee = self.ops_dict[opcall.callee.name][0]
                self.callees +=1

            elif opcall.root() in self.ops_dict:
                opcall.callee = self.ops_dict[opcall.root()][0]
                self.callees +=1
                
            elif self._find_method_in_builtin(opcall.root()):
                opcall.callee.module = "builtins"
                opcall.callee.path = "<import-method>"
                self.methods += 1
            
            else:
                for m in self.imported_modules:
                    if hasattr(m, opcall.root()):
                        opcall.callee.module = m.__name__
                        opcall.callee.path = "<import>"
                        self.modules +=1 
                        break
        return self.calls
           
    def stats(self):
        stats = {}
        stats["total"] = len(self.calls)
        stats["total_resolved"] = self.callees + self.modules + self.methods
        stats["total_unresolved"] = stats["total"] - stats["total_resolved"]
        stats["in-app"] = self.callees
        stats["out-app"] = self.modules + self.methods
        stats["modules"] = self.modules
        stats["methods"] = self.methods
        return stats
        
        
        
    