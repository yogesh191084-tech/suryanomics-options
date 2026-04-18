import requests
import time

URL = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}


def get_option_chain():
    session = requests.Session()

    # Step 1: visit homepage (important for cookies)
    session.get("https://www.nseindia.com", headers=HEADERS)

    # Step 2: retry logic
    for _ in range(3):
        try:
            response = session.get(URL, headers=HEADERS, timeout=5)

            if response.status_code == 200:
                data = response.json()

                # SAFE CHECK
                if "records" in data:
                    return data

            time.sleep(1)

        except Exception:
            time.sleep(1)

    return None


def get_premium(strike, option_type="CE"):
    data = get_option_chain()

    if not data:
        return None

    try:
        for item in data["records"]["data"]:
            if item.get("strikePrice") == strike:

                if option_type == "CE" and item.get("CE"):
                    return item["CE"].get("lastPrice")

                if option_type == "PE" and item.get("PE"):
                    return item["PE"].get("lastPrice")

    except Exception:
        return None

    return None