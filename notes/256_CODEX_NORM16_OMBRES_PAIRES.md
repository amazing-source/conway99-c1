# 256 — Norme 16 : dix attaches entières exclues par les ombres paires

10 octobre2026. Suite de la note255, sans hypothèse de rang.

**Résultat.** Parmi les478 attaches au cœur de la note169, quinze ont
toutes leurs intersections C_xy paires. Neuf sont exclues par un
comptage10>8 ; une dixième par un vecteur entier de Rayleigh. Ces
exclusions couvrent D indépendant et D à une arête. Les cinq autres
attaches paires ne permettent plus que trois formes de Z.

| Cœur (indice dans les fichiers) | Attaches exclues (indices à partir de0) |
|---|---|
| 8 (cas0) | 52 |
| 4+4 (cas2) | 44,46,81,82,84,85 |
| 4+2+2 (cas3) | 26 |
| 2+2+2+2 (cas4) | 0,3 |

Cela élimine dix orbites d'attaches nécessaires, et non dix graphes
à99 sommets. La norme16 reste ouverte. On ne recompte pas ici les
exclusions antérieures sur la seule branche D indépendant.

## 1. Le graphe des intersections paires

Pour x≠y dans D, soit C_xy le nombre de leurs voisins communs au
cœur P∪Q ; poser C_xx=0. Chaque sommet du cœur a deux voisins D,
chaque D a quatre voisins au cœur, donc chaque ligne de C a somme4.
On a C_xy<=2.

Supposons toutes les entrées de C paires. Alors C=2L, où L est
l'adjacence d'un graphe simple2-régulier sur les huit sommets D.
La note255 exige, si D porte de, quatre valeurs impaires parmi
C_dx+C_ex. C'est impossible ici : **D est indépendant**.

Pour chaque z dans Z, N_D(z) est un stable de L. En effet, une arête
xy de L signifie que x,y possèdent déjà leurs deux voisins communs
au cœur ; aucun z ne peut être voisin des deux. De plus

    |N_D(z)|=2+d_Z(z),    |N_Z(d)|=4 pour tout d dans D.

Les seuls types2-réguliers possibles sur8 points sont C8, C4+C4 et
C3+C5. Le dernier est impossible : les trois D du triangle demandent
12 incidences avec Z, mais chacun des11 sommets Z peut en voir au plus un.

## 2. Deux cycles de quatre imposeraient dix incidences pour une capacité de huit

Supposons L=C4+C4, de composantes U,V. Pour z dans Z, écrire
a_z=|N_D(z)∩U| et b_z=|N_D(z)∩V|. Les deux nombres sont au plus2.
Le nombre de paires de voisins de z contenues dans une même composante
est donc

    binom(a_z,2)+binom(b_z,2) >= a_z+b_z-2 = d_Z(z).

En sommant sur Z, on obtient au moins2e(Z)=10 telles incidences.
Dans chaque C4, seules les deux diagonales peuvent être vues par z.
Il y a donc quatre paires utilisables en tout, chacune possédant au
plus deux voisins Z communs. Le total est au plus8. Contradiction.

**Tout graphe d'ombres paires réalisable est donc un unique C8 doublé.**
Ce comptage exclut les neuf attaches C4+C4 de la liste, sur trois types
de cœur. Il ne dépend pas des autres arêtes de Z ou des simples B.

## 3. Un cycle de huit interdit les étoiles et les P4 dans Z

Supposons maintenant L=C8. Un stable de L a au plus quatre sommets,
donc d_Z(z)<=2 pour tout z. Les composantes K1,3 sont exclues.

Supposons qu'une composante de Z soit le chemin x-a-b-y. Les deux
sommets centraux a,b ont chacun quatre voisins D. Les seuls stables
de taille4 d'un C8 sont ses deux classes de bipartition. Comme a,b
sont adjacents, leurs voisinages D ne peuvent coïncider ; ils sont
donc complémentaires et partitionnent D.

La feuille x voit au plus un voisin D de a, puisque xa est une arête.
Elle voit aussi au plus un voisin D de b, puisque x et b partagent
déjà a dans Z. Ainsi |N_D(x)|<=2, contrairement à |N_D(x)|=3.

Il reste exactement les formes de la branche D indépendant :

| Identifiant historique | Z |
|---|---|
| 3 | 2P3 + K2 + 3K1 |
| 6 | P3 + 3K2 + 2K1 |
| 7 | 5K2 + K1 |

En particulier, pour le cœur de défaut(2,2,2,2), les attaches0 et3
sont exclues, et les attaches1 et2 ne laissent que ces trois forêts.
Le nombre de paires cœur/Z permis par les notes255–256 passe ainsi
de51 à au plus47 ; ce n'est toujours pas un nombre de complétions.

## 4. Une dixième attache exclue sur vingt-quatre sommets

Pour le cœur0, attache52 du fichier de la note169, C=2C8 force encore
D indépendant. Soit A_F l'adjacence induite sur cœur+D, ordonné
P0..P7,Q0..Q7,D0..D7. Le vecteur entier suivant a somme nulle :

    (106,101,33,-50,-106,-101,-33,50,
      50,106,33,-106,-33,101,-50,-101,
     141,94,94,0,-94,-141,-94,0).

Une multiplication entière donne

    3||v||² - vᵀ A_F v = -470 < 0.

Son prolongement nul au graphe contredirait la borne de Rayleigh3
sur les vecteurs de somme nulle. L'attache52 est donc exclue.

Ce certificat vient du Schur de la note254 : pour
w=(3,2,2,0,-2,-3,-2,0), on a wᵀHw=-10/47. La partie au cœur de v
est47 M^-1 Vw, et sa partie sur D est47w. Le fichier
`codex_norm16_even_shadows.json` contient A_F et le vecteur entier ;
aucune approximation spectrale n'est nécessaire pour le certificat.

## 5. Portée, couverture et suite

Les cinq attaches paires restantes sont (cas,attache)

    (0,226), (0,241), (0,242), (4,1), (4,2).

Toutes ont D indépendant, C=2C8 et Z parmi les trois formes ci-dessus.
Ce sont des contraintes nouvelles sur une famille complète ; elles ne
disent rien de définitif sur les463 attaches qui possèdent une entrée
impaire de C.

Un pilote fini sur (4,1) laisse30484 supports satisfaisant la PSD exacte
de3I-A+J/9, répartis352,6852,23280 entre les trois forêts. Les sept
forêts originales ont été parcourues, sans arrêt anticipé ; les quatre
autres sont vides. Cette relaxation n'exclut donc pas l'attache. Ces
supports ne sont ni des SRG ni un décompte global de mondes de rang33.
La sonde numérique de l'autre borne spectrale, E_3, n'a pas réduit ce
pilote ; aucun nouveau certificat n'en est revendiqué.

La génération générique par millions n'est pas relancée. La suite
cherchera une incompatibilité uniforme du C8 ou un autre comptage sur
les ombres mixtes. LAB poursuit son pilote de cellule sur la branche
à une arête et les cœurs18/20 ; aucun de ces travaux n'est dupliqué ici.

Reproduction de la liste et du nouveau certificat :

    python code/codex/norm16_even_shadows.py

Le programme réutilise les478 attaches archivées. Il identifie leurs
intersections paires, applique les types ci-dessus, et vérifie uniquement
la nouvelle identité entière-470 du certificat.
