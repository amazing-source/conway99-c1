# 236 — Du dossier Convergences aux arêtes partagées du bord

9 octobre 2026. Suite à la demande directe de l'utilisateur : exploiter
le dossier et attaquer l'étape restante, pas seulement commenter son intérêt.

**Résultat de ce travail :** réduction explicite des trois bords exceptionnels
à 95 étoiles enracinées, puis construction d'inégalités exactes sur les choix
de bord qui utilisent une même arête dans les équations de ses deux extrémités.
Deux choix entiers passant les moments du bord sont exclus par ces inégalités.
Ce ne sont pas deux cas C1 exclus : ce sont deux affectations de masques dans
une seule des 95 étoiles. Les 95 étoiles et les cinq bords initiaux restent ouverts.

Le gain utile est une méthode pour renvoyer une contradiction sur les arêtes
vers le choix des masques, au lieu de recommencer une recherche complète à
chaque choix. Aucune garantie de convergence rapide de cette méthode n'est acquise.

## 1. Les 95 étoiles du sommet exceptionnel

Le dossier donne trois couples `(H,T)`, où H est le support de douze sommets
et T le triple de voisins du sommet exceptionnel z :

| Support | Triple, indexation du script | Orbites |
|---|---|---:|
| Cube | (0,5,10) | 19 |
| Wagner | (0,2,5) | 38 |
| Wagner | (0,3,9) | 38 |

Le voisinage de z contient T, les deux sommets vides du bord de H,
et neuf singletons. Les classes de ces singletons sont données par
`c = 2·1 − 1_T − A_H 1_T`, qui a neuf entrées égales à un.
Pour chaque i dans T, le singleton de classe i est apparié à i dans N(z).
Ces trois paires sont forcées. Les huit autres voisins sont appariés :
il y a exactement `7·5·3·1=105` appariements étiquetés par couple `(H,T)`.

Le script `transport_exception_star.py` prend leurs orbites sous le
stabilisateur de `(H,T)` et l'échange des deux sommets vides. Chaque action
est une permutation de la matrice du support ; chaque liste d'orbites
recouvre exactement les 105 appariements. Il en résulte 19+38+38=95
noyaux sur 24 sommets `H ∪ {z} ∪ (N(z)\H)`.

Les 75 sommets restants sont des singletons (42) ou des doubles (33)
relativement à H. Chacun a une paire distincte de voisins dans N(z).
En effet les 84 non-arêtes de N(z) ont chacune un unique second voisin
commun, et neuf de ces sommets sont déjà dans H\T. Ces étiquettes
distinctes permettent d'utiliser des variables de présence binaires
pour les masques de 24 coordonnées.

Les moments d'ordre deux et les tests spectraux individuels du nouveau
noyau restent faisables sur les 95 orbites. Ce calcul complet est archivé
dans `data/codex_transport_exception_star.json` ; il n'est pas à relancer
comme une campagne d'exclusion prometteuse en soi.

## 2. L'obstacle effectivement rencontré

Sur l'orbite zéro du Cube, un choix de 75 masques satisfait exactement :

- tous les degrés et nombres de voisins communs à l'intérieur du noyau ;
- les effectifs des classes du bord de H ;
- la limite de deux voisins communs déjà visibles pour chaque paire choisie.

De plus, les tests linéaires de capacité de voisinage, examinés séparément
pour chaque sommet extérieur, n'y détectent aucune contradiction.

Mais il n'existe même pas d'arêtes **fractionnaires dans [0,1]** entre
ces 75 sommets satisfaisant simultanément les degrés et les équations
de voisins communs entre le noyau et l'extérieur. Une arête doit être
la même dans les deux lignes de la matrice d'adjacence.

Cette impossibilité possède un certificat entier : après combinaison
des équations, leur second membre vaut −4552, alors que les bornes
des arêtes imposent au premier membre une valeur au moins −3978.
Ce choix de bord est donc réellement exclu. Ce résultat montre une
limite des tests précédents ; il ne ferme pas l'orbite qui contient
beaucoup d'autres choix.

## 3. Inégalité uniforme sur les choix de masques

Soient A l'adjacence du noyau, `b_p` les masques possibles, et `x_p`
leur présence (zéro ou un). Posons

    d_p = (1, b_p),
    t_p = (14−|b_p|, 2·1−b_p−b_p A).

Si `e_pq` est l'arête entre deux sommets extérieurs de ces masques,
les équations nécessaires sont

    Σ_q e_pq d_q = x_p t_p,
    e_pq = e_qp,       0 ≤ e_pq ≤ min(x_p,x_q).

On retire les paires qui ne peuvent être adjacentes : trop de voisins
communs dans le noyau, ou un budget de voisins communs noyau/extérieur
déjà saturé que cette arête dépasserait. Conserver d'autres paires
impossibles affaiblirait seulement le test.

Choisir arbitrairement un vecteur entier `u_p` de 25 coordonnées pour
chaque masque, et écrire

    c_pq = u_p·d_q + u_q·d_p.

En sommant les équations avec ces potentiels, on obtient

    Σ_p (u_p·t_p) x_p = Σ_{p<q} c_pq e_pq.

Pour chaque paire autorisée avec `c_pq<0`, choisir une extrémité
`a(p,q)∈{p,q}`. Puisque `e_pq≤x_a`, toute complétion satisfait

    Σ_p (u_p·t_p) x_p − Σ_{c_pq<0} c_pq x_{a(p,q)} ≥ 0.       (1)

Il s'agit d'une **inégalité linéaire entière sur tous les choix de bord**.
Elle n'exige ni rang modulo sept, ni une affectation préalable définitive
des 75 masques.

Un certificat d'impossibilité pour un choix particulier fournit les `u_p`
sur ses 75 masques ; on les prolonge par zéro aux autres. Pour une paire
dont une extrémité est absente de ce choix, on choisit cette extrémité
dans (1). L'inégalité reproduit alors exactement la contradiction du
certificat au choix courant, tout en restant valable pour les autres.
Ce n'est donc pas seulement une clause interdisant de répéter ce choix.

## 4. Deux coupes produites et frontière actuelle

Le premier certificat fournit une inégalité (1) violée de 574.
Après son ajout au problème de choix des masques, une autre affectation
entière est trouvée. Elle aussi ne possède pas d'arêtes partagées,
et donne une seconde coupe, violée de 4412. Les deux inégalités restent
compatibles avec une affectation fractionnaire des masques.

La recherche entière après ces deux coupes n'a pas tranché dans son
budget de dix secondes. Un autre modèle, avec toutes les arêtes du
graphe à distance deux de z et 711 équations de paires imposées dès le
départ, était resté indécis après 90 secondes. Ces deux sorties sont
`UNKNOWN`, jamais des exclusions.

Les outils et leurs rôles sont distincts :

- `transport_exception_star.py` : couverture des étoiles et moments du bord ;
- `transport_exception_capacity.py` : capacités examinées séparément ;
- `transport_exception_shared_edges.py` : arêtes communes aux deux extrémités
  pour une affectation, avec extraction d'un certificat entier ;
- `transport_exception_benders.py` : relèvement des certificats en (1) ;
- `transport_exception_completion.py` : modèle binaire direct, encore indécis.

Les deux certificats et les deux coupes sont dans
`data/codex_transport_exception_benders.json`. Leur contrôle entier,
sans appel à un solveur ni répétition de la campagne, se lance ainsi :

    python code/codex/transport_exception_benders.py --check

La suite utile est de simplifier ou renforcer ces inégalités pour éliminer
une étoile entière. Accumuler des affectations impossibles sans cette
généralisation ne sera pas présenté comme autant de cas C1 éliminés.

## 5. Piste distincte du pair : rubans longs

LAB a rapporté au message 470 (commit annoncé `da1282e`) l'exclusion des
deux rubans fermés propres de longueur six par des certificats de Farkas
exacts, après usage des deux vecteurs propres de valeur trois de leur
support. Avec sa borne spectrale préalable, les seules longueurs propres
fermées encore possibles sont 3,4,5. Il rapporte aussi qu'un segment
ouvert propre à cinq centres est impossible spectralement.

Ces résultats proviennent de la piste confiée à LAB, pas de la présente
campagne. Ils sont utilisés comme résultats rapportés, sans audit en double.
Les cycles de transport plus longs avec identifications ou arêtes
supplémentaires restent possibles à ce stade ; aucun de ces résultats
ne force un cycle de longueur quatre dans tout C1.
