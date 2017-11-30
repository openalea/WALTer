"""
Questions: Do we need to separate Project and Simulation classes?

"""

import sys, os
from os.path import join as pj
from path import Path
import tempfile
import pandas as pd

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

class Project(object):
    """ TODO
    """

    def __init__(self, name=''):
        if not name:
            # TODO: Add the date time rather than temp string
            name = tempfile.mkdtemp(dir='.', prefix='simu_')
        dirname = Path(name)

        if not dirname.exists():
            dirname.mkdir()

        self.name = str(dirname.name)
        self.dirname = dirname.abspath()

        # remove global variables into class fields
        # self.set_dir()
        set_dir(self.dirname)

        copy_input() # move to self._copy_input()
        generate_output()
        which_output()

        self._outputs = {}

    def activate(self):
        set_dir(self.dirname)

    def deactivate(self):
        set_dir(OLD_DIR)

    def clean(self):
        pass

    def remove(self, force=False):
        self.deactivate()
        if force:
            self.dirname.rmtree()

    @property
    def which_outputs(self):
        if not self._outputs:
            df=pd.read_csv(self.dirname/'which_output_files.csv', sep='\t')
            outs = df.to_dict(orient='records')[0]
            self._outputs = outs

        return self._outputs


    @which_outputs.setter
    def which_outputs(self, outputs):
        self._outputs = outputs

        # Write the which_output_files
        df = pd.DataFrame.from_dict(data=[outputs], orient='columns')
        df.to_csv(path_or_buf=self.dirname/'which_output_files.csv', sep='\t', index=False)



    def run(self, **kwds):
        """ Run WALTer locally.

        Set parameter values as keyword arguments::

            run(nb_plt_utiles=1,
                dist_border_x=0,
                dist_border_y=0,
                nbj=30,
                beginning_CARIBU=290)
        """
        self.activate()

        data = walter_data()
        walter = str(data / 'WALTer.lpy')

        # TODO check if this file exists...
        lsys = Lsystem(walter, {'params': kwds})
        lstring = lsys.iterate()

        return lsys, lstring

    def csv_parameters(self, csv_filename):

        self.deactivate()

        df=pd.read_csv(csv_filename, sep='\t')
        param_list = df.to_dict(orient='records') # a list of dict

        self.activate()

        return param_list


class Simulation(object):
    """ Run one or several simulation """

    def __init__(self, project, csv_params=None):
        self.project = project
        self.parameters = []

    def run(self, **kwds):
        """ Run WALTer locally.

        Set parameter values as keyword arguments::

            run(nb_plt_utiles=1,
                dist_border_x=0,
                dist_border_y=0,
                nbj=30,
                beginning_CARIBU=290)
        """
        self.project.activate()

        data = walter_data()
        walter = str(data / 'WALTer.lpy')

        # TODO check if this file exists...
        lsys = Lsystem(walter, {'params': kwds})
        lstring = lsys.iterate()

        return lsys, lstring


    def run_all(self):
        """
        """
        for p in self.parameters:
            self.run(**p)


    def set_csv_parameters(self, csv_filename):
        """ Add a set of csv parameters (with tab separators).
        """
        df=pd.read_csv(csv_filename, sep='\t')
        param_list = df.to_dict(orient='records') # a list of dict
        self.parameters.extend(param_list)


    def save_parameters(self, csv_filename = 'sim_scheme.csv'):
        """ save the parameters into a csv file. """
        pass # TODO


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



