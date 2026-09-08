# zerodha_broker.py
from kiteconnect import KiteConnect
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class ZerodhaBroker:
    def __init__(self, api_key, access_token):
        """Initialize Zerodha broker connection"""
        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)
        self.positions = {}
        self.daily_pnl = 0
        logging.info("✅ Connected to Zerodha Kite API")

    def buy(self, workstream, symbol, qty, price):
        """Place a BUY order via Zerodha"""
        try:
            order_id = self.kite.place_order(
                variety=self.kite.VARIETY_REGULAR,
                exchange=self.kite.EXCHANGE_NSE,
                tradingsymbol=symbol,
                transaction_type=self.kite.TRANSACTION_TYPE_BUY,
                quantity=int(qty),
                order_type=self.kite.ORDER_TYPE_MARKET
            )
            self.positions[workstream] = {
                "symbol": symbol,
                "qty": qty,
                "order_id": order_id,
                "entry_price": price
            }
            logging.info(f"[{workstream}] 🟢 BUY order placed on Zerodha: {order_id} for {symbol}")
            return True
        except Exception as e:
            logging.error(f"[{workstream}] ❌ BUY failed on Zerodha: {e}")
            return False

    def sell(self, workstream, price):
        """Place a SELL order via Zerodha"""
        try:
            if workstream not in self.positions:
                logging.warning(f"[{workstream}] No position to sell")
                return False
            
            pos = self.positions[workstream]
            order_id = self.kite.place_order(
                variety=self.kite.VARIETY_REGULAR,
                exchange=self.kite.EXCHANGE_NSE,
                tradingsymbol=pos["symbol"],
                transaction_type=self.kite.TRANSACTION_TYPE_SELL,
                quantity=int(pos["qty"]),
                order_type=self.kite.ORDER_TYPE_MARKET
            )
            
            pnl = (price - pos["entry_price"]) * pos["qty"]
            self.daily_pnl += pnl
            
            logging.info(f"[{workstream}] 🔴 SELL order placed on Zerodha: {order_id} for {pos['symbol']} | PnL: {pnl}")
            del self.positions[workstream]
            return True
        except Exception as e:
            logging.error(f"[{workstream}] ❌ SELL failed on Zerodha: {e}")
            return False

    def get_position(self, workstream):
        """Get position details for a workstream"""
        return self.positions.get(workstream, None)
