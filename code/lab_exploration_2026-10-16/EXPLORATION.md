# Branche exploratoire (LAB, à partir du 16/10/2026 vers 17:05 UTC)

Consigne de Dilan : phase exploratoire, dans une branche séparée. On part du principe que le graphe n'existe pas, et on
cherche la contradiction avec tous nos résultats, en osant des idées risquées mais cohérentes. Branche git :
`lab/exploration-2026-10-16` (dépôt privé conway99-c1). Le dossier principal (`work/REVUE_GLOBALE_2026-10-16.md`) reste la
version sobre.

Règle unique : une contradiction annoncée doit être vérifiable (calcul exact ou preuve écrite). Tout le reste est permis :
conjectures, raccourcis, paris.

## Cible principale : R8

Énoncé :
- R8 = base à quatre étoiles (lettres 0..3 exactes) + les huit labels {4,u} (u = 6..13), la lettre 4 seulement bornée,
  C1' et caps C2.
- R8 IMPOSSIBLE ⇒ aucun srg(99,14,1,2), symétrique ou non : R8 est une relaxation de la cinquième étoile, présente en
  tout sommet.
- Avec 7 labels la réponse est oui ; les 6 témoins refusent tous le 8ᵉ.

### Reformulation exacte (prouvée) : R8 = un problème de décomposition
- Avec X complet, tout est serré : chaque label y de la base a exactement c(y,4) voisins dans L_4 = X ∪ C4.
- Le résidu R(y) = c(y,4) − |N(y) ∩ C4| ne dépend QUE de la base.
- Pour chaque étoile r ∈ {0,1,2,3}, Σ_{y ∈ L_r} R(y) = 16 = 8 labels × 2. Chaque x ∈ X doit prendre exactement 2 labels
  de L_r, et une paire non M_r, non déjà couverte par un label lointain de la base.
- Donc, pour chaque r, le résidu sur L_r se décompose en 8 paires distinctes : un b-couplage H_r de degrés R sur L_r. Ce
  sont 4 b-couplages, étiquetés par les 8 labels de X, avec une compatibilité croisée (deux labels de X partagent au plus
  un voisin de base, aucun s'ils sont adjacents ; caps C2 de x contre chaque label de base).
- C'est une structure de type « classes parallèles orthogonales » (comme les carrés latins orthogonaux) : le genre
  d'objet où vivent les obstructions de Bruck-Ryser.

### Pistes risquées (ordre d'attaque)
1. **Hall dans une étoile.** Pari : le b-couplage H_r échoue déjà dans une étoile pour toute base. Test immédiat sur les
   témoins et les bases aléatoires, comparé à K = 22.
2. **Orthogonalité.** Si chaque H_r existe, l'obstruction vient de l'étiquetage commun : chercher un invariant de
   comptage ou de parité, comme pour les MOLS.
3. **DISC-35.** Pari : tout bloc admissible PSD de rang 30 a 3 et 5 à exposant impair dans sa classe (645 germes sur 645).
   Cela tuerait Conway par DISC. Il faut une raison structurelle (3-adique) ou un contre-exemple.
4. **Toutes les cinquièmes étoiles à la fois.** Les 10 lettres hors de la base jouent chacune le rôle de la lettre 4 :
   sommer les 10 structures R8 serrées d'une même base.

## Journal

### 16/10 environ 17:10-17:25 UTC
- Pari 1 (Hall dans une étoile) RÉFUTÉ (`hall_star.py`) : pour 6 témoins R7, 8 bases aléatoires (K = 14) et 5 bases
  (K = 22), chaque étoile admet le b-couplage du résidu. Seule différence : 22 à 40 paires admissibles pour 8 (K = 14),
  contre 103 à 144 pour 16 (K = 22). L'obstruction est inter-étoiles.
- Pari 2 (graphe de partage) RÉFUTÉ (`sharing.py`) : β = #{y : R(y) = 2} vaut 16 à 21 (K = 14) et 46 à 50 (K = 22),
  sous la borne C(|X|,2) − a.
- Apport de Codex (vérifié dans le principe) : pour une composante C de G[N(l)],
  Σ_{z lointain} (n_C(z) − 2c/(k−2))² = (k − 14)·c·(1 − c/(3(k−2))). La résonance θ = 3 = degré cubique est propre à
  k = 14 dans la famille. Grille 3×3 : 9(k − 4) = v − 9 ⟺ k = 14, donc chaque sommet extérieur a exactement 1 voisin
  dans la grille, et 1_G − (1/11)·1 est un vecteur propre de valeur 3.
- PROUVÉ (principe de résonance) : si y est de somme nulle, yᵀAy ≤ 3‖y‖². Donc deux sous-graphes induits disjoints et
  sans arête entre eux ne peuvent pas avoir tous deux un rayon spectral > 3, et s'ils sont tous deux cubiques,
  n_{C1}(z)/|C1| = n_{C2}(z)/|C2| pour tout z extérieur.
- Test (`psd_witness.py`) : les témoins R7 ont λ_min(T_51) ≈ −1 et un rang de 39-40. Ils sont loin de la positivité
  (T ⪰ 0, rang ≤ 30, valeurs propres ≤ 7).
- Pari suivant, COLONNE : aucun bloc à quatre étoiles PSD de rang ≤ 30 n'admet de colonne extérieure (645 germes sur 645
  à domaine vide). Mécanisme : les 14 vecteurs q du noyau imposent 8·Σ_{y ∈ N(z) ∩ S} q_y = −Σ_y q_y (3|y ∩ z| + m_yz − 2)
  à chaque colonne z.

### 16/10 environ 17:25-17:35 UTC
- Formes de Smith (`snf_germ.py`, exact) des deux germes de rang 30 :
  - urep100 : v3 = [1], v5 = [1, 2, 2], classe 2·3·5 ;
  - HB : v3 = [1], v5 = [1], v7 = [1], classe 2·3·5·7.
  La partie 3 est exactement Z/3.
- Pari 3 (DISC-35 par vecteurs universels) RÉFUTÉ (`zp_vectors.py`). Les vecteurs universels de ker(8T mod p) portés par
  la base sont :
  - mod 3 : 1_{L_1} − 1_{L_0} et 1_{L_3} − 1_{L_2} ;
  - mod 5 : 1_{(L_2 ∪ L_3) \ K} − 1_{(L_0 ∪ L_1) \ K} ;
  c'est-à-dire les vecteurs triviaux du noyau, toujours présents. Les facteurs 3 et 5 des germes dépendent donc de Γ (de
  leurs familles), pas d'une loi universelle.
- Reformulation PROUVÉE (principe d'extension A7 : ‖Bᵀw‖² = (3−α)(4+α)‖w‖²). Soit U = {v} ∪ 14 lettres ∪ base S (59
  sommets).
  - Tout vecteur propre de A_UU de valeur 3 et orthogonal à 1 s'étend par zéro en un vecteur propre de A.
  - Donc ν(T_SS) = dim(E_3(A_UU) ∩ 1^⊥) ≥ 14.
  - Pour chaque label extérieur z, 1_{N(z) ∩ U} est orthogonal à E_3(A_UU) (« aucune fuite »).
  Les 14 équations de colonne sont exactement cela. Forme nette du pari COLONNE : pour U admissible avec A_UU ≤ 3 sur
  1^⊥ et mult_3 ≥ 14, aucun voisinage de label extérieur (2 lettres de Z + 8 incidences de base) n'est orthogonal à E_3.
- Comptages grossiers essayés sans succès :
  - par paire de droites extérieures, demande 16 contre capacité 28 ;
  - résonance appliquée à H1 = {v} ∪ lettres de A (rayon 2,56) et H2 = ZZ (40 labels, non adjacents à H1) : on obtient
    seulement ρ(ZZ) ≤ 6,5 environ, alors que le degré moyen est environ 4,9.

### 16/10 environ 17:35-17:55 UTC
- Synthèse de Codex (commit 51460e5) : registre de 48 entrées (9U + 7A + 15C + 10S + 7F). Le même facteur
  k − 14 = (r − 3)(3 − s) est derrière :
  - l'équilibre des voisinages de droites (variance nulle seulement pour 99) ;
  - la couverture des grilles : (k − 4)(k − 14)/2 sommets sans voisin, soit 0 pour 99 ;
  - le débordement de la cinquième étoile : D_k = 8 + a − (k − 14)(k − 7)/2, soit +8 seulement pour 99.
  Ces rigidités sont liées, pas indépendantes. Il n'y a aucun argument général contre l'asymétrie.
- `line_components.py` :
  - témoins combinatoires (R7, base à quatre étoiles) : G[N(l0)] et G[N(l1)] connexes (36) ;
  - germes PSD de rang 30 : urep100 [6, 6, 6, 6, 12] pour les deux droites, HB [6, 6, 6, 6, 12] et [6, 12, 18] ;
    équilibre exact, 0 violation.
  La nullité 14 semble exiger des droites très spéciales (grilles), et la cinquième étoile l'inverse.
- PROUVÉ (entrelacement de Cauchy avec le spectre 14, 3^54, (−4)^44) : tout sous-graphe induit sur m sommets vérifie
  λ_i ≥ 3 pour i ≤ m − 44, donc la valeur propre 3 a une multiplicité ≥ m − 45 dès que m ≥ 45 (λ_2 ≤ 3). Pour U = racine,
  lettres et base (59 sommets), cela donne λ_2 = ... = λ_15 = 3 : c'est ν ≥ 14. Pour la cinquième étoile (67 sommets),
  multiplicité ≥ 22.
- Pari 5 (plus faible que N9-NG, suffisant pour une contrainte énorme) : si c(l) = c(m) = 1, alors ν ≤ 13. Conséquence :
  chaque sommet a au plus une droite non spéciale. Avec N9-NG complet (ν ≤ 9 + min c), on aurait ≥ 4 grilles par droite,
  contradiction avec P ≤ 852 (route vérifiée par Codex le 15/10).
- Reformulation PROUVÉE de N9-NG.
  - Soit E = ker T_S, E_X = E ∩ R^{L_0 ∪ L_1} (dimension 1 + c(l), par positivité) et E_X' = E ∩ R^{L_2 ∪ L_3}
    (dimension 1 + c(m)).
  - E_X ∩ E_X' = E ∩ R^C = 0 (un vecteur porté par les coins a une énergie ≥ 8).
  - Donc ν = 2 + c(l) + c(m) + μ, où μ = dim E/(E_X ⊕ E_X') compte les directions « mixtes ».
  - N9-NG ⟺ μ ≤ 7 − max(c(l), c(m)) = 1 + (6 − max c). Or 6 − c(l) est le nombre de fusions dans la partition des
    6 autres droites par v induite par les composantes de G[N(l)] (composante de taille 6m ↔ m droites).
  - Pari 6 : chaque fusion de droites porte au plus une direction mixte, plus une. C'est faux avec une grille sur
    (l, m), car les objets c22 ont μ = 8.
  - Données (THREE_RESULTS §6) : 97 structures PSD sans grille vérifient la borne, avec égalité dans 56 cas, de
    (ν, c) = (10, (1,1)) à (14, (5,5)).

### 16/10 environ 17:55-18:05 UTC : réduction de Conway à UN énoncé local net (avec Codex)
- Matrice de résonance (`q_corank.py`). Avec l = {v,0,1}, N(l) cubique (36), Y = les 20 labels de L_2 ∪ L_3 évitant 0, 1 :
  Q = 3I − A_YY − A_YN (3I − A_NN)^+ A_NY, de taille 20 × 20.
- Codex (bba12ce, preuve écrite ; message 926 et suivant) : V = 0, Q·1 = −(5/3)·1, F = Q + J/12 PSD avec F1 = 0, et
  EXACTEMENT ν = c(l) + 2 + corank(Q), c'est-à-dire rank T = 23 − c(l) + rank F. F est le complément de Schur de T44 sur
  Y, après élimination de L_0 ∪ L_1.
- Balayage (`q_scan.py`) : 7 018 structures distinctes, 6 122 PSD (2 400 avec grille, 3 722 sans).
  - dim P = corank(Q) + 1 : 12 244 vrais sur 12 244.
  - corank(Q) sur les côtés sans grille : {3: 110, 4: 624, 5: 2977, 6: 2842, 7: 891}, maximum 7.
  - Codex : les grilles de rang 30 vont jusqu'à 10.
- PROUVÉ (entrelacement avec W = N(l) ∪ Y, 56 sommets) : dans un graphe de Conway, mult_3(A_W) ≥ 11. Or
  mult_3(A_W) = (c(l) − 1) + corank(Q) exactement (élimination ; ker Q ⊥ 1). Donc corank(Q) ≥ 12 − c(l).
- CONJECTURE Q7 : pour (l, m) sans grille, du côté où c est minimal, corank(Q) ≤ 7, c'est-à-dire rank(F) ≥ 12.
- Q7 ⟹ pas de graphe de Conway. P ≤ 852 (certificat de Codex) donne une paire sans grille avec c_min ≤ 4, donc
  corank(Q) ≥ 8 : contradiction.
- Prochaine étape : prouver Q7. Il faut trouver pourquoi l'espace des profils (ker Q ⊂ R^20) a dimension ≤ 7 sans grille,
  et pourquoi une grille ajoute 3 dimensions.

### 16/10 environ 18:05-18:30 UTC : Q7 se scinde en deux lois, toutes deux vraies sur les données
- Ventilation (`q_scan.py`), côtés PSD sans grille, (c, corank Q) :
  - c = 1 : corank ≤ 7 (il suffirait de ≤ 10) ;
  - c = 2 : ≤ 7 (il suffirait de ≤ 9) ;
  - c = 3 : ≤ 7 (il suffirait de ≤ 8) ;
  - c = 4 : ≤ 7 (il faut exactement ≤ 7, pas de marge) ;
  - c = 5 : ≤ 7.
  Aucune violation de la borne 11 − c qui tuerait Conway. Avec grille, corank va jusqu'à 11 (c = 2).
- Décomposition (`q_split_scan.py`, environ 7 444 côtés sans grille) :
  - ODDCONST : le rang des parties antisymétriques w_{2s} − w_{3s} vaut toujours exactement 1 (le vecteur trivial
    χ_2 − χ_3) ;
  - SYM6 : le rang des parties symétriques w_{2s} + w_{3s} est ≤ 6, avec toujours corank = 1 + rang symétrique.
  Les grilles CASSENT ODDCONST (rang antisymétrique 2 ou 3, des centaines de cas) : c'est ainsi qu'elles gonflent le
  noyau.
- Donc Q7 ⟸ ODDCONST + SYM6 (sans grille).
- Hypothèse LINE-SUM pour SYM6 RÉFUTÉE (`sym_linesum.py`, 0 sur 16) ; seule la somme totale nulle tient (16 sur 16).
- Identité exacte : f(s) := w_{2s} + w_{3s} = (A_NY w)_s = ((3I − A_NN) x_N)_s pour les lettres s = 4..13, avec
  x_N = (3I − A_NN)^+ A_NY w.
- Pistes de preuve :
  - ODDCONST est la partie ι_m-impaire (permutation formelle 2 ↔ 3 ; voir R5/R6 de N9NG_ATTACK) restreinte à Y. Le lemme
    de signe R5 contrôle déjà l'énergie de (x ± ι_m x)/2 ;
  - SYM6 doit venir de la structure de G_l à travers A_NY.

### 16/10 environ 18:15-18:35 UTC : partage avec Codex, un lemme impair prouvé
- Codex prend SYM6. Avec P f = (f, f) et R g = (g, −g), F devient [[A, C], [Cᵀ, D]] ; Z = A − C D⁺ Cᵀ. Alors
  SYM6 ⟺ rank Z ≥ 3, et rank F = rank D + rank Z. Pour Q7 avec SYM6, il suffit d'avoir rank D = 9 (ODD-PURE : seuls
  les multiples de (1, −1) sont des profils purement impairs). Données de Codex : rank D = 9 partout sans grille ; deux
  traces de Z donnent déjà rang ≥ 3. Deux mécanismes de grille : Z5h_c62 garde ODDCONST et casse SYM6 ; HB/H30_23 casse
  les deux.
- ODDCONST n'est PAS combinatoire (`q_split_nonpsd.py`) : hors PSD, elle échoue sur 12 côtés sans grille (rang
  antisymétrique 2-3). La positivité est indispensable.
- `d_laplacian.py` : D n'est pas un laplacien (termes hors diagonale positifs jusqu'à 1,42 sans grille). Piste fermée.
- LEMME IMPAIR (PROUVÉ). On note ι = (2 3), qui agit sur S par permutation formelle des lettres ; K est ι-invariant.
  - Pour y impair (y_{ιu} = −y_u, donc nul sur les labels fixes Y'), avec δ_a = y_{2a} − y_{3a} pour a ∈ {0,1,4..13}
    (12 indices) :
    E(y) = yᵀTy = (1/4) δᵀ Φ δ, avec Φ = 6I − Aˢ − J/2.
  - Aˢ est le graphe signé 4-régulier sur les 12 indices : arêtes M_2 et M_3 positives, arêtes φ_23 négatives, boucles
    éventuelles −2. On a Aˢ1 = 0 et |Aˢ| ≤ 4 (Gershgorin), donc Φ ≥ 2I sur 1^⊥ et Φ1 = 0.
  - Conséquence : les vecteurs impairs de ker T_S sont les multiples de la partie impaire de χ_2 − χ_3. Si x et ιx sont
    dans ker T_S, alors x₋ = (x − ιx)/2 est dans ker T_S, et le profil impair de x est constant.
  - Cas restant : x ∈ ker T_S avec ιx ∉ ker T_S. On pose Γ = Γˢ + Γᵃ (parties ι-symétrique et antisymétrique) et
    Tˢ = 3I − Γˢ − K. Alors Tˢx₋ = Γᵃx₊, Tˢx₊ = Γᵃx₋, et E(x₋) = E(x₊) = ε = x₋ᵀΓᵃx₊ ≥ |δ⊥|²/2. Pour un profil
    purement impair, x₊ est porté par X = L_0 ∪ L_1. Il faut montrer que ce couplage ne peut pas porter un δ non
    constant.
- Forme « contraction » du cas restant : T ⪰ 0 ⟺ ‖K_ι‖ ≤ 1, avec K_ι = (Tˢ_impair)^{+1/2} Γᵃ (Tˢ_pair)^{+1/2}.
  Un profil purement impair non constant ⟺ valeur singulière 1 de K_ι, avec un vecteur singulier dont le profil est
  non constant. C'est la même structure que la forme contraction de (H-MATCH) du 15/10, qui avait résisté : ODD-PURE est
  une cousine de H-MATCH pour la transposition simple ι_m.
- Complément de Codex (sym6 67ffa75) : avec rank D = 9, Conway exige rank Z ≤ c − 2. Donc :
  - c = 1 est exclu par ODD-PURE seul ;
  - c = 2 demande Z ≠ 0 ;
  - c = 3 demande rank Z ≥ 2 ;
  - c = 4 demande rank Z ≥ 3.
  Z a des termes hors diagonale des deux signes (pas un laplacien). Piste scalaire : (tr Z)² > 2 tr Z² suffit.
- BILAN de la soirée : Conway ⟸ [ODD-PURE (rank D = 9) + rank Z ≥ c − 1 pour c ≤ 4], sur les paires sans grille du
  côté où c est minimal, avec P ≤ 852. Toutes ces conditions tiennent sur 100 % de nos données sans grille.
  Rien n'est prouvé dans le cas général, hors le lemme impair.

### 16/10 19:02 UTC : fin de session
- R8 (8 labels {4,t}) : cadical `--unsat` 2 h avec cassage de symétrie complet, et 2 h sans : TIMEOUT tous les deux.
  kissat via python-sat plante sur ce PC. R8 reste indécis par SAT.
- Codex, suite du secteur impair (sans re-audit) : on décompose T44 en U (20 labels fixes), P (12 pairs), R (12 impairs).
  Alors ODD-PURE ⟺ ker K1 = ker K (avec K = T_UU, K1 = K − C Φ⁺ Cᵀ), et δ = rank K − rank K1 = 9 − rank D. On a
  rank T = 32 − c(l) − δ + rank Z. Sur ses objets sans grille δ = 0 ; sur HB (grille) δ = 1.
- Codex, côté pair : borne d'énergie PROUVÉE à deux étoiles (E ≥ G/5). La perte de rang vient donc du couplage avec les
  20 labels fixes. Impasse notée : « trois directions découplées de N1 ».
- ÉTAT : Conway ⟸ [ODD-PURE + rank Z ≥ c − 1, pour les paires sans grille, côté c minimal ≤ 4] avec P ≤ 852.
  - Prouvé : la réduction (Codex), le lemme impair (LAB), le comptage de dimensions (corank Q ≥ 12 − c).
  - Ouvert : ODD-PURE dans le cas couplé (forme contraction, comme H-MATCH) et les rangs de Z.
  - Données : aucune violation sur 7 444 côtés sans grille.

### 16/10 après la fin de session : marge d'ODD-PURE (`oddpure_margin.py`)
- Calcul : λ_max = plus grande valeur propre généralisée de (CΦ⁺Cᵀ, K) hors de ker K ; ODD-PURE ⟺ λ_max < 1. Côtés
  PSD, les deux orientations.
- δ = 9 − rank D = 0 sur tous les côtés sans grille. Les 872 côtés avec δ > 0 sont des grilles (cohérent avec
  ODDCONST).
- La marge n'est PAS uniforme : λ_max s'étale de 0,5 à 0,99993 (`wmix_h_c44_m4_MIX3_5243.json`, c44), avec 106 côtés
  au-dessus de 0,995.
- Conséquence : aucune borne de contraction uniforme (λ_max ≤ 1 − ε) ne peut prouver ODD-PURE. La preuve doit être
  algébrique ou exacte : montrer qu'une saturation λ = 1 avec un profil impair non constant contredit les comptes
  entiers (C1, C2), et non une inégalité de norme.
- Lecture du cas extrémal : un vecteur y = (u, 0_P, z) du noyau, antisymétrique sur tous les labels échangés, avec
  uᵀKu > 0. Son miroir ιy a l'énergie 4uᵀKu. Si ker T est ι-invariant, le cas est vide (lemme impair).
- Anatomie des quasi-saturations (`near_saturation.py`, `oddpure_anatomy.py`) :
  - les 340 côtés avec λ_max ≥ 0,99 ont un vecteur extrême u exactement impair sous l'autre transposition
    (⟨u, miroir u⟩/⟨u,u⟩ = −1) ; le vecteur y = (u, z) est donc impair sous h = (01)(23), avec u dans (−,+) et z dans
    (+,−) ;
  - le secteur (−,−) de R^44 est 1-dimensionnel, réduit à w_C (les coins) ;
  - dans le cas h-invariant, ODD-PURE se ramène à ODD9-NG (graphe signé quotient sur 22 orbites sans valeur propre 3,
    sans grille ; ODD9 n'a été réfuté que par des grilles le 15/10).
- `oddpure_hsplit.py` : sans symétrie h, λ_max monte aussi jusqu'à 0,990 (b_*.json, lignées asymétriques ; 110 côtés
  ≥ 0,95). Le danger n'est donc pas limité au cas h-invariant ; la preuve doit être exacte dans tous les cas.
