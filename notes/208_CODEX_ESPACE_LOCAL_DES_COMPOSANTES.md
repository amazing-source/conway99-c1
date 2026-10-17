# 208 — L'espace hyperbolique universel des composantes autour d'un sommet

8 octobre 2026. Prolonge les notes 205–206 et les formules d'intersection
transmises par LAP, via LAB, au message 348 du pont.

**Théorème.** Tous les Grams centrés des composantes des sept droites
passant par un sommet sont représentables dans un espace hyperbolique
fixe de dimension 14 sur F₇. Leurs rangs sont donc au plus 14. Cette
borne vaut pour tous les systèmes de partitions, sans échantillonnage.

Il en résulte que les seuls Grams de composantes autour d'un sommet
ne peuvent exclure aucun des rangs globaux 37,39,41 : leurs espaces
ambiants centrés sont hyperboliques de dimensions 18,16,14. Au rang
43, de dimension centrée 12, ce test peut encore produire des
obstructions. Cette conclusion concerne ce test quadratique précis,
pas toutes les contraintes combinatoires d'un voisinage.

## 1. Les vingt et un vecteurs formels

Fixons v et ses sept droites L₀,…,L₆. Chaque paire ij définit neuf
points : v, les quatre autres points de Lᵢ∪Lⱼ, et les quatre coins
correspondants parmi les 84 points à distance deux. Notons gᵢⱼ leur
indicatrice, que ces neuf points soient ou non une véritable grille.

Ces vecteurs formels sont définis par les coordonnées du voisinage,
indépendamment des arêtes entre les 84 points. En entiers,

    <g_e,g_f> = 9 si e=f,
               3 si |e∩f|=1,
               1 si e∩f=∅.

Une composante C de la boule cubique de Lᵢ détermine un bloc B des six
autres droites à v. Si m=|B|, elle contient les deux points de chaque
Lⱼ−v, j∈B, et les quatre coins ij associés. Ainsi |C|=6m et

    κ(i,B) = 1_C + m 1_Lᵢ = Σ_{j∈B} gᵢⱼ.             (1)

C'est une égalité de 99 coordonnées entières. Le cas m=1 retrouve
l'indicatrice d'une véritable grille.

## 2. Formules d'intersection

Pour deux blocs B,B′ de la même ligne i, on a plus généralement

    <κ(i,B),κ(i,B′)> = 6|B∩B′| + 3mm′.

Pour i≠j,

    <κ(i,B),κ(j,B′)> = 2|B∩B′| + 4[j∈B][i∈B′]
                      + 2m′[j∈B] + 2m[i∈B′] + mm′.

Ces formules vérifient celles de LAP. Comme Σκ=9m, le centrage sur
F₇ est κ′=κ−2m·1, puisque <1,1>=99≡1. Le produit centré s'obtient
en soustrayant 81mm′ **modulo 7**. Il ne s'agit pas de cette même
formule de centrage orthogonal en caractéristique zéro.

Le script `code/codex/local_component_space.py` contrôle les 441 blocs
non vides possibles et leurs 97 461 produits non ordonnés, diagonale
comprise, directement dans les 99 coordonnées entières.

## 3. Un quotient hyperbolique de dimension quatorze

Soit C la matrice d'incidence non orientée 7×21 du graphe complet K₇.
Le Gram des g′=g−2·1 est

    Γ = 4I₂₁ + 2CᵀC − 3J₂₁,             sur F₇.

Or CCᵀ=5I₇+J₇ est inversible sur F₇, de déterminant 5. En particulier
C est de rang 7. On vérifie ΓCᵀ=0. Sur ker C, Γ agit par 4I ; en
effet Ca=0 implique également Σa=0. On obtient la décomposition
orthogonale, pour le produit standard des coefficients,

    F₇²¹ = im Cᵀ ⊥ ker C,
    ker Γ = im Cᵀ,
    E = F₇²¹ / im Cᵀ ≅ ker C,            dim E = 14.

Le discriminant du produit standard sur im Cᵀ a la classe de 5,
non carrée. Celui sur ker C a donc aussi une classe non carrée,
puisque le produit standard de dimension 21 a déterminant 1.
La multiplication du Gram par 4 ne change pas cette classe. Une forme
de dimension 14 est hyperbolique exactement lorsque son déterminant
a la classe de (−1)⁷, non carrée dans F₇. **E est donc hyperbolique.**

Le vérificateur fournit en outre un mineur principal de taille 14,
de déterminant 3 modulo 7, et contrôle les sept directions du noyau.

## 4. Ces sept directions sont de vraies relations de classes

Il faut distinguer le noyau d'un Gram et une véritable relation dans
le quotient arithmétique. Ici les sept relations se relèvent
explicitement, comme dans la note 206.

Pour z=(z₀,…,z₆), Z=Σzᵢ, plaçons y(v)=Z, y=zᵢ sur les deux autres
points de Lᵢ, et y=0 sur les 84 points restants. En entiers,

    (A+4I)y = Σ_{i<j}(zᵢ+zⱼ)gᵢⱼ.                       (2)

Comme Σ_{i<j}(zᵢ+zⱼ)=6Z, le vecteur centré de droite vaut modulo 7

    (A+4I)y − 5Z·1.

Ce vecteur appartient à im(A−3I)∩1⊥, donc au radical R de la
réduction de K₊ décrit en note 205. On peut également constater son
appartenance à la réduction du réseau d'eigenvaleur 3 par le relèvement
entier

    11(A+4I)y − 6Z·1,

qui est un eigenvecteur de valeur 3 et réduit à quatre fois le vecteur
centré précédent. Ainsi toutes les combinaisons de composantes dont
les coefficients formels sont dans im Cᵀ ont réellement classe nulle.

On ne prétend pas que chaque gᵢⱼ formel ait lui-même une classe dans
K₊ : seuls les blocs provenant de composantes réelles, et leurs
combinaisons, sont utilisés à cette étape.

## 5. Compter plus finement par un graphe de blocs

Construisons F_v : un sommet pour chaque bloc composante (i,B) et,
pour chaque paire ij, une arête joignant le bloc de i contenant j au
bloc de j contenant i. Il a exactement 21 arêtes. Posons

    n = Σ_i c_i,
    b = nombre de composantes connexes biparties de F_v.

La matrice W des blocs en coordonnées gᵢⱼ est précisément l'incidence
non orientée de F_v. Sa transposée impose x_s+x_t=0 sur chaque arête.
Sur un corps de caractéristique différente de 2, son noyau a une
dimension par composante bipartie et zéro par composante non bipartie.
Donc rang W=n−b, également sur F₇.

En sommant les lignes de W de chaque famille i, on obtient la ligne
i de C. Ainsi im Cᵀ est contenue dans l'espace des coefficients des
blocs. Après les sept relations de (2), ce dernier a dans E la
dimension exacte

    h = n − b − 7 ≤ 14.                                  (3)

Les b relations d'incidence biparties sont déjà des égalités entières
entre les κ. Les sept relations supplémentaires sont des égalités de
classes issues du voisinage fermé. S'il existe d'autres relations
dans le quotient global, elles peuvent encore abaisser la dimension.

En notant d la dimension des vraies classes locales et q leur rang
de Gram, on a donc

    max(0,2h−14) ≤ q ≤ d ≤ h ≤ 14.                        (4)

La première inégalité vient de ce qu'un sous-espace de dimension h
d'un espace non dégénéré de dimension 14 a un radical de dimension
au plus 14−h. Le Gram local est exactement WΓWᵀ. Il ne faut pas
identifier systématiquement q, d et h.

Exemples vérifiés, considérés comme systèmes formels de partitions :

| Partitions des sept lignes | n | b | h | q |
|---|---:|---:|---:|---:|
| un bloc de six à chaque ligne | 7 | 0 | 0 | 0 |
| six singletons à chaque ligne | 42 | 21 | 14 | 14 |
| deux blocs de trois issus du tournoi cyclique sur sept points | 14 | 1 | 6 | 5 |

Aucune réalisabilité simultanée de ces exemples dans un SRG n'est
affirmée. Le dernier exemple illustre la distinction h≠q.

## 6. Portée pour la recherche

D'après la note 205, l'espace global centré associé à un rang r a
dimension 55−r et est hyperbolique. Pour r=37,39,41, l'espace E de
dimension 14 s'y plonge isométriquement. Tous les Grams précédents
y sont donc représentables, avec les relations locales connues.

Ainsi une recherche fondée uniquement sur ces Grams à un sommet ne
peut fournir la contradiction souhaitée pour ces trois rangs. Il faut
y ajouter une information supplémentaire : produits entre composantes
attachées à plusieurs sommets, couplage de plusieurs étoiles, ou une
contrainte arithmétique/combinatoire non contenue dans ce Gram.

Cette obstruction à une méthode est uniforme ; elle remplace les
30 000 essais mentionnés par LAP pour ce plafond. Elle ne clôt aucun
nouveau rang global. Au rang 43, la dimension ambiante n'est que 12,
ce qui explique pourquoi les tests locaux des notes 205–206 restent
utiles dans ce cas.

Validation :

    python code/codex/local_component_space.py --verify-only

Données : `data/codex_local_component_space.json`.
