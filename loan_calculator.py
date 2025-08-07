import streamlit as st
from financial_utils import calculate_loan_payment
from ui_components import format_currency, format_percentage

def render_loan_section():
    """Render loan calculator section"""
    with st.expander("🏠 Calcolo Interessi su un Prestito (TAN e TAEG)", expanded=False):
        st.subheader("Calcolo Prestito")
        
        col1, col2 = st.columns(2)
        
        with col1:
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
        
        if st.button("Calcola Prestito", key="calc_loan"):
            try:
                results = calculate_loan_metrics(loan_amount, tan_annual, taeg_annual, loan_duration_years)
                display_loan_results(results)
            except Exception as e:
                st.error("Errore nel calcolo. Verifica i valori inseriti.")
                st.exception(e)

def calculate_loan_metrics(loan_amount, tan_annual, taeg_annual, loan_duration_years):
    """Calculate loan payment and total costs"""
    
    # Calculate monthly payment using TAN
    monthly_payment = calculate_loan_payment(loan_amount, tan_annual, loan_duration_years)
    
    # Calculate totals
    total_payments = loan_duration_years * 12
    total_loan_cost = monthly_payment * total_payments
    total_interest = total_loan_cost - loan_amount
    
    # Calculate interest percentage of total cost
    interest_percentage = (total_interest / loan_amount) * 100 if loan_amount > 0 else 0
    
    # Calculate monthly interest and principal for first payment
    monthly_rate = (tan_annual / 100) / 12
    first_interest_payment = loan_amount * monthly_rate
    first_principal_payment = monthly_payment - first_interest_payment
    
    return {
        'monthly_payment': monthly_payment,
        'total_interest': total_interest,
        'total_loan_cost': total_loan_cost,
        'taeg_annual': taeg_annual,
        'tan_annual': tan_annual,
        'loan_amount': loan_amount,
        'loan_duration_years': loan_duration_years,
        'total_payments': total_payments,
        'interest_percentage': interest_percentage,
        'first_interest_payment': first_interest_payment,
        'first_principal_payment': first_principal_payment
    }

def display_loan_results(results):
    """Display loan calculation results"""
    st.success("**Risultati Prestito:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**💳 Pagamenti:**")
        st.write(f"• **Rata Mensile:** {format_currency(results['monthly_payment'])}")
        st.write(f"• **Numero Totale Rate:** {results['total_payments']}")
        st.write(f"• **Costo Totale del Prestito:** {format_currency(results['total_loan_cost'])}")
        
        st.write("**📊 Prima Rata - Composizione:**")
        st.write(f"• Quota Interessi: {format_currency(results['first_interest_payment'])}")
        st.write(f"• Quota Capitale: {format_currency(results['first_principal_payment'])}")
    
    with col2:
        st.write("**💸 Analisi Costi:**")
        st.write(f"• **Interessi Totali Pagati (TAN):** {format_currency(results['total_interest'])}")
        st.write(f"• **Percentuale Interessi:** {format_percentage(results['interest_percentage'])}")
        st.write(f"• **TAN Annuo di Riferimento:** {format_percentage(results['tan_annual'])}")
        st.write(f"• **TAEG Annuo di Riferimento:** {format_percentage(results['taeg_annual'])}")
        
        # Cost analysis
        if results['interest_percentage'] > 50:
            st.warning("⚠️ Interessi molto elevati (> 50% del capitale)")
        elif results['interest_percentage'] > 30:
            st.info("ℹ️ Interessi significativi (> 30% del capitale)")
        else:
            st.success("✅ Costo degli interessi contenuto")
        
        # TAEG vs TAN analysis
        taeg_tan_diff = results['taeg_annual'] - results['tan_annual']
        if taeg_tan_diff > 1:
            st.warning(f"⚠️ TAEG significativamente > TAN (+{format_percentage(taeg_tan_diff)})")
        else:
            st.info(f"ℹ️ Differenza TAEG-TAN: +{format_percentage(taeg_tan_diff)}")
