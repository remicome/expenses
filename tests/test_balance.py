from expenses.balance import balance
from expenses.definitions import Member, Transaction


def test_balance():
    """Compute a simple balance."""
    first = Member(name="first")
    second = Member(name="second")
    transactions = [
        Transaction(
            value=100,
            payer=first,
            members=[first, second],
        )
    ]
    balances = balance(transactions)
    assert balances[first] == 50 and balances[second] == -50


def test_weighted_balance():
    """Compute a simple balance."""
    first = Member(name="first")
    second = Member(name="second")
    transactions = [
        Transaction(
            value=100,
            payer=first,
            members=[first, second],
            weights={first: 3, second: 1},
        )
    ]
    balances = balance(transactions)
    assert balances[first] == 25 and balances[second] == -25


def test_sum_of_balances(transactions):
    """The balance sum should be zero."""
    balances = balance(transactions)
    summed_balance = sum(balances.values())
    assert round(summed_balance, 2) == 0
