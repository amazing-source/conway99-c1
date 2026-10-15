# C1 — journal de recherche de la nuit du14 octobre2026

## Consigne et état de départ —02h06 Paris

Travail continu demandé par Dilan, relayé par Claude LAB. Repartir de la
définition de SRG(99,14,1,2), sans rouvrir les anciennes notes de Codex ou
de LAB. Aucun calcul payant ; aucune relance des campagnes UNKNOWN.
But : exclusion, réduction finie abordable démontrée, ou contraintes
supplémentaires effectives pour le solveur. Les résultats restent distincts
des hypothèses et des témoins de relaxations.

Ce nouveau fichier reçoit les preuves et les points de reprise. Commits
fréquents ; signe de vie à Claude au moins toutes les45minutes. Session
du pont :01a1379f-6e0a-7da2-8355-ea6b7c7eda46. Le lecteur automatique
est actif, curseur619 au départ. Le fichier historique modifié
`code/codex/coheawood_completion.py` est laissé intact.

## Axiomes utilisés

G a99 sommets, degré14 ; deux sommets adjacents ont exactement un voisin
commun, deux sommets non adjacents exactement deux. Sa matrice A vérifie

    A=A^t, diag A=0, A_ij dans{0,1}, A1=14*1,
    A²+A=12I+2J.

Chaque voisinage induit est donc un appariement de sept arêtes. Toute
arête appartient à un unique triangle ; il y a231 triangles, sept par
sommet. Un sommet extérieur à un triangle touche au plus un sommet de
celui-ci, sinon une arête aurait deux voisins communs.

Cible initiale : exploiter la coexistence de ces231 triangles et les
relations entre triangles disjoints. Une identité dérivée n'est pas encore
une réduction ; chercher une conséquence entière ou une obstruction
qui élimine des choix dans un système commun.

## 02h22 — Coupure sur le triangle de base : au plus neuf prismes

**Résultat prouvé à partir des seuls axiomes.** Il existe un triangle T
qui a au plus neuf triangles disjoints U reliés à T par trois arêtes.
Le nombre total de ces paires non ordonnées (prismes triangulaires
induits) est au plus1151. Cela exclut la famille où chaque triangle a
au moins dix partenaires de prisme. Dans toute recherche à triangle
de base libre, on peut imposer p(T)<=9 sans perdre de candidat.

Voici la preuve, avec normalisations explicites. Le projecteur P sur
l'espace propre -4 de A est (27I-9A+J)/63. Posons

    u_x = sqrt(63) P e_x ; q_T = sqrt(7) P 1_T.

Les produits des u sont28 sur la diagonale, -8 sur les arêtes, 1
sur les non-arêtes. Le produit u_x.q_T vaut4 si x appartient à T,
-2 si x est extérieur et voisin de T, 1 sinon. Il y a respectivement
3,36,60 sommets dans ces cas. Les produits des q valent4 sur la
diagonale, 0 pour deux triangles sécants, et1-j pour deux triangles
disjoints ayant j arêtes entre eux. Ces arêtes forment un appariement.

Pour un triangle T, écrivons p=p(T)=n_3. On a

    n_0=32-p, n_1=144+3p, n_2=36-3p, n_3=p.

Justification : il y a212 triangles disjoints, somme j*n_j=216.
Avec N l'incidence sommets-triangles, NN^t=A+7I, donc la Gram M des q
vérifie M²=21M et M1=0. Ces deux identités donnent respectivement
16+n_0+n_2+4p=84 et4+n_0-n_2-2p=0. On en déduit les formules.
En particulier0<=p<=12.

Considérons les tenseurs symétriques réels

    S = somme_T q_T tensor q_T tensor q_T,
    V = somme_x u_x tensor u_x tensor u_x.

Le produit des cubes tensoriels est le cube du produit scalaire. Avec
p_bar la moyenne sur les231 triangles, les comptes précédents donnent

    ||S||² = 231*(64+n_0-n_2-8p_bar) = 1386*(10-p_bar),
    <S,V> = 231*(3*64-36*8+60) = -8316,
    ||V||² = 99*(28³-14*8³+84) = 1471932.

Cauchy-Schwarz impose ||S||²>=2772/59, donc

    p_bar <= 588/59 < 10,
    somme_T p(T) <= 135828/59,
    nombre de prismes = (somme_T p(T))/2 <= 1151.

La dernière inégalité utilise l'intégralité du nombre de paires. Il
existe donc T avec p(T)<=9. La positivité des seuls cubes q ne donnait
que p_bar<=10 ; le couplage avec les99 sommets est essentiel pour
éliminer l'égalité dix.

**Lecture pour le solveur.** Les36 voisins extérieurs de T se partagent
en X_a,X_b,X_c, douze par sommet de T. Chaque X induit un appariement,
et chaque paire de X est reliée par un appariement parfait : pour
x dans X_a et b dans T, les deux voisins communs de x,b sont a et
un unique sommet de X_b. Après avoir normalisé les appariements
X_a-X_b et X_a-X_c à l'identité, celui de X_b-X_c est une permutation
pi de douze lettres. Ses points fixes sont exactement les p(T)
triangles transversaux. On peut donc exiger au moins trois lettres
déplacées par pi (au plus neuf points fixes). Le choix du triangle
de base est libre : ce n'est pas une borne locale pour tous les T.

**Vérification.** `code/codex/night_20261014/triangle_frame_moments.py`
calcule les produits et bornes en arithmétique rationnelle SymPy, et
vérifie les polynômes des quatre projecteurs du graphe d'intersection
des triangles modulo z(z-18)(z-7)(z+3). Rapport dans
`data/codex_night_20261014/triangle_frame_moments.json`.

**Suite.** Examiner les contraintes conjointes sur les trois codages des
60 non-voisins du triangle ; chaque codage est une bijection avec les
60 paires non appariées d'un X de douze sommets. Aucun lancement de
campagne UNKNOWN. Message623 de Claude lu : résultats indépendants
sur la même Gram et sur les grilles, pas utilisés comme ancienne note.

## 02h35 — Exclusion indépendante des21 grilles passant par un sommet

**Énoncé.** Dans un srg(99,14,1,2), aucun sommet v ne peut avoir la
propriété que chacune des21 paires de triangles passant par v engendre
une grille3x3 induite. La preuve ci-dessous réduit cette famille à128
configurations sur F2, puis à136656 systèmes linéaires de signes ; tous
sont contradictoires. Le script autonome termine en une dizaine de
secondes, sans solveur SAT. Cela confirme indépendamment le verdict
SAT transmis par Claude au message626, sans lire son code ni ses notes.

### 1. Les21 carrés et les105 permutations

Écrivons les voisins de v sous la forme i+,i- (i=0,...,6), chaque paire
formant avec v un triangle. Tout non-voisin de v a deux voisins dans ce
voisinage, dans des paires distinctes. Chaque couple de tels voisins
non adjacents a exactement un deuxième voisin commun : les84 sommets
restants sont donc z_(i epsilon,j delta), quatre par paire e={i,j}.

Sous l'hypothèse, v, les quatre points i+/i-/j+/j-, et ces quatre z
forment une grille. Chaque grille R est un code parfait :

    1_R^t P 1_R = (27*9-9*36+81)/63 = 0,
    P1_R=0, donc A1_R=3*1_R+1.

Tout sommet extérieur a exactement un voisin dans R. Par conséquent,
les quatre z d'une cellule Q_e induisent un carré ; deux cellules
Q_e,Q_f n'ont aucune arête si e,f se rencontrent, et sont reliées par
un appariement parfait si e,f sont disjointes. Il reste donc105 matrices
de permutation4x4, sur les arêtes du graphe KG(7,2).

Soit H la matrice induite sur les84 z, et D l'incidence14x84 entre les
voisins de v et les z. Les équations SRG donnent

    H²+H=12I+2J-D^tD,
    D H=2J-(I+S)D,

où S apparie i+ à i-. L'incidence D est celle du graphe complet
multiparti à sept parts de taille2. Son rang réel est14. Sur im D^t,
H a les valeurs12 (une fois), -2 (six fois) et0 (sept fois). Sur ker D,
H a3 (40 fois) et-4 (30 fois), par l'équation quadratique et la trace.

Les fonctions constantes sur les21 cellules portent 2I+A_KG, de
spectre12^1,(-2)^6,3^14. Sur les trois caractères non constants de
chaque carré, la matrice restante M, d'ordre63, a donc

    spectre M = 0^7,3^26,(-4)^30.

La base des caractères est (epsilon,delta,epsilon*delta)/2. Le bloc
diagonal vaut diag(0,0,-2). Chaque bloc hors diagonale non nul est une
permutation signée3x3 dont le produit des trois signes est+1 : c'est
la représentation des24 permutations de quatre points. Le script
vérifie directement les24 cas avec la matrice de Hadamard du carré.

Écrivons U_i le vecteur qui a coefficient+1 sur le caractère du point
i dans chacune des six cellules contenant i, et0 ailleurs. Les sept
U_i sont orthogonaux, de norme carrée6, et

    M U_i=0 ; M²+M=12I-2*sum_i U_i U_i^t.

### 2. Le projecteur symplectique de rang12

Modulo2, M devient la matrice d'un revêtement à trois feuilles de
KG(7,2), et M²=M. Son polynôme caractéristique modulo2 lui impose le
rang26. La représentation de permutation sur F2^3 se décompose en la
droite constante et le plan de somme nulle. La première porte A_KG,
idempotent de rang14 (son spectre entier est10^1,(-4)^6,1^14).
La seconde donne un projecteur B de rang12 sur un espace de dimension42.

Le plan de somme nulle de F2^3 porte une forme alternée non dégénérée
(restriction du produit scalaire). B est auto-adjoint pour la somme
orthogonale de ces21 plans ; son image V est donc un espace symplectique
de dimension12. Les images E_ij des21 plans de coordonnées sont des
plans isotropes, injectifs puisque les blocs entre cellules disjointes
sont inversibles. Deux de ces plans sont orthogonaux si leurs indices
se rencontrent, et leur couplage est inversible sinon.

Pour un indice i fixé, les six E_ij engendrent un espace isotrope W_i,
donc de dimension au plus6. Trois E_ij,E_ik,E_il sont toujours en somme
directe : le couplage avec E_jk annule les deux premiers et est
inversible sur le troisième. Ainsi dim W_i=6 et W_i est lagrangien.
En outre W_i inter W_j=E_ij. Pour le voir, les noyaux dans W_i des
couplages avec E_jk et E_jl sont respectivement E_ij+E_ik et
E_ij+E_il ; leur intersection est E_ij. L'orthogonal de W_j vaut W_j.

Les six plans d'un W_i forment l'unique configuration de six plans de
dimension2 dans F2^6 dont chaque triple est direct. Preuve élémentaire :
fixer trois plans comme axes, puis un quatrième comme (I,I,I). Tout
autre s'écrit (I,A,B), avec A,B,I+A,I+B,A+B inversibles. Dans GL(2,2),
les seules matrices A avec I+A inversible sont R et R², où

    R = [[0,1],[1,1]].

Les deux plans restants sont donc (I,R,R²) et (I,R²,R). Ils satisfont
bien les conditions, vérifiées directement par le script.

### 3. Classification de128 configurations symplectiques

Fixons W_0 et les six plans P_i=E_0i sous cette forme. Identifions
V=W_0+W_0*, avec la forme symplectique usuelle. Posons S_i=P_i^perp
dans W_0*. Tout lagrangien W_i rencontrant W_0 exactement en P_i
est le graphe, modulo P_i, d'une forme bilinéaire symétrique f_i sur
S_i (dimension4), soit dix bits par i. Pour i!=j, la condition
dim(W_i inter W_j)=2 équivaut exactement à

    f_i restreinte à (S_i inter S_j) = f_j sur ce même plan.

Ce sont45 équations binaires sur60 bits ; leur rang calculé est32,
d'où une solution de dimension28. Les cisaillements symplectiques
(x,y)->(x+F y,y), F symétrique6x6, donnent un sous-espace de dimension21.
Ils préservent tous les couplages. Il suffit donc d'examiner 2^7=128
représentants du quotient. Le script construit une base de ce quotient
par élimination exacte et vérifie que la somme avec les cisaillements
engendre tout le noyau, sans hypothèse d'orbites supplémentaire.

Pour chaque représentant, il construit les sept W_i, leurs21 plans
d'intersection, et vérifie les105 couplages entre paires disjointes.
Un seul représentant passe. Sa Gram symplectique, multipliée par les
blocs [[0,1],[1,0]], donne bien un projecteur B de rang12. Aucun autre
cas n'est écarté sur un critère numérique ou heuristique.

### 4. Aucun relèvement des signes :136656 contradictions XOR

Dans le plan E_ij, les trois caractères du carré correspondent aux
trois vecteurs non nuls. Ceux associés aux indices i,j sont distincts,
et le troisième est leur somme. La projection modulo2 de M U_i=0
impose de choisir un vecteur non nul dans chacun des six E_ij avec
somme nulle dans V. Il y a exactement18 choix par i, obtenus en
énumérant les3^6 possibilités. Entre deux indices, leurs choix sur le
plan commun doivent être distincts. Il y a136656 affectations
compatibles aux sept indices.

Une fois ces choix fixés, le transport des caractères entre cellules
disjointes est fixé par B. Chaque appariement4x4 conserve seulement
deux bits de signes libres : le troisième signe est leur produit.
On a donc210 variables binaires. Pour une cellule e ne contenant pas i,
les quatre transports du caractère i venant des cellules f contenant i
et disjointes de e doivent avoir somme nulle dans M U_i. Dans l'unique
configuration survivante et pour chacun des18 choix, ils se regroupent
toujours en deux paires de même caractère (vérification exhaustive
finie). Chaque paire exige des signes opposés : une équation XOR
avec second membre1. Il y a30 équations par i, donc210 au total.

L'élimination binaire incrémentale trouve une contradiction pour les
136656 affectations, chaque fois à l'ajout du septième indice ; aucune
affectation complète ne survit. Le script utilise seulement les
équations de noyau M U_i=0, qui sont nécessaires. Il n'est donc même
pas nécessaire de vérifier ensuite toutes les équations quadratiques
réelles de M. Un exemple de certificat XOR (somme de membres gauches0,
second membre1) est conservé et vérifié directement dans le rapport.

**Artefacts de cette nuit.**

- `code/codex/night_20261014/grid_star_f2.py` : calcul autonome, entiers
  et bits uniquement, aucun paquet ni solveur externe ; vérification
  exhaustive des normalisations et des deux étapes finies.
- `data/codex_night_20261014/grid_star_f2.json` : bases du quotient,
  unique configuration, comptes, et premier certificat XOR.

**Portée exacte.** Tout sommet a au plus20 grilles passant par lui.
Cela ne prouve ni l'absence d'une grille ni l'exclusion de C1. Les
familles à moins de21 grilles demandent d'autres arguments. La preuve
de couverture mathématique est écrite ci-dessus ; le script est une
vérification exhaustive courte, pas un certificat formel Lean/Coq.

**Prochaine question.** Trouver si les contradictions XOR admettent une
formule de parité commune, puis assouplir la configuration des21 carrés.
Claude travaille indépendamment sur les sous-familles à moins de
grilles et sur un seul triangle à12 prismes. Dernier message envoyé627,
02h33 environ ; aucun retour d'accusé attendu.

## 04h20 — Reprise courte et contrainte spectrale sur TOUS les prismes

Nouvelle session après la panne : `01a13828-ddc7-74a1-9684-acd17b8ee4e9`.
Lectures de reprise limitées au log des huit commits et à ce journal ; les
anciennes notes de recherche n'ont pas été ouvertes. Le lecteur du pont a
été arrêté proprement, son état sauvegardé, reciblé puis relancé caché.
Messages LAB628–629 lus et acquittés ; message de vie630 envoyé. Le résultat
LAB « pas de K6 dans le graphe des grilles d'un sommet » est pris avec sa
portée annoncée, sans refaire son audit. La factorisation autour d'un
triangle n'a pas encore fourni de nouvelle exclusion locale.

**Nouveau théorème.** Soit R le graphe sur les231 triangles, deux triangles
étant adjacents lorsqu'ils forment un prisme (trois arêtes entre eux).
Sa matrice d'adjacence, aussi notée R, vérifie

    10I - R - M/138 - (2/13629)J >= 0,

au sens des matrices positives, où M est la Gram des q_T définie plus haut.
En particulier :

1. rho(R)<10 ; toute sous-famille non vide contient un triangle ayant au
   plus neuf partenaires DANS cette sous-famille. Le graphe R est donc
   9-dégénéré : l'effeuillage des degrés <=9 doit retirer tous les sommets.
2. sum_T (59 p(T)+2)^2 <= 231*590^2.
3. Le nombre total de prismes non ordonnés est au plus1150 (contre1151
   dans la première borne de cette nuit).

Ce sont des conditions nécessaires supplémentaires, pas une exclusion de
C1. La première borne porte sur chaque sous-famille et ne dit pas que tous
les degrés individuels p(T) sont <=9.

### Preuve par cubes sans trace

L'espace propre -4 a dimension44. Pour un vecteur x de cet espace,
écrivons g pour le tenseur métrique et posons

    h(x) = x tensor x tensor x
           - |x|^2/46 * (x_i delta_jk + x_j delta_ik + x_k delta_ij).

La contraction sur deux indices vaut zéro, et un calcul direct donne

    <h(x),h(y)> = <x,y>^3 - 3 |x|^2 |y|^2 <x,y>/46.

Puisque |q_T|^2=4, leur Gram harmonique est M^{circ3}-(24/23)M.
Sur les six relations (égalité, intersection, j=0,1,2,3 arêtes entre
triangles disjoints), les valeurs de M sont (4,0,1,0,-1,-2). Donc

    M^{circ3} = 60I + M - 6R,
    Gram(h(q_T)) = 60I - 6R - M/23.

Le tenseur V=sum_x u_x^{tensor3} a lui aussi une contraction nulle,
car |u_x|^2=28 et sum_x u_x=0. Les comptes déjà démontrés donnent

    |V|^2=1471932,
    <h(q_T),V>=<q_T^{tensor3},V>=3*64-36*8+60=-36.

Projeter chaque h(q_T) orthogonalement à V soustrait
1296/1471932 J = (4/4543)J à sa Gram. Sa positivité, divisée par6,
est exactement l'inégalité matricielle annoncée.

Posons beta=2/13629 et K=R+beta J. En oubliant le terme M/138>=0,
on obtient 10I-K>=0. K est symétrique à coefficients positifs, donc
son rayon spectral est <=10 et toutes ses valeurs propres sont dans
[-10,10] (on peut remplacer un vecteur par ses valeurs absolues dans
le quotient de Rayleigh). Or

    K1 = p + (2/59)1.

L'inégalité |K1|^2<=100|1|^2 donne exactement la contrainte quadratique.
Pour un total de1151 arêtes, la somme des degrés vaut2302 ; la convexité
entière minimise la somme des carrés avec223 degrés10 et huit degrés9.
Cela donne80426184 > 231*590^2 = 80411100. Les totaux supérieurs sont
également impossibles ; le maximum autorisé par ce seul test est1150.

Enfin un vecteur propre de Perron v>=0 non nul de R vérifie

    (10-rho(R))*|v|^2 >= beta*(sum v)^2 > 0.

D'où rho(R)<10. Une sous-famille dont tous les degrés internes sont >=10
contredirait cette borne par son quotient de Rayleigh.

### Filtre exact, utilisable pendant une recherche

`code/codex/night_20261014/prism_spectral_cut.py` accepte un JSON avec
`order` et `edges` d'un graphe PARTIEL de prismes, jusqu'à231 sommets.
Les degrés et arêtes déjà forcés suffisent : ajouter des arêtes ne peut
faire décroître ni le score quadratique ni le rayon spectral d'une
matrice symétrique non négative. Les sommets absents sont complétés par
des sommets isolés pour le score. Le filtre vérifie successivement la
borne12 des degrés, le score quadratique, l'absence d'un noyau de degré
minimum10, puis la coupure spectrale rationnelle.

Le dernier test exige B=10I-R>0 et

    1^t B^{-1}1 <= 13629/2.

C'est le complément de Schur de la matrice entière

    [[2B, 2*1], [2*1^t, 13629]].

Élimination de Bareiss, sans nombres flottants : tous les mineurs
principaux initiaux jusqu'à B doivent être positifs, le dernier peut
être nul. C'est équivalent au test 10I-R-beta J>=0 dans notre classe
non négative. Sur une sous-famille, c'est une condition principale
nécessaire ; sur un sous-graphe partiel, la monotonie de Perron assure
la couverture. La réussite du filtre n'est jamais un témoin de C1.

**Contrôles courts.** Formule harmonique vérifiée directement en
coordonnées, dont la dimension44 ; six relations vérifiées en fractions ;
borne entière calculée exhaustivement. Le filtre spectral rejette K(9,12)
malgré son noyau de degré minimum10 vide. Un graphe circulant de degré10
sur231 sommets, privé de quatre arêtes disjointes, passe l'ancienne borne
de moyenne mais échoue à la nouvelle contrainte quadratique. Ces graphes
sont des contrôles du filtre, pas des types locaux réalisables de C1.
Exécution autonome :0,4s environ, sans paquet externe ni solveur.
Rapport : `data/codex_night_20261014/prism_spectral_cut.json`.
## 04h37 — Une fermeture de prisme en P3 est impossible ; 598 types éliminés

**Lemme nouveau, élémentaire.** Soient deux triangles disjoints
T={a0,a1,a2}, U={b0,b1,b2} formant un prisme, avec arêtes transversales
ai-bi. Soit ci l'unique voisin commun de ai et bi. Alors les trois ci
ne peuvent pas induire un chemin P3 (exactement deux arêtes). Leur graphe
induit a zéro, une ou trois arêtes.

Les ci sont distincts et extérieurs au prisme. De plus ci ne touche aucun
aj,bj pour j!=i : sinon une arête de T ou U aurait deux voisins communs.
Supposons c0-c1-c2 un P3. Le sous-graphe S sur ces neuf sommets a17 arêtes.
Ses degrés sont4 sur les six ai,bi et sur c1, et3 sur c0,c2. Posons s=1_S,

    f = (3I-A)s + 1.

Les seules équations A²+A=12I+2J et A1=14*1 donnent

    Af=-4f, sum f=0,
    |f|² = 21*9 -7*(2*17) +2*9² -22*9 +99 =14.

Sur S, f vaut1 aux deux extrémités c0,c2 et0 ailleurs. Hors S, f vaut
1-d_S(x). Ainsi toutes ses coordonnées positives valent1. Sa masse
positive totale est au plus7, puisque f est entier, de somme nulle et
|f|²=14. Si f_x<=-2, l'équation Af=-4f exigerait une somme >=8 dans son
voisinage, impossible avec une masse positive totale <=7. Donc f est
exactement +1 sur sept sommets, -1 sur sept, et0 ailleurs.

Chaque sommet négatif a au moins quatre voisins positifs. En comptant
les paires positives partageant un sommet négatif, on obtient au moins
7*C(4,2)=42 incidences. Les21 paires positives ont chacune au plus deux
voisins communs dans tout G : au plus42 incidences au total. Il y a donc
égalité partout ; aucune paire positive ne peut avoir de voisin commun
hors du support négatif. Or c0,c2 sont positifs et ont déjà le voisin
commun c1 de valeur0. Contradiction. Aucun catalogue de supports ni
solveur n'intervient dans cette preuve.

### Conséquence forte pour un triangle à douze prismes

Dans la normalisation Xa-Xb=Xa-Xc=identité, p(T)=12 impose également
Xb-Xc=identité. On a douze triangles Ui={a_i,b_i,c_i}. Les trois
appariements internes de Xa,Xb,Xc deviennent Ma,Mb,Mc sur douze indices.

Si Ma et Mb contiennent tous deux l'arête {i,j}, les deux triangles
{a,a_i,a_j}, {b,b_i,b_j} forment un prisme. Les trois sommets qui
complètent leurs arêtes transversales sont c,c_i,c_j. Les deux arêtes
c-c_i et c-c_j existent. Le lemme impose c_i-c_j, donc Mc contient
également {i,j}. Même raisonnement pour chaque paire de couleurs :

    une arête présente dans deux appariements est présente dans les trois.

Le multigraphe cubique coloré Ma+Mb+Mc est donc une réunion de graphes
cubiques simples et de composantes isolées à deux sommets et trois arêtes
parallèles. Il n'a aucune arête de multiplicité exactement deux.

**Réduction calculée :790 types ->192 types nécessaires.** Un programme
standard-library autonome retrouve les790 classes à permutation des
indices et des trois couleurs près, puis en élimine598 par ce seul lemme.
Les192 survivants se répartissent selon le nombre de composantes triples :
157 avec0,23 avec1,8 avec2,2 avec3,1 avec4 et1 avec6. Ce sont des types
locaux non éliminés, jamais des témoins de Conway. Aucun des192 types
n'est déclaré complétable, et la famille p(T)=12 reste ouverte.

**Couverture finie.** Fixer Ma=(01)(23)...(10,11). La réunion de Ma,Mb
est une réunion de cycles alternés, dont les demi-longueurs forment une
partition de6 (onze possibilités). Pour chacun des onze couples standards,
on parcourt les10395 appariements Mc. Le stabilisateur du couple est
engendré par la rotation de deux crans et la réflexion de chaque cycle,
et par les échanges de cycles de même longueur ; ces générateurs sont
construits explicitement. Le parcours des orbites couvre chaque fois les
10395 appariements, et donne3580 classes à couleurs ordonnées. Les deux
échanges de couleurs adjacentes engendrent S3 ; la renormalisation des
cycles alternés puis l'union des classes donne790 classes. Le critère
« aucune multiplicité deux » est invariant sous tous ces changements.
Il reste724 classes à couleurs ordonnées,192 après oubli des couleurs.
Les représentants sont conservés dans le JSON.

**Coupure SAT directement disponible.** Avec Ma fixé et B_ij,C_ij les
variables des deux autres appariements :

- sur les six arêtes de Ma, imposer B_ij=C_ij (douze clauses binaires) ;
- sur les soixante autres paires, imposer non(B_ij et C_ij) (soixante clauses).

Les72 clauses binaires sont exportées en DIMACS. Ce fichier est uniquement
la nouvelle coupure ; il suppose que le modèle appelant impose déjà les
deux appariements parfaits. La satisfaction de ces clauses a été comparée
au critère combinatoire sur les3580 représentants à couleurs ordonnées.

Artefacts : `code/codex/night_20261014/prism_closure_types.py`,
`data/codex_night_20261014/prism_closure_types.json`,
`data/codex_night_20261014/prism12_no_double_cut.cnf`.
Exécution complète :0,7s environ. Verdict et preuve courte transmis à LAB
au message632. Aucun calcul payant ni relance d'une campagne UNKNOWN.

**Autre structure de p(T)=12 pour la suite.** Chaque sommet y parmi les
60 non-voisins de T touche six sommets de X, deux dans chaque Xa,Xb,Xc.
Ces six voisins sont deux à deux non adjacents : une paire d'un même X
ne peut être son arête d'appariement, et y ne touche qu'un sommet de chaque
triangle Ui. Dans les sept arêtes du voisinage de y, ces six voisins de
X sont donc appariés à six voisins distincts de Y ; les deux derniers
voisins de Y sont appariés ensemble. Ainsi G[Y],8-régulier, possède
exactement vingt triangles qui partitionnent ses60 sommets. Les autres
arêtes de G[Y] forment un graphe6-régulier, et chacune de ces arêtes a
son unique voisin commun dans X. Cela peut servir à une réduction de la
complétion des192 types ; aucune borne abordable sur cette complétion
n'est encore démontrée.
## 04h56 — Extension à tout triangle et propagation dans les tuiles locales

Le tour précédent est un progrès vérifié : lemme P3 et exclusion598/790,
commit dcef9ae. LAB633 a confirmé le lemme et proposé sa lecture sur les
quatre couplages d'une grille locale. Le présent prolongement s'applique
sans hypothèse p(T)=12 et sans exclure préalablement les co-Heawood.

**Tous les partenaires de prisme de T sont disjoints.** Si U,V en
partageaient un sommet x, voisin de t_i dans T, les non-adjacents x,t_j
(j!=i) auraient trois voisins communs : t_i et les deux sommets distincts
de U,V voisins de t_j. C'est impossible.

**Alignement forcé.** Écrire T={t_i}, U={u_i}, V={v_i}, avec arêtes de
prisme t_i-u_i et t_i-v_i. Une arête u_i-v_j pour i!=j donnerait aux
non-adjacents u_i,t_j les trois voisins communs t_i,u_j,v_j. Donc les
arêtes U-V possibles sont uniquement u_i-v_i, i=0,1,2.

**Exactement deux arêtes U-V est impossible.** Dans ce cas S=T+U+V a
neuf sommets et17 arêtes ; f=(3I-A)1_S+1 a norme14, vaut1 aux deux
sommets u_k,v_k non couplés et0 aux autres sommets de S. Les deux positifs
partagent t_k de valeur0 : la même preuve de saturation que pour la
fermeture P3 donne la contradiction. Les prétendus cas « tordus » de
(3,3,2) sont déjà écartés par l'alignement et mu=2 ; précision transmise
à LAB634. Aucun cas co-Heawood n'est laissé ouvert pour ce motif précis.

Ainsi, si R désigne toujours le graphe des prismes, on a les zéros
supplémentaires

    (R²)_{TU}=0 si T,U se rencontrent,
    (R²)_{TU}=0 si T,U sont disjoints avec exactement deux arêtes entre eux.

Sur les p(T) partenaires d'un triangle quelconque, les arêtes de G entre
triangles partenaires forment trois appariements PARTIELS alignés. Leur
multigraphe est simple de degré au plus3, sauf composantes isolées à
arêtes triples. En particulier, le voisinage d'un sommet de R induit un
appariement : chaque arête de R appartient à au plus un triangle de R.
Les partenaires restants ne sont pas déclarés complétables.

**Clauses pour les partenaires.** Pour chaque paire de partenaires déjà
identifiés, les six arêtes non alignées sont interdites (clauses unités).
Pour les trois arêtes alignées e0,e1,e2, interdire exactement deux valeurs1 :

    (!e0 or !e1 or e2), (!e0 or e1 or !e2), (e0 or !e1 or !e2).

Ces clauses peuvent propager dès que deux des trois états sont connus.
Elles généralisent les72 clauses spécialisées du cas p(T)=12.

**Quatre couplages autour d'un sommet (lecture LAB633).** Dans les quatre
sommets Q_ij associés à deux droites du voisinage de v, les quatre arêtes
du carré sont les quatre couplages locaux aux extrémités des deux droites.
Trois couplages vrais imposent le quatrième. Sinon les neuf sommets
forment une grille privée d'une arête :17 arêtes, deux sommets de degré3,
les sept autres de degré4. Les deux sommets de degré3 partagent le troisième
point de leur droite, de degré4. Le vecteur f de norme14 donne encore la
contradiction. Les diagonales supplémentaires sont déjà interdites par
lambda=1 à partir des trois arêtes du carré.

Pour chaque quadruplet de variables, quatre clauses de longueur4
interdisent exactement trois valeurs1. Il y a21 tuiles, donc84 clauses
par sommet racine dont les84 sommets extérieurs sont déjà coordonnés.
Si tous les voisinages sont coordonnés, cela donne8316 clauses avant
suppression des doublons. Ce compte ne suppose pas que ces coordonnées
soient disponibles dans n'importe quel modèle global.

**Artefact.** `code/codex/night_20261014/local_prism_propagation.py` fournit
les constructeurs de clauses et les contrôles exacts, sans solveur externe.
Il parcourt les34 appariements possibles entre les triangles extrêmes de
deux prismes normalisés :26 sont éliminés par les nombres de voisins
communs, trois par le vecteur de norme14, cinq passent ces seules conditions
(zéro arête, une arête de trois façons, ou trois arêtes). Il vérifie aussi
les quatre grilles privées d'une arête et les tables de vérité des clauses.
Le rapport est `data/codex_night_20261014/local_prism_propagation.json`.
Exécution :0,06s. Il s'agit de propagation nécessaire, pas d'une nouvelle
campagne UNKNOWN ni d'une exclusion de la famille des192 types restants.

## 05h27 — Vecteurs entiers minimaux : angle interdit et au plus 28 racines orthogonales

Résultat nouveau de cette reprise, indépendant des campagnes SAT. On conserve
`P=(27I-9A+J)/63`, projecteur orthogonal sur l'espace propre -4, de dimension 44.
Il ne s'agit pas d'une exclusion de C1 ni d'un co-Heawood isolé.

**1. Minimum entier.** Tout vecteur entier non nul `f` tel que `Af=-4f`
a une norme carrée au moins 14. En effet `sum f=0`. Si `a=max |f_v|`,
la masse de chaque signe est au moins `4a`, donc `||f||²>=8a`.
Pour une norme au plus 14, toutes les entrées non nulles valent donc +1 ou -1.
Avec `p` entrées de chaque signe, chaque sommet négatif a au moins quatre
voisins positifs. Le comptage des paires positives donne

    6p <= 2*C(p,2), donc p>=7.

À la norme 14, toutes ces inégalités sont des égalités : les deux supports
de taille sept sont indépendants, le graphe entre eux est 4-régulier et
chaque paire d'un côté a deux voisins communs de l'autre côté. C'est le
complément de l'incidence du plan de Fano, donc le co-Heawood.
Chaque sommet extérieur a au plus un voisin dans chaque signe, et autant
dans les deux signes : zéro ou un de chaque. La réciproque pour un
co-Heawood induit découle du quotient de Rayleigh égal à la valeur propre
minimale -4.

**2. L'angle de produit scalaire 7 est impossible.** Soient `f,g` deux tels
vecteurs de norme 14, distincts et non opposés. Le minimum précédent impose
`|f.g|<=7`. Supposons `f.g=7`, quitte à changer le signe de `g`. Alors
`h=f-g` est encore de norme 14. Il ne peut avoir d'entrée de valeur absolue
deux : les supports de `f,g` se rencontrent donc en exactement sept sommets,
avec les mêmes signes. Écrivons `I` pour l'intersection, `F` pour le support
propre de `f`, et `G` pour celui de `g`; chacun a sept sommets.

Pour un sommet de `G` de signe epsilon dans `g`, ses voisins dans `I`
doivent avoir le signe -epsilon, et ses voisins dans `F` le signe epsilon
(en utilisant `h`). Comme il est extérieur au co-Heawood de `f`, il a au
plus un voisin de chaque signe dans `I+F`. Ses degrés dans les supports de
`g` et `h` valent tous deux quatre; son degré dans `G` est donc au moins
trois. Or le graphe induit sur `G` est biparti sur sept sommets, avec degré
minimum trois. Ses parts ont tailles trois et quatre, et les quatre sommets
d'une part sont tous joints aux trois de l'autre. Deux d'entre eux ont
trois voisins communs, contradiction à mu=2. Ainsi

    f != +/-g  =>  |f.g| <= 6.

Cela interdit notamment deux co-Heawoods partageant exactement sept sommets
avec des bipartitions compatibles. Une intersection de taille sept avec
des signes incompatibles n'est pas exclue par cet argument.

**3. Toute famille orthogonale a au plus 28 membres, à un signe près.**
Plaçons les vecteurs de norme 14 d'une telle famille dans les colonnes de
`F`, posons `R=F F^t`, et notons `k_v=R_vv` le nombre de supports passant
par `v`. Les relations `AR=-4R`, `R²=14R`, `R1=0` donnent, pour la matrice
entière `T=2A-6I+R`,

    T1=22*1,  T²=8J-14T,  T_vv=k_v-6.

Par conséquent,

    sum_{w!=v} T_vw*(T_vw-1) = 28-k_v*(k_v+1).

Chaque terme du membre de gauche est non négatif, puisqu'il est entier.
Donc `k_v<=4` pour tout sommet, et `14*r=sum k_v<=396`, soit `r<=28`.
Cette borne vaut pour toute famille orthogonale de co-Heawoods signés,
sans hypothèse de provenance dans un réseau particulier.

**4. Application au réseau entier naturel.** Considérons

    L = { (7P c)/sqrt(7) : c entier, sum(c) multiple de 9 }.

Si `sum(c)=9k`, alors `f=7Pc=(3I-A)c+k*1` est entier. Le réseau `L`
est entier et pair, car le produit de deux de ses vecteurs vaut

    3*c.d-c^t*A*d+sum(c)*sum(d)/9,

et la norme est paire par réduction modulo deux. Une racine de norme deux
correspond donc à un `f` de norme 14. Entre deux racines distinctes non
opposées, `f.g` est multiple de sept; le point 2 force `f.g=0`.
Le système de racines est ainsi `A_1^r`, avec `r<=28`, donc au plus 56
racines en comptant les deux signes. **La condition d'antécédent entier
sur c est nécessaire ici : nous ne prétendons pas que tous les co-Heawoods
de C1 sont mutuellement orthogonaux.**

**Contrôles.** `integral_root_obstructions.py` vérifie exactement les
identités dans l'algèbre engendrée par `I,A,J,R`, le comptage de norme minimale,
le petit obstacle biparti, et l'incidence complémentaire du plan de Fano.
Le rapport est `data/codex_night_20261014/integral_root_obstructions.json`.
Exécution réussie en 0,05 s, sans solveur externe. Les contrôles finis
accompagnent les preuves ci-dessus; ils ne sont pas un certificat SAT global.

**Autres observations de ce tour.** Le théorème N9 communiqué par LAB au
message 635 (aucun neuf-ensemble à 17 arêtes) a été lu et acquitté. Sur le
squelette fixé des 192 types à douze prismes, il retrouve seulement la coupe
« pas exactement deux appariements superposés » : aucune nouvelle exclusion
n'est annoncée. Enfin une grille consomme six paires de droites en prisme,
et une telle paire détermine sa grille de manière unique par les troisièmes
sommets de ses trois arêtes transversales. La borne globale de 1150 prismes
donne donc **au plus 191 grilles**.

## 05h56 — Intersections orthogonales et exclusion de trois co-Heawoods sur une arête

**Verdict.** Une arête de C1 ne peut appartenir à trois co-Heawoods dont
les vecteurs signés sont deux à deux orthogonaux. Le troisième forcerait
un quatrième; cette dernière famille est exclue par une réduction exacte
à 16 cas locaux, puis 15552 lignes d'incidence possibles. Aucun solveur SAT
n'est utilisé. Un co-Heawood isolé et C1 restent ouverts.

### A. Un petit lemme de norme 28

Pour un vecteur entier `h` de l'espace -4, de norme carrée 28, soit `a`
la plus grande valeur absolue. La masse `M` de chaque signe vérifie `M>=4a`,
et le coefficient de valeur absolue `a` ajoute `a²-a` à la norme l1.
Donc `28>=a²+7a`, d'où `a<=2`. Si `t` est le nombre total de coefficients
de valeur absolue deux, on a `M+t=14`.

Deux coefficients +2 demanderaient chacun une masse négative voisine d'au
moins huit. Leurs voisinages ont au plus deux points communs, donc une
masse commune au plus quatre : `M>=12`, puis `t<=2`. Les deux coefficients
de valeur absolue deux seraient alors précisément ces deux coefficients
positifs. La masse négative commune serait au plus deux, d'où `M>=14`,
contradiction à `M+t=14`. Il y a donc **au plus un +2 et au plus un -2**.
Les trois types, à changement de signe près, sont :

    14(+1),14(-1) ; 1(+2),11(+1),13(-1) ;
    1(+2),1(-2),10(+1),10(-1).

### B. Deux co-Heawoods orthogonaux partagent 0, 2 ou 4 sommets

Appliquer A à `f+g` et `f-g` montre qu'il y a au plus un sommet de chacun
des quatre types de signes `++,+-,-+,--` dans l'intersection. L'orthogonalité
équilibre les produits de signes, d'où les tailles 0, 2 ou 4.

**À la taille quatre, les deux couples de signes opposés sont des arêtes.**
Tous les autres couples sont non adjacents, car ils partagent un même signe
dans au moins un co-Heawood. Supposons les points `u=++`, `v=--` non adjacents.
Le vecteur entier

    h=7P(e_u-e_v)-f-g

a norme 14, est orthogonal à `f,g`, et vaut +1 en u, -1 en v. Nous aurions
donc trois co-Heawoods orthogonaux contenant u et v avec ces mêmes signes.
Dans chacun, u a quatre voisins négatifs. Ces douze voisins sont distincts :
une répétition donnerait un deuxième sommet de type `--` pour une paire
de vecteurs, alors que v occupe déjà ce type. Les deux voisins communs de
u et v sont extérieurs aux trois supports, puisqu'un support biparti ne
contient pas de voisin commun à deux points de signes opposés. Ils occupent
les deux places restantes dans le voisinage de u.

Chacun de ces deux voisins communs a déjà son unique voisin positif u et
son unique voisin négatif v dans chaque support. Il ne peut donc rencontrer
aucun des douze autres voisins de u. Le voisinage de u étant sept arêtes
disjointes, les deux voisins communs doivent être adjacents entre eux.
Leur arête aurait alors u et v comme deux voisins communs, contradiction.
Ainsi l'intersection de taille quatre induit exactement **deux arêtes
disjointes**, entre signes opposés. Aucun antécédent entier dans L n'est
nécessaire pour ce résultat.

### C. Trois vecteurs orthogonaux sur une arête en forcent quatre

Orienter les trois vecteurs pour qu'ils valent +1 en u et -1 en v, avec
`u~v`. Le vecteur `d=7P(e_u-e_v)` est entier, de norme carrée 56, et son
produit avec chacun des trois vecteurs vaut 14. Donc

    f_4=d-f_1-f_2-f_3

est un quatrième vecteur entier de norme 14, orthogonal aux trois premiers,
et il vaut également +1 en u et -1 en v.

### D. Quatre vecteurs sur une arête : seulement 16 squelettes

Supposons désormais quatre vecteurs `f_i`, `i=0..3`, valant +1 en u et -1
en v. Pour chaque paire i,j, le point B impose un point `q_ij` de signe
positif dans i, négatif dans j, et le point `q_ji` de signes opposés;
ces deux points sont adjacents. Les douze `q_ij` sont distincts et n'ont
aucun autre signe non nul : un troisième signe répéterait un type déjà
occupé par u ou v pour l'une des paires de vecteurs.

Chaque support conserve trois points positifs propres et trois négatifs
propres. Notons `P_i`, `N_i` ces groupes de trois. Les voisins de u sont
v, les douze points des `N_i`, et le troisième point d de l'arête uv.
Symétriquement pour v et les `P_i`. Le point d ne rencontre aucun autre
point des quatre supports, ayant déjà un voisin de chaque signe dans chacun.
L'union avec d compte donc **39 sommets**.

Pour i!=j, le point `q_ij` rencontre deux des trois points de `N_i`;
ce sont ses deux voisins communs avec u. Le point exceptionnel de `N_i`
doit avoir, dans le support j, un voisin négatif dans `N_j`, car son voisin
positif est déjà u. Ce voisin est nécessairement son partenaire dans le
voisinage de u. Chaque point de `N_i` peut être exceptionnel pour un seul j.
On peut ainsi les nommer `n_ij`, avec `n_ij~n_ji`, et
`q_ij~n_ik` exactement lorsque k!=i,j. La même argumentation donne
`p_ij~p_ji`, et `q_ij~p_jk` exactement lorsque k!=i,j.

Dans le support i, chaque `q_ij` est joint à `q_ji` et à exactement un
autre `q_ki`. Cela définit un dérangement des trois indices différents de i,
donc un cycle `epsilon_i` de longueur trois, avec deux choix. Le comptage
des deux voisins communs des points positifs `p_ij` et `q_ik` impose
`n_ij~p_i,epsilon_i^(-1)(j)`. Il reste donc `2^4=16` configurations.

Les seules arêtes encore possibles entre les `q` concernent des indices
disjoints. Pour `q_ij`, poser `k=epsilon_i(j)` et `l=epsilon_j^(-1)(i)`.
Si k=l, ses signes dans les autres supports sont déjà équilibrés et ces
deux arêtes sont interdites. Si k!=l, l'équilibre impose l'arête vers `q_lk`.
Le script ajoute ces arêtes puis contrôle toutes les équations `Af_i=-4f_i`.
Six cas échouent. Huit autres dépassent lambda=1 ou mu=2. Les deux derniers
sont explicitement isomorphes par permutation des quatre indices.

Il reste un graphe induit unique de 39 sommets et 117 arêtes, de degrés
`14^2,7^12,5^24,2^1`. Le code produit sa liste d'arêtes et l'isomorphisme.

### E. Aucun voisin extérieur possible pour d

La matrice principale `B=27I-9A_S+J`, d'ordre 39, a un noyau de dimension
cinq calculé sur les rationnels. Pour toute base entière c de ce noyau,
la positivité du projecteur global force `Pc=0`, même hors du squelette.
Un sommet extérieur z doit donc satisfaire

    sum_{x~z, x in S} c_x = sum(c)/9.

Supposons `z~d`. Comme u et v ont déjà leurs quatorze voisins, z ne leur
est pas adjacent. Les deux voisins communs de z avec u, respectivement v,
sont d et exactement un point n des douze N, respectivement un point p
des douze P. Sa partie restante dans S est un sous-ensemble des douze q.
Le sommet z étant extérieur à chaque co-Heawood, il rencontre au plus un
point positif et un point négatif de chacun, en nombres égaux. Sur les
arcs q_ij, cela signifie un sous-ensemble avec degrés entrant et sortant
au plus un. Il y en a **108**, obtenus en parcourant les 4096 masques.

Le script parcourt donc exactement `12*12*108=15552` lignes. Parmi elles,
1512 équilibrent les quatre signes et 864 respectent aussi le plafond d'un
voisin de chaque signe. **Aucune des 864 ne satisfait les cinq équations
du noyau principal.** Or d n'a que deux voisins dans S et doit en avoir
douze au dehors. Contradiction. La famille de quatre est exclue, donc aussi
celle de trois par C.

**Reproduction.** `orthogonal_root_intersections.py` effectue en 0,11 s
les calculs exacts : 16 configurations, isomorphisme explicite, base entière
du noyau, et toutes les lignes d'incidence. Le rapport
`orthogonal_root_intersections.json` contient les témoins d'échec des 14 cas
locaux et les cinq vecteurs du noyau avec leurs seconds membres.
`four_root_edge_graph.txt` contient le squelette avant exclusion.

**Contrôle exploratoire distinct.** Le programme C++ `dense_nine_scan.cpp`
a parcouru ses 211915132 sous-ensembles de neuf sommets en 0,39 s : maximum
14 arêtes. Le résultat est dans `four_root_edge_dense9.json`. N9 n'exclut
donc pas ce squelette; c'est bien l'extension par les équations du projecteur
qui donne la contradiction. Le binaire est temporaire et n'est pas commité.

**Relais LAB lu à 06h00 (messages 637–638, acquittés).** LAB annonce une
voie par formes modulaires et certificats de Farkas rationnels : rang sur
F7 de `A+4I` au moins 31, après exclusion de ses paramètres b<=26 puis
b=28 (commit LAB `4f661d9`). Les entrées annoncées sont au moins 462
vecteurs de norme 4 et 14970 de norme 8 dans son réseau A, au plus 7920
co-Heawoods signés dans son réseau B, puis au plus 360360 vecteurs de
norme 16 contre plus d'un million exigés pour b=28. La marche suivante
b=30 demanderait, selon LAB, une borne sur les vecteurs de norme 24 de B
(environ trente millions exigés) ou de norme 12 de A (environ 140 millions).
Résultats de pair intégrés sans relancer un audit ni ouvrir les anciennes
notes. Notre exclusion d'arête a été transmise au message 639.

### 06h12 — Intersections orthogonales : supports 0 ou 4, au plus 12 racines

**Résultat exact.** Deux vecteurs entiers orthogonaux de norme 14 de l'espace
propre -4 ont des supports disjoints ou une intersection de quatre sommets.
Trois tels supports ne passent jamais par un même sommet. Toute famille
orthogonale contient donc **au plus 12 vecteurs**, et le système de racines
du réseau L décrit à 05h27 est `A1^r`, avec **r<=12**, soit au plus 24 racines
en comptant les opposés. La borne précédente r<=28 est remplacée.

Le nouveau calcul fini prouve deux faits intermédiaires : l'intersection de
taille deux est impossible; trois supports passant par v doivent avoir une
arête commune. Ce second cas est exclu par le théorème de 05h56, commit
`234fac5`. La dépendance est explicite : ce calcul d'incidences seul laisse
survivre des configurations qui partagent une arête.

**Coordonnées locales exhaustives.** Fixons v. Ses 14 voisins sont sept
paires. Chacun des 84 autres sommets est l'unique second voisin commun
Q_ab d'une paire de voisins a,b de v qui ne sont pas appariés. Cela utilise
seulement lambda=1 et mu=2 et donne les 99 étiquettes sans ambiguïté.

Orientons une racine f par f(v)=1. Elle choisit quatre voisins négatifs N
de v dans quatre paires différentes. Ses six autres sommets positifs sont
les six Q_ab pour {a,b} inclus dans N. Les trois sommets négatifs restants
sont des Q_ab qui apparient les six extrémités des trois paires inutilisées,
sans employer une paire initiale. En effet, un voisin de v hors du support
doit avoir exactement un voisin de chaque signe; les partenaires des quatre
voisins négatifs ont déjà leur voisin négatif. Les six autres voisins de v
sont donc couverts exactement une fois par les trois sommets négatifs Q.
Il y a huit appariements admissibles, d'où `C(7,4)*16*8 = 4480` supports.

Pour chaque support, il reste exactement six graphes internes possibles.
Un sommet négatif Q doit toucher quatre des six Q positifs. Vu comme quatre
arêtes du K4 sur N, ce choix est un cycle de longueur quatre : ses deux
arêtes omises forment un couplage parfait. Les trois Q négatifs doivent
omettre les trois couplages parfaits différents. Il reste donc 3! choix.
Les autres arêtes du co-Heawood sont déjà fixées par les coordonnées.

**Filtrage des supports.** Le lemme de norme 28 de 05h56 borne chaque
intersection de signes (++,+-,-+,--) à un sommet. Avec v commun positif,
l'orthogonalité donne une intersection totale de taille deux ou quatre.
Si elle a taille quatre, les signes opposés sont adjacents (lemme de 05h56),
donc l'éventuel sommet négatif commun est dans N(v). Ces conditions laissent
528 supports compatibles avec un premier support fixé, puis 8784 triples
contenant ce premier support. Le groupe local agit transitivement sur les
4480 premiers supports. Le stabilisateur de celui fixé a ordre 144 : les
24 permutations des quatre paires sélectionnées, et les six automorphismes
des trois autres paires préservant leur couplage choisi.

Il reste huit orbites de paires et 64 orbites de triples. Pour chaque
orbite, les 6^2 ou 6^3 incidences internes sont toutes couvertes. On rejette
une arête également imposée comme non-arête, un sommet extérieur ayant deux
voisins de même signe dans un co-Heawood, ou un excès de voisins communs.
Les rejets se produisent déjà avec les deux premières règles. Deux orbites
de paires survivent, toutes deux avec intersection de taille quatre. Une
orbite de triples survit, avec arête commune : 72 supports étiquetés et 40
choix internes pour le représentant. Aucun triple sans arête commune.

**Vérification sans quotient.** L'option `--labelled-audit` parcourt aussi
les 312 paires et 8712 triples sans voisin négatif commun, sans réduction par
le stabilisateur; aucun ne survit. Le contrôle total se termine localement
en moins d'une minute. Le calcul supplémentaire des quadruples (53 orbites)
ne laisse lui aussi que l'arête commune; il n'est pas nécessaire à la borne.
Un co-Heawood isolé garde bien ses six incidences possibles dans le même
modèle, ce qui contrôle que les règles ne rejettent pas par construction.

**Borne globale.** Dans une famille orthogonale de r supports, chacun a 14
sommets et chaque intersection non vide contient quatre sommets. Aucun
sommet ne pouvant appartenir à trois supports, les intersections à l'intérieur
d'un support sont disjointes. Le graphe d'intersection des supports a donc
degré au plus trois. S'il a e arêtes, leur union a exactement `14r-4e`
sommets, au moins `8r`. Puisque l'union est dans les 99 sommets, r<=12.
En cas r=12, ce graphe doit être cubique et l'union a 96 sommets : 72 sommets
doubles, 24 privés et trois hors de tous les supports. Ce cas n'est pas exclu
par la borne; il offre une nouvelle famille très contrainte à examiner.

Fichiers : `orthogonal_root_stars.py`, rapport exact
`data/codex_night_20261014/orthogonal_root_stars.json`. Aucun SAT, aucun
flottant, aucune hypothèse de symétrie globale de C1. C1 reste ouvert.

### 06h25 — Petits vecteurs entiers et angles de tous les co-Heawoods

**Résultats prouvés.** Tout vecteur entier h de valeur propre -4 et de norme
carrée au plus 24 a ses coordonnées dans {0,+1,-1}. Pour deux co-Heawoods
signés f,g distincts et non opposés, les seules valeurs absolues possibles
de leur produit scalaire sont **0, 1, 2, 4**. Si sa valeur absolue est quatre,
leur intersection est un C4, et les signes y coïncident après orientation.
Si elle vaut deux, leur intersection contient exactement deux sommets, un de
chaque signe, là aussi avec signes concordants. Aucune existence de ces
configurations survivantes n'est affirmée.

**Lemme sur les coordonnées.** Soit M la masse totale de chaque signe, et
a=max|h_v|. L'équation propre au sommet extrémal donne M>=4a, donc
`||h||^2 >= a^2+2M-a >= a^2+7a`. Une norme <=24 impose a<=2. Si t est
le nombre d'entrées de module deux, `||h||^2=2(M+t)`. Deux entrées +2
exigeraient une masse négative >=8+8-4=12, car elles ont au plus deux voisins
communs, de poids au plus deux. Cela contredit M+t<=12 avec t>=2. De même
pour deux entrées -2. Restent, à changement de signe près, les cas suivants.

1. Une entrée +2, aucune -2 : M<=11. Le sommet u de valeur +2 ne peut être
   adjacent à une entrée positive x. Sinon la masse négative voisine de u
   est >=9, celle requise par x est >=6, et leur unique voisin commun peut
   porter au plus deux unités négatives. La masse négative disponible pour x
   est alors <=2+(M-9)<=4, contradiction. Donc u touche exactement huit
   entrées -1. Chacune des M-2 entrées +1, non adjacente à u, doit toucher
   au moins deux des M-8 entrées négatives restantes. Pour M<10, c'est
   impossible. Pour M=10, les huit +1 touchent toutes la même paire négative,
   contre mu=2. Pour M=11, neuf +1 choisissent au moins une paire parmi trois
   sommets négatifs, mais ces trois paires ne peuvent avoir ensemble que six
   voisins communs. Contradiction dans tous les cas.

2. Une +2 en u et une -2 en w : M<=10, avec M-2 entrées unitaires de chaque
   signe. Le même argument interdit les voisins de même signe de u et w.
   S'ils ne sont pas adjacents, l'équation de u impose M=10 et ses huit
   voisins négatifs unitaires; w touche de même les huit +1. Tout +1 a alors
   exactement deux voisins -1 et aucun voisin positif, par mu=2 avec u;
   symétriquement les huit -1 sont indépendants. Cela donnerait huit voisins
   indépendants dans N(u), qui est une réunion de sept arêtes : impossible.
   S'ils sont adjacents, u touche six des négatifs unitaires N1, w six des
   positifs unitaires P1. Pour M<=9, chaque sommet de P1 doit toucher au moins
   un négatif hors N1 : son voisin w occupe déjà une des deux places communes
   avec u. S'il n'en reste aucun, contradiction; s'il en reste un, il est
   voisin des six sommets de P1, tout comme w, contre mu=2.
   Enfin M=10 laisse deux positifs P0 et deux négatifs N0 hors P1,N1. Chaque
   sommet de P0 doit toucher les deux N0 et exactement deux N1, par son
   équation propre et mu=2 avec u; symétriquement chaque N0 touche les deux
   P0 et exactement deux P1. Il n'y a donc que quatre arêtes entre P1 et N0.
   Mais chacun des six P1 en requiert au moins une, comme ci-dessus. Impossible.

**Angles.** Après orientation, écrivons d=f.g>=0. Le minimum entier de norme
14 donne d<=7 pour des racines distinctes. Si d>=2, h=f-g a norme
`28-2d<=24`, donc aucune coordonnée de module deux. Sur l'intersection I
de leurs supports, f et g ont donc le même signe, et |I|=d. Dans le
co-Heawood de g, chaque sommet extérieur au support de f peut avoir au plus
un voisin dans I : ses voisins dans I auraient tous le même signe de f.
Le sous-graphe induit par supp(g)\I a donc degré minimum au moins trois.

L'énumération exacte des 16383 sous-ensembles non vides d'un co-Heawood donne
les nombres de tels sous-graphes par taille : 21 de taille 10, 49 de taille
12, 14 de taille 13, un de taille 14, et aucun autre. Les 21 compléments de
taille quatre sont tous des C4; les 49 compléments de taille deux ont un
sommet dans chaque partie. Cela exclut d=3,5,6,7 et précise d=2,4. La borne
générale |f.g|<=6 de 05h27 est donc remplacée par |f.g|<=4, avec le trou 3.

**Contrainte supplémentaire pour les petites couches entières.** Si h a
p entrées +1 et p entrées -1, les deux graphes induits par les signes ont le
même nombre e d'arêtes. En notant d_x le degré dans son propre signe,
le comptage des voisins communs des p positifs donne exactement la nécessité
`9e + somme_x C(d_x,2) <= p(p-7)`, où x parcourt les deux signes. En effet,
les négatifs contribuent `6p+8e+somme_neg C(d_x,2)` et les positifs
`somme_pos C(d_x,2)`, contre au plus `p(p-1)-e`.
Pour p=7,8,9,10,11,12, cela borne e par 0,0,2,3,4,6. Aucun de ces deux
graphes n'a de triangle : trois sommets d'un même signe dans une droite
exigeraient trois ensembles disjoints d'au moins six voisins de l'autre
signe, alors que p<=12. En particulier une norme 24 entière signifie
exactement 12 coordonnées de chaque signe et au plus six arêtes dans chacun
de leurs graphes induits. Cela ne borne pas encore le nombre de ces vecteurs,
et ne traite pas les classes non entières du réseau B de LAB.

Code exact : `coheawood_angle_bound.py`; rapport
`data/codex_night_20261014/coheawood_angle_bound.json`. Le petit script vérifie
les paramètres des sept cas de coefficients et les sous-graphes du
co-Heawood; les arguments graphiques sur les coefficients sont ci-dessus.

**Relais LAB 641, lu et acquitté.** LAB annonce l'exclusion du paramètre
b=30, donc `rang_F7(A+4I)>=33`, par nouveaux minorants de couches dans A
issus de petits vecteurs entiers projetés (commits `4f8303e/d2e0ecc`,
certificat `cert_b30.json`). Il poursuit b=32, où la distinction des images
projetées au-delà du support huit se heurte aux prismes jumeaux. Contribution
de pair enregistrée; pas de réaudit ni de lecture d'anciennes notes.

**06h28, raffinement du comptage des petites couches.** Pour un sommet z
hors du support, ses nombres de voisins dans les deux signes sont égaux;
notons-les a_z. Les identités exactes SRG donnent, avec
`W=somme_x C(d_x,2)` sur les deux signes,

```
somme_hors_support a_z = 10p-4e,
somme_hors_support C(a_z,2) = p(p-7)-9e-W,
somme_hors_support (a_z-1)(a_z-2)/2 = p^2-19p+99-5e-W.
```

Le dernier membre de gauche est non négatif pour tout entier a_z>=0.
Donc **5e+W <= p^2-19p+99**, qui améliore les bornes sur e aux valeurs
**0,0,1,1,2,3** pour p=7,8,9,10,11,12. En norme 24, si e=3, W=0 : chaque
signe induit trois arêtes disjointes. Tous les 75 sommets extérieurs ont
alors a_z=1 ou 2, exactement 42 du premier type et 33 du second. Il s'agit
d'une égalité exacte et d'une contrainte de solveur, pas d'une exclusion de
la couche de norme 24. Le script et son rapport incorporent ce raffinement.

### 06h32 — Au plus 396 co-Heawoods, soit 792 vecteurs signés

**Nouvelle borne globale :** C1 contient au plus **396 co-Heawoods induits**,
et donc au plus **792 vecteurs entiers de norme 14**, opposés compris. La
borne LAB précédente sur cette couche était 7920. Aucun quotient modulo
symétrie n'intervient ici : il s'agit du nombre total dans un éventuel C1.

Fixons un C4 I et signons ses deux parties par +1 et -1. Tous les
co-Heawoods qui le contiennent peuvent être orientés de manière concordante
sur I. Deux de leurs vecteurs f,g ont alors produit scalaire exactement
quatre et n'ont aucun autre sommet commun. Voici pourquoi ce point n'est
pas une hypothèse : f+g possède déjà deux +2 et deux -2. Pour deux sommets
de valeur +2, la masse négative de f+g est au moins 8+8-4=12. Avec au moins
quatre entrées de module deux, cela donne `||f+g||^2>=2*(12+4)=32`, donc
f.g>=2. Le lemme de coordonnées appliqué à f-g, de norme <=24, interdit
toute intersection de signes opposés. Le produit scalaire est donc la
taille de l'intersection, au moins quatre; la borne d'angle le borne par
quatre. Il vaut quatre et l'intersection est exactement I.

Soit c le vecteur signé de I et `q=7P c=3c-Ac`, entier propre -4. On a
`c.c=4`, `c.Ac=-8`, donc `q.q=7*(3*4+8)=140`. Pour chaque co-Heawood f
contenant I, `q.f=7*c.f=28`. Si cinq tels vecteurs f1,...,f5 existaient,
leur somme s aurait norme `5*14+2*C(5,2)*4=150`. Le vecteur entier propre
`q-s` aurait alors norme `140+150-2*5*28=10`, impossible au minimum entier
de norme 14. **Chaque C4 appartient donc à au plus quatre co-Heawoods.**

Le graphe C1 possède exactement `99*84/4=2079` C4, puisque chaque paire
non adjacente a ses deux voisins communs et chaque C4 est compté par ses
deux diagonales. Un co-Heawood en possède exactement 21, un pour chaque
paire de sommets de l'une de ses parties. Le double comptage donne
`nombre_coHeawoods <= 4*2079/21 = 396`.

Contrôle supplémentaire plus faible : les coordonnées locales à v montrent
que deux co-Heawoods distincts ne peuvent choisir les mêmes trois voisins
négatifs. Trois tels voisins forcent sept sommets communs concordants et
aucun croisement de signes, contre la borne d'angle. Les 280 triples
admissibles, quatre par co-Heawood en v, donnent au plus 70 co-Heawoods en
v, donc 495 globalement. Le comptage par C4 améliore cette borne à 396 et
ne dépend pas du calcul des 4480 supports.

Les constantes, les 21 C4 et le résidu de norme dix sont intégrés au script
`coheawood_angle_bound.py` et au rapport correspondant. Preuve globale
élémentaire; pas d'annonce d'exclusion de C1.

**Corollaires locaux.** Chaque sommet est sur 84 C4, et chaque co-Heawood
qui le contient utilise six de ces C4 : au plus 56 co-Heawoods par sommet.
Chaque arête est sur 12 C4, et chaque co-Heawood qui la contient en utilise
trois : au plus 16 co-Heawoods par arête. Ces bornes sont uniformes.

**Relais LAB 643 et 645, lus et acquittés à 06h38.** LAB annonce aussi
l'exclusion de b=32 (commit `e5805a1`), soit `rang_F7(A+4I)>=35`. Les
petits vecteurs projetés donnent a4>=1749546 après contrôle des collisions
par prismes jumeaux. Pour b=34, son programme reste faisable même en
remplaçant notre borne c7<=792 par zéro; il lui faut surtout augmenter a4,
vers 1,4e7. LAB a vérifié le calcul C4/résidu de norme dix mais n'a pas encore
relu les deux lemmes préalables sur les coefficients et les angles. Notre
borne 792 est donc transmise avec sa preuve, sans prétendre à une validation
indépendante de tout l'argument par LAB.

### 06h54 — Petites couches entières de valeur propre +3

**Attention au signe de la valeur propre :** cette section traite +3, et
non les co-Heawoods de valeur propre -4. Elle vise les collisions entre
petits vecteurs projetés dont LAB a besoin pour b=34.

Pour Ah=3h entier non nul, de masse M de chaque signe et a=max|h|, le sommet
extrémal requiert au moins 3a de masse de son propre signe parmi ses voisins.
Donc M>=4a, et de nouveau `||h||^2>=a^2+7a`. Jusqu'à la norme 16 incluse,
les coefficients sont nécessairement 0,+1,-1. Si p est la taille de chaque
signe, les deux graphes induits ont degré minimum trois, et un sommet de
degré interne d a exactement d-3 voisins de l'autre signe.

Un graphe induit de n sommets et de degré minimum trois a degré maximum
`floor((2n-2)/3)` : les d voisins d'un sommet induisent un couplage, chacun
requiert au moins un voisin parmi les n-d-1 non-voisins du sommet, et chacun
de ces derniers peut en desservir au plus deux. Ainsi d<=2(n-d-1).
En particulier p>=6, et d<=4 pour p<=8.

**Classification finie exacte.** Le script `small_positive_three_supports.py`
énumère les graphes cubiques par degrés, puis les graphes avec un sommet de
degré quatre en fixant ce sommet, le couplage parmi ses quatre voisins et
les incidences restantes. Les  n! réétiquetages donnent le quotient exact.
Tous les couples sont ensuite reliés par les couplages possibles entre
leurs sommets de degré quatre, et les bornes lambda/mu sont contrôlées.

- p=6 : un seul type, le prisme triangulaire; aucune arête entre les signes.
- p=7 : un seul type H7, degrés (4,3,3,3,3,3,3). Son centre a deux paires
  de voisins; ses deux non-voisins sont adjacents et se partagent les quatre
  voisins, un de chaque paire chacun. Deux H7 sont reliés par leurs centres.
- p=8 : sept types induits, dont trois cubiques, trois de degrés (4,4,3^6),
  et un de degrés (4^4,3^4), ce dernier étant une grille privée d'un sommet.
  Treize couples de types et 42 couplages étiquetés subsistent. Les 42 ne sont
  pas annoncés comme des classes non isomorphes de supports complets.

**Calcul d'extension qui ne conclut pas.** Pour chacun des 44 supports
(1+1+42), toutes les lignes d'incidence extérieure sont énumérées. Elles
équilibrent les deux signes, ne violent aucun compte de voisins communs
dans le support ou avec le nouveau sommet, et ont au plus 14 incidences.
Les multiplicités de ces lignes doivent satisfaire les degrés restants et
tous les comptes de voisins communs des paires du support. Les 44 systèmes
ont une solution rationnelle : chaque solution a été reconstruite en
fractions et vérifiée exactement, et est enregistrée dans le rapport. Les
solutions trouvées sont entières pour 27 supports, fractionnaires pour 17.
Cela **n'est pas** une extension en C1 : les arêtes entre sommets extérieurs
ne sont pas construites. Ne pas relancer ce même LP en espérant une exclusion.

**Au plus 2871 paires de prismes jumeaux.** Pour un prisme P, posons
`b_P=A 1_P-3 1_P`. Sur P il vaut zéro. Dehors, un sommet ne peut toucher
deux sommets de P que s'ils forment l'une des trois arêtes transversales;
toutes les autres paires ont déjà leur quota de voisins communs dans P.
Les trois compléteurs de ces arêtes sont distincts. Ainsi b_P vaut deux sur
trois sommets, un sur 60 sommets, zéro sur 36 sommets, P compris.

Deux prismes de même b_P sont disjoints : sinon leur différence serait un
vecteur propre +3 dont chaque signe a moins de six sommets. Tous les prismes
d'une même classe sont contenus dans les mêmes 36 zéros, donc une classe
en contient au plus six. Avec notre borne globale de 1150 prismes, le nombre
maximal de paires est `191*C(6,2)+C(4,2)=2871`, et le nombre de vecteurs
entiers propres +3 de norme 12 est **au plus 5742**, opposés compris. La
borne de 8625 paires utilisée par LAB peut donc être abaissée à 2871.

Si une classe contient six prismes, ses trois compléteurs forment une
droite à p=12. En effet `(A+4I)b_P=12*1`; sur un compléteur cela donne
`nombre_voisins_zero = 10 + nombre_voisins_parmi_les_trois_completeurs`.
Les six prismes imposent déjà douze voisins zéros, donc les deux autres
compléteurs sont voisins. Les six prismes donnent alors les six grilles
contenant cette droite. Ce cas reste autorisé, sous les contraintes p=12
déjà obtenues cette nuit.

**Au plus 8316 vecteurs entiers propres +3 de norme 14.** Le nombre de H7
induits est au plus `99*C(7,2)*2=4158`. Pour son centre, on choisit deux
arêtes de son voisinage; il reste deux façons de répartir leurs extrémités
entre les deux sommets non voisins du centre, chacun déterminé par mu=2.
Pour la fonction `b_H=A 1_H-3 1_H`, deux H7 de même b_H sont disjoints :
une intersection laisserait au plus six sommets dans chaque signe de leur
différence; avec six, retirer un sommet à H7 laisse toujours un degré deux,
et avec moins de six le degré minimum trois est impossible.
Les centres de deux H7 de même b_H sont nécessairement adjacents et
constituent l'unique arête entre eux. Les centres d'une classe forment donc
une clique, de taille au plus trois par lambda=1. Il y a au plus 4158 paires
de H7 d'une même classe, donc au plus **8316 vecteurs signés de norme 14**.

La couche de norme 16 a ses 42 supports nécessaires, mais aucun majorant de
son nombre n'est obtenu ici. Les vecteurs de support <=16 avec coefficients
de module deux et de norme supérieure ne sont pas encore classifiés. La
distinction complète demandée pour les projections de LAB reste donc ouverte.

Fichiers : `small_positive_three_supports.py` et
`data/codex_night_20261014/small_positive_three_supports.json`. Énumération
et vérification rationnelle locales en environ 2,5 secondes; aucun SAT.

### 07h08 — Tous les noyaux entiers +3 de masse l1 au plus 16

**Résultat : 48 configurations couvrantes, au plus 313434 vecteurs signés.**
Il s'agit de tous les h entiers non nuls tels que Ah=3h et `||h||_1<=16`.
Ce seuil couvre les différences de deux vecteurs 0,+1,-1 portés par au plus
huit sommets **et de même somme**, lorsqu'ils ont la même projection P.
Il ne couvre pas à lui seul les collisions entre sommes différentes :
P(h)=0 donne alors `(A-3I)h=(somme h)/9 * 1`, avec un terme constant possible.
Cette distinction est conservée dans le relais à LAB.

**Les quatre cas pondérés manquants.** La masse de chaque signe est M<=8,
et M>=4a impose a<=2. S'il existe une entrée +2, M=8. Ce sommet doit toucher
toute la masse positive restante, égale à six, et aucun sommet négatif.
Deux entrées +2 seraient adjacentes et auraient au moins deux autres
sommets positifs communs, contre lambda=1. Il n'y a donc qu'une +2 et six
entrées +1, toutes voisines de celle-ci. Chaque +1 exige exactement un
partenaire positif parmi les six voisins, et aucun voisin négatif. Le signe
positif est le moulin de trois triangles F3, de poids deux au centre et un
sur ses six autres sommets. L'autre signe est soit le même moulin pondéré,
soit l'un des trois graphes cubiques de huit sommets. Aucune arête entre les
signes. Cela donne quatre configurations, de norme 20 ou 18, qui s'ajoutent
aux 44 précédentes. Leurs incidences extérieures passent également le LP;
les quatre solutions rationnelles sont vérifiées exactement et enregistrées.

**Bornes sur les nombres de graphes à huit sommets.** Pour chacun des sept
types, une programmation dynamique sur ses 256 sous-ensembles choisit un
ordre d'injection dans C1. Le premier sommet a au plus 99 images. Avec un
voisin déjà choisi, il en reste au plus 14 moins les voisins déjà utilisés.
Avec deux voisins choisis, il en reste au plus lambda ou mu, moins leurs
voisins communs déjà utilisés. Sans voisin choisi, un non-voisin choisi
donne au plus 84 images, moins celles déjà utilisées qui lui sont non
adjacentes. On minimise le produit de ces bornes, puis on divise par l'ordre
du groupe d'automorphismes du type, connu par les 8! réétiquetages.

Le rapport enregistre les ordres et tous les facteurs, donc cette borne
ne suppose pas un comptage réel de copies dans C1. Pour les trois cubiques,
les majorants sont 4158,24948,49896, total 79002. Pour les trois types à
deux sommets de degré quatre, ils sont 8316 chacun, total 24948. Pour le
type à quatre sommets de degré quatre, le majorant est 2079.

**Classes de même fonction b=A1_H-3*1_H, pour la norme 16.**

* Cas cubique. Une fonction b a somme 88 et norme carrée 128, et vaut zéro
  sur le support de H. Comme `somme C(b_x,2)=20`, elle est non nulle sur au
  moins 68 sommets; elle a donc au plus 31 zéros. Deux graphes cubiques
  distincts de même b sont disjoints : leur différence aurait sinon un
  signe porté par un sous-graphe propre de degré minimum trois, impossible
  dans un graphe cubique connexe. Il y en a donc au plus trois par classe,
  et au plus `2*79002=158004` vecteurs signés de norme 16 de ce type.
* Deux degrés quatre. Les trois types n'ont aucun sous-graphe propre de
  degré minimum trois, ce qui est contrôlé exhaustivement par le script.
  Deux supports de même b sont donc disjoints, et leurs deux sommets de
  degré quatre sont reliés par un couplage parfait. Pour une classe de t
  supports, les 2t sommets distingués ont chacun degré au moins t-1 dans
  leur union. Tout graphe induit de n sommets satisfait
  `somme deg(v)^2 <= 2n(n-1)` par comptage des voisins communs. Il faut donc
  `(t-1)^2<=4t-2`, soit t<=5. Au plus `4*24948=99792` vecteurs signés.
* Quatre degrés quatre. Le seul type a exactement deux sous-graphes propres
  de degré minimum trois : les deux prismes obtenus en retirant une arête
  entre sommets de degré trois. Deux supports distincts de même b sont donc
  disjoints ou se rencontrent sur une telle arête. Leurs ensembles de quatre
  sommets de degré quatre sont toujours disjoints. Pour un support fixé,
  chaque partenaire disjoint requiert un nouveau voisin de chacun de ses
  quatre sommets distingués, dans les sommets distingués du partenaire.
  Ces voisins sont distincts et il reste dix places après les quatre voisins
  internes. Donc au plus dix partenaires disjoints, soit `10*2079=20790`
  vecteurs signés. Les partenaires non disjoints donnent la norme 12 déjà
  comptée, pas la norme 16.

Les trois sortes de classes sont séparées par `||b||^2=128,114,100`.
En tout, la norme 16 contribue au plus **278586** vecteurs signés.

**Comptage des cas pondérés.** Il y a au plus `99*C(7,3)=3465` moulins
pondérés : choisir le centre et trois des sept paires de son voisinage.
Un moulin pondéré et un cubique de huit sommets ont même masse huit; leur
b a somme 88, norme carrée 128 et au plus 31 zéros. Des composantes positives
connexes, propres de valeur trois dans leur support, de même masse et même
b, sont distinctes et disjointes. En effet, b vaut zéro sur chacun des
supports; un sommet d'un support extérieur à l'autre ne peut être adjacent
à cet autre support. La connexité impose alors égalité ou disjonction; sur
un même support, l'unicité du vecteur propre positif et la masse fixée
donnent le même vecteur. Chaque composante a au moins sept sommets : une
classe en contient au plus quatre. Chaque moulin a donc au plus trois
partenaires de masse huit, ce qui borne ensemble les normes 18 et 20
pondérées par `2*3*3465=20790` vecteurs signés.

Total : `5742 + 8316 + 278586 + 20790 = 313434`. Tous les nombres sont des
majorants, avec surcomptages possibles, pas des nombres de vecteurs existants.
Le passage de cette borne de noyaux à un nombre de collisions de petits z
doit encore tenir compte des représentations z-z'=h; il n'est pas effectué
ici. Le script et son rapport sont mis à jour, calcul complet en environ
2,6 secondes. Aucune exclusion de C1 ni du prochain rang modulaire annoncée.

### 07h18 — Noyaux affines : 40 types supplémentaires, borne totale 911178

On couvre maintenant les collisions de projections de sommes différentes.
Soit `P=(27I-9A+J)/63` et `h` entier non nul, `Ph=0`, `||h||_1<=16`.
L'équation est `(A-3I)h=(somme h)/9 * 1`. Sa somme est donc 0 ou ±9.
La somme nulle relève des 48 gabarits et de la borne 313434 précédente.
Orientons l'autre cas pour avoir somme h=9. Si M et N sont les masses
positive et négative, alors M=9+N et N<=3. Un coefficient positif a impose
M>=4a+1, donc a<=2. Un coefficient négatif -a impose N>=4a-1 : s'il y a
une partie négative, elle comprend exactement trois coefficients -1.
Leurs équations imposent qu'ils forment une droite T et n'aient aucune
arête vers le support positif S.

**Aucun coefficient 2.** Sans partie négative, un sommet de coefficient 2
doit être adjacent à toute la masse restante, égale à sept. Le voisinage
est une réunion d'arêtes : un autre coefficient 2 ne peut recevoir le
poids sept requis, et une fois ces autres 2 exclus, un coefficient 1 ne
peut recevoir que 2+1 au lieu des quatre requis. Avec la droite négative
T, écrivons X pour ses 36 voisins et Y pour les 60 sommets non adjacents
à T. Le support positif est dans Y. Un sommet de Y a exactement six
voisins dans X, donc huit dans Y. Un sommet de coefficient 2 ne peut
avoir aucun voisin de Y hors S, car à ce voisin l'équation affine impose
un poids positif total de un. Ses huit voisins de Y seraient donc dans S,
ce qui excède le poids interne requis, égal à sept. Contradiction.

Il reste exactement deux formes nécessaires, à changement de signe près :

* h est l'indicatrice d'une grille de neuf sommets (norme carrée 9).
* `h=1_S-1_T`, où T est une droite, S comprend douze sommets non adjacents
  à T et induit un graphe régulier de degré quatre (norme carrée 15).
  Chaque sommet de X a exactement deux voisins dans S, et chaque sommet
  de Y hors S en a exactement un. En particulier T est déterminée par S :
  ce sont les trois zéros du vecteur `(A-3I)1_S`.

**Énumération exhaustive abordable.** Le générateur C++ remplit les lignes
successives de la matrice d'adjacence. Les sommets encore non traités avec
le même voisinage dans le préfixe traité sont interchangeables : choisir
un segment initial de chaque classe suffit, sans supprimer de classe
d'isomorphisme. Chaque ajout vérifie degré <=4 et les capacités de voisins
communs (un sur une arête, deux ailleurs). Sur douze sommets : 46620 nœuds,
2350 feuilles avant quotient, **40 types** après individualisation et
raffinement exacts. Histogramme du nombre de triangles :
`{0:1, 2:2, 3:4, 4:22, 5:6, 6:3, 8:2}`. Sur neuf sommets, le même
générateur ne donne qu'un type, la grille, avec 72 automorphismes.
Les automorphismes des 41 types sont aussi vérifiés par une seconde
recherche de bijections conservant l'adjacence, sans raffinement de couleurs.

Pour chaque type, la programmation dynamique sur les 4096 sous-ensembles
choisit un ordre d'insertion des sommets. Les facteurs sont 99 au départ,
au plus 14 moins les voisins déjà employés si un voisin est fixé, et au
plus la capacité résiduelle lambda/mu d'une paire si deux voisins sont
fixés. Un facteur analogue emploie les 84 non-voisins quand aucun voisin
n'est fixé. Le produit borne les plongements étiquetés; sa division par
le groupe d'automorphismes borne les copies induites. Les ordres, facteurs,
graphes et nombres sont tous conservés dans le rapport.

Somme des majorants des 40 types : **298681** copies. Une copie détermine
au plus une droite T, donc au plus un noyau orienté de somme 9. Avec la
borne déjà prouvée de 191 grilles, les sommes non nulles contribuent au
plus `2*(298681+191)=597744` noyaux signés. En incluant la somme nulle :

**Au plus 911178 vecteurs entiers non nuls h tels que Ph=0 et ||h||_1<=16.**

Fichiers : `affine_regular_supports.cpp`, `small_affine_kernels.py`, deux
listes exhaustives JSONL et rapport `small_affine_kernels.json`. Génération
C++ <0,1 s, quotient, automorphismes et majorants Python environ 4,8 s.
Ce sont des conditions nécessaires et des majorants, sans affirmation
d'extension des 40 types ni d'exclusion de C1. Cette borne compte les
noyaux h; elle ne compte pas encore les représentations z-z'=h.

### 07h37 — Multiplicités certifiées pour une famille de vecteurs de norme 8

Périmètre précis : `z dans {0,+/-1}^99`, support **exactement huit**,
**somme zéro**, et `||sqrt(7)Pz||^2=8`. Le support est donc une paire
ordonnée de quatre-ensembles anticomplets, chacun induisant quatre arêtes
(C4 ou paw). Écrire D pour cet ensemble de z. Les calculs suivants ne
couvrent pas les collisions avec des z de sommes ou de tailles différentes.

Une collision z-z'=h a somme nulle et masse absolue <=16, donc relève des
48 gabarits précédents. Un noyau unitaire de norme 2p partage exactement
8-p sommets extérieurs entre z et z'; un noyau pondéré de masse 16 n'en
partage aucun. Sur son support, chaque coefficient 1 de h choisit entre
`(z,z')=(1,0)` et `(0,-1)` (analogue pour -1); un coefficient 2 force
`(1,-1)` (analogue pour -2). L'équation de norme devient simplement :
la somme des produits des signes sur les arêtes de z vaut huit.

**Norme 16 ou cas pondérés.** Énumération directe des partitions du support,
sans inconnue extérieure. Pour les trois cubiques de huit sommets, les
multiplicités sur les paires de types valent les produits des nombres
`6,4,8`; diagonale `36,16,64`. Pour les trois types à deux sommets de degré
quatre : diagonale `32,72,50`, termes hors diagonale `48,40,60` (maximum
sur les deux couplages admissibles). Type à quatre degrés quatre : 32 ou
64. Cas pondérés : moulin/moulin 144, moulin/cubique 72,48,96.
Ces multiplicités comptent les couples ordonnés (z,z') pour un h signé fixé.

**Norme 14, un sommet extérieur.** On énumère les 99 profils possibles de
ce sommet dans le support de h. Pour chaque profil, on compte exactement
ses contributions possibles, avec les deux signes. Les variables sont
les nombres de sommets de chaque profil; leurs sommes, degrés résiduels
et comptes de voisins communs sont fixés. Le dual rationnel vérifié donne
**au plus 184 représentations** pour un h signé de norme 14.

**Norme 12, deux sommets extérieurs.** Il y a 46 profils individuels.
On ajoute les nombres de paires extérieures de chaque paire de profils,
selon qu'elles sont adjacentes ou non : 1892 sortes admissibles après
vérification des capacités de voisins communs dans le support augmenté.
Les marges de paires par profil valent 86 fois la taille du profil, et
les marges de paires voisines valent le degré extérieur fois cette taille.
Pour chaque sommet du support, on fixe de même les marges des partenaires
qui lui sont adjacents : tous les partenaires, puis seulement ceux voisins
du premier sommet. La dernière égalité est exactement le compte lambda/mu
des voisins communs entre un sommet du support et un sommet extérieur.
Avec les marges individuelles, cela donne 1276 égalités linéaires.
L'objectif compte exactement les partitions et signes pour chaque sorte
de paire extérieure. Le dual rationnel vérifié donne **au plus 2508
représentations** pour un h signé issu de deux prismes jumeaux.

Dans les deux LP, le solveur ne sert qu'à proposer un dual. Les coefficients
sont reconstruits en fractions, une éventuelle erreur d'arrondi est
corrigée par la ligne de somme constante, puis toutes les inégalités
duales et la valeur sont vérifiées en arithmétique rationnelle. Les
certificats complets sont conservés dans le rapport. Aucune infeasibilité
ni extension intégrale n'est annoncée.

**Borne globale de pertes, encore trop large.** Chaque composante cubique
de huit sommets a au plus deux partenaires, celles à deux degrés quatre
au plus quatre, celles à quatre degrés quatre au plus dix. Pour les deux
premières familles, chaque multiplicité hors diagonale est au plus la
moyenne des deux diagonales. En chargeant les arêtes de compatibilité
à leurs extrémités et en utilisant les bornes de copies déjà prouvées :
3742200, 2561328 et 665280 paires de collisions respectivement. Pour les
moulins, une paire moulin/cubique se charge au plus 96 au moulin, une paire
moulin/moulin 72 à chacun. Au plus trois partenaires et 3465 moulins donnent
997920 paires. Ajouter `2871*2508=7200468` pour les prismes jumeaux et
`4158*184=765072` pour la norme 14. Total : **15932268 paires non ordonnées
en collision dans D**. Donc `|sqrt(7)P(D)| >= |D|-15932268`.

Ce résultat rend le passage noyaux-vers-représentations effectif sur D,
mais ne donne pas encore le minorant de |D| nécessaire, ni l'exclusion du
rang modulaire suivant. Ne pas ajouter ce minorant à ceux d'autres familles
sans traiter leurs collisions croisées. Script et rapport :
`norm_eight_collision_multiplicities.py/json`; exécution complète <2 s.

### 07h41 — Comptes exacts dans les anti-voisinages de petits motifs

Message LAB649 lu et acquitté : le blocage principal du prochain rang est
bien le nombre de supports garantis, déjà insuffisant avant collisions.
Pas de relance du calcul des mêmes multiplicités. L'exploitation directe
de A² et A³ donne néanmoins des contraintes locales plus fortes.

Pour un motif induit S de taille s, noter X son voisinage extérieur, Y son
anti-voisinage extérieur, `j(x)=|N(x) inter S|`, et `R={x dans X:j(x)>=2}`.
Chaque sommet y de Y vérifie exactement
`deg_Y(y)=14-2s+somme_{r dans R voisin de y}(j(r)-1)`.
On obtient aussi
`e(Y)=C+somme_{rr' dans E(R)}(j(r)-1)(j(r')-1)`.
La constante C dépend seulement du motif et des profils multiples réalisés.

Preuve de l'identité d'arêtes : poser d=A_S*1 et
`W=somme_{xx' dans E(X)} j(x)j(x')`. L'identité
`A³=13A-12I+26J`, puis `A²=12I-A+2J`, déterminent W à partir de S :
`2W=26e(S)-12s+26s²-d^t A_S d
     -2*somme_v d_v(12+2s-d_v-(A_S d)_v)`.
Pour x dans X, la somme des poids j sur ses voisins de X vaut
`2s-j(x)-somme_{v dans S voisin de x}d_v`.
Multiplier par j(x)-1 et sommer donne D. Sur une arête de X, W-D contribue
`1-(j(x)-1)(j(x')-1)`. Donc `e(X)=W-D+correction` et
`e(Y)=693-e(S)-14|X|+e(X)`, d'où C.

Les profils multiples sont forcés par les capacités résiduelles de voisins
communs dans S. Ils sont de taille deux, sauf pour la maison : son unique
profil de taille trois est réalisé ou non, selon delta=1 ou 0. Le sommet
de ce profil complète la maison en prisme. Le script énumère toutes les
possibilités (au plus 64 sélections de profils et 1024 graphes sur R).
Les intervalles ci-dessous sont des conditions nécessaires, pas des
affirmations que toutes leurs valeurs s'étendent à C1.

| Motif S | Taille Y | Identité pour e(Y) | Correction possible |
|---|---:|---:|---:|
| C4 | 51 | 173 + e(R) | 0,1,2 |
| paw | 50 | 164 + e(R) | 0,1 |
| moulin/bowtie | 40 | 96 + e(R) | 0,1,2,3,4 |
| maison, delta=0 | 41 | 103 + e(R) | 0,1,2 |
| maison, delta=1 | 40 | 99 + e(R_2) | 0,1 |

Dans le dernier cas, R comprend le sommet de poids deux et deux sommets
R_2 de poids un; le premier n'est adjacent à aucun des deux autres, donc
la correction se réduit à l'arête éventuelle de R_2.

Il y a 2079 moulins : centre puis deux des sept paires de son voisinage.
Il y a 8316 maisons : un C4 puis l'une de ses quatre arêtes, dont le
compléteur fournit le toit et ne peut être adjacent aux deux autres sommets.
Chaque prisme contient six maisons, et chacune a au plus un compléteur en
prisme. Ainsi `somme delta=6p`, où p est le nombre total de prismes.
Le nombre de z signés de support sept, somme ±3 et norme projetée huit,
obtenus par un moulin ou une maison positif et une arête négative éloignée,
est donc au moins `2*(2079*96+8316*103-24p)`, soit **2057064** en utilisant
p<=1150. C'est un compte brut : ne pas le lire comme un minorant de a_4
sans retrancher les collisions. Le gain seul ne comble pas l'écart du rang.

Code et rapport `small_antineighborhoods.py/json`, calcul <0,1 s.

### 14 octobre, apres-midi : demande explicite de CONSTRUIRE un SRG asymetrique lambda=1

Travail de construction effectif dans code/codex/lambda_one_search, donnees
codex_lambda_one_construction_20261014. Aucun SRG asymetrique obtenu.
Les recherches par voisinages incrementaux et SAT global sur243 ne donnent
que des copies connues ou des limites de temps, jamais une exclusion generale.
Le moteur incremental a ete etendu a378 et a CP-SAT, avec choix de labels
pour les colonnes identiques du bord (sans imposer d'automorphisme).

Claude a construit hemi_s1, SRG(378,52,1,8). Verification INDEPENDANTE ici :
identite matricielle exacte et groupe COMPLET BLISS d'ordre6 (0,063s).
Bords aleatoires gardes90,75,60 : reconstruction du seed seul. Bord45 :
seed seul mais22 enumerations incompletes. Bord35 avec CP-SAT :214 lignes
candidates,171 noeuds, profondeur45 en420s, aucune completion. Un controle
spectral numerique de Schur n'a pas apporte de coupe sur ce pilote ; aucune
preuve d'exclusion ne repose sur ce controle numerique. Deux essaisR40 avec
priorite aux petites modifications sont en cours au moment de cette entree.

AUTRE CONSTRUCTION TESTEE PUIS FERMEE PAR PREUVE EXACTE : 3-ovoide dans le
quadrangle de Payne surGF9,729points et891droites de9. La geometrie ambiante
est verifiee SRG(729,88,7,11). SAT/CPSAT et recherche locale n'ont produit
aucun3-ovoide. Le blocage a ensuite ete explique sans solveur : incidence M
891x729 de rang binaire441, noyau de dimension288 DOUBLEMENT PAIR. Chacun
des288 vecteurs d'une base explicite a poids0mod4 et les intersections de
toutes les paires sont paires. Un3-ovoide aurait243points ; son complement,
de poids486, rencontre chaque droite en6points, donc serait dans ker(M),
mais486=2mod4 : contradiction. La base, son independance et l'appartenance
au noyau sont verifiees exactement. Script payne9_obstruction.py et certificat
payne9/obstruction_certificate.json. Le constructeur effectue maintenant ce
precontrole en0,31s et ne relance plus de SAT sur cette voie impossible.
Portee : CE quadrangle explicite seulement, pas les SRG243 generaux, pas
les autres GQ de meme ordre, pas Conway. Resultat transmis aClaude : pont667.
Commits precedents de cette construction :0b0ea1a,bafa35e.

Fin des deux essaisR40 : seeds902/903,359/347noeuds,80/70s, seul le graphe
de depart reconstruit,17 enumerations incompletes dans chaque essai. Aucun
nouveau SRG, aucune exclusion de ces bords. Bilan des essais et sources :
data/codex_lambda_one_construction_20261014/construction_run_summary.json.

### 14 octobre : mecanisme d'asymetrie par les triangles et circuits

Priorite precisee par Dilan : comprendre fondamentalement l'asymetrie des
SRG, en particulier lambda=1. Pas de sondages repetes du pont vide, ni de
verification independante des resultats de Claude. Les graphes et leurs
groupes complets deja fournis sont acceptes. Les calculs suivants portent
sur de NOUVEAUX objets derives ; aucun groupe complet n'est recalcule.

Pour une racine x, F=V\N[x]. T_x retient l'arete yz de G[F] lorsque son
unique triangle est complete dans N(x). T_x est mu-regulier et sans triangle.
En effet, chaque a dans N(x) intersection N(y) fournit exactement un tel z,
necessairement dans F ; deux a ne peuvent fournir le meme z (lambda=1).
Aucune arete de T_x n'appartient a un triangle dans F. Le graphe residuel
U_x=G[F]-T_x est donc (k-2mu)-regulier, et chacune de ses aretes appartient
encore a un unique triangle dans U_x. Si mu=2, T_x est une union de cycles
de longueur au moins quatre.

K_x retient les aretes touchant N[x] et celles de T_x, avec x distingue.
Aut(G)_x est un sous-groupe de Aut(K_x,x). Si un invariant intrinseque de x
definit une classe de taille m et si |Aut(K_x,x)|=h, alors |Aut(G)|<=m*h.
Un sommet intrinsequement unique avec un squelette enracine rigide suffit
donc a certifier l'asymetrie. Rigidite apres fixation et impossibilite de
deplacer la racine sont deux problemes differents.

Calcul nouveau sur les huit243 et hemi378 (1,7s). Invariant : longueurs des
cycles de T_x pour mu2, histogramme des nombres de C4 aux sommets de T_x
pour mu8. BvLS garde tout le groupe local 2^11*11!=81749606400 dans K_x.
Gamma5 : m243,h12. Gamma6 et Gamma8 : m27,54,54,108 et h4,2,2,1.
Gamma7 : trois classes81 avec h2. Hemi378 : 59 classes6,h1 ; 5 classes3,h2 ;
4 classes2,h3 ; une classe1,h6. Tous les produits valent6. La racine unique
est375 ; 354 sommets ont un squelette enracine rigide. Les bornes retrouvent
les ordres COMPLETS deja fournis pour Gamma5-8 et hemi378, sans les recalculer.
Donc lambda1, meme avec mu2, ne force PAS un stabilisateur de point non trivial.

Reduction explicite pour mu2 : S=N(x) a son appariement P. Chaque sommet
de F est l'unique second voisin commun d'une paire non appariee {a,b} de S.
F s'identifie aux aretes de H=K_k-P. Les triangles passant par a apparient
les aretes de H incidentes a a ; ils definissent un systeme de transitions,
dont les circuits sont precisement les cycles T_x. Le mot d'un circuit
enumere les couleurs a de ses aretes. Ses lettres consecutives donnent les
paires etiquetant les sommets de F. Aut(K_x,x) est exactement le groupe des
permutations de S preservant P et la collection non orientee de ces mots.

CRITERE FINI : un circuit de longueur L unique parmi ces circuits, utilisant
les k lettres, reduit le stabilisateur a au plus 2L alignements dihedraux.
Chaque alignement doit respecter l'egalite des lettres repetees, puis P,
puis les autres circuits. Sur Gamma6, racine0, le seul circuit de longueur68
utilise les22 lettres et les repetitions eliminent A ELLES SEULES les135
alignements non identiques. Sur Gamma8, racine0, longueur40 : les79 autres
sont elimines de la meme facon. Ce sont des explications combinatoires de
la rigidite, sans solveur de groupes. Les temoins de rejet sont sauvegardes.

Correction du14/10 apres le message684 : le twin a des cycles de longueur30,
donc l'observation initiale « tous multiples de4 » etait fausse. Les cycles
des huit243 sont tous PAIRS. Une construction PARTIELLE sur99, apres31 echanges,
donne des cycles4,11,69 et un squelette enracine rigide. Les lignes de N[x]
sont completes, chaque arete presente a un voisin commun, et toute autre
paire en a au plus deux. Chaque sommet de F a encore10 voisins inconnus.
Ce n'est PAS un SRG, et sa completabilite n'est pas etablie. Ne pas imposer
la parite des cycles a un SRG inconnu sans une preuve globale supplementaire.

Scripts : asymmetry_triangle_transport.py, triangle_transport_words.py,
triangle_transport_local_experiment.py. Donnees et preuves detaillees dans
data/codex_asymmetry_mechanisms_20261014/. Aucun nouveau SRG asymetrique
construit ; aucun argument d'inexistence de Conway obtenu.

Corollaire utile pour CONSTRUIRE : si la borne m*h est saturee par l'ordre
connu de Aut(G), et si m compte les racines ayant le meme invariant du
SQUELETTE LUI-MEME, tout isomorphisme entre K_x et un K_y compatible est
deja la restriction d'un automorphisme de G. En effet l'orbite de x a
taille m et le stabilisateur taille h. Comme K_x contient tous les sommets,
une completion SRG differente, gardant exactement ce squelette etiquete,
ne peut pas etre isomorphe a G. Cela s'applique a Gamma5-8 et hemi378
(les invariants initiaux donnent deja les classes utilisees). On peut
donc bloquer le seed etiquete seul dans une telle recherche : toute autre
completion serait une nouvelle classe d'isomorphisme. Elle ne serait pas
automatiquement asymetrique. Aucune telle completion construite ici.

Lecture ponctuelle des deux nouveaux messages scientifiques671 et673,
acquittes673 ; pas de boucle de sondage. Claude poursuit une construction
independante sur115 et une analyse des petits vecteurs propres et de la
rarete des selections dans les hotes geometriques. Aucun audit de ces travaux.
Supplement theorique transmis : les symetries heritees sur une selection S
sont K_S/K_(S), donc leur ordre est au moins |K|/(N*|K_(S)|), ou N compte
les selections etiquetees. Dans un m-ovoide d'un GQ(s,t), chaque point hors S
a m(t+1) voisins dans S. Si ce nombre depasse max(s-1,t+1), les profils
des points exterieurs dans S sont tous distincts, donc K_(S)=1. Pour le
hemisysteme378 de Claude :78>26, application immediate sans recalcul.
Un exemple asymetrique construit ainsi exige alors une orbite reguliere de
selections de taille |K|. C'est necessaire, pas suffisant : des symetries
internes peuvent encore ne pas s'etendre a l'hote. Une obstruction propre
a une famille de constructions n'est pas une obstruction generale a lambda1.
Formulation complete : host_symmetry_criterion.json.

### Cible precisee apres la question de Dilan relayee par Claude682

Construction visee : SRG(243,22,1,2), seed Gamma6, racine0, squelette K_0
conserve exactement. Aucun calcul de completion n'est en cours. Objectif
asymetrique, sans affirmer qu'une completion differente existe.
Comparaison des signatures DEJA calculees :17*C4+C12+C32+C40+C68 apparait
sur108 racines de Gamma6, et sur AUCUNE racine de chacun des sept autres
graphes243. Aucun nouveau groupe calcule. Une completion differente avec
ce K_0 serait donc non isomorphe aux HUIT graphes connus : exclusion des
sept autres par invariant intrinseque, et exclusion du seed par la borne
locale saturee. La rigidite de la racine serait automatique ; son unicite
intrinseque, ou une autre preuve empechant son deplacement, resterait a
obtenir pour conclure Aut=1. Cible et preuves : gamma6_root0_target.json.

### Reprise theorique apres Claude684 : rigidite et unicite sont distinctes

La question « pourquoi K_x determine Gamma6/Gamma8 » partait d'une premise
NON prouvee. Ni la rigidite de K_x, ni la saturation m*h=|Aut(G)| ne prouvent
l'unicite d'une completion. Elles montrent que toute autre completion
serait nouvelle. Correction transmise au pont685. Aucun calcul lourd lance.

Pour un morceau avec paires decidees, son groupe L agit sur les completions
Omega ; l'orbite de G a taille |L|/|L intersection Aut(G)|. Une completion
unique herite donc de L. Si toutes les completions sont asymetriques,
|Omega| est un multiple de |L|. Mais une orbite entiere peut ne compter
que des renumerotations : les quelque5,16millions provenant de BvLS sont
de ce type. Si L=1, l'action ne renseigne plus sur le nombre de completions.

NON-UNICITE REELLE DU SQUELETTE BvLS : pour lambda1,mu2, Aut(K_x,x) agit
fidelement sur les k=2t lettres de l'appariement de N(x). Si son ordre
atteint 2^t*t!, son image est tout le groupe W_t. Le stabilisateur des
lettres a,b doit fixer l'unique voisin de transport de {a,b} partageant a.
La seule autre lettre admissible fixe est bar(b). Ainsi les deux voisins
sont {a,bar(b)} et {bar(a),b} : c'est le squelette canonique des grilles.
Les rapports existants donnent cet ordre maximal pour BvLS/racine0 ET
twin/racine0. Ils ont donc le MEME squelette a isomorphisme pres et donnent
au moins deux completions NON ISOMORPHES. Pas de nouveau calcul de groupe.
Cette conclusion ne repose pas sur les seules longueurs des cycles.

Pour tout lambda1, le complement U_x du transport est (k-2mu)-regulier,
chaque arete ayant son triangle unique dans U_x. Si k=2mu, U_x est vide :
K_x=G et l'unicite est automatique. Les triangles forment alors un GQ
d'ordre(2,mu-1) : un point hors d'une droite a au plus un voisin sur elle
par lambda1, et au moins un car aucun triangle ne peut etre entierement
dans son ensemble F. Le degre residuel est10 pour99,18 pour243,36 pour378.
Un degre positif ne prouve PAS la non-unicite : il definit l'inconnue.

EQUATIONS EXACTES POUR mu2 : B est l'appariement de N(x), D l'incidence
de K_k-B, m=k(k-2)/2. Pour E=T+U sur F,
  DE=(J-I-B)D=2J-(I+B)D ;
  E^2+E=(k-2)I+2J-D^tD.
DD^t=(k-3)I+J-B est inversible pour k>4. Les entrees sur les paires
partageant une lettre sont exactement celles de T ; la distance2 dans T
force aussi une entree nulle. Avec symetrie, diagonal0 et binaire, ces
equations sont necessaires ET suffisantes pour la completion SRG.

Obstacle a une reconstruction PUREMENT LINEAIRE : avant les zeros de
distance2, il reste N=m(m-1)/2-k(k-2)(k-3)/2 inconnues. Sur Delta symetrique,
le rang de Delta -> D Delta est au plus km-k(k-1)/2, car (D Delta)D^t est
symetrique. Les zeros de distance2 ajoutent au plus m contraintes. Si le
systeme reel est non vide, sa dimension est donc au moins1393 pour99 et
15081 pour243, meme avec un squelette rigide. Cela ne compte AUCUN graphe
binaire ni direction faisable dans le cube : integralite, inegalites et
equations quadratiques peuvent encore isoler la completion.

Specialisation du cadre spectral deja utilise : W=ker D, Pi son projecteur,
E0=D^t(DD^t)^(-1)(J-I-B)D. Alors E=E0+r*Pi-(r-s)*Q, Q projecteur dans W,
r,s racines de z^2+z=k-2. Les circuits imposent des entrees de Q ; la
rigidite de leur groupe ne signifie pas l'unicite de Q.
CRITERE SUFFISANT D'UNICITE : pour le projecteur Q0 du seed, trouver C
symetrique porte sur les entrees decidees tel que Z=Pi*C*Pi soit strictement
positif sur im Q0 et strictement negatif sur son orthogonal dans W, sans
terme croise. Toute completion a la meme trace(ZQ) ; Q0 est l'unique
maximiseur de cette trace sur0<=Q<=I. Donc E est unique. Aucun tel certificat
n'est trouve ici pour Gamma6/Gamma8 ; aucun SDP lance. Une recherche de
certificat qui echoue ne prouverait pas non plus la non-unicite.
Preuves et portee : skeleton_completion_theory.json.

Campagne conservee dans codex_lambda_one_construction_20261014/parked_campaign/
manifest.json :17 empreintes de sources/entrees/rapport, cible,30 essais
anterieurs en place, configuration et bord d'un ancien pilote378 sauvegardes.
Le moteur specifique conservant exactement K_0 n'etait PAS encore implemente,
donc aucune commande de lancement pour ce modele n'est inventee. Le moteur
general existant devra aussi etre adapte a la consigne de ne plus auditer
les seeds deja acquis avant une reprise. Aucune execution de solveur ici.

### Extension mathematique du flip de Claude687 : majorite de paires

Dans un SRG(1+2t^2,2t,1,2), un automorphisme fixant x et CHAQUE paire de
N(x) comme ensemble est un retournement d'un sous-ensemble de q paires.
THEOREME : s'il est non trivial, q>=ceil(t/2). Cela etend l'obstruction
de Claude pour une seule paire, sans refaire ses calculs ni sa preuve.

Si q=t la borne est immediate. Sinon prendre y={a,c}, a retourne et c fixe.
Son image est {bar(a),c}. Parmi ses voisins dans F, noter n_i ceux dont
l'etiquette a i lettres sur les paires retournees. Alors
  n0+n1+n2=2t-2 ; n1+2n2=4q-2.
La seconde identite compte les incidences aux lettres retournees : a donne1,
bar(a) donne1 (a fournit deja un voisin commun dans N(x)), les2q-2 autres
donnent2. Donc n0=2t-4q+n2>=2t-4q. Les n0 voisins fixes et c sont tous
voisins communs de y et g(y), d'ou n0<=1 et q>=ceil((2t-1)/4)=ceil(t/2).

COROLLAIRE : les retournements purs qui sont de vrais automorphismes forment
un code binaire lineaire C_x de longueur t, distance minimale ceil(t/2).
Pour t impair, si M=|C_x|, chaque coordonnee active apparait M/2 fois,
d'ou somme des poids<=Mt/2 ; les M-1 mots non nuls ont poids>=(t+1)/2.
Ainsi M<=t+1, arrondi a une puissance de2. Pour Conway(t7) : poids>=4 et
|C_x|<=8. Pour243(t11) : poids>=6 et |C_x|<=8. Ce n'est PAS une borne8
sur tout le stabilisateur de x : les permutations de paires restent possibles.
Si le retournement de TOUTES les paires est un automorphisme, alors pour t
impair C_x={0,1} : un autre mot et son complement ne peuvent tous deux
avoir poids>t/2.

Pour un squelette K_x, son code local C_K peut etre plus grand. Chaque mot
local de poids inferieur au seuil est un automorphisme de K_x qui ne peut
s'etendre a AUCUNE completion comme automorphisme. Il envoie donc chaque
completion sur une autre matrice etiquetee, isomorphe. Cela exclut l'unicite
etiquetee, pas l'existence ni l'unicite a isomorphisme pres. La conjecture S
de Claude impliquerait que l'absence de lignes plates force deja cette
distance minimale dans C_K ; exclure seulement les flips individuels est
plus faible. Aucun contre-exemple de SRG a S etabli ici.
Preuve complete : pure_flip_majority_theorem.json. Aucun solveur lance.

### Consequence pour le solveur : combiner majorite et nombre de completions

Claude689 apporte un critere CONDITIONNEL de reconstruction par49 lignes :
si le rang spectral restreint atteint44, ces lignes determinent G. Ce rang
n'est pas prouve pour toute configuration. Pas de nouveau resultat global
de rang annonce, et pas de nouvelle campagne lancee.

NOUVELLE COUPURE PAR ORBITES : soit Omega l'ensemble des completions SRG
et L un groupe de retournements purs preservant TOUTE l'instance fixee.
Pour Conway, chaque element non nul de poids1,2 ou3 agit sans point fixe,
par le theoreme de majorite. Si r retournements INDIVIDUELS preservent
l'instance, avec r<=3, leur sous-groupe agit librement : |Omega| est un
multiple de2^r, meme si les graphes completes ont d'autres automorphismes.

En particulier, DEUX retournements individuels donnent quatre elements :
0,s,u,s+u. Les trois non nuls ont poids1,1,2 et aucun ne peut fixer une
completion. Donc |Omega| est multiple de4. Si un certificat donne au plus
DEUX completions etiquetees, la branche est impossible pour TOUT SRG,
pas seulement dans C1. Cela combine directement le theoreme de majorite
avec notre ancien regime de completion residuelle de rang au plus1
(coclique_rank_one_completion.py, dont les bords43 spectraux positifs).

Version plus generale : S={s dans L : 0<poids(s)<ceil(t/2)}. Une orbite
de taille2 definirait une forme lineaire chi sur L avec chi(s)=1 pour
tout s dans S. Tester b.s=1 sur F2 (t inconnues) suffit. Une dependance
impaire XOR-zero entre ces mots est un certificat d'incompatibilite.
Elle exclut les orbites1 et2 ; toutes les orbites restantes ont taille
multiple de4. Un majorant certifie U<=3 donne alors Omega vide.
Un test compatible ne prouve aucune existence.

Pour C1 uniquement, la regle generale est encore plus simple : tout
groupe L de l'instance agit librement sur ses completions asymetriques.
Si le nombre total de completions est majore par U<|L|, aucune completion
C1 n'existe. Une completion symetrique peut rester, sauf si la coupure
par petits retournements ci-dessus l'exclut egalement.

PORTEE : groupe de l'instance ENTIERE, pas seulement du squelette lorsque
d'autres contraintes ont ete ajoutees. Bloquer une seule matrice connue
peut casser cette invariance. Le squelette rigide Gamma6 n'offre aucun
retournement non trivial a exploiter. Aucune branche concrete reunissant
le majorant et ces symetries n'est fournie ici ; aucune exclusion de C1,
aucune acceleration mesuree et aucun ajout au solveur. Preuves et regles
precises : flip_orbit_completion_filter.json. Le resultat est une coupure
conditionnelle finie, pas une borne sur le cout total de recherche.

### Objet49 : domaines des50 colonnes et graphe residuel presque biregulier

Lecture/ack Claude692, reponses693 et694. Claude traite les structures
admissibles sur S=L_a union L_a' union L_b (34 labels) et leurs conditions
spectrales. De mon cote : colonnes et completions, sans refaire son travail.
Le script ancien code/omega/twostar_psd.py ne genere que DEUX etoiles mates
(24 labels), pas trois ; contraintes exactes transmises, sans le relancer.
Il execute20000 tirages au chargement et n'exporte aucun objet.

Les50 sommets hors R=N[x] union S ont des etiquettes FIXES : paires non
mates parmi les11 lettres hors {a,a',b}. Quarante evitent b', dix le
contiennent. Pour h=N(u) inter S et delta=[b' dans u], les sommes sur
L_a,L_a',L_b sont2,2,2-delta. Avec p={a,b},p'={a',b}, z=h_p,z'=h_p',
les groupes disjoints de tailles11,11,10 contiennent2-z,2-z',2-delta-z-z'
voisins. Leur nombre de profils vaut148346 (delta0) ou31460 (delta1).
Les autres budgets de voisins communs avec les14 lettres reduisent ces
nombres a94743 et25926 : enumeration exacte0,343s, aucun seed utilise.
Ventilation par degre futur6/7/8 :84582/10044/117 et0/24776/1150.

THEOREME SUR LE BLOC U50 : ses degres sont TOUS6,7,8 ; AU PLUS TROIS
sommets ont degre8. Plus precisement, epsilon=Gamma_pp',
  d=1-epsilon-(Gamma^2)_pp' dans{0,1},
  j=2-somme Gamma[v,w] pour v=p,p', w={a,b'},{a',b'} dans{0,1,2}.
Alors n8=d+j, n7=28+2epsilon-2n8, n6=22-2epsilon+n8. Ces trois effectifs
sont donc fixes par Gamma. Si epsilon1, d0 et n8<=2. Les positions des
degre8 ont au plus C(40,d)*C(10,j)<=1800 choix (pas les graphes entiers).

Preuve : deg_U(u)=6+delta+z+z', et z+z'<=2-delta. Les sommes d'etoiles
donnent deg_Gamma(p)=deg_Gamma(p')=3-epsilon, donc9+epsilon voisins
exterieurs pour chacun. On trouve |E(S)|=68+epsilon, |E(R)|=157+epsilon,
|E(R,U)|=372-2epsilon, |E(U)|=164+epsilon. Les degre8 sont exactement
les d voisins communs exterieurs de p,p' sans b', et les j sommets avec
b' adjacents a l'un des deux. Chacun de p,p' a exactement un voisin
lointain portant b' : j est determine par ceux deja presents dans S.

PREPROCESSEUR EXACT ecrit : code/codex/three_star_column_domains.py.
M=8T_SS=24I-8Gamma-8K_SS, avec8K=3*intersection+incidences_mates-2.
Chaque colonne m=-8h-8K_Su doit etre dans im(M) et satisfaire
m_I^t M_II^-1 m_I<=20, egalite au rang30. Les relations du noyau sont
traitees par jointure de petites listes (55,55,45 au plus). Au rang r,
la somme des deficits rho=20-m_I^t M_II^-1 m_I vaut56*(30-r).
Le moteur filtre aussi les capacites de DD^t, les voisins communs connus,
les marges possibles apres enumeration et l'histogramme des degres.
Toutes les operations de rejet sont entieres/rationnelles ; limite de
temps pour l'enumeration, domaines incomplets explicitement signales.

DISTINCTION ESSENTIELLE : au rang30, Gamma/B ne donnent PAS les50 colonnes.
Une fois ces colonnes choisies, leur produit Gram force les aretes de U.
Le produit des tailles des domaines est alors un majorant des completions,
encore potentiellement enorme. Le choix simultane des50 profils n'est
pas implemente. Aucun objet49 PSD de rang<=30 fourni/traite dans ce tour,
aucun graphe99 construit ou exclu, aucun gain de temps global mesure.

Controles de NOS primitives : comptes exhaustifs des domaines, relation
lineaire supplementaire12100/1210, norme rationnelle creuse contre dense,
conditions de Hall sur les degres. Pas de nouvel audit de graphe du pair.
SymPy1.14.0 installe dans c1-lambda1-env pour ce calcul exact. Sources,
preuves et rapports dans data/codex_three_star_completion_20261014/.

### Limite exacte de la relaxation continue a trois etoiles

Claude695 : aucun Gamma34 PSD dans40 tirages ; coupes MILP toujours sans
temoin ; passage a une relaxation continue. Pas de reproduction de ses
tirages. Construction de MON cote d'un temoin fractionnaire explicite,
specialisation de l'ancien operateur force E0, transmise au pont696.

Sur les84 labels, Gamma0_yz=(2-|y inter z|-m(y,z))/10, m comptant les
incidences de mates. Les entrees sont0,1/10,1/5 et la diagonale0.
Avec D l'incidence14x84, DD^t=11I+J-B_matching et
(DD^t)^(-1)=(11I+B_matching)/120-J/240. On obtient exactement
  T0=3I-Gamma0-K=3Pi, Pi=I-D^t(DD^t)^(-1)D.
Donc0<=T0_SS<=3I<=7I. Le temoin satisfait les trois comptes d'etoiles,
les plafonds naturels (B49^2)_ij<=2-B49_ij et les degres<=14.

Mais rang(T0_SS)=31, pas30. Un vecteur dans ker(Pi_SS), prolonge par zero,
est D^t f porte sur S. Les50 paires restantes imposent f_c+f_d=0 sur les
11 lettres hors des centres. Leur graphe est connexe et contient un
triangle, donc tous ces poids sont nuls ; restent les3 poids des centres.
Nullite exactement3. Il manque donc bien une quatrieme relation.

Consequence : les comptes/plafonds continus annonces et les coupes PSD
SEULS ne peuvent pas exclure ce point. L'integralite et la condition
non convexe de rang<=30 restent des obstacles distincts. D'eventuelles
contraintes supplementaires du LP du pair peuvent changer la relaxation ;
aucun jugement sur son implementation, aucun nouvel audit de ses calculs.

Certificat exact entier/rationnel produit en2,57s par
code/codex/three_star_fractional_witness.py : Pi^2=Pi, D Pi=0, identite
T0=3Pi, rang31 et plafonds verifies pour NOTRE temoin. Marge minimale sur
les plafonds des paires de S :16/100. Matrices sauvegardees dans
data/codex_three_star_completion_20261014/fractional_psd_witness.json.
Ce fichier est volontairement fractionnaire, non accepte comme entree
binaire du preprocesseur de colonnes. Aucun graphe99 construit ou exclu.

### Exemple binaire PSD du pair : le filtre de rang reste indispensable

Claude697 fournit une structure BINAIRE a trois etoiles,68 aretes sur S,
avec T_SS PSD mais de rang EXACT31 (calcul rationnel du pair). Chemin
cote LAB : work/stars_rank_2026-10-14/lns3_psd_found.json. Resultat accepte,
sans refaire sa construction, son calcul de rang ni sa recherche locale.

Cela renforce notre temoin fractionnaire : meme les comptes/plafonds,
l'integralite ET la positivite ne rendent pas automatique le rang<=30.
Ce cas partiel particulier ne peut pas se completer en Conway, puisque
le rang du bloc principal31 excede le rang30 du Gram residuel global.
Ce n'est ni une exclusion globale de C1 ni un succes du filtre des50
colonnes. Le pair cherche un premier exemple de rang<=30 ; aucun tel
exemple n'est encore entre dans notre preprocesseur. Pas de relance ici.

### Pourquoi31, et comment viser exactement la quatrieme relation

Dilan demande une recherche propre sur la question du rang31. Claude
interroge via698, export de son Gamma34 demande via699. Le fichier LAB
n'est pas present dans l'arbre Recherche_Conway Windows. Pas de recopie
ni d'audit de son rang. Travail ici sur le mecanisme de modification.

Les trois indicatrices d'etoiles forment un noyau force independant.
Rang31 signifie exactement que T est positif defini sur leur orthogonal
H de dimension31. Conway impose une relation supplementaire parce que
le Gram residuel global a rang30. Cela ne fait pas du rang31 un theoreme
universel sur les configurations locales ni une obstruction d'asymetrie.

Resultat neuf exploitable : un echange d'aretes en rectangle s'ecrit
DeltaGamma=sigma(a*b^t+b*a^t), a=e_u-e_r, b=e_v-e_s, quatre sommets
 distincts. Il preserve les trois relations ssi u,r sont dans une meme
cellule d'appartenance aux centres et v,s aussi. Les tailles des cellules
non triviales sont11,11,10 ; les deux recouvrements sont des singletons.
Donc10585 formes de rectangles au total, aucune ne peut changer les
lignes des deux recouvrements. Toutes conservent les degres.

Avec G=T^+ sur H, alpha=a^tGa, beta=b^tGb, gamma=a^tGb, le determinant
relatif apres echange vaut F=(1-sigma*gamma)^2-alpha*beta. Blanchir T
reduit la modification a deux dimensions : les deux valeurs propres
non triviales sont1-sigma*gamma +/- sqrt(alpha*beta). La plus grande
est strictement positive. Donc F>0 conserve PSD/rang31, F=0 donne
EXACTEMENT PSD/rang30, F<0 cree une valeur propre negative. Au zero,
q=G(sigma*beta*a+(1-sigma*gamma)*b) donne la nouvelle relation.

Code three_star_rank_repairs.py : une inversion rationnelle du quotient
pour toutes les reponses, numerateur entier exact de F, filtrage binaire
et plafonds locaux, export d'eventuelles reparations de rang30 satisfaisant
aussi T<=7I. Pas de recalcul complet du rang du seed. La certification
PSD31 du producteur est une precondition explicite. Pas encore de seed
recu ; aucun resultat de ce balayage n'est annonce pour l'exemple LAB.

Tests des nouvelles primitives : six cas exacts T=c*P_H, c=1,2,3,
signes+/-, couvrant les trois issues ; relation nouvelle verifiee aux
zeros. Passage en1,08s. Pas d'audit independant d'un resultat du pair.
Preuve et limites dans rank31_switch_theory.json. Les echanges plus
longs et ceux modifiant les recouvrements restent hors de cette famille.

### Premier rang30 du pair : grille comprise, completion refusee a la colonne suivante

Claude700 fournit la4e relation explicite : le carre de quatre labels
croises d'une grille3x3 a son indicatrice dans ker(T). La grille force
DONC rang<=30 ; l'egalite30 est celle de ses exemples, pas une consequence
universelle de la seule presence d'une grille. Son exemple invariantZ5,
69 aretes, PSD/rang30, est accepte et importe depuis sa liste d'aretes
(lab700_z5_rank30.json). Aucun nouvel audit du calcul du pair.

Application NEUVE de notre filtre de completion : le premier label
manquant {3,4} suffit. Enumeration complete de cette colonne :31460
profils bruts,20250 compatibles avec le noyau,228 avec les plafonds
locaux. Parmi ces228,77 ont m_I^t H^-1 m_I<20,151 ont une norme>20,
aucun n'a la norme20 necessaire pour conserver le rang30. Les77 premiers
peuvent ajouter une dimension PSD, donc rang31, interdit pour Conway.
Les151 autres rendent l'extension nonPSD. Cette configuration locale
precise est donc noncompletable en SRG99, sans campagne SAT ni
hypothese de symetrie sur une completion. Calcul exact0,157s (hors
lancement Python), resultat envoye au pont703. Aucune exclusion de la
familleZ5 complete ni des grilles en general. Diagnostic de norme ajoute
au preprocesseur ; rapport lab700_column_domains.json.

### Balayage exact d'un echange sur le rang31 du pair

Claude702 transmet enfin l'exemple binaire68 aretes. La nouvelle analyse
par reponse de rang2 couvre10585 rectangles :374 binaires legaux,
259 rejetes par les plafonds locaux,115 admissibles. Parmi115 :102
rendent T nonPSD,13 gardent PSD/rang31, ZERO donne le rang30. Calcul
exact0,075s, sans audit de son rang initial. Rapport lab702_one_switch.
Les recouvrements restent fixes ; il n'y a donc aucun resultat global
sur toutes les reparations. Exploration bornee de ces13 voisins lancee
ensuite pour chercher un mecanisme en plusieurs echanges.

### Obstruction arithmetique courte de notre exemple700

La norme de la colonne {3,4} ne peut pas etre20, MEME avant les plafonds
locaux. Sur les20250 profils de noyau, aucune norme n'est entiere. Une
preuve courte remplace cette enumeration : H^-1=N/d avec d=38230440,
43 divise d et N=7*r*r^t(mod43). Les poids r valent1 sur{0,2},{1,2},
4 sur{0,x},{1,x} pour x pair>=4,2 sur{2,x} pour x pair>=4,0 ailleurs.
La relation de grille oblige h=0 sur les4 labels de grille. Il reste
2 choix A,2 choix A',1 choix B. Si e est le nombre de x pairs parmi
les4 premiers et f parmi le dernier, r^tm=62-32e-16f. La norme20
impose r^tm=0(mod43), donc n=2e+f=20(mod43), mais0<=n<=9. Impossible.
Certificat exact dans lab700_mod43_certificate.json, script reproductible
three_star_grid_mod43.py. Ce resultat porte sur cette frontiere.

### Deuxieme Gram ambiant : une famille exclue et16 coupes lineaires

En cherchant la structure de cette obstruction, derivation d'une borne
plus forte que T_SS<=7I. Pour le graphe complet, T=7P avec imP contenu
dans kerD (D incidence14x84). Pi projette sur kerD. Donc0<=T<=7Pi,
et pour CHAQUE bloc S, T_SS<=7Pi_SS. Le Gram complementaire est
 U=7Pi_SS-T_SS=4I+Gamma-(4*inter-mates+2J)/15.
Ainsi15U=60I+15Gamma-4*inter+mates-2J doit etre PSD. Les identites
completes viennent de DD^t=11I+J-B_matching et Gamma^2+Gamma=12I sur
kerD. Il s'agit du second cote spectral de la completion ; aucune
hypothese d'automorphisme n'est introduite.

Consequence combinatoire : choisir des signes opposes sur chaque paire
mate parmi4..13, poser q_{c,x}=s_x pour c=0,1,2 et x>=4, q=0 sur
les4 autres labels. On a q^tq=30, q^tPi q=q^tKq=45/2. Donc
 q^tGamma q>=-90, soit e_croisees-e_memes<=45.
Il y a16 coupes distinctes modulo signe global. Avec une grille sur
{0,1}/{2,3}, ses4 labels sont un C4 isole dans Gamma et les30 autres
labels portent65 aretes. Il faut donc AU MOINS10 aretes de meme signe
pour CHACUNE des16 orientations. Toute cette famille a grille avec
65 aretes toutes croisees pour une orientation est exclue. C'est plus
large que deux exemples, mais ce ne sont PAS toutes les grilles/Z5.

700 et EX2 du message704 violent la coupe :0 meme,65 croisees,
q^t(15U)q=-600. EX0 passe U PSD entier, mais notre filtre de colonne
{3,4} donne553 profils locaux,4 de norme<20,549>20,0=20 : EX0 est
lui aussi noncompletable (0,235s). Les3 frontieres a grille fournies
sont exclues, sans supposer de symetrie de leur completion. Les11
graines PSD31 (702 et S61..70) passent U PSD : la nouvelle borne ne
resout pas leur4e relation. Resultats transmis708 puis message de lot.

Implementation three_star_ambient_upper.py :16 coupes puis decision
rationnelle de PSD, avec temoin entier pour toute negativite. Des
vecteurs numeriques peuvent proposer un petit temoin, mais la valeur
negative est calculee exactement. Integre a three_star_column_domains
et aux candidats exportes par three_star_rank_repairs. Tests propres :
petits cas PSD singuliers/indefinis, U=4Pi pour notre temoin fractionnaire,
et energies exactes des16 orientations. Aucun nouvel audit des rangs
T du pair. Rapports individuels et synthese ambient_upper_seed_summary.

### Limite de l'exploration des echanges

Depuis702,200 etats PSD31 traites en10,64s ;1936 etats encore en file,
aucune reparation de rang30. Arret borne, sans pretention d'exhaustivite.
Sur les10 nouvelles graines S61..70 du pair, tous les echanges simples
admissibles sont examines ; aucun F=0. La conjecture du pair « PSD et
rang<=30 implique grille sur(l,m) » n'est NI prouvee NI refutee. De
plus, les rectangles conservent les lignes des recouvrements, et une
hypothetique nouvelle relation pourrait correspondre a une autre grille
deja contenue dans S ; il faudrait la classifier avant de dire hors-grille.

### Trois nouvelles frontieres passent les deux Grams, mais pas la premiere colonne

Claude709 : parmi10000 structuresZ5 examinees,595 sontT PSD et572
passent aussiU PSD ; toutes ont le rang30 via leur grille. Donnees du
pair acceptees, sans reproduire sa campagne. Il transmetV0,V7,V15.
Application du travail de completion propre, apres import des aretes :
 V0 :491 profils locaux pour{3,4},42 norme<20,449>20,0=20 ;
 V7 :698 profils,52<20,646>20,0=20 ;
 V15:786 profils,52<20,734>20,0=20.
Enumerations completes0,22-0,24s parfrontiere. Tous trois exclus, donc
6 exemples a grille transmis sont noncompletables, dont4 qui passaient
les deuxGrams. Ceci n'exclut PAS tous les572 cas de l'echantillon,
encore moins toute la familleZ5. Le lot572 serait un calcul fini
abordable pour ce filtre (aucun domaine nonvide n'a encore ete trouve).
Message de resultats envoye au pair ; aucun calcul de groupe ni campagne
SAT, aucune verification du rangT annonce par lui.

### Lot713 : les572 frontieres fournies sont toutes noncompletables

Message713 deClaude : export Windows lab_exchange_2026-10-14/z5_valid_all.json,
572 frontieresZ5 retenues parmi les10000 premieres configurations enumerees,
T PSD, U PSD et rang30 certifies par le pair. Entree388969octets, SHA256
8640aec5d9fc8e7ce5471928216678d245054dd35c6e0c8ecd8a3517e55363ac.
Aucun recalcul des certifications du pair : nouveau mode du preprocesseur
--producer-certified-grid-rank30. Les3 etoiles et la grille donnent les4
relations connues ; leurs pivots choisissent une base principale de taille30.
Seule l'inverse rationnelle necessaire a NOTRE filtre de colonnes est calculee.
Le changement de base a ete compare sur notre precedent rapportEX0 : memes
comptes et meme norme minimale exacte. Pas de repetition d'un audit du pair.

Resultat exhaustif pour CE LOT,572 adjacences etiquetees distinctes :
-75 rejets immediats par un plafond de voisins communs dans B49 ;
-496 domaines vides pour le label manquant{3,4} ;
-1 survivant de{3,4}, indice282 en base0, puis domaine vide pour{3,5}.
Premier passage39,95s ; suite sur282 en0,125s. Aucune interruption ni
aucun domaine incomplet utilise pour exclure un cas. Aucun restant.

Pour282, {3,4} admet exactement le profil {0.9,0.13,1.6,1.10,2.9}.
La colonne{3,5} a804 profils locaux :46 de norme<20,758>20,0=20.
Exemple de plafond viole (indice2 du lot) : le voisin de racine5 et
le label{2,8}, nonadjacents, ont deja3 voisins communs dans la frontiere,
{0,5},{1,5},{2,5}, au lieu de mu=2. Les75 preuves elementaires sont
exportees dans cap_obstructions.json.

Script reproductible pour le premier passage : code/codex/three_star_column_batch.py.
Snapshot source, rapportsJSONL des572 cas, deuxieme passe sur282 avec
profils exacts, synthese et petites preuves sont sauvegardes dans
 data/codex_three_star_completion_20261014/lab713_batch/.
La synthese separe le bilan du premier passage du verdict final.
Le premier passage est reproduit par --input input_source_snapshot.json
--output-folder DOSSIER ; la suite par three_star_column_domains.py
--gamma survivor_282.json --producer-certified-grid-rank30 --save-profiles.
Resultats transmis au pair par le pont, avec correction explicite de portee.

PORTEE : les572 proviennent d'un PREFIXE de10000 structures. Il n'est
pas etabli que le lot soit exhaustif pour toutes les structuresZ5 a
3etoiles. Aucune exclusion de toute cette famille n'est donc annoncee,
ni de C1. Aucune symetrie de la completion n'a ete supposee. Le resultat
constitue une exclusion finie exacte du lot et montre que son filtrage
est abordable ; ce n'est pas une borne du nombre total de frontieres.

### Relation hors grille du pair714 et classification COMPLETE sur deux etoiles mates

Claude714 fournit z2b, objet local T/U PSD, rang exact30, sans la grille
sur(l,m), avec4e relation1_Y pour Y={0,1} x {2,3,12,13}. Gamma_Y est un
8-cycle. Resultat du pair accepte : l'hypothese locale « rang30 implique
la grille designee » est FAUSSE. Son exemple est importe depuis le depot
d'echange Windows, sans recalcul de son rang ni de ses deux PSD.

Apport propre : classification de T_X sur X=L_a union L_a',24 labels.
Chaque sommet de Gamma_X a1 voisin dans chaque etoile, donc Gamma_X est
2-regulier. Les2 indicatrices sont dans kerT_X. Sur leur orthogonal H,
ecrire q=(f,g), sommes f=g=0, et B le matching des12 lettres exterieures.
On a q^tKq=[3||f+g||^2+(f+g)^t B(f+g)]/8, d'ou l'identite EXACTE :
 q^tTq = somme_{yz arete Gamma_X}(q_y-q_z)^2
        +(1/2) somme_x(f_x-g_x)^2
        +(1/8) somme_{paires mates{x,x'}}(f_x+g_x-f_x'-g_x')^2.
Cela prouve a la fois PSD automatique a2etoiles mates et caracterise
TOUT le noyau supplementaire : constant sur les aretes de Gamma_X,
identique entre les2 copies de chaque lettre, identique entre mates.

Construire Q sur les6 droites autres que l ; une arete de Gamma_X relie
les indices des droites de ses2 lettres exterieures. Si Q a c composantes
M_1,...,M_c, les relations sont engendrees par les2 etoiles et les1_{l x M_j}.
Une seule dependance : somme des1_{l x M_j}=somme des2 etoiles. Ainsi
 nullite(T_X)=c+1, rang(T_X)=23-c.
Sous PSD de la3e etoile, toute relation de X propagee par zero reste une
relation (energie nulle dans une matricePSD). La3e etoile ajoute1relation
independante : rang(T_S)<=32-c. Pour c=2, les types de bipartition sont
1+5 (carre ferme droit ou tordu, correction722),2+4,3+3. Ce theoreme classe les relations PORTEES par les
2etoiles mates ; il ne classe pas les relations avec des coefficients
nouveaux sur la3e etoile. C'est la limite precise de l'analogue H3'.

L'identite est controlee symboliquement sur tout H de dimension22, et
sur un exemple de matchings construit ici, pas sur les rangs du pair.
Script two_mate_star_structure.py ; preuve two_mate_star_kernel_theory.json.
Applique comme description combinatoire a z2b : Q a les composantes
{1,6} et{2,3,4,5}, formule rang21 a2etoiles et borne30 a3etoiles.
Aucun calcul de rang pour produire cette description. Resultat envoye717.

### z2b ne se prolonge pas, malgre son mecanisme local nouveau

Mode de preprocesseur generalise aux relations fermees certifiees :
--producer-certified-closed-pairs 1 6. Les certifications T/U PSD et
rang30 du pair sont utilisees telles quelles. La colonne{3,4} a13888
profils de noyau,1112 profils locaux,18 normes<20,1094>20,0=20.
Enumeration complete0,094s : z2b ne se complete pas en SRG99. Cela ne
retire RIEN a son statut de contre-exemple local a « rang30=>grille ».
Snapshot et rapport : data/codex_three_star_completion_20261014/lab714_closed_cycle/.
Resultat envoye719. Ni ce cas ni le lot572 n'excluent toutes les frontieres.

### Correction de portee des graines de rectangles, messages716/718

Le pair716 precise que son ancien generateur omettait des plafonds
partiels vers les lettres hors des3 etoiles. S61,S62,S64,S68 les violent
et sortent des graines localement admissibles ; les autres et z2b les
respectent. La synthese des rectangles est annotee. Le marcheur exige
maintenant ces plafonds sur le seed avant le filtrage incremental des
4 lignes changees. Nouveau garde teste sur S61 : rejet avant analyse.
Les reponses de rang2 anterieures restent des calculs spectraux, mais
les4 graines ne doivent pas etre comptees comme frontieres admissibles.
Aucune relance d'audit du pair. Claude a ajoute ces plafonds au generateur.

Claude718 travaille sur la possibilite Q connexe avec rang30 a3etoiles.
Formulation precise : la relation SUPPLEMENTAIRE modulo les3 indicatrices
serait representable sur les2 etoiles mates. L'enonce n'est pas etabli.
Son exploration reste distincte de nos relations fermees/colonnes.

### Message720 : trois conjectures separees et nouvelle transition exacte de noyau

Claude distingue(A) : Q connexe et T/U PSD impliquent rang31 a3 etoiles ;
(B) : tout Conway possede une droite speciale(c>=2) ; (C) : tout Conway
possede une droite non speciale. Toutes trois OUVERTES. Le lemme intrinseque
c(l)+1=dim(E_3 supporte sur N[l]) s'ecrit directement par Schur :
F=3I-A[N[v]] a son bloc lettres3I-B_mate>0 et le dernier pivot-4.
Il est inversible ; la restriction E_3 -> kerT est un isomorphisme, puis
PSD propage les relations de X. Aucun renvoi a une vieille note necessaire.
Meme(B) ne prouverait pas, seule, un cout ABORDABLE pour toute l'enumeration.

PROUVE : pour T PSD rang30, noyau des3 etoiles plus q, une modification
T'=T-sigma(ab^t+ba^t) preservant les3 etoiles est classee exactement.
Poser r=a.q, s=b.q, delta=-2sigma*r*s, w=s*a-r*b. Si delta>0,
eta=delta-w^t T^+ w distingue PSD rang31(eta>0), PSD rang30 avec nouvelle
relation(eta=0), et indefini(eta<0). Preuve ecrite : elimination du pivot
positif cree sur l'ancien noyau, puis downdate H-z z^t/d. Si delta=0
et exactement un contraste non nul, energie nulle mais image non nulle,
donc impossibilite PSD. Script three_star_connected_repairs.py, preuve
connected_repairs_720/rank_update_theory.json. Trois exemples propres
exacts de dimension3 couvrent les trois signes ; pas d'audit des graines.

VERIFIE : z2b fournit40 rectangles binaires deplacant sa relation fermee,
26 rejetes par plafonds,14 admissibles mais tous indefinis apres modification.
Sur le lot572,75 entrees sont deja invalides comme auparavant ; les497
autres donnent4970 rectangles reliant les2 composantes de Q :2270 PSD
rang31,2700 indefinis, aucun rang30. Temps26,48s. Ce resultat epuise
ces rectangles sur ce lot seulement, et ne prouve PAS(A). ArtifactsJSONL
dans data/codex_three_star_completion_20261014/connected_repairs_720/.
Prochaine variation : circuits de relations entre les3 indicatrices,
autorisant aussi le mouvement des2 sommets de recouvrement jusque-la figes.

### Circuits mobiles, limites exactes et deux obstructions de conjugaison

PROUVE : les colonnes des3 indicatrices ont les5 types e0,e1,e2,p=e0+e2,
p'=e1+e2. Leurs dependances minimales sont155 differences paralleles,
220 relations p-e0-e2 ou p'-e1-e2 et121 relations p-p'-e0+e1.
Les paires disjointes de ces496 circuits donnent67730 echanges de rang2,
dont57145 depassent les anciens rectangles et peuvent bouger les recouvrements.
Code three_star_circuit_trades.py ; preuve circuit_trade_theory.json.
Cela ne couvre PAS toutes les modifications de rang2 ni de rang superieur.

VERIFIE : sur702, les nouvelles directions donnent106 echanges binaires,
34 locaux,31 indefinis et3 PSD31, aucun rang30. Puis une levee eta>0
choisie pour chacune de298 sources du lot donne298 graines connexes PSD31.
Leurs67730 directions chacune produisent136476 echanges binaires,
33271 locaux :25874 indefinis,7099 PSD31 et298 PSD30. Les298 derniers
ANNULENT EXACTEMENT la levee initiale : aucun nouvel objet de rang30.
Premier passage236 graines55,14s ; suite62 graines3,60s. Aucun contre-
exemple(A), aucune preuve(A). Les levees intermediaires ne sont pas
filtrees par U ; tout nouveau candidat connexe30 aurait du passer U.
Les duplicatas des sources sont retires des exports ; les recettes
inversees exactes suffisent et les retours de source ne sont plus audites.

PROUVE : pour un4-cycle alterne u de l'incidence D_S, H=I-uu^t/2
fixe D_S^t, K et Pi ; une conjugaison binaire Gamma'=H Gamma H conserve
donc T,U,rang. Deux obstructions de METHODE, pas une preuve(A) :
(i) l'indicatrice du carre ferme sur la droite b est D_S^t w avec
w=(1,1,1,1,-1,...,-1)/2 ; toute conjugaison fixant l'incidence la fixe.
(ii) pour un ensemble ferme de2 droites CONTENANT b, tout4-cycle qui
deplace son indicatrice q produit z=2Hq avec une seule coordonnee
negative-1, en(b,y) hors composante. Kz y vaut-2 ; l'equation
Gamma'z=3z-Kz y exigerait-1, impossible avec matrice nonnegative et
diagonale0. Preuve incidence_reflection_obstructions.json.
Controle symbolique des5 positions possibles :160 reflets mobiles,
tous frappes par cette obstruction ; aucune matrice du pair re-auditee.
Sur z2b,22 des32 reflets mobiles ont une diagonale non nulle,10 ne sont
pas entiers. Le cas2+4 avec b dans la composante4, et3+3, echappent a
cette obstruction. Cette zone manque a nos graines actuelles ; signale724.

### Messages722-723 et conservation rigoureuse des statuts

CORRECTION de terminologie722 : une composante singleton de Q force un
CARRE FERME, droit ou tordu (matching croise echange), pas necessairement
la grille geometrique. Phrase corrigee dans two_mate_star_kernel_theory.json.
Les relations d'indicatrices et les filtres qui les utilisent restent
valides ; les exemples explicitement certifies grilles restent tels quels.
Le theoreme de relations mixtes du pair722 a4 etoiles est accepte et
consigne avec provenance, sans nouvel audit. Je n'ai pas de somme de
carres positive a3 etoiles : le Schur10x10 reste signe. (A),(B),(C) OUVERTS.

PROUVE, transmis725 pour la recherche du pair sur les bases : avant la3e
etoile, une base39 laisse60 labels, chacun avec4356 profils bruts de
voisinage vers X (2 voisins dans chaque etoile), et un reste8-regulier.
Si c=1, rang22 sur X et rang8 restant ; le budget exact des60 normes de
projection pour M=8T est752, les deficits totalisent448. En general la
somme vaut808-56c, par le projecteur global M/56. Ce filtre SUR LA BASE
n'est pas encore implemente ni demontre contradictoire pour toute base.
Preuve intrinseque de c(l), budgets et statuts :
connected_repairs_720/line_invariant_and_base_budget.json.

Les57145 nouvelles directions ont aussi ete parcourues sur les6 autres
graines31 localement admissibles du pair(S63,S65,S66,S67,S69,S70),
sans recalcul des rangs sources :637 mouvements binaires,192 locaux,
166 indefinis,26 PSD31,aucun rang30. Additionnes a702, cela couvre
les7 graines historiques valides pour cette nouvelle famille de mouvements.
Synthese six_seed_circuit_summary.json. Aucun processus de recherche
reste en cours a la fin de ce passage ; aucune campagne globale lancee.

### Nouvelles bases du pair726 :2+4 avec b dans4, puis3+3

SourceWindows lab_exchange_2026-10-14/dec_seeds.json, SHA256
ceb0ec8edef6e227e836707b5db7ce3f8634d5cfd431df21d9ec3aeec4337192.
dec81/82 : composanteM={2,3} en indices de paires, b dans l'autre ;
dec83/84 : M={2,3,4}. Les4 certifications T/U PSD, rang30,c2 etplafonds
sont acceptees du producteur. Snapshot et travail dans lab726_decomposable/.

VERIFIE : chacune est exclue par la colonne manquante{3,4}. Les comptes
complets (local ; norme<20,=20,>20) sont81:(1013;48,0,965),
82:(1452;102,0,1350),83:(881;74,0,807),84:(779;47,0,732).
Temps par enumeration0,078-0,109s. Les2+4 ont12320 profils de noyau,
les3+3 en ont12510. Les50 domaines ne sont pas tous parcourus puisqu'un
seul domaine VIDE suffit. Ce n'est pas une exclusion des types entiers.

Les192 reflets4cycles mobiles des4 graines echouent tous a produire une
adjacence binaire sans boucles(89 diagonales non nulles,103 non entiers).
Les192 rectangles mobiles donnent82 rejets de plafonds,96 indefinis,
14 PSD31,aucun rang30. Nouvelle marche three_star_rank30_walk.py :
les circuits disjoints r=s=0 utilisent le critere determinant sur l'image
de rang30 ; les circuits mobiles utilisent eta. Le pseudo-inverse sur
une base principale n'est applique qu'a des vecteurs de l'image, notamment
w=s*a-r*b. Controle propre sur deux projecteurs rationnels construits,
sans aucune matrice du pair :4 identites exactes PASS.

VERIFIE/BORNE :400 etats explores en24,40s ;5000 en file,402 ecartes a
la borne de stockage.50328 mouvements locaux :10252 PSD30 conservant le
noyau,2330 PSD31,13636 indefinis en deplacant le noyau,16474 indefinis en
le conservant,7636 impossibles par energie nulle/negative de l'ancien noyau.
Aucun nouveau noyau de rang30,aucun rang29.19200 reflets mobiles sur
ces etats,aucun binaire. Ne pas annoncer une composante epuisee. U n'est
pas filtre sur les etats intermediaires ; il serait exige sur un candidat.
La marche est terminee, pas en arriere-plan. Correction defensive du
scanner : un nouveau rang30 peut avoir Q encore deconnecte ; il est
classe ainsi, sans l'annoncer comme contre-exemple a(A).

### Message727 : rectification du carre tordu et invariant de droite

Les resultats du pair727 sont acceptes sans refaire ses preuves. Sous les
seuls axiomes de matchings a deux etoiles, le carre ferme peut etre tordu.
Sous les plafonds complets de voisins communs avec les lettres racines,
le cas tordu est impossible : il donnerait trois voisins communs au lieu
de deux. Ainsi une composante singleton de Q dans un bord admissible est
bien une grille3x3. Ceci rectifie l'entree722 ci-dessus et le JSON de theorie.

Le pair identifie aussi c(l) au nombre de composantes du graphe cubique H_l
sur les36 voisins de la droite hors de celle-ci. Une composante a6r sommets ;
chaque sommet eloigne de la droite y a r voisins. Le graphe induit restant
sur60 sommets a valeur propre-4 de multiplicite7+c(l), et3 de multiplicite18.
Provenance et portee : prescribed_kernel_728/peer727_line_structure.json.
Les observations sur les huit graphes243 ne prouvent ni(B) ni(C).

### Construction avec noyau prescrit et obstruction binaire generale

Nouveau moteur three_star_prescribed_kernel.py : aucune graine du pair en
entree. On impose trois etoiles et z=2q+u dans le noyau, q indicatrice de
l x M, u un cycle signe d'incidence. Contraintes binaires, plafonds locaux
complets,16 coupes d'orientation ; les futures coupes spectrales utilisent
des valeurs quadratiques entieres negatives. Les deux premiers modeles
(r2,y8 et r3,y10, u rectangle) donnent CP-SAT INFEASIBLE en environ2s
chacun, sans coupe spectrale ajoutee. Relaxations lineaires faisables.
Ce sont deux verdicts solveur locaux, pas une preuve de(A).

PROUVE analytiquement, independamment de ces calculs : pour tout SRG(v,k,1,mu)
avec mu>0 paire, A^2=A sur F2 et C=im(A)=Fix(A). Si un mot non nul a poids w,
e aretes internes et d_x voisins dans son support, d_x est impair dedans,
pair dehors. Donc w est pair, 2e>=w et
  (k-1)w <= somme d_x(d_x-1)
          = mu*w*(w-1)-2*(mu-1)*e
          <= mu*w*(w-1)-(mu-1)*w.
Ainsi w>=2+(k-2)/mu, arrondi au prochain entier pair. Conway : poids>=8 ;
parametres243,22,1,2 : poids>=12, sans recalcul d'aucun graphe du pair.
Au poids8 pour Conway, l'egalite force quatre aretes disjointes dans le
support ; dehors52 sommets ont deux voisins et39 aucun.

Sur nos34 labels (trois etoiles), le poids8 est impossible : chaque centre,
exterieur au support, aurait au plus deux voisins dans celui-ci ; trois
centres couvrant huit labels demanderaient au moins huit incidences, pas six.
Le poids minimal d'un mot NON NUL de C supporte sur ces labels est donc>=10.

Application nouvelle aux noyaux : sur TOUS les84 labels,
  (Kq)_p = r*|p cap l| + |p cap M| - r,
ou M contient2r lettres. Ceci est entier ; Dq est pair. Si Du=0 et
z=2q+u, alors Dz et Kz=2Kq sont pairs. Une relation Tz=0 dans un Conway
donne donc A(z mod2)=z mod2, apres prolongement par zero sur le repere.
Un noyau local d'un bloc PSD se propage au T global de toute completion.
On peut ainsi rejeter AVANT la recherche toute relation de cette famille
avec2,4,6 ou8 coefficients impairs sur nos34 labels. En particulier tous
les reflets d'incidence4cycle deplacant q avec q.u impair sont globalement
exclus, meme si un bord PSD local existait. Ce n'est PAS une exclusion de
tous les changements de noyau, de tous les rangs30, ni de l'asymetrie.

Preuve : prescribed_kernel_728/binary_obstruction.json. Controle de notre
formule Kq sur les63 sous-ensembles non vides de six paires, avec les84
labels complets ; aucun calcul sur une matrice du pair. Transmis729.

Quatre essais suivants a poids impair10 : u est la somme d'un4cycle et
d'un6cycle. Deux ont une entree negative sur X et deux evitent cela.
Tous echouent deja lineairement. Pour CHACUN, extraction d'un certificat
EXACT de Farkas, puis verification rationnelle :15,18,24,22 inegalites,
coefficients entiers non negatifs, somme des coefficients de chaque arete
nulle, second membre-1. Ils n'utilisent QUE les relations de noyau et les
bornes0<=Gamma_ij<=1, ni plafonds ni coupes PSD. Les JSON *_linear_certificate
contiennent tous les multiplicateurs et les lignes. Ces quatre relations
particulieres sont donc PROUVEES impossibles meme fractionnairement.

Le filtre binary_obstruction du nouveau moteur calcule Dz et Kz sur les84
labels ; il distingue explicitement une impossibilite de completion d'une
impossibilite PSD locale. Les six essais sont termines, sans processus en
arriere-plan. Aucun contre-exemple a(A), aucune preuve de(A),(B),(C), aucun
SRG asymetrique construit. L'apport est un obstacle structurel de parite
aux constructions de noyaux, et non une nouvelle borne sur le nombre
d'automorphismes.

Suite bornee : avec le meme u de poids10, une exploration des choix de M
s'arrete au PREMIER choix fractionnairement faisable, M={paire1} (celle
contenant b), apres0,031s. Ce n'est pas une enumeration des62 choix : un
seul a ete essaye. Le modele binaire correspondant donne ensuite UNSAT
en0,516s, sans coupe PSD ajoutee. Fichiers weight10_component_scan.json
et r1_b_w10.json. Sept relations au total testees, toujours aucune preuve
generale de(A). Pas de nouvelle campagne lancee apres ce verdict.

### Message731 et construction avec coefficients libres

Message731 lu et acquitte. Resultats du pair ACCEPTES, sans re-audit :
code im_F2(A) de dimension54, intersection triviale avec son dual, code
dual de poids minimal>=8 ; formulation spectrale de T/U par le graphe
induit49 et multiplicites3/-4 ; une grille est un code parfait, avec neuf
fibres exterieures de dix sommets. Provenance et enonces precis dans
variable_kernel_731/peer731_results.json. Claude poursuit(B) ; je poursuis(A).

NOUVEAU moteur three_star_variable_kernel.py : z=2q+u, TOUS les coefficients
u dans{-1,0,1} sont variables, avec Du=0. On impose Q connexe par ses31
coupures, et une queue non constante sur la troisieme etoile. Cette derniere
condition assure une quatrieme relation independante des trois etoiles.
Le q de reference n'est PAS impose dans le noyau, ni sa composante dans
Gamma. Aucun graphe du pair en entree. Deux essais40s(M={2,3} et{2,3,4})
donnent UNKNOWN, aucun candidat local ; aucune exclusion.

PROUVE : forme normale de cette famille ternaire. Pour chaque lettre
x=4..13, (u0x,u1x,u2x) est nul ou une permutation de(1,-1,0), soit sept
etats. Les recouvrements verifient u02=-u12=a, u03=-u13=c ; les dix triples
somment a(-a-c,a+c,0). Echanger0/1 normalise a>0 ou a=0,c>=0, puis on
trie les etats dans chaque paire de lettres et les paires dans M/horsM.
Ces symetries sont compatibles et preservent q. Deux nouveaux essais40s
avec cette forme restent UNKNOWN. Pas d'inference d'impossibilite.

Enumeration COMPLETE des coefficients dans cette famille, par
three_star_ternary_kernel_templates.py :194336 formes normalisees pour
chacune des deux partitions. Il peut subsister des repetitions ; ce ne
sont pas194336 classes d'isomorphisme prouvees. Les tailles d'orbites sous
les flips et permutations de paires somment a38673438 vecteurs etiquetes
avec(a,c) normalises, egalement obtenus par un DP sur dix etats ordonnes.
Controle de couverture propre, pas de verification d'un graphe du pair.

Filtre entier necessaire par ligne : les quatre choix d'adjacence vers
les deux recouvrements fixent les comptes dans les trois groupes exclusifs.
Le poids de voisinage requis doit se trouver entre la somme des k plus
petits et celle des k plus grands coefficients. Il reste118848 et104528
vecteurs, en3,64s et3,52s respectivement. Aucun de ces vecteurs n'est un
graphe construit. Les survivants sont stockes en NPZ. Sur un PREFIXE
limite aux poids>=10 (choix de recherche, pas exclusion locale), le premier
LP compatible avec Qconnexe est obtenu apres5 et25 essais ; ces deux
relations fixees sont ensuite UNSAT binaires en0,610s et0,469s. Aucune
coupe PSD n'a ete ajoutee, faute de candidat local. L'assertion(A) reste
ouverte, la famille ternaire entiere n'est pas exclue.

### Nouveau lemme de couverture des supports binaires

PROUVE pour TOUT SRG(v,k,1,2). Si X est le support d'un mot non nul de
C=im_F2(A), w=|X|, d_y=|N(y) cap X|, alors
  somme_horsX d(d-2) + somme_dansX d(d-1) = w*(2w-k-2).
Preuve : soustraire somme_horsX d = kw-2e(X) du compte exact
somme d(d-1)=2w(w-1)-2e(X). Tous les termes affiches sont non negatifs
par parite (d impair dans X, pair dehors).

Si X est couvert par h voisinages dont les centres sont HORS de X,
leurs degres somment a t>=w. Cauchy donne une contribution>=t^2/h-2t,
donc>=w^2/h-2w lorsque w>=h. On obtient
                     w >= h*k/(2h-1), arrondi pair.
Si w<h, cette borne decoule deja de w>=(k+2)/2. Version discrete :
w=2h*a+2b,0<=b<h, contribution des centres>=4h*a*(a-1)+8a*b.
Pour UN voisinage, w>=k : le seul mot non nul contenu dans N(v) est N(v)
lui-meme. Pour trois voisinages, poids>=10 Conway,>=14 aux parametres243.
Cela compare les parametres sans recalculer aucun des graphes connus.

PROUVE, Conway au poids10 dans trois voisinages : RHS40, contribution
des centres>=16 ; somme interne<=24 et divisible8. Les degres impairs
1,3,5,7 coutent0,6,20,42. Donc soit les dix degres internes valent1,
soit quatre valent3 et six valent1. Dans le second cas, les trois centres
ont degres(4,4,2) et tous les autres sommets exterieurs ont0 ou2 voisins.
Les quatre sommets de degre3 induisent3 ou4 aretes (5/6 violeraient lambda1).
Leur graphe est P4, K1,3, K3+isole, C4 ou paw ; les feuilles et l'eventuelle
arete entre sommets de degre1 sont ensuite forcees. Avec le couplage5K2,
cela donne SIX formes abstraites possibles, sans affirmer leur realisation.
Enumeration propre des64 graphes sur les quatre sommets de degre3 : cinq
formes non isomorphes et les plafonds internes verifient cette description.

PROUVE aux parametres243,22,1,2 au poids14 : RHS56, contribution des trois
centres>=40, somme interne<=16 et divisible8 ; les seuls degres possibles
sont tous1. Le support est donc obligatoirement7K2. Pour le code dual de
Conway, le resultat du pair implique aussi qu'un mot de poids8 serait une
coclique avec tous les degres exterieurs0/2 : impossible sur trois etoiles,
d'ou poids>=9 sur les labels lointains, sans supposer les poids duaux pairs.

Preuve principale neighbourhood_cover_bound.json ; exemples abstraits et
table de bornes cover_bound_checks.json. Ce sont des restrictions globales
de completion, pas une preuve de(A) ni de l'existence d'automorphismes.
Tous les pilotes sont termines ; aucun processus de recherche en cours.

### Message733 : relations non binaires et poids positif minimal

Message733 lu et acquitte. Classification binaire et congruences du pair
ACCEPTEES sans re-audit, dans nonnegative_kernel_733/peer733_results.json.
Avec Q connexe, les seuls vecteurs binaires de kerT sont0,L0,L1,L0+L1,L2.
Pour q entier, w=sommeq est divisible4 ; d_i=d_mate modulo4 et tous les
t_i=3d_i+d_mate ont le meme residu modulo8, necessairement0 ou4.

NOUVELLE forme de recherche : toute relation supplementaire rationnelle
peut etre rendue entiere, puis positive ou nulle en ajoutant les etoiles.
Soustraire une etoile des que toutes ses coordonnees sont positives finit
avec au moins un zero dans chaque etoile (w decroit de12). La relation
reste supplementaire. Sa queue de dix coefficients doit etre non constante,
sinon soustraire L2 la ramene au noyau connu des deux premieres etoiles.
Son maximum est>=2 par733. Aucune borne universelle de hauteur annoncee.

PROUVE ANALYTIQUEMENT : une telle relation non negative a w>=12.
On utilise d_i+d_mate<=w et d0+d1+d2=w+q02+q12. Les congruences eliminent
w4. A w8, les profils de degres equilibres et le residu4 sont impossibles.
Il ne reste, a symetrie pres, que d0,d1,d2,d3=(1,5,5,1), une paire
exterieure(a,a') de degres(2,2), et les autres degres0. Les lignes a zero
forcent q02=1,q12=2,q13=1,q1a=q1a'=q2a=q2a'=1. La ligne12 demande alors
un poids voisin4, mais les comptes vers L1 et L2 l'autorisent au plus2.
Preuve detaillee : normalization_and_weight_bound.json. L'enumeration
entiere<=8 retrouve un seul profil normalise, exclu par cette ligne.

NOUVELLE EXCLUSION FINIE : w12 est aussi impossible. Enumeration COMPLETE
en0,738s des coefficients0..12 satisfaisant la normalisation et les
congruences :19 profils normalises (pas un compte affirme de classes
d'isomorphisme). Les domaines exacts de chaque ligne en excluent17.
Les profils10 et12 restants sont impossibles meme fractionnairement :
certificats exacts de Farkas de46 et50 termes, seconds membres-4 et-8,
avec uniquement equations de noyau et positivite des aretes. Ils n'utilisent
ni Q connexe, ni les plafonds de voisins communs, ni PSD. Tous les
coefficients sont annules exactement par les multiplicateurs entiers.
Donc une relation supplementaire normalisee doit avoir w>=16.
La couverture des19 profils repose sur l'enumeration entiere terminee ;
ce n'est pas encore une classification analytique du cas w12.

Moteur three_star_nonnegative_kernel.py : tous les coefficients0..H sont
libres, sans q de reference ni contrainte Du=0. Symetries de la paire0/1
et des cinq paires exterieures, equations de noyau, congruences, Q connexe,
plafonds locaux puis coupes spectrales exactes. Premier essai H2,40s :
deux nouveaux candidats locaux de poids24 ; tous deux T non PSD, six
coupes exactes ajoutees. Timeout ensuite : aucune exclusion de H2,
aucun bord PSD construit, aucune preuve de(A).

Essai exploratoire w16,20s :437 profils,149 survivants des domaines de
lignes, enumeration INCOMPLETE. Aucun verdict d'exclusion sur w16.
Filtre supplementaire prouve : T_ii=20/8 et T_ij>=-10/8 donnent
3*q_i<=w pour toute relation non negative. La hauteur necessaire pour
un poids fixe16 est donc au plus5, ce qui facilite une enumeration ciblee.

Suite : le pilote CP avec hauteur5 reste incomplet apres40s (803 profils,
226 survivants). Remplace par une enumeration COMBINATOIRE directe :
triples de coefficients sur chaque lettre exterieure, paires de triples
compatibles avec le residu0/4, multisets de cinq paires, puis les quatre
coefficients de recouvrement. La borne3q_i<=w fixe la hauteur. La preuve
de couverture est le tri des flips/permutations ; pas de solveur general
pour cette enumeration. w12 :19 profils en0,078s, ce qui fournit aussi
une couverture directe du resultat precedent. w16 :1420 profils COMPLETS
en2,641s, dont993 exclus par le domaine exact d'une seule ligne.

Les427 survivants w16 passent tous au filtre lineaire en17,735s :151
contradictions EXACTES de Farkas,276 faisables fractionnairement. Les
certificats compacts citent les lignes originales, sont re-deployes et
additionnes en entiers avant sauvegarde.80 n'utilisent que noyau et
bornes d'aretes ;71 utilisent aussi les plafonds aux lettres. Aucun
n'utilise une coupe spectrale. Total1144/1420 profils exclus exactement.
Ce n'est PAS une preuve d'exclusion du poids16.

Un modele unique autorise les276 profils restants et reutilise les six
coupes spectrales du pilote H2. En40,031s :quatre nouveaux candidats
locaux de poids16, tous T indefini, six nouvelles coupes exactes. Timeout
ensuite ; aucun bord PSD produit, aucune exclusion de la famille276.
Les calculs sont termines, aucun processus de recherche en cours.

Corollaire net de la borne precedente : pour Q connexe et T PSD, les
vecteurs entiers non negatifs de kerT de somme<=12 sont exactement0 et
les trois etoiles individuelles. Les coefficients d'un vecteur entier
dans leur span se lisent sur les groupes exclusifs, donc sont entiers ;
la non-negativite les rend non negatifs et leur somme vaut w/12. Une
quatrieme relation normalisee commence donc au poids16. Cela explique
une obstruction aux relations courtes, sans prouver le rang31 general.

Message735 observe dans le saut de sequence avant notre envoi736, puis
lu et acquitte. Claude a construit un exemple Q connexe, nullite exacte4,
T indefini, avec une symetrie h; resultat accepte sans audit. Reponse :
nos six candidats locaux imposent aussi Q connexe par31 coupures et ont
nullite>=4 par les relations construites. Ils montrent deja que(A) SANS
positivite est faux. Aucune nullite exacte supplementaire annoncee pour
nos candidats. La positivite est donc indispensable a toute preuve de(A),
qui reste ouvert. Claude poursuit ses constructions avec symetries.

### Message738 : symetrie h3 et separation des contraintes de positivite/C2

Message738 lu et acquitte. Resultats/echantillons du pair acceptes sans
re-audit. Sur NOS objets : les deux matrices finales sauvegardees ne sont
pas h3-invariantes (110 et118 entrees d'aretes changent). Les six relations
ne sont ni paires ni impaires modulo le span des trois etoiles, et leurs
supports ne sont pas h3-invariants. Seule la premiere queue de poids24
est constante dans les paires. Les quatre matrices intermediaires n'ont
pas ete conservees : pas d'affirmation sur leur groupe. Reponse739.

Nouvelle piste propre : coupes PSD sur les profils de coefficients, via
LP continu. Toute direction ENTIERE donne une inegalite PSD valide, meme
si elle a ete proposee par une valeur propre numerique. Seules des
combinaisons de Farkas a cancellation entiere comptent comme exclusions.
Premier pilote12 profils/12 iterations : aucune exclusion. Un suivi80
iterations du profil31 n'exclut rien non plus. Ces limites ne prouvent
aucune faisabilite. Scripts three_star_psd_profile_cuts.py et variantes.

Recherche d'une marge positive sur les quotients principaux : on retire
quatre ancres independantes des relations de T et trois de U. Le noyau
force permet une congruence, donc la positivite du quotient suffit.
Le pilote a necessite de cacher la marge avant d'ajouter une coupe au
modele GLOP : lire solution_value apres mutation invalide la lecture.
Corrige dans le code avant les pilotes avec coupes C2. Les anciennes
coupes restent des inegalites PSD valides ; aucun verdict ne repose sur
une marge numerique. Le point retenu est ensuite certifie en rationnels.

CONSTRUCTION RATIONNELLE EXACTE, profil31 : Gamma a denominateur commun
29664,115 aretes strictement fractionnaires. Les659 equations/inegalites
lineaires (noyau, plafonds aux lettres, orientations, connexite Q) passent
exactement. Les quotients de8T et15U ont tous leurs pivots rationnels
strictement positifs ; les noyaux forces donnent rang(T)=30, rang(U)=31.
Mais22 plafonds de voisins communs lointains(C2) sont violes, dont15 deja
dans leur relaxation McCormick. Ce n'est PAS un graphe ni un contre-exemple
a(A). Cela localise une faiblesse du seul LP+PSD. Certificat/matrice dans
profile31_fractional_certificate_738.json.

Coupes C2 valides : pour tout couple i,j et tout ensemble K de sommets
intermediaires, Gamma_ij+somme_K(Gamma_ik+Gamma_jk)
  <=2-|label_i intersection label_j|+|K|.
Preuve : ab>=a+b-1 pour0<=a,b<=1, puis plafond de voisins communs.
Elles se separent en prenant K={k:Gamma_ik+Gamma_jk>1} au point LP.
Le profil45 est exclu exactement par ces coupes ; son certificat
individuel utilise deux coupes C2, aucune coupe PSD.

FAMILLE TERMINEE : poids16, une seule paire exterieure active dans le
support (au plus dix labels sur0,1,2,3,a,a').52 profils dans la liste
complete1420 ;47 deja exclus, il restait31,42,44,45,46. Nouveau scan C2
des cinq :42,44,45 ont des contradictions de Farkas exactes(-2,-1,-2),
utilisant noyau, plafonds aux lettres, C2 et bornes d'aretes, sans PSD.
Les31 et46 atteignent la limite des coupes LP, puis sont UNSAT binaires
au presolve (zero branche). On retire ensuite TOUTES les coupes initiales
d'orientation PSD pour distinguer le mecanisme : toujours UNSAT,
0,122s et0,174s de solveur, aucun test spectral demande. Ce sont deux
verdicts UNSAT finis ; pas de trace de preuve SAT portable annoncee.

Ainsi une relation supplementaire normalisee de poids16 doit toucher
au moins DEUX paires exterieures. Total1149/1420 profils exclus,271 restent
(97 sur deux paires,146 sur trois,28 sur cinq). La masse minimale16 ne
monte pas a20. Aucune conclusion sur les automorphismes complets, aucun
SRG asymetrique construit, (A) ouvert. Tous les calculs pilotes termines.

### Messages741/743 : (A) FAUX ; passage a la compatibilite de quatre etoiles

Les resultats du producteur Claude LAB sont ACCEPTES SANS RE-AUDIT.
Le germe counterexample_A_1.json a34 labels, Gamma binaire admissible,
Q connexe, T et U PSD, rang(T)=30 et rang(U)=31, certifies exactement
par Claude. Cela REFUTE(A), qui annoncait rang31 pour tous ces objets.
Arret de la recherche d'une preuve de(A). Les restrictions anterieures
sur les relations nonnegatives (poids>=16, poids16 sur au moins deux
paires exterieures) restent des conditions necessaires, pas une exclusion
de tous les germes de rang30.

Message743 : CE GERME NE SE PROLONGE PAS EN CONWAY. Pour le label{4,6},
Claude obtient5335 profils localement admissibles et ZERO de norme20.
Ce resultat est repris tel quel, sans refaire les domaines. Les51 autres
structures de son export sont seulement numeriquement PSD a ce stade :
ne pas leur attribuer la certification exacte du premier germe.

Notre piste distincte : JOINDRE les dix colonnes(3,x), x=4..13, en une
quatrieme etoile. Claude poursuit ses domaines individuels et ses
constructions directes de quatre etoiles. Si H4' (aucune extension avec
deux Q connexes, les deux PSD et rangT<=30) etait etabli universellement,
un sommet aurait au plus une droite non speciale. H4' reste OUVERT.

REDUCTION EXACTE DU JOIN, pour un germe de rang30 deja certifie :
M=8T, I base principale30, H=M_II^{-1}. A un profil h_u correspond
m_u=-8h_u-K8(S,u), avec m_u[I]^T H m_u[I]=20 et les relations du noyau.
La seule entree nouvelle possible est M_uv=m_u[I]^T H m_v[I] ; donc
Gamma_uv=(-K8(u,v)-M_uv)/8 doit valoir0 ou1. Toutes les nouvelles aretes
sont ainsi determinees par les dix choix de colonnes.

Noter a=(0,3), b=(1,3). Les34 budgets exacts de l'etoile L3 sont
somme_x h_(3,x)[i]=2-1_(3 dans i)-1_(2 dans i)-Gamma_ia-Gamma_ib.
L3 doit induire un couplage parfait. On impose ensemble toutes les
capacites des49 anciens sommets, via R=12I+2J-B-B^2 et les contributions
d_u d_u^t des dix nouveaux voisins. Pour deux nouveaux sommets, le
couplage interdit un voisin commun parmi les dix nouveaux : leur plafond
se lit exactement dans d_u.d_v<=2-Gamma_uv. Pour un couple ancien/nouveau,
un nouveau voisin eventuel ajoute uniquement le profil de son partenaire
de couplage ; ceci se filtre dans les tables de compatibilite. Ces
contraintes couvrent donc tous les plafonds locaux du bord59 assemble.

REDUCTION COMPLEMENTAIRE : N=15U, et rang(U_S)=31 certifie par le
producteur. Retirer trois pivots independants des trois relations
d'etoile donne une base principale J. Son inverse sert au prolongement,
sans refaire un calcul de rang ni un certificat PSD sur le germe.
W=N_BB-N_BJ N_JJ^{-1} N_JB est de taille10. Les equations d'etoile
imposent W*1=0 ; N>=0 equivaut donc a la positivite d'un principal9x9
de W, puisque le bloc ancien est PSD et les colonnes orthogonales a son
noyau. Avant le join, les inegalites W_uv^2<=W_uu W_vv sont des filtres
exacts de COUPLES, plus forts que la positivite individuelle des colonnes.
Ici N_uu=50, N_uv=15Gamma_uv-6+1_(x,y mates) pouru=(3,x),v=(3,y).

Implementation four_star_profile_join.py : tables de Gram exactes,
capacites communes, budgets d'etoile, couplage, option Q2 connexe par31
coupes, filtre des mineurs de Schur et quotient9x9, coupes PSD entieres
sur toute extension proposee. Les depassements de temps/taille ne sont
jamais des exclusions. Un UNSAT serait limite au germe fourni et au
type de seconde droite demande. Les grands temoins PSD utilisent un
nogood exact pour eviter un debordement int64 dans CP-SAT.

Controles de NOS primitives de Gram, capacites conjointes et mineurs
de Schur : PASS. Aucun essai complet sur un germe survivant pour
l'instant ; celui de741 est deja tue par la colonne du pair. Aucune
nouvelle exclusion H4', aucun graphe Conway/C1 construit ou exclu,
aucune enumeration globale abordable demontree. Messages742 et744
transmettent la division du travail et cette reduction. Artifacts :
data/codex_three_star_completion_20261014/four_star_join_741/.

### Messages745/746 : lot52 epuise, couplage exact et100 coupes strictes

745 et746 lus/acquittes ; aucun re-audit des objets certifies du pair.
Nouveau resultat de Claude : un bord44 localement admissible avec T/U
PSD existe, rangT34, rangU40, c(l)=3 et c(m)=4. L'impossibilite de toute
positivite sur quatre etoiles est donc FAUSSE. Ce rang34 ne convient pas
a Conway. H4' (deux Q connexes et rangT<=30) reste ouvert. La proposition
(A4), positivite forcant les deux droites speciales, est une CONJECTURE
du pair ; on ne l'impose pas comme contrainte demontree.

Claude laisse a Codex les51 autres germes de counterexamples_A_all.json.
Test NOUVEAU de leur prolongement : elimination rationnelle pour les
bases de colonnes, aucune certification PSD repetee. Index38 saute car
deja exclu par Claude. Les51 autres bases ont dimension30. Pour{4,6},
410745 profils satisfont les equations du noyau ;5771 satisfont aussi
les capacites de l'ancien bord. Parmi ces derniers,303 ont une norme
strictement inferieure a20,5468 une norme strictement superieure, ZERO
la norme20 requise par le prolongement de rang30. Domaines tous complets,
2,844s au total. Les51 sont exclus, donc les52 entrees fournies sont
non prolongeables avec le resultat du pair. Pas d'hypothese de symetrie
sur la completion, pas de classification de toute la famille h3.
Code three_star_extension_batch.py ; donnees lab745_extension_batch/.

NOUVEAU THEOREME DE COUPLAGE. Reprise de l'identite exterieure de745,
sans la re-auditer. Pour q=D_ext^t z avec z entier mate-symetrique de
somme0, Tq=q-Gamma q. Pour z mate-antisymetrique, Tq=2q-Gamma q.
Ecrire alpha=1 ou2, h=(alpha||q||^2-q^tGamma q)/2, entier,
et s_i=alpha q_i-(Gamma q)_i, entier. Comme T_ii=5/2, le mineur PSD
sur(q,e_i) impose5h>=s_i^2. A saturation h=0, Gamma q=alpha q est
donc FORCE. Sinon w=2q-sign(s_i)e_i donne exactement
w^t(8T)w=20-32|s_i|<=-12 : petit temoin entier, sans vecteur propre
numerique de la matrice fine.

Pour tout entier t, s_i^2>=(2t+1)s_i-t(t+1) sur les ENTIERS. D'ou
la coupe LINEAIRE 5h>=(2t+1)s_i-t(t+1), valable sur Gamma binaire.
Au point entier courant, choisir t=s_i separe toute violation du mineur.
Attention : Gamma q=alpha q est CONDITIONNEL a h=0 ; les coupes entieres
ne sont pas annoncees valides pour une matrice fractionnaire quelconque.
Implementation four_star_coupling_cuts.py, directions courtes25 sym et
121 anti, plus noyaux exacts des compressions4x4/5x5. Notre fixture
algebrique (pas un germe admissible) donne le temoin exact-12.

NOUVEAU THEOREME DE POSITIVITE STRICTE. N=15U satisfait Nq=48q+15Gamma q
dans le secteur symetrique de somme0, et Nq=40q+15Gamma q dans le secteur
antisymetrique. Si U est PSD et q non nul de valeur quadratique nulle,
Nq=0 donnerait une valeur propre de Gamma egale a-16/5 ou-8/3.
Impossible : une valeur propre rationnelle d'une matrice ENTIERE est
entiere. Les DEUX compressions de U sur ces secteurs sont donc DEFINIES
POSITIVES (separement ; pas d'affirmation sur tous leurs melanges).
Cette preuve vaut pour tout q reel du secteur, pas seulement les courts.

100 RENFORCEMENTS LINEAIRES explicites :
-40 directions anti, trois coefficients non nuls dans{+-1} sur cinq
paires, modulo signe global : ||q||^2=24, q^tNq=960+30E(q), ou
E(q)=somme_{i<j}q_i q_j Gamma_ij. La positivite stricte et l'integralite
donnent E(q)>=-31 ; la seule inegalite PSD donnait>=-32.
-60 directions sym, permutations de(2,1,0,-1,-2) modulo signe global :
||q||^2=80, q^tNq=3840+30E(q), donc E(q)>=-127 au lieu de>=-128.
Generateur strict_upper_cuts(), export disponible. Valides sans groupe
suppose ni connexite Q imposee. Pas de gain de temps solveur mesure.

Controles exacts de nos identites, comptes25/121 et40/60, ainsi que du
temoin de saturation : PASS. Transmissions747,748,749 au pair. Donnees
four_star_coupling_745/. Pas de germe survivant a joindre dans le lot,
aucun graphe SRG asymetrique nouveau, aucun Conway/C1 exclu. Les100
coupes sont un renforcement demontre des contraintes, pas une preuve
qu'elles terminent le solveur.
Export portable des100 lignes, avec l'ordre des44 labels :
../lab_exchange_2026-10-14/four_star_strict_upper_100.json (451123 octets).

Message750 lu/acquitte apres un saut de sequence, sans sondage vide.
Claude annonce487 structures PSD dans ses recherches G1, toutes avec
les deux c>=3, et signale lui-meme un biais de cette famille preservant
les droites. Ces comptes sont des OBSERVATIONS, pas une preuve de(A4),
ni une nouvelle certification exacte des487 matrices. Il lance le test
conjoint PSD+nullite>=14. Aucun de ces calculs ne tourne cote Codex.
Le message751 donne l'export concret des100 coupes ; aucune reponse
d'accuse de reception au commentaire du pair sur notre theoreme.

### Messages752/754 : domaines44->45 et contraintes par caracteres de G1

Resultats du pair acceptes sans re-audit : meilleurs bords quatre etoiles
PSD annonces de nullite12/rang32. Un objet de nullite13 existe mais n'est
PAS PSD. Aucun germe PSD de rangT<=30 disponible. Les futurs certificats
du pair fourniront une base principale T et le rang de U pour nos domaines.

Moteur four_star_column_domains.py, 44 anciens labels et40 manquants :
les quatre labels de recouvrement sont02,03,12,13. Chacun de leurs16
masques impose, dans chaque bloc de dix labels ax, exactement2-deg(a)
voisins. Total brut4 949 026 profils par label manquant. En groupant les
centres(0,1) et(2,3), deux tables de4356 entrees suffisent pour joindre
les equations de noyau ; elles sont reutilisees sur les40 labels.
ATTENTION :8712 est le nombre d'entrees, PAS le cout total du domaine.
Il reste a parcourir les correspondances, en nombre dependant du germe,
puis les capacites et les normes. Pas d'enumeration globale abordable
des germes demontree. Budgets de temps, aucun timeout pris pour exclusion.

La base principale certifiee permet de calculer l'inverse et les relations
necessaires aux colonnes, sans refaire rang/PSD du germe. Si rangT30,
m=-8h-K8(S,u) doit satisfaire m_I^t(8T_II)^{-1}m_I=20. Si rangT<30,
seule l'inegalite<=20 est imposee. Si le pair certifie AUSSI rangU40,
le rang ambiant complementaire est deja atteint : n=15h-4intersection+
mate-2 doit satisfaire n_J^t(15U_JJ)^{-1}n_J=50. Cette seconde egalite
ne doit pas etre imposee si rangU<40. Les quatre relations d'etoile
permettent de choisir le principal40 de U sans calculer son rang.

Controles propres :4356+4356 entrees,4 949 026 profils bruts,221801 avec
le bit02 force, et les deux polynomes quadratiques exacts : PASS.
Aucune application a un germe rang30, puisqu'il n'y en a pas encore.
Le vieux join34->44 n'est pas applique tel quel a un objet44.

NOUVEAU THEOREME POUR G1 : les44 labels sont11 orbites regulieres du
groupe de Klein. Les quatre caracteres ont donc chacun dimension11.
Les etoiles donnent des nullites(2,1,1,0) dans(++,-+,+-,--).
Pour une droite de composantes c, ses24 labels forment6 orbites regulieres.
Le noyau deux-etoiles connu a dimension c+1 ; ses c relations invariantes
viennent des composantes Q, tandis que la difference des deux etoiles
est dans un caractere non trivial. Son bloc trivial6x6 a rang6-c.
Le bloc trivial11x11 global contient les deux principaux correspondants,
donc rang_trivial>=6-min(c_l,c_m). Par suite, rangT<=30 impose
nullite_nontriviale>=9-min(c_l,c_m).

Pour c=(4,4), il faut au moins5 dimensions de noyau non triviales,
dont deux differences d'etoiles deja connues : AU TOTAL trois autres
relations non triviales, en comptant celles deja trouvees. Sous l'absence
de C4 mentionnee par le pair, parmi les quatre relations mixtes necessaires,
au moins trois doivent etre non triviales. Le secteur trivial, de rang>=2,
ne fournit qu'une relation de plus que les huit locales.
Couverture par10 cibles minimales de nullite(-+,+-,--)=(1+a,1+b,c),
a+b+c=3 ; ces cibles peuvent se recouvrir et ne suffisent pas a certifier
le rang ou la positivite. Elles orientent les recherches du pair.

Code four_star_g1_sectors.py : bases B_chi44x11 explicites, B_chi^t B_chi=4I,
blocs B_chi^t T B_chi/4 et dix cibles. Action du groupe, dimensions,
orthogonalite et types des etoiles controles sans lire de graphe : PASS.
Restriction a la famille LOCALE G1 ; aucune symetrie du graphe complet
n'est supposee. Transmissions753/755. Donnees four_star_columns_752/.
Aucun calcul local restant, aucun Conway/C1 exclu, aucune construction SRG.

### Messages756-762 : quotient c55 et catalogue exact de deux secteurs

756/757 lus/acquittes. Claude donne les nullites(9,1,1,1) de son meilleur
bord PSD c44 et reprend ses recherches par caracteres. Le germe null13
n'etait pas exporte au debut de ce tour ; aucun audit entrepris. Message758 :
rappeler que c55 donne SIX cibles minimales, et qu'une nullite totale13
reste un rang31 meme si un seuil non trivial est satisfait. Demande d'export.
759 (lu lors du saut de sequence760) fournit lui-meme la nouvelle analyse :
null13=(10,1,1,1), non PSD ; sc_7_null14=(10,1,1,2), T PSD rang30,
mais U negatif dans10/01. Ces certifications sont acceptees sans re-audit.

LEMME C55 NON GRILLE. Les11 orbites regulieres sont O (recouvrement),
L_i et R_i, i=0..4. Soit D_ij la valence de l'orbite i vers j et H le
bloc trivial de T, dans la base des indicatrices d'orbites divisees par2.
H_ii=2-D_ii. Hors diagonale : -D_ij sur chaque droite et vers O ;
H_Li,Rj=1-[i=j]-D_Li,Rj. Identite issue directement de K8, controlee.
Dans chaque droite, c=5 signifie une composante de taille2 et quatre
singletons. Si O n'est pas une grille, les deux paires actives sont
{O,L_p}, {O,R_q}, de meme poids t=2-D_OO dans{1,2}. Les huit autres
diagonales nulles imposent leurs lignes nulles par positivite. Le coeur
est [[t,-t,-t],[-t,t,e],[-t,e,t]], determinant -t(e-t)^2. Donc e=t.
Comme e<=1-[p=q], on obtient t=1, p!=q et D_Lp,Rq=0. Ainsi H=ww^t,
w=e_O-e_Lp-e_Rq, rang1/nullite10. Les20 choix(p,q) sont equivalents
par renommage des paires exterieures : fixer p=0,q=1 est complet ici.
Le recouvrement grille est explicitement HORS de cette reduction.

Construction propre par CP-SAT du quotient normalise : variables de
couplages G1, equations des quatre etoiles completes, capacites de voisins
communs. Premier bord59 en0.95s ; controles directs de son residual,
des cinq lignes completes et du quotient : PASS. Il n'est pas T/U PSD.
Un essai borne de30 candidats,101 coupes PSD rationnelles exactes,
27.44s, reste UNKNOWN (limite de30 tours atteinte). Tous echouent en T11 :
observation seulement, contredite comme enonce universel par sc_7_null14.
Transmission760 du lemme et des exports, sans nouvelle exclusion.

CATALOGUE EXACT DES SECTEURS10/01. Pour10, ordonner les coordonnees
gauche O,L0,...,L4 puis droite R0,...,R4. e=1 sur les six gauches,
v=e_O-e_L0. La matrice U vaut
 [4I+s vv^t-(2/3)ee^t, B^t ; B, diag(2,4+d,2,2,2)],
et T vaut
 [3I-s vv^t-(1/2)ee^t, -B^t ; -B, diag(5,3-d,5,5,5)],
avec s,d dans{+-1}. Chaque ligne de B a quatre signes, deux+ et deux-,
sur un support impose. La ligne1 porte O et L2,L3,L4 ; les autres
portent les quatre L_i avec i different de l'indice de ligne. Modulo
son signe global, chaque ligne a3 partitions. Les inversions de lignes
sont des congruences simultanees, donc les4*3^5=972 cas couvrent tout.

Eliminer le bloc droit positif et enlever la coordonnee O (e est dans
le noyau). Les Schur5x5, multiplies par6(4+d) pour U et10(3-d) pour T,
sont ENTIERS. Catalogue complet par pivots rationnels/temoins entiers :
 (s,d)    U PSD      T ET U PSD
 (-1,-1)   18/243      18/243
 (-1,+1)   18/243      18/243
 (+1,-1)   72/243      72/243
 (+1,+1)   72/243      18/243
Total180 U,126 conjoints. Dans les126 cas conjoints, les DEUX Schur
sont definis positifs de rang5. Donc T10,U10 ont rang10, une seule
relation d'etoile. Meme resultat en01, en echangeant les deux droites
et les indices exterieurs0/1. Le secteur trivial est fixe : T rang1,
U rang9, PSD (calcul exact de la matrice constante, pas d'audit de germe).

CONSEQUENCE LOCALE PROUVEE : tout objet de cette sous-famille avec T/U
PSD a les nullitesT=(10,1,1,k). RangT<=30 force k>=2 EN11. Les autres
cibles ajoutant une relation en10 ou01 sont impossibles ici. Ce n'est
pas un theoreme imposant G1 ou c55 a un Conway eventuel.

La table126 est integree deux fois au CP-SAT, avec les MEMES variables
de couplage, dix variables de partitions ternaires. Controles propres :
correction K/upper par caracteres, singleton=grille via capacites locales,
972 cas exacts, canalisation des deux tables sur un bord construit : PASS.
Code four_star_g1_c55.py / four_star_g1_c55_upper.py ; artefacts
four_star_g1_c55_756/. Le catalogue contient rangs et temoins negatifs.

Construction intermediaire avec les tablesU : bord59 local valide,
U entierement PSD, T PSD en00/10/01 et negatif en11. Il montre que les
quatre grilles par droite ne forcent pas a elles seules U negatif.
La positivite SIMULTANEE de T reste essentielle. Export portable
codex_c55_Upsd_T11negative.json. Avec tablesU et coupes,50 candidats,
79 coupes,41.69s : UNKNOWN (limite50), aucune famille exclue. Le dernier
pilote de la table conjointe126 trouve un bord local en0.77s ; cela ne
certifie pas le secteur11. Aucun gain global de solveur mesure.

761/762 lus/acquittes lors du saut763. Contributions du pair acceptees :
rang quatre-etoiles=30-delta, delta multiplicite de-4 sur les40 exterieurs ;
conjecture de transversales t(l)>=8 sous les conditions locales completes,
et question sur une borne inferieure globale de P. Rien de cela n'est
re-audite ni transforme en instruction autonome. Aucune preuve que tout
Conway doit entrer dans G1/c55 ; aucune exclusion C1. Transmission763 :
catalogue exact, cible unique11, construction U PSD avec T11 negatif.
Les bornes inferieures globales sur P restent a examiner, pas resolues ici.
Pas de processus local restant, aucun nouveau SRG construit.

### Prolongement15/10, messages764-766 : un budget sommable sans G1

764 lu/acquitte : Claude demande une inegalite de comptage issue des
formes locales et sommable dans TOUT Conway. 765/766 lus/acquittes lors
du saut767 : ses recherches sans symetrie restent non concluantes ; les
seuils t(l)+t(m)>=15 ou quatre grilles par droite sont des CONJECTURES.
Pas de re-audit de ses recherches ni de lancement d'une campagne jumelle.

QUESTION P=0. Le certificat anterieur conserve dans c1-codex/data/
codex_order9_prism_cap.json donne P<=11088/13, donc P<=852 entier.
Il est consomme sans re-verification de son identite. La nouvelle question
est la faisabilite P=0 dans le census affine d'ordre9, lui aussi accepte.
Source codex_order9_census.json (5311 types,57 parametres), SHA256
a49f811e4b64729d6da8c806ef2e1db1836cc221a17451893ecccb2ff699a291.
GLOP avec P fixe a0, puis reconstruction rationnelle et evaluation exacte
du NOUVEAU point :57 parametres non negatifs,5311 comptes non negatifs,
231 comptes nuls,4001 comptes non entiers, somme1731030945644=C(99,9).
Temps2.22s. Donc cette RELAXATION REELLE ne donne aucune borne P>0.
Cela ne prouve ni la faisabilite du census ENTIER ni celle d'un graphe.
Outil conway_census_prism_zero.py ; point complet et empreinte source dans
data/codex_local_global_20261015/census_prism_zero.json.

NOUVEAU BUDGET LOCAL. Choisir v, deux de ses sept droites, et les44 labels
S des quatre etoiles. Pour chaque lettre exterieure x, B_x contient les
quatre labels ax avec a dans les deux droites. D est la matrice10x44
de ces dix ensembles disjoints, E=D Gamma D^t. E_xx compte deux fois les
aretes internes ; E_xy compte une fois les aretes entre deux ensembles.
Poser Mt le couplage des dix lettres et h=sum des5 E[x,xbar]. Alors
 M=D T D^t=6I+2(J-Mt)-E,
 V=D U D^t=(176I+16Mt-44J)/15+E,
 M+V=(14/15)(19I-Mt-J).
Dans tout Conway, M et V sont PSD. Ainsi tr(MV)>=0, sans commutation
requise. Le developpement exact donne
 15 tr(MV)=3520-[15||E||_F^2+86 trE+92h-74 sumE].
Donc le score entre crochets est<=3520.

VERSION SOLVEUR. Une seule somme de55 termes entiers :
 - diagonale e dans{0,2,4} :15e^2+12e ;
 - paire mate e dans0..4 :30e^2-56e ;
 - autre paire non ordonnee e dans0..8 :30e^2-148e.
La somme est<=3520. Export de toutes les tables(e,valeur), avec les
labels/buckets. Les domaines viennent des matchings d'etoiles et des
capacites1/2 vers une etoile, sans groupe d'automorphismes. Aucun gain
de vitesse ni independance de toute ancienne contrainte n'est affirme.

SOMMATION EXACTE. A la racine v, definir t_v=sum des sept nombres de
transversales et d_v=#aretes {a,x}~{abar,xbar} entre deux paires racines.
Le graphe lointain a84 sommets de degre12,504 aretes, dont84 ont une
lettre commune. Les comptes des cinq types (intersection,incidence mate)
sont respectivement :
 (1,0):84-t ; (1,1):t ; (0,0):336+t+d ; (0,1):84-t-2d ; (0,2):d.
L'identite t+b+2d=84 vient de la somme des aretes entre etoiles mates.
Sur les21 paires de droites, un comptage de CHAQUE arete donne :
 sum trE=168+8t ; sum h=84+4t+8d ;
 sum e(recouvrement)=t+d ; sum sumE=4368+8t+8d.
Les cinq quadruplets de multiplicites ont ete enumeres sur tous les
couples des84 labels, sans lire un germe. Le budget local somme devient
 15 sum_l<m ||E_vlm||_F^2+464 t_v+144 d_v<=374976.

Chaque prisme est vu par les trois sommets de chacun de ses deux triangles :
sum_v t_v=6P. Chaque motif Z2 de sept sommets a une unique racine de
degre4, d'ou sum_v d_v=Z. En sommant sur les99 racines puis divisant par3 :
 5 sum_v,l<m ||E_vlm||_F^2+928P+48Z<=12374208.
C'est une contrainte NECESSAIRE SUR TOUT CONWAY, sans G1, et un comptage
de second moment (les carres comptent des paires d'aretes). Ce n'est PAS
encore une borne inferieure sur P, ni une exclusion. Une borne inferieure
suffisante sur cette somme de carres reste a obtenir par les recollements.

POURQUOI CETTE MOYENNE SIMPLE NE SUFFIT PAS. Moyenner M sur les21 paires
de droites puis sur tous les renommages/orientations des cinq paires
exterieures. Dans les secteurs constant,symetrique de somme0,antisymetrique,
de dimensions1,4,5, ses valeurs propres sont
 4(84-t-d)/105 ; 3(84-t-d)/35 ; 8+8d/105.
Celles de V sont
 64/15+4(t+d)/105 ; 48/5+3(t+d)/35 ; 32/3-8d/105.
Les comptes elementaires t,d>=0 et t+2d<=84 rendent M moyen PSD et V
moyen defini positif. En particulier t=d=0 passe avec des marges strictes.
Cette moyenne PRECISE des compressions10x10 ne peut donc forcer t>0.
La portee ne s'etend pas a toute methode d'averaging imaginable : le
budget nouveau conserve les carres avant de sommer, donc les fluctuations.

Outil conway_coarse_counting_budget.py, artefact coarse_counting_budget.json.
Controles propres : compressions exactes, identite de trace sur une fixture
algebrique, multiplicites des cinq types d'aretes, coefficients globaux :
PASS. Transmission767 des deux resultats et exports portables dans
lab_exchange_2026-10-14. Pas de re-audit de germe, aucun processus restant,
aucune construction SRG, aucune exclusion C1.

### 15/10, suite768 : plancher entier et limite exacte des comptes grossiers

768 lu/acquitte. Claude travaille sur une autre compression, aux vecteurs
impairs. Je poursuis sa question sur la borne inferieure de Q, sans audit
de ses germes. Correction de portee de son commentaire : le point P=0
concerne le census affine FOURNI, pas toute relaxation imaginable<=9.

IDENTITE ENTIERE. Pour chaque E, definir Delta(E) par la somme de
 e_ii(e_ii-2) sur la diagonale,
 2e_ij(e_ij-1) sur les cinq paires mates,
 2(e_ij-2)(e_ij-3) sur les quarante autres paires non ordonnees.
Tous ces termes sont non negatifs sur les domaines entiers autorises.
Exactement ||E||^2=5sumE-3trE-8h-480+Delta(E). D'ou, avec les
identites de comptage deja obtenues :
 sum_21 ||E||^2=10584-16t_v-24d_v+sum_21 Delta(E),
 Q=1047816-96P-24Z+Delta_global,
 et le budget precedent devient5Delta_global+448P-72Z<=7135128.

TEMOIN EXACT DE LA RELAXATION GROSSIERE. Construction d'une matrice
entiere10x10 avec trE=8,h=4,sumE=208,||E||^2=504,Delta=0 ;
ses deux compressions M et V sont DEFINIES POSITIVES (pivots LDL
rationnels strictement positifs exportes). Les sommes de lignes sont
20 ou22. Elles satisfont sum_y E_xy=24-2u_x avec u entier>=0,
sum u=16, compatible avec un recouvrement de quatre labels sans arete.
Preuve de l'identite de ligne : pour chaque label ax, les quatre
etoiles centrales comptent six voisins avec multiplicite, un voisin
du recouvrement etant compte deux fois. Sommer sur les quatre a.

Les21 copies de cette matrice, puis99 racines INDEPENDANTES, satisfont
les comptes agreges P=Z=0 et Q=1047816. Le minimum moyen504 est donc
EXACT dans cette relaxation, meme avec les deux compressions PSD et
les identites de lignes indiquees. Le budget ne contredirait P=Z=0
que pour une moyenne>5952/5=1190.4. Cette construction ne recolle PAS
les matrices en une meme adjacency et ne satisfait pas de conditions
PSD sur les formes COMPLETES44x44 ni de bornes de rang. Elle ne
prouve aucun germe Conway, aucune possibilite d'un Conway sans prisme.

CAS D'EGALITE APRES RECOLLEMENT. Conditionnellement a t_v=d_v=0 et
sum Delta=0, chaque matching d'etoile tau_x, sur les douze lettres
restantes, se contracte sur les six paires mates en C6 ou2C3. Pas de
boucle (t=0), pas de double arete (sinon un E_yy=4 et Delta>0), degre2.
Enumeration propre des10395 matchings :3840 du typeC6,640 du type2C3,
soit4480 et seulement DEUX formes a renommage des paires pres.
La bijection sigma entre deux etoiles mates n'a aucune arete interne
a une paire (t=d=0) et au plus une fleche par paire non ordonnee
de lignes (E_x,xbar<=1). Son graphe contracte est donc K6 prive d'un
couplage parfait, oriente avec deux entrees/deux sorties partout.
Il y a38 orientations par graphe,15 couplages manquants et4^6 releves,
soit2334720 bijections etiquetees. Classifications necessaires de CE
cas d'egalite, pas de tous les germes Conway.

PILOTES DE RECOLLEMENT. Un nouveau modele sur les84 labels impose
Gamma B=2J-B(I+Mt), t=d=0 et Delta=0 sur les21 matrices, plus sommes
de lignes>=18 (condition suffisante simple pour V defini positif).
Il n'impose ni equations SRG lointain-lointain ni PSD44/rangs.
Deux essais bornes15s chacun : sans symetrie UNKNOWN ; avec rotation
des sept lignes imposee uniquement pour chercher un temoin,480 variables
d'adjacence, UNKNOWN aussi. Aucun verdict d'impossibilite, aucun temoin
recolle obtenu. Pas de relance automatique ni de processus restant.

Outils conway_coarse_integer_floor.py et conway_coarse_gluing_floor.py.
Artefacts coarse_integer_floor.json, coarse_gluing_floor.json et
coarse_gluing_floor_cyclic.json dans data/codex_local_global_20261015/.
Controles propres : secantes entieres, identite exacte, pivots LDL,
classifications locales par enumeration ; aucun germe du pair audite.
Aucun SRG construit et aucune exclusion C1.

### 15/10, suite769 : obstruction croisee impaire et interface exacte au census

Transmission770 du plancher grossier. Le saut a revele769, lu/acquitte.
Claude situe numeriquement les violations de ses exemples dans la
compression impaire de deux droites ; observations acceptees sans audit.
Il demande quels blocs/cycles sont representables dans le census existant.
Son message rapporte aussi une directive utilisateur : cette attribution
reste une contribution du pair, pas une instruction utilisateur nouvelle.

NOUVEAU LEMME UNIFORME. Pour UNE droite racine l={v,a,abar}, sur les
douze autres lettres, Q=tau_a+tau_abar-sigma-sigma^t. Les deux tau sont
des matrices de matchings, sigma une permutation. Donc Q1=0, Q symetrique
et ||Q||_op<=4, sans hypothese de symetrie du graphe. Dans1-perp :
 T_impair=6I-Q a toutes ses valeurs propres dans[2,10],
 U_impair=8I+Q a toutes ses valeurs propres dans[4,12].
Ainsi chaque bloc diagonal impair est automatiquement defini positif
sur les onze dimensions utiles et a exactement le noyau1 impose.
Une obstruction dans la compression a DEUX droites vient necessairement
du BLOC CROISE. Ce n'est pas une preuve de positivite des formes44x44.

Certificat par carres :4I-Q=(I-tau_a)^2/2+(I-tau_abar)^2/2+
(I+sigma)(I+sigma^t). La borne inferieure analogue vient des signes
inverses. Dans des bases orthonormales de1-perp, les tests de positivite
de la compression impaire combinee sont exactement les deux Schur :
 D_T-C^t A_T^-1 C>=0,
 D_U-(7Omega+C)^t A_U^-1(7Omega+C)>=0.
Les inverses existent toujours. Chaque Schur est11x11 ; aucune borne de
rang globale ni positivite complete du bord ne suit de ces seuls tests.

MOMENTS ET CENSUS. Poser f=tr sigma (prismes de l), a=tr(tau_a tau_abar),
b=tr(sigma^2), c=tr(tau_a sigma), d=tr(tau_abar sigma). Alors
 trQ=-2f ; ||Q||_F^2=48+2a+2b-4c-4d ;
 tr(T_impair U_impair)=528+4f-||Q||^2>=432+4f.
Le dernier minorant est automatique car a,b<=12 et c,d>=0 : le produit
de traces sur une seule droite ne peut donc localiser une violation.

Enumeration de NOUVEAUX motifs marques, census accepte sans regeneration :
 a : racine, deux lettres de l, deux lettres exterieures, quatre labels
lointains, donc9 sommets ;32 completions brutes,10 admissibles,6 types.
 b hors points fixes : meme support9 ;32 brutes,4 admissibles,2 types.
 c : trois labels lointains, donc8 sommets ;4 brutes,1 admissible,1 type.
Multiplicites exactes = nombre de completions etiquetees * |Aut(type)|.
Diviser par2 pour a et b (deux orientations de l) ; le motif c somme
sur les deux orientations donne directement c+d. Les sommes portent
sur les99*7=693 drapeaux(racine,droite non orientee).

Hn_code designe le COMPTE INDUIT du type, libre ou expression affine :
 sum a=6H9_10984541408+36H9_13262907120+2H9_13912920516+
       2H9_15781745092+2H9_40207239904+2H9_61757303448 ;
 sum b=6P+12H9_13904794052+6H9_61505645208 ;
 sum(c+d)=2H8_225487536=4Z2 ;
 Z2=H7_1761497=133056-6P-h7_1985025/4.
Les vecteurs affines complets sur les57 parametres sont exportes, ainsi
que les graphes definissant chaque parametre. A l'ordre7 :208 types,
2 parametres ; a8 :916 types,9 parametres ; a9 :5311 types,57 parametres.
Notre ancien point rationnel P=0 donne sum a=24948/5,sum b=0,
sum(c+d)=33264/5,sum||Q||^2=16632,sumtr(TU)=349272. Ces moments
seuls ne le refutent pas. Il reste un point de RELAXATION sans graphe.

LIMITE DE SUPPORT. Une entree B_xy avec les quatre lettres centrales,
les deux exterieures et les deux labels lointains tient sur9 sommets.
Un produit generique de deux telles entrees peut employer quatre labels
lointains et11 sommets. Le census9 ne le code donc pas automatiquement ;
il faut des identites supplementaires ou des comptes cibles. Cette
remarque ne prouve pas l'independance algebrique des comptes d'ordre11.

Outil conway_odd_census_interface.py ; artefact odd_census_interface.json.
Controles propres : nouvelles expansions de traces et certificat par
carres sur une fixture de permutations, completions des motifs marques,
facteurs d'automorphismes et identite affine sum(c+d)=4Z2. Aucun germe
du pair audite, aucun census re-genere, aucun processus restant.
Aucune exclusion C1 ni construction d'un SRG.

### 15/10, suite772 : prolonger c55 force une rupture massive de symetrie locale

772 lu/acquitte. Claude fournit fourstar_psd_rank30_urep100.json : bord
local G1 c55, T/U PSD de rangs30/40, nullitesT(10,1,1,2), certification
exacte du producteur acceptee SANS ouvrir ni re-auditer son germe.
Son label{4,6} ne se prolonge pas :2591 profils,16 compatibles au noyau,
aucun de norme5/2. Son analyse de ces16 profils lui reste reservee.
Le temoin refute l'exclusion locale par C1/C1'/C2+PSD+rangs ; il ne
refute pas toutes les contraintes sur un bord deduites d'un prolongement.

NOUVEAU RESULTAT POUR LA FAMILLE ENTIERE, non pour son seul germe :
supposer G1, c=(5,5), recouvrement NON grille et T/U PSD. Normaliser
les deux paires exterieures actives A=(4,5),B=(6,7). Les trois autres
paires sont ordinaires. Le quotient trivial T00=ww^t avec
w=e_O-e_LA-e_RB est celui deja prouve, de rang1. Pour un label manque
u, nO(u) est le nombre de voisins parmi les quatre labels de O.
La positivite impose B00^t T(S,u)/2=(1-nO)w/2. Les onze comptes
d'orbites sont donc determines par nO et les paires utilisees par u.
Table exacte exportee (y compris projections T00/U00) : nO dans{0,1}
si u utilise A ou B ; nO dans{0,1,2} si ses deux paires sont ordinaires.
Pas d'utilisation des caracteres non triviaux d'un germe particulier.

VECTEUR PROPRE GLOBAL. Dans un vrai Conway, T_far^2=7T_far,
T_far annihile l'incidence des14 lettres racines et porte l'espace
propre-4 du graphe lointain. Poser z=T_far*1_O et le prolonger par0
sur la racine et ses14 voisins. Sur S, z vaut+1 sur les4 labels de O,
-1 sur les8 labels de LA et RB,0 sur les32 autres. Sur les40 labels
exterieurs, z_u=1-nO(u), donc encore dans{0,+1,-1}. De plus
||z||^2=7*1_O^t T_far 1_O=28 et somme z=0. Donc A99 z=-4z avec
EXACTEMENT14 signes+1,14 signes-1,71 zeros. Les4 labels de O ont
degre3 dans S et12 dans le graphe lointain, donc sum_u nO=36.
Cela donne N0+N1+N2=40, N1+2N2=36, N0+N2=16, d'ou
 (N0,N1,N2)=(10,24,6).
Les six labels ayant deux voisins dans O utilisent tous deux paires
ordinaires : ils sont parmi les douze labels sur(8,9),(10,11),(12,13).

RUPTURE DE L'INVOLUTION LOCALE. h=g1g2 permute(0 1)(2 3) et fixe
les dix lettres exterieures, donc chacun des40 labels manquants.
Un tel label brise h lorsque son voisinage dans S differe sur au moins
une des22 paires(i,h(i)). Projeter T(S,manquants) sur les caracteres10
et01, c'est-a-dire le secteur h-impair, donne une matrice R. Dans ces
deux blocs T+U=7Pi, Pi projetant sur les deux espaces de dimension10
orthogonaux aux etoiles imposees. Le catalogue exact126 deja etabli
donne T et U definis positifs sur chacun. Par T_far^2=7T_far :
 RR^t=7T_impair-T_impair^2=T_impair U_impair, donc rangR=20.

La partie fixe geometrique des colonnes est h-paire : une colonne
de R est nulle exactement quand le profil de voisinage est h-invariant.
Pour chaque lettre exterieure x, son etoile dans S est h-paire ;
T_far B=0 donne R B_manquants=0. B_manquants est l'incidence NON
ORIENTEE des40 aretes de K10 prive de ses cinq paires mates.
Soit H le sous-graphe forme par les labels dont la colonne est non
nulle. Alors20<=|E(H)|-rang(B_H). Le rang d'une composante connexe
est m-1 si elle est bipartie, m sinon. Avec au plus10 sommets, les
bornes binom(m,2)-max(0,m-5), ou floor(m^2/4) si bipartie, laissent
seulement une composante NON bipartie sur9 ou10 sommets :
 - neuf sommets : au moins29 aretes ;
 - dix sommets : au moins30 aretes.
L'enumeration finie des tailles de composantes confirme que toutes
les composantes<=8 ne donnent qu'une nullite d'incidence<=17.
Donc AU MOINS29 DES40 SOMMETS EXTERIEURS DOIVENT BRISER h. Aucun
automorphisme global n'est impose ; ce resultat quantifie justement
l'impossibilite de prolonger cette involution en conservant la plupart
des profils. Il ne prouve pas que le groupe global entier serait trivial.

VERSION SOLVEUR. Adaptateur add_completion_cuts(model,rows_by_label),
conditionnel a CETTE famille canonique. Domaines et histogramme nO,
880 XOR pour les22 paires et40 labels,40 indicateurs break,10 indicateurs
de lettres utilisees. Imposer used>=9 et sum_break>=20+used. Cela
implique au plus11 profils h-invariants, et au plus10 si toutes les
lettres sont utilisees. Aucun appel de ces contraintes sur une famille
generale non couverte. Adaptateur valide dans CP-SAT :2850 variables
dont1760 adjacences d'entree,2123 contraintes ; pas de campagne solveur
ni de gain de vitesse mesure.

Outil four_star_c55_global_constraints.py, c55_global_constraints.json.
Controles propres : tables du quotient, cap fixe des caracteres,
equations d'histogramme, enumeration des tailles et fixture29 aretes
de rang d'incidence9 (temoin de ce seul argument de rang, pas un SRG).
Le support29 est optimal POUR CES SEULES contraintes d'incidence.
Aucun fichier du germe772 lu, aucun processus restant. Ni la famille
c55 ni C1 ne sont exclus ; aucune preuve que tout Conway entre dans c55.

### 15/10, suite774 : exclusion de la famille G1 c55 non grille par F7

774 lu/acquitte. Claude a exclu les40 extensions individuelles de son
germe quatre etoiles, et constate rang_F7(8T)=30 sur ce germe. Il rappelle
les resultats globaux anterieurs L4/L23/L22 : tout bord principal a
rang_F7(8T_S)<=k<=28. Ces resultats du producteur sont ACCEPTES ; aucun
germe, extension, rang ou discriminant fourni par Claude n'est re-audite.

Notre piste complementaire porte sur TOUTE la famille G1 c55 NON GRILLE,
pas sur les germes deja refutes. Les conditions sont celles du quotient
canonique etabli : invariance G1 du bord44, cinq composantes sur chacune
des deux droites, recouvrement non grille, T/U PSD. Aucun G1 global suppose.

THEOREME NOUVEAU : dans cette famille, rang_F7(8T_S)>=29. Avec la borne
globale<=28 rappelee dans774, AUCUN bord de cette famille ne se prolonge
en un Conway. Ce n'est pas une exclusion du cas de recouvrement grille,
des autres comptes de composantes, des bords generaux ou de tout C1.

PREUVE FINIE. Le changement de base par caracteres de G1 a determinant
inversible modulo7. Les quatre rangs s'additionnent. Le bloc trivial
ww^t a rang1. Reutiliser le catalogue exact126 des secteurs10/01 :
rang_F7(T_chi)=5+rang_F7(schur_t). Les pivots droits et le facteur
10(3-d) sont inversibles modulo7 ; la relation d'etoile est retiree
par une congruence entiere. Sur126 etats,114 ont rang10,12 ont rang9.
Les12 derniers ont s=d=+1. Le seul offset interne de O est non nul,
donc ses deux signes10/01 ne peuvent etre simultanement+1 : les deux
pertes de rang ne peuvent pas se produire ensemble.

Pour chaque bloc de degre1 du quotient, la valeur du caractere11
d'adjacence est le produit de celles des caracteres10 et01. Sur les
grilles ordinaires de degre interne2, la valeur11 est0. Les trois
diagonales O,L0,R1 interdisent chacune la paire de signes(+1,+1).
Sur126^2 paires de tables, il en reste exactement4536.

POINT ESSENTIEL DE RECOLLEMENT : chaque table avait supprime cinq
signes de lignes, soit dix en tout. Une congruence diagonale en11
les retire des entrees d'adjacence MAIS change la correction geometrique
Li,Ri. Il reste cinq PRODUITS de signes t_i dans{-1,+1}. Garder les
32 possibilites est indispensable. Notre message de direction775
annoncait trop vite seulement126^2 cas ; la presente preuve les inclut.

La matrice explicite2*T11 commence par diag(6,5,...,5) et les cinq
entrees Li,Ri=-t_i ; on soustrait deux fois le produit des signes
d'adjacence10/01 partout ou le degre du quotient est1. Elle est
congruente au vrai bloc, avec facteurs inversibles modulo7.

Elimination exacte modulo7 de4536*32=145152 matrices11x11 :
 - rangs10/01=(9,10) : rang11=9/10/11 en12/996/5904 cas ;
 - rangs10/01=(10,9) : memes comptes ;
 - rangs10/01=(10,10) : rang11=9/10/11 en342/17550/113436 cas.
Rangs totaux :29 en24 cas,30 en2334,31 en29358,32 en113436.
Minimum29, sans meme imposer PSD dans11, le rang rationnel<=30,
ni les autres capacites de voisins communs. Ce sur-ensemble couvre
tous les bords de la famille, donc le minorant est universel pour elle.
Une sous-matrice principale ne peut depasser le rang de8T_far :
contradiction avec la borne globale28 deja etablie.

CONTROLES PROPRES : reconstruction de12 nouveaux lifts44 (fixtures
de la relaxation, pas des SRG), bases de caracteres calculees depuis
les labels, tous blocs croises nuls, normalisations et congruences
exactes, rang44 direct egal a la somme des rangs. Trois choix distincts
des cinq signes eliminables par exemple. Rangs des blocs11 representatifs
confirmes par DomainMatrix sur GF(7). Aucun fichier de germe Claude lu.
Le catalogue126 utilise a pour SHA256
2d7da56d1b3d34821d8b98b58caaf4e4b0d3d463c2c3bfdf934096243fea0224.

SOLVEUR : toute branche de COMPLETION globale qui etablit ces conditions
locales peut etre rejetee immediatement. Le modele local de seule
positivite peut toujours avoir des temoins, dont celui du producteur.
Pas d'integration inconditionnelle a un solveur general, ni de gain de
temps mesure. Les contraintes de772 sont correctes mais cette famille
est desormais eliminee avant leur recherche d'extension.

Outil code/codex/four_star_c55_mod7.py ; artefact
data/codex_local_global_20261015/c55_mod7.json et copie portable
lab_exchange_2026-10-14/codex_c55_mod7.json. Aucun processus restant.

### 15/10, suite778 : au moins336 bords avec quatre relations mixtes

778 lu/acquitte. Claude accepte l'exclusion G1 c55 non grille sans la
refaire. Il etudie les relations mixtes, observe au plus2 dans ses2500
bords G1 PSD et cherche hors G1. Observation et identite G9 acceptees,
aucun rang de ses bords re-audite. Son enumeration des seuils uniformes
MIX<=M ne prouve pas ces seuils : ils restent des conjectures.

STATUT DES BORNES demande par le pair. P<=1151 a une preuve cubique
dans ce journal, ensuite renforcee en P<=1150. Chaque grille utilise
six prismes, dont chacun a au plus une grille completante, donc6rho<=P.
Le certificat conserve c1-codex/data/codex_prism_plus_five_grids_cap.json
exprime1386-P-5rho comme somme de15 comptes induits a9 sommets avec
coefficients rationnels positifs. C'est un certificat exact deja verifie,
pas seulement une sortie LP numerique ; ses identites sont celles du
census9 accepte. Aucun census regenere. Ensemble :11rho<=1386, rho<=126.
Le fichier distinct codex_order9_prism_cap.json donne aussi P<=11088/13.
Statuts et chemins transmis dans779, sans nouvelle verification du pair.

NOUVELLE IDENTITE SANS SYMETRIE. Pour chaque sommet v, G_v est le graphe
des grilles sur ses sept droites. Ecrire e_v=|E(G_v)|, g_l=deg(l),
epsilon_lm=1 si la paire est une grille. Les composantes H_l donnent
c_l<=f(g_l)=3+floor(g_l/2), et g_l!=5 (resultat P9 accepte).
Poser o_v=nombre de degres impairs et h_v=sum_l(f(g_l)-c_l)>=0.
Pour le bord44 de la paire, poser
 m_lm=dim ker(T_S44)-(2+c_l+c_m-epsilon_lm),
 delta_lm=30-rang(T_S44)>=0 dans un Conway.
G9 donne m_lm=12-c_l-c_m+epsilon_lm+delta_lm. Chaque droite apparait
dans six paires et sum floor(g_l/2)=e_v-o_v/2. En sommant :
 sum_l<m m_lm=126-5e_v+3o_v+6h_v+Delta_v,
avec Delta_v=sum_l<m delta_lm. Une grille a9 sommets contribue neuf
incidences, donc sum_v e_v=9rho. Ainsi EXACTEMENT
 sum_global m=12474-45rho+3O+6H+Delta.
La borne rho<=126 donne sum m>=6804, moyenne>=36/11 sur2079 drapeaux.
L'exces positif sum max(m-3,0) est au moins567, et augmente avec O,H,
Delta et les deficits des couples ayant moins de trois relations.
Ces relations sont lineaires dans les noyaux ; elles ne sont pas des
automorphismes. Aucune hypothese G1 n'intervient.

NOUVEAU COMPTAGE DES COUPLES EXCEPTIONNELS. Chaque m_lm est au moins
12-f(g_l)-f(g_m)+epsilon_lm. Classer les sommets de G_v en A (degres0,1),
B (2,3), C (4), D (6). Les paires forcement >=4 sont exactement :
toutes celles incidentes a A, celles internes a B, et les aretes B-C.
Pour A-D, le sommet de D est universel. Leur nombre est donc
 b_v=|A|(13-|A|)/2+binom(|B|,2)+e(B,C).
Enumeration de CE NOUVEL objectif sur les2^21 graphes etiquetes :
1142968 sans degre5. Minimum b selon e=0,...,18,21 :
 21,21,21,21,21,21,20,19,17,15,11,7,3,1,0,0,0,0,0,0.
Les e=19,20 ont toujours un degre5. Les temoins des minima sont exportes.
Ce calcul ne refait pas les bords PSD de Claude ni sa recherche de germes.

CERTIFICAT COURT POUR336. Le profil implique13b+20e>=273. Somme sur99
sommets, avec sum e<=1134 :13B>=4347, donc B>=335. Si B=335, alors
sum e=1134 et la somme des ecarts a273 est au plus8. Les seuls profils
individuels possibles sont (e,b,ecart)=(0,21,0),(13,1,0),(12,3,6),(14,0,7).
Un b superieur au minimum ajoute13 a l'ecart. Il peut donc y avoir au
plus un profil de type12 ou14 ; tous les autres ont0 ou13 aretes.
La somme des e serait0,+1 ou-1 modulo13, alors que1134 vaut3. Contradiction.
Donc AU MOINS336 des2079 drapeaux (v,{l,m}) ont m_lm>=4.
Au moins18 sommets ont un tel couple : les autres ont au moins14 grilles,
et le budget global est1134 incidences. On compte des drapeaux centres,
pas336 matrices non isomorphes ni336 sous-ensembles necessairement distincts.

La relaxation des99 graphes de grilles INDEPENDANTS atteint336 avec
12 graphes vides,84 graphes a13 aretes et3 graphes a14 aretes. Cela ne
les recolle pas en un seul Conway, ni ne realise leurs relations mixtes.
Le plancher est exact pour cette relaxation seulement.

CONTROLES PROPRES : formule du nouveau b confrontee a sa definition
directe sur tous les temoins extremes, identite locale de somme,
programmation dynamique entiere sur99 sommets et1134 incidences,
certificat par ecarts et modulo13. Calcul total2.56 secondes. Aucun
appel SAT ni germe du pair traite. Le budget seul n'exclut pas Conway.
Il impose une population importante de bords a quatre relations mixtes,
au-dela de la seule recherche d'un contre-exemple a MIX<=2.

Outil conway_mixed_relations_budget.py ; artefact
data/codex_local_global_20261015/mixed_relations_budget.json et copie
portable codex_mixed_relations_budget.json. Aucun processus restant.

### 15/10, reprise785 : c55 sans G1, puis axe ODD9

781 acceptait le budget336 et annoncait des marches hors G1. Travail
ci-dessous commence avant l'interruption, conserve au retour du matin.
782-785 lus/acquittes ; reponse786 par le pont. Contre-exemples du pair
acceptes (4 puis6 relations mixtes, c pouvant valoir1), sans re-audit.
H-MATCH => point de Hamming accepte, mais H-MATCH et ODD9 restent ouverts.
Codex prend T2 : ODD9 par Schur / couplages ; Claude travaille T3.
La conjecture N9 refutee (nullite<=9+min(c)) n'est PAS le theoreme global
LAB635 interdisant un neuf-ensemble a17 aretes. Distinction lue directement
dans AUDIT_EXCLUSIONS_2026-10-15.md, branche LAB du matin, sans vieilles notes.

GENERALISATION c55 NON GRILLE, SANS G1. La decomposition de chaque droite
en cinq composantes partage ses six paires exterieures en une composante
de deux paires et quatre singletons, ces derniers etant des grilles.
Le recouvrement O appartient donc a la composante active des deux droites.
Noter LA et RB leurs fibres actives exterieures. Les dix relations connues
sur les indicatrices de fibres (huit grilles, O+LA et O+RB) imposent
la compression normalisee H=t*w*w^t sur onze fibres de quatre sommets,
w=eO-eLA-eRB, t=2-e(O)/2. Son entree LA,RB est aussi
1-[A=B]-e(LA,RB)/4. Donc A!=B et0<t<=1, soit e(O)=2 ou3.
Le cas3 donne avec le centre et ses quatre voisins un neuf-ensemble
a17 aretes, exclu par le THEOREME GLOBAL accepte635. Les tests locaux
de coeur seuls ne l'excluent pas :32 coeurs passent T/U PSD.

Pour e(O)=2, normaliser A={4,5}, B={6,7}. Le coeur O+LA+RB a12 labels.
Enumeration des3*3*24 choix de deux couplages et d'une permutation sur
quatre lettres, avec connexite et C1/C2 :122 motifs de droite, dont
36 avec e(O)=2,8 avec3,68 avec1,10 avec0. Les cas0/1 ne passent pas
la compression complete precedente. Deux motifs avec recouvrement commun,
les deux relations de noyau et C2 donnent128 coeurs distincts pour e(O)=2.
Tous passent T/U PSD sur12 labels, rangT10 ; O,LA,RB induisent chacun
un couplage parfait, O-LA et O-RB aussi ; LA-RB est vide.
Les16 flips des quatre paires et l'echange simultane des deux droites
et des deux paires exterieures donnent un groupe32 :18 types de coeur.

Les huit noyaux de grilles imposent tous les nombres de voisins entre
fibres : le quotient est EQUITABLE et identique au precedent quotient
c55, sans imposer G1. Il reste19 blocs de couplage4x4, soit19 permutations
arbitraires de S4. Sur les trois directions de Walsh non constantes,
chacune agit par une permutation signee3x3 dont le produit des trois
signes vaut+1 :24 choix, dont seulement4 diagonaux (ancienne restriction
V4). Un coeur G1 ne rend pas automatiquement toute la completion G1.

Le secteur constant de T a rang1 ; le secteur standard a dimension33,
2T_std=C_T-2Gamma_std et3U_std=C_U+3Gamma_std, corrections entieres
exportees. APRES les equations completes des quatre etoiles, deux
relations ont des pivots1 dans les coordonnees10/01 de O : suppression
par congruence, tests principaux31x31. Ainsi rangT44=1+rangT31 et
nombre de relations mixtes=31-rangT31. Une completion Conway impose
rang_Q(T31)<=29 et rang_F7(2T31)<=27. Ce n'est pas une exclusion.

EXTENSION DES COMPTES GLOBAUX. z=T_far*1O, prolonge par0 sur la boule
du centre, vaut+1 sur O,-1 sur LA/RB,0 sur les32 autres labels presents,
et1-nO(u) sur les40 labels absents. Les relations de composantes donnent
nO<=1 si u utilise A ou B, sinon nO<=2. Donc z est entier dans{0,+1,-1}.
T_far^2=7T_far et1O^t*T*1O=4 donnent ||z||^2=28 ; z est de somme0,
vecteur propre de valeur-4. Il a14 signes+ et14 signes-. Les quatre
sommets O ont chacun neuf voisins parmi les40 absents, soit sum nO=36.
Les comptes exterieurs0/1/2 sont donc exactement(10,24,6). Aucun G1 requis.
La borne de29 profils brisant h, elle, utilise le catalogue G1 et N'EST
PAS etendue. Adaptateur CP-SAT general add_completion_counts : histogramme
et400 equations de comptage par composantes, aucune coupe d'automorphisme.

Controles propres :128 coeurs distincts,18 orbites,24 actions S4 exactes,
18 nouvelles fixtures de lifts equitables/Fourier ; elles ne sont PAS
des bords PSD ou des graphes de Conway. Les catalogues de coeurs avaient
ete controles exactement lors de leur production. Aucun germe du pair lu.
18*24^19 reste un parametrage fini, PAS un cout abordable prouve.
Outils four_star_c55_general_overlap.py, four_star_c55_permutation_lift.py ;
donnees c55_general_overlap2.json, c55_general_overlap3.json,
c55_permutation_lift.json. Famille generale et C1 toujours ouverts.

### 15/10 matin, T2 : ODD9 comme energie dans un reseau pondere

NOUVELLE FORMULE EXPLICITE, sans hypothese h/G1. Sur les24 labels X_l,
F e_{a,y}=e_{a^1,y}, M e_{a,y}=e_{a,y^1}, u=(1^12,-1^12). Gamma_X
est la reunion de deux couplages : un dans chaque etoile et un entre elles.
Alors, par les entrees geometriques K deja definies,
 8T_X = L8-u*u^t,
 L8=8(2I-Gamma_X)+3(I-F)+(I-M)+(I-FM).
C'est un VRAI laplacien de graphe pondere, de conductances8 sur Gamma,
3 sur F,1 sur M et1 sur FM ; additionner les poids si une arete coincide.
F et M sont seulement des permutations de labels, PAS des automorphismes
de Gamma. Aucune commutation GammaF=FGamma n'est utilisee.

L8u=24u et||u||^2=24. Les composantes du reseau sont equilibrees en u,
car chacune contient les partenaires sous F. Retirer u*u^t supprime
exactement cette direction propre ; les autres noyaux sont les c
indicatrices de composantes. On retrouve rangT_X=23-c, cette fois avec
un inverse explicite par potentiels de reseau utilisable pour ODD9.

Poser f_y=e_{2y}-e_{3y}, y=4,...,13, et Fodd la matrice de ces colonnes.
La somme des dix f_y differe d'un vecteur de X_l par la difference des
etoiles2 et3, dans kerT. Les neuf colonnes P=(e_0-e_9,...,e_8-e_9)
representent donc tout le gain impair. Leur incidence sur les14 lettres
est nulle : K*Fodd*P=0. Poser
 q=Gamma[X_l,:]*Fodd*P,
 d8=8*P^t*Fodd^t*(3I-Gamma)*Fodd*P.
Les comptes C1 donnent u^t*q=0 (chaque nouvelle etiquette a deux voisins
dans chacune des etoiles0 et1). Sous T PSD, les sources q ont aussi somme0
sur chaque composante, par les noyaux de T_X. Un echec de ce dernier test
fournit immediatement un mineur de Gram2x2 a determinant negatif.

Retirer une ligne/colonne de L8 par composante, pour obtenir G definie
positive de taille24-c, et retirer les memes lignes de q pour obtenir qg.
Les solutions de Kirchhoff donnent exactement
 S9=d8-64*qg^t*G^-1*qg.
Le mode u ne contribue pas, puisque q lui est orthogonal. Le RANG de S9
est le gain des dix vecteurs impairs au-dela de X_l. Sous T PSD, S9 est
PSD : ODD9 est donc equivalente a sa positivite STRICTE, ou a
 det B >0, B=[[G,-8qg],[-8qg^t,d8]], entier de taille33-c.
det B=det G * det S9, et det G est le produit des nombres d'arbres
couvrants ponderes des composantes. Un determinant nul donne une relation
impaire exacte par le potentiel8G^-1*qg*t, t dans kerS9.
Cette formule ne prouve PAS det B>0 universellement. C2 et U PSD restent
a exploiter pour interdire la saturation. Une petite dimension de matrice
n'est pas une borne d'enumeration abordable de toutes ses entrees.

CONTROLES PROPRES : identite du laplacien sur les122 motifs actifs c55
produits par Codex ; six reseaux algebriques de c=1,...,6 composantes,
avec noyaux/rangs attendus ; pour chacun, deux matrices de Gram fabriquees
avec complement de Schur de rang8 puis9. Tous les complements exacts sont
restitues, la branche determinant nul rend la bonne relation. Une source
deliberement desequilibree sur une composante est rejetee. Ces douze
fixtures ne sont PAS des bords admissibles ni des graphes de Conway.

TEST D'UNE NOUVELLE EXPLICATION : le Schur10, a sommes de lignes nulles,
pourrait-il etre toujours un laplacien ordinaire a conductances positives ?
NON. Sur le c11 certifie du pair783 (certification ACCEPTEE, aucune PSD,
aucun rang ni groupe recalcules), calcul de CES NOUVEAUX COEFFICIENTS :
31 entrees hors diagonale negatives et14 positives ; maximum positif
592/63, entre lettres exterieures5 et13, en normalisation8T. Donc l'argument
par simple connexite d'un reseau positif n'est pas disponible pour le
Schur final. Cela ne refute PAS ODD9 et ne reprend pas l'audit du temoin.
Source fourstar_psd_c11_mix6.json, SHA256
e2423b0b92be52387bb0c65f9d20c2396e8d1081c4d96737911b59168f4a0b9a.

Code odd9_network_schur.py et odd9_conductance_probe.py ; artefacts
odd9_network_schur.json et odd9_conductance_c11.json. Aucun processus
restant. ODD9, la famille c55 generale et C1 restent ouverts.

Transmission789 : trois exports portables copies dans lab_exchange et
formules envoyees. Le saut de sequence a motive UNE lecture du pont,
787/788 lus/acquittes. Claude confirme la repartition T2/T3 et distingue
les trois N9. Il constate ODD9 sur120 structures aleatoires NON positives
et conjecture aussi nullite2 pour la compression h-impaire. Ces observations
sont acceptees, sans devenir des lois generales. Sa piste T3 est maintenant
T=[[A,B],[B^t,C]] et l'obstruction quantitative au bloc de couplage B.
Ne pas dupliquer ce travail. Le complement de Schur9 de notre reduction
reste un test exact, pas une preuve de nonsingularite universelle.

### 15/10, suite790 : adaptation au bloc h-pair, et limite du comptage de composantes

790 lu/acquitte. Claude annonce son analyse complete de15936 structures
au noyau fixe (9408 cassees, aucune positive) et distingue les echecs des
blocs diagonaux de U des echecs de couplage. Resultats acceptes, non refaits.
Sa question : notre reseau pondere peut-il faire de rang(A22)=10 une
condition sur le nombre de composantes ? Reponse precise : l'adaptation
naturelle est une DIFFERENCE de laplaciens ; le rang compte une multiplicite
spectrale, pas les composantes du reseau obtenu.

Soit Q la matrice44x22 des indicatrices des orbites de h=(0 1)(2 3),
lettres exterieures fixees. Ordonner O0={02,13}, O1={03,12}, puis
L_y={0y,1y}, R_y={2y,3y}, y=4,...,13. La base orthonormale est Q/sqrt2.
Poser Gamma_+=Q^t Gamma Q/2 et K_+=Q^t K Q/2. Aucun h automorphisme
de Gamma n'est suppose ; cette compression vaut aussi pour sa moyenne.
La geometrie donne R0=K_++J/2>=0, de denominateur4. Poser R=Gamma_++R0.
Alors A=3I-R+J/2 ;4R est une matrice symetrique ENTIERE non negative
pour tout bord binaire (Gamma_+ est a demi-entiers).

Les deux relations d'etoiles paires ont pour somme/difference
 w=(2,2,1^20), v=(0,0,1^10,-1^10), avec Aw=Av=0.
Comme sum w=24, Rw=3w+12*1. Pour D_w=diag(w), definir L_R comme le
laplacien aux conductances w_i*w_j*R_ij et L_K aux conductances w_i*w_j.
On obtient EXACTEMENT
 D_w A D_w = L_R - L_K/2,  L_K=24 D_w-w*w^t.
Les deux sont des laplaciens positifs. R0 seul a151 aretes de poids
strictement positif et est deja connexe (O0 est adjacent a toutes les
autres orbites). Donc L_R a TOUJOURS une seule composante, quel que soit
Gamma : ses composantes ne peuvent porter le rang variable de A.

Sur1-perp, L_K est defini positif. Sous A PSD, les valeurs propres
generalisees de (L_R,L_K) sont >=1/2 ; chaque egalite ajoute une direction
de noyau, en plus des constantes. Ainsi rangA10 equivaut a une multiplicite
11 du seuil1/2 sur cet espace de dimension21. Reformulation entiere plus
simple : H=3I-R=A-J/2 verifie
 ker H = ker A inter1-perp,
car Hx=0 donne0=w^t Hx=-12*sum x, et la reciproque est immediate.
Le fonctionnel somme est non nul sur kerA (il contient w), d'ou
nulliteH=nulliteA-1. Donc
 rangA=10 <=> multiplicite de12 dans4R egale11.
Sous A PSD, H a exactement une valeur propre negative (tester w,
et la perturbation est de rang1), dix positives et onze nulles.
Ainsi4R a une valeur propre>12, onze egales a12 et dix<12.
C'est une condition spectrale forte, PAS une preuve de rangA10 pour les
bords de nullite14, ni une exclusion de H-INV ou Conway.

OBSTRUCTION STRUCTURELLE A UN LAPLACIEN DIRECT. Les blocs geometriques sont
 K_+[L_y,L_z]=3/4*[y=z]+1/4*[z=y^1],
 K_+[L_y,R_z]=-1/2+3/4*[y=z]+1/4*[z=y^1],
 K_+[O_i,L_y]=K_+[O_i,R_y]=0.
Donc A[L_y,R_y]=-Gamma_+[L_y,R_y]-1/4<0, tandis que les entrees O-L/R
sont non positives. Les deux noyaux donnent, ligne par ligne,
 sum_z A[L_y,R_z] = -sum_i A[L_y,O_i] >=0.
Chaque ligne L_y du bloc L-R contient donc une entree strictement positive ;
de meme pour chaque colonne R_z. Au moins10 paires hors diagonale de A
sont positives, toutes dans L-R. Elles valent1/4 ou1/2, et correspondent
a un bloc original2x2 SANS ARETE, par la demi-integralite de Gamma_+.
A n'est donc jamais lui-meme un laplacien ordinaire a poids positifs.

L'analogue canonique de la correction a UNE droite ne marche pas non plus.
Garder w dans le noyau et ajouter un seul mode dans l'espace des deux
etoiles force la direction v, soit A+alpha*v*v^t, alpha>0. Or chaque
ligne L_y a somme d'adjacences Gamma_+ egale2 vers O+L. Parmi les huit
L_z non mates, au plus quatre entrees peuvent etre non nulles (pas0,5).
A une entree nulle, K_+=0 : la correction cree l'entree positive alpha.
Une congruence diagonale positive ne change pas ce signe. Ceci exclut
seulement cette construction canonique, pas toute transformation imaginable.

CONTROLES PROPRES. Geometrie K_+ exacte et identites de blocs ; support
fixe151 aretes/une composante. Une fixture rationnelle propre
 Gamma_+=d*d^t/136-v*v^t/10, d=(4,4,6^20),
est non negative, verifie Gamma_+ w=d, Gamma_+ v=-2v, et la congruence.
Elle n'est PAS un bord binaire/a demi-aretes, ni un graphe C1/C2.
Son spectre exact A est0^2,1^4,2^5,3^10,(42/17)^1 : rang20 et A PSD ;
rangH21. Elimination exacte par DomainMatrix ; le premier essai avec
elimination d'expressions generales a ete arrete car inutilement lent.
Aucun autre processus arrete, aucun processus restant, aucun germe du
pair lu ou re-audite. Code h_even_network.py ; artefact h_even_network.json.

### 15/10, suite792 : norme exacte du bloc mixte et filtres sur une moyenne

792 lu/acquitte. Claude distingue55 structures cassees (47 moyennes) qui
passent les deux blocs moyens positifs mais echouent par le couplage de U,
facteur commun annonce0,6691. Il demande une borne sur B en fonction des
40 paires cassees. Ces resultats sont acceptes, aucun lot re-audite.

IDENTITE PLUS DIRECTE, sans utiliser la connexite du reseau151. Fixer
Delta=Gamma-HGammaH, coefficients0,+1,-1. Soit b le nombre d'orbites
d'aretes NON ORIENTEES{e,h(e)} de taille2 avec exactement une arete
presente. Chacune contribue quatre carres1 a Delta, donc||Delta||F^2=4b.
Dans les bases de parite ORTHONORMALES, T_mixte=B=-Gamma_mixte et
 Delta=[[0,-2B],[-2B^t,0]]. Donc
 ||Delta||F^2=8||B||F^2,  ||B||F^2=b/2.
Si q compte plutot les paires d'orbites de SOMMETS dont le bloc2x2 est
casse, q<=b<=2q : q/2<=||B||F^2<=q. Ne pas confondre les deux comptes.

Pour un bloc original[[a,b],[c,d]], poser x=a-d,y=b-c. Les deux entrees
mixtes correspondantes valent-(x-y)/2 et-(x+y)/2. Leur cout est
(x^2+y^2)/2 : une orbite d'aretes cassee donne deux modules1/2 ; deux
donnent un module1 et un0. Les16 blocs binaires donnent4 couts0,8 couts1/2,
4 couts1. Pour une moyenne a demi-aretes FIXEE, les orbites cassees sont
exactement celles de moyenne1/2. La norme Frobenius est donc FIXEE ;
changer leurs orientations peut modifier les valeurs singulieres et
l'energie ponderee, mais pas cette norme.

Les relations d'etoiles donnent rangB<=20. Sous T PSD et rangA10,
B^t kerA=0 donne rangB<=10. Par la somme des carres singuliers,
 ||B||op^2 >= b/(2 rangB) >= b/20 >= q/20.
Ainsi40 cassures dans l'un ou l'autre sens donnent||B||F^2>=20 et
||B||op>=sqrt2 pour un candidat positif de rangA10. Cette borne seule
ne prouve pas que U est impossible : elle doit etre comparee a sa marge.

CAPACITE DE LA MOYENNE. Noter A',C' les deux blocs de U0 et N une base
de kerA. Eliminer les coordonnees N, auxquelles B est orthogonal, donne
la forme courte S sur rangeA :
 S=A'-A'N(N^t A'N)^+N^t A'.
Sous A',C' PSD et N^t B=0, U PSD equivaut a la positivite du bloc
[[S,-B],[-B^t,C']]. Donc B=S^(1/2) K C'^(1/2), K contraction. Si s_i,c_i
sont les valeurs propres decroissantes et r=rangB<=10,
 b/2=||B||F^2 <= sum_{i<=r} s_i*c_i.
Prendre r=10 donne une borne sure calculable depuis la seule moyenne.
Plus simplement, C'<=beta I donne b<=2 beta trS. Avec T0,U0 PSD,
beta=7 est toujours permis, soit b<=14 trS. Pour b>=40, trS<20/7 serait
donc un certificat d'impossibilite de TOUTES les orientations de la moyenne.
On n'affirme pas que cette inegalite rejette les47 moyennes du pair.

CERTIFICAT QUADRATIQUE SUR LES SIGNES. Pour une moyenne fixee,
B=sum_k epsilon_k B_k, epsilon_k=+-1, une variable par orbite cassee.
Les B_k sont orthogonaux pour Frobenius, chacun de norme carree1/2.
Avec les pseudo-inverses des blocs superieurs,
 H_kl=tr(A'^+ B_k C'^+ B_l^t).
Sous les conditions de portee de U, epsilon^t H epsilon est la norme
Frobenius carree de A'^{+1/2} B C'^{+1/2}. U PSD et rangB<=10 imposent
 epsilon^t H epsilon<=10.
Tout diagonal rationnel d avec H-diag(d) PSD donne une minoration
independante des signes par sum d. Si sum d>10, toutes les orientations
sont exclues, meme avant C1/C2. Un certificat bon marche est
d_i=H_ii-sum_{j!=i}|H_ij| (dominance diagonale) ; s'il ne depasse pas10,
il est INCONCLUSIF. Aucune enumeration2^b abordable n'est revendiquee,
aucun probleme quadratique general resolu.

OUTILS. h_mixed_energy.py fournit shorted_upper, orientation_energy_gram
(quatre produits par coefficient grace au support de B_k), diagonal_minorant.
Controles propres :16 blocs binaires, trois matrices binaires44 arbitraires
pour les facteurs4/8, une forme courte dont la trace passe de7 a2, et une
energie sur quatre canaux comparee exactement aux traces denses sur les16
choix de signes. Le minorant diagonal de cette fixture vaut17/4, donc
inconclusif au seuil10. Ces objets ne sont pas des bords C1/C2 ou des SRG.
Artefact h_mixed_energy.json. Aucun fichier du lot55 lu, aucune certification
du producteur refaite, aucun processus actif. ODD9, H-INV et C1 restent ouverts.

### 15/10, suite794/795 : reduction exacte des orientations et coupes de direction

794 puis795 lus/acquittes. Le trou795 a ete observe lors de l'envoi796 ;
aucune interrogation repetee d'une boite vide. Reponse796 : chemins absolus
vers ce depot et lab_exchange_2026-10-14. Les commits sont LOCAUX, pas
pousses sur le depot distant. h_mixed_energy.py importe maintenant les
modules de geometrie seulement dans report() ; les trois fonctions
reutilisables s'importent depuis l'export avec SymPy seul.

RETOUR NEGATIF ACCEPTE DU PAIR795. Sur ses47 moyennes, b40, rangA10,
Frobenius20. Capacite spectrale151,43 et trS30,67 : notre borne ne coupe
rien. Energie ponderee7,108<=10, mais norme operateur1,495>1, donc U
reste impossible pour les orientations observees. L'energie est concentree.
Les bornes diagonales essayees restent inconclusives. Les47 moyennes
appartiennent deja a une classe entierement enumeree : inutile de refaire
ce calcul ou de re-auditer les certificats. Aucun de ces fichiers lu ici.

PRECISION DE MODELISATION. Les fuites de B_k individuels dans un noyau
ne sont PAS une obstruction : leurs signes peuvent les annuler. Seules
les sommes N_gauche^t B=0 et B N_droite=0 sont requises. Projeter tous les
canaux puis relaxer les signes donne une borne necessaire sure, mais la
norme b/2 ne reste fixe dans la projection que pour les sommes satisfaisant
les equations de portee. Cette precision transmise dans796.

REDUCTION EXACTE. Pour une moyenne fixee, constituer la matrice rationnelle
R dont la colonne k vectorise N_gauche^t B_k et B_k N_droite pour tous
les noyaux requis (A,A' a gauche, C,C' a droite, ou blocs correctement
shortes). Les signes doivent verifier R epsilon=0. Une RREF fournit
 epsilon=L z,
ou les z sont des coordonnees LIBRES originales de epsilon, donc +-1.
Ce parametrage est exact avec la condition restante |(Lz)_i|=1.
Apres passage d'une equation homogene aux coefficients entiers primitifs,
une somme de coefficients impaire donne immediatement une contradiction.

Une ligne a deux termes a z_i+c z_j de L donne
 z_i z_j=(1-a^2-c^2)/(2ac).
Si ce nombre n'est pas +-1, aucun signe n'est possible ; sinon il fusionne
deux variables de signe, avec leur signe relatif. Iterer ces fusions peut
faire apparaitre d'autres lignes a deux termes. Ce n'est pas seulement une
elimination lineaire : exemple epsilon3=epsilon1+2epsilon2, dimension
lineaire2, force epsilon1=-epsilon2 et ne garde qu'une dimension de signe.
Les lignes a trois termes ou plus restent imposees explicitement.

Si d signes restent apres propagation, au plus2^(d-1) choix modulo inversion
globale suffisent. Cette inversion est exactement l'action de h sur le bloc
mixte pour la moyenne fixee. Le programme refuse l'enumeration au-dela de
d14 par defaut (8192 essais maximum). Ce n'est PAS une borne universelle
sur d, ni une enumeration abordable de toutes les moyennes. Pour40 signes
libres, le programme affiche2^39 essais et ne lance rien.

COUPES QUI VOIENT UNE DIRECTION. Pour toute paire de vecteurs rationnels
u,v, la positivite de U=[[A',-B],[-B^t,C']] impose, en testant(u,+-v),
 |2u^t Bv| <= u^t A'u+v^t C'v.
Le membre gauche est la valeur absolue d'une forme LINEAIRE en epsilon.
Effacer les denominateurs fournit deux inegalites entieres directement
utilisables par un solveur. Les directions peuvent provenir d'un vecteur
singulier flottant puis etre rationalisees : la validite de la coupe ne
depend d'aucune certification de ce vecteur comme vecteur propre.
Cela vise directement l'obstruction de norme operateur, que la norme
totale peut manquer. Une liste finie de coupes est seulement necessaire.

OUTIL AUTONOME : code/codex/h_orientation_kernel.py, fonctions
range_equations, reduce_sign_kernel, operator_direction_cut,
enumerate_reduced_signs. Artefact h_orientation_kernel.json. Les noyaux et
blocs moyens sont ceux certifies par le producteur, jamais recalcules ici.
Controles propres : annulation de deux canaux qui fuient chacun, parite,
fusion de signes, condition a trois termes non automatique, et48 petits
systemes compares a l'enumeration directe des signes. Une fixture
algebrique10D avec A'=C'=2I/3 et deux canaux a energie9/4<=10 mais norme
operateur3/2 ; les deux coupes |-3e1+3e2|<=4, |-3e1-3e2|<=4 rejettent
toutes ses orientations. Aucun de ces exemples n'est un graphe C1/C2.
Aucune nouvelle moyenne reelle exclue ; ODD9, H-INV et C1 restent ouverts.
Aucun processus actif, aucun calcul intensif lance pendant le jeu.

### 15/10, suite797 : famille de moyennes a40 cassures, au plus4096 orientations

797 lu/acquitte. Claude a trouve le module et confirme les conventions.
Nouveau fait combinatoire du pair accepte : ses40 cassures sont simples,
10 dans chacun des deux blocs internes L,R et20 croisees ; chaque support
interne est un cycle10. Aucune cassure n'implique les deux orbites O.
Aucun fichier du pair lu. Le resultat qui suit vaut pour TOUTE moyenne de
ce type, sans utiliser le rangA10 ou la dimension14 du noyau.

Les quatre relations d'etoiles connues, en base de parite, ont vecteurs
 pairs : (2,2,1_L,1_R) et (0,0,1_L,-1_R),
 impairs : (1,1,1_L,0_R) et (1,-1,0_L,1_R).
Comme les lignes/colonnes O de B sont nulles, elles imposent separement
les sommes de lignes ET de colonnes nulles dans B_LL,B_LR,B_RL,B_RR.
Une cassure simple donne toujours des entrees de module1/2 dans les deux
directions. Sur chacun des cycles10 internes, ces equations propagent un
signe autour du cycle : au plusUNE dimension par cycle, ou contradiction.
La position des mates a distance3 rapportee par Claude n'est pas necessaire
pour cette borne ; elle pourrait encore renforcer le filtre.

Soit D le support biparti des20 paires croisees, V son nombre de sommets
ACTIFS et c son nombre de composantes. Les sommes de lignes/colonnes de
B_LR donnent une matrice d'incidence bipartie, avec signes de colonnes,
de rang V-c. Les signes croises ont donc dimension lineaire au plus
20-V+c. Toute valence impaire est immediatement impossible, puisqu'une
somme impaire d'entrees+-1/2 ne peut etre nulle.

LEMME FINI. Un graphe biparti simple a20 aretes et degres actifs pairs
satisfait V-c>=9. Supposons V-c<=8. Chaque composante a au moins4 sommets,
donc il y a au plus deux composantes. Une seule aurait au plus9 sommets :
les bornes a*2floor(b/2) et b*2floor(a/2), a+b<=9, donnent au plus16
aretes. Deux composantes auraient au plus10 sommets au total, tailles au
moins4 ; les bornes biparties ordinaires donnent au plus4+9=13 aretes
(tailles4+6), ou6+6=12 (tailles5+5). Contradiction dans tous les cas.

BORNE : dimension totale <=1+1+20-V+c<=13. Choisir les coordonnees libres
parmi les signes ORIGINAUX, puis identifier epsilon et-epsilon (action de h),
donne AU PLUS2^12=4096 essais pour une moyenne fixee. Les autres conditions
|Lz|=1, C1/C2 et PSD sont encore a appliquer ; elles ne peuvent qu'enlever
des essais. Le nombre de moyennes differentes reste non borne ici.
Si toutes les valences croisees valent2, D est une union de cycles pairs
sur20 sommets : c<=5, dimension<=2+c<=7, soit au plus64 essais modulo h.
Cette hypothese plus forte n'est PAS deduite du message797 ni verifiee
sur ses47 moyens.

CODE : forty_simple_cycle_bound dans h_orientation_kernel.py reconnait
le type et fournit les bornes effectives. Nouvelle fixture abstraite :
cycles10 internes et support croise K4,6 prive d'un K2,2 (20 aretes,10
sommets actifs, tous degres pairs). Les quatre seules relations d'etoiles
donnent bien rang27, dimension13 ;4096 essais produisent552 solutions de
signes modulo h. C'est un temoin de l'optimalite de la borne de dimension
pour cette relaxation, PAS un bord C1/C2 ou un SRG. Un support de cinq
cycles4 croises donne la borne64. Executions environ une seconde, aucun
calcul lourd, aucun processus restant. Exports actualises.

### 15/10, cloture de ce tour : retour799, transmission800

799 lu/acquitte apres le trou de sequence observe a l'envoi800. Le pair
annonce ses140 classes newk2 completes en SAT, SANS certificat exporte :
404 structures PSD,14960 non PSD, toutes a couplages h-relies, aucune
cassee. Total avec les campagnes precedentes :287 classes completes ;
seule obj53 contient9408 structures cassees, aucune PSD. Ce bilan est
conserve comme resultat du producteur, sans re-audit ni transformation
en un certificat independant. Il n'y a pas de nouvelle moyenne en attente.

Observation structurelle du pair : un noyau h-invariant dont la classe
admissible est un singleton force Gamma=hGammah, puisque la conjugaison
preserve cette classe. Cela ne prouve pas l'unicite des classes encore
inexplorees. Les formes de relations paires u=-Phi g en cinquiemes pour
c22/c62/c42, ainsi que les variantes c55/c33, sont acceptees ; leur portee
reste celle des noyaux observes. Claude entreprend des marches dans des
groupes ne contenant pas h ; ne pas doubler cette recherche.

Transmission800 donne la preuve et l'outil de la borne4096, ainsi que64
sous l'hypothese supplementaire de valence croisee2. Cette borne est une
etape exhaustive abordable par moyenne du type defini, PAS une nouvelle
famille exclue, ni une enumeration du nombre de moyennes. L'ancien lot47
etait deja couvert par SAT. Aucun processus propre actif en fin de tour.

### 15/10, suite801 : obstruction de volume au passage de nullite13 a14

801 lu/acquitte. Faits nouveaux du pair acceptes, sans relance ni audit :
le sous-groupe G_N du cadre preserve chaque classe de noyau ; h est central,
donc les images par ce groupe d'une structure h-invariante le restent.
Les membres casses d'une meme classe ne viennent pas de ces images.
Survol213/287 classes : rapports |G_N|/|Aut| annonces1 dans25 classes,
2 dans119,4 dans32,96 dans deux classes rep006 et rep037. Ce sont des
statistiques observees, pas une necessite universelle de grande symetrie.
Marches sans h depuis c55 : milliers de visites PSD, nullites11 a14,
aucun couplage casse. KHOMOG autour hm_id_c22_HB_1, intersection initiale
12D :672 structures, enumeration annoncee complete en27s ; celles de
nullite14 (8 PSD,340 non PSD) sont h-reliees ; les cassees restent a12/13.
Claude teste une marche par projection sans groupe ni graine. Aucun de
ces fichiers producteurs lu ici.

FORMULATION EXACTE DU MUR, pour une moyenne FIXEE et sous positivite.
T=[[A,B],[B^t,C]], T0=(T+hTh)/2=diag(A,C). Comme T et hTh sont PSD,
 kerT0 = kerT inter hkerT.
Poser i=nulliteT0. Sur les supports positifs de A et C, une congruence
reduit T a [[I,K],[K^t,I]], K=A^-1/2 B C^-1/2. Ainsi T PSD equivalaut
a toutes les valeurs singulieres de K<=1, et
 nulliteT = i + nombre de valeurs singulieres de K exactement egales a1.
Donc, a i12 fixe, nullite13 requiert UNE saturation, nullite14 en requiert
DEUX. Ce n'est pas une deduction de positivite pour les cas non PSD du pair.
Si une classe KHOMOG n'impose qu'un sous-espace12 dans le noyau moyen,
i peut augmenter ; la formule doit employer sa valeur ACTUELLE.

COMBINER AVEC U. Shorter A',C' sur les supports de A,C, obtenant S,Q.
Ici S,Q doivent etre definis positifs sur ces supports. Un upper shorte
singulier demande d'abord une autre reduction de support ; aucune
conclusion du nouveau module n'est revendiquee pour cet usage hors contrat.
Sous les conditions de portee de T, U PSD equivaut au bloc shorte positif,
donc L=S^-1/2 B Q^-1/2 est une contraction. Ecrire
 L=P K R, P=S^-1/2 A^1/2, R=C^1/2 Q^-1/2.
Si K a au moins p valeurs singulieres1, la norme de sa puissance exterieure
d'ordre p vaut1. De K=P^-1 L R^-1 et ||exterieur^p L||<=1, on deduit
 produit_p_petites(sigma(P)) * produit_p_petites(sigma(R)) <=1.
Au carre, les alpha sont les valeurs generalisees de(A,S), beta celles
de(C,Q), en ordre CROISSANT :
  (alpha_1 ... alpha_p)(beta_1 ... beta_p) <=1.
Tout produit strictement superieur a1 interdit nulliteT>=i+p.
La condition p2 peut etre plus forte que p1 pour le mur13/14. Elle ne vise
PAS les47 anciennes moyennes de nullite14, pour lesquelles p0 suffit.

CERTIFICAT RATIONNEL. Pour t rationnel, l'inertie negative de A-tS compte
les valeurs generalisees strictement inferieures a t. Au plus j-1 directions
negatives certifient alpha_j>=t, y compris les egalites et multiplicites.
Quatre seuils rationnels certifies suffisent donc pour un produit p2>1,
sans isoler les racines algebriques. Les seuils peuvent etre proposes par
un calcul flottant, mais le certificat lui-meme est rationnel exact.

OUTIL : code/codex/h_nullity_volume.py, autonome SymPy. Fonctions
rational_inertia (pivots1x1 et2x2), certify_ordered_ratio_bounds,
certify_nullity_drop. Artefact h_nullity_volume.json. Exemple propre :
A=C=I2, S=diag(2,1/4), Q=I2. Plus petites valeurs alpha=(1/2,4), beta=(1,1).
p1 donne1/2, inconclusif ; p2 donne2>1, donc interdit deux saturations.
B=diag(1,0) produit pourtant T PSD avec une seule direction nulle et U PD.
Ajouter12 directions nulles communes illustre algebriquement13 permis,
14 interdit ; ce n'est PAS un bord Conway. Controles de18 congruences
rationnelles d'inertie connue, pivot diagonal nul, et seuil volontairement
trop haut refuse. Le premier lancement a rencontre une conversion bool
SymPy/int ; corrigee, les controles passent en moins d'une seconde.
Aucune moyenne reelle exclue, aucun processus actif, aucun calcul lourd.

### 15/10, suite803 : les cassures comme circulations par paire de composantes

803 lu/acquitte. Le pair rapporte des produits de volume faibles sur HB_1
(0,0067 ;0,0001 ; environ0) : aucun obstacle a la seconde saturation par
ce filtre. near_0 passe aussi ; kmilp_obj53_ambig a deja un bloc upper
negatif. Ces retours sont acceptes sans reexecution. L'enumeration KHOMOG
reste plus forte sur HB_1. Le cas upper shorte singulier exige la reduction
de support signalee ; aucun resultat d'exclusion n'en depend ici.

Le lemme de composantes du pair803 fournit la nouvelle entree : les
indicateurs de cote sont h-pairs ; quand ils sont dans le noyau global T,
ils forcent les comptes equitables. Une composante W de H_l ne contenant
pas m a indicateur pur sur L_W ; une composante Z de H_m ne contenant pas l
a indicateur pur sur R_Z. Poser B le bloc mixte de T dans la base de h.
Les equations B^t*kappa_W=0 et B^t*kappa_Z=0 se restreignent INDEPENDAMMENT
au rectangle L_W x R_Z. Les composantes actives contenant l'autre droite
ont des termes O supplementaires : le present critere ne s'y applique pas
automatiquement.

CONVENTION IMPORTANTE. Dans le bloc d'adjacence[[a,b],[c,d]], les deux
orbites d'aretes sont PARALLELE{a,d} et CROISEE{b,c}. 'Croisee' ici designe
ce type d'orbite, PAS le simple fait d'aller de L a R. Une orbite cassee
est un canal de signe epsilon. Une cassure SIMPLE en donne un, une DOUBLE
en donne deux, parallele et croise. Ils sont des aretes paralleles d'un
multigraphe biparti D sur les ORBITES de labels L_W,R_Z.

MATRICE D'INCIDENCE SIGNEE. Deux fois les contributions aux equations de
composantes valent(-epsilon,-epsilon) pour un canal parallele et
(-epsilon,+epsilon) pour un canal croise (premier bout dans L, second R).
Ce systeme admet des signes si et seulement si :
 1. toute valence active de D est PAIRE ;
 2. chaque composante connexe contient un nombre PAIR de canaux CROISES.
La condition caracterise uniquement ces equations, pas C1/C2 ou la PSD.

NECESSITE. Une somme impaire de signes ne peut etre nulle. Dans chaque
composante, sommer les equations sur L et sur R puis soustraire donne
sum_croises epsilon=0 : le nombre de canaux croises est pair. Le nombre
total d'aretes est deja pair puisque D est biparti et toutes les valences
sont paires.
SUFFISANCE CONSTRUCTIVE. Prendre un tour eulerien ferme dans chaque
composante. Fixer le premier signe et propager le suivant afin d'annuler
les deux contributions consecutives a chaque passage par un sommet.
La fermeture demande(-1)^E fois le produit des rapports de bouts=1.
E est pair, et le produit des rapports vaut(-1)^nombre_croises. La parite
paire garantit donc la fermeture ; tous les passages se compensent deux
a deux. Les visites multiples et les aretes paralleles sont permises.

DIMENSION EXACTE. Une dependance entre les lignes se propage par
 y_R=-s_e*y_L, s_e=+1 parallele,-1 croise.
Sur une composante, elle a dimension1 si CHAQUE cycle contient un nombre
pair de canaux croises, sinon0. Donc rang=V-c_bal et dimension du systeme
lineaire E-V+c_bal. Toute solution signe est determinee par au plus ce
nombre de signes libres, mais |Lz|=1 reste a imposer. Ne pas quotienter
independamment chaque composante pour le probleme global : C2/PSD peuvent
coupler leurs choix. Seul le retournement h de tous les signes est acquis.

NE PAS CONFONDRE LES DEUX PARITES. La solvabilite requiert seulement une
parite totale PAIRE par composante ; le rang baisse d'une unite seulement
si TOUS ses cycles ont parite paire. Deux carres ayant chacun un canal
croise, et PARTAGEANT un sommet, ne sont pas orientables separement mais
leur union l'est : leurs defauts se compensent au sommet commun. S'ils
sont disjoints, l'union reste impossible. De meme, une cassure double seule
est impossible, mais deux cassures doubles partageant un sommet peuvent
satisfaire les equations. C'est un mecanisme precis de cooperation des
cassures ; l'interdiction de chaque cycle impair serait FAUSSE.

OUTIL AUTONOME : code/codex/h_component_circulation.py, classify_tile.
Il fournit l'obstruction, le rang exact par propagation de signes, et un
temoin par tour eulerien quand les equations sont faisables. Exemples
propres : carre parallele, carre impair, deux carres impairs joints ou
separes, une ou deux cassures doubles.32 petits multigraphes supplementaires
compares a une enumeration litterale des signes et a leur rang rationnel.
Tout passe en moins d'une seconde. Artefact h_component_circulation.json.
Aucun fichier de graphe du pair lu ; aucune nouvelle famille C1 exclue.
Ce critere est un filtre sur les moyennes et une construction des seules
orientations equitables du rectangle, PAS la construction d'un SRG.

### 15/10, suite805 : defauts de conjugaison et tests de couplage de taille au plus4

805 lu/acquitte. Le pair fournit l'involution cachee exacte g=h(4 6) de
HB_1, qui ne preserve pas les mates. Son defaut D=K-gKg a rang2, spectre
+-1, et ses noyaux observes sont g-invariants (11 pairs,2 impairs).
Ces donnees sont acceptees sans lire/re-auditer HB_1. Claude poursuit les
marches a froid G1'' contenant h(4 5) mais pas h, avec G1 temoin. Aucun
doublement de ces recherches par Codex.

GENERALISATION GEOMETRIQUE. Pour TOUTE involution p des10 lettres
exterieures, g=(0 1)(2 3)p agit librement sur les44 labels, meme si p ne
preserve pas les mates. Soit M le matching des mates exterieurs et
M'=pMp. Si Gamma est g-invariant, les seuls termes geometriques changes
sont les incidences de mates exterieurs. Sur les40 labels(s,y),
 D=K-gKg = (1/8) J4 tensor(M-M'),
et D est nul dans les lignes/colonnes des quatre labels O. On a
 gTg=T+D.
La correction de U est L=(4*intersection-mateinc+2)/15, d'ou
 gUg=U-(8/15)D.
Ce ratio est different du simple signe oppose dans les parites preservant
le cadre ; les tests doivent l'utiliser.

RANG GEOMETRIQUE. L'union des deux matchings se decompose en cycles
alternes2s, avec s1 pour une arete commune. M-M'=M(I-MM') ; MM' est le
produit de deux s-cycles sur chaque composante. Le noyau y a dimension2,
donc rang2s-2. Si c est le nombre de composantes, rangD=10-2c.
Puisque gDg=-D, en parite g orthonormale
 D=[[0,E],[E^t,0]], rangE=5-c<=4.
T_mixte=-E/2, U_mixte=4E/15 : ces deux couplages sont FIXES par la
geometrie, independants du graphe Gamma g-invariant.

CLASSIFICATION FINIE DE LA GEOMETRIE. Les945 matchings M' sur10 lettres
se repartissent selon les7 partitions de5. Comptes par rangE0,1,2,3,4 :
1,20,140,400,384. Chaque type se realise par une involution p, obtenue
par reflexion sur chacun des cycles alternes. Les controles symboliques
ont porte sur ces7 representants, sans aucun graphe fourni par le pair.
945 compte des matchings geometriques, PAS des bords, moyennes ou SRG.

TEST EXACT DU COUPLAGE. Factoriser E=X Y^t, X,Y de rang colonne r<=4,
rationnellement. Les diagonales A,C de T sont supposees PSD ; elles
doivent contenir X,Y dans leurs images. Poser G_A=X^t A^+ X,
G_C=Y^t C^+ Y. Ces metriques sont definies positives en taille r. Alors
 T PSD ssi R_T=4 G_A^-1-G_C PSD.
De meme avec les diagonales A',C' de U et leurs conditions de portee,
 U PSD ssi R_U=(225/16) G_Aprime^-1-G_Cprime PSD.
Preuve par complement de Schur sur les supports positifs, pour un bloc
mixte aXY^t : le residu est (a^2 G_A)^-1-G_C. Les autres directions du
complement restent strictement positives. Les tests diagonaux restent
necessaires, mais le couplage est EXACTEMENT reduit a une matrice r<=4.
Pour le swap non mate simple de805, r1 : deux inegalites scalaires.

NULLITE ET LIMITE DU DIAGNOSTIC. Sous positivite,
 nulliteT = nulliteT_moyen + nulliteR_T.
En particulier N=gN ssi R_T est strictement positif (cas r0 compris).
L'observation N=gN chez HB_1 signifie donc AUCUNE saturation du couplage :
sa nullite13 est DEJA celle des blocs moyens (11 relations paires,2 impaires).
Le defaut de rang2 ne suffit pas, seul, a forcer une relation de moins.
Deux exemples algebriques propres avec le meme rang et les memes rapports
T/U montrent les deux voies possibles vers14 :
- moyenne de nullite14, residuT=3>0, residuU=209/16>0 ; noyau g-invariant ;
- moyenne de nullite13, residuT=0, residuU=209/16>0 ; une saturation ajoute
  une direction nulle et le noyau n'est pas g-invariant.
Dans les deux cas, nulliteT14/nulliteU4, mais les matrices ne sont PAS des
adjacences binaires et n'imposent PAS toute la geometrie C1/C2. Elles ne
refutent ni la campagne du pair ni un theoreme specifique aux graphes.
Pour demontrer le plafond13, il faut donc encore des contraintes sur la
nullite des moyennes et la saturation du petit residu.

OUTIL : h_geometric_defect.py, fonctions geometric_defect (ordre des labels
parametrable), rank_factor, metric_on_range, coupling_residual. Les
fonctions centrales ne dependent que de SymPy. L'export report utilise
notre helper d'inertie deja exporte. Artefact h_geometric_defect.json.
Controles :945 matchings,7 types exacts, ratio lower/upper, deux exemples
abstraits de nullite14, trois petits blocs a couplage sous-critique, critique,
sur-critique, et une obstruction de portee. Export execute en moins d'une
seconde. Aucun processus actif ; aucune famille C1 exclue.

### 15/10, suite807 : un carre force normalise les96 interfaces G1''

807 lu/acquitte : Claude a26760 structures admissibles G1'' en600s,
enumeration incomplete, aucune PSD ; marches a froid jusque G1 temoin
inconclusives (max nullite10). Il projette les cubes sur M0,M2. Aucun
doublement de cette enumeration. Sa correction est acquise : M0 contient
45 ; c'est M2 ne contenant pas45 qui briserait H-MATCH dans cette famille.

NOUVEAU LEMME. Poser a=(01)M, b=(23)M'', avec M tous les flips exterieurs
et M'' sans45. F={04,05,14,15} est fixe point par point par b. M0 contient
45, donc M1 aussi. C1 impose un unique voisin de chaque sommet de F dans
l'autre etoile de l ; ce voisin doit etre b-fixe, donc encore dans F.
Le matching04-15,05-14 donnerait deux voisins communs a04 et14, qui ont
deja la lettre4 en commun : C2 l'interdit. F induit donc le carre
04-05-15-14-04. C1 exclut toutes ses aretes vers O et les autres labels L.

POSITIVITE UTILISEE. Pour kappa=1_F, kappa^t T kappa=0. Sous T>=0,
T*kappa=0. La somme des quatre termes K vaut-1 pour les labels R2/3,y
avec y=6..13, et0 pour tous les autres labels hors F. Donc chacun des
16 premiers labels a EXACTEMENT un voisin dans F, tous les autres zero.
Cette reduction vise les structures PSD ; elle n'est pas imposee aux
structures simplement admissibles sans justification spectrale.

NORMALISATION. Les deux orbites non triviales de a sur F sont{04,15}
et{05,14}. Chacune des quatre orbites regulieres R d'une paire exterieure
6/7,...,12/13 s'attache a une de ces deux orbites, avec deux orientations.
Chaque sommet de F doit avoir deux voisins dans R2 et deux dans R3 :
exactement deux paires s'attachent a chaque orbite. Total binom(4,2)*2^4=96.
Le groupe C2 wr S4 (ordre384) des quatre paires agit TRANSITIVEMENT sur
ces96 interfaces, tout en preservant a,b, les mates et h. On peut donc
fixer une interface, y compris pour chercher un contre-exemple H-MATCH.
Ce facteur porte sur les interfaces etiquetees, pas sur le temps SAT.

TEMOIN CANONIQUE. Pour y=6,8, les voisins dans F de R2y,R2(y^1),R3y,
R3(y^1) sont respectivement04,15,15,04. Pour y=10,12, ils sont05,14,14,05.
Ainsi20 aretes incidentes a F sont presentes (4 internes+16 attaches)
et146 absentes. C2 force huit absences supplementaires : dans chacune
des etoiles R2 et R3, les paires d'indices6-8,7-9,10-12,11-13, puisqu'un
voisin dans F et la lettre centrale sont deja communs. Les matchings M2
invariants possibles passent331->284 ; ceux ne contenant pas45 passent
250->216. M0 a encore81 choix abstraits. Les produits23004 et17496 sont
des bornes de CHOIX DE MATCHINGS avant les autres contraintes, pas des
nombres de cubes SAT faisables ni des estimations de temps.

ELIMINATION EXACTE DU CARRE. Les caracteres00,10,01,11 de G1'' ont les
dimensions12,12,10,10. Les40 labels hors F forment10 orbites regulieres,
donnant dix directions par caractere. Sur F, les modes normalises par2
sont kappa=(1,1,1,1)/2 et q=(1,-1,-1,1)/2 de caractere00 ; r=(1,1,-1,-1)/2
et t=(1,-1,1,-1)/2 de caractere10. Les blocs sur ces quatre modes sont
T_F=diag(0,5,5/2,5/2), U_F=diag(14/3,2,10/3,10/3).
Le couplage T de kappa est nul ; tous les autres couplages sont FIXES
par l'interface. Schur elimine donc F : pour chaque caractere chi, avec
Gamma_chi=V_chi^t Gamma V_chi/4, les tests EXACTS sont
 T_offset_chi-Gamma_chi >=0 et U_offset_chi+Gamma_chi >=0,
quatre matrices10x10 de chaque sorte. Les offsets sont exportes. RangT
vaut3+somme des rangs reduits ; nulliteT vaut1+somme des nullites reduites.
Donc la cible locale rangT<=30 devient somme<=27. Si l'on impose aussi
la borne GLOBALE acceptee rang_F7(8T)<=28, la cible devient somme<=25 :
les pivots5,5/2 et tous les denominateurs des offsetsT (ppcm10) sont
inversibles modulo7. Cette borne globale ne decoule pas du seul PSD local.

OUTIL AUTONOME g1_twist_square.py : square_template(labels) pour les
assignations, geometry_reduction(labels) pour les bases/couplages/offsets,
compressed_adjacency pour les quatre blocs de Gamma en1600 lectures
entrees au lieu d'une multiplication44x44. Le producteur fournit son
ordre de labels et l'invariance ; aucun audit de ses graphes. Controles
propres : orbite96, lignes C1 du carre, contraintes C2 deja decidables,
decomposition exacte, projection sur une matrice algebrique invariante,
comptes de matchings abstraits. Tout termine en moins d'une seconde.
Artefact g1_twist_square.json ; lemme transmis par808, export ensuite.
Cette reduction ne prouve pas encore H-MATCH ni l'exclusion de G1''/C1.

### 15/10, suite809 : quatre grilles interdites et c_m<=3 dans le cas casse

809 lu/acquitte apres le saut de sequence du message810. Claude trouve
les26811=81*331 couples M0,M2 admissibles, mais aucun de quatre cubes
sondes n'est termine apres150s ;10454 a14566 structures par cube, aucune
PSD. Cela indique un mauvais cout brut ; extrapoler3e8 structures n'est
pas un plancher prouve par quatre sondes. Il impose maintenant les
relations des composantes et notre interface normalisee. Pas de doublon.

NOUVELLE EXCLUSION LOCALE (envoyee811). Pour P={y,y^1}, y=6,8,10,12,
R_P={2y,2y^1,3y,3y^1} est une orbite reguliere de G1''. Son degre interne
d_P est donc constant et entier. Dans T, le mode1_RP/2 a norme2-d_P.
Le mode q_F=(04-05-14+15)/2 a norme5 ; leur couplage vaut+-1 puisque
tous les sommets de R_P s'attachent a la meme orbite{04,15} ou{05,14}.
Le mineur PSD2x2 impose5(2-d_P)-1>=0. Donc d_P<=1. C'est aussi la
diagonale du Schur precedent :9/5-d_P>=0. Aucune de ces quatre paires
ne peut ainsi former une grille avec la droite m.

COUPES LINEAIRES : pour chacun des quatre y,
 Gamma[2y,2y^1]+Gamma[2y,3y]+Gamma[2y,3y^1]<=1.
Ces coupes sont nouvelles et distinctes des huit zeros C2 deja exportes.
Elles contraignent notamment les couplages croises quand M2 contient
une paire mate. square_template exporte les trois indices par coupe.

CONSEQUENCE POUR LES CUBES. Les seules grilles possibles de m avec les
six autres droites du cadre sont l (orbite O) et P45. Donc g_m<=2 et
c_m<=floor((6+g_m)/2)<=4, chaque composante non singleton de H_m consommant
au moins deux de ses six paires. Dans le cas M2 ne contenant pas45,
P45 n'est pas une grille non plus : g_m<=1, donc c_m<=3. Toute la
sous-famille G1'' brisant H-MATCH avec c_m>=4 est donc exclue SOUS T>=0.
C'est une exclusion de sous-famille, pas l'exclusion de G1'' ni de C1.
Code/artefact g1_twist_square mis a jour et exportes, controles propres
des quatre coefficients de Schur9/5 et des couplages+-1, moins d'une seconde.

### 15/10, suite812 : coupes PSD entieres et distinction Farkas / preuve binaire

812 lu/acquitte. Claude a integre interface, comptes et coupes d_P<=1
dans enum_cubes.py et psd_milp_group.py. Ses six cubes sondes restent
incomplets avec5700 a10400 structures en120s, aucune PSD ; plus de45000
cubes raffines en600s, encore incomplet. Resultats acceptes sans audit.
Il passe a HiGHS sur254 orbites de paires, avec C1/C1', C2 paresseux et
coupes de directions propres negatives de T/U ; G1 est son temoin.
Question du pair : les blocs10 permettent-ils un certificat exact ?

REPONSE813. Oui pour justifier les coupes, mais un verdict MILP n'est
pas automatiquement un certificat de Farkas a la racine. Pour un modele
affine rationnel M(x)=C+sum_j x_j B_j, T comme U, tout q rationnel donne
 sum_j (-q^t B_j q)x_j <= q^t Cq.
q n'a PAS besoin d'etre propre. Une direction numerique arrondie vers un
vecteur entier donne une coupe valide ; seule sa capacite a separer le
candidat doit etre controlee exactement. Sinon raffiner la direction,
ou eliminer rationnellement le petit bloc pour trouver un temoin negatif.
Eliminer les denominateurs et diviser par le pgcd POSITIF donne une ligne
entiere equivalente meme sur les reels. Aucune coupe n'est arrondie en
une inegalite plus forte non justifiee.

NOUVEL OUTIL psd_exact_cuts.py, autonome SymPy : negative_direction,
psd_cut, separate et adjacency_psd_cut. L'elimination exacte conserve les
vecteurs de congruence. Pivot negatif : le vecteur de base courant est
un temoin. Pivot nul avec hors-diagonale b non nulle : pour l'autre
diagonale c, f_j-(c+1)/(2b)*f_i a norme-1. Pivot nul avec ligne nulle :
direction de noyau ; les autres pivots sont positifs. Les valeurs
quadratiques rationnelles negatives, meme -1/1000, ne sont pas tronquees.
Les flottants sont refuses dans les donnees exactes ; on peut fournir
une direction arrondie explicitement en entiers.

RELEVEMENT DES PETITS BLOCS. g1_twist_square.py ajoute
lift_schur_direction(reduction,side,chi,q). Si V est la base des dix
orbites hors F, f_k les modes non normalises de F, c_k leurs couplages
et d_k leurs diagonales positives, poser
 w=Vq-sum_k f_k (c_k q)/d_k.
Le mode kappa de diagonaleT nulle n'intervient pas, son couplage est nul.
Avec nos normes de colonnes2, w^t M w=4 q^t M_reduit q. Ainsi un temoin
negatif10 se releve EXACTEMENT en un temoin rationnel44. La coupe finale
w^t M w>=0 est une coupe PSD ordinaire valide dans l'espace original,
meme sans invoquer l'interface pour sa validite. L'interface garantit
qu'elle separe le candidat normalise. full_geometric_offsets fournit
3I-K et4I-L. adjacency_psd_cut somme directement les2*w_i*w_j sur chaque
orbite d'aretes, avec signe-1 pour T et+1 pour U : pas besoin de construire
254 matrices de coefficients44x44. Le producteur conserve ses variables
fixees du carre avec leurs equations exactes dans le modele.

FORMAT DE PREUVE. Pour Ax<=b rationnel, un seul lambda>=0 avec lambda^t A=0
et lambda^t b<0 est une preuve complete d'infaisabilite LINEAIRE. Mais
2x=1 avec x binaire fournit un contre-exemple elementaire a l'idee qu'un
tel certificat existe pour toute infaisabilite MILP : x=1/2 est faisable
sur les reels. Le module propose alors un format fini : noeud split j,
enfants zero et one, ajoutant x_j<=0 ou-x_j<=-1 ; toutes les variables
sont binaires. Chaque feuille porte des multiplicateurs Farkas exacts
sur les contraintes globales, bornes0/1 et branches de son chemin.
La couverture et les contradictions sont exactes. Il faut fournir le
certificat : l'outil ne reconstruit PAS l'arbre de HiGHS, ni les sources
de contraintes arbitraires. Chaque ligne doit garder sa provenance valide
(C1, C2, normalisation, direction PSD, etc.) dans une preuve complete.

Un verdict flottant suivi d'une rationalisation des coupes ne suffit pas :
il faut demontrer l'infaisabilite du systeme EXACT obtenu. L'outil ne donne
aucune borne abordable sur la taille de l'arbre ou le nombre de coupes.
Controles propres : petit negatif rationnel, pivot nul non diagonal,
matrice PSD singuliere, congruence10x10 indefinie, separation affine,
certificat Farkas racine, arbre binaire a deux feuilles, quatre entrees
invalides rejetees. Huit identites de relevement T/U x quatre caracteres
sur une matrice algebrique invariante propre. Artefacts psd_exact_cuts.json
et g1_twist_square.json ; executions autour d'une seconde. Aucun germe,
cube ou verdict du pair re-audite. Pas de nouvelle exclusion de G1''/C1.

### 15/10, suite815 : projection exacte de C2 et certificats a variables mixtes

815 lu/acquitte. Claude annonce70 iterations/384 coupes PSD pour G1'',
sans verdict, et50/252 pour le temoin G1, encore sans structure PSD.
Il a remplace C2 paresseux par sa linearisation exacte : auxiliaires
continus y_ijt>=x_it+x_jt-1, somme_t y_ijt<=2-s-x_ij, avec nonnegativite.
10668 colonnes continues. Ses cubes M0,M2 sont un decoupage envisage,
pas une campagne au cout demontre abordable. Aucun calcul du pair repris.

NOUVELLE ELIMINATION (message816). Pour une paire i,j, poser e=x_ij,
s=nombre de lettres communes, L_t=x_it+x_jt et c=2-s. Les seules bornes
inferieures y_t>=0,y_t>=L_t-1 ont pour minimum max(0,L_t-1). Toutes les
apparitions dans les sommes C2 sont a coefficients positifs. Il existe
donc des auxiliaires ssi
 e+sum_t max(0,L_t-1)<=c.
Pour x dans[0,1], ces minima sont aussi<=1 : des bornes y<=1 ne changent
pas la projection. Les auxiliaires identiques sous le groupe ont la meme
forme L_t, et peuvent etre regroupes avec leur multiplicite entiere m_t.
Cette projection est EXACTE sur la relaxation continue, pas seulement
sur les affectations binaires. Elle concerne ces auxiliaires et ces
contraintes ; des contraintes supplementaires arbitraires sur y ne sont
pas supposees dans cette equivalence.

SEPARATION COMPLETE. La somme de max est le maximum sur les sous-ensembles W
de la somme des L_t-1 selectionnes. Pour tout W, la coupe equivalente est
 e+sum_{t dans W} m_t L_t <= c+sum_{t dans W} m_t.
Au point courant, prendre tous les termes L_t>1. Une seule passe sur
les termes suffit pour produire une coupe la plus violee ou prouver
qu'aucune coupe C2 de cette paire n'est violee. Il n'est pas necessaire
d'enumerer les2^42 sous-ensembles. Cela ne borne pas le nombre d'iterations
du solveur et ne garantit pas une acceleration ; la relaxation obtenue
apres separation complete a exactement la meme force que l'etendue.

CERTIFICAT DE CHAQUE COUPE. Ajouter une fois e+sum m_t y_t<=c, m_t fois
L_t-y_t<=1 pour les termes selectionnes, et m_t fois-y_t<=0 pour tous
les autres. Les coefficients de TOUS les auxiliaires s'annulent. Les
multiplicateurs entiers nonnegatifs sont exportes avec la coupe. C'est
une justification courte utilisable dans une preuve d'infaisabilite.
La selection de W peut venir d'un calcul flottant sans invalider la
coupe : tout W est valide ; seule la certification de la separation
complete exige une comparaison exacte au point rationnel courant.

OUTIL c2_projected_cuts.py, bibliotheque standard seulement.
models_from_edge_orbits(labels,orbits) construit les formes dans l'ordre
des variables et labels du producteur. Toutes les paires doivent etre
couvertes, y compris les variables fixees par des equations ; les formes
C2 identiques sont fusionnees par leurs coefficients effectifs, sans
supposer une action de groupe non fournie. separate_all parse une fois
le point rationnel et renvoie toutes les paires violees ; subset_cut
permet aussi une selection externe. Aucun graphe du pair lu.

CERTIFICAT MIXTE. Si Claude conserve la formulation etendue, seules les
254 variables d'aretes sont binaires. Le nouveau mixed_binary_tree_certificate
de psd_exact_cuts.py recoit explicitement leurs indices ; les autres
variables restent continues et leurs bornes sont dans les lignes globales.
Les feuilles Farkas doivent annuler les colonnes binaires ET continues.
Ne jamais traiter les10668 y comme des bits pour conclure sur le modele
mixte. Les lignes creuses sont maintenant acceptees avec n_variables
explicite ; bornes et branches sont creuses pour eviter de remplir de
grandes matrices. binary_tree_certificate reste l'interface tout-binaire.
Cette infrastructure consomme une preuve ; elle ne tire toujours pas un
certificat d'un seul statut HiGHS et ne borne pas la taille de l'arbre.

CONTROLES PROPRES :486 points fractionnaires compares a tous les
sous-ensembles dans deux petits modeles ; multiplicites et variables
alias ;72 affectations binaires de quatre labels comparees directement
a C2, avec et sans egalites de variables. Identite des multiplicateurs
elimnant y. Certificat mixte pour x binaire,y continu,y=x,2y=1 : deux
feuilles exactes, et rejet d'un branchement sur y. Aucune structure SRG
construite ou exclue. Artefacts c2_projected_cuts.json et psd_exact_cuts.json,
exports portables correspondants ; calculs courts, pas de processus actif.

### 15/10, suite818/819/821 : exclusion de toute la famille locale Z5-hM

818/819/821 lus et acquittes. Claude818 annonce G1'' MILP/SDP encore
inconclusif, sans candidat PSD meme dans le temoin G1. Il garde ses
auxiliaires C2 continus : notre projection n'est pas implementee chez lui,
aucun gain de temps mesure. Nouvelle question : pourquoi la famille
<z,hM>, z=(4 6 8 10 12)(5 7 9 11 13), h=(01)(23), M=(45)...(12 13),
plafonne-t-elle a nullite9 dans son echantillon ? Claude819 donne un cube
complet9024 structures/4PSD nullite9, c=(6,2), noyau entierement constitue
des relations de cote. Claude821 :9/25 cubes finis,130856 structures,
80PSD max9 ; sous-famille FORCE_TM complete26340/16PSD max9, c=(2,6).
Ces resultats sont acceptes. Aucun de ses graphes ou enumerations relance.

RESULTAT NOUVEAU (envoye822). Sous C1,C1',C2 et T,U PSD, tout bord44
LOCAL invariant sous <z,hM> a nullite_Q(T)<=14. Si sa nullite est14,
rang_F7(8T)>=29. Avec les conditions GLOBALES necessaires deja etablies
rang_Q(T)<=30 et rang_F7(8T)<=28 (L4/L23/L22, rappelees par LAB774),
aucun bord de CETTE FAMILLE LOCALE ne se prolonge en un Conway99.
Ni z ni hM n'ont besoin de s'etendre en automorphismes du graphe99.
Ce resultat n'exclut pas C1 en general et ne prouve PAS le plafond LOCAL9,
ni l'absence de relations mixtes. Il exclut aussi les candidats locaux
de nullite14 qui echappaient eventuellement a la campagne du pair.

PARAMETRAGE COMPLET. Les quatre labels O={02,03,12,13}, fixes par z,
forment obligatoirement un C4 : dans chaque etoile, les deux labels
fixes ne peuvent etre apparies a une orbite de taille5. C1 sature alors
leurs besoins et interdit toute arete entre O et les40 autres labels.
Noter e_i=4+2i, o_i=5+2i, i modulo5. Le matching de l'etoile0 est
e_i--o_(i+a). Celui de1 est l'image par M, donc le decalage oppose.
Entre0 et1, le matching est soit D_s=diag(z^s,z^-s), soit M lui-meme.
C'est exhaustif : une permutation des deux orbites5 commute avec z,
et l'invariance hM donne M R^* M=R. Dans le cas croise cela impose les
deux decalages nuls. Le choix M,a=0 est interdit par C2 (deux voisins
communs plus une lettre commune). Memes parametres pour2 et3.
Les deux blocs croises libres B=A02,C=A03 sont binaires circulants,
chacun a sommes de lignes et colonnes2. A13=M B M et A12=M C M.

DECOMPOSITION EXACTE. L'espace z-trivial a dimension12. Les autres
32 dimensions se decomposent en deux blocs4x4 sur Q(zeta5), selon
la parite de g=hM. Avec f=(1,-1,1,-1),
 T+=3I-Gamma+-J/2, T-=3I-Gamma--f*f^t/4 ;
 U+=4I+Gamma+-J/5, U-=4I+Gamma--f*f^t/3.
Les couplages de Gamma sont B+C*M et B-C*M. Les diagonales internes
sont explicites en zeta^a et zeta^s. Pour 2T+, la diagonale scalaire
est5 et l'oppose de l'entree hors diagonale vaut1+2zeta^a+2zeta^s
dans le typeD ; dans le typeM, ce sont3 et1+2zeta^a. Ce bloc2x2 est
defini positif sauf D,a=s=0 (inegalite triangulaire, egalite unique).
Pour4T-, les diagonales sont11 ou15, les hors-diagonales ont module
au plus9 ou5 : ils sont TOUJOURS definis positifs.

EXCLUSION ANALYTIQUE DU CAS DOUBLE GRILLE (message820, z non necessaire).
Deux diagonales+ singulieres signifient cinq grilles exterieures de
chaque cote, donc c_l=c_m=6 avec O. Leurs indicatrices sont dans kerT.
Cela force aucune arete entre les grilles L_i,R_i, et un matching parfait
entre L_i,R_j pour i!=j. hM agit antipodalement sur chaque C4 ; le
matching commute donc aux antipodies et est un automorphisme du C4.
Sur les dix modes damier normalises (1,-1,-1,1)/2, la restriction U
est [[2I5,B],[B^t,2I5]], avec B_ii=0 et B_ij=+-1 sinon. Les offsets
geometriques s'annulent sur ces modes (incidences de lettres nulles).
Positivite =>BB^t<=4I ; sa diagonale vaut4, donc BB^t=4I. Mais deux
lignes ont TROIS positions communes : produit scalaire impair, impossible.
Cette sous-famille est donc exclue sous hM seul. Si une seule diagonale+
est singuliere, echanger les deux droites pour utiliser la non singuliere.

MINEURS FINIS SUR Q(zeta5). Avec une diagonale gauche2x2 inversible,
rang du bloc4x4 <=2 equivaut a l'annulation du complement de Schur2x2.
Premier filtre : ses deux diagonales (mineurs3x3) ; second : hors-diagonale.
Chaque colonne+ est deux polynomes de coefficients0,1,2, de masse totale4
(une somme B+C*M). Chaque colonne- a au plus2 coefficients+1 et2
coefficients-1 parmi ses10 positions (une difference B-C*M). Ces domaines
sont des SUR-ENSEMBLES exhaustifs des blocs binaires et tiennent en615
ou1351 colonnes. Arithmetic dans Z[zeta5], base1,z,z^2,z^3, sans flottants.

Secteur+ :128 colonnes possibles de chaque cote,304 blocs de rang2,
3152 relevements B,C binaires avec les sommes requises. C1' rejette720,
C2 rejette1912, il reste520. Tous ont un vecteur ENTIER q negatif :
416 pour15U,104 pour8T. Les vecteurs ont ete trouves initialement par
direction numerique arrondie, MAIS le certificat et sa reproduction
n'utilisent que q^t M q entier strictement negatif, sans tolerance.
Aucun verdict flottant n'entre dans la preuve. Chaque vecteur est associe
au SHA256 des44 lignes binaires et a sa valeur quadratique exacte.
Secteur- :32 colonnes possibles de chaque cote, AUCUN bloc4x4 de rang2,
avant tout test PSD. Les deux nullites cyclotomiques a,b valent donc0 ou1.

QUOTIENT TRIVIAL. Poser epsilon_l,epsilon_m=+1 pourD,-1 pourM, et
t,w dans{-2,0,2} les comptes signes exterieurs dans B et C. Les tests
exacts12x12 T/U laissent14 des36 quadruplets. Leur nullite nu0 est5 ou6.
Les deux cas nu0=6 sont epsilon_l=epsilon_m=+1, (t,w)=(2,0) ou(0,2).
Par conjugaison galoisienne, null_Q T=nu0+4a+4b<=14. Une completion
Conway exige nullite>=14 : donc nu0=6,a=b=1. Echanger2,3 normalise
les deux cas : B a comptes diag(2,2), C a les quatre comptes egaux a1.
Cette permutation commute avec z et hM. Le secteur z-trivial a alors
rang exactement5 surF7 (et6 surQ).

OBSTRUCTION MODULAIRE CIBLEE. Phi5 est irreductible surF7 car7 est
d'ordre4 modulo5. La decomposition par z et hM reste inversible mod7 :
ordre10, facteurs2,4,5,8,15 tous inversibles. Les rangs des deux secteurs
non triviaux contribuent donc4 fois leur rang surF_(7^4).
Reprendre les MEMES equations de Schur, modulo7, dans le quotient nu0=6 :
 - secteur+ :88 colonnes de chaque cote, AUCUN bloc de rang<=2 ;
   la seule diagonale singuliere reste le cas grille deja traite ;
 - secteur- :212 colonnes de chaque cote,16 blocs de rang<=2 ;
   seulement8 relevements binaires B,C ont les comptes normalises.
Les huit violent C1' : un label a3 voisins dans une etoile exterieure
dont le plafond est2. Les huit petites violations sont exportees.
Ainsi chaque rang cyclotomique mod7 est>=3, et le rang44 est
 5+4*3+4*3>=29,
contraire au plafond GLOBAL28. C'est une nouvelle exclusion de famille,
pas une nouvelle demonstration des resultats globaux utilises.

ARTEFACTS. code/codex/z5_hm_rank_obstruction.py, bibliotheque standard,
data/codex_local_global_20261015/z5_hm_negative_certificates.json (520
vecteurs entiers), z5_hm_rank_obstruction.json (preuve detaillee, compte
des cas, quotient, huit violationsC1'). Reproduction complete4,6s.
Trois tests propres comparent les formules cyclotomiques aux produits
exacts sur44 labels, typesD/D,M/D,M/M ; tous passent. Exports portables
codex_z5_hm_* dans lab_exchange_2026-10-14. Pas de processus actif, pas
de graphe du pair lu, pas de doublement de sa campagne par cubes.

Suite823 : Claude annonce17/25 cubes complets avec plafond9 ; sous-famille
t=(12,12) complete4788 structures,0PSD. Resultats acceptes sans verification.
Il demande les520 graphes et le traitement de la diagonale singuliere.
Le fichier des certificats contient maintenant chaque graphe explicitement
(44 lignes binaires codees en hexadecimal, ordre des labels fourni), son
empreinte et son vecteur negatif. La preuve precise tau=(02)(13), qui
commute avec z,hM, echange les deux diagonales et transforme B en B^*,
C en(M C M)^*. Les domaines de colonnes et les contraintes sont preserves.
Reproduction avec les graphes explicites :5,2s. Module et trois fichiers
exportes, commit initial8aeef02, livraison824. Claude mentionne une
relecture independante : rappeler la consigne utilisateur de ne pas
remplacer l'un des deux chercheurs par un verificateur ; aucun agent
de verification lance par Codex.

### 15/10, suite826 : enumeration locale terminee et correction sur les relations mixtes

826 lu/acquitte. Claude renonce au relecteur dedie et conserve la
repartition entre chercheurs. Il annonce les25 cubes <z,hM> termines,
avec UNSAT final dans chacun :339556 structures invariantes admissibles,
192 PSD, nullite maximale9, aucune>=10. Il s'agit d'une enumeration SAT
complete annoncee SANS certificat exporte ; resultat accepte sans refaire
la campagne. Notre preuve finie de non-extensibilite, sous la borne globale
F7, demeure un resultat distinct. L'explication structurelle du plafond
LOCAL9 ne decoule pas encore de notre borne14.

CORRECTION EXPLICITE DU MESSAGE819. L'affirmation « hM tue toutes les
relations mixtes » est FAUSSE. Elle ne vaut que pour c=(6,2) et(2,6),
dont les neuf relations sont de cote. Dans c=(2,2), les objets de
nullite9 ont CINQ relations de cote et QUATRE relations mixtes ; Claude
en comptait53 parmi les72 PSD de son ancien run. Ce nombre53 n'est pas
une classification des192 PSD de l'enumeration maintenant terminee.

DEDUCTION STRUCTURELLE COMPLEMENTAIRE. Notre decomposition impose
nullT=nu0+4a+4b, nu0 dans{5,6}. A nullite9, necessairement nu0=5 et
a+b=1. Les cinq relations z-triviales sont exactement les quatre
indicatrices d'etoiles et celle du carreO. Sous g=hM, les etoiles
s'echangent0<->1,2<->3 et O reste fixe : dimension3 paire et2 impaire.
Les quatre autres relations forment UN module irreductible Q(zeta5).
Puisque g commute avec z et est une involution, il agit sur ce module
de dimension1 sur Q(zeta5) comme+1 ou-1. Les deux seuls profils sont
 (dim kerT_g+, dim kerT_g-)=(7,2) ou(3,6).
Dans c=(2,2), ce signe est exactement la parite commune des quatre
relations mixtes. Dans c=(6,2)/(2,6), les cinq indicatrices des grilles
exterieures fournissent les quatre relations non triviales et sont
g-paires : profil(7,2). Ce diagnostic distingue deux mecanismes sans
supposer que les relations mixtes seraient absentes. Aucun graphe ni
noyau sauvegarde par Claude n'a ete relu pour cette deduction.

### 15/10, suite828 : composantes forcees et sept plafonds locaux par reduction mod5

828 lu/acquitte. Claude propose un lemme pour g=h*p, p preservant les
mates, avec k transpositions exterieures. Sous(H_g), tout noyau g-impair
a coordonnees c_y=0 ; les k differences g_y-g_p(y) ne peuvent donc etre
absorbees et le gain pair est>=k. Sa borne de nullite utilise ensuite
ODD9 : cette derniere condition reste explicite, pas une preuve universelle
nouvelle d'ODD9. Il collecte les parites des PSD de sa campagne complete.
Aucune de ses matrices n'est ouverte ou recalculee par Codex.

PREMIERE DEDUCTION : min(c_l,c_m)=2 est structurel. Sous z, O est une
grille et la droite centrale opposee est isolee dans H_l. Apres contraction
des identifications geometriques, les cinq sommets restants sont les
cinq paires exterieures. z les permute transitivement. Une partition
invariante en composantes a des blocs de meme taille divisant5 : soit
cinq singletons, soit une composante. Donc c_l dans{2,6}, et pareil
pour c_m. Les quatre supports circulants non orientes sur5 sommets
(pas0, pas+-1, pas+-2, les deux) donnent exactement6,2,2,2 composantes
apres ajout de la droite isolee. Cette partie utilise z seul. Ajouter
hM et T/U PSD exclut(6,6) par notre obstruction damier. Ainsi min c=2
sur TOUTE la famille, sans recourir aux statistiques de Claude.

DEUXIEME DEDUCTION : filtre exact sur le noyau cyclotomique g-impair.
Noter R_l le matching ENTRE les etoiles0 et1, e=+1 s'il est D_s,
e=-1 s'il est M. Ne pas le confondre avec M0, matching interne a l'etoile0.
Definir f pareil pour2 et3. t,w sont les comptes signes de B=A02,C=A03.
Evaluer en X=1 les REPRESENTANTS DE LAURENT du bloc4x4 T_-(X), en gardant
son offset geometrique cyclotomique (il ne s'agit pas du vrai bloc
z-trivial12x12). La decomposition paire/impaire des deux bits donne
 3I2 et P=[[7/2-e,-t-w-1/2],[-t-w-1/2,7/2-f]].
Donc pour N=4T_-,
 det N(1)=576*d,
 d=(7-2e)(7-2f)-(2(t+w)+1)^2.
Evaluation en1 n'est PAS un morphisme Q(zeta5)->Q ; seule la reduction
modulo5 est intrinseque. Phi5(1)=5 donne bien Z[zeta5]->F5,zeta5->1.
Si d!=0 mod5, detN est non nul dans Q(zeta5), donc le bloc - est inversible.
C'est un critere suffisant ; un residu nul ne prouve PAS la singularite.

Sur les14 quadruplets(e,f,t,w) laisses par le quotient T/U PSD, SEPT
ont ce residu non nul. Tous ont nu0=5. Combiner b=0 et notre a<=1 deja
prouve donne nullT=5+4a<=9. C'est une preuve LOCALE du plafond9 pour ces
sept cas, sans ODD9 ni borne globaleF7. Ce sont sept types de quotient,
pas une mesure de la proportion des339556 graphes ou des192 PSD.

PREDICTION POUR LES MESURES DE CLAUDE. A nullite9, le profil(3,6) ne
survit a ce filtre que dans cinq quadruplets : e,f de signes opposes,
(t,w)=(2,0) ou(0,2), ou bien e=f=-1,t=w=0. Il exige donc R=M sur au
moins une droite. Tout cas D/D de nullite9 est necessairement(7,2).
Ces cinq cas sont des POSSIBILITES necessaires, pas des graphes construits.
Les deux autres quadruplets ont nu0=6 et sont incompatibles avec la
nullite9 par la formule modulo4 ; leur existence locale n'est pas reglee
par ce filtre. L'explication structurelle du plafond9 pour les sept
cas restants n'est pas achevee.

OUTIL : ajout mixed_parity_reduction et --parity-only dans
z5_hm_rank_obstruction.py ; bibliotheque standard, aucune lecture des
520 certificats necessaire pour cette nouvelle reduction. Identite du
determinant controlee directement par les24 termes de Leibniz pour
chacun des14 quotients. Rapport z5_hm_mixed_parity.json, temps0,37s.
La preuve de a<=1 provient bien du calcul precedent, elle n'est pas
redemontree par le seul petit filtre. Deductions communiquees dans829.

### 15/10, suite831 : profils de parite et filtre ramifie au second ordre

831 lu/acquitte. Claude a profile exactement180 des192 PSD de sa campagne
complete :116 de nullite9,c=(2,2), avec5 relations de cote et4 mixtes
PAIRES ;32 de nullite5,c=(2,2) ;16+16 de nullite9,c=(2,6)/(6,2), avec9
relations de cote. Les profils sont(7,2) ou(3,2), aucun(3,6) sur ces180.
H_hM est observe sur les deux cotes des180. Les12 autres ne sont pas
encore profiles ; ne pas transformer180 en192. Le raisonnement de LAB
par gain pair utilise ODD9 en plus de H_hM : condition toujours explicite.
Resultats acceptes sans relecture de ses graphes ni recalcul de ses noyaux.

NOUVELLE CONSTRUCTION LOCALE LAB : penaliser toutes les symetries h*p,
vraies ou fausses geometriquement, donne des PSD sans aucune de ce type,
de nullite10,c=(2,2),t=(6,10), et nullite11,c=(3,2),t=(7,10). Ces objets
sont des structures LOCALES44. Absence de h*p ne prouve pas que le groupe
complet est trivial ; aucun nouveau SRG asymetrique n'est annonce ici.

NOUVEAU RESULTAT Codex, sans enumerer les structures. Le test mod5
precedent ne regardait que la valeur en1 du determinant cyclotomique.
Il existe une reduction plus fine et toujours minuscule :
 Z[zeta5]/5 = F5[e]/(e^4), zeta5=1+e.
Elle est valable car Phi5(1+e)=e^4 mod5. Si le determinant reduit est
NON NUL, le bloc est inversible sur Q(zeta5). Si la reduction est nulle,
aucune singularite n'en decoule. Le determinant de Laurent est invariant
par X->X^-1 ; son developpement a donc la forme c0+c2(e^2-e^3).
Le second ordre suffit a exploiter TOUTE la reduction modulo5.

Dans les cinq types restants de nu0=5, N(1)=4T_-(1) a rang3 surF5.
Si v engendre son noyau et H est le mineur complementaire inversible,
le coefficient de Schur au second ordre est
 Q=v^t*N2*v + (E^t*N1*v)^t*H^-1*(E^t*N1*v).
Le signe PLUS provient de N1 antisymetrique. Avec les vecteurs v ci-dessous,
le mineur complementaire vaut1 mod5 ; c2=Q.

CAS MIXTE D/M, t+w=2. Noter D1=moment1(B-CM), les moments etant calcules
sur les decalages0,...,4 modulo5. Pour D a gauche, delta_j=D1[0,j]-D1[1,j] ;
pour D a droite, delta_i=D1[i,0]-D1[i,1]. Si a,s sont les decalages du
cote D, le noyau impair cyclotomique exige
 delta_0*delta_1 = 2*s*(a-s) mod5.
En effet v est(1,-1) sur le cote D, nul sur l'autre. Le terme diagonal
v^t*N2*v vaut4(a^2-s^2), et la correction Schur vaut(a-s)^2+delta0*delta1.
Leur somme se simplifie en Q=delta0*delta1-2*s*(a-s).

CAS M/M, t=w=0. Poser f=(1,-1), j=(1,1), alpha=j^t*D1*f,
beta=f^t*D1*j, p=f^t*D1*f, S2=f^t*moment2(B-CM)*f. Le vecteur
v=(f,-f) engendre le noyau de N(1). La congruence necessaire est
 S2 = a*alpha-b*beta-alpha^2-beta^2+p^2 mod5.
La decomposition en j_gauche,j_droite,(f,f),(f,-f) donne les trois
valeurs propres non nulles2,2,1 de N(1) modulo5. Les termes en a^2,b^2
se compensent dans Q. Si Q!=0, b_cyclotomique=0 ; avec a_cyclotomique<=1
de notre preuve precedente, la nullite LOCALE est<=9 pour ce candidat.

LES DEUX TYPES D/D DE nu0=6. Noter p=f^t*moment1(B-CM)*f et L la somme
de tous les moments1 des cellules de B+C. Les matrices constantes ont
rang2 surF5. Leur Schur commence par une matrice antisymetrique2x2.
On obtient directement
 det(4T_-)=p^2(e^2-e^3), det(2T_+)=4L^2(e^2-e^3) modulo5.
Donc p!=0 interdit b, L!=0 interdit a ; les deux non nuls imposent
nullite6. Une nullite14 exigerait p=L=0. Une nullite>=10 exige au moins
l'une de ces deux congruences. Ce n'est pas encore une preuve du plafond9
pour tous les candidats, ni une nouvelle exclusion de tout C1.

ARTEFACTS : code/codex/z5_hm_ramified_filter.py, standardlib autonome,
rapport z5_hm_ramified_filter.json. Entree --candidate : JSON contenant
block,B,C, avec la parametrisation existante. Il calcule les deux petits
determinants dans F5[e]/e^4 et les formules explicites des moments, puis
une borne de nullite CONDITIONNELLE aux hypotheses C1/C1'/C2 et T/U PSD.
Les112 fixtures synthetiques servent seulement a controler les identites
de polynomes ; ce ne sont pas des graphes annonces admissibles. La preuve
universelle est le calcul de Schur ci-dessus. Duree0,2s, aucun solveur,
aucun graphe LAB ouvert, aucun processus long. Cette arithmetique montre
comment la symetrie impose des relations par paquets de quatre ; hors de
cette famille, elle ne fournit pas de contrainte sur l'asymetrie generale.

### 15/10, suite833 : cible de relations mixtes et dimension de la liberte sans symetrie

Filtre ramifie livre dans832, commit595aa1d. Message833 lu/acquitte.
LAB confirme que son lemme utilise ODD9 ; les12 PSD manquantes venaient
du cube0 non sauvegarde, qu'il relance. Depuis HB_1 :8884 visites PSD,
meilleur objet sans h*p a nullite11,c=(3,2),t=(7,10). Depuis c22 :2019
visites PSD, aucune sans h*p dans ce run. Son protocole d'inspection
reste chez lui ; Codex poursuit une deduction nouvelle et n'a lu aucune
de ses matrices. La notion sans h*p reste distincte du groupe complet
trivial et d'un SRG construit.

NOUVELLE ANALYSE, SANS Z5, SANS h*p, SANS ODD9. Noter X,Y les deux
cotes24, O=X inter Y={02,03,12,13}, L=X moins O,R=Y moins O, de20 labels.
La formule de cote deja etablie donne rangT_X=23-c_l et rangT_Y=23-c_m.
Il faut traiter O correctement : ce n'est pas forcement une grille hors
de nos anciennes familles cycliques. Sur O, T a diagonale5/2, entrees
-1/4-Gamma sur les quatre aretes du C4 geometrique, et -Gamma sur ses
deux diagonales. C1 interdit qu'une diagonale partage un sommet avec
une arete de ce C4. La matrice est donc irreductiblement a diagonale
dominante, avec au moins une dominance stricte sauf si tout le C4 est
present. Ainsi delta=nullT_O vaut1 exactement pour la grille,0 sinon.
Les19 motifs de O permis par les plafondsC1 donnent1 rang3 et18 rang4.
Cette petite liste ne classe pas les graphes44.

Sous T PSD, chaque noyau principal se prolonge par zero. Les deux noyaux
de cote ont pour intersection exactement kerT_O, lui aussi prolonge par
zero. Leur somme a donc dimension
 k_cote = c_l+c_m+2-delta.
Le nombre de relations mixtes independantes modulo celles de cote est
 m = nullT-k_cote.
Eliminer le support positif de O, puis choisir des bases principales
positives des deux cotes. Leurs dimensions sont r_l=19-c_l+delta et
r_m=19-c_m+delta. Pour les blocs obtenus A,E,C, definir
 R_mix = A-E*C^-1*E^t.
Sous les hypotheses, nullR_mix=m. Normaliser donne une contraction
A^-1/2*E*C^-1/2 : ses valeurs singulieres egales a1 comptent exactement
les relations mixtes. En particulier,
 rangR_mix = 21+c_m-nullT,
et la cible Conway nullT>=14 equivaut rangR_mix<=7+c_m. C'est une
REFORMULATION de la cible spectrale, pas une contrainte supplementaire
ou une exclusion nouvelle. Elle isole l'objet a faire degenerer.

APPLICATION AUX PROFILS FOURNIS, SANS OUVRIR LES SEEDS. Pour c32,null11 :
- si O non-grille :7 relations de cote+4 mixtes, R_mix16x16 de rang12 ;
- si O grille :6 relations de cote+5 mixtes, R_mix17x17 de rang12.
Dans les deux cas, cible14 => rangR_mix<=9 : trois relations mixtes
supplementaires a c fixes. Pour c22,null10, le residu est17 ou18 de
dimension, de rang13 ; il faut quatre relations mixtes de plus pour14.
La valeur de delta des objets LAB n'est pas supposee ni re-mesuree.

SECONDE DEDUCTION, POUR CONSTRUIRE DES CHANGEMENTS QUI CONSERVENT LE NOYAU.
Fixer les deux cotes, donc seules les400 entrees du bloc croise LxR
varient. Pour une base COMPLETE N du noyau T, un changement Delta conserve
N si et seulement si Delta*N_R=0 et Delta^t*N_L=0. Or
 rangN_L=nu-(c_m+1), rangN_R=nu-(c_l+1),
car le noyau de la projection sur L est exactement le noyau du cote Y,
et reciproquement. Si P_L,P_R sont des bases des orthogonaux de ces
projections, tous les changements sont
 Delta=P_L*Z*P_R^t,
avec Z reel arbitraire de taille(21+c_m-nu)x(21+c_l-nu).
Les indicatrices des quatre etoiles etant dans N, les egalites C1
centrales sont automatiquement conservees. A c32,nu11, cela fait12*13=156
dimensions REELLES ; a nu14,9*10=90. Ce ne sont PAS156 changements binaires
ni156 graphes : boite0/1,C1',C2,U restent des contraintes supplementaires.
Les petites variations reelles conservent T PSD sur son support positif,
mais ne satisfont pas automatiquement ces autres contraintes.

LIEN PRECIS AVEC L'ASYMETRIE. Pour n'importe quelle permutation p des10
lettres exterieures, h*p agit sur chaque cote20 par[[0,P],[P,0]]. Tout
espace propre a dimension<=10, car une moitie des coordonnees determine
l'autre. Si TOUS les tenseurs u*v^t de l'espace des changements etaient
fixes par ce h*p, les deux espaces de facteurs seraient des espaces
propres scalaires (valeurs propres reciproques). Impossible si l'un
des facteurs a dimension>10. Donc, lorsque
 nu < 11+max(c_l,c_m),
les equations de conservation du noyau seules ne peuvent forcer aucun
h*p fixe. Comme il n'y a qu'un nombre fini de p, l'union de leurs
sous-espaces affines fixes ne couvre pas l'espace des changements reels.
Un choix reel generique evite tous les h*p. Ce n'est pas une construction
de graphe binaire admissible, mais cela identifie les hypotheses qui
manquent a un eventuel argument de symetrie forcee.
Pour c32, cette impossibilite de forcer h*p par les seules equations
dure jusqu'a nu13. A nu14, le facteur maximal descend a10 : cet obstacle
dimensionnel disparait. Cela PERMET un mecanisme de symetrie forcee a14,
sans prouver qu'il se produit. Ne pas convertir cette possibilite en
preuve de H-MATCH ou de l'impossibilite de l'asymetrie.

OUTIL : asymmetric_mixed_residual.py et rapport associe. API from_adjacency
construit le residu et releve chaque noyau mixte en une relation sur44
labels, a partir d'un objet deja accepte par le producteur. API
cross_trade_factors prend son noyau complet fourni, sans le recalculer,
et renvoie P_L,P_R. Six fixtures de Gram abstraites controlent la formule
et les releves ; deux controlent les espaces156/90 et une variation
elementaire. Elles ne sont pas des graphes. Duree1,0s ; pas de solveur
lance, aucune affirmation d'acceleration ou d'accessibilite du probleme
binaire restant. Nouvelle direction de construction complementaire des
marches LAB, plutot qu'un audit de leurs resultats.

Suite immediate : resultat ci-dessus commit7b89328 et envoye dans835.
Le saut de sequence a revele834, lu/acquitte : LAB a maintenant profile
192/192. Les12 dernieres sont null9,c22,t22,5 relations de cote+4 mixtes
paires, profil(7,2),H_hM des deux cotes. Totaux :128 de ce type,32 null5
c22,16+16 null9 c26/c62. H_hM vaut donc sur192 ; la conclusion par6h
utilise toujours ODD9. Marches :15777 visites HB_1,max sans h*p11 ;3774
depuis c22, aucune sans h*p dans ce run. Accepte sans audit ni reponse
d'accuse. Aucun processus propre actif.

### 15/10, suite836/837 : ODD9, une coupe stricte universelle et un modele de relaxation

836 lu/acquitte. LAB relaie la repartition : il prend A(mecanisme sans
symetrie) et B(construction), Codex prend C=ODD9. D(extension d'abord)
est mis de cote. Ce choix est dans notre mission de recherche deja
autorisee. Reprise ciblee de odd9_network_schur.py, aucun ancien gros
carnet ni matrice du pair relu. L'ancienne reduction9x9 reste exacte,
mais la stricte positivite universelle n'est pas etablie.

NOUVEAU THEOREME, NE SUPPOSANT NI ODD9 NI SYMETRIE. Soit F l'ensemble des
40 labels exterieurs, O={02,03,12,13}. Choisir S contenu dansF avec5 labels
par etoile centrale et2 par lettre exterieure. Alors|S|=20 et le vecteur
q, nul surO,+1 surS,-1 surF-S, a incidence nulle sur les14 lettres. Donc
Kq=0. Pour Gamma BINAIRE satisfaisant C1, sommer les comptes par etoile
pour un sommet exterieur x donne
 deg_F(x)+2deg_O(x)=6.
Ainsi chaque degre dansF est PAIR, meme lorsque O n'est pas une grille.
Gamma*q est donc pair surF, alors que3q est impair. Le vecteur q ne peut
pas appartenir au noyau de T=3I-Gamma-K.

IDENTITE DE COMPTAGE. Poser H=e(O,F), H_S=e(O,S), E0=e(O). Sommer C1 surO
donne H=16-4E0. Sommer surS donne2e(S)+cut(S,F-S)=120-2H_S. Enfin
e(F)=120-H. Comme Kq=0,
 q^t*T*q=120-2e(F)+4cut(S,F-S)=8*(49-e(O union S)).
Sous T PSD, l'inegalite ordinaire est e(O union S)<=49. L'egalite
mettrait q dans kerT et contredirait la parite ci-dessus. Le nombre
d'aretes etant entier, on obtient la coupe STRICTE
 e(O union S)<=48, ou q^t*T*q>=8.
Hypotheses precises : C1, Gamma binaire, T PSD. Ni U, ni C2, ni une
symetrie, ni O grille ne sont requis. Si O est une grille, C1 interdit
O-F et e(O)=4 ; on retrouve e(S)<=44 au lieu45, ou coupe>=32 au lieu30.

CERTIFICAT A SATURATION. Si un candidat binaire C1 atteint49, alors
s_i=(Tq)_i est impair non nul pour tout i exterieur. Avec T_ii=5/2,
v=5q-2s_i e_i donne exactement v^t*(8T)*v=-80s_i^2<0. Le module fournit
une fixture BINAIRE C1 construite ici a49, volontairement non PSD, avec
s_i=5 et valeur -2000. C'est un certificat de la coupe, pas un graphe
nouveau admissible. Une autre fixture C1 fractionnaire a O vide controle
l'identite generale sur3 directions, sans hypothese de grille ni de PSD.

FAMILLE EXPLICITE POUR LE SOLVEUR. Choisir5 lettres positives pour
l'etoile0, les5 complementaires pour1, independamment5 pour2 et leurs
complementaires pour3. Cela donne des q h-impairs qui respectent tous les
equilibres requis. Identifier q et-q laisse126*252=31752 directions
indexees. flat_odd_cut renvoie une ligne de276 variables d'aretes sur24
labels, borne48 ; avec assume_overlap_grid=True,190 variables sur20
labels, borne44. flat_odd_cuts est un iterateur ; aucune grosse liste
generee par defaut. Pas de gain de temps solveur mesure. La preuve vaut
aussi pour les S equilibres qui ne sont pas de cette sous-famille h-impaire.

MODELE FRACTIONNAIRE DE NECESSITE. Une construction explicite donne
C1/C1', diagonale0, entrees[0,1], T et U PSD, c=(2,2), nullT=6,nullU=4,
mais gain impair8. SurO : C4, sans aretes versF. SurF, en ordre
(centre,lettre), Gamma=P tensor H + Q tensor D, ou
 H=(J10-I10)/9, t=(1,-1)^5, D=t*t^t-I10+H,
 P a diagonale et mates centraux1, autres entrees2 ;
 Q est la matrice circulante de Klein de premiere ligne
 (2/25,-9/100,2/25,-7/80).
Quatre caracteres centraux et les secteurs exterieurs{1},{t},M+ de
somme0,M- orthogonal a t donnent36 vecteurs propres communs T/U, tous
positifs sauf une valeur nulle de T. Le quotient restant8x8 a rang3
pour T,4 pour U, avec elimination exacte PSD. Cette preuve rationnelle
evite la diagonalisation dense. Les six relations T sont les4 etoiles,
l'indicatriceO et n(c,y)=(1,-1,1,-1)_c*t_y. Le dernier verifie Kn=0,
Gamma*n=3n. Il est interdit dans le cas binaire par notre parite.

Le matching interne de chaque etoile a poids1/5 a l'interieur des
deux classes de5 et1/25 entre elles. Il est la MOYENNE EXPLICITE de225
vrais matchings : choisir une arete transversale(25 choix), puis un des
3 matchings sur les4 sommets restants de chaque classe. Donc ajouter
toutes les inegalites d'ensembles impairs du polytope des matchings ne
supprime pas ce modele. Il atteint e(O union S)=49 et viole notre coupe48.
Il viole aussi C2 : pour(3,13),(3,11), communs ponderes785639/648000,
arete1/5, exces267239/648000. Il n'est PAS un contre-exemple binaire a
ODD9 et ne permet pas d'isoler laquelle de l'integralite ou C2 suffit.
Il prouve l'insuffisance de comptes lineaires+boite+matchings convexes+
T/U PSD pour obtenir ODD9. Une exploration pilote de30000 coefficients
binaires de la famille cyclique nu0=6 n'a rien trouve en1,5s : aucun
verdict exhaustif n'en est tire, aucune enumeration du pair dupliquee.

DIAGNOSTIC DE NOYAU, SANS REFAIRE LES CALCULS DU PRODUCTEUR. Pour son
noyau complet N, nu=dimN, definir C_m(n)_y=n(2y)+n(3y) et rho=rang(C_m N).
La projection de N sur les20 nouveaux labels a noyau de dimensionc_l+1.
Ses relations antisymetriques ont dimensionnu-rho-c_l-1. Donc
 gain_impair=11+c_l-nu+rho,
 defautODD9=nu-c_l-2-rho.
La PSD de T est necessaire a cette interpretation par relations de Gram.
Si le defaut est positif, une relation de ker(C_m N), debarrassee de sa
moyenne par l'etoile2-moins-3, fournit un temoin extra avec coefficients
antisymetriques de somme0 sur le nouveau cote. API kernel_projection_profile
consomme N sans recalculer Gamma,PSD,rang ou automorphismes. Sur notre
modele, rho=1,defaut1. Une relation ODD9 generale peut avoir des valeurs
non plates, une autre parite entiere, ou une incidence non nulle : les
coupes ne terminent donc PAS la preuve d'ODD9.

ARTEFACT : odd9_necessity_models.py et rapport exact, environ1,1s, SymPy.
Adjacence rationnelle explicite a echelle3600, modes propres, noyau,
modeles de necessite, coupe, temoin negatif binaire et API de projection.
Message d'etape838 envoye ; pas de processus actif.

837 lu/acquitte pendant ce travail. LAB distingue typeI (cassure invisible
au noyau, U exclut) et typeII (intersection avec hN de dimension12,nu<=13
sur ses voisinages). Correction acceptee : 'une seule saturation' est
FAUX ;128 PSD c22 du groupe cyclique ont4 saturations relativement a h.
KER-SYM, existence d'une involution h*p preservant le noyau, reste une
loi EMPIRIQUE a lignages biaisés ; asy11 a profil(9,2) sous la fausse
h(46), sans symetrie de Gamma. Ses tests a froid ne sont pas dupliques.
Reponse algebrique preparee : apres les4 etoiles forcees, le quotient
a dimension40, avec20 directions paires et20 impaires pour chaque h*p.
Si d=nu-4, une strate invariante a+b=d a codimension20d-2ab dans Gr(d,40).
A nu14, cette codimension est au moins150. La grande nullite et les
seules etoiles ne forcent donc pas KER-SYM par dimension ; il faudrait
un mecanisme combinatoire supplementaire. Ce calcul ne construit pas
de noyau de graphe admissible et ne refute pas la conjecture du pair.

839 lu/acquitte. LAB adopte le diagnostic de projection sur son noyau ;
sa conjecture KER-SYM est observee sur342 structures, avec biais de
familles toujours a lever. Il lance <Z5,tau>,tau=(02)(13),5 cubes, hors
des familles contenant h*p. Aucun de ses calculs n'est duplique ici.
Artefact et rapport regeneres en1,1s : toutes les identites exactes
passent ; statut explicite EXACT_ODD9_INTEGER_CUTS_AND_RELAXATION_OBSTRUCTION,
ODD9 binaire OPEN. Preuve et portee sont conservees ci-dessus.

## 15/10 - Suite841 : KER-SYM universelle refutee et profil complet des coupes

Resultat de19d6bf5 transmis au pont840. Une notification ancienne a
conduit a une unique lecture utile :841, lu/acquitte. LAB rapporte46
premieres structures PSD de nullite9 de <Z5,tau>,tau=(02)(13), dont le
noyau n'est invariant sous AUCUNE des9496 involutions h*p testees.
La loi KER-SYM universelle est donc refutee, resultat accepte sans
reverification. Ces nullites9 ne refutent pas une eventuelle version
restreinte aux nullites>=14. LAB poursuit l'enumeration de cette famille.

NOUVEAU CALCUL, DEMANDE EN841 : la coupe48 est-elle saturee sur les
objets deja construits ? J'ai calcule ce NOUVEL invariant sur4 exports
locaux, sans recalculer leur admissibilite, rang, PSD ou automorphismes.
Je n'ai pas les331 objets de rang30 en lot ici : aucune affirmation sur
ce corpus entier. L'outil portable permet a LAB de les traiter lui-meme.

Enumeration COMPLETE de la famille des coupes equilibrees S, sans se
limiter aux31752 h-impaires. Chaque lettre exterieure choisit2 etoiles
parmi4 ; chaque etoile en choisit5. Si les nombres des six types de
colonnes01,02,03,12,13,23 sont(a,b,c,d,e,f), l'equilibrage impose
f=a,e=b,d=c et a+b+c=5. Le nombre de directions a signe pres est donc
 (1/2) sum_{a+b+c=5} 10!/(a! b! c!)^2 =586278.
Pour a=0..5, les nombres sont31752,220500,252000,75600,6300,126.
a=0 est exactement notre sous-famille h-impaire ; a=5 est h-paire.
Normalisation : (0,4) appartient a S, ce qui choisit exactement l'un de
S et F-S. Leurs nombres d'aretes dans O union S sont egaux sous C1.

ALGORITHME : lister les6^5=7776 choix des cinq premieres lettres et des
cinq dernieres ; reunir seulement les comptes d'etoiles complementaires
a5. Les valeurs sont des nombres entiers d'aretes obtenus directement
par petits produits matriciels, sans diagonalisation, solveur ou test
de rang. Aucun grand tableau de586278 contraintes n'est stocke.
Temps mesure environ0,03s/objet apres le cache initial. Chaque maximum
a un temoin24 explicite, recompte directement pour proteger l'indexation
du nouvel outil. Les effectifs par a retrouvent la formule multinomiale.

RESULTATS (maximum sur TOUTES les586278 directions ; puis h-impaires) :
- fourstar_psd_rank30_urep100.json :46, puis43 ;6 directions maximales.
- null13.json :46, puis44 ;6 directions maximales.
- fourstar_psd_asym_c31.json :45, puis44 ;5 directions maximales.
- fourstar_psd_grid_Z5h_c22.json :43, puis43 ;190 directions maximales.
Aucun de ces4 objets ne sature48. Le serrage de la borne48 n'est donc
PAS etabli. Les profils par a sont respectivement
 [43,43,43,43,45,46], [44,43,43,44,45,46],
 [44,44,43,44,44,45], [43,43,43,43,43,43].
Dans les trois premiers, les directions les plus proches de la borne
sont h-PAIRES (a=5), pas dans la famille impaire initialement indexee.
Cela ne constitue pas un theoreme de symetrie ou une preuve d'ODD9.

Nos controles propres : le modele fractionnaire T/U PSD atteint49,
et la fixture binaire C1 nonPSD atteint49 avec exactement1 direction
violant48. Aucun objet du pair n'a ete reaudite. Module autonome
odd9_balanced_cut_profile.py (NumPy), API profile(G,labels,scale=1) et
from_export(data) ; CLI --input un_ou_plusieurs_JSON --output rapport.
Rapport odd9_balanced_cut_profiles.json contient les temoins, les
effectifs de maximisants et tous les profils par a. Le calcul consomme
les labels fournis pour eviter toute hypothese cachee sur leur ordre.

## 15/10 - Suite843 : ODD9 refutee, decomposition exacte de son defaut

843 lu/acquitte. LAB rapporte des contre-exemples BINAIRES admissibles
C1/C1'/C2 et PSD exacts pour T et U : hv_h_c22_H30_23, c22,nu14,
rangT30,rangU39, gains impairs8/8 et pairs1/1 ; deux autres temoins
c32,c52 ; au total58 structures h-invariantes nu14, neuf types de c,
toutes a gains8/8. r7_Z5h_cold1_PSD_1, c22,nu9, a gains5/5.
Certificats et calculs du producteur ACCEPTES, aucun re-audit demande
ni effectue. Les fichiers correspondants ne sont pas encore dans
lab_exchange cote Codex. ODD9 universelle est REFUTEE, meme a nu14,c22,h.
Les anciennes mentions 'ouverte' dans ce journal sont historiques.
La chaine conditionnelle ODD9=>B' ne prouve plus B', qui reste ouverte.
La coupe48, le Schur exact et la formule de projection rho ne supposaient
pas ODD9 et restent valables. L'exclusion cyclotomique/F7 de <Z5,hM>
reste aussi valable ; LAB rapporte9/9 sur ses membres de cette famille.
LAB refute egalement SUM14 universelle : exemple nu13,s2,dim(N+hN)=15.
Sa version limitee a nu14 reste ouverte.

NOUVELLE DECOMPOSITION SANS SYMETRIE. Soit N=kerT, nu=dimN. Decomposer
l'espace des44 labels selon h=(01)(23), en V+ et V- de dimensions22.
Poser a=dim(N inter V+), b=dim(N inter V-), s=nu-a-b. Alors
 dim(N+hN)=nu+s.
Sur le vieux cote24, le noyau a parites(c_l,1) : les c_l indicatrices
des composantes du reseau pondere sont toutes h-paires ; la difference
d'etoiles est h-impaire. Pourquoi les composantes sont-elles h-stables ?
Elles sont fermees par F et M (conductances positives). h agit comme F
hors du recouvrement, et comme FM sur le recouvrement. Cette description
du vieux noyau NE requiert PAS que Gamma globale soit h-invariante.

Soit C_m(n)_y=n_2y+n_3y et rho_l=rang(C_m N). Le sous-espace
K_m=N inter kerC_m a dimension nu-rho_l. Il contient la somme directe
des b relations pures impaires et des c_l relations pures paires du
vieux cote. Le quotient a donc dimension
 eta_l=nu-rho_l-b-c_l.
Il s'injecte dans N/((N inter V+)+(N inter V-)) : si une relation de K_m
se decompose en une paire et une impaire, sa partie paire a ses nouvelles
coordonnees nulles et appartient donc au vieux noyau pair. D'ou
 0<=eta_l<=s,
 d_l=9-gain_impair_l=b-2+eta_l.
Meme formule a droite. Si N est h-invariant, s=0 et eta_l=eta_m=0 :
 gain_impair_l=gain_impair_m=11-b.
Une vraie symetrie de Gamma suffit, mais n'est pas necessaire pour cette
derniere identite. Sans invariance, ignorer eta peut etre faux : notre
fixture de sous-espace abstrait a nu5,a=b2,s1,c_l=c_m1,gains8/9,
eta_l1,eta_m0. C'est un exemple d'algebre lineaire, PAS un graphe.

EXPLICATION SPECTRALE. Pour les22 orbites de h, F a colonnes e_i-e_hi,
donc F^tF=2I. Les2 differences d'etoiles u0,u1 ont norme carree24 et
sont orthogonales. W=F^t[u0,u1]/2 verifie W^tW=12I. Calcul geometrique :
 K_-=F^tKF/2=WW^t/4,
 L_-=F^tLF/2=WW^t/3.
C1 donne Gamma*u0=Gamma*u1=0. Sur l'orthogonal de W, de dimension20,
 T_-=3I-Gamma_-, U_-=4I+Gamma_-, Gamma_-=F^t Gamma F/2.
Sous T PSD, un noyau de cette compression se releve au noyau complet.
Ainsi b-2 est EXACTEMENT la multiplicite de3 dans Gamma_-. Cela vaut
meme sans commutation de Gamma et h. Si Gamma commute avec h, le
quotient est signe ENTIER, entrees Gamma(i,j)-Gamma(i,hj).
T/U PSD autorisent l'intervalle ferme[-4,3] ; elles ne rendent PAS
stricte l'extremite3. Les exemples du pair occupent cette extremite :
gain8 -> b3 -> multiplicite1 ; gain5 -> b6 -> multiplicite4.

BUDGET CORRIGE, SANS SYMETRIE : apres le vieux cote et les nouveaux
vecteurs impairs, le gain residuel pair vaut
 e_l=(44-nu)-(23-c_l)-(9-d_l)=12+c_l-nu+d_l.
Si l'on prouve INDEPENDAMMENT e_l>=k, on obtient
 nu<=12+c_l+d_l-k.
Il serait faux d'omettre d_l, ou d'affirmer sans examen qu'un ancien
lemme conditionnel fournit encore k. Sur les58 cas h,nu14,gain8,
(a,b)=(11,3) et e_l=c_l-1,e_m=c_m-1. DANS cette classe, min c>=2
equivaut a e_l,e_m>=1. C'est une reformulation de la cible, pas sa preuve.

PARITE RENFORCEE. Une relation pure h-impaire, normalisee en retirant
ses projections sur u0,u1, a incidence nulle sur toutes les14 lettres.
Elle verifie donc Gamma*n=3n. Apres mise sous forme entiere primitive,
ses40 coefficients exterieurs ne peuvent PAS tous etre impairs, MEME
si n n'est pas nul sur O. En effet C1 donne e(O,F)=16-4e(O)<=16 :
au moins24 exterieurs n'ont aucun voisin dans O. Sur l'un d'eux,
Gamma*n serait une somme paire de coefficients impairs, contre3n impair.
La nouvelle obstruction ne suppose plus n|O=0. Elle n'exclut pas les
relations a coefficients pairs ou nuls, donc respecte la refutation.

ARTEFACT : odd9_defect_decomposition.py et rapport. Identites de
projecteurs et fixture abstraite calculees exactement en1,2s. Les
budgets des cas LAB sont deduits de SES nombres, sans lire ses graphes.
API normalize_odd_relation consomme un vecteur fourni, retire les
etoiles forcees, exporte le vecteur primitif et ses profils de valeurs
et parites ; elle ne recalcule pas l'appartenance au noyau du producteur.
Message844 a demande au pair les labels et UNE relation supplementaire
pour comprendre comment les coefficients evitent la parite plate.
Statuts executables et rapports ODD9/STILL_OPEN corriges, sans relancer
les anciens calculs. Aucun processus de recherche lourd actif.
