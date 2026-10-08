# 198 — Moments des degrés et comptage exact du canal (9,0)

8 octobre 2026. Comptage pour six grilles proposé par LAB aux messages
289 et 293 ; généralisation uniforme et certificats par Codex, vérifiés
également à la main par LAB au message 295.

## 1. Le résultat combinatoire

Pour toute paire de prismes issue de deux grilles ayant la droite Θ en
commun, notons Z l'ensemble des 24 points sans voisin dans les deux
prismes. Si t est le nombre de triangles induits par Z, le nombre de
collisions internes de masse six entre représentants de forme `(9,0)` est
exactement

    C_90 = 5376 + 12t ≤ 5472.                            (1)

Les deux signes sont inclus. Dans un faisceau de six grilles, Z est la
réunion des quatre autres prismes, donc t=8 et C_90=5472 exactement.
L'identité (1), et pas seulement sa borne, vaut pour toute paire de grilles.

Ce résultat ne s'obtient pas en soustrayant deux plafonds d'optimisation.
Il provient d'un comptage exhaustif des trois points communs aux deux
représentants. Il améliore les modèles de la note 197 lorsqu'on y ajoute
les moments locaux des degrés décrits ci-dessous.

## 2. Degrés et types de triangles

On reprend la partition de la note 197 : les deux prismes X1,X2, les trois
apices Θ, les soixante points B qui voient un point de chaque prisme, et
les 24 points Z. Les apices forment un triangle, ne voient aucun point
de B et partitionnent Z en trois couleurs de huit points.

Chaque point de B a deux voisins dans X1∪X2, quatre dans Z et huit dans B.
Chaque point de Z a un voisin dans Θ, dix dans B et trois dans Z, dont
exactement un de chaque couleur. Ainsi

    e(B)=240,  e(B,Z)=240,  e(Z)=36.

Douze arêtes de Z relient des points de même couleur. Elles ont déjà leur
apex pour voisin commun ; elles n'appartiennent donc à aucun triangle de
Z ni à aucun triangle BZZ. Les 24 autres arêtes ont des couleurs
distinctes. Leur unique voisin commun est dans B ou dans Z. En notant
T_BBB, T_BBZ, T_BZZ les nombres de triangles des types indiqués, on a

    T_BZZ + 3t = 24.                                   (2)

Chaque arête BZ a son unique voisin commun dans B ou Z. Un triangle BBZ
ou BZZ contient deux arêtes BZ, d'où

    T_BBZ + T_BZZ = 120.                               (3)

Enfin, chaque sommet d'un des deux prismes voit dix points de B. Dans son
voisinage, ces dix points forment cinq arêtes disjointes : les deux
voisins de sa face sont déjà appariés, et son voisin de barreau est
apparié à son apex. Il y a donc exactement 12·5=60 triangles formés de
deux points de B et d'un point de X1∪X2. Le comptage des 240 arêtes de B
donne

    3T_BBB + T_BBZ + 60 = 240.                         (4)

On obtient

    T_BZZ = 24−3t,   T_BBZ = 96+3t,   T_BBB = 28−t.

Le nombre de chemins induits à trois points de B est donc

    60·binom(8,2) − 3T_BBB = 1596+3t.                 (5)

Un triangle de Z utilise trois couleurs distinctes. Chaque point de Z
n'a qu'un voisin dans chacune des deux autres couleurs et peut donc
appartenir à au plus un tel triangle. Cela prouve t≤8. Pour un faisceau
de taille m, les m−2 autres prismes fournissent déjà 2(m−2) triangles.

## 3. Énumération complète du canal (9,0)

Deux représentants positifs en collision s'écrivent X1∪W0 et X2∪W0,
où W0 est un trois-ensemble extérieur aux deux prismes. Si W0 contient
β points de B et α apices, sa contribution en arêtes vers chaque prisme
est β+2α. Une indicatrice de neuf points a norme huit exactement lorsque
son support a quatorze arêtes. Comme un prisme a neuf arêtes, la condition
sur W0 est

    e(W0) + β + 2α = 5.                               (6)

Les possibilités sont exhaustivement les suivantes.

| Type de W0 | Condition | Nombre |
|---|---|---:|
| BBB | Chemin induit de deux arêtes | 1596+3t |
| BBZ | Triangle | 96+3t |
| ΘBB | Les deux points de B sont adjacents | 720 |
| ΘBZ | L'apex voit z et z voit b | 240 |
| ΘZZ | Triangle avec une arête de Z de même couleur | 12 |
| ΘΘZ | z a la troisième couleur | 24 |

La somme vaut 2688+6t. Le signe négatif fournit le même nombre de paires,
ce qui prouve (1). Le programme contrôle indépendamment sur chaque patron
archivé que son coût `(9,0)` vaut deux si (6) est satisfaite, zéro sinon.

## 4. Les moments ajoutés au modèle

Les équations de degré de la note 197 portent sur des sommes dans chaque
cellule. Pour exploiter davantage les degrés individuels, on ajoute les
nombres de paires de voisins, avec ou sans restriction à une couleur.

Les quatre catégories de voisins utilisées sont B,Z0,Z1,Z2. Pour une
cellule de B, les degrés sont `(8, 2−r0, 2−r1, 2−r2)`, où r_c compte
ses deux voisins des prismes ayant la couleur c. Pour une cellule de Z,
ils sont `(10,1,1,1)`. Un apex a degré zéro vers B, huit vers sa couleur
et zéro vers les deux autres couleurs.

Pour toute cellule I, chaque sommet ayant les mêmes degrés d_S, on impose

    Σ_(v∈I) binom(d_S(v),2) = |I| binom(d_S,2),
    Σ_(v∈I) d_S(v)d_T(v) = |I| d_S d_T  (S≠T).         (7)

Les membres de gauche sont des sommes linéaires de patrons de trois
points : un centre dans I et deux extrémités adjacentes au centre.
L'arête éventuelle entre les extrémités n'est pas restreinte. Le programme
respecte les multiplicités lorsque plusieurs points sont dans une même
cellule. Il utilise les mêmes variables et bornes finies que la note 197.

L'identité (1) n'est pas ajoutée comme axiome au modèle. Deux optimisations
indépendantes dans le modèle m=2 donnent

    C_90−12t ≤ 5376,  −C_90+12t ≤ −5376,

après arrondi à l'entier pair, et retrouvent donc (1). Un troisième
certificat donne directement C_90≤5472. La première borne rationnelle
est exactement 5376 ; celle du sens opposé est
`−671999999999/125000000`, dont l'arrondi pair est −5376.

## 5. Plafonds conjoints

Les objectifs sont ceux de la note 197 : toutes les collisions binaires
de masse six à somme égale entre les familles de norme huit de support
au plus neuf, avec e(W)≤8 pour `(6,3)`, et toutes les formes `(9,0)`.
Les deux signes et les canaux croisés de cette collection sont inclus.

| Taille m du faisceau | Ancien plafond (note 197) | Nouveau plafond |
|---|---:|---:|
| 2 | 29144 | 27828 |
| 3 | 29142 | 27818 |
| 4 | 29140 | 27810 |
| 6 | 29140 | 27798 |

Le modèle m=2 n'interdit pas la présence d'autres prismes dans Z. Son
plafond est donc valable pour toute paire de grilles. Les raffinements
m=3,4,6 distinguent respectivement un, deux ou quatre autres prismes.

Le calcul dans le sens opposé donne également le nouveau plancher
uniforme, pour toute paire de grilles,

    C_6 par paire ≥ 16496,                              (8)

contre 14430 auparavant. Il est obtenu en majorant l'opposé du coût,
puis en utilisant la parité. L'intervalle `[16496,27828]` contient encore
la cible exploratoire d'environ 17900 de LAB ; il ne prouve ni l'existence
d'une configuration dans cet intervalle, ni l'échec de cette cible.

Les certificats de la composante F0 à triangles négatifs disjoints donnent :

| Taille m du faisceau | Ancien plafond (note 197) | Nouveau plafond F0 |
|---|---:|---:|
| 2 | 7056 | 6564 |
| 3 | 6970 | 6528 |
| 4 | 6872 | 6490 |
| 6 | 6660 | 6364 |

Par rapport à la borne générique 7304 de la note 195, le gain est de 940
pour m=6, soit environ 12,9 %. Il s'agit toujours d'une composante du
compte, et non d'un gain à soustraire une seconde fois du plafond conjoint.

## 6. Le plafond global

On reprend les 74 modèles de moments de la note 197, en remplaçant les
quatre coefficients de faisceau par ceux du tableau précédent. Le coût
des paires hors grille reste 31976 et leur variable est conservée dans
le modèle. Le résultat certifié est

    C_6 ≤ 39016713,  donc C_6 ≤ 39016712 par parité.     (9)

Le cas donnant la plus grande borne est encore s=56. Par rapport aux
40889844 de la note 197, le plafond baisse de **1873132**, soit environ
4,58 %. Il s'agit de la baisse d'une majoration certifiée ; aucun graphe
atteignant l'une ou l'autre borne n'est affirmé.

La portée de (9) reste celle de la note 197 : collisions de masse six
binaire, à somme égale, dans la collection de représentants spécifiée.
Les autres masses et les changements de somme ne sont pas inclus. Les
références globales τ≤1403 et b3≥45898 restent inchangées ; aucun nouveau
rang n'est exclu par cette note.

## 7. Reproduction

Le programme `code/codex/pencil_degree_moment_bounds.py` reprend les
patrons archivés de la note 197 et ajoute les équations (7). Les résultats
sont dans `data/codex_pencil_M_degree_moments.json.gz` pour M=2,3,4,6.
Chaque certificat est vérifié en arithmétique rationnelle, sans solveur,
avec les bornes finies des variables.

    python code/codex/pencil_degree_moment_bounds.py --size M --verify-only

Le programme `code/codex/pencil_weighted_moments.py` conserve le mode de
la note 197 et accepte un nouveau mode pour ces coefficients :

    python code/codex/pencil_weighted_moments.py --degree-moments --verify-only

Les 74 certificats globaux sont archivés dans
`data/codex_pencil_degree_weighted_moments.json.gz`.

Tous les certificats locaux et les 74 certificats globaux ont été relus
sans solveur après leur production. Le contrôle direct du coût `(9,0)`
est également refait sur tous les patrons à chaque reconstruction.
