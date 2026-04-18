from ingestion.options_fetcher import fetch_options_chain
from ingestion.options_writer import write_options_chain

df = fetch_options_chain("NIFTY")
print(df.head())

write_options_chain(df)
print("Options snapshot saved. Rows:", len(df))
