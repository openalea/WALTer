from walter import project
import os
from path import Path


def test_working_dir():
    cwd = Path(os.getcwd()).abspath()

    p = project.Project(name='')
    try:
        assert p.name
        assert str(cwd) != str(p.dirname)
        assert (cwd / p.name).exists()
        assert (cwd / p.name).isdir()
        for d in ('input', 'output'):
            assert (p.dirname / d).exists()
            assert (p.dirname / d).isdir()
        assert (p.dirname / 'which_output_files.csv').exists()

        p.deactivate()
        whereIam = str(Path(os.getcwd()).abspath())
        assert str(cwd) == whereIam, str(cwd) + ' / ' + whereIam

        p.activate()
    except:
        raise
    finally:
        p.remove(force=True)
    assert (cwd / p.name).exists() is False

    p = project.Project()
    p.deactivate()
    pp = project.Project(name=p.name)
    try:
        assert str(pp.dirname) == str(p.dirname)
    except:
        raise
    finally:
        pp.remove(force=True)


def test_which_outputs():
    p = project.Project()
    try:
        output = p.which_outputs
        assert output
        assert output['Apex']
        p.which_outputs = {'Apex': 0}
        new_output = p.which_outputs
        assert not new_output['Apex']
        assert len(new_output) == len(output)  # all outputs flag are required
    except:
        raise
    finally:
        p.remove(force=True)


def test_combi_params():
    p = project.Project()
    try:
        assert len(p.combi_params) == 0

        p.run(dry_run=True)
        combi = p.combi_params
        assert len(combi) == 1
        assert combi.ID[0] == 'walter_defaults'

        p.run(nbj=30, dry_run=True)
        combi = p.combi_params
        assert len(combi) == 2
        assert combi.ID[0] == 'walter_defaults'
        assert combi.nbj[1] == 30

        # repeat run: same id
        p.run(nbj=30, dry_run=True)
        combi = p.combi_params
        assert len(combi) == 2
        assert combi.ID[0] == 'walter_defaults'
        assert combi.nbj[1] == 30

        path = 'sim_scheme_test.csv'
        p.run_parameters(path, dry_run=True)
        combi = p.combi_params
        assert len(combi) == 3
        assert len(combi.columns) == 27

        # repeat
        p.run_parameters(path, dry_run=True)
        combi = p.combi_params
        assert len(combi) == 3
        assert len(combi.columns) == 27
    except:
        raise
    finally:
        p.remove(force=True)
