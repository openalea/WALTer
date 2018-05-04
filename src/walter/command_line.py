#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Run WALTer simulation as a command
"""
import argparse
from subprocess import Popen
import pandas as pd

from walter import project

usage = """
WALTer generates a project directory and run simulations inside this directory.


1. To create a simulation project only, type:

       walter -p simu_walter


2. To run simulations inside the project, type:

       walter -p simu_walter -i sim_scheme.csv

    or, inside an existing project:

       cd simu_walter
       walter -i sim_scheme.csv
        or
       walter -i

3. To run project management only, without running te model (for debug)  

       walter -i sim_scheme.csv -p simu_walter --dry_run 

"""


def walter_parser():
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("-i", type=str, help="Select input simulation scheme", nargs='?', const='walter_default',
                        default='', action='store')
    parser.add_argument("-p", type=str, default='.',
                        help="Name of the project where simulations will be run")
    parser.add_argument("--dry_run", help="do only project management tasks", action="store_true")
    return parser


def main():

    parser = walter_parser()
    args = parser.parse_args()

    if args.p == '.':  # check '.' is walter-like (in case user has  forgotten -p)
        if not project.check_cwd():
            answer = raw_input("Current directory doesn't look like a walter project dir, Continue ? [Y/N]")
            if answer != 'Y':
                return

    prj = project.Project(args.p)

    # TODO: add a flag in the project to know if the project has been generated, modified or not.
    if prj.dirname.exists():
        print('Use Project %s located at %s' % (prj.name, prj.dirname))
    else:
        print('Project %s has been generated at %s' % (prj.name, prj.dirname))

    if args.i:  # -i has been set
        sim_scheme = args.i
        if sim_scheme == 'walter_default':  # walter command called with dry -i args
            prj.run(dry_run=args.dry_run)
        else:
            param_list = prj.csv_parameters(sim_scheme)
            if len(param_list) == 1:
                prj.run(dry_run=args.dry_run, **(param_list[0]))
            else:
                print('Multiple processes')
                print('generate ids')
                prj.run_parameters(sim_scheme, dry_run=True)
                print('run simulations')
                tmp = prj.dirname / 'tmp'
                if not tmp.exists():
                    tmp.mkdir()
                pids = []
                for i, pdict in enumerate(param_list):
                    df = pd.DataFrame.from_dict(data=[pdict], orient='columns')
                    scheme_name = str(tmp / 'sim_scheme_%d.csv' % (i + 1))
                    df.to_csv(path_or_buf=scheme_name, sep='\t', index=False)
                    prj.activate()
                    pid = Popen(["walter", "-i", scheme_name])
                    pids.append(pid)
                for pid in pids:
                    pid.wait()
                tmp.rmtree()

