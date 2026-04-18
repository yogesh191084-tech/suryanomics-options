import yfinance as yf
import pandas as pd


# Map logical symbols to Yahoo symbols
YAHOO_SYMBOL_MAP = {
    "NIFTY": "^NSEI",
    # Future:
    # "BANKNIFTY": "^NSEBANK"
}


def fetch_spot_5m(symbol):
    """
    Fetch last 5 days of 5-minute spot data using Yahoo Finance
    """
    if symbol not in YAHOO_SYMBOL_MAP:
        raise ValueError(f"Unsupported symbol: {symbol}")

    yahoo_symbol = YAHOO_SYMBOL_MAP[symbol]

    ticker = yf.Ticker(yahoo_symbol)
    df = ticker.history(period="5d", interval="5m")

    if df is None or df.empty:
        raise ValueError("No data received from yfinance")

    df = df.reset_index()

    df = df.rename(columns={
        "Datetime": "datetime",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    df["datetime"] = pd.to_datetime(df["datetime"])

    return df[["datetime", "open", "high", "low", "close", "volume"]]
