"""A collection of function / macros to simulate light interception with
Walter"""
from alinea.caribu.sky_tools import GenSky, GetLight
from alinea.caribu.CaribuScene import CaribuScene
from alinea.caribu.light import light_sources
from alinea.astk.sun_and_sky import sun_sky_sources


def scene_pattern(crop_scheme):
    xmin = crop_scheme["dist_intra_rang"] * 100. / 2
    ymin = crop_scheme["dist_inter_rang"] * 100. / 2
    xmax = xmin + crop_scheme["nb_plante_par_rang"] * crop_scheme[
        "dist_intra_rang"] * 100
    ymax = ymin + crop_scheme["nb_rang"] * crop_scheme["dist_inter_rang"] * 100
    return xmin, ymin, xmax, ymax


def get_light(current_PAR, nb_azimuth, nb_zenith):
    sky = GenSky.GenSky()(current_PAR, 'soc', nb_azimuth, nb_zenith)
    sky = GetLight.GetLight(sky)
    sky = sky.split()
    sky_tup = []

    for i in range(nb_azimuth * nb_zenith):
        sky_tup.append((float(sky[4*i]), (
        float(sky[4*i + 1]), float(sky[4*i + 2]), float(sky[4*i + 3]))))

    return sky_tup


def get_turtle_light(current_PAR):
    """Sun + sky source using the 46 sector turtle sky discretisation"""
    # parameter for soc sky (like get_light). More realistic skies can be obtained
    ghi = current_PAR
    dhi = ghi # force sun = 0
    _ , sky = sun_sky_sources(ghi, dhi, model='sun_soc')
    sun = [[],[],[]]

    return light_sources(*sun) + light_sources(*sky)


def caribu_scene(lscene, crop_scheme, light):
    """Create a caribu scene from walter lscene

    Args:
        lscene: walter scene (units: cm)
        crop_scheme:
        current_PAR: incident light (micromolPAR.m-2)
        nb_azimuth:
        nb_zenith:

    Returns:

    """
    pattern = scene_pattern(crop_scheme)
    return CaribuScene(scene=lscene, scene_unit="cm", light=light,
                       pattern=pattern)
