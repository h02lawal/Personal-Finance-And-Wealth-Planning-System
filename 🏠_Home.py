import streamlit as st
from src.database import create_debts_table, create_tables, create_savings_table, create_financial_profile, get_financial_profiles, get_financial_profile

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

if "financial_profile" not in st.session_state:
    st.session_state.financial_profile = {
        "monthly_income": 0.0,
        "total_expenses": 0.0,
        "debt_balance": 0.0,
        "debt_interest_rate": 0.0,
        "emergency_fund": 0.0,
        "remaining_balance":0.0,
        "savings_rate": 0.0,
        "investor_profile": "Not assessed"
    }

create_tables()
create_debts_table()
create_savings_table()

profiles = get_financial_profiles()
st.subheader("Financial Profiles")

if profiles:
    profile_ids = [profile["id"] for profile in profiles]

    selected_profile_ids = st.selectbox("Select an existing profile", profile_ids)
    if st.button("Load profile"):
        db_profile = get_financial_profile(selected_profile_ids)
        if db_profile is not None:
            st.session_state.profile_id = selected_profile_ids
            monthly_income = (float(db_profile["monthly_income"]) or 0.0)
            total_expenses = (float(db_profile["total_expenses"]) or 0.0)
            remaining_balance = (monthly_income - total_expenses)
            savings_rate = (remaining_balance/monthly_income if monthly_income > 0 else 0.0)
            st.session_state.financial_profile = {
                "monthly_income": monthly_income,
                "total_expenses": total_expenses,
                "remaining_balance": remaining_balance,
                "savings_rate": savings_rate,
                "investor_profile": db_profile["investor_profile"] or "Not assessed",
                "risk_score": int(db_profile["risk_score"] or 0)
            }
            st.success(f"Profile {selected_profile_ids} loaded successfully")
else:
        st.info(f"No financial profiles exist. Create a new profile to get started")

if st.button("Create New Profile"):
    new_profile_id = create_financial_profile()
    st.session_state.profile_id = new_profile_id
    st.success(
        f"New profile {new_profile_id} created successfully."
    )