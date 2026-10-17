# Comment la preuve informatique est contrôlée

## Couche 1 — Couverture mathématique

COUVERTURE.md démontre que chaque design concerné, après un renommage autorisé, appartient à l'une des sélections d'orbites énumérées. Un stabilisateur est imposé au design de bord, jamais à la complétion du graphe.

## Couche 2 — Deux générateurs de catalogue

Le premier utilise les classes de différences dans les groupes. `verify_catalogues.py` développe explicitement toutes les orbites, puis utilise les 231 comptes de paires de points. Les deux listes complètes sont comparées comme ensembles de blocs étiquetés.

## Couche 3 — Deux énumérateurs de lignes

`rows22.cpp` choisit un point dont le quota n'est pas rempli, puis choisit ensemble tous les blocs encore nécessaires sur ce point. Tout voisinage valable apparaît dans une des branches : son ensemble de blocs incident au point choisi est une des combinaisons parcourues. Ces choix sont disjoints. Les quotas, incompatibilités et cardinalités ne suppriment que des branches impossibles.

`rows22_independent.cpp` procède différemment : saturation des points dont tous les candidats sont nécessaires, puis branchement binaire « inclure / exclure » sur un seul bloc. Il ne lit pas les réponses du premier énumérateur.

Les deux codes manipulent des entiers, des ensembles de bits et des cardinalités. Les horloges ne servent qu'aux limites : une interruption donne STOPPED, qui fait échouer le contrôle. Tous les domaines sauvegardés et réénumérés de cette campagne sont exhaustifs.

Les 1283 réénumérations concernent un représentant de chaque orbite de blocs (quatre par design cyclique, cinq par design C7⋊C3). Les permutations des points sont développées en permutations de blocs et contrôlent ensuite les ensembles complets de candidats des 20867 lignes. On ne contraint jamais les CHOIX de lignes à être images les uns des autres.

## Couche 4 — Relecture indépendante des suppressions

Le programme `verify_campaign.py` vérifie chaque candidat, puis chaque suppression (i,a,j) par le calcul direct : pour aucun candidat encore vivant b de j, les équations de symétrie et de voisins communs ne sont satisfaites. Une ligne vide conclut.

Cette étape ne suppose pas qu'une table de compatibilité pré-calculée soit correcte. Elle la recalcule mathématiquement au moment de la vérification.

## Couche 5 — Contrôle positif

`positive_control.py` construit la grille3×3, choisit une coclique de Hoffman de trois sommets, puis soumet ses incidences aux deux énumérateurs. Les vraies lignes sont conservées et l'assemblage complet donne exactement quatre matrices SRG étiquetées. Ce contrôle ne remplace pas les preuves de couverture, mais détecte une contradiction artificielle dans le moteur.

## Statut de confiance

La preuve est assistée par programmes exhaustifs et contrôles séparés, tous exécutés ici. Elle n'est pas formalisée dans un assistant de preuve et aucun certificat DRAT n'est revendiqué. Le code et les arguments de couverture sont les éléments à relire pour une validation externe.

Les matrices de Paley et leurs certificats sont contrôlés avec des programmes Python seuls. La preuve d'asymétrie ne dépend pas d'un logiciel annonçant simplement |Aut|=1.

Les deux codes ont été écrits dans cette session. Leur indépendance algorithmique est un contrôle logiciel, pas une relecture humaine externe. La reproduction finale depuis un dossier vide est consignée dans `reports/FRESH_REPRODUCTION.json`.
