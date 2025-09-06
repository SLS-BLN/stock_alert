from twilio.rest import Client
from utils import shorten_url, format_sms_message


def prepare_sms(config: dict, messages: list[tuple[str, str]], pct_change: float) -> dict | None:
    return build_sms(config, messages, pct_change)

def build_sms(config: dict, messages: list[tuple[str, str]], pct_change: float) -> dict | None:
    if not messages:
        return None

    trial_mode = config.get("TWILIO_TRIAL_MODE", "false").lower() == "true"

    if trial_mode:
        title, url = messages[0]
        short_url = shorten_url(url)
        body = format_sms_message(title, short_url, pct_change)
    else:
        body_lines = [
            format_sms_message(title, shorten_url(url), pct_change)
            for title, url in messages
        ]
        body = "\n".join(body_lines)

    return {
        "body": body,
        "from_": config["TWILIO_PHONE_NUMBER"],
        "to": config["MY_PHONE_NUMBER"]
    }

def send_sms(account_sid: str, auth_token: str, sms_data: dict) -> None:
    client = Client(account_sid, auth_token)
    message = client.messages.create(**sms_data)
    status = message.status
    if status in ["sent", "queued", "delivered"]:
        print(f"✅ SMS {status}: {message.sid}")
    else:
        print(f"❌ SMS failed: {status}")
        if message.error_code:
            print(f"Error code: {message.error_code}")
        if message.error_message:
            print(f"Error message: {message.error_message}")