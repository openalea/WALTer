from walter import project
from path import Path
import os

call_dir = Path(os.getcwd()).abspath()


# ensure tests start in call dir for finding parameters
def reset_call_dir():
    os.chdir(call_dir)


def test_direct_run():
    p = project.Project()
    lsys, lstring = p.run(nb_plt_utiles=1,
                          dist_border_x=0,
                          dist_border_y=0,
                          nbj=30,
                          beginning_CARIBU=290)

    assert len(lstring) > 10
    s = lsys.sceneInterpretation(lstring)
    assert len(s) > 2
    p.remove(force=True)


def test_run_parameters():
    reset_call_dir()
    p = project.Project()
    lsys, lstring = p.run_parameters('sim_scheme_fast_test.csv')
    assert len(lstring) > 10
    s = lsys.sceneInterpretation(lstring)
    assert len(s) > 2
    lsys, lstring = p.run_parameters('sim_scheme_fast_test2.csv')
    assert len(lstring) > 10
    s = lsys.sceneInterpretation(lstring)
    assert len(s) > 2
    assert len(p.combi_params) == 3

    p.remove(force=True)


def test_which_parameters():
    reset_call_dir()
    p = project.Project()
    lsys, lstring = p.run_parameters('sim_scheme_fast_test2.csv', which=0)
    assert lstring
    assert len(p.combi_params) == 1
    lsys, lstring = p.run_parameters('sim_scheme_fast_test2.csv', which=[1,2])
    assert lstring
    assert len(p.combi_params) == 3
    p.remove(force=True)


def test_modified_parameters():
    reset_call_dir()
    p = project.Project()
    param = p.csv_parameters('sim_scheme_fast_test.csv')[0]
    param.update(dict(nbj=40))
    lsys, lstring = p.run(**param)
    assert lstring
    assert p.combi_params.nbj[0] == 40
    p.remove(force=True)

