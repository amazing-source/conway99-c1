# 201 — Ce que les fentes disent d'une droite dans six grilles

8 octobre 2026. Audit de la question de LAB au message 319 (son message
215), après la note 200. Il s'agit de préciser la portée des notes
108–111, pas d'une nouvelle exclusion de graphe ou de rang.

## 1. La question structurelle

Une droite Θ dans six grilles donne, en chacun de ses trois points,
une classe h complète avec les six autres classes. LAB propose
d'exclure cette configuration par les fentes de la note 108 ou leur
second ordre. Son modèle global comprend six prismes, leurs trois
apices communs et soixante points B.

Le fait d'avoir une classe complète avec toutes les autres donne bien
une règle supplémentaire très simple. Mais les équations agrégées
des notes 108–109 restent compatibles avec cette hypothèse. Un témoin
entier, désormais archivé, le démontre. La compatibilité des voisinages
effectifs, notamment entre les trois apices, reste une condition plus forte.

## 2. Les quatre fentes forcées

Supposons h complète avec toutes les classes, et prenons y∈Q_ij avec
h∉{i,j}. Aucun voisin spécial de y ne porte une étiquette de h : les
partenaires des étiquettes de h restent appariés entre eux, et les
ombres les fixent, par complétude.

Pour les quatre classes k hors de {h,i,j}, les équations donnent

    Σ_k n_{hk}(y)=4,        0≤n_{hk}(y)≤1.

Donc

    n_{hk}(y)=1 pour chacun de ces quatre k.             (1)

Dans le modèle de LAB, (1) exprime l'unique voisin de b dans chacun
des autres prismes. Ce n'est pas encore une contrainte nouvelle sur
son modèle, qui l'impose déjà.

Il faut conserver le sens de (1). Les quatre points de Q_ij ont chacun
un voisin dans Q_hk, donc il y a quatre arêtes entre les deux blocs.
Si Q_ij est incomplet, cela ne rend pas ce graphe biparti un couplage
parfait : les degrés des quatre points de Q_hk peuvent être, par
exemple, `(0,0,2,2)`. Le mécanisme de bijections et d'holonomie de la
note 105 ne s'applique donc pas automatiquement.

## 3. Un témoin exact pour la relaxation du second ordre

On reprend la configuration L14 de la note 111 : seules les étiquettes
0⁺ et 1⁺ tordent, toutes deux les classes {2,3}, avec le premier choix
de partenaires produit par `slot_tests.configs`. Les paires incomplètes
sont exactement

    {02,03,12,13}.

Les classes **4,5,6 sont toutes complètes avec les six autres**.

Le fichier `data/codex_universal_hub_slot_witness.json` fournit les
840 nombres entiers n_R(y). Le vérificateur reconstruit les voisins
spéciaux, les bornes et les équations depuis la configuration, puis
contrôle exactement :

- les 525 équations linéaires : 420 fentes et 105 cohérences entre blocs ;
- toutes les bornes, dont n_R(y)≤1 vers un bloc complet ;
- les 231 identités du second ordre, diagonales comprises ;
- la règle (1) pour chacun des trois centres 4,5,6.

Les identités du second ordre sont celles de la note 109. En posant
d_P(v)=|N(v)∩Q_P| et en comptant les arêtes internes deux fois :

    Σ_v d_P(v)d_R(v) = 32−e_PR     si P∩R=∅ ;
                      24−e_PR     si |P∩R|=1 ;
                      64−2e_PP    si P=R.

La recherche s'est arrêtée après 29 solutions linéaires complètes ;
elle n'utilise aucun solveur. La relecture du témoin ne fait aucune
recherche. Parmi les directions qui ne sont pas des couplages, on a

    Q_45 vers Q_02 : (0,0,2,2),
    Q_45 vers Q_03 : (2,2,0,0).

Le résultat est un **témoin des équations agrégées uniquement**.
Il ne fournit ni arêtes entre les blocs, ni graphe à 99 sommets,
ni compatibilité de trois voisinages autour d'une même droite.

## 4. La condition manquante est déjà visible dans L14

La configuration utilisée ci-dessus est elle-même exclue par la
note 111. Il n'y a aucune contradiction entre les deux résultats :
la preuve de cette note utilise les ensembles réels de voisins communs,
et pas seulement leurs sommes par blocs. Elle force cinq contributions
pour un budget disponible de quatre.

Ainsi, les notes 108–109 ne contiennent pas à elles seules une preuve
qu'une droite ne peut pas appartenir à six grilles. Leur hypothèse de
classe complète avec toutes les autres survit même avec trois telles
classes. En revanche, le type de raisonnement de la note 111 indique
une condition à travailler : la compatibilité des sous-ensembles de
voisins dans les blocs, et leur réalisation simultanée aux trois apices.
Cette compatibilité n'est pas résolue ici.

Le modèle à soixante noms proposé par LAB est une restriction
structurelle du problème C1. On ne déduit ni qu'il est réalisable,
ni qu'il est aussi difficile que le problème sans restriction. Les
moments seuls ne tranchent pas. Aucun nouveau comptage de collisions
ou programme linéaire global n'a été lancé pour cet audit.

## 5. Reproduction

    python code/codex/universal_hub_slot_witness.py --verify-only

La commande sans option reconstruit un témoin par recherche finie.
Le vérificateur et le témoin reposent sur les définitions locales
déjà présentes dans `slot_calculus.py`, `slot_tests.py` et
`slot_second_order.py` ; les nombres affichés sont vérifiés en entiers.
