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
