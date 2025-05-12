# data_ingestion/api_agent.py
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(tickers, start_date, end_date):
    stock_data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        stock_data[ticker] = data
    return stock_data

def save_to_csv(stock_data, filename):
    combined_data = pd.DataFrame()
    for ticker, data in stock_data.items():
        data['Ticker'] = ticker
        combined_data = pd.concat([combined_data, data])
    combined_data.to_csv(filename)
    print(f"Saved data to {filename}")

if __name__ == "__main__":
    tickers = ["2330.TW", "005930.KS"]  # TSMC, Samsung
    end_date = datetime.today()
    start_date = end_date - timedelta(days=7)
    stock_data = fetch_stock_data(tickers, start_date, end_date)
    save_to_csv(stock_data, "../data/stock_data.csv")  # Path to root data folder