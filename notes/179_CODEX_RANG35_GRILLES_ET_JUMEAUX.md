# 179 — Le rang 35 impose des grilles et des prismes jumeaux

8 octobre 2026. Proposition de LAB au message 182, audit et correction par Codex.

**Résultat vérifié.** Dans un hypothétique srg(99,14,1,2) de rang modulo sept égal à 35,
il existe au moins **16 grilles induites 3×3**, **450 prismes triangulaires induits** et
**33 paires non ordonnées de prismes jumeaux**. Deux prismes sont dits jumeaux lorsque
leurs indicatrices ont la même projection sur l'espace propre −4.

Les cinq rangs 35,37,39,41,43 restent possibles. En revanche, la branche du rang 35 sans
grille est exclue. Les résultats ne supposent aucune transitivité ni aucun automorphisme.

**Correction importante.** Le message 182 et l'archive LAB `74068d6` annonçaient au moins
43 grilles, puis un terme supplémentaire donnait provisoirement 44. L'audit a découvert
des collisions entre représentants de signes opposés dans une nouvelle famille. Ces seuils
ne sont donc pas établis sans hypothèse supplémentaire. Les bornes ci-dessus incluent
explicitement ces collisions ; leur certificat exact est donné au §6.

## 1. Notations et noyau de la projection

On conserve les réseaux L1 et M=√7 L1* des notes 167 et 175, avec

    θ_L1 = Σ a_n q^n,       θ_M = Σ b_n q^n,
    Q(ψ) = 7||P_4 ψ||² = 3||ψ||² − ψᵀAψ + (Σψ/3)².

Pour deux représentants entiers ψ,ψ′ de sommes divisibles par trois, leurs images dans M
coïncident exactement lorsque φ=ψ−ψ′ vérifie

    (A−3I)φ = (Σφ/9)1.

En particulier 9 divise Σφ. À sommes égales, φ est un vecteur propre entier de valeur +3.
Le lemme de la note 168 dit que si sa masse positive est au plus six, alors, s'il est non nul,
il a exactement six +1 et six −1 : les deux supports sont des prismes disjoints, sans arête
entre eux. Ce lemme ne dit pas que de tels jumeaux sont impossibles.

Tous les représentants de la note 175 ont somme 0 ou ±3, y compris ±(2e_i+e_j).
Les nouvelles collisions de différence de somme neuf ne changent donc aucun résultat de cette note.

Notons P le nombre de prismes, ρ celui des grilles et τ celui des paires non ordonnées de jumeaux.

## 2. Tous les comptages à six sommets sont affines en P

La méthode indépendante de la note 175 est prolongée d'un sommet. En ajoutant un sommet
aux vingt-et-un types admissibles sur cinq sommets, puis en imposant les budgets intérieurs
de voisins communs λ≤1 et μ≤2, on obtient **62 types** sur six sommets.

Les identités d'extension avec zéro, un ou deux sommets marqués donnent **171 équations
de rang 61**. La variable libre est exactement le nombre P de prismes. Après fixation de
ce nombre, un mineur de rang plein est non nul. La matrice, le second membre, ce mineur
et les 62 solutions affines sont archivés dans `data/codex_six_vertex_grid_audit.json`.

Si N_e désigne le nombre de sous-ensembles de six sommets induisant e arêtes, on trouve :

| e | N_e |
|---:|---:|
| 0 | 101287494 − P |
| 1 | 275371866 + 9P |
| 2 | 333001746 − 36P |
| 3 | 243053811 + 84P |
| 4 | 118760796 − 126P |
| 5 | 39640293 + 126P |
| 6 | 8560860 − 84P |
| 7 | 831600 + 36P |
| 8 | 20790 − 9P |
| 9 | P |

Les trois dernières lignes ont respectivement dix, trois et un types, en accord avec LAB.
Un des trois types à huit arêtes a pour nombre 8316−6P, d'où **P≤1386**.
Le type formé d'un triangle et d'un chemin induit à trois sommets, sans arête entre eux,
donne **731808+12P représentants signés** de la forme ±(1_T−1_Y).

Ces comptages sont des conséquences d'identités exactes, pas une extrapolation à partir
de quelques graphes témoins. Le programme vérifie aussi que ΣN_e=C(99,6).

## 3. Indicatrices de six sommets et collisions à travers les grilles

Pour |W|=6, on a Q(1_W)=22−2e(W). Si e(W)≤8, deux ensembles distincts W,W′ ne peuvent
avoir la même image : leur différence aurait masse positive au plus six, donc les deux
ensembles seraient des prismes à neuf arêtes. Les signes opposés ont des sommes de différence
douze, non divisible par neuf. Ces nouveaux représentants sont donc tous distincts entre eux.

Ils ne rencontrent les anciens représentants de la note 175 qu'entre les classes de sommes
6 et −3, ou entre leurs opposées. Pour les normes considérées, les représentants de somme −3
sont −1_Y avec |Y|=3, ou e_z−1_S avec |S|=4 et z∉S. Les types −(2e_i+e_j) sont traités ci-dessous.

Une collision donne respectivement

    φ=1_W+1_Y,       ou       φ=1_W+1_S−e_z,
    (A−3I)φ=1,      Σφ=9.

Dans le second cas, z∉W laisserait une seule coordonnée négative, de valeur −1. La somme
de ses voisins serait non négative, alors que l'équation impose −2. Donc z∈W et φ≥0.

**Petit lemme.** Tout φ entier non négatif de somme neuf avec Aφ=3φ+1 est binaire.
À une coordonnée de hauteur h, on a 3h+1≤9−h, donc h≤2. Si φ_v=2, les sept unités
de masse restantes doivent toutes être voisines de v. Deux coordonnées de valeur deux
seraient donc adjacentes et partageraient au moins trois autres sommets positifs, ce qui
viole λ=1. S'il n'y en a qu'une, chaque coordonnée +1 doit recevoir la masse quatre de
ses voisins, dont deux en v ; il lui faut donc au moins deux autres voisins positifs,
tous voisins de v, ce qui viole encore λ=1. Ainsi φ est binaire.

Son support R a neuf sommets, degré intérieur quatre et chaque sommet extérieur a exactement
un voisin dedans. Tous les voisins communs des paires de R sont alors dans R, donc R est
un srg(9,4,1,2), c'est-à-dire la grille 3×3. On peut retrouver cette grille à partir d'un
sommet dont les quatre voisins forment deux arêtes ; les quatre autres points sont les
seconds voisins communs des quatre paires prises entre ces deux arêtes.
Le même lemme exclut une collision avec −(2e_i+e_j), puisque φ conserverait une coordonnée ≥2.

Réciproquement, toute grille induite dans le graphe à 99 sommets satisfait cette équation.
En effet un sommet extérieur ne peut toucher deux points de la grille, car leurs budgets
de voisins communs y sont déjà saturés. Les 9(14−4)=90 arêtes sortantes desservent les
90 sommets extérieurs, chacun une fois.

Ainsi les collisions décrites sont exactement celles obtenues en ajoutant une indicatrice
de grille. Pour e(W)=7, elles sont au nombre de 2286 par grille et par signe :

- 36 triples Y à une arête, avec W=R\Y ;
- 9 quadrangles et 36 triangles avec pendant S dans R, puis 50 choix de z extérieur
  dont l'unique voisin dans R appartient aux cinq points de R\S. Ici W=(R\S)∪{z}.

Pour e(W)=8, il y en a 36 par grille et par signe, provenant des 36 chemins Y dans R.
Les deux familles anciennes sont injectives, de même que la famille nouvelle : soustraire
ces nombres couvre donc toutes les collisions.

## 4. Triangle moins chemin : le cas oublié des signes opposés

Soient T un triangle et Y un chemin induit à trois sommets, disjoints et anticomplets.
Le vecteur 1_T−1_Y a somme zéro et Q=8.

La famille avec cette orientation est injective. Une collision non triviale entre deux
représentants orientés pareillement imposerait deux supports prismatiques de taille six.
L'un contiendrait un triangle et un chemin. Une extrémité du chemin a au plus un voisin
dans le triangle (λ=1) et un dans son chemin : elle ne peut avoir degré trois.

Cependant une collision entre orientations opposées a la forme

    P_4(1_T−1_Y) = P_4(1_Y′−1_T′),
    1_(T∪T′) − 1_(Y∪Y′) ∈ ker(A−3I).

Les deux unions sont alors des prismes jumeaux. Un prisme possède douze chemins induits
à trois sommets et six partitions non ordonnées en deux tels chemins. Pour une paire
non ordonnée de jumeaux S,R, les deux triangles de S et les douze chemins de R, puis
les choix symétriques, donnent 48 représentants orientés ; avec leurs opposés, il y en
a 96. Dans le quotient par la relation 1_S−1_R=0, ils donnent 48 images, chacune deux fois.
Le programme contrôle explicitement ces 96 vecteurs et les 48 collisions.

Toutes les collisions non triviales de cette famille sont de cette forme. La famille
apporte donc au moins

    731808 + 12P − 48τ

vecteurs distincts. Elle est disjointe des familles de somme zéro antérieures : avec une
différence de sommets ou d'arêtes la masse de collision est au plus cinq ; avec une différence
de triangles reliés par une arête, un support potentiel contiendrait encore triangle et chemin.
Les sommes séparent les autres familles.

La note 168 comptait exactement 33264+6P différences de triangles avec une arête croisée.
On conserve ici ce terme +6P, précédemment abandonné dans la minoration scalaire. Les deux
nouvelles bornes complètes sont donc

    b_3 ≥ 66528 − 18P − 72ρ,
    b_4 ≥ 3826746 + 90P − 4572ρ − 48τ.                 (B)

## 5. Deux contrôles géométriques du nombre de jumeaux

Tout sommet extérieur à un prisme a au plus deux voisins dedans. Deux voisins éventuels
forment une arête transversale du prisme : les arêtes des deux triangles ont déjà leur
voisin commun intérieur, et les non-arêtes ont déjà leurs deux voisins communs intérieurs.
Les trois arêtes transversales ont chacune un unique troisième point de triangle extérieur,
distinct des deux autres. Il y a donc trois sommets extérieurs de degré deux, soixante
de degré un, et trente sans voisin dans le prisme.

La relation « même projection » est une équivalence. Tous les autres prismes d'une même
classe sont disjoints et anticomplets au premier et entre eux. Les trente points lointains
ne peuvent en contenir que cinq. Chaque classe a donc taille au plus six, et

    τ ≤ 5P/2.                                                    (T1)

Une grille contient six prismes ; un prisme détermine au plus une grille, puisque les trois
points manquants sont les troisièmes points des triangles sur ses arêtes transversales. Donc

    6ρ ≤ P ≤ 1386.                                               (G)

Si g_T est le nombre de grilles contenant un triangle T, alors Σ_T g_T=6ρ. Deux grilles
distinctes sur T ont exactement T en commun : un quatrième point forcerait, avec T, un
quadrangle puis la grille entière par clôture sous les troisièmes points et les seconds
voisins communs. Leurs compléments de T sont des prismes jumeaux. Une paire de jumeaux
ainsi obtenue détermine T par les troisièmes points de ses arêtes transversales.
Ainsi Σ_T C(g_T,2)≤τ. Il y a 231 triangles, et C(g,2)≥g−1 pour tout g≥0, d'où

    τ ≥ 6ρ−231.                                                  (T2)

## 6. Certificat exact au rang 35

Posons B_3=b_3−66528+18P+72ρ et
B_4=b_4−3826746−90P+4572ρ+48τ. Ce sont des quantités non négatives par (B).
Dans la base êta indépendante des notes 167–168, au rang 35, l'identité exacte est

    9191 a_8 + 43 a_10 + 11 a_11 + 1555(b_2−462)
      + 1300(55440−7a_7−8a_8)
      + 651 B_3 + 34 B_4 + 135344(88−b_1)
      = 202320ρ + 8658P + 1632τ − 20783998.

Chaque terme de gauche est non négatif : positivité des coefficients, b_2≥462 (note 168),
budget commun de graines (note 173), et b_1≤88 (note 176). Donc

    101160ρ + 4329P + 816τ ≥ 10391999.                            (C)

Le programme reconstruit la base, vérifie les sept annulations des coordonnées libres,
ainsi que les coefficients de P,ρ,τ et la constante. Le contrôle de l'identité ne dépend
pas d'une approximation numérique du simplexe.

Par (T1), on obtient **101160ρ+6369P≥10391999**. Avec P≤1386,

    ρ ≥ 312913/20232 > 15, donc ρ≥16.

Avec ρ≤P/6, on obtient P≥10391999/23229, donc P≥448. Les valeurs 448 et 449 sont
encore impossibles, car ρ≤floor(P/6)=74 ne satisfait pas l'inégalité : **P≥450**.

Enfin, (T2) donne ρ≤(τ+231)/6. En l'insérant dans (C), avec P≤1386,
on trouve τ≥497345/17676>28, donc τ≥29. Pour τ entre 29 et 32, l'intégralité impose
ρ≤43 ; même avec P=1386 et τ=32, le membre de gauche de (C) est strictement trop petit.
Par conséquent **τ≥33**.

Sous l'hypothèse supplémentaire τ=0, (C) aurait donné les seuils provisoires 44 grilles
et 492 prismes. Cette hypothèse est désormais elle-même exclue au rang 35.

## 7. Autres couches et limites de la relaxation

Le même audit des six-ensembles s'étend aux autres e≤8. Dans une grille, les pertes signées
aux normes Q=6,8,10,12,14 sont respectivement 72,4572,7212,7380,3600 ; aucune aux normes
supérieures. Pour un S de quatre points de la grille, il y a cinquante choix de z extérieur
avec deg_S(z)=0 et quarante avec deg_S(z)=1. Cela permet de vérifier tous les nombres de
collisions sans énumérer un graphe à 99 sommets. Par exemple,

    b_5 ≥ 35123088 − 168P − 7212ρ.

Les nouvelles bornes jusqu'à b_11 sont aussi testées avec les contraintes de la note 175.
Elles ne changent pas les minima rationnels précédents. Des points rationnels explicites
sont archivés, notamment P=450,ρ=75 après élimination de τ par (T1), et
P=1386,ρ=44,τ=33 dans le système qui conserve τ. Ces points ne sont pas des réseaux ni des
graphes ; ils montrent seulement que cette relaxation ne prouve pas encore la contradiction.
Le rang 37 reste faisable dans la relaxation avec P=ρ=0.

Fichiers reproductibles :

    python code/codex/six_vertex_grid_audit.py
    python code/codex/rank35_grid_audit.py

Le premier reconstruit le recensement et contrôle les collisions de grilles et de jumeaux.
Le second utilise le simplexe rationnel de LAB pour découvrir les extrema, puis vérifie
les certificats et points dans nos coordonnées indépendantes ; il contrôle séparément
l'identité entière affichée ci-dessus. Les sorties sont dans les deux JSON de mêmes noms
préfixés par `codex_` sous `data/`.

Ces preuves et contrôles ont été relus par des sessions d'IA ; aucune formalisation dans
un assistant de preuve ni expertise humaine n'est revendiquée.
