"""Calcul des virements nécessaires au rééquilibrage."""

import enum

import pandas as pd

from ._statement import compute_statement
from .expense import Expense


class _Transfer(enum.StrEnum):
    """Variables descriptives d'un virement."""

    origin = "émetteur"
    destination = "destinataire"
    amount = "montant"


def settle(expenses: list[Expense], weights: dict | None = None) -> pd.DataFrame:
    """
    Détermine les transferts à effectuer pour équilibrer une liste de dépenses.

    L'algorithme utilisé est celui de Splittypie : la personne ayant la dette la plus
    grande envers le groupe paie celle qui a la créance la plus élevée, et ainsi de
    suite jusqu'à ce que toutes les dettes soient soldées.

    Args:
        expenses: une liste de dépenses engagées par le groupe.
        weights: un dictionnaire optionnel de poids. Celui-ci est au format

            {label: {membre1: poids1, membre1: poids1,...}, ...}

    Returns:
        Un DataFrame décrivant l'ensemble des virements à réaliser pour assurer
        l'équilibre.
    """
    if len(expenses) == 0:
        return pd.DataFrame(columns=list(_Transfer))

    transfers = []
    statements = individual_statements(expenses, weights=weights)

    while _exists_positive(statements) and _exists_negative(statements):
        member_with_lowest_balance = min(statements, key=lambda k: statements[k])
        member_with_highest_balance = max(statements, key=lambda k: statements[k])

        transfer_amount = _largest_possible_transfer(
            origin=statements[member_with_lowest_balance],
            destination=statements[member_with_highest_balance],
        )

        transfers.append(
            {
                _Transfer.origin: member_with_lowest_balance,
                _Transfer.destination: member_with_highest_balance,
                _Transfer.amount: transfer_amount,
            }
        )
        statements[member_with_lowest_balance] += transfer_amount
        statements[member_with_highest_balance] -= transfer_amount

    return pd.DataFrame(transfers)


def individual_statements(
    expenses: list[Expense],
    weights: dict | None = None,
) -> dict[str, float]:
    """
    Calcule le bilan de chaque membre.

    Le bilan d'un membre est l'argent dépensé par un membre du groupe (au passif du
    groupe), auquel on soustrait l'ensemble des dépenses engagées en son nom (à l'actif
    du groupe) L'actif étant égal au passif, la somme des bilans doit être de zéro.

    Exemple:
        Alice paie 100€ pour le groupe constitué d'Alice et Bob. Bob paie 50€ pour Alice
        et Bob. Alors :

            * Le groupe a engagé 75€ de dépense pour chacun de ses membres.
            * Le bilan d'Alice est de 25€ (100€ - 75€)
            * Le bilan de Bob est de -25€ (50€ - 75€).

    Args:
        expenses: une liste de dépenses engagées par le groupe.
        weights: un dictionnaire optionnel de poids à affecter aux dépenses d'un certain
            type. Celui-ci est au format

            {label: {membre1: poids1, membre1: poids1,...}, ...}
            * La dette d'Alice est de -25€ (75€ - 100€).

    Returns:
        Un dictionnaire donnant la dette pour chaque membre du groupe.
    """
    complete_statement = compute_statement(expenses, weights=weights)
    return complete_statement["bilan"].to_dict()


def _weights_for_label(expense: Expense, weights: dict) -> dict:
    """Retourne les poids associés à une dépense de ce type."""
    default_weights = {member: 1 for member in expense.who_for}
    return weights.get(expense.label, default_weights)


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
