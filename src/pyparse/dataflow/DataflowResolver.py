from State import *
from dataflow.CommonBlock import *

class DataflowResolver():  
    def __init__(self, searcher, external=None, verbose=False):
        self._searcher = searcher
        self._external = external
        self._verbose = verbose
        self._datacalls = self._searcher.datacalls
        
        # Make a list of all the datacalls definitions
        self._data = list({call.caller for call in self._searcher.datacalls})
        
        # Make list of common blocks based on classes (attr) and files (global_vars)
        self._common_blocks = [
            CommonBlock(elem.name, vars=elem.vars)
            for elem in set(self._searcher.classes) | self._searcher.files
            if elem.vars  # Ensures `CommonBlock` isn't empty
        ]
                      
    @property             
    def common_blocks(self):
        return self._common_blocks
    
    @property
    def datacalls(self):
        return self._datacalls
    
    @property
    def data(self):
        return self._data
                                                                         
    def resolve_all(self):
        for i, call in enumerate(self._datacalls, start=1):
            if self._verbose:
                print(f"[INFO] [Dataflow] Resolving: {call}")
            
            call in self._data
            for b in self._common_blocks:
                call in b.vars
            call in self._searcher.funcs
            call in self._searcher.classes
            call in self._searcher.import_froms
            call in self._searcher.iterator_vars
            if self._external:
                self._external.resolve_external_call(call)
                
            if self._verbose:
                print(f"[INFO] [Dataflow] Resolved {i}/{len(self._datacalls)}: {call}")    
