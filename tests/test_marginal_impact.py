from plttools import MarginalImpact, PLT


def test_marginal_impact():
    d_1 = {
        "PeriodId": [1, 1, 2, 3, 4, 5, 6],
        "EventId": [123, 678, 124, 125, 126, 127, 128],
        "EventDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018],
        "Loss": [1000, 1020, 900, 1100, 1200, 800, 1000],
        "LossDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018]
    }
    d_2 = {
        "PeriodId": [1, 1, 2, 3, 4, 5, 6],
        "EventId": [123, 678, 124, 125, 126, 127, 128],
        "EventDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018],
        "Loss": [100, 102, 90, 110, 120, 80, 100],
        "LossDate": [10/19/2018, 10/20/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018, 10/19/2018]
    }
    number_of_simulations = 6
    marginal = MarginalImpact(PLT(d_1), PLT(d_2), number_of_simulations)
    assert abs(1170 - 1287) / 1170 == marginal.change_in_aal()

    marginal_aep = marginal.base_aep()
