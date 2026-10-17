# Failure ledger — campagne Paley du 11 octobre 2026

Ce registre est **local à cette campagne**. Il ne remplace pas l’atlas complet de C1.
Il distingue le mécanisme essayé, la portée de l’échec et le résultat conservé.

## P-01 — Comparer à nouveau seulement les petits motifs

**Antériorité interne :** l’ancienne archive `PAULUS_ASYMMETRY_EXPERIMENT.zip` compare déjà
les quinze graphes, leurs groupes, leurs motifs et leurs graphes lointains.

**Décision :** ne pas présenter une répétition de ces statistiques comme un résultat de construction.
La campagne présente reconstruit effectivement les graphes. Les petits comptes de cliques ne
servent que de certificats intrinsèques d’asymétrie ou d’accélérateurs d’isomorphisme.

## P-02 — Sortir de Paley par changements standards de Godsil–McKay à une cellule

**Statut : CLOSED pour ce mécanisme sur Paley(25).**

Tous les sous-ensembles propres de taille paire 4 à 24 ont été testés. Cinquante sont
admissibles, tous de taille douze ; chaque résultat est isomorphe à Paley.
La classe est donc isolée pour toute succession de ces changements.

**Ce qui n’est pas exclu :** changements à plusieurs cellules, autres opérations
orthogonales, reconstructions de bord.
**Réouverture :** changer effectivement de mécanisme, pas seulement de graine.
La reconstruction \(K_5\) réussit là où ce mécanisme échoue.

## P-03 — Conserver une partition complète en cinq cliques \(K_5\)

**Statut : CLOSED comme voie vers l’asymétrie, pour SRG(25,12,5,6).**

Le recensement des partitions sur les quinze classes donne trois partitions pour chacun des
deux graphes latins, aucune pour les autres. Les deux seuls résultats possibles ont groupes
d’ordres 72 et 600.

**Résultat conservé :** une seule clique et son bord exact suffisent au contraire à accéder
aux quinze classes.
**Ne pas transférer sans preuve :** les asymétriques à 243 devraient nécessairement perdre
toute partition en grilles. Cette campagne ne l’établit pas.

## P-04 — Reconstruction derrière deux cliques disjointes de Paley

**Statut : COMPLET, deux classes symétriques seulement.**

Pour le bord explicite \(S_{10}\) du dossier : six complétions étiquetées, deux classes.
Ce n’est pas une impossibilité de modifier Paley globalement. Les bords plus petits de la
même échelle atteignent douze puis quinze classes, dont les asymétriques.

**Réouverture :** libérer les incidences de bord, et non faire tourner plus longtemps le
même problème complètement énuméré.

## P-05 — Seuil universel à six ou sept sommets

**Statut : NON DÉMONTRÉ.**

L’échelle du rapport porte sur des ensembles emboîtés précis. Elle ne démontre pas qu’un
bord de sept sommets quelconque interdit l’asymétrie, ni que six est un seuil universel.
La minimalité de 74 changements est également relative au bord \(K_5\) fixé.

## P-06 — Héritage erroné de signatures dans un sous-graphe

**Statut : BUG CORRIGÉ pendant le diagnostic.**

Une première routine réutilisait des attributs de couleurs hérités du graphe entier lors du
passage au sous-graphe induit. Ces couleurs n’étaient pas nécessairement intrinsèques au
sous-graphe et pouvaient sous-estimer son groupe.

**Correction :** le cache dépend désormais de l’ensemble exact des sommets et des arêtes.
Les groupes des noyaux et des régions restantes ont été comparés à une énumération
non colorée. Le noyau du témoin livré a bien deux automorphismes, pas un.
L’involution restante est détruite par les attaches.

Les graphes du recensement principal étaient construits à neuf ; ce défaut ne change pas
leur validité ni leur classification. Le vérificateur autonome du noyau ne réutilise pas
cette routine.

## P-07 — Supprimer les symétries de recherche contre imposer des symétries au graphe

**Statut : distinction essentielle, contrôlée.**

Les échanges utilisés dans la recherche sont ceux du bord partiel. Ils ne sont pas ajoutés
comme équations d’automorphisme de la matrice finale. Les poids rétablissent le nombre
d’étiquetages. Les contrôles avec/sans échanges concordent.

Un code « invariant par un sous-groupe » et un code « quotientant les renommages des entrées »
ne cherchent pas la même famille. Ne pas confondre les deux.

## P-08 — Nouveauté des graphes

**Statut : KNOWN EXAMPLES.**

Les deux SRG asymétriques et la liste des quinze existent dans la classification de 1973.
Aucun nouveau graphe de paramètres 25 ni nouvelle priorité bibliographique n’est revendiqué.
Le résultat de la session est un laboratoire constructif achevé, des certificats explicites,
et un diagnostic de la structure qui bloquait les modèles plus restreints.

## P-09 — Relancer les pistes avant de lire les corrections de jauge

**Source :** commit `5f3cea4defff360d1b77445be44e047e9f094151`, note 167 du dépôt C1.
Fixer tous les recollements d’un arbre à l’identité n’est pas une jauge libre lorsque les
fibres portent une grille déjà étiquetée. Le dépôt a corrigé cette erreur avec des contrôles positifs.

La reconstruction Paley conserve explicitement les matrices de bord et ne fixe pas des
permutations d’attache non justifiées.
