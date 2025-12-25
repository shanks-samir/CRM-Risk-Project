import sqlite3
import pandas as pd
import yfinance as yf
from datetime import datetime
import os

# Import the logic we built for Day 2
from modules.risk_math import calculate_var, get_esg_rating
from modules.conformity import check_market_conformity

class DataPipeline:
    def __init__(self, db_path='data/crm_risk.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._initialize_db()

    def _initialize_db(self):
        """Initializes tables for Market Data and the Trade Audit Trail."""
        with sqlite3.connect(self.db_path) as conn:
            # Table 1: Historical Market Data (Updated with high/low for conformity)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ticker TEXT,
                    asset_class TEXT,
                    price REAL,
                    high REAL,
                    low REAL,
                    consensus_mech TEXT,
                    data_source TEXT
                )
            ''')
            # Table 2: Trade Audit (The 'Big Four' Audit Trail)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS trade_audit (
                    trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ticker TEXT,
                    trade_price REAL,
                    conformity_status TEXT,
                    remarks TEXT
                )
            ''')
        print(f"Database initialized at {self.db_path}")

    def fetch_market_context(self, ticker, asset_class, consensus):
        """Fetches current price and 30-day history for Monte Carlo VaR."""
        print(f"Fetching context for {ticker}...")
        try:
            asset = yf.Ticker(ticker)
            # We need history for VaR calculations
            hist = asset.history(period='30d')
            if hist.empty:
                print(f"Warning: No data found for {ticker}")
                return None
            
            latest_row = hist.iloc[-1]
            return {
                'ticker': ticker,
                'asset_class': asset_class,
                'price': round(latest_row['Close'], 4),
                'high': round(latest_row['High'], 4),
                'low': round(latest_row['Low'], 4),
                'consensus_mech': consensus,
                'history': hist['Close'].tolist(),
                'data_source': 'Yahoo Finance'
            }
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None

    def save_market_snapshot(self, data):
        """Saves current market conditions to the DB."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO market_data (ticker, asset_class, price, high, low, consensus_mech, data_source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data['ticker'], data['asset_class'], data['price'], 
                  data['high'], data['low'], data['consensus_mech'], data['data_source']))

    def log_trade(self, ticker, price, status, remarks=""):
        """Logs a trade execution for the audit dashboard."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO trade_audit (ticker, trade_price, conformity_status, remarks)
                VALUES (?, ?, ?, ?)
            ''', (ticker, price, status, remarks))
            print(f"Audit Logged: {ticker} | Status: {status}")

# --- Execution Block ---
if __name__ == "__main__":
    pipeline = DataPipeline()
    
    # Define our multi-asset universe
    assets_to_track = [
        {'ticker': 'BTC-USD', 'class': 'Native', 'consensus': 'PoW'},
        {'ticker': 'ETH-USD', 'class': 'Native', 'consensus': 'PoS'},
        {'ticker': 'IBIT', 'class': 'Delta-1', 'consensus': 'N/A'},
        {'ticker': 'SHV', 'class': 'Tokenized', 'consensus': 'N/A'} # Proxy for Tokenized T-Bill
    ]

    for item in assets_to_track:
        # 1. Fetch live market context
        ctx = pipeline.fetch_market_context(item['ticker'], item['class'], item['consensus'])
        
        if ctx:
            # 2. Store the market snapshot
            pipeline.save_market_snapshot(ctx)

            # 3. Perform Risk Calculations (Monte Carlo & ESG)
            # These demonstrate the 'Secret Sauce' [00:52]
            var_amount = calculate_var(ctx['history'])
            esg_info = get_esg_rating(ctx['consensus_mech'])
            print(f"  > Risk Metrics: VaR=${var_amount} | ESG: {esg_info['rating']}")

            # 4. Market Conformity Check (Fair Market Value)
            # Scenario: BTC fails (bad price), others pass (fair price)
            if item['ticker'] == 'BTC-USD':
                # Simulating a price 3% outside the daily high/low range
                trade_price = ctx['high'] * 1.03 
                note = "Simulated Fat-Finger Error"
            else:
                trade_price = ctx['price']
                note = "Standard Execution"

            status, bounds = check_market_conformity(trade_price, ctx['high'], ctx['low'])
            
            # 5. Log for the Auditor
            pipeline.log_trade(
                ticker=item['ticker'], 
                price=trade_price, 
                status=status, 
                remarks=f"{note} | Range: {bounds['min']:.2f}-{bounds['max']:.2f}"
            )

    print("\nTasks Complete. Ready for Dashboard View.")