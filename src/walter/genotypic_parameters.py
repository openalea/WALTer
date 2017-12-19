"""Define genotype-dependant parameters"""


def Maxwell():
    # Final plant height (internodes+peduncle+ear of mainstem)
    Param_PlHeight = 55.6155
    d = locals().copy()
    return d


def Soissons():
    Param_PlHeight = 87.6579
    d = locals().copy()
    return d


def Gigant_Maxwell():
    Param_PlHeight = 110
    d = locals().copy()
    return d


def Darwinkel_Maxwell():
    Param_PlHeight = 55.6155
    d = locals().copy()
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
        raise ValueError('No parameter found for genotype: '+ name )

    for parameter in p:
        user_p = parameter + '_' + name
        if user_p in user_parameters:
            p[parameter] = user_parameters[user_p]

    return p


def genotypic_parameters():
    return Maxwell().keys()