import requests
import os

# 🔐 Use ENV variables (GitHub safe)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(message):

    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram config missing")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
        # ❌ Removed parse_mode (fixes all markdown errors)
    }

    try:
        response = requests.post(url, json=payload)

        # Debug output
        print("Telegram Response:", response.text)

        return response.json()

    except Exception as e:
        print("Telegram Error:", e)


# 🔧 LOCAL TEST
if __name__ == "__main__":
    send_message("🚀 Suryanomics Options is LIVE")