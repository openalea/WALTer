from walter.leaf_shape import walter_sr
from nose.tools import assert_almost_equal


def test_walter_sr():
    s,r = walter_sr()


def test_leaf_area():
    x, y, s, r = parametric_leaf()
    stot = blade_elt_area(s,r)
    st = blade_elt_area(s, r, sr_base=0.5)
    sb = blade_elt_area(s, r, sr_top=0.5)
    assert sb > st
    assert_almost_equal(sb+st, stot, 2)