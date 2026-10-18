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

## Pourquoi ça meurt : run gc2a (ablations et découpage Gram par Gram)

**Ablations** (`gram_cover_ablation.py`). Chaque variante est un sous-modèle, donc une mort y vaut pour le modèle
complet.

| Gabarit | all | nobudget | nouniv | notri | core | crzero (sans table) |
|---|---|---|---|---|---|---|
| 3581 | 21 s | 20 s | 20 s | 12 s | **12 s** | en cours |
| 4378 | 117 s | 67 s | 47 s | 95 s | **70 s** | en cours |
| 4801 | 46 s | 45 s | 105 s | 41 s | **48 s** | en cours |
| 4861 | 87 s | 83 s | 32 s | 22 s | en cours | **57 s, SANS table** |

Toutes les cellules chiffrées sont INFEASIBLE.

- **Lemme de fait 1.** Le budget, les coupes universelles et les triangles ne sont pas nécessaires. Le cœur exact
  (C1/C2 + équations de composantes + définitions de R) et la liste des Gram positifs suffisent : aucune structure à
  84 étiquettes ne réalise un Gram permis.
- **Lemme de fait 2.** Pour 4861, les seules identités linéaires CR = 0, écrites sur les arêtes, suffisent sans
  table. Le modèle de base restait UNKNOWN à 600 s. Ce sont des conséquences prouvées (Tσ = 0, audit §3 point 5) que
  le solveur ne déduisait pas de lui-même : elles sont maintenant ajoutées au découpage par Gram
  (`gram_cover_split.py`).

**Gram par Gram** : une table d'une seule ligne, toutes les entrées r_ij fixées, 300 s.

- 4192 (79 Gram) : 69 INFEASIBLE sur 75 faits (médiane 23 s), 6 UNKNOWN (Gram 7, 17, 34, 35, 38, 46). La table des
  79 réunis restait UNKNOWN à 600 s : branchement par Gram ≫ table unique.
- 4491 (92 Gram) : les 4 premiers sont INFEASIBLE (19 à 68 s).
- 5128 (5 Gram) : Gram 4 INFEASIBLE (206 s) ; Gram 0 à 3 UNKNOWN à 300 s.
- Les Gram durs (5128 : 0 à 3 ; 4192 : 7, 17, 34, 35, 38, 46) sont tous de rang maximal 5 = dim ker C. Le relèvement
  de noyau de Codex (Rv = 0 ⟹ Hv = 0, car HᵀH = 7R) n'y ajoute donc rien.
- Piste pour eux : l'identité exacte Σ_w h_w h_wᵀ = 7R sur les 84 étiquettes (H = TP, T² = 7T), avec les tables de
  signatures par sommet. Codex la prend en charge sur 5128 (bundle `gram_covers/template_05128_bundle.json`).

## La vraie raison de mort des Gram durs : l'identité de moments HᵀH = 7R (18/10, soirée)

**Énoncé.** On pose H = TP. C'est une matrice 84 × m, dont la ligne h_w est la signature de l'étiquette w :
h_{w,f} = base − |N(w) ∩ Q_f|, avec base = 2, 0 ou 1. Comme T² = 7T :

  Σ_{w parmi les 84 étiquettes} h_w h_wᵀ = 7R   (exact).

**Ce que chaque rectangle Q impose à ses 4 coins.** Une réalisation de Q est un graphe de coins et 4 signatures.
Elle est permise si :
- les signatures sont entières et dans les bornes [0,2], [−2,0], [−3,1] (λ = 1 et μ = 2 aux lettres) ;
- chaque signature vérifie h ∈ im R et hᵀR⁺h ≤ T_ww = 5/2 ;
- les 4 signatures ont pour somme la colonne R e_Q, ou 0 si Q est une grille ;
- le complément de Schur T_QQ − H_Q R⁺ H_Qᵀ est ⪰ 0 ;
- chaque coin est voisin d'au plus un coin portant une lettre mate donnée.

On note M_Q = Σ_{w∈Q} h_w h_wᵀ le moment de la réalisation.

**Les tests.** Il faut Σ_Q M_Q = 7R. Les bornes sont faites en entiers :
- bornes par paire : Σ_Q min ≤ 7R_ef ≤ Σ_Q max ;
- design exact : choisir une réalisation par rectangle avec Σ_Q M_Q = 7R pour toutes les paires (petit CP-SAT) ;
- côté Codex, des combinaisons linéaires de moments (LP), recalculées en entiers.

**Résultats sur les gabarits durs** :

| Gabarit | Codex (`root_component_corner_moment_bounds`, 63e87d62 / 80556dc3) | LAB (`moment_bounds.py`, réécrit de zéro) |
|---|---|---|
| 5128 (5 Gram) | 5/5 exclus, une seule paire ((0,3),(0,4)) : max −44, −45, −37, −36, −39 contre des cibles −42, −42, −35, −35, −35 | 5/5 exclus : mêmes nombres sur cette paire (Gram 0, 2, 3, 4), Gram 1 par ((0,3),(0,3)) avec 56 < 58 |
| 4192 (79 Gram) | 79/79 : 58 sans coins, 16 moments simples, 5 combinaisons (18, 25, 35, 38, 39) | mêmes 74 par les bornes, mêmes 5 survivants, puis 5/5 par le design exact (≈ 2 s chacun) |

- Les deux méthodes et les deux codes sont indépendants, et leurs conclusions concordent Gram par Gram.
- La méthode à retenir : la somme des maxima locaux (par rectangle) est plus petite que le moment global exigé 7R.
- Les 21 tables sont toutes non vides sur 5128 : c'est l'assemblage global qui échoue, pas un rectangle seul.

## RÉTRACTATION (18/10, ~20 h) : les verdicts du modèle sans Gram étaient un artefact

**Tous les verdicts INFEASIBLE de `gram_free_moment.py` et de `local_moment_test.py` produits avant la correction
sont nuls.** Aucun n'avait été compté comme exclusion, et le run gfm1 n'a jamais été lancé.

**Cause.**
- Les bornes des variables produits étaient lues par `var.proto.domain[-1]`.
- Dans OR-Tools 9.15, l'indexation négative de ces champs pybind renvoie 0 ; `d[1]` et `list(d)` sont justes.
- Les domaines des produits étaient donc trop étroits, et le modèle sur-contraint.
- Codex connaissait ce piège : test de régression `root_component_domain_regression.py`, commentaires dans
  `root_component_rotated_gram.py` et `conway_linear_explanation.py`. Ses lectures matérialisent toujours `list(...)`.

**Comment on l'a trouvé.** Un contrôle positif au niveau CP, conseillé par Codex : `srg243_cp_control.py`, le même
encodage porté à k = 22, sur le vrai srg(243,22,1,2), adjacences fixées.
- Avant correction : INFEASIBLE. Pourtant, toutes les contraintes évaluées en Python (degrés, quotas, bornes, 1 540
  identités) sont vraies.
- Après correction (bornes gardées en Python, aucune lecture du proto) : OPTIMAL, comme il se doit.

**Après correction.**
- 5128 et 3744 sont UNKNOWN à 90 s, comme avec l'encodage de Codex (`root_component_neighbor_moments`, 52d7d465).
- L'identité reste juste et l'implication logique entre les deux encodages aussi (Codex, message reçu) : c'est
  seulement un renforcement ordinaire, sans plus.

**Ce qui n'est pas touché** (vérifié par grep : aucune lecture de domaine) :
- les tables de Gram (`gram_cover_branch.py`, `add_gram_table` de Codex) ;
- le découpage par Gram (`gram_cover_split.py`) ;
- les tests de moments par Gram (`moment_bounds.py`, `codex_moment_batch.py`) ;
- les énumérateurs de couvertures.

**Leçon retenue.** Tout nouvel encodage passe un contrôle positif CP sur un vrai graphe avant le moindre verdict.

## Le modèle sans Gram (18/10, 19 h) : l'identité de moments écrite sur les arêtes — VERDICTS RÉTRACTÉS, voir ci-dessus

**Statut : les résultats ci-dessous sont NULS (bug de lecture des domaines), conservés seulement pour la trace.**

**Construction** (`gram_free_moment.py`). On part du modèle exact de Codex : tous couplages libres, budget 51, coupes
universelles, triangles, et on ajoute CR = 0. Puis :
- pour chacune des 84 étiquettes w et chaque rectangle non-grille f : h_{w,f} = base − |N(w) ∩ Q_f| ;
  - la base vaut 2, 0 ou 1 selon le cas (rectangle de w, une droite commune, aucune) ;
  - les bornes [0,2], [−2,0], [−3,1] découlent directement des quotas de lettres du modèle de Codex : le nombre de
    voisines contenant la lettre r vaut 2 − [r ∈ w] − [r^1 ∈ w] ;
- pour chaque paire e ≤ f : Σ_w h_{w,e} h_{w,f} = 7 r_ef (produits CP-SAT).

**Pourquoi c'est juste, et pourquoi ça manquait.**
- L'identité vient de H = TP et T² = 7T (audit §3).
- Codex en a donné la lecture élémentaire : pour un rectangle Q, avec z_w = |N(w) ∩ Q|, les six contraintes C2 des
  paires de coins de Q donnent Σ_w C(z_w, 2) + e(Q) = 8. Avec Σ_w z_w = 48 et Σ_{droite commune} z_w = 16 − 4e, on
  retrouve Σ_w h_{w,Q}² = 7(8 − 2e).
- Hors diagonale, ce sont de même des sommes de C1/C2 sur les paires (u ∈ Q, v ∈ Q').
- L'identité est donc une **agrégation des contraintes du modèle lui-même** : elle ne retire aucune solution.
  CP-SAT ne forme pas ces sommes quadratiques par sommet ; écrites explicitement, elles propagent.

**Contrôles.**
- Contrôle positif de la dérivation sur un vrai srg(243,22,1,2) (`srg243_moment_check.py`, deux racines, entiers
  exacts) : TBᵀ = 0, T² = 9T, HᵀH = 9R, h = base − |N(w) ∩ Q_f| sur toutes les entrées, bornes vérifiées. Les
  constantes générales (c1, c2, c3) redonnent exactement la formule de T de l'audit à k = 14.
- graph[w][w] = 0 dans `build_global` (constante).
- 5128 : la seule paire diagonale (0,0) suffit, avec ou sans presolve (sans presolve : 321 branches, 1 conflit).
  Sans les bornes, une seule paire reste UNKNOWN ; les bornes seules restent UNKNOWN.

**Résultats locaux** (INFEASIBLE en presolve, < 2 s chacun) :
- c3 : 5128, 4491 ; 3744, 2744, 2751, 3665 (dimension 6, couverture de Gram inénumérable) ; 6, 459, 864, 877, 993,
  1084 (UNKNOWN à la 2ᵉ passe) ;
- **c = 2** : 6 gabarits tirés au hasard dans le recensement (dimension 4 à 6). 5 meurent en presolve, le 6ᵉ dès la
  propagation de Codex.

**Lancé** : gfm1, le modèle sans Gram sur les 10 052 gabarits c3 (y compris les 3 574 déjà exclus, comme contrôle de
cohérence), plus un échantillon stratifié de 419 gabarits c = 1 et c = 2 (25 par famille (c, k)).

## 1ʳᵉ passe c3 : bilan final (c3oa + c3ob)

- 10 052 gabarits ouverts après le Gram : **3 574 exclus** par l'étoile complète à 60 s par représentant d'orbite ;
  6 478 ouverts.

## 2ᵉ passe c3 (c3ga) : premiers résultats

- 118 premiers gabarits finis : **118 INFEASIBLE**. Pour les 118, le contrôle croisé par `enumerate_grams` de
  Codex donne LAB_COVER_CONFIRMED.
- Médiane de 46 s CPU pour le modèle avec table.
- Les premiers finis sont les plus faciles : le taux final sera plus bas.

## Suite lancée

- **c3ga** : 2ᵉ passe sur les 5 988 gabarits ouverts après la 1ʳᵉ passe. Pour chacun : énumération (≤ 900 s), modèle
  exact + table « full » (600 s), contrôle croisé de Codex (≤ 300 s). Spot m7a.32xlarge, 120 workers.
- **gc2a** : pourquoi ça meurt.
  - Ablations (all / nobudget / nouniv / notri / core / notable / crzero) sur 3581, 4801, 4861 et 4378.
  - Découpage Gram par Gram (une table d'une seule ligne par branche) sur 5128, 4192 et 4491.
