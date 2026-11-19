import numpy as np
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
output_path = PROJECT_ROOT / "data" / "synthetic_financial_data.csv"
np.random.seed(42)
num_rows = 40000

income = np.random.lognormal(mean=11.0, sigma=0.4, size=num_rows)
income = np.round(income, 2)

expense_ratio = np.random.uniform(low=0.55, high=1.20, size=num_rows)
expense = (income * expense_ratio + np.random.normal(0, 2000, size=num_rows)).clip(min=12000).round(2)

disposable = np.maximum(0, income-expense)
savings = (disposable * np.random.uniform(0.05, 0.50, size=num_rows)+ np.random.exponential(scale=2000, size=num_rows)).round(2)


debt_factor = np.random.exponential(scale=0.35, size=num_rows)
debt = (income * debt_factor + np.maximum(0, expense-income) * 2).round(2)

remaining_savings = savings.copy()
shortfall = np.zeros(num_rows, dtype=bool)

for month in range(6):
    monthly_income = (income / 12) * np.random.normal(1.0, 0.08, num_rows)
    monthly_income = np.clip(monthly_income, a_min=0, a_max=np.inf)
    income_disruption = np.random.random(num_rows) < 0.05
    monthly_income = np.where(income_disruption, monthly_income * np.random.uniform(0.2, 0.7, size=num_rows),monthly_income)
    unexpected_expenses = np.where( np.random.random(num_rows) < 0.15, np.random.exponential(1000, num_rows), 0.0)

    monthly_expenses = (expense / 12) + unexpected_expenses
    remaining_savings += monthly_income - monthly_expenses
    shortfall |= remaining_savings < 0

label = np.where(shortfall, "Yes", "No")


df = pd.DataFrame({
    "income": (income/12).round(2),
    "expense": (expense/12).round(2),
    "savings": savings,
    "debt": debt,
    "label": label
})

df.to_csv(output_path, index=False)

