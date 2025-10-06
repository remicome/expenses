"""Définition de l'interface principale du module."""

from __future__ import annotations

import dataclasses
import datetime
import os

import pandas as pd

from ._settle import settle
from .expense import Expense


@dataclasses.dataclass
class Expenses:
    """
    Une liste de dépenses.

    Args:
        expenses: liste de dépenses à ajouter
        weights: une définition optionnelle de poids à appliquer aux dépenses d'un
            certain type.
    """

    expenses: list[Expense] = dataclasses.field(default_factory=list)
    weights: pd.DataFrame = dataclasses.field(default_factory=pd.DataFrame)

    def append(
        self,
        amount: float,
        who_paid: str,
        who_for: list[str],
        description: str = "",
        when: datetime.datetime | str | None = None,
        label: str | None = None,
    ) -> None:
        """Ajoute une dépense à la liste."""
        self.expenses.append(
            Expense(
                amount=amount,
                who_paid=who_paid,
                who_for=who_for,
                description=description,
                when=when,
                label=label,
            )
        )

    def settle(self) -> pd.DataFrame:
        """
        Équilibre les dépenses.

        Returns:
            Un DataFrame qui donne les virement à effectuer pour parvenir à l'équilibre.
        """
        return settle(self.expenses)

    def with_weights(self, path: os.PathLike) -> Expenses:
        """
        Ajoute des poids depuis un fichier CSV.

        Le fichier CSV doit avoir une colonne "membre", ainsi qu'une colonne par poids
        qu'on souhaite définir.

        Args:
            path: chemin vers le fichier CSV.

        Raises:
            ValueError: si la colonne membre n'est pas présente, ou si un poids défini
            par le fichier ne correspond pas à une étiquette connue.
        """
        weights = pd.read_csv(path, sep=";", decimal=",")
        return dataclasses.replace(self, weights=weights)

    @property
    def members(self) -> set[str]:
        """
        Retourne l'ensemble des membres impliqués dans les dépenses.

        Returns:
            L'ensemble des membres trouvés dans les dépenses entrées jusqu'à présent.
        """
        members = (
            {expense.who_paid} | set(expense.who_for) for expense in self.expenses
        )
        return set.union(*members)

    def __len__(self) -> int:
        """Retourne le nombre de dépenses."""
        return len(self.expenses)
