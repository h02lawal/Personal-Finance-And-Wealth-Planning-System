
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "financial_risk_model.joblib"


@st.cache_resource
def load_financial_risk_model():
    return joblib.load(MODEL_PATH)


def predict_six_month_shortfall(monthly_income, monthly_expenses, liquid_savings, total_debt):
    model = load_financial_risk_model()

    features = pd.DataFrame([{
        "income": monthly_income,
        "expense": monthly_expenses,
        "savings": liquid_savings,
        "debt": total_debt
    }])

    probability = float(model.predict_proba(features)[0, 1])
    prediction = "Yes" if probability >= 0.5 else "No"

    return prediction, probability


def predict_financial_risk(savings_rate, debt_interest_rate, emergency_fund_months, debt_to_income, savings_goal_progress):
    risk_points = 0

    #savings_rate
    if savings_rate < 0.10:
        risk_points += 2
    elif savings_rate < 0.20:
        risk_points += 1

    #Debt interest
    if debt_interest_rate >= 15:
        risk_points += 2
    elif debt_interest_rate >= 8:
        risk_points += 1

    #Debt_to_Income
    if debt_to_income >= 0.40:
        risk_points += 2
    elif debt_to_income >= 0.25:
        risk_points += 1

    #Emergency Fund Capacity
    if emergency_fund_months < 1:
        risk_points += 2
    elif emergency_fund_months < 3:
        risk_points += 1

    #Savings goal Progress
    if savings_goal_progress < 0.25:
        risk_points += 1

    if risk_points >= 7:
        return "High Risk"
    elif risk_points >= 4:
        return "Medium Risk"
    else:
        return "Low Risk"