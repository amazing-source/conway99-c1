# 202 — Rang modulo sept : un motif de grilles denses est exclu

8 octobre 2026. La borne sur le réseau complémentaire a été proposée
par LAP et relayée par LAB aux messages 325 et 326. La présente note
en vérifie la justification et fournit une obstruction locale nouvelle
dans ce programme, avec un certificat fini. **Aucun rang entier n'est
exclu et une droite dans six grilles n'est pas exclue en général.**

Le calcul ne suppose pas que les soixante noms proviennent du modèle
canonique de Petersen ou d'un total de synthèmes. Il ne suppose aucune
symétrie du graphe.

## 1. La borne sur les matrices de produits scalaires

Posons r=rank₇(A−3I), et

    L = Z⁹⁹ ∩ E_{−4},
    K⁺ = Z⁹⁹ ∩ (E₃ ⊕ ⟨1⟩) = L^⊥ ∩ Z⁹⁹.

Ces réseaux sont primitifs dans Z⁹⁹ et ont des formes discriminantes
opposées. La note 101 donne pour L une partie sept-primaire élémentaire
de rang r−1. Il en va donc de même pour K⁺, qui a rang 55.
La forme sur K⁺/7K⁺ a un radical de dimension r−1 ; son quotient
non dégénéré a dimension

    55−(r−1)=56−r.

Par conséquent, toute famille de vecteurs entiers de K⁺ a une matrice
de Gram de rang au plus 56−r modulo sept. En particulier :

| r | 37 | 39 | 41 | 43 |
|---|---:|---:|---:|---:|
| Rang maximal du Gram | 19 | 17 | 15 | 13 |

L'indicatrice d'une grille appartient à K⁺ : son voisinage vaut quatre
à l'intérieur et un à l'extérieur, donc (A−3I)1_G=1. Son Gram est la
matrice des intersections des grilles, avec entrées 9,3,1,0.

Les différences de prismes d'un même faisceau sont 1_G−1_G′. Les
ajouter à une famille contenant déjà ces grilles n'augmente pas son
rang. Les différences de prismes hors grille ne sont pas couvertes
par cette observation.

## 2. Les grilles autour d'une droite dans six grilles

Écrivons Θ={t₀,t₁,t₂}, et G_k=Θ∪X_k, k=0,…,5. Les X_k sont six
prismes disjoints et anticomplets. Notons R_{i,k} les deux points de
X_k voisins de t_i, et ℓ_{i,k}={t_i}∪R_{i,k} leur droite.

Les soixante autres points forment B. Chaque b∈B a un voisin dans
chaque X_k ; exactement deux de ces six voisins sont de chaque couleur
i. Pour une paire {a,b} d'indices de prismes, posons

    D^i_ab = {z∈B : ses voisins dans X_a et X_b ont couleur i}.

Cet ensemble a quatre points : chacune des quatre paires de sommets
de R_{i,a}×R_{i,b} a, en plus de t_i, exactement un voisin commun
dans B. Ces quatre voisins communs sont distincts. Pour i fixé, les
quinze D^i_ab partitionnent B.

Si les droites ℓ_{i,a},ℓ_{i,b} engendrent une grille, elle est
nécessairement

    H^i_ab = {t_i} ∪ R_{i,a} ∪ R_{i,b} ∪ D^i_ab.

Son D^i_ab induit un carré. Les intersections sont alors :

- |G_k∩H^i_ab|=3 si k∈{a,b}, et 1 sinon ;
- pour deux H distinctes au même apex : 3 si leurs paires se coupent,
  et 1 sinon ;
- pour deux apices différents : l'intersection est contenue dans B,
  vaut zéro si les paires d'indices se coupent, et vaut zéro ou un sinon.

Pour la dernière assertion, une intersection de trois points de grilles
distinctes serait une droite. Or D^i_ab, carré induit, ne contient
aucune droite. On utilise ici le fait classique déjà employé dans le
programme : deux grilles distinctes se coupent en zéro point, un point
ou une droite. Le serrage le redonne : deux points non adjacents communs
forcent leurs deux voisins communs, puis les apices et toute la grille.

## 3. Le motif exclu

Appelons **universelle en t_i** une droite ℓ_{i,k} contenue dans six
grilles. Les sept droites de t_i sont Θ et les six ℓ_{i,k}. Ainsi,
ℓ_{i,k} est universelle exactement lorsque toutes les cinq H^i_kj,
j≠k, existent ; G_k est sa sixième grille.

**Proposition.** Si r≥37, il est impossible d'avoir simultanément :

1. toutes les H^i_0k pour i=0,1,2 et k=1,…,5 ;
2. toutes les H⁰_1k pour k=2,…,5 ;
3. H¹_12.

Par permutation des indices, la troisième grille peut être n'importe
quelle H¹_1k ou H²_1k avec k∉{0,1}.

La première famille, avec les six G_k, comprend 21 grilles : son Gram
entièrement connu a rang **18** modulo sept. Elle est donc déjà
impossible pour r≥39. Il reste à traiter r=37.

### Réduction des intersections inconnues

Considérons une grille supplémentaire H^i_1k et un autre apex j.
Ses intersections avec H^j_01 et H^j_0k sont vides. Il reste trois
grilles H^j_0l, où l∉{0,1,k}.

Le serrage de H^i_1k impose que chacun des deux points de R_{j,0}
ait exactement un voisin dans D^i_1k : il n'a aucun voisin dans
la partie connue {t_i}∪R_{i,1}∪R_{i,k}. Ces deux voisins sont
distincts, puisque chaque point de B a un seul voisin dans X₀.

On obtient donc exactement deux points de D^i_1k ayant couleur j
dans le prisme 0. Leur deuxième prisme de couleur j est un des trois
l précédents. Par la partition en D^j_0l et les intersections binaires,

    Σ_(l∉{0,1,k}) |H^i_1k ∩ H^j_0l| = 2.

Le triplet d'intersections est une permutation de `(0,1,1)`.
Pour les deux autres apices, cela donne **neuf possibilités**.
Toutes les intersections entre les cinq grilles supplémentaires
sont connues : elles partagent le même indice 1, donc valent trois
au même apex et zéro à des apices différents.

### Vérification exhaustive avec certificats

On ajoute successivement H⁰_12,H⁰_13,H⁰_14,H⁰_15,H¹_12.
Une branche dont un Gram principal a rang supérieur à 19 est rejetée ;
ses extensions ne peuvent pas diminuer ce rang.

| Nombre de grilles ajoutées | Rangs des prolongements testés | Branches de rang ≤19 |
|---|---|---:|
| 1 | 19 : 9 | 9 |
| 2 | 19 : 20 ; 20 : 61 | 20 |
| 3 | 19 : 12 ; 20 : 20 ; 21 : 148 | 12 |
| 4 | 19 : 12 ; 21 : 96 | 12 |
| 5 | 20 : 6 ; 21 : 102 | **0** |

Chaque branche rejetée possède un mineur d'ordre vingt non nul
modulo sept, archivé avec ses indices de lignes, ses indices de
colonnes et son déterminant. Les **433 certificats** couvrent
exactement les **9⁵=59049** choix initiaux. Les conditions entre noms
non utilisées ne peuvent qu'en supprimer davantage. Aucun solveur
ni calcul flottant n'intervient. Cela prouve la proposition.

## 4. Conséquences et limites

Si le barreau du prisme 0 est universel aux trois apices et celui du
prisme 1 l'est en t₀, alors aux deux autres apices les droites
ℓ_{1,1},ℓ_{2,1} sont dans **exactement deux grilles** : G₁ et H^i_01.
Toutes leurs autres grilles possibles sont interdites par la proposition.

En particulier, trois points de Θ portant chacun au moins trois droites
universelles ne peuvent pas partager un même indice de prisme qui
fournit une droite universelle aux trois points. Il suffit même que
deux points portent trois telles droites et le troisième les deux
droites communes Θ et ℓ_{i,0}.

En effet, au deuxième point ayant un troisième centre universel c≠0,
une H¹_1k avec k∉{0,1} existe : prendre k=c si c≠1, ou n'importe
quel k∉{0,1} si c=1. C'est précisément la grille interdite.

Ce résultat ne suppose pas les intersections du modèle canonique de
Petersen. Il laisse ouverts les autres arrangements de centres
universels, notamment lorsque les indices supplémentaires aux trois
apices n'ont aucun indice commun. Il ne donne pas encore de majoration
globale de ρ, de τ, ni d'exclusion du rang 37.

## 5. Reproduction

    python code/codex/grid_kernel_rank_obstruction.py --verify-only

Le fichier `data/codex_grid_kernel_rank_obstruction.json.gz` contient
les matrices sous forme de leurs choix d'intersections et les mineurs.
Le vérificateur reconstruit les Grams, contrôle les déterminants et
la couverture exhaustive de l'arbre. La commande sans option régénère
l'archive. Les deux commandes ont été exécutées avec succès.
