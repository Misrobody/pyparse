import importlib, builtins, sys

class CallResolver:
    def __init__(self, calls):
        self.calls = calls
        self.callees = 0
        self.modules = 0
        self.methods = 0

    def _resolve_callees(self, operation_dict): 
        for opcall in self.calls:
            if opcall.callee.name in operation_dict:
                opcall.callee = operation_dict[opcall.callee.name][0]
                self.callees +=1
            elif opcall.callee.name.split(".")[-1] in operation_dict:
                opcall.callee = operation_dict[opcall.callee.name.split(".")[-1]][0]
                self.callees +=1
   
    def _resolve_modules(self, imports):
        for module_name in imports:       
            try:
                module = importlib.import_module(module_name)
            except ModuleNotFoundError:
                continue       
            for opcall in self.calls:
                if hasattr(module, opcall.callee.name.split(".")[-1]) and opcall.is_unresolved():
                    opcall.callee.module = module_name
                    opcall.callee.path = "<import>"
                    self.modules +=1

    def _resolve_default_methods(self):
        for opcall in self.calls:
            if self._find_method_in_builtin(opcall.callee.name.split(".")[-1]):
                opcall.callee.module = "builtins"
                opcall.callee.path = "<import>"
                self.methods += 1
    
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

    def resolve_all(self, ops_dict, imports, builtin=False, external=False):      
        self._resolve_callees(ops_dict)
        
        # Search in the default Python library
        if external:
            default_imports = list(sys.stdlib_module_names)
            default_imports.remove("this")
            self._resolve_modules(default_imports)
            self._resolve_default_methods()
        
        # Search in the modules imported from the app
        if builtin:
            self._resolve_modules(imports)   
                                
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
        
        
        
    