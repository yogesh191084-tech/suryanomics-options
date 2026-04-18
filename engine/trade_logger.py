import csv
import os
from datetime import datetime

LOG_FILE = "logs/trades.csv"


def log_trade(trade):

    os.makedirs("logs", exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "date",
                "status",
                "spot",

                "ce_strike", "ce_entry", "ce_sl", "ce_target",
                "pe_strike", "pe_entry", "pe_sl", "pe_target",

                "exit_ce", "exit_pe", "pnl", "exit_reason"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d"),
            "OPEN",
            trade["spot"],

            trade["ce"]["strike"],
            trade["ce"]["entry"],
            trade["ce"]["sl"],
            trade["ce"]["target"],

            trade["pe"]["strike"],
            trade["pe"]["entry"],
            trade["pe"]["sl"],
            trade["pe"]["target"],

            "", "", "", ""
        ])

    print("Trade saved correctly")