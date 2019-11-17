""" EP Curve module for the representation of an EP Curve"""
from enum import Enum
import pandas as pd


class EPCurve:
    """EP Curve"""

    def __init__(self, data, ep_type=None):
        """ Type initialiser for EP Curve """

        self.curve = pd.DataFrame(data)
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

    def get_ep_type(self):
        """ Get the type of EP Curve """
        return self.ep_type


class EPType(Enum):
    """ EP Type Enum representing type of EP Curve """
    OEP = 1
    AEP = 2
    UNKNOWN = 3
