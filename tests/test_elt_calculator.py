""" elt Calculator tests"""
# pylint: disable=line-too-long

from aggregationtools import elt_calculator
from aggregationtools.elt import ELT


def test_group_elts():
    """Group ELTs"""
    d_1 = {
        "EventId": [100, 200, 300, 400, 500, 600],
        "Loss": [51765, 30931, 3281, 21980, 19025, 84287],
        "StdDevI": [2591, 10482, 6019, 15272, 75853, 62429],
        "StdDevC": [67373, 13942, 12004, 49023, 58268, 181382],
        "ExpValue": [200000, 200000, 50000, 50000, 500000, 200000],
        "Rate": [0.000018, 0.00021, 0.000305, 0.000912, 0.000078, 0.000042]
    }
    d_2 = {
        "EventId": [100, 200, 350, 400, 526],
        "Loss": [16329, 19782, 27540, 76387, 44536],
        "StdDevI": [26826, 13335, 48962, 5052, 7441],
        "StdDevC": [18160, 4792, 17761, 4792, 22090],
        "ExpValue": [100000, 100000, 210000, 70000, 300000],
        "Rate": [0.000018, 0.00021, 0.000411, 0.000912, 0.000729]
    }
    grouped_elt = elt_calculator.group_elts(
        ELT(d_1), ELT(d_2)).elt

    assert grouped_elt.loc[grouped_elt['EventId'] == 100].Loss.sum() == 68094


def test_group_elts_single_input():
    """Group elts"""
    d_1 = {
        "EventId": [100, 200, 300, 400, 500, 600, 100, 200, 350, 400, 526],
        "Loss": [51765, 30931, 3281, 21980, 19025, 84287, 16329, 19782, 27540, 76387, 44536],
        "StdDevI": [2591, 10482, 6019, 15272, 75853, 62429, 26826, 13335, 48962, 5052, 7441],
        "StdDevC": [67373, 13942, 12004, 49023, 58268, 181382, 18160, 4792, 17761, 4792, 22090],
        "ExpValue": [200000, 200000, 50000, 50000, 500000, 200000, 100000, 100000, 210000, 70000, 300000],
        "Rate": [0.000018, 0.00021, 0.000305, 0.000912, 0.000078, 0.000042, 0.000018, 0.00021, 0.000411, 0.000912, 0.000729]
    }

    grouped_elt = elt_calculator.group_elts(
        ELT(d_1)).elt

    assert grouped_elt.loc[grouped_elt['EventId'] == 100].Loss.sum() == 68094
