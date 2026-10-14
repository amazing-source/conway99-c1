# C1 — journal de recherche de la nuit du14 octobre2026

## Consigne et état de départ —02h06 Paris

Travail continu demandé par Dilan, relayé par Claude LAB. Repartir de la
définition de SRG(99,14,1,2), sans rouvrir les anciennes notes de Codex ou
de LAB. Aucun calcul payant ; aucune relance des campagnes UNKNOWN.
But : exclusion, réduction finie abordable démontrée, ou contraintes
supplémentaires effectives pour le solveur. Les résultats restent distincts
des hypothèses et des témoins de relaxations.

Ce nouveau fichier reçoit les preuves et les points de reprise. Commits
fréquents ; signe de vie à Claude au moins toutes les45minutes. Session
du pont :01a1379f-6e0a-7da2-8355-ea6b7c7eda46. Le lecteur automatique
est actif, curseur619 au départ. Le fichier historique modifié
`code/codex/coheawood_completion.py` est laissé intact.

## Axiomes utilisés

G a99 sommets, degré14 ; deux sommets adjacents ont exactement un voisin
commun, deux sommets non adjacents exactement deux. Sa matrice A vérifie

    A=A^t, diag A=0, A_ij dans{0,1}, A1=14*1,
    A²+A=12I+2J.

Chaque voisinage induit est donc un appariement de sept arêtes. Toute
arête appartient à un unique triangle ; il y a231 triangles, sept par
sommet. Un sommet extérieur à un triangle touche au plus un sommet de
celui-ci, sinon une arête aurait deux voisins communs.

Cible initiale : exploiter la coexistence de ces231 triangles et les
relations entre triangles disjoints. Une identité dérivée n'est pas encore
une réduction ; chercher une conséquence entière ou une obstruction
qui élimine des choix dans un système commun.

## 02h22 — Coupure sur le triangle de base : au plus neuf prismes

**Résultat prouvé à partir des seuls axiomes.** Il existe un triangle T
qui a au plus neuf triangles disjoints U reliés à T par trois arêtes.
Le nombre total de ces paires non ordonnées (prismes triangulaires
induits) est au plus1151. Cela exclut la famille où chaque triangle a
au moins dix partenaires de prisme. Dans toute recherche à triangle
de base libre, on peut imposer p(T)<=9 sans perdre de candidat.

Voici la preuve, avec normalisations explicites. Le projecteur P sur
l'espace propre -4 de A est (27I-9A+J)/63. Posons

    u_x = sqrt(63) P e_x ; q_T = sqrt(7) P 1_T.

Les produits des u sont28 sur la diagonale, -8 sur les arêtes, 1
sur les non-arêtes. Le produit u_x.q_T vaut4 si x appartient à T,
-2 si x est extérieur et voisin de T, 1 sinon. Il y a respectivement
3,36,60 sommets dans ces cas. Les produits des q valent4 sur la
diagonale, 0 pour deux triangles sécants, et1-j pour deux triangles
disjoints ayant j arêtes entre eux. Ces arêtes forment un appariement.

Pour un triangle T, écrivons p=p(T)=n_3. On a

    n_0=32-p, n_1=144+3p, n_2=36-3p, n_3=p.

Justification : il y a212 triangles disjoints, somme j*n_j=216.
Avec N l'incidence sommets-triangles, NN^t=A+7I, donc la Gram M des q
vérifie M²=21M et M1=0. Ces deux identités donnent respectivement
16+n_0+n_2+4p=84 et4+n_0-n_2-2p=0. On en déduit les formules.
En particulier0<=p<=12.

Considérons les tenseurs symétriques réels

    S = somme_T q_T tensor q_T tensor q_T,
    V = somme_x u_x tensor u_x tensor u_x.

Le produit des cubes tensoriels est le cube du produit scalaire. Avec
p_bar la moyenne sur les231 triangles, les comptes précédents donnent

    ||S||² = 231*(64+n_0-n_2-8p_bar) = 1386*(10-p_bar),
    <S,V> = 231*(3*64-36*8+60) = -8316,
    ||V||² = 99*(28³-14*8³+84) = 1471932.

Cauchy-Schwarz impose ||S||²>=2772/59, donc

    p_bar <= 588/59 < 10,
    somme_T p(T) <= 135828/59,
    nombre de prismes = (somme_T p(T))/2 <= 1151.

La dernière inégalité utilise l'intégralité du nombre de paires. Il
existe donc T avec p(T)<=9. La positivité des seuls cubes q ne donnait
que p_bar<=10 ; le couplage avec les99 sommets est essentiel pour
éliminer l'égalité dix.

**Lecture pour le solveur.** Les36 voisins extérieurs de T se partagent
en X_a,X_b,X_c, douze par sommet de T. Chaque X induit un appariement,
et chaque paire de X est reliée par un appariement parfait : pour
x dans X_a et b dans T, les deux voisins communs de x,b sont a et
un unique sommet de X_b. Après avoir normalisé les appariements
X_a-X_b et X_a-X_c à l'identité, celui de X_b-X_c est une permutation
pi de douze lettres. Ses points fixes sont exactement les p(T)
triangles transversaux. On peut donc exiger au moins trois lettres
déplacées par pi (au plus neuf points fixes). Le choix du triangle
de base est libre : ce n'est pas une borne locale pour tous les T.

**Vérification.** `code/codex/night_20261014/triangle_frame_moments.py`
calcule les produits et bornes en arithmétique rationnelle SymPy, et
vérifie les polynômes des quatre projecteurs du graphe d'intersection
des triangles modulo z(z-18)(z-7)(z+3). Rapport dans
`data/codex_night_20261014/triangle_frame_moments.json`.

**Suite.** Examiner les contraintes conjointes sur les trois codages des
60 non-voisins du triangle ; chaque codage est une bijection avec les
60 paires non appariées d'un X de douze sommets. Aucun lancement de
campagne UNKNOWN. Message623 de Claude lu : résultats indépendants
sur la même Gram et sur les grilles, pas utilisés comme ancienne note.
