# 97 — L20 : l'invariant 7-adique k borné par le type de torsion de chaque étiquette

*Nuit du 25/09, vers 04 h. Répond à la direction retenue en notes/93 (« comprendre k ») : premier lien démontré entre
l'invariant global k = rank₇(A − 3I) − 15 (L4, L19) et la torsion locale.*

## Priorité (vérifiée en texte intégral)
Le **principe** est classique : C. A. van Eijl, *On the p-rank of the adjacency matrices of strongly regular graphs*,
mémoire de master, TU Eindhoven, oct. 1991 (dir. A. E. Brouwer), §3.3 « Bounds from subgraphs » :
r_p(A + τI) ≥ r_p(A' + τI) pour tout sous-graphe induit. Son théorème 3.5(iii) donne la borne supérieure
rank₇(A − 3I) ≤ min(f, g) + 1 = 45, c'est-à-dire k ≤ 30. Son exemple 3.2 (Gewirtz, 2-rang) utilise un argument « une
ligne n'est pas somme de lignes locales, sinon μ = 2 est violé », du même type que notre preuve de k ≥ 2 (notes/94).
**Ce qui est nouveau ici** : l'application à 99, le choix des étoiles (sous-matrice déterminée par τ_a), la formule
rank₇ = 11 − 2e(τ_a) et ses conséquences (k ≥ 6, k = 6 ⟹ P = 0), et la formule locale exacte de k. Le mémoire ne
mentionne pas (99,14,1,2).

## Principe
Pour un sommet x et Y' ⊂ Γ₂(x) dont la structure interne est connue, la sous-matrice principale de A − 3I sur
B₁(x) ∪ Y' est entièrement déterminée. Le bloc du moulin, F − 3I, est inversible modulo 7 (det = 2²³). D'où
rank₇(A − 3I) ≥ 15 + rank₇(S_{Y'}), où S_{Y'} est le complément de Schur, et donc **k ≥ rank₇(S_{Y'})**.
- Y' = {y} (un sommet) : S est un scalaire non nul mod 7, donc k ≥ 1, et k ≥ 2 par parité (L2). C'est une seconde
  preuve, en une ligne, de L19 bis.
- Y' = étoile(a) = les 12 sommets de Γ₂(x) d'étiquette a. Deux sommets {a,b}, {a,c} sont adjacents ssi
  τ_a(b) = c, et chacun n'est adjacent qu'à ses deux étiquettes dans B₁(x). La sous-matrice ne dépend donc que de τ_a.

## Le résultat (calcul exhaustif exact, `code/star_rank7.py`, les 10 395 couplages τ_a)
Le **type de classes** de τ_a est le multigraphe 2-régulier induit sur les 6 autres classes : une boucle pour une
classe non tordue (ses deux étiquettes appariées entre elles), sinon des cycles. Soit e(τ_a) le nombre de cycles de
**longueur paire** (les 2-cycles, c'est-à-dire deux classes échangées, comptent).

| type (classes non tordues ; cycles) | nombre de τ_a | rank₇(S) |
|---|---|---|
| (0 ; 2,2,2) | 120 | 5 |
| (0 ; 2,4) | 1440 | 7 |
| (0 ; 6) | 3840 | 9 |
| (0 ; 3,3) | 640 | 11 |
| (1 ; 2,3) | 960 | 9 |
| (1 ; 5) | 2304 | 11 |
| (2 ; 2,2) | 180 | 7 |
| (2 ; 4) | 720 | 9 |
| (3 ; 3) | 160 | 11 |
| (4 ; 2) | 30 | 9 |
| (6 ; —) (non tordu) | 1 | 11 |

Dans tous les cas, **rank₇(S) = 11 − 2·e(τ_a)**.
*Contre-vérification indépendante* : rang sur GF(7) de la sous-matrice principale complète 27 × 27, calculé par
sympy (DomainMatrix sur GF(7), sans complément de Schur) pour un représentant de chaque type : 15 + 11 − 2e dans
les 11 cas. Le rang ne dépend que du type (calcul exhaustif ci-dessus).

## Lemme L20
Pour tout sommet x et toute étiquette a ∈ Γ(x) : **k ≥ 11 − 2e(τ_a)**, donc (k pair) **k ≥ 12 − 2e(τ_a)**.
Conséquences :
1. **k ≥ 6** dans tout srg(99,14,1,2), puisque e ≤ 3. Cela améliore k ≥ 2.
2. **k = 6 ⟹ chaque τ_a, en chaque sommet, échange ses 6 classes en trois paires.** Toutes les étiquettes sont alors
   entièrement tordues, donc Σ|W| = 99·84 = 8316 et **P = 0** (L15) : aucun prisme.
3. Contraposée : **P ≥ 1 ⟹ k ≥ 8.** En effet un prisme donne une classe non tordue pour une étiquette. Avec une boucle,
   il reste ≤ 5 classes tordues, donc au plus 2 cycles pairs.
4. **Une seule étiquette non tordue (τ_a = mate) quelque part ⟹ k ≥ 12.** C'est le cas au voisinage d'une grille.
   Une étiquette dont le graphe de classes n'a que des cycles impairs (types 3,3 ; 5 ; 3) donne aussi k ≥ 12.
5. k est global : **k ≥ 12 − 2·min_{x, a} e(τ_a)**.

## Portée, honnêtement
- C'est le premier lien démontré entre k et la torsion, mais il va dans le sens « peu tordu ⇒ k grand ». Or L19 ne
  mord que pour k petit. Le cas k petit est rejeté vers la torsion maximale (P = 0), que L16 autorise.
- Il n'y a toujours **aucune borne supérieure sur k** (un Γ générique aurait k = 30). Un argument qui donnerait k ≤ 10,
  par exemple, combiné à L20, forcerait des types de torsion très particuliers en tout sommet.
- La formule 11 − 2e a maintenant une **preuve à la main** (section suivante), en plus du calcul exhaustif.
- Généralisation possible : des Y' plus grands à structure connue (boules de droites, 39 sommets, déterminées par
  l'holonomie) donneraient des bornes plus fortes, mais avec des entrées inconnues à énumérer.

## Preuve à la main de rank₇(S) = 11 − 2e(τ_a)
1. **Inverse du moulin.** F − 3I = [[−3, 1ᵀ], [1, P − 3I]] (P : involution des mates sur les 14 étiquettes). Le bloc
   étiquettes de l'inverse est (P − 3I + J/3)⁻¹. Ses valeurs propres sont −4 (antisymétriques), −2 (symétriques
   ⊥ 1) et 8/3 (sur 1). D'où **G = −(3/8)I − (1/8)P + J/16**.
2. **Complément de Schur.** Le sommet {a, b} a pour colonne e_a + e_b. Donc C₀[b,c] = G_aa + G_ab + G_ac + G_bc
   = −1/8 − (3/8)δ_bc − (1/8)P'_bc (P' : mates parmi les 12 étiquettes b). Alors
   S = H_τ − 3I − C₀ = H_τ + P'/8 − (21/8)I + J/8, et **modulo 7 (8 ≡ 1, 21 ≡ 0) : S ≡ H_τ + P' + J**.
3. **Cycles alternés.** M = H_τ + P' est la matrice d'adjacence (avec multiplicités) de la réunion de deux couplages
   parfaits. Une classe non tordue donne une arête double (bloc [[0,2],[2,0]], inversible mod 7). Un cycle du graphe
   de classes de longueur m donne **un** cycle alterné de longueur 2m : on traverse chaque classe une fois (τ puis
   mate), et les 2m étiquettes sont épuisées en un tour.
4. **Noyau d'un cycle C_{2m} mod 7** : v_{i−1} + v_{i+1} = 0 impose v_{i+2} = −v_i, donc une période 4. Il est de
   dimension 2 si 2m ≡ 0 (mod 4), c'est-à-dire m pair, et nul si m est impair (car 2 est inversible). Donc
   dim ker₇ M = 2e, et ces vecteurs sont de somme nulle.
5. **Effet de J.** M1 = 2·1 et (2 + 12) ≡ 0 (mod 7), donc 1 ∈ ker(M + J). Réciproquement, si (M + J)v = 0, alors
   w = v + (Σv/2)·1 ∈ ker M. D'où ker₇(M + J) = ker₇ M ⊕ ⟨1⟩, de dimension 2e + 1, et **rank₇ S = 11 − 2e**. ∎
(Cas d'un seul sommet {a, b} : S = −3 − C₀[b,b] = −5/2 ≡ 1 ≢ 0 (mod 7), d'où k ≥ 1, donc k ≥ 2.)

## Test « tous les τ_a de type (2,2,2) en un sommet » (k = 6 ⟹ cela en tout sommet)
`code/type222.py` (modèle enraciné exact, τ_a parmi les 120 permutations de classes par paires, cassage de symétrie
valide, τ_(0,0) canonique) : 1,6 M variables, 3,8 M clauses. **Tué au plafond de 4000 Mo après 165 s**, non décidé sur
le portable. À relancer sur le PC du labo : UNSAT donnerait k ≥ 8. Les règles humaines L9', L12, L13 ne disent rien
dans ce régime (tout est tordu).

## Remarque : lecture isotrope modulo 7, et une cible nette
Modulo 7, N = A − 3I vérifie N² = 2J, et N1 = 4·1. Sur W = 1^⊥ (dimension 98, forme standard non dégénérée de
discriminant 1/99 ≡ 1), N est donc de **carré nul**. Son image I est **totalement isotrope**, de dimension 14 + k
(c'est l'intersection des réductions de Λ₃ et Λ₋₄, recollement de L2–L4). L'indice de Witt de W est 48 (−1 n'est pas
un carré mod 7), d'où seulement k ≤ 34, plus faible que k ≤ 30 (cohérent avec L3 : recollement non scindé).
**Cible** : comme k ≥ 6 (L20), toute preuve de k ≤ 4, c'est-à-dire rank₇(A − 3I) ≤ 19, prouverait la non-existence.
Hors de portée (il faudrait exhiber 26 vecteurs du noyau mod 7 au-delà des 54 rationnels), mais c'est une
reformulation arithmétique exacte d'une condition suffisante.

## Formule locale exacte pour k
La même réduction (G ≡ 4I + 6P + 4J mod 7 pour le bloc étiquettes de (F − 3I)⁻¹) donne, pour deux sommets
y = {a,b}, z = {c,d} de Γ₂(x) : C₀[y,z] ≡ 4s + 6p' + 2 (s : étiquettes communes, p' : couples d'étiquettes mates).
D'où, pour **tout** sommet x :
  **k = rank₇( H + 4I + 3S + P' + 5J )** (matrice 84 × 84 sur F₇ ; S = MᵀM, P' = MᵀPM).
Sur K (Mv = 0, v ⊥ 1) elle agit comme H − 3I, ce qui redonne L4. Sur une étoile elle se réduit à H_τ + P' + J (L20).
C'est une expression de l'invariant global k par la seule structure de Γ₂(x). Il resterait à la calculer sur des
modèles, mais aucun modèle de Γ₂(x) n'est connu (c'est le problème).
