import streamlit as st
import math
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# Configuration of the page
st.set_page_config(
    page_title="Calcolatore Finanziario",
    page_icon="💰",
    layout="wide"
)

# Main title
st.title("🏦 Calcolatore Finanziario Avanzato")
st.markdown("---")

# Function to calculate bond accrued interest
def calculate_accrued_interest(nominal_value, coupon_rate, last_coupon_date, purchase_date, coupon_frequency):
    """Calculate accrued interest from last coupon payment to purchase date"""
    days_since_last_coupon = (purchase_date - last_coupon_date).days
    
    # Days in coupon period based on frequency
    if coupon_frequency == "Semestrale":
        days_in_period = 182.5  # Average days in 6 months
    elif coupon_frequency == "Trimestrale":
        days_in_period = 91.25  # Average days in 3 months
    else:  # Annuale
        days_in_period = 365
    
    # Annual coupon amount
    annual_coupon = nominal_value * (coupon_rate / 100)
    
    # Coupon amount per period
    if coupon_frequency == "Semestrale":
        coupon_per_period = annual_coupon / 2
    elif coupon_frequency == "Trimestrale":
        coupon_per_period = annual_coupon / 4
    else:  # Annuale
        coupon_per_period = annual_coupon
    
    # Accrued interest calculation
    accrued_interest = coupon_per_period * (days_since_last_coupon / days_in_period)
    
    return accrued_interest

# Function to calculate YTM using Newton-Raphson method
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

# Section 1: Advanced Bond Calculation
with st.expander("📊 Calcolo Avanzato Obbligazioni (YTM Preciso)", expanded=False):
    st.subheader("Calcolo Obbligazioni con Date Precise")
    st.info("💡 Calcolo accurato con date precise, frequenza cedole e rateo interessi")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Basic bond parameters
        nominal_value = st.number_input(
            "Valore Nominale (€)", 
            min_value=0.01, 
            value=1000.00,
            step=10.00,
            key="adv_bond_nominal"
        )
        
        coupon_rate = st.number_input(
            "Tasso Cedolare Annuo (%)", 
            min_value=0.0, 
            max_value=50.0,
            value=3.5,
            step=0.1,
            key="adv_bond_coupon"
        )
        
        purchase_price = st.number_input(
            "Prezzo Clean di Acquisto (€)", 
            min_value=0.01, 
            value=975.00,
            step=1.00,
            key="adv_bond_price"
        )
    
    with col2:
        # Dates
        purchase_date = st.date_input(
            "Data di Acquisto", 
            value=date.today(),
            key="adv_bond_purchase_date"
        )
        
        maturity_date = st.date_input(
            "Data di Scadenza", 
            value=date.today() + relativedelta(years=5),
            min_value=date.today(),
            key="adv_bond_maturity_date"
        )
        
        last_coupon_date = st.date_input(
            "Data Ultimo Pagamento Cedola", 
            value=date.today() - relativedelta(months=6),
            key="adv_bond_last_coupon"
        )
    
    with col3:
        # Coupon frequency
        coupon_frequency = st.selectbox(
            "Frequenza Pagamento Cedole",
            ["Annuale", "Semestrale", "Trimestrale"],
            index=1,  # Default to Semestrale
            key="adv_bond_frequency"
        )
        
        # Calculate periods automatically
        days_to_maturity = (maturity_date - purchase_date).days
        
        if coupon_frequency == "Semestrale":
            periods_to_maturity = days_to_maturity / 182.5
            payments_per_year = 2
        elif coupon_frequency == "Trimestrale":
            periods_to_maturity = days_to_maturity / 91.25
            payments_per_year = 4
        else:  # Annuale
            periods_to_maturity = days_to_maturity / 365
            payments_per_year = 1
        
        st.write(f"**Giorni alla Scadenza:** {days_to_maturity}")
        st.write(f"**Periodi Cedolari:** {periods_to_maturity:.2f}")
    
    # Advanced bond calculations
    if st.button("Calcola Obbligazione Avanzata", key="calc_adv_bond"):
        try:
            # Check date validity
            if maturity_date <= purchase_date:
                st.error("❌ La data di scadenza deve essere successiva alla data di acquisto!")
                st.stop()
            
            if last_coupon_date >= purchase_date:
                st.error("❌ L'ultimo pagamento cedola deve essere precedente all'acquisto!")
                st.stop()
            
            # Calculate accrued interest
            accrued_interest = calculate_accrued_interest(
                nominal_value, coupon_rate, last_coupon_date, 
                purchase_date, coupon_frequency
            )
            
            # Dirty price (clean price + accrued interest)
            dirty_price = purchase_price + accrued_interest
            
            # Calculate annual coupon
            annual_coupon = nominal_value * (coupon_rate / 100)
            
            # Calculate coupon per period
            if coupon_frequency == "Semestrale":
                coupon_per_period = annual_coupon / 2
            elif coupon_frequency == "Trimestrale":
                coupon_per_period = annual_coupon / 4
            else:
                coupon_per_period = annual_coupon
            
            # Calculate YTM
            ytm = calculate_ytm(purchase_price, nominal_value, coupon_rate, periods_to_maturity, coupon_frequency)
            
            # Calculate total return if held to maturity
            total_coupon_payments = coupon_per_period * int(periods_to_maturity)
            capital_gain = nominal_value - purchase_price
            total_return = total_coupon_payments + capital_gain
            total_return_percentage = (total_return / purchase_price) * 100
            
            # Display results
            st.success("**🎯 Risultati Calcolo Avanzato Obbligazione:**")
            
            # Create results columns
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.write("**💰 Informazioni Cedole:**")
                st.write(f"• Cedola Annuale: €{annual_coupon:.2f}")
                st.write(f"• Cedola per Periodo: €{coupon_per_period:.2f}")
                st.write(f"• Frequenza: {coupon_frequency}")
                st.write(f"• Numero Cedole Rimanenti: {int(periods_to_maturity)}")
                
                st.write("**💵 Analisi Prezzi:**")
                st.write(f"• Prezzo Clean: €{purchase_price:.2f}")
                st.write(f"• Rateo Interessi: €{accrued_interest:.2f}")
                st.write(f"• Prezzo Dirty: €{dirty_price:.2f}")
            
            with res_col2:
                st.write("**📈 Rendimenti:**")
                st.write(f"• **YTM (Yield to Maturity): {ytm:.3%}**")
                st.write(f"• Rendimento Cedole Totali: €{total_coupon_payments:.2f}")
                st.write(f"• Capital Gain/Loss: €{capital_gain:.2f}")
                st.write(f"• **Rendimento Totale: €{total_return:.2f}**")
                st.write(f"• **Rendimento Totale %: {total_return_percentage:.2f}%**")
            
            # Additional metrics
            st.write("**📊 Metriche Aggiuntive:**")
            current_yield = (annual_coupon / purchase_price) * 100
            st.write(f"• Current Yield: {current_yield:.2f}%")
            st.write(f"• Giorni alla Scadenza: {days_to_maturity}")
            st.write(f"• Anni alla Scadenza: {days_to_maturity/365:.2f}")
            
            if ytm > coupon_rate / 100:
                st.info("📊 L'obbligazione è **sotto la pari** - YTM > Coupon Rate")
            elif ytm < coupon_rate / 100:
                st.info("📊 L'obbligazione è **sopra la pari** - YTM < Coupon Rate") 
            else:
                st.info("📊 L'obbligazione è **alla pari** - YTM = Coupon Rate")
            
        except Exception as e:
            st.error(f"Errore nel calcolo avanzato: {str(e)}")
            st.error("Verifica che tutte le date e i valori siano corretti.")

st.markdown("---")

# Section 2: Loan Interest Calculation (TAN and TAEG)
with st.expander("🏠 Calcolo Interessi su un Prestito (TAN e TAEG)", expanded=False):
    st.subheader("Calcolo Prestito")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Input fields for loan calculation
        loan_amount = st.number_input(
            "Importo del Prestito (€)", 
            min_value=1.00, 
            value=100000.00,
            step=1000.00,
            key="loan_amount"
        )
        
        tan_annual = st.number_input(
            "TAN Annuo (%)", 
            min_value=0.0, 
            max_value=50.0,
            value=3.5,
            step=0.1,
            key="loan_tan"
        )
    
    with col2:
        taeg_annual = st.number_input(
            "TAEG Annuo (%)", 
            min_value=0.0, 
            max_value=50.0,
            value=3.8,
            step=0.1,
            key="loan_taeg"
        )
        
        loan_duration_years = st.number_input(
            "Durata del Prestito (Anni)", 
            min_value=1, 
            value=20,
            step=1,
            key="loan_duration"
        )
    
    # Loan calculations
    if st.button("Calcola Prestito", key="calc_loan"):
        try:
            # Convert annual TAN to monthly rate
            monthly_rate = (tan_annual / 100) / 12
            
            # Calculate total number of payments
            total_payments = loan_duration_years * 12
            
            # Calculate monthly payment (amortization formula)
            if monthly_rate > 0:
                monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**total_payments) / ((1 + monthly_rate)**total_payments - 1)
            else:
                monthly_payment = loan_amount / total_payments
            
            # Calculate total loan cost and total interest
            total_loan_cost = monthly_payment * total_payments
            total_interest = total_loan_cost - loan_amount
            
            # Display results
            st.success("**Risultati Prestito:**")
            st.write(f"💳 **Rata Mensile:** €{monthly_payment:.2f}")
            st.write(f"💸 **Interessi Totali Pagati (basato sul TAN):** €{total_interest:.2f}")
            st.write(f"📊 **TAEG Annuo di Riferimento:** {taeg_annual:.2f}%")
            st.write(f"💰 **Costo Totale del Prestito:** €{total_loan_cost:.2f}")
            
        except Exception as e:
            st.error("Errore nel calcolo. Verifica i valori inseriti.")

st.markdown("---")

# Section 3: Compound Interest Calculation (with Recurring Investment)
with st.expander("📈 Calcolo Interesse Composto (con Investimento Ricorrente)", expanded=False):
    st.subheader("Calcolo Investimento con Interesse Composto")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Input fields for compound interest calculation
        initial_investment = st.number_input(
            "Somma Iniziale Investita (€)", 
            min_value=0.00, 
            value=10000.00,
            step=100.00,
            key="compound_initial"
        )
        
        interest_rate_annual = st.number_input(
            "Tasso di Interesse Annuo (%)", 
            min_value=0.0, 
            max_value=50.0,
            value=5.0,
            step=0.1,
            key="compound_rate"
        )
    
    with col2:
        investment_years = st.number_input(
            "Numero di Anni", 
            min_value=1, 
            value=10,
            step=1,
            key="compound_years"
        )
        
        recurring_investment = st.number_input(
            "Investimento Ricorrente Annuo (€) - Opzionale", 
            min_value=0.00, 
            value=0.00,
            step=100.00,
            key="compound_recurring"
        )
    
    # Compound interest calculations
    if st.button("Calcola Interesse Composto", key="calc_compound"):
        try:
            # Convert interest rate to decimal
            interest_rate_decimal = interest_rate_annual / 100
            
            # Future Value of Initial Investment
            fv_initial = initial_investment * (1 + interest_rate_decimal)**investment_years
            
            # Future Value of Recurring Investments (Annuity Future Value)
            if recurring_investment > 0 and interest_rate_decimal > 0:
                fv_recurring = recurring_investment * (((1 + interest_rate_decimal)**investment_years - 1) / interest_rate_decimal)
            elif recurring_investment > 0 and interest_rate_decimal == 0:
                fv_recurring = recurring_investment * investment_years
            else:
                fv_recurring = 0
            
            # Total Future Value
            total_future_value = fv_initial + fv_recurring
            
            # Total invested amount
            total_invested = initial_investment + (recurring_investment * investment_years)
            
            # Total gains
            total_gains = total_future_value - total_invested
            
            # Display results
            st.success("**Risultati Interesse Composto:**")
            st.write(f"🎯 **Valore Futuro dell'Investimento:** €{total_future_value:.2f}")
            st.write(f"💰 **Totale Investito:** €{total_invested:.2f}")
            st.write(f"📊 **Guadagno Totale:** €{total_gains:.2f}")
            st.write(f"🚀 **Valore Futuro Investimento Iniziale:** €{fv_initial:.2f}")
            if fv_recurring > 0:
                st.write(f"🔄 **Valore Futuro Investimenti Ricorrenti:** €{fv_recurring:.2f}")
            
        except Exception as e:
            st.error("Errore nel calcolo. Verifica i valori inseriti.")

st.markdown("---")

# Section 4: Final Annual Return and Invested Capital Calculation
with st.expander("🎯 Calcolo Rendimento Annuo Finale e Capitale Investito", expanded=False):
    st.subheader("Calcolo CAGR (Compound Annual Growth Rate)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Input fields for CAGR calculation
        initial_capital = st.number_input(
            "Capitale Iniziale (€)", 
            min_value=0.01, 
            value=10000.00,
            step=100.00,
            key="cagr_initial"
        )
    
    with col2:
        final_capital = st.number_input(
            "Capitale Finale (€)", 
            min_value=0.01, 
            value=15000.00,
            step=100.00,
            key="cagr_final"
        )
    
    with col3:
        cagr_years = st.number_input(
            "Numero di Anni", 
            min_value=1, 
            value=5,
            step=1,
            key="cagr_years"
        )
    
    # CAGR calculations
    if st.button("Calcola CAGR", key="calc_cagr"):
        try:
            # Calculate CAGR
            if initial_capital > 0 and cagr_years > 0:
                cagr = ((final_capital / initial_capital)**(1 / cagr_years)) - 1
            else:
                cagr = 0
            
            # Calculate total return
            total_return = ((final_capital - initial_capital) / initial_capital) if initial_capital > 0 else 0
            
            # Display results
            st.success("**Risultati CAGR:**")
            st.write(f"📈 **Rendimento Annuo Finale (CAGR):** {cagr:.2%}")
            st.write(f"💰 **Capitale Iniziale Investito:** €{initial_capital:.2f}")
            st.write(f"🎯 **Capitale Finale:** €{final_capital:.2f}")
            st.write(f"🚀 **Rendimento Totale:** {total_return:.2%}")
            st.write(f"💵 **Guadagno Assoluto:** €{final_capital - initial_capital:.2f}")
            
        except Exception as e:
            st.error("Errore nel calcolo. Verifica i valori inseriti.")

# Footer
st.markdown("---")
st.markdown("### 📝 Note:")
st.info("""
- **TAN (Tasso Annuo Nominale)**: Il tasso di interesse puro del prestito
- **TAEG (Tasso Annuo Effettivo Globale)**: Include tutti i costi del finanziamento
- **YTM (Yield to Maturity)**: Rendimento effettivo dell'obbligazione se mantenuta fino alla scadenza
- **CAGR (Compound Annual Growth Rate)**: Tasso di crescita annuale composto
- **Prezzo Clean**: Prezzo dell'obbligazione senza rateo interessi
- **Prezzo Dirty**: Prezzo Clean + rateo interessi maturati
- **Current Yield**: Rendimento annuale delle cedole rispetto al prezzo di acquisto
""")

st.markdown("### 📦 Requirements.txt per Deploy:")
st.code("""streamlit>=1.28.0
python-dateutil>=2.8.2""", language="txt")

st.markdown("*Sviluppato per calcoli finanziari di base.*")
