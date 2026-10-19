# Inventaire des 10 052 gabarits c = 3 (19/10/2026, vers 08 h 20 UTC)

## Fichiers

- **Table complète** : `c3_inventaire_2026-10-19.csv`.
  - 10 052 lignes, séparateur « ; », UTF-8 : elle s'ouvre directement dans Excel.
  - La même table existe en JSON (`c3_inventaire_2026-10-19.json`), avec un résumé (`_resume.json`).
- **Script** : `c3_inventaire_2026-10-19.py`.
  - Il ne calcule aucun nouveau verdict. Il rejoue les règles du registre `c3_ledger_2026-10-19.py` sur les répertoires de
    runs rapatriés.
  - Il recalcule en arithmétique exacte les propriétés de structure de chaque gabarit.
- **Univers** : les 10 052 gabarits ouverts à l'issue du test de Gram entier.
  - 10 027 gabarits `gz` : `c3_open_templates_k3_12.json.gz`, de 3 à 12 grilles.
  - 3 gabarits `g1` (une grille) et 22 gabarits `g2` (deux grilles), dans les fichiers d'entrée de Codex.

## Bilan

| | Exclus | Ouverts |
|---|---:|---:|
| gz | 9 987 | 40 |
| g1 | 3 | 0 |
| g2 | 22 | 0 |
| **Total** | **10 012** | **40** |

**Les 40 ouverts.**
- **8 sont dans P3**, en production sur AWS : 2708, 2718, 2721, 2727, 5984, 6010, 7841, 9798.
- **2 sont dans 2K2N seulement**, en production locale avec les marques B/C : 7991, 9904.
- **20 n'ont aucune paire partagée forcée.**
- **10 ont une paire partagée mais pas assez de grilles pour les familles existantes** : 2744, 2751, 5986, 6019, 7972,
  9342, 9387, 9657, 9673, 9883.

## Codes des méthodes

Définitions reprises des commentaires des règles du registre. « Verdict de solveur » signifie INFEASIBLE sans certificat
vérifiable.

| Code | Méthode | Nature de la preuve | Gabarits (présente / seule) |
|---|---|---|---:|
| P1 | 1re passe : étoile complète, 60 s par représentant d'orbite de flips (c3oa, c3ob, après correction du bug OR-Tools) | verdict de solveur | 3 574 / 1 |
| P2 | 2e passe : couverture complète de Gram + table sur chaque entrée, modèle exact (c3ga, c3gb, c3ga2) | verdict de solveur ; couverture recoupée par l'énumérateur de Codex, sauf 35 notés | 3 605 / 14 |
| GC | tests de couverture de Gram sur le noyau dur (gc1a, gc2a) | verdict de solveur | 8 / 0 |
| P3, P3E, P3H, P3EH | Gram par Gram avec filtres de moments (gc3b, c3gs), avec reprises c3hard1 (H) et sonde propre c3eig1 (E) | verdict de solveur | 125, 29, 2, 28 / 1 (P3E) |
| P4E | sonde propre de Codex (fixed_gram_probe --eigen, rang ≤ 6) sur toutes les Gram de la couverture | verdict de solveur | 261 / 0 |
| PALL, PORB | union des sondes à Gram fixée couvrant toutes les Gram (PALL) ou tous les représentants d'orbite (PORB) | verdict de solveur | 440, 99 / 2, 2 |
| ZJ | modèle sans Gram de Codex (jhat_zjoint) | verdict de solveur | 135 / 0 |
| ZC | design de comptage de Codex : certificat de Farkas exact, revérifié en entiers | certificat | 7 361 / 12 |
| ZCP | même design, verdicts CP-SAT sur les multiplicités | verdict de solveur | 392 / 3 |
| MOM | certificats de moments (Codex ; LAB 5128 et 4192) | certificat | 2 / 0 |
| T23 | famille (2,3) de Codex (7d95ad5e) : calcul exact, sans Gram, sous E3 | calcul fini exact | 403 / 0 |
| C4C3 | fermeture C4+C3 : cœur de 8, puis 20, 36 et frontière (comme 5602) | calcul fini exact | 134 / 6 |
| K3U | famille K3 universelle (manifeste de Codex, 322 preuves RUP) | calcul exact + RUP, sous E3 | 1 613 / 7 |
| 2K2 | famille 2K2 (deux étages, certificats de Codex) | calcul exact + RUP, sous E3 | 4 772 / 16 |
| P3NB | famille P3NB (fermée cette nuit) | calcul exact + RUP, sous E3 | 8 618 / 24 |
| K2BC | famille K2BC (fermée ce matin, 3e relecture propre) | calcul exact + RUP, sous E3 | 8 088 / 57 |
| GFM | modèle de moments sans Gram | **retiré le 18/10 (bug OR-Tools)** ; aucun gabarit ne l'utilise | 0 |

- Nombre de méthodes par exclu : 145 gabarits par une seule, 836 par deux, 2 367 par trois, et 6 664 par quatre ou plus.
- **Points fragiles à revoir** :
  - **gz 155** n'est exclu que par P2, et sa couverture P2 n'a pas été confirmée par l'énumérateur de Codex. C'est le seul
    exclu dans ce cas ; il faut le confirmer.
  - 22 autres ne tiennent qu'à un verdict de solveur sans certificat :
    - P2 seul : g2 15 et gz 157, 164, 851, 852, 856, 1474, 1480, 5600, 6067, 7851, 7852, 8274 ;
    - ZCP seul : g2 5, gz 838, 6004 ;
    - PALL seul : gz 6014, 6069 ;
    - PORB seul : gz 7853, 9820 ;
    - P3E seul : gz 857 ;
    - P1 seul : gz 10009.

## Structure (propriétés recalculées pour chaque gabarit)

Pour chaque gabarit, la table donne aussi :
- **Les relations à deux termes** forcées par les relations de blocs et de grilles (calcul exact) :
  - paire partagée H_ab = −H_ac ;
  - paire opposée disjointe ;
  - paire égale H_A = H_B.
- **Le plus petit cœur signé S|T** (|S| = 3) : la somme des H internes à S égale celle des H internes à T. Le cœur est la
  réunion des rectangles internes non-grilles.
- **Le meilleur cœur bloc.** Un bloc non-grille P à une droite a donne un cœur 2-régulier de 4|P| étiquettes. Les grilles
  Y (sur les droites libres) le découpent en |P|-uplets, et les grilles internes à P le couplent.
- **Les familles** dont il est membre : K3U, P3U, 2K2, 2K2N, P3NB, K2BC, 45+14+26.

| Dimension du noyau | Exclus | Ouverts |
|---:|---:|---:|
| 2 | 23 | 0 |
| 3 | 776 | 0 |
| 4 | 4 750 | 6 |
| 5 | 4 233 | 20 |
| 6 | 227 | 13 |
| 7 | 3 | 1 |

Les ouverts ont tous de 6 à 12 grilles.

**Sans paire partagée : 27 gabarits en tout, dont 7 exclus.**
- Six l'ont été par C4C3 : gz 5602, 7912, 9229, 9505, 9744 (aussi ZJ) et 9954. Ils ont tous une **paire opposée
  disjointe**, donc un cœur signé de 8 sommets.
- Le septième, gz 10009, est exclu par P1 seul ; il a trois paires égales.
- Parmi les 20 ouverts, 3 ont un cœur de 8, mais formé d'une paire **égale** (9179, 9912, 9966) : C4C3 ne s'y applique
  pas. Les 17 autres ont des cœurs de 12 ou 16.

## Les 40 ouverts

| Gabarit | dim | grilles | paires partagées | paires égales | cœur signé min | meilleur cœur bloc | état |
|---|---:|---|---|---|---|---|---|
| gz 2708 | 6 | 01 02 13 24 34 56 | 05/15 16/26 | - | 20 | 8@5{01} Y=24,34 | P3 (AWS) |
| gz 2718 | 6 | 01 02 13 24 34 56 | 05/15 06/26 | - | 20 | 8@5{01} Y=24,34 | P3 (AWS) |
| gz 2721 | 6 | 01 02 13 24 34 56 | 05/15 06/46 | - | 20 | 8@5{01} Y=24,34 | P3 (AWS) |
| gz 2727 | 6 | 01 02 13 24 34 56 | 05/15 26/36 | - | 20 | 8@5{01} Y=24,34 | P3 (AWS) |
| gz 5984 | 5 | 01 02 03 12 14 34 56 | 05/15 16/26 | - | 16 | 8@6{12} Y=03,34 | P3 (AWS) |
| gz 6010 | 5 | 01 02 03 12 14 34 56 | 15/45 26/36 | - | 16 | 8@5{14} Y=02,03 | P3 (AWS) |
| gz 7841 | 5 | 01 02 03 04 05 06 12 | 13/23 14/24 15/25 16/26 | 34=56 35=46 36=45 | 20 | 8@3{12} Y=04,05,06 | P3 (AWS) |
| gz 9798 | 5 | 01 02 03 04 05 06 12 13 14 56 | 15/16 | - | 12 | 8@1{56} Y=02,03,04 | P3 (AWS) |
| gz 7991 | 5 | 02 03 04 12 13 15 46 56 | 06/16 26/36 | - | 12 | 8@6{23} Y=04,15 | 2K2N (local) |
| gz 9904 | 4 | 01 02 03 04 13 15 16 24 25 26 | 05/06 12/14 12/23 | 14=23 | 12 | 8@0{56} Y=13,24 | 2K2N (local) |
| gz 5628 | 7 | 01 02 13 24 35 46 56 | - | - | 16 | 16@0{3456} P=35,46,56 | sans paire |
| gz 7861 | 6 | 01 02 03 12 14 35 46 56 | - | - | 12 | 12@0{456} Y=12 P=46,56 | sans paire |
| gz 7937 | 6 | 01 02 04 13 15 23 46 56 | - | - | 12 | 12@0{356} P=56 | sans paire |
| gz 7990 | 6 | 02 03 04 12 13 15 46 56 | - | - | 12 | 12@0{156} P=15,56 | sans paire |
| gz 8111 | 6 | 02 03 05 12 14 16 34 56 | - | - | 16 | 12@0{146} P=14,16 | sans paire |
| gz 9174 | 6 | 01 02 03 12 13 23 45 46 56 | - | - | 12 | 12@0{456} Y=12,13,23 P=45,46,56 | sans paire |
| gz 9179 | 5 | 01 02 03 12 13 24 35 46 56 | - | 23=45 | 8 | 12@0{456} Y=12,13 P=46,56 | sans paire |
| gz 9221 | 5 | 01 02 03 12 14 25 34 36 56 | - | - | 12 | 12@1{356} Y=02 P=36,56 | sans paire |
| gz 9239 | 5 | 02 03 04 12 13 14 25 36 56 | - | - | 12 | 12@0{156} P=56 | sans paire |
| gz 9302 | 6 | 01 02 03 04 05 06 12 34 56 | - | - | 16 | 16@1{3456} Y=02 P=34,56 | sans paire |
| gz 9502 | 5 | 01 02 04 12 15 26 34 35 36 | - | - | 12 | 12@0{356} Y=12 P=35,36 | sans paire |
| gz 9512 | 5 | 01 02 03 14 15 24 26 35 36 | - | - | 12 | 12@1{236} P=26,36 | sans paire |
| gz 9522 | 5 | 01 03 04 12 15 24 26 35 36 | - | - | 12 | 12@2{035} P=03,35 | sans paire |
| gz 9748 | 4 | 02 03 04 12 13 14 25 35 46 56 | - | - | 12 | 12@4{235} P=25,35 | sans paire |
| gz 9791 | 5 | 01 02 03 04 05 06 12 13 24 56 | - | - | 12 | 12@1{456} Y=02,03 P=56 | sans paire |
| gz 9912 | 5 | 01 02 03 04 05 06 13 14 25 26 | - | 34=56 | 8 | 12@1{256} Y=03,04 P=25,26 | sans paire |
| gz 9966 | 4 | 01 02 03 04 05 06 12 13 24 35 46 | - | 15=26 | 8 | 12@3{246} Y=01,05 P=24,46 | sans paire |
| gz 10003 | 5 | 01 02 03 04 05 06 12 13 14 15 16 | - | - | 16 | 16@2{3456} Y=01 | sans paire |
| gz 10006 | 4 | 01 02 03 04 05 06 12 13 23 45 46 56 | - | - | 12 | 12@1{456} Y=02,03,23 P=45,46,56 | sans paire |
| gz 10025 | 4 | 01 02 03 04 05 06 12 13 14 15 16 23 | - | - | 12 | 12@2{456} Y=01,03,13 | sans paire |
| gz 2744 | 6 | 01 02 13 24 34 56 | 06/46 15/25 | - | 20 | 8@5{12} Y=34 | paire, sans outil |
| gz 2751 | 6 | 01 02 13 24 34 56 | 15/25 16/46 | - | 20 | 8@5{12} Y=34 | paire, sans outil |
| gz 5986 | 5 | 01 02 03 12 14 34 56 | 05/15 26/36 | - | 16 | 8@6{23} Y=01,14 | paire, sans outil |
| gz 6019 | 5 | 01 02 03 12 14 34 56 | 25/35 26/46 | - | 16 | 8@5{23} Y=01,14 | paire, sans outil |
| gz 7972 | 6 | 01 02 04 05 13 23 46 56 | 03/06 | - | 12 | 8@0{36} | paire, sans outil |
| gz 9342 | 5 | 02 03 04 05 12 13 14 26 56 | 01/06 | - | 12 | 8@0{16} | paire, sans outil |
| gz 9387 | 5 | 02 03 04 05 12 13 14 16 56 | 01/06 01/15 | 06=15 | 16 | 8@0{16} P=16 | paire, sans outil |
| gz 9657 | 5 | 01 03 04 05 13 16 24 25 26 | 02/06 | - | 12 | 8@0{26} Y=13 P=26 | paire, sans outil |
| gz 9673 | 5 | 03 04 05 06 12 13 14 25 26 | 01/02 | - | 12 | 8@0{12} P=12 | paire, sans outil |
| gz 9883 | 4 | 02 03 04 05 12 14 15 16 23 36 | 01/06 01/13 | 06=13 | 12 | 8@0{16} Y=23 P=16 | paire, sans outil |

Notation du cœur bloc : `taille@droite{bloc}`. Y désigne les grilles Y qui découpent le cœur ; P désigne les grilles
internes au bloc.

## Colonnes du CSV

| Colonne | Contenu |
|---|---|
| gabarit, source, indice | identifiant |
| statut, methodes, nb_methodes, notes | registre |
| dim_noyau, nb_grilles, grilles, composantes_par_droite, blocs | gabarit |
| paires_partagees, paires_opposees_disjointes, paires_egales, sans_paire | relations à deux termes |
| coeur_signe_min, meilleur_coeur_bloc | cœurs |
| familles | appartenance aux familles, gz seulement |
| gram_catalogue | statut de Gram du catalogue |
| etat_si_ouvert | pour les ouverts : production en cours ou absence d'outil |
