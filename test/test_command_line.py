import os
from shutil import rmtree, copy
from walter.command_line import walter_parser
import json

call_dir = os.getcwd()


def reset_call_dir():
    os.chdir(call_dir)

def read_itable(path):
    def _byteify(input):
        if isinstance(input, dict):
            return {_byteify(key): _byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [_byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input
# The use of the byteify function kill encoding problems from json importation between unicode and strings
    with open(path) as itable:
        return _byteify(json.load(itable))


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

def test_combi_params_error():
    reset_call_dir()
    cmd = "walter -i sim_scheme_test_combi_params_err.csv -p combi_params_error"
    os.system(cmd)
    reset_call_dir()
    index_table_test = read_itable("combi_params_error/index-table.json")
    if os.path.exists('combi_params_error'):
        rmtree('combi_params_error')
    assert len(index_table_test) == 2

