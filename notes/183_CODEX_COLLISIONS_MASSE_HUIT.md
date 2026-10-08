# 183 — Classification et contrôle de la composante de masse huit

8 octobre 2026. Suite aux notes 181–182.

Cette note traite les collisions **de masse huit** entre représentants `(4,4)`
de norme projetée huit. Elle inclut les différences non binaires, indispensables
ici. Les différences de masses six et sept et les anciennes familles restent à
traiter avant de déduire une nouvelle borne complète sur b4.

## 1. Supports possibles d'une différence propre

Écrivons δ=u−v, avec u,v positifs, à supports disjoints, de même masse S=8,
et Aδ=3δ. La borne S≥4h de la note 168 donne h≤2.

Si u possède une coordonnée 2, son sommet est adjacent à tout le reste du support
positif : la masse disponible est exactement six, égale à sa somme de voisins
requise. Il n'a donc aucun voisin négatif. S'il y avait a≥2 coordonnées 2, deux
d'entre elles seraient adjacentes et auraient 6−a≥2 voisins communs positifs
(a≤4), contrairement à λ=1. Il y a donc un seul 2 et six coordonnées 1.

Chaque feuille reçoit déjà poids deux du centre et doit encore recevoir au moins
un voisin positif. Le voisinage du centre est un appariement. Les six feuilles
forment donc trois arêtes, et toutes les équations sont saturées : il n'y a aucune
arête vers le support négatif. Ce support pondéré est un **moulin de trois triangles**,
avec poids deux au centre. Il y en a exactement 99·C(7,3)=3465 dans le graphe.

Sur l'autre support, la somme des excès de degrés pondérés vaut aussi zéro. Il est
donc soit un moulin pondéré, soit un graphe cubique à huit sommets, anticomplet au
premier support. Si les deux supports sont binaires, le recensement complet à huit
sommets fournit exactement les sept possibilités suivantes.

| Code | Arêtes | Degrés | Partitions ordonnées en deux quatre-ensembles à quatre arêtes |
|---:|---:|---|---:|
| 2022000 | 12 | 3⁸ | 6 |
| 5683824 | 12 | 3⁸ | 4 |
| 5691760 | 12 | 3⁸ | 8 |
| 127305925 | 13 | 3⁶4² | 10 |
| 128354469 | 13 | 3⁶4² | 12 |
| 245715219 | 13 | 3⁶4² | 8 |
| 127242964 | 14 | 3⁴4⁴ | 16 |

Le dernier graphe est une grille 3×3 privée d'un sommet. Cela **ne suppose pas**
qu'il s'étend à une grille dans le graphe ambiant.

Deux supports binaires de même projection ont le même nombre d'arêtes, puisque
leur norme projetée vaut (24−2e)/7+64/63. Pour e=13, les deux sommets de degré
quatre de chaque support sont reliés par un appariement entre les supports.
Pour e=14, cet appariement relie les quatre sommets de degré quatre.

## 2. Classes cubiques et moulins : au plus cinq supports

Considérons les supports cubiques et les moulins pondérés ayant une même projection.
Deux supports distincts d'une telle classe sont disjoints.

Pour deux cubiques, une intersection laisserait une différence de masse au plus
sept. Les seuls cas possibles sont un prisme à six sommets ou D à sept sommets
(note 181). Supprimer un ou deux sommets d'un cubique à huit sommets laisse
respectivement neuf ou au plus sept arêtes, insuffisamment pour D ou un prisme.

Pour un moulin et un cubique qui s'intersectent, le centre du moulin doit être
dans le cubique : sinon il resterait une coordonnée 2 avec S≤7. Après annulation
partielle du centre, le support positif est un moulin avec éventuellement des
feuilles supprimées ; il possède un sommet de degré au plus deux et ne peut être
ni D ni un prisme. Pour deux moulins, un centre commun laisse seulement des
arêtes entre feuilles. Si les centres sont distincts, ils doivent tous deux être
dans l'autre support pour éviter une coordonnée 2 ; la différence de masse au plus
six laisse encore un support de degré minimum inférieur à trois. Ces intersections
sont donc également impossibles.

Les supports d'une classe sont ainsi disjoints et anticomplets. Sur les sommets
extérieurs à leur union, leur degré pondéré commun d vérifie

    Σd=88,       Σd²=128.

En effet Au=3u sur chaque support et A²=12I−A+2J. Cauchy donne au moins
ceil(88²/128)=61 sommets extérieurs. L'union des supports comporte au plus 38
sommets. Une classe contient donc au plus cinq supports ; si tous sont cubiques,
elle en contient au plus quatre.

Un moulin admet douze découpages en deux supports de taille quatre et quatre arêtes
se partageant son centre : on choisit trois des six feuilles, dont exactement une
paire complète. Notons t le nombre de découpages, soit 6,4,8 pour les cubiques et 12
pour un moulin. Une paire de supports de même projection produit exactement t_i t_j
paires de représentants `(4,4)` en collision. Les dix modèles finis correspondants
sont vérifiés dans `mass8_kernel_audit.py`.

Dans une classe de taille m≤5,

    Σ(i<j) t_i t_j ≤ (m−1)/2 · Σt_i² ≤ 2Σt_i².

En notant C_c les comptes des graphes à huit sommets, les collisions de cette
composante sont donc au plus

    72C_2022000 +32C_5683824 +128C_5691760 +997920.       (1)

Le dernier terme est 2·12²·3465.

## 3. Supports à treize arêtes : au plus cinq par classe

Les supports d'une classe de treize arêtes sont également disjoints. Supprimer un
sommet laisse neuf ou dix arêtes, jamais les onze de D ; supprimer deux sommets
en retire au moins cinq et ne laisse pas de prisme. Les intersections plus grandes
donneraient une différence propre non nulle de masse au plus cinq.

Pour une classe de m supports, chaque support a deux arêtes vers chacun des autres.
Sur les 99−8m sommets extérieurs, le degré commun d vérifie

    Σd=88−2m,       Σd²=114−2m.

La positivité de la variance impose

    (88−2m)² ≤ (99−8m)(114−2m).

Avec m≤12, cette inégalité impose m≤5.

Dans toutes les partitions du tableau, chacun des deux quatre-ensembles contient
un des sommets de degré quatre. Pour une orientation fixée de ces sommets, le
nombre de partitions vaut b=5,6,4 selon le type. Les deux arêtes entre supports
imposent des orientations compatibles : une paire de supports produit 2b_i b_j
paires de représentants en collision. Donc

    Σ(i<j) 2b_i b_j ≤ (m−1)Σb_i² ≤4Σb_i².

La perte de cette composante est au plus

    100C_127305925 +144C_128354469 +64C_245715219.         (2)

## 4. Supports à quatorze arêtes : contrôle des intersections

Ces supports peuvent s'intersecter. Dans une classe de m supports de même
projection, notons n_j le nombre de paires dont l'intersection a taille j.
Seules les valeurs j=0,1,2 sont possibles pour deux supports distincts.

Si u est une telle indicatrice, ||P4u||²=4/9. Pour u,v dans une même classe,

    <P3u,P3v> = |U∩V| −4/9−64/99 = |U∩V|−12/11.

En développant la norme carrée de la somme des P3u, on obtient

    12n0+n1 ≤38m+10n2.                                  (3)

Une paire d'intersection deux donne deux prismes jumeaux après suppression des
deux points communs Z. Pour passer de neuf à quatorze arêtes, Z doit être une
arête et chacun de ses sommets doit voir deux sommets du prisme. Ce sont donc
deux des trois sommets extérieurs complétant ses arêtes transversales en triangles.
Une paire de prismes jumeaux produit au plus trois telles paires de supports :
en sommant sur toutes les classes, Σn2≤3τ.

Pour deux supports disjoints, les quatre arêtes transversales apparient leurs
sommets de degré quatre. Parmi les seize partitions de chaque support, il existe
quatre profils possibles sur ces sommets, chacun de multiplicité quatre. Le
nombre de paires de partitions compatibles est au plus 4·4²=64, borne vérifiée
sur les vingt-quatre appariements possibles. Par (3), la perte de masse huit de
cette composante est donc au plus

    (608/3)C_127242964 +160τ.                             (4)

Les termes (1),(2),(4) contrôlent toutes les différences propres de masse huit
de la famille `(4,4)`. Ils ne contrôlent pas encore ses différences de masses
six et sept, ni ses collisions avec les représentants des familles antérieures.

## 5. Une autre exception à conserver pour la famille `(6,3)`

Une collision entre 1_W−1_Y, |W|=6,|Y|=3, et une indicatrice négative de six
sommets donne φ=1_W−1_Y+1_Z avec Aφ=3φ+1. Si une coordonnée négative subsiste,
sa somme de voisins doit être −2. Comme il y a au plus trois coordonnées négatives,
les trois doivent subsister, former un triangle et être anticomplètes à tout le
support positif. Ainsi deux branches doivent être examinées :

- Y est entièrement annulé par Z : le lemme non négatif ramène φ à une grille ;
- Y est un triangle entièrement non annulé, anticomplet à W∪Z : la partie positive
  est de masse douze, éventuellement avec des coordonnées deux.

La seconde branche n'est pas exclue par le lemme des grilles. Elle est propre aux
nouvelles familles avec trois coordonnées négatives et n'affecte pas les pertes
auditées des notes 179–181. LAB a revérifié cette distinction aux messages 210–211.

Reproduction : `python code/codex/mass8_kernel_audit.py`.
Les comptages finis et les bornes partielles sont archivés dans
`data/codex_mass8_kernel_audit.json`. Aucune nouvelle borne complète sur b4 n'est
déduite de cette note seule.
