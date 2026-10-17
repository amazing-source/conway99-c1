# 229 — Partenaires cubiques et graphes sans voisin dans un support

9 octobre 2026. Suite au message LAB 437 et à la note 228.

**Résultat.** L'anticomplétude de deux supports positifs propres de valeur
trois suffit à imposer l'égalité de leurs projections normalisées. Le
graphe sans voisin dans un tel support a rayon spectral au plus trois.
Pour un cubique à huit sommets, les composantes cubiques de ce graphe ont
donc taille huit ou seize ; pour un moulin, huit, seize ou vingt-quatre.

Un cubique à huit sommets partenaire d'un moulin a exactement 23, 48 et
20 sommets extérieurs de degrés respectifs zéro, un et deux vers lui.
La présence d'un seul degré extérieur au moins trois interdit donc tout
partenaire moulin. Des restrictions supplémentaires de degrés locaux
sont démontrées au §4, sans hypothèse de rang ou d'absence de prismes.

Ces implications ne suppriment pas encore un des 174 noyaux C1, ni un
des 359 supports positifs de la note 228. Le nouveau pilote d'arêtes du
§5 laisse ses cinq entrées ouvertes ; il n'est pas étendu par défaut.

## 1. L'anticomplétude suffit

Dans un hypothétique SRG(99,14,1,2), posons

    E=(3I−A+J/9)/7.

Soient u,v des vecteurs positifs sur deux supports disjoints et
anticomplets S,T. Supposons A[S]u=3u et A[T]v=3v. Notons s=Σu et t=Σv.
Alors

    ||Eu||²=s²/63,   ||Ev||²=t²/63,   <Eu,Ev>=st/63.

L'égalité dans Cauchy donne

    Eu/s = Ev/t,       A(tu−sv)=3(tu−sv).                 (1)

En particulier, pour deux cubiques à huit sommets, il suffit de vérifier
qu'ils sont anticomplets : il n'y a pas de condition supplémentaire
d'égalité des voisinages extérieurs à tester dans le graphe C1 complet.
Il en va de même pour un cubique à huit sommets et un moulin pondéré
u=2e_v+1_L de masse huit.

**Forme directe transmise par LAP via LAB 442.** Si z est porté par S
et A[S]z=3z, écrivons Az=3z+e, où e est porté hors de S. L'identité
A²=12I−A+2J donne

    ||Az||²=9||z||²+2(Σz)²,       ||e||²=2(Σz)².

Un vecteur propre interne de somme nulle se prolonge donc automatiquement
en vecteur propre global. Appliqué à z=tu−sv, cela redonne (1). Pour
les composantes C_i,C_j d'un graphe proche de triangle, il s'applique
à |C_j|·1_C_i−|C_i|·1_C_j et retrouve l'équilibre de leurs ombres
utilisé dans la note 225. Ce raccord est une autre preuve d'un acquis,
pas une nouvelle exclusion. Les composantes de tailles 12,18,24 de
la campagne LAP n'épuisent pas les partenaires cubiques huit étudiés ici.

## 2. Confinement spectral et composantes

Écrivons Z(S) pour les sommets hors de S n'ayant aucun voisin dans S.
Pour un vecteur réel x porté par Z(S), posons

    y=x−(Σx/s)u.

Comme Σy=0, l'anticomplétude et A[S]u=3u donnent

    0 ≤ 7<y,Ey> = xᵀ(3I−A[Z(S)])x.

Ainsi

    3I−A[Z(S)] est positive,       ρ(A[Z(S)])≤3.          (2)

Tout sous-graphe induit connexe de Z(S) ayant valeur propre de Perron
trois est une composante entière de Z(S). En effet, son vecteur de
Perron positif v satisfait (1). Pour z dans Z(S) hors de son support,
cette égalité donne (Av)(z)=0 ; il ne peut donc voir ce support.

En particulier tout cubique induit connexe contenu dans Z(S) est
automatiquement une composante. Le message LAB 437 donnait déjà cette
nécessité pour les partenaires de même projection ; (1) fournit aussi
la réciproque et (2) s'applique au reste du graphe.

Le message LAB 439 propose de détecter ces composantes par
det(3I−A[Z(S)])=0. Cette équivalence concerne un partenaire positif de
**masse quelconque, après normalisation**. Elle ne détecte pas à elle
seule une collision de masse huit : une composante cubique connexe de
seize points, par exemple, correspond à 2·1_U−1_C de masse seize.

## 3. Divisibilité et profils forcés

Pour un cubique U à huit sommets, notons n_k le nombre de sommets
extérieurs ayant k voisins dans U. Les équations du SRG donnent

    Σ n_k=91,       Σ k n_k=88,       Σ binom(k,2)n_k=20.

D'où

    n_0=23−Σ_{k≥3} binom(k−1,2)n_k ≤23,
    n_1=48+Σ_{k≥3} k(k−2)n_k ≥48.                       (3)

Pour un moulin pondéré u de masse huit, tout sommet extérieur a degré
pondéré zéro, un ou deux. Un voisin extérieur du centre ne peut voir
une feuille, par λ=1 ; un non-voisin du centre voit au plus deux
feuilles, par μ=2. Les moments extérieurs sont Σd=88 et Σd²=128,
d'où les effectifs exacts

    (n_0,n_1,n_2)=(24,48,20).                            (4)

Soit C un cubique induit connexe anticomplet à U ou au moulin. Un des
48 sommets au moins de degré (pondéré) un est extérieur aux deux
supports. Par (1), son nombre de voisins dans C vaut |C|/8. Ainsi

    8 divise |C|.                                       (5)

Avec (3)–(4), les tailles possibles sont {8,16} dans Z(U) et {8,16,24}
dans Z(moulin). Le message LAB 437 en déduisait déjà au plus trois
cubiques par classe, ou au plus trois cubiques et un moulin.

Si U est lui-même partenaire d'un moulin W, (1) impose d_U=d_W à
l'extérieur des deux supports. Sur W, d_U=0. Par conséquent aucun
sommet extérieur à U ne peut avoir trois voisins dans U, et (3) devient

    (n_0,n_1,n_2)=(23,48,20).                            (6)

Pour le cube 2022000, cette condition est déjà automatique, comme le
signale LAB 439 : deux points d'une même part de sa bipartition ont
déjà deux voisins communs dans le cube. Un sommet extérieur voit donc
au plus un point de chaque part. Le critère n'interdit des partenaires
moulins que pour les deux autres types de cubiques.

De plus W est une composante de Z(U), U une composante de Z(W), et

    Z(U)=W ⊔ R,       Z(W)=U ⊔ R,       |R|=16,          (7)

où les unions sont anticomplètes et ρ(A[R])≤3. Dans les coordonnées de
la note 228, R est précisément l'ensemble des seize cellules extérieures
de profil {x,x′}⊂X. Ces cellules ont chacune effectif un. Les arêtes de
R restent inconnues ; (7) n'affirme pas qu'il est cubique.

## 4. Restrictions locales de degrés

Pour un sommet z de Z(S), notons d son degré dans Z(S) et t le nombre
d'arêtes entre ses voisins dans Z(S). Ces arêtes forment un appariement.
L'étoile avec ces t arêtes a, dans 3I−A, complément de Schur central

    3−(d−2t)/3−2t/2=(9−d−t)/3.

Par (2), d+t≤9. D'autre part chaque voisin non apparié dans Z(S) a,
avec z, un troisième point de triangle hors de Z(S). Ces points sont
distincts. Le degré ambiant quatorze impose d−t≤7.

Pour S un cubique huit ou un moulin pondéré, les cas d+t=9 autres
que (d,t)=(6,3) sont impossibles. Les seuls cas à considérer sont
(9,0),(8,1),(7,2),(6,3). Le premier viole déjà d−t≤7. Dans les cas
(8,1),(7,2), l'étoile est une composante de Z(S), par égalité dans (2),
et possède un vecteur propre positif w de masse 24 : poids six au
centre, trois aux feuilles appariées, deux aux autres.

Prenons une feuille non appariée. Le troisième point de son arête
avec le centre est extérieur aux deux supports. Il ne voit dans cette
étoile que le centre et cette feuille, car le voisinage du centre est
un appariement. Son degré pondéré vers w vaut donc huit. Or (1) impose
Aw=3Au en ce point, contradiction modulo trois.

On obtient :

- dans Z(U), d≤7 ; l'égalité d+t=9 ne peut provenir que d'une
  composante moulin de trois triangles, unique par la note 227 ;
- dans Z(W), d≤6 et d+t≤8. En effet A²u=12u−Au+16·1 donne, en
  z∈Z(W), Σ_{x~z}(Au)(x)=16. Seuls les 14−d voisins hors de Z(W)
  contribuent, chacun au plus deux ; donc d≤6. Le cas (6,3) serait
  un second moulin anticomplet à W, interdit par (1) et la note 227.

Ces interdictions portent sur le graphe entier Z, y compris les
composantes qui ne sont pas cubiques.

## 5. Nouveau pilote : arêtes entre cellules forcées

On utilise les 359 supports H de la note 228 sans refaire leurs tests
H/H+1. La cellule i a masque b_i sur H et effectif c_i. Pour les nombres
d'arêtes e_ij entre cellules, les équations nécessaires sont

    Σ_{j≠i} e_ij + 2e_ii = c_i(14−|b_i|),
    Σ_{j≠i} e_ij b_j + 2e_ii b_i
        = c_i(2·1−b_i−A_H b_i).                         (8)

La seconde ligne compte les voisins communs d'un point de la cellule i
et de chaque sommet de H, puis somme sur la cellule. On interdit les
arêtes épuisant déjà un budget λ ou μ avec H. La cellule {v} contient
trois arêtes internes. Deux points d'une même cellule de paire ont
déjà deux voisins communs dans H ; leurs voisinages extérieurs sont
donc disjoints, ce qui impose e_ij≤c_j pour une telle cellule double.

Les cinq indices 0,29,151,200,358 du catalogue ordonné, couvrant les
trois types de cubiques, satisfont la relaxation fractionnaire (8).
**Aucune exclusion.** Ce n'est pas un prolongement en graphe, et le
pilote ne traite pas l'ensemble des 359 cas. Le calcul achevé prend
environ 1,1 seconde ; aucune recherche prolongée n'est laissée active.

- `code/codex/positive18_cell_edges.py`
- `data/codex_positive18_cell_edges_pilot.json`

Le diagnostic global de LAB 437 est utilisé comme acquis : les nouvelles
bornes de collisions restent trop larges. L'étape suivante doit porter
sur l'existence des composantes partenaires, ou sur une obstruction
structurelle dans R, et non sur une nouvelle certification de plafonds
numériques loin de la cible.

**Complément LAB 439 utilisé sans reproduction :** le comptage d'ordre
dix de U disjoint-anticomplet à une arête majore les partenaires cubiques
par e(Z(U))/12, mais cette majoration est trop large sur tout son polytope.
Ne pas relancer cette piste de comptage comme si elle n'avait pas été
essayée. La coupe e(Z(U))≤34 issue de (2) reste valide ; elle ne fournit
pas, à elle seule, une exclusion annoncée par LAB.
