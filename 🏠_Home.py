import streamlit as st

st.set_page_config(
    page_title="Personal Finance Planner",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Finance & Wealth Planning System")

st.write(
    """
    Welcome to your personal finance dashboard.
    
    Use the sidebar to navigate through:
    - Budget Dashboard
    - Debt Planner
    - Savings Goals
    - Investment Profile
    - AI Advisor
"""
)

st.info("This tool provides educational financial planning suggestions.")