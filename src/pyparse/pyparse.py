from operation_definitions import *
from params import *
from call_table import *
from utils import *
            
if __name__ == "__main__":      
    arg_check_dir()
    source_dir = get_source_dir()
    target_dir = get_target_dir()
    print("[INFO] Source directory: ", source_dir)

    #print("\n[INFO] Ast")
    #print(ast_str(get_ast(source_file))) 
     
    ops = operation_list(source_dir)
    print("[INFO] Operation definitions")   
    #dump_list(ops)
    
    ops_dict = operation_dict(ops)
    print("[INFO] Operation definitions dict")   
    #dump_default_dict(ops_dict)
        
    calls = call_table(source_dir)
    print("[INFO] Calls")
    #dump_list(calls)   
    
    print("[INFO] Resolve callees")
    resolved = resolve_callees(calls, ops_dict)
    #dump_list(calls)
    print("[INFO] Resolved " + str(resolved) + " out of " + str(len(calls)) + " callees")
    
    print("[INFO] Export operation_definitions.csv")
    export_operation_list(ops)
    print("[INFO] Exported operation_definitions.csv")
    
    print("[INFO] Export operation_definitions.csv")
    export_call_table(calls)
    print("[INFO] Exported operation_definitions.csv")  
    
    print("[INFO] Export notfound.csv")
    export_not_found(calls)
    print("[INFO] Exported notfound.csv")  
    
    

    


