# Coût réel de l'étape « étoile complète » pour c_min ≥ 3, après correction du bug (LAB, 18/10/2026)

Demande de l'utilisateur (18/10, vers 13 h 50) : « mesurer le coût de c=3, et essayer surtout de le réduire tout en
restant sur l'énoncé, avec des lemmes et tout ».

## Pilotes AWS

- **Échantillon** : 100 tâches (gabarit, couplage de l'étoile) tirées uniformément, graine 20261018, parmi les 106 852
  tâches du manifeste de Codex (`complete_star_manifest10052.json`, 10 052 gabarits ouverts après le Gram).
- **Code de Codex** : 8d45031f, puis 156fda14 (correctif des produits inclus). Commande :
  `root_component_complete_star.py <catalogue> --index i --matching-indices j --seconds S --residual-eigen 2`,
  avec ou sans `--no-transport`, avec ou sans `--grid-corner-tables`.
- **Machines** : run verif1b, puis verif2b (m7a.32xlarge, 1 cœur par tâche, `taskset` disjoints).

| Variante (S = 60 s) | INFEASIBLE | UNKNOWN | temps mural moyen |
|---|---:|---:|---:|
| transport (défaut) | 38 | 62 | 50,7 s |
| `--no-transport` | **58** | 42 | 40,2 s |
| `--grid-corner-tables` (transport) | 40 | 60 | – |

- Les 38 tâches exclues avec transport sont toutes exclues aussi sans transport.
- Sur les 42 tâches non résolues dans les deux variantes à 60 s, avec S = 600 s :
  - `--no-transport` en exclut 18 de plus, avec un CPU de 88 à 557 s ;
  - `--grid-corner-tables` en exclut 11.
- **Réunion de tous les modèles (tous valides)** : 77 tâches sur 100 exclues ; 23 résistent à 600 s.
- Étiquette `python_list_endpoints_v2` : présente sur 94 des 100 sorties avec transport. Les 6 autres sont INFEASIBLE
  et déjà couvertes par `--no-transport`, qui n'utilise pas les produits.

## Le noyau dur

| Classe | Tâches | dim ker C | Parts de la droite étoile |
|---|---:|---|---|
| ouvertes à 600 s | 23 | 5 (22 fois), 6 | (3,1,1,1) dans 15 cas sur 23 |
| exclues entre 60 et 600 s | 19 | 4, 5 | surtout (2,2,1,1) |
| exclues en ≤ 60 s | 58 | 3 à 6 | variées |

- Sur l'ensemble du manifeste, dim ker C = 5 avec une part de taille 3 représente 37 185 tâches (34,8 %).
- Le sous-type (5, (3,1,1,1)) en représente 21 390, sur 1 426 gabarits. Ses droites ont typiquement les blocs (2,3),
  (2,3), (2,3), (3), (4), (4), (4) ; la droite étoile est celle à bloc (3) seul.
- Choisir une autre droite comme étoile coûterait plus de couplages : 45 pour (2,3), 105 pour (4).

## Extrapolation (sans transport, 60 s puis 600 s)

- Première passe : 106 852 × 40 s ≈ 1 190 h·cœur ; elle exclut environ 58 %.
- Seconde passe : environ 44 900 tâches × 424 s ≈ 5 290 h·cœur ; elle en exclut environ 43 %.
- **Total ≈ 6 500 h·cœur, soit environ 100 $ en Spot, et environ 23 % des tâches restent ouvertes.** La méthode actuelle
  ne ferme donc pas c ≥ 3 seule.

## Réduction par symétrie des lettres (en attente de la confirmation de Codex)

**Principe.**
- Échanger les deux lettres d'une droite j ≠ r0 renomme les étiquettes de l'étoile, et un graphe de Conway réalisant
  (gabarit, couplage M) réalise aussi (gabarit, σM) dans l'étiquetage échangé.
- Il suffit donc de traiter un représentant par orbite, **à condition que le modèle ne contienne aucune normalisation
  qui dépende des lettres**.

**Comptes exacts** (Burnside, orbites des couplages internes sous (Z2)^s) :
- par composante de taille s : 1/1 (s = 1), 2/3 (s = 2), 5/15 (s = 3), 17/105 (s = 4) ;
- sur le manifeste : **106 852 → 40 297 tâches (÷ 2,65)**.

**Contrôle nécessaire fait** (`equivariance_test.py`).
- On construit le modèle de Codex pour M et pour σM, pour chacune des 6 droites j ≠ r0, et on compare les multisets de
  signatures : domaines des variables ; et, par contrainte, type, coefficients triés, domaine, nombres de variables et
  de littéraux.
- **Identiques** dans tous les cas testés :
  - gabarit 4378 (parts (1,1,3,1), dim 5, une tâche dure), avec et sans transport ;
  - gabarit 1 (parts (2,2,2)).
- C'est un indice fort, pas une preuve. On attend la confirmation de Codex sur l'absence de normalisation.

**Coût avec la réduction** : environ 2 450 h·cœur, soit environ 38 $, et toujours environ 23 % ouvert.

## Pistes pour le noyau dur

1. Une coupe ou un lemme sur les composantes à 18 sommets du type (3,1,1,1). Les tables « codes18 » de Codex sont une
   piste.
2. Un modèle par gabarit avec le couplage de l'étoile comme variable, pour partager l'apprentissage entre les 15
   couplages.
3. Fixer aussi l'étoile opposée (15 × 15, réduits par symétrie), pour des tâches plus nombreuses mais plus faciles.
4. Une coupe de Gram plus forte, R ⪯ 28·Π₀ (prouvée, `cle3_gram_pi0.py`) : **aucun effet** sur les 853 gabarits
   ouverts à k ≥ 9 (54 coupes générées, 0 exclusion).

## Essais de réduction du 18/10 après-midi

- **Deux étoiles fixées** (`two_star_branch.py`) :
  - modèle `--no-transport` de Codex, avec en plus le couplage M' de l'étoile opposée fixé ;
  - les branches (M, M') couvrent exactement la branche M ;
  - testé sur les 23 tâches dures, soit 435 sous-branches à 60 s (run verif4b, c7a.16xlarge à la demande).
  - Résultat : beaucoup de sous-branches meurent à la propagation ou en moins d'une seconde, mais **aucune des 23
    tâches n'est fermée** ; plusieurs ont leurs 15 M' tous UNKNOWN. Le noyau dur ne tient pas à l'étoile opposée.
- **Pistes restantes** :
  - normalisation de racine « x minimise s » avec s(y) ≥ s(x) aux étoiles transportées (option de Codex, à brancher
    dans l'étoile complète ; une seule normalisation pour toute la couverture) ;
  - réduction par symétrie, en attente de Codex ;
  - un lemme sur les composantes à 18 sommets.

## Taille des recensements c_min ≤ 2 (estimateur de Knuth, `cle_templates_la.cpp --estimate`)

- **Contrôle** : sur c ≥ 3, k = 6, l'estimateur donne 179 555 gabarits étiquetés pour 184 217 exacts (400 sondes par
  graphe).
- **Résultats** :

| k (grilles à la racine) | c_min = 2 exact (étiquetés) | c_min = 1 exact (étiquetés) |
|---|---:|---:|
| 0 (K7) | 2,5·10¹⁰ (≈ 5·10⁶ à S7 près) | 1,0·10¹⁰ (≈ 2·10⁶) |
| 1 | 2,1·10⁹ | 6,5·10⁸ |
| 2 | 3,4·10⁸ | 7,6·10⁷ |
| 3 | 7,3·10⁷ | 1,1·10⁷ |

- L'élagage par le rang partiel (`--pk`, prouvé) ne change rien à ces tailles.
- **Les jobs K7 ont été arrêtés.** La canonisation de chaque survivant sur les 5 040 permutations de S7 les rendait
  infaisables. Le reste (k ≥ 1) est faisable et tourne (run verif1a relancé à 14 h 55).
- **Conclusion** : à symétrie près, c ≤ 2 compte de l'ordre de 10⁷ gabarits. L'étape « étoile complète » n'est pas
  envisageable à cette échelle, avec des composantes jusqu'à 36 sommets. Il faut un argument nouveau pour c ≤ 2.
