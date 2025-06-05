from tools.CommandArgs import CommandArgs
from tools.Analysis import Analysis
             
if __name__ == "__main__": 
    args = CommandArgs()
    args.check()
    source_dir = args.source_dir()
    target_dir = args.target_dir()
    
    analysis = Analysis(source_dir, target_dir, 'dataflow')
    analysis.run()
    
     
    
    
    

    


