# 166 — Norme 16 sans involution : exactement cinq cœurs de support

7 octobre 2026. Codex, suite de la note 165. Aucune hypothèse de symétrie du graphe.

**Résultat.** Si un srg(99,14,1,2) possède un vecteur propre entier de valeur −4 et de norme carrée 16,
son support est constitué de deux ensembles indépendants P,Q de huit sommets. À permutations indépendantes
de P et Q près, il existe exactement **cinq** matrices possibles pour les arêtes entre P et Q.

Cette classification porte seulement sur les 16 sommets du support. Aucun des cinq cœurs n'est ici exclu
comme sous-graphe d'un SRG, et aucune complétion aux 99 sommets n'est construite.

## 1. Les supports sont indépendants

Par la note 165 §2, un vecteur entier de norme 16 prend seulement les valeurs 0,1,−1. Écrivons-le 1_P−1_Q.
L'équilibre impose |P|=|Q|=8. Le comptage des arêtes entre P et Q donne e(P)=e(Q)=e, et l'identité de la note 165 devient

    Σ_ext t_x(t_x−1) = 16 − 14e − Σ_{P∪Q} a_v².

Or Σa_v² ≥ Σa_v = 4e. Donc e≥1 rend le membre de droite négatif. Ainsi e=0 : les deux supports sont indépendants.
La matrice B des arêtes P–Q a toutes ses sommes de lignes et de colonnes égales à 4 ; deux lignes distinctes,
et deux colonnes distinctes, ont un produit scalaire au plus 2.

## 2. Graphe des défauts et cycles de longueur paire

Posons M=2I+2J−BB^t. Sa diagonale est nulle, ses autres entrées sont dans {0,1,2}, et M1=2·1.
C'est donc l'adjacence d'un multigraphe 2-régulier sans boucle sur huit sommets : une union de cycles,
où un cycle de longueur 2 est une arête double.

**Tous ses cycles ont une longueur paire.** En effet, pour une composante C de longueur ℓ,
w=1_C−(ℓ/8)1 est orthogonal à 1 et vérifie Mw=2w. D'où BB^t w=0, puis B^t w=0 sur les réels.
Dans chaque colonne de B, le nombre de 1 sur C est donc (ℓ/8)·4=ℓ/2, un entier. Ainsi ℓ est pair.

Il reste cinq partitions possibles :

    8 ; 6+2 ; 4+4 ; 4+2+2 ; 2+2+2+2.

Le même raisonnement s'applique au défaut des colonnes N=2I+2J−B^tB. Le calcul ci-dessous vérifie que
ses longueurs de cycles coïncident avec celles de M pour chaque solution. Les cinq types sont donc distincts
même si l'on autorise aussi l'échange de P et Q.

## 3. Classification exhaustive, deux calculs distincts

Pour chaque M fixé dans sa forme canonique, une colonne de B est un sous-ensemble de quatre des huit points.
Les colonnes sont distinctes : deux colonnes égales auraient quatre voisins communs. Il s'agit donc de choisir
huit colonnes parmi les 70 sous-ensembles de taille quatre, avec :

- chaque point dans exactement quatre colonnes ;
- chaque paire {p,p′} dans exactement 2−M_pp′ colonnes ;
- toute paire de colonnes ayant une intersection de taille au plus deux.

Le programme `code/codex/norm16_cores.py` effectue une recherche exhaustive exacte en Python standard.
À chaque état, il choisit une contrainte encore déficitaire et branche sur **toutes** les colonnes encore
compatibles qui peuvent la remplir. Les bornes de capacité ne rejettent que les états avec trop peu de colonnes
disponibles. Deux états avec le même ensemble de colonnes déjà choisies sont identiques ; leur mémoïsation
élimine les répétitions d'ordre sans supprimer de solution. La profondeur finale est huit.

Il compare ensuite ces listes, ensemble par ensemble et pas seulement en cardinal, avec une seconde méthode :
70 variables booléennes et les contraintes ci-dessus dans OR-Tools CP-SAT, énumération complète sur un seul
processus. Les statuts terminaux sont OPTIMAL (énumération achevée) ou INFEASIBLE, jamais UNKNOWN.
Enfin, les permutations des huit points conservant M donnent les orbites des listes de colonnes.

| Cycles de M | Ensembles de colonnes, M fixé | États du calcul Python | Aut(M) | Orbites |
|---|---:|---:|---:|---:|
| 8 | 2 | 494 | 16 | 1 |
| 6+2 | 4 | 197 | 24 | 1 |
| 5+3 (contrôle de rejet) | 0 | 556 | 60 | 0 |
| 4+4 | 4 | 431 | 128 | 1 |
| 4+2+2 | 4 | 69 | 64 | 1 |
| 3+3+2 (contrôle de rejet) | 0 | 192 | 144 | 0 |
| 2+2+2+2 | 2 | 53 | 384 | 1 |

Les matrices représentantes sont stockées dans `data/codex_norm16_cores.json`. Chaque matrice est revérifiée
directement : coefficients 0/1, degrés quatre, Gram exact, défaut des colonnes non négatif et 2-régulier.
L'ensemble du calcul, symétries et comparaison CP-SAT incluses, prend environ une seconde localement.
Cela ne constitue pas une estimation du coût des complétions aux 99 sommets.

Commande :

    python code/codex/norm16_cores.py --crosscheck-ortools

Sans l'option, la classification et le calcul des orbites utilisent uniquement la bibliothèque standard de Python.

## 4. Les 83 sommets extérieurs se répartissent en 11 + 64 + 8

Pour un sommet extérieur x, notons t_x son nombre de voisins dans chacun des deux supports.
On a Σt_x=8·10=80 et Σt_x(t_x−1)=16.

**t_x≤2.** Sinon, choisissons trois voisins p_1,p_2,p_3 dans P. Chaque paire a déjà x comme voisin commun,
donc a au plus un voisin commun dans Q. Leurs trois voisinages dans Q ont chacun taille quatre et leurs
intersections deux à deux taille au plus un. Leur réunion a donc taille au moins 12−3=9, impossible dans Q
qui a huit points.

Il y a donc exactement huit sommets de type t=2 (ensemble D), 64 de type t=1 (ensemble S), et onze de type t=0
(ensemble Z). Les huit sommets de D réalisent les huit arêtes du multigraphe M : leurs deux voisins dans P
forment ces arêtes, avec les multiplicités de M. Ils réalisent de même les huit arêtes du défaut N sur Q.
Une complétion doit donc, d'abord, apparier ces deux listes de huit arêtes.

Un sommet de D adjacent à {p,p′} et {q,q′} exige que le sous-graphe de B sur ces quatre points soit un couplage
(éventuellement vide) : le voisinage d'un sommet du SRG est l'union de sept arêtes disjointes.
Chaque sommet de S s'attache à une cellule (p,q). Son nombre dans cette cellule est forcé :

    2−B_pq − nombre de sommets de D adjacents à p et q.

Ce nombre doit être positif ou nul. Ces conditions donnent de premiers filtres finis, sans prétendre suffire.

## 5. Contraintes supplémentaires à l'extérieur

Pour y extérieur, notons d_D(y), d_S(y), d_Z(y) ses degrés dans les trois ensembles. Les comptes des voisins
communs avec tous les sommets de P donnent :

| Position de y | Identités de degrés |
|---|---|
| y ∈ D | d_S(y)+2d_D(y)=6 ; d_Z(y)=4+d_D(y) |
| y ∈ S | d_S(y)+2d_D(y)=11 ; d_Z(y)=1+d_D(y) |
| y ∈ Z | d_S(y)+2d_D(y)=16 ; d_D(y)=2+d_Z(y) |

Par exemple, pour y∈D, la somme des nombres de voisins communs avec P vaut 2·8−2=14 ; ses deux voisins
dans Q y contribuent pour huit, d'où d_S+2d_D=6. Le degré total restant vaut dix, d'où d_Z=4+d_D.
Les deux autres lignes se démontrent de la même manière.

En comptant les arêtes D–Z dans les deux sens, on obtient

    e(Z) = e(D)+5.

Ainsi, à la différence du cas de norme 14, Z ne peut pas être indépendant. Transporter à cette branche la
configuration de deux cocliques de Hoffman de la note 165 serait incorrect.

## 6. Portée

Les deux programmes classent le même petit problème de support par des méthodes distinctes ; les preuves de
réduction expliquent pourquoi tous les vecteurs de norme 16 sont couverts. Il reste à étudier les attaches de D,
les arêtes parmi D,S,Z et les contraintes globales du SRG. Aucun lancement de cette recherche n'est inclus dans
la présente note. Les résultats à 243 de la note 165 demeurent des contrôles d'une autre valeur propre et d'un
autre palier de norme ; ils ne décident pas ces cinq types propres aux paramètres 99.
