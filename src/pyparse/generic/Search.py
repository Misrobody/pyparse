import os
from utils import *
from generic.Context import *
from generic.ClassInfo import *
from generic.FileInfo import *

class Search:
    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.context = Context()
        
        self._opcalls = []
        self._datacalls = []

        self._imports = set()
        self._import_froms = []

        self._classes = {}
        self._funcs = []
        self._files = []
        
    @property
    def opcalls(self):
        return self._opcalls    
    
    @property
    def datacalls(self):
        return self._datacalls
    
    @property
    def funcs(self):
        return self._funcs
    
    @property
    def imports(self):
        return list(self._imports)    
    
    @property
    def classes(self):
        return self._classes.values()
    
    @property
    def files(self):
        return self._files
    
    # remove root module itself from import_froms ?
    @property
    def import_froms(self):
        return self._import_froms
    
    def search(self):                
        current_module = ""
        for dirpath, dirnames, filenames in os.walk(self.source_dir): 
            
            # resolve module name        
            if "__init__.py" in filenames:         
                parent_dir = os.path.dirname(dirpath)
                if parent_dir.endswith(current_module):
                    new_module = f"{current_module}/{file_name(dirpath)}"
                else:
                    new_module = f"{longest_common_substring(current_module, parent_dir)}{file_name(dirpath)}"
                current_module = new_module    
                
            # parse files                      
            for file in filenames:              
                if file.endswith(".py"):
                    fileInfo = FileInfo(dirpath, file, current_module.strip("/").replace("/", "."))
                    self._files.append(fileInfo)
                    self.context.update_file(fileInfo)
                    self._depth_first_search()
                                                                              
    def _depth_first_search(self):
        def _walk_search(node, parent=None):
            if not any(ast.iter_child_nodes(node)):  
                return
                        
            if isinstance(node, ast.ClassDef):
                classInfo = self.context.build_class(node)
                self.context.update_class(classInfo)
                self._classes[node.name] = classInfo
                           
            elif isinstance(node, ast.FunctionDef):
                self.context.update_func(node)
                func = self.context.build_func(node)
                if is_method(node) or is_static_method(node):
                    self._classes[self.context.cur_class_name].add_method(func)
                else:
                    self._funcs.append(func)
            
            elif isinstance(node, ast.Call):
                self._opcalls.append(self.context.build_call(node))
            
            elif isinstance(node, ast.Import):
                self._imports.update(alias.name for alias in node.names) 
                 
            elif isinstance(node, ast.ImportFrom):
                self._import_froms.extend(self.context.build_import_froms(node)) 
                
            elif isinstance(node, ast.Assign) or isinstance(node, ast.AnnAssign) or isinstance(node, ast.AugAssign):
                self._datacalls.extend(self.context.build_datacalls(node, parent))

            for child in ast.iter_child_nodes(node):
                _walk_search(child, node)

        _walk_search(self.context.file.get_ast(), None)