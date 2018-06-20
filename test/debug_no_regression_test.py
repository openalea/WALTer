# coding=utf-8
from walter import project
import pandas,os
from walter.data_access import get_data_dir
from pathlib2 import Path
import numpy.testing as np
import re

def compare (atol_PAR=100):
    reference_directory = get_data_dir() + "/ref_output/"
    reference_directory_windows = get_data_dir() + "/ref_output_windows/"
    list_file_ref = os.listdir(reference_directory)
    for i in list_file_ref:
        element = reference_directory+ i
        windows = reference_directory_windows + i
        reference = pandas.read_csv(element, sep='\t')  # Recover file and content
        ref_windows = pandas.read_csv(windows, sep='\t')  # Recover file and content
        for column in reference.columns:
            try:
                if re.match('.*PAR.*', column):
                    np.assert_allclose(ref_windows[column], reference[column], atol=atol_PAR)
                else:
                    np.assert_array_equal(ref_windows[column], reference[column])
            except:
                print(i +"/"+column)
