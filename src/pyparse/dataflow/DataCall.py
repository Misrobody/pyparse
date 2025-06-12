from State import *

class DataCall:
    def __init__(self, caller, callee, direction):
        self.caller = caller
        self.callee = callee
        self.direction = direction

    def __repr__(self):
        return f"{repr(self.caller)} --> {repr(self.callee)} : {self.direction}"
    
    def export(self):
        return (self.caller.path, 
                self.caller.module,
                self.caller.name,
                self.callee.path,
                self.callee.module,
                self.callee.name,
                self.direction)
        
    def export_not_found(self):
        return (self.caller.path, self.caller.module, self.caller.name, self.callee.name)
    
    def update_callee_origin(self, file, module, state):
        if self.callee.state != State.FOUND:
            self.callee.path = file
            self.callee.module = module
            self.callee.state = state