from termcolor import colored
from State import *

class Stats:
    def __init__(self):
        self.stats = {}
        self.stats["not_found"] = 0
        self.stats["import"] = 0
        self.stats["method"] = 0
        self.stats["call"] = 0
     
    def count_stats(self, calls):
        for call in calls:
            if call.callee.state == State.UNKNOWN:
                self.stats["not_found"] += 1
            elif call.callee.state == State.IMPORTED:
                self.stats["import"] += 1
            elif call.callee.state == State.METHOD:
                self.stats["method"] += 1
            else:
                self.stats["call"] += 1
                
        self.stats["total"] = len(calls)
        self.stats["found"] = self.stats["call"] + self.stats["import"] + self.stats["method"]
        self.stats["out-app"] = self.stats["import"] + self.stats["method"]
        
    def _rate(self, key):
            return f"{(self.stats[key] / self.stats['total'] * 100):.2f}%" 
        
    def _stat(self, key):
        formatted_key = key.replace("_", " ").title() + ":"
        return f"{formatted_key:<20}{self.stats[key]:>10} ({self._rate(key)})"
      
    def print_stats(self, name):     
        print("=" * 40)
        print(f"{name} Statistics Overview")
        print("=" * 40)
        
        print(self._stat("total"))
        
        print("")
        print(self._stat("found"))
        print(self._stat("not_found"))
        
        print("\nFound Calls Breakdown:")
        print(self._stat("call"))
        print(self._stat("import"))
        print(self._stat("method"))
        
        print("=" * 40)