# Dossiers externes (ChatGPT) et pièces transmises par Dilan

Les dossiers sont arrivés en zip dans la session web des 11–12 octobre 2026. Ils avaient été lus et intégrés dans les
notes 171–178, mais n'avaient pas été versés au dépôt. Ils sont maintenant ici.

**Statut.** Ce sont des résultats externes, *rapportés*, sauf mention contraire. Chaque dossier a son propre
vérificateur. Ce qui a été revérifié ici est indiqué dans la colonne « Intégré dans ».

## Contenu

| Dossier | Reçu | Sujet | Intégré dans |
|---|---|---|---|
| `PALEY_ASYMETRIE_DOSSIER/` | 11/10 | Paley(25) : on garde un K₅ et ses attaches et on reconstruit les 20 autres sommets. On obtient les 15 classes srg(25,12,5,6), dont les 2 asymétriques (n° 7 et 13 du fichier McKay). Témoin explicite à 37+37 arêtes de Paley. | note 171 §1–2 ; rapport « Asymétrie des graphes fortement réguliers » |
| `BVLS_RECONSTRUCTION_DOSSIER/` | 11/10 | BvLS (243) : on libère la région lointaine d'un triangle et 2 prismes, soit 192 sommets libres. Seules complétions : BvLS et son jumeau (27 648 matrices = 2 classes). | note 171 §1–2 |
| `HOFFMAN_UPDATE_20261011/` (zip `HOFFMAN_REPONSES_20261011`) | 11/10 | α = 22 à 99. Les 72 designs cycliques et les 199 designs « one-rotational » (ordre 21 avec point fixe) sont exclus. Un srg(25) asymétrique a le même bord de Hoffman que Paley. Q = 9I − 3D − N + J. | note 171 §7 ; note 172 (scripts `code/asym243/hoffman/lattice/`) |
| `C1_K7_RESULTATS_PARTIELS/` | 12/10 | K7 partiel. Théorème 1 : Γ_c ∪ M_c est connexe (laplacien Q_W = 6I − 3M − G), revérifié ici. Rang 13 / Schur rang 9. Type ternaire (7,15,0) : n_ef ≤ 3. Défauts = normes 4/6/8 des w_e + w_f. **Pas** de preuve de K7, **pas** de contre-exemple. | note 173 §6 |
| `../code/code7_mots_binaires/` (zip `C1_CODE7_MOTS_BINAIRES`) | 12/10 | Les mots binaires de ker₇(A+4I) ont un poids 0, 63 ou 77. Le poids 77 équivaut à une coclique de Hoffman 22. Revérifié ici. | note 178 |
| `C3_preuve/proof_c3_english.pdf` | 12/10 | Preuve C3 (ordre 3), version anglaise envoyée en relecture. | (branche C3, hors C1) |

Les zips d'origine, complets et inchangés, sont dans `archives/` :

```
394dd2ad0cb4662a16ec0730208c28edba22dee2d1a46baf9cfc050afaf5b48d  HOFFMAN_REPONSES_20261011.zip
e633231421cd6e6550c247aa38582f767db81a7744f5888de4c35edc9b08e724  BVLS_RECONSTRUCTION_DOSSIER.zip
8610fc56f6916a1fde1f05256a5457d79570e7d03d4d4824531b115e4ecd6539  PALEY_ASYMETRIE_DOSSIER.zip
d40b46d71e01bf61276b12e3086bf4df95bcc659af1d5ff6878fff26996d45d4  C1_K7_RESULTATS_PARTIELS.zip
8a979755b9455cdbf5c7bf04752635d6082b832bd4c8b26059cba5817933b5ef  C1_CODE7_MOTS_BINAIRES.zip
```

## Données volumineuses : seulement dans les zips

Deux dossiers ne sont pas entièrement déballés, pour ne pas mettre environ 22 000 petits fichiers dans l'arbre :

- **BvLS.** Les dossiers `data/` (17 Mo : domaines `.rows`, `.npy`) et `integration/` (15 Mo, dont
  `repository_overlay.zip` et `BVLS_BOUNDARY.patch`) ne sont pas déballés.
- **Hoffman.** Le dossier `data/` n'est pas déballé : 84 Mo, environ 21 000 fichiers (`cyc*.inst`, `frob*.inst`,
  `*.rows`, `cyclic_designs22.json`, `one_rotational_designs22.json`, `paley*_complement.adj`).

Les `SHA256SUMS` de chaque dossier passent sur toutes les entrées présentes (`sha256sum -c --ignore-missing`).

Pour récupérer ces données, par exemple les `.inst` lus par `lamc.py` et `r3.py` (note 172) :

```sh
mkdir -p /tmp/hoffman && unzip -q dossiers_externes/archives/HOFFMAN_REPONSES_20261011.zip \
  'HOFFMAN_UPDATE_20261011/data/*' -d /tmp/hoffman
mkdir -p /tmp/bvls && unzip -q dossiers_externes/archives/BVLS_RECONSTRUCTION_DOSSIER.zip \
  'BVLS_RECONSTRUCTION_DOSSIER/data/*' -d /tmp/bvls
```

`check_all.py` (Hoffman) et `verify_bundle.py` (BvLS) ont besoin de `data/`. Il faut donc les lancer depuis une
extraction complète du zip, pas depuis la copie partielle ci-dessus.

## Manquants

- **`C1_HOFFMAN_ARITHMETIQUE.zip` n'a jamais été transmis à cette session.** Dilan n'en a collé que le résumé texte
  (classification ternaire : dim ker_F3 Yᵀ ≤ 2, six types, a = 1 + 2t, h = 22 − w, rang₇(A+4I) = 45 − b − 2η,
  cocliques de 15 points, 12 réseaux). Ce résumé est consigné dans la note 172 §5. Le dossier lui-même est à ajouter
  ici, sous `archives/`, s'il est retrouvé.
