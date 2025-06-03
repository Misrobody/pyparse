from params import *
from call_table import *
from utils import *
from imports import *
from csv_export import *
             
if __name__ == "__main__":      
    arg_check_dir()
    source_dir = get_source_dir()
    target_dir = get_target_dir()
    print("[INFO] Source directory: ", source_dir)

    ops_dict, calls = go_over(source_dir)
    #dump_default_dict(ops_dict)
    
    print("[INFO] Resolve callees from internal operation definitions")
    nb_resolved_int = resolve_callees(calls, ops_dict)
    #dump_list(calls)
    
    print("[INFO] Resolved " + str(nb_resolved_int) + " out of " + str(len(calls)) + " callees")
    print("[INFO] Still " + str(len(calls) - nb_resolved_int) + " out of " + str(len(calls)) + " unresolved")
    
    export_operation_dict(ops_dict)
    print("[INFO] Exported operation_definitions.csv")
    
    export_call_table(calls)
    print("[INFO] Exported operation_definitions.csv")  
    
    export_not_found(calls)
    print("[INFO] Exported notfound.csv") 
    
     
    
    
    

    


