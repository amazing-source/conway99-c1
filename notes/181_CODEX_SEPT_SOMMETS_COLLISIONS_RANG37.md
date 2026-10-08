# 181 — Sept sommets : un invariant supplémentaire et une nouvelle borne duale

8 octobre 2026. Suite aux familles proposées par LAB aux messages 198 et 200.

**Résultats.** Le recensement exact à sept sommets comporte 208 types et un seul nouvel
invariant en plus du nombre P de prismes. Il donne un comptage exact des représentants
« maison ou papillon moins une arête lointaine ». Après contrôle de leurs collisions,
on obtient la nouvelle inégalité du §5 pour la couche de norme huit de M.
Les quatre rangs 37,39,41,43 restent ouverts : cette note prépare l'attaque du rang 37.

## 1. Recensement exact et définition de H

La méthode d'extension des notes 175 et 179 donne, sur sept sommets, **208 types** respectant
les budgets de voisins communs λ≤1,μ≤2, puis **712 équations de rang 207**. Les seconds
membres sont affines en P. Le seul invariant nouveau peut être pris comme le nombre H
de copies du graphe suivant, appelé ici D :

- un sommet central v, adjacent aux quatre sommets a,b,c,d ;
- les arêtes ab et cd, formant deux triangles sur v ;
- deux autres sommets x,y avec les arêtes xa,xc,yb,yd,xy.

D a onze arêtes et degrés (4,3,3,3,3,3,3). C'est le **seul** type admissible sur sept sommets
ayant degré minimum au moins trois. Le recensement complet le vérifie directement.

Le programme utilise d'abord le compte brut h du type de code 1985025. La transformation
vers l'invariant géométrique H est

    H = 133056−6P−h/4,       h = 532224−24P−4H.

Le type de code 1972867 a pour nombre 8316−6P−4H. Sa positivité donne

    3P+2H≤4158.                                             (1)

Les matrices, solutions affines et conventions de codage sont conservées dans
`data/codex_seven_vertex_census.json`. Aucune valeur n'est choisie pour un invariant libre.

## 2. Deux familles exactes de représentants de norme huit

Considérons ψ=1_W−1_Y, avec W de taille cinq, Y de taille deux, disjoints. Sa somme vaut
trois et sa norme projetée vaut

    Q(ψ)=22−2(e(W)+e(Y)−e(W,Y)).

Sur cinq sommets les budgets locaux imposent e(W)≤6. Ainsi Q=8 exactement lorsque W
est une maison ou un papillon à six arêtes, Y est une arête, et W,Y sont anticomplets.
Une maison est un quadrangle avec un triangle sur une de ses arêtes ; un papillon est
constitué de deux triangles partageant leur sommet central.

Le recensement, avec les deux signes, donne exactement :

| Support positif | Nombre de représentants |
|---|---:|
| Papillon | 399168+12P+2H |
| Maison | 1713096−36P+12H |
| Total | 2112264−24P+14H |

LAB a retrouvé indépendamment le premier comptage à la main au message 202 : chaque
papillon a 96+κ+π arêtes lointaines, avec Σκ=H et Σπ=6P. Le second comptage est obtenu
par nos identités exactes d'extension.

Ces nombres comptent des représentants. Les paragraphes suivants traitent toutes les
collisions nécessaires avant leur addition à une borne sur b_4.

## 3. Différences propres +3 de masse sept

Pour une différence propre +3 dont la masse positive vaut S≤7, la borne S≥4h de la note 168
exclut toute coordonnée de valeur absolue deux. La différence est binaire. Si S≤6, les
supports sont deux prismes jumeaux, cas déjà classé. Si S=7, chaque support a degré
intérieur minimum trois, donc est une copie de D par le recensement du §1.

Dans une copie de D, chaque sommet non central a degré intérieur trois : l'équation
propre interdit donc toute arête vers le support opposé. Le centre a degré intérieur
quatre et doit avoir un voisin opposé. Il n'y a donc qu'une arête entre les deux supports,
celle reliant leurs centres.

Notons Ω le nombre de paires non ordonnées de copies de D ayant la même projection P_4.
Deux copies distinctes dans une telle classe sont disjointes. Sinon leur différence aurait
masse au plus six ; le seul cas possible exigerait deux prismes après suppression d'un
sommet de chacune, mais D privé d'un sommet possède sept ou huit arêtes, jamais neuf.

Les centres de toutes les copies d'une même classe sont donc deux à deux adjacents.
Ils forment une clique de taille au plus trois, car λ=1 interdit K4. En sommant sur les
classes de tailles m≤3, C(m,2)≤m donne

    Ω≤H.                                                    (2)

## 4. Audit des pertes de projection pour la nouvelle famille

La condition générale de collision reste

    (A−3I)(ψ−ψ′) = (Σψ−Σψ′)/9 ·1.

Deux orientations opposées de la famille ont des sommes de différence six : elles ne
coïncident pas. À sommes égales, la masse positive d'une différence est au plus sept,
donc seuls les prismes jumeaux et les paires de copies de D du §3 interviennent.

### 4.1. Contre les anciens représentants de norme huit

Les anciens représentants de somme trois sont les triples à une arête et les vecteurs
1_S−e_z avec |S|=4,e(S)=4,z lointain. Une collision contre un triple a masse au plus cinq
et est impossible. Contre 1_S−e_z, la masse vaut au plus six : une collision exige deux
prismes jumeaux Π,Π′.

Le nouveau support positif est alors Π\{z}, nécessairement une maison, et son arête
négative Y est une des neuf arêtes de Π′ ; l'ancien support S est Π′\Y. Pour une paire
non ordonnée de prismes, il y a deux choix du prisme positif, six choix de z, neuf choix
de Y et deux signes : **216 collisions**. Les autres anciennes familles de somme zéro
sont séparées par la congruence modulo neuf des sommes.

### 4.2. Entre nouveaux représentants : une différence prismatique

Écrivons deux représentants de même orientation W−Y et W′−Y′. Une différence de masse
six impose exactement un point de même signe commun. Les croisements de signes seraient
des coordonnées ±2 et sont déjà exclus.

- Si le point commun z est positif, les deux prismes sont (W\{z})∪Y′ et (W′\{z})∪Y.
  Le point z a deux voisins dans chacun : c'est un des trois troisièmes points des
  arêtes transversales des prismes. Dans chaque prisme, il y a quatre choix d'arête
  disjointe des deux voisins de z. Cela donne 4·4·2=32 paires de représentants signés
  pour chaque z, soit 96 par paire de prismes.
- Si z est négatif, il a exactement un voisin dans chaque prisme et appartient à
  l'ensemble des soixante sommets de degré extérieur un. Chacun détermine une paire
  de représentants et son opposée, soit 120 collisions signées par paire de prismes.

Avec le §4.1, la soustraction totale nécessaire est donc au plus

    (216+96+120)τ = 432τ.

### 4.3. Entre nouveaux représentants : une différence de masse sept

Les deux supports D sont disjoints et reliés seulement par l'arête des centres. Dans
chaque D, supprimer une arête dont les deux extrémités ont degré trois laisse une maison
ou un papillon à cinq sommets et six arêtes. Il y a sept telles arêtes ; elles évitent
toutes le centre, ce qui garantit l'anticomplétude requise avec l'autre support positif.
On compte 7·7 choix et leurs opposés : **98 collisions signées par paire**, soit 98Ω.

### 4.4. Contre les indicatrices négatives de six sommets

La différence des sommes vaut maintenant neuf. Une collision a la forme

    φ = 1_W−1_Y+1_Z,       |Z|=6,       Aφ=3φ+1.

Toute coordonnée négative restante aurait valeur −1 et au plus un autre voisin négatif,
alors que l'équation impose une somme de voisins −2. Donc Y⊂Z. Le lemme non négatif de
la note 179 implique que φ est l'indicatrice d'une grille R. Ainsi W⊂R, Y est extérieur
à R et Z=(R\W)∪Y.

Une grille contient neuf papillons et trente-six maisons sur cinq sommets. Le complément
S de chacun a quatre sommets et quatre arêtes. Chaque point de R possède une fibre de
dix voisins extérieurs, et tout point extérieur est dans une seule fibre.

Chaque fibre contient cinq arêtes (le voisinage d'un point est un appariement). Entre
les fibres de deux points adjacents de R il y a dix arêtes ; entre celles de deux points
non adjacents il y en a vingt. En effet le nombre de voisins d'un point d'une fibre dans
une autre vaut respectivement un ou deux, en comptant ses voisins communs avec le point
de R correspondant.

Les arêtes Y lointaines de W sont dans les quatre fibres sur S. Il y en a donc

    4·5 + 4·10 + 2·20 = 100.

Aucun point de R\W n'est lointain de W, puisqu'il a au plus trois voisins dans R\W et
degré quatre dans R. On a ainsi toutes les possibilités : (9+36)·100·2 = **9000 pertes
par grille**, dont 1800 pour les papillons et 7200 pour les maisons.

## 5. Nouvelle inégalité, et portée

Le nombre de classes de projection d'un ensemble de représentants est au moins son
cardinal moins le nombre de paires distinctes donnant la même image. Soustraire également
toutes les collisions avec les familles anciennes fournit donc une borne sûre, même si
plusieurs pertes sont redondantes dans des classes de multiplicité supérieure à deux.

En ajoutant le §2 à la borne corrigée de la note 179, on obtient

    b_4 ≥ 5939010 + 66P + 14H − 13572ρ − 480τ − 98Ω.        (3)

On doit conserver aussi l'ancienne borne. Par (1),(2), lorsque P=0 on a ρ=τ=0 et H≤2079,
donc (3) donne **b_4≥5764374**, contre 3826746 pour les familles précédentes dans ce cas.
Dans la relaxation limitée à sept sommets, le coin P=1386,ρ=231,H=0 permet encore aux
pertes d'absorber le gain. **Ajout : le recensement à neuf sommets de la note 182 exclut
ce coin, prouve P≤852 et ρ≤126, et porte la borne uniforme issue de (3) à b_4≥3371634.**

Le programme `code/codex/seven_support_collisions.py` vérifie explicitement les modèles
finis attachés à chaque paire de supports et la réduction modulo leur relation de noyau.
Il retrouve 216,32,2,98 et les 9000 pertes de grille. La classification exhaustive des cas
du §4 justifie leur emploi ; les modèles finis ne sont pas présentés comme des graphes
à 99 sommets réalisés.

## 6. Seuils exacts à viser pour le rang 37

`code/codex/rank37_dual_frontier.py` reconstruit les contraintes à q^84, avec a_7≤990,
b_1≤88, le budget commun des graines, toutes les bornes de six-ensembles et leurs pertes
couplées aux paramètres P,ρ. Il ne suppose pas b_5≥35000000 : la borne uniforme qui suit
de la note 179 n'est que **33224268**.

Pour chaque hypothèse supplémentaire sur b_3, on maximise b_4 exactement :

| Hypothèse sur b_3 | Maximum de b_4 dans cette relaxation |
|---:|---:|
| 24948, borne déjà prouvée | 218908933/13 ≈ 16839148,69 |
| 150000 | 1975616753/136 ≈ 14526593,77 |
| 300000 | 1585016753/136 ≈ 11654534,95 |
| 600000 | 803816753/136 ≈ 5910417,30 |
| 900000 | Infaisable, même sans nouvelle hypothèse sur b_4 |

Les certificats rationnels et les points atteignant les maxima sont archivés dans
`data/codex_rank37_dual_frontier.json`. Ces valeurs indiquent les cibles suffisantes pour
une exclusion ; elles ne sont pas des minorations déjà démontrées des couches du réseau.
L'inégalité (3), arrivée après ce tableau, n'est pas incluse dans ces maxima.

Les résultats à huit et neuf sommets sont développés séparément. Leurs comptages de
représentants ne seront pas ajoutés aux coefficients thêta avant contrôle de leurs collisions.
