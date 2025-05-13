from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os
import glob

app = FastAPI()
class AnalysisRequest(BaseModel):
         ticker: str
         retrieved_context: list

def load_csv_data(ticker: str, data_dir: str = "C:/Users/anany/Desktop/raga_data"):
         stock_data = None
         earnings_data = None
         for csv_file in glob.glob(f"{data_dir}/*.csv"):
             try:
                 df = pd.read_csv(csv_file)
                 if f"stock_data_{ticker}.csv" in csv_file:
                     stock_data = df
                 elif f"earnings_data_{ticker}.csv" in csv_file:
                     earnings_data = df
             except Exception as e:
                 print(f"Error loading {csv_file}: {e}")
         return stock_data, earnings_data

@app.post("/analyze")
def analyze(request: AnalysisRequest):
         ticker = request.ticker
         retrieved_context = request.retrieved_context
         response = {"ticker": ticker, "risk_exposure": {}, "earnings_analysis": {}}

         # Load CSVs
         stock_data, earnings_data = load_csv_data(ticker)

         # Risk Exposure (hypothetical AUM and allocations)
         try:
             aum = 10_000_000  # $10M AUM
             allocations = {
                 "AAPL": 0.2,  # 20% of AUM
                 "TSLA": 0.15,
                 "2330.TW": 0.1,  # Asia tech
                 "005930.KS": 0.05  # Asia tech
             }
             allocation = allocations.get(ticker, 0.0)
             exposure = allocation * aum
             response["risk_exposure"] = {
                 "allocation_percent": f"{allocation*100}%",
                 "exposure_usd": round(exposure, 2),
                 "is_asia_tech": ticker in ["2330.TW", "005930.KS"]
             }
         except Exception as e:
             response["risk_exposure"] = {"error": str(e)}

         # Earnings Surprises
         try:
             if earnings_data is not None and not earnings_data.empty:
                 surprises = []
                 for _, row in earnings_data.iterrows():
                     actual_eps = float(row.get("actualEps", 0))
                     consensus_eps = float(row.get("consensusEps", 0))
                     surprise = actual_eps - consensus_eps
                     surprise_pct = (surprise / consensus_eps * 100) if consensus_eps else 0
                     surprises.append({
                         "date": row.get("date", "Unknown"),
                         "actual_eps": actual_eps,
                         "consensus_eps": consensus_eps,
                         "surprise": round(surprise, 2),
                         "surprise_percent": f"{round(surprise_pct, 2)}%"
                     })
                 response["earnings_analysis"] = surprises
             else:
                 response["earnings_analysis"] = {"error": "No earnings data available"}
         except Exception as e:
             response["earnings_analysis"] = {"error": str(e)}

         if not stock_data and not earnings_data and retrieved_context:
             response["from_context"] = retrieved_context[:3]  
         elif not retrieved_context:
             response["from_context"] = "No retrieved context available"

         return response

if __name__ == "__main__":
         import uvicorn
         uvicorn.run(app, host="0.0.0.0", port=8004)