# AI Trading Signal Engine

**Author:** Sam Shaikh · [github.com/samshai5](https://github.com/samshai5)  
**Stack:** Python · Yahoo Finance API · NewsAPI · Pandas · NumPy  
**Status:** ✅ Live — pulls real market data  

---

## Overview

A Python-based **AI trading signal engine** that fetches real-time stock prices, runs technical analysis across multiple indicators, and generates **BUY / SELL / HOLD signals** with plain-English explanations for each decision.

Built for educational and portfolio purposes — demonstrates real-world skills in API integration, data analysis, algorithmic logic, object-oriented programming, and financial data processing.

---

## Why This Project

Most trading apps are black boxes — they give you a signal but never explain why. This engine shows its work. Every BUY or SELL signal comes with a scored breakdown of exactly which indicators triggered it, why the score pushed in that direction, and what the data actually looks like. Transparency over mystery.

---

## What It Does

- 📈 **Fetches real stock prices** from Yahoo Finance (free, no API key needed)
- 🤖 **Generates AI signals** — BUY, SELL, or HOLD — using a multi-indicator scoring engine
- 📰 **Pulls live market & politics news** with bullish/bearish sentiment tagging
- 💾 **Exports results** to `trading_signals.json` for downstream use or frontend display
- 🔍 **Explains every signal** in plain English so you understand the reasoning

---

## Signal Engine — How It Works

The AI engine scores each stock across 4 technical indicators. Each indicator contributes positively (bullish) or negatively (bearish) to a cumulative score. The final score determines the signal:

| Score | Signal |
|---|---|
| +3 or higher | ✅ BUY |
| -3 or lower | 🔴 SELL |
| Between -2 and +2 | 🟡 HOLD |

### Indicators Used

| Indicator | What It Measures | Bullish Condition | Bearish Condition |
|---|---|---|---|
| **RSI** | Momentum — is the stock overbought or oversold? | RSI < 35 (oversold) | RSI > 70 (overbought) |
| **MACD** | Trend direction — is momentum accelerating? | MACD above signal line | MACD below signal line |
| **Moving Averages** | Trend confirmation — is price in an uptrend? | Price > MA5 > MA15 | Price < MA5 < MA15 |
| **Volume Ratio** | Conviction — is there strong money flow? | 1.5x+ avg volume on up move | 1.5x+ avg volume on down move |

---

## Watchlist

Default watchlist — edit in `trading_backend.py` to customize:

`AAPL` · `TSLA` · `NVDA` · `MSFT` · `AMZN` · `SPY` · `META` · `GOOGL`

---

## Sample Output

```
============================================================
  AI TRADING SIGNAL ENGINE — github.com/samshai5
============================================================
  Run time: 2026-05-27 09:32:11
  Watchlist: AAPL, TSLA, NVDA, MSFT, AMZN, SPY, META, GOOGL
============================================================

Analyzing NVDA...
  Signal: BUY (score: 5)
  Price: $878.42 (+1.3%)
  RSI: 48.2 | MA5: $862.10 | MA15: $845.30
  - RSI 48.2 — below midpoint, room to grow
  - MACD above signal line — bullish crossover
  - Price ($878.42) above MA5 ($862.10) and MA15 ($845.30) — uptrend confirmed
  - Volume 1.8x above average — strong buying interest

============================================================
  SIGNAL SUMMARY
============================================================
  BUY signals  (3): NVDA, MSFT, SPY
  SELL signals (1): TSLA
  HOLD signals (4): AAPL, AMZN, META, GOOGL
```

---

## News Feed

Uses [NewsAPI](https://newsapi.org) (free tier: 100 requests/day) to pull real market and politics headlines, with basic keyword sentiment analysis:

```
[BULLISH] Fed signals potential rate cut in Q3 amid cooling inflation
  Source: Reuters | 2026-05-27

[BEARISH] White House announces new semiconductor export restrictions
  Source: WSJ | 2026-05-27

[NEUTRAL] Senate committee passes new crypto regulation framework
  Source: Politico | 2026-05-27
```

---

## Setup & Installation

**1. Clone the repo:**
```bash
git clone https://github.com/samshai5/Trading.git
cd Trading
```

**2. Install dependencies:**
```bash
pip install yfinance requests pandas numpy
```

**3. Get a free NewsAPI key:**
- Sign up at [newsapi.org/register](https://newsapi.org/register) (free, 100 req/day)
- Open `trading_backend.py` and replace:
```python
NEWS_API_KEY = "YOUR_FREE_KEY_HERE"
```
with your actual key. Stock data works without any key.

**4. Run the engine:**
```bash
python trading_backend.py
```

Results are printed to the terminal and saved to `trading_signals.json`.

---

## Project Files

| File | Purpose |
|---|---|
| `trading_backend.py` | Core engine — signal generation, API calls, news feed, sentiment analysis |
| `trading_signals.json` | Auto-generated output file with all signals and news |

---

## Roadmap

- [ ] React frontend dashboard (connect to the signal engine via Flask API)
- [ ] Email/SMS alerts when BUY or SELL signal fires
- [ ] Backtesting module — test signals against historical data
- [ ] Portfolio tracker — track paper trades over time
- [ ] Docker containerization for easy deployment

---

## Skills Demonstrated

`Python` `Yahoo Finance API` `NewsAPI` `REST API Integration` `Pandas` `NumPy` `Technical Analysis` `RSI` `MACD` `Moving Averages` `Algorithmic Logic` `Sentiment Analysis` `JSON` `Data Processing` `Object-Oriented Programming` `Financial Data` `Debugging` `Software Development Lifecycle`

---

## Disclaimer

This project is for **educational and portfolio purposes only**. It is not financial advice. Never make real investment decisions based solely on algorithmic signals. Always do your own research.

---

## Related Projects

- 🔗 [dq-dashboard](https://github.com/samshai5/dq-dashboard) — Frontend HTML/CSS/JS dashboard (future home of the trading UI)
- 🔗 [sql-dq-engine](https://github.com/samshai5/sql-dq-engine) — SQL data quality rule engine
- 🔗 [snowflake-dq-project](https://github.com/samshai5/snowflake-dq-project) — Enterprise DQ framework in Snowflake

---

*Built by Sam Shaikh — Computer Science student at the University of Houston, passionate about AI, financial data, and building systems that turn raw market data into actionable insights.*
