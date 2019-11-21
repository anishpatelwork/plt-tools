""" EP Curve module for the representation of an EP Curve"""
from enum import Enum
import pandas as pd
import numpy as np
import plttools.ep_settings as ep_settings


class EPCurve:
    """EP Curve"""

    def __init__(self, data, ep_type=None):
        """ Type initialiser for EP Curve """

        self.curve = pd.DataFrame(data)
        max_loss_prob = [{"Probability": np.finfo(
            float).tiny, "Loss": self.curve.max().Loss}]
        self.curve = self.curve.append(pd.DataFrame(max_loss_prob))
        self.curve = self.curve.set_index('Probability')

        if ep_type is None:
            self.ep_type = EPType.UNKNOWN
        else:
            self.ep_type = ep_type

    def loss_at_a_given_return_period(self, return_period):
        """ Get a loss from EP curve """

        probability = 1 / return_period
        if probability in self.curve.index:
            loss = self.curve.loc[probability].Loss
        else:
            prob_array = [probability]
            self.curve = self.curve.reindex(self.curve.index.union(prob_array)).sort_index(
                ascending=True).interpolate(method='index')
            loss = self.curve.loc[probability].Loss
        return loss

    def tce_loss_at_a_given_return_period(self, return_period):
        """ Calculate TCE from EP curve at a given return period """
        return_period_loss = self.loss_at_a_given_return_period(return_period)
        probability = 1 / return_period
        subset = self.curve[self.curve.index <= probability]
        expected_loss_above_rpl = (subset.index * subset['Loss']).mean()
        return return_period_loss + expected_loss_above_rpl

    def get_ep_type(self):
        """ Get the type of EP Curve """
        return self.ep_type

    def get_standard_return_period_ep(self):
        """ Calculates standard EP return periods and returns the overall curve """
        return_periods = ep_settings.RETURN_PERIODS
        probabilities = list(map(lambda x: 1/x, return_periods))
        self.curve = self.curve.reindex(self.curve.index.union(probabilities)).sort_index(
            ascending=True).interpolate(method='index')
        return self.curve.to_dict()['Loss']


class EPType(Enum):
    """ EP Type Enum representing type of EP Curve """
    OEP = 1
    AEP = 2
    UNKNOWN = 3
