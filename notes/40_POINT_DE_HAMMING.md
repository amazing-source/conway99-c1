# 40 — Le cas « point de Hamming » (idée F15) : dérivation complète

Γ = srg(99,14,1,2), x un sommet. **x est un point de Hamming** si τ = mate en x, c'est-à-dire ab ~ ab̄ pour tous
a, b ∈ N(x) non mates ; de façon équivalente x est dans les 21 grilles 3×3 G_ij (une par paire de classes {i,j}).

## Notations
Classes 0,…,6 ; étiquettes (i,s), s ∈ {0,1} (mate = changer s). Pour une paire P = {i<j}, Q_P = les 4 sommets de X
d'étiquettes (i,s_i), (j,s_j), repérés par (s_i,s_j) ∈ F₂². Les arêtes étiquetées de Q_P forment un 4-cycle
(s ~ s' ⟺ un seul signe diffère). X = ⊔ Q_P (21 × 4 = 84).

## Faits
**(T) Serrage** (L5) : tout point hors d'une grille a exactement un voisin dans la grille. Pour u ∈ Q_P et une grille
G_{P'} avec P' ∩ P = ∅, ce voisin est dans Q_{P'}. Pour P' ∩ P ≠ ∅, c'est l'étiquette commune. Donc :
les 10 voisins disjoints de u sont un dans chaque Q_{P'}, P' ⊂ [7] ∖ P (10 paires), et aucun voisin disjoint de u
n'a de classe commune avec u (confirmé aussi par les comptes d'étiquettes : l'unique voisin de ac contenant ā est
cā).

**(A) Bijections.** Deux sommets de Q_P n'ont aucun voisin disjoint commun : adjacents, leur unique voisin commun est
l'étiquette partagée ; antipodaux, leurs deux voisins communs sont les deux autres sommets de Q_P. Donc pour P ∩ P' = ∅
les arêtes disjointes entre Q_P et Q_{P'} forment une bijection φ_{PP'} : Q_P → Q_{P'}. Il y en a 105.
(Toute bijection de F₂² est affine : AGL(2,2) ≅ S₄. Les 8 isométries du 4-cycle sont celles de partie linéaire I ou
l'échange ; ce sont exactement celles qui commutent avec l'antipodie.)

**(B) λ.** Pour u ∈ Q_P et P' disjoint, l'arête u–φ_{PP'}(u) est dans exactement un triangle ; le 3e sommet est un
voisin disjoint commun, donc dans Q_{P''} avec P'' ⊂ [7] ∖ (P ∪ P') (3 choix) :
exactement un P'' tel que φ_{P'P''}(φ_{PP'}(u)) = φ_{PP''}(u).

**(C) μ, grilles partageant une classe.** P = {i,j}, P' = {i,k}, u ∈ Q_P, w ∈ Q_{P'}. Mêmes signes en i : u, w ont
l'étiquette (i,s) en commun, ne sont pas adjacents (leurs autres étiquettes sont de classes différentes), et aucun
voisin étiqueté de l'un n'est voisin de l'autre. Il faut donc exactement **une** coïncidence
φ_{PP''}(u) = φ_{P'P''}(w), P'' ⊂ [7] ∖ {i,j,k} (6 choix). Signes opposés : aucun voisin commun étiqueté, donc
exactement **deux** coïncidences.

**(D) μ, grilles disjointes.** P ∩ P' = ∅, w ≠ φ(u) : voisins communs = [φ⁻¹(w) ~ u] + [φ(u) ~ w] (voisins étiquetés)
+ le nombre de coïncidences sur les 3 paires P'' ⊂ [7] ∖ (P ∪ P'). Total = 2.

**(E) Comptes d'étiquettes.** u ∈ Q_P, classe libre m : parmi les 4 voisins de u dans les Q_{m,l}, exactement 2
portent (m,0).

Les paires restantes (x, étiquettes, étiquette–sommet de X non traitées) sont automatiquement correctes.
**(T)+(A)–(E) sont équivalents aux équations SRG** une fois τ = mate fixé ; le modèle d'adjacence `hamming_point.py`
encode directement ces équations et sert de contrôle indépendant.

## Structure locale supplémentaire (à la main)
- En chaque u, les 5 triangles disjoints ont 5 directions distinctes (la classe manquante), et les paires de classes
  des deux autres sommets forment une **quasi-1-factorisation de K₅** sur les 5 classes libres.
- Triangle {u, v, z}, u ∈ Q_ij, v ∈ Q_kl, z ∈ Q_mn : {ij, kl, mn} ∪ {d} partitionne [7].
- σ_x ∈ Aut ⟺ toutes les φ sont des isométries. Sous cette hypothèse, (E) interdit la répartition 3+1 des 4 images
  selon la coordonnée lue (preuve directe : les équations a₀ + b₀ = 2 et a₀ − b₀ = 1 sont incompatibles).

## Résultats
| Variante | Encodage | Résultat |
|---|---|---|
| τ = mate + σ_x ∈ Aut | adjacence (`hamming_point.py --sigma`) | **UNSAT**, 201 s |
| τ = mate + σ_x ∈ Aut | φ (`hamming_phi.py --iso`) | **UNSAT**, 34 s (et avec BCD, BCE, BDE, CDE seuls) |
| τ = mate, général | adjacence | UNKNOWN après 30 min |
| τ = mate, général | φ | en cours |
| τ = mate, au moins une φ non isométrique | φ | en cours |

→ **L7** (30_LEMMES.md). Si la variante générale est UNSAT : **aucun sommet de Γ n'est dans ses 21 grilles**.
