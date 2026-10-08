# 205 — Deux apices denses : rang, discriminant et vraies relations

8 octobre 2026. Suite des notes 202–204. Le message 338 de LAB/LAP
demande de distinguer les relations effectives entre classes de grilles
du radical de leur Gram. Cette note apporte un calcul général du motif
(2,2,0), un test de discriminant au rang 37, et cette distinction précise.

**Résultats.** Pour r≥39, une droite dans six grilles ne peut pas avoir
deux points portant chacun trois droites dans six grilles. Si nh compte
les points portant exactement h telles droites, alors

    6n3≤n1+2n2,             donc n3≤24.                 (1)

Pour r=37, le motif n'est pas entièrement exclu. Parmi les 29 modèles
entiers des trois types de placements, quatre sont exclus par le rang
et trois autres par le discriminant. Les 22 restants passent ces tests
nécessaires ; ils ne sont pas des constructions de graphes.

## 1. Le type de la forme ambiante est fixé

Conservons L=Z⁹⁹∩E₋₄ et K⁺=L⊥∩Z⁹⁹. La note 101 prouve

    det L = det K⁺ = 9·7^(r−1).

Écrivons sur Z₇

    L=U₋ ⊥ 7V₋,       K⁺=U₊ ⊥ 7V₊.

Les V ont rang α=r−1, pair ; U₊ a rang D=56−r. Posons
m=(r−15)/2 et notons χ le caractère quadratique modulo sept.
La formule d'oddité de la note 101 donne

    χ(det V₋)=(-1)^m.

Les formes discriminantes de L et K⁺ sont opposées. Leurs matrices
sept-primaires sont V₋⁻¹/7 et V₊⁻¹/7 ; on a donc V₊≃−V₋ modulo sept.
Comme α est pair, leurs déterminants ont le même caractère. La partie
unité 9 du déterminant de K⁺ est un carré, d'où

    χ(det U₊)=χ(det V₊)=(-1)^m.                        (2)

| r | D | Caractère du déterminant de la forme non dégénérée |
|---|---:|---|
| 37 | 19 | non carré |
| 39 | 17 | carré |
| 41 | 15 | non carré |
| 43 | 13 | carré |

Ainsi, **au rang 37, un Gram de rang 19 doit avoir un mineur principal
non singulier de déterminant non carré**. Ces dix-neuf vecteurs donnent
une base de l'espace non dégénéré ; un changement de base multiplie le
déterminant par un carré. Un déterminant carré est donc une obstruction
même lorsque le plafond du rang est respecté.

La classe de 1 a norme 99≡1. Son complément orthogonal a dimension
55−r et déterminant de caractère (-1)^((55−r)/2) : il est de type
hyperbolique. Seul le caractère (2) est nécessaire aux exclusions ci-dessous.

## 2. Les 225 placements du motif (2,2,0)

Autour de Θ dans six grilles, on reprend les six prismes Xk, les
cellules D et les quatre-vingt-dix mots de colonnes de la note 203.
Deux apices ont chacun deux droites universelles supplémentaires :

    |U0|=|U1|=2,       U2=∅.

Cela force six grilles Gk et neuf grilles H à chacun des deux apices,
soit **24 grilles**. Les 15² placements se divisent en trois types
selon que U0 et U1 sont identiques, se coupent en un indice ou sont
disjoints. Il s'agit de renommages, sans automorphisme présumé du graphe.

Le modèle impose exactement les mêmes conditions nécessaires que la
note 203 : marges de deux coordonnées, marges de serrage des grilles
existantes, multiplicité au plus un si deux cellules complètes la
déterminent, au plus quatre autrement. Les colonnes restent entières.

| U0 ; U1 | Placements | Variables libres | Affectations examinées | Solutions | Rangs et déterminants principaux modulo 7 |
|---|---:|---:|---:|---:|---|
| 01 ; 01 | 15 | 7 | 78125 | 15 | 12 de rang 19, det 5 ; 3 de rang 19, det 1 |
| 01 ; 02 | 120 | 5 | 3125 | 6 | 6 de rang 19, det 3 |
| 01 ; 23 | 90 | 6 | 15625 | 8 | 4 de rang 18, det 3 ; 4 de rang 20, det 1 |

Les déterminants sont ceux des bases de colonnes choisies par le
programme ; leur valeur peut varier sous changement de base, mais
leur caractère quadratique est invariant. Les non-carrés sont 3,5,6.

Pour r≥39, le plafond ambiant est au plus 17, alors que les 29 Grams
ont rang au moins 18. Chaque modèle possède un mineur d'ordre dix-huit
non nul archivé. Le motif est donc exclu dans tous les placements.

Pour r=37, les quatre solutions de rang vingt sont exclues. Les trois
solutions de rang dix-neuf et déterminant un sont exclues par (2).
Les douze de déterminant cinq, les six de déterminant trois et les
quatre de rang dix-huit demeurent possibles à ce niveau de contraintes.

## 3. Conséquence globale pour r≥39

Une droite dans six grilles ayant deux points de type h=3 réaliserait
un des motifs précédents : chacun fournit deux droites supplémentaires
à l'apex correspondant. Elle a donc au plus un point de type trois.

Si ah compte ses points de type h, alors 2a3≤a1+a2. En sommant sur
les droites dans six grilles, un sommet de type h est compté h fois :

    6n3≤n1+2n2≤2(99−n3).

Cela prouve (1). La borne précédente était n3≤39 pour r≥37. Le nouveau
plafond 24 porte uniquement sur r=39,41,43 et sur les sommets de type
trois ; il ne majore pas à lui seul le nombre total de grilles.

## 4. Radical du Gram et relations effectives

Soit S le sous-espace engendré par une famille dans un espace non
dégénéré W de dimension D. Notons d=dim S et q le rang de son Gram.
Alors

    q=d−dim(S∩S⊥),       dim(S∩S⊥)≤D−d,

donc

    q≤d≤floor((D+q)/2).                                (3)

En particulier, **si D=19 et q=18 ou 19, alors d=q**. Le Gram n'a
aucune dégénérescence interne à S ; tout vecteur de coefficients dans
le noyau du Gram est une vraie relation entre les classes. On peut
donc répondre à la question de LAB dans ces deux cas, sans témoin
supplémentaire. Pour des rangs plus petits, la distinction reste nécessaire.

Dans la famille de 24 grilles du §2, ajoutons la classe de 1. Les cinq
droites universelles connues (Θ et les quatre supplémentaires) donnent
cinq relations indépendantes :

    Σ_(G contenant la droite) [1G] = 5[1].

Leur indépendance se voit par une grille H^i_kj avec k dans Ui et j
hors Ui : son coefficient isole celui de la relation de k. La relation
de Θ reste ensuite seule. Le programme vérifie aussi leur rang cinq
et leur annulation dans le Gram augmenté, où les produits avec 1
valent deux et sa norme vaut un.

Puisque 1 appartient déjà à l'espace engendré par les six Gk, le rang
du Gram augmenté est inchangé. Pour les candidats compatibles avec
r=37, la dimension réelle est donc dix-neuf ou dix-huit, par (3).
Les 25 colonnes ont respectivement six ou sept relations indépendantes :
**une ou deux de plus que les cinq relations de faisceaux connues ici**.

Cette dernière phrase est locale. Des relations de faisceaux extérieurs
pourraient, par combinaison, produire une relation portée par cette
famille. On n'en déduit pas une borne sur le nombre global de relations
supplémentaires après quotient par tous les faisceaux.

### Convention sur le quotient

Posons N=A−3I modulo sept et M=K⁺/7K⁺, plongé dans F₇⁹⁹ par primitivité.
Le radical de M n'est pas toute l'image de N :

    R=im N ∩ 1⊥,        dim R=r−1,
    im N=R ⊕ ⟨1⟩.

En effet, N1=4·1, N²=2J et (A+4I)≡N. Les colonnes de A+4I sont
dans K⁺ ; leurs combinaisons de somme de coefficients nulle sont
orthogonales modulo sept à K⁺. Leur dimension r−1 identifie R.
La forme non dégénérée de dimension 56−r est celle sur M/R.

Les classes centrées g′=[1G]−2[1] appartiennent à 1⊥. Pour leurs
combinaisons, « appartenir à im N » est bien le critère de relation.
Pour une combinaison non centrée ΣaG[1G]+k[1], il faut aussi
2ΣaG+k=0 modulo sept. Sans cette condition, [1] lui-même donnerait
à tort une relation nulle, alors qu'il a norme un.

Si p est le rang global des relations de faisceaux et c le nombre
de relations indépendantes supplémentaires, la formule correcte est

    dim⟨g′⟩=ρ−p−c,       p≤x6,

où x6 est le nombre de droites dans six grilles. Elle implique bien
ρ≤55−r+x6+c. L'égalité dim⟨g′⟩=ρ−x6−c suppose en plus l'indépendance
de toutes les relations de faisceaux.

## 5. Un test pour ajouter une grille à une famille de rang dix-huit

La famille commune de 21 grilles de la note 202, avec un même indice
universel supplémentaire aux trois apices, a rang dix-huit et un
déterminant principal non carré (le programme trouve cinq).
Au rang 37 son espace est non dégénéré, et son complément orthogonal
est une droite de norme carrée, par (2).

Choisissons une base de Gram B dans cette famille. Pour une nouvelle
grille, soit b le vecteur de ses intersections avec cette base. Son
résidu de norme est

    Δ=2−bᵀB⁻¹b modulo sept.

Il faut alors **Δ∈{0,1,2,4}**. Après compatibilité avec les relations
de la famille entière, Δ=0 détermine une seule classe et Δ non nul
au plus deux. Deux grilles distinctes ne peuvent avoir la même classe,
car leur intersection devrait valoir deux modulo sept, impossible
parmi 0,1,3.

Lorsque Δ=2, les deux classes possibles ne peuvent même pas coexister :
leur produit serait 2−2Δ=5, également impossible. Ce test est prêt
à être utilisé pour des grilles témoins supplémentaires ; aucune
énumération complète de ces extensions n'est revendiquée ici.

## 6. Certificats et reproduction

    python code/codex/grid_kernel_rank_two_dense_apices.py --verify-only

L'archive `data/codex_grid_kernel_rank_two_dense_apices.json.gz`
contient les trois orbites, les combinaisons rationnelles de réduction
des 90 variables, les 29 solutions, les mineurs d'ordre dix-huit et les
bases principales avec leurs déterminants. Le vérificateur reconstruit
les équations, contrôle les réductions exactement, refait toutes les
affectations entières et calcule les déterminants modulo sept.

Il vérifie aussi les cinq relations locales, les caractères imposés
par l'identité d'oddité de la note 101 et le type de la famille de
rang dix-huit du §5. Il ne redémontre pas le théorème de genre de la
note 101. Aucun solveur numérique n'intervient. Génération et
vérification ont été exécutées avec succès.
