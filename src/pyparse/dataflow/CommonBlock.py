from termcolor import colored
from dataflow.DataCall import *

class CommonBlock:
    def __init__(self, name):
        self.name = name
        self.vars = []
        
    def addCaller(self, caller, direction):
        self.vars.append((caller, direction))
        
    def __repr__(self):
        res = self.name + " \n\tvars:\n"      
        for v in self.vars:
            res += "\t" + str(v) + "\n"           
        if not self.vars:
            return colored(res, "red")
        return res
    
    def empty(self):
        return len(self.vars) == 0
    
    def export(self):
        vars = []
        files = []
        modules = []
        for v in self.vars:
            vars.append(v.name)
            files.append(v.path)
            modules.append(v.module)
        return (self.name, files.__repr__(), modules.__repr__(), vars.__repr__())
    
    def export_dataflow_cb(self):
        res = []
        for v in self.vars:
            res.append((self.name, v.path, v.module, v.name, "WRITE"))
        return res
        
    