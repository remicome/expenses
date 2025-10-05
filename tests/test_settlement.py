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
    expenses: list[Expense] = []
    settlement = settle(expenses)
    assert len(settlement) == 0


def test_positive_amounts(expenses: list[Expense]) -> None:
    """Teste que le montant de chaque virement est positif."""
    transfers = settle(expenses)
    is_positive = transfers["montant"] > 0
    assert is_positive.all()


def test_simple_settlement(expenses: list[Expense]) -> None:
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
