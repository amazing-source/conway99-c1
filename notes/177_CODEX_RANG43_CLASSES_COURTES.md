# 177 — Rang 43 : une classe porte au moins dix-huit vecteurs de norme 16, 18 ou 26

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
