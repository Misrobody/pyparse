from tools.Operation import Operation 
from tools.OperationCall import OperationCall
from tools.Context import Context
from utils import *

class CallContext(Context):
    def __init__(self, filepath):
        super().__init__(filepath)

    def resolve_caller_name(self, current_level):
        if self.func_level == current_level:
            self.update_func(None, 0)
        if self.func_node is None:
            return ""
        return self.resolve_operation_name()
        
    def resolve_operation_name(self):
        if is_method(self.func_node) or is_static_method(self.func_node):
            return f"{self.class_node.name}.{self.func_node.name}"
        return self.func_node.name   
        
    def build_call(self, call, call_level):
        caller = Operation(self.filepath, file_name(self.filepath), self.resolve_caller_name(call_level))
        callee = Operation("<unknown>", "<unknown>", self.resolve_callee_name(call))
        return OperationCall(caller, callee)
    
    def build_operation_definition(self):
        return Operation(self.filepath, file_name(self.filepath), self.resolve_operation_name())
    
    def build_class_definition(self):
        return Operation(self.filepath, file_name(self.filepath), self.class_node.name)