from fastapi import FastAPI
from pydantic import BaseModel
import requests
import re
from voice_agent import speak  #
app = FastAPI()

class QueryRequest(BaseModel):
    query: str

def extract_ticker(query: str) -> str:
    ticker_pattern = r'\b[A-Z]{1,5}\b(?:\.[A-Z]{1,2})?'
    match = re.search(ticker_pattern, query.upper())
    return match.group(0) if match else None

@app.post("/process_query")
def process_query(request: QueryRequest):
    query = request.query.lower()
    ticker = extract_ticker(query)
    if not ticker:
        return {"error": "No valid ticker found in query"}

    response_data = {}

   
    try:
        retriever_response = requests.post(
            "http://localhost:8002/retrieve",
            json={"query": query}
        )
        retriever_data = retriever_response.json()
        response_data["retrieved_context"] = retriever_data.get("results", retriever_data.get("error", "No retrieved data"))
    except Exception as e:
        response_data["retrieved_context"] = f"Retriever error: {str(e)}"

    # Analysis Agent
    if any(k in query for k in ["risk", "exposure", "analyze", "analysis", "earnings analysis"]):
        try:
            analysis_response = requests.post(
                "http://localhost:8004/analyze",
                json={
                    "ticker": ticker,
                    "retrieved_context": response_data["retrieved_context"]
                }
            )
            response_data["analysis"] = analysis_response.json()
        except Exception as e:
            response_data["analysis"] = f"Error fetching analysis: {str(e)}"

    # API Agent - Stock Data
    if any(k in query for k in ["stock", "price", "market"]):
        try:
            stock_response = requests.post(
                "http://localhost:8001/get_stock_data",
                json={"ticker": ticker}
            )
            response_data["stock_data"] = stock_response.json()
        except Exception as e:
            response_data["stock_data"] = f"Error fetching stock data: {str(e)}"

    # Scraping Agent - Earnings
    if "earnings" in query and "analysis" not in query:
        try:
            earnings_response = requests.post(
                "http://localhost:8003/get_earnings",
                json={"ticker": ticker}
            )
            response_data["earnings_data"] = earnings_response.json()
        except Exception as e:
            response_data["earnings_data"] = f"Error fetching earnings: {str(e)}"

    # Scraping Agent - SEC Filings
    if "filings" in query:
        try:
            filings_response = requests.post(
                "http://localhost:8003/get_filings",
                json={"ticker": ticker}
            )
            response_data["filings_data"] = filings_response.json()
        except Exception as e:
            response_data["filings_data"] = f"Error fetching filings: {str(e)}"

    # Scraping Agent - News
    if "news" in query:
        try:
            news_response = requests.post(
                "http://localhost:8003/get_news",
                json={"ticker": ticker}
            )
            response_data["news_data"] = news_response.json()
        except Exception as e:
            response_data["news_data"] = f"Error fetching news: {str(e)}"

    # Language Agent - Final Summary
    try:
        language_response = requests.post(
            "http://localhost:8005/generate_narrative",
            json={"query": query}
        )
        response_data["narrative"] = language_response.json().get("narrative", "No narrative returned.")
    except Exception as e:
        response_data["narrative"] = f"Language agent error: {str(e)}"

    # Voice Agent - Speak key insights
    try:
        speakable = []

        if "narrative" in response_data:
            speakable.append(response_data["narrative"])

        if isinstance(response_data.get("retrieved_context"), list):
            for item in response_data["retrieved_context"]:
                speakable.append(item["text"])

        if "analysis" in response_data:
            speakable.append(str(response_data["analysis"]))

        if "stock_data" in response_data:
            speakable.append(str(response_data["stock_data"]))

        if "earnings_data" in response_data:
            for e in response_data["earnings_data"]:
                speakable.append(e.get("title", str(e)))

        if "news_data" in response_data:
            for n in response_data["news_data"]:
                speakable.append(n.get("title", str(n)))

        if "filings_data" in response_data:
            for f in response_data["filings_data"]:
                speakable.append(f.get("title", str(f)))

        combined_text = ". ".join(speakable[:5])  # Limit to 5 key points
        speak(combined_text)

    except Exception as e:
        print(f"Voice agent error: {str(e)}")

    return response_data
