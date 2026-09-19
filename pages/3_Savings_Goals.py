import streamlit as st
from datetime import date, timedelta
from src.visualizations import create_savings_progress_chart
from src.database import insert_savings, display_savings_table, delete_savings, update_savings, record_savings_contribution

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

if "financial_profile" not in st.session_state:
    st.session_state.financial_profile = {}

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
        col1, col2, col3, col4 = st.columns([7,2,2,2])
        with col1:
            st.write(f"Target Savings: \\${saves['planned_savings_amount']:,.2f}, Current Savings: \\${saves['current_savings_amount']:,.2f}, Target Date: {saves['target_date']}, Monthly Contribution: \\${saves['monthly_contribution']:,.2f}")

            saved_fig = create_savings_progress_chart(saves['current_savings_amount'], saves['planned_savings_amount'])
            st.pyplot(saved_fig)

        with col2:
            if st.button("Delete Savings", key=f"delete_savings_{saves['id']}"):
                num_rows_deleted = delete_savings(savings_id = saves['id'], profile_id = profile_id)

                if num_rows_deleted == 1:
                    st.success("Savings deleted successfully.")
                    st.rerun()
                else:
                    st.error("There was a problem. The savings wasn't deleted.")
        with col3:
            if st.button("Edit Savings", key=f"edit_savings_{saves['id']}"):
                st.session_state.editing_savings_id = saves['id']
        with col4:
            if st.button("Contribute", key=f"contribute_savings_{saves['id']}"):
                st.session_state.contribute_savings_id = saves['id']

        if st.session_state.get("editing_savings_id") == saves['id']:
            edit_savings_name = st.text_input("Enter savings name: ", value=saves['savings_name'], key=f"edit_savings_name_{saves['id']}")
            edit_target_amount = st.number_input("Enter target amount: ", min_value=100.0, value=saves['planned_savings_amount'], key=f"edit_target_amount_{saves['id']}")
            edit_current_savings = st.number_input("Enter your current savings amount: ", min_value=0.0, value=saves['current_savings_amount'], key=f"edit_current_savings_{saves['id']}")
            edit_monthly_contribution = st.number_input("Enter your monthly contribution: ", min_value=5.0, value=saves['monthly_contribution'], key=f"edit_monthly_contribution_{saves['id']}")
            existing_target_date = date.fromisoformat(saves['target_date'])
            edit_target_date = st.date_input("Target Date", value=existing_target_date, key=f"edit_target_date_{saves['id']}")
            edit_target_date_string = edit_target_date.isoformat()
            today = date.today()
            days_remaining = (edit_target_date - today).days
            target_months_timeline = max(round(days_remaining / 30.44), 1)

            if st.button("Save Changes", key=f"save_changes_{saves['id']}"):
                rows_updated = update_savings(saves['id'], profile_id, edit_savings_name, edit_target_amount, edit_current_savings, edit_monthly_contribution, edit_target_date_string, target_months_timeline)

                if rows_updated == 1:
                    st.success("Savings edited successfully.")
                    st.session_state.editing_savings_id = None
                    st.rerun()
                else:
                    st.error("There was a problem. The savings wasn't updated.")

        if st.session_state.get("contribute_savings_id") == saves['id']:
            contribute_amount = st.number_input("Enter the amount you'll want to contribute", min_value=0.01, max_value=float(saves['planned_savings_amount']), key=f"contribute_amount_{saves['id']}")
            contribution_date = st.date_input("Enter the date of the contribution", value=date.today(), key=f"contribution_date_{saves['id']}")

            contribution_date_string = contribution_date.isoformat()

            if st.button("Submit Contribution", key=f"contribution_save_{saves['id']}"):
                update_status = record_savings_contribution(profile_id, saves['id'], contribute_amount, contribution_date_string)

                if update_status == 1:
                    st.success("Savings contribution updated successfully.")
                    st.session_state.contribute_savings_id = None
                    st.rerun()
                else:
                    st.error("There was a problem. The savings contribution wasn't updated.")

