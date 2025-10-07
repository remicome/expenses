"""Calcul du bilan comptable."""

import enum

import pandas as pd

from .expense import Expense


def compute_statement(
    expense_list: list[Expense],
    weights: dict | None = None,
) -> pd.DataFrame:
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
        expense_list: une liste de dépenses.
        weights: un dictionnaire optionnel de poids à affecter aux dépenses d'un certain
            type. Celui-ci est au format

            {label: {membre1: poids1, membre1: poids1,...}, ...}
            * La dette d'Alice est de -25€ (75€ - 100€).

    Returns:
        Un DataFrame représentant le bilan.
    """
    members = set.union(
        *({expense.who_paid} | set(expense.who_for) for expense in expense_list)
    )
    labels = {expense.label for expense in expense_list}
    return pd.DataFrame(
        columns=list(_Statement)
        + [f"{_Statement.expenses} {label}" for label in labels],
        index=list(members),
    )


class _Statement(enum.StrEnum):
    paid = "a payé"
    expenses = "dépenses"
    total = "bilan"
