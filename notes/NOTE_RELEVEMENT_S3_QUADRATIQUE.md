# Relèvement des signes de BH : formulation quadratique exacte sur F₃

12 octobre 2026, Codex. Suite constructive de l'audit du commit `640ffe1`.
Cette note précise le passage manquant entre le squelette de parité et un
revêtement complet. Elle ne construit pas de nouveau SRG et n'exclut pas
les revêtements de monodromie S₃.

## 1. Résultat

Fixons sur BH = SRG(81,20,1,6) des signes s_xy=s_yx dans {1,−1}, tels que :

- le produit des signes autour de chaque triangle soit 1 ;
- pour toute paire non adjacente P,R, les six signes des chemins P-Z-R
  se répartissent en 6+0, 3+3 ou 0+6.

**Théorème de reformulation.** Les revêtements à fibres K₃ réalisant ces
signes et les paramètres (243,22,1,2) correspondent exactement aux solutions
d'un système sur F₃ constitué d'équations homogènes linéaires et d'équations
quadratiques à second membre 1 ou 2, décrit ci-dessous.

Avant d'imposer les équations des paires non adjacentes, l'espace des
translations compatibles avec les triangles, modulo les changements
d'origine dans les fibres, a dimension **459 si le signing est non trivial
modulo changement de signes aux sommets**, et **460 s'il est trivial**.
Les équations linéaires des paires peuvent encore réduire cette dimension.
Les équations quadratiques restantes sont nécessaires **et suffisantes**.

## 2. Gains affines et équations de triangle

Toute permutation de F₃ s'écrit de manière unique

\[
g_{xy}(t)=s_{xy}t+b_{xy},\qquad b_{xy}\in\mathbf F_3.
\]

Choisir une orientation de chaque arête et une variable b par arête ; dans
l'autre sens,

\[
b_{yx}=-s_{xy}b_{xy}.
\]

Pour un triangle orienté x-y-z-x, l'holonomie identité équivaut, les signes
étant déjà équilibrés, à l'équation linéaire

\[
b_{zx}+s_{zx}b_{yz}+s_{zx}s_{yz}b_{xy}=0.
\]

Il y a 810 arêtes et 270 triangles dans BH. Chaque arête appartient à un
unique triangle : ces 270 équations ont donc des supports disjoints et sont
indépendantes. L'espace des translations satisfaisant les triangles a
dimension 810−270=540.

## 3. Le lemme des deux moments

**Lemme.** Soient q=1 ou 2 et c₁,…,c₃q des éléments de F₃. Chacune des
valeurs 0,1,2 apparaît exactement q fois si et seulement si

\[
\sum_i c_i=0,\qquad \sum_i c_i^2=2q\quad\text{dans }\mathbf F_3.
\]

*Preuve.* Si r₀,r₁,r₂ sont les multiplicités entières, les équations donnent
r₁−r₂=0 et r₁+r₂=2q modulo 3. Donc r₁=r₂=q modulo 3, puis r₀=q modulo 3
puisque r₀+r₁+r₂=3q. Chaque r_i est un entier non négatif, donc au moins q
(q vaut 1 ou 2). Leur somme est exactement 3q : ils valent tous q. La
réciproque est immédiate. ∎

La restriction q∈{1,2} est essentielle à cet argument de taille ; elle
correspond exactement aux deux cas présents dans le revêtement.

## 4. Les équations des six chemins

Pour P,R non adjacents et Z l'un de leurs six voisins communs, poser

\[
e_Z=s_{ZR}s_{PZ},\qquad c_Z=s_{ZR}b_{PZ}+b_{ZR}.
\]

Le chemin P-Z-R agit par t↦e_Zt+c_Z. La condition de voisins communs du
revêtement est que la somme de ces six matrices de permutation soit 2J₃.

**Six signes égaux.** La condition exacte est

\[
\sum_Z c_Z=0,\qquad \sum_Z c_Z^2=1.
\]

En effet, chaque translation doit apparaître deux fois, et le lemme
s'applique avec q=2.

**Trois signes de chaque sorte.** Pour ε=+1 et ε=−1, imposer séparément

\[
\sum_{Z:e_Z=\varepsilon} c_Z=0,\qquad
\sum_{Z:e_Z=\varepsilon} c_Z^2=2.
\]

Le lemme donne une occurrence de chaque translation dans chaque classe de
signe. On obtient alors une occurrence de chaque élément de S₃, et la somme
des six matrices est 2J₃.

Pour voir la nécessité dans le cas 3+3 sans supposer cette distribution,
noter n_a et m_a les nombres de chemins de translation a de signes + et −.
L'entrée (t,u) de la somme impose n_(u−t)+m_(u+t)=2. Sur F₃, l'application
(t,u)↦(u−t,u+t) est bijective. Donc n_a+m_b=2 pour tous a,b ; les n_a sont
constants, de même que les m_b. Leurs sommes étant toutes deux 3, tous
valent 1.

Les c_Z sont des formes linéaires en b. Les premières équations sont donc
linéaires homogènes ; les secondes sont quadratiques. Les calculs se font
exclusivement dans F₃, sans approximation numérique.

## 5. Pourquoi ces conditions suffisent au SRG complet

La construction met un triangle dans chaque fibre et un couplage parfait
sur chaque arête de BH ; tous les sommets ont donc degré 2+20=22.

- Deux sommets distincts d'une fibre sont adjacents et ont leur unique
  voisin commun dans cette fibre.
- Pour deux fibres adjacentes, BH fournit une unique fibre commune. Si les
  deux sommets sont appariés, l'holonomie du triangle leur donne exactement
  un voisin commun dans cette troisième fibre. S'ils ne sont pas appariés,
  ils ont un voisin commun dans chacune des deux fibres initiales et aucun
  dans la troisième.
- Pour deux fibres non adjacentes, les équations de la section 4 assurent
  exactement deux voisins communs, quels que soient les deux sommets.

Ainsi λ=1 et μ=2 pour toutes les paires. Réciproquement, les paramètres du
SRG imposent l'holonomie identité sur les triangles et les sommes 2J₃ sur
les paires non adjacentes, d'où toutes les équations précédentes.

## 6. Quotient par les origines des fibres : dimensions 459 et 460

Changer l'origine de la fibre x par t'_x=t_x+a_x transforme les translations
selon

\[
b'_{xy}=b_{xy}+a_y-s_{xy}a_x.
\]

Ces transformations préservent les équations de triangle. Le noyau de
l'application a↦(a_y−s_xy a_x) est l'espace des fonctions telles que
a_y=s_xy a_x sur chaque arête. BH est connexe :

- si tout cycle a signe +, cet espace est de dimension 1 ;
- s'il existe un cycle de signe −, son transport impose a_x=−a_x, donc
  a_x=0 sur F₃ et a=0 partout.

La dimension des changements effectifs d'origine vaut donc respectivement
80 ou 81. Après quotient, les 540 dimensions des triangles deviennent
460 ou 459. Concrètement, on peut annuler b sur les 80 arêtes d'un arbre
couvrant ; dans le cas non trivial, le changement d'origine résiduel
permet encore d'annuler b sur une arête négative après normalisation des
signes de l'arbre.

Les équations de moments passent bien au quotient : dans une classe de
signe, tous les c_Z subissent le même ajout d. Il y a 3 ou 6 termes ; leur
somme ne change donc pas modulo 3. Si cette somme est nulle, la somme de
leurs carrés ne change pas non plus.

## 7. Conséquence pour la recherche

Pour un signing admissible fixé, on peut désormais :

1. imposer les triangles et les premiers moments, puis quotienter par les
   changements d'origine, par algèbre linéaire exacte ;
2. substituer une base dans les équations de seconds moments ;
3. chercher une solution, ou une incompatibilité, dans le système
   quadratique réduit sur F₃.

Cela complète la formulation du problème de relèvement. Il reste à obtenir
un signing non trivial admissible et à décider la solubilité de son système
quadratique, ou à prouver une obstruction uniforme. Aucun gain de complexité
pratique n'est garanti par cette reformulation ; aucun solveur lourd n'a
été lancé pour cette note.

Si un tel relèvement d'un signing non trivial existe, sa monodromie est
effectivement S₃ : pour une paire non adjacente, les six chemins envoient
chaque point de la fibre de départ sur les trois points d'arrivée. En
revenant par l'un de ces chemins, les holonomies agissent donc transitivement
sur trois points. Les seules possibilités sont A₃ et S₃ ; un cycle négatif
exclut A₃. Cette conclusion ne dit toujours pas que le groupe complet des
automorphismes du graphe est trivial.

Le seul contrôle informatique nouveau est exhaustif sur les 27 triplets et
729 sextuplets de F₃ : `code/codex/check_s3_lifting_moments.py`. Il accompagne
le lemme des deux moments, sans répéter les calculs des quatre graphes.
