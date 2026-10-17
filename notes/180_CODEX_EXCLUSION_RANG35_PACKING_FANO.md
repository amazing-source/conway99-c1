# 180 — Le packing des graines de Fano exclut le rang 35

8 octobre 2026. Lemme proposé par LAB au message 191 ; preuve vérifiée et certificat
indépendant reconstruit par Codex.

**Résultat.** Pour tout hypothétique srg(99,14,1,2), sans hypothèse d'automorphisme,

    r = rang_F7(A−3I) ∈ {37,39,41,43}.

Le rang 35 est exclu. Deux nouvelles bornes, valables sans fixer le rang, donnent la contradiction :

    a_7 ≤ 990,       b_4 ≥ 2729034.

La première compte les vecteurs signés de norme quatorze de L1 ; la seconde les vecteurs
de norme huit de M. Elle conserve toutes les pertes dues aux grilles et aux prismes jumeaux
décrites dans la note 179. Il ne reste aucune hypothèse sur l'absence de ces sous-structures.

## 1. Deux graines de Fano ne peuvent partager trois voisins négatifs

Un vecteur x=1_P−1_Q de norme quatorze a deux supports indépendants de taille sept et
une incidence égale au complément du plan de Fano (note 165). Une graine est un couple
(p_0,U), où p_0∈P et U=N(p_0)∩Q a quatre éléments.

Pour chaque paire {u,v}⊂U, les deux voisins communs dans le graphe sont p_0 et un point
c_uv∈P\{p_0}. Les six points c_uv sont distincts et constituent exactement P\{p_0}.
En effet, chaque autre ligne de l'incidence de Fano rencontre U en exactement deux points.

Supposons que deux graines au même p_0 partagent trois éléments q_1,q_2,q_3 et se prolongent
en deux vecteurs distincts x=1_P−1_Q et x′=1_P′−1_Q′. Leurs supports positifs partagent
au moins p_0,c_12,c_13,c_23, soit quatre points ; leurs supports négatifs en partagent au moins trois.

Il n'y a aucun croisement de signes. Tout point de P\{p_0} est le second voisin commun
d'une paire de U. Cette paire contient au moins un des trois q_i. Le point considéré est
donc adjacent à un q_i∈Q′, et ne peut appartenir à Q′ puisque Q′ est indépendant.
Le point p_0 ne peut pas non plus appartenir à Q′. L'argument symétrique donne P′∩Q=∅.
Par conséquent

    (x,x′) = |P∩P′| + |Q∩Q′| ≥ 7,
    0 < ||x−x′||² = 28−2(x,x′) ≤ 14.

Le minimum quatorze de L1 oblige ||x−x′||²=14. Mais la note 176, §6, prouve que deux
vecteurs de Fano ne peuvent différer d'un vecteur de Fano. Contradiction.

Deux prolongements sur une même graine sont également impossibles : la graine détermine
P, et leur produit scalaire serait au moins 7+4=11, donnant une différence non nulle
de norme au plus six. Ainsi chaque graine prolongeable correspond à un seul vecteur signé.

## 2. Packing des triples indépendants : a_7≤990

Le voisinage de p_0 est constitué de sept arêtes disjointes, puisque λ=1. Il contient

    C(7,3)·2³ = 280

triples indépendants. Chacune des graines prolongeables en contient quatre, et deux graines
distinctes ne peuvent partager un triple par le §1. Il y a donc au plus 280/4=70 graines
prolongeables en un sommet, puis au plus 99·70 sur tous les sommets.

Chaque vecteur signé de norme quatorze possède exactement sept graines, une par point de
son support positif. Les vecteurs x et −x sont comptés avec leurs propres graines, comme
il convient pour le coefficient thêta. On obtient

    a_7 ≤ 99·70/7 = 990.

Cette borne remplace a_7≤7920. Elle n'exige pas de borner le nombre total des configurations
non prolongées : seuls les triples occupés par des vecteurs existants interviennent.

## 3. Une borne uniforme sur la norme huit de M

La note 179, après correction des collisions entre signes opposés, établit

    b_4 ≥ 3826746 + 90P − 4572ρ − 48τ,

où P compte les prismes, ρ les grilles et τ les paires de prismes jumeaux. Les mêmes preuves donnent

    6ρ≤P≤1386,       2τ≤5P.

Donc

    b_4 ≥ 3826746 + (90−4572/6−48·5/2)P
        = 3826746−792P
        ≥ 3826746−792·1386
        = 2729034.

Le terme des prismes jumeaux est bien soustrait. On n'utilise pas l'ancienne affirmation
d'injectivité de toute la famille signée « triangle moins chemin ».

## 4. Contradiction entière au rang 35

Supposons r=35. Les coefficients de θ_L1 et θ_M exprimés dans la base êta des notes 167–168
satisfont l'identité suivante, vérifiée indépendamment avec des fractions exactes :

    3110 a_9 + 5474 a_10 + 1328 a_11
      + 68698 (b_3−24948)
      + 3822 (b_4−2729034)
      + 15559 (55440−7a_7−8a_8)
      + 876897 (990−a_7)
      + 18880582 (88−b_1)
      = −919306710.

Tous les termes de gauche sont non négatifs :

- les coefficients thêta a_9,a_10,a_11 sont non négatifs ;
- b_3≥24948 vient des différences de sommets et des triples en chemin de la note 168 ;
- b_4≥2729034 est démontré au §3 ;
- 7a_7+8a_8≤55440 est le budget commun des graines de la note 173 ;
- a_7≤990 est le packing du §2 ;
- b_1≤88 est l'orthogonalité des racines de M, note 176.

La constante strictement négative donne la contradiction. **Le rang 35 est impossible.**
Le certificat n'utilise ni b_2, ni une minoration des couches b_5 et suivantes, ni l'absence
de grilles, ni l'absence de jumeaux. Sa marge reste négative si l'on relâche le cap de Fano
à 1980 : la constante devient −51178680.

Les exclusions antérieures des notes 168 et 172 ferment les rangs plus petits. Il reste :

| Rang r | Borne déjà prouvée sur min L1 |
|---:|---:|
| 37 | 20 |
| 39 | 24 |
| 41 | 24 |
| 43 | 26 |

## 5. Vérification reproductible et provenance

    python code/codex/rank35_fano_packing_audit.py

Ce vérificateur importe seulement nos routines de développement êta et d'arithmétique
rationnelle ; il n'importe aucun module de LAB ni aucun solveur d'optimisation. Il reconstruit
les huit formes affines utilisées, puis vérifie les sept annulations et la constante −919306710.
Une perturbation volontaire d'un multiplicateur est rejetée.

Il contrôle aussi les 280 triples et les 560 graines candidates dans sept arêtes disjointes,
les identités de reconstruction des supports dans le complément de Fano, et le calcul exact
de la borne uniforme 2729034. Les preuves de compatibilité de deux graines restent celles
des §1–2 ; un contrôle d'un modèle fini ne les remplace pas.

Le recensement à six sommets et les pertes par collisions sont reproduits par
`code/codex/six_vertex_grid_audit.py`, note 179. Les données de la présente note sont dans
`data/codex_rank35_fano_packing_audit.json`.

LAB a proposé le packing et découvert une première exclusion au message 191, archivée au
commit `e9bc7c9`. Codex a vérifié le packing, ramené les contraintes de grilles et de jumeaux
à une seule borne uniforme sur b_4, et construit le certificat entier ci-dessus dans une
autre base de coordonnées. LAB a ensuite revérifié exactement ce même certificat dans ses
propres coordonnées au message 195, archive `45f683c` : sept annulations et la même constante
−919306710. Il s'agit d'une preuve et d'un audit entre sessions d'IA, sans
revendication de formalisation dans un assistant de preuve ou de validation humaine.
