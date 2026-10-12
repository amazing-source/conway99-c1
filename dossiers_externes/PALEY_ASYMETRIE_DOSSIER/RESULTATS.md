# Résultats — passer de Paley à des SRG asymétriques

## 1. Ce qui a été fait

Cette campagne applique à Paley la question posée par les travaux à 243 :
peut-on conserver un bord exact d’un graphe symétrique, reconstruire le reste et obtenir une
réalisation asymétrique des mêmes paramètres ?

La réponse expérimentale est **oui à 25 sommets**, avec un recensement terminé et des témoins
dont l’asymétrie se démontre par une petite configuration intrinsèque.

La collection de quinze SRG(25,12,5,6) est connue depuis les travaux de Paulus et Rozenfeld
en 1973. Deux de ces graphes sont asymétriques. La présente campagne ne revendique ni ces
graphes ni cette classification historique. Elle reconstruit les quinze classes depuis le
même bord de Paley, sans utiliser de graphe cible dans le générateur, et mesure les obstacles
de plusieurs représentations plus restrictives. Les sources primaires figurent dans
`sources/PROVENANCE.md`.

Les derniers commits lus dans le dépôt C1 comprennent les notes 165–166, puis la correction
de jauge de la note 167 et les journaux au commit
`1bbc7fdc5dde795d944bad0f2d9ae0af17e27c24`. La restriction erronée « tous les recollements
d’un arbre sont identités » n’est pas réutilisée. Aucun groupe d’automorphismes du graphe
terminé n’est imposé à notre reconstruction.

## 2. Un bord conservé, pas un graphe cible caché

Étiqueter les sommets de Paley(25) par \(5r+c\), avec \(r,c\in\mathbb F_5\), et déclarer deux
positions adjacentes lorsqu’elles partagent une ligne, une colonne ou la valeur de \(r+c\).
Le vérificateur retrouve indépendamment ce graphe par les carrés non nuls de
\(\mathbb F_5[\alpha]/(\alpha^2-2)\).

Fixons
\[
S=\{4,8,12,16,20\}.
\]
C’est la clique des cinq positions où \(r+c=4\). Nous conservons sa matrice interne et
toutes ses connexions aux vingt sommets \(F\) restants. Dans l’entrée remise au moteur,
**toutes les arêtes \(F-F\) ont été effacées**.

Le générateur n’a donc pas accès aux arêtes du graphe asymétrique, ni aux quinze graphes du
catalogue. Il travaille seulement sur un bord extrait de Paley et les paramètres SRG.

Chaque sommet de \(F\) a deux voisins dans \(S\). Chacune des dix paires de \(S\) étiquette
exactement deux sommets de \(F\). Si \(Y\) est cette matrice d’incidence \(5\times20\), alors
\[
YY^{\mathsf T}=6I_5+2J_5.
\]

Les inconnues sont les 190 paires de \(F\), ou, de façon équivalente, vingt lignes binaires.
La matrice symétrique \(D\) de la région reconstruite doit vérifier
\[
D\mathbf1=10\mathbf1,\qquad YD=4J_{5,20},\qquad
D^2+D=6I_{20}+6J_{20}-Y^{\mathsf T}Y,
\]
avec diagonale nulle. **Ces conditions sont exactes et suffisantes**, pas seulement
nécessaires : les autres blocs de l’identité SRG sont déjà fixés correctement.

Chaque ligne possède exactement 1 718 candidats après les contraintes linéaires et de degré.
Deux lignes candidates sont compatibles si leur adjacency réciproque coïncide et si leur
nombre de voisins communs est exactement celui requis. Le programme résout ce problème
fini de compatibilité, sans OR-Tools ni bibliothèque SAT.

## 3. Recensement terminé

Le moteur, avec sa graine d’ordre de visite 3, termine en
\[
67\,130\text{ nœuds},\qquad 3\,983\text{ feuilles représentatives}.
\]
Les réductions d’échanges entre sommets encore interchangeables sont accompagnées de poids.
Le total, après rétablissement de ces poids, est
\[
\boxed{1\,999\,872\text{ complétions étiquetées}.}
\]

Les 3 983 feuilles ne sont pas annoncées comme des orbites toutes distinctes :
l’élimination de symétries est partielle. Chaque matrice produite est vérifiée puis reliée
à son représentant du catalogue par une permutation explicite. On retrouve les quinze classes.

| N° McKay | \(|Aut|\) | \(K_5\) | Complétions étiquetées de ce bord |
|---:|---:|---:|---:|
| 1 | 72 | 15 | 25 600 |
| 2 — Paley | 600 | 15 | 3 072 |
| 3 | 72 | 3 | 5 120 |
| 4 | 6 | 3 | 61 440 |
| 5 | 2 | 3 | 184 320 |
| 6 | 6 | 3 | 61 440 |
| 7 — asymétrique | 1 | 3 | 368 640 |
| 8 | 3 | 3 | 122 880 |
| 9 | 2 | 3 | 184 320 |
| 10 | 6 | 3 | 61 440 |
| 11 | 6 | 3 | 61 440 |
| 12 | 2 | 3 | 184 320 |
| 13 — asymétrique | 1 | 3 | 368 640 |
| 14 | 3 | 3 | 122 880 |
| 15 | 2 | 3 | 184 320 |

Un contrôle combinatoire indépendant vérifie, pour chaque classe,
\[
N_{\mathrm{étiqueté}}
=\frac{\#K_5\cdot5!\cdot2^{10}}{|Aut(G)|}.
\]
Les quinze résultats concordent exactement. Les ordres d’automorphismes ont été recomptés
par énumération d’isomorphismes, pas copiés pour classifier les sorties.

Une répétition complète avec les programmes livrés a repris la génération, l’énumération,
la vérification, les correspondances et les tests annexes. Le moteur principal a pris moins
d’une seconde dans cette session ; l’ensemble mesuré après compilation initiale, incluant
classification et tests annexes, environ 65 secondes. Ce sont des mesures de cette machine,
pas une prédiction pour 99 ou 243 sommets.

## 4. Une transformation explicite : 37 arêtes retirées, 37 ajoutées

Le fichier `data/paley25_to_asymmetric.adj` est obtenu en changeant 74 paires :
37 arêtes de Paley disparaissent et 37 autres apparaissent. Toutes les équations SRG restent
vraies, sur les 300 paires. Les cinq lignes de \(S\) restent inchangées ; une sixième ligne,
celle du sommet 6, est aussi inchangée dans ce témoin.

Ce témoin appartient à la classe asymétrique n° 13. La liste des arêtes modifiées est dans
`certificats/explicit_transformation.json`.

Le nombre 74 est minimal **parmi les complétions asymétriques respectant ce bord fixé**.
Il a été obtenu en examinant toutes les feuilles asymétriques et tous les \(2^{10}\)
échanges des deux sommets de même profil sur \(S\). Aucune minimalité sans cette restriction
de bord n’est revendiquée.

### Où disparaît exactement la dernière symétrie ?

Le graphe final contient exactement trois cliques de taille cinq, deux à deux disjointes :
\[
\begin{aligned}
X&=\{4,8,12,16,20\},\\
Y&=\{1,2,5,6,10\},\\
Z&=\{11,14,18,23,24\}.
\end{aligned}
\]
Leur réunion \(U\), de taille quinze, est **intrinsèque** : tout automorphisme doit la préserver,
puisqu’elle est la réunion de toutes les \(K_5\).

Les arêtes entre \(X,Y\), puis entre \(X,Z\), forment un \(C_{10}\).
Entre \(Y,Z\), elles forment \(C_4\sqcup C_6\).
Ainsi \(X\) est la seule des trois cliques reliée aux deux autres par un \(C_{10}\) : elle est
reconnaissable dans le graphe, et non marquée arbitrairement.

Le graphe induit sur \(U\) possède exactement deux automorphismes. Ce décompte se vérifie
par seulement \(2\cdot5!=240\) possibilités : permuter \(X\), décider si \(Y,Z\) sont échangées,
puis utiliser les voisins dans \(X\) pour déterminer toutes les autres images.

Il reste l’identité et une involution \(\tau\). Mais, pour le sommet extérieur 0,
\[
N(0)\cap U=\{2,4,5,11,20,24\}.
\]
Sous \(\tau\), cet ensemble devient
\[
\{1,4,10,14,16,18\}.
\]
**Aucun des dix sommets extérieurs n’a ce profil d’attache.** L’involution ne peut donc pas
se prolonger.

Enfin, les dix profils d’attache sont distincts. Un automorphisme fixant \(U\) point par point
fixe donc chacun des dix sommets restants. Conclusion :
\[
\boxed{Aut(H)=\{\mathrm{id}\}.}
\]

C’est une explication de l’asymétrie par incompatibilité du prolongement d’une symétrie du
noyau. Il n’est pas nécessaire de faire confiance à la seule sortie d’un logiciel de groupes.

Une seconde preuve indépendante utilise les nombres de \(K_4\) et \(K_5\) incidents, puis le
raffinement par les couleurs des voisins. Les nombres de couleurs sont
\[
5\longrightarrow16\longrightarrow22\longrightarrow25.
\]
Toute permutation préservant les arêtes préserve ces couleurs ; vingt-cinq couleurs
distinctes imposent l’identité. L’autre classe asymétrique donne
\(5\to13\to18\to25\).

## 5. Pourquoi les approches plus contraintes se bloquaient

### Préserver cinq fibres-cliques interdit ici l’asymétrie

J’ai recensé les partitions en cinq \(K_5\) disjointes dans chaque classe. Seules les classes
n° 1 et 2 en possèdent, trois chacune. Leurs groupes ont ordres 72 et 600.
Les treize autres classes, notamment les deux asymétriques, n’en possèdent aucune.

Ainsi, dans cette famille connue et reconstruite, une recherche imposant une telle partition
ne peut pas atteindre l’asymétrie. En gardant une seule clique et en libérant la partition
du reste, le même type de reconstruction atteint les quinze classes.

### Un échec complet du changement standard n’est pas une impossibilité globale

Tous les ensembles de commutation standards de Godsil–McKay à une cellule, de taille paire
4 à 24, ont été énumérés dans les quinze graphes. Dans Paley, il y en a exactement cinquante,
tous de taille douze, et ils redonnent tous Paley à isomorphisme près.

Le graphe des transitions possède trois composantes :
\[
\{2\},\quad \{1,3,6,11\},\quad
\{4,5,7,8,9,10,12,13,14,15\}.
\]
**Aucune succession de ces seuls changements ne mène de Paley à l’asymétrie.**
La reconstruction avec un bord \(K_5\) y parvient pourtant.
Cela ne concerne pas toutes les généralisations de Godsil–McKay à plusieurs cellules.

### Une échelle de bords fixés

Pour une seconde clique précise \(C=\{3,7,11,15,24\}\), j’ai conservé \(S\) et les premières
positions de \(C\), avec toutes leurs incidences :

| Sommets du bord fixés | Classes de complétions | Asymétriques |
|---:|---:|---:|
| 10 | 2 | 0 |
| 9 | 2 | 0 |
| 8 | 2 | 0 |
| 7 | 4 | 0 |
| 6 | 12 | 2 |
| 5 | 15 | 2 |

L’énumération est terminée pour chaque ligne. Cette table porte sur ces ensembles emboîtés
explicites ; elle ne classe pas tous les sous-ensembles de chaque taille.

## 6. Un contrôle dans la famille \(\lambda=1,\mu=2\)

Sur Paley(9), le même moteur, paramétré par \((9,4,1,2)\) et un triangle fixé, retrouve
quatre complétions étiquetées. Toutes sont la grille \(3\times3\) à renommage près.
Il n’invente donc pas un asymétrique dans ce petit cas.

Les calculs avec et sans suppression des échanges ont aussi été comparés : les totaux
coïncident pour ce contrôle, pour le bord à six sommets de Paley(25), et pour celui à dix.

## 7. Ce qui est réutilisable dans la campagne à 243

Le résultat n’est pas « moins de symétries implique plus de désordre ». Le témoin asymétrique
a encore un noyau reconnaissable, des cliques et des profils d’incidence très rigides.

Deux conclusions précises émergent :
1. **On peut bloquer la construction d’asymétriques en conservant une représentation trop forte.**
   À 25, la partition en cinq fibres-cliques est exactement un tel obstacle.
2. **Une structure locale peut être conservée sans conserver son groupe de symétries.**
   Le bord \(K_5\) est identique dans les quinze classes ; les attaches au noyau final détruisent
   la dernière involution dans le témoin livré.

Cela donne un contrôle positif pour les moteurs de reconstruction : l’objectif « partir d’un
graphe symétrique, préserver un bord, obtenir un SRG asymétrique » est effectivement réalisé,
et l’on sait pourquoi certains modèles plus étroits échouent.

Les preuves de cette campagne ne disent pas que les partitions en grilles de la famille
243 doivent disparaître pour permettre l’asymétrie. Ce serait une autre affirmation à tester.
Elles n’excluent aucun rang de Conway. Leur apport est un mécanisme concret et un problème
complètement décidé permettant d’évaluer les stratégies avant de les transporter.
