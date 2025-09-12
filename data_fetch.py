import requests
from typing import Dict, List, Tuple, Optional
from utils import extract_latest_prices

def fetch_stock_data(api_endpoint: str, api_key: str, symbol: str) -> Optional[Dict]:
    """Fetch stock data from Alpha Vantage API.

    Args:
        api_endpoint: Alpha Vantage API endpoint
        api_key: Alpha Vantage API key
        symbol: Stock symbol to fetch data for

    Returns:
        Stock data if successful, None otherwise

    TODO: Add support for different timeframes (weekly, monthly)
    TODO: Implement data validation and sanitization for symbol
    TODO: Add request timeout and retry logic
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "compact"
    }

    try:
        response = requests.get(api_endpoint, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check for API errors
        if "Error Message" in data or "Note" in data:
            return None

        if "Time Series (Daily)" not in data:
            return None

        return data
    except:
        return None

DEFAULT_PAGE_SIZE = 3  # TODO: Make configurable via .env or external config file

# TODO: Refactor API config parameters into a dataclass (e.g., NewsAPIConfig)
#       to improve readability, reduce parameter count, and support cleaner config management.
def fetch_news_articles(api_endpoint: str, api_key: str, company_name: str, page_size: int = DEFAULT_PAGE_SIZE) -> List[Tuple[str, str, str]]:
    """Fetch news articles related to the company.

    Args:
        api_endpoint: News API endpoint
        api_key: News API key
        company_name: Company name to search for
        page_size: Number of articles to return

    Returns:
        List of (title, url) tuples
    """
    params = {
        "apiKey": api_key,
        "q": company_name,
        "searchIn": "title",
        "pageSize": page_size,
        "language": "en"
    }

    try:
        response = requests.get(api_endpoint, params=params, timeout=10)
        response.raise_for_status()

        articles = response.json().get("articles", [])
        return [(article["title"], article["description"], article["url"])
                for article
                in articles
                if article.get("title") and article.get("description") and article.get("url")]
    except:
        return []