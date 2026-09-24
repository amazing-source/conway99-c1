# 20 — Chercheur R : attaques (journal des verdicts)

Règle : une idée meurt sur une objection mathématique ou un calcul exact, pas sur une impression.
Scripts dans `code/`, données dans `data/`. Tous les calculs sont exacts (entiers / corps finis), sauf
les spectres flottants signalés.

## Témoins disponibles
- Famille (λ,μ) = (1,2) existante : srg(9,4,1,2) = H(2,3), srg(243,22,1,2) (BvLS). **Les deux sont
  « grid-full »** (τ = mate partout, holonomie triviale) : aveugles à toute idée fondée sur la torsion.
- Analogue q = 2 (λ = 0, μ = 2) : Clebsch (quotient du 5-cube) et **Gewirtz srg(56,10,0,2), qui est tordu**
  (56 ∤ 2¹⁰) **et existe**. Toute idée qui « prouverait » la non-existence par la seule torsion doit être
  confrontée à Gewirtz.
- **Nouveaux témoins tordus (trouvés ici)**, graphes localement (t+1)K₂, λ = 1, μ ∈ {0,2}, non SRG :
  - t = 2 : 20 sommets, 6-régulier, diamètre 3, tordu en tout sommet, |Aut| = 240. C'est le graphe des arcs
    de K₅ : (i,j) ~ (j,k), (k,i) ; droites = triangles orientés ; revêtement double antipodal de T(5).
    (`data/t2_twisted.json`)
  - t = 3 : 39 sommets, 8-régulier, diamètre 3, tordu en tout sommet, |Aut| = 78 ≅ Z₁₃ ⋊ Z₆, 3 orbites de 13.
    (`data/t3_twisted.json`)
  - Contrôle positif du modèle SAT : en imposant τ = mate en 0, n = 27 donne exactement H(3,3).

## Verdicts

### F2 — rigidité q = 3 (« localement (t+1)K₂ + μ = 2 ⇒ grid-full ») — **TUÉE (forme locale)**
`twist_search.py` : exemples tordus pour t = 2 (n = 20) et t = 3 (n = 39). Donc aucun argument purement local
(rayon 2, axiomes λ = 1, μ ∈ {0,2}) ne force τ = mate. La forme SRG (diamètre 2) reste ouverte, sans
mécanisme local.
- *Lemme conservé* (preuve dans 30_LEMMES.md, L1) : grid-full ⇒ revêtement par H(7,3) ⇒ 99 | 3⁷, absurde.
  **Γ est donc nécessairement tordu.**
- *Mutation F2'* (revêtement universel du 2-complexe triangles + quadrangles, argument de divisibilité) —
  **TUÉE** : `complex_homology.py` donne H₁ = 0 sur F₂, F₃, F₅, F₇, Q pour les deux exemples tordus
  (comme pour H(2,3), H(3,3)). Les géométries tordues sont déjà « universelles » ; aucun quotient à exploiter.
- Observation : la torsion *comprime* : à racine fixée, nombre de sommets à distance 3 : H(3,3) 8 vs tordu 1 ;
  H(4,3) 32 vs tordu 6. Le SRG (0 sommet à distance 3) est l'extrême de cette compression.

### F3 — ensembles serrés × transitions — **TUÉE (sous la forme testée)**
`star_interlace.py` : S_a = {x} ∪ N(x) ∪ étoile(a) (27 sommets) est déterminé par τ_a. Pour les 11 types de τ_a
(partitions de 6) : λ₂ = 3 et λ_min = −4 exactement, avec un vecteur propre de somme nulle chacun, identique à
tous les types (ce sont les modules de Terwilliger de dimension 2). Aucune contrainte sur τ.
Raison de fond : les configurations entièrement déterminées par τ sont de degré ≤ 4, donc λ_min ≥ −4
automatiquement ; l'entrelacement ne mord que sur des configurations denses, qui dépendent des triangles disjoints.
- Conservé : les grilles sont serrées ; (A − 3I)g = g_tot·1.

### F1 / F13 — holonomie de droite ρ_ℓ et entrelacement autour d'une droite — **TUÉE (entrelacement)**
`line_config.py` : ℓ ∪ Γ₁(ℓ) (39 sommets) est déterminé par (τ_a, τ_ā, ρ_ℓ). 20 000 tirages, 15 765 localement
valides, **0 violation** de λ₂ ≤ 3 / λ_min ≥ −4, tous types d'holonomie (12), (11,1), (9,2,1), …
Les exemples tordus montrent aussi des holonomies non triviales réalisées.
- Conservé comme vocabulaire (l'holonomie est un invariant canonique). Nom proche dans l'ancien repo (« wave 133 »),
  non utilisé.

### F4 — torsion de Fano / cohérence de classes — **TUÉE (forme locale)**
Pour t = 2 toute torsion est automatiquement cohérente (2 classes restantes) — c'est ce qu'on voit à 20 sommets,
avec une règle de signes de type quaternions (τ_A, τ_C préservent le signe, τ_B l'inverse). Mais l'exemple t = 3
(39 sommets) a **12 à 24 entrées non cohérentes par sommet**. La cohérence de classes n'est pas forcée localement.
Reste une curiosité non réfutée : 99 est le seul cas ouvert avec t + 1 = 7 ≡ 1 (mod 6) (STS(7) = Fano).

### F5 — genre entier / formule d'oddité — **SURVIT comme lemme (pas comme obstruction)**
Lemmes L2, L3 (30_LEMMES.md) : **rank₇(A − 3I) est impair** ; la forme de recollement 7-adique du réseau propre
E₃ ∩ Z⁹⁹ est de type **non scindé** (non hyperbolique). Aucune contradiction ; cohérent avec les deux formules
d'oddité (Λ₃ et Λ₋₄). À comparer à la littérature (Brouwer–van Eijl sur les p-rangs).
Nom proche dans l'ancien repo (codes 7-adiques « non scindés », signe d'Arf) — non utilisé, dérivation indépendante.

### F6 — invariant d'Arf mod 2 — **ABSORBÉE par F5**
Q(S) = e(S) mod 2 : Q(1) = e(V) = 693 impair, donc Q n'est pas nulle sur le radical (la forme n'a pas d'Arf).
L'Arf de q(c) = wt(c)/2 sur C = im₂(A) (dim 54) vaut [det Λ₃ ≡ 3 mod 8] : c'est exactement la donnée
2-adique utilisée dans F5.

### F7 — algèbre T/Δ (piste A) — **ABSORBÉE**
La cohérence « les 4 points W(C,·) d'un quadrangle coïncident » est une condition de fermeture de grille ;
l'algèbre T/Δ mesure la même torsion que F1/F2. Pas de contenu propre.

### F8 — réseau de transition (piste C) × F5 — **SURVIT comme lemme**
Lemme L4 : sur Z₇, Z⁹⁹ = K ⊕ K^⊥ (K = ker B ∩ Z⁸⁴, 7 ∤ det) ; l'action de A sur K^⊥ (29 dim) est forcée
(vérifiée exactement sur srg(9,4,1,2) et BvLS) et son 7-rang vaut **k' = 15**. Donc
**k(x) = rank₇((H − 3I)|_K) = rank₇(A − 3I) − 15 est le même en tout sommet et est pair**, 0 ≤ k(x) ≤ 30.
La partie non mince réalise un recollement 3/−4 maximal (14) ; tout le reste vit dans le 70-espace.
Pas de contradiction : les formules d'oddité de K₃ = K ∩ E₃(H) et K₋₄ sont compatibles pour tout k (calcul).

### F9 — surface des quadrangles Σ — **encodage, pas d'obstruction**
Σ : sommets = 2079 angles, faces = 2079 quadrangles, arêtes = côtés ; un côté est intérieur (2 faces) ssi le
prisme correspondant existe. χ(Σ) = 3P − 4158 (P = nombre de prismes). Grid-full : P = 1386, χ = 0 (231 tores).
Aucune contrainte trouvée sur P.

### F11 — complexe cubique / variété plate — **TUÉE**
Les exemples tordus n'ont pas les fermetures en 3-cubes : 40/160 (t = 2), 0/1248 (t = 3), contre 100 % pour
H(3,3) et BvLS. Les structures tordues ne sont pas des quotients de cubulations plates.

### F10, F12 — non encore attaquées (voir 10_IDEES_F.md).

### F14 — annulation de Krein — **TUÉE**
Paramètres de Krein de srg(99,14,1,2) : q₁₁¹ = 1629/49, q₁₁² = 1188/49, q₁₂¹ = 968/49, q₁₂² = 1458/49,
q₂₂¹ = 1188/49, q₂₂² = 649/49 : tous > 0. Aucune rigidité de design sphérique (contraste : 9 et 243 ont des
paramètres de Krein entiers, Gewirtz non — pas une obstruction).

### Zoo des géométries tordues (témoins non SRG) — résultats
- t = 2 : `twist_zoo.py` : le graphe des arcs de K₅ (20 sommets) est la **seule** géométrie connexe tordue à
  ≤ 34 sommets (UNSAT prouvé pour 21 ≤ n ≤ 34 avec torsion en 0). |Aut| = 240, les 20 σ_x sont des automorphismes.
- t = 3 : 39 sommets, **tripartite** (3 orbites Z₁₃ sans arête interne), blocs d'incidence = ensembles de différences
  planaires de PG(2,3) : D₀ = D₂ = S = {0,1,4,6}, D₁ = −2S = {0,1,5,11}. 13/39 σ_x sont des automorphismes.
- **Famille tri-incidence** (`triincidence.py`, `sidon_tri.py`) : parties Z_N, D = (S, −2S, S).
  q = 3 (N = 13) : tordue, 39 sommets ; **q = 5 (N = 31) : tordue, 93 sommets (t = 5)** ; q = 2, 4 : rien.
  Avec |S| = 4, 6 et N non planaire (Sidon) jusqu'à 30 / 45 : rien. Donc l'ansatz exige un ensemble de différences
  planaire (N = t² + t + 1) : la condition μ force les b − 2a à s'apparier deux à deux.
  **t = 6 : aucune solution pour N = 44…64** (N = 43 exigerait un plan projectif d'ordre 6, inexistant).
  → Idée radicale F17 (10_IDEES_F.md).
- `triincidence.py` q = 7 : **tordue, 171 sommets (t = 7)**, profil (1, 16, 112, 42). La famille marche pour
  q = 3, 5, 7 et échoue pour q = 2, 4. Explication : il faut que −2 ne soit pas un multiplicateur de l'ensemble de
  différences (théorème des multiplicateurs : si 2 | q, 2 est multiplicateur) et que S n'ait pas de 3-progression.
  Excès (sommets à distance 3 d'un sommet) = q(q − 1).
- `tricirc_sat.py` (tri-circulants **généraux** D₀, D₁, D₂, SAT exact) : t = 3 → seulement N = 13 (N ≤ 20) ;
  t = 5 → seulement N = 31 (N ≤ 31). Retrouve exactement la famille planaire. t = 6 : N = 34…60 en cours.
- `twist_zoo.py` t = 3 : n = 39 (PG(2,3)), n = 40, 41 : UNSAT, **n = 42 : une seconde géométrie tordue**,
  56 droites, |Aut| = 672 = 2·|PGL(2,7)|, spectre 8, 3⁸, 2√2⁶, 0⁷, −1⁸, −2√2⁶, −4⁶, excès 9, toutes les σ_x
  automorphismes. La torsion ne vient donc pas seulement des plans d'ordre t : F17 sous forme stricte est affaiblie
  (reste testable à t = 6).
- Tous les exemples tordus trouvés ont un **excès > 0** (1, 6, 9, 20, 42). Un SRG est exactement une géométrie
  d'excès 0. D'où la reformulation F20 = F2-SRG : « torsion ⇒ excès > 0 », non testable à petit t (aucun SRG
  pour t ∉ {1, 6, 10, 55, 496}).

### F15 — point de Hamming — **INDÉCIS**
`hamming_point.py` (modèle exact, 350 280 variables, 818 160 clauses ; contrôle relâché SAT ; aucune contradiction
dans la partie fixe) : Cadical **UNKNOWN après 30 min**. La symétrie W(B₇) (ordre 645 120) n'est pas cassée.
Structure dérivée à la main (valable pour 99) : entre deux grilles par x à classes disjointes, les arêtes
disjointes forment une bijection φ entre leurs 4-cycles ; en chaque sommet de X les triangles réalisent une
quasi-1-factorisation de K₅ sur les 5 classes libres ; les triangles sont une condition de cocycle partiel sur les φ.
À reprendre avec une recherche dédiée (sur le PC du labo).

### Recherche par mécanisme (piste « grid-full »)
- Unicité de BvLS srg(243,22,1,2) : **ouverte** (Wikipédia, 2026). « Tout PQ(2,t,2) est grid-full » impliquerait
  cette unicité (via l'unicité du code de Golay ternaire parfait) : la conjecture est au moins aussi dure.
- Gewirtz : unicité par forçage spectral (Brouwer–Haemers 1993) ; ses sous-constituants ont peu de valeurs propres,
  H ici en a 5 : pas transplantable tel quel.
- Codes parfaits dans les graphes de Doob (Hamming tordus pour q = 4) : exclus pour e ≥ 2 via Lloyd, parce que l'hôte
  est distance-régulier ; pour q = 3 il n'y a pas d'hôte tordu distance-régulier (Egawa).
- Graphes distance-réguliers avec a₁ = 1, c₂ = 2 : pas de classification couvrant le diamètre 2 (elle résoudrait
  le problème) ; 99 n'est pas « géométrique » (clique de Delsarte = 4,5 ≠ 3).

## Contrôle d'antériorité (après les attaques, sur consigne)
L'ancien repo (conway-99-research) est un travail amateur assisté par IA, **non utilisé comme source**. Index de noms
seulement : il nomme une holonomie de triangle (≈ F1), un signe d'Arf 2-adique (≈ F6/F5), un design de transitions
(≈ piste B), un code 7-adique non scindé (≈ F8). **Aucune mention** de quotient de Hamming, de revêtement,
d'exemples tordus, de Gewirtz, de graphe des arcs.


### Validation de la méthode enracinée sur l'analogue q = 2 (`q2_rooted.py`) — **RÉUSSIE**
Même modèle exact (racine, étiquettes, sommets à distance 2 = paires, inconnues = arêtes entre paires disjointes,
toutes les équations SRG) pour λ = 0, μ = 2 :
- srg(16,5,0,2) : SAT, solution isomorphe à Clebsch ; avec une fermeture en 3-cube imposée : SAT (Clebsch en a).
- **srg(56,10,0,2) : SAT en 1,9 s, solution isomorphe au graphe de Gewirtz** (reconstruit de zéro).
- **Gewirtz + une fermeture en 3-cube imposée : UNSAT (13 s)** — cohérent avec l'unicité de Gewirtz et le fait
  qu'il n'a **aucune** fermeture en 3-cube (0/6720, mesuré : il est *maximalement* tordu en chaque sommet).
Conséquences : (i) la chaîne « modèle enraciné + SAT + exclusion d'une configuration locale » donne la bonne
réponse sur un SRG tordu connu, dans les deux sens ; (ii) **contre-poids heuristique** : dans l'analogue q = 2,
« torsion maximale partout » est exactement ce que fait le seul SRG tordu connu — la torsion forte n'est donc pas
un argument contre l'existence ; reste l'argument du groupe d'automorphismes (|Aut(Gewirtz)| = 80 640, contre ≤ 3
pour Γ). (iii) Pour q = 2 le problème enraciné complet se résout en 2 s ; pour 99 il est ~10× plus gros (2 562
inconnues + τ contre 630) et des heures de SAT (ici et ailleurs) n'ont rien trouvé : indice faible de non-existence.

### F23 — confinement local→global du spectre de Hodge — **TUÉE** (détails : notes/60_HODGE.md)
- L'identité de Garland localisée aux sommets redonne seulement L₁ = 15 + Q (le lien K₁₄ voit tout sauf les arêtes
  opposées, c'est-à-dire exactement Q).
- **Théorème H0** : confinement ⟹ M = Q² + Q − 12 = 0 ⟹ P = P_max ⟹ grid-full ⟹ M ≠ 0 dès que t ≥ 2 (deux
  2-chemins de même signe dans le revêtement de Hamming). Le confinement est donc faux pour *tout* SRG de la famille
  avec t ≥ 2 : le démontrer pour 99 revient à démontrer la non-existence, sans gain.
- Contrôle BvLS (prédiction par théorie des représentations, puis calcul `hodge_blocks.py --big`, 24 s) : spectre
  rotationnel {−20^11, −5^660, −2^660, 4^880, 7^220} : 231 valeurs hors de [−5, 4], 660 dedans.
- Mutation F23' (évitement sur curl₀) : équivalente à F2-SRG. Reformulation, pas levier.
- Recherche bibliographique : Reimbayev 2026 (ordre 7) a pour variable libre n₃ = ½Σ|W| (notre L15) ; la
  non-négativité des 208 comptages ne donne que 0 ≤ n₃ ≤ 4158 à (99,14). Le comptage ne borne pas la torsion.
