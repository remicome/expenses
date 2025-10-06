"""Test l'import des dépenses depuis IHateMoney."""

import pathlib
import tempfile
import typing

import pandas as pd
import pytest

from expenses import Expenses


def test_import(original_expenses: Expenses, ihatemoney_file: pathlib.Path) -> None:
    """Teste l'import."""

    imported_expenses = Expenses.from_ihatemoney(ihatemoney_file)
    assert all(
        imported_expense == original_expense
        for imported_expense, original_expense in zip(
            imported_expenses, original_expenses
        )
    )


@pytest.fixture
def original_expenses(expenses: Expenses) -> Expenses:
    """
    La liste des dépenses enregistrées à travers I Hate Money

    Il s'agit de la liste telle quelle, à laquelle on retire les étiquettes.
    """
    return Expenses(
        [expense.model_copy(update={"label": None}) for expense in expenses]
    )


@pytest.fixture
def ihatemoney_file(expenses: Expenses) -> typing.Iterator[pathlib.Path]:
    """
    Un fichier de dépense au format exporté par I Hate Money.

    On ne conserve que les colonnes effectivement utilisées.
    """
    expenses = pd.DataFrame(
        [
            {
                "what": expense.description,
                "amount": expense.amount,
                "date": expense.when.strftime("%Y-%m-%d"),
                "payer_name": expense.who_paid,
                "owers": ",".join(expense.who_for),
            }
            for expense in expenses
        ]
    )
    with tempfile.TemporaryDirectory() as directory:
        destination = pathlib.Path(directory) / "ihatemoney.csv"
        expenses.to_csv(destination, sep=";", index=False)
        yield destination
