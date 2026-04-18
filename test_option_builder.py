import pandas as pd
from strategies.builders import build_bull_call_spread
from engine.options_chain import get_atm_strike

# Fake spot
spot = 22560
step = 50

atm = get_atm_strike(spot, step)

# Simulated options chain
data = [
    {"symbol":"NIFTY22550CE","strike":22550,"type":"CE","ltp":120,"delta":0.55},
    {"symbol":"NIFTY22600CE","strike":22600,"type":"CE","ltp":80,"delta":0.35},
    {"symbol":"NIFTY22550PE","strike":22550,"type":"PE","ltp":90,"delta":-0.45},
    {"symbol":"NIFTY22500PE","strike":22500,"type":"PE","ltp":70,"delta":-0.30},
]

chain = pd.DataFrame(data)

trade = build_bull_call_spread(chain, atm, step)
print(trade)
