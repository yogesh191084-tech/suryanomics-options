def build_bull_call_spread(chain, atm, step):
    buy = chain[(chain.type=="CE") & (chain.strike==atm)].iloc[0]
    sell = chain[(chain.type=="CE") & (chain.strike==(atm + step))].iloc[0]

    return {
        "strategy": "BULL_CALL_SPREAD",
        "legs": [
            {"action": "BUY", "symbol": buy.symbol, "price": buy.ltp},
            {"action": "SELL", "symbol": sell.symbol, "price": sell.ltp}
        ],
        "max_loss": buy.ltp - sell.ltp
    }


def build_bear_put_spread(chain, atm, step):
    buy = chain[(chain.type=="PE") & (chain.strike==atm)].iloc[0]
    sell = chain[(chain.type=="PE") & (chain.strike==(atm - step))].iloc[0]

    return {
        "strategy": "BEAR_PUT_SPREAD",
        "legs": [
            {"action": "BUY", "symbol": buy.symbol, "price": buy.ltp},
            {"action": "SELL", "symbol": sell.symbol, "price": sell.ltp}
        ],
        "max_loss": buy.ltp - sell.ltp
    }


def build_short_strangle(chain):
    ce = chain[(chain.type=="CE") & (chain.delta < 0.25)].iloc[0]
    pe = chain[(chain.type=="PE") & (chain.delta > -0.25)].iloc[-1]

    credit = ce.ltp + pe.ltp

    return {
        "strategy": "SHORT_STRANGLE",
        "legs": [
            {"action": "SELL", "symbol": ce.symbol, "price": ce.ltp},
            {"action": "SELL", "symbol": pe.symbol, "price": pe.ltp}
        ],
        "credit": credit
    }
