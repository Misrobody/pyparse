from State import *

class CallResolver():  
    def __init__(self, searcher, external=None, verbose=False):
        self._searcher = searcher
        self._external = external
        self._verbose = verbose
        self._opcalls = self._searcher._opcalls
        
        # Make a list of all the involved operations (funcs + importfroms + classdefs)       
        self._ops = set(f.as_operation() for f in self._searcher.funcs) | \
            self._searcher.import_froms | \
            set(c.as_operation() for c in self._searcher.classes)
        
    @property
    def ops(self):
        return self._ops
    
    @property
    def opcalls(self):
        return self._searcher.opcalls
                    
    def resolve_all(self):     
        for i, opcall in enumerate(self._opcalls, start=1):
            if self._verbose:
                print(f"[INFO] [Call] Resolving {i}/{len(self._opcalls)}: {opcall}")
            
            opcall in self._searcher._funcs
            opcall in self._searcher.classes
            opcall in self._searcher.import_froms
            
            if self._external:
                self._external.resolve_external_call(opcall)

            if self._verbose:
                print(f"[INFO] [Call] Resolved {i}/{len(self._opcalls)}: {opcall}")

    