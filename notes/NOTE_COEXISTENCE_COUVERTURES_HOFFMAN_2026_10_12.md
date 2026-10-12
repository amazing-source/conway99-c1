# Coexistence : couvertures doubles et transport des voisinages

12 octobre 2026. Suite aux échanges avec Dilan sur la nécessité de suivre
les obligations des voisinages jusqu'à leur coexistence dans un même graphe.
Cette note donne des conditions uniformes et leur exploitation effective.
La priorité bibliographique n'est pas revendiquée ; les preuves ci-dessous
permettent de réutiliser les conditions sans dépendre d'une heuristique.

## 1. Cadre et objet commun aux différents domaines

Soit une complétion hypothétique SRG(99,14,1,2) contenant une coclique C de
22 points. Ses 77 sommets extérieurs sont indexés par les blocs B_i d'un
design 2-(22,4,2), avec intersections de blocs au plus deux. Notons H sa
matrice d'incidence et D le graphe extérieur, de degré 10. Alors

    H D = 2 J - H,
    D² + D = 12 I + 2 J - Hᵀ H.

Un domaine admissible D_i contient les ensembles R de dix indices, sans i,
qui couvrent chaque point de B_i une fois et chaque autre point deux fois,
avec intersections au plus un entre tous les blocs de {i} ∪ R.

Définissons F comme la famille des ensembles K de onze blocs qui couvrent
chaque point de C exactement deux fois, deux blocs de K se rencontrant en
au plus un point. L'application R ↦ {i} ∪ R est une bijection entre D_i et
les éléments de F contenant i. On dispose donc d'UNE famille de couvertures,
dont les domaines sont les sections par un indice, et non de 77 objets
indépendants. En particulier, la somme des tailles des domaines vaut 11|F|.

## 2. Lemme des onze couvertures distinctes

Dans toute complétion, K_j = {j} ∪ N_D(j) appartient à F. Cela découle de
H(I+D)=2J. La linéarité des intersections découle de λ=1 et μ=2 : deux
voisins de j ont déjà j comme voisin commun, donc ne peuvent partager
deux points de C.

Les 77 ensembles K_j sont distincts. Sinon K_j=K_k avec j≠k implique que
j et k sont adjacents et ont neuf voisins communs extérieurs, impossible.

Par réciprocité de l'adjacence, i appartient exactement aux onze K_j dont
j appartient à K_i. D'où les conditions nécessaires uniformes

    |F| ≥ 77,             |D_i| ≥ 11 pour tout i.

Ce seuil exprime une obligation de coexistence. Un domaine non vide, ou même
de taille dix, ne suffit pas : les autres sommets doivent lui fournir onze
couvertures différentes.

## 3. Lemme de multiplicité pour une paire de blocs

Posons z_ij=|B_i ∩ B_j| et f_ij=|{K∈F : i,j∈K}|. Parmi les couvertures
effectivement réalisées, le nombre contenant i et j est

    |K_i ∩ K_j| = 2 - z_ij + D_ij   (i≠j).

En effet, si i,j sont adjacents, on compte les deux extrémités en plus
de leurs 1-z_ij voisins communs extérieurs ; sinon on compte leurs
2-z_ij voisins communs extérieurs. Les couvertures K_j étant distinctes,

    f_ij ≥ 2 - z_ij + D_ij,        donc f_ij ≥ 2 - z_ij.

Conséquences exploitables :

- si deux blocs se rencontrent en un point, ils doivent appartenir ensemble
  à au moins une couverture de F ;
- s'ils sont disjoints, ils doivent appartenir ensemble à au moins deux
  couvertures distinctes ;
- si f_ij = 2-z_ij, l'arête ij est interdite dans toute complétion ;
- si f_ij < 2-z_ij, le bord entier est exclu.

Exemple concret du premier bord asymétrique du précédent dossier :

    B_0 = {0,1,11,12},     B_5 = {0,3,10,19}.

Le domaine D_0 possède 25 candidats, mais aucun ne contient l'indice 5 :
f_0,5=0 alors que z_0,5=1. Si le graphe existait, 0 et 5 seraient donc
non adjacents et devraient avoir un deuxième voisin commun hors C. Le
voisinage fermé de ce sommet donnerait précisément une couverture contenant
0 et 5, qui n'existe pas. Cette contradiction utilise des candidats tous
localement admissibles, mais l'existence simultanée des autres sommets
impose une couverture supplémentaire.

## 4. Une résolution de dix lignes imposée par les voisins

Fixons i et son voisinage réel R_i. Pour chacun des dix j∈R_i, posons

    S_j = ({j} ∪ N_D(j)) \ {i}.

Les dix S_j sont des éléments distincts de D_i, distincts aussi de R_i.
En sommant leurs indicatrices, les équations de D donnent, pour k≠i,

    somme_j [k∈S_j] = (D²+D)_ik = 2-z_ik.

Il y a exactement 40 blocs rencontrant B_i en un point, 30 disjoints et
6 le rencontrant en deux points. Les dix lignes S_j doivent donc couvrir
les 40 premiers indices une fois et les 30 suivants deux fois ; les six
derniers ne sont jamais sélectionnés. Chacune des dix lignes choisit un
bloc dans chacun des quatre groupes de dix attachés aux points de B_i.

Cela donne un problème exact de résolution, plus fort que la seule
cardinalité des domaines : choisir dix lignes avec ces multiplicités.
Leur intersection deux à deux est au plus deux. Leur intersection avec
R_i est soit un indice de type z=1, soit deux indices de type z=0, les
seconds correspondant à un triangle extérieur passant par i.

Ainsi les onze lignes constituent aussi un code de poids constant dix
dont les intersections deux à deux sont au plus deux. Ce sont des
conditions nécessaires ; leur faisabilité seule n'est pas une complétion.

## 5. Conséquences établies sur les données déjà calculées

Sans relancer l'énumération des domaines des 36 designs :

- tous les 36 ont un domaine de taille inférieure à onze ; le même lemme
  explique donc leurs 36 exclusions ;
- huit ont même moins de 77 couvertures au total ;
- sur leurs 2 772 domaines, 2 771 présentent une violation de la condition
  de multiplicité d'une paire ; 1 918 de ces domaines ont pourtant au moins
  onze candidats. Le défaut porte donc souvent sur les obligations de
  recouvrement, même quand le nombre brut de possibilités semble suffisant.

Les domaines complets proviennent du paquet antérieur
`data/codex_hoffman_trades/proof_bundle.json`. Ce changement d'explication
n'est pas compté comme 36 nouvelles exclusions.

## 6. Exclusion d'une famille avec un bord réellement variable

Source : design `37c3bb63972f…` du paquet précédent. On conserve uniquement
les incidences des 18 points hors {3,4,5,6}. Les incidences de ces quatre
points sont des variables, soumises aux équations du design et aux
intersections de blocs au plus deux. Aucune borne sur le nombre d'échanges
depuis le design source n'est imposée.

Pour le sommet extérieur 10, l'énumération sur les seules incidences
conservées donne 333 couvertures potentielles. Un sélecteur de couverture
ne peut être vrai que si les incidences manquantes la rendent effectivement
valide. On impose au moins onze couvertures et les bornes f_10,j≥2-z_10,j.
Le système entier est INFEASIBLE en environ 3,35 secondes.

**Toutes les complétions C1 de ce bord partiel sont donc exclues.**
L'énumération séparée des designs compatibles avec le bord partiel termine
environ 24,84 secondes : 29 classes d'isomorphisme, dont 27 asymétriques et
deux de groupe d'ordre deux. Ce décompte décrit la portée du résultat ;
l'exclusion repose sur le système variable, pas sur 29 solveurs de graphes.

La normalisation ordonne les points libres et les colonnes ayant les mêmes
incidences conservées. Elle est sans perte pour une complétion complète :
ces renommages préservent le bord partiel, et toute complétion doit satisfaire
les bornes de couvertures à chacun de ses sommets. Aucun automorphisme du
graphe terminé n'est demandé.

Fichiers :

- `code/codex/hoffman_cover_capacity.py` et
  `code/codex/hoffman_coexistence_extensions.py` ;
- `data/codex_hoffman_extensions/capacity_37c3bb63972f_3-4-5-6_pairs/result.json` ;
- `data/codex_hoffman_extensions/family_37c3bb63972f_3-4-5-6_members.json`.

Une famille à trois points libres {3,4,5} a aussi été fermée, en ajoutant
symboliquement deux lignes à deux premières lignes compatibles. Elle
illustre le raffinement par une contradiction de coexistence, puis est
absorbée par la famille ci-dessus.

## 7. Cinq points libres : exclusion pendant la construction du bord

**Toute la famille à cinq points libres {3,4,5,6,7} est maintenant exclue.**
Seules les incidences des 17 autres points sont conservées. Les premières
formulations monolithiques avaient atteint leurs budgets avec UNKNOWN ;
la décomposition suivante permet de terminer exactement.

Un point effacé doit être incident à 14 blocs et rencontrer chaque point
conservé dans deux blocs. Deux blocs le contenant ne peuvent déjà partager
deux points conservés. L'énumérateur exact donne 4 297 incidences possibles
pour un point effacé, en environ 0,07 seconde. Pour reconstruire un design,
il faut choisir cinq de ces lignes, d'intersections mutuelles deux, en
respectant les multiplicités manquantes de chaque colonne et les
intersections finales de blocs au plus deux.

On dispose aussi des 1 173 couvertures potentielles du sommet extérieur 10,
énumérées sur les seules incidences conservées. Après le choix d'une ligne
de point effacé, une couverture reste possible si elle rencontre cette
ligne dans exactement deux blocs et reste linéaire. Tant que le bord n'est
pas terminé, cette famille est une SUR-FAMILLE de toutes les couvertures
qui pourront exister dans une extension.

Si cette sur-famille a moins de onze membres, ou si une multiplicité de
paire tombe sous 2-z, aucune extension du bord partiel n'est réalisable.
On élimine alors la branche entière, sans fabriquer ses designs complets.

Résultat du parcours exhaustif :

- 87 304 nœuds en 12,328 secondes ;
- 42 421 branches arrêtées par un certificat de coexistence : 137 après
  deux lignes de points choisies, 38 823 après trois et 3 461 après quatre ;
- aucun bord complet n'a besoin d'être construit ;
- les 42 421 certificats ont été rejoués arithmétiquement en 0,91 seconde,
  à partir des incidences choisies, sans réutiliser les mises à jour
  incrémentales des intersections du chercheur.

La couverture exhaustive repose sur le parcours fini documenté et sur
les deux énumérations d'entrée EXHAUSTED. Le rejeu vérifie séparément les
inégalités de chaque branche ; il ne constitue pas une formalisation Lean.
Les points effacés sont anonymes : choisir un ensemble de cinq lignes
représente toutes leurs permutations. Aucun automorphisme n'est imposé
à la complétion graphique.

Fichiers :

- `code/codex/hoffman_point_domain_completion.py --free 3,4,5,6,7 --cover-pruning` ;
- `code/codex/check_hoffman_cover_prunes.py` ;
- `data/codex_hoffman_extensions/point_prune_37c3bb63972f_3-4-5-6-7/result.json` ;
- le `certificate_replay.json` voisin et les domaines d'entrée dans
  `point_domains_37c3bb63972f_3-4-5-6-7/point_domain.json`.

Une comparaison qui construit les designs avant de les exclure a atteint
son budget après 3 106 classes, toutes exclues, sans finir le recensement.
Ce nombre n'est donc pas la cardinalité de la famille. Il illustre pourquoi
la propagation de la coexistence pendant la construction remplace utilement
l'accumulation de cas. Ces classes sont absorbées par l'exclusion exhaustive
du bord partiel ; on ne les ajoute pas comme des résultats indépendants.

L'extension à six points libres {3,4,5,6,7,8} utilise 45 213 lignes possibles
pour un point. Un premier parcours avec les seules obligations du sommet 10
n'a pas terminé à cinq minutes (1 869 824 nœuds, 941 860 coupures). Un essai
avec les obligations des sommets 0,10,15 s'arrête aussi sans épuisement
(1 441 792 nœuds, 848 313 coupures). Aucune exclusion exhaustive à six points
n'est déduite de ces deux parcours. Les premières branches sont trop
nombreuses : 5 665 choix pour le point effacé attaché à la colonne47.

**Obstacle suivant identifié.** Les couvertures qui subsistent dans la
sur-famille doivent elles-mêmes pouvoir réaliser la résolution de dix
lignes de la section4. Sur201 parents échantillonnés des coupures du premier
parcours, tous passent le filtre de multiplicité du parent, mais tous
échouent à cette résolution exacte. Le test parcourt5 766 nœuds cumulés,
sans atteindre son plafond, en environ1,48s avec la préparation des données.
Ce sondage n'est pas une couverture de la famille ; il justifie d'intégrer
la résolution plus tôt dans le générateur. La simple vérification de Hall
sur les projections biparties n'échoue que sur17 de ces201 parents.

L'outil `hoffman_resolution_filter.py` renvoie explicitement UNKNOWN si
son plafond de nœuds est atteint. Un témoin combinatoire positif de dix
lignes et son sous-ensemble impossible de neuf lignes servent à contrôler
le sens des résultats. Les201 cas et les statistiques sont conservés dans
`resolution_parent_probe.json`. Aucun nouveau parcours géant à six points
n'est lancé sans exploiter cette information.

## 8. Portée au-delà d'une coclique de Hoffman

Pour une coclique C quelconque de C1, on garde H(I+D)=2J. Les voisinages
fermés extérieurs sont donc encore des couvertures doubles linéaires de C,
mais leur taille devient 15-|B_i|. Un sommet a au plus sept voisins dans C,
car son voisinage est formé de sept arêtes disjointes. Les voisinages fermés
extérieurs restent donc distincts : une égalité donnerait au moins six
voisins communs à une paire adjacente.

Toute réalisation impose 99-|C| couvertures distinctes, et le sommet i
appartient à 15-|B_i| d'entre elles. La même borne de paire
f_ij≥2-z_ij+D_ij subsiste. Le transport vers un domaine de taille fixée
demande des précautions lorsque les |B_i| varient ; la formulation par la
famille commune de couvertures, elle, reste valable.

Le mécanisme de coexistence ne dépend donc pas intrinsèquement de α=22.
Le cas de Hoffman est celui où toutes les couvertures ont la même taille,
ce qui rend l'outil particulièrement concret et rapide à exploiter.

## 9. Aller au-delà d'une résolution possible : les triangles doivent coexister

Une résolution de dix lignes peut encore être faisable sans que ces lignes
puissent représenter les voisins d'un même sommet. On peut imposer davantage
de la géométrie commune, sans reconstruire le graphe entier.

Fixons un candidat central R. Quatre de ses indices rencontrent B_i en un
point ; les six autres lui sont disjoints. Puisque le voisinage d'un sommet
de C1 est constitué de sept arêtes disjointes, ces six derniers indices
doivent former trois paires : les trois triangles entièrement extérieurs
passant par i. Les deux blocs d'une telle paire doivent être disjoints.

Pour les lignes transportées S_j de la section4 :

- si j est un des quatre indices de type intersection1, R∩S_j={j} ;
- si {j,k} est une des trois paires de triangle, R∩S_j=R∩S_k={j,k},
  et S_j∩S_k={j,k} ;
- les lignes provenant de triangles différents ont intersection au plus un.
  En effet, leurs centres j,k sont non adjacents et partagent déjà i,
  donc |S_j∩S_k|=1-|B_j∩B_k|≤1.

On doit donc faire coexister un candidat central, un couplage parfait des
six indices, quatre lignes de type singleton et deux lignes pour chaque
paire du couplage. Les dix lignes doivent toujours résoudre les40 indices
de type intersection1 une fois et les30 disjoints deux fois. Les restrictions
ne demandent aucun choix arbitraire : tout graphe complet produirait l'un
des choix ainsi énumérés.

**Résultat sur le même bord à cinq points libres.** Les seuls17 points
conservés donnent1 173 candidats centraux. Le test épuise tous ces candidats
et les4 367 couplages qui passent ses filtres élémentaires. Les résolutions
exactes parcourent69 701 nœuds cumulés et sont toutes impossibles, sans
aucun plafond atteint, en environ15,6s. Aucune incidence des cinq points
libres n'est choisie pendant ce test.

Cela donne une seconde preuve, plus directement géométrique, de l'exclusion
de la même famille à cinq points libres. Les domaines projetés sont des
sur-domaines, donc oublier ces incidences ne peut créer une fausse exclusion.
La preuve porte sur les incidences conservées vers les77 sommets ; elle
n'affirme pas l'existence d'un sous-graphe universel interdit sur11 sommets.

Le sous-cas quatre points libres se termine en environ0,16s :333 candidats
centraux,237 couplages,316 nœuds de résolution. Les cas à cinq et quatre
points ne sont pas deux familles disjointes à additionner.

Outil et reproduction :

    python code/codex/hoffman_triangle_star.py --free 3,4,5,6,7

Le fichier `triangle_star_37c3bb63972f_3-4-5-6-7/result.json` et son domaine
projeté conservent les entrées et le résultat. L'outil commence par un
témoin combinatoire positif de cette relaxation et une variante impossible,
puis contrôle les multiplicités du témoin retourné. Ce témoin de test n'est
pas un graphe de Conway. Un plafond de recherche conduit à UNKNOWN.

Cette étape explique précisément pourquoi une résolution apparente ne
suffit pas : ses lignes doivent aussi réaliser les mêmes triangles, avec
les mêmes intersections. La prochaine extension doit conserver ce couplage
pendant le choix du bord, plutôt que reprendre les parcours à six points
avec les seules bornes de multiplicité.
