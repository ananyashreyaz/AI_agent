API Agent: Stock Data Retrieval
Overview
The API Agent is responsible for fetching real-time stock data using the yfinance library. It listens for POST requests containing stock ticker symbols, retrieves the latest and previous day’s closing prices, calculates the percentage change, and returns this information in a JSON response.

Endpoint: /get_stock_data
Method: POST
URL: http://127.0.0.1:8001/get_stock_data

Request Body
The request body must be a JSON object containing the stock ticker symbol.

Example Request:

{
  "ticker": "AAPL"
}

Response
The API responds with the latest stock data, including the latest close price, previous close price, and the percentage change.

Example Response:

{
  "ticker": "AAPL",
  "latest_close": 210.92,
  "previous_close": 198.53,
  "percent_change": "6.24 %"
}
Error Handling
If the provided ticker is invalid or there is no data available, the API will return an error message:

Example Error Response:


{
  "error": "Invalid ticker or no data available"
}
Dependencies
yfinance: For fetching stock data.

fastapi: For creating the API service.

pydantic: For data validation.

Running the API
To run the API, execute the following command:

uvicorn api_agent:app --reload
This will start the server on http://127.0.0.1:8001, and the /get_stock_data endpoint will be available for use.

