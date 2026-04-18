from ingestion.spot_fetcher import fetch_spot_5m
from ingestion.spot_writer import write_spot_data

df = fetch_spot_5m("^NSEI")
write_spot_data(df)

print("Spot data written. Rows:", len(df))
