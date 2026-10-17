# 169 — Norme 16 : 478 premières attaches à symétrie près, portée du test de rang

8 octobre 2026. Codex, réponse à la suggestion de LAB au message 139 du pont.

**Résultat.** Pour les cinq cœurs de norme 16 de la note 166, nous classons les attaches des huit sommets D
ayant deux voisins dans P et deux dans Q, sous les premiers filtres locaux nécessaires. À B fixé, on obtient
4985 possibilités, ou **478 orbites** sous les automorphismes conservant séparément P et Q.
Les 64 attaches simples S sont ensuite entièrement déterminées par leurs multiplicités dans les cellules (p,q).

Ces données fixent le bloc des 16 sommets du support et toutes ses colonnes vers l'extérieur.
Le test de rang par blocs donne seulement 15, 17 ou 19 suivant le cœur, donc ne renforce pas la borne globale 33.
Nous ne prétendons pas exclure la norme 16 au rang 33. Il faut exploiter d'autres contraintes, notamment
les arêtes entre sommets extérieurs ; la classification présente fournit un premier niveau fini pour cela.

## 1. Données et filtres

Les cinq matrices B entre P et Q sont celles de `data/codex_norm16_cores.json` (note 166).
Posons M=2I+2J−BBᵀ et N=2I+2J−BᵀB. Les huit sommets D donnent une bijection entre les arêtes
des multigraphes M et N, en comptant les arêtes doubles avec leur multiplicité.

Un sommet d∈D est donc représenté par un quadruplet (p,p′,q,q′). Nous imposons :

1. les huit paires {p,p′} sont exactement les arêtes de M, avec multiplicité ; de même pour N ;
2. B sur {p,p′}×{q,q′} est un appariement, éventuellement vide, car les voisins de d induisent un appariement ;
3. pour chaque cellule (p,q), son nombre de couvertures par D ne dépasse pas 2−B_pq ;
4. deux sommets de D ont au plus deux voisins communs dans P∪Q.

Ces quatre conditions sont nécessaires dans tout SRG recherché. La troisième utilise le nombre exact de
voisins communs de p et q : ils sont tous extérieurs à P∪Q, et valent 1 si B_pq=1, 2 sinon.
La quatrième ne suppose pas l'adjacence entre les deux sommets D : tout couple du SRG a au plus deux
voisins communs. Elle ne prétend pas vérifier le nombre total, qui dépend aussi de l'extérieur.

Le nombre de sommets S de cellule (p,q) est alors

    s_pq = 2−B_pq−nombre de quadruplets contenant p et q.

Il est non négatif, de somme 64 ; chacun des seize sommets du support a dix voisins extérieurs,
dont deux dans D et huit dans S. Les onze sommets Z n'ont aucun voisin dans le support.

## 2. Énumération complète de ce premier étage

`code/codex/norm16_attachments_rank.py` compare exactement les ensembles obtenus par deux méthodes :

- un retour sur trace sur les huit paires de M, avec consommation des multiplicités de N,
  capacités des cellules et rejet des intersections trop grandes ;
- les 8! permutations de la liste des arêtes de N, suivies de vérifications sur les objets complets.

Les sommets de D sont non étiquetés : un résultat est une liste triée de huit quadruplets.
Les répétitions d'arêtes doubles ne produisent donc pas de faux cas supplémentaires.
La première méthode ordonne les choix correspondant à des paires de M identiques ; la seconde les
déduplique seulement après génération. Elles retrouvent exactement les mêmes ensembles, pas seulement
les mêmes nombres.

Les automorphismes conservant P et Q sont calculés parmi les 8! permutations de P. Puisque les colonnes
de B sont distinctes, une permutation de P conservant leur ensemble détermine une unique permutation de Q.
Le programme vérifie B_pq=B_σ(p),τ(q), puis partitionne la liste complète des attaches en orbites.
Il contrôle que chaque image appartient à la liste et que les orbites la recouvrent sans intersection.

| Cycles du défaut | Attaches, B fixé | Ordre du groupe conservant P,Q | Orbites |
|---|---:|---:|---:|
| 8 | 1820 | 8 | 243 |
| 6+2 | 681 | 6 | 118 |
| 4+4 | 2068 | 32 | 86 |
| 4+2+2 | 326 | 16 | 27 |
| 2+2+2+2 | 90 | 192 | 4 |
| Total | 4985 | | 478 |

L'échange de P avec Q n'est pas quotienté : les 478 cas peuvent encore contenir des paires équivalentes
par échange des signes du vecteur. Ce nombre est un nombre d'orbites sous le groupe explicitement indiqué,
pas une classification complète à isomorphisme quelconque près.

Les représentants et tailles de toutes les orbites sont archivés dans `data/codex_norm16_attachments_rank.json`.
Des empreintes de la liste complète triée permettent d'identifier exactement les ensembles énumérés.

## 3. Rangs sur F7

Le bloc du support de A−3I est

    F = [ −3I_8    B   ]
        [   Bᵀ   −3I_8 ].

Soit C le bloc 16×83 vers D∪S∪Z. Il est entièrement déterminé par une attache du §2,
à permutation des sommets S de même cellule près. Le vecteur φ=(1_P,−1_Q) vérifie
Fφ=0 modulo 7 et Cᵀφ=0 sur les entiers. Il reste donc toujours au moins une dimension du noyau non couplée.

Le programme calcule un noyau de F et le rang de sa restriction par Cᵀ pour **chacune des 4985 attaches**.
Dans tous les cas, le noyau commun est exactement la droite engendrée par φ.

| Cycles | rang F | dim ker F | rang(Cᵀ sur ker F) | Borne par blocs |
|---|---:|---:|---:|---:|
| 8 | 13 | 3 | 2 | 17 |
| 6+2 | 15 | 1 | 0 | 15 |
| 4+4 | 11 | 5 | 4 | 19 |
| 4+2+2 | 13 | 3 | 2 | 17 |
| 2+2+2+2 | 15 | 1 | 0 | 15 |

La dernière colonne utilise la même inégalité que la note 165 :

    rang [F C; Cᵀ H] ≥ rang F + 2 rang(Cᵀ|ker F).

Les calculs se font par élimination exacte modulo 7, sans calcul approché. Les cinq rangs de F sont aussi
comparés à l'implémentation indépendante de la note 165.

Pour un représentant de chaque cœur, nous construisons explicitement un bloc symétrique H sur F7 qui
atteint exactement cette borne. Si I indexe un bloc principal inversible de F de taille rang F, prendre

    H = C_Iᵀ (F_II)⁻¹ C_I.

Après élimination, le complément est [0 K;Kᵀ 0], de rang 2 rang K. Le programme vérifie directement
les cinq rangs des matrices complètes de taille 99.

**Ces matrices ne sont pas des matrices d'adjacence.** Elles montrent seulement que les données F,C
et la symétrie, sans contraintes supplémentaires sur H, ne peuvent imposer un seuil de rang plus élevé.
Elles ne donnent ni contre-exemple au problème de Conway ni complétion admissible d'un cœur.

## 4. Pourquoi Z ne se transporte pas comme dans la norme 14

Dans la norme 14, Z est une coclique de quinze sommets : on l'incorpore au bloc connu et cela conduit à 33.
Dans la norme 16, Z a onze sommets et vérifie e(Z)=e(D)+5 (note 166), donc ne peut pas être indépendant.
Il manque les arêtes internes de Z, ainsi que ses attaches à D et S.

À titre de comparaison algébrique seulement, si A_Z−3I était inversible modulo 7, l'ajouter au bloc
ferait passer les cinq bornes du tableau à 28,26,30,28,26. Si ce bloc est singulier, son noyau et son
couplage extérieur doivent être étudiés. Aucune de ces situations n'est exclue par le présent calcul.

La suggestion « tous les cœurs de norme 16 forcent r≥35 » n'est donc pas démontrée par le seul petit
calcul de rang du support. La réduction à 478 attaches garde une utilité pour le niveau suivant,
qui doit intégrer des contraintes du SRG entre sommets extérieurs.

## 5. Reproduction et piste quartique

Depuis la racine du dépôt :

    python code/codex/norm16_attachments_rank.py

Le programme utilise Python standard, ainsi que SymPy uniquement pour la comparaison des cinq rangs
avec le vérificateur précédent. Durée locale observée : environ cinq secondes.

En parallèle, la lecture du programme quartique de LAB (commit `f31263d`, message 139) a révélé un signe
incorrect dans sa correction des 462 vecteurs de triangles. Si U=hi·b_2−S et si chacun de ces 462 vecteurs
contribue c=52/3, la contrainte renforcée est

    U−462(hi−c) ≥ 0,

et non U+462(hi−c)≥0. À hi=100 et b_2=462, la vraie somme des 462 contributions vaut 8008 ; la bonne
inégalité est alors une égalité. Une somme fictive 46200 doit être rejetée, et ne l'était pas par la version
au signe erroné. Correction signalée au message 140 et recalcul demandé à LAB.
Cette erreur est dans l'essai quartique ultérieur ; les certificats de la note 168 ne l'utilisent pas.
