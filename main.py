import requests

from twilio.rest import Client
from dotenv import dotenv_values
from functools import partial

load_config = partial(dotenv_values, ".env")

def get_stock_data(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Alpha Vantage sometimes returns "Error Message" or "Note" instead of data
        if "Error Message" in data:
            print(f"Alpha Vantage error: {data['Error Message']}")
            return None
        if "Note" in data:
            print(f"Alpha Vantage notice: {data['Note']}")
            return None
        if "Time Series (Daily)" not in data:
            print(f"Unexpected API response: {data}")
            return None

        return data

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_percentage_change(latest_close: float, previous_close: float) -> float:
    """
    Returns the signed percentage change from previous_close to latest_close.
    "Positive" means the price went up, "negative" means the price went down.
    """
    if previous_close == 0:
        raise ValueError("Previous close cannot be zero.")
    return (latest_close - previous_close) / previous_close * 100


def is_percentage_threshold_reached(percentage_change: float, threshold: float) -> bool:
    """
    Returns True if the absolute percentage change exceeds the threshold.
    Works for both positive (up) and negative (down) changes.
    """
    return abs(percentage_change) > threshold

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

def shorten_url(url):
    try:
        response = requests.get(f"https://tinyurl.com/api-create.php?url={url}")
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error shortening URL: {e}")
        return url  # fallback to original

# TODO: Make SMS body customizable via config or template system.
def build_sms(config, messages, pct_change):
    """
    Build SMS payload with colored triangle and percentage change.
    Uses only the first article in trial mode.
    """
    if not messages:
        return None

    trial_mode = config.get("TWILIO_TRIAL_MODE", "false").lower() == "true"

    # Choose emoji based on price movement
    if pct_change > 0:
        indicator = "🟢▲"
    else:
        indicator = "🔴▼"

    pct_text = f"{indicator} {pct_change:.2f}%"

    if trial_mode:
        title, url = messages[0]
        short_url = shorten_url(url)

        max_title_length = 100
        if len(title) > max_title_length:
            title = title[:max_title_length - 3] + "..."

        body_text = f"{pct_text}\n{title} {short_url}"

    else:
        article_lines = []
        for title, url in messages:
            short_url = shorten_url(url)
            article_lines.append(f"{title} {short_url}")
        body_text = f"{pct_text}\n" + "\n".join(article_lines)

    print(f"SMS length: {len(body_text)} characters")

    return {
        "body": body_text,
        "from_": config["TWILIO_PHONE_NUMBER"],
        "to": config["MY_PHONE_NUMBER"]
    }

# TODO: Separate Twilio client creation from message sending for better testability.
def send_sms(account_sid, auth_token, sms_data):
    client = Client(account_sid, auth_token)
    return client.messages.create(**sms_data)


def main():
    config = load_config()

    account_sid = config["TWILIO_ACCOUNT_SID"]
    auth_token = config["TWILIO_AUTH_TOKEN"]

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
        messages = []
        articles = get_news(
            config["NEWS_API_ENDPOINT"],
            {"apiKey": config["NEWS_API_KEY"], "q": config["COMPANY_NAME"]}
        )
        for article in articles:
            messages.append([article["title"], article["url"]])

        sms_data = build_sms(config, messages, pct_change)
        if not sms_data:
            return
        message = send_sms(account_sid, auth_token, sms_data)

        # Check status and provide meaningful feedback
        status = message.status
        if status in ["sent", "queued", "delivered"]:
            print(f"✅ SMS successfully {status}: {message.sid}")
        else:
            print(f"❌ SMS failed with status '{status}'")
            if message.error_code:
                print(f"Twilio error code: {message.error_code}")
            if message.error_message:
                print(f"Twilio error message: {message.error_message}")


    else:
        print("Nothing")

if __name__ == "__main__":
    main()



