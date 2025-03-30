#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Run WALTer simulation as a command
"""
from __future__ import print_function
from __future__ import division
from builtins import input
from builtins import str
from past.utils import old_div
import os
import shutil
import argparse
from subprocess import Popen
import pandas as pd
import time

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
            answer = input("Current directory doesn't look like a walter project dir, Continue ? [Y/N]")
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
                tmp = old_div(prj.dirname, 'tmp')
                if not tmp.exists():
                    tmp.mkdir()
                pids = []
                procs = {}
                active_procs = []
                for i, pdict in enumerate(param_list):
                    ############################################# temporary fix #############################################################################################
                    while len(active_procs) > 2: # As long as there are 3 active_procs, test if one ends : temporary fix to avoid running too many processes at the same time
                        active_procs = [proc for proc in active_procs if proc.poll() == None]
                        #time.sleep(300) # To avoid testing for finished processes too often, wait 5 minutes between loops
                    df = pd.DataFrame.from_dict(data=[pdict], orient='columns')
                    scheme_name = str(old_div(tmp, 'sim_scheme_%d.csv') % (i + 1))
                    df.to_csv(path_or_buf=scheme_name, sep='\t', index=False)
                    prj.activate()
                    pid = Popen(["walter", "-i", scheme_name])
                    pids.append(pid)
                    procs[scheme_name] = pid
                    active_procs.append(pid)
                ############################################# temporary fix #############################################################################################
                # Test caribuRunError re-launching : temporary fix until CaribuRunErrors are solved
                while len(procs) > 0: # While there are processes to test
                    for scheme in list(procs.keys()): #Not using iteritems because you cannot change the size of a dictionary while iterating on it
                        if procs[scheme].poll() != None: # If the proces is finished
                            procs.pop(scheme) # Remove this proc from procs
                            param_list_dict = prj.csv_parameters(scheme)
                            sim_id = prj.get_id(param_list_dict[0]) # Get the ID
                            if os.path.exists(prj.dirname+"/output/"+sim_id+"/error_caribu.txt"): # Check if the file error_caribu.txt has been generated
                                shutil.rmtree(prj.dirname+"/output/"+sim_id) # Supress the output directory
                                ex_rep = param_list_dict[0]["rep"] # Get the rep (random seed) used for the simulation
                                param_list_dict[0].update(rep = ex_rep +1) # Update the sim_scheme with a new seed to re-launch the simulation
                                df = pd.DataFrame.from_dict(data=param_list_dict, orient='columns')
                                df.to_csv(path_or_buf=scheme, sep='\t', index=False) # Create the csv file sim_scheme to launch the simulation
                                p = Popen(["walter", "-i", scheme]) # Launch the simulation
                                prj.itable[sim_id] = param_list_dict[0] # updating combi_param
                                prj.update_itable()
                                pids.append(p) # Add the new process to the list of processes for futher testing
                                procs[scheme] = p # Add the new process to the dict of processes
                    #time.sleep(120) # To avoid testing for finished processes too often, wait 2 minutes between loops
                tmp.rmtree()

