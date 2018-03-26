""" Test the behavior of Lpy regarding the indexation bug when cut module is used"""

from os.path import join as pj
from openalea.lpy import Lsystem
from walter import data_access

fake_rule = """
Fake:
  produce Fake"""

def test_cut_bug():
    lsystem_file = pj(data_access.get_data_dir(), 'check_cut_module.lpy')
    lsys = Lsystem(lsystem_file)
    lstring = lsys.iterate()
    # cut branches
    fake_lsys = Lsystem()
    fake_lsys.addRule(fake_rule)
    fake_lsys.axiom = lstring
    new_lstring = fake_lsys.iterate()
    lscene = lsys.sceneInterpretation(lstring)
    for sid in lscene.todict():
        assert sid in range(len(lstring))
        # suucceed if correction is needed
        # assert new_lstring[sid].name == 'Internode'
        #  succeed if lpy bug has been fixed
        assert lstring[sid].name == 'Internode'