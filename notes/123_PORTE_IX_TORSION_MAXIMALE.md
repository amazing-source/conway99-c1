# 123 — Porte I_x en torsion maximale (P = 0) : holonomies, hexagones, triangles signés, ombres

*26/09, nuit. Mathématiques pures (partage du dossier n° 3 : C1 prend le cas général, porte I_x à P = 0 ; Astra prend le
Fano tendu). DÉRIVÉ = preuve écrite ; les seuls calculs sont des contrôles exacts sur BvLS = srg(243,22,1,2), où les
mêmes raisonnements s'appliquent avec k = 22. Aucun solveur.*

## 0. Résumé
| résultat | statut |
|---|---|
| prismes sur un triangle T = points fixes de l'holonomie σ_T ; P(x) = Σ_{T∋x} fix(σ_T), 2P = Σ_T fix(σ_T) | DÉRIVÉ |
| hexagones induits : **H + 3P = 213 444** (= formule de Reimbayev 2024, H = 209 286 + n₂) | DÉRIVÉ, contrôle BvLS exact |
| à P = 0 et S = 0 : **H(x) = 12 936 en tout sommet** (comptage local par barreaux, N(q) = 306 + 2s(q)) | DÉRIVÉ ; cadre contrôlé sur BvLS |
| triangles : A_Σ = N₀ − N₂ − 2N₃ vérifie **A_Σ² = 13A_Σ + 68I** ; à P = 0, graphe signé {0, ±1} à deux valeurs propres | DÉRIVÉ, contrôle BvLS |
| ombres : Q_U ≅ arêtes de K₁₂ − τ_u, pour toute étiquette u | DÉRIVÉ |
| **conclusion** : tout cela est automatique ; aucun plafond | — |

## 1. Holonomie d'un triangle
- Soit T = {x, y, z}. Chaque sommet de N₁(x) = N(x) ∖ T a exactement un voisin dans N₁(y) : c'est le second voisin
  commun avec y, par μ = 2.
- Les trois couplages croisés N₁(x) → N₁(y) → N₁(z) → N₁(x) composent une permutation σ_T de 12 points.
- **Un point fixe de σ_T est exactement un prisme de triangle T** : v ~ φ(v) ~ φ²(v) ~ v forme un triangle
  transversal.
- En x, σ_{T_U} = σ_U (la bijection σ de la classe U). Donc P(x) = Σ_{T∋x} fix(σ_T) et 2P = Σ_T fix(σ_T).
- Comptes par triangle (sans hypothèse) : n₀(T) = 32 − fix, n₁ = 144 + 3fix, n₂ = 36 − 3fix, n₃ = fix. Le graphe
  lointain F_T contient 32 − fix(σ_T) triangles, ce qui recoupe notes/114 (où le spectre de F_T est déjà fixé par G(L)).
- À P = 0, M_T = G(L) est sans triangle. Ses seuls 4-cycles viennent des coïncidences S (σ_U(v) = v̄). Sinon, ses deux
  appariements transportés sont disjoints : c'est « ρ sans point fixe » (JOURNAL du 26/09).

## 2. Hexagones induits
**Énoncé.** Dans tout srg(99,14,1,2) : **H + 3P = 213 444**, où H est le nombre de 6-cycles induits.

**Preuve.**
- Nombre total de 6-cycles, par paires opposées : une paire non adjacente est opposée dans 2k² − 7k + 5 = 299
  cycles, une paire adjacente dans C(k − 2, 2) = 66. D'où c₆ = (4 158·299 + 693·66)/3 = 429 660.
- Classement selon les cordes. Deux cordes longues sont impossibles (μ), ainsi que diverses cordes courtes
  (λ, diamant). Les classes restantes sont : L (une longue), S (une courte), SS_o (deux courtes opposées), SS_a
  (deux courtes à sommet commun), SL, et SSL (hamiltoniens des prismes).
- Leurs comptes : SSL = 3P ; SS_o = n₂ = 4 158 − 3P ; SS_a = 8 316 ; SL = 8 316 − 6P ; L = 37 422 + 3P ;
  S = 158 004 + 6P.
- Donc H = 429 660 − (somme) = 213 444 − 3P. ∎

**Remarques.**
- C'est la formule de Reimbayev (arXiv:2409.10620), H = 209 286 + n₂, retrouvée indépendamment.
- Contrôle : la même comptabilité, écrite pour srg(v,k,1,2), donne sur BvLS H = 4 980 690, et le comptage direct des
  6-cycles induits donne 4 980 690.
- Le plafond visé par notes/100 (P ≥ 1152) équivaut à H ≤ 209 988 : H devrait être presque minimal. Aucune
  majoration de H n'est connue.

**Version locale.**
- H(x) = ½ Σ_{q∈Δ_x} N(q), où N(q) est le nombre de couples ordonnés de « barreaux » (u, p) : x ~ u ~ p ~ q, avec
  u ≁ q, p ∈ Δ_x, plus les conditions d'induction.
- Il y a 22 barreaux par q : 2 par les τ-partenaires, 4 par les σ-partenaires, 16 par les génériques. Les exclusions
  se comptent classe par classe.
- **À P = 0 et S = 0 : N(q) = 306 + 2s(q)**, où s(q) est le nombre de droites internes par q dont l'arête opposée
  est une σ-arête. Comme Σ_q s(q) = 84 (chaque σ-arête est sur une seule droite interne), **H(x) = 12 936 en tout
  sommet**.
- Contrôle du cadre (conditions de barreaux ⟺ 6-cycles induits par x) sur BvLS : 122 980 des deux façons.
- Le comptage de troisième ordre est donc localement constant en torsion maximale, comme ceux du premier et du second
  ordre (notes/100, mise à jour 108–109).

## 3. Graphe signé des triangles
- Soient s_T = Σ_{x∈T} p_x, avec p_x la représentation de x dans V₋₄ (Gram 27I − 9A + J). On a BᵀG_VB = 9X avec
  X = 4I + A_Σ.
- A_Σ vaut 1 − (#barreaux) sur deux triangles disjoints, et 0 sur deux triangles qui se coupent.
- Comme BBᵀ = 7I + A et G_V(7I + A)G_V = 189G_V, on obtient X² = 21X, soit **A_Σ² = 13A_Σ + 68I**.
- À P = 0, A_Σ = N₀ − N₂ est un graphe signé {0, ±1}, 68-régulier (32 arêtes positives, 36 négatives), de valeurs
  propres 17 (×44) et −4 (×187).
- Les 7 triangles par un sommet donnent 7 vecteurs orthonormés dans R⁴⁴ (repère ajusté de 231 vecteurs, produits
  scalaires dans {0, ±1/4}).
- Contrôle BvLS : BᵀE₋₅B a pour valeurs propres {0, 6}, et ses entrées ne dépendent que du nombre de barreaux.
- Les 21 identités (X²)_{T_U T_U′} = 0 en x sont des identités de troisième ordre sur les droites internes :
  - elles lient, pour chaque couple de classes, les droites évitant U et U′, les droites σ_U évitant U′, les τ-arêtes
    entre U et U′, et les droites portant deux σ-arêtes en une paire du bloc UU′ ;
  - leur somme est l'identité triviale t₂ + 2t₃ + 3t₄ = 84 ;
  - ce sont des coupes possibles pour un modèle de paires, sans contradiction à la main.

## 4. Ombres et conditions P = 0 aux voisins
- **Bijection d'ombre.** Pour une étiquette u, toute paire q qui évite U a exactement 2 voisins contenant u (μ = 2).
  Deux u-paires non τ_u-adjacentes ont exactement un voisin commun hors de u.
  - Donc q ↦ β_u(q) est une bijection des 60 paires de Q_U sur les arêtes de K₁₂ − τ_u.
  - Deux paires adjacentes de Q_U ont des ombres disjointes, sauf si le troisième sommet de leur droite contient u.
- **P = 0 dans le repère de x.** Tout prisme a ses deux triangles parmi : droite de x, droite d'étiquette, droite
  interne. Il y a donc cinq familles de conditions :
  - (a) τ_u(v) ≠ v̄ ;
  - (b) σ_U sans point fixe, qui découle de (a) ;
  - (c) τ_u ∩ σ_U⁻¹τ_ūσ_U = ∅ ;
  - (i) l'appariement des droites internes en {u,v}, transporté par β_u, évite τ_u ;
  - (ii) aucun prisme entre droites internes.
- Comptes par classe U, à P = 0 et S = 0 : 12 droites uūQ, 48 uQQ, 48 ūQQ, 32 QQQ (les 32 de F_{T_U}).

## 5. Portée
- Tout ce qui précède est une conséquence de A² = 12I − A + 2J et de la structure locale. En torsion maximale, les
  comptes jusqu'au troisième ordre sont localement constants. Aucune contradiction ne peut en sortir.
- Le plafond ne peut venir que des **arêtes génériques effectives**, c'est-à-dire du niveau paire × bloc et au-delà.
- Les bornes ordonnées d'Astra (JOURNAL, dossier n° 3) y mordent dès que les comptes sont fixés. En torsion maximale
  générique, les comptes ne sont pas fixés.
- Piste ouverte : trouver une strate rigide **forcée** à P = 0, par exemple une famille tendue, un G(L) non connexe, ou
  un revêtement (suggestion de « structures », d'après le théorème d'Astra sur les revêtements de K₇ sans prisme).

Scripts (`code/`) : x29_bvls_triangle.py, x29b_hex_bvls.py, x29c_hex_local.py, x29d_sigma_signed.py.
