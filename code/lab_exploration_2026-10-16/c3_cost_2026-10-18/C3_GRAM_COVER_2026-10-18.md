# Couvertures de Gram dans le modèle exact « étoile complète » (LAB, 18/10/2026, fin d'après-midi)

Demande de l'utilisateur : « toujours essayer d'en extraire des lemmes, la raison de mort… il faut toujours comprendre
pourquoi quelque chose se passe pour adapter les prochaines passes ».

## Le constat qui a mené ici

- Au niveau des gabarits, le test de Gram entier tue 500 874 gabarits sur 510 926 (98 %). Son ingrédient décisif est
  la positivité : 0 ⪯ R ⪯ 28I.
- Le modèle exact de Codex (`root_component_complete_star`, C1/C2 sur les 84 étiquettes, équations de composantes,
  budget, coupes universelles, triangles) définit bien R par les arêtes, avec ses bornes, sa trace et E3. Mais il
  **n'impose pas R ⪰ 0** : CP-SAT ne sait pas exprimer cette contrainte.
- L'ablation du matin le confirmait déjà : environ 2/3 des morts viennent du cœur combinatoire, et la positivité n'y
  intervient jamais.

## La méthode

- **Couverture de Gram.** C'est la liste complète des matrices entières R permises pour le gabarit. On les énumère
  sous les contraintes prouvées de l'audit (§3, points 4 à 8) :
  - CR = 0 ;
  - E3 : R_ii ∈ {4, 6, 8} ;
  - bornes et signes ;
  - zéros entre composantes ;
  - coupes de connexité ;
  - trace ≤ 28 dim ker C ;
  - R ⪰ 0 et 28I − R ⪰ 0, tous deux exacts.
- R est déterminée par son bloc d'ancres, car son image est dans ker C. Chaque R trouvée est interdite sur ce bloc,
  et la boucle s'arrête quand le modèle devient infaisable : la liste est alors complète.
- **Deux énumérateurs LAB** :
  - `gram_cover_enum.py` : coupes PSD paresseuses ;
  - `gram_cover_enum2.py` : la même phase, puis une énumération CP-SAT complète, chaque solution étant testée
    exactement. Les deux tests se ramènent à des matrices d × d :
    - X ⪰ 0 ;
    - 28 (LᵀL)⁻¹ − X ⪰ 0, qui équivaut à 28I − R ⪰ 0.
  - Les deux énumérateurs donnent la même liste sur 4491 (92 = 92).
- **Dans le modèle exact** (`gram_cover_branch.py`) :
  - c'est `build(..., gram_cover=…)` / `add_gram_table` de Codex, en mode tous couplages libres, sans transport ;
  - variante « anchors » : table sur le bloc d'ancres ;
  - variante « full » : table sur toutes les entrées R_ij ;
  - INFEASIBLE exclut le gabarit pour tous les couplages de l'étoile à la fois.

## Contrôle croisé avec l'énumérateur de Codex (`gram_cover_crosscheck.py`)

- On lance `enumerate_grams` de Codex, sans modification. Il n'utilise ni E3 (il garde R_ii = 2 sous le budget) ni la
  connexité.
- On reconstruit chaque R complète avec le relèvement de Codex, puis on teste chaque différence contrainte par
  contrainte.
- Résultats sur les 17 gabarits testés :
  - toute R du LAB est dans la liste de Codex : `only_lab` = 0 partout ;
  - toutes les R que Codex a en plus après E3 violent **une coupe de connexité, et rien d'autre** : 1 + 4 + 2 + 11
    + 8 + 17 + … ;
  - aucune n'est inexpliquée : `unexplained` = 0.
- La couverture LAB est donc exactement « liste de Codex ∩ E3 ∩ connexité ».
- Lemme utilisé : une composante est cubique et connexe, donc toute coupe propre a une taille paire ≥ 2 (audit §3,
  point 8).

## Run gc1a (AWS, une c7a.16xlarge à la demande, ≈ 1 $)

- **Échantillon** : les 17 gabarits du noyau dur que le modèle tous couplages libres laisse UNKNOWN à 600 s (run
  verif6b), plus 4378 comme témoin.
- **Budget** : 600 s CPU par variante.

| Gabarit | Gram | anchors | full |
|---|---:|---|---|
| 3581 | 2 | INFEASIBLE 389 s | **INFEASIBLE 17 s** |
| 4801 | 3 | UNKNOWN | **INFEASIBLE 29 s** |
| 4861 | 51 | UNKNOWN | **INFEASIBLE 25 s** |
| 4378 (témoin, 521 s sans table) | 8 | INFEASIBLE 218 s | **INFEASIBLE 98 s** |
| 5446 | 21 | UNKNOWN | **INFEASIBLE 222 s** |
| 4889 | 40 | UNKNOWN | **INFEASIBLE 228 s** |
| 1395 | 36 | **INFEASIBLE 320 s** | UNKNOWN |
| 7023 | 6 100 | UNKNOWN | **INFEASIBLE 512 s** |
| 5128 | 5 | UNKNOWN | UNKNOWN |
| 4192, 4491 | 79, 92 | UNKNOWN | UNKNOWN |
| 6947, 7320, 7377, 7470, 7520, 8650 | 751 à 37 709 | UNKNOWN | UNKNOWN |
| 3744 (dim 6) | > 19 965, énumération incomplète en 272 s en local | en cours | – |

- **Bilan : 7 des 16 gabarits durs sont fermés**, et le témoin passe de 521 s à 98 s. Il en reste 9.
- Un petit nombre de Gram ne suffit pas : 5128 n'en a que 5 et résiste.
- La variante « full » est la plus forte. « anchors » ferme seule 1395, et les deux se complètent.

## Lecture

- La positivité de R est l'ingrédient qui manquait au modèle exact. Imposée par une table finie, elle ferme une
  bonne partie du noyau dur.
- Le gain de « full » sur « anchors » montre que le solveur ne relie pas lui-même les entrées hors ancres au bloc
  d'ancres. CR = 0 n'est pas propagé sous forme agrégée. La variante `crzero` de `gram_cover_ablation.py` teste ce
  point seul, sans table.

## Suite lancée

- **c3ga** : 2ᵉ passe sur les 5 988 gabarits ouverts après la 1ʳᵉ passe. Pour chacun : énumération (≤ 900 s), modèle
  exact + table « full » (600 s), contrôle croisé de Codex (≤ 300 s). Spot m7a.32xlarge, 120 workers.
- **gc2a** : pourquoi ça meurt.
  - Ablations (all / nobudget / nouniv / notri / core / notable / crzero) sur 3581, 4801, 4861 et 4378.
  - Découpage Gram par Gram (une table d'une seule ligne par branche) sur 5128, 4192 et 4491.
