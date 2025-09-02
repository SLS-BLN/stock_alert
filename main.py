import requests

from dotenv import dotenv_values
from functools import partial

load_config = partial(dotenv_values, ".env")


def main():
    config = load_config()

    alphavantage_url = config.get("ALPHAVANTAGE_API_ENDPOINT")
    alphavantage_params = {
        # TODO: make the function value dynamic
        "function": "TIME_SERIES_DAILY",
        "symbol": config.get("STOCK"),
        "apikey": config.get("ALPHAVANTAGE_API_KEY")
    }

    news_api_url = config.get("NEWS_API_ENDPOINT")
    news_api_params = {
        "apiKey": config.get("NEWS_API_KEY"),
        # TODO: names like "Tesla Inc." are not working" - search for a better solution
        "q": config.get("COMPANY_NAME")
    }


    data = requests.get(alphavantage_url, params=alphavantage_params).json()

    # Extract the daily time series
    time_series = data["Time Series (Daily)"]

    # Get all available dates sorted (the most recent first)
    dates = list(time_series.keys())

    latest_day = dates[0]
    previous_day = dates[1]  # The day before the latest trading day

    latest_close = float(time_series[latest_day]["4. close"])
    previous_close = float(time_series[previous_day]["4. close"])

    percentage_change = abs((latest_close - previous_close) / previous_close * 100)

    # TODO: replace magic number with a variable
    if percentage_change > 5:
        get_news = requests.get(news_api_url, params=news_api_params).json()
        # TODO: get the first 3 articles
        print(get_news)
        print("Get News")
    else:
        print("Nothing")

if __name__ == "__main__":
    main()



