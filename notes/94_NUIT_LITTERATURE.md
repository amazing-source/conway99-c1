# 94 — Nuit du 24 au 25/09 : k ≥ 2, parités, littérature lue en texte intégral

*Consigne : 8 h de travail autonome, non-existence, recherche bibliographique en largeur et en profondeur (textes
complets, pas des résumés). Rien de lourd sur le portable, pas d'agents.*

## 1. L19 bis : k ≥ 2 (preuve à la main)
**Énoncé.** rank₇(A − 3I) ≥ 16 ; donc k = rank₇(A − 3I) − 15 ≥ 1 et, k étant pair (L2/L4), **k ≥ 2**. Le cas
favorable de L19 (k = 0 : U_x/7 d'ordre fini, congruences en chaque sommet) n'arrive jamais.

**Preuve.** Soit x un sommet et B₁ = {x} ∪ Γ(x) (15 sommets). Le bloc principal de A − 3I sur B₁ est celui du
moulin F₇ (7 triangles de sommet commun x) : polynôme caractéristique (t − 1)⁶(t + 1)⁷(t² − t − 14), et
det(A_{B₁} − 3I) = 2²³ ≢ 0 (mod 7) (vérifié par sympy). Les 15 lignes de A − 3I indexées par B₁ sont donc
indépendantes mod 7. Si le rang valait 15, elles engendreraient tout l'espace des lignes mod 7.
Restreignons aux colonnes de X = Γ₂(x), identifié aux 84 paires non mates {a, b} d'étiquettes de Γ(x) (μ = 2). La
ligne de x y est nulle ; celle de a ∈ Γ(x) est l'indicatrice des paires contenant a. Une combinaison Σ c_v L_v y vaut
donc f({a, b}) = c_a + c_b (« additive en étiquettes »).
Soit y ∈ X, d'étiquette {a, b}. Sur X, sa ligne vaut −3 en y, 1 en ses 12 voisins dans X (a', b' sur les droites ya,
yb, et les 10 points de ses 5 droites intérieures), 0 ailleurs (71 paires). Soit Z le graphe sur les 14 étiquettes
dont les arêtes sont les 71 paires où f doit s'annuler.
*Chaque étiquette c est dans au plus 2 des 13 paires exclues* : si c ∈ {a, b}, disons c = a, les sommets de
{y} ∪ (Γ(y) ∩ X) adjacents à a sont y et l'unique voisin commun de a et y ; si c ∉ {a, b}, alors c ≁ y et ces sommets
sont des voisins communs de c et y, au plus μ = 2. Donc chaque étiquette c a au moins 10 voisins dans Z (parmi ses
12 non-mates). Parmi ces ≥ 10 voisins, il y a au moins C(10,2) − 5 − 13 = 27 paires non mates non exclues, donc un
triangle {c, u, w} de Z : c_c + c_u = c_u + c_w = c_c + c_w = 0 donne 2c_c = 0, c_c = 0 (7 impair). Ainsi toutes les c
sont nulles, f ≡ 0, alors que f(y) doit valoir −3 ≢ 0. La ligne de y n'est pas dans l'espace engendré. ∎

**Portée.** On a désormais 2 ≤ k ≤ 30, k pair. L19 reste vrai, mais son cas tranchant (k = 0) est vide. Le programme
C de ChatGPT (« comprendre k ») ne mordrait que si l'on pouvait prouver k petit (≤ 4, disons), et rien ne l'indique : un
Γ « générique » aurait k = 30.

## 2. Programme D (parités d'holonomie) : pas de loi (`code/parity_probe.py`)
Pour chaque droite L et chaque point x ∈ L, l'holonomie σ_L est la permutation des 12 étiquettes de N(x) \ L obtenue
en faisant le tour de L (b → voisin dans N(a) → voisin dans N(ā) → voisin dans N(x)). Relevé (t = nombre de points
déplacés, signe de la permutation) sur toutes les géométries disponibles :

| géométrie | droites | (t, signe) | produit des signes par sommet |
|---|---|---|---|
| tordue t = 2 (20 sommets) | 20 | (4, −1) × 20 | −1 partout |
| tordue t = 3 (39 sommets) | 52 | (4, +1) × 39, (6, +1) × 13 | +1 |
| tordue t = 3 (42 sommets) | 56 | (6, −1) × 56 | +1 |
| srg(9,4,1,2) | 6 | (0, +1) | +1 |
| BvLS (243) | 891 | (0, +1) | +1 |

Le signe et t ne dépendent pas du point de base choisi sur L (vérifié). Mais aucune loi : t = 6 donne +1 dans la
géométrie à 39 sommets et −1 dans celle à 42, t = 4 donne −1 (20 sommets) et +1 (39 sommets). Aucune contrainte de
parité locale ni globale n'en sort.

## 3. Littérature lue en texte intégral
### 3.1 Makhnev 1988 : notre L1 était connu
A. A. Makhnev, *О сильно регулярных графах с λ = 1*, Mat. Zametki 44(5) (1988) 667–672 (mathnet.ru, PDF complet).
Condition (∗) : deux triangles reliés par au moins deux arêtes le sont par exactement trois, c'est-à-dire **Γ non tordu**
(n₃ = 0). Théorème 1 : un srg à λ = 1 vérifiant (∗) a μ ≤ 3, ou bien est (27, 10, 1, 5). Théorème 2 : ni (99,14,1,2) ni
(115,18,1,3) ne vérifient (∗). Preuve par le « graphe des triangles » Λ (triangles reliés par 3 arêtes) : à partir d'un
triangle Δ, Λ₀ = {Δ} ∪ Λ₁ ∪ Λ₂ serait un srg(33,12,1,6) vérifiant (∗), exclu par le théorème 1.
**Conséquence.** L1 (« Γ est tordu ») est le théorème 2 de Makhnev (1988), avec une autre preuve. Il faut le lui
créditer partout (fait : 30_LEMMES, rapport). Notre preuve (par la structure enracinée) reste valable et indépendante.
Reimbayev (arXiv « hexagons », 2024) conjecture un nombre minimal d'hexagones qui équivaut à (∗). La conjecture
entraînerait donc la non-existence via Makhnev. Elle n'est pas démontrée.

### 3.2 Wilbrink–Brouwer 1983, srg(57,14,1,4) : la méthode et pourquoi elle ne passe pas à 99
Texte complet : rapport CWI ZW121 (1978), ir.cwi.nl/pub/6822/6822D.pdf. Trois outils :
1. **Lemme de variance.** Pour F induit (N sommets, degrés d_i), x_j = nombre de sommets hors de F ayant j voisins
   dans F : x₀ + Σ_{j≥3} C(j−1, 2)·x_j = c(F) ≥ 0, avec égalité ssi tout sommet extérieur a 1 ou 2 voisins dans F.
   Pour srg(99,14,1,2), **c(F) = 99 + N(N − 16) − ½ Σ d_i(d_i − 2)** (dérivé et vérifié : grille 3×3 : c = 0, c'est
   L5 ; prisme : c = 30 ; grille moins une arête : c = 5 ; deux grilles ayant exactement une droite commune : c = 0,
   donc aucune arête entre leurs parties propres ; tout graphe 4-régulier induit à 10 sommets aurait c = −1, il est donc interdit).
2. **Borne de Hoffman et design.** Coclique ≤ 15 à 57, avec égalité ⇒ 2-(15,5,4). À 99, coclique ≤ 22 ; si elle est
   atteinte, 2-(22,4,2) à 77 blocs (chaque sommet extérieur a exactement 4 voisins dedans). Rien ne force son
   existence.
3. **Design divisible local.** À 57, Γ(∞) = 7K₂ et les blocs Γ(z) ∩ Γ(∞) sont de taille μ = 4 : GD[4,3,2;14], dont la
   combinatoire (tiroirs : 42 blocs contre C(7,4) = 35 quadruples de groupes) conclut.
**Pourquoi rien ne passe.** (i) À 57 le prisme est *tendu* (c = 0) et engendre une 15-coclique, ce qui ramène au cas
du design. À 99, c(prisme) = 30 : aucune contrainte. (ii) La coclique de Hoffman n'est pas forcée. (iii) μ = 2 : les
« blocs » locaux sont les 84 paires non mates, chacune exactement une fois. Le design local est trivial, l'argument
des tiroirs n'a rien à mordre. L'analogue de (A) à 99 (points de Δ sans voisin dans deux groupes) donne 40 points et
x₀ = x₂ + 4 : pas de contradiction.

### 3.3 Reimbayev 2025, srg(19,6,1,2) sans valeurs propres (arXiv:2511.06569)
Argument enraciné sur une droite L = {a, b, c} : A, B, C = voisins propres, W = points à distance 2 de L. Couplages
parfaits A–B, B–C, C–A (μ = 2), leur composée est l'holonomie de L. À t = 2 : |W| = 4, pas de triangle transversal
(comptage des 19 droites), 12 « échelons lointains » (arêtes transversales dont le triangle a son sommet dans W) pour
4 sommets de W portant chacun ≤ 3 échelons : **saturation**, puis cas C₆ + C₆ ou C₁₂, contradiction μ = 3.
**Transposition à 99 (t = 6).** 36 voisins propres, |W| = 60, 3·t(L) ≤ 36 échelons lointains, chaque w ∈ W en porte
ρ(w) ≤ 3 : Σρ(w) = 3t(L) ≤ 36 ≪ 180. Aucune saturation, la marge disparaît. Il faudrait une information globale
supplémentaire (c'est encore « majorer la torsion »).

### 3.4 Brouwer–Van Maldeghem, *Strongly Regular Graphs* (2022), état de l'art sur 99
(PDF complet, homepages.cwi.nl/~aeb/math/srg/rk3/srgw.pdf, p. 16.) Wilbrink (1984, *Papers dedicated to J. J. Seidel*,
EUT 84-WSK-03) : pas d'automorphisme d'ordre 11, donc pas de groupe transitif. Behbahani–Lam (2011) : un automorphisme
d'ordre premier est d'ordre 2 ou 3. Crnković–Maksimović (Contrib. Discr. Math. 15, 2020) : pas de groupe d'ordre 6 ni 9.
Le livre signale que la « preuve » de Makhnev pour le graphe de Moore (3250, 57, 0, 1) (arXiv:2010.13443) est
**fausse**. Cet article n'est donc pas une source.
**Lecture.** Tout ce qui est connu sur 99, hors Makhnev 1988, porte sur les symétries. Pour C1 (groupe trivial), la
littérature ne contient que Makhnev 1988 (non tordu exclu) et des faits locaux (Lou–Murin, Reimbayev). C1 est
essentiellement le problème entier.

### 3.5 Cesarz–Woldar 2025 (Algebraic Combinatorics 8(2), 379–398, accès libre)
*On the automorphism group of a putative Conway 99-graph.* Preuves **sans ordinateur** : si 2 divise |G| alors |G|
divise 6 (pas d'élément d'ordre 14, par partitions en orbites et valences), et si 7 divise |G| alors G = Z₇ (Frob(21)
exclu). Ils s'appuient sur Makhnev (J. Math. Sci. 166, 2010, cor. 2.4) et Makhnev–Minakova (Diskret. Mat. 16, 2004 :
|G| divise 2·3³·7·11 ; srg(v,k,1,2) ⇒ k = u² + u + 2, u ∈ {1, 3, 4, 10, 31}). Rien pour C1 ; pour C2, rien de plus que
Makhnev.

### 3.6 Ishida 2026, « No involutions in the missing Moore graph » (arXiv:2606.29183 v2)
Outil nouveau : **identité trace–rang** par le quotient de Brauer des réseaux de p-permutation. Si t est un
automorphisme d'ordre premier p de points fixes F et E un idempotent p-entier qui commute avec t, alors
tr(t | E) = rang_p(E[F]). Justification vérifiée : restreint à ⟨t⟩, un réseau de p-permutation est un réseau de
permutation, et Br(E) = E[F] mod p. Contrôles à la main sur la grille 3×3 (involution à 1 point fixe : trace 0 =
rang 0 ; involution fixant une droite : trace 2 = rang₂(K₃) = 2).
**Application à 99 (faite ici).** E₃ ≡ A et E₋₄ ≡ A + I + J (mod 2), tous deux 2-entiers. Pour une involution t :
(4f + a₁ − 18)/7 = rang₂(A_F), qui est pair (matrice alternée). Si f = 1, on obtient a₁ = 14 : t retourne les 7 droites
en son point fixe (t = σ_x). La congruence classique (a₁ ≡ 0 mod 7, 2 ≤ a₁ ≤ 14) le donnait déjà. Avec un idempotent
local (partie « impaire » du spectre de H, 3⁴⁰, 2-entière), on retrouve la même chose : H sur K^⊥ se scinde en blocs
symétriques et antisymétriques, de trace nulle. **Rien de nouveau pour C2 si f = 1**, et rien pour C1 (pas
d'automorphisme). Si une droite est fixe (f = 3), l'identité donne Σ_w φ_w = 10 retournements, sans exclure le cas.

### 3.7 Shpectorov–Zhao 2025, srg(85,14,3,2) n'existe pas (arXiv:2504.02449)
Énumération exhaustive (GAP, 96 cœurs pendant 14 mois) du voisinage d'une 3-clique maximale, que la représentation
euclidienne élimine (Gram semi-définie positive dès 30 sommets, rang ≤ 34 à 38 sommets). Le levier est un graphe local
riche (graphes cubiques à 14 sommets) et un espace propre de petite dimension (34). À 99, le graphe local est 7K₂
(trivial) et les dimensions sont 44/54. **Vérifié ici** : pour la boule d'une droite (39 sommets), la positivité de
Gram est automatique, quelle que soit l'holonomie. Les vecteurs de sommes nulles par classe voient le graphe cubique
H₃₆, de spectre dans [−3, 3] ; le quotient à 6 classes a pour valeurs propres {6, −1, 3², (−4)²}. Le rang ne mord
qu'au-delà de 44 sommets, donc en faisant intervenir W (60 points lointains), c'est-à-dire toute la torsion.
**Non transposable à coût raisonnable.**

### 3.8 Wilbrink 1984, *On the (99,14,1,2) strongly regular graph* (texte intégral obtenu)
Dans *Papers dedicated to J. J. Seidel*, EUT Report 84-WSK-03, p. 342–355 (volume complet de 393 pages récupéré via
research.tue.nl, derrière un défi Cloudflare, par le navigateur ; fichier pure.tue.nl/ws/portalfiles/portal/2449333/
256699.pdf). Contenu :
- Thm 1 (entrelacement de Haemers) : |Fix(g)| ≤ max(λ, μ)·n/(k − r), et ≤ n/(k − r) si g est d'ordre premier
  p > max(λ, μ). À 99 : ≤ 18 points fixes pour une involution, ≤ 9 sinon.
- Thm 2 (Brouwer, non publié) : un graphe à λ, μ > 0 constants est régulier, ou bien μ = 1 et c'est un moulin.
  Corollaire : pour p > max(λ, μ), le sous-graphe fixe est vide, un point, une (λ + 2)-clique, ou un srg de mêmes λ, μ.
- Thm 4 : conditions sur la matrice d'orbites (C² + (μ − λ)C + (μ − k)I = μNJ, valeurs propres, tr C ≡ k + s(t − 1)
  mod (r − s)).
- À 99 : premiers possibles 2, 3, 5, 7, 11 ; ordre 7 ⇒ un seul point fixe ; ordre 11 ⇒ aucun point fixe. Il signale
  un cas intéressant d'ordre 10, dont le sous-graphe fixe serait une grille 3×3 L₂(3).
- **Thm 5 : pas d'automorphisme d'ordre 11** (7 types de lignes pour la matrice d'orbites 9×9, élimination à la main
  et « 6 heures de calculatrice programmable »). Il remarque dès 1984 que Γ est une géométrie semi-partielle
  (Debroey–Thas) et un quadrangle partiel (Cameron).
Rien pour C1.

### 3.9 Autres lectures (texte intégral, rien d'utilisable)
- Brouwer–Neumaier 1988 (Combinatorica 8) : borne pour les espaces linéaires partiels de maille 5, appliquée au premier
  sous-constituant des srg à μ = 2. Ici Γ(x) = 7K₂, c'est-à-dire λ = 1 : la borne k ≥ λ(λ + 3)/2 = 2 est triviale.
- Mohammadian–Tayfeh-Rezaie 2013 (arXiv:1303.0473) : PQ(2, (n³ + 3n² − 2)/2, n² + n), c'est-à-dire la famille
  9 / 81 / 729 (Bondarenko–Radchenko), pas la nôtre (μ = 2 fixé).
- Reichard 2014 (arXiv:1401.6816) : condition des 7 sommets, graphes de rang 3 ; hors sujet.
- DeLeo 2024 (arXiv:2409.00268) : structures de voisinage partagé uniformes ; pour λ = 1 c'est un point, trivial.
- Reimbayev 2024 (arXiv:2409.10620, hexagones ; conjecture équivalente à Makhnev), 2025 (arXiv:2508.03377,
  sous-graphes d'ordre 6) : contenus dans notre hiérarchie exacte (ordres 6–8).
- Zehavi–de Oliveira 2017 (arXiv:1707.08047) : une autre lecture de l'énoncé de Conway, résolue ; hors sujet.

**Bilan de la bibliographie.** Pour C1 (groupe trivial), la littérature se réduit à Makhnev 1988 (non tordu exclu, =
notre L1), aux faits locaux (Lou–Murin, Reimbayev) et aux échecs de recherche (Keramatipour : SAT ; Thakkar–Severini :
heuristiques). Tout le reste porte sur les automorphismes : Wilbrink 1984, Makhnev–Minakova 2004, Behbahani–Lam 2011,
Crnković–Maksimović 2020, Cesarz–Woldar 2025. Les deux non-existences récentes de la même taille, (85,14,3,2) et
(57,14,1,4), utilisent un levier local qui manque à 99 : un graphe local riche, ou un μ plus grand.

### 3.10 Caractérisations des graphes de Hamming (vérifiées, inapplicables)
- Kivva (JCTB 2021, arXiv:1912.11427), thm 1.4 : graphe distance-régulier géométrique, μ ≥ 2, localement une union
  disjointe de cliques, avec l'hypothèse **θ₁ ≥ (1 − η)b₁** (seconde valeur propre proche de b₁, comme pour
  H(d,s) où θ₁ = b₁ − 1) : c'est un graphe de Hamming. À 99, θ₁ = 3 et b₁ = 12 : l'hypothèse spectrale est fausse.
  (Sans elle, BvLS serait un contre-exemple.)
- Caractérisation par comptage (μ ∈ {0, 2}, sans diamant ni prisme privé d'une arête, cliques maximales régulières ⇒
  Hamming) : l'hypothèse « pas de prisme privé d'une arête » est exactement « non tordu ». C'est Makhnev / L1 sous
  une autre forme.
