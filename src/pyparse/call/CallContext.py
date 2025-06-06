from utils import *
from generic.Operation import Operation 
from generic.Context import Context
from call.OperationCall import OperationCall

class CallContext(Context):
    def __init__(self, filepath):
        super().__init__(filepath)

    def resolve_caller_name(self, current_level):
        if self.func_level == current_level:
            self.update_func(None, 0)
        if self.func_node is None:
            return ""
        return self.resolve_operation_name()
                
    def build_call(self, call, call_level):
        caller = Operation(self.filepath, file_name(self.filepath), self.resolve_caller_name(call_level))
        callee = Operation("<unknown>", "<unknown>", self.resolve_callee_name(call))
        return OperationCall(caller, callee)