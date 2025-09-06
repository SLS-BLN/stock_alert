from dotenv import dotenv_values

def load_config(path: str = ".env") -> dict:
    config = dotenv_values(path)
    required_keys = [
        "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN",
        "TWILIO_PHONE_NUMBER", "MY_PHONE_NUMBER",
        "ALPHAVANTAGE_API_ENDPOINT", "ALPHAVANTAGE_API_KEY",
        "NEWS_API_ENDPOINT", "NEWS_API_KEY",
        "STOCK", "COMPANY_NAME", "THRESHOLD"
    ]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")
    return config