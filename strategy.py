# strategy.py
import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def get_market_data(symbol):
    # Fetch live data for the stock
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d', interval='1m')
    
    if todays_data.empty:
        return None, None, None
        
    current_price = todays_data['Close'].iloc[-1]
    open_price = todays_data['Open'].iloc[0]
    
    return current_price, open_price

def check_signal(symbol):
    current_price, open_price = get_market_data(symbol)
    
    if not current_price:
        return "NO_DATA"
        
    change_pct = ((current_price - open_price) / open_price) * 100
    
    # YOUR LOGIC: +1% Buy, -1% Sell
    if change_pct >= 1.0:
        return "BUY"
    elif change_pct <= -1.0:
        return "SELL"
    else:
        return "WAIT"
