# agent.py
import time
from datetime import datetime
import config
from paper_broker import PaperBroker
from strategy import check_signal
import requests

class TradingAgent:
    def __init__(self):
        self.broker = PaperBroker(config.WALLET_BALANCE)
        self.is_running = False

    def send_telegram(self, message):
        """Send alerts to your phone"""
        if "YOUR_TELEGRAM" in config.TELEGRAM_BOT_TOKEN:
            return # Skip if not configured
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": config.TELEGRAM_CHAT_ID, "text": message}
        try:
            requests.post(url, json=payload)
        except:
            pass

    def market_is_open(self):
        now = datetime.now()
        # Basic check: Monday(0) to Friday(4)
        if now.weekday() >= 5:
            return False
            
        current_time = now.strftime("%H:%M")
        if config.MARKET_START <= current_time <= config.MARKET_END:
            return True
        return False

    def run(self):
        self.is_running = True
        print("🤖 Agent started. Monitoring market...")
        self.send_telegram("🤖 Trading Agent Started. Monitoring market...")

        while self.is_running:
            if not self.market_is_open():
                # Sleep if market closed (check every 5 mins to save CPU)
                time.sleep(300)
                continue

            # 1. Check Daily Loss Limit (Kill Switch)
            if self.broker.daily_pnl <= -config.DAILY_LOSS_LIMIT:
                print("⛔ DAILY LOSS LIMIT HIT. Squaring off and stopping.")
                self.square_off_all()
                self.send_telegram("⛔ DAILY LOSS LIMIT HIT. Agent stopped.")
                break

            # 2. Process each workstream
            for ws in config.WORKSTREAMS:
                if ws['status'] != 'ACTIVE':
                    continue

                signal = check_signal(ws['symbol'])
                pos = self.broker.get_position(ws['name'])

                # Virtual Option Price: We simulate option price as 10% of stock price for this test
                # In real life, you would fetch the Option Chain LTP here.
                current_stock_price, _ = __import__('strategy').get_market_data(ws['symbol'])
                if not current_stock_price:
                    continue
                virtual_option_price = current_stock_price * 0.10 

                if signal == "BUY" and not pos:
                    qty = int(ws['allocated_capital'] / virtual_option_price)
                    self.broker.buy(ws['name'], ws['symbol'], qty, virtual_option_price)
                    self.send_telegram(f"🟢 BUY Signal: {ws['symbol']}")

                elif signal == "SELL" and pos:
                    self.broker.sell(ws['name'], virtual_option_price)
                    self.send_telegram(f"🔴 SELL Signal: {ws['symbol']}")

            # Check every 60 seconds
            time.sleep(60)

    def square_off_all(self):
        for ws in config.WORKSTREAMS:
            pos = self.broker.get_position(ws['name'])
            if pos:
                current_stock_price, _ = __import__('strategy').get_market_data(pos['symbol'])
                virtual_option_price = current_stock_price * 0.10
                self.broker.sell(ws['name'], virtual_option_price)

if __name__ == "__main__":
    agent = TradingAgent()
    agent.run()
