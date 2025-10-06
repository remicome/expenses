"""Définition d'une transaction individuelle."""

import datetime

import pydantic


class Expense(pydantic.BaseModel):
    """
    Une dépense engagée pour le groupe.

    Chaque dépense est une opération comptable portée au bilan du groupe. Ainsi, si
    Alice dépense 100€ au nom de Bob et Charlie, on inscrit :

        - 100€ au *passif* du groupe correspondant aux ressources apportées par Alice ;
        - 100€ à *l'actif* du groupe, qu'on distingue en deux créances de 50€ : il
          s'agit de l'argent que Bob et Charlie doivent maitenant au groupe.

    Attributs:
        amount: montant de la dépense.
        who_paid: qui réalisé la dépense ?
        who_for: au nom de qui la dépense a-t-elle été réalisée ?
        description: une description optionnelle de la dépense
        when: quand a eu lieu la dépense ?
        label: une étiquette optionnelle à attribuer à la dépense.
    """

    amount: float
    who_paid: str
    who_for: list[str]
    description: str = ""
    when: datetime.date = pydantic.Field(default_factory=datetime.date.today)
    label: str | None = None

    @pydantic.field_validator("when", mode="before")
    @classmethod
    def cast_datetime(cls, when: datetime.date | str | None) -> datetime.date | str:
        """Convertit la date donnée."""
        if when is None:
            return datetime.date.today()

        return when
