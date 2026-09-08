# config.py

WALLET_BALANCE = 10000
TRADE_SIZE = 5000
DAILY_LOSS_LIMIT = 2000  # Stop trading if down Rs. 2000

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
