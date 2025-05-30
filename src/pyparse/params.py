import sys, os

usage_dir = "usage: python main.py <inputdir> <outputdir>"
usage_file = "usage: python main.py <filename>"

'''
Check command line params for dir input
'''
def arg_check_dir():
    if len(sys.argv) < 3:
        print(usage_dir)
        sys.exit(1)
    elif not os.path.isdir(sys.argv[1]):
        print(usage_dir)
        print("<inputdir> is not a directory")
        sys.exit(1)

'''
Format dirname
'''
def format_dirname(param_num):
    path = sys.argv[param_num]
    if not path.endswith("/"):
        path += "/"
    return os.path.dirname(path)

'''
Extract the source dir from the params
'''
def get_source_dir():
    return format_dirname(1)

'''
Extract the target dir from the params
'''
def get_target_dir():
    return format_dirname(2)

##############################################

'''
Check command line params for file input
'''
def arg_check_file():
    if len(sys.argv) < 2:
        print(usage_file)
        sys.exit(1)
    elif not os.path.isfile(sys.argv[1]):
        print(usage_dir)
        print("<dirname> is not a file")
        sys.exit(1)

'''
Extract the source file from the params.
'''
def get_source_file():
    return sys.argv[1]
