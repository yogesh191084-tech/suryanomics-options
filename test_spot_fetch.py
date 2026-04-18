from ingestion.spot_fetcher import fetch_spot_5m

# NIFTY index symbol for yfinance
df = fetch_spot_5m("^NSEI")

print(df.tail())
