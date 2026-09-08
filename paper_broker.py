# paper_broker.py
import logging
import json
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

LEDGER_FILE = "ledger.json"

class PaperBroker:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.positions = {}
        self.daily_pnl = 0
        
        # Load saved state if file exists
        if os.path.exists(LEDGER_FILE):
            with open(LEDGER_FILE, 'r') as f:
                data = json.load(f)
                self.balance = data.get('balance', initial_balance)
                self.positions = data.get('positions', {})
                self.daily_pnl = data.get('daily_pnl', 0)
            logging.info(f"Loaded saved state. Balance: {self.balance}")

    def save_state(self):
        # Save wallet and positions to file so it survives server restarts
        with open(LEDGER_FILE, 'w') as f:
            json.dump({
                'balance': self.balance,
                'positions': self.positions,
                'daily_pnl': self.daily_pnl
            }, f, indent=4)

    def buy(self, workstream, symbol, qty, price):
        cost = qty * price
        if cost > self.balance:
            logging.warning(f"[{workstream}] Insufficient funds to buy.")
            return False
        
        self.balance -= cost
        self.positions[workstream] = {
            "symbol": symbol,
            "qty": qty,
            "buy_price": price
        }
        self.save_state() # Save after every trade
        logging.info(f"[{workstream}] BOUGHT {symbol} at {price}. Balance: {self.balance}")
        return True

    def sell(self, workstream, price):
        if workstream not in self.positions:
            return False
        
        pos = self.positions[workstream]
        pnl = (price - pos['buy_price']) * pos['qty']
        self.balance += (pos['qty'] * price)
        self.daily_pnl += pnl
        
        self.save_state() # Save after every trade
        logging.info(f"[{workstream}] SOLD {pos['symbol']} at {price}. PnL: {pnl}. Balance: {self.balance}")
        del self.positions[workstream]
        return True

    def get_position(self, workstream):
        return self.positions.get(workstream, None)
