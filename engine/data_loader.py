import pandas as pd

def load_spot(path):
    return pd.read_csv(path, parse_dates=["datetime"])

def load_options(path):
    return pd.read_csv(path, parse_dates=["datetime"])
