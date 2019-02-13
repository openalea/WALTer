"""Test light/sky function and connection with walter date / meteo data"""

import datetime
from walter.light import get_light, get_turtle_light
from nose.tools import assert_almost_equal


def walter_dates(sowing_date=datetime.date(1998,10,15), iterations=1):
    """generate dates like walter.lpy over time"""
    dd = [sowing_date + datetime.timedelta(elapsed_time) for elapsed_time in range(iterations)]
    if iterations == 1:
        return dd[0]
    else:
        return dd


def test_get_turtle_light():
    par = 1
    d = walter_dates()
    nrj0, dir0 = zip(*get_light(par, 4, 5))
    nrj, dir = zip(*get_turtle_light(par))
    assert_almost_equal(sum(nrj0), 1)
    assert_almost_equal(sum(nrj), 1)

    par = 10
    nrj0, dir0 = zip(*get_light(par, 4, 5))
    nrj, dir = zip(*get_turtle_light(par))
    assert_almost_equal(sum(nrj0), 10)
    assert_almost_equal(sum(nrj), 10)

    par = 1
    nrj_soc, _ = zip(*get_turtle_light(par))
    nrj, dir = zip(*get_turtle_light(par, curent_date=d, sky_type='clear_sky'))
    assert_almost_equal(sum(nrj), 1)
    assert len(nrj) == 46