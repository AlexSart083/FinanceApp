import streamlit as st
from ui_components import format_currency, format_percentage

def render_real_estate_section():
    """Render real estate investment calculator section"""
    with st.expander("🏘️ Calcolo Investimento Immobiliare", expanded=False):
        st.subheader("Analisi Investimento Immobiliare")
        st.info("💡 Calcolo completo con rivalutazione, inflazione, mutuo e adeguamento affitti personalizzabile")
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
                value=14900.00,
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
                value=0.3,
                step=0.1,
                key="real_estate_insurance_perc"
            )
            
            costi_gestione_euro = st.number_input(
                "Costi Gestione Annui (€)", 
                min_value=0.00, 
                max_value=50000.00,
                value=1000.00,
                step=100.00,
                key="real_estate_annual_costs_euro",
                help="Costi fissi annui (es. amministratore, pulizie, piccole manutenzioni). Verranno adeguati all'inflazione."
            )
            
            manutenzione_straordinaria_perc = st.number_input(
                "Manutenzione Straordinaria Annua (%)", 
                min_value=0.0, 
                max_value=99.0,
                value=1.0,
                step=0.1,
                key="real_estate_maintenance"
            )
            
            tassazione_affitti_perc = st.number_input(
                "Tassazione su Affitti (%)", 
                min_value=0.0, 
                max_value=99.0,
                value=21.0,
                step=1.0,
                key="real_estate_tax_rate"
            )
            
            tassa_catastale_perc = st.number_input(
                "Tassa di propietá (% valore immobile)", 
                min_value=0.0, 
                max_value=99.0,
                value=0.8,
                step=0.1,
                key="real_estate_cadastral_tax",
                help="⚠️ Valore semplificato - Il calcolo della tassa di propietá in questa applicazione è basato sul **valore dell'immobile**. È importante sapere che per il calcolo ufficiale dell'imposta in Italia é legata alla **rendita catastale** e al **coefficiente catastale** dell'immobile."
            )
            
            # Sezione Mutuo alla fine
            st.write("**🏦 Mutuo (se presente)**")
            rata_mutuo_mensile = st.number_input(
                "Rata Mutuo Mensile (€)", 
                min_value=0.00, 
                max_value=10000.00,
                value=0.00,
                step=50.00,
                key="real_estate_mortgage_payment"
            )
            
            anni_restanti_mutuo = st.number_input(
                "Anni Restanti Mutuo", 
                min_value=0, 
                max_value=50,
                value=0,
                step=1,
                key="real_estate_mortgage_years"
            )
        
        with col3:
            st.write("**📊 Parametri Economici e Adeguamenti**")
            
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
                max_value=100.0,
                value=2.0,
                step=0.1,
                key="real_estate_inflation"
            )
            
            # NUOVA FUNZIONALITÀ: Scelta tipo di adeguamento affitto
            tipo_adeguamento = st.selectbox(
                "Modalità Adeguamento Affitto",
                ["Valore Immobile", "Inflazione", "Nessun Adeguamento"],
                index=0,
                key="real_estate_adjustment_type",
                help="Scegli come adeguare l'affitto nel tempo"
            )
            
            adeguamento_affitto_anni = st.number_input(
                "Adeguamento Affitto ogni (Anni)", 
                min_value=1, 
                max_value=99,
                value=4,
                step=1,
                key="real_estate_rent_adjustment_years",
                help="Ogni quanti anni l'affitto viene adeguato secondo la modalità scelta"
            )
            
            # Informazioni sui costi del mutuo
            if rata_mutuo_mensile > 0:
                rata_annua_mutuo = rata_mutuo_mensile * 12
                st.info(f"💰 Rata Annua Mutuo: {format_currency(rata_annua_mutuo)}")
                if anni_restanti_mutuo > 0:
                    costo_totale_mutuo = rata_annua_mutuo * min(anni_restanti_mutuo, anni_investimento)
                    st.info(f"💸 Costo Totale Mutuo nel Periodo: {format_currency(costo_totale_mutuo)}")
            
            # Informazioni aggiuntive per tipo di adeguamento
            if tipo_adeguamento == "Valore Immobile":
                st.info("🏠 Affitto adeguato al valore rivalutato dell'immobile")
            elif tipo_adeguamento == "Inflazione":
                st.info("📈 Affitto adeguato al tasso di inflazione")
            else:
                st.warning("⚡ Affitto rimane fisso per tutto il periodo")
        
        # Note informative
        st.write("**ℹ️ Note sui Metodi di Adeguamento e Costi:**")
        note_col1, note_col2 = st.columns(2)
        
        with note_col1:
            st.write("• **Valore Immobile**: L'affitto mantiene la stessa % del valore immobile")
            st.write("• **Inflazione**: L'affitto cresce con l'inflazione")
            st.write("• **Nessun Adeguamento**: Affitto fisso (perdita potere d'acquisto)")
            st.write("• **Costi Gestione**: Importo fisso adeguato annualmente all'inflazione")
        
        with note_col2:
            st.write("• Costi percentuali si aggiornano sempre al valore dell'immobile")
            st.write("• Manutenzione e tasse calcolate su valore corrente")
            st.write("• **Mutuo**: Se presente, viene considerato fino alla scadenza")
            st.write("• Rate mutuo sono fisse e non si adeguano all'inflazione")
        
        if st.button("🏠 Calcola Investimento Immobiliare", key="calc_real_estate"):
            try:
                params = {
                    'valore_immobile': valore_immobile,
                    'affitto_lordo': affitto_lordo,
                    'rivalutazione_annua': rivalutazione_annua,
                    'anni_investimento': anni_investimento,
                    'costi_assicurazione_perc': costi_assicurazione_perc,
                    'costi_gestione_euro': costi_gestione_euro,
                    'rata_mutuo_mensile': rata_mutuo_mensile,
                    'anni_restanti_mutuo': anni_restanti_mutuo,
                    'manutenzione_straordinaria_perc': manutenzione_straordinaria_perc,
                    'tassazione_affitti_perc': tassazione_affitti_perc,
                    'tassa_catastale_perc': tassa_catastale_perc,
                    'periodo_sfitto_perc': periodo_sfitto_perc,
                    'inflazione_perc': inflazione_perc,
                    'adeguamento_affitto_anni': adeguamento_affitto_anni,
                    'tipo_adeguamento': tipo_adeguamento
                }
                results = calculate_real_estate_investment_improved(params)
                display_real_estate_results_simplified(results, params)
            except Exception as e:
                st.error(f"❌ Errore nel calcolo immobiliare: {str(e)}")
                st.error("Verifica che tutti i valori siano corretti.")
                st.exception(e)

def calculate_real_estate_investment_improved(params):
    """Calculate real estate investment returns with flexible rent adjustment methods, mortgage costs and inflation-adjusted management costs"""
    
    # Convert percentages to decimals
    rivalutazione_decimal = params['rivalutazione_annua'] / 100
    inflazione_decimal = params['inflazione_perc'] / 100
    periodo_sfitto_decimal = params['periodo_sfitto_perc'] / 100
    manutenzione_decimal = params['manutenzione_straordinaria_perc'] / 100
    tassazione_decimal = params['tassazione_affitti_perc'] / 100
    
    # Convert cost percentages to decimals
    costi_assicurazione_decimal = params['costi_assicurazione_perc'] / 100
    tassa_catastale_decimal = params['tassa_catastale_perc'] / 100
    
    # Initialize variables for year-by-year calculation
    valore_corrente = params['valore_immobile']
    affitto_corrente = params['affitto_lordo']
    costi_gestione_correnti = params['costi_gestione_euro']  # Costi fissi iniziali
    
    # Calculate initial rent-to-value ratio for property value adjustments
    rapporto_affitto_iniziale = params['affitto_lordo'] / params['valore_immobile']
    
    # Mortgage parameters
    rata_mutuo_annua = params['rata_mutuo_mensile'] * 12 if params['rata_mutuo_mensile'] > 0 else 0
    
    # Lists to store annual data
    valori_annuali = []
    affitti_lordi_annuali = []
    affitti_netti_annuali = []
    rendimenti_annuali = []
    costi_gestione_annuali = []
    costi_mutuo_annuali = []
    
    # Calculate year by year
    for anno in range(1, params['anni_investimento'] + 1):
        # Update property value with appreciation
        valore_corrente = valore_corrente * (1 + rivalutazione_decimal)
        
        # Update management costs with inflation
        costi_gestione_correnti = costi_gestione_correnti * (1 + inflazione_decimal)
        
        # Determine if rent adjustment should occur
        adeguamento_questo_anno = (anno % params['adeguamento_affitto_anni'] == 0)
        
        # Adjust rent based on selected method
        if adeguamento_questo_anno:
            if params['tipo_adeguamento'] == "Valore Immobile":
                # Adjust rent to maintain same percentage of property value
                affitto_corrente = valore_corrente * rapporto_affitto_iniziale
                
            elif params['tipo_adeguamento'] == "Inflazione":
                # Adjust rent by cumulative inflation for the adjustment period
                inflazione_cumulativa = (1 + inflazione_decimal) ** params['adeguamento_affitto_anni']
                affitto_corrente = affitto_corrente * inflazione_cumulativa
                
            # If "Nessun Adeguamento", rent stays the same
        
        # Calculate mortgage cost for this year
        costo_mutuo_anno = 0
        if rata_mutuo_annua > 0 and anno <= params['anni_restanti_mutuo']:
            costo_mutuo_anno = rata_mutuo_annua
        
        # Calculate costs as percentages of current property value (updated annually)
        costi_assicurazione_correnti = valore_corrente * costi_assicurazione_decimal
        tassa_catastale_corrente = valore_corrente * tassa_catastale_decimal
        
        # Calculate effective rent considering vacancy
        affitto_effettivo = affitto_corrente * (1 - periodo_sfitto_decimal)
        
        # Calculate taxes on rent
        tasse_affitto = affitto_effettivo * tassazione_decimal
        
        # Calculate annual costs (management costs adjusted for inflation, others based on current property value)
        manutenzione_annua = valore_corrente * manutenzione_decimal
        costi_totali_annui = (costi_assicurazione_correnti + costi_gestione_correnti + 
                            manutenzione_annua + tassa_catastale_corrente + 
                            tasse_affitto + costo_mutuo_anno)
        
        # Calculate net annual rent
        affitto_netto = affitto_effettivo - costi_totali_annui
        
        # Calculate annual yield on original property value
        rendimento_annuo = (affitto_netto / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        
        # Store data
        valori_annuali.append(valore_corrente)
        affitti_lordi_annuali.append(affitto_corrente)
        affitti_netti_annuali.append(affitto_netto)
        rendimenti_annuali.append(rendimento_annuo)
        costi_gestione_annuali.append(costi_gestione_correnti)
        costi_mutuo_annuali.append(costo_mutuo_anno)
    
    # Final calculations
    valore_finale_nominale = valori_annuali[-1]
    valore_finale_reale = valore_finale_nominale / ((1 + inflazione_decimal) ** params['anni_investimento'])
    
    # Total net rent received over the period
    totale_affitti_netti = sum(affitti_netti_annuali)
    totale_costi_mutuo = sum(costi_mutuo_annuali)
    
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
    
    # Calculate rent growth analysis
    affitto_iniziale = params['affitto_lordo']
    affitto_finale = affitti_lordi_annuali[-1]
    crescita_affitto_totale = ((affitto_finale / affitto_iniziale) - 1) * 100 if affitto_iniziale > 0 else 0
    crescita_affitto_annua = ((affitto_finale / affitto_iniziale) ** (1/params['anni_investimento']) - 1) * 100 if affitto_iniziale > 0 and params['anni_investimento'] > 0 else 0
    
    # Calculate management costs growth
    costi_gestione_finali = costi_gestione_annuali[-1]
    crescita_costi_gestione = ((costi_gestione_finali / params['costi_gestione_euro']) - 1) * 100 if params['costi_gestione_euro'] > 0 else 0
    
    return {
        'valori_annuali': valori_annuali,
        'affitti_lordi_annuali': affitti_lordi_annuali,
        'affitti_netti_annuali': affitti_netti_annuali,
        'rendimenti_annuali': rendimenti_annuali,
        'costi_gestione_annuali': costi_gestione_annuali,
        'costi_mutuo_annuali': costi_mutuo_annuali,
        'valore_finale_nominale': valore_finale_nominale,
        'valore_finale_reale': valore_finale_reale,
        'totale_affitti_netti': totale_affitti_netti,
        'totale_costi_mutuo': totale_costi_mutuo,
        'rendimento_medio_annuo': rendimento_medio_annuo,
        'guadagno_capitale_nominale': guadagno_capitale_nominale,
        'guadagno_capitale_reale': guadagno_capitale_reale,
        'rendimento_totale_nominale': rendimento_totale_nominale,
        'rendimento_totale_reale': rendimento_totale_reale,
        'cagr_nominale': cagr_nominale,
        'cagr_reale': cagr_reale,
        'affitto_finale': affitto_finale,
        'crescita_affitto_totale': crescita_affitto_totale,
        'crescita_affitto_annua': crescita_affitto_annua,
        'costi_gestione_finali': costi_gestione_finali,
        'crescita_costi_gestione': crescita_costi_gestione
    }

def display_real_estate_results_simplified(results, params):
    """Display real estate investment calculation results - SIMPLIFIED VERSION"""
    st.success("**🎯 Risultati Analisi Investimento Immobiliare**")
    
    # Create main results layout - 3 columns for key metrics
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.write("**🏠 Valore Immobile:**")
        st.write(f"• Valore Iniziale: {format_currency(params['valore_immobile'])}")
        st.write(f"• **Valore Finale (Nominale): {format_currency(results['valore_finale_nominale'])}**")
        st.write(f"• **Valore Finale (Reale): {format_currency(results['valore_finale_reale'])}**")
        st.write(f"• Plusvalenza (Nominale): {format_currency(results['guadagno_capitale_nominale'])}")
        rivalutazione_totale = ((results['valore_finale_nominale']/params['valore_immobile'] - 1) * 100) if params['valore_immobile'] > 0 else 0
        st.write(f"• Rivalutazione Totale: {format_percentage(rivalutazione_totale)}")
    
    with res_col2:
        st.write("**💰 Analisi Affitti:**")
        st.write(f"• Affitto Iniziale: {format_currency(params['affitto_lordo'])}")
        st.write(f"• **Affitto Finale: {format_currency(results['affitto_finale'])}**")
        st.write(f"• **Crescita Affitto Totale: {format_percentage(results['crescita_affitto_totale'])}**")
        st.write(f"• **Totale Affitti Netti {params['anni_investimento']} anni: {format_currency(results['totale_affitti_netti'])}**")
        st.write(f"• **Rendimento Medio Annuo: {format_percentage(results['rendimento_medio_annuo'])}**")
        st.write(f"• Modalità Adeguamento: **{params['tipo_adeguamento']}**")
    
    with res_col3:
        st.write("**📈 Rendimento Totale:**")
        st.write(f"• **Rendimento Totale (Nominale): {format_currency(results['rendimento_totale_nominale'])}**")
        st.write(f"• **Rendimento Totale (Reale): {format_currency(results['rendimento_totale_reale'])}**")
        
        # Mostra costi mutuo se presente
        if results['totale_costi_mutuo'] > 0:
            st.write(f"• **Totale Costi Mutuo: {format_currency(results['totale_costi_mutuo'])}**")
        
        rendimento_perc_nominale = (results['rendimento_totale_nominale'] / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        rendimento_perc_reale = (results['rendimento_totale_reale'] / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        
        st.write(f"• Rendimento % (Nominale): {format_percentage(rendimento_perc_nominale)}")
        st.write(f"• **CAGR (Nominale): {format_percentage(results['cagr_nominale'] * 100)}**")
        st.write(f"• **CAGR (Reale): {format_percentage(results['cagr_reale'] * 100)}**")
    
    # Simplified cost breakdown - ultimo anno only
    st.write("**💸 Sintesi Costi e Performance:**")
    cost_col1, cost_col2 = st.columns(2)
    
    # Calculate final year key metrics
    valore_finale = results['valori_annuali'][-1]
    affitto_finale = results['affitto_finale']
    periodo_sfitto_decimal = params['periodo_sfitto_perc'] / 100
    affitto_effettivo_finale = affitto_finale * (1 - periodo_sfitto_decimal)
    affitto_netto_finale = results['affitti_netti_annuali'][-1]
    
    with cost_col1:
        st.write("**📊 Ultimo Anno - Metriche Chiave:**")
        st.write(f"• Affitto Lordo: {format_currency(affitto_finale)}")
        st.write(f"• Affitto Effettivo: {format_currency(affitto_effettivo_finale)}")
        st.write(f"• **Affitto Netto: {format_currency(affitto_netto_finale)}**")
        
        # Calculate key percentages
        rendimento_lordo_finale = (affitto_finale / valore_finale) * 100 if valore_finale > 0 else 0
        rendimento_netto_finale = (affitto_netto_finale / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        st.write(f"• Rendimento Lordo: {format_percentage(rendimento_lordo_finale)}")
        st.write(f"• **Rendimento Netto: {format_percentage(rendimento_netto_finale)}**")
        
        # Percentage of costs on effective rent
        total_costs_final_year = affitto_effettivo_finale - affitto_netto_finale
        cost_percentage = (total_costs_final_year / affitto_effettivo_finale) * 100 if affitto_effettivo_finale > 0 else 0
        st.write(f"• **% Costi Totali su Affitto: {format_percentage(cost_percentage)}**")
    
    with cost_col2:
        st.write("**⚠️ Valutazioni e Raccomandazioni:**")
        
        # Performance evaluation
        if results['rendimento_medio_annuo'] > 7:
            st.success("✅ Rendimento netto interessante (> 7%)")
        elif results['rendimento_medio_annuo'] > 3:
            st.info("📈 Rendimento netto moderato (3-7%)")
        else:
            st.warning("⚠️ Rendimento netto basso (< 3%)")
        
        # CAGR evaluation
        if results['cagr_reale'] > 0.05:
            st.success("🚀 CAGR reale buono (> 5%)")
        elif results['cagr_reale'] > 0:
            st.info("📊 CAGR reale positivo")
        else:
            st.error("📉 CAGR reale negativo")
        
        # Cost structure evaluation
        if cost_percentage > 60:
            st.warning("⚠️ Struttura costi elevata (> 60%)")
        elif cost_percentage < 40:
            st.success("✅ Struttura costi efficiente (< 40%)")
        else:
            st.info("📊 Struttura costi nella media (40-60%)")
        
        # Rent adjustment strategy evaluation
        if params['tipo_adeguamento'] == "Nessun Adeguamento":
            st.error("🚨 Strategia rischiosa: perdita potere d'acquisto")
        elif params['tipo_adeguamento'] == "Inflazione":
            st.success("✅ Strategia conservativa")
        else:  # Valore Immobile
            st.info("📈 Strategia dinamica")
        
        # Property appreciation vs inflation
        if params['rivalutazione_annua'] <= params['inflazione_perc']:
            st.warning("⚠️ Rivalutazione ≤ Inflazione")
        else:
            st.success("✅ Rivalutazione > Inflazione")
    
    # Mortgage analysis (if present) - simplified
    if results['totale_costi_mutuo'] > 0:
        st.write("**🏦 Analisi Mutuo:**")
        mortgage_col1, mortgage_col2 = st.columns(2)
        
        with mortgage_col1:
            st.write(f"• **Totale Costi Mutuo {params['anni_investimento']} anni: {format_currency(results['totale_costi_mutuo'])}**")
            rata_annua = params['rata_mutuo_mensile'] * 12
            percentuale_rata = (rata_annua / params['affitto_lordo']) * 100 if params['affitto_lordo'] > 0 else 0
            st.write(f"• Rata annua vs Affitto iniziale: {format_percentage(percentuale_rata)}")
            
            if params['anni_restanti_mutuo'] < params['anni_investimento']:
                anni_liberi = params['anni_investimento'] - params['anni_restanti_mutuo']
                st.success(f"✅ Ultimi {anni_liberi} anni senza rata")
        
        with mortgage_col2:
            # Mortgage sustainability
            if percentuale_rata < 50:
                st.success("✅ Mutuo sostenibile (< 50% affitto)")
            elif percentuale_rata < 70:
                st.warning("⚠️ Mutuo impegnativo (50-70% affitto)")
            else:
                st.error("🚨 Mutuo rischioso (> 70% affitto)")
            
            # Compare with and without mortgage
            rendimento_senza_mutuo = results['rendimento_totale_nominale'] + results['totale_costi_mutuo']
            miglioramento = rendimento_senza_mutuo - results['rendimento_totale_nominale']
            st.info(f"📊 Rendimento senza mutuo: +{format_currency(miglioramento)}")
    
    # Final summary
    st.write("**📋 Riepilogo Investimento:**")
    summary_col1, summary_col2 = st.columns(2)
    
    with summary_col1:
        # Break-even analysis
        avg_net_rent = results['totale_affitti_netti'] / params['anni_investimento'] if params['anni_investimento'] > 0 else 0
        break_even_years = params['valore_immobile'] / avg_net_rent if avg_net_rent > 0 else float('inf')
        
        if break_even_years != float('inf') and break_even_years > 0:
            st.write(f"• **Payback Period: {break_even_years:.1f} anni**")
        
        # Total investment and returns summary
        investimento_totale = params['valore_immobile'] + results['totale_costi_mutuo']
        capitale_finale_affitti_nominale = results['valore_finale_nominale'] + results['totale_affitti_netti']
        capitale_finale_affitti_reale = results['valore_finale_reale'] + results['totale_affitti_netti']
        
        st.write(f"• **Investimento Totale: {format_currency(investimento_totale)}**")
        st.write(f"• **Capitale Finale + Affitti (Nominale): {format_currency(capitale_finale_affitti_nominale)}**")
        st.write(f"• **Capitale Finale + Affitti (Reale): {format_currency(capitale_finale_affitti_reale)}**")
    
    with summary_col2:
        # Final recommendation based on key metrics
        st.write("**💡 Valutazione Complessiva:**")
        
        # Count positive indicators
        positive_indicators = 0
        if results['cagr_reale'] > 0.03:  # 3%
            positive_indicators += 1
        if results['rendimento_medio_annuo'] > 4:  # 4%
            positive_indicators += 1
        if cost_percentage < 50:  # Costs < 50%
            positive_indicators += 1
        if params['rivalutazione_annua'] > params['inflazione_perc']:
            positive_indicators += 1
        if break_even_years != float('inf') and break_even_years < 20:
            positive_indicators += 1
        
        # Final assessment
        if positive_indicators >= 4:
            st.success("🚀 **Investimento Attraente**")
            st.write("• Buoni rendimenti e struttura costi efficiente")
        elif positive_indicators >= 3:
            st.info("📈 **Investimento Accettabile**")
            st.write("• Rendimenti moderati, valuta pro e contro")
        elif positive_indicators >= 2:
            st.warning("⚠️ **Investimento Rischioso**")
            st.write("• Rendimenti limitati, considera alternative")
        else:
            st.error("📉 **Investimento Non Raccomandato**")
            st.write("• Rendimenti insufficienti per i rischi")
    
    # Disclaimer semplificato
    st.info("""
    **📝 Nota:** Questo calcolo è basato su assunzioni semplificate. I mercati immobiliari reali sono influenzati da 
    numerosi fattori non considerati (domanda/offerta locale, normative, condizioni economiche, ecc.). 
    Consulta sempre un consulente finanziario prima di investire.
    """)
