# 237 — Les réparations entre centres seuls imposent une longueur au plus huit

9 octobre 2026. Déduction théorique à partir de la piste des rubans de
transport du dossier Convergences et du message LAB 472. Aucun nouveau
balayage de graphes, aucun solveur. Cette note étend la restriction de LAB
sur les seules cordes `c_i ~ c_(i+4)` à **tout graphe d'arêtes entre centres**.

## Énoncé

Dans un SRG(99,14,1,2), considérer un ruban fermé à m centres avec **3m
sommets distincts** `c_i,a_i,b_i`. Ses triangles sont

    {c_i,a_i,a_(i+1)},  {c_i,b_i,b_(i+1)}.

La fermeture peut être circulaire ou tordue : dans le second cas,
`a_m=b_0` et `b_m=a_0`. Supposer que les seules autres arêtes entre ces
3m sommets relient deux centres. Alors

    m ≤ 8.

**Conséquence pour le transport :** tout cycle de longueur au moins neuf
doit présenter une identification de rôles, ou une arête supplémentaire
incidente à un sommet a ou b. Une quantité arbitraire de cordes entre
centres ne suffit pas à réaliser ce cycle.

Ce théorème exclut une famille entière de rubans réparés. Il ne borne pas
la longueur de tous les cycles de transport, ne force pas un cycle quatre,
et ne ferme aucun rang ni C1. Les rubans réparés de longueurs six à huit
ne sont pas exclus par cet argument.

## 1. Les moments des deux côtés donnent d'abord m ≤ 15

Soit R l'ensemble des 2m sommets a et b. Il induit un graphe 2-régulier :
deux cycles, ou un cycle de longueur 2m dans la fermeture tordue. Écrire
`t_x=|N(x)∩R|` pour x extérieur à R. Les équations SRG donnent

    Σ t_x = 24m,
    Σ t_x² = 4m(2m+3).

La première compte les douze voisins extérieurs de chaque sommet de R.
Pour la seconde, chaque paire de sommets de R a `2−A_R(u,v)` voisins
communs au total, et on retranche ceux qui sont dans R. Comme R est
2-régulier, cela donne `Σ binom(t_x,2)=2m(2m−3)`.

Chacun des m centres a exactement quatre voisins dans R. Les `99−3m`
autres sommets vérifient donc

    Σ t_x = 20m,
    Σ t_x² = 4m(2m−1).

Cauchy impose

    (20m)² ≤ (99−3m)·4m(2m−1),
    6m²−101m+99 ≤ 0.

Le dernier polynôme vaut 19 en m=16 et croît strictement pour les entiers
m≥16. Ainsi m≤15. Ce raisonnement n'impose aucune borne sur les degrés
du graphe des centres.

## 2. Les voisins d'un centre sont indépendants dans le cycle des indices

Noter C l'adjacence du graphe induit par les centres. Les centres `c_i`
et `c_(i+1)` ont déjà les deux voisins communs `a_(i+1),b_(i+1)`.
Ils ne peuvent être adjacents, car λ=1, ni avoir un troisième voisin
commun, car μ=2.

En particulier, pour chaque i, l'ensemble des indices des voisins de
`c_i` dans C ne contient pas deux indices consécutifs modulo m. C'est
une partie indépendante du cycle abstrait des m indices.

## 3. La positivité impose une corrélation négative précise

Supposer désormais `9≤m≤15`. Posons

    θ=2π/m,       c=cos θ.

Choisir f dans l'espace réel engendré par `cos(iθ)` et `sin(iθ)` sur
les centres. Sa somme est nulle et il est propre de valeur 2c pour le
cycle abstrait des indices. Sur chacun des deux côtés, poser

    r_(a_i)=r_(b_i)=f_(i−1)+f_i.

Ces valeurs égales sur les deux côtés rendent les calculs identiques
pour les deux fermetures. On a

    ||r||² = 4(1+c)||f||²,
    A_R r = 2c r,
    fᵀ A_(centres,R) r = 4(1+c)||f||².

Les vecteurs portés par les centres et par R ont chacun une somme nulle.
Le Gram `3I−A+J/9`, positif semi-défini dans tout C1, se comprime donc
sur leurs versions normalisées en

    [ 3−α                 −2√(1+c) ]
    [ −2√(1+c)             3−2c   ],

où `α=fᵀ C f / ||f||²`. Son déterminant doit être non négatif. Comme
`3−2c>0`, on obtient, pour tout f dans cet espace,

    α ≤ η_m := (5−10c)/(3−2c).                         (1)

Appliquer (1) aux sinus et cosinus, dont les normes au carré valent m/2,
puis prendre la moyenne. Il vient

    (1/m) Σ_i Σ_(j∈N_C(i)) cos((j−i)θ) ≤ η_m.         (2)

## 4. L'indépendance impose la borne contraire

Pour toute partie indépendante S du cycle des indices,

    Σ_(j∈S) cos(jθ) ≥ −1/sin θ.                       (3)

Preuve : les arcs de rayon θ centrés aux angles jθ, pour j dans S,
ont des intérieurs disjoints. Pour leur union U,

    −Σ_(j∈S) cos(jθ) = (1/(2 sin θ)) ∫_U −cos t dt
                    ≤ (1/(2 sin θ)) ∫_0^(2π) max(−cos t,0) dt
                    = 1/sin θ.

Le §2 permet d'appliquer (3) à chaque ligne de (2), après translation
des indices. Leur moyenne est donc au moins `−1/sin θ`. La positivité
demande nécessairement

    −1/sin θ ≤ η_m.                                  (4)

## 5. Contradiction exacte pour toutes les longueurs restantes

Pour `9≤m≤15`, on a `3/4<c<11/12`. Sur cet intervalle,

    (10c−5) sin θ > 3−2c,

donc `η_m < −1/sin θ`, en contradiction avec (4).

Voici un certificat rationnel de cette inégalité, sans approximation
trigonométrique ni liste de calculs numériques. Les deux côtés étant
positifs, il suffit de montrer

    P(c) := (10c−5)²(1−c²) − (3−2c)²
          = −100c⁴+100c³+71c²−88c+16 > 0.

Écrire `c=3/4+t/6`, avec `0≤t≤1`. Dans la base de Bernstein de degré
quatre, les cinq coefficients de P sont

    (2511, 6507, 9507, 10311, 7319) / 5184.

Autrement dit `P(3/4+t/6)` est la somme de ces coefficients multipliés
par `binom(4,j)t^j(1−t)^(4−j)`. Ils sont tous strictement positifs.

Pour justifier les bornes sur c : le minimum est `cos(2π/9)>3/4`, car
`4x³−3x` est croissant au-delà de 1/2, vaut −9/16 en 3/4 et vaut
−1/2 en `cos(2π/9)`. Le maximum est `cos(2π/15)<11/12` : le polynôme
`T5(x)=16x⁵−20x³+5x` est croissant sur `[cos(π/5),1]`, et

    T5(11/12) + 1/2 = 527/15552 > 0,
    T5(cos(2π/15)) = −1/2.

Cela exclut toutes les longueurs de neuf à quinze. Le §1 exclut toutes
les longueurs supérieures. Le théorème est démontré.

## Portée et provenance

Le message LAB 472 apportait les exclusions des rubans propres, certaines
réparations uniques, et la restriction calculée aux seules cordes de pas
quatre pour m=9..24. La présente preuve ne rejoue aucun de ces certificats
et n'en dépend pas : elle utilise les équations SRG, leur Gram positif,
et la forme du ruban du dossier de l'utilisateur.

Le petit script `code/codex/center_repaired_ribbons.py` enregistre seulement
les identités polynomiales exactes du §1 et du §5, sans classifier de
graphes. Le résultat est dans `data/codex_center_repaired_ribbons.json`.

La prochaine difficulté combinatoire se situe donc dans les identifications
de rôles et les arêtes supplémentaires touchant a ou b. Les réparations
restreintes aux centres ne constituent plus une piste pour les cycles longs.
