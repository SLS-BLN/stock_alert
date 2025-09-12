from pathlib import Path
from typing import Dict, Any
from dotenv import dotenv_values

def load_config(path: str = ".env") -> Dict[str, Any]:
    """Load configuration from .env file.

    Args:
        path: Path to the .env file

    Returns:
        Dictionary with configuration values

    Raises:
        FileNotFoundError: If .env file is not found
        ValueError: If required configuration is missing
    """
    env_path = Path(path)
    if not env_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {env_path}")

    config = dotenv_values(env_path)

    # Validate required keys
    required_keys = [
        "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN",
        "TWILIO_PHONE_NUMBER", "MY_PHONE_NUMBER",
        "ALPHAVANTAGE_API_ENDPOINT", "ALPHAVANTAGE_API_KEY",
        "NEWS_API_ENDPOINT", "NEWS_API_KEY",
        "STOCK", "COMPANY_NAME", "THRESHOLD"
    ]

    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ValueError(f"Missing required configuration keys: {', '.join(missing_keys)}")

    # Convert threshold to float
    try:
        config["THRESHOLD"] = float(config["THRESHOLD"])
    except ValueError:
        raise ValueError("THRESHOLD must be a number")

    # Convert trial mode to boolean
    config["TWILIO_TRIAL_MODE"] = config.get("TWILIO_TRIAL_MODE", "false").lower() == "true"

    return config