import sys
from walter import simulation

simulation.set_dir('simu1')
simulation.copy_input()
simulation.which_output()
simulation.generate_output()

try:
    lsys, lstring= simulation.run(nb_plt_utiles=1,
                                  dist_border_x=0,
                                  dist_border_y=0,
                                  nbj=30,
                                  beginning_CARIBU=290)
except Exception as e:
    errors = sys.exc_info()
    for e in errors:
        print e

simulation.change_dir(init=True)