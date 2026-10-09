# Coût du calcul du rang 37 : mesures et plancher (09/10/2026 15:35 UTC, session du PC labo)

Demande de l'utilisateur : « coupe le coût du calcul ». Objet : le balayage exhaustif des boules de droites au rang 37
(session portable : environ 1,9e11 types de boules, dont 1,4e10 connexes sans prisme ; test d'une étoile par boule).

## Ce qui a été mesuré ici (un cœur, ce PC, boules aléatoires connexes, sans prisme, sans torsion)

Modèle : celui de `fast.c` de la session portable, cas connexe (aucun signe libre) ; rappel en tête de `star37.c`.
Tirage : sur 675 boules valides, 90 ont de la torsion (13 %), 285 ont un discriminant résidu (42 %, éliminées sans
calcul par le filtre L23), 300 restent à tester (44 %).

| version | candidats par étoile | nœuds | tests de paires | temps par boule testée |
|---|---|---|---|---|
| `star37.c` (portage de la recherche de la session portable) | 3244 | 32 101 | 4,6 millions | 63 à 67 ms |
| `star37b.c` (tables pour la norme et pour les relations) | 3244 | 32 101 | 4,6 millions | 43,6 ms (+ 0,3 ms de candidats, 0,1 ms d'inverse) |
| `star37b.c`, sommet d'étoile ayant le plus de zéros dans K | 2932 | 23 123 | 3,4 millions | 31,7 ms |

Contrôle : sur 100 boules, `star37b` et la recherche de référence donnent les mêmes candidats, les mêmes nombres de
nœuds et les mêmes verdicts (0 écart). Toutes les boules testées (plus de 400) sont mortes : aucune étoile.
Profil de la recherche (`star37_stats.c`) : 286 choix au niveau 1 (422 candidats vivants après un choix), 9 600 nœuds
au niveau 2 (49 vivants), 22 000 au niveau 3 (5 vivants), mort au niveau 4. La borne réelle e ≤ 37/12 ne retire que
11 % des candidats. D'un sommet à l'autre d'une même boule le coût varie d'un facteur 2 à 3
(`star37_spread.c`).

## Plancher de cette méthode

Le coût est le produit de deux nombres qui sont chacun près de leur minimum :
1. **Nombre de boules, de l'ordre de 1e11.** Toute base qui porte les 36 dimensions modulo 7 a au moins 36 sommets ;
   les 36 proches d'une droite sont la base la moins coûteuse en types (les bases « rigides », réunions de droites
   ou de points deux à deux non adjacents, ont au plus 33 sommets : borne de Hoffman). Aucun invariant de la boule
   seule autre que le discriminant (facteur 3/7, déjà utilisé) : un espace quadratique sur F7 n'a que deux invariants.
2. **Coût par boule, de l'ordre du million de tests de paires.** Les conditions à un sommet lointain (norme, structure,
   borne réelle) laissent environ 300 candidats par emplacement ; les contradictions n'apparaissent qu'à partir de
   quatre membres de l'étoile. La frontière au niveau 2 (environ 1e4 paires) est proportionnelle au carré du nombre
   de candidats, que rien ne réduit.

Estimation avec une version à lignes de compatibilité en bits (non écrite) : 6 à 10 ms par boule, soit un gain total
de 6 à 10 sur la référence, pas de 1000.

## Ce que cela donne

| périmètre | boules à tester (44 %) | à 32 ms (acquis) | à 8 ms (atteignable) |
|---|---|---|---|
| connexes sans prisme, sans torsion (1,4e10 types) | 6,2e9 | 6,3 années-cœur | 1,6 année-cœur |
| tous les types sans torsion (1,9e11 types) | 8,4e10 | 85 années-cœur | 21 années-cœur |

Non compris : les boules avec torsion (13 %), dont le test est plus lourd, et les trois autres rangs.
Le PC du laboratoire fournit environ une année-cœur par mois (12 processus). Le facteur 1000 n'est donc pas atteint :
le calcul du rang 37 passe de plusieurs centaines d'années-cœur à quelques dizaines, pas à quelques semaines.

## Fichiers

`star37.c` (référence), `star37b.c` (version à tables, option `check`), `star37_stats.c` (profil et borne réelle),
`star37_spread.c` (36 sommets par boule). Compilation : `gcc -O2 -march=native`. Un processus, quelques Mo.
