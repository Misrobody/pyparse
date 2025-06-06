from utils import *
from tools.CallSearch import *
from tools.CsvExporter import *
from tools.CallResolver import *
from tools.Stats import *
from tools.DataflowSearch import *
from tools.DataflowResolver import *

# Mode is either 'call' or 'dataflow'
class Analysis:
    def __init__(self, source_dir, target_dir, mode):
        self.source_dir = source_dir  
        self.mode = mode     
 
        self.stats = Stats()
        self.exporter = CsvExporter(target_dir)
                             
    def run(self):
        if self.mode == "call":
            self.run_call_analysis()
        elif self.mode == "dataflow":
            self.run_dataflow_analysis()
        else:
            raise ValueError("No such mode for analysis: " + self.mode)
                       
    def run_dataflow_analysis(self):
       searcher = DataflowSearch(self.source_dir)
       searcher.search()
       #dump_list(searcher.datacalls())
       resolver = DataflowResolver(searcher)
       resolver.resolve_all()

       dump_list(resolver.resolved_calls())
       #dump_default_dict(resolver.resolved_ops())
              
    def run_call_analysis(self):
        searcher = CallSearch(self.source_dir)
        searcher.search()
        resolver = CallResolver(searcher) 
        resolver.resolve_all()
        self.exporter.export_calls(resolver)
        self.stats.print_call_stats(resolver)
        