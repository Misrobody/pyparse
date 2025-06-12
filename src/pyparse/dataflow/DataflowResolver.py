from State import *
from ExternalOpsComparator import *
from dataflow.CommonBlock import *

class DataflowResolver():  
    def __init__(self, searcher, external):
        self._searcher = searcher
        self._ext = ExternalOpsComparator(self._searcher.imports)
        self._external = external
        
        self._data = set()
        for call in self._searcher.datacalls:
            self.data.add(call.caller)
        self._data = list(self._data)
        
        self._common_blocks = []
        to_parse = list(self._searcher.classes) + self._searcher.files
        for elem in to_parse:
            b = CommonBlock(elem.name)
            b.vars.extend(elem.vars)
            if not b.empty():
                self._common_blocks.append(b)
                      
    @property             
    def common_blocks(self):
        return self._common_blocks
    
    @property
    def datacalls(self):
        return self._searcher.datacalls
    
    @property
    def data(self):
        return self._data
                                                                         
    def resolve_all(self):
        for call in self._searcher.datacalls:
            call in self._data
            for b in self._common_blocks:
                call in b.vars
            call in self._searcher.funcs
            call in self._searcher.classes
            call in self._searcher.import_froms
            if self._external:
                self._ext.resolve_external_call(call)
            
            
            
        
        
        
    