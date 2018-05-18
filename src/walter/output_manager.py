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

    def get_global_loggers(self):
        if self.loggers is None:
            Logger()
        else:
            return self.loggers


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

    def add_ParPerAxesLog(self):
        """ Add children class in Logger if there isn't defined in the init"""
        self.loggers[ParPerAxesLog.name] = ParPerAxesLog()

    def write(self, dirname):
        """Write each logger into a file"""
        if self.loggers is not None:
            for subclass in self.loggers.values():
                subclass.write(dirname)


    def log(self, name, **kwds):
        """log each logger """
        self.get_global_loggers()
        self.loggers[name].log(**kwds)



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
        for var in self.df:
            self.df[var].append(kwargs.get(var, None))



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
        Caribu is enabled
        """
        self.fields.append(("Weakest_axis", "PAR_weakest_axis"))
        self.__init__()

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
              "Sum_PAR", "Inc_PAR", "Abs_int_PAR"]
    name = 'ParPerAxes'

    def __init__(self):
        """
        Initialize the ParPerAxes output file
        """
        super(ParPerAxesLog, self).__init__()

### --- Log