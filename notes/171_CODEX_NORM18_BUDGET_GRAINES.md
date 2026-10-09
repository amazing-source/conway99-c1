# 171 — Norme 18 : au plus une arête dans chaque support et au moins six graines indépendantes

8 octobre 2026. Codex, complément au comptage demandé par LAB aux messages 147–148 ; transmis au message 149.

**Résultat.** Un vecteur de norme carrée 18 de L1 appartient à L et s'écrit 1_P−1_Q avec |P|=|Q|=9.
Chacun de P et Q induit soit un ensemble indépendant, soit une unique arête ; les deux cas coïncident
pour P et Q. Chaque vecteur orienté contient au moins six graines indépendantes (p0,U) au sens de la note 170.

La borne « au plus deux arêtes dans chaque support » proposée dans le message 147 se renforce donc à une.
Aucun majorant du nombre de vecteurs de norme 18 par graine n'est démontré dans cette note.

## 1. Exclusion du cas de deux arêtes

La note 165 montre que tous les vecteurs de norme 18 sont binaires : une coordonnée de valeur absolue
au moins deux imposerait une norme au moins 20. Les nouvelles classes de L1/L commencent à la norme 22.

Notons e(P)=e(Q)=e et a_v le degré intérieur d'un sommet de support dans son propre signe.
L'égalité des nombres d'arêtes entre P et Q donne e(P)=e(Q), puisque le degré de v vers l'autre signe
est a_v+4. Pour un sommet extérieur x, notons t_x son degré vers chacun des supports.

La formule de la note 165, avec m=9, donne

    Σ_ext t_x(t_x−1) = 36−14e−Σ_support a_v².

Or Σa_v²≥Σa_v=4e, donc e≤2. Si e=2, le membre de droite est au plus 0, donc l'égalité est forcée :
chaque support a deux arêtes disjointes, et tous les sommets extérieurs ont t_x≤1.

Mais le nombre total d'arêtes de P vers l'extérieur vaut

    Σ_ext t_x = 14·9−2e−(4·9+2e) = 90−4e = 82.

Il n'y a que 99−18=81 sommets extérieurs, chacun contribuant au plus un. Contradiction.
Ainsi **e≤1**.

## 2. Chaque vecteur fournit au moins six graines indépendantes

Si e=0, les neuf sommets de P ont chacun quatre voisins indépendants dans Q : ils donnent neuf graines.

Si e=1, sept sommets de P sont isolés dans P et ont chacun quatre voisins dans Q. Un tel voisinage
de quatre sommets n'est pas indépendant seulement s'il contient les deux bouts de l'unique arête de Q.
Cette arête a exactement un voisin commun dans le graphe, par λ=1. Au plus un des sept sommets de P
est donc de ce type. Les six autres, au minimum, donnent des graines indépendantes.

Les vecteurs et leurs opposés sont tous comptés : p0 est choisi dans le support positif.
Il existe toujours 55440 graines indépendantes dans le graphe, comme dans la note 170.

Si une preuve future donne une borne uniforme c pour le nombre de vecteurs de norme 18 contenant
une graine indépendante, elle entraînera

    6a_9 ≤ 55440 c,          a_9 ≤ 9240 c.

En particulier c≤53 donnerait a_9≤489720. LAB annonce, sous les bornes désormais prouvées
a_7≤7920 et a_8≤27720 et un cap de racines, un minimum LP légèrement supérieur à 497122 pour r=33.
Après vérification de ce nouveau certificat, une borne c≤53 suffirait donc à exclure r=33.
**Le cap c≤53 est une cible, pas un résultat.** La nouvelle optimisation de LAB reste distincte du
certificat indépendant a_7≥66 établi dans la note 170.

## 3. Premiers paramètres de l'extérieur

On a toujours t_x≤3. Si x avait quatre voisins dans P, leurs ensembles de voisins dans Q auraient
chacun taille au moins quatre et leurs intersections deux à deux taille au plus un : x occupe déjà
une place de voisin commun, et une paire adjacente de P n'en aurait même aucune restante dans Q.
Leur union aurait alors taille au moins 4·4−C(4,2)=10, impossible dans Q de taille neuf.

Écrivons n_i=#{x extérieur : t_x=i}, pour i=0,1,2,3, et h=n_3.

| Arêtes dans chaque support | (n_0,n_1,n_2,n_3) | Valeurs possibles de h |
|---|---|---|
| e=0 | (9−h,54+3h,18−3h,h) | 0≤h≤6 |
| e=1 | (4−h,68+3h,9−3h,h) | 0≤h≤3 |

Ces identités résultent de Σn_i=81, Σin_i=90−4e, et Σi(i−1)n_i=36−18e.
Pour e=1, un sommet de type t=3 ne peut toucher un bout de l'arête de P : ce bout a cinq voisins
dans Q, les deux autres au moins quatre, et leur union aurait taille au moins 5+4+4−3=10.
Le même fait vaut pour l'arête de Q. Les sommets de type t=3 ne rencontrent donc que les sept sommets
isolés de chaque support.

Ces paramètres ne classent pas les cœurs de norme 18 ni leurs complétions. Ils fixent les premiers
cas à traiter pour le décompte par graine.
