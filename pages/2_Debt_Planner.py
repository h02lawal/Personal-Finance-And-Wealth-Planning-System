import streamlit as st
import math

st.set_page_config(
    page_title="Debt Planner",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Debt Planner")
st.write("Enter the Information Below: ")

debt_name = st.text_input("Enter the name of the debt")
debt_balance = st.number_input("Enter the balance of the debt", min_value=0.0)
annual_interest_rate = st.number_input("Annual Interest Rate: ",min_value=0.0, max_value=100.0, value=19.99)
monthly_payment = st.number_input("Monthly Payment: ",min_value=0.0)

monthly_interest_rate = annual_interest_rate/100/12
monthly_interest_amount = monthly_interest_rate*debt_balance
months_to_payoff = -1
if monthly_payment > 0 and monthly_interest_rate > 0:
    if monthly_payment > monthly_interest_amount:
        months_to_payoff = math.ceil(-math.log(1 - (debt_balance * monthly_interest_rate / monthly_payment)) / math.log(1 + monthly_interest_rate))
    else:
        math.ceil( debt_balance/monthly_payment )
total_paid = months_to_payoff * monthly_payment
total_interest_paid = total_paid - debt_balance

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Monthly Interest", f"${monthly_interest_amount:.2f}")

with col2:
    st.metric("Months to Pay Off", months_to_payoff)

with col3:
    st.metric("Total Interest Paid", f"${total_interest_paid:.2f}")

if debt_balance == 0:
    st.info("Enter your debt details to calculate a payoff plan")
elif monthly_payment <= monthly_interest_amount:
    st.error("Your monthly payment is too low. It does not cover the monthly interest.")
elif annual_interest_rate >= 15:
    st.warning("This is a high interest debt, consider prioritizing the debt first.")
else:
    st.success("Your debt payoff plan looks manageable based on your current payment.")
st.session_state["debt_balance"] = debt_balance
st.session_state["debt_interest_rate"] = annual_interest_rate
