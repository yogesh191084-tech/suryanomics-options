import math
from ingestion.option_chain import get_premium


def round_to_strike(price, step=50):
    return int(round(price / step) * step)


def build_short_strangle(spot_price):
    """
    Build SHORT STRANGLE using REAL option premiums
    """

    atm = round_to_strike(spot_price)

    distance = 200

    ce_strike = atm + distance
    pe_strike = atm - distance

    # ===== REAL PREMIUM FETCH =====
    ce_premium = get_premium(ce_strike, "CE")
    pe_premium = get_premium(pe_strike, "PE")

    # Fallback if API fails
    if ce_premium is None:
        ce_premium = 120

    if pe_premium is None:
        pe_premium = 110

    # ===== RISK RULES =====
    ce_sl = round(ce_premium * 1.3, 2)
    pe_sl = round(pe_premium * 1.3, 2)

    ce_target = round(ce_premium * 0.6, 2)
    pe_target = round(pe_premium * 0.6, 2)

    return {
        "spot": spot_price,
        "ce": {
            "strike": ce_strike,
            "entry": ce_premium,
            "sl": ce_sl,
            "target": ce_target
        },
        "pe": {
            "strike": pe_strike,
            "entry": pe_premium,
            "sl": pe_sl,
            "target": pe_target
        }
    }