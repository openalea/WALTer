from __future__ import division
from builtins import map
from past.utils import old_div
from walter.leaf_shape import walter_sr, walter_xy, walter_leaf, leaf_area, walter_leaf_mesh, mesh_area
from walter.cereals_leaf import blade_elt_area, form_factor
from walter.cereals_fitting import fit2, simplify, leaf_to_mesh_2d, plantgl_shape
from nose.tools import assert_almost_equal
from numpy.testing import assert_allclose
from numpy import array


def test_walter_sr():
    s,r = walter_sr()


def test_leaf_area():
    x, y, s, r = walter_leaf()
    stot = blade_elt_area(s,r)
    st = blade_elt_area(s, r, sr_base=0.5)
    sb = blade_elt_area(s, r, sr_top=0.5)
    assert sb > st
    assert_almost_equal(sb+st, stot, 2)


def test_positive_area():
    # fitting.fit2 should not return negative radius
    x,y = walter_xy(insertion_angle=50, scurv=0.5, curvature=0.4)
    s,r = walter_sr(rank=8, rank_j=8, rank_max=10, rank_flag=11)
    (xx, yy, ss, rr), area = fit2(x,y,s,r)
    assert all(rr >= 0)
    leaf = (xx, yy, ss, rr)
    # simplify should return s with same max
    sx, sy, sis, sr = simplify(leaf, 10)
    assert max(ss) == max(sis)

def test_nb_segment():
    leaf_ref = walter_leaf(nb_segment=100)
    ffref = form_factor(leaf_ref)
    nseg = (2,5,10,20)
    leaves = list(map(walter_leaf,nseg))
    ff = list(map(form_factor, leaves))
    rel_err = old_div(abs(array(ff) - ffref), ffref)
    max_err = array([1e-6]*len(nseg))
    assert all(rel_err < max_err)


def test_area_vs_area_mesh():
    # TODO check why meash area is not compensated by cereals.fitting

    # a 100 points described leaf
    s, r = walter_sr(rank=2, rank_j=8, rank_max=10, rank_flag=11)
    leaf = walter_leaf()
    area_ref = leaf_area((s,r,s,r))
    area = leaf_area(leaf)
    assert_almost_equal(area, area_ref, 2)
    # formula using ff
    ff = form_factor(leaf)
    areaff = leaf_area(leaf, form_factor=ff)
    assert_almost_equal(area, areaff, 2)

    # compare with mesh
    # about 1 percent difference between area and meash area (caribu) if compensate=False: to be tested for rank2
    mesh = walter_leaf_mesh(leaf)
    marea = mesh_area(mesh)
    assert_almost_equal(area, marea)

    #test scaling
    mesh = walter_leaf_mesh(leaf,10,1,10)
    marea = mesh_area(mesh)
    assert_almost_equal(area*10, marea)
    mesh = walter_leaf_mesh(leaf,10,2,10)
    marea = mesh_area(mesh)
    assert_almost_equal(area*20, marea)

    # test compensation for varying nb_segments
    leafref = walter_leaf(nb_segment=50)
    area_ref = leaf_area(leafref)
    leaf = walter_leaf(nb_segment=2)
    area = leaf_area(leaf)
    assert_almost_equal(area, area_ref, 2)
    mesh = walter_leaf_mesh(leaf)
    marea = mesh_area(mesh)
    assert_allclose(area, marea)
    # direct flat mesh (debug)
    xx, yy, ss, rr = leaf
    m = plantgl_shape(*leaf_to_mesh_2d(ss, [0] * len(ss), rr))
    dmarea = mesh_area(m)
    assert_almost_equal(area, dmarea)

    # growing leaf
    leaf = walter_leaf()
    area = leaf_area(leaf, length=0.5)
    mesh = walter_leaf_mesh(leaf, visible_length=0.5)
    marea = mesh_area(mesh)
    assert_almost_equal(area, marea,2)

    area = leaf_area(leaf, length=1e-1)
    mesh = walter_leaf_mesh(leaf, visible_length=1e-1)
    marea = mesh_area(mesh)
    assert_almost_equal(area, marea,2)

    # a particularly deformed mesh even with 10 points: rank=2: to be checked if this is due to the loss of the 'maximal width' point
    # during leaf simplification
