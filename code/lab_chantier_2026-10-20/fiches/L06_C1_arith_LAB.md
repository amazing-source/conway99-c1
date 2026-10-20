# Fiche L06_C1_arith_LAB : arithmétique de C1 par la session du PC labo (LAB), 07 au 13/10/2026, et pièces rattachées

Agent de consolidation du chantier du 20/10/2026. Lecture seule des sources ; aucun calcul relancé (seuls des `git show`,
des lectures et deux comparaisons de copies). 182 résultats dans `fiches/L06_C1_arith_LAB.jsonl` (identifiants
L06-001 à L06-182, sur trois chiffres car il y en a plus de 99). Statuts recopiés des sources, jamais rehaussés.

Abréviations des sources (chemins relatifs à la racine du dépôt de travail sauf mention) :
- NOTE = `work/c1_theta_lp_2026-10-07/NOTE.md` (4240 lignes ; copie identique, blob 752b249b, dans
  `conway99-c1:origin/main:code/lab_theta_lp_2026-10-08/NOTE.md`, et dans les branches `origin/lab/theta-lp-2026-10-08`
  et `origin/lab/exploration-2026-10-16` ; copie CRLF af07a02e dans `Desktop/Recherche_Conway/c1-main-codex/`).
- RB = `work/c1_theta_lp_2026-10-07/RECHERCHE_B_REALISATION_GLOBALE.md` ; COUT = `work/c1_cost37_2026-10-09/COUT_RANG37.md` ;
  RD = `work/c1_index_2026-10-09/NOTE_RESEAUX_DE_DROITE.md` ; S3 = `work/s3_question_2026-10-12/NOTE_S3.md` ;
  SF = `work/spreadfree_243_2026-10-12/NOTE_SPREADFREE.md` ; NG = `.../NEW_GRAPHS_2026-10-13.md` ;
  TR = `work/c1_triangles_2026-10-13/NOTE_TRIANGLES.md` ; BP = `work/c1_biplane_test_2026-10-07/{README.md,RESULT.txt,OUTPUT.txt}` ;
  LAPR = `work/c1_lap_sweep48_2026-10-09/README.md`.
- DI = `conway99-c1:origin/main:code/lab_theta_lp_2026-10-08/imports_2026-10-09_convergences/DOSSIER_C1_INTEGRE.md`
  (dossier externe « Convergences », auteur non indiqué ; original dans `Desktop/Recherche_Conway/c1-imports/`).
- JOURNAL = `C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md` (journal C1 du 24 au 26/09 ; trois copies
  identiques, même md5 : c1-norm16-export, c1-p3-export, c2_experimental/external_c1).
- Articles : `conway99-c1:origin/main:papers/{README.md, rank7/rank7.tex, s5_2adic/s5_2adic.tex, srg243_second/srg243_second.tex}`
  et `strongly-regular-graphs-research:main:papers/{conway99_asymmetric, conway99_order2, conway99_order3, conway99_order7}`.
- Auteurs : LAB = session du PC labo ; LAP = session de l'ordinateur portable (« laptop session ») ; Codex ; Astra ;
  « structures » = session du labo des structures ; C1 = session C1 de septembre (auteur du JOURNAL).

## 1. Résumé (10 lignes)

1. Le programme thêta de niveau 7 (réseaux L1 et M = sqrt7 L1*) exclut r = rang_7(A - 3I) <= 33 (07/10) puis r = 35 (08/10,
   identité entière de Codex re-vérifiée) : fenêtre r ∈ {37, 39, 41, 43}, statut C, audité par Codex (L06-023, L06-024).
2. Échelle : min(L1) <= 20 / 24 / 24 / 26 ; identités exactes 2a_8 + 16a_9 + a_13 = 329(7^m+1) + … et, au rang 37,
   350 a_8 + 91 a_9 + 13 a_10 = 7462 + … (L06-015, L06-030) ; chemin critique : normes 18 et 26 (L06-103).
3. Rang 37 par comptage (recensement d'induits, jumeaux, grilles, collisions) : CLOS par sa marge (L06-046) ; les
   canaux de masses 7 à 9 ne sont bornés qu'à 20-35 fois la marge (L06-056).
4. Rang 37 par les étoiles : certificats exacts par boule (L06-074), aucune raison uniforme ; barrière de Codex et
   complétude des paires : aucune obstruction par la seule forme bilinéaire (L06-077, L06-078).
5. Lemme N14 (calcul exhaustif, non audité) : pas de vecteur propre (-4) de norme 14 au rang 37 (L06-092) ; norme 16 : trois
   mondes tués, catalogue incomplet ; normes 18 et 20 hors de portée (L06-168).
6. Sans rang : 373 -> 310 coeurs de Makhnev (Codex, re-dérivé indépendamment par LAB) puis 174 (Codex ; LAB a seulement
   apparié l'encodage) ; aucun coeur ne meurt dans les pilotes (15 et 29 coeurs) ; loi de parité prouvée sans effet ; rubans <= 5.
7. 243 sommets : question S3 close par UNSAT avec DRAT vérifié (encodage non audité) ; huit srg(243,22,1,2) connus dont quatre
   nouveaux sans spread régulier ; aucun membre asymétrique (L06-128, L06-130).
8. Aucune exclusion de C1, ni du rang 37, n'est obtenue dans ce lot ; le rang 37 est un cas d'égalité dont les maillons (a')
   et NT restent ouverts (L06-066, L06-067).
9. Deux redécouvertes du lemme L23 de septembre le 09/10 ; une redécouverte plus faible de la fenêtre le 14/10 (lot L07).
10. Le lot contient aussi le journal C1 de septembre (L16-L25) et six articles (rank7, s5_2adic, srg243_second, C2, C3, C7).

## 2. Chronologie

- 24-26/09 (JOURNAL) : session C1 : L16 P <= 1151 ; L20 (k >= 6, 8, 10) ; L21 (droite générique : k >= 22) ; L22 (k <= 28) ;
  L23 ; L8 (pas de point de Hamming) ; L25 ; L11 ; cycles des graphes de droites ; résultats sous NT ; transfert q:7 vers C2.
- 23/09 : manuscrit C3 (preuve candidate, Lean) ; octobre : manuscrit C7.
- 07/10 21:06-21:14 UTC : test biplan sur BvLS et twin (BP) ; 07/10 : `papers/README.md` « Articles prêts à relire »
  (rank7, s5_2adic, srg243_second), note « asymmetric » et brouillon 2 de C2.
- 07/10 soir : programme thêta : r >= 29 / 33 (sect. 1-8), r = 33 exclu à 22:57 UTC, audité par Codex (note 172) à 23:07 UTC.
- 08/10 00:04-01:23 UTC : règles de descente, lemme F, identité de la sect. 15, 6-ensembles, empilement des graines,
  **r = 35 exclu à 01:23 UTC** ; 01:28 : note 180 de Codex lue.
- 08/10 07:12-15:00 : rang 37 par comptage : recensement LAB (08:24), plafonds (08:38), jumeaux et grilles (11:15), coupes de
  Codex, corrections 17.44 (14:47) et 17.45 (15:00) : comptage des supports <= 9 clos.
- 08/10 15:20-17:30 : littérature ; droite à six grilles et Petersen ; classes de grilles mod 7 ; relations à un sommet
  (lemme 4+3, 16:25-16:55) ; rétrospective « cas d'égalité » (16:55).
- 08/10 17:50-21:25 : (6,6) partout ; modèle à deux étoiles (certificats, 18:30-20:42) ; une étoile ; barrière de Codex (21:25).
- 08/10 21:54-23:55 : routes de C2 relues ; coeurs de Makhnev 373 -> 310 -> 174 ; résultat maille 5 de LAP et son audit ;
  cibles « plus de 200 prismes » puis correction.
- 09/10 00:01-05:08 : lemme des moulins ; balayage (4,8) (fini 04:49) ; L23 redécouvert (03:44, signalé 03:49) ;
  **calculs arrêtés par l'utilisateur à 05:08 UTC**.
- 09/10 05:51-14:55 : noyaux de quadrangle ; mandat B (loi de parité, RB) ; rubans ; quartiques exactes (12:59).
- 09/10 (13:09) : dossier externe « Convergences » (DI) lu ; 09/10 jusqu'à 19:29 : COUT (mesures de coût du rang 37).
- 09/10 20:29-23:16 : 17.88 (faux) puis 17.89 ; anatomie des boules ; dépendances collectives ; stratégie des vecteurs courts.
- 09/10 ~21:31 : RD (réseaux de droite, invariants de Hasse ; L23 retrouvé une seconde fois).
- 10/10 00:02 : **lemme N14** ; 00:33-02:11 : coeurs des normes 18 et 20, norme 18 à supports indépendants, n16cell
  (trois mondes tués), identité 17.100 (01:36).
- 12/10 11:57 : branche co-Heawood sans rang et monde de norme 18 (17.101) ; message de Codex sur la même branche.
- 12/10 12:55 -> 13/10 13:00 : question S3 (UNSAT 18:36 le 12/10 ; DRAT vérifié le 13/10).
- 12/10 19:20 -> 13/10 17:41 : graphes à 243 sommets sans spread (SF, NG) ; 13/10 18:56 : TR.

## 3. Table des résultats

| id | énoncé court | statut | source principale |
|---|---|---|---|
| L06-001 | Cadre thêta de niveau 7 : réseaux L, L1, M et séries dans M_22(Gamma_0(7)) | P | work/c1_theta_lp_2026-10-07/NOTE.md:3-29 |
| L06-002 | Premières exclusions thêta : r <= 27 ; r >= 29 seul, r >= 33 avec le lemme a_7 = 0 de Codex | C | work/c1_theta_lp_2026-10-07/NOTE.md:31-66 |
| L06-003 | Plafonds a_7 <= 7920 (vecteurs de Fano) et b_1 <= 3784 (racines de M) | P | work/c1_theta_lp_2026-10-07/NOTE.md:102-106 |
| L06-004 | Au plus 4 vecteurs de norme 16 par graine : a_8 <= 27 720 | P | work/c1_theta_lp_2026-10-07/NOTE.md:131-136 |
| L06-005 | Bornes duales distinctes b_4 >= 1 431 738 (familles F1, F2) et b_5, b_6, b_7 | P | work/c1_theta_lp_2026-10-07/NOTE.md:178-215 |
| L06-006 | Rang 33 exclu (identité entière à d = 32) | C | work/c1_theta_lp_2026-10-07/NOTE.md:217-242 |
| L06-007 | Échelle des minima de L1 : min(L1) <= 18 / 20 / 24 / 24 / 26 pour r = 35 / 37 / 39 / 41 / 43 | C | work/c1_theta_lp_2026-10-07/NOTE.md:67-70 |
| L06-008 | Nombres forcés de vecteurs courts de L1 par rang (tables d'abondance) | E | work/c1_theta_lp_2026-10-07/NOTE.md:107-122 |
| L06-009 | What-if : absence de racine et petits nombres de vecteurs de normes 4 et 6 de M fermeraient le haut de la fenêtre | H | work/c1_theta_lp_2026-10-07/NOTE.md:71-74 |
| L06-010 | Rang 43 : a_7k = b_k pour tout k (forme parabolique de SL_2(Z)) | P | work/c1_theta_lp_2026-10-07/NOTE.md:123-127 |
| L06-011 | Côté valeur propre 3 : réseau pair de rang 60, seconde échelle, aucune exclusion | E | work/c1_theta_lp_2026-10-07/NOTE.md:256-280 |
| L06-012 | Programme theta_pi (réseau Lam de rang 52 avec les vecteurs de sommets) plus faible | E | work/c1_theta_lp_2026-10-07/NOTE.md:281-290 |
| L06-013 | Règles de descente (R1), (R2) contre les vecteurs forcés de sqrt7 M | P | work/c1_theta_lp_2026-10-07/NOTE.md:300-309 |
| L06-014 | Lemme F : deux vecteurs de Fano distincts ne diffèrent jamais d'un vecteur de Fano ; b_1 <= 88 | P | work/c1_theta_lp_2026-10-07/NOTE.md:338-344 |
| L06-015 | Identité universelle des coefficients (section 15) : 2 a_8 + 16 a_9 + a_13 = 329 (7^m + 1) + 7^(m+1) b_1 + 7 a_7 + 7 a_10 + 2 a_11 + a_12 | C | work/c1_theta_lp_2026-10-07/NOTE.md:353-370 |
| L06-016 | Les coefficients duaux comme fonctions affines exactes de (a_7..a_13) ; inégalités (I1)-(I3) | E | work/c1_theta_lp_2026-10-07/NOTE.md:372-400 |
| L06-017 | Lemme G : les solutions entières de (A - 3I) phi = 1 de norme minimale sont exactement les grilles 3x3 induites | P | work/c1_theta_lp_2026-10-07/NOTE.md:422-442 |
| L06-018 | Comptes des 6-ensembles : N(6,7) = 831 600 + 36 P, N(6,8) = 20 790 - 9 P, N(6,9) = P, N(6,6) = 8 560 860 - 84 P | P | work/c1_theta_lp_2026-10-07/NOTE.md:460-519 |
| L06-019 | Famille (a) triangle moins chemin lointain : 731 808 + 12 P vecteurs (puis - 48 tau) | P | work/c1_theta_lp_2026-10-07/NOTE.md:444-458 |
| L06-020 | Rang 35 => au moins 43 grilles et plus de 400 prismes (énoncé à auditer), puis rho >= 44, P >= 492 | X | work/c1_theta_lp_2026-10-07/NOTE.md:521-528 |
| L06-021 | Lemme d'empilement des graines (seed packing) : a_7 <= 990 | P | work/c1_theta_lp_2026-10-07/NOTE.md:597-617 |
| L06-022 | Borne uniforme b_4 >= 2 729 034 (Codex, sans paramètre de grille ni de jumeaux) | P | work/c1_theta_lp_2026-10-07/NOTE.md:635-640 |
| L06-023 | Rang 35 exclu (identité de Codex, re-vérifiée par LAB) | C | work/c1_theta_lp_2026-10-07/NOTE.md:633-655 |
| L06-024 | Fenêtre des rangs : r in {37, 39, 41, 43} | C | work/c1_theta_lp_2026-10-07/NOTE.md:655 |
| L06-025 | Bornes duales uniformes de Codex (vecteurs distincts) : progression b_3, b_4, b_5 | C | work/c1_theta_lp_2026-10-07/NOTE.md:689-693 |
| L06-026 | Rang 43 en six paramètres et conditions d'exclusion | C | work/c1_theta_lp_2026-10-07/NOTE.md:1032-1044 |
| L06-027 | Profil C = 22-coclique marquée ; 44 vecteurs de norme 28 de L1 par 22-coclique | P | work/c1_theta_lp_2026-10-07/NOTE.md:1046-1064 |
| L06-028 | Tout vecteur de Fano contient deux 22-cocliques ; b_1 <= 44 ; b_2 >= 968 à r = 43 | P | work/c1_theta_lp_2026-10-07/NOTE.md:1066-1088 |
| L06-029 | Réseau d'une 22-coclique (programme de niveau 21) : aucune exclusion | E | work/c1_theta_lp_2026-10-07/NOTE.md:1116-1140 |
| L06-030 | Rang 37 en une identité (d = 36) : 13 a_10 + 91 a_9 + 350 a_8 + 1183 a_7 = 7462 + a_12 + 2429 b_1 + 476 (b_2 - 462) + 21 (b_3 - 24948) | C | work/c1_theta_lp_2026-10-07/NOTE.md:4068-4086 |
| L06-031 | Nombres forcés au rang 37 sans vecteur de Fano : >= 22 (normes 16-20), >= 82 (18/20 sans 16), >= 574 (norme 20 sans 16 ni 18) | C | work/c1_theta_lp_2026-10-07/NOTE.md:4074-4078 |
| L06-032 | Après N14 (a_7 = b_1 = 0, statut E) et avec b_3 >= 45 898 (Codex) : 350 a_8 + 91 a_9 + 13 a_10 >= 447 412 au rang 37 | C | work/c1_theta_lp_2026-10-07/NOTE.md:4088-4115 |
| L06-033 | Quartiques harmoniques (sommets et droites) : réponse exacte, aucune exclusion au rang 37 | C | work/c1_theta_lp_2026-10-07/NOTE.md:3395-3411 |
| L06-034 | Le 3-côté ne borne pas les grilles ni les jumeaux ; sur-réseaux d'indice 7 n'apportent rien | E | work/c1_theta_lp_2026-10-07/NOTE.md:946-949 |
| L06-035 | Contraintes de classe mod 7 : Gram de toute famille de L1 de rang <= 45 - r ; famille de vecteurs du noyau de rang <= 56 - r | P | work/c1_theta_lp_2026-10-07/NOTE.md:1477-1482 |
| L06-036 | Moteur de recensement indépendant census2.py (ordres <= 10) : reproduit les 6533 formules du paquet de Codex | E | work/c1_theta_lp_2026-10-07/NOTE.md:855-877 |
| L06-037 | Test du recensement de Codex sur les vrais graphes à 243 sommets (ordres 8 et 9) : 0 désaccord | E | work/c1_theta_lp_2026-10-07/NOTE.md:685-717 |
| L06-038 | Plafonds du polytope du recensement d'ordre 10 (LP flottant) : P <= 852,92, H <= 1867,25, ... | H | work/c1_theta_lp_2026-10-07/NOTE.md:896-904 |
| L06-039 | Plafond recensement des Fano : a_7 <= (2/21) N(F10), d'où a_7 <= 842 ; Codex : a_7 + 13 rho <= 2013 | P | work/c1_theta_lp_2026-10-07/NOTE.md:954-960 |
| L06-040 | Théorème de structure des classes de prismes jumeaux (le coin des jumeaux est le coin des grilles) | P | work/c1_theta_lp_2026-10-07/NOTE.md:1142-1179 |
| L06-041 | Le coin LP du « monde de grilles pur » est impossible (g = 6 se propage) | P | work/c1_theta_lp_2026-10-07/NOTE.md:1181-1187 |
| L06-042 | Bornes certifiées de Codex sur tau (paires de prismes jumeaux) et sur P, rho | C | work/c1_theta_lp_2026-10-07/NOTE.md:589-590 |
| L06-043 | Constantes de collision certifiées par Codex (canal de masse six) et bornes de la sous-collection à P = 0 | C | work/c1_theta_lp_2026-10-07/NOTE.md:961-962 |
| L06-044 | Plafonds certifiés de la série thêta au rang 37 (notes 199 et 204 de Codex) | C | work/c1_theta_lp_2026-10-07/NOTE.md:1514-1516 |
| L06-045 | Paramétrisation exacte de la famille du rang 37 (LAP) et ses conséquences | C | work/c1_theta_lp_2026-10-07/NOTE.md:1376-1399 |
| L06-046 | Route de comptage (supports <= 9) au rang 37 : close sur les trois comptabilités essayées | H | work/c1_theta_lp_2026-10-07/NOTE.md:1620-1636 |
| L06-047 | CORRECTION : les seuils de 17.27, 17.41, 17.42 portaient sur une collection plus grande que celle du cap de Codex | X | work/c1_theta_lp_2026-10-07/NOTE.md:1620-1637 |
| L06-048 | Les classes de grilles vivent dans 56 - r dimensions mod 7 ; tables du modèle canonique ; certificats généraux de Codex autour d'une droite à six grilles | P | work/c1_theta_lp_2026-10-07/NOTE.md:1787-1832 |
| L06-049 | Énoncé manquant chiffré : le rang 37 est exclu dès que le nombre total de paires en collision C < 17,1 millions | H | work/c1_theta_lp_2026-10-07/NOTE.md:1888-1922 |
| L06-050 | « Au plus 10 relations mod 7 au-delà des relations de pinceau » : cible FAUSSE | R | work/c1_theta_lp_2026-10-07/NOTE.md:1936-1977 |
| L06-051 | Lemme (4 + 3) : relation exacte entre neuf grilles à un sommet, dans tout srg(99,14,1,2) | P | work/c1_theta_lp_2026-10-07/NOTE.md:2014-2031 |
| L06-052 | La droite dans six grilles : objet fini (noms dans (Z_3 x Z_2)^6, 60 étoiles ordonnées du graphe de Petersen) | O | work/c1_theta_lp_2026-10-07/NOTE.md:1689-1745 |
| L06-053 | Matrice entière d'une droite à six grilles ; q^2 = 420 q automatique ; conditions mod 3 et mod 5 automatiques | P | work/c1_theta_lp_2026-10-07/NOTE.md:2831-2864 |
| L06-054 | Lemme des moulins : deux moulins pondérés disjoints n'ont jamais la même projection ; ensemble lointain d'un support | P | work/c1_theta_lp_2026-10-07/NOTE.md:2900-2938 |
| L06-055 | Les paires de supports cubiques de même projection sont exactement les paires anticomplètes | P | work/c1_theta_lp_2026-10-07/NOTE.md:2981-3003 |
| L06-056 | LP couplé avec les bornes de collision de Codex à P = 0 : une charge par support est 20 à 35 fois trop grande | H | work/c1_theta_lp_2026-10-07/NOTE.md:2949-2979 |
| L06-057 | Cible « au rang 37 le graphe a plus de 200 prismes » : marges, puis correction | X | work/c1_theta_lp_2026-10-07/NOTE.md:2807-2829 |
| L06-058 | 17.88 « le LP de comptage sans grille est au seuil » : FAUX (deux collections comparées) | X | work/c1_theta_lp_2026-10-07/NOTE.md:3413-3477 |
| L06-059 | Une droite est dans une grille exactement quand G(T) a une composante prisme ; masse (9!!)^3/6 = 1,4e8 | P | work/c1_theta_lp_2026-10-07/NOTE.md:3438-3449 |
| L06-060 | Effet de N14 sur le LP de comptage (coin sans grille) | H | work/c1_theta_lp_2026-10-07/NOTE.md:3829-3843 |
| L06-061 | Levier réfuté : coupes de sommes de carrés (drapeaux) sur le recensement | E | work/c1_theta_lp_2026-10-07/NOTE.md:1024-1030 |
| L06-062 | Le recensement ne porte aucune congruence sur ses 549 paramètres | E | work/c1_theta_lp_2026-10-07/NOTE.md:3484-3487 |
| L06-063 | Route des graines (multiplicités par graine aux normes 18 à 24) : fermée comme méthode | S | work/c1_theta_lp_2026-10-07/NOTE.md:1319-1349 |
| L06-064 | Lemme N16 (LAP) : un vecteur de norme 16 ne peut être non nul en un point dont les lignes de graine et les autres lignes engendrent toutes des grilles | P | work/c1_theta_lp_2026-10-07/NOTE.md:1540-1547 |
| L06-065 | Représentants sans prisme, principe du « plus court représentant » (LAP) et pool | O | work/c1_theta_lp_2026-10-07/NOTE.md:1549-1618 |
| L06-066 | Le rang 37 est un cas d'égalité (identité de septembre de Codex) | P | work/c1_theta_lp_2026-10-07/NOTE.md:2052-2063 |
| L06-067 | Chaîne de septembre pour k = 22 : (a') uniforme, (NT), puis « toute droite déconnectée » | O | work/c1_theta_lp_2026-10-07/NOTE.md:2059-2063 |
| L06-068 | « Étoile complète morte 42/42 » (septembre, structures-lab) | S | work/c1_theta_lp_2026-10-07/NOTE.md:2095-2103 |
| L06-069 | Plafond local 14 : les Grams de composantes autour d'UN sommet ne peuvent exclure aucun des rangs 37, 39, 41 | P | work/c1_theta_lp_2026-10-07/NOTE.md:2133-2147 |
| L06-070 | Cas résiduel « (6,6) partout » à P = S = 0 : réduction conditionnelle, puis lecture honnête | O | work/c1_theta_lp_2026-10-07/NOTE.md:2149-2193 |
| L06-071 | Côté lointain d'une droite (6,6) : designs de triples par composante | S | work/c1_theta_lp_2026-10-07/NOTE.md:2195-2206 |
| L06-072 | Modèle conjoint de deux étoiles (Codex, notes 211-213) : trois boules aléatoires de septembre entièrement exclues par certificats finis | C | work/c1_theta_lp_2026-10-07/NOTE.md:2228-2269 |
| L06-073 | Ablation des filtres de paires (note 214 de Codex) sur la boule 12 : le seuil est la saturation | C | work/c1_theta_lp_2026-10-07/NOTE.md:2353-2385 |
| L06-074 | Réfutation de profondeur un sans solveur : valeurs de Green et sommes d'étoile seulement (1721 branches, quatre boules) | C | work/c1_theta_lp_2026-10-07/NOTE.md:2387-2425 |
| L06-075 | C'est une obstruction à UNE étoile (boule 12, étoile du sommet 12 seule) | E | work/c1_theta_lp_2026-10-07/NOTE.md:2457-2484 |
| L06-076 | Lemme de comptage de Codex : motif forcé d'une étoile complète (z = 0) | P | work/c1_theta_lp_2026-10-07/NOTE.md:2524-2554 |
| L06-077 | Barrière de Codex (note 219) : toute paire d'apex et un troisième membre compatibles se complètent en un Gram abstrait complet sur F_7 | P | work/c1_theta_lp_2026-10-07/NOTE.md:2579-2583 |
| L06-078 | Théorème : les conditions de paires sont complètes au premier ordre ; complétion abstraite (Witt) | P | work/c1_theta_lp_2026-10-07/NOTE.md:3557-3596 |
| L06-079 | Anatomie de la mort de 10 000 boules aléatoires : équidistribution, aucun mécanisme | H | work/c1_theta_lp_2026-10-07/NOTE.md:3522-3555 |
| L06-080 | Règle exacte manquante dans le test rapide : la saturation (gain mesuré) | E | work/c1_theta_lp_2026-10-07/NOTE.md:3619-3645 |
| L06-081 | Si toute boule de tout type échoue son test d'étoile, le rang 37 est exclu, sans lemme global | P | work/c1_theta_lp_2026-10-07/NOTE.md:3656-3692 |
| L06-082 | Coût mesuré du test d'une étoile par boule au rang 37 (modèle de LAP) | E | work/c1_cost37_2026-10-09/COUT_RANG37.md:1-21 |
| L06-083 | Discriminant de V et nombre d'arbres couvrants mod 7 (= L23 de Codex, redécouvert) ; corollaire B | P | work/c1_theta_lp_2026-10-07/NOTE.md:3083-3151 |
| L06-084 | Identité réelle exacte de LAP pour une droite connexe ; Pi 7-intégral au rang 37 | P | work/c1_theta_lp_2026-10-07/NOTE.md:2331-2340 |
| L06-085 | Objection : aucun complément d'étoile ne contient la boule d'une droite | P | work/c1_theta_lp_2026-10-07/NOTE.md:2631-2638 |
| L06-086 | Fait structurel : dans chaque couche, les 60 colonnes de N sont en bijection avec les 60 paires non appariées | P | work/c1_theta_lp_2026-10-07/NOTE.md:2626-2630 |
| L06-087 | LAP : au rang 37, une droite dont G(T) n'a ni triangle ni 4-cycle est CONNEXE | E | work/c1_theta_lp_2026-10-07/NOTE.md:2768-2774 |
| L06-088 | Combinaison conditionnelle : au rang 37 avec P = S = 0, NT et (a') uniforme sont incompatibles | O | work/c1_theta_lp_2026-10-07/NOTE.md:2153-2156 |
| L06-089 | Balayage (4,8) à P = 0 (modèle de LAP exécuté sur le PC labo) : toute boule représentante sans torsion est morte | E | work/c1_theta_lp_2026-10-07/NOTE.md:2940-2947 |
| L06-090 | Course pouvant fabriquer une boule « morte » (trouvée par LAP) : aucune trace dans le balayage LAB | E | work/c1_theta_lp_2026-10-07/NOTE.md:3059-3081 |
| L06-091 | Au rang 37, il existe un vecteur propre entier (-4) non nul de norme 14, 16, 18 ou 20 | C | work/c1_theta_lp_2026-10-07/NOTE.md:3700-3707 |
| L06-092 | Lemme N14 : un srg(99,14,1,2) de rang 37 n'a pas de vecteur propre entier (-4) de norme 14 | E | work/c1_theta_lp_2026-10-07/NOTE.md:3739-3825 |
| L06-093 | Le test spectral (positivité) ne tue pas le monde de norme 14 | E | work/c1_theta_lp_2026-10-07/NOTE.md:3845-3855 |
| L06-094 | Norme 16 au rang 37 : le test d'un voisinage complet (n16cell) tue les trois mondes exportés par Codex | E | work/c1_theta_lp_2026-10-07/NOTE.md:4021-4061 |
| L06-095 | Lemme : un vecteur propre entier (-4) de norme 18 a ses deux supports indépendants | P | work/c1_theta_lp_2026-10-07/NOTE.md:3968-3985 |
| L06-096 | Liste couvrante des coeurs des vecteurs propres courts : norme 14 : 1 ; 16 : 5 ; 18 : 26 ; 20 : 1199 + 182 | E | work/c1_theta_lp_2026-10-07/NOTE.md:3873-3887 |
| L06-097 | Identités de degrés pour toute norme ; en norme 20 les doubles ne sont pas indépendants ; borne de rang réel 44 - 2m | P | work/c1_theta_lp_2026-10-07/NOTE.md:3922-3952 |
| L06-098 | Norme 18 sans rang : le monde n'est pas tué par la positivité sur les doubles | E | work/c1_theta_lp_2026-10-07/NOTE.md:4209-4227 |
| L06-099 | Branche co-Heawood (deux cocliques de Hoffman se coupant en 15) sans hypothèse de rang : hors de portée d'une énumération | E | work/c1_theta_lp_2026-10-07/NOTE.md:4128-4199 |
| L06-100 | Message de Codex (12/10) : réductions démontrées sur la branche des deux 22-cocliques se coupant en 15 | P | C:/home/researcher/Desktop/Recherche_Conway/RECOVERY_2026-10-12/snapshot_20261012T113936Z/bri… |
| L06-101 | Configuration biplan minimale de norme 22 absente des srg(243,22,1,2) connus | E | work/c1_biplane_test_2026-10-07/README.md:1-60 |
| L06-102 | Un vecteur propre entier (-4) d'un srg(99,14,1,2) avec une entrée de valeur absolue >= 2 a une norme >= 20 | P | work/c1_biplane_test_2026-10-07/README.md:52-55 |
| L06-103 | Chemin critique : toute exclusion d'un rang par les mondes passe par la norme 18 ET une borne sur les vecteurs de norme 26 | C | work/c1_theta_lp_2026-10-07/NOTE.md:4229-4234 |
| L06-104 | Cible pour le rang 37 : N14 (fait), N16 et N18 au rang 37, et une BORNE PAR GRAINE pour la norme 20 | O | work/c1_theta_lp_2026-10-07/NOTE.md:4096-4106 |
| L06-105 | Recouvrement sans rang : tout srg(99,14,1,2) contient un des 310 coeurs de 14 sommets (puis 174) | P | work/c1_theta_lp_2026-10-07/NOTE.md:2666-2701 |
| L06-106 | Deux pilotes bornés sur les 174 coeurs : négatifs | H | work/c1_theta_lp_2026-10-07/NOTE.md:2709-2728 |
| L06-107 | x_58 = x_59 = 0 dans tout srg(99,14,1,2) (deux graphes 4-réguliers à 10 sommets absents) | E | work/c1_theta_lp_2026-10-07/NOTE.md:2756-2759 |
| L06-108 | Les deux noyaux obligatoires d'un quadrangle : relation exacte de partenaires entre les 174 types (aucun type exclu) | P | work/c1_theta_lp_2026-10-07/NOTE.md:3241-3316 |
| L06-109 | Loi de parité globale des holonomies de quadrangles (mandat B) | P | work/c1_theta_lp_2026-10-07/RECHERCHE_B_REALISATION_GLOBALE.md:7-51 |
| L06-110 | Loi exacte omega = somme des c_e + kappa x longueur : conjecture (neuf graphes), puis RÉFUTÉE | R | work/c1_theta_lp_2026-10-07/NOTE.md:3359-3392 |
| L06-111 | Le voisinage d'un quadrangle a 44 = multiplicité de -4 sommets : conséquences exactes sans rang | P | work/c1_theta_lp_2026-10-07/RECHERCHE_B_REALISATION_GLOBALE.md:247-266 |
| L06-112 | Cycles de transport et rubans : énoncés exacts pour tout srg(99,14,1,2) | C | work/c1_theta_lp_2026-10-07/RECHERCHE_B_REALISATION_GLOBALE.md:347-385 |
| L06-113 | Deux prismes jumeaux ont les mêmes trois sommets de barreaux ; test à un sommet : rien d'exclu | P | work/c1_theta_lp_2026-10-07/RECHERCHE_B_REALISATION_GLOBALE.md:444-454 |
| L06-114 | Dossier externe « Convergences » : théorème de saturation par témoins de bord (supports Cube et Wagner d'un cycle de transport de longueur quatre) | P | conway99-c1:origin/main:code/lab_theta_lp_2026-10-08/imports_2026-10-09_convergences/DOSS… |
| L06-115 | Dossier externe : obstruction de carré à l'extension de l'action complexe Q(sqrt(-15)) à certains blocs | P | conway99-c1:origin/main:code/lab_theta_lp_2026-10-08/imports_2026-10-09_convergences/DOSS… |
| L06-116 | Dossier externe : raccord des cinq bords aux 174 noyaux par LP couplé : faisable | H | conway99-c1:origin/main:code/lab_theta_lp_2026-10-08/imports_2026-10-09_convergences/DOSS… |
| L06-117 | Réseaux propres portés loin d'une droite : déterminants exacts, structure en 7, invariants de Hasse | P | work/c1_index_2026-10-09/NOTE_RESEAUX_DE_DROITE.md:1-62 |
| L06-118 | Hermite/Blichfeldt pour une droite connexe : min Lambda_3(T) <= 3,41 (5 * 7^(2k) Theta / 256)^(1/18) ; norme <= 30 au rang 37 pour les boules typiques | P | work/c1_index_2026-10-09/NOTE_RESEAUX_DE_DROITE.md:45-51 |
| L06-119 | Le Gram des droites (triangles) est une reformulation des coupes de sommets | P | work/c1_triangles_2026-10-13/NOTE_TRIANGLES.md:1-31 |
| L06-120 | Conjectures (G), (E), (L), (P) de Codex (notes 176-177) testées hors des revêtements : (L) pour l = 5 RÉFUTÉE | R | work/c1_triangles_2026-10-13/NOTE_TRIANGLES.md:33-74 |
| L06-121 | Un second srg(243,22,1,2) (Gamma', « twin243_switched ») : BvLS n'est pas unique | C | conway99-c1:origin/main:papers/srg243_second/srg243_second.tex:17-29 |
| L06-122 | Conjecture de Reimbayev sur le nombre d'hexagones induits : RÉFUTÉE par Gamma' | R | conway99-c1:origin/main:papers/srg243_second/srg243_second.tex:99-119 |
| L06-123 | Aucune commutation de Godsil-McKay dans un srg(v,k,1,2) pour k in {14, 22, 112, 994} | P | conway99-c1:origin/main:papers/srg243_second/srg243_second.tex:148-166 |
| L06-124 | Reformulation : srg(243,22,1,2) à spread régulier <=> graphe distance-régulier {20,18,4,1;1,2,18,20} ; quatre tels graphes deux à deux non isomorphes | P | work/s3_question_2026-10-12/NOTE_S3.md:140-153 |
| L06-125 | (S) Aucune classe de squelette de parité non triviale n'est invariante par un automorphisme non trivial de BH ; un revêtement non cyclique serait un DRG asymétrique | S | work/s3_question_2026-10-12/NOTE_S3.md:177-195 |
| L06-126 | Lemme de parité sur BH : chacune des 720 familles W(v,u,c) contient un nombre impair de paires plates | P | work/s3_question_2026-10-12/NOTE_S3.md:208-250 |
| L06-127 | Instance « paire de type B » (full_ultimate.py) UNSAT, preuve DRAT vérifiée par drat-trim | C | work/s3_question_2026-10-12/NOTE_S3.md:276-302 |
| L06-128 | Si chaque maillon tient : les srg(243,22,1,2) à spread régulier sont exactement BvLS, twin, Gamma3, Gamma4 | E | work/s3_question_2026-10-12/NOTE_S3.md:288-312 |
| L06-129 | Le graphe de Conway, s'il existe, n'a pas de spread régulier ; (lambda, mu) = (1,2) ne force pas de spread régulier | P | work/spreadfree_243_2026-10-12/NOTE_SPREADFREE.md:11-27 |
| L06-130 | Quatre nouveaux srg(243,22,1,2) sans spread régulier (Gamma5 Aut 2916 ; sixième Aut 108 ; septième Aut 162 ; huitième Aut 108) | C | work/spreadfree_243_2026-10-12/NOTE_SPREADFREE.md:126-172 |
| L06-131 | Un srg(243,22,1,2) avec un groupe abélien élémentaire semi-régulier d'ordre 81 est BvLS, Gamma4 ou Gamma5 | S | work/spreadfree_243_2026-10-12/NOTE_SPREADFREE.md:99-124 |
| L06-132 | Un srg(243,22,1,2) contenant un graphe de Hamming plié H(5,3)/<11111> induit sur 81 sommets est l'un de exactement sept graphes | E | work/spreadfree_243_2026-10-12/NOTE_SPREADFREE.md:305-333 |
| L06-133 | Un srg(243,22,1,2) contenant une droite de BvLS avec ses 60 voisins attachés comme dans BvLS est BvLS ou le twin | E | work/spreadfree_243_2026-10-12/NOTE_SPREADFREE.md:343-348 |
| L06-134 | Descente sous le bloc : 63 sommets gardés forcent le bloc ; échelon 54 : seulement la famille connue | E | work/spreadfree_243_2026-10-12/NOTE_SPREADFREE.md:414-471 |
| L06-135 | Deux régularités tentantes des premiers exemples à 243 sommets sont FAUSSES | R | work/spreadfree_243_2026-10-12/NOTE_SPREADFREE.md:174-180 |
| L06-136 | Membre asymétrique de srg(243,22,1,2) : aucun trouvé ; portrait-robot | O | work/spreadfree_243_2026-10-12/NOTE_SPREADFREE.md:414-429 |
| L06-137 | Article rank7 : rank_7(A - 3I) est impair et 23 <= rank_7(A - 3I) <= 43 (25 avec un petit calcul) | P | conway99-c1:origin/main:papers/rank7/rank7.tex:21-53 |
| L06-138 | Article s5_2adic : condition 2-adique de non-existence pour les srg (35 entrées ouvertes de la table de Brouwer exclues) | P | conway99-c1:origin/main:papers/s5_2adic/s5_2adic.tex:20-35 |
| L06-139 | Note « A Conway 99-graph, if it exists, is asymmetric » : énoncé conditionnel et ses dépendances | P | strongly-regular-graphs-research:main:papers/conway99_asymmetric/asymmetric.tex:1-8 |
| L06-140 | Manuscrit « no automorphism of order two » (brouillon 2 du 07/10) : une validation de calcul restait à terminer | P | strongly-regular-graphs-research:main:papers/conway99_order2/order2.tex:62-76 |
| L06-141 | Manuscrit « pas d'automorphisme d'ordre 3 » (23/09) : preuve candidate formalisée en Lean 4 | P | strongly-regular-graphs-research:main:papers/conway99_order3/preuve_c3.tex:30-55 |
| L06-142 | Manuscrit « computer-free proof : no automorphism of order seven » (octobre 2026) | P | strongly-regular-graphs-research:main:papers/conway99_order7/order7.tex:55-70 |
| L06-143 | L16 : P <= 1151 (condition de Krein sur les droites) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:42-46 |
| L06-144 | L20 / L20 bis : k >= 6 puis k >= 8 (à la main), avec k = rank_7(A - 3I) - 15 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:124-132 |
| L06-145 | L21 : rank_7(A - 3I) sur la boule d'une droite = 2 + rank_7(A_G(L) - 3I) ; k >= 23 - d(L) ; une droite générique donne k >= 22 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:139-142 |
| L06-146 | L22 : k <= 28, i.e. rank_7(A - 3I) <= 43 (genre de Lambda_-4, formule d'oddité) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:160-163 |
| L06-147 | L23 : une droite de boule à d(L) = 1 a disc = tau(G(L)) ; (tau/7) = +1 => k >= 24 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:164-169 |
| L06-148 | Point de Hamming : 18 <= k <= 26 (notes/103), puis L8 démontré : pas de point de Hamming (notes/105) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:170-181 |
| L06-149 | F10 / L25 : un tissu de 11 grilles à couplages tous anti donnerait un plan projectif d'ordre 10 (exclu par Lam) ; tissus à couplages purs exclus | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:192-199 |
| L06-150 | L11 : g(x) <= 17 grilles par sommet (comptage des fentes) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:212-218 |
| L06-151 | Sigma_L c_4(G(L)) = S + 3P et Sigma_L c_3(G(L)) = 2P ; à P = S = 0 maille >= 5 partout, profils (4,4,4) et (4,8) exclus, reste (6,6) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:395-410 |
| L06-152 | Sous NT (pas de torsion équilibrée) : k >= 20, k >= 22 à P = 0 ; à k = 22 sans droite générique, toute droite est non connexe ((6,6) partout si de plus P = S = 0) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:447-454 |
| L06-153 | Méthodes 7-adiques de C1 transposées à C2 (« q:7 ») : g- in {16, 18, 20} | E | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:521-566 |
| L06-154 | H + 3P = 213 444 (hexagones induits) : théorème de Reimbayev retrouvé | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:341-342 |
| L06-155 | Littérature après le 25/09 (lue, non auditée) : rien pour le rang 37 ; le théorème 3.4.3 de Keramatipour a une preuve omise | H | work/c1_theta_lp_2026-10-07/NOTE.md:1747-1763 |
| L06-156 | Tout rang contient des paires de type rang 43 ; seul b_4 de M sépare le rang 37 du rang 43 | P | work/c1_theta_lp_2026-10-07/NOTE.md:1313-1317 |
| L06-157 | Triangles lointains d'un prisme : au plus 12 ; au plus 6 jumeaux ; 4 tau <= 12 P et 4 tau <= Phi | P | work/c1_theta_lp_2026-10-07/NOTE.md:973-976 |
| L06-158 | La positivité du recensement aux ordres 11 et 12 ne coupe ni les jumeaux ni P | E | work/c1_theta_lp_2026-10-07/NOTE.md:977-983 |
| L06-159 | 9-ensembles 2-dégénérés à 14 arêtes : famille injective d'au moins ~1 million de vecteurs de norme 8 par signe | H | work/c1_theta_lp_2026-10-07/NOTE.md:891-894 |
| L06-160 | Sans grille, toute solution entière de (A - 3I) y = 1 a norme >= 15 | P | work/c1_theta_lp_2026-10-07/NOTE.md:3497-3502 |
| L06-161 | Le complément de srg(99,14,1,2) a les paramètres du graphe des points d'une pg(21,3,18), qui ne peut exister | P | work/c1_theta_lp_2026-10-07/NOTE.md:3509-3510 |
| L06-162 | Plancher de coût « rang 37 par droites » ; correction : avec les droites à torsion testées, tout échec d'étoile exclurait le rang 37 | H | work/c1_theta_lp_2026-10-07/NOTE.md:3511-3517 |
| L06-163 | Pas d'inégalité de comptage uniforme pour les étoiles ; idée « énergie d'apex > 37/12 » réfutée | R | work/c1_theta_lp_2026-10-07/NOTE.md:2441-2455 |
| L06-164 | Sur-énoncés de LAB sur la route des étoiles, retirés après l'échange avec Codex (note 218) | X | work/c1_theta_lp_2026-10-07/NOTE.md:2556-2574 |
| L06-165 | Les trois routes de C2 relues ; ce qui se transpose à C1 | H | work/c1_theta_lp_2026-10-07/NOTE.md:2643-2664 |
| L06-166 | Route de réserve « pas de grille » : sans les indicatrices de 9-ensembles, le plancher n'atteint pas le plafond | H | work/c1_theta_lp_2026-10-07/NOTE.md:2730-2746 |
| L06-167 | Les traces (moments) des étoiles sont automatiques : toutes découlent de N N^T = K | P | work/c1_theta_lp_2026-10-07/NOTE.md:3177-3194 |
| L06-168 | Route « quatre normes » (14, 16, 18, 20) au rang 37 : un cas fermé (N14), trois au moins aussi coûteux que le balayage refusé | H | work/c1_theta_lp_2026-10-07/NOTE.md:3897-3911 |
| L06-169 | Retraits de 17.97 : « des dizaines de millions de mondes de norme 16 », « des années d'un coeur », « une cellule n'est pas tuée seule » | X | work/c1_theta_lp_2026-10-07/NOTE.md:3954-3966 |
| L06-170 | Correction de deux nombres de 17.94 (monde de norme 14) : rangs de Seidel 8 et 22, radical de dimension 5 | X | work/c1_theta_lp_2026-10-07/NOTE.md:4138-4143 |
| L06-171 | Rigidité locale des quadrangles en petite valence (SAT local) | S | work/c1_theta_lp_2026-10-07/RECHERCHE_B_REALISATION_GLOBALE.md:240-245 |
| L06-172 | Cycles de transport comme géodésiques par réflexions : aucune loi universelle sur les périodes | E | work/c1_theta_lp_2026-10-07/RECHERCHE_B_REALISATION_GLOBALE.md:318-337 |
| L06-173 | Question S3 à 243 sommets : problème local en un sommet, types A et B, conséquences globales G1-G3 et (D) | S | work/s3_question_2026-10-12/NOTE_S3.md:77-136 |
| L06-174 | Échanges (trades) entre deux srg(243,22,1,2) : critère de support, épaisseur, rigidité du voisinage fermé (Whitney) | P | work/spreadfree_243_2026-10-12/NOTE_SPREADFREE.md:40-69 |
| L06-175 | L18 (seconde variable libre de Reimbayev), L19 (forme de Smith 7-adique de U_x), L19 bis (k >= 2) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:59-64 |
| L06-176 | L7 à la main (point de Hamming + sigma_x in Aut impossible) ; lemme du triangle (e <= 12) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:103-107 |
| L06-177 | Routes closes de septembre (C1) : Hodge / Sigma nu^3, Minkowski, Akiyama, voie 7-adique par sous-matrices déterminées, statistiques de holonomie | H | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:31-41 |
| L06-178 | Astra (rapporté) : un unique revêtement de degré 4 de K_7 à lambda = 1 ; la branche « factorisation de Heawood » du Fano tendu force P >= 24 | E | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:303-311 |
| L06-179 | Astra (rapporté) : P-Psi + admissibilité + identités de bloc ont une solution ; outil des bornes ordonnées | P | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:322-336 |
| L06-180 | Plafonds de référence de Codex au rang 37 (notes 194 et 196) : b_4 <= 15 975 390,7 puis 15 972 863,3 ; couplé <= 16 851 675,0 | E | work/c1_theta_lp_2026-10-07/NOTE.md:1256-1258 |
| L06-181 | Plafonds au rang 37 qui reposent sur le cap flottant a_7 <= 842 (ou dont l'exactitude n'est pas précisée) | H | work/c1_theta_lp_2026-10-07/NOTE.md:1010 |
| L06-182 | L20 ter : k >= 10, i.e. rank_7(A - 3I) >= 25 (assisté par ordinateur) | E | C:/home/researcher/Desktop/Recherche_Conway/c1-norm16-export/JOURNAL.md:133-137 |

## 4. Routes fermées, et pourquoi

1. **Côté valeur propre 3** (réseau pair de rang 60) et 3-côté pour les grilles et les jumeaux : faisable partout, marges de
   10^12 à 10^16 ; « Do not retry », « Closed » (L06-011, L06-034).
2. **Programme theta_pi** (rang 52, vecteurs de sommets) : plus faible que L1 (L06-012).
3. **Quartiques harmoniques** (sommets, puis sommets et droites) : aucune exclusion, même exactement sur les 64 coins (L06-033).
4. **Coupes de sommes de carrés** sur le recensement : aucune valeur propre négative (L06-061).
5. **Positivité du recensement aux ordres 11 et 12** pour les jumeaux et P : aucune coupe (L06-158) ; aucune
   congruence dans le recensement (L06-062).
6. **Comptage des collisions au rang 37, supports <= 9** : clos sur les trois comptabilités (paires k = 2 sur la collection
   de Codex, sans prisme k = 1, pool avec liens) ; côté plafond épuisé ; même sans grille, court de 21 % ; avec N14, court
   de 13 à 15 % (L06-046, L06-058, L06-060).
7. **Canaux de masses 7 à 9 bornés par une charge par support** : 20 à 35 fois trop grand ; seule une borne sur le nombre de
   PAIRES de supports de même projection aiderait (L06-056).
8. **Route des graines** (multiplicités par graine aux normes 18 à 24) : close comme méthode (deux, puis trois vecteurs de
   norme 18 par graine localement faisables) (L06-063).
9. **Comptage de dimension avec les seules relations de pinceau** : cible fausse (relations à un sommet) (L06-050).
10. **Grams autour d'un seul sommet** : ne peuvent exclure aucun des rangs 37, 39, 41 (plafond local 14, hyperbolique)
    (L06-069) ; **tests de Gram abstraits sur une étoile** : ne peuvent fermer (L06-077, L06-078).
11. **Inégalité de comptage uniforme pour les étoiles** : réfutée (équidistribution) (L06-163, L06-079).
12. **Loi exacte des holonomies sur toutes les marches** : fausse (produits) ; sous-lemme omega = 0 en diamètre deux abandonné
    (L06-110).
13. **Sur-réseaux d'indice 7 / enveloppe presque unimodulaire au rang 37** : redonnent seulement a_7k >= b_k ; route C de C2
    non transposable (rang 46 sans classification) (L06-034, L06-165).
14. **Tests sur les 174 coeurs** (fermeture forcée, second niveau, croisement avec le recensement, unions de noyaux de
    quadrangle) : aucune mort, aucun effet (L06-106, L06-108).
15. **Cycles de transport longs** : « Je ferme cette piste ici » (RB:410-413) ; aucune loi sur les périodes (L06-172).
16. **Test spectral du monde de norme 14** : pas un pré-filtre utile (L06-093).
17. **Branche co-Heawood sans rang par énumération** (~3e22 secondes lignes par base) et **monde de norme 18** :
    hors de portée (L06-099, L06-098) ; route « quatre normes » : trois cas sur quatre aussi chers que le
    balayage refusé (L06-168).
18. **Balayage de toutes les boules de droites** : refusé par l'utilisateur ; calculs arrêtés le 09/10 à 05:08 UTC
    (NOTE:3229-3239, 3681-3683).
19. **Gram des droites (triangles)** : reformulation des coupes de sommets (L06-119).
20. **Conditions mod 3 et mod 5 sur une droite à six grilles**, positivité de 7 Pi autour d'une telle droite : automatiques
    ou sans effet (L06-053 ; NOTE:2120-2121).
21. **Invariants de Hasse aux premiers autres que 7** : toujours satisfaits (L06-117).
22. **Route de réserve « pas de grille » sans les 9-ensembles** : le plancher n'atteint pas le plafond (L06-166).
23. **Moments des étoiles jusqu'à tout ordre** : automatiques (L06-167).
24. **Routes de septembre** (JOURNAL) : Hodge / Sigma nu^3, Minkowski, Akiyama, voie 7-adique par sous-matrices déterminées,
    statistiques de holonomie (L06-177).
25. **Biplan minimal à 243 sommets** : absent ; les exemples ne décident pas le cas de norme 14 (L06-101).
26. **Recensements symétriques à 243 sommets** : arrêtés à la demande de l'utilisateur (le but est l'asymétrie) (SF:416-419).

## 5. Questions ouvertes, classées par levier

**Levier arithmétique (réseaux L1, M, vecteurs courts).**
- N16 et N18 au rang 37 (catalogue des mondes de norme 16 incomplet ; mondes de rang de Seidel 32 et 31 non écrits) ;
  borne par graine c_20 <= 4 pour la norme 20 (L06-104, L06-094).
- Borne supérieure sur b_2 (vecteurs de norme 4 de M non triangulaires) : ~2480 nécessaires à l'optimum du rang 37 ;
  < 968 exclurait le rang 43 (L06-045, L06-026, L06-028).
- Borne supérieure de quelques 10^5 sur les vecteurs de norme 26 de L1 (L06-045).
- Existence d'une 22-coclique ; classification de f(n) <= 4 dans son réseau à r = 43 (L06-027, L06-029).
- Rang 43 : « only the frame can exclude this rank » (L06-026).
- Borne inférieure de min Lambda_3(T) pour une droite connexe (L06-118).

**Levier comptage et collisions (rang 37).**
- Borne sur le nombre de paires de supports de même projection (masses 7, 8, 9 ; changements de somme) (L06-056).
- Support 10 : constantes de (5,5) et (8,2), pool et liens ; recensement d'ordre 11 (formes (7,4), (10,1)) (L06-046).
- tau total < ~540, ou C total < 17,1 M (L06-049).
- Borne inférieure sur le rang des systèmes de classes (grilles et différences jumelles) en dimension 18 sur F_7, comptant
  TOUTES les relations indépendantes (L06-050, L06-048).

**Levier structure locale du rang 37 (cas d'égalité).**
- (a') uniforme : l'étoile complète est impossible pour toute boule générique à k = 22 ; NT ; exclusion de « toute droite
  déconnectée » par des rangs exacts mod 7 (L06-067).
- Interdire les motifs forcés A et B pour toute boule (L06-076).
- Graphes Xi_v possibles ; un prisme non-grille peut-il avoir deux jumeaux ; g(l) <= 3 ; partie lignes de la droite à six
  grilles (L06-040, L06-052).
- Famille couvrante forçant une droite de type rare (L06-081).

**Levier sans rang (structures obligatoires).**
- 174 coeurs : quatre autres noyaux obligatoires le long des cycles d'arêtes croisées (relation de transition)
  (L06-108).
- Loi des quadrangles c(Q) = somme des c_e (conjecture) (L06-110).
- Cycle de transport de longueur quatre forcé ? réalisation des cinq bords ; injectivité de H -> h_H (L06-114).

**Levier calcul (coûts connus, non lancés).**
- Boules à torsion du profil (4,8) (16 516 représentants ; rang 1 arrêté à 2792/15 462) ; vérification complète
  d'isomorphisme jamais lancée (L06-089).
- Générateur exhaustif des 1,4e10 types connexes ; modèles des boules à torsion et déconnectées ; audit du modèle de LAP
  (Codex n'a audité que la partie maille 5) (L06-082).
- 213 survivants cycliques à certifier (~30 min, au-dessus de la règle des cinq minutes) (NOTE:2309-2310).
- Run étiqueté complet de N14 (~6 h) et audit par une autre session (L06-092).

**Levier 243 sommets.**
- Ré-implémentation indépendante de l'encodage S3, calcul d'orbite, passage final (L06-128).
- Membre asymétrique de srg(243,22,1,2) ; groupes non abéliens d'ordre 81 ; Z_9 x Z_3^2 ; fenêtres < 50 sommets (L06-136).
- « Pas de carré alternant » et (P) (L06-120).

## 6. Contradictions et corrections (qui dit quoi, quand)

1. **Attribution des notes de septembre du dépôt C1** : le JOURNAL (24-26/09, JOURNAL:25 « Claude Code a coupé les boucles
   d'attente ») est écrit par la session « C1 » ; NOTE (09/10, NOTE:3085-3087) attribue la note 102 (L23) et les notes
   124-127 à « Codex », et aussi les notes 103, 105, 108 (point de Hamming, L8, L11 : NOTE:1203-1204, 1794-1795).
   Concerne L06-147, L06-148, L06-150, L06-066, L06-067. À recouper par les lots L05, L09, L10.
2. **Distinction des vecteurs de 17.3** (LAB, 08/10 01:05) vs **correction de Codex** (01:15) : les énoncés « rho >= 43 ou 44,
   P >= 492 » ne tiennent que sans prismes jumeaux (NOTE:583-595) (L06-020).
3. **17.22(b)** (10:05) vs **17.26** (11:15) : les chiffres 22,87 M / 15,43 M / « 5,7 M de marge » ne chargeaient que (4,4) et (5,2)
   (NOTE:1146-1154).
4. **17.27, 17.41, 17.42** vs **17.44** (14:47) : collections différentes ; puis **17.44** (« closed ») vs **17.45** (15:00 :
   « diagnostic flottant, pas un énoncé ») (L06-047, L06-046).
5. **17.32** (12:15) vs **17.34** (12:20, Codex) : comptes de graines trop optimistes (L06-063).
6. **17.50** (16:25) vs **17.51** : cible « au plus 10 relations » fausse (L06-050).
7. **17.53** (17:50) vs **correction de Codex** (~18:10) : « >= 114 relations non locales » faux ; b(F_v) <= 2 corrigé en <= 1
   (L06-070).
8. **17.62** (20:42) vs **17.63** (20:51) : observation 4 retirée, règle algorithmique réfutée (NOTE:2526-2534).
9. **17.64** : sur-énoncés de LAB retirés après l'échange avec Codex (L06-164).
10. **17.73 A** (23:39) vs **17.74** (23:55) : « attendu bien sous la marge » sans fondement (L06-057).
11. **17.85** (10:40, 09/10) vs **17.86** (12:28) : loi exacte fausse (L06-110) ; RB sect. 9 vs RB sect. 11 idem.
12. **17.88** (20:29, 09/10) vs **17.89** (20:35) : même erreur de collection que 17.44, commise une seconde fois (L06-058).
13. **17.90** dernier point vs **17.93** (22:32) : « le balayage ne se termine pas en exclusion » faux comme énoncé général
    (L06-162, L06-081).
14. **17.94** (23:16) vs **17.101(0)** (12/10) : rangs de Seidel 7/21/6 corrigés en 8/22/5 (L06-170).
15. **17.97** (00:33, 10/10) vs correction de 00:40, **17.99** et **17.101(5)** : nombre de mondes de norme 16 inconnu ; les
    cellules meurent ; les ensembles complets de doubles de norme 18 existent par millions (L06-169, L06-098).
16. **Précision après 17.98** (574 dépendrait de lignes non auditées) vs **17.100** (574 obtenu avec les lignes auditées)
    (L06-031).
17. **17.26(a)** vs correction de LAP (11:50) ; **17.27** : Codex corrige « tous les jumeaux du point de grille sont des
    différences de grilles » ; **17.31** : Codex corrige la « fenêtre » de C (NOTE:1167-1169, 1219-1221, 1299-1303).
18. **TR** : la coupe G_S <= 21 I annoncée comme nouvelle puis rétractée (message 596) (L06-119).
19. **SF:95-97** (« nombre pair de parallèles », observation) vs **SF 6b** (faux dans le huitième graphe) (L06-135).
20. **S3 sect. 13** (« to be verified before it is called a theorem ») vs **sect. 15** (DRAT vérifié) : cohérent, la réserve
    sur l'encodage demeure (L06-128).
21. **COUT** : « environ 14 % » de boules à torsion (COUT:73) contre « 15 % » (COUT:92) : écart mineur.
22. **NOTE 17.78** : LAB écrit d'abord « 20 000 » à LAP sans l'avoir calculé, corrigé (5076) au message suivant (NOTE:3047-3048).
23. **JOURNAL** : corrections internes successives (notes/123 réécrite : identités déjà connues ; notes/125 : correction
    d'une correction sur la maille) (JOURNAL:351-354, 405-410).
24. **rank7.tex** (07/10 : 23 <= r <= 43) vs **NOTE** (08/10 : r >= 37) : pas une contradiction, la borne inférieure de
    l'article est dépassée (L06-137).

## 7. Redécouvertes (un même résultat établi deux fois)

1. **L23** : session C1 / note 102 (25/09, JOURNAL:164-169) ; LAB le 09/10 à 03:44 UTC par la formule d'oddité (NOTE 17.80,
   signalé à 03:49 : recherche en anglais sur des notes en français) ; LAB de nouveau le 09/10 vers 21:31 par les invariants
   de Hasse (RD:39, signalé) (L06-147, L06-083, L06-117).
2. **Fenêtre des rangs** : r >= 37 par LAB les 07-08/10 ; re-dérivation plus faible (r >= 35) la nuit du 14/10 sans consulter
   le programme du 07/10 (`work/c1_night_2026-10-14/NOTE_NIGHT.md:350-352, 606-609`, lot L07) (L06-024).
3. **P <= 852** : Codex (11088/13) et LAB (852,92, flottant, « found here independently », 08/10) ; re-vérifié exactement le
   18/10 (`work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:211-245`, lot L08) (L06-038).
4. **Recensement de Codex** reproduit par census2.py (08/10) (L06-036) ; **1403** de Codex reproduit (NOTE:1928) ;
   **cinq coeurs de norme 16** de Codex retrouvés par cores1820.py (L06-096) ; **373 -> 310** re-dérivé indépendamment
   (L06-105) : réplications indépendantes (voulues).
5. **Identité réelle de LAP** (17.57, 08/10) « retrouvée ici indépendamment » pour les filtres de star37d (COUT:35-37, 09/10)
   (L06-084).
6. **« L'étoile complète meurt avec les valeurs de Green seules »** : septembre (`logs/star_ablation_astra.log`) puis 17.61
   (08/10) (L06-075).
7. **Spectre du graphe lointain d'une droite** (note 114 de Codex) et **droites comme vecteurs** (LAP sect. 10.1, 14.4) :
   re-dérivés à la main par LAB le 09/10 avant d'être trouvés dans les journaux (NOTE:3480-3496).
8. **H + 3P = 213 444** = théorème de Reimbayev, retrouvé par C1 le 26/09 (L06-154) ; **Makhnev 1988 = L1** (JOURNAL:97-98) ;
   **Thm 3.4.2 de Keramatipour = Makhnev** (L06-155).
9. **Prismes jumeaux à mêmes sommets de barreaux** : « probablement déjà contenu dans le théorème de structure du 8 octobre »
   (L06-113).
10. **574 vecteurs de norme 20** : LP de LAP et LP exact de LAB (L06-031).
11. **Monde de norme 14 = branche « deux cocliques de Hoffman se coupant en 15 »** : LAB au rang 37 (10/10, N14) et Codex sans
    rang (12/10) (L06-100).

## 8. Résultats remplacés ou retirés

- Bornes de rang : r >= 29 / 33 (sect. 3) -> r >= 35 (sect. 9) -> r >= 37 (17.11) ; rank7.tex (23 / 25) et L20 (k >= 6, 8, 10)
  dépassés ; bornes de septembre sous NT (k >= 20, 22) dépassées pour la fenêtre (obtenue sans NT).
- a_7 : 7920 -> 990 -> 842 (flottant) -> a_7 + 13 rho <= 2013 (Codex 199) -> a_7 = 0 au rang 37 (N14, non audité) ;
  b_1 : 3784 -> 88 -> 78 (LAP) -> 44 (Codex) ; a_8 : 90 090 -> 27 720 -> 6930 ; b_3, b_4, tau : voir L06-025,
  L06-042.
- Retirés (statut X) : L06-020, L06-047, L06-057, L06-058, L06-164, L06-169,
  L06-170 ; réfutés (R) : L06-050, L06-110, L06-163, L06-135, L06-120
  (pour l = 5), L06-122 (conjecture de Reimbayev).
- **Bug OR-Tools du 18/10** : la portée publiée (`work/scratchpad_LAB_2026-09-30/files/codex_27ac387d/notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt` :
  `root_component_rotated_gram.py`, pilotes c3, registre c4) ne cite aucun résultat de ce lot. Les calculs de ce lot qui
  utilisent OR-Tools CP-SAT (lemme « deux solutions » et table de commutation de srg243_second ; modèles locaux de LAP ;
  pilotes UNKNOWN de 17.47, 17.53) n'ont pas été ré-examinés ici vis-à-vis de ce bug.

## 9. Notes lues, survolées, non lues

**Lues en entier** : NOTE (4240 lignes) ; RB (464) ; COUT (107) ; RD (62) ; S3 (343) ; SF (481) ; NG (42) ; TR (74) ; BP
(README 60, RESULT 40, OUTPUT 23) ; LAPR (47) ; DI (932) ; JOURNAL (607) ; rank7.tex ; s5_2adic.tex ; srg243_second.tex ;
papers/README.md ; asymmetric.tex ; message de Codex `RECOVERY_2026-10-12/.../codex_20261012_coheawood_rank16.txt`.

**Survolés** : order2.tex (résumé, introduction, lignes de statut) ; preuve_c3.tex (titre, résumé, énoncés) ; order7.tex
(résumé, début de l'introduction) ; sorties lues : certificates_N84_check.txt, certificates2_N84_check.txt,
OUTPUT_ladder_N84.txt, OUTPUT_identity_N40.txt, OUTPUT_forced37_N84.txt, OUTPUT_cert35_N84.txt,
OUTPUT_fano37_exhaustive_nodisc.txt (début et fin), OUTPUT_n16cell_tight_survivor.txt (fin), les cinq petites sorties de
`work/coheawood_2026-10-12/`, journaux du balayage de torsion (comptes : 346 parties, 2792 boules mortes) ; quatre copies
d'OUTPUT comparées entre le dossier de travail et conway99-c1 : identiques aux fins de ligne près.

**Non lus, avec la raison** :
- environ 120 autres `OUTPUT_*.txt` de `work/c1_theta_lp_2026-10-07/` et leurs copies LF dans conway99-c1 (sorties de
  programmes résumées par NOTE section par section ; non relues une à une) ; `balls/potentials_ball12_comparison.txt`,
  `balls/radial_exact_cyclic241_t2_sample.txt` (résumés en NOTE 17.56) ;
- 11 sorties `OUTPUT_star37*_*.txt`, `OUTPUT_fano37_controls.txt`, `OUTPUT_fano37_pilot_seed2.txt`,
  `OUTPUT_n16cell_two_worlds.txt` de `work/c1_cost37_2026-10-09/` (résumées par COUT et NOTE 17.92, 17.95, 17.99) ;
- données : `work/coheawood_2026-10-12/bases_orbits.txt` (2,1 Mo), `cores18/core_*.txt` (26 fichiers),
  `work/c1_lap_reps48_2026-10-09/{act22_c.txt, act48.txt, types_m4_p0.txt, reps48*.txt}`, `commands_48*.txt`,
  `sweep_48_torsion.txt`, journaux de pool ;
- deux fichiers de télémétrie CP-SAT de Codex (`c1-asymmetry-audit/data/codex_coheawood/telemetry/*.txt`) : statistiques
  de workers, aucune affirmation ;
- PDF (rank7, s5_2adic, srg243_second, asymmetric, order2, preuve_c3, order7) : compilations des .tex lus ou survolés ;
- `work/scratchpad_LAB_2026-09-30/files/notes_codex_coheawood-hoffman-20261012.txt` et `notes_lab_biplane243-2026-10-07.txt` :
  simples listes de noms de notes (débuts lus) ;
- `work/c1_cores_sat_2026-10-09/` : ne contient qu'un `__pycache__` (les scripts sont dans conway99-c1, sans note) ;
- journaux d'exécution et données des dossiers `s3_question_2026-10-12/` (`drat_trim_main_2026-10-13.log`,
  `ultimate_core_2026-10-13.cnf`), `spreadfree_243_2026-10-12/` (`census_common_third_2026-10-13.log`,
  `staged54_2026-10-13.log`, fichiers `.edges` et `.g6` des graphes), `c1_triangles_2026-10-13/` (`fx_test_2026-10-13.log`,
  `square_pattern_2026-10-13.log`) : non lus (leurs résultats sont résumés dans les notes ; hors inventaire des notes) ;
  scripts `.py`, `.c` et exécutables : non lus (ce sont des programmes, pas des affirmations) ;
- autres versions de NOTE.md rangées au lot L05 (c07012e0, 363 140 octets, branche lab/theta-lp de c1-codex ; db092f4b et
  cad1051c, ~80 Ko, versions précoces) : non lues ;
- sources citées par NOTE mais hors lot (notes 165 à 260 de Codex, dépôt conway99-c2-aws de LAP, conway99-structures-lab,
  THEOREM_Z3_COVERS.md) : non ouvertes ; leurs énoncés sont recopiés tels que NOTE les rapporte.
- Le message de Codex (L06-100) est lu dans `Desktop/Recherche_Conway/RECOVERY_2026-10-12/snapshot_20261012T113936Z/bridge/messages/` :
  il est inscrit au lot ; le dossier s'appelle `bridge` (instantané de récupération), pas `claude-codex-bridge` ; à confirmer
  par le coordinateur si ce dossier doit être traité comme interdit.
- Remarque d'inventaire : NOTE_S3.md, NOTE_SPREADFREE.md, NEW_GRAPHS et NOTE_RESEAUX_DE_DROITE.md sont rangés par
  l'inventaire dans les lots L05 / L08 (première copie dans une branche Codex ou d'exploration) ; ils sont traités ici
  comme demandé, d'où un recouvrement possible.

## 10. Matériaux pour la recombinaison

Format fixe, une ligne par élément, pour le croisement automatique. Statuts : ceux de la source. « id » renvoie au jsonl.

### 10.1 Énoncés conditionnels « si X alors exclusion »

- [COND-01] SI L1 n'a aucun vecteur non nul de norme <= 20 ALORS r != 37 ; SI aucun de norme <= 24 ALORS r ∉ {39, 41} ; SI aucun de norme <= 26 ALORS r != 43 | statut : C | source : NOTE:67-70, OUTPUT_ladder_N84.txt | id : L06-007
- [COND-02] SI L1 contient k vecteurs dont la matrice de Gram est inversible mod 7 ALORS r <= 45 - k | statut : P (énoncé de la note) | source : NOTE:252-254 | id : L06-035
- [COND-03] SI 2 a_8 + 16 a_9 + a_13 < 329 (7^m + 1) + 7^(m+1) b_1 + 7 a_7 + 7 a_10 + 2 a_11 + a_12 (m = (45-r)/2) ALORS le rang r est exclu ; avec a_8 <= 6930 : SI 16 a_9 + a_13 < 776 398 (r = 37), < 99 316 (r = 39), < 2 590 (r = 41) ALORS exclu | statut : C | source : NOTE:353-366 | id : L06-015
- [COND-04] SI a_9 = a_13 = 0 ALORS a_8 >= 395 129 (r = 37), 56 588 (r = 39), 8 225 (r = 41), contre a_8 <= 6930 : donc aux rangs 37, 39, 41 il existe un vecteur de L1 de norme 18 ou 26 ; à r = 43 un de norme 18 ou 26 ou au moins 1316 de norme 16 | statut : C | source : NOTE:4229-4234 | id : L06-103
- [COND-05] (r = 43) SI 2 a_8 + 16 a_9 + a_13 < 2632, OU b_2 < 922, OU b_3 < 6 696 790 ALORS r = 43 exclu ; comme b_2 >= 968 est forcé (Codex), SI b_2 <= 967 est prouvé à r = 43 ALORS r = 43 exclu | statut : C (formules) + P (968) | source : NOTE:1032-1041, 1074-1079 | id : L06-026, L06-028
- [COND-06] (r = 37) SI le nombre b_4 de vecteurs distincts de norme 8 de M dépasse 15 196 716 à rho = 126 avec b_3 >= 45 964 (note 204), OU b_4 + (651/34) b_3 > 15 457 549 + (450359/272) a_7 (note 199) ALORS r = 37 exclu | statut : C (certifiés par Codex) | source : NOTE:1514-1516, 1974-1977 | id : L06-044 ; variantes : b_4 > 15 972 863,3 ou b_4 + (651/34) b_3 > 16 851 675,0 (notes 194, 196, certification non précisée : E, L06-180) ; plafonds sous le cap flottant a_7 <= 842 (H, L06-181)
- [COND-07] (r = 37, what-if exact) r = 37 infaisable SI b_4 >= 18 M seul, OU (b_3 >= 150 000 ET b_4 >= 15 M), OU (b_3 >= 300 000 ET b_4 >= 12 M), OU (b_3 >= 600 000 ET b_4 >= 6 M), OU b_3 >= 900 000 seul (avec a_7 <= 990, b_5 >= 33 224 268) | statut : H (« what-if, not results ») | source : NOTE:674-678 | id : L06-025
- [COND-08] (r = 37) SI le nombre total C de paires en collision (tous canaux) < 17,1 M ALORS r = 37 exclu ; suffisant : 27 828 tau_g + 31 976 tau_n + (canaux hors C6) < 17,1 M (ex. tau_g < 614 sans paire non-grille ; tau_n < 535 sans grille ; tau_g <= 347 (rho <= 30) avec tau_n <= 232) | statut : H (constante flottante ; caps C) | source : NOTE:1895-1908 | id : L06-049
- [COND-09] (r = 37) SI au plus 10 relations indépendantes mod 7 entre classes de grilles au-delà des relations de pinceau ALORS exclu — cible FAUSSE (relations à un sommet dans tout graphe) | statut : R | source : NOTE:1957-1971, 2032-2039 | id : L06-050
- [COND-10] (r = 37) SI aucune droite n'est dans 4 ou 6 grilles (g(l) <= 3) ALORS tau_g <= 693 et rho <= 115 : environ le facteur nécessaire, sans marge (« necessary-looking, not sufficient ») | statut : H | source : NOTE:1243-1246, 1691-1694 | id : L06-052
- [COND-11] (r = 37) SI chaque classe de M a au plus 2 représentants de support <= 9 (resp. au plus 3 de support <= 10) ALORS exclu ; SI les représentants sans prisme de support <= 10 ont au plus 2 représentants par classe ALORS 20,6 M > 15,2 M, exclu ; « au plus deux par classe » est FAUX dans les pinceaux de >= 3 grilles | statut : H + R | source : NOTE:937-939, 1579-1580, 1639-1645 | id : L06-065
- [COND-12] (r = 37) SI moins de 82 % des représentants sans prisme de support <= 9 sont en collision (10,45 M paires) et les classes ont au plus deux représentants ALORS exclu | statut : H | source : NOTE:1575-1578 | id : L06-065
- [COND-13] (r = 37, route des graines) SI 539·(9240 kappa_18) + 392·(7920 kappa_20) + 147·(5040 kappa_22) + 49·(4620 kappa_24) + (mêmes poids x nombres des autres types : supports avec arêtes, entrée 2, 33-ensembles réguliers, profil (34,1)) < 15 241 977 ALORS r = 37 exclu ; la condition kappa_18 <= 2 et kappa_20 <= 1 environ est seulement NÉCESSAIRE (pas suffisante : a_11, a_12 non bornés) | statut : H ; seuil = minimum exact sous le cap a_7 <= 842, lui-même flottant (avec le seul cap prouvé a_7 <= 990 : ~15,15 M) ; route fermée comme méthode (NOTE:1473-1476) | source : NOTE:1321-1349, 1363-1374 | id : L06-063
- [COND-14] (r = 37, après N14) SI a_8 = a_9 = 0 (N16 et N18 au rang 37) ET au plus 4 vecteurs de norme 20 par graine indépendante (c_20 <= 4 ; c_20 <= 6 si les supports sont indépendants) ALORS r = 37 exclu | statut : C (identité) dépendant de b_3 >= 45 898 (Codex 196) et de N14 (E) | source : NOTE:4096-4104 | id : L06-104
- [COND-15] (r = 37) SI a_13 <= 3·10^5 ALORS b_4 <= 11,0 M (facteur 1,8 sur tau) ; SI a_13 <= 10^6 ALORS b_4 <= 13,4 M — pas une exclusion seule | statut : H | source : NOTE:1304-1308 | id : L06-045
- [COND-16] (historique r = 33, 35) SI a_9 <= 497 122 ALORS r = 33 exclu ; SI au plus 13 configurations de norme 16 par graine ALORS r = 33 sans Fano exclu ; SI deux configurations de Fano distinctes forcent r >= 35 ALORS r = 33 exclu ; SI b_4 >= 4 011 587 ALORS r = 35 exclu ; SI chaque couche 16..26 a < 4,8 M vecteurs ALORS r = 35 exclu — tous dépassés par L06-023 | statut : H | source : NOTE:119-121, 141-142, 167-168, 328-329, 420 | id : L06-006
- [COND-17] SI le graphe a au plus une 22-coclique ALORS il n'a pas de vecteur de Fano | statut : P | source : NOTE:1070-1073 | id : L06-028
- [COND-18] (r = 43) SI deux 22-cocliques se coupent en i points ALORS i ∈ {1, 8, 15} ; (tout rang) i <= 15 | statut : P | source : NOTE:1054-1058 | id : L06-027
- [COND-19] (cas d'égalité r = 37) SI (a') uniforme ET NT ALORS toute droite est déconnectée à k = 22 ; SI de plus « toutes droites dégénérées » est exclu par rangs exacts mod 7 ALORS r = 37 exclu | statut : O | source : NOTE:2059-2072 | id : L06-067
- [COND-20] (r = 37, P = S = 0) SI NT ET (a') uniforme ALORS contradiction : le monde P = S = 0 du rang 37 est vide (maille >= 5 partout à P = S = 0 ; maille >= 5 => connexe au rang 37 (LAP, E) ; connexe non générique impossible sous NT ; (a') tue les génériques) | statut : O (assemblage) | source : JOURNAL:403, 465-469 ; NOTE:2153-2156, 2768-2774 | id : L06-088
- [COND-21] (r = 37) SI toute droite a un graphe G(T) connexe ALORS aucune grille au rang 37 (rho = 0) | statut : P | source : NOTE:2800-2805 | id : L06-087
- [COND-22] (r = 37) SI tous les profils de boules à composante prisme autres que (1^6) sont exclus ALORS rho = 0 | statut : P | source : NOTE:3446-3449 | id : L06-059
- [COND-23] (r = 37) SI rho = 0 est prouvé ALORS, avec les bornes certifiées, AUCUNE exclusion ne suit (seuil 25 201 < 31 976, masses 7-9 non bornées) | statut : H | source : NOTE:3462-3470 | id : L06-058
- [COND-24] (r = 37, what-if) SI a_7 = a_8 = 0 ALORS le seuil sans grille 33 780 dépasse le cap 31 976 — « pas une exclusion » | statut : H | source : NOTE:3838-3843 | id : L06-060
- [COND-25] (r = 37) SI toute boule de tout type (connexe, à torsion, déconnectée) échoue son test d'étoile ALORS r = 37 exclu, sans lemme global | statut : P | source : NOTE:3669-3673 | id : L06-081
- [COND-26] (r = 37) SI une droite connexe sans torsion a tau(G(T)) résidu quadratique mod 7 ALORS contradiction (aucune sélection de 60 ombres binaires valide) ; au rang 37 toute droite connexe a tau ∈ {0, 3, 5, 6} mod 7 ; deux composantes sans torsion : c0 = tau1 tau2 modulo les carrés | statut : P | source : NOTE:3126-3137, 3154-3160 | id : L06-083
- [COND-27] (L23) SI une droite a d(L) = 1 et (tau|7) = +1 ALORS k >= 24 (r >= 39) | statut : P | source : JOURNAL:164-169 | id : L06-147
- [COND-28] (L21) SI une droite a d(L) = 1 ALORS k >= 22 (r >= 37) ; en général k >= 23 - d(L) + 2 r(L) | statut : P | source : JOURNAL:139-142, 425-428 | id : L06-145
- [COND-29] (sous NT) k >= 20 ; SI P = 0 ALORS k >= 22 ; SI k = 22 et aucune droite générique ALORS toute droite est non connexe ; SI NT, k = 22, aucune droite générique ET P = S = 0 ALORS (6,6) partout | statut : P (conditionnel à NT) | source : JOURNAL:465-492 | id : L06-152
- [COND-30] SI le graphe a un point de Hamming ALORS 18 <= k <= 26 ; (L8) il n'en a pas | statut : P | source : JOURNAL:170-173, 200-211 | id : L06-148
- [COND-31] SI un tissu de 11 grilles a tous ses couplages anti ALORS il existe un plan projectif d'ordre 10 avec polarité (exclu par Lam) | statut : P | source : JOURNAL:192-197 | id : L06-149
- [COND-32] SI rank_7(A - 3I) <= 21 ALORS pas de srg(99,14,1,2) (trivial vu la borne inférieure) | statut : P | source : rank7.tex:260-261 | id : L06-137
- [COND-33] (S5) SI r - s a un facteur premier = 3 mod 4 ALORS le critère ne contrôle pas c_q : ne s'applique pas à 99 (d = 7) | statut : P | source : s5_2adic.tex:184-190 | id : L06-138
- [COND-34] (243) SI chaque maillon de la chaîne S3 tient ALORS les srg(243,22,1,2) à spread régulier sont exactement BvLS, twin, Gamma3, Gamma4 | statut : E | source : S3:298-301 | id : L06-128
- [COND-35] (243) SI un revêtement non cyclique de BH existe ALORS c'est un graphe distance-régulier asymétrique | statut : S | source : S3:189-195 | id : L06-125
- [COND-36] (243) SI un srg(243,22,1,2) est asymétrique ALORS il est sans spread régulier, sans Hamming plié induit, sans droite attachée comme dans BvLS | statut : E | source : SF:421-423 | id : L06-136
- [COND-37] (99) SI un srg(99,14,1,2) existe ALORS il n'a pas de spread régulier ; aucune preuve ne peut passer par « tout srg(v,k,1,2) a un spread régulier » | statut : P | source : SF:13-27 | id : L06-129
- [COND-38] (dossier externe) SI les cinq bords de transport de longueur quatre sont non réalisables ALORS tous les cycles de transport de longueur quatre sont exclus (ne ferme pas t_4 = 0) | statut : P (énoncé de cible) | source : DI:776-785 | id : L06-114
- [COND-39] (quadrangle) SI Delta(Q) != 0 ALORS les 44 projections forment une base et le graphe est déterminé par les quatre murs et 51 ombres | statut : P | source : RB:257-262 | id : L06-111
- [COND-40] (parité) SI la loi des quadrangles c(Q) = c_va + c_aw + c_wb + c_bv mod 2 est vraie ALORS une condition d'un bit par configuration à quatre murs et F(T) = F(T') quand T + T' est somme de quadrangles | statut : O | source : RB:314-315 | id : L06-110
- [COND-41] aucun candidat n'a tous ses quadrangles d'holonomie impaire | statut : P | source : RB:98 | id : L06-109
- [COND-42] SI les certificats de Codex pour les 63 + 136 coeurs exclus tiennent ALORS x_58 = x_59 = 0 dans tout srg(99,14,1,2) | statut : E | source : NOTE:2756-2759 | id : L06-107
- [COND-43] (Keramatipour, preuve omise) « pas onze sous-graphes Paley(9) disjoints » : non utilisable tel quel | statut : H | source : NOTE:1759-1761 | id : L06-155
- [COND-44] SI le graphe n'a pas de grille ALORS toute solution entière de (A - 3I) y = 1 a norme >= 15, et norme 15 seulement pour y = 1_P - 1_Q (Q droite, P 12 sommets lointains 4-réguliers) | statut : P | source : NOTE:3497-3502 | id : L06-160
- [COND-45] SI un point a ses 4 lignes de graine deux à deux en grilles et ses 3 autres lignes deux à deux en grilles ALORS aucun vecteur de norme 16 n'y est non nul (lemme N16 de LAP) | statut : P | source : NOTE:1540-1547 | id : L06-064
- [COND-46] SI les sept droites d'un sommet se répartissent en 4 + 3 deux à deux en grilles ALORS les 6 grilles et les 3 grilles satisfont une relation exacte | statut : P | source : NOTE:2014-2019 | id : L06-051
- [COND-47] (droite à six grilles, r >= 37) SI deux points de la droite ont trois lignes hub chacun ALORS le troisième n'en a qu'une ; le motif (2,2,1) est exclu ; « trois apex à trois hubs partageant un indice commun » est exclu ; (r = 39, 41, 43) rung du prisme 0 universel aux trois apex => 21 grilles de rang 18 mod 7, exclu | statut : C (Codex) | source : NOTE:1834-1851, 1871-1878 | id : L06-048
- [COND-48] SI W_1, W_2 sont des moulins pondérés disjoints ALORS u_1 - u_2 n'est pas vecteur propre de valeur 3 ; SI 1_U - 1_V est vecteur propre (U cubique de 8 sommets) ALORS V est une composante de G[Z(U)] | statut : P | source : NOTE:2907-2934 | id : L06-054
- [COND-49] SI deux 8-ensembles cubiques induits ont la même projection ALORS ils sont anticomplets (et réciproquement) | statut : P | source : NOTE:2983-2993 | id : L06-055
- [COND-50] SI f est un vecteur propre entier (-4) de norme 18 ALORS ses deux supports sont indépendants | statut : P | source : NOTE:3972-3982 | id : L06-095
- [COND-51] SI un vecteur propre entier (-4) a une entrée de valeur absolue >= 2 ALORS sa norme est >= 20 | statut : P | source : BP README:52-55 | id : L06-102
- [COND-52] SI deux graines au même sommet s'étendent en vecteurs de Fano ALORS elles partagent au plus 2 voisins | statut : P | source : NOTE:597-606 | id : L06-021
- [COND-53] SI y, z et y + z sont des vecteurs de Fano ALORS contradiction (lemme F) | statut : P | source : NOTE:338-341, 607-612 | id : L06-014
- [COND-54] (243) SI le graphe est BvLS, twin, Gamma3 ou Gamma4 ALORS tout vecteur propre entier (-5) non nul a norme >= 24 | statut : E | source : BP README:34-51 ; NOTE:4201-4207 | id : L06-101
- [COND-55] (BH) toute signature de BH avec toutes les paires séparées est impossible | statut : S (LAB, 0,2 s) ; article Cesarz-Williford lu par l'abstract | source : S3:210-230 | id : L06-126
- [COND-56] (dossier externe) h_H est un vecteur triangulaire SI ET SEULEMENT SI il n'y a pas d'exception et Z_0 est un triangle | statut : P | source : DI:309-317 | id : L06-114

### 10.2 Bornes quantitatives

- [BORNE-01] rang r = rank_7(A - 3I) | impair, 23 <= r <= 43 (25 assisté) | P | rank7.tex:21-53 | L06-137
- [BORNE-02] rang r | r ∈ {37, 39, 41, 43} | C | NOTE:633-655 | L06-024
- [BORNE-03] min L ; vecteurs de L1 hors de L | min L = 14 (Fano) ; hors L : norme >= 22 ; entrée 2 impossible sous norme 28 dans L1 \ L | P | NOTE:13-19, 370 | L06-001
- [BORNE-04] min(L1) | <= 18 / 20 / 24 / 24 / 26 pour r = 35 / 37 / 39 / 41 / 43 (<= 16 à r = 33, historique) | C | NOTE:67-70, 241-242 | L06-007
- [BORNE-05] a_7 (vecteurs de Fano) | <= 7920 ; <= 990 ; <= 3960 (version faible) ; <= (2/21) N(F10) et <= 842 (flottant) ; a_7 + 13 rho <= 2013 (Codex 199) ; a_7 <= 374 à rho = 126 ; a_7 + 4 b_1 <= 990 (LAP, non audité) ; a_7 <= 9h ; a_7 = 2 #{paires de 22-cocliques à 15 points communs} ; r = 43 : a_7 = b_1 <= 88 ; r = 37 : a_7 = 0 (N14, E) | P/C/H/E | NOTE:102-106, 614-617, 954-960, 1514-1517, 923-926, 1070-1088, 3745 | L06-003, L06-021, L06-039, L06-092
- [BORNE-06] a_8 (norme 16) | <= 90 090 ; <= 27 720 ; un par graine : 7 a_7 + 8 a_8 <= 55 440, a_8 <= 6930 ; 7 a_7 + 8 a_8 + 273 b_1 <= 55 440 (LAP : preuves à la main et recherche CP-SAT locale, non auditées, NOTE:923-924) | P | NOTE:131-158, 308-309, 923-926 | L06-004
- [BORNE-07] b_1 (racines de M) | <= 3784 ; <= 88 ; <= 78 (LAP, non audité) ; <= 44 (Codex) ; racines deux à deux orthogonales ; au plus 22 droites de racines | P | NOTE:105, 342-343, 924, 1074-1079 | L06-014, L06-028
- [BORNE-08] b_2 (norme 4 de M) | >= 462 ; >= 462 + 41 b_1 + b_1^2/2 (Codex) ; r = 43 : >= 968 et b_2 = 1000 - 8 a_7 + 25 a_8 + 11 a_9 + 8 a_10 + 3 a_11 + a_12 ; r = 43 sans Fano : >= 538 vecteurs de norme 4 non triangulaires | P/C | NOTE:37, 1038, 1074-1079, 545-547 | L06-026
- [BORNE-09] b_3 (norme 6 de M) | >= 24 948 (audité) ; >= 66 528 - 18P - 72 rho ; >= 43 848 ; 45 528 ; 45 766 ; 45 898 ; 45 964 ; r = 43 : >= 46 000 ; >= 73 920 - 20P - 72 rho - 4 tau (LAP, non arbitré) | P/C | NOTE:38, 515, 689-693, 851-853, 1256-1258, 1378, 1974-1977, 2085-2086, 826-827 | L06-025
- [BORNE-10] b_4 (norme 8 de M, distincts) | >= 388 080 ; >= 1 431 738 ; >= 3 826 746 + 84P - 4572 rho (sans jumeaux) ; >= 3 826 746 + 90P - 4572 rho ; >= 3 826 746 - 30P - 4572 rho (sûr) ; >= 3 826 746 - 792P >= 2 729 034 ; >= 3 371 634 | P/C | NOTE:39, 195, 514, 560, 592, 639, 690 | L06-005, L06-022
- [BORNE-11] b_5, b_6, b_7, b_8 | b_5 >= 196 812 ; >= 17 668 728 ; >= 18 001 368 ; >= 35 123 088 - 168P - 7212 rho (uniformément >= 33 224 268) ; >= 34 087 368 ; b_6 >= 23 272 326 / 86 272 956 ; b_7 >= 5 987 520 / 208 016 424 ; b_8 >= 263 126 556 | P/C | NOTE:40, 207-213, 291-293, 566-567, 675-676, 690 | L06-005
- [BORNE-12] plafonds au rang 37 | certifiés (C, Codex) : b_4 + (651/34) b_3 <= 15 457 549 + (450359/272) a_7 (note 199) ; b_4 <= 15 196 716 à rho = 126 avec b_3 >= 45 964 (note 204) | référence (E, certification non précisée) : 15 975 390,7 / 16 851 675,0 (note 194) ; 15 972 863,3 (note 196) | sous le cap flottant a_7 <= 842 ou d'exactitude non précisée (H) : 16,23 M / 17,15 M (note 189) ; 16 014 183,8 / 16 978 453,3 ; 15 979 604 / 16 950 588,3 ; what-if a_7 = 0 : 14 444 540,6 / 15 409 176,2 ; 16 499 433 (a_7 <= 990, LP LAB) | NOTE:758-761, 1010, 1080-1084, 1256-1258, 1378, 1514-1516, 1974-1977 | L06-044, L06-180, L06-181
- [BORNE-13] nombres forcés au rang 37 | (minima exacts SOUS le cap a_7 <= 842, flottant ; avec le seul cap prouvé a_7 <= 990 la première ligne ne garantit que ~15,15 M) 539 a_9 + 392 a_10 + 147 a_11 + 49 a_12 >= 15 241 976,8 ; 9 a_9 + 10 a_10 + 11 a_11 + 12 a_12 >= 254 504,25 ; ... + 13 a_13 >= 436 723,9 ; a_9 + ... + a_12 >= 28 278,25 ; a_9 + ... + a_13 >= 48 524,9 ; (sans cap sur a_7) 16 a_9 + a_13 >= 776 398 ; (a_7 = 0) a_8 + a_9 + a_10 >= 533/25, a_10 + 7 a_9 + (350/13) a_8 >= 574 ; 350 a_8 + 91 a_9 + 13 a_10 >= 7462 (lignes auditées) et >= 447 412 (avec b_3 >= 45 898) ; a_14 >= 5,0 M | C | NOTE:1321-1335, 1398-1399, 4074-4094 | L06-030, L06-031, L06-032
- [BORNE-14] nombres forcés de vecteurs de L1 de norme <= 2m | tables r = 33..43 (ex. r = 37 : 7 (<=20), 413 (<=22), 16 647 (<=24), 49 392 (<=26) ; r = 43 : 165 (<=26)) | E | NOTE:110-117 | L06-008
- [BORNE-15] P (prismes) | 6 rho <= P <= 1386 ; P <= 1151 (L16) ; P <= 852 (Codex, re-vérifié 18/10) ; P + 5 rho <= 1386 ; 3P + 2H <= 4158 ; (r = 35, historique) P >= 450 | P/C | NOTE:442, 690, 901, 1356, 2813 ; JOURNAL:42-46 | L06-038, L06-143
- [BORNE-16] rho (grilles 3x3 induites) | rho <= 126 (ordre 9) ; g(x) <= 17 grilles par sommet (L11) ; g(Theta) ∈ {0,1,2,3,4,6} ; n_3 <= 39 ; r = 43 : e <= 15 par sommet ; paires de grilles partageant une droite <= (207/17) rho, <= 11 rho + 17 | P/C | NOTE:690, 1165, 1203-1205, 1406, 1878, 2085 ; JOURNAL:212-218 | L06-040, L06-042, L06-150
- [BORNE-17] tau (paires de prismes jumeaux) | <= 5P/2 ; <= 2P + 3 rho ; <= 1890 ; <= 2120 (Phi/4, flottant) ; <= 2048 et <= 4615 (LP flottants, « nothing here is a bound to be used », NOTE:966) ; 4 tau <= 12 P ; 4 tau <= Phi ; 17 tau <= 17P + 105 rho ; <= 1534 ; <= 1403 ; <= P + 5 rho + 17 ; <= 1354 ; r = 43 : <= 1326 ; classe de jumeaux non-grille <= 3 prismes ; au plus 6 jumeaux par prisme | C/P/H | NOTE:589-590, 815-816, 975-979, 990-995, 1170-1179, 1201-1206, 1351-1359, 1406, 1974-1977, 2085 | L06-042, L06-157
- [BORNE-18] H (copies de D / maisons) ; N4 ; Phi | H <= 1867,25 (flottant ; 2079 à l'ordre 9) ; max copies de D à P = 0 : 1867 ; N4 <= 17 325 ; Phi <= 8483,3 (flottant) ; P >= 850 => Phi <= 7514 | H/C | NOTE:902, 2883, 816, 994-995 | L06-038
- [BORNE-19] constantes de collision (Codex) | masse 6 (6,3) : <= 756 tau (norme 6), <= 12 814 tau (norme 8) ; masse 7 : <= 108 Omega, <= 3612 Omega ; constante jointe par paire de grilles ∈ [16 496, 27 828] ; non-grille <= 31 976 (23 150 sans 9-ensembles) ; c(2) = 29 144 ... c(6) = 29 140 ; C6 <= 38 084 490 ; total masse six supports <= 9 <= 40 889 844 ; sans prisme 6992..18 244 (grille), 7034..19 178 (non-grille) ; liens <= 12 674 / 14 426 ; canal 9-ensembles = 5376 + 12 t_Z par paire de grilles ; à P = 0 : masse 7 <= 5402 par D, masse 8 : 1872, 1840, 3088, 3512, 3616, 4448 par support, 2592 par moulin ; masse 9 : coefficients 58 à 1301 | C | NOTE:961-962, 1287-1303, 1448-1471, 1503, 1651-1658, 1974-1977, 2866-2874 | L06-043
- [BORNE-20] comptes de familles (99,14) | N(6,7) = 831 600 + 36P ; N(6,8) = 20 790 - 9P ; N(6,9) = P ; N(6,6) = 8 560 860 - 84P ; triangle - chemin lointain = 731 808 + 12P (- 48 tau) ; bowtie - arête lointaine = B[(v-5k+11)(k-10) + 4(k-6)] + 12P + 2H ; Q8 = 4 108 104 + 468P - 512H + 72 C14 - 12(C13a + C13b + C13c) ; Q6 = 132P + 46H - 8 C14 ; N(5,5) = 332 640 ; 3465 moulins ; H + 3P = 213 444 (hexagones) ; 2-dégénérés à 14 arêtes >= 1 022 353 (flottant) | P/C/H | NOTE:487, 452, 711-713, 723-725, 842-843, 864, 913-916, 2814 ; JOURNAL:341-342 | L06-018, L06-019, L06-154, L06-159
- [BORNE-21] recensement | types par ordre 2..10 : 2, 4, 9, 21, 62, 208, 916, 5311, 42 430 ; 549 paramètres ; supports d'ordre 8 <= 53 465, ordre 9 <= 476 669, ordre 10 <= 8,86 M (flottant) | E/H | NOTE:862, 901-904 | L06-036, L06-038
- [BORNE-22] monde de norme 14 | 800 427 bases étiquetées, 33 508 orbites ; rang de Seidel 36 : 689 967 (28 875 orbites), 35 : 110 460 (4633) ; ~1,9e5 noeuds par recherche ; ~3e22 secondes lignes par base sans rang ; r - 28 coordonnées libres par sommet de bord (9, 11, 13, 15) | E | NOTE:3766-3800, 4156-4158, 4176-4186 | L06-092, L06-099
- [BORNE-23] mondes des normes 16 à 20 | coeurs : 1 / 5 / 26 / 1199 + 182 ; norme 16 : 478 attachements, 71 351 mondes PSD sur cinq attachements d'un coeur ; norme 18 : >= 2 317 413 ensembles complets de doubles dans une tranche, 160 colonnes de sommets triples ; norme 20 : e(D) = e(Z) + 27, doubles non indépendants ; Schur de rang <= 44 - 2m | E/P | NOTE:3873-3887, 3954-3960, 3987-4002, 3922-3947, 4209-4219 | L06-096, L06-097, L06-098
- [BORNE-24] multiplicités par graine | 55 440 graines ; kappa_16 = 1 ; norme 18 lemme A : <= 2 (sous-cas) ; type (1,2,5) <= 12 par graine ; (2,0,6) vide ; a_9 <= 9240 kappa_18 (général) / 6160 c_18 (supports indépendants) ; a_10 <= 7920 c_20 (7 graines garanties) / 5544 c_20 (10 graines, supports indépendants) | P | NOTE:345-351, 1361-1367, 4095-4097 | L06-063, L06-104
- [BORNE-25] dimensions mod 7 | Gram d'une famille de L1 : rang <= 45 - r (8 à r = 37, 2 à r = 43) ; famille du noyau : <= 56 - r (19, 17, 15, 13) ; espace centré de dimension 18 à r = 37 ; espace local hyperbolique de dimension 14 ; espace de Green des ombres de dimension 33 ; classes locales <= n - b(F_v) - 7 ; (6,6) : b(F_v) <= 1, >= 177 relations entières automatiques ; famille de vraie dimension d dans un espace non dégénéré de dimension 19 : rang de Gram >= 2d - 19 et >= d - 9 | P/C | NOTE:1477-1480, 1787-1793, 1938-1948, 2136-2139, 2177-2181, 2210, 2212-2214 | L06-035, L06-069
- [BORNE-26] coûts mesurés | star37d, classe sans prisme : 2,2 ms (entier), 1,26 ms (réel) par boule ; masse des boules 1,87e11 ; toutes les connexes : 1,33 / 0,77 ms par boule, 6,3e10 à tester : 2,7 / 1,5 années-coeur ; boules à composante prisme : (9!!)^3/6 = 1,4e8 ; connexes avec torsion ~2e10, déconnectées ~4e10 ; N14 : 977 s ; balayage (4,8) : 97 896 représentants (81 380 morts, 16 516 à torsion) | E/H | COUT:11-20, 62-85 ; NOTE:3440-3442, 3676-3678, 3792-3793, 3201-3202 | L06-082, L06-089
- [BORNE-27] rubans et quadrangles | cycle de transport propre : longueur 3, 4 ou 5 ; segment propre <= 4 centres ; 2079 quadrangles, 12 par arête ; >= 1715 relations entre 2310 parités ; voisinage d'un quadrangle : 44 sommets ; Delta(Q) carré parfait divisible par 7^(45-r) | C/P | RB:45-50, 247-258, 416-428 | L06-112, L06-109, L06-111
- [BORNE-28] réseaux de droite (Hermite) | pour toute droite connexe : min Lambda_3(T) <= 3,41 (5·7^(2k) Theta/256)^(1/18), min Lambda_-(T) <= 2 (4·7^(2k) tau/9)^(1/8) ; pour les boules TYPIQUES (Theta ~ 1,1e19, tau ~ 2e12) au rang 37 : norme <= 30 (valeur 3), <= 62 (valeur -4) ; rangs 39, 41, 43 : 38, 48, 60 | P | RD:45-51 | L06-118
- [BORNE-29] srg(243,22,1,2) | huit graphes connus (Aut 3 849 120, 4320, 864, 3888, 2916, 108, 162, 108) ; grilles par sommet 55 / 13-19-55 / 23 / 31 / 25 / 17 / 17 / 19 ; Aut(BH) = 233 280 ; <= 40 paires plates par sommet d'un squelette non trivial ; >= 90 paires plates ; H^1 de dimension 460 ; Reimbayev H_0 = 4 980 690 contre 5 000 130 pour Gamma' | E/C/S | NG:10-19 ; S3:30-32, 226-230, 269-271 ; srg243_second.tex:111-119 | L06-130, L06-126, L06-122
- [BORNE-30] dossier externe | det R_H0 = 253 125 ; det R_H1 = 275 625 ; K_H de rang 32 ; triangulaires saturés : 3456 (rang 7), 9408 (rang 8) ; 18 vecteurs de norme 4 dans R_H ; plan de Makhnev det 15, orthogonal rang 42, det 15·7^delta | P/E | DI:33-40, 421-460, 509-534, 576-598 | L06-114
- [BORNE-31] automorphismes | |Aut(Gamma)| divise 2·3^3·7·11 ; sans ordinateur |G| ∈ {1, 2, 11} | P | asymmetric.tex:60, 99-103 | L06-139
- [BORNE-32] septembre (JOURNAL) | k >= 6, 8, 10 (r >= 21, 23, 25) ; k <= 28 ; P <= 1151 ; g(x) <= 17 ; e <= 12 (triangle) ; 0 <= S <= n_3 ; Sigma_L c_4 = S + 3P <= 4158 à P = 0 ; Sigma_L c_3 = 2P ; à k = 18 sous NT : P ∈ [924, 1122], g(x) ∈ [14, 17] ; Sigma_L p_L = (2/3) Sigma g(x) <= P <= 1151 | P | JOURNAL:42-46, 124-137, 160-163, 212-218, 245-252, 59-64, 395-399, 450-451, 519 | L06-144, L06-182, L06-146, L06-143, L06-150

### 10.3 Lemmes ouverts et étapes manquantes (et ce qu'ils donneraient)

- [OUVERT-01] (a') uniforme : pas d'étoile complète pour toute boule générique à k = 22 | donnerait avec NT : toute droite déconnectée au rang 37 (et avec COND-20 le monde P = S = 0 vide) | NOTE:2060, 2089-2094 | L06-067
- [OUVERT-02] NT : une 7-torsion d'un G(L) connexe n'est jamais équilibrée | idem | NOTE:2061-2063 ; JOURNAL:447-464 | L06-067
- [OUVERT-03] exclusion de « toute droite déconnectée » au rang 37 par des rangs exacts mod 7 (231 droites contre 18 dimensions) | donnerait avec OUVERT-01, 02 : r = 37 exclu | NOTE:2062, 2067-2072 | L06-066
- [OUVERT-04] borne inférieure du rang des systèmes de classes (grilles, différences jumelles) comptant TOUTES les relations indépendantes | donnerait des bornes sur tau_g, tau_n (COND-08) | NOTE:1910-1912, 2036-2039 | L06-050
- [OUVERT-05] graphes Xi_v possibles ; un prisme non-grille peut-il avoir deux jumeaux ; g(l) <= 3 | donnerait COND-10 | NOTE:1195-1196, 1245-1248 | L06-040
- [OUVERT-06] partie lignes (signes) de la droite à six grilles, couplages M_k, triangles | exclurait les droites à six grilles | NOTE:1785, 1728-1731 | L06-052
- [OUVERT-07] borne supérieure sur b_2 | couperait le plafond au rang 37 ; < 968 exclurait le rang 43 | NOTE:1392-1393, 1483-1484 | L06-045
- [OUVERT-08] borne supérieure de quelques 10^5 sur a_13 (norme 26 de L1) | facteur 1,8 sur tau | NOTE:1306-1308 | L06-045
- [OUVERT-09] multiplicités par graine aux normes 18, 20, 22, 24 ; c_20 <= 4 | COND-13, COND-14 | NOTE:1348-1349, 1396-1397, 4099-4104 | L06-104
- [OUVERT-10] N16 et N18 au rang 37 (catalogue complet des mondes de norme 16 ; mondes de rang de Seidel 32, 31) | COND-14 | NOTE:3820-3825, 4060-4061 | L06-094
- [OUVERT-11] borne sur le nombre de PAIRES de supports de même projection (masses 7 à 9, changements de somme), comme forme linéaire certifiée | COND-08 | NOTE:2826-2829, 2974-2979 | L06-056
- [OUVERT-12] support 10 : constantes de (5,5) et (8,2), pool et liens ; recensement d'ordre 11 ((7,4), (10,1)) | pourrait rouvrir le comptage | NOTE:1461-1463, 1675-1678 | L06-046
- [OUVERT-13] existence d'une 22-coclique ; classification de f(n) <= 4 dans son réseau (r = 43) | COND-17 ; exclusion des 22-cocliques à r = 43 | NOTE:1064, 1097-1099, 1139-1140 | L06-027, L06-029
- [OUVERT-14] lemme uniforme interdisant les motifs A et B de toute étoile | (a') | NOTE:2553-2554, 2562-2563 | L06-076
- [OUVERT-15] 174 coeurs : les quatre autres noyaux obligatoires le long des cycles d'arêtes croisées | exclusion de types de coeurs | NOTE:3311-3316 | L06-108
- [OUVERT-16] loi des quadrangles c(Q) = somme des c_e (conjecture) | COND-40 | RB:308 ; NOTE:3389 | L06-110
- [OUVERT-17] boules à torsion du profil (4,8) (16 516) ; vérification complète d'isomorphisme ; générateur exhaustif des 1,4e10 types ; modèles torsion et déconnecté ; audit du modèle de LAP | COND-25 | NOTE:3233-3239 ; COUT:87-100 | L06-089, L06-082
- [OUVERT-18] ré-implémentation indépendante de l'encodage S3 ; calcul d'orbite ; passage « squelette trivial » -> « pas de revêtement non cyclique » | COND-34 | S3:324-327 | L06-128
- [OUVERT-19] membre asymétrique de srg(243,22,1,2) ; groupes non abéliens d'ordre 81 ; Z_9 x Z_3^2 ; fenêtres < 50 | modèle positif d'asymétrie | SF:416-471 | L06-136
- [OUVERT-20] « pas de carré alternant » (l = 2) et (P) | réduction des partitions de 6 à 51, 411, 3111, 1^6 | TR:63-74 | L06-120
- [OUVERT-21] rang 43 : un argument de repère | « only the frame can exclude this rank » | NOTE:1040-1041 | L06-026
- [OUVERT-22] monde de norme 18 : une nouvelle réduction | exclusion des rangs par les mondes | NOTE:4236-4240 | L06-098
- [OUVERT-23] (dossier) cycle de transport de longueur quatre forcé ? réalisation des cinq bords ; injectivité de H -> h_H | COND-38 | DI:46-52, 776-822 | L06-114
- [OUVERT-24] audit de N14 par une autre session ; run étiqueté complet (~6 h) | consolider N14 | NOTE:3816-3818 | L06-092
- [OUVERT-25] borne inférieure de min Lambda_3(T) pour une droite connexe | une borne dépassant la borne de Hermite de RD:47 pour cette droite donnerait une contradiction | RD:51 | L06-118
- [OUVERT-26] 213 survivants de la boule cyclique (2,4,1) à certifier ponctuellement (~30 min) | calibration | NOTE:2309-2310 | L06-072
- [OUVERT-27] JOURNAL : k = 20 à P > 0 sous NT (désormais hors fenêtre), k = 24 à 28, « k = 22 sans générique » | — | JOURNAL:508-520 | L06-152

### 10.4 Méthodes transposables (d'un cas à un autre)

- [METH-01] programme thêta de niveau 7 (L1, M, Fricke, LP exact avec certificats) | de : C1 rangs | vers : tout srg(v,k,1,2) avec r - s = 7 ; analogue niveau 63 avec les vecteurs de sommets proposé la nuit du 14/10 (lot L07) | NOTE:1-29 | L06-001
- [METH-02] empilement des graines (Fano) | de : norme 14 | vers : normes 16 et 18 : NE se transpose PAS tel quel (NOTE:667-669, 765) | L06-021
- [METH-03] recensement d'induits (formules en v, k) | de : 99 | vers : toute la famille srg(v,k,1,2), testé sur 243 | NOTE:698-717, 855-869 | L06-036, L06-037
- [METH-04] test du biplan minimal paramétré (n, k, bloc, valeur propre) | de : 99 (u = 3) | vers : u = 1, 4 (fait), 10, 31 | BP README:25-31 | L06-101
- [METH-05] saturation par témoins de bord | de : supports Cube/Wagner | vers : « d'autres supports possédant des masques qui séparent intégralement leurs coordonnées » | DI:403 | L06-114
- [METH-06] système des multiplicités de masques (note 222 de Codex) | de : 310 coeurs | vers : unions de noyaux de quadrangle, rubans, prismes jumeaux (fait) | NOTE:3291-3296 ; RB:369-372, 446-454 | L06-105
- [METH-07] certificats de propagation à une / deux étoiles (sac_two_star.py, rejouables) | de : quatre boules | vers : toute boule ; base d'un lemme uniforme | NOTE:2387-2425, 2486-2494 | L06-074
- [METH-08] base typée d'un vecteur court forcé + conditions mod 7 (N14) | de : norme 14 au rang 37 | vers : norme 16 (n16cell, partiel) ; coûteux pour 18, 20 ; au rang >= 39, deux coordonnées libres par sommet | NOTE:3694-3707, 4155-4158, 4190-4193 | L06-092
- [METH-09] holonomie et loi de parité des quadrangles | de : 99 | vers : tout graphe où chaque arête est dans un unique triangle et mu = 2 (srg(243,22,1,2), géométries tordues) | RB:14-51 | L06-109
- [METH-10] reformulation DRG, parité des faisceaux, certification DRAT | de : 243 (S3) | vers : 99 seulement si un spread régulier existait (il n'existe pas : COND-37) | S3:140-163 | L06-124
- [METH-11] échanges et rigidité (critère de support, Whitney), impossibilité de Godsil-McKay | de : 243 | vers : toute la famille, dont 99 (k = 14 inclus) | SF:40-69 ; srg243_second.tex:148-166 | L06-174, L06-123
- [METH-12] genre / formule d'oddité (L22, L23, 17.80) | de : C1 | vers : C2 (« C2 avait déjà g pair, forme hyperbolique », JOURNAL:528) et réciproquement | JOURNAL:521-566 ; NOTE:3100-3124 | L06-146, L06-153
- [METH-13] route C de C2 (enveloppes de réseaux, Borcherds) | de : C2 | vers : C1 : sur-réseau 7-unimodulaire de L1 + 7 I_2 de rang 46, sans classification : fermé | NOTE:2655-2661 | L06-165
- [METH-14] routes A et B de C2 | de : C2 | vers : route des étoiles (analogue de A sans ses piliers) et « (6,6) partout » (analogue de B) | NOTE:2659-2664 | L06-165
- [METH-15] méthode de LAP pour les droites déconnectées (scalaire résiduel, recherche exhaustive d'étoile) | de : maille 5 | vers : « toute famille finie de profils déconnectés », profils à k prismes (k = 1..6) | NOTE:2802-2805 | L06-087
- [METH-16] bornes ordonnées d'Astra | de : Fano tendu | vers : « dès que les comptes sont fixés, hors du Fano aussi » | JOURNAL:330-333 | L06-179
- [METH-17] positivité exacte par compléments de Schur (projecteurs 27I - 9A + J, 44I + 11A - 2J) | de : coeurs, rubans, triangle | vers : tout support | NOTE:2681-2682 ; RB:347-353 ; JOURNAL:245-252 | L06-105, L06-112
- [METH-18] q:7 (méthodes 7-adiques de C1) | de : C1 | vers : C2 (involution) : g- ∈ {16, 18, 20} | JOURNAL:521-566 | L06-153
- [METH-19] critère S5 (2-adique) | de : table de Brouwer | vers : srg généraux ; pas 99 | s5_2adic.tex:55-75, 184-190 | L06-138
- [METH-20] formule locale de rang (matrice 84 x 84) et lemme des étoiles | de : rank7 / L20 | vers : bornes inférieures de rang par sous-matrices déterminées (limite : support déterminé de rang >= 45 nécessaire) | rank7.tex:151-205 ; JOURNAL:287-290 | L06-137
- [METH-21] Akiyama (Venkov, racines) | de : srg(266,45,0,9) | vers : 99 : non transposable | JOURNAL:108-113, 219-222 | L06-177
- [METH-22] positivité de Delsarte sur les droites | de : 99 | vers : général ; degré 3 : moyenne f <= 10 | TR:13-14 | L06-119
- [METH-23] estimateur de Knuth pour dimensionner une recherche | de : S3, co-Heawood | vers : tout calcul avant lancement | S3:40-47 ; NOTE:4169-4186 | L06-099
