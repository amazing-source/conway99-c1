# 120 — Vecteurs propres cellulaires forcés ; triades de doubles au Fano tendu

*26/09, après-midi. Mathématiques pures. DÉRIVÉ = preuve écrite. Relectures : « structures » a refait le §1 à la main.
Le §2 vient de la transposition du Théorème F de C2 (carnet C2 §16), qui a transmis son énoncé et sa preuve. Les
prémisses du §2 ont été contrôlées sur 9 configurations tendues (0 écart) ; aucun solveur.*

## 0. Résumé
| résultat | statut |
|---|---|
| en tout sommet, au moins 5 fonctions constantes sur les cellules sont vecteurs propres de A_Δ pour 3 | DÉRIVÉ (dimension), refait par « structures » |
| mod 7 : au moins 35 − k ≥ 7 fonctions cellulaires annulées par A_Δ − 3 | DÉRIVÉ (avec L19 et L22) |
| au Fano tendu, les doubles d'un bloc viennent tous de ses deux blocs parallèles (même troisième point) | DÉRIVÉ (lemme 1 de S21) |
| **triades** : les types cerise/antipode entre blocs parallèles obéissent à des règles rigides (cas A ou B) | DÉRIVÉ |
| contradiction au Fano tendu par les triades | **non obtenue** (le budget de C2, qui vaut 4 − 2n_s, vaut 8 en C1 et y est saturé) |

## 1. Vecteurs propres cellulaires forcés
- **Cadre.** K = ker∂ ∩ Z⁸⁴ (rang 70), H = A_Δ|_K. Sur K ⊗ Q, K = V₃ ⊕ V₋₄, de dimensions 40 et 30.
  - La trace est nulle, d'où 3m₃ − 4m₋₄ = 0 ; « structures » l'a revérifié par B·N = N(J − P − I).
- **Sous-réseau cellulaire.** K_cell = {f ∈ K : f constante sur chacune des 42 cellules}.
  - Son rang est 35 : 14 pour la partie E₋₂ des blocs, 21 pour les ε_R. Les sommes par paire de ∂f ne dépendent que
    des blocs.
- **Énoncé (Q).** dim(K_cell ∩ V₃) ≥ 35 + 40 − 70 = **5**.
  - En tout sommet x de tout srg(99,14,1,2), il existe au moins 5 fonctions f = F(cellule), linéairement
    indépendantes, telles que Σ_C F(C)·c_z(C) = 3F(cellule de z) pour chacune des 84 paires z.
  - Ce sont des vecteurs propres de Γ pour 3, nuls sur B₁(x) et constants sur chaque cellule.
- **Énoncé (mod 7).** Les deux valeurs propres sont ≡ 3 (mod 7), et rank₇((H − 3)|_K) = k ≤ 28 (L19, L22).
  - Comme K_cell est saturé dans K : dim(ker₇(H − 3) ∩ K_cell/7) ≥ 35 − k ≥ **7**.
- **Portée.**
  - La condition est **non linéaire** en les comptes de cellules, puisque F est inconnu : les PL par types ne la voient
    pas.
  - Forme matricielle (« structures ») : M(δ) = [M_β | M_γ(δ)] (84 × 35) doit être de rang ≤ 30 sur Q.
  - Au Fano tendu, M_β est connue ; son rang au témoin est en cours de calcul exact (contrôle, pas solveur).
  - Si l'on trouvait un sous-réseau V ⊂ K de rang ≥ 30 sur lequel H − 3 est injective mod 7, on aurait k ≥ 30, ce qui
    contredit L22.

## 2. Au Fano tendu : triades de doubles
**Triade.** T_M = les 3 blocs X, Y, Z de même troisième point M (7 triades, qui partitionnent les 21 blocs).
- Par le lemme 1 (S21), une paire x ∈ X a exactement 2 voisins dans Y et 2 dans Z, et au plus 1 dans tout autre
  bloc. Il n'y a aucun double spécial, car τ tombe dans les blocs {x_i, M} et σ hors de la droite.
- Le budget du bloc Y vaut exactement 4 **cerises** et 4 **antipodes**, et il vient en entier de X et de Z :
  - une cerise est le voisin commun (hors l) de {l,m₀} et {l,m₁}, une par étiquette l de Y ;
  - un antipode est un voisin commun d'une paire antipodale de Y, deux par paire.
- Chaque x a ses deux atterrissages σ l'un dans les classes de Y, l'autre dans celles de Z. En effet {a,b} ∈ M_{x₁}
  ∪ M_{x₂} est une paire transverse de C4 = Y ∪ Z. L'étiquette touchée λ_x^Y a le degré générique 1 dans G_x : **une
  cerise de x en λ_x^Y est impossible.**

**Types.** T(X→Y) désigne le multi-ensemble des types des doubles des 4 paires de X dans Y. Chaque y a 2 voisins dans X,
ce qui ne laisse que trois cas :
- (i) 4 antipodes (2 A, 2 B) ;
- (iv) 4 cerises, une par étiquette de Y ;
- (m) 2 cerises aux deux étiquettes d'une même classe de Y, plus 1 A et 1 B.

**Règles**, toutes par λ = 1 et μ = 2.
- **R1.** T(X→Y) = (i) ⟺ T(Y→X) = (i). Une paire antipodale a exactement 2 voisins communs, ce qui force les 4
  antipodes de X à se grouper par paires. Ces paires ont alors 2 voisins communs dans Y ; ce ne sont donc pas des
  cerises, qui n'en ont qu'un.
- **R2.** Si T(X→Y) ∈ {(iv), (m)}, les doubles de Y dans X sont les 4 paires croisées d'une partition {x₁,x₂} | {x₃,x₄}.
  On obtient (iv) si {x₁,x₂} est antipodale, et (m) si c'est une cerise.
- **Budget.** {T(Y→X), T(Z→X)} = {(i),(iv)} ou {(m),(m)}.

**Deux cas par triade.**
- **A.** X ↔ Y en (i) ; Z → X et Z → Y en (iv) ; X → Z et Y → Z en (m), avec des cerises sur les deux classes
  différentes de Z.
- **B.** Les 6 flèches sont (m). Pour chaque flèche X → Y, les deux paires de X qui portent les cerises partagent une
  étiquette α de X, et les paires par ᾱ portent les antipodes.
- Dans les deux cas, chaque triade porte 12 cerises et 12 antipodes. Le comptage global (84 et 84) ne tranche donc pas.

**Ce qui manque.** En C2, le budget de doubles vaut 4 − 2n_s et l'argument dépasse ce budget. En C1, le budget vaut 8 et
il est saturé exactement par les blocs parallèles : pas de dépassement possible. Une contradiction devrait coupler les
triades entre elles, par les étiquettes (λ_x), par σ (bijections) et par P-Ψ (notes/119). Non fait.
