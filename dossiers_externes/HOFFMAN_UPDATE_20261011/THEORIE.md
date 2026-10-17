# Cocliques de Hoffman : équations, complétions et symétries

11 octobre 2026. Note mathématique produite pendant la mise à jour sur la note 171 du dépôt `amazing-source/conway99-c1`.

## 1. Le problème exact à 99

Supposons qu'un graphe Γ de paramètres (99,14,1,2) possède une coclique C de 22 sommets. La borne spectrale de Hoffman vaut 22. Son cas d'égalité donne exactement quatre voisins dans C à chaque sommet de F=V\C.

Pour ne pas dépendre d'une citation du cas d'égalité, voici la preuve. Soit x=1_C et z=x−(22/99)1. L'identité SRG impose les valeurs propres 14, 3, −4. Comme C est indépendante, xᵀAx=0. Un calcul donne zᵀ(A+4I)z=0. La restriction de A+4I à 1^⊥ est positive semi-définie, donc (A+4I)z=0. Par conséquent (A+4I)x=4·1. Les coordonnées hors de C disent que chacune a quatre voisins dans C.

Ordonnons Γ sous la forme

    A = [ 0   Y ]
        [ Yᵀ  D ].

Y est une matrice binaire 22×77, de sommes de lignes 14 et de colonnes 4. Ses colonnes sont les blocs B_i d'un 2-(22,4,2). Deux colonnes distinctes se rencontrent en au plus deux points : sinon les deux sommets correspondants auraient au moins trois voisins communs. Les colonnes sont donc distinctes.

Les équations exactes sont :

    YYᵀ = 12I₂₂ + 2J₂₂,
    YD  = 2J₂₂,₇₇ − Y,
    D² + D = 12I₇₇ + 2J₇₇ − YᵀY,
    D1 = 10·1.

Avec Y,D binaires, D symétrique et sans boucle, elles sont équivalentes au SRG. Le coefficient **12** est nécessaire : le premier produit a diagonale 14. Le coefficient 18 donné dans une précédente réponse était erroné ; la note 171 du dépôt emploie correctement 12.

Pour un bloc B, notons n_j le nombre des autres blocs l'intersectant en j points. Les équations n_0+n_1+n_2=76, n_1+2n_2=4·13 et n_2=C(4,2)=6 donnent

    (n_0,n_1,n_2)=(30,40,6).

Les nombres globaux de paires sont donc (1155,1540,231). Ils ne sont pas des nouveaux résultats de cette note : ils sont déjà dans la note 171.

## 2. Domaines exacts de voisinages et règle de réfutation

Fixons le design Y, mais absolument aucune adjacency entre ses 77 blocs. Un candidat R_i pour le voisinage dans F du bloc B_i satisfait :

1. R_i est un ensemble de dix indices distincts ne contenant pas i.
2. Chaque point de B_i est couvert une fois par les blocs de R_i ; chacun des dix-huit autres points l'est deux fois.
3. Chaque bloc de R_i rencontre B_i en au plus un point. Sinon une arête aurait deux voisins communs dans C.
4. Deux blocs distincts de R_i se rencontrent en au plus un point. Ils ont déjà i pour voisin commun dans F et ne peuvent en avoir deux autres dans C.

Ces quatre conditions sont nécessaires. Elles ne prétendent pas qu'un seul candidat se prolonge à lui seul en graphe.

Deux candidats R_i,R_j peuvent coexister exactement si

    [j∈R_i]=[i∈R_j],
    |R_i∩R_j| + |B_i∩B_j| = 2−[j∈R_i].             (P)

Sélectionner un candidat dans chaque domaine en satisfaisant (P) pour toutes les paires donne toutes les équations du paragraphe 1. La diagonale de la dernière équation est automatique puisque |R_i|=10 et |B_i|=4.

**Règle sûre.** Si un candidat R_i n'a aucun partenaire compatible dans le domaine actuel d'une autre ligne j, il ne peut appartenir à aucune complétion. Le retirer ne supprime aucune solution. Si un domaine devient vide, aucune complétion n'existe.

Les certificats enregistrent chaque suppression comme (i, numéro du candidat, j). Le relecteur recalcule directement toutes les comparaisons (P) encore possibles ; il n'utilise pas les tables de compatibilité du constructeur.

## 3. Ce que la symétrie d'un design implique — et n'implique pas

Soit H le groupe des permutations des points et des blocs préservant Y. Il agit sur l'ensemble X(Y) des complétions par D↦QDQᵀ, où Q est la permutation des blocs.

**Lemme de prolongement.** Le stabilisateur dans H d'une complétion D est exactement le groupe des automorphismes du graphe complété qui préservent la coclique C comme ensemble.

Preuve : la permutation conserve 0 et Y par définition de H. Elle conserve le dernier bloc si et seulement si QDQᵀ=D. C'est exactement conserver toute A. Réciproquement, tout automorphisme préservant C fournit une telle permutation d'incidence.

Conséquences :

- si la complétion est unique, tous les automorphismes du design se prolongent ;
- si H est non trivial et qu'une complétion unique existe, le graphe n'est pas asymétrique ;
- avec plusieurs complétions, les automorphismes de Y peuvent les échanger plutôt que stabiliser chacune ; ils ne se prolongent alors pas automatiquement ;
- les complétions dont le graphe est asymétrique forment des orbites libres sous H. Leur nombre étiqueté est donc un multiple de |H|.

Le stabilisateur de C peut être trivial sans que le groupe complet du graphe soit trivial : un automorphisme peut envoyer C sur une autre coclique. Aucune réciproque injustifiée n’est utilisée.

Ce lemme explique pourquoi une structure de bord symétrique peut produire un graphe asymétrique. Il explique aussi exactement ce qu'apporte la rigidité annoncée pour le design précis de BvLS : **unicité de la complétion + symétrie du design**, et non la seule présence d'une coclique de Hoffman.

## 4. Contre-exemple vérifié à l'inférence « Hoffman exclut l'asymétrie »

Le témoin du dossier Paley précédent est un SRG(25,12,5,6). Les comptes de K4 et K5 par sommet, puis le raffinement par les couleurs des voisins, produisent 5,16,22,25 couleurs distinctes. Ces invariants sont préservés par tout automorphisme ; 25 classes singletons prouvent que le groupe est trivial.

L'énumération de tous les 53 130 sous-ensembles de cinq sommets donne exactement trois cocliques :

    {1,9,11,13,20}, {3,6,12,15,24}, {4,7,10,18,21}.

Pour chacune, (A+3I)1_C=3·1. Ce sont donc des cocliques de Hoffman, de taille 25·3/(12+3)=5, dans un graphe asymétrique.

Plus directement encore, complémentons la transformation connue de Paley, qui gardait un K5 et toutes ses incidences. Le complément de ce K5 est une coclique de Hoffman de cinq sommets. Les graphes avant et après transformation ont **le même bord complet**, c'est-à-dire la même coclique et exactement les mêmes incidences avec ses vingt sommets extérieurs. Le premier est isomorphe à Paley(25) ; le second est asymétrique, car complémenter ne change pas le groupe d'automorphismes.

Le bord commun est

    C={4,8,12,16,20}.

Ses vingt blocs sont de taille trois, chaque point apparaît douze fois, chaque paire six fois : c'est un 2-(5,3,6), avec chaque triple répété deux fois. Les deux matrices et l'isomorphisme explicite identifiant le graphe initial au complément de Paley sont fournis.

Cela ne classe pas les graphes à 243 sommets. Cela réfute l'inférence générale selon laquelle une coclique de Hoffman, ou même ses incidences complètes fixées, empêcherait l'asymétrie. À 243, la note 171 a traité un design déterminé, pas tous les 2-(45,5,2).

## 5. Une forme de Gram utile, sans nouvelle exclusion spectrale revendiquée

Posons N=YᵀY. Les équations donnent N²=12N+32J et DN=ND=8J−N. Le spectre de D est

    10¹, (−1)²¹, 3³³, (−4)²².

Ce spectre figurait déjà dans l'annexe de la note 104. La matrice entière

    Q=9I−3D−N+J

satisfait

    Q²=21Q,   QYᵀ=0,   Q1=0,   diag(Q)=6.

Elle est positive semi-définie, de rang 22. Les valeurs hors diagonale sont −3 (arête mate), −2 (arête entre blocs disjoints), −1 (non-arête et intersection deux), 0 (non-arête et intersection un), 1 (non-arête et intersection zéro).

Cette reformulation relie exactement le design et la complétion à un Gram entier. Elle n'est pas utilisée pour les exclusions finies du présent dossier et aucune contradiction universelle n'en est déduite.

## 6. Vérification du découpage A/B de Claude

Son générateur normalise le voisinage du point 0 de la coclique en sept paires mates. Les blocs22 et23 sont donc adjacents et se rencontrent exactement en {0}. Leurs autres points peuvent être étiquetés {1,2,3} et {4,5,6}.

La paire de points {0,1} est contenue dans exactement un autre bloc, noté24 après renommage des six autres paires mates du voisinage de 0. Écrivons-le {0,1,a,b}. Il ne peut contenir 2 ou3 : l'intersection avec le bloc22 aurait au moins trois points. Il ne peut contenir deux points de {4,5,6}, pour la même raison avec23.

Il reste exactement deux formes, à renommage permis près : {0,1,4,7} et {0,1,7,8}. Le découpage A/B est donc couvrant. Pour conclure à l'exclusion générale α=22 à partir de ce découpage, il faut réfuter les deux branches (ou la formule de base entière), avec une couverture valide des sous-branches éventuelles.
