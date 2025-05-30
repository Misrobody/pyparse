import ast

class Operation:
    def __init__(self, path, module, name):    
        # path representing the module
        self.path = path
        # module name
        self.module = module    
        # caller operation name
        self.name = name
        
    def __repr__(self):
        return "(" + self.module.__repr__() + ", " + self.name + ")"
    
    def export(self):
        return (self.module, self.name)
    
