from utils import *
from CsvExporter import *
from Stats import *

from generic.Search import *

from call.CallResolver import *
from dataflow.DataflowResolver import *

class Analysis:
    def __init__(self, source_dir, target_dir, mode):
        self.source_dir = source_dir  
        self.mode = mode     

        self.exporter = CsvExporter(target_dir)
        self.search = Search(self.source_dir)
                             
    def run(self):
        self.search.search()
 
        if self.mode == "call":
            self.call_analysis()
        elif self.mode == "dataflow":
            self.dataflow_analysis()
        elif self.mode == "both":
            self.call_analysis()
            self.dataflow_analysis()
                                 
    def call_analysis(self):
        resolver = CallResolver(self.search)
        resolver.resolve_all()
        stats = Stats()
        stats.count_stats(resolver.resolved_calls())          
        stats.print_stats("Call")
        self.exporter.export_calls(resolver)
    
    def dataflow_analysis(self):
        resolver = DataflowResolver(self.search)
        resolver.resolve_all()
        stats = Stats()
        stats.count_stats(resolver.resolved_calls())          
        stats.print_stats("Dataflow")
        self.exporter.export_dataflow(resolver)
        