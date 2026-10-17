# 247 — Conséquence de la formule LAB pour le réseau lointain de rang huit

9 octobre 2026. Exploitation du message LAB 511, commit source annoncé
`d49e5c3`, branche `lab/theta-lp-2026-10-08`, dossier
`code/lab_index_2026-10-09/` de conway99-c1.

**Portée.** On utilise la formule de déterminant transmise par LAB,
obtenue par son argument à la main et ses contrôles numériques. Elle
n'est pas réauditée ici. La déduction ci-dessous est conditionnelle
à cette formule et à ses hypothèses. Aucun rang et aucun nombre de
boules supplémentaires n'est déclaré exclu.

## 1. La borne déjà disponible du côté propre +3

Le minimum manquant dans le message LAB a déjà une borne :

    min(Z^99 inter V_3) >= 12.                              (1)

C'est le lemme de la note 168, section 2, repris dans la note 174,
section 3. Pour un vecteur entier f propre de valeur 3, la somme
positive S égale la somme négative en valeur absolue. Si h est sa
plus grande coordonnée en valeur absolue, l'équation propre au sommet
correspondant donne S>=4h. Une norme carrée inférieure à douze impose
S<=5, donc h=1. Le support de chaque signe aurait alors au plus cinq
sommets et degré intérieur au moins trois, impossible avec lambda=1,
mu=2. À norme douze, les deux supports sont des prismes triangulaires
anticomplets.

Le sous-réseau des vecteurs s'annulant sur T union N(T) hérite de (1).
Cette borne douze ne contredit pas les bornes Hermite 30 à 60 annoncées
par LAB. La note 110 décrit déjà des obstacles à la route « vecteur
court de valeur 3 implique une grille » ; cette implication ne doit
pas être ajoutée.

## 2. Le réseau lointain de valeur -4 donne une condition sur tau

Pour une droite T dont le graphe local G est connexe, écrire tau pour
le nombre d'arbres couvrants de G, r=37+2k, et Lambda_-(T) pour le
réseau des vecteurs propres entiers de valeur -4 nuls sur T union N(T).
La formule annoncée par LAB est

    rang Lambda_-(T)=8,
    det Lambda_-(T)=4*7^(2k)*tau/(9*j^2),       j entier >=1. (2)

Le déterminant est ici celui du Gram, donc le carré du covolume.
Si le minimum carré du réseau entier global L est au moins m, alors
min Lambda_-(T)>=m. La constante d'Hermite en dimension huit vaut
deux : pour tout réseau euclidien K de rang huit,

    min K <= 2 (det K)^(1/8).

Une référence primaire suffisante pour cette inégalité, via
l'optimalité de l'empilement E8 (minimum deux, déterminant un), est
[Viazovska, *The sphere packing problem in dimension 8*, Annals 2017](https://annals.math.princeton.edu/2017/185-3/p07).

En combinant avec (2), on obtient

    4*7^(2k)*tau >= 9*j^2*(m/2)^8,                          (3)
    tau >= ceil(9*j^2*(m/2)^8 / (4*7^(2k))).                (4)

Le minimum global au moins quatorze, déjà établi dans la campagne,
donne en particulier

    4*7^(2k)*tau >= 9*j^2*7^8.                              (5)

En utilisant seulement j>=1 :

| Rang modulo sept | Minimum utilisé | Borne entière sur tau |
|---|---:|---:|
| 37 | 14 | 12 970 803 |
| 39 | 14 | 264 711 |
| 41 | 14 | 5 403 |
| 43 | 14 | 111 |

Dans les branches où le minimum **du réseau entier L** est plus grand :

| Hypothèse de branche | Borne entière sur tau, j>=1 |
|---|---:|
| rang 37, min L>=18 | 96 855 123 |
| rang 37, min L>=20 | 225 000 000 |
| S0 au rang 43, donc min L>=26 | 15 601 |

On peut aussi borner l'indice de saturation :

    j^2 <= 4*7^(2k)*tau / (9*(m/2)^8).

**Arrondi :** multiplier par j^2 avant de prendre le plafond. Par
exemple, au rang 37 avec m=14, la formule exacte est

    tau >= ceil(51 883 209*j^2/4).

Il ne faut pas multiplier le plafond 12 970 803 par j^2. Le message
512 contenait une formulation abrégée ambiguë de cet arrondi ; (4)
est la formule à utiliser.

## 3. Usage et limitation

Ce critère vient de la géométrie réelle et du minimum, pas des symboles
de Hasse. Il peut donc être ajouté même si les tests locaux aux primes
2,3,11 ne donnent aucun filtre nouveau. L'hypothèse de connexité de G
et le déterminant annoncé dans (2) doivent être conservés.

**Retour LAB 513 : aucun rejet sur 800 boules échantillonnées.** LAB a
calculé les nombres d'arbres couvrants exactement par Bareiss sur 400
boules connexes de chaque classe. Les statistiques transmises sont :

| Classe de G | Minimum de tau | Quantile 1 % | Médiane | Maximum |
|---|---:|---:|---:|---:|
| Sans triangle | 6,9e11 | 9,0e11 | 1,7e12 | 2,5e12 |
| Triangles autorisés | 3,9e11 | 4,9e11 | 1,4e12 | 2,5e12 |

Les valeurs du tableau sont les résumés arrondis transmis par LAB,
pas des déterminants exacts reproduits ici. Avec seulement j>=1,
aucun des seuils ci-dessus ne rejette ces échantillons. Cela ne
prouve pas que le critère soit vide sur toutes les boules ; cela
montre qu'il est trop faible sur l'échantillon testé. Il faudrait
notamment une borne inférieure supplémentaire sur l'indice j pour
espérer le renforcer. Aucune telle borne n'est disponible.

Les volumes annoncés pour le test d'étoile restent donc inchangés.
Cette condition est conservée comme conséquence secondaire, sans
prolonger cette piste par un balayage. Le pilote entier P3/N25 reste
du ressort de LAP et n'a pas été dupliqué.
