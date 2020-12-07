from walter import project
import walter.geometry_analysis_caribu as gac
import os



def test1(dirname, name, nbj=30):
    os.chdir(dirname)
    p = project.Project(name)
    lsys, lstring = p.run(nb_plt_utiles=2,
                          dist_border_x=0,
                          dist_border_y=0,
                          nbj=nbj,
                          beginning_CARIBU=290)
    lscene = lsys.sceneInterpretation(lstring)
    #p.remove(force=True)
    return p, lsys, lstring, lscene


def test_analyse(dirname, name, nbj=30):
    os.chdir(dirname)
    p, lsys, lstring, lscene = test1(dirname, name, nbj)
    crop_scheme = lsys.context().locals()['crop_scheme']
    plant_map = lsys.context().locals()['plant_map']
    df = gac.analyse(lscene, lstring, crop_scheme, plant_map)
    neighbours = gac.neighbours(plant_map, df['Ri'])
    df['Ri_neighbours'] = ['[' + ','.join(neighbours[i]) + ']' for i in neighbours]
    return df











