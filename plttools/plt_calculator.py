def CalculateAAL(plt, number_of_simulations):
    annual_losses = plt[['periodId', 'loss']].groupby('periodId').sum()
    total_annual_losses = annual_losses[['loss']].sum()
    return total_annual_losses.loss / number_of_simulations
    