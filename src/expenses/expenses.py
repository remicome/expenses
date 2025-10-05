"""Définition de l'interface principale du module."""

import dataclasses
import datetime

from ._expense import Expense


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

    def __len__(self) -> int:
        """Retourne le nombre de dépenses."""
        return len(self._expenses)
