from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def calculate_ytm_linear(dirty_price, nominal_value, total_future_cash_flows, days_to_maturity):
    """Calculate YTM using linear approximation formula (market standard for short-term bonds)"""
    if days_to_maturity > 0 and dirty_price > 0:
        ytm = ((total_future_cash_flows / dirty_price) - 1) * (365 / days_to_maturity)
        return ytm
    else:
        return 0

def calculate_ytm(price, nominal_value, coupon_rate, periods_to_maturity, coupon_frequency):
    """Calculate Yield to Maturity using iterative method"""
    
    # Convert annual coupon rate to periodic rate
    if coupon_frequency == "Semestrale":
        coupon_per_period = (nominal_value * coupon_rate / 100) / 2
        periods_per_year = 2
    elif coupon_frequency == "Trimestrale":
        coupon_per_period = (nominal_value * coupon_rate / 100) / 4
        periods_per_year = 4
    else:  # Annuale
        coupon_per_period = nominal_value * coupon_rate / 100
        periods_per_year = 1
    
    # Initial guess for YTM (5% annually)
    ytm_guess = 0.05 / periods_per_year
    
    # Newton-Raphson iteration
    for _ in range(100):  # Max 100 iterations
        # Calculate bond price with current YTM guess
        pv_coupons = 0
        pv_derivative = 0
        
        for period in range(1, int(periods_to_maturity) + 1):
            discount_factor = (1 + ytm_guess) ** period
            pv_coupons += coupon_per_period / discount_factor
            pv_derivative -= period * coupon_per_period / (discount_factor * (1 + ytm_guess))
        
        # Present value of principal
        pv_principal = nominal_value / ((1 + ytm_guess) ** periods_to_maturity)
        pv_derivative -= periods_to_maturity * nominal_value / ((1 + ytm_guess) ** (periods_to_maturity + 1))
        
        # Total theoretical price
        theoretical_price = pv_coupons + pv_principal
        
        # Price difference
        price_difference = theoretical_price - price
        
        # Break if close enough
        if abs(price_difference) < 0.01:
            break
        
        # Newton-Raphson update
        ytm_guess = ytm_guess - (price_difference / pv_derivative)
    
    # Convert to annual YTM
    annual_ytm = ytm_guess * periods_per_year
    return annual_ytm

def generate_coupon_dates(issue_date, maturity_date, first_coupon_date, coupon_frequency):
    """Generate all coupon payment dates from issue to maturity"""
    coupon_dates = []
    
    # Determine the increment based on frequency
    if coupon_frequency == "Semestrale":
        months_increment = 6
    elif coupon_frequency == "Trimestrale":
        months_increment = 3
    else:  # Annuale
        months_increment = 12
    
    # Start from first coupon date
    current_date = first_coupon_date
    
    # Generate all coupon dates until maturity
    while current_date <= maturity_date:
        coupon_dates.append(current_date)
        current_date = current_date + relativedelta(months=months_increment)
    
    return coupon_dates

def find_last_coupon_before_purchase(coupon_dates, purchase_date):
    """Find the last coupon payment date before purchase date"""
    last_coupon = None
    next_coupon = None
    
    for coupon_date in coupon_dates:
        if coupon_date <= purchase_date:
            last_coupon = coupon_date
        elif coupon_date > purchase_date and next_coupon is None:
            next_coupon = coupon_date
            break
    
    return last_coupon, next_coupon

def calculate_precise_accrued_interest(nominal_value, coupon_rate, last_coupon_date, purchase_date, next_coupon_date):
    """Calculate accrued interest based on actual coupon period"""
    if last_coupon_date is None or next_coupon_date is None:
        return 0
    
    # Days from last coupon to purchase
    days_since_last_coupon = (purchase_date - last_coupon_date).days
    
    # Total days in the coupon period
    days_in_coupon_period = (next_coupon_date - last_coupon_date).days
    
    # Annual coupon amount
    annual_coupon = nominal_value * (coupon_rate / 100)
    
    # Determine coupon frequency and amount per period
    months_between = (next_coupon_date.year - last_coupon_date.year) * 12 + (next_coupon_date.month - last_coupon_date.month)
    
    if months_between <= 3:
        coupon_per_period = annual_coupon / 4
    elif months_between <= 6:
        coupon_per_period = annual_coupon / 2
    else:
        coupon_per_period = annual_coupon
    
    # Calculate accrued interest using actual/actual day count
    accrued_interest = coupon_per_period * (days_since_last_coupon / days_in_coupon_period)
    
    return accrued_interest

def count_remaining_coupons(coupon_dates, purchase_date):
    """Count remaining coupon payments after purchase date"""
    return len([date for date in coupon_dates if date > purchase_date])

def calculate_loan_payment(principal, annual_rate, years):
    """Calculate monthly loan payment using amortization formula"""
    monthly_rate = (annual_rate / 100) / 12
    total_payments = years * 12
    
    if monthly_rate > 0:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**total_payments) / ((1 + monthly_rate)**total_payments - 1)
    else:
        monthly_payment = principal / total_payments
    
    return monthly_payment

def calculate_compound_interest(initial_investment, interest_rate_annual, investment_years, recurring_investment=0):
    """Calculate future value with compound interest and optional recurring investments"""
    interest_rate_decimal = interest_rate_annual / 100
    
    # Future Value of Initial Investment
    fv_initial = initial_investment * (1 + interest_rate_decimal)**investment_years
    
    # Future Value of Recurring Investments (Annuity Future Value)
    if recurring_investment > 0:
        if interest_rate_decimal != 0:
            fv_recurring = recurring_investment * (((1 + interest_rate_decimal)**investment_years - 1) / interest_rate_decimal)
        else:
            # If interest rate is exactly 0%, simple sum
            fv_recurring = recurring_investment * investment_years
    else:
        fv_recurring = 0
    
    # Total Future Value
    total_future_value = fv_initial + fv_recurring
    
    # Total invested amount
    total_invested = initial_investment + (recurring_investment * investment_years)
    
    return {
        'total_future_value': total_future_value,
        'fv_initial': fv_initial,
        'fv_recurring': fv_recurring,
        'total_invested': total_invested,
        'total_gains': total_future_value - total_invested
    }

def calculate_cagr(initial_capital, final_capital, years):
    """Calculate Compound Annual Growth Rate (CAGR)"""
    if initial_capital > 0 and years > 0:
        cagr = ((final_capital / initial_capital)**(1 / years)) - 1
        total_return = ((final_capital - initial_capital) / initial_capital)
        return cagr, total_return
    else:
        return 0, 0
