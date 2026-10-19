# Conway-99 : état réel, mécanismes de C2, C3 et C7, information oubliée, cadre lointain d'une droite

*19/10/2026, LAB. Réponse au mandat « recherche conceptuelle et changement de représentation ».*

- **Commit de référence** : `origin/main` 76860d92 (amazing-source/conway99-c1). Le registre c = 3 y est à 35 ouverts
  (de96dd72).
- **Statuts** : P = preuve écrite ici, C = calcul exact, O = observation, A = déjà dans l'archive (référence donnée),
  N = négatif, X = ouvert.
- **Noms** : « C1 » désigne le régime sans automorphisme (C2 = involution, C3 = ordre 3, C7 = ordre 7). Le cas
  combinatoire c(ℓ) = 1, une droite dont le graphe cubique G_ℓ est connexe, est une autre chose.

---

## 0. Le meilleur résultat, sa portée, ce qu'il ne tranche pas

**Théorème 1 (cadre lointain d'une droite) — section 4.** Soit T une droite d'un srg(99,14,1,2), de voisinage N
(36 sommets) et de côté lointain F (60 sommets), et c = c(T). On a les identités exactes entre G_T, l'incidence
E : N × F et le graphe R_T induit sur F. Il en découle :
- le spectre de R_T ;
- l'espace lointain E₋₄(Γ) ∩ ℝ^F, de dimension 7 + c, et l'espace E₃(Γ) ∩ ℝ^F, de dimension 18 ;
- la formule explicite du projecteur lointain :
  7Π_T = 3I − R_T − [Eᵀ(4I + G_T) − 2J](EEᵀ)⁺E, où (4I + G_T)(EEᵀ)⁺ = (3I − G_T)⁺ sur Y ;
- le mécanisme propre à 99 : la dépendance en c vient de la coïncidence r = 3 = degré de G_T, qui fait entrer le
  laplacien de G_T.

Les identités générales et la formule du projecteur ont été contrôlées exactement sur deux srg(243,22,1,2) réels. Les
dimensions lointaines y valent 72 et 50, indépendantes de c (C).

**Corollaire 2 (droite dans six grilles) — section 5.** Si c(T) = 6, alors 420 Π_T est une matrice **entière**
explicite, fonction des 60 noms (Z₃ × Z₂)⁶ de l'archive et de R_T. C'est un cadre de rang 13 du type de C7. Les
conditions λ, μ côté lointain y deviennent trois équations de vecteurs propres.

**Proposition 3 (portée exacte de la réduction) — section 1.3.**
- Le registre c = 3 porte sur une racine de **budget** (s ≤ 51) dont les sept droites ont c ≥ 3. Il couvre donc le
  minimum global m = 3, mais pas tel quel la branche « il existe une racine à sept droites c ≥ 3 ».
- Pour cette branche, l'extension sans budget compte 20 survivants des filtres (13 à 21 grilles). Aujourd'hui,
  **6 sont exclus par des certificats exacts d'ordre 2**, revérifiés par le vérificateur indépendant ; 14 restent.

**Ce que cela concerne.**
- Les droites à c ≤ 2 (branche (II)) et les droites à c = 6 (sous-cas de toutes les branches).
- La portée des branches m = 3 et m ≤ 2 (I).

**Ce que cela ne tranche pas.** Aucune branche n'est fermée par ces résultats. Aucune nouvelle exclusion d'un Conway
global. Les pistes non abouties, avec le maillon précis qui manque, sont en section 7.

---

## 1. État réel

### 1.1 Objets

- **Racine r.** 14 lettres en 7 droites ; 84 étiquettes, chacune étant une paire de lettres de droites distinctes ;
  B est le graphe des étiquettes, U l'incidence lettres/étiquettes.
- Γ est entièrement déterminé par (r, la structure des lettres, B) : 99 = 1 + 14 + 84.
- **Équivalence (P).** Γ est un Conway si et seulement si :
  - UB = Q (quotas, Q_xw = 2 − [x ∈ w] − [x' ∈ w]) ;
  - B² + B = 12I + 2J − UᵀU ;
  - B est 0/1, symétrique, à diagonale nulle.
- **Droite T** (triangle de Γ). G_T est le graphe cubique induit sur les 36 voisins de T, et c(T) son nombre de
  composantes.
  - Composantes de taille 6k, avec 2k sommets par classe (§4).
  - Une composante de 6 sommets est un prisme, donc une grille 3×3 contenant T. K₃,₃ est exclu par μ = 2 : deux
    sommets d'un même côté auraient 3 voisins communs (A, note 194).
  - Vu d'un point de T, c(T) est le nombre de **blocs** de la droite.
- **Trois normalisations distinctes.**
  - (a) Le minimum global m = min_ℓ c(ℓ).
  - (b) Le minimum des sept droites d'une racine choisie.
  - (c) Une racine de budget s(x) ≤ 51, où s(x) est la somme des prismes des droites passant par x. Elle existe parce
    que Σ_x s(x) = 6P ≤ 5112.
  - Rien ne permet de réaliser deux de ces normalisations au même sommet sans preuve.

### 1.2 La réduction par les droites

| Étape | Énoncé | Statut, dépendances |
|---|---|---|
| m ≤ 4 | Il existe une droite à c ≤ 4. | **P.** P ≤ 852 (certificat rationnel du recensement d'ordre 9 : Σ w_g N_g = 11088/13 − P, poids ≥ 0, revérifié exactement le 18/10). Σ_L t(L) = 2P, donc une droite a t(L) ≤ 7. Chaque grille par L donne 2 prismes, donc g(L) ≤ 3. Hors prismes, les composantes ont au moins 12 sommets, donc c ≤ 3 + g/2 ≤ 4. |
| m = 4 exclu | « c(L) ≥ 4 pour toute droite » est impossible. | **Verdicts CP-SAT**, sans certificat portable (`c4_selected_root_closed.json` : racine minimisant 9s + 8g, 79 gabarits sur 79). Pour une racine de budget quelconque, 76 sur 79 (7, 9, 19 non couverts). |
| m = 3 | Pour une racine de budget à sept droites c ≥ 3 : 10 052 gabarits (k ≤ 12 grilles, Gram entier), 35 ouverts. | 7 en production P3 (AWS). Méthodes et statuts : `c3_inventaire_2026-10-19.md`. |
| m ≤ 2 | Dichotomie : (I) un sommet a ses sept droites à c ≥ 3, possible si au plus 32 droites ont c ≤ 2 ; (II) tout sommet est sur une droite à c ≤ 2, d'où au moins 33 telles droites. | (I) : section 1.3. (II) : **aucune méthode finie** (X). |

### 1.3 Portée du registre c = 3 (Proposition 3)

**Énoncé (P).**
- (i) Sous m = 3 global, la racine de budget a ses sept droites à c ≥ 3. Le registre c = 3, une fois ses 35 ouverts
  fermés, exclut donc m = 3 global.
- (ii) La branche m ≤ 2 (I) produit une racine à sept droites c ≥ 3, **sans budget**. Le registre ne s'y applique
  qu'à deux conditions :
  - les gabarits à plus de 12 grilles sont aussi exclus ;
  - chaque méthode d'exclusion ne s'est pas servie de la contrainte s ≤ 51.

**Calculs du jour (C).**
- Le recensement sans budget (`cpp_census_nobudget/`, 18/10) a laissé 20 survivants des filtres de gabarits à 13–21
  grilles. Leur dimension de noyau va de 0 à 3. Le bilan d'audit parlait de « 17 ouverts » après le test de Gram.
- Le design d'ordre 2 (`z2_certify.py`) donne un certificat de Farkas exact pour les indices 0, 3, 6, 8, 11 et 15.
  Les six certificats sont **valides** pour `z2_verify.py`, en bibliothèque standard, avec son propre catalogue
  d'états, qui concorde.
- Les 14 autres sont réalisables au niveau du design. Leur statut au test de Gram reste à recouper.
- Fichiers : `representation_2026-10-19/nobudget_z2/`.

**Dépendance au budget.**
- ZC et Z2C n'utilisent pas le budget.
- Certains modèles CP-SAT l'imposent (`root_prism_budget: 51`) avec un drapeau « redondant ». Le statut sans budget de
  chaque exclusion du registre est **à recenser méthode par méthode** (X). Ce n'est pas fait ici.

---

## 2. Pourquoi les changements de langage de C2, C3 et C7 ont servi

### C3 (`preuve_c3.tex`)

- **Les deux évaluations.** L'action de Z/3 fait de A un module sur Z[x]/(x³ − 1). Le morphisme Φ envoie
  l'identité A² + A = 12I + 2J sur le quotient de taille 33. Les évaluations en x = 1 et x = ω donnent deux
  matrices :
  - Q, entière, avec Q² + Q = 12I + 6J, car Φ(J) = (1 + x + x²)J et 1 + 1 + 1 = 3 ;
  - M, hermitienne sur Z[ω], avec M² + M = 12I, car 1 + ω + ω² = 0.
- **Pourquoi Z[ω] et la congruence modulo π.** Z[ω] est l'anneau des valeurs du caractère non trivial. On a
  Q − M = (1 − ω)A₁ + (1 − ω²)A₂ ≡ 0 modulo π = 1 − ω, et Z[ω]/π = F₃. Les deux évaluations se rencontrent donc
  modulo π.
- **Le mécanisme.**
  - On note d et d' les déterminants des réseaux des vecteurs propres entiers de valeur 3.
  - d = 7^a 11^b avec b **impair**, à cause du 11 de ⟨j, j⟩ = 33 et de la colle avec Zj ; donc d ≡ −1 (mod 3).
  - d' = 7^c, donc d' ≡ 1 (mod 3).
  - La congruence Q ≡ M (mod π) force r = r' et d ≡ d' (mod 3), car tout carré non nul de F₃ vaut 1.
- **Pourquoi le discriminant fait plus que le rang.** Les rangs concordent ; seule la classe du déterminant, fixée
  par une donnée globale (le premier 11), les sépare.

### C7 (`order7.tex`)

- **La compression.** Les comptages d'orbites donnent C (12 × 12) avec C² + C = 12I + 12J − 2uuᵀ. Un argument de
  représentation rationnelle donne une diagonale nulle (d ≡ 0 mod 6). Alors G = 3C + 12I − 4J − 2uuᵀ vaut 21 fois
  un projecteur de rang 4 : ce sont 12 vecteurs de ℝ⁴ à Gram **entier**, de forme imposée.
- **Ce qui ferme.**
  - Bornes entières : C_ij ≤ 4 et h ∈ {3, 4, 5}, par Cauchy–Schwarz.
  - Arithmétique des résidus. Projetés sur une normale, les résidus α = 12 z² sont entiers et de somme nulle. Donc
    √α_l = √α_j + √α_k, ce qui force α_j α_k à être un carré.
  - Une analyse de cas finie.
- La baisse de dimension seule ne suffit pas. Il faut aussi que les entrées soient entières dans un petit ensemble et
  qu'il y ait des relations linéaires exactes, qui deviennent des conditions diophantiennes.

### C2 (`order2.tex`)

- **La chaîne.**
  - Les fonctions impaires donnent S (49 × 49) avec S² + S = 12I, puis H = 3I − S = 7 fois un projecteur de rang 22 :
    c'est un cadre entier.
  - N = √7 K*, de discriminant F₇^{22−g}. L'oddité force g pair et une forme **non scindée**.
  - On en tire un sur-réseau N_max de déterminant 49, que l'on recolle avec 7I₂. On obtient une **enveloppe**
    unimodulaire impaire de rang 24 : l'un des 156 réseaux de Borcherds.
  - On exclut ensuite par les vecteurs courts : l'énergie vérifie E ≥ 11, grâce aux lemmes T16, T18 et T20 (pas de
    fonction propre entière impaire de norme ≤ 20).
- **La part de calcul.** Les lemmes T16–T20 et l'énumération des paires de normales sont **assistés par
  ordinateur**. La preuve n'est donc pas entièrement sans ordinateur.

### Mécanisme transférable

- **Ce que les trois preuves ont en commun.**
  - Une identité quadratique exacte transforme un **petit** objet entier en un projecteur mis à l'échelle, donc en un
    cadre entier de petit rang.
  - L'arithmétique de ce cadre ferme : classes de discriminant, enveloppe classifiée, conditions diophantiennes sur
    les résidus.
- **Rôle de la symétrie.** Elle sert à produire l'objet petit. Dans C3, elle produit en plus la **seconde** forme
  entière congrue.
- **Sans symétrie (C1)**, l'identité quadratique vaut sur trois objets :
  - (i) le second sous-constituant d'une racine : rang 30, 8T entier (A) ;
  - (ii) le côté lointain d'une droite : rang 7 + c (Théorème 1) ;
  - (iii) les réseaux propres globaux : rang 44 ou 54.
- **L'objet le plus petit est (ii)**, avec un rang 8 si c = 1. C'est le seul de taille comparable à C7 ou C2. Mais son
  cadre n'est entier qu'au laplacien de G_T près : ses dénominateurs sont τ(G_T) et det(4I + G_T). Il est entier dès
  que G_T a un spectre entier, en particulier pour c = 6 (Corollaire 2).

---

## 3. La chaîne entre le graphe et le solveur, et ce qu'elle oublie

| Passage | Nature |
|---|---|
| Γ → (r, lettres, B) | **Équivalent** (§1.1) |
| Choix de r : budget, minimum local, minimisation de 9s + 8g | **Choix couvrant**, prouvé normalisation par normalisation, jamais deux à la fois sans preuve (§1.1) |
| B → 2-facteurs des 7 droites, composantes, blocs | Données déterminées par B ; rien de perdu |
| → gabarit (graphe des grilles + partitions en blocs) | **Seulement nécessaire** : oublie B |
| → vecteurs H_F = 1 + (3I − A)χ_X (X = r ∪ deux droites ∪ Q_ab), dans W_r = E₋₄(B) ∩ ker U | Équivalent à une partie de B |
| → Gram G_H = 7RᵀH, semi-défini, de rang ≤ dim ker C, entrées dans 7ℤ bornées, diagonale 56 − 14e | **Nécessaire** : connaît le réseau des H à isométrie près, pas son plongement |
| → couverture par des Gram entiers, à automorphismes du gabarit près | **Dépend des coordonnées** : normalisation |
| → familles : relations du noyau → identités coordonnée par coordonnée → cœurs signés → SAT + RUP | Exact sur le sous-modèle ; **nécessaire** |
| → designs de comptage ZC et z2 | **Relaxations**, avec certificats exacts quand elles tuent |

**Ce qui disparaît**, avec l'endroit où c'est récupéré.
- **(F1) Le plongement du réseau des H dans ℤ⁸⁴** : coordonnées base − z, multiplicités d'états. ZC et z2 le
  récupèrent en partie.
- **(F2) L'adjacence B entre étiquettes** au-delà des comptes. Seul le SAT sur des cœurs la récupère.
- **(F3) Le cadre lointain de chacune des 7 droites**, de rang 7 + c_a (Théorème 1). Le test de Gram ne voit que des
  sommes de rectangles. La condition de rang (rang F ≤ 7 + c(l)) n'existe que dans les objets « T_S » à quatre
  étoiles (A, EXPLORATION l. 335).
- **(F4) L'arithmétique des cartes d'au moins 45 sommets entièrement connus.** Par DISC (SQ3, prouvé, A), tout
  sous-graphe induit H de 45 sommets a det(A_H − 3I) carré parfait. Le gabarit ne l'atteint **jamais** (fait de
  structure, P) :
  - deux étiquettes de rectangles-grilles disjoints sont reliées par un couplage inconnu ;
  - des rectangles-grilles deux à deux sécants forment une étoile (au plus 6) ou un triangle (3) ;
  - on a donc au plus 15 + 24 = 39 sommets connus.
- **(F5) La simultanéité des racines voisines** : droites, grilles et c partagés, transports de gabarits.
- **(F6) Le genre du réseau global** (k ≤ 28, fenêtre de rang 7 ; A).

**Question prioritaire : une même donnée de Gram peut-elle avoir des prolongements différents ?** Oui.
- **Exemples exacts de l'archive.** Les 645 germes de rang 30 et les 331 objets de rang 30 à quatre étoiles du 15/10
  passent tous les tests au niveau réel : positivité, rang 30, borne de rang 7. Ils meurent par la classe carrée
  (DISC : exposants impairs en 3 et 5) ou par l'extension (A, `NOTE_PROOFS_1410.md`).
- **La donnée qui rend la différence visible sans SAT** est arithmétique : classe carrée du déterminant d'une carte de
  45 sommets, ou forme discriminante p-adique d'un réseau local. C'est exactement la leçon de C3. Le gabarit ne peut
  pas la voir (F4).
- Pour un réseau lointain, la condition locale de Hasse ne filtre qu'en 7 (A, `NOTE_RESEAUX_DE_DROITE.md`, 09/10).

**Ce que la dimension ne mesure pas.**
- Elle ne dit pas que les branches de grande dimension sont plus proches de l'existence. dim ker C, jusqu'à 14 pour
  c = 1, mesure le jeu de la relaxation.
- Elle ignore le **rang lointain** 7 + c de chaque droite, qui varie en sens inverse : petit pour c petit.
- Elle ignore l'**arithmétique du laplacien de G_T**, qui fixe les dénominateurs du cadre lointain (§4, (l)).

---

## 4. Théorème 1 : le cadre lointain d'une droite

**Notations.**
- T = {p, q, s} est une droite ; N_x = N(x) ∖ T pour x ∈ T ; N = N_p ⊔ N_q ⊔ N_s, avec |N| = 36 ;
  F = V ∖ (T ∪ N), avec |F| = 60.
- G = G_T est le graphe induit sur N ; E est l'adjacence N × F ; R = R_T est le graphe induit sur F.
- J_cl est l'indicatrice « même classe » sur N ; Y = {y ∈ ℝ^N : y ⊥ 1_{N_p}, 1_{N_q}, 1_{N_s}}.

**(a) Degrés (P).**
- Un sommet u ∈ N_p a :
  - un voisin dans N_p : le troisième point de la droite pu, par λ = 1 ;
  - un voisin dans N_q, car μ(u, q) = 2 ; les voisins communs sont p et un sommet de N_q, puisque u ≁ s ;
  - de même un voisin dans N_s ;
  - donc 10 voisins dans F.
- Un sommet w ∈ F a exactement 2 voisins dans chaque N_x (μ(w, x) = 2). Il en a donc 6 dans N et 8 dans F.

**(b) Identités par blocs (P).** On restreint A² = 12I − A + 2J aux blocs (N,N), (N,F) et (F,F) :
- (I1) EEᵀ = 12I − G − G² + 2J − J_cl ;
- (I2) ER = 2J − E − GE ;
- (I3) R² + R + EᵀE = 12I + 2J.

**(c) Spectre de G sur Y (P).** On a G 1_{N_x} = 1_N, donc G préserve span(1_{N_x}) et Y.
- Sur span(1_{N_x}), G a les valeurs propres 3 (sur 1_N), puis 0 et 0.
- Sur Y, EEᵀ = (3I − G)(4I + G).

**(d) Composantes (P).** Une composante K, qui est cubique, rencontre chaque classe en |K|/3 sommets, en nombre pair.
- Les vecteurs 1_K − (|K|/36)1_N engendrent Y ∩ E₃(G), de dimension c − 1.
- Comme les valeurs propres de G sont ≥ −3, on a (3 − θ)(4 + θ) = 0 si et seulement si θ = 3. Donc
  ker EEᵀ = (Y ∩ E₃(G)) ⊕ span(1_{N_p} − 1_{N_q}, 1_{N_q} − 1_{N_s}). D'où rang E = 35 − c.

**(e) Équirépartition (P).** Comme 1_K − (|K|/36)1_N ∈ ker Eᵀ, tout w ∈ F a exactement |K|/6 voisins dans K.

**(f) Spectre de R (P).**
- **Sur ker E** (dimension 25 + c, orthogonal à 1_F car 1_F = Eᵀ1_N/6) : R² + R = 12 par (I3). Les valeurs propres
  sont 3 et −4, de multiplicités a + b = 25 + c.
- **Sur im Eᵀ.** Pour y ∈ Y avec Gy = θy et θ ≠ 3, (I2) donne R Eᵀy = −(1 + θ)Eᵀy, avec Eᵀy ≠ 0. De plus R 1_F = 8·1_F.
- **Les traces.** De tr G = 0 on tire Σθ_i = −3c. De tr R = 0 on tire 3a − 4b = 26 − 4c. Donc **b = 7 + c** et
  **a = 18**.
- Les −1 − θ_i ne valent jamais 3 ou −4, puisque θ_i ∉ {−4, 3}.

**(g) Prolongement (P).** Soient θ ∈ {3, −4} et x ∈ ker E avec Rx = θx. Prolongé par 0, x est un vecteur propre de
valeur θ de Γ : (Ax)_T = 0, (Ax)_N = Ex = 0 et (Ax)_F = Rx. La réciproque est immédiate.
- Donc dim(E₋₄(Γ) ∩ ℝ^F) = 7 + c et dim(E₃(Γ) ∩ ℝ^F) = 18. Ces dimensions étaient dans l'archive (EXPLORATION
  l. 479).

**(h) Projecteur (P).**
- Soit Π_T le projecteur orthogonal sur E₋₄(Γ) ∩ ℝ^F = E₋₄(R) ∩ ker E.
- Par (f), Π_T = (3I − R)/7 · (I − Eᵀ(EEᵀ)⁺E), car R commute avec Π_{ker E}.
- Comme (3I − R)Eᵀ = Eᵀ(4I + G) − 2J par (I2) :

  **7 Π_T = 3I − R − [Eᵀ(4I + G) − 2J](EEᵀ)⁺E.**

- Sur Y, (4I + G)(EEᵀ)⁺ = (3I − G)⁺. C'est l'inverse généralisé du **laplacien** de G_T : ses dénominateurs
  (arbres couvrants, groupe critique) sont ceux du cadre lointain.
- Les déterminants des réseaux Λ₋(T) et Λ₃(T) en fonction de τ et Θ figurent dans l'archive (A,
  `NOTE_RESEAUX_DE_DROITE.md`). La formule du projecteur est donnée explicitement ici.

**(i) Ce qui est propre à 99 (P + C).**
- Pour un srg(v, k, 1, 2) de valeurs propres r et s, le même calcul donne, sur Y, EEᵀ = (rI − G)(G − sI).
- Les composantes de G_T n'entrent dans le noyau que si r = 3 = deg G_T, c'est-à-dire dans le seul cas k = 14.
- De même, la domination exacte par une grille vient de (A − 3I)χ_X = 1. Pour r = 4, (A − 4I)χ_X n'est pas
  constant.
- **Contrôle exact sur deux srg(243,22,1,2)** (BvLS et twin, `far_frame_check.py`) :
  - (I1), (I2) et (I3) tiennent exactement ;
  - les dimensions lointaines valent 72 (r = 4) et 50 (s = −5) sur chaque droite testée, avec c = 10 ;
  - le spectre de R_T est {16, 4⁷², (−5)⁵⁰, (−4)⁹, (−2)¹⁰, (−1)¹⁸, 1²⁰}, comme le prédit la version générale de (f)
    pour dix prismes ; comme r ≠ 3, les vecteurs de composantes n'y sont pas dans ker Eᵀ et donnent −1 − 3 = −4 ;
  - la formule générale du projecteur, (r − s)Π = (rI − R)(I − Eᵀ(EEᵀ)⁺E), est vérifiée à 10⁻¹⁵ près.
- **Conséquence pour les bancs d'essai.** Un énoncé lointain qui dépend de c ne peut pas être calibré à 243 sommets.
  Les identités (I1)–(I3) et le projecteur, si.

---

## 5. Corollaire 2 : droite dans six grilles

**Hypothèse et notations.**
- c(T) = 6 : T est dans six grilles G_k = T ∪ X_k.
- Par domination exacte, (A − 3I)χ_{G_k} = 1, donc chaque b ∈ F a un unique voisin v_k(b) ∈ X_k. On note
  x_k(b) = (colonne, ligne) ∈ ℤ₃ × ℤ₂.
- Faits (N1) et (N2) de la note C1 §17.46 (redérivés le 19/10) :
  - chaque nom utilise chaque colonne deux fois ;
  - pour k ≠ j, #{b : x_k = v, x_j = v'} vaut 1 si v et v' ont même colonne, 2 sinon.

**Énoncé (P).**
- **Le Gram entier.** Pour b, b' ∈ F, on pose rel_k(b, b') ∈ {égal, barreau (même colonne), ligne (même ligne),
  autre}, avec les poids w = −19, −1, −3, +3. Alors :

  **420 Π_T(b, b') = 180 δ_{bb'} − 60 R(b, b') + 25 + Σ_k w(rel_k(b, b')).**

  C'est une matrice entière, semi-définie, telle que (420Π)² = 420·(420Π), de rang 13 et de diagonale 91.
- **Relations.** La somme des 10 vecteurs de chaque bloc {b : x_k(b) = v} est nulle. Les vecteurs voisins d'un sommet
  ont pour somme −4 fois ce sommet.
- **Les conditions côté lointain** (λ, μ entre F et les prismes ; C1 §17.46) équivalent à trois équations de
  vecteurs propres de R :
  - R ε_k = −2ε_k, où ε_k est le signe de la ligne de x_k ;
  - R f(c_k) = −f(c_k) pour f : ℤ₃ → ℝ de somme nulle ;
  - R (f(c_k)ε_k) = f(c_k)ε_k.

**Preuve.**
- **Les fonctions images.** Les vecteurs propres du prisme K₃ × K₂ sont 1 (θ = 3), (−1)^σ (θ = 1), f(i) (θ = 0) et
  f(i)(−1)^σ (θ = −2). Leurs images par Eᵀ sont 1_F, ε_k, f(c_k) et f(c_k)ε_k. Par (f), R y agit par 8, −2, −1 et 1.
- **Orthogonalité.** Par (N2) :
  - ⟨ε_k, ε_j⟩ = 60 δ ;
  - ⟨f(c_k), g(c_j)⟩ = ⟨f, g⟩(20 δ_{kj} − 4(1 − δ_{kj})) ;
  - ⟨f(c_k)ε_k, g(c_j)ε_j⟩ = 20 δ_{kj}⟨f, g⟩ ;
  - les termes croisés sont nuls.
- **Les projecteurs.** On en déduit :
  - P_ε = (1/60) Σ ε_k ε_kᵀ ;
  - P_c(b, b') = (a_col(b, b') − 2)/24, où a_col compte les colonnes égales ;
  - P_{cε}(b, b') = (1/20) Σ_k ([c_k(b) = c_k(b')] − 1/3) ε_k(b) ε_k(b').
- **Conclusion.** Par (h), 7Π = 3I − R + J/12 − 5P_ε − 4P_c − 2P_{cε}. En regroupant coordonnée par coordonnée,
  on obtient les poids −19/60, −1/60, −3/60 et +3/60, d'où la formule.
- **Contrôles.** Trace 91·60 = 420·13. Sommes de lignes nulles. 420Π ε_k = 0, car (N2) équilibre les lignes.

**Lecture.**
- C'est un objet du type de C7 : 60 vecteurs de ℝ¹³ à Gram entier dans un petit ensemble, avec des relations
  linéaires exactes.
- La méthode des résidus de C7 devient **applicable** ; elle n'est pas encore appliquée.
- Le design reste à classer (section 7, P1).

---

## 6. Énoncés négatifs démontrés ou calculés aujourd'hui

1. **(N, P) Le transfert le plus direct de C3 (gains sur Γ) est impossible.**
   - Soit s un gain ℤ₃ sur les arêtes orientées. Si A_s² + A_s = 12I, le revêtement triple dérivé aurait
     Ã² + Ã − 12I = (2/3)J, qui n'est pas entier.
   - Une signature ±1 avec A_s² + A_s = 14I donnerait des valeurs propres irrationnelles (−1 ± √57)/2, de
     multiplicités égales, alors que 99 est impair.
   - Cela n'exclut pas d'autres « secondes formes ». Mais l'analogue direct de M, obtenu par un gain sur Γ, n'existe
     pas sans action de groupe.
2. **(N, C) Positivité de Gegenbauer projetée** (méthode de Liao–Wang–Yu–Cai, réimplémentée).
   - Références de 1 à 4 sommets, dans E₋₄ et E₃, jusqu'au degré 40 : aucune contrainte sur P.
   - Sommets + droites avec noyaux produits : P ≤ 1151 seulement ; L16 de l'archive le donnait déjà.
   - C'est plus faible que le recensement d'ordre 9 (P ≤ 852). Commit 76860d92.
3. **(C) Design « six grilles ».** La partie colonnes n'est **pas** unique : plus de 536 classes à S₆ × S₃ près en
   moins de 5 minutes, sans terminer. L'archive n'avait vu qu'une solution canonique. Le SAT brut de l'étape A (noms)
   reste indécis à 280 s : UNKNOWN, qui ne ferme rien.
4. **(C) Moteur de comptage indépendant.** Ordres 2 à 6 : 2, 4, 9, 21 et 62 types, un paramètre libre à l'ordre 6.
   C'est l'accord avec census2 et avec l'affirmation non relue de Reimbayev.

---

## 7. Ponts essayés : contrats et maillons manquants

| Pont | Objet construit depuis un Conway | Résultat extérieur | Maillon manquant | Conséquence si réussite |
|---|---|---|---|---|
| **P1. Six grilles, type C7** | Noms (ℤ₃×ℤ₂)⁶ + R_T ; Gram entier 420Π de rang 13 (Cor. 2) | Aucun : combinatoire finie | Classer les solutions de colonnes (≥ 536 classes ; génération ordonnée à écrire), puis la partie signes, à petite taille (360 bits par classe). Les solveurs CDCL butent sur les contraintes d'équilibre (UNKNOWN à 45 s) : il faut un argument par caractères sur ℤ₂⁶ ou un programme en nombres entiers. | « Aucune droite dans six grilles » : tue 9302, 9791, 9912, 9966, 10003, 10006 et 10025, et supprime c = 6 de toutes les branches |
| **P2. Trou lointain en valeur 3, type C2** | Λ₃(T), de rang 18 ; pour une droite à G_T connexe et Θ typique (≈ 10¹⁹), Hermite donne un vecteur propre entier de valeur 3, nul sur N[T], de norme ≤ 30 au rang 37 (A, 09/10) | Hermite, Blichfeldt | **Le lemme sans hypothèse est faux (P, ci-dessous).** Il faut donc un énoncé restreint et une normalisation qui garantit une droite où il s'applique ; aucune des deux n'existe | Exclusion du rang 37, le verrou de la route des rangs, si l'on obtient à la fois un lemme restreint et le choix de droite qui va avec |
| **P3. Deux formes congrues, type C3** | — | — | **Impasse démontrée** au niveau de A (§6.1). Au niveau d'une droite, les trois racines voient le même G_T, sans torsion. | — |
| **P4. DISC sur les cartes du gabarit** | Cartes de 45 sommets | SQ3 | **Impasse de structure** : au plus 39 sommets connus (F4). Via une droite à six grilles, DISC se réduit à **une** classe carrée du complément de Schur lointain (rang 6) : peu d'information. | — |
| **P5. Cadre de fusion des voisinages** | U_v = vect{x_u : u ∼ v} ; Σ Q_v = 31,5·I (cadre de fusion serré) ; c(T) = 37 − dim(U_p + U_q + U_s) (P) | Bornes de Bachoc sur les grassmanniennes | Les traces de produits sont des comptes de recensement d'ordre ≤ 8 ; 99 sous-espaces dans Gr(14, 44) restent trop peu nombreux | Rien de linéaire de nouveau ; reformulation seulement |
| **P6. Positivité globale** | Sommets, droites, références jusqu'à 4 sommets | Schoenberg | Négatif calculé (§6.2) | — |
| **P7. Intégralité du recensement, enveloppe de rang 48** | — | — | Impasses archivées : aucune congruence ; masse ≈ 10¹²¹ | — |

**Pourquoi le lemme P2 non restreint est faux (P).**
- Soit L une droite disjointe de T avec e(T, L) = 3 (prisme), et soient L ∪ K, L ∪ K′ deux grilles de L ne contenant pas T.
- Chaque t ∈ T a exactement un voisin dans L ∪ K, par domination exacte. C'est son voisin sur L, donc K ∩ N[T] = ∅, et de même
  K′ ∩ N[T] = ∅.
- χ_K − χ_{K′} = χ_{L∪K} − χ_{L∪K′} est un vecteur propre entier de valeur 3, nul sur N[T], de norme 12.
- Une minoration des normes lointaines doit donc exclure cette situation : par exemple, aucune droite parallèle à T n'est dans deux
  grilles évitant T. Il faut alors une normalisation couvrante qui fournit une telle droite. C'est le maillon manquant.


---

## 8. Registre (à reporter dans le ledger)

| Entrée | Nature | Portée |
|---|---|---|
| Théorème 1 (cadre lointain, projecteur explicite, spécificité r = 3) | P, contrôle C à 243 sommets | Toute droite ; base des ponts P1 et P2 |
| Corollaire 2 (Gram entier six grilles) | P | Droites à c = 6 |
| Proposition 3 (portée du registre c = 3 ; budget) | P | m = 3 global contre m ≤ 2 (I) |
| 6 des 20 gabarits sans budget exclus par z2 (indices 0, 3, 6, 8, 11, 15) | C, certificats revérifiés | Branche (I), partie à 13–21 grilles |
| Seconde forme à la C3 par gains sur Γ impossible | N, P | Ferme le transfert direct de C3 |
| Lemme P2 non restreint faux (χ_K − χ_K′, norme 12) | N, P | Indique quelle hypothèse est nécessaire pour P2 |
| Gegenbauer projeté jusqu'à 4 sommets ; positivité droites ≤ 1151 | N, C | Positivité globale aux ordres ≤ 6 |
| Colonnes du design six grilles : plus de 536 classes | C, énumération incomplète | P1 |
| SAT brut de l'étape A : UNKNOWN | **difficulté non surmontée**, pas une impasse | P1 |
| DISC sur gabarits : au plus 39 sommets connus | P (structure) | Impasse pour le test sur gabarits seuls |

---

## 9. Questions discriminantes suivantes

1. **(P2)** Sous quelle hypothèse sur T (aucune droite parallèle à T dans deux grilles évitant T, par exemple) un vecteur propre
   entier de valeur 3, nul sur N[T], a-t-il une norme au-dessus de la borne d'Hermite de T ?
   - Il faut en outre une normalisation qui garantit une telle droite. Le lemme sans hypothèse est faux (section 7).
   - Premier essai : la méthode de comptage de C2 (Prop. 87) adaptée aux vecteurs portés par F, où R_T ⊕ E impose
     Ex = 0 et Rx = 3x.
2. **(P1)** Classifier les solutions de colonnes, puis trancher la partie signes par un argument par caractères sur
   ℤ₂⁶, avant tout gros SAT.
3. **(Proposition 3)** Recenser, pour chaque méthode du registre c = 3, l'usage du budget. Statuer sur les 14
   gabarits sans budget restants.
4. **(Théorème 1)** Pour c ≤ 2, le groupe critique K(G_T) contrôle le cadre lointain. Une condition sur K(G_T)
   peut-elle être forcée globalement, comme (τ | 7) = −1 au rang 37 (L23, A) ?
