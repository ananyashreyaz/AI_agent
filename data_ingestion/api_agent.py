import yfinance as yf
from fastapi import FastAPI
from pydantic import BaseModel

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

    return {
        "ticker": ticker,
        "latest_close": latest_close,
        "previous_close": previous_close,
        "percent_change": f"{change} %"
    }
