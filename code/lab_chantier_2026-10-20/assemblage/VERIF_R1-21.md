# VERIF R1-21 — x₅₈ = x₅₉ = 0 par le lemme de variance, sans les certificats de Codex

Vérificateur adverse, contexte neuf, 20/10/2026. Lecture seule. Scripts du scratchpad de la session : `check_r1_21.py` et
`count_dense10.py`. Le second lit `census2_99_order10_today.json` (18/10, 60 Mo), en un processus, en moins d'une
minute et sous 1 Go.

## Verdict : DÉJÀ CONNUE (et l'énoncé tient, statut P)

L'énoncé « x₅₈ = x₅₉ = 0 dans tout srg(99,14,1,2) » est vrai sans aucun certificat. Le lemme de variance l'impliquait
dès le 25/09, soit deux semaines avant que L06-107 (08/10) le fasse dépendre des 63 + 136 cœurs exclus de Codex. Il
n'a aucun effet sur les comptages (NOTE 17.71 : « NO EFFECT »).

## 1. Ce que sont x₅₈ et x₅₉

- **Source.** `work/c1_theta_lp_2026-10-07/NOTE.md:2756-2759` (17.71, 08/10, 22:54 UTC) : « two 4-regular graphs on 10
  vertices (20 edges), which are census parameters: x_58 = x_59 = 0 in every srg(99,14,1,2), given Codex's certificates
  for the 63 + 136 excluded cores ».
- **Paramètres du recensement** (`census2.py`, docstring l. 1-20). Les types de degré minimum ≥ 3 sont laissés comme
  paramètres, sous la forme de leurs comptes induits non étiquetés N_H. Le JSON d'ordre 10 stocke les comptes de
  plongements x_H = N_H·|Aut H|.
- **Les deux types** (`core_forbidden_types.json`) :
  - type « form {"59": "10"} » : lignes [30, 169, 209, 323, 549, 594, 300, 774, 712, 432] ;
  - type « form {"58": "16"} » : lignes [30, 101, 387, 673, 833, 330, 178, 588, 564, 408].
- **Décodage** (`check_r1_21.py`). Les deux matrices sont symétriques et sans boucle. Les deux graphes sont
  **4-réguliers, avec 10 sommets et 20 arêtes**, et ont respectivement 5 et 4 triangles.
- **Conséquence.** Le nombre de copies induites de chacun vaut 10·x₅₉ ou 16·x₅₈. Donc x₅₈ = 0 et x₅₉ = 0 si et
  seulement si aucun de ces deux graphes n'est induit. C'est bien ce que dit R1 (point 7 de sa liste, R1:181).

## 2. Le lemme de variance, à la source et refait

- **Énoncé à la source.** `conway99-c1`, `origin/main:notes/94_NUIT_LITTERATURE.md:62-66` (nuit du 24 au 25/09, commit
  a6e8087) :
  > « Lemme de variance. Pour F induit (N sommets, degrés d_i), x_j = nombre de sommets hors de F ayant j voisins dans
  > F : x₀ + Σ_{j≥3} C(j−1, 2)·x_j = c(F) ≥ 0 [...] c(F) = 99 + N(N − 16) − ½ Σ d_i(d_i − 2) [...] tout graphe
  > 4-régulier induit à 10 sommets aurait c = −1, il est donc interdit. »
- **Attention, piège de notation.** Ces x_j-là comptent des sommets extérieurs. Ils n'ont rien à voir avec les paramètres
  x₅₈ et x₅₉ du recensement.
- **Redérivation.** Soit n_j le nombre de sommets hors de F ayant j voisins dans F, et e le nombre d'arêtes de F.
  - Σ n_j = 99 − N.
  - Σ j·n_j = 14N − 2e.
  - Σ j(j−1)·n_j = Σ_{u≠v ordonnés} (λ ou μ) − Σ_w d_w(d_w − 1) = 2N(N − 1) − Σ d², avec λ = 1 et μ = 2.
  - Donc Σ (j−1)(j−2)·n_j = 2N² − 32N + 198 − Σ d(d − 2).
  - Or (j−1)(j−2) vaut 2 pour j = 0, 0 pour j = 1 et 2, et 2·C(j−1, 2) pour j ≥ 3.
  - D'où n₀ + Σ_{j≥3} C(j−1, 2)·n_j = 99 + N(N − 16) − ½ Σ d(d − 2) = c(F) ≥ 0. ∎
- **Application.** Pour N = 10 et F 4-régulier : c = 99 − 60 − 40 = −1 < 0. Contradiction.
- **Plus fort.** Sur toutes les suites de degrés à 10 sommets et 20 arêtes, le maximum de c(F) vaut −1 (énumération
  exhaustive). Donc **tout 10-ensemble induit a au plus 19 arêtes**. À 19 arêtes, le maximum de c vaut 4, sans
  contradiction.
- **Confirmation indépendante.** NOTE_NIGHT 17.5 (`work/c1_night_2026-10-14/NOTE_NIGHT.md:310-313`, 14/10) obtient
  e(S) ≤ 19 pour s = 10 par la norme de f_S = 7E·1_S. Recalcul : (210 + 700/9 − 88/9)/14 = 139/7, donc e ≤ 19.

## 3. Portée exacte dans le recensement

- Dans `census2_99_order10_today.json`, l'ordre 10 compte 42 430 types admissibles (λ ≤ 1 et μ ≤ 2 à l'intérieur).
  **Exactement 2 ont au moins 20 arêtes, et ce sont x₅₈ et x₅₉** (formes à un seul terme).
- Le lemme de variance donne donc exactement x₅₈ = x₅₉ = 0 à l'ordre 10, et rien de plus.
- Le recensement ne l'imposait pas, puisque ces deux types y sont « admissibles ».

## 4. Chaîne réécrite

1. **(P, note 94, 25/09 ; redérivé ici.)** Dans un srg(99,14,1,2), tout sous-graphe induit F vérifie c(F) ≥ 0.
2. **(Calcul exact ici.)** Un sous-graphe à 10 sommets et 20 arêtes a c(F) ≤ −1. Il est donc absent.
3. **(C, décodage ici.)** x₅₈ et x₅₉ comptent deux graphes 4-réguliers à 10 sommets et 20 arêtes.
4. **Conclusion (P).** x₅₈ = x₅₉ = 0. Les certificats de Codex ne sont pas nécessaires.

## 5. Redécouverte

- **25/09.** Note 94, l. 66 : l'interdiction explicite de tout graphe 4-régulier induit à 10 sommets.
- **08/10.** NOTE 17.71 et pont #416-417 : le même fait, retrouvé de façon conditionnelle, par les 174 cœurs. C'est une
  preuve plus faible.
- **14/10.** NOTE_NIGHT 17.5 : e(S) ≤ 19 pour s = 10.
- **Effet.** Le statut de L06-107 / COND-42 peut passer de E (conditionnel) à P (preuve à la main indépendante).

## 6. Ce qui manquerait

Rien pour ce point. Le fait n'a aucun effet connu, puisque l'injection dans le programme linéaire du rang 37 ne change
rien (17.71). Une obstruction de ce type demanderait des motifs d'ordre ≥ 11, comme l'écrit 17.71.
