import streamlit as st
from financial_utils import calculate_compound_interest, calculate_cagr
from ui_components import format_currency, format_percentage

def render_compound_interest_section():
    """Render compound interest calculator section with inflation analysis"""
    with st.expander("📈 Calcolo Interesse Composto", expanded=False):
        st.subheader("Calcolo Investimento con Interesse Composto")
        st.info("💡 Calcolo completo con analisi inflazione e potere d'acquisto reale")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**💰 Parametri Investimento**")
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
            
            investment_years = st.number_input(
                "Numero di Anni", 
                min_value=1, 
                value=10,
                step=1,
                key="compound_years"
            )
        
        with col2:
            st.write("**🔄 Investimenti Ricorrenti**")
            recurring_investment = st.number_input(
                "Investimento Ricorrente Annuo (€)", 
                min_value=0.00, 
                value=1200.00,
                step=100.00,
                key="compound_recurring",
                help="Importo investito ogni anno in aggiunta al capitale iniziale"
            )
            
            recurring_frequency = st.selectbox(
                "Frequenza Investimenti Ricorrenti",
                ["Annuale", "Mensile"],
                index=0,
                key="compound_frequency",
                help="Frequenza con cui vengono effettuati gli investimenti ricorrenti"
            )
        
        with col3:
            st.write("**📊 Parametri Economici**")
            inflation_rate = st.number_input(
                "Tasso di Inflazione Annuo (%)", 
                min_value=0.0, 
                max_value=20.0,
                value=2.0,
                step=0.1,
                key="compound_inflation",
                help="Tasso di inflazione medio atteso per il periodo"
            )
            
            # Calcolo automatico del rendimento reale
            real_return = interest_rate_annual - inflation_rate
            if real_return >= 0:
                st.success(f"📈 **Rendimento Reale:** {format_percentage(real_return)}")
            else:
                st.error(f"📉 **Rendimento Reale:** {format_percentage(real_return)}")
                st.warning("⚠️ Rendimento negativo dopo inflazione!")
            
            st.write("**ℹ️ Note:**")
            st.write("• Rendimento reale = Rendimento nominale - Inflazione")
            st.write("• Valori reali mostrano il potere d'acquisto effettivo")
        
        if st.button("📊 Calcola Interesse Composto con Inflazione", key="calc_compound"):
            try:
                # Adatta il calcolo in base alla frequenza
                if recurring_frequency == "Mensile":
                    monthly_investment = recurring_investment / 12
                    adjusted_recurring = recurring_investment
                else:
                    monthly_investment = 0
                    adjusted_recurring = recurring_investment
                
                results = calculate_compound_interest_with_inflation(
                    initial_investment, interest_rate_annual, investment_years, 
                    adjusted_recurring, inflation_rate, recurring_frequency
                )
                display_compound_interest_results_with_inflation(
                    results, interest_rate_annual, inflation_rate, investment_years
                )
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

def calculate_compound_interest_with_inflation(initial_investment, interest_rate_annual, 
                                             investment_years, recurring_investment=0, 
                                             inflation_rate=2.0, frequency="Annuale"):
    """Calculate future value with compound interest, recurring investments and inflation analysis"""
    
    # Calcoli nominali (senza considerare inflazione)
    base_results = calculate_compound_interest(
        initial_investment, interest_rate_annual, investment_years, recurring_investment
    )
    
    # Calcoli reali (considerando inflazione)
    real_interest_rate = interest_rate_annual - inflation_rate
    real_results = calculate_compound_interest(
        initial_investment, real_interest_rate, investment_years, recurring_investment
    )
    
    # Calcolo del potere d'acquisto del valore futuro nominale
    inflation_factor = (1 + inflation_rate / 100) ** investment_years
    future_value_real_purchasing_power = base_results['total_future_value'] / inflation_factor
    
    # Calcolo di quanto denaro servirebbe oggi per avere lo stesso potere d'acquisto
    equivalent_today_value = base_results['total_future_value'] / inflation_factor
    
    # Perdita di potere d'acquisto per l'inflazione
    purchasing_power_loss = base_results['total_future_value'] - future_value_real_purchasing_power
    
    return {
        'nominal_results': base_results,
        'real_results': real_results,
        'real_interest_rate': real_interest_rate,
        'inflation_factor': inflation_factor,
        'future_value_real_purchasing_power': future_value_real_purchasing_power,
        'equivalent_today_value': equivalent_today_value,
        'purchasing_power_loss': purchasing_power_loss,
        'inflation_rate': inflation_rate
    }

def display_compound_interest_results_with_inflation(results, interest_rate_annual, 
                                                   inflation_rate, investment_years):
    """Display compound interest calculation results with inflation analysis"""
    st.success("**📊 Risultati Interesse Composto con Analisi Inflazione**")
    
    # Show warning for negative real interest rates
    real_rate = results['real_interest_rate']
    if real_rate < 0:
        st.error(f"⚠️ **Rendimento reale negativo ({format_percentage(real_rate)})** - L'investimento perde potere d'acquisto!")
    elif real_rate < 1:
        st.warning(f"⚠️ **Rendimento reale basso ({format_percentage(real_rate)})** - Crescita limitata del potere d'acquisto")
    else:
        st.success(f"✅ **Rendimento reale positivo ({format_percentage(real_rate)})** - Crescita del potere d'acquisto")
    
    # Risultati principali
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**💰 Valori Nominali (Senza Inflazione):**")
        nominal = results['nominal_results']
        st.write(f"• **Valore Futuro Nominale:** {format_currency(nominal['total_future_value'])}")
        st.write(f"• **Totale Investito:** {format_currency(nominal['total_invested'])}")
        
        if nominal['total_gains'] >= 0:
            st.write(f"• **Guadagno Nominale:** {format_currency(nominal['total_gains'])}")
        else:
            st.error(f"• **Perdita Nominale:** {format_currency(nominal['total_gains'])}")
        
        if nominal['total_invested'] > 0:
            nominal_return_percentage = (nominal['total_gains'] / nominal['total_invested']) * 100
            st.write(f"• **Rendimento Nominale:** {format_percentage(nominal_return_percentage)}")
    
    with col2:
        st.write("**🔥 Valori Reali (Dopo Inflazione):**")
        real = results['real_results']
        st.write(f"• **Valore Futuro Reale:** {format_currency(real['total_future_value'])}")
        st.write(f"• **Potere d'Acquisto Futuro:** {format_currency(results['future_value_real_purchasing_power'])}")
        
        if real['total_gains'] >= 0:
            st.write(f"• **Guadagno Reale:** {format_currency(real['total_gains'])}")
        else:
            st.error(f"• **Perdita Reale:** {format_currency(real['total_gains'])}")
        
        st.write(f"• **Perdita per Inflazione:** {format_currency(results['purchasing_power_loss'])}")
        
        if real['total_invested'] > 0:
            real_return_percentage = (real['total_gains'] / real['total_invested']) * 100
            st.write(f"• **Rendimento Reale:** {format_percentage(real_return_percentage)}")
    
    with col3:
        st.write("**📊 Analisi Inflazione:**")
        st.write(f"• **Tasso Inflazione:** {format_percentage(inflation_rate)}")
        st.write(f"• **Fattore Inflazione {investment_years} anni:** {results['inflation_factor']:.3f}")
        
        # Calcolo di quanto l'euro vale meno dopo l'inflazione
        euro_devaluation = (1 - (1 / results['inflation_factor'])) * 100
        st.write(f"• **Svalutazione Euro:** {format_percentage(euro_devaluation)}")
        
        # Equivalenza di potere d'acquisto
        st.write(f"• **{format_currency(results['nominal_results']['total_future_value'])} futuri**")
        st.write(f"  equivalgono a **{format_currency(results['equivalent_today_value'])}** di oggi")
        
        # Performance comparison
        if results['real_results']['total_gains'] > 0:
            st.success("✅ Investimento batte l'inflazione")
        elif results['real_results']['total_gains'] == 0:
            st.info("⚖️ Investimento pareggia l'inflazione")
        else:
            st.error("❌ Investimento perde contro l'inflazione")
    
    # Analisi dettagliata performance
    st.write("**📈 Analisi Performance Dettagliata:**")
    performance_col1, performance_col2 = st.columns(2)
    
    with performance_col1:
        st.write("**Confronto Rendimenti:**")
        st.write(f"• Rendimento Nominale: {format_percentage(interest_rate_annual)}")
        st.write(f"• Tasso Inflazione: {format_percentage(inflation_rate)}")
        st.write(f"• **Rendimento Reale: {format_percentage(results['real_interest_rate'])}**")
        
        # Calcolo rendimenti annualizzati
        if investment_years > 0:
            nominal_annualized = ((results['nominal_results']['total_future_value'] / 
                                 results['nominal_results']['total_invested']) ** (1/investment_years) - 1) * 100
            real_annualized = ((results['real_results']['total_future_value'] / 
                              results['real_results']['total_invested']) ** (1/investment_years) - 1) * 100
            
            st.write(f"• Rendimento Annualizzato Nominale: {format_percentage(nominal_annualized)}")
            st.write(f"• **Rendimento Annualizzato Reale: {format_percentage(real_annualized)}**")
    
    with performance_col2:
        st.write("**Impatto Inflazione:**")
        
        # Calcolo percentuale di perdita per inflazione
        if results['nominal_results']['total_future_value'] > 0:
            inflation_impact_percentage = (results['purchasing_power_loss'] / 
                                         results['nominal_results']['total_future_value']) * 100
            st.write(f"• Perdita % per Inflazione: {format_percentage(inflation_impact_percentage)}")
        
        # Anni necessari per raddoppiare il potere d'acquisto
        if results['real_interest_rate'] > 0:
            years_to_double_real = 72 / results['real_interest_rate']  # Regola del 72
            st.write(f"• Anni per raddoppiare (reale): {years_to_double_real:.1f}")
        
        # Raccomandazioni basate sui risultati
        if results['real_interest_rate'] < 0:
            st.error("🚨 Considera investimenti con rendimenti più alti")
        elif results['real_interest_rate'] < 2:
            st.warning("⚠️ Rendimento reale modesto, valuta alternative")
        elif results['real_interest_rate'] > 5:
            st.success("🚀 Ottimo rendimento reale!")
        else:
            st.info("📊 Rendimento reale accettabile")

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
