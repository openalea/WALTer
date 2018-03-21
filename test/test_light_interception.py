from walter import project
from openalea.lpy import Lsystem
from alinea.caribu.CaribuScene import CaribuScene

fake_rule = """
Fake:
  produce Fake"""
fake_lsys = Lsystem()
fake_lsys.addRule(fake_rule)


def force_cut(lstring):
    fake_lsys.axiom = lstring
    return fake_lsys.iterate()

def test_zero_light_dyn():
    p = project.Project(name='simu_test1')
    lsys, lstring = p.run(crop_ccptn='classical',
                          nb_plt_utiles=0,
                          nb_plt_temp=50,
                          nb_rang=10,
                          dist_border_x=10,
                          dist_border_y=10,
                          nbj=50,
                          beginning_CARIBU=2900)
    lstring = force_cut(lstring)
    lscene = lsys.sceneInterpretation(lstring)
    c_scene = CaribuScene(scene=lscene, scene_unit="m")
    _, res_sky = c_scene.run(simplify=True)
    axis_census = lsys.context().locals()['axis_census']
    Debug_PAR_dico_df = lsys.context().locals()['Debug_PAR_dico_df']
    dico_PAR = lsys.context().locals()['dico_PAR']
    tiller_surface = lsys.context().locals()['tiller_surface']
    dico_PAR_per_axis = lsys.context().locals()['dico_PAR_per_axis']
    Tempcum = lsys.context().locals()['Tempcum']
    Temperature = lsys.context().locals()['Temperature']

    #emulate endeach
    if Temperature > 0 and res_sky:
        for num_plt in axis_census.keys():
            for axis in axis_census[num_plt].keys():
                dico_PAR_per_axis[num_plt][axis][round(Tempcum, 1)] = 0
    for id in res_sky['Ei'].keys():
        # if id not in new_lstring: continue
        new_ = lstring[id]
        if ((new_.name == "Blade" and new_[0].photosynthetic == True) or
                (new_.name in ("Sheath", "Internode", "Peduncle")) or
                (new_.name == "Ear" and new_[0].emerged)):
            if new_[0].tiller in axis_census[new_[0].num_plante].keys():
                Debug_PAR_dico_df["Ei"].append(res_sky["Ei"][id])

                if res_sky["Ei"][id] < 0:
                    new_[0].PAR = 0
                else:
                    new_[0].PAR = res_sky["Ei"][id] * res_sky["area"][id]

                new_[0].organ_surface = res_sky["area"][id]
                dico_PAR[new_.name][new_[0].num_plante][new_[0].tiller][
                    new_[0].n] = new_[0].PAR

                if tiller_surface[(lstring[id][0].num_plante, lstring[id][
                    0].tiller)] < 0.00001:
                    dico_PAR_per_axis[lstring[id][0].num_plante][
                        lstring[id][0].tiller][round(Tempcum, 1)] += 0
                else:
                    dico_PAR_per_axis[lstring[id][0].num_plante][
                        lstring[id][0].tiller][round(Tempcum, 1)] += \
                    lstring[id][0].PAR / Temperature / tiller_surface[
                        (lstring[id][0].num_plante, lstring[id][0].tiller)]
    print dico_PAR_per_axis


    p.deactivate()
    p.remove(force=True)


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
