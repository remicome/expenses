"""Teste le calcul du rééquilibrage."""

from expenses._expense import Expense
from expenses._settle import settle


def test_format(expenses: list[Expense]) -> None:
    """
    Teste le format de sortie.

    La fonction de rééquilibrage retourne un DataFrame avec trois colonnes décrivant les
    virements : "émetteur", "destinataire", "montant" (dans cet ordre).
    """
    settlement = settle(expenses)
    assert len(settlement) > 0

    expected_columns = ["émetteur", "destinataire", "montant"]
    assert list(settlement.columns) == expected_columns


def test_empty_list() -> None:
    """
    Teste le rééquilibrage d'une liste vide.

    Le rééquilibrage d'une liste vide doit retourner un DataFrame vide.
    """
    expenses = []
    settlement = settle(expenses)
    assert len(settlement) == 0
