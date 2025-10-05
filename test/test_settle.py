import random

from expenses.balance import balance
from expenses.definitions import Member, Transaction
from expenses.settle import settle


def test_simple_settlement():
    """Settle a single transaction."""
    members = [
        Member(name="first"),
        Member(name="second"),
    ]
    transactions = [
        Transaction(
            value=100,
            payer=members[0],
            members=members,
        )
    ]
    paiements = settle(transactions)
    assert (
        len(paiements) == 1
        and paiements[0].sender.name == members[1].name
        and paiements[0].recipient.name == members[0].name
    )


def test_sum_of_paiements(transactions):
    """
    The sum of all paiement values should equal the positive balance, up to the
    algorithm's precision.
    """
    paiements = settle(transactions)
    balances = balance(transactions)

    total_paiement_value = sum(paiement.value for paiement in paiements)
    positive_balance_values = (value for value in balances.values() if value > 0)
    precision = 0.02
    assert abs(total_paiement_value - sum(positive_balance_values)) < precision
