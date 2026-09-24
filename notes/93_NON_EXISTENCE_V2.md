# 93 — Retour à la non-existence, nouvelle posture (2026-09-24/25, nuit)

*Consigne : supposer que Γ n'existe pas et chercher l'invariant manquant ; pas de construction, pas de gros calcul,
pas d'agents. Prompt de travail rédigé par ChatGPT (sans tout le contexte), lu avec recul.*

## 0. Le cadrage « six unités de torsion » est trompeur
P = 1386 − Σ|W|/6 et L16 donne Σ|W| ≥ 1410. Conclure demande Σ|W| ≤ 1404, c'est-à-dire une **borne supérieure sur la
torsion**, alors que nous n'en avons aucune (seulement Σ|W| ≤ 8316, torsion maximale). L'écart n'est pas 6 : il sépare
« on sait que la torsion est ≥ 1410 » de « il faudrait qu'elle soit ≤ 1404 », et rien de connu ne majore la torsion.

## 1. Programme B (second moment de Δ) : échec expliqué
Sur E₋₄, Δ est positive de rang ≤ 44 et tr = (4n₃ − S)/7 est linéaire en la torsion. Cauchy–Schwarz donne
(4n₃ − S)²/49 ≤ 44‖E₋₄ΔE₋₄‖² ≤ 44‖Δ‖²_F. Mais ‖Δ‖²_F contient Σ_{arêtes} (Z − t(L))², de l'ordre de Σ_L t(L)², qui est
*quadratique* en la torsion. Linéaire² contre quadratique : aucune majoration de la torsion ne peut sortir de ce
moment, quel que soit le rang. Même conclusion pour λ_max : la trace de Δ se répartit sur 44 directions, avec une valeur
propre moyenne ≈ 54, loin de ce qu'il faudrait (≤ 7).

## 2. Programmes D/E et « principe de construction à l'envers »
- **F17 naïve est fausse** : le produit cartésien de deux géométries localement μ = 2 en est une (vérifié à la main :
  λ = 1, μ = 2 à distance 2), avec t = t₁ + t₂ + 1. Donc il existe des géométries tordues avec t = 6 sans plan
  d'ordre 6 : (tordue t = 2, 20 sommets) □ H(4,3) (1620 sommets), (tordue t = 3) □ H(3,3), K₃ □ (tordue t = 5,
  93 sommets) = 279 sommets. Dans un produit, la torsion reste confinée aux classes d'un facteur.
- La géométrie t = 3 à 42 sommets (tordue au maximum, « non planaire ») a |Aut| = 672 ; son origine n'est pas
  identifiée (testé : elle n'est PAS la géométrie des triangles orientés non dégénérés du plan de Fano, qui a aussi
  42 sommets et 56 droites). Les autres : 20 sommets, |Aut| = 240 ; 39 sommets, |Aut| = 78 = 2·3·13 (PG(2,3)).
- Il reste une version « torsion uniforme ⇒ plan d'ordre t » non réfutée, mais rien ne force la torsion à être
  uniforme dans Γ : L16 ne donne qu'une moyenne (≥ 14,2 sur 84).

## 3. Programme C : lemme L19 (nouveau) — structure 7-adique de la similitude de torsion
**Cadre.** x sommet, K ⊂ Z⁸⁴ (rang 70, det 2²¹3⁸5⁶, donc **unimodulaire en 7**), H et Σ = Σ_x préservent K,
U = (2H + I)Σ, UᵀU = 49 sur K. k = rank₇((H − 3I)|_K) = α − 14 (L4 : **le même en tout sommet**, pair, 0 ≤ k ≤ 30).
**Énoncé.**
(a) Les diviseurs élémentaires 7-adiques de U sur K sont 1 (k fois), 7 (70 − 2k fois), 49 (k fois).
(b) Toute valeur propre λ de U est un entier algébrique dont tous les conjugués ont module 7. λ/7 est une racine de
    l'unité ssi v_𝔓(λ) = v_𝔓(7) pour tout 𝔓 | 7 (« λ équilibrée »). Le « déficit » Σ_{v(λ)<1} (1 − v(λ)) (valuations
    7-adiques normalisées) est ≤ k. En particulier : au plus k valeurs propres sont des unités 7-adiques, et au plus k
    facteurs quadratiques « rotations irrationnelles » t² − mt + 49 avec 7 ∤ m.
(c) tr U = 2s(x), tr U² = 8e_σ(x) − 602 ; chaque orbite équilibrée contribue un multiple de 7 à tr U et de 49 à tr U².
(d) **Si k = 0** : U = 7V avec V entière, orthogonale et **d'ordre fini** (toutes ses valeurs propres sont des racines
    de l'unité) ; donc σ_x et la réflexion Q = (2H + 1)/7 engendrent un groupe diédral fini sur K⊗Q, et en tout sommet
    **s(x) ≡ 0 (mod 7)** et **e_σ(x) ≡ 14 (mod 49)** (non tordu : e_σ = 504 ≡ 14 ✓).
**Preuve.** (a) U et son adjoint U* (entier, K₇ unimodulaire) vérifient U*U = 49, donc U⁻¹ = U*/49 : les exposants
a_i de la forme de Smith vérifient {−a_i} = {a_i − 2}, d'où a_i ∈ {0, 1, 2}, autant de 0 que de 2 ; le nombre de 0 est
rank₇(U) = rank₇((2H + 1)|_K) = rank₇((H − 3)|_K) = k (Σ inversible, 2H + 1 ≡ 2(H − 3)). (b) Kronecker (entier
algébrique dont tous les conjugués sont de module 1 ⇒ racine de l'unité) et « Newton au-dessus de Hodge » : les
sommes partielles des valuations des valeurs propres dominent max(0, j − k). (c) Calculs déjà faits (notes/90) ; la
somme des racines primitives m-ièmes vaut μ(m). (d) k = 0 ⇒ polygone de Newton = droite de pente 1 ⇒ toutes
équilibrées ; U ≡ 0 (mod 7). ∎
**Portée honnête.** Lien nouveau et rigoureux entre la torsion en chaque sommet et l'invariant 7-adique global k.
Mais pour k ≥ 2 les congruences disparaissent (une seule rotation irrationnelle suffit à ajuster les résidus), et un
Γ « générique » aurait vraisemblablement k maximal (rank₇(A − 3I) = 45, k = 30), où L19 est presque vide. L19 ne
devient tranchant que si l'on sait montrer que k est petit.

## 4. Bilan et choix d'une direction
Les cinq programmes, tels quels, retombent sur la même difficulté : la torsion forte est localement cohérente, et
tous nos outils (positivité, comptage, moments, arithmétique au niveau du genre) la tolèrent. La seule direction où
un invariant *global* rencontre la torsion *sommet par sommet* est L19 : l'entier k = rank₇(A − 3I) − 15 est le même
partout et borne la quantité de « rotation irrationnelle » autorisée en chaque sommet. **Direction retenue : comprendre
k** (le relier à la torsion, ou le borner), car c'est le seul endroit où « diamètre 2 + 99 sommets » (via le
recollement 7-adique global) contraint chaque sommet individuellement.
