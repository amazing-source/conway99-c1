# 186 — Triangles lointains : 45528 vecteurs de norme six

8 octobre 2026. Proposition de LAP relayée par LAB au message 227 du pont,
audit et renforcement par Codex.

Le réseau M possède au moins **45528 vecteurs de norme six**, contre 43848
dans la note 182. La nouvelle famille est celle des différences de triangles
disjoints et anticomplets. Le gain uniforme de **1680 vecteurs** utilise les
multiplicités des collisions, au-delà de la simple soustraction du nombre de paires.
Si P=0, la nouvelle borne est **b3≥73920**.

## 1. Représentants et toutes leurs collisions

Pour deux triangles disjoints et anticomplets T,Y, posons ψ=1_T−1_Y. Alors
Σψ=0 et Q(ψ)=18−2(3+3)=6. Les deux orientations sont comptées. Le recensement
exact de la note 179 donne

    R = 7392−2P

représentants. Le programme reconstruit ce nombre à partir des 62 comptes induits
à six sommets, en énumérant les partitions signées admissibles de chaque type.

Deux représentants distincts ont une différence de masse positive au plus six.
Le lemme +3 de la note 168 impose que cette différence soit binaire et ait pour
supports deux prismes disjoints et anticomplets. En particulier les quatre
triangles sont disjoints. Chaque prisme a exactement deux triangles : pour une
paire non ordonnée de prismes, les choix des deux triangles positifs et négatifs
donnent huit représentants, réunis en quatre paires de collisions.
La différence des représentants détermine de façon unique la paire de prismes.
Ainsi le nombre total de paires non ordonnées de représentants qui coïncident est

    C = 4τ.

Le quotient fini par la différence des indicatrices des prismes contrôle
explicitement les huit représentants et les quatre paires. Globalement, des
classes de taille supérieure à deux restent possibles ; on ne suppose pas que
chaque paire donne une perte supplémentaire distincte.

Cette famille est disjointe de toutes celles déjà comptées à la norme six.
Les anciennes familles de sommes ±3 et ±6 sont séparées de la somme zéro
par la congruence modulo neuf. À somme zéro, la famille antérieure de norme six
est celle des différences de deux points non adjacents. Une collision avec
cette famille aurait une masse positive au plus quatre, donc serait impossible.

## 2. Compter les classes plutôt que soustraire toutes les paires

Soit D le nombre d'images distinctes de la nouvelle famille, et m_i les tailles
de ses classes. On a Σm_i=R et Σ binom(m_i,2)=C. Pour tout entier k≥1 et tout
entier m≥1,

    1 − [2m/(k+1) − 2 binom(m,2)/(k(k+1))]
        = (m−k)(m−k−1)/(k(k+1)) ≥ 0.

En sommant cette inégalité sur les classes,

    D ≥ 2R/(k+1) − 8τ/(k(k+1)).                         (1)

Le choix k=1 retrouve R−4τ. Le choix k=3 donne

    D ≥ 3696−P−(2/3)τ.

En l'ajoutant à la borne b3≥66528−18P−72ρ de la note 179,

    b3 ≥ 70224−19P−72ρ−(2/3)τ.

La borne τ≤2P+3ρ de la note 185 implique alors

    b3 ≥ 70224−(61/3)P−74ρ.                            (2)

Le recensement d'ordre neuf certifie exactement que le membre droit de (2)
est au moins **45528**. Le certificat est une combinaison à coefficients
rationnels positifs de quatorze comptes de types à neuf sommets. Dans le système
complet, les seuls autres multiplicateurs non nuls sont 2/3 pour
`tau<=2P+3rho` et 1 pour la borne des classes k=3.

Le programme conserve les anciennes bornes et toutes les lignes (1) pour
1≤k≤8. Les poids rationnels sont vérifiés contre chaque coordonnée du système,
sans utiliser la valeur numérique du simplexe comme preuve. Si P=0, alors τ=ρ=0,
et k=1 donne directement b3≥66528+7392=73920.

## 3. Effet sur la relaxation du rang 37

En remplaçant la borne uniforme 43848 par 45528 et en ajoutant les conséquences
de (1), le plafond rationnel sur b4 à q^84 passe de

    214492633/13 ≈ 16499433,31

à

    214100073/13 ≈ 16469236,38.

La diminution est d'environ **30197**. Un point rationnel de la relaxation
atteint encore ce plafond ; le rang 37 n'est donc pas exclu par ces contraintes.
Le nouveau comptage est néanmoins une amélioration démontrée, directement
utilisable dans les contraintes couplées avec les prochaines familles.

Reproduction :

    python code/codex/far_triangle_shell_bound.py
    python code/codex/rank37_dual_frontier.py --order9 --far-triangles

Certificats et contrôles : `data/codex_far_triangle_shell_bound.json` et
`data/codex_rank37_dual_frontier_order9_far_triangles.json`.
Le second fichier contient aussi les cibles conditionnelles b3≥150000,
300000,600000,900000 ; ces seuils ne sont pas de nouvelles minorations prouvées.

Les tests indépendants du recensement à neuf sommets transmis par LAB sont
consignés, avec leurs limites, dans la mise à jour de la note 184.
