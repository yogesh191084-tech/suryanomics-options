import requests

BOT_TOKEN = "8702505358:AAFCjzcXy7i07y51TD5GGxY0QZMb9VIOofM"
CHAT_ID = "-1003967988003"

def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        print(response.text)   # 👈 IMPORTANT (so you see result)
        return response.json()
    except Exception as e:
        print("Telegram Error:", e)


if __name__ == "__main__":
    send_message("🚀 Suryanomics Options is LIVE")