"""Test le bilan comptable."""

import pandas as pd
import pytest

from expenses._statement import compute_statement
from expenses.expense import Expense


def test_format(expense_list: list[Expense], weights: dict) -> None:
    """
    Teste le format du bilan.

    Celui-ci comporte une ligne par membre du groupe, ainsi que les colonnes suivantes :
    "a payé", "dépenses", "bilan", ainsi qu'une colonne "dépense <label>" par étiquette.
    """
    statement = compute_statement(expense_list, weights=weights)

    labels = {expense.label for expense in expense_list}
    expected_columns = {"a payé", "dépenses", "bilan"} | {
        f"dépenses {label}" for label in labels
    }
    assert set(statement.columns) == expected_columns

    members = set.union(
        *({expense.who_paid} | set(expense.who_for) for expense in expense_list)
    )
    assert set(statement.index) == members


def test_a_paye(expense_list: list[Expense], weights: dict) -> None:
    """
    Teste la cohérence de la colonne 'a payé'.

    La somme des paiement doit être égale à la somme des dépenses engagées.
    """
    total_expense = sum(expense.amount for expense in expense_list)
    statement = compute_statement(expense_list, weights=weights)

    assert statement["a payé"].sum() == total_expense


def test_depenses(expense_list: list[Expense], weights: dict) -> None:
    """
    Teste la cohérence de la colonne de dépenses.

    La somme des dépenses doit être égale à la somme des dépenses engagées.
    """
    total_expense = sum(expense.amount for expense in expense_list)
    statement = compute_statement(expense_list, weights=weights)

    assert statement["dépenses"].sum() == total_expense


def test_bilan(expense_list: list[Expense], weights: dict) -> None:
    """
    Teste la cohérence de la colonne de bilan.

    Le bilan est la différence des paiements et des dépenses engagées.
    """
    statement = compute_statement(expense_list, weights=weights)
    is_equal = statement["bilan"] == statement["a payé"] - statement["dépenses"]
    assert is_equal.all()


@pytest.fixture
def weights(weights: pd.DataFrame) -> dict:
    """Convertis le DataFrame de poids en dict."""
    return weights.set_index("membre").to_dict()
