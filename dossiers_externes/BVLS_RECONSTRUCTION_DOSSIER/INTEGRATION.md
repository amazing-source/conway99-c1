# Intégration non destructive au dépôt C1

Le dépôt distant n’a pas été modifié. Les outils disponibles ici exposaient les lectures GitHub, pas la création de commits. La contribution est livrée prête à appliquer sur une branche distincte, sans modifier les fichiers de l’autre session.

## Option Git : patch additif

Depuis votre clone authentifié, créer un worktree distinct :

```sh
git fetch origin
git worktree add -b astra/bvls-boundary-2026-10-11 ../bvls-boundary origin/claude/v7-simultaneous
git -C ../bvls-boundary am /chemin/absolu/BVLS_RECONSTRUCTION_DOSSIER/integration/BVLS_BOUNDARY.patch
```

Le patch crée uniquement :

- `notes/ASTRA_2026_10_11_BVLS_BOUNDARY.md`
- `code/astra_bvls_boundary_2026_10_11/` (dossier autonome avec code, données et rapports).

Il ne change ni les notes numérotées, ni les matrices existantes, ni `code/asym243/`. Après contrôle local, cette branche peut être poussée avec `git push -u origin astra/bvls-boundary-2026-10-11`. Aucun push n’a été fait par cette session.

## Option sans patch

`integration/repository_overlay.zip` contient exactement les deux chemins additifs, à extraire dans le worktree. Ne pas appliquer les deux méthodes l’une après l’autre.

## Contrôles effectués sur la livraison

Le patch a été appliqué dans un dépôt local neuf, puis chaque fichier a été comparé octet par octet à la superposition. Le manifeste `SHA256SUMS` porte sur le dossier scientifique autonome; les empreintes de l’intégration sont dans `integration/SHA256SUMS`.
