# 248 — Capacité triangulaire d'un bloc extérieur

9 octobre 2026. Suite du message LAB 515, relayant le pilote LAP.

## Résultat transmis par LAP, sans reproduction du calcul

LAP annonce 59 exclusions parmi les 252 premiers supports du registre
ouvert de 4 581 supports : par delta de 3 à 9, respectivement
15/25, 16/44, 16/61, 9/60, 3/40, 0/19, 0/3. Les certificats de Farkas
sont annoncés rationnels et contrôlés exactement sur toutes les colonnes.
Aucun de ces 59 certificats n'utilise les lignes de triplets. Exemple
transmis : support 443, delta=4, 26 312 blocs, valeur -679979/500000.
La liste des IDs et les certificats doivent encore être transmis.
Source annoncée : `conway99-c2-aws`, commit `300c2a6c7`, dossier
`c1_mandat_c_transformations/p3n25_search/`.

Ce sont de nouvelles applications de la relaxation au registre ouvert.
Les deux conditions soupçonnées d'être absentes de notre ancien modèle
y figurent déjà : dans `p3_n25_open_triangles.py`, le filtre
`candidates @ a <= 2 - candidates` impose simultanément l'appariement
induit dans le bloc et au plus deux voisins dans le bloc pour chaque
sommet extérieur au bloc. Les nombres de blocs des supports 4 et 443
sont bien respectivement 24 602 et 26 312 avec ces conditions. Notre
ancien pilote n'avait pas testé tous ces supports : la faisabilité du
support 4 n'impliquait pas celle des 4 581. Aucune supériorité de cette
relaxation sur l'ancienne n'est donc établie par ce seul résultat.

## Une condition supplémentaire sur chaque bloc

Soit S un support induit, z un sommet extérieur et B=N(z) inter S.
Poser b=|B| et t=e(S[B]). Puisque lambda=1, le graphe induit par les
quatorze voisins de z est exactement un appariement de sept arêtes.
Le graphe S[B] est donc un appariement partiel. Ses b-2t sommets non
appariés doivent recevoir des partenaires distincts parmi les 14-b
autres voisins de z. Ainsi

    b-2t <= 14-b,  soit  t >= b-7.                         (1)

Ce raisonnement vaut pour tout support induit, indépendamment du rang.
Pour les blocs P3/N25, k=|B inter P| et |B inter N|=4+k, donc

    b=4+2k,     t >= max(0,2k-3).                         (2)

Il suffit donc de retirer les blocs de taille huit sans arête et les
blocs de taille dix ayant moins de trois arêtes. Ce filtre ne dépend
ni d'une solution LP ni d'un calcul spectral.

On obtient aussi la décomposition exacte du voisinage extérieur de z :

    14-b voisins hors S,
    b-2t d'entre eux ont exactement un voisin dans B,
    14-2b+2t d'entre eux n'ont aucun voisin dans B.

Les premiers complètent les triangles des sommets non appariés de B.
Les derniers sont appariés entre eux, en 7-b+t arêtes. Ces identités
pourront servir lors du choix des arêtes entre sommets extérieurs ;
elles ne construisent pas ce choix.

## Effet mesuré, sans relancer le calcul de supports

Le petit programme `code/codex/p3_n25_block_capacity.py` applique (2)
aux colonnes de cinq supports déjà enregistrés. Aucun solveur appelé,
aucune nouvelle énumération de supports, aucun support déclaré exclu.

| Support | delta | Blocs avant (2) | Blocs supprimés |
|---|---:|---:|---:|
| 4 | 3 | 24 602 | 0 |
| 443 | 4 | 26 312 | 0 |
| 623 | 4 | 28 146 | 115 |
| 3234 | 7 | 32 543 | 52 |
| 5594 | 7 | 34 996 | 25 |

Les trois derniers exemples couvrent les valeurs u=5,4,3 ; les deux
premiers ont u=6 et aucun bloc contenant deux sommets positifs. Chaque
suppression observée concerne un bloc indépendant de taille huit :
huit partenaires nécessaires pour seulement six places restantes.
Les données incluent un témoin explicite pour chaque support concerné.

Ce filtre est une petite amélioration des colonnes, pas une fermeture
de S0. Le balayage LP reste à LAP ; il n'est pas dupliqué ici. Les
certificats obtenus sur une liste plus large de colonnes restent valides
après suppression de colonnes interdites par (2).
