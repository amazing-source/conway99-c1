# 246 — Une preuve directe de 3<=delta<=9, et des contraintes par sommet

9 octobre 2026. Suite de la note 245 ; exploitation du message LAP
relayé par LAB au numéro 504. Aucun calcul de séries modulaires repris.

**Nouveau théorème.** Dans toute configuration P3/N25 de la note 245,
chacun des trois sommets positifs p porte entre **un et trois triangles
entièrement contenus dans P union N**. Une inégalité locale explicite
renforce encore cette borne. Elle donne directement **3<=delta<=9**,
où delta compte les arêtes de N dont le triangle sort du support.

La borne delta>=3 n'a donc plus besoin de l'énumération et des
certificats de la note 245. La preuve ci-dessous est indépendante
du rang, pourvu que P soit indépendant et que le profil satisfasse
l'équation (A+4I)(1_P-1_N)=-4*1.

Appliquée aux 5 345 supports encore non exclus du registre précédent,
cette borne locale en élimine **764**. Il reste 4 581 supports, dont
209 avec delta=3. **S0 reste ouvert.**

## 1. Donnée nouvelle de LAP, conservée comme telle

Le message 504 cite le commit `effd38579`, dossier
`conway99-c2-aws/c1_mandat_c_transformations/`, section 14, fichiers
`s0_cert.py`, `s0_cert_N32_b9.json`, `z9_validate.py`. LAP donne
l'identité exacte suivante dans S0 :

    n = 10 + u_LAP + s44 + 2w + 4c1 + g_l + 7g_v.           (1)

Ici n est le nombre de vecteurs y=(2/9)1+1_P-1_N, norme 208/9 de
L9, classe deux. Les six termes sont des nombres d'objets, donc positifs
ou nuls :

- u_LAP : vecteurs de classe quatre de O, norme 34/9 ;
- s44 : ensembles réguliers de taille 44, classe quatre de L9,
  norme 220/9 ;
- w : vecteurs de classe deux de L9, norme 190/9 ;
- c1 : vecteurs de classe un de L9, norme 178/9 ;
- g_l : lignes fantômes, au-delà des 231 lignes, dans un signe de la
  couche fractionnaire de norme quatre de M ;
- g_v : sommets fantômes, au-delà des 99 sommets, classe un de O,
  norme 28/9.

Ainsi n=10 exactement lorsque les six nombres s'annulent. L'identité
est un résultat de LAP, exploité ici sans refaire son simplex. Sa
remarque sur les quatre sommes triangulaires donne aussi delta<=9.

LAP précise que le profil (1^3;(-1)^25) vaut à tout rang ; seule
l'indépendance de P utilise S0 dans cette application. La preuve
combinatoire qui suit est conditionnelle à cette indépendance.

## 2. Le comptage séparé pour un sommet positif

Fixer p dans P={p,a,b}. Poser Q=N(p) inter N, avec |Q|=8, et Z=V sans
(P union N), avec |Z|=71. Le graphe Q est un appariement, car deux
voisins de p ne peuvent avoir plus d'un voisin dans N(p). Noter :

    t_p = e(Q),
    c_pa = |N(p) inter N(a) inter N|,
    c_pb = |N(p) inter N(b) inter N|,
    X_p = binom(c_pa,2)+binom(c_pb,2),
    W_p = sum_{v dans N} binom(|N(v) inter Q|,2).

On a 0<=c_pa,c_pb<=2 et W_p>=0. Le résultat local est

    1 <= t_p,
    3t_p <= 5+2(c_pa+c_pb)-X_p-W_p.                         (2)

Pour la première borne, p a six voisins dans Z. Les 8-2t_p sommets
non appariés de Q ont chacun leur partenaire de triangle dans Z.
Ces partenaires sont distincts, car N(p) est un appariement parfait
sur quatorze sommets. Ainsi 8-2t_p<=6, donc t_p>=1.

Pour la seconde borne, écrire d_p(z)=|N(z) inter Q|, z dans Z.
Si p~z alors d_p(z)<=1 ; sinon d_p(z)<=2. Le nombre

    H_p = sum_{z dans Z}(d_p(z)-binom(d_p(z),2))

compte donc les z ayant au moins un voisin dans Q.

Chaque q de Q a d(q)=|N(q) inter P| voisins dans N et d(q) dans P,
donc 14-2d(q) voisins dans Z. Comme

    sum_{q dans Q} d(q)=8+c_pa+c_pb,

on obtient

    sum_z d_p(z)=96-2(c_pa+c_pb).                            (3)

Les binom(8,2)-t_p paires non adjacentes de Q ont déjà p comme voisin
commun. Leur unique autre voisin commun est dans P sans {p}, dans N,
ou dans Z. Le premier cas est compté X_p fois, le deuxième W_p fois.
Les paires adjacentes de Q ont déjà leur triangle complet avec p.
Par conséquent,

    sum_z binom(d_p(z),2)=28-t_p-X_p-W_p.                    (4)

Il suit de (3)-(4) que

    H_p=68-2(c_pa+c_pb)+t_p+X_p+W_p.

Parmi les 71 sommets de Z, 65 ne sont pas adjacents à p. Parmi les
six autres, exactement 8-2t_p ont un voisin dans Q. Donc

    H_p<=65+(8-2t_p)=73-2t_p,

ce qui donne (2).

## 3. Conséquences uniformes et description du premier cas restant

Pour c dans {0,1,2}, le nombre 2c-binom(c,2) vaut 0,2,3.
Le membre droit de (2) est donc au plus 5+3+3=11. Comme t_p est
entier, **t_p<=3**. En sommant les trois appariements internes,

    delta=12-t_p-t_a-t_b,       1<=t_p,t_a,t_b<=3,

d'où **3<=delta<=9**, par une preuve de quelques comptages seulement.

On obtient même une interprétation exacte du défaut local

    ell_p=5+2(c_pa+c_pb)-X_p-W_p-3t_p >=0.                   (5)

C'est le nombre de sommets z de Z non adjacents à p et sans aucun
voisin commun avec p dans N. Leurs deux voisins communs avec p sont
donc tous deux dans Z. Cela permet de faire porter les prochains
arguments sur un ensemble de sommets identifié, et pas seulement
sur une inégalité numérique.

Si delta=3, les trois t valent trois. La borne (2) exclut c_pa=0
ou c_pb=0. Toutes les paires positives ont ainsi un ou deux voisins
communs dans N. Alors X_p=c_pa+c_pb-2 et

    0<=ell_p=c_pa+c_pb-2-W_p<=2,
    W_p<=c_pa+c_pb-2.                                       (6)

Pour chaque p, parmi ses 65 non-voisins dans Z, exactement

- ell_p ont zéro voisin commun avec p dans N ;
- 40+2W_p en ont un ;
- 27-c_pa-c_pb-W_p en ont deux.

Les six voisins de p dans Z induisent deux arêtes et deux sommets
isolés : quatre sont appariés entre eux, deux avec les deux sommets
non appariés de Q. Le multigraphe des défauts de la note 245 est le
triangle sur P. Le graphe des seules arêtes sortantes de N a toujours
l'une des deux formes 3K2 ou P3+K2.

## 4. Application au registre, sans relancer les solveurs

Le script `code/codex/p3_n25_local_matching.py` lit les supports déjà
enregistrés et calcule (2) pour chacun des trois points positifs.
Il conserve les identifiants du registre. Les résultats et chaque
obstruction locale figurent dans `data/codex_p3_n25_local_matching.json`.

Sur les 5 345 supports encore non exclus, 764 violent une inégalité
locale. Ce total inclut les 158 supports de delta=10,11,12 supprimés
par la borne globale transmise par LAP. Les **606 autres exclusions**
proviennent du raffinement par sommet, même lorsque 3<=delta<=9.

Les 4 581 supports non exclus se répartissent par delta=3,...,9 en

    209, 496, 914, 1155, 1054, 596, 157.

Ces nombres comptent des supports à renommage près, pas des graphes
réalisés. La contrainte nécessaire est renforcée ; la configuration
obligatoire n'est pas entièrement exclue.

Un seul pilote a ensuite été fait au bord pour delta=3, sur le support
numéro 4. Sa relaxation de multiplicité des masques est numériquement
faisable (résidu maximal 2,8e-13 environ), sans conclusion d'existence
d'un SRG. Résultat conservé dans `data/codex_p3_n25_delta3_pilot.json`.
Cela ne justifie pas une reprise volumineuse du même filtre ; la suite
utile est le couplage entre les triangles sortants et les petits
ensembles de sommets comptés par ell_p.

Reproduction courte, sans optimisation :

    python code/codex/p3_n25_local_matching.py
