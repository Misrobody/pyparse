class Link:
    def __init__(self, caller, callee):
        self.caller = caller
        self.callee = callee
    
    def __init__(self, caller):
        self.caller = caller
        self.callee = None
        
    def __repr__(self):
        repr = self.caller.__repr__()
        repr += " --> "
        if self.callee is not None:
            repr += self.callee.__repr__()
        return repr
    
    def export(self):
        if self.callee == None:
            return (self.caller.module,
                    "<no module>",
                    self.caller.name, 
                    "<unknown>", 
                    "<unknown>", 
                    "<unknown>")
        return (self.caller.module, 
                "<no module>",
                self.caller.name,
                self.callee.module,
                "<no module>",
                self.callee.name)
        
    def export_not_found(self):
        return self.caller.module + ":" + self.caller.name + " --> " + self.caller.name
        