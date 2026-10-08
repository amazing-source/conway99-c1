# 221 — Un noyau obligatoire de 14 sommets, sans séparation des rangs

9 octobre 2026. Nouveau point de départ choisi après la demande de
changer de route (note 220). Aucun rang modulo sept, aucune hypothèse
P=0, S=0, de généricité ou d'automorphisme n'intervient.

**Résultat :** tout SRG(99,14,1,2) contient un noyau enraciné d'une
liste de 373 types ; 63 de ces types sont impossibles par positivité
réelle, avec certificats entiers. Il reste 310 types à cette étape.
La note 222 en exclut ensuite 136 supplémentaires par les contraintes
simultanées des 85 sommets extérieurs, laissant 174 types à prolonger.
Ce sont des sous-graphes induits de 14 sommets, pas une liste de
graphes complets ni une estimation du coût de leurs prolongements.

## 1. Le motif de départ est obligatoire

Le théorème de Makhnev (1988, théorème 2, rappelé dans la note 94)
exclut un SRG(99,14,1,2) dans lequel deux triangles ne sont jamais
reliés par exactement deux arêtes. Tout candidat contient donc

    triangles 012 et 345, arêtes transversales 03 et 14,
    sans aucune autre arête entre ces deux triangles.

Notons S cet ensemble de six sommets et A_S son adjacency. Les
degrés dans S sont (3,3,2,3,3,2).

Ce recours à un motif obligatoire est essentiel : il couvre aussi
les candidats sans prisme complet et tous les rangs encore ouverts.
On ne suppose pas l'existence d'une grille ni d'une coclique de taille 22.

## 2. Tous les effectifs autour de S sont déterminés

Pour un sommet extérieur x, son masque est N(x)∩S. Il contient au
plus un point par triangle, donc a taille au plus deux. Pour une paire
u,v de S, le nombre de sommets extérieurs qui la couvrent vaut

    δ_uv = 2 − (A_S)_uv − (A_S²)_uv.

Ces déficits imposent exactement les effectifs suivants. Les formules
de la troisième colonne valent dans la famille SRG(1+k²/2,k,1,2)
dès qu'un tel motif S y est présent.

| Masque dans S | Effectif à k=14 | Effectif général |
|---|---:|---:|
| vide | 33 | k²/2 − 6k + 19 |
| {0},{1},{3},{4}, chacun | 9 | k−5 |
| {2},{5}, chacun | 8 | k−6 |
| {0,3},{1,4}, chacun | 1 | 1 |
| {2,3},{2,4},{0,5},{1,5}, chacun | 1 | 1 |
| {2,5} | 2 | 2 |

Tous les autres masques ont effectif zéro.

**Preuve.** Les déficits des paires donnent les sept lignes de
masques doubles, avec multiplicité deux pour {2,5}. Chaque sommet
de S a ensuite k−deg_S(u) voisins extérieurs ; en retirant les
contributions doubles, on obtient les six effectifs simples. Enfin
la soustraction au nombre total de sommets donne l'effectif vide.
Le programme vérifie ces calculs par le système linéaire complet :
14 masques admissibles, 14 colonnes indépendantes, solution unique.

Soit D l'ensemble des huit sommets doubles, ordonnés par leurs masques

    6:03, 7:14, 8:23, 9:24, 10:05, 11:15, 12:25, 13:25.

Le noyau H=S∪D a donc 14 sommets. Toutes les arêtes touchant S sont
fixées. Seules des arêtes intérieures à D restent à choisir.

## 3. Catalogue exhaustif et exclusions exactes

Dans tout sous-graphe induit d'un SRG(99,14,1,2), les voisins communs
déjà présents satisfont, pour u≠v,

    (A_H²)_uv ≤ 2 − (A_H)_uv.                       (1)

Parmi les 28 paires de D, sept ne peuvent même pas être ajoutées
isolément au noyau de base : elles violent (1). Il reste 21 arêtes
optionnelles. L'ajout d'autres arêtes ne peut réparer une violation
de (1), ce qui justifie l'élagage de l'énumération.

L'examen exhaustif prend 9168 nœuds de récursion et produit 2299
graphes étiquetés. Histogramme selon le nombre d'arêtes dans D :

    0:1, 1:21, 2:156, 3:514, 4:790, 5:565, 6:206, 7:42, 8:4.

Le motif S a quatre automorphismes, et les deux sommets de masque
25 peuvent être échangés. Ce groupe d'ordre huit agit sur les 21
arêtes optionnelles. Le quotient donne **373 orbites**. L'ensemble
des orbites reconstruit exactement les 2299 graphes : ni représentant
manquant, ni identification supposant une symétrie du graphe complet.
S reste distingué ; ce catalogue n'est pas présenté comme un quotient
maximal par tous les isomorphismes des graphes à 14 sommets.

Le spectre réel d'un candidat à 99 sommets vaut 14¹,3⁵⁴,(−4)⁴⁴.
Ses projecteurs donnent deux conditions nécessaires sur chaque H :

    Q₋ = 27I₁₄ − 9A_H + J₁₄ = 63 E₋₄[H] ⪰ 0,
    Q₊ = 44I₁₄ + 11A_H − 2J₁₄ = 77 E₃[H] ⪰ 0.     (2)

Une élimination symétrique **rationnelle exacte**, incluant le cas
singulier, applique (2) aux 373 représentants : 63 sont exclus,
310 passent ces deux conditions. Pour chacun des 63, un vecteur
entier z est archivé avec zᵀQ₋z<0 ou zᵀQ₊z<0. Le calcul flottant
ne sert qu'à proposer un vecteur court ; son produit quadratique
est ensuite calculé en entiers.

Exemple : pour le représentant de code binaire 1673 dans le fichier,

    z=(-33,-35,-33,-35,-35,-29,-28,-28,-20,-16,-8,-15,-26,-8),
    zᵀ Q₋ z = −1490.

**Couverture après exclusions.** Tout candidat à 99 sommets possède
un motif S par §1. Ses huit sommets doubles sont imposés par §2,
et son noyau figure dans le catalogue par (1). Il satisfait (2),
donc appartient à l'un des 310 types restants. Exclure tous leurs
prolongements suffit à exclure C1, sans séparer les rangs modulo sept.

## 4. Le problème de prolongement est explicite

Notons C les 33 sommets de masque vide, et U_i les six classes de
masque {i}, de tailles (9,9,8,9,9,8). Il reste à placer les arêtes
entre D, C et les U_i, puis à l'intérieur de C et des U_i.

Pour x∈C, compter les chemins de longueur deux de x vers S donne

    2 deg_D(x) + Σ_i deg_Ui(x) = 12,
    deg_C(x) = 2 + deg_D(x),                         (3)
    2 ≤ deg_C(x) ≤ 8.

La borne supérieure vient de deg_D(x)≤6 dans la première égalité.
Pour le sommet y_i∈D, le même compte et le degré total 14 donnent

    deg_C(y_i) = b_i + deg_D(y_i),
    b = (8,8,7,7,7,7,6,6).                          (4)

**Détail.** Si y a masque {u,v}, le nombre total d'incidences vers S
de ses voisins extérieurs à S vaut 10−deg_S(u)−deg_S(v). Chaque
voisin dans D en contribue deux, chaque voisin dans U une, et chaque
voisin dans C zéro. Retirer ces incidences des douze voisins restant
à placer donne (4).

En sommant (3) et (4), on obtient

    e(C) = 61 + e(D).                               (5)

Le noyau détermine encore davantage : pour y∈D et i∈S,

    deg_Ui(y) = 2 − A_H(y,i) − (A_H²)(y,i).          (6)

Tous les voisins communs restants de y et i se trouvent dans U_i,
car les sommets doubles sont déjà tous dans H.

**Cible suivante.** Démontrer que ces classes de tailles fixes ne
peuvent satisfaire simultanément leurs degrés, les λ/μ de toutes
les paires et les conditions (2) sur leurs prolongements ; ou réduire
cette question à une liste plus petite effectivement traitable.
Les égalités (3)–(6) seules ne sont pas déclarées contradictoires.

Un premier modèle nécessaire peut utiliser les masques des 85
sommets restants sur H : chaque masque contient zéro ou un sommet
de S, avec huit bits libres sur D. Il y a au plus 7·2⁸=1792 masques
avant filtrage. Leurs multiplicités doivent totaliser les degrés et
voisinages communs résiduels de H. Une contradiction à ce niveau
exclurait uniformément tous les prolongements du noyau concerné.
La faisabilité ne construirait pas le graphe : les arêtes entre les
85 sommets resteraient à placer.

## 5. Contrôle, fichiers et limites

Le graphe tordu à 243 sommets sert de contrôle positif : on y trouve
un vrai motif S, puis ses huit sommets doubles. Leur noyau figure
dans le catalogue (représentant 0 pour le témoin choisi). Les
effectifs sont ceux de §2 à k=22 : |C|=129, tailles simples 16/17,
huit sommets doubles. Le contrôle vérifie aussi les analogues de
(3)–(5) : deg_C(x)=10+deg_D(x) et e(C)=705+e(D).
Il ne demande évidemment pas au 243 de satisfaire les projecteurs
spécifiques à 99.

- Programme : `code/codex/twisted_prism_core.py`.
- Catalogue, effectifs et certificats : `data/codex_twisted_prism_core.json`.
- Relecture :

      python code/codex/twisted_prism_core.py --out data/codex_twisted_prism_core.json --verify-only

La relecture recalcule la couverture, vérifie les 63 produits
quadratiques en entiers et les 310 positivités en rationnels. Un
certificat dont le vecteur a été remplacé par zéro a été rejeté.
LAB a également retrouvé indépendamment les 373 types et les 63 exclusions
par projecteurs, avant consultation de ce code et de ses données
(message du pont 408). Toutes les 63 exclusions proviennent de Q₋ ;
Q₊ n'en ajoute aucune à cette étape.

Cette réduction n'élimine aucun rang entier et ne constitue pas
63/373 d'une preuve de non-existence : les noyaux peuvent se
chevaucher dans un même graphe, et leurs prolongements ont des coûts
inconnus. Elle fournit une couverture locale obligatoire, valable
pour tout C1, et des familles de noyaux interdites à tous les rangs.
