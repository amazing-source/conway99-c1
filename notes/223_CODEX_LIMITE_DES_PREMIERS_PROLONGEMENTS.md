# 223 — Limite des premiers prolongements des 174 noyaux

9 octobre 2026. Aucun noyau supplémentaire exclu dans cette note.

## 1. Retour LAB, message 412

LAB rapporte deux pilotes sans gain après la réduction de la note 222 :

- Fermeture par les troisièmes sommets de triangles sur les arêtes entre
  S et D : 15 noyaux sur 174, tous arrêtés au plafond, aucun arbre épuisé.
  L'absence de contradiction avant le plafond n'est pas une extension.
- Relaxation sur les nombres d'arêtes entre classes de masques : les 29
  noyaux essayés restent faisables numériquement. Aucune exclusion.

Ce sont les résultats communiqués par LAB, pas une seconde exécution par
Codex. Ils justifient de ne pas approfondir automatiquement ces campagnes.
Le seul noyau mort dans un essai antérieur de LAB appartenait déjà aux
136 exclusions de la note 222 ; il n'ajoute donc aucune exclusion.

## 2. Pilote Codex : intégralité et coexistence

Le programme `code/codex/twisted_prism_coexistence.py` prend un noyau sur
douze dans la liste triée des 174 survivants, soit 15 noyaux, et impose
d'abord des multiplicités **entières** dans le modèle de la note 222.
Les 15 systèmes ont un témoin, vérifié par substitution exacte dans
Mx=r et contrôle des bornes. L'intégralité seule n'exclut aucun de ces
15 noyaux. Aucune conclusion n'est tirée sur les 159 non essayés.

Un second modèle impose la coexistence des masques deux à deux. Pour
deux sommets distincts de masques b et c, on examine séparément les deux
statuts a=0 et a=1 de leur éventuelle arête. Les conditions nécessaires
sont :

    b·c ≤ 2−a,
    A_H b + a c ≤ 2−b,
    A_H c + a b ≤ 2−c,

ainsi que la positivité exacte des deux projecteurs sur H augmenté des
deux sommets. Les compléments de Schur sont de taille deux ; après
multiplication par un dénominateur commun, leurs déterminants sont testés
en entiers. Si aucun statut n'est possible, les deux masques ne peuvent
coexister. Cela concerne aussi deux occurrences d'un même masque.
En particulier, un masque de poids au moins trois ne peut apparaître
deux fois, puisqu'il donnerait déjà au moins trois voisins communs.

Le solveur utilise des variables de présence et des multiplicités bornées.
**Les 15 noyaux ont encore un témoin entier**, archivé puis relu exactement.
Les statuts de chaque paire ne sont pas assemblés en une matrice complète
d'adjacence : ces témoins satisfont des conditions nécessaires, sans
construire les arêtes extérieures ni un SRG.

Le contrôle positif conserve les 229 vrais sommets extérieurs du 243 tordu
et leurs **26106 paires**, chacune avec son vrai statut d'adjacence.
Tous les témoins et ce contrôle ont été relus avec succès.

Reproduction et relecture :

    python code/codex/twisted_prism_coexistence.py --out data/codex_twisted_prism_coexistence.json --stride 12 --seconds 2
    python code/codex/twisted_prism_coexistence.py --out data/codex_twisted_prism_coexistence.json --verify-only

Le plafond est de deux secondes de solveur par modèle et par noyau,
en plus du calcul exact des domaines et des contrôles positifs. Aucun
résultat INFEASIBLE du solveur n'est traité comme certificat indépendant
dans ce programme ; les résultats présents sont tous des témoins.

## 3. Conséquence lisible du catalogue et cible globale

Le nombre d'arêtes à l'intérieur des huit sommets D, parmi les 174
survivants, a la distribution suivante :

    e(D)=0 : 1 type ; 1 : 6 ; 2 : 31 ; 3 : 81 ; 4 : 55.

La couverture et les exclusions des notes 221–222 donnent donc, autour
de **tout** motif S à exactement deux arêtes transversales dans un
candidat C1,

    e(D(S)) ≤ 4,        61 ≤ e(C(S)) ≤ 65.

La seconde borne utilise e(C)=61+e(D), déjà démontrée en note 221.
Il s'agit de conséquences des exclusions déjà comptées, pas de nouvelles
exclusions s'ajoutant aux 199 types supprimés.

Une cible différente de l'approfondissement de chaque noyau est la
compatibilité de ces restrictions autour de **tous les motifs S d'un
même graphe**. Le premier sous-problème proposé à LAB est un double
comptage de la somme des e(D(S)), ou des effectifs de types qui y
contribuent. On ne suppose pas que cette somme fournisse une contradiction.

Pour fixer les conventions, soit N_j le nombre de paires non ordonnées
de triangles disjoints avec j arêtes transversales. Ces arêtes forment
un couplage, donc 0≤j≤3. Dans les paramètres de C1 :

    N_0+N_1+N_2+N_3 = 24486,
    N_1+2N_2+3N_3 = 24948,
    N_2+3N_3 = 4158.

Preuves : il y a 231 triangles, sept par sommet, donc 231·230/2−99·21
paires disjointes. Chacune des 693 arêtes se prolonge de 6·6 façons
en une arête transversale entre deux triangles disjoints. Enfin les
2079 quadrilatères induits donnent deux paires de triangles par les
deux choix d'arêtes opposées à prolonger ; une paire comptée dans N_j
contribue pour j(j−1)/2 quadrilatères. Ainsi

    N_2=4158−3N_3,  N_1=16632+3N_3,  N_0=3696−N_3.

Ces identités élémentaires n'introduisent aucune exclusion nouvelle.
Le comptage analogue sur le 243 tordu donne (N_0,N_1,N_2,N_3)=
(140130,221130,19440,2430). Sur ses 19440 motifs S, e(D) vaut 0,1,2
avec effectifs 8640,6480,4320. Il ne justifie donc pas une prétendue
borne universelle e(D)>4 ; tout argument de contradiction devra exploiter
les paramètres de 99 et des relations supplémentaires.

## 4. Ce que l'identification avec les anciennes étoiles permet

Dans S=012∪345, l'arête 34 est une arête transversale du graphe proche
de T=012, et 5 son apex lointain. Les huit sommets D décrivent les
partenaires proches, les autres voisins transversaux de 3 et 4, et le
reste de l'ombre de 5. Cette identification relie les deux descriptions.

Elle ne transforme pas les exclusions des quatre boules de contrôle
(note 216) en un théorème sur toutes les boules au rang 37. Observer
qu'un type parmi les 174 n'apparaît pas dans ces quatre boules n'exclurait
pas ses autres réalisations. Ce croisement n'est donc pas lancé comme
nouvelle campagne d'exclusion.

**État inchangé : 174 noyaux ouverts.** Les pilotes de cette note
localisent une limite des relaxations essayées. Ils ne ferment aucune
famille supplémentaire et ne prouvent pas l'inefficacité de toute la route.
