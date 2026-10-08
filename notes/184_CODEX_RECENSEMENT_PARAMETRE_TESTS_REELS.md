# 184 — Recensement paramétré et paquet pour vérification sur graphes réels

8 octobre 2026. Réponse au message LAB 216.

Le programme `code/codex/census_real_graph_packet.py` reconstruit les comptes
depuis **un sommet**, avec les paramètres numériques `(v,k,1,2)` injectés dans
les mêmes équations d'extension et la même élimination rationnelle creuse.
Il fournit trois paquets pour `(99,14)`, `(243,22)` et `(9,4)`, désormais jusqu'à neuf sommets.

Deux contrôles sont déjà terminés :

- toutes les 208, 916 et 5311 formules des ordres sept, huit et neuf pour `(99,14)` coïncident
  exactement avec les données des notes 181–182, après changement de coordonnées ;
- sur la grille 3×3, les **6533 comptes de types**, y compris les comptes nuls,
  des ordres deux à neuf coïncident exactement avec une énumération exhaustive
  des sous-ensembles du graphe réel.

LAB a maintenant vérifié indépendamment le paquet d'ordre huit sur les deux
graphes à 243 sommets : 173 types connexes sur bvls243, 106 sur twin243_switched,
ainsi que les comptages des papillons, maisons, familles `(4,4)` et `(7,1)`.
**Aucune différence trouvée.** Ses scripts et sorties sont archivés dans les
commits 7f6bafe et 99d3d3a de sa branche, importés ici. Les types omis sont les
types déconnectés ou trop nombreux pour le budget de calcul fixé par LAB.

Limites : H, C8_5683824 et C8_245715219 sont nuls dans les deux graphes, donc ces
tests n'éprouvent pas leurs coefficients. Le paquet à neuf sommets utilise la
canonisation par individualisation et raffinement de la note 182 ; son test
indépendant sur les deux graphes à 243 sommets reste à effectuer. Le contrôle
exhaustif sur la grille couvre déjà ce chemin de calcul, dans ce cas particulier.

## 1. Coordonnées géométriques

À six sommets, l'invariant est P, le nombre de prismes. À sept sommets, on prend
H, le nombre de copies de D défini dans la note 181. À huit sommets, les sept
comptes des types de degré minimum trois forment une base du nouvel espace libre.
La matrice de changement de coordonnées a bien rang sept. À neuf sommets,
les 48 types de degré minimum trois forment de même une base des 48 nouveaux
invariants. Ils sont nommés C9_CODE, avec l'adjacence de chaque type dans le paquet.

L'ordre des coordonnées affines à huit sommets est

    1, P, H, C8_2022000, C8_5683824, C8_5691760,
    C8_127242964, C8_127305925, C8_128354469, C8_245715219.

Ces types sont tous connexes et denses ; le vérificateur indépendant peut ainsi
mesurer ces invariants sans recenser les milliards de sous-ensembles peu denses.
Les tableaux d'adjacence binaires sont inclus dans les paquets pour éviter toute
ambiguïté liée au codage canonique.

Chaque étape archive toutes les formules affines, les invariants nouveaux avec
leurs graphes, et les comptages signés des familles utiles. Les identités complètes
d'extension et la somme C(v,n) sont vérifiées exactement avant écriture.

## 2. Quelques formules pour les graphes à 243 sommets

Les nombres incluent les deux signes :

    papillon moins arête lointaine = 23950080+12P+2H,
    maison moins arête lointaine   = 97404120−132P+12H.

La famille `(4,4)` de deux quatre-ensembles anticomplets à quatre arêtes a pour compte

    F8 = 705137400−2190P+74H
         +6C8_2022000+4C8_5683824+8C8_5691760
         −10C8_127305925−12C8_128354469.

Sur la grille 3×3, les invariants mesurés sont P=6,H=0,C8_127242964=9 ; les six
autres comptes denses sont nuls. Toutes les familles ci-dessus y ont le compte zéro.

## 3. Nouvelle famille `(7,1)` pour C1

Pour ψ=1_W−e_y, |W|=7,y extérieur, la norme projetée est

    Q=28−2(e(W)−d_W(y)).

Le recensement à huit sommets de C1 donne les comptes signés exacts suivants :

    Q6 = 132P+46H−8C8_127242964,

    Q8 = 4108104+468P−512H+72C8_127242964
         −12(C8_127305925+C8_128354469+C8_245715219).

Le compte Q8 est la somme de deux branches : `e(W)=10,d_W(y)=0` et
`e(W)=11,d_W(y)=1`. Q6 correspond à `e(W)=11,d_W(y)=0`.
Ces formules comptent des représentants et **n'ajoutent pas encore une borne à b3 ou b4**.
Les collisions de cette famille sont en cours d'étude par LAB.

## 4. Fichiers et reproduction

    python code/codex/census_real_graph_packet.py --max-order 9

Paquets : `data/codex_census_validation_99.json`,
`data/codex_census_validation_243.json`, `data/codex_census_validation_9.json`.
Pour chaque entrée `counts` ou `families`, le tableau `affine` (ou la liste de la
famille) multiplie le vecteur `[1]+parameters` de l'étape concernée. Les comptes
sont ceux de sous-ensembles induits, sans multiplicateur d'automorphismes.
