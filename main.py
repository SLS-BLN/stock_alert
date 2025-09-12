import sys
from typing import Dict, Any

# TODO: Add proper logging setup instead of print statements
# TODO: Consider using a configuration management library like Pydantic for better type safety
from config import load_config
from data_fetch import fetch_stock_data, fetch_news_articles
from utils import evaluate_stock_change
from sms import prepare_sms, send_sms

# TODO: Add CLI or GUI interface for user interaction
# TODO: Consider adding back logging when needed for production use

def run_alert_pipeline(config: Dict[str, Any]) -> None:
    """Run the stock alert pipeline.

    Args:
        config: Application configuration
        
    TODO: Add retry mechanism for API calls with exponential backoff
    TODO: Add input validation for config parameters
    TODO: Consider making this function async for better performance with I/O operations
    """
    # Fetch stock data
    stock_data = fetch_stock_data(
        config["ALPHAVANTAGE_API_ENDPOINT"],
        config["ALPHAVANTAGE_API_KEY"],
        config["STOCK"]
    )

    if not stock_data:
        print("❌ No stock data available.")
        return

    # Check if price change exceeds threshold
    threshold = config["THRESHOLD"]
    alert_needed, pct_change = evaluate_stock_change(stock_data, threshold)

    if not alert_needed:
        print(f"ℹ️  Threshold not reached: {abs(pct_change):.2f}% (threshold: {threshold}%)")
        return

    print(f"📈 Significant price movement detected: {pct_change:+.2f}%")

    # Fetch news articles
    messages = fetch_news_articles(
        config["NEWS_API_ENDPOINT"],
        config["NEWS_API_KEY"],
        config["COMPANY_NAME"]
    )

    if not messages:
        print("ℹ️  No news articles found.")
        return

    # Prepare and send SMS
    sms_data = prepare_sms(config, messages, pct_change)
    if sms_data and send_sms(config["TWILIO_ACCOUNT_SID"], config["TWILIO_AUTH_TOKEN"], sms_data):
        print("✅ SMS alert sent successfully!")
    else:
        print("❌ Failed to send SMS alert.")

def main() -> None:
    """Main entry point for the stock alert application."""
    try:
        config = load_config()
        run_alert_pipeline(config)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()