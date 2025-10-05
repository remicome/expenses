import typing

from ._member import Member
from ._transaction import Transaction


def balance(transactions: typing.List[Transaction]) -> typing.Mapping[Member, float]:
    """Compute each member's balance."""
    balances: typing.Dict[Member, float] = {}

    for transaction in transactions:
        balances[transaction.payer] = (
            balances.get(transaction.payer, 0) + transaction.value
        )
        total_transaction_weight = sum(
            transaction.weights.get(member, 1) for member in transaction.members
        )

        for member in transaction.members:
            debt_ratio = transaction.weights.get(member, 1) / total_transaction_weight
            debt = transaction.value * debt_ratio
            balances[member] = balances.get(member, 0) - debt

    return balances
