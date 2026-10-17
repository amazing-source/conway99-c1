# Hoffman, asymétrie et Conway-99 — campagne du 11 octobre 2026

## Lire

- `RESULTATS.md` : résultats et portée exacte.
- `THEORIE.md` : équations de reconstruction, lemme de prolongement des symétries, contre-exemple de Paley, Gram entier.
- `COUVERTURE.md` : pourquoi les catalogues couvrent entièrement les actions de designs annoncées.
- `CERTIFICATION.md` : rôle des deux énumérateurs, transports et traces de suppressions.
- `COORDINATION.md` : état du dépôt lu, message à transmettre à Claude, absence de modification distante.
- `FAILURE_LEDGER_ADDITIONS.md` : familles désormais fermées et généralisations à ne pas réintroduire.
- `sources/SOURCES.json` : provenance et références.

## Deux résultats

1. Aucun SRG(99,14,1,2) avec une coclique de taille 22 ne peut avoir pour design de voisinages l'un des designs cycliques sur 22 points, ni un design portant une action régulière de groupe d'ordre 21 sur 21 points avec un point fixe. La preuve combine couverture par orbites et réfutations exactes, sans imposer de symétrie au graphe complété.
2. Un SRG asymétrique à 25 sommets peut conserver une coclique de Hoffman et même exactement les mêmes incidences de cette coclique que Paley. Les matrices et une preuve élémentaire d'asymétrie sont fournies.

Le cas général α=22, les graphes asymétriques à 243 et C1 ne sont pas résolus par ces résultats.

## Vérification complète des fichiers fournis

Environnement : Python 3.10 ou supérieur, compilateur C++17 (`g++` par défaut), Linux/WSL/macOS. Aucun paquet Python tiers, solveur SAT, compte cloud ou connexion réseau n'est requis.

Depuis la racine extraite :

```sh
python3 code/check_all.py
```

Le programme compile les deux énumérateurs, régénère les deux catalogues par une seconde méthode, réénumère indépendamment 1283 domaines représentatifs et transporte les résultats sur les 20867 lignes, contrôle toutes les suppressions et exécute les contrôles positifs.

Il vérifie aussi les deux matrices au bord de Hoffman commun et l'asymétrie du témoin par des invariants qui distinguent les 25 sommets.

Les rapports temporaires du contrôle ne remplacent pas les journaux archivés. Ne pas utiliser `python -O`, qui désactive les assertions.

## Refaire la campagne depuis zéro

```sh
python3 code/reproduce.py --work ../hoffman_reproduction_neuve
```

Le répertoire cible doit ne pas exister. Le pilote ne copie aucun design, aucun domaine de lignes ni aucune réfutation du dossier d'origine : il les régénère. Il ne copie que le code et les petites matrices nécessaires au contre-exemple de Paley. Tous les calculs sont séquentiels ; aucun appel de modèle n'est effectué.

Une limite atteinte ou une erreur de vérification provoque un arrêt explicite, jamais une conclusion d'inexistence.

## Données

- `data/cyclic_designs22.json` : 72 designs normalisés admissibles aux premiers filtres.
- `data/one_rotational_designs22.json` : 199 designs normalisés pour l'action non abélienne.
- `data/cyc*.inst`, `data/frob*.inst` : incidences et quotas de reconstruction.
- `data/cyc*_*.rows`, `data/frob*_*.rows` : domaines exhaustifs des voisinages.
- `reports/*.certificate.json` : suites de suppressions justifiées par absence de partenaire.
- `reports/verification_cyclic.json`, `reports/verification_one_rotational.json` : contrôles indépendants effectivement terminés.
- `reports/catalogues_verified.json` : comparaison des catalogues régénérés.
- `data/paley*_complement.adj` : matrice source et matrice asymétrique au même bord de Hoffman.

Les identifiants commencent à zéro. Les noms « 72 » et « 199 » ne désignent pas des classes d'isomorphisme : voir COUVERTURE.md.

`SHA256SUMS` enregistre les empreintes des fichiers livrés. Les binaires sont compilés localement ; ils ne sont pas nécessaires dans l'archive.
