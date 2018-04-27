from walter import project
from walter.light import get_light, scene_pattern
import pandas


def test_zero_light():

        #assert : all tillers receive light (value > 0 for Sum_PAR in the PAR_per_axes.csv output file)

    p = project.Project(name='zero_light')
    params = p.csv_parameters('sim_scheme_test.csv')[0]
    params.update(dict(nb_plt_temp=50, nb_rang=10, nbj=325))
    outs = p.which_outputs
    p.which_outputs = outs
    lsys, lstring = p.run(**params)
    PAR_per_axes_dico = lsys.context().locals()['PAR_per_axes_dico']
    df = pandas.DataFrame(PAR_per_axes_dico)
    PAR = df.groupby('Num_plante').agg('sum')['Sum_PAR'].values
    assert all(PAR > 0)
    with open(p.dirname/'ID_simul.txt') as f:
        id = f.read()
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
    params = p.csv_parameters('sim_scheme_test.csv')[0]
    outs = p.which_outputs
    p.which_outputs = outs
    lsys, lstring = p.run(**params)
    PAR_per_axes_dico = lsys.context().locals()['PAR_per_axes_dico']
    df = pandas.DataFrame(PAR_per_axes_dico)
    df['relative_Inc_PAR'] = df['Inc_PAR'] / df['Inc_PAR'].mean()
    df['relative_Sum_PAR'] = df['Sum_PAR'] / df['relative_Inc_PAR']


    def _max_variation(x):
        variation = (x.relative_Sum_PAR.diff().abs() / x.relative_Sum_PAR)[1:] * 100
        return variation.max()

    # test max variation per plante
    relative_variation = df.groupby(['Num_plante', 'Elapsed_time']).agg('sum').reset_index().groupby(
        'Num_plante').apply(_max_variation)

    assert all(relative_variation < 100)

    p.deactivate()
    p.remove(force=True)


def test_infinite():
    p = project.Project(name='infinite_canopy')
    params = p.csv_parameters('sim_scheme_test.csv')[0]
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


def check_light_balance():
    """test if total par intercepted is above or below incident par"""
    p = project.Project(name='light_balance')
    params = p.csv_parameters('sim_scheme_test.csv')[0]
    params.update(dict(write_debug_PAR=True,infinity_CARIBU=0))
    outs = p.which_outputs
    p.which_outputs = outs
    lsys, lstring = p.run(**params)
    crop_scheme = lsys.context().locals()['crop_scheme']
    df = pandas.DataFrame(lsys.context().locals()['Debug_PAR_dico_df'])
    control = df.groupby('Elapsed_time').agg({'Organ_PAR':'sum', 'Inc_PAR':'mean'})
    balance = control.Organ_PAR / control.Inc_PAR / crop_scheme['surface_sol']
    p.deactivate()
    p.remove(force=True)


# debug helper

def get_res_sky(lsys, lstring):
    """relaunch light simulation for the last time step"""
    lscene = lsys.sceneInterpretation(lstring)
    current_PAR = lsys.context().locals()['current_PAR']
    nb_azimuth = lsys.context().locals()['nb_azimuth']
    nb_zenith = lsys.context().locals()['nb_zenith']
    crop_scheme = lsys.context().locals()['crop_scheme']
    caribu_scene = lsys.context().locals()['caribu_scene']

    c_scene = caribu_scene(lscene, crop_scheme, current_PAR, nb_azimuth, nb_zenith)
    _, res_sky = c_scene.run(simplify=True)
    return res_sky


def debug_par_dico_df(lsys, lstring, res_sky=None):
    """Construct the Debug_PAR_dico_df"""
    if res_sky is None:
        res_sky = get_res_sky(lsys, lstring)
    Debug_PAR_dico_df = {"Elapsed_time": [], "Temp_cum": [], "Num_plante": [], "Num_talle": [], "Organ_PAR": [],
                         "Organ_type": [], "Num_organe": [], "Organ_surface": [], "Ei": [], "id": [], 'tiller_surface': []}
    elapsed_time = lsys.context().locals()['elapsed_time']
    axis_census = lsys.context().locals()['axis_census']
    Temperature = lsys.context().locals()['Temperature']
    tiller_surface = lsys.context().locals()['tiller_surface']
    for id in res_sky['Ei'].keys():
        # if id not in new_lstring: continue
        new_ = lstring[id]
        if ((new_.name == "Blade" and new_[0].photosynthetic == True) or
                (new_.name in ("Sheath", "Internode", "Peduncle")) or
                (new_.name == "Ear" and new_[0].emerged)):
            if new_[0].tiller in axis_census[new_[0].num_plante].keys():
                Debug_PAR_dico_df["Elapsed_time"].append(elapsed_time)
                Debug_PAR_dico_df["Temp_cum"].append(Temperature)
                Debug_PAR_dico_df["Ei"].append(res_sky["Ei"][id])
                Debug_PAR_dico_df["Organ_type"].append(lstring[id].name)
                Debug_PAR_dico_df["id"].append(id)
                Debug_PAR_dico_df["Num_talle"].append(lstring[id][0].tiller)
                Debug_PAR_dico_df["Num_plante"].append(lstring[id][0].num_plante)
                Debug_PAR_dico_df["Num_organe"].append(lstring[id][0].n)
                Debug_PAR_dico_df["Organ_surface"].append(lstring[id][0].organ_surface)
                Debug_PAR_dico_df["Organ_PAR"].append(lstring[id][0].PAR)
                Debug_PAR_dico_df["tiller_surface"].append(tiller_surface[(lstring[id][0].num_plante,
                                                                                          lstring[id][0].tiller)]*1e-4)
    return Debug_PAR_dico_df

def shift_in_light_bug():
    """Inspect the shift in light bug """
    p = project.Project(name='shift_in_light')
    params = p.csv_parameters('sim_scheme_test.csv')[0]
    params.update(dict(nbj=225))
    lsys, lstring = p.run(**params)
    res_sky = get_res_sky(lsys, lstring)
    Debug_PAR_dico_df = debug_par_dico_df(lsys, lstring, res_sky)
    dd = pandas.DataFrame(Debug_PAR_dico_df)
    dfag=dd.groupby(['Num_plante', 'Num_talle']).agg({'Organ_surface': 'sum', 'tiller_surface':'mean'})
    dfag.tiller_surface / dfag.Organ_surface



def debug_dico_PAR_per_axis(lsys, lstring, res_sky=None):
    """generate a dico_par_per_axis like dict for the current time"""

    axis_census = lsys.context().locals()['axis_census']
    tiller_surface = lsys.context().locals()['tiller_surface']
    Temperature = lsys.context().locals()['Temperature']
    dico_PAR_per_axis = {}
    for num_plt in axis_census.keys():
        if num_plt not in dico_PAR_per_axis:
            dico_PAR_per_axis[num_plt] = {}
        for axis in axis_census[num_plt].keys():
            dico_PAR_per_axis[num_plt][axis] = 0
    for id in res_sky['Ei'].keys():
        new_ = lstring[id]
        if ((new_.name == "Blade" and new_[0].photosynthetic == True) or
                (new_.name in ("Sheath", "Internode", "Peduncle")) or
                (new_.name == "Ear" and new_[0].emerged)):
            if new_[0].tiller in axis_census[new_[0].num_plante].keys():
                if tiller_surface[(lstring[id][0].num_plante, lstring[id][0].tiller)] < 0.00001:
                    dico_PAR_per_axis[lstring[id][0].num_plante][lstring[id][0].tiller] += 0
                else:
                    dico_PAR_per_axis[lstring[id][0].num_plante][lstring[id][0].tiller] += lstring[id][
                                                                                              0].PAR \
                                                                                           / Temperature / \
                                                                                          tiller_surface[(
                                                                                          lstring[id][0].num_plante,
                                                                                          lstring[id][0].tiller)]
    return dico_PAR_per_axis

