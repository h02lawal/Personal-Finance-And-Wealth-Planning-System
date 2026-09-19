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

def delete_debt(profile_id: int, debt_id: int) -> int:
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM debts
            WHERE profile_id = ? AND id = ?
            
        """, (profile_id, debt_id))
        rows_deleted = cursor.rowcount
        conn.commit()
        return rows_deleted

    except Exception:
        conn.rollback()
        raise

    finally:
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

def update_debt(profile_id:int, debt_id:int, debt_type:str, debt_name:str, debt_balance:float, annual_interest_rate:float, monthly_payment: float, credit_limit:float|None=None, minimum_payment:float|None=None, vehicle_value:float|None=None, remaining_term_months:int|None=None, property_value:float|None=None, remaining_amortization_years: int|None=None, repayment_plan: str|None=None, description: str|None=None) -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if debt_type == "Credit Card":
            cursor.execute("""
            UPDATE debts 
            SET debt_name = ?,
            debt_balance = ?,
            annual_interest_rate = ?,
            monthly_payment = ?,
            credit_limit = ?,
            minimum_payment = ?
            WHERE id = ? AND profile_id = ?
            """, (debt_name, debt_balance, annual_interest_rate, monthly_payment, credit_limit, minimum_payment, debt_id, profile_id))
        elif debt_type == "Car Loan":
            cursor.execute("""
            UPDATE debts 
            SET debt_name = ?,
            debt_balance = ?,
            annual_interest_rate = ?,
            monthly_payment = ?,
            vehicle_value = ?,
            remaining_term_months = ?
            WHERE id = ? AND profile_id = ?
            """, (debt_name, debt_balance, annual_interest_rate, monthly_payment, vehicle_value, remaining_term_months, debt_id, profile_id))
        elif debt_type == "Mortgage":
            cursor.execute("""
            UPDATE debts 
            SET debt_name = ?,
            debt_balance = ?,
            annual_interest_rate = ?,
            monthly_payment = ?,
            property_value = ?,
            remaining_amortization_years = ?
            WHERE id = ? AND profile_id = ?
            """, (debt_name, debt_balance, annual_interest_rate, monthly_payment, property_value, remaining_amortization_years, debt_id, profile_id))
        elif debt_type == "Student Loan":
            if repayment_plan == "Interest-Free":
                annual_interest_rate = 0.0

            cursor.execute("""
            UPDATE debts 
            SET debt_name = ?,
            debt_balance = ?,
            annual_interest_rate = ?,
            monthly_payment = ?,
            repayment_plan = ?
            WHERE id = ? AND profile_id = ?
            """, (debt_name, debt_balance, annual_interest_rate, monthly_payment, repayment_plan, debt_id, profile_id))
        elif debt_type == "Personal Loan":
            cursor.execute("""
            UPDATE debts
            SET debt_name = ?,
            debt_balance = ?,
            annual_interest_rate = ?,
            monthly_payment = ?
            WHERE id = ? AND profile_id = ?
            """,(debt_name, debt_balance, annual_interest_rate, monthly_payment, debt_id, profile_id))

        elif debt_type == "Other":
            cursor.execute("""
            UPDATE debts 
            SET debt_name = ?,
            debt_balance = ?,
            annual_interest_rate = ?,
            monthly_payment = ?,
            description = ?
            WHERE id = ? AND profile_id = ?
            """, (debt_name, debt_balance, annual_interest_rate, monthly_payment, description, debt_id, profile_id))

        rows_updated = cursor.rowcount
        conn.commit()
        return rows_updated
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def delete_savings(savings_id, profile_id) -> int:
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM savings 
        WHERE id = ? AND profile_id = ?
        """, (savings_id, profile_id))

        rows_deleted = cursor.rowcount
        conn.commit()
        return rows_deleted

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

def update_savings(savings_id, profile_id, savings_name, planned_savings, current_savings, monthly_contribution, target_date, timeline) -> int :
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE savings 
        SET savings_name = ?,
        planned_savings_amount = ?,
        current_savings_amount = ?,
        monthly_contribution = ?,
        target_date = ?,
        timeline = ?
        WHERE id = ? AND profile_id = ?
        """, (savings_name, planned_savings, current_savings, monthly_contribution, target_date, timeline, savings_id, profile_id))

        rows_updated = cursor.rowcount
        conn.commit()
        return rows_updated

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def create_debt_payment_history():
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS debt_payment_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        debt_id INTEGER NOT NULL,
        payment_amount REAL NOT NULL,
        payment_date TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (debt_id) REFERENCES debts(id) ON DELETE CASCADE
        );
        """)

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_debt_payments(debt_id) -> list:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT *
        FROM debt_payment_history
        WHERE debt_id = ?
        ORDER BY payment_date DESC
        """, (debt_id,))

        rows = cursor.fetchall()
        conn.commit()
        return rows
    finally:
        conn.close()

def get_total_debt_payments(debt_id) -> int:
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT COALESCE(SUM(payment_amount), 0)
        FROM debt_payment_history
        WHERE debt_id = ?
        """, (debt_id,))

        total_paid = cursor.fetchone()[0]
        return total_paid
    finally:
        conn.close()

def insert_debt_payment(debt_id, payment_amount, payment_date):
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO debt_payment_history (debt_id, payment_amount, payment_date) VALUES (?, ?, ?)
        """, (debt_id, payment_amount, payment_date))

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

def update_debt_balance_after_payment(debt_id, profile_id, payment_amount) -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE debts 
        SET debt_balance = debt_balance - ?
        WHERE debts.id = ? AND debts.profile_id = ?
        """, (payment_amount, debt_id, profile_id))

        rows_updated = cursor.rowcount
        conn.commit()
        return rows_updated
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def record_debt_payment(profile_id, debt_id, payment_amount,payment_date):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT debt_balance
            FROM debts
            WHERE id = ? AND profile_id = ?
        """, (debt_id, profile_id))

        debt = cursor.fetchone()

        if debt is None:
            return 0

        current_balance = debt[0]

        if payment_amount <= 0:
            return 0

        if payment_amount > current_balance:
            return 0

        cursor.execute("""
            INSERT INTO debt_payment_history(debt_id, payment_amount, payment_date) VALUES (?, ?, ?)
        """, (debt_id, payment_amount, payment_date))

        cursor.execute("""
            UPDATE debts
            SET debt_balance = debt_balance - ?
            WHERE id = ? AND profile_id = ?
        """, (payment_amount, debt_id, profile_id))

        rows_updated = cursor.rowcount
        conn.commit()
        return rows_updated

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

def create_savings_contributions():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS savings_contributions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        savings_id INTEGER NOT NULL,
        contribution_amount REAL NOT NULL,
        contribution_date TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (savings_id) REFERENCES savings(id) ON DELETE CASCADE
        );
        """)
        conn.commit()

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def increase_current_savings(savings_id, profile_id, amount) -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE savings
        SET current_savings_amount = current_savings_amount + ?
        WHERE savings.id = ? AND savings.profile_id = ?
        """, (amount, savings_id, profile_id))

        rows_updated = cursor.rowcount
        conn.commit()
        return rows_updated

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_savings_contribution(savings_id, contribution_id) -> float:
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT contribution_amount
            FROM savings_contributions
            WHERE savings_contributions.savings_id = ? AND savings_contributions.id = ?
        """, (savings_id, contribution_id))

        row = cursor.fetchone()

        if row is None:
            return 0

        total = row[0]
        return total
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_total_savings_contribution(savings_id) -> float:
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT COALESCE(SUM(contribution_amount), 0)
        FROM savings_contributions
        WHERE savings_contributions.savings_id = ?
        """, (savings_id,))

        total = cursor.fetchone()[0]
        return total
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def record_savings_contribution(profile_id, savings_id, contribution_amount, contribution_date) -> int:
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT planned_savings_amount
        FROM savings
        WHERE savings.profile_id = ? AND savings.id = ?
        """, (profile_id, savings_id))

        amt = cursor.fetchone()

        if amt is None:
            return 0

        if contribution_amount <= 0:
            return 0

        cursor.execute("""
        INSERT INTO savings_contributions(savings_id,contribution_amount,contribution_date) VALUES (?, ?, ?)
        """, (savings_id, contribution_amount, contribution_date))

        cursor.execute("""
        UPDATE savings
        SET current_savings_amount = current_savings_amount + ?
        WHERE savings.id = ? AND savings.profile_id = ?
        """, (contribution_amount, savings_id, profile_id))

        rows_updated = cursor.rowcount
        conn.commit()
        return rows_updated

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
