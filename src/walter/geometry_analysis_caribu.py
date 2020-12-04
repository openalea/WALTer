from walter.light import scene_pattern
from alinea.caribu.CaribuScene import CaribuScene
import pandas
from openalea.plantgl.all import Scene



def plant_pattern(num_plante, crop_scheme, plant_map):
    xp = plant_map[num_plante]['x']
    yp = plant_map[num_plante]['y']
    xmin = xp - crop_scheme["dist_intra_rang"] * 100. / 2
    ymin = yp - crop_scheme["dist_inter_rang"] * 100. / 2
    xmax = xp + crop_scheme["dist_intra_rang"] * 100. / 2
    ymax = yp + crop_scheme["dist_inter_rang"] * 100. / 2
    return xmin, ymin, xmax, ymax


def analyse(lscene, lstring, crop_scheme, plant_map):
    # Sp_within : projection surface of individual plants within canopy as seen from above
    # (with occlusions by other plants)
    domain = scene_pattern(crop_scheme)
    c_scene = CaribuScene(scene=lscene, scene_unit="cm", pattern=domain)
    raw, agg = c_scene.run(simplify=True, infinite=True, direct=True)
    df = pandas.DataFrame(agg)
    plants = {'plant': {id: m[0].num_plante for id, m in enumerate(lstring) if id in df.index and m.name == 'Blade'}}
    df = pandas.concat([df, pandas.DataFrame(plants)], axis=1)
    df['Sp_within'] = df['Ei'] * df['area']
    res = df.groupby('plant').agg('sum').loc[:,['area', 'Sp_within']].rename(columns={'area':'S'})
    # Sp_isolated : projection surface of individual plants isolated from other plants
    # Sp_selfsim : projection surface of individual plants placed in a self similar canopy
    res = res.reindex(columns=res.columns.tolist() + ['Sp_isolated', 'Sp_selfsim'])
    dfs = pandas.DataFrame.from_dict(lscene.todict(), orient='index', columns=['geometry'])
    plants = {'plant': {id: m[0].num_plante for id, m in enumerate(lstring) if id in dfs.index}}
    dfs = pandas.concat([dfs, pandas.DataFrame(plants)], axis=1)
    for pid, dfp in dfs.groupby('plant'):
        sc = Scene()
        for geom in dfp['geometry']:
            sc.add(geom)
        c_scene = CaribuScene(scene=sc, scene_unit="cm")
        raw, agg = c_scene.run(simplify=True, infinite=False, direct=True)
        #TODO : filter Leaves before aggregating
        df = pandas.DataFrame(agg)
        res.loc[pid, 'Sp_isolated'] = (df['Ei'] * df['area']).sum()
        domain = plant_pattern(pid, crop_scheme, plant_map)
        c_scene = CaribuScene(scene=sc, scene_unit="cm", pattern=domain)
        raw, agg = c_scene.run(simplify=True, infinite=True, direct=True)
        # TODO : filter Leaves before aggregating
        df = pandas.DataFrame(agg)
        res.loc[pid, 'Sp_selfsim'] = (df['Ei'] * df['area']).sum()
    return res