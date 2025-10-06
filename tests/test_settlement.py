"""Teste le calcul du rééquilibrage."""

from expenses._settle import settle
from expenses.expense import Expense


def test_format(expense_list: list[Expense]) -> None:
    """
    Teste le format de sortie.

    La fonction de rééquilibrage retourne un DataFrame avec trois colonnes décrivant les
    virements : "émetteur", "destinataire", "montant" (dans cet ordre).
    """
    settlement = settle(expense_list)
    assert len(settlement) > 0

    expected_columns = ["émetteur", "destinataire", "montant"]
    assert list(settlement.columns) == expected_columns


def test_empty_list() -> None:
    """
    Teste le rééquilibrage d'une liste vide.

    Le rééquilibrage d'une liste vide doit retourner un DataFrame vide.
    """
    expenses: list[Expense] = []
    settlement = settle(expenses)
    assert len(settlement) == 0


def test_positive_amounts(expense_list: list[Expense]) -> None:
    """Teste que le montant de chaque virement est positif."""
    transfers = settle(expense_list)
    is_positive = transfers["montant"] > 0
    assert is_positive.all()


def test_simple_settlement() -> None:
    """
    Vérifie le calcul sur un exemple simple.

    Ici Rémi engage 100€ au nom de François et lui-même. Le groupe a donc engagé 50€
    pour chaque membre : Rémi est en excédent de 50€ et François en déficit de 50€.

    Le rééquilibrage doit donc constituer en un unique virement de François à Rémi.
    """
    remi = "Rémi"
    francois = "François"

    expenses = [
        Expense(
            amount=100,
            who_paid=remi,
            who_for=[remi, francois],
        )
    ]
    transfers = settle(expenses)
    assert len(transfers) == 1

    transfer = transfers.iloc[0].to_dict()
    assert transfer == {
        "émetteur": francois,
        "destinataire": remi,
        "montant": 50,
    }


def test_weighted_settlement() -> None:
    """
    Vérifie un calcul simple avec des poids.

    Rémi engage 100€ au nom de François et lui-même, sur une dépense à répartir sous la
    forme 75% - 25%. François doit donc 25€ au groupe, tandis que Rémi est en excédent
    de 25€.

    Le rééquilibrage doit donc constituer en un unique virement de François à Rémi.
    """
    remi = "Rémi"
    francois = "François"
    label = "logement"

    expenses = [
        Expense(
            amount=100,
            who_paid=remi,
            who_for=[remi, francois],
            label=label,
        )
    ]
    weights = {label: {remi: 75, francois: 25}}
    transfers = settle(expenses, weights=weights)
    assert len(transfers) == 1

    transfer = transfers.iloc[0].to_dict()
    assert transfer == {
        "émetteur": francois,
        "destinataire": remi,
        "montant": 25,
    }
