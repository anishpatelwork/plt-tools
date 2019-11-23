""" PLT """


class PLT:
    """ Period Loss Table (PLT)
        Structure of a PLT is as follows:
        periodId (int),
        eventId (int),
        lossDate (datetime),
        eventDate (datetime),
        loss (float),
        peril (string - optional),
        businessUnit (string - optional)
        admin1 (string - optional)
        country (string - optional)
    """

    def __init__(self, df, number_of_simulations):
        self.plt = df
        self.simulations = number_of_simulations

    def get_aal(self):
        """ Retrieves the AAL for the PLT
            Parameters
            ----------

            Returns
            -------
            float :
                The average annual loss = total annual losses / number of simulations
        """
        annual_losses = self.plt[['periodId', 'loss']
                                 ].groupby('periodId').sum()
        total_annual_losses = annual_losses[['loss']].sum()
        aal = total_annual_losses.loss / self.simulations
        return aal

    def get_standard_deviation(self):
        """ Retrieves the Standard Deviation for the losses of the annual losses for the PLT
            Parameters
            ----------

            Returns
            -------
            float :
                The standard deviation of the annual losses for the PLT
        """
        annual_losses = self.plt[['periodId', 'loss']
                                 ].groupby('periodId').sum()
        stddev = annual_losses.loss.std()
        return stddev
