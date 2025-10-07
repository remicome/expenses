"""Test le bilan comptable."""

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
