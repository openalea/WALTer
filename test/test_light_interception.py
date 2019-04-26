from walter import project
from walter.light import scene_pattern
import pandas


def test_zero_light():

    #assert : all tillers receive light (value > 0 for Sum_PAR in the PAR_per_axes.csv output file)

    p = project.Project(name='zero_light') #Create Folder
    try:
        params = p.csv_parameters('sim_scheme_test.csv')[0]  #Recover list of parameters
        params.update(dict(nb_plt_temp=50, nb_rang=10, nbj=156)) #Add new parameters
        lsys, lstring = p.run(**params)
        PAR_per_axes_dico = lsys.context().locals()['PAR_per_axes_dico']
        df = pandas.DataFrame(PAR_per_axes_dico)
        PAR = df.groupby('Num_plante').agg('sum')['Sum_PAR'].values
        assert all(PAR > 0)
        outdir = p.output_path()
        dfout = pandas.read_csv(outdir/'PAR_per_axes.csv', sep='\t')
        PARout = df.groupby('Num_plante').agg('sum')['Sum_PAR'].values
        assert all(PARout > 0)
    except:
        raise
    finally:
        p.remove(force=True)


def test_shift_in_light():


    #assert : the difference between the light intercepted by one plant on
    # one day and the light intercepted by that same plant the next day
    # (PAR_per_axes.csv output file ; value for Sum_PAR) is always less
    # than 1000% (or x10)
    p = project.Project(name='shift_in_light')
    try:
        # run the reference simulation
        lsys, lstring = p.run_parameters('sim_scheme_test.csv')
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

        assert all(relative_variation < 50)
    except:
        raise
    finally:
        p.remove(force=True)


def test_infinite():
    p = project.Project(name='infinite_canopy')
    try:
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
    except:
        raise
    finally:
        p.remove(force=True)

# debug helper

def test_check_light_balance():
    """test if total par intercepted is above or below incident par"""
    p = project.Project(name='light_balance')
    try:
        params = p.csv_parameters('sim_scheme_test.csv')[0]
        params.update(dict(write_debug_PAR=True, infinity_CARIBU=1))
        lsys, lstring = p.run(**params)
        crop_scheme = lsys.context().locals()['crop_scheme']
        # do we really need debug par dico df ? (simulation time is extremly long !)
        df = pandas.DataFrame(lsys.context().locals()['Debug_PAR_dico_df'])
        control = df.groupby('Elapsed_time').agg({'Organ_PAR':'sum', 'Inc_PAR':'mean'})
        balance = control.Organ_PAR / control.Inc_PAR / crop_scheme['surface_sol']
        assert all(balance <= 1)
    except:
        raise
    finally:
        p.remove(force=True)


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


def shift_in_light_bug():
    """Inspect the shift in light bug """
    p = project.Project(name='shift_in_light')
    params = p.csv_parameters('sim_scheme_test.csv')[0]
    params.update(dict(nbj=225))
    lsys, lstring = p.run(**params)
    res_sky = get_res_sky(lsys, lstring)
    dd = pandas.DataFrame(lsys.context().locals()['PAR_per_organ'])
    dfag=dd.groupby(['Num_plante', 'Num_talle']).agg({'Organ_surface': 'sum', 'tiller_surface':'mean'})
    dfag.tiller_surface / dfag.Organ_surface


def projecion_screen_tuning():
    p = project.Project(name='projection_screen_tuning')
    # run the reference simulation
    lsys, lstring = p.run_parameters('sim_scheme_test.csv')
    caribu_recorder = lsys.context().locals()['caribu_recorder']
    df = pandas.DataFrame(caribu_recorder.records_data())
    p.remove(force=True)
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

