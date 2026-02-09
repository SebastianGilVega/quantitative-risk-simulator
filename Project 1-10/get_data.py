import yfinance as yf
import os
import pandas as pd

DATA_DIR = "stock_data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_stock_data(ticker, start_date, end_date, force_download=False):
    file_name = os.path.join(DATA_DIR, f"{ticker}_{start_date}_to_{end_date}.csv")
    df_to_return = None

    if os.path.exists(file_name) and not force_download:
        print(f"Loding {ticker} data from {file_name} ...")
        try:
            df_loaded = pd.read_csv(file_name, index_col=0, parse_dates=True)
            if df_loaded.index.name != "Date":
                df_loaded.index.name = "Date"
            
            # Safeguard: Ensure loaded DataFrame has simple columns
            if isinstance(df_loaded.columns, pd.MultiIndex):
                print(f"Loaded CSV for {ticker} has MultiIndex columns. Flattering ...")
                df_loaded.columns = df_loaded.columns.get_level_values(0)

            # Ensure "Close" column is numeric
            if "Close" in df_loaded and pd.api.types.is_numeric_dtype(df_loaded["Close"]):
                print(f"Successfully loaded and validated {ticker} data from CSV")
                df_to_return = df_loaded
            else:
                error_msg = f"Problem with Loaded CVS for {ticker}:"
                if "Close" not in df_loaded.columns: 
                    error_msg += "'Close' column missing. "
                elif not pd.api.types.is_numeric_dtype(df_loaded["Close"]): 
                    error_msg += f"'Close' column not numeric type: (type {df_loaded['Close'].dtype})"
                print(error_msg + "Redownloading.")
        except Exception as e:
            print(f"Error reading or processing {file_name}: {e}. Re-downloading.")
    
    if df_to_return is None: # Triggered if file didn't exist, force_download, or loading failed
        print(f"Downloading {ticker} data from Yahoo Finance ... ")
         # yf.download for a single ticker can still return MultiIndex with auto_adjust=True
        df_downloaded = yf.download(ticker, start=start_date, end=end_date, progress=False)

        if not df_downloaded.empty:
            df_processed = df_downloaded.copy() # Work on a copy

            # FLATTEN the downloaded data columns before returning AND saving
            if isinstance(df_processed.columns, pd.MultiIndex):
                print(f"Downloaded {ticker} data has MultiIndex columns. Flattening...")
                # This takes the first level of the column index, e.g., ('Close', 'GOOG') -> 'Close'
                df_processed.columns = df_processed.columns.get_level_values(0)
            
            # At this point, df_processed should have simple column names like 'Open', 'Close', etc.
            
            df_processed.to_csv(file_name, index=True, header=True)
            print(f"Saved flattened {ticker} data to {file_name}")
            df_to_return = df_processed
        else:
            print(f"Warning: No data downloaded for {ticker}. Check ticker symbol or date range.")
            df_to_return = pd.DataFrame() # Return an empty DataFrame
    
    return df_to_return
