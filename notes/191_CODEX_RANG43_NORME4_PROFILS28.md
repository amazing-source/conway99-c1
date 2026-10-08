# 191 — Rang 43 : au moins 922 vecteurs de norme quatre et trois profils fractionnaires

Suite : la note 192 renforce b1≤78 en b1≤44 à tous les rangs, et b2≥922
en b2≥968 au rang 43, grâce aux cocliques de taille 22 du profil C.

8 octobre 2026. Point de départ : résultats de LAP transmis par LAB au
message 244. Redérivation des identités et de la borne sur les racines,
ajout du comptage des sommes de racines, classification des profils et
structure du cas à coordonnée −2 : Codex.

**Résultats.** Pour tout rang encore possible, les racines de M vérifient

\[
 b_1\le78,\qquad b_2\ge462+41b_1+\tfrac12 b_1^2.
\]

Au rang 43, on en déduit **b2≥922**, donc au moins **460 vecteurs de norme
quatre non triangulaires**. La borne 914 annoncée par LAP utilisait les
réflexions des vecteurs triangulaires ; le gain à 922 compte également
les sommes de deux racines orthogonales.

À un signe près, les vecteurs fractionnaires de norme 28 ont exactement
trois profils possibles, décrits au §4. Ce sont des conditions nécessaires,
sans affirmation d'existence. Le profil à une coordonnée −2 entraîne une
partition équitable 1+14+21+63 et un graphe cubique sur quatorze sommets.
Les vecteurs entiers de norme 28 ne sont pas classifiés ici. Le rang 43
reste ouvert.

## 1. Bessel sur les arêtes donne b1≤78

La note 176 prouve que les racines de M sont ±r1,…,±rk, deux à deux
orthogonales, et que gi=√7 ri est un vecteur entier de Fano de norme 14.
Ainsi b1=2k. Les vecteurs gi/√14 sont orthonormés dans l'espace propre E−4.

Le projecteur est P4=(3I−A)/7+J/63. Ses entrées diagonales valent 4/9 et
celles d'une arête valent −8/63. Pour une arête uv, Bessel donne

\[
 \sum_i(g_i(u)+g_i(v))^2
 \le14\,\|P_4(e_u+e_v)\|^2=\frac{80}{9}.
\]

La somme de gauche est entière : elle est donc au plus huit. D'autre part,
pour chaque gi,

\[
 \sum_{uv\in E}(g_i(u)+g_i(v))^2
 =g_i^t(14I+A)g_i=10\cdot14=140.
\]

Le graphe a 693 arêtes, d'où 140k≤8·693=5544, donc k≤39 et b1≤78.
Cette preuve utilise l'orthogonalité déjà démontrée ; aucun calcul CP-SAT
ni nouvelle classification de systèmes de racines n'est nécessaire.

## 2. Réflexions triangulaires et sommes de racines : aucun doublon

Pour chacun des 231 triangles T, posons tT=√7 P4 1T. Il a norme quatre,
et fT=√7 tT=7P4 1T appartient à la classe +1/3 modulo le réseau entier L.
Les 462 vecteurs ±tT sont distincts.

Pour une ligne de racines ri, on a (tT,ri)=gi(T). Les supports positif et
négatif de gi sont indépendants, donc gi(T)∈{−1,0,1}. L'identité d'incidence
triangulaire NNᵗ=7I+A donne

\[
 \sum_T g_i(T)^2=3\|g_i\|^2=42.
\]

Il y a donc 42 triangles non orthogonaux à ri. Leurs reflets

\[
 s_i(t_T)=t_T-(t_T,r_i)r_i
\]

et leurs opposés donnent 84 vecteurs de norme quatre par ligne de racines.

Voici la séparation de tous les comptages :

- Deux triangles positifs distincts ont produit scalaire au plus un.
  S'ils partagent un sommet, ce produit vaut zéro ; s'ils sont disjoints,
  il vaut 1−e(T,U)≤1. Ils ne partagent pas une arête, car λ=1.
- Un reflet non trivial ne peut être un vecteur triangulaire positif :
  leur différence serait une racine, ce qui imposerait le produit trois.
- Deux reflets issus d'une même ligne ne coïncident pas, puisque la
  réflexion est une isométrie bijective.
- Deux reflets issus de lignes distinctes et de triangles distincts ne
  coïncident pas : leur égalité donnerait tT−tU=±ri±rj de norme quatre,
  donc (tT,tU)=2. Si le triangle est le même, l'orthogonalité des deux
  racines interdit immédiatement l'égalité.
- Les reflets positifs ont tous, après multiplication par √7, la classe
  +1/3 modulo L ; leurs opposés ont la classe −1/3. Ces deux classes sont
  distinctes, ce qui sépare les signes.

Il reste à ajouter les quatre sommes ±ri±rj pour chaque paire i<j. Elles
ont norme quatre et sont toutes distinctes, puisque les racines choisies
sont linéairement indépendantes. Après multiplication par √7, elles sont
entières, donc distinctes des triangles et de leurs reflets fractionnaires.
Par conséquent

\[
 b_2\ge462+84k+4\binom{k}{2}
     =462+82k+2k^2=462+41b_1+\tfrac12b_1^2.
\]

Il s'agit d'une borne pour tous les rangs, et pas seulement pour le rang 43.

## 3. Identités au rang 43 et conséquence b2≥922

Au rang 43, le quotient discriminant anisotrope donne a7k=bk pour tout k,
en particulier a7=b1 (notes 176–177). La redérivation dans notre base êta
donne les cinq identités annoncées par LAP :

```text
a13 = 2632 + 56a7 − 2a8 − 16a9 + 7a10 + 2a11 + a12
b2  = 1000 − 8a7 + 25a8 + 11a9 + 8a10 + 3a11 + a12 = a14
a15 = 74704 + 1064a7 − 196a8 + 86a9 + 22a10 + 13a11 − 6a12
b3  = 10648712 + 19388a7 + 5150a8 + 1237a9 + 31a10 − 68a11 − 39a12
b4  = 4464109880 + 275744a7 − 14374a8 − 24188a9 − 3996a10 + 388a11 + 701a12.
```

La deuxième et la positivité donnent b2≥1000−8a7=1000−16k.
Si k≤4, alors b2≥936. Si k≥5, le comptage du §2 donne
b2≥462+82·5+2·5²=922, puisque ce polynôme croît pour k≥0.
Donc **b2≥922** dans tous les cas. En retirant les 462 vecteurs
triangulaires, il reste au moins **460** vecteurs non triangulaires.

Ce raisonnement n'a pas besoin de la borne k≤39, ni d'un programme
linéaire. Il emploie seulement l'intégralité de k, une identité thêta et
les comptages géométriques précédents.

Le scénario a7=…=a12=0 donne a13=2632, a14=b2=1000, a15=74704,
b3=10648712 et b4=4464109880. Les deux séries ont des coefficients
non négatifs et pairs hors terme constant jusqu'à q^84. Ce contrôle fini
ne prouve ni l'existence d'un réseau avec ce scénario, ni la positivité
à tous les ordres. Dans ce scénario, il faut expliquer 538 vecteurs de
norme quatre en plus des triangles.

## 4. Classification complète des profils fractionnaires de norme 28

D'après la note 167, après changement de signe si nécessaire,

\[
 x=\varphi-\tfrac13\mathbf1,\quad
 (A+4I)\varphi=6\mathbf1,\quad
 \sum\varphi=33,\quad \sum\varphi^2=39.
\]

Ainsi Σφ(φ−1)=6. Les termes sont des entiers pairs non négatifs.
Les seules possibilités pour les exceptions à {0,1} sont trois valeurs
dans {−1,2}, ou une seule valeur −2 ou 3. Cela donne six profils arithmétiques.

Une coordonnée 3 exigerait une somme des voisins égale à −6 alors que
toutes les autres coordonnées sont non négatives. Au moins deux
coordonnées +2 laisseraient au plus une coordonnée −1, alors que chaque
sommet de valeur 2 exige une somme des voisins égale à −2. Ces trois
profils sont impossibles. Il en reste exactement trois :

| Type | φ | Contraintes initiales |
|---|---|---|
| A | 1S−1Z, avec |S|=36, |Z|=3 | S et Z disjoints |
| B | 1S+2ev−ea−eb, avec |S|=33 | v,a,b distincts hors S ; v touche a,b et aucun point de S |
| C | 1S−2ev, avec |S|=35 | v∉S ; N(v)⊂S |

Les dernières contraintes résultent directement de la somme des voisins
en v : −2 au type B, 14 au type C.

### Type A : les trois sommets négatifs

Les équations exactes sont celles de la note 178 : dS−dZ vaut 2 sur S,
10 sur Z, 6 ailleurs. Si e=e(Z) et O est l'ensemble des 60 autres sommets,

```text
e(S,Z)=30+2e ; e(S)=51+e ; e(Z,O)=12−4e ;
e(S,O)=372−4e ; e(O)=228+4e.
```

Si Z est un triangle, chacun de ses sommets touche ses douze voisins
extérieurs dans S. Aucun sommet extérieur ne touche deux sommets de Z,
par λ=1. Ces 36 voisins distincts épuisent S. On retrouve exactement
x=−fZ. Un vecteur non triangulaire de type A a donc e(Z)≤2.

### Type B : une exception +2

Posons Z={a,b}, ε=e(Z)∈{0,1}, et O les 63 sommets restants. Le sommet v
touche les deux points de Z, aucun de S et douze de O. On obtient

```text
e(S,Z)=16+2ε ; e(S)=41+ε ; e(Z,O)=10−4ε ;
e(S,O)=364−4ε ; e(O)=248+4ε.
```

Ces formules sont nécessaires ; elles ne suffisent pas à construire le
graphe, et aucun de ces deux cas n'est déclaré exclu.

## 5. Type C : un graphe cubique sur quatorze sommets

Notons U=N(v), de taille 14, et B=S\U, de taille 21. Le voisinage U
induit un couplage parfait, comme tout voisinage dans ce graphe.

Un sommet de U a quatre voisins dans S, dont son partenaire dans U :
il a donc trois voisins dans B. Un sommet de B a deux voisins dans S
par l'équation propre ; comme il est non adjacent à v, il a exactement
deux voisins dans U par μ=2. Il n'a donc aucun voisin dans B. Les deux
voisins dans U ne sont pas appariés, sinon leur arête aurait à la fois
v et ce sommet de B comme voisins communs.

Deux sommets de B ne codent pas la même paire de U : une telle paire
aurait au moins trois voisins communs, avec v. Les 21 sommets de B
codent donc les 21 arêtes d'un graphe simple **cubique H sur U**, disjoint
du couplage parfait induit sur U.

Tous les 84 sommets non adjacents à v sont en bijection avec les paires
non appariées de U : chaque paire a exactement un second voisin commun,
et chaque sommet à distance deux de v touche exactement deux points de U.
Les 63 sommets O de valeur zéro correspondent donc aux 63 autres paires,
celles de K14 privées des sept arêtes du couplage et des 21 arêtes de H.

Chaque sommet de O a six voisins dans S, dont deux dans U ; il en a
donc quatre dans B et huit dans O. La partition (v,U,B,O), de tailles
(1,14,21,63), est équitable avec quotient

\[
 Q=\begin{pmatrix}
 0&14&0&0\\
 1&1&3&9\\
 0&2&0&12\\
 0&2&4&8
 \end{pmatrix}.
\]

Les bilans d'arêtes et l'identité Q²=12I−Q+2·1(1,14,21,63) sont exacts.
En particulier B est une coclique de taille 21. Ce profil ne se réduit
donc pas à un choix arbitraire de 35 sommets : il impose la structure
décrite ci-dessus sur la totalité des 99 sommets. La compatibilité de
ce quotient ne démontre pas l'existence du graphe ni celle de ce vecteur.

## 6. Vérification reproductible et limites

```text
python code/codex/rank43_norm4_audit.py
```

Le script reconstruit exactement les cinq identités dans la base de Codex,
contrôle les égalités a7k=bk jusqu'à k=12, la positivité et la parité
jusqu'à q^84 au scénario origine, l'arithmétique des bornes sur les
racines, les six profils et leurs trois éliminations, les bilans d'arêtes
et l'identité du quotient équitable. Il n'importe ni programme de LAB
ni solveur d'optimisation.

Les arguments géométriques d'absence de doublons et de reconstruction
du graphe cubique sont donnés dans cette note ; les contrôles arithmétiques
du script ne les remplacent pas. Données :
`data/codex_rank43_norm4_audit.json`.
