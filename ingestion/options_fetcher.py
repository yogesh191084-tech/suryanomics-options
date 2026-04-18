import requests
import pandas as pd
from datetime import datetime

NSE_URL = "https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
    "Connection": "keep-alive",
}

def fetch_options_chain(symbol="NIFTY"):
    """
    Fetch options chain snapshot from NSE (defensive)
    """
    session = requests.Session()
    session.headers.update(HEADERS)

    # Warm-up (MANDATORY for NSE)
    home = session.get("https://www.nseindia.com", timeout=10)
    if home.status_code != 200:
        raise RuntimeError("NSE homepage not reachable")

    response = session.get(NSE_URL.format(symbol=symbol), timeout=10)

    # Validate response
    if response.status_code != 200:
        raise RuntimeError(f"NSE API failed: {response.status_code}")

    try:
        data = response.json()
    except Exception:
        raise RuntimeError("NSE did not return JSON (blocked / throttled)")

    # Defensive schema check
    if "records" not in data or "data" not in data["records"]:
        raise RuntimeError(
            f"NSE schema unexpected. Keys received: {list(data.keys())}"
        )

    records = data["records"]["data"]

    rows = []
    snapshot_time = datetime.now()

    for item in records:
        expiry = item.get("expiryDate")
        strike = item.get("strikePrice")

        if "CE" in item:
            ce = item["CE"]
            rows.append({
                "datetime": snapshot_time,
                "symbol": ce.get("identifier"),
                "expiry": expiry,
                "strike": strike,
                "type": "CE",
                "ltp": ce.get("lastPrice"),
                "iv": ce.get("impliedVolatility"),
                "delta": ce.get("delta"),
                "oi": ce.get("openInterest"),
            })

        if "PE" in item:
            pe = item["PE"]
            rows.append({
                "datetime": snapshot_time,
                "symbol": pe.get("identifier"),
                "expiry": expiry,
                "strike": strike,
                "type": "PE",
                "ltp": pe.get("lastPrice"),
                "iv": pe.get("impliedVolatility"),
                "delta": pe.get("delta"),
                "oi": pe.get("openInterest"),
            })

    if not rows:
        raise RuntimeError("No option rows parsed — NSE response empty")

    return pd.DataFrame(rows)
