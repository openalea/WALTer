from walter.experimental_conditions import experimental_conditions, get_latitude

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


def light_update(old, new):
    """update old with new only for key in new not in old"""
    items = {k:v for k,v in new.iteritems() if k not in old}
    old.update(items)
    return old


def initialisation(user_parameters):
    _p = user_parameters
    # add experimental conditions if not user-defined with possibly
    # user-redefined expe_related
    _p = light_update(_p, experimental_conditions(_p['expe_related']))

    hazard_driver = {"plant_azi": _p['hazard_plant_azi'],
                     "plant_xy": _p['hazard_plant_xy'],
                     "axis": _p['hazard_axis'],
                     "organ": _p['hazard_organ'],
                     "emerg": _p['hazard_emerg']}

    crop_genotype = []
    for geno in _p['genotype']:
        crop_genotype.append(geno)
    geno_nb = len(crop_genotype)
    latitude = get_latitude(_p['location'])

    # Si SIRIUS n'est pas active, le nombre final de feuilles est fixe a la
    #  donnee experimentale. S'il n'y a pas de donnee experimental il est a 11
    #  par defaut.
    param_Ln_final = _p.get("Ln_final", 11)


    d = locals().copy()
    d.pop('_p')
    d.pop('user_parameters')
    d.update(_p)
    return d

