
import streamlit as st
from datetime import date
from src.calculations import debt_information
from src.database import insert_debt, get_depts_by_profile, delete_debt, update_debt, record_debt_payment


st.set_page_config(
    page_title="Debt Planner",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Debt Planner")
st.write("Enter the Information Below: ")

debt_name = st.text_input("Enter the name of the debt")
debt_type = st.selectbox("What type of debt",
                         ["Credit Card", "Car Loan", "Student Loan", "Personal Loan", "Mortgage", "Other"])

debt_balance = st.number_input("Enter the balance of the debt", min_value=0.0)
annual_interest_rate = st.number_input("Annual Interest Rate: ",min_value=0.0, max_value=100.0, value=19.99)
monthly_payment = st.number_input("Monthly Payment: ",min_value=0.0)
monthly_interest_rate = annual_interest_rate/100/12

credit_limit: float|None = None
credit_utilization: float |None=None
minimum_payment: float |None = None
vehicle_value: float | None = None
remaining_term_months: int | None = None
property_value: float | None = None
remaining_amortization_years: int | None = None
repayment_plan: str | None = None
description: str | None = None

if debt_type == "Credit Card":
    credit_limit = float(st.number_input("Credit limit", min_value=1.0, step=100.0))
    minimum_payment = float(st.number_input("Required minimum payment", min_value=0.0, step=10.0))
    assert credit_limit is not None
    credit_utilization = (debt_balance / credit_limit * 100)

elif debt_type == "Car Loan":
    vehicle_value = float(st.number_input("Estimated vehicle value", min_value=0.0, step=100.0))
    remaining_term_months = int(st.number_input("Remaining term in months", min_value=1, step=1))

elif debt_type == "Mortgage":
    property_value = float(st.number_input("Estimated property value", min_value=0.0, step=1000.0))
    remaining_amortization_years = int(st.number_input("Remaining amortization in years", min_value=1, step=1))

elif debt_type == "Student Loan":
    repayment_plan = st.selectbox("Repayment plan", ["Standard", "Extended", "Income-Based", "Interest-Free", "Other"])

elif debt_type == "Other":
    description = st.text_input("Brief description of the debt")

debt = {
    "debt_type":debt_type,
    "balance":debt_balance,
    "interest_rate":annual_interest_rate,
    "monthly_payment":monthly_payment
}

monthly_interest_rate = annual_interest_rate / 100 / 12
monthly_interest_amount = monthly_interest_rate * debt_balance
effective_annual_interest_rate = annual_interest_rate

####Student Loan

if (debt["debt_type"] == "Student Loan") and (repayment_plan == "Interest-Free"):
    effective_annual_interest_rate = 0.0
    monthly_interest_rate = (effective_annual_interest_rate / 100 / 12)
    monthly_interest_amount = (monthly_interest_rate * debt_balance)

####Student Loan

months_to_payoff, total_paid, total_interest_paid = debt_information(debt_balance, monthly_payment, monthly_interest_rate, monthly_interest_amount)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Monthly Interest", f"${monthly_interest_amount:.2f}")

with col2:
    st.metric("Months to Pay Off", months_to_payoff)

with col3:
    if total_interest_paid is None:
        st.metric("Total Interest Paid", "N/A")
    else:
        st.metric("Total Interest Paid", f"${total_interest_paid:.2f}")


#### Student Loan

if debt["debt_type"] == "Student Loan":
    if repayment_plan == "Income-Based":
        st.info(
            "Income-based payments may change when the borrower's"
            "income changes, so the current payoff estimate is approximate "
        )
    elif repayment_plan == "Extended":
        st.warning(
            "An extended repayment plan may reduce the monthly payment "
            "but increase the total interest paid."
        )
    elif repayment_plan == "Other":
        st.info(
            "The payoff estimate uses the entered payment and interest "
            "rate because the selected repayment plan is not predefined."
        )

#### Student Loan

#### Credit Card

if debt["debt_type"] == "Credit Card" and credit_utilization is not None:
    if credit_utilization > 90:
        st.error(f"Credit utilization is currently at {credit_utilization:.1f}%, consider reducing it.")
    elif credit_utilization > 30:
        st.warning(f"Credit utilization is high at {credit_utilization:.1f}%, consider reducing the balance.")
if debt["debt_type"] == "Credit Card" and minimum_payment is not None:
    if minimum_payment > 0 and monthly_payment < minimum_payment:
        st.error(f"Your monthly payment of {monthly_payment:.2f}is too low. It does not cover the required minimum payment of {minimum_payment}")
if debt_type == "Credit Card" and credit_limit is not None and 0 < credit_limit < debt_balance:
    st.error("The entered balance exceeds the credit limit. Verify the balance or credit limit.")


#### Credit Card

#### Car Loan
if debt["debt_type"] == "Car Loan" and vehicle_value is not None and remaining_term_months is not None:

    loan_to_value = (debt_balance/vehicle_value * 100 if vehicle_value > 0 else None)

    if loan_to_value is not None and loan_to_value > 100:
        st.warning(f"The loan-to-value ratio is {loan_to_value:.1f}%."
                   "You currently owe more than the estimated vehicle value."
                   )
    if months_to_payoff is not None and remaining_term_months is not None and months_to_payoff > remaining_term_months:
        st.warning(
            "Your calculated payoff period is longer than the "
            "remaining loan term."
        )
#### Car Loan

####Mortgage

if debt["debt_type"] == "Mortgage" and property_value is not None and remaining_amortization_years is not None:
    remaining_years = remaining_amortization_years

    remaining_months = (remaining_years * 12 if remaining_years is not None else None)
    mortgage_ltv = (debt_balance/property_value*100 if property_value > 0 else None)

    if mortgage_ltv is not None:
        st.metric("Mortgage LTV", f"{mortgage_ltv:.1f}%")

    if months_to_payoff is not None and remaining_months is not None and abs(months_to_payoff - remaining_months) > 12:
        st.info(
            "The calculated payoff time differs significantly from "
            "the entered remaining amortization."
        )

####Mortgage

if debt_balance == 0:
    st.info("Enter your debt details to calculate a payoff plan")
elif monthly_payment <= monthly_interest_amount:
    st.error(f"Your monthly payment is too low. It does not cover the monthly interest of ${monthly_interest_amount:.2f}.")
elif effective_annual_interest_rate >= 15:
    st.warning("This is a high interest debt, consider prioritizing the debt first.")
else:
    st.success("Your debt payoff plan looks manageable based on your current payment.")

if "financial_profile" not in st.session_state:
    st.session_state.financial_profile = {}

profile = st.session_state.financial_profile
profile_id = st.session_state.get("profile_id")

if not isinstance(profile_id, int):
    st.error("Select or create a profile first.")
    st.stop()

profile["debt_balance"] = debt_balance
profile["debt_interest_rate"] = annual_interest_rate

if not debt_name.strip():
    st.error("Enter a debt name.")
elif debt_balance <= 0:
    st.error("Debt balance must be greater than zero.")
elif monthly_payment <= 0:
    st.error("Monthly payment must be greater than zero.")
else:
    if st.button("Save Debt"):
        insert_debt(
            profile_id=profile_id,
            debt_name=debt_name,
            debt_type=debt_type,
            debt_balance=debt_balance,
            annual_interest_rate=effective_annual_interest_rate,
            monthly_payment=monthly_payment,
            credit_limit=credit_limit,
            minimum_payment=minimum_payment,
            vehicle_value=vehicle_value,
            remaining_term_months=remaining_term_months,
            property_value=property_value,
            remaining_amortization_years=remaining_amortization_years,
            repayment_plan=repayment_plan,
            description=description
        )

        st.success("Debt saved successfully.")

debts = get_depts_by_profile(profile_id)

st.subheader("Saved Debts")
if not debts:
    st.info("No debts have been saved yet for that Profile ID")
else:
    for debt in debts:
        col1, col2, col3, col4 = st.columns([5,2,2,2])

        with col1:
            st.write(f"Debt: {debt['debt_name']}, Debt Balance: ${debt['debt_balance']:,.2f}")
        with col2:
            if st.button("Delete Debt", key=f"delete_debt_{debt['id']}"):
                num_rows_deleted = delete_debt(profile_id, debt['id'])
                if num_rows_deleted == 1:
                    st.write(f"Debt with id {debt['id']} has been deleted successfully")
                    st.rerun()
                else:
                    st.error("The debt couldn't be found or deleted")
        with col3:
            if st.button("Edit Debt", key=f"edit_debt_{debt['id']}"):
                st.session_state.editing_debt_id = debt['id']
        with col4:
            if st.button("Record Payment", key=f"record_payment{debt['id']}"):
                st.session_state.payment_debt_id = debt['id']

        if st.session_state.get("editing_debt_id") == debt["id"]:
            editing_debt_type = debt["debt_type"]
            editing_debt_name = st.text_input("Enter new debt name", value=debt["debt_name"], key=f"editing_debt_name_{debt['id']}")
            editing_debt_balance = st.number_input("Enter new debt balance", min_value=0.0,value=float(debt["debt_balance"] or 0), key=f"editing_debt_balance_{debt['id']}")
            editing_annual_interest_rate = st.number_input("Enter new interest rate", min_value=0.0, max_value=100.0,value=float(debt["annual_interest_rate"] or 0), key=f"editing_annual_interest_rate_{debt['id']}")
            editing_monthly_payment = st.number_input("Enter new monthly payment", min_value=0.0,value=float(debt["monthly_payment"] or 0), key=f"editing_monthly_payment_{debt['id']}")
            editing_monthly_interest_rate = editing_annual_interest_rate / 100 / 12

            editing_credit_limit = None
            editing_minimum_payment = None
            editing_vehicle_value = None
            editing_remaining_term_months = None
            editing_property_value = None
            editing_remaining_amortization_years = None
            editing_repayment_plan = None
            editing_description = None

            if editing_debt_type == "Credit Card":
                editing_credit_limit = float(st.number_input("Enter new Credit Limit", min_value=1.0, step=100.0, value=float(debt["credit_limit"] or 1), key=f"editing_credit_limit_{debt['id']}"))
                editing_minimum_payment = float(st.number_input("Enter new minimum payment", min_value=0.0, step=10.0, value=float(debt["minimum_payment"] or 0), key=f"editing_minimum_payment_{debt['id']}"))
                editing_credit_utilization = (editing_debt_balance / editing_credit_limit * 100)
            elif editing_debt_type == "Car Loan":
                editing_vehicle_value = float(st.number_input("Enter new vehicle value", min_value=0.0, step=100.0, value = float(debt["vehicle_value"] or 0), key=f"editing_vehicle_value_{debt['id']}"))
                editing_remaining_term_months = int(st.number_input("Enter new remaining term months", min_value=1, step=1, value=int(debt["remaining_term_months"] or 1), key=f"editing_remaining_term_months_{debt['id']}"))
            elif editing_debt_type == "Mortgage":
                editing_property_value = float(st.number_input("Enter new estimated property value", min_value=0.0, step=1000.0, value=float(debt["property_value"] or 0.0), key=f"editing_property_value_{debt['id']}"))
                editing_remaining_amortization_years = int(st.number_input("Enter new remaining amortization in years", min_value=1, step=1, value=int(debt["remaining_amortization_years"] or 1), key=f"editing_remaining_amortization_years_{debt['id']}"))
            elif editing_debt_type == "Student Loan":
                repayment_options = ["Standard", "Extended", "Income-Based", "Interest-Free", "Other"]
                editing_repayment_plan = st.selectbox("Enter new repayment plan", repayment_options, index=repayment_options.index(debt["repayment_plan"] or "Standard"), key=f"editing_repayment_plan_{debt['id']}")
                if editing_repayment_plan == "Interest-Free":
                    editing_annual_interest_rate = 0.0
                    editing_monthly_interest_rate = (editing_annual_interest_rate / 100 / 12)
                    editing_monthly_interest_amount = (editing_monthly_interest_rate * editing_debt_balance)
            elif editing_debt_type == "Other":
                editing_description = st.text_input("Enter a new description here", value=debt["description"] or "", key=f"editing_description_{debt['id']}")

            if st.button("Save Changes", key=f"save_debt_{debt['id']}"):
                num_rows_updated = update_debt(profile_id, debt["id"], editing_debt_type, editing_debt_name, editing_debt_balance, editing_annual_interest_rate, editing_monthly_payment, editing_credit_limit, editing_minimum_payment, editing_vehicle_value, editing_remaining_term_months, editing_property_value, editing_remaining_amortization_years, editing_repayment_plan, editing_description)
                if num_rows_updated == 1:
                    st.success("Debt updated successfully.")
                    st.session_state.editing_debt_id = None
                    st.rerun()
                else:
                    st.error("Something went wrong. The debt could not be updated.")

        if st.session_state.get("payment_debt_id") == debt['id']:
            payment_amount = st.number_input("Enter the amount you'll like to pay", min_value=0.01, max_value=float(debt['debt_balance']), key=f"payment_amount_{debt['id']}")
            payment_date = st.date_input("Enter the payment date", value=date.today(), key=f"payment_date_{debt['id']}" )

            if st.button("Submit Payment", key=f"submit_payment_{debt['id']}"):
                payment_date_string = payment_date.isoformat()

                rows_updated = record_debt_payment(profile_id, debt['id'], payment_amount, payment_date_string)

                if rows_updated == 1:
                    st.write("Debt updated successfully.")
                    st.session_state.payment_debt_id = None
                    st.rerun()
                else:
                    st.error("Payment not accepted")