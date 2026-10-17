# 228 — Réduire moulin–cubique à un noyau positif de 17 sommets

9 octobre 2026. Nouvelle piste issue du cas restant signalé par LAB au
message 433. La note 227 traite séparément le gain déjà acquis sur C8.

**Réduction.** Une relation de projection entre un moulin et un cubique
à huit sommets équivaut à un vecteur entier non négatif de noyau, de
profil (2,1^16). Son support de 17 sommets détermine exactement les
voisinages et les effectifs de ses 82 sommets extérieurs. Sous P=0,
il reste 359 types de supports enracinés, nécessaires seulement.

Ces 359 types concernent **les relations moulin–cubique**, pas une
nouvelle couverture de tous les graphes C1. Ils ne remplacent pas les
174 noyaux obligatoires de la note 222.

## 1. Identité de réduction et réciproque

Soit E le projecteur sur l'espace propre −4. Écrivons le moulin

    u=2e_v+1_L,

où L est la réunion de trois arêtes du voisinage de v. Si un cubique V
à huit sommets a Eu=E1_V, les deux supports sont disjoints et anticomplets
(note 183). Posons X=N(v)\L, réunion des quatre autres arêtes.

Puisque E(A+4I)=0,

    φ=(A+4I)e_v−(u−1_V)=2e_v+1_X+1_V

vérifie Eφ=0, donc

    Σφ=18,       Aφ=3φ+2·1.                          (1)

Réciproquement, supposons qu'un vecteur de noyau φ ait un unique
coefficient deux, en v, et seize coefficients un. L'équation (1) en v
impose exactement huit voisins de v dans son support : c'est X. Les
huit autres points V sont lointains de v.

Un voisin de v hors du support voit déjà le poids deux de v. Par (1),
il ne voit aucun autre point du support. L'appariement induit par N(v)
impose donc que X soit une réunion de quatre arêtes et que les six
voisins restants L forment trois arêtes.

Chaque point x de X voit v (poids deux) et son conjoint dans X (poids un).
Il doit donc voir exactement deux points de V. Chaque point de V a
exactement deux voisins dans N(v), par μ=2 ; aucun n'est dans L, donc
les deux sont dans X. L'équation (1) impose alors degré trois dans V.

Ainsi X–V est biparti 2-régulier, V est cubique, et

    u−1_V=(A+4I)e_v−φ

appartient au noyau de E, a somme zéro, donc est propre de valeur +3.
Cela donne exactement une relation moulin–cubique.

## 2. Tous les profils extérieurs sont forcés

Soit H={v}∪X∪V. Pour tout y extérieur à H, (1) donne

    2 [y~v] + |N(y)∩(X∪V)|=2.

Il n'y a donc que deux formes de voisinage dans H :

- {v}, avec exactement six sommets de ce profil ;
- une paire {i,j} de X∪V, avec effectif exactement

      m_ij = 2−A_ij−(A_H²)_ij.                       (2)

La formule (2) est le déficit en voisins communs du couple i,j. Chaque
effectif est 0,1 ou 2. Aucun autre sommet extérieur ne peut contribuer
à ce déficit, car tous les autres profils ont taille un ou deux.

Les six premiers sommets forment trois arêtes. Les profils de paires
comptent les 76 autres sommets. Leurs effectifs satisfont également
tous les déficits de degré des sommets de H. Les arêtes entre sommets
extérieurs ne sont pas déterminées par ce lemme.

## 3. Lien avec les grilles

Si le support de φ contient une grille R, son indicatrice appartient
au noyau E et φ−1_R est un vecteur non négatif de noyau, de somme neuf.
Le lemme de la note 179 impose que ce reste soit aussi l'indicatrice
d'une grille. La première grille doit contenir v, faute de quoi le
reste conserverait un coefficient deux.

Ainsi, dans un graphe C1 effectif, les deux propriétés sont équivalentes :

- le support de φ contient une grille ;
- φ est la somme de deux indicatrices de grilles qui se coupent
  exactement en v.

On ne conclut pas que toute relation (1) se décompose ainsi. Les
relations indécomposables restent une cible possible pour un lemme.
Sous P=0, le support est nécessairement sans prisme, condition plus forte.

## 4. Catalogue fini nécessaire sous P=0

Le cubique V est l'un des trois types déjà connus de la note 183.
Chaque sommet x de X est représenté par sa paire de voisins dans V.
Ces huit paires sont distinctes : deux sommets de X partageant leurs
deux voisins dans V auraient, avec v, trois voisins communs.
Elles forment donc un 2-facteur simple F sur V. Ses cycles sont
8, 5+3 ou 4+4. Il y a 3507 tels 2-facteurs étiquetés.

Les quatre arêtes de X correspondent à un appariement des huit arêtes
de F. Les contraintes locales λ≤1,μ≤2 se traduisent exactement ainsi :

1. Une arête ij de F n'est autorisée que si le couple i,j de V n'a pas
   déjà épuisé son budget de voisins communs dans V.
2. Deux arêtes de F appariées doivent être disjointes ; aucun de leurs
   sommets ne doit voir dans V les deux extrémités de l'autre arête.

On construit H pour chacun de ces choix et retire les supports contenant
deux triangles disjoints reliés par un couplage parfait, c'est-à-dire
un prisme induit. Le résultat est :

| Type du cubique V | H localement admissibles, étiquetés | Sans prisme | Types enracinés sans prisme |
|---|---:|---:|---:|
| 2022000 | 2826 | 621 | 29 |
| 5683824 | 4120 | 1489 | 122 |
| 5691760 | 1094 | 735 | 208 |
| Total | 8040 | 2845 | **359** |

Le centre v est l'unique sommet de degré huit ; X et V ont respectivement
degré quatre et cinq dans H. L'isomorphisme du graphe H préserve donc
automatiquement ces rôles. La canonisation exacte utilise cette structure.

Les deux projecteurs réels et l'ajout de chaque profil extérieur forcé
ne suppriment aucun des 359 types. Cela reste une condition nécessaire,
sans témoin de prolongement à 99 sommets. Ce premier test n'est pas une
raison de relancer des vérifications répétées : toute suite doit apporter
des contraintes nouvelles sur les arêtes entre les profils forcés.

## 5. Fichiers et suite précise

- `code/codex/mill_cubic_positive18.py` et
  `data/codex_mill_cubic_positive18.json` : construction finie des supports.
- `code/codex/positive18_forced_extensions.py` et
  `data/codex_positive18_forced_extensions.json` : 359 représentants,
  multiplicité de chaque profil extérieur, portée des premières contraintes.

Deux suites théoriques sont désormais définies : montrer que toute
relation positive (2,1^16) contient une grille, ou trouver une obstruction
à la compatibilité simultanée des profils de (2). Aucune de ces deux
affirmations n'est démontrée dans cette note.
