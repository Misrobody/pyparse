import importlib, builtins, sys
from utils import *

class DataflowResolver:  
    def __init__(self, dataflow_searcher):
        self.datacalls = dataflow_searcher.datacalls()
        self.datacalls_dict = call_dict(self.datacalls)
        
        self.common_blocks = dataflow_searcher.common_blocks()
        self.ops_dict = dataflow_searcher.ops()
                  
        self.func = 0 
        self.calls = 0    
                  
    def resolved_calls(self):
        return self.datacalls
    
    def resolved_ops(self):
        return self.ops_dict
    
    def resolved_common_blocks(self):
        return self.common_blocks
                                               
    def resolve_datacalls(self):       
        for call in self.datacalls:
            if not call.is_unresolved():
                continue
            if call.callee.name in self.ops_dict:
                call.callee = self.ops_dict[call.callee.name][0]
                self.func +=1              
            elif call.root() in self.ops_dict:
                call.callee = self.ops_dict[call.root()][0]
                self.func +=1
                
            elif call.callee.name in self.datacalls_dict:
                call.callee = self.datacalls_dict[call.callee.name][0]
                self.calls +=1              
            elif call.root() in self.datacalls_dict:
                call.callee = self.datacalls_dict[call.root()][0]
                self.calls +=1            
                   
    def resolve_all(self):
        self.resolve_datacalls()
                 
    def stats(self):
        stats = {}
        stats["func"] = self.func
        stats["calls"] = self.calls
        return stats
        
        
        
    