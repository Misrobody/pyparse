import ast
from termcolor import colored
from State import *
from call.OperationCall import *
from dataflow.DataCall import *

class Operation:
    def __init__(self, path, module, name, state):
        self.path = path
        self.module = module
        self.name = name
        self.state = state
   
    def __repr__(self):
        res = f"({self.path}, {self.module}, {self.name})"
        if self.name == "":
            color = "magenta"
        elif self.state == State.UNRESOLVED:
            color = "cyan"
        elif self.state == State.UNKNOWN:
            color = "red"
        elif self.state == State.IMPORTED:
            color = "yellow"
        elif self.state == State.METHOD:
            color = "blue"
        elif self.state == State.FOUND:
            color = "green"
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
            if isinstance(other, OperationCall) or isinstance(other, DataCall):
                if self.name == other.callee.name:
                    other.update_callee_origin(self.path, self.module)
            return False
        
    def __hash__(self):
        return hash((self.path, self.module, self.name))

