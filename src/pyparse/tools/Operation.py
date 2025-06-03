import ast
from termcolor import colored

class Operation:
    def __init__(self, path, module, name):
        self.path = path
        self.module = module
        self.name = name

    def __repr__(self):
        res = f"({repr(self.module)}, {self.name})"
        if self.module == "<unknown>":
            return colored(res, "red")
        return res

    def export(self):
        return self.module, self.name