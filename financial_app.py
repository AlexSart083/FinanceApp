import streamlit as st
from ui_components import setup_page_config, render_header, render_footer
from bond_calculator import render_bond_section, render_professional_bond_section
from loan_calculator import render_loan_section
from investment_calculator import render_compound_interest_section, render_cagr_section
from real_estate_calculator import render_real_estate_section

def main():
    """Main application function"""
    # Setup page configuration
    setup_page_config()
    
    # Render header
    render_header()
    
    # Render all sections
    render_real_estate_section()
    render_professional_bond_section()
    render_loan_section()
    render_compound_interest_section()
    render_cagr_section()
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()
