from walter.leaf_shape import walter_sr, walter_leaf, leaf_area, walter_leaf_mesh, mesh_area
from walter.cereals_leaf import blade_elt_area, form_factor
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


def test_nb_segment():
    """how nb segment changes form factor"""
    leaf_ref = walter_leaf(nb_segment=100)
    ffref = form_factor(leaf_ref)
    nseg = (2,5,10,20)
    leaves = map(walter_leaf,nseg)
    ff = map(form_factor, leaves)
    rel_err = abs(array(ff) - ffref) / ffref
    max_err = array((0.03, 0.05, 0.01, 0.001))
    assert all(rel_err < max_err)


def test_area_vs_area_mesh():
    # TODO check why meash area is not compensated by cereals.fitting

    leaf = walter_leaf()
    ff = form_factor(leaf)
    area = leaf_area(leaf)
    areaff = leaf_area(leaf, form_factor=ff)
    assert_almost_equal(area, areaff, 2)
    # about 1 percent difference between area and meash area (caribu) if compensate=False
    mesh = walter_leaf_mesh(leaf, compensate=False)
    marea = mesh_area(mesh)
    assert_allclose(area, marea, rtol=0.015)
    # No diff between mesh and leaf if compensate=True (but mesh width are modified)
    mesh = walter_leaf_mesh(leaf)
    marea = mesh_area(mesh)
    assert_allclose(area, marea)

    # effect of nb_segments
    leaf = walter_leaf(nb_segment=100)
    area = leaf_area(leaf)
    mesh = walter_leaf_mesh(leaf, compensate=False)
    marea = mesh_area(mesh)
    # error decrease below 1 per thousand
    assert_allclose(area, marea, rtol=0.0015)

    leaf = walter_leaf(nb_segment=2)
    area = leaf_area(leaf)
    mesh = walter_leaf_mesh(leaf, compensate=False)
    marea = mesh_area(mesh)
    # error drop to 30 percent
    assert_allclose(area, marea, rtol=.3)
    # but compensate still works
    mesh = walter_leaf_mesh(leaf)
    marea = mesh_area(mesh)
    assert_allclose(area, marea)

    # growing leaf
    leaf = walter_leaf()
    area = leaf_area(leaf, length=0.5)
    mesh = walter_leaf_mesh(leaf, visible_length=0.5)
    marea = mesh_area(mesh)
    assert_allclose(area, marea)