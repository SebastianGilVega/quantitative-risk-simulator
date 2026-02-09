import pandas as pd
import numpy as np
from get_data import get_stock_data
import statsmodels.api as sm
from plotting import plot_regression


def regression_engine(ticker, df):
    
    # Get Benchmark (bm)
    starting_date = df.index[0].strftime('%Y-%m-%d')
    ending_date = df.index[-1].strftime('%Y-%m-%d')

    bm = get_stock_data("^GSPC", starting_date, ending_date)

    # Benchmark Log Returnts
    bm["Log Return"] = np.log(bm["Close"] / bm["Close"].shift(1))

    # Inner join the stock and benchmark index
    merged_df =pd.merge(df, bm, left_index=True, right_index=True, suffixes=('_stock', '_mkt'))
    merged_df = merged_df.dropna() #dop NaNs

    # Define X and Y
    Y = merged_df["Log Return_stock"]
    X = merged_df["Log Return_mkt"]

    X = sm.add_constant(X) #Add a constant

    # Linear Regression (OLS) to get beta and alpha
    model = sm.OLS(Y, X)
    results = model.fit()

    alpha = results.params.iloc[0]
    beta = results.params.iloc[1]

    # Print friendly summary
    print(f"\n--- Regression Results for {ticker} ---")
    print(f"Beta (Market Risk): {beta:.4f}")
    print(f"Alpha (Excess Return): {alpha:.6f}")
    print(f"R-squared: {results.rsquared:.4f}")

    plot_regression(ticker, merged_df["Log Return_mkt"], Y, results)


    return alpha, beta