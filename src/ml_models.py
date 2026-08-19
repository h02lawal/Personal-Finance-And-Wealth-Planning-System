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