from walter import project
from path import Path
import os

#Assert the simulation works even with a high number of leaves on the main stem

def test_bug_Ln_final():
    p = project.Project()
    param = p.csv_parameters('sim_scheme_test.csv')[0]
    param.update(dict(Ln_final_Maxwell=20.3, nbj=120))
    lsys, lstring = p.run(**param)
    assert lstring
    p.remove(force=True)

