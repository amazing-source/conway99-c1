# Paley : reconstruction exacte et apparition de l’asymétrie

**Campagne du 11 octobre 2026.** Dossier de résultats, de matrices et de programmes.
Aucun fichier du dépôt GitHub de l’utilisateur n’a été modifié.

## Résultat principal

En gardant une clique \(K_5\) de Paley(25) **et toutes les arêtes incidentes à ses cinq sommets**,
puis en reconstruisant uniquement les arêtes entre les vingt autres sommets, le moteur exact
retrouve les **15 classes** de SRG(25,12,5,6), dont les **deux classes asymétriques connues**.

Ce sont des graphes de Paulus–Rozenfeld déjà connus, et non de nouveaux SRG.
La nouvelle expérience de cette campagne est le passage constructif depuis un bord de Paley,
sa classification exhaustive et l’explication vérifiable de la disparition des symétries.

| Résultat | Valeur |
|---|---:|
| Domaines binaires de chaque ligne libre | 1 718 |
| Nœuds du moteur, graine 3 | 67 130 |
| Feuilles représentatives après réductions partielles | 3 983 |
| Complétions étiquetées, poids de symétrie rétablis | 1 999 872 |
| Classes d’isomorphisme retrouvées | 15 |
| Classes asymétriques | 2 |
| Modification explicite livrée | 37 arêtes retirées, 37 ajoutées |
| Symétries du noyau canonique du témoin livré | 2 |
| Symétries de ce noyau compatibles avec les attaches | 1 |
| Automorphismes du témoin livré | identité seulement |

**Contrôle Paley(9)** : le même principe de reconstruction, autour d’un triangle fixé,
donne quatre complétions étiquetées, toutes isomorphes à la grille \(3\times3\).

**Obstacles complètement testés à 25 :**
les changements standards de Godsil–McKay à une cellule ne quittent jamais la classe de Paley ;
imposer une partition complète en cinq \(K_5\) ne permet que les deux classes de graphes latins,
toutes deux symétriques. Libérer cette partition, tout en conservant un \(K_5\), permet l’asymétrie.

## Vérifier le résultat sans aucune dépendance

Depuis le dossier extrait :

```sh
python3 -S code/verify_witness.py
python3 -S code/verify_census.py
python3 -S code/verify_spectral.py
```

Le premier programme reconstruit Paley sur \(\mathbb F_{25}\), vérifie les 300 paires du témoin,
la liste des arêtes modifiées et **deux preuves d’asymétrie**, sans nauty ni solveur.

Le second contrôle les 3 983 matrices représentatives, leurs isomorphismes explicites vers le
catalogue et les totaux enregistrés. La couverture exhaustive vient du moteur et de son argument
de couverture, pas de la seule présence d’un fichier de témoins.

## Refaire la recherche

Python 3.10 ou plus, NetworkX et un compilateur `g++` prenant C++17 en charge :

```sh
python3 -m pip install -r requirements.txt
python3 code/reproduce.py --out runs/essai_001
```

Pour les comparaisons de frontières, le recensement des changements Godsil–McKay et le minimum
de modification dans la famille fixée :

```sh
python3 code/reproduce.py --out runs/essai_complet_001 --extra
```

Un dossier de sortie déjà existant est refusé. Aucun appel réseau, aucune API de modèle,
aucun calcul cloud et aucune dépendance SAT ne sont utilisés.
L’exécutable est ici limité aux graphes d’au plus 25 sommets ; ce n’est pas un moteur 243/99 prêt à l’emploi.

## Lire

- `RESULTATS.md` : résultats, explication de l’asymétrie et portée pour la campagne 243.
- `THEORIE.md` : équations exactes, preuve de couverture et justification des certificats.
- `FAILURE_LEDGER.md` : impasses effectivement testées et conditions de réouverture.
- `sources/PROVENANCE.md` : données publiques, commits GitHub consultés, numérotation et antériorité.
- `data/paley25_to_asymmetric.adj` : témoin explicite (également `.g6` et `.edges`).
- `certificats/` : transformation, couleurs et noyau/attaches.
- `resultats/` : résultats bruts, correspondances, contrôles et répétition complète.

Les identifiants 1 à 15 sont les positions dans le fichier de McKay, **pas** les noms P25.xx
de la page de Brouwer. Le Paley est ici le n° 2 ; les asymétriques sont les n° 7 et 13.

Ces résultats ne classifient pas les SRG(243,22,1,2) et n’excluent pas C1. Ils apportent un
banc d’essai positif où l’on peut expliquer et vérifier la fabrication de l’asymétrie.
