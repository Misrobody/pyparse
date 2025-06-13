import os, ast

class FileInfo:
    def __init__(self, path, name, modulepath):
        self._path = path
        self._name = name
        self._modulepath = modulepath
        self._module = f"{self._modulepath}.{self.base_name}"
        self._global_vars = []
 
    @property
    def full_path(self):
        return os.path.join(self._path, self._name) 
 
    @property
    def base_name(self):
        file_name, _ = os.path.splitext(self._name)
        return file_name 
    
    @property
    def module(self):
        return self._module
    
    @property
    def vars(self):
        return self._global_vars
    
    @property
    def name(self):
        return self._name
        
    def get_ast(self): 
        with open(self.full_path, "r") as file:
            content = file.read()
        tree = ast.parse(content)
        return tree
    
    def add_global_var(self, var):
        self._global_vars.append(var)
    
    def __repr__(self):
        return "(" + self._modulepath + ", " + self._name + ")"