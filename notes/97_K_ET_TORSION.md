# 97 — L20 : l'invariant 7-adique k borné par le type de torsion de chaque étiquette

*Nuit du 25/09, vers 04 h. Répond à la direction retenue en notes/93 (« comprendre k ») : premier lien démontré entre
l'invariant global k = rank₇(A − 3I) − 15 (L4, L19) et la torsion locale.*

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
- La formule 11 − 2e est vérifiée exhaustivement ; une preuve à la main passerait par la décomposition de
  τ_a ∪ (mates) en cycles alternés sur les 12 étiquettes (la correction de Schur est une combinaison de I, J et de la
  matrice des mates). Non rédigée.
- Généralisation possible : des Y' plus grands à structure connue (boules de droites, 39 sommets, déterminées par
  l'holonomie) donneraient des bornes plus fortes, mais avec des entrées inconnues à énumérer.
