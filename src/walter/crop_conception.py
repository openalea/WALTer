"""compute crop_schemes for different configurations"""
from __future__ import division
from builtins import range
from math import floor, ceil, sqrt


def design_crop_classical(nb_plt_temp=1, nb_rang=1, densite=150, dist_inter_rang = 0.135):
    crop_scheme = {"dist_inter_rang": dist_inter_rang, "density": densite}
    area = nb_plt_temp / crop_scheme["density"]
    dy = nb_rang * dist_inter_rang
    dx = area / dy
    nb_plante_par_rang = int(nb_plt_temp / nb_rang)
    dist_intra = dx / nb_plante_par_rang
    nplant_peupl = int(nb_rang * nb_plante_par_rang)
    crop_scheme["nplant_peupl"] = nplant_peupl
    crop_scheme["dx"] = dx
    crop_scheme["dy"] = dy
    crop_scheme["surface_sol"] = dx * dy
    crop_scheme["nb_rang"] = nb_rang
    crop_scheme["nb_plante_par_rang"] = nb_plante_par_rang
    crop_scheme["dist_intra_rang"] = dist_intra
    crop_scheme["real_density"] = nplant_peupl / crop_scheme["surface_sol"]
    return crop_scheme


def design_crop_mesh_for_nplants(densite=150, nb_plt_utiles=1, dist_border_x=0, dist_border_y=0):
    crop_scheme = {"density": densite}
    nb_rang_utiles = floor(sqrt(nb_plt_utiles))
    nb_plant_par_rang_utiles = ceil(sqrt(nb_plt_utiles))
    d_intra = sqrt(1./densite)
    d_inter = d_intra
    # choosing dist_border > 0 triggers creation of a border
    nb_rang = nb_rang_utiles + 2 * ceil(dist_border_x / d_inter)
    nb_plant_par_rang = nb_plant_par_rang_utiles + 2 * ceil(dist_border_y / d_intra)
    dy = nb_rang*d_inter
    dx = nb_plant_par_rang*d_intra
    nplant_peupl = nb_rang*nb_plant_par_rang
    crop_scheme["area"] = dx*dy
    crop_scheme["nb_rang"] = int(nb_rang)
    crop_scheme["nb_plante_par_rang"] = int(nb_plant_par_rang)
    crop_scheme["dist_inter_rang"] = d_intra
    crop_scheme["dist_intra_rang"] = d_intra
    crop_scheme["dx"] = dx
    crop_scheme["dy"] = dy
    crop_scheme["nplant_peupl"] = int(nplant_peupl)
    crop_scheme["real_density"] = nplant_peupl/crop_scheme["area"]
    crop_scheme["surface_sol"] = dx*dy
    return crop_scheme


def adapting_crop_area(density=150, area_min=1, area_max=13, dist_inter=0.135, opt_plt_nb=10):
    crop_scheme = {"dist_inter_rang": dist_inter, "density": density}
    #print "density : ",density, "opt : ",opt_plt_nb, "area_max", area_max
    if density < (opt_plt_nb/area_max):
        area_temp = area_max
        plt_nb_temp = density*area_temp
    #elif (opt_plt_nb/area_max) < density < 55:
    #  area_temp = (50/density)
    #  plt_nb_temp = density*area_temp
    elif density > (opt_plt_nb/area_min):
        area_temp = area_min
        plt_nb_temp = density*area_temp
    else:
        #a = (area_max - area_min)/((opt_plt_nb/area_max) - (opt_plt_nb/area_min))
        #b = area_min - a*(opt_plt_nb/area_min)
        #area = a * density + b
        area_temp = (opt_plt_nb/density)
        plt_nb_temp = density*area_temp
    nb_rang = int(ceil(sqrt(area_temp)/dist_inter))
    dy = nb_rang * dist_inter
    dx = (area_temp/dy)
    nb_plante_par_rang = int(plt_nb_temp/nb_rang)
    dist_intra = dx/nb_plante_par_rang
    nplant_peupl = int(nb_rang*nb_plante_par_rang)
    crop_scheme["dx"] = dx
    crop_scheme["dy"] = dy
    crop_scheme["surface_sol"] = dx*dy
    crop_scheme["nb_rang"] = nb_rang
    crop_scheme["nb_plante_par_rang"] = nb_plante_par_rang
    crop_scheme["dist_intra_rang"] = dist_intra
    crop_scheme["nplant_peupl"] = nplant_peupl
    crop_scheme["real_density"] = nplant_peupl/crop_scheme["surface_sol"]
    return crop_scheme


def design_crop_Darwinkel(area=1, density=150):
    crop_scheme = {"area": area, "density": density}
    nb_rang = floor(sqrt(area * density))
    nb_plant_par_rang = ceil(sqrt(area * density))
    d_intra = sqrt(area/(nb_rang*nb_plant_par_rang))
    dy = nb_rang*d_intra
    dx = nb_plant_par_rang*d_intra
    nplant_peupl = nb_rang*nb_plant_par_rang
    crop_scheme["nb_rang"] = int(nb_rang)
    crop_scheme["nb_plante_par_rang"] = int(nb_plant_par_rang)
    crop_scheme["dist_inter_rang"] = d_intra
    crop_scheme["dist_intra_rang"] = d_intra
    crop_scheme["dx"] = dx
    crop_scheme["dy"] = dy
    crop_scheme["nplant_peupl"] = int(nplant_peupl)
    crop_scheme["real_density"] = nplant_peupl/area
    crop_scheme["surface_sol"] = dx*dy
    return crop_scheme


# Geographical disposition of all plants on the soil (Sowing)
def plant_disposition(crop_scheme, center_plants=True):
    nb_rang, nb_plante_par_rang, dist_inter_rang, dist_intra_rang = crop_scheme["nb_rang"], crop_scheme[
        "nb_plante_par_rang"], crop_scheme["dist_inter_rang"], crop_scheme["dist_intra_rang"]
    xmid, ymid = 0, 0
    if center_plants:
        xmid = (nb_plante_par_rang - 1) * dist_intra_rang * 100 / 2
        ymid = (nb_rang - 1) * dist_inter_rang * 100 / 2
    maillage = []
    plant_map = {}
    num_plante = 0
    for rang in range(int(nb_rang)):
        y = dist_inter_rang * rang * 100
        prov = []
        for plant_par_rang in range(int(nb_plante_par_rang)):
            x = dist_intra_rang * plant_par_rang * 100
            num_plante += 1
            plant_map[num_plante] = {"x": x - xmid, "y": y - ymid}
            prov.append(num_plante)
        maillage.append(prov)
    return maillage, plant_map


def domain(crop_scheme):
    """return extreme points (cm) of 2D domain of a walter centered plot"""
    xmin = -(crop_scheme["dx"] * 100) / 2
    xmax = (crop_scheme["dx"] * 100) / 2
    ymin = -(crop_scheme["dy"] * 100) / 2
    ymax = (crop_scheme["dy"] * 100) / 2
    return xmin, ymin, xmax, ymax


def central_domain(crop_scheme, dist_border_x=0, dist_border_y=0):
    """return extreme points (cm) of 2D central domain of a walter centered plot"""
    xmin, ymin, xmax, ymax = domain(crop_scheme)
    d_intra, d_inter = crop_scheme["dist_intra_rang"], crop_scheme["dist_inter_rang"]
    # reproduce the same rule as design_crop_mesh_for_nplants
    dbx = d_intra * ceil(dist_border_x / d_intra)
    dby = d_inter * ceil(dist_border_y / d_inter)
    xmin_center = xmin + dbx * 100
    xmax_center = xmax - dbx * 100
    ymin_center = ymin + dby * 100
    ymax_center = ymax - dby * 100
    return xmin_center, ymin_center, xmax_center, ymax_center


def central_and_border_plants(crop_scheme, dist_border_x, dist_border_y):
    """create list of plants within and outside central domain.
    In the case all plants are border plants they are also all considered as central plants"""
    plant_census = list(range(1, crop_scheme["nplant_peupl"] + 1))
    border_plants = []
    xmin_center, ymin_center, xmax_center, ymax_center = central_domain(crop_scheme, dist_border_x=dist_border_x, dist_border_y=dist_border_y)
    _, positions = plant_disposition(crop_scheme, center_plants=True)
    for num_plante in plant_census:
        # Determining which plant is in the border, which plant is not
        if positions[num_plante]["x"] <= xmin_center or positions[num_plante]["x"] >= xmax_center:
            border_plants.append(num_plante)
        if num_plante not in border_plants:
            if positions[num_plante]["y"] <= ymin_center or positions[num_plante]["y"] >= ymax_center:
                border_plants.append(num_plante)
    if border_plants != plant_census:
        for brd_plt in border_plants:
            plant_census.remove(brd_plt)
    return plant_census, border_plants


def set_neighbour(maillage, crop_scheme, radius=1, toric="True"):
    # TODO prendre en compte l'alea de positionnement des graines dans la determination des voisins dune plante cible
    d_intra, d_inter = crop_scheme["dist_intra_rang"], crop_scheme["dist_inter_rang"]
    nb_rang, nb_plante_par_rang = crop_scheme["nb_rang"], crop_scheme["nb_plante_par_rang"]
    nb_voisins_glob = {}
    dico_voisins = {}
    voisins = []
    neighbour_indexes = []
    ncol = int(round(2 * radius / d_inter)) + 1
    nrow = int(round(2 * radius / d_intra)) + 1
    for j in range(ncol):
        for i in range(nrow):
            delta_j = j - int(round(radius / d_inter))
            delta_i = i - int(round(radius / d_intra))
            d_to_cible = sqrt((delta_j * d_inter) ** 2 + (delta_i * d_intra) ** 2)
            if d_to_cible <= radius:
                neighbour_indexes.append((delta_j, delta_i))
    nb_voisins_glob[0] = len(neighbour_indexes)
    #####
    for num_col in range(nb_rang):
        for num_ligne in range(nb_plante_par_rang):
            plante_cible = maillage[num_col][num_ligne]
            for (deltaj, deltai) in neighbour_indexes:
                if toric == "True":
                    voisins.append(maillage[(num_col + deltaj) % nb_rang][(num_ligne + deltai) % nb_plante_par_rang])
                else:
                    if (0 <= num_col + deltaj < nb_rang) and (0 <= num_ligne + deltai < nb_plante_par_rang):
                        voisins.append(maillage[(num_col + deltaj)][(num_ligne + deltai)])
            dico_voisins[plante_cible] = voisins
            voisins = []

    return nb_voisins_glob, dico_voisins


# not used yet : common frontend to crop design functions
def crop_conception(crop_ccptn='Mesh_for_n_plants', densite=150, nb_rang=1,
                    dist_inter_rang=.135, nb_plt_utiles=1, dist_border_x=0.,
                    dist_border_y=0, area_targeted=1, area_min=1, area_max=13,
                    opt_plt_nb=10, nb_plt_temp=1):
    if crop_ccptn == 'classical':
        crop_scheme = design_crop_classical(nb_plt_temp, nb_rang, densite,
                                            dist_inter_rang)
    elif crop_ccptn == 'Mesh_for_nplants':
        crop_scheme = design_crop_mesh_for_nplants(densite, nb_plt_utiles,
                                                   dist_border_x, dist_border_y)
    elif crop_ccptn == 'Darwinkel_original':
        crop_scheme = design_crop_Darwinkel(area_targeted, densite)
    elif crop_ccptn == 'neo_Darwinkel':
        crop_scheme = adapting_crop_area(densite, area_min, area_max,
                                         dist_inter_rang, opt_plt_nb)
    else:
        raise ValueError('unknown crop_ccptn: ' + crop_ccptn)
    return crop_scheme


#def crop_conception2(densite, dx, dy, dist_inter_rang, area_max):
#  if dx*dy > area_max:
#    print "ATTENTION LES DIMENSIONS DE LA PARCELLE SONT TROP GRANDES!"
#    dx, dy = sqrt(area_max)-0.01, sqrt(area_max)-0.01
#  nb_rang_m2 = 1/dist_inter_rang
#  nb_plante_par_rang_m2 = densite/nb_rang_m2
#  crop_scheme["nb_rang"] = int(floor(dx*nb_rang_m2))
#  crop_scheme["nb_plante_par_rang"] = int(floor(dy*nb_plante_par_rang_m2))
#  crop_scheme["dist_intra_rang"] = dy/crop_scheme["nb_plante_par_rang"]
#  crop_scheme["nplant_peupl"] = crop_scheme["nb_plante_par_rang"]*crop_scheme["nb_rang"]
#  print crop_scheme
#  return crop_scheme

# def crop_conception(densite, nb_rang, dist_inter_rang, nb_plante_min,
#                     nb_plante_max):
#     crop_scheme = {"dist_inter_rang": dist_inter_rang, "density": densite}
#     crop_scheme["nb_rang"] = int(nb_rang)
#     dx = nb_rang * dist_inter_rang
#     nb_rang_m2 = 1 / dist_inter_rang
#     nb_plante_par_rang_m2 = densite / nb_rang_m2
#     dist_intra_rang = 1 / nb_plante_par_rang_m2
#     nb_plt_p_rang_min = nb_plante_min / nb_rang
#     nb_plt_p_rang_max = nb_plante_max / nb_rang
#     crop_scheme["dx"], crop_scheme["dist_intra_rang"] = dx, dist_intra_rang
#     resultats = {}
#     if nb_plante_min == nb_plante_max == 1:
#         nb_plante_par_rang = 1
#         nb_rang = 1
#         dx, dy = dist_inter_rang, 1 / nb_plante_par_rang_m2
#         nplant_peupl = 1
#         crop_scheme["dy"] = dy
#         crop_scheme["nb_plante_par_rang"], crop_scheme["nplant_peupl"] = int(
#             nb_plante_par_rang), int(nplant_peupl)
#     else:
#         if round(nb_plt_p_rang_max * dist_intra_rang, 2) - round(
#                         nb_plt_p_rang_min * dist_intra_rang, 2) < 0.01:
#             dy = round(nb_plt_p_rang_min * dist_intra_rang, 2)
#             nb_plante_par_rang = floor(dy * nb_plante_par_rang_m2)
#             nplant_peupl = nb_rang * nb_plante_par_rang
#             surface_sol = dx * dy
#             virtual_density = nplant_peupl / surface_sol
#             ecart_de_densite = abs(densite - virtual_density) / densite
#             resultats[ecart_de_densite] = (dx, dy)
#             crop_scheme["nb_plante_par_rang"], crop_scheme[
#                 "nplant_peupl"] = int(nb_plante_par_rang), int(nplant_peupl)
#         else:
#             for dy in np.arange(round(nb_plt_p_rang_min * dist_intra_rang, 2),
#                                 round(nb_plt_p_rang_max * dist_intra_rang, 2),
#                                 0.01):
#                 nb_plante_par_rang = floor(dy * nb_plante_par_rang_m2)
#                 nplant_peupl = nb_rang * nb_plante_par_rang
#                 surface_sol = dx * dy
#                 virtual_density = nplant_peupl / surface_sol
#                 ecart_de_densite = abs(densite - virtual_density) / densite
#                 resultats[ecart_de_densite] = (round(dx, 2), round(dy, 2))
#             dy = round(resultats[min(resultats.keys())][1], 2)
#             nb_plante_par_rang = floor(dy * nb_plante_par_rang_m2)
#             nplant_peupl = nb_rang * nb_plante_par_rang
#             crop_scheme["nb_plante_par_rang"], crop_scheme[
#                 "nplant_peupl"] = int(nb_plante_par_rang), int(nplant_peupl)
#         crop_scheme["dy"] = dy
#         if min(resultats.keys()) * 100 > 5:
#             print "ATTENTION ERREUR CONSEQUENTE DE PREDICTION DE LA DENSITE"
#     crop_scheme["surface_sol"] = dx * dy
#     crop_scheme["map_middle_y"] = ((crop_scheme["nb_rang"] * (
#     crop_scheme["dist_inter_rang"]) * 100) + (
#                                    crop_scheme["dist_inter_rang"]) * 100) / 2
#     crop_scheme["map_middle_x"] = ((crop_scheme["nb_plante_par_rang"] * (
#     crop_scheme["dist_intra_rang"]) * 100) + (
#                                    crop_scheme["dist_intra_rang"]) * 100) / 2
#     return crop_scheme
