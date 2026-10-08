# 197 — Collisions conditionnées par la taille du faisceau de grilles

8 octobre 2026. Proposition de LAB au message 287 ; raffinement des profils,
comptages et certificats par Codex. Un faisceau de taille m est l'ensemble
des grilles contenant une droite Θ fixée. Les tailles donnant des paires
sont m=2,3,4,6 ; la taille cinq est exclue par la note 194.

## 1. Résultats

On fixe deux prismes X1,X2 obtenus en supprimant Θ de deux grilles du
faisceau. Le tableau donne les pertes de **masse six binaire, à somme égale**,
par paire de prismes, avec les deux signes des représentants.

La famille complète est celle de la note 195 : toutes les formes signées
de norme huit de support au plus neuf, avec e(W)≤8 pour `(6,3)`, et avec
toutes les indicatrices `(9,0)` de norme huit.

| Taille du faisceau m | Plafond conjoint c(m) | Composante F0 à triangles négatifs disjoints |
|---|---:|---:|
| 2 | 29144 | 7056 |
| 3 | 29142 | 6970 |
| 4 | 29140 | 6872 |
| 6 | 29140 | 6660 |
| Ancienne borne générique pour une paire de grilles | 29204 | 7304 |

Sans les `(9,0)`, les nouveaux plafonds sont 22372 pour m=2 et 22326 pour
m=6, contre 22422 auparavant. Les cas m=3,4 de cette sous-famille n'ont
pas été optimisés séparément.

Le canal F0 visé par LAB baisse de 644 pour m=6, soit environ 8,8 %.
Le plafond conjoint ne baisse que de 64. Les contraintes introduites ne
fournissent donc pas la division par deux espérée du coût total. Cela ne
prouve pas qu'une réalisation globale pourrait atteindre ces plafonds.

Un calcul dans le sens opposé donne aussi : toute paire de grilles,
si elle existe, entraîne **au moins 14430** collisions de la collection
complète ci-dessus. Ce plancher ne contredit pas à lui seul la cible
exploratoire d'environ 17900 discutée avec LAB.

Enfin, en pondérant les profils locaux de la note 196 par ces coefficients,
on obtient le plafond uniforme exact

    C_6 ≤ 204449226/5,
    donc C_6 ≤ 40889844 par parité.                      (1)

Cette fois les paires hors grille sont également prises en compte, avec
leur coefficient 31976. Le résultat porte uniquement sur C_6 ; les autres
masses et les changements de somme ne sont pas inclus. Aucun rang
supplémentaire n'est exclu. Les références restent τ≤1403 et b3≥45898.

## 2. La partition affinée des 24 points lointains

Pour la paire X1,X2, on conserve B, les soixante points ayant un voisin
dans chaque prisme, et Θ, les trois apices communs. Les 24 points Z
lointains des deux prismes contiennent les m−2 autres prismes du faisceau,
disjoints et anticomplets, ainsi qu'un reste F de taille 36−6m.

Une grille est serrée : tout sommet extérieur possède exactement un
voisin dans la grille. Chaque point de Z voit donc exactement un apex,
tandis que B est anticomplet à Θ. Colorons Z par cet apex.

Chaque apex voit deux sommets dans chacun des m prismes et les deux autres
apices. Il lui reste 12−2m voisins dans F. Les trois cellules colorées de
F ont donc chacune taille **12−2m**.

Le modèle distingue individuellement les six sommets de chaque autre
prisme, mais conserve les trois cellules du reste F. On a ainsi 42,48,54
ou 63 cellules extérieures selon m. Les 36 cellules de B, de tailles un
ou deux, et les trois apices sont ceux de la note 188.

## 3. Degrés et arêtes imposés

On connaît toutes les arêtes dans les m−2 autres prismes et leur absence
entre prismes différents ou entre ces prismes et F. On connaît aussi les
arêtes de Θ et celles reliant chaque point de Z à son apex.

Pour z∈Z, le comptage des voisins communs avec les six sommets de X1
donne 12 : son apex en fournit deux, et chaque voisin dans B en fournit
un. Donc z a dix voisins dans B, un dans Θ et trois dans Z.

L'arête entre z et son apex a un unique voisin commun, qui doit être dans
Z de la même couleur. Avec chacun des deux autres apices, z a deux voisins
communs : son propre apex en est un, l'autre est dans Z de la couleur
considérée. Ainsi

    chaque point de Z a exactement un voisin dans Z de chaque couleur.  (2)

Pour b∈B, ses voisins dans chaque prisme Xi sont au nombre d'un. Si r_c(b)
compte ceux de X1∪X2 dont l'apex a la couleur c, alors b est non adjacent
à cet apex et leurs deux voisins communs donnent

    d_(Z_c)(b)=2−r_c(b).                                (3)

En outre, b possède exactement un voisin dans chacun des m−2 autres
prismes. Il voit donc 6−m points dans F. En particulier, pour m=6 il n'y
a plus de reste F et tous ses voisins dans Z sont répartis dans les
quatre autres prismes.

Les équations (2),(3) sont ajoutées au niveau de chaque cellule. Les
patrons de trois points violant les restrictions individuelles sont
exclus : par exemple, un point de B ne peut voir deux points du même
autre prisme. Les trois apices sont présents dans chaque contrôle local
de λ,μ, même lorsqu'ils ne figurent pas dans le triplet choisi.

## 4. Le sous-cas interdit proposé par LAB

Pour F0 avec triangles négatifs disjoints, les représentants ont la forme
ψ=1_U+1_W0−1_T, où U et T sont des faces de la paire de prismes et W0
est le même trois-ensemble positif pour les deux représentants.
Les points de W0 sont dans B ou Z, et

    e(W)=3+|W0∩B|+e(W0)=7.

Si W0 contient un point de B et deux de Z, il doit donc être un triangle.
Dans un faisceau de six grilles, deux points adjacents de Z appartiennent
au même autre prisme ; le point de B ne peut les voir tous les deux.
Ce sous-cas est donc impossible, conformément à la proposition de LAB.

Le programme retrouve zéro patron de ce type pour m=6. Les patrons
restants comportent deux points de B et un de Z, ou trois points de B.
Leur contribution est encore importante : l'interdiction ci-dessus ne
suffit pas à supprimer la composante dominante entière.

## 5. Comptage, certification et portée du modèle

Les coûts des patrons sont repris des énumérations exhaustives de la
note 195. Les raffinements ne changent pas la forme quadratique d'un
représentant : ils distinguent des cellules qui avaient le même voisinage
sur X1∪X2, puis interdisent des configurations devenues impossibles.

| m | Patrons de deux points | Patrons de trois points | Variables du modèle |
|---|---:|---:|---:|
| 2 | 1620 | 69096 | 69984 |
| 3 | 2079 | 100538 | 101693 |
| 4 | 2574 | 136840 | 138298 |
| 6 | 3375 | 199593 | 201570 |

Le modèle conserve les identités de degré, de voisins communs, de marges
d'arêtes et de triangles des notes 188 et 195. Les constantes exactes des
canaux ne comportant pas de couple de points extérieurs totalisent 4146 ;
elles sont ajoutées une seule fois à l'objectif conjoint.

Chaque optimisation est accompagnée de poids rationnels non négatifs.
Les résidus sont calculés exactement et absorbés par les bornes finies
des variables, comme dans la note 188. L'arrondi final utilise la parité
des comptes signés. Pour le plancher 14430, on majore l'opposé du nombre
de collisions ; la sortie `negative_all_including90≤−14430` est donc
équivalente à ce plancher.

Il s'agit encore d'une relaxation. En particulier, les compatibilités
simultanées entre les voisinages complets des soixante points de B ne
sont pas toutes imposées. Pour m=6, un tel voisinage choisit un sommet
dans chacun des six prismes, avec deux choix de chaque couleur d'apex :
il y a 6!/(2!)³·2⁶=5760 mots possibles avant les contraintes entre points
de B. Le modèle actuel n'utilise pas ces mots complets comme variables.
L'incompatibilité des deux anciens pires cas ne peut donc pas être tenue
pour démontrée sur la seule base du découpage proposé.

## 6. Intégration des coûts dans les moments globaux

Pour une suite locale de degrés (d1,…,d7) du graphe Ξ_v, posons

    w_v=Σ_i binom(d_i,2)c(d_i),

les termes de degré zéro ou un étant nuls. Chaque droite est vue par ses
trois points, donc les pertes de la partie grille sont au plus Σ_v w_v/3.

On reprend les 74 valeurs de s=|{v:e_v≥14}| et les moments de la note
196. Pour chaque triplet de profil (e,c,h), on retient le plus grand w
parmi ses suites de degrés, ce qui conserve une majoration sûre.
Une variable τ_n représente les paires hors grille, avec

    0≤τ_n≤P−6ρ,
    τ_n+(1/3)Σ_v c_v≤1403,
    (1/3)Σ_v c_v≤11ρ+17.

L'objectif est Σ_v w_v/3+31976τ_n. Les 74 certificats donnent (1), avec
le plus grand plafond rationnel pour s=56. Aucune réalisation du modèle
optimisant n'est affirmée. En particulier, on n'a pas multiplié un coût
valable seulement pour les grilles par le nombre de toutes les paires.

## 7. Reproduction

Les patrons et certificats par faisceau sont archivés dans
`data/codex_pencil_M_patterns.json.gz` et
`data/codex_pencil_M_collision_bounds.json.gz`, pour M=2,3,4,6.
Le certificat global est `data/codex_pencil_weighted_moments.json.gz`.

Pour chaque valeur M :

    python code/codex/pencil_collision_bounds.py --size M --generate --verify-only
    python code/codex/pencil_collision_bounds.py --size M --verify-only

Puis :

    python code/codex/pencil_weighted_moments.py --verify-only

Les quatre archives de patrons ont été régénérées et comparées exactement,
tous les certificats locaux ont été relus sans solveur, puis les 74
certificats pondérés ont été vérifiés en arithmétique rationnelle.
