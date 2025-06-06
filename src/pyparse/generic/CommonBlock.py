from termcolor import colored

class CommonBlock:
    def __init__(self, name):
        self.name = name
        self.vars = []
        self.files = []
        self.modules = []
        
    def addCaller(self, caller):
        self.vars.append(caller)
        
    def __repr__(self):
        res = self.name + " \n\tvars:\n"
        
        for v in self.vars:
            res += "\t" + str(v) + "\n"
            
        if not self.files and not self.modules and not self.vars:
            return colored(res, "red")
        return res