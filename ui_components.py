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

    st.markdown("*Sviluppato per calcoli finanziari di base. Consultare sempre un consulente finanziario qualificato per decisioni di investimento.*")

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
