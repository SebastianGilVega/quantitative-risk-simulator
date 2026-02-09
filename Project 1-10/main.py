import numpy as np
import pandas as pd
from get_data import get_stock_data
from plotting import plot_prices_log_return
from plotting import plot_price_with_volatility
from regression_engine import regression_engine
from risk_manager import calculate_var
from monte_carlo_simulation import monte_carlo_simulation
from porfolio import portfolio_analysis

tickers = input("Tickers (e.g. AAPL, MSFT): ")
start_date = input("What is the starting date (YYYY-MM-DD): ")
end_date = input("What is the ending date (YYYY-MM-DD): ")

ticker_list = [t.strip() for t in tickers.split(",")]
all_returns = []


for ticker in ticker_list:
    df = get_stock_data(ticker, start_date, end_date)
    # Check if df is empty before proceeding
    if df is None or df.empty:
        print(f"Skipping {ticker} due to missing data.")
        continue

    df["Log Return"] = np.log(df["Close"] / df["Close"].shift(1))
    df["Volatility"] = df["Log Return"].rolling(window=30).std()

    plot_prices_log_return(ticker, df["Close"], df["Log Return"], df.index)

    plot_price_with_volatility(ticker, df["Close"], df["Volatility"], df.index)

    regression_engine(ticker, df)

    calculate_var(ticker, df)

    monte_carlo_simulation(ticker, df)

    df = df.rename(columns={"Log Return": ticker})
    all_returns.append(df[ticker])

big_df = pd.concat(all_returns, axis=1)
big_df = big_df.dropna()

portfolio_analysis(big_df)
