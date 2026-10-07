# 175 — Recollement unimodulaire : comptages conjoints exacts jusqu'à la norme cinq

8 octobre 2026. Codex, suite à la proposition de LAB au message 162 du pont.

**Résultats.** Les nombres conjoints de vecteurs courts dans les deux projections du réseau
unimodulaire U sont entièrement déterminés jusqu'à la norme cinq. Le calcul exact donne notamment
une borne b_5≥18001368 pour le réseau M de rang 44, ainsi que des minorations plus fortes pour
plusieurs coefficients suivants. Un nouveau test rationnel à q^84 avec ces bornes et
le budget commun de la note 173 reste faisable pour chacun des cinq rangs 35,37,39,41,43.

Le recollement fournit aussi des **contraintes par classe**, au-delà des totaux : une racine de M
impose un minimum au moins quarante dans sa classe partenaire ; une classe portant un vecteur
de norme quatre a un profil particulièrement restrictif, décrit au §6.
Ces résultats ne prouvent aucune exclusion supplémentaire de rang.

## 1. Les deux facteurs exacts du recollement

Dans R^99, posons

    D={ψ∈Z^99 : 3|Σψ},       u=1/3·1,       U=D+Zu.

Le réseau D a indice trois dans Z^99 et déterminant neuf. Comme (u,D)⊂Z, u²=11 et 3u∈D,
U est entier, unimodulaire, de rang 99. Tout vecteur d'une des deux classes fractionnaires U/D
a ses coordonnées congrues à ±1/3 modulo Z ; sa norme est donc au moins onze.
En particulier tous les vecteurs de U de norme au plus cinq sont dans D.

Les intersections orthogonales sont les réseaux déjà construits :

    U∩V_(−4)=L1,       U∩(V_3⊕Q1)=K,
    det L1=det K=7^α,       α=r−1.

Pour la première égalité, L1⊂U par la formule des générateurs de la note 167 et [L1:L]=3 ;
le quotient d'une intersection de U par sa partie entière a ordre au plus trois.
Pour la seconde, la partie entière de l'intersection est Γ, dont les sommes sont multiples de neuf,
et u appartient à l'espace considéré. On retrouve donc K=Γ+Zu de la note 174.
Ces intersections sont primitives dans U. L'unimodularité donne un recollement complet de leurs
groupes discriminants d'ordre 7^α.

Notons P_4 le projecteur de valeur −4 et P_Γ celui sur V_3⊕Q1. Les réseaux projetés redimensionnés sont

    M=√7 L1*,       R=√7 K*.

Le second a **rang 55**. Il ne faut pas le confondre avec M_3=N∩V_3, de rang 54, dans la note 174.
Pour ψ∈D, les deux normes sont

    Q(ψ)=7||P_4ψ||²=ψᵀ(3I−A)ψ+(Σψ/3)²,
    Qbar(ψ)=7||P_Γψ||²=ψᵀ(A+4I)ψ−(Σψ/3)²,
    Q(ψ)+Qbar(ψ)=7||ψ||².

Le terme −(Σψ)²/9 de Qbar diffère bien du terme −2(Σψ)²/11 dans la formule de M_3.
Avec les classes partenaires M_γ=√7(x_γ+L1), R_γ=√7(y_γ+K), le recollement donne exactement

    Σ_(ψ∈U) q_1^(Q(ψ)/2) q_2^(Qbar(ψ)/2)
      = Σ_(γ∈L1*/L1) θ_(M_γ)(τ_1) θ_(R_γ)(τ_2).

Les exposants du second facteur peuvent être demi-entiers. Il ne s'agit pas ici de la série
du réseau pair de rang 60, et le produit des coefficients par classe est bilinéaire.

## 2. Déterminer tous les sous-graphes induits sur au plus cinq sommets

Le programme énumère les graphes simples de chaque taille m≤5 et élimine ceux qui violent
les budgets intérieurs : au plus un voisin commun par paire adjacente, au plus deux par paire non adjacente.
Il en reste respectivement 2,4,9,21 types non isomorphes pour m=2,3,4,5.
Les types sont codés par le minimum, sur toutes les permutations des sommets, du masque des arêtes
dans l'ordre lexicographique des paires.

Pour un sous-graphe induit H à m−1 sommets et un ensemble marqué T de zéro, un ou deux sommets,
le nombre de sommets extérieurs adjacents à tous les points de T est exactement

    |T|=0 : 99−(m−1),
    T={i} : 14−deg_H(i),
    T={i,j} : [1 si ij est une arête, 2 sinon]−|N_H(i)∩N_H(j)|.

On agrège cette identité sur les copies induites de H et les marques dans une même orbite
d'automorphismes. Le membre de droite dépend seulement du nombre de copies de H.
Le membre de gauche est une combinaison entière des nombres de graphes à m sommets : pour
chaque graphe K, on parcourt les sommets supprimés v et les marques T de K−v, et on compte
les cas où v est adjacent à tout T. C'est une identité de double comptage, sans hypothèse de transitivité.

À partir des 99 sommets, les systèmes successifs ont 2,6,16,50 équations et **rang plein**.
Les solutions sont donc uniques ; tous les nombres obtenus sont des entiers positifs ou nuls et
leur somme vaut C(99,m). Les matrices entières, seconds membres, solutions et déterminants
non nuls de mineurs de rang maximal sont archivés dans les données.

Le même calcul est comparé à l'énumération directe de tous les sous-ensembles de tailles deux
à cinq de la grille 3×3. Les nombres coïncident pour chaque type, y compris les types absents.
Ce contrôle n'est pas utilisé à la place des identités de double comptage et des certificats de rang.

## 3. Table complète des premières antidiagonales

Les représentants dans D de normes deux à cinq sont : les différences de deux sommets ;
les deux signes des triples ; les quatre signes avec deux positifs et deux négatifs ;
les cinq signes avec sommes ±3 ; et, à la norme cinq, les vecteurs ±(2e_i+e_j), i≠j.
Les formules de Q et Qbar s'appliquent directement à chaque type induit et chaque orientation.

| Norme dans U | Q | Qbar | Nombre exact |
|---:|---:|---:|---:|
| 2 | 6 | 8 | 8316 |
| 2 | 8 | 6 | 1386 |
| 3 | 4 | 17 | 462 |
| 3 | 6 | 15 | 16632 |
| 3 | 8 | 13 | 99792 |
| 3 | 10 | 11 | 196812 |
| 4 | 8 | 20 | 253638 |
| 4 | 10 | 18 | 3218292 |
| 4 | 12 | 16 | 10869012 |
| 4 | 14 | 14 | 6503112 |
| 4 | 16 | 12 | 1555092 |
| 4 | 18 | 10 | 182952 |
| 4 | 20 | 8 | 4158 |
| 5 | 8 | 27 | 1043658 |
| 5 | 10 | 25 | 14586264 |
| 5 | 12 | 23 | 75403944 |
| 5 | 14 | 21 | 201513312 |
| 5 | 16 | 19 | 261571464 |
| 5 | 18 | 17 | 129499524 |
| 5 | 20 | 15 | 28611198 |
| 5 | 22 | 13 | 2910600 |
| 5 | 24 | 11 | 110880 |

Toutes les autres paires sur ces quatre antidiagonales sont absentes. Les sommes des lignes
sont respectivement 9702,313698,22586256,715250844, en accord avec les comptages directs
2C(99,2), 2C(99,3), 6C(99,4), 10C(99,5)+4C(99,2).

## 4. Injectivité et bornes scalaires pour M

La projection sur M est injective sur **l'ensemble** des représentants de U de norme au plus cinq.
En effet une collision donne w=ψ−ψ′∈Γ, donc 9|Σw. Les sommes des représentants valent 0 ou ±3 ;
la seule différence divisible par neuf est zéro. Il s'ensuit Aw=3w.

Dans la classe de somme zéro, les représentants ont masses positive et négative au plus deux,
et la différence a masse positive au plus quatre. Dans la classe de somme +3, ces deux masses
valent au plus quatre et un respectivement ; la différence a masse positive au plus cinq.
La classe de somme −3 est symétrique. Le lemme +3 de la note 168 exclut une différence non nulle
de masse positive au plus cinq. Cela inclut les représentants avec une coordonnée ±2.

En sommant les lignes du tableau pour un Q donné, on obtient donc les bornes sur b_n de θ_M :

| n | Borne inférieure de b_n |
|---:|---:|
| 2 | 462 |
| 3 | 24948 |
| 4 | 1398474 |
| 5 | 18001368 |
| 6 | 86272956 |
| 7 | 208016424 |
| 8 | 263126556 |
| 9 | 129682476 |
| 10 | 28615356 |
| 11 | 2910600 |
| 12 | 110880 |

Pour b_4, on conserve la meilleure borne 1431738 de la note 172, qui contient aussi des
représentants de norme six dans U. Les nouvelles bornes sont des **minorations** de θ_M ;
seuls les nombres conjoints du tableau précédent sont des égalités exactes.

## 5. Une seconde preuve du coefficient 14586264

Pour ψ=1_S−e_v avec |S|=4, v∉S, la norme Q vaut 16−2(e(S)−deg_S(v)).
La condition Q=10 exige e(S)−deg_S(v)=3. Les possibilités sont les trois types à trois arêtes
avec v lointain, ou les deux types à quatre arêtes avec v de degré un.

Il y a 91476 chemins P_4, 27720 griffes K_(1,3), 13860 triangles accompagnés d'un sommet isolé,
2079 quadrangles et 8316 pattes (triangles avec une arête pendante).
Pour une griffe ou un triangle avec sommet isolé, il y a exactement 51 sommets lointains :
50 incidences sortantes, six paires de voisins communs extérieurs et aucun sommet extérieur de degré trois.
Un quadrangle a quarante sommets extérieurs de degré un, une patte quarante-deux (note 172).

Pour un P_4, les incidences sortantes sont cinquante et la somme extérieure des C(t_v,2) vaut sept.
Il n'existe aucun sommet extérieur de degré quatre. Les sommets de degré trois donnent exactement
des maisons (quadrangle avec un triangle ajouté sur une arête). Le nombre de sommets lointains vaut
52−h, où h est ce nombre de sommets de degré trois. Il y a 4·2079=8316 maisons : chaque arête
d'un quadrangle a son unique troisième point de triangle, qui ne peut toucher les deux autres coins.
Chaque maison contient deux P_4 dont le sommet restant a degré trois. Ainsi Σh=16632.

Le nombre total recherché, avec les deux signes, est

    2[(52·91476−16632)+51·27720+51·13860+40·2079+42·8316]
      =14586264.

Les représentants ±(2e_i+e_j) ont Q=12 ou 16, donc ne contribuent pas ici.
Cette preuve retrouve exactement le résultat obtenu par les vingt-et-un types à cinq sommets.

## 6. Ce que les coefficients exacts imposent à chaque classe partenaire

Deux vecteurs distincts de M dans la même classe modulo √7 L1 diffèrent d'un vecteur de
norme au moins 7·min L1≥98. Si chacun a norme au plus vingt-quatre, leur distance carrée
est au plus 4·24=96. Chaque classe contient donc **au plus un vecteur de M de norme ≤24**.

Fixons un tel vecteur m et sa classe γ. Chaque partenaire y∈R_γ donne un unique vecteur
de U de norme (||m||²+||y||²)/7. L'injectivité du §4 implique qu'il y a au plus un tel partenaire
avec ||y||²≤35−||m||². Le tableau indique exactement quelles classes ont ce partenaire court.

- Si m est une racine de M, sa norme vaut deux. La congruence de recollement impose
  ||y||²≡5 (mod 7). Les normes 5,12,19,26,33 sont toutes absentes, puisque le tableau
  ne contient aucun Q=2 et que U n'a aucun vecteur de norme un. Donc min R_γ≥40.
- Si m a norme quatre, la classe partenaire a ses normes congrues à trois modulo sept.
  Les normes 3,10,24,31 sont absentes. Exactement 462 classes, celles des vecteurs venant
  des triangles signés, possèdent un partenaire de norme dix-sept, nécessairement unique.
  Tout autre vecteur de M de norme quatre impose min R_γ≥38.

Ces contraintes ne peuvent pas être remplacées par une égalité globale b_2=462 : des vecteurs
supplémentaires de norme quatre ne sont pas encore exclus. Il faut exploiter les classes partenaires
pour aller au-delà des seules minorations scalaires.

## 7. Test de la relaxation scalaire et fichiers

`code/codex/joint_theta_lp_probe.py` reconstruit les formes dans nos coordonnées c_1,…,c_7,
avec notre base êta indépendante. Il utilise le simplexe rationnel de LAB importé depuis `1cfb4e7`,
mais vérifie ensuite chaque inégalité sur le point rationnel obtenu. Les contraintes à q^84 sont :

- positivité des a_n et b_n ;
- toutes les minorations du §4, avec b_4≥1431738 ;
- a_(7n)≥b_n pour 1≤n≤12 ;
- 7a_7+8a_8≤55440.

Les cinq cas r=35,37,39,41,43 restent faisables. Chacun possède un point rationnel explicite
respectant les 186 contraintes, conservé dans `data/codex_joint_theta_lp_probe.json`.
Cela établit une limite de cette relaxation à cette précision, pas l'existence d'un réseau
ou d'un graphe, ni la faisabilité après ajout de l'intégralité ou des contraintes par classe.

L'autre programme, `code/codex/joint_theta_small_shells.py`, reconstruit les systèmes de comptage,
leurs solutions et les coefficients conjoints. Ses résultats et certificats de rang sont dans
`data/codex_joint_theta_small_shells.json`. Les vérifications utilisent de l'arithmétique exacte ;
elles ne sont ni une formalisation dans un assistant de preuve ni une expertise humaine.
