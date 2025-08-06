import streamlit as st
from financial_utils import calculate_compound_interest, calculate_cagr
from ui_components import format_currency, format_percentage

def render_compound_interest_section():
    """Render compound interest calculator section"""
    with st.expander("📈 Calcolo Interesse Composto", expanded=False):
        st.subheader("Calcolo Investimento con Interesse Composto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            initial_investment = st.number_input(
                "Somma Iniziale Investita (€)", 
                min_value=0.00, 
                value=10000.00,
                step=100.00,
                key="compound_initial"
            )
            
            interest_rate_annual = st.number_input(
                "Tasso di Interesse Annuo (%)", 
                min_value=-50.0, 
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
        
        if st.button("Calcola Interesse Composto", key="calc_compound"):
            try:
                results = calculate_compound_interest(
                    initial_investment, interest_rate_annual, investment_years, recurring_investment
                )
                display_compound_interest_results(results, interest_rate_annual, investment_years)
            except Exception as e:
                st.error("Errore nel calcolo. Verifica i valori inseriti.")
                st.exception(e)

def render_cagr_section():
    """Render CAGR calculator section"""
    with st.expander("🎯 Calcolo Rendimento Annuo Finale e Capitale Investito", expanded=False):
        st.subheader("Calcolo CAGR (Compound Annual Growth Rate)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
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
        
        if st.button("Calcola CAGR", key="calc_cagr"):
            try:
                cagr, total_return = calculate_cagr(initial_capital, final_capital, cagr_years)
                display_cagr_results(cagr, total_return, initial_capital, final_capital, cagr_years)
            except Exception as e:
                st.error("Errore nel calcolo. Verifica i valori inseriti.")
                st.exception(e)

def display_compound_interest_results(results, interest_rate_annual, investment_years):
    """Display compound interest calculation results"""
    st.success("**Risultati Interesse Composto:**")
    
    # Show warning for negative interest rates
    if interest_rate_annual < 0:
        st.warning(f"⚠️ **Tasso di interesse negativo ({format_percentage(interest_rate_annual)})** - L'investimento perde valore nel tempo!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**💰 Valori Finali:**")
        st.write(f"• **Valore Futuro dell'Investimento:** {format_currency(results['total_future_value'])}")
        st.write(f"• **Totale Investito:** {format_currency(results['total_invested'])}")
        
        # Color code gains/losses
        if results['total_gains'] >= 0:
            st.write(f"• **Guadagno Totale:** {format_currency(results['total_gains'])}")
        else:
            st.error(f"• **Perdita Totale:** {format_currency(results['total_gains'])}")
        
        st.write(f"• **Valore Futuro Investimento Iniziale:** {format_currency(results['fv_initial'])}")
        if results['fv_recurring'] > 0:
            st.write(f"• **Valore Futuro Investimenti Ricorrenti:** {format_currency(results['fv_recurring'])}")
    
    with col2:
        st.write("**📊 Analisi Performance:**")
        
        if interest_rate_annual < 0:
            # Calculate how much value is lost each year
            annual_loss_rate = abs(interest_rate_annual)
            st.error("**⚠️ Analisi Perdite:**")
            st.write(f"• Perdita annuale: {format_percentage(annual_loss_rate)}")
            st.write(f"• Valore perso totale: {format_currency(abs(results['total_gains']))}")
            if results['total_invested'] > 0:
                loss_percentage = (abs(results['total_gains']) / results['total_invested']) * 100
                st.write(f"• Percentuale di perdita: {format_percentage(loss_percentage)}")
        else:
            # Show positive return analysis
            if results['total_invested'] > 0:
                total_return_percentage = (results['total_gains'] / results['total_invested']) * 100
                st.write(f"• **Percentuale di Guadagno:** {format_percentage(total_return_percentage)}")
                
                # Calculate annualized return
                if investment_years > 0:
                    annualized_return = ((results['total_future_value'] / results['total_invested']) ** (1/investment_years) - 1) * 100
                    st.write(f"• **Rendimento Annualizzato:** {format_percentage(annualized_return)}")
                
                # Performance indicators
                if total_return_percentage > 100:
                    st.success("🚀 Rendimento eccellente (> 100%)")
                elif total_return_percentage > 50:
                    st.success("✅ Rendimento molto buono (> 50%)")
                elif total_return_percentage > 20:
                    st.info("📈 Rendimento buono (> 20%)")
                else:
                    st.info("📊 Rendimento modesto")

def display_cagr_results(cagr, total_return, initial_capital, final_capital, cagr_years):
    """Display CAGR calculation results"""
    st.success("**Risultati CAGR:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📈 Rendimenti:**")
        st.write(f"• **Rendimento Annuo Finale (CAGR):** {format_percentage(cagr * 100)}")
        st.write(f"• **Rendimento Totale:** {format_percentage(total_return * 100)}")
        st.write(f"• **Guadagno Assoluto:** {format_currency(final_capital - initial_capital)}")
        
        # CAGR performance analysis
        if cagr > 0.15:  # 15%
            st.success("🚀 CAGR eccellente (> 15%)")
        elif cagr > 0.10:  # 10%
            st.success("✅ CAGR molto buono (> 10%)")
        elif cagr > 0.05:  # 5%
            st.info("📈 CAGR buono (> 5%)")
        elif cagr > 0:
            st.info("📊 CAGR positivo")
        else:
            st.error("📉 CAGR negativo - perdita di valore")
    
    with col2:
        st.write("**💰 Capitali:**")
        st.write(f"• **Capitale Iniziale Investito:** {format_currency(initial_capital)}")
        st.write(f"• **Capitale Finale:** {format_currency(final_capital)}")
        st.write(f"• **Periodo di Investimento:** {cagr_years} anni")
        
        # Calculate equivalent simple interest rate
        if cagr_years > 0:
            simple_rate = total_return / cagr_years
            st.write(f"• **Rendimento Semplice Equivalente:** {format_percentage(simple_rate * 100)}/anno")
        
        # Time-based analysis
        if cagr_years < 2:
            st.info("ℹ️ Periodo breve - CAGR meno significativo")
        elif cagr_years > 10:
            st.info("📊 Periodo lungo - CAGR molto rappresentativo")
        else:
            st.info("📈 Periodo medio - CAGR rappresentativo")
