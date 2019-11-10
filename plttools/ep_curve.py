import pandas as pd

class EPCurve:

    def __init__(self, data):
        self.curve = pd.DataFrame(data)

    def loss_at_a_given_return_period(self, return_period):
        probability = 1 / return_period
        loss = self.curve[self.curve.Probability == probability].Loss.iloc[0]
        return loss