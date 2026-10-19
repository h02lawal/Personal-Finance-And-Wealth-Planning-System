import math
from src.database import get_debt, get_depts_by_profile

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
        pass
    elif monthly_interest_rate == 0:
        months_to_payoff = math.ceil(debt_balance / monthly_payment)
        total_paid = debt_balance
        total_interest_paid = 0.0
    elif monthly_payment <= monthly_interest_amount:
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

def calculate_one_month_debt(debt_balance, annual_interest_rate, monthly_payment):
    monthly_interest_rate = (annual_interest_rate/100)/12
    monthly_interest = debt_balance * monthly_interest_rate

    total_debt = debt_balance + monthly_interest
    new_balance = total_debt - monthly_payment
    if new_balance < 0:
        return 0, monthly_interest, (monthly_payment - total_debt)
    else:
        return new_balance, monthly_interest, 0

def calculate_debt_payoff(profile_id:int, debt_id:int):
    debts = get_debt(profile_id, debt_id)
    number_of_months = 0
    total_interest_paid = 0

    if debts:
        balance = debts["debt_balance"]
        annual_ir = debts["annual_interest_rate"]

        monthly_interest = balance * ((annual_ir / 100) / 12)
        if debts["monthly_payment"] <= monthly_interest:
            return -1,-1

        while balance > 0:
            balance, interest_paid, excess = (calculate_one_month_debt(balance, annual_ir, debts["monthly_payment"]))
            number_of_months += 1
            total_interest_paid += interest_paid
    else:
        return -2,-2

    return number_of_months, total_interest_paid

def one_month_forecasting(profile_id:int):
    debts = get_depts_by_profile(profile_id)
    new_data = []
    if debts:
        for debt in debts:
            d_id = debt["id"]
            bal = debt["debt_balance"]
            air = debt["annual_interest_rate"]
            month_p = debt["monthly_payment"]

            new_bal, mon_int_pay, excess = calculate_one_month_debt(bal, air, month_p)
            new_data.append({"debt_id": d_id, "debt_name": debt["debt_name"], "debt_type": debt["debt_type"], "debt_balance": new_bal, "monthly_interest": mon_int_pay, "annual_interest_rate": debt["annual_interest_rate"], "monthly_payment": debt["monthly_payment"]})

        return new_data
    else:
        return -3

def highest_interest(debts):
    highest_interest_id = 0
    high_i_r_air = -1

    for debt in debts:
        if debt["balance"] > 0:
            if debt["annual_ir"] > high_i_r_air:
                high_i_r_air = debt["annual_ir"]
                highest_interest_id = debt["id"]

    return highest_interest_id


def lowest_balance(debts):
    lowest_balance_id = 0
    low_mon_bal = float("inf")

    for debt in debts:
        if debt["balance"] > 0:
            if debt["balance"] < low_mon_bal:
                low_mon_bal = debt["balance"]
                lowest_balance_id = debt["id"]

    return lowest_balance_id


def payments_until_complete(profile_id: int, technique: str = "avalanche",extra_monthly_payment: float = 0):
    debts = get_depts_by_profile(profile_id)
    temp_debt_storage = []
    months = 0
    total_interest = 0

    if technique not in ("avalanche", "snowball"):
        raise ValueError("Technique must be 'avalanche' or 'snowball'.")

    if extra_monthly_payment < 0:
        raise ValueError("Extra monthly payment cannot be negative.")

    if not debts:
        return -3

    for debt in debts:
        temp_debt_storage.append({"id": debt["id"], "balance": float(debt["debt_balance"]), "annual_ir": float(debt["annual_interest_rate"]), "monthly_pay": float(debt["monthly_payment"]), "duration_till_paid": 0})

    def get_priority_id():
        if technique == "avalanche":
            return highest_interest(temp_debt_storage)
        else:
            return lowest_balance(temp_debt_storage)

    while any(debt["balance"] > 0 for debt in temp_debt_storage):
        months += 1
        if months > 1200:
            return -1
        current_month_excess = extra_monthly_payment
        completed_debts = []

        for debt in temp_debt_storage:
            if debt["balance"] > 0:
                bal, mon_int_pay, excess = calculate_one_month_debt(debt["balance"], debt["annual_ir"], debt["monthly_pay"])
                debt["balance"] = bal
                total_interest += mon_int_pay
                current_month_excess += excess

                if debt["balance"] <= 0:
                    debt["duration_till_paid"] = months
                    completed_debts.append(debt)

        while current_month_excess > 0:
            priority_id = get_priority_id()
            if priority_id == 0:
                break

            for debt in temp_debt_storage:
                if debt["id"] == priority_id:
                    payment_applied = min(current_month_excess, debt["balance"])
                    debt["balance"] -= payment_applied
                    current_month_excess -= payment_applied

                    if debt["balance"] <= 0:
                        debt["balance"] = 0
                        debt["duration_till_paid"] = months
                        completed_debts.append(debt)
                    break

        for completed_debt in completed_debts:
            priority_id = get_priority_id()

            if priority_id == 0:
                break

            for debt in temp_debt_storage:
                if debt["id"] == priority_id:
                    debt["monthly_pay"] += completed_debt["monthly_pay"]
                    break

            completed_debt["monthly_pay"] = 0

    return {"months_to_payoff": months, "total_interest": total_interest, "debts": temp_debt_storage}