from os.path import join as pj
from openalea.lpy import Lsystem
from walter import data_access
from alinea.caribu.CaribuScene import CaribuScene

def test_caribu():
    Debug_PAR_dico_df = {"Elapsed_time": [], "Temp_cum": [], "Num_plante": [],
                         "Num_talle": [], "Organ_PAR": [], "Organ_type": [],
                         "Num_organe": [], "Organ_surface": [], "Ei": []}

    lsystem_file = pj(data_access.get_data_dir(), 'WALTer.lpy')
    lsys = Lsystem(lsystem_file,{'params': {'nb_plt_utiles': 1,
                                  'dist_border_x':0,
                                  'dist_border_y': 0,
                                  'nbj': 52,
                                  'beginning_CARIBU': 23000

         }})
    lstring = lsys.iterate()
    lscene = lsys.sceneInterpretation(lstring)

    new_lstring = lstring.replace("%", "")
    mapping_table = {}
    if lscene:
        for i in range(len(lscene)):
            mapping_table[lscene[i].id] = i
    c_scene = CaribuScene(scene=lscene, scene_unit="m")
    raw, res_sky = c_scene.run(simplify=True)
    for id in mapping_table.keys():
        # if id not in new_lstring: continue
        new_ = new_lstring[id]
        if ((new_.name == "Blade" and new_[0].photosynthetic == True) or
                (new_.name in ("Sheath", "Internode", "Peduncle")) or
                (new_.name == "Ear" and new_[0].emerged)):
            if new_[0].tiller in axis_census[new_[0].num_plante].keys():
                Debug_PAR_dico_df["Ei"].append(
                    res_sky["Ei"][mapping_table[id]])

                if res_sky["Ei"][mapping_table[id]] < 0:
                    new_[0].PAR = 0
                else:
                    new_[0].PAR = res_sky["Ei"][mapping_table[id]] * \
                                  res_sky["area"][mapping_table[id]]

                new_[0].organ_surface = res_sky["area"][mapping_table[id]]
