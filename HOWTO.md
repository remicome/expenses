# Comment utiliser cette librairie ?

Je recommande l'utilisation de [I hate money](https://ihatemoney.org/) pour
entrer les dépenses de manière collaborative. 

Dans groupe constitué de trois personnes : Rémi, François et Sophie. Ce groupe a
entré deux dépenses dans I hate money

## 1. Télécharger les dépenses
Les dépenses peuvent être téléchargées depuis l'interface web de I hate
money en cliquant en haut à droite sur le nom du projet, puis sur Options. Dans
la page qui s'ouvre, naviguer jusqu'à "Télécharger les données du projet" et
cliquer sur le bouton "CSV" pour "Télécharger la liste des factures et détails".

On obtient alors un fichier `factures.csv` qui contient les informations suivantes :

|what      |amount|currency|date      |payer_name|payer_weight|owers                 |
|----------|------|--------|----------|----------|------------|----------------------|
|Restaurant|50.0  |XXX     |2025-10-07|Sophie    |1.0         |Rémi, François, Sophie|
|Gîte      |300.0 |XXX     |2025-10-07|Rémi      |1.0         |Rémi, François, Sophie|

## 2. Définir des poids
Rémi a passe seulement une nuit dans le logement alors que François et Sophie y
ont dormi deux nuits. On décide alors d'attribuer des poids différents à la
location du gite. Pour ça, deux étapes.

### 2.1 Marquer les dépenses concernées
On ajoute une étiquette "logement" à la dépense concernée en créant la colonne
"label" dans le fichier `factures.csv` :

|what      |**label**   |amount|currency|date      |payer_name|payer_weight|owers                 |
|----------|------------|------|--------|----------|----------|------------|----------------------|
|Restaurant|            |50.0  |XXX     |2025-10-07|Sophie    |1.0         |Rémi, François, Sophie|
|Gîte      |**logement**|300.0 |XXX     |2025-10-07|Rémi      |1.0         |Rémi, François, Sophie|

### 2.2 Écrire les poids dans un fichier
On entre les poids correspondant dans un autre fichier `poids.csv` :

|membre    |logement|
|----------|--------|
|Rémi      |1       |
|François  |2       |
|Sophie    |2       |

### 2.3 Compliquons l'exemple
Rémi est un gros mangeur, on décide alors qu'il paiera sa nourriture 3 fois plus
cher que tout le monde. On crée donc une nouvelle étiquette dans `factures.csv`
:

|what      |label          |amount|currency|date      |payer_name|payer_weight|owers                 |
|----------|---------------|------|--------|----------|----------|------------|----------------------|
|Restaurant|**nourriture** |50.0  |XXX     |2025-10-07|Sophie    |1.0         |Rémi, François, Sophie|
|Gîte      |logement|300.0 |XXX     |2025-10-07|Rémi      |1.0         |Rémi, François, Sophie|

Les poids correspondants sont ajoutés comme nouvelle colonne du fichier
`poids.csv` :

|membre    |logement|nourriture|
|----------|--------|----------|
|Rémi      |1       |3         |
|François  |2       |1         |
|Sophie    |2       |1         |

## 3. Équilibrer les dépenses
On utilise maintenant la librairie pour équilibrer les dépenses. Si celle-ci
n'est pas installée, référez-vous au [README](README.md).

### 3.1 Établir le bilan des dépenses
```python
from expenses import Expenses

expenses = expenses.from_ihatemoney("factures.csv").with_weights("poids.csv")
expenses.statement()
```
On obtient le bilan détaillé de chaque membre du groupe :

|membre    |a payé|dépenses|dont logement|dont nourriture|bilan |
|----------|------|--------|-------------|---------------|----- |
|François  |0.0   |130.0   |120.0        |10.0           |-130.0|
|Rémi      |300.0 |90.0    |60.0         |30.0           |210.0 |
|Sophie    |50.0  |130.0   |120.0        |10.0           |-80.0 |

### 3.2 Déterminer les virements nécessaires
```python
from expenses import Expenses

expenses = expenses.from_ihatemoney("factures.csv").with_weights("poids.csv")
expenses.settle()
```
Cette commande donne une liste de virements qui permet d'atteindre l'équilibre des comptes :

|émetteur|destinataire|montant|
|--------|------------|-------|
|François|Rémi        |130    |
|Sophie  |Rémi        |80     |
