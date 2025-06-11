import ast
from termcolor import colored
from State import *

class Operation:
    def __init__(self, path, module, name):
        self.path = path
        self.module = module
        self.name = name

    def is_not_found(self):
        return self.module == State.UNKNOWN and self.path == State.UNKNOWN
    
    def is_from_import(self):
        return self.path == State.IMPORTED
        
    def is_from_method(self):
        return self.path == State.METHOD
    
    def is_unresolved(self):
        return self.name == State.UNRESOLVED
    
    def is_empty_name(self):
        return self.name == ""
    
    def __repr__(self):
        res = f"({self.path}, {self.module}, {self.name})"
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

    
    