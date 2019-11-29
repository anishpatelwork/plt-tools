from plttools import PLT, plt_calculator, EPCurve


class MarginalImpact:
    def __init__(self, base_plt, submission_plt, number_of_simulations):
        self.base_plt = base_plt
        self.submission_plt = submission_plt
        self.grouped_plt = plt_calculator.group_plts(base_plt, submission_plt)
        self.number_of_simulations = number_of_simulations

    def base_aal(self):
        return self.base_plt.get_aal()

    def submission_aal(self):
        return self.submission_plt().get_aal()

    def grouped_aal(self):
        return self.grouped_plt.get_aal()

    def change_in_aal(self):
        return abs(self.base_aal() - self.grouped_aal())/self.base_aal()

    def base_aep(self):
        return plt_calculator.calculate_aep_curve(self.base_plt.plt, self.number_of_simulations)

    def submission_aep(self):
        return plt_calculator.calculate_aep_curve(self.submission_plt.plt, self.number_of_simulations)

    def grouped_aep(self):
        return plt_calculator.calculate_aep_curve(self.grouped_plt.plt, self.number_of_simulations)

    def marginal_aep(self):
        grouped_aep_std = self.grouped_aep().get_standard_return_period_ep()
        base_aep_std = self.base_aep().get_standard_return_period_ep()
        return_periods = EPCurve.RETURN_PERIODS

        marginal_aep = {}
        for return_period in return_periods:
            probability = 1/return_period
            marginal_aep[probability] = abs(
                base_aep_std[probability] - grouped_aep_std[probability])/base_aep_std[probability]

        return marginal_aep
