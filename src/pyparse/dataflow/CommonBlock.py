from termcolor import colored

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
    
    def export(self):
        vars = []
        files = []
        modules = []
        for v in self.vars:
            vars.append(v[0].name)
            files.append(v[0].path)
            modules.append(v[0].module)
        return (self.name, files.__repr__(), modules.__repr__(), vars.__repr__())
    
    def export_dataflow_cb(self):
        res = []
        for v in self.vars:
            res.append((self.name, v[0].path, v[0].module, v[0].name, v[1]))
        return res
    