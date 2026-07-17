import streamlit as st

st.set_page_config(
    page_title="Investment Profile",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Investment Profile")
st.write("Enter the Information Below: ")

age = st.number_input("Enter your age", min_value=18)
investment_horizon = st.selectbox("How long do you plan to Invest", ["Less than 3 years","3-5 years","5-10 years","10+ years"])
investment_experience = st.selectbox("What is your investment experience level", ["Beginner","Intermediate","Advanced"])
market_drop = st.selectbox("If your portfolio dropped 20%, what would you do", ["Sell Everything","Sell some investments","Do nothing","Buy more"])

risk_score = 0
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

if risk_score <= 4:
    profile = "Conservative"
elif risk_score <= 7:
    profile = "Moderate"
else:
    profile = "Aggressive"

if profile == "Conservative":
    stocks = 30
    bonds = 60
    cash = 10
elif profile == "Moderate":
    stocks = 60
    bonds = 30
    cash = 10
else:
    stocks = 80
    bonds = 15
    cash = 5

st.metric( "Investor Profile", profile)

st.write(
    f"""
    Suggested educational allocation:

    Stocks: {stocks}%

    Bonds: {bonds}%

    Cash: {cash}%
    """
)

if profile == "Conservative":
    st.info("You prioritize capital preservation and lower volatility.")
elif profile == "Moderate":
    st.info("You seek a balance between growth and stability.")
else:
    st.info("You are comfortable with higher risk in pursuit of higher returns.")

st.session_state["investor_profile"] = profile