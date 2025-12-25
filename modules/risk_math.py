import pandas as pd
import numpy as np

def calculate_var(price_history, confidence_level=0.95, simulations=10000):
    """
    Calculates Value at Risk (VaR) using the Monte Carlo Method.
    
    Instead of assuming a normal distribution, we simulate 10,000 possible 
    'tomorrows' based on historical volatility and drift.
    """
    if not price_history or len(price_history) < 2:
        return 0.0
    
    # 1. Prepare Data
    prices = pd.Series(price_history)
    current_price = prices.iloc[-1]
    
    # Calculate daily returns (percentage change)
    returns = prices.pct_change().dropna()
    
    # 2. Get Statistics (Drift and Volatility)
    mu = returns.mean()
    sigma = returns.std()
    
    # 3. Monte Carlo Simulation
    # Generate 10,000 random returns based on the asset's statistical profile
    # np.random.normal creates a bell curve of random possibilities
    simulated_returns = np.random.normal(mu, sigma, simulations)
    
    # 4. Calculate Simulated Future Prices
    # Price_tomorrow = Price_today * (1 + random_return)
    simulated_prices = current_price * (1 + simulated_returns)
    
    # 5. Calculate Potential Profit/Loss (PnL) for every simulation
    simulated_pnl = simulated_prices - current_price
    
    # 6. Determine VaR
    # We want the cutoff for the worst (1 - confidence) percent of cases.
    # If confidence is 95%, we look at the 5th percentile (the worst 5% of outcomes).
    percentile_cutoff = (1 - confidence_level) * 100
    var_value = np.percentile(simulated_pnl, percentile_cutoff)
    
    # VaR is typically expressed as a positive number representing magnitude of loss
    # e.g., "We are 95% confident the loss won't exceed $500"
    return round(abs(var_value), 4)

def get_esg_rating(consensus_mech):
    """
    Compliance logic based on MiCAR ESG requirements.
    """
    mapping = {
        'PoS': {'score': 85, 'rating': 'A (Low Impact)'},
        'PoW': {'score': 30, 'rating': 'C (High Energy)'},
        'N/A': {'score': 100, 'rating': 'A+ (Neutral)'}
    }
    # Default fallback
    return mapping.get(consensus_mech, {'score': 0, 'rating': 'Unrated'})