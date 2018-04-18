from walter import project
from walter.light import get_light, scene_pattern
import pandas


def test_zero_light():

    #assert : all tillers receive light (value > 0 for Sum_PAR in the PAR_per_axes.csv output file)

    p = project.Project(name='zero_light') #Create Folder
    params = p.csv_parameters('sim_scheme_test.csv') #Recover list of parameters
    params = p.generate_index_table(params) #Generate ID for each simulation.
    params = p.csv_parameters(p.name +'/combi_params.csv')[0] #Recover list of parameters with ID.
    params.update(dict(nb_plt_temp=50, nb_rang=10, nbj=156)) #Add new parameters
    outs = p.which_outputs
    p.which_outputs = outs
    lsys, lstring = p.run(**params)
    PAR_per_axes_dico = lsys.context().locals()['PAR_per_axes_dico']
    df = pandas.DataFrame(PAR_per_axes_dico)
    PAR = df.groupby('Num_plante').agg('sum')['Sum_PAR'].values
    assert all(PAR > 0)
    id = p.get_id(0, params)
    dfout = pandas.read_csv(p.dirname/'output'/id/'PAR_per_axes.csv', sep='\t')
    PARout = df.groupby('Num_plante').agg('sum')['Sum_PAR'].values
    assert all(PARout > 0)

    p.deactivate()
    p.remove(force=True)


def test_shift_in_light():


    #assert : the difference between the light intercepted by one plant on
    # one day and the light intercepted by that same plant the next day
    # (PAR_per_axes.csv output file ; value for Sum_PAR) is always less
    # than 1000% (or x10)
    p = project.Project(name='shift_in_light')
    params = p.csv_parameters('sim_scheme_test.csv')
    params = p.generate_index_table(params)
    params = p.csv_parameters('zero_light/combi_params.csv')[0]
    outs = p.which_outputs
    p.which_outputs = outs
    lsys, lstring = p.run(**params)
    PAR_per_axes_dico = lsys.context().locals()['PAR_per_axes_dico']
    df = pandas.DataFrame(PAR_per_axes_dico)
    df['relative_Inc_PAR'] = df['Inc_PAR'] / df['Inc_PAR'].mean()
    df['relative_Sum_PAR'] = df['Sum_PAR'] / df['relative_Inc_PAR']

    def _mean_variation(x):
        variation = (x.relative_Sum_PAR.diff().abs() / x.relative_Sum_PAR)[1:] * 100
        return variation.mean()

    relative_variation = df.groupby(['Num_plante', 'Num_talle']).apply(_mean_variation)
    assert all(relative_variation < 50)
    p.deactivate()
    p.remove(force=True)


def test_infinite():
    p = project.Project(name='infinite_canopy')
    params = p.csv_parameters('sim_scheme_test.csv')
    params = p.generate_index_table(params)
    params = p.csv_parameters(p.name +'/combi_params.csv')[0]
    params.update(dict(nb_plt_utiles=1,
                          dist_border_x=0,
                          dist_border_y=0,
                          nbj=53,
                          infinity_CARIBU=1,
                          beginning_CARIBU=290))
    lsys, lstring = p.run(**params)
    crop_scheme = lsys.context().locals()['crop_scheme']
    pattern = scene_pattern(crop_scheme)
    assert pattern[0] > 1
    p.deactivate()
    p.remove(force=True)


def debug_stuff():
    # some lines that can be run after lsys, lstring = p.run(**pars)
    # to examine how caribu run
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

    lstring = force_cut(lstring)
    lscene = lsys.sceneInterpretation(lstring)
    current_PAR = lsys.context().locals()['current_PAR']
    nb_azimuth = lsys.context().locals()['nb_azimuth']
    nb_zenith = lsys.context().locals()['nb_zenith']
    light = get_light(current_PAR, nb_azimuth, nb_zenith)
    c_scene = CaribuScene(scene=lscene, scene_unit="m", light=light)
    _, res_sky = c_scene.run(simplify=True)
    axis_census = lsys.context().locals()['axis_census']
    Debug_PAR_dico_df = lsys.context().locals()['Debug_PAR_dico_df']
    dico_PAR = lsys.context().locals()['dico_PAR']
    tiller_surface = lsys.context().locals()['tiller_surface']
    dico_PAR_per_axis = lsys.context().locals()['dico_PAR_per_axis']
    Tempcum = lsys.context().locals()['Tempcum']
    Temperature = lsys.context().locals()['Temperature']

    # emulate endeach
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
