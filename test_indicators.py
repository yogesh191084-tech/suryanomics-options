import pandas as pd
from indicators.trend import add_trend_indicators

df = pd.DataFrame({
    "close": range(1, 50),
    "high": range(2, 51),
    "low": range(0, 49)
})

df = add_trend_indicators(df)
print(df.tail())
