""" PLT Calculator tests"""
# pylint: disable=line-too-long

import pandas as pd
from plttools import plt_calculator, EPCurve, EPType


def test_calculate_oep_curve():
    """ Test Calculate OEP Curve"""
    oep = plt_calculator.calculate_oep_curve(TEST_PLT, 5)
    assert isinstance(oep, EPCurve)
    assert oep.get_ep_type() == EPType.OEP
    assert oep.loss_at_a_given_return_period(5) == 900
    assert oep.loss_at_a_given_return_period(2.5) == 800
    assert oep.loss_at_a_given_return_period(5/3) == 300
    assert oep.loss_at_a_given_return_period(1.25) == 100
    assert oep.loss_at_a_given_return_period(1) == 0


def test_calculate_aep_curve():
    """ Test Calculate AEP curve"""
    aep = plt_calculator.calculate_aep_curve(TEST_PLT, 5)
    assert isinstance(aep, EPCurve)
    assert aep.get_ep_type() == EPType.AEP
    assert aep.loss_at_a_given_return_period(5) == 3000
    assert aep.loss_at_a_given_return_period(2.5) == 900
    assert aep.loss_at_a_given_return_period(5/3) == 500
    assert aep.loss_at_a_given_return_period(1.25) == 100
    assert aep.loss_at_a_given_return_period(1) == 0


def test_group_plts():
    """Group PLTs"""
    d_1 = {
        "periodId": [1, 1, 2, 3, 4, 5, 6],
        "eventId": [123, 678, 124, 125, 126, 127, 128],
        "eventDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018],
        "loss": [100, 102, 90, 110, 120, 80, 100],
        "lossDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018]
    }
    d_2 = {
        "periodId": [1, 1, 2, 3, 4, 5, 6],
        "eventId": [123, 678, 124, 125, 126, 127, 128],
        "eventDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018],
        "loss": [100, 102, 90, 110, 120, 80, 100],
        "lossDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018]
    }
    grouped_plt = plt_calculator.group_plts(
        pd.DataFrame(d_1), pd.DataFrame(d_2))
    assert grouped_plt.loc[grouped_plt['periodId'] == 1].loss.sum() == 404


# def test_marginal_impact():
#     original_oep = plt_calculator.calculate_oep_curve(TEST_PLT, 5)
#     grouped_plt = plt_calculator.group_plts(
#         TEST_PLT, TEST_PLT
#     )
#     grouped_oep = plt_calculator.calculate_oep_curve(grouped_plt, 6)
#     assert original_oep.loss_at_a_given_return_period(2.5) == 800
#     assert grouped_oep.loss_at_a_given_return_period(2.5)

#     grouped_ep_curve = grouped_oep.get_standard_return_period_ep()
#     original_ep_curve = original_oep.get_standard_return_period_ep()
#     marginal_oep = {key: original_ep_curve[key] - grouped_ep_curve.get(key, 0)
#                     for key in original_ep_curve.keys()}
#     # This assertion is not a valid one
#     assert marginal_oep.loss_at_a_given_return_period(100) == 100


DATA = [
    {
        "periodId": 1,
        "eventId": 3500016,
        "lossDate": "3/13/2016 12:00:00 AM",
        "eventDate": "03/10/2016 00:00",
        "loss": 100
    },
    {
        "periodId": 3,
        "eventId": 3500129,
        "lossDate": "8/25/2016 12:00:00 AM",
        "eventDate": "8/24/2016 12:00:00 AM",
        "loss": 200
    },
    {
        "periodId": 3,
        "eventId": 3500140,
        "lossDate": "01/01/2017 00:00",
        "eventDate": "12/29/2016 12:00:00 AM",
        "loss": 300
    },
    {
        "periodId": 4,
        "eventId": 3500141,
        "lossDate": "01/10/2016 00:00",
        "eventDate": "01/09/2016 00:00",
        "loss": 400
    },
    {
        "periodId": 4,
        "eventId": 3500141,
        "lossDate": "01/11/2016 00:00",
        "eventDate": "01/09/2016 00:00",
        "loss": 500
    },
    {
        "periodId": 4,
        "eventId": 3500141,
        "lossDate": "1/13/2016 12:00:00 AM",
        "eventDate": "01/09/2016 00:00",
        "loss": 600
    },
    {
        "periodId": 4,
        "eventId": 3500141,
        "lossDate": "1/14/2016 12:00:00 AM",
        "eventDate": "01/09/2016 00:00",
        "loss": 700
    },
    {
        "periodId": 4,
        "eventId": 3500151,
        "lossDate": "8/19/2016 12:00:00 AM",
        "eventDate": "8/19/2016 12:00:00 AM",
        "loss": 800
    },
    {
        "periodId": 5,
        "eventId": 3500166,
        "lossDate": "9/19/2016 12:00:00 AM",
        "eventDate": "9/19/2016 12:00:00 AM",
        "loss": 900
    }
]

TEST_PLT = pd.DataFrame(DATA)
