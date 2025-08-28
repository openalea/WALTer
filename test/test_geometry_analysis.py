from walter import project
from walter.light import scene_pattern
from openalea.plantgl.all import Scene

def test1():
    p = project.Project(name='zero_light')

    params = p.csv_parameters('sim_scheme_fast_test.csv')[0]
    params.update(dict(nbj=100 ))
    #new_output = p.which_outputs
    
    #p.which_outputs = dict(Lstring= 1, Lscene=1)
    
    #assert( len(p.which_outputs) > 2)
    lsys, lstring = p.run(**params)
    lscene = lsys.sceneInterpretation(lstring)
    p.deactivate()
    return p, lstring, lscene

def save_all(lstring, lscene, prefix='test1'):
    s_save = Scene(lscene)
    s_save.save('%s.bgeom'%prefix)

    with open("%s_lstring.txt" % prefix, "w") as out_lstring:
        out_lstring.write("%s" % lstring)
    
def read_all(prefix='test1'):
    from openalea.lpy import Lstring
    lscene = Scene('%s.bgeom'%prefix)
    with open("%s_lstring.txt" % prefix, "r") as in_lstring:
        lstring = in_lstring.read()

    lstring = Lstring(lstring)
    return lscene, lstring
