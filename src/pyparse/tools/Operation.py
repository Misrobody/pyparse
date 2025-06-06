import ast
from termcolor import colored

class Operation:
    def __init__(self, path, module, name):
        self.path = path
        self.module = module
        self.name = name

    def __repr__(self):
        res = f"({repr(self.path)}, {self.name})"
        if self.name == "":
            return colored(res, "magenta")
        if self.name == "<unresolved>":
            return colored(res, "cyan")
        elif self.module == "<unknown>" and self.path == "<unknown>":
            return colored(res, "red")
        elif self.path == "<import>":
            return colored(res, "yellow")
        elif self.path == "<import-method>":
            return colored(res, "blue")
        return res

    def export(self):
        return self.module, self.name