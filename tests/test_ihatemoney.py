"""Test l'import des dépenses depuis IHateMoney."""

import pathlib
import tempfile
import typing

import pandas as pd
import pytest

from expenses import Expenses


def test_import(ihatemoney_file: pathlib.Path) -> None:
    """Teste l'import."""

    expenses = Expenses.from_ihatemoney(ihatemoney_file)
    assert len(expenses) > 0


@pytest.fixture
def ihatemoney_file() -> typing.Iterator[pathlib.Path]:
    """
    Un fichier de dépense au format exporté par I Hate Money.

    On ne conserve que les colonnes effectivement utilisées.
    """
    remi = "Rémi"
    francois = "François"
    sophie = "Sophie"

    expenses = pd.DataFrame(
        [
            {
                "what": "gite",
                "amount": 1000,
                "date": "2025-01-01",
                "payer_name": remi,
                "owers": f"{remi}, {francois}, {sophie}",
            }
        ]
    )
    with tempfile.TemporaryDirectory() as directory:
        destination = pathlib.Path(directory) / "ihatemoney.csv"
        expenses.to_csv(destination, sep=";")
        yield destination
