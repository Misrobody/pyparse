import csv, sys, os
from utils import *

class CsvExporter:
    def __init__(self, target_dir):
        self.target = target_dir
              
    def export_target(self, headers, data, filename): 
        if not os.path.isdir(self.target):
            os.mkdir(self.target)
        
        path = self.target + "/" + filename + ".csv"  
        with open(path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        
    def _export_operation_dict(self, ops_dict):
        headers = ["file", "operation"]
        uncompressed = []
        for ops in ops_dict.values():
            for op in ops:
                uncompressed.append(op.export())
        self.export_target(headers, uncompressed, "operation_definitions")
        
    def _export_call_table(self, calls):
        headers = ["callerfilename",
                "callermodule",
                "callerfunction",
                "calleefilename",
                "calleemodule",
                "calleefunction"]
        uncompressed = [call.export() for call in calls]
        self.export_target(headers, uncompressed, "calltable")
        
    def _export_not_found(self, calls):
        headers = ["callerfilename",
                "callermodule",
                "callerfunction",
                "calleefunction"]
        uncompressed = [call.export_not_found() for call in calls if call.is_unresolved()]
        uncompressed = list(set(uncompressed))
        self.export_target(headers, uncompressed, "notfound")
              
    def _export_common_blocks(self, blocks):
        headers = ["name",
                "files",
                "modules",
                "variables"]
        uncompressed = [block.export() for block in blocks]
        self.export_target(headers, uncompressed, "common-blocks")
              
    def _export_dataflow_cc(self, calls):
        headers = ["source-path",
                "source-module",
                "source-operation",
                "target-path",
                "target-module",
                "target-operation",
                "direction"]
        uncompressed = [call.export() for call in calls]
        self.export_target(headers, uncompressed, "dataflow-cc")
    
    def _export_dataflow_cb(self, calls, blocks):
        headers = ["common-block",
                "file",
                "module",
                "operation",
                "direction"]
        uncompressed = [block.export() for block in blocks]
        self.export_target(headers, uncompressed, "dataflow-cb")
              
    def export_calls(self, resolver):
        self._export_operation_dict(resolver.resolved_ops())      
        self._export_call_table(resolver.resolved_calls())      
        self._export_not_found(resolver.resolved_calls())
        
    def export_dataflow(self, resolver):
        calls = resolver.resolved_calls()
        blocks = resolver.resolved_common_blocks()
        
        self._export_operation_dict(resolver.resolved_ops())
        self._export_not_found(calls)
        self._export_common_blocks(blocks)
        self._export_dataflow_cc(calls)
        #self._export_dataflow_cb(calls, blocks)
        