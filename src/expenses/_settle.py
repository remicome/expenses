from __future__ import annotations

import dataclasses
import typing

from ._expense import Expense


def settle(expenses: typing.List[Expense]) -> typing.List[Paiement]:
    """Settle a set of expense by issuing a list of paiements to be made.

    This is the algorithm used by splittypie: the person with the lowest balance pays
    all it cans to the one with the highest balance, until we reach equilibrium.
    """
    paiements = []
    debts = _individual_debts(expenses)

    while _exists_positive(debts) and _exists_negative(debts):
        member_with_lowest_balance = min(debts, key=lambda k: debts[k])
        member_with_highest_balance = max(debts, key=lambda k: debts[k])

        lowest_balance = debts[member_with_lowest_balance]
        highest_balance = debts[member_with_highest_balance]
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
        debts[member_with_lowest_balance] += paiement_value
        debts[member_with_highest_balance] -= paiement_value

    return paiements


def _individual_debts(expenses: list[Expense]) -> dict[str, float]:
    """
    Calcule la dette de chaque membre envers le groupe.

    La dette d'un membre est l'ensemble des dépenses engagées en son nom (à l'actif du
    groupe), auquel on soustrait l'argent effectivement déboursé par ce membre (au
    passif du groupe). L'actif étant égal au passif, la somme des dette doit être de
    zéro.

    Exemple:
        Alice paie 100€ pour le groupe constitué d'Alice et Bob. Bob paie 50€ pour Alice
        et Bob. Alors :

            * Le groupe a engagé 75€ de dépense pour chacun de ses membres.
            * La dette de Bob est de 25€ (100€ - 25€).
            * La dette d'Alice est de -25€ (75€ - 100€).
    """
    balances: typing.Dict[str, float] = {}

    for expense in expenses:
        balances[expense.who_paid] = balances.get(expense.who_paid, 0) + expense.amount

        for member in expense.who_for:
            # La somme engagée est divisée équitablement entre les membres impliqués
            debt = expense.amount / len(expense.who_for)
            balances[member] = balances.get(member, 0) - debt

    return balances


@dataclasses.dataclass(repr=False)
class Paiement:
    """A paiement to be issued.

    Args:
        * sender: issuer of the paiement
        * recipient: recipient of the paiement
        * value: currency value of the paiement
    """

    sender: str
    recipient: str
    value: float

    def __repr__(self) -> str:
        return f"{self.sender} owes {self.value:.2f} to {self.recipient}."


def _exists_positive(balances: typing.Mapping) -> bool:
    return any(value > 0 for value in balances.values())


def _exists_negative(balances: typing.Mapping) -> bool:
    return any(value < 0 for value in balances.values())
