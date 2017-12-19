from walter.experimental_conditions import experimental_conditions, get_latitude
from walter.genotypic_parameters import genotypic_parameters, get_genotypic_parameters


def default_parameters():
    """Setup default parameters for walter simulation"""
    # simulation tags
    expe_related = "Sensitivity_Analysis"
    rep = 1
    nbj = 25 + 300  # Duree de la simulation

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
    """Manage expansion of parameters from simulation tags and preccedence rules

    Args:
        user_parameters: a dict of parameters that take precedence over defaults

    Returns:
        A set of simulation parameters
    """
    parameters = default_parameters()
    parameters.update(user_parameters)

    # expansion/ completion
    _p = parameters

    # add experimental conditions if not user-defined with possibly
    # user-redefined expe_related
    parameters = light_update(_p, experimental_conditions(_p['expe_related']))
    # add derived params / aliases
    parameters['crop_genotype'] = _p['genotype']
    parameters['geno_nb'] = len(_p['genotype'])
    parameters['latitude'] = get_latitude(_p['location'])

    # Si SIRIUS n'est pas active, le nombre final de feuilles est fixe a la
    #  donnee experimentale. S'il n'y a pas de donnee experimental il est a 11
    #  par defaut.
    parameters['param_Ln_final'] = _p.get("Ln_final", 11)

    #  genotypic parameters
    genotypic = genotypic_parameters()
    for what in genotypic:
        parameters[what] = {}
    for g in _p['genotype']:
        gp = get_genotypic_parameters(g, user_parameters)
        for what in genotypic:
            parameters[what][g] = gp[what]

    return parameters

