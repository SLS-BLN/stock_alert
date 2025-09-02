import requests

from dotenv import dotenv_values
from functools import partial

load_config = partial(dotenv_values, ".env")


def main():
    config = load_config()
    url = config.get("API_ENDPOINT")
    params = {
        # TODO: make the function value dynamic
        "function": "TIME_SERIES_DAILY",
        "symbol": config.get("STOCK"),
        "apikey": config.get("API_KEY")
    }

    data = requests.get(url, params=params).json()

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
        print("Get News")
    else:
        print("Nothing")

if __name__ == "__main__":
    main()



