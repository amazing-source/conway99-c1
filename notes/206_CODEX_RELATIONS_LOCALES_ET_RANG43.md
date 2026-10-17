# 206 — Relations locales de grilles, Laplacien sans signe et borne au rang 43

8 octobre 2026. LAB/LAP ont fourni au message 341 la relation « quatre
droites contre trois » et une classification numérique des relations
obtenues dans le voisinage fermé d'un sommet. Codex en donne ici une
description générale, sa liaison avec le Gram et une conséquence au rang 43.

**Résultats.** La relation proposée est une identité entière avant
réduction modulo sept. Les relations construites dans une boule de
sommet sont paramétrées exactement par les composantes biparties du
complémentaire du graphe local de grilles. Au rang 43, on obtient

    e(Ξv)≤15 pour chaque sommet v,
    τ≤1326,                    b3≥46000.

Les deux dernières bornes remplacent respectivement 1354 et 45964
pour ce rang. Elles ne sont pas annoncées pour les rangs 37,39,41.

## 1. Coordonnées locales indépendantes des arêtes lointaines

Fixons v. Ses sept droites sont ℓ0,…,ℓ6, chacune avec deux autres
points. Chaque sommet à distance deux de v a exactement deux voisins
dans N(v), sur deux droites différentes. Réciproquement, chaque paire
de points de deux droites différentes a, outre v, un unique voisin
commun. Les 84 points lointains sont ainsi répartis en quatre coins
pour chacune des 21 paires de droites.

Soit X=Ξv le graphe sur les sept droites : ij est une arête quand
elles engendrent une grille Gij. Cette grille est constituée de v,
des quatre points des deux droites, et de leurs quatre coins.

Écrivons B=A+4I. Si y est porté par N[v], de valeur yv en v et de
valeur yi aux deux points de ℓi\{v}, alors By vaut exactement

- 4yv+2Σyi en v ;
- 5yi+yv aux deux points de la droite i ;
- yi+yj aux quatre coins de la paire ij.

Toutes ces coordonnées sont connues, sans aucune arête lointaine.

## 2. La relation « quatre contre trois » est entière

Supposons les sept droites partagées en un ensemble I de quatre
droites deux à deux en grille et un ensemble J de trois droites
deux à deux en grille. Les grilles entre I et J peuvent exister ou non.
Posons

    y=−ev+1_(union des huit points des droites de I, hors v).

Le contrôle aux quatre types de coordonnées précédents donne, dans Z⁹⁹,

    By = Σ_(ij⊂I) 1_Gij − Σ_(ij⊂J) 1_Gij + 1.          (1)

En v, les deux côtés valent quatre. Sur une droite de I ils valent
quatre, sur une droite de J moins un. Aux coins, ils valent deux,
zéro ou un selon les appartenances à I et J. C'est donc une identité
exacte, plus forte que sa seule réduction modulo sept.

On a Σy=7. Dans l'espace non dégénéré de K⁺ modulo son radical,
[By]=4(Σy)[1]=0. En posant g′G=[1G]−2[1], (1) donne

    Σ_(ij⊂I) g′Gij = Σ_(ij⊂J) g′Gij.                  (2)

Il s'agit bien d'une relation entre neuf grilles, sans hypothèse de
faisceau à six grilles et sans modèle canonique de colonnes.

## 3. Toutes les relations construites dans une boule de sommet

Soit H le complémentaire de X sur les sept droites. Considérons z∈F₇⁷
tel que

    zi+zj=0 pour chaque arête ij de H.                  (3)

Posons Z=Σzi et, pour ij arête de X, aij=zi+zj. Alors le vecteur porté
par N[v] défini par yv=Z et yi=zi vérifie

    By=Σ_(ij∈E(X)) aij 1_Gij.                          (4)

Pour le voir, les coins utilisent directement (3). Sur la droite i,
la somme des coefficients incidents est

    Σ_(j adjacent à i dans X)(zi+zj)=5zi+Z,

car les non-voisins contribuent l'opposé de zi. Enfin Σaij=6Z,
ce qui vérifie la coordonnée en v. La somme des coordonnées de y
vaut 3Z. En centrant (4), on obtient donc

    Σ aij g′Gij=0.                                    (5)

La condition (3) a une base entière particulièrement simple : sur
une composante bipartie de H, prendre +1 sur une partie et −1 sur
l'autre, zéro ailleurs. Un sommet isolé constitue une composante
bipartie et fournit son propre vecteur unité. Une composante avec
un cycle impair ne fournit aucun paramètre, puisque 2 est inversible.
Ces vecteurs satisfont (3) sur Z ; leurs identités (4) sont donc
entières, pas seulement modulo sept.

### Complétude dans la classe de témoins considérée

Supposons plus généralement By=Σaij1_Gij+k1 modulo sept, avec y
porté par N[v]. Les quatre coins de chaque paire de droites imposent
d'abord que y soit constant sur les deux points de chaque droite.
Ils donnent yi+yj=k sur les non-arêtes et aij=yi+yj−k sur les arêtes.

En posant zi=yi−k/2, on retrouve (3). Les équations aux points des
droites donnent yv=Z−3k/2 ; l'équation en v suit automatiquement.
Le paramètre k seul ne produit aucun coefficient de grille. L'espace
des relations de coefficients obtenues ainsi est donc exactement
l'image de (3) par z↦(zi+zj)_(ij∈E(X)). Cette application est injective :
si tous ces coefficients s'annulent, les sommes zi+zj s'annulent sur
toutes les paires de K7, donc z=0.

**Sa dimension est le nombre b(H) de composantes biparties de H.**
Les sommets isolés de H sont les droites dans six grilles et redonnent
les relations de faisceaux. Les autres composantes biparties donnent
les relations locales supplémentaires.

Cette complétude concerne les témoins y portés par N[v]. Des relations
avec témoin plus étendu peuvent exister. Les relations obtenues à des
sommets différents ne sont pas déclarées indépendantes.

## 4. Dix-sept types avec une relation locale supplémentaire

Les degrés de X appartiennent à {0,1,2,3,4,6}. Tout degré non nul
de H est donc au moins deux. Une composante bipartie non triviale
de H a au moins quatre sommets ; il ne peut y en avoir deux sur sept
sommets. Il y a donc **au plus une relation supplémentaire par sommet**
au-delà de celles de ses droites dans six grilles.

Le programme énumère directement les graphes bipartis de quatre à
sept sommets, de degré minimal deux, par toutes leurs matrices entre
les deux parties. Il quotient les permutations des parties et,
lorsqu'elles ont même taille, leur échange. Les sommets restants
sont isolés, sauf une possibilité de triangle lorsque la composante
bipartie a quatre sommets. Cela couvre tous les cas, sans utiliser
une liste externe de graphes non isomorphes.

On retrouve **17 types**, avec 17 profils (e,c,h2,u6) distincts,
en accord avec LAB. L'archive donne pour chacun les arêtes de H,
le vecteur signé z, les coefficients de (4), le profil et le rang du
Gram. L'identité entière est contrôlée sur les 99 coordonnées.

## 5. Le noyau du Gram vient du Laplacien sans signe

Soit C la matrice d'incidence sans signe de X, de taille 7×e, et

    QH=Diag(deg H)+A_H.

Deux grilles passant par v ont pour intersection v seul, une droite,
ou la grille entière si elles coïncident. Le Gram de leurs classes
centrées est donc

    Γ=4I_e+2CᵀC−3J_e modulo sept.                      (6)

Comme Cᵀ1=2·1, posons T=4I₇+2J₇. Sur F₇, J₇²=0 et
T⁻¹=2I₇−J₇. On vérifie

    Γ=4(I_e+CᵀTC),
    T⁻¹+CCᵀ=−QH.

L'application z↦Cᵀz est ainsi une bijection de ker QH vers ker Γ.
Son inverse sur ce noyau est a↦−TCa. Par conséquent,

    rang₇ Γ=e−nullité₇ QH.                            (7)

En ajoutant [1], de norme un et orthogonal aux classes centrées,
le rang devient e+1−nullité₇ QH.

Les b(H) vecteurs du §3 sont dans ker QH. Mais ce noyau peut être
plus grand modulo sept : les facteurs de Smith non nuls de QH
divisibles par sept y ajoutent des dimensions. Cette distinction
sépare les relations locales déjà prouvées du surplus de noyau du
Gram. Ce surplus peut correspondre à une dégénérescence de la famille
ou à des relations obtenues avec d'autres témoins ; (7) ne tranche
pas à lui seul entre les deux.

## 6. Au rang 43, au plus quinze grilles par sommet

Au rang 43, l'espace non dégénéré de K⁺ a dimension treize. Si e≥16,
la borne e≤17 laisse quatre ou cinq arêtes dans H, dont tous les
degrés non nuls sont au moins deux. À renommage près, il reste exactement
trois possibilités :

| H | e | Nullité₇ QH | Rang avec [1] |
|---|---:|---:|---:|
| C4 et trois isolés | 17 | 4 | 14 |
| C5 et deux isolés | 16 | 2 | 15 |
| K4 privé d'une arête et trois isolés | 16 | 3 | 14 |

En effet, un graphe simple de quatre ou cinq arêtes, sans degré un,
ne peut avoir deux composantes non triviales. Le cas à quatre arêtes
est C4 ; à cinq arêtes, le support est un C5 ou un K4 privé d'une arête.
Les trois rangs dépassent treize. Cela prouve **e(Ξv)≤15** pour r=43.

## 7. Certification des conséquences globales au rang 43

Le modèle de la note 204 est restreint aux **174 profils** ayant e≤15.
On utilise également la coupure de la note 205,

    6n3≤n1+2n2,

valable pour r≥39. Les cinq égalités de moments, l'expansion, les bornes
sur P et ρ et le domaine 0≤s≤73 restent ceux des notes 196 et 204.

Les 74 certificats rationnels donnent, pour l'objectif majorant τ,

    max_s plafond(s)=63653/48=1326+5/48,

avec la plus grande valeur pour s=23. L'intégralité donne **τ≤1326**.
L'ajout de cette contrainte au système de recensement et de classes de
triangles lointains donne une identité duale exacte prouvant **b3≥46000**.
Cette dernière preuve n'affirme pas l'existence d'un point rationnel
atteignant la relaxation ; la combinaison non négative suffit à la borne.

## 8. Reproduction et portée

    python code/codex/grid_vertex_relations.py --verify-only

Archives :

- `data/codex_grid_vertex_relations.json` : les 17 types, les identités
  entières et les trois obstructions denses au rang 43 ;
- `data/codex_rank43_vertex_moments.json.gz` : les 74 certificats ;
- `data/codex_rank43_vertex_b3_bound.json` : le certificat dual de b3.

La génération et la vérification passent. Les identités locales et les
rangs sont vérifiés exactement. Les poids des optimisations sont découverts
numériquement puis contrôlés avec des fractions rationnelles et des bornes
finies ; la vérification n'appelle aucun solveur.

La formule générale des relations vaut pour tout rang. Les améliorations
τ≤1326 et b3≥46000 utilisent r=43. Elles ne constituent pas à elles seules
une exclusion de ce rang. Le comptage du rang des relations entre plusieurs
voisinages reste nécessaire pour une borne globale sur le nombre de grilles.
