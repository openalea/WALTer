"""Leaf shape model for the geometry of leaves"""
from walter import cereals_fitting as fitting
from walter.cereals_leaf import leaf_shape_perez, sr_dornbush, leaf_mesh


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

    return sr_dornbush(nb_segment=100, klig=klig, swmax=swmax, f1=f1, f2=f2)


def walter_leaf(nb_segment=10, rank=10, rank_j=8, rank_max=10, rank_flag=11, insertion_angle=50, scurv=0.5,
                curvature=0.4):
    x, y = walter_xy(insertion_angle=insertion_angle, scurv=scurv, curvature=curvature)
    s, r = walter_sr(rank=rank, rank_j=rank_j, rank_max=rank_max, rank_flag=rank_flag)
    return fitting.fit3(x, y, s, r, nb_points=nb_segment)


def walter_leaf_mesh(leaf, final_length, max_width, visible_length, inclination):
    return leaf_mesh(leaf, L_shape=final_length, Lw_shape=max_width, length=visible_length, inclination=inclination,
                     relative=False)