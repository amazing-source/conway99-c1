# Coût du calcul du rang 37 : mesures (session du PC labo, 09/10/2026, mis à jour à 16:35 UTC)

Demande de l'utilisateur : « coupe le coût du calcul ». Objet : le test d'une étoile par boule de droite au rang 37
(modèle de la session portable, `c1_rank37_girth5_lines/NOTE.md` de `conway99-c2-aws`, non audité par un tiers), pour
les boules **connexes, sans prisme, sans torsion**. Rien ici n'exclut un rang ; ce sont des mesures de coût.

## Résultat

Un cœur de ce PC (Ryzen 7 7800X3D), boules aléatoires de la classe, sommet d'étoile ayant le plus de zéros dans K.

| version | nœuds (étoiles partielles) | temps par boule testée | gain |
|---|---|---|---|
| `star37.c` : portage de la recherche de la session portable | 31 000 | 60 à 65 ms | 1 |
| `star37b.c` : tables (première étape, 15:35 UTC) | 23 000 | 32 ms | 2 |
| `star37d.c`, conditions entières seules (`real 0`) | 84 000 (ordre fixe des emplacements) | **2,2 ms** | 28 |
| `star37d.c`, avec les filtres réels (`real 1`) | 23 000 | **1,26 ms** | 48 |

Détail de `star37d` (2000 boules testées, graine 41, `OUTPUT_star37d_seed41_*.txt`) : inverse modulo 7 : 0,004 ms par
boule valide ; tables et candidats 0,05 ms (0,08 avec les réels) ; recherche 2,09 ms (1,15 avec les réels). Aucune des
2000 boules n'a d'étoile ; la recherche meurt au niveau 6 ou 7.

## Ce qui a changé

1. **Dix emplacements, ordre fixe.** Une étoile prend exactement un candidat par point de la couche de U (dix points de
   demande 1). Les emplacements sont pris du plus petit au plus grand.
2. **Lignes de compatibilité en bits, à la demande.** Pour un candidat m et un emplacement b, deux ensembles de 512
   bits : candidats de b compatibles avec m sans arête, ou avec arête. Une ligne se calcule par paquets de 64 candidats
   (AVX-512 VBMI : la relation est la somme de trois tables de 64 octets) : environ 60 ns la ligne, 4000 lignes par
   boule au lieu de 3,4 millions de tests de paires.
3. **Ensembles vivants par opérations sur les mots.** L'ensemble des candidats vivants d'un emplacement pour une étoile
   partielle se déduit de celui du parent par quelques opérations de 512 bits (partenaires, couverture) ; un
   emplacement n'est traité que lorsque la recherche l'atteint.
4. **Inverse modulo 7 et candidats par paquets de 64 octets** : 0,1 ms → 0,004 ms et 0,25 ms → 0,05 ms.
5. **Filtres réels (option), valables à tout rang.** Complément de Schur de 7 E_(-4) = 3I - A + J/9 par rapport aux 36
   points proches : chaque sommet lointain f d'ombre n_f a un vecteur résiduel rho_f de R^8, avec
   |rho_f|^2 = 37/12 - n_f^T H^+ n_f et <rho_f, rho_g> = 1/12 - A_fg - n_f^T H^+ n_g (H^+ pseudo-inverse du laplacien
   de la boule). C'est l'identité réelle de la session portable (NOTE 17.57, point 2), retrouvée ici indépendamment.
   Utilisé : norme >= 0 (garde 89 % des candidats), mineurs 2 x 2 (gardent 79 % des paires sans arête et 50 % des paires
   avec arête compatibles modulo 7), déterminant de la matrice de Gram de l'étoile partielle (tailles 3, 4, 5).
   Effet : 84 000 → 23 000 nœuds. Arithmétique flottante avec tolérances (1e-9 à 1e-6) : un rejet demande une violation
   supérieure à la tolérance.

Essayé et abandonné : ordre des emplacements choisi pour chaque premier membre (25 % de nœuds en moins, mais plus de
lignes : plus lent, option `order 1`) ; choix du sommet d'étoile par le nombre de candidats ou par le produit des trois
plus petits emplacements (10 % de mieux que « le plus de zéros », pour 36 calculs de candidats : ne paie pas).

## Contrôles (tous à 0 écart)

* Mode `check` : sur chaque boule, inverse rapide contre Gauss-Jordan ordinaire ; liste des candidats contre celle de
  la recherche de référence (mêmes ombres, même ordre) ; verdict de la recherche de référence de `star37.c` ; nombres
  d'étoiles partielles cohérentes à chaque profondeur recomptés par force brute à partir des formules du modèle
  (relation recalculée depuis Gm, déterminants par élimination de Gauss). 431 boules en tout sur la version finale et
  celle qui la précède (profondeurs 4 à 6, avec et sans filtres réels, deux choix de U, deux ordres).
* Version sans instruction vectorielle (`-DSCALAR`, mêmes formules en C ordinaire) : mêmes comptes que la version
  vectorielle sur 200 boules, et 0 écart en mode `check` sur 63 boules.
* **Contrôle positif** (mode `plant`) : dans chaque boule on choisit une étoile combinatoire (couverture, points
  communs, appariement des huit membres non sommets) et on déclare ses 45 paires compatibles ; la recherche rapide la
  retrouve dans 120 boules sur 120, avec les mêmes comptes que la référence à toutes les profondeurs jusqu'à 10 et le
  même nombre d'étoiles complètes. C'est le seul contrôle qui exerce l'acceptation finale : sur les boules réelles
  aucune étoile n'existe.

## Ce que cela donne

Tirage (66 283 tirés, graine 41) : 7,2 % des boules étiquetées sont dans la classe ; avec la masse (11!!)^3/6 = 1,87e11
cela fait environ 1,4e10 types. Parmi les valides : 14,7 % ont de la torsion, 43,2 % un discriminant résidu (éliminées
sans recherche, L23 de Codex), 42,1 % sont à tester, soit environ 6e9 tests d'étoile.

| périmètre | tests | à 60 ms (départ) | à 2,2 ms (entier) | à 1,26 ms (avec réels) |
|---|---|---|---|---|
| connexes sans prisme, sans torsion | 6e9 | 11 années-cœur | **150 jours-cœur** | **90 jours-cœur** |
| extrapolation à toute la masse (1,87e11), même coût par boule supposé | 8e10 | 150 années-cœur | 5,6 années-cœur | 3,2 années-cœur |

Ce PC a 8 cœurs (16 fils) : avec la limite de 80 % il fournit environ 7 cœurs, pas 12 (ma note précédente disait
« une année-cœur par mois », c'était trop). Première ligne : environ 3 semaines de ce PC en version entière, 2 semaines
avec les filtres réels. Deuxième ligne : 6 à 10 mois de ce PC, ou de l'ordre du millier de dollars de machines louées
(ordre de grandeur non vérifié, aucun devis).

## Ce qui manque pour lancer quoi que ce soit (rien n'est lancé)

1. **Un générateur exhaustif des 1,4e10 types.** Mon programme tire des boules au hasard. Le générateur (une boule par
   classe d'isomorphisme, ou un excès contrôlé) n'existe pas pour le cas connexe ; il doit être écrit et validé (son
   total contre la masse). Son coût par boule devrait rester très inférieur à la milliseconde, non mesuré.
2. **Les boules connexes avec torsion (15 %)** : autre modèle (vecteur de torsion équilibré, `fastg.c` de la session
   portable), non accéléré ici.
3. **Les boules avec prisme (92 % de la masse) et les boules non connexes avec prisme** : hors du programme actuel
   (triangles dans G(T), 4-cycles de type I). Sans elles, ou sans un lemme donnant une droite sans prisme, le rang 37
   n'est pas exclu même si toute la première ligne meurt. L'énoncé accessible est : « au rang 37, aucune droite sans
   prisme n'a un graphe connexe sans torsion » (avec l'énoncé B de la session portable, incomplet lui aussi).
4. **Rigueur des filtres réels** : flottants. Pour une preuve, la version entière (2,2 ms) est la version sûre ; la
   version réelle demanderait une analyse d'erreur ou un recalcul exact.
5. **Audit du modèle** par un tiers (Codex n'a audité que la partie maille 5).

## Fichiers

`star37d.c` (version rapide ; modes `check` et `plant` ; `gcc -O3 -march=native`, ou `-DSCALAR`), `star37c.c` (étape
intermédiaire : bits, conditions entières seules), `star37.c` (référence), `star37b.c`, `star37_stats.c`,
`star37_spread.c` (première étape), `OUTPUT_star37d_seed41_integer.txt`, `OUTPUT_star37d_seed41_real.txt`.
Un processus, environ 30 Mo (100 Mo en mode `check`), chaque essai de quelques secondes à une minute.
