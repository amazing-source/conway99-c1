# 182 — Recensements exacts à huit et neuf sommets

8 octobre 2026. Prolongement de la note 181 et des familles proposées par LAB.

**Résultat géométrique : P≤852 et ρ≤126.** Le recensement à neuf sommets resserre
les bornes sur les prismes et les grilles et donne les minorations déjà valides
**b3≥43848, b4≥3371634, b5≥34087368**, après les pertes auditées des notes 179 et 181.
Le certificat est présenté au §5 ; il ne dépend pas de la résolution des nouvelles collisions.

La famille signée `(6,3)` à neuf sommets possède par ailleurs au moins
**10 336 557 représentants de norme projetée huit**. Son compte de norme six
n'a pas de minoration strictement positive dans la relaxation de comptage.
Les deux comptes satisfont cependant des minorations conjointes, données au §4.
Il s'agit encore de représentants : leurs collisions ne sont pas soustraites ici.

## 1. Systèmes complets d'extension

On conserve tous les graphes induits respectant les budgets locaux λ≤1 et μ≤2.
Les identités d'extension comptent les sommets extérieurs sans marque, voisins
d'un sommet marqué, puis voisins communs de deux sommets marqués. Tous les
invariants laissés libres par ces identités sont conservés.

| Taille | Types | Équations | Rang | Nouveaux paramètres libres |
|---:|---:|---:|---:|---:|
| 7 | 208 | 712 | 207 | 1 |
| 8 | 916 | 3 578 | 909 | 7 |
| 9 | 5 311 | 22 930 | 5 263 | 48 |

Il y a donc 57 paramètres à l'ordre neuf : P, l'invariant h de l'ordre sept,
sept comptes de graphes à huit sommets et quarante-huit à neuf sommets.

L'ordre neuf utilise une canonisation par individualisation et raffinement.
Chaque branche de la première cellule non singleton est explorée ; toutes les
numérotations minimales sont conservées pour canoniser aussi les graphes marqués.
Les anciens graphes sont recanonisés lors de la construction des équations.

L'élimination rationnelle creuse choisit d'abord une ligne ayant peu d'inconnues,
puis une colonne apparaissant dans peu de lignes. Les colonnes affines du second
membre sont transportées sans être utilisées comme pivots. La substitution
inverse donne une solution affine complète. On vérifie exactement son produit
par **la matrice initiale**, ainsi que la somme des comptes, égale à C(99,n).
Les lignes restantes sont nulles, sans nouvelle relation imposée aux anciens
paramètres. L'ordre neuf s'est terminé en environ 132 secondes sur cette machine.

Les JSON `codex_order8_census.json` et `codex_order9_census.json` archivent les
matrices creuses, seconds membres, comptes affines et conventions de codage.
Le script d'élimination est `code/codex/sparse_census_elimination.py`.

## 2. Huit sommets : quatre positifs et quatre négatifs

Pour ψ=1_W−1_Y, avec |W|=|Y|=4, la norme projetée vaut

    Q(ψ)=24−2(e(W)+e(Y)−e(W,Y)).

Les graphes admissibles sur quatre sommets ont au plus quatre arêtes. La norme
huit correspond donc exactement à deux quatre-ensembles à quatre arêtes,
anticomplets entre eux. Le compte signé F8 vérifie

    F8 ≥ 2 723 490.

Plus précisément, en notant G_c le compte du graphe de code c dans le JSON :

    F8 = 2723490 + 6G_2022000 + 4G_5683824 + 8G_5691760
                   + 38G_48674912 + 18G_57358896
                   + 6G_115750946 + 5G_123090978.

La non-négativité de ces sept comptes suffit à certifier la borne. Un point
rationnel admissible l'atteint dans la relaxation.

## 3. Neuf sommets : six positifs et trois négatifs

On compte les deux signes de ψ=1_W−1_Y, avec |W|=6, |Y|=3. La norme vaut

    Q(ψ)=28−2(e(W)+e(Y)−e(W,Y)).

Notons N6 et N8 les comptes signés des représentants de normes six et huit.
Le tableau donne des minorations exactes, séparées par nombre d'arêtes.
Les minima des différentes lignes ne sont pas supposés simultanément atteints.

| Norme | e(W) | e(Y) | Arêtes entre W et Y | Minoration |
|---:|---:|---:|---:|---:|
| 4 | 9 | 3 | 0 | 0 |
| 6 | 8 | 3 | 0 | 0 |
| 6 | 9 | 2 | 0 | 0 |
| 6 | 9 | 3 | 1 | 0 |
| 8 | 7 | 3 | 0 | 95513418/25 |
| 8 | 8 | 2 | 0 | 48066480/13 |
| 8 | 8 | 3 | 1 | 213854256/515 |
| 8 | 9 | 1 | 0 | 0 |
| 8 | 9 | 2 | 1 | 0 |
| 8 | 9 | 3 | 2 | 0 |

Le minimum du total N8 est plus fort que la somme des minima séparés :

    N8 ≥ 10 336 557.

Le certificat est une identité affine exacte avec 54 coefficients rationnels
non négatifs appliqués à des comptes de graphes. Le JSON des minima l'archive.
Un point rationnel atteint ce minimum avec P=0, H=1617/2, N6=341418.
Ce point de relaxation n'est pas présenté comme un graphe réalisé : les comptes
de graphes y sont autorisés à être rationnels.

La relaxation admet aussi N6=0, par exemple avec P=0,H=2079,N8=14985432.
L'estimation heuristique de 190 000 représentants de norme six ne constitue donc
pas une borne uniforme démontrée par ce système.

## 4. Minorations conjointes et portée

L'optimisation conjointe donne les certificats rationnels suivants :

    N8 +       N6 ≥ 308506968/29,
    N8 +     5 N6 ≥ 1132249734/97,
    N8 +    10 N6 ≥ 12615372,
    N8 + (651/34) N6 ≥ 64543248/5,
    N8 +    20 N6 ≥ 64543248/5.

Le dernier seuil vaut 12 908 649,6. Contrairement aux minima individuels des
totaux N6 et N8, nous n'archivons pas de point rationnel atteignant ces seuils
conjoints ; leurs **certificats de minoration** sont intégralement vérifiés.

Le solveur flottant sert uniquement à découvrir le support d'une combinaison
duale. Les coefficients sont ensuite recalculés rationnellement et chaque
coefficient de l'identité affine est vérifié, ainsi que leur non-négativité.

Ces nouvelles familles peuvent compléter les représentants de la note 181.
Pour les convertir en bornes sur b3 et b4, il reste à borner les collisions
internes et celles avec les familles déjà comptées. Les systèmes thêta ne
reçoivent pas automatiquement les valeurs F8,N6,N8 comme nombres de vecteurs
distincts. **Cette note n'exclut pas le rang 37.**

## 5. Bornes géométriques et conséquences immédiatement utilisables

Le recensement à huit sommets permet encore P=1386. Celui à neuf sommets donne

    P ≤ 11088/13, donc P≤852 ;       ρ≤126.

La borne sur P découle de l'identité entière suivante (codes de graphes à neuf sommets) :

    33696P
    +1296G_3667157184 +657G_3669387456 +1296G_3918849232
    +432G_3949811904 +432G_3985958096 +774G_6890084544
    +900G_10979993824 +441G_10984517760 +10G_13610133664
    +351G_15191070912 +702G_15781745092 +20G_22406639744
    +351G_25040839304 +684G_28490511536 +684G_30378173584
    +702G_38029107329 = 28740096.

Tous les coefficients sont positifs. L'identité est vérifiée sur chacune des
57 coordonnées affines du recensement. Le code du graphe grille est 13262907120.
Son majorant 126 possède également un certificat rationnel exact et un point
rationnel admissible qui l'atteint. Les bornes H≤2079 et 3P+2H≤4158 ne sont pas
améliorées par ces optimisations.

En optimisant conjointement les formes déjà prouvées des notes 179 et 181, on obtient :

| Forme dont on minimise la valeur | Minimum certifié |
|---|---:|
| 66528−18P−72ρ | 43848 |
| 3826746−30P−4572ρ | 3227994 |
| 5939010−1134P−84H−13572ρ | 3371634 |
| 35123088−168P−7212ρ | 34087368 |

La troisième forme utilise τ≤5P/2 et Ω≤H dans la borne de sept sommets. Ces
minorations sont donc bien des bornes sur **les vecteurs distincts** :

    b3≥43848,       b4≥3371634,       b5≥34087368.

Elles utilisent la géométrie des graphes à neuf sommets pour resserrer les
paramètres des anciennes familles. Elles n'utilisent pas F8,N6,N8 comme nombres
de projections distinctes. Le coin P=1386,ρ=231 qui limitait les bornes précédentes
est désormais impossible. Les certificats de ce paragraphe reposent sur notre
recensement exact ; LAB a revérifié les premières conséquences arithmétiques,
sans encore reproduire indépendamment le recensement à neuf sommets.

En réinjectant ces conséquences dans la relaxation thêta à q^84, le maximum
possible de b4 au nouveau seuil b3=43848 devient 214492633/13, soit environ
16 499 433,31. Le rang 37 reste admissible dans cette relaxation. Les cibles
conditionnelles pour b3≥150000,300000,600000 restent celles de la note 181.
Le script `rank37_dual_frontier.py --order9` archive les certificats et les
points rationnels correspondants dans `codex_rank37_dual_frontier_order9.json`.

## 6. Reproduction

Depuis la racine du dépôt :

```text
python code/codex/seven_vertex_census.py
python code/codex/higher_vertex_census.py --order 8
python code/codex/higher_vertex_census.py --order 9
python code/codex/higher_census_minima.py --order 8
python code/codex/higher_census_minima.py --order 9
python code/codex/higher_census_geometry.py
```

Certificats : `data/codex_order8_raw_family_minima.json` et
`data/codex_order9_raw_family_minima.json`.
Les autres certificats sont dans `codex_order9_prism_cap.json`,
`codex_order9_geometry_caps.json` et `codex_order9_uniform_shell_bounds.json`.
