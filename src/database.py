import sqlite3

DB_NAME = 'data/finance_app.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financial_profile(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monthly_income REAL,
        total_expenses REAL,
        debt_balance REAL,
        debt_interest_rate REAL,
        emergency_fund REAL,
        investor_profile TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_financial_table(monthly_income, total_expenses, debt_balance,
                           debt_interest_rate, emergency_fund, investor_profile):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO financial_profile (monthly_income, total_expenses, debt_balance,
                   debt_interest_rate, emergency_fund, investor_profile) VALUES (?, ?, ?, ?, ?, ?)
                   """, (monthly_income, total_expenses, debt_balance, debt_interest_rate, emergency_fund,
                   investor_profile))

    conn.commit()
    conn.close()