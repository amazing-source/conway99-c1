# 125 — Cycles courts des graphes de droites : Σ_L c₄(G(L)) = S + 3P ; à P = S = 0, maille ≥ 5, seuls les profils connexe et (6,6)

*26/09, nuit. C1, porte I_x (mathématiques pures). DÉRIVÉ = preuve écrite ; les seuls calculs sont des contrôles exacts
d'énoncés dérivés à la main, sur les géométries tordues de data/ et par énumération de composantes. Aucun solveur.
Relu contre notes/99, 109, 114 et 123 : l'identité du §2 n'y figure pas.*

## 0. Résumé
| énoncé | statut |
|---|---|
| un 4-cycle de G(L) est soit un Z₂ centré en un point de L (deux événements S), soit le carré d'un prisme dont un barreau est une arête de L | DÉRIVÉ |
| Σ_L c₃(G(L)) = 2P (F1) et **Σ_L c₄(G(L)) = S + 3P** | DÉRIVÉ ; contrôle exact sur les 3 géométries tordues |
| avec L15 et L18 (S ≤ n₃ = 4158 − 3P) : **Σ_L c₄(G(L)) ≤ 4158** ; à P = 0, **S = Σ_L c₄(G(L))** | corollaire |
| critère exact de maille ≥ 5 pour une composante de G(L), en termes de (τ_u, τ_ū, σ_U) | DÉRIVÉ ; énumération 96/96 et 46 080/46 080 |
| **une composante à 4 étiquettes par couche contient toujours un cycle de longueur ≤ 4** (groupe de Klein) | DÉRIVÉ ; énumération : 0 sur 96 |
| à P = S = 0 : tous les G(L) ont maille ≥ 5 ; **profils (4,4,4) et (4,8) exclus** ; restent connexe et (6,6) | DÉRIVÉ |
| (6,6) à P = S = 0 : 288 composantes étiquetées à maille ≥ 5, 15 types ; non exclu | énumération exacte |
| **correction de la correction b231c36** du JOURNAL, et la strate (4,4,4) de d7cd060 est vide à S = 0 | §6 |

## 1. Les 4-cycles de G(L)
Soit L une droite et N(L) = ⊔_{p∈L} X_p. Tout sommet de N(L) a exactement un voisin dans chaque couche : dans sa propre
couche X_p, c'est son partenaire (troisième point de la droite par p) ; dans une autre couche X_q, c'est le second voisin
commun avec q. On classe les 4-cycles n₀n₁n₂n₃ de G(L) selon la suite des couches.
- Deux arêtes consécutives mènent à deux couches différentes, sinon les deux extrémités coïncident.
- **(i) Aucune arête interne : impossible.** Trois couches consécutives seraient distinctes, et la quatrième devrait
  différer des trois.
- **(ii) Une arête interne**, n₀n₁ dans X_p, avec n₂ ∈ X_q et n₃ ∈ X_r ({p, q, r} = L).
  - C'est une copie de Z₂ de centre p, construite sur les droites L et {p, n₀, n₁}.
  - Donc n₃ = σ_p(n₂) et n₂ ~ n₃ : ce sont les deux événements S (p, n₂) et (p, n₃) de L18.
  - Réciproquement, un événement S (p, E) avec E ∈ N(L) donne un tel 4-cycle.
- **(iii) Deux arêtes internes opposées**, dans X_p et X_q (p ≠ q). Les droites {p, n₀, n₁} et {q, n₃, n₂} forment un
  prisme de barreaux pq, n₁n₂, n₀n₃, et le barreau pq est une arête de L. Réciproquement, un prisme et l'un de ses
  barreaux donnent un tel 4-cycle dans G(droite du barreau).
- (iv) Trois arêtes internes ou plus : impossible (deux seraient consécutives).

## 2. L'identité
- Un événement S (p, E) avec E ∈ Γ₂(p) a ses deux étiquettes en p sur deux droites distinctes par p. E est dans N(L)
  exactement pour ces deux droites. Donc Σ_L S(L) = 2S, où S(L) compte les événements (p, E) avec p ∈ L et E ∈ N(L).
- Chaque 4-cycle de type (ii) porte deux événements. D'où Σ_L c₄^{(ii)} = S.
- Chaque prisme a trois barreaux, chacun sur une seule droite. D'où Σ_L c₄^{(iii)} = 3P.
- **Σ_L c₄(G(L)) = S + 3P.** De même, Σ_L c₃(G(L)) = 2P : les triangles de G(L) sont les points fixes de l'holonomie
  (F1).
- **Contrôle exact** (`code/x30_c4_line_graphs_vs_S.py`, code indépendant de rooted.py). Les axiomes locaux suffisent,
  et G(L) y est cubique.

| géométrie | P | S | Σ c₃ | Σ c₄ |
|---|---|---|---|---|
| tordue t = 2 (20 sommets) | 0 | 120 | 0 | 120 |
| tordue t = 3 (39) | 39 | 0 | 78 | 117 |
| tordue t = 3 (42) | 0 | 336 | 0 | 336 |

- **Corollaire.** Par L15 et L18, n₃ = 4158 − 3P et S ≤ n₃. Donc 3P ≤ Σ_L c₄(G(L)) ≤ 4158, soit en moyenne au plus
  18 quatre-cycles par droite.
- **À P = 0, la seconde variable libre d'ordre 7 est le nombre total de 4-cycles des 231 graphes cubiques G(L).**

## 3. Critère de maille ≥ 5 pour une composante
On se place dans le repère de x, avec L = {x, u, ū}, σ = σ_U et une composante de G(L) d'ensemble d'étiquettes X_C.
Lus dans ce repère :
- l'événement S en u sur la droite L s'écrit σ(w) = τ_u(w). C'est exactement le cas où le second voisin commun r_v de
  {u,v} et {ū,v} est la u-paire {u, τ_u v} (avec w = τ_u v) ;
- l'événement S en ū s'écrit σ(v) = τ_ū(v), c'est-à-dire r_v = {ū, τ_ū v} ;
- l'événement S en x s'écrit σ(v) = v̄.

**G[C] a une maille ≥ 5 si et seulement si :**
1. τ_u et τ_ū évitent les mates (pas de prisme de barreau xu ou xū) ;
2. σ(v) ∉ {v, v̄, τ_u(v), τ_ū(v)} pour tout v (pas de triangle, pas d'événement S en x, u, ū) ;
3. τ_ū(σ(w)) ≠ σ(τ_u(w)) pour tout w (pas de prisme de barreau uū ; c'est (c) de notes/123).

Contrôle par énumération directe de la maille (`code/x30b_component_girth_criterion.py`) : 96/96 composantes à
2 classes et 46 080/46 080 à 3 classes, 0 désaccord.

**Conséquence locale de S = 0.** En tout sommet x et pour toute classe U, σ_U(v) ∉ {v̄, τ_u(v), τ_ū(v)}. P = 0 ajoute
σ_U(v) ≠ v et (c). Chaque σ_U évite donc 4 valeurs sur 12.

## 4. Lemme : une composante à 4 étiquettes par couche a un cycle de longueur ≤ 4
X_C = A ∪ B (deux classes). Supposons G[C] de maille ≥ 5.
- Par 1, τ_u et τ_ū sont des couplages A ↔ B.
- Par 2, pour v ∈ A, σ(v) ∈ B ∖ {τ_u v, τ_ū v}. Donc τ_u(v) = τ_ū(v), et σ(v) = M̄(v), où M̄ est l'autre couplage A ↔ B.
  De même pour v ∈ B. Donc τ_ū = τ_u et σ = M̄.
- Les trois couplages parfaits de K₄ (mate, τ_u, M̄) forment le groupe de Klein. Ils commutent, donc
  τ_u(M̄ w) = M̄(τ_u w), ce qui contredit 3. ∎

C'est la forme conceptuelle du lemme (4,4,4) du JOURNAL (d7cd060), relu par « structures ». Là, S = 0 était imposé en
x seulement, et chaque étiquette v donnait r_v ∈ P_u ∪ P_ū. **C'est exactement un événement S en u ou en ū pour chacune
des 12 étiquettes.** Cela fait au moins 12 quatre-cycles dans G(L).

## 5. À P = S = 0
- Tous les G(L) sont de maille ≥ 5 (§2).
- Aucune composante n'a 4 étiquettes par couche (§4). **Les profils (4,4,4) et (4,8) sont exclus.** Les composantes à
  2 étiquettes l'étaient déjà (boucle de τ). Restent le profil connexe et le profil (6,6).
- **(6,6).** Composantes à 3 classes et maille ≥ 5 : 288 étiquetées, 15 types sous les 48 renumérotations qui
  préservent les mates (`code/x30c_comp66_girth5_orbits.py`).
  - Les σ ont pour types de cycles [3,3], [6], [2,2,2] ou [2,4].
  - Dans 8 types, τ_ū = τ_u ; dans 4 types, ils ont 2 arêtes communes ; dans 3 types, aucune.
  - Un type a maille 6 (graphe cubique à 18 sommets).
  - Non exclu : il faut l'analyse du lointain (équilibre : chaque lointain voit 3 points de chaque composante ; lemme E :
    chaque lointain intra-composante y a exactement un voisin de plus).

## 6. Corrections du JOURNAL
- **b231c36 (« maille ≥ 5 » déclarée fausse).** Les 4-cycles d'holonomie invoqués, σ_U(τ_u(v)) = v ou
  τ_ū(v) = σ_U(v), sont des événements S en u ou en ū (§3). Or S est global (L18). **À P = S = 0, l'énoncé initial
  « maille ≥ 5 » était juste.** La correction lisait S = 0 comme une condition en x seulement. Seul survit le constat
  suivant : sous S = 0 imposé en x seulement, ces 4-cycles sont permis.
- **d7cd060 (strate (4,4,4), « cohérente aux niveaux 1 et 2 »).** Elle est vide à S = 0 global (§4). Son contenu reste
  valable sous S = 0 en x seulement, mais c'est alors une strate à S ≥ 12.

## 7. Portée
- L'identité rend S géométrique. Le bord S = 0 du polygone d'ordre 7 est exactement « tous les graphes de droites sont
  de maille ≥ 5 ». Les strates rigides à P = 0 y vivent, et elles s'y réduisent au seul profil (6,6).
- Pour S > 0, rien n'est exclu ici. À P = 0, une droite seule donne S ≥ c₄(G(L)), puisque S(L) = 2c₄(G(L)) et
  2S = Σ_L S(L). Une droite (4,4,4) coûte donc au moins 3 à S (un 4-cycle par composante), et au moins 12 si S est nul
  en x.
- À vérifier : les échantillons « S = 0 » de notes/117-118 imposaient-ils les conditions 2 en u et en ū
  (σ_U(v) ≠ τ_u(v), τ_ū(v)), ou seulement σ_U(v) ≠ v̄ ?
