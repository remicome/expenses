"""Teste la fonction qui calule les dettes de chacun à l'égard du groupe."""

from expenses._expense import Expense
from expenses._settle import _individual_debts


def test_debts() -> None:
    """
    Vérifie le calcul sur un exemple simple.

    Ici Rémi engage 100€ au nom de François et lui-même. Le groupe a donc engagé 50€
    pour chaque membre : Rémi est en excédent de 50€ et François en déficit de 50€.
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
    debts = _individual_debts(expenses)
    assert debts[remi] == 50 and debts[francois] == -50


def test_sum_of_debts(expenses: list[Expense]) -> None:
    """La somme des dettes est zéro par définition."""

    debts = _individual_debts(expenses)
    assert sum(debts.values()) == 0
