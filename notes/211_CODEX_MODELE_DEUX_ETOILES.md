# 211 — Modèle entier et modulo sept de deux étoiles génériques

8 octobre 2026. Mise en œuvre de la note 209 dans
`code/codex/joint_generic_stars.py`. Le modèle est une condition
nécessaire locale à P=0, pour une droite générique au rang global 37.
Il n'est pas une construction complète du SRG.

## 1. Variables et contraintes

L'entrée est le graphe cubique G(T), avec ses trois couches indexées
0…11, 12…23, 24…35, et une arête uv entre couches. Le script contrôle
la structure des couches, l'absence de triangles et la nullité un de
3I−G modulo sept. Il calcule K et H⁺ exactement.

Les candidats d'une étoile sont les supports de six points, deux
non partenaires par couche, contenant son centre. Ils satisfont

    Gn ≤ 2−n,       K_pq>0 sur les paires du support,
    nᵀH⁺n=6 modulo 7.

Chaque ombre est indexée par son second point dans la couche du
centre, ce qui impose les dix paires une fois chacune.

Le script branche sur l'ombre w commune aux deux étoiles. Ses
supports sont obtenus indépendamment depuis les deux pools et leur
égalité est contrôlée. Pour chaque w fixé, il reste neuf variables
de choix d'ombre de chaque côté. Le domaine de chacune exclut l'autre
centre et impose g(n,w)=3 et |n∩w|≤2. Les 19 ombres sont ainsi
distinctes par construction.

Le modèle CP-SAT utilise uniquement des variables entières, des
tables finies et des contraintes linéaires booléennes :

- pour toute paire d'ombres, g(n_i,n_j)∈{2,3}, l'adjacence étant
  a_ij=3−g(n_i,n_j), et l'intersection au plus 2−a_ij ;
- dans chaque étoile, degré interne égal à 1−(Gn_i)_centre ;
- somme exacte des dix ombres égale à K e_centre, dans Z³⁶ ;
- couplage transversal de cardinal 7+c₄(uv), avec degré au plus un ;
- absence des quatre-cycles qui formeraient un prisme sur uv ;
- incidence partielle M★M★ᵀ≤K sur les paires de points proches ;
- pour deux ombres, intersection des supports plus nombre de voisins
  communs lointains déjà choisis au plus 2−a_ij ;
- pour un point proche x et une ombre y, nombre de voisins communs
  déjà présents, dans G et parmi les 19 ombres, au plus 2−n_y(x).

L'apex commun est isolé dans cette union. Les produits booléens
nécessaires aux deux dernières familles d'inégalités sont linéarisés
exactement. Ces familles contrôlent les voisins communs connus,
sans exiger que le système partiel ait déjà tous les voisins communs
du futur graphe.

Tout témoin éventuellement trouvé est revérifié par reconstruction
des matrices entières et de leur Gram, hors du modèle CP-SAT.

## 2. Premier contrôle

Sur la boule cyclique (2,4,1), avec u=0 et v=12, le générateur trouve
473 supports possibles pour l'apex commun. Les trois premiers
supports, et les domaines des 18 ombres restantes, sont enregistrés
dans `data/codex_joint_generic_stars_pilot.json`.

Les trois modèles sont infaisables au prétraitement CP-SAT, avec zéro
branche de recherche. Le contrôle prend quelques secondes au total.
Les versions de NumPy et OR-Tools sont consignées dans le résultat.

**Portée exacte : 3 branches sur 473.** Cette expérience ne clôt pas
les autres branches. La boule de contrôle était de toute façon déjà
exclue par l'étoile unique de la note 207. Ce contrôle valide une
première exécution du nouveau modèle couplé ; ce n'est ni une nouvelle
exclusion mathématique, ni une preuve par certificat indépendant du
solveur de son infaisabilité. La liste des contraintes est exposée
pour permettre une relecture de leur nécessité.

## 3. Utilisation bornée

À la racine du dépôt :

    python code/codex/joint_generic_stars.py --max-apex 3 --seconds 30 --out data/codex_joint_generic_stars_pilot.json

Par défaut une seule branche est testée. `--apex-start N` change la
première branche ; `--max-apex 0` demande toutes les branches, avec
une limite de temps à conserver. Une entrée différente utilise
`--ball fichier.json`, dont la clé `adjacency` contient la matrice
36×36, et éventuellement `--u` et `--v`.

Le calcul emploie un seul worker et une graine fixe. Un arrêt par
temps, une branche `UNKNOWN`, ou un sous-ensemble des apex produit
explicitement `PARTIAL_RUN_NO_GLOBAL_EXCLUSION`. Seule une énumération
exhaustive d'apex tous déclarés infaisables peut produire
`ALL_COMMON_APEX_BRANCHES_EXCLUDED`. Un témoin local n'est pas déclaré
être un SRG.
