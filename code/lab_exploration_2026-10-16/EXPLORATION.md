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

## 16/10 soir, après la critique de Dilan (« ouvert, ouvert ... il manque une idée, une mesure »)
Diagnostic écrit (message à Dilan) :
1. Tous les murs (H-MATCH, N9-NG, Q7, ODD-PURE + Z, R8) sont le MÊME énoncé dans d'autres coordonnées : un bloc local ne
   porte pas la nullité que le spectre global impose, sauf s'il est plein de grilles. Les réductions sont exactes, donc
   la difficulté est conservée, et les données saturent chaque borne (marge 0).
2. Les lois locales validées sur des populations biaisées cassent l'une après l'autre (ODD9, (A), N9 sur les grilles,
   SUM14, KER-SYM, R7, le 7ᵉ label).
3. Tout ce qui a FERMÉ quelque chose était arithmétique : C3 (mod 3), C2 (réseaux), r ≤ 35 (F7), b = 26..32, c55 (F7),
   Z5-hM (Q(ζ5)/F7), les 645 germes (DISC). Le « mou » ne donne que des reformulations.
MESURE (`f7_rank_scan.py`, exact mod p, 6 122 blocs PSD distincts) :
- sans grille (3 722) : rang_F7(8T_S) ≥ 30 toujours ; pour rang_Q = 30 (46 blocs), rang_F7 = 30, aucune chute ; des
  chutes de 2 seulement à rang_Q ≥ 33 ;
- avec grille : rang_F7 jusqu'à 25 (403 blocs à rang_Q 30), et aussi 26, 27, 28.
- Conway exige rang_F7(8T_S) ≤ k ≤ 28 pour tout bloc principal (G13 de CONWAY_CONSTRAINTS : L4/L22 de Codex, statut P)
  et possède une paire sans grille à chaque sommet (N2 de Codex). Donc :
  (R7-NG) « tout bloc PSD sans grille a rang_F7 ≥ 29 » ⟹ pas de Conway.
  Marge sur les données : 1 (minimum observé 30). Algèbre linéaire sur F7, exacte.
- ANTÉRIORITÉ : le test rang_F7 ≤ 28 faisait partie de NG14 (THREE_RESULTS §5, 15/10), et (R7) sans « NG » avait été
  réfuté par un objet à grille (E7, rang 25). Nouveau ce soir : la séparation systématique grille / sans grille.
- Mécanisme mod 7 : (8T)² = 56·8T ≡ 0 mod 7 globalement, donc (8T_S)² ≡ −(8T)_{SZ}(8T)_{ZS} mod 7 (Z = les 40
  labels extérieurs).
- `f7_kernel_look.py`, bloc à grille n9ng_z5h_SCH_1 (rang_Q 30, rang_F7 25) : 5 directions mod 7 non relevables. Les
  représentants ont des supports de 20-25 labels ; l'un est un vecteur de parité (+1/−1 alterné sur L_1 selon la
  parité de la seconde lettre, −2 sur les labels impairs de L_2, −1 sur L_3). Pas encore de mécanisme lisible.

## 16/10 nuit : la forme lisible de la chute 7-adique (demande de Dilan : « la forme lisible pour comprendre exactement le système »)
Scripts : `f7_classform.py`, `f7_letters.py`, `f7_balanced.py`, `f7_charpoly.py`, `f7_lmin_check.py`, `f7_parity_check.py`,
`f7_tau_check.py`, `build_cache.py` (cache dédoublonné : 486 669 fichiers → 7 023 structures, 6 122 PSD). Tables :
`f7_balanced.log`, `f7_admissible_table.log`. Tout est exact (mod 7 ; rangs rationnels = max des rangs modulo deux
grands premiers, 0 désaccord sur 6 122 blocs).

Énoncés exacts (preuves de quelques lignes) :
- (E1) h « équilibré » (B_S h = 0 : chaque lettre a une somme nulle) ⟹ 8T_S h = 8(3I − Γ_S) h (les termes en B
  s'annulent, Jh = ½ Σ_r (Bh)_r = 0). Donc mod 7, sur les équilibrés, ker_7(8T_S) = ker_7(Γ_S − 3I), qui contient les
  vrais vecteurs propres 3 ET −4 du graphe des labels, puisque 3 ≡ −4 mod 7.
- (E2) 8T_S = 8 × complément de Schur de 3I − A_W, W = {v} ∪ N(v) ∪ S (59 sommets), relativement au bloc 15 × 15 de
  {v} ∪ N(v) (dét = −2^23, inversible sur Z_(7)) : ker_7(8T_S) = vecteurs propres mod 7 de la boule de 59 sommets pour
  la valeur propre 3 ≡ −4.
- (E3) T + U = 7Π (Π = projecteur sur les équilibrés, 7-entier : dét BBᵀ = 24·10^6·12^7) ⟹ T_S ≡ −U_S mod 7. Côté 3
  (noyau de T_S) et côté −4 (noyau de U_S) se confondent mod 7. U_S ≥ 0 ⟺ A_W ≥ −4 (entrelacement côté −4).
- (E4) Dans Conway : T = 7P_U, U = {vecteurs propres −4 nuls sur {v} ∪ N(v)} (dim 30). Alors
  rang_Q(T_S) = 30 − z, z = dim(U ∩ R^Z) (vecteurs propres −4 portés par les 40 labels extérieurs Z) ;
  mult. de la valeur propre 7 de T_S (= 56 pour 8T_S) = b = dim(U ∩ R^S) (vecteurs propres −4 portés par S) ;
  rang_F7(8T_S) = 30 − z − b − σ, σ = recollement 7-adique de la partie oblique.
  La borne F7 (≤ 28) dit EXACTEMENT : z + b + σ ≥ 2 pour chaque sommet et chaque paire de droites.
  Par A + 4I ≥ 0, tout vecteur propre −4 de Γ_S est un vrai vecteur propre −4 du graphe (donc automatiquement équilibré).

Mesure (5 173 blocs avec T_S ≥ 0 ET U_S ≥ 0) :
- grille (1 455) : σ = 0 dans TOUS ; la chute est exactement b ∈ {0, 1, 3, 4, 5} ; rang_Q ≥ 30 (z = 0).
  Compatibles F7 : (rang 30, b = 5) ×403 [famille Z5h] et (rang 31, b = 4) ×60, rien d'autre.
- sans grille (3 718) : b = 0 TOUJOURS ; chute = σ ≤ 3, sporadique ; rang_Q ≥ 30 ; minimum rang_F7 = 30.
- Forme explicite de b en grille : produit de parités h({r,s}) = σ(r)σ(s) sur les 40 labels extérieurs, 0 aux coins,
  σ(mate a) = −σ(a) ; chaque label extérieur a 1 voisin de même signe et 5 de signe opposé (1 − 5 = −4). Il donne la
  dimension 1 de b dans 1 178 blocs ; les autres vecteurs −4 (b = 3, 4, 5) sont « doublement impairs » :
  h_{1s} = −h_{0s}, h_{3s} = −h_{2s}, coins 0 (1 239 des 1 261 blocs à b ≥ 1, toutes positivités confondues).
  Les « vecteurs de classe » 3(e_12 − e_03) + 1_{3,E} − 1_{1,O} du support minimal sont ces vecteurs −4 décalés par un
  vecteur du noyau rationnel (même ombre sur les lettres : `f7_letters.py`).
- σ (sans grille) : un facteur irréductible de degré ~10 du polynôme caractéristique (partie équilibrée) qui a 3 pour
  racine mod 7, ou un facteur de degré 11-28 de charpoly(8T_S) de terme constant divisible par 7 (ex. 7·2^34). Aucune
  structure lisible : arithmétique accidentelle.

Corrections de calibration :
- 945 des 2 400 blocs à grille et 4 sans grille de nos données violent A ≥ −4 (U_S non PSD, λ_min(Γ_S) jusqu'à −4,57) :
  ils n'ont jamais été des candidats. Ils contenaient TOUS les blocs à grille de rang_Q 28-29 et toutes les chutes
  sporadiques en grille. Le tableau du 16/10 soir (`f7_rank_scan.py`) ne filtrait que T_S ≥ 0.
- « chutes de 2 seulement à rang_Q ≥ 33 » (plus haut) : en fait jusqu'à 3 (2 blocs, rang 33 → 30).
- BIAIS : 3 474 des 3 722 blocs sans grille ont τ = (01)(23) comme automorphisme ; 248 seulement sont asymétriques.

Ce que ça dit (honnêtement) :
- Il y a UN seul mécanisme structurel mod 7 : la confluence 3 ≡ −4, visible comme valeur propre 56 de 8T_S (vecteurs
  propres −4 localisés sur S). Il n'apparaît qu'avec une grille.
- Sans grille, R7-NG n'est pas un mécanisme caché : rang_F7 = rang_Q − (accidents). La séparation « ≥ 30 » vient du
  rang rationnel (≥ 30, et ≥ 31 pour c ≤ 4 : c'est Q7) ; R7-NG ≈ Q7 + contrôle des accidents.
- Pour Conway à une paire sans grille (N2) : il faut z + σ ≥ 2 si b = 0 : deux vecteurs propres −4 portés par les 40
  labels lointains Z, ou deux accidents 7-adiques. Cibles nettes : (T1) sans grille ⟹ b = 0 (structurel, à prouver) ;
  (T2) borner z (vecteurs propres −4 portés par Z) ; (T3) σ dans Conway est un recollement GLOBAL (U et U^⊥ en 7, de
  rang k ≤ 28), pas un accident : c'est là que le local ne peut pas conclure seul.

## 16/10 nuit, suite : l'angle global (demande de Dilan : « prends l'angle global »)
1. Formalisation au niveau d'un sommet v (exact) :
   - Γ_v (84 labels) a le spectre 12, 3^40, 0^7, (−2)^6, (−4)^30 (identité srg sur les labels + C1) ; sur les
     équilibrés, (Γ_v − 3)(Γ_v + 4) = 0 ; mod 7, N = Γ_v − 3I vérifie N² = 0 sur ker_7 B et rang_F7(Γ_v − 3I) = 14 + k.
   - Mod 7 sur tout le graphe : radical commun C_0 = (A − 3I)(1^⊥) (autodual, dim 14 + k) ; ker_7(A − 3I)/C_0 =
     Q_3 ⊥ Q_{−4}, de dimensions 40 − k et 30 − k. Le réseau des vecteurs propres −4 entiers a un Gram mod 7 de rang
     30 − k ∈ {2, 4, 6, 8} ; celui des vecteurs propres 3, de rang 40 − k. (Théorie standard du p-rang, pas nouvelle.)
   - Pour un bloc S : rang_F7(8T_S) = rang de la forme discriminante de M_U restreinte à l'image de S, ≤ k.
   VERDICT : la « coexistence » de la dégénérescence 7-adique sur les 21 paires est AUTOMATIQUE (héritée de rang ≤ k
   pour la matrice 84 × 84 du sommet) : pas de contrainte cachée entre paires. Le contenu est entièrement local.
2. Calibration sur les srg(243,22,1,2) CONNUS (`cal243_ball.py`, `cal243_universal.py`, logs `cal243_ball_*.log`) :
   analogue exact (valeurs propres 4 et −5, 4 − (−5) = 9, p = 3), boule à quatre étoiles = 99 sommets, transfert par
   positivité identique. Aux paires SANS grille, dans les trois graphes non-BvLS :
   - n4 = n5 = 4 : seuls les vecteurs propres UNIVERSELS (A + 5I)(e_u − e_w), (A − 4I)(e_u − e_w) vivent sur la boule ;
   - noyau mod 3 de la boule = noyau global restreint = minimum forcé : twin 13 = 13, Γ3 9 = 9, Γ4 20 (forcé 18) ;
   - donc presque tout est du RECOLLEMENT (σ = 5, 1, 12 au-delà des 8 rationnels) ;
   - grilles : noyau local plus gros (14 à 39), b5 = 0 partout (pas de vecteur −5 localisé ; le vecteur de parité de
     Conway exige 6 voisins = 1 + 5, la résonance k = 14 ; à 243 la parité l'interdit).
   LEÇON : dans un vrai graphe, le recollement p-adique est le mécanisme NORMAL aux paires sans grille, et il sature
   exactement la borne globale. L'absence de recollement dans nos blocs Conway vient très probablement de leur mode de
   génération (jamais conditionnés par F7). R7-NG n'est pas une loi structurelle crédible ; ne pas investir dans sa preuve.
3. Ce qui est propre à Conway : la surcharge RATIONNELLE. Chaque boule doit porter ν ≥ 54 − 40 = 14 vrais vecteurs
   propres 3 (4 universels + ≥ 10 non universels), alors qu'à 243 les boules sans grille n'en portent aucun non
   universel (rien n'y est forcé : 132 − 144 < 0). C'est Q7 : sans grille et c ≤ 4, nos données plafonnent à ν ≤ 13.
   => l'angle global renvoie à la surcharge rationnelle aux paires sans grille de petit c (Codex : c = 4, 64/79
   modèles exclus ; LAB : c ≤ 3).

## 16/10 nuit : branche min c ≤ 3, ce qu'elle exige concrètement (`cle3_spectrum.py`, `cle3_spectrum.log`)
- c(l) = nombre de morceaux du graphe cubique induit sur les 36 voisins de la droite l ; morceau de 6 = prisme (grille)
  ou K_{3,3} (paire tordue). c(l) ≤ 3 ⟹ au plus 2 morceaux de 6, donc au moins 4 partenaires sans grille en chaque point.
- Pour TOUTE paire sans grille (l, m) (pas besoin du « côté minimal ») : rank T_S = 23 − c(l) + rank F (F = Schur 20 × 20
  sur les labels extérieurs de m) ; Conway exige rank F ≤ 7 + c(l). Identité de Codex rank T = 32 − c − δ + rank Z
  vérifiée sur les 7 436 côtés sans grille admissibles (T ≥ 0, U ≥ 0) ; on a rank Z − δ = rank F − 9.
- Données (7 436 côtés) : δ = 0 et rank Z ≥ 3 partout, donc rank F ≥ 12. Marges de la branche : c = 1 : 3 ; c = 2 : 2 ;
  c = 3 : 1 (rank Z = 3 apparaît 14 fois à c = 3).
- Spectre des saturations impaires (valeurs propres généralisées λ de (CΦ⁺Cᵀ, K), δ = #{λ = 1}) : au plus 2 valeurs
  ≥ 0,99 par côté ; max λ_2 ≈ 0,97 ; max λ_3 ≈ 0,85 (c ≤ 2), 0,90 (c = 3) ; max λ_4 = 0,716 (c = 1).
- Cible la plus accessible : c = 1, « rank F ≥ 9 » (marge 3), par exemple rank Z ≥ 2 (marge 1) et δ ≤ 2 (λ_3 ≤ 0,85).
  Si rank Z = 3, Conway à c = 1 demanderait 4 saturations impaires EXACTES simultanées ; les données n'en approchent que 2.

## 16/10 nuit : c = 1, de façon fine (demande de Dilan : « rigoureuse et fine, microscopique »)
Scripts : `c1_network.py`, `c1_signed.py`, `c1_starsets.py`-like checks (`c1_starsets.log`), `h46_scan.py`, `h46_lambda2.log`,
`h46_det.py`, logs `c1_network.log`, `c1_signed.log`, `c1_bottleneck.log`, `c1_modp_nullity.log`, `h46_scan.log`, `h46_det.log`.
1. Réduction exacte (prouvée à la main, vérifiée sur les 931 côtés c = 1) : avec l = {v,0,1}, m = {v,2,3}, G_l = graphe
   cubique induit sur les 36 voisins de l (chaque sommet a exactement 1 voisin dans chacun des 3 groupes N(v)\l, L_0, L_1),
   Y = 20 labels {2,s}, {3,s} :
   - les points v, 0, 1 se découplent : seules les combinaisons x_p − x̄ (2 vecteurs universels) et x̄ (t = x̄/12)
     interviennent ; ν(T_S) = 2 + dim ker F avec F = 3I − A_YY + J/12 − Bᵀ L⁺ B (L = laplacien de G_l, B = adjacence
     G_l × Y, chaque y ∈ Y a exactement 6 voisins dans G_l, 2 par groupe). Conway exige dim ker F ≥ 12 ; données 5 à 8.
   - Conway à c = 1 exige en particulier un profil purement impair non constant (δ ≥ 1) : ODD-PURE(c = 1) ⟹ c = 1 exclu.
     Forme signée : ODD-PURE ⟺ la plus grande valeur propre 3 du graphe signé SG (46 sommets : G_l + 10 lettres impaires,
     poids ±1/√2 et A_σ/2) est de multiplicité exactement 2 (vérifié : 931/931). Marge nulle : λ_3(SG) jusqu'à 2,999926.
   - Pas de corrélation entre cette saturation et la connectivité algébrique de G_l (corr 0,07).
2. CRITÈRE H46 (nouveau, net) : soit x ∈ N(l) (ici x = 3, lettre de m) et Y_x = N(x) \ N[l] (10 sommets) ;
   H = N(l) ∪ Y_x a 46 sommets. Entrelacement (spectre 14, 3^54, (−4)^44) : dans Conway, λ_2(A_H) = 3 EXACTEMENT pour
   tout sous-graphe induit de 46 sommets. Données :
   - c = 1 (3 480 cas, deux choix de x) : λ_2(A_H) ∈ [2,9107 ; 2,9927] < 3, jamais 3 ;
   - c ≥ 2 : λ_2(A_H) = 3, multiplicité de 3 = c − 1 exactement (sans grille).
   Donc H46-c1 : « si G_l est connexe, λ_2(A_H) < 3 » ⟹ aucune droite de Conway n'a c = 1. H ne fait intervenir NI le
   second point 2 de m NI ses labels : l'objet local se réduit à G_l (3 appariements sur 12 lettres) + les 10 voisins de x.
   Forme exacte : λ_2(A_H) < 3 ⟺ F_3 = (3I − A_33 − B_3ᵀ L⁺ B_3) restreint aux vecteurs de somme nulle (9 dim) est défini
   positif (inertie : In(3I − A_H) = (36 + p(F_3), z(F_3), 1 + n(F_3))).
   det(3I − A_H) = −16 200 × Δ (2^3·3^4·5^2 divise toujours), Δ ≠ 0 sur les données ; aucun petit premier ne divise
   toujours Δ (7 : 2/30, 11 : 3/30) : pas de preuve par congruence simple.
3. Statut : réduction rigoureuse ; l'énoncé H46-c1 est vérifié sur 100 % des données (biaisées : 93 % h-symétriques) ;
   PAS de preuve. Pistes : inégalité de réseau électrique (marge 0,0073 au pire), énumération exhaustive de (G_l,
   attaches de Y_x) avec certificat, ou filtre dans les modèles globaux de Codex.

## 17/10 : c = 1, marge et mécanisme (demande de Dilan : « prouve ou procède comme Codex, ta marge est plus large »)
Scripts/logs : `c1_robust46.py/.log`, `c1_defect.py/.log`, `c1_trace_ratio.log`, `c1_lambda9.log`, `c1_structV.py/.log`,
`c1_structV9.log`, `c1_nearsat.log`, `c1_cpsat.py`, `c243_components.py/.log`.
- La marge existe dans la bonne formulation : il faut rank F ≥ 9 ; λ_9(F) ≥ 0,52 sur les 931 côtés (médiane 0,95).
  Mais elle est dans des directions NON canoniques :
  - Pboth (motif (1,−1,−1,1) sur {2s, 2s', 3s, 3s'}, 5 dim) : F ≥ 0,15 ; Phub⁰ (motif (1,1,−1,−1), somme nulle, 4 dim) :
    F ≥ 0,12 ; leur réunion = espace impair non constant : serré (0,0002, c'est ODD-PURE), à cause du couplage ;
  - les espaces pairs contiennent des profils exacts (noyau) ; la direction quasi saturée est étalée sur les 5 droites
    (75 % Pboth, 25 % Phub).
  - Bornes de trace : δ ≤ ½ Σ E_s inutile (Σ E_s = 25 à 33 ; C est maximal, 80 incidences, aucune annulation) ;
    tr F/λ_max ∈ [4,8 ; 6,2] et (tr F)²/tr F² ∈ [7,95 ; 9,45] : insuffisant.
  - Meilleur ensemble de 46 sommets (recherche exhaustive C(20,10) sur les côtés les plus serrés) : écart ≤ 0,076.
- Façon Codex : son quotient de Gram (rang R ≤ dim ker C ≤ 4 pour c ≥ 4) dégénère à c = 1 (jusqu'à 14). Modèle CP-SAT
  exhaustif local (`c1_cpsat.py` : axiomes cp6 + connexité de G_l + N vecteurs du noyau mod 5 sur W') : même N = 2
  (que toutes les données satisfont) reste UNKNOWN en 240 s (2 cœurs). Force brute impraticable sans quotient.
- MÉCANISME (exact) : sur H = N(l) ∪ Y_x, les vecteurs propres de valeur propre 3 des données sont exactement les
  vecteurs « de composantes » : ξ constant sur chaque composante de G_l, ζ = 0 sur Y_x, avec Σ_K α_K n_K(y) = 0 où
  n_K(y) = nombre d'attaches de y dans la composante K (comptes FORCÉS par Tσ = 0, relation (5) de Codex) ; d'où
  multiplicité c − 1. Pour c = 1, aucun. Énoncé à prouver (rigidité) : pas d'autre vecteur propre, i.e.
  N_3 − B_3ᵀ L⁺ B_3 ≻ 0 sur l'orthogonal des vecteurs n_K.
- srg(243,22,1,2) connus : c(l) ≥ 2 pour TOUTES les droites des 4 graphes (BvLS 10 ; twin {2,3,10} ; Γ3 {4,5,10} ;
  Γ4 {5,7,10}), toujours au moins une composante prisme : chaque droite est dans une grille. c = 1 n'arrive jamais.

## 17/10 : rigidité pour c = 1 (Dilan : « vas-y »)
Logs : `h46_neareig.log`, `c1_ab.log`.
1. Avec T_S ⪰ 0 (positivité du bloc, vraie dans Conway) : tout vecteur propre (valeur 3) de A_H, H = N(l) ∪ Y_3, se
   prolonge par 0 sur Y_2 en vecteur propre de A_W' ; il vérifie donc aussi les 10 équations de Y_2 (gratuites par
   positivité), ses sommes de groupes sont nulles, et dans Conway c'est un vecteur propre GLOBAL porté par les
   46 sommets de H (nul sur l). Un tel vecteur donne un profil (0, ζ) dont la partie ι-impaire (−ζ/2, ζ/2) est non
   constante : H46-c1 ⟸ ODDCONST (comme ODD-PURE) ; c'est la même difficulté de fond (vecteur du noyau « chiral »,
   cas d'égalité de la contraction ‖K_ι‖ ≤ 1).
2. Anatomie : le quasi-vecteur propre est proche d'un vecteur « de composante » pour une coupure presque réalisée de
   G_l (ajustement en escalier 0,75 à 0,95, recouvrement Fiedler jusqu'à 0,98) ; G_l des données a toujours un goulot
   (a(G_l) ≤ 0,14) ; mais l'écart à 3 ne suit pas a(G_l).
3. Découpage par moyeu (exact) : dim ker F = (1 + a) + (10 − b), a = mult_3(A_H) = dim(P ∩ R^{Y_3}) − 1,
   b = rang de F/F_33 (Schur sur Y_2). Conway exige a ≥ b + 1. Données (1 862 cas, deux moyeux) : a = 0, b ∈ {3..6} ;
   - « a ≤ 1 » ⟺ λ_3(A_H) < 3 : écart min 0,040 (médiane 0,086) ;
   - « b ≥ 1 » ⟺ λ_max(F/F_33) > 0 : min 1,32 ; « b ≥ 2 » : λ_2 min 0,47.
   Donc c = 1 exclu ⟸ (a ≤ 1) ∧ (b ≥ 1). Aucun des deux n'est prouvé.

## 17/10 : suite sur b ≥ 1 et l'angle « toute droite dans une grille » (Dilan : « continue sur ça »)
Log : `c1_bstruct.log`.
- b ≥ 1 ⟺ range(F) contient un vecteur non nul porté par Y_2 ⟺ une relation linéaire vérifiée par la partie Y_2 de
  TOUS les profils. Pas de relation STRUCTURELLE : aucun vecteur fixe (antisymétrique de droite, différence ou somme
  d'arête M) n'est dans R_o de façon systématique (1 à 2 % des cas) ; R_o ∩ (antisymétriques de droite) ≠ 0 dans
  1 738 cas sur 1 862 seulement. b ≥ 1 est un fait de rang « générique ».
- Voie par inégalités (flots de Thomson ⟹ minoration de F) : bloquée exactement par la direction serrée de H46.
  Minorer F/F_33 demande d'inverser F_33, presque singulière (écart 0,007) ; des flots sous-optimaux rendent F'_33
  indéfinie. b ≥ 1 n'est donc PAS plus facile que a ≤ 1 par cette voie.
- « Toute droite est dans une grille » : aucun mécanisme de minoration connu (ρ ≤ 126 et P ≤ 852 sont des
  majorations ; le nombre de grilles n'est pas forcé par les paramètres : 1485, 405, 621, 837 dans les 243). Les
  vecteurs f_S = 3·1_S − A1_S + 1 (9-ensembles, A5) donnent pour chaque paire sans grille un vecteur propre −4
  entier dans U (nul sur N[v]) de norme 14(4 − k), k = arêtes entre coins ; isotropes et orthogonaux mod 7 entre eux :
  pas de contradiction de rang.
- Fait général (entrelacement, vérifié) : dans Conway, tout sous-graphe induit sous-cubique à m ≥ 45 sommets a au
  moins m − 44 composantes 3-régulières (λ_1..λ_{m−44} ≥ 3), chacune d'au moins 6 sommets (ni K4, ni K_{3,3}) ; donc
  tout sous-graphe induit sous-cubique a au plus 52 sommets. Ne s'applique pas à c = 1 (tout sommet hors N[l] touche
  G_l).
- Bilan : la rigidité de c = 1 (sous ses deux formes a ≤ 1, b ≥ 1) relève du même noyau dur que ODDCONST / H-MATCH ;
  aucune des deux voies ne la contourne.

## 17/10 nuit : A et B après la critique de Dilan (« liste énumérée, cas par cas, solveurs »)
Scripts : `cle3_templates.py`, `cle3_qspace.py`, `cle3_template_count.py`, `c1_mincut.py`, `c1_cutfilter.py`,
`c1_cuttypes.py`, `c1_balcut.py`, `sigcut_local.py`, `gg_test.py`, `gg_assign.py`. Logs : `cle3_templates.log`,
`cle3_qspace.log`, `c1_shortvec.log`.

### B1. Modèles de racine pour min c ≤ 3 (extension du générateur de Codex, son fichier non modifié)
- `cle3_templates.py` : tous degrés, toutes partitions en blocs ≥ 2, c_i = 6 − deg_i + #blocs ; filtres exacts
  P (cycle de parité impair), O' (deux liens d'une racine dans deux blocs, même classe), S' (même classe dans un bloc
  ≥ 3 : +égal contredit ⟨v,v'⟩ = −e ≤ 0, −égal ferme la paire), Z (Codex), et K (NOUVEAU, prouvé) : à la racine i la
  Gram des v_ij est diagonale par blocs, chaque bloc = laplacien du multigraphe connexe des rectangles de la composante,
  donc les v_ij engendrent exactement 6 − c_i dimensions et dim ker C ≥ max_i (6 − c_i).
- Validation : `cle3_templates.py 4 --no-exact` redonne EXACTEMENT la sortie de Codex (367 modèles étiquetés,
  200 à permutation près).
- c_min = 3 : 8 706 modèles à symétrie près dans les 131 premiers graphes sur 588 (dim ker C de 3 à 7, run complet
  > 5 min non lancé) ; les relations d'orthogonalité laissent une famille de Gram de dimension ≥ 2 pour presque tous
  (`cle3_qspace.log`). Comptes bruts : 3,7·10⁸ (c_min = 3), 1,8·10¹¹ (2), 3,3·10¹⁰ (1).
  Verdict : le quotient par rectangles ne donne PAS une liste fermable à c ≤ 3 (des blocs de taille ≥ 3 apparaissent).

### B2. c = 1 par vecteurs entiers courts (même mécanisme que les lemmes de Codex)
À une racine l = {v,0,1} avec c(l) = 1, M_0 = multigraphe des 6 rectangles Q_0j (m_jk = arêtes de Γ entre Q_0j et
Q_0k), connexe, degrés d_j = 8 − 2e(Q_0j). Pour tout ensemble S de rectangles, h_S = T 1_{Q_0S} est un vecteur propre −4
ENTIER de norme 7·|coupe_S| (Codex : HᵗH = 7R ; R restreint à la racine = laplacien de M_0).
- Lemme de Codex (17/10) e(Q) ≠ 3, RE-VÉRIFIÉ : norme 14 ⟹ co-Heawood (±1, 7 + 7, même signe ⟹ non adjacents, disjoints
  en lettres, sans voisin commun hors du support) ; dans un rectangle une arête diagonale est isolée (chaque label a
  exactement un voisin par lettre de la racine), donc e = 3 est un chemin le long des côtés, dont les bouts (h = +1)
  partagent une lettre : contradiction.
- LEMME DES 2-COUPES (nouveau, prouvé) : si exactement 2 arêtes de Γ quittent Q_0S, alors ce sont deux arêtes σ
  ({0,a}–{1,σa}, a dans S ; {0,b}–{1,σb}, b hors de S) et σ(b) ≠ a, σ(a) ≠ b (quatre lettres distinctes), et
  σ(μ_0(a)) ≠ σ(b). Preuve : chaque type d'arête (μ_0, μ_1, σ) traverse la coupe un nombre pair de fois (S est une
  réunion de droites) ; deux μ_0 mettraient les deux bouts +1 dans L_0 (lettre 0 commune) ; une lettre commune ou un
  voisin commun d'indice 0 est interdit par co-Heawood. Vaut à toute racine, pour tout c.
- Version « droite » (prouvée) : pour tout C ⊂ G_l équilibré (|C ∩ X_p| = q pair pour les 3 groupes),
  y = (A − 3I)(1_C − (q/12)1_{G_l}) est un vecteur propre −4 entier, nul sur l, de norme 7·|∂C| ; une 2-coupe
  équilibrée est donc co-Heawood (deux arêtes entre les deux mêmes groupes ; bouts intérieurs sans voisin commun).
- Données (1 884 côtés c = 1) : 1 610 ont un rectangle à 3 arêtes ; 1 709 ont une 2-coupe de M_0, TOUTES de type
  interdit (μμ, ou σσ à lettre commune ; sur toutes les données, aucune σσ à quatre lettres distinctes) ; 175 survivent,
  coupe min de M_0 = 4 (109), 6 (45), 8 (21). Sur 40 d'entre eux : 6 ont une 2-coupe équilibrée non alignée, les autres
  ont une coupe équilibrée minimale de 4 ou 6. Ce sont des données, pas une énumération complète.
- Le cas σσ à lettres distinctes est localement possible (`sigcut_local.py`, témoin CP-SAT pour s = 2 et 3).
- Découpage fini pour c = 1 (racine c = 1, coupe min λ de M_0) : I : λ = 2 (σσ distinct, vecteur co-Heawood rigide) ;
  II : λ = 4 (vecteurs de norme 28) ; III : λ = 6 ; IV : λ = 8 (aucun rectangle n'a d'arête interne). Aucun cas fermé.

### A. Faits exacts à une droite l (prouvés, valables pour tout c ; outils, pas d'exclusion)
- Tout sommet lointain (à distance 2 de l, 60 sommets D) a exactement |C|/6 voisins dans chaque composante C de G_l :
  x_C = 1_C − (|C|/36)1_G vérifie que (A − 3I)x_C est porté par D, orthogonal à x_C, donc nul (mesure 11/99·(Σx)² − 7‖Π₋₄x‖²).
- dim(E₋₄ ∩ R^D) = 7 + c(l) et dim(E₃ ∩ R^D) = 18 (vecteurs de span(1) ⊕ E₃, resp. span(1) ⊕ E₋₄, portés par N[l] :
  2 + c, resp. 3, calcul explicite).
- Le graphe lointain A_D (8-régulier, 60 sommets) a un spectre FORCÉ par G_l : {8, 3^18, (−4)^(7+c)} ∪ {λ − 4 :
  λ valeur propre du laplacien de G_l hors 0^c et des deux 3 des vecteurs de groupe} (entrelacement N A_D = (L − 4I)N + 2J,
  identité des sommes μ/λ des paires G–D). Traces A_D, A_D², A_D³ vérifiées (t_D + t_G = 32).
- Structure lointaine : pour chaque point p de l, z ↦ (paire de ses 2 voisins dans X_p) est une bijection de D sur les
  60 paires non adjacentes de X_p ; comptes croisés exacts. CP-SAT (deux encodages) : UNKNOWN en 30-60 s, pas un filtre
  rapide. Le noyau dur « chiral » n'est pas attaqué ici.
- Suite (17/10 vers 02:30-03:30, `c1_rlattice.py`, `c1_n28look.py`, `case1_coheawood.py`, `gg_case1.py`) :
  - vecteurs de norme 14 du réseau R des 11 rectangles visibles (deux racines l, m ; c ∈ {−1,0,1}^11) : sur les 175
    survivants, 64 en ont, et les 64 sont tués par une violation co-Heawood visible (valeur ±2, plus de 7 d'un signe,
    deux labels de même signe adjacents ou partageant une lettre) ; 111 restent, sans vecteur de norme 14 visible
    (48 sans même un vecteur de norme 28 de ce type). Bilan données : 1 773 / 1 884 côtés c = 1 tués par des
    arguments entiers exacts ; les 111 restants sont le régime « générique » (rectangles presque sans arête interne).
  - Fait co-Heawood utile (prouvé) : hors du support, tout sommet a soit aucun voisin dans le support, soit exactement
    un + et un − (deux sommets de même signe ont leurs 2 voisins communs dans le signe opposé) ; 70 sommets « liés »,
    15 « libres ».
  - Cas I (2-coupe σσ à lettres distinctes), type de droite LIBRE : le modèle co-Heawood local (sans plan lointain)
    est SAT en 13 s ; avec le plan lointain exact (GG), la condition « lié » sur les 60 labels lointains et le degré
    lointain 8 : UNKNOWN en 220 s. Le plan lointain reste le goulot de CP-SAT. Cas I non fermé.
  - Remarque : la version « droite » du lemme des 2-coupes vaut aussi À L'INTÉRIEUR d'une composante de 12 ou 18
    sommets (ensemble équilibré de 6 sommets coupé par 2 arêtes) ; elle pourrait filtrer les tables locales 12/18 de
    Codex. Non transmis (consigne : laisser Codex seul).
