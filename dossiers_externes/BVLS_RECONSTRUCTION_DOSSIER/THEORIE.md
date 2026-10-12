# Modèle exact et couverture

## 1. Une seule matrice, un bord fixe

Soit A0 l'adjacence d'un SRG(243,22,1,2), et V=S ⊔ F. On fixe les blocs C=A0[S,S] et Y=A0[S,F]. Le seul bloc inconnu est D sur F :

    A = [ C   Y ]
        [ Y^t D ].

L'identité A²+A=20I+2J donne exactement

    YD = 2J - Y - CY,
    D²+D = 20I+2J-Y^tY,
    D1 = 22·1-Y^t1.

Les équations sur S×S et les degrés de S sont déjà vrais puisqu'ils ne dépendent pas de D. Pour une ligne i de D, on énumère tous les vecteurs binaires d_i tels que

    d_i(i)=0,
    1^t d_i=22-1^tY_i,
    Yd_i = 2·1-Y_i-CY_i.

On utilise de plus la condition nécessaire suivante : deux voisins j et k de i ne peuvent déjà avoir deux voisins communs dans S. Sinon ils auraient ces deux sommets et i comme voisins communs. Ainsi deux indices sélectionnés dans d_i vérifient `(Y^tY)[j,k] ≤ 1`.

Pour deux lignes choisies, les contraintes restantes sont

    d_i(j)=d_j(i),
    d_i·d_j+(Y^tY)[i,j]=2-d_i(j).

Elles sont nécessaires et suffisantes, avec les contraintes de ligne, pour obtenir une matrice SRG. La contrainte additionnelle de domaine est redondante dans tout SRG final; elle ne perd donc aucune complétion.

## 2. Exhaustivité de l'énumérateur de lignes

`rows.cpp` est un exact-cover à capacités. Il maintient les coordonnées déjà sélectionnées, les candidats restants, les quotas r_s et le nombre de voisins à choisir.

Pour une équation non saturée s, il énumère **tous** les sous-ensembles de taille r_s parmi ses candidats restants (ici r_s vaut 1 ou 2), les ajoute, puis retire les autres candidats de cette équation. Les budgets sont mis à jour en entiers. Chaque solution doit choisir exactement un de ces sous-ensembles et suit donc une branche unique.

Les suppressions sont exclusivement dues à un quota nul, un quota dépassé, une capacité insuffisante, la diagonale interdite ou la condition de voisins communs du §1. Quand les quotas sont tous nuls mais des colonnes nulles subsistent, le code conserve un branchement binaire complet. Ce dernier cas n'intervient pas dans le résultat principal.

Une limite de temps ou de nombre de solutions donne STOPPED; un tel domaine n'est pas accepté comme complet par `prepare_csp.py` ou `assemble.py`. Les cinq domaines utilisés dans le théorème ont le statut EXHAUSTED.

## 3. Transport des domaines

Le BvLS de référence est reconstruit à partir de la matrice génératrice ternaire du fichier `code/asym243/golay.py` du dépôt. Le fichier d'arêtes ainsi obtenu possède exactement le blob Git `cfc398cea8d6d75905f1db06f264607abd9c2b68`.

Les sommets sont F3^5, avec 22 différences de connexion ±h_i. `cap_aut.cpp` énumère les applications linéaires inversibles préservant ces différences : 15 840 matrices. Il suffit de vérifier leurs images sur les 22 différences pour vérifier l'automorphisme sur tout le graphe de Cayley. L'utilisation de ce groupe concerne le **graphe source**, pas une symétrie exigée des reconstructions.

Parmi les applications affines construites, 4 320 préservent T={0,1,2}. Le sous-groupe qui préserve l'union des deux prismes choisis contient les 96 applications utilisées pour transporter les domaines. Les cinq orbites sur F ont tailles 12,12,48,96,24.

Pour chaque ligne transportée, le certificat donne une permutation qui préserve A0 et les ensembles S et F. Elle permute également les équations et leurs seconds membres; elle donne donc une bijection entre les deux domaines complets.

## 4. Réduction partielle des renommages

Deux sommets libres qui ont le même profil vers S et la même histoire d'adjacence aux lignes déjà fixées sont interchangeables dans l'état partiel. Cet échange ne doit pas être un automorphisme de la complétion.

Au moment de choisir la ligne i, on exclut i de ces classes, ainsi que tous les sommets déjà fixés. Sur chaque classe restante de taille m, on conserve seulement le motif ayant d'abord ses k uns puis ses m-k zéros. Tout autre choix de k voisins se ramène à celui-ci par une permutation préservant le bord et les lignes antérieures. Le poids est multiplié par binom(m,k).

Après la décision, les classes sont raffinées par le nouveau bit d'adjacence. Aucune permutation qui déplacerait une ligne fixée n'est supprimée par cette règle.

`complete.cpp` combine cette réduction avec les compatibilités exactes du §1. `complete_noquotient.cpp` supprime intégralement cette réduction et retrouve les 27 648 feuilles. Cette seconde passe contrôle le décompte pondéré sans faire appel aux facteurs d'orbites.

Dans la frontière principale, les seuls profils initiaux répétés sont trois groupes de quatre sommets parmi les douze libérés. Les autres profils sont tous distincts. La classification finale comporte une orbite libre de `(S4)^3` pour chacun des deux graphes, d'où le facteur `(4!)^3=13 824`, également vérifié directement.

## 5. Non-asymétrie certifiée

Les deux feuilles représentatives sont identifiées à BvLS et au jumeau par des permutations explicites, vérifiées sur les 29 403 paires. Ce ne sont pas de simples comparaisons de spectres ou de nombres de grilles.

Dans les coordonnées de référence, la translation qui ajoute 1 à la dernière coordonnée de F3^5 est un automorphisme d'ordre trois de chacun des deux graphes; cette assertion est vérifiée sur leurs matrices. Conjuguer cet automorphisme par l'isomorphisme fournit un automorphisme d'ordre trois de la feuille, puis de chacune de ses copies étiquetées. Il est non trivial et sans point fixe.

## 6. Extension à tous les triangles et aux deux prismes quelconques

Les 891 triangles sont parcourus et chacun reçoit un transport depuis T. Les 45 unions de deux parmi les dix prismes voisins de T reçoivent un transport qui fixe T ensemblistement.

Composer ces deux transports couvre tout choix annoncé dans le théorème. Aucune classification complète du groupe d'automorphismes n'est nécessaire : les applications explicitement exhibées suffisent à la couverture.

Les 891×45 objets comptés sont des choix (triangle, paire de prismes); on n'affirme pas que leurs problèmes sont indépendants ou qu'ils couvrent tous les graphes à 243 sommets.

Le même contrôle donne 360 transports pour trois paires mates dans une couche du voisinage de T. Le résultat Gamma3 n'est pas étendu à d'autres triangles sans certificat de transport approprié.
