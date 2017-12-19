import datetime

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
    # control if variability factor are applied or not
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
    # Final leaf number by SIRIUS
    Tvermin = 0
    Tverint = 8
    Tvermax = 17
    Lmax = 24
    Lmin = 8
    DLsat = 15
    # Adjusting phyllochrone to leaf number
    Ldecr = 2
    Lincr = 8
    phyllo_decr = 0.75
    phyllo_incr = 1.25


    # Thermal time
    Tbase = 0.
    # temps phyllochronique
    DelayHSToCol = 0.2

    # Phenology
    Delta_hf = 1.3  # Delay between heading and flowering (phyllochronic unit) | old name : delta_epi_flo
    Delta_c_GN = 30  # Duration of the critical period determining grain number (days) | old name : duration_critical_period
    Delta_hm = 800  # Delay between heading and maturity (in degree-days) | old name : delta_epi_mat
    Delta_lflf = 1.39  # Delay between the ligulation of the flag leaf and flowering (phyllochronic units) | old name : delta_ligflagleaf_flo

    # Adjusting phyllochron to extreme sowing dates
    SDSA = 200  # mi-juillet (en DOY)
    SDWS = 90  # Fin de l'hiver (
    Rp = 0.003  # decroissement du phyllo

    # Organ initiation, emergence and elongation
    # Number of primordia already preformed inside the seed
    # old name : nb_primord_seed
    N_p_s = 4
    # Thermal time shift between the floral transition of axes belonging to
    #  two consecutive cohorts | old name : transiflo_shift_param
    Psi_FT = 0
    # Tiller emergence
    # Delay between the initiation of a bud and the start of its activity
    # (plastochronic unit) | old name : inactive_time_bud
    Delta_b = 1
    # dimensions
    # length of the coleoptil at the emergence
    # old name : coleoptil_length
    l_c = 0.5
    ED_I = 1.66  # Duration for internode extension (value extracted directly from ADEL-wheat) (phyllochronic time) | old name : gr_duration_internode
    ED_B = 1.6  # Duration for blade extension (phyllochronic time)                                                | old name : gr_duration_blade
    ED_FB = 1  # Duration for the extension of the flag blade(phyllochronic time)                                 | old name : gr_duration_flagblade
    ED_S = 0.4  # Duration for sheath extension (phyllochronic time)                                                 | old name : gr_duration_sheath
    ED_P = 2  # Duration for peduncle extension (phyllochronic time)                                                 | old name : gr_duration_peduncle

    # Organ death
    Delta_flsp = 100  # Thermal time delay between the senescence of the flag blade and the beginning of peduncle senescence (en degree-days) | old name : delta_senflagleaf_to_senped

    # Cessation of tillering
    cohorte_max = 9
    # Infinitisation du couvert pour le calcul du GAI de proximite
    infinity_GAIp = "True"      # A METTRE EN TEXTE
    dGAIp = 1  # Maximal range of plant detection (meter)
    L_b_S = 2  # Buried length of the first sheath (in cm) | old name : L_burried

    # Tiller death
    Delta_l = 100  # Duration of radiation integration to determine the survival of a tiller (degree-day) | old name : ray_integration
    Delta_SGtC = 600  # Thermal time between the moment a tiller stops growing and its entire removal | old name : delta_stopgr_to_cut
    Delta_SGtR = 200  # Thermal time between the moment a tiller stops growing and the beginning of the reverse growth of leaves | old name : delta_stopgr_to_reg

    # Plant geometry
    Phi_zen_B = 40  # Angle between blade inclination and Y axis | old name : bl_incl_shift
    Phi_azi_B = 185  # Angle between the azimuth of two consecutive blades | old name : bl_azi_shift
    Phi_zen_T = 0  # Angle between the zenith of two consecutive tillers  | old name : till_zen_shift
    Phi_azi_T = 40  # Angle between the azimuth of two consecutive tillers | old name : till_azi_shift

    Phi_zen_E = 0  # Angle between ear inclination and Y axis | old name : ear_zen_shift
    Phi_azi_S = 0  # Angle between seed azimuth and X axis | old name : seed_azi_shift
    Phi_zen_S = 0  # Angle between seed inclination and Y axis | old name : seed_zen_shift

    # Variability parameters (will be controled by hazard controls
    y_position_hazard = 2
    x_position_hazard = 3
    z_position_hazard = 0
    blade_incl_hazard = 5
    blade_azi_hazard = 20
    till_zen_hazard = 7
    till_azi_hazard = 90
    plant_azi_hazard = 360

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

    # Phyllochron adjustment and phyllochon dependant parameters
    double_finger = datetime.date(int(_p['year']) - 1, 1, 1)  # Premier janvier
    sowing_DOY = (_p['sowing_date'] - double_finger).days  # DOY du semis
    parameters['phyll_adjust'] = parameters['Phl'].copy()
    if sowing_DOY < _p['SDSA']:
        for g in _p['genotype']:
            parameters['phyll_adjust'][g] *= (1 - _p['Rp'] * min(sowing_DOY, _p['SDWS']))
    #
    parameters['Pls'] = {g: parameters['phyll_adjust'][g] / 2. for g in
                         _p['genotype']}
    parameters['DelayTipToHS'] = {g: parameters['phyll_adjust'][g] * 0.4125 for
                                  g in _p['genotype']}
    for what in ('Pls', 'DelayTipToHS'):
        for g in _p['genotype']:
            user_p = what + '_' + g
            if user_p in parameters: # it has been set externally
                parameters[what][g] = parameters.pop(user_p)

    # hazard driver will trigger if necessary hazard in different cases:
    # if hazard == False : hazard parameter value = 0, if hazard == True,
    # hazard parameter value is set at the value of the parameter
    for what in ('y_position_hazard','x_position_hazard','z_position_hazard'):
        parameters[what] *= int(_p['hazard_plant_xy'])
    for what in ('blade_incl_hazard', 'blade_azi_hazard'):
        parameters[what] *= int(_p['hazard_organ'])
    for what in ('till_zen_hazard', 'till_azi_hazard'):
        parameters[what] *= int(_p['hazard_axis'])
    parameters['plant_azi_hazard'] *= int(_p['hazard_plant_azi'])

    # syntactic sugars
    parameters['Delta_Reg'] = _p['Delta_SGtC'] - _p['Delta_SGtR']  # | old name : duration_reg
    parameters['hazard_driver'] = {
        "plant_azi": _p['hazard_plant_azi'],
        "plant_xy": _p['hazard_plant_xy'],
        "axis": _p['hazard_axis'],
        "organ": _p['hazard_organ'],
        "emerg": _p['hazard_emerg']}

    return parameters

