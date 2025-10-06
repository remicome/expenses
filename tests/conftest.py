"""Fixtures communes aux différents modules de test."""

import pathlib
import random
import tempfile
import typing

import pandas as pd
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
def expense_list(members: list[str], labels: list) -> list[Expense]:
    """Une liste de dépenses aléatoires."""
    return [
        Expense(
            amount=random.randint(1, 100),
            who_paid=random.choice(members),
            who_for=random.sample(members, k=2),
            label=random.choice(labels),
        )
        for _ in range(10)
    ]


@pytest.fixture
def weight_file(weights: pd.DataFrame) -> typing.Iterator[pathlib.Path]:
    """Chemin vers un fichier de poids."""
    with tempfile.TemporaryDirectory() as directory:
        destination = pathlib.Path(directory) / "weights.csv"
        weights.to_csv(destination, sep=";", decimal=",")
        yield destination


@pytest.fixture
def weights(members: list, labels: list) -> pd.DataFrame:
    """Poids associés à chaque dépense."""
    return pd.DataFrame(
        [
            {"membre": member} | {label: random.randint(1, 10) for label in labels}
            for member in members
        ]
    )


@pytest.fixture
def labels() -> list[str | None]:
    """Liste d'étiquettes associées aux dépenses."""
    return [None, "logement", "ski"]


@pytest.fixture
def members() -> list[str]:
    """Liste des membres du groupe."""
    return ["Rémi", "François", "Sophie"]
