import requests

class TwelveProvider():
    def __init__(self, api_key: str):
        self.api_key = api_key

    # 800 lookups per day
    def get_closing_prices(self, stock_ticker, num_days=None) -> list[tuple[str, float]]:
        num_days_text = f'&outputsize={num_days}' if num_days is not None else ''
        url = f'https://api.twelvedata.com/time_series?symbol={stock_ticker}{num_days_text}&interval=1day&apikey={self.api_key}'

        r = requests.get(url)

        if r.status_code != 200:
            raise RuntimeError(f"API call failed: {r.status_code}")
        try:
            json_data = r.json()
        except ValueError:
            raise RuntimeError("Failed to parse JSON")
        
        price_data = json_data['values']

        closing_price_data = []

        for row in price_data:
            date = row['datetime']
            closing_price = float(row['close'])
            closing_price_data.append((date, closing_price))
        
        # Sort by date (oldest to newest)
        closing_price_data.sort(key=lambda x: x[0])

        return closing_price_data
