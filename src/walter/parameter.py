from walter.experimental_conditions import experimental_conditions, liste_expe, get_latitude

def default_parameters():
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

    experiment = experimental_conditions(p['expe_related'])
    crop_genotype = []
    for geno in experiment["genotype"]:
        crop_genotype.append(geno)
    geno_nb = len(crop_genotype)
    if 'year' not in user_parameters:
        year = experiment["year"]
    if 'sowing_date' not in user_parameters:
        sowing_date = experiment["sowing_date"]
    if 'dist_inter_rang' not in user_parameters:
        dist_inter_rang = experiment["dist_inter_rang"]
    if 'location' not in user_parameters:
        location = experiment['location']
    else:
        location = user_parameters['location']
    latitude = get_latitude(location)

    # Si SIRIUS n'est pas active, le nombre final de feuilles est fixe a la
    #  donnee experimentale. S'il n'y a pas de donnee experimental il est a 11
    #  par defaut.
    param_Ln_final = None
    if p['SIRIUS_state'] == "disabled":
        if p['expe_related'] in liste_expe():
            param_Ln_final = experiment["Ln_final"]
        else:
            param_Ln_final = 11

    d = locals().copy()
    d.pop('p')
    d.pop('user_parameters')
    d.pop('experiment')
    return d
