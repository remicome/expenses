"""Module gérant l'interface avec I Hate Money."""

import os

import pandas as pd

from .expense import Expense


def read_ihatemoney_csv(path: os.PathLike) -> list[Expense]:
    """Lit un fichier tel qu'exporté par I Hate Money."""
    df = pd.read_csv(path, sep=";")
    return [
        Expense(
            amount=row.amount,
            who_paid=row.payer_name,
            who_for=_who_for(row.owers),
            when=row.date,
            description=row.what,
        )
        for _, row in df.iterrows()
    ]


def _who_for(owers: str) -> list[str]:
    """Extrait la liste des débiteur à partir d'une chaîne de caractère."""
    return owers.split(",")
