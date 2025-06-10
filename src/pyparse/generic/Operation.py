import ast
from termcolor import colored

class Operation:
    def __init__(self, path, module, name):
        self.path = path
        self.module = module
        self.name = name

    def is_not_found(self):
        return self.module == "<unknown>" and self.path == "<unknown>"
    
    def is_from_import(self):
        return self.path == "<import>"
        
    def is_from_method(self):
        return self.path == "<import-method>"
    
    def is_unresolved(self):
        return self.name == "<unresolved>"
    
    def is_empty_name(self):
        return self.name == ""
    
    def __repr__(self):
        res = f"({repr(self.path)}, {self.name})"
        if self.is_empty_name():
            return colored(res, "magenta")
        elif self.is_unresolved():
            return colored(res, "cyan")
        elif self.is_not_found():
            return colored(res, "red")
        elif self.is_from_import():
            return colored(res, "yellow")
        elif self.is_from_method():
            return colored(res, "blue")
        return res

    def export(self):
        return self.module, self.name
    
    def root(self):
        return self.name.split(".")[-1]

    
    