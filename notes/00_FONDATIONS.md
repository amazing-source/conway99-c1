# 00 — Fondations : faits redérivés depuis les seuls axiomes de srg(99,14,1,2)

Aucun résultat du repo n'est utilisé ici. Chaque fait est prouvé en quelques lignes ; ceux marqués [calc] sont
aussi contrôlés par `code/` sur srg(9,4,1,2) et srg(243,22,1,2).

Notation : Γ = srg(99,14,1,2), A sa matrice d'adjacence, J la matrice tout-un.
Identité fondamentale : A² = 14I + A + 2(J − I − A), soit **A² + A − 12I = 2J**, i.e. (A − 3I)(A + 4I) = 2J.

## F1. Spectre
Valeurs propres 14 (×1), 3 (×54), −4 (×44). (3f − 4g = −14, f + g = 98.)

## F2. Structure de géométrie
λ = 1 : chaque arête est dans un unique triangle ; tout triangle est une « droite ». Γ est le graphe de colinéarité
d'un espace linéaire partiel : 99 points, **231 droites** de 3 points, 7 droites par point.
Un point p hors d'une droite ℓ est adjacent à 0 ou 1 point de ℓ (2 voisins sur ℓ donneraient λ ≥ 2).
μ = 2 : deux points non colinéaires ont exactement 2 voisins communs, eux-mêmes non adjacents
(sinon cette arête aurait 2 voisins communs). Donc Γ = quadrangle partiel **PQ(2,6,2)**.
Tout 4-cycle est induit ; chaque non-arête est diagonale d'un unique 4-cycle : **2079 quadrangles**
(= 4158 non-arêtes / 2). L'involution Δ des diagonales est bien définie et Δ² = id.

## F3. Structure enracinée en x
N(x) = 7K₂ ; les 7 arêtes de N(x) sont les « mates » a ↔ ā (droites {x,a,ā}).
X = Γ₂(x) (84 points). Chaque u ∈ X a exactement 2 voisins dans N(x), non mates ⇒ **X ≅ E(F), F = K_{2×7}**
(cocktail party, 84 arêtes). On note u = ab.
Pour a ∈ N(x) : N(a) = {x, ā} ∪ {ab : b ≠ a, ā} et N(a) = 7K₂ ⇒ les 12 sommets ab sont couplés par 6 arêtes :
**τ_a**, couplage parfait de L∖{a,ā} (ab ~ a τ_a(b)).

Arêtes de H = Γ[X] (12-régulier, 504 arêtes) :
- **étiquetées** (partagent une étiquette) : exactement celles de τ ; chaque u = ab en a 2 (une via a, une via b) ⇒ 84 ;
- **disjointes** (étiquettes disjointes) : 10 par sommet ⇒ 420, groupées en **140 triangles** de 3 arêtes de F
  deux à deux disjointes (le 3e sommet ne peut partager une étiquette : sinon l'arête étiquetée aurait 2 voisins communs).
Comptage des droites : 7 (par x) + 84 (par un a ∈ N(x), pas par x) + 140 (dans X) = 231. ✓

**Système de transitions.** Les τ_a forment un *système de transitions* sur F (au sens de Kotzig) : le 2-facteur
des arêtes étiquetées = décomposition de E(F) en traces fermées b → a → τ_a(b) → … Aucun 3-cycle
(un 3-cycle étiqueté {ab, ac, bc} serait un triangle de X formé d'arêtes étiquetées, contradiction λ).

**Comptes d'étiquettes (μ).** Pour u = ac ∈ X :
- exactement 1 voisin de u contient ā ; exactement 1 contient c̄ ;
- pour b ∉ {a,ā,c,c̄} : exactement 2 voisins de u contiennent b.
(Preuve : μ(b, ac) = 2 avec aucun voisin commun dans {x} ∪ N(x) ; μ(ā, ac) = 2 avec a comme voisin commun.)

## F4. Spectre de H (sous-constituant 2)
H B^T = 2J − B^T(I + P) où B (14×84) est l'incidence étiquette–sommet et P la permutation des mates. Donc :
B^T(antisym.) → valeur propre 0 (×7), B^T(sym., somme nulle) → −2 (×6), 1 → 12, et **ker B** (dimension 70) est
H-invariant avec H² + H − 12 = 0 dessus : valeurs propres 3 (×40), −4 (×30). (Multiplicités : modules de Terwilliger.)
Spectre : 12¹, (−2)⁶, 0⁷, 3⁴⁰, (−4)³⁰. [calc sur les témoins pour l'analogue]

## F5. Grille, prisme, torsion
- **Grille** = K₃□K₃ induit (9 points, 6 droites). Une grille est déterminée par un quelconque de ses quadrangles.
  Deux grilles distinctes se coupent en 0, 1 ou 3 points (une droite).
- **Lemme (grilles serrées).** Tout point hors d'une grille G a exactement 1 voisin dans G.
  (≤ 1 : deux voisins colinéaires ⇒ λ ≥ 2 ; non colinéaires ⇒ ils ont déjà leurs 2 voisins communs dans G.
  Égalité : 9·10 = 90 arêtes sortantes pour 90 points.) Spectralement : Σ_{p∈G} v_p = 0 dans l'espace propre −4.
  Conséquence : si g(x) = nombre de grilles par x et g_tot le total, **(A − 3I) g = g_tot · 1**.
- Grille par x sur les classes {a,ā},{b,b̄} ⟺ τ_a(b)=b̄, τ_ā(b)=b̄, τ_b(a)=ā, τ_b̄(a)=ā.
- **« Grid-full »** : tout quadrangle est dans une grille ⟺ τ = mate en tout point. Alors il y a 2079/9 = 231 grilles
  (autant que de droites) ; le graphe serait un quotient de H(7,3) (à vérifier, voir idée F2), impossible
  car 99 ∤ 3⁷. **Donc la torsion (τ ≠ mate quelque part) est nécessaire** — sous réserve du théorème de revêtement.
- Dans srg(243,22,1,2) (Cayley sur F₃⁵) : τ_s(t) = −t = t̄ partout (vérifié à la main et [calc]).

## F6. Structure autour d'une droite ℓ = {x,a,ā}
Partition en distance : ℓ (3), Γ₁(ℓ) (36), Γ₂(ℓ) (60), **équitable** de quotient [[2,12,0],[1,3,10],[0,6,8]]
(valeurs propres 14, 3, −4). Γ₁(ℓ) induit un graphe **cubique** : pour p ∈ N(x)∖ℓ, ses voisins dans Γ₁(ℓ) sont
son mate p̄ et ses deux « ombres » p_a (unique voisin commun de p et a autre que x) et p_ā.
**Holonomie de droite** ρ_ℓ = (ombre ā→x)∘(ombre a→ā)∘(ombre x→a) ∈ Sym(N(x)∖ℓ) (12 points).
Points fixes de ρ_ℓ ⟺ prismes K₃□K₂ contenant ℓ. Le 2-facteur des ombres a des cycles de longueur 3×(cycles de ρ_ℓ).
En grid-full, ρ_ℓ = id.

## F7. Rangs modulaires forcés
- mod 2 : A² ≡ A (A idempotent sur F₂). rank₂(A) ≤ 55 (noyau ⊇ réduction du réseau propre −4), rank₂(A+I) ≤ 45,
  somme = 99, rank₂(A) pair (forme alternée) ⇒ **rank₂(A) = 54, rank₂(A + I) = 45** (forcé).
- mod 7 : 4 ≡ −3 ⇒ (A − 3I)² ≡ 2J ; M = A − 3I − 4J vérifie M² ≡ 0 (mod 7) : code auto-orthogonal, dim ≤ 49.
- mod 3 : A(A + I) ≡ 2J.
- 3-partie de la forme discriminante de (Z⁹⁹, A) : élémentaire (Z/3)⁵⁴ (preuve : Ax ≡ 0 mod 9 avec x primitif
  force x ≡ c·1 mod 3 puis 3 | 14, absurde).

## F8. Coïncidence propre à 99 dans la famille PQ(2,t,2)
Famille : k = 2(t+1), valeurs propres r, s avec r − s = √(8t+1) ; cas admissibles t ∈ {1, 6, 10, 55, 496}.
**t + 1 = r − s ⟺ t = 6** : le nombre de droites par point égale r − s = 7 uniquement pour 99.
Équivalent : s = 2 − t, et le graphe des droites (231 sommets, 18-régulier, spectre 18, 7⁵⁴, 0⁴⁴, (−3)¹³²)
est **singulier** uniquement pour t = 6. Aussi : t + 1 = 7 est le seul cas ouvert où un système triple de Steiner
STS(t+1) existe (plan de Fano).
