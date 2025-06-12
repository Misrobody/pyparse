from State import *
from ExternalOpsComparator import *

class CallResolver():  
    def __init__(self, searcher):
        self._searcher = searcher
        self._ext = ExternalOpsComparator(self._searcher.imports)
        
        self._ops = self._searcher.funcs
        self._ops.extend(self._searcher.import_froms)
        for c in self._searcher.classes:
            self._ops.append(c.as_operation())
        
    @property
    def ops(self):
        return self._ops
    
    @property
    def opcalls(self):
        return self._searcher.opcalls
                    
    def resolve_all(self):       
        for opcall in self._searcher._opcalls:
            opcall in self._searcher.funcs
            opcall in self._searcher.classes
            opcall in self._searcher.import_froms
            self._ext.resolve_external_call(opcall)
        
        
        
    