"""Define genotype-dependant parameters"""


def Maxwell():
    # Final plant height (internodes+peduncle+ear of mainstem)
    Param_PlHeight = 55.6155
    # Tiller emergence
    P_T = 0.88
    P_CT = 0
    ## Internode final length
    # shape. Possibilities are: "linear","squared","Homogenous", "Linear",
    # "ExpIncrease", "ExpDecrease"
    shp_I = "squared"
    # Number of elongated internodes
    N_I_el = 5
    # Linear formalism
    inc_I = 3.48
    # Power formalism
    a_I_L = -0.93
    b_I_L = -0.04
    # Sheath final length
    a_S_L = 0.6919
    b_S_L = -2.6953
    # Blade final length
    # Final length of the first blade of each axis (cm)
    #  old name : first_blade_length
    L_B_1 = 7
    # Final length increment between two successive leaves (bef FT)
    # | old name : incr_Bl
    s_B_1 = 0.8
    # Number of higher leaves with are smaller than the previous
    # old name : nbf_reduce
    N_B_r = 2
    # Reduction factor of blade final length w 2 succ leaves
    # old name : ratio_flag_blade
    s_B_f = 0.8
    # Coefficient for blade width (cm)
    # old name: b_blade_width
    b_B_w = -0.3
    # Fixed dimensions (ear, peduncle, etc.)
    # Diameter of the internode  (cm)
    # old name : internode_diameter
    d_I = 0.38
    # Diameter of the peduncle (cm)
    # old name : peduncle_diameter
    d_P = 0.25
    # Final length of the peduncle (cm)
    # old name : peduncle_length
    L_P = 22.58
    # Diameter of the sheath (cm)
    # old name : sheath_diameter
    d_S = 0.4
    # Diameter of the ear (cm)
    # old name : ear_diameter
    d_E = 0.4
    # Final length of the ear (cm)
    # old name : ear_final_length
    L_E = 7.93
    # Organ death
    # All these parameters are calibrated in order to fit on experimental datas
    #  of Mariem Abichou (cv Maxwell) and Jessica Bertheloot (cv Soissons)
    # Haun stage of the beginning of the first phase of blade senescence
    n0_sen = 4.75
    # Number of green blades at the end of the first phase of blade senescence
    n1_sen = 3.31
    # Number of green blades at the end of the second phase of blade senescence
    #  (only for tillers)
    n2_sen = 4.5
    # Number of green blades at the end of blade senescence
    n3_sen = 0
    # Date of the beginning of the blade senescence
    t0_sen = 468
    # Date of the end of the first phase of blade senescence
    t1_sen = 691
    # Date of the second phase of blade senescence (only for tillers)
    t2_sen = 1131
    # Date of the end of blade senescence
    t3_sen = 2000

    # Tillering cessation model
    # Cessation of tillering
    # Green Area Index threshold above which tillering of a plant stops
    GAI_c = 0.59
    # Tiller death
    # Date of potentiel beginning of the regression (in Haun Stage unit)
    t_beg_reg = 6.8
    # PAR threshold below which a tiller don't survive | old name : PARseuil
    PAR_t = 280000
    # Thermal time interval during which two tillers of the same plant cannot
    # die | old name : duration_plant_protection
    Delta_prot = 75

    d = locals().copy()
    return d


def Soissons():
    Param_PlHeight = 87.6579
    P_T = 0.88
    P_CT = 0
    shp_I = "squared"
    N_I_el = 5
    inc_I = 4.5
    a_I_L = 0.79
    b_I_L = -0.29
    a_S_L = 0.6857
    b_S_L = -2.16
    L_B_1 = 7
    s_B_1 = 0.5
    N_B_r = 1
    s_B_f = 0.92
    b_B_w = -0.4
    d_I = 0.2
    d_P = 0.3
    L_P = 19.8
    d_S = 0.32
    d_E = 0.65
    L_E = 7.38
    n0_sen = 4.91
    n1_sen = 3.3
    n2_sen = 4.35
    n3_sen = 0
    t0_sen = 468
    t1_sen = 691
    t2_sen = 959
    t3_sen = 1850
    #
    GAI_c = 0.78
    t_beg_reg = 6.8
    PAR_t = 150000
    Delta_prot = 50

    d = locals().copy()
    return d

def Caphorn():
    n0_sen = 4.76
    n1_sen = 3.56
    n2_sen = 5.19
    n3_sen = 0
    t0_sen = 382
    t1_sen = 671
    t2_sen = 1050
    t3_sen = 1900
    d = locals().copy()
    return d

def Gigant_Maxwell():
    Param_PlHeight = 110
    shp_I = "ExpIncrease"
    b_I_L = -0.04
    a_S_L = 0.6919
    b_S_L = -2.6953
    #
    GAI_c = 0.35
    t_beg_reg = 7.8
    PAR_t = 100000
    Delta_prot = 25
    #
    new = locals().copy()
    d = Maxwell()
    d.update(new)
    return d


def Darwinkel_Maxwell():
    Param_PlHeight = 55.6155
    shp_I = "ExpIncrease"
    #
    GAI_c = 0.35
    t_beg_reg = 7.8
    PAR_t = 100000
    Delta_prot = 25
    #
    new = locals().copy()
    d = Maxwell()
    d.update(new)
    return d


def get_genotypic_parameters(name='Maxwell', user_parameters={}):
    if name == 'Maxwell':
        p = Maxwell()
    elif name == 'Soissons':
        p = Soissons()
    elif name == 'Gigant_Maxwell':
        p = Gigant_Maxwell()
    elif name == 'Darwinkel_Maxwell':
        p = Darwinkel_Maxwell()
    else:
        raise ValueError('No parameter found for genotype: ' + name)

    for parameter in p:
        user_p = parameter + '_' + name
        if user_p in user_parameters:
            p[parameter] = user_parameters[user_p]

    return p


def genotypic_parameters():
    return Maxwell().keys()
