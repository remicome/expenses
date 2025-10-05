"""Teste le calcul du rééquilibrage."""

from expenses._settle import settle


def test_empty_list() -> None:
    """
    Teste le rééquilibrage d'une liste vide.

    Le rééquilibrage d'une liste vide doit retourner un DataFrame vide.
    """
    expenses = []
    settlement = settle(expenses)
    assert len(settlement) == 0
