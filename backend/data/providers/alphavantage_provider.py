import requests

class AlphaVantageProvider():
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_dividend_data(self, stock_ticker):
        url = f'https://www.alphavantage.co/query?function=DIVIDENDS&symbol={stock_ticker}&apikey={self.api_key}'
        r = requests.get(url)

        if r.status_code != 200:
            raise RuntimeError(f"API call failed: {r.status_code}")
        try:
            json_data = r.json()
        except ValueError:
            raise RuntimeError("Failed to parse JSON")
        
        return json_data