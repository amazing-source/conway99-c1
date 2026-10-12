# Deux cocliques de Hoffman et réduction au noyau de Fano

12 octobre 2026. Cadre : un hypothétique SRG(99,14,1,2), sans hypothèse
sur ses automorphismes ni sur son rang modulo 7.

La branche où deux cocliques de Hoffman se coupent en quinze sommets
équivaut à la présence d'un sous-graphe co-Heawood. Son bord est entièrement
fixé sur quatorze sommets. Les appariements autour de ce bord se réduisent,
par renommage, à 21 choix binaires. Une projection supplémentaire fournit
sur les 70 sommets restants une matrice entière H vérifiant

    H >= 0,    rang H = 16,    H² = 147 H.

Ces résultats réduisent la branche ; ils ne l'excluent pas. Le premier
essai exact de complétion reste UNKNOWN à 45 secondes. Les deux essais
locaux sur un hexagone passent les contraintes de prolongement testées.

## 1. Un noyau qui équivaut à deux cocliques

Écrivons C = Z ∪ S et C' = Z ∪ T, avec |Z|=15 et |S|=|T|=7.
Les ensembles C et C' sont indépendants. L'égalité de Hoffman impose
qu'un sommet extérieur à une telle coclique ait exactement quatre voisins
en elle. Le graphe entre S et T est donc biparti 4-régulier.

Soit B sa matrice d'incidence 7×7. Deux sommets distincts de S ont au plus
deux voisins communs dans T. Pour un sommet de S, la somme de ces six
intersections est 4·3=12 : elles valent donc toutes deux. Ainsi

    BBᵀ = BᵀB = 2I + 2J.

Le complément de B est le design 2-(7,3,1), c'est-à-dire le plan de Fano.
Le graphe biparti défini par B est le co-Heawood.

Réciproquement, supposons que Γ contienne un co-Heawood induit sur S∪T.
Chaque paire de sommets dans S a déjà ses deux voisins communs dans T.
Un sommet extérieur touche donc au plus un S et au plus un T.

Le vecteur h=1_S−1_T est propre de valeur −4 sur le noyau. La borne
spectrale inférieure de Γ est −4. Son cas d'égalité, après prolongement
par zéro, impose Ah=−4h. Les nombres de voisins extérieurs dans S et T
sont donc égaux. Chaque sommet extérieur a profil (0,0) ou (1,1).

Chaque sommet de S a dix voisins extérieurs. Il y a donc exactement
70 sommets de profil (1,1), notés R, et quinze de profil (0,0), notés Z.
Pour z∈Z, compter ses chemins de longueur deux vers S donne 7·2=14.
Chaque voisin dans R contribue une fois, aucun autre sommet ne contribue.
Tous les quatorze voisins de z sont donc dans R : Z est indépendant.
Les ensembles Z∪S et Z∪T sont les deux cocliques de taille 22 recherchées.

Cette équivalence permet d'attaquer directement un sous-graphe déterminé.
Elle ne suppose pas qu'un co-Heawood doive exister dans tout C1.
Le type ternaire (7,15,0) du dossier K7 est une condition suffisante connue
pour entrer dans cette branche.

## 2. Les quarante-neuf cases ont des tailles fixées

Chaque r∈R a un unique voisin s(r)∈S et un unique voisin t(r)∈T.
La case R_st a taille

    |R_st| = 2 − B_st.

En effet, les voisins communs de s et t sont exactement les sommets de
cette case. Il y a 28 cases simples et 21 cases doubles. Un sommet d'une
case simple sera dit de type simple, et un sommet d'une case double de
type double. R comporte donc 28 sommets simples et 42 doubles.

Chaque r a trois voisins dans Z, par l'égalité de Hoffman appliquée à
Z∪S. Notons U_r ce triple. Les soixante-dix triples forment un design
simple 2-(15,3,2) : une paire de Z a exactement deux voisins communs,
tous dans R ; deux triples identiques donneraient trois voisins communs
à deux sommets de R.

Chaque ligne s contient dix triples, chaque point de Z y apparaît deux
fois ; même propriété dans chaque colonne t. Les deux triples d'une case
double sont disjoints : les deux sommets ont déjà s et t comme voisins
communs.

## 3. Les appariements se ramènent à vingt et un bits

Le voisinage d'un sommet de Γ est une réunion de sept arêtes disjointes.
Dans N(s), les quatre sommets de T sont appariés aux quatre sommets des
cases simples de la ligne s. Restent les six sommets des trois cases
doubles. Ils sont appariés entre eux, sans arête à l'intérieur d'une case.

En contractant les trois cases, cet appariement donne un multigraphe
2-régulier sans boucle sur trois sommets : c'est le triangle. Il y a donc
une arête entre chaque paire de cases. Choisir ses extrémités laisse
exactement 2³=8 appariements.

Les échanges indépendants des deux sommets de chacune des trois cases
agissent transitivement, et librement, sur ces huit choix. On fixe donc
un appariement standard dans chacune des sept lignes de S. Les 21 cases
doubles étant distinctes, ces normalisations sont simultanément valables.

Il reste huit choix dans chacune des sept colonnes T, donc

    8⁷ = 2²¹ = 2 097 152 configurations étiquetées

pour tous les appariements passant par S ou T, avant les autres
contraintes de Γ. Ce compte ne désigne ni des classes d'isomorphisme,
ni des complétions. Le renommage utilisé ne suppose aucun automorphisme
du graphe final.

Sur les 42 sommets doubles, les arêtes ainsi imposées forment la réunion
de deux appariements parfaits disjoints. Leurs cycles sont pairs et de
longueur au moins six. Un cycle de longueur quatre donnerait un quadrangle
dans le graphe d'incidence du plan de Fano, qui n'en possède pas.

Dans un cycle de longueur six, une corde à distance deux ferait un
deuxième triangle sur une arête déjà complétée par S ou T. Seuls les trois
diamètres sont possibles. Deux diamètres donneraient trois voisins
communs à deux sommets non adjacents du cycle. Il reste donc les cas
sans corde ou avec un seul diamètre.

## 4. Le graphe résiduel sur soixante-dix sommets

Soient D l'adjacence sur R, X_S et X_T les incidences S×R et T×R,
et Y l'incidence Z×R. On a D1=9·1 et

    YYᵀ = 12I + 2J,
    X_S Yᵀ = X_T Yᵀ = 2J,
    X_S X_Sᵀ = X_T X_Tᵀ = 10I,
    X_S X_Tᵀ = 2J − B.

Les équations de Γ donnent

    YD   = 2J − Y,
    X_S D = 2J − X_S − B X_T,
    X_T D = 2J − X_T − Bᵀ X_S.

Sur l'espace engendré par les lignes de X_S et X_T, orthogonal à 1,
on obtient les valeurs propres −1±√2, chacune six fois. Sur les quatorze
contrastes des lignes de Y, orthogonaux à cet espace, D vaut −1.
Sur le complément de dimension 43, l'identité SRG donne D²+D=12I.
La trace nulle fixe les multiplicités restantes. Le spectre complet est

    9¹,  (−1+√2)⁶,  (−1−√2)⁶,  (−1)¹⁴,  3²⁷,  (−4)¹⁶.

En particulier R contient 56 triangles. Un sommet simple appartient à
trois de ces triangles, un sommet double à deux : les autres triangles
passent par ses trois voisins dans Z, puis par S et T. C'est une
description nécessaire, pas un graphe construit.

## 5. Une matrice entière de rang seize

Partons de la coclique C=Z∪S. Sur F=T∪R, le dossier K7 établit

    Q = 9I − 3A_F − N_C + J,
    Q² = 21Q,    Q >= 0,    rang Q = 22,

où N_C est le Gram de l'incidence vers C. Écrivons Q comme Gram de
vecteurs v_f. Sur T, on a Q[T,T]=7I−J, donc les sept v_t engendrent un
espace de dimension six.

Projetons orthogonalement les v_r sur le complément de cet espace et
notons w_r leurs projections. Elles engendrent un espace de dimension
16. Pour r∈R_st, les produits scalaires vers T sont les sept entiers

    k_r(j) = 1 − B_sj − 3[j=t],    somme_j k_r(j)=0.

L'inverse sur l'image de 7I−J est 1/7. Le Gram résiduel est donc
Q[R,R]−KᵀK/7. En le multipliant par sept, on obtient une matrice entière H.
Pour r dans la case (s,t),

    H_rr = 36 − 6 B_st.

Pour r≠r' dans les cases (s,t), (u,v), poser q=|U_r∩U_r'| et
e=D_rr'. Alors

    H_rr' = 12 − 21e − 9([s=u]+[t=v])
                    − 7q − 3(B_sv+B_ut).                 (1)

Pour vérifier la formule, il suffit de développer

    k_r·k_r' = −5 + 2[s=u] + 9[t=v] + 3(B_sv+B_ut).

Il reste à établir l'identité polynomiale annoncée. Puisque Q²=21Q et
rang Q=22, on peut choisir les vecteurs v_f avec

    somme_f v_f v_fᵀ = 21 I_22.

La projection orthogonale annihile les sept v_t. Par conséquent

    somme_r w_r w_rᵀ = 21 I_16.

Le Gram des w_r a donc seize valeurs propres égales à 21 et toutes les
autres nulles. Comme H est sept fois ce Gram,

    H >= 0,    rang H = 16,    H² = 147 H.

Sa diagonale comporte 28 valeurs 30 et 42 valeurs 36, de somme 2352=16·147.
Cette contrainte couple toutes les lignes, toutes les colonnes et tous
les triples U_r. Elle n'introduit pas d'hypothèse de rang modulo sept.

## 6. Calculs bornés et limites établies

Les programmes sont dans `code/codex/`, les sorties dans
`data/codex_coheawood/`.

- `check_coheawood_structure.py` : contrôle exact des huit appariements,
  de leur unique orbite sous les échanges des trois cases, des tailles
  du bord et des 2 401 coefficients de projection. PASS.
- `coheawood_completion.py` : modèle exact à 2 940 variables d'arêtes,
  avec toutes les conditions de degré et de voisins communs. Il couvre
  la branche entière après la normalisation du §3. Un essai à quatre
  workers, limité à 45 secondes, donne UNKNOWN. Aucun certificat
  d'infaisabilité, aucune complétion.
- `coheawood_hexagon_masks.py` : les deux hexagones du §3 ont des moments
  de prolongement entiers faisables. Ils sont donc conservés. Ces moments
  ne décident pas les arêtes entre sommets extérieurs.
- `coheawood_local_gram.py` : un essai exploratoire sur 2 000 échantillons de graphes
  cubiques locaux ne trouve aucune obstruction de positivité sur une
  seule ligne de dix sommets. Ce n'est pas une classification.
- `coheawood_probe.py` : les premiers blocs locaux passent les bornes
  spectrales testées ; les évaluations flottantes de ce pilote ne servent
  à aucune exclusion.

Le point restant est la compatibilité simultanée des sept lignes et des
sept colonnes avec le même design de triples et la même adjacence D.
La positivité d'une ligne et les moments d'un hexagone ne la décident pas.
La formule (1) et l'identité H²=147H donnent désormais une contrainte
commune explicite, au lieu de traiter ces lignes séparément.

## 7. Sources réutilisées

- Dossier `C1_K7_RESULTATS_PARTIELS/PREUVES.md`, publié au commit
  `f2b6454` : Q²=21Q, rang 22, et la construction des deux cocliques
  sous le type ternaire (7,15,0).
- `notes/110_ROUTES_CLOSES_ET_CODES_DES_DROITES.md` : la configuration
  Fano de norme 14 et l'intersection de quinze points étaient déjà
  identifiées dans la campagne. Leur ancienneté ne limite pas leur usage.
- [Brouwer, Heawood graph](https://aeb.win.tue.nl/drg/graphs/Heawood.html) :
  identification classique du co-Heawood au graphe de non-incidence de
  Fano et son spectre. L'argument des sections 1–5 est donné ci-dessus
  avec les paramètres de C1.

Aucune exclusion de toute la branche (7,15,0), ni de α=22, ni de C1
n'est annoncée dans cette note.

## 8. Attaque du système global

Suite à la consigne de Dilan du 12 octobre : les faisabilités locales
ne constituent pas un point d'arrêt. Les programmes ci-dessous portent
sur un même graphe à 99 sommets, avec les sept lignes, les sept colonnes
et les quinze points de Z simultanément.

### Renommer tous les points de Z en une seule fois

Fixons une ligne S, constituée de dix sommets de R. Chacun des quinze
points z de Z touche exactement deux de ces dix sommets. Deux points
distincts z,z' ne peuvent définir la même paire {r,r'} : cette paire
aurait alors trois voisins communs, à savoir S, z et z'.

On peut donc numéroter Z par ordre croissant des quinze masques binaires
à dix bits de ces paires. Ceci supprime toute la liberté de permutation
S_15 des points de Z, pour un étiquetage fixé de R. C'est une normalisation
couvrante, sans hypothèse d'automorphisme ni choix d'un graphe cubique
particulier. L'ancien modèle ne fixait que les trois voisins d'un seul r.

L'essai complet avec cette normalisation reste UNKNOWN après 240 secondes
(`global_canonical_z.json`). Ce résultat ne fournit aucune exclusion.

### Deux contraintes spectrales suffisent globalement

Voici un critère exact utilisé comme outil de recherche, sans revendication
de nouveauté. Pour une matrice d'adjacence A d'un graphe simple 14-régulier
sur 99 sommets, posons

    P = 27I − 9A + J,       Q = 44I + 11A − 2J.

Alors le graphe est un SRG(99,14,1,2) si et seulement si P et Q sont toutes
deux positives semi-définies.

**Preuve.** Les deux matrices annulent 1. Sur son orthogonal, leur
positivité équivaut à −4 ≤ λ ≤ 3 pour chaque valeur propre λ de A.
La régularité et la diagonale de A² donnent

    somme λ = −14,       somme λ² = 99·14 − 14² = 1190,

où les sommes portent sur les 98 valeurs propres orthogonales à 1.
Par conséquent

    somme (λ−3)(λ+4) = 1190 − 14 − 12·98 = 0.

Chaque terme est négatif ou nul ; chacun est donc nul. A²+A−12I annule
1-perp et vaut 198 sur 1, d'où A²+A=12I+2J. La réciproque découle du
spectre du SRG. Ce critère assure toutes les compatibilités de paires,
pas seulement celles de certains supports.

### Coupes entières portant sur le graphe complet

Un vecteur entier z fournit les deux inégalités nécessaires

    18 somme_(u<v) z_u z_v A_uv ≤ 27 somme_u z_u² + (somme_u z_u)²,
    22 somme_(u<v) z_u z_v A_uv ≥ 2(somme_u z_u)² − 44 somme_u z_u².

Le moteur `coheawood_global_cuts.py` résout d'abord les équations linéaires
du bord sur les 2 940 arêtes inconnues. Pour un candidat entier, les
vecteurs propres flottants suggèrent des z ; seuls sont conservés les z
dont la violation est confirmée en arithmétique entière. Les inégalités
elles-mêmes sont exactes et valables pour chaque complétion possible.
Elles sont ajoutées au problème commun, avec les équations des paires
qui sont violées. Un graphe construit ne serait annoncé qu'après
vérification de l'identité SRG en nombres entiers.

Le premier essai révèle un coût de prétraitement excessif à partir de
83 coupes. La reprise sans ce prétraitement utilise les coupes déjà
obtenues et atteint 311 coupes, avec 132 équations supplémentaires de
paires, en 90 secondes. Elle reste UNKNOWN. Les 311 coupes proviennent
de onze candidats globaux rejetés ; ce n'est ni un nombre de familles
C1 exclues, ni une estimation de la fraction restante.

Ces coupes sont également réinjectables dans le modèle **complet** :

```text
python code/codex/coheawood_completion.py --canonical-z --no-presolve \
  --cuts data/codex_coheawood/global_spectral_resume.json \
  --seconds 120 --workers 4 \
  --output data/codex_coheawood/global_complete_with_cuts.json
```

Le fichier de sortie distingue explicitement UNKNOWN d'INFEASIBLE et
d'une construction. Les coupes accumulées sont conservées et peuvent
être reprises ; le moteur corrigé ne répète plus automatiquement un
solveur UNKNOWN sur un modèle identique avec le même budget.

L'essai du modèle complet renforcé est terminé : **UNKNOWN** après
121,3 secondes, avec les 2 940 variables d'arêtes, les 200 655 produits
et les 311 coupes globales. Il ne ferme pas la branche. Aucun calcul
n'est laissé actif et les essais ne seront pas prolongés à paramètres
inchangés comme s'ils apportaient un nouveau résultat.
