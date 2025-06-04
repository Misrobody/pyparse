from params import *
from tools.Analysis import *
             
if __name__ == "__main__":      
    arg_check_dir()
    source_dir = get_source_dir()
    target_dir = get_target_dir()
    print("[INFO] Source directory: ", source_dir)

    analysis = Analysis(source_dir, builtin=True, external=True)
    analysis.run()
    analysis.export()
    analysis.print_stats()
    
     
    
    
    

    


