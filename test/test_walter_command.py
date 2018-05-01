import os
from shutil import rmtree, copy

call_dir = os.getcwd()


def reset_call_dir():
    os.chdir(call_dir)


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

