#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import join as pj

from openalea.lpy import Lsystem
from walter import data_access


def test_main():
    lsystem_file = pj(data_access.get_data_dir(), 'WALTer.lpy')
    lsys = Lsystem(lsystem_file,{'params': {'nb_plt_utiles': 1,
                                  'dist_border_x':0,
                                  'dist_border_y': 0,
                                  'nbj': 55,
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

def test_infinitized_run():
    lsystem_file = pj(data_access.get_data_dir(), 'WALTer.lpy')
    lsys = Lsystem(lsystem_file,{'params': {'nb_plt_utiles': 1,
                                  'dist_border_x':0,
                                  'dist_border_y': 0,
                                  'nbj': 70,
                                  'infinity_CARIBU' : 1,
                                  'beginning_CARIBU': 290

         }})
    assert isinstance(lsys, Lsystem)
    
    lstring = lsys.iterate()
    assert len(lstring) > 10
    
    s=lsys.sceneInterpretation(lstring)
    assert len(s) > 2



