import matplotlib.pyplot as plt

def create_budget_pie_chart(expense_data):
    expense_data = {key: value for key, value in expense_data.items() if value > 0}
    fig, ax = plt.subplots()
    ax.pie(expense_data.values(), labels=expense_data.keys(), autopct="%1.1f%%")
    ax.set_title("Expense Breakdown")
    return fig

def create_savings_progress_chart(current_savings, target_amount):
    fig, ax = plt.subplots()
    remaining = max(target_amount - current_savings, 0)

    ax.bar(["Current Savings", "Remaining"], [current_savings, remaining])
    ax.set_title("Savings Goal Progress")
    ax.set_ylabel("Amount ($)")
    return fig