"""
this is output_manager.
"""
### Importation de libraries
import pandas as pd
from math import pi
import os
import os.path

# which_output_files = pd.read_csv(pj(data_dir, "which_output_files.csv"), sep="\t")
# write_output_file = {"GAI": which_output_files.GAIp[0], "Peraxes": which_output_files.Peraxes[0],
#                      "Proba": which_output_files.Proba[0], "Apex_Sirius": which_output_files.Apex_sirius[0],
#                      "Apex": which_output_files.Apex[0], "Apex_R": which_output_files.Apex_R[0],
#                      "Blade": which_output_files.Blade[0], "Internode": which_output_files.Internode[0],
#                      "Sheath": which_output_files.Sheath[0], "Ear": which_output_files.Ear[0],
#                      "Peduncle": which_output_files.Peduncle[0], "PAR_per_axes": which_output_files.PAR_per_axes[0],
#                      "Lstring": which_output_files.Lstring[0], "Lscene": which_output_files.Lscene[0]}
# print "ce qu'on ecrit:", write_output_file["Lscene"]


### --- Initialisation --- ###

# initialise all the variables at the same time.

class Logger(object):
    """ Composite class to log the different elements through time during the simulation

    This class has the same interface than Log and contains the set of sub-Log class instances.
    """
    loggers = None

    def __init__(self):
        """ Create all the children classes based on the csv config file"""
        if self.loggers is None:
            subclass = [ApexSiriusLog,
                        ApexRLog,
                        ApexLog,
                        BladeLog,
                        InternodeLog,
                        SheathLog,
                        EarLog,
                        PeduncleLog,
                        GAILog,
                        PeraxesLog,
                        ProbaLog,
                        DebugLog]

            #Do not check the condition of config_file
            self.loggers = dict((klass.name, klass()) for klass in subclass)

    def add(self, subclass):
        """ Add children class in Logger if there isn't defined in the init"""
        if subclass not in self.loggers.keys():
                self.loggers.update(subclass, subclass())

    def write(self, dirname):
        """Write each logger into a file"""
        if self.loggers is not None:
            for subclass in self.loggers.values():
                subclass.write(dirname)

    def log(self, **kwds):
        """log each logger """
        if self.loggers is not None:
            for subclass in self.loggers.values():
                subclass.log(**kwds)


# ABSTRACT Class
class Log(object):
    """
    Abstract class used to implements the differents subclass
    """
    def __init__(self):
        """
        Initialize the dictionnary
        """
        self.df = dict()
        for var in self.fields:
            self.df[var] = []

    def write(self, dirname):
        """
        Write the csv file
        """
        _df = pd.DataFrame(self.df)
        df = _df.reindex(self.fields, axis="columns", copy=False)
        # create or check if the directory exist and create it if not

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        df.to_csv(os.path.join(dirname, self.name + ".csv"), sep="\t",
                  header=True, index=False)

    def log(self, **kwargs):
        # tout les logs-fils possedent les memes noms d'attributs
        # Ne marche que si :
        # Le log_mere contient toutes les variables a transmettre, dont les dictionnaires et leurs indices.
        for var in self.df:
            var.append(kwargs[var])


### SUBCLASS - LEGACY OF LOG ###

class GAILog(Log):
    """
    Log GAI through time.

    """
    fields = ["Init_flag", "Elapsed_time", "Temp_cum", "DOY", "Genotype",
              "Num_plante", "Surface_plante", "Surface_visible", "Surface_sol",
              "GAI_tot", "GAI_center", "GAI_ind", "GAI_prox", "Position"]

    name = 'GAI'

    def activate(self):
        """
        If Caribu is enabled
        This function must be static ?
        """
        self.fields.append("Weakest_axis", "PAR_weakest_axis")

    def __init__(self):
        """
        Initialize the GAI output file.
        """
        super(GAILog, self).__init__()


class ApexSiriusLog(Log):
    """
    Log Apex_Sirius throught time

    """
    fields = ["Elapsed_time","Temperature","Temp_cum","Daylength","Num_plante",
              "Genotype","PN","LN","Sumtemp","Vern_rate","Vern_prog",
              "Vern_flag","Debut_ppd_flag","Fin_ppd_flag","Ln_pot","Var_L_min",
              "Ln_app","Ln_final"]

    name = 'ApexSirius'

    def __init__(self):
        """
        Initialize the Apex_Sirius output file
        """
        super(ApexSiriusLog, self).__init__()


class ApexLog(Log):
    """
    Log Apex throught time

    """
    fields = ["Elapsed_time","Temperature","Temp_cum","Time_count","Sum_temp",
              "Current_PAR","Num_plante", "Genotype","Num_talle","Num_cohorte",
              "Nb_phyto_emi","Nb_emerged_leaf","Transiflo_flag",
              "STOP_init_flag","Transiflo_DOY","Ln_final"]
    name = 'Apex'

    def __init__(self):
        """
        Initialize the Apex_Sirius output file
        """
        super(ApexLog, self).__init__()


class ApexRLog(Log):
    """
    Log Apex throught time

    """
    fields = ["Elapsed_time","DOY","Temperature","Temp_cum","Sum_temp",
              "Num_plante","Genotype","Num_cohorte","Ln_final","Num_talle",
              "Date_epiaison","Epi_DOY","Date_de_flo","Mont_flag","Mont_DOY",
              "Flo_flag","Flo_DOY","Death_flag","Date_de_maturite", "Mat_DOY"]

    name = 'ApexR'

    def __init__(self):
        """
        Initialize the ApexR output file
        """
        super(ApexRLog, self).__init__()


class BladeLog(Log):
    """
    Log Blade throught time

    """
    fields = ["Elapsed_time","Temp_cum","Temperature","Num_plante","Genotype",
              "Num_talle","Num_cohorte","Num_rang","Blade_sumtemp","Blade_width",
              "Blade_length","Blade_visible_length","Blade_final_length",
              "Blade_visible_surface","Blade_surface","Blade_PAR","Senesc_flag",
              "Photosynthetic"]
    name = 'Blade'

    def __init__(self):
        """
        Initialize the Blade output file
        """
        super(BladeLog, self).__init__()


class InternodeLog(Log):
    """
    Log Internode throught time
    """
    fields = ["Elapsed_time","Temp_cum","Temperature","Num_plante","Genotype",
              "Num_talle","Num_cohorte","Num_rang","Internode_length",
              "Internode_final_length","Internode_surface","Internode_PAR",
              "Photosynthetic"]
    name = 'Internode'

    def __init__(self):
        """
        Initialize the Internode output file
        """
        super(InternodeLog, self).__init__()


class PeduncleLog(Log):
    """
    Log Peduncle throught time
    """
    fields = ["Elapsed_time","Temp_cum","Temperature","Num_plante","Genotype",
              "Num_talle","Num_cohorte","Num_rang", "Sum_temp",
              "Peduncle_length","Peduncle_final_length","Peduncle_surface",
              "Peduncle_PAR","Photosynthetic"]
    name = 'Peduncle'

    def __init__(self):
        """
        Initialize the Peduncle output file
        """
        super(PeduncleLog, self).__init__()

        
class SheathLog(Log):
    """
    Log Sheath throught time
    """
    fields = ["Elapsed_time","Temp_cum","Temperature","Num_plante","Genotype",
              "Num_talle","Num_cohorte","Num_rang","Sheath_sumtemp",
              "Sheath_diameter","Sheath_length","Sheath_final_length",
              "Sheath_surface","Sheath_PAR","Photosynthetic"]
    name = 'Sheath'

    def __init__(self):
        """
        Initialize the Sheath output file
        """
        super(SheathLog,self).__init__()


class EarLog(Log):
    """
    Log Ear throught time
    """
    fields = ["Elapsed_time","Temp_cum","Temperature","Num_plante","Genotype",
              "Num_talle","Ear_sumtemp","Ear_length","Ear_surface","Ear_PAR",
              "Photosynthetic","Emerged"]

    name = 'Ear'

    def __init__(self):
        """
        Initialize the Ear output file
        """
        super(EarLog, self).__init__()


class ProbaLog(Log):
    """
    Log Proba throught time
    """
    fields = ["Elapsed_time","Temp_cum","Temperature","Num_plante","Genotype",
              "Num_talle","Ear_sumtemp","Ear_length","Ear_surface","Ear_PAR",
              "Photosynthetic","Emerged"]

    name = 'Proba'

    def __init__(self):
        """
        Initialize the Proba output file
        """
        super(ProbaLog, self).__init__()


class PeraxesLog(Log):
    """
    Log Peraxes throught time
    """
    fields = ["Init_flag", "Elapsed_time", "DOY", "Temperature", "Temp_cum", "Num_plante", "Num_talle", "Sheath_max",
                 "Collar_height", "Dead_collar_height", "Delta_H", "Visible_leaves_surface", "Visible_surface",
                 "Leaf_contrib_to_GAI", "Stem_contrib_to_GAI", "Ear_contrib_to_GAI", "Peduncle_contrib_to_GAI",
                 "Stop_growth_flag"]

    name = 'Peraxes'

    def __init__(self):
        """
        Initialize the Peraxes output file
        """
        super(PeraxesLog, self).__init__()


class DebugLog(Log):
        """
        Log Debug throught time
        """
        fields = ["Elapsed_time", "Temp_cum", "Num_plante", "Num_talle",
                  "Organ_PAR",
                  "Organ_type", "Num_organe", "Organ_surface", "Ei"]

        name = 'Debug'
        
        def __init__(self):
            """
            Initialize the Debug output file
            """
            super(DebugLog, self).__init__()


class ParPerAxesLog(Log):
    """
    Log ParPerAxes throught time
    """
    fields = ["Elapsed_time", "Temp_cum", "Num_plante", "Num_talle",
              "Sum_PAR", "Inc_PAR"]
    name = 'ParPerAxes'

    def __init__(self):
        """
        Initialize the ParPerAxes output file
        """
        super(ParPerAxesLog, self).__init__()

### --- Log --- ###

"""
#Comparaison des differentes signatures 

log_Apex_Sirius    (day, current_temperature, _Tempcum, duree_du_jour, latitude, DOY, StA)
log_Apex           (elapsed_time, Temperature, Tempcum, current_PAR, cohort_number, StA)
log_Apex_R         (elapsed_time, DOY, Temperature, Tempcum, cohort_number, dico_stades, StAR)
log_Proba          (elapsed_time, Temperature, Tempcum, GAI_prox, StBu)
log_Blade          (elapsed_time, Tempcum, Temperature, cohort_number, leaf_emergence, StBl):
log_Sheath         (elapsed_time, Tempcum, Temperature, cohort_number, StS):
log_Ear            (elapsed_time, Tempcum, StE):
log_Internode      (elapsed_time, Tempcum, Temperature, cohort_number, StI)
log_Peduncle       (elapsed_time, Tempcum, Temperature, cohort_number, StP):
log_Peraxes        (initialization_Flag, num_plt, elapsed_time, DOY, Temperature,Tempcum, axis, Sh_max_temp, Hcol_max, Hcol_dead, delta_H, tiller_surface, axis_census, leaf_contrib,
                stem_contrib, ear_contrib, peduncle_contrib)
log_Debug_PAR      (elapsed_time, Temperature, lstring):
log_Gai            (initialization_Flag, num, elapsed_time, Tempcum, DOY, surface_plante, surface_plante_visible,
            crop_scheme, GAI_tot, GAI_center, GAI_ind, GAI_prox):
log_PAR_per_axes   (elapsed_time, Tempcum, num_plt, axis, current_PAR, dico_PAR_per_axis):
"""

def log_Apex_Sirius(Apex_Sirius_dico_df, day, current_temperature, _Tempcum, duree_du_jour, latitude, DOY, StA):
    apex = Apex_Sirius_dico_df


    Apex_Sirius_dico_df['Elapsed_time'].append(day)
    Apex_Sirius_dico_df['Temperature'].append(current_temperature)
    Apex_Sirius_dico_df['Temp_cum'].append(_Tempcum)
    Apex_Sirius_dico_df['Daylength'].append(duree_du_jour(latitude, DOY))
    Apex_Sirius_dico_df['Num_plante'].append(StA.num_plante)
    Apex_Sirius_dico_df['Genotype'].append(StA.geno)
    Apex_Sirius_dico_df['PN'].append(StA.pn)
    Apex_Sirius_dico_df['LN'].append(StA.ln)
    Apex_Sirius_dico_df['Sumtemp'].append(StA.sumtemp)
    Apex_Sirius_dico_df['Vern_rate'].append(StA.vern_rate)
    Apex_Sirius_dico_df['Vern_prog'].append(StA.vern_prog)
    Apex_Sirius_dico_df['Vern_flag'].append(StA.vrn)
    Apex_Sirius_dico_df['Debut_ppd_flag'].append(StA.debut_ppd)
    Apex_Sirius_dico_df['Fin_ppd_flag'].append(StA.photop_flag)
    Apex_Sirius_dico_df['Ln_pot'].append(StA.Ln_pot)
    Apex_Sirius_dico_df['Var_L_min'].append(StA.var_Lmin)
    Apex_Sirius_dico_df['Ln_app'].append(StA.Ln_app)
    Apex_Sirius_dico_df['Ln_final'].append(StA.Ln_final)


def log_Apex(Apex_dico_df, elapsed_time, Temperature, Tempcum, current_PAR, cohort_number, StA):
    Apex_dico_df['Elapsed_time'].append(elapsed_time)
    Apex_dico_df['Temperature'].append(Temperature)
    Apex_dico_df['Temp_cum'].append(Tempcum)
    Apex_dico_df['Time_count'].append(StA.time)
    Apex_dico_df['Sum_temp'].append(StA.sumtemp)
    Apex_dico_df['Current_PAR'].append(current_PAR)
    Apex_dico_df['Num_plante'].append(StA.num_plante)
    Apex_dico_df['Genotype'].append(StA.geno)
    Apex_dico_df['Num_talle'].append(str(StA.tiller))
    Apex_dico_df['Num_cohorte'].append(cohort_number(StA.tiller))
    Apex_dico_df['Nb_phyto_emi'].append(StA.n)


def log_Apex_R(Apex_R_dico_df, elapsed_time, DOY, Temperature, Tempcum, cohort_number, dico_stades, StAR):
    Apex_R_dico_df['Elapsed_time'].append(elapsed_time)
    Apex_R_dico_df['DOY'].append(DOY)
    Apex_R_dico_df['Temperature'].append(Temperature)
    Apex_R_dico_df['Temp_cum'].append(Tempcum)
    Apex_R_dico_df['Sum_temp'].append(StAR.sumtemp)
    Apex_R_dico_df['Num_cohorte'].append(cohort_number(StAR.tiller))
    Apex_R_dico_df['Ln_final'].append(StAR.Ln_final)
    Apex_R_dico_df['Num_plante'].append(StAR.num_plante)
    Apex_R_dico_df['Genotype'].append(StAR.geno)
    Apex_R_dico_df['Num_talle'].append(StAR.tiller)
    Apex_R_dico_df['Mont_flag'].append(StAR.mont)
    Apex_R_dico_df['Mont_DOY'].append(dico_stades[StAR.num_plante][StAR.tiller]["Montaison"][2])
    Apex_R_dico_df['Flo_flag'].append(StAR.flo)
    Apex_R_dico_df['Flo_DOY'].append(dico_stades[StAR.num_plante][StAR.tiller]["Flo"][2])
    Apex_R_dico_df['Death_flag'].append(StAR.death_flag)
    Apex_R_dico_df['Date_epiaison'].append(dico_stades[StAR.num_plante][StAR.tiller]["Epiaison"][1])
    Apex_R_dico_df['Epi_DOY'].append(dico_stades[StAR.num_plante][StAR.tiller]["Epiaison"][2])
    Apex_R_dico_df['Date_de_flo'].append(dico_stades[StAR.num_plante][StAR.tiller]["Flo"][1])
    Apex_R_dico_df['Mat_DOY'].append(dico_stades[StAR.num_plante][StAR.tiller]["Maturite"][2])
    Apex_R_dico_df['Date_de_maturite'].append(dico_stades[StAR.num_plante][StAR.tiller]["Maturite"][1])


def log_Proba(Proba_dico_df, elapsed_time, Temperature, Tempcum, GAI_prox, StBu):
    Proba_dico_df["Elapsed_time"].append(elapsed_time)
    Proba_dico_df["Temperature"].append(Temperature)
    Proba_dico_df["Temp_cum"].append(Tempcum)
    Proba_dico_df["Num_plante"].append(StBu.num_plante)
    Proba_dico_df["Genotype"].append(StBu.geno)
    Proba_dico_df["Num_talle"].append(str(StBu.tiller[0:len(StBu.tiller) - 1]))
    Proba_dico_df["Num_rang"].append(StBu.tiller[-1])
    Proba_dico_df["Sumtemp"].append(StBu.sumtemp)
    Proba_dico_df["GAI_prox"].append(GAI_prox[StBu.num_plante])
    Proba_dico_df["P_debourr"].append(StBu.p_debourr)


def log_Blade(Blade_dico_df, elapsed_time, Tempcum, Temperature, cohort_number, leaf_emergence, StBl):
    Blade_dico_df['Elapsed_time'].append(elapsed_time)
    Blade_dico_df['Temp_cum'].append(Tempcum)
    Blade_dico_df['Temperature'].append(Temperature)
    Blade_dico_df['Num_plante'].append(StBl.num_plante)
    Blade_dico_df['Genotype'].append(StBl.geno)
    Blade_dico_df['Num_talle'].append(str(StBl.tiller))
    Blade_dico_df['Num_cohorte'].append(cohort_number(StBl.tiller))
    Blade_dico_df['Num_rang'].append(StBl.n)
    Blade_dico_df['Blade_sumtemp'].append(leaf_emergence[StBl.num_plante][StBl.tiller][StBl.n][1])
    Blade_dico_df['Blade_width'].append(StBl.width)
    Blade_dico_df['Blade_length'].append(StBl.length)
    Blade_dico_df['Blade_visible_length'].append(StBl.visible_length)
    Blade_dico_df['Blade_final_length'].append(StBl.final_length)
    Blade_dico_df['Blade_visible_surface'].append(StBl.visible_area)
    Blade_dico_df['Blade_surface'].append((StBl.width * StBl.length * 0.75))
    Blade_dico_df['Blade_PAR'].append(StBl.PAR)
    Blade_dico_df['Senesc_flag'].append(StBl.senesc_flag)
    Blade_dico_df['Photosynthetic'].append(StBl.photosynthetic)


def log_Sheath(Sheath_dico_df, elapsed_time, Tempcum, Temperature, cohort_number, StS):
    Sheath_dico_df['Elapsed_time'].append(elapsed_time)
    Sheath_dico_df['Temp_cum'].append(Tempcum)
    Sheath_dico_df['Temperature'].append(Temperature)
    Sheath_dico_df['Num_plante'].append(StS.num_plante)
    Sheath_dico_df['Genotype'].append(StS.geno)
    Sheath_dico_df['Num_talle'].append(str(StS.tiller))
    Sheath_dico_df['Num_cohorte'].append(cohort_number(StS.tiller))
    Sheath_dico_df['Num_rang'].append(StS.n)
    Sheath_dico_df['Sheath_sumtemp'].append(StS.sumtemp)
    Sheath_dico_df['Sheath_diameter'].append(StS.diameter)
    Sheath_dico_df['Sheath_length'].append(StS.length)
    Sheath_dico_df['Sheath_final_length'].append(StS.final_length)
    Sheath_dico_df['Sheath_surface'].append(
        pi * (StS.diameter / 2) * StS.length)
    Sheath_dico_df['Sheath_PAR'].append(StS.PAR)
    Sheath_dico_df['Photosynthetic'].append(StS.photosynthetic)


def log_Ear(Ear_dico_df, elapsed_time, Tempcum, StE):
    Ear_dico_df["Elapsed_time"].append(elapsed_time)
    Ear_dico_df["Temp_cum"].append(Tempcum)
    Ear_dico_df["Num_plante"].append(StE.num_plante)
    Ear_dico_df["Genotype"].append(StE.geno)
    Ear_dico_df["Num_talle"].append(str(StE.tiller))
    Ear_dico_df["Ear_sumtemp"].append(StE.sumtemp)
    Ear_dico_df["Ear_length"].append(StE.length)
    Ear_dico_df["Ear_surface"].append(StE.area)
    Ear_dico_df["Emerged"].append(StE.emerged)
    Ear_dico_df["Ear_PAR"].append(StE.PAR)
    Ear_dico_df["Photosynthetic"].append(StE.photosynthetic)


def log_Internode(Internode_dico_df, elapsed_time, Tempcum, Temperature, cohort_number, StI):
    Internode_dico_df['Elapsed_time'].append(elapsed_time)
    Internode_dico_df['Temp_cum'].append(Tempcum)
    Internode_dico_df['Temperature'].append(Temperature)
    Internode_dico_df['Num_plante'].append(StI.num_plante)
    Internode_dico_df['Genotype'].append(StI.geno)
    Internode_dico_df['Num_talle'].append(str(StI.tiller))
    Internode_dico_df['Num_cohorte'].append(cohort_number(StI.tiller))
    Internode_dico_df['Num_rang'].append(StI.n)
    Internode_dico_df['Internode_length'].append(StI.length)
    Internode_dico_df['Internode_final_length'].append(StI.final_length)
    Internode_dico_df['Internode_surface'].append(StI.area)
    Internode_dico_df['Internode_PAR'].append(StI.PAR)
    Internode_dico_df['Photosynthetic'].append(StI.photosynthetic)


def log_Peduncle(Peduncle_dico_df, elapsed_time, Tempcum, Temperature, cohort_number, StP):
    Peduncle_dico_df['Elapsed_time'].append(elapsed_time)
    Peduncle_dico_df['Temp_cum'].append(Tempcum)
    Peduncle_dico_df['Temperature'].append(Temperature)
    Peduncle_dico_df['Num_plante'].append(StP.num_plante)
    Peduncle_dico_df['Genotype'].append(StP.geno)
    Peduncle_dico_df['Num_talle'].append(str(StP.tiller))
    Peduncle_dico_df['Num_cohorte'].append(cohort_number(StP.tiller))
    Peduncle_dico_df['Num_rang'].append(StP.n)
    Peduncle_dico_df['Sum_temp'].append(StP.sumtemp)
    Peduncle_dico_df['Peduncle_length'].append(StP.length)
    Peduncle_dico_df['Peduncle_final_length'].append(StP.final_length)
    Peduncle_dico_df['Peduncle_surface'].append(StP.area)
    Peduncle_dico_df['Peduncle_PAR'].append(StP.PAR)
    Peduncle_dico_df['Photosynthetic'].append(StP.photosynthetic)


def log_Peraxes(Peraxes_dico_df, initialization_Flag, num_plt, elapsed_time, DOY, Temperature,
                Tempcum, axis, Sh_max_temp, Hcol_max, Hcol_dead, delta_H, tiller_surface, axis_census, leaf_contrib,
                stem_contrib, ear_contrib, peduncle_contrib):
    Peraxes_dico_df["Elapsed_time"].append(elapsed_time)
    Peraxes_dico_df["DOY"].append(DOY)
    Peraxes_dico_df["Temperature"].append(Temperature)
    Peraxes_dico_df["Temp_cum"].append(Tempcum)
    Peraxes_dico_df["Num_plante"].append(num_plt)
    Peraxes_dico_df["Num_talle"].append(axis)
    Peraxes_dico_df["Sheath_max"].append(Sh_max_temp)
    Peraxes_dico_df["Collar_height"].append(Hcol_max[num_plt][axis])
    Peraxes_dico_df["Dead_collar_height"].append(Hcol_dead[num_plt][axis])
    Peraxes_dico_df["Delta_H"].append(delta_H[num_plt][axis])
    Peraxes_dico_df["Visible_surface"].append(tiller_surface[(num_plt, axis)])
    Peraxes_dico_df["Stop_growth_flag"].append(axis_census[num_plt][axis]['Stop_growth_flag'])
    Peraxes_dico_df["Leaf_contrib_to_GAI"].append(leaf_contrib)
    Peraxes_dico_df["Stem_contrib_to_GAI"].append(stem_contrib)
    Peraxes_dico_df["Ear_contrib_to_GAI"].append(ear_contrib)
    Peraxes_dico_df["Peduncle_contrib_to_GAI"].append(peduncle_contrib)


def log_Debug_PAR(Debug_PAR_dico_df, elapsed_time, Temperature, lstring):
    Debug_PAR_dico_df["Elapsed_time"].append(elapsed_time)
    Debug_PAR_dico_df["Temp_cum"].append(Temperature)
    Debug_PAR_dico_df["Organ_type"].append(lstring[id].name)
    Debug_PAR_dico_df["Num_talle"].append(lstring[id][0].tiller)
    Debug_PAR_dico_df["Num_plante"].append(lstring[id][0].num_plante)
    Debug_PAR_dico_df["Num_organe"].append(lstring[id][0].n)
    Debug_PAR_dico_df["Organ_surface"].append(lstring[id][0].organ_surface)
    Debug_PAR_dico_df["Organ_PAR"].append(lstring[id][0].PAR)


def log_Gai(GAI_dico_df, initialization_Flag, num, elapsed_time, Tempcum, DOY, surface_plante, surface_plante_visible,
            crop_scheme, GAI_tot, GAI_center, GAI_ind, GAI_prox):
    GAI_dico_df["Init_flag"].append(initialization_Flag[num])
    GAI_dico_df['Elapsed_time'].append(elapsed_time)
    GAI_dico_df['Temp_cum'].append(Tempcum)
    GAI_dico_df['DOY'].append(DOY)
    GAI_dico_df['Genotype'].append(0)
    GAI_dico_df['Num_plante'].append(num)
    GAI_dico_df['Surface_plante'].append(surface_plante[num])
    GAI_dico_df['Surface_visible'].append(surface_plante_visible[num])
    GAI_dico_df['Surface_sol'].append((crop_scheme["nplant_peupl"] * (
    (crop_scheme["dist_inter_rang"] * 100) * (crop_scheme["dist_intra_rang"] * 100))))
    GAI_dico_df['GAI_tot'].append(GAI_tot)
    GAI_dico_df['GAI_center'].append(GAI_center)
    GAI_dico_df['GAI_ind'].append(GAI_ind[num])
    GAI_dico_df['GAI_prox'].append(GAI_prox[num])


def log_PAR_per_axes(PAR_per_axes_dico, elapsed_time, Tempcum, num_plt, axis, current_PAR, dico_PAR_per_axis):
    PAR_per_axes_dico["Elapsed_time"].append(elapsed_time)
    PAR_per_axes_dico["Temp_cum"].append(Tempcum)
    PAR_per_axes_dico["Num_plante"].append(num_plt)
    PAR_per_axes_dico["Num_talle"].append(axis)
    PAR_per_axes_dico["Inc_PAR"].append(current_PAR)
    tt = round(Tempcum, 1)
    PAR_per_axes_dico["Sum_PAR"].append(dico_PAR_per_axis[num_plt][axis].get(tt, 0.))
