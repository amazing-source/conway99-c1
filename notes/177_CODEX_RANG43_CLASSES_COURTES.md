# 177 — Rang 43 : une classe porte au moins dix-huit vecteurs de norme 16, 18 ou 26

**Complément du 9 octobre, message LAB 481 :** les séries par classes ont
été construites par LAP, sans exclusion du rang 43. Le §7 consigne leur
portée et une conséquence de parité : dans la branche où les normes
16,20,22,24 sont absentes, la norme 26 est obligatoire même avec des
racines. Le résultat de pair est exploité sans audit en double.

8 octobre 2026. Codex, audit et prolongement des messages 166, 169 et 171 de LAB.

**Résultat.** Si r=43, une classe non nulle de L1/(√7 M) contient au moins dix-huit vecteurs
distincts, tous de même norme, et cette norme peut être choisie dans **{16,18,26}**.
Si la norme 18 est absente, une classe de norme 16 ou 26 contient au moins cent dix vecteurs.
Si les normes 16 et 18 sont toutes deux absentes, une classe de norme 26 en contient au moins 329.

Ce résultat suit d'une identité modulaire exacte et du plan quadratique anisotrope à quarante-neuf
éléments. Il donne un problème concret sur des ensembles de vecteurs dans une même classe ;
il n'exclut pas encore le rang 43.

## 1. Quarante-huit classes non nulles, huit par valeur quadratique

Au rang 43, det L1=7^42 et M=√7 L1*. Le quotient

    C=L1/(√7 M)=L1/(7L1*)

a ordre 49. La forme q([x])=||x||²/2 modulo sept est bien définie, non dégénérée et anisotrope.
En effet il s'agit de la réduction de la composante unimodulaire de rang deux dans la décomposition
7-adique du réseau ; son type non hyperbolique est établi dans `papers/rank7/rank7.tex`.
L'extension d'indice trois de L à L1 ne change pas cette composante à la prime sept.

Un plan anisotrope sur F_7 est équivalent à un multiple non nul de x²+y². La valeur zéro est
représentée seulement par (0,0), et chacune des six valeurs non nulles a huit représentants.
Le programme vérifie directement cette distribution sur les quarante-neuf éléments du plan.

Ainsi les vecteurs de norme quatorze sont dans la classe nulle et correspondent exactement
aux racines de M : a_7=b_1. Les normes 16,18,20,22,24,26 ont des valeurs quadratiques respectives
1,2,3,4,5,6. Chaque couche se répartit donc dans **huit classes**, et une même classe non nulle
ne peut contenir deux normes différentes parmi ces six normes.

## 2. Une identité modulaire à trois termes positifs

Dans les coordonnées de la base indépendante de la note 167, l'égalité coefficient par coefficient est

    2a_8+16a_9+a_13
      =2632+7a_7+49b_1+7a_10+2a_11+a_12.                 (1)

Le vérificateur contrôle sa constante et ses sept coefficients libres par arithmétique rationnelle.
Comme a_7=b_1, on peut remplacer 7a_7+49b_1 par 56a_7. Tous les termes à droite après 2632
sont positifs ou nuls.

En posant S=a_8+…+a_13, on déduit immédiatement

    S≥2632/16=329/2,
    max(a_8,a_9,a_13)≥2632/19.

Les coefficients a_n comptent les deux signes et sont donc pairs. Il y a au moins 166 vecteurs
dans les quarante-huit classes non nulles, et au moins 140 vecteurs dans une des couches de
norme 16,18 ou 26. Répartis dans huit classes, ils en donnent au moins dix-huit dans une classe.
La classe opposée porte autant de vecteurs opposés et est différente, car sa caractéristique est sept.

Si a_9=0, (1) donne max(a_8,a_13)≥2632/3 : une des deux couches contient au moins 878 vecteurs,
donc une classe en contient au moins 110. Si a_8=a_9=0, on a a_13≥2632, puis 2632/8=329.

Les bornes 329/2 et 2632/19 sont aussi atteintes par des points rationnels de la relaxation
de la note 175. Les coordonnées et certificats du simplexe sont conservés, mais la preuve des
minorations ci-dessus ne requiert que (1) et la positivité, sans les grands comptages forcés du dual.

### Extension aux cinq rangs, proposée par LAB

Au message 178, LAB a donné la généralisation suivante, vérifiée ici dans notre propre base.
Avec m=(45−r)/2, on a exactement

    2a_8+16a_9+a_13
      =329(7^m+1)+7^(m+1)b_1+7a_7+7a_10+2a_11+a_12.

Les constantes pour r=35,37,39,41,43 sont respectivement
5529832,790258,113176,16450,2632. Avec a_8≤6930, cela impose notamment

    16a_9+a_13 ≥ 5515972, 776398, 99316, 2590

aux quatre premiers rangs. Ce sont des contraintes exactes entre les nombres de vecteurs de
normes 18 et 26. Elles ne donnent pas à elles seules de majorations de ces deux nombres.

## 3. La dépendance quantitative à la norme dix-huit

Une seconde combinaison exacte de coefficients, utilisant notamment a_15≥0, donne

    S + (1513/98)a_9 ≥ 15756/7.

En particulier, si a_9=0, il y a au moins 2252 vecteurs dans les autres couches de normes 16 à 26.
Le certificat rationnel est archivé et vérifié indépendamment dans nos coordonnées.

Cette implication **conditionnelle** ne signifie pas « au moins 166 vecteurs de norme 18 ou
au moins 2252 dans les autres couches ». Des mélanges sont permis. Par exemple, la relaxation
admet exactement

    a_7=0, a_8=20826/49, a_9=100,
    a_10=a_11=a_12=0, a_13=8916/49,

avec S=34642/49. C'est un point rationnel respectant toutes les contraintes scalaires utilisées,
pas une série thêta de réseau attestée. Il sert à éviter cette interprétation erronée des tests
où une couche est entièrement absente.

## 4. Produits scalaires dans une même classe

Soient x≠y deux vecteurs d'une même classe non nulle, de norme commune ℓ≤26.
Leur différence appartient à √7 M et a donc norme 14k, k entier positif. Ainsi

    (x,y)=ℓ−7k.

Ils ne sont pas opposés, car la classe n'est pas d'ordre deux. Le vecteur x+y est donc non nul
et de norme au moins quatorze. Cette dernière contrainte retire les distances trop grandes
que laisserait passer la seule inégalité de Cauchy. Avec l'exclusion des différences de Fano
aux normes 16 (note 173) et 18 (note 176), il reste :

| Norme commune | Produits scalaires possibles |
|---:|---|
| 16 | 2, −5 |
| 18 | 4, −3, −10 |
| 20 | 13, 6, −1, −8 |
| 22 | 15, 8, 1, −6, −13 |
| 24 | 17, 10, 3, −4, −11 |
| 26 | 19, 12, 5, −2, −9, −16 |

En particulier, même pour la norme 26, les différences redimensionnées dans M ont norme au plus
douze, et non quatorze. Les classes de norme 16 ou 18 se trouvent de plus dans l'orthogonal
de l'espace des racines de M (notes 173 et 176).

## 5. Les différences des vecteurs binaires sont des vecteurs supplémentaires du dual

Soient x,y binaires, chacun de norme au plus vingt, et supposons x−y=7P_4ψ pour un représentant
ψ de U de norme au plus cinq du tableau de la note 175. Alors x−y est entier. La formule

    7P_4ψ=(3I−A)ψ+(Σψ/9)1

impose 9|Σψ. Comme les sommes des petits représentants sont 0 ou ±3, on a Σψ=0.
Il reste seulement les différences de deux sommets et les signes deux-contre-deux sur quatre sommets.

Pour ψ=e_a−e_b, la coordonnée en a de 7P_4ψ vaut 3+A_ab≥3, alors que celle de x−y est au plus deux.
Dans le cas ψ=1_S−1_T, |S|=|T|=2, la coordonnée en s∈S vaut

    3−deg_S(s)+deg_T(s).

Pour qu'elle soit au plus deux, S doit être une arête et n'avoir aucune arête vers T.
Le raisonnement négatif impose que T soit également une arête. Les deux arêtes sont donc anticomplètes.
Alors ||7P_4ψ||²=56 et ses quatre coordonnées du support valent ±2. À l'extérieur, une coordonnée
de valeur absolue deux doit être le troisième point du triangle de l'une des deux arêtes ; il y en
a donc au plus deux autres. Toutes les coordonnées ont valeur absolue au plus deux, d'où
||7P_4ψ||_1≥56−2·6=44. Mais ||x−y||_1≤||x||_1+||y||_1≤40. Contradiction.

Ainsi aucune de ces différences ne vient des familles forcées U≤5. Pour les normes 16,18,20,
désormais toutes binaires, les regroupements dans une même classe exigent de petits vecteurs
**supplémentaires** de M. Les comptages forcés de la note 175 ne constituent pas une liste exhaustive
dans laquelle il suffirait de choisir leurs différences.

## 6. Audit et portée

`code/codex/rank43_coset_audit.py` reconstruit les contraintes dans notre base, obtient des
certificats rationnels et vérifie les identités, les signes des multiplicateurs et les points primaux.
Il vérifie aussi (1) directement, la distribution du plan anisotrope et le tableau du §4.
Les données sont dans `data/codex_rank43_coset_audit.json`.

Le seuil dix-huit a été découvert par le calcul de LAB (message 169), puis vérifié ici.
Le passage aux seules normes 16,18,26, les seuils conditionnels 110 et 329, et les restrictions
géométriques supplémentaires sont explicités dans cette note. Nous ne prétendons pas encore
classer tous les ensembles de dix-huit vecteurs répondant à ces contraintes.

## 7. Complément par classes reçu au message 481

Source : LAP, relayé par LAB sans contrôle supplémentaire, commit
`b47317977` de `conway99-c2-aws`, fichiers
`c1_mandat_c_transformations/w49.py` et `s0_rank43.py`, section 12 de sa
note. L'exactitude annoncée emploie python-flint. Nous ne reproduisons pas
ce programme.

LAP annonce un espace de dimension 44 pour les 49 séries de classes de
L1/(√7 M). Après les absences prouvées, il reste 19 paramètres : b1,
quatre classes pour chacune des normes 16,18,20,22, et deux classes de
norme 24. Six relations déterminent les deux autres classes de norme 24
et les quatre classes de norme 26, où les classes opposées ont été
identifiées dans les paramètres. Le message ne fournit pas les six
relations complètes ; elles ne sont donc pas reconstruites ici.

Le scénario sans racine et sans norme 16 à 24 reste compatible avec
l'intégralité des classes. Les tailles annoncées, pour chacune des huit
classes du cercle concerné, sont 329 à norme 26, 9338 à norme 30, 35287 à
norme 32. On retrouve b2=1000, b3=10648712, a13=2632. Ces résultats ne
constituent pas une réalisation de réseau ou de graphe.

### Une conséquence entière dans la branche 18/26

Supposer a8=a10=a11=a12=0 : seules les normes 18 et 26 peuvent donc être
présentes parmi les normes 16 à 26. Les racines, de norme 14 dans L1 et
de norme deux dans M, restent autorisées. Écrire b1=2k.

Dans cette branche, LAP donne les quatre tailles de classes à norme 18
sous la forme (x1,x2,x2,x1), classes opposées identifiées, et chaque classe
à norme 26 a exactement

    t = 329+7b1−8(x1+x2) = 329+14k−8(x1+x2).

**Ce nombre est impair.** Comme t est un cardinal non négatif, il est
strictement positif. La norme 26 est donc obligatoire **même en présence
de racines**, et ses huit classes sont toutes non vides.

Plus précisément :

| k modulo 4 | t modulo 8 | Minimum possible de t |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 7 | 7 |
| 2 | 5 | 5 |
| 3 | 3 | 3 |

Ainsi x1+x2≤41+floor(7k/4), et a13=8t est au moins respectivement
8,56,40,24 selon k modulo quatre. Ces minima ne sont pas annoncés atteints.
En particulier la branche « seule norme 18 parmi 16 à 26 » est impossible.

La non-disparition de la norme 26 se lit aussi directement dans (1) :
avec les quatre absences ci-dessus, a13=2632+56b1−16a9 est congru à huit
modulo seize puisque b1 est pair. La nouvelle information du résultat
par classes est que **chaque classe**, et pas seulement la couche totale,
doit être non vide. Aucune exclusion du rang 43 ne suit de cette seule
conséquence.

## 8. Sommes nulles par classe et cible quadratique (message 482)

LAP annonce ensuite, via LAB au message 482, le calcul de degré un
`w49odd.py`, commit `055a7e791`. L'espace a dimension 44 ; les 24 zéros
en dessous de la norme 14 laissent vingt paramètres, les sommes
vectorielles des classes de normes 16 à 24. Si ces cinq normes sont
absentes, **les vecteurs de chaque norme dans chaque classe non nulle
ont une somme vectorielle nulle**. Ce résultat de pair n'est pas réaudité.

Il est important de distinguer cette moyenne nulle d'un second moment
isotrope. En effet, dans cette branche sans norme 16 à 24, les identités
de la note 191 et les comptages de la note 192 donnent

    b2=1000−16k ≥ 462+170k+2k².

Le membre de droite dépasse celui de gauche dès k=3 et l'écart croît.
Ainsi k≤2. Les classes de norme 26 ont donc les tailles

    N=329+14k ∈ {329,343,357}.

**Obstruction de degré deux.** Un ensemble X de N vecteurs de norme 26
dans un réseau entier, contenu dans l'espace de dimension 44, ne peut
avoir un second moment isotrope que si 11 divise N. En effet, si

    Σ_(y∈X) y yᵀ = (26N/44) I,

alors, pour x∈X,

    Σ_(y∈X) (x,y)² = N·26²/44 = 169N/11.

La somme de gauche est entière. Comme 169 est premier à onze, 11|N.
Aucune des trois tailles précédentes n'est divisible par onze. Il en
va de même de la couche entière de norme 26, de taille 8N.

Donc les classes obtenues par le résultat de degré un sont centrées,
mais **ne peuvent pas être des 2-designs sphériques** dans V_-4. Leur
couche totale ne le peut pas non plus. Cela donne une cible précise à
un éventuel calcul de degré deux sur V_-4 : forcer l'isotropie de ce
second moment fermerait la branche, mais cette isotropie n'est pas
démontrée ici. Des harmoniques sur le seul facteur auxiliaire qui séparent
les classes n'imposent pas automatiquement ce second moment géométrique.
Ce lemme de divisibilité n'exclut donc pas encore la branche ni le rang.
