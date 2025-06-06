from CommandArgs import *
from Analysis import *
             
if __name__ == "__main__": 
    args = CommandArgs()
    args.check()
    source_dir = args.source_dir()
    target_dir = args.target_dir()
    mode = args.get_mode()
    
    analysis = Analysis(source_dir, target_dir, mode)
    analysis.run()
    
     
    
    
    

    


