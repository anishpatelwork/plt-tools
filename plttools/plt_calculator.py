""" PLT Calculator
A happy place for PLT calculator functions.
"""

import pandas as pd
import numpy as np
from plttools import ep_curve, PLT


def calculate_oep_curve(plt, number_of_simulations):
    """ This function calculates the OEP of a given PLT over a set number of simulations
    Parameters
    ----------
    plt : pandas dataframe containing PLT
    number_of_simulations :
        Number of simulation periods. Important to supply as cannot assume
        that the max number of periods is the number of simulation periods

    Returns
    -------
    EPCurve :
        An exceedance probability curve for the occurrance of a single event in a given year

    """
    complete_plt = _fill_plt_empty_periods(plt, number_of_simulations)
    max_period_losses = complete_plt.groupby(
        'PeriodId').max().fillna(0).sort_values(by=['Loss'])
    max_period_losses = _calculate_probabilities_for_period_losses(
        max_period_losses)
    return ep_curve.EPCurve(max_period_losses, ep_type=ep_curve.EPType.OEP)


def calculate_aep_curve(plt, number_of_simulations):
    """ This function calculates the AEP of a given PLT over a set number of simulations
    Parameters
    ----------
    plt : pandas dataframe containing PLT
    number_of_simulations :
        Number of simulation periods. Important to supply as cannot assume
        that the max number of periods is the number of simulation periods

    Returns
    -------
    EPCurve :
        An exceedance probability curve for the aggregate losses in a given year

    """
    complete_plt = _fill_plt_empty_periods(plt, number_of_simulations)
    sum_period_losses = complete_plt.groupby(
        'PeriodId').sum().fillna(0).sort_values(by=['Loss'])
    sum_period_losses = _calculate_probabilities_for_period_losses(
        sum_period_losses)
    return ep_curve.EPCurve(sum_period_losses, ep_type=ep_curve.EPType.AEP)


def group_plts(plt1, plt2):
    """ This function groups two PLTs together
    Parameters
    ----------
    plt1 : pandas dataframe containing PLT
    plt2 : pandas dataframe containing PLT

    Returns
    -------
    plt :
        A pandas dataframe containing a PLT

    """
    grouped_plt = pd.concat([plt1.plt, plt2.plt], axis=0)
    concatenated_plt = grouped_plt.groupby(['PeriodId',
                                            'EventId',
                                            'EventDate',
                                            'LossDate'], observed=True).sum().reset_index()
    return PLT(concatenated_plt)


def _calculate_probabilities_for_period_losses(period_losses):
    period_losses['row'] = np.arange(len(period_losses))
    period_losses['inv_row'] = len(period_losses) - period_losses['row']
    period_losses['Probability'] = period_losses['inv_row'] * \
        1/len(period_losses)
    return period_losses


def _fill_plt_empty_periods(plt, number_of_simulations):
    plt_placeholder = []
    for period in range(1, number_of_simulations + 1):
        plt_placeholder.append(period)
    placeholder = pd.DataFrame(plt_placeholder, columns=['PeriodId'])
    return pd.merge(placeholder, plt, how='left', on=['PeriodId'])
