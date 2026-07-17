import streamlit as st
import math
from src.recommendations import get_financial_recommendation
from src.database import create_tables, insert_financial_table
from src.ml_models import predict_spending_risk

st.set_page_config(
    page_title="AI Advisor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Financial Advisor")
st.write("This advisor provides educational financial planning suggestions.")

monthly_income = st.session_state.get("monthly_income", 0)
total_expenses = st.session_state.get("total_expenses", 0)
remaining_balance = st.session_state.get("remaining_balance", 0)
savings_rate = st.session_state.get("savings_rate", 0)

debt_balance = st.session_state.get("debt_balance", 0)
debt_interest_rate = st.session_state.get("debt_interest_rate", 0)

emergency_fund_months = math.ceil(remaining_balance/total_expenses) if total_expenses>0 else 0

investor_profile = st.session_state.get("investor_profile", "Moderate")
st.subheader('Financial Summary')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Savings Rate", f"{savings_rate:.1%}")

with col2:
    st.metric("Emergency Fund Months", f"{emergency_fund_months:.1f}")

with col3:
    st.metric("Monthly Cash Flow", f"${remaining_balance:.2f}")

st.subheader('Advisor Recommendation:')

get_financial_recommendation(monthly_income, savings_rate, debt_balance, debt_interest_rate,
                             emergency_fund_months, investor_profile)

st.write(f"Financial Risk Assessment: {predict_spending_risk(savings_rate, debt_interest_rate, emergency_fund_months)} ")

create_tables()
if st.button('Save Profile'):
    insert_financial_table(monthly_income,total_expenses, debt_balance, debt_interest_rate,
                           remaining_balance, investor_profile)

    st.success('Profile Saved Successfully')