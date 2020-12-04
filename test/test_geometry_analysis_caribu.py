from walter import project
import walter.geometry_analysis_caribu as gac




def test1(nbj=30):
    p = project.Project()
    lsys, lstring = p.run(nb_plt_utiles=2,
                          dist_border_x=0,
                          dist_border_y=0,
                          nbj=nbj,
                          beginning_CARIBU=290)
    lscene = lsys.sceneInterpretation(lstring)
    p.remove(force=True)
    return p, lsys, lstring, lscene


def test_analyse(nbj=30):
    p, lsys, lstring, lscene = test1(nbj)
    crop_scheme = lsys.context().locals()['crop_scheme']
    plant_map = lsys.context().locals()['plant_map']
    df = gac.analyse(lscene, lstring, crop_scheme, plant_map)
    return df










