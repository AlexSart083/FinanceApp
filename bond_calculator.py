import streamlit as st
from datetime import date
from .financial_utils import (
    calculate_ytm_linear, generate_coupon_dates, find_last_coupon_before_purchase,
    calculate_precise_accrued_interest, count_remaining_coupons
)
from .ui_components import format_currency, format_percentage

def render_bond_section():
    """Render basic bond calculator section"""
    with st.expander("📊 Calcolo Base Obbligazioni", expanded=False):
        st.subheader("Calcolo Cedole e Rendimento Annuo Obbligazione")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nominal_value = st.number_input(
                "Valore Nominale (€)", 
                min_value=0.01, 
                value=1000.00,
                step=100.00,
                key="bond_nominal"
            )
            
            coupon_rate = st.number_input(
                "Tasso Cedolare Annuo (%)", 
                min_value=0.0, 
                max_value=50.0,
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
        
        if st.button("Calcola Obbligazione Base", key="calc_bond"):
            results = calculate_basic_bond(nominal_value, coupon_rate, purchase_price, years_to_maturity)
            display_bond_results(results)

def render_professional_bond_section():
    """Render professional bond calculator section with issue dates"""
    with st.expander("📊 Calcolatore Professionale Obbligazioni (con Data Emissione)", expanded=False):
        st.subheader("Calcolo Obbligazioni Professionale")
        st.info("💡 Calcolo completo con data emissione, ciclo cedolare preciso e rateo accurato")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**📋 Parametri Base Obbligazione**")
            
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
            
            coupon_frequency = st.selectbox(
                "Frequenza Pagamento Cedole",
                ["Annuale", "Semestrale", "Trimestrale"],
                index=1,
                key="prof_bond_frequency"
            )
            
            num_bonds = st.number_input(
                "Numero di Obbligazioni Acquistate", 
                min_value=1, 
                value=1,
                step=1,
                key="prof_bond_number"
            )
        
        with col2:
            st.write("**📅 Date Fondamentali**")
            
            issue_date = st.date_input(
                "📅 Data di Emissione", 
                value=date(2024, 2, 1),
                key="prof_bond_issue_date",
                format="DD/MM/YYYY"
            )
            
            first_coupon_date = st.date_input(
                "🎯 Data Primo Pagamento Interessi", 
                value=date(2025, 3, 19),
                key="prof_bond_first_coupon",
                format="DD/MM/YYYY"
            )
            
            purchase_date = st.date_input(
                "🛒 Data di Acquisto", 
                value=date(2025, 8, 6),
                key="prof_bond_purchase_date",
                format="DD/MM/YYYY"
            )
            
            maturity_date = st.date_input(
                "⏰ Data di Scadenza", 
                value=date(2026, 3, 19),
                min_value=purchase_date,
                key="prof_bond_maturity_date",
                format="DD/MM/YYYY"
            )
        
        with col3:
            st.write("**📊 Informazioni Calcolate**")
            
            days_since_issue = (purchase_date - issue_date).days
            days_to_maturity = (maturity_date - purchase_date).days
            years_to_maturity = days_to_maturity / 365.25
            
            st.write(f"**Giorni da Emissione:** {days_since_issue}")
            st.write(f"**Giorni a Scadenza:** {days_to_maturity}")
            st.write(f"**Anni a Scadenza:** {years_to_maturity:.3f}")
            
            periods_per_year = get_periods_per_year(coupon_frequency)
            st.write(f"**Cedole/Anno:** {periods_per_year}")
        
        if st.button("🚀 Calcola Obbligazione Professionale", key="calc_prof_bond"):
            try:
                results = calculate_professional_bond(
                    nominal_value, coupon_rate, purchase_price, coupon_frequency,
                    num_bonds, issue_date, first_coupon_date, purchase_date, maturity_date
                )
                display_professional_bond_results(results)
            except Exception as e:
                st.error(f"❌ Errore nel calcolo professionale: {str(e)}")

def calculate_basic_bond(nominal_value, coupon_rate, purchase_price, years_to_maturity):
    """Calculate basic bond metrics"""
    annual_coupon = nominal_value * (coupon_rate / 100)
    approximate_ytm = (annual_coupon + (nominal_value - purchase_price) / years_to_maturity) / purchase_price
    current_yield = annual_coupon / purchase_price
    
    return {
        'annual_coupon': annual_coupon,
        'approximate_ytm': approximate_ytm * 100,
        'current_yield': current_yield * 100,
        'total_return': annual_coupon * years_to_maturity + (nominal_value - purchase_price)
    }

def calculate_professional_bond(nominal_value, coupon_rate, purchase_price, coupon_frequency,
                              num_bonds, issue_date, first_coupon_date, purchase_date, maturity_date):
    """Calculate professional bond metrics with precise calculations"""
    
    # Validate dates
    if issue_date >= purchase_date:
        raise ValueError("La data di emissione deve essere precedente alla data di acquisto!")
    
    if first_coupon_date <= issue_date:
        raise ValueError("La data primo pagamento interessi deve essere successiva alla data di emissione!")
        
    if maturity_date <= purchase_date:
        raise ValueError("La data di scadenza deve essere successiva alla data di acquisto!")
    
    # Generate all coupon dates
    coupon_dates = generate_coupon_dates(issue_date, maturity_date, first_coupon_date, coupon_frequency)
    
    if not coupon_dates:
        raise ValueError("Impossibile generare le date delle cedole. Verifica i parametri.")
    
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
            days_since_issue = (purchase_date - issue_date).days
            days_to_first_coupon = (first_coupon_date - issue_date).days
            
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
    
    # Calculate dirty price and other metrics
    dirty_price = purchase_price + accrued_interest
    remaining_coupons = count_remaining_coupons(coupon_dates, purchase_date)
    
    # Calculate coupon amounts
    annual_coupon = nominal_value * (coupon_rate / 100)
    coupon_per_period = get_coupon_per_period(annual_coupon, coupon_frequency)
    
    # Calculate YTM and future cash flows
    days_to_maturity = (maturity_date - purchase_date).days
    total_future_coupons = coupon_per_period * remaining_coupons * num_bonds
    total_future_cash_flows = total_future_coupons + nominal_value * num_bonds
    
    if days_to_maturity > 0:
        ytm = calculate_ytm_linear(dirty_price, nominal_value, total_future_cash_flows / num_bonds, days_to_maturity)
    else:
        ytm = 0
    
    return {
        'coupon_dates': coupon_dates,
        'last_coupon': last_coupon,
        'next_coupon': next_coupon,
        'accrued_interest': accrued_interest,
        'dirty_price': dirty_price,
        'remaining_coupons': remaining_coupons,
        'annual_coupon': annual_coupon,
        'coupon_per_period': coupon_per_period,
        'total_future_coupons': total_future_coupons,
        'total_future_cash_flows': total_future_cash_flows,
        'ytm': ytm,
        'num_bonds': num_bonds,
        'nominal_value': nominal_value,
        'purchase_price': purchase_price,
        'issue_date': issue_date,
        'first_coupon_date': first_coupon_date,
        'purchase_date': purchase_date,
        'maturity_date': maturity_date,
        'days_to_maturity': days_to_maturity
    }

def get_periods_per_year(coupon_frequency):
    """Get number of coupon periods per year"""
    if coupon_frequency == "Semestrale":
        return 2
    elif coupon_frequency == "Trimestrale":
        return 4
    else:
        return 1

def get_coupon_per_period(annual_coupon, coupon_frequency):
    """Calculate coupon amount per period"""
    if coupon_frequency == "Semestrale":
        return annual_coupon / 2
    elif coupon_frequency == "Trimestrale":
        return annual_coupon / 4
    else:
        return annual_coupon

def display_bond_results(results):
    """Display basic bond calculation results"""
    st.success("**Risultati Obbligazione:**")
    st.write(f"💰 **Cedola Annuale:** {format_currency(results['annual_coupon'])}")
    st.write(f"📈 **Rendimento Annuo (YTM Approssimato):** {format_percentage(results['approximate_ytm'])}")
    st.write(f"📊 **Current Yield:** {format_percentage(results['current_yield'])}")
    st.write(f"🎯 **Rendimento Totale:** {format_currency(results['total_return'])}")

def display_professional_bond_results(results):
    """Display professional bond calculation results"""
    st.success("**🎯 Risultati Calcolo Professionale Obbligazione**")
    
    # Create detailed results layout
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.write("**📅 Analisi Date e Ciclo Cedolare:**")
        st.write(f"• Data Emissione: {results['issue_date'].strftime('%d/%m/%Y')}")
        st.write(f"• Primo Pagamento Interessi: {results['first_coupon_date'].strftime('%d/%m/%Y')}")
        st.write(f"• Data Acquisto: {results['purchase_date'].strftime('%d/%m/%Y')}")
        st.write(f"• Data Scadenza: {results['maturity_date'].strftime('%d/%m/%Y')}")
        if results['last_coupon']:
            st.write(f"• Ultimo Pagamento Cedola: {results['last_coupon'].strftime('%d/%m/%Y')}")
        else:
            st.write("• **Nessuna cedola ancora pagata**")
        if results['next_coupon']:
            st.write(f"• Prossima Cedola: {results['next_coupon'].strftime('%d/%m/%Y')}")
        else:
            st.write(f"• Prossima Cedola: {results['first_coupon_date'].strftime('%d/%m/%Y')}")
        st.write(f"• **Cedole Rimanenti: {results['remaining_coupons']}**")
        
    with res_col2:
        st.write("**💰 Analisi Prezzi e Cedole:**")
        st.write(f"• Cedola Annuale (per obbligazione): {format_currency(results['annual_coupon'])}")
        st.write(f"• Cedola per Periodo (per obbligazione): {format_currency(results['coupon_per_period'])}")
        st.write(f"• **Numero Obbligazioni: {results['num_bonds']}**")
        st.write(f"• **Prezzo Clean (per obbligazione): {format_currency(results['purchase_price'])}**")
        st.write(f"• **Rateo Interessi (per obbligazione): {format_currency(results['accrued_interest'])}**")
        st.write(f"• **Prezzo Dirty (per obbligazione): {format_currency(results['dirty_price'])}**")
        st.write(f"• **Investimento Totale: {format_currency(results['dirty_price'] * results['num_bonds'])}**")
        
    with res_col3:
        st.write("**📈 Rendimenti e Metriche:**")
        total_capital_at_end = results['total_future_cash_flows']
        total_investment = results['dirty_price'] * results['num_bonds']
        total_gain = total_capital_at_end - total_investment
        
        st.write(f"• **YTM (Yield to Maturity): {format_percentage(results['ytm'] * 100, 3)}**")
        st.write(f"• **Capitale Totale a Fine Investimento: {format_currency(total_capital_at_end)}**")
        st.write(f"• **Guadagno Totale a Fine Investimento: {format_currency(total_gain)}**")
    
    # Price analysis
    st.write("**📊 Analisi Aggiuntiva:**")
    analysis_col1, analysis_col2 = st.columns(2)
    
    with analysis_col1:
        if results['purchase_price'] < results['nominal_value']:
            discount = ((results['nominal_value'] - results['purchase_price']) / results['nominal_value']) * 100
            st.info(f"📉 Obbligazione acquistata **sotto la pari** (sconto: {format_percentage(discount)})")
        elif results['purchase_price'] > results['nominal_value']:
            premium = ((results['purchase_price'] - results['nominal_value']) / results['nominal_value']) * 100
            st.info(f"📈 Obbligazione acquistata **sopra la pari** (premio: {format_percentage(premium)})")
        else:
            st.info("📊 Obbligazione acquistata **alla pari**")
        
        # YTM vs Coupon analysis
        coupon_rate = (results['annual_coupon'] / results['nominal_value'])
        if results['ytm'] > coupon_rate:
            st.info("🔽 YTM > Tasso Cedolare: rendimento attraente")
        elif results['ytm'] < coupon_rate:
            st.info("🔼 YTM < Tasso Cedolare: pagato un premio")
        else:
            st.info("⚖️ YTM = Tasso Cedolare: pricing corretto")
    
    with analysis_col2:
        # Time analysis
        years_to_maturity = results['days_to_maturity'] / 365.25
        days_since_issue = (results['purchase_date'] - results['issue_date']).days
        
        st.write("**⏱️ Analisi Temporale:**")
        st.write(f"• Anni dalla Emissione: {days_since_issue/365.25:.2f}")
        st.write(f"• Anni rimanenti: {years_to_maturity:.3f}")
        
        # Risk indicators
        if years_to_maturity < 1:
            st.warning("⚠️ Scadenza a breve termine (< 1 anno)")
        elif years_to_maturity > 10:
            st.warning("⚠️ Scadenza a lungo termine (> 10 anni)")
    
    # Show coupon schedule (first 5 and last 5)
    if len(results['coupon_dates']) > 0:
        st.write("**📋 Calendario Cedole (Prime 5 e Ultime 5):**")
        schedule_col1, schedule_col2 = st.columns(2)
        
        with schedule_col1:
            st.write("**Prime 5 Cedole:**")
            for i, coupon_date in enumerate(results['coupon_dates'][:5]):
                if coupon_date <= results['purchase_date']:
                    status = "✅ Pagata"
                elif i == 0 and results['last_coupon'] is None:
                    status = "🔄 Prima cedola (in maturazione)"
                else:
                    status = "⏳ Futura"
                st.write(f"{i+1}. {coupon_date.strftime('%d/%m/%Y')} - {status}")
        
        with schedule_col2:
            if len(results['coupon_dates']) > 5:
                st.write("**Ultime 5 Cedole:**")
                for i, coupon_date in enumerate(results['coupon_dates'][-5:]):
                    if coupon_date <= results['purchase_date']:
                        status = "✅ Pagata"
                    else:
                        status = "⏳ Futura"
                    st.write(f"{len(results['coupon_dates'])-4+i}. {coupon_date.strftime('%d/%m/%Y')} - {status}")
