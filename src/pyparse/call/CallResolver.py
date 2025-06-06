import importlib, builtins, sys
from tools.Resolver import *
from utils import *

class CallResolver(Resolver):  
    def __init__(self, callsearcher):
        super().__init__(callsearcher)
        self.ops_dict = callsearcher.ops()
        self.calls = callsearcher.calls()
                      
        self.callees = 0
        self.modules = 0
        self.methods = 0
              
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
        
        
        
    