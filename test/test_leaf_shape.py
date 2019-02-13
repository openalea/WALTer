from walter.cereals_leaf import parametric_leaf, blade_elt_area
from nose.tools import assert_almost_equal

def test_leaf_area():
    x, y, s, r = parametric_leaf()
    stot = blade_elt_area(s,r)
    st = blade_elt_area(s, r, sr_base=0.5)
    sb = blade_elt_area(s, r, sr_top=0.5)
    assert sb > st
    assert_almost_equal(sb+st, stot, 2)