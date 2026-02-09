import numpy as np
from plotting import plot_monte_carlo_simulation

def monte_carlo_simulation(ticker, df):

    days = 30
    simulations = 1000
    log_return = df["Log Return"].dropna()

    # Discrite Equation elements
    mu = np.mean(log_return)
    Sigma = np.std(log_return)
    z_hat = np.random.randn(days, simulations)
    simulation = np.zeros((days, simulations))

    drift = (mu - ((Sigma ** 2) / 2))
        
    simulation[0, :] = df["Close"].iloc[-1]
    
    # Simulation
    for l in range(1, days):
        simulation[l, :] = simulation[(l - 1), :] * np.exp(drift + Sigma * z_hat[l, :])

    
    plot_monte_carlo_simulation(ticker, simulation)

