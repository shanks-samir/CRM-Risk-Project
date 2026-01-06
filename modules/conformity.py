def check_market_conformity(trade_price, daily_high, daily_low):
    """
    Checks if a trade price is within the 'Fair Market Value' range.
    Returns True if passed, False if failed.
    """
    # In a real scenario, you might allow a 1% buffer outside the range
    buffer = 0.01 
    lower_bound = daily_low * (1 - buffer)
    upper_bound = daily_high * (1 + buffer)
    
    is_conform = lower_bound <= trade_price <= upper_bound
    
    status = "PASS" if is_conform else "FAIL"
    return status, {"min": lower_bound, "max": upper_bound}

