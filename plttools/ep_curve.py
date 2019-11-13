import pandas as pd
from enum import Enum

class EPCurve:

    def __init__(self, data, ep_type=None):
        self.curve = pd.DataFrame(data)
        self.curve = self.curve.set_index('Probability')
        if ep_type is None:
            self.ep_type = EPType.UNKNOWN
        else:
            self.ep_type = ep_type

    def loss_at_a_given_return_period(self, return_period):
        probability = 1 / return_period
        if probability in self.curve.index:
            loss = self.curve.loc[probability].Loss
        else:
            prob_array = [probability]
            self.curve = self.curve.reindex(self.curve.index.union(prob_array)).sort_index(ascending=True).interpolate(method='index')
            loss = self.curve.loc[probability].Loss
        return loss

    def get_ep_type(self):
        return self.ep_type

class EPType(Enum):
    OEP = 1
    AEP = 2
    UNKNOWN = 3