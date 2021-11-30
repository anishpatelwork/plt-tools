""" elt Calculator
ELT calculator functions
"""
import numpy
import pandas as pd
import numpy as np
from aggregationtools import ep_curve, ELT


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

