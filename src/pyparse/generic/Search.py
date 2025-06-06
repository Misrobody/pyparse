import os
from utils import *

class Search:
    def __init__(self, source_dir):
        self.source_dir = source_dir
        
        self.all_calls = []
        self.all_operations = []
        self.all_imports = set()
    
    def ops(self):
        return operation_dict(self.all_operations)
    
    def calls(self):
        return self.all_calls
    
    def imports(self):
        return list(self.all_imports)    
    
    def search(self):          
        for root, _, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith(".py"):
                    source_file = os.path.join(root, file)             
                    self._depth_first_search(source_file)
                                                    
    def _depth_first_search(self, path):
        pass


