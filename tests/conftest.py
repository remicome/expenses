"""Fixtures communes aux différents modules de test."""

import random

import pytest
from expenses._expense import Expense


@pytest.fixture
def expenses() -> list[Expense]:
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
