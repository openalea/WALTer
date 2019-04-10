import os
from shutil import rmtree, copy
from walter.command_line import walter_parser
from walter.project import Project


call_dir = os.getcwd()


def reset_call_dir():
    os.chdir(call_dir)


def test_parser():
    parser = walter_parser()
    args = parser.parse_args(''.split())
    assert args.p == '.'
    assert args.i == ''
    args = parser.parse_args('-p my_project -i'.split())
    assert args.p == 'my_project'
    assert args.i == 'walter_default'
    args = parser.parse_args('-p my_project -i my_sim'.split())
    assert args.p == 'my_project'
    assert args.i == 'my_sim'

def test_one_sim():
    reset_call_dir()
    cmd = "walter -p test_one_sim"
    os.system(cmd)
    assert os.path.exists('test_one_sim')
    if os.path.exists('test_one_sim'):
        copy('sim_scheme_fast_test.csv', 'test_one_sim')
        os.chdir('test_one_sim')
        cmd = "walter -i sim_scheme_fast_test.csv"
        os.system(cmd)
        reset_call_dir()
        rmtree('test_one_sim')


def test_multi_simulation():
    reset_call_dir()
    cmd = "walter -i sim_scheme_fast_test2.csv -p test_multi_sim"
    os.system(cmd)
    reset_call_dir()
    if os.path.exists('test_multi_sim'):
        rmtree('test_multi_sim')


def test_multi_simulation_ghost_simulation_error():
    """Only occur on some machine if project.csv_parameters method use simple float precision in read.csv:
      when the bug occurs, the second simulation leads to the generation of 3 ids instead of 2, one corresponding
      to a 'ghost' (no directory generated) simulation with GAI_c_Maxwell = 0.6xxxxxxxxx where xxxxx are
      strange additional digits"""
    reset_call_dir()
    cmd = "walter -i sim_scheme_test_combi_params_err.csv -p combi_params_error"
    os.system(cmd)
    reset_call_dir()
    index_table_test = Project.read_itable("combi_params_error/index-table.json")
    if os.path.exists('combi_params_error'):
        rmtree('combi_params_error')
    assert len(index_table_test) == 2

