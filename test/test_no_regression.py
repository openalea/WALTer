# coding=utf-8
from walter import project
import pandas,os
import glob
from walter.data_access import get_data_dir
from pathlib2 import Path
import numpy.testing as np
import re

_rtol_PAR = 0.02 # windows and linux version of walter lead up to 2 percent PAR output difference


def _compare_list_of_files(p):
    result_directory = str(p.output_path()) + os.sep
    reference_directory = os.path.join(get_data_dir(), "ref_output", '')  # Reference folder
    list_of_file_ref = map(os.path.basename, glob.glob(reference_directory + '*.csv'))  # Listing of the different reference files
    list_of_result = map(os.path.basename, glob.glob(result_directory + '*.csv'))
    np.assert_array_equal(list_of_file_ref, list_of_result) # Check that the 2 lists are equal


def _compare_file_content(p, rtol=_rtol_PAR):
    result_directory = str(p.output_path()) + os.sep
    reference_directory = os.path.join(get_data_dir(), "ref_output", '')  # Reference folder
    list_of_file_ref = map(os.path.basename, glob.glob(reference_directory + '*.csv'))  # Listing of the different reference files
    for i in list_of_file_ref:
        element = reference_directory + i  # Recover the absolut path
        reference = pandas.read_csv(element, sep='\t')  # Recover file and content
        my_file = Path(result_directory + i)
        if my_file.is_file():
            dfout = pandas.read_csv(my_file, sep='\t')
            print(' \n The tested file is : ' + i + '\n')
            # pandas.testing.assert_frame_equal(reference, dfout)
            for column in reference.columns:
                # print column
                if re.match('.*PAR.*', column):
                    np.assert_allclose(dfout[column], reference[column], rtol=rtol)
                else:
                    pandas.testing.assert_series_equal(dfout[column], reference[column])
        else:
            print(' \n The ' + my_file + ' file is non-existent ')


def test_same_result(debug=False):
    #assert : verify if the same wheat field have the same results for the same chosen parameters.

    p = project.Project(name='same') # Create the simulation directory
    try:
        directory = project.walter_data()
        params = p.csv_parameters(str(directory/'sim_scheme_ref.csv'))[0] # recovery of parameters
        p.run(**params)
        _compare_list_of_files(p)
        _compare_file_content(p)
    except:
        raise
    finally:
        if debug:
            return p
        else:
            p.remove(force=True)


