import sys, os

class CommandArgs():
    def __init__(self):
        self.USAGE = "usage: python main.py <inputdir> <outputdir> <mode>\nMode is either 'dataflow', 'call' or 'both'"

    def check(self):
        if len(sys.argv) < 4:
            print(self.USAGE)
            sys.exit(1)
        elif not os.path.isdir(sys.argv[1]):
            print(self.USAGE)
            print("<inputdir> is not a directory")
            sys.exit(1)
        elif sys.argv[3] != "call" and sys.argv[3] != "dataflow" and sys.argv[3] != "both":
            print(self.USAGE)
            sys.exit(1)
        
    def _format_dirname(self, param_num):
        path = sys.argv[param_num]
        if not path.endswith("/"):
            path += "/"
        return os.path.dirname(path)

    def source_dir(self):
        return self._format_dirname(1)

    def target_dir(self):
        return self._format_dirname(2)
    
    def get_mode(self):
        return sys.argv[3]
