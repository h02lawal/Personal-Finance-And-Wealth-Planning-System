import sqlite3

DB_NAME = 'data/finance_app.db'

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

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
        investor_profile TEXT,
        risk_score INTEGER
    );
    """)

    conn.commit()
    conn.close()

def create_financial_profile() -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO financial_profile (monthly_income, total_expenses, debt_balance, debt_interest_rate, emergency_fund, investor_profile, risk_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (0.0, 0.0, 0.0, 0.0, 0.0, None, 0)
        )
        conn.commit()
        profile_id = cursor.lastrowid
        if profile_id is None:
            raise RuntimeError(
                "SQLite did not return a profile ID."
            )
        return profile_id
    finally:
        conn.close()

def insert_financial_table(monthly_income, total_expenses, debt_balance,
                           debt_interest_rate, emergency_fund, investor_profile, risk_score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO financial_profile (monthly_income, total_expenses, debt_balance,
                   debt_interest_rate, emergency_fund, investor_profile, risk_score) VALUES (?, ?, ?, ?, ?, ?, ?)
                   """, (monthly_income, total_expenses, debt_balance, debt_interest_rate, emergency_fund,
                   investor_profile, risk_score))

    conn.commit()
    conn.close()

def update_financial_table(profile_id, monthly_income, total_expenses, debt_balance, debt_interest_rate, emergency_fund, investor_profile, risk_score):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE financial_profile
        SET monthly_income = ?,
            total_expenses = ?,
            debt_balance = ?,
            debt_interest_rate = ?,
            emergency_fund = ?,
            investor_profile = ?,
            risk_score = ?
        WHERE id = ?
        """,(monthly_income, total_expenses, debt_balance, debt_interest_rate, emergency_fund, investor_profile, risk_score, profile_id)
    )

    rows_updated = cursor.rowcount

    conn.commit()
    conn.close()

    return rows_updated

def update_budget_profile(profile_id, monthly_income, total_expenses) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE financial_profile
        SET monthly_income = ?,
            total_expenses = ?
        WHERE id = ?
        """,(monthly_income, total_expenses, profile_id)
    )

    rows_updated = cursor.rowcount
    conn.commit()
    conn.close()

    return rows_updated

def get_financial_profiles():
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM financial_profile
        """)

        return cursor.fetchall()

    finally:
        conn.close()

def create_debts_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(""" 
     CREATE TABLE IF NOT EXISTS debts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    debt_name TEXT NOT NULL,
    debt_type TEXT NOT NULL,
    debt_balance REAL NOT NULL DEFAULT 0,
    annual_interest_rate REAL NOT NULL DEFAULT 0,
    monthly_payment REAL NOT NULL DEFAULT 0,
    credit_limit REAL,
    minimum_payment REAL,
    vehicle_value REAL,
    remaining_term_months INTEGER,
    property_value REAL,
    remaining_amortization_years INTEGER,
    repayment_plan TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id)
        REFERENCES financial_profile(id)
        ON DELETE CASCADE
);
     """)

    conn.commit()
    conn.close()

def insert_debt(profile_id, debt_name, debt_type, debt_balance, annual_interest_rate, monthly_payment, credit_limit: float|None=None, minimum_payment: float|None=None, vehicle_value: float| None=None, remaining_term_months: int | None=None, property_value: float|None=None, remaining_amortization_years: int|None=None, repayment_plan: str|None=None, description: str|None=None) -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO debts (profile_id, debt_name, debt_type, debt_balance, annual_interest_rate, monthly_payment, credit_limit, minimum_payment, vehicle_value, remaining_term_months, property_value, remaining_amortization_years, repayment_plan, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (profile_id, debt_name, debt_type, debt_balance, annual_interest_rate, monthly_payment, credit_limit, minimum_payment, vehicle_value, remaining_term_months, property_value, remaining_amortization_years, repayment_plan, description)
        )

        conn.commit()

        debt_id = cursor.lastrowid
        if debt_id is None:
            raise RuntimeError("SQLite did not return a debt ID.")

        return debt_id
    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

def get_depts_by_profile(profile_id:int):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT *
                   FROM debts d 
                       WHERE d.profile_id = ?
                       ORDER BY d.created_at DESC
                   """, (profile_id,))

    debts = cursor.fetchall()
    conn.close()

    return debts

def create_savings_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS savings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    savings_name TEXT NOT NULL,
    planned_savings_amount REAL NOT NULL DEFAULT 0,
    current_savings_amount REAL NOT NULL DEFAULT 0,
    timeline REAL NOT NULL,
    monthly_contribution REAL NOT NULL DEFAULT 0,
    target_date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES financial_profile(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

def insert_savings(profile_id, savings_name, planned_savings_amount, current_savings, timeline, contribution, target_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO savings(profile_id, savings_name, planned_savings_amount, current_savings_amount, timeline, monthly_contribution, target_date) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (profile_id, savings_name, planned_savings_amount, current_savings, timeline, contribution, target_date))

    conn.commit()
    conn.close()

def display_savings_table(profile_id:int):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM savings s
    WHERE s.profile_id = ?
    ORDER BY s.created_at DESC
    """, (profile_id,))

    savings = cursor.fetchall()
    conn.close()

    return savings

def update_investor_profile(profile_id:int, risk_score:int, investor_profile:str) -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE financial_profile 
            SET investor_profile = ?,
            risk_score = ?
            WHERE id = ?
            """,
            (investor_profile, risk_score, profile_id)
        )

        rows_updated = cursor.rowcount
        conn.commit()
        return rows_updated

    finally:
        conn.close()

def get_financial_profile(profile_id:int):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * 
        FROM financial_profile 
        WHERE id = ?
        """, (profile_id,)
                       )
        return cursor.fetchone()
    finally:
        conn.close()