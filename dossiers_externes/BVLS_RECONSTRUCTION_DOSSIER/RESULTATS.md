# BvLS : reconstruction sans fibres imposées, puis classification exacte

11 octobre 2026 — recherche issue de l'expérience Paley(25).

## Résultat principal

Fixons un triangle T du BvLS classique. Ses 60 voisins extérieurs induisent dix prismes triangulaires disjoints. Soit U la réunion de deux de ces prismes (12 sommets), et F la réunion des 180 sommets lointains de T avec U.

**Classification informatique exacte.** Parmi tous les graphes simples fortement réguliers de paramètres (243,22,1,2) qui coïncident avec BvLS sur chaque paire ayant au moins une extrémité hors de F, il y a exactement deux classes d'isomorphisme : BvLS et son jumeau de la note 159 / du manuscrit `srg243_second`.

Dans les étiquettes fixées du dossier : **27 648 matrices**, soit **13 824 copies de chaque classe**. Les correspondances avec les deux graphes de référence sont explicites. Le facteur 13 824 vaut `(4!)^3`.

Cela vaut pour **tout triangle T et tout choix de deux des dix prismes**. La couverture est vérifiée par des automorphismes affines explicites : 891 triangles et 45 paires de prismes pour chaque triangle. Ces 40 095 choix sont des présentations de problèmes de reconstruction, pas 40 095 graphes ou sous-cas indépendants de Conway.

**Corollaire.** Dans cette famille de reconstructions, chaque complétion possède un automorphisme d'ordre trois. Il n'existe donc pas de complétion asymétrique. Cette symétrie n'est pas imposée au modèle : elle résulte de la classification et est donnée explicitement sur les témoins finaux.

**Autre lecture.** Dans une reconstruction qui conserve toutes les incidences du triangle T, pour produire depuis BvLS un SRG non isomorphe à BvLS et à son jumeau, les sommets modifiés dans le voisinage extérieur de T ne peuvent pas tous être contenus dans seulement deux de ses dix prismes. La région lointaine de 180 sommets était pourtant entièrement libre. Cette conclusion concerne ce cadre de bord fixé; elle ne borne pas arbitrairement toutes les transformations du graphe.

## Comparaison des expériences effectivement terminées

| Origine et région libre | Sommets du bord dont toutes les incidences sont fixées | Sommets libres | Matrices étiquetées | Classes finales |
|---|---:|---:|---:|---|
| BvLS, région lointaine de T | 63 | 180 | 2 | BvLS, jumeau — contrôle connu |
| BvLS, lointain + un prisme | 57 | 186 | 16 | BvLS, jumeau |
| BvLS, lointain + deux prismes | 51 | 192 | 27 648 | BvLS, jumeau |
| BvLS, lointain + trois paires mates dans une même couche de N(T) | 57 | 186 | 2 | BvLS, jumeau |
| Gamma3 du dépôt, lointain du triangle (0,1,2) + le prisme (3,4,5,6,7,8) | 57 | 186 | 8 | Gamma3 seulement |

Le résultat Gamma3 porte sur la région étiquetée indiquée. Il n'est pas annoncé pour toutes ses orbites de triangles. Les isomorphismes des huit matrices avec Gamma3 sont vérifiés, et non simplement déduits du même nombre de grilles.

Pour les trois paires mates dans une couche de BvLS, 360 transports explicites couvrent les 3 couches et les choix de 3 paires parmi 10. Ces trois paires ne sont pas trois prismes complets.

## Le calcul n'est pas un modèle de revêtement caché

Les inconnues sont **toutes** les adjacences entre les sommets libres, soit 18 336 paires dans le cas principal à 192 sommets. Aucun étalement, aucune partition en grilles, aucune monodromie, aucune invariance par un groupe et aucune structure affine n'est imposée au graphe cherché.

Les automorphismes de BvLS servent uniquement à transporter des problèmes déjà équivalents et à éviter des renommages du même état partiel. Une seconde recherche **sans aucune réduction de renommages** retrouve exactement les mêmes 27 648 matrices.

## Comment les 192 lignes se réduisent

Les équations entre le bord fixe et une ligne libre donnent un domaine fini de voisinages binaires. Pour les cinq orbites de lignes du cas principal :

| Représentant local | Nombre de lignes dans l'orbite | Taille exacte du domaine de chaque ligne |
|---:|---:|---:|
| 0 | 12 | 3 264 |
| 9 | 12 | 252 |
| 24 | 48 | 32 |
| 27 | 96 | 116 |
| 36 | 24 | 28 |

Les cinq domaines représentatifs sont énumérés entièrement, puis transportés par des permutations explicitement vérifiées.

Un détail particulièrement court est conservé dans `reports/prism2_certificate.json` : pour la ligne du sommet global 42, **26 des 28 voisinages candidats n'ont aucun partenaire possible dans au moins une autre ligne**. Chacun a son témoin d'incompatibilité. Les deux candidats restants conduisent aux deux classes finales.

La recherche avec réduction partielle des renommages visite 385 nœuds et deux feuilles canoniques. Sans cette réduction, elle visite 1 562 240 nœuds et 27 648 feuilles. Les identités SRG finales sont vérifiées en entiers.

Mesures initiales de cette session : environ 45 s pour les cinq domaines représentatifs; 0,023 s pour leur assemblage avec réduction de renommages; environ 18 s pour le recensement sans réduction. Ces durées ne sont pas des estimations pour une recherche sur tous les SRG à 243 sommets.

## Ce qui est nouveau ici et ce qui ne l'est pas

La région lointaine seule donnant BvLS et son jumeau était déjà connue et sert de contrôle positif. L'extension traitée ici libère douze sommets du bord en plus et reste complètement classifiable sans hypothèse de fibres. Cette famille ne figure pas dans les notes 165–170 consultées. Aucune revendication de priorité bibliographique générale n'est faite.

Aucun cinquième SRG ni aucun SRG asymétrique n'a été construit. Le résultat est une rigidité **prouvée par un recensement terminé dans une famille plus large**, pas l'échec d'un solveur au bout d'un délai. Il indique précisément une liberté supplémentaire qui reste insuffisante.

Cela ne ferme pas les recherches de l'autre session sur S3, les nouveaux squelettes ou les graphes sans partition particulière. Ces expériences n'ont pas été relancées ici.

## Fichiers et contrôle

- `THEORIE.md` : équivalence du modèle, preuve de couverture et des réductions de renommage.
- `code/verify_bundle.py` : vérification entière des témoins, des isomorphismes, des domaines présents et des 26 petits certificats.
- `code/reproduce.py` : reconstruction des domaines et réexécution du recensement, avec une seconde passe sans quotient.
- `reports/prism2_certificate.json` : isomorphismes, automorphismes d'ordre trois et obstructions de paires.
- `reports/coverage.json` : transports de triangles et de paires de prismes.
- `REGISTRE_ECHECS.md` : étapes connues, limites mesurées et recherches incomplètes.
- `COORDINATION.md` : références figées et périmètre de la contribution.

La chaîne n'est pas une formalisation Lean ni un certificat DRAT. La complétude repose sur les petits programmes exhaustifs joints, leur justification et les recensements recoupés; le vérificateur de témoins ne prétend pas à lui seul prouver la complétude.

## Répétition depuis un dossier neuf

`code/reproduce.py` a été exécuté de bout en bout dans `/mnt/data/BVLS_REPLAY_FINAL`, à partir des sources et du seul fichier graph6 Gamma3. Les cinq domaines représentatifs ont été régénérés, le jumeau retrouvé avec son empreinte originale et les deux recensements terminés. Résultats répétés : 385 nœuds / 2 représentants pondérés; 1 562 240 nœuds / 27 648 feuilles sans quotient. Les isomorphismes, les transports et les 26 obstructions ont ensuite été contrôlés. Les journaux sont dans `reports/reproduction_fresh/`. Le vérificateur rapide final contrôle aussi les automorphismes explicites d'ordre trois.
