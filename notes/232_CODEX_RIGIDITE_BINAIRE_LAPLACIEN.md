# 232 — Rigidité binaire : un carré nul modulo sept interdit toute seconde complétion

9 octobre 2026. Recherche reprise à la demande directe de l'utilisateur.
Point de départ : note 230 et résultat de LAP transmis par LAB 455.
LAP interdit les deux complétions de rangs (37,39) à boule générique
et ombres fixées. Le présent argument interdit **(37,r') pour tout r'**,
sans classifier les formes résiduelles de dimensions quatre ou six.

**Portée.** Si les données proches et les 60 ombres admettent une
complétion de rang 37 et si le bloc proche est inversible modulo sept,
cette complétion est l'unique SRG possible sur ces données, tous rangs
confondus. Aucun candidat de rang 37 n'est exclu : l'existence des
données binaires admissibles reste ouverte. Ce résultat ne suppose
ni absence de prismes ni automorphisme.

## 1. Lemme entier : une différence ne peut cacher un laplacien

Soient A et A' les matrices de deux graphes simples k-réguliers sur
le même ensemble. Supposons que deux sommets distincts aient au plus
c voisins communs dans chacun des deux graphes. Posons D=A'−A.

Soit S un ensemble de sommets dont les lignes sont identiques dans
A et A'. Posons U=V\S et B=A[S,U]=A'[S,U]. Supposons :

1. les colonnes de B sont deux à deux distinctes ;
2. BD_U=0 sur les entiers, où D_U=D[U,U] ;
3. D_U² est nul modulo un entier m>2c.

**Alors A'=A.**

Preuve. Les lignes et colonnes de D sur S sont nulles. Posons L=D_U².
Pour u≠v,

    L_uv = somme_w (A'_uw−A_uw)(A'_vw−A_vw)
          ≤ (A'²)_uv + (A²)_uv ≤ 2c < m.

Les termes croisés soustraits sont non négatifs ; aucun argument
modulaire ne remplace cette inégalité entière. Comme L_uv est un
multiple de m, on obtient L_uv≤0.

D_U1=0 par la régularité commune, donc L1=0. La matrice L est le
laplacien d'un graphe pondéré, de poids w_uv=−L_uv≥0. Par BD_U=0,
chaque ligne b de B vérifie D_U b^t=0 et donc

    0 = b L b^t = somme_(u<v) w_uv (b_u−b_v)².

Si w_uv>0, toutes les lignes b imposent b_u=b_v : les colonnes u et v
de B seraient égales. Elles sont distinctes, donc tous les poids sont
nuls. Alors L=0, puis D_U=0, car D_U est une matrice réelle symétrique
et (D_U²)_uu=somme_v (D_U)_uv². CQFD.

Si A et A' ont les mêmes paramètres SRG, l'hypothèse 2 est automatique :
le bloc S×U de A'²−A² est BD_U, et celui de A'−A est nul.

Le mécanisme utilise les entrées binaires dans la borne L_uv≤2c.
Les complétions pondérées à entrées négatives du fichier de recherche A
ne vérifient pas cette étape et ne constituent pas des contre-exemples.

## 2. Obtenir le carré nul depuis un bloc qui porte tout le rang

Revenons aux paramètres (99,14,1,2), et travaillons dans F7. Posons

    Q=A−3I+3J,    Q'=A'−3I+3J.

Les deux identités SRG donnent Q²=Q'²=0. Si
r=rang_7(A−3I), alors rang_7 Q=r−1 : Q annule 1 et coïncide avec
A−3I sur 1-perp, tandis que A−3I vaut 4 sur la droite des constantes.

Supposons Q[S,S]=M inversible et rang_7 Q=|S|. Les lignes de A et A'
sur S étant égales, écrire

         [ M   R ]           [ 0   0 ]
    Q =  [       ],    D =   [       ].
         [ R^t Z ]           [ 0  D_U]

Le complément de Schur donne Z=R^t M^(-1)R. Le bloc S×U de
Q'²−Q²=QD+DQ+D²=0 donne RD_U=0. Par suite ZD_U=0, donc QD=DQ=0.
L'identité complète impose alors

    D_U²=0 dans F7.

Le lemme du §1, avec c=2 et m=7, s'applique dès que les profils vers S
sont distincts. Aucun rang de Q' n'a été utilisé.

**Théorème général de reconstruction.** Si un SRG de Conway A possède
un bloc Q[S,S] inversible portant tout le rang de Q, et si ses profils
extérieurs vers S sont distincts, aucune autre complétion SRG des
mêmes lignes sur S n'existe, quel que soit son rang modulo sept.

## 3. Application à la boule générique d'une droite

Fixer un triangle T, les 36 sommets proches X, leur graphe G, et la
matrice N des 60 ombres. Deux complétions partagent tous les blocs
sauf le graphe F sur les 60 sommets lointains. Leurs différences sont
donc portées par F×F. Les équations SRG donnent ND_F=0 en entiers.

Les colonnes de N sont distinctes : chacune possède six uns, tandis
que deux sommets distincts ont au plus deux voisins communs.

Si rang_7(3I−G)=35, le bloc

    Q[X,X]=G−3I+3J

est inversible (note 230). Si une première complétion a rang_7(A−3I)=37,
Q est de rang 36, exactement la taille du bloc proche. L'argument du
§2 fonctionne avec ce bloc : il donne QD=0 puis D_F²=0 modulo sept.
Le lemme entier avec B=N force D_F=0.

**Corollaire.** Une complétion de rang 37 sur ces données interdit
toute seconde complétion distincte de rang 37, 39, 41, 43, ou autre.

La partie (37,37) était acquise dans la note 230, et (37,39) avait
été annoncée par LAP. Les deux cas (37,41) et (37,43) sont maintenant
fermés pour le problème précis de coexistence à données fixées.
Ce n'est pas l'exclusion de ces rangs comme candidats C1.

## 4. Une couverture par des supports séparateurs

Pour chaque graphe candidat et chaque racine v, les quatorze voisins
N(v) séparent tous les autres sommets : v a le profil tout-un, et les
84 autres ont les 84 profils distincts de poids deux non appariés.

Le bloc Q[N(v),N(v)] vaut M_pair−3I+3J. Modulo sept, il vaut 3 sur
l'espace antisymétrique des sept paires, et 5 sur l'espace symétrique
(constantes comprises). Il est donc inversible.

On peut compléter ces quatorze colonnes en une base de colonnes Q
indexée par S, de taille r−1. Pour une matrice symétrique, le bloc
principal sur une base de colonnes est inversible. Les profils vers S
restent distincts puisqu'ils le sont déjà vers N(v).

Chaque candidat possède donc un support séparateur de r−1 sommets
auquel le théorème du §2 s'applique. Dans la fenêtre connue, ces tailles
sont 36,38,40,42. Cette existence de bases relève de l'algèbre linéaire
déjà utilisée par la route Ω ; ne pas la présenter comme un petit
catalogue désormais classifié. Le gain nouveau est l'unicité parmi
toutes les complétions binaires, sans fixer le rang de la seconde.

## 5. Ce qui reste à résoudre

Le théorème supprime toute liberté de seconde complétion sur les
données d'un candidat de rang 37 générique. Il ne construit pas ces
données, ne prouve pas qu'elles sont impossibles, et ne borne pas le
nombre des couples (G,N). Il ne traite pas encore la coexistence
(39,39) ou les cas où le bloc choisi ne porte pas tout le rang.

La suite utile doit agir sur l'existence des profils binaires ou sur
les supports qui portent le rang ; recommencer une classification des
seuls résidus de dimensions quatre et six pour (37,r') est inutile.
