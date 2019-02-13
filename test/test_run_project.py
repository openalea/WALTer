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
    s = lsys.sceneInterpretation(lstring)
    p.remove(force=True)
    assert len(lstring) > 10
    assert len(s) > 0


def test_run_parameters():
    reset_call_dir()
    p = project.Project()
    try:
        lsys, lstring = p.run_parameters('sim_scheme_fast_test.csv')
        s = lsys.sceneInterpretation(lstring)
        assert len(lstring) > 10
        assert len(s) > 0
        lsys, lstring = p.run_parameters('sim_scheme_fast_test2.csv')
        s = lsys.sceneInterpretation(lstring)
        assert len(lstring) > 10
        assert len(s) > 0
        assert len(p.combi_params) == 3
    except:
        raise
    finally:
        p.remove(force=True)


def test_which_parameters():
    reset_call_dir()
    p = project.Project()
    try:
        lsys, lstring = p.run_parameters('sim_scheme_fast_test2.csv', which=0)
        assert lstring
        assert len(p.combi_params) == 1
        lsys, lstring = p.run_parameters('sim_scheme_fast_test2.csv', which=[1,2])
        assert lstring
        assert len(p.combi_params) == 3
    except:
        raise
    finally:
        p.remove(force=True)


def test_modified_parameters():
    reset_call_dir()
    p = project.Project()
    try:
        param = p.csv_parameters('sim_scheme_fast_test.csv')[0]
        param.update(dict(nbj=40))
        lsys, lstring = p.run(**param)
        assert lstring
        assert p.combi_params.nbj[0] == 40
    except:
        raise
    finally:
        p.remove(force=True)

