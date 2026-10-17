# 209 — Deux étoiles couplées sur une arête : 38 types à P=S=0

8 octobre 2026. Suite de l'audit 207. Le présent couplage concerne les
étoiles d'ombres autour d'une droite T, et non les étoiles de cellules
employées dans d'autres sections du corpus.

**Résultat.** Si P=0 et si uv est une arête entre deux couches du graphe
cubique G(T), les deux étoiles lointaines de u et v partagent exactement
un apex. Les arêtes entre leurs neuf autres ombres forment un couplage
de taille 7+c₄(uv). En particulier c₄(uv)≤2. À P=S=0, leur union a
exactement 38 types abstraits non étiquetés. Cette contrainte est
uniforme et couple effectivement deux étoiles ; aucun de ces types
n'est ici déclaré irréalisable par des ombres.

## 1. Notations et hypothèses

T est une droite du SRG hypothétique (99,14,1,2). G=G(T) est le graphe
cubique sur ses 36 voisins, répartis en trois couches A,B,C. F est
l'ensemble des 60 sommets lointains. N est la matrice 36×60 des ombres
et A_F l'adjacence induite sur F. On a exactement, en entiers,

    NNᵀ = K = 12I − G + 2J − G² − D,
    NA_F = 2J − (G+I)N,
    D = diag(J₁₂,J₁₂,J₁₂).

Fixons u,v de couches différentes, avec u~v dans G. Nous supposons
P=0. Alors G est sans triangle, et le voisinage de chaque sommet du
SRG est un couplage de sept arêtes.

Les ensembles Sᵤ={y∈F:n_y(u)=1} et Sᵥ ont dix éléments chacun. Le
graphe induit sur chaque étoile est 4K₂+2K₁ : les deux isolés sont
appariés aux deux voisins transversaux de son centre, et les huit
autres sommets s'apparient entre eux.

## 2. Un apex commun et un troisième couplage

Les sommets adjacents u,v ont un unique voisin commun w. Il ne se
trouve ni sur T, ni dans G, puisque G est sans triangle. Donc

    Sᵤ ∩ Sᵥ = {w}.

Le triangle uvw fait de w un apex des deux étoiles. Il est isolé dans
le graphe induit sur Sᵤ∪Sᵥ.

Posons U=Sᵤ−{w} et V=Sᵥ−{w}, chacun de taille neuf. Pour z∈V,
l'équation mixte donne

    deg_{Sᵤ}(z) = 2 − (Gn_z)ᵤ ≤ 1,

car v appartient à n_z et v~u. La même propriété vaut dans l'autre
sens. Les arêtes entre U et V forment donc un **couplage**.

Son cardinal t se calcule sans connaître A_F :

    t = Nᵤ A_F Nᵥᵀ = 20 − Kᵤᵥ − (GK)ᵤᵥ.

Ici Kᵤᵥ=1. Comme GD=J et G²ᵤᵥ=0,

    (GK)ᵤᵥ = 17 − (G³)ᵤᵥ.

Dans un graphe cubique simple sans triangle, les marches de longueur
trois de u à v sont les cinq marches avec retour immédiat et les
chemins correspondant aux quatre-cycles contenant uv. Ainsi

    (G³)ᵤᵥ = 5 + c₄(uv),
    t = 7 + c₄(uv).                                      (1)

Le couplage entre deux ensembles de taille neuf impose c₄(uv)≤2.

## 3. Classification des graphes abstraits du couplage

Sur U∪V, il y a huit arêtes internes (quatre par étoile) et 7+c₄
arêtes transversales. C'est l'union de deux couplages : chaque
composante est un chemin, sommet isolé compris, ou un cycle.

Sur un cycle, arêtes internes et transversales alternent. Le nombre
d'arêtes transversales est pair, puisqu'elles échangent U et V ; la
longueur du cycle est donc divisible par quatre.

Un cycle de longueur quatre produirait deux triangles, l'un centré
en u et l'autre en v, reliés par les trois barreaux uv et les deux
arêtes transversales. Ce serait un prisme, exclu par P=0. Les cycles
possibles ont donc longueurs 8,12,16 ; deux cycles de longueur 8 sont
également possibles au seul niveau abstrait.

Avec 18 sommets et 15+c₄ arêtes, le nombre de composantes chemins est

    p = 18 − (15+c₄) = 3−c₄.                            (2)

On énumère donc les partitions de 18−Σ(longueurs des cycles) en p
longueurs positives de chemins. Le vérificateur construit, pour
chaque type obtenu, une coloration U/V avec neuf sommets de chaque
côté, quatre arêtes internes de chaque côté et le bon couplage
transversal. C'est une réalisation du patron abstrait, pas du SRG.

| c₄(uv) | Couplage transversal | Chemins | Types abstraits |
|---:|---:|---:|---:|
| 0 | 7 | 3 | 38 |
| 1 | 8 | 2 | 19 |
| 2 | 9 | 1 | 5 |

À P=S=0, G a maille au moins cinq (note 125), donc c₄=0. Il reste
soit trois chemins sur 18 sommets, soit un cycle de longueur 8 et
trois chemins sur 10 sommets, soit un cycle de longueur 12 et trois
chemins sur 6 sommets. Les nombres de partitions sont 27,8,3, soit
**38 types**. Il faut toujours ajouter l'apex commun isolé w.

Ce compte oublie les étiquettes des ombres, leur choix dans les
couches et les contraintes supplémentaires du SRG. Il réduit les
formes possibles du couplage ; il ne classe pas les solutions.

## 4. Le véritable espace de Green a dimension 33

Supposons maintenant T générique : H=3I−G a nullité un sur F₇.
L'espace V des vecteurs dont les sommes sur les trois couches sont
nulles a dimension 33. Les indicatrices des couches engendrent un
complément non dégénéré, puisque 12 n'est pas nul modulo 7.

Sur V, D et J s'annulent. On a

    K|_V = −H²|_V,

car K≡−H²−D+2J modulo 7. H est inversible sur V, donc K aussi.
Sur les indicatrices de couches e_A,e_B,e_C, K e_i=20·1 : les
différences de couches forment le noyau de K et K·1=60·1≠0. Ainsi

    rang₇ K = 34.

Chaque colonne de N a deux points dans chaque couche, donc rang N≤34.
L'égalité NNᵀ=K force rang N=34. En posant x_y=n_y−6·1, les colonnes
x_y appartiennent à V et l'engendrent. En effet la projection de
im N, de dimension 34, sur V retire précisément la direction 1,
présente puisque N·1=10·1.

L'inverse de Green H⁺=(H+J)⁻¹−J s'annule sur 1 et est non dégénéré
sur V. Par conséquent

    Z=NᵀH⁺N=(x_yᵀH⁺x_z)_{y,z},       rang₇ Z=33.         (3)

La dimension 35 du complément de 1 est donc un plafond trop large
pour ces ombres. Les deux contraintes de couches supplémentaires
doivent être conservées. Une identité utile est

    H⁺KH⁺ = −I+3D = −projection_V.

Le script vérifie ces formules de matrices, ainsi que (1), sur la
boule cyclique (2,4,1). Il ne construit pas de matrice N complète
pour cette boule, déjà exclue par la note 207.

## 5. Gram prescrit des deux étoiles au rang 37

Lorsque le résidu générique est nul (rang global 37), le Gram des
19 ombres de Sᵤ∪Sᵥ est

    3I₁₉+3J₁₉−A_{Sᵤ∪Sᵥ}.

Si sᵤ et sᵥ sont les sommes des dix ombres respectives, le Gram sur
(sᵤ,sᵥ,n_w) vaut

    [ 0    2−c₄    5 ]
    [ 2−c₄   0     5 ]                 dans F₇.
    [ 5      5     6 ]

Le catalogue exact donne les rangs suivants :

| c₄ | Rang 15 | Rang 16 | Rang 17 | Rang 18 | Rang 19 |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 3 | 6 | 9 | 20 |
| 1 | 1 | 1 | 5 | 3 | 9 |
| 2 | 1 | 0 | 2 | 0 | 2 |

Ces Grams restent tous représentables dans un espace non dégénéré
de dimension 33. Même si les 19 vecteurs étaient indépendants,
adjoindre un dual à leur radical demanderait une dimension
38−q≤23, inférieure à 33. Le rang abstrait seul ne tue donc pas ces
patrons. Le test utile doit imposer simultanément les **supports
binaires des ombres**, leurs sommes entières et ce couplage précis,
ou relier davantage d'étoiles.

Fichiers : `code/codex/two_star_edge_coupling.py` et
`data/codex_two_star_edge_coupling.json`.

    python code/codex/two_star_edge_coupling.py --verify-only
