# 30 — Lemmes qui survivent (avec preuves)

Γ = srg(99,14,1,2) hypothétique. E_θ = projecteur spectral, Λ_θ = E_θ ∩ Z⁹⁹ (réseau propre, primitif).
Statut : [P] preuve écrite ici ; [C] contrôlé par calcul sur les témoins ; [?] à confronter à la littérature.

---------------------------------------------------------------------------------------------------------
## L1. Γ est tordu : il existe un sommet x et a, b ∈ N(x) avec τ_a(b) ≠ b̄.   [P] [C]

*Preuve.* Supposons τ = mate en tout sommet (« grid-full »). Pour une arête x–a et une droite {x,b,b̄} ≠ {x,a,ā},
ab et ab̄ sont colinéaires avec a : {x,b,b̄} et {a,ab,ab̄} forment un prisme. On transporte ainsi les droites le
long des arêtes ; autour d'un triangle ou d'un quadrangle le transport est trivial (tout quadrangle est dans une
grille, on le lit sur la grille 3×3). Soit K le 2-complexe (triangles + quadrangles) et K̃ son revêtement universel ;
son 1-squelette Γ̃ vérifie les mêmes axiomes locaux (les liens sont préservés) et y est simplement connexe, donc le
transport des droites a une holonomie triviale : on obtient 7 « directions » globales, puis (en transportant aussi
l'orientation cyclique des droites, et en passant au revêtement d'ordre 2 si nécessaire, qui reste simplement connexe
car K̃ l'est) des fonctions f_i : V(Γ̃) → Z/3 définies par intégration le long des chemins (un pas dans la direction i
ajoute ±1 à f_i). Elles sont bien définies car chaque triangle (3 pas dans une direction) et chaque quadrangle
(côtés opposés parallèles et de même orientation) est fermé. f = (f_1,…,f_7) : Γ̃ → H(7,3) est un isomorphisme local
de complexes (bijection N(v) → N(f(v)), préserve triangles et quadrangles). Le complexe de H(7,3) est le 2-squelette
du produit de 7 triangles pleins (contractile), donc simplement connexe : f est un isomorphisme, Γ̃ ≅ H(7,3).
Γ = Γ̃/G avec G le groupe du revêtement agissant librement : 99·|G| = 3⁷. Absurde. ∎
*Contrôles.* H(2,3), H(3,3), BvLS sont grid-full et respectivement H(2,3), H(3,3), H(11,3)/Golay. [C]
*Remarque.* Même argument pour tout PQ(2,t,2) grid-full : n doit être une puissance de 3. Les cas ouverts
6273 = 3²·17·41 et 494019 = 3⁵·2033 sont donc aussi nécessairement tordus.

---------------------------------------------------------------------------------------------------------
## L2. rank₇(A − 3I) est impair.   [P] [?]

*Preuve.* (i) Dénominateurs : E₃ = (A + 4I)/7 − (2/77)J, E₋₄ = [−(A − 3I) + J/9]/7, E₁₄ = J/99.
(ii) 2-adique : E₃ est 2-entier et E₃ ≡ A (mod 2) ; donc Z₂⁹⁹ = Λ₃⊗Z₂ ⊥ (reste), Λ₃⊗Z₂ unimodulaire de rang 54.
Tout x ∈ Λ₃ a x mod 2 ∈ im₂(A), engendré par des lignes de poids 14 : x·x pair. Λ₃⊗Z₂ est pair unimodulaire de
rang 54 = 2·27, donc det Λ₃ ≡ (−1)²⁷ = 7 ou (−1)²⁶·3 = 3 (mod 8, à carrés près).
(iii) det Λ₃ = 7^α·11^γ (seuls 7 et 11 apparaissent dans les dénominateurs de E₃).
11-adique : E₋₄ est 11-entier ; N = (E₃ ⊕ E₁₄) ∩ Z₁₁⁹⁹ est unimodulaire et contient Λ₃ ⊥ Z1 avec recollement
cyclique d'ordre divisant 11 ; det(Λ₃)·99 doit être un carré d'unité × 11^{2·(0 ou 1)} ; comme 11 | 99, le
recollement est Z/11 et γ = 1.
(iv) 7^α·11 ≡ (−1)^α·3 (mod 8) doit valoir 3 ou 7 : seul α pair convient.
(v) Sur Z₇ : Z₇⁹⁹ = Z₇·1 ⊥ N₇ (1·1 = 99 unité), A − 3I = −7E₋₄ sur N₇, d'où (A − 3I)N₇ = 7Λ₋₄^#, et
rank₇ sur N₇ = dim(Λ₋₄^#/Λ₋₄) = α (recollement d'exposant 7 car E₋₄ a 7 au dénominateur une seule fois).
Avec (A − 3I)1 = 11·1 : rank₇(A − 3I) = α + 1, impair. ∎
*Encadrement.* rank₇(A − 3I) ≤ 45 et, par L4, ≥ 15.

## L3. La forme de recollement 7-adique de Λ₃ est non scindée.   [P] [?]
*Preuve.* Formules d'oddité (Conway–Sloane) pour Λ₃ (signature 54, 2-adique pair ⇒ oddité 0) et Λ₋₄ (44) :
54 + (6α + 4e₃) + (10 + 4e₁₁) ≡ 0 et 44 + (6α + 4e₋₄) + 0 ≡ 0 (mod 8), où e = [ε = −1] ; le recollement
anti-isométrique de dimension paire donne e₃ = e₋₄, et le calcul de la forme 11-adique de Z1 (norme 99, unité 9,
carré mod 11) donne e₁₁ = 1. On obtient e₃ ≡ 1 + α/2 : ε₃ = −1 ⟺ α ≡ 0 (mod 4). Dans les deux cas
ε₃ ≠ ((−1)^{α/2} | 7), c'est-à-dire que la forme sur (Z/7)^α n'est pas hyperbolique. ∎
(Les deux équations sont compatibles : aucune contradiction n'en sort.)

## L4. Le recollement 7-adique du 70-espace est le même en tout sommet, et pair.   [P] [C]
Soit x un sommet, K = ker B ∩ Z⁸⁴ (coordonnées sur X = Γ₂(x)), rang 70.
*Preuve.* det(K) divise det(BBᵀ) = 24·12⁷·10⁶ (BBᵀ = 12I + A_F, F = K_{2×7}) : 7 ∤ det K, donc Z₇⁹⁹ = K ⊥ K^⊥
et K^⊥⊗Z₇ = ⟨e_x, e_a, Bᵀe_a⟩ (la saturation de BᵀZ¹⁴ est d'indice ≤ 2). A préserve K (A = H sur K) et K^⊥.
L'action sur K^⊥ est forcée : A e_x = Σe_a ; A e_a = e_x + e_ā + Bᵀe_a ;
A Bᵀe_a = 12e_a + Σ_{b∉{a,ā}} e_b + Σ_{b∉{a,ā}} Bᵀe_b (via HBᵀ = 2J − Bᵀ(I+P) et 2·1_X = ΣBᵀe_b).
Calcul exact (`glue7.py`) : rank₇((A − 3I)|_{K^⊥}) = 15. Donc rank₇(A − 3I) = k(x) + 15 avec
k(x) = rank₇((H − 3I)|_K). Par L2, k(x) = α − 14 est pair et indépendant de x ; 0 ≤ k(x) ≤ 30. ∎
*Contrôles.* L'action forcée sur K^⊥ coïncide exactement avec la vraie matrice sur srg(9,4,1,2) et BvLS. [C]
*Lecture.* C'est la version démontrée de la piste C de ChatGPT : le « recollement intégral des espaces 3 et −4 »
du 70-espace est un invariant global déguisé (α − 14), de parité forcée. Il ne dépend pas de x.

---------------------------------------------------------------------------------------------------------
## L5. Grilles serrées.   [P] [C]
Tout point hors d'une grille G a exactement un voisin dans G ; si g(x) = #grilles par x : (A − 3I)g = g_tot·1.

## L6. Identités de comptage enracinées (valables dans tout graphe aux axiomes locaux).   [P] [C]
- Les arêtes étiquetées forment toujours un 2-facteur de X (2t(t+1) arêtes).
- M(x) + D(x) = |X| (M = arêtes étiquetées « mates » ab–ab̄, D = incidences (arête disjointe, paire de mates entre
  les étiquettes des deux bouts)). Preuve : chaque u = ac a exactement un voisin contenant ā et un contenant c̄.
- d_X(u) = 2 + #{étiquettes lointaines b à distance 2 de u} ; SRG ⟺ toutes à distance 2 ⟺ H 12-régulier.
- Surface des quadrangles : χ(Σ) = 3P − 4158 (P = nombre de prismes).
