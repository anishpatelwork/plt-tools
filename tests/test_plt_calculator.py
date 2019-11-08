from plttools import plt_calculator
import pytest
import pandas as pd

def test_calculate_plt():
    plt_file = 'tests/test_plt.csv'
    plt_df = pd.read_csv(plt_file)
    aal = plt_calculator.CalculateAAL(plt_df, 50000)
    assert aal == pytest.approx(101041, rel=1)