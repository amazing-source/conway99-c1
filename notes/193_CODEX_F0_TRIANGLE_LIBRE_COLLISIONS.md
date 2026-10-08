# 193 — F0 sans triangle positif : pertes de masses six et sept

8 octobre 2026. Sous-famille F0 proposée par LAB au message 254 ;
énumération, restriction sans triangle et certificats par Codex.

On considère les représentants de norme projetée huit

    F0 = { ±(1_W−1_Y) : |W|=6, e(W)=7, |Y|=3, Y triangle, W⊥Y }.

La notation W⊥Y signifie ici qu'aucune arête ne les relie. On note Ftf la
sous-famille où W ne contient aucun triangle. Les anciennes familles Fp
ont p sommets positifs et p−3 négatifs, pour p=3,4,5, et Q=8.
Tous les résultats ci-dessous incluent les deux signes.

**Résultat principal.** Le nombre total de paires en collision de masses six
et sept, internes à Ftf ou entre Ftf et F3∪F4∪F5, est au plus

    642τ + 710Ω.

Ici τ compte les paires non ordonnées de prismes jumeaux et Ω les paires
non ordonnées de copies de D reliées par leur centre, comme dans les
notes 181 et 188. Pour F0 entier, la même méthode donne 10380τ+1528Ω.
Ce sont des plafonds de pertes par paires ; on ne suppose pas qu'ils
soient atteints dans un graphe ambiant.

La restriction laisse exactement deux types de W. Leur réunion fournit
**au moins 166320 représentants bruts signés**, par un certificat exact
du recensement d'ordre neuf. Ce nombre n'est pas encore un nombre de
vecteurs distincts : les masses huit et neuf et les collisions de sommes
différentes restent à traiter. Aucun nouveau rang n'est exclu ici.

## 1. Détail des bornes par canal

Pour F0, les résultats sont :

| Masse | Interne F0 | Avec F3 | Avec F4 | Avec F5 | Borne jointe |
|---:|---:|---:|---:|---:|---:|
| 6, par paire de prismes | 7564 | 0 | 1200 | 1680 | **10380** |
| 7, par paire de D | 1440 | impossible | 8 | 80 | **1528** |

Pour Ftf :

| Masse | Interne Ftf | Avec F3 | Avec F4 | Avec F5 | Borne jointe |
|---:|---:|---:|---:|---:|---:|
| 6, par paire de prismes | 192 | 0 | 0 | 480 | **642** |
| 7, par paire de D | 684 | impossible | 8 | 24 | **710** |

Les valeurs 1200 et 8 pour F0, et 8 pour Ftf, sont des comptes exacts
conditionnellement à la paire de supports ; les autres valeurs non nulles
sont des majorations. Les bornes jointes optimisent la somme des pertes,
et peuvent donc être inférieures à la somme des maxima séparés. Ainsi le
premier calcul séparé 672τ+716Ω se renforce en 642τ+710Ω.

## 2. Deux types positifs et deux variantes plus étroites

Il existe dix types admissibles de W à six sommets et sept arêtes. Deux
seulement sont sans triangle, tous deux de degrés 2,2,2,2,3,3 :

| Code Codex IR | Voisinages binaires | Cycles induits de longueur quatre | Biparti |
|---:|---|---:|---|
| 7064 | [48,48,40,20,11,7] | 1 | non |
| 21812 | [40,36,18,17,44,19] | 2 | oui |

Les codes des graphes W∪Y correspondants dans le recensement d'ordre neuf
sont respectivement 1292951744 et 35652125060. Chacun possède un unique
triangle isolé, donc le nombre brut signé de Ftf est exactement

    2 N9(1292951744) + 2 N9(35652125060).

`f0_positive_types.py` retrouve les dix types dans les 5311 graphes du
recensement, vérifie les deux codes sélectionnés et contrôle une combinaison
linéaire à coefficients rationnels non négatifs prouvant la borne 166320.
Un point rationnel du modèle de recensement atteint cette valeur ; sa
faisabilité est vérifiée exactement. Cela ne prouve pas l'existence d'un
graphe ambiant réalisant ce point.

On peut aussi ne retenir qu'un des deux types. Les bornes sont alors :

| Type retenu | Masse 6 interne | Masse 6 avec F5 | Masse 6 jointe | Masse 7 interne | Masse 7 avec F4 | Masse 7 avec F5 | Masse 7 jointe |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 7064 | 72 | 360 | **408** | 98 | 0 | 24 | **122** |
| 21812 | 138 | 480 | **480** | 336 | 8 | 0 | **344** |

Les collisions avec F3 et celles de masse six avec F4 restent nulles.
Ces variantes ne peuvent pas être additionnées sans traiter les collisions
entre les deux types ; la ligne Ftf les traite déjà conjointement.

## 3. Paramétrisation exhaustive

Pour une différence propre binaire δ=1_X−1_X′ de masse m∈{6,7}, les supports
du noyau ont taille m. Prenons ψ∈F0 de somme +3 et un partenaire ψ′∈Fp.
Le nombre de sommets communs extérieurs est r=p+3−m. Toutes les paires
de cette orientation s'écrivent

    ψ  =1_X −1_B−1_B′+1_C−1_K,
    ψ′ =1_X′−1_B−1_B′+1_C−1_K,

avec B⊆X, B′⊆X′, C,K extérieurs disjoints, et

    |C|=c, |K|=r−c, |B|=m−6+c, |B′|=3−r+c.

Pour p=6, le partenaire est lui aussi filtré dans F0 ou dans la restriction
choisie. Une orientation fixée compte les paires internes non ordonnées
une fois. Pour p<6, les deux orientations de δ doivent être parcourues :
les tailles des familles distinguent le premier représentant du second.
Enfin on multiplie par deux pour les représentants opposés de somme −3.

Les coordonnées du noyau sont binaires car S≥4h et m≤7. Il n'y a donc
pas d'autre type de recouvrement à ces masses. Le programme vérifie
e(W)=7, e(Y)=3 et e(W,Y)=0 pour chaque représentant nouveau. L'égalité
des normes des deux partenaires suit de la différence propre et est
aussi contrôlée directement par la forme quadratique complète.

Le filtre « sans triangle » est calculé par les triangles entièrement
dans le noyau, puis ceux rencontrant un, deux ou trois points extérieurs.
Un contrôle indépendant reconstruit les triangles du graphe étendu.
Pour les variantes par type, le code canonique de W est en outre
comparé à une vérification indépendante par bipartition.

## 4. Contraintes et certification

La géométrie des profils et les équations proviennent de la note 188 :
40 profils d'effectifs exacts autour de deux prismes, puis 4480
appariements admissibles des sept apices autour de deux copies de D.

À masse six :

- Avec F3, aucun point extérieur n'est nécessaire et W serait un prisme,
  ce qui contredit e(W)=7.
- Avec F4, il y a un point extérieur. Les 60 points simples donnent
  chacun 20 collisions signées, les autres profils zéro : 1200 au total.
  W contient alors un prisme privé d'un sommet, donc un triangle ; Ftf
  exclut tout ce canal.
- Avec F5, il y a deux points extérieurs. Leur coût est affine dans les
  nombres d'arêtes entre les 40 profils. Le modèle possède 805 variables
  de paires, les équations de degrés et de voisins communs avec le noyau,
  et les arêtes localement forcées ou interdites.
- En interne, il y a trois points extérieurs. Le modèle de la note 188
  possède 64147 variables et 89154 lignes. Le programme réutilise ses
  63342 types de triples canoniques en recalculant les coûts filtrés.
  Pour la borne jointe, il ajoute à l'objectif les coûts de F5 sur les
  variables de paires, le compte constant de F4, et impose explicitement
  les arêtes forcées/interdites du modèle de paires.

Les multiplicateurs LP sont rationalisés, puis les résidus sont couverts
par les plafonds combinatoires exacts des variables, selon la note 188.
Voici les plafonds rationnels conjoints avant arrondi au nombre pair :

| Famille | Plafond rationnel à masse six | Plafond entier pair |
|---|---:|---:|
| F0 | 10381500002313/1000000000 | 10380 |
| Ftf | 80421686827/125000000 | 642 |
| Type 7064 | 204000000189/500000000 | 408 |
| Type 21812 | 240000000179/500000000 | 480 |

À masse sept, aucun LP flottant n'intervient : on parcourt tous les
appariements, puis les onze valeurs possibles de t=e(apices), et on
affecte les arêtes disponibles aux plus grands incréments de coût.
Les collisions avec F5 dépendent seulement du profil du point extérieur.
La borne jointe maximise leur somme avec la perte interne et le compte
constant de F4, pour un même appariement.

## 5. Une élimination supplémentaire à masse huit

**Une collision interne à Ftf ne peut pas avoir une différence non binaire
de masse huit.** En effet, la classification de la note 183 impose qu'un
support contenant un coefficient deux soit un moulin de trois triangles,
avec poids deux au centre et un aux six feuilles.

Orientons la différence pour que ce support soit positif. Le centre
appartient alors à W∩Y′. Parmi les six feuilles, au plus deux peuvent
être prises en charge par les deux autres sommets de Y′. Au moins quatre
appartiennent donc à W. Quatre feuilles parmi les trois paires du moulin
contiennent une paire complète ; avec le centre, elles forment un triangle
dans W, contradiction.

Cet argument concerne les collisions **internes** à Ftf. Il n'élimine
pas toutes les différences non binaires avec F5, dont le support positif
peut contenir des triangles. Les différences binaires de masse huit et
les différences de masse neuf restent également à examiner.

## 6. Reproduction et limites

Les scripts sont `code/codex/f0_collision_patterns.py`,
`f0_prism_bounds.py`, `f0_mass7_matching_bound.py` et `f0_positive_types.py`.
Les données portent le préfixe `data/codex_f0_`.

Pour chaque variante, utiliser aucun drapeau (F0), `--triangle-free`
(Ftf), ou `--triangle-free --positive-type 7064` / `21812`.

    python code/codex/f0_collision_patterns.py --mass 6 --p 6 --triangle-free
    python code/codex/f0_prism_bounds.py --p 6 --triangle-free --verify-only
    python code/codex/f0_prism_bounds.py --p 6 --triangle-free --joint --verify-only
    python code/codex/f0_mass7_matching_bound.py --triangle-free --verify-only
    python code/codex/f0_positive_types.py --verify-only

La génération des patrons doit aussi être exécutée pour p=3,4,5 à masse
six et p=4,5,6 à masse sept. `--verify-only` permet de reconstruire les
patrons et les comparer aux archives, ou de contrôler les certificats
rationnels sans relancer l'optimisation. Le fichier de chaque appariement
de masse sept est conservé dans une archive gzip déterministe.

Les pertes traitées ici ne suffisent pas à transformer le compte brut
en minoration de b4. Outre les masses restantes, les collisions de sommes
différentes avec les familles négatives (6,0) et (7,1) restent ouvertes.
Il faut y conserver **la branche avec triangle négatif non annulé** de
la note 183, et pas seulement la branche non négative des grilles.

## 7. Compter les classes sans fixer leur taille

Après la publication initiale, LAB a corrigé au message 257 son budget
global : certaines collisions des indicatrices à neuf sommets manquaient.
Son calcul flottant avec les pertes séparées 672τ+716Ω ne donne pas un
gain net pour Ftf. La présente note ne revendique donc aucune amélioration
du plancher global de b4. Voici une autre manière exacte d'exploiter les
comptes de collisions, proposée au message 260.

Soit R le nombre brut de représentants **de toute une famille de même
norme**, C le nombre total de paires non ordonnées qui ont la même image,
et D le nombre d'images. Pour tout entier k≥1, la note 186 donne

    D ≥ 2R/(k+1) − 2C/[k(k+1)].                         (6)

Cette formule ne suppose ni une taille maximale des classes, ni une
décomposition canonique des représentants en prisme et reste. Pour k=2,
elle devient D≥(2R−C)/3. On peut choisir des valeurs différentes de k
pour les normes six et huit, puis combiner leurs minorations. C doit
cependant inclure **toutes** les collisions : les seules pertes de masses
six et sept de cette note ne suffisent pas.

Il existe aussi une version qui conserve le compte des anciennes images.
Notons Rn le nombre de nouveaux représentants, Cnn les paires en collision
entre eux et Cna les paires entre un nouveau et un ancien représentant.
Le nombre Δ de nouvelles images absentes de la famille ancienne satisfait

    Δ ≥ 2Rn/(k+1) − 2Cnn/[k(k+1)] − 2Cna/(k+1).        (7)

Preuve : dans une classe sans ancien représentant et contenant m nouveaux,
(7) se réduit à l'identité de la note 186,

    1 − 2m/(k+1) + m(m−1)/[k(k+1)]
      = (m−k)(m−k−1)/[k(k+1)] ≥ 0.

Si la classe contient n≥1 anciens représentants, son gain réel est zéro.
Sa contribution au membre droit de (7) vaut

    2m(1−n)/(k+1) − m(m−1)/[k(k+1)] ≤ 0.

La somme prouve (7), même si les anciens représentants ont eux-mêmes des
doublons. Tout plafond prouvé pour Cnn ou Cna peut remplacer le compte
correspondant puisque son coefficient est négatif. Cela permet de tester
les nouvelles sous-familles sans réduire le plancher déjà établi pour les
anciennes. Les canaux de collision restant ouverts doivent encore être
complétés avant toute application numérique globale.
