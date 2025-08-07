import streamlit as st
from ui_components import format_currency, format_percentage

def render_real_estate_section():
    """Render real estate investment calculator section"""
    with st.expander("🏘️ Calcolo Investimento Immobiliare", expanded=False):
        st.subheader("Analisi Investimento Immobiliare")
        st.info("💡 Calcolo completo con rivalutazione, inflazione e adeguamento affitti personalizzabile")
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
                help="⚠️ Valore semplificato - Il calcolo dell'**IMU** in questa applicazione è basato su un **valore semplificato dell'immobile**. È importante sapere che per il calcolo ufficiale dell'imposta si utilizza la **rendita catastale** dell'immobile, un dato che potrebbe non coincidere con il valore di mercato."
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
                max_value=15.0,
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
            
            # Informazioni aggiuntive per tipo di adeguamento
            if tipo_adeguamento == "Valore Immobile":
                st.info("🏠 Affitto adeguato al valore rivalutato dell'immobile")
            elif tipo_adeguamento == "Inflazione":
                st.info("📈 Affitto adeguato al tasso di inflazione")
            else:
                st.warning("⚡ Affitto rimane fisso per tutto il periodo")
        
        # Note informative
        st.write("**ℹ️ Note sui Metodi di Adeguamento:**")
        note_col1, note_col2 = st.columns(2)
        
        with note_col1:
            st.write("• **Valore Immobile**: L'affitto mantiene la stessa % del valore immobile")
            st.write("• **Inflazione**: L'affitto cresce con l'inflazione")
            st.write("• **Nessun Adeguamento**: Affitto fisso (perdita potere d'acquisto)")
        
        with note_col2:
            st.write("• Costi percentuali si aggiornano sempre al valore dell'immobile")
            st.write("• Manutenzione e tasse calcolate su valore corrente")
        
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
                    'adeguamento_affitto_anni': adeguamento_affitto_anni,
                    'tipo_adeguamento': tipo_adeguamento
                }
                results = calculate_real_estate_investment_improved(params)
                display_real_estate_results_improved(results, params)
            except Exception as e:
                st.error(f"❌ Errore nel calcolo immobiliare: {str(e)}")
                st.error("Verifica che tutti i valori siano corretti.")
                st.exception(e)

def calculate_real_estate_investment_improved(params):
    """Calculate real estate investment returns with flexible rent adjustment methods"""
    
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
    
    # Calculate initial rent-to-value ratio for property value adjustments
    rapporto_affitto_iniziale = params['affitto_lordo'] / params['valore_immobile']
    
    # Lists to store annual data
    valori_annuali = []
    affitti_lordi_annuali = []
    affitti_netti_annuali = []
    rendimenti_annuali = []
    adeguamenti_effettuati = []
    
    # Calculate year by year
    for anno in range(1, params['anni_investimento'] + 1):
        # Update property value with appreciation
        valore_corrente = valore_corrente * (1 + rivalutazione_decimal)
        
        # Determine if rent adjustment should occur
        adeguamento_questo_anno = (anno % params['adeguamento_affitto_anni'] == 0)
        
        # Adjust rent based on selected method
        if adeguamento_questo_anno:
            if params['tipo_adeguamento'] == "Valore Immobile":
                # Adjust rent to maintain same percentage of property value
                affitto_corrente = valore_corrente * rapporto_affitto_iniziale
                adeguamenti_effettuati.append(f"Anno {anno}: Adeguato a valore immobile")
                
            elif params['tipo_adeguamento'] == "Inflazione":
                # Adjust rent by cumulative inflation for the adjustment period
                inflazione_cumulativa = (1 + inflazione_decimal) ** params['adeguamento_affitto_anni']
                affitto_corrente = affitto_corrente * inflazione_cumulativa
                adeguamenti_effettuati.append(f"Anno {anno}: Adeguato all'inflazione ({format_percentage(inflazione_cumulativa - 1)})")
                
            # If "Nessun Adeguamento", rent stays the same
        
        # Calculate costs as percentages of current property value (updated annually)
        costi_assicurazione_correnti = valore_corrente * costi_assicurazione_decimal
        costi_annui_correnti = valore_corrente * costi_annui_decimal
        tassa_catastale_corrente = valore_corrente * tassa_catastale_decimal
        
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
        affitti_lordi_annuali.append(affitto_corrente)
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
    
    # Calculate rent growth analysis
    affitto_iniziale = params['affitto_lordo']
    affitto_finale = affitti_lordi_annuali[-1]
    crescita_affitto_totale = ((affitto_finale / affitto_iniziale) - 1) * 100 if affitto_iniziale > 0 else 0
    crescita_affitto_annua = ((affitto_finale / affitto_iniziale) ** (1/params['anni_investimento']) - 1) * 100 if affitto_iniziale > 0 and params['anni_investimento'] > 0 else 0
    
    return {
        'valori_annuali': valori_annuali,
        'affitti_lordi_annuali': affitti_lordi_annuali,
        'affitti_netti_annuali': affitti_netti_annuali,
        'rendimenti_annuali': rendimenti_annuali,
        'adeguamenti_effettuati': adeguamenti_effettuati,
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
        'affitto_finale': affitto_finale,
        'crescita_affitto_totale': crescita_affitto_totale,
        'crescita_affitto_annua': crescita_affitto_annua
    }

def display_real_estate_results_improved(results, params):
    """Display real estate investment calculation results with rent adjustment analysis"""
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
        st.write(f"• **Affitto Finale: {format_currency(results['affitto_finale'])}**")
        st.write(f"• **Crescita Affitto Totale: {format_percentage(results['crescita_affitto_totale'])}**")
        st.write(f"• **Crescita Affitto Annua: {format_percentage(results['crescita_affitto_annua'])}**")
        st.write(f"• **Totale Affitti Netti {params['anni_investimento']} anni: {format_currency(results['totale_affitti_netti'])}**")
        st.write(f"• **Rendimento Medio Annuo: {format_percentage(results['rendimento_medio_annuo'])}**")
        st.write(f"• Modalità Adeguamento: **{params['tipo_adeguamento']}**")
        
        # Analisi efficacia dell'adeguamento scelto
        if params['tipo_adeguamento'] == "Inflazione":
            inflazione_cumulativa = ((1 + params['inflazione_perc']/100) ** params['anni_investimento'] - 1) * 100
            st.info(f"📊 Inflazione cumulativa: {format_percentage(inflazione_cumulativa)}")
            if results['crescita_affitto_totale'] >= inflazione_cumulativa * 0.95:  # Tolleranza del 5%
                st.success("✅ Affitto ha mantenuto il potere d'acquisto")
            else:
                st.warning("⚠️ Affitto ha perso potere d'acquisto")
        elif params['tipo_adeguamento'] == "Valore Immobile":
            rapporto_finale = (results['affitto_finale'] / results['valore_finale_nominale']) * 100
            rapporto_iniziale = (params['affitto_lordo'] / params['valore_immobile']) * 100
            st.success(f"✅ Rapporto affitto/valore mantenuto: {format_percentage(rapporto_finale)}")
    
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
    
    # Detailed rent adjustment analysis
    display_rent_adjustment_analysis(results, params)
    
    # Detailed cost breakdown for the last year
    display_cost_breakdown_improved(results, params)
    
    # Additional analysis
    display_additional_analysis_improved(results, params)

def display_rent_adjustment_analysis(results, params):
    """Display detailed analysis of rent adjustments"""
    if params['tipo_adeguamento'] != "Nessun Adeguamento":
        st.write("**🔄 Analisi Adeguamenti Affitto:**")
        
        adjustment_col1, adjustment_col2 = st.columns(2)
        
        with adjustment_col1:
            st.write("**📊 Statistiche Adeguamenti:**")
            numero_adeguamenti = len(results['adeguamenti_effettuati'])
            st.write(f"• **Numero Adeguamenti Effettuati: {numero_adeguamenti}**")
            st.write(f"• **Frequenza: ogni {params['adeguamento_affitto_anni']} anni**")
            
            if numero_adeguamenti > 0:
                adeguamento_medio = (results['crescita_affitto_totale'] / numero_adeguamenti) if numero_adeguamenti > 0 else 0
                st.write(f"• **Adeguamento Medio per Volta: {format_percentage(adeguamento_medio)}**")
            
            # Confronto con benchmark
            if params['tipo_adeguamento'] == "Inflazione":
                inflazione_teoria = params['inflazione_perc'] * params['anni_investimento']
                differenza = results['crescita_affitto_totale'] - inflazione_teoria
                if abs(differenza) < 1:  # Tolleranza 1%
                    st.success("✅ Adeguamento perfettamente allineato all'inflazione")
                elif differenza > 0:
                    st.info(f"📈 Adeguamento superiore all'inflazione di {format_percentage(differenza)}")
                else:
                    st.warning(f"📉 Adeguamento inferiore all'inflazione di {format_percentage(abs(differenza))}")
        
        with adjustment_col2:
            if results['adeguamenti_effettuati']:
                st.write("**📅 Cronologia Adeguamenti:**")
                for adeguamento in results['adeguamenti_effettuati']:
                    st.write(f"• {adeguamento}")
            
            # Analisi impatto economico degli adeguamenti
            if numero_adeguamenti > 0:
                st.write("**💰 Impatto Economico:**")
                affitto_senza_adeguamenti = params['affitto_lordo'] * params['anni_investimento']
                affitto_con_adeguamenti = sum(results['affitti_lordi_annuali'])
                guadagno_da_adeguamenti = affitto_con_adeguamenti - affitto_senza_adeguamenti
                
                st.write(f"• Affitto senza adeguamenti: {format_currency(affitto_senza_adeguamenti)}")
                st.write(f"• Affitto con adeguamenti: {format_currency(affitto_con_adeguamenti)}")
                if guadagno_da_adeguamenti > 0:
                    st.success(f"• **Guadagno da adeguamenti: {format_currency(guadagno_da_adeguamenti)}**")
                else:
                    st.error(f"• **Perdita da adeguamenti: {format_currency(guadagno_da_adeguamenti)}**")
    else:
        st.warning("⚠️ **Nessun Adeguamento Applicato** - L'affitto rimane fisso per tutto il periodo")
        
        # Calcola la perdita di potere d'acquisto
        inflazione_cumulativa = ((1 + params['inflazione_perc']/100) ** params['anni_investimento'] - 1) * 100
        perdita_potere_acquisto = params['affitto_lordo'] * (inflazione_cumulativa / 100)
        
        st.error(f"📉 **Perdita di potere d'acquisto annuo finale:** {format_currency(perdita_potere_acquisto)}")
        st.error(f"📉 **Inflazione cumulativa nel periodo:** {format_percentage(inflazione_cumulativa)}")

def display_cost_breakdown_improved(results, params):
    """Display detailed cost breakdown for the last year with rent adjustment info"""
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

def display_additional_analysis_improved(results, params):
    """Display additional analysis and considerations with rent adjustment insights"""
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
        
        # Rent adjustment effectiveness analysis
        st.write("**🔄 Efficacia Adeguamento Affitti:**")
        if params['tipo_adeguamento'] == "Valore Immobile":
            variazione_rendimento = gross_yield_final - gross_yield_initial
            if abs(variazione_rendimento) < 0.1:  # Tolleranza 0.1%
                st.success("✅ Rendimento lordo mantenuto stabile")
            else:
                st.info(f"📊 Variazione rendimento: {format_percentage(variazione_rendimento)}")
        elif params['tipo_adeguamento'] == "Inflazione":
            # Verifica se la crescita dell'affitto ha battuto l'inflazione
            inflazione_cumulativa = ((1 + params['inflazione_perc']/100) ** params['anni_investimento'] - 1) * 100
            if results['crescita_affitto_totale'] >= inflazione_cumulativa:
                st.success("✅ Affitto ha battuto/pareggiato l'inflazione")
            else:
                st.warning("⚠️ Affitto non ha tenuto il passo con l'inflazione")
        else:
            perdita_potere_acquisto = ((1 + params['inflazione_perc']/100) ** params['anni_investimento'] - 1) * 100
            st.error(f"❌ Perdita potere d'acquisto: {format_percentage(perdita_potere_acquisto)}")
        
        # Break-even analysis
        avg_net_rent = results['totale_affitti_netti'] / params['anni_investimento'] if params['anni_investimento'] > 0 else 0
        break_even_years = params['valore_immobile'] / avg_net_rent if avg_net_rent > 0 else float('inf')
        if break_even_years != float('inf'):
            st.write(f"• Payback Period: {break_even_years:.1f} anni")
        else:
            st.write("• Payback Period: Non determinabile")
    
    with analysis_col2:
        st.write("**⚠️ Considerazioni e Raccomandazioni:**")
        
        # Yield warnings and recommendations
        if results['rendimento_medio_annuo'] < 3:
            st.warning("⚠️ Rendimento netto basso (< 3%)")
        elif results['rendimento_medio_annuo'] > 7:
            st.success("✅ Rendimento netto interessante (> 7%)")
        else:
            st.info("ℹ️ Rendimento netto moderato (3-7%)")
        
        # Rent adjustment strategy recommendations
        st.write("**💡 Analisi Strategia Affitti:**")
        if params['tipo_adeguamento'] == "Nessun Adeguamento":
            st.error("🚨 Strategia rischiosa: perdita di potere d'acquisto garantita")
            st.info("💡 Considera adeguamenti periodici all'inflazione o al valore")
        elif params['tipo_adeguamento'] == "Inflazione":
            if params['rivalutazione_annua'] > params['inflazione_perc']:
                st.info("💡 Considera adeguamento al valore immobile per maggiori ricavi")
            else:
                st.success("✅ Strategia conservativa e sostenibile")
        else:  # Valore Immobile
            if params['rivalutazione_annua'] > params['inflazione_perc'] + 1:
                st.success("🚀 Strategia aggressiva: massimizza i ricavi")
            else:
                st.info("📊 Strategia bilanciata")
        
        # Market condition warnings
        if params['adeguamento_affitto_anni'] > 5:
            st.warning("⚠️ Periodo adeguamento lungo: maggiore esposizione all'inflazione")
        
        # Property appreciation vs inflation
        if params['rivalutazione_annua'] < params['inflazione_perc']:
            st.warning("⚠️ Rivalutazione < Inflazione: perdita valore reale immobile")
        else:
            st.success("✅ Rivalutazione > Inflazione: mantenimento valore reale")
        
        # Cost efficiency warning
        total_costs_perc = (params['costi_assicurazione_perc'] + params['costi_annui_perc'] + 
                           params['manutenzione_straordinaria_perc'] + params['tassa_catastale_perc'])
        if total_costs_perc > 4:
            st.warning("⚠️ Costi totali elevati (> 4% valore immobile)")
        elif total_costs_perc < 2:
            st.success("✅ Struttura costi efficiente (< 2%)")
        else:
            st.info("ℹ️ Struttura costi nella media (2-4%)")
        
        # CAGR analysis with rent adjustment context
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
    
    # Comparative analysis section
    st.write("**🔍 Confronto Strategie Adeguamento:**")
    display_rent_strategy_comparison(results, params)
    
    # Disclaimer finale
    st.info("""
    **RICORDA:** I valori calcolati sono basati su assunzioni semplificate. I mercati immobiliari reali sono influenzati da numerosi fattori non considerati in questo modello (domanda/offerta locale, normative, condizioni economiche generali, ecc.).
    """)

def display_rent_strategy_comparison(results, params):
    """Display comparison between different rent adjustment strategies"""
    comparison_col1, comparison_col2, comparison_col3 = st.columns(3)
    
    # Calculate what would happen with different strategies
    current_strategy = params['tipo_adeguamento']
    
    with comparison_col1:
        st.write("**🔒 Strategia Attuale:**")
        st.write(f"• **{current_strategy}**")
        st.write(f"• Affitto finale: {format_currency(results['affitto_finale'])}")
        st.write(f"• Crescita totale: {format_percentage(results['crescita_affitto_totale'])}")
        st.write(f"• CAGR reale: {format_percentage(results['cagr_reale'] * 100)}")
    
    with comparison_col2:
        # Quick calculation for inflation strategy
        if current_strategy != "Inflazione":
            st.write("**📈 Se Adeguamento all'Inflazione:**")
            inflazione_factor = (1 + params['inflazione_perc']/100) ** params['anni_investimento']
            affitto_inflazione = params['affitto_lordo'] * inflazione_factor
            crescita_inflazione = (inflazione_factor - 1) * 100
            
            st.write(f"• Affitto finale: {format_currency(affitto_inflazione)}")
            st.write(f"• Crescita totale: {format_percentage(crescita_inflazione)}")
            
            if affitto_inflazione > results['affitto_finale']:
                st.success("✅ Affitto più alto")
            elif affitto_inflazione < results['affitto_finale']:
                st.error("❌ Affitto più basso")
            else:
                st.info("⚖️ Affitto simile")
    
    with comparison_col3:
        # Quick calculation for property value strategy
        if current_strategy != "Valore Immobile":
            st.write("**🏠 Se Adeguamento al Valore:**")
            rapporto_iniziale = params['affitto_lordo'] / params['valore_immobile']
            affitto_valore = results['valore_finale_nominale'] * rapporto_iniziale
            crescita_valore = ((affitto_valore / params['affitto_lordo']) - 1) * 100
            
            st.write(f"• Affitto finale: {format_currency(affitto_valore)}")
            st.write(f"• Crescita totale: {format_percentage(crescita_valore)}")
            
            if affitto_valore > results['affitto_finale']:
                st.success("✅ Affitto più alto")
            elif affitto_valore < results['affitto_finale']:
                st.error("❌ Affitto più basso")
            else:
                st.info("⚖️ Affitto simile")
    
    # Summary recommendation
    st.write("**💡 Raccomandazione Strategica:**")
    if params['rivalutazione_annua'] > params['inflazione_perc'] + 1:
        if current_strategy != "Valore Immobile":
            st.info("💡 **Considera l'adeguamento al valore immobile** per massimizzare i ricavi nel lungo termine")
        else:
            st.success("✅ Strategia ottimale per questo scenario di mercato")
    elif params['inflazione_perc'] > params['rivalutazione_annua']:
        if current_strategy != "Inflazione":
            st.info("💡 **L'adeguamento all'inflazione** potrebbe essere più stabile e prevedibile")
        else:
            st.success("✅ Strategia prudente per questo scenario economico")
    else:
        st.info("📊 Entrambe le strategie di adeguamento sono valide per questo scenario")
