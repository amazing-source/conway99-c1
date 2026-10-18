# Branche c_min = 3 : couverture complète des gabarits de racine (LAB, 18/10/2026)

**Statut : couverture finie, VÉRIFIÉE au niveau des gabarits et du Gram entier. Pas d'exclusion de la branche.**

## Cadre

- **Racine.** On prend la racine de budget : τ(v) = Σ_{l ∋ v} t(l) ≤ 51.
  - Elle existe dans tout graphe de Conway, car P ≤ 852 (certificat de Codex, à reproduire indépendamment).
  - Sous c_min = 3, ses 7 droites ont toutes c ≥ 3.
  - Chaque grille à la racine coûte 4 prismes, donc k ≤ 12 grilles.
- **Gabarit.** C'est le graphe J des paires sans grille, avec la partition de chaque droite en composantes (singletons
  = grilles).
- **Filtres exacts sur les gabarits** (`cle3_templates.py`, LAB, prouvés) :
  - (P) classes signées : un bloc de taille 2 force v = −v', et un cycle impair est exclu ;
  - (O') deux blocs d'une même droite sont orthogonaux ;
  - (S') un bloc de taille ≥ 3 ;
  - (Z) une coordonnée nulle dans ker C ;
  - (K) rang R ≥ 6 − c_i pour chaque droite.
- **Test de Gram entier** (`cle3_gram.py`, adapté de `root_component_gram.py` de Codex) :
  - C R = 0 ;
  - E3 : R_ee ∈ {4, 6, 8} ;
  - bornes et signes de Codex, mineurs 2×2, trace ≤ 28 dim ker C ;
  - connexité des composantes : toute coupe propre d'une composante a un poids ≤ −2 ;
  - coupes exactes de positivité pour R ⪰ 0 et 28I − R ⪰ 0.
- **Contrôles croisés.**
  - Le lemme de parité de la note ChatGPT (aucune racine sans grille sous c ≥ 3) est retrouvé : 0 gabarit.
  - Pour une grille, 33 gabarits dont 30 infaisables au Gram et 3 survivants : c'est exactement le résultat
    ChatGPT obtenu par certificats de Farkas.

## Résultats

| Grilles à la racine | Graphes J | Gabarits | Infaisables au Gram | Ouverts |
|---|---:|---:|---:|---:|
| 0 | 1 | 0 | – | 0 |
| 1 | 1 | 33 | 30 | 3 |
| 2 | 2 | 2 579 | 2 557 | 22 |
| 3 | 5 | 71 115 | 70 936 | 179 |
| 4 | 10 | 161 444 | 160 763 | 681 |
| 5 | 20 | 149 328 | 147 491 | 1 837 |
| 6 | 39 | 81 936 | 79 031 | 2 905 |
| 7 | 60 | 31 972 | 29 713 | 2 259 |
| 8 | 84 | 9 477 | 8 164 | 1 313 |
| 9 | 102 | 2 396 | 1 829 | 567 |
| 10 | 97 | 493 | 302 | 191 |
| 11 | 76 | 127 | 54 | 73 |
| 12 | 48 | 26 | 4 | 22 |
| **Total** | 545 | **510 926** | 500 874 | **10 052** |

- Aucun cas UNKNOWN au test de Gram.
- dim ker C des ouverts : de 2 à 7, surtout 4 et 5.
- Calcul : AWS, 541 tâches sur 2 × 128 coeurs, environ 25 min, environ 1 $.

## Étape suivante, et ce qu'elle a déjà montré

- La réalisation des coins avec le budget 51 (`cle3_corner.py`, fonctions de Codex sans sa borne de rang ≤ 4, qui
  n'est qu'une limite d'énumération) ne retire aucun des 25 ouverts à 1 et 2 grilles. C'est le même constat que chez
  Codex à c ≥ 4 (106 → 100).
- Les 10 052 gabarits ouverts demandent donc le modèle global (C1/C2 sur les 84 étiquettes et au-delà), comme les 79
  gabarits de Codex à c ≥ 4.
- **Ce qu'on peut en dire :** c'est environ 100 fois plus de gabarits qu'à c ≥ 4, mais c'est une liste finie et
  explicite.

## Couverture totale visée

Avec la même racine, la réunion des trois balayages suivants couvre TOUT graphe de Conway (sous P ≤ 852) :
- c_min = 3 (toutes les droites de la racine à c ≥ 3), ce fichier ;
- c_min = 2 « exact » (une droite de la racine à c = 2) ;
- c_min = 1 « exact » (une droite de la racine à c = 1).

Les deux derniers ne sont pas encore faits. Un essai local sur un graphe de c_min = 2 donne 37 % d'ouverts au Gram,
contre environ 2 % pour c_min = 3.
