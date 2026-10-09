# Mandat B — réalisation globale simultanée (session LAB)

9 octobre 2026. Révision consultée : `amazing-source/conway99-c1`, branche `codex/c1-arithmetic-audit`, commit
`19ec316` (copie locale avec `RECHERCHE_ACTIVE_C1.md` modifié, non commité). Lus : `AGENTS.md`,
`RECHERCHE_ACTIVE_C1.md`, notes 94 §2, 95, 164, 191 (début), 223, 225, 226, 229.

## Résultat, en une phrase

**Une loi de parité globale, démontrée, nouvelle par rapport au dossier ; aucun candidat, noyau ni rang n'est
exclu par elle.** Ce n'est donc pas un résultat substantiel pour C1 au sens du mandat.

## 1. Énoncé

Soit Γ un graphe dans lequel toute arête est dans exactement un triangle et deux sommets à distance deux ont
exactement deux voisins communs (cas de tout srg(99,14,1,2) ; aussi des srg(243,22,1,2) et des géométries tordues
à 20, 39 et 42 sommets du dépôt). Le degré k est pair (les voisinages sont des couplages).

**Transport.** Pour v ∼ w, de troisième point t, et x ∈ N(v) ∖ {w, t}, on a x ≁ w ; soit π_vw(x) le voisin
commun de x et w autre que v. C'est une bijection N(v) ∖ {w,t} → N(w) ∖ {v,t}, d'inverse π_wv. On la prolonge par
l'identité sur {v, w, t} en Φ_vw : N[v] → N[w].

**Holonomie.** Pour une marche fermée γ = (v₀, v₁, …, v_m = v₀), ω(γ) ∈ F₂ est la parité de la permutation
Φ_{v_{m−1}v₀} ∘ … ∘ Φ_{v₀v₁} de N[v₀].

**Lemme 1 (ω est un morphisme).** ω ne dépend que de la classe de γ dans l'espace des cycles Z₁(Γ ; F₂) et y
est linéaire. *Preuve.* On ordonne chaque N[v] ; f(vw) est la parité de Φ_vw entre ensembles ordonnés, et
f(wv) = f(vw). Alors ω(γ) = Σ f(v_i v_{i+1}). Changer l'ordre de N[v] par une permutation impaire change f sur
toutes les arêtes en v, donc ne change pas la somme le long d'une marche fermée. ∎

**Lemme 2 (valeurs locales).**
- Pour une droite T = {u, v, w} : ω(T) est la parité de ρ_T = π_wu π_vw π_uv sur N(u) ∖ T, soit
  ω(T) ≡ c(T) (mod 2), c(T) = nombre de cycles transversaux du graphe proche G(T).
- Pour un quadrilatère Q = (v, a, w, b) : l'holonomie permute cycliquement {v, b, a} et agit sur les k − 2 points
  de N(v) ∖ {a, b} ; ω(Q) ≡ c(Q) (mod 2), c(Q) = nombre de cycles de cette action. Géométriquement, x ↦ x′ où
  l'on tourne autour de Q par quatre quadrilatères consécutifs (v,a,y,x), (a,w,z,y), (w,b,u,z), (b,v,x′,u).
- Forme matricielle : avec les lignes N(w) = (v, t, Y) et les colonnes N(v) = (w, t, X),
  A[N(w), N(v)] = [[1, 1, 1ᵀ], [1, 0, 0], [1, 0, Π]], Π matrice de π_vw, donc **dét A[N(w), N(v)] = −sgn(π_vw)**.
  La cochaîne f est, à une constante près, le signe d'un mineur 14×14 de A.

**Théorème (loi de parité).** Chaque arête vw est dans exactement k − 2 quadrilatères (un par x ∈ N(v) ∖ {w,t}).
Comme k − 2 est pair, la somme des bords de TOUS les quadrilatères est nulle dans Z₁(Γ ; F₂). Donc

    Σ_Q ω(Q) = 0,   c'est-à-dire : le nombre de quadrilatères Q avec c(Q) impair est pair.

Pour srg(99,14,1,2) : 2079 quadrilatères (nombre impair), 12 par arête. Le nombre de quadrilatères d'holonomie
impaire est pair ; celui des quadrilatères d'holonomie paire est impair, donc non nul.

Plus généralement, pour toute combinaison de triangles et de quadrilatères de bord nul modulo deux, la somme des
ω s'annule. Il y a 231 + 2079 = 2310 faces et le bord est de rang au plus 693 − 98 = 595 : **au moins 1715
relations linéaires indépendantes** entre les 2310 parités locales c(T), c(Q). Seule la relation « tous les
quadrilatères » est canonique ; les autres dépendent du graphe.

## 2. Contrôles (programme `holonomy_class.py`, quelques secondes, un processus)

| Graphe | diamètre deux | droites impaires | quadrilatères impairs | classe ω |
|---|---|---|---|---|
| grille 3×3 | oui | 0 sur 6 | 0 sur 9 | nulle |
| Clebsch (16,5,0,2), λ = 0 | oui | (pas de droite) | 0 sur 40 | longueur mod 2 |
| BvLS 243 | oui | 0 sur 891 | 0 sur 13 365 | nulle |
| 243 tordu | oui | 0 sur 891 | 0 sur 13 365 | nulle |
| non tordue t=2, 27 sommets | non | 0 sur 27 | 0 sur 81 | nulle |
| tordue t=2, 20 sommets | non | 20 sur 20 | 0 sur 60 | longueur mod 2 |
| tordue t=3, 42 sommets | non | 56 sur 56 | 0 sur 252 | longueur mod 2 |
| tordue t=3, 39 sommets | non | 0 sur 52 | **78 sur 234** | autre |

« Longueur mod 2 » : ω(γ) est la parité de la longueur de γ (toutes les droites impaires, tous les quadrilatères
pairs). Le transport s'étend tel quel à λ = 0 (`holonomy_mu2.py`) ; pour λ ≥ 2 ce n'est plus une bijection.

Dans tous les cas la somme de la cochaîne f reproduit la parité calculée directement sur chaque droite et chaque
quadrilatère, et le nombre de quadrilatères impairs est pair. Le cas à 39 sommets (78 impairs) est le seul où la
loi n'est pas vide ; il la confirme. Le 243 tordu a des holonomies très non triviales (types (1,1,3,15),
(1⁴,8,8), …) mais toutes paires.

## 3. Résultat antérieur le plus proche, et différence

- Note 94 §2 (« programme D », 25/09) : signes des holonomies de droites σ_L sur cinq géométries, conclusion
  « aucune loi ». Note 164 : la proposition « cocycle et holonomie » jugée déjà explorée sans contradiction.
- Note 95 (L7) : un comptage « chaque terme apparaît 12 fois, donc 0 ≡ 1 », mais seulement en un point de Hamming
  fixé par une involution.
- Différence effective : l'idée d'une classe de cohomologie figurait déjà dans la proposition évaluée en note 164.
  Ce qui est ajouté : (i) la classe explicite (signe du transport sur N[v]) et sa valeur sur les QUADRILATÈRES,
  absente du dossier ; (ii) le 2-cycle universel « tous les quadrilatères », qui donne une relation sans aucune
  hypothèse. Le « aucune loi » de la note 94 portait sur les droites seules, où il n'y a
  effectivement pas de relation universelle (la somme des bords des 231 droites est l'ensemble de toutes les
  arêtes, qui n'est pas nul).

## 4. Où la loi cesse d'être une conséquence des comptages et du spectre

C'est une congruence modulo deux sur des types de cycles de permutations. Aucune relaxation linéaire ou
semi-définie en fréquences de motifs ne la contient : elle distingue des configurations de mêmes marges. Elle
utilise que les MÊMES 693 arêtes portent chacune 12 quadrilatères.

## 5. Effet sur C1 : aucun pour l'instant, et pourquoi

- La loi est UNE équation sur F₂ (plus des relations non canoniques). Chaque ω(Q) dépend des quatre « murs »
  N(v), N(a), N(w), N(b), soit 48 sommets : bien au-delà des noyaux de 14 à 20 sommets. Je n'ai pas de formule
  de ω(Q) en fonction d'un type de noyau, donc pas de conséquence sur les 174 types.
- Énoncé exclu, faible : aucun candidat n'a tous ses quadrilatères d'holonomie impaire.
- **Sous-lemme attaqué, non résolu.** « Dans un graphe de diamètre deux de cette famille, ω est nulle ou égale à
  la classe longueur ; autrement dit tout quadrilatère a une holonomie paire et toutes les droites ont la même
  parité. » S'il était vrai, chacun des 2079 quadrilatères d'un candidat aurait un nombre pair de cycles de bande,
  et les 231 graphes proches auraient tous la même parité de cycles transversaux : une contrainte couvrante, sans
  rang. Les quatre graphes de diamètre deux disponibles le vérifient.
  **Obstacle précis :** (i) la géométrie tordue à 39 sommets (mêmes λ, μ locaux, diamètre > 2) a 78 quadrilatères
  impairs : aucune preuve locale n'est possible, il faut un argument utilisant le diamètre deux ; (ii) les quatre
  exemples sont très symétriques ; sur le 243 tordu les cycles pairs viennent par paires, ce qu'un automorphisme
  renversant la droite expliquerait (explication possible, non vérifiée). Ce n'est donc pas une indication
  fiable pour un graphe sans automorphisme. Ni preuve, ni contre-exemple.
- Essai lié, négatif (`minors_sign.py`) : dans la jauge où tous les mineurs d'arêtes dét A[N(v), N(w)] valent +1,
  les mineurs des paires NON adjacentes ont un seul signe sur la grille (+1) et sur BvLS (−64), mais les deux
  signes sur le 243 tordu (−64, −16, −8, −4, 0, +8). Il n'y a donc pas de « signe global » des mineurs à exploiter.
- Tentatives de seconde évaluation de ω, sans succès : (a) matrice 99×99 des mineurs dét B[N(v), N(w)] pour B
  positive. Elle est positive (compression de Λ¹⁴B) et porte sur les arêtes le signe de π_vw. Pour B = 7E₋₄ le
  terme d'arête vaut ±256/9 et le terme diagonal (32/9)·2²⁰ : rapport 2¹⁷, aucune contrainte de signe (de même
  pour A + cI, c ≥ 4). (b) Discriminants : sur une arête e, les 12 droites par ses extrémités (hors la droite de
  e) engendrent dans l'espace propre −4 un réseau de déterminant 12^{c_e}·carré, c_e = nombre de cycles à deux
  couches (identité vérifiée exactement sur 300 tirages). Cela relie une parité à une classe de carrés, mais en
  codimension 32 dans un espace de dimension 44 : aucune contrainte.

## 6. Remarques non revendiquées (probablement connues, cf. notes 191–192 « vecteurs triangulaires »)

Dans l'espace propre −4, avec ℓ_L = √7·E₋₄·1_L : ⟨ℓ_L, ℓ_L⟩ = 4 ; 0 si L et L′ se coupent ; 1 − j si elles sont
disjointes avec j arêtes transversales. Les sept droites par un point forment un repère orthogonal. Les 18
droites coupant une droite T ont pour matrice de Gram le laplacien du multigraphe quotient de G(T) par les
partenaires. Vérification par identité : Mᵀ(27I − 9A + J)M = 9(3I − L − C + J), C = L² − 5L − 18I.

## 7. Fichiers

- `holonomy_class.py` : calcul de f, des holonomies de droites et de quadrilatères, de la nullité de ω.
- `holonomy_mu2.py` : la même classe pour λ ≤ 1, avec le test « nulle / longueur / autre » sur tous les graphes.
- `minors_sign.py` : signes des mineurs dét A[N(v), N(w)] pour toutes les paires.
- Sorties reproduites dans le tableau du §2.

## 8. Suite du 9 octobre, 10:02 UTC : le sous-lemme n'a aucun appui hors symétrie

Cinquième graphe de diamètre deux, de nature différente : Gewirtz srg(56,10,0,2) (`gewirtz_test.py`). Les 630
quadrilatères sont pairs et la classe est « longueur mod 2 », alors que la loi de parité ne s'y applique même pas
(9 quadrilatères par arête).

**Mais cet accord s'explique entièrement par la symétrie.** En diamètre deux avec λ = 0, tout sommet autre que v
et ses voisins s'écrit [x, y]_v (le second voisin commun de x, y ∈ N(v)). Pour v ∼ w on a donc une permutation
canonique Ψ_vw de TOUS les sommets : v ↔ w, x ↔ π_vw(x), [x, y]_v ↦ [πx, πy]_w. Pour k pair, son signe est une
cochaîne de la classe (vérifié sur Gewirtz : la différence avec la cochaîne de Φ est un cobord). Cette cochaîne
est canonique, donc constante sur chaque orbite d'arêtes : dans un graphe transitif sur les arêtes la classe est
automatiquement nulle ou égale à la longueur. La grille et BvLS relèvent d'un argument analogue (graphes de
Cayley d'un groupe d'ordre impair, stabilisateur linéaire transitif sur les directions).

**Conclusion sur ce point.** Les cinq exemples de diamètre deux sont très symétriques et quatre d'entre eux sont
expliqués par leur symétrie ; seul le 243 tordu ne l'est pas par ces arguments. Pour λ = 1 la permutation Ψ_vw
n'est pas canonique (il faudrait apparier les droites sans prisme en v et en w), donc aucune cochaîne canonique.
Je n'ai aucune raison de croire le sous-lemme vrai pour un graphe sans automorphisme, et aucun exemple de ce
type n'existe pour le tester. **Je l'abandonne comme non décidable par les moyens disponibles.**

État final du mandat B dans cette session : la loi de parité du §1 est démontrée ; elle n'exclut rien.

## 9. Suite du 9 octobre, 10:40 UTC : la loi exacte (conjecturale) qui remplace le sous-lemme ; non démontrée

L'utilisateur a demandé de PROUVER le sous-lemme du §5. Résultat de la tentative : le sous-lemme tel qu'énoncé est
faux dans la famille générale, et il est remplacé par une formule précise, vérifiée sur neuf graphes, que je n'ai
pas su démontrer.

**Notation.** Pour une arête e = vw de troisième point t, le graphe « à deux couches » de e est le graphe induit
sur (N(v) ∪ N(w)) ∖ {v, w, t} : partenaires et couplage π_vw ; c'est une réunion de cycles de longueur 4ℓ. Soit
c_e leur nombre. Identité vérifiée : dét (A + I)[X ∪ Y] = (−3)^{c_e} si aucun ℓ n'est multiple de trois (0 sinon).

**Loi observée (conjecture).** Pour toute marche fermée γ,

    ω(γ) ≡ Σ_{e ∈ γ} c_e + κ·longueur(γ)   (mod 2),   κ ∈ {0, 1} constante du graphe.

Autrement dit la cochaîne de signe f est égale à c + κ à un cobord près. Conséquences :
- quadrilatère Q = (v, a, w, b) : c(Q) ≡ c_va + c_aw + c_wb + c_bv (mod 2) ;
- droite T = {u, v, w} : F(T) = c(T) + c_uv + c_vw + c_wu ≡ κ (mod 2) pour TOUTES les droites. F(T) est le nombre
  de faces de la carte Σ_T tracée sur G(T) (cycles transversaux et cycles à deux couches), et χ(Σ_T) = F(T) − 18.

**Vérification** (`two_layer_test.py`, `triinc_test.py`, test sur tous les cycles par arbre couvrant) :

| Graphe | n, k | valeurs de c_e | classe de f seule | f + c |
|---|---|---|---|---|
| grille | 9, 4 | 1 | nulle | cobord + 1 |
| t=2 non tordue | 27, 6 | 2 | nulle | cobord |
| t=2 tordue | 20, 6 | 1 | longueur | cobord |
| t=3 tordue (tri-incidence q=3) | 39, 8 | 1, 2, 3 | autre | cobord + 1 |
| t=3 tordue, 42 sommets | 42, 8 | 1 | longueur | cobord |
| tri-incidence q=5 | 93, 12 | 2, 3 | autre | cobord + 1 |
| tri-incidence q=7 | 171, 16 | 2, 3, 5 | autre | cobord + 1 |
| BvLS | 243, 22 | 10 | nulle | cobord |
| 243 tordu | 243, 22 | 4, 10 | nulle | cobord |

Les trois graphes de tri-incidence ont une holonomie de parité non triviale (« autre ») et des c_e de parités
mélangées ; leur groupe ne suffit pas à forcer le résultat (pour q = 7, les classes invariantes sous Z_57 forment
un espace de dimension 22). Le sous-lemme « tout quadrilatère est pair » y est FAUX ; ce qui est vrai est la formule.

**Ce n'est pas une identité locale.** Modèle abstrait des quatre murs d'un quadrilatère (`abstract_quad.py` :
partenaires et couplages tirés au hasard, seules les contraintes aux coins imposées) : c(Q) + Σ c_e est pair dans
9917 tirages et impair dans 10083, sur 20000. Si la loi est vraie, elle exclut donc la moitié des recollements
abstraits de quatre murs : ce serait une obstruction de réalisation au sens du mandat. Elle n'est pas démontrée.

**Réductions démontrées vers une preuve.**
1. Formule de Pfaffien : pour une orientation cyclique o des droites, f = c + d_o dans la jauge induite, où d_o(e)
   est le nombre de paires de partenaires aux extrémités de e orientées contre le parcours de leur cycle à deux
   couches. De façon équivalente d_o(e) est la parité de la distance de o aux orientations « anti-parallèles en e »
   (tout quadrilatère par e a ses deux côtés adjacents à e de sens opposés).
2. Liberté de jauge plus grande : pour une orientation ξ QUELCONQUE des 693 arêtes,
   Λ_ξ(vw) = #{p dans une classe de couleur du graphe à deux couches : ξ oriente p → partenaire(p)}
             + [ξ : t → w] + [ξ : t → v]
   a une classe indépendante de ξ. Démontrer la loi revient à exhiber, dans chaque graphe, une orientation des
   arêtes pour laquelle Λ_ξ est constante.

**Pistes de preuve essayées, toutes insuffisantes** (`parallel_orient.py`, `balanced_orient.py`,
`arc_coherence.py`) :
- orientation des droites parallèle (ou anti-parallèle) dans tout quadrilatère : existe sur six graphes, pas sur
  le 243 tordu ni sur le graphe à 42 sommets ;
- orientation « équilibrée » (nombre pair de côtés à contresens dans tout quadrilatère) : même échec ; là où elle
  existe, d_o est constante ;
- orientation des arêtes cohérente le long de tous les cycles à deux couches : n'existe que sur le graphe à 20
  sommets ;
- aucune orientation canonique locale de N(v) ne peut convenir (dans un graphe de Hamming une réflexion fixe v et
  renverse l'orientation) : la preuve, si elle existe, est globale.

**Autre essai sans suite** (`flip_zoo.py`) : la bascule BvLS → 243 tordu ne se laisse ni appliquer partiellement
ni combiner à deux droites parallèles ; pas de nouveau graphe de diamètre deux pour tester.

**Effet pour un candidat à 99 sommets, SI la loi est démontrée :** les 231 droites ont toutes la même parité de
F(T) ; chacun des 2079 quadrilatères vérifie c(Q) ≡ somme des quatre c_e. État : conjecture, neuf graphes.

## 10. Travail du 9 octobre après 11:16 UTC (consigne : aucun compte rendu sans exclusion d'un rang ou de C1)

Aucune exclusion à ce stade. Faits établis depuis le §9, à exploiter :

**10.1 Forme « transport apparié » de la loi.** Pour v ∼ w, T~_vw : N(v) → N(w) = « avancer de deux pas le long
des cycles à deux couches orientés » (x ↦ π(x′) pour le point d'entrée, x′ ↦ π(x′)′ pour le point de sortie ;
w ↦ t, t ↦ v). Elle envoie partenaires sur partenaires ; elle est définie à des permutations cycliques de droites
près, sans retournement. sgn(T~_vw) = sgn(Φ_vw)·(−1)^{c_vw+1}. L'holonomie des T~ est donc dans W(B₇) = 2⁷⋊S₇,
et la loi du §9 dit exactement : **son caractère « nombre de retournements » est trivial sur les marches paires**,
c'est-à-dire que la structure se réduit à W(D₇) (choix cohérent d'une classe de transversales de N(v) modulo un
nombre pair d'échanges). En diamètre deux, T~ se prolonge canoniquement en une permutation T^_vw de tous les
sommets (v ↦ w, [x,y]_v ↦ [T~x,T~y]_w), fonctorielle, et sgn(Ĥ) = χ_retournements·χ_permutation des droites.
`chart_transport.py` : T^ n'est pas proche d'un automorphisme, même sur BvLS.

**10.2 Le plus petit cas est localement rigide** (`local_quad_sat.py`, cadical, axiomes exacts sur le
quadrilatère et ses quatre murs, sommets supplémentaires libres). Valence 6 : 26 configurations abstraites des
quatre murs ; les 13 impaires sont UNSAT, et 10 des 13 paires aussi ; il en reste 3 (toutes paires). Valence 8 :
7 configurations tirées au hasard sur 8 sont UNSAT (4 impaires, 3 paires), 1 non décidée en 25 s. La parité y
est donc un sous-produit de contraintes locales bien plus fortes, dues à la petitesse des degrés ; cela
n'explique pas le cas des grandes valences (12, 16, 22), où la loi tient aussi.

**10.3 Voisinage d'un quadrilatère = ensemble étoilé pour −4 (propre à 99).** Un quadrilatère Q a 4·12 − 4 = 44
voisins extérieurs (40 voisins d'un seul sommet, 4 troisièmes points), et 44 est la multiplicité de −4.
(Note 172 compte ces 44 voisins ; elle n'utilise pas cette coïncidence.) Conséquences exactes, SANS hypothèse de
rang, pour S = N(Q) et G_S = 27I − 9A_S + J :
- G_S ⪰ 0, donc A_S − J/9 a toutes ses valeurs propres ≤ 3 (pour une boule de droite, cubique, la condition
  analogue est vide). Correction de Codex (11:28 UTC) à ma description des degrés : un sommet simple x a
  deg_S(x) = 5 − (nombre de troisièmes points adjacents à x) ; |E(S)| = 100 + t, t = 0, 1, 2 étant le nombre
  d'arêtes entre troisièmes points ; A_S a les valeurs propres −1, −1, +1 forcées (vecteurs Bᵀz, z de somme
  nulle sur Q). La condition est satisfaisable : `quad_ball_psd.py` trouve une structure qui la vérifie ;
- dét G_S = 3⁸⁶·(7^{(45−r)/2}·m_Q)², m_Q = indice du réseau engendré par les 44 projections ; donc
  Δ(Q) := 9·dét(3I − A_S) + 1ᵀ adj(3I − A_S) 1 est un carré parfait divisible par 7^{45−r} ≥ 49, à tous les rangs ;
- si Δ(Q) ≠ 0, les 44 projections forment une base de l'espace propre : les 4 sommets de Q s'écrivent
  q_v = −(7/24)ΣW_v + (1/12)(ΣW_a + ΣW_b) − (1/24)ΣW_w, et chacun des 51 sommets lointains f est déterminé
  par son ombre s_f (8 points, deux par mur) avec les conditions de Green EXACTES sur Q :
  (1 − 9s_f)ᵀ G_S⁻¹ (1 − 9s_f) = 28 et (1 − 9s_f)ᵀ G_S⁻¹ (1 − 9s_g) ∈ {1, −8}.
  C'est l'analogue sans rang de la complétion binaire des notes 230 et 232 : le graphe est déterminé par la
  structure des quatre murs (quatre couplages, deux graphes entre murs opposés) et 51 ombres.
- Même fait pour une « griffe » (v ; a, b, c) : (N[v] ∪ N[a] ∪ N[b] ∪ N[c]) privé des quatre centres a 44 points.
- Variante modulo 7 : rang₇ Gram(Q ∪ N(Q)) ≤ r − 1 ≤ 42 pour 48 sommets, dont 4 relations automatiques.
Non exploité : énumérer les structures de quatre murs reste hors de portée ; aucune exclusion.

**10.4 Sans suite.** Le caractère quadratique de τ(G(T)) modulo 7 est indépendant de la parité du nombre de faces
(`tau_parity_test.py`, 6000 graphes proches aléatoires).

**10.5 Deux vérifications sans gain pour le coût de la première étoile de LAP (11:28 UTC).** (i) La relation réelle
« somme des résidus d'une étoile = 0 » donne n_fᵀH⁺d_x = 17/6 + (G n_f)_x, qui est une identité pour toute ombre
contenant x (H⁺d_x = 4e_x + G e_x − (1/3)·1_couche(u) − (1/12)·1) : aucun filtre unaire. (ii) Le Gram résiduel de
m sommets lointains est positif de rang ≤ 8 : les égalités réelles exactes ne commencent qu'à 9 sommets.
En revanche le quadrilatère (u, v, y, x) d'une arête transversale x–y donne un test exact sans rang pour DEUX
étoiles adjacentes : N(Q) = (couche u ∖ x) ∪ (couche v ∖ y) ∪ {w, voisins de x et y dans la couche w} ∪ étoile(x)
∪ étoile(y), soit 44 sommets ; les dix points restants de la couche w doivent alors vérifier 10 + 45 égalités
rationnelles. Transmis à LAP.


## 11. 9 octobre, 12:28 UTC : la « loi exacte » du §9 est FAUSSE en général ; ce qui reste

**Réfutation.** Le produit cartésien de deux graphes de la famille (toute arête dans un seul triangle, deux sommets à
distance deux ont exactement deux voisins communs) est dans la famille. Pour une droite T du premier facteur, le graphe
proche dans le produit est G₁(T) plus k₂/2 prismes, donc F(T) = F₁(T) + 5k₂/2. Une loi universelle « F de même parité sur
toutes les droites » forcerait κ + k/2 à être le même pour tous les graphes de la famille. Or κ + k/2 vaut 1 pour huit des
neuf graphes du §9 et 0 pour la géométrie tordue à 42 sommets. Vérification directe (`product_test.py`) : sur
t3_twisted_42 × K₃ (126 sommets, valence 10), t2_twisted × t3_twisted_42 (840 sommets, **valence 14**) et
grille × t3_twisted_42, ni f + c ni f + c + 1 n'est un cobord ; les droites ont les deux parités (par exemple 1120 et 840).
Je cesse donc de chercher à démontrer un énoncé faux. Les voies de preuve du §9 et du §10.1 (réduction à W(D₇),
transports appariés) portaient sur cet énoncé : elles sont closes.

**Ce qui reste vrai sur tous les graphes disponibles** (`product_quad_test.py`) : pour tout quadrilatère Q,
(f + c)(Q) = 0, c'est-à-dire c(Q) ≡ c_va + c_aw + c_wb + c_bv (mod 2). Les quadrilatères et les droites engendrent tout
l'espace des cycles, et la dimension d du quotient (cycles) / (quadrilatères) est :

| graphe | cycles | quadrilatères | d |
|---|---|---|---|
| t2_twisted (20) | 41 | 40 | 1 |
| H(3,3) (27) | 55 | 52 | 3 |
| t3_twisted (39) | 118 | 117 | 1 |
| t3_twisted_42 | 127 | 125 | 2 |
| grille 3×3 | 10 | 8 | 2 |
| BvLS (243) | 2431 | 2420 | 11 |
| 243 tordu | 2431 | 2429 | 2 |

La classe [f + c] est donc un élément de Hom(cycles / quadrilatères, F₂) ; « F(T) de parité constante » n'est vrai que
lorsque d = 1 ou par accident. Statut de la loi des quadrilatères : conjecture. Les produits ne la mettent pas à l'épreuve
(elle se transmet des facteurs au produit : holonomie d'un quadrilatère mixte triviale, c_e des côtés opposés égaux).
Appui réel : les neuf graphes de base et le cas de valence 6 (SAT local). Recherche de membres non construits à la main
(`random_family_sat.py`, cadical) : en valence 6 seuls 20 et 27 sommets apparaissent ; en valence 8, 39 sommets retrouvé,
42 à 48 non décidés en une minute.

**Conséquence pour un graphe à 99 sommets, si la loi des quadrilatères est vraie :** une condition d'un bit sur chaque
configuration à quatre murs (48 sommets), et F(T) ≡ F(T') dès que T + T' est somme de quadrilatères. Rien n'est exclu.


## 12. 9 octobre, 13:09 UTC : dossier externe « Convergences » (piste « couverture et cycles longs ») ; rien d'exclu

Source : `Desktop/c1-imports/2026-10-09-convergences/DOSSIER_C1_CONVERGENCES/DOSSIER_C1_INTEGRE.md`, signalé par Codex
(message du pont reçu pendant ce travail) comme fourni par l'utilisateur. Lu comme donnée ; aucun de ses programmes n'a été exécuté.
Sa piste « Claude 1 » : le cas sans cycle de transport de longueur quatre, les rubans longs, une loi propre à 99.

**Lecture du transport comme flot géodésique (mienne).** Pour un sommet x, soit s_x la réflexion ponctuelle de la carte
de x : elle fixe x, échange les deux voisins de chaque droite par x, et envoie le second voisin commun [u, v] de deux
voisins non adjacents sur [u', v']. Le transport de non-arêtes du dossier est exactement : les centres consécutifs d'un
cycle vérifient c_{i+1} = s_{c_i}(c_{i-1}). Un cycle de transport est donc une « géodésique » fermée par réflexions
successives, partant d'un couple ordonné non adjacent ; dans un quotient de Hamming c'est une droite affine de direction
de poids deux, de période 3 (les grilles). Il y a 99 × 42 = 4158 triplets (centre, paire antipodale), autant que de
non-arêtes. Les s_x ne sont pas des automorphismes (sinon C1 serait faux) et la loi x ▷ y = s_x(y) n'est pas
autodistributive.

**Données** (`transport_cycles.py`, `antipodal_matrix.py`) : périodes des géodésiques — grille 3 ; t2_twisted 4, 6 ;
t3_twisted 6, 13, 39 ; t3_twisted_42 4, 6, 8 ; BvLS 3 ; 243 tordu 3, 6, 8, 9, 16. Le multigraphe antipodal
(nombre de centres où deux sommets sont antipodaux) vaut le complémentaire dans la grille et BvLS, mais prend les
valeurs 0, 1, 3, 4 sur les non-arêtes du 243 tordu et ne commute pas avec A. Aucune loi universelle sur les périodes ni
sur ce multigraphe ; pas de minoration du nombre de cycles de longueur quatre. Rien d'exclu.

**Remarque non exploitée** (à ne pas présenter comme résultat) : la série thêta harmonique de degré 2 à valeurs
tensorielles, Σ_y (y yᵀ − |y|²E/44) q^{|y|²/2} sur L1 et son analogue sur M, est une forme parabolique de poids 24 sur
Γ₀(7) (dimension 15) qui s'annule à l'ordre 7 à l'infini ; les tenseurs d'écart au 2-design de toutes les couches de L1
et de M sont donc combinaisons linéaires d'au plus neuf d'entre eux. Les couches « algébriques » (droites, différences
de sommets) sont des 2-designs ; l'écart mesure l'inhomogénéité du graphe. Sans couche connue non homogène, aucune
contradiction.


**Addendum du 9 octobre, 13:19 UTC : rubans propres de longueur au plus six.** Appelons propre un cycle de transport de
longueur m dont les 3m points (a_i, b_i, c_i) sont distincts et induisent exactement le graphe 4-régulier
H = L(D), D étant l'échelle circulaire ou l'échelle de Möbius à 2m sommets. Les valeurs propres de H sont μ + 1 (μ valeur
propre de D) et −2 ; la plus grande valeur propre non principale vaut 2 cos(2π/m) + 2 dans les deux cas, portée par un
vecteur de somme nulle. La positivité de 3I − A_H + J/9 (bloc de 7E) exige donc cos(2π/m) ≤ 1/2 :

    un ruban propre a m ∈ {3, 4, 5, 6} ;  m = 3 et m = 6 sont les cas d'égalité (valeur propre 3 exacte).

Dans les cas d'égalité, le vecteur propre prolongé par zéro est un vecteur propre de A pour la valeur 3 porté par le
ruban (m = 3 : les grilles ; m = 6 : deux vecteurs entiers de support ≤ 18). Contrôle numérique des deux fermetures pour
m = 3..9 dans le terminal (m ≥ 7 : valeur propre minimale −0,247 ; −0,414 ; −0,532). Le dossier externe donnait
𝒟(H) = 9m² − 60m + 99 ≥ 0, qui ne borne pas m. Conséquence : tout cycle de transport de longueur ≥ 7 comporte des
identifications de points ou des arêtes supplémentaires (c'est le cas des périodes 8, 9, 16 du 243 tordu : 4, 9, 16
paires de centres adjacentes). Pour m = 4 le ruban est toujours propre (dossier). Rien d'exclu ; pas de minoration du
nombre de cycles courts.


**Addendum du 9 octobre, 13:25 UTC : pas de ruban propre de longueur six ; pas de segment propre à cinq centres.**

(a) *Ruban fermé propre de longueur 6 : impossible dans un srg(99,14,1,2)* (`ribbon6_boundary.py 6 cylinder|moebius`,
certificats exacts `ribbon6_*_certificate.json`). Dans le cas d'égalité m = 6, les deux vecteurs propres de A_H pour la
valeur 3, de somme nulle, prolongés par zéro sont des vecteurs propres de A ; donc le masque S ⊂ H de tout sommet
extérieur est une coclique équilibrée (somme nulle pour ces deux vecteurs). Avec « chaque point de H a 10 voisins
extérieurs » et « deux points non adjacents p, q de H ont 2 − |N_H(p) ∩ N_H(q)| voisins extérieurs communs », les
multiplicités des 113 (cylindre) ou 111 (Möbius) masques admissibles vérifient 135 égalités linéaires sans solution
rationnelle positive : vecteur de Farkas exact vérifié (y·colonne ≥ 0 pour tout masque, y·second membre = −132).
Contrôles du même programme : m = 3 Möbius (la grille) force 90 masques singletons ; m = 4 et m = 5 sont faisables.
Donc : **un ruban fermé propre a m ∈ {3, 4, 5}.**

(b) *Segment ouvert propre : au plus quatre centres.* Pour w centres consécutifs c_1..c_w et les paires p_1..p_(w+1)
(3w + 2 points distincts, aucune arête hors des 2w droites), la plus petite valeur propre de 3I − A_H + J/9 vaut
+0,969 ; +0,595 ; +0,559 ; +0,186 pour w = 1, 2, 3, 4 et −0,128 pour w = 5 (puis décroît). Donc, le long de toute
géodésique de transport, **toute fenêtre de cinq centres consécutifs (17 rôles) contient une identification de deux
rôles ou une arête supplémentaire**. Le vecteur propre négatif est antisymétrique le long du ruban : les réparations
par une seule arête relient les deux moitiés (16 arêtes possibles, par exemple c_1–c_5, a_2–a_5, c_2–c_4 au bord), et
35 identifications simples conviennent (par exemple c_1 = c_5, a_1 = a_6 : c'est la fermeture en cycle de longueur 5).
C'est une loi locale sur les identifications demandée par le dossier externe ; elle ne borne pas la longueur des cycles
et n'exclut ni rang ni C1.


**Addendum du 9 octobre, 13:52 UTC : fenêtres de cinq centres réparées par UNE relation** (`support_masks.py window5`,
indication : programmes linéaires flottants, pas de certificat exact). Le test est celui de la note 222 de Codex pour un
support quelconque : masques d'un sommet extérieur filtrés par les axiomes locaux et par les deux compléments de Schur
exacts, puis système des multiplicités (degrés extérieurs, voisins communs extérieurs exacts, total 99 − |H|).
Classes sous l'échange des deux brins et le retournement.
- Une arête supplémentaire : 34 classes ; 14 violent les axiomes locaux, 13 ne rétablissent pas la positivité, 6
  échouent au système des multiplicités (a2–a5, a2–b5, a2–c4, a2–c5, c1–c4, c2–c4) ; **seule c1–c5 passe**.
- Une identification de deux rôles : 34 classes ; 23 locales, 1 non positive, 1 échoue (c1 = c4) ; **neuf passent** :
  a1 = a5, a1 = a6, a1 = b5, a1 = b6, a1 = c4, a1 = c5, a2 = b5, a2 = c5, c1 = c5.
Lecture : dans toute fenêtre de cinq centres d'une géodésique, ou bien les centres extrêmes sont adjacents, ou bien
deux rôles éloignés coïncident (dix formes), ou bien il y a au moins deux relations supplémentaires. Les contraintes
propres au transport au-delà des axiomes locaux (par exemple le second voisin commun des paires extrêmes) ne sont pas
toutes imposées dans ce test. Cela ne borne pas la longueur des cycles et n'exclut rien.
