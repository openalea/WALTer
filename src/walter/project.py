"""
Management of walter simulations and projects
"""

import os
import tempfile


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


def check_cwd():
    """ does the current dir looks like a walter project dir ?"""
    dir = cwd()
    return (dir / 'input').exists() and (dir / 'output').exists() and (dir / 'which_output_files.csv').exists()


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
            self.itable = OrderedDict(self.read_itable(self.dirname / itable))
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
            self._combi_params = pd.read_csv(self.dirname/'combi_params.csv', sep='\t')
        return self._combi_params

    @staticmethod
    def csv_parameters(path):
        params = []
        i = 0
        with open(path) as f:
            dialect = csv.Sniffer().sniff(f.read(4096))
            f.seek(0)
            reader = csv.reader(f, dialect)
            headers = reader.next()
            for list_val in reader:
                params.append({})
                #list_val = l.strip().split('\t')
                for ind in range(len(list_val)):
                    val = list_val[ind]
                    try :
                        params[i][headers[ind]] = int(val)
                    except :
                        try :
                            params[i][headers[ind]] = float(val)
                        except :
                            params[i][headers[ind]] = val
                i += 1
                
        return params


    @staticmethod
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

    @staticmethod
    def write_itable(itable, path):
        with open(path, "w") as out:
            json.dump(itable, out)

    def update_itable(self):
        path = str(self.dirname / 'index-table.json')
        self.write_itable(self.itable, path)

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
        df.to_csv(path, index=False, sep = '\t')

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
            self.update_itable()
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
        parameters = self.csv_parameters(csv_parameters)
        if which is not None:
            try:
                iter(which)
            except TypeError:
                which = [which]
            parameters = [p for i, p in enumerate(parameters) if i in which]
        already_known_id = self.itable.keys()
        sim_ids = self.generate_id(parameters)
        if not all([sid in already_known_id for sid in sim_ids]):
            self.update_itable()
        for sid, param in zip(sim_ids, parameters):
            lsys, lstring = self.run(sid, dry_run=dry_run, **param)

        return lsys, lstring

    def output_path(self, index=-1):
        """return the path to output directory of a simulation

        Parameters
        ----------
        index (int):
            the index of the simulation. -1 stands for the last simulation

        Returns
        -------
            a path.Path instance
        """
        sid = self.itable.keys()[index]
        return self.dirname / 'output' / sid
