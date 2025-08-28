# coding=utf-8
from __future__ import print_function
from __future__ import division
from builtins import str
from past.utils import old_div
from walter import project
import os,shutil
from walter.data_access import get_data_dir
from path import Path

def change_reference():

    p = project.Project(name='same') # Create the simulation directory
    directory = project.walter_data()
    params = p.csv_parameters(str(old_div(directory,'sim_scheme_ref.csv')))[0] # recovery of parameters
    p.run(**params)
    reference_directory = get_data_dir() + '/ref_output'  # Reference folder
    if os.path.isdir(reference_directory):
        shutil.rmtree(reference_directory)
    result_directory = str(p.output_path()) + '/'
    list_of_result = os.listdir(result_directory)
    os.mkdir(Path(old_div(project.walter_data(),'ref_output')))
    for i in list_of_result:
        shutil.move(result_directory+i, reference_directory+'/'+i)
        print(result_directory+i, "has being moved into reference directory ")

    p.remove(force=True)