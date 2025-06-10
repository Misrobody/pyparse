import importlib, builtins, sys
from utils import *
from generic.Resolver import *

class DataflowResolver(Resolver):  
    def __init__(self, dataflow_searcher):
        super().__init__(dataflow_searcher)
        self.datacalls = dataflow_searcher.datacalls()
        self.datacalls_dict = call_dict(self.datacalls)
        
        self.common_blocks = dataflow_searcher.common_blocks()
        self.ops_dict = dataflow_searcher.ops()
                     
    def resolved_common_blocks(self):
        return self.common_blocks
    
    def resolved_calls(self):
        return self.datacalls
                                                                         
    def resolve_all(self):
        for call in self.datacalls:
            if not call.is_unresolved():
                continue
            
            if call.callee.name in self.ops_dict:
                call.set_callee(self.ops_dict[call.callee.name][0])           
            elif call.callee.root() in self.ops_dict:
                call.set_callee(self.ops_dict[call.callee.root()][0])                                
            elif call.callee.name in self.datacalls_dict:
                call.set_callee(self.datacalls_dict[call.callee.name]) 
            elif call.callee.root() in self.datacalls_dict:
                call.set_callee(self.datacalls_dict[call.callee.root()])            
            elif self._find_method_in_builtin(call.callee.root()):
                call.callee.module = "builtins"
                call.callee.path = "<import-method>"         
            else:
                for m in self.imported_modules:
                    if hasattr(m, call.callee.root()):
                        call.callee.module = m.__name__
                        call.callee.path = "<import>"
                        break
        
        
        
    