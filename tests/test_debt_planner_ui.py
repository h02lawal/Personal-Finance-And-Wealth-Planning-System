
import pytest
from pathlib import Path
from streamlit.testing.v1 import AppTest

import src.database as database


PAGE_PATH = (
    Path(__file__).resolve().parents[1]
    / "pages"
    / "2_Debt_Planner.py"
)


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test_finance.db"

    monkeypatch.setattr(database, "DB_NAME", str(db_path))

    database.create_tables()
    database.create_debts_table()
    database.create_debt_payment_history()

    return database


@pytest.fixture
def debt_app(test_db):
    profile_id = test_db.create_financial_profile()

    app = AppTest.from_file(str(PAGE_PATH))
    app.session_state["profile_id"] = profile_id
    app.run(timeout=15)

    assert not app.exception

    return app, profile_id


def test_debt_planner_loads(debt_app):
    app, profile_id = debt_app

    assert not app.exception
    assert any(
        "Debt Planner" in title.value
        for title in app.title
    )

    assert len(app.text_input) > 0
    assert len(app.number_input) > 0

########################################################################################



def test_save_debt(debt_app, test_db):
    app, profile_id = debt_app

    # Enter debt details
    app.text_input[0].set_value("Test Credit Card")

    app.number_input[0].set_value(1000.0)
    app.number_input[1].set_value(19.99)
    app.number_input[2].set_value(100.0)

    # Apply the input changes
    app.run(timeout=15)

    # Save the debt
    app.button[0].click().run(timeout=15)

    # Check for Streamlit exceptions
    assert not app.exception

    # Verify the debt was saved in SQLite
    debts = test_db.get_depts_by_profile(profile_id)

    assert len(debts) == 1
    assert debts[0]["debt_name"] == "Test Credit Card"
    assert debts[0]["debt_balance"] == pytest.approx(1000.0)


def test_delete_debt(debt_app, test_db):
    app, profile_id = debt_app

    # Create a debt directly in the test database
    debt_id = test_db.insert_debt(
        profile_id=profile_id,
        debt_name="Test Personal Loan",
        debt_type="Personal Loan",
        debt_balance=2000,
        annual_interest_rate=10,
        monthly_payment=150
    )

    # Reload the page so the saved debt appears
    app.run(timeout=15)

    # Verify the debt exists
    debts = test_db.get_depts_by_profile(profile_id)
    assert len(debts) == 1

    # Click the Delete Debt button
    app.button[0].click().run(timeout=15)

    # Verify no Streamlit exceptions occurred
    assert not app.exception

    # Verify the debt was deleted from SQLite
    debts = test_db.get_depts_by_profile(profile_id)
    assert len(debts) == 0


def test_record_debt_payment(debt_app, test_db):
    app, profile_id = debt_app

    # Create a debt with a $1,000 balance
    debt_id = test_db.insert_debt(
        profile_id=profile_id,
        debt_name="Test Credit Card",
        debt_type="Credit Card",
        debt_balance=1000,
        annual_interest_rate=19.99,
        monthly_payment=100
    )

    # Reload the Streamlit page
    app.run(timeout=15)

    # Find and click the Record Payment button
    payment_button = next(
        button for button in app.button
        if button.label == "Record Payment"
    )

    payment_button.click().run(timeout=15)

    # Enter a payment of $250
    payment_input = next(
        widget for widget in app.number_input
        if widget.label == "Enter the amount you'll like to pay"
    )

    payment_input.set_value(250.0)
    app.run(timeout=15)

    # Submit the payment
    submit_button = next(
        button for button in app.button
        if button.label == "Submit Payment"
    )

    submit_button.click().run(timeout=15)

    assert not app.exception

    # Check the remaining balance
    debts = test_db.get_depts_by_profile(profile_id)

    assert len(debts) == 1
    assert debts[0]["debt_balance"] == pytest.approx(750.0)

    # Check payment history
    payments = test_db.get_debt_payments(debt_id)

    assert len(payments) == 1
    assert payments[0]["payment_amount"] == pytest.approx(250.0)


def test_edit_debt(debt_app, test_db):
    app, profile_id = debt_app

    debt_id = test_db.insert_debt(
        profile_id=profile_id,
        debt_name="Original Loan",
        debt_type="Personal Loan",
        debt_balance=2000,
        annual_interest_rate=10,
        monthly_payment=150
    )

    # Display the saved debt
    app.run(timeout=15)

    # Open the editing interface
    edit_button = next(
        button for button in app.button
        if button.label == "Edit Debt"
    )

    edit_button.click().run(timeout=15)

    # Update the debt information
    for widget in app.text_input:
        if widget.label == "Enter new debt name":
            widget.set_value("Updated Loan")

    for widget in app.number_input:
        if widget.label == "Enter new debt balance":
            widget.set_value(1500.0)
        elif widget.label == "Enter new interest rate":
            widget.set_value(8.0)
        elif widget.label == "Enter new monthly payment":
            widget.set_value(200.0)

    app.run(timeout=15)

    # Save the changes
    save_button = next(
        button for button in app.button
        if button.label == "Save Changes"
    )

    save_button.click().run(timeout=15)

    assert not app.exception

    # Verify the database was updated
    debts = test_db.get_depts_by_profile(profile_id)

    assert len(debts) == 1
    assert debts[0]["id"] == debt_id
    assert debts[0]["debt_name"] == "Updated Loan"
    assert debts[0]["debt_balance"] == pytest.approx(1500.0)
    assert debts[0]["annual_interest_rate"] == pytest.approx(8.0)
    assert debts[0]["monthly_payment"] == pytest.approx(200.0)


def test_view_payment_history(debt_app, test_db):
    app, profile_id = debt_app

    debt_id = test_db.insert_debt(
        profile_id=profile_id,
        debt_name="History Test Loan",
        debt_type="Personal Loan",
        debt_balance=1000,
        annual_interest_rate=10,
        monthly_payment=100
    )

    # Record a payment directly in the test database
    result = test_db.record_debt_payment(
        profile_id,
        debt_id,
        250.0,
        "2026-11-16"
    )

    assert result == 1

    # Reload the page
    app.run(timeout=15)

    # Open payment history
    history_button = next(
        button for button in app.button
        if button.label == "Payment History"
    )

    history_button.click().run(timeout=15)

    assert not app.exception

    # Verify the total paid metric
    assert any(
        metric.label == "Total Debt Paid is "
        and metric.value == "$250.00"
        for metric in app.metric
    )

    # Verify the payment is displayed
    assert any(
        "$250.00" in element.value
        and "2026-11-16" in element.value
        for element in app.markdown
    )


def test_strategy_comparison(debt_app, test_db):
    app, profile_id = debt_app

    test_db.insert_debt(
        profile_id=profile_id,
        debt_name="Credit Card",
        debt_type="Credit Card",
        debt_balance=3000,
        annual_interest_rate=24,
        monthly_payment=150
    )

    test_db.insert_debt(
        profile_id=profile_id,
        debt_name="Personal Loan",
        debt_type="Personal Loan",
        debt_balance=1000,
        annual_interest_rate=8,
        monthly_payment=100
    )

    app.run(timeout=15)

    comparison_button = next(
        button for button in app.button
        if button.label == "Strategy Comparison"
    )

    comparison_button.click().run(timeout=15)

    assert not app.exception

    # Verify that the comparison results are displayed
    comparison_labels = [
        metric.label for metric in app.metric
    ]

    assert any(
        label in comparison_labels
        for label in [
            "Interest Savings with Avalanche",
            "Interest Savings with Snowball",
            "Interest Difference"
        ]
    )

    assert any(
        label in comparison_labels
        for label in [
            "Months Saved with Avalanche",
            "Months Saved with Snowball",
            "Duration Difference"
        ]
    )
