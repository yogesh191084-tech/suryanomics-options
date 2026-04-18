import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/spot_5m.csv")

def write_spot_data(df):
    """
    Writes spot data to CSV with deduplication and bad-line protection
    """
    if DATA_PATH.exists():
        existing = pd.read_csv(
            DATA_PATH,
            parse_dates=["datetime"],
            on_bad_lines="skip"
        )
        df = pd.concat([existing, df], ignore_index=True)
        df = df.drop_duplicates(subset=["datetime"]).sort_values("datetime")

    df.to_csv(DATA_PATH, index=False)
