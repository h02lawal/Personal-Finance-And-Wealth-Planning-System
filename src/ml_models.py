def predict_spending_risk(savings_rate, debt_interest_rate, emergency_fund_months):
    if savings_rate < 0.05 and debt_interest_rate > 15:
        return "High Risk"
    elif savings_rate < 0.10 or emergency_fund_months < 3:
        return "Medium Risk"
    else:
        return "Low Risk"