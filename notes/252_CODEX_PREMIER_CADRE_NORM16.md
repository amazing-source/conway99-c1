# 252 — Premier cadre explicite de norme 16 pour la recherche de LAB

10 octobre 2026. Suite constructive de la note251. Aucun rang exclu.

## Résultat livré

Le fichier `data/codex_norm16_typed_frame_0_0_2.json` contient un cadre
de37 sommets, sa matrice d'adjacence, les types des62 autres sommets et
leurs colonnes binaires satisfaisant les filtres locaux décrits ci-dessous.
Il appartient au premier cœur (défaut8), à l'orbite d'attaches D numéro0,
à la branche où D est indépendant, et à la forêt

    Z = P3 + P4 + 4 K1.

Le cadre comprend P,Q,Z et Y=N(P0) sans Q. Ses indices sont :

- P :0..7 ; Q :8..15 ; Z :16..26 ;
- les deux voisins D de P0 :27,28 (D0,D1 de l'attache) ;
- les huit voisins simples de P0 :29..36.

Le JSON `codex_norm16_frame_0_0_2.json` conserve aussi le témoin auxiliaire
de43 sommets utilisé pour le construire (tous les D ajoutés). Ce témoin
satisfait les contraintes combinatoires locales du pilote, mais sa matrice
de Seidel a rang40 modulo sept. **Les six D supplémentaires de ce témoin
ne sont donc pas fixés dans le test de rang37.** Seul le cadre sur37 points
est donné comme base du fichier `typed_frame`; les attaches D–Z des six D
restants y sont à choisir parmi leurs domaines.

Cela ne fournit ni un graphe fortement régulier, ni un témoin de rang37,
ni une famille exhaustive de cadres. L'objet livré permet à LAB de tester
son moteur sur une première entrée explicite de norme16.

## Deux relations automatiques, rang au plus35

Pour S=J-I-2A, l'identité A²+A=12I+2J implique exactement

    S(A+4I)=7(2J-A-4I).

Ainsi g=4e_p+1_{N(p)} est une relation modulo sept dès que le voisinage
complet de p figure dans le cadre. Le vecteur f=1_P-1_Q est une autre
relation. Elles sont indépendantes puisque g est non nul sur Y, où f
s'annule. Tout cadre de37 points de cette construction a donc rang≤35.
Le premier cadre livré a rang35, avec ces deux relations pour noyau.

Dans l'espace global non dégénéré de dimension36 de LAB, ses vecteurs
engendrent alors un sous-espace non dégénéré de dimension35 : un
engendrement de dimension36 donnerait une matrice de Gram de rang36.
La complétion utilise donc une droite orthogonale résiduelle. Il faut
traiter cette droite, ou ajouter un sommet, avant d'utiliser un moteur
qui exige une base non dégénérée de dimension36.

Cinq premiers témoins locaux (même cœur et attache, forêts2,3,5,6,7)
ont respectivement les rangs35,34,35,35,35. Ce petit échantillon n'est
pas une distribution sur l'ensemble des cadres.

## Construction du cadre

Le programme `norm16_frame_pilot.py` fixe le cœur, les huit attaches D
déjà archivées et la forêt Z. Il ajoute les huit simples de cellule
(P0,q), dont les multiplicités sont déjà forcées. Il choisit les arêtes
D–Z, D–B(P0), Z–B(P0) et B(P0)–B(P0) sous les contraintes suivantes :

1. D est indépendant ; d_Z(d)=4 ; d_D(z)=2+d_Z(z).
2. Chaque paire dans les43 positions a au plus2-A_uv voisins communs.
3. Pour toute paire contenant P0, l'égalité est imposée : son voisinage
   complet est présent.
4. Pour chaque simple b de B(P0), d_Z(b)=1+d_D(b) ; les degrés sont≤14.

Le premier témoin est obtenu en moins d'une seconde de résolution
CP-SAT localement. Un contrôle direct des seules contraintes imposées
accompagne l'export. Ce temps ne mesure pas une classification complète.

## Colonnes à donner au moteur de rang

Un masque est un entier dont le bit i indique l'adjacence au sommet i
du cadre. Toutes les attaches au cœur sont fixées par les types.
Chaque sommet extérieur au cadre est non adjacent à P0 ; ses deux
voisins dans N(P0) imposent son nombre de voisins dans Y :

    d_Y(v)=2-|N(v) inter N(P0) inter Q|.

Pour D, on impose aussi l'absence d'arêtes aux deux D déjà présents,
exactement quatre voisins Z, et les budgets de degrés D des simples
déjà présents. Pour un simple b, on utilise

    d_Z(b)=1+d_D(b),
    sum_{simples b} binom(d_D(b),2)=9-W_Z.

Ici W_Z=3, donc le budget total vaut6. On en soustrait les contributions
des huit simples déjà présents. Tout candidat respecte ensuite

    |N(v) inter N(u) inter cadre| <= 2-A_uv

pour chacun des37 sommets u du cadre. L'export énumère ces colonnes
nécessaires ; il n'affirme pas qu'elles se prolongent simultanément.
Leurs produits de Seidel et leur isotropie restent à tester par LAB.

Pour la cellule de P1, un voisin D (D0, indice27) est déjà dans le
cadre. Les neuf membres restants ont les nombres de colonnes suivants :

| Type | Colonnes |
|---|---:|
| D2, attaché à P1,P2,Q0,Q1 | 13 |
| chacun des deux simples (P1,Q2) | 2223 |
| chacun des deux simples (P1,Q3) | 2164 |
| simple (P1,Q4) | 1876 |
| simple (P1,Q6) | 2548 |
| chacun des deux simples (P1,Q7) | 3354 |

Les62 types restants, leurs domaines et les sept cellules P1..P7 sont
dans le JSON. Les règles entre deux membres nouveaux doivent aussi
compter leurs voisins communs parmi tous les sommets déjà placés,
pas seulement dans la base initiale. Le voisinage complet de chaque
positif doit finalement induire sept arêtes disjointes.

## Reproduction et suite

Depuis la racine du dépôt, avec OR-Tools installé :

    python code/codex/norm16_frame_pilot.py --case 0 --orbit 0 --forest 2
    python code/codex/norm16_typed_frame.py

Les modules de construction emploient OR-Tools ; le JSON livré n'en
dépend pas pour être lu. La note251 et sa liste de quinze forêts
restent des résultats indépendants de ce pilote.

LAB possède le moteur de rang. La tâche Codex suivante est d'exploiter
les contraintes des incidences pour réduire et borner le catalogue,
puis de traiter les cœurs18/20. Aucun ordre de grandeur défendable du
nombre total de cadres n'est encore obtenu.
