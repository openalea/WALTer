"""
Management of walter simulations and projects
"""

import os
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


def walter_data():
    d = data_access.get_data_dir()
    data_dir = Path(d).abspath()
    return data_dir


def cwd():
    return Path(os.getcwd()).abspath()


def read_parameters(path):
    df = pd.read_csv(path, sep='\t')
    param_list = df.to_dict(orient='records')  # a list of dict
    return param_list


def read_itable(path):

    def _byteify(input):
        if isinstance(input, dict):
            return {_byteify(key): _byteify(value)
                    for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [_byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    # The use of the byteify function kill encoding problems from json importation between unicode and strings
    with open(path) as itable:
        return _byteify(json.load(itable))


def write_itable(itable, path):
    with open(path, "w") as out:
        json.dump(itable, out)


class Project(object):
    """ TODO
    """

    def __init__(self, name=''):

        self.call_dir = Path(os.getcwd()).abspath()

        if not name:
            # TODO: Add the date time rather than temp string
            name = tempfile.mkdtemp(dir='.', prefix='simu_')

        dirname = Path(name)
        if not dirname.exists():
            dirname.mkdir()
        self.dirname = dirname.abspath()
        self.name = str(self.dirname.name)

        self.copy_input()
        self.generate_output()
        data = walter_data()
        if not (data / 'WALTer.lpy').exists():
            raise ImportError('could not locate walter.lpy source code')
        self.walter = str(data / 'WALTer.lpy')

        csv = 'which_output_files.csv'
        if not (self.dirname / csv).exists():
            (walter_data() / csv).copy(self.dirname)
        self._outputs = {}  # needed for first call to which_output

        itable = 'index-table.json'
        if (self.dirname / itable).exists():
            self.itable = OrderedDict(read_itable(itable))
        else:
            self.itable = OrderedDict()
        self._combi_params = {}

    def copy_input(self):
        """ Copy the input dir from WALTer if it is not present.
        """
        data = walter_data()
        input_src = data / 'input'
        input_dest = self.dirname / 'input'
        if not input_dest.exists():
            input_src.copytree(input_dest, symlinks=True)
            # TODO add log: copy input

        return True

    def generate_output(self):
        """ Generate output dir if not present.
        """
        output = self.dirname / 'output'
        if not output.exists():
            output.mkdir()

    def activate(self):
        """ Change directory to the project one. """
        os.chdir(self.dirname)

    def deactivate(self):
        """ Change dir to the user one. """
        os.chdir(self.call_dir)

    def clean(self):
        pass

    def remove(self, force=False):
        self.deactivate()
        if force:
            self.dirname.rmtree()

    @property
    def which_outputs(self):
        if not self._outputs:
            df = pd.read_csv(self.dirname/'which_output_files.csv', sep='\t')
            outs = df.to_dict(orient='records')[0]
            self._outputs = outs

        return self._outputs

    @which_outputs.setter
    def which_outputs(self, outputs):
        self._outputs.update(outputs)
        # Write the which_output_files
        df = pd.DataFrame.from_dict(data=[outputs], orient='columns')
        df.to_csv(path_or_buf=self.dirname/'which_output_files.csv', sep='\t', index=False)

    @property
    def combi_params(self):
        if (self.dirname/'combi_params.csv').exists():
            self._combi_params = pd.read_csv(self.dirname/'combi_params.csv')
        return self._combi_params

    def write_itable(self):
        path = str(self.dirname / 'index-table.json')
        write_itable(self.itable, path)

        # update combi_parameters.csv
        path = str(self.dirname / 'combi_params.csv')

        parameters = self.itable.values()
        allkeys = set().union(*parameters)

        def _missing(d):
            return len(allkeys - set(d.keys()))
        if any([_missing(p) for p in parameters]):
            self.activate()
            new = []
            for p in parameters:
                lsys = Lsystem(self.walter, {'params': p})
                newp = {k: lsys.context().locals().get(k, 'undef') for k in allkeys}
                new.append(newp)
            parameters = new

        combi = []
        for k, v in zip(self.itable, parameters):
            d = {'ID': k}
            d.update(v)
            combi.append(d)
        df = pd.DataFrame(combi)
        df.to_csv(path, index=False)

    def get_id(self, param):
        sim_id = None

        if len(param) == 0:
            sim_id = 'walter_defaults'

        for _id in self.itable:
            if param == self.itable[_id]:
                sim_id = _id
                break

        if sim_id is None:
            sim_id = 'id-' + str(uuid.uuid4())

        if sim_id not in self.itable:
            self.itable[sim_id] = param

        return sim_id

    def run(self, sim_id=None, dry_run=False, **kwds):
        """Run WALTer in project dir

        Parameters
        ----------
        sim_id:
            simulation identifier
        dry_run: (bool)
            prevent running the simulation (do only side effects).
        **kwds:
            walter parameters values (as named arguments)

        Examples
        --------
           p = Project()
           p.run(nb_plt_utiles=1,
                dist_border_x=0,
                dist_border_y=0,
                nbj=30,
                beginning_CARIBU=290)

        Returns
        -------
            the lsystem and lstring generated by the run
        """

        self.activate()
        already_known_id = self.itable.keys()
        if sim_id is None:
            sim_id = self.get_id(kwds)
        if sim_id not in already_known_id:
            self.write_itable()
        lsys, lstring = None, None
        if not dry_run:
            lsys = Lsystem(self.walter, {'params': kwds, 'ID': sim_id})
            lstring = lsys.iterate()

        return lsys, lstring

    def generate_id(self, parameter_list):
        return [self.get_id(p) for p in parameter_list]

    def run_parameters(self, csv_parameters, which=None, dry_run=False):
        """Run walter with input parameters specified in csv file

        Parameters
        ----------
        csv_parameters: (string)
            name csv file containing inputs
        which: (sequence or None)
            indices of lines (index 0 = line 1) of input csv to be run.
            If None (default), all lines are run.
        dry_run: (bool)
            prevent running the simulation (do only side effects).

        Returns
        -------
            the lsystem and the lstring of the last run
        """
        self.deactivate()
        lsys, lstring = None, None
        parameters = read_parameters(csv_parameters)
        if which is not None:
            parameters = [p for i, p in enumerate(parameters) if i in which]
        already_known_id = self.itable.keys()
        sim_ids = self.generate_id(parameters)
        if not all([sid in already_known_id for sid in sim_ids]):
            self.write_itable()
        for sid, param in zip(sim_ids, parameters):
            lsys, lstring = self.run(sid, dry_run=dry_run, **param)

        return lsys, lstring

    def generate_index_table(self, parameters):
        """ Generate a file named index-table.json.

        The file contains a dict with :
          - as key an ID ('id_'+str(uuid.uuid4()))
          - as value a dict of a set of parameters (parameters[i])

        If the file already exists, do not regenerate it (due to recursive call).
        Else generate it plus another file named from_json_to_humanbeing.txt

        :param parameters: list of dict
        """

        self.activate()

        itable = 'index-table.json'

        # allkey = set().union(*alldict)
        if os.path.isfile(itable):
            # The use of the byteify function kill encoding problems from json importation between unicode and strings
            ID_params = OrderedDict(byteify(json.load(open(itable))))
        else:
            # Generate the dict ID_params
            ID_params = OrderedDict()

        for param in parameters:
            already_known_ID = False
            for idp in ID_params:
                # If the combination of parameters has already been encountered previously and stored in the json file
                if sorted(ID_params[idp].values()) == sorted(param.values()):
                    already_known_ID = True
            # If the ID of the simulation is already known
            if already_known_ID:
                ID = idp
            else:
                # compute a new ID
                ID = 'id-'+str(uuid.uuid4())
                ID_params[ID] = param

        itable_file = open(itable, "w")
        json.dump(ID_params, itable_file)

        # generate combi_parameters.csv
        combi = []
        for k, v in ID_params.iteritems():
            d = {'ID': k}
            d.update(v)
            combi.append(d)


        combi_param = pd.DataFrame(combi)
        combi_param.to_csv(path_or_buf=self.dirname /'combi_params.csv', index=False)


        # We can now generate from_json_to_humanbeing.txt
        # json_2_human = open("from_json_to_humanbeing.txt", "a")
        # for ID in ID_params:
        #     params = ID_params[ID]
        #     for key, val in params.iteritems():
        #         json_2_human.write("%s \t %s \t %s \n" % (ID, key, val))
        #     json_2_human.write("\n")
        # json_2_human.close()

        return ID_params



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




