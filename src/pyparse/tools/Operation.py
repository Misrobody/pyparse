import ast

class Operation:
    def __init__(self, path, module, name):
        self.path = path
        self.module = module
        self.name = name

    def __repr__(self):
        return f"({repr(self.module)}, {self.name})"

    def export(self):
        return self.module, self.name