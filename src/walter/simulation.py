"""

"""

import sys, os
from os.path import join as pj
from path import Path

from openalea.lpy import Lsystem

from walter import data_access


def cwd():
    return Path(os.getcwd()).abspath()

def set_dir(d):
    global DIR
    _cwd = Path(d).abspath()
    DIR = _cwd

    change_dir()

DIR = cwd()
OLD_DIR = DIR

def change_dir(init=False):
    if not init:
        os.chdir(DIR)
    else:
        os.chdir(OLD_DIR)

def walter_data():
    d = data_access.get_data_dir()
    data_dir = Path(d).abspath()
    return data_dir

def copy_input():
    """ Copy the input dir from WALTer if it is not present.
    """
    data = walter_data()
    input_src = data/'input'
    input_dest = DIR / 'input'
    if not input_dest.exists():
        input_src.copytree(input_dest, symlinks=True)
        # TODO add log: copy input

    return True

def generate_output():
    """ Generate output dir if not present.
    """
    output = DIR / 'output'
    if not output.exists():
        output.mkdir()

def which_output():
    data = walter_data()
    csv = 'which_output_files.csv'
    if not (DIR /csv).exists():
        (data/csv).copy(DIR)




def run(**kwds):
    """ Run WALTer locally.

    Set parameter values as keyword arguments::

        run(nb_plt_utiles=1,
            dist_border_x=0,
            dist_border_y=0,
            nbj=30,
            beginning_CARIBU=290)
    """
    data = walter_data()
    walter = str(data / 'WALTer.lpy')

    # TODO check if this file exists...
    lsys = Lsystem(walter, {'params': kwds})
    lstring = lsys.iterate()

    return lsys, lstring


def main():
    pass



