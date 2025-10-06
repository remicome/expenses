"""Teste la fonction qui calule les dettes de chacun à l'égard du groupe."""

from expenses._settle import _individual_debts
from expenses.expense import Expense


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


def test_weighted_debts() -> None:
    """
    Vérifie le calcul sur un exemple simple, avec des poids.

    Rémi engage 100€ au nom de François et lui-même, sur une dépense à répartir sous la
    forme 75% - 25%. François doit donc 25€ au groupe, tandis que Rémi est en excédent
    de 25€.
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
    debts = _individual_debts(expenses, weights=weights)
    assert debts[remi] == 25 and debts[francois] == -25


def test_sum_of_debts(expense_list: list[Expense]) -> None:
    """La somme des dettes est zéro par définition."""

    debts = _individual_debts(expense_list)
    assert sum(debts.values()) == 0
