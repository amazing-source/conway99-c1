# 105 — L8 démontré : un point de Hamming impose un plan de Fano, puis une contradiction

*25/09, après-midi. Suite de notes/103 (cas mixte de L8). Consigne : maths pures, pas de solveur ; les seuls calculs
sont des vérifications finies exhaustives (quelques secondes chacune). **Résultat : L8 est démontré.** Aucun sommet
de srg(99,14,1,2) n'est un point de Hamming. La preuve n'utilise pas le SAT de notes/40 ; elle remplace le
« calcul SAT non certifié ».*

## 0. Résumé
| résultat | énoncé | statut |
|---|---|---|
| **L8** | aucun point de Hamming | **preuve** (§1–5) ; quatre vérifications finies |
| squelette de Fano | en un point de Hamming, le nombre ℓ(t) de droites de Γ au-dessus de chaque triangle de Kneser est la fonction d'un plan de Fano sur les 7 classes | preuve + énumération exhaustive (30 solutions = 30 plans) |
| section X | une partition X_P de chaque Q_P, parallèle le long des 84 arêtes hors faisceaux | preuve |
| cas coupe (notes/103 §7) | impossible (preuve indépendante, §6) | preuve + énumération des 2²⁰ coupes |
| lemme spectral | (S_I − 5)(S_I + 2) = −KKᵀ : le graphe isométrique signé a son spectre dans [−2, 5] | preuve (§7) |
| lemme des composantes | un sous-revêtement de degré 1 est la nappe A (cas L7) | preuve (§7) |
| 7-adique | en un point de Hamming, k = rang₇(N − 3I) sur Z^⊥ exactement | preuve + calcul (§7) |
| négatifs | intégralité d'ordre 8 : aucune congruence ; « les triangles NNN forment un 2-cycle » (notes/103 §8) n'est pas établi | calcul ; correction |

## 1. Rappels (notes/103) et règles locales
Au point de Hamming x : Γ₂(x) = ⊔ Q_P (21 paires de classes), Q_P ≅ F₂², les siblings forment un 4-cycle dans chaque
Q_P, et les arêtes génériques forment des bijections φ_{PR} : Q_P → Q_R pour P ∩ R = ∅ (une S₄-connexion sur
K(7,2)). Holonomie d'une page R de l'arête P–P′ : θ_R = φ_{P′P}∘φ_{RP′}∘φ_{PR}. L'équation (K) en P–P′ s'écrit
Σ_R Perm(θ_R) = 2J − I − Sib_P − φ⁻¹Sib_{P′}φ.
*Notations.* Parts(P) = {A_P, π_i^P, π_j^P} (partition antipodale, partitions « même étiquette »). β_{PR} = bijection
induite parts(P) → parts(R). Arête **isométrique** si β(A_P) = A_R ; sinon β_{PR}(A_P) = π_κ^R avec
κ = κ(P→R) ∈ R. G_P = ensemble des arêtes non isométriques en P, vu comme graphe sur les 5 classes hors de P.

**Classification d'arête (`code/fano_verify.py`, V1, V1b ; exhaustive sur S₄³).** En toute arête P–P′ :
- aucune holonomie de page n'est un 3-cycle ; les profils de points fixes |Fix θ_R| sont {4, 0, 0} ou {2, 2, 0} ;
- au profil {2, 2, 0}, les deux transpositions induisent la **même** transposition de parts(P). Elle fixe A_P si
  l'arête est isométrique, et A_P ou π_{κ(P′→P)} sinon (jamais la troisième partition) ;
- en une arête isométrique, les trois holonomies fixent A_P.

**Règles déduites (preuves en une ligne).**
- (T1) *Règle des triangles* : un triangle de Kneser n'a jamais exactement deux arêtes isométriques.
- (i) Triangle {P, P″, R} avec PP″ isométrique et les deux autres non : κ(P→R) = κ(P″→R).
- (Z_A) μ avec les étiquettes (M Z_m = 0, composante A) : en chaque P, l'orientation R ↦ κ(P→R) de G_P a tous ses
  degrés entrants pairs.
- (T2) Donc chaque composante de G_P a un nombre pair d'arêtes. Deux telles composantes demanderaient 6 sommets. G_P
  est donc vide ou connexe à nombre pair d'arêtes.
- (C′) Fait C, projection sur A′ : pour P = ij, P′ = ik, le nombre de pages R ⊂ [7]∖{i,j,k} de transport isométrique
  est pair. Ces pages sont (iso, iso) ou (non, non) avec κ(P→R) = κ(P′→R).

## 2. Les droites de Γ₂(x) : le squelette ℓ
1. Un y ∈ Q_P est sur 7 droites. Deux passent par ses étiquettes (et contiennent ses siblings). Les cinq autres sont
   dans Γ₂(x). Chacune contient deux voisins génériques y_R ∈ Q_R, y_S ∈ Q_S avec {P, R, S} triangle de Kneser : le
   troisième point d'une droite par y, y_R n'est pas une étiquette (étiquettes disjointes), ni un sibling de y (φ
   bijective). Les cinq arêtes {R, S} de Petersen(link P) forment donc un **couplage parfait F(y)**.
2. ℓ(t) := nombre de droites au-dessus du triangle t = {P, R, S}. y est sur une droite au-dessus de t ssi
   θ_t(y) = y. Donc **ℓ(t) = |Fix θ_t| ∈ {0, 2, 4}** (pas de 3-cycle).
3. Le graphe de Petersen a 6 couplages parfaits. Chaque arête est dans exactement 2 d'entre eux, et deux couplages
   se coupent en exactement une arête (V3). Ce sont donc les sommets de K₆, et les arêtes de Petersen sont les paires.
   Avec n_M = #{y ∈ Q_P : F(y) = M}, l'arête M ∩ M′ est couverte n_M + n_{M′} = ℓ fois, nombre pair. Tous les n_M
   ont donc la même parité : ils sont pairs, puisque six nombres impairs font au moins 6 > 4.
   - **Type A** : F(y) est le même pour les 4 points de Q_P. Alors ℓ = 4 sur les 5 triangles de ce couplage, 0 sur
     les autres.
   - **Type B** : deux couplages M, M′, deux points chacun. Alors ℓ = 4 sur leur arête commune t₀(P), 2 sur leurs 8
     autres arêtes, 0 sur les 6 restantes.

## 3. Théorème (squelette de Fano)
**Énoncé.** Les fonctions ℓ sur les 105 triangles de Kneser, compatibles en chaque paire avec le type A ou B, sont
exactement les 30 fonctions de Fano. Pour un plan de Fano Φ sur les 7 classes et t = {P, R, S} de classe manquante v,
on regarde les triples P ∪ {v}, R ∪ {v}, S ∪ {v} :
- ℓ(t) = 4 si les trois sont des droites de Φ (t est le **faisceau** de Φ en v) ;
- ℓ(t) = 2 si aucun ne l'est ;
- ℓ(t) = 0 si exactement un l'est.

Toute paire est de type B, et t₀(P) est le faisceau qui contient P. On a 7 faisceaux, 56 triangles « sans droite »
et 42 « à une droite ».

*Preuve.* Recherche exhaustive, avec 21 options par paire et cohérence sur chaque triangle
(`code/ell_skeleton.py`) : 30 solutions. Elles coïncident avec les 30 fonctions de Fano recalculées indépendamment
(`code/fano_verify.py`, V4). ∎

*Remarque.* Les « familles de 1-factorisations voisines des grands ensembles de plans de Fano » pressenties
(notes/103 §8) se réalisent ainsi. Il n'y a pas de grand ensemble : un seul plan, et le type A est impossible.

## 4. La section X et la dichotomie B / C
Soit X_P la partition de Q_P en {points utilisant M} | {points utilisant M′}.
1. Pour t ∈ M ∖ t₀, les droites au-dessus de t passent par les deux M-points. θ_t fixe exactement ces deux points :
   c'est la transposition des M′-points, qui induit sur parts(P) la transposition fixant X_P. Même chose pour M′. Les
   huit triangles ℓ = 2 par P ont donc la même S₃-holonomie τ_{X_P}.
2. Toute arête **hors faisceau** PQ est dans un triangle ℓ = 2. En conjuguant l'holonomie, on obtient
   **β_{PQ}(X_P) = X_Q** : X est parallèle le long des 84 arêtes hors faisceau.
3. Par la classification d'arête, X_P = A_P si PQ est isométrique, et X_P ∈ {A_P, π_{κ(Q→P)}} sinon.

Soient B = {P : X_P = A_P} et C = {P : X_P ≠ A_P}.

**Lemme B/C.**
- (a) *C est indépendant dans le graphe hors faisceaux.* Soient P, Q ∈ C avec PQ hors faisceau. Si PQ était
  isométrique, on aurait X_P = A_P. Sinon X_P = π_{κ(Q→P)}^P, qui est l'image de A_Q par β_{QP}. Alors
  X_Q = β_{PQ}(X_P) = A_Q, ce qui contredit Q ∈ C.
- (b) Une arête hors faisceau est isométrique entre deux paires de B, et non isométrique entre B et C.
- (c) Soit PQ une arête d'un faisceau (en v, de troisième membre S). Ses deux pages ℓ = 0 sont Y = {s, v}, s ∈ S. Les
  arêtes PY et QY sont hors faisceau, car le point de faisceau de Y est l'autre point de S.
  - Arête B–C : Y est dans B par (a), donc PQ est non isométrique par (T1).
  - Arête B–B : PQ est isométrique dès qu'une de ses deux pages est dans B.
- (d) *C = ∅ est impossible.* Alors toutes les arêtes hors faisceau sont isométriques. Toute arête de faisceau a
  une page dans B, donc elle est isométrique par (c). Tout est isométrique, ce que **L7** exclut. ∎

## 5. Fin de la preuve
1. *Énumération (`code/fano_bc_structure.py`, Φ = {0,1,3} + d, sans perte de généralité).* Le graphe hors faisceaux
   a 722 ensembles indépendants. On impose les statuts forcés par le lemme B/C, puis on essaie toutes les valeurs des
   arêtes de faisceau restées libres, avec (T1) et (T2). **Il reste 35 configurations.**
   - **14 étoiles** : C = les 6 paires contenant une classe, toutes entièrement non isométriques.
   - **21 quadrilatères** : C = les 4 arêtes d'un 4-cycle sur le complémentaire d'une droite L de Φ. Les deux
     diagonales sont les paires du faisceau en un point de L. Il y a une configuration par drapeau de Φ.
2. *Étoiles.* Trois paires par une même classe, entièrement non isométriques : c'est exclu par notes/103 §6 (version
   locale). Le certificat trouvé est exactement cet argument : (C′) pour (0 ; 1,2), (0 ; 1,3), (0 ; 2,3), plus six
   (Z_A).
3. *Quadrilatères (preuve à la main).* Prenons C = {01, 02, 15, 25}.
   - La paire 23 est dans B. Ses arêtes non isométriques sont exactement 01 et 15 : un chemin 0–1–5 sur {0,1,4,5,6}.
     Par (Z_A), les deux arêtes pointent vers le sommet milieu, donc **κ(23→01) = 1**.
   - La paire 45 est dans B. Ses arêtes non isométriques sont 01 et 02 (chemin 1–0–2), donc **κ(45→01) = 0**.
   - Dans le triangle {23, 45, 01}, l'arête 23–45 est isométrique (hors faisceau, dans B), et les deux autres ne le
     sont pas. La règle (i) donne κ(23→01) = κ(45→01), ce qui est **contradictoire**.
   - Le groupe de Φ est transitif sur les drapeaux, donc les 21 cas se traitent de même. Contrôle direct : le système
     linéaire (Z_A, (i), (C′)) est incompatible dans les 35 configurations (`code/fano_verify.py`, V5 ;
     `code/fano_certificate.py` extrait des certificats de 3 à 9 équations).

**Donc aucun point de Hamming n'existe (L8).** ∎

*Ce que la preuve utilise.*
- De notes/103 : la réduction §1, la classification d'arête (revérifiée ici), L7 (trois preuves à la main) et la
  version locale du §6 (pour les étoiles).
- De cette note : le squelette ℓ et la section X.
- Aucun solveur. Quatre vérifications exhaustives, toutes en quelques secondes : S₄³ par arête, squelettes,
  ensembles indépendants, systèmes linéaires sur F₂.

## 6. Le cas coupe, preuve indépendante (antérieure au §5)
Sans triangle entièrement non isométrique, ν est un cocycle. H¹(K(7,2) ; F₂) = 0 (`code/nnn_tools_check.py` : rang
85), donc ν = δ(1_{V₀}) est une coupe.
- Parmi les 2²⁰ coupes, **28 seulement** satisfont (T2) (`code/cut_patterns.py`). Les 7 étoiles V₀ = {paires ∋ i}
  sont exclues par notes/103 §6. Il reste une orbite : V₀ = {paires coupant D = {0,1} en un point}.
- Là, (i) dans les triangles {0a, 1b, R} (R ⊂ E = [7] ∖ D) rend κ(·→R) = κ_R indépendant de la paire de V₀.
- (Z_A) en {d, a} demande que le tournoi R ↦ κ_R sur E, privé de a, ait ses degrés entrants pairs, et ce pour tout a.
  Cela force chaque sommet de E à être une source : impossible.

L'exemple de coupe de notes/103 §7 (paires de {1,2,3,4}) viole déjà (T2).

## 7. Outils obtenus en chemin
- **Lemme spectral.** Avec N = M − 2E_A (notes/103 §1.5), le bloc A donne (S_I − 5)(S_I + 2) = −KKᵀ. Ici S_I est le
  graphe isométrique signé par δ, et K = N_{AL}. Tout sous-graphe induit de S_I a donc son spectre dans [−2, 5]. Le
  bloc des étiquettes a le sien dans [−4, 3], et K N_LL = (1 − S_I)K.
  - *Quatrième preuve de L7* : tout isométrique, avec H¹ = 0, donne S_I ~ A_{K(7,2)}, de valeur propre −4 < −2.
  - *Seconde fin du cas coupe* : V₀ induit K_{5,5} moins un couplage, 4-régulier et biparti. Il faudrait S² = 4I,
    mais deux sommets d'un même côté ont 3 voisins communs.
  - Localement, aucun cône sur Petersen[I_P] n'est exclu : λ_min ≥ −2 toujours (`code/nnn_tools_check.py`).
- **Lemme des composantes.** N est diagonal par blocs selon les composantes du revêtement 𝒢. Proj_Z l'est donc aussi,
  et le support de chaque Z_m est dans une seule composante. La trace sur une composante de degré 1 donne alors
  2z + α ≡ 0 (mod 7) avec α = 21 − 6z, d'où z = 0 et α = 21 : c'est la nappe A, donc le cas L7. Dans tout cas mixte,
  𝒢 est connexe. Une parité de composantes (s + Σ_i C(t_i, 2) ≡ 0) redonne aussi L7.
- **7-adique.** En un point de Hamming, M_x s'annule sur ⟨1_P, Z_m⟩ (`code/hamming_fixed_block.py` : bloc fixe
  nul). Donc **k = rang₇(N − 3I)|_{Z^⊥}**, le rang de recollement entre L₃ (rang 26) et L₋₄ (rang 30) dans
  Z²¹ ⊕ A₅⁷. Cela redonne k ≤ 26. L'excès 7-adique s'annule (forme hyperbolique), donc le genre ne donne rien de plus.
- **Règle NNN** (64 cas) : dans un triangle entièrement non isométrique, le nombre de sommets recevant de façon
  concordante vaut 0, 1 ou 3, jamais 2 (sinon l'holonomie serait un 3-cycle).
- **Correction de notes/103 §8.** « Une arête non isométrique est dans 0 ou 2 triangles NNN » ne découle pas de (K)
  en l'arête : trois pages de statuts (iso, non), (iso, non), (non, non) sont compatibles (`code/nnn_edge_parity.py`).
  Cette affirmation n'a pas servi.
- **Négatif : intégralité d'ordre 8** (`code/order8_padic.py`). Élimination p-adique du système d'ordre 8 (6 032
  équations, 916 inconnues) : aucune condition sur (P, S) modulo 2³, 3², 5 ou 7².
- **Négatif : le système linéaire en κ seul** n'exclut pas tout motif de non-isométrie (il est compatible pour le
  facteur de triangles cyclique). C'est le squelette de Fano qui rend le problème fini.

## 8. Portée pour C1
1. **L8 passe de « SAT non certifié » à « démontré ».** Tout sommet porte de la torsion (|W(x)| > 0). Le cas
   g(x) = 21 de L10 (g(x) ≤ 18) n'est plus un calcul SAT.
2. Comme l'explique notes/100 §4, un plancher de torsion ne suffit pas : le profil de torsion maximale satisfait
   toujours tous les lemmes. La contradiction finale demande un plafond.
3. **Ce que la méthode apporte.** Pour la première fois, la structure générique de Γ₂(x) est contrôlée. Le graphe
   12-régulier à 84 sommets de arXiv 2608.11211 y est vu à travers ses droites. Le principe : les droites au-dessus
   des triangles de Kneser donnent des nombres ℓ pairs (pas de 3-cycle), ce qui produit un squelette rigide.
4. **Planche suivante : transporter le principe aux sommets tordus.** En un sommet quelconque, les droites de
   Γ₂(x) restent 5 par point. Le nombre de droites au-dessus d'une configuration de classes est encore un nombre de
   points fixes d'holonomie. Candidats immédiats : L11 et L14 (encore « SAT non certifié »), dont les sommets sont
   presque de Hamming.
