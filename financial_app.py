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

# Section 5: Real Estate Investment Calculator
with st.expander("🏘️ Calcolo Investimento Immobiliare", expanded=False):
    st.subheader("Analisi Investimento Immobiliare")
    st.info("💡 Calcolo completo con rivalutazione, inflazione e adeguamento affitti")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**🏠 Parametri Base Immobile**")
        
        valore_immobile = st.number_input(
            "Valore Immobile (€)", 
            min_value=1000.00, 
            value=200000.00,
            step=5000.00,
            key="real_estate_value"
        )
        
        affitto_lordo = st.number_input(
            "Affitto Lordo Annuo (€)", 
            min_value=0.00, 
            value=12000.00,
            step=100.00,
            key="real_estate_rent"
        )
        
        rivalutazione_annua = st.number_input(
            "Rivalutazione Annua (%)", 
            min_value=0.0, 
            max_value=20.0,
            value=2.5,
            step=0.1,
            key="real_estate_appreciation"
        )
        
        anni_investimento = st.number_input(
            "Anni di Investimento", 
            min_value=1, 
            value=10,
            step=1,
            key="real_estate_years"
        )
    
    with col2:
        st.write("**💸 Costi e Spese**")
        
        costi_assicurazione = st.number_input(
            "Costi Assicurazione Annui (€)", 
            min_value=0.00, 
            value=500.00,
            step=50.00,
            key="real_estate_insurance"
        )
        
        costi_condominiali = st.number_input(
            "Costi Condominiali Annui (€)", 
            min_value=0.00, 
            value=1200.00,
            step=100.00,
            key="real_estate_condo"
        )
        
        manutenzione_straordinaria_perc = st.number_input(
            "Manutenzione Straordinaria Annua (%)", 
            min_value=0.0, 
            max_value=10.0,
            value=0.5,
            step=0.1,
            key="real_estate_maintenance"
        )
        
        costi_aggiuntivi = st.number_input(
            "Costi Aggiuntivi Annui (€)", 
            min_value=0.00, 
            value=300.00,
            step=50.00,
            key="real_estate_additional"
        )
        
        tassazione_affitti_perc = st.number_input(
            "Tassazione su Affitti (%)", 
            min_value=0.0, 
            max_value=50.0,
            value=21.0,
            step=1.0,
            key="real_estate_tax_rate"
        )
        
        tassa_proprieta = st.number_input(
            "Tassa di Proprietà Annua (€)", 
            min_value=0.00, 
            value=800.00,
            step=50.00,
            key="real_estate_property_tax"
        )
    
    with col3:
        st.write("**📊 Parametri Economici**")
        
        periodo_sfitto_perc = st.number_input(
            "Periodo Annuo Sfitto (%)", 
            min_value=0.0, 
            max_value=100.0,
            value=5.0,
            step=1.0,
            key="real_estate_vacancy"
        )
        
        inflazione_perc = st.number_input(
            "Inflazione Annua (%)", 
            min_value=0.0, 
            max_value=15.0,
            value=2.0,
            step=0.1,
            key="real_estate_inflation"
        )
        
        st.write("**ℹ️ Note:**")
        st.write("• L'affitto si adegua ogni 4 anni")
        st.write("• al valore rivalutato dell'immobile")
        st.write("• Manutenzione calcolata sul valore")
        st.write("• dell'immobile rivalutato")
    
    # Real Estate calculations
    if st.button("🏠 Calcola Investimento Immobiliare", key="calc_real_estate"):
        try:
            # Convert percentages to decimals
            rivalutazione_decimal = rivalutazione_annua / 100
            inflazione_decimal = inflazione_perc / 100
            periodo_sfitto_decimal = periodo_sfitto_perc / 100
            manutenzione_decimal = manutenzione_straordinaria_perc / 100
            tassazione_decimal = tassazione_affitti_perc / 100
            
            # Initialize variables for year-by-year calculation
            valore_corrente = valore_immobile
            affitto_corrente = affitto_lordo
            
            # Lists to store annual data
            valori_annuali = []
            affitti_netti_annuali = []
            rendimenti_annuali = []
            
            # Calculate year by year
            for anno in range(1, anni_investimento + 1):
                # Update property value with appreciation
                valore_corrente = valore_corrente * (1 + rivalutazione_decimal)
                
                # Adjust rent every 4 years based on new property value
                if anno % 4 == 0:
                    # Calculate new rent as percentage of current property value
                    # Assuming initial rent was about 6% of property value, maintain same ratio
                    rapporto_affitto_iniziale = affitto_lordo / valore_immobile
                    affitto_corrente = valore_corrente * rapporto_affitto_iniziale
                
                # Calculate effective rent considering vacancy
                affitto_effettivo = affitto_corrente * (1 - periodo_sfitto_decimal)
                
                # Calculate taxes on rent
                tasse_affitto = affitto_effettivo * tassazione_decimal
                
                # Calculate annual costs
                manutenzione_annua = valore_corrente * manutenzione_decimal
                costi_totali_annui = (costi_assicurazione + costi_condominiali + 
                                    manutenzione_annua + costi_aggiuntivi + 
                                    tassa_proprieta + tasse_affitto)
                
                # Calculate net annual rent
                affitto_netto = affitto_effettivo - costi_totali_annui
                
                # Calculate annual yield on current property value
                rendimento_annuo = (affitto_netto / valore_immobile) * 100 if valore_immobile > 0 else 0
                
                # Store data
                valori_annuali.append(valore_corrente)
                affitti_netti_annuali.append(affitto_netto)
                rendimenti_annuali.append(rendimento_annuo)
            
            # Final calculations
            valore_finale_nominale = valori_annuali[-1]
            valore_finale_reale = valore_finale_nominale / ((1 + inflazione_decimal) ** anni_investimento)
            
            # Total net rent received over the period
            totale_affitti_netti = sum(affitti_netti_annuali)
            
            # Average annual net yield
            rendimento_medio_annuo = sum(rendimenti_annuali) / len(rendimenti_annuali)
            
            # Total return calculation
            guadagno_capitale_nominale = valore_finale_nominale - valore_immobile
            guadagno_capitale_reale = valore_finale_reale - valore_immobile
            
            rendimento_totale_nominale = totale_affitti_netti + guadagno_capitale_nominale
            rendimento_totale_reale = totale_affitti_netti + guadagno_capitale_reale
            
            # Display comprehensive results
            st.success("**🎯 Risultati Analisi Investimento Immobiliare**")
            
            # Create detailed results layout
            res_col1, res_col2, res_col3 = st.columns(3)
            
            with res_col1:
                st.write("**🏠 Valore Immobile:**")
                st.write(f"• Valore Iniziale: €{valore_immobile:,.2f}")
                st.write(f"• **Valore Finale (Nominale): €{valore_finale_nominale:,.2f}**")
                st.write(f"• **Valore Finale (Reale): €{valore_finale_reale:,.2f}**")
                st.write(f"• Guadagno Capitale (Nominale): €{guadagno_capitale_nominale:,.2f}")
                st.write(f"• Guadagno Capitale (Reale): €{guadagno_capitale_reale:,.2f}")
                st.write(f"• Rivalutazione Totale: {((valore_finale_nominale/valore_immobile - 1) * 100):.2f}%")
            
            with res_col2:
                st.write("**💰 Analisi Affitti:**")
                st.write(f"• Affitto Iniziale: €{affitto_lordo:,.2f}")
                st.write(f"• Affitto Finale: €{affitto_corrente:,.2f}")
                st.write(f"• **Totale Affitti Netti {anni_investimento} anni: €{totale_affitti_netti:,.2f}**")
                st.write(f"• **Rendimento Medio Annuo: {rendimento_medio_annuo:.2f}%**")
                st.write(f"• Periodo Sfitto Considerato: {periodo_sfitto_perc}%")
                st.write(f"• Adeguamenti Affitto: {anni_investimento // 4} volte")
            
            with res_col3:
                st.write("**📈 Rendimento Totale:**")
                st.write(f"• **Rendimento Totale (Nominale): €{rendimento_totale_nominale:,.2f}**")
                st.write(f"• **Rendimento Totale (Reale): €{rendimento_totale_reale:,.2f}**")
                rendimento_perc_nominale = (rendimento_totale_nominale / valore_immobile) * 100
                rendimento_perc_reale = (rendimento_totale_reale / valore_immobile) * 100
                st.write(f"• Rendimento % (Nominale): {rendimento_perc_nominale:.2f}%")
                st.write(f"• Rendimento % (Reale): {rendimento_perc_reale:.2f}%")
                
                # CAGR calculation
                cagr_nominale = ((valore_finale_nominale + totale_affitti_netti) / valore_immobile) ** (1/anni_investimento) - 1
                cagr_reale = ((valore_finale_reale + totale_affitti_netti) / valore_immobile) ** (1/anni_investimento) - 1
                st.write(f"• **CAGR (Nominale): {cagr_nominale:.2%}**")
                st.write(f"• **CAGR (Reale): {cagr_reale:.2%}**")
            
            # Detailed cost breakdown for the last year
            st.write("**💸 Dettaglio Costi Ultimo Anno:**")
            cost_col1, cost_col2 = st.columns(2)
            
            with cost_col1:
                ultima_manutenzione = valori_annuali[-1] * manutenzione_decimal
                ultimo_affitto_effettivo = affitto_corrente * (1 - periodo_sfitto_decimal)
                ultime_tasse_affitto = ultimo_affitto_effettivo * tassazione_decimal
                ultimi_costi_totali = (costi_assicurazione + costi_condominiali + 
                                     ultima_manutenzione + costi_aggiuntivi + 
                                     tassa_proprieta + ultime_tasse_affitto)
                
                st.write(f"• Assicurazione: €{costi_assicurazione:,.2f}")
                st.write(f"• Spese Condominiali: €{costi_condominiali:,.2f}")
                st.write(f"• Manutenzione Straordinaria: €{ultima_manutenzione:,.2f}")
                st.write(f"• Costi Aggiuntivi: €{costi_aggiuntivi:,.2f}")
                st.write(f"• **Tassa di Proprietà: €{tassa_proprieta:,.2f}**")
                st.write(f"• **Tasse su Affitti ({tassazione_affitti_perc}%): €{ultime_tasse_affitto:,.2f}**")
            
            with cost_col2:
                st.write(f"• **Totale Costi Annui: €{ultimi_costi_totali:,.2f}**")
                st.write(f"• Affitto Lordo: €{affitto_corrente:,.2f}")
                st.write(f"• Meno Periodo Sfitto: €{affitto_corrente * periodo_sfitto_decimal:,.2f}")
                st.write(f"• Affitto Effettivo: €{ultimo_affitto_effettivo:,.2f}")
                st.write(f"• **Affitto Netto Finale: €{affitti_netti_annuali[-1]:,.2f}**")
                
                # Calculate net yield after all costs and taxes
                rendimento_lordo_finale = (affitto_corrente / valore_finale_nominale) * 100
                rendimento_netto_finale = (affitti_netti_annuali[-1] / valore_immobile) * 100
                st.write(f"• Rendimento Lordo: {rendimento_lordo_finale:.2f}%")
                st.write(f"• **Rendimento Netto: {rendimento_netto_finale:.2f}%**")
            
            # Additional analysis
            st.write("**📊 Analisi Aggiuntiva:**")
            
            analysis_col1, analysis_col2 = st.columns(2)
            
            with analysis_col1:
                # Yield analysis
                gross_yield_initial = (affitto_lordo / valore_immobile) * 100
                gross_yield_final = (affitto_corrente / valore_finale_nominale) * 100
                
                st.write("**📈 Analisi Rendimenti:**")
                st.write(f"• Rendimento Lordo Iniziale: {gross_yield_initial:.2f}%")
                st.write(f"• Rendimento Lordo Finale: {gross_yield_final:.2f}%")
                st.write(f"• Rendimento Netto Medio: {rendimento_medio_annuo:.2f}%")
                
                # Break-even analysis
                break_even_years = valore_immobile / (sum(affitti_netti_annuali) / anni_investimento) if sum(affitti_netti_annuali) > 0 else float('inf')
                st.write(f"• Payback Period: {break_even_years:.1f} anni")
            
            with analysis_col2:
                st.write("**⚠️ Considerazioni:**")
                if rendimento_medio_annuo < 3:
                    st.warning("⚠️ Rendimento netto basso (< 3%)")
                elif rendimento_medio_annuo > 7:
                    st.success("✅ Rendimento netto interessante (> 7%)")
                else:
                    st.info("ℹ️ Rendimento netto moderato (3-7%)")
                
                if periodo_sfitto_perc > 10:
                    st.warning("⚠️ Periodo di sfitto elevato considerato")
                
                if rivalutazione_annua < inflazione_perc:
                    st.warning("⚠️ Rivalutazione < Inflazione: perdita valore reale")
                else:
                    st.info("✅ Rivalutazione > Inflazione: mantenimento valore reale")
            
        except Exception as e:
            st.error(f"❌ Errore nel calcolo immobiliare: {str(e)}")
            st.error("Verifica che tutti i valori siano corretti.")
            st.exception(e)

st.markdown("---")

# Corrected YTM calculation with proper formula
def calculate_ytm_linear(dirty_price, nominal_value, total_future_cash_flows, days_to_maturity):
    """Calculate YTM using linear approximation formula (market standard for short-term bonds)"""
    
    # Linear YTM formula: (Future Cash Flow / Dirty Price - 1) * (365 / days)
    if days_to_maturity > 0 and dirty_price > 0:
        ytm = ((total_future_cash_flows / dirty_price) - 1) * (365 / days_to_maturity)
        return ytm
    else:
        return 0

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

# Function to generate all coupon dates
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

# Function to find last coupon payment before purchase
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

# Function to calculate precise accrued interest
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

# Function to count remaining coupons
def count_remaining_coupons(coupon_dates, purchase_date):
    """Count remaining coupon payments after purchase date"""
    return len([date for date in coupon_dates if date > purchase_date])

# Section 1: Professional Bond Calculator
with st.expander("📊 Calcolatore Professionale Obbligazioni (con Data Emissione)", expanded=False):
    st.subheader("Calcolo Obbligazioni Professionale")
    st.info("💡 Calcolo completo con data emissione, ciclo cedolare preciso e rateo accurato")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**📋 Parametri Base Obbligazione**")
        
        # Basic bond parameters
        nominal_value = st.number_input(
            "Valore Nominale (€)", 
            min_value=0.01, 
            value=100.00,
            step=10.00,
            key="prof_bond_nominal"
        )
        
        coupon_rate = st.number_input(
            "Tasso Cedolare Annuo (%)", 
            min_value=0.0, 
            max_value=50.0,
            value=2.500,
            step=0.001,
            key="prof_bond_coupon"
        )
        
        purchase_price = st.number_input(
            "Prezzo Clean di Acquisto (€)", 
            min_value=0.01, 
            value=100.359,
            step=0.001,
            key="prof_bond_price"
        )
        
        # Coupon frequency
        coupon_frequency = st.selectbox(
            "Frequenza Pagamento Cedole",
            ["Annuale", "Semestrale", "Trimestrale"],
            index=1,  # Default to Semestrale
            key="prof_bond_frequency"
        )
        
        # Number of bonds purchased
        num_bonds = st.number_input(
            "Numero di Obbligazioni Acquistate", 
            min_value=1, 
            value=1,
            step=1,
            key="prof_bond_number"
        )
    
    with col2:
        st.write("**📅 Date Fondamentali**")
        
        # Issue date
        issue_date = st.date_input(
            "📅 Data di Emissione", 
            value=date(2024, 2, 1),
            key="prof_bond_issue_date",
            format="DD/MM/YYYY"
        )
        
        # First coupon date
        first_coupon_date = st.date_input(
            "🎯 Data Primo Pagamento Interessi", 
            value=date(2025, 3, 19),
            key="prof_bond_first_coupon",
            format="DD/MM/YYYY"
        )
        
        # Purchase date
        purchase_date = st.date_input(
            "🛒 Data di Acquisto", 
            value=date(2025, 8, 6),
            key="prof_bond_purchase_date",
            format="DD/MM/YYYY"
        )
        
        # Maturity date
        maturity_date = st.date_input(
            "⏰ Data di Scadenza", 
            value=date(2026, 3, 19),
            min_value=purchase_date,
            key="prof_bond_maturity_date",
            format="DD/MM/YYYY"
        )
    
    with col3:
        st.write("**📊 Informazioni Calcolate**")
        
        # Calculate preliminary info
        days_since_issue = (purchase_date - issue_date).days
        days_to_maturity = (maturity_date - purchase_date).days
        years_to_maturity = days_to_maturity / 365.25
        
        st.write(f"**Giorni da Emissione:** {days_since_issue}")
        st.write(f"**Giorni a Scadenza:** {days_to_maturity}")
        st.write(f"**Anni a Scadenza:** {years_to_maturity:.3f}")
        
        # Show coupon frequency info
        if coupon_frequency == "Semestrale":
            periods_per_year = 2
            st.write(f"**Cedole/Anno:** {periods_per_year}")
        elif coupon_frequency == "Trimestrale":
            periods_per_year = 4
            st.write(f"**Cedole/Anno:** {periods_per_year}")
        else:
            periods_per_year = 1
            st.write(f"**Cedole/Anno:** {periods_per_year}")
    
    # Professional bond calculations
    if st.button("🚀 Calcola Obbligazione Professionale", key="calc_prof_bond"):
        try:
            # Validate dates
            if issue_date >= purchase_date:
                st.error("❌ La data di emissione deve essere precedente alla data di acquisto!")
                st.stop()
            
            if first_coupon_date <= issue_date:
                st.error("❌ La data primo pagamento interessi deve essere successiva alla data di emissione!")
                st.stop()
                
            if maturity_date <= purchase_date:
                st.error("❌ La data di scadenza deve essere successiva alla data di acquisto!")
                st.stop()
            
            # Generate all coupon dates
            coupon_dates = generate_coupon_dates(issue_date, maturity_date, first_coupon_date, coupon_frequency)
            
            if not coupon_dates:
                st.error("❌ Impossibile generare le date delle cedole. Verifica i parametri.")
                st.stop()
            
            # Find last and next coupon relative to purchase
            last_coupon, next_coupon = find_last_coupon_before_purchase(coupon_dates, purchase_date)
            
            # Calculate precise accrued interest
            if last_coupon:
                accrued_interest = calculate_precise_accrued_interest(
                    nominal_value, coupon_rate, last_coupon, purchase_date, next_coupon
                )
            else:
                # If no coupon has been paid yet, calculate from issue date
                if purchase_date > issue_date:
                    # Calculate accrued interest from issue date to purchase date
                    days_since_issue = (purchase_date - issue_date).days
                    days_to_first_coupon = (first_coupon_date - issue_date).days
                    
                    # Determine coupon amount for the first period
                    annual_coupon = nominal_value * (coupon_rate / 100)
                    months_to_first_coupon = (first_coupon_date.year - issue_date.year) * 12 + (first_coupon_date.month - issue_date.month)
                    
                    if months_to_first_coupon <= 3:
                        first_coupon_amount = annual_coupon / 4
                    elif months_to_first_coupon <= 6:
                        first_coupon_amount = annual_coupon / 2
                    else:
                        first_coupon_amount = annual_coupon
                    
                    accrued_interest = first_coupon_amount * (days_since_issue / days_to_first_coupon)
                else:
                    accrued_interest = 0
            
            # Calculate dirty price
            dirty_price = purchase_price + accrued_interest
            
            # Count remaining coupons
            remaining_coupons = count_remaining_coupons(coupon_dates, purchase_date)
            
            # Calculate annual coupon and coupon per period
            annual_coupon = nominal_value * (coupon_rate / 100)
            
            if coupon_frequency == "Semestrale":
                coupon_per_period = annual_coupon / 2
            elif coupon_frequency == "Trimestrale":
                coupon_per_period = annual_coupon / 4
            else:
                coupon_per_period = annual_coupon
            
            # Calculate periods to maturity for YTM
            years_to_maturity_exact = days_to_maturity / 365.25
            
            if coupon_frequency == "Semestrale":
                periods_to_maturity = years_to_maturity_exact * 2
            elif coupon_frequency == "Trimestrale":
                periods_to_maturity = years_to_maturity_exact * 4
            else:
                periods_to_maturity = years_to_maturity_exact
            
            # Calculate total future coupons (adjusted for number of bonds)
            total_future_coupons = coupon_per_period * remaining_coupons * num_bonds
            
            # Calculate total future cash flows (adjusted for number of bonds)
            total_future_cash_flows = (total_future_coupons + nominal_value * num_bonds)
            
            # Calculate YTM using linear method (per single bond)
            if days_to_maturity > 0:
                ytm = calculate_ytm_linear(dirty_price, nominal_value, total_future_cash_flows / num_bonds, days_to_maturity)
            else:
                ytm = 0
            
            # Display results
            st.success("**🎯 Risultati Calcolo Professionale Obbligazione**")
            
            # Create detailed results layout
            res_col1, res_col2, res_col3 = st.columns(3)
            
            with res_col1:
                st.write("**📅 Analisi Date e Ciclo Cedolare:**")
                st.write(f"• Data Emissione: {issue_date.strftime('%d/%m/%Y')}")
                st.write(f"• Primo Pagamento Interessi: {first_coupon_date.strftime('%d/%m/%Y')}")
                st.write(f"• Data Acquisto: {purchase_date.strftime('%d/%m/%Y')}")
                st.write(f"• Data Scadenza: {maturity_date.strftime('%d/%m/%Y')}")
                if last_coupon:
                    st.write(f"• Ultimo Pagamento Cedola: {last_coupon.strftime('%d/%m/%Y')}")
                else:
                    st.write("• **Nessuna cedola ancora pagata**")
                if next_coupon:
                    st.write(f"• Prossima Cedola: {next_coupon.strftime('%d/%m/%Y')}")
                else:
                    st.write(f"• Prossima Cedola: {first_coupon_date.strftime('%d/%m/%Y')}")
                st.write(f"• **Cedole Rimanenti: {remaining_coupons}**")
                
            with res_col2:
                st.write("**💰 Analisi Prezzi e Cedole:**")
                st.write(f"• Cedola Annuale (per obbligazione): €{annual_coupon:.2f}")
                st.write(f"• Cedola per Periodo (per obbligazione): €{coupon_per_period:.2f}")
                st.write(f"• Frequenza: {coupon_frequency}")
                st.write(f"• **Numero Obbligazioni: {num_bonds}**")
                st.write(f"• **Prezzo Clean (per obbligazione): €{purchase_price:.2f}**")
                st.write(f"• **Rateo Interessi (per obbligazione): €{accrued_interest:.2f}**")
                st.write(f"• **Prezzo Dirty (per obbligazione): €{dirty_price:.2f}**")
                st.write(f"• **Investimento Totale: €{dirty_price * num_bonds:.2f}**")
                
            with res_col3:
                st.write("**📈 Rendimenti e Metriche:**")
                # Calculate total capital at end of investment (coupons + principal repayment)
                total_capital_at_end = total_future_coupons + (nominal_value * num_bonds)
                
                # Calculate total gain (total capital at end - total dirty price paid)
                total_investment = dirty_price * num_bonds
                total_gain = total_capital_at_end - total_investment
                
                st.write(f"• **YTM (Yield to Maturity): {ytm:.3%}**")
                st.write(f"• **Capitale Totale a Fine Investimento: €{total_capital_at_end:.2f}**")
                st.write(f"• **Guadagno Totale a Fine Investimento: €{total_gain:.2f}**")
                
            # Calculate current yield
            current_yield = (annual_coupon / purchase_price) * 100
            
            # Additional analysis
            st.write("**📊 Analisi Aggiuntiva:**")
            
            analysis_col1, analysis_col2 = st.columns(2)
            
            with analysis_col1:
                # Price analysis
                if purchase_price < nominal_value:
                    discount = ((nominal_value - purchase_price) / nominal_value) * 100
                    st.info(f"📉 Obbligazione acquistata **sotto la pari** (sconto: {discount:.2f}%)")
                elif purchase_price > nominal_value:
                    premium = ((purchase_price - nominal_value) / nominal_value) * 100
                    st.info(f"📈 Obbligazione acquistata **sopra la pari** (premio: {premium:.2f}%)")
                else:
                    st.info("📊 Obbligazione acquistata **alla pari**")
                
                # YTM vs Coupon analysis
                if ytm > coupon_rate / 100:
                    st.info("🔽 YTM > Tasso Cedolare: rendimento attraente")
                elif ytm < coupon_rate / 100:
                    st.info("🔼 YTM < Tasso Cedolare: pagato un premio")
                else:
                    st.info("⚖️ YTM = Tasso Cedolare: pricing corretto")
            
            with analysis_col2:
                # Time analysis
                st.write("**⏱️ Analisi Temporale:**")
                st.write(f"• Anni dalla Emissione: {days_since_issue/365.25:.2f}")
                st.write(f"• Anni rimanenti: {years_to_maturity:.3f}")
                st.write(f"• Periodi cedolari rimanenti: {periods_to_maturity:.2f}")
                
                # Risk indicators
                if years_to_maturity < 1:
                    st.warning("⚠️ Scadenza a breve termine (< 1 anno)")
                elif years_to_maturity > 10:
                    st.warning("⚠️ Scadenza a lungo termine (> 10 anni)")
            
            # Show coupon schedule (first 5 and last 5)
            if len(coupon_dates) > 0:
                st.write("**📋 Calendario Cedole (Prime 5 e Ultime 5):**")
                schedule_col1, schedule_col2 = st.columns(2)
                
                with schedule_col1:
                    st.write("**Prime 5 Cedole:**")
                    for i, coupon_date in enumerate(coupon_dates[:5]):
                        if coupon_date <= purchase_date:
                            status = "✅ Pagata"
                        elif i == 0 and last_coupon is None:
                            status = "🔄 Prima cedola (in maturazione)"
                        else:
                            status = "⏳ Futura"
                        st.write(f"{i+1}. {coupon_date.strftime('%d/%m/%Y')} - {status}")
                
                with schedule_col2:
                    if len(coupon_dates) > 5:
                        st.write("**Ultime 5 Cedole:**")
                        for i, coupon_date in enumerate(coupon_dates[-5:]):
                            if coupon_date <= purchase_date:
                                status = "✅ Pagata"
                            else:
                                status = "⏳ Futura"
                            st.write(f"{len(coupon_dates)-4+i}. {coupon_date.strftime('%d/%m/%Y')} - {status}")
            
        except Exception as e:
            st.error(f"❌ Errore nel calcolo professionale: {str(e)}")
            st.error("Verifica che tutte le date e i valori siano corretti.")
            st.exception(e)

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

st.markdown("*Sviluppato per calcoli finanziari di base. Consultare sempre un consulente finanziario qualificato per decisioni di investimento.*")
