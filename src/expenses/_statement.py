"""Calcul du bilan comptable."""

import enum

import pandas as pd

from .expense import Expense


def compute_statement(
    expenses: list[Expense],
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
        expenses: une liste de dépenses.
        weights: un dictionnaire optionnel de poids à affecter aux dépenses d'un certain
            type. Celui-ci est au format

            {label: {membre1: poids1, membre1: poids1,...}, ...}
            * La dette d'Alice est de -25€ (75€ - 100€).

    Returns:
        Un DataFrame représentant le bilan.
    """

    paiements = {}
    debts = {}

    for expense in expenses:
        paiements[expense.who_paid] = (
            paiements.get(expense.who_paid, 0) + expense.amount
        )

        expense_weights = _weights_for_label(expense, weights=weights)
        total_weight = sum(expense_weights.values(), start=0)
        for member in expense.who_for:
            # La somme engagée est divisée équitablement entre les membres impliqués
            debt = expense.amount * expense_weights.get(member, 0) / total_weight
            debts[member] = debts.get(member, 0) + debt

    statement = pd.DataFrame(
        {
            _Statement.paid: pd.Series(paiements),
            _Statement.expenses: pd.Series(debts),
        }
    )

    labels = {expense.label for expense in expenses}
    for label in labels:
        statement[f"{_Statement.expenses} {label}"] = 0

    statement[_Statement.total] = 0
    return statement


class _Statement(enum.StrEnum):
    """Colonnes du bilan."""

    paid = "a payé"
    expenses = "dépenses"
    total = "bilan"


def _weights_for_label(expense: Expense, weights: dict | None) -> dict:
    """Retourne les poids associés à une dépense de ce type."""
    default_weights = {member: 1 for member in expense.who_for}

    if not weights:
        return default_weights

    return weights.get(expense.label, default_weights)
