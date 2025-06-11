import os
from utils import *
from generic.Context import *

class Search:
    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.context = Context()
        
        self._opcalls = []
        self._datacalls = []
        self._operations = []
        self._imports = set()
        self._common_blocks = []
        self._classes = {}
        self._class_nodes = []
        self._funcs = []
        
    def common_blocks(self):
        return self._common_blocks
    
    def ops(self):
        return operation_dict(self._operations)
    
    def opcalls(self):
        return self._opcalls
    
    def datacalls(self):
        return self._datacalls
    
    def imports(self):
        return list(self._imports)    
    
    def classes(self):
        return self._classes
    
    def search(self):                
        current_module = "" 
        for dirpath, dirnames, filenames in os.walk(self.source_dir):         
            if "__init__.py" in filenames:         
                parent_dir = os.path.dirname(dirpath)
                if parent_dir.endswith(current_module):
                    new_module = f"{current_module}/{file_name(dirpath)}"
                else:
                    new_module = f"{longest_common_substring(current_module, parent_dir)}/{file_name(dirpath)}"
                current_module = new_module                          
            for file in filenames:              
                if file.endswith(".py"):
                    self._depth_first_search(os.path.join(dirpath, file), current_module.strip("/").replace("/", "."))
        
        # Add super methods with self prefix
        for node in self._class_nodes:
            if node.bases:
                for base in node.bases:        
                    base_name = resolve_name_utils(base).split('.')[-1]
                    if base_name in self._classes:
                        for base_method in self._classes[base_name]:
                            op = Operation(base_method.path, base_method.module, f"{node.name}.{base_method.name.split('.')[-1]}")
                            self._operations.append(op)
                                                           
    def _depth_first_search(self, path, modulepath):
        def _walk_search(node, parent):
            if not any(ast.iter_child_nodes(node)):  
                return

            if isinstance(node, ast.Module):
                self._common_blocks.append(self.context.build_common_block(node))
                
            elif isinstance(node, ast.FunctionDef):
                self.context.update_func(node)
                func_def = self.context.build_operation_definition(node)
                self._operations.append(func_def)
                if is_method(node) or is_static_method(node):
                    if self.context.class_node != None:
                        self._classes[self.context.class_node.name].append(func_def)
                
            elif isinstance(node, ast.ClassDef):
                self.context.update_class(node)
                class_def = self.context.build_class_definition(node)
                self._operations.append(class_def)
                self._classes[node.name] = []
                self._common_blocks.append(self.context.build_common_block(node))
                self._class_nodes.append(node)
                
            elif isinstance(node, ast.Call):
                self._opcalls.append(self.context.build_call(node))
                
            elif isinstance(node, ast.Import):
                self._imports.update(alias.name for alias in node.names) 
                 
            elif isinstance(node, ast.ImportFrom):
                self._operations.extend(self.context.build_import_froms(node)) 
                
            elif isinstance(node, ast.Assign) or isinstance(node, ast.AnnAssign) or isinstance(node, ast.AugAssign):
                self._datacalls.extend(self.context.build_datacall(node, parent))

            for child in ast.iter_child_nodes(node):
                _walk_search(child, node)

        self.context.update_path(path)
        self.context.update_modulepath(modulepath)
        _walk_search(get_ast(path), None)