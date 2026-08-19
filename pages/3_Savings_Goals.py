import streamlit as st
from datetime import date, timedelta
from src.visualizations import create_savings_progress_chart
from src.database import insert_savings, display_savings_table

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
monthly_contribution = st.number_input("Enter your monthly contribution: ", min_value=5)
target_date = st.date_input("Target Date", value=date.today()+ timedelta(days=1), min_value=date.today() + timedelta(days=1))
target_date_string = target_date.isoformat()
today = date.today()
days_remaining = (target_date - today).days
target_months = max(days_remaining/30.44, 1)

remaining_amount = target_amount - current_savings
if remaining_amount < 0:
    remaining_amount = 0
required_monthly_savings = remaining_amount/target_months
projected_savings = current_savings+(monthly_contribution * target_months)
progress = current_savings / target_amount if target_amount > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Amount Remaining", f"${remaining_amount:,.2f}")

with col2:
    st.metric("Required Monthly Savings", f"${required_monthly_savings:,.2f}")

with col3:
    st.metric("Projected Savings", f"${projected_savings:,.2f}")

with col4:
    st.metric("Progress", f"{progress:.1%}")

with col5:
    st.metric("Days Remaining", f"{days_remaining}")

st.progress(min(progress, 1.0))

if current_savings >= target_amount:
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

profile = st.session_state.financial_profile
profile_id = st.session_state.get("profile_id")

if not isinstance(profile_id, int):
    st.error("Select or create a profile first.")
    st.stop()

if not savings_name.strip():
    st.error("Enter a savings name.")
elif target_amount <=0:
    st.error("Target amount must be greater than zero.")
elif monthly_contribution <= 0:
    st.error("Monthly contribution must be greater than zero.")
else:
    if st.button("Save Plan"):
        insert_savings(
            profile_id = profile_id,
            savings_name = savings_name,
            planned_savings_amount = target_amount,
            current_savings = current_savings,
            timeline = target_months,
            contribution = monthly_contribution,
            target_date = target_date_string
        )
        st.success("Savings saved successfully.")

st.subheader("Saved savings")
fetched_savings = display_savings_table(profile_id)

if not fetched_savings:
    st.error("You currently have not stored any savings.")
else:
    for saves in fetched_savings:
        with st.expander(saves["savings_name"]):
            st.write(
                f"Target Savings: "
                f"${saves['planned_savings_amount']:,.2f}"
            )

            st.write(
                f"Current Savings: "
                f"${saves['current_savings_amount']:,.2f}"
            )

            st.write(
                f"Target Date: {saves['target_date']}"
            )

            st.write(
                f"Monthly Contribution: "
                f"${saves['monthly_contribution']:,.2f}"
            )