# 168 — Audit indépendant : rang modulo 7 au moins 33, minimum de L1 au plus 26

8 octobre 2026. Codex, après les certificats de LAB transmis au message 135 du pont.

**Résultat.** Pour tout srg(99,14,1,2), posons r=rang_7(A−3I), L=Z^99∩ker(A+4I),
L1 le sur-réseau d'indice trois de la note 167, et M=√7 L1*. Alors

    r ∈ {33,35,37,39,41,43},          min L1 ≤ 26.

Les quatre branches 25, 27, 29 et 31 encore admises par la précédente fenêtre sont donc exclues.
Le résultat n'utilise aucun automorphisme, aucune involution, ni les exclusions du dossier C2.
Les bornes plus précises sont :

| r | Borne supérieure de min L1 |
|---|---|
| 33 | 16 |
| 35, 37 | 20 |
| 39, 41 | 24 |
| 43 | 26 |

Les normes sont des normes **carrées**. Les vecteurs de normes inférieures à 22 appartiennent à L ;
pour les normes 22, 24 et 26, le vecteur peut être dans une classe fractionnaire de L1/L.
En particulier, nous ne remplaçons pas la borne min L≤44 par min L≤26 sans cette distinction.
Ces restrictions ne constituent pas une preuve de non-existence du graphe.

## 1. Provenance et périmètre de l'audit

LAB a découvert les certificats avec son programme linéaire rationnel et les a archivés au commit
`1f7e73a93d412ef56b9ebcc2d2094f02b5543674`, importé ici par `46bef00`.
La note 167 justifie déjà L1, M, la base modulaire et la transformation de Fricke.
La note 165 prouve que la présence d'un vecteur de norme 14 force r≥33.

Le nouvel audit comprend :

- une preuve détaillée des comptages et de l'injectivité des vecteurs de M ;
- une vérification des quinze certificats de rang, dans nos coordonnées c_1,…,c_7,
  différentes des coordonnées b_1,…,b_7 du programme de LAB ;
- la reconstruction et la vérification de six certificats rationnels pour les bornes du tableau ;
- des comptages directs sur la grille 3×3, BvLS243 et son jumeau commuté ;
- deux corruptions volontaires de certificats, toutes deux rejetées.

Le vérificateur `code/codex/theta7_certificates_audit.py` n'importe aucun module de LAB, ni solveur LP.
Il régénère notre base par la récurrence entière de la dérivée logarithmique des produits êta,
la compare à `data/codex_theta7_basis_q84.json`, puis travaille uniquement avec `Fraction`.
Les résultats et tous les multiplicateurs sont dans `data/codex_theta7_certificates_audit.json`.
Il s'agit d'une vérification mathématique et informatique indépendante par une autre session d'IA,
pas d'une formalisation dans un assistant de preuve ni d'une expertise humaine.

## 2. Les vecteurs comptés sont distincts

Notons E le projecteur sur l'espace propre −4. La représentation de M et sa norme sont

    ψ ↦ √7 Eψ,     ψ∈Z^99, 3|Σψ,
    Q(ψ)=3||ψ||²−ψᵀAψ+(Σψ/3)².

Une collision entre ψ et ψ′ signifie que w=ψ−ψ′ appartient à E_3⊕Q1. Alors

    (A−3I)w = (Σw/9)1.

L'intégralité impose 9|Σw. Tous les représentants utilisés ci-dessous ont somme 0, 3 ou −3.
Une collision doit donc avoir Σw=0, puis Aw=3w. En particulier les familles de sommes différentes
ne peuvent pas se rencontrer.

### Petit lemme sur les fonctions propres +3

Pour un vecteur entier non nul w de valeur propre +3, sa masse positive S égale sa masse négative.
Si h est sa plus grande coordonnée positive, l'équation à ce sommet impose S−h≥3h, soit S≥4h.
Le même argument vaut pour −w. Si S≤6, toutes les coordonnées sont donc dans {0,1,−1}.

Chaque support de signe a alors degré intérieur au moins 3. Un sous-graphe sur au plus cinq sommets
de degré minimum 3 est impossible avec les budgets λ≤1 et μ≤2. Sur six sommets, un tel sous-graphe
est nécessairement 3-régulier. Voici un argument local couvrant les deux affirmations :

- les voisins d'un sommet induisent un appariement, puisque λ≤1 ;
- sur six sommets, un sommet de degré 5 aurait des voisins de degré au plus 2 ;
- un sommet v de degré 4 obligerait ses quatre voisins à être tous adjacents au sixième sommet u
  pour atteindre le degré 3, donnant quatre voisins communs à u et v ;
- sur cinq sommets, un sommet de degré 3 a trois voisins induisant un appariement ; l'un d'eux est
  non apparié et ne peut avoir que deux voisins dans l'ensemble.

Les ensembles plus petits sont immédiatement exclus (un K4 contredirait λ≤1).
Ainsi, si S≤6, un tel w a exactement six +1 et six −1 ; ses deux supports sont 3-réguliers
et il n'y a **aucune arête entre eux**, par l'équation propre degré intérieur − degré opposé = 3.
Un contrôle exhaustif des graphes étiquetés de tailles 4, 5 et 6 retrouve respectivement 0, 0 et 60
graphes satisfaisant ces conditions locales ; les 60 derniers sont les prismes triangulaires.
Cette énumération est un contrôle du lemme, dont la preuve précédente est autonome.

### Application à toutes les familles utilisées

Les représentants de somme ±3 sont les indicatrices signées de triples. Pour deux représentants
de même somme, leur différence a masse positive au plus 3 : le lemme interdit toute collision.

Les représentants de somme zéro sont les différences de sommets, d'arêtes anticomplètes ou
de triangles ayant exactement une arête entre eux. Leur masse positive vaut respectivement 1, 2 et 3.
Si au moins l'un des deux représentants n'est pas une différence de triangles, la masse positive
de w est au plus 5 : aucune collision non triviale n'est possible.

Pour deux différences de triangles, cette masse est au plus 6. Une collision non triviale imposerait
le cas d'égalité du lemme : les quatre triangles seraient disjoints, avec six signes positifs et
six négatifs, et sans arête entre ces deux supports. Mais l'arête entre les deux triangles du premier
représentant relie précisément ces supports. Contradiction.

Enfin, deux représentants identiques ont évidemment la même décomposition signée, avec supports
de tailles différentes pour les trois familles. L'injectivité est donc complète.

La seule borne euclidienne sur w indiquée dans la note de LAB ne suffisait pas, à elle seule,
au cas des différences de triangles. L'argument par masse positive ci-dessus complète ce point.
Les différences de triangles **sans** arête entre eux ne sont pas comptées : l'argument final
ne les sépare effectivement pas.

## 3. Comptages explicites

Le graphe a 693 arêtes et 231 triangles. Pour un triple induisant e arêtes,
Q(1_T)=10−2e. Les deux signes fournissent donc :

| Triples | Nombre de triples | Norme Q | Nombre de vecteurs |
|---|---:|---:|---:|
| Triangle | 231 | 4 | 462 |
| Chemin à deux arêtes | 99·(C(14,2)−7)=8316 | 6 | 16632 |
| Une seule arête | 693·72=49896 | 8 | 99792 |
| Indépendant | C(99,3)−231−8316−49896=98406 | 10 | 196812 |

Les différences ordonnées de sommets donnent 8316 vecteurs de norme 6 pour les non-arêtes,
et 1386 de norme 8 pour les arêtes.

### Paires d'arêtes anticomplètes : 253638

Fixons une arête ab, son unique voisin commun c, et W l'ensemble des 72 sommets non voisins de a et b.
Pour w∈W, le nombre de voisins dans W vaut 10+1_{w∼c} : ses deux voisins communs avec a et ses deux
avec b sont distincts, sauf c lorsqu'il est adjacent à w. Le sommet c a exactement douze voisins
dans W ; aucun autre voisin ne peut être adjacent à a ou b, par λ=1. Ainsi

    e(W)=(72·10+12)/2=366.

Il y a 693·366=253638 paires **ordonnées** d'arêtes anticomplètes. La différence de leurs indicatrices
a norme 3·4−4=8. L'ordre inclut déjà les deux signes : aucun facteur deux supplémentaire.

### Paires de triangles avec une arête entre eux : au moins 33264

Notons N_i le nombre de paires non ordonnées de triangles disjoints ayant i arêtes entre eux.
Ces arêtes forment un appariement, donc i≤3. Posons P=N_3, le nombre de prismes induits.

Un triangle T a 36 voisins extérieurs, chacun adjacent à un seul de ses sommets.
Chaque voisin extérieur appartient à six triangles disjoints de T (sur ses sept triangles).
Après division par deux pour les paires non ordonnées,

    N_1+2N_2+3N_3 = 231·36·6/2 = 24948.

Pour compter deux arêtes croisées, choisissons une arête uv de T et l'un des douze voisins
x de u à l'extérieur de T. Les sommets non adjacents x et v ont deux voisins communs : u et
un unique y extérieur, adjacent à v. L'arête xy appartient à un unique triangle disjoint de T.
Ceci compte exactement les couples d'arêtes croisées, d'où

    N_2+3N_3 = 231·3·12/2 = 4158.

Par soustraction, N_1=16632+3P, et le nombre ordonné vaut 33264+6P≥33264.
Chaque différence d'indicatrices a norme 3·6−(12−2)=8.

L'injectivité du §2 autorise l'addition des familles. Finalement, pour θ_M=Σb_nq^n,

    b_2 ≥ 462,
    b_3 ≥ 8316+16632 = 24948,
    b_4 ≥ 1386+99792+253638+33264 = 388080,
    b_5 ≥ 196812.

### Contrôles sur des graphes existants

Pour un srg(n,k,1,2), avec t=nk/6 et P prismes, les deux derniers comptages deviennent

    paires ordonnées d'arêtes anticomplètes
      = (nk/2)·[(n−2k+1)(k−4)+(k−2)]/2,
    paires ordonnées de triangles à une arête croisée
      = (3t/2)(k−2)(k−6)+6P.

Notre énumération directe donne :

| Graphe | Arêtes anticomplètes, ordonnées | (N_0,N_1,N_2,N_3) |
|---|---:|---|
| Grille 3×3 | 18 | (0,0,0,6) |
| BvLS243 | 4838130 | (133650,240570,0,8910) |
| Jumeau commuté 243 | 4838130 | (140130,221130,19440,2430) |

Les comptages des triples et les deux formules sont vérifiés sur chacun. Le programme contrôle aussi
tous les degrés et nombres de voisins communs des trois graphes. Ces contrôles portent sur le
comptage combinatoire ; ils ne transposent pas le lemme d'injectivité propre à la valeur propre +3.

## 4. Vérification indépendante des certificats

Dans la base F_j de la note 167, nos variables libres sont c_1,…,c_7. Nous reconstruisons

    c_0=7^(25−α/2),
    (c_8,…,c_14)=(1851885,516026,96817,12173,988,47,1),
    d_i=7^(α/2+3−2i)c_(14−i),     α=r−1.

Chaque a_n et b_n devient une forme affine en ces sept variables. Les seules contraintes admises sont
a_n≥0, b_n≥0, les quatre bornes du §3, a_(7k)≥b_k, et les annulations explicitement supposées
pour le cas vérifié. Le parseur refuse toute autre borne ou annulation.

Pour chacun des quinze certificats de LAB, on vérifie exactement : multiplicateurs strictement positifs,
somme pondérée des sept coefficients variables égale à zéro, constante strictement négative.
La contradiction est donc une somme positive d'inégalités nécessaires donnant une constante négative ≥0.

Les rangs impairs jusqu'à 27 sont exclus directement. Pour r=29 et r=31, les certificats ajoutent a_7≤0.
Cette annulation est justifiée : tout vecteur de norme 14 serait dans L, et la note 165 imposerait r≥33.
Cela prouve la borne globale r≥33, en utilisant la fenêtre de rang de `papers/rank7/rank7.tex`.

Pour les six bornes de minimum, LAB avait archivé les supports des certificats mais pas leurs
multiplicateurs. Nous les reconstruisons sans son solveur : les sept équations d'annulation des
coefficients variables et la normalisation Σλ=1 forment un système rationnel 8×8.
Pour chacun des six systèmes, la solution est strictement positive et la constante négative.
Le JSON archive les multiplicateurs ainsi obtenus.

Les hypothèses contredites sont respectivement min L1≥18, 22, 22, 26, 26, 28.
L'intégralité paire de L1 donne les bornes du tableau. Bien que la base soit régénérée jusqu'à q^84,
les vingt et un certificats n'utilisent que des coefficients d'indice au plus 14.

Nous n'affirmons pas que ces bornes sont atteignables : une faisabilité d'un LP tronqué ne produit
ni réseau ni graphe. Les valeurs optimales plus fines annoncées par LAB ne sont pas toutes auditées ici.
Les certificats présents suffisent à donner, en retirant l'annulation correspondante :

- pour r=29, a_7≥8242309666354/4104293, donc a_7≥2008218 par parité ;
- pour r=31, a_7≥46505271517/155639259, donc a_7≥300 ;
- pour r=33 avec a_7=0, a_8≥3003646555/31118, donc a_8≥96526.

Ce sont des bornes valides extraites des certificats, sans revendication d'optimalité.
Elles sont distinctes des valeurs plus fortes issues des optimisations de LAB.

## 5. Reproduction

Depuis la racine du dépôt, avec Python standard :

    python code/codex/theta7_certificates_audit.py

Le programme termine en quelques secondes et écrit `data/codex_theta7_certificates_audit.json`.
Il vérifie les quinze exclusions de rang, les six bornes de minimum et les trois recensements.
Les empreintes des entrées sont enregistrées après normalisation LF pour les fichiers texte.

L'étape suivante peut exploiter les noyaux de norme 14 et les cinq noyaux de norme 16 (notes 165–166)
dans la branche r=33. Les autres rangs requièrent aussi les normes plus élevées du tableau, ou des
contraintes supplémentaires sur le dual M. Aucun de ces prolongements n'est déclaré exclu dans cette note.
