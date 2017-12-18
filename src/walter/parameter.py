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


def initialisation(user_parameters):
    p = user_parameters

    hazard_driver = {"plant_azi": p['hazard_plant_azi'],
                     "plant_xy": p['hazard_plant_xy'],
                     "axis": p['hazard_axis'],
                     "organ": p['hazard_organ'],
                     "emerg": p['hazard_emerg']}


    d = locals().copy()
    d.pop('p')
    d.pop('user_parameters')
    return d
