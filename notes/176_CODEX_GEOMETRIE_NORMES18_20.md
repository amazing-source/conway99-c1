# 176 — Normes 18 et 20 : différences interdites et supports binaires

8 octobre 2026. Codex, échanges avec LAB aux messages 167, 170, 171 et 173 du pont.

**Résultats nouveaux.** Dans le réseau L1 associé à un hypothétique srg(99,14,1,2) :

- tout vecteur de norme 20 est dans L, a ses coordonnées dans {0,1,−1}, et ses deux supports
  de dix sommets contiennent chacun au plus une arête ;
- deux vecteurs de norme 18 ne peuvent avoir une différence de norme 14 ;
- tous les vecteurs de norme 18 sont orthogonaux aux racines de M, comme ceux de norme 16 ;
- les racines de M sont deux à deux orthogonales, à un signe près, donc b_1≤88 (lemme de LAB) ;
- pour un vecteur de norme 20, les sommets extérieurs ont au plus quatre voisins dans chaque
  support ; leurs histogrammes se réduisent à vingt-neuf possibilités arithmétiques.

Ces résultats sont valables pour tous les rangs encore possibles. La première preuve a été
redérivée et confirmée par LAB au message 171. La descente par triangles de LAB a motivé cette
recherche ; la preuve de binarité ci-dessous utilise seulement les équations propres et λ,μ.

## 1. Rappels et descente par les triangles

On note L=Z^99∩ker(A+4I), L1 son extension d'indice trois et M=√7 L1*.
Les notes 165–167 établissent min L1≥14 et min(L1\L)≥22. Les normes 14,16,18 sont déjà binaires.
Pour un vecteur entier de hauteur h, sa norme est au moins h²+7h (note 165).

Voici les deux descentes proposées par LAB au message 167, vérifiées directement.
Pour un triangle T, le vecteur f_T=7P_4 1_T appartient à L1\L, a norme 28, et

    f_T=3·1_T−A1_T+(1/3)1,       (x,f_T)=7Σ_(v∈T)x_v.

Si x∈L et ||x||²≤20, les deux vecteurs x±f_T sont dans les classes fractionnaires, donc

    22≤||x||²+28−14|x(T)|.

Comme x(T) est entier, **|x(T)|≤1**. La matrice d'incidence sommets-triangles satisfait
NNᵀ=7I+A. Ainsi Σ_T x(T)²=3||x||² et Σ_T x(T)=0. Pour ||x||²=2n≤20, exactement 3n triangles
ont somme +1 et 3n somme −1.

Si deux triangles disjoints T,T′ forment un prisme, leurs trois arêtes croisées donnent
||f_T+f_T′||²=28. Ce vecteur appartient encore à L1\L, d'où

    |x(T)+x(T′)|≤1       pour x∈L, ||x||²≤20.

Deux triangles de somme +1 ne peuvent donc former un prisme ; de même pour la somme −1.
La restriction aux classes fractionnaires est essentielle dans ces deux preuves.

## 2. La norme vingt est binaire

Soit ||x||²=20. Comme 20<22, x∈L. La borne h²+7h exclut h≥3.
Supposons h=2 et changeons le signe pour qu'une coordonnée v vaille 2.
Notons S la masse positive, égale à la masse négative, et t le nombre de coordonnées de valeur absolue deux.
Alors

    20=2S+2t,       S≥8,       1≤t≤2.

La seconde inégalité vient de la somme −8 des valeurs des voisins de v.

### Deux coordonnées de valeur absolue deux

Ici S=8. Le sommet v touche toute la masse négative et aucun sommet positif.

Si la seconde coordonnée vaut +2, les deux sommets positifs de valeur deux partagent les huit
sommets négatifs, tous de valeur −1. Ils sont non adjacents, ce qui contredit μ=2.

Si elle vaut −2, ce sommet u touche, symétriquement, tous les sommets positifs.
Prenons un sommet p de valeur +1. Il n'est pas adjacent à v ; tous ses voisins négatifs sont
dans N(v), donc au plus deux d'entre eux sont possibles. L'un est u, de valeur −2 ; l'autre
vaut au plus −1. Leur poids négatif total est au plus trois, alors que l'équation en p exige
un poids négatif au moins quatre. Contradiction.

### Une seule coordonnée de valeur absolue deux

Ici S=9 : il y a sept autres coordonnées +1 et neuf coordonnées −1.
Si v touchait un sommet positif p, sa somme de voisins −8 l'obligerait à toucher les neuf
sommets négatifs et exactement ce sommet positif. Mais p, adjacent à la valeur +2, aurait
au moins six voisins négatifs. Tous seraient aussi voisins de v, contredisant λ=1.

Donc v ne touche aucun sommet positif et touche exactement huit des neuf sommets négatifs.
Tout autre sommet p de valeur +1 est non adjacent à v : il peut toucher au plus deux de ces
huit sommets négatifs, et éventuellement le neuvième. Il ne peut atteindre le poids négatif
quatre imposé par l'équation propre. Contradiction.

Ainsi x est binaire, avec dix +1 et dix −1. Cette preuve n'utilise pas la descente du §1.

## 3. Au plus une arête dans chaque support de norme vingt

Écrivons x=1_P−1_Q avec |P|=|Q|=10. Pour p∈P, posons a_p=deg_P(p) ; définissons a_q de même sur Q.
L'équation propre donne deg_Q(p)=4+a_p et deg_P(q)=4+a_q. En sommant, on obtient
e(P)=e(Q)=e et e(P,Q)=40+2e.

Pour chacun des 79 sommets extérieurs z, les deux nombres de voisins dans P et Q sont égaux ;
notons-les t_z. En posant S_2=Σ_(p∈P)a_p²+Σ_(q∈Q)a_q², les doubles comptages donnent

    Σ t_z=100−4e,
    Σ t_z(t_z−1)=60−14e−S_2.

Pour la seconde identité, le nombre total de voisins communs des paires de P est 90−e.
Les contributions des centres dans P et Q sont respectivement Σ_P a_p²/2−e
et 60+7e+Σ_Q a_q²/2. On soustrait puis multiplie par deux.

Pour tout entier t≥0, t(t−1)≥2(t−1). Par conséquent

    60−14e−S_2 ≥ 2(100−4e−79)=42−8e,
    18≥6e+S_2≥10e.

Donc **e≤1**. Si e=1, le troisième point du triangle sur l'arête de P appartient à Q,
et réciproquement, par la borne |x(T)|≤1 du §1.

## 4. Degrés extérieurs et vingt-neuf histogrammes

On a t_z≤4. Pour le prouver, supposons t=t_z≥5 et posons T=N(z)∩P, U=N(z)∩Q.
Chaque q∈U a au plus un voisin dans T, puisque l'arête zq a un seul voisin commun.
Les t points de T ont au moins 4t voisins dans Q, comptés avec multiplicité. Les 10−t
points de Q\U reçoivent donc au moins 3t incidences.

Deux points de T ont déjà z comme voisin commun, donc au plus un voisin commun dans Q.
En notant d_q=deg_T(q), on a Σ_Q d_q(d_q−1)≤t(t−1). Pour t<10, Cauchy donne alors

    9t²/(10−t)−3t ≤ t(t−1),       soit t²+t≤20,

impossible pour t≥5. Le cas t=10 est immédiatement impossible, car Q\U serait vide.

Si t=4, toutes les inégalités sont des égalités : T et U évitent les extrémités des arêtes
intérieures éventuelles ; T−U est un couplage parfait, et chacun des six points de Q\U
touche une paire différente de T. L'énoncé symétrique vaut pour P\T et U.

Notons n_i le nombre de sommets extérieurs de degré t_z=i, h=n_3 et j=n_4. Comme e≤1,
S_2=4e et les deux identités du §3 donnent

    (n_0,n_1,n_2,n_3,n_4)
      =(9−5e−h−3j, 40+14e+3h+8j, 30−9e−3h−6j, h, j).

Il reste exactement vingt-deux histogrammes non négatifs pour e=0 et sept pour e=1.
Ce sont des possibilités arithmétiques, pas vingt-neuf configurations déjà réalisées.

## 5. Deux normes dix-huit ne peuvent différer d'un Fano

Supposons f,h de norme 18 et g=f−h de norme 14. Les trois vecteurs sont binaires.
Les supports de signe opposé de f et h ne se croisent donc pas, sinon g aurait une coordonnée ±2.
Écrivons, avec unions disjointes,

    f=1_(R∪A_1)−1_(U∪B_1),       h=1_(R∪A_2)−1_(U∪B_2).

Posons r=|R|, s=|U|. Le produit (f,h)=11 donne r+s=11 ; |A_i|=9−r et |B_i|=9−s.
Les supports de g sont A_1∪B_2 et A_2∪B_1 : ils sont indépendants et leur incidence est le
complément du plan de Fano (note 165). Tout sommet extérieur touche zéro ou un sommet de
chaque support de g. Les ensembles correspondants sont Z_g et X_g, et **Z_g est indépendant**.

Notons e_i≤1 le nombre d'arêtes dans chacun des deux supports du vecteur i=f,h (note 171),
x_R=|R∩X_g|, x_U=|U∩X_g|, e_R=e(R), e_U=e(U), et E=e(R,U).
Pour p∈R, en notant ε_p son indicatrice d'appartenance à X_g, les équations propres donnent

    deg_U(p)=4+deg_R(p)+deg_(A_1)(p)+deg_(A_2)(p)−ε_p.

L'identité symétrique vaut pour u∈U. Chaque degré croisé est donc au moins trois et, en sommant,

    E=4r+e_1+e_2−x_R=4s+e_1+e_2−x_U.

Puisque e_1+e_2≤2, les inégalités E≥3max(r,s) obligent {r,s}={5,6}.
Après changement des signes, prenons r=5, s=6. On obtient x_U=x_R+4 et x_R≤2.
Si U contenait un point de Z_g, alors x_R≤1. Ce point aurait au moins quatre voisins dans R,
tous dans R∩X_g puisque Z_g est indépendant : impossible. Donc x_R=2 et x_U=6.

Considérons maintenant le bloc B_2×B_1 de l'incidence Fano. Ses deux dimensions valent trois.
Les équations sur B_1 donnent

    e(B_2,B_1)=e(R,B_1)−e(U,B_1).

Or

    e(R,B_1)=x_R−e(R,A_2)=2−e_2+e_R,
    e(U,B_1)=e_1−e_U.

Ainsi e(B_2,B_1)=2−e_1−e_2+e_R+e_U≤2, car e_R,e_U≤min(e_1,e_2).
Mais tout bloc 3×3 du complément de Fano contient au moins trois arêtes : dans le plan de Fano,
un bloc 3×3 ne peut contenir sept incidences, car les degrés de colonnes totalisant au moins sept
donneraient au moins cinq intersections de paires de lignes, alors que trois lignes n'en ont que trois.
Contradiction. **La différence de norme quatorze est impossible.**

## 6. Orthogonalité des normes dix-huit aux racines

Pour une racine ρ∈M, g=√7ρ∈L1 a norme 14 et appartient à 7L1*.
Si h∈L1 a norme 18, le nombre (g,h) est divisible par sept. Le minimum quatorze donne
32−2|(g,h)|≥14, donc (g,h)∈{0,±7}. Une valeur ±7 produirait un second vecteur de norme 18,
h∓g, différent de h par un Fano. Le §5 l'exclut. Par conséquent (h,ρ)=0.

La même propriété pour la norme 16 figurait déjà dans la note 173. Elle couvre désormais
les deux couches de normes 16 et 18, sans hypothèse sur le rang modulo sept.

LAB a redérivé la preuve du §5 et ce corollaire au message 175, et les a confirmés.

### Lemme complémentaire de LAB : les racines forment A_1^k

Au même message, LAB applique la comparaison à deux vecteurs de Fano f,h dont la différence g
serait encore un Fano. Dans les notations du §5, r+s=7 ; les supports sont indépendants,
donc tous les degrés entre R et U valent trois ou quatre. Ainsi r,s≥3, puis {r,s}={3,4}.
Pour r=3,s=4, on a E≤rs=12 et E≥3s=12. Le biparti R−U est K_(3,4), ce qui donne quatre
voisins communs à deux sommets non adjacents de R, en contradiction avec μ=2.

Deux Fano distincts et non opposés ne peuvent donc avoir produit scalaire ±7.
Pour deux racines ρ,ρ′ de M, les Fano √7ρ et √7ρ′ ont produit scalaire 7(ρ,ρ′).
L'intégralité et les normes deux des racines laissent seulement 0,±1 comme produits scalaires
pour des racines non opposées ; ±1 sont désormais exclus. Le système de racines est donc
A_1^k avec k≤44, et **b_1=2k≤88**. Au rang 43, a_7=b_1, donc a_7≤88 également.
Cette preuve a été vérifiée par Codex ; aucune nouvelle classification externe de systèmes
de racines n'est nécessaire pour cette borne, qui suit simplement de l'orthogonalité.

## 7. Vérifications reproductibles

`code/codex/small_shell_geometry_audit.py` effectue trois contrôles complémentaires :

- pour les trois profils non binaires de norme vingt, un modèle CP-SAT sur le seul support,
  utilisant les équations propres et les budgets de voisins communs, est infaisable ; il
  n'utilise pas la descente par triangles ni les déductions particulières du §2 ;
- les 1225 blocs 3×3 du complément de Fano ont bien au moins trois arêtes, tandis que
  les paramètres d'intersection admis par le §5 en exigeraient au plus deux ;
- les vingt-neuf histogrammes du §4 satisfont exactement les trois identités de comptage.

Les sorties sont dans `data/codex_small_shell_geometry_audit.json`. Les preuves ci-dessus sont
autonomes ; les sorties du solveur sont des contrôles indépendants, pas des certificats formels
d'assistant de preuve. Aucun nouveau rang n'est déclaré exclu par cette note.

## 8. Deux premières bornes par graine de norme dix-huit, supports indépendants

Fixons une graine (p_0,U), avec p_0 positif, |U|=4, U son ensemble de voisins négatifs.
Supposons les deux supports P,Q indépendants, de taille neuf. Les six seconds voisins communs
des paires de U sont distincts ; notons leur ensemble V. Si n_i compte les points de P\{p_0}
ayant i voisins dans U, on a n_0+n_1+n_2=8 et n_1+2n_2=12. Il reste trois types :

    (n_0,n_1,n_2)=(2,0,6), (1,2,5), (0,4,4).

Dans le premier type, tous les six points de V appartiennent à P. Pour deux réalisations sur
la même graine, les signes ne se croisent pas : un point de Q\U a au moins deux voisins parmi
les six points communs de V, tandis qu'un des deux partenaires positifs n'a aucun voisin parmi
les sept positifs connus et ne pourrait atteindre quatre voisins dans l'autre support positif.
Les supports communs contiennent au moins sept positifs et quatre négatifs. La différence a donc
norme au plus quatorze ; si elle est non nulle, c'est un Fano, interdit par le §5.
**Il y a au plus une réalisation du type (2,0,6) par graine.**

Pour le type (1,2,5), fixons en plus le point manquant c∈V\P. Il y a six positifs connus et
trois partenaires, dont un unique p_* sans voisin dans U. L'argument de LAP et LAB transmis
au message 174 est correct : un point de Q\U a au moins un voisin parmi les cinq points communs
de V ; p_* ne touche aucun positif connu et ne peut avoir quatre voisins parmi les trois
partenaires de l'autre réalisation ; les deux autres partenaires touchent U et ne peuvent
appartenir à un support négatif indépendant contenant U. Il n'y a donc aucun croisement de signes.

Deux réalisations distinctes ont une différence de norme au plus seize. Le §5 élimine quatorze,
donc la différence a norme seize et les partenaires et les Q\U sont disjoints entre réalisations.
Pour une réalisation f fixée, sa différence g=f−h porte alors, au sommet p_*, la graine formée
des quatre voisins de p_* dans Q\U. Elle est déterminée par f. L'unicité des graines de norme
seize (note 173) détermine g, donc h : il y a au plus un autre h.

**Il y a au plus deux réalisations du type (1,2,5) par graine et point manquant fixé**, donc
au plus douze sur les six choix de point manquant. Cette borne est due à LAP et LAB et a été
vérifiée ici ; l'exclusion générale du §5 simplifie ses sous-cas.
Les deux types réunis donnent au plus treize réalisations par graine. Ce n'est pas encore
une borne sur toute la norme dix-huit : le type (0,4,4) et le cas d'une arête dans chaque
support restent à traiter.
