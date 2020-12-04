from walter.light import scene_pattern
from alinea.caribu.CaribuScene import CaribuScene
import pandas
import numpy
from openalea.plantgl.all import Scene


def plant_position(num_plante, plant_map):
    return plant_map[num_plante]['x'], plant_map[num_plante]['y']


def plant_pattern(num_plante, crop_scheme, plant_map):
    xp, yp = plant_position(num_plante, plant_map)
    xmin = xp - crop_scheme["dist_intra_rang"] * 100. / 2
    ymin = yp - crop_scheme["dist_inter_rang"] * 100. / 2
    xmax = xp + crop_scheme["dist_intra_rang"] * 100. / 2
    ymax = yp + crop_scheme["dist_inter_rang"] * 100. / 2
    return xmin, ymin, xmax, ymax


def density_radius(crop_scheme):
    sd = 1. / crop_scheme["density"]
    return numpy.sqrt(sd / numpy.pi)


def bounding_cylinder(c_scene, center):
    xc, yc = center
    x, y, z = map(numpy.array, zip(*reduce(lambda x, y: list(x) + list(y),
                                    reduce(lambda x, y: x + y,
                                           c_scene.scene.values()))))
    rads = numpy.sqrt((x - xc)**2 + (y - yc)**2)
    return rads.max() / 100, z.max() / 100


def analyse(lscene, lstring, crop_scheme, plant_map):
    # get some meta info on modules present in the scene
    lsd = lscene.todict()
    meta = {'plant': {}, 'organ': {}}
    for id in lsd:
        meta['plant'][id] = lstring[id][0].num_plante
        meta['organ'][id] = lstring[id].name
    meta = pandas.DataFrame(meta)
    # Sp_within : projection surface of individual plants within canopy as seen from above
    # (with occlusions by other plants)
    domain = scene_pattern(crop_scheme)
    c_scene = CaribuScene(scene=lscene, scene_unit="cm", pattern=domain)
    raw, agg = c_scene.run(simplify=True, infinite=True, direct=True)
    df = pandas.concat([meta, pandas.DataFrame(agg)], axis=1)
    df = df[df.organ == 'Blade']
    df['Sp_within'] = df['Ei'] * df['area']
    res = df.groupby('plant').agg('sum').loc[:,['area', 'Sp_within']].rename(columns={'area':'S'})
    #
    # Sp_isolated : projection surface of individual plants isolated from other plants
    # Sp_selfsim : projection surface of individual plants placed in a self similar canopy
    # rd : density radius (radius of the disc whose area match plant density)
    # ri : radius of the bounding circle
    # hi = height of the bounding cylinder
    res = res.reindex(columns=res.columns.tolist() + ['Sp_isolated', 'Sp_selfsim', 'Ri', 'Hi'])
    geoms = pandas.DataFrame.from_dict(lsd, orient='index', columns=['geometry'])
    dfs = pandas.concat([meta, geoms], axis=1)
    for pid, dfp in dfs.groupby('plant'):
        sc = Scene()
        for geom in dfp['geometry']:
            sc.add(geom)
        c_scene = CaribuScene(scene=sc, scene_unit="cm")
        raw, agg = c_scene.run(simplify=True, infinite=False, direct=True)
        df = pandas.concat([dfp['organ'], pandas.DataFrame(agg)], axis=1)
        df = df[df.organ == 'Blade']
        res.loc[pid, 'Sp_isolated'] = (df['Ei'] * df['area']).sum()
        #
        domain = plant_pattern(pid, crop_scheme, plant_map)
        c_scene = CaribuScene(scene=sc, scene_unit="cm", pattern=domain)
        raw, agg = c_scene.run(simplify=True, infinite=True, direct=True)
        df = pandas.concat([dfp['organ'], pandas.DataFrame(agg)], axis=1)
        df = df[df.organ == 'Blade']
        res.loc[pid, 'Sp_selfsim'] = (df['Ei'] * df['area']).sum()
        # bounding cynlinder
        ri, hi = bounding_cylinder(c_scene, plant_position(pid, plant_map))
        res.loc[pid, 'Ri'] = ri
        res.loc[pid, 'Hi'] = hi
    res['Rd'] = density_radius(crop_scheme)
    return res