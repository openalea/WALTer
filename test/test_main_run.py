#!/usr/bin/python
# -*- coding: utf-8 -*-

from openalea.lpy import Lsystem
import sys
from walter import data_access
from os.path import join as pj


def test_main():
    lsystem_file = pj(data_access.get_data_dir(), 'WALTer.lpy')
    lsys = Lsystem(lsystem_file,{'params': {'nb_plt_utiles': 1,
                                  'dist_border_x':0,
                                  'dist_border_y': 0,
                                  'nbj': 30,
                                  'beginning_CARIBU': 290

         }})
    assert isinstance(lsys, Lsystem)

    # lsys.nbj = 10
    # lsys.derivationLength = lsys.nbj
    # lsys.animate()
    lstring = lsys.iterate()
    assert len(lstring) > 10
    # ipython --gui=qt4
    s=lsys.sceneInterpretation(lstring)
    assert len(s) > 2
    # Viewer.display(s)
