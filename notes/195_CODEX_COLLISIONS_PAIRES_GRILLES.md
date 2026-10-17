# 195 — Pertes séparées par type de paire de prismes

8 octobre 2026. Séparation proposée par LAB au message 269 ; modèles locaux,
énumérations et certificats rationnels par Codex. Cette note complète les
canaux de **masse six binaire** à somme égale pour les familles précisées
ci-dessous. Elle ne ferme pas les masses sept à neuf ni les changements de
somme de neuf, et n'exclut pas le rang 37.

## 1. Résultats utilisables

Tous les nombres sont des majorations de paires non ordonnées de
représentants en collision, **avec les deux signes**, par paire non ordonnée
de prismes jumeaux. « Grille » signifie que leurs trois apices Θ forment
un triangle ; sinon la paire est dite hors grille.

| Canal de norme huit | Paire de grilles | Paire hors grille |
|---|---:|---:|
| `(6,3)` interne, e(W)≤8 | 12182 | 12814 |
| `(6,3)` contre `(5,2)` | 2256 | 2304 |
| `(6,3)` contre `(4,1)` | 1488, exact | 1488, exact |
| `(6,3)` contre `(3,0)` | 0, exact | 0, exact |
| `(4,4)` interne et contre les anciennes familles équilibrées | 2166 | 2178 |
| `(7,1)` interne et contre `(6,0)` | 4128 | 4212 |
| Tous les canaux précédents et les anciens, sans `(9,0)` : maximum conjoint | **22422** | **23150** |
| Même total, avec tous les `(9,0)` de norme huit | **29204** | **31976** |

La première borne était 12814 pour tout type de paire : le gain sur la
branche grille est 632. Pour `(4,4)`, la borne précédente sur cette même
branche était 2646 ; le gain est 480, soit environ 18 %.

Pour la norme six, les collisions **internes** de `(6,3)`, e(W)≤8, sont
majorées par **738** sur les paires de grilles et **756** hors grille.
Il ne s'agit pas d'un audit de toutes les familles de norme six.

Si τ_g et τ_n comptent les deux types de paires, le total de masse six
binaire de norme huit pour la collection sans `(9,0)` satisfait donc

    C_6 ≤ 22422 τ_g + 23150 τ_n.

Avec tous les `(9,0)`, une borne sûre est

    C_6 ≤ 29204 τ_g + 31976 τ_n.

Les ensembles positifs de `(6,3)` restent limités à e(W)≤8 dans ces deux
formules. Les `(9,0)` sont les indicatrices signées de tous les neuf-ensembles
à quatorze arêtes. Toute collision de masse six entre ces derniers utilise
des supports contenant un prisme. Ce canal ne doit donc pas être imputé à
une sous-famille qui exclut ces supports.

Ces coefficients sont des **plafonds certifiés**, pas des coûts minimaux ni
des valeurs réalisées dans un graphe. Leur taille montre que les plafonds
actuellement démontrés ne suffisent pas au budget communiqué par LAB ; elle
ne prouve pas l'impossibilité d'une méthode de comptage par paires.

## 2. Ce qui change dans le modèle local

La paire de prismes fixée utilise douze sommets. Les 87 points extérieurs
ont les quarante profils de la note 188 : Z de taille 24, 36 cellules
simples totalisant 60 points, et trois apices de multiplicité un.

Les variables comptent les arêtes entre cellules et les configurations
induites de trois points extérieurs. On conserve toutes les équations de
degré, de voisins communs, de marges d'arêtes et de triangles de la note
188, avec leurs bornes combinatoires finies. Le modèle a 64147 variables
et 89154 lignes avant les contraintes supplémentaires.

Pour une paire de grilles, les trois arêtes entre apices valent un, et
aucun apex ne voit de point simple : d_B(a)=4−2d_Θ(a)=0. Hors grille,
on impose seulement e(Θ)≤2 ; ignorer la structure précise des deux arêtes
éventuelles conserve une relaxation sûre.

Les objectifs des différents canaux portent sur **les mêmes variables**.
Les plafonds conjoints du tableau sont donc obtenus en maximisant la somme
des coûts, plutôt qu'en additionnant les plafonds individuels.

## 3. Paramétrisation des collisions entre familles

On écrit ψ=1_W−1_Y, avec |W|=p, |Y|=q, et de même (p′,q′) pour ψ′.
Pour une différence binaire de masse six et de somme zéro,

    p−q=p′−q′,
    r=(p+q+p′+q′−12)/2

est le nombre de points communs de même signe hors des deux prismes.
Si c de ces r points sont positifs, ψ utilise p−c points positifs dans
le premier prisme et q−r+c points négatifs dans le second. Le partenaire
est exactement ψ′=ψ−1_X+1_X′.

Le programme énumère tous ces choix pour r=0,1,2,3. La norme est calculée
par la forme entière

    Q(ψ)=3||ψ||²−ψᵀAψ+(Σψ/3)².

Pour `(6,3)`, on exige également e(W)≤8 pour chaque membre appartenant
à cette famille. Les familles équilibrées contiennent déjà leurs opposés ;
les autres comptes sont multipliés par deux. Entre familles différentes,
on compte les deux orientations de la différence de prismes.

Les patrons sont au nombre de 1, 40, 1526 et 63342 selon r. Un calcul
indépendant par matrices complètes contrôle la norme et les tailles des
supports sur chaque classe de degrés, d'arêtes et de coûts. Les 1526 coûts
internes de `(4,4)` sont en outre comparés, un à un, à la formule locale
indépendante déjà vérifiée dans la note 185.

Les canaux ne faisant intervenir aucun couple de points extérieurs ont
les nombres **exacts** suivants, indépendamment du type de paire :

| Canal | Nombre |
|---|---:|
| `(6,3)`–`(3,0)` | 0 |
| `(6,3)`–`(4,1)` | 1488 |
| `(7,1)`–`(6,0)` | 1224 |
| `(6,0)` interne | 0 |
| `(5,2)`–`(4,1)` | 216 |
| `(5,2)` interne | 216 |
| `(4,4)`–`(2,2)` | 162 |
| `(4,4)`–`(3,3)` | 792 |
| `(3,3)` interne | 48 |

En particulier, les anciennes familles contribuent au total 480 par paire,
soit les 432 de la note 181 plus les 48 de `(3,3)`. Cette contribution
est incluse une seule fois dans les plafonds conjoints de la section 1.

## 4. F0 : identifier la composante à traiter par classes

F0 désigne W à six sommets et sept arêtes moins un triangle Y anticomplet,
avec les deux signes. Les nouveaux plafonds de la branche grille sont :

| Famille et portée | Borne antérieure globale | Borne grille |
|---|---:|---:|
| F0 interne | 7564 | 7496 |
| F0 interne et contre `(3,0),(4,1),(5,2)` | 10380 | 10360 |
| F0 avec W sans triangle, interne | 192 | 168 |
| Même sous-famille et contre les anciennes familles | 642 | 642 |

LAB propose au message 271 de compter d'abord les classes de différences
de triangles. Pour déterminer la portée de cette piste, le programme sépare
les collisions internes suivant |Y∩Y′|. Sur les 63342 patrons, les seules
valeurs contribuant sont zéro et un ; elles sont respectivement présentes
dans 1668 et 450 patrons.

| Type interne de F0 | Paire de grilles | Paire hors grille |
|---|---:|---:|
| Triangles négatifs disjoints | 7304 | 7224 |
| Triangles négatifs partageant un apex de barreau | 216 | 528 |
| Intersection de taille deux ou trois | 0 | 0 |

Les deux premières lignes sont des **maxima séparés**. Leur somme n'est
pas la décomposition d'un maximum conjoint : dans la branche grille,
7304+216=7520, alors que le maximum conjoint certifié reste 7496.
Pour des comptes effectifs D et A des deux composantes, on sait A≤216 et
D+A≤7496. Si D+A atteignait 7496, alors D≥7280. Plus généralement,
D≥(D+A)−216.

Dans la première composante, il existe des triangles U,T,U′,T′ et un même
trois-ensemble positif W0 tels que

    ψ = 1_W0 + 1_U − 1_T,
    ψ′= 1_W0 + 1_U′− 1_T′,
    X=U∪T′,    X′=U′∪T.

Les deux derniers ensembles sont les prismes jumeaux. Si t_U désigne
l'image du triangle U, la collision vient donc de

    t_U−t_T = t_U′−t_T′.

Cela identifie précisément la composante que le quotient proposé par LAB
vise à traiter. Pour en tirer une nouvelle minoration, il reste à compter
les différences **distinctes** puis les W0 admissibles pour chacune. Les
7304 pertes ne peuvent pas être supprimées d'un budget sans recalculer le
nombre de représentants après quotient.

## 5. Correction de classement du coefficient 2794

Le terme 2794τ de la borne globale `(4,4)` de la note 185 contient :

- 2634τ issu du traitement de masse six, accompagné de 20C14 ;
- 160τ issu du contrôle de la composante **de masse huit** à supports C14.

À l'échelle d'une paire de prismes, l'ancienne borne pure de masse six
était 2634+4e(Θ), donc 2646 dans la branche grille. Elle est remplacée par
2166 dans cette branche et 2178 hors grille. Le terme 160τ ne disparaît
pas : il reste attaché à l'audit de masse huit. Les nouvelles bornes ne
doivent pas conduire à omettre ce terme lors d'une réutilisation de la
formule complète de la note 185.

## 6. Certification et reproduction

HiGHS sert à trouver des poids candidats. Comme dans les notes 188 et 193,
ils sont arrondis en rationnels non négatifs de dénominateur 10^9. Le calcul
exact utilise les plafonds finis des variables pour absorber tout résidu
négatif. Chaque plafond final est ensuite arrondi vers le bas à un entier
pair, car les deux signes sont inclus. Aucun optimum flottant n'est admis
comme prémisse et aucun optimum rationnel atteint n'est revendiqué ici.

Les patrons communs et la séparation de F0 sont archivés dans
`data/codex_mass6_family_patterns.json.gz` et
`data/codex_f0_internal_pattern_split.json.gz`. Les huit archives de
certificats commencent par `data/codex_grid_pair_collisions_`.

    python code/codex/mass6_family_patterns.py --verify-only
    python code/codex/f0_internal_pattern_split.py --verify-only
    python code/codex/grid_pair_collision_bounds.py --family 63 --kind grid --verify-only
    python code/codex/grid_pair_collision_bounds.py --family 63 --kind nongrid --verify-only
    python code/codex/grid_pair_collision_bounds.py --family all --kind grid --verify-only
    python code/codex/grid_pair_collision_bounds.py --family all --kind nongrid --verify-only
    python code/codex/grid_pair_collision_bounds.py --family f0 --kind grid --verify-only
    python code/codex/grid_pair_collision_bounds.py --family ftf --kind grid --verify-only
    python code/codex/grid_pair_collision_bounds.py --family f0split --kind grid --verify-only
    python code/codex/grid_pair_collision_bounds.py --family f0split --kind nongrid --verify-only

Tous ces contrôles passent. Les plafonds τ≤1534, b3≥45766 et les plafonds
thêta de la note 194 restent les références ; cette note améliore et complète
les coûts combinatoires avant leur future intégration globale.
