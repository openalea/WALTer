"""
Questions: Do we need to separate Project and Simulation classes?

"""

import sys, os
from os.path import join as pj
import tempfile
import argparse
from subprocess import Popen

from path import Path
import pandas as pd

# ID management
import json
import uuid
from collections import OrderedDict

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

        self.dirname = dirname.abspath()
        self.name = str(self.dirname.name)

        # remove global variables into class fields
        # self.set_dir()
        set_dir(self.dirname)

        copy_input() # move to self._copy_input()
        generate_output()
        which_output()

        self._outputs = {}

    def activate(self):
        """ Change directory to the project one. """
        set_dir(self.dirname)

    def deactivate(self):
        """ Change dir to the user one. """
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


    def generate_index_table(self, parameters):
        """ Generate a file named index-table.json.

        The file contains a dict with :
          - as key an ID ('id_'+str(uuid.uuid4()))
          - as value a dict of a set of parameters (parameters[i])

        If the file already exists, do not regenerate it (due to recursive call).
        Else generate it plus another file named from_json_to_humanbeing.txt

        """

        self.activate()

        itable = 'index-table.json'

        if os.path.isfile(itable):
            return True

        # Generate the dict ID_params
        ID_params = OrderedDict()

        for param in parameters:
            # compute a new ID
            ID = 'id_'+str(uuid.uuid4())
            ID_params[ID] = param

        itable_file = open(itable, "w")
        json.dump(ID_params, itable_file)

        # generate combi_parameters.csv
        combi = []
        for k,v in ID_params.iteritems():
            d = {'ID': k}
            d.update(v)
            combi.append(d)
        combi_param = pd.DataFrame(combi)
        combi_param.to_csv(path_or_buf=self.dirname / 'combi_params.csv', sep='\t', index=False)


        # We can now generate from_json_to_humanbeing.txt
        # json_2_human = open("from_json_to_humanbeing.txt", "a")
        # for ID in ID_params:
        #     params = ID_params[ID]
        #     for key, val in params.iteritems():
        #         json_2_human.write("%s \t %s \t %s \n" % (ID, key, val))
        #     json_2_human.write("\n")
        # json_2_human.close()

        return ID_params

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


    def run_all(self, i=-1):
        """
        """
        if i == -1:
            for p in self.parameters:
                self.run(**p)
        else:
            p = self.parameters[i]
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
    """
    """

    input_folder = Path(os.getcwd()).abspath()

    usage = """
WALTer generates a project directory and run simulations inside this directory.


1. To create a full simulation project, run:

       walter -p simu_walter


2. To run simulations inside the project, type:

       cd simu_walter
       walter -i sim_scheme.csv
       
3. To run simulations and delete it after, type: 

       walter -i sim_scheme.csv -p [name_test] --test_only #[IN-WORK] 

"""

    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("-i", type=str,
                        help="Select input simulation scheme")
    parser.add_argument("-p", type=str,
                        help="Name of the project where simulations will be run")
    parser.add_argument("-t_o", "--test_only", help="Delete the project after simulation", action="store_true")

    args = parser.parse_args()

    _cwd = cwd()
    project_name = str(_cwd.name)

    project = '.'

    if args.i:
        sim_scheme = args.i
        print (sim_scheme)
    if args.p:
        project = args.p
        print(project)
    if args.test_only:
        print ("test_only")



    prj = Project(project)

    # TODO: add a flag in the project to know if the project has been generated, modified or not.
    if Path(project).exists():
        print('Use Project %s located at %s'%(prj.name, prj.dirname))
    else:
        print('Project %s has been generated at %s'%(prj.name, prj.dirname))


    param_list = prj.csv_parameters(sim_scheme)

    # Management of IDs
    # Generate a file index-table.json and an from_json_to_humanbeing.txt file

    status = prj.generate_index_table(param_list)

    done = False

    if len(param_list) == 1:
        prj.run(**(param_list[0]))
        done = True
    else:

        print 'Multiple processes'
        tmp = prj.dirname/'tmp'
        if not tmp.exists():
            tmp.mkdir()

        pids = []
        for i, pdict in enumerate(param_list):
            df = pd.DataFrame.from_dict(data=[pdict], orient='columns')
            scheme_name = str(tmp/'sim_scheme_%d.csv'%(i+1))
            df.to_csv(path_or_buf=scheme_name, sep='\t', index=False)
            pid = Popen(["walter", "-i", scheme_name])
            #, env={"PATH": "/Users/pradal/miniconda2/envs/adel2/bin"})
            #os.system("walter -i %s"%scheme_name)
            pids.append(pid)
        for pid in pids : 
            pid.wait() 
        
        done = True

    if args.test_only and done:
       prj.dirname.rmtree()




