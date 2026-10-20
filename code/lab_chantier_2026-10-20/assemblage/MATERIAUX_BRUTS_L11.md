# Matériaux pour la recombinaison : extraits bruts des fiches (copie verbatim)

Chaque bloc renvoie à fiches/<lot>.md:<lignes>. Les statuts et sources sont ceux des fiches.



<!-- ===== L11a_pont.md:336-457 ===== -->

## Matériaux pour la recombinaison

### 1. Conditionnels « si X, alors contradiction ou exclusion »

| # | X (précis) | statut de X | conclusion | source |
|---|---|---|---|---|
| K1 | T20 (+ T16, T18, Théorème R, complétude du producteur et des recherches) | T20 : P + deux programmes, « accepté » par l'utilisateur pour des sessions IA seules | les ≈ 2,4 M paires différées des 13 réseaux tombent ; 156/156 ; pas d'involution | pont:#6, #72, #80 (L11a-01, -31) |
| K2 | T18 et T20 ; une racine r de U avec (r,y1) = ±2 | P / C | ce y1 ne porte aucun repère, quel que soit y2 (Corollaire Y1) | pont:#62–#64 (L11a-27) |
| K3 | « aucune fonction propre entière (σ-impaire) de norme 22 » (T22) | O (non revendiqué, L02_C2_aws-167) | les paires de 003 d'énergie minimale 11 tomberaient ; une paire sans témoin E ≤ 10 a un minimum dual ≥ 12/7 | pont:#61 (L11a-28) |
| K4 | un vrai repère n'a pas de h de norme 4 d'empreinte nulle | O (prouvé pour 129 réseaux, audit E pour 25) | noyau rigide complet par preuve | pont:#52 (L11a-23) |
| K5 | le jumeau a strictement plus de racines | P (induction, accepté par Codex) | transfert « twin with strictly more roots » sûr sans identifier le jumeau | pont:#107, #109 (L11a-38) |
| K6 | une configuration de Fano existe (min L = 14) | ouvert par rang ; exclue à r = 37 par N14 (L06-092, E) | rang_7(A − 3I) = 33 + rang(S \| ker D_2) ≥ 33 ; à r ∈ {39,41,43} : rang(S \| ker D_2) = r − 33 | pont:#126, #127 (L11a-52, -53) |
| K7 | deux configurations de Fano distinctes forcent rang_7 ≥ 35 | O (non établi, pont:#149) | r = 33 exclu sans extension (sans objet ensuite) | pont:#145 (L11a-75) |
| K8 | au plus 13 (puis 10, puis 4) vecteurs de norme 16 par graine | P | r = 33 force un Fano, puis a_7 ≥ 14 / 42 / 94 / 66 (cert.) | pont:#143–#150 (L11a-66) |
| K9 | a_9 ≤ 497 122 ; ou ≤ 53 vecteurs de norme 18 par graine indépendante | O (sans objet) | r = 33 exclu | pont:#147, #149 (L11a-68) |
| K10 | un cœur de norme 16 engendre k classes indépendantes de Q_r | O | r ≤ 45 − k dès qu'un tel vecteur existe (k = 4 ⇒ r ≤ 41) | pont:#155 (L11a-74) |
| K11 | une famille de k vecteurs courts de L1 a un Gram de rang > 45 − r mod 7 | P (critère) | la famille est impossible au rang r | pont:#159 (L11a-74) |
| K12 | 16a_9 + a_13 < 329(7^m + 1) − 2a_8, m = (45 − r)/2 | C (identité) ; X ouvert | le rang r est exclu | pont:#178 (L11a-87) |
| K13 | r = 35 : a_9 ≤ 10^6 et a_13 < 4 837 873 | E (PL) ; X ouvert | r = 35 exclu (remplacé : r = 35 exclu plus tard, L05-017) | pont:#178 (L11a-88) |
| K14 | r = 37 : a_9 ≤ 10^4 et a_13 < 757 806 (ou a_10 + a_11 + a_12 < 13 521) | E ; X ouvert | r = 37 exclu | pont:#178 (L11a-88) |
| K15 | r = 39 : a_9 ≤ 1 000 et a_13 < 83 316 | E ; X ouvert | r = 39 exclu | pont:#178 (L11a-88) |
| K16 | r = 41 : a_9 = 0 et a_13 < 11 686 | E ; X ouvert | r = 41 exclu | pont:#178 (L11a-88) |
| K17 | r = 43 : a_9 = 0 et a_13 < 1 870 | E ; X ouvert | r = 43 exclu | pont:#178 (L11a-88) |
| K18 | norme 18 seule à r = 37 : moins de 49 392 vecteurs ; à r = 39 : moins de 7 074 | E ; X ouvert | scénario « norme 18 seule » exclu ; il faut alors ≥ 1 063 860 (r = 37) ou ≥ 106 246 (r = 39) vecteurs d'autres normes | pont:#171, #172 (L11a-82) |
| K19 | vecteur de norme 18 unique par graine indépendante (a_9 ≤ 9 240) | O | r = 37, 39 reportés sur les autres normes ; r = 43 intact | pont:#171 (L11a-82) |
| K20 | chaque couche a_8..a_13 < 4,8 M | O | r = 35 exclu (remplacé) | pont:#171 (L11a-82) |
| K21 | b_1 = 0, b_2 ≤ 3 234, b_3 ≤ 32 340 | H, retiré (pont:#142) | r = 39, 41, 43 exclus | pont:#135 (L11a-65) |
| K22 | borne prouvée sur les vecteurs de norme 6 de M (< 10^6 ; < 80 000) | H, retiré | r = 41, 43 (resp. 39) exclus | pont:#136 (L11a-65) |
| K23 | tout cœur de norme ≤ échelle(r) a un seuil de rang > r, pour chaque r impair de la fenêtre | O (seuils norme 16 : 17/15/19/17/15, insuffisants) | C1 exclu | pont:#139, #141 (L11a-61) |
| K24 | configuration biplan minimale dans un srg(243) réel | E : absente des deux connus | (si présente) aucun argument uniforme de famille ne tuerait la norme 14 | pont:#120, #123 (L11a-50) |
| K25 | un vecteur de norme 22 de L1 \ L avec 33 triangles d'une partition commune | H | coordonnée ternaire, élément de ker(Nᵀ mod 3) ; 198 transversaux ⇒ vecteur (−4) | pont:#159 (L11a-77) |
| K26 | r = 45 | P | impossible (pas de réseau pair unimodulaire de rang 44) ; r impair (Milgram) | pont:#130 (L11a-56) |

### 2. Bornes quantitatives (objet, inégalité, statut, source)

**C2 / T20**
- Paires en attente de T20 : ≈ 2,4 M sur 13 réseaux (relais, pont:#6).
- n_3 = 0 : e(X_2) = e(X_0) + 27 ; 27 ≤ e(X_2) ≤ 36 (P, #8) ; e(X_0) ≤ 8, e(X_2) ≤ 35 (P, #28) ; profil (4,2,1) : e(R) ∈ {0,2,4}, e(X_2) ≤ 34 (P, #31) ; (3,4,0) : e(X_0) ∈ {0,…,8} pair (P, #32).
- Σ (a_2 − 6)² + … = 44 (n_3 = 0) ; 55 − 16|U∩V| (n_3 = 2) (P, #8).
- Bases n_3 = 2 : 640/4608/1536/2176/2432/1536 → 186/1356/452/638/718/452 → 136/712/262/365/439/225 → 44/227/87/121/146/75 = 700 → 533 (E, deux programmes, #38).
- Route A : ≈ 2 M nœuds pour une base lourde ; 173 M nœuds pour 160 bases ; ≈ 1 000 cœur-heures par programme ; max 12,6 M nœuds (E, #41, #45).
- Route B : 1 173 102 → 686 675 → 8 557 ; 12 557 760 → 7 461 476 → 55 971 ; 64 528 bases = 64 498 classes ; 86 968 nœuds ; 0 complète (E, #46, #57).
- n_3 = 0 (I.0, (4,2,1)) : 178 768 → 11 322 → 3 022 ; 33 511 nœuds (E, #18).
- Règle duale : N(k,m) ∉ {3, 5, 6} suffit (P, #21).
- Empreinte nulle : Σ(β,h)² = 8(H1 + H2) − 4Σh_j|P_j h|² ≥ 8|H1 − H2| ; H1 + H2 = r/8 + 2 ; 129 réseaux complets ; 3 à 378 droites d'empreinte nulle dans les 24 autres (P, #52).
- Couches : N3 = 4096 ; N4 = 196 560 − 24(N2 + N3) = 98 256 − 24N2 ; |U4/±| = 49 128 − 12r ; 22 892 544 droites de norme 7 ; M²Σ|G_ij| ≤ 2 928 240 < 2^63 (C, #56, #72–#77).
- Corollaire Y1 : |(r,y_i)| ≤ 1 pour toute racine (P sous T18, T20, #63) ; 96/182 (003), 9 143/10 802 (55 réseaux), 4 073/4 334 (28 réseaux) représentants tués au niveau y1 (C).
- Empilement : au plus un vecteur impair du repère avec |(.,β)| = 3/2 par nouvelle racine ; Σ_u m_j(u) ≤ #nouvelles racines de S_j (P, #94).
- 143 : Σ_{42 u}|P_V u|² ≤ 7 dim V ; 2c ≤ 56 ; 4a + 16b ≥ 9 ⇒ 378 ≤ 336 (P, #69, #79).
- Piège caractéristique : (z,y1)² + (z,y2)² > 66 exclut (P, #107).
- Type de racines : n1 = 2h − 4, rang = 4m/(n1 + 4) (P, #110).
- 28 réseaux : 173 708 paires → 63 044 / 78 048 / 29 964 / 2 652 ; 1 042 sans aucun témoin (C/E, #87, #107).
- Transferts : 592 864 217 paires ; 32 265 417 / 1 300 094 / 2 863 005 (E, #107) ; résidu ≤ 2 479 669 paires, 11 234 représentants (E, #111).

**C1**
- min L ≥ 14 (P, #120) ; normes ≤ 16 binaires (P, #121) ; h ≥ 2 ⇒ norme ≥ 20 (P, #124) ; norme 18 : e ≤ 1 ; norme 20 : binaire, e ≤ 1 (P, #149, #170).
- Famille (v,k,1,2), k = u² + u + 2 : demi-support m ≥ 1 + u(u+1)/2 (P, #120) ; dans BvLS et le 243 tordu, vecteurs (−5) entiers de norme ≥ 24 (P + E, #124).
- Configuration de Fano : 70 sommets X (28 apex, 42 autres), 15 Z ; diagonale du projecteur 10/49 et 12/49 ; rang 16 ; triangles 28/21/21/105/56 (P, #125, #130).
- rang_7(A − 3I) ≥ 33 si min L = 14 ; = 33 + rang(S | ker D_2), ker D_2 de dimension 65 (P, #126, #127).
- det L = 9·7^(r−1) ; det L1 = 7^(r−1) ; det M = 7^(45−r) ; min(L1 \ L) ≥ 22 (P, #121, #130).
- Hermite : γ_44 ≲ 6,6 ; min L ≲ 18 / 21 / 45 pour a = 22 / 25 / 43 (H, #120).
- Norme 16 : 5 cœurs ; 4 985 attaches, 478 orbites ; seuils 17/15/19/17/15 ; 28/26/30/28/26 si A_Z − 3I inversible (E, #129, #141).
- PL : r ≤ 27 infaisable ; a_7 ≥ 2 558 811 (opt.) ou ≥ 2 008 218 (cert.) à r = 29 ; a_7 ≥ 316 / ≥ 300 à r = 31 ; a_8 ≥ 100 986 / ≥ 96 526 à r = 33 sans Fano (C, #135, #138).
- Échelle de min L1 : 16/20/20/24/24/26 puis 18/20/24/24/26 pour r = 35..43 (C, #135, #151).
- b_2 ≥ 462 ; b_3 ≥ 24 948 ; b_4 ≥ 388 080 puis ≥ 1 431 738 (F1 212 058 + F2 831 600) ; b_5 ≥ 196 812 (audités) ; ext3 : b_5 ≥ 17 668 728, b_6 ≥ 23 272 326, b_7 ≥ 5 987 520 (non audités) ; note 175 : b_5 ≥ 18 001 368, b_6 ≥ 86 272 956, b_7 ≥ 208 016 424, b_8 ≥ 263 126 556 (E/P, #135, #151, #164).
- Max b_4 compatible à r = 33 : 1 049 063,5 / 1 159 234,7 / 1 214 320,3 / 5,78 M selon le plafond sur a_8 (E, #151) ; à r = 35 : max b_4 ≈ 9,8 M, max b_3 = 661 138 (E, #151).
- Plafonds : a_7 ≤ 7 920 ; b_1 ≤ 3 784 → ≤ 88 ; a_8 ≤ 90 090 → 69 300 → 27 720 → 6 930 ; 7a_7 + 8a_8 ≤ 55 440 ; graines : 99·560 = 55 440 (P, #142–#157, #175).
- Fano : exactement 21 triangles à +1 et 21 à −1 ; 42 vecteurs de triangles non orthogonaux à chaque racine ; deux Fano distincts : |(f,h)| ≤ 6 (P, #134, #138, #175).
- Abondance (E, #142) : r = 33 : 128 / 81 322 / 93 171 / 131 751 / 12,4 M (normes ≤ 16..24) ; r = 35 : 3 357 / 6 117 / 136 011 ; r = 37 : 7 / 413 / 16 647 / 49 392 ; r = 39 : 1 974 / 7 074 ; r = 41 : 234 / 1 029 ; r = 43 : 165.
- r = 33 (avant exclusion) : a_7 ≥ 14 / 42 / 94 ; a_9 ≥ 497 124 ; a_7 + a_9 ≥ 5 075 (E, #143, #147).
- r = 35 : ≥ 994 vecteurs de norme ≤ 18 ; norme 18 seule : a_9 ≥ 55 172 ; a_8 + a_9 ≥ 5 829 ; a_7 + a_9 ≥ 994 (E, #151, #155).
- r = 37 : a_10 ≥ 574 (norme 20 seule) ; a_9 + a_10 ≥ 82 ; ≥ 413 vecteurs de norme ≤ 22 (E, #155).
- r = 43 : a_7k = b_k ; a_14 − b_2 = −288(a_7 − b_1) ; a_7 ≤ 88 ; ≥ 166 vecteurs dans 48 classes ; ≥ 140 dans une couche ; ≥ 18 dans une classe ; ≥ 110 ou ≥ 329 selon les couches vides (P/C, #142, #168, #169, #176) ; a_7 ≤ 5 189 à r = 41 (E, #175).
- Identité universelle : constantes 2 632 / 16 450 / 113 176 / 790 258 / 5 529 832 ; 16a_9 + a_13 ≥ 5 515 972 / 776 398 / 99 316 / 2 590 pour r = 35/37/39/41 (C, #178).
- Tableau à travers les rangs (E, #171) et bornes hautes du PL sur a_13 : 40 M / 28 M / 9 M / 2,4 M / 295 000 (E, #178).
- p-rangs : rang_2(N) ≥ 72, rang_5(N) ≥ 72, rang_3(N) ≥ 77 (P non relu, #159).
- Q_r : dimension 45 − r, type moins, indice de Witt (45 − r)/2 − 1 ; au plus 5 Fano orthogonaux indépendants à r = 33 (P, #145).
- Côté +3 : A_5 = 1040 + 52G, G ≤ 231 ; B3 ≥ 1 386, B4 ≥ 12 474, B5 ≥ 182 952 ; ν ≤ 20 (≥ 667, puis ≥ 1 844 vecteurs) à r = 35 (P/E, #160–#166).
- Recollement : (Q, Q̄) = (10, 25) : 14 586 264 ; au plus un vecteur de norme ≤ 24 par classe de M/(√7L1) ; partenaires ≥ 40 (racine), ≥ 38 (norme 4 supplémentaire) (E/P, #164).
- 243 : 3 592 512 candidats biplan par graphe ; 4 838 130 couples d'arêtes anticomplètes ; (N0..N3) = (133 650, 240 570, 0, 8 910) et (140 130, 221 130, 19 440, 2 430) (E, #123, #138).

### 3. Lemmes ouverts et étapes manquantes (ce qu'ils donneraient)

| lemme ou étape | ce qu'il donnerait | source |
|---|---|---|
| majorations prouvées de a_9 et a_13 (normes 18 et 26) | exclusion des rangs via K12–K17 | pont:#171, #178 |
| borne par graine en norme 18 (c manquants différents, type (1,1,1,1), e = 1) | majoration de a_9 ; seuil ≈ 5 par graine indépendante à r = 37 | pont:#172, #174 |
| comptage des vecteurs de L1 \ L de norme 26 | majoration de a_13 | pont:#178 |
| nombre de classes de Q_r engendrées près d'un cœur 16 | r ≤ 45 − k | pont:#155 |
| « deux Fano ⇒ r ≥ 35 » et analogues pour des paires de cœurs | exclusions de rangs par bornes de bloc | pont:#145 |
| extension de la configuration de Fano (groupe d'ordre 336) ; critère K² = 147K | min L ≥ 16 si elle meurt | pont:#120, #125 |
| extension des cinq cœurs de norme 16 (478 orbites) | min L ≥ 18 si ils meurent | pont:#129, #141 |
| existence de vecteurs primitifs de norme 4 dans M | contrôle de b_2 (≤ 3 234 avec triangles et prismes seuls) | pont:#136 |
| T22 (énergie 11) | paires E = 11 de 003 (C2) | pont:#61 |
| preuve d'absence de h d'empreinte nulle | H2 par preuve | pont:#52 |
| recertification exacte des transferts jumeaux | lever la réserve du papier (≤ 2 479 669 paires) | pont:#111 |
| explication à la main de la mort rapide des bases T20 ; analogue (3,4,0) | preuve de T20 sans calcul | pont:#18, #32, #34 |
| usage des p-rangs de l'incidence | contrainte sur les F_3-coordonnées | pont:#159 |
| vérificateur Lean des certificats (143, Y1, Farkas) | formalisation partielle | pont:#79, #83, #87 |

### 4. Méthodes transférables (analogies ; en quoi les objets diffèrent)

- **Budgets λ/μ autour d'un ancrage** : l'isolation (4,2,1) et β = 1 de T20 (ancrage : sommet fixe p de σ et ses sept blocs) et les bornes par graine de C1 (ancrage : graine p0 + 4 voisins, clôture par seconds voisins communs). Différence : sans σ, il n'y a ni orbites ni sommet fixe ; la clôture se fait par « ensembles déterminés » à partir de la graine.
- **Minimum d'un réseau contre petits vecteurs construits** : règle duale H6 (C2, réseau du repère de rang 24, min L* ≥ 8/7) et descentes (R1)/(R2) de C1 (réseau L1 de rang 44, min(L1 \ L) ≥ 22 contre f_T). Même mécanisme « x − v doit rester long » ; objets et normes différents.
- **Identité de séries thêta forçant la complétude d'une énumération** (H3, d4 + 24d2 + 24d3 = 0) : transposable pour certifier des listes de petits vecteurs de M ou L1 en C1 si une identité à déficits positifs existe ; en niveau 7 il reste sept paramètres libres, donc ce n'est pas immédiat.
- **Tri à une seule coordonnée avant le producteur** (lemme à y1 fixé) ↔ en C1, un seul vecteur court force une contrainte globale (Fano ⇒ rang ≥ 33 ; une racine de M ⇒ partenaires ≥ 40).
- **Certificats linéaires rationnels** (143 : 378 ≤ 336 ; identités de Farkas entières de C1) : mêmes objets formels, candidats naturels à un vérificateur Lean.
- **Bornes de rang par blocs** : borne « partie impaire ≤ 22 » de T18/T20 (rang réel d'un Gram) ↔ borne de bloc mod 7 de C1 (rang_7(A − 3I), invariant global r). L'une borne un rang réel, l'autre un rang sur F_7.
- **Contrôles négatifs de vérificateurs** (témoin demi-entier ; unité invalide ; plan tronqué) : applicables à tout vérificateur de certificats C1 (Farkas, comptes de graines).
- **Type exact d'un système de racines par comptage entier** (n1 = 2h − 4) : remplace un rang flottant partout (C1 : racines de M de type A_1^k).
- **Induction descendante sur un invariant entier** (transfert vers un jumeau plus riche) : schéma réutilisable si l'on ordonne des objets C1 par un invariant entier strict (pas d'analogue identifié dans le lot).
- **Bancs d'essai de famille** (tour 3 × 3, BvLS, 243 tordu) : un énoncé uniforme en (v,k,1,2) doit y être testé ; le biplan est présent à u = 1 et absent à u = 4, donc les exemples ne décident pas.

### 5. Combinaisons candidates (pour la vérification adverse)

1. **L07_C1_asym_local-118 × L11a-50** : BvLS a au moins 1 691 cocliques de Hoffman de taille 45 (le graphe tordu aucune) et aucun vecteur propre entier (−5) non nul de norme < 24. Pour deux cocliques de Hoffman C ≠ C', 1_C − 1_C' est un vecteur propre entier (−5) de norme 2|C \ C'| ; donc |C ∩ C'| ≤ 33 pour toute paire de cocliques de Hoffman de BvLS (la valeur 34 est exclue). Fait de banc d'essai, pas une exclusion ; analogue à 99 : |C ∩ C'| ≤ 15 pour deux 22-cocliques (min L ≥ 14), avec égalité ⇔ configuration de Fano.
2. **L11a-71 × L05-001 / L06-002** : la fenêtre {35..43} ne dépend pas du lemme « norme 14 ⇒ r ≥ 33 » pour r ≤ 31 ; une chaîne d'exclusion de C1 peut s'en passer.
3. **L11a-53 × L06-092 (N14 à r = 37)** : une configuration de Fano n'est possible qu'à r ∈ {39, 41, 43} et y force rang(S | ker D_2) = r − 33 ∈ {6, 8, 10} sur un sous-espace de dimension 65 : contrainte exacte à ajouter à toute recherche d'extension de la branche de Fano.
4. **L11a-85 × L11a-68 × L11a-88** : avec ≤ 2 vecteurs par (graine, c manquant) dans un type, ≥ 6 graines indépendantes par vecteur et les seuils K15–K17, une borne complète par graine en norme 18 (≈ 5 par graine indépendante pour r = 37 ; a_9 ≤ 1 000 pour r = 39) rendrait les conditionnels actifs, à condition de majorer aussi a_13.
5. **L11a-77 × L03b_session_eeaf2d22-207** : rang_3(N) ≥ 77 borne à 22 la dimension des F_3-fonctions nulles sur tout triangle ; à confronter aux codes ternaires (code PQ centré, distance duale ≥ 4 à P = 0) de L03b-207.
6. **L11a-58 (N2 = 0 contre 19 440)** : invariant combinatoire simple séparant les deux srg(243) connus ; utile pour calibrer tout énoncé « uniforme en famille ».



<!-- ===== L11b_pont.md:374-518 ===== -->

## 9. Matériaux pour la recombinaison

### 9.1 Conditionnels « si X, alors exclusion »

| # | X | conclusion | statut de X | statut de l'implication | source |
|---|---|---|---|---|---|
| K1 | une exclusion du rang 43 n'utilisant que des entrées monotones (min 14, caps a_7, a_8, minorations b_n, racines orthogonales) | exclusion de TOUS les rangs | O | P (LAP, non audité) | L11b-36 c (pont:#237) ; L06-156 |
| K2 | 2a_8 + 16a_9 + a_13 < 2632, ou b_2 < 914 (seuil relevé à 922 puis 968), ou b_3 < 6 696 790 | rang 43 exclu | O (aucun majorant connu) | E (LAP), formules reproduites par Codex | L11b-42 (pont:#244, #245) |
| K3 | b_4 > plafond (15 972 863 ; 15 196 716 à ρ = 126 ; 15 197 980 via Fano à ρ = 126) ou b_4 + (651/34)b_3 > 16 851 675 | rang 37 exclu | O : minoration certifiée de vecteurs distincts b_4 ≥ 3 371 634 seulement | C (plafonds) | L11b-66, L11b-72, L11b-87 |
| K4 | b_4 ≥ 18 M seul ; ou b_3 ≥ 150k et b_4 ≥ 15 M ; 300k et 12 M ; 600k et 6 M ; ou b_3 ≥ 900k | rang 37 exclu (anciens plafonds) | O | E (frontier37) ; coupé exactement par Codex (16,839 / 14,527 / 11,655 / 5,910 M) | L11b-13, L11b-15 |
| K5 | a_9 ≤ 20000, a_8 ≤ 866, et un cap ~6·10^5 sur a_13 | rang 37 exclu | O | E (needs37, « et si ») | L11b-13 |
| K6 | 3 320 240κ_18 + 2 716 560κ_20 + 740 880κ_22 + 226 380κ_24 (+ types sans graine) < 15 241 977, avec les comptes de graines corrigés (a_9 ≤ 9240κ_18, a_10 ≤ 7920κ_20) | rang 37 exclu | O (lemmes par graine ouverts) | E | L11b-65 |
| K7 | pas de 22-coclique (ou au plus une) | a_7 = 0 à tout rang, plus de profil C ; au rang 37, plafonds 14 444 540,6 / 15 409 176,2 | O | P (note 165 ; LAP) ; plafonds C | L11b-50, L11b-53. **ATTENTION** : la suite « ⇒ rang 37 exclu » est invalidée (pont:#257 C) |
| K8 | g(l) ≤ 3 pour toute droite (τ_g ≤ 6ρ) | τ_g ≤ 693, ρ ≤ 115 ; budget doublé (~30 300) ; limite sans marge contre 27 818 | O | H (flottant) | L11b-60, L11b-78 |
| K9 | 27 828τ_g + 31 976τ_n + (canaux hors C6) < 17,1 M (τ_g < 614 sans hors-grille ; τ_n < 535 sans grille) | rang 37 exclu | O | H (flottant, collection de Codex) | L11b-86 |
| K10 | ρ ≲ 58 sans paire hors grille (via τ_g(ρ) : ρ ≤ 50 → τ_g ≤ 515 ; ρ ≤ 30 → 308) | rang 37 exclu (comptabilité) | O | H | L11b-87 |
| K11 | au rang 37, au plus 10 relations mod 7 indépendantes au-delà des faisceaux | rang 37 exclu | **R** (cible fausse) | — | L11b-88 |
| K12 | sur la collection de Codex, constante totale par paire jumelle < ~13 900 (k = 2) | point de grilles exclu | impossible : plancher certifié 16 496 | H | L11b-73 |
| K13 | un mineur non nul d'ordre 19 (ou 20 augmenté) sur « droite centrale + 18 droites latérales » à P = 0, pour toutes les données d'intersection | contradiction au rang 37 | O | P (Codex, formulation) | L11b-92 |
| K14 | (a') uniforme + NT | à P = S = 0 et k = 22 : toutes les droites (6,6) (note 126 §3 ter) | O, O | P sous hypothèses (Codex) | L11b-96 |
| K15 | un Gram de vecteurs du noyau de rang > 56 − r mod 7, ou de rang 19 à déterminant principal carré au rang 37 | contradiction | — (critère) | P / C | L11b-81, L11b-90 |
| K16 | un majorant de a_13 (norme 26 de L1) de quelques 10^5 | plafond b_4 ≤ 11,0 M ; forcerait C_total ≥ 42,6 M au point de grilles | O | E (sensibilités de LAP) ; à recalculer sur la bonne collection | L11b-63 |
| K17 | un majorant de b_2 au rang 37 (par exemple b_2 ≤ 1000) | plafond coupé via l'identité de LAP | O (Codex : aucun) | C (identité) | L11b-67 |
| K18 | « (6,6) partout » et des relations entre h_T engendrées localement à 14 près | contradiction | équivaut à la non-existence (LAB) | — | L11b-96 |

### 9.2 Bornes quantitatives

| objet | borne | statut | source |
|---|---|---|---|
| r = rang_7(A − 3I) | r ∈ {37, 39, 41, 43} | C | L11b-12 |
| a_7 (Fano, norme 14 de L1) | ≤ 990 → ≤ 842 → a_7 + 13ρ ≤ 2013, 14a_7 + 25P + 32ρ ≤ 28182 ; ≤ 374 à ρ = 126 ; ≤ 388 à ρ = 125 | P → C | L11b-10, L11b-39, L11b-72 |
| a_7 | ≤ 9h (h = nombre de 22-cocliques) | P (non audité) | L11b-54 |
| a_7 | = 2·#{paires de 22-cocliques se coupant en 15} | P | L11b-50 |
| a_7 + 4b_1 ; 7a_7 + 8a_8 + 273b_1 | ≤ 990 ; ≤ 55440 | P (LAP, non audité) | L11b-36 |
| b_1 (racines de M) | ≤ 88 → ≤ 78 → ≤ 44 (tous rangs) | P | L11b-03, L11b-44, L11b-49 |
| b_2 | ≥ 462 + 41b_1 + b_1²/2 (tous rangs) ; ≥ 462 + 42b_1 (LAP) ; sécantes ≥ 462 − 2j(j+1) + (42 + 2j)b_1 ; ≥ 84b_1 − 462 | P / C | L11b-44, L11b-36, L11b-53, L11b-72 |
| b_2 au rang 43 | ≥ 922 → ≥ 968 (≥ 506 non triangulaires) ; intervalle LAP 914 ≤ b_2 ≤ 376 369 | P / E | L11b-44, L11b-49, L11b-42 |
| b_2 à l'optimum du rang 37 | ≈ 2480 nécessaires à l'adversaire | E | L11b-67 |
| b_3 (norme 6 de M) | 24 948 → 40 968 → 43 848 → 45 528 → 45 766 → 45 898 → 45 964 ; P = 0 : ≥ 73 920 ; ≥ 70224 − (61/3)P − 74ρ ; ≥ 73920 − 20P − 72ρ − 4τ (LAP) | C (sauf LAP : P) | L11b-19 … L11b-87, L11b-29 |
| b_3 au rang 43 | ≥ 46 000 ; intervalle LAP 6 696 790 ≤ b_3 ≤ 31 723 013 | C / E | L11b-91, L11b-42 |
| b_3 au rang 35 | ≤ 159 686 | E | L11b-04 |
| b_4 (norme 8 de M), minorations | 3 826 746 − 30P − 4572ρ (sûre) → 2 729 034 → 3 151 962 → 3 371 634 (distincts) ; 5 939 010 + 66P + 14H − 13572ρ − 480τ − 98Ω ; 5 764 374 si P = 0 | C | L11b-09, L11b-12, L11b-19, L11b-20, L11b-16 |
| b_4, plafonds au rang 37 | 16,839 M → 16,499 M → 16 469 236 → 16 014 184 → 15 979 948 → 15 975 391 → 15 972 863 → 15 196 716 (ρ = 126, b_3 ≥ 45 964) ; via Fano 15 197 980 (ρ = 126), 15 221 160 (ρ = 125) | C | L11b-15 … L11b-87 |
| b_4 + (651/34)b_3 au rang 37 | ≤ 17 398 653 → 17 153 604 → 16 978 453 → 16 851 675 ; ≤ 15 457 549 + (450359/272)a_7 ; 272b_4 + 5208b_3 + 5 854 667ρ ≤ 5 111 025 995 | C | L11b-28, L11b-39, L11b-53, L11b-72 |
| b_4 au rang 35 | ≤ 4 011 586 | E | L11b-04 |
| b_5 | ≥ 35 123 088 − 168P − 7212ρ ; uniforme 33 224 268 → 33 955 848 → 34 087 368 | C | L11b-07, L11b-13, L11b-19, L11b-20 |
| P (prismes) | ≤ 852 ; P + 5ρ ≤ 1386 ; P ≥ 6ρ ; au rang 35 ≥ 450 (sans objet) | C | L11b-19, L11b-66, L11b-09 |
| ρ (grilles) | ≤ 142 → ≤ 126 | C | L11b-19, L11b-20 |
| τ (paires de prismes jumeaux) | ≤ 5P/2 ; ≤ 2130 ; ≤ 2P + 3ρ ; ≤ 1890 ; 8τ ≤ N4 ; 17τ ≤ 17P + 105ρ ; ≤ 1534 ; ≤ 1403 ; τ_g ≤ 11ρ + 17, τ ≤ P + 5ρ + 17 ; ≤ 1354 (r ≥ 37) ; ≤ 1326 (r = 43) ; ≤ 2048 et ≤ 4615 (plus faibles) | C | L11b-09 … L11b-91 |
| N4 = paires (prisme, triangle lointain), signées | ≤ 17 325 ; Φ ≤ 8483,3 (flottant) | C / H | L11b-26, L11b-46 |
| taille d'une classe de jumeaux | ≤ 6 ; hors grille ≤ 3 ; grille : g(Θ) ∈ {0,1,2,3,4,6} | C / P | L11b-09, L11b-58 |
| triangles lointains d'un prisme | F ≤ 12 (≤ 10 dans une grille) ; F ≥ 2(m − 1) | P | L11b-43 |
| H (graphe D à 7 sommets) | 3P + 2H ≤ 4158 ; H ≤ 1867,25 (flottant) | C / H | L11b-15, L11b-35 |
| Ω (paires de D jumeaux) | ≤ H | P | L11b-15 |
| e(Ξ_v) = g(v) (grilles par un sommet) | ≤ 17 ; ≤ 15 au rang 43 | P / C | L11b-58, L11b-91 |
| n_3 (sommets sur 3 droites dans six grilles) | 3n_3 ≤ 2n_1 + n_2, n_3 ≤ 39 (r ≥ 37) ; 6n_3 ≤ n_1 + 2n_2, n_3 ≤ 24 (r ≥ 39) | C | L11b-85, L11b-90 |
| \|{v : g(v) = 17}\| | ≤ 50 | P (pont seulement) | L11b-64 |
| s = \|{v : g(v) ≥ 14}\| | ≤ 73 | C | L11b-66 |
| rang mod 7 des vecteurs du noyau | ≤ 56 − r (19, 17, 15, 13 aux rangs 37-43) | P | L11b-81 |
| rang local des composantes en un sommet | ≤ 14 (espace hyperbolique) ; vraies classes h = n − b(F_v) − 7 | P | L11b-95 |
| b(F_v) dans « (6,6) partout » | ≤ 1 ; relations locales ≤ 99 | P | L11b-96 |
| c4(uv) (arête entre couches, P = 0) | ≤ 2 ; 38 types à S = 0 | P | L11b-97 |
| dimension de l'espace de Green des 60 ombres | 33 | P | L11b-97 |
| collisions de masse six par paire de grilles (binaire, même somme, supports ≤ 9) | 16 496 ≤ C6 ≤ 27 828 (27 798 à m = 6) ; hors grille ≤ 31 976 ; total C6 ≤ 38 084 490 | C | L11b-62, L11b-68, L11b-70, L11b-87 |
| (6,3) interne, e(W) ≤ 8 | norme 6 : 756τ, 108Ω ; norme 8 : 12 814τ (12 182 grille), 3612Ω | C | L11b-37, L11b-62 |
| (4,4) | L44 = 997920 + 2794τ + … ; masse 6 pure 2634 + 4t par paire | C | L11b-26, L11b-62 |
| F0, Ftf | F0 ≤ 10 380τ + 1528Ω ; Ftf ≤ 642τ + 710Ω | C | L11b-55 |
| canal (9,0) par paire de grilles | C90 = 5376 + 12t_Z ≤ 5472 | C | L11b-69 |
| sans prisme (pf) | 6992 ≤ C_pf(grille) ≤ 18 244 ; 7034 ≤ C_pf(hors grille) ≤ 19 178 ; égalités ≤ 12 674 / 14 426 | C | L11b-76 |
| représentants bruts (pas des vecteurs distincts) | (6,3) N8 ≥ 10 336 557 ; F8 (4,4) ≥ 2 723 490 ; (5,5) N8 ≥ 2 896 844 ; (5,2) = 2 112 264 − 24P + 14H ; (7,1) Q8 = 4 108 104 + 468P − 512H + 72C14 − 12(C13a + C13b + C13c) ; Ftf ≥ 166 320 | C | L11b-15 … L11b-55 |
| r8 + (651/34)r6 (aucune collision retirée) | ≥ 39,7 M (supports ≤ 9), 66,6 M (≤ 10) ; partie propre 18,43 M | H | L11b-34, L11b-35 |
| recensement | ordres 2..10 : 2, 4, 9, 21, 62, 208, 916, 5311, 42 430 types ; 549 paramètres ; 492 types d'ordre 10 de degré minimum 3 | E / C | L11b-33, L11b-32 |
| couches duales au côté 3 | ~10^12 à 10^16 (pas de majorant utile) | E | L11b-27, L11b-38 |

### 9.3 Lemmes ouverts et étapes manquantes, avec ce qu'ils donneraient

- **(a') uniforme** : obstruction des étoiles génériques au rang 37. Avec NT et la note 126 §3 ter, elle réduit tout au cas (6,6) à P = S = 0 (L11b-92, L11b-96).
- **NT** : pas de torsion équilibrée sur les droites connexes. Même rôle (L11b-92, L11b-96).
- **Exclusion de « (6,6) partout »**. Clôturerait la chaîne de septembre (L11b-96).
- **Borne inférieure du rang mod 7** d'un système de grilles et de différences jumelles en fonction de τ (« ρ ≤ N », N ≲ 50). Ferait passer la comptabilité sous le budget (L11b-86, L11b-87).
- **g(l) ≤ 3**. Donnerait τ_g ≤ 693, limite (L11b-60, L11b-78).
- **κ_18 ≤ 2 et κ_20 ≤ 1**. Rendraient la route des graines active (L11b-65).
- **Majorant de b_2 au rang 37, ou de a_13 (norme 26)**. Couperait le plafond d'un facteur comparable à 1,8 sur τ (L11b-63, L11b-67).
- **Constantes de collision des supports 10, (5,5) et (8,2)**. Budget ~59 300 par paire jumelle à R = 65,57 M (L11b-71).
- **Fermeture en cube** : un triangle de Ξ_v impose-t-il l'union H(3,3) ? Combinée au lemme H(3,3), elle donnerait Ξ_v sans triangle, donc τ_grille ≤ 945 (L11b-58, L11b-59).
- **Les 12 survivants de la note 112** et l'exclusion des classes de Ξ-degré 4 ou 6 (L11b-61, L11b-79).
- **Existence d'une 22-coclique**. Son absence donnerait a_7 = 0 (L11b-50).

### 9.4 Méthodes transférables (des analogies, pas des transpositions)

- **Recensement par identités d'extension et récurrence triangulaire** (L11b-21, L11b-32, L11b-33).
  - Valable pour tout srg(v,k,1,2) et déjà validé sur srg(243,22,1,2) et sur la tour.
  - Analogue pour le banc d'essai srg(243) de la campagne d'asymétrie (L07).
  - Différences : constantes et coefficients dépendent de (v,k) ; dans les deux srg(243) connus, H et plusieurs invariants d'ordres 8 et 9 sont nuls, donc leurs coefficients n'y sont pas testés.
- **Inégalité de classes et principe du plus court représentant** (L11b-30, L11b-57, L11b-75).
  - Classes ≥ 2R/(k+1) − 2C/(k(k+1)) ; poids 1/(nombre de plus courts).
  - Outil général de comptage de classes latérales.
  - Transférable à tout comptage d'orbites ou de classes avec paires de collisions : gabarits de la route c (L08), complétions de cadre du principe de symétrie forcée (L07).
  - Différence : il faut un plafond de TOUTES les paires, ce que fournissent rarement les recherches par solveur.
- **Borne de rang mod p sur les vecteurs du noyau, test de genre** (L11b-81, L11b-90).
  - Analogue du théorème A de C2 (parité de rank_F7, corrigé : L05-214) et de la formule d'oddité de C2 (L02_C2_aws-360).
  - Remarque de la fiche, non tirée des sources : pour srg(243,22,1,2), les valeurs propres sont 4 et −5 (x² + x − 20 = 0, écart 9), donc le premier pertinent est 3, pas 7. Le rang mod 3 de A − 4I jouerait le rôle de r, et la borne « 56 − r » serait à recalculer.
- **Inutilité des méthodes locales démontrée a priori** (L11b-95).
  - Un espace local hyperbolique se plonge dans l'ambiant.
  - Analogue de la limite des méthodes de rang local à une arête en C2 (L03a-74 : « ne peuvent dépasser 39 ») : un critère « no-go » à appliquer avant de lancer des balayages locaux.
- **Certificats rationnels exacts avec vérificateur autonome** (--verify-only, sans solveur ni module tiers) pour les PL de bornes.
  - Même discipline que la route C de C2.
  - Remède direct au bug OR-Tools du 18/10 (L05-179) : un certificat exact exporté ne dépend pas du solveur.
- **PL de moments de voisinage dans un SRG** (Σd = 14s ; Σd² + Σ_S d = 12s + 2s² ; Σ_S d ≤ 3s + s²/9) (L11b-64, L11b-66).
  - S'applique à tout sous-ensemble S d'un srg.
  - Transférable aux sommets à forte densité de grilles du rang 37, aux droites c ≤ 3 de la route c, et à srg(243) avec ses paramètres.
- **Lemme (4 + 3) et formule du rang par le laplacien sans signe du complément de Ξ_v** (L11b-91).
  - Transférable à srg(243,22,1,2), qui a 11 droites par sommet et un module différent.
  - Différence : la constante 4I + 2CᵀC − 3J et la condition « pas de sommet de degré 1 » changent.
- **Empilement des graines** : deux graines qui partagent 3 voisins forcent un grand produit scalaire, d'où une petite différence (L11b-10).
  - Même schéma que « deux vecteurs ne diffèrent jamais d'un vecteur court » en C2/C3.
  - Ne se transpose pas tel quel aux normes 16/18 (L11b-14, L11b-36).
- **Couplage de deux étoiles par une arête** : appariement et 38 types (L11b-97).
  - Analogue des registres d'étoiles P = 0 de C2 (L05-209).
  - Différence : en C1 les étoiles sont attachées à une droite générique du rang 37, et non à une involution.

### 9.5 Combinaisons candidates (à soumettre à une vérification adverse)

1. **|{v : g(v) = 17}| ≤ 50 (L11b-64, rigoureux, seulement dans le pont) × PL de moments de la note 204 (L11b-87, τ ≤ 1354).**
   - Cette contrainte n'a jamais été injectée.
   - Codex note qu'elle ne suffit pas seule (les sommets à g = 16), mais son effet sur le maximum de τ n'a pas été calculé.
2. **Congruence mod 7 coclique-prisme (L11b-52) × P ≤ 852, ρ ≤ 126, structure des grilles × a_7 ≤ 9h (L11b-54).**
   - Une 22-coclique coupe chaque grille en 2 points et chaque prisme selon une congruence mod 7.
   - Restriction possible sur h, donc sur a_7, donc sur le plafond (K7). Jamais testé.
3. **Lemme H(3,3) (L11b-59) × « Ξ_v sans triangle ⇒ τ_grille ≤ 945 » (L11b-58).**
   - Il manque la fermeture en cube (§9.3).
   - Si elle est prouvée, τ_grille ≤ 945 au lieu de 1354.
4. **Majorant de a_13 (K16) × C6 ≤ 38 084 490 (L11b-87).**
   - À plafond 11,0 M, le C_total forcé (42,6 M, calculé avec l'ancienne collection R = 36,59 M) dépasse le cap C6.
   - Mais C_total contient d'autres canaux (correction de Codex, pont:#275). À recalculer sur la collection de Codex (R = 32,43 M) avant toute conclusion.
5. **K1 (rang 43 par entrées monotones ⇒ tous les rangs) × résultats du rang 43 (L11b-42, L11b-49, L11b-91).**
   - Vérifier si les exclusions partielles du rang 43 n'utilisent que des entrées monotones au sens de LAP.
   - Celles de la note 206 utilisent la borne de rang 13 (propre au rang) : a priori non monotones.
6. **P ≤ 852 (L11b-19, C) × conditionnels ultérieurs hors lot.**
   - L05-150 : P ≤ 852 ⇒ ≥ 18 droites t ≤ 7 et ≥ 254 blocs hors grille.
   - L07_C1_asym_local-264 : N9-NG/NG5 ⇒ P ≥ 924 > 852.
   - L'exclusion ne dépend que de NG5 ; le maillon P ≤ 852 vient d'ici, avec un statut contesté (§8.2.4).
7. **Plafond Fano-grilles 272b_4 + 5208b_3 + 5 854 667ρ ≤ 5 111 025 995 (L11b-72) × une minoration de b_4 qui croîtrait avec ρ.**
   - Aucune n'est connue : les minorations certifiées décroissent en ρ, et les copies d'une seule grille gonflent les représentants, pas les classes (L11b-69).



<!-- ===== L11c_pont.md:438-635 ===== -->

## 12. Matériaux pour la recombinaison

### 12.1 Conditionnels « si X, alors exclusion »

| # | Si X… | … alors | Statut de X | Source |
|---|---|---|---|---|
| K1 | aucun des 174 noyaux de Makhnev ne se prolonge en srg(99,14,1,2) | C1 exclu, tous rangs, sans généricité, sans P = 0, sans involution | O (couverture : C) | L11c-045, L05-098 ; pont:#407, #410 |
| K2 | chaque droite est dans ≥ 5 grilles | contradiction (0 type) ; pour q = 1, 2, 3, 4 il reste 115, 52, 11, 2 types | conditionnel prouvé (C) ; X non établi | L11c-055 ; pont:#423, #424 |
| K3 | (rang 37, droite connexe sans torsion) toute sélection binaire de 60 ombres compatibles de moments K a e(F) ≥ 247 | aucune telle droite ; déjà vrai par L23 si τ est un carré non nul | O pour τ ≡ 3, 5, 6 mod 7 | L11c-079, L11c-081 ; pont:#444, #446 |
| K4 | (rang 37) toute droite a G(T) connexe | aucune grille au rang 37 | O (maille ≥ 5 ⇒ connexe : E ; énoncé B incomplet) | L11c-054 ; pont:#422 |
| K5 | (rang 37) tout profil à composante prisme autre que (1^6) est exclu | g ∈ {0, 6} sur toute droite ; g = 6 force ρ = 231 > 126 ; donc aucune grille | implication P ; X ouvert (masse 1,4e8 boules) | L11c-134 ; pont:#517, #518 |
| K6 | (rang 37, P = 0, sous-collection z) nombre total de paires en collision des masses 7, 8, 9 < 3,84 M | rang 37 exclu à P = 0, donc « rang 37 ⇒ P > 0 » | H (LP flottant) ; certifié : 185,2 M (34,6 fois trop) | L11c-061, L11c-069 |
| K7 | (rang 37, collection x63, k = 2) 27 828 τ_g + 31 976 τ_n + (hors C6) < 17,1 M ; à ρ = 0, coût d'une paire jumelle hors grille < 25 201 | rang 37 exclu | H | L06-049, L11c-042, L11c-134 |
| K8 | (rang 43, S0) borne < 4979 sur les vecteurs de classe 2, norme 40/9, non arêtes | S0 exclu, puis toute la branche « sans 16..24 » (avec L11c-115) | O | L11c-117 ; pont:#491 |
| K9 | (S0) borne uniforme ≤ 2288 sur les configurations P7 indépendant / Q29 | S0 exclu | O | L11c-119 ; pont:#495 |
| K10 | (S0 sans fantôme) borne < 2001 sur les configurations (P7, N29) | S0 sans fantôme exclu | O | L11c-118 ; pont:#493 |
| K11 | (S0) la configuration P3/N25 est exclue (n ≥ 11 forcé) | S0 exclu | O : 3271 supports ouverts | L11c-120, L11c-124, L11c-126, L11c-144 |
| K12 | (rang 43, sans 16..24) une relation force l'isotropie du second moment de la couche 26 | contradiction (169N/11) | O ; non forcée au degré 2 | L11c-111, L11c-112, L11c-114 |
| K13 | les sommes cubiques par classe s'annulent | la branche meurt mod 49 | O ; non forcées | L11c-114 |
| K14 | (rang 43) 10a₈ + 2a₉ + 5a₁₀ + 2a₁₁ + a₁₂ < 328 | aucune racine | P | L11c-115 |
| K15 | (rang 43) aucun objet bas (κ, g_v, u, g_l, c₁, w, s₄₄) | aucun vecteur de norme 14 ou 16, au plus une paire de norme 18 ou 20 ; S0 en possède toujours un | E | L11c-126 |
| K16 | (rang 37 ou 39 générique, bloc proche inversible) les données (boule, 60 ombres) ont un automorphisme non trivial | Γ a un automorphisme ; à croiser avec les exclusions des ordres 2, 3, 7, 11 (combinaison α, L02-458) | P (rigidité) | L11c-088 à L11c-090 |
| K17 | (rang 37 générique) « la symétrie de (boule, ombres) est forcée » ou « ces données n'existent pas » | droites génériques exclues | O | L11c-093 |
| K18 | (rang 37, z = 0) les motifs A et B sont interdits au niveau d'une étoile complète | aucune étoile générique à z = 0 | O | L11c-033, L11c-037 |
| K19 | (rang 37) minoration de j, l'indice de saturation | le filtre de Hermite τ ≥ ⌈51 883 209 j²/4⌉ retire des boules ; il faut j ≳ 230 à 440 pour les τ observés (6,9e11 à 2,5e12) | O | L11c-132 (seuil en j : calcul de l'agent) |
| K20 | le triangle des centres alternés est exclu | toute réparation d'un ruban six injectif contient deux cordes disjointes | O | L11c-104 |
| K21 | (rang 37) les mondes des normes 16, 18 et 20 meurent | rang 37 exclu : il force une norme 14, 16, 18 ou 20, et la norme 14 est exclue le 10/10 (L06-092) | O | L11c-142, L11c-145, L06-091 |
| K22 | (P = 0) aucun vecteur φ = (2, 1^16) du noyau | le canal moulin-cubique de C8 disparaît | O (359 types) | L11c-068 |
| K23 | un sommet extérieur a ≥ 3 voisins dans un cubique U | U n'a aucun partenaire moulin | P | L11c-071 |
| K24 | (sans grille) un prisme a au plus un jumeau | τ ≤ P/2 (le « 20,2 M » de LAB, calculé sur une mauvaise collection, est retiré) | O | L11c-134, L11c-135 |

### 12.2 Bornes quantitatives (objet, inégalité, statut, source)

- **Composantes (6,6).** 288 composantes étiquetées, 15 types. Candidats 630 → 612. Un design de 60 triplets existe pour chacune (S). L11c-002, L11c-007.
- **Relations.** h_T de rang rationnel ≤ 54, donc ≥ 177 relations entières de témoin 0. Noyau des classes ≥ 213 contre 99 relations incidentes (P). L11c-004.
- **Patrons à deux étoiles.** 38 / 19 / 5 selon c₄ = 0, 1, 2 ; rangs 15 à 19 (E). L11c-006.
- **Branches d'apex.**
  - Effectifs : 473 (cyclique), 368 (boule 5), 464 (boule 9), 416 (boule 12). Total 1721 branches, 38 518 feuilles (C). L11c-023.
  - Marges : 4067 (branche 0) ; 3556, 7410, 6010, 8133 (boule 12) ; potentiels, marge 7 (−405 > −412) (C). L11c-010 à L11c-012.
- **Heuristique de rareté (H, critiquée).**
  - Étoiles attendues par boule : 8,6e-16 et 2,2e-15 ; ~4e-3 sur toutes les boules.
  - Sous-étoile de m ombres : 340^m 7^(−C(m,2)).
  - Masse d'orbites (11!!)³/6 = 1,9e11 ; ~2,6e10 boules sans triangle, génériques, τ non carré ; ~16 années-cœur à 20 ms.
  - L11c-014, L11c-035.
- **Profil des sommes d'étoile.** K = 1 sur 8 − 2z points, K = 2 sur 16 + z, K = 0 sur z ; a(w_i) ≤ 3 (P). L11c-031, L11c-033.
- **Triplets d'apex** (boule 12, centre 0 ; E). L11c-034.
  - Pool 3372 ; paires d'apex 24 058 (10 814 avec le filtre réel).
  - Triplets : 344 057 avec d ≥ 2 et 333 489 avec d ≤ 1 ; avec le filtre réel, 77 880 et 91 175.
- **Barrière.** Gram C10 de déterminant 2 ; ambiant de dimension 28, complément de dimension 6 (P). L11c-036.
- **Noyaux de Makhnev.** L11c-043, L11c-045, L11c-048, L11c-050.
  - 33 sommets vides ; simples 9, 9, 8, 9, 9, 8 ; 8 doubles.
  - 21 arêtes optionnelles ; 2299 graphes étiquetés ; 373 → 310 → 174 (C) ; masques ≤ 1792.
  - e(D(S)) ≤ 4 ; e(C(S)) ∈ [61, 65] ; x₅₈ = x₅₉ = 0 (E).
- **Paires de triangles disjoints (99).** N₀ + N₁ + N₂ + N₃ = 24 486 ; Σ j N_j = 24 948 ; N₂ = 4158 − 3N₃ ; N₁ = 16 632 + 3N₃ ; N₀ = 3696 − N₃ (P). L11c-048.
- **Double comptage.** T ∈ [0 ; 18 649] ; N₂ ∈ [1599 ; 4158] ; T − 4N₂ ∈ [−16 632 ; 2017] (H, flottant). L11c-049.
- **Grilles par droite.** Selon q = 1, 2, 3, 4, ≥ 5 : il reste 115, 52, 11, 2, 0 types (C). L11c-055.
- **Comptage au rang 37 (H, flottant).** L11c-042, L11c-056, L11c-061, L11c-134.
  - R = 32,5 M ; plafond 15,8 M ; seuils 16,75 M / 17,7 M.
  - Seuils par paire jumelle : 87 431 (P ≤ 100), 45 402 (P ≤ 200), 30 697 (P ≤ 300).
  - Sous-collection z : R = 19,48 M, budget 3,84 M, seuil 8244 à P ≤ 200.
  - Coût d'une paire jumelle hors grille : 25 201 nécessaire contre 31 976 certifié.
- **Formes de collision (P ; maxima H).**
  - C7 ≤ 5402 Ω ; C8 avec 2592 × 3465 = 8,98 M, puis sans constante ; C9 : 39 types.
  - Maxima : 193,5 M (ordre 9), 149,2 M (ordre 10), 151,1 M (après le lemme e = 14).
  - Total couplé 185,2 M, facteur 34,6.
  - L11c-062, L11c-063, L11c-065, L11c-067, L11c-069.
- **Classes de même projection (P).**
  - Taille ≤ 4 (Codex), ≤ 3 sans moulin (LAB), au plus un moulin.
  - e = 14 : classes disjointes, taille ≤ 3.
  - |Z(U)| ≤ 23, |Z(W)| = 24 ; profil (23, 48, 20) ; e(Z(U)) ≤ 34.
  - d + t ≤ 9, d − t ≤ 7 ; d ≤ 7 pour Z(cubique), d ≤ 6 pour Z(moulin).
  - L11c-065, L11c-066, L11c-070 à L11c-072.
- **Moulin-cubique.** 3507 deux-facteurs, 8040 H locaux, 2845 sans prisme, 359 types (29 / 122 / 208) (E). L11c-068.
- **Cubique induit à s sommets.** Σ degrés extérieurs = 11s, Σ carrés = 2s², s ≤ 38 (P). L11c-078.
- **Balayages de LAP (E, non audités).** L11c-073, L11c-074.
  - (4,4,4) : 275 / 275.
  - (4,8) : 97 896 représentants : 81 380 morts, 16 516 à torsion (15 462 / 964 / 71 / 19).
  - Rangs de torsion de 81 959 types : 68 372 / 12 811 / 719 / 48 / 9.
- **L23, échantillon de 200 graphes.** 24 avec τ ≡ 0, 97 résidus, 79 non-résidus (E) ; det(3J − H) = −3888 τ (P). L11c-080.
- **Seuil 240.** e(F) = 240 + 7q ; degrés 8 + 7a_f (P). L11c-079.
- **Quadrangles (P).** 2079 quadrangles ; ≥ 1715 relations entre 2310 parités ; 44 voisins extérieurs ; |E(S)| = 100 + t ; Δ(Q) carré parfait divisible par 7^(45−r) ≥ 49. L11c-086, L11c-091.
- **Rigidité.** rang₇(D) ≤ r + r′ − 74 ; r + r′ ≥ 78 (P, LAP) ; rang(D) ≥ 5 ; 729 Grams, 7 classes (C) ; mouvement par bloc ≥ 9 sommets (13 pour 243) ; bascule 243 : D³ = 45D, ≤ 96 des 240 arêtes. L11c-088 à L11c-090.
- **Rubans (C/P).** L11c-097 à L11c-105.
  - Ruban propre fermé : m ∈ {3, 4, 5} ; segment ouvert ≤ 4 centres.
  - Réparations entre centres seulement : m ≤ 8 (m ≤ 15 par Cauchy) ; E(C) ≥ ⌈m/4⌉.
  - Masques des formes en étoile : 119, 119, 111, 118, 118, 107 ; paires disjointes : 126, 87, 358, 106 couples ; second niveau : 279 masques restants.
- **Convergences.** det R6 = 3255 = 3·5·7·31 ; D(H + z) = 12 − t(t + 5)/2, t ≤ 3 ; deux supports de même vecteur partagent ≤ 3 points ; 95 = 19 + 38 + 38 étoiles (P/C). L11c-094, L11c-098.
- **Réseau des droites (P).** [M : Λ_L] = 3^(e₃−1) ; e₃ ≤ 22, e₂ ≤ 27, e₅ ≤ 27 ; ≥ 33 droites monochromes. L11c-099.
- **Thêta (E).** Z/9 : 71 paramètres, 18 libres ; cubique : 64 dimensions, 19 libres ; au plus 93 696 22-cocliques au rang 37. L11c-106, L11c-108.
- **Rang 43, classes et racines (P/E).** L11c-108, L11c-110, L11c-111, L11c-113 à L11c-116.
  - Normes 18 et 26 seules : x₁ + x₂ ≤ (329 + 7b₁)/8 ; t = 329 + 14k − 8(x₁ + x₂) impair, minima 1, 7, 5, 3 ; a₁₃ ≥ 8, 56, 40, 24 ; x₁ + x₂ ≤ 41 + ⌊7k/4⌋.
  - k ≤ 2 ; N ∈ {329, 343, 357}.
  - T_L26 + 14 T_M4 = 2828 I ; T_extra ≤ 160 I ; valeurs propres de T ∈ [−48,9 ; 111,1].
  - Une racine impose 10a₈ + 2a₉ + 5a₁₀ + 2a₁₁ + a₁₂ ≥ 328 ; si seule la norme 18 est présente, a₉ ≥ 164.
  - Contacts d ≤ 48 (≤ 45) ; e_tri ≥ 6 ou ≥ 22 ; Σ_T x(T)² = 78.
- **S0 (E/P).** L11c-117 à L11c-120, L11c-124, L11c-126.
  - Plages par classe et par norme (L11c-117, L11c-120) ; classe 2, norme 40/9 : 5672 à 6396.
  - ≥ 4979 non-arêtes ; ≥ 4361 du type (1⁷ ; (−1)²⁹) ; ≥ 2289 + 15g configurations P7 indépendantes ; ≥ 2001 sans fantôme.
  - Fantômes : g ≤ 22 ; 15g₀ + 13g₁ ≤ 330 ; N₁ + N₃ ≤ 288.
  - e(X) = e(Y) ≤ 5 pour tout vecteur binaire de norme 28 (tout srg).
  - n = 10 + u + s₄₄ + 2w + 4c₁ + g_l + 7g_v ≥ 11 ; δ ≤ 9.
- **Supports P3/N25.** 6899 → 5345 → 4581 → 3640 → 3343 → 3271 ; 3 ≤ δ ≤ 9 ; 1 ≤ t_p ≤ 3 ; 59 des 252 premiers infaisables au LP (C/P/S). L11c-122, L11c-125, L11c-128, L11c-137, L11c-144.
- **Réseaux lointains (P).** L11c-130, L11c-132.
  - det Λ₋(T) = 4·7^(2k)τ/(9j²) ; det Λ₃(T) = 5·7^(2k)Θ/(256j′²).
  - Hermite : norme ≤ ~30, 38, 48, 60 aux rangs 37 à 43 ; τ ≥ ⌈51 883 209 j²/4⌉.
  - τ échantillonnés : 3,9e11 à 2,5e12 (E).
- **Coût du test d'étoile (E).** 60 → 2,2 → 1,26 ms ; 145 jours-cœur, 1,3 puis 2,7 années-cœur ; 78,8 % de la masse ; 10 000 boules sans étoile ; saturation : nœuds de 52 767 à 41 106. L11c-121, L11c-131, L11c-139.
- **Conflits minimaux.** Environ 94 par boule, de taille 6 ou 7, jamais ≤ 5 (E). L11c-141.
- **Norme 14 (E).** Bases de 39 sommets : 111/120 de rang 36 ; 800 427 bases exactement. L11c-145.
- **Norme 16 (P/E).** 5e(D) + W = 9, e(D) ≤ 1, e(Z) ∈ {5, 6} ; 15 → 14 formes, 75 → 70 supports ; cadre de rang ≤ 35 ; 1696 types d'incidences D-Z ; 478 attaches → 86 graphes. L11c-143, L11c-146.
- **Apices indépendants.** C14 + 2τ ≤ 2P (P) ; plafond C6 = 31 976, inchangé (C). L11c-135.

### 12.3 Lemmes ouverts ou étapes manquantes, et ce qu'ils donneraient

1. Obstruction uniforme (a′) : interdire A et B. Donnerait : plus de droite générique sans triangle au rang 37, et avec NT un monde P = S = 0 vide (L06-088). Sources : L11c-033, L11c-037.
2. e(F) ≥ 247 pour τ ≡ 3, 5, 6. Donnerait : plus de droite connexe sans torsion au rang 37 (L11c-079).
3. Une borne sur les PAIRES de supports de même projection, aux masses 7 à 9. Donnerait : « rang 37 ⇒ P > 0 » (L11c-069).
4. Coût d'une paire jumelle hors grille < 25 201, ou « au plus un jumeau ». Donnerait : rang 37 exclu sans grille, avec K4 et K5 (L11c-042, L11c-135).
5. Prolongement des 174 noyaux, ou une coupe structurelle (Benders, parabole). Donnerait : C1 (K1).
6. Énoncé B complet et droites connexes. Donnerait : « rang 37 et P = 0 ⇒ toute droite connexe », puis K4 (L11c-073, L11c-077).
7. S0 : bornes de K8 à K11, ou le design entier de l'étage 1. Donnerait : la branche « sans 16..24 » du rang 43 (L11c-117 à L11c-128, L11c-144).
8. Isotropie de degré 2, ou annulation des sommes cubiques. Donnerait : la même branche (K12, K13).
9. Rigidité pour (39,41), (39,43), (41,41) et les droites non génériques ; existence des données (G, N). Donnerait : la symétrie forcée étendue (L11c-089, L11c-090).
10. Une minoration de j. Donnerait : un filtre de Hermite effectif (K19).
11. Les mondes des normes 16, 18 et 20 au rang 37 ; un catalogue des cœurs de normes 18 et 20. Donnerait : le rang 37 (K21).
12. Les structures à quatre murs d'un quadrangle ; le cas Δ(Q) = 0. Donnerait : une reconstruction sans rang à partir d'un objet présent 2079 fois (L11c-091, L11c-092).
13. Le triangle des centres alternés ; une borne supérieure sur E(C). Donnerait : la piste des rubans (L11c-101, L11c-104).
14. Moulin-cubique : arêtes entre cellules, reste R16. Donnerait : la disparition du canal moulin-cubique de C8 (L11c-068, L11c-071).
15. « Lemme qui divise le nombre de boules par 1e3 » (demande de LAP). Donnerait : un balayage exhaustif réaliste du rang 37 (L11c-093).

### 12.4 Méthodes transférables (analogies, avec les différences)

- **Réfutation de profondeur un (« une ombre fixée puis propagation »)** (L11c-023).
  - Vers : cellules des mondes de normes 14 et 16, design P3/N25, complétions de noyaux.
  - Différence : les domaines à deux étoiles sont des ombres à produits de Green mod 7 et sommes exactes ; dans P3/N25, ce sont des blocs à équations de couverture de paires.
- **Lecture des certificats de Farkas par potentiels** (L11c-012).
  - Vers : tout LP à marginales de paires (niveau 2 des noyaux, masques de rubans, bords de Convergences).
  - Exige des tables de compatibilité par paires ; les noyaux n'ont qu'un statut adjacent ou non adjacent.
- **Ablation exacte avec témoins rationnels** (L11c-017).
  - Pour calibrer quelles contraintes portent vraiment ; applicable au LP de l'étage 1 de S0 et au LP des noyaux.
- **Identité réelle du projecteur lointain et mineurs PSD 3×3 avec un sommet isolé connu** (L11c-015, L11c-020).
  - Valable à tout rang ; vers les rangs 39 à 43, le quadrangle (G_S) et les cadres de normes 14 et 16.
  - Différence : seul le rang 37 rend Π 7-intégral ; ailleurs il reste un résidu de dimension 2k.
- **Tests de déterminant et de classe de carré** (L11c-025, L11c-091, L11c-130).
  - Exemples : τ det Σ_X carré rationnel, Δ(Q) carré divisible par 49, det Λ₋(T).
  - Analogue des contrôles de déterminant et de discriminant de la route C de C2 ; mais C2 disposait d'une classification globale finie (156 réseaux), ici seulement de conditions locales nécessaires.
- **Motif forcé et théorème de couverture** (Makhnev, L11c-043).
  - Analogue de l'« objet obligatoire » de C2.
  - Différence : 14 sommets sur 99 et complétions non contrôlées, contre 156 objets décidés un par un en C2.
- **LP de multiplicités de masques à certificats entiers (« niveau un sommet »)** (L11c-045).
  - Réutilisable sur tout support : déjà appliqué aux rubans, à Convergences et aux réunions de noyaux.
  - Contrôle positif disponible sur twin243.
- **Relèvement de Benders d'une contradiction de réalisation en coupe linéaire sur le maître** (L11c-098).
  - Vers : complétions des 174 noyaux, design P3/N25.
- **Lemme A (parabole entière, tout ensemble S) et sa version « filtre de colonnes »** (L11c-137, L11c-138).
  - Universel et bon marché ; vers toute énumération de configurations induites (boules, étoiles, noyaux, cadres, rubans).
  - Déjà suggéré par la combinaison ε de L02-462.
- **Budgets de voisins communs**.
  - Exemples : 5e(D) + W = 9, lemme 14, 3t_p ≤ …, lemme de la forêt, connexité des murs.
  - Sans rang ; vers les cœurs de normes 18 et 20, les noyaux de Makhnev, les murs des quadrangles.
- **Lemme du laplacien et différence de rang ≤ 4** (L11c-089, L11c-090).
  - Vers toute paire de candidats ayant les mêmes lignes sur S et des profils extérieurs distincts (automatique si chaque sommet modifié a ≥ 3 voisins non modifiés).
  - Exige un bloc principal inversible portant tout le rang de Q mod 7.
  - Analogie avec les bascules de srg(243) (D³ = 45D).
- **Barrières de Witt** (L11c-036, L11c-140).
  - Méthode négative : elle dit d'avance qu'un filtre de Gram sur F₇ ne peut pas conclure. À appliquer avant tout nouveau filtre de ce type (classes de S0, cadres de norme 16).
- **Équilibre réel |C| = 6|N(f) ∩ C|** et regroupement (L11c-055) : vers toute analyse par composantes des droites (profils de LAP).
- **Entrelacement sur les anti-voisinages** : partenaire si et seulement si det(3I − A_{Z(U)}) = 0 (L11c-072). Vers tout support de vecteur propre entier.
- **Formes modulaires de degré 2 et séries thêta par classes** (L11c-112 à L11c-114).
  - Recollement propre au rang 43 ; transfert aux rangs 37 à 41 proposé par la combinaison γ (L02-460).
  - Différence : plus de paramètres libres aux rangs inférieurs, et aucune simplification de type S0.
- **Descentes y ∓ 7Ee_v et minima de classes forçant les profils (fantômes)** (L11c-117 à L11c-120) : vers d'autres classes et d'autres rangs dont les minima de classes sont connus.
- **Produits cartésiens comme générateurs de contre-exemples** dans la famille λ = 1, μ = 2 (L11c-087) : contrôle de cohérence analogue aux étalonnages sur srg(243).
- **Positivité de 3I − A_H + J/9 sur des supports structurés, certificats de Bernstein** (L11c-097, L11c-100).
  - Transférable à srg(243) en ajustant la valeur propre (−5) et le terme J.
- **Forme de Seidel sans droite** : tout ensemble de rang de Seidel 36 est une base (L11c-142).
  - Permet de choisir une base rigide (monde biplan de norme 14 : 800 427 bases, contre 1,5e11 boules ; quadrangle et ses 44 voisins).

### 12.5 Combinaisons candidates (à soumettre à la vérification adverse ; non vérifiées)

1. **Rang 43 : identité de budget × inégalité des racines.**
   - L11c-126 (pont:#507) : 17a₇ + 10a₈ + 4a₉ + 4a₁₀ + 2a₁₁ + a₁₂ + f₁₁ ≤ 10 + B, avec B = 7g_v + u + g_l + 4c₁ + 2w + s₄₄ ; a_j entiers.
   - L11c-115 (pont:#489) : 10a₈ + 2a₉ + 5a₁₀ + 2a₁₁ + a₁₂ ≥ 328 dès qu'une racine existe.
   - Conséquence : une racine au rang 43 forcerait B + a₁₀ + 3f₁₁ + a₁₂^frac ≥ 318 + 17a₇ + 2a₉.
   - Réserve : dérivation de l'agent ; vérifier si les a₁₁ et a₁₂ de #489 comptent aussi les vecteurs fractionnaires. Aux normes 14 à 20, L1 et L coïncident (L06-001).
2. **Rang 37 sans grille : apices × P ≤ 852 × seuil.**
   - C14 + 2τ ≤ 2P (L11c-135) et P ≤ 852 (L07-237, L08-067) donnent τ ≤ 852, alors que L06-049 demande τ_n < 535.
   - Avec « au plus un jumeau » (ouvert), τ ≤ 426 laisserait environ 3,5 M aux canaux hors C6 ; ces canaux ne sont pas bornés finement sous ρ = 0 (L11c-135).
   - Chaîne : K4 (aucune grille au rang 37) + K24 + bornes C7 à C9 sous ρ = 0.
3. **Quadrangle comme base de reconstruction.** Δ(Q) carré parfait divisible par 49 (L11c-091), connexité des murs (L11c-092) et lemme A sur S = N(Q) ou Q ∪ N(Q) (L11c-137). C'est un objet présent 2079 fois dans tout candidat ; il manque la classification des structures à quatre murs.
4. **Lemme triangulaire de la note 243 × chemin critique.**
   - Lemme (sans rang) : Σ_T x(T)² = 78, e_tri ≥ 6 ou ≥ 22 pour tout vecteur de L1 de norme 26 (L11c-116).
   - Chemin critique L10-035 : aux rangs 37, 39, 41, un vecteur de norme 18 ou 26 est exigé.
   - À essayer : contraindre ce vecteur de norme 26.
5. **Lemme 14 de LAP (sans rang) aux rangs 37 à 41.** e(X) = e(Y) ≤ 5 pour tout vecteur binaire de norme 28 (L11c-118). Avec les techniques de S0 transférées (combinaison γ, L02-460).
6. **Déjà proposées par L02** (à ne pas refaire) :
   - α : rigidité × ordres d'automorphisme, L02-458.
   - ε : lemmes A et B sur les configurations ouvertes, L02-462.


<!-- ===== L11d_pont.md:607-694 ===== -->

## Matériaux pour la recombinaison

### 1. Énoncés conditionnels « si X, alors … » (X précis, statut de X)

| # | Conditionnel | Statut de X / des maillons | Source |
|---|---|---|---|
| C1 | Si N16 et N18 sont exclus au rang 37 ET si c_20 ≤ 4 (au plus 4 vecteurs orientés de norme 20 par graine indépendante ; c_20 ≤ 6 avec supports indépendants seuls), alors le rang 37 est exclu (34 418 > 7920·c_20). | N14 : E non audité ; identité : C ; b_3 ≥ 45 898 : Codex note 196 (non revérifié ici) ; N16@37, N18@37, c_20 ≤ 4 : O | L11d-027 (pont:#551, #552) |
| C2 | Si aucun vecteur propre entier −4 de norme 18 ni 26 n'existe, les rangs 37, 39, 41 sont exclus ; au rang 43 il faut en plus a_8 < 1316. | Échelle : P ; a_8 ≤ 6930 (note 173) ; prémisses O | L11d-046 (pont:#567, #609) |
| C3 | Si le monde de norme 20 meurt par la borne de rang réel (25 doubles toujours dépendants, 15 relations exigées sur D + Z), alors a_10 = 0 à tout rang. | O (« jamais testé ») | L11d-008 (pont:#542) |
| C4 | Si le plafond 31 976 (paire jumelle non grille, collection (9,0)) baisse de 14 % (≤ 27 684), le coin sans grille du LP de comptage se ferme. | H (LP flottant) ; coin à grilles et masses 7–9 restent ouverts | L11d-007 (pont:#541) |
| C5 | Si les bords de Hoffman (22) ET les sept profils de cocliques de 21 maximales sont exclus, ET si α ≥ 21, alors pas de Conway ; sans α ≥ 21, seulement α ≤ 20. | Logique : P (relue par Codex) ; α ≥ 21 : O ; (0,2) : O ; (1,3)/E = K3 exclu (P), E = P3 O | L11d-090, L11d-062, L11d-065 |
| C6 | Si les onze répartitions de cycles autour d'une arête quelconque (bord de 27 sommets, 72 restants) sont toutes exclues avec attaches générales, alors C1 est exclu. | O (non tenté ; « ce qui manque est considérable ») | L11d-069 (pont:#582) |
| C7 | Fermer (0,2) ferme un des sept profils numériques d'une coclique maximale de 21 (pas C1, ni α = 22, ni α ≤ 20). | Portée (P) | L11d-069 |
| C8 | H3 + L8 ⇒ pas de Conway. | H3 RÉFUTÉE (L11d-172) ; de plus insuffisant (rang 30 − δ', L07_C1_asym_local-063) | L11d-168 |
| C9 | (A) + (C) ⇒ pas de Conway ; (A) ⇒ toutes les droites spéciales ⇒ (B) ; (B) ⇒ route finie (racine en droite spéciale, bases décomposables, filtre de colonnes). | (A) : O dans le lot, R ensuite (L07_C1_asym_local-065) ⇒ C9 mort pour (A) ; (B), (C) : O ; coût de la route finie non borné (~10⁸–10⁹ bases, L11d-179) | L11d-175 |
| C10 | H3'' (toute relation à trois étoiles est portée par les deux étoiles mates) ⇒ chaque drapeau (v,l) a Q(v,l) non connexe (squelette décomposable partout) ⇒ analyse globale « à la L8 » à faire. | O | L11d-175 (pont:#718) |
| C11 | Si l'instance ENTIÈRE préserve deux flips individuels (poids < ⌈t/2⌉) et si le nombre de complétions est ≤ 2 (régime V15), la branche est exclue pour tout SRG ; pour C1 : si un groupe L de l'instance agit et que les complétions sont ≤ U < |L|, aucune complétion C1. | Filtre : P ; aucune branche exhibée | L11d-159, L11d-157 |
| C12 | Dans un C1, le nombre de complétions de toute pièce H est un multiple de |Aut(H)| ; une pièce FORCÉE avec plus de symétries que de complétions exclut C1. | P (note 171 §7) ; pièce forcée symétrique : O | L11d-154, L11d-137 |
| C13 | L'asymétrie ne devient une exclusion qu'avec une borne SUPÉRIEURE de complétions d'un hôte symétrique inférieure à l'ordre de son groupe. | H (programme) | L11d-158 |
| C14 | Sur un bord 43 positif, ≥ 3 composantes de signes forcés ⇒ un co-Heawood disjoint du bord ⇒ deux cocliques de 22 se coupant en 15. | P | L11d-103 |
| C15 | Si h = dim ker[D;1ᵗ] ≤ 2, toutes les complétions d'un même facteur sont isomorphes par un échange ; si D a ses colonnes distinctes (ou m ≤ 25), la complétion est unique. | P | L11d-097 |
| C16 | Si un Conway contient une grille 3 × 3 (composante μ = 1 de H_l), alors (B) (droite spéciale). | Implication : P ; existence d'une grille : O | L11d-183, L11d-185 |
| C17 | Une relation z = 2q + u avec u à 4 ou 6 entrées impaires (8 sur trois étoiles) n'existe dans aucune complétion Conway. | P | L11d-184 |
| C18 | Un monde de norme 16 de rang 33 ayant une cellule morte est exclu au rang 37 ; N16 au rang 37 = catalogue × (0,3 s à 1 min par monde). | E ; catalogue incomplet | L11d-023 |
| C19 | Exclure la branche co-Heawood sans hypothèse de rang ne ferme aucun rang. | P/H | L11d-046, L11d-048 |

### 2. Bornes quantitatives (objet, inégalité, statut)

**Rang 37 / thêta** : vecteurs −4 de norme 14 au rang 37 : 0 (E, L11d-002) ; 350a_8 + 91a_9 + 13a_10 ≥ 447 412 (C, L11d-027) ⇒ a_8 ≥ 1280 ou a_9 ≥ 4918 ou a_10 ≥ 34 418 ; bornes par graine a_8 ≤ 6930, a_9 ≤ 6160·c_18, a_10 ≤ 7920·c_20 (Codex, notes 173/176) ; LAP : ≥ 22 / ≥ 82 / ≥ 574 (E, L11d-024) ; rang 43 : ≥ 1316 vecteurs de norme 16 sans norme 18/26 (P, L11d-046) ; rang réel extérieur ≤ 44 − 2m (P, L11d-008) ; r − 28 coordonnées libres par sommet de bord (L11d-045).
**Thêta niveau 7 (nuit du 14/10)** : rang_7(A + 4I) ≥ 29, 31, 33, 35 (C ; plus faible que la fenêtre connue) ; a_2 ≥ 462 ; a_4 ≥ 14 970 → 354 816 → 1 749 546 ; a_3 ≥ 24 948 ; a_5 ≥ 196 812 ; c_7 ≤ 7920 puis ≤ 792 ; N_16(B) ≤ 360 360 (b = 28 exige 1,06e6) ; b = 34 exige a_4 > 1,42e7 (1,31e7 si a_5 ≥ 3e7) contre ~3,6e6 prouvables (+ 2 057 064 bruts) (L11d-118 … L11d-124, L11d-129, L11d-131).
**Cœurs et mondes** : cœurs 1 / 5 / 26 (25) / 1199 (753) + 182 (132) (E) ; norme 16 : cadre 35 de rang ≤ 33 ; 344 candidats (cœur8/attache0) ; 71 351 supports PSD sur 5 attaches ; 6 303 880 candidats « mineurs ≤ 4 » ; 18 attaches entières exclues sur 478 ; 463 attaches à C mixte non tranchées ; positions d'arête D 3317 → 2145 → 467 → 438 ; ≤ 51 paires cœur/Z, 11 formes Z ; 30 484 supports PSD (cas4/1) ; 128 / 64 / 56 (sous-branche C_de = 1) ; norme 18 : ‖b‖² = 504, Σb = 180, ‖w‖² = 117/7 ; Σc = 90, Σc² = 198, Σ(c − 1)(c − 2) = 36 ; > 1e13 mondes par noyau (H) ; 2 317 413 ensembles de doubles positifs sur une tranche (E).
**Co-Heawood** : ≤ 396 co-Heawoods induits (≤ 792 vecteurs signés) (P) ; familles orthogonales ≤ 12 (C) ; aucune arête dans 3 orthogonaux (C) ; |f·g| ∈ {0,1,2,4} ; norme ≤ 24 ⇒ coordonnées 0, ±1 ; norme 24 : e ≤ 0,0,1,1,2,3 pour p = 7..12 (P) ; branche : 33 508 cas, ~3e22 secondes lignes par base (H), bloc 20 × 20 de rang 18 (jamais ≤ 16, échantillonné), H de rang 9 et valeurs propres dans [0 ; 76,73], 2^21 appariements, Gram résiduel de rang 16 avec H² = 147H.
**Triangles et grilles** : p(T) ≤ 12 par droite ; p̄ ≤ 588/59 ; il existe T avec p ≤ 9 (pas pour tout T) ; prismes ≤ 1150 (P ; ≤ 852 connu, plus fort) ; ρ(R) < 10 ; ≤ 191 grilles ; ≤ 11 triangles deux à deux sans arête ; paires de prismes jumeaux ≤ 2871 ; < 21 grilles par sommet (T1 : S + C), pas de K6 dans le graphe des grilles (kk6 : S), K5 force les deux autres (S) ; aucun 9-ensemble à 17 arêtes (P) ; p(T) = 12 : 790 → 192 types.
**Noyaux et collisions** : noyaux +3 de masse ≤ 16 : ≤ 313 434 (somme 0), ≤ 597 744 (somme ±9), ≤ 911 178 au total ; couches norme 12 ≤ 5742, 14 ≤ 8316, 16 ≤ 278 586, 18/20 ≤ 20 790 ; H7 ≤ 4158 ; collisions dans D : ≤ 2508 (norme 12), ≤ 184 (norme 14), ≤ 15 932 268 paires (C).
**Automorphismes** : tout automorphisme non trivial d'un Conway déplace ≥ 13 sommets (P, non relu, L11d-102) ; noyau des automorphismes fixant x et chaque paire : code binaire de longueur 7, distance ≥ 4, ordre ≤ 8 ; flips de 1 à 3 paires impossibles (P, L11d-157) ; K_x de Conway : 273 des 693 arêtes (L11d-154).
**Complétion** : V7 : ≤ 2^δ complétions, δ ≤ h(h − 1)/2 ; V13 : q = (tr E0 + 3h)/7 = 44 − rang(3I − B + J/9) ; V15 : bord 43 positif ⇒ ≤ 8192 affectations, ≤ 2 complétions étiquetées ; bord 44 positif ⇒ unique ; 1540 paires extérieures ; V14 : différence de rang 2 = transposition, support 26 (24 + 24 arêtes) ; dimension linéaire de la complétion de K_x ≥ 1393 (99), ≥ 15 081 (243) ; défaut de modèle partiel : σ ≤ 49/4, G nul hors de ]−4, 3[.
**Cocliques** : coclique de 21 : pas de b ∈ {6,7} ; 2 ≤ n5 ≤ 6 ; n3 = 6 + 3a + 3e ; n4 = 66 − a − 3e ; sept profils ; supp(q) ≤ 30 (64 à c = 20) ; composante w < 0 ou > 18δ ; p ≤ 6 (e = 5), p ≤ 7 (e = 6) ; (0,2) : bord 61/38, 24 voisins exclusifs, onze partitions de 6, bords 59/60 et 39/40 ; 21 puis 304 conditions (non additives) ; 61 branches (a, b, classe de t) ; V12 : 16 / 48 quadruplets au lieu de 256.
**Bords de Hoffman** : |F| ≥ 77, |D_i| ≥ 11 ; f_ij ≥ 2 − z_ij + D_ij ; boule de 37 designs exclue ; familles à 4, 5, 6 points libres exclues (S, C, E) ; 7 ouverte.
**Trois étoiles / objet 49** : rang ≤ 30 (3 relations automatiques + 1) ; quatre étoiles : 10 relations de plus ; nullité(T_S4) ≥ 14 ; relations mixtes ≥ 12 − c_l − c_m + [carré] ≥ 1 (≥ 10 si non spéciales) ; rang T_X = 23 − c ; U50 : degrés 6, 7, 8, ≤ 3 de degré 8, |E(U)| = 164 + ε ; 94 743 / 25 926 profils ; ≤ 1800 positions ; Σρ_u = 56(30 − r) ; base à c = 1 : 4356 profils bruts par colonne, budget 752 ; e_croisées − e_même ≤ 45 ; Z5 : 595/10 000 PSD, 572 avec U ⪰ 0 ; mult_3(A_Σ) ≥ |Σ| − 45, mult_−4(A_Σ) ≥ |Σ| − 55 ; lointains d'une droite : mult(−4) = 7 + c(l), mult(3) = 18.
**Code F2** : dim im_F2(A) = 54 ; poids minimal ≥ 8 (≥ 10 sur trois étoiles, ≥ 10 sur trois voisinages) ; C⊥ : poids ≥ 8 ; Conway au poids 10 sur trois voisinages : six formes abstraites.
**Familles voisines** : 243 : 8 graphes (|Aut| 3 849 120, 4320, 864, 3888, 2916, 108, 162, 108) ; Z3-revêtements : exactement 4 (1154 solutions au signe près) ; S3 : aucun (C) ; coclique 45 : BvLS seulement ; 44 indécis ; 378 : |Aut| = 6 (59 orbites régulières) ; seuil de rigidité |F| ≈ 280, P_ii·P_jj ≥ 1/900 ; Payne : rang F2 441, noyau 288 doublement pair ; rareté : FTWKB(5) |K| = 9·10⁶ contre N = 3,18·10⁶, H(3,25) 5,9·10¹⁰ contre 7,7·10⁶, BH 233 280 contre 1154.

### 3. Lemmes ouverts ou étapes manquantes (et ce qu'ils donneraient)

- **c_20 ≤ 4** (avec N16 et N18 au rang 37) ⇒ rang 37 exclu (L11d-027).
- **Catalogue complet N16** (attaches à C mixte, sous-branches) ⇒ N16 au rang 37 par n16cell ; écrire les mondes de rang 32/31 et les paires de cellules (L11d-023).
- **Norme 18 au rang 37–41** : modèle global (V13 avec régularité, H_− ≻ 0 sur tout support de norme 18) ; borne sur le nombre de facteurs D par noyau (L11d-092, L11d-101).
- **Norme 20** par le levier 44 − 2m ⇒ a_10 = 0 à tout rang (L11d-008).
- **α ≥ 21** ⇒ le cadre coclique deviendrait une route vers C1 (L11d-090).
- **(0,2) entière** (ε = 1, onze répartitions), **E = P3** dans (1,3), cinq autres profils (L11d-068, L11d-065).
- **Recherche de Q dans le cas singulier** (V6/V13) et construction/coupe de (B, D) avant la phase de complétion (L11d-074, L11d-100).
- **Instancier le filtre d'action libre** : un bord forcé dont l'instance préserve deux flips (L11d-159).
- **(B) / (C)** et un critère sur la base (L11d-175, L11d-181) ; **existence d'une grille** ⇒ (B) (L11d-183).
- **« Pas de 8-cycle UUVV »** et (P) ⇒ les onze partitions tomberaient à 51, 411, 3111, 1⁶ (L11d-087, L11d-088).
- **Une droite à 12 prismes** (192 types) ; **K5 + K2** en un sommet (L11d-113, L11d-114).
- **Unicité des complétions de K_0** pour Γ6/Γ8 (certificat ΠCΠ) ; **conjecture S** (L11d-153, L11d-155).
- **Hoffman à 7 points libres** ; filtre de parité du graphe L (L11d-058, L11d-059).
- **Familles de support 9–10 forcées** pour b = 34 ; niveau 63 avec les 99 vecteurs-sommets (L11d-129).
- **Certifications** : DRAT pour T1, kk6, les calibrations du modèle enraciné ; ré-implémentation indépendante de l'encodage S3 ; rédaction du lemme « ≥ 13 sommets déplacés » (L11d-107, L11d-110, L11d-149, L11d-067, L11d-102).

### 4. Méthodes transférables (analogies ; en quoi les objets diffèrent)

- **Complétion par projecteurs** (V6/V13/V15, à 99) ↔ **complétion par lignes et projecteurs entiers à 243** (LAB, Δ = 9(E' − E), row_clique) : même structure E0 + r·P − (r − s)Q ; mais à 243 le bord vient d'un graphe connu, à 99 il faut produire (B, D) ; r − s = 7 (99), 9 (243), 15 (378).
- **Rigidité de rang 2** (V14) : vaut pour λ = μ − 1 en remplaçant 12 par ν = k − μ (donc transposable à (243,22,1,2) avec ν = 20) ; faux pour SRG(16,6,2,2) (contre-exemple de Codex).
- **Critère de concentration** (tout srg) : seuil 1/(2(r − s))² = 1/196 (99), 1/324 (243), 1/900 (378) ; à 99 il n'y a pas de graphe-germe : utilisable seulement à l'intérieur d'une recherche de complétion.
- **Lemme d'extension / levier** : à 243 et 378 on mesure |G_B|/#complétions ; pour C1 il devient « #complétions multiple de |Aut(H)| ».
- **Théorème de majorité** : srg(1 + 2t², 2t, 1, 2) ; t = 7 (99) et 11 (243), même borne d'ordre 8 pour le noyau.
- **Code F2 de im(A)** : tout SRG(v,k,1,μ) avec μ pair (poids ≥ 8 à 99, ≥ 12 à 243) ; lemme de localisation pour μ = 2.
- **Loi des charges carrées** Q ≥ (2k + 1)T − M·k(k + 1) : tout bord induit de tout srg(v,k,1,2) (seules les constantes de K_B changent).
- **Moments de repères serrés** (sommets/droites) : transposables aux autres λ = 1 ; à 99 ils donnent moins que le certificat d'ordre 9 (P ≤ 852).
- **Formes modulaires de niveau 7** (réseaux A, B des droites, rang_7(A + 4I)) ↔ **mission C2** (formes de poids 11, représentation de Weil, enveloppe U de rang 24 avec deux normales) : même outil, objets différents (réseau −4 de rang 44 contre réseau unimodulaire de rang 24).
- **Classification des Z3-revêtements** (partie linéaire F3 + DFS + comptage d'orbites) ↔ signings S3 fixés, ou quotients par un automorphisme (C3) ; à 99 il n'y a pas de spread régulier (L06-129), donc pas de structure de revêtement.
- **Filtre de colonnes** (norme exactement 20 au rang 30) et **critères η / F** de réponse de rang 2 : transposables aux bords à 4–5 étoiles ; obstruction propre à chaque objet (pas de règle 2-adique).
- **Classification à deux étoiles** (somme de carrés, rang 23 − c) : propre à λ = 1, μ = 2, t = 7 ; l'analogue à 243 (t = 11) n'est pas établi.
- **Couvertures doubles de Hoffman** (22) ↔ toute coclique (couvertures de taille 15 − |B_i|) ; à 243 la coclique de Hoffman (45) n'existe que dans BvLS.
- **3-ovoïdes de GQ** : seulement 243 (numérique, non réalisé dans Payne) et 378 ; Conway n'est pas un 3-ovoïde : méthode non transférable à 99.
- **Reconstruction incrémentale avec propagation des paires saturées** (Codex) ↔ **listes de lignes** (LAB) : applicables à 99 seulement à partir d'un bord construit.

### 5. Combinaisons candidates issues de ce lot (à soumettre à vérification adverse)

- **K1 — V15 × levier (C1)** : dans un C1, une pièce H = (bord 43 positif, facteur D fixé) a au plus 2 complétions (L11d-100) et un nombre de complétions multiple de |Aut(H)| (L11d-154) ; donc |Aut(H)| ≤ 2 pour toute telle pièce ; avec L11d-097, deux complétions diffèrent par une transposition de deux extérieurs à colonnes égales, qui est elle-même dans Aut(H). Conséquence à vérifier : aucune pièce (B43 positif, D) d'un C1 n'a de symétrie d'ordre ≥ 3. Maillons : V15 et V14 P (non relus par LAB) ; définition exacte de Aut(H) (préserver B, D et l'instance) à préciser. Pas une exclusion tant qu'on n'exhibe pas une pièce forcée symétrique.
- **K2 — dichotomie V15 × N14** : au rang 37, aucun vecteur −4 de norme 14 (L11d-002, E non audité), donc aucun co-Heawood ; par L11d-103, tout facteur commun (B43 positif, D) d'un graphe de rang 37 se décide par au plus deux affectations de signes. Réduction de coût de la complétion au rang 37, pas une exclusion ; dépend de N14 et de V15.
- **K3 — (fausse piste à écarter)** « N14 × co-Heawood ⇔ deux cocliques de 22 » : redondant, N14 est précisément l'absence du monde co-Heawood/Fano au rang 37.
- **K4 — V15 × flips × majorité** : exhiber un bord 43 positif FORCÉ dont l'instance est invariante sous deux flips individuels exclurait la branche pour tout SRG (L11d-159) ; lemme manquant : l'existence d'un tel bord forcé.
- **K5 — grilles** : (B) ⇐ existence d'une grille (L11d-183) ; bornes supérieures ≤ 191 grilles et < 21 par sommet (L11d-117, L11d-107), aucune borne inférieure dans ce lot : chercher dans d'autres lots un énoncé « tout Conway contient une grille 3 × 3 » ou « une droite dans une grille » ; à croiser aussi avec le Théorème D′ du labo C2 (L01-31).
- **K6 — échelle × norme 18 × V15** : les rangs 37–41 exigent un vecteur de norme 18 (ou 26) (L11d-046) ; tout support de norme 18 se prolonge en un bord 43 positif (L11d-101), dont chaque facteur D se complète en ≤ 8192 signes (≤ 2 sans co-Heawood) : la question se ramène au nombre de facteurs D compatibles avec les 26 noyaux (lemme manquant ; aucune borne dans ce lot).
- **K7 — c_20** : chercher dans les lots de Codex (L05) une borne « vecteurs de norme 20 par graine indépendante » (≤ 4, ou ≤ 6 avec supports indépendants) : avec N16 et N18 au rang 37, elle fermerait le rang 37 (L11d-027).
- **K8 — (probablement négative) plafond 31 976 × N9** : L06-043 indique « paire non-grille ≤ 31 976 (23 150 sans les indicatrices de 9-ensembles) », or 23 150 < 27 684 (L11d-007) ; mais N9 (L11d-116) n'élimine que les 9-ensembles à 17 arêtes (norme projetée 2), alors que les indicatrices de 9-ensembles du canal de collisions semblent être celles à 14 arêtes (norme 8, L06-159) : pas de combinaison directe ; à vérifier avant d'écarter (et le LP reste flottant).


<!-- ===== L11e_pont.md:362-487 ===== -->

## 10. Matériaux pour la recombinaison

### 10.1 Énoncés conditionnels « si X, alors exclusion »

| # | X (précis) | conclusion | statut de l'implication | statut de X | source |
|---|---|---|---|---|---|
| K1 | (H-MATCH) : tout bloc à 4 étoiles admissible, T, U >= 0, nullité >= 14 a M_1 = h(M_0) et M_3 = h(M_2) | pas de Conway (21 grilles en un sommet : point de Hamming, contre L8) | P (relu par un agent, selon #785 ; accepté par Codex) | O (route locale déclarée épuisée, #884) | pont:#785, L11e-046 |
| K2 | (N9-NG) : bloc PSD sans grille ⇒ nullité <= 9 + min(c(l), c(m)) ; ou seulement NG5 (non-grille et ν >= 14 ⇒ c >= 5 des deux côtés) | t(l) >= 8 pour toute droite, P >= 924 > 852 et ρ >= 154 > 126 : pas de Conway | P (vérifiée par Codex, #853) | O | pont:#850, #853, L11e-091 |
| K3 | (NG7) : aucun bloc non-grille avec min(t(l), t(m)) <= 7 ne passe T/U PSD, ν >= 14, F7, DISC, extension | pas de Conway (il en existe >= 254) | P | O | pont:#851, L11e-092 |
| K4 | rang F >= 12 pour tout bloc sans grille, orienté sur la droite de c minimum (⇔ N9-NG ⇔ corank(Q) <= 7) | contradiction avec rang F <= 7 + c_min <= 11 | P | O (données : vrai sur ~7 444 côtés sans grille) | pont:#926-#928, L11e-126 |
| K5 | ODDCONST et SYM6 sur tous les côtés sans grille (Q7) | pas de Conway (avec P <= 852) | P | O | pont:#928, L11e-127 |
| K6 | ODD-PURE (rang D = 9) et rang Z >= 1, >= 2, >= 3 respectivement à c_min = 2, 3, 4 (c_min = 1 est déjà impossible sous ODD-PURE) | pas de Conway | P | O | pont:#931, #932, L11e-127 |
| K7 | (R7-NG) : tout bloc PSD sans grille a rang_F7(8T_S) >= 29 | pas de Conway (avec L4/L22 et N2) | P | O (données : >= 30 sur 3722 blocs, mais 93 % ont (01)(23) pour automorphisme ; à 243 le recollement est normal aux paires sans grille) | pont:#941, #947, #949, L11e-131 |
| K8 | (R7) : PSD ⇒ rang_7 >= 29 ; (K22) : PSD et ν >= 14 ⇒ rang_7 >= 23 | Conway exclu ; k = 22 (r = 37) exclu | P | (R7) R (grilles à 25) ; (K22) O | pont:#774, L11e-038 |
| K9 | positivité à 4 étoiles incompatible avec 8 - δ chutes 7-adiques (au rang 37) | r = 37 exclu | proposition (non rédigée) | O | pont:#784, L11e-044 |
| K10 | il n'existe aucune structure admissible à cinq étoiles (52 labels) | pas de Conway | P (relaxation) | O (18/34 cas en TIMEOUT 90 min) | pont:#890, #907, L11e-112 |
| K11 | R8 (4 étoiles exactes + les 8 labels {4,t}) UNSAT | pas de Conway | P (relaxation de la 5e étoile) | O | pont:#918, L11e-123 |
| K12 | H46-c1 : c(l) = 1 ⇒ λ_2(A_H) < 3 sur H = N(l) ∪ (N(x) privé de N[l]) | aucune droite c = 1 (l'entrelacement impose λ_2 = 3) | P | O (données : 3480/3480 cas c = 1) | pont:#952, L11e-138 |
| K13 | « toute droite est dans une grille » | c = 1 impossible | P (immédiat) | O (aucun mécanisme, pont:#956) | pont:#954, L11e-139 |
| K14 | (B') : aucun bloc PSD de ν >= 14 n'a de droite c = 1 | toute droite de Conway spéciale (pas une exclusion seule) | P | O | pont:#843, #961, L11e-140 |
| K15 | t(l), t(m) >= 8 ou t(l) + t(m) >= 15 sous la condition à 4 étoiles ; 4 grilles par droite | P >= 924 / 867 > 852 ; ρ >= 154 > 126 | P | O | pont:#762, #765, L11e-025 |
| K16 | MIX <= 2 ; MIX <= 3 (borne universelle des relations mixtes) | ρ >= 198 > 191 ; ρ >= 154 > 126 | P (réduction non re-vérifiée par Codex) | R (#782) | pont:#778, L11e-039 |
| K17 | aucun bloc PSD ne porte >= 4 relations mixtes | pas de Conway (avec le budget >= 336 drapeaux) | P | R (c31_mix4, c21_mix4, c11_mix6) | pont:#781, #782 |
| K18 | (A4) ; (A) ; ODD9 ; H4' | toutes les droites spéciales, ou au plus une non spéciale par sommet | P | (A4), (A), ODD9 : R ; H4' : O | pont:#741, #746, #785 |
| K19 | moyenne de ‖E_vlm‖_F² sur les 2079 triplets > ~1190 | P < 0, contradiction | P | inutilisable seul : 504 est atteignable dans la relaxation (#770) | pont:#768, L11e-029, -031 |
| K20 | KER-SYM (noyau de grande nullité invariant par une h·p) | H-MATCH se réduit à un nombre fini de types de p | indicatif | universelle : R ; ν >= 14 : O | pont:#837, L11e-080 |
| K21 | une borne strictement positive d'un défaut pour tous les candidats binaires (selon #910 ; formulation à clarifier) | contradiction globale | annoncée sans preuve | O | pont:#910, L11e-120 |
| K22 | nombre de complétions étiquetées d'un bord H < ordre de Aut(H) | pas de complétion asymétrique de H | P (critère) | application aux bords 43/44 : O | pont:#923, L11e-125 |
| K23 | branche « minimum GLOBAL c >= 4 » entièrement fermée | tout Conway a une droite c <= 3 | P | S (76/79 au 17/10 ; 79/79 au 18/10 par CP-SAT, hors lot) | pont:#940-#966, L11e-133 |

### 10.2 Bornes quantitatives

| objet | inégalité | statut | source |
|---|---|---|---|
| poids d'une 4e relation positive normalisée (trois étoiles) | w >= 16 ; masse <= 12 ⇒ seulement 0 et les trois étoiles | C | pont:#734, #736 |
| profils de poids 16 | 1149 exclus sur 1420, 271 restent ; >= 2 paires extérieures actives | S | pont:#740 |
| rang d'un bloc à quatre étoiles dans Conway | rang T_S4 = 30 - δ (<= 30) ; mixtes = 12 - c_l - c_m + [grille] + δ | P | pont:#761 |
| nullités non triviales (famille G1) | >= 9 - min(c_l, c_m) si rang <= 30 | P | pont:#755 |
| prismes P, grilles ρ | P <= 1151 → 1150 ; 6ρ <= P ; 1386 - P - 5ρ >= 0 ; ρ <= 126 ; P <= 11088/13 (852) | C | pont:#779 |
| transversales moyennes | t moyen <= 7,38 (P <= 852) | P | pont:#762 |
| relations mixtes, au total | Σ mixtes = 12474 - 45ρ + 3O + 6H + Δ >= 6804 ; moyenne >= 36/11 ; excès >= 567 | P | pont:#779 |
| drapeaux à >= 4 mixtes | >= 336 des 2079 ; >= 18 sommets ; 13b + 20e >= 273 | P | pont:#780 |
| minimum de grilles par sommet sous MIX <= M | 18, 14, 10, 6 pour M = 2, 3, 4, 5 ; ρ >= 11·min | P | pont:#778 |
| blocs non-grille | >= 4 par sommet, >= 396 au total (>= 945 avec ρ <= 126) | P | pont:#849 |
| blocs non-grille à min t <= 7 | >= 254 ; droites t <= 7 : >= 18 ; e(L) <= floor(7m/2 + m²/42) | P | pont:#851, #853 |
| coupe plate | e(O ∪ S) <= 48 (au lieu de 49) ; e(S) <= 44 si O grille | P | pont:#840 |
| second moment | 15‖E‖² + 86trE + 92h - 74ΣE <= 3520 ; 5Σ‖E‖² + 928P + 48Z <= 12374208 ; 5Δ_global + 448P - 72Z <= 7135128 | P | pont:#767, #770 |
| compressions U extérieures | coupes strictes : somme >= -31 (anti), >= -127 (sym) | P | pont:#749 |
| spectre d'une droite (secteur impair) | T = 6I - Q ∈ [2,10], U = 8I + Q ∈ [4,12] sur 1⊥ | P | pont:#771 |
| énergie paire | E >= G/5 + (2/5)(I - M) >= G/5 ; rang E = 12 - c(m) | P | pont:#934 |
| rang de G (bord SYM6) | rang G = 11 - c(m) ; rang L = 10 - c(m) >= 5 hors grille | P | pont:#933 |
| Conway avec c_min <= 4 | rang F <= 7 + c_min <= 11 ; sous rang D = 9 : rang Z <= c - 2 | P | pont:#927, #931 |
| données Q20 | corank(Q) <= 7 sur ~7 444 côtés sans grille ; jusqu'à 11 avec grille | E | pont:#928 |
| rang_F7 de familles locales | G1 c55 non grille : >= 29 ; <z, hM> à nullité 14 : >= 29 ; global <= 28 (L22) | C | pont:#777, #822 |
| nullité de <z, hM> | null T <= 14 (preuve) ; plafond local 9 (SAT) ; <= 9 prouvé dans 7 des 14 types (mod 5) | C / S / P | pont:#822, #826, #829 |
| prolongement c55 | >= 29 des 40 profils brisent h ; histogramme exact (10,24,6) | P | pont:#773 |
| cinq étoiles | D >= 12 (>= 3 lignes cassent h) ; D >= 2k - 16 ; >= 4 lignes vers l'ancien 44 ; φ : D >= 12 + 2t - 4δ >= 10 ; joint : broken_union + AND(diagonales) >= 4 | P | pont:#894, #896, #900, #902 |
| symétries à cinq étoiles | 2f <= 10 (g agit comme h sur {0,1,2,3}, fixe 4 et f lettres) | P | pont:#901 |
| orientations d'une moyenne à 40 cassures simples | <= 4096 modulo h (64 si valences 2) | P | pont:#800 |
| bloc mixte | ‖B‖_F² = b/2 ; q/2 <= ‖B‖_F² <= q ; ‖B‖_op² >= b/20 | P | pont:#793 |
| volume | (α_1…α_p)(β_1…β_p) <= 1 si nullité T >= nullité T0 + p | P | pont:#802 |
| vecteurs propres -4 entiers | ‖h‖² >= m² + 7·abs(m) ; r² + s² + 7(r + s) + 2e(r + s + 1) + 2c <= N + 4 ; N = 28 ⇒ au plus un +2 et un -2 | P | pont:#956, #966 |
| rectangles | e(Q_ij) ≠ 3 | P | pont:#957 |
| inégalité signée (15 étiquettes) | e(P7) + e(N8) - e(P7,N8) <= 14 | P | pont:#891 |
| témoin 15 lignes | Σ (motif de 58 arêtes) <= 57 | P | pont:#904 |
| R8 (Conway) | n_1 + n_2 >= 8 + a (36 labels contre 28 - a paires) | P | pont:#918 |
| famille (v,k,1,2) | Σ_F (n_C - 2c/(k-2))² = (k - 14)c(1 - c/(3(k-2))) ; (k-4)(k-14)/2 sommets hors grille ; D_k = 8 + a - (k-14)(k-7)/2 | P | pont:#922, #923 |
| sous-graphes induits à 46 sommets | λ_2 = 3 exactement (entrelacement) | P | pont:#952 |
| c = 1 | ν = 2 + dim ker F ; Conway exige dim ker F >= 12 ; données 5 à 8 | P / E | pont:#952 |
| quotient de composantes | dim ker C <= 4 (min c = 4) ; = 14 si toutes les droites racine ont c = 1 | P | pont:#940, #963 |
| racine de budget | Σ_{l∋x} t(l) <= 51 pour une racine (6P <= 5112) | P | pont:#942 |
| gabarits min c = 4 | 200 configurations ; 100 puis 79 gabarits ; 76/79 exclus ; Gram 456/19/510 ouverts | S | pont:#940-#966 |
| discriminants | det(8T_I) ∈ {2, 14} × carré ; det(ker B ∩ Z^84) = 2^21·3^8·5^6 ; 15U : classe 1 ou 7 | P | pont:#886, #887 |
| germes de rang 30 | 643 (ou 645) sur 643, tous en échec DISC | E | pont:#887, #907 |
| classes de noyau | 287 puis 416 complètes (413) sans cassée de ν >= 14 ; obj53 : 15 936 structures, 9 408 cassées, 0 PSD | S | pont:#799, #884 |
| G1'' | >= 3·10^8 structures (estimation, non certifiée) ; 26 811 cubes = 81 × 331 | E / H | pont:#809, #811 |
| <Z5, hM> | 339 556 structures, 192 PSD, max 9 ; t = (12,12) : 4 788, 0 PSD | S | pont:#823, #826 |
| groupe du cadre | ordre 30 720 ; |G_N| = 1920 pour rep_006 et rep_037 | E | pont:#801 |

### 10.3 Lemmes ouverts ou étapes manquantes, et ce qu'ils donneraient

- **H-MATCH** ⇒ exclusion de Conway (K1). Il manque un argument binaire/C1/C2 excluant la saturation simultanée (pont:#876). Sous-étape manquante pour la voie fractionnaire : « nullité 14 ⇒ rang A = 10 » (pont:#790), et (H-INV) (pont:#788).
- **NG5 / NG7 / N9-NG / rang F >= 12** ⇒ exclusion (K2-K4). Étapes : prouver hors grille rang S >= 9, 10, 11, 12 pour c_l = 1..4 (pont:#857) ; ou ODD-PURE + rang Z >= c - 1 (K6) ; ou (SYM) + (QUOT) (pont:#860).
- **ODD-PURE** (rang D = 9) : une saturation λ = 1 à profil impair non constant doit contredire les comptes entiers. Une borne uniforme est exclue (λ_max jusqu'à 0,99993, pont:#938).
- **SYM6** (rang Z >= 3) : piste scalaire (trZ)² > 2tr(Z²) ou mineur 3x3 positif (pont:#929, #931) ; échec connu de la trace normalisée (pont:#936).
- **(R7-NG)** ⇒ exclusion (K7) : il faut z + σ >= 2 hors grille (b = 0 sans grille, pont:#947) ; or à 243 le recollement σ est le mécanisme normal (pont:#949).
- **Classification de δ > 0** (vecteur propre -4 global supporté sur les 40 extérieurs) : question (a) de pont:#761, sans réponse. Elle relierait G9, R7-NG (z = δ) et les blocs de rang 29.
- **Cinq étoiles sans base / R8** ⇒ exclusion (K10, K11) : il faut une contrainte nouvelle (globale), la force brute étant sans coût borné (pont:#912). Candidats : bijection de design (pont:#895), n_1 + n_2 >= 8 + a (pont:#918), égalités n_C(z) = c/6 (pont:#922).
- **H46-c1** ⇒ pas de droite c = 1 (K12) : à prouver comme une rigidité (« aucun autre vecteur propre 3 que les vecteurs de composantes », pont:#954).
- **(B')** ⇒ toute droite spéciale (K14) : bloquée sans E3, C2a, C2b, RL (pont:#961).
- **Familles 7, 9, 19** (branche min c = 4) et toute la **branche min c <= 3** : générateur de gabarits à étendre (pont:#950).
- **Coexistence des 4 blocs cassés de G18** autour d'un sommet, par zéro-extension des noyaux (pont:#876).
- **Borne inférieure sur P** : il faudrait une majoration nouvelle de la norme du tenseur cubique (pont:#851) ; ou une borne inférieure sur Σ‖E‖² (pont:#768) ; (P) seule donne P >= 231, insuffisant.
- **G1''** : test complet (B&B SDP ou réduction analytique) ; une PSD de ν 14 avec M_0 sans {4,5} réfuterait H-MATCH (pont:#805, #818).

### 10.4 Méthodes transférables (analogies, pas transpositions)

- **Valeurs propres rationnelles non entières** (pont:#749) : une saturation PSD forcerait Γq = -(16/5)q ou -(8/3)q, impossible pour Γ entière. Les constantes 48, 40, 15 sont propres à (99,14,1,2). À 243 (valeurs propres 4 et -5), il faut recalculer les dénominateurs ; la méthode ne vaut que si la valeur forcée n'est pas entière.
- **Parité binaire** (pont:#838, #840, #846) : Γn = 3n est impossible quand chaque sommet extérieur a un nombre pair de voisins ; d'où la coupe plate 48. Le « 6 voisins = 1 + 5 » est propre à Conway (pont:#949 : à 243 la parité l'interdit autrement). À recalculer pour d'autres degrés.
- **Trace du produit de deux PSD** (pont:#767) : inégalité sommable de second moment. Elle est transférable à toute paire de compressions forcées (LAB suggère les vecteurs impairs, pont:#768), mais elle a été trop lâche ici.
- **Réduction de Schur des racines extérieures** (pont:#880) : E_T, E_U >= 0 remplacent T, U PSD et le Schur 10 termine là où la recherche naïve échoue. Analogie pour tout germe dont les étoiles centrales sont fixées ; la taille 10 dépend de k.
- **Comptes globaux du 84 avant les arêtes entre nouveaux sommets** (pont:#891) : c'est ce qui ferme le cœur 30, réutilisable pour d'autres cœurs. Le module accepte root_count 14, 4 ou 22 (pont:#892), donc il s'étalonne aussi sur rook9 et srg(243).
- **DISC** (pont:#886) : classe de carrés de det(8T_I) pour tout germe de rang plein. L'analogue à 243 passe par p = 3 au lieu de 7. Mécanisme de grille de classe 10 (pont:#887).
- **Rang modulo 7 et blocs cyclotomiques Z[ζ5]** (pont:#777, #822, #829, #832) : exclusion de familles locales par rang_F7 >= 29 > 28. Transférable à toute famille locale à symétrie cyclique ; dépend de la borne globale L22 propre à Conway.
- **Énumération SAT par classe de noyau** (pont:#790, #799) et **KHOMOG** (pont:#801) : énumérer toutes les structures d'un noyau donné. Transférable, mais biaisé par les lignées d'origine (pont:#841).
- **Détection de symétries cachées ou fausses h·p** (pont:#805) et **lemme d'asymétrie dimensionnel** (pont:#835).
- **Certificat entier de λ_min < -4** (pont:#872) : U(M) <= 4I + Γ. Valable pour tout sous-graphe candidat (c'est l'entrelacement ; λ_min >= -5 à 243).
- **Rigidité des rematchings purs** (pont:#878) : P'v = -v sur W. Transférable à toute étoile de tout germe.
- **Théorème de circulation** (pont:#804) : solvabilité des signes par parité des canaux croisés, sur les composantes ne contenant pas l'autre droite (termes O exclus).
- **Calibration positive obligatoire** (pont:#890, #912, #916) : tout UNSAT ou UNKNOWN doit être étalonné sur de vrais srg(243) (SAT à 4, 5, 6 étoiles). Un encodage défectueux a produit une fausse « barrière » (pont:#916). Lien avec le bug OR-Tools du 18/10 (L05-179), hors lot.
- **Résonance k - 14** (pont:#922) : identité de variance commune à la famille. À 99 elle force l'équilibre exact, à 243 elle laisse une variance (coefficient 8).
- **Entrelacement H46** (pont:#952) : tout sous-graphe induit dont la taille force λ_2 = 3 exactement donne une condition de codimension 1 (36 conditions par droite c = 1). Transférable à d'autres tailles et multiplicités (à 243 : spectre 22, 4^132, -5^110).
- **E3 et ses rotations** (pont:#957, #958, #963) : vecteurs propres -4 de norme 14 (designs co-Heawood) et interdiction des P4 dans les rectangles. Pour 243, l'analogue passerait par des vecteurs -5, avec un design et des normes différents (non calculé).
- **Quotient des composantes à une racine** (pont:#940) : 2^21 graphes, gabarits, Gram R variable. Il dégénère à c = 1 (K7, pont:#963), donc il n'est pas transposable tel quel à la branche c <= 3.
- **Normalisation par budget de racine** (pont:#942) : P <= 852 ⇒ une racine de Σt <= 51 ; même principe pour 3P + 4G <= 2772 (18/10, hors lot).

### 10.5 Combinaisons candidates (à soumettre à la vérification adverse)

1. **K4 × données Q20.** rang F >= 12 hors grille exclurait Conway, et ~7 444 côtés sans grille vérifient corank(Q) <= 7. Un théorème uniforme suffit (pas de calcul de plus). Par L11e-127, il suffit d'ODD-PURE et de rang Z >= c - 1 ; le lemme impair de LAB (L11e-128) donne déjà ODDCONST quand ιx ∈ ker. Point faible : la marge d'ODD-PURE n'est pas uniforme (L11e-130).
2. **K7 (R7-NG) × G9 (L11e-024) × L22.** Conway exige z + b + σ >= 2 à chaque paire, avec z = δ (multiplicité de -4 sur les 40 extérieurs, pont:#761, #947). Sans grille, b = 0 sur toutes les données, mais ce n'est qu'une observation (pont:#947). Prouver « b = 0, δ <= 1 et σ = 0 pour une paire sans grille » exclurait Conway (N2 garantit une telle paire en chaque sommet). Point faible : à 243 le recollement σ est le mécanisme normal aux paires sans grille (pont:#949).
3. **K3 (NG7) × L11e-094 (clôture).** Garder 4 grilles de chaque côté interdit NG7 dans la classe c55 ; il faut étendre cela aux classes à min t <= 7.
4. **K12 (H46-c1) × L11e-136.** Toutes les structures positives c = 1 connues sont tuées par les formes tournées d'E3. Une preuve « c = 1 + positivité ⇒ rectangle tourné à 3 arêtes » fermerait (B') pour c = 1. Point faible : 17 structures sans lemme (non positives).
5. **K10/K11 × L11e-114 (bijection de design) × L11e-123 (n_1 + n_2 >= 8 + a) × L11e-125 (D_k > 0 seulement à 99).** Ce sont trois contraintes de comptage propres à k = 14, à combiner dans R8. Aucune n'est contradictoire seule.
6. **K9 (rang 37) × (K22) × données 7-adiques.** Les grilles de rang_Q 30 descendent jusqu'à rang_F7 25 (5 chutes) ; r = 37 en exige 8 - δ. Une borne « au plus 7 - δ chutes sous PSD » exclurait r = 37 (à croiser avec la route finie du rang 37, hors lot).
7. **K23 (min c >= 4 fermé) × branche c <= 3 × K12/K14.** Si c = 1 est exclu (H46-c1 ou (B')), il reste c ∈ {2, 3} pour la droite minimale. À croiser avec les lots du 18-19/10 (registre c3).



<!-- ===== L11f_pont.md:381-467 ===== -->

## Matériaux pour la recombinaison

### 1. Énoncés conditionnels (« si X, alors exclusion »)

| Si X… | …alors | Statut de l'implication | Statut de X | Source |
|---|---|---|---|---|
| min global c(L) ≥ 4 | contradiction (tout Conway a une droite c ≤ 3) | S (CP-SAT, sans certificat portable) | — | pont:#1050 (L11f-054) |
| plafond P ≤ 791 (racine de s minimal, branche c ≥ 4) | gabarit 7 fermé comme racine minimale ; P ≤ 593 ferme aussi 9 | P (arithmétique) | O ; le plafond démontré est 852 | pont:#1017, #1019 (L11f-034) |
| la racine x minimise 9s + 8g et g(x) = 12, s(x) ≥ 48 | impossible (score ≥ 528 > 504) : 7 exclu | C | — | pont:#1018 (L11f-035) |
| carré de blocs-paires, exactement 2 grilles parmi les 3 rectangles de T, et H_F = H_D (D disjoint) forcée par C h = 0 | gabarit exclu (e_F ≥ 4 contre E3) | P (preuve manuscrite, non relue) | détecté sur 240 gabarits c3 et sur c12_364 | pont:#1135, #1137 (L11f-087) |
| aucune marche fermée de Ĵ à signes alternés ne passe par la non-grille q | contradiction (e(q) = 4) | P | testé par BFS : 51,1 % des classes c = 1 | pont:#1086 (L11f-070) |
| le graphe des grilles à une racine contient C4 ⊔ C3 | les deux diagonales du C4 sont des grilles (K4 ⊔ C3) | E (dépend de E3 et du calcul de 5602) | — | pont:#1172 (L11f-096) |
| le graphe des grilles contient K4 sur X et deux arêtes du triangle complémentaire | la troisième est une grille | P (LAB, non relu) | — | pont:#1181 (L11f-099) |
| familles K3 et 2K2 fermées, H01 = −H02 ≠ 0, Q12 grille | les grilles sur les 4 autres racines forment une étoile | P | K3 : E ; 2K2 : E (RUP/DRAT sur les résidus, réserve sur les coupes) | pont:#1247 (L11f-111) |
| famille P3 fermée | K3 fermée, et 821 ouverts retirés au 19/10 00:19 | P (inclusion des hypothèses) | O (production inachevée) | pont:#1190, #1207 (L11f-107) |
| K3 et 2K2 fermées | registre 1 163 → 537 ; avec P3 : 250 | H (projection) | réalisé pour K3 et 2K2 | pont:#1224 |
| P3NB et K2BC tombent | 45 ouverts ; avec P3 et 2K2N : 32 ; plus tard 40 / 32 / 30 | H (projection) | P3NB : E ; K2BC : E (relecture en cours) | pont:#1259, #1263, #1268, #1269 |
| H_A = −H_B pour deux rectangles disjoints (les 3 racines restantes deux à deux en grilles), sous E3 | e(A) = e(B) = 2, R_AA = R_BB = 4, R_AB = −4 | P | — | pont:#1158, #1160 (L11f-095) |
| H_P = H_Q pour deux rectangles disjoints non-grilles, sous E3 | deux couplages parfaits sans arête entre eux (4K2) ; h ternaire ou un seul −2 | P | situation de 9179, 9912, 9966, 9387, 9883 | pont:#1272, #1274 (L11f-120) |
| 2K2N, S = {0,1,2}, et E(Q12) ≤ 3 (fermeture 2K2) | E(C) ∈ {28, 32, 36, 40} pour C = Q12 + Q35 + Q36 + Q45 + Q46 | P | E(Q12) ≤ 3 : conséquence de la fermeture 2K2 | pont:#1260, #1262 (L11f-114) |
| 5602 : R25,25 = 8 et R04,25 + R16,25 ≤ −1 | vᵀRv ≥ 104 pour v = 11(e04 + e16) + e25 + 7e35 | P (spécifique au gabarit) | — | pont:#1155 (L11f-093) |
| 5602 : le bloc principal S 6 × 6 de (04,06,14,16,25,36) est la sous-matrice de R | aucune complétion (interdit) | P / E | — | pont:#1152 (L11f-093) |
| sous c ≥ 3 GLOBAL | N(L) en 3 bins non vides de tailles 6h (h = 1..4), équilibrés, sans arêtes entre bins | P | branche (A) jamais exploitée dans le pont | pont:#1035 (L11f-047) |
| L est dans 6 grilles | Spec B = {8, 3^18, (−2)^6, (−1)^10, 1^12, (−4)^13} et 13 vecteurs propres −4 de Conway portés par D_L | P (redécouverte) | — | pont:#1138-#1141 (L11f-088) |
| « aucune droite dans six grilles » démontré | 7 des 19 sans paire tomberaient (d'après L08-126, hors de ce lot) | — | O | L08-126, L08-138, L08-141 |

### 2. Bornes quantitatives

| Objet | Inégalité ou valeur | Statut | Source |
|---|---|---|---|
| P (prismes induits) | P ≤ 852 (dual 11088/13 ; max PL d'ordre 9 = 852,923) | C | pont:#1012, #1020 |
| P, G (prismes, grilles) | 3P + 4G ≤ 2772, universel | C | pont:#1018, #1020 |
| sous c ≥ 4 | G ≥ 77, P ≤ 821 ; P ≥ 462 ; avec front 76 : P ≤ 816, G ≥ 81, P ≥ 594 ; après 9 : 9s + 8g ≥ 440 partout, 3P + 4G ≥ 2420, P ≥ 660 | P (conditionnelles) | pont:#1017-#1019, #1047 |
| racine pondérée | ∃ x : 9s(x) + 8g(x) ≤ 504 (Σ = 18(3P + 4G)) | C | pont:#1018 |
| racine de s minimal, gabarits 7/9/19 | g = 12/9/10, s ≥ 48/36/40, P ≥ 792/594/660 | P | pont:#1019 |
| colonne H_F (e arêtes, a = #(−3), b = #(−2)) | e + a ≤ 2 ; 2e + 2a + b ≤ 8 ; 5e + 5a + b ≤ 11 ; 11e + 12a + 2b ≤ 24 ; à e = 0 : b + 6a ≤ 8 | P | pont:#1111, #1121 |
| norme de h_Q / de δ | 7(8 − 2e) / 56 − 14e ; (Σ_S h)² ≤ q(8 − 2e) | P | pont:#967, #979, #983 |
| signature h_w | h_wᵀ R⁺ h_w ≤ 5/2 | P (vérifiée à la main) | pont:#1059, #1153 |
| Gram R | Σ_q R_pq² ≤ 28 R_pp ; R_ii = 8 − 2e ∈ {4,6,8} sous E3 ; Σ arêtes internes des 21 rectangles = 84 − tr(R)/2 | P | pont:#1011, #1048, #1097 |
| rectangle Q | Σ_w C(z_w,2) + e = 8 ; Σ z = 48 ; Σ_share z = 16 − 4e ; moments mixtes 24/32 | P | pont:#1068 |
| D_L (toute droite) | Γ[D_L] 8-régulier, exactement 32 − τ_L triangles ; m_B(3) ≥ 16 ; 12 − t(T_r) arêtes croisées hors côtés | P | pont:#1133, #1138, #1140 |
| noyau signé | 2K2N : E(C) = 28 + 4E(Q12) ; P3NB : 24 + 4E(Q12) ; K2BC : 36 + 4E(Q12) (S = 012), 24 + E(Q01) + 4E(Q03) (S = 013), 16 + 4E(A) (S345/S456) | P | pont:#1260, #1262, #1265, #1267 |
| cœurs sans paire | taille minimale 36 − 4t(S) : 8 (9179, 9912, 9966), 12 (13 gabarits), 16 (4 gabarits) | P | pont:#1270, #1271 |
| gabarits c_min = 3 | 510 926 passent les filtres, 10 052 ouverts après Gram ; sans budget 510 946 / 10 069 | E | pont:#997, #1012 |
| couplages d'étoile | c3 : 105/45/27 ; c2 : 945/315/225 ; c1 : 10 395 ; 10 052 gabarits → 106 852 ; orbites de flips → 40 297 ; c_min = 2 : 119 582 gabarits → 1 673 872 | E | pont:#998, #1002, #1005, #1027 |
| recensements c ≤ 2 | Knuth : c = 2 ≈ 2,5·10¹⁰ étiquetés (≈ 5·10⁶ à S7 près), c = 1 ≈ 10¹⁰ ; C++ c_min = 2 k = 12..4 : 0, 6, 59, 609, 4 892, 32 212, 170 144, 732 827, 2 502 807 | H / E | pont:#1010, #1029 |
| c = 1 | 4 708 882 classes S7 (k ≥ 1) ; FG en tue 2 406 345 ; reste ≈ 160 000 (#1091), puis 178 311 (#1148) | E / S | pont:#1086, #1091, #1148 |
| c = 2 | 213 M puis 338,7 M lignes ; 46,6 M survivantes (13,7 %) ; survie par dimension 4..10 : 1, 5, 25, 61, 86, 96, 100 % | E | pont:#1091, #1148 |
| registre c = 3 | 1 713 → 1 674 → 1 636 → 1 591 → 1 531 → 1 374 → 1 285 → 1 187 → 1 163 → 902 → 537 → 435 → 97 ouverts | S / E / C mêlés | pont:#1086-#1273 |
| ouverts c = 3 par dimension (19/10) | 7 : 4/4 ; 6 : 223/240 ; 5 : 894/4 246 ; 4 : 159/4 738 ; ≤ 3 : 5/802 | E | pont:#1142 |
| couvertures de Gram | médiane 4 / 70 / 34 688 (dim 4 / 5 / 6), max 452 475 ; 1 014 couvertures UNKNOWN = 7 406 294 Gram | E | pont:#1093, #1148 |
| \|Aut\| des gabarits ouverts | 1 (931), 2 (287), 4 (90), 8 (31), quelques 24, 48, 72, 144, 240 ; 10006 : 72, 44 292 Gram → 908 orbites | E | pont:#1126 |
| 5602 | 304 cœurs (7 orbites) → 80 ; 1 328 bords ; 3 bords partiels ; 58 réalisations à 36 sommets | E | pont:#1158-#1171 |
| familles fermées | (2,3) : 5 312 positions ; K3U : 2 742 342 bords, 322 RUP ; 2K2 : ≈ 844 000 raccordements, 7 résidus ; P3NB : 137 454 bords ; K2BC : 1 261 bords, 301 936 raccordements | E / C | pont:#1186, #1237, #1238, #1259, #1269 |
| boule à 33 sommets (7/9) | 24³ = 13 824 configurations, 59 orbites | E | pont:#987 |
| triplets X24 | exactement 816 ensembles de 24 triplets, 34 orbites | E | pont:#1206 |
| coûts | AWS v1 ≈ 243 h-tâches, ≈ 2 $ ; pass c3 complète ≈ 6 500 h-cœur ; v2 nominal 4 232 CPU·h ; crédits ≈ 105 $ (#981), ≈ 65 $ (#1084) | H | pont:#985, #990, #1028 |

### 3. Lemmes ouverts et étapes manquantes, avec ce qu'ils donneraient

- **Vérification indépendante des 76 exclusions c4** et **certificat portable** de la fermeture c ≥ 4 (#1023, #1050). Cela ferait passer « tout Conway a une droite c ≤ 3 » de S à un niveau certifié.
- **Revérification du front 0306** (verdicts AWS v1 et pilotes d'avant le bug). La fermeture c ≥ 4 en dépend (#1009, #1011).
- **Relecture indépendante de PREUVE_COUPES_CONTINUATION** (#1256). Elle consoliderait 2K2 (4 cas sur 7).
- **Contrôle de bout en bout du probe** (#1146). Il consoliderait toutes les exclusions P3E, P4E et couche 1/2.
- **Borne de rang ou de dimension** excluant les dimensions de noyau 6 et 7 (#1142, #1143). Elle viserait 227 gabarits.
- **Lemme pour les composantes 18 du type (3,1,1,1)** (#1028). Il fermerait 34,8 % des tâches de l'étoile complète.
- **Lemme du carré pour les blocs de taille 3** (#1136). Il viserait 10006 et les gabarits sans paire.
- **Argument sans Gram au niveau du gabarit** (front A, #1106, #1108). Il viserait les 245 couvertures de plus de 3 000 Gram, puis c ≤ 2.
- **Argument nouveau pour c ≤ 2** (#1029, #1148). Sans lui, les recensements sont infaisables.
- **Fin de la production P3** : elle retirerait les 7 « dans P3 » du registre final (L08-126).
- **Mode de base « cœur seul + Y »** pour les 10 « autres » (#1276).
- **E3 dans le PL d'ordre 10** (#1020). Il pourrait baisser le plafond P, donc le budget de racine.

### 4. Méthodes transférables (analogies, avec les différences)

- **« Somme des maxima locaux < moment global exigé »** (#1062, 5128 et 4192). Transférable aux plans de comptage sans Gram de c ≤ 2. Différence : à c3 la Gram R est fixée par la couverture ; sans Gram, les moments deviennent des comptes z et l'assemblage doit passer par la réalisation binaire (témoin agrégé de 8650).
- **Comptes positifs z_w et moments de voisins** (#1068). Valables pour tout srg(v,k,1,2) et tout c. Différence : les constantes changent avec k ; pour srg(243,22,1,2), r = 11 au lieu de 7, et la domination parfaite des grilles n'y vaut pas.
- **Isoler une seule colonne par CP, puis écrire la preuve à la main** (H46 pour 364, #1135). Méthode générale d'ablation. Différence : elle n'a marché que pour un cas à six blocs-paires ; les gros blocs n'ont pas de carré.
- **Réduction par automorphismes du gabarit** (#1126). Analogue, sur les droites, de la réduction par lettres mates (#1027) et du transport exact de certificats par permutations de racines et de lettres (#1241). Différence : sur les droites, elle n'est valide que si l'on vérifie que J et les partitions sont préservés ; la réduction par lettres n'est valide que pour complete_star (pas pour matching_global, normalisé).
- **Blocs principaux interdits** (#1152) comme « no-good » hiérarchique sur la Gram. Transférable aux couvertures géantes de dimension 6. Différence : le bloc 6 × 6 de 5602 vaut sans équations de composantes, le bloc 4 × 4 non.
- **Lemme du noyau signé n_B − n_A** (#1260). Valable pour tout sous-ensemble S de racines et tout srg(v,k,1,2) (r est le nombre de droites) ; il s'applique aux gabarits sans paire (#1270). Différence : sur 243, les constantes et les degrés changent ; le contrôle positif a été fait avec r = 11.
- **Export CNF et vérification DRAT/RUP** des verdicts CP-SAT (#1026, #1034). Transférable à toute fermeture S, notamment c ≥ 4. Différence : il faut une CNF équivalente (upper-only, tables) ; l'export PySAT sous Windows a trois pièges (#1203, #1208, #1227).
- **Contrôle positif d'un encodeur sur un vrai SRG** : srg(243,22,1,2) (BvLS, gamma3, twin243) ou rook9, Clebsch16 et SRG9. C'est ce qui a démasqué le bug de LAB (#1076). Différence : un contrôle sur 243 ne vaut que pour les contraintes génériques (C2, quotas) ; les faits propres à Conway (E3, domination, constantes 5/2) se vérifient à part.
- **Certificats de census d'ordre 9** (P ≤ 852, 3P + 4G ≤ 2772), transférables à d'autres comptes (G, P, motifs). Différence : E3 n'apporte rien à l'ordre 9 (#1020) ; l'ordre 10 n'est pas fini.
- **Énumération finie par niveaux** (5602 : 8 → 20 → 36 → frontière ; (2,3) : 5 312 positions). Transférable aux familles à paire opposée (K3, 2K2, P3). Différence : les cœurs « touchants » (2-réguliers C8/2C4) n'ont pas les égalités C2 du cœur cubique de 5602 (#1176, #1179).
- **Équidistribution de la route C de C2** : LAB rappelle que pour c ≤ 2 « il faudra un argument nouveau, pas l'étoile complète » (#1029). La route finie de C2 n'est pas transposable telle quelle : le nombre de gabarits c ≤ 2 est de l'ordre de 10¹⁰.

