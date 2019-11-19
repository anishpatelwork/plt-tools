""" Tests for EP Settings """
from plttools import ep_settings


def test_return_periods():
    """ Test that return periods list exists and is not empty """
    assert len(ep_settings.RETURN_PERIODS) > 0
