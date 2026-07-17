

def calculate_savings_rate(monthly_income, total_expenses):
    if monthly_income <= 0:
        return 0
    return (monthly_income-total_expenses)/monthly_income