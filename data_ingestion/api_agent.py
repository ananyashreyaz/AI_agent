# data_ingestion/api_agent.py
import yfinance as yf
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()

class StockRequest(BaseModel):
    ticker: str

@app.post("/get_stock_data")
def get_stock_data(request: StockRequest):
    ticker = request.ticker
    stock = yf.Ticker(ticker)
    hist = stock.history(period="2d")

    if hist.empty:
        return {"error": "Invalid ticker or no data available"}

    latest_close = hist["Close"].iloc[-1]
    previous_close = hist["Close"].iloc[-2]
    change = round(((latest_close - previous_close) / previous_close) * 100, 2)

    # Save to CSV
    try:
        data = {
            "Ticker": [ticker],
            "Latest_Close": [latest_close],
            "Previous_Close": [previous_close],
            "Percent_Change": [f"{change}%"]
        }
        df = pd.DataFrame(data)
        data_dir = "C:/Users/anany/OneDrive/Desktop/Ananya/Raga_Ai_Agent/data"
        os.makedirs(data_dir, exist_ok=True)
        csv_path = f"{data_dir}/stock_data_{ticker}.csv"
        df.to_csv(csv_path, index=False)
        print(f"Saved CSV to {csv_path}")
    except Exception as e:
        print(f"Error saving CSV: {e}")

    return {
        "ticker": ticker,
        "latest_close": latest_close,
        "previous_close": previous_close,
        "percent_change": f"{change}%"
    }