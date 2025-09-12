from twilio.rest import Client
from typing import Dict, List, Tuple, Optional
from utils import shorten_url, format_sms_message

def prepare_sms(
    config: Dict[str, any],
    messages: List[Tuple[str, str, str]],
    pct_change: float
) -> Optional[Dict[str, str]]:
    """Prepare SMS message content.

    Args:
        config: Application configuration
        messages: List of (title, description, url) tuples
        pct_change: Percentage change in stock price

    Returns:
        Dictionary with 'to', 'from_', and 'body' keys if successful, None otherwise
    """

    if not messages:
        return None

    symbol = config.get("STOCK")

    # In trial mode, only send the first message (max 160 chars)
    if config.get("TWILIO_TRIAL_MODE", True):
        title, _, url = messages[0]  # Unpack all three values but ignore description
        short_url = shorten_url(url)
        # Format without emojis and description to save space
        change_direction = '+' if pct_change >= 0 else '-'
        body = f"{symbol} {change_direction}{abs(pct_change):.1f}%\n{title}\n{short_url}"
        # Ensure message is within 160 characters
        if len(body) > 160:
            # Truncate title if needed, leaving room for the rest
            max_title_length = 160 - (len(symbol) + 10 + len(short_url) + 3)  # +3 for newlines and %
            if max_title_length > 0:
                title = title[:max_title_length - 3] + '...' if len(title) > max_title_length else title
                body = f"{symbol} {change_direction}{abs(pct_change):.1f}%\n{title}\n{short_url}"
    # In production mode, send all messages
    else:
        # Add header with symbol and percentage change
        change_emoji = "🟢▲" if pct_change >= 0 else "🔴▼"
        header = f"{symbol} {change_emoji} {abs(pct_change):.2f}%\n\n"

        message_lines = []
        for title, description, url in messages:
            short_url = shorten_url(url)
            # Format without symbol and pct_change since they're in the header
            message = f"{title}\n{description}\n{short_url}"
            message_lines.append(message)

        # Combine header with all messages
        body = header + "\n\n".join(message_lines)
        print(body)



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