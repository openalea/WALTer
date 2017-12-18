def parameters():
    # simulation tags
    expe_related = "Sensitivity_Analysis"
    rep = 1

    # main controls
    lpy_cut_bug = True
    write_lscene = False
    write_lstring = False
    write_debug_PAR = False
    #
    hazard_plant_xy = True
    hazard_plant_azi = True
    hazard_axis = True
    hazard_organ = True
    hazard_emerg = True

    # plot parameters
    densite = 150
    crop_ccptn = "Mesh_for_nplants"

    ## CARIBU
    CARIBU_state = "enabled"
    infinity_CARIBU = bool(0)  # En booleen 0 : False 1: True
    nb_azimuth = 5
    nb_zenith = 4

    # SIRIUS
    SIRIUS_state = "disabled"

    d = locals().copy()
    return d


def init(params):
    for p_name in params:
        globals().setdefault(p_name, params[p_name])



    d = locals().copy()
    d.pop('params')
    d.update(params)
    return d
