import pandas as pd

def get_atm_strike(spot_price, strike_step):
    return round(spot_price / strike_step) * strike_step


def filter_chain(chain_df, expiry):
    """
    Filters chain for a specific expiry
    """
    return chain_df[chain_df["expiry"] == expiry].copy()


def select_atm_options(chain_df, atm_strike):
    ce = chain_df[(chain_df["type"] == "CE") & (chain_df["strike"] == atm_strike)].iloc[0]
    pe = chain_df[(chain_df["type"] == "PE") & (chain_df["strike"] == atm_strike)].iloc[0]
    return ce, pe
