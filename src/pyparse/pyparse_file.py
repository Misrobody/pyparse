from operation_definitions import *
from params import *
from call_table import *
from utils import *
            
if __name__ == "__main__":      
    arg_check_file()   
    source_file = get_source_file()
    print("\n[INFO] Source file: ", source_file)
     
    #print("\n[INFO] Ast")
    #print(ast_str(get_ast(source_file))) 
     
    ops = collect_operations(source_file)
    print("\n[INFO] Operation definitions")   
    #dump_list(ops)
    
    ops_dict = operation_dict(ops)
    print("\n[INFO] Operation definitions dict")   
    #dump_default_dict(ops_dict)
        
    calls = collect_calls(source_file)
    print("\n[INFO] Calls")
    #dump_list(calls)   
      
    print("\n[INFO] Resolve callees")
    resolve_callees(calls, ops_dict)
    dump_list(calls) 
    

