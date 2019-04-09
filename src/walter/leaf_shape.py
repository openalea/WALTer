"""Leaf shape model for the geometry of leaves"""
from walter import cereals_fitting as fitting
from walter.cereals_leaf import leaf_shape_perez, sr_dornbush, leaf_mesh, blade_elt_area, form_factor
from openalea.plantgl.all import SurfComputer, Discretizer, Scaling

def walter_xy(insertion_angle=50, scurv=0.5, curvature=0.4):
    """ x,y coordinates of points sampling a leaf midrib placed in a vertical plane (origin = leaf base)

    Parameters
    ----------
    insertion_angle: the angle (degree) between stem and leaf at leaf base
    scurv : the relative position on the midrib where 2/3 of total leaf curvature is achieved
    curvature : leaf angular curvature (tip angle - insertion angle) relative to curvature_max (set to 240)

    Returns
    -------
    x, y coordinates of 100 points sampling the leaf midrib
    """
    return leaf_shape_perez(nb_segment=100, insertion_angle=insertion_angle, l=scurv, curvature=curvature,
                            curvature_max=240)

def wheatI_dornbush(rank=10, rank_j=8, rank_max=10, rank_flag=11):
    """Mini model proposed by Dornbush for parameterising wheat I dataset"""
    f1 = 0.64
    f2 = 0.92
    klig = 0.6
    if rank ==1:
        f1 = 0.79
        swmax = 0.38
    elif rank == 2:
        f1 = (0.64 + 0.79) / 2
        swmax = 0.62
    elif rank <= rank_j:
        swmax = 0.62 + (0.42 - 0.62) * float(rank - 2) / (rank_j - 2)
    elif rank <= rank_max:
        swmax = 0.48
    else:
        swmax = 0.48 + (0.57 - 0.48) * float(rank - rank_max) / (rank_flag - rank_max)
    return {'klig':klig, 'swmax':swmax, 'f1':f1,'f2':f2}



def walter_sr(rank=10, rank_j=8, rank_max=10, rank_flag=11):
    """ s,r coordinate of relative leaf width (r) as a function of relative distance to leaf base (s)

    Parameters
    ----------
    rank: the rank of the leaf (counted from plant base)
    rank_j: the rank of the last juvenile leaf (rank of the first elongated internode)
    rank_max: the rank of the longest leaf
    rank_flag : the rank of flag leaf

    Returns
    -------
    s, r coordinates of 100 points sampling the leaf
    """
    # parameter of Dornbush 2010 for wheat I dataset
    return sr_dornbush(nb_segment=100, **wheatI_dornbush(rank=rank, rank_j=rank_j, rank_max=rank_max, rank_flag=rank_flag))


def walter_leaf(nb_segment=10, rank=10, rank_j=8, rank_max=10, rank_flag=11, insertion_angle=50, scurv=0.5,
                curvature=0.4):
    x, y = walter_xy(insertion_angle=insertion_angle, scurv=scurv, curvature=curvature)
    s, r = walter_sr(rank=rank, rank_j=rank_j, rank_max=rank_max, rank_flag=rank_flag)
    return fitting.fit3(x, y, s, r, nb_points=nb_segment)


def walter_leaf_mesh(leaf, final_length=1, max_width=1, visible_length=1, inclination=0, compensate=True):
    mesh = leaf_mesh(leaf, L_shape=final_length, Lw_shape=max_width, length=visible_length, inclination=inclination,
                     relative=False)
    # compensate for area error
    # TODO search where does this error come from ?
    if mesh is not None and compensate:
        area = leaf_area(leaf, length=visible_length, mature_length=final_length)
        sc = SurfComputer(Discretizer())
        mesh.apply(sc)
        scale_radius = area / sc.surface
        mesh = mesh.transform(Scaling((1, scale_radius, 1)))

    return mesh


def leaf_area(leaf , length=1, mature_length=1, width_max=1, form_factor=None):
    """
    Leaf area as a function of length
    -------

    Parameters
    ----------
    leaf: x,y,s,r coordinate describing mature leaf shape
    length: current length of the leaf
    mature_length: the length of the leaf once mature
    width_max: maximal width of the mature leaf
    form_factor: (optional) the form_factor of the mature leaf (if known), used to avoid integration

    Returns
    -------
    the area of the leaf corresponding to the distal part up to length
    """
    if length >= mature_length and form_factor is not None:
        return length * width_max * form_factor
    _,_,s,r = leaf
    sr_b = 1- float(length) / mature_length
    return blade_elt_area(s,r, mature_length, width_max, sr_base=sr_b, sr_top=1)


def mesh_area(mesh):
    if mesh:
        sc = SurfComputer(Discretizer())
        mesh.apply(sc)
        return sc.surface
    else:
        return None



