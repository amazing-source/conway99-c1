# BvLS — reconstruction à bord libéré

Voir **RESULTATS.md** pour le théorème calculé et **THEORIE.md** pour sa justification.

Résultat principal : après libération de la région lointaine d'un triangle de BvLS et de deux des dix prismes de son voisinage, les seules complétions SRG(243,22,1,2) sont BvLS et son jumeau à isomorphisme près. 27 648 matrices étiquetées, deux classes; les 192 sommets libres ne sont soumis à aucune partition en fibres imposée.

## Vérifier les témoins et petits certificats

Python 3.10 ou ultérieur, bibliothèque standard seulement :

    python code/verify_bundle.py

Ce contrôle vérifie les matrices, les domaines archivés, les 26 obstructions de paires, les isomorphismes et les transports. Il ne remplace pas l'énumération pour la complétude.

## Reproduire toute la classification principale

Dépendances : Python 3.10 ou ultérieur, NumPy, g++ compatible C++17, en-têtes Boost pour les entiers de décompte. Aucun appel à un LLM ni service cloud.

    python code/reproduce.py --work /chemin/vers/un_dossier_qui_n_existe_pas

Le programme refuse d'écraser un dossier existant. Il génère BvLS, retrouve exactement le jumeau, énumère les domaines, les transporte, exécute deux recherches (avec et sans suppression des renommages), vérifie les témoins et la couverture.

Ajouter `--all-cases` pour les expériences complémentaires à 186 sommets. Le premier cas à 180 sommets est un contrôle du résultat déjà connu.

Les exécutables et caches locaux ne sont pas indispensables à la livraison : les sources sont fournies et sont recompilées. Les données `.npy` ne contiennent pas d'objets Python; aucun pickle n'est nécessaire.

## Intégration au dépôt

Voir COORDINATION.md et, dans l'archive de livraison, INTEGRATION.md. Aucun changement n'a été poussé au dépôt distant depuis cette session.

Les verdicts historiques incomplets sont conservés dans REGISTRE_ECHECS.md. Aucune nouvelle classe SRG ni résolution de l'asymétrie à 243 en général n'est revendiquée.
