import requests
from typing import Dict, List, Tuple, Optional

def fetch_stock_data(api_endpoint: str, api_key: str, symbol: str) -> Optional[Dict]:
    """Fetch stock data from Alpha Vantage API.
    
    Args:
        api_endpoint: Alpha Vantage API endpoint
        api_key: Alpha Vantage API key
        symbol: Stock symbol to fetch data for
        
    Returns:
        Stock data if successful, None otherwise
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

def extract_latest_prices(stock_data: Dict) -> Tuple[float, float]:
    """Extract latest and previous day's closing prices.
    
    Args:
        stock_data: Stock data from Alpha Vantage API
        
    Returns:
        Tuple of (latest_price, previous_price)
    """
    time_series = stock_data["Time Series (Daily)"]
    sorted_dates = sorted(time_series.keys(), reverse=True)
    
    latest = float(time_series[sorted_dates[0]]["4. close"])
    previous = float(time_series[sorted_dates[1]]["4. close"])
    
    return latest, previous

def fetch_news_articles(api_endpoint: str, api_key: str, company_name: str) -> List[Tuple[str, str]]:
    """Fetch news articles related to the company.
    
    Args:
        api_endpoint: News API endpoint
        api_key: News API key
        company_name: Company name to search for
        
    Returns:
        List of (title, url) tuples
    """
    params = {
        "apiKey": api_key,
        "q": company_name,
        "pageSize": 3,
        "language": "en"
    }
    
    try:
        response = requests.get(api_endpoint, params=params, timeout=10)
        response.raise_for_status()
        
        articles = response.json().get("articles", [])
        return [(a["title"], a["url"]) for a in articles if a.get("title") and a.get("url")]
    except:
        return []