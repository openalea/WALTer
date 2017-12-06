#!/usr/bin/python
# -*- coding: utf-8 -*-

from walter import project


def test_main():
    p = project.Project(name='simu_test1')
    lsys, lstring = p.run(nb_plt_utiles=1,
                          dist_border_x=0,
                          dist_border_y=0,
                          nbj=30,
                          beginning_CARIBU=290)
	
    assert len(lstring) > 10
    s=lsys.sceneInterpretation(lstring)
    assert len(s) > 2

    p.deactivate()
    p.remove(force=True)


def test_infinitized_run():
    p = project.Project(name='simu_test1')

    lsys, lstring = p.run(nb_plt_utiles=1,
                          dist_border_x=0,
                          dist_border_y=0,
                          nbj=53,
                          infinity_CARIBU=1,
                          beginning_CARIBU=290)

    p.deactivate()
    p.remove(force=True)




