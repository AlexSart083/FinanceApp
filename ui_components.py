import streamlit as st

def setup_page_config():
    """Configure the Streamlit page settings"""
    st.set_page_config(
        page_title="Calcolatore Finanziario",
        page_icon="💰",
        layout="wide"
    )

def render_header():
    """Render the main header of the application"""
    st.title("🏦 Calcolatore Finanziario Avanzato")
    st.markdown("---")

def render_footer():

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
    
    🔒 **Privacy dei Dati**: I dati inseriti nell'applicazione non vengono salvati, archiviati o trasmessi in alcun modo dal sistema o dall'applicazione stessa.
    """)
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
    st.markdown("---")
    st.markdown("*Sviluppata da **AS** con la collaborazione di **KIM** 🐱 - Versione per fini didattici © 2025*")

def display_results_section(title, results_data):
    """Display results in a formatted section
    
    Args:
        title (str): Section title
        results_data (dict): Dictionary with column data
    """
    st.success(f"**{title}**")
    
    if len(results_data) == 2:
        col1, col2 = st.columns(2)
        cols = [col1, col2]
    elif len(results_data) == 3:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
    else:
        cols = [st]  # Use single column for other cases
    
    for i, (col_title, col_data) in enumerate(results_data.items()):
        with cols[i % len(cols)]:
            st.write(f"**{col_title}:**")
            for line in col_data:
                st.write(line)

def format_currency(value):
    """Format value as currency"""
    return f"€{value:,.2f}"

def format_percentage(value, decimals=2):
    """Format value as percentage"""
    return f"{value:.{decimals}f}%"
