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
