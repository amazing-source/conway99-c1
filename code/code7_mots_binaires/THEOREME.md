# Section binaire du noyau modulo 7 d'un éventuel Conway-99

Date : 12 octobre 2026.
Statut : déduction mathématique à partir des seules équations SRG, démontrée ci-dessous. Aucune revendication de priorité bibliographique. Aucun graphe à 99 sommets n'est construit, aucune hypothèse d'existence supplémentaire n'est démontrée.

## 1. Cadre et énoncé

Soit A la matrice d'adjacence d'un srg(99,14,1,2), supposé exister. On a

    A 1 = 14 1 ;  A² + A = 12 I + 2 J.

Posons T = A + 4 I. Alors

    T 1 = 18 1 ;  T² = 7 T + 2 J.

Le noyau K = ker_F7(T) est le dual du code engendré par les lignes de T, puisque T est symétrique.

**Théorème.** Pour x dans {0,1}^99 tel que T x = 0 modulo 7, son poids w appartient à {0,63,77}. Les deux cas non nuls sont exactement :

* w = 63 : le support S induit un graphe 10-régulier et chaque sommet hors de S a sept voisins dans S. Autrement dit A x = 3 x + 7 1. La partition (S,S^c) est équitable, de quotient [[10,4],[7,7]]. Son complément H a 36 sommets et satisfait A 1_H = 3 1_H + 4 1.
* w = 77 : le complément C est une coclique de Hoffman de taille 22. On a T x = 14 1 et T 1_C = 4 1.

Réciproquement, chacune de ces deux configurations fournit un tel mot binaire.

La propriété de Hoffman n'est pas supposée dans la preuve. Elle apparaît seulement dans l'interprétation du cas w = 77.

**Attention.** « Binaire » signifie ici que toutes les coordonnées du mot de F7 valent 0 ou 1. Le théorème ne borne pas le poids minimal des mots arbitraires du code, dont les coordonnées peuvent prendre les valeurs 2,3,4,5,6. Il ne force pas non plus l'existence d'un mot binaire non nul.

## 2. Preuve complète par deux moments

Soit S le support de x. En sommant T x = 0 modulo 7, on obtient 18w = 0 modulo 7. Écrivons w = 7t, avec 0 <= t <= 14.

Notons d(v) le nombre de voisins de v dans S. Comme 0 <= d(v) <= 14 :

* si v appartient à S, d(v) + 4 = 0 modulo 7 impose d(v) dans {3,10} ;
* sinon, d(v) = 0 modulo 7 impose d(v) dans {0,7,14}.

Introduisons les entiers non négatifs :

    u = nombre de v dans S ayant d(v) = 10 ;
    v7 = nombre de v hors de S ayant d(v) = 7 ;
    v14 = nombre de v hors de S ayant d(v) = 14.

Premier moment : somme_v d(v) = 14w. Donc

    3w + 7u + 7v7 + 14v14 = 14w,
    u + v7 + 2v14 = 11t.                         (1)

Second moment :

    somme_v d(v)^2 = x^T A² x
                   = 12w - x^T A x + 2w²
                   = 9w - 7u + 2w².

En comptant par les cinq types de sommets, le membre de gauche vaut

    9w + 91u + 49v7 + 196v14.

Ainsi

    2u + v7 + 4v14 = 2t².                       (2)

De (1) et (2), on déduit

    v7 = 2t(11-t),                              (3)
    u + 2v14 = t(2t-11).                        (4)

Si t > 0, (3) et (4) impliquent 6 <= t <= 11. De plus v7 <= 99-7t, donc

    2t² - 29t + 99 = (2t-11)(t-9) >= 0.

Il reste t dans {9,10,11}.

* t = 9. Alors v7 = 36 = 99-w, donc v14 = 0 ; (4) impose u = 63 = w. Tous les sommets de S ont dix voisins dans S, tous les autres sept.
* t = 10. Alors v7 = 20, et il n'y a que 29 sommets hors de S, donc v14 <= 9. Mais (4) exige u + 2v14 = 90, impossible car u <= 70 et u + 2v14 <= 88.
* t = 11. Alors v7 = 0 et u + 2v14 = 121. Les bornes u <= 77 et v14 <= 22 donnent une somme au plus 121, donc elles sont toutes deux saturées. Tous les sommets de S ont dix voisins dans S ; tous les sommets hors de S ont leurs quatorze voisins dans S. Le complément C est indépendant et chaque sommet de S a quatre voisins dans C.

Cela prouve l'énoncé et les équations exactes. Les réciproques résultent immédiatement des équations T x = 7(x+1) dans le cas 63, et T x = 14 1 dans le cas 77. ∎

## 3. Une réciproque particulièrement courte pour le poids 77

Supposons x dans {0,1}^99 de poids 77 et T x = 0 modulo 7. Posons y = 1-x, de poids 22. Alors T y = 4 1 modulo 7.

Toutes les coordonnées entières de T y sont non négatives et congrues à 4, donc au moins 4. Leur somme est

    1^T T y = 18*22 = 396 = 4*99.

Toutes valent donc exactement 4. Sur le support de y, cela interdit toute arête interne. Hors de ce support, cela impose quatre voisins dans celui-ci.

Ainsi, pour un éventuel SRG,

    alpha = 22
       si et seulement s'il existe x dans {0,1}^99
       de poids 77 avec T x = 0 modulo 7.

Cette réciproque n'utilise même pas l'identité quadratique : la régularité, les dimensions et la positivité des coefficients suffisent. L'identification à une coclique maximale utilise ensuite la borne de Hoffman du SRG.

## 4. Interaction entre les deux types

Si S a taille 63 et C est une coclique de Hoffman de taille 22, alors

    A(1_S - (7/11)1) = 3(1_S - (7/11)1),
    A(1_C - (2/9)1) = -4(1_C - (2/9)1).

L'orthogonalité des espaces propres distincts donne

    |S inter C| = 63*22/99 = 14.

Par conséquent H = S^c, de taille 36, vérifie |H inter C| = 8. Équivalemment, si F = C^c a taille 77, alors |S inter F| = 49.

Ce résultat ne suppose ni que S ni que C existent nécessairement.

## 5. Dimension du code des différences

Soit r = rang_F7(T), et soit Delta le code engendré par les différences de lignes b_i-b_j de T.

Chaque ligne a somme de coordonnées 18 = 4 modulo 7 ; chaque différence a somme nulle. Toute ligne s'écrit b_0 + (b_i-b_0), et b_0 n'a pas somme nulle. Ainsi

    dim Delta = r-1.

Comme T² = 2J modulo 7, tous les produits scalaires b_i.b_j valent 2. Les différences de lignes sont donc deux à deux orthogonales.

Enfin T = A-3I modulo 7, et A-3I a rang rationnel 45 (ses seules valeurs propres nulles correspondent à la valeur propre 3 de A, de multiplicité 54). La réduction modulo 7 ne peut augmenter ce rang. Donc

    r <= 45 ; dim Delta <= 44.

La borne 49 venant seulement de l'auto-orthogonalité dans F7^99 est correcte, mais beaucoup moins précise.

## 6. Portée et coordination

Lecture du dépôt : amazing-source/conway99-c1, branche claude/v7-simultaneous, révision 76fd9a53993163f99c34cdb6430de0101d12a261.

Les notes 90, 107, 172 et 173 ont été consultées pour la coordination. La note 107 décrit déjà des ensembles serrés, la note 172 décrit le noyau F7 via les réseaux propres. Le présent texte formule et démontre la classification de la section {0,1} du noyau. Il ne prétend pas classifier le noyau entier ou tous les ensembles serrés.

Ce lemme n'établit pas K7, ne ferme pas alpha = 22, n'impose pas une coclique de Hoffman, et ne fournit pas de verdict sur les recherches SAT. Le cas où la section binaire se réduit à {0} n'est pas exclu.

L'énumérateur de poids usuel sur F7 ne détecte pas la contrainte « coordonnées 0 ou 1 ». Un mot arbitraire de poids 77 ne suffit pas à identifier une coclique. Il faudrait garder les symboles ou leur signification d'incidence.
