from State import *
from dataflow.CommonBlock import *

class DataflowResolver():  
    def __init__(self, searcher, external=None, verbose=False):
        self._searcher = searcher
        self._external = external
        self._verbose = verbose
        
        # Make a list of all the datacalls definitions
        self._data = set()
        for call in self._searcher.datacalls:
            self._data.add(call.caller)
        self._data = list(self._data)
        
        # Make list of common blocks based on classes (attr) and files (global_vars)
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
        for i, call in enumerate(self._searcher.datacalls, start=1):
            if self._verbose:
                print(f"[INFO] [Dataflow] Resolving {i}/{len(self._searcher._opcalls)}: {call}")
            
            call in self._data
            for b in self._common_blocks:
                call in b.vars
            call in self._searcher.funcs
            call in self._searcher.classes
            call in self._searcher.import_froms
            call in self._searcher.iterator_vars
            if self._external:
                self._external.resolve_external_call(call)        
        
        
        
    