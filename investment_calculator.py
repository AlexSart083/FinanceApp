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
                results = calculate_compound_interest_with_inflation(
                    initial_investment, interest_rate_annual, investment_years, 
                    recurring_investment, inflation_rate, recurring_frequency
                )
                display_compound_interest_results_with_inflation(
                    results, interest_rate_annual, inflation_rate, investment_years, recurring_frequency
                )
            except Exception as e:
                st.error("Errore nel calcolo. Verifica i valori inseriti.")
                st.exception(e)

def render_cagr_section():
    """Render CAGR calculator section"""
    with st.expander("📊 Calcolo CAGR (Compound Annual Growth Rate)", expanded=False):
        st.subheader("Calcolo Rendimento Annuo Composto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            initial_capital = st.number_input(
                "Capitale Iniziale (€)", 
                min_value=0.01, 
                value=10000.00,
                step=100.00,
                key="cagr_initial"
            )
            
            final_capital = st.number_input(
                "Capitale Finale (€)", 
                min_value=0.01, 
                value=15000.00,
                step=100.00,
                key="cagr_final"
            )
        
        with col2:
            investment_years = st.number_input(
                "Periodo di Investimento (Anni)", 
                min_value=1, 
                value=5,
                step=1,
                key="cagr_years"
            )
            
            # Preview calculation
            if initial_capital > 0 and investment_years > 0:
                preview_cagr, preview_total_return = calculate_cagr(initial_capital, final_capital, investment_years)
                st.info(f"📊 **CAGR Preview:** {format_percentage(preview_cagr * 100)}")
        
        if st.button("📈 Calcola CAGR", key="calc_cagr"):
            try:
                results = calculate_cagr_metrics(initial_capital, final_capital, investment_years)
                display_cagr_results(results)
            except Exception as e:
                st.error("Errore nel calcolo. Verifica i valori inseriti.")
                st.exception(e)

def calculate_compound_interest_with_inflation(initial_investment, interest_rate_annual, 
                                             investment_years, recurring_investment=0, 
                                             inflation_rate=2.0, frequency="Annuale"):
    """Calculate future value with compound interest, recurring investments and inflation analysis"""
    
    # Calcoli nominali (senza considerare inflazione)
    if frequency == "Mensile":
        base_results = calculate_compound_interest_monthly(
            initial_investment, interest_rate_annual, investment_years, recurring_investment
        )
    else:
        base_results = calculate_compound_interest(
            initial_investment, interest_rate_annual, investment_years, recurring_investment
        )
    
    # Calcoli reali (considerando inflazione)
    real_interest_rate = interest_rate_annual - inflation_rate
    if frequency == "Mensile":
        real_results = calculate_compound_interest_monthly(
            initial_investment, real_interest_rate, investment_years, recurring_investment
        )
    else:
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
        'inflation_rate': inflation_rate,
        'frequency': frequency
    }

def calculate_compound_interest_monthly(initial_investment, interest_rate_annual, investment_years, monthly_investment_annual=0):
    """Calculate future value with compound interest for monthly recurring investments and monthly compounding"""
    
    # Converti parametri - CORRETTO: tasso mensile con capitalizzazione mensile
    monthly_rate = (interest_rate_annual / 100) / 12
    total_months = investment_years * 12
    monthly_investment = monthly_investment_annual / 12 if monthly_investment_annual > 0 else 0
    
    # Future Value del capitale iniziale con capitalizzazione mensile
    fv_initial = initial_investment * (1 + monthly_rate) ** total_months
    
    # Future Value degli investimenti mensili ricorrenti
    # Ogni investimento mensile viene capitalizzato per il numero di mesi rimanenti
    fv_recurring = 0
    if monthly_investment > 0:
        for month in range(total_months):
            # Ogni investimento mensile viene capitalizzato per (total_months - month - 1) mesi
            months_to_compound = total_months - month
            if monthly_rate != 0:
                fv_recurring += monthly_investment * (1 + monthly_rate) ** (months_to_compound - 1)
            else:
                fv_recurring += monthly_investment
    
    # Totali
    total_future_value = fv_initial + fv_recurring
    total_invested = initial_investment + (monthly_investment_annual * investment_years)
    total_gains = total_future_value - total_invested
    
    return {
        'total_future_value': total_future_value,
        'fv_initial': fv_initial,
        'fv_recurring': fv_recurring,
        'total_invested': total_invested,
        'total_gains': total_gains
    }

def calculate_cagr_metrics(initial_capital, final_capital, investment_years):
    """Calculate CAGR and related metrics"""
    cagr, total_return = calculate_cagr(initial_capital, final_capital, investment_years)
    
    absolute_gain = final_capital - initial_capital
    
    return {
        'cagr': cagr,
        'total_return': total_return,
        'absolute_gain': absolute_gain,
        'initial_capital': initial_capital,
        'final_capital': final_capital,
        'investment_years': investment_years
    }

def display_compound_interest_results_with_inflation(results, interest_rate_annual, inflation_rate, investment_years, frequency="Annuale"):
    """Display compound interest results with inflation analysis"""
    st.success("**🎯 Risultati Interesse Composto con Analisi Inflazione**")
    
    # Mostra il tipo di capitalizzazione
    if frequency == "Mensile":
        st.info("📅 **Capitalizzazione MENSILE** - Gli interessi vengono reinvestiti ogni mese")
    else:
        st.info("📅 **Capitalizzazione ANNUALE** - Gli interessi vengono reinvestiti ogni anno")
    
    # Create main results layout
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.write("**💰 Valori Nominali (Non Aggiustati per Inflazione):**")
        st.write(f"• **Valore Futuro Totale: {format_currency(results['nominal_results']['total_future_value'])}**")
        st.write(f"• Guadagno Totale: {format_currency(results['nominal_results']['total_gains'])}")
        st.write(f"• Capitale Investito: {format_currency(results['nominal_results']['total_invested'])}")
        
        # Return calculation
        if results['nominal_results']['total_invested'] > 0:
            nominal_return_rate = (results['nominal_results']['total_gains'] / results['nominal_results']['total_invested']) * 100
            st.write(f"• Rendimento Totale: {format_percentage(nominal_return_rate)}")
    
    with res_col2:
        st.write("**🔍 Valori Reali (Aggiustati per Inflazione):**")
        st.write(f"• **Valore Futuro Reale: {format_currency(results['real_results']['total_future_value'])}**")
        st.write(f"• Guadagno Reale: {format_currency(results['real_results']['total_gains'])}")
        st.write(f"• **Potere d'Acquisto Finale: {format_currency(results['future_value_real_purchasing_power'])}**")
        
        # Real return calculation
        if results['nominal_results']['total_invested'] > 0:
            real_return_rate = (results['real_results']['total_gains'] / results['nominal_results']['total_invested']) * 100
            st.write(f"• Rendimento Reale: {format_percentage(real_return_rate)}")
        
        st.write(f"• Tasso Interesse Reale: {format_percentage(results['real_interest_rate'])}")
    
    with res_col3:
        st.write("**📊 Analisi Inflazione:**")
        st.write(f"• Tasso Inflazione: {format_percentage(inflation_rate)}")
        st.write(f"• **Perdita Potere d'Acquisto: {format_currency(results['purchasing_power_loss'])}**")
        st.write(f"• Fattore Inflazione {investment_years} anni: {results['inflation_factor']:.3f}")
        
        # Inflation impact analysis
        inflation_impact_percentage = (results['purchasing_power_loss'] / results['nominal_results']['total_future_value']) * 100
        st.write(f"• % Impatto Inflazione: {format_percentage(inflation_impact_percentage)}")
        
        if results['real_interest_rate'] <= 0:
            st.error("⚠️ Rendimento reale negativo!")
        elif results['real_interest_rate'] < 2:
            st.warning("⚠️ Rendimento reale basso")
        else:
            st.success("✅ Rendimento reale positivo")
    
    # Additional analysis with frequency comparison
    st.write("**📈 Analisi Dettagliata:**")
    analysis_col1, analysis_col2 = st.columns(2)
    
    with analysis_col1:
        st.write("**💡 Confronto Scenari:**")
        st.write(f"• Con Inflazione {format_percentage(inflation_rate)}: {format_currency(results['real_results']['total_future_value'])}")
        st.write(f"• Senza Inflazione: {format_currency(results['nominal_results']['total_future_value'])}")
        
        difference = results['nominal_results']['total_future_value'] - results['real_results']['total_future_value']
        st.write(f"• **Differenza: {format_currency(difference)}**")
        
        # Frequency information with comparison
        if frequency == "Mensile":
            st.success("📅 **Capitalizzazione Mensile:** Maggior effetto compounding")
            # Calculate what it would be with annual compounding for comparison
            annual_results = calculate_compound_interest(
                results['nominal_results']['total_invested'] - (results['nominal_results']['total_invested'] - results['nominal_results']['fv_initial']),
                interest_rate_annual, 
                investment_years, 
                (results['nominal_results']['total_invested'] - results['nominal_results']['fv_initial']) if results['nominal_results']['total_invested'] > results['nominal_results']['fv_initial'] else 0
            )
            if annual_results['total_future_value'] != results['nominal_results']['total_future_value']:
                advantage = results['nominal_results']['total_future_value'] - annual_results['total_future_value']
                st.info(f"💰 Vantaggio vs Annuale: {format_currency(advantage)}")
        else:
            st.info("📅 **Capitalizzazione Annuale:** Standard per investimenti")
    
    with analysis_col2:
        st.write("**🎯 Raccomandazioni:**")
        
        if results['real_interest_rate'] > 5:
            st.success("🚀 Rendimento reale eccellente (>5%)")
        elif results['real_interest_rate'] > 2:
            st.info("📈 Rendimento reale buono (2-5%)")
        elif results['real_interest_rate'] > 0:
            st.warning("⚠️ Rendimento reale modesto (0-2%)")
        else:
            st.error("📉 Rendimento reale negativo - perdita potere d'acquisto")
        
        # Investment strategy suggestion
        if inflation_rate > interest_rate_annual:
            st.error("🚨 Inflazione > Rendimento: considera investimenti più remunerativi")
        elif interest_rate_annual - inflation_rate < 1:
            st.warning("⚠️ Margine inflazione ridotto: monitora l'evoluzione dei tassi")
        else:
            st.success("✅ Buon margine contro l'inflazione")
        
        # Frequency recommendation
        if frequency == "Annuale":
            st.info("💡 Considera investimenti mensili per maggior compounding")

def display_cagr_results(results):
    """Display CAGR calculation results"""
    st.success("**Risultati CAGR:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 Metriche di Rendimento:**")
        st.write(f"• **CAGR (Tasso Crescita Annuale Composto): {format_percentage(results['cagr'] * 100)}**")
        st.write(f"• **Rendimento Totale: {format_percentage(results['total_return'] * 100)}**")
        st.write(f"• **Guadagno Assoluto: {format_currency(results['absolute_gain'])}**")
        
        # Performance evaluation
        if results['cagr'] > 0.15:
            st.success("🚀 Rendimento eccellente (>15% annuo)")
        elif results['cagr'] > 0.10:
            st.success("📈 Buon rendimento (10-15% annuo)")
        elif results['cagr'] > 0.05:
            st.info("📊 Rendimento moderato (5-10% annuo)")
        elif results['cagr'] > 0:
            st.warning("⚠️ Rendimento basso (0-5% annuo)")
        else:
            st.error("📉 Perdita di valore")
    
    with col2:
        st.write("**💰 Riepilogo Investimento:**")
        st.write(f"• Capitale Iniziale: {format_currency(results['initial_capital'])}")
        st.write(f"• **Capitale Finale: {format_currency(results['final_capital'])}**")
        st.write(f"• Periodo: {results['investment_years']} anni")
        
        # Additional metrics
        average_annual_gain = results['absolute_gain'] / results['investment_years'] if results['investment_years'] > 0 else 0
        st.write(f"• Guadagno Medio Annuo: {format_currency(average_annual_gain)}")
        
        # Investment efficiency
        roi_percentage = (results['absolute_gain'] / results['initial_capital']) * 100 if results['initial_capital'] > 0 else 0
        st.write(f"• ROI Totale: {format_percentage(roi_percentage)}")
