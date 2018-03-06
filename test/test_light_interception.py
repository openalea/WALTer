from walter import project

def test_zero_light():

    def run_one_simu(p, param_dict):
        lsys, lstring = p.run(**param_dict)

        #assert : all tillers receive light (value > 0 for Sum_PAR in the PAR_per_axes.csv output file)

    p = project.Project(name='zero_light')
    params = p.csv_parameters('sim_scheme_test.csv')

    outs = p.which_outputs
    p.which_outputs = outs
    for param_dict in params:
        yield run_one_simu, p, param_dict
    p.deactivate()
    p.remove(force=True)



def test_shift_in_light():

    def run_one_simu(p, param_dict):
        lsys, lstring = p.run(**param_dict)

        #assert : the difference between the light intercepted by one plant on one day and the light intercepted by that same plant the next day (PAR_per_axes.csv output file ; value for Sum_PAR) is always less than 1000% (or x10)

    p = project.Project(name='shift_in_light')
    params = p.csv_parameters('sim_scheme_test.csv')

    outs = p.which_outputs
    p.which_outputs = outs
    for param_dict in params:
        yield run_one_simu, p, param_dict
    p.deactivate()
    p.remove(force=True)
