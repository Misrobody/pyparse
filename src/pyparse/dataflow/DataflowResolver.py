import importlib, builtins, sys
from utils import *
from generic.Resolver import *

class DataflowResolver(Resolver):  
    def __init__(self, dataflow_searcher):
        super().__init__(dataflow_searcher)
        self.datacalls = dataflow_searcher.calls()
        self.datacalls_dict = call_dict(self.datacalls)
        
        self.common_blocks = dataflow_searcher.common_blocks()
        self.ops_dict = dataflow_searcher.ops()

        self.stats["func"] = 0
        self.stats["calls"] = 0
                     
    def resolved_common_blocks(self):
        return self.common_blocks
                                               
    def resolve_datacalls(self):       
        for call in self.datacalls:
            if not call.is_unresolved():
                continue
            
            if call.callee.name in self.ops_dict:
                call.set_callee(self.ops_dict[call.callee.name][0])
                self.stats["func"] += 1              
            elif call.callee.root() in self.ops_dict:
                call.set_callee(self.ops_dict[call.callee.root()][0])
                self.stats["func"] += 1   
                
                   
            elif call.callee.name in self.datacalls_dict:
                call.set_callee(self.datacalls_dict[call.callee.name])
                self.stats["calls"] += 1   
            elif call.callee.root() in self.datacalls_dict:
                call.set_callee(self.datacalls_dict[call.callee.root()])
                self.stats["calls"] += 1 
                          
                   
    def resolve_all(self):
        self.resolve_datacalls()
        
        
    