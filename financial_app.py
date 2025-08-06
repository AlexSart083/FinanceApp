import streamlit as st
import math

# Configuration of the page
st.set_page_config(
    page_title="Calcolatore Finanziario",
    page_icon="💰",
    layout="wide"
)

# Main title
st.title("🏦 Calcolatore Finanziario Avanzato")
st.markdown("---")

# Section 1: Bond Coupon and Annual Yield Calculation
with st.expander("📊 Calcolo Cedole e Rendimento Annuo Obbligazione", expanded=False):
    st.subheader("Calcolo Obbligazioni")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Input fields for bond calculation
        nominal_value = st.number_input(
            "Valore Nominale (€)", 
            min_value=0.01, 
            value=1000.00,
            step=10.00,
            key="bond_nominal"
        )
        
        coupon_rate = st.number_input(
            "Tasso Cedolare Annuo (%)", 
            min_value=0.0, 
            max_value=100.0,
            value=2.5,
            step=0.1,
            key="bond_coupon"
        )
    
    with col2:
        purchase_price = st.number_input(
            "Prezzo di Acquisto (€)", 
            min_value=0.01, 
            value=980.00,
            step=10.00,
            key="bond_price"
        )
        
        years_to_maturity = st.number_input(
            "Anni alla Scadenza", 
            min_value=1, 
            value=5,
            step=1,
            key="bond_years"
        )
    
    # Bond calculations
    if st.button("Calcola Obbligazione", key="calc_bond"):
        try:
            # Annual coupon calculation
            annual_coupon = nominal_value * (coupon_rate / 100)
            
            # Simplified YTM calculation
            annual_yield = (annual_coupon + (nominal_value - purchase_price) / years_to_maturity) / purchase_price
            
            # Display results
            st.success("**Risultati Obbligazione:**")
            st.write(f"💰 **Cedola Annuale:** €{annual_coupon:.2f}")
            st.write(f"📈 **Rendimento Annuo (YTM Semplificato):** {annual_yield:.2%}")
            
        except Exception as e:
            st.error("Errore nel calcolo. Verifica i valori inseriti.")

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
            st.write(f"📊 **TAEG Annuo di Riferimento:** {taeg_annual:.2%}")
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
- **YTM (Yield to Maturity)**: Rendimento dell'obbligazione se mantenuta fino alla scadenza
- **CAGR (Compound Annual Growth Rate)**: Tasso di crescita annuale composto
""")

st.markdown("*Sviluppato per calcoli finanziari di base. Consultare sempre un consulente finanziario qualificato per decisioni di investimento.*")
