# 226 — Un lemme de masse neuf et une borne complète sans prisme

9 octobre 2026. Exploration demandée par LAB, messages 425 et 428, dans
le cadre de la priorité aux nouveaux lemmes. Aucun audit antérieur relancé.

**Résultats nouveaux :** une fonction propre entière de valeur propre +3
et de masse positive neuf est nécessairement binaire. Les nouveaux canaux
de masse sept sont bornés par 1420Ω. On obtient également des formes
linéaires couvrant les masses huit et neuf d'une sous-collection sans
changement de somme, sous l'hypothèse P=0.

**Conséquence et limite :** tous les canaux de collision de cette
sous-collection peuvent maintenant être incorporés dans un même comptage.
Les plafonds trouvés sont trop larges pour en tirer « rang 37 implique
P>0 ». Le résultat nouveau est le lemme et la couverture des canaux,
pas une exclusion de rang ou de noyau.

## 1. Collection et couverture des canaux

On conserve les représentants binaires ψ=1_W−1_Y de norme projetée huit,
de formes (1,1),(2,2),(3,3),(4,4), et les deux signes de
(3,0),(4,1),(5,2),(6,3). Pour (6,3), on impose e(W)≤8.

Leurs sommes sont 0,+3,−3. La condition de collision

    (A−3I)(ψ−ψ′) = (Σψ−Σψ′)/9 ·1

impose donc des sommes égales. Il n'y a aucun canal de changement de
somme à traiter. Une différence non nulle a masse positive entre six
et neuf. Sous P=0, la masse six est impossible (note 168). Les seules
masses restantes sont sept, huit et neuf.

Cela ne couvre pas la collection plus grande contenant (6,0),(7,1),(9,0).
Les changements de somme de cette dernière restent ouverts.

## 2. Lemme : masse neuf implique coefficients −1,0,1

Soit δ une fonction propre entière non nulle, Aδ=3δ, de masse positive
neuf. La borne S≥4h de la note 168 impose |δ_v|≤2.

Deux sommets positifs de poids deux sont impossibles. S'ils ne sont pas
adjacents, chacun exige au moins six unités de masse positive parmi les
cinq restantes. S'ils sont adjacents, chacun exige encore quatre unités
dans ces cinq : leur voisinage commun a masse au moins trois. Or λ=1
autorise au plus un voisin commun, de poids au plus deux.

Supposons donc un unique poids deux. Les sept autres points positifs ont
poids un. Le sommet de poids deux en voit au moins six.

- S'il voit les sept, le graphe sur ses voisins est un appariement : une
  des sept feuilles n'a aucun voisin positif autre que le centre. Sa
  somme de voisins positifs vaut deux, insuffisante pour Aδ=3δ.
- S'il en voit six, le septième point est non adjacent au centre. Par
  μ=2, il ne peut voir que deux de ces six feuilles, encore insuffisant.

La même preuve vaut pour les poids négatifs. Ainsi

    δ = 1_U−1_V,  |U|=|V|=9,  U∩V=∅.

Les deux graphes induits ont degré minimum trois. Ce lemme n'utilise
ni P=0, ni le rang modulo sept.

## 3. Masse sept : compléter les canaux croisés

Les supports sont les deux copies de D de la note 181, reliées uniquement
par l'arête de leurs centres. Notons Ω le nombre de paires non ordonnées
de copies de D ayant même projection. On utilise Ω≤H déjà établi.

Les nouveaux canaux, deux signes inclus, sont :

| Canal | Borne par paire de D |
|---|---:|
| (6,3) contre (4,1) | 296 |
| (6,3) contre (5,2) | 1124 |
| Total nouveau | 1420 |

Le premier canal n'a aucun point commun extérieur à U∪V. Le second
en a un. Les 85 points extérieurs ont degré commun 0,1,2 vers U et V,
avec effectifs 17,61,7. Leurs coûts maximaux sont respectivement 0,12,56,
d'où 61·12+7·56=1124.

La borne existante pour (6,3) interne est 3612Ω. Les anciens canaux
contribuent 98Ω (note 181) et 272Ω (note 185). Donc

    C7 ≤ 5402Ω ≤ 5402H.                              (1)

Les nombres désignent des paires non ordonnées de représentants ; les
deux signes sont inclus, avec la convention des notes précédentes.

## 4. Masse huit : une forme linéaire complète sous P=0

La classification de la note 183 fournit trois cubiques à huit points,
trois types à treize arêtes, un type à quatorze arêtes et le moulin
pondéré (centre de poids deux, six feuilles de poids un). Le type à
quatorze arêtes contient un prisme et disparaît sous P=0.

Seuls interviennent (6,3) interne, (6,3) contre (5,2), et (4,4) interne.
Le premier a un point commun extérieur aux supports de la différence ;
les deux autres n'en ont aucun. Les coordonnées de poids deux de la
différence sont incluses explicitement dans la génération des deux
représentants, avec signes opposés.

Pour une paire de supports cubiques ou de moulins, il n'y a aucune arête
entre les supports. Si d(x) est le degré pondéré commun d'un point
extérieur, les moments sont

    Σd(x)=88,  Σd(x)²=128.

Le nombre de points extérieurs vaut 99−|U|−|V|. Pour les supports à
treize arêtes, les deux arêtes entre supports apparient leurs sommets
de degré quatre ; les moments deviennent

    nombre=83,  Σd(x)=84,  Σd(x)²=110.

Ces identités suivent de A²=12I−A+2J et A(u−v)=3(u−v).
Le programme énumère les profils admissibles d'un unique point extérieur,
calcule leurs coûts, puis maximise ces coûts sous les trois moments.
Ce dernier calcul énumère les sommets d'un polytope d'au plus cinq
variables en arithmétique rationnelle, sans approximation numérique.
Les profils ne sont pas affirmés prolongeables en un graphe complet.

Les classes de supports de même projection sont disjointes et de taille
au plus cinq, par la note 183. Si B_ij borne le coût d'une paire de types
i,j, chacun des supports a au plus quatre partenaires. Par conséquent

    C8 ≤ Σ_i 2 max_j(B_ij) C_i.

On obtient la forme suivante, déjà complète pour les canaux précisés :

    C8 ≤ 1872 C2022000 +1840 C5683824 +3088 C5691760
         +3512 C127305925 +3616 C128354469 +4448 C245715219
         +2592·3465.                                  (2)

Les 3465 moulins sont comptés avec leur centre pondéré, qui est unique.
Les coûts B_ij, plus fins que cette enveloppe, figurent dans le JSON.
Le terme constant vaut 8 981 280 ; c'est une majoration, absolument pas
une quantité de collisions dont l'existence aurait été démontrée.

## 5. Masse neuf : borne linéaire par positivité et intersections

Seul le canal (6,3) interne peut atteindre la masse neuf. D'après le
lemme, les supports U,V sont binaires, disjoints, de neuf points.
Sous P=0, le catalogue existant donne 39 types de degré minimum trois,
sans prisme, ayant 14,15 ou 16 arêtes (respectivement 11,22,6 types).

Chaque partition U=W⊔Y′ doit avoir |W|=6, |Y′|=3,
e(W)∈{7,8}, e(Y′)∈{2,3}. Notons a_U,b_U,c_U,d_U les nombres de partitions
de types A=(7,2), B=(7,3), C=(8,2), D=(8,3).

La norme huit impose e(W)+e(Y)−e(W,Y)=10. Ainsi A peut seulement être
apparié à D ; B et C ne peuvent pas être appariés entre eux. Une borne
sur les paires compatibles, deux signes inclus, est donc

    2 w_U w_V,   w_U=a_U/k+b_U+c_U+k d_U,   k≥1.

Le choix enregistré est k=4 pour e=14,15 et k=2 pour e=16. Ce choix
est une commodité de majoration, pas un optimum revendiqué.

Dans une classe de même projection, tous les U ont le même nombre e
d'arêtes. En posant E3 le projecteur orthogonal sur l'espace propre +3,

    <E3 1_U,E3 1_V> = |U∩V|−α,
    α=(459−22e)/77 ∈ {151/77,129/77,107/77}.

Sous P=0, deux supports distincts ont intersection de taille au plus
deux : une intersection plus grande donnerait une différence propre de
masse au plus six, donc une paire de prismes ou le vecteur nul.

Soit ℓ_U le nombre de suppressions de deux sommets de U laissant une
copie de D. À suppression fixée, une intersection deux peut donner au
plus deux autres supports V, puisque la classe de copies de D a taille
au plus trois (note 181).

Écrivons W_e=max w_U sur les types à e arêtes. La positivité de
||Σ_U w_U E3 1_U||² donne, après omission du terme d'intersection un
(coefficient 1−α<0),

    C9 ≤ Σ_U [(9−α)/α · w_U²
              +2(2−α)/α · ℓ_U w_U W_e].              (3)

En effet la somme w_Uw_V sur les paires d'intersection deux est au plus
Σ_U ℓ_U w_U W_e. Regrouper (3) par type, puis arrondir chaque coefficient
au-dessus à un entier, fournit la forme linéaire du fichier
`data/codex_mass9_prismfree_collision_bound.json`.

**Amélioration pour e=14.** Deux supports d'une même classe sont
disjoints : une intersection de un ou deux points laisserait des
supports de masse huit ou sept, avec au plus onze ou neuf arêtes,
insuffisamment pour le degré minimum trois. Les autres intersections
ont déjà été exclues. Chacun des supports a un unique sommet de degré
quatre ; les arêtes entre supports relient ces sommets deux à deux.
Ils forment une clique, donc la classe a taille au plus trois. La perte
de cette composante est ainsi au plus 2Σ_U w_U². Le JSON utilise cette
amélioration à la place du coefficient (9−α)/α pour e=14.

## 6. Résultat de l'exploration et obstacle précis

Pour la collection du §1, sous P=0, on dispose maintenant de

    nombre d'images distinctes ≥ R−C7−C8−C9.

Aucun canal manquant n'est implicitement mis à zéro. Les changements
de somme ont été évités en changeant la collection et son numérateur R.

LAB estime, dans sa relaxation du rang 37, que cette collection laisse
une marge d'environ 3,84 millions avant collisions (message 428,
calcul flottant). Notre première forme C9 seule atteint un plafond
d'environ 193,5 millions dans la relaxation d'ordre neuf, avant
l'amélioration e=14 ci-dessus. LAB rapporte
149,2 millions après ajout de son ordre dix (message 431). Ce sont des
diagnostics numériques, pas des bornes exactes ni des collisions réalisées.

Après l'amélioration des classes à e=14, le diagnostic enregistré d'ordre
neuf descend à environ 151,1 millions, encore très éloigné de la cible.

Cette forme ne permet donc pas l'exclusion visée. Le défaut identifié
est le coût imputé à tous les supports comme s'ils avaient des partenaires.
Il faut contraindre les paires de même projection, ou obtenir un autre
lemme réduisant leurs classes. Ajouter mécaniquement les mêmes équations
de recensement ne règle pas cette difficulté. Aucune certification
supplémentaire d'un optimum aussi éloigné n'est demandée.

Pour e=14, les supports U,V ont chacun un unique sommet de degré quatre
et sont reliés par l'arête entre ces deux sommets. Leurs classes sont
disjointes, et ces sommets forment une clique : la taille de classe est
au plus trois. Cette structure est exploitée dans l'amélioration du §5 ;
elle n'est pas annoncée comme une exclusion.

## 7. Fichiers

- `code/codex/mass9_prismfree_collision_bound.py` et son JSON :
  coefficients exacts de (3), plus diagnostic LP explicitement flottant.
- `code/codex/small_collision_new_channels.py` et
  `data/codex_small_collision_new_channels.json` : nouveaux canaux de
  masse sept, coûts par paire de types de masse huit et moments exacts.

Les catalogues et résultats des notes 181,183,185 sont utilisés comme
acquis. Les calculs présents portent sur des canaux nouveaux, sans
relance de leurs campagnes de vérification.
