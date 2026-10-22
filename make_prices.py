
import pandas as pd
import yfinance as yf

tickers = ["SGOV", "IEF", "AGG", "VT"]
prices = {}

for ticker in tickers:
    data = yf.download(
        ticker,
        start="2021-09-01",
        end="2026-10-01",
        interval="1d",
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError(f"No prices downloaded for {ticker}")

    close = data["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    prices[ticker] = close.resample("ME").last()

df = pd.DataFrame(prices).dropna()
df.index.name = "Date"

if len(df) < 60:
    raise ValueError(
        f"Only {len(df)} months downloaded; check the data."
    )

df.to_csv("prices.csv")
print(f"SUCCESS! Saved {len(df)} months to prices.csv")
print(df.tail())
