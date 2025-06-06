import os

class Search:
    def __init__(self, source_dir):
        self.source_dir = source_dir
    
    def search(self):          
        for root, _, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith(".py"):
                    source_file = os.path.join(root, file)             
                    self._depth_first_search(source_file)
                                                    
    def _depth_first_search(self, path):
        pass


