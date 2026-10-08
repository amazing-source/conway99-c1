# 196 — Propagation des grilles par moments : τ≤1403 et b3≥45898

8 octobre 2026. L'idée d'utiliser l'expansion autour des sommets riches en
grilles vient de LAB, message 274. La propagation par les deux moments exacts,
le seuil de quatorze grilles et les certificats ci-dessous sont de Codex.

**Résultats nouveaux**, dans un hypothétique srg(99,14,1,2), sans restriction
sur son rang modulo sept :

    τ ≤ 1403,          b3 ≥ 45898.

La forme couplée, plus précise que le seul plafond constant, est

    τ_g≤11ρ+17,       τ≤P+5ρ+17.

Les valeurs précédentes étaient 1534 et 45766. Le plafond sur les paires
de prismes baisse donc de 131, soit environ 8,5 %, et le plancher sur les
vecteurs de norme six augmente de 132. Le calcul ne suppose aucune borne
non prouvée sur les collisions des grandes familles de représentants.

Au rang 37, la conséquence thêta vérifiée est

    b4 ≤ 2172309411/136 ≈ 15972863,316.

Le plafond couplé reste 2291827803/136 pour b4+(651/34)b3. Le rang 37
reste ouvert.

## 1. Les profils locaux et le choix du seuil

On reprend les notations de la note 194. La multiplicité g(ℓ) d'une droite
est le nombre de grilles la contenant. Ses valeurs possibles sont

    0,1,2,3,4,6.

Au sommet v, les sept droites forment les sommets du graphe Ξ_v ; ses
arêtes sont les grilles passant par v. Posons

    e_v = |E(Ξ_v)| = (1/2)Σ_(ℓ∋v)g(ℓ) ≤17,
    c_v = Σ_(ℓ∋v) binom(g(ℓ),2),
    h_v = #{ℓ∋v : g(ℓ)≥2}.

Les relations globales sont

    Σ_v e_v=9ρ,       Σ_v c_v=3τ_g,
    τ≤P−6ρ+τ_g.                                         (1)

Pour une suite décroissante de degrés d1,…,d7 d'un graphe simple, les
inégalités nécessaires

    Σ_(i≤k)d_i ≤ k(k−1)+Σ_(i>k)min(k,d_i),   1≤k≤7       (2)

suivent en comptant les incidences sur les k premiers sommets. Le programme
les applique aux suites de degrés dans {0,1,2,3,4,6}, de somme paire au
plus 34. Il exige également que chaque sommet non universel ait un degré
au moins égal au nombre de sommets universels. Il reste **170 triplets
(e,c,h)** distincts. On n'a besoin que de conditions nécessaires : aucun
prolongement de ces profils en un graphe global n'est présumé.

Si e_v≥14, tous les degrés de Ξ_v sont au moins deux. En effet, un sommet
de degré zéro interdit les degrés six et laisse une somme au plus 24 ;
un sommet de degré un autorise au plus un degré six et donne une somme
au plus 1+6+5·4=27. Les deux cas ont moins de quatorze arêtes.

On choisit donc

    S={v:e_v≥14},        s=|S|.

Toutes les droites passant par un sommet de S ont multiplicité au moins
deux. Cette propriété se transmet le long de chaque droite.

## 2. Propagation aux voisins et identités exactes

Pour tout sommet v, notons d(v)=|N(v)∩S|. Si v est extérieur à S, tout
voisin de S doit appartenir à une des h_v droites de multiplicité au moins
deux passant par v. Chacune contient deux voisins de v, donc

    0≤d(v)≤min(s,2h_v),               v∉S.              (3)

Pour v∈S, on conserve 0≤d(v)≤min(14,s−1).

La matrice d'adjacence vérifie A²=12I−A+2J. En l'appliquant à 1_S :

    Σ_v d(v)=14s,
    Σ_v d(v)² + Σ_(v∈S)d(v)=12s+2s².                  (4)

La seconde égalité est essentielle : beaucoup de sommets de petit profil
ne peuvent absorber les voisins de S sans violer ce second moment.

La plus grande valeur propre non constante de A est trois. Pour
x=1_S−(s/99)1, l'inégalité xᵀAx≤3||x||² donne

    Σ_(v∈S)d(v)≤3s+s²/9,
    e(S,V\S)≥11s(99−s)/99.                            (5)

Il ne reste qu'un nombre fini de tailles s à examiner. Pour v∉S,
2e_v=Σg(ℓ)≥2h_v, donc e_v≥h_v≥d(v)/2. Par (5),

    9ρ=Σe_v ≥14s + 11s(99−s)/198.                     (6)

Comme ρ≤126, le membre de gauche vaut au plus 1134. Le membre de droite
est strictement supérieur à 1134 pour tous les entiers 74≤s≤99. Ainsi

    0≤s≤73.

## 3. Le modèle fini, pour chaque valeur entière de s

Une variable non négative n_(i,e,c,d) compte les sommets de profil (e,c,h)
ayant d voisins dans S ; i indique l'appartenance à S et est déterminé
par e≥14. Les profils ayant les mêmes e,c et autorisant la même valeur d
peuvent être représentés plusieurs fois sans conséquence : cela ne fait
que relâcher le modèle. Les bornes (3) sont imposées lors de la génération.

On impose les cinq égalités suivantes :

    Σ_(i=0)n =99−s,              Σ_(i=1)n =s,
    Σe n=9ρ,                    Σd n=14s,
    Σ(d²+i d)n=12s+2s².

On ajoute (5) et les contraintes de recensement

    0≤P≤852,     0≤ρ≤126,     P≥6ρ,     P+5ρ≤1386.      (7)

La dernière coupure est nouvelle sous cette forme. Elle est certifiée
par une combinaison rationnelle non négative des comptes à neuf sommets.
Les anciens certificats P≤11088/13, donc P≤852 par intégralité, et ρ≤126
sont également revérifiés par le programme.

D'après (1), il suffit de majorer l'objectif

    P−6ρ+(1/3)Σc n.                                    (8)

Les 74 modèles ont chacun un certificat rationnel. Le plus grand plafond
certifié vaut

    138943/99 =1403+46/99,

et correspond à la relaxation pour s=56. L'intégralité de τ donne
**τ≤1403**. Ce « cas maximal » concerne le modèle relâché, pas une
configuration du graphe dont on affirmerait l'existence.

### Forme couplée conservant P et ρ

Une seconde série de 74 certificats maximise l'objectif

    (1/3)Σc n−11ρ.

Le plafond maximal est **1729/99=17+46/99**, encore pour s=56. Comme
τ_g et ρ sont entiers, on obtient

    τ_g≤11ρ+17,        τ≤P+5ρ+17.                       (8b)

Avec P+5ρ≤1386, on retrouve τ≤1403. La relation (8b) est toutefois
plus forte quand P+5ρ<1386. Par exemple, le point relâché approximatif
P=691, ρ=115,2, τ=1403 communiqué par LAB respecte le plafond constant
mais viole (8b), dont le membre de droite vaut alors 1284. Les futurs
programmes globaux peuvent donc utiliser cette coupure supplémentaire.

## 4. Ce que vérifient les certificats

Les lignes sont écrites a_i0+Σ_j a_ij x_j≥0. Le programme minimise
l'opposé de (8). Pour des poids rationnels w_i≥0, il calcule exactement

    r_j=f_j−Σ_i w_i a_ij,
    f(x)≥−Σ_i w_i a_i0+Σ_(r_j<0) r_j U_j,              (9)

où les bornes finies sont U_j=99 pour les comptes de sommets, 852 pour P
et 126 pour ρ. Les poids proposés numériquement sont rationalisés ; (9)
est ensuite vérifiée sans solveur. Les résidus sont traités dans leur
intégralité, sans tolérance de signe.

À titre d'exemple, le certificat du cas s=56 utilise seulement les cinq
lignes suivantes, avec les conventions de signe du programme :

| Ligne | Poids |
|---|---:|
| inside_count− | 881/396 |
| grid_incidence− | 283/198 |
| neighbour_first_moment+ | 155/198 |
| neighbour_second_moment− | 31/792 |
| P+5ρ≤1386 | 1 |

La correction par la borne de ρ est incluse dans (9). Les autres valeurs
de s ont leurs propres poids archivés ; le seul exemple s=56 n'est pas
employé pour prétendre couvrir les 73 autres cas.

## 5. Conséquence sur la coque de norme six

On ajoute τ≤1403 au système complet à neuf sommets et aux inégalités de
classes de différences de triangles lointains de la note 186. Le nouveau
certificat exact, avec point rationnel atteignant la relaxation, donne

    b3≥137692/3=45897+1/3.

Puisque b3 est pair, **b3≥45898**. Cette minoration porte bien sur des
vecteurs distincts : elle utilise les familles dont les collisions sont
déjà intégralement traitées dans les notes 179, 181 et 186.

Avec a7≤842, b1≤44, les contraintes de norme quatre de la note 192 et la
positivité thêta jusqu'à q^84, les deux plafonds certifiés sont

    b4 ≤2172309411/136 ≈15972863,316,
    b4+(651/34)b3 ≤2291827803/136 ≈16851675,022.

Le premier baisse d'environ 2527,41 par rapport à la note 194 ; le second
reste inchangé. Il n'y a pas d'exclusion supplémentaire de rang.

## 6. Limites corrigées et reproduction

Une minoration du **nombre total** de collisions déduite d'un plafond sur
b4 ne peut pas être combinée avec une majoration du seul canal de masse
six pour obtenir un intervalle sur ce canal. En particulier, ces données
ne forcent pas à elles seules ρ ou τ à être proches de leurs plafonds, ni
un pourcentage de réalisation d'un profil local extrémal. Les nouveaux
résultats sont indépendants de cette interprétation, retirée par LAB.

Fichiers de preuve :

- `data/codex_prism_plus_five_grids_cap.json` ;
- `data/codex_grid_neighbour_moment_bounds.json.gz` ;
- `data/codex_grid_neighbour_moment_coupled.json.gz` ;
- `data/codex_neighbour_moment_b3_bound.json` ;
- `data/codex_neighbour_moment_theta_effect.json`.

Reproduction sans optimisation :

    python code/codex/grid_neighbour_moment_bounds.py --verify-only
    python code/codex/grid_neighbour_moment_bounds.py --coupled --verify-only
    python code/codex/grid_neighbour_shell_effect.py --verify-only

Les trois commandes passent. Les deux premières vérifient les profils nécessaires,
la coupure P+5ρ et ses dépendances, les tailles exclues par expansion et
les deux séries de 74 certificats de moments. La dernière vérifie les identités duales et
les points rationnels pour b3 et les deux plafonds thêta.
