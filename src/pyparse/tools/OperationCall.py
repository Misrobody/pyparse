class OperationCall:
    def __init__(self, caller, callee):
        self.caller = caller
        self.callee = callee

    def __repr__(self):
        return f"{repr(self.caller)} --> {repr(self.callee)}"
    
    def export(self):
        return (self.caller.path, 
                self.caller.module,
                self.caller.name,
                self.callee.path,
                self.callee.module,
                self.callee.name)
        
    def export_not_found(self):
        return (self.caller.module, self.caller.name, self.caller.name, self.caller.name)