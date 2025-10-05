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


def test_members() -> None:
    """
    Teste la liste des membres.

    La liste des membres doit coïncider avec celle définie par les dépenses.
    """
    expenses = Expenses()
    members = ["Rémi", "Sophie", "François"]
    expenses.append(
        2000,
        who_paid=members[0],
        who_for=members[1:],
    )
    assert set(expenses.members) == set(members)


def test_settlement() -> None:
    """
    Teste l'interface du rééquilibrage des dépenses.

    La fonction settle doit retourner un DataFrame avec trois colonnes : "émetteur",
    "destinataire", "montant".
    """
    expenses = Expenses()
    expenses.append(
        10,
        who_paid="Rémi",
        who_for=["Sophie", "François"],
    )
    settlement = expenses.settle()

    assert len(settlement) > 0

    expected_columns = {"émetteur", "destinataire", "montant"}
    assert set(settlement.columns) == set(expected_columns)
