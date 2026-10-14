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
