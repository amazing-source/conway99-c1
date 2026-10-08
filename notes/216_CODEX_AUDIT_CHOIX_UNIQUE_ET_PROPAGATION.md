# 216 — Audit des preuves par un choix puis propagation

8 octobre 2026. Audit du résultat LAB, note 17.59, commit 331f76e,
annoncé dans le message 385. Le mécanisme est confirmé sur les
quatre graphes de contrôle : **1721 branches d'apex exclues par
38518 feuilles de propagation exacte**, avec toutes les traces
archivées et revérifiées. Aucun solveur LP ou CP n'intervient dans
la production ou la vérification de ces preuves.

Les graphes étaient déjà exclus en septembre. L'avancée est la
simplification et la certification du mécanisme local ; aucun
nouveau rang global n'est exclu. Une ablation supplémentaire montre
que, sur treize branches pilotes, une seule étoile conditionnée
par l'apex suffit déjà.

## 1. Hypothèses effectivement conservées

Chaque exemple utilise l'arête proche (0,12), le cadre générique
au rang 37, et les pools unaires historiques des notes 211–214 :
six points, deux par couche, conditions locales et norme de Green 6.
Pour un apex commun w fixé, chaque ombre privée conserve aussi
son produit de Green 3 avec w et l'intersection de taille au plus 2.

Entre deux ombres privées, le mode `green` impose uniquement

    n_iᵀ H⁺₇ n_j ∈ {2,3} modulo 7.

Les 72 sommes ponctuelles sont exactes :

    Σ_{i dans l'étoile s, privé} n_i = K e_s − w.

Les contraintes privées d'intersection, de capacité, de saturation,
de plafond K et de positivité réelle ne sont pas utilisées. Cela
ne signifie pas que les pools unaires sont dépourvus de filtres
locaux : ceux-ci font partie des hypothèses conservées.

Les domaines sont reconstruits avant chaque propagation ; aucune
suppression obtenue dans un mode plus fort n'est réutilisée.

## 2. Une preuve de profondeur un, une fois l'apex fixé

La propagation de base alterne deux règles nécessaires :

1. supprimer un candidat sans partenaire compatible dans un autre
   domaine ;
2. supprimer un candidat dont une coordonnée rend une somme exacte
   inaccessible, même entre les minima et maxima des autres domaines.

Sur les 1721 branches, cette propagation de base ne produit aucune
contradiction. On choisit ensuite un domaine de taille minimale,
avec départage par indice, et on essaie **tous** ses candidats.
Pour chaque candidat c, on fixe ce seul choix et on propage.
Chaque essai finit par une contradiction.

Les feuilles repartent toutes des **mêmes domaines de base**.
Aucune feuille n'hérite d'une suppression obtenue dans une autre.
Puisque tous les candidats du pivot sont couverts, la branche
d'apex est impossible. C'est une recherche de profondeur un
conditionnellement au choix de w, et non une recherche sans choix.

## 3. Audit du programme LAB et vérification séparée

Le découpage des sous-tables de `sac_two_star.py` est correct :
`compat[i,j][ix(dom_i,dom_j)]`, dans les deux sens. Le report des
indices des domaines restants est correct aussi. Dans les sorties
contrôlées, seules les suppressions du pivot se succèdent, donc
fixer le pivot à un autre candidat rend ces suppressions antérieures
sans effet sur la nouvelle feuille.

Un point manquait aux certificats initiaux : `close()` appelait
`replay` seulement lorsque la propagation survivait. Les feuilles
contradictoires n'étaient pas rejouées et leurs traces n'étaient
pas enregistrées. Cela ne constituait pas une erreur logique du
programme, mais la vérification publiée était incomplète.

`code/codex/two_star_single_choice.py` produit maintenant chaque
trace, puis la vérifie immédiatement avec `replay_original` :

- les indices de la trace sont ramenés aux candidats originaux ;
- les supports sont vérifiés dans les tables originelles, sans
  employer les sous-tables du producteur ;
- les bornes de somme sont recalculées en entiers sur les domaines
  courants ;
- la contradiction terminale est vérifiée ;
- la liste des feuilles doit être exactement le domaine du pivot,
  sans doublon ni candidat manquant.

Le vérificateur ne relance pas la recherche ni l'algorithme de
propagation. La construction initiale des pools et des tables
reste commune aux deux programmes : ce point n'est pas présenté
comme une implémentation indépendante du modèle mathématique.

Chaque archive complète a ensuite été relue depuis le disque.
Les quatre listes de suppressions coïncident exactement avec
celles de LAB.

## 4. Résultats exhaustifs par graphe

| Graphe | Branches d'apex | Contradictions de base | Branches exclues après un choix | Feuilles |
|---|---:|---:|---:|---:|
| Boule 5 | 368 | 0 | 368 | 6882 |
| Boule 9 | 464 | 0 | 464 | 9484 |
| Boule 12 | 416 | 0 | 416 | 9395 |
| Cyclique (2,4,1) | 473 | 0 | 473 | 12757 |
| Total | **1721** | **0** | **1721** | **38518** |

Les résumés `data/codex_single_choice_{ball5,ball9,ball12,cyclic241}.json`
contiennent les graphes, centres, indices d'apex, nombres de feuilles,
références du commit LAB et empreintes SHA-256 des archives
`.proofs.jsonl.gz` correspondantes. Ces quatre archives occupent
15984562 octets. `data/codex_single_choice_coverage.json` rassemble
leurs empreintes, couvertures complètes et nombres de feuilles.

Pour chacune des quatre sorties :

    python code/codex/two_star_single_choice.py --out data/codex_single_choice_ball5.json --verify-only

Le script exige la couverture exacte des indices 0,…,m−1 avant
d'annoncer l'exclusion complète du graphe d'entrée. Une limite de
temps ou un balayage partiel ne peut produire cette conclusion.

## 5. Contrôles positifs et négatifs du vérificateur

Sur quinze feuilles du premier pilote, le replay antérieur sur
sous-système et le nouveau replay sur indices originaux donnent
exactement les mêmes domaines survivants.

Quatre corruptions volontaires sont rejetées : feuille manquante,
candidat dupliqué, trace effacée et indice de suppression invalide.

Pour trois graines, on choisit une solution entière artificielle,
on adapte les sommes à ses ombres et on autorise ses couples dans
les tables. La procédure conserve chaque candidat de cette solution
dans la feuille correspondante et conclut à une survie. Ces témoins
sont des contrôles du moteur logique, pas des graphes C1.

## 6. Ablation des relations entre les deux étoiles

On remplace toutes les tables entre étoiles différentes par des
tables entièrement vraies, avant toute propagation. Les tables
internes gardent seulement les valeurs de Green 2 ou 3 ; les sommes
et les filtres unaires/apex sont inchangés.

Treize branches pilotes sont encore exclues après un seul choix.
Dix le sont avec le pivot minimal initial ; trois demandent un
autre pivot :

| Graphe, apex | Pivot minimal qui laisse un choix vivant | Pivot donnant une preuve complète |
|---|---:|---:|
| Boule 12, 113 | 2 | 4 |
| Cyclique, 33 | 6 | 12 |
| Cyclique, 53 | 9 | 6 |

Les indices sont comptés à partir de zéro. Une survie signifie
uniquement que cette propagation ne conclut pas, pas qu'une
solution existe.

Les treize cas sont : boule 5 {0,33}, boule 9 {0,33}, boule 12
{0,33,113,137,184}, cyclique {0,33,53,100}. Le script
`code/codex/single_choice_within_pilots.py` produit et vérifie leurs
traces. Il vérifie aussi que toutes les suppressions de chaque
feuille et sa contradiction terminale restent du côté du pivot,
et qu'aucune suppression de base n'utilise une table entre étoiles.
C'est donc bien une preuve portée par une seule étoile, avec
l'apex et les conditions unaires conservées.

Les 349 feuilles ont toutes été archivées puis rejouées depuis
`data/codex_single_choice_within_pilots.proofs.jsonl.gz`.
Rejeu :

    python code/codex/single_choice_within_pilots.py --out data/codex_single_choice_within_pilots.json --verify-only

Cette ablation ne couvre pas les 1721 branches. Elle interdit
néanmoins de déduire de leur exclusion que les relations entre
les deux étoiles sont indispensables. L'étape suivante est de
chercher si l'obstruction d'une étoile, conditionnée par deux
ombres, admet une formulation uniforme.

## 7. Rapport avec les autres méthodes

La note 215 éliminait les 473 branches cycliques par des contraintes
réelles et propagation, sans choix supplémentaire. Ici, les tables
privées sont plus faibles, mais un choix supplémentaire est permis.
Ce sont deux façons complémentaires d'obtenir des contradictions
exactes sur les mêmes exemples.

Ni ce balayage, ni les treize pilotes ne prouvent que tous les
graphes proches admissibles possèdent une telle contradiction.
L'obtention d'un énoncé uniforme reste la question T20 ouverte.
