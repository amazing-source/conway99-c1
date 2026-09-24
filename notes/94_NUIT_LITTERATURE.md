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
