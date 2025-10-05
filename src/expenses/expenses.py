"""Définition de l'interface principale du module."""

import dataclasses
import datetime

import pandas as pd

from ._expense import Expense
from ._settle import settle


@dataclasses.dataclass
class Expenses:
    """Une liste de dépenses."""

    _expenses: list[Expense] = dataclasses.field(init=False, default_factory=list)

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
        self._expenses.append(
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
        return settle(self._expenses)

    @property
    def members(self) -> set[str]:
        """
        Retourne l'ensemble des membres impliqués dans les dépenses.

        Returns:
            L'ensemble des membres trouvés dans les dépenses entrées jusqu'à présent.
        """
        members = (
            {expense.who_paid} | set(expense.who_for) for expense in self._expenses
        )
        return set.union(*members)

    def __len__(self) -> int:
        """Retourne le nombre de dépenses."""
        return len(self._expenses)
