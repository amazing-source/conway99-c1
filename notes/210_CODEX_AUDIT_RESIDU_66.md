# 210 — Résidu (6,6) : relations locales et correction du filtre de triplets

8 octobre 2026. Réponse aux messages 355–362 de LAB ; les calculs de
plans de triplets mentionnés par LAB sont distincts des vérifications
finies présentées ici.

## 1. La réduction reste conditionnelle

La note 126 §3 ter est correcte avec ses deux hypothèses : absence de
torsion équilibrée sur les droites connexes, et obstruction uniforme
des étoiles génériques. Sous ces hypothèses, P=S=0 et rang global 37
imposent que les 231 droites aient profil (6,6).

Ici S est la variable globale de L18. La note 125 prouve

    Σ_T c₄^{(ii)}(G(T)) = S,
    Σ_T c₄(G(T)) = S+3P.

Ainsi P=S=0 impose maille au moins cinq dans tous les G(T). Les
hypothèses sur la torsion et l'étoile uniforme demeurent ouvertes.
Le test x32 exclut la torsion équilibrée portée sur une composante
isolément ; il n'exclut pas automatiquement une torsion équilibrée
obtenue en couplant les deux composantes.

Pour une droite T de profil (6,6), posons

    h_T = 1_C₁ − 1_C₂.

Chaque C_i contient 18 points. Donc h_T est un vecteur propre entier
de valeur 3, de somme nulle et de norme **36≡1 modulo 7**. Il ne faut
pas confondre cette norme avec celle, égale à 2 modulo 7, de la classe
centrée κ correspondant à une seule composante : h_T=2κ′ en classes.

## 2. Au plus une relation incidente par sommet

Autour d'un sommet v, les sept droites se partagent chacune en deux
blocs de trois autres droites. Le graphe F_v de la note 208 est simple,
cubique, à 14 sommets et 21 arêtes. Une arête joint deux blocs de
droites distinctes, et chaque paire de droites apparaît exactement
une fois.

**Lemme.** F_v a au plus une composante connexe bipartie.

Une composante cubique simple bipartie a au moins six sommets. S'il
y en avait deux, leurs tailles seraient six et huit : deux tailles
six laisseraient deux sommets, impossibles pour une autre composante
cubique simple. La composante de taille six serait K₃,₃.

Ses six sommets portent six étiquettes de droites distinctes. Deux
blocs de même étiquette dans des parties opposées donneraient une
arête entre deux blocs de la même droite. Dans la même partie, ils
répéteraient une paire d'étiquettes en joignant un même bloc opposé.
Les deux cas sont impossibles.

Pour chacune des six étiquettes, il reste alors un unique bloc hors
du K₃,₃. Les trois étiquettes de chacune de ses parties se relient
mutuellement par ces blocs restants, puisqu'aucune de ces paires
n'a été utilisée dans le K₃,₃. Il reste donc deux triangles. Le
complément de taille huit n'est pas biparti, contradiction. ∎

Pour compter exactement les relations locales, orientons les deux
blocs de chaque droite et écrivons s_ij=±1 selon le bloc contenant j.
Alors h_i=Σ_{j≠i}s_ij g_ij, dans les coordonnées formelles de la note
208. Un témoin porté par N[v], avec éventuellement un terme constant,
impose et est imposé par

    c_i s_ij + c_j s_ji = z_i+z_j,       pour chaque paire ij.

La complétude suit des quatre coins de chaque paire, comme en note
206 : le témoin est constant sur les deux points de chaque droite.
En posant x_(i,±)=±c_i−z_i, l'équation devient x_a+x_b=0 sur les
arêtes de F_v. Son espace de solutions a dimension b(F_v). La
projection sur les coefficients c est injective : c=0 imposerait
z_i+z_j=0 sur K₇, donc z=0. Ainsi la dimension des relations obtenues
est exactement b(F_v)≤1.

**Le mot local impose ici deux conditions** : les coefficients sont
portés par les sept droites passant par v et le témoin par N[v]. La
seule condition sur le support du témoin ne suffit pas.

Le contrôle exact énumère les 700 systèmes normalisés contenant un
K₃,₃ : 70 ont composantes de tailles (4,4,6), 630 de tailles (6,8).
Tous ont une seule composante bipartie. Le script vérifie aussi dans
les 99 coordonnées l'identité entière (A+4I)y=Σc_i h_i associée.

## 3. Pourquoi le déficit de relations locales ne prouve pas l'exclusion

Au rang 37, les 231 classes h_T appartiennent à un espace centré de
dimension 18. Le noyau des classes a donc dimension au moins 213.
Le sous-espace engendré par les relations incidentes du §2 a dimension
au plus 99. Il reste donc au moins 114 dimensions de relations modulo
celles-ci.

Mais ces relations ne doivent pas être décrites comme ayant
nécessairement un témoin de support non local. Les 231 vecteurs h_T
appartiennent déjà, en caractéristique zéro, à l'espace propre de
valeur 3, de dimension 54. Il existe donc au moins **177 relations
entières indépendantes** entre les vecteurs eux-mêmes.

Le noyau entier de la matrice des h_T est saturé dans Z²³¹ ; sa
réduction fournit donc au moins 177 relations indépendantes modulo
sept. Toutes ont le témoin **y=0**, de support vide. Au moins 78
dimensions de ces égalités de coordonnées ne peuvent être engendrées
par les relations incidentes, puisque 177−99=78.

Le radical arithmétique de dimension 36 au rang 37 peut ajouter au
plus 36 dimensions de relations de classes aux relations de
coordonnées. Cette distinction explique pourquoi le seul comptage
213 contre 99 n'approche pas une contradiction : beaucoup de
relations globales sont déjà forcées rationnellement.

## 4. Les 630 triplets passent un filtre incomplet

Pour une composante C de 18 points, chaque ombre lointaine rencontre
C en un triplet. Le test x32, et la première recherche de plans
rapportée par LAB, utilisent les conditions suivantes : au plus deux
points par couche, multiplicité K positive sur chaque paire, et au
plus une arête de G[C] dans le triplet. Il y a 630 candidats dans
chacune des 288 composantes étiquetées de maille au moins cinq.

Il faut aussi imposer, en chaque point x de C,

    (G[C] 1_T)_x ≤ 2−1_T(x).                            (1)

Cette contrainte retire exactement les 18 triplets N_G(x). Chacun de
ces voisinages est indépendant, a un point par couche et des paires
de multiplicité un : il passe les trois filtres précédents. Mais il
donnerait trois voisins communs à x et au sommet lointain, contre
μ=2. Les 18 voisinages sont distincts, sinon deux sommets auraient
trois voisins communs dans un graphe de maille au moins cinq.

Réciproquement, sous les filtres précédents, une violation de (1) ne
peut se produire en x∈T, puisqu'elle demanderait déjà deux arêtes
dans T. Pour x∉T, elle impose les trois voisins de x dans T, donc
T=N_G(x). Ce sont exactement les triplets retirés.

La reconstruction indépendante vérifie donc, pour **les 288
composantes**, le passage uniforme **630→612 candidats**. Les
multiplicités de paires ont somme 20 hors diagonale à chaque point,
soit dix occurrences par point dans un éventuel plan de 60 triplets.

Cette correction préserve les exclusions obtenues par x32 : un test
d'infaisabilité sur une relaxation reste valable. En revanche, une
solution de plan parmi les 630 candidats ne suffit pas à satisfaire
les équations avec la boule. Les recherches de faisabilité doivent
utiliser les 612 candidats restants. Leur existence simultanée et
le couplage des deux composantes ne sont pas tranchés par cet audit.

Fichiers : `code/codex/component66_local_audit.py` et
`data/codex_component66_local_audit.json`.

    python code/codex/component66_local_audit.py --verify-only
