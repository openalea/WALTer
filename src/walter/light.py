"""A collection of function / macros to simulate light interception with
Walter"""
from alinea.caribu.sky_tools import GenSky, GetLight
from alinea.caribu.CaribuScene import CaribuScene
from alinea.caribu.light import light_sources
from alinea.astk.sun_and_sky import sun_sources, sun_fraction, sky_irradiances, sky_sources, _timezone, _longitude, _latitude, _altitude


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


def get_turtle_light(current_PAR, sky_type='soc', turtle_sectors=46, add_sun=False, curent_date=None,
                     longitude = _longitude, latitude=_latitude, altitude=_altitude, timezone=_timezone):
    """Sun + sky source using the 46 sector turtle sky discretisation
        Args:
        current_date: a naive datetime object
        sky_type:(str) type of sky luminance model. One of :
                           'soc' (standard overcast sky),
                           'uoc' (uniform overcast sky)
                           'clear_sky' (standard clear sky)
        turtle_sectors : (int) the minimal number of sectors to be used for discretising the sky hemisphere. Turtle
        discretisation will be one of 1, 6, 16 or 46 sectors
        longitude: (float) in degrees
        latitude: (float) in degrees
        altitude: (float) in meter
        timezone:(str) the time zone
    """
    daydate = '2000-06-21'
    if curent_date is not None:
        daydate = curent_date.strftime('%Y-%m-%d')
    sun = [(), (), ()]
    f_sun = 0
    if add_sun:
        sky_irr = sky_irradiances(daydate=daydate, longitude=longitude,
                                  latitude=latitude, altitude=altitude,
                                  timezone=timezone)
        f_sun = sun_fraction(sky_irr)
        sun = sun_sources(irradiance=f_sun * current_PAR,
                          daydate=daydate, latitude=latitude, longitude=longitude,
                          altitude=altitude, timezone=timezone)
    sky = sky_sources(sky_type=sky_type, irradiance=current_PAR * (1 - f_sun), turtle_sectors=turtle_sectors,
                      daydate=daydate, longitude = longitude, latitude=latitude, altitude=altitude, timezone=timezone)
    return light_sources(*sky) + light_sources(*sun)


class CaribuRecorder(object):
    records = []

    def record(self, caribu_scene, raw, show=False):
        try:
            self.records.append(caribu_scene.run_statistics(raw, show=show))
        except AttributeError: # old caribu version (<= 7.0.3)
            pass

    def records_data(self):
        resolution, ldiag, pixel_per_cm, pixel_per_triangle, confidence = zip(*self.records)
        return dict(zip(('resolution', 'ldiag', 'pixel_per_cm', 'pixel_per_triangle', 'confidence'),
                        (resolution, ldiag, pixel_per_cm, pixel_per_triangle, confidence)))


def caribu_scene(lscene, crop_scheme, current_PAR, nb_azimuth, nb_zenith):
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
