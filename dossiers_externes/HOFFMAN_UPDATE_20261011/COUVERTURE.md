# Couverture des deux familles de designs exclues

Le théorème assisté par calcul de ce dossier porte sur le **design d'une coclique**, pas sur un groupe d'automorphismes supposé du graphe entier.

> Aucun SRG(99,14,1,2) avec une coclique de 22 sommets ne peut avoir, pour design de voisinages de cette coclique :
> 1. un design invariant par un cycle transitif de longueur 22 ;
> 2. un design invariant par un groupe de 21 éléments fixant un point et agissant régulièrement sur les 21 autres.

Dans le deuxième cas, les groupes possibles sont C21 et le groupe non abélien C7⋊C3. Ils sont traités séparément ci-dessous. Le mot « régulièrement » signifie transitivement avec stabilisateurs triviaux, pas la régularité des degrés du graphe.

## 1. Famille cyclique sur Z/22

Un bloc de quatre points sous les translations a un stabilisateur dont l'ordre divise à la fois 22 et 4. Ses orbites ont donc taille 22 ou 11.

Un bloc d'orbite 11 est une réunion de deux paires antipodales {a,a+11}. Les cinq orbites de ce type sont équivalentes par multiplication par une unité modulo 22. On peut fixer l'orbite des translates de {0,1,11,12}.

Il faut au moins une orbite courte puisque le nombre de blocs, 77, est impair. Chaque orbite courte couvre exactement deux fois chaque paire antipodale. Deux orbites courtes donneraient quatre occurrences par paire, interdites par λ_design=2. Il y en a donc exactement une. Aucun bloc d'une orbite longue ne peut contenir de paire antipodale.

Il reste exactement trois orbites longues : 77=11+3·22.

Pour les distances non orientées d=1,...,10, l'orbite courte contribue une fois à d=1 et d=10, et zéro ailleurs. Les trois blocs de base longs doivent donc avoir pour somme de leurs vecteurs de distances

    (1,2,2,2,2,2,2,2,2,1).

Une différence dans un bloc de base long contribue une occurrence à chaque paire de cette distance dans l'orbite développée. La cible ci-dessus est donc exacte, pas un filtre heuristique.

`cyclic_designs.py` parcourt toutes les C(22,4) parties, construit leurs orbites et choisit toutes les combinaisons possibles de trois orbites longues. Il obtient :

- 330 orbites longues au départ ;
- 190 admissibles au quota de distances ;
- 80 sélections normalisées donnant un 2-(22,4,2) ;
- 8 sélections impossibles pour un SRG, car deux blocs se rencontrent en trois points ;
- 72 designs restants, tous exclus par les domaines de voisinages et leur compatibilité.

Ces 72 sont des designs normalisés étiquetés, **pas 72 classes d'isomorphisme**. Aucun quotient par le groupe complet du design n'est prétendu.

## 2. Action régulière de C21 sur 21 points, avec un point fixe

Écrivons les points comme C21∪{∞}. Les blocs contenant ∞ correspondent à des triples de points finis. Leurs orbites ont taille 21 ou 7. Le point ∞ appartient exactement à 14 blocs, donc seules deux orbites de taille 7 peuvent être utilisées.

Une telle orbite est formée des cosets d'un sous-groupe d'ordre trois, auxquels on ajoute ∞. C21 possède un seul sous-groupe d'ordre trois, donc une seule orbite courte possible. On devrait la répéter ; des blocs répétés se rencontreraient en quatre points et sont impossibles dans le design issu d'un SRG.

**Cette famille est exclue sans calcul.**

## 3. Action régulière du groupe non abélien C7⋊C3, avec un point fixe

Les 21 points finis sont les couples (a,i)∈F7×Z3, avec

    (a,i)(b,j)=(a+2^i b, i+j).

Le point supplémentaire est ∞. Comme ci-dessus, ses 14 blocs sont exactement deux orbites courtes de taille sept. Le groupe possède sept sous-groupes d'ordre trois, engendrés par (a,1). Les automorphismes

    (x,i) ↦ (u x + b(1−2^i),i),  u≠0,

agissent sur ces sept sous-groupes par toutes les transformations affines a↦u a−b, donc transitivement sur les paires ordonnées distinctes. On peut fixer les deux sous-groupes correspondant à a=0 et a=1, sans perdre aucun design.

Ces orbites courtes sont les translates de

    {∞,(0,0),(0,1),(0,2)},
    {∞,(0,0),(1,1),(3,2)}.

Les autres blocs évitent ∞. Leur stabilisateur est trivial : son ordre doit diviser 21 et 4. Ils forment donc trois orbites de taille 21, puisque 77−14=63.

Il existe dix orbites de paires non ordonnées de points finis. Chaque orbite contient 21 paires. Elles sont indexées par les différences g^{-1}h, à inversion près. Chacune des deux orbites courtes couvre entièrement une de ces dix classes de paires. La cible résiduelle pour les trois orbites longues est donc de multiplicité un sur ces deux classes et deux sur les huit autres.

`one_rotational_designs.py` énumère les 285 orbites de parties de quatre points finis, les 222 qui respectent les quotas, puis toutes les triples d'orbites correspondantes. Il obtient :

- 236 sélections normalisées donnant un 2-(22,4,2) ;
- 37 impossibles à cause d'une intersection de trois points ;
- 199 designs restants, tous exclus ; douze ont déjà un domaine de ligne vide, les autres meurent à la propagation de compatibilité.

Là encore, **199 n'est pas un nombre de classes d'isomorphisme**. Ces designs peuvent recouper des types présents dans l'autre famille ; les résultats portent sur la couverture, pas sur une addition de classes distinctes.

## 4. Audit séparé du catalogue

`verify_catalogues.py` ne reprend pas les vecteurs de différences. Il développe toutes les orbites et compte directement les occurrences des **231 paires de points**, puis recherche les trois orbites complétant le vecteur des 231 quotas.

Il retrouve exactement les mêmes 80 et 236 sélections, les mêmes 8 et 37 rejets pour intersection trois, et exactement les mêmes matrices d'incidence restantes.

## 5. Pourquoi les symétries du design ne sont pas imposées au graphe

Dans les 271 instances, chacune des 77 lignes de D a son domaine propre. On n'impose jamais D_{gi,gj}=D_{ij}, même lorsque g préserve le design.

Les translations du design servent uniquement à normaliser les entrées et, dans le second vérificateur, à transporter des **ensembles complets de possibilités de lignes**. Cette opération dit que les domaines sont bijectifs ; elle ne dit pas que deux lignes choisies dans une complétion doivent être images l'une de l'autre.

Un graphe asymétrique complétant l'un de ces designs serait donc bien présent dans le problème testé. Il est exclu par les équations de voisins communs, pas éliminé par une contrainte d'invariance.

## 6. Ce qui reste hors couverture

Les designs 2-(22,4,2) sans l'une des actions précises ci-dessus ne sont pas classifiés ni exclus. Cela comprend en particulier les designs asymétriques et de nombreuses actions de groupes plus petites ou différentes. Aucune preuve n'est donnée que toute coclique de Hoffman devrait appartenir à nos familles.

Les résultats n'impliquent donc ni α(Γ)≤21 en général, ni une exclusion de C1, ni une exclusion d'un rang modulo sept. Ils ferment deux classes explicitement définies de bords dans le sous-cas α=22.
