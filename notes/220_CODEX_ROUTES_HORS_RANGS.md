# 220 — Reprendre C1 par des routes qui couvrent tous les rangs

9 octobre 2026, investigation commencée le 8. Demande explicite de
l'utilisateur : changer effectivement de cible, examiner d'autres
approches que l'exclusion successive de 37,39,41,43, et relire les
trois routes A/B/C de C2.

## 1. Ce que faisaient réellement les trois routes de C2

Source relue : `Desktop/c2_experimental/notes/46_LIGNE_D_ARRIVEE_C2.md`,
§§1–8 ; notes C1 137 et 139. Ces lettres ne désignent pas les routes
internes A/B de T20.

| Route C2 | Objet et preuve de couverture | Obstacle initial |
|---|---|---|
| A | Une identité force un bloc lourd ; après sélection du bloc, liste des types locaux à pivots (1507 dans le raffinement). | Les recherches locales restaient indécises sans lemme supplémentaire. |
| B | Si le bloc lourd choisi avec bris d'égalité n'a pas de pivot, tout le système est dans la famille globale tout-dis. | La relaxation linéaire symétrisée était faisable ; les signes et incidences restaient nécessaires. |
| C | Les deux valeurs possibles du paramètre g donnent une enveloppe unimodulaire de dimension 24 appartenant à une même liste de 156 réseaux. | Exclure le repère requis dans chaque enveloppe. |

A et B étaient deux branches complémentaires d'une même réduction.
C offrait une autre couverture de l'ensemble et pouvait fermer A et
B simultanément. Leur clôture via C ne signifie donc pas trois preuves
indépendantes achevées. La leçon transférable est **objet obligatoire,
couverture complète, puis exclusion des réalisations**, avec un critère
de fin écrit avant les calculs.

La classification de dimension 24 venait de l'involution. Les objets
de réseau globaux connus pour C1 sont de dimension bien plus grande ;
adjoindre une enveloppe n'apporte pas de petit catalogue comparable.
La masse estimée en note 156 ne prouve cependant pas l'impossibilité
de toute autre réduction : elle concerne une construction précise.

## 2. Trois directions distinctes pour C1

### Motif obligatoire et prolongement — direction retenue

Un théorème de Makhnev impose deux triangles reliés par exactement
deux arêtes dans tout candidat à 99 sommets. Partir de cette
configuration, plutôt que d'un graphe proche arbitraire à 36 sommets,
donne un point de départ couvert par un théorème.

Le premier calcul a été effectué, pas seulement proposé : autour
des six sommets, les équations exactes imposent huit sommets à deux
voisins dans le motif. La note 221 classe les noyaux de 14 sommets :
373 types enracinés, 63 exclus par les projecteurs réels du SRG,
310 non exclus à cette étape. La note 222 réduit ensuite cette liste
à 174 par les incidences extérieures. Ces exclusions ne dépendent
d'aucun rang modulo 7.

**But suffisant :** exclure les prolongements des 174 noyaux restants dans
99 sommets. Une contradiction dans chaque prolongement ferme C1.
Il n'est pas établi que ces prolongements se réduisent à 174 petits
calculs : c'est le verrou suivant, et non un détail d'exécution.

Les preuves d'Azarija–Marc pour d'autres paramètres suivent une
architecture proche : forcer une structure, en contrôler les
prolongements, puis employer les compléments étoilés. Elles montrent
que cette architecture peut fonctionner, pas qu'elle sera efficace
ici. Le théorème Ω de la note 157 fournit déjà une reconstruction
exacte ; il ne fournit pas le petit catalogue de compléments adapté.

Il ne faut pas supposer qu'un complément étoilé contient toute
configuration choisie. LAB rappelle (message 404) que la boule entière
d'un triangle contient des supports de fonctions propres et ne peut
être incluse arbitrairement dans un tel complément. Le noyau de 14
sommets ci-dessus est utilisé comme sous-graphe induit obligatoire ;
aucune propriété de complément étoilé ne lui est attribuée.

### Plan binaire à trois couches — direction de réserve solide

Pour chaque triangle, les 60 sommets lointains donnent des triplets
de paires dans trois ensembles de 12 points. Chaque couche utilise
exactement une fois chacune des 60 paires non appariées. Il faut
réaliser simultanément toutes les concurrences prescrites par G,
soit une matrice binaire N avec NNᵀ=K (note 163).

**But suffisant :** prouver l'impossibilité de ce système pour toutes
les configurations proches nécessaires, ou forcer une sous-famille
pour laquelle il est impossible. Cela couvre tous les rangs et garde
la binarité perdue dans la relaxation de la note 219.

**État exact :** LAB n'a aucun témoin de N complet pour m=12. Ses
témoins pour une composante (6,6) sont des demi-systèmes ; le système
joint reste indécis. La partie colonnes du pinceau de six grilles
n'est pas une complétion de toutes ses contraintes. Ces faits ne
prouvent ni l'existence ni l'impossibilité d'un N complet.

Les coûts et probabilités des notes 156/163 sont des indications sur
les méthodes essayées, pas des bornes inférieures sur tout algorithme.
En particulier, une estimation aléatoire qui serait défavorable même
aux SRG existants ne sert pas de preuve d'inexistence.

### Transformations et argument extrémal — direction exploratoire

Supposer un candidat à 99 sommets, puis choisir parmi tous les
candidats celui qui maximise un invariant entier borné, par exemple
le nombre de prismes. Si une transformation préservant exactement
les paramètres améliore toujours cet invariant, contradiction.
Autre cible : amener tout candidat à un graphe ayant une symétrie
déjà interdite par les autres dossiers.

Cette logique évite de classer les graphes un par un. La bascule
entre les deux graphes à 243 sommets montre qu'une transformation
non triviale existe dans la famille, mais ne prouve pas qu'elle existe
au point nécessaire dans tout candidat à 99 sommets. Quatre types
de triangles sur cinq du 243 tordu sont rigides pour cette opération
(note 159). La commutation standard de Godsil–McKay n'est pas un
remplacement disponible : la rigidité correspondante est recensée
en note 162.

**Premier verrou à résoudre avant d'y investir davantage :** construire
une transformation admissible dans une famille obligatoire de cas,
et prouver un changement strict d'invariant. Aucun tel mécanisme
général n'est établi ici. Cette direction reste secondaire.

## 3. Voies examinées sans les annoncer comme nouvelles

- Les cocliques de taille 22 produiraient un design 2-(22,4,2), mais
  leur existence n'est pas forcée. Une étude conditionnelle de ces
  designs ne couvrirait donc pas C1 à elle seule (Lou–Murin, note 104).
- Le graphe des 231 triangles et les codes des droites sont de vrais
  objets globaux ; les identités spectrales et les rangs binaires ou
  ternaires déjà obtenus ne suffisent pas (notes 70, 91, 99, 110).
  La littérature récente sur les graphes de cliques confirme l'intérêt
  de l'objet, sans fournir ici une nouvelle obstruction applicable.
- Forcer toute géométrie de la famille à être non tordue est faux :
  le second graphe à 243 sommets du dossier est un contre-exemple.
  Une obstruction doit exploiter les paramètres de 99.

## 4. Décision et prochaine étape

La recherche active passe au noyau obligatoire de la note 221 et à
ses prolongements. Les nombres à suivre seront les types réellement
interdits ou les familles de prolongements effectivement supprimées,
pas le nombre de relectures. Un certificat exact nouveau se vérifie ;
les mêmes exemples déjà exclus ne sont pas relancés par défaut.

Le premier prolongement a une description concrète : 33 sommets sans
voisin dans le motif initial, six classes de 8 ou 9 sommets, et les
huit sommets doubles déjà fixés. Les degrés entre ces parties et les
voisinages communs sont imposés. Le prochain test utile est la
compatibilité globale de ces incidences, puis la fermeture des arêtes
entre les classes. Rien ne garantit encore une exclusion totale.

**Premier prolongement effectivement réalisé (note 222).** Les 310 noyaux
passant les projecteurs ont tous été examinés en 22,4 secondes. Le modèle
des incidences des 85 sommets extérieurs exclut **136 noyaux supplémentaires**,
chaque fois avec un certificat entier relu. Il reste **174 noyaux** dans
une couverture valable pour tous les rangs. Ce gain concret motive la
poursuite de cette voie ; il ne prédit pas le coût des étapes suivantes.
Le graphe tordu à 243 sommets passe le même modèle avec ses propres
paramètres et sa vraie extension à 229 sommets extérieurs.

La fermeture bornée des voisins communs est le prochain pilote confié à
LAB. Continuer si elle supprime des familles ou révèle une implication
uniforme ; si les branches prolifèrent sans gain, confronter ce coût aux
deux voies en réserve et aux contraintes de rang encore utiles. Le choix
de route reste révisable : le but est une obstruction à C1, pas la défense
de cette méthode particulière.

## Sources consultées

- A. A. Makhnev, *Strongly regular graphs with λ=1* (1988),
  DOI [10.1007/BF01158426](https://doi.org/10.1007/BF01158426),
  [notice Math-Net](https://m.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=4220&wshow=paper).
  Le théorème pertinent et sa preuve avaient été lus dans la note 94 §3.1.
- Azarija–Marc, [non-existence pour (75,32,10,16)](https://arxiv.org/html/1509.05933v6),
  §§2–3, et [pour (95,40,12,20)](https://arxiv.org/html/1603.02032v2), §§2–3.
- Lou–Murin, [étude du graphe (99,14,1,2)](https://math.mit.edu/research/highschool/primes/materials/2014/Lou-Murin.pdf),
  §§4 et 7.
- Connor Phillips, [étude des graphes de cliques](https://arxiv.org/html/2605.22867v1),
  §4.1. Pas d'obstruction supplémentaire utilisée comme axiome.
