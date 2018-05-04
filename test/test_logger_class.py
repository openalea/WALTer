import walter.output_manager as out
from walter import project

def test_write():

    dirname = "out"
    p = project.Project(name=dirname)
    outs = p.which_outputs
    p.which_outputs = outs

    a = out.Logger() #Init # directory
    print(" Here are the files to create : ")
    for var in a.loggers:
        print (var)
    log_dirname = "output"
    a.write(log_dirname)# directory


