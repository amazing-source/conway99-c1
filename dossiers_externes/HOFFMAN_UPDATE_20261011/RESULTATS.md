# Mise à jour Hoffman : résultats obtenus ici

**11 octobre 2026 — dépôt lu jusqu'à `f4e82d78d68510abca1782536ae102970f3e7d16`, branche `claude/v7-simultaneous`.**

## Résultat principal : deux familles de bords entièrement exclues à 99

Aucun graphe SRG(99,14,1,2) avec une coclique de Hoffman de 22 sommets ne peut avoir un design de voisinages :

- invariant par un cycle transitif de longueur 22 ;
- invariant par un groupe de 21 éléments fixant un point de la coclique et agissant régulièrement sur les 21 autres.

**Aucune symétrie n'est imposée à la complétion du graphe.** Une symétrie du design n'est pas supposée se prolonger au graphe entier. Les 77 voisinages extérieurs sont choisis indépendamment, puis couplés par leurs équations exactes.

Le cas du groupe cyclique C21 fixant un point est impossible directement : il faudrait répéter l'unique orbite courte des blocs contenant le point fixe. Le groupe non abélien d'ordre 21 est étudié exhaustivement.

| Famille d'action sur les points du design | Sélections normalisées de designs | Intersection de trois points, rejet immédiat | Designs restant à compléter | Complétions possibles |
|---|---:|---:|---:|---:|
| C22 transitif | 80 | 8 | 72 | **0** |
| C7⋊C3 régulier sur 21 points, plus un point fixe | 236 | 37 | 199 | **0** |

Les nombres 72 et 199 ne sont pas des nombres de classes d'isomorphisme. Ce sont des présentations normalisées couvrant toutes les instances des familles définies. Leurs éventuels recouvrements ne sont pas additionnés comme des classes distinctes.

### Ce qui a effectivement été calculé

Les 271 designs restants ont été générés à partir de toutes les orbites de blocs possibles. Les voisinages candidats sont tous énumérés. Aucune instance n'a produit STOPPED ; aucune interruption n'est utilisée comme réfutation.

- Famille cyclique : **181 742 candidats de lignes**, tous contrôlés ; **2 770 suppressions justifiées** dans les traces.
- Famille C7⋊C3 : **250 943 candidats de lignes**, tous contrôlés ; **24 565 suppressions justifiées** ; douze designs ont déjà un domaine initial vide.
- Tous les autres cas sont réfutés par propagation de compatibilité, sans arbre de recherche global sur les 77 lignes.

Les premières campagnes ont pris environ 125 s et 245 s sur la machine de cette session, génération des domaines et contrôles compris. Ces durées ne sont pas des prédictions pour un autre matériel. La dernière version utilise des ensembles de bits compacts afin de limiter la mémoire des tables de compatibilité.

### Vérification indépendante au niveau du code

Un second énumérateur C++, écrit avec des branchements binaires et une propagation différente, a recalculé **1 283 domaines représentatifs**. Leur transport par des permutations explicites du design a contrôlé les domaines de **toutes les 20 867 lignes** des 271 instances. Les deux énumérateurs donnent exactement les mêmes ensembles de possibilités.

Un autre programme a ensuite relu chaque suppression en recalculant directement les intersections des ensembles. Un audit séparé a régénéré les catalogues à partir des 231 paires de points, sans utiliser les vecteurs de différences du générateur initial.

Le contrôle positif sur Paley(9), avec une coclique de Hoffman fixée, retrouve exactement quatre complétions étiquetées et conserve les vraies lignes du graphe. Les deux énumérateurs y concordent.

C'est une preuve assistée par énumération reproductible. Le code n'est pas formalisé dans Lean, et les traces ne sont pas des certificats DRAT.

## Deuxième résultat : une coclique de Hoffman peut subsister dans un SRG asymétrique

La conclusion « un asymétrique doit être cherché sans coclique de Hoffman » ne découle pas de la rigidité d'un design particulier de BvLS.

J'ai repris la matrice asymétrique du dossier Paley(25). Toutes les équations SRG sont vérifiées. Une preuve par invariants distingue successivement 5,16,22,25 classes de sommets, donc le groupe d'automorphismes est trivial. Pourtant ce graphe possède exactement **trois cocliques de Hoffman** de taille cinq.

Mieux : en complémentant la transformation précédente de Paley, on obtient deux SRG de paramètres (25,12,5,6), l'un isomorphe à Paley et l'autre asymétrique, qui conservent **la même coclique de Hoffman ET toutes ses incidences**. Les vingt sommets extérieurs ne changent leurs arêtes qu'entre eux.

Les deux matrices sont `data/paley25_complement.adj` et `data/paley_asymmetric25_complement.adj`. Leur coclique commune est {4,8,12,16,20}. Les données communes définissent un 2-(5,3,6), avec répétitions de blocs. L'égalité de tous les blocs et l'asymétrie du graphe final sont vérifiées en entiers.

Ce n'est pas un nouvel SRG : c'est un contre-exemple exact à une inférence méthodologique trop forte. Il montre qu'une structure de bord extrémale ne suffit pas, à elle seule, à forcer la symétrie.

## Lemme reliant vraiment rigidité et automorphismes

Le groupe d'automorphismes d'un design de bord agit sur l'ensemble de ses complétions. Le stabilisateur d'une complétion est exactement le groupe des automorphismes du graphe préservant cette coclique.

Donc :

    complétion unique + design ayant une symétrie
        ⇒ cette symétrie se prolonge au graphe.

Avec plusieurs complétions, la symétrie du design peut simplement les permuter, sans être une symétrie de chacune. C'est ce qui rend l'asymétrie possible malgré un bord très structuré.

## Mise à jour du dépôt : acquis, doublons et limites

La note 171 contient correctement YYᵀ=12I+2J. Le coefficient 18 indiqué dans une précédente réponse était faux.

La réduction à un design 2-(22,4,2) était déjà dans la note 94 ; le spectre 10¹,3³³,(−1)²¹,(−4)²² était déjà dans l'annexe de la note 104. Ils sont repris comme données acquises, pas annoncés comme nouveautés ici.

La rigidité BvLS décrite par Claude porte sur **son design précis**, pas sur tous les designs 2-(45,5,2). Les 1691 cocliques annoncées sont un minorant d'une énumération interrompue, pas une classification complète.

Au dernier état lu, les recherches α=22 sont découpées en sous-instances avec un registre de reprise : trois indiquées RUNNING, cinq PENDING et deux parents SPLIT. Cela ne donne encore ni SAT ni UNSAT pour le cas global. Le statut est celui du commit, pas un accès aux processus actuels de la machine de Claude.

## Portée finale

**Fermé ici :** les deux familles d'actions de designs définies dans COUVERTURE.md, sans symétrie imposée au graphe.

**Non fermé :** le sous-cas α=22 pour tous les designs, les graphes à 243 sommets asymétriques, C1 et les rangs encore ouverts.

Ces résultats retirent des familles exactes de bords à explorer. Ils ne mesurent pas un pourcentage du problème restant.

## Reproduction finale depuis un dossier neuf

La campagne entière a été régénérée sans copier les catalogues, domaines ou réfutations. Résultat : 271 designs exclus, 432685 candidats contrôlés, 27335 suppressions relues, en environ 344 secondes sur cette machine. Les 21138 fichiers de domaines et d’instances sont identiques octet par octet aux originaux. Les 271 certificats de suppression sont identiques hors champs de temps. Voir `reports/FRESH_REPRODUCTION.json`.
