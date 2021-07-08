"""
Computation of the fitness of each plant in WALTer
based on the amount of light intercepted and the mean temperature
during a key period of the development
"""
from __future__ import division

from builtins import range
from past.utils import old_div
import pandas as pd

def flo_date(Transiflo_dico, nb_days=30):
    """
    Identify days to consider for the fitness

    Parameters
    ----------
    Transiflo_dico: (dict)
        Flowering dates of each axis of each plant (typically dico_stades)
    nb_days: (int)
        Number of days before flowering considered in the computation of the fitness

    Returns
    -------
        A dict with the days to consider for the computation of the fitness for each axis of each plant
    """

    Flo_date_dict = {} # Initializing an empty dictionary that will be filled with the flowwoing loop
    for plante, val in list(Transiflo_dico.items()): # For each plant in the dico_stade dict
        Flo_date_dict[plante] = {} # There is a key for each plant in the Flo_date_dict
        for axis, val2 in list(val.items()): # For each axis in dico_stade dict
            date_flo = val2["Flo"][2] # Flowering date in DOY
            Flo_date_dict[plante][axis] = list(range(date_flo-nb_days, date_flo)) # For each axis of each plant, the dict is filled with a list of DOYs for which the PAR must be summed
    return Flo_date_dict
# WARNING in extreme cases, the line above might not work. If date_flo-nb_days < 0, there would be DOYs such as 0, -1, -2 etc... in the list. 0 should be 365, -1 = 364 etc...
# TODO : change to : range(date_flo_el-nb_days, date_flo_el), where date_flo_el is in elapsed time instead of DOY


def fitness(PAR_dict, geno_dict, flo_date_dict, a_k=1, b_k=0, nb_days=30):
    """
    Computes fitness for each plant in the simulation

    Parameters
    ----------
    PAR_dict: (dict)
        Dictionary with intercepted PAR for each axis of each plant for each day + temperature for each day (typically PAR_per_axes_dico)
    geno_dict: (dict)
        Genotype of each plant (typically genotype_map)
    flo_date_dict: (dict)
        Days to consider for the computation of the fitness for each axis of each plant (typically the output of the flo_date function)
    a_k:
        Coefficient for the calculation of the number of kernels
    b_k:
        Coefficient for the calculation of the number of kernels
    nb_days: (int)
        Number of days before flowering considered in the computation of the fitness

    Returns
    -------
        Pandas data.frame with fitness and genotype for each plant of the simulation
    """

    PARdf = pd.DataFrame(PAR_dict) # Translate the PAR_dict dict into a dataframe

    i = 0

    for plante in PARdf.Num_plante.unique(): # For each plant in the PARdf dataframe
        PARdfplante = PARdf[PARdf.Num_plante == plante] # Take a subset of the dataframe, corresponding to the plant
        for axis in PARdfplante.Num_talle.unique(): # For each axis of the plant
            i = i+1
            PARdfaxe = PARdfplante[PARdfplante.Num_talle == axis] # Take a subset of the dataframe, corresponding to the axis
            if i == 1:
                PAR_fitness = PARdfaxe[PARdfaxe.DOY.isin(flo_date_dict[plante][axis])] # PAR_fitness is a selection of PARdfaxe with only the lines corresponding to the 30 days preceding flowering for each axis of each plant
            else:
                PARdfaxe_bons_jours = PARdfaxe[PARdfaxe.DOY.isin(flo_date_dict[plante][axis])] # Select only the lines corresponding to the 30 days preceding flowering for this axis of this plant
                PAR_fitness = PAR_fitness.append(PARdfaxe_bons_jours) # Append your selection to the PAR_fitness Dataframe


    Final_PAR_fitness = PAR_fitness.groupby(['Num_plante','Num_talle']).agg('sum')[['Sum_PAR', 'Temperature']] # For each axis of each plant, sum the intercepted PAR and the temperature for every days considered
    Final_PAR_fitness['Fitness_by_axis'] = old_div(Final_PAR_fitness['Sum_PAR'],Final_PAR_fitness['Temperature']) # (Fischer, 1985) The fitness (number of kernels) is proportional to the ratio mean(PAR)/mean(Temperature)
    Final_PAR_fitness['Number_of_kernels'] = a_k*Final_PAR_fitness['Fitness_by_axis']+b_k # (Fischer, 1985) The fitness (number of kernels) is a*(mean(PAR)/mean(Temperature))+b

    for plante, axis in Final_PAR_fitness.index: # For each plant in the simulation
        Final_PAR_fitness.loc[plante, 'genotype'] = geno_dict[plante] # Add a column to the Final_PAR_fitness dataframe with the genotype corresponding to the plant


    WALTer_output_for_GenoWALT = old_div((old_div((Final_PAR_fitness.groupby('Num_plante').agg('sum')['Sum_PAR']),nb_days)),(PAR_fitness.groupby('Num_plante').agg('mean')['Temperature']))
    WALTer_output_for_GenoWALT = WALTer_output_for_GenoWALT.to_frame()
    WALTer_output_for_GenoWALT.columns = ['PAR_fitness_by_plant']
    for plante in WALTer_output_for_GenoWALT.index: # For each plant in the simulation
        WALTer_output_for_GenoWALT.loc[plante, 'genotype'] = geno_dict[plante] # Add a column to the WALTer_output_for_GenoWALT dataframe with the genotype corresponding to the plant

    return WALTer_output_for_GenoWALT

