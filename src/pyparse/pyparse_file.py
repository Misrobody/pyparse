from params import *
from call_table import *
from utils import *
from operation_definitions import *
from termcolor import colored
            
if __name__ == "__main__":      
    arg_check_file()   
    source_file = get_source_file()
    print("\n[INFO] Source file: ", source_file)
     
    

    ops_dict, calls = depth_first_search(source_file)  

    dump_default_dict(ops_dict) 
    #dump_list(calls)
    print("---------------")
         
    resolve_callees(calls, ops_dict)
    dump_list(calls) 
    