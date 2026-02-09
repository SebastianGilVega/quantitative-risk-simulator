import matplotlib.pyplot as plt
from statsmodels.graphics.regressionplots import abline_plot
import seaborn as sns


def plot_prices_log_return(ticker, close_price, log_return, data_index):
    #graph
    fig, ax1 = plt.subplots(figsize=(12,6))
    
    color ="tab:blue"
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price", color=color)
    ax1.plot(data_index, close_price, label="Close Price", color=color, alpha=0.8)
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.grid(True)

    ax2 = ax1.twinx()

    color = "tab:green"
    ax2.set_ylabel("Log Returns", color=color)
    ax2.plot(data_index, log_return, label="Log Return", alpha=0.9, color=color)
    ax2.tick_params(axis="y", labelcolor=color)

    #Set title, Labels, Legend (common elements)
    plt.title(f"{ticker}: price vs Log Returns")
    plt.tight_layout()
    plt.show()

def plot_price_with_volatility(ticker, close_price, volatility, data_index):
    #canva
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,8), sharex=True)
    
    #Plot Price on top
    ax1.plot(data_index, close_price, label="Close Price", color="blue")
    ax1.set_title(f"{ticker} Price vs Volatility (Risk)")
    ax1.set_ylabel("Price")
    ax1.grid(True)
    ax1.legend(loc="upper left")

    #Plot Volatility on Bottom
    ax2.plot(data_index, volatility, label="30-days Volatility (Std Dev)", color="orange")
    ax2.set_ylabel("Volatility")
    ax2.set_xlabel("Date")
    ax2.grid(True)
    ax2.legend(loc="upper left")

    plt.tight_layout()
    plt.show()

    
def plot_regression(ticker, X, Y, results):

    # Canva
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(X, Y, alpha=0.6)

    abline_plot(model_results=results, ax=ax, color="red", label="OLS Line")

    ax.set_xlabel("Benchmark")
    ax.set_ylabel(f"{ticker} Stock")
    ax.set_title(f"Linear Regression {ticker} Stock against Benchmark")
    ax.legend()
    
    plt.grid(True)
    plt.show()

def plot_var_histogram(ticker, log_returns, param_var, hist_var):
    
    plt.figure(figsize=(10, 6))

    # Plot the histogram of actual returns
    plt.hist(log_returns, bins=50, density=True, alpha=0.6, label="Actual Returns")

    # Add vertical lines for the VaR calculations
    plt.axvline(x=param_var, color='r', linestyle="--", label=f"Parametric VaR: {param_var:.4f}")
    plt.axvline(x=hist_var, color="k", linestyle="-", label=f"Historical VaR: {hist_var:.4f}")

    plt.title(f"Value at Risk (VaR) Analisis: {ticker}")
    plt.legend()
    plt.show()

def plot_monte_carlo_simulation(ticker, simulation):

    fig, ax = plt.subplots(figsize=(12, 6))

    days_count = simulation.shape[0]
    ax.plot(simulation, alpha=0.1, color="red")

    ax.plot([], [], color="red", label="Possible Stock Routes")

    ax.set_xlabel("Days into the Future")
    ax.set_ylabel("Stock Price")
    ax.set_title(f"{ticker} Monte Carlo Simalation ({days_count} Days)")

    ax.grid(True)
    plt.show()

def plot_scree(explained_variance):
    labels = [f"PC{i+1}" for i in range(len(explained_variance))]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, explained_variance, alpha=0.7, color='blue', label='Individual Variance')
    
    plt.ylabel('Explained Variance Ratio')
    plt.xlabel('Principal Components')
    plt.title('Scree Plot: The Invisible Forces Driving Your Portfolio')
    plt.show()