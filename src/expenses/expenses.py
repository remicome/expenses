"""Définition de l'interface principale du module."""

from __future__ import annotations

import dataclasses
import datetime
import os
import typing

import pandas as pd

from ._ihatemoney import read_ihatemoney_csv
from ._settle import individual_balances, settle
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
    weights: dict = dataclasses.field(default_factory=dict)

    def __post_init__(self) -> None:
        """Vérifie la validité des poids donnés."""
        try:
            self._validate_weights(self.weights)
        except ValueError as exception:
            message = "Données de poids invalide."
            raise ValueError(message) from exception

    @classmethod
    def from_ihatemoney(cls: type[typing.Self], path: os.PathLike) -> typing.Self:
        """
        Importe des dépenses depuis un export de I Hate Money

        Source:
            https://ihatemoney.org

        Args:
            path: chemin vers un fichier CSV tel qu'exporté par I Hate Money.

        Returns:
            Une liste de dépenses.
        """
        expenses = read_ihatemoney_csv(path)
        return cls(expenses)

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
        return settle(self.expenses, weights=self.weights)

    def statement(self) -> pd.Series:
        """
        Calcule le bilan de chaque membre du groupe.

        Returns:
            Une série donnant le bilan de chaque membre. Si ce dernier est négatif,
            le membre doit de l'argent au groupe ; s'il est positif, le groupe lui doit
            de l'argent.
        """
        statement = individual_balances(self.expenses, weights=self.weights)
        return pd.Series(statement)

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
        weights_df = pd.read_csv(path, sep=";", decimal=",")
        weights = weights_df.set_index("membre").to_dict()
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

    @property
    def labels(self) -> set[str]:
        """
        Retourne l'ensemble des étiquettes définies par les dépenses.

        Returns:
            L'ensemble des étiquettes trouvés dans les dépenses entrées jusqu'à présent.
        """
        return {expense.label for expense in self.expenses if expense.label}

    def __len__(self) -> int:
        """Retourne le nombre de dépenses."""
        return len(self.expenses)

    def __iter__(self) -> typing.Iterable[Expense]:
        """Itère sur la liste des dépenses."""
        yield from self.expenses

    def _validate_weights(self, weights: dict) -> None:
        """Valide les données de poids."""
        if not weights:
            return

        all_members = (set(value.keys()) for value in weights.values())
        weight_members = set.union(*all_members)
        extra_members = weight_members - self.members
        if extra_members:
            message = (
                f"Les poids sont donnés pour des membres inconnus : {extra_members}."
            )
            raise ValueError(message)

        missing_members = self.members - weight_members
        if missing_members:
            message = (
                f"Les poids pour ces membres ne sont pas définis : {missing_members}."
            )
            raise ValueError(message)

        weight_labels = set(weights.keys()) - {"membre"}
        unknown_labels = weight_labels - self.labels
        if unknown_labels:
            message = (
                f"Étiquettes inconnues dans les données de poids : {unknown_labels}."
            )
            raise ValueError(message)
