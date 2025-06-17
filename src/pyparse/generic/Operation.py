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
        res = f"(STATE: {self.state}, {self.module}, {self.name})"
        if self.state == State.UNKNOWN:
            color = "red"
        elif self.state == State.IMPORTED:
            color = "yellow"
        elif self.state == State.FOUND:
            color = "green"
        elif self.state == State.CLASS:
            color = "cyan"
        elif self.state == State.ITERVAR:
            color = "dark_grey"
        elif self.state == State.PARAM:
            color = "magenta"
        else:
            color = "white"
        return colored(res, color)

    def export(self):
        return self.module, self.name
       
    def __eq__(self, other):
            if isinstance(other, Operation):
                return self.name == other.name and self.path == other.path and self.module == other.module           
            if isinstance(other, OperationCall):
                if self.name == other.callee.name:
                    other.update_callee_origin(self.path, self.module, State.FOUND)
            return False
        
    def __hash__(self):
        return hash((self.path, self.module, self.name))
    
    def update_origin(self, file, module, state):
        self.path = file
        self.module = module
        self.state = state
        
    def is_unresolved(self):
        return not State.isknown(self.state)

