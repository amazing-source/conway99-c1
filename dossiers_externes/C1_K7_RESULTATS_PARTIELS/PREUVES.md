# K7 sous α = 22 — résultats partiels démontrés

## Portée et sources

Objet : un hypothétique SRG(99,14,1,2) Γ muni d'une coclique de Hoffman C de 22 points.
Notations du dépôt `amazing-source/conway99-c1`, branche `claude/v7-simultaneous`,
révision consultée `fd7a1f1c90410b3514b2ce1974ef64f1370c5305` :

- `notes/171_BORDS_SERRES_HOFFMAN.md` ;
- `notes/172_RESEAU_Q_ALPHA22.md` ;
- `notes/173_CONJECTURE_K7.md`.

Le dossier antérieur `C1_HOFFMAN_ARITHMETIQUE` fournit la classification ternaire
et le lemme des deux cocliques se coupant en quinze points. Ce lemme est rappelé
ci-dessous uniquement pour rendre la preuve conditionnelle autonome.

**K7 n'est ni démontrée ni réfutée ici.** Les configurations (i) et (ii) ne sont
pas exclues en général. Les résultats nouveaux de cette analyse sont la connexité,
le rang local qui en découle, et les restrictions conditionnelles du §3. Aucune
priorité bibliographique n'est revendiquée. Les preuves ne sont pas formalisées
et n'ont pas fait l'objet d'une relecture humaine externe.

## 0. Les identités utilisées

F a 77 sommets. Y est l'incidence C × F, D l'adjacence sur F, et N = YᵀY.

    YYᵀ = 12I + 2J,       YD = 2J − Y,
    D² + D = 12I + 2J − N,       D1 = 10·1.

On a aussi Y1 = 14·1 et Yᵀ1 = 4·1. En particulier :

    N² = 12N + 32J,   DN = ND = 8J − N,
    NJ = JN = 56J,    DJ = JD = 10J,    J² = 77J.

Posons, comme dans les notes 171–172,

    Q = 9I − 3D − N + J.

Un développement avec les cinq identités précédentes donne

    Q² = 21Q,       QYᵀ = 0,       Q1 = 0,       Qii = 6.

Q est symétrique : ses valeurs propres sont 0 et 21. Il est donc positif
semi-défini, et son rang est tr(Q)/21 = 77·6/21 = 22. On peut écrire
Qij = ⟨v_i,v_j⟩ pour 77 vecteurs v_i de R²².

**Usage de Hoffman.** Les identités de Y, et notamment le degré quatre vers C,
proviennent de l'égalité dans la borne de Hoffman. L'existence de Q avec cette
formule et cette identité polynomiale n'est pas affirmée pour une coclique
arbitraire de taille inférieure à 22.

## 1. Théorème universel : le quotient sur les sept mates est connexe

Fixons c ∈ C, W = N(c), G l'adjacence de Γ_c sur W, et M = M_c.
Chaque point de C\{c} correspond à une arête de Γ_c. Chaque sommet de Γ_c a degré
3 : son bloc contient c et trois autres points. Les mates n'ont pas d'arête dans G.

### Théorème 1

Le graphe Γ_c ∪ M_c est connexe. Par conséquent le multigraphe Γ_c/M_c sur sept
sommets est connexe. Cela vaut pour tous les c ∈ C, sans hypothèse ternaire.

### Preuve

Sur W, D[W,W] = M. Le Gram des blocs vaut

    N[W,W] = 3I + J + G.

En effet, sa diagonale vaut 4 ; deux blocs distincts contiennent c, et leur
intersection contient un second point de C exactement lorsqu'ils sont reliés
par une arête de Γ_c. Ainsi

    Q[W,W] = 6I − 3M − G.                       (1)

C'est le laplacien du graphe pondéré qui donne poids 1 aux arêtes de Γ_c et poids
3 aux mates. Pour tout vecteur réel h sur W,

    hᵀ Q[W,W] h = Σ_{ab∈E(Γ_c)} (h_a−h_b)²
                    + 3 Σ_{ab∈M_c} (h_a−h_b)².       (2)

Supposons S une composante connexe propre et non vide de Γ_c ∪ M_c. Étendons
u = 1_S par zéro aux 77 coordonnées de F. Alors uᵀQu = 0 d'après (2). L'identité
Q²=21Q implique

    ||Qu||² = uᵀQ²u = 21uᵀQu = 0,

donc Qu=0.

Mais S est fermé par M, donc |S| est pair. Pour un point x ≠ c de C, les deux
blocs contenant {c,x} sont les deux extrémités d'une arête de Γ_c : ils sont
soit tous deux dans S, soit tous deux dehors. Par conséquent

    (Yu)_c = |S|,       (Yu)_x ∈ {0,2} pour x ≠ c.

**Yu est un vecteur entier pair**, et Nu = YᵀYu aussi.

Prenons a ∈ S et b ∈ W\S. Ce ne sont ni des mates, ni les extrémités d'une arête
de Γ_c. Le second voisin commun z_ab n'appartient donc pas à C : c'est un sommet
de F\W. Ses deux seuls voisins dans W sont a et b, d'où

    u_{z_ab}=0,       (Du)_{z_ab}=1.

La formule de Q donne alors

    (Qu)_{z_ab} = |S| − 3 − (Nu)_{z_ab}.

Le membre de droite est impair, tandis que Qu=0. Contradiction. ∎

### Corollaires exacts

1. Le bloc Q[W,W] a rang **13** sur R. Sa seule relation linéaire entre les
   quatorze vecteurs v_a est Σ_{a∈W}v_a=0.
2. Le quotient ne peut pas se décomposer en composantes de tailles 3 et 4.
   C'est la seule partition de 7 en tailles de composantes possibles avant ce
   théorème : une composante à une ou deux fibres ne permettrait pas un degré
   trois dans Γ_c. Une composante de trois fibres aurait nécessairement trois
   arêtes entre chacune des trois paires de fibres.
3. En choisissant treize sommets I ⊂ W, B=Q[I,I] est définie positive. Avec
   U=F\W (63 sommets), le complément de Schur

       Q[U,U] − Q[U,I] B⁻¹ Q[I,U]

   est positif semi-défini de rang **9**. En effet, le quatorzième vecteur de W
   est la somme opposée des treize autres, et supprimer cette coordonnée ne
   change pas le rang 22 de Q. Cette réduction est valable **sans K7**. Elle
   ne choisit pas les inconnues de la matrice ni ne prouve leur existence.

La connexité est strictement plus faible que la simplicité. Le §4 fournit un
exemple local explicite qui respecte cette connexité avec n_ef=4.

## 2. Reformulation géométrique exacte du défaut K7

Cette section est une traduction de la conjecture, **pas une preuve supplémentaire**.

Pour e={a,a′} ∈ M_c, posons w_e=v_a+v_{a′}. La formule de Q donne

    ||w_e||² = 6,       Σ_e w_e = 0,
    ⟨w_e,w_f⟩ = −n_ef pour e≠f,
    ||w_e+w_f||² = 12−2n_ef.                    (3)

Le Gram des sept w_e est le laplacien 6I−(n_ef), de rang 6 par le théorème 1.

| n_ef | ||w_e+w_f||² |
|---:|---:|
| 0 | 12 |
| 1 | 10 |
| 2 | 8 |
| 3 | 6 |
| 4 | 4 |

Ainsi K7 équivaut à : ces sept vecteurs forment un simplexe régulier de Gram
7I−J. Elle équivaut aussi à l'absence des normes 4,6,8 **dans la collection
marquée des 21 sommes w_e+w_f**. Il serait incorrect de remplacer cette
collection par tous les vecteurs du réseau L : celui-ci contient déjà les
vecteurs v_i et w_e de norme 6.

Les identités de défaut, valables pour chaque c, sont

    Σ_{e<f} n_ef = 21,
    Σ_{e<f} n_ef² = 21 + tr(G²M) + ½ tr((GM)²).

Si I_c compte les couples d'arêtes de Γ_c partageant une extrémité et dont les
extrémités restantes sont mates, et J_c compte les couples diagonaux, alors

    tr(G²M)=2I_c,       tr((GM)²)=4J_c,
    Σ_{e<f} binom(n_ef,2)=I_c+J_c.

Ces formules ne donnent pas la nullité des deux traces.

## 3. Théorème conditionnel dans le type ternaire (7,15,0)

Supposons que ker_F3(Yᵀ) contienne 1_Z pour un ensemble Z ⊂ C de taille 15.
Posons S=C\Z, |S|=7. C'est le type ternaire de dimension un à un signe près
identifié dans le dossier antérieur. La preuve qui suit ne nécessite que
l'existence du mot 1_Z, pas la classification exhaustive des six types.

### Rappel démontré : une seconde coclique

Chaque bloc rencontre Z en zéro ou trois points, donc rencontre S en quatre ou
un point. Soit T l'ensemble des blocs contenus dans S.

Les 42 occurrences de paires de S sont toutes contenues dans les blocs de T,
chacun contribuant six occurrences. Donc |T|=7. Chaque point de S appartient à
quatre blocs de T : ils constituent un design 2-(7,4,2). En particulier deux
blocs distincts de T ont exactement deux points communs. Cela se voit aussi en
fixant un bloc : ses six paires doivent être reprises par les six autres blocs,
avec une contribution au plus un par bloc puisque les intersections sont ≤2.

De plus

    Yᵀ1_S = 1 + 3·1_T.

En multipliant par D et en utilisant DYᵀ=2J−Yᵀ et D1=10·1, on obtient

    D1_T = 1−1_T.                               (4)

Donc T est indépendant, et chaque sommet de F\T possède exactement un voisin
dans T. Comme les blocs de T sont contenus dans S, Z∪T est une seconde coclique
de Hoffman C′, avec |C∩C′|=15. Cette construction était déjà démontrée dans le
dossier ternaire ; elle n'est pas revendiquée comme nouvelle ici.

### Théorème 2

Pour tout c∈S (les **sept** points de couleur zéro), on a

    n_ef ≤ 3 pour toutes les paires e,f.

Plus précisément, les sept paires de mates en c se répartissent en quatre
paires mixtes et trois paires pures. Les 21 quadruplets satisfont :

| paire de fibres | nombre de quadruplets | valeurs possibles de n_ef |
|---|---:|---|
| deux mixtes | 6 | 1 ou 2 |
| une mixte et une pure | 12 | 0,1,2 |
| deux pures | 3 | 0,1,2,3 ; un sommet déterminé du quadruplet est dans T, donc hors C |

En particulier **n_ef=4 est exclu aux sept points de S**. Une valeur 3 ne peut
apparaître que dans les trois quadruplets entre fibres pures. Rien n'est affirmé
par cette borne sur les quinze points de Z.

### Preuve

Fixons c∈S et notons T_c les quatre blocs de T contenant c. Les quatorze voisins
de c se répartissent en T_c (quatre sommets) et U_c=N(c)\T (dix sommets). Chaque
u∈U_c a pour bloc {c} plus trois points de Z.

Par (4), u a un unique voisin t(u) dans T. S'il appartient à T_c, les sommets
c,u,t(u) forment un triangle : u et t(u) sont donc mates en c. Inversement,
chacun des quatre t∈T_c est apparié dans N(c) à un sommet de U_c, car T est
indépendant. On obtient quatre paires mixtes et trois paires pures sur les six
sommets restants de U_c.

Pour ces six sommets purs, t(u) appartient à T\T_c, qui a trois éléments.
Chaque t∈T\T_c est non adjacent à c, et ses deux voisins communs avec c sont
deux sommets purs de U_c. Chaque valeur t est donc prise exactement deux fois.
Cela définit un second appariement L sur les six sommets purs.

L est disjoint de l'appariement M_c : deux mates ont déjà c comme voisin
commun et ne peuvent en avoir un autre t∈T. L∪M_c est donc un cycle alterné
sur six sommets. En contractant les trois mates, les trois arêtes de L forment
un triangle simple. Ainsi, pour chaque paire de fibres pures e,f, il y a
exactement un couple u∈e,v∈f avec t(u)=t(v). Pour ce couple,

    z_uv = t(u) ∈ T ⊂ F.

Le quadruplet possède donc un sommet hors C, ce qui prouve n_ef≤3 dans ce cas.

Pour une paire mixte {t,u} et une pure {v,w}, les intersections de blocs
B_t∩B_v et B_t∩B_w valent exactement {c} : B_t⊂S tandis que B_v,B_w rencontrent
S en {c}. Par conséquent z_tv et z_tw ne sont pas dans C. Il reste au plus deux
positions dans C.

Enfin, pour deux paires mixtes {t,u},{t′,u′}, les positions z_tu′ et z_ut′ ne
sont pas dans C pour la même raison. Comme deux blocs distincts de T
s'intersectent en deux points, z_tt′ est le second point de B_t∩B_t′, donc
appartient à S\{c}. La position z_uu′ est libre à ce stade. D'où n_ef∈{1,2}. ∎

### Ce que cela dit des motifs (i) et (ii)

- Entre deux paires mixtes, la valeur 2 ne peut être qu'un motif diagonal (ii).
- Entre une paire mixte et une paire pure, la valeur 2 ne peut être qu'un motif
  latéral (i).
- Entre deux paires pures, les deux motifs restent possibles ; une valeur 3
  implique des occurrences des deux.

**Ni (i) ni (ii) n'est donc exclu globalement par ce théorème.**

### Usage explicite de Hoffman

On utilise les degrés quatre vers C, le design, DYᵀ=2J−Yᵀ et D1=10·1 pour
obtenir (4). C'est (4), autrement dit l'existence du voisin unique dans T, qui
fournit les trois étiquettes et l'obstruction à n=4. On ne suppose aucun
automorphisme ni aucune grille. Le mécanisme ne s'applique pas à Paley(9) :
il n'y a ni ces ensembles de tailles 15 et 7, ni ce design 2-(7,4,2).

## 4. Un test local explicite — PAS un contre-exemple à K7

`data/local_fixture.json` donne un graphe cubique G sur les quatorze blocs et
le matching M={(0,1),(2,3),...,(12,13)}. Leur union est connexe, mais
n_{ {0,1},{2,3} }=4. Le laplacien local a rang 13, et ses deux traces de défaut
valent respectivement 8 et 28. La somme des carrés des multiplicités vaut 43.

Le vérificateur construit une **matrice partielle** sur 99 sommets :

- les 22 points de C sont indépendants ;
- c est adjacent aux 14 blocs, qui induisent M ;
- les 84 sommets à distance deux sont identifiés aux 84 paires non mates ;
- les 21 arêtes de G désignent les autres points de C ;
- les 63 autres paires désignent les sommets de F\N(c) ;
- toutes les incidences impliquant c ou un de ses 14 voisins sont fixées.

Les quinze lignes c et N(c) ont degré 14. Chacun des quatorze blocs par c a
exactement quatre voisins dans C. Toutes les 98 équations de voisins communs
entre c et un autre sommet, et toutes les 91 équations entre deux sommets de
N(c), sont vérifiées exactement. La positivité du Gram local découle de (2).

**Il reste 3 276 arêtes indéterminées**, entre les autres points de C et les
63 blocs lointains, et entre ces 63 blocs. En particulier le design complet,
les degrés de ces autres sommets, les autres conditions de Hoffman et les
équations restantes ne sont pas réalisés. Les inconnues restent marquées
`None` ; elles ne sont pas transformées silencieusement en non-arêtes.

Ce témoin ne constitue donc ni un SRG, ni un contre-exemple à K7, ni une preuve
que sa complétion existe. Il vérifie seulement que le modèle enraciné initial,
la cubicité, la connexité et le Gram local ne suffisent pas à imposer K7.
Il n'est pas non plus un test de suffisance des identités spectrales **globales**
de D et N, qui n'y sont pas imposées.

## 5. Ce qui reste à prouver

Pour chaque point c, il reste à éliminer les normes 8,6,4 dans la collection
marquée (3), ou à prouver directement la nullité des deux traces de défaut.
La connexité ne le fait pas. Le théorème 2 interdit seulement le cas maximal
n=4 sous l'hypothèse ternaire indiquée, en sept points.

Aucune des conclusions du dossier ne permet d'imposer K7 dans un solveur
couvrant le cas α=22. En revanche la connexité, le rang local 13, le rang
résiduel 9 et les restrictions conditionnelles sont utilisables avec leurs
hypothèses exactes.
