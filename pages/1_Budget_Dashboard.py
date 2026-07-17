import streamlit as st
from src.calculations import calculate_savings_rate
from src.visualizations import create_budget_pie_chart

st.set_page_config(
    page_title="Budget Planner",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Budget Planner")
st.write("Enter the Information Below: ")


monthly_income = st.number_input(  "How much do you earn each month: ",min_value=0.0)
rent = st.number_input( "How much do you pay for rent each month: ",min_value=0.0)
food = st.number_input( "How much does food cost you in a month: ",min_value=0.0)
transportation = st.number_input( "How much does transportation cost you each month: ",min_value=0.0)
utilities = st.number_input( "How much does utilities cost you each month: ",min_value=0.0)
subscriptions = st.number_input( "How much are your subscriptions each month: ",min_value=0.0)

total_expenses = rent+food+transportation+utilities+subscriptions
remaining_balance = monthly_income - total_expenses
savings_rate = calculate_savings_rate(monthly_income, total_expenses)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total expense",
        f"${total_expenses:.2f}"
    )

with col2:
    st.metric(
        "Remaining Funds",
        f"${remaining_balance:.2f}"
    )

with col3:
    st.metric(
        "Savings Rate",
        f"${savings_rate:.1%}"
    )

with col4:
    st.metric(
        "Recommended min. savings at 20%",
        f"${0.2*monthly_income:.2f}"
    )

if savings_rate >= 0.40:
    st.success("Excellent savings habits.")
elif savings_rate >= 0.10:
    st.warning("Good progress.")
else:
    st.error(
        "Your savings rate is low. Consider reducing expenses."
    )

#Create expense budget dictionary or list
expenses = {"Rent":rent, "Food":food,
            "Transportation":transportation, "Utilities":utilities, "Subscriptions":subscriptions}

if total_expenses>0:
    fig = create_budget_pie_chart(expenses)
    st.pyplot(fig)


st.session_state["monthly_income"] = monthly_income
st.session_state["total_expenses"] = total_expenses
st.session_state["remaining_balance"] = remaining_balance
st.session_state["savings_rate"] = savings_rate
