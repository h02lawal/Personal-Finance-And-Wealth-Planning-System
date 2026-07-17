import streamlit as st
from src.visualizations import create_savings_progress_chart

st.set_page_config(
    page_title="Savings Goals",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Savings Planner")
st.write("Enter the Information Below: ")

savings_name = st.text_input("Enter savings name: ")
target_amount = st.number_input("Enter target amount: ", min_value=100)
current_savings = st.number_input("Enter your current savings amount: ", min_value=0)
target_months = st.number_input("Enter your target timeline in months(how long you will like to save for): ", min_value=1)
monthly_contribution = st.number_input("Enter your monthly contribution: ", min_value=5)

remaining_amount = target_amount - current_savings
if remaining_amount < 0:
    remaining_amount = 0
required_monthly_savings = remaining_amount/target_months
projected_savings = current_savings+(monthly_contribution * target_months)
on_track = projected_savings>target_amount
progress = current_savings / target_amount if target_amount > 0 else 0

if on_track:
    st.success("You are on track to reach your savings goal.")
else:
    st.warning("You are not currently on track to reach your savings goal.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Amount Remaining", f"{remaining_amount}")

with col2:
    st.metric("Required Monthly Savings", f"{required_monthly_savings:.2f}")

with col3:
    st.metric("Projected Savings", f"{projected_savings}")

with col4:
    st.metric("Progress", f"{progress:.1%}")

st.progress(min(progress, 1.0))

if target_amount == 0:
    st.info("Enter your savings goal details. ")
elif current_savings >= target_amount:
    st.success(f"Congratulations! you have reached your {savings_name} goal.")
elif monthly_contribution >= required_monthly_savings:
    st.success(f"You are on track to reach your {savings_name} goal.")
else:
    shortfall = required_monthly_savings - monthly_contribution

    st.warning(
        f"You need to save an extra ${shortfall:.2f} per month"
        f" to reach your {savings_name} goal on time."
    )

fig = create_savings_progress_chart(current_savings, target_amount)
st.pyplot(fig)