# 253 — Norme 16 : un sommet lointain isolé est forcé

10 octobre 2026. Suite de la note251. Aucun rang global supposé.

**Théorème.** Dans la partition P,Q,D,B,Z associée à tout vecteur propre
entier de valeur−4 et de norme carrée16, le sous-graphe Z contient un
sommet isolé. La forme Z=4K2+P3 est impossible. La liste de la note251
se réduit donc de15 à **14 formes**, soit **70 supports connus sur27
sommets** avec les cinq cœurs. Cela n'exclut pas la norme16.

## 1. Un budget local pour chaque sommet double

Notons k_z=d_Z(z). Pour d dans D, compter les voisins communs de d
avec les sept autres sommets de D. Leur nombre total est14-d_D(d).
Les quatre voisins de d dans le cœur ont chacun exactement deux
voisins D ; ils contribuent donc4. D induit au plus une arête, donc
aucun voisin commun de deux D n'appartient à D.

Chaque z voisin de d dans Z contribue d_D(z)-1=1+k_z. Enfin la
contribution des simples est

    L_d = sum_{b dans B voisin de d} (d_D(b)-1) >= 0.

Comme d_Z(d)=4+d_D(d), on obtient l'identité

    L_d = 6-2d_D(d)-sum_{z dans N_Z(d)} k_z.              (1)

En particulier, la somme des degrés Z vus par d est au plus6 si d
n'a pas de voisin D, et au plus4 si d est extrémité de l'unique arête D.

## 2. L'unique arête D forme son triangle avec un sommet Z

Le cas où D est indépendant est déjà réglé : les sept formes de la
note251 à cinq arêtes Z ont toutes au moins un isolé. Supposons donc
que D possède l'unique arête de. Posons R=N_Z(d), T=N_Z(e).
On a |R|=|T|=5 et, par(1), sum_R k_z<=4, sum_T k_z<=4.

Si R et T étaient disjoints, leur union couvrirait dix des onze
sommets Z. Or sum_Z k_z=12 et Delta(Z)<=3, donc la somme sur cette
union serait au moins9, contradiction. Comme d,e sont adjacents,
ils ont exactement un voisin commun : il s'agit donc d'un unique
sommet z* dans R inter T. En particulier, **les deux extrémités de
l'arête D n'ont aucun voisin commun dans le cœur ni dans B.**

L'union R union T contient neuf sommets ; noter u,v les deux sommets
Z omis. Tout voisin Z de z* appartient à {u,v} : sinon une arête dz*
ou ez* aurait deux voisins communs. Ainsi k=d_Z(z*)<=2. La somme
des deux bornes(1) donne

    12-k_u-k_v+k <= 8,
    donc k_u+k_v >= 4+k.                                (2)

## 3. Le troisième sommet est isolé ou appartient à une forme précise

Si k=2, le chemin u-z*-v impose k_u+2+k_v<=5 par la note251,
contrairement à(2). Donc k<=1.

Si k=1, le budget W_Z=sum binom(k_z,2)<=4 interdit deux sommets
de degré3. Avec Delta(Z)<=3, on a k_u+k_v<=5. L'égalité est forcée
par(2), et leurs degrés sont3,2. Ils consomment tout le budget W_Z=4.
Le graphe Z est donc exactement

    K1,3 + P3 + K2 + 2 K1.

Il possède deux sommets isolés. Le sommet z* est une feuille de
l'étoile ou du P3, son voisin étant l'un des deux sommets omis.

Si k=0, z* est lui-même isolé. Cela achève le théorème.

## 4. Les attaches des extrémités de l'arête D sont plus rigides

Dans le cas k=1, l'égalité k_u+k_v=5 implique L_d+L_e=0 par(1),
donc L_d=L_e=0.

Dans le cas k=0, on a4<=k_u+k_v<=5. Si la somme valait5, les
degrés seraient3,2 et W_Z=4. L'identité de la note251 donnerait
W_B=9-5-W_Z=0. Tous les simples auraient au plus un voisin D,
donc L_d=L_e=0. Mais(1) donnerait alors L_d+L_e=5-4=1,
contradiction. Ainsi k_u+k_v=4 et, de nouveau, L_d=L_e=0.

Dans les deux cas :

- chaque extrémité D voit cinq sommets Z de somme des degrés exactement4 ;
- chacune voit quatre simples B ; ces huit simples sont distincts et
  chacun a **exactement un voisin dans D** ;
- si z* est isolé, les deux sommets Z omis ont degrés(2,2) ou(3,1) ;
- si z* est une feuille, la forme de Z est celle du paragraphe3.

Ces contraintes doivent servir avant d'énumérer les incidences D–Z
dans la branche à une arête D. Elles éliminent notamment toute arête
D dont les deux ombres au cœur ont une intersection non vide.

**Saturation de toutes les paires incidentes aux extrémités.** Pour tout
autre sommet j de D, aucun simple n'est voisin à la fois de d et j,
ni à la fois de e et j. Posons C_dj le nombre de leurs voisins communs
au cœur. Les incidences X entre D et Z satisfont donc exactement

    (XX^t)_dj = 2-C_dj,   (XX^t)_ej = 2-C_ej.            (3)

Écrire alpha_j=1 si j voit z*, et0 sinon. Comme R,T ont pour
intersection{z*} et pour complément{u,v}, (3) implique

    |N_Z(j) inter {u,v}| = C_dj+C_ej+alpha_j.            (4)

Ainsi C_dj+C_ej<=2 pour chacun des six autres j. Si z* est isolé,
tous les alpha_j sont nuls. Si z* est une feuille, exactement un de
ces six alpha_j vaut1, et ce j doit vérifier C_dj+C_ej<=1. Une fois
R,T fixés, les intersections des six autres lignes avec les deux
ensembles de quatre points R\{z*}, T\{z*} sont donc imposées par C
et alpha. Ce filtre précède toute recherche des attaches simples.

## 5. Un autre point de départ couvrant pour la norme16

Choisir un sommet z isolé de Z, dont le théorème force l'existence.
On connaît son voisinage par types :

    N(z) = deux sommets D + douze sommets B.

Il ne contient ni sommet du cœur ni autre sommet Z. Chaque point p
du cœur est non adjacent à z, donc possède exactement deux voisins
dans N(z). Après choix des deux D, le nombre des douze simples qui
touchent p est exactement2 moins le nombre de ces deux D qui touchent p.

Les douze simples, étiquetés par leurs cellules(P_i,Q_j), forment
ainsi les douze arêtes d'un **multigraphe biparti de degré au plus2**
sur P union Q, avec degrés entièrement imposés par les deux D choisis.
Les multiplicités des cellules ne peuvent dépasser celles de la note169.

Le support cœur+Z+N(z) possède41 sommets et inclut les deux relations
f=1_P-1_Q et4e_z+1_N(z) modulo sept. Cette piste offre un cadre
couvrant supplémentaire, à développer ; aucune borne sur le nombre
de tels cadres ni exclusion par leur rang n'est affirmée ici.

## 6. Organisation du catalogue local D–Z

Pour D indépendant, poser C_de=|N(d) inter N(e) inter(P union Q)|
pour d!=e, C_dd=0. C est l'adjacence d'un multigraphe4-régulier
sur8 sommets, de multiplicités<=2 : les quatre points du cœur vus
par d ont chacun un second voisin D.

Une fois Z fixé, toutes les contraintes locales sur cœur+D+Z
dépendent de l'attache au cœur uniquement par C. Pour une matrice
d'incidence X entre D et Z, elles s'écrivent :

    X1=4*1 ; X^t1=2*1+A_Z*1,
    (XX^t)_de <= 2-C_de                        (d!=e),
    (X^tX)_zw <= 2-(A_Z)_zw-(A_Z²)_zw          (z!=w),
    (XA_Z)_dz <= 2-X_dz.

Le script `norm16_D_intersection_types.py` regroupe les478 attaches
archivées en **86 types de C**, avec les permutations explicites de
chaque attache vers son représentant. Cela permet de réutiliser un
catalogue local pour plusieurs attaches ; ce n'est pas une identification
des complétions globales correspondantes.

Le compteur `norm16_dz_catalogue.cpp` choisit les huit lignes binaires
de X, propage les degrés et les budgets de paires, et quotiente les
automorphismes de Z par stabilisateurs successifs. Le choix de la ligne
D suivante dépend seulement des tailles de domaines et de son indice,
donc est invariant sous les automorphismes Z encore permis. À chaque
étape, une ligne minimale dans son orbite est gardée, puis son
stabilisateur devient le groupe de l'étape suivante. Les permutations
supplémentaires des D conservant l'attache ne sont pas quotientées.

Premier résultat exhaustif pour cœur8, attache0, Z=P3+P4+4K1 :
**1696 incidences modulo Aut(Z)**, avant les attaches des64 simples.
Cela ne donne pas encore un ordre de grandeur global du catalogue.
Le premier compteur Python s'était arrêté à20 secondes ; son compte
partiel n'est pas utilisé comme total. Le compteur C++ achève ce cas.

Le fichier `codex_norm16_far_forest_refined.json` retire la forme15
de la liste historique, en conservant les identifiants des14 autres.
Les notes251/252 et leurs anciens fichiers restent lisibles avec leurs
identifiants d'origine.

Le programme `norm16_D_edge_reduction.py` applique les conditions
C_de=0 et C_dj+C_ej<=2 aux arêtes D encore possibles après les bornes
locales sur cœur+D. Sur les478 attaches, les positions d'arêtes D
étiquetées passent de3317 à2145. Ces positions ne sont pas quotientées
par les stabilisateurs des attaches ; ce n'est pas un nombre de graphes.
Aucune attache entière n'est ainsi exclue, puisque la branche D
indépendant reste possible.

Reproduction du petit comptage exhaustif :

    python code/codex/norm16_dz_catalogue.py --write-instance data/codex_norm16_dz_instance_0_0_2.txt
    g++ -std=c++20 -O3 code/codex/norm16_dz_catalogue.cpp -o norm16_dz_catalogue
    ./norm16_dz_catalogue data/codex_norm16_dz_instance_0_0_2.txt 30

La première commande utilise NetworkX pour les automorphismes de Z.
Le compteur C++ n'a pas de dépendance externe. Une sortie STOPPED donne
seulement un compte partiel ; EXHAUSTED signifie que le problème local
indiqué a été entièrement énuméré.
