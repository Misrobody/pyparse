from tools.Operation import *
from tools.DataCall import *
from tools.Context import *
from tools.CommonBlock import *
from utils import *
import ast

class DataflowContext(Context):
    def __init__(self, filepath):
        super().__init__(filepath)
        
        self.common_block = None
                   
    def resolve_datacall_targets(self, datacall):
        if isinstance(datacall, ast.Assign):
            res = []
            for i in datacall.targets:
                res.append(i)
            return res    
        return [datacall.target]
    
    def resolve_direction(self, name):
        if isinstance(name.ctx, ast.Load):
            return "READ"
        elif isinstance(name.ctx, ast.Store) or isinstance(name.ctx, ast.Del):
            return "WRITE"
        return "NONE"
    
    def build_datacall(self, datacall, datacall_level):
        res = []
        callee = self.build_datacall_callee(datacall)
        
        targets = self.resolve_datacall_targets(datacall)
        for name in targets:
            caller = Operation(self.filepath, file_name(self.filepath), self.resolve_callee_name(name))            
            res.append(DataCall(caller, callee, self.resolve_direction(name)))
                   
            if self.common_block != None:
                # if caller is a global var (child of module)
                if datacall_level == 1:
                    self.common_block.addCaller(caller)
                
                #if caller is a class attribute
                if datacall_level == (self.class_level + 1) or (self.class_node != None and self.class_node.name in caller.name):
                    self.common_block.addCaller(caller)       
        return res
    
    def build_datacall_callee(self, datacall):
        if isinstance(datacall.value, ast.Constant):
            return Operation(self.filepath, file_name(self.filepath), datacall.value.value)
        return Operation("<unknown>", "<unknown>", self.resolve_callee_name(datacall.value))

    def build_common_block(self, node):
        if isinstance(node, ast.ClassDef):
            name = node.name 
        else:
            name = self.filepath
        self.common_block = CommonBlock(name)
        return self.common_block