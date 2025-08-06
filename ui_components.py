def render_footer():
    """Render the footer with notes and requirements"""
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

    # Disclaimer migliorato
    st.markdown("---")
    st.markdown("### ⚠️ **DISCLAIMER IMPORTANTE**")
    st.error("""
    **🚨 AVVISO LEGALE - LEGGERE ATTENTAMENTE**
    
    📚 **Scopo Didattico**: Questa applicazione è stata sviluppata esclusivamente a scopo educativo e dimostrativo per illustrare concetti finanziari di base.
    
    🚫 **Non è Consulenza Finanziaria**: I calcoli e le informazioni fornite NON costituiscono consigli di investimento, raccomandazioni finanziarie o consulenza professionale di alcun tipo.
    
    ⚠️ **Accuratezza dei Dati**: I valori calcolati e visualizzati potrebbero essere imprecisi, incompleti o contenere errori. Le formule utilizzate sono semplificate e potrebbero non riflettere la complessità dei mercati finanziari reali.
    
    📊 **Responsabilità**: Lo sviluppatore declina ogni responsabilità per:
    - Eventuali perdite finanziarie derivanti dall'uso di questa applicazione
    - Imprecisioni nei calcoli o negli algoritmi implementati  
    - Decisioni di investimento basate sui risultati ottenuti
    
    💡 **Raccomandazione**: Prima di prendere qualsiasi decisione finanziaria, consultare SEMPRE un consulente finanziario qualificato e autorizzato.
    
    📋 **Uso a Proprio Rischio**: L'utilizzo di questa applicazione avviene sotto la completa responsabilità dell'utente.
    """)
    
    st.markdown("---")
    st.markdown("*Sviluppata da **AS** con la collaborazione di **KIM** 🐱 - Versione per fini didattici © 2025*")
