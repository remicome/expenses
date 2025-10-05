from __future__ import annotations

import dataclasses
import typing

from ._member import Member
from ._transaction import Transaction
from .balance import balance


def settle(transactions: typing.List[Transaction]) -> typing.List[Paiement]:
    """Settle a set of transaction by issuing a list of paiements to be made.

    This is the algorithm used by splittypie: the person with the lowest balance pays
    all it cans to the one with the highest balance, until we reach equilibrium.
    """
    paiements = []
    balances = balance(transactions)

    while _exists_positive(balances) and _exists_negative(balances):
        member_with_lowest_balance = min(balances, key=lambda k: balances[k])
        member_with_highest_balance = max(balances, key=lambda k: balances[k])

        lowest_balance = balances[member_with_lowest_balance]
        highest_balance = balances[member_with_highest_balance]
        if lowest_balance > 0 or highest_balance < 0:
            raise RuntimeError

        paiement_value = min(-lowest_balance, highest_balance)

        paiements.append(
            Paiement(
                sender=member_with_lowest_balance,
                recipient=member_with_highest_balance,
                value=paiement_value,
            )
        )
        balances[member_with_lowest_balance] += paiement_value
        balances[member_with_highest_balance] -= paiement_value

    return paiements


@dataclasses.dataclass(repr=False)
class Paiement:
    """A paiement to be issued.

    Args:
        * sender: issuer of the paiement
        * recipient: recipient of the paiement
        * value: currency value of the paiement
    """

    sender: Member
    recipient: Member
    value: float

    def __repr__(self) -> str:
        return f"{self.sender.name} owes {self.value:.2f} to {self.recipient.name}."


def _exists_positive(balances: typing.Mapping) -> bool:
    return any(value > 0 for value in balances.values())


def _exists_negative(balances: typing.Mapping) -> bool:
    return any(value < 0 for value in balances.values())
