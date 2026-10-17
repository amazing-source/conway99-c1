# 238 — Contrainte locale et densité des écarts dans les cycles de transport

9 octobre 2026. L'utilisateur demande de poursuivre le raccord du lemme 237
à C1. Cette note remplace son hypothèse portant sur un cycle entier par une
contrainte obligatoire sur chaque fenêtre courte, puis en tire un comptage
sur tous les cycles longs. Les identifications de rôles sont prises en compte.

## 1. Résultats et limites

Dans une fenêtre de transport à w centres, les rôles sont

    c_1,...,c_w ; a_1,...,a_(w+1) ; b_1,...,b_(w+1),

avec les triangles `(c_i,a_i,a_(i+1))` et `(c_i,b_i,b_(i+1))`.
Une arête **latérale supplémentaire** est une paire de rôles adjacents
dans le graphe, dont au moins un rôle est a ou b, et qui n'est pas une
des arêtes de ces triangles. Les arêtes entre centres sont libres.

Deux conclusions sont obtenues :

1. Une fenêtre à **sept centres** dont les rôles sont distincts contient
   au moins une arête latérale supplémentaire.
2. Une fenêtre à **huit centres** dont les rôles sont distincts en contient
   au moins deux, quelles que soient les arêtes entre centres.

La preuve utilise une petite classification locale avec témoins entiers :
sept vecteurs suffisent pour le premier filtrage spectral, 61 pour le
second. Les contradictions de moments extérieurs sont également entières.
Les statuts numériques d'un solveur ne servent pas de preuve.

Pour les fenêtres où des rôles sont identifiés, un argument direct du §5
donne encore au moins deux paires de rôles latérales supplémentaires.
Ces paires peuvent représenter la même arête physique du graphe ; cette
distinction est conservée dans le comptage.

Ainsi, si C est un cycle de transport de longueur m≥10 et E(C) le nombre
de telles paires de rôles apparaissant dans au moins une fenêtre de huit
centres de C, alors

    E(C) ≥ ceil(m/4).                                      (D)

Cette restriction vaut même lorsque des sommets du graphe se répètent
dans le ruban déroulé. Elle n'exclut pas tous les cycles longs : aucune
borne supérieure contradictoire sur E(C) n'est établie. Les cycles courts,
les 174 noyaux et les rangs globaux restent ouverts.

## 2. Fenêtres sans arête latérale supplémentaire

Les centres consécutifs ont déjà les deux voisins communs a_(i+1),b_(i+1).
Ils ne peuvent être adjacents. Sur six centres, seules dix arêtes entre
centres restent donc à choisir : 2^10=1024 ensembles, avant les contraintes.

Pour chaque matrice A du support, on impose les nécessités exactes

    (A²+A)_uv ≤ 2  pour u≠v,
    27I−9A+J ≥ 0,
    44I+11A−2J ≥ 0.

900 ensembles violent la première condition. Les 122 suivants ont un
témoin entier v avec `vᵀGv<0` pour l'un des deux Grams ; seulement sept
vecteurs distincts sont nécessaires pour les couvrir. Deux ensembles restent :

    A6 = {15,24,26,35},
    B6 = {14,16,25,36},

où ij désigne l'arête c_i c_j.

### A6 ne possède pas de bord possible

Le support a vingt sommets, donc 79 sommets extérieurs. Pour un masque
b de voisinage extérieur dans ce support, les conditions utilisées sont

    |b|≤14,
    bA ≤ 2·1−b,
    b_u b_v=0 dès que (2−A−A²)_uv=0.

Tous les masques satisfaisant ces conditions sont énumérés, y compris
le masque vide. Aucun test spectral de masque n'est nécessaire ici.
Leurs multiplicités x doivent vérifier

    Σ x_b = 79,
    Σ x_b b_u = 14−deg_A(u),
    Σ x_b b_u b_v = (2−A−A²)_uv.

Un certificat entier y donne un coefficient non négatif sur chaque
masque, alors que la combinaison des seconds membres vaut −3. Ainsi
A6 est impossible. **Toute fenêtre à six centres sans arête latérale
supplémentaire doit avoir exactement B6 comme graphe de centres.**

### Deux fenêtres B6 se recouvrant donnent une contradiction à sept centres

Leurs restrictions imposent

    P7 = {14,16,25,27,36,47}.

La seule arête entre centres encore indéterminée serait 17. Elle est
impossible : elle donnerait c_1 comme troisième voisin commun de c_6
et c_7. Pour le support à 23 sommets avec P7, le premier Gram possède
le témoin entier suivant, dans l'ordre a_1..a_8,b_1..b_8,c_1..c_7 :

    v = (-17,-29,-26,-10,10,26,29,17,
         -17,-29,-26,-10,10,26,29,17,
         -22,-23,-16,0,16,23,22),
    vᵀ(27I−9A+J)v = −4482.

Une fenêtre à sept centres sans arête latérale supplémentaire est donc
impossible lorsque ses rôles sont distincts.

## 3. Une seule arête latérale : six types nécessaires à sept centres

On autorise exactement une arête latérale, et toujours n'importe quel
ensemble d'arêtes entre centres. Le renversement de la fenêtre et
l'échange global des deux côtés réduisent les positions de cette arête
à 53 représentants. Il y a 1089 graphes de centres satisfaisant déjà
les budgets locaux sans cette arête ; ajouter l'arête ne peut réparer
un budget déjà dépassé.

Après ajout de l'arête, les mêmes deux Grams éliminent toutes les
possibilités restantes sauf quatorze. Les témoins sont entiers ; un
ensemble de 61 vecteurs couvre les exclusions spectrales.
Les équations de moments extérieurs excluent huit des quatorze supports,
par des certificats entiers portant sur tous leurs masques combinatoires.

Les six formes qui restent comme **conditions nécessaires**, sans
affirmation de prolongement, ont toutes le graphe de centres P7. Leur
seule arête latérale est, à symétrie près,

    a_2 a_6,  a_2 a_7,  a_3 a_6,
    a_2 b_6,  a_2 b_7,  a_3 b_6.

En ne retenant que les colonnes et en rétablissant le renversement,
les positions possibles sont

    {2,6}, {3,7}, {2,7}, {3,6}.                         (P)

En particulier, une unique arête supplémentaire entre un centre et
un côté ne suffit jamais sur une telle fenêtre.

## 4. Le recouvrement exclut une seule arête sur huit centres

Supposons une fenêtre à huit centres, avec des rôles distincts, ayant
au plus une arête latérale supplémentaire. Ses deux fenêtres de sept
centres doivent chacune en contenir une, par le §2. C'est donc la même
arête dans les deux, et sa paire de colonnes appartient à l'intersection
de (P) et de sa translation d'une unité. Cette intersection est

    { {3,7} }.

Les deux graphes P7 imposent en outre

    C8 = {14,16,25,27,36,47,38,58},

avec la seule possibilité d'ajouter 18. À échange des côtés près, l'arête
latérale est `a_3 a_7` ou `a_3 b_7`. Il reste donc quatre supports sur
26 sommets. Chacun possède un témoin entier négatif pour `27I−9A+J`.
Les valeurs enregistrées sont −108, −1404, −108 et −1458.

Cela prouve le deuxième résultat : **huit centres et des rôles distincts
imposent au moins deux arêtes latérales supplémentaires**.

## 5. Que deviennent les identifications ?

On compte ici des **paires de rôles**. Si deux rôles ont le même sommet
image dans le graphe, les adjacences prescrites de l'un sont également
des adjacences de l'autre. Dès qu'une paire ainsi obtenue n'est pas une
arête prescrite du ruban, elle est une paire latérale supplémentaire.

Toute identification dans une fenêtre de transport de huit centres
en impose au moins deux :

- **Deux centres identifiés.** Leurs ensembles de quatre voisins latéraux
  prescrits diffèrent par au moins deux rôles. Ceux-ci donnent deux paires
  supplémentaires pour l'autre rôle de centre.
- **Un centre et un rôle latéral identifiés.** Un centre a quatre voisins
  latéraux prescrits, tandis qu'un rôle latéral en a au plus deux.
  Au moins deux de ces quatre adjacences sont donc supplémentaires.
- **Deux rôles latéraux identifiés.** Ils ne sont ni dans la même colonne
  (les paires transportées sont des non-arêtes), ni dans deux colonnes
  consécutives. Dans ce dernier cas, une identification sur un même côté
  créerait une boucle ; une identification croisée confondrait les deux
  triangles au centre commun et rendrait une paire transportée adjacente.
  Pour deux colonnes non consécutives, les ensembles des centres voisins
  prescrits sont disjoints et non vides. En transférant une adjacence de
  chaque rôle vers l'autre, on obtient deux paires latérales supplémentaires.

Ces adjacences existent bien dans le graphe, puisque leurs modèles sont
des arêtes prescrites. Elles sont deux paires distinctes de rôles, même
si leurs images peuvent être une seule arête physique après identification.
Ainsi chaque fenêtre de huit centres porte au moins deux telles paires,
qu'il y ait des identifications ou non.

## 6. Une restriction sur chaque cycle long, sans hypothèse d'injectivité

Dérouler un cycle de transport de longueur m≥10 en m centres et m
paires latérales, en respectant son éventuelle fermeture tordue.
Considérer ses m fenêtres cycliques de huit centres.

Chaque fenêtre porte au moins deux paires latérales supplémentaires,
par les §4–5. Une paire de rôles contenant un centre appartient à au
plus huit fenêtres, puisque ce rôle de centre appartient à huit fenêtres.
Deux rôles latéraux appartiennent chacun à neuf fenêtres. S'ils sont
dans des colonnes distinctes, leurs ensembles de fenêtres sont deux
intervalles cycliques propres distincts, donc leur intersection a taille
au plus huit. S'ils sont dans la même colonne, ils ne sont pas adjacents
et ne peuvent contribuer.

Pour m≥10, aucune arête prescrite du cycle située hors de la fenêtre
ne devient une arête entre ses deux colonnes extrêmes : la fenêtre ne
contient que neuf des m colonnes. Les paires supplémentaires comptées
localement sont donc bien supplémentaires dans le ruban cyclique déroulé.

En double comptant les incidences fenêtre/paire supplémentaire,

    2m ≤ 8 E(C),

ce qui donne (D). Si L est la somme des longueurs des cycles de longueur
au moins dix du graphe de transport, on obtient aussi

    Σ_(C long) E(C) ≥ Σ_(C long) ceil(|C|/4) ≥ ceil(L/4).

Il s'agit d'une contrainte sur les adjacences **aux positions de transport**.
On ne peut pas identifier cette somme au nombre d'arêtes du graphe C1,
ni compter chaque répétition comme une nouvelle arête physique.

## 7. Certificats et frontière de la preuve

Le programme `code/codex/ribbon_window_obstructions.py` construit le
support, parcourt les ensembles d'arêtes permis et produit les témoins.
Le fichier `data/codex_ribbon_window_obstructions.json` contient les
68 vecteurs réutilisés, les références de couverture, les certificats
de moments et les quatre témoins finaux. Le contrôle exact, sans appel
à un solveur ni calcul de valeurs propres, est :

    python code/codex/ribbon_window_obstructions.py --check

Les pilotes intermédiaires sont conservés dans
`data/codex_ribbon7_one_lateral_pilot.json` et
`data/codex_ribbon7_one_lateral_extensions.json` avec leur portée.
La preuve repose sur les témoins entiers du fichier final, pas sur
la seule décision spectrale flottante du pilote.

Le passage du lemme 237 à une règle sur chaque fenêtre, puis à (D),
est acquis. Pour conclure contre C1, il manque une restriction incompatible
sur ces adjacences supplémentaires, ou un argument excluant les assemblages
des fenêtres restantes. Ni le simple budget de degré quatorze ni le nombre
total de 693 arêtes ne fournissent cette contradiction, car une arête peut
apparaître à plusieurs positions de transport. Aucun des 174 noyaux n'est
déclaré clos sur la base de ce seul comptage.
