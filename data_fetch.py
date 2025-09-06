import requests

# TODO: Add error handling for failed API requests (e.g., retries, timeouts)
# TODO: Cache responses to reduce redundant API calls

def get_stock_data(url: str, params: dict) -> dict | None:
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "Error Message" in data or "Note" in data or "Time Series (Daily)" not in data:
            return None
        return data
    except requests.RequestException:
        return None

def fetch_stock_data(config: dict) -> dict | None:
    return get_stock_data(
        config["ALPHAVANTAGE_API_ENDPOINT"],
        {
            "function": "TIME_SERIES_DAILY",
            "symbol": config["STOCK"],
            "apikey": config["ALPHAVANTAGE_API_KEY"]
        }
    )

# NOTE: This function is currently specific to Alpha Vantage's response format.
# If support for multiple stock APIs is added in the future, consider moving this
# to utils.py and generalizing it as a reusable price parser.
def extract_latest_prices(data: dict) -> tuple[float, float]:
    time_series = data["Time Series (Daily)"]
    dates = sorted(time_series.keys(), reverse=True)
    latest = float(time_series[dates[0]]["4. close"])
    previous = float(time_series[dates[1]]["4. close"])
    return latest, previous

def get_news(url: str, params: dict) -> list[tuple[str, str]]:
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])[:3]
        return [(a["title"], a["url"]) for a in articles]
    except requests.RequestException:
        return []

def fetch_news_articles(config: dict) -> list[tuple[str, str]]:
    return get_news(
        config["NEWS_API_ENDPOINT"],
        {"apiKey": config["NEWS_API_KEY"], "q": config["COMPANY_NAME"]}
    )