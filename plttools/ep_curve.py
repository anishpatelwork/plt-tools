import pandas as pd
from enum import Enum

class EPCurve:

    def __init__(self, data, ep_type=None):
        self.curve = pd.DataFrame(data)
        if ep_type is None:
            self.ep_type = EPType.UNKNOWN
        else:
            self.ep_type = ep_type

    def loss_at_a_given_return_period(self, return_period):
        probability = 1 / return_period
        loss = self.curve[self.curve.Probability == probability].Loss.iloc[0]
        return loss

    def get_ep_type(self):
        return self.ep_type

class EPType(Enum):
    OEP = 1
    AEP = 2
    UNKNOWN = 3