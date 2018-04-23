from walter import project

def test_simu1():
    p = project.Project(name='simu_test1')
    lsys, lstring = p.run(nb_plt_utiles=1,
                          dist_border_x=0,
                          dist_border_y=0,
                          nbj=30,
                          beginning_CARIBU=290)

    assert len(lstring) > 10
    s=lsys.sceneInterpretation(lstring)
    assert len(s) ==1

    p.deactivate()
    p.remove(force=True)


def test_simu2():

    def run_one_simu(p, param_dict):
        lsys, lstring = p.run(**param_dict)

        assert len(lstring) > 10
        s = lsys.sceneInterpretation(lstring)
        assert len(s) > 2

    p = project.Project(name='simu_test2')
    params = p.csv_parameters('sim_scheme_test.csv')

    for param in params:
        param['CARIBU_state'] = 'disabled'

    outs = p.which_outputs
    outs['GAIp'] = 0
    p.which_outputs = outs
    for param_dict in params:
        yield run_one_simu, p, param_dict
    p.deactivate()
    p.remove(force=True)


def test_simu3():

    def run_one_simu(p, param_dict):
        lsys, lstring = p.run(**param_dict)

        assert len(lstring) > 10
        s = lsys.sceneInterpretation(lstring)
        assert len(s) > 2

    p = project.Project(name='simu_test3')
    params = p.csv_parameters('sim_scheme_test.csv')

    outs = p.which_outputs
    p.which_outputs = outs
    for param_dict in params:
        yield run_one_simu, p, param_dict
    p.deactivate()
    p.remove(force=True)

