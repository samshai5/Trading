import requests
import json
from datetime import datetime, timedelta
import time

# ============================================================
# AI Trading Signal Engine — Sam Shaikh
# github.com/samshai5/Trading
#
# FREE APIs used:
# - Yahoo Finance (via yfinance) — real stock prices, no key needed
# - NewsAPI — market & politics headlines (free tier: 100 req/day)
#   Get your free key at: https://newsapi.org/register
#
# Install dependencies:
# pip install yfinance requests pandas numpy
# ============================================================

try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
    print("All libraries loaded successfully.")
except ImportError:
    print("Run this first: pip install yfinance requests pandas numpy")
    exit()

NEWS_API_KEY = "YOUR_FREE_KEY_HERE"  # Get free at newsapi.org/register

WATCHLIST = ["AAPL", "TSLA", "NVDA", "MSFT", "AMZN", "SPY", "META", "GOOGL"]

# ============================================================
# FETCH REAL STOCK DATA
# ============================================================

def fetch_stock_data(symbol, period="30d", interval="1d"):
    """Fetch real historical price data from Yahoo Finance."""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        if df.empty:
            print(f"No data returned for {symbol}")
            return None
        return df
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def get_current_price(symbol):
    """Get the latest real-time price for a symbol."""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2)
        return None
    except Exception as e:
        print(f"Error getting price for {symbol}: {e}")
        return None

# ============================================================
# AI SIGNAL ENGINE
# ============================================================

def calculate_rsi(prices, period=14):
    """Calculate RSI (Relative Strength Index)."""
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi.iloc[-1], 2)

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)."""
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return round(macd_line.iloc[-1], 4), round(signal_line.iloc[-1], 4), round(histogram.iloc[-1], 4)

def calculate_moving_averages(prices):
    """Calculate 5-day, 15-day, and 50-day moving averages."""
    ma5 = round(prices.rolling(window=5).mean().iloc[-1], 2)
    ma15 = round(prices.rolling(window=15).mean().iloc[-1], 2)
    ma50 = round(prices.rolling(window=min(50, len(prices))).mean().iloc[-1], 2)
    return ma5, ma15, ma50

def generate_signal(symbol):
    """
    AI Signal Engine — generates BUY / SELL / HOLD based on:
    - RSI (momentum)
    - MACD crossover (trend direction)
    - Moving average alignment (trend confirmation)
    - Price vs moving averages (momentum confirmation)
    """
    df = fetch_stock_data(symbol, period="60d")
    if df is None or len(df) < 20:
        return None

    prices = df['Close']
    current_price = round(prices.iloc[-1], 2)
    prev_price = round(prices.iloc[-2], 2)
    price_change = round(((current_price - prev_price) / prev_price) * 100, 2)

    rsi = calculate_rsi(prices)
    macd_line, signal_line, histogram = calculate_macd(prices)
    ma5, ma15, ma50 = calculate_moving_averages(prices)

    volume = df['Volume'].iloc[-1]
    avg_volume = round(df['Volume'].rolling(window=10).mean().iloc[-1], 0)
    volume_ratio = round(volume / avg_volume, 2) if avg_volume > 0 else 1

    # --- Signal Scoring ---
    score = 0
    reasons = []

    # RSI signals
    if rsi < 35:
        score += 2
        reasons.append(f"RSI {rsi} — oversold territory (bullish)")
    elif rsi < 50:
        score += 1
        reasons.append(f"RSI {rsi} — below midpoint, room to grow")
    elif rsi > 70:
        score -= 2
        reasons.append(f"RSI {rsi} — overbought territory (bearish)")
    elif rsi > 60:
        score -= 1
        reasons.append(f"RSI {rsi} — approaching overbought")

    # MACD crossover
    if macd_line > signal_line and histogram > 0:
        score += 2
        reasons.append("MACD above signal line — bullish crossover")
    elif macd_line < signal_line and histogram < 0:
        score -= 2
        reasons.append("MACD below signal line — bearish crossover")

    # Moving average alignment
    if current_price > ma5 > ma15:
        score += 2
        reasons.append(f"Price (${current_price}) above MA5 (${ma5}) and MA15 (${ma15}) — uptrend confirmed")
    elif current_price < ma5 < ma15:
        score -= 2
        reasons.append(f"Price (${current_price}) below MA5 (${ma5}) and MA15 (${ma15}) — downtrend confirmed")

    # Volume confirmation
    if volume_ratio > 1.5:
        if score > 0:
            score += 1
            reasons.append(f"Volume {volume_ratio}x above average — strong buying interest")
        else:
            score -= 1
            reasons.append(f"Volume {volume_ratio}x above average — strong selling pressure")

    # Final signal decision
    if score >= 3:
        signal = "BUY"
    elif score <= -3:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {
        "symbol": symbol,
        "signal": signal,
        "score": score,
        "current_price": current_price,
        "price_change_pct": price_change,
        "rsi": rsi,
        "macd": macd_line,
        "macd_signal": signal_line,
        "ma5": ma5,
        "ma15": ma15,
        "ma50": ma50,
        "volume_ratio": volume_ratio,
        "reasons": reasons,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# ============================================================
# REAL NEWS FEED (NewsAPI — free tier)
# ============================================================

def fetch_market_news(api_key, query="stock market OR Federal Reserve OR interest rates OR earnings", page_size=8):
    """Fetch real market and politics news from NewsAPI."""
    if api_key == "YOUR_FREE_KEY_HERE":
        print("\nNo NewsAPI key set. Get a free key at newsapi.org/register")
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if data.get("status") == "ok":
            articles = data.get("articles", [])
            news = []
            for a in articles:
                news.append({
                    "title": a.get("title", ""),
                    "source": a.get("source", {}).get("name", ""),
                    "published": a.get("publishedAt", "")[:10],
                    "url": a.get("url", "")
                })
            return news
        else:
            print(f"NewsAPI error: {data.get('message')}")
            return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def fetch_politics_news(api_key, page_size=5):
    """Fetch political news that could impact markets."""
    return fetch_market_news(
        api_key,
        query="Federal Reserve OR inflation OR interest rates OR Congress economy OR trade tariffs",
        page_size=page_size
    )

# ============================================================
# SENTIMENT ANALYZER (basic keyword-based)
# ============================================================

def analyze_sentiment(text):
    """Basic keyword sentiment analysis for news headlines."""
    bullish_words = ['rally', 'surge', 'beat', 'growth', 'profit', 'gain', 'rise', 'strong',
                     'positive', 'up', 'high', 'record', 'boost', 'recovery', 'optimism']
    bearish_words = ['drop', 'fall', 'loss', 'miss', 'decline', 'weak', 'risk', 'concern',
                     'down', 'crash', 'fear', 'recession', 'cut', 'layoff', 'sell-off']

    text_lower = text.lower()
    bull_count = sum(1 for word in bullish_words if word in text_lower)
    bear_count = sum(1 for word in bearish_words if word in text_lower)

    if bull_count > bear_count:
        return "BULLISH"
    elif bear_count > bull_count:
        return "BEARISH"
    return "NEUTRAL"

# ============================================================
# MAIN — RUN THE ENGINE
# ============================================================

def run_engine():
    print("\n" + "="*60)
    print("  AI TRADING SIGNAL ENGINE — github.com/samshai5")
    print("="*60)
    print(f"  Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Watchlist: {', '.join(WATCHLIST)}")
    print("="*60)

    results = []
    for symbol in WATCHLIST:
        print(f"\nAnalyzing {symbol}...")
        result = generate_signal(symbol)
        if result:
            results.append(result)
            print(f"  Signal: {result['signal']} (score: {result['score']})")
            print(f"  Price: ${result['current_price']} ({'+' if result['price_change_pct'] >= 0 else ''}{result['price_change_pct']}%)")
            print(f"  RSI: {result['rsi']} | MA5: ${result['ma5']} | MA15: ${result['ma15']}")
            for reason in result['reasons']:
                print(f"  - {reason}")
        time.sleep(0.5)

    print("\n" + "="*60)
    print("  SIGNAL SUMMARY")
    print("="*60)
    buys = [r for r in results if r['signal'] == 'BUY']
    sells = [r for r in results if r['signal'] == 'SELL']
    holds = [r for r in results if r['signal'] == 'HOLD']

    print(f"  BUY signals  ({len(buys)}): {', '.join([r['symbol'] for r in buys])}")
    print(f"  SELL signals ({len(sells)}): {', '.join([r['symbol'] for r in sells])}")
    print(f"  HOLD signals ({len(holds)}): {', '.join([r['symbol'] for r in holds])}")

    print("\n" + "="*60)
    print("  MARKET & POLITICS NEWS")
    print("="*60)
    news = fetch_market_news(NEWS_API_KEY)
    if news:
        for article in news:
            sentiment = analyze_sentiment(article['title'])
            print(f"\n  [{sentiment}] {article['title']}")
            print(f"  Source: {article['source']} | {article['published']}")
    else:
        print("  Add your NewsAPI key to see real headlines.")
        print("  Free key at: https://newsapi.org/register")

    output = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "signals": results,
        "news": news
    }
    with open("trading_signals.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\n\nFull results saved to trading_signals.json")
    print("="*60)
    print("\nDISCLAIMER: For educational and portfolio purposes only.")
    print("Not financial advice. Always do your own research.")
    print("="*60)

if __name__ == "__main__":
    run_engine()
