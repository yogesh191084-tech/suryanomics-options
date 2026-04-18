import csv
import os
from datetime import datetime

FILE_PATH = "logs/trades.csv"


def log_trade(trade):

    file_exists = os.path.isfile(FILE_PATH)

    with open(FILE_PATH, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "date","spot",
                "ce_strike","ce_entry","ce_sl","ce_target",
                "pe_strike","pe_entry","pe_sl","pe_target",
                "status","exit_ce","exit_pe","pnl"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d"),
            trade["spot"],

            trade["ce"]["strike"],
            trade["ce"]["entry"],
            trade["ce"]["sl"],
            trade["ce"]["target"],

            trade["pe"]["strike"],
            trade["pe"]["entry"],
            trade["pe"]["sl"],
            trade["pe"]["target"],

            "OPEN",
            "",
            "",
            ""
        ])