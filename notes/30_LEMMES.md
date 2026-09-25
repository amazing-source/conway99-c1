# 30 — Lemmes qui survivent (avec preuves)

Γ = srg(99,14,1,2) hypothétique. E_θ = projecteur spectral, Λ_θ = E_θ ∩ Z⁹⁹ (réseau propre, primitif).
Statut : [P] preuve écrite ici ; [C] contrôlé par calcul sur les témoins ; [?] à confronter à la littérature.
**Synthèse (tableau, corollaires, cohérence de l'ensemble) : notes/100_SYNTHESE_DES_LEMMES.md.**

---------------------------------------------------------------------------------------------------------
## L1. Γ est tordu : il existe un sommet x et a, b ∈ N(x) avec τ_a(b) ≠ b̄.   [P] [C]
*Priorité.* **Résultat connu : Makhnev (1988), Mat. Zametki 44(5), théorème 2** (condition (∗) = non tordu ; preuve
différente, par un srg(33,12,1,6) dérivé). Notre preuve ci-dessous est indépendante (notes/94 §3.1).

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
## L7. Un point de Hamming n'est jamais le point fixe d'une involution.   [P] (2026-09-25, notes/95) [calcul exact, 2 encodages]
*Énoncé.* Si x est un sommet de Γ tel que τ = mate en x (x est dans les 21 grilles qui passent par lui), alors la
réflexion σ_x (x ↦ x, a ↦ ā, ab ↦ āb̄) n'est pas un automorphisme de Γ. Par le lemme de Makhnev (l'involution d'un
srg(99,14,1,2) fixe un seul sommet x et y agit comme σ_x), **dans la branche C2 le point fixe est tordu**.
*Preuve humaine (notes/95).* Si σ_x ∈ Aut, chaque bijection φ_{PR} (faits T, A) commute avec les antipodies,
donc envoie diagonales sur diagonales avec un décalage δ(P,R) ∈ F₂. Le fait C force, pour P = ij, P' = ik, les 6
images d'un point de Q_P à se répartir 3 + 3 entre les deux diagonales de Q_{P'} : exactement 3 des 6 paires
R ⊂ [7] ∖ {i,j,k} ont δ(ij,R) + δ(ik,R) = 1, donc Σ_R (δ(ij,R) + δ(ik,R)) ≡ 1. En sommant les 105 équations, chaque
δ(X,Y) apparaît 12 fois : 0 ≡ 105 ≡ 1. ∎ (Vérifications : le système réduit à 105 bits est UNSAT par Cadical ; sa
version de parité est incompatible sur F₂, `code/hamming_diag.py`.)
*Preuve (calcul, antérieure).* Deux encodages indépendants du cas « τ = mate en x + invariance par σ_x », tous deux UNSAT :
(i) `hamming_point.py --t 6 --sigma` : équations SRG brutes (λ, μ sur toutes les paires) + serrage des grilles (L5),
UNSAT en 201 s (Cadical 1.5.3) ; (ii) `hamming_phi.py --iso` : modèle en bijections φ (faits B–E, notes/20),
UNSAT en 34 s ; UNSAT aussi avec seulement trois des quatre groupes de faits (BCD, BCE, BDE, CDE).
Contrôles : contrôle relâché SAT ; aucune contradiction dans la partie fixe ; le serrage est prouvé (L5).
*À faire.* ~~Preuve humaine~~ faite (ci-dessus). Le certificat DRAT n'est plus nécessaire pour L7.

*Noyau.* Dans le modèle φ isométrique, le fait C seul (μ entre grilles partageant une classe) suffit (UNSAT 3,2 s) ;
B seul est SAT ; CD, CE, DE sont UNSAT. Amorce de preuve humaine : pour P = ij, P' = ik, les 6 isométries
ψ_{P''} = φ_{P'P''}⁻¹∘φ_{PP''} doivent couvrir chaque paire (u,w) de même signe en i une fois et de signes opposés
deux fois ; cela force (n₀, n₁, c₀, c₁) ∈ {(2,4,0,0), (1,3,1,1), (0,2,2,2)} (droites préservant/renversant le signe
en i, croisées), donc un nombre **pair ≥ 2** de ψ « droites ». Reste à montrer l'incompatibilité globale de ces
parités d'orientation.

## L8. Aucun sommet de Γ n'est un point de Hamming.   [calcul exact, 3 exécutions / 2 encodages] [à certifier DRAT]
*Énoncé.* Pour tout sommet x de srg(99,14,1,2), il existe a, b ∈ N(x) non mates avec τ_a(b) ≠ b̄ ; de façon
équivalente, x n'est pas dans ses 21 grilles.
*Preuve (calcul).* Modèle φ sans cassage de symétrie : UNSAT (2 114 s) ; modèle φ avec cassage (quasi-1-factorisation
canonique en u₀ + 3 normalisations de signes, validité argumentée dans notes/40) : UNSAT (46 s) ; modèle d'adjacence
(équations SRG brutes) avec le même cassage : UNSAT (100 s). Variante « au moins une φ non isométrique » : UNSAT
(2 244 s sans cassage, 56 s avec).
*Conséquence (parité).* Si une grille par x manque, au moins deux manquent (si τ_a n'est pas mate sur la classe j,
il envoie un élément de j dans une autre classe k, et la grille (i,k) tombe aussi). Donc g(x) ∈ [0, 19].

*Remarque (2026-09-24, signalée par la session C2).* La validité du cassage de symétrie utilisé dans les exécutions
rapides n'est rédigée nulle part (notes/40 ne la contient pas). La conclusion de L8 repose donc sur l'exécution sans
cassage (UNSAT, 2 114 s), qui reste elle-même à certifier (DRAT) et sans contrôle positif sur BvLS.

## L11. Les torsions ne peuvent pas être confinées à 3 classes.   [calcul exact] [à certifier DRAT]
*Énoncé (calcul).* Il n'existe pas de sommet x dont toutes les torsions (paires (étiquette, classe) tordues) ne
font intervenir que 3 classes. *Calcul.* `rooted_family.py K` avec |K| = 3 (τ libre sur les classes de K, au moins une
torsion, mate ailleurs) : UNSAT en 1,2 s ; contrôle relâché SAT (notes/50). *Non fait* : second encodage, DRAT,
contrôle positif BvLS. À ne pas utiliser pour élaguer une construction tant que ce n'est pas certifié.

## L10. Aucun sommet n'est dans exactement 19 grilles : g(x) ≤ 18 pour tout x.   [P] (2026-09-25, via L9') [calcul exact]
*Portée exacte.* g(x) = 19 : preuve humaine (L9' ; la classification des configurations à 19 grilles se refait à la
main : deux grilles manquantes G_{ij}, G_{ik}, donc seules les étiquettes de la classe i sont tordues, et elles
échangent les classes j et k). g(x) = 20 : impossible par parité (une torsion casse deux grilles). g(x) = 21 : c'est
L8, qui reste **calcul SAT non certifié**. « g(x) ≤ 18 » dépend donc encore de L8.
*Énoncé.* À symétrie près, g(x) = 19 n'admet que trois configurations de τ en x (τ_{i±} échangent deux classes j, k,
tout le reste mate) ; les trois sont réfutées **par simple propagation unitaire** des équations SRG
(`rooted_model.py --case g19A|g19AA|g19AB`), avec ou sans les contraintes de serrage ; le contrôle relâché
(degrés + serrage) est SAT ; le même modèle ne réfute pas instantanément le cas Hamming (cohérence).
*Preuve humaine de g19A.* u = {(0,0),(1,0)} : τ_{(0,0)}((1,0)) = (2,0) ≠ (1,1), donc (compte d'étiquettes) un voisin
disjoint de u contient (1,1) ; le serrage de G_{1m}, m ≥ 2, ne laisse que w = {(0,1),(1,1)} ; alors
z = {(1,0),(0,1)} est voisin de u (via τ_{(1,0)} = mate) et de w (via τ_{(0,1)} = mate), et l'arête étiquetée u–z
aurait deux voisins communs, contre λ = 1.
**Lemme local L9' (nouveau, 2026-09-25 ; noyau SAT minimal de 7 contraintes, identique pour g19A, g19AA, g19AB).**
*Énoncé.* Si τ_a(c) ≠ c̄ et τ_{c̄}(a) = ā, alors au moins une grille G_{[c],m}, m ∉ {[a],[c]}, manque en x.
*Preuve.* Supposons toutes ces grilles présentes. (i) Serrage : l'unique voisin de z₂ = {a, c} dans G_{[c],m} est
son étiquette c, donc z₂ n'a aucun voisin dans Q_{[c],m}. (ii) μ(c̄, z₂) = 2 : un voisin commun est c ; l'autre est un
sommet de Γ₂(x) d'étiquette c̄ voisin de z₂, donc dans Q_{[a],[c]} par (i), c'est-à-dire {a, c̄} ou {ā, c̄}. Or
{a, c̄} ≁ z₂, car la droite par a et z₂ est {a, z₂, {a, τ_a(c)}} avec τ_a(c) ≠ c̄. Donc z₂ ~ z₁ := {ā, c̄}.
(iii) a et z₁ ne sont pas adjacents, mais ā (mate de a, étiquette de z₁), {a, c̄} (voisin de z₁ car τ_{c̄}(a) = ā) et
z₂ (par (ii)) sont trois voisins communs : contradiction avec μ = 2. ∎
*Priorité.* L10 était déjà démontrable à la main par **L12** (même session antérieure : pour a = (0,0), c = (1,1),
τ_c(ā) = a et τ_y(c) = c̄ hors des classes 0, 1, donc contradiction) ; l'entrée « P partielle » ne l'écrivait pas.
L9' en donne une seconde preuve, par une règle différente (hypothèses de grilles au lieu de transitions).
*Seconde preuve humaine de L10.* Dans les trois configurations g19A, g19AA, g19AB (a = (0,0) tord la classe 1 vers
la classe 2 ; les transitions des étiquettes de la classe 1 sont mates ; les grilles G_{1m}, m ≥ 2, sont présentes),
prendre c = (1,1) : τ_a(c) = (2,·) ≠ c̄ et τ_{c̄}(a) = ā. L9' donne la contradiction. (`code/core_extract.py` :
noyaux minimaux, tous formés de μ(0a, {0b,1a}), μ(1a, {0a,1b}) et du serrage de {0a,1b} dans G_{12}, …, G_{16}.)
*Remarque.* L9' seul n'exclut que 24 des 728 configurations tordues confinées à 3 classes (L11). Le noyau minimal de
L11 compte 112 équations, dont la « partie Hamming » des classes non tordues : pas de preuve courte en vue.

**Lemme local L9 (généralisation).** Si τ_a(c) ≠ c̄, τ_c(a) = ā et τ_ā(c̄) = c, alors au moins une grille
G_{[c],m}, m ∉ {[a],[c]}, manque en x. (Même preuve.)

## L12. Règle de propagation de la torsion (preuve à la main, valable dans toute géométrie locale).   [P] [C]
*Énoncé.* En un sommet x, soient a, c des étiquettes de classes différentes avec τ_a(c) ≠ c̄. Alors τ_c(ā) ≠ a, ou il
existe une étiquette y hors des classes de a et de c avec τ_y(c) ≠ c̄.
*Preuve.* Supposons τ_c(ā) = a et τ_y(c) = c̄ pour tout y hors de [a] ∪ [c].
(1) Pour un tel y : c̄ et cy sont à distance 2 (voisin commun c) ; yc̄ est un second voisin commun (yc̄ ∋ c̄, et
cy ~ yc̄ car τ_y(c) = c̄) ; comme μ = 2, aucun autre sommet contenant c̄ n'est voisin de cy ; en particulier ac̄ ≁ cy.
(2) c et ac̄ sont à distance 2 (voisin commun c̄) ; le second voisin commun est un voisin de c autre que x, c̄, donc un
sommet cz de X adjacent à ac̄ : z ≠ a (car τ_a(c) ≠ c̄), z hors de [a] ∪ [c] est exclu par (1), donc z = ā : cā ~ ac̄.
(3) a et cā sont à distance 2 ; or ā, ac (cā ~ ac car τ_c(ā) = a) et ac̄ (par (2)) sont trois voisins communs,
contre μ = 2. ∎
Seuls λ = 1 et « μ = 2 à distance 2 » servent : L12 vaut dans toute géométrie localement (t+1)K₂.
*Contrôle.* Vérifié sur les géométries tordues (20, 39, 42, 93 sommets) : 0 violation sur 12 828 paires tordues.
*Provenance.* Extrait automatiquement (`explain_up.py`) : la réfutation par propagation des trois cas g = 19 utilise
exactement les 12 équations de cette preuve.
*Conséquences à la main (`l12_closure.py`).* En notant W(a, j) « a tord la classe j » (ne dépend que de la classe ;
0 ou ≥ 2 classes par étiquette), L12 donne : si W(a, j), chaque étiquette c de j tord [a], ou une étiquette d'une
troisième classe tord j. D'où, **sans ordinateur** : une étiquette tordue seule est impossible, une seule classe tordue
aussi. L12 seule permet encore 2 étiquettes (de classes différentes, tordant la même paire de classes) ou un triangle
de 3 classes — les SAT montrent que ces motifs meurent aussi (L11) ; les règles supplémentaires sont en cours
d'extraction.

## L13. Règle d'holonomie : une classe est tordue par 0 ou au moins 2 étiquettes (preuve à la main).   [P]
*Énoncé.* En x, pour une droite ℓ = {x, a, ā}, l'ensemble Z = {z ∈ N(x)∖ℓ : τ_z(a) ≠ ā} (les étiquettes qui tordent la
classe de a) est stable par l'holonomie ρ_ℓ, qui n'y a aucun point fixe ; pour z ∈ Z, az ~ ā ρ_ℓ(z) (arête disjointe).
Donc |Z| ≠ 1.
*Preuve.* L'ombre σ : étoile(a) → étoile(ā) (az ↦ son unique voisin dans étoile(ā)) est une bijection (μ(a, āy) = 2 avec
ā pour voisin commun, et symétriquement). σ(az) = āz ⟺ az ~ āz ⟺ τ_z(a) = ā. ρ_ℓ(z) := y si σ(az) = āy ; ρ_ℓ est une
permutation dont les points fixes sont exactement les z ∉ Z ; elle permute donc Z sans point fixe. ∎
*Usage.* Avec R0 (une étiquette tord 0 ou ≥ 2 classes), L13 est la règle « transposée ». Elle explique la réfutation
par propagation du motif « triangle avec un échange renversant » : ρ_ℓ doit échanger les deux seules étiquettes de Z,
ce qui force deux arêtes disjointes, et le sommet {(4,0),(6,0)} reçoit 3 voisins contenant (5,0) au lieu de 2.

## L14. Deux étiquettes tordues ne suffisent pas (cas |C| = 2).   [calcul exact] [à certifier]
Par R0 + L12, si exactement deux étiquettes tordent en x, elles sont dans deux classes différentes et tordent le même
ensemble C de classes (C disjoint de leurs classes, 2 ≤ |C| ≤ 5). Pour |C| = 2 : les deux motifs concrets à symétrie
près (échanges préservant/préservant et préservant/renversant) sont UNSAT (69 s et 41 s, modèle d'adjacence exact) ;
la version « famille » (τ libres sur le domaine C) confirme (92 s). |C| = 3 : UNSAT (1 120 s, `data/twolabel_dom234`) ;
|C| = 4 : UNSAT (2 695 s, `data/twolabel_dom2345`) ; |C| = 5 : non lancé. Aucun certificat DRAT, pas de contrôle positif BvLS.

## L15. Torsion totale = moment spectral (identité exacte).   [P] [C partiel]
*Énoncé.* Pour une arête e = xa, soit d(e) le nombre de classes (en x, hors celle de a) que a tord ; d(e) = 6 − m(e)
où m(e) = nombre de prismes de barreau e, donc d est symétrique. Avec |W(x)| = Σ_{a~x} d(xa) (paires étiquette-classe
tordues en x) et P le nombre de prismes :
  **P = 1386 − (1/6) Σ_x |W(x)|**   et, avec F21 (6P = 2268 − Σν³),   **Σ_x |W(x)| = 6048 + Σ_curl ν³**,
où ν parcourt le spectre du laplacien de Hodge des arêtes, décalé de 15, sur la partie rotationnelle (595 valeurs,
Σν = 84, Σν² = 7056).
*Preuve.* 3P = Σ_e m(e) (chaque prisme a 3 barreaux) = Σ_e (6 − d(e)) = 4158 − ½ Σ_x Σ_{a~x} d(xa). Puis F21. ∎
*Contrôle.* F21 vérifié sur srg(9) (P = 6) et BvLS (P = 8 910) ; m(e) et d(e) = 6 − m(e) vérifiés sur les exemples.
*Intérêt.* C'est le chaînon manquant identifié : **une majoration de Σν³** bornerait la torsion totale, donc
forcerait des sommets peu tordus, que la frontière exclut. Le 4ᵉ moment Σν⁴ = 173 880 + 8·S₄ (S₄ = 4-cycles signés du
graphe O des arêtes opposées, liés aux fermetures en 3-cube) donnerait |Σν³| ≤ √(7056·Σν⁴) — encore trop faible.
*Mise à jour (soir).* Confirmation indépendante : dans Reimbayev (arXiv:2608.19410), la variable libre n₃ des
fréquences d'ordre 7 vaut 3(P_max − P) = ½ Σ_x |W(x)| (via z₃₉ = (n − 6k + 15)·P). Majorer Σν³ revient exactement à
majorer n₃ ; ni Hodge (confinement réfuté : théorème H0) ni le comptage d'ordre ≤ 7 (borne triviale n₃ ≤ 4158) ne
le font. Identités par blocs H1–H3, dont ||[Q, B_T]||² = 24(P_max − P) = 4Σ|W| : notes/60_HODGE.md.

## L16. Condition de Krein pour les droites : P ≤ 1151.   [P] (preuve à la main, notes/70)
*Énoncé.* Avec u_L = projection unitaire de 1_L sur E₋₄ (dim 44) : **12P = 13860 − 64‖Σ_L u_L^{⊗3}‖²**, donc
P ≤ 1155 ; avec les points (Cauchy–Schwarz sur les tenseurs cubiques), **P ≤ 1151**. Équivalents : Σ_x|W(x)| ≥ 1410
(moyenne ≥ 14,2), n₃ ≥ 705, prismes par droite ≤ 10 en moyenne (grid-full : 12).
*Preuve.* Dans E₋₄, 7⟨w_L,w_M⟩ = 4 (L = M), 0 (sécantes : les 7 droites par un point sont orthogonales), 1 − e
(disjointes, e arêtes) ; par droite n₃ = π, n₂ = 36 − 3π, n₁ = 144 + 3π, n₀ = 32 − π ; Σ_M K³ = 60 − 6π(L) ; la somme
des cubes des produits scalaires est la norme au carré de Σ u^{⊗3}. ∎
*Contrôle.* BvLS : formules et somme des cubes vérifiées numériquement à 1e-13. Propre à 99 dans la famille.
*Portée.* Borne supérieure sur les prismes (torsion forte obligatoire), obtenue sans ordinateur ; pas une
contradiction : il manquerait une borne inférieure sur P.

## L17. Le 70-espace local se scinde en 2, 3, 5.   [P] [C sur BvLS]
*Énoncé.* K = {v ∈ Z^{Γ₂(x)} : sommes nulles par étiquette} est pair, det K = 2²¹·3⁸·5⁶ ; pour p ∈ {2,3,5},
K ⊗ Z_p = K₃ ⊥ K₋₄ ; tout le 3- et 5-discriminant est dans K₃, tout le 2-discriminant dans K₋₄. Donc K₃ (rang 40) est
pair, 2-adiquement unimodulaire, det 3⁸·5⁶·7^k, formes 3- et 5-adiques déterminées (antisquare) ; K₋₄ (rang 30) est
pair, det 2²¹·7^k. Oddité : k/2 ≡ k₇ (mod 2), compatible avec L3.
*Preuve.* H agit sur disc(K) ≅ disc(K^⊥) par Φ = J − I − M (valeurs propres 12, −2, 0) ; comparaison des actions
de H (3 sur K₃, −4 sur K₋₄) modulo p. Détails : notes/80. ∎
*Contrôle.* Mécanisme vérifié sur BvLS en p = 5 (rangs 110 / 76 exactement prédits), 7, 11 (`local_split_check.py`).
*Portée.* Tout est cohérent au niveau du genre : pas de contradiction sans information plus fine.

## L18. La seconde variable libre d'ordre 7 est une statistique de torsion.   [P] [C] (notes/90)
*Énoncé.* σ_x = réflexion ponctuelle en x (mates échangés, étiquette {b,c} ↦ {b̄,c̄}) ; S = #{(x,E) : E ∈ Γ₂(x),
E ~ σ_x(E)} = nombre de coïncidences τ_a(c) = τ_c(a). Dans toute géométrie aux axiomes locaux : z₂ = S/2,
z₃ = Σ|W| − 2S, z₁₁ = 2Σ|W| − 2S (z_i = copies induites des graphes Z_i de Reimbayev). Dans un SRG, z₁₁ = 4n₃ − 2S
et le polygone d'ordre 7 est exactement 0 ≤ S ≤ n₃. Grilles avortées : pour x et une paire de classes, les 9 points
G vérifient |Σ_G p_v|²_{63E₋₄} = 18(18 − e(G)), et Σ(18 − e) = 2n₃ − S/2.
*Preuve.* Identification directe de Z₂, analyse de cas pour Z₁₁ et Z₃ (notes/90). ∎
*Contrôle.* Comptage direct des copies induites sur 3 géométries tordues et srg(9) (`code/z11_identity.py`) ;
identité des grilles avortées aussi sur BvLS.
*Portée.* Dictionnaire exact, pas une contradiction : il faudrait une relation supplémentaire entre n₃ et S.

## L19. Structure 7-adique de la similitude de torsion U_x = (2H + I)Σ_x.   [P] (notes/93)
*Énoncé.* Sur le réseau local K (unimodulaire en 7), U_x a pour diviseurs élémentaires 7-adiques 1^k, 7^{70−2k}, 49^k,
où k = rank₇(A − 3I) − 15 est le même en tout sommet (L4). Les valeurs propres de U_x sont 7ζ (ζ racine de l'unité) sauf
un « déficit 7-adique » total ≤ k (au plus k rotations quadratiques irrationnelles t² − mt + 49, 7 ∤ m). tr U_x = 2s(x),
tr U_x² = 8e_σ(x) − 602. Si k = 0 : U_x/7 est entière d'ordre fini, s(x) ≡ 0 (mod 7), e_σ(x) ≡ 14 (mod 49) partout.
*Preuve.* U*U = 49 sur K₇ unimodulaire (forme de Smith symétrique autour de 7), Newton au-dessus de Hodge, Kronecker. ∎
*Portée.* Seul lien connu entre la torsion en chaque sommet et un invariant global ; presque vide si k est grand.
*Complément (notes/94 §1, amélioré par L20 : k ≥ 6).* **k ≥ 2** : la ligne d'un sommet y ∈ Γ₂(x) n'est jamais combinaison mod 7 des 15 lignes
de B₁(x) (sur Γ₂(x) ces combinaisons sont additives en étiquettes, et les paires où elles doivent s'annuler
contiennent assez de triangles pour tout annuler). Le cas k = 0 de L19 est donc vide.

## L20. L'invariant 7-adique k est borné par le type de torsion de chaque étiquette.   [P] [calcul exhaustif exact] (notes/97)
*Énoncé.* Pour tout sommet x et toute étiquette a : k ≥ 11 − 2e(τ_a), où e(τ_a) est le nombre de cycles pairs du
multigraphe induit par τ_a sur les 6 autres classes. Donc k ≥ 6 ; k = 6 ⟹ tous les τ_a échangent leurs classes par
paires ⟹ P = 0 ; P ≥ 1 ⟹ k ≥ 8 ; une étiquette non tordue ⟹ k ≥ 12.
*Priorité.* Principe des bornes de p-rang par sous-graphe induit : van Eijl 1991 (mémoire, dir. Brouwer), §3.3 ;
l'application à 99 (étoiles, formule 11 − 2e, lien avec la torsion) est nouvelle.
*Preuve.* Sous-matrice principale de A − 3I sur B₁(x) ∪ étoile(a), déterminée par τ_a ; bloc du moulin inversible
mod 7 ; k ≥ rang₇ du complément de Schur S ≡ H_τ + P' + J (mod 7) ; H_τ + P' = réunion de deux couplages = un
cycle alterné de longueur 2m par cycle de classes de longueur m, de noyau mod 7 de dimension 2 si m est pair ; J ajoute
le vecteur 1 au noyau. D'où rang = 11 − 2e ; k pair (L2). ∎ (Aussi vérifié exhaustivement sur les 10 395 couplages.)

## L20 ter. k ≥ 10.   [P + calcul exact : énumération sur F₇ et 32 petites instances UNSAT par propagation] (notes/97)
*Idée.* Même mécanisme que L20 bis pour k = 8 : les étoiles de type (0;2,4), (2;2,2) sont exclues par l'algèbre
linéaire seule ; pour (0;2,2,2), les 32 sous-espaces admissibles sont tous incompatibles avec les degrés et la
contrainte d'étiquette (τ_ℓ(a) unique). La méthode à une étoile ne dépasse pas k ≥ 10.

## L20 bis. k ≥ 8.   [P] (notes/97)
*Preuve.* Si k = 6, toutes les étoiles sont de type (2,2,2) et de rang 5 = k − 1 ; les vecteurs du noyau d'un bloc
d'étoile sont alors des relations entre lignes complètes de la matrice locale M_x = H + 4I + 3S + P' + 5J (F₇), en
particulier ligne({a,ℓ₁}) = ligne({a,ℓ₃}) pour un 4-cycle alterné. En la colonne {ℓ₁, q}, cela impose
H − H' ≡ 4 ou 5 (mod 7) avec H, H' ∈ {0, 1}. ∎ Donc 8 ≤ k ≤ 30.

## L21. Boule d'une droite : k ≥ 23 − d(L).   [P] [C numérique] (notes/99)
*Énoncé.* Pour une droite L, soit G(L) le graphe induit sur les 36 points adjacents à exactement un point de L. Il
est cubique (un couplage par point de L, plus le 2-facteur de Lou–Murin). On a
rang₇ (A − 3I)[L ∪ N(L)] = 2 + rang₇(A_{G(L)} − 3I), donc **k ≥ 23 − d(L)** avec
d(L) = dim ker₇(A_{G(L)} − 3I) = c(L) + r₇(K(G(L))) (composantes + 7-rang du groupe du tas de sable).
En particulier, si G(L) est connexe et que 7 ne divise pas son nombre d'arbres couvrants, alors **k ≥ 22**.
*Preuve.* Complément de Schur par rapport au bloc J₃ − 4I₃ de L (inversible mod 7, inverse −(I + J)/4) :
S ≡ A_G − 3I + 2D + 2J. On décompose selon U = ⟨indicatrices des trois parties⟩ et U^⊥. Sur U^⊥, S = A_G − 3I ; sur
U, A_G − 3I a rang 2 et S rang 1. Laplacien 3I − A_G et forme de Smith pour le tas de sable. ∎
*Cas particuliers.* Avec deux points de L seulement (27 points, graphe 2-régulier), on retrouve L20 (11 − 2e). Le rang
du bloc « deux étoiles » de notes/97 vaut 23 − d(L).
*Contrôles.* Identité vérifiée sur 700 configurations (τ_a, τ_ā, σ) aléatoires ; d = 1 ⟺ 7 ∤ τ(G) sur 317
configurations admissibles (0 exception). Maximum de d trouvé par recuit : 9, d'où la conjecture k ≥ 14.
*Portée.* Minoration seulement : la voie 7-adique pousse k vers le haut (k ≥ 22 dès qu'une droite est générique) et
ne peut pas donner le verrou sans une majoration globale de k.

## L22. Le genre de Λ₋₄ interdit k = 30 : 10 ≤ k ≤ 28.   [P] [C sur Petersen, T(7), T(8), srg(9)] (notes/101)
*Énoncé.* rank₇(A − 3I) ≤ 43 (au lieu de 45) ; la partie 7-unimodulaire de Λ₋₄ (rang 30 − k) est non nulle et
jamais hyperbolique sur F₇.
*Preuve.* Λ₋₄ est pair, de rang 44 et de déterminant 9·7^{14+k}, avec une partie 3 cyclique Z/9 (3-excès 8 ≡ 0). Sur
Z₇, Λ₋₄ = U ⊥ 7V et (det U|7)(det V|7) = (9|7) = +1. L'oddité donne 44 + 8 + 6(14 + k) + 4δ_V ≡ 0 (mod 8), d'où
δ_V ≡ k/2. À k = 30, U = 0 force δ_V = 0, alors que k/2 = 15 est impair. ∎
*Portée.* Premier plafond de k. Il exclut le profil 7-générique (k = 30) : en chaque sommet, la matrice locale M_x
est 7-dégénérée d'au moins deux dimensions. Il reste à relier cette dégénérescence à la torsion.

## L23. Signe de la boule d'une droite : (τ(G(L)) | 7) = +1 ⟹ k ≥ 24.   [P] [C : 300 configurations, 5 SRG] (notes/102)
*Énoncé.* Q = A − 3I + 3J (mod 7) est le Gram de la forme β, non dégénérée et **non scindée** sur G = N(W), de
dim 14 + k. Pour tout S ⊆ V : rang₇ Q_SS ≤ 14 + k, et en cas d'égalité la partie non dégénérée de Q_SS est non scindée.
Pour la boule d'une droite (39 points) : rang = 37 − d(L), et si d(L) = 1 le discriminant est τ(G(L)) (arbres
couvrants). Donc k = 22 impose (τ(G(L)) | 7) = −1 pour toute droite générique, et une droite τ-carrée force k ≥ 24.
*Preuve.* N = A − 3I vérifie N² ≡ 2J, donc N² = 0 sur W = 1^⊥. β(Nv, Nv') = v·Nv' est la 7-partie de la forme
discriminante de Λ₋₄, de signe (−1)^{k/2} (L22) : non scindée. Pour la boule : F³⁹ = (F^L ⊕ U) ⊥ U^⊥, où la partie fixe
T a rang 3 et disc carré, et −L_G|_{U^⊥} a disc −3⁻¹τ (théorème des arbres). ∎
*Compléments.* Localement, la forme de M_x est hyperbolique (G = G_x ⊥ W_x, W_x non scindé fixé par le moulin) et
M_x² ≡ 0. Les blocs d'arête (L20) ont un rang Q impair : le signe n'y ajoute rien.
*Portée.* La torsion entre par le signe. Heuristique : k ∈ {24, 26, 28}. Critère de non-existence : un S avec
rang₇ Q_SS ≥ 43, ou = 42 et scindé.

## L24. Point de Hamming : réduction de Kneser et 18 ≤ k ≤ 26.   [P] [C] (notes/103)
*Énoncé.* En un point de Hamming x, H = ⊕ C₄ + couplages parfaits entre paires de classes disjointes : une
S₄-connexion sur K(7,2) soumise aux équations (K), (T). Si tous les couplages préservent les paires antipodales,
contradiction (transposition du Théorème D de la branche C2). Dans tous les cas, 18 ≤ k ≤ 26.
*Preuve.* Siblings adjacents, λ = 1 et μ = 2 ⟹ au plus un voisin par paire disjointe, et 10 = C(5,2). Régime A :
signature A_χ avec A_χ² = 3A_χ + 10, triangles équilibrés, couples complémentaires ⟹ somme ≠ 0. Pour k : lignes en
configuration grille (d = 6, L21) ; les 21 grilles complètes donnent η_P = 11·1_G − 1 ∈ Λ₃, de Gram de rang 14 mod 7,
de radical ⟨Σ_{v∈L} f_v⟩ ⊂ G, donc 14 ≤ 40 − k. ∎
*Portée.* Régime mixte ouvert : L8 n'est pas encore démontré à la main.

## L5. Grilles serrées.   [P] [C]
Tout point hors d'une grille G a exactement un voisin dans G ; si g(x) = #grilles par x : (A − 3I)g = g_tot·1.

## L6. Identités de comptage enracinées (valables dans tout graphe aux axiomes locaux).   [P] [C]
- Les arêtes étiquetées forment toujours un 2-facteur de X (2t(t+1) arêtes).
- M(x) + D(x) = |X| (M = arêtes étiquetées « mates » ab–ab̄, D = incidences (arête disjointe, paire de mates entre
  les étiquettes des deux bouts)). Preuve : chaque u = ac a exactement un voisin contenant ā et un contenant c̄.
- d_X(u) = 2 + #{étiquettes lointaines b à distance 2 de u} ; SRG ⟺ toutes à distance 2 ⟺ H 12-régulier.
- Surface des quadrangles : χ(Σ) = 3P − 4158 (P = nombre de prismes).
