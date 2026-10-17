# 233 — Les ombres binaires interdisent une différence de rang au plus quatre

9 octobre 2026. Suite de la recherche demandée directement par l'utilisateur
sur le verrou binaire. Preuve assistée par un petit calcul exact sur F7
et des certificats rationnels ; aucun catalogue de graphes proches n'est
balayé. Les sorties d'infaisabilité flottantes ne servent pas de preuve.

**Théorème.** Deux SRG(99,14,1,2) ayant la même boule d'une droite et
les mêmes 60 ombres, mais des complétions lointaines différentes, ont
une différence de matrices de rang **au moins cinq sur F7**.

**Conséquence.** Si le bloc proche est inversible modulo sept, deux
complétions de rang 39 ne peuvent pas coexister sur les mêmes données.
La note 232 exclut déjà toute seconde complétion lorsqu'une première
est de rang 37. Restent notamment les couples (39,41), (39,43),
(41,41), etc. L'existence d'une première complétion n'est pas tranchée.

La note 230 connaissait l'unicité (37,37) ; LAP a annoncé (37,39)
dans le message LAB 455. Le cas (39,39) traité ici ne découle pas du
seul carré nul de la note 232 : c'est la faible dimension de la
différence combinée aux colonnes binaires qui le ferme.

## 1. Toute relation sur les ombres porte sur au moins six colonnes

Soit N une matrice binaire dont chaque colonne a poids six et dont
deux colonnes distinctes ont un produit scalaire au plus deux. Ces
propriétés sont obligatoires pour les ombres des 60 sommets lointains.

**Lemme.** Le code ker_F7(N) a distance minimale au moins six.

Preuve. Supposons une relation non nulle sur h≤5 colonnes, de
coefficients non nuls c_i. En sommant les lignes, 6·somme(c_i)=0,
donc somme(c_i)=0 dans F7. Chaque ligne non vide du sous-tableau est
un sous-ensemble de coefficients dont la somme est nulle.

Pour h≤3, chaque colonne possède un point absent des autres, puisque
6>2(h−1) ; la relation est impossible.

Pour h=4, les lignes non vides ont taille deux ou quatre. Les paires
autorisées relient des coefficients opposés. Aucun coefficient ne
possède trois opposés : leur somme totale serait −2c_i≠0. Si f lignes
contiennent les quatre colonnes, chaque colonne apparaît donc dans
au plus f+2(2−f)=4−f≤4 lignes, au lieu des six requises.

Pour h=5, les tailles possibles sont deux, trois et cinq. Une paire
est autorisée exactement lorsque ses coefficients sont opposés ;
un triple est autorisé exactement lorsque sa paire complémentaire
l'est. Le graphe E des paires opposées ne contient pas deux arêtes
disjointes, car le cinquième coefficient serait alors nul. Ce graphe
est biparti, donc ses arêtes forment une étoile K_(1,t). Si E est vide,
seules les lignes pleines sont possibles, contredisant les intersections
au plus deux. Par ailleurs t≤3, car t=4 donnerait une somme −3c≠0.

Notons f le nombre de lignes pleines. La colonne centrale apparaît
dans les lignes de paires et les lignes pleines, jamais dans les
triples. Les t intersections centre–feuille donnent

    6+(t−1)f ≤ 2t.

Il faut donc t=3, f=0 et deux lignes pour chaque paire de l'étoile.
La cinquième colonne appartient à tous les triples, donc leur total
est six. Chaque feuille appartient à quatre de ces triples, puisque
ses deux autres incidences sont dans sa paire. Son intersection avec
la cinquième colonne vaut alors quatre, contradiction. CQFD.

## 2. Réduction de la différence à un petit Gram

Écrire D=F'−F sur les 60 sommets lointains. Les équations exactes
donnent ND=0 et D1=0. Toute ligne non nulle de D possède r signes
plus et r signes moins, avec r≥3 : si r≤2, les ombres du côté opposé
ne couvriraient qu'au plus quatre des six points d'une ombre fixée.

Deux lignes non nulles de D ne sont jamais égales. Elles auraient
alors les mêmes r≥3 voisins supprimés dans F, ce qui donnerait trois
voisins communs dans le premier SRG. Sur F7, deux lignes projectivement
égales sont donc soit opposées, soit identiques ; le deuxième cas est
interdit. En effet un coefficient non nul ±1 impose que le facteur
de proportionnalité soit lui-même ±1. Une direction non signée a donc
au plus deux représentants, un de chaque signe.

La symétrie de D permet de choisir un bloc principal inversible H de
taille d=rang_F7(D). Sa diagonale est nulle et ses autres entrées sont
dans {0,1,−1}. Tout sommet actif a une colonne de produits

    w∈{0,1,−1}^d,   w≠0,   w^t H^(-1)w=0.

Deux telles colonnes satisfont w^t H^(-1)w'∈{0,1,−1}. Les directions
non signées choisies doivent contenir les d colonnes de H et former
une clique dans ce graphe de compatibilité.

La distance minimale du §1 s'applique à toute combinaison linéaire
des lignes de D. Si une forme linéaire est non nulle sur au plus deux
directions d'une clique maximale, elle donne un mot de poids au plus
quatre dans la réalisation, puisque chaque direction apparaît au plus
deux fois. Le mot ne peut être nul : les directions effectivement
utilisées engendrent l'espace de dimension d. Une telle clique est
donc interdite.

Les rangs d≤3 sont immédiatement exclus. Le rang un contredit la
diagonale nulle. En rang deux, les directions isotropes compatibles
avec la base sont les deux directions de base. En rang trois, après
changements de signes et signe global, H=J3−I3 ; son inverse est
−I3+J3/2. Parmi les vecteurs de {0,±1}^3, ses seuls vecteurs isotropes
non nuls, à signe près, sont les trois colonnes de H. Dans les deux
cas, une forme linéaire isole une direction et donne un poids ≤2.

## 3. Calcul exact en dimension quatre : une seule géométrie survivante

Le script `code/codex/rank4_binary_difference_probe.py` examine les
3^6=729 matrices H possibles, les quotientant par permutation de base,
changement des signes et signe global. Sept classes sont inversibles
sur F7. Pour chacune, il énumère les directions w et toutes les cliques
maximales contenant la base. Il examine les 400 formes linéaires à
scalaire près pour le critère du §2.

Après ce critère, sept cliques maximales subsistent dans cette
présentation enracinée. Elles ont toutes neuf directions. Le second
script fournit pour chacune un isomorphisme signé exact avec

    S9 = K ⊗ K,       K = [ 0  1 −1 ]
                         [−1  0  1 ]
                         [ 1 −1  0 ].

Ainsi tout D de rang quatre serait porté par au plus dix-huit sommets,
soit au plus un représentant de chacun des signes de ces neuf directions.
La congruence des produits modulo sept est ici une égalité entière,
puisque les deux valeurs à comparer appartiennent à {0,1,−1}.

Les lignes de S9 sont portées par les rectangles 2×2 d'une grille 3×3.
La distance six impose au moins six sommets, avec multiplicité, sur
chacun de ces neuf rectangles. De plus D1=0 exactement.

L'énumération des 4^9 choix (absent, plus, moins, les deux) laisse
40 configurations orientées. À équivalence signée près entre matrices
équilibrées, elles donnent quatre types :

| Sommets actifs | Multiplicités et signes | Nombre orienté |
|---|---|---:|
| 14 | quatre directions simples, cinq doubles | 18 |
| 15 | une ligne ou colonne simple, six directions doubles | 12 |
| 16 | une direction absente, huit doubles | 9 |
| 18 | neuf directions doubles | 1 |

Fichiers exacts : `data/codex_rank4_binary_difference_probe.json` et
`data/codex_rank4_grid_trade_probe.json`. La première version du pilote
oubliait la clique réduite à la base lorsque le graphe complémentaire
était vide ; ce cas a été ajouté avant la présente conclusion. Il est
exclu par un mot de poids un en directions non signées.

### Pourquoi le quotient signé est permis ici

On n'affirme pas que changer arbitrairement des signes conserve un SRG.
On utilise seulement les contraintes nécessaires ci-dessous. Si D et
RDR sont tous deux de sommes de lignes nulles, R étant diagonal ±1,
alors D1=D(R1)=0. Le changement de Seidel sur le support

    C -> RCR + (J−RJR)/2

préserve la binarité et la diagonale nulle. Il transporte les équations
du §4 pour la paire C,C+D. Sur im(D), le terme ajouté est nul après
identification par R ; le polynôme spectral y est donc également
préservé. Le signe global de D échange simplement les deux graphes.
Les bornes de degrés ou de voisins communs des pilotes ne sont pas
nécessaires aux certificats d'exclusion du §4.

## 4. Les quatre types ne se prolongent pas en deux SRG

Sur le support actif U, noter C=A[U,U]. Les positions D=−1 imposent
C=1 ; celles où D=1 imposent C=0. Les autres positions hors diagonale
sont les seules variables binaires communes aux deux graphes.
La différence des deux identités SRG impose exactement

    CD+DC+D²+D=0.                                      (1)

En outre im(D) est invariant par A : D² commute avec A, et les
blocs extérieurs à U annulent D. Cet espace est dans 1-perp. La
restriction h de C à im(D) doit donc satisfaire

    h²+h=12I4.                                        (2)

**Types 14,16,18.** La résolution rationnelle de (1) exprime les arêtes
communes en fonction d'arêtes libres tau_i. Elle impose respectivement,
dans les indexations du certificat, les expressions suivantes pour
une autre arête :

    14 : tau10 + tau9 − 1/2,
    16 : tau1 − tau16 + tau17 + tau18 − 1/2,
    18 : tau15 − tau16 + tau2 − tau22 + tau24 − tau26
         − tau27 + tau28 + tau29 + tau36 − 1/2.

Toutes les tau_i sont des coordonnées d'arêtes libres, donc entières.
Ces demi-entiers sont impossibles. La preuve n'utilise pas un statut
UNSAT flottant : elle utilise la solution affine rationnelle exacte.

**Type 15.** La même résolution donne, pour quatre coordonnées entières
a,b,c,t de la restriction,

    h = [ a   b    e     −3  ]
        [ c   z    3     e−3 ]
        [ t   4   1−z    b−4 ]
        [−4  t+4  c+4   −a−3 ],

    e=(3t−4b+4c−4a+22)/4,   z=2b+a−2c−6.

Les bornes 0≤tau_i≤1 donnent

    −5≤a≤2,  −2≤b≤6,  c∈{−4,−2,0},  −7≤t≤3.

Sur ces 2376 quadruplets, le contrôle entier de (2), après multiplication
par seize, n'en conserve que deux :

    (a,b,c,t)=(-4,2,-2,-2) ou (1,2,-2,-2).

Mais (1), les bornes des arêtes et b=2,c=t=−2 imposent

    −3≤a≤0.

Les deux bornes sont accompagnées de multiplicateurs rationnels
exacts. Pour vérifier un tel certificat, si Ex=b0, 0≤x≤1, objectif q,
prendre le multiplicateur y fourni et écrire

    q^t x = y^t b0 + (q−E^t y)^t x
           ≥ y^t b0 + somme_j min(0,(q−E^t y)_j).

Les deux substitutions rationnelles donnent les bornes annoncées et
excluent les deux quadruplets. Le solveur ne fait que proposer y ;
l'inégalité et sa valeur sont contrôlées exactement ensuite.

Script et certificat : `code/codex/rank4_trade_certificates.py`,
`data/codex_rank4_trade_certificates.json`. Le script vérifie aussi
la solution affine et l'expression symbolique de h. Les quatre
certificats sont terminés et passent leurs contrôles exacts.

## 5. Retour aux rangs et limite de la réduction

Si le bloc proche M de taille 36 est inversible, les compléments de
Schur Y,Y' de Q,Q' ont rangs r−37 et r'−37. Leur différence est D,
à un signe près. Ainsi

    rang_F7(D) ≤ r+r'−74.

Pour r=r'=39, le membre droit vaut quatre ; le théorème impose D=0.
Plus généralement, deux complétions distinctes nécessitent r+r'≥80.
La note 232 interdit séparément toute paire distincte contenant un
rang 37, même lorsque sa somme de rangs dépasse cette borne.

Autre conséquence : au rang 39 et avec un bloc proche inversible,
toute permutation préservant le triangle, sa boule et l'ensemble des
ombres (avec la bijection correspondante des 60 colonnes) préserve
le graphe complet. En transportant la complétion par cette permutation,
on obtiendrait sinon une seconde complétion de même rang 39. Cela étend
au rang 39 la propagation des symétries des données déjà connue au
rang 37 ; cela ne démontre pas l'existence d'une telle symétrie.

Ce sont des théorèmes de contrôle des réalisations à données fixées.
Ils suppriment des choix possibles de complétion, mais ne donnent pas
encore un petit catalogue des données (G,N), et n'excluent aucun des
174 noyaux ni un rang global entier. Le prochain verrou de cette
approche concerne les différences de rang cinq ou six et, surtout,
l'existence des systèmes binaires de profils eux-mêmes.
