# 194 — Classes de prismes, grilles locales : τ≤1534 et b3≥45766

8 octobre 2026. Théorème sur les classes de prismes proposé par LAB au
message 261 ; preuve relue, coupure locale et certificats par Codex.

**Résultats.** Dans un hypothétique srg(99,14,1,2),

    17τ ≤ 17P + 105ρ,
    τ ≤ 1534,
    b3 ≥ 45766.

P compte les prismes, ρ les grilles 3×3, et τ les paires non ordonnées de
prismes ayant la même projection sur E_{−4}. Le plafond précédent était
τ≤1890 ; le plancher précédent était b3≥45528. Les deux nouvelles bornes
numériques sont certifiées exactement par le recensement d'ordre neuf.

Les classes de prismes qui ne sont pas contenus dans une grille ont
**au plus trois membres**. Les autres classes sont exactement les
compléments d'une même droite dans les grilles contenant cette droite.
Leur taille appartient à {1,2,3,4,6} ; cinq est impossible.

Le rang 37 reste ouvert. La dernière section distingue les restrictions
démontrées des questions de fermeture cubique encore ouvertes.

## 1. Les profils communs d'une classe de prismes

Pour un prisme X, notons Θ ses trois apices de barreaux et B les soixante
sommets ayant un seul voisin dans X (note 179). On a

    u=(A−3I)1_X=2·1_Θ+1_B,
    (A+4I)u=12·1.

Deux prismes de même projection sont disjoints et anticomplets ; leur
différence est un vecteur propre de valeur trois. Ils ont donc le même u,
et les mêmes ensembles Θ et B. Une classe de taille m utilise 6m sommets
R, et le reste Z, disjoint de R∪Θ∪B, a taille 36−6m. Chaque point de B
possède un voisin dans chacun des m prismes ; chaque point de R possède
un seul voisin dans Θ. Les points de Z sont anticomplets à R.

Pour c∈Θ, si d_Θ(c) est son degré dans Θ, les identités donnent

    d_B(c)=4−2d_Θ(c),
    d_Z(c)=10−2m+d_Θ(c).                                 (1)

En particulier m≤6.

## 2. Une classe de taille au moins quatre est une classe de grilles

Pour w∈B et c∈Θ, soit r_c(w) le nombre de voisins de w dans R dont
l'apex de barreau est c. Leur somme sur les trois apices vaut m.

Si w est adjacent à c, alors r_c(w)=0 : sinon w serait un deuxième
troisième point sur une arête joignant c à un sommet de barreau. Si w
n'est pas adjacent à c, les r_c(w) points sont des voisins communs de
w,c, donc r_c(w)≤2.

Lorsque m≥3, w ne peut donc voir deux apices : tous ses voisins dans R
devraient être affectés au troisième, qui ne peut en recevoir que deux.
Si w voit exactement un apex c, alors m≤4. Pour m=4, les deux autres
valeurs r sont chacune deux ; c ne peut être adjacent à aucun autre
apex, car il fournirait un troisième voisin commun avec w.

Ainsi, pour m=4, aucun apex ne peut avoir degré un dans Θ : il aurait
d_B(c)=2 par (1), mais tout voisin dans B impose d_Θ(c)=0. Le graphe Θ
est donc vide ou triangulaire.

Le cas vide est impossible. Chaque apex a exactement deux voisins dans Z.
Deux apices ont deux voisins communs, qui ne peuvent appartenir ni à R,
ni à B, ni à Θ. Leurs voisinages de taille deux dans Z sont donc égaux.
Les trois apices ont les mêmes deux voisins dans Z ; ces deux points ont
trois voisins communs, contradiction.

Pour m≥5, aucun apex ne peut avoir de voisin dans B, puisque cela
imposerait m≤4. Par (1), chaque apex a degré deux dans Θ. On conclut :

    m≥4 ⇒ Θ est un triangle.                            (2)

Quand Θ est un triangle, X∪Θ est une grille. Les classes de prismes
hors grille ont donc taille au plus trois.

## 3. Les classes de grilles sont indexées par les droites

Pour une grille G, P4(1_G)=0 (grille serrée, note 00). Si Θ est l'une de
ses six droites, X=G\Θ est un prisme et

    P4(1_X)=−P4(1_Θ).

Tous les prismes issus des grilles sur Θ ont donc la même projection.
Deux de ces prismes distincts ne peuvent se rencontrer : leur différence
serait propre de masse positive au plus cinq, exclue par la note 168.
Ils sont ensuite anticomplets par les équations propres et leur degré
interne trois. Réciproquement, une classe possède un unique ensemble
d'apices, qui est Θ. On obtient une bijection entre les classes de grilles
et les droites présentes dans au moins une grille.

Notons g(ℓ) le nombre de grilles contenant la droite ℓ. Alors

    Σ_ℓ g(ℓ)=6ρ,
    τ_grille=Σ_ℓ binom(g(ℓ),2),
    τ ≤ P−6ρ+τ_grille.                                  (3)

La dernière inégalité utilise binom(m,2)≤m pour les classes hors grille,
dont m≤3. Un prisme appartient à au plus une grille, donc exactement 6ρ
prismes sont des prismes de grille.

**Cinq grilles sur une droite en imposent six.** Supposons m=5. Il reste
six points Z. Tout z∈Z voit exactement un point de Θ, car il est extérieur
à chacune des cinq grilles serrées et ne voit aucun de leurs prismes.
L'identité du §1 donne alors d_B(z)=10, donc d_Z(z)=3.

Un graphe cubique simple à six sommets est le complément d'un 2-régulier,
donc un prisme ou K_{3,3}. Le second viole μ≤2. Z est un prisme. Chaque
apex a deux voisins dans Z ; ceux-ci sont adjacents puisque son voisinage
est un appariement. Les trois arêtes ainsi obtenues ne peuvent être dans
les faces triangulaires de Z, dont le troisième point est déjà interne :
ce sont ses trois barreaux. Z∪Θ est donc une sixième grille.

Par conséquent,

    g(ℓ)∈{0,1,2,3,4,6}.                                 (4)

La classification de tous les graphes possibles sur Z n'est pas nécessaire
à cette preuve ; en particulier on ne suppose pas qu'ils soient tous des
produits C_{3k}□K₂.

## 4. Une inégalité locale sur sept droites

Pour un sommet v, construisons Ξ_v sur les sept droites passant par v :
deux sont adjacentes si elles engendrent une grille. Une paire de droites
détermine au plus une grille, donc Ξ_v est simple. Le degré de son sommet
ℓ est g(ℓ), et son nombre e_v d'arêtes est le nombre de grilles par v.
Les notes 105 et 108 prouvent e_v≤17.

Posons c_v=Σ_{ℓ∋v} binom(g(ℓ),2). Montrons que

    17c_v ≤ 69e_v.                                      (5)

Soit a le nombre de sommets de degré six dans Ξ_v. Quatre sommets
universels imposeraient au moins dix-huit arêtes, donc a≤3. Chaque autre
degré d vérifie a≤d≤4, puisque cinq est exclu par (4). Ainsi

    d(d−1) ≤ (a+3)d−4a.

En sommant et en tenant compte des a degrés six,

    c_v ≤ (a+3)e_v−a(a+8).

Pour a=0,1,2,3 et e_v≤17, cette expression implique (5). Le cas d'égalité
non vide est réalisé dans cette relaxation locale par K₇ privé d'un
4-cycle : degrés (6,6,6,4,4,4,4), e=17 et c=69. On n'affirme pas que ce
graphe local admette un prolongement en srg(99,14,1,2).

Chaque grille contribue à neuf e_v, chaque droite à trois c_v. Donc

    Σ_v e_v=9ρ,    Σ_v c_v=3τ_grille,
    17τ_grille≤207ρ.

Avec (3), cela donne la nouvelle coupure

    17τ ≤ 17P+105ρ.                                     (6)

Elle quantifie l'impossibilité du précédent coin τ=1890, P=756, ρ=126.
Dans ce coin, toutes les classes de grilles auraient taille six ; tout
Ξ_v non vide serait alors K₇, déjà exclu par la note 105.

## 5. Conséquences exactes du recensement

`grid_class_bounds.py` ajoute (6) aux contraintes de la note 185 et aux
5311 comptes non négatifs d'ordre neuf. Une combinaison de **17 lignes
à poids rationnels non négatifs** donne

    τ ≤ 26082/17 = 1534 + 4/17,
    donc τ ≤ 1534.

Le programme conserve un point rationnel atteignant le plafond du modèle
linéaire et en vérifie toutes les contraintes. L'intégralité et la
réalisation combinatoire de ce point ne sont pas affirmées.

En ajoutant la même coupure au calcul des différences de triangles
lointains de la note 186, une combinaison de **14 lignes** donne

    b3 ≥ 778008/17 = 45765 + 3/17,
    donc b3 ≥ 45766 par parité.

Cela apporte **238 vecteurs de norme six supplémentaires** à la borne
uniforme précédente. Au rang 37, avec les autres contraintes prouvées de
la note 192 et la précision q^84, `grid_class_theta_effect.py` vérifie

    b4 ≤ 2172653139/136 ≈ 15975390,73.

Le plafond diminue de 4557. Le plafond couplé demeure

    b4+(651/34)b3 ≤ 2291827803/136 ≈ 16851675,02.

Ces deux plafonds disposent aussi de certificats et de points rationnels
atteignant la relaxation. Le rang 37 n'est pas exclu.

## 6. Un cube de Hamming induit est impossible

**Lemme.** Γ ne contient aucun H(3,3)=K₃□K₃□K₃ induit.

Supposons un tel sous-graphe S, à 27 sommets et de degré interne six.
Deux sommets à distance un dans S ont déjà leur voisin commun unique ;
deux sommets à distance deux ont déjà leurs deux voisins communs. Deux
voisins dans S d'un sommet extérieur doivent donc être à distance trois,
c'est-à-dire différents dans chacune des trois coordonnées.

Un sommet extérieur a ainsi au plus trois voisins dans S. Or le nombre
d'arêtes sortant de S vaut 27·(14−6)=216 et il reste 72 sommets. Chacun
d'eux doit avoir exactement trois voisins dans S.

Il n'existe que (3!)²=36 triples diagonaux de S : en ordonnant leurs
points selon la première coordonnée, les deux autres coordonnées sont
deux permutations indépendantes. Deux sommets extérieurs ne peuvent
avoir le même triple de voisins, car ils auraient trois voisins communs.
Il faudrait donc 72 triples distincts parmi 36, contradiction.

Ce lemme **ne prouve pas que Ξ_v soit sans triangle**. Trois grilles
deux à deux portées par trois droites en v ne donnent immédiatement
qu'une union de dix-neuf sommets. Le programme vérifie que cette union
passe les budgets locaux λ≤1, μ≤2. Il manque un théorème de fermeture
en cube complet pour utiliser le lemme contre les triangles de Ξ_v.

## 7. Cibles locales et reproduction

La note 112 laisse vingt configurations de torsion au cas e_v=17 :
huit du motif (0,2,0,2) et douze du motif (2,2,2,2), après les contrôles
de second ordre. Au coin P=6ρ, tous les prismes sont des prismes de
grille, donc P(v)=4e_v. Avec P(v)=84−|W(v)|, e_v=17 impose |W(v)|=16.
Cela sélectionne le second motif et ses **douze configurations restantes**.
Il s'agit d'une cible précise de recherche, pas d'une nouvelle exclusion.

Autre limite : P=6ρ n'élimine pas à lui seul tous les supports propres
de masses huit et neuf autres que les différences de grilles. Au point
rationnel atteignant notre plafond de recensement, le type à huit sommets
C_127305925, à treize arêtes, a compte 1890 ; il n'est pas le type à
quatorze arêtes obtenu en retirant un point d'une grille. Toute réduction
de toutes les collisions à des paires de grilles doit encore être prouvée.

Reproduction :

    python code/codex/grid_class_bounds.py --verify-only
    python code/codex/grid_class_theta_effect.py --verify-only

Le premier script contrôle les contraintes nécessaires sur les degrés
locaux, le cas d'égalité K₇−C₄, les 36 triples diagonaux du cube et son
union de trois grilles à dix-neuf sommets. Il reconstruit ensuite les
lignes du recensement et vérifie les identités rationnelles et les points
atteignant les bornes. Les fichiers de preuve portent le préfixe
`data/codex_grid_class_`. Sans `--verify-only`, les deux scripts régénèrent
leurs certificats.
