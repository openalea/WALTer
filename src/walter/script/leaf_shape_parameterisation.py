"""Utilities to parameterise leaves"""
import matplotlib.pyplot as plt
from walter.leaf_shape import walter_sr, walter_xy, walter_leaf


def compare_leaf_shape_2d(nb_segment=10, rank=10, rank_j=8, rank_max=10, rank_flag=11, insertion_angle=50, scurv=0.5,
                curvature=50):
    x, y = walter_xy(insertion_angle=insertion_angle, scurv=scurv, curvature=curvature)
    s, r = walter_sr(rank=rank, rank_j=rank_j, rank_max=rank_max, rank_flag=rank_flag)
    xx, yy, ss, rr = walter_leaf(nb_segment=nb_segment, rank=rank, rank_j=rank_j, rank_max=rank_max, rank_flag=rank_flag, insertion_angle=insertion_angle, scurv=scurv,
                curvature=curvature)
    fig, axs = plt.subplots(1, 2)
    axs[0].plot(x,y)
    axs[0].plot(xx, yy)
    axs[0].axis('equal')
    axs[1].plot(s, r)
    axs[1].plot(ss, rr)
    axs[1].axis('equal')
    plt.show()