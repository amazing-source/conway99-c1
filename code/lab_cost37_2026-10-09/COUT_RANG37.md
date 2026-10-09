# Coût du calcul du rang 37 : mesures (session du PC labo, 09/10/2026, mis à jour à 19:29 UTC)

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

Tirages (graine 41) et masse (11!!)^3/6 = 1,87e11 des boules étiquetées modulo les symétries :

| classe de boules connexes, sans torsion | part de la masse | types | à tester (discriminant non résidu) | version entière | avec filtres réels |
|---|---|---|---|---|---|
| sans prisme (ni triangle dans G(T), ni 4-cycle de type I) | 7,2 % | 1,35e10 | 42 % : 5,7e9 | 2,2 ms : 145 jours-cœur | 1,26 ms : 83 jours-cœur |
| sans triangle dans G(T), 4-cycles de type I permis (contient la ligne du dessus) | 28,7 % | 5,4e10 | 43,5 % : 2,3e10 | 1,71 ms : 1,3 année-cœur | 0,99 ms : 0,73 année-cœur |
| **toutes les boules connexes** (triangles de G(T) permis ; contient les deux lignes du dessus) | 78,8 % | 1,47e11 | 42,8 % : 6,3e10 | 1,33 ms : **2,7 années-cœur** | 0,77 ms : **1,5 année-cœur** |

Avec la recherche de départ (60 ms) la troisième ligne coûterait plus de 100 années-cœur.
Dans les trois classes, environ 14 % des boules valides ont de la torsion (non traitées ici) et 42 à 43 % ont un
discriminant résidu (éliminées sans recherche, L23 de Codex). Aucune des 10 000 boules testées n'a d'étoile.
Les classes 2 et 3 sont des options du même programme (variables `STAR37_TYPE1`, `STAR37_NT`) ; pour la classe 3 le
sommet d'étoile est pris hors des triangles de G(T), l'étoile a alors la même forme. Mêmes contrôles à 0 écart
(80 + 80 boules en mode `check`, 30 + 30 en contrôle positif).

Essai sans gain : les filtres réels de l'autre espace propre (vecteurs résiduels dans R^18) ne retirent rien de plus
(8239,0 étoiles partielles au niveau 3 avec ou sans eux, sur 40 boules).

Ce PC a 8 cœurs (16 fils) : avec la limite de 80 % il fournit environ 7 cœurs, pas 12 (ma note précédente disait
« une année-cœur par mois », c'était trop). Troisième ligne : 20 semaines de ce PC en version entière, 11 semaines
avec les filtres réels ; moitié moins avec l'ordinateur portable en plus. En location, de l'ordre de 300 à 500 dollars
pour la version entière (ordre de grandeur non vérifié, aucun devis).

## Ce qui manque pour lancer quoi que ce soit (rien n'est lancé)

1. **Un générateur exhaustif des 1,4e10 types.** Mon programme tire des boules au hasard. Le générateur (une boule par
   classe d'isomorphisme, ou un excès contrôlé) n'existe pas pour le cas connexe ; il doit être écrit et validé (son
   total contre la masse). Son coût par boule devrait rester très inférieur à la milliseconde, non mesuré.
2. **Les boules connexes avec torsion (15 %)** : autre modèle (vecteur de torsion équilibré, `fastg.c` de la session
   portable), non accéléré ici.
3. **Les boules non connexes** (profils avec ou sans prisme) : modèles de la session portable, non accélérés ici ;
   la droite dans six grilles n'est pas décidée par une seule étoile (note de la session portable).
   L'énoncé que le balayage de la troisième ligne donnerait à lui seul : « au rang 37, aucune droite n'a un graphe
   connexe sans torsion ».
4. **Rigueur des filtres réels** : flottants. Pour une preuve, la version entière (2,2 ms) est la version sûre ; la
   version réelle demanderait une analyse d'erreur ou un recalcul exact.
5. **Audit du modèle** par un tiers (Codex n'a audité que la partie maille 5).

## Fichiers

`star37d.c` (version rapide ; modes `check` et `plant` ; `gcc -O3 -march=native`, ou `-DSCALAR`), `star37c.c` (étape
intermédiaire : bits, conditions entières seules), `star37.c` (référence), `star37b.c`, `star37_stats.c`,
`star37_spread.c` (première étape), `OUTPUT_star37d_seed41_*.txt` (six sorties : trois classes, avec et sans filtres réels).
Un processus, environ 30 Mo (100 Mo en mode `check`), chaque essai de quelques secondes à une minute.
