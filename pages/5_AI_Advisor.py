import streamlit as st
from src.recommendations import get_financial_recommendation
from src.database import get_financial_profile, get_depts_by_profile, display_savings_table
from src.calculations import financial_health_score
from src.ml_models import predict_financial_risk

st.set_page_config(
    page_title="AI Advisor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Financial Advisor")
st.write("This advisor provides educational financial planning suggestions.")

#profile = st.session_state.financial_profile

profile_id = st.session_state.get("profile_id")
if not isinstance(profile_id, int):
    st.error("No valid financial profile is currently active")
    st.stop()

financial_profile = get_financial_profile(profile_id)
if financial_profile is None:
    st.error("financial profile could not be found")
    st.stop()
assert financial_profile is not None



risk_score = int(financial_profile["risk_score"] or 0)
monthly_income = float(financial_profile["monthly_income"] or 0.0)
total_expenses = float(financial_profile["total_expenses"] or 0.0)
remaining_balance = (monthly_income - total_expenses)
savings_rate = (remaining_balance / monthly_income if monthly_income > 0 else 0.0)
emergency_fund_months = max(remaining_balance, 0.0) / total_expenses if total_expenses > 0 else 0

investor_profile = financial_profile["investor_profile"] or "Moderate" #profile.get("investor_profile", "Moderate")
debts = get_depts_by_profile(profile_id)
debt_balance = sum(float(debt["debt_balance"] or 0.0) for debt in debts)
debt_interest_rate = max((float(debt["annual_interest_rate"] or 0.0) for debt in debts), default=0.0)
total_monthly_debt_payments = sum(float(debt["monthly_payment"] or 0.0) for debt in debts)

savings = display_savings_table(profile_id)
total_current_savings = sum(float(saving["current_savings_amount"] or 0.0) for saving in savings)
total_savings_targets = sum(float(saving["planned_savings_amount"] or 0.0) for saving in savings)
total_monthly_contribution = sum(float(saving["monthly_contribution"] or 0.0) for saving in savings)
number_of_savings_goals = len(savings)

st.subheader('Financial Summary')

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Savings Rate", f"{savings_rate:.1%}")
with col2:
    st.metric("Emergency Fund Months", f"{emergency_fund_months:.1f}")
with col3:
    st.metric("Monthly Cash Flow", f"${remaining_balance:.2f}")


col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Current Savings", f"${total_current_savings:.1f}")
with col2:
    st.metric("Total Planned Savings", f"${total_savings_targets:.1f}")
with col3:
    st.metric("Total Monthly Contribution", f"${total_monthly_contribution}")

st.subheader('Advisor Recommendation:')

savings_goal_progress = (total_current_savings/total_savings_targets if total_savings_targets > 0 else 0.0)

get_financial_recommendation(monthly_income, savings_rate, debt_balance, debt_interest_rate,
                             emergency_fund_months, investor_profile, total_current_savings, total_savings_targets)

debt_to_income = (total_monthly_debt_payments/monthly_income if monthly_income > 0 else 0.0)
st.write(f"Financial Risk Assessment: {predict_financial_risk(savings_rate, debt_interest_rate, emergency_fund_months, debt_to_income, savings_goal_progress)} ")


fin_h_s = financial_health_score(savings_rate, debt_to_income, emergency_fund_months, remaining_balance, savings_goal_progress, total_monthly_contribution, total_savings_targets)
st.metric("Financial Health Score", f"{fin_h_s}/100")
