# data_loader.py
# Fetches data for Global Tech Giants.

import yfinance as yf
import pandas as pd
import numpy as np

# 1. Define our list of Global Tech Giants
TECH_LIST = {
    'AAPL': {'name': 'Apple Inc.', 'sector': 'Technology'},
    'MSFT': {'name': 'Microsoft Corporation', 'sector': 'Technology'},
    'GOOGL': {'name': 'Alphabet Inc. (Google)', 'sector': 'Technology'},
    'NVDA': {'name': 'NVIDIA Corporation', 'sector': 'Technology'},
    'TSLA': {'name': 'Tesla, Inc.', 'sector': 'Technology'}  # Classified as Technology for this analysis
}

# 2. The main function to get data
def get_company_data(ticker):
    """Fetches data for a given tech stock ticker."""
    try:
        company = yf.Ticker(ticker)
        info = company.info
        
        # Check if basic info is available
        if not info:
            print(f"No info found for {ticker}")
            return None
        
        # Get historical stock prices (2019-2024)
        stock_history = company.history(start='2019-01-01', end='2024-12-31')
        if stock_history.empty:
            print(f"No stock history found for {ticker}")
            return None
        
        # Get financial statements
        income_stmt = company.income_stmt
        balance_sheet = company.balance_sheet
        
        if income_stmt is None or income_stmt.empty:
            print(f"No income statement found for {ticker}")
            # Create a simple dataframe as a fallback
            financials_df = pd.DataFrame()
        else:
            # Process Annual Financials
            financials = income_stmt.T
            financials_df = pd.DataFrame(index=financials.index)
            
            # Safely get metrics if they exist
            key_metrics = ['Total Revenue', 'Net Income', 'Gross Profit', 'Operating Income']
            for metric in key_metrics:
                if metric in financials.columns:
                    financials_df[metric] = financials[metric]
            
            # Calculate key ratios
            if 'Net Income' in financials.columns and 'Total Revenue' in financials.columns:
                financials_df['Net Profit Margin'] = (financials['Net Income'] / financials['Total Revenue']) * 100
        
        # Combine into a master dictionary for this company
        company_data = {
            'info': info,
            'stock_history': stock_history,
            'financials': financials_df
        }
        
        print(f"Successfully loaded data for {ticker}")
        return company_data
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None

# 3. Function to get data for ALL tech firms
def get_all_company_data():
    """Loops through TECH_LIST and gets data for each one."""
    all_data = {}
    for ticker in TECH_LIST:
        print(f"\nAttempting to fetch data for {ticker}...")
        data = get_company_data(ticker)
        if data is not None:
            all_data[ticker] = data
            print(f"✓ Successfully added {ticker} to dataset")
        else:
            print(f"✗ Failed to load data for {ticker}")
    
    print(f"\nTotal companies loaded: {len(all_data)}/{len(TECH_LIST)}")
    return all_data