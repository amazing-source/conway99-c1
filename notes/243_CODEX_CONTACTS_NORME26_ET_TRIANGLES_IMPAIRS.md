# 243 — Norme 26 : peu de voisins proches dans une classe

9 octobre 2026. Codex, conséquence de la note 242 et du raffinement
quadratique par classes de LAP transmis au message 487.

**Résultat.** Au rang 43, sans racines et sans normes 16 à 24, chacun
des 329 vecteurs x d'une classe de norme 26 a au plus **48** autres
vecteurs y de cette classe tels que (x,y)=12. Si x n'est pas entier
dans les coordonnées des 99 sommets, la borne est **45**.

Ce sont exactement les voisins y pour lesquels (x-y)/sqrt(7) est un
vecteur de norme quatre de M. Ces restrictions ne prouvent pas encore
l'impossibilité des huit classes de taille 329.

## 1. Un lemme sur les triangles, indépendant du rang 43

Soit x dans L1 de norme 26. Pour chaque triangle T, écrire t_T=x(T).
Ce nombre est entier. Si f_T=7E1_T, alors ||f_T||²=28 et
(x,f_T)=7t_T. Le minimum 14 de L1 appliqué à x±f_T donne
|t_T|<=2. D'autre part,

    sum_T t_T² = x^t (7I+A)x = 3||x||² = 78.

Soient d_tri le nombre de triangles avec |t_T|=2 et e_tri le nombre
avec |t_T|=1. Alors

    4d_tri+e_tri=78.                                         (1)

**Si x est fractionnaire, e_tri>=22 et d_tri<=14.** Après changement
de signe, la note 178 donne x=phi-(1/3)1, phi=1_S-1_B, |S|=35,
|B|=2. Il y a 62 coordonnées nulles de phi. Modulo deux, si p est le
vecteur des triangles où t_T est impair,

    p=N^t phi-1,
    Np=(7I+A)phi-7*1=phi+1.

On a utilisé (A+4I)phi=6*1. Chacun des 62 sommets où phi=0 doit donc
appartenir à un nombre impair de triangles sélectionnés. Ainsi
3e_tri>=62. Comme e_tri=78 modulo quatre, il faut e_tri>=22.

**Si x est entier, e_tri>=6 et d_tri<=18.** On a cette fois
p=N^t x et Np=x modulo deux, puisque Ax=-4x. La congruence dans (1)
ne permet en dessous de six que e_tri=2. Supposons que les deux
triangles soient T et U. Alors x modulo deux est 1_T+1_U.
S'ils se coupent en un sommet, x a quatre coordonnées impaires,
contrairement à ||x||²=26 modulo quatre. Ils sont donc disjoints.

Comme A(1_T+1_U)=0 modulo deux, chaque sommet de T a un nombre pair
de voisins dans U ; il en a au plus un par lambda=1, donc aucun.
Les triangles sont anticomplets. Un sommet extérieur touche au plus
un sommet de chaque triangle et doit toucher les deux ou aucun.
Les 36 voisins extérieurs distincts de T sont donc aussi ceux de U.
Ils donnent 36 voisins communs comptés sur les neuf paires T cross U,
alors que mu=2 autorise exactement 18 incidences. Contradiction.

Ces deux bornes sur les triangles utilisent uniquement les propriétés
de L1 et du SRG, sans hypothèse sur le rang modulo sept.

## 2. Un budget de contacts dans la branche sans racines

Revenir au rang 43, avec a7=...=a12=0. Les résultats par classes de
LAP utilisés dans les notes 177 et 242 donnent : chaque classe de
norme 26 est centrée, de taille N=329 ; pour deux classes orthogonales
C,C',

    T(C)+T(C')=560I-(7/2)F_ex,                               (2)

où F_ex est le second moment des 538 vecteurs de M[4] non triangulaires.
On utilise ces résultats de pair sans refaire leurs programmes.

Fixer x dans C. Dans sa propre classe, les produits scalaires avec
y distinct de x sont -9,-2,5,12 : ils valent 26 modulo sept ; le
minimum de M, égal à quatre, exclut 19, et le minimum de L1 exclut
les valeurs inférieures à -13. Écrire a,b,c,d leurs multiplicités.
La taille 329 et la moyenne nulle donnent

    b=238-2a+d, c=90+a-2d,
    sum_(y in C) (x,y)² = 3878+98(a+d).                      (3)

Dans C', les produits sont -7,0,7. La moyenne nulle impose autant
de +7 que de -7 ; noter j ce nombre. Son second moment vaut 98j.
Ainsi le membre gauche de (2), évalué sur x, vaut

    3878+98s, avec s=a+d+j >= d.                             (4)

Poser u=x/sqrt(7) dans M*. Pour v dans M[4], le produit (u,v) est
entier et appartient à {-2,-1,0,1,2}, en appliquant le minimum de L1
à x±sqrt(7)v. Les vecteurs v de produit deux sont exactement
(x-y)/sqrt(7), avec y dans C et (x,y)=12. Ils sont donc d.
Si e désigne le nombre de v de produit un, les deux signes donnent

    sum_(v in M[4]) (u,v)² = 8d+2e.

Les triangles signés contribuent exactement 156 à cette somme,
et e>=e_tri. Par conséquent, (2), évaluée sur x, donne

    3878+98s = 560*26-(49/2)(8d+2e-156),
    2s+4d+e=296.                                           (5)

Puisque s>=d, il reste 6d+e<=296. Le §1 impose e>=6 si x est
entier, donc d<=48 ; s'il est fractionnaire, e>=22, donc d<=45.

La progression est une restriction locale supplémentaire sur les
ensembles de 329 vecteurs. Leur existence n'est pas décidée ici.
