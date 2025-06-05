import importlib, builtins, sys
from utils import *

class DataflowResolver:  
    def __init__(self, dataflow_searcher):
        self.datacalls = dataflow_searcher.datacalls()
        self.common_blocks = dataflow_searcher.common_blocks()
                                            
    def resolve_datacalls(self):       
        pass
    
    def resolve_all(self):
        pass
                 
    def stats(self):
        stats = {}
        return stats
        
        
        
    