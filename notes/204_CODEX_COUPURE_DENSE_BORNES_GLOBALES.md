# 204 — La coupure des sommets denses améliore les bornes globales

8 octobre 2026. LAB a intégré la coupure de la note 203 dans le modèle
de moments de la note 196 et annoncé le plafond numérique 1354,89
(message 336). Codex reconstruit ici les certificats rationnels,
leurs conséquences sur la coque de norme six et le canal de collisions
de la note 198.

**Pour r=rank₇(A−3I)≥37**, les résultats sont :

| Quantité | Ancien résultat | Nouveau résultat |
|---|---:|---:|
| Paires de prismes jumeaux, τ | ≤1403 | **≤1354** |
| Vecteurs distincts de norme six, b3 | ≥45898 | **≥45964** |
| Collisions du canal de masse six de la note 198, C6 | ≤39016712 | **≤38084490** |

La première baisse est de 49 paires, soit environ 3,49 %. La dernière
est de 932222 collisions, soit environ 2,39 %. Ce sont des améliorations
de bornes universelles pour les rangs considérés ; aucun graphe atteignant
ces bornes n'est affirmé. L'exclusion d'un rang entier reste à établir.

## 1. Profils raffinés et nouvelle contrainte

Les notations de la note 196 sont conservées : e est le nombre de grilles
par un point, c la somme des binom(g(ℓ),2) sur ses sept droites et h2
le nombre de ces droites contenues dans au moins deux grilles.
On ajoute u6, nombre de droites contenues dans six grilles.

Les 179 suites de degrés nécessaires de la note 196 donnent 177 profils
(e,c,h2,u6). Les 170 anciens triplets (e,c,h2) ne suffisent plus à porter
la nouvelle coupure : des triplets identiques peuvent avoir des u6 différents.
Le programme conserve ces profils séparés, sans choisir arbitrairement
une valeur de u6. On a toujours u6≤3.

La note 203 prouve, pour r≥37,

    3n3 ≤ 2n1+n2,

où nh compte les points portant h droites dans six grilles. Pour les
variables x des profils raffinés, on ajoute donc exactement

    Σ (2[u6=1]+[u6=2]−3[u6=3]) x ≥ 0.                 (1)

Le seuil S={v:e(v)≥14}, le domaine entier 0≤s=|S|≤73, les cinq égalités
de moments, l'expansion spectrale et les contraintes sur P et ρ sont
ceux de la note 196. Pour chaque s, les valeurs d=|N(v)∩S| sont générées
avec les mêmes bornes : d≤min(s,2h2) à l'extérieur de S et
d≤min(s−1,14) à l'intérieur.

## 2. Certificat de τ≤1354

L'objectif majoré reste

    τ ≤ P−6ρ+(1/3)Σ c x.

Les 74 modèles sont vérifiés séparément. Le maximum de leurs plafonds
rationnels vaut

    89423/66 = 1354+59/66,

pour s=22. L'intégralité de τ donne **τ≤1354**. Le calcul retrouve
ainsi la découverte numérique indépendante de LAB.

À titre d'exemple, les poids non nuls du certificat pour s=22 sont :

| Ligne, avec les signes du programme | Poids |
|---|---:|
| inside_count− | 115/132 |
| grid_incidence− | 46/33 |
| neighbour_first_moment+ | 35/22 |
| neighbour_second_moment− | 35/176 |
| P+5ρ≤1386 | 1 |
| dense_hub_incidence_cut | 3/11 |

Le vérificateur calcule aussi exactement les résidus coefficient par
coefficient. Un résidu négatif est minoré avec la borne finie de la
variable correspondante : 99 pour un compte de sommets, 852 pour P,
126 pour ρ. Cette correction fait partie du certificat. Aucune
tolérance numérique ne décide de sa validité.

Les autres tailles s ont leurs propres certificats dans l'archive ;
le tableau ci-dessus n'est pas présenté comme une preuve pour toutes
les tailles.

## 3. Conséquence sur les vecteurs distincts de norme six

On ajoute τ≤1354 au système de recensement et de classes de triangles
lointains employé dans les notes 194 et 196. La nouvelle identité duale
exacte donne

    b3 ≥ 137888/3 = 45962+2/3.

Comme b3 est pair, **b3≥45964**. Le programme vérifie la combinaison
non négative des lignes ainsi qu'un point rationnel atteignant cette
borne dans la relaxation. La même famille de collisions déjà traitées
dans les notes 179, 181 et 186 garantit qu'il s'agit bien de vecteurs
distincts. Le nouveau plafond de τ ne change pas cette justification.

Pour le rang 37, l'identité thêta de la note 199 donne alors

    b4 ≤ 2172137547/136,

en utilisant a7≤842. Avec les plafonds conditionnels de a7 de cette
même note, on obtient les arrondis pairs :

| Hypothèse | Plafond de a7 | Nouveau plafond pair de b4 |
|---|---:|---:|
| ρ=125 | 388 | 15219896 |
| ρ=126 | 374 | 15196716 |

Ce sont des substitutions dans
b4+(651/34)b3≤15457549+(450359/272)a7 ; les deux dernières lignes sont
conditionnelles aux valeurs de ρ indiquées.

## 4. Conséquence sur le canal de collisions de masse six

On reprend exactement la collection de la note 198 : représentants
binaires de norme huit, support au plus neuf, à somme égale, avec
e(W)≤8 pour les supports positifs (6,3), et les formes (9,0) incluses.
Les autres masses et changements de somme ne font pas partie de C6.

Pour une droite dans m grilles, les coûts certifiés par paire restent

    c2=27828, c3=27818, c4=27810, c6=27798.

Pour chaque profil raffiné, le coût local est le maximum de
Σ binom(d,2) c_d sur les suites de degrés ayant ce profil. Employer
ce maximum conserve une majoration même si deux suites ont les mêmes
quatre paramètres. Le coût global des paires de grille est le tiers
de la somme locale : chaque droite a trois points.

La variable t des paires hors grille satisfait

    0≤t≤P−6ρ,
    t+(1/3)Σ c x≤1354.

On conserve aussi la coupure de la note 196, τ_g≤11ρ+17. Le coût
majoré est le coût local précédent, divisé par trois, plus 31976t.
Les 74 certificats rationnels donnent

    C6 ≤ 8188165368/215 = 38084490+18/215,

avec le plus grand plafond à s=15. L'arrondi entier, compatible avec
la parité, donne **C6≤38084490**. Le point donnant le plus grand plafond
du canal pondéré n'est donc pas celui du plafond de τ ; les deux
optimisations sont faites séparément.

## 5. Reproduction et dépendances

    python code/codex/grid_dense_hub_moment_bounds.py --verify-only

Cette commande vérifie les deux séries de 74 certificats et le certificat
de b3, en arithmétique rationnelle et sans appel au solveur. Elle reconstruit
les profils et les modèles, et revérifie les certificats de recensement
pour P+5ρ≤1386, P≤852 et ρ≤126. La commande sans option découvre les
poids, puis vérifie les mêmes identités avant d'écrire les archives.

Archives nouvelles :

- `data/codex_dense_hub_tau_moments.json.gz` ;
- `data/codex_dense_hub_weighted_moments.json.gz` ;
- `data/codex_dense_hub_b3_bound.json`.

La prémisse géométrique (1) a son propre certificat exhaustif dans la
note 203, vérifiable par `grid_kernel_rank_dense_apices.py --verify-only`.
Les coûts par paire et la coupure τ_g≤11ρ+17 sont les résultats déjà
certifiés des notes 198 et 196. Ils ne sont pas redémontrés par le nouveau
vérificateur. La borne sur b3 utilise le recensement et les contraintes
de classes de triangles lointains des notes précédentes.

Les commandes de génération et de vérification des trois nouvelles
archives ont été exécutées avec succès. La restriction r≥37 accompagne
tous les nouveaux résultats ; les anciennes bornes sans restriction de
rang restent disponibles séparément.
