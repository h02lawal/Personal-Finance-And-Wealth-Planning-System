
import pytest

from src.calculations import calculate_one_month_debt
from src.calculations import highest_interest, lowest_balance
import src.calculations as calculations


def test_normal_monthly_payment():
    balance, interest, excess = calculate_one_month_debt(
        1000, 12, 200
    )

    assert balance == pytest.approx(810.00)
    assert interest == pytest.approx(10.00)
    assert excess == pytest.approx(0)


def test_overpayment():
    balance, interest, excess = calculate_one_month_debt(
        500, 12, 600
    )

    assert balance == pytest.approx(0)
    assert interest == pytest.approx(5)
    assert excess == pytest.approx(95)


def test_zero_interest():
    balance, interest, excess = calculate_one_month_debt(
        1000, 0, 250
    )

    assert balance == pytest.approx(750)
    assert interest == pytest.approx(0)
    assert excess == pytest.approx(0)


def test_payment_below_monthly_interest():
    balance, interest, excess = calculate_one_month_debt(
        5000, 24, 50
    )

    assert balance == pytest.approx(5050)
    assert interest == pytest.approx(100)
    assert excess == pytest.approx(0)

def test_highest_interest_priority():
    debts = [
        {"id": 1, "balance": 5000, "annual_ir": 10},
        {"id": 2, "balance": 2000, "annual_ir": 24},
        {"id": 3, "balance": 1000, "annual_ir": 15}
    ]

    assert highest_interest(debts) == 2


def test_lowest_balance_priority():
    debts = [
        {"id": 1, "balance": 5000, "annual_ir": 10},
        {"id": 2, "balance": 2000, "annual_ir": 24},
        {"id": 3, "balance": 1000, "annual_ir": 15}
    ]

    assert lowest_balance(debts) == 3


def test_priority_excludes_paid_debts():
    debts = [
        {"id": 1, "balance": 0, "annual_ir": 30},
        {"id": 2, "balance": 2000, "annual_ir": 24},
        {"id": 3, "balance": 1000, "annual_ir": 15}
    ]

    assert highest_interest(debts) == 2
    assert lowest_balance(debts) == 3


def test_priority_when_all_debts_paid():
    debts = [
        {"id": 1, "balance": 0, "annual_ir": 20},
        {"id": 2, "balance": 0, "annual_ir": 15}
    ]

    assert highest_interest(debts) == 0
    assert lowest_balance(debts) == 0

#####################################################################################################


def test_single_debt_payoff(monkeypatch):
    test_debts = [
        {
            "id": 1,
            "debt_name": "Test Loan",
            "debt_balance": 1000,
            "annual_interest_rate": 0,
            "monthly_payment": 200
        }
    ]

    monkeypatch.setattr(
        calculations,
        "get_depts_by_profile",
        lambda profile_id: test_debts
    )

    result = calculations.payments_until_complete(
        profile_id=1,
        technique="snowball"
    )

    assert result["months_to_payoff"] == 5
    assert result["total_interest"] == pytest.approx(0)
    assert result["debts"][0]["duration_till_paid"] == 5
    assert result["monthly_balances"][-1]["total_balance"] == pytest.approx(0)


def test_extra_payment_reduces_payoff_time(monkeypatch):
    test_debts = [
        {
            "id": 1,
            "debt_name": "Test Loan",
            "debt_balance": 1000,
            "annual_interest_rate": 0,
            "monthly_payment": 200
        }
    ]

    monkeypatch.setattr(
        calculations,
        "get_depts_by_profile",
        lambda profile_id: test_debts
    )

    without_extra = calculations.payments_until_complete(
        1, "avalanche", 0
    )

    with_extra = calculations.payments_until_complete(
        1, "avalanche", 100
    )

    assert without_extra["months_to_payoff"] == 5
    assert with_extra["months_to_payoff"] == 4
    assert with_extra["months_to_payoff"] < without_extra["months_to_payoff"]


def test_no_debts(monkeypatch):
    monkeypatch.setattr(
        calculations,
        "get_depts_by_profile",
        lambda profile_id: []
    )

    result = calculations.payments_until_complete(
        1, "snowball"
    )

    assert result == -3

###################################################################################################


def test_payment_redistribution(monkeypatch):
    test_debts = [
        {
            "id": 1,
            "debt_name": "Debt A",
            "debt_balance": 200,
            "annual_interest_rate": 0,
            "monthly_payment": 100
        },
        {
            "id": 2,
            "debt_name": "Debt B",
            "debt_balance": 1000,
            "annual_interest_rate": 0,
            "monthly_payment": 100
        }
    ]

    monkeypatch.setattr(
        calculations,
        "get_depts_by_profile",
        lambda profile_id: test_debts
    )

    result = calculations.payments_until_complete(
        profile_id=1,
        technique="snowball"
    )

    assert result["months_to_payoff"] == 6
    assert result["total_interest"] == pytest.approx(0)

    payoff_months = {
        debt["id"]: debt["duration_till_paid"]
        for debt in result["debts"]
    }

    assert payoff_months[1] == 2
    assert payoff_months[2] == 6

    expected_balances = [
        1200, 1000, 800, 600, 400, 200, 0
    ]

    actual_balances = [
        month["total_balance"]
        for month in result["monthly_balances"]
    ]

    assert actual_balances == pytest.approx(
        expected_balances
    )

#################################################################################################


def test_snowball_vs_avalanche(monkeypatch):
    test_debts = [
        {
            "id": 1,
            "debt_name": "Personal Loan",
            "debt_balance": 1000,
            "annual_interest_rate": 5,
            "monthly_payment": 100
        },
        {
            "id": 2,
            "debt_name": "Credit Card",
            "debt_balance": 2000,
            "annual_interest_rate": 24,
            "monthly_payment": 100
        }
    ]

    monkeypatch.setattr(
        calculations,
        "get_depts_by_profile",
        lambda profile_id: test_debts
    )

    result = calculations.compare_repayment_strategies(
        profile_id=1,
        extra_monthly_payment=100
    )

    snowball = result["snowball"]
    avalanche = result["avalanche"]

    assert snowball["months_to_payoff"] == 12
    assert avalanche["months_to_payoff"] == 11

    assert snowball["total_interest"] == pytest.approx(
        322.71, abs=0.01
    )

    assert avalanche["total_interest"] == pytest.approx(
        276.60, abs=0.01
    )

    assert result["interest_saving"] == pytest.approx(
        46.11, abs=0.01
    )

    assert result["months_difference"] == 1


################################################################################################


def test_invalid_repayment_technique():
    with pytest.raises(ValueError):
        calculations.payments_until_complete(
            profile_id=1,
            technique="invalid_strategy"
        )


def test_negative_extra_payment():
    with pytest.raises(ValueError):
        calculations.payments_until_complete(
            profile_id=1,
            extra_monthly_payment=-100
        )


def test_unpayable_debt(monkeypatch):
    test_debts = [
        {
            "id": 1,
            "debt_name": "High Interest Debt",
            "debt_balance": 1000,
            "annual_interest_rate": 24,
            "monthly_payment": 10
        }
    ]

    monkeypatch.setattr(
        calculations,
        "get_depts_by_profile",
        lambda profile_id: test_debts
    )

    result = calculations.payments_until_complete(
        profile_id=1,
        technique="avalanche"
    )

    assert result == -1

