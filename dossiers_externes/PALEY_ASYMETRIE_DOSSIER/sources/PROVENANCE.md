# Provenance, périmètre et antériorité

## Données publiques

Catalogue utilisé après la construction pour reconnaître les graphes :
Brendan D. McKay, *Combinatorial Data*, fichier `sr251256.g6`.

- https://users.cecs.anu.edu.au/~bdm/data/graphs.html
- https://users.cecs.anu.edu.au/~bdm/data/sr251256.g6
- SHA-256 du fichier livré : `f55f86eb48cd61c3315c62341cc3a8c59289c58504edb3ab859d7ef2068b9aa4`.
- Quinze entrées graph6, toutes contrôlées comme SRG(25,12,5,6).

Le fichier est repris de l’archive de l’expérience Paulus précédente fournie dans cette
conversation ; son contenu est comparé à la ressource publique identifiée ci-dessus.
La page de licence générale de McKay annonce CC BY 4.0 pour ses fichiers de données,
sauf attribution différente indiquée :
https://users.cecs.anu.edu.au/~bdm/data/ .
Les pages HTML ne sont pas redistribuées dans ce dossier.

Antériorité de la classification et description des graphes :
A. E. Brouwer, *Paulus–Rozenfeld graphs*,
https://aeb.win.tue.nl/graphs/Paulus.html .

Références historiques citées par cette page :
A. J. L. Paulus, *Conference matrices and graphs of order 26*, rapport WSK 73/06, 1973 ;
M. Z. Rozenfeld, *The construction and properties of certain classes of strongly regular graphs*,
Uspehi Mat. Nauk 28 (1973), 197–198.

Cette page distingue quinze classes à 25 sommets, dont deux asymétriques, et deux classes
principales de carrés latins d’ordre cinq. Sa colonne « max cliques » compte des cliques
maximales, et non toutes les occurrences de \(K_4\). L’ancienne confusion de ces deux
quantités ne doit pas être réintroduite.

Les identifiants du dossier suivent l’ordre du fichier McKay ; ils ne sont pas les P25.xx de Brouwer.

## Source de la motivation à 243 : GitHub privé de l’utilisateur

Dépôt : `amazing-source/conway99-c1`, branche `claude/v7-simultaneous`.

Révisions consultées pour la campagne :

- `8a8e986ccc5b8081de74ed7481ec942b403bbc8f` : quatrième SRG243, re-voltage et tableau des familles.
- `24a29b6f0cc2419f17f14fd976da5ee5c4ea2ea9` : note 166, partitions équitables.
- `356cd0e419ec1ab727ce2d66124c670669410d60` : entrée des graphes réguliers d’ordre neuf.
- `58b7ad2da32fda86161a4b9b5f5c602122e393a4` : note 167, mécanismes de recollement ; identifié dans l’historique.
- `5f3cea4defff360d1b77445be44e047e9f094151` : correction de jauge, code et contrôles positifs.
- **`1bbc7fdc5dde795d944bad0f2d9ae0af17e27c24`** : pointe observée au dernier relevé, journaux de recollement,
  datée du 11 octobre 2026 à 13:15:14 UTC.

Sources exactes :
https://github.com/amazing-source/conway99-c1/blob/356cd0e419ec1ab727ce2d66124c670669410d60/notes/165_SRG243_REVETEMENTS_ET_SYMETRIE.md
https://github.com/amazing-source/conway99-c1/commit/24a29b6f0cc2419f17f14fd976da5ee5c4ea2ea9
https://github.com/amazing-source/conway99-c1/commit/5f3cea4defff360d1b77445be44e047e9f094151
https://github.com/amazing-source/conway99-c1/commit/1bbc7fdc5dde795d944bad0f2d9ae0af17e27c24

Les notes 165 et 166, les différences pertinentes et les nouveaux journaux ont servi à
identifier ce qui avait déjà été essayé. Ce dossier n’est pas un audit exhaustif de tous
les fichiers historiques de C1, ni une certification indépendante des quatre graphes243.
Il ne recopie pas leurs données privées.

La pointe est un instantané, pas une promesse que la branche ne changera plus.
Aucun push, modification de visibilité ou lancement distant n’a été effectué.

## Ce qui provient de cette campagne

- Génération de Paley(25) en coordonnées F5² et vérification séparée sur F25.
- Reconstruction exhaustive avec un \(K_5\) et toutes ses incidences fixés.
- Restauration pondérée des étiquetages, classement des 3 983 représentants.
- Recensement des changements standards GM et des partitions en \(K_5\).
- Reconstruction de la petite échelle de bords fixés.
- Témoin à 37 arêtes supprimées et 37 ajoutées, minimum dans le bord fixé.
- Deux certificats élémentaires d’asymétrie et description noyau/attaches.
- Contrôle Paley(9), répétition complète et tests négatifs.

Il s’agit de calculs exacts et de preuves explicitées ici, **pas d’une validation humaine externe**.
La nouveauté bibliographique éventuelle du protocole de reconstruction n’a pas été revendiquée.
