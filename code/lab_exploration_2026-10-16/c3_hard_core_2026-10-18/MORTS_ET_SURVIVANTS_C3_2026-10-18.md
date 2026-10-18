# c = 3 : ce qui meurt, ce qui survit, et pourquoi — 18/10/2026, 22 h 45 (LAB)

Méthode demandée par l'utilisateur : observer comment et pourquoi les objets meurent, puis les comparer aux survivants.
Tous les chiffres ci-dessous sont des **données** (registre c3_ledger.py, verdicts du probe de Codex).

## 1. Au niveau des Gram : le probe à équation propre de Codex en couche 0

Sources : 13 249 Gram, issues des runs c3eig1 (Gram dures de la 3ᵉ passe), c3p4e et c3p4eb (toutes les Gram des couvertures
d'au plus 3 000 Gram). 11 392 sont INFEASIBLE et 1 857 UNKNOWN (30 s).

| caractéristique | mortes | survivantes |
|---|---:|---:|
| arêtes internes des 21 rectangles (84 − tr R / 2), moyenne | 49,0 | 45,4 |
| directions de norme 2, moyenne (maximum) | 0,3 (15) | 0,0 (2) |
| directions de norme 4, moyenne | 6,3 | 8,5 |
| variables du modèle, moyenne | 12 300 | 19 500 |
| lignes de coins, moyenne | 3 000 | 8 200 |

Taux de survie selon le nombre d'arêtes internes :

| arêtes internes | 40 | 41 | 42 | 43 | 44 | 46 | 48 | 50 | 52 | 54 | plus de 55 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| survie | 17 % | 64 % | 35 % | 41 % | 22 % | 12 % | 11 % | 13 % | 7 % | 3 % | moins de 2 % |

**Pourquoi.** Peu d'arêtes internes donnent beaucoup de paires de coins non adjacentes. Pour chacune, la C2 impose μ = 2
voisins communs, et la couche 0 n'impose aucune C2 individuelle. La couche 1 (C2 dans les rectangles) tue les deux Gram
dures testées : gz 934, Gram 1 et 5, en 8,9 s et 17,0 s. Le run c3eig2 en couche 1 portera sur toutes les UNKNOWN.

## 2. Au niveau des gabarits : registre (10 027 gabarits gz)

Le nombre de **blocs de taille 2** (paires) décide presque tout.

| paires | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 et plus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ouverts / total | 26/27 | 124/155 | 367/728 | 324/1430 | 267/1703 | 149/1432 | 95/1490 | 31/1046 | 40/2016 |
| survie | 96 % | 80 % | 50 % | 23 % | 16 % | 10 % | 6 % | 3 % | 2 % |

Autres facteurs :
- taille maximale de bloc 4 : 16 % de survie, contre 3 % pour la taille 3 ;
- peu de rectangles non grille, donc k élevé : 17 à 30 % de survie pour 9 à 14 rectangles non grille, contre 2 à 6 % pour 16 à 18 ;
- dimension du noyau, mesurée sur le registre à 1 713 ouverts : 7 % de survie en dimension 4, 27 % en dimension 5, 93 % en
  dimension 6, 100 % en dimension 7.

**Pourquoi.** Une paire {b, c} à la racine a donne, pour chaque étiquette, h(ab) + h(ac) = 0. Ce couplage rigide alimente
les chaînes de propagation (lemme FG, saturation E3 + symétrie de R1). Un bloc de 3 ou 4 ne donne qu'une équation sur 3 ou 4
inconnues : beaucoup plus de liberté.

## 3. Le cas extrême : les 27 gabarits sans paire (26 ouverts)

À chaque racine, la partie non grille est un seul bloc de taille 3 ou 4 (ou rien). Le graphe des blocs Ĵ est alors J
lui-même, et une ligne est une pondération entière de J à somme nulle en chaque sommet.

| gabarit | k | dim | degrés de J |
|---|---:|---:|---|
| 5602, 5628 | 7 | 7 | J 4-régulier sur 7 sommets |
| 7861, 7912, 7937, 7990, 8111 | 8 | 6 | (3, 3, 4, 4, 4, 4, 4) |
| 9174, 9179, 9221, 9229, 9239, 9502, 9505, 9512, 9522 | 9 | 5 ou 6 | (3, 3, 3, 3, 4, 4, 4) |
| 9302 | 9 | 6 | (0, 4, 4, 4, 4, 4, 4) |
| 9744, 9748 | 10 | 4 | (3, 3, 3, 3, 3, 3, 4) |
| 9791, 9912 | 10 | 5 | (0, 3, 3, 4, 4, 4, 4) |
| 9954, 9966 | 11 | 4 | (0, 3, 3, 3, 3, 4, 4) |
| 10003 | 11 | 5 | (0, 0, 4, 4, 4, 4, 4) |
| 10006, 10025 | 12 | 4 | — |

Le gabarit 10009, de dimension 3, est le seul mort de cette famille.

**Cible de lemme.** Il faut décrire les composantes de G_{l_a} formées de 3 ou 4 unités : graphes cubiques à 18 ou 24
sommets, avec λ = 1, μ = 2 et la structure de lettres. Les identités signées d^K (Gram 8(6pδ − pp′), vecteurs propres −1 de
D_a) y sont très contraignantes, puisque chaque racine n'a qu'une composante non triviale et des prismes. C'est l'objet
transmis à Codex pour son front sans Gram.
