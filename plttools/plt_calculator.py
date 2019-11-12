import pandas as pd
from plttools import ep_curve
import numpy as np

def calculate_AAL(plt, number_of_simulations):
    annual_losses = plt[['periodId', 'loss']].groupby('periodId').sum()
    total_annual_losses = annual_losses[['loss']].sum()
    return total_annual_losses.loss / number_of_simulations

def calculate_OEP_curve(plt, number_of_simulations):
    complete_plt = _fill_plt_empty_periods(plt, number_of_simulations)
    max_period_losses = complete_plt.groupby('periodId').max().fillna(0).sort_values(by=['loss'])
    max_period_losses = _calculate_probabilities_for_period_losses(max_period_losses)
    return ep_curve.EPCurve(max_period_losses.rename(columns={'loss': 'Loss'}), ep_type=ep_curve.EPType.OEP)

def calculate_AEP_curve(plt, number_of_simulations):
    complete_plt = _fill_plt_empty_periods(plt, number_of_simulations)  
    max_period_losses = complete_plt.groupby('periodId').sum().fillna(0).sort_values(by=['loss'])
    max_period_losses = _calculate_probabilities_for_period_losses(max_period_losses)
    return ep_curve.EPCurve(max_period_losses.rename(columns={'loss': 'Loss'}), ep_type=ep_curve.EPType.AEP)

def _calculate_probabilities_for_period_losses(period_losses):
    period_losses['row'] = np.arange(len(period_losses))
    period_losses['inv_row'] = len(period_losses) - period_losses['row']
    period_losses['Probability'] = period_losses['inv_row'] * 1/len(period_losses)
    return period_losses

def _fill_plt_empty_periods(plt, number_of_simulations):
    plt_placeholder = []
    for period in range(1,number_of_simulations + 1):
        plt_placeholder.append(period)
    placeholder = pd.DataFrame(plt_placeholder, columns=['periodId'])
    return pd.merge(placeholder, plt, how='left', on=['periodId'])