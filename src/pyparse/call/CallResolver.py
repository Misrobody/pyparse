import importlib, builtins, sys
from generic.Resolver import *

class CallResolver(Resolver):  
    def __init__(self, callsearcher):
        super().__init__(callsearcher)
        self.ops_dict = callsearcher.ops()
        self.calls = callsearcher.calls()
                                      
        self.stats["callees"] = 0
        self.stats["modules"] = 0
        self.stats["methods"] = 0  
              
    def resolve_all(self):       
        for opcall in self.calls:
            if opcall.callee.name in self.ops_dict:
                opcall.callee = self.ops_dict[opcall.callee.name][0]
                self.stats["callees"] +=1
            elif opcall.root() in self.ops_dict:
                opcall.callee = self.ops_dict[opcall.root()][0]
                self.stats["callees"] +=1             
            elif self._find_method_in_builtin(opcall.root()):
                opcall.callee.module = "builtins"
                opcall.callee.path = "<import-method>"
                self.stats["methods"] += 1          
            else:
                for m in self.imported_modules:
                    if hasattr(m, opcall.root()):
                        opcall.callee.module = m.__name__
                        opcall.callee.path = "<import>"
                        self.stats["modules"] +=1 
                        break
        
        
        
    