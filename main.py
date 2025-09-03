import requests

from dotenv import dotenv_values
from functools import partial

load_config = partial(dotenv_values, ".env")

def get_stock_data(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_percentage_change(latest_close: float, previous_close: float) -> float:
    return abs((latest_close - previous_close) / previous_close * 100)

def is_percentage_threshold_reached(percentage_change: float, threshold: float) -> bool:
    return percentage_change > threshold

def extract_latest_prices(data: dict) -> tuple[float, float]:
    time_series = data["Time Series (Daily)"]
    dates = sorted(time_series.keys(), reverse=True)
    latest_close = float(time_series[dates[0]]["4. close"])
    previous_close = float(time_series[dates[1]]["4. close"])
    return latest_close, previous_close

def get_news(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        news_data = response.json()
        return news_data.get("articles", [])[:3]
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

def main():
    config = load_config()

    stock_data = get_stock_data(
        config["ALPHAVANTAGE_API_ENDPOINT"],
        {
            "function": "TIME_SERIES_DAILY",
            "symbol": config["STOCK"],
            "apikey": config["ALPHAVANTAGE_API_KEY"]
        }
    )

    if not stock_data:
        return

    latest, previous = extract_latest_prices(stock_data)
    pct_change = calculate_percentage_change(latest, previous)

    if is_percentage_threshold_reached(pct_change, float(config["THRESHOLD"])):
        articles = get_news(
            config["NEWS_API_ENDPOINT"],
            {"apiKey": config["NEWS_API_KEY"], "q": config["COMPANY_NAME"]}
        )
        for article in articles:
            print(article["title"], article["url"])
    else:
        print("Nothing")

if __name__ == "__main__":
    main()



