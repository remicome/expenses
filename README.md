# Gestion des dépenses entre amis

![Build and test](https://github.com/remicome/expenses/actions/workflows/build_and_test.yml/badge.svg)

Un gestionnaire de dépenses de groupes avec des options avancées de
répartitions.

```python
from expense import Expenses

expenses = Expenses.add(
    36,
    who_paid="Rémi",
    who_for=["Rémi", "François"]
    description="Restaurant",
)
expenses.settle()

# émetteur  destinataire  montant
# François  Rémi          18
```

## Pourquoi ?
Cette librairie permet d'attribuer des *poids* selon le type de dépense : ainsi,
les dépenses de nourriture et logement peuvent être traitées différemment des
dépenses générales, en payant par exemple au _pro rata_ du nombre de nuits.

Elle permet également d'importer des dépenses depuis [I hate
money](https://ihatemoney.org/), alternative libre à Tricount.

```python
expenses = Expenses.from_ihatemoney("dépenses.csv").with_weights("poids.csv")
```

## Comment l'installer ?
Depuis les sources :
```bash
git clone https://github.com/remicome/expenses.git
pip install expenses
```

## Comment l'utiliser ?
Voir le [HowTo](HOWTO.md).
