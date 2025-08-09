# Correzione nel file investment_calculator.py
# Sostituire la funzione render_compound_interest_section

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
                # CORREZIONE: Gestione corretta della frequenza mensile
                results = calculate_compound_interest_with_inflation_corrected(
                    initial_investment, interest_rate_annual, investment_years, 
                    recurring_investment, inflation_rate, recurring_frequency
                )
                display_compound_interest_results_with_inflation(
                    results, interest_rate_annual, inflation_rate, investment_years
                )
            except Exception as e:
                st.error("Errore nel calcolo. Verifica i valori inseriti.")
                st.exception(e)

# NUOVA FUNZIONE CORRETTA per gestire investimenti mensili
def calculate_compound_interest_with_inflation_corrected(initial_investment, interest_rate_annual, 
                                                       investment_years, recurring_investment=0, 
                                                       inflation_rate=2.0, frequency="Annuale"):
    """Calculate future value with compound interest, recurring investments and inflation analysis - CORRECTED for monthly investments"""
    
    # Calcoli nominali (senza considerare inflazione)
    if frequency == "Mensile":
        # Per investimenti mensili, utilizziamo un calcolo diverso
        base_results = calculate_compound_interest_monthly(
            initial_investment, interest_rate_annual, investment_years, recurring_investment
        )
    else:
        # Per investimenti annuali, utilizziamo il calcolo originale
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

# NUOVA FUNZIONE per calcolo con investimenti mensili
def calculate_compound_interest_monthly(initial_investment, interest_rate_annual, investment_years, monthly_investment_annual=0):
    """Calculate future value with compound interest for monthly recurring investments"""
    
    # Converti parametri
    monthly_rate = (interest_rate_annual / 100) / 12
    total_months = investment_years * 12
    monthly_investment = monthly_investment_annual / 12 if monthly_investment_annual > 0 else 0
    
    # Future Value del capitale iniziale
    fv_initial = initial_investment * (1 + monthly_rate) ** total_months
    
    # Future Value degli investimenti mensili ricorrenti
    if monthly_investment > 0 and monthly_rate != 0:
        # Formula per annuity future value con capitalizzazione mensile
        fv_recurring = monthly_investment * (((1 + monthly_rate) ** total_months - 1) / monthly_rate)
    elif monthly_investment > 0 and monthly_rate == 0:
        # Se il tasso è 0, somma semplice
        fv_recurring = monthly_investment * total_months
    else:
        fv_recurring = 0
    
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
