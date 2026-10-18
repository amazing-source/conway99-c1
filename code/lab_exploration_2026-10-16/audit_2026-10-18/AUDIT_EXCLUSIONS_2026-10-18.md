# Audit « exclu veut dire exclu » (LAB, 18/10/2026)

Demande de l'utilisateur (18/10, vers 11 h) : « il faut juste s'assurer que tous vos scripts, que ça soit pour c=4,3,2,1,
une fois exclu etc, que ça signifie bien qu'ils sont exclus ».

**Résumé.**
- Le bug OR-Tools trouvé par Codex est confirmé, et il est plus large que `[-1]`.
- Il ne reste aucune lecture fautive dans les deux bases de code.
- Ma chaîne c_min ≥ 3 (gabarits → Gram) tient :
  - lemmes re-démontrés ci-dessous ;
  - filtres recoupés par une implémentation indépendante. Pour k ≥ 8 la vérification est complète, avec 0 faux rejet.
    Pour k ≤ 7, ce n'est qu'un échantillon : 290 093 gabarits étiquetés tirés au hasard par le relecteur, 0 faux rejet.
  - verdicts Gram recoupés par un autre solveur et un autre codage : 0 désaccord sur 22 532 gabarits (k ≥ 8 complets
    plus des échantillons pour k = 3..7), et le relecteur a ajouté k = 1, 2 complets (2 612 gabarits). Cela couvre environ
    4 % des 500 874 exclusions ; les autres (k = 3..7) reposent sur CP-SAT seul. Coût d'une passe complète : environ
    2 heures CPU, non lancée.
- Tout ce qui passait par le code fautif de Codex est retiré. Cela vaut pour les pilotes c3, la campagne AWS c3star v1,
  les préfixes partiels et les gabarits 7, 9 et 19 de c4.
- Le plafond **P ≤ 852 est revérifié** : le recensement indépendant LAB du 08/10 (`census2.py`) a été relancé
  aujourd'hui ; il est identique à celui de Codex ; le certificat a été vérifié exactement sur lui ; le PL a été refait.
  Le détail est au §8. Le nouveau certificat de Codex, 3P + 4G ≤ 2772, est vérifié de la même façon : il exclut le
  gabarit 7 de c4 à la racine de score minimal.
- Sans le budget, ma couverture c ≥ 3 garde 17 gabarits ouverts de plus (k = 13..21) ; elle ne dépend alors plus de
  P ≤ 852.

## 1. Le bug

`audit_2026-10-18/rf_probe.py`, sortie `rf_probe.out`. Version OR-Tools 9.15.6755.

Les champs répétés concernés sont ceux du proto : `domain`, `linear.vars`, `linear.coeffs` et `linear.domain`.

| Opération sur le champ | Résultat |
|---|---|
| `f[-1]` | **0**, sans erreur |
| `f[-2]` | **mémoire non initialisée** (ex. −8 070 175 653 742 845 120), sans erreur |
| `f == liste` | **False**, sans erreur |
| tranches `f[:-1]`, `f[1:]`, `f[::-1]` | TypeError (bruyant, sans danger) |
| `list(f)`, `len`, itération, `min`, `max`, `sorted`, indices positifs | corrects |

**Scan statique** (`rf_scan.py`, sortie `rf_scan.out`) :
- analyse AST de 440 fichiers : tout `code/codex` dans son état actuel et tout mon `work/exploration_2026-10-16` ;
- motifs cherchés : indice négatif, tranche, `==`/`!=` et `reversed`, sur un champ du proto ou sur un nom affecté depuis un
  champ du proto ;
- **aucun cas restant**, hors le test de régression de Codex, qui reproduit le bug exprès ;
- les noms marqués « inspect by hand » ont été lus : ce sont des `len(...)`, des itérations ou des listes déjà copiées ;
- la librairie OR-Tools (`sat/python`) ne contient pas ce motif.

**Portée** : notes de Codex `CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt`, commits ac8921c3 et 8ce2e720, et mon arrêt AWS.
- c4 : 76/79 restent. Les sources de ces 76 n'appellent pas le module fautif (vérification de Codex sur ses sources
  directes, pas un recalcul indépendant).
  - 7, 9 et 19 sont **rouverts**.
  - L'instantané 0421 est inutilisable pour 7 et 9 ; le front valide est 0306.
- c3, méthode de l'étoile complète :
  - les 162 verdicts des 8 pilotes sont **retirés** ;
  - la campagne AWS c3star v1 (code 2c7bdd0b) a été arrêtée par moi, avec les deux machines terminées et 8 508 gabarits
    traités. **Aucune de ses sorties ne compte**, même celles marquées INFEASIBLE (S3 `runs/c3star-v1a`, `runs/c3star-v1b`).
  - Recalcul corrigé (Codex) : g1, gabarit 0, M0 = 0 reste INFEASIBLE, mais en 17,3 s CPU au lieu de moins d'1 s. Le bug
    faisait donc une grande partie du travail : il faudra re-chiffrer la campagne c3.
- Préfixes partiels c ≤ 2 (Codex) : les 5 anciens INFEASIBLE sont **retirés**. Le recalcul du préfixe 33 donne UNKNOWN.
  - Un second défaut de même famille a été vu dans l'arbre de travail de Codex : `six_prisms = not groups[root]` vaut True
    pour une droite inconnue (None) et imposait `== 1` au lieu de `>= 1`.
  - Ce défaut ne touche que le schéma partiel, en préparation (8ce2e720).

## 2. Ce qui tient, branche par branche

| Branche | Énoncé | Statut après audit |
|---|---|---|
| c_min = 4 (Codex) | 79 gabarits à la racine de budget | 76 exclus (verdicts CP-SAT, sans certificat portable, non recalculés par LAB) ; 3 rouverts (7, 9, 19) |
| c_min ≥ 3 (LAB) | gabarits → Gram entier | 510 926 gabarits (k ≤ 12), 500 874 Gram-infaisables, **10 052 ouverts**. Sans le budget : k = 13..21 ajoutent 20 gabarits, dont 3 infaisables, soit **10 069 ouverts**. L'étape d'après (étoile complète) est entièrement à refaire. |
| c_min = 2 exact (LAB) | recensement C++ | k = 12..4 : 0, 6, 59, 609, 4 892, 32 212, 170 144, 732 827, 2 502 807 gabarits (dim ker C jusqu'à 10). k ≤ 3 : plus de 280 s chacun, non fini. Gram partiel antérieur (AWS c21sweep, `cle3_gram`, non touché par le bug) : 1 793 745 gabarits mesurés, 119 452 ouverts. Aucune exclusion de branche. |
| c_min = 1 exact | – | non commencé |

- Le pilote du modèle global de Codex sur 4 gabarits c ≥ 3 à 1 ou 2 grilles (`cle3_global_pilot.py`) donne 2 INFEASIBLE.
  - Ce modèle n'importe pas le module fautif.
  - Ces 2 verdicts ne sont **pas** déduits des 10 052.

## 3. Lemmes de ma chaîne, re-démontrés aujourd'hui

**Notations.**
- Racine v, 7 droites, 14 lettres (voisins), 84 étiquettes (distance 2).
- Q_ij : les 4 étiquettes voisines d'une lettre de i et d'une lettre de j.
- B : incidence lettres × étiquettes ; M : couplage des lettres mates ; Γ : adjacence entre étiquettes.
- T = 3I − Γ − (3BᵀB + BᵀMB − 2J)/8 ; P : indicatrices des Q_ij ; R = PᵀTP.

1. **Structure.**
   - Chaque étiquette a exactement 2 lettres, sur deux droites différentes. C'est μ = 2 avec v ; et une étiquette
     voisine des deux lettres mates a, a* serait, avec v, un second voisin commun de a et a*, contre λ = 1.
   - Les 21 rectangles partitionnent donc les 84 étiquettes.
   - G_l est cubique : chaque étiquette de Q_ij a dans G_{l_i} une lettre et deux étiquettes.
   - Les composantes de G_{l_i} correspondent aux partitions des 6 autres droites. Une composante sur s droites a 6s
     sommets.
   - s = 1 ⟺ prisme ⟺ e(Q) = 4 (grille). L'autre appariement croisé donnerait 3 voisins communs à deux étiquettes non
     adjacentes (vérifié à la main).
2. **TBᵀ = 0.** On utilise λ = 1 et μ = 2 :
   - ΓBᵀ = 2J − Bᵀ − BᵀM ;
   - BBᵀ = 11I + J − M ;
   - donc 3BᵀBBᵀ + BᵀMBBᵀ − 2JBᵀ = 8(4Bᵀ + BᵀM − 2J) = 8(3I − Γ)Bᵀ.
3. **0 ⪯ T ⪯ 7Π et T² = 7T** (Π : projecteur sur ker B).
   - Sur ker B, on a 1ᵀx = 0, car 1 = Bᵀ1/2.
   - On en tire Tx = (3I − Γ)x, et −4 ≤ θ ≤ 3 sur 1^⊥ donne les deux bornes.
   - (0, Tx) = −(A − 3I)(0, x) est un vecteur propre −4, ce qui donne T² = 7T.
4. **Formules de R.**
   - R_ee = 8 − 2e(Q_e).
   - R_ef = −W_ef si e et f partagent une droite ; R_ef = 4 − W_ef s'ils sont disjoints.
   - Ce sont des calculs directs avec B1_Q = 2·(les 4 lettres).
5. **Somme nulle par composante** : σᵀTσ = 12s − 8s − (24s² + 24s + 8s² + 8s − 32s²)/8 = 0. Donc Tσ = 0, d'où CR = 0.
6. **Composantes et bornes.**
   - R_ef = 0 entre deux composantes d'une même droite : G_{l_i} est induit, donc il n'y a aucune arête entre elles.
   - −8 ≤ R_ef ≤ 4, et R_ef ≤ 0 sur une droite partagée ; les mineurs 2×2 viennent de R ⪰ 0.
   - PᵀΠP = 4I − (4/5)C₀ᵀC₀ + (4/15)J = 4·proj(ker C₀), calculé sur im L. D'où R ⪯ 28I et tr R ≤ 28 dim ker C.
7. **E3, e(Q) ≠ 3.**
   - h_Q = (0, T1_Q) est entier, vecteur propre −4, nul sur v et les lettres, de norme 7R_QQ.
   - Si R_QQ = 2, la norme vaut 14. Alors : coordonnées dans {0, ±1}, 7 positives, positives deux à deux non adjacentes,
     aucune lettre commune entre deux positives.
   - Une diagonale de Q est isolée : chaque étiquette a exactement une voisine adjacente à chaque lettre mate.
   - Donc e = 3 force un P4 le long des côtés. Ses bouts (h = 2 − 1 = 1) partagent une lettre : contradiction.
   - Preuve de Codex (MOMENTS §18-19), déjà relue par LAB le 17/10.
8. **Coupes de connexité.**
   - Une composante est cubique, donc toute coupe de ses sommets a une taille paire.
   - Elle est connexe, donc la coupe vaut au moins 1, donc au moins 2. D'où Σ_{e∈U, f∉U} R_ef ≤ −2.
9. **Filtres des gabarits** : P, O′, S′, Z, K de `cle3_templates.py`, conséquences de 4 à 8.
   - O′ : un seul vecteur à la fois ±égal et orthogonal.
   - S′ : « + » contredit R_ef ≤ 0 ; « − » donne une coupe nulle.
   - K : le bloc de la racine i est un laplacien connexe, de rang 6 − c_i.
10. **Racine de budget (facultative depuis aujourd'hui).**
    - t(l) compte les triangles de G_l, et Σ_l t(l) = 2P.
    - Une grille à la racine coûte 4 (deux triangles dans chacune des deux droites).
    - Donc 4k ≤ τ(v) ≤ ⌊6·852/99⌋ = 51, soit k ≤ 12.
    - Ce point dépend de P ≤ 852, revérifié au §8.

## 4. Vérifications indépendantes faites aujourd'hui

| Contrôle | Méthode | Résultat |
|---|---|---|
| Liste des 588 graphes J | Σ 7!/\|Aut\| sur les représentants comparée au décompte brut des 2²¹ graphes étiquetés sans sommet de degré 1 | 1 142 968 = 1 142 968 |
| Filtres P/O′/S′/Z/K (union-find, Python et C++) | `cle3_filter_crosscheck.py` : réécriture par algèbre linéaire exacte (e_e ∓ e_f ∈ espace des lignes de C), avec son propre générateur de partitions et sa propre forme canonique | k = 8..21 complets : **0 faux rejet**. L'algèbre linéaire est plus forte : 9 477 → 4 997 (k = 8), 2 396 → 1 426, 493 → 339, 127 → 93, 26 → 25, 13 → 11. Le rejet de plus testé est aussi Gram-infaisable, comme attendu (ces conditions découlent de CR = 0). |
| Verdicts Gram (CP-SAT et `psd_or_witness`) | `cle3_gram_milp_check.py` : même système réécrit depuis son énoncé, solveur HiGHS (scipy), propre test PSD exact (LDLᵀ en fractions), solutions réalisables re-vérifiées exactement | **22 532 gabarits, 0 désaccord, 0 UNKNOWN**. k = 8..13 complets (12 532), plus 2 000 tirés au hasard (graine fixe) pour chacun de k = 3..7. Les comptes complets redonnent le tableau du recensement (k = 8 : 8 164/1 313 ; k = 9 : 1 829/567 ; k = 10 : 302/191 ; k = 11 : 54/73 ; k = 12 : 4/22). |
| Certificat P ≤ 852 | `p852_identity.py` : relecture des 16 poids (tous ≥ 0) et des 16 expressions de comptes du recensement, en fractions exactes | Σ w_g N_g = 11088/13 − P **exactement**. SHA256 du recensement : a49f811e…a291, le même que celui cité par Codex. |
| Le test PSD de Codex | lecture | Rejet certifié par un vecteur entier vérifié exactement ; acceptation par pivots rationnels exacts |

## 5. Ce qui n'est PAS établi

1. ~~Le recensement d'ordre 9 n'est pas re-dérivé indépendamment.~~ **Levé le jour même**, voir §8.
   - Une re-dérivation indépendante LAB existait déjà (08/10). Elle a été relancée et recomparée aujourd'hui.
   - Ma couverture c ≥ 3 peut aussi s'en passer : 17 gabarits ouverts de plus (k = 13..21, `cpp_census_nobudget/`).
2. **Les verdicts INFEASIBLE sont des verdicts de solveur**, pas des certificats.
   - Deux solveurs concordent, mais seulement sur environ 4 % des exclusions Gram (voir le résumé) ; une passe HiGHS
     complète coûterait environ 2 heures CPU.
   - Les filtres de gabarits ne sont recoupés complètement que pour k ≥ 8. Une vérification complète pour k ≤ 7 demande
     un énumérateur « algèbre linéaire seule », sans élagage par union-find, en code compilé.
   - Il faudrait des certificats (DRAT, ou Farkas sur la dernière relaxation) pour une preuve publiable.
3. **Les 76 exclusions c4 de Codex** ne sont pas recalculées par LAB.
4. **L'étape après le Gram**, celle qui doit tuer les 10 052 (+17) gabarits ouverts, n'a **aucun** verdict valable
   aujourd'hui.

## 6. Gain de vitesse trouvé au passage

- Le filtre par algèbre linéaire retire 34 à 47 % de gabarits de plus que l'union-find, avant le Gram.
- Il ne change pas les ouverts, car le Gram les tue de toute façon. Il réduit en revanche le travail du Gram et la taille
  des fichiers.
- Mesure : le Gram coûte environ 0,006 s CPU par gabarit sur les échantillons, presque tous infaisables.

**Report fait dans `cle_templates.cpp`**, option `--la`.
- Calcul : rang modulo p = 2⁶¹ − 1. Il est exact, car tous les mineurs des matrices en jeu sont inférieurs à 6¹¹ < p.
- Le test n'est appliqué qu'aux représentants, ce qui suffit puisque le verdict est invariant par Aut.

**Validation** :
- sans `--la`, les sorties sont identiques octet par octet à la version précédente (k = 8..13) ;
- avec `--la`, les ensembles de survivants sont identiques à ceux du vérificateur Python en fractions, pour k = 8..21 ;
- le compteur « LA_zero », qui ne doit jamais servir, est resté à 0.

**Effet sur c_min = 2 exact** (`cpp_census_la/`) :

| k | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sans `--la` | 0 | 6 | 59 | 609 | 4 892 | 32 212 | 170 144 | 732 827 | 2 502 807 |
| avec `--la` | 0 | 5 | 42 | 411 | 3 091 | 19 984 | 103 151 | 431 264 | 1 445 038 |

- Pour k = 4, le calcul prend 160 s.
- Pour k = 3, chacun des deux premiers graphes dépasse 140 s. La suite (k = 3..0, puis c_min = 1) demande un découpage
  `--graph` et `--fix`, sur plus de 5 minutes au total.

## 7. Fichiers

**Dans `audit_2026-10-18/`** :
- `rf_probe.py` et `rf_probe.out` ;
- `rf_scan.py` et `rf_scan.out` ;
- `p852_identity.py` et `p852_identity.out`.

**Scripts, dans `work/exploration_2026-10-16/`** :
- `cle_templates.cpp` (énumérateur C++) ;
- `cle3_gram_jsonl.py` ;
- `cle3_filter_crosscheck.py` ;
- `cle3_gram_milp_check.py` ;
- `compare_gram_verdicts.py`.

**Données** :
- `cpp_census/` : comptes c_min = 3 et 2 ;
- `cpp_census_nobudget/` : gabarits k = 9..21, verdicts des deux solveurs, journal des filtres, échantillons compressés
  k = 3..8 ;
- `cpp_census_la/` : recensement c_min = 2 avec `--la`, et validation de `--la` à c_min ≥ 3 ;
- `audit_2026-10-18/census/` : relances du recensement indépendant et contrôles des certificats (§8).

## 8. Le plafond P ≤ 852, revérifié (demande de l'utilisateur, 18/10 vers 12 h 30)

> « bah le plafond, levez juste le doute avec codex et reverifiez le rigoureusement vous pourriez meme peut etre en
> extraire quelque chose de nouveau avec vos nouveaux lemmes et travaux »

**Source indépendante.** Codex l'a signalée (message du 18/10) et je l'ai vérifiée.
- `census2.py` : LAB, 08/10, `work/c1_theta_lp_2026-10-07/` et `code/lab_theta_lp_2026-10-08/` (commit e317a1b6).
- Il a été écrit sans le code de Codex.
- Méthode : récurrence sur les identités de double comptage, pas d'élimination. Seules les deux bornes de voisins communs
  définissent les types admissibles ; Codex a confirmé que son générateur n'utilise rien d'autre.
- Il avait déjà été recoupé le 08/10 sur deux graphes réels srg(243,22,1,2), par comptage d'embeddings induits :
  - bvls243 : 173 types d'ordre ≤ 8 et 40 types d'ordre 9 égaux aux prédictions ;
  - twin243 : 276 types égaux aux prédictions.
- Limite : ces graphes réels ne testent que les coefficients des paramètres non nuls chez eux.

**Relancé aujourd'hui** (`census/`, empreintes `census2_sources.sha256`) :

| Contrôle | Résultat |
|---|---|
| `census2.py census 9 99 14` | 27 s ; types par ordre 2, 4, 9, 21, 62, 208, 916, 5 311 ; les comptes somment à C(99, n) identiquement |
| `compare_census.py` contre `codex_census_validation_99.json` | 6 533 formules, 57 paramètres appariés, **0 désaccord** (`compare_census_99_today.out`) |
| Certificat de Codex (16 poids ≥ 0) évalué sur la famille census2 | Σ w_H N_H = 11088/13 − P **exactement** (`p852_recheck.json`) |
| PL refait par LAB (HiGHS sur la famille census2, ordre 9) | max P = 852,923 ; certificat dual rationalisé et vérifié exactement : 11088/13 |

**Pourquoi c'est une preuve.**
- Tout vecteur de comptes d'un srg(99,14,1,2) vérifie toutes les identités de double comptage.
- Il est donc dans la famille census2, qui n'impose qu'une identité par type. Les N_H y sont ≥ 0.
- Une combinaison à poids ≥ 0 égale identiquement à 11088/13 − P donne P ≤ 852.

**Essai E3, la piste suggérée par l'utilisateur.**
- La configuration racine + deux droites + rectangle à 3 arêtes est un graphe à 9 sommets. Dans un srg(99,14,1,2), tout
  9-ensemble induit de ce type EST une telle configuration, car μ(x, y) = 2 force les 4 étiquettes.
- Ses 4 placements (P4 le long des côtés) forment un seul type ; les placements avec diagonale sont déjà non admissibles
  localement.
- On impose N = 0 pour ce type. Le PL d'ordre 9 reste à **852,923** : E3 n'apporte rien à l'ordre 9.
- À l'ordre 10, on interdit aussi toutes les extensions du type E3. Le recensement d'ordre 10 a été reconstruit (287 s),
  mais le PL n'a pas fini sous 5 minutes. Non conclu ; à relancer quand le PC est libre.

**Nouveau certificat de Codex (18/10), vérifié exactement sur census2** (`grid_bound_recheck.py`) :
- 12 comptes d'ordre 9 à poids ≥ 0 somment à 924 − P − (4/3)G, où G est le nombre de grilles 3×3. Donc
  **3P + 4G ≤ 2772** dans tout srg(99,14,1,2).
- Double comptage, vérifié à la main :
  - Σ_x s(x) = 6P et Σ_x g(x) = 9G, avec s = Σ t(l) sur les droites de x et g le nombre de paires-grilles en x ;
  - en effet, chaque grille donne exactement une paire-grille à chacun de ses 9 sommets, et une grille 3×3 est toujours
    induite (une diagonale donnerait 2 voisins communs à deux sommets adjacents).
  - Donc Σ_x (9s + 8g) = 18(3P + 4G) ≤ 99·504, et un sommet x a 9s(x) + 8g(x) ≤ 504.
- Sous c ≥ 4 global, on a g ≥ 7 : le degré non-grille est au plus 4 partout, donc au plus 14 non-grilles. Alors s ≤ 49,
  et la couverture 51 s'applique à ce sommet.
- Le gabarit 7 (g = 12, s ≥ 48) donne 9s + 8g ≥ 528 > 504. Il est donc **exclu à la racine de score minimal**.
- Il reste 9 et 19, chez Codex.
- Ce choix de racine ne se cumule pas avec un autre choix minimal.

## 9. Relecture indépendante (agent relecteur, contexte neuf, 18/10)

**Verdict** : aucune exclusion fausse et aucune contrainte cachée en trop ; les §3 et `cle3_gram.py` sont justes.

**Formulations trop fortes**, corrigées ci-dessus :
- couverture des filtres limitée à k ≥ 8 ;
- couverture HiGHS d'environ 4 % ;
- « 3 voisins communs » corrigé en λ = 1.

**Contrôles ajoutés par le relecteur** :
- k = 1, 2 complets : 2 612 gabarits, verdicts anciens = CP-SAT = HiGHS, soit 2 587 infaisables et 25 ouverts ;
- 290 093 gabarits étiquetés tirés au hasard pour k = 1..7 : 0 faux rejet ;
- les 541 sorties AWS redonnent 510 926 / 500 874 / 10 052, avec 0 UNKNOWN, et concordent gabarit par gabarit avec ces
  recalculs ;
- le scan récursif des deux bases ne trouve que des lectures `domain[0]` ou `domain[1]`.
