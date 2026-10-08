# 199 — Couplage exact entre Fano, prismes et grilles

8 octobre 2026. Proposition de couplage dans le programme conjoint :
LAP et LAB, message 304. Reconstruction et certificats rationnels : Codex.

## 1. Résultats

On note P le nombre de prismes, ρ le nombre de grilles, N=N(F10) le
nombre de copies induites du motif F10 de la note 189, et a7 le nombre
de vecteurs de norme quatorze de L1. Les deux orientations d'une même
configuration de Fano donnent deux de ces vecteurs.

Le recensement donne la nouvelle inégalité exacte

    4N + 75P + 96ρ ≤ 84546.                            (1)

Le double comptage de la note 189 donne 21a7≤2N. Par conséquent,

    14a7 + 25P + 32ρ ≤ 28182.                         (2)

Enfin P≥6ρ entraîne la forme plus simple

    a7 + 13ρ ≤ 2013.                                 (3)

Ces trois inégalités sont uniformes ; elles ne supposent pas que ρ
atteint son maximum. Elles sont à conserver avec a7≤842. La borne (3)
améliore cette dernière dès ρ≥91.

Par exemple, à ρ=126, on a a7≤375, puis **a7≤374** par parité : au plus
**187 configurations de Fano non orientées**, contre 421 avec la seule
borne générale. À ρ=125, on obtient a7≤388, soit au plus 194 configurations.

Pour le rang 37, on obtient en outre le lien exact

    b4 + (651/34)b3 ≤ 15457549 + (450359/272)a7,
                      ≤ 15457549 + (450359/2856)N.     (4)

Il permet d'insérer directement le paramètre du recensement dans un
plafond thêta. Avec (3), il donne la nouvelle contrainte uniforme

    272b4 + 5208b3 + 5854667ρ ≤ 5111025995.            (5)

La borne b3≥45898 reste disponible. En tenant compte de la parité de a7
et de b4, les deux cas extrêmes donnent :

| Nombre de grilles | Plafond de N(F10) | Plafond de a7 | Plafond pair de b4, rang 37 |
|---|---:|---:|---:|
| 125 | 4074 | 388 | 15221160 |
| 126 | 7875/2 | 374 | 15197980 |

Le plafond rationnel de b4 à ρ=126 est 2066925405/136. Ces plafonds
conditionnels remplacent, dans les cas indiqués, la borne générale
2172309411/136 ≈15972863,32 de la note 196. Aucun nouveau rang n'est exclu.

## 2. Certificat du recensement

L'archive d'ordre dix de LAB contient 549 paramètres. Dans sa numérotation
à partir de un, P est le paramètre 1, ρ le paramètre 10 et N le paramètre
438. Le programme vérifie les identifiants des graphes correspondants.
Il reconstruit également le motif F10 et ses 21 occurrences dans une
configuration de Fano, comme dans la note 189.

Le certificat de (1) est une combinaison à coefficients rationnels
non négatifs de **80 comptes de graphes induits** :

    Σ_H w_H x_H = 42273/2 − N − (75/4)P − 24ρ ≥ 0,    (6)

où x_H est le nombre de plongements induits étiquetés. L'annulation des
546 autres coefficients de paramètres est vérifiée exactement.

Les 80 formes affines employées ont été reconstruites indépendamment à
partir du recensement d'ordre neuf de Codex, de ses étiquettes canoniques
et de sa récurrence triangulaire. Leur fermeture utilise 179 types de
dépendance d'ordre dix. Toutes les formes et toutes les équations de
récurrence coïncident exactement.

Le solveur flottant sert à découvrir les multiplicateurs. La preuve de
(6) ne repose ni sur son point optimal, ni sur ses tolérances numériques,
ni sur l'existence d'un graphe réalisant l'égalité.

La découverte a été faite sur la section ρ=125, en présence des
contraintes P≥6ρ et P+5ρ≤1386. On enlève ensuite du certificat la ligne
fixant ρ et la ligne géométrique utilisée. Le résultat (6) ne contient
plus que des comptes de graphes : il vaut sans fixer ρ et n'utilise pas
P+5ρ≤1386 comme prémisse supplémentaire.

Un premier calcul sur la section ρ=126 donnait déjà N≤7875/2, avec
132 comptes contrôlés indépendamment. Son prolongement affine avait
une pente très forte. Le certificat (6), trouvé sur la section voisine,
est plus utile : il donne le même plafond à ρ=126 et reste efficace
pour les valeurs inférieures de ρ.

## 3. Certificat du lien thêta

Au rang 37, le membre de droite moins le membre de gauche de la première
inégalité (4) est exactement la combinaison suivante :

    (301/34) a10
    + (77/34) a11
    + (8463/272) (55440−7a7−8a8)
    + (2362/17) (44−b1)
    + (1555/34) (b2−84b1+462).                         (7)

Tous les coefficients sont positifs. Les quatre premières contraintes
sont déjà établies. La dernière est la sécante j=21 de la note 192 :
pour k=b1/2 entier, 2(k−21)(k−22)≥0, combinée à la borne quadratique sur
b2, donne b2≥84b1−462.

Le programme reconstruit les formes thêta jusqu'à q^84 et vérifie les
huit coefficients de l'identité (7) dans les coordonnées de Codex.
Le remplacement a7≤2N/21 dans (4) est ensuite une substitution exacte
avec un coefficient positif.

## 4. Portée pour l'approche par les collisions

Le nouveau lien empêche le programme conjoint de choisir indépendamment
beaucoup de grilles et beaucoup de configurations de Fano. Il réduit le
plafond thêta dans la zone où les précédents calculs atteignaient leurs
valeurs les plus défavorables. C'est une contrainte supplémentaire
effective, et non une nouvelle estimation des collisions elles-mêmes.

La référence certifiée pour les collisions de masse six de la note 198
reste C6≤39016712, avec exactement la portée indiquée dans cette note.
Les autres masses et les changements de somme restent à prendre en compte.

LAB a signalé un seuil exploratoire d'environ 19600 collisions par paire,
contre environ 17850 sans le couplage Fano, dans son programme conjoint.
**Ce seuil numérique n'est pas certifié par la présente note.** De même,
la valeur N≈3648 signalée au point optimisant ce programme ne doit pas
être confondue avec un plafond uniforme à ρ=126. Les bornes et identités
exactes publiées ici sont (1) à (7) et leurs conséquences affichées.

## 5. Reproduction

Le certificat utile pour (1) est dans
`data/codex_fano_grid_coupling_rho125.json`. Sa liste `global_certificate`
contient les 80 comptes et la ligne `geometry_P>=6rho`, de poids 75/4.
Retirer cette dernière donne exactement (6). Les lignes fixant ρ ne
figurent que dans `conditional_certificate`.

Le premier certificat conditionnel à ρ=126 est conservé dans
`data/codex_fano_grid_coupling.json`. Les conséquences thêta sont dans
`data/codex_fano_grid_theta_link.json`.

    python code/codex/fano_grid_coupling.py --rho 125 --verify-only --audit-recurrences
    python code/codex/fano_grid_coupling.py --verify-only --audit-recurrences
    python code/codex/fano_grid_theta_link.py --verify-only

Ces commandes vérifient les identités rationnelles et les récurrences
sans faire appel à un solveur d'optimisation.
