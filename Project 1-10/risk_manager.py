import numpy as np
from scipy.stats import norm
from plotting import plot_var_histogram

def calculate_var(ticker, df, confidence_level=0.95):

    # Parametric VaR (The Gaussian Way)
    mean = np.mean(df["Log Return"])
    std = np.std(df["Log Return"])
    # ppf = Percent Point Function
    z_score = norm.ppf(1 - confidence_level)

    parametric_var = mean - (z_score  * std)

    # Historical Var (The Empitical Way)
    percentile = (1 - confidence_level) * 100
    log_return = df["Log Return"].dropna()
    historical_var = np.percentile(log_return, percentile)

    plot_var_histogram(ticker, df["Log Return"], parametric_var, historical_var)
