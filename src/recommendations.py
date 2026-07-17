import streamlit as st

def get_financial_recommendation(monthly_income, savings_rate, debt_balance,
                                 debt_interest_rate, emergency_fund_months,
                                 investor_profile):
    if monthly_income == 0:
        st.info("Enter your financial information to receive a recommendation.")
    elif debt_interest_rate >= 15 and debt_balance > 0:
        st.warning("You have high-interest debt. Consider prioritizing debt repayment before increasing investments.")
    elif emergency_fund_months < 3:
        st.warning("Your emergency fund is below 3 months of expenses. Consider building your emergency savings first.")
    elif savings_rate < 0.10:
        st.warning("Your savings rate is below 10%. Consider reducing non-essential expenses.")
    elif investor_profile == "Aggressive" and emergency_fund_months < 6:
        st.info(
            "You have an aggressive investor profile, but you may want a stronger emergency fund before taking higher investment risk.")
    else:
        st.success(
            "Your financial foundation looks stable. You may be ready to focus more on long-term wealth building.")