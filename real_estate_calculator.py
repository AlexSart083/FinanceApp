import streamlit as st
from ui_components import format_currency, format_percentage

def render_real_estate_section():
    """Render real estate investment calculator section"""
    with st.expander("🏘️ Calcolo Investimento Immobiliare", expanded=False):
        st.subheader("Analisi Investimento Immobiliare")
        st.info("💡 Calcolo completo con rivalutazione, inflazione e adeguamento affitti")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**🏠 Parametri Base Immobile**")
            
            valore_immobile = st.number_input(
                "Valore Immobile (€)", 
                min_value=5000.00, 
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
                max_value=50.0,
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
            
            costi_assicurazione_perc = st.number_input(
                "Costi Assicurazione Annui (% valore immobile)", 
                min_value=0.0, 
                max_value=30.0,
                value=0.5,
                step=0.1,
                key="real_estate_insurance_perc"
            )
            
            costi_annui_perc = st.number_input(
                "Costi Gestione Annui (% valore immobile)", 
                min_value=0.0, 
                max_value=30.0,
                value=0.5,
                step=0.1,
                key="real_estate_annual_costs_perc"
            )
            
            manutenzione_straordinaria_perc = st.number_input(
                "Manutenzione Straordinaria Annua (%)", 
                min_value=0.0, 
                max_value=30.0,
                value=1.0,
                step=0.1,
                key="real_estate_maintenance"
            )
            
            tassazione_affitti_perc = st.number_input(
                "Tassazione su Affitti (%)", 
                min_value=0.0, 
                max_value=50.0,
                value=21.0,
                step=1.0,
                key="real_estate_tax_rate"
            )
            
            tassa_catastale_perc = st.number_input(
                "Tassa Catastale/IMU (% valore immobile)", 
                min_value=0.0, 
                max_value=99.0,
                value=0.8,
                step=0.1,
                key="real_estate_cadastral_tax",
                help="⚠️ Valore semplificato -  Il calcolo dell'**IMU** in questa applicazione è basato su un **valore semplificato dell'immobile**. È importante sapere che per il calcolo ufficiale dell'imposta si utilizza la **rendita catastale** dell'immobile, un dato che potrebbe non coincidere con il valore di mercato. "
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
            
            adeguamento_affitto_anni = st.number_input(
                "Adeguamento Affitto ogni (Anni)", 
                min_value=1, 
                max_value=99,
                value=4,
                step=1,
                key="real_estate_rent_adjustment_years",
                help="Ogni quanti anni l'affitto viene adeguato al valore rivalutato dell'immobile"
            )
            
            st.write("**ℹ️ Note:**")
            st.write("• L'affitto si adegua in base")
            st.write("agli anni specificati")
            st.write("al valore rivalutato dell'immobile.")
            st.write("• Costi percentuali si aggiornano")
            st.write("al valore dell'immobile.")
            st.write("• Manutenzione e tassa catastale")
            st.write("calcolate su valore corrente")
        
        if st.button("🏠 Calcola Investimento Immobiliare", key="calc_real_estate"):
            try:
                params = {
                    'valore_immobile': valore_immobile,
                    'affitto_lordo': affitto_lordo,
                    'rivalutazione_annua': rivalutazione_annua,
                    'anni_investimento': anni_investimento,
                    'costi_assicurazione_perc': costi_assicurazione_perc,
                    'costi_annui_perc': costi_annui_perc,
                    'manutenzione_straordinaria_perc': manutenzione_straordinaria_perc,
                    'tassazione_affitti_perc': tassazione_affitti_perc,
                    'tassa_catastale_perc': tassa_catastale_perc,
                    'periodo_sfitto_perc': periodo_sfitto_perc,
                    'inflazione_perc': inflazione_perc,
                    'adeguamento_affitto_anni': adeguamento_affitto_anni
                }
                results = calculate_real_estate_investment(params)
                display_real_estate_results(results, params)
            except Exception as e:
                st.error(f"❌ Errore nel calcolo immobiliare: {str(e)}")
                st.error("Verifica che tutti i valori siano corretti.")
                st.exception(e)

def calculate_real_estate_investment(params):
    """Calculate real estate investment returns"""
    
    # Convert percentages to decimals
    rivalutazione_decimal = params['rivalutazione_annua'] / 100
    inflazione_decimal = params['inflazione_perc'] / 100
    periodo_sfitto_decimal = params['periodo_sfitto_perc'] / 100
    manutenzione_decimal = params['manutenzione_straordinaria_perc'] / 100
    tassazione_decimal = params['tassazione_affitti_perc'] / 100
    
    # Convert cost percentages to decimals
    costi_assicurazione_decimal = params['costi_assicurazione_perc'] / 100
    costi_annui_decimal = params['costi_annui_perc'] / 100
    tassa_catastale_decimal = params['tassa_catastale_perc'] / 100
    
    # Initialize variables for year-by-year calculation
    valore_corrente = params['valore_immobile']
    affitto_corrente = params['affitto_lordo']
    
    # Lists to store annual data
    valori_annuali = []
    affitti_netti_annuali = []
    rendimenti_annuali = []
    
    # Calculate year by year
    for anno in range(1, params['anni_investimento'] + 1):
        # Update property value with appreciation
        valore_corrente = valore_corrente * (1 + rivalutazione_decimal)
        
        # Calculate costs as percentages of current property value (updated annually)
        costi_assicurazione_correnti = valore_corrente * costi_assicurazione_decimal
        costi_annui_correnti = valore_corrente * costi_annui_decimal
        tassa_catastale_corrente = valore_corrente * tassa_catastale_decimal
        
        # Adjust rent every X years based on new property value
        if anno % params['adeguamento_affitto_anni'] == 0:
            # Calculate new rent as percentage of current property value
            rapporto_affitto_iniziale = params['affitto_lordo'] / params['valore_immobile']
            affitto_corrente = valore_corrente * rapporto_affitto_iniziale
        
        # Calculate effective rent considering vacancy
        affitto_effettivo = affitto_corrente * (1 - periodo_sfitto_decimal)
        
        # Calculate taxes on rent
        tasse_affitto = affitto_effettivo * tassazione_decimal
        
        # Calculate annual costs (all based on current property value)
        manutenzione_annua = valore_corrente * manutenzione_decimal
        costi_totali_annui = (costi_assicurazione_correnti + costi_annui_correnti + 
                            manutenzione_annua + tassa_catastale_corrente + 
                            tasse_affitto)
        
        # Calculate net annual rent
        affitto_netto = affitto_effettivo - costi_totali_annui
        
        # Calculate annual yield on original property value
        rendimento_annuo = (affitto_netto / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        
        # Store data
        valori_annuali.append(valore_corrente)
        affitti_netti_annuali.append(affitto_netto)
        rendimenti_annuali.append(rendimento_annuo)
    
    # Final calculations
    valore_finale_nominale = valori_annuali[-1]
    valore_finale_reale = valore_finale_nominale / ((1 + inflazione_decimal) ** params['anni_investimento'])
    
    # Total net rent received over the period
    totale_affitti_netti = sum(affitti_netti_annuali)
    
    # Average annual net yield
    rendimento_medio_annuo = sum(rendimenti_annuali) / len(rendimenti_annuali) if rendimenti_annuali else 0
    
    # Total return calculation
    guadagno_capitale_nominale = valore_finale_nominale - params['valore_immobile']
    guadagno_capitale_reale = valore_finale_reale - params['valore_immobile']
    
    rendimento_totale_nominale = totale_affitti_netti + guadagno_capitale_nominale
    rendimento_totale_reale = totale_affitti_netti + guadagno_capitale_reale
    
    # CAGR calculation
    cagr_nominale = ((valore_finale_nominale + totale_affitti_netti) / params['valore_immobile']) ** (1/params['anni_investimento']) - 1 if params['valore_immobile'] > 0 else 0
    cagr_reale = ((valore_finale_reale + totale_affitti_netti) / params['valore_immobile']) ** (1/params['anni_investimento']) - 1 if params['valore_immobile'] > 0 else 0
    
    return {
        'valori_annuali': valori_annuali,
        'affitti_netti_annuali': affitti_netti_annuali,
        'rendimenti_annuali': rendimenti_annuali,
        'valore_finale_nominale': valore_finale_nominale,
        'valore_finale_reale': valore_finale_reale,
        'totale_affitti_netti': totale_affitti_netti,
        'rendimento_medio_annuo': rendimento_medio_annuo,
        'guadagno_capitale_nominale': guadagno_capitale_nominale,
        'guadagno_capitale_reale': guadagno_capitale_reale,
        'rendimento_totale_nominale': rendimento_totale_nominale,
        'rendimento_totale_reale': rendimento_totale_reale,
        'cagr_nominale': cagr_nominale,
        'cagr_reale': cagr_reale,
        'affitto_finale': affitto_corrente
    }

def display_real_estate_results(results, params):
    """Display real estate investment calculation results"""
    st.success("**🎯 Risultati Analisi Investimento Immobiliare**")
    
    # Create detailed results layout
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.write("**🏠 Valore Immobile:**")
        st.write(f"• Valore Iniziale: {format_currency(params['valore_immobile'])}")
        st.write(f"• **Valore Finale (Nominale): {format_currency(results['valore_finale_nominale'])}**")
        st.write(f"• **Valore Finale (Reale): {format_currency(results['valore_finale_reale'])}**")
        st.write(f"• Plusvalenza (Nominale): {format_currency(results['guadagno_capitale_nominale'])}")
        st.write(f"• Plusvalenza (Reale): {format_currency(results['guadagno_capitale_reale'])}")
        rivalutazione_totale = ((results['valore_finale_nominale']/params['valore_immobile'] - 1) * 100) if params['valore_immobile'] > 0 else 0
        st.write(f"• Rivalutazione Totale: {format_percentage(rivalutazione_totale)}")
    
    with res_col2:
        st.write("**💰 Analisi Affitti:**")
        st.write(f"• Affitto Iniziale: {format_currency(params['affitto_lordo'])}")
        st.write(f"• Affitto Finale: {format_currency(results['affitto_finale'])}")
        st.write(f"• **Totale Affitti Netti {params['anni_investimento']} anni: {format_currency(results['totale_affitti_netti'])}**")
        st.write(f"• **Rendimento Medio Annuo: {format_percentage(results['rendimento_medio_annuo'])}**")
        st.write(f"• Periodo Sfitto Considerato: {format_percentage(params['periodo_sfitto_perc'])}")
        adeguamenti = params['anni_investimento'] // params['adeguamento_affitto_anni']
        st.write(f"• Adeguamenti Affitto: {adeguamenti} volte (ogni {params['adeguamento_affitto_anni']} anni)")
    
    with res_col3:
        st.write("**📈 Rendimento Totale:**")
        st.write(f"• **Rendimento Totale (Nominale): {format_currency(results['rendimento_totale_nominale'])}**")
        st.write(f"• **Rendimento Totale (Reale): {format_currency(results['rendimento_totale_reale'])}**")
        
        rendimento_perc_nominale = (results['rendimento_totale_nominale'] / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        rendimento_perc_reale = (results['rendimento_totale_reale'] / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        
        st.write(f"• Rendimento % (Nominale): {format_percentage(rendimento_perc_nominale)}")
        st.write(f"• Rendimento % (Reale): {format_percentage(rendimento_perc_reale)}")
        st.write(f"• **CAGR (Nominale): {format_percentage(results['cagr_nominale'] * 100)}**")
        st.write(f"• **CAGR (Reale): {format_percentage(results['cagr_reale'] * 100)}**")
    
    # Detailed cost breakdown for the last year
    display_cost_breakdown(results, params)
    
    # Additional analysis
    display_additional_analysis(results, params)

def display_cost_breakdown(results, params):
    """Display detailed cost breakdown for the last year"""
    st.write("**💸 Dettaglio Costi Ultimo Anno:**")
    cost_col1, cost_col2 = st.columns(2)
    
    # Calculate final year costs
    valore_finale = results['valori_annuali'][-1]
    affitto_finale = results['affitto_finale']
    
    # Convert percentages to decimals
    periodo_sfitto_decimal = params['periodo_sfitto_perc'] / 100
    tassazione_decimal = params['tassazione_affitti_perc'] / 100
    manutenzione_decimal = params['manutenzione_straordinaria_perc'] / 100
    costi_assicurazione_decimal = params['costi_assicurazione_perc'] / 100
    costi_annui_decimal = params['costi_annui_perc'] / 100
    tassa_catastale_decimal = params['tassa_catastale_perc'] / 100
    
    ultima_manutenzione = valore_finale * manutenzione_decimal
    ultimo_affitto_effettivo = affitto_finale * (1 - periodo_sfitto_decimal)
    ultime_tasse_affitto = ultimo_affitto_effettivo * tassazione_decimal
    
    # Calculate final costs based on final property value
    costi_assicurazione_finali = valore_finale * costi_assicurazione_decimal
    costi_annui_finali = valore_finale * costi_annui_decimal
    tassa_catastale_finale = valore_finale * tassa_catastale_decimal
    
    ultimi_costi_totali = (costi_assicurazione_finali + costi_annui_finali + 
                         ultima_manutenzione + tassa_catastale_finale + 
                         ultime_tasse_affitto)
    
    with cost_col1:
        st.write(f"• Assicurazione ({format_percentage(params['costi_assicurazione_perc'])}): {format_currency(costi_assicurazione_finali)}")
        st.write(f"• Costi Annui ({format_percentage(params['costi_annui_perc'])}): {format_currency(costi_annui_finali)}")
        st.write(f"• Manutenzione Straordinaria ({format_percentage(params['manutenzione_straordinaria_perc'])}): {format_currency(ultima_manutenzione)}")
        st.write(f"• **Tassa Catastale/IMU ({format_percentage(params['tassa_catastale_perc'])}): {format_currency(tassa_catastale_finale)}** ⚠️")
        st.write(f"• **Tasse su Affitti ({format_percentage(params['tassazione_affitti_perc'])}): {format_currency(ultime_tasse_affitto)}**")
        st.write("• *Costi calcolati su valore finale immobile*")
    
    with cost_col2:
        st.write(f"• **Totale Costi Annui: {format_currency(ultimi_costi_totali)}**")
        st.write(f"• Affitto Lordo: {format_currency(affitto_finale)}")
        perdita_sfitto = affitto_finale * periodo_sfitto_decimal
        st.write(f"• Meno Periodo Sfitto: {format_currency(perdita_sfitto)}")
        st.write(f"• Affitto Effettivo: {format_currency(ultimo_affitto_effettivo)}")
        affitto_netto_finale = results['affitti_netti_annuali'][-1]
        st.write(f"• **Affitto Netto Finale: {format_currency(affitto_netto_finale)}**")
        
        # Calculate net yield after all costs and taxes
        rendimento_lordo_finale = (affitto_finale / valore_finale) * 100 if valore_finale > 0 else 0
        rendimento_netto_finale = (affitto_netto_finale / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        st.write(f"• Rendimento Lordo: {format_percentage(rendimento_lordo_finale)}")
        st.write(f"• **Rendimento Netto: {format_percentage(rendimento_netto_finale)}**")
        
        # Show percentage breakdown of costs
        total_cost_perc = (ultimi_costi_totali / ultimo_affitto_effettivo) * 100 if ultimo_affitto_effettivo > 0 else 0
        st.write(f"• **% Costi su Affitto Effettivo: {format_percentage(total_cost_perc)}**")

def display_additional_analysis(results, params):
    """Display additional analysis and considerations"""
    st.write("**📊 Analisi Aggiuntiva:**")
    
    analysis_col1, analysis_col2 = st.columns(2)
    
    with analysis_col1:
        # Yield analysis
        gross_yield_initial = (params['affitto_lordo'] / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        gross_yield_final = (results['affitto_finale'] / results['valore_finale_nominale']) * 100 if results['valore_finale_nominale'] > 0 else 0
        
        st.write("**📈 Analisi Rendimenti:**")
        st.write(f"• Rendimento Lordo Iniziale: {format_percentage(gross_yield_initial)}")
        st.write(f"• Rendimento Lordo Finale: {format_percentage(gross_yield_final)}")
        st.write(f"• Rendimento Netto Medio: {format_percentage(results['rendimento_medio_annuo'])}")
        
        # Break-even analysis
        avg_net_rent = results['totale_affitti_netti'] / params['anni_investimento'] if params['anni_investimento'] > 0 else 0
        break_even_years = params['valore_immobile'] / avg_net_rent if avg_net_rent > 0 else float('inf')
        if break_even_years != float('inf'):
            st.write(f"• Payback Period: {break_even_years:.1f} anni")
        else:
            st.write("• Payback Period: Non determinabile")
        
        # Cost structure analysis
        total_costs_perc = (params['costi_assicurazione_perc'] + params['costi_annui_perc'] + 
                           params['manutenzione_straordinaria_perc'] + params['tassa_catastale_perc'])
        st.write(f"• **Costi Totali (% valore): {format_percentage(total_costs_perc)}**")
    
    with analysis_col2:
        st.write("**⚠️ Considerazioni:**")
        
        # Yield warnings and recommendations
        if results['rendimento_medio_annuo'] < 3:
            st.warning("⚠️ Rendimento netto basso (< 3%)")
        elif results['rendimento_medio_annuo'] > 7:
            st.success("✅ Rendimento netto interessante (> 7%)")
        else:
            st.info("ℹ️ Rendimento netto moderato (3-7%)")
        
        if params['periodo_sfitto_perc'] > 10:
            st.warning("⚠️ Periodo di sfitto elevato considerato")
        
        if params['rivalutazione_annua'] < params['inflazione_perc']:
            st.warning("⚠️ Rivalutazione < Inflazione: perdita valore reale")
        else:
            st.info("✅ Rivalutazione > Inflazione: mantenimento valore reale")
        
        # Cost efficiency warning
        total_costs_perc = (params['costi_assicurazione_perc'] + params['costi_annui_perc'] + 
                           params['manutenzione_straordinaria_perc'] + params['tassa_catastale_perc'])
        if total_costs_perc > 4:
            st.warning("⚠️ Costi totali elevati (> 4% valore immobile)")
        elif total_costs_perc < 2:
            st.success("✅ Struttura costi efficiente (< 2%)")
        else:
            st.info("ℹ️ Struttura costi nella media (2-4%)")
        
        # CAGR analysis
        if results['cagr_reale'] > 0.08:  # 8%
            st.success("🚀 CAGR reale eccellente (> 8%)")
        elif results['cagr_reale'] > 0.05:  # 5%
            st.success("✅ CAGR reale buono (> 5%)")
        elif results['cagr_reale'] > 0.02:  # 2%
            st.info("📈 CAGR reale moderato (> 2%)")
        elif results['cagr_reale'] > 0:
            st.info("📊 CAGR reale positivo ma basso")
        else:
            st.error("📉 CAGR reale negativo - perdita di valore")
    
    # Disclaimer finale per IMU
    st.info("""
    **RICORDA:** Il calcolo della **Tassa Catastale/IMU** in questo strumento è semplificato. 
    Nella realtà, l'IMU si basa sulla **rendita catastale** e non direttamente sul valore di mercato dell'immobile. 
    
    **Per calcoli precisi dell'IMU, consultare sempre un consulente fiscale qualificato.**
    """)
    
