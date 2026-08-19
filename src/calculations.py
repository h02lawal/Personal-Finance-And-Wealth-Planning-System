import math

def calculate_savings_rate(monthly_income, total_expenses):
    if monthly_income <= 0:
        return 0
    return (monthly_income-total_expenses)/monthly_income

def financial_health_score(savings_rate, debt_to_income, emergency_fund_months, remaining_balance, savings_goal_progress, total_monthly_contributions, total_savings_targets):
    score = 100


    has_saving_goal = total_savings_targets > 0

    if savings_rate < 0:
        score -= 25
    elif savings_rate < 0.10:
        score -= 15
    elif savings_rate < 0.20:
        score -= 5

    if debt_to_income >= 0.50:
        score -= 25
    elif debt_to_income >= 0.35:
        score -= 15
    elif debt_to_income >= 0.20:
        score -= 5

    if emergency_fund_months < 1:
        score -= 15
    elif emergency_fund_months < 3:
        score -= 10
    elif emergency_fund_months < 6:
        score -= 5

    if remaining_balance < 0:
        score -= 20
    elif remaining_balance == 0:
        score -= 10

    if has_saving_goal:
        if savings_goal_progress < 0.10:
            score -= 10
        elif savings_goal_progress < 0.25:
            score -= 5

        if total_monthly_contributions <= 0:
            score -= 5

    return max(0, min(score, 100))

def debt_information(debt_balance, monthly_payment, monthly_interest_rate, monthly_interest_amount):
    months_to_payoff = None
    total_paid = None
    total_interest_paid = None

    if debt_balance == 0:
        months_to_payoff = 0
        total_paid = 0.0
        total_interest_paid = 0.0
    elif monthly_payment <= 0:
        # No payoff calculation is possible without a payment.
        pass
    elif monthly_interest_rate == 0:
        # No-interest debt.
        months_to_payoff = math.ceil(debt_balance / monthly_payment)
        total_paid = debt_balance
        total_interest_paid = 0.0
    elif monthly_payment <= monthly_interest_amount:
        # Payment does not cover the monthly interest.
        # The balance will not decrease.
        pass
    else:
        months_to_payoff = math.ceil(
            -math.log(
                1 - (
                        debt_balance
                        * monthly_interest_rate
                        / monthly_payment
                )
            )
            / math.log(1 + monthly_interest_rate)
        )
        total_paid = months_to_payoff * monthly_payment
        total_interest_paid = total_paid - debt_balance
    return months_to_payoff, total_paid, total_interest_paid

