import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/options_chain.csv")

def write_options_chain(df):
    """
    Appends options chain snapshots safely
    """
    if DATA_PATH.exists():
        existing = pd.read_csv(DATA_PATH, parse_dates=["datetime"], on_bad_lines="skip")
        df = pd.concat([existing, df], ignore_index=True)

    df.to_csv(DATA_PATH, index=False)
