from twilio.rest import Client
from typing import Dict, List, Tuple, Optional
from utils import shorten_url, format_sms_message

def prepare_sms(
    config: Dict[str, any],
    messages: List[Tuple[str, str]],
    pct_change: float
) -> Optional[Dict[str, str]]:
    """Prepare SMS message content.
    
    Args:
        config: Application configuration
        messages: List of (title, url) tuples
        pct_change: Percentage change in stock price
        
    Returns:
        Dictionary with 'to', 'from_', and 'body' keys if successful, None otherwise
    """
    if not messages:
        return None
    
    # In trial mode, only send the first message
    if config.get("TWILIO_TRIAL_MODE", False):
        title, url = messages[0]
        short_url = shorten_url(url)
        body = format_sms_message(title, short_url, pct_change)
    else:
        body_lines = [
            format_sms_message(title, shorten_url(url), pct_change)
            for title, url in messages
        ]
        body = "\n\n".join(body_lines)
    
    return {
        "to": config["MY_PHONE_NUMBER"],
        "from_": config["TWILIO_PHONE_NUMBER"],
        "body": body
    }

def send_sms(account_sid: str, auth_token: str, sms_data: Dict[str, str]) -> bool:
    """Send an SMS message using Twilio.
    
    Args:
        account_sid: Twilio account SID
        auth_token: Twilio auth token
        sms_data: Dictionary containing 'to', 'from_', and 'body' keys
        
    Returns:
        True if message was sent successfully, False otherwise
    """
    try:
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            to=sms_data["to"],
            from_=sms_data["from_"],
            body=sms_data["body"]
        )
        
        return message.status in ["sent", "queued", "delivered"]
    except Exception:
        return False