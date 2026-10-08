# 203 — Exclusion générale du motif (2,2,1) et coupure globale

8 octobre 2026. Suite de la note 202. LAB a fourni au message 330
une table exhaustive dans le modèle canonique de colonnes. La preuve
ci-dessous traite **toutes les multiplicités entières de colonnes**,
y compris les modèles non canoniques. Aucun automorphisme du graphe
n'est supposé.

**Résultats pour r=rank₇(A−3I)≥37.**

- Sur une droite contenue dans six grilles, deux points portant chacun
  trois droites contenues dans six grilles obligent le troisième point
  à n'en porter qu'une : la droite initiale.
- Si n_h est le nombre de sommets portant exactement h droites
  contenues dans six grilles, alors

      3n₃ ≤ 2n₁+n₂,             donc n₃ ≤ 39.

Ces résultats ne supposent plus qu'un même indice de prisme fournisse
un centre universel aux trois apices, contrairement à la note 202.
Ils n'excluent ni toutes les droites dans six grilles, ni un rang entier.

## 1. Le motif à interdire

On conserve Θ={t₀,t₁,t₂}, ses six grilles G_k=Θ∪X_k, les soixante
points B et les cellules D^i_ab de quatre points de la note 202, §2.
Une droite ℓ_{i,k}={t_i}∪R_{i,k} est dite universelle si elle est
contenue dans six grilles. Les cinq grilles H^i_kj, j≠k, existent
alors, ainsi que G_k.

Choisissons deux indices de droites universelles supplémentaires
en t₀, deux en t₁ et un en t₂. Notons ces ensembles U₀,U₁,U₂,
de tailles (2,2,1). « Supplémentaire » signifie autre que Θ,
elle-même universelle aux trois points.

Pour chaque couleur i, toute paire d'indices rencontrant U_i
engendre une grille H^i_ab. Il y en a respectivement 9,9,5.
Avec les six G_k, on a donc **29 grilles distinctes**. Le Gram de
leurs indicatrices doit avoir rang au plus 19 modulo sept, par
la borne 56−r démontrée dans la note 202, §1.

Il suffit d'exclure les familles choisies : d'autres grilles éventuelles
ne peuvent pas faire diminuer le rang de ce Gram principal.

## 2. Les quatre-vingt-dix noms de colonnes

Un point de B choisit un voisin dans chacun des six prismes ; la
couleur de ce voisin est l'apex auquel il est adjacent. Chaque couleur
apparaît exactement deux fois, par μ(b,t_i)=2.

On dispose donc de 90 mots w de longueur six sur {0,1,2}, chacun
contenant deux fois chaque couleur. Notons m_w le nombre de points
de B portant le mot w. Ce sont des **entiers non négatifs**. Aucune
hypothèse n'impose qu'ils valent zéro ou un au départ.

### Marges de deux coordonnées

Pour a≠b et des couleurs i,j,

    Σ_(w_a=i, w_b=j) m_w = 4 si i=j, et 8 sinon.        (1)

En effet, les deux barreaux concernés contiennent deux sommets chacun.
Chaque paire de sommets de prismes distincts a deux voisins communs.
Un apex est commun si et seulement si i=j ; tous les autres voisins
communs appartiennent à B. Un point de B est compté une seule fois.

En particulier, les quinze cellules D^i_ab de chaque couleur ont
chacune quatre points et partitionnent B. On a m_w≤4 et Σ_w m_w=60.

### Marges supplémentaires imposées par le serrage

Si {a,b} rencontre U_i, la grille H^i_ab existe. Pour k∉{a,b} et j≠i,

    Σ_(w_a=w_b=i, w_k=j) m_w = 2.                      (2)

Les deux sommets de R_{j,k} sont extérieurs à cette grille et n'ont
aucun voisin dans sa partie {t_i}∪R_{i,a}∪R_{i,b}. Chacun doit donc
avoir exactement un voisin dans D^i_ab. Ces voisins sont distincts,
car un point de B a exactement un voisin dans X_k. Cela prouve (2).

### Bornes binaires provenant des intersections

Chaque mot définit trois duades d_i={k:w_k=i}. Si au moins deux des
grilles H^i_{d_i} existent, alors

    m_w ≤ 1.                                          (3)

Leur intersection est exactement l'ensemble des points portant w :
les deux couleurs fixent quatre coordonnées, et la troisième couleur
fixe nécessairement les deux restantes. Par la note 202, §2, deux
telles grilles d'apices différents ont au plus un point commun.
Pour les autres mots, on conserve seulement m_w≤4.

Les équations (1),(2) et les bornes (3) sont des conditions nécessaires.
Nous n'imposons ni les bits de lignes des prismes, ni toutes les arêtes
dans B. Leur absence affaiblit le modèle ; elle ne peut invalider une
exclusion exhaustive des solutions du modèle.

## 3. Les sept cas et leur vérification exacte

Les 15·15·6=1350 placements de (U₀,U₁,U₂) se répartissent en sept
orbites par permutation des six prismes et échange des deux premiers
apices. Ce sont des renommages du problème, pas des automorphismes
imposés à un graphe. Le programme reconstruit ces orbites et vérifie
leur couverture complète.

| U₀ ; U₁ ; U₂ | Taille de l'orbite | Variables libres | Affectations examinées | Solutions entières | Rangs des Grams modulo 7 |
|---|---:|---:|---:|---:|---|
| 01 ; 01 ; 0 | 30 | 5 | 200 | 9 | 24 |
| 01 ; 01 ; 2 | 60 | 5 | 500 | 6 | 23 |
| 01 ; 02 ; 0 | 120 | 5 | 500 | 6 | 24 |
| 01 ; 02 ; 1 | 240 | 5 | 500 | 6 | 24 |
| 01 ; 02 ; 3 | 360 | 5 | 3125 | 6 | 24 |
| 01 ; 23 ; 0 | 360 | 5 | 200 | 6 | 24 |
| 01 ; 23 ; 4 | 180 | 6 | 6250 | 8 | 24 |
| **Total** | **1350** | — | **11275** | **47** | **≥23** |

L'élimination rationnelle exprime les 84 ou 85 autres multiplicités
en fonction de coordonnées libres prises parmi les m_w eux-mêmes.
Pour chaque expression, l'archive contient la combinaison rationnelle
des équations initiales qui la prouve. Le vérificateur recalcule cette
combinaison coefficient par coefficient. Ainsi, toute solution véritable
est nécessairement comprise dans l'énumération des coordonnées libres.

Les coordonnées libres sont parcourues dans leurs bornes entières,
de zéro à un ou de zéro à quatre. Les expressions déterminent toutes
les autres. Le programme rejette seulement les défauts d'intégralité,
les violations de bornes ou d'équations initiales. Il obtient exactement
les 47 solutions indiquées. Les première et dernière orbites montrent
pourquoi il fallait traiter davantage que les six modèles canoniques.

À partir de chaque solution, le Gram des 29 grilles est entièrement
déterminé. Pour deux grilles H à des apices différents, les entrées
inconnues sont précisément les m_w ; toutes les autres entrées sont
9,3,1 ou 0 comme dans la note 202.

Pour chacun des 47 Grams, un **mineur d'ordre vingt non nul modulo
sept** est archivé et vérifié. Les rangs complets sont 23 ou 24.
Ils contredisent tous le plafond 19. Le motif (2,2,1) est donc exclu
pour r≥37. Le motif (2,2,2), et tous ses placements, l'est a fortiori.

## 4. Une inégalité globale sur les sommets denses

Posons h(v)=nombre de droites par v contenues dans six grilles.
On a h(v)≤3. En effet, quatre sommets universels du graphe Ξ_v sur
sept droites imposeraient au moins 6+4·3=18 arêtes, alors que la
note 108 donne e(Ξ_v)≤17.

Sur une droite contenue dans six grilles, les trois h(v) sont dans
{1,2,3}. Le motif exclu interdit les multisets (3,3,2) et (3,3,3).
Si deux points ont h=3, le troisième a donc h=1.

Sur chaque telle droite, notons a_h le nombre de ses points de type h.
Les huit types restants satisfont

    a₃ ≤ 2a₁ + a₂/2.                                  (4)

Les cas à égalité avec a₃>0 sont (3,3,1) et (3,2,2).
En sommant (4) sur toutes les droites contenues dans six grilles,
un sommet de type h est compté h fois. Avec n_h=|{v:h(v)=h}| :

    3n₃ ≤ 2n₁ + (2n₂)/2 = 2n₁+n₂.                    (5)

Comme n₀+n₁+n₂+n₃=99,

    3n₃ ≤ 2n₁+n₂ ≤ 2(99−n₃),

d'où **n₃≤39**. La forme (5), plus précise, est celle à intégrer
aux modèles globaux de profils. Cette intégration et les nouvelles
bornes sur ρ ou τ ne sont pas calculées dans cette note.

## 5. Reproduction et portée

    python code/codex/grid_kernel_rank_dense_apices.py --verify-only

L'archive est `data/codex_grid_kernel_rank_dense_apices.json.gz`.
Elle contient les sept représentants, les certificats de réduction
linéaire, les 47 vecteurs de multiplicités et les mineurs.

La commande sans option régénère les données avec une élimination
rationnelle exacte. La vérification relit les combinaisons et refait
l'énumération entière ; aucun solveur, calcul flottant ou modèle de
Petersen n'intervient. Les deux commandes ont été exécutées avec succès.

Le résultat interdit un voisinage dense précis et donne (5). Il laisse
notamment possibles, au niveau de ces seules contraintes, une droite
dans six grilles avec moins de centres universels aux apices. Il ne
constitue pas une exclusion du rang 37 ni des rangs 39,41,43.
