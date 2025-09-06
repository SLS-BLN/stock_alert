import requests
from data_fetch import extract_latest_prices

# TODO: Move reusable formatting or validation functions here
# TODO: Add docstrings to clarify utility function purposes
def calculate_percentage_change(latest: float, previous: float) -> float:
    if previous == 0:
        raise ValueError("Previous close cannot be zero.")
    return (latest - previous) / previous * 100

def is_threshold_reached(change: float, threshold: float) -> bool:
    return abs(change) > threshold

def evaluate_stock_change(config: dict, stock_data: dict) -> tuple[bool, float]:
    latest, previous = extract_latest_prices(stock_data)
    pct_change = calculate_percentage_change(latest, previous)
    threshold = float(config["THRESHOLD"])
    return is_threshold_reached(pct_change, threshold), pct_change

def shorten_url(url: str) -> str:
    try:
        response = requests.get(f"https://tinyurl.com/api-create.php?url={url}")
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return url

def format_sms_message(title: str, url: str, pct_change: float) -> str:
    triangle = "🟢▲" if pct_change > 0 else "🔴▼"
    pct_text = f"{triangle} {pct_change:.2f}%"
    return f"{pct_text}\n{title} {url}"