def calculate_lots(capital, max_loss_per_lot, lot_size, max_risk_pct):
    """
    Determines number of lots based on max allowable risk
    """
    max_risk_amount = capital * max_risk_pct

    if max_loss_per_lot <= 0:
        return 0

    lots = int(max_risk_amount // (max_loss_per_lot * lot_size))
    return max(lots, 0)
