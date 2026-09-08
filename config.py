# config.py
import os

WALLET_BALANCE = 10000
TRADE_SIZE = 5000
DAILY_LOSS_LIMIT = 2000  # Stop trading if down Rs. 2000

# Trading Mode: "paper" for paper trading, "zerodha" for live trading
TRADING_MODE = os.getenv("TRADING_MODE", "paper")

# Zerodha Credentials (NEVER hardcode, always use environment variables)
ZERODHA_API_KEY = os.getenv("ZERODHA_API_KEY", "")
ZERODHA_ACCESS_TOKEN = os.getenv("ZERODHA_ACCESS_TOKEN", "")

# Workstreams: Mapping of strategy to stock and virtual option lot
WORKSTREAMS = [
    {
        "name": "WS_MIDCAP_01",
        "symbol": "M&MFIN.NS",  # Mahindra & Mahindra Financial Services
        "allocated_capital": 5000,
        "status": "ACTIVE"
    }
]

# Telegram Bot Settings (Optional but highly recommended)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

# Market timings (IST)
MARKET_START = "09:15"
MARKET_END = "15:15" # We square off 15 mins before close
