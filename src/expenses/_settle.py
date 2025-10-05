"""Calcul des virements nécessaires au rééquilibrage."""

import enum

import pandas as pd

from ._expense import Expense


class _Transfer(enum.StrEnum):
    """Variables descriptives d'un virement."""

    origin = "émetteur"
    destination = "destinataire"
    amount = "montant"


def settle(expenses: list[Expense]) -> pd.DataFrame:
    """
    Détermine les transferts à effectuer pour équilibrer une liste de dépenses.

    L'algorithme utilisé est celui de Splittypie : la personne ayant la dette la plus
    grande envers le groupe paie celle qui a la créance la plus élevée, et ainsi de
    suite jusqu'à ce que toutes les dettes soient soldées.

    Args:
        expenses: une liste de dépenses engagées par le groupe.

    Returns:
        Un DataFrame décrivant l'ensemble des virements à réaliser pour assurer
        l'équilibre.
    """
    if len(expenses) == 0:
        return pd.DataFrame(columns=list(_Transfer))

    transfers = []
    debts = _individual_debts(expenses)

    while _exists_positive(debts) and _exists_negative(debts):
        member_with_lowest_balance = min(debts, key=lambda k: debts[k])
        member_with_highest_balance = max(debts, key=lambda k: debts[k])

        transfer_amount = _largest_possible_transfer(
            origin=debts[member_with_lowest_balance],
            destination=debts[member_with_highest_balance],
        )

        transfers.append(
            {
                _Transfer.origin: member_with_lowest_balance,
                _Transfer.destination: member_with_highest_balance,
                _Transfer.amount: transfer_amount,
            }
        )
        debts[member_with_lowest_balance] += transfer_amount
        debts[member_with_highest_balance] -= transfer_amount

    return pd.DataFrame(transfers)


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
    balances: str[str, float] = {}

    for expense in expenses:
        balances[expense.who_paid] = balances.get(expense.who_paid, 0) + expense.amount

        for member in expense.who_for:
            # La somme engagée est divisée équitablement entre les membres impliqués
            debt = expense.amount / len(expense.who_for)
            balances[member] = balances.get(member, 0) - debt

    return balances


def _largest_possible_transfer(origin: float, destination: float) -> float:
    """
    Calcule le montant du plus grand transfert possible entre deux personnes.

    ``origin`` représente une dette (de signe négatif), ``destination`` une créance
    (de signe positif). Le montant calculé est le plus grand possible qui puisse
    être payé par la personne endetté, sans dépassé le montant que doit recevoir le
    détenteur de la créance.
    """
    return min(-origin, destination)


def _exists_positive(mapping: dict) -> bool:
    """Retourne True si le dictionnaire contient une valeur positive."""
    return any(value > 0 for value in mapping.values())


def _exists_negative(mapping: dict) -> bool:
    """Retourne True si le dictionnaire contient une valeur négative."""
    return any(value < 0 for value in mapping.values())
