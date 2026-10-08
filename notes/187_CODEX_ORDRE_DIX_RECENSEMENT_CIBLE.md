# 187 — Un recensement ciblé exact à dix sommets

8 octobre 2026. Proposition de la famille `(5,5)` par LAB au message 230,
construction et vérification des formules par Codex.

Le passage à dix sommets est réalisable sans éliminer une grande matrice dense.
Une récurrence triangulaire donne exactement les comptes des familles `(5,5)`
de normes six et huit à partir de **3875 types** et **469 nouveaux comptes de
graphes de degré minimum trois**. On ajoute **66182 inégalités d'extension**
et tous les comptes positifs à neuf sommets.

La première conséquence uniforme est **N8≥2896844 représentants signés**
de norme huit, et une borne conjointe d'environ **8,985 millions** sur
N8+(651/34)N6. N6,N8 désignent ici les représentants de cette seule famille,
pas les coefficients b3,b4 du réseau. Les collisions de masse jusqu'à dix
restent à traiter avant toute addition aux bornes de vecteurs distincts.

## 1. Familles complètes aux deux normes

Pour ψ=1_X−1_Y, avec X,Y disjoints de taille cinq,

    Q(ψ)=30−2(e(X)+e(Y)−e(X,Y)).

Les graphes localement admissibles sur cinq sommets ont au plus six arêtes.
Les deux types à six arêtes sont le papillon et la maison. Par conséquent :

- Q=6 : deux types à six arêtes anticomplets ;
- Q=8 : un type à six arêtes et un à cinq arêtes, anticomplets, ou deux types
  à six arêtes avec exactement une arête entre eux.

Le générateur parcourt toutes ces possibilités, dédoublonne les types induits
à dix sommets et recompte leurs partitions signées de taille cinq. Il obtient
trois types pour Q=6 et vingt-cinq pour Q=8. Il ne suppose pas que les représentants
ont des images distinctes.

## 2. Identité triangulaire sur les plongements étiquetés

Notons I(F)=|Aut(F)|·C(F), le nombre de plongements induits étiquetés de F.
Si F possède un sommet v de degré au plus deux, posons H=F−v et S=N_F(v).
Pour une copie étiquetée de H, le nombre de sommets extérieurs adjacents à S vaut

    β(H,S) = 99−|H|                                      si |S|=0,
             14−deg_H(s)                                 si S={s},
             λ ou μ − |N_H(s)∩N_H(t)|                    si S={s,t}.

Pour T⊆V(H), soit H+_T v l'extension dont le voisinage de v est exactement T.
Le double comptage étiqueté donne

    I(F)=β(H,S) I(H) − Σ_(T strictement supérieur à S) I(H+_T v).       (1)

Les extensions violant les budgets locaux λ≤1, μ≤2 sont absentes. Chaque terme
restant possède strictement plus d'arêtes que F : la récurrence termine sur
les types de degré minimum trois, conservés comme paramètres de comptage.
Les répétitions isomorphes de voisinages T sont conservées avec leur multiplicité.
La division par |Aut(F)| intervient seulement après le calcul étiqueté.

Les trois types Q=6 seuls nécessitaient 485 types et 238 nouveaux paramètres.
L'ensemble Q=6,8 nécessite 3875 types et 469 paramètres. Les coefficients sont
rationnels exacts ; chaque identité (1) est revérifiée après substitution.

Ce calcul ne prouve pas que ces 469 coordonnées sont indépendantes dans un
recensement complet à dix sommets. Ce sont des comptes géométriques conservés
comme variables ; des relations supplémentaires peuvent resserrer la relaxation.

## 3. Bornes supplémentaires par extensions partielles

Pour chaque type F retenu, chaque sommet supprimé et chaque marque de taille
zéro, un ou deux contenue dans son voisinage, on retrouve une équation d'extension
de la méthode des notes 175–182. Son second membre est connu à neuf sommets.

Tous les types à dix sommets n'étant pas présents, la somme des contributions
des seuls types retenus est **au plus** ce second membre. Les types omis ont
des comptes non négatifs. Cette procédure fournit 66182 inégalités valides,
en plus de la positivité des 3875 types retenus et des 5311 comptes d'ordre neuf.

Les marques sont regroupées sous les automorphismes du graphe à neuf sommets ;
le facteur d'orbite multiplie le budget et son compte induit. Un contrôle sur
le recensement complet à sept sommets retrouve exactement toutes les égalités,
sans reste dû à des types omis.

## 4. Certificats obtenus et limites

Les bornes rationnelles ci-dessous sont vérifiées par combinaison non négative
des lignes exactes. Le solveur flottant sert uniquement à choisir un support
de multiplicateurs ; une résolution rationnelle vérifie ensuite chaque coordonnée.

| Hypothèse | Expression | Borne certifiée |
|---|---|---:|
| Aucune | N6 | 0 |
| Aucune | N8 | 409338402858/141305 ≈2896843,019 |
| Aucune | N8+(651/34)N6 | 6476525335771850898/720851152565 ≈8984552,931 |
| P=0 | N6 | 0 |
| P=0 | N8 | 409338402858/141305 ≈2896843,019 |
| P=0 | N8+(651/34)N6 | 606289749471681/66769492 ≈9080340,906 |

N8 est pair, d'où la borne entière 2896844. Aucun point rationnel atteignant
les bornes du tableau n'a été vérifié : on parle donc de **bornes inférieures
certifiées**, et non d'optima exacts établis. Le zéro de la première ligne
signifie que ce calcul n'a pas certifié de minoration positive pour N6.

L'estimation d'environ 600000 représentants de norme six proposée par LAB,
issue d'un transfert de ratios mesurés sur les graphes à 243 sommets, reste
une heuristique. Les présents calculs ne permettent pas de l'employer dans
une preuve au rang 37. Les inégalités ci-dessus concernent uniquement des
représentants ; aucune nouvelle exclusion de rang n'est revendiquée.

## 5. Catalogue des supports binaires potentiels de masse dix

Indépendamment du choix des cibles, on engendre tous les graphes admissibles
à dix sommets de degré minimum trois. Supprimer un sommet dans un tel graphe
laisse nécessairement un type à neuf sommets de degré minimum deux. En le
réétendant, tous ses sommets de degré deux doivent recevoir le nouveau voisin.
L'énumération de tous les voisinages restants est donc exhaustive.

Elle donne **492 types**, dont 469 apparaissent dans le recensement ciblé.
Les 23 autres types, leurs codes et toutes les adjacences sont archivés.
Il s'agit de candidats nécessaires pour un support de signe **binaire** dans
une différence de masse dix. Les arêtes entre les deux supports, leur compatibilité
et les différences non binaires ne sont pas classifiées par ce catalogue.

## 6. Contrôles et fichiers

La récurrence (1) retrouve exactement **1428 comptes d'ordre neuf** de degré
minimum au moins deux, en utilisant les comptes d'ordre huit et les paramètres
denses déjà connus. Tous les contrôles des identités à sept sommets et toutes
les identités triangulaires du nouveau calcul passent en arithmétique exacte.

    python code/codex/targeted_order10_census.py
    python code/codex/targeted_order10_minima.py
    python code/codex/targeted_order10_minima.py --verify-only
    python code/codex/mass10_support_catalogue.py

Le troisième appel vérifie les six certificats archivés **sans relancer le LP**.
Les formules, adjacences, identités étiquetées et inégalités d'extension sont
dans `data/codex_targeted_order10_census.json.gz` (JSON compressé, environ 6,3 Mo).
Les certificats sont dans `data/codex_targeted_order10_minima.json`, et le catalogue
dans `data/codex_mass10_support_catalogue.json`.

Le recensement est ciblé : la complétion à tous les types d'ordre dix et l'audit
des collisions constituent des prolongements distincts encore nécessaires.
