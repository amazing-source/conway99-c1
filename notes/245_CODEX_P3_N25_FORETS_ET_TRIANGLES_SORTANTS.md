# 245 — Cible P3/N25 : forêts courtes et triangles obligatoirement sortants

9 octobre 2026. Exploitation du message LAP relayé par LAB au numéro 496.

**Résultat analytique.** Soient P et N deux ensembles disjoints de sommets
d'un SRG(99,14,1,2), avec P indépendant, |P|=3, |N|=25, et

    (A+4I)(1_P-1_N)=-4*1.                                    (1)

Alors le graphe induit sur N est une forêt de douze arêtes : des chemins
sur au plus sept sommets, des sommets isolés et au plus une étoile K1,3.
Il reste 32 formes possibles de cette forêt avant attachement à P.
De plus, **au moins deux arêtes de N ont leur troisième sommet de triangle
hors de P union N**. Une inégalité plus précise figure en section 4.

**Renforcement par une exclusion finie exacte : au moins trois de ces
arêtes ont leur triangle complété à l'extérieur.** Le cas delta=2 est
exclu pour tous ses 146 supports : 61 certificats spectraux entiers et
85 certificats entiers sur les multiplicités des voisinages extérieurs.

Ces résultats ne supposent aucun rang. Dans S0 — rang 43, sans racines,
sans normes 16,18,20,22,24 — le programme neuf classes de LAP force au
moins dix configurations (1). Le présent théorème restreint ces objets
obligatoires ; **S0 reste ouvert**.

## 1. Donnée de pair et conventions

Le message 496 cite le commit `aae5e1efb` de
`conway99-c2-aws/c1_mandat_c_transformations/`, programmes `r43full.py`,
`z9lin.py`, note section 13. Le programme rationnel exact donne, dans S0,
entre 10 et 300 vecteurs y de classe deux et de norme 208/9 dans L9.
LAP donne leur profil :

    y=(2/9)1+1_P-1_N, |P|=3, |N|=25, P indépendant,

avec l'équation (1). Cette donnée est utilisée sans reproduire son calcul.
L'exclusion complète de (1) fermerait S0, mais n'est pas obtenue ici.

Poser Z=V(Gamma) sans (P union N), donc |Z|=71, et d(v)=|N(v) inter P|
pour v dans N. L'équation (1) implique :

- chaque p de P a huit voisins dans N et six dans Z ;
- chaque q de N a exactement d(q) voisins dans N, avec 0<=d(q)<=3 ;
- chaque z de Z a 4+k(z) voisins dans N, où k(z)=|N(z) inter P|.

Ainsi e(N)=12. Si n_i compte les sommets de N de degré i dans N,

    n1+2n2+3n3=24,       n0=1+n2+2n3,
    u:=n2+3n3 <= 6.                                          (2)

La dernière borne compte les voisins communs des trois paires de P.

## 2. Une forêt, des chemins courts, une étoile au plus

Un triangle dans N aurait deux sommets adjacents de degré au moins deux.
Leurs ensembles de voisins dans P, de taille au moins deux dans P3,
s'intersectent : avec le troisième sommet du triangle, cela ferait deux
voisins communs pour une arête. Un cycle de longueur quatre est également
impossible : deux sommets opposés auraient leurs deux voisins communs
dans le cycle et au moins un dans P.

Deux sommets de degré trois partageraient les trois points de P, ce qui
est impossible. S'il existe un sommet de degré trois, chacun de ses
voisins dans N a degré un, sinon leur arête aurait au moins deux voisins
communs dans P. Ses trois feuilles portent trois labels distincts dans P.
Il constitue donc une composante K1,3. Écrire s=n3, avec s dans {0,1}.

Les autres composantes non triviales sont des chemins ou des cycles.
Un sommet de degré deux porte l'un des labels AB,AC,BC. Deux tels sommets
à distance un ou deux dans N ne peuvent avoir le même label : cela
violerait respectivement lambda=1 ou mu=2. Le long de sommets consécutifs
de degré deux, les trois labels alternent donc périodiquement.

Un cycle a ainsi une longueur multiple de trois, au plus six par (2).
Il ne reste que C6. Mais P et ce cycle induiraient la grille 3 par 3.
Toutes les paires de cette grille ont déjà leurs nombres complets de
voisins communs. Chaque sommet extérieur a donc au plus un voisin dans
la grille. Ses 9*(14-4)=90 incidences extérieures et les 90 sommets
extérieurs imposent exactement un voisin pour chacun. Or (2) donne alors
sept sommets isolés de N, anticomplets à la grille. Contradiction.

Pour supprimer les chemins sur huit sommets, on utilise le comptage
suivant. Si H est un sous-graphe induit sur h sommets, avec e arêtes et

    W=sum_{v dans H} binom(deg_H(v),2),

le nombre z0 de sommets extérieurs anticomplets à H vérifie

    z0 <= h^2-16h+99+e-W.                                    (3)

En effet, les degrés t_z vers H vérifient

    sum t_z=14h-2e,
    sum binom(t_z,2)=2 binom(h,2)-e-W,

et sum_{t_z>0}(t_z-1)<=sum binom(t_z,2).

Un chemin sur huit sommets consommerait les six sommets de degré deux
autorisés. P et ses six sommets intérieurs induisent la grille 3 par 3
privée d'une arête : h=9, e=17, W=48. La borne (3) autorise au plus cinq
sommets extérieurs anticomplets, mais N en contient sept. Les chemins
plus longs sont déjà interdits par n2<=6.

## 3. Trente-deux formes du graphe négatif

Noter b_l le nombre de composantes chemins avec l arêtes, 1<=l<=6.
On a

    sum l*b_l+3s=12,
    n2=sum (l-1)*b_l,
    n0=1+n2+2s,       n2+3s<=6.                              (4)

Ces équations donnent 29 formes sans étoile et sept avec une étoile.
Quatre des premières sont impossibles : celles où n2<=2.

En effet, une paire de P n'a alors aucun voisin commun dans N. Ses deux
voisins communs z,z' sont dans Z. Pour un sommet extérieur adjacent à k
points de P,

    sum_{q dans N(z) inter N} d(q) <= 6-k.

Il a 4+k voisins dans N ; au moins 2k-2 d'entre eux sont donc isolés
dans N. Chacun de z,z' touche au moins deux isolés. Ils ne peuvent en
partager un, puisqu'ils partagent déjà les deux points de P. Il faudrait
au moins quatre isolés, contrairement à n0=1+n2<=3.

Il reste donc **25 formes sans étoile et sept avec étoile**. Il s'agit
des formes de N uniquement, pas de 32 supports complets ni de 32 SRG.

## 4. Comptage direct des triangles sortants

Soit delta le nombre d'arêtes de N dont l'unique troisième sommet de
triangle est dans Z. Comme N est sans triangle, les 12-delta autres
arêtes ont leur troisième sommet dans P. Poser

    c_ab=|N(a) inter N(b) inter N|, pour {a,b} dans P,
    X_P=2 sum_{a<b} binom(c_ab,2),
    X_N=sum_{p dans P, w dans N}
             binom(|N(w) inter N(p) inter N|,2).

Alors sum c_ab=u, 0<=c_ab<=2, et X_N>=0. On obtient l'inégalité

    3*delta >= 21-4u+X_P+X_N.                               (5)

**Preuve.** Pour p dans P et z dans Z, poser
d_p(z)=|N(p) inter N(z) inter N|. Ce nombre est au plus un si p~z,
au plus deux sinon. Par conséquent

    h:=sum_{p,z} (d_p(z)-binom(d_p(z),2))

compte les couples (p,z) avec au moins un voisin commun dans N.

Chaque voisin q dans N porte d(q) labels et a 14-2d(q) voisins dans Z :

    sum_{p,z} d_p(z)=sum_q d(q)(14-2d(q))=288-4u.

Les huit voisins dans N de chaque p induisent un appariement. En tout,
ces trois appariements portent 12-delta arêtes. Parmi les 3*binom(8,2)
paires comptées, les paires non adjacentes partagent déjà p. Compter
leur éventuel autre voisin commun donne exactement

    sum_{p,z} binom(d_p(z),2)=72+delta-X_P-X_N.

Ainsi h=216-4u-delta+X_P+X_N.

Il y a 3*71-18=195 couples (p,z) non adjacents. Quant aux couples
adjacents comptés dans h, ils correspondent exactement aux arêtes P-N
dont le triangle sort du support. Leur nombre est 24-2(12-delta)=2delta.
D'où h<=195+2delta, ce qui prouve (5).

Comme X_P>=2 max(0,u-3) et u<=6, le membre droit de (5) est au moins
trois. Donc delta n'est pas nul. **Ce seul comptage remplace les 29
certificats de l'ancienne sous-famille complètement triangulée.**

Le cas delta=1 est également impossible. Pour chaque p, le nombre
d'arêtes P-N dont le triangle sort vaut huit moins deux fois le nombre
d'arêtes de l'appariement interne : il est pair. Si q-r était la seule
arête sortante de N, chacun de q et r aurait exactement un label positif
dont le triangle sort. Ces labels seraient distincts, puisque q et r
n'ont aucun voisin commun dans P. Deux points de P auraient donc chacun
exactement une telle arête sortante, contredisant la parité.

En particulier delta>=2. Si delta=2, (5) impose :

- u=5, X_P=4, X_N<=1 ; ou
- u=6, X_P=6, X_N<=3.

Plus généralement, les triangles manquants définissent un multigraphe
eulérien sans boucle sur P. À chaque q de N, associer bijectivement
ses arêtes sortantes dans N aux labels positifs dont le triangle P-q
sort également. Ces deux ensembles ont la même taille. Une arête
sortante q-r relie alors les deux labels associés ; ils sont distincts,
car q et r n'ont aucun voisin commun dans P. Chaque degré dans ce
multigraphe est pair par le comptage huit moins deux fois un appariement.

**Conséquence pour la première tranche encore ouverte, delta=3 :** ce
multigraphe est exactement le triangle sur P. Chaque point de P a deux
arêtes P-N dont le triangle sort. Dans N, une arête sortante a forcément
une feuille comme extrémité, puisque deux sommets de degré au moins deux
partageraient un label positif. Le graphe formé uniquement des arêtes
sortantes est donc soit trois K2 disjoints, soit P3+K2. Dans le second cas, les deux feuilles du
P3 portent le même label C, son centre porte AB, et le K2 restant relie
les défauts A et B. Cela donne deux géométries précises à exploiter ensuite.

La preuve des sections 2 à 4 est autonome et n'utilise aucun solveur.

## 5. Exploration finie avec les triangles extérieurs autorisés

`code/codex/p3_n25_open_triangles.py` énumère les 32 forêts puis tous
leurs attachements à P. Une feuille porte un label singleton et un
sommet de degré deux un label parmi AB,AC,BC. Les feuilles peuvent
porter un label absent de leur voisin dans N : cette possibilité est
essentielle. On impose les degrés huit de P, les contraintes locales
lambda/mu, la borne (5) et delta>=2, puis on quotient par permutation
de P, permutation des composantes et retournement des chemins.

Résultat : 6 899 supports passent ces contraintes. Pour 1 469 d'entre
eux, un vecteur entier donne un quotient strictement négatif dans l'un
des deux Grams positifs nécessaires

    27I-9A_H+J,       44I+11A_H-2J.

Chaque certificat est évalué en arithmétique entière. Les 5 430 autres
supports ne sont pas déclarés réalisables. Parmi les supports avec
delta=2, 61 sont exclus de cette façon et 85 restent à ce stade.

Le modèle au bord emploie tous les masques autorisés sur P union N,
avec k voisins dans P et 4+k dans N, les bornes locales lambda/mu et
les annulations imposées par les noyaux des Grams. Une arête n'est
interdite dans un masque que si son triangle est déjà interne. Les
équations imposent 71 sommets extérieurs, les degrés résiduels et les
nombres résiduels de voisins communs de chaque paire. Une contradiction
est conservée sous forme d'un certificat entier de combinaison linéaire.

Le premier pilote sur trois supports distincts de delta=2 donne trois
exclusions exactes. La tranche complète a ensuite été terminée : les
85 supports restants sont tous exclus par des certificats entiers de
bord, conservés dans `data/codex_p3_n25_delta2.json`. Avec les 61
certificats spectraux de l'énumération, **tous les supports delta=2
sont exclus**. Cela renforce delta>=2 en **delta>=3**.

Concrètement, si M est la matrice des masques et b le vecteur des
obligations, chaque certificat fournit un vecteur entier a tel que

    sum_j min(0,71*(a^T M)_j) > a^T b.

Or les multiplicités vérifient Mx=b et 0<=x_j<=71. La contradiction
ne dépend donc pas de l'arrondi ou du statut annoncé par le solveur.
Les coefficients et cette inégalité ont été contrôlés en entiers à
la production de chaque certificat. Le solveur ne sert qu'à les trouver.

Reproduction :

    python code/codex/p3_n25_open_triangles.py
    python code/codex/p3_n25_open_triangles.py --delta 2 --dual-first --boundary-out data/codex_p3_n25_delta2_rerun.json

La deuxième commande recalcule les 85 certificats au bord ; elle n'est
pas nécessaire pour utiliser le résultat déjà conservé. Au total,
1 554 des 6 899 supports énumérés sont maintenant exclus, dont tous
ceux ayant delta=2. Les 5 345 supports non exclus ont delta>=3. Ce
décompte ne signifie pas qu'ils se prolongent en un graphe à 99 sommets.

## 6. Correction de portée conservée explicitement

Une première liste de 29 supports supposait que toutes les arêtes du
support avaient leur triangle à l'intérieur. Ses 18 certificats spectraux
et 11 certificats de bord excluent correctement cette sous-famille.
Elle ne couvrait pas les attachements où des triangles sortent.

L'annonce de fermeture S0 au message 500 était donc incorrecte et a été
retirée au message 501, avant publication de cette note. Les fichiers
`p3_n25_saturated.py` et `codex_p3_n25_saturated.json` indiquent désormais
explicitement cette hypothèse. Ils sont conservés comme trace de la
découverte ; la section 4 donne une preuve plus courte de leur conclusion
correcte. L'exclusion complète de delta=2 utilise l'énumération corrigée
avec triangles extérieurs autorisés. **Ni S0 ni le rang 43 ne sont
déclarés exclus.**
