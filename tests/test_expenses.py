"""Tests de l'interface principale."""

from expenses import Expenses


def test_add_expense() -> None:
    """Test l'ajout d'une dépense."""
    expenses = Expenses()
    expenses.append(
        2000,
        who_paid="Rémi",
        who_for=["Rémi", "Thomas"],
        description="Gite",
        when="2025-01-01",
        label="logement",
    )
    assert len(expenses) == 1
