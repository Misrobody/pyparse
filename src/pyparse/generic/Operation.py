import ast
from termcolor import colored
from State import *
from call.OperationCall import *

class Operation:
    def __init__(self, path, module, name, state):
        self.path = path
        self.module = module
        self.name = name
        self.state = state
   
    def __repr__(self):
        res = f"({self.module}, {self.name})"
        if self.state == State.UNRESOLVED:
            color = "cyan"
        elif self.state == State.UNKNOWN:
            color = "red"
        elif self.state == State.IMPORTED:
            color = "yellow"
        elif self.state == State.METHOD:
            color = "blue"
        elif self.state == State.FOUND:
            color = "green"
        elif self.state == State.CLASS:
            color = "light_grey"
        elif self.state == State.ITERVAR:
            color = "dark_grey"
        elif self.state == State.PARAM:
            color = "magenta"
        else:
            color = "white"
        return colored(res, color)

    def export(self):
        return self.module, self.name
    
    def root(self):
        return self.name.split(".")[-1]
    
    def __eq__(self, other):
            if isinstance(other, Operation):
                return self.name == other.name and self.path == other.path and self.module == other.module           
            if isinstance(other, OperationCall):
                if self.name == other.callee.name:
                    other.update_callee_origin(self.path, self.module, State.FOUND)
            return False
        
    def __hash__(self):
        return hash((self.path, self.module, self.name))

