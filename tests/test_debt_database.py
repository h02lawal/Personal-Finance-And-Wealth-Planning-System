
import pytest
import sqlite3

import src.database as database


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    # Create a temporary SQLite database path
    test_database_path = tmp_path / "test_finance.db"

    # Redirect database connections to the test database
    monkeypatch.setattr(
        database,
        "DB_NAME",
        str(test_database_path)
    )

    # Create the required tables
    database.create_tables()
    database.create_debts_table()
    database.create_debt_payment_history()

    return database


@pytest.fixture
def sample_debt(test_db):
    profile_id = test_db.create_financial_profile()

    debt_id = test_db.insert_debt(
        profile_id=profile_id,
        debt_name="Test Credit Card",
        debt_type="Credit Card",
        debt_balance=1000,
        annual_interest_rate=12,
        monthly_payment=100
    )

    return profile_id, debt_id

##################################################################################################


def test_create_profile(test_db):
    profile_id = test_db.create_financial_profile()

    assert isinstance(profile_id, int)
    assert profile_id > 0

    profile = test_db.get_financial_profile(profile_id)

    assert profile is not None
    assert profile["id"] == profile_id


def test_insert_debt(sample_debt, test_db):
    profile_id, debt_id = sample_debt

    debts = test_db.get_depts_by_profile(profile_id)

    assert len(debts) == 1
    assert debts[0]["id"] == debt_id
    assert debts[0]["debt_balance"] == pytest.approx(1000)


def test_record_debt_payment(sample_debt, test_db):
    profile_id, debt_id = sample_debt

    result = test_db.record_debt_payment(
        profile_id, debt_id, 200, "2026-11-16"
    )

    assert result == 1

    debt = test_db.get_debt(profile_id, debt_id)[0]

    assert debt["debt_balance"] == pytest.approx(800)

    payments = test_db.get_debt_payments(debt_id)

    assert len(payments) == 1
    assert payments[0]["payment_amount"] == pytest.approx(200)
    assert payments[0]["payment_date"] == "2026-11-16"


def test_reject_excessive_payment(sample_debt, test_db):
    profile_id, debt_id = sample_debt

    result = test_db.record_debt_payment(
        profile_id, debt_id, 1500, "2026-11-16"
    )

    assert result == 0

    debt = test_db.get_debt(profile_id, debt_id)[0]

    assert debt["debt_balance"] == pytest.approx(1000)
    assert test_db.get_debt_payments(debt_id) == []


def test_profile_isolation(sample_debt, test_db):
    profile_id, debt_id = sample_debt

    other_profile_id = test_db.create_financial_profile()

    result = test_db.record_debt_payment(
        other_profile_id, debt_id, 200, "2026-11-16"
    )

    assert result == 0

    debt = test_db.get_debt(profile_id, debt_id)[0]

    assert debt["debt_balance"] == pytest.approx(1000)
    assert test_db.get_debt_payments(debt_id) == []


def test_delete_debt_and_payment_history(sample_debt, test_db):
    profile_id, debt_id = sample_debt

    test_db.record_debt_payment(
        profile_id, debt_id, 200, "2026-11-16"
    )

    result = test_db.delete_debt(profile_id, debt_id)

    assert result == 1
    assert test_db.get_debt(profile_id, debt_id) == []
    assert test_db.get_debt_payments(debt_id) == []


def test_full_debt_payoff(sample_debt, test_db):
    profile_id, debt_id = sample_debt

    result = test_db.record_debt_payment(
        profile_id, debt_id, 1000, "2026-11-16"
    )

    assert result == 1

    # Fully paid debts are excluded from get_debt()
    assert test_db.get_debt(profile_id, debt_id) == []

    # Verify the actual stored balance
    conn = test_db.get_connection()

    try:
        row = conn.execute(
            "SELECT debt_balance FROM debts WHERE id = ?",
            (debt_id,)
        ).fetchone()

        assert row is not None
        assert row["debt_balance"] == pytest.approx(0)
    finally:
        conn.close()


def test_update_debt(sample_debt, test_db):
    profile_id, debt_id = sample_debt

    result = test_db.update_debt(
        profile_id=profile_id,
        debt_id=debt_id,
        debt_type="Credit Card",
        debt_name="Updated Credit Card",
        debt_balance=750,
        annual_interest_rate=15,
        monthly_payment=150,
        credit_limit=3000,
        minimum_payment=50
    )

    assert result == 1

    debt = test_db.get_debt(profile_id, debt_id)[0]

    assert debt["debt_name"] == "Updated Credit Card"
    assert debt["debt_balance"] == pytest.approx(750)
    assert debt["annual_interest_rate"] == pytest.approx(15)
    assert debt["monthly_payment"] == pytest.approx(150)
    assert debt["credit_limit"] == pytest.approx(3000)
    assert debt["minimum_payment"] == pytest.approx(50)


def test_update_debt_wrong_profile(sample_debt, test_db):
    profile_id, debt_id = sample_debt

    other_profile_id = test_db.create_financial_profile()

    result = test_db.update_debt(
        profile_id=other_profile_id,
        debt_id=debt_id,
        debt_type="Credit Card",
        debt_name="Unauthorized Update",
        debt_balance=100,
        annual_interest_rate=0,
        monthly_payment=50
    )

    assert result == 0

    debt = test_db.get_debt(profile_id, debt_id)[0]

    assert debt["debt_name"] == "Test Credit Card"
    assert debt["debt_balance"] == pytest.approx(1000)


@pytest.mark.parametrize("payment_amount", [
    0,
    -50,
    -1000
])
def test_invalid_payment_amount(
    sample_debt, test_db, payment_amount
):
    profile_id, debt_id = sample_debt

    result = test_db.record_debt_payment(
        profile_id,
        debt_id,
        payment_amount,
        "2026-11-16"
    )

    assert result == 0

    debt = test_db.get_debt(profile_id, debt_id)[0]

    assert debt["debt_balance"] == pytest.approx(1000)
    assert test_db.get_debt_payments(debt_id) == []


def test_payment_transaction_rollback(sample_debt, test_db):
    profile_id, debt_id = sample_debt

    with pytest.raises(sqlite3.IntegrityError):
        test_db.record_debt_payment(
            profile_id,
            debt_id,
            200,
            None
        )

    debt = test_db.get_debt(profile_id, debt_id)[0]

    assert debt["debt_balance"] == pytest.approx(1000)
    assert test_db.get_debt_payments(debt_id) == []
