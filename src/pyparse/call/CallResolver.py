from State import *

class CallResolver():  
    def __init__(self, searcher, external=None, verbose=False):
        self._searcher = searcher
        self._external = external
        self._verbose = verbose
        
        # Make a list of all the involved operations (funcs + importfroms + classdefs)
        self._ops = []
        for f in self._searcher.funcs:
            self._ops.append(f.as_operation())
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
        i = 0 
        for opcall in self._searcher._opcalls:
            i += 1
            if self._verbose:
                print("[INFO] [Call] Resolving "  + str(i) + "/" + str(len(self._searcher._opcalls)) + ": " + str(opcall))            
            
            opcall in self._searcher._funcs
            opcall in self._searcher.classes
            opcall in self._searcher.import_froms
            if self._external:
                self._external.resolve_external_call(opcall)
            
            if self._verbose:
                print("[INFO] [Call] Resolved "  + str(i) + "/" + str(len(self._searcher._opcalls)) + ": " + str(opcall))    
        
        
        
    