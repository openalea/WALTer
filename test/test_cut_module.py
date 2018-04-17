""" Test the behavior of Lpy regarding the indexation bug when cut module is used"""

from os.path import join as pj
from openalea.lpy import Lsystem
from walter import data_access


def force_cut(lstring):
    fake_rule = """
    Fake:
      produce Fake"""
    fake_lsys = Lsystem()
    fake_lsys.addRule(fake_rule)
    fake_lsys.axiom = lstring
    return fake_lsys.iterate()


def test_cut_bug():
    lsystem_file = pj(data_access.get_data_dir(), 'check_cut_module.lpy')
    lsys = Lsystem(lsystem_file)
    lstring = lsys.iterate()
    # cut branches
    new_lstring = force_cut(lstring)
    lscene = lsys.sceneInterpretation(lstring)
    for sid in lscene.todict():
        assert sid in range(len(lstring))
        # suucceed if correction is needed (old lpy version)
        # assert new_lstring[sid].name == 'Internode'
        #  succeed on more recent lpy version
        assert lstring[sid].name == 'Internode'
        # if correction is needed force_cut has to be applied in EndEach on lstring to get matching ids with lscene
