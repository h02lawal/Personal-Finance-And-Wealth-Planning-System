import streamlit as st
from src.database import update_investor_profile

st.set_page_config(
    page_title="Investment Profile",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Investment Profile")
st.write("Enter the Information Below: ")

investment_horizon = st.selectbox("How long do you plan to Invest", ["Less than 3 years","3-5 years","5-10 years","10+ years"])
investment_experience = st.selectbox("What is your investment experience level", ["Beginner","Intermediate","Advanced"])
market_drop = st.selectbox("If your portfolio dropped 20%, what would you do", ["Sell Everything","Sell some investments","Do nothing","Buy more"])
income_stability = st.selectbox("How stable is your income?", ["Unstable","Somewhat Stable","Very Stable"])
investment_goal = st.selectbox("Primary investment goal",["Capital Preservation", "Income", "Balanced Growth", "Long-Term Growth"])
liquidity_need = st.selectbox("How likely are you to need this money soon?", ["Very Likely", "Possibly", "Unlikely"])


risk_score = 0

if liquidity_need == "Unlikely":
    risk_score += 2
elif liquidity_need == "Possibly":
    risk_score += 1
else:
    risk_score -= 1

if investment_goal == "Capital Preservation":
    risk_score += 0
elif investment_goal == "Income":
    risk_score += 1
elif investment_goal == "Balanced Growth":
    risk_score += 2
else:
    risk_score += 3

if income_stability == "Unstable":
    risk_score -= 1
elif income_stability == "Somewhat Stable":
    risk_score += 1
else:
    risk_score += 2

if investment_horizon == "10+ years":
    risk_score += 3
elif investment_horizon == "5-10 years":
    risk_score += 2
else:
    risk_score += 1

if investment_experience == "Advanced":
    risk_score += 3
elif investment_experience == "Intermediate":
    risk_score += 2
else:
    risk_score += 1

if market_drop == "Buy more":
    risk_score += 3
elif market_drop == "Do nothing":
    risk_score += 2
elif market_drop == "Sell some investments":
    risk_score += 1
else:
    risk_score += 0

if risk_score <= 5:
    investor_profile = "Conservative"
elif risk_score <= 10:
    investor_profile = "Moderate"
else:
    investor_profile = "Aggressive"

if investor_profile == "Conservative":
    stocks = 30
    bonds = 60
    cash = 10
elif investor_profile == "Moderate":
    stocks = 60
    bonds = 30
    cash = 10
else:
    stocks = 80
    bonds = 15
    cash = 5

st.metric( "Investor Profile", investor_profile)

st.write(
    f"""
    Suggested educational allocation:

    Stocks: {stocks}%

    Bonds: {bonds}%

    Cash: {cash}%
    """
)

if investor_profile == "Conservative":
    st.info("You prioritize capital preservation and lower volatility.")
elif investor_profile == "Moderate":
    st.info("You seek a balance between growth and stability.")
else:
    st.info("You are comfortable with higher risk in pursuit of higher returns.")

if "financial_profile" not in st.session_state:
    st.session_state.financial_profile = {}

finance_profile = st.session_state.financial_profile
finance_profile["investor_profile"] = investor_profile
finance_profile["risk_score"] = risk_score
profile_id = st.session_state.get("profile_id")

if st.button("Save Investment Profile"):
    if profile_id is None:
        st.error("No financial profile is currently active")
    else:
        rows_updated = update_investor_profile(profile_id, risk_score, investor_profile)
        st.success("Investment Profile Saved")
