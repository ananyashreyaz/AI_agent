import requests
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()

     # Updated FMP API key
FMP_API_KEY = "API_KEY"

class TickerRequest(BaseModel):
         ticker: str

@app.post("/get_earnings")
def get_earnings(request: TickerRequest):
         url = f"https://financialmodelingprep.com/api/v3/earnings-surprises/{request.ticker}?apikey={FMP_API_KEY}"
         response = requests.get(url)
         data = response.json()
         result = data[:3] if isinstance(data, list) else data

         # Save to CSV
         try:
             if isinstance(result, list) and result:
                 df = pd.DataFrame(result)
                 data_dir = "C:/Users/anany/OneDrive/Desktop/Ananya/Raga_Ai_Agent/data"
                 os.makedirs(data_dir, exist_ok=True)
                 csv_path = f"{data_dir}/earnings_data_{request.ticker}.csv"
                 df.to_csv(csv_path, index=False)
                 print(f"Saved CSV to {csv_path}")
             else:
                 print(f"No valid earnings data for {request.ticker}")
         except Exception as e:
             print(f"Error saving CSV: {e}")

         return result

@app.post("/get_filings")
def get_filings(request: TickerRequest):
         url = f"https://financialmodelingprep.com/api/v3/sec_filings/{request.ticker}?apikey={FMP_API_KEY}"
         response = requests.get(url)
         data = response.json()
         result = data[:3] if isinstance(data, list) else data

         # Save to CSV
         try:
             if isinstance(result, list) and result:
                 df = pd.DataFrame(result)
                 data_dir = "C:/Users/anany/OneDrive/Desktop/Ananya/Raga_Ai_Agent/data"
                 os.makedirs(data_dir, exist_ok=True)
                 csv_path = f"{data_dir}/filings_data_{request.ticker}.csv"
                 df.to_csv(csv_path, index=False)
                 print(f"Saved CSV to {csv_path}")
             else:
                 print(f"No valid filings data for {request.ticker}")
         except Exception as e:
             print(f"Error saving CSV: {e}")

         return result

@app.post("/get_news")
def get_news(request: TickerRequest):
         url = f"https://financialmodelingprep.com/api/v3/stock_news?tickers={request.ticker}&limit=3&apikey={FMP_API_KEY}"
         response = requests.get(url)
         data = response.json()

         # Save to CSV
         try:
             if isinstance(data, list) and data:
                 df = pd.DataFrame(data)
                 data_dir = "C:/Users/anany/OneDrive/Desktop/Ananya/Raga_Ai_Agent/data"
                 os.makedirs(data_dir, exist_ok=True)
                 csv_path = f"{data_dir}/news_data_{request.ticker}.csv"
                 df.to_csv(csv_path, index=False)
                 print(f"Saved CSV to {csv_path}")
             else:
                 print(f"No valid news data for {request.ticker}")
         except Exception as e:
             print(f"Error saving CSV: {e}")

         return data