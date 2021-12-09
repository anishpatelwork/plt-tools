""" elt Calculator
ELT calculator functions
"""
import numpy
import math
import pandas as pd
import numpy as np
from scipy.stats import beta
from aggregationtools import ELT, ep_curve


def calculate_oep_curve(elt, grid_size=2**14):
    """ This function calculates the OEP of a given ELT
    ----------
    plt : pandas dataframe containing PLT
    number_of_simulations :
        Number of simulation periods. Important to supply as cannot assume
        that the max number of periods is the number of simulation periods

    Returns
    -------
    EPCurve :
         exceedance probability curve

    """
    elt_lambda = ELT(elt).get_lambda()
    severity_distribution = calculate_severity_distribution(elt, grid_size)
    severity_distribution['OEP'] = 1 - numpy.exp(-elt_lambda * severity_distribution['CEP'])
    oep_test = severity_distribution.rename(columns={'OEP': 'Probability', 'threshold': 'Loss'})

    return ep_curve.EPCurve(oep_test, ep_type=ep_curve.EPType.OEP)


def calculate_oep_curve(elt, grid_size=2**14):
    """ This function calculates the OEP of a given ELT
    ----------
    plt : pandas dataframe containing PLT
    number_of_simulations :
        Number of simulation periods. Important to supply as cannot assume
        that the max number of periods is the number of simulation periods

    Returns
    -------
    EPCurve :
         exceedance probability curve

    """
    elt_lambda = ELT(elt).get_lambda()
    severity_distribution = calculate_severity_distribution(elt, grid_size)
    severity_distribution['OEP'] = 1 - numpy.exp(-elt_lambda * severity_distribution['CEP'])
    oep_test = severity_distribution.rename(columns={'OEP': 'Probability', 'threshold': 'Loss'})

    return ep_curve.EPCurve(oep_test, ep_type=ep_curve.EPType.OEP)

def calculate_frequency_distribution(elt):
    """ This function calculates the frequency distribution or the probability of having
    exactly n occurences in a year
    ----------
    elt : pandas dataframe containing ELT

    Returns
    -------
    frequency_distribution
    """
    elt_lambda = ELT(elt).get_lambda()
    frequency_distribution = [(math.exp(-elt_lambda)*elt_lambda**n)/math.factorial(n) for n in range(0, 5)]

    return frequency_distribution


def calculate_severity_distribution(elt, n=2**2):
    """ This function calculates the severity distribution or the distribution
    of the size of losses, given that an event has occurred
    ----------
    elt : pandas dataframe containing ELT

    Returns
    -------
    severity_distribution
    """
    max_loss = elt['Loss'].max()
    loss_thresholds = numpy.linspace(0, max_loss, num=n+1)
    probability = {}
    CEP = {}

    for threshold in loss_thresholds:
        probability[threshold] = 1 - beta.cdf(threshold/elt['ExpValue'], elt['alpha'], elt['beta'])
        probability[threshold] = np.nan_to_num(probability[threshold])
        CEP[threshold] = sum(elt['Rate'] * probability[threshold]) / ELT(elt).get_lambda()

    severity_distribution = pd.DataFrame(CEP.items(), columns=['threshold', 'CEP'])
    severity_density_function = severity_distribution.copy(deep=True)
    severity_density_function['shift_CEP'] = severity_density_function['CEP'].shift(1)
    severity_density_function = severity_density_function[1:]
    severity_density_function['CEP'] = severity_density_function['shift_CEP'] - severity_density_function['CEP']
    severity_density_function.drop('shift_CEP', axis=1, inplace=True)

    return severity_distribution, severity_density_function


def group_elts(elt1, elt2=None):
    """ This function groups two elts together
    Parameters
    ----------
    elt1 : pandas dataframe containing ELT
    elt2 : pandas dataframe containing elt

    Returns
    -------
    elt :
        A pandas dataframe containing a elt

    """
    if elt2 is None:
        grouped_elt = elt1.elt
    else:
        grouped_elt = pd.concat([elt1.elt, elt2.elt], axis=0)

    elt_unique = grouped_elt[['EventId','Rate','Loss','StdDevI','StdDevC','ExpValue']].loc[~grouped_elt.duplicated(subset='EventId', keep=False), :]
    elt_matches = grouped_elt[['EventId','Rate','Loss','StdDevI','StdDevC','ExpValue']].loc[grouped_elt.duplicated(subset='EventId', keep=False), :]
    elt_matches = elt_matches.groupby(['EventId', 'Rate']).agg({
                             'Loss': 'sum',
                             'StdDevC': 'sum',
                             'ExpValue': 'sum',
                             'StdDevI': lambda x: np.sqrt((x*x).sum())}
            ).reset_index()
    concatenated_elt = pd.concat([elt_unique, elt_matches]).reset_index(drop=True)

    return ELT(concatenated_elt)

