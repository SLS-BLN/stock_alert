from config import load_config
from data_fetch import fetch_stock_data, fetch_news_articles
from utils import evaluate_stock_change
from sms import prepare_sms, send_sms

def run_alert_pipeline(config: dict) -> None:
    stock_data = fetch_stock_data(config)
    if not stock_data:
        print("No stock data available.")
        return

    alert_needed, pct_change = evaluate_stock_change(config, stock_data)
    if not alert_needed:
        print("Threshold not reached.")
        return

    messages = fetch_news_articles(config)
    sms_data = prepare_sms(config, messages, pct_change)
    if sms_data:
        send_sms(config["TWILIO_ACCOUNT_SID"], config["TWILIO_AUTH_TOKEN"], sms_data)

def main():
    config = load_config()
    run_alert_pipeline(config)

if __name__ == "__main__":
    main()