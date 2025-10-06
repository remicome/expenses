"""Fixtures communes aux différents modules de test."""

import random

import pytest
from expenses import Expenses
from expenses._expense import Expense


@pytest.fixture
def expenses(expense_list: list[Expense]) -> Expense:
    """Une liste de dépenses aléatoires."""
    expenses = Expenses()
    for expense in expense_list:
        expenses.append(**dict(expense))
    return expenses


@pytest.fixture
def expense_list() -> list[Expense]:
    """Une liste de dépenses aléatoires."""
    members = ["Rémi", "François", "Sophie"]
    return [
        Expense(
            amount=random.randint(1, 100),
            who_paid=random.choice(members),
            who_for=random.sample(members, k=2),
        )
        for _ in range(10)
    ]
