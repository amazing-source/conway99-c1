# 60 — Route Hodge / Σν³ : examen critique (2026-09-24, soir)

*Demande de l'utilisateur : poursuivre la piste « borner Σν³ » (message précédent : identité Σ(ν+4)(3−ν) = 0 et
idée d'un confinement local→global du spectre). Verdict : **la piste, telle que je l'avais formulée, est réfutée** ;
ce qui survit est une reformulation exacte (identités H1–H3), sans levier. Scripts : `code/hodge_blocks.py`,
`code/reimbayev7.py`.*

## 0. Cadre et notations
Complexe K = sommets, 693 arêtes, 231 triangles (droites), 2079 quadrangles. L₁ = 15I + Q, Q = adjacence signée du
graphe O des arêtes opposées (12-régulier). Gradient : Q = −1 − θ ∈ {−4 (×54), 3 (×44)}. Rotationnel (595) : ν.
Géométrie à axiomes locaux générale : t (lignes par point − 1), k = 2t + 2, O est 2t-régulier,
g(x) = x² + x − 2t (racines r', s' ; pour t = 6 : 3 et −4), n_SRG = 2t² + 4t + 3, P_max = tE/3 (= 1386 pour 99),
M = Q² + Q − 2t·I.
Identités générales (vérifiées) :
- tr M = 0 ; M δ₀ = δ₀(A² + A − 2t) (= δ₀·2J = 0 pour un SRG) ;
- Σ_rot g(ν) = −2(n − n_SRG) (= 0 pour un SRG) ;
- tr(QM) = 6(P_max − P) = Σ_x |W(x)| (pour 99, via L15) = Σ_rot ν g(ν) pour un SRG.

## 1. Réfutation du « confinement » (ce que j'avais proposé)
Énoncé proposé : montrer que le spectre rotationnel reste dans [−4, 3] (ou à ~0,03 près de {3, −4}) par une
méthode local→global (Garland, expanseurs de grande dimension), le lien de chaque sommet étant K₁₄.

**(a) Garland est vide ici.** Pour f ∈ C¹ et f_x sa localisation au sommet x (fonction sur les 14 arêtes en x) :
Σ_x ||d_x f_x||² = ||δf||² + 13||f||² − fᵀQf (triangle : (a+b+c)² + Σa² ; quadrangle : (a+b+c+d)² + Σa² − 2(ac+bd))
et, le lien étant K₁₄, Σ_x ||d_x f_x||² = 28||f||² − ||div f||². On retrouve seulement L₁ = 15 + Q : les liens voient
tout sauf les arêtes opposées, c'est-à-dire exactement Q. (Bochner–Forman : courbure F(e) = 13 + 2 − 12 = 3, d'où
L₁ ≥ 3 et H¹(K; ℝ) = 0, rien de plus.)

**(b) Théorème H0 (le confinement est faux pour tout SRG de la famille avec t ≥ 2).**
Confinement ⟹ g(ν) ≤ 0 pour tout ν, de somme nulle ⟹ M = 0 ⟹ chaque arête de O est dans exactement un prisme
(M_{ee''} = Q_{ee''}(1 − π(e,e'')) sur les arêtes de O) ⟹ P = P_max ⟹ grid-full ⟹ Γ revêtu par H(t+1, 3) (L1) ⟹
pour e d'une direction i et e'' = e + a·e_j + b·e_l (j ≠ l, tous deux ≠ i), deux 2-chemins de O de même signe
(toutes les entrées de Q valent −1 pour l'orientation invariante par translation), et aucun autre relevé ne peut
compenser (il faudrait un mot de code de poids ≤ 4 alors que le revêtement préserve les boules de rayon 2) ⟹
M_{ee''} = 2 ≠ 0. Contradiction. Donc « spectre rotationnel ⊂ [s', r'] » n'est vrai pour **aucun** SRG existant de
la famille avec t ≥ 2 : le démontrer pour 99 revient à démontrer la non-existence, sans aucun gain.

**(c) Contrôle BvLS (théorie des représentations, puis calcul).** BvLS = H(11,3)/C, C = code de Golay ternaire
[11,6,5] ; les caractères des sommets sont indexés par c ∈ C^⊥ = [11,5,6], de poids 0 (×1), 6 (×132), 9 (×110). Les
arêtes de direction i sont indexées par a ∈ F₃¹¹ (a → a + e_i) ; Q = −Σ_{j≠i}(T_{e_j} + T_{2e_j}) donne la valeur
propre 3w_i − 20 avec w_i = #{j ≠ i : c_j ≠ 0}, et B_T = I + T_{e_i} + T_{2e_i} vaut 3 si c_i = 0, sinon 0. D'où la
prédiction : rotationnel = {−20^11, −5^660, −2^660, 4^880, 7^220}, partie triangles C_T = {−20, −2, 7}, partie
curl₀ = {−5, 4}.
**Calcul** (`hodge_blocks.py --big`, 24 s, 557 Mo) : exactement ce spectre. 231 valeurs propres hors de [−5, 4],
660 strictement dedans. Σg = 11·360 − 660·18 + 220·36 = 0.
**(d) Conséquence.** Toute méthode uniforme en t (Garland, HDX, Bochner) qui confinerait le spectre est réfutée par
BvLS ; la version « à 0,03 près » aussi (BvLS a −20, −2, 7 avec multiplicités 11, 660, 220). **Piste tuée.**

## 2. Ce qui survit : le bloc « triangles »
C_T = vect des circulations des 231 triangles (orthogonales, car les triangles sont disjoints en arêtes), contenu dans
le rotationnel. C₀ = C_T^⊥ = cochaînes fermées sur les triangles ≅ fonctions de drapeaux de somme nulle sur chaque
droite (dim 462) = gradient (98) ⊕ curl₀ (364).

**Lemme H1.** Deux droites disjointes sont reliées par 0, 1, 2 ou 3 arêtes ; 2 arêtes ⟺ un seul quadrangle entre
elles (n = 1) ; 3 arêtes ⟺ couplage parfait ⟺ prisme (n = 3) ; jamais n = 2. (Un point a au plus un voisin sur une
droite qui ne le contient pas ; deux arêtes partant du même point forceraient un triangle.)
Conséquence : les arêtes de O hors prisme sont en bijection avec les paires de droites reliées par exactement
2 arêtes ; leur nombre est 3(P_max − P) = ½ Σ_x |W(x)|.

**Lemme H2 (torsion = non-commutation).** Soient B_T = ∂₂,T ∂₂,Tᵀ (projecteur ×3 sur C_T) et
B = P_T Q (1 − P_T). Alors
  ||B||²_F = (4/3)(P_max − P),   ||[Q, B_T]||²_F = 24 (P_max − P)   (= 4 Σ_x |W(x)| pour 99).
*Preuve.* tr(P_T Q²) = 2tE/3 (deux arêtes adjacentes n'ont aucun voisin commun dans O) ;
tr(P_T Q P_T Q) = (1/9) Σ_{T,T'} s(T,T')², s = nombre signé d'arêtes de O entre T et T' ∈ {0, ±1, ±3} (H1), avec
Σ_{T'} s² = 9π(T) + (6t − 3π(T)) et Σ_T π(T) = 2P. ∎  Grid-full ⟺ [Q, B_T] = 0.

**Lemme H3 (traces par blocs).** tr(P_T M) = 0 pour tout t. Donc, avec α = spectre de Q comprimé à C_T et κ = spectre
de Q comprimé à curl₀ :
  Σ_{C_T} g(α) = −||B||²,   Σ_{curl₀} g(κ) = −||B||² − 2(n − n_SRG).

**Vérification exacte** (`hodge_blocks.py`) :

| géométrie | n | t | P / P_max | ||[Q,B_T]||² = 24(P_max−P) | Σ_rot g | curl₀ strictement dans (s', r') |
|---|---|---|---|---|---|---|
| srg(9,4,1,2) | 9 | 1 | 6/6 | 0 = 0 | 0 | 0/4 |
| H(3,3) | 27 | 2 | 54/54 | 0 = 0 | −16 | 12/28 |
| tordu t=2 | 20 | 2 | 0/40 | 960 = 960 | −2 | 21/21 |
| tordu t=3 (39) | 39 | 3 | 39/156 | 2808 = 2808 | −12 | 51/66 |
| tordu t=3 (42) | 42 | 3 | 0/168 | 4032 = 4032 | −18 | 63/71 |
| tri-incidence t=5 | 93 | 5 | 186/930 | 17856 = 17856 | −40 | 201/280 |
| BvLS | 243 | 10 | 8910/8910 | 0 = 0 | 0 | 0/1540 |

## 3. Mutation (une seule, autorisée) et verdict
*Énoncé muté :* sur curl₀, le spectre comprimé évite l'intervalle ouvert (s', r'). Il est vrai pour BvLS (exactement
{−5, 4}) et pour srg(9) ; pour un SRG, H3 donne alors −||B||² ≥ 0, donc P = P_max, grid-full, contradiction pour 99
(L1). Version approchée avec la frontière (si chaque sommet a ≥ 4 étiquettes tordues : Σ|W| ≥ 792) : il suffirait
Σ_{curl₀} g(κ) > −176.
*Attaque R :* les géométries tordues non SRG violent massivement l'évitement, mais elles ne sont pas SRG
(le terme −2(n − n_SRG) force déjà de la masse intérieure) : contrôle non décisif, et il n'existe aucun SRG tordu à
q = 3 pour tester. Surtout, l'énoncé muté est **équivalent** à « SRG ⟹ grid-full » (conjecture F2-SRG) : aucun
mécanisme ne le rend plus facile. **Verdict : reformulation exacte, pas un levier.** H1–H3 restent des identités
valides (H2 caractérise la torsion comme un commutateur).

## 4. Recherche bibliographique ciblée (autorisée par l'utilisateur)
- **R. Reimbayev, arXiv:2608.19410 (août 2026)**, 208 fréquences de sous-graphes induits d'ordre 7 dans
  srg(n,k,1,2), linéaires en deux variables libres n₃ et z₁₁.
  - *Identification.* z₃₉ (prisme + sommet isolé) = (n − 6k + 15)·P avec P = P_max − n₃/3 ; le coefficient constant
    vérifie nk(k−2)(k−4)(k−8)/24 = (n − 6k + 15)·P_max exactement quand n = 1 + k²/2. Donc
    **n₃ = 3(P_max − P) = ½ Σ_x |W(x)|** : leur variable libre est notre torsion. C'est une confirmation
    indépendante de L15. Aussi z₁ = 3P (prisme + troisième point d'un barreau) et z₈₂ = (n − 6k + 18)·n₃.
  - *Contrôle de la liste* (`reimbayev7.py`, transcription manuelle). Les coefficients de n₃ et de z₁₁ passent la
    règle Σ z_i = C(n,7) exactement. Les constantes ne la passent pas : l'écart est
    −B(19k⁴ − 456k³ + 4484k² − 21752k + 42008)/168, avec B = nk(k−2)(k−4). Il s'explique presque entièrement par
    z₁₇₆ = (1/8)… au lieu de (1/84)… (lecture ou coquille) ; il reste un écart B(k + 6), dû à au moins une autre
    erreur (la mienne ou celle de l'article).
  - *Conséquence pour 99.* La non-négativité des 208 comptages donne seulement 0 ≤ n₃ ≤ 4158 et 2n₃ ≤ z₁₁ ≤ 4n₃.
    La borne supérieure est triviale (P ≥ 0) ; les contraintes qui la fixent (z₁, z₈, z₃₉) ont été re-dérivées
    indépendamment, donc la conclusion ne dépend pas de l'écart ci-dessus. Intégralité : seulement z₁₁ ≡ 0 (mod 4).
    **Le comptage jusqu'à l'ordre 7 ne borne pas la torsion.**
- **S. Lou, M. Murin (MIT PRIMES 2014)**, faits locaux : autour d'une droite L, les 36 voisins extérieurs forment un
  2-facteur à cycles de longueur multiple de 3, dont les triangles sont les prismes. Donc π(L) ∈ {0, …, 10, 12}
  (jamais 11), et γ = 12 partout ⟺ grid-full. Leur Théorème 2.1 (pas de « grille 3×3 moins une arête » induite)
  est dans la portée de nos modèles SAT exacts ; il n'est pas re-vérifié ici. Autres résultats : indépendants
  ≤ 22, 5 ≤ χ ≤ 11. Rien de global.
- **Thakkar–Severini, arXiv:2608.11211 (2026)** : réduction au 12-régulier sur 84 sommets, CP-SAT, construction
  partielle à 70,73 %. Rien de nouveau pour nous.
- arXiv:2308.02978 (automorphismes : 2 | |Aut| ⟹ |Aut| divise 6 ; 7 | |Aut| ⟹ Aut ≅ Z₇) concerne C2/C3.
  arXiv:2508.05871 (complexes de cliques des SRG) ne porte que sur les triangles : sans objet ici.

## 5. Bilan de la route Σν³
La route revient exactement à **majorer n₃ = ½ Σ|W|** (pour 99, il faudrait n₃ ≤ 395 face à la frontière,
qui donnerait n₃ ≥ 396 si elle est complétée). Ni l'analyse de Hodge (confinement réfuté, blocs = reformulation), ni
le comptage de sous-graphes jusqu'à l'ordre 7 (borne triviale) ne donnent de majoration non triviale. La majoration
équivaut à la conjecture F2-SRG (« tout PQ(2,t,2) SRG est grid-full »), au moins aussi dure que l'unicité de BvLS
(ouverte). **Route close sans contradiction.** Ce qu'elle laisse : H0 (à ne pas refaire), H1–H3, n₃ = ½Σ|W|
confirmé par une source indépendante.
