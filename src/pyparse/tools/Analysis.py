from utils import *
from termcolor import colored
from tools.CallSearch import CallSearch
from tools.CsvExporter import CsvExporter
from tools.CallResolver import CallResolver

class Analysis:
    def __init__(self, source_dir, target_dir):
        self.source_dir = source_dir       
        
        self.ops_dict = {}
        self.calls = []
        self.imports = []
        self.exporter = CsvExporter(target_dir)
                             
    def run(self):
        searcher = CallSearch(self.source_dir)
        self.ops_dict, self.calls, self.imports = searcher.search()

        self.resolver = CallResolver(self.ops_dict,
                                     self.calls,
                                     self.imports) 
        self.calls = self.resolver.resolve_all()
        #dump_list(self.calls)
        
    def export(self):
        self.exporter.export_all(self.ops_dict, self.calls)  
        
    def print_stats(self):
        stats = self.resolver.stats()
        print(f"Total resolved: {stats['total_resolved']}/{stats['total']}")
        print(colored(f"Total unresolved: {stats['total_unresolved']}/{stats['total']}", "red"))
        print(f"In app callees: {stats['in-app']}")
        print(f"Out app callees: {stats['out-app']}")
        print(colored(f"\tModules: {stats['modules']}", "yellow"))
        print(colored(f"\tMethods: {stats['methods']}", "blue"))

        