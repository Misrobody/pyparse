import csv, sys, os
from params import *
      
def export(headers, data, target_dir, filename): 
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)
    
    path = target_dir + "/" + filename + ".csv"  
    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
        
def export_target(headers, data, filename): 
    export(headers, data, get_target_dir(), filename)
        
'''
Export a given operation list as csv
'''
def export_operation_list(operations):
    headers = ["file", "operation"]
    uncompressed = [op.export() for op in operations]
    export_target(headers, uncompressed, "operation_definitions")
    
'''
Export a given operation dict as csv
'''
def export_operation_dict(ops_dict):
    headers = ["file", "operation"]
    uncompressed = []
    for ops in ops_dict.values():
        for op in ops:
            uncompressed.append(op.export())
    export_target(headers, uncompressed, "operation_definitions")
      

'''
Export a given call table as csv
'''
def export_call_table(calls):
    headers = ["callerfilename",
               "callermodule",
               "callerfunction",
               "calleefilename",
               "calleemodule",
               "calleefunction"]
    uncompressed = [call.export() for call in calls]
    export_target(headers, uncompressed, "calltable")
    
def export_not_found(calls):
    headers = ["callerfilename",
               "callermodule",
               "callerfunction",
               "calleefunction"]
    uncompressed = [call.export_not_found() for call in calls if call.is_resolved()]
    uncompressed = list(set(uncompressed))
    export_target(headers, uncompressed, "notfound")