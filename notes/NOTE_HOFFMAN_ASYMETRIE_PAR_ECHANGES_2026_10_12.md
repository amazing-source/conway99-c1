# Bords de Hoffman asymétriques par échanges : construction et exclusions globales

12 octobre2026. Travail sur les mécanismes d'asymétrie et de reconstruction,
sans hypothèse de rang modulo7. L'objectif reste C1, soit les paramètres
(99,14,1,2). Aucun graphe de Conway n'est construit ici.

## 1. Résultat obtenu

À partir d'un design cyclique précis2-(22,4,2), on autorise l'échange
partiel de deux points dans certains blocs, en préservant les incidences
de paires. Un échange est **admissible** si le design résultant a77 blocs
distincts et si deux blocs se rencontrent toujours en au plus deux points.
Chaque design intermédiaire doit respecter ces conditions.

Le voisinage à distance au plus deux pour cette opération, à isomorphisme
près, comprend le design initial et **36 autres designs** :

- deux classes nouvelles à la première étape,34 à la seconde ;
-29 ont un groupe d'automorphismes trivial ; les sept autres ont un
  groupe d'ordre2. Le centre cyclique a un groupe d'ordre22 ;
-les36 nouveaux bords sont tous **incompatibles avec une complétion
  SRG(99,14,1,2)**, sans imposer de symétrie à cette complétion ;
-les36×77 domaines de voisinages ont été entièrement énumérés. Aucun
  n'est vide : leurs tailles vont de2 à29. La contradiction apparaît
  quand on exige leur compatibilité, et non dans un test d'une ligne seule ;
-des certificats utilisant2,3,4,5 domaines suffisent respectivement
  pour9,21,5,1 des designs. Ces domaines dépendent du **bord complet** :
  ce ne sont pas des obstructions universelles sur seulement2 à5 sommets.

Le centre était déjà exclu par la campagne cyclique du dossier Hoffman.
On ne répète pas ce calcul. Avec ce résultat acquis, toute cette boule
de37 classes est exclue comme design de bord de C1. Cette boule ne couvre
ni tous les designs2-(22,4,2), ni tous les graphes avec une coclique de22,
ni tout C1. Les mots « classes nouvelles » signifient nouvelles dans cette
exploration, sans revendication de nouveauté bibliographique.

## 2. Échange exact de deux points

Fixons deux points a,b. Soit L une sélection de blocs contenant a mais
pas b, et R une sélection de blocs contenant b mais pas a. Supposons
que chaque autre point apparaît autant dans les résidus des blocs de L
que dans ceux des blocs de R. Alors remplacer a par b dans L, et b par a
dans R, conserve les paramètres du design.

**Preuve.** La somme des incidences résiduelles impose |L|=|R|, car
chaque résidu a trois points. Les multiplicités de a,b sont donc conservées.
Une paire extérieure à{a,b} reste dans exactement les mêmes blocs.
La paire{a,b} n'est jamais modifiée. Pour une paire{a,x}, le nombre
d'occurrences perdues dans L est égal au nombre gagné dans R par hypothèse ;
idem pour{b,x}. Les tailles de blocs restent quatre. ∎

Dans un2-(22,4,2), il y a exactement12 blocs a-seul et12 blocs b-seul.
Les sélections sont donc traitées par deux listes de4096 sommes
d'incidences, réunies sur leur signature exacte. Chaque point résiduel
apparaît au plus deux fois : une écriture en base3 encode ces sommes sans
retenue. L'échange de tous les blocs est un simple renommage de a,b.

Les échanges de blocs sont des outils classiques de construction de
designs ; voir par exemple Crnković–Švob,
[Switching for 2-designs](https://arxiv.org/abs/2108.02529).
La preuve élémentaire ci-dessus précise exactement l'opération utilisée
ici, sans supposer qu'elle transporte une complétion graphique.

## 3. Un bord asymétrique explicite après seulement six blocs changés

Le centre est formé des translatés modulo22 des quatre blocs de base

    {0,1,3,7}, {0,2,7,16}, {0,3,8,12}, {0,1,11,12}.

Les trois premières orbites ont22 blocs, la dernière11. Dans les six
blocs suivants, échanger0 et5 :

| Avant | Après |
| --- | --- |
| 0,1,3,7 | 1,3,5,7 |
| 0,4,19,20 | 4,5,19,20 |
| 0,10,11,21 | 5,10,11,21 |
| 1,5,20,21 | 0,1,20,21 |
| 3,5,10,19 | 0,3,10,19 |
| 4,5,7,11 | 0,4,7,11 |

Les trois résidus de chaque côté partitionnent le même ensemble de neuf
points :{1,3,4,7,10,11,19,20,21}. Le lemme s'applique immédiatement.
Ils forment les lignes et colonnes de la grille

    1   3   7
    20  19  4
    21  10  11

Les trois lignes sont complétées par0, les trois colonnes par5 ; on
échange ces deux points d'attache. Ce motif fournit le même échange
valide dans tout2-design qui le contient, sous réserve de conserver
les conditions supplémentaires demandées aux blocs après modification.
L'intégralité des paramètres et l'absence d'intersection de taille3
ont aussi été contrôlées directement sur le design construit.

**Certificat d'asymétrie indépendant du calcul de groupe.** Sur les77
blocs, former le graphe d'intersection en exactement deux points. Colorer
chaque bloc par ses nombres de triangles et de quadrangles dans ce graphe.
Ce sont des invariants du design. On obtient22 couleurs de blocs.
Les multiensembles de couleurs des14 blocs incidents distinguent ensuite
**les22 points**. Tout automorphisme fixe donc chaque point, puis chaque
bloc, puisque les blocs sont distincts. Le groupe est trivial.

Le raffinement de couleurs dans le graphe d'incidence donne
23→44→99 classes, en séparant initialement points et blocs. Les vecteurs
d'invariants et toutes les couleurs sont conservés dans le certificat.
La même construction fournit une preuve intrinsèque pour chacun des29
designs asymétriques du recensement ; on ne dépend donc pas uniquement
de la sortie BLISS pour leur asymétrie.

## 4. Pourquoi ces bords ne se complètent pas

Notons B_i le bloc de quatre voisins du sommet i dans la coclique C.
Un voisinage R_i parmi les77 sommets hors C doit comporter dix sommets,
couvrir chaque point de B_i une fois et chaque autre point deux fois.
Il exclut i ; chaque bloc choisi rencontre B_i en au plus un point,
et deux blocs choisis se rencontrent en au plus un point.

Ces conditions définissent le domaine complet D_i. Pour deux lignes,
la compatibilité nécessaire et suffisante est

    [j dans R_i] = [i dans R_j],
    |R_i ∩ R_j| + |B_i ∩ B_j| = 2 − [j dans R_i].

Sélectionner un R_i dans chaque D_i en respectant ces deux égalités
pour toutes les paires donne exactement la complétion SRG, par les
équations de blocs du dossier Hoffman. Une valeur sans partenaire dans
un autre domaine ne peut appartenir à aucune complétion.

**Petit certificat du premier design asymétrique.** Les indices sont
ceux des77 blocs rangés par ordre lexicographique après l'échange.
Le bloc65={8,9,11,15} possède exactement huit voisinages candidats.
Les quatre domaines suivants les éliminent tous, sans même filtrer
les domaines des quatre autres sommets :

| Autre bloc | Ses points | Candidats de la ligne65 n'ayant aucun partenaire |
| ---: | --- | --- |
| 47 | 4,7,12,16 | 0,1,5 |
| 39 | 3,7,17,20 | 2,5 |
| 5 | 0,3,10,19 | 5,6,7 |
| 9 | 0,5,14,20 | 3,4 |

L'union des dernières colonnes est{0,…,7}. Toute complétion choisirait
nécessairement un de ces huit candidats, et échouerait à l'une des
égalités entre paires. C'est une exclusion du **graphe entier sous ce
bord fixé**, pas un échec de recherche locale à budget limité.

Les autres35 bords admettent des certificats du même type encore plus
courts. Aucun ne nécessite un solveur SAT, un calcul de rang modulo7,
une approximation numérique ou une hypothèse sur Aut du graphe terminé.

## 5. Couverture et vérifications pertinentes

Pour le centre cyclique, tout couple de points se transporte en{0,b}
par translation ; les21 valeurs de b couvrent donc les échanges initiaux.
Les deux représentants obtenus sont ensuite traités sur toutes leurs231
paires de points. Une seconde étape depuis une copie isomorphe du centre
ne donne rien au-delà de sa première étape, déjà couverte.

Le calcul traite483 paires de points. Il rencontre360 sélections
étiquetées non triviales :224 échouent au filtre d'intersections,
100 redonnent une classe déjà rencontrée,36 créent une nouvelle classe.
Aucun cap n'est atteint. Les renommages sont des isomorphismes de designs ;
aucun automorphisme n'est exigé des graphes que l'on cherche à compléter.

Les domaines sont produits par l'énumérateur C++ déjà documenté de LAB,
récupéré au commit `f2b6454`. Ses36×77 sorties sont toutes EXHAUSTED.
L'assemblage dure environ24,2s sur ce PC pour les36 bords. Une passe directe
a contrôlé les conditions de chaque voisinage enregistré et rejoué toutes
les suppressions à partir des ensembles de voisins, sans réutiliser les
tables de compatibilité du chercheur. La complétude des domaines repose
sur l'énumérateur exhaustif documenté ; le paquet n'est pas une preuve Lean
ou un certificat DRAT.

## 6. Fichiers et suite exploitable

Sources dans `code/codex/` :

- `prepare_hoffman_trade_inputs.py` récupère les graines archivées et
  l'énumérateur, sans refaire la campagne cyclique ;
- `hoffman_two_point_trades.py --seeds 1 --generations 2 --max-designs 100`
  construit et classe ce voisinage fini ;
- `complete_hoffman_trades.py` énumère les domaines et impose leur
  compatibilité ;
- `analyze_hoffman_trade_obstructions.py` rejoue les exclusions, réduit
  les certificats et fournit les preuves intrinsèques d'asymétrie.

Sorties : `data/codex_hoffman_trades/`. `proof_bundle.json` contient les36
designs, tous les domaines, leurs statuts, les suppressions et les
certificats courts dans un seul fichier d'environ1,1Mo.
`provenance.json` conserve les références et empreintes des entrées.

Pour reconstruire les domaines après récupération de l'énumérateur :

    g++ -O3 -std=c++17 data/codex_hoffman_trades/lab_rows22.cpp -o data/codex_hoffman_trades/rows22.exe
    python code/codex/complete_hoffman_trades.py
    python code/codex/analyze_hoffman_trade_obstructions.py

La classification emploie igraph/BLISS ; les certificats intrinsèques
et le rejeu arithmétique n'en dépendent pas. Sur ce PC, utiliser le Python
de `../c2_experimental/.venv/` et les dépendances `../c1-audit-deps/`.

**Conséquence de méthode.** L'asymétrie du design de bord peut être obtenue
par une petite modification exacte. Le couplage des voisinages ajoute
ensuite une obstruction effective, qui peut tenir en quelques domaines.
Une suite utile doit exploiter ces conflits pendant la construction du
bord ; agrandir simplement le catalogue d'asymétriques ne suffit pas.
Les anciens graphes243 et la reconstruction à deux prismes n'ont pas été
recalculés. Aucune prétention à résoudre tout le sous-cas α=22 n'est faite.
