import requests
from typing import Tuple

def calculate_percentage_change(latest: float, previous: float) -> float:
    """Calculate the percentage change between two values.
    
    Args:
        latest: Latest value
        previous: Previous value
        
    Returns:
        Percentage change as a float
        
    Raises:
        ValueError: If previous value is zero
    """
    if previous == 0:
        raise ValueError("Previous close cannot be zero.")
    return (latest - previous) / previous * 100

def is_threshold_reached(change: float, threshold: float) -> bool:
    """Check if the absolute change exceeds the threshold.
    
    Args:
        change: Percentage change
        threshold: Threshold to check against
        
    Returns:
        True if the absolute change exceeds the threshold, False otherwise
    """
    return abs(change) > threshold

def evaluate_stock_change(stock_data: dict, threshold: float) -> Tuple[bool, float]:
    """Evaluate if stock change exceeds threshold.
    
    Args:
        stock_data: Stock data containing daily prices
        threshold: Threshold percentage
        
    Returns:
        Tuple of (threshold_reached, percentage_change)
    """

    # TODO: duplicated logic with data_fetch.py
    time_series = stock_data["Time Series (Daily)"]
    sorted_dates = sorted(time_series.keys(), reverse=True)
    
    latest = float(time_series[sorted_dates[0]]["4. close"])
    previous = float(time_series[sorted_dates[1]]["4. close"])
    
    pct_change = calculate_percentage_change(latest, previous)
    return is_threshold_reached(pct_change, threshold), pct_change

def shorten_url(url: str) -> str:
    """Shorten a URL using TinyURL.
    
    Args:
        url: URL to shorten
        
    Returns:
        Shortened URL or original URL if shortening fails
    """
    try:
        response = requests.get(f"https://tinyurl.com/api-create.php?url={url}", timeout=5)
        response.raise_for_status()
        return response.text
    except:
        return url

def format_sms_message(title: str, url: str, pct_change: float) -> str:
    """Format an SMS message with stock change information.
    
    Args:
        title: Article title
        url: Article URL
        pct_change: Percentage change in stock price
        
    Returns:
        Formatted message string
    """
    triangle = "🟢▲" if pct_change > 0 else "🔴▼"
    pct_text = f"{triangle} {abs(pct_change):.2f}%"
    return f"{pct_text}\n{title} {url}"