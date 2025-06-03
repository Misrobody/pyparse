from params import *
from call_table import *
from utils import *
from imports import *
from csv_export import *
from resolve import *
             
if __name__ == "__main__":      
    arg_check_dir()
    source_dir = get_source_dir()
    target_dir = get_target_dir()
    print("[INFO] Source directory: ", source_dir)

    ops_dict, calls, imports = go_over(source_dir)
    default_imports = sys.stdlib_module_names
    all_imports = list(set(default_imports) | set(imports))
    all_imports.remove("this")
         
    calls = resolve_all(calls, ops_dict, all_imports)   
    dump_list(calls)
    

    
    #export_all(ops_dict, calls)
    
     
    
    
    

    


