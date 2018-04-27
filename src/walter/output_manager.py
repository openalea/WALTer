"""
this is output_manager.
"""
### Importation de libraries
from __future__ import division
from openalea.plantgl.all import *
import pandas as pd
from math import pi
import os

pj = os.path.join
data_dir = os.getcwd()
input_dir = pj(data_dir, 'input')
out_dir = pj(data_dir, "output")
ID = "output_debug"
folder_name = ID

which_output_files = pd.read_csv(pj(data_dir, "which_output_files.csv"), sep="\t")
write_output_file = {"GAI": which_output_files.GAIp[0], "Peraxes": which_output_files.Peraxes[0],
                     "Proba": which_output_files.Proba[0], "Apex_Sirius": which_output_files.Apex_sirius[0],
                     "Apex": which_output_files.Apex[0], "Apex_R": which_output_files.Apex_R[0],
                     "Blade": which_output_files.Blade[0], "Internode": which_output_files.Internode[0],
                     "Sheath": which_output_files.Sheath[0], "Ear": which_output_files.Ear[0],
                     "Peduncle": which_output_files.Peduncle[0], "PAR_per_axes": which_output_files.PAR_per_axes[0],
                     "Lstring": which_output_files.Lstring[0], "Lscene": which_output_files.Lscene[0]}
print "ce qu'on ecrit:", write_output_file["Lscene"]


### --- Initialisation --- ###

# initialise all the variables at the same time.
def init_all(GAI_dico_df, Apex_Sirius_dico_df, Apex_dico_df, Apex_R_dico_df, Blade_dico_df,
             Internode_dico_df, Peduncle_dico_df, Sheath_dico_df, Ear_dico_df, Proba_dico_df, Peraxes_dico_df,
             Debug_dico_df, PAR_per_axes_dico):
    init_output_Gai(GAI_dico_df)
    init_output_Apex_Sirius(Apex_Sirius_dico_df)
    init_output_Apex(Apex_dico_df)
    init_output_Apex_R(Apex_R_dico_df)
    init_output_Blade(Blade_dico_df)
    init_output_Internode(Internode_dico_df)
    init_output_Peduncle(Peduncle_dico_df)
    init_output_Sheath(Sheath_dico_df)
    init_output_Ear(Ear_dico_df)
    init_output_Proba(Proba_dico_df)
    init_output_Peraxes(Peraxes_dico_df)
    init_output_Debug(Debug_dico_df)
    init_output_PAR_per_axes(PAR_per_axes_dico)


def init_output_Gai(GAI_dico_df):
    GAI_dico_df = {"Init_flag": [], "Elapsed_time": [], "Temp_cum": [],
                   "DOY": [], "Genotype": [], "Num_plante": [],
                   "Surface_plante": [], "Surface_visible": [],
                   "Surface_sol": [], "GAI_tot": [], "GAI_center": [],
                   "GAI_ind": [], "GAI_prox": [], "Position": []}


def init_output_Apex_Sirius(Apex_Sirius_dico_df):
    Apex_Sirius_dico_df = {"Elapsed_time": [], "Temperature": [],
                           "Temp_cum": [], "Daylength": [], "Num_plante": [],
                           "Genotype": [], "PN": [], "LN": [], "Sumtemp": [],
                           "Vern_rate": [], "Vern_prog": [], "Vern_flag": [],
                           "Debut_ppd_flag": [], "Fin_ppd_flag": [],
                           "Ln_pot": [], "Var_L_min": [], "Ln_app": [],
                           "Ln_final": []}


def init_output_Apex(Apex_dico_df):
    Apex_dico_df = {"Elapsed_time": [], "Temperature": [], "Temp_cum": [],
                    "Time_count": [], "Sum_temp": [], "Current_PAR": [],
                    "Num_plante": [], "Genotype": [], "Num_talle": [],
                    "Num_cohorte": [], "Nb_phyto_emi": [],
                    "Nb_emerged_leaf": [], "Transiflo_flag": [],
                    "STOP_init_flag": [], "Transiflo_DOY": [], "Ln_final": []}


def init_output_Apex_R(Apex_R_dico_df):
    Apex_R_dico_df = {"Elapsed_time": [], "DOY": [], "Temperature": [],
                      "Temp_cum": [], "Sum_temp": [], "Num_plante": [],
                      "Genotype": [], "Num_cohorte": [], "Ln_final": [],
                      "Num_talle": [], "Date_epiaison": [], "Epi_DOY": [],
                      "Date_de_flo": [], "Mont_flag": [], "Mont_DOY": [],
                      "Flo_flag": [], "Flo_DOY": [], "Death_flag": [],
                      "Date_de_maturite": [], "Mat_DOY": []}


def init_output_Blade(Blade_dico_df):
    Blade_dico_df = {"Elapsed_time": [], "Temp_cum": [], "Temperature": [], "Num_plante": [], "Genotype": [],
                     "Num_talle": [], "Num_cohorte": [], "Num_rang": [], "Blade_sumtemp": [], "Blade_width": [],
                     "Blade_length": [], "Blade_visible_length": [], "Blade_final_length": [],
                     "Blade_visible_surface": [], "Blade_surface": [], "Blade_PAR": [], "Senesc_flag": [],
                     "Photosynthetic": []}


def init_output_Internode(Internode_dico_df):
    Internode_dico_df = {"Elapsed_time": [], "Temp_cum": [], "Temperature": [],
                         "Num_plante": [], "Genotype": [], "Num_talle": [],
                         "Num_cohorte": [], "Num_rang": [],
                         "Internode_length": [], "Internode_final_length": [],
                         "Internode_surface": [], "Internode_PAR": [],
                         "Photosynthetic": []}


def init_output_Peduncle(Peduncle_dico_df):
    Peduncle_dico_df = {"Elapsed_time": [], "Temp_cum": [], "Temperature": [],
                        "Num_plante": [], "Genotype": [], "Num_talle": [],
                        "Num_cohorte": [], "Num_rang": [], "Sum_temp": [],
                        "Peduncle_length": [], "Peduncle_final_length": [],
                        "Peduncle_surface": [], "Peduncle_PAR": [],
                        "Photosynthetic": []}


def init_output_Sheath(Sheath_dico_df):
    Sheath_dico_df = {"Elapsed_time": [], "Temp_cum": [], "Temperature": [],
                      "Num_plante": [], "Genotype": [], "Num_talle": [],
                      "Num_cohorte": [], "Num_rang": [], "Sheath_sumtemp": [],
                      "Sheath_diameter": [], "Sheath_length": [],
                      "Sheath_final_length": [], "Sheath_surface": [],
                      "Sheath_PAR": [], "Photosynthetic": []}


def init_output_Ear(Ear_dico_df):
    Ear_dico_df = {"Elapsed_time": [], "Temp_cum": [], "Num_plante": [],
                   "Genotype": [], "Num_talle": [], "Ear_sumtemp": [],
                   "Ear_length": [], "Ear_surface": [], "Ear_PAR": [],
                   "Photosynthetic": [], "Emerged": []}


def init_output_Proba(Proba_dico_df):
    Proba_dico_df = {"Elapsed_time": [], "Temperature": [], "Temp_cum": [],
                     "Num_plante": [], "Genotype": [], "Num_talle": [],
                     "Num_rang": [], "Sumtemp": [], "GAI_prox": [],
                     "P_debourr": []}


def init_output_Peraxes(Peraxes_dico_df):
    Peraxes_dico_df = {"Init_flag": [], "Elapsed_time": [], "DOY": [],
                       "Temperature": [], "Temp_cum": [], "Num_plante": [],
                       "Num_talle": [], "Sheath_max": [], "Collar_height": [],
                       "Dead_collar_height": [], "Delta_H": [],
                       "Visible_leaves_surface": [], "Visible_surface": [],
                       "Stop_growth_flag": [], "Leaf_contrib_to_GAI": [],
                       "Stem_contrib_to_GAI": [], "Ear_contrib_to_GAI": [],
                       "Peduncle_contrib_to_GAI": []}


def init_output_Debug(Debug_PAR_dico_df):
    Debug_PAR_dico_df = {"Elapsed_time": [], "Temp_cum": [], "Num_plante": [],
                         "Num_talle": [], "Organ_PAR": [], "Organ_type": [],
                         "Num_organe": [], "Organ_surface": [], "Ei": []}


def init_output_PAR_per_axes(PAR_per_axes_dico):
    PAR_per_axes_dico = {"Elapsed_time": [], "Temp_cum": [], "Num_plante": [],
                         "Num_talle": [], "Sum_PAR": [], "Inc_PAR": []}


### --- Writers --- ###

def write_output_Gai(GAI_dico_df):
    _GAI_df = pd.DataFrame(GAI_dico_df)
    dF_labels = ["Init_flag", "Elapsed_time", "Temp_cum", "DOY", "Genotype",
                 "Num_plante", "Surface_plante", "Surface_visible",
                 "Surface_sol", "GAI_tot", "GAI_center", "GAI_ind", "GAI_prox",
                 "Position", "Weakest_axis", "PAR_weakest_axis"]
    GAI_df = _GAI_df.reindex_axis(dF_labels, axis="columns", copy=False)
    GAI_df.to_csv(pj(out_dir, folder_name, "GAI.csv"), sep="\t", header=True,
                  index=False)


def write_output_Apex_Sirius(Apex_Sirius_dico_df):
    _Apex_Sirius_df = pd.DataFrame(Apex_Sirius_dico_df)
    dF_labels = ["Elapsed_time", "Temperature", "Temp_cum", "Daylength",
                 "Num_plante", "Genotype", "PN", "LN", "Sumtemp",
                 "Vern_rate", "Vern_prog", "Vern_flag", "Debut_ppd_flag",
                 "Fin_ppd_flag", "Ln_pot", "Var_L_min", "Ln_app",
                 "Ln_final"]
    Apex_Sirius_df = _Apex_Sirius_df.reindex_axis(dF_labels, axis="columns", copy=False)
    Apex_Sirius_df.to_csv(pj(out_dir, folder_name, "Apex_Sirius.csv"), sep="\t", header=True, index=False)


def write_output_Apex(Apex_dico_df):
    _Apex_df = pd.DataFrame(Apex_dico_df)
    dF_labels = ["Elapsed_time", "Temperature", "Temp_cum", "Time_count", "Sum_temp", "Current_PAR", "Num_plante",
                 "Genotype", "Num_talle", "Num_cohorte", "Nb_phyto_emi", "Nb_emerged_leaf", "Transiflo_flag",
                 "STOP_init_flag", "Transiflo_DOY", "Ln_final"]
    Apex_df = _Apex_df.reindex_axis(dF_labels, axis="columns", copy=False)
    Apex_df.to_csv(pj(out_dir, folder_name, "Apex.csv"), sep="\t", header=True, index=False)


def write_output_Apex_R(Apex_R_dico_df):
    _Apex_R_df = pd.DataFrame(Apex_R_dico_df)
    dF_labels = ["Elapsed_time", "DOY", "Temperature", "Temp_cum", "Sum_temp", "Num_plante", "Genotype", "Num_talle",
                 "Num_cohorte", "Ln_final", "Date_epiaison", "Epi_DOY", "Date_de_flo", "Mont_flag", "Mont_DOY",
                 "Flo_flag", "Flo_DOY", "Death_flag", "Date_de_maturite", "Mat_DOY"]
    Apex_R_df = _Apex_R_df.reindex_axis(dF_labels, axis="columns", copy=False)
    Apex_R_df.to_csv(pj(out_dir, folder_name, "Apex_R.csv"), sep="\t", header=True, index=False)


def write_output_Blade(Blade_dico_df):
    _Blade_df = pd.DataFrame(Blade_dico_df)
    dF_labels = ["Elapsed_time", "Temp_cum", "Temperature", "Num_plante", "Genotype", "Num_talle", "Num_cohorte",
                 "Num_rang", "Blade_sumtemp", "Blade_width", "Blade_length", "Blade_visible_length",
                 "Blade_final_length", "Blade_visible_surface", "Blade_surface", "Blade_PAR", "Senesc_flag",
                 "Photosynthetic"]
    Blade_df = _Blade_df.reindex_axis(dF_labels, axis="columns", copy=False)
    Blade_df.to_csv(pj(out_dir, folder_name, "Blade.csv"), sep="\t", header=True, index=False)


def write_output_Internode(Internode_dico_df):
    _Internode_df = pd.DataFrame(Internode_dico_df)
    dF_labels = ["Elapsed_time", "Temp_cum", "Temperature", "Num_plante", "Genotype", "Num_talle", "Num_cohorte",
                 "Num_rang", "Internode_length", "Internode_final_length", "Internode_surface", "Internode_PAR",
                 "Photosynthetic"]
    Internode_df = _Internode_df.reindex_axis(dF_labels, axis="columns", copy=False)
    Internode_df.to_csv(pj(out_dir, folder_name, "Internode.csv"), sep="\t", header=True, index=False)


def write_output_Peduncle(Peduncle_dico_df):
    _Peduncle_df = pd.DataFrame(Peduncle_dico_df)
    dF_labels = ["Elapsed_time", "Temp_cum", "Temperature", "Num_plante", "Genotype", "Num_talle", "Num_cohorte",
                 "Num_rang", "Sum_temp", "Peduncle_length", "Peduncle_final_length", "Peduncle_surface", "Peduncle_PAR",
                 "Photosynthetic"]
    Peduncle_df = _Peduncle_df.reindex_axis(dF_labels, axis="columns", copy=False)
    Peduncle_df.to_csv(pj(out_dir, folder_name, "Peduncle.csv"), sep="\t", header=True, index=False)


def write_output_Sheath(Sheath_dico_df):
    _Sheath_df = pd.DataFrame(Sheath_dico_df)
    dF_labels = ["Elapsed_time", "Temp_cum", "Temperature", "Num_plante", "Genotype", "Num_talle", "Num_cohorte",
                 "Num_rang", "Sheath_sumtemp", "Sheath_diameter", "Sheath_length", "Sheath_final_length",
                 "Sheath_surface", "Sheath_PAR", "Photosynthetic"]
    Sheath_df = _Sheath_df.reindex_axis(dF_labels, axis="columns", copy=False)
    Sheath_df.to_csv(pj(out_dir, folder_name, "Sheath.csv"), sep="\t", header=True, index=False)


def write_output_Ear(Ear_dico_df):
    _Ear_df = pd.DataFrame(Ear_dico_df)
    dF_labels = ["Elapsed_time", "Temp_cum", "Num_plante", "Genotype", "Num_talle", "Ear_sumtemp", "Ear_length",
                 "Ear_surface", "Ear_PAR", "Photosynthetic", "Emerged"]
    Ear_df = _Ear_df.reindex_axis(dF_labels, axis="columns", copy=False)
    Ear_df.to_csv(pj(out_dir, folder_name, "Ear.csv"), sep="\t", header=True, index=False)


def write_output_Proba(Proba_dico_df):
    _Proba_df = pd.DataFrame(Proba_dico_df)
    dF_labels = ["Elapsed_time", "Temperature", "Temp_cum", "Num_plante", "Genotype", "Num_talle", "Num_rang",
                 "Sumtemp", "GAI_prox", "P_debourr"]
    Proba_df = _Proba_df.reindex_axis(dF_labels, axis="columns", copy=False)
    Proba_df.to_csv(pj(out_dir, folder_name, "Probabilities.csv"), sep="\t", header=True, index=False)


def write_output_Peraxes(Peraxes_dico_df):
    _Peraxes_df = pd.DataFrame(Peraxes_dico_df)
    dF_labels = ["Init_flag", "Elapsed_time", "DOY", "Temperature", "Temp_cum", "Num_plante", "Num_talle", "Sheath_max",
                 "Collar_height", "Dead_collar_height", "Delta_H", "Visible_leaves_surface", "Visible_surface",
                 "Leaf_contrib_to_GAI", "Stem_contrib_to_GAI", "Ear_contrib_to_GAI", "Peduncle_contrib_to_GAI",
                 "Stop_growth_flag"]
    Peraxes_df = _Peraxes_df.reindex_axis(dF_labels, axis="columns", copy=False)
    Peraxes_df.to_csv(pj(out_dir, folder_name, "Peraxes.csv"), sep="\t", header=True, index=False)


def write_debug_PAR(Debug_PAR_dico_df):
    Debug_PAR_df = pd.DataFrame(Debug_PAR_dico_df)
    Debug_PAR_df.to_csv(pj(out_dir, folder_name, "Debug_PAR.csv"), sep="\t", header=True, index=False)


def write_output_PAR_per_axes(PAR_per_axes_dico):
    PAR_per_axes_df = pd.DataFrame(PAR_per_axes_dico)
    PAR_per_axes_df.to_csv(pj(out_dir, folder_name, "PAR_per_axes.csv"), sep="\t", header=True, index=False)


### --- Log --- ###

def log_Apex_Sirius(Apex_Sirius_dico_df, day, current_temperature, _Tempcum, duree_du_jour, latitude, DOY, StA):
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
