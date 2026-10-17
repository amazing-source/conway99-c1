# 200 — Représentants sans prisme et égalités de longueur

8 octobre 2026. Réponses aux messages 310–316 de LAB/LAP. Les propositions
de familles viennent de LAB/LAP ; les comptages locaux et certificats
ci-dessous ont été reconstruits par Codex.

## 1. Deux collections à distinguer

Un représentant est un vecteur entier ψ=1_W−1_Y, où W et Y sont disjoints,
de support au plus neuf, de somme divisible par trois et de norme projetée
Q(ψ)=8. Il est **sans prisme** si ni W ni Y ne contient un prisme induit.
On compte les deux signes.

La collection sans prisme n'est pas la collection de la note 198. Celle-ci
conservait toutes les formes `(9,0)` et `(7,1)`, mais imposait e(W)≤8 à
`(6,3)`. Le numérateur complet de LAB, qui comprenait aussi les `(6,3)`
dont le six-ensemble est un prisme, ne pouvait donc pas être associé
directement au plafond 27828 de cette note.

Pour la nouvelle collection sans prisme, les nombres C_pf de collisions
**binaires de masse six, à somme égale**, par paire de prismes jumeaux,
satisfont les bornes certifiées suivantes :

| Type de paire | Plancher | Plafond |
|---|---:|---:|
| Deux grilles ayant une droite commune | 6992 | 18244 |
| Paire hors grille | 7034 | 19178 |

Ce sont des bornes nécessaires ; aucune réalisation des extrémités par
un graphe n'est affirmée. Elles ne comptent ni les autres masses, ni les
changements de somme.

Pour les représentants **les plus courts dans leur classe**, seules les
collisions à égalité de longueur peuvent subsister. En imposant en plus
les deux contraintes de grilles disponibles, on obtient les plafonds :

| Type de paire | Plafond des collisions à égalité de longueur |
|---|---:|
| Paire de grilles | 12674 |
| Paire hors grille | 14426 |

La seconde ligne n'impose que l'absence de prisme et l'égalité des tailles,
puisqu'il n'y a pas les deux grilles de la première ligne. Ces ensembles
de conditions sont des relaxations de la minimalité globale : leurs
plafonds s'appliquent aux collisions du véritable ensemble de représentants
les plus courts. **Aucun plancher pour ce dernier ensemble n'est déduit.**

## 2. Reconstruction exacte de la collection sans prisme

Pour chaque patron local de deux points extérieurs, et pour les canaux
ne nécessitant que zéro ou un point extérieur, le programme construit
explicitement les deux représentants en collision. Il vérifie leur norme
par la matrice complète et recherche un prisme dans chacun des quatre
supports positifs ou négatifs.

Une énumération exhaustive des 32768 graphes étiquetés sur six sommets
vérifie le fait suivant : parmi les graphes satisfaisant les restrictions
locales λ≤1, μ≤2, les seuls ayant au moins neuf arêtes sont les 60
étiquetages du prisme. Ainsi, pour `(6,3)`, être sans prisme équivaut
exactement à e(W)≤8. Le canal interne de trois points extérieurs de la
note 195 est donc réutilisable ; ses 63342 coûts ont été recomptés.

Les changements par rapport à la collection de la note 198 sont :

- `(9,0)` interne : zéro, car une collision de masse six y impose un
  prisme dans le support de chacun des partenaires ;
- `(7,1)` contre `(6,0)` : zéro, pour la même raison ;
- `(7,1)` interne : recherche explicite des prismes alternatifs, même
  lorsque l'échange est bilatéral sur la paire fixée ;
- les autres canaux de cette collection restent inchangés.

Les contributions constantes à zéro ou un point extérieur totalisent
2922 : 1488 pour `(6,3)` contre `(4,1)`, 792 pour `(4,4)` contre `(3,3)`,
162 pour `(4,4)` contre `(2,2)`, 216 pour `(5,2)` interne, 216 pour
`(5,2)` contre `(4,1)`, et 48 pour `(3,3)` interne.

Pour une paire de grilles, `(7,1)` interne sans prisme vaut également
zéro. Les seuls candidats bilatéraux admissibles qui contribuent avant
le test final utilisent deux apices adjacents et contiennent un autre
prisme. Le programme retrouve zéro sur tous les patrons affinés de la
note 198. Cela montre pourquoi « bilatéral » ne suffit pas à garantir
« sans prisme ».

Les objectifs ainsi reconstruits sont optimisés dans le modèle de degrés
de la note 198 pour une paire de grilles et dans le modèle hors grille
de la note 195. Les certificats utilisent des poids rationnels non
négatifs et les bornes finies des variables. Les arrondis utilisent la
parité du nombre de paires signées.

## 3. Filtrage des égalités de longueur

Fixons δ=1_X1−1_X2 et ψ′=ψ−δ. Posons

    a=|W∩X1|,  b=|Y∩X2|.

Pour que les deux représentants restent binaires, ψ est positif ou nul
sur X1 et négatif ou nul sur X2. La variation de longueur euclidienne est

    ||ψ′||²−||ψ||² = 12−2(a+b).

Une égalité de longueur impose donc a+b=6. Comme la somme des coordonnées
est conservée, les deux formes `(p,q)` sont alors identiques. Tous les
canaux croisés entre formes différentes disparaissent de ce comptage.

Dans le cas des grilles Gi=Xi∪Θ, soit t=Σ_(v∈Θ)ψ_v. Les sommes sur les
deux grilles sont

    ψ(G1)=a+t,   ψ(G2)=−b+t.

Les sommes du partenaire sont les mêmes dans l'ordre inverse si a+b=6.
Puisque 1_Gi est une relation de la projection et a longueur carrée neuf,
un représentant globalement le plus court doit satisfaire

    |a+t|≤4,   |−b+t|≤4.                              (1)

En effet, une somme de valeur absolue au moins cinq permet d'ajouter ou
de retrancher 1_Gi en diminuant strictement la longueur. L'argument reste
valable si le représentant plus court n'est plus binaire.

Après ces filtres, les seuls canaux de masse six restants côté grilles
sont `(3,3)`, `(4,4)` et `(6,3)` internes. La contribution constante est
48 ; `(5,2)` interne disparaît entièrement, ainsi que `(7,1)`. Le canal
`(6,3)` est recompté en tenant compte du signe de chacun des apices.

Les contraintes liées à d'autres grilles ou d'autres relations ne sont
pas toutes imposées. Les plafonds 12674 et 14426 sont donc des majorations
sûres des pertes du véritable ensemble minimal. Son nombre de
représentants reste à établir : on ne peut pas conserver le numérateur
de toute la collection sans prisme après en avoir supprimé les copies.

## 4. Trois représentants sans prisme de même classe

Considérons trois prismes X1,X2,X3 d'un même faisceau et un point b de B.
Notons vi son unique voisin dans Xi. Choisissons un apex θ dont la couleur
est différente de celles des trois vi. Pour {i,j,k}={1,2,3}, posons

    ψ_i = 1_(Xi\{vi}) + 1_θ − 1_b − 1_vj − 1_vk.       (2)

Le positif a six points et huit arêtes : le prisme privé de vi a six
arêtes, et θ voit les deux points de son barreau. Le négatif est le chemin
vj−b−vk. Les deux supports sont anticomplets. Donc

    Q(ψ_i)=3·9+1−2(8+2)=8.

Les deux supports sont sans prisme, mais

    ψ_i−ψ_j=1_Xi−1_Xj.

Chaque représentant a ainsi deux partenaires dans ce triplet. Dans un
faisceau de six grilles, b a deux voisins de chaque couleur parmi ses
six voisins des prismes. Pour chaque θ, quatre prismes évitent sa couleur,
et chacun des quatre choix de trois prismes donne une construction (2).

Pour un faisceau fixé, cela donne 60·3·4=720 triplets de représentants
positifs, ou 1440 en comptant aussi leurs opposés. Ils sont disjoints
comme ensembles de représentants pour ce faisceau. Ce décompte n'affirme
pas que toutes leurs images sont différentes, ni que les triplets
provenant de faisceaux différents sont disjoints.

Les quatre choix pour b et θ fixés ne sont pas une classe à quatre
représentants établie par cette construction. Leurs représentants courts
ci-dessous diffèrent par e_v−e_w, de norme projetée six, donc leurs images
sont distinctes.

Tous les ψ_i sont en réalité des copies plus longues d'un même représentant :

    ψ_i−1_Gi = −1_b−1_v1−1_v2−1_v3−1_(Θ\{θ}).         (3)

Ce dernier a six coordonnées non nulles, sept arêtes dans son support
et norme projetée huit. Les ψ_i ont somme six sur Gi et sont donc
éliminés par (1). La construction réfute l'idée d'un partenaire unique
pour toute la collection sans prisme sous l'hypothèse d'un faisceau
de six ; elle n'est pas un obstacle établi à une telle propriété après
tous les filtres de minimalité.

Un modèle induit de 22 sommets, avec couleurs des vi égales à `(0,0,1)`
et θ de couleur 2, est archivé. Le programme vérifie les contraintes
locales λ,μ, les supports, les normes, les différences propres et la
relation (3). Ce modèle n'est pas une complétion à 99 sommets.

## 5. Canaux à conserver séparément

Les relations d'une grille entière changent la somme de neuf. Elles ne
sont incluses ni dans les présentes bornes, ni dans C6 des notes 195–198.
Le retrait de leurs copies doit s'accompagner d'un comptage du numérateur
restant. Une borne supérieure par grille donne, par soustraction, une
borne inférieure après ce seul retrait ; les recouvrements et les autres
conditions de minimalité doivent encore être traités.

En revanche, pour `(4,4)`, les collisions de masse huit associées à deux
grilles se rencontrant en un point sont couvertes par la note 183, §4.
Chaque grille privée de ce point est le type C14 de code 127242964.
La majoration est 64 par paire de tels supports, et
`(608/3)C14+160τ` pour toute cette composante. Elle figure dans L44 de
la note 185 ; elle ne figure pas dans les totaux de masse six ci-dessus.

Les seuils numériques proposés par LAB ne sont pas certifiés ici. Une
borne supérieure au-dessus d'un seuil exploratoire signifie que cette
borne ne suffit pas, pas qu'une preuve avec des contraintes plus fortes
est impossible. Aucun rang supplémentaire n'est exclu dans cette note.

## 6. Reproduction

Patrons et comptages : `data/codex_prism_free_mass6_patterns.json.gz`.
Certificats : `data/codex_prism_free_mass6_KIND.json.gz` et
`data/codex_prism_free_mass6_KIND_ties.json.gz`, pour KIND=`grid`,`nongrid`.
Le modèle local est dans `data/codex_prism_free_twin_triangle.json`.

    python code/codex/prism_free_mass6_bounds.py --generate --verify-only
    python code/codex/prism_free_mass6_bounds.py --kind KIND --verify-only
    python code/codex/prism_free_mass6_bounds.py --kind KIND --ties --verify-only
    python code/codex/prism_free_twin_triangle.py --verify-only

Tous les patrons ont été régénérés et comparés, les quatre archives de
certificats ont été relues en arithmétique rationnelle sans solveur,
et le modèle local a été vérifié indépendamment des optimisations.
