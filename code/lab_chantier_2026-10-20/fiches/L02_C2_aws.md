# Lot L02_C2_aws : la campagne de calcul AWS du cas C2 (route C) et les notes du dépôt conway99-c2-aws

Chantier du 20/10/2026. Carte en lecture seule, établie le 20/10/2026. Résultats : `fiches/L02_C2_aws.jsonl` (463 lignes,
identifiants `L02_C2_aws-001` à `L02_C2_aws-463`).

## 0. Portée, méthode, conventions

- **Lot.** 1 014 contenus distincts dont la première copie est dans `C:\Users\RESEARCHER\cw\conway99-c2-aws` (295 références, dont
  255 branches `run/*`). Environ 70 % sont des journaux de machines (`status.txt`, `tail_agent.txt`, `done.txt`...) ; le reste est
  la campagne (HANDOFF, README, mesures, énoncé final, partie B du document de preuve), les lemmes T16, T18, T20 et le pont, l'audit
  de la réduction et le papier C2, et du matériau C1 (07-10/10) déposé sur master.
- **Qui a lu quoi.** Le coeur de la campagne (partie K : branches, file, enregistrements, couverture, coût, énoncé final, notes Codex
  sur la campagne) a été lu par l'agent L02. Quatre sous-agents, avec les mêmes consignes en lecture seule, ont couvert : **A** le
  matériau C1 hébergé ici ; **B** T16, T18 et le pont ; **C** T20 et les branches `lemma-run/*` ; **D** la réduction (Théorème R),
  les audits, le papier. J'ai vérifié la validité des JSONL, les renvois croisés et quelques recoupements (blob T20 accepté,
  résidu de la règle jumelle, représentants tier L) ; je n'ai pas revérifié chaque numéro de ligne des parties A à D.
- **Recomptes propres.** Les comptes marqués « recompte L02 » viennent de scripts de lecture (git cat-file, un processus, moins de
  15 s) sur les branches `run/*` et `queue` ; ils ne refont aucun calcul mathématique.
- **Sources.** Format `conway99-c2-aws:<branche>:<chemin>:<lignes>` ; dans les sections reprises de la partie A, `H:a-b` =
  `master:HANDOFF_2026-10-01.md:a-b`, `G:a-b` = `master:c1_rank37_girth5_lines/NOTE.md:a-b`, `M:a-b` =
  `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:a-b`. Heures en UTC sauf les dates de commit (+02:00).
- **Identifiants.** Chaque ligne du JSONL garde dans `remarques` son « id de travail » (préfixe « L02- » suivi de K01-K40,
  D01-D71, B01-B64, C01-C90, A01-A192 ou L01-L06) ; dans ce texte tous les renvois sont convertis en identifiants finaux. Plages :
  K = 001-040, D = 041-111, B = 112-175, C = 176-265, A = 266-457, L = 458-463 (combinaisons repérées par l'agent L02, section 17).
- **Sessions.** LAP = session Claude du portable ; LAB = session Claude du PC du labo ; Codex = CDX ; « l'utilisateur » = Dilan
  Djematene. Toutes les relectures citées sont des relectures par des sessions IA, sauf mention contraire.

## 1. Résumé (10 lignes)

1. Campagne AWS de la route (C), 29/09-07/10 : paquets v1-v10 (moteur frame_dfs, calibration 118:2), deux comptes, 255 branches `run/*` ; file de 17 024 clés, toutes faites sauf 003:181:182.
2. 07/10 17:47 UTC : 156/156 exclusions enregistrées au tracker du labo (statut composite : verdicts S, certificats C, lemmes P relus par IA seulement).
3. Couverture : 91 réseaux par balayage stream (220 260 576 paires) ; 13 par mise de côté (5 190 752 paires sur T18, 2 508 295 sur T20, certifiées) ; 20 au niveau réseau ; 29 anciens réseaux repris en v10 le 07/10 au soir.
4. L'énoncé « pas d'automorphisme d'ordre 2 » repose sur le Théorème R (P, relu par Codex), T16-T18-T20 (P, IA), 25 775 627 exclusions par recherche sans certificat (S) et une énumération comparée sur 4 réseaux.
5. Seul calcul ouvert du papier : la règle de transfert jumeau, au plus 2 479 669 paires à recertifier (O), garé par l'utilisateur le 07/10 20:36 UTC.
6. Écarts : 28 réseaux S sans enregistrement sur branche ; environ 780 représentants y1 sur enregistrements du seul PC ; 000, 004, 010 en lecture unique ; 044 en un passage ; écart ARM inexpliqué.
7. Lemmes : T16 (dossier ChatGPT, arbitre Codex) ; T18 (deux arbitres IA, au moins deux programmes) ; T20 (Codex, deux programmes par calcul ; blob accepté différent de master ; écart de comptes vu en partie C) ; pont relu.
8. Coût : grand livre du premier compte environ 243 $ (07/10 12:00 UTC) + environ 21 $, au prix Spot maximal (borne haute) ; crédits épuisés le 06/10 (septembre 76,77 $, octobre 120,34 $ couverts) ; second compte environ 15 $ de crédits gratuits ; rien n'est formalisé, aucun humain n'a relu.
9. Matériau C1 hébergé (07-10/10) : rang 35 exclu le 08/10, r ∈ {37, 39, 41, 43} ; résultats locaux au rang 37 ; Mandat C (rigidité, S₀ au rang 43, 3 271 supports P3/N25 ouverts) ; aucun autre rang exclu.
10. JSONL : 457 résultats (P 182, E 158, S 30, C 23, X 22, O 18, H 17, R 7) et 6 combinaisons repérées entre notes (O).

## 2. Chronologie (route C, dépôt conway99-c2-aws)

### Partie K : la campagne de calcul

Heures en UTC sauf mention ; les dates de commit git sont en heure locale (+02:00).

| Date, heure (UTC) | Événement | Source |
|---|---|---|
| 29/09 ~19:58 | Dépôt créé : paquet vérifié `c2_cloud_run.zip` (sha256 209c9319), `machine.sh`, plan de 18 machines | `commit e884ac1f7` |
| 29/09 21:13-22:12 | Run « 54 tranches » : 18 machines (3 comptes x 6 régions, tranches 0-17/54) puis 26 autres (`run/slice-19..44`) ; moteur v1 ; calibration 118:2 EQUIVALENT partout | `master:OLD_README_54_TRANCHES.md:1-12` ; `origin/run/*:status.txt` |
| 30/09 ~05:15 | Derniers statuts du run 54 tranches (figés EN_COURS) : le run « died when the account had a problem » ; 399 jobs finis | `master:HANDOFF_2026-10-01.md:32` |
| 01/10 | Import des 399 au labo (0 refusé) : tracker 94 exclus / 61 ouverts / 1 partiel (000). File adaptative (3 026 jobs, plafond 115 $), répétitions CI gratuites ; deux défauts corrigés avant dépense | `master:REPRO_COMMANDS.md:11-29` ; `master:HANDOFF_2026-10-01.md:5-15,97-100` |
| 01/10 20:12-20:20 | Pilote puis 3 machines c7a.8xlarge Spot à eu-north-1 (paquet v1) | `master:HANDOFF_2026-10-01.md:102-153` |
| 01/10 22:24-22:30 | Paquet v2 (FD_SYM3, FD_TWINCANON) ; premières interruptions Spot | `master:HANDOFF_2026-10-01.md:155-190` |
| 01/10 23:00 - 02/10 02:30 | v3 (O24, Golay 001), v4 (Golay 002/004/010) ; 000 exclu (~01:10, 107/156) ; 010 exclu (~02:30, 108/156) | `master:HANDOFF_2026-10-01.md:192-246` |
| 02/10 ~04:45 | v5 (correctif HSfull) ; 059 exclu (109/156) ; capacité Intel à eu-west-2 ; flotte de 12 | `master:HANDOFF_2026-10-01.md:247-273` |
| 02/10 ~14:50 | v6, v7 ; cascade 109 -> 132 (23 réseaux) après les 4 INCOMPLETE de 052:7:8 | `master:HANDOFF_2026-10-01.md:282-370` |
| 02/10 ~15:20-19:35 | v8 (118 paires K = 0 de 023/024/026/028) ; 004 exclu (133/156) ; récupérations massives Spot à us-east-2c | `master:HANDOFF_2026-10-01.md:371-415` |
| 02/10 22:30 | Alerte budget : 5 500-8 000 heures-job restantes, impossible sous le plafond | `master:HANDOFF_2026-10-01.md:416-441` |
| 02/10 23:30 - 03/10 07:28 | 026, 028, 024 exclus ; 023 puis 020, 021 en cascade : 139/156 ; essai ARM en STOP CALIB | `master:HANDOFF_2026-10-01.md:442-480` |
| 03/10 10:52 | ARRÊT à la demande de l'utilisateur : 139/156, 17 ouverts, grand livre 121,87 $ | `master:HANDOFF_2026-10-01.md:513-544` |
| 03/10 après-midi | Second compte (frère), paquet v9 (jobs fins) ; 018 exclu (22:29, 140/156) ; 019 puis 017 (23:31, 142/156) | `master:HANDOFF_2026-10-01.md:546-578` |
| 04/10 15:20 | Paquet v10 (filtre Y = 13, min L* >= 9/7) | `master:HANDOFF_2026-10-01.md:589-594` |
| 05/10 ~10:10 | Flotte arrêtée jusqu'aux quotas | `master:HANDOFF_2026-10-01.md:600-602` |
| 06/10 (laptop) | Pilote v10, correctif fetch ; réordonnancement par dépendances jumelles ; flottes de 8 + 8 ; tail runner ; 016 entièrement calculé (18:00) ; cible de lemme (T18, T20) | `master:HANDOFF_2026-10-01.md:610-696` |
| 06/10 21:00-23:50 | Décision utilisateur : mettre de côté les paires couvertes par T18/T20 ; mode DEFERRED déployé (22:12), variante rapide (22:43), plafond 300 $, incident de contention de la file corrigé | `master:HANDOFF_2026-10-01.md:698-880` |
| 07/10 ~03:00 | Cinq jobs tronqués par le producteur (max_out 10^6) ; sessions AWS expirées | `master:HANDOFF_2026-10-01.md:882-920` |
| 07/10 13:45 | Toute la file faite sauf 003:181:182 ; 143 exclus + 13 balayés (5 190 752 paires pour T18, 2 508 295 pour T20) | `master:HANDOFF_2026-10-01.md:922-940` |
| 07/10 ~15:00-15:46 | 003:181 par le corollaire Y1 ; audit H2 25/25 ; certificats 7 762/7 762 ; 143 par preuve à la main | `master:lemma/FINAL_STATEMENT_DRAFT.md:31,49,56-67` |
| 07/10 17:43-17:47 | F4 égal sur 064 ; acceptation de T18 et T20 par l'utilisateur ; conversion : 156/156 | `master:lemma/FINAL_STATEMENT_DRAFT.md:6,25` ; `master:measures/lemmas_accepted_2026-10-07.json` |
| 07/10 ~18:05 | Clés de déploiement révoquées ; aucune instance sur les deux comptes | `master:HANDOFF_2026-10-01.md:1001-1005` |
| 07/10 18:17-20:29 | Reprises : 713 représentants sans programme identifié (2 419 830 paires) ; les 28 réseaux des anciennes listes (6 657 309 paires ; 044 fini 20:29) ; route des témoins (17 réseaux sans recherche) | `master:lemma/PROOF_C2/B_LATTICES.md:95-207` |
| 07/10 20:36 | Calculs GARÉS par l'utilisateur ; reste ouvert : recertification de la règle de transfert jumeau | `master:HANDOFF_2026-10-01.md:1130-1153` ; `commit ef135d188` |
| 07/10 21:05 | C1 ouvert ; ce dépôt reste le registre de C2 (notes C1 ultérieures : partie A ci-dessous) | `master:HANDOFF_2026-10-01.md:1173-1175` |

### Partie B : T16, T18 et le pont (Chronologie)

| date, heure | événement | source |
|---|---|---|
| 2026-10-04 | Trois notes de ChatGPT : obstruction du cube, lemme d'égalité 8/7 (« deuxième avis »), obstruction de Wagner + certificats | `lemma/t16/dossier_2026-10-04/C2_PROLONGEMENT_SUPPORT16_PREUVE_CUBE.txt:1-2` ; `LEMME_EGALITE_8_SUR_7_C2.txt:1-2` ; `C2_WAGNER_BORNE_9_SUR_7.txt:1-2` |
| 2026-10-04 (matin) | LAB rederive la note cube à la main : « Verdict: correct. No gap was found » ; Wagner encore ouvert | `lemma/t16/lab_check/VERIF_CUBE_OBSTRUCTION_2026-10-04.md:1-54` |
| 2026-10-04 vers 14:00 UTC | LAB : critère de paire Y = 13, mesure min97_probe ; règle « NOT USABLE for verdicts at this point » | idem :56-98 |
| 2026-10-04 vers 15:00 UTC | LAB : dossier Wagner relu, parties finies relancées (enregistrements identiques) | idem :100-144 |
| 2026-10-04 vers 17:30 UTC | Réimplémentation indépendante (agent LAB) concordante ; « Y = 13 criterion: usable » | idem :146-179 |
| 2026-10-06 17:28 (+0200) | LEMMA_TARGET créé par LAP : mesure Emin, dictionnaire, cibles T18 et T20 | commit 2a9978420 ; `LEMMA_TARGET_2026-10-06.md:1-80` |
| 2026-10-06 17:47 | Certificat local à neuf vecteurs : ne décide pas, plus lent | commit b1c5817df ; `LEMMA_TARGET_2026-10-06.md:82-97` |
| 2026-10-06 19:46 | T18 réduit à trois graphes (round 1, « about 45 min of work ») | commit b5737591d ; `lemma/t18/T18_REPORT.md:1-153` |
| 2026-10-06 20:02-21:10 | Round 2 : (4,1,2) à la main, (3,3,1) calculé (une implémentation) | commit 341a92b4f ; `T18_REPORT.md:155-333` |
| 2026-10-06 21:03-22:30 | Round 3 : B1 profil (2,5,0), 4 survivants sur 47 sommets | `T18_REPORT.md:335-502` |
| 2026-10-06 22:40 | n_3 = 0 prouvé à la main (agent N3) | commit 2f3ca43da ; `lemma/t18/N3_REPORT.md` |
| 2026-10-06 22:27-23:55 | Round 4 (B1) ; agents B0 (22:27-23:52), B2 (22:29-23:27), VERIF331, STRUCT | `T18_REPORT.md:504-680` ; `lemma/t18_B0/REPORT.md:1` ; `lemma/t18_B2/REPORT.md:3` |
| 2026-10-06 23:08 | Borne de rang (STRUCT) : les 4 survivants de B1 exclus | commit 37298d0bf |
| 2026-10-06 23:41 | B2 fermé, (3,3,1) revérifié, borne de rang, T20 round 1, mode report retravaillé | commit 645201b5b |
| 2026-10-07 00:41 | Étape C refaite par CMINE sur tout B0 (0) et tout B1 (les 4) | commit 508b487e0 |
| 2026-10-07 01:37 | Arbitre 1 : « no error found; nine fixes for the written text » | commit aae8ea4b0 |
| 2026-10-07 02:17 | `lemma/T18_PROOF.md` v1 | commit e657f46c3 |
| 2026-10-07 03:40 | Arbitre 2 (texte seul, calculs refaits) : aucune erreur, onze points | commit 0c5d3f8cf |
| 2026-10-07 04:23 | `T18_PROOF.md` v2 (onze corrections) | commit e9a5058fa |
| 2026-10-07 04:27 / 04:45 | `lemma/BRIDGE.md` ; arbitrage du pont (aucune erreur ; H4 paire par paire) | commits d16b014c9, d54db2ab2 |
| 2026-10-07 15:26 UTC | LAB demande l'accord explicite de l'utilisateur pour T18 et T20 | `measures/lemmas_accepted_2026-10-07.json:8` |
| 2026-10-07 15:30 (+0200) | Corrections de l'arbitre fusionnées dans le pont | commit 1e55a4e1e |
| 2026-10-07 15:48 / 16:00 / 16:03 | Index T16 et dossier versés ; arbitrage Codex de T16 ; « Consequently » | commits 9ad23660d, d26b985ac, fd2ff2c9f, c0e5c2f32 |
| 2026-10-07 16:57 / 17:02 / 17:04 | Codex : certificat à y1 fixé pour 003:181:182 ; Corollaire Y1 dans le pont ; intégration vérifiée | commits c3d1431ad, a3e561a7a, 0dfdf92d6 |
| 2026-10-07 17:47 UTC | Acceptation de T18 et T20 enregistrée (blob T18 6cbcf896, = master actuel) | `measures/lemmas_accepted_2026-10-07.json:1-21` |
| 2026-10-07 19:48 (+0200) | « the 156 lattices are excluded in the lab tracker (conversion of the 13 last ones, T18 and T20 accepted by the user) » | commit 414e68d23 |
| 2026-10-07 20:54 | Document de preuve : A2 (énergie, règles témoins, Y1), A3 (T16, T18, T20) | commit 87d7b5450 |
| 2026-10-07 21:38 / 21:52 | `T20_PROOF.md` modifié après l'acceptation (hors partie B ; le blob accepté e50d5be0 n'est plus celui de master) | commits bbdeea453, 474aa859a |

### Partie C : T20 et les calculs des branches lemma-run (Chronologie)

| Date, heure (UTC sauf mention) | Événement | Source |
|---|---|---|
| 06/10, 22:20-23:35 (heure du rapport) | Round 1 : réduction à neuf configurations (main + deux énumérateurs) | `master:lemma/t20/T20_REPORT.md:1-9` ; commit 645201b5b (2026-10-06 23:41 +0200) |
| 07/10, 00:37-04:50 local | Round 2 : III.0 et IIa.0 exclus (deux programmes chacun) ; III.1 et le cas I ouverts | `master:lemma/t20_R2/REPORT.md:1-16` ; commit 715802e33 |
| 07/10, 09:24 | III.1 : premier programme fini (8 parties, 0 complète, un programme) | commit a7af3b1da (11:24 +0200) ; `master:lemma/t20_III1/README.md:1-13` |
| 07/10, 09:30 | Agent du round 3 (cas I) lancé par LAP | `master:lemma/T20_WORK.md:91` |
| 07/10, 09:35-11:47 | Seconde vérification de III.1 (engv2, 48 parties) ; board C1 « closed 11:47 » | `master:lemma/t20_III1/VERIF.md:1` ; `master:lemma/T20_BOARD.md:34` |
| 07/10, 09:44 | Page de travail T20_WORK (trois sessions LAP, LAB, CDX) | commit ce0cfd7a4 |
| 07/10, 10:18-10:20 | Boîte de calcul à usage unique ; autotest réussi 10:20 | `master:lemma/cloud/README.md:11-13` ; branche selftest |
| 07/10, 10:35 | v1 du pipeline cas I (6471b9d64) | `master:lemma/ARTIFACTS_T18_T20.md:18-20` |
| 07/10, 10:36:23-10:57:06 | `t20_I_rest` : neuf cas n_3 = 0, premier programme seul | `origin/lemma-run/t20_I_rest-...:ALL.txt:1-153` |
| 07/10, ~10:51 | Route A run 1 : 168 classes fermées (dernier push) | `origin/lemma-run/t20_n3-i-0b8ae938c1fc89c62:STATUS.txt:1` |
| 07/10, 10:59 | Jobs t20_Iv_A..F (vérificateur v1) ; démarrage 11:00-11:05 sur 5 x 8 vCPU | commit a318b7419 ; `origin/defer-n4:lemma/T20_BOARD.md:72` |
| 07/10, 11:14 | Route A relancée avec restauration des 168 | `master:lemma/t20_HAND/NOTES.md:356` |
| 07/10, ~11:15 | t20_Iv_F repris (Spot) avant tout résultat | `97f7c9c16:lemma/T20_BOARD.md:35` |
| 07/10, 11:18 | v2 (ea16eb42b) : le second programme ferme les nœuds de rang par sa propre recherche | `master:lemma/ARTIFACTS_T18_T20.md:18-20` |
| 07/10, 11:19:43-11:52:31 | `t20_I1_340` (128 vCPU, compte utilisateur) : I.1 (3,4,0), deux programmes d'accord | `origin/lemma-run/t20_I1_340-...:I1_340/timing.txt:1-5` |
| 07/10, 11:30 / 11:43 | Route A : 168 puis 183 classes fermées ; run arrêté 11:43 | `master:lemma/t20_HAND/SPEC_N3.md:150-151` ; `master:lemma/T20_BOARD.md:13` |
| 07/10, 11:50-12:30 | Mesure de coût de la route A (t20_n3_sample) : environ 1,000 h-cœur par programme | `master:lemma/T20_BOARD.md:13` |
| 07/10, 11:55 | Second programme Codex route A implémenté, comptes de bases conformes | `origin/defer-n4:lemma/T20_BOARD.md:17` |
| 07/10, 10:14-11:27 | Notes LAB (H1-H10) et SPEC_N3 poussées | commits 4ca3b84aa à c0b99ec12 (12:14-13:27 +0200) |
| 07/10, 10:51-11:52 | Lemmes Codex : HAND, PROFILE_421, EDGE_BOUND, TRIANGLE_REDUCTION, n3_second | commits dbe141ef3, bd0848c1c, 34fa040fe, 8ecf577ff, 3e94576b3, 330933f35 |
| 07/10, 12:12 / 12:22 | t20_Iv_E : dernier push ; machine reprise à 12:22 (I.1 (4,2,1) avorté, vérificateur v1) | `origin/lemma-run/t20_Iv_E-...:STATUS.txt:1` ; `97f7c9c16:lemma/T20_BOARD.md:35` |
| 07/10, 12:31 | T20_PROOF.md première version, 9.B en attente (8510844a4) | `origin/defer-n4:lemma/T20_PROOF.md:1-28` |
| 07/10, 12:42 | Premier passage d'arbitrage Codex (E1, E2, G1-G3, C1-C3) | `master:lemma/t20_CODEX/REFEREE_T20_PROOF.md:1-30` ; commit d2d7edfd0 |
| 07/10, 12:45 / 12:55 | Décision route B ; premier programme route B fini, 0 complète | `master:lemma/T20_BOARD.md:15-16` |
| 07/10, 13:18-14:33 | Relance des cas (4,2,1) : t20_Iv_G..J (v2) ; I.1 (4,2,1) fini 14:33 : douze cas sur douze | `master:lemma/T20_BOARD.md:35` |
| 07/10, 13:28 | Corrections E1, E2, C2, G3 fusionnées | commit 4e545ceab |
| 07/10, 13:52 | v3 (99eb1fb50) : spécification route B et second programme | `master:lemma/ARTIFACTS_T18_T20.md:18-20` |
| 07/10, 14:00 | Route B : les deux programmes complets sur les 50 cas | `master:lemma/T20_BOARD.md:14` |
| 07/10, 13:56-14:20 | 9.B.6 et Théorème 10.2 écrits ; addendum Codex (aucune erreur bloquante) | commits f7e726ff2, cef222870 ; `master:lemma/T20_BOARD.md:44` |
| 07/10, 15:25-15:26 | Branche d'archive route B ; table de provenance ARTIFACTS (blob T20 e50d5be079) | commits b960cd136, a730e7b5e |
| 07/10, 17:47 | Conversion du registre du labo après acceptation de T18 et T20 par l'utilisateur | `master:lemma/FINAL_STATEMENT_DRAFT.md:6` |
| 07/10, 19:38-19:52 | Contrat G2 fusionné ; passage Codex sur l'article (G2 relu à 66c12bd73, ligne I.1 (3,4,0) d'ARTIFACTS fausse) ; quatre points fusionnés | commits bbdeea453, 60bddfdef, 474aa859a |
| 07/10, 20:29 | Plus aucune machine ; clé de déploiement révoquée | `master:lemma/T20_BOARD.md:84-92` |

### Partie D : réduction, audits, papier (Chronologie)

Heures de commit en heure locale (+0200) ; les heures « UTC » sont celles des notes.

| Date, heure | Événement | Source |
|---|---|---|
| 27-29/09 | Runs de septembre : balayages stream et h-stage, frame_dfs + Lemme U+, empilement C1 (envelope_pack 19af6fb), budget de composantes de 143 (28/09), piège caractéristique et règle swap (Astra, 28/09) | PROOF_SKELETON_C2.md:14-19, 25-180 ; AUDIT_REDUCTION.md:316-326 |
| 01/10 19:49 | Squelette auto-généré : « excluded 93, open 62, partial 1 » | PROOF_SKELETON_C2.md:1-3 |
| 04/10 | LAB recalcule les 156 réseaux (erratum sur 150) ; règles des jumeaux relues (« conservative ») ; dossier T16 | upstream/README.md:10-15 ; AUDIT_REDUCTION.md:288-301 |
| 07/10 12:17 | Dépôt des copies amont (MODEL.md, squelette) | commit f18bd62d5 |
| 07/10 13:33 UTC | Message 52 de LAB : recensement H1 ; lemme H2 de l'empreinte nulle ; 12 620 paires « pair budget » | AUDIT_ENGINE_RULES.md:136-183, 332-335 |
| 07/10 « 14:45 » | Selon LAB, H4 « Closed » (105 relancé sans le test de budget) | FINAL_STATEMENT_DRAFT.md:51 |
| 07/10 15:14 | Section A (Théorème R, A.1 à A.8) écrite par LAP | commit f115663b7 |
| 07/10 15:18 | Sections C, D, E par LAB (F4 « NOT DONE » ; 143 et 153 reposent sur une seule méthode) | commit c10bb83e1 ; AUDIT_REDUCTION.md:230-331 |
| 07/10 15:21-15:25 | A.9 (indécomposabilité), A.0 (point fixe) ; arbitrage Codex de la section A | commits 9aee7b1cf, 399c4c758, f4499d116 |
| 07/10 15:33-15:37 | Section B de Codex (H1 à H5) fusionnée ; identité N4 ; Codex relit A.0 et A.9 | commits 7dfadcc7e, 8bee8a0e2, b276fad77, d3c89af62 |
| 07/10 16:00 | Codex arbitre T16 et vérifie les obstructions de Wagner | commit d26b985ac |
| 07/10 17:16-17:28 | Preuve à la main de 143 (LAB), arbitrée et acceptée par Codex | commits 452619fd0, 53ceec278, 70425a6ba |
| 07/10 17:37-17:47 | Codex arbitre les comptes de couches ; 156 catalogues locaux certifiés ; couverture H2 25/25 | commits 350eba97d, 60201a7b2 |
| 07/10 17:47 UTC | Tracker du labo à 156/156, après acceptation de T18 et T20 par l'utilisateur | FINAL_STATEMENT_DRAFT.md:6, 56 ; commit 414e68d23 |
| 07/10 18:17-18:49 UTC | Certificats Y1 sur 55 réseaux (18:20) ; 713 y1 relancés ; 28 réseaux relancés en entier | B_LATTICES.md:88-100, 185-189 |
| 07/10 19:03 | Certificat linéaire 378 ≤ 336 (Codex) ; note de faisabilité Lean | commit ce200ea36 |
| 07/10 19:54-20:54 | Dossier PROOF_C2 : A1 (= section A), puis A2, A3, MAIN | commits 0b3c233f4, 87d7b5450 |
| 07/10 20:05 UTC | Correction de LAB sur les « 732 paires » | B_LATTICES.md:190-197 |
| 07/10 20:29 UTC | 044 terminé et accepté (un seul passage) | B_LATTICES.md:201-205 |
| 07/10 21:24 | Premier texte complet du papier (c1bcba6bb) | commit c1bcba6bb |
| 07/10 21:26-21:38 | Codex : empilement indépendant (18 sur 18) ; identité exacte des 156 entrées | commits b417896b2, bd4e1f021 |
| 07/10 21:35 | Le corollaire devient l'asymétrie ; note asymmetric.tex | commit 62b5ddabe |
| 07/10 21:46-21:58 | Arbitrage du papier par Codex ; corrections ; ordre 7 réattribué | commits 60bddfdef, 474aa859a, e22cfc57f |
| 07/10 22:08-22:31 | Règle de transfert décrite avec ses nombres ; outil exact des jumeaux (Codex) ; résidu dimensionné (≤ 2 479 669 paires) ; 044 dans le papier | commits acf843312, 43de8ae4d, 453974af8, 2d9122f02, 9d9094241 |
| 07/10 22:46-22:52 | Revue éditoriale de Codex ; version finale du papier | commits 83111092d, 253e7ec16, c8c84b73c, fd2df9787 |

### Partie A : matériau C1 hébergé dans le dépôt (Chronologie (UTC))

| date, heure | événement | source |
|---|---|---|
| 07/10 20:36-20:37 | L'utilisateur parque les calculs (C2) ; « C1 next » | commits ef135d188, 915fc4f69 |
| 07/10 21:05 | « C1 IS OPEN » (mot de l'utilisateur au labo 21:06) ; C1 vit dans conway99-c1 ; Codex mène ; envoi à Codex de ce qui survit des T-preuves sans σ (L02_C2_aws-266-A03) | H:1173-1193 ; commit bef651efb |
| 07/10 21:11 | Correction : l'observation norme 14 était déjà dans notes/110 ; aucun 2-(11,5,2) dans les deux srg(243) | H:1195-1202 ; commit 0f42094e9 |
| 07/10 22:04 | Programme thêta du labo (premiers verdicts r ≤ 25, 27…) ; norme duale, prismes | H:1204-1219 |
| 07/10 22:36 | r ≥ 33 accepté (audit Codex 168) ; lemme des graines (13 configurations) envoyé | H:1221-1235 |
| 07/10 23:06 | r ≥ 35 accepté (Codex 168, 170, 172) ; graines 13 → 4 ; routes mortes (Weil, dual, Hermite) | H:1237-1252 |
| 08/10 00:09 | Bilan de nuit ; lemme A (norme 18) ; Codex continue seul | H:1254-1269 |
| 08/10 07:14 | Rang 35 exclu, r ∈ {37, 39, 41, 43} ; audit à la main de LAP ; exception de la note 183 | H:1271-1291 ; commit dd3dda4a0 |
| 08/10 07:34-07:36 | Collisions de prismes jumeaux dans (6,3), masses 6 et 7 | H:1293-1313 |
| 08/10 08:49 | Phase exploratoire ; racines contre vecteurs courts ; espoirs locaux réfutés (CP-SAT) ; PL +3 inutile | H:1315-1339 |
| 08/10 09:25 | Rang 43 en six paramètres ; conditionnels d'exclusion du rang 43 | H:1341-1360 |
| 08/10 09:35 | Consigne de l'utilisateur : plus exploratoire, concret, pas de faux résultats | H:1362-1368 |
| 08/10 10:06 | Codex note 191 ; labo : profil C = 22-coclique ; question de la 22-coclique (ouverte) | H:1370-1385 |
| 08/10 10:26-10:38 | Codex b₁ ≤ 44 ; réseau Λ de la coclique (faisable) ; route arrêtée (deux entrées ouvertes) | H:1387-1412 |
| 08/10 10:45-11:10 | Utilisateur : tout l'effort sur le rang 37 ; « innover, trouver des lemmes » | H:1415-1418 |
| 08/10 10:58 | Correction de marge par le labo (9,62 M / 12,62 M sous les plafonds) | H:1427-1428 |
| 08/10 11:54 | Théorème de structure des prismes ; sous-réseaux de type 43 (transfert) | H:1414-1451 |
| 08/10 12:54 | Rang 37 en coordonnées lisibles ; routes collisions et plafond closes | H:1453-1482 ; commit e0ed1ffda (heure corrigée) |
| 08/10 13:34 | Route des graines close ; contrainte bilinéaire 45 − r ; Codex 196-198 | H:1484-1505 |
| 08/10 14:19-14:35 | Lemme N16 ; relu par le labo | H:1507-1546 |
| 08/10 14:40-15:02 | Comptabilité par paires (≤ 9) puis réservoir (≤ 9) clos | H:1548-1586 |
| 08/10 15:10-15:18 | Critique de l'utilisateur (reformulations) ; test du déterminant d'une droite dans g grilles : négatif | H:1588-1602 |
| 08/10 15:25-15:42 | Vérification de duplication (notes de septembre) ; borne de rang 56 − r sur les vecteurs du noyau | H:1604-1635 |
| 08/10 15:50-16:20 | Borne reprise par le labo et Codex ; « énoncé manquant » ; comptage pinceaux | H:1637-1703 |
| 08/10 16:46-17:17 | Correction (labo 17.51, Codex 206) : relations en un sommet dans tout graphe ; cible « au plus 10 relations » retirée | H:1705-1747 ; commit 7197f8554 |
| 08/10 17:23 | Contrôle arithmétique des identités d'une droite connexe | H:1749-1763 |
| 08/10 19:34 | Lien labo rétabli ; identités de Green réelles ; remarque de classe carrée retirée | H:1765-1803 ; commit 6ddd014b2 |
| 08/10 20:09-20:40 | Équation d'étoile dépend des ombres ; piste énergie d'apex réfutée ; critère du carré audité par Codex (note 217) | H:1805-1879 |
| 08/10 21:31 | Attaque propre des quatre rangs : aucun exclu ; déterminants des réseaux locaux | H:1881-1927 |
| 08/10 22:41 | Maille ≥ 5 ⇒ connexe (rang 37), dossier c1_rank37_girth5_lines/ | H:1929-1951 ; commit 15a3cfe3f |
| 08/10 23:05 | Utilisateur : réduire par lemmes, se coordonner, résultats le matin | H:1959-1962 |
| 08/10 23:49 | Audit du résultat maille 5 par Codex (note 224) ; solveurs ; balayages lancés | H:1953-1995 ; commit be2d973f4 |
| 09/10 00:53 | Profil (4,4,4) [(2,2,2)] clos : 275/275 | G:119-129 ; commit 784c31c98 |
| 09/10 01:27-03:52 | (3,3) sans prisme : toutes torsions mortes ; réductions | G:151-191 ; commits cb4ff9ec1, d4f74ddc3, 7efa7c8da, 5bbc0f47d, fa0acfa56 |
| 09/10 03:19 | Incident de travailleurs orphelins ; torsions 3 et 4 relancées | G:201-206 |
| 09/10 04:43-04:49 | (2,4) torsion 4 : 19/19 mortes | G:208-210 ; commit 1b8b47967 |
| 09/10 05:08-05:11 | Utilisateur : « arrête les calculs » ; tout arrêté ; rien ne redémarre sans lui | H:1997-2000 ; commit a25537df1 |
| 09/10 05:12 | 13e note : état de l'énoncé B (incomplet) | H:1997-2019 ; commit f8cf3894a |
| 09/10 09:29-09:56 | Mandat C : verdict, rigidité, bascule du 243, pilote négatif | M:1-193 ; commit c5ded3eeb |
| 09/10 10:00-10:47 | Remarque 9 ; lemme laplacien de Codex (relu) ; (39,39) annoncé (non relu) | M:114-164 ; commits 17877608a, 07855cf76, 199f150de, f049718ed |
| 09/10 11:20 | §8 : symétrie forcée ou données inexistantes au rang 37 ; coût exhaustif | M:195-231 ; commit 6d2155f3d |
| 09/10 12:30-12:59 | §9 : séries thêta quartiques ; artefacts flottants ; LAB : 64 coins faisables, piste close | M:233-282 ; commits faf2ac76d, 9718e6525, d7e1b8f5e |
| 09/10 13:28-15:07 | §10-11 : proposition 13 ; nombres forcés ; programme à neuf classes (fermé au degré 0) ; contrôle sur srg(243) | M:284-398 ; commits 9ca72369f, 3f37b16f7, 9b797fda2 |
| 09/10 15:11-15:47 | §12 : rang 43 classe par classe | M:400-488 ; commits 452352f13, 055a7e791, bd27d407c |
| 09/10 16:10-16:34 | §13 : S₀, lemme 14, couches forcées, P3/N25 ≥ 10 | M:490-603 ; commits 62af6b1a0, c4f41cac3, 8f3757a43, aae5e1efb |
| 09/10 ~17:0x | Retrait de Codex : « S₀ exclu » retiré | M:607-610 |
| 09/10 17:43-18:58 | §14-15 : certificat P3/N25, Jacobi, identité de budget, congruences, profils | M:605-879 ; commits effd38579 … 9ab032ba2 |
| 09/10 19:47-20:05 | §16 : ordre de l'utilisateur, recherche combinatoire P3/N25 ; crible lancé | M:881-909 ; commit 300c2a6c7 |
| 09/10 21:20 | §17 : lemmes A et B ; 941 supports tués | M:911-956 ; commit a7667ddbb |
| 09/10 23:08 | §18 : niveau 2, lemme C, moteur d'étoile, coquille | M:958-1065 ; commit bdf492708 |
| 10/10 00:02-01:41 | §18.6-18.7 : étoile double, rang 37 (r_low, r_short, compromis, dual) | M:1067-1119 ; commits 65ca98696, d1cb20101, b10b1af9c |
| 10/10 02:35 | §18.8 : 72 verdicts confirmés sans solveur ; 3271 supports ouverts | M:1121-1129 ; commit c118f1aac |

## 3. Ce que chaque famille de branches a exécuté

| Famille (nb de branches) | Période | Code / paramètres | Ce qui a tourné | Issue |
|---|---|---|---|---|
| `run/{pere,frere,toi}-<région>-0` (18) | 29-30/09 | paquet v1 : frame_dfs.py b48cf844, hstage_stream.py cfbfd9c0, twin_transfer.py 77a446c7 ; 26 workers par c7a.8xlarge | tranches 0-17/54 (64 jobs chacune) | 209 enregistrements ; statuts figés EN_COURS (morts avec le compte) |
| `run/slice-19` à `slice-44` (26) | 29-30/09 | idem | tranches 19-44/54 (63 jobs) | 190 enregistrements ; beaucoup morts en moins de 2 h ; tranches 18 et 45-53 jamais lancées |
| `run/qci-*` (16) | 01-07/10 | runners GitHub gratuits, un par paquet v2...v10, plus tests d'arrêt | calibration 118:2:8, 028:x:8, 001:5:4000, 000:31:141, 011:0:2950, 002:9409:23040, r037:0:28 ... | toutes les répétitions de déploiement PASS ; deux FAILED utiles (v2 manifeste, v3 sauvegarde O24) |
| `run/q-i-<instance>` (195) | 01/10 20:12 - 07/10 | paquets v1 à v10 selon la machine ; Spot c7a (8x, 2x, 32x), quelques c7i, 1 c8g ; deux comptes ; On-Demand sur le compte gratuit | jobs stream (lid:k:n), golay_pairs, o24, resolve ; mode DEFERRED (Q_DEFER, Q_DEFER_NODES=0, Q_DEFER_N4) ; tail runners (par_consumer, Q_TAIL_KEYS) ; puis hors file le 07/10 : certificats (Q_CERT), audit H2 (Q_AUDIT), F4 (Q_F4), reprises 713 / 28 / 044 / 105 | 61 INTERRUPTED (Spot), 60 STOP, 43 FINI, 3 ERREUR AGENT, 1 STOP CALIB (ARM), statuts figés pour les autres |
| `queue` (file principale), `queue-ci`, `queue-cid` (files des répétitions) | 01/10-07/10 | `events.jsonl`, `order.txt`, `control.json` | file principale : 24 880 événements, 145 machines, 17 024 clés | toutes faites sauf 003:181:182 (L02_C2_aws-002) |
| `v2`...`v10`, `v10-fetch-retry` | 01-06/10 | branches de construction des paquets (HANDOFF et code à l'état de chaque version) | - | fusionnées sur master après répétition CI |
| `tail-runner`, `defer-mode`, `defer-quick`, `defer-n4`, `agent-backlog`, `tmp/push-test-laptop` | 06-07/10 | branches de travail (tail runner, mise de côté, N4, correctif de contention, poussées du laptop) | - | fusionnées ; leurs copies de HANDOFF, LEMMA_TARGET, T18_REPORT, T20_PROOF, FINAL_STATEMENT sont des états antérieurs |
| `lemma-run/*` (15), `lemma-archive/t20_n3_routeB` | 07/10 | boîte de calcul « lemma/cloud » (compte gratuit) | énumérations de T20 (cas I, n_3 = 0 et 2) | voir partie C |
| `lab-records-2026-10-07` | 07/10 | copie de `data/finishC` du PC du labo | enregistrements locaux des 27/09-07/10 | « not a certified archive » |

Correspondance paquet -> moteur sur les enregistrements (recompte L02) : v1 b48cf844 ; v2-v4 frame_dfs_next 41fbcbff ; v5-v9 267d2bb5 ; v10 1591aeea (15 408 enregistrements). Détail : L02_C2_aws-003, L02_C2_aws-014.

## 4. Couverture

**Par méthode (table générée `B_TABLE_156.md`, partition 000-155 vérifiée par l'agent L02).**

| Méthode | Réseaux | Paires | Par recherche | T18 | T20 | Où sont les enregistrements |
|---|---|---|---|---|---|---|
| S (balayage stream) | 91 | 220 260 576 | 22 702 398 | 0 | 0 | colonne « records » : 33 branches run/*, 13 PC du labo en partie sur branches, 45 PC du labo (dont 17 ont aussi des enregistrements v10 de la reprise 713 sur branches : recompte L02) |
| SD (stream v10 + T18/T20) | 11 | 372 603 641 | 3 073 229 | 5 179 532 | 2 501 532 | branches run/* |
| GD (Golay 001, 002) | 2 | 835 490 | - | 11 220 | 6 763 | branches run/* |
| G (Golay 004, 010) | 2 | 416 383 + 3 962 classes | - | - | - | PC du labo (copies aussi sur run/*) |
| O (000, O24) | 1 | 141 classes | 55 cherchées | - | - | PC du labo (47 classes aussi sur run/*) |
| H (h-stage, 28-29/09) | 13 | - | - | - | - | PC du labo ; repris en v10 le 07/10 |
| F (frame_dfs + lemme U+, 27/09) | 14 | - | - | - | - | PC du labo ; repris en v10 le 07/10 |
| H3 (115, 132) | 2 | - | - | - | - | PC du labo ; repris en v10 |
| P, EP, SP, So, B (niveau réseau) | 20 | - | - | - | - | aucun enregistrement de paires |
| **Total** | **156** | **593 699 707** | **25 775 627** | **5 190 752** | **2 508 295** | |

Sources : `master:lemma/PROOF_C2/B_TABLE_156.md:6-24,183-187` ; `master:lemma/PROOF_C2/B_LATTICES.md:22-52`.

**Sur les branches run/*** : 108 réseaux ont au moins un enregistrement ; 48 n'en ont aucun : les 20 réseaux de niveau réseau et 28 réseaux S calculés au seul PC du labo (060, 065-069, 071, 076, 077, 079-086, 088-093, 103, 109, 110, 113, 149), dont les enregistrements ne sont que sur `lab-records-2026-10-07` (copie non certifiée). Recompte L02.

**Tranches** : 44 des 54 tranches du 29/09 ont tourné (aucune branche pour 18 et 45-53) ; ce manque est sans effet final, car la file adaptative a été construite depuis l'état réel du labo (jobs non faits seulement) ; `master:README.md` et `master:REPRO_COMMANDS.md:25-29`.

## 5. Verdicts (sommes sur enregistrements, recompte L02)

- Run 54 tranches : 399 enregistrements, 32 041 201 paires, 0 INCOMPLETE (L02_C2_aws-001).
- File q-i, stream : 12 413 enregistrements uniques ; char-vector trap 251 072 836 ; swap 232 276 668 ; twin-deferred 31 108 012 ; stage 1 vide 21 722 072 ; dual-min 9/7 13 224 254 ; DEFERRED T18 5 179 532 ; TWIN-CANON 2 863 198 ; DEFERRED T20 2 501 532 ; twin transfer 1 525 782 ; no local star sums 95 653 ; INCOMPLETE 160. Les sommes chevauchent entre découpages ; les nombres DEFERRED coïncident avec ceux de la table B.
- File q-i, golay_pairs : 5 038 enregistrements uniques ; char-vector 932 487 ; stage 1 vide 165 368 ; no local star sums 128 820 ; dual-min 19 055 ; DEFERRED T18 11 282 et T20 6 815 (chevauchement des blocs grossiers et fins ; la table B donne 11 220 et 6 763 paires distinctes) ; twin transfer 218 ; INCOMPLETE 118 ; no joint star sums 6.
- o24 : 47 classes EMPTY ; resolve : 143 paires, 139 « stage 1 empty », 4 « no local star sums ».
- Recompte officiel des 91 réseaux S : 220 260 576 paires = 97 628 147 d'emblée + 22 702 398 par recherche + 93 822 540 swap + 6 107 330 jumeau, + 161 d'abord INCOMPLETE (L02_C2_aws-024).

## 6. Échecs, délais, bogues et reprises

- Interruptions Spot : 61 machines INTERRUPTED ; 2 500 heures-job perdues sur des jobs de 10-32 h au 03/10 (leçon : jobs courts, prix maximum haut, plusieurs zones) (`master:HANDOFF_2026-10-01.md:536-544`).
- Paires INCOMPLETE : 161 stream + 118 Golay, toutes résolues ou mises de côté (L02_C2_aws-007).
- Cinq jobs tronqués par le producteur à 10^6 candidats y2, refaits avec un plafond relevé (L02_C2_aws-013).
- 003:181:182 : plus de 5 h sur 124 coeurs sans fin, puis exclu sans calcul (L02_C2_aws-020).
- Défauts d'infrastructure : L02_C2_aws-015 ; aucun verdict faux rapporté ; écart de calibration ARM jamais expliqué.
- Reprises de provenance du 07/10 soir : 713 représentants (L02_C2_aws-026), 28 réseaux (L02_C2_aws-028), 105 sans test de budget (H4), audit H2 (L02_C2_aws-018).
- Retraits : total 212 825 691 non reproductible (L02_C2_aws-024) ; phrase sur les 732 paires (L02_C2_aws-029) ; manifeste RERUN_713 de LAP superseded (L02_C2_aws-026) ; vérificateur de témoins sans test d'intégralité (L02_C2_aws-027) ; « wrapper L indisponible » retiré (L02_C2_aws-033).

## 7. Coût

Voir L02_C2_aws-034. En bref : premier compte, septembre 76,77 $ et octobre (crédits épuisés le 06/10, 120,34 $ d'usage d'octobre couverts), puis argent de l'utilisateur jusqu'à un grand livre d'environ 243 $ + 21 $ au prix Spot maximal (borne haute ; réel environ 0,8 à 0,88 du grand livre) ; second compte environ 15 $ de crédits gratuits ; Azure jamais utilisé (couche non construite) ; plus aucune machine sur le compte de l'utilisateur sans son accord depuis le 07/10 18:40 UTC.

## 8. Ce que ces calculs établissent, et avec quel statut

**Énoncés finaux (sans rehausser).**

| énoncé | statut | maillon le plus faible | source |
|---|---|---|---|
| 156 exclusions enregistrées au tracker du labo (000-155), conversion des 13 derniers le 07/10 à 17:47 UTC | S (composite) | verdicts de moteur sans certificat ; T18/T20 acceptés sur relecture IA | L02_C2_aws-021 ; `master:lemma/t20_CODEX/CHECKPOINT_156.md:7-20` |
| « No strongly regular graph with parameters (99, 14, 1, 2) has an automorphism of order 2 » (brouillon 7 ; Théorème 1.1 du papier) | S, avec une composante O | règle jumelle non recertifiée (O) ; 25 775 627 paires par recherche (S) ; énumération comparée sur 4 réseaux | L02_C2_aws-022 ; L02_C2_aws-097 (Théorème 1.1) ; L02_C2_aws-096 (Théorème B) |
| Asymétrie : si le graphe existe, il n'a pas d'automorphisme non trivial | P conditionnel aux ingrédients (A)-(E) | C2 ci-dessus ; ordre 3 (Lean, selon le dépôt conway99-c3-experimental) ; ordre 7 (conway-C7) ; ordre 11 (Behbahani-Lam, non ouvert) | L02_C2_aws-098 ; L02_C2_aws-099 à L02_C2_aws-104 |

**Par maillon de la chaîne.**

| maillon | ce qui l'établit | statut | référence |
|---|---|---|---|
| R0 : une involution fixe exactement un sommet (A.0) | preuve à la main de LAP, relue par Codex | P | L02_C2_aws-042 |
| R1 : Théorème R (repère dans un réseau impair unimodulaire de rang 24 sans norme 1) | preuve à la main, une relecture Codex « errors only » | P | L02_C2_aws-041, L02_C2_aws-043 à L02_C2_aws-052 |
| R2 : les 156 réseaux | classification de Borcherds (citée) ; entrées recalculées exactement par Codex | P cité + E | L02_C2_aws-049, L02_C2_aws-078 |
| R3 : énumération des paires (y1, y2) | producteur C1 ; comparé à un énumérateur indépendant sur 140, 135, 141, 064 | E sur 4 réseaux, sinon code seul | L02_C2_aws-019 |
| R4 : règles du moteur | audit de Codex contre le Théorème R ; trous H1-H5 traités avec des portées inégales | P (audit) ; verdicts S | L02_C2_aws-059 à L02_C2_aws-070 ; L02_C2_aws-018 |
| R5-R7 : T16, T18, T20 | mains + énumérations exactes, deux programmes ou plus ; arbitres IA | P (IA seulement) | L02_C2_aws-112, L02_C2_aws-127, L02_C2_aws-176 |
| R8 : pont et règles de témoins (E = 8, 9, 10) | pont arbitré ; certificats par paire | P + C | L02_C2_aws-157, L02_C2_aws-158 ; L02_C2_aws-017 |
| R8' : corollaire Y1 | preuve de trois lignes (Codex) ; certificats vérifiés par deux vérificateurs | P + C | L02_C2_aws-160 ; L02_C2_aws-020, L02_C2_aws-025 |
| R9 : couverture des 156 | recompte des enregistrements, certificats, reprises | E (recomptes) de verdicts S et de certificats C | L02_C2_aws-023, L02_C2_aws-024 |

**Ce que la campagne AWS apporte en propre (branches `run/*`).**

- **Balayages stream** (paquets v1 à v10) pour 33 réseaux entièrement couverts par des enregistrements de machine, 13 en partie, et
  les reprises v10 de 2026-10-07 (25 réseaux de la reprise 713, 28 anciens réseaux, 105) : verdicts S.
- **Balayage de mise de côté** des 13 derniers réseaux (DEFERRED T18/T20) et **certificats** des paires mises de côté (7 762
  enregistrements stream bons ; 17 983 paires Golay) : S pour les paires cherchées, C pour les témoins (L02_C2_aws-016, L02_C2_aws-017).
- **Golay** 004 (416 383 classes) et 010 (3 962) en blocs v4 ; 001 et 002 en blocs v10 ; **O24** : 47 classes EMPTY (L02_C2_aws-004,
  L02_C2_aws-005).
- **Résolution des INCOMPLETE** (jobs resolve v6/v8) (L02_C2_aws-007).
- **Audit H2** (noyau rigide, 25/25), **F4** (énumérateur indépendant sur 4 réseaux), **calculs de T20** (branches `lemma-run/*`,
  voir partie C, L02_C2_aws-212 à L02_C2_aws-218).

**Recoupement avec l'énoncé final (brouillon 7) et la partie B du document de preuve.** Les nombres concordent : 5 190 752 et
2 508 295 paires, 7 762 certificats, 25/25 réseaux audités, 147 475 940 paires lues, F4 sur quatre réseaux, 220 260 576 paires
(B.2). Les recomptes L02 sur les branches retrouvent exactement les totaux DEFERRED de la table B. Écarts relevés : section 14.

## 9. Écarts de couverture

| écart | portée | statut | référence |
|---|---|---|---|
| Tranches 18 et 45-53 du plan du 29/09 jamais lancées | sans effet final (file reconstruite depuis l'état réel du labo) | E | L02_C2_aws-001 |
| 28 réseaux S sans aucun enregistrement sur une branche `run/*` | archivage : enregistrements seulement dans la copie `lab-records-2026-10-07` (« not a certified archive ») | E | L02_C2_aws-040 |
| Environ 780 représentants y1 (tier L) | enregistrements du PC du 29/09, programme identifié, ni refaits ni couverts par Y1 (la partie D donne la borne « au plus 946 ») | E (dérivé) | L02_C2_aws-039 |
| 003:181 | aucun enregistrement de paires ; couvert par le certificat à y1 fixé (dépend de T18, T20) | C | L02_C2_aws-020 |
| 044 (8 chunks une seule fois) | un seul passage, contre deux machines pour les autres reprises (105, refait pour H4, a des flux identiques sur AWS et sur le PC) | S | L02_C2_aws-028 ; `master:lemma/FINAL_STATEMENT_DRAFT.md:51` |
| 000, 004, 010 | enregistrements anciens, une seule lecture ; 86 certificats LP et 55 recherches de 000 non refaits | S / C | L02_C2_aws-004, L02_C2_aws-005 |
| Énumération des paires | comparée à un énumérateur indépendant sur 4 réseaux sur 136 réseaux à paires | O | L02_C2_aws-019, L02_C2_aws-038 |
| Recherches sans certificat | 25 775 627 paires | S | L02_C2_aws-038 |
| Règle de transfert jumeau | au plus 2 479 669 paires à recertifier | O | L02_C2_aws-030 |
| Survivants des 28 réseaux | min E >= 11 des 2 652 paires non revérifié ; 1 610 témoins caractéristiques non rejoués (1 042 compte rapporté) | O | L02_C2_aws-027, L02_C2_aws-029 |
| Indépendance de plateforme | calibration différente sur aarch64, jamais expliquée ; nombres de noeuds dépendant du CPU | O | L02_C2_aws-037 |
| T20 : comptes de noeuds de I.0 (4,2,1) et I.5 (4,2,1) | 33 511 et 27 524 dans le texte contre 51 241 et 48 823 sur les branches citées (0 configuration complète partout) | E (écart vu par la partie C) | L02_C2_aws-218 |
| H2 | couverture 25/25 au niveau des archives seulement (Codex) | E | L02_C2_aws-065 |
| H4 | « closed » pour 105 selon LAB ; « not a global H4 closure » selon Codex (12 620 paires « pair budget ») | E / O | L02_C2_aws-069 |

## 10. Détails par partie

### Partie B : T16, T18 et le pont : Résumé

- **T16** (norme carrée 16, d'où min L* >= 9/7) : dossier ChatGPT du 04/10 (cube à la main ; Wagner à la main + classification
  finie exacte certifiée), contrôlé par LAB et un agent indépendant le 04/10, arbitré par Codex le 07/10 (« no blocking
  mathematical error », un défaut de vérificateur couvert). Filtre moteur v10 (W8 / FD_MIN97 : norme 3, Y = 13).
- **T18** (norme carrée 18) : LAP et agents, 06-07/10 ; à la main : réduction à B0 = K3 x K3, B1, B2 = C9(1,2), n_3 = 0, profils
  (2,5,0), (3,3,1), (4,1,2), (4,1,2) exclu ; le reste par énumérations exactes à au moins deux implémentations ; 4 survivants de
  B1 tués par la borne de rang et par l'étape D. Deux arbitres IA sans erreur ; v2 non relue ; acceptée par l'utilisateur (IA seules).
- **Pont** : tout v de U donne une fonction propre (-4) entière sigma-impaire de norme carrée 2E(v) ; d'où W8/W9/W10 et le
  Corollaire Y1 (Codex). Arbitré sans erreur ; H4 à certifier paire par paire.
- **Usage** : T18 jamais dans le moteur ; report puis conversion des paires (5 190 752 paires reposent sur T18).

### Partie B : T16, T18 et le pont : Versions multiples

- `LEMMA_TARGET_2026-10-06.md` : `origin/tail-runner` (6 689 o, §1-4), `origin/defer-mode` (14 824 o, §1-10),
  `origin/agent-backlog` (17 171 o, §1-11) sont des **préfixes stricts** de master (19 057 o, §1-12) : le diff ne montre que des
  ajouts.
- `lemma/t18/T18_REPORT.md` : `origin/defer-mode` (620 lignes) est un **état antérieur** sans la fin du round 4 (sections B, C, D,
  « Final lines », tableau d'état de B1) ; deux phrases d'état diffèrent (ligne 6 ; lignes 508-510 : « the whole of profile
  (3,3,1) (one implementation) » devient « steps 2-3 of profile (3,3,1) ») : mise à jour, pas divergence de fond.
- `lemma/BRIDGE.md` : `origin/defer-n4` (460 lignes, commit d54db2ab2) est un **état antérieur** : corrections de l'arbitre listées
  en tête mais non fusionnées, deux phrases ensuite retirées (L02_C2_aws-162, L02_C2_aws-163), sans Corollaire Y1. `lemma/bridge/BRIDGE.txt` est la
  version d'origine (avant arbitrage, sans bandeau).
- `lemma/t18_PROOF/T18_PROOF_v1.md` est identique octet pour octet à la première version de `T18_PROOF.md` (commit e657f46c3) ;
  la v2 ajoute §9.6, §9.7, A.7 et les 70 modifications de `T18_PROOF_v2_changes.txt` (comparé au niveau de la liste seulement).
- `lemma/t18_B0/b0_body_src.txt` = corps de `t18_B0/REPORT.md` (identique) ; `b0_final_note.txt` = sa section finale.

### Partie C : T20 et les calculs des branches lemma-run : Résumé

- T20 est écrit comme Théorème 10.2 de `lemma/T20_PROOF.md` (master 474aa859a, 07/10) : à la main jusqu'aux neuf configurations du
  support, puis huit calculs (4.12, 7.4, 7.5, 8.8, 8.9, 9.19, 9.20, 9.29), chacun avec deux programmes ; 0 configuration complète partout.
- Arbitre : Codex seul (IA), deux passages et un passage sur l'article : « no blocking error », Théorème 10.2 « conditional on all its
  stated Computations ». Aucun lecteur humain. Code des moteurs non audité ligne à ligne.
- L'utilisateur a « accepté » T20 dans le registre du labo sur le blob e50d5be079 (état a730e7b5e, avant la fusion du contrat G2) ;
  conversion des 13 derniers réseaux à 17:47 UTC (156/156).
- Réserves vivantes : les seconds programmes suivent le plan d'unités du premier (contrat G2, formulation finale non relue) ; III.1
  partage modèle et squelette ; certificats seulement échantillonnés ; fichiers par base de trois cas portables et plans de III.1 hors git.
- Écart vu par moi, absent des notes : I.0 (4,2,1) et I.5 (4,2,1) ont 33,511 et 27,524 nœuds dans le texte (runs portables) mais 51,241
  et 48,823 sur les branches nuage que ARTIFACTS cite pour ces cas ; les deux runs concluent 0 configuration complète.

### Partie C : T20 et les calculs des branches lemma-run : Sous-cas de T20 : ce qui les exclut

| Sous-cas | Exclu par | Comptes | Date, auteur | Arbitre | Réserves |
|---|---|---|---|---|---|
| Valeurs +-2, +-3 ; motif {2,1^6} | main (Lemmes 3.1, 3.2, Prop. 3.3) | - | 06/10, agent LAP round 1 | Codex : vérifié | cas d'égalité vu par l'auteur seul (10.4 item 12) |
| k impair ou >= 6 ; e >= 2 | main (4.1-4.5) | - | 06/10, round 1 | Codex : vérifié | - |
| IIb (arête plus interne-externe) | main (4.7) + 0 structure (deux énumérateurs) | 1,463,867 / 10,596,116 nœuds | 06/10 | Codex : vérifié | - |
| Réduction aux neuf configurations | main + Calcul 4.12 | 27720 / 2880 / 0 / 10080 étiquetées | 06/10 | Codex : ordres d'automorphismes recontrôlés | ordres d'aut. par un énumérateur (+ deux contrôles), second sans test d'isomorphisme |
| III.0 | Calcul 7.4 | 130,004 nœuds, 0 au niveau 10 | 07/10, agent LAP round 2 | modèle relu | deux implémentations partageant `cases.py` ; le second suit le plan |
| III.1 | Calcul 7.5 + seconde vérification | 1,628,864 nœuds ; 1 rejet par rang, aussi mort sans rang | 07/10, LAP (agents) | G3 : indépendance partielle | modèle et squelette partagés ; plans, journaux, certificats hors git |
| IIa.0 | Lemmes 8.1-8.6 + Calculs 8.8, 8.9 | 180 -> 87 ; 45,497 nœuds | 07/10, agent LAP round 2 | modèle relu | listes partagées `iia_w.json` (comparées) |
| Cas I : d = 3 dans N(p), n_3 = 4, profil (5,0,2) | main (9.1, 9.2, 9.4) | - | 07/10, round 2 | Codex : vérifié | - |
| Cas I, n_3 = 0, 6 graphes x (3,4,0), (4,2,1) | Calculs 9.19, 9.20 | 615,405 bases, 15,762,181 nœuds, prof. <= 5 ; rang : 15 nœuds de I.1 (premiers programmes seulement) | 07/10, agent LAP round 3 ; nuage LAP | modèle relu | premier programme : 3 cas portables (fichiers hors git) + 9 nuage ; second : portable (I.0, I.5 (4,2,1)) + nuage (douze cas) ; écart de comptes I.0/I.5 (4,2,1) |
| Cas I, n_3 = 2 (route B) | Lemmes 9.22, 9.23, 9.27, 9.28 + Calcul 9.29 | 64,528 bases, 86,968 nœuds, <= 3 orbites, pas de rang | 07/10, agent LAP | addendum : aucune erreur bloquante | deux programmes de la même session, un portable ; sorties brutes archivées non certifiées |
| Cas I, n_3 = 2 (route A) | non utilisé | 183 de 700 classes fermées, 421 ouvertes | 07/10, LAB | - | abandonnée sur coût |
| Rang (16 nœuds) | seconds programmes sans borne de rang | III.1 1 ; I.1 13 + 2 | 07/10 | Codex : enregistrements vérifiés | - |

### Partie C : T20 et les calculs des branches lemma-run : Calculs sur les branches (agrégat)

| Branche | Cas | Machine, processus | Début-fin (UTC) | État final | Programmes, version | Comptes | Fichiers |
|---|---|---|---|---|---|---|---|
| `lemma-run/selftest-i-0dee8516208b24d42` | 60 s de III.0 | nproc 8 (versions.txt) | -> 10:20:35 | FINISHED exit=0 | eng5 | 768 tâches sur 769, timeout True, 0 complète | 7 |
| `lemma-run/t20_I_rest-i-02f356c70da99d700` | 9 cas n_3 = 0 (tous sauf I.0 (4,2,1), I.0 (3,4,0), I.5 (4,2,1)) | 128 processus ; instance non décrite | 10:36:23-10:57:06 | FINISHED exit=0 | premier seul, v1 | 9 x COMPLETE True, 0 complète ; rang 13 + 2 (I.1) | 4,648 (9 x 128 logs s1, 128 logs s2, 128 jsonl, 128 sum.json) |
| `lemma-run/t20_I1_340-i-019e86d399c17954f` | I.1 (3,4,0) | compte utilisateur 128 vCPU eu-west-2 ; 128 processus | 11:19:43-11:52:31 | FINISHED exit=0 | deux, v2 | 7,279,961 nœuds ; d'accord ; 13 nœuds de rang fermés sans rang ; 200,534,596 vecteurs entiers | 904 ; pas d'ALL.txt |
| `lemma-run/t20_Iv_A-i-0390fd53333c148ad` | I.1 (3,4,0) prévu | 8 vCPU | 11:00:33 | INSTALLING seulement | - | - | 1 |
| `lemma-run/t20_Iv_B-i-0a03ce79bff09fa5d` | I.3 (3,4,0), I.0 (3,4,0) | 8 processus (gratuit) | 11:01:04-13:19:43 | FINISHED exit=0 | deux, v1 | 2,055,948 et 250,504 nœuds, d'accord | 126 |
| `lemma-run/t20_Iv_C-i-092f5550d84f61e09` | I.4 (3,4,0), I.3 (4,2,1) | 8 | 11:01:02-12:43:19 | FINISHED exit=0 | deux, v1 | 1,200,322 et 427,984 | 126 |
| `lemma-run/t20_Iv_D-i-09169834049067883` | I.2 (3,4,0), I.4 (4,2,1) | 8 | 11:04:36-13:11:24 | FINISHED exit=0 | deux, v1 | 2,053,687 et 237,408 | 126 |
| `lemma-run/t20_Iv_E-i-0cd9427b48ee5704e` | I.5 (3,4,0) ; I.1 (4,2,1) | 8, Spot | 11:01:19-(12:12:07) | RUNNING, machine reprise 12:22 | deux, v1 ; v1 avorte sur I.1 (4,2,1) « plan out of step » | 366,642, d'accord ; I.1 (4,2,1) non utilisé | 133 |
| `lemma-run/t20_Iv_F-i-0c5414832a6ac4ff5` | I.2 (4,2,1) (+ I.0, I.5 (4,2,1) prévus) | 8, Spot | 11:01:17-(11:11:17) | RUNNING, reprise ~11:15 | - | non utilisé | 72 |
| `lemma-run/t20_Iv_G-i-05703a74fbb027423` | I.1 (4,2,1) | 8 vCPU us-east-2, à la demande | 13:19:09-14:33:09 | FINISHED exit=0 | deux, v2 | 1,406,917 ; 2 nœuds de rang fermés sans rang | 65 |
| `lemma-run/t20_Iv_H-i-004334efafb6ceb56` | I.2 (4,2,1) | 8 | 13:19:30-13:41:09 | FINISHED exit=0 | deux, v2 | 421,773 | 65 |
| `lemma-run/t20_Iv_I-i-032b7d25d335204f8` | I.0 (4,2,1) | 8 | 13:19:39-13:22:33 | FINISHED exit=0 | deux, v2 | 51,241 (texte : 33,511) | 65 |
| `lemma-run/t20_Iv_J-i-038ea54927e5a01c4` | I.5 (4,2,1) | 8 | 13:19:21-13:23:08 | FINISHED exit=0 | deux, v2 | 48,823 (texte : 27,524) | 65 |
| `lemma-run/t20_n3-i-0b8ae938c1fc89c62` | route A, 700 classes | 128 processus (8/41/16/22/27/14) | -> 10:51:40 | RUNNING (arrêté) | eng5z (LAB), un programme | 168 bases fermées, 0 survivant, 4,864,767 nœuds, 139 rejets de rang | 594 |
| `lemma-run/t20_n3-i-04bb3ac564f658b79` | route A, relance | 128 | 11:14-> 11:35:31 (arrêt 11:43) | RUNNING (arrêté) | eng5z | 183 fermées, 5,825,640 nœuds, 163 rejets de rang | 622 |
| `lemma-run/t20_n3_sample-i-0cefd01aef8eade8a` | mesure route A | 8 vCPU eu-north-1 | 11:50-> 12:30:42 | RUNNING (arrêté) | n3_split.py sample | 160 des 421 bases échantillonnées ; SUMMARY_before : 183 + 96 à la main, 421 ouvertes | 954 (330 sample) |
| `lemma-archive/t20_n3_routeB` | sorties brutes du Calcul 9.29 | portable | commit 17:25 +0200 | archive | deux programmes, v3 | 50 cas | 519 (39.6 Mo) |

Format des parties (échantillons lus) : `parts/s2_<i>of<N>.sum.json` (résumé de partie, champ `width`), `.jsonl` (une ligne par base
avec son plan, 5 champs par ligne en v1, 6 en v2), `parts/vf_<i>of<N>.json` (vérificateur), `logs/*.out`. Les fichiers par partie ont
été comptés, pas lus (sauf un échantillon). Les champs `nproc` des STATUS sont faussés par OMP_NUM_THREADS=1 (`lemma/cloud/README.md:12-13`).

### Partie D : réduction, audits, papier : Résumé

1. La réduction « involution ⇒ repère de 51 vecteurs dans l'un des 156 réseaux de Borcherds » (Théorème R, A.0 à A.9) a été
   prouvée à la main par LAP le 07/10. Codex l'a relue une fois, en mode « errors only » : « No mathematical error found ».
   Elle n'utilise plus Makhnev-Minakova (A.0 prouve F0) ni l'hypothèse g ∈ {18,20} (A.4 traite tout g).
2. Codex a audité les règles du moteur : toutes découlent de R et aucune n'utilise g. L'exécutable avait cinq trous, H1 à H5,
   traités le jour même avec des portées inégales. H1 n'est pas exercé. H2 est couvert à 25/25 au niveau des archives.
   H3 est certifié pour les listes locales. H4 n'est levé que pour 143 selon Codex (et pour 105 selon LAB). H5 est levé par T16.
3. 20 réseaux sont exclus sans énumérer de paires : 18 par empilement ou piège dual (recalculés exactement par Codex), 152 et
   153 par indécomposabilité, et 143 par une preuve à la main, avec le certificat 378 ≤ 336.
4. Les 136 autres réseaux reposent sur quatre éléments : l'énumération des paires (comparée à un énumérateur indépendant sur
   4 réseaux seulement) ; un seul programme de recherche, sans certificat (environ 2,6·10^7 paires) ; des témoins certifiés via
   T16, T18, T20 (lemmes assistés par ordinateur, relus par des sessions IA) ; la règle de transfert.
5. Pour au plus 2 479 669 paires transférées par les formes « statut » ou « même réseau », la recertification n'est pas faite.
   C'est le seul point de calcul ouvert du papier, estimé à au moins ~100 cœur-heures.
6. Le papier énonce « pas d'automorphisme d'ordre 2 ». Avec MM04, D3 (Lean), BL11 et D7 (Lean), il en tire l'asymétrie, qui
   est conditionnelle aux ingrédients (A) à (E). Aucun lecteur humain ; rien n'est formalisé pour C2 ; les dépôts sont privés.

### Partie A : matériau C1 hébergé dans le dépôt : Résumé (10 lignes)

1. Périmètre : HANDOFF_2026-10-01.md lignes 1173-2019 (07/10 21:05 UTC → 09/10 05:12 UTC), `c1_rank37_girth5_lines/` (NOTE.md + données), `c1_mandat_c_transformations/` (RECHERCHE_C_TRANSFORMATIONS.md, 1129 lignes, 09/10 09:29 UTC → 10/10 02:35 UTC), messages de commit du 07/10 au 10/10. Le dossier `c1-lap-girth5-audit/` n'existe nulle part.
2. Rangs exclus dans ce matériau : r ≥ 33 puis r ≥ 35 (PL thêta exact du labo, audité par Codex), puis rang 35 exclu le 08/10 au matin (Codex notes 179-184 + labo ; audit partiel à la main par LAP, recensements non vérifiés). Donc r = rang₇(A − 3I) ∈ {37, 39, 41, 43}. AUCUN autre rang n'est exclu (dit et répété : HANDOFF 1882, 2000 ; Mandat C 1065).
3. Rang 37, route de comptage (b₄ contre collisions de paires jumelles / grilles) : close pour les supports ≤ 9 (L02_C2_aws-324, L02_C2_aws-326) ; l'énoncé manquant est une minoration du 7-rang des classes de jumeaux/grilles (espace de dimension 18) en fonction du nombre de paires jumelles (< ~540) (L02_C2_aws-335). La cible « au plus 10 relations » a été retirée (L02_C2_aws-340, L02_C2_aws-341).
4. Rang 37, résultats locaux assistés par ordinateur : une droite de maille ≥ 5 est connexe (L02_C2_aws-364, audit partiel de Codex note 224) ; profils (2,2,2) et (3,3) sans prisme morts ; l'énoncé B (droites sans prisme connexes) est INCOMPLET (12 670 + 147 boules et 17 tests manquants, L02_C2_aws-377).
5. Mandat C : rigidité (pas de mouvement par bloc orthogonal sur < 9 sommets ; au rang 37 générique une seule complétion parmi tous les rangs, lemme de Codex relu par LAP) ; symétrie forcée seulement conditionnelle ; route « transformations » close (L02_C2_aws-382-A131).
6. Rang 43, scénario S₀ (pas de racine, pas de norme 16-24) : série thêta déterminée ; identité exacte certifiée « #P3/N25 = 10 + objets bas » (L02_C2_aws-423) ; identité de budget pour tout le rang 43 (L02_C2_aws-431) ; S₀ a toujours un objet bas (L02_C2_aws-432) ; l'annonce de Codex « S₀ exclu » est retirée (L02_C2_aws-422).
7. Recherche P3/N25 : 4581 supports → 3271 ouverts ; 1310 tués avec témoins vérifiables sans solveur (lemmes A, B, C à la main ; 72 verdicts de solveur confirmés par énumération exhaustive) (L02_C2_aws-453).
8. Statuts : 75 E, 74 P, 11 H, 8 C, 8 O, 7 S, 5 X, 4 R.
9. Presque tout ce qui est « P » ici est à la main par LAP et non relu par un tiers ; les relectures tierces explicites : r ≥ 33/35 (Codex), lemme N16 (labo), identités τ/dét (Codex 217), maille 5 (Codex 224 partiel), lemme laplacien de Codex (relu par LAP).
10. Auteurs : LAP = la session « portable » qui écrit le HANDOFF et le Mandat C (MC 3 : « Session LAP » ; MC 884 : « Portable seulement ») ; LAB = session du labo ; Codex (= « Astra », HANDOFF 1206).

## 11. Table des résultats

Générée depuis `fiches/L02_C2_aws.jsonl` (énoncé complet, sources, dépendances et remarques dans le JSONL). Colonne « partie » : K campagne, D réduction et papier, B T16/T18/pont, C T20, A matériau C1, L combinaisons repérées par l'agent L02.

| id | partie | énoncé court | statut | relu par | source principale |
|---|---|---|---|---|---|
| L02_C2_aws-001 | K | Run 54 tranches du 29-30/09 (moteur v1) : 399 jobs finis | S | importeur du labo (vérifie le sha du moteur par résultat)... | `master:OLD_README_54_TRANCHES.md:1-12` |
| L02_C2_aws-002 | K | File adaptative c2q-20261001 : 17 024 clés, toutes faites sauf 003:181:182 | E | recompte de l'agent L02 (lecture seule de origin/queue:ev... | `origin/queue:events.jsonl` |
| L02_C2_aws-003 | K | Paquets v1 à v10 : versions du moteur et changements | E | répétitions CI (calibration EQUIVALENT) ; correspondance ... | `master:HANDOFF_2026-10-01.md:14,155-171,192-218,247-254,303-307,371-380,559-564,589-594` |
| L02_C2_aws-004 | K | O24 (réseau 000) exclu le 02/10 vers 01:10 UTC | S | arithmétique des ensembles OK-RECOMPUTED le 07/10 ; certi... | `master:HANDOFF_2026-10-01.md:197-200,241-242` |
| L02_C2_aws-005 | K | Réseaux Golay 010 et 004 exclus le 02/10 | S | OK-RECOMPUTED depuis les blocs stockés (07/10) | `master:HANDOFF_2026-10-01.md:243-246,403` |
| L02_C2_aws-006 | K | Cascade du 02/10 : 109 -> 132 réseaux exclus | S | simulation préalable sur copie ; dépendances jumelles 1 6... | `master:HANDOFF_2026-10-01.md:286-292,359-370` |
| L02_C2_aws-007 | K | Paires INCOMPLETE : toutes résolues EXCLUDED | S | Codex (lien des enregistrements, pas les recherches) | `master:lemma/t20_CODEX/CHECKPOINT_156.md:104-112` |
| L02_C2_aws-008 | K | Loi K + E(y1) + E(y2) = 3\|Phi\|/4 + 8 (étude de cascade) | P | non indiqué dans ce dépôt | `master:HANDOFF_2026-10-01.md:386-389` |
| L02_C2_aws-009 | K | Arrêt du 03/10 à 139/156 et coûts réels mesurés | E | mesures du grand livre et des événements de la file (source) | `master:HANDOFF_2026-10-01.md:416-436,462-511,513-544` |
| L02_C2_aws-010 | K | Second compte et paquet v9 : 018, 019, 017 exclus (142/156) | S | importeur du labo | `master:HANDOFF_2026-10-01.md:546-578` |
| L02_C2_aws-011 | K | Temps v10 mesurés et localisation du coût de recherche | E | non (mesures de la session laptop) | `master:measures/V10_TIMINGS_2026-10-06.md:8-17,36-38` |
| L02_C2_aws-012 | K | Mode de mise de côté (DEFERRED) : conception et validation | E | répétitions CI et comparaisons laptop ; règle N4 vérifiée... | `master:HANDOFF_2026-10-01.md:744-761,774-802,837-852,931-937` |
| L02_C2_aws-013 | K | Cinq jobs tronqués par le producteur (max_out = 10^6) | S | labo (importeur, ligne D4 du tableau) | `master:HANDOFF_2026-10-01.md:897-907` |
| L02_C2_aws-014 | K | Recensement des branches run/* (recompte L02) | E | recompte de l'agent L02 (lecture seule, git cat-file) | `origin/run/*:status.txt, done.txt, results/*.jsonl, tail_agent.txt (script L02_runs.py)` |
| L02_C2_aws-015 | K | Incidents et défauts de l'infrastructure (aucun verdict faux rapporté) | E | répétitions CI après chaque correctif (source) | `master:HANDOFF_2026-10-01.md:97-100,169-171,197-198,248-254,365,405-406,459-460,627-630...` |
| L02_C2_aws-016 | K | Balayage de mise de côté terminé : 13 réseaux, 5 190 752 + 2 508 295 paires | S | importeur du labo (import_sweep.py) ; recompte L02 identi... | `master:HANDOFF_2026-10-01.md:929-937` |
| L02_C2_aws-017 | K | Certificats des paires mises de côté : 7 762 / 7 762 enregistrements bons | C | cert_census.py (labo) ; machines qcert | `master:measures/CERT_CENSUS_2026-10-07.json` |
| L02_C2_aws-018 | K | Audit H2 du noyau rigide : 25/25 réseaux, 0 paire non réexclue | S | collecteur et premier rapport relus par Codex (AUDIT_ENGI... | `master:lemma/FINAL_STATEMENT_DRAFT.md:49` |
| L02_C2_aws-019 | K | Comparaison F4 de l'énumération des paires : égale sur 4 réseaux | E | Codex (lecture de f4/064_compare.json et de f4_compare.py... | `master:lemma/FINAL_STATEMENT_DRAFT.md:25` |
| L02_C2_aws-020 | K | 003:181:182 exclu sans calcul par le corollaire Y1 | C | preuve de 3 lignes relue par LAB et LAP ; certificat véri... | `master:lemma/t20_CODEX/FIXED_Y1_003.md:5-35,37-63,65-92,111-125` |
| L02_C2_aws-021 | K | Conversion du 07/10 17:47 UTC : 156/156 exclusions enregistrées | S | Codex (CHECKPOINT_156, lecture seule) | `master:lemma/t20_CODEX/CHECKPOINT_156.md:7-20,76-81` |
| L02_C2_aws-022 | K | Énoncé final de la route (C) : pas d'automorphisme d'ordre 2 (sous conditions) | S | sessions IA seulement (LAB, LAP, Codex) ; aucun lecteur h... | `master:lemma/FINAL_STATEMENT_DRAFT.md:1-32,116-128` |
| L02_C2_aws-023 | K | Couverture des 156 réseaux par méthode (table générée B_TABLE_156) | E | le générateur vérifie ses assertions avant écriture (sour... | `master:lemma/PROOF_C2/B_TABLE_156.md:3-24,183-187` |
| L02_C2_aws-024 | K | Recompte des 91 réseaux S : 220 260 576 paires (remplace 212 825 691) | E | Codex (arithmétique par réseau et totaux vérifiés) | `master:lemma/PROOF_C2/B_LATTICES.md:58,70-86` |
| L02_C2_aws-025 | K | Certificats Y1 sur les 55 réseaux S hors paquet : 9 143 / 10 802 représentants | C | Codex (vérificateur indépendant, sans catalogue de racine... | `master:lemma/PROOF_C2/B_LATTICES.md:88-93` |
| L02_C2_aws-026 | K | Reprise des 713 représentants sans programme identifié : 2 419 830 paires exclues | S | Codex (REFEREE_RERUN_713 : deux enregistrements de chaque... | `master:lemma/PROOF_C2/B_LATTICES.md:95-112` |
| L02_C2_aws-027 | K | Les 28 réseaux des anciennes listes de paires par les lemmes seuls | C | Codex (REFEREE_HAND_WITNESSES : 171 056 témoins et 4 073 ... | `master:lemma/PROOF_C2/B_LATTICES.md:125-183` |
| L02_C2_aws-028 | K | Les 28 réseaux repris en entier par le moteur v10 | S | rerun_713_check.py renforcé après la revue de Codex ; 044... | `master:lemma/PROOF_C2/B_LATTICES.md:185-207` |
| L02_C2_aws-029 | K | Correction : les 732 paires sans témoin de dix réseaux ne sont pas toutes exclues par recherche | X | Codex (REFEREE_TWIN_DEPENDENCIES section 7 : arithmétique... | `master:lemma/PROOF_C2/B_LATTICES.md:190-200` |
| L02_C2_aws-030 | K | Règle de transfert jumeau : recertification non faite (point ouvert du papier) | O | Codex (REFEREE_TWIN_DEPENDENCIES) ; aide exacte q/codex_e... | `master:HANDOFF_2026-10-01.md:1118-1125,1135-1143` |
| L02_C2_aws-031 | K | Acceptation de T18 et T20 par l'utilisateur (17:47 UTC) : portée | P | sessions IA seulement (deux arbitres pour T18 ; Codex pou... | `master:measures/lemmas_accepted_2026-10-07.json` |
| L02_C2_aws-032 | K | Provenance des enregistrements des 143 réseaux exclus avant la conversion | E | non (le script localise les enregistrements, il ne rederi... | `master:lemma/FINAL_STATEMENT_DRAFT.md:90-100` |
| L02_C2_aws-033 | K | Datation des 132 enregistrements sans version : inférence | H | Codex (hachages LF et CRLF des 19 sauvegardes recalculés ... | `master:q/tools/lab_2026-10-07/engine_history/README.md:3-18` |
| L02_C2_aws-034 | K | Coût de la campagne (chiffres rapportés) | E | Cost Explorer et get-account-plan-state (selon la source)... | `master:HANDOFF_2026-10-01.md:17-20,481-488,535,571-572,615-616,623,660,856,940,1004-100...` |
| L02_C2_aws-035 | K | Formule entière du rang d'un système de racines (Codex) | P | Codex (preuve directe) ; renvoi à Heckman, Coxeter Groups... | `master:lemma/t20_CODEX/REFEREE_TWIN_DEPENDENCIES.md:61-91` |
| L02_C2_aws-036 | K | Validité de la règle du vecteur caractéristique | P | Codex | `master:lemma/t20_CODEX/REFEREE_TWIN_DEPENDENCIES.md:167-174` |
| L02_C2_aws-037 | K | Répétitions CI et calibrations : verdicts identiques, nombres de noeuds non | E | répétitions CI (GitHub Actions) | `master:README.md:24-29` |
| L02_C2_aws-038 | K | Ce que la partie B n'établit pas (réserves écrites) | O | - | `master:lemma/PROOF_C2/B_LATTICES.md:209-217` |
| L02_C2_aws-039 | K | Réserve résiduelle de provenance : environ 780 représentants y1 sur enregistrements du PC (tier L) | E | dérivation de l'agent L02 à partir de RERUN_Y1_SUMMARY et... | `master:measures/RERUN_Y1_SUMMARY_2026-10-07.json` |
| L02_C2_aws-040 | K | 28 réseaux S sans aucun enregistrement sur une branche run/* | E | recompte de l'agent L02 (branches run/* contre B_TABLE_156) | `master:lemma/PROOF_C2/B_TABLE_156.md:24-183` |
| L02_C2_aws-041 | D | Théorème R : une involution donne un repère de 51 vecteurs dans un réseau impair unimodulaire de rang 24 | P | Codex (une passe « errors only » sur AUDIT_REDUCTION.md à... | `master:lemma/upstream/AUDIT_REDUCTION.md:39-54` |
| L02_C2_aws-042 | D | A.0 : une involution fixe exactement un sommet (preuve à la main ; = F0) | P | Codex (REFEREE_REDUCTION à 8bee8a0e2 : « No mathematical ... | `master:lemma/upstream/AUDIT_REDUCTION.md:56-88` |
| L02_C2_aws-043 | D | A.1 : l'involution retourne les sept blocs ; 49 orbites | P | Codex (section A, aucune erreur) ; LAP : « Checked: corre... | `master:lemma/upstream/AUDIT_REDUCTION.md:90-104` |
| L02_C2_aws-044 | D | A.2 : le quotient signé S (49×49), S^2 + S = 12I | P | Codex (section A, aucune erreur) | `master:lemma/upstream/AUDIT_REDUCTION.md:106-113` |
| L02_C2_aws-045 | D | A.3 : le repère serré de rang 22 et le réseau N = √7 K* | P | Codex (section A, aucune erreur) | `master:lemma/upstream/AUDIT_REDUCTION.md:115-123` |
| L02_C2_aws-046 | D | A.4 : classe de Witt de la forme discriminante de N pour tout g (formule d'oddité) | P | Codex (REFEREE_REDUCTION : « the oddity and Witt-class ca... | `master:lemma/upstream/AUDIT_REDUCTION.md:125-150` |
| L02_C2_aws-047 | D | A.5 : min N* ≥ 8/7 (pas de fonction propre −4 σ-impaire entière de norme ≤ 14) | P | Codex (section A : « the lower bound for the dual minimum... | `master:lemma/upstream/AUDIT_REDUCTION.md:152-167` |
| L02_C2_aws-048 | D | A.6 : l'enveloppe U (recollement de Nmax avec 7I2) | P | Codex (section A : « the integral unimodular gluing, prim... | `master:lemma/upstream/AUDIT_REDUCTION.md:169-182` |
| L02_C2_aws-049 | D | A.7 : classification de Borcherds (citée) : 156 classes | P | théorème publié, cité, non redémontré ; Codex a lu la cop... | `master:lemma/upstream/AUDIT_REDUCTION.md:184-188` |
| L02_C2_aws-050 | D | A.8 / Lemme 6.6 : couverture des nouvelles racines | P | Codex (section A, « the two consequences in A.8 (145-150)... | `master:lemma/upstream/AUDIT_REDUCTION.md:190-195` |
| L02_C2_aws-051 | D | A.8 / Lemme 6.7 : piège caractéristique Y ≤ 66 | P | Codex (section A ; puis REFEREE_TWIN_DEPENDENCIES §7 : « ... | `master:lemma/upstream/AUDIT_REDUCTION.md:196-197` |
| L02_C2_aws-052 | D | A.9 / Lemme 6.4 : indécomposabilité ; exclusion de 152 et 153 | P | Codex (REFEREE_REDUCTION à 8bee8a0e2 : « No mathematical ... | `master:lemma/upstream/AUDIT_REDUCTION.md:199-215` |
| L02_C2_aws-053 | D | Lemme 6.3 : les 42 uo engendrent N ; graphe des uo connexe | P | Codex (REFEREE_PAPER : « no new defect in ... the word-ge... | `master:lemma/PROOF_C2/paper/main.tex:437-453` |
| L02_C2_aws-054 | D | Lemme 6.8 (jumeaux) et construction du jumeau par R = [[2,2],[−2,2]] | P | Codex (REFEREE_PAPER : « no new defect in ... the twin le... | `master:lemma/PROOF_C2/paper/main.tex:495-506` |
| L02_C2_aws-055 | D | Théorème 7.1 (lemmes T16, T18, T20) : pas de fonction propre −4 σ-impaire entière de norme au carré 16, 18 ... | P | sessions IA seulement : T16 arbitré par Codex (pas d'erre... | `master:lemma/PROOF_C2/paper/main.tex:515-533` |
| L02_C2_aws-056 | D | Corollaire 7.2 : E(v) ≥ 11 hors du plan des normales ; témoins W8, W9, W10 | P | « These rules are complete for E <= 10 (hand remark of 07... | `master:lemma/PROOF_C2/paper/main.tex:535-550` |
| L02_C2_aws-057 | D | Corollaire 7.3 (Y1) : une racine de produit ±2 tue une normale, quelle que soit l'autre | P | « three-line proof, reread by the lab and by the laptop s... | `master:lemma/PROOF_C2/paper/main.tex:552-560` |
| L02_C2_aws-058 | D | Bornes du minimum dual : 8/7, 9/7, 11/7 | P | Codex (H5 : séparation de la dépendance T16) ; papier rel... | `master:lemma/upstream/AUDIT_REDUCTION.md:166` |
| L02_C2_aws-059 | D | Section B : chaque règle du moteur découle du Théorème R ; aucune n'utilise g | P | toutes les lignes relues par CDX (Codex) dans cette passe... | `master:lemma/upstream/AUDIT_ENGINE_RULES.md:1-14` |
| L02_C2_aws-060 | D | Règles quantitatives du moteur (points frontière, WPRUNE, Lemme Z, sommes d'étoiles, identité T, budgets) | P | Codex (OK pour chaque ligne ; budgets : « OK model, solve... | `master:lemma/upstream/AUDIT_ENGINE_RULES.md:61-63` |
| L02_C2_aws-061 | D | Filtres du producteur de paires : conséquences de R ; piège dual exact ramené aux normes 2 et 3 | P | LAB (OK-REREAD, « the statements only ») ; Codex (lignes ... | `master:lemma/upstream/AUDIT_REDUCTION.md:241-249` |
| L02_C2_aws-062 | D | Réduction de Weyl, automorphismes de diagramme et règle swap | P | Codex : « OK principle », swap « OK conditional on C's co... | `master:lemma/upstream/AUDIT_REDUCTION.md:232-236` |
| L02_C2_aws-063 | D | H1 : plafond silencieux de 1000 solutions jointes ; recensement : jamais exercé | E | Codex a inspecté le garde de l'importeur ; le recensement... | `master:lemma/upstream/AUDIT_ENGINE_RULES.md:120-147` |
| L02_C2_aws-064 | D | H2 : lemme de l'empreinte nulle (nombres de Coxeter des voisins pairs) | P | Codex a vérifié l'algèbre et le critère d'égalité ; n'a p... | `master:lemma/upstream/AUDIT_ENGINE_RULES.md:71` |
| L02_C2_aws-065 | D | H2 : couverture d'audit 25/25 ; paires exposées toutes ré-exclues | E | Codex : lecture et contrôle des rapports archivés (hachag... | `master:lemma/upstream/AUDIT_ENGINE_RULES.md:185-247` |
| L02_C2_aws-066 | D | H3 : lemme de complétude jointe des couches 2, 3, 4 | P | Codex (message 72 : « joint-count completeness lemma acce... | `master:lemma/upstream/AUDIT_ENGINE_RULES.md:286-302` |
| L02_C2_aws-067 | D | Identités thêta et ombre en rang 24 : N4 = 196560 − 24N2 − 24N3, N3 = 4096 | P | formules citées (Conway-Sloane, « A Note on Optimal Unimo... | `master:lemma/t20_CODEX/REFEREE_SHELL_COUNTS.md:14-40` |
| L02_C2_aws-068 | D | Acceptation exacte des listes de normes 2, 3, 4 pour les 156 entrées locales | C | Codex (exécution du vérificateur archivé avec borne anti-... | `master:lemma/t20_CODEX/REFEREE_SHELL_COUNTS.md:76-148` |
| L02_C2_aws-069 | D | H4 : verdicts « pair budget » fondés sur un statut de solveur ; 143 remplacé, 105 relancé | S | Codex pour 143 (« H4 is discharged for the lattice-level ... | `master:lemma/upstream/AUDIT_ENGINE_RULES.md:320-351` |
| L02_C2_aws-070 | D | H5 : la règle 9/7 exige T16 ; arbitrage T16 et revérification des 240 + 32 obstructions | C | Codex (REFEREE_T16_PROOF.md, non lu par moi) | `master:lemma/upstream/AUDIT_ENGINE_RULES.md:56` |
| L02_C2_aws-071 | D | Proposition 8.3 : le réseau 143 (a15 a8) ne contient pas de repère ; certificat 378 ≤ 336 | P | Codex (REFEREE_143_PROOF : « Accepted for the supplied la... | `master:lemma/upstream/LATTICE_143.md:1-57` |
| L02_C2_aws-072 | D | Réseau 143 : table complète des 4096 vecteurs de norme 3 par le recollement exact | C | Codex : referee_143_checks.py (arithmétique exacte SymPy,... | `master:lemma/upstream/LATTICE_143.md:29-45` |
| L02_C2_aws-073 | D | Réseau 143 : le test d'empilement ne l'exclut pas | E | non relu séparément (dans LATTICE_143.md accepté par Codex) | `master:lemma/upstream/LATTICE_143.md:97-102` |
| L02_C2_aws-074 | D | Proposition 8.1 (empilement) : (a) frappes disjointes des nouvelles racines ; (b) piège dual 8/7 | P | Codex (REFEREE_PAPER : « no new defect in ... the mathema... | `master:lemma/PROOF_C2/paper/main.tex:580-604` |
| L02_C2_aws-075 | D | Quatorze réseaux exclus par le test d'empilement (a) | E | deux programmes indépendants : C1 envelope_pack.py et Cod... | `master:lemma/t20_CODEX/INDEPENDENT_PACKING.md:1-27` |
| L02_C2_aws-076 | D | Quatre réseaux exclus par le piège dual (b) : 117, 134, 145, 146 | E | Codex (calcul exact indépendant, énumération stricte < 8/... | `master:lemma/t20_CODEX/INDEPENDENT_PACKING.md:79-123` |
| L02_C2_aws-077 | D | Bilan : 20 réseaux exclus sans énumérer de paires de normales | E | voir L02_C2_aws-052, L02_C2_aws-071, L02_C2_aws-075, L02_... | `master:lemma/PROOF_C2/paper/main.tex:679-680` |
| L02_C2_aws-078 | D | Identification exacte des 156 réseaux d'entrée (Codex) | E | programme indépendant (n'importe aucun programme d'identi... | `master:lemma/t20_CODEX/EXACT_LATTICE_IDENTITY.md:1-61` |
| L02_C2_aws-079 | D | Recalcul LAB des 156 (04/10) : erratum du réseau 150 ; contrôle de masse non fait | E | non relu ; Codex : ces scripts ne sont pas exacts (rang f... | `master:lemma/upstream/AUDIT_REDUCTION.md:282-303` |
| L02_C2_aws-080 | D | F4 : énumération indépendante des paires égale à celle du producteur sur 4 réseaux | E | fichiers de comparaison f4/<lid>_compare.json lus par LAB... | `master:lemma/PROOF_C2/paper/main.tex:704-710` |
| L02_C2_aws-081 | D | Producteur : réseaux 001/002/004/010 (repère de Golay) et réseaux à racines non génératrices | E | argument SOURCE-ONLY (LAB) ; concordance Golay selon l'en... | `master:lemma/upstream/AUDIT_REDUCTION.md:259-273` |
| L02_C2_aws-082 | D | 91 réseaux de l'énumération principale : 220 260 576 paires toutes exclues | S | recomptage LAB (stream_recount.py, STREAM_RECOUNT_2026-10... | `master:lemma/PROOF_C2/paper/main.tex:796-803` |
| L02_C2_aws-083 | D | 13 réseaux 001–003, 005–009, 011–015 : 7 699 047 paires exclues via T18/T20 avec certificats | C | vérificateurs exacts séparés (q/cert_stream.py, cert_gola... | `master:lemma/PROOF_C2/paper/main.tex:805-809` |
| L02_C2_aws-084 | D | 003 : le représentant y1 n° 181 exclu par le Corollaire Y1 | C | deux vérificateurs indépendants ; conditionnel à T18 et T20 | `master:lemma/PROOF_C2/paper/main.tex:808-809` |
| L02_C2_aws-085 | D | 000 (Leech impair) : 141 classes de paires, 86 certificats PL + 55 recherches | S | 86 certificats « verified twice per the tracker » (projet... | `master:lemma/PROOF_C2/paper/main.tex:811-813` |
| L02_C2_aws-086 | D | 004 et 010 : 416 383 et 3 962 paires exclues par (i) et (iii) | S | recomptées par LAB le 07/10 ; non reproduites | `master:lemma/PROOF_C2/paper/main.tex:812-813` |
| L02_C2_aws-087 | D | 28 réseaux par les lemmes seuls : 17 réseaux exclus sans aucune recherche | C | témoins et 4 073 certificats Y1 vérifiés par deux vérific... | `master:lemma/PROOF_C2/paper/main.tex:818-823` |
| L02_C2_aws-088 | D | Seconde exécution complète des 28 réseaux (et de 105) le 07/10 | S | contrôle d'acceptation LAB (rerun_713_check.py renforcé a... | `master:lemma/PROOF_C2/paper/main.tex:825-831` |
| L02_C2_aws-089 | D | Enregistrements de septembre à version non enregistrée : 10 802 y1 dans 55 réseaux | S | vérificateur exact des certificats Y1 ; vérificateur 713 ... | `master:lemma/PROOF_C2/paper/main.tex:921-927` |
| L02_C2_aws-090 | D | Exclusions par recherche : un seul programme, sans certificat | S | règles auditées par Codex ; exécutable non dupliqué | `master:lemma/PROOF_C2/paper/main.tex:910-933` |
| L02_C2_aws-091 | D | Règle de transfert vers un jumeau : trois formes et leurs comptes | S | Codex : l'induction (b) est valide (REFEREE_TWIN_DEPENDEN... | `master:lemma/PROOF_C2/paper/main.tex:736-753` |
| L02_C2_aws-092 | D | Résidu de transfert après Y1 : au plus 2 479 669 paires, recertification non faite | O | dimensionnement LAB ; formulation du papier reprise « aft... | `master:lemma/PROOF_C2/paper/main.tex:889-897` |
| L02_C2_aws-093 | D | Outil exact de type des jumeaux : formule de rang r = 4m/(n1+4) ; flux historiques non vérifiés | P | Codex (preuve directe de la formule de LAB) ; contrôles e... | `master:lemma/t20_CODEX/REFEREE_TWIN_DEPENDENCIES.md:61-123` |
| L02_C2_aws-094 | D | Rejeu du lot 713 : 60 308 transferts = 59 697 statut + 428 plus riches + 183 canoniques | E | Codex (réexécution) | `master:lemma/t20_CODEX/REFEREE_TWIN_DEPENDENCIES.md:149-165` |
| L02_C2_aws-095 | D | Les 1 610 témoins caractéristiques des 28 réseaux : compte rapporté, non rejoué par Codex | E | Codex (lecture des enregistrements, sans rejeu) | `master:lemma/t20_CODEX/REFEREE_TWIN_DEPENDENCIES.md:176-186` |
| L02_C2_aws-096 | D | Théorème 6.2 (B) : aucun des 156 réseaux ne contient de repère | S | sessions IA seulement (voir L02_C2_aws-097) ; parties : 2... | `master:lemma/PROOF_C2/paper/main.tex:426-433` |
| L02_C2_aws-097 | D | Théorème 1.1 : un srg(99,14,1,2) n'a pas d'automorphisme d'ordre 2 | S | sessions IA seulement : passe Codex « errors only » sur c... | `master:lemma/PROOF_C2/paper/main.tex:63-77` |
| L02_C2_aws-098 | D | Corollaire 1.2 / Théorème d'asymétrie (note asymmetric.tex), conditionnel à (A)–(E) | P | Codex : « The assembly argument in asymmetric.tex at 62b5... | `master:lemma/PROOF_C2/paper/asymmetric.tex:33-55` |
| L02_C2_aws-099 | D | Ingrédient (A) : Makhnev-Minakova 2004, \|G\| divise 2·3^3·7·11 | P | publié ; Codex a lu l'original russe (Theorem 1 et Coroll... | `master:lemma/PROOF_C2/paper/asymmetric.tex:60-61` |
| L02_C2_aws-100 | D | Ingrédient (C) : pas d'automorphisme d'ordre 3 (manuscrit D3, formalisé en Lean 4) | P | formalisation Lean selon le dépôt conway99-c3-experimenta... | `master:lemma/PROOF_C2/paper/asymmetric.tex:67-71` |
| L02_C2_aws-101 | D | Behbahani-Lam 2011 (et thèse 2009) : seuls 2 et 3 peuvent diviser \|G\| ; ordres 7 et 11 exclus par ordinateur | E | publié ; ni l'article BL ni la thèse n'ont été ouverts (P... | `master:lemma/PROOF_C2/paper/main.tex:94-96` |
| L02_C2_aws-102 | D | Ingrédient (D) sans ordinateur : pas d'automorphisme d'ordre 7 (manuscrit D7, Lean 4) | P | formalisation Lean selon le dépôt conway-C7 (lu, non reco... | `master:lemma/PROOF_C2/paper/asymmetric.tex:72-75` |
| L02_C2_aws-103 | D | Cesarz-Woldar 2025 et Crnković-Maksimović 2020 (cités) | P | CW25 publié, lu directement (pp. 379-380 et liste de réfé... | `master:lemma/PROOF_C2/paper/main.tex:96-98` |
| L02_C2_aws-104 | D | Ce qui reste de \|G\| selon les sources : {1,2,3} (publié), {1,2,11} (sans ordinateur), {1} (tout) | P | assemblage relu par Codex (conditionnel aux ingrédients) | `master:lemma/PROOF_C2/paper/asymmetric.tex:97-109` |
| L02_C2_aws-105 | D | MODEL.md : modèle exact (S, L_N, T4, EX) et lien avec C2 | O | T4 : « independently hand-reviewed according to the suppl... | `master:lemma/upstream/MODEL.md:15-25` |
| L02_C2_aws-106 | D | Squelette de preuve du 01/10 : 93 exclus, 62 ouverts, 1 partiel (remplacé) | X | les quatre items de la Partie I étaient « source only, no... | `master:lemma/upstream/PROOF_SKELETON_C2.md:1-19` |
| L02_C2_aws-107 | D | Méthodes d'exclusion niveau réseau antérieures, remplacées | X | LAB (section E, 07/10) : « Lattices resting on one method... | `master:lemma/upstream/AUDIT_REDUCTION.md:305-331` |
| L02_C2_aws-108 | D | Formalisation : rien n'est formalisé pour C2 ; cibles et architecture proposées | O | note de faisabilité de Codex (pas une formalisation) | `master:lemma/t20_CODEX/LEAN_FEASIBILITY.md:1-101` |
| L02_C2_aws-109 | D | Corrections de l'arbitre au texte gelé c1bcba6bb du papier | R | Codex (passe « errors only ») ; corrections reportées dan... | `master:lemma/t20_CODEX/REFEREE_PAPER_c1bcba6bb.md:18-118` |
| L02_C2_aws-110 | D | Obligations de présentation et de bibliographie restantes (revue éditoriale de Codex) | O | Codex (revue éditoriale, pas une certification mathématique) | `master:lemma/t20_CODEX/EDITORIAL_REVIEW_PAPER.md:37-63` |
| L02_C2_aws-111 | D | Environnement et coût de calcul de l'énumération principale | E | non relu | `master:lemma/PROOF_C2/paper/main.tex:941-949` |
| L02_C2_aws-112 | B | T16 : pas de fonction propre (-4) entière sigma-impaire de norme carrée 16 (min L* >= 9/7) | P | LAB 04/10 (cube et partie structurelle de Wagner rederivé... | `master:lemma/T16_PROOF.md:1-58` |
| L02_C2_aws-113 | B | T16, étape 1 : au cas d'égalité 8/7 les coefficients valent 0, +1 ou -1 (huit +1, huit -1) | P | LAB 04/10 (rederivé) ; LAP 07/10 ; pont F4 (LAP 07/10) ; ... | `master:lemma/t16/dossier_2026-10-04/LEMME_EGALITE_8_SUR_7_C2.txt:60-78` |
| L02_C2_aws-114 | B | T16, étapes 2-3 : nombre k de h actifs dans {0,2}, et k = 2 impossible | P | LAB 04/10 (rederivé à la main) ; Codex 07/10 (« no error ... | `master:lemma/t16/dossier_2026-10-04/LEMME_EGALITE_8_SUR_7_C2.txt:4-29` |
| L02_C2_aws-115 | B | Inégalité D >= 0 : le côté positif du support est indépendant (m = 8) | P | LAB 04/10 ; Codex 07/10 ; pont F6 (LAP) | `master:lemma/t16/dossier_2026-10-04/LEMME_EGALITE_8_SUR_7_C2.txt:98-118` |
| L02_C2_aws-116 | B | Classification : le complément de B est le cube ou le graphe de Wagner | P | LAB 04/10 (« §8 only uses the no triangle part ... This i... | `master:lemma/t16/dossier_2026-10-04/C2_PROLONGEMENT_SUPPORT16_PREUVE_CUBE.txt:206-222` |
| L02_C2_aws-117 | B | Comptes globaux autour d'un support de taille 16 | P | LAB 04/10 (rederivé) ; Codex 07/10 ; pont (LAP) | `master:lemma/t16/dossier_2026-10-04/C2_PROLONGEMENT_SUPPORT16_PREUVE_CUBE.txt:42-77` |
| L02_C2_aws-118 | B | Support 16 : le complément du cube est impossible (au moins 10, au plus 8) | P | LAB 04/10 (« Verdict: correct. No gap was found ») ; Code... | `master:lemma/t16/dossier_2026-10-04/C2_PROLONGEMENT_SUPPORT16_PREUVE_CUBE.txt:4-17` |
| L02_C2_aws-119 | B | Support 16 : t = 1 et exactement deux profils A et B | P | LAB 04/10 (§7 rederivé) ; Codex 07/10 (« the two global W... | `master:lemma/t16/dossier_2026-10-04/C2_PROLONGEMENT_SUPPORT16_PREUVE_CUBE.txt:146-196` |
| L02_C2_aws-120 | B | Support 16 : le complément de Wagner est impossible (classification finie exacte) | C | LAB 04/10 (réductions structurelles relues ; énumérateurs... | `master:lemma/t16/dossier_2026-10-04/C2_WAGNER_BORNE_9_SUR_7.txt:109-352` |
| L02_C2_aws-121 | B | Défaut du vérificateur reçu du dossier T16 (check_B) | R | Codex (auteur du constat, 07/10) | `master:lemma/t20_CODEX/REFEREE_T16_PROOF.md:14-31` |
| L02_C2_aws-122 | B | Critère de paire Y = 13 (règle W8, filtre moteur FD_MIN97) | P | LAB 04/10 (réduction rederivée) ; pont F1-F7 (LAP 07/10) ... | `master:lemma/t16/dossier_2026-10-04/C2_WAGNER_BORNE_9_SUR_7.txt:382-400` |
| L02_C2_aws-123 | B | Témoins Y = 13 sur les 400 paires historiques du réseau 011 | C | LAB 04/10 ; LAP (pont, 07/10) ; arbitre du pont (ref_engi... | `master:lemma/t16/dossier_2026-10-04/C2_WAGNER_BORNE_9_SUR_7.txt:402-424` |
| L02_C2_aws-124 | B | Mesure du critère Y = 13 sur des échantillons de paires cherchées (min97_probe) | E | non relu | `master:lemma/t16/lab_check/VERIF_CUBE_OBSTRUCTION_2026-10-04.md:56-98` |
| L02_C2_aws-125 | B | Ancien critère de rang pour les témoins Y = 13 (avant la fermeture de Wagner) | X | non relu | `master:lemma/t16/dossier_2026-10-04/LEMME_EGALITE_8_SUR_7_C2.txt:172-227` |
| L02_C2_aws-126 | B | Route « témoin » de la note 54 : coupes k = 1, 2, 3 ouvertes | O | LAB 04/10 (portée) | `master:lemma/t16/dossier_2026-10-04/C2_WAGNER_BORNE_9_SUR_7.txt:53-55` |
| L02_C2_aws-127 | B | T18 : pas de fonction propre (-4) entière sigma-impaire de norme carrée 18 | P | arbitre 1 (agent t18_REFEREE, sur les rapports de travail... | `master:lemma/T18_PROOF.md:114-134` |
| L02_C2_aws-128 | B | T18, Proposition 3.1 : valeurs entières -> 0, +1, -1 avec neuf +1 | P | preuve de l'arbitre 1 (étape absente des rapports de trav... | `master:lemma/T18_PROOF.md:195-232` |
| L02_C2_aws-129 | B | T18, réductions sur le support : k = 0, e = 0, S+ indépendant, S hors de N[p] | P | arbitre 1 (A1-A4 CORRECT ; A3 : cas C et deux justificati... | `master:lemma/T18_PROOF.md:235-419` |
| L02_C2_aws-130 | B | Identités de comptage et loi de parité pour une taille de support m quelconque | P | arbitre 1 (CORRECT) ; arbitre 2 | `master:LEMMA_TARGET_2026-10-06.md:104-112` |
| L02_C2_aws-131 | B | Calcul 4.10 : trois graphes d'orbites possibles B0 = K3 x K3, B1, B2 = C9(1,2) | E | quatre programmes : enum_S.py, verify_S.py (qui importe l... | `master:lemma/T18_PROOF.md:421-497` |
| L02_C2_aws-132 | B | T18, Théorème 5.3 (N3) : aucun sommet extérieur n'a 3 voisins dans S+ | P | session principale LAP (ligne à ligne) ; agent B1 (round ... | `master:lemma/t18/N3_REPORT.md:1-38` |
| L02_C2_aws-133 | B | T18, Lemme 5.4 : identités sur X_0, X_1, X_2 et t <= 9 | P | arbitre 1 (A8 CORRECT) ; arbitre 2 (864 - 2t, 576 - 2t, 3... | `master:lemma/T18_PROOF.md:552-603` |
| L02_C2_aws-134 | B | T18 : trois profils en p, h_0 <= 1, profil (4,1,2) impossible | P | arbitre 1 (CORRECT ; trou : A9 citait le fait calculé A6,... | `master:lemma/T18_PROOF.md:605-651` |
| L02_C2_aws-135 | B | Les deux matrices semi-définies positives et le budget de voisins communs | P | arbitre 1 (CORRECT) ; arbitre 2 (correct) | `master:lemma/T18_PROOF.md:653-700` |
| L02_C2_aws-136 | B | Borne de rang : parties impaire et paire de 63 E_{-4} de rang <= 22 | P | agent t18_STRUCT (auteur) ; rederivée par l'agent B1 (A19... | `master:lemma/T18_PROOF.md:786-837` |
| L02_C2_aws-137 | B | STRUCT P1, P3, P4, P5 : vecteurs propres entiers, rang-nullité, t pair, t != 8 | P | arbitre 1 (P1-P5 CORRECT ; non nécessaires) | `master:lemma/t18_STRUCT/REPORT.md:15-32` |
| L02_C2_aws-138 | B | STRUCT P6, P7, P8 (sans preuve écrite) | H | non vérifié (arbitre 1 : « NOT VERIFIED (unused) », pas d... | `master:lemma/t18_STRUCT/REPORT.md:89-98` |
| L02_C2_aws-139 | B | T18, Lemme 7.1 : X_2 en bijection avec les 18 paires déficitaires, appariement tau | P | arbitre 1 ; arbitre 2 (correct) | `master:lemma/T18_PROOF.md:843-913` |
| L02_C2_aws-140 | B | Calcul 7.3 (étape 1) : rectangles et appariements admissibles | E | quatre programmes concordants (r2_stage1.py ; r3_verify.p... | `master:lemma/T18_PROOF.md:916-941` |
| L02_C2_aws-141 | B | Profil (3,3,1) impossible pour B0, B1, B2 (Calcul 7.6, Proposition 7.7) | E | I1 (lemma/t18) et I2 (t18_VERIF331, écrit depuis la descr... | `master:lemma/T18_PROOF.md:1096-1183` |
| L02_C2_aws-142 | B | Les deux matrices sont nécessaires : avec M1 seule, 10 configurations de B1 survivent sur 51 sommets | E | I2 (VERIF331) et REF1 ; REF2 (p331_m1.py) : mêmes comptes | `master:lemma/T18_PROOF.md:1185-1204` |
| L02_C2_aws-143 | B | Énoncé réfuté : « the violated matrix is 9(3I-A)+J » | R | réfuté par t18_VERIF331 et par l'arbitre 1 (remarque 3) ;... | `master:lemma/t18/T18_REPORT.md:220` |
| L02_C2_aws-144 | B | T18 n'utilise pas T16 (H16) : le fichier types.json ne filtre rien | E | arbitre 2 (recount.py ; recherche dans les sources des se... | `master:lemma/T18_PROOF.md:1737-1758` |
| L02_C2_aws-145 | B | Profil (2,5,0), étape B (Calcul 8.4) : triples (tau,F,H) sur 37 sommets | E | ENUM (r3_p250.py) et VERIF (r3_verify.py, sans code parta... | `master:lemma/T18_PROOF.md:1362-1421` |
| L02_C2_aws-146 | B | Profil (2,5,0), étape C (Calcul 8.5) : 0 survivant pour B0 et B2, exactement 4 pour B1 | E | B1 et B2 : ENUM et CMINE complets sans code partagé (et V... | `master:lemma/T18_PROOF.md:1423-1515` |
| L02_C2_aws-147 | B | Les quatre survivants de B1 sont exactement PSD sur 47 sommets | E | r3_survivors.py (élimination rationnelle, deux matrices) ... | `master:lemma/T18_PROOF.md:1516-1536` |
| L02_C2_aws-148 | B | Calcul 8.6 : la borne de rang exclut les quatre survivants de B1 | E | cinq codes exacts écrits séparément (r4_rank.py ; rank_su... | `master:lemma/T18_PROOF.md:1538-1563` |
| L02_C2_aws-149 | B | Calcul 8.8 (étape D) : aucun sommet de X_0 privé de p ne s'ajoute aux quatre survivants | C | r4_stageD.py (3 048 certificats revérifiés par r3_verify.... | `master:lemma/T18_PROOF.md:1565-1622` |
| L02_C2_aws-150 | B | Remarque de l'arbitre 2 : rang M1[Y47] = 46 > 44 suffit à exclure les quatre survivants | P | non relu (« not used; unrefereed ») | `master:lemma/T18_PROOF.md:1934-1941` |
| L02_C2_aws-151 | B | Niveau 1 cohérent : l'obstruction de T18 n'est pas visible dans les voisinages dans S | E | non relu | `master:lemma/t18/T18_REPORT.md:105-131` |
| L02_C2_aws-152 | B | Route « X_0 d'abord » pour B0 : 8 tables survivent sans W, PSD et compatibles avec la borne de rang | E | b0_x0_check.py (force brute indépendante, décisions PSD e... | `master:lemma/t18_B0/REPORT.md:75-93` |
| L02_C2_aws-153 | B | Bogue de b0_x0.py (diagonales des matrices), sorties écartées | X | agent t18_B0 (auto-relecture) | `master:lemma/t18_B0/REPORT.md:81-83` |
| L02_C2_aws-154 | B | Certificat local autour d'une racine d'énergie 9 : ne décide pas, plus lent que la recherche de cadre | E | non relu | `master:LEMMA_TARGET_2026-10-06.md:82-97` |
| L02_C2_aws-155 | B | Où va le temps de recherche v10 : énergie minimale des paires cherchées | E | non relu | `master:LEMMA_TARGET_2026-10-06.md:7-34` |
| L02_C2_aws-156 | B | Dictionnaire : minimum du dual du réseau du cadre <=> norme des fonctions propres sigma-impaires | P | d'abord une reconstruction marquée « check it against the... | `master:LEMMA_TARGET_2026-10-06.md:36-61` |
| L02_C2_aws-157 | B | Théorème du pont : vecteur de l'enveloppe -> fonction propre (-4) entière sigma-impaire | P | agent bridge_REFEREE (07/10, nuit) : « No error that brea... | `master:lemma/BRIDGE.md:184-201` |
| L02_C2_aws-158 | B | Corollaires du pont : énergies 8, 9, 10 interdites par T16, T18, T20 | P | bridge_REFEREE (Corollaire T18 « Correct given T18 » ; T2... | `master:lemma/BRIDGE.md:203-209` |
| L02_C2_aws-159 | B | Réduction par classes : quels vecteurs ont une énergie donnée | P | arbitre du pont : ref_arith.py (force brute sur (N, a, b)... | `master:lemma/BRIDGE.md:280-296` |
| L02_C2_aws-160 | B | Corollaire Y1 : une racine de produit +-2 avec y1 tue ce y1 pour tout y2 | P | non arbitré par bridge_REFEREE (ajouté après son passage,... | `master:lemma/BRIDGE.md:211-222` |
| L02_C2_aws-161 | B | Hypothèse H4 non vérifiée sur la voie de report rapide ; certificat exigé par paire | E | arbitre du pont (démontré par exécution) | `master:lemma/BRIDGE.md:319` |
| L02_C2_aws-162 | B | Phrase retirée du pont : « the engine would answer INVALID for such a pair » | X | agent bridge_REFEREE (item 2 : « ERROR in the description... | `origin/defer-n4:lemma/BRIDGE.md:367` |
| L02_C2_aws-163 | B | « The converse is false in general » remplacé par « not available » | X | agent bridge_REFEREE (item 7 : « UNVERIFIED ... Harmless ») | `origin/defer-n4:lemma/BRIDGE.md:342` |
| L02_C2_aws-164 | B | Validation du dictionnaire sur Paley(9) et srg(243,22,1,2) avec x -> -x | E | deux implémentations : graph_check.py (LAP) et ref_graphs... | `master:lemma/BRIDGE.md:325-334` |
| L02_C2_aws-165 | B | Contrôle du moteur sur le réseau 011 et ses 400 paires | E | deux implémentations (engine_check.py, LAP ; ref_engine.p... | `master:lemma/BRIDGE.md:404-427` |
| L02_C2_aws-166 | B | Usage de T18 comme exclusion : report des paires, certificats par paire, conversion | C | selon A2_BRIDGE.md ; certificats non relus ici | `master:LEMMA_TARGET_2026-10-06.md:190-196` |
| L02_C2_aws-167 | B | Limite des lemmes T16-T20 : paires d'énergie minimale >= 11, T22 non revendiqué | E | non relu (fait cité par A3) | `master:lemma/PROOF_C2/A3_LEMMAS.md:70-78` |
| L02_C2_aws-168 | B | Hypothèse amont du pont (H5) : tout 99-graphe donne une des 156 enveloppes et une paire énumérée | P | Codex selon HANDOFF:984 (« Theorem R proved by hand (A.0 ... | `master:lemma/BRIDGE.md:117-120` |
| L02_C2_aws-169 | B | A7 : conséquences de H16 pour T18 (conditionnel, inutilisé) | P | non vérifié (arbitre 1 : « NOT VERIFIED (conditional, unu... | `master:lemma/t18/T18_REPORT.md:94-103` |
| L02_C2_aws-170 | B | Faits généraux de T18 testés sur Paley(9) et srg(243,22,1,2) | E | arbitre 1 (ref3_bvls.out, non lu ici) | `master:lemma/t18_REFEREE/REPORT.md:113-114` |
| L02_C2_aws-171 | B | Le double comptage du cube (T16) ne se transfère pas à T18 | E | non relu | `master:lemma/t18/T18_REPORT.md:282-283` |
| L02_C2_aws-172 | B | Condition de noyau à l'étape D : vacuité | E | r4_verifyD.py (exact) ; arbitre 2 (remarque vérifiée exac... | `master:lemma/t18/T18_REPORT.md:531-537` |
| L02_C2_aws-173 | B | Profil (3,3,1), ligne 1 : ce que comptent 3 510 / 7 224 / 2 406 | E | arbitre 2 (recount.py, recount2.py) | `master:lemma/T18_PROOF.md:1204-1230` |
| L02_C2_aws-174 | B | « Type solutions » de B2 comptées sans la condition (C6) | E | arbitre 1 (ref5b_types_variants_B2.out, non lu ici) | `master:lemma/T18_PROOF.md:1510-1514` |
| L02_C2_aws-175 | B | Revendication retirée : « deux implémentations exactes complètes » de l'étape C pour B0 | X | arbitre 2 (remarque 6) ; recomptage de la réduction (ferm... | `master:lemma/t18_PROOF/T18_PROOF_v2_changes.txt:136-144` |
| L02_C2_aws-176 | C | T20 (Théorème 10.2) : énoncé et statut global | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:1-27` |
| L02_C2_aws-177 | C | Valeurs entières réduites à 0, +1, -1 ; \|S+\| = 10 (Lemmes 3.1, 3.2, Prop. 3.3) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:268-327` |
| L02_C2_aws-178 | C | k (orbites actives internes) vaut 0, 2 ou 4 (Lemme 4.1) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:376-400` |
| L02_C2_aws-179 | C | Identités de comptage (I1)-(I3) et e <= 1 (Lemmes 4.2, 4.3) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:402-434` |
| L02_C2_aws-180 | C | Loi de parité et trois cas (Lemme 4.4, Cor. 4.5) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:436-449` |
| L02_C2_aws-181 | C | Cas II : l'arête plus joint deux mots, dans un 4-cycle (Lemmes 4.6, 4.7, 4.8) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:451-505` |
| L02_C2_aws-182 | C | Cas III : mots du support = arêtes de K4 ; cas I : graphe d'orbites B (Lemmes 4.9, 4.10) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:507-550` |
| L02_C2_aws-183 | C | Calcul 4.12 : structures de support (27720 / 2880 / 0 / 10080 étiquetées ; 6 + 1 + 2 classes) | E | deux programmes pour les totaux (t20_enum.py, t20_verify.... | `master:lemma/T20_PROOF.md:587-639` |
| L02_C2_aws-184 | C | Corollaire 4.13 : neuf configurations I.0-I.5, IIa.0, III.0, III.1 et leurs unités | E | Hand + Calcul 4.12 ; tables recalculées par _check_text_d... | `master:lemma/T20_PROOF.md:641-712` |
| L02_C2_aws-185 | C | PSD exact sur S u {p} et sur S u N[p] (cas III) : rien n'est exclu à ce niveau | E | un programme (t20_common.psd_exact, élimination rationnel... | `master:lemma/T20_PROOF.md:714-716` |
| L02_C2_aws-186 | C | Identité des chemins G0 et d <= 4 (Lemme 5.1, Cor. 5.2) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:740-765` |
| L02_C2_aws-187 | C | Tailles des classes X_d (Lemme 5.3) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:767-798` |
| L02_C2_aws-188 | C | Borne G1 sur les voisins dans X_0 (Lemme 5.4) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:800-813` |
| L02_C2_aws-189 | C | Types et unités (Lemme 5.5) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:815-843` |
| L02_C2_aws-190 | C | Deux matrices PSD M1 = 63 E_{-4}, M2 = 77 E_3 et témoins entiers (Lemme 6.1) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:852-871` |
| L02_C2_aws-191 | C | Budget des voisins communs sur graphes partiels (Lemme 6.2) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:873-887` |
| L02_C2_aws-192 | C | Borne de rang sigma (Lemme 6.3, Prop. 6.4) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:953-1002` |
| L02_C2_aws-193 | C | Exhaustivité de la recherche par unités (Lemme 6.5 ; (6.1), (6.2)) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:889-951` |
| L02_C2_aws-194 | C | Contrat du vérificateur qui suit un plan (réserve G2) et contrôles négatifs | P | Codex : contrat demandé (G2, REFEREE_T20_PROOF l.85-129) ... | `master:lemma/T20_PROOF.md:1061-1107` |
| L02_C2_aws-195 | C | Modèle du cas III, ensembles déterminés et règle de symétrie (Lemmes 7.1, 7.2, 7.3) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:1116-1200` |
| L02_C2_aws-196 | C | Calcul 7.4 (III.0) : aucun nœud de niveau 10 sur 12 | E | deux implémentations (eng3/eng4 ; vérificateur engv.py qu... | `master:lemma/T20_PROOF.md:1204-1214` |
| L02_C2_aws-197 | C | Calcul 7.5 (III.1), premier programme : aucun nœud de niveau 10 | E | un programme au moment de l'écriture ; seconde vérificati... | `master:lemma/T20_PROOF.md:1216-1229` |
| L02_C2_aws-198 | C | Seconde vérification de III.1 (engv2.py) et nœud de rang mort sans la borne de rang | E | vérificateur engv2.py (validé sur III.0 contre engv.py) ;... | `master:lemma/t20_III1/VERIF.md:1-31` |
| L02_C2_aws-199 | C | Proposition 7.6 : pas de configuration en cas III (k = 4) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:1235-1242` |
| L02_C2_aws-200 | C | Lemmes de main du cas II (Lemmes 8.1-8.6) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:1307-1392` |
| L02_C2_aws-201 | C | Calcul 8.8 (IIa.0, étape 1) : 180 -> 87 bases | E | deux programmes, listes identiques (iia_w.py ; iian_verif... | `master:lemma/T20_PROOF.md:1434-1435` |
| L02_C2_aws-202 | C | Calcul 8.9 et Prop. 8.10 (IIa.0, étape 2) : aucune configuration en cas II | E | deux programmes sans code commun (eng5.py modèle cases.Ca... | `master:lemma/T20_PROOF.md:1437-1455` |
| L02_C2_aws-203 | C | Cas I : pas de d = 3 dans N(p), n_3 dans {0, 2} (Lemmes 9.1, 9.2) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:1521-1558` |
| L02_C2_aws-204 | C | Profils (3,4,0), (4,2,1), (5,0,2) ; (5,0,2) impossible (Lemme 9.3, Prop. 9.4) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:1560-1597` |
| L02_C2_aws-205 | C | Types des paires de N(p), cases-slots, bornes rho (Lemmes 9.5-9.10) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:1599-1721` |
| L02_C2_aws-206 | C | Cellules des profils (4,2,1) et (3,4,0), n_3 = 0 (Lemmes 9.11, 9.12) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:1723-1775` |
| L02_C2_aws-207 | C | Identités d'arêtes n_3 = 0 et identité quadratique (Q0) (Lemme 9.13) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:1777-1811` |
| L02_C2_aws-208 | C | Isolation de la paire interne de X_0 en profil (4,2,1) (Théorème 9.14, Cor. 9.15) | P | LAB (messages du pont 24 pour n3=0 et 26 pour n3=2, 'chec... | `master:lemma/T20_PROOF.md:1813-1879` |
| L02_C2_aws-209 | C | Bornes e(X_0) <= 8, e(X_2) <= 35 pour n_3 = 0 (Théorème 9.16, Cor. 9.17) | P | LAB (message du pont 29, vérifié pas à pas) ; Codex auteur | `master:lemma/T20_PROOF.md:1881-1962` |
| L02_C2_aws-210 | C | Calcul 9.19 (stade 1, n_3 = 0) : N-configurations et bases | E | deux programmes sur les douze cas depuis le 07/10 14:33 U... | `master:lemma/T20_PROOF.md:2036-2061` |
| L02_C2_aws-211 | C | Calcul 9.20 (stade 2, n_3 = 0) et Prop. 9.21 : aucune configuration en cas I avec n_3 = 0 | E | deux programmes sur les douze cas (eng6.py/run_stage2.py ... | `master:lemma/T20_PROOF.md:2063-2104` |
| L02_C2_aws-212 | C | Branche lemma-run/t20_I_rest : neuf cas, premier programme seul (v1) | E | un programme (T20_SKIP_VERIFY=1) ; recompté sur le portab... | `origin/lemma-run/t20_I_rest-i-02f356c70da99d700:ALL.txt:1-153` |
| L02_C2_aws-213 | C | Branche lemma-run/t20_I1_340 : I.1 (3,4,0), deux programmes (v2) | E | deux programmes sans code commun ; résumé lu, pas de nouv... | `origin/lemma-run/t20_I1_340-i-019e86d399c17954f:I1_340/verify_I1_340.out:1-9` |
| L02_C2_aws-214 | C | Branches lemma-run/t20_Iv_B, t20_Iv_C, t20_Iv_D : six cas, deux programmes (v1) | E | deux programmes (le premier relancé, le second in_verify.... | `origin/lemma-run/t20_Iv_B-i-0a03ce79bff09fa5d:ALL.txt:1-50` |
| L02_C2_aws-215 | C | Branche lemma-run/t20_Iv_E : I.5 (3,4,0) complet ; I.1 (4,2,1) avorté | E | pour I.5 (3,4,0) : deux programmes ; pour I.1 (4,2,1) : r... | `origin/lemma-run/t20_Iv_E-i-0cd9427b48ee5704e:ALL.txt:1-26` |
| L02_C2_aws-216 | C | Branches lemma-run/t20_Iv_A et t20_Iv_F : sans résultat utilisé | X | - | `origin/lemma-run/t20_Iv_A-i-0390fd53333c148ad:STATUS.txt:1` |
| L02_C2_aws-217 | C | Branches lemma-run/t20_Iv_G et t20_Iv_H : I.1 (4,2,1) et I.2 (4,2,1), deux programmes (v2) | E | deux programmes (in_verify.py v2) | `origin/lemma-run/t20_Iv_G-i-05703a74fbb027423:ALL.txt:1-26` |
| L02_C2_aws-218 | C | Branches lemma-run/t20_Iv_I et t20_Iv_J : I.0 (4,2,1) et I.5 (4,2,1), deux programmes (v2), comptes de nœud... | E | deux programmes sur chaque run ; l'écart entre runs n'est... | `origin/lemma-run/t20_Iv_I-i-032b7d25d335204f8:ALL.txt:1-25` |
| L02_C2_aws-219 | C | Les 16 nœuds rejetés par la borne de rang sont fermés sans elle | E | seconds programmes ; Codex a vérifié les enregistrements ... | `master:lemma/T20_PROOF.md:2641-2645` |
| L02_C2_aws-220 | C | Orbite X_3 pour n_3 = 2 (Lemme 9.22) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:2204-2258` |
| L02_C2_aws-221 | C | Unités need_z et nombres exacts pour X_2, n_3 = 2 (Lemme 9.23) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:2260-2313` |
| L02_C2_aws-222 | C | beta = 1 en profil (4,2,1), n_3 = 2 (Lemme 9.24, TRIANGLE_REDUCTION) | P | LAB (message du pont 34) ; Codex auteur | `master:lemma/T20_PROOF.md:2315-2339` |
| L02_C2_aws-223 | C | Partition autour d'un triangle dans srg(99,14,1,2) (TRIANGLE_REDUCTION) | P | LAB (message du pont 34) | `master:lemma/t20_CODEX/TRIANGLE_REDUCTION.md:12-37` |
| L02_C2_aws-224 | C | Couplage parfait dans N(z) (Lemme 9.25, H3) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:2341-2355` |
| L02_C2_aws-225 | C | Identités d'arêtes n_3 = 2 et (Q2) = 55 - 16 eps (Lemme 9.26, H4) | P | Codex (REFEREE_T20_PROOF, premier passage sur 8510844a4 :... | `master:lemma/T20_PROOF.md:2357-2393` |
| L02_C2_aws-226 | C | Modèle de la route B : base Y_z à 37 sommets (Lemmes 9.27, 9.28) | P | Codex, addendum route B : 'No blocking error found in the... | `master:lemma/T20_PROOF.md:2395-2484` |
| L02_C2_aws-227 | C | Calcul 9.29 (a) : 25 classes de types de z | E | trois calculs indépendants : ztypes.py (LAP), x3_types.py... | `master:lemma/T20_PROOF.md:2486-2491` |
| L02_C2_aws-228 | C | Calcul 9.29 (b) : stade 1 de la route B, 64,528 bases | E | deux programmes sans code commun (stage1c.py z= ; in_veri... | `master:lemma/T20_PROOF.md:2493-2513` |
| L02_C2_aws-229 | C | Calcul 9.29 (c) et Prop. 9.30 : aucune configuration en cas I avec n_3 = 2 | E | deux programmes sans code commun, même modèle (eng6.py/ru... | `master:lemma/T20_PROOF.md:2515-2549` |
| L02_C2_aws-230 | C | Branche d'archive lemma-archive/t20_n3_routeB | E | - | `origin/lemma-archive/t20_n3_routeB:README.md:1-10` |
| L02_C2_aws-231 | C | Route A : bases S u {p} u X_3 u X_0' (29 sommets), 700 classes | E | LAB (n3_cases.py) ; comptes reproduits indépendamment par... | `master:lemma/t20_HAND/NOTES.md:222-253` |
| L02_C2_aws-232 | C | Route A : runs t20_n3 (168 puis 183 bases fermées, 421 ouvertes), arrêtée | E | un programme (eng5z.py) ; non utilisé | `origin/lemma-run/t20_n3-i-0b8ae938c1fc89c62:STATUS.txt:1` |
| L02_C2_aws-233 | C | Route A : mesure de coût (t20_n3_sample) | H | - | `master:lemma/T20_BOARD.md:13` |
| L02_C2_aws-234 | C | Second programme Codex pour la route A (n3_second) | E | - | `master:lemma/t20_CODEX/n3_second/README.md:1-102` |
| L02_C2_aws-235 | C | Moyenne de 3,7 minutes par base (premier programme, route A) retirée | X | - | `master:lemma/t20_CODEX/n3_second/MEASUREMENTS.md:45-51` |
| L02_C2_aws-236 | C | Règle de norme duale (Lemme 10.2, NOTES H6) : conditionnelle à (E14) | P | Codex (REFEREE l.192-195 : résidus {0,3,5,6} vérifiés ; r... | `master:lemma/T20_PROOF.md:2652-2690` |
| L02_C2_aws-237 | C | Obstructions de norme duale (Codex HAND.md, Prop. 1, 2, Cor. 3) : conditionnelles | P | aucune relecture indépendante mentionnée dans les notes l... | `master:lemma/t20_CODEX/HAND.md:1-86` |
| L02_C2_aws-238 | C | Calculs locaux de Codex (dual_local, dual_pairs, dual_n3, double_defect) | C | une implémentation (dit par la source : 'computed claims ... | `master:lemma/t20_CODEX/HAND.md:88-120` |
| L02_C2_aws-239 | C | Types de z (H2) et preuve à la main de e(U) >= 1 si U n V vide | P | aucune relecture mentionnée dans les notes lues | `master:lemma/t20_HAND/NOTES.md:79-110` |
| L02_C2_aws-240 | C | N(p) comme dix racines de D7 (H5) | P | aucune relecture mentionnée ; T20_PROOF : reformulation d... | `master:lemma/t20_HAND/NOTES.md:160-181` |
| L02_C2_aws-241 | C | Cas I, n_3 = 2 : l'ensemble S u X_3 u X_0 (29 sommets) n'est pas contradictoire (H7) | E | un programme (n3_base.py) ; comptes étiquetés et budget/d... | `master:lemma/t20_HAND/NOTES.md:222-253` |
| L02_C2_aws-242 | C | Lemmes de Codex appliqués aux bases de la route A (H10) | E | deux programmes (LAB n3_cases.py ; Codex rigidity_n3.py, ... | `master:lemma/t20_HAND/NOTES.md:315-349` |
| L02_C2_aws-243 | C | Indépendance de T20 vis-à-vis de T18 et des petites normes | E | vérification par recherche textuelle de l'auteur du texte | `master:lemma/T20_PROOF.md:2620-2633` |
| L02_C2_aws-244 | C | Premier passage d'arbitrage de Codex sur T20_PROOF (D3) | P | Codex lui-même (arbitre IA) ; pas d'arbitre humain | `master:lemma/t20_CODEX/REFEREE_T20_PROOF.md:1-165` |
| L02_C2_aws-245 | C | E1 : erreur de signe dans la preuve du Corollaire 5.2 (corrigée) | X | Codex | `master:lemma/t20_CODEX/REFEREE_T20_PROOF.md:34-60` |
| L02_C2_aws-246 | C | Contrôle indépendant des données imprimées (referee_text_checks.py) | E | Codex (programme indépendant, sortie referee_text_checks.... | `master:lemma/t20_CODEX/REFEREE_T20_PROOF.md:197-214` |
| L02_C2_aws-247 | C | Addendum d'arbitrage : route B, section 9.B.6 et Théorème 10.2 | P | Codex (arbitre IA) | `master:lemma/t20_CODEX/REFEREE_T20_PROOF.md:224-331` |
| L02_C2_aws-248 | C | Bloc de référence I.0 (4,2,1) de SPEC_ROUTE_B : convention 'raw Z' (étiqueté après revue) | X | Codex (addendum, correction 1) | `master:lemma/t20_R3_I/SPEC_ROUTE_B_N3.txt:244-263` |
| L02_C2_aws-249 | C | Formulations retirées : 'node by node', 'keep the same ones' | X | Codex (G2 ; addendum correction 2) | `master:lemma/t20_CODEX/REFEREE_T20_PROOF.md:106-112` |
| L02_C2_aws-250 | C | Table de provenance ARTIFACTS_T18_T20.md (réponse à G1) | E | LAB (17:50 UTC) : 'not reviewed' ; puis Codex a relu la l... | `master:lemma/ARTIFACTS_T18_T20.md:1-89` |
| L02_C2_aws-251 | C | Étiquette 'v1' et chemin 'ALL.txt' de la ligne I.1 (3,4,0) (corrigés) | X | Codex (REFEREE_PAPER, 'New issue in the supporting proven... | `master:lemma/t20_CODEX/REFEREE_PAPER_c1bcba6bb.md:94-110` |
| L02_C2_aws-252 | C | Acceptation de T20 par l'utilisateur et conversion du registre du labo | E | Codex (CHECKPOINT_156 : registre vivant et archive concor... | `master:lemma/t20_CODEX/CHECKPOINT_156.md:10-34` |
| L02_C2_aws-253 | C | Rôle de T20 dans la route (C) : paires différées | P | pont BRIDGE.md non lu dans la partie C (source secondaire) | `master:lemma/T20_WORK.md:15-18` |
| L02_C2_aws-254 | C | Corollaire Y1 (conditionnel à T18 et T20) et la paire 003:181:182 | P | certificats LAB (q/cert_y1.py, six contrôles négatifs) et... | `master:lemma/T20_BOARD.md:55` |
| L02_C2_aws-255 | C | Cas IIa par la main : une unité de jeu, non fermé par la main (round 1 A8) | O | - | `master:lemma/t20/T20_REPORT.md:105-109` |
| L02_C2_aws-256 | C | Énoncé du round 1 : PSD exact sur S <=> B connexe et valeurs propres hors 4 dans [-3,3] | H | non vérifié (T20_PROOF 10.4 item 11 : 'Not verified at al... | `master:lemma/t20/T20_REPORT.md:136` |
| L02_C2_aws-257 | C | Borne h_2 + 4h_3 + n_3/2 <= 7 et profils avec h_3 = 1 (round 1 A10) : remplacée | X | - | `master:lemma/t20/T20_REPORT.md:138-142` |
| L02_C2_aws-258 | C | Balayage des types d = 3, d = 4 sur 23 sommets (round 1 B4) : remplacé | X | deux programmes pour la colonne 'pass (L)' (t20_types_che... | `master:lemma/t20/T20_REPORT.md:186-204` |
| L02_C2_aws-259 | C | Exploration du round 2 : I.0 (4,2,1) avec N(p) dans la base (ne prouve rien) | H | - | `master:lemma/t20_R2/REPORT.md:116-118` |
| L02_C2_aws-260 | C | Premières versions fautives retirées (iii_enum.py, t20_verify.py) | X | - | `master:lemma/t20_R2/REPORT.md:133-134` |
| L02_C2_aws-261 | C | Round 3 : essais qui ne ferment rien | H | - | `master:lemma/t20_R3_I/REPORT.md:96-98` |
| L02_C2_aws-262 | C | Boîte de calcul à usage unique et autotest | E | - | `master:lemma/cloud/README.md:1-13` |
| L02_C2_aws-263 | C | Fermeture de n_3 = 2 par la main : il manque une identité globale (question ouverte) | O | - | `master:lemma/t20_HAND/NOTES.md:351-354` |
| L02_C2_aws-264 | C | Question de Codex : combiner la Prop. 2 et les comptes d'unités pour exclure un profil entier | O | - | `master:lemma/t20_CODEX/HAND.md:141-145` |
| L02_C2_aws-265 | C | Parties de T20_PROOF vues par leur seul auteur, et absence d'arbitre humain | P | auteur seul pour ces points au moment de l'écriture ; ens... | `master:lemma/T20_PROOF.md:2751-2762` |
| L02_C2_aws-266 | A | Ce qui survit des preuves T16/T18/T20 sans l'involution | P | non relu (« derived by hand, NOT refereed ») | `master:HANDOFF_2026-10-01.md:1177-1182` |
| L02_C2_aws-267 | A | Norme 14 sans σ : deux 7-ensembles reliés par le plan 2-(7,4,2) | P | non relu | `master:HANDOFF_2026-10-01.md:1183-1186` |
| L02_C2_aws-268 | A | Motif de famille srg(v,k,1,2) : m ≥ 1 + u(u+1)/2, égalité ssi biplan | P | non relu | `master:HANDOFF_2026-10-01.md:1187-1190` |
| L02_C2_aws-269 | A | Aucun 2-(11,5,2) dans les deux srg(243,22,1,2) | E | — | `master:HANDOFF_2026-10-01.md:1197-1200` |
| L02_C2_aws-270 | A | Codex : vecteurs propres entiers de norme ≤ 16 à entrées 0, ±1 | P | non indiqué (relais) | `master:HANDOFF_2026-10-01.md:1200-1202` |
| L02_C2_aws-271 | A | Route d'Hermite : mise en garde (route déjà close) | H | — | `master:HANDOFF_2026-10-01.md:1191-1193` |
| L02_C2_aws-272 | A | Programme thêta du labo : premiers verdicts par rang | C | « to be refereed » à cette date ; puis audit indépendant ... | `master:HANDOFF_2026-10-01.md:1207-1211` |
| L02_C2_aws-273 | A | Norme d'un vecteur dual ; minorations liées aux prismes ; classes ±1 de M | P | non relu ; un défaut corrigé par le labo | `master:HANDOFF_2026-10-01.md:1212-1218` |
| L02_C2_aws-274 | A | r ≥ 33 (accepté) et minima de L1 par rang | C | Codex (audit indépendant, note 168, branche codex/c1-arit... | `master:HANDOFF_2026-10-01.md:1222-1226` |
| L02_C2_aws-275 | A | r = 33 sans vecteur de Fano : a₈ ≥ 96 526 ; a₇ ≤ 7 920 | E | — | `master:HANDOFF_2026-10-01.md:1227-1228` |
| L02_C2_aws-276 | A | Lemme des graines (13 configurations) ⇒ a₈ ≤ 90 090 | P | « NOT yet refereed » à 22:36 UTC ; repris et affiné par C... | `master:HANDOFF_2026-10-01.md:1229-1235` |
| L02_C2_aws-277 | A | r ≥ 35 (accepté) ; échelle des vecteurs courts forcés | C | Codex (notes 168, 170, 172 de conway99-c1) | `master:HANDOFF_2026-10-01.md:1238-1242` |
| L02_C2_aws-278 | A | Contrainte vectorielle (représentation de Weil) : identiquement satisfaite | P | non relu | `master:HANDOFF_2026-10-01.md:1243-1246` |
| L02_C2_aws-279 | A | Classification exacte du dual M : peu de levier ; ce que le comptage ne peut pas faire | H | — | `master:HANDOFF_2026-10-01.md:1225-1226` |
| L02_C2_aws-280 | A | Bornes de Codex et du labo (tableau du 08/10 00:09 UTC) | P | « audited by Codex unless said » | `master:HANDOFF_2026-10-01.md:1252` |
| L02_C2_aws-281 | A | PL exact : la norme 18 est la couche pivot | E | — | `master:HANDOFF_2026-10-01.md:1260-1262` |
| L02_C2_aws-282 | A | Lemme A (deux vecteurs de norme 18 sur une même graine), cas partiels | P | non relu (« by hand, NOT refereed ») | `master:HANDOFF_2026-10-01.md:1263-1267` |
| L02_C2_aws-283 | A | Rang 35 exclu : r ∈ {37, 39, 41, 43} | E | LAP à la main, partiellement, sans erreur (L02_C2_aws-284... | `master:HANDOFF_2026-10-01.md:1271-1275` |
| L02_C2_aws-284 | A | Audit à la main de l'exclusion du rang 35 par LAP | P | (c'est un audit) | `master:HANDOFF_2026-10-01.md:1279-1283` |
| L02_C2_aws-285 | A | Cible b₄ du rang 37 ; b₄ ≥ 3 371 634 ; familles (4,4), (6,3), (7,1) | E | — | `master:HANDOFF_2026-10-01.md:1275-1278` |
| L02_C2_aws-286 | A | Exception de la note 183 par. 5 : le 12-ensemble U ; plafond 1 663 200 + 72P | P | non relu (envoyé au labo pour Codex) | `master:HANDOFF_2026-10-01.md:1284-1291` |
| L02_C2_aws-287 | A | Collisions de prismes jumeaux dans la famille (6,3) : critère et formes | P | non relu | `master:HANDOFF_2026-10-01.md:1293-1303` |
| L02_C2_aws-288 | A | Restriction e(W) ≤ 8 ; différences de triangles lointains ajoutables à b₃ | P | non relu | `master:HANDOFF_2026-10-01.md:1304-1306` |
| L02_C2_aws-289 | A | Rang 37 : plafond b₄ + (651/34)b₃ ≤ 17,40 M contre 39,7 à 66,6 M représentants | E | — | `master:HANDOFF_2026-10-01.md:1316-1318` |
| L02_C2_aws-290 | A | Les racines de M excluent les autres vecteurs courts : (a)-(e) | P | « what-if until audited » ; b₁ ≤ 78 re-démontré par Codex... | `master:HANDOFF_2026-10-01.md:1319-1326` |
| L02_C2_aws-291 | A | Espoirs locaux du labo réfutés par CP-SAT (localement possibles) | R | — | `master:HANDOFF_2026-10-01.md:1327-1332` |
| L02_C2_aws-292 | A | Le PL thêta du côté +3 ne majore pas les prismes jumeaux | R | — | `master:HANDOFF_2026-10-01.md:1333-1334` |
| L02_C2_aws-293 | A | Rang 43 : série thêta affine en six nombres ; formules et intervalles | E | Codex note 191 (commit 8622d91) : les cinq formules repro... | `master:HANDOFF_2026-10-01.md:1341-1348` |
| L02_C2_aws-294 | A | Rang 43 : trois conditionnels d'exclusion ; scénario minimal de l'adversaire | E | formules reproduites par Codex (note 191) | `master:HANDOFF_2026-10-01.md:1349-1355` |
| L02_C2_aws-295 | A | Triangles lointains d'un prisme ; 4τ ≤ #(prisme, triangle lointain) ; a₇ ≤ 842 | P | non relu | `master:HANDOFF_2026-10-01.md:1356-1360` |
| L02_C2_aws-296 | A | Codex note 191 : b₂ ≥ 462 + 41b₁ + b₁²/2 ; trois profils fractionnaires de norme 28 | P | non indiqué | `master:HANDOFF_2026-10-01.md:1371-1374` |
| L02_C2_aws-297 | A | Labo : profil C = 22-coclique marquée ; représentants de norme 4 sur supports spéciaux | P | non indiqué | `master:HANDOFF_2026-10-01.md:1375-1376` |
| L02_C2_aws-298 | A | Marge du coin prismes jumeaux (5,7 M) — remplacée | X | — | `master:HANDOFF_2026-10-01.md:1376-1379` |
| L02_C2_aws-299 | A | Question de la 22-coclique : structure forcée cohérente ; « pas de 22-coclique ⇒ a₇ = 0 » | O | non relu (« hand, not refereed ») | `master:HANDOFF_2026-10-01.md:1380-1385` |
| L02_C2_aws-300 | A | Codex : b₁ ≤ 44 à tout rang ; b₂ ≥ 968 au rang 43 | P | contre-lu par le labo | `master:HANDOFF_2026-10-01.md:1388-1389` |
| L02_C2_aws-301 | A | Réseau Λ d'une 22-coclique : programme thêta faisable ; b ≤ 14 | E | non relu | `master:HANDOFF_2026-10-01.md:1390-1399` |
| L02_C2_aws-302 | A | Λ au rang 43 : c ≤ 1, b = 2 ; vecteurs forcés seulement pour d ≤ 3 ; deux entrées ouvertes | O | non relu | `master:HANDOFF_2026-10-01.md:1404-1412` |
| L02_C2_aws-303 | A | Retrait par le labo de sa conjecture sur les vecteurs de norme 4 de Λ | X | — | `master:HANDOFF_2026-10-01.md:1406-1407` |
| L02_C2_aws-304 | A | Audit à la main de la note 185 de Codex (famille (4,4), 2794 par paire jumelle) | P | (c'est un audit) | `master:HANDOFF_2026-10-01.md:1419-1421` |
| L02_C2_aws-305 | A | Plafond du rang 37 reconstruit ; leviers ; coupe Fano démontrée mais inutile | E | accord avec le PL du labo | `master:HANDOFF_2026-10-01.md:1422-1426` |
| L02_C2_aws-306 | A | Correction de la marge par le labo : familles sûres sous les plafonds | E | — | `master:HANDOFF_2026-10-01.md:1427-1428` |
| L02_C2_aws-307 | A | Théorème de structure des prismes (labo) ; τ ≤ (P − 6ρ) + Σ C(g,2), g ≠ 5 | P | LAP (vérifié, « could not break it ») | `master:HANDOFF_2026-10-01.md:1429-1434` |
| L02_C2_aws-308 | A | Dictionnaire en un point : Γ₂(v), couplages σ_x, grilles | P | non relu | `master:HANDOFF_2026-10-01.md:1435-1436` |
| L02_C2_aws-309 | A | Configurations de grilles par un point : partitions équitables, test spectral passé (négatif) | P | non relu | `master:HANDOFF_2026-10-01.md:1437-1441` |
| L02_C2_aws-310 | A | Sous-réseaux de type rang 43 dans L1 à tout rang r < 43 (transfert d'exclusion) | P | non relu (« hand, NOT refereed ») | `master:HANDOFF_2026-10-01.md:1442-1448` |
| L02_C2_aws-311 | A | Budget par paire jumelle (labo, 08/10 midi) | E | — | `master:HANDOFF_2026-10-01.md:1449-1451` |
| L02_C2_aws-312 | A | Rang 37 en coordonnées lisibles (coefficients entiers) | E | le labo a vérifié la ligne b₄ contre son PL ; le reste « ... | `master:HANDOFF_2026-10-01.md:1453-1464` |
| L02_C2_aws-313 | A | Lectures du rang 37 : b₅, b₆ forcés ; ≥ 5 013 138 vecteurs de norme 28 ; coïncidences forcées | E | non relu | `master:HANDOFF_2026-10-01.md:1465-1470` |
| L02_C2_aws-314 | A | Routes « collisions paire par paire » et « plafond par normes 24/26 » closes comme méthodes | H | — | `master:HANDOFF_2026-10-01.md:1471-1474` |
| L02_C2_aws-315 | A | Route « au plus κ vecteurs propres par graine » : verdicts locaux, close comme méthode | S | — | `master:HANDOFF_2026-10-01.md:1475-1481` |
| L02_C2_aws-316 | A | Contrainte bilinéaire : rang de Gram ≤ 45 − r mod 7 sur L1 | P | le labo est d'accord avec l'énoncé | `master:HANDOFF_2026-10-01.md:1490-1495` |
| L02_C2_aws-317 | A | Codex notes 196-198 : τ ≤ 1403, τ_grid ≤ 11ρ + 17, P + 5ρ ≤ 1386 ; collisions de masse six | E | « certified on its side, not read by me » | `master:HANDOFF_2026-10-01.md:1496-1499` |
| L02_C2_aws-318 | A | Plafond comme variable de recensement : a₇ ≤ (2/21)N(F10) ; a₇ ≤ 347 au sommet riche en grilles | E | — | `master:HANDOFF_2026-10-01.md:1500-1502` |
| L02_C2_aws-319 | A | Lemme N16 (vecteurs de norme 16 contre les grilles) | P | labo (14:35 UTC, son horloge) : « re-derived step by step... | `master:HANDOFF_2026-10-01.md:1512-1517` |
| L02_C2_aws-320 | A | Classification au niveau du repère de p₀ (norme 16) — solveur | S | — | `master:HANDOFF_2026-10-01.md:1518-1525` |
| L02_C2_aws-321 | A | Valeur de N16 dans le PL joint : point mort 19 728 | E | — | `master:HANDOFF_2026-10-01.md:1533-1535` |
| L02_C2_aws-322 | A | Essais arrêtés : bornes de voisins communs, point à 21 grilles, normes 20 et 22 par graine | S | — | `master:HANDOFF_2026-10-01.md:1526-1528` |
| L02_C2_aws-323 | A | Principe du plus court représentant | P | non relu ; principe enregistré par le labo | `master:HANDOFF_2026-10-01.md:1538-1546` |
| L02_C2_aws-324 | A | Comptabilité par paires des supports ≤ 9 CLOSE (labo, NOTE 17.43-17.44) | E | « not re-computed by me » | `master:HANDOFF_2026-10-01.md:1548-1563` |
| L02_C2_aws-325 | A | Contre-exemple de Codex : trois prismes d'un pinceau, trois représentants dans une classe | R | — | `master:HANDOFF_2026-10-01.md:1564-1565` |
| L02_C2_aws-326 | A | Réservoir des plus courts : supports ≤ 9 insuffisants ; méthode b₄ épuisée pour ≤ 9 | E | « certified on its side » (Codex) ; « not re-computed by ... | `master:HANDOFF_2026-10-01.md:1566-1568` |
| L02_C2_aws-327 | A | Ce qui reste pour le rang 37 selon le labo (15:02 UTC) | O | — | `master:HANDOFF_2026-10-01.md:1582-1585` |
| L02_C2_aws-328 | A | Déterminant d'une droite dans g grilles (négatif) | E | non relu | `master:HANDOFF_2026-10-01.md:1596-1602` |
| L02_C2_aws-329 | A | Contenu des notes de septembre (vérification de duplication) | P | non relu ici (cité) | `master:HANDOFF_2026-10-01.md:1604-1614` |
| L02_C2_aws-330 | A | Borne de rang mod 7 sur TOUS les vecteurs du noyau : ≤ 56 − r | P | le labo a vérifié l'argument ; Codex confirme la borne (1... | `master:HANDOFF_2026-10-01.md:1615-1620` |
| L02_C2_aws-331 | A | Rangs exacts de systèmes de grilles par un point et autour d'une droite dans six grilles | E | labo (pencil6_rank7.py, NOTE 17.48, commit eb83e87 de con... | `master:HANDOFF_2026-10-01.md:1621-1627` |
| L02_C2_aws-332 | A | Lecture : classes de grilles presque indépendantes mod 7 (non démontré) | H | — | `master:HANDOFF_2026-10-01.md:1628-1631` |
| L02_C2_aws-333 | A | Labo : formes à trois hubs ; cible de 540 paires jumelles ; méthode polynomiale ρ ≤ 1330 | E | — | `master:HANDOFF_2026-10-01.md:1639-1645` |
| L02_C2_aws-334 | A | Codex : extensions d'une droite dans six grilles (108 extensions, mineurs d'ordre 20) | E | relais (certificat « in preparation ») | `master:HANDOFF_2026-10-01.md:1646-1652` |
| L02_C2_aws-335 | A | L'énoncé manquant du rang 37 : minorer le rang en fonction du nombre de paires jumelles | O | — | `master:HANDOFF_2026-10-01.md:1655-1660` |
| L02_C2_aws-336 | A | Vérifications à la main autour de la borne de rang (dépendances mod 7, motifs de trois grilles) | P | non relu | `master:HANDOFF_2026-10-01.md:1661-1674` |
| L02_C2_aws-337 | A | Lien avec la note 127 : 231 droites pour 18 dimensions | H | — | `master:HANDOFF_2026-10-01.md:1675-1678` |
| L02_C2_aws-338 | A | Conversion du labo (NOTE 17.49) : rang 37 exclu si τ_g < 614 sans paire non grille, ou ρ ≤ ~58 | E | — | `master:HANDOFF_2026-10-01.md:1681-1683` |
| L02_C2_aws-339 | A | Codex notes 202, 203 : motifs (2,2,1), (2,2,2) impossibles au rang ≥ 37 ; 3n₃ ≤ 2n₁ + n₂ | E | relais ; « certified without solver » | `master:HANDOFF_2026-10-01.md:1684-1687` |
| L02_C2_aws-340 | A | Comptage de dimension « relations de pinceaux seulement » ⇒ rang 37 exclu (hypothèse fausse) | X | « hand reasoning NOT refereed » | `master:HANDOFF_2026-10-01.md:1688-1703` |
| L02_C2_aws-341 | A | Relations en un sommet dans tout graphe ; la cible « au plus 10 relations » était fausse | P | — | `master:HANDOFF_2026-10-01.md:1705-1716` |
| L02_C2_aws-342 | A | Rang 37 = cas d'égalité ; chaîne de septembre ((a′), NT, droites déconnectées) ouverte | O | — | `master:HANDOFF_2026-10-01.md:1717-1723` |
| L02_C2_aws-343 | A | Composantes aux sept droites d'un sommet : rang centré mod 7 de 4 à 14 | P | non relu | `master:HANDOFF_2026-10-01.md:1724-1731` |
| L02_C2_aws-344 | A | Identités exactes pour une droite à graphe cubique CONNEXE (τ, dét, ι) ; filtre | P | « hand, not machine-checked » à la date ; constantes test... | `master:HANDOFF_2026-10-01.md:1732-1739` |
| L02_C2_aws-345 | A | Contrôle arithmétique des identités sur 60 graphes cubiques connexes | E | — | `master:HANDOFF_2026-10-01.md:1749-1756` |
| L02_C2_aws-346 | A | La recherche d'étoile de septembre n'utilise que mod 7 ; témoin de Codex à dix ombres | E | — | `master:HANDOFF_2026-10-01.md:1757-1761` |
| L02_C2_aws-347 | A | Remarque « classe carrée de τ(G(T)) » retirée (pas nouvelle) | X | — | `master:HANDOFF_2026-10-01.md:1771-1773` |
| L02_C2_aws-348 | A | Identités de Green RÉELLES pour une droite connexe ; conditions (a)-(d) | P | vérifié par une trace (Σ sur les 60 lointains de nᵀH⁺n = ... | `master:HANDOFF_2026-10-01.md:1774-1789` |
| L02_C2_aws-349 | A | Élagage mesuré par (a) et (b) : modeste | E | — | `master:HANDOFF_2026-10-01.md:1790-1794` |
| L02_C2_aws-350 | A | Reformulation : droite générique au rang 37 ⇔ aucun vecteur de ker₇(A − 3I) sur N(T) | P | — | `master:HANDOFF_2026-10-01.md:1795-1799` |
| L02_C2_aws-351 | A | Lecture : l'obstruction des étoiles est dans la forme 0/1 des ombres | H | — | `master:HANDOFF_2026-10-01.md:1800-1803` |
| L02_C2_aws-352 | A | Ablation de Codex (note 214) ; l'équation d'une étoile dépend des ombres | P | — | `master:HANDOFF_2026-10-01.md:1805-1821` |
| L02_C2_aws-353 | A | Dérivation de (d) ; facteur t identifié ; confirmation indépendante de Codex (note 217) | P | Codex (note 217 annoncée ; lab commit 916cdcc, NOTE 17.60... | `master:HANDOFF_2026-10-01.md:1822-1829` |
| L02_C2_aws-354 | A | Mineurs 3 × 3 : les 473 branches d'apex de la boule cyclique (2,4,1) rejetées | E | « not re-run here » ; partie « quatre boules » en attente... | `master:HANDOFF_2026-10-01.md:1834-1840` |
| L02_C2_aws-355 | A | Pas de borne de comptage uniforme en G pour les étoiles | H | — | `master:HANDOFF_2026-10-01.md:1841-1847` |
| L02_C2_aws-356 | A | Piste « énergie d'apex » réfutée | R | — | `master:HANDOFF_2026-10-01.md:1848-1850` |
| L02_C2_aws-357 | A | Identité Z² = 7Z − NᵀN + J (rien de nouveau) | P | — | `master:HANDOFF_2026-10-01.md:1851-1853` |
| L02_C2_aws-358 | A | Conditions sur l'apex seul automatiques ; reformulation de Seidel ; boule 12 (labo) | P | — | `master:HANDOFF_2026-10-01.md:1863-1878` |
| L02_C2_aws-359 | A | Attaque propre des quatre rangs : aucune exclusion ; doublons évités | P | — | `master:HANDOFF_2026-10-01.md:1881-1888` |
| L02_C2_aws-360 | A | Formule d'oddité : H_L elliptique aux quatre rangs, H_K hyperbolique | P | non relu | `master:HANDOFF_2026-10-01.md:1889-1893` |
| L02_C2_aws-361 | A | Déterminants exacts des réseaux locaux en un sommet : dét L_v = 2²¹·7^(r−15), dét K_v = 3⁸5⁶·7^(r−15) | P | « not audited by anyone » ; chaque déterminant recalculé ... | `master:HANDOFF_2026-10-01.md:1894-1914` |
| L02_C2_aws-362 | A | Ce que donnent ces déterminants : Hermite et comptes gaussiens au seuil | H | — | `master:HANDOFF_2026-10-01.md:1915-1918` |
| L02_C2_aws-363 | A | Faits annexes ; au rang 39 le résidu de rang 2 est anisotrope ssi τ(G(T)) est résidu quadratique | P | non audité | `master:HANDOFF_2026-10-01.md:1919-1927` |
| L02_C2_aws-364 | A | Théorème (rang 37) : une droite dont le graphe a une maille ≥ 5 est connexe | E | Codex (note 224, commit e7bba78 de codex/c1-arithmetic-au... | `master:c1_rank37_girth5_lines/NOTE.md:1-18` |
| L02_C2_aws-365 | A | Modèle mod 7 de dimension 36 (points 1 à 4 et 7 de la note maille 5) | P | Codex note 224 (points 1 à 7 re-dérivés, sans défaut) ; c... | `master:c1_rank37_girth5_lines/NOTE.md:20-32` |
| L02_C2_aws-366 | A | Lemme I : un vecteur de torsion porté par UNE composante n'est jamais équilibré | E | déjà dans la note 126 par. 3 bis (avec sa propre vérifica... | `master:c1_rank37_girth5_lines/NOTE.md:33-37` |
| L02_C2_aws-367 | A | Les 7 types de composantes à trois droites par couche ; quatre cas | E | Codex note 224 (288 formes normales, 7 types) | `master:c1_rank37_girth5_lines/NOTE.md:38-47` |
| L02_C2_aws-368 | A | Recherches exhaustives d'étoiles : cas (0,0), (0,1), (1,0), (1,1) — aucune étoile | E | les 576 recherches NON rejouées par Codex (note 224) | `master:c1_rank37_girth5_lines/NOTE.md:58-77` |
| L02_C2_aws-369 | A | Cas (3,3) de maille 5 : 33 784 128 matrices → 25 588 → 44 → 0 | E | Codex note 224 : fin du cas (3,3) reproduite (25 588 → 44... | `master:c1_rank37_girth5_lines/NOTE.md:78-88` |
| L02_C2_aws-370 | A | Contrôles du résultat maille 5 (deux formulations, étoile plantée, sans mod 7) | E | — | `master:c1_rank37_girth5_lines/NOTE.md:90-100` |
| L02_C2_aws-371 | A | Force de la méthode des étoiles : D = c − 1 ; table h mod 7 des composantes prismes | P | — | `master:HANDOFF_2026-10-01.md:1963-1969` |
| L02_C2_aws-372 | A | Réduction des 4-cycles et comptes exacts des types de composantes | E | accord avec l'énumération Python et les 15 du labo | `master:HANDOFF_2026-10-01.md:1970-1979` |
| L02_C2_aws-373 | A | Addendum 1 : trois composantes à deux droites par couche (« (4,4,4) » = (2,2,2)) — aucune étoile | E | non audité (« same status as above (computer-assisted, no... | `master:c1_rank37_girth5_lines/NOTE.md:119-129` |
| L02_C2_aws-374 | A | Fait A : relations de composantes vraies à tout rang ; K_{3,3} jamais une composante | P | le labo et Codex ont la forme générale (NOTE 17.77 ; note... | `master:c1_rank37_girth5_lines/NOTE.md:138-145` |
| L02_C2_aws-375 | A | Profil (3,3) sans prisme complet : toutes les torsions mortes (6,57e9 nœuds) | E | non audité | `master:c1_rank37_girth5_lines/NOTE.md:151-163` |
| L02_C2_aws-376 | A | Trois réductions : boules (2,4) par classe d'isomorphisme ; lemme de paires ; orbites | E | le labo a reconstruit les fichiers de (1) (mêmes hachages... | `master:c1_rank37_girth5_lines/NOTE.md:168-185` |
| L02_C2_aws-377 | A | Énoncé B (droites sans prisme au rang 37 ⇒ G(T) connexe) — INCOMPLET | O | non audité (seule la partie maille 5 l'a été, Codex note ... | `master:c1_rank37_girth5_lines/NOTE.md:131-136` |
| L02_C2_aws-378 | A | Les conditions réelles seules ne décident pas ; échantillon de 150 boules connexes sans prisme | E | — | `master:c1_rank37_girth5_lines/NOTE.md:187-199` |
| L02_C2_aws-379 | A | La droite dans six grilles n'est pas décidée par une étoile ; fastr2.c non validé | E | — | `master:c1_rank37_girth5_lines/NOTE.md:220-223` |
| L02_C2_aws-380 | A | Comptabilité à P = 0 (labo, 23:40 UTC) : conditionnel ; « rang 37 ⇒ P > ~285 » | E | — | `master:HANDOFF_2026-10-01.md:1992-1995` |
| L02_C2_aws-381 | A | Coût d'une exclusion exhaustive par étoiles (estimation) | H | « estimation, non mesurée » | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:227-231` |
| L02_C2_aws-382 | A | Verdict du Mandat C : aucun résultat substantiel pour C1 | H | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:1-16` |
| L02_C2_aws-383 | A | Proposition C (cible) : l'étage lointain déterminé par la boule et les 60 ombres — non démontrée | O | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:30-38` |
| L02_C2_aws-384 | A | Lemme 1 : deux candidats diffèrent de D = 7(E − E′) (paire de projecteurs) | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:42-52` |
| L02_C2_aws-385 | A | Lemme 2 : un mouvement de rang 2 est l'échange de deux sommets | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:54-60` |
| L02_C2_aws-386 | A | Théorème 3 : aucun mouvement par bloc orthogonal sur moins de k/2 + 2 sommets (9 pour 99, 13 pour 243) | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:62-75` |
| L02_C2_aws-387 | A | Lemmes 4 et 5 : bascules à boule fixée (lignes de poids ≥ 3+3 ; vecteurs propres à support dans S) | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:77-92` |
| L02_C2_aws-388 | A | Lemme 6 et Théorème 7 : rang₇(D) ≤ r + r′ − 74, donc r + r′ ≥ 78 ; pas de seconde complétion de rang 37 ni 39 | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:94-108` |
| L02_C2_aws-389 | A | Corollaire 8 (symétrie forcée, conditionnelle) au rang 37 générique | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:110-112` |
| L02_C2_aws-390 | A | Lemme laplacien de Codex : au rang 37 générique la complétion est unique parmi tous les rangs | P | LAP (« J'ai relu l'argument, il est correct ») | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:114-124` |
| L02_C2_aws-391 | A | Codex note 233 : aucune différence D de rang ≤ 4 (fermerait (39,39)) — annoncé, non relu | E | NON relu par LAP (« la note n'est pas accessible depuis c... | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:126-131` |
| L02_C2_aws-392 | A | Cas restants de la proposition C | O | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:133-136` |
| L02_C2_aws-393 | A | La bascule BvLS → 243 tordu décodée : re-réglure simultanée de 80 grilles lointaines (D³ = 45D) | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:138-154` |
| L02_C2_aws-394 | A | Remarque 9 : une re-réglure à 99 demande g ≥ 3 grilles par sommet touché | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:156-164` |
| L02_C2_aws-395 | A | Pilote local sensible au rang (repères de rangs 30 et 40) : aucune coupe | S | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:166-174` |
| L02_C2_aws-396 | A | Obstacle précis : la route « transformations » ne décide pas C1 | H | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:176-188` |
| L02_C2_aws-397 | A | Lemme 10 (scindage entier Z_Λ = N_far ⊥ K_far) et Corollaire 11 | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:202-212` |
| L02_C2_aws-398 | A | Lemme 12 (discriminants, tout rang, G(T) connexe) | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:214-218` |
| L02_C2_aws-399 | A | Cadre du sommet au rang 37 : résidus dans un espace de dimension 22, code auto-orthogonal [84, 22] | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:220-225` |
| L02_C2_aws-400 | A | Séries thêta pondérées par un quartique harmonique : énoncé et coefficients exacts | P | aucune relecture mentionnée ; relation de Fricke contrôlé... | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:233-255` |
| L02_C2_aws-401 | A | Test quartique : faisable aux rangs 37, 39, 41, 43 en arithmétique exacte ; infaisabilités flottantes = art... | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:257-273` |
| L02_C2_aws-402 | A | Réponse du LAB : 64 coins faisables au rang 37 ; les sommes du catalogue ne peuvent pas rendre 37 infaisable | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:275-282` |
| L02_C2_aws-403 | A | Proposition 13 : [M : Λ_L] = 3^(e₃−1) (saturation du réseau des droites) | P | aucune relecture mentionnée ; étapes contrôlées à la mach... | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:286-304` |
| L02_C2_aws-404 | A | Corollaires de la proposition 13 (e₃ ≤ 22, e₂ ≤ 27, e₅ ≤ 27 ; au moins 33 droites monochromes) | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:306-319` |
| L02_C2_aws-405 | A | Contrôle machine de la proposition 13 sur srg(243,22,1,2) (BvLS) | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:393-398` |
| L02_C2_aws-406 | A | Nombres forcés par rang (programme exact de degré 0 des notes 167-168) | E | « recoupent les notes 177 et 192 de Codex » | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:321-335` |
| L02_C2_aws-407 | A | Programme thêta à neuf classes : entrées démontrées (minima par classe, objets d'égalité) | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:339-367` |
| L02_C2_aws-408 | A | Programme thêta à neuf classes : validé, faisable aux rangs 37-43, sans gain (fermé au degré 0) | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:337-376` |
| L02_C2_aws-409 | A | Variante impaire (cubique) à neuf classes : 19 paramètres libres, fermée | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:378-391` |
| L02_C2_aws-410 | A | Rang 43 : les 49 classes de L1/√7M une par une ; 19 paramètres libres ; relations exactes | E | contrôle interne contre la note 177 | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:400-440` |
| L02_C2_aws-411 | A | Rang 43 : conséquences par classe ; scénario S₀ entièrement déterminé et intègre | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:442-454` |
| L02_C2_aws-412 | A | Majoration des 22-cocliques au rang 37 dans le programme à neuf classes : 93 696 (sans effet) | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:456-458` |
| L02_C2_aws-413 | A | Rang 43 : sommes vectorielles par classe déterminées par celles des normes 16 à 24 | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:460-467` |
| L02_C2_aws-414 | A | Rang 43 : seconds moments par classe ; dans S₀ un seul tenseur libre, isotropie non forcée | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:469-488` |
| L02_C2_aws-415 | A | S₀ dans le programme à neuf classes : sept paramètres, intervalles exacts, point entier | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:490-526` |
| L02_C2_aws-416 | A | S₀ : géométrie forcée (au moins 4979 vecteurs de classe 2, norme 40/9, non arêtes ; quatre profils) | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:528-536` |
| L02_C2_aws-417 | A | Origine des vecteurs fantômes de classe 2 dans S₀ (sommets fantômes, vecteurs entiers de norme 4 plus une a... | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:538-549` |
| L02_C2_aws-418 | A | Lemme 14 (tout rang) : un vecteur propre entier binaire de norme 28 a e(X) = e(Y) ≤ 5 | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:551-557` |
| L02_C2_aws-419 | A | S₀ sans fantôme : au moins 2289 vecteurs à support positif indépendant, dont au moins 2001 de profil (1⁷ ; ... | E | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:559-572` |
| L02_C2_aws-420 | A | Couches forcées dans S₀ ; plus petit objet forcé : P3/N25 (au moins 10) | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:574-599` |
| L02_C2_aws-421 | A | Codex : S₀ exige ≥ 2289 + 15g configurations (1⁷ ; (−1)²⁹) ; une borne uniforme 2288 fermerait S₀ | P | non vérifié par LAP | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:601-603` |
| L02_C2_aws-422 | A | Retrait de Codex : l'annonce « S₀ exclu » est retirée (note 245) ; 5345 supports ouverts | X | relayé par le LAB vers 17:0x UTC, non vérifié par LAP | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:605-610` |
| L02_C2_aws-423 | A | Identité exacte du nombre de P3/N25 dans S₀ (certificat de Farkas à six lignes) | C | vérification par le même auteur (somme identiquement −1) ... | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:612-626` |
| L02_C2_aws-424 | A | Unicité du profil (1³ ; (−1)²⁵) pour la classe 2 de norme 208/9, à tout rang | P | aucune relecture mentionnée (« preuve écrite ») | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:628-633` |
| L02_C2_aws-425 | A | Validation de bout en bout du programme à neuf classes sur K₈ ⊕ B¹⁸ | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:635-639` |
| L02_C2_aws-426 | A | Rang 43 général (15 paramètres) : aucune couche basse n'est forcée seule | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:641-645` |
| L02_C2_aws-427 | A | Pistes arithmétiques fermées dans S₀ (cubique, divisibilités, 441 classes, sommes vectorielles) | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:647-663` |
| L02_C2_aws-428 | A | Forme de Jacobi des droites (indice 2) : ne ferme pas S₀ ; rangs 37 à 43 faisables | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:665-702` |
| L02_C2_aws-429 | A | Distribution d'un vecteur P3/N25 sur les droites : effectifs (9 − δ, 59 + 3δ, 163 − 3δ, δ), δ ≤ 9 | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:704-709` |
| L02_C2_aws-430 | A | Jacobi des droites classe par classe dans S₀ : 51 équations de rang 17, compatibles ; aucune fermeture | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:711-738` |
| L02_C2_aws-431 | A | Identité de budget de tout le rang 43 : 17a₇ + 10a₈ + 4a₉ + 4a₁₀ + 2a₁₁ + a₁₂ + f₁₁ ≤ 10 + objets bas | E | contrôles internes (entier + 2·fractionnaire en norme 26 ... | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:742-767` |
| L02_C2_aws-432 | A | S₀ en coordonnées naturelles : congruences ; S₀ n'est jamais « sans objet bas » ; n ≥ 11 | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:769-789` |
| L02_C2_aws-433 | A | Liens géométriques entre objets bas de S₀ (g_ℓ ≥ 22κ ; g_v ≥ 1 ⇒ g_ℓ ≥ 1 ; c₁ ≠ 1) | P | aucune relecture mentionnée (« à la main ») | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:791-801` |
| L02_C2_aws-434 | A | Formes de Jacobi de niveau 1 au rang 43 : identités exactes nouvelles, aucune violée | E | outil contrôlé sur le réseau de Leech | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:803-825` |
| L02_C2_aws-435 | A | Produits de deux vecteurs P3/N25 au rang 43 ; dans S₀ deux d'entre eux sont dans la même classe | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:827-831` |
| L02_C2_aws-436 | A | Profils uniques dans S₀ ; c₁ pair ; correction du tableau du §13 | P | aucune relecture mentionnée (« à la main ») | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:833-848` |
| L02_C2_aws-437 | A | Histogrammes de coordonnées (Jacobi des sommets) dans S₀ : 40 équations de rang 12, aucun intervalle changé | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:849-859` |
| L02_C2_aws-438 | A | Relèvement d'un vecteur court dans U (rang 43, sans racine) : a₂(U) ≡ 0 mod 6 ; n'exclut aucun type | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:865-873` |
| L02_C2_aws-439 | A | Structure cyclique des classes des vecteurs P3/N25 (étiquetage par Z/8) | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:875-879` |
| L02_C2_aws-440 | A | Recherche combinatoire P3/N25, étage 1 : énoncé exact ; solveurs génériques sans décision ; 59 infaisables ... | C | certificats revérifiés par le même auteur ; pas de relect... | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:881-904` |
| L02_C2_aws-441 | A | Crible linéaire avec certificats : 1766 supports traités, 326 tués, 326 certificats exacts (arrêté) | C | certificats exacts revérifiés par le même auteur ; pas de... | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:902-904` |
| L02_C2_aws-442 | A | Lemme A (parabole entière) pour tout ensemble de sommets d'un srg(99,14,1,2) | P | aucune relecture tierce mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:911-934` |
| L02_C2_aws-443 | A | Lemme B (plafond) | P | aucune relecture tierce mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:936-942` |
| L02_C2_aws-444 | A | Lemmes A et B : 941 supports éliminés avec témoins revérifiés ; 3640 restent | C | témoins revérifiés par un programme du même auteur (check... | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:944-956` |
| L02_C2_aws-445 | A | Niveau 2 (lemmes A et B sur S ∪ {z}) : 8 morts sur 63 ; 5 certificats vérifiés indépendamment | C | 5 certificats vérifiés par un programme indépendant écrit... | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:964-987` |
| L02_C2_aws-446 | A | Lemme C (sommet d'un triangle par un positif) | P | « preuve à la main » ; aucune relecture tierce mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:989-1011` |
| L02_C2_aws-447 | A | Lemme C : 567 supports le violent, dont 297 non tués par A et B (3640 → 3343) | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:1013-1016` |
| L02_C2_aws-448 | A | Moteur d'étoile (CP-SAT) : 366 positifs sans étoile, dont 72 hors lemme C (verdicts de solveur) | S | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:1018-1032` |
| L02_C2_aws-449 | A | Pourquoi les 51 positifs sans coupe meurent (lecture du support 3344) : comptage de degrés | P | aucune relecture mentionnée | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:1034-1041` |
| L02_C2_aws-450 | A | Vérification exhaustive sans solveur des 72 verdicts « positif sans étoile » : 72 sur 72 confirmés | E | « Programme et règles écrits par moi seul, non relus par ... | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:1083-1086` |
| L02_C2_aws-451 | A | Coquille des trois positifs : chaque coquille trouvée réfutée par le lemme A ; boucle non fermée | S | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:1043-1052` |
| L02_C2_aws-452 | A | Étoile double et extension au troisième positif : non-extension vue seulement sur le support 4 | S | « Verdicts de solveur, non revérifiés » | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:1072-1081` |
| L02_C2_aws-453 | A | Bilan P3/N25 : 4581 → 3640 → 3343 → 3271 ; 1310 supports tués avec témoins vérifiables sans solveur | E | pas de relecture tierce | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:1054-1065` |
| L02_C2_aws-454 | A | Rang 37 (programme à neuf classes sans égalité de classe) : aucun objet bas fractionnaire forcé | E | — | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:1088-1091` |
| L02_C2_aws-455 | A | Rang 37 sans norme 14 : au moins 11 paires ±v de norme ≤ 20 (avec la ligne des chemins induits) | E | « Minima d'un programme linéaire, sans certificat écrit n... | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:1103-1112` |
| L02_C2_aws-456 | A | Rang 37, a₈ = 0 : 7a₉ + a₁₀ ≥ 574 ; la facette duale du labo n'est pas améliorée par les neuf classes | E | « sans certificat écrit ni relecture » | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:1114-1119` |
| L02_C2_aws-457 | A | Absence du dossier c1-lap-girth5-audit/ ; état des versions sur les autres branches | E | — | `master:c1_rank37_girth5_lines/NOTE.md` |
| L02_C2_aws-458 | L | Combinaison α (vue par L02) : symétrie forcée au rang 37 générique + exclusion des ordres 2, 3, 7, 11 | O | non relu (chaîne vue par l'agent L02) | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:36-37,110-112,197-200` |
| L02_C2_aws-459 | L | Combinaison β (vue par L02) : lemmes T sans σ contre vecteurs courts forcés au rang 37 | O | non relu (chaîne vue par l'agent L02) | `master:HANDOFF_2026-10-01.md:1177-1186,1200-1202,1206-1208` |
| L02_C2_aws-460 | L | Combinaison γ (vue par L02) : outils du rang 43 transférés aux rangs 37, 39, 41 | O | non relu (chaîne vue par l'agent L02 ; transfert proposé ... | `master:HANDOFF_2026-10-01.md:1442-1448` |
| L02_C2_aws-461 | L | Combinaison δ (vue par L02) : levée de la réserve de la règle jumelle par comptes exacts de racines | O | non relu (chaîne vue par l'agent L02 ; plan décrit par le... | `master:lemma/t20_CODEX/REFEREE_TWIN_DEPENDENCIES.md:10-26,61-133` |
| L02_C2_aws-462 | L | Combinaison ε (vue par L02) : lemmes A et B (tout ensemble de sommets) appliqués aux configurations finies ... | O | non relu (chaîne vue par l'agent L02 et par la partie A) | `master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:911-942,953` |
| L02_C2_aws-463 | L | Combinaison ζ (vue par L02) : bornes de rang des lemmes T pour un automorphisme d'ordre 3 ou sans automorph... | O | non relu (vu par l'agent L02 et par la partie B) | `master:lemma/T18_PROOF.md:653-700,786-837` |

## 12. Routes fermées et pourquoi

### Partie K (campagne de calcul)

- **Plan « 54 tranches » sur trois comptes** (29/09) : abandonné quand le compte a lâché ; « ARCHIVE ... ne plus utiliser », remplacé par la file adaptative (`master:OLD_README_54_TRANCHES.md:1` ; `master:HANDOFF_2026-10-01.md:32`).
- **Azure** : couche jamais construite (quotas Spot à 3 vCPU, demandes refusées, ticket ouvert) ; aucune machine Azure (`master:HANDOFF_2026-10-01.md:76-95`).
- **Machines ARM (Graviton c8g)** : STOP CALIB sur la calibration v2 (« some content field differs on aarch64 ») ; à ne plus utiliser sans enquête (`master:HANDOFF_2026-10-01.md:459-460`).
- **Capacité Intel/ARM à eu-west-2d et régions chères** : récupérées en 20-60 min, moins efficaces par dollar ; les 8 machines us-east-1 / us-west-2 / eu-west-2 du 06/10 arrêtées (1,5 à 1,8 fois plus chères par job) (`master:HANDOFF_2026-10-01.md:332,665-668`).
- **Jobs longs (10-32 h)** : 2 500 heures-job perdues aux interruptions Spot ; remplacés par des sous-jobs x8 / x10 puis des jobs fins (un y1 par job) et le tail runner (`master:HANDOFF_2026-10-01.md:502-511,536-544,681-690`).
- **Planifier sur est_h** : faux (estimation v1 répartie uniformément ; ratios réels 0,24 à 30) (`master:HANDOFF_2026-10-01.md:541-542,645`).
- **Recherche complète des paires couvertes par T18/T20** : 5 000 à 9 000 heures-cœur estimées ; remplacée par la mise de côté avec certificats (`master:HANDOFF_2026-10-01.md:710-712,774-791`).
- **Force brute sur 003:181:182** (5,2 h sur 124 coeurs, cinq exécutions aveugles d'environ 18 heures-machine) : remplacée par le corollaire Y1 (L02_C2_aws-020).
- **Garder les enregistrements « sans version »** : refusé par l'utilisateur le 07/10 au soir ; remplacé par les certificats Y1, la reprise des 713 et des 28 réseaux (L02_C2_aws-025, L02_C2_aws-026, L02_C2_aws-028).
- **Prendre le mot « excluded » du tracker comme certificat dans la règle jumelle** : refusé par Codex ; d'où le point ouvert L02_C2_aws-030.

### Partie B : T16, T18 et le pont

- **Certificat local autour d'une racine d'énergie 9** (L02_C2_aws-154) : règle R9a, 0 candidat retiré ; recherche à neuf mots plus lente
  (100 s contre 2 s par paire) et non décisive ; « The obstruction is not local to r » (`LEMMA_TARGET_2026-10-06.md:82-97`).
  Forcer « 0 ou 2 des 7 h rencontrent r » dans le DFS : non essayé, élagage attendu modeste (idem :94-95).
- **Tests au niveau du support seul** : PSD exacte sur S, S u {p}, S u {p,w,sigma w} ne tue aucune S-structure ; `ninf.py`
  (33 sommets) non exhaustif et test de réseau sans rejet ; énumération niveau 1 + test F1 trop lâche (L02_C2_aws-151) ; sigma-parité
  pondérée vacuité (« (B^3 + B)_ii even, always true ») ; partition {S, D_0, D_1, D_2} : seulement e(D_0) = e(D_2) <= 9 ;
  hexagones de B0 sans contradiction (`lemma/t18/T18_REPORT.md:121-135`).
- **Round 2** : test « étoile » `star.py` abandonné (7 de 8 vivants) ; énumération X_0 d'abord correcte mais lente ;
  complétion du Gram impair sur T u X_2 (`r2_gram.py`) faible ; **double comptage du cube non transférable** (L02_C2_aws-171)
  (`T18_REPORT.md:273-283`).
- **Round 3-4** : premières versions de l'étape C trop lentes ; vérificateurs « ordre dual » v0, v1 corrects mais 20 à 50 s par
  triple ; v2 avec tests impairs seuls explose ; **condition de noyau de l'étape D vacuité** (L02_C2_aws-172) (`T18_REPORT.md:424-435`, `633-642`).
- **Tentative structurelle (STRUCT)** : « No hand proof closes profile (2,5,0) » ; sommet agrégé Z (0 rejet), inégalités
  déflatées, route réseau H16 avec les nouveaux vecteurs, parités, paramètres de Krein (aucun nul), forme quotient de E_{-4},
  double comptage du cube, t = 6 par (**) et (L), e_1 = 4 ; réductions mod 2, 3, 7 « give nothing usable »
  (`lemma/t18_STRUCT/REPORT.md:3`, `100-112`).
- **Route X_0 d'abord pour B0** (L02_C2_aws-152) : partielle (81 de 2 667) ; S u X_0 u X_2 seul n'exclut pas B0 et la borne de rang ne tue
  pas les 8 tables restantes ; seule l'étape C (W) conclut.
- **A7 / H16 dans T18** : l'outil n'a rien retiré au-delà du PSD (`T18_REPORT.md:94-103`) ; inutilisé.
- **Dossier T16** : avant Wagner, le test de rang simple ne fournissait pas l'argument de fermeture sur 25 paires
  (`LEMME_EGALITE_8_SUR_7_C2.txt:243-258`) ; « Les tests de Gram ont aussi laissé des candidats et ne donnent pas de contradiction
  supplémentaire générale » (`..._PREUVE_CUBE.txt:238-241`).
- **Pont** : dériver l'existence de U du cadre seul (forme discriminante 7-adique hyperbolique) : non abouti
  (`lemma/BRIDGE.md:458-463`).

### Partie C : T20 et les calculs des branches lemma-run

- **Route A pour n_3 = 2** (base S u {p} u X_3 u X_0', 700 classes, moteur eng5z de LAB) : abandonnée sur coût, pas sur un résultat
  mathématique. 183 classes fermées par recherche et 96 par le lemme d'isolation seul, 421 ouvertes, 0 configuration complète ; mesure :
  environ 1,000 heures-cœur par programme (jusqu'à 2,000) (`master:lemma/T20_BOARD.md:13`, `:15`). Le second programme de Codex
  (route A) est mis en attente (`master:lemma/t20_CODEX/n3_second/MEASUREMENTS.md:45-59`). Remplacée par la route B (environ 7 h CPU
  sur un portable pour les deux programmes, `master:lemma/T20_PROOF.md:2532`).
- **Fermeture à la main de IIa** : une unité de jeu dans l'argument de T18 A3 (`master:lemma/t20/T20_REPORT.md:105-109`, `:295`) ;
  fermé par calcul.
- **Fermeture à la main de n_3 = 2** : non atteinte ; « a hand closure of n_3 = 2 needs a new global identity »
  (`master:lemma/t20_HAND/NOTES.md:351-354`).
- **Règle de norme duale comme filtre** : aucun certificat sur S, S u {z,z'}, S u N(p) (échantillons) ; conditionnelle à (E14) ; non
  utilisée (`master:lemma/t20_HAND/NOTES.md:217-220`, `master:lemma/t20_R3_I/REPORT.md:98`).
- **Translation réticulaire c -> c - G e_O** pour le motif {2,1^6} : redonne la norme 10, ne se ramène pas à un lemme de vecteur plus court
  (`master:lemma/t20/T20_REPORT.md:290-292`) ; fermé par la preuve directe A2.
- **Identités globales du cas I** (cellules C6, C7, (Q0), matchings) : satisfaites par toutes les solutions, ne ferment rien
  (`master:lemma/t20_R3_I/REPORT.md:96-98`, `master:lemma/t20/T20_REPORT.md:294`).
- **Runs nuage abandonnés** : t20_Iv_A (installation seulement), t20_Iv_F (Spot repris), I.1 (4,2,1) de t20_Iv_E (vérificateur v1 avorté,
  machine reprise) ; refaits par t20_I1_340 et t20_Iv_G..J.

### Partie D : réduction, audits, papier

- **Dépendance à g ∈ {18,20}** (chaîne g ≥ 14, puis Blichfeldt, puis note C1 132 « to be reread »). Elle n'est plus nécessaire,
  car A.4 donne la classe de Witt pour tout g (AUDIT_REDUCTION.md:14-18, 341). De plus, aucune règle du moteur n'utilise g
  (AUDIT_ENGINE_RULES.md:372-379).
- **Citation de Makhnev-Minakova pour F0.** Elle n'est plus nécessaire, car A.0 la prouve à la main (AUDIT_REDUCTION.md:19-21).
  Le crédit à MM est maintenu dans le papier (main.tex:191-194).
- **Exclure 143 par un solveur** (budget de composantes, MILP, 28/09). Abandonné : un statut de solveur n'est pas admis comme
  preuve (H4). La méthode est remplacée par la preuve à la main (LATTICE_143.md:3-5, 108-110).
- **Exclure 143 par empilement.** Cela ne marche pas : 1120 vecteurs ont m = 0, donc le test passe (LATTICE_143.md:97-102).
- **Critère (E) et « Sol 0836 »** (117, 134, 142, 145, 146, 151, 152, 155, 153). Remplacés par l'empilement, le piège dual et
  A.9 (AUDIT_REDUCTION.md:322-331 ; main.tex:578-680).
- **theta_odd24.py comme preuve de N3 = 4096.** Invalide : le script prend N3 en entrée. La valeur vient de l'argument de
  l'ombre ou du recollement exact (REFEREE_143_PROOF.md:129-135 ; theta_odd24.py:9).
- **Contrôler N4 contre une valeur attendue en supposant les autres couches complètes.** Remplacé par le lemme de complétude
  jointe (REFEREE_SHELL_COUNTS.md:55-59).
- **Rejouer les transferts en égalant des totaux ou des histogrammes.** Déclaré insuffisant par Codex, qui demande de
  reproduire la branche prise puis de la certifier (REFEREE_TWIN_DEPENDENCIES.md:135-142).
- **Le mot « excluded » du tracker comme certificat.** C'est une dépendance, pas un certificat
  (REFEREE_TWIN_DEPENDENCIES.md:31-34 ; EDITORIAL_REVIEW_PAPER.md:108).
- **La comparaison entière sur 112 et 114 comme test des transferts.** Elle n'en est pas un : ces réseaux n'ont aucune paire
  transférée (main.tex:887-889 ; REFEREE_TWIN_DEPENDENCIES.md:144-147).
- **Une preuve sans ordinateur du Théorème B** n'est pas connue (main.tex:985). La route n'est pas fermée, mais personne ne l'a
  trouvée.

### Partie A : matériau C1 hébergé dans le dépôt

« Close comme méthode » = la source le dit explicitement « not as a truth ».

| route | pourquoi | source | id |
|---|---|---|---|
| Hermite (vecteurs courts forcés par le déterminant) | demanderait des minorations du minimum jusqu'aux normes ~40 ; déjà close dans notes/110 | H:1191-1197, 1248 | L02_C2_aws-271 |
| Contrainte vectorielle (représentation de Weil) | identiquement satisfaite sur la famille du labo | H:1243-1246 | L02_C2_aws-278 |
| Classification exacte des vecteurs courts du dual M | peu de levier (millions de vecteurs de norme 6 possibles) | H:1246-1248 | L02_C2_aws-279 |
| Arguments locaux (réunion de supports) pour le tassement des graines et autour des jumeaux | trop faibles ; ce qui marche est l'algèbre linéaire globale | H:1327-1336 | L02_C2_aws-291 |
| PL thêta du côté +3 (rang 60) | A₆ − 1220 jusqu'à 2,9e9 au rang 37 | H:1333-1334, 1360 | L02_C2_aws-292 |
| Exclusion spectrale ou par comptage de l'exception de la note 183 | tout est cohérent ; non excluable localement (instance par trois grilles) | H:1288-1291 | L02_C2_aws-286 |
| 22-coclique : arguments spectraux, forme quadratique rationnelle ; test thêta de niveau 21 avec Fricke seul | cohérents / faisable ; la route du réseau Λ demande deux entrées ouvertes | H:1385, 1402, 1411-1412 | L02_C2_aws-299, L02_C2_aws-301, L02_C2_aws-302 |
| Configurations de grilles par un point (3, 4 droites ; droite dans 6 grilles) par partition équitable | toutes passent le test spectral | H:1437-1441 | L02_C2_aws-309 |
| Collisions paire par paire | demande τ ≤ ~860 ; le polytope de recensement contient le monde des grilles pures | H:1471-1473 | L02_C2_aws-314 |
| Plafond par les normes 24 / 26 | équivaut à des planchers sur b₃ ou plafonds sur a₇, a₈ | H:1474 | L02_C2_aws-314 |
| « Au plus κ vecteurs propres par graine » | trois vecteurs de norme 18 par graine localement possibles ; rien aux normes 22, 24 | H:1475-1489 | L02_C2_aws-315 |
| Plafonds sur a₇, a₈ pour le rang 37 ; couches courtes de L1 ; 22-cocliques | même tout à zéro, le point mort reste sous le plafond certifié | H:1549-1552, 1533-1535 | L02_C2_aws-321, L02_C2_aws-324 |
| Plancher de norme 6 par représentants sans prisme | 60 346 seulement au sommet | H:1553 | L02_C2_aws-324 |
| Comptabilité par paires, supports ≤ 9 | point mort ~13 900 < minimum certifié 16 496 | H:1558-1570 | L02_C2_aws-324 |
| Réservoir des plus courts, supports ≤ 9 ; méthode b₄ pour ≤ 9 | égalités ≤ 12 674 par paire contre ≤ 7 447 abordables ; « exhausted » | H:1572-1586 | L02_C2_aws-326 |
| Déterminant / Hermite pour une droite dans g grilles | n'exclut une droite dans six grilles que pour r ≤ 31 | H:1596-1602 | L02_C2_aws-328 |
| Comptage de dimension « relations de pinceaux seulement » | relations en un sommet dans tout graphe ; max τ_g = 1331 | H:1688-1716 | L02_C2_aws-340, L02_C2_aws-341 |
| Méthode polynomiale (Frankl-Wilson) ; disjonction seule | ρ ≤ ~1500 (ou 1330) ; ≤ 11 grilles / 8 paires indépendantes | H:1645, 1670-1672 | L02_C2_aws-333, L02_C2_aws-336 |
| Invariants algébriques d'une droite générique ; borne de comptage uniforme en G ; énergie d'apex | automatiquement satisfaits / équirépartis / réfutée | H:1800-1803, 1841-1850 | L02_C2_aws-351, L02_C2_aws-355, L02_C2_aws-356 |
| Densité / Hermite sur les réseaux locaux L_v, K_v | au seuil (1,2 et 0,7 vecteur attendu) | H:1915-1918 | L02_C2_aws-362 |
| Une étoile pour la droite dans six grilles | une étoile de rang ≤ 5 existe | G:220-223 | L02_C2_aws-379 |
| Conditions réelles seules pour les étoiles | une étoile est trouvée tout de suite | G:187-188 | L02_C2_aws-378 |
| Transformations (mouvements universels, bascules, argument extrémal) | aucun mouvement local (< 9 sommets) ; 243 non modèle ; bascule involutive | M:7-16, 176-188 | L02_C2_aws-382, L02_C2_aws-396 |
| Pilote local sensible au rang (repères de rangs 30 et 40) | les 3655 points restent admissibles | M:166-174 | L02_C2_aws-395 |
| Séries thêta quartiques | faisable 37-43 ; 64 coins faisables, ensemble convexe | M:257-282 | L02_C2_aws-401, L02_C2_aws-402 |
| Programme à neuf classes au degré 0 ; variante cubique ; degré 2 au rang 43 | faisable ; 13 / 19 paramètres absorbent tout ; isotropie non forcée | M:369-391, 487-488 | L02_C2_aws-408, L02_C2_aws-409, L02_C2_aws-414 |
| Pistes arithmétiques dans S₀ (cubique, 441 classes, sommes vectorielles, Jacobi des droites et des sommets, relèvement dans U) | tout compatible ; aucun intervalle changé | M:647-733, 849-873 | L02_C2_aws-427-A165, L02_C2_aws-437, L02_C2_aws-438 |
| Solveurs génériques sur l'étage 1 P3/N25 (CP-SAT, HiGHS), crible levé, boucles de coquille, regard en avant | aucune décision / pas de fermeture | M:893-900, 982-984, 1043-1052, 1069-1070, 1099-1101 | L02_C2_aws-440, L02_C2_aws-445, L02_C2_aws-451, L02_C2_aws-452 |

## 13. Questions ouvertes, classées par levier

### Partie K (campagne de calcul)

**Levier 1 : règle de transfert jumeau (le seul calcul ouvert du papier).**
- Recertifier au plus 2 479 669 paires (11 234 représentants, 5 130 chunks, 102 réseaux) avec `q/twin_recert.py` (classes W, Z, M, C exactes ; paires H par le moteur avec FD_TWIN=0 et FD_SWAP=0) ; test sur 043 : 23 paires H sur 33 311. Garé par l'utilisateur (L02_C2_aws-030).

**Levier 2 : complétude de l'énumération des paires.**
- Comparaison F4 faite sur 140, 135, 141, 064 seulement (L02_C2_aws-019) ; le lanceur `q/qf4.py` et `q/ypairs_c2.py` (parallélisé : YP_WORKERS, YP_PART) existent pour d'autres réseaux.

**Levier 3 : certificats de recherche.**
- 25 775 627 paires exclues par une recherche de repère sans certificat (L02_C2_aws-038) : un second moteur indépendant ou des certificats de recherche changeraient leur statut.

**Levier 4 : archivage et provenance.**
- 28 réseaux S sans aucun enregistrement sur branche (L02_C2_aws-040) ; environ 780 représentants tier L sur enregistrements du PC (L02_C2_aws-039) ; 000, 004, 010 en lecture unique ; 044 en un seul passage.

**Levier 5 : reproductibilité de plateforme.**
- Écart de calibration sur aarch64 jamais expliqué ; nombres de noeuds dépendant du CPU (L02_C2_aws-037).

**Levier 6 : contrôles déclarés manquants par Codex.**
- Minimum E >= 11 des 2 652 survivantes non revérifié ; 1 610 témoins caractéristiques non rejoués ; certificats z à archiver (L02_C2_aws-027, L02_C2_aws-029).

### Partie B : T16, T18 et le pont

1. **Lemme suivant (gain direct sur la recherche de cadre).** T22 (E = 11, vecteurs de norme 3 avec {|a|,|b|} = {1,3}) :
   « none is claimed » (`lemma/PROOF_C2/A3_LEMMAS.md:72-74`) ; les paires d'énergie >= 11 restent nombreuses (L02_C2_aws-167).
2. **Preuve sans énumération.** Profil (2,5,0) à la main (« t = 2 is the most rigid case ... a hand treatment looks possible but
   long ») ; montrer que le Gram impair de T u X_2 u W n'est jamais singulier ; convertir P3 à l'étape B en contradiction ;
   écrire des preuves de P6-P8 (`t18_STRUCT/REPORT.md:89-107`).
3. **Vérification des calculs.** Programmes non audités ligne à ligne ; correspondance sorties / scripts en place non vérifiée ;
   scripts patchés (`_patch_*.py`) ; certificats PSD seulement échantillonnés (50 000 sur environ 1,6 million pour B1, 12 000 pour
   B2 ; ceux de B0 non revérifiés) ; 2 667 représentants stockés de B0 non comparés ; texte v2 de T18 non arbitré
   (`T18_PROOF.md:1699-1788`, `1906`). Corollaire Y1 non relu par l'arbitre du pont.
4. **Formalisation et lecture humaine.** Aucune (« no human reader has gone through them and nothing is formalised » ;
   plan : énoncer les lemmes comme hypothèses nommées du théorème final, `A3_LEMMAS.md:76-78`).
5. **Campagne.** H4 par paire (certificats `q/cert_stream.py`, non relus ici) ; dépendance de Y1 et des paires T20 à T20, dont le
   texte a changé après l'acceptation (blob accepté e50d5be0, master 77a4dea9 ; hors partie B).
6. **Route témoin de la note 54.** Coupes k = 1, 2, 3 ouvertes (L02_C2_aws-126) ; inutiles pour la route (C).
7. **Accélération (historique).** Utiliser P2 dans les énumérateurs (cinquième paire de W déterminée par b^T G^{-1} b = 4)
   (`t18_STRUCT/REPORT.md:101-102`).

### Partie C : T20 et les calculs des branches lemma-run

**Levier « certification et indépendance »**
1. G1 résiduel : fichiers par base des trois cas portables de n_3 = 0 et plans/journaux/certificats de III.1 hors git ; versions établies
   par marqueurs et heures, pas par hachage (`master:lemma/T20_PROOF.md:2729-2731`, `master:lemma/ARTIFACTS_T18_T20.md:83-89`).
2. G2 : formulation finale du contrat non relue par l'arbitre (`master:lemma/T20_PROOF.md:7-10`) ; conditions 2 et 3 lues dans le code,
   non testées par contrôle (`:1106-1107`). C3 « still to merge » (`:25`).
3. Programmes non audités ligne à ligne ; moteurs générés et patchés, lien exact entre versions et sorties non vérifié
   (`master:lemma/T20_PROOF.md:2704-2711`, `:2737-2739`).
4. Les deux programmes de la route B sont de la même session (LAP) et partagent le modèle ; Codex n'a pas fait de troisième run
   (`master:lemma/T20_BOARD.md:17`).
5. Aucun lecteur humain ; pas de formalisation (`master:lemma/FINAL_STATEMENT_DRAFT.md:6`, `:114`).
6. Écart de comptes de nœuds I.0 (4,2,1) / I.5 (4,2,1) entre texte et branches citées : à expliquer (vu par moi, L02_C2_aws-218).

**Levier « preuves à la main »**
7. n_3 = 2 par la main (nouvelle identité globale ; L02_C2_aws-263).
8. IIa par la main (L02_C2_aws-255).
9. Exclure un profil entier en combinant la Prop. 2 de Codex et les comptes d'unités (L02_C2_aws-264), conditionnel à (E14).
10. (E14) n'est pas prouvé dans le texte ; il ne sert qu'à la règle de norme duale (L02_C2_aws-236) et aux propositions de Codex (L02_C2_aws-237).

**Levier « réutilisation »**
11. Transposer le cadre de recherche (ensembles déterminés, unités, budgets, deux projecteurs, rang, contrat) à d'autres normes ou
    automorphismes (voir Matériaux (4)).

### Partie D : réduction, audits, papier

1. **Seul point de calcul ouvert du papier** (L02_C2_aws-092) : recertifier au plus 2 479 669 paires, closes par la forme « statut »
   (1 025 447) ou « même réseau » (1 454 222), soit 11 234 représentants et 5 130 morceaux.
   - Conditions : sans statut enregistré ni rang flottant. Il faut les racines exactes du jumeau, puis soit plus de racines,
     soit une descente stricte de clé, soit une recherche sans la règle.
   - Outil exact disponible : `q/codex_exact_twin_type.py` ; ses contrôles passent, mais les flux historiques ne sont pas
     vérifiés (L02_C2_aws-093).
   - Coût selon LAB : au moins ~100 cœur-heures, probablement plusieurs centaines (main.tex:894-897).
   - Plan le moins cher selon Codex : recompter d'abord exactement les nombres de racines (REFEREE_TWIN_DEPENDENCIES.md:125-133).
   - Annexe : la forme (b) (32 265 417 paires) utilise le compte de racines du programme, sans recomptage exact
     (main.tex:884-885). Une borne inférieure certifiée suffirait (REFEREE_TWIN_DEPENDENCIES.md:20-26).
2. **Complétude de l'énumération des paires** pour les 152 réseaux non comparés, et réduction par automorphismes de diagramme
   (main.tex:899-903). Le papier la nomme « its main reservation » après l'absence d'expert humain.
3. **Programme de recherche.** Il n'y a pas de second programme indépendant ni de certificats de recherche pour les environ
   2,6·10^7 paires exclues par recherche (main.tex:910-933).
4. **Preuves de provenance à compléter :**
   - les certificats z des 1 610 témoins caractéristiques (REFEREE_TWIN_DEPENDENCIES.md:176-180) ;
   - la sortie durable du recensement H1 (AUDIT_ENGINE_RULES.md:144-145) ;
   - les enregistrements de 000, 004, 010, non reproduits (main.tex:928-929) ;
   - au plus 946 y1 sur version labo retrouvée, sans Y1 et non relancés (dérivé par moi, L02_C2_aws-089) ;
   - 044, qui n'a tourné que sur une machine ;
   - les 86 certificats PL de 000, non relancés ;
   - les autres enregistrements « pair budget » : H4 n'est pas global selon Codex (AUDIT_ENGINE_RULES.md:349-351) ;
   - pour H3, les décisions numériques de rang et de type dans les transferts et les listes d'ombre
     (AUDIT_ENGINE_RULES.md:316-318).
5. **Validation globale :**
   - une passe de relecture unique sur le texte gelé, avec manifeste (TODO 6 de main.tex:22-23 ; MAIN.md:58) ;
   - un lecteur humain ;
   - une formalisation Lean, avec hypothèses nommées et vérificateurs de certificats (L02_C2_aws-108).
6. **Bibliographie :**
   - BL11 et la thèse de Behbahani ne sont pas ouverts ; [Mak] est cité via le résumé de [CW] ; l'argument LM14 n'est pas
     vérifié ;
   - la Table 17.1 de Borcherds n'a pas été comparée ;
   - il manque la section de la formule d'oddité dans SPLAG ;
   - le contrôle de masse des 156 n'est pas fait (AUDIT_REDUCTION.md:302-303).
7. **Mathématique hors calcul :**
   - prolonger la borne des fonctions propres au-delà de la norme au carré 22 (« every further step of this kind would shorten
     the searches », main.tex:987-988) ;
   - une preuve sans ordinateur du Théorème B.

### Partie A : matériau C1 hébergé dans le dépôt

**Levier 1 — rang 37 par le comptage (b₄ contre collisions).**
- L'énoncé manquant : minorer le 7-rang du système des classes de différences de jumeaux et d'indicatrices de grilles (dimension 18) en fonction du nombre de paires jumelles, jusqu'à < ~540 paires (L02_C2_aws-335 ; H:1655-1660). Formes équivalentes : « aucune droite dans 4 ou 6 grilles » (τ_grid ≤ 693, H:1594-1595) ; τ_g < 614 sans paire non grille, ou ρ ≤ ~58 (L02_C2_aws-338).
- Constantes de collision : supports 9 et 10 (H:1504-1505) ; réservoir au support 10 (non calculé) ; recensement d'ordre 11 (non lancé ; décision de l'utilisateur) (L02_C2_aws-327) ; masses 7 à 9 à P = 0 (L02_C2_aws-380).
- Codex « pas encore » : grilles hors des trois points, droites dans quatre grilles, borne globale sur ρ, τ, paires non grilles (L02_C2_aws-339 ; H:1686-1687) ; autres solutions de colonnes (H:1630-1631) ; les manques de 1 à 3 du modèle canonique (couplages, hexagones, deux triangles) sont-ils de vraies relations ? (H:1701-1703).

**Levier 2 — rang 37 par les droites et les étoiles (cas d'égalité).**
- (a′) pas de droite générique à k = 22 ; NT ; « toute droite déconnectée » contre les 18 dimensions (L02_C2_aws-342) ; raison uniforme de la mort de l'étoile (H:1746-1747, 1854-1856).
- Énoncé B : 12 670 + 147 boules et 17 tests de rang manquants (L02_C2_aws-377) ; profil (2,2,2) avec triangles (3 passages sur 641) ; test à deux étoiles fastr2.c jamais validé, pour la droite dans six grilles (L02_C2_aws-379).
- Droites connexes sans prisme : ~1e10 à 2e11 boules, réduction d'un facteur ~1e4 nécessaire (L02_C2_aws-381) ; droites touchant des prismes : non touchées (H:2019).
- Proposition C : droites non génériques ; paires de rangs r + r′ ≥ 80 (L02_C2_aws-392) ; (39,39) de Codex non relu (L02_C2_aws-391) ; symétrie forcée ou données inexistantes au rang 37 générique (M:197-200).

**Levier 3 — rang 43, scénario S₀ et P3/N25.**
- 3271 supports P3/N25 ouverts (L02_C2_aws-453) ; preuve finie au niveau de la coquille (M:1064-1065) ; parcours de toutes les étoiles doubles (M:1081).
- Borne uniforme 2288 sur les configurations (1⁷ ; (−1)²⁹) à support positif indépendant : fermerait tout S₀ (L02_C2_aws-421) ; majoration du nombre des quatre profils (M:536).
- Géométrie des 538 vecteurs de norme 4 non triangulaires de M et des 329 vecteurs de norme 26 par classe (M:452-453) ; classification des vecteurs de O de norme ≤ 12 dans les classes 1 à 4 (M:390).
- Rang 43 hors S₀ : aucun objet bas forcé seul (L02_C2_aws-426).

**Levier 4 — objets transverses (tous rangs).**
- Existence d'une 22-coclique (si aucune : a₇ = 0 à tout rang) (L02_C2_aws-299) ; 3-rang du plan 2-(22,4,2) ≥ 19 et vecteurs courts de Λ (L02_C2_aws-302) ; duaux partiels, d ≥ 2 (L02_C2_aws-301).
- Classification de la norme 4 de M dans les classes ±1 (trois −1 en position générale, motif (2,−1,−1)) ; classe 0 en norme 28 (L02_C2_aws-273).
- Lemme A (norme 18 par graine) : sous-cas ouverts (L02_C2_aws-282) ; comptage mécanisé par graine en norme 18 (L02_C2_aws-279).
- Classification du 12-ensemble U de l'exception de la note 183 (L02_C2_aws-286).
- Structure réciproque du cas norme 14 (2-(15,3,2)), en audit chez Codex (L02_C2_aws-270).

**Levier 5 — transfert entre rangs.**
- Toute exclusion du rang 43 n'utilisant que le genre, les vecteurs de M et les vecteurs courts de L1 exclut aussi 37, 39, 41 (L02_C2_aws-310) : à confronter aux outils du rang 43 du Mandat C (voir Matériaux (4)).

## 14. Contradictions, redécouvertes, résultats remplacés ou retirés

### Partie K (campagne de calcul)

**Remplacés ou retirés**
- Total des paires du balayage stream : 212 825 691 (brouillon de 12:50 UTC et brouillon 6 de 15:47 UTC, `origin/defer-n4:lemma/FINAL_STATEMENT_DRAFT.md:55`, `origin/tmp/push-test-laptop:lemma/FINAL_STATEMENT_DRAFT.md:71`) remplacé par 220 260 576 (brouillon 7, `master:lemma/FINAL_STATEMENT_DRAFT.md:71`) : « came from a count that I cannot reproduce » (L02_C2_aws-024).
- Brouillon de 12:50 UTC : énoncé A (involution à un point fixe) + énoncé B (avec F0), « R2 ... SOURCE-ONLY. This is the one external assumption », 143 « SOURCE-ONLY » (`origin/defer-n4:lemma/FINAL_STATEMENT_DRAFT.md:12-27,63`) ; remplacés au brouillon 7 par un énoncé unique, A.0 prouvé à la main, Théorème R relu, 143 par preuve à la main (`master:lemma/FINAL_STATEMENT_DRAFT.md:10-31,62-66`).
- Manifeste RERUN_713 de LAP (`measures/RERUN_713_MANIFEST_2026-10-07.json`) : SUPERSEDED (deux défauts trouvés par le labo) (`master:HANDOFF_2026-10-01.md:1047-1049`).
- Phrase « les 732 paires sans témoin ... exclues par la recherche v10 » : fausse telle quelle, corrigée à 20:05 UTC (L02_C2_aws-029).
- « Wrapper L indisponible » (message 83) retiré au message 85 : retrouvé (L02_C2_aws-033).
- Attribution des 60 308 paires jumelles du lot 713 au seul raccourci de statut : corrigée en 59 697 + 428 + 183 (L02_C2_aws-026).
- Premier vérificateur des témoins : acceptait des tableaux flottants (témoin hors réseau accepté) ; corrigé, 4 contrôles négatifs (L02_C2_aws-027).

**Écarts entre notes (pas de désaccord de fond, mais à lire avec soin)**
- Le brouillon 7 (17:50 UTC) et le HANDOFF section 19 disent que l'utilisateur a décidé de ne pas refaire les réseaux locaux (`master:lemma/FINAL_STATEMENT_DRAFT.md:100,113` ; `master:HANDOFF_2026-10-01.md:981`) ; le soir même, B_LATTICES et le HANDOFF section 20 documentent leur reprise (713 représentants, 28 réseaux) : le brouillon 7 n'a pas été mis à jour.
- B_TABLE_156 (généré à 20:30 UTC) garde « lab PC » comme lieu des enregistrements des 29 réseaux H/F/H3 et de 004/010, alors que des enregistrements v10 (reprise) ou v4 (Golay) existent sur les branches run/* (recompte L02).
- « 55 réseaux hors moteur de paquet » (provenance du moteur, B_LATTICES B.3), « 58 réseaux en partie au seul PC » (lieu, brouillon 7 section 4) et « 28 réseaux sans enregistrement sur branche » (recompte L02) : trois notions différentes.
- 288 / 464 / 331 paires canoniques (F4) contre 576 / 928 / 637 lignes de flux (reprises v10) pour 140 / 135 / 141 : objets différents.
- Le blob T20 accepté par l'utilisateur (e50d5be0) n'est pas la version finale de master (77a4dea9) (L02_C2_aws-031 ; aussi signalé par les parties B et C).
- Totaux T18 de 001 : 4 540 au relevé de 02:57 UTC (balayage inachevé, 757 paires non couvertes) contre 4 545 au certificat final : instantanés différents (`master:measures/SWEEP_STATE_2026-10-07.txt` ; `master:measures/cert_golay_001.json`).

**Redécouvertes**
- Le corollaire Y1, trouvé par Codex pour 003:181 (~15:00 UTC), a été réappliqué deux fois le même soir (55 réseaux S, puis 28 réseaux) : même lemme, trois usages, pas une redécouverte.
- Le défaut H2 (noyau rigide) n'est signalé nulle part avant l'audit de Codex du 07/10 dans les notes lues.

### Partie B : T16, T18 et le pont

**Réfutés ou retirés**
- « The violated matrix is 9(3I-A)+J » (rapport T18 round 2, 06/10, `T18_REPORT.md:220`) : faux ; dix configurations de B1 ne
  meurent que par M2 (VERIF331 et arbitre 1, 06-07/10) (L02_C2_aws-142, L02_C2_aws-143).
- Vérificateur reçu du dossier T16 : check_B ne teste pas W <= set(V) (Codex, 07/10) ; aucune obstruction perdue (L02_C2_aws-121).
- Pont v1 : « the engine would answer INVALID for such a pair » (faux, L02_C2_aws-162) ; « The converse is false in general » (non
  établi, L02_C2_aws-163) ; Lemme 3 énoncé sans (G) ; H5 présentée comme hypothèse « garantie » (`bridge_REFEREE/REPORT.md:10-45`).
- T18_PROOF v1 : « two complete exact implementations » de l'étape C pour B0 (L02_C2_aws-175) ; « cell room alone gives 1834/4096/1265 »
  (L02_C2_aws-173) ; survivant défini par « no violation is found » (dépendant du programme), redéfini en v2 (`t18_REFEREE2/REPORT.md:15-18`).
- `b0_x0.py` première version : diagonales 27/44 au lieu de 28/42, sorties écartées (L02_C2_aws-153).
- Index T16 : « Equivalently » remplacé par « Consequently » (`REFEREE_T16_PROOF.md:33-40`).

**Remplacés par des états ultérieurs (pas de désaccord de fond)**
- Round 3 : les 4 survivants de B1 « a genuine open case » (PSD, rang 46 sur 47) -> rang 46 impossible (STRUCT §0, 06/10 23:08).
- `LEMMA_TARGET` §8 (06/10 23:45) : « B0 open », « B1 stage-C list has one implementation » -> §11 (07/10 01:45) : CMINE
  complet. Même remplacement pour `T18_REPORT.md` (B1 : 2 891 triples à une seule implémentation) et `t18_B0/REPORT.md`
  (étape C : une implémentation).
- `T18_REPORT.md` A11/A12 « computed, one implementation » -> deuxième implémentation I2 (VERIF331).
- Rapports de travail : « 846 » à l'étape D (avec la borne haute de (D3)) contre 849 (arbitre 1, sans) ; « type solutions »
  11 235 / 4 227 sans (C6) contre 770 / 514 avec (L02_C2_aws-174) ; « completions C » 23 155 / 93 684 / 44 (I1) contre 11 797 / 45 362 / 88
  (I2, REF1) : objets différents (`T18_PROOF.md:1232-1239`).
- Nombre de fichiers ENUM pour B1 : 14 (`04_b1_coverage.out`), 17 (`r3_finalB.out`), 15 (`13_B1_survivors_compare.out`) :
  expliqué (copies identiques et essai précoce), sans effet (`T18_PROOF.md`, notes de A.5).
- « sample of 29 triples » (B0) -> « run of part 0 of 150 cut by its time limit after 29 triples ».
- « 0 configurations on 55 vertices left » (sorties de l'étape D) : aucun ensemble de 55 sommets n'est déterminé (L02_C2_aws-149).
- LEMMA_TARGET §2 : remarque « for a root r every |(u,r)| <= 1 ... already remove the pairs » incomplète pour un h (L02_C2_aws-156).
- `T18_PROOF.md` §1.4 et §9.3 item 11 laissent le dictionnaire « not verified at all » (v2 de 04:23) ; le pont (04:27) le prouve.
- VERIF331 : test (i') « could not be identified » ; T18_PROOF : (i') est automatique.
- STRUCT §3 titre « Hand lemmas ... (proved) » mais P6-P8 sans preuve écrite selon les arbitres (L02_C2_aws-138).
- Formulation globale « every computation re-done by at least three programs, one of them written from the text alone »
  (`A3_LEMMAS.md:51-52`, `HANDOFF_2026-10-01.md:910-911`, `lemma/ARTIFACTS_T18_T20.md:13`) : `T18_PROOF.md` §9.2-9.3 est plus
  fin (REF1 n'est qu'un contrôle de comptes flottant ; ligne 4a : I2 + arbitres ; étape C de B0 : CMINE + REF2 complets, ENUM
  modulo stabilisateurs). Cohérent si l'on compte ainsi ; je le signale comme arrondi, pas comme contradiction.
- `t18_B2/REPORT.md` : « 15048 saved PSD certificates re-checked » contre `T18_PROOF.md` « 12000 for B2 » : cohérent
  (12 000 + 3 048 de l'étape D, `lemma/t18_B2/b2_certs_check.out:1-4`).
- T20 : un texte de tâche disait 32 / 36 / 40 au lieu de 16 / 18 / 20 (facteur 2), relevé dans `BRIDGE.md:345-347` (hors partie B).

**Redécouvertes signalées par les sources**
- t <= 1 et les identités §2-3 du support 16 : anciens (Wave 81), redonnés à la main dans la note cube (L02_C2_aws-117, L02_C2_aws-119).
- Inégalité A9 : redérivée par VERIF331 sous la forme 2h_3 + 4h_0 + n_3 <= 4 (L02_C2_aws-134).
- Borne de rang : trouvée par STRUCT (« coordinator's argument ») et redérivée par les agents B1, B0, B2 (L02_C2_aws-136).
- Proposition 3.1 pour la norme 18 : écrite par l'arbitre 1 (la réduction existait pour la norme 20 dans `T20_REPORT`) (L02_C2_aws-128).
- Dictionnaire : reconstruit par LAP le 06/10, confirmé par le pont d'après les dossiers du 04/10 (L02_C2_aws-156).

**Noms qui se recouvrent**
- Le même lemme s'appelle T16, « H16 », « lemme du 04/10 », « 9/7 lemma ».
- Dans les sources du pont, « C1 » désigne un dossier de code et des notes du paquet (`SP\pkgfull\c1\code\y_pairs.py`,
  « C1 notes 139-145 », `BRIDGE.md:42-49`) ; je n'ai pas établi le lien avec le cas C1 (groupe trivial) du brief.

### Partie C : T20 et les calculs des branches lemma-run

**Contradictions et passages périmés (master)**
- `T20_PROOF.md:37` « This text does not prove T20 » et `:168` « It is not proved here » contre le Théorème 10.2 (`:2579-2583`) et le titre
  (`:27`) ; restes de la version 8510844a4 (`origin/defer-n4:lemma/T20_PROOF.md:23`).
- `T20_PROOF.md:69-70` « The section has not yet been refereed » contre le bandeau (`:4-6`, passage d'arbitrage du 07/10).
- Table de 10.2 (`T20_PROOF.md:2602-2613`) : « **1** (eng5.py) ... verifier running », « **1** for the nine/ten other cases », sans note
  du soir ; le bandeau (`:15-16`) liste les sections annotées sans 10.2. Codex avait demandé de mettre à jour ou d'étiqueter ces blocs
  (`REFEREE_PAPER_c1bcba6bb.md:112-118`).
- Board : ligne B (`T20_BOARD.md:27`, « closed by the first program ... I.0 (4,2,1), I.5 (4,2,1) by two programs ») contre C2, C3
  (`:35-36`, douze cas sur douze).
- Bandeau « Not yet re-read by the referee » (`T20_PROOF.md:10`) : l'arbitre a lu le paragraphe G2 à 66c12bd73 et demandé une correction
  (`REFEREE_PAPER_c1bcba6bb.md:120-134`), fusionnée dans 474aa859a ; c'est cette dernière version qui n'est pas relue.
- Comptes de nœuds de I.0 (4,2,1) et I.5 (4,2,1) : 33,511 / 27,524 (texte, `T20_PROOF.md:2072`, `:2082`, runs portables) contre 51,241 /
  48,823 (`t20_Iv_I:ALL.txt:8`, `t20_Iv_J:ALL.txt:8`) que `ARTIFACTS_T18_T20.md:50-51` cite comme sorties de ces cas. Non signalé
  (vu par moi) ; aucune incidence sur l'exclusion (0 complète dans les deux).
- H6 cite les valeurs interdites 3, 5, 6 (`NOTES.md:197-202`) ; le Lemme 10.2 donne 3, 5, 6, 7 (`T20_PROOF.md:2677-2679`) ; même conclusion
  ((E14) suffit).
- Lignes du contrat dans `in_verify.py` : 670 et 743 selon le relecteur LAB à 12:45 UTC (`REFEREE_T20_PROOF.md:114-122`), 971 et 1044
  dans T20_PROOF (`:1086`) : versions différentes du fichier (v1/v2 contre v3).
- `FINAL_STATEMENT_DRAFT.md:104` (17:50 UTC) : ARTIFACTS « not reviewed; program versions inferred from launch times » ; plus tard Codex a
  relu une ligne et ARTIFACTS a remplacé l'inférence par des marqueurs (`ARTIFACTS_T18_T20.md:54-78`).
- Énoncés acceptés contre énoncés courants : le registre accepte le blob e50d5be079 (`CHECKPOINT_156.md:22-26`), master est 77a4dea999.
- Divergences relevées par le texte lui-même (`T20_PROOF.md:2782-2812`) : III.1 « open » (round 2) contre complété ; plafonds de stade 2
  « C4 et C5 » (rapport) contre 8 - h_0 dans le code ; borne a_2 de SPEC_N3/H9 contre a_0 <= 4 ; I.0 (4,2,1) 1,784,786 (round 2) contre
  178,768 (round 3), objets différents ; « two independent programs » (round 1) contre absence de test d'isomorphisme ; « two programs »
  pour III.0 (board) contre « two implementations, one shared model file » (round 2) ; norme 40 du texte de tâche contre norme 20.
- Board defer-n4 D3 : « CDX authors the second checker and therefore is not a code-blind referee » (`origin/defer-n4:lemma/T20_BOARD.md:45`),
  phrase disparue du board ensuite ; Codex le dit lui-même (`REFEREE_T20_PROOF.md:27-30`).

**Redécouvertes (même résultat établi deux fois)**
- Les 25 types de z : x3_types.py (LAB, H2), ztypes.py (LAP), referee_route_b_checks.py (Codex), même jour (L02_C2_aws-227).
- (Q0) = 44 : H4 (LAB) et C8 (round 3) (L02_C2_aws-207).
- beta = 1 : lemme à la main de Codex, déjà observé par les tests de bases (8,557 sur 8,557 ; aucune base beta = 0) (L02_C2_aws-222).
- Lemme d'isolation : les 66 bases violantes déjà traitées avaient été fermées par la recherche (L02_C2_aws-242).
- Comptes de bases de la route A : n3_cases.py (LAB), dual_n3.py et n3_second (Codex) (L02_C2_aws-231).
- Premier programme relancé sur sept cas (t20_I_rest puis t20_I1_340 et t20_Iv_B..E) : mêmes comptes ; I.0 (4,2,1) et I.5 (4,2,1) vérifiés
  deux fois par deux programmes avec des arbres différents (L02_C2_aws-218).

**Retirés ou remplacés (X)** : L02_C2_aws-216 (runs A, F), L02_C2_aws-235 (moyenne 3,7 min), L02_C2_aws-245 (E1, E2), L02_C2_aws-248 (bloc raw Z), L02_C2_aws-249
(« node by node », « keep the same ones »), L02_C2_aws-251 (étiquette v1), L02_C2_aws-257, L02_C2_aws-258 (énoncés du round 1 remplacés), L02_C2_aws-260
(premières versions de iii_enum.py et t20_verify.py). Plus : la première version de T20_PROOF (9.B en attente, `origin/defer-n4`) ;
le vérificateur v1 sur I.1 (4,2,1) (AssertionError, non compté, L02_C2_aws-215) ; « III.1 open » du round 2.

**Versions sur d'autres branches**
- `origin/defer-n4` (pointe d5c223d2e, 12:44 UTC) et `origin/tmp/push-test-laptop` (pointe b4c3f3036, 16:15 UTC) sont des ancêtres de master :
  états antérieurs, pas des divergences. T20_PROOF.md : defer-n4 = 8510844a4 (9.B « PLACEHOLDER », pas de Théorème 10.2) ; tmp/push-test-laptop
  = a730e7b5e (blob e50d5be079, celui accepté par l'utilisateur ; sans contrat G2, avec l'ancienne phrase « node by node » en 10.4 item 3).
- T20_BOARD.md : defer-n4 = état de 12:45 UTC environ (A2-A4 en attente, C2 en cours, D3 « queued ») ; tmp/push-test-laptop = identique à
  master hors section « Machines running » (état 14:30 UTC).
- ARTIFACTS_T18_T20.md : tmp/push-test-laptop = version de 15:26 UTC (ligne I.1 (3,4,0) en v1 et ALL.txt, sans le paragraphe de preuve
  des versions) ; absent de defer-n4. T20_WORK.md : identique sur les trois branches.

### Partie D : réduction, audits, papier

**Contradictions et écarts entre notes**

- **MAIN.md:43-44 (20:54)** dit des cinq conditions qu'elles sont « each discharged ». Or AUDIT_ENGINE_RULES.md:243-245,
  316-318 et 349-351 limitent H2 aux archives et H3 aux listes locales, et ferment H4 pour 143 seulement, avec « not a global
  H4 closure ». Le papier final dit « Each was investigated » (main.tex:914), après la critique de EDITORIAL:45. MAIN.md n'a pas
  été mis à jour.
- **H4.** FINAL_STATEMENT_DRAFT.md:51 : « concerned one lattice, 105 (6,310 pairs) ... Closed 14:45 ». AUDIT_ENGINE_RULES.md:332-335
  rapporte 12 620 paires « pair budget » dans les fichiers labo (message 52) et « H4 remains open ». La réexécution de 105 n'est
  pas consignée par Codex. Le lien 12 620 = 2 × 6 310 n'est pas expliqué.
- **Total des paires des 91 réseaux.** AUDIT_REDUCTION.md:316 (vers 15:18) donne « 212,825,691 pairs, complete ». Le recomptage
  final donne 220 260 576 paires, dont 212 804 047 sur moteurs de paquet et 7 456 529 sur versions labo (B_LATTICES.md:58, 73,
  83 ; main.tex:801). L'écart n'est pas expliqué dans mes sources.
- **Nombre de réseaux exposés à H2.** AUDIT_REDUCTION.md:32 donne 24. AUDIT_ENGINE_RULES.md:175-179 en trouve 25 (27 ids moins
  117 et 152, avec le message 56 : 001 omis). FINAL_STATEMENT_DRAFT.md:49 dit « 27 lattices, 25 of them treated by the engine ».
- **Accès au dépôt.** MAIN.md:47-48 dit des programmes « public there ». TODO 1 de main.tex:7-8 et le résumé (main.tex:73-74)
  disent que les dépôts sont privés depuis le 07/10.
- **Portée du théorème.** Le Théorème 1.1 et le Cor. 1.2 sont énoncés sans condition. Le résumé et la §9 gardent la
  recertification ouverte ; EDITORIAL:41-42 demande de porter cette condition dès l'ouverture. asymmetric.tex rend l'asymétrie
  conditionnelle.
- **Notes périmées :**
  - TODO de asymmetric.tex:8-9 : MM a été lu par Codex et CW lu directement depuis (REFEREE_PAPER:157-158 ; main.tex:12-16) ;
  - tableau G de AUDIT_REDUCTION.md:346-349 : B y est encore « open » ;
  - MAIN.md:55-56 : 044 « in progress » ;
  - TODO 5 (G2 de T20), peut-être périmé : le commit bbdeea453 dit « reserve G2 merged ».
- **Mineur, vu par moi :**
  - le TODO 6 de main.tex cite « Lemma 6.2 » et « Lemma 6.6 (twins) », alors que la numérotation actuelle donne 6.3 pour la
    génération et 6.8 pour les jumeaux ;
  - l'identité thêta est citée [CS90 §2] en main.tex:549-550 mais [SPLAG] en main.tex:961-962.

**Remplacés ou retirés**

- Le squelette du 01/10 (93/62/1) est remplacé par le tracker 156/156 et la section A (L02_C2_aws-106).
- Upstream README:16-17 (Partie I « source only, not reread ») est remplacé par la section A prouvée et relue.
- AUDIT_REDUCTION.md:251 (F4 « NOT DONE (OPEN) ») est remplacé par la comparaison F4 sur 4 réseaux (L02_C2_aws-080).
- La décision « ne pas relancer les réseaux labo » (AUDIT_REDUCTION.md:309, 330-331 ; FINAL_STATEMENT_DRAFT.md:100, 113) a été
  revue le soir même : 29 réseaux et 713 y1 ont été relancés (main.tex:815-831, 921-927).
- LATTICE_143 citait theta_odd24.py pour la complétude de N3. C'est corrigé : la complétude vient du recollement exact
  (LATTICE_143.md:75-77).
- La phrase de LAB « 732 paires exclues par la recherche v10 » est « wrong as worded ». Le détail : 586 par la règle
  caractéristique, 108 par recherche, 38 par transfert (B_LATTICES.md:190-197 ; commit acf843312).
- Le message 107 attribuait les 60 308 transferts au seul statut. Le détail exact est 59 697 + 428 + 183 (L02_C2_aws-094).
- L'exclusion de l'ordre 7 sans ordinateur était attribuée à CW. C'est corrigé (commit e22cfc57f).
- Pour la ligne T20 I.1/(3,4,0) de ARTIFACTS, le chemin et la version étaient faux : le run était v2 et non v1 (L02_C2_aws-109).
- Six corrections ont été faites sur c1bcba6bb (L02_C2_aws-109).
- Les anciennes méthodes niveau réseau sont remplacées (L02_C2_aws-107).
- Le recalcul flottant du 04/10 est remplacé par le recalcul exact (L02_C2_aws-079, puis L02_C2_aws-078).

**Redécouvertes (même résultat établi deux fois)**

- F0 : MM04 Théorème 1 (2004), puis A.0 (07/10). Même dispositif d'intégralité d'un caractère, sur l'espace propre
  complémentaire.
- min N* ≥ 8/7 : dossier Astra AUDIT_NORME1 (avant 01/10), refait par LAP (07/10).
- g pair et g ≠ 22 : note S27 de structures-lab (section 1), refaite dans A.4.
- 153 : « Sol 0836 » D ≥ 12, puis A.9 (07/10). 152 : empilement, A.9 et « Sol 0836 » E8.
- 143 : budget de composantes avec les h (28/09), puis preuve à la main avec les u seuls (07/10).
- Empilement des 18 réseaux : C1 (27-28/09), puis Codex en exact (07/10) ; le test (a) a aussi été calculé une troisième fois
  par LAB.
- Identification des 156 : LAB (04/10, en flottant), puis Codex (07/10, en exact).
- N4 = 98256 − 24N2 : SHELL §1.1 (« 49128−12r » lignes), puis theta_odd24 et l'arbitre (07/10).
- Golay 001 : deux implémentations concordantes.

### Partie A : matériau C1 hébergé dans le dépôt

**Retraits (X) et réfutations (R).**
| quoi | qui, quand | remplacé par / raison | source |
|---|---|---|---|
| Marge de 5,7 M au coin prismes jumeaux | LAB, 08/10 10:06 | corrigée à 10:58 : 9,62 M / 12,62 M SOUS les plafonds | H:1376-1379, 1427-1428 (L02_C2_aws-298 → L02_C2_aws-306) |
| Conjecture « Λ ne peut pas avoir des milliers de vecteurs de norme 4 » | LAB, 08/10 10:38 | retirée (taille générique) | H:1406-1407 (L02_C2_aws-303) |
| Cible « au plus 10 relations » / « pas de relation au-delà des pinceaux » | LAP 16:20 → retirée 17:17 (08/10) | relations en un sommet dans tout graphe (labo 17.51, Codex 206) | H:1688-1716 ; commit 7197f8554 (L02_C2_aws-340 → L02_C2_aws-341) |
| Remarque « classe carrée de τ(G(T)) » | LAP, 08/10 19:34 | retirée avant envoi : c'est « τ non carré » de septembre | H:1771-1773 (L02_C2_aws-347) |
| « S₀ exclu » | Codex, 09/10 ~17:0x | retiré : hypothèse fausse sur les triangles des arêtes P-N, N-N ; 5345 supports ouverts | M:607-610 (L02_C2_aws-422) |
| Infaisabilités « marge −1 » du solveur flottant (quartique, troncatures ≥ 18) | LAP, 09/10 12:59 | artefacts d'arrondi (coefficients jusqu'à 7²¹) ; en exact : faisable | M:271-273 (L02_C2_aws-401) |
| « L'histogramme complet des coordonnées est déterminé par les effectifs » | LAP, 09/10 18:40 | corrigé à 18:46 : en classe 4 un nombre libre par couche | commit 7c177c4c9 ; M:849-859 (L02_C2_aws-437) |
| Profils de la norme 26 fractionnaire « avec −2 » (tableau du §13) | LAP | corrigé au §15.4 : profil unique (1² ; (−1)³⁵) | M:838-840 (L02_C2_aws-436) |
| Total de nœuds du profil (3,3) « about 5.4e9 » | LAP, 09/10 03:52 | 6,57e9, compté depuis les six journaux | commit fa0acfa56 ; G:190 (L02_C2_aws-375) |
| Chiffres de point mort 17 850 / 19 600 / 19 728 | LAB, 08/10 | « superseded » par la correction de 14:47 | H:1563 (L02_C2_aws-318, L02_C2_aws-321 → L02_C2_aws-324) |
| Espoirs locaux du labo (produits ≥ 8, peu de Fano par sommet, etc.) | LAB, réfutés par LAP (CP-SAT) | configurations locales trouvées | H:1327-1332 (L02_C2_aws-291) |
| « Un partenaire par représentant sans prisme » | réfuté par Codex | trois prismes d'un pinceau | H:1564-1565 (L02_C2_aws-325) |
| Piste « énergie d'apex » | LAP | réfutée par calcul (1,87 à 2,02 < 3,083) | H:1848-1850 (L02_C2_aws-356) |
| « Au plus deux représentants par classe » | LAP | faux en général (contre-exemple de pinceau) | H:1545-1546 (L02_C2_aws-323) |
| Lemme des graines (13 configurations) | LAP | affiné à 4 par graine ; motif (c) de LAP impossible | H:1240-1241 (L02_C2_aws-276 → L02_C2_aws-277) |
| Une phrase de la partie (c) du théorème de structure des prismes | LAB | fausse (« demi-grilles ») ; conclusion g ≠ 5 conservée | H:1433-1434 (L02_C2_aws-307) |

**Redécouvertes (même résultat établi deux fois).**
- Configuration norme 14 et route d'Hermite close : notes/110 (septembre) puis LAP le 07/10 21:05 (H:1195-1197 ; L02_C2_aws-267, L02_C2_aws-271).
- Repère en un sommet, rang₇ d'une étoile : note 97 « L20 » (septembre) puis LAP le 08/10 21:31 (H:1886-1888 ; L02_C2_aws-359) ; voisin du « cadre du sommet » du Mandat C (M:220-225 ; L02_C2_aws-399).
- Rang 43 par l'anisotropie et recollement de rang 48 : NOTE du labo (section 6, 17.22(e)) avant le Mandat C §12 (H:1883-1885 ; L02_C2_aws-359, L02_C2_aws-410).
- Formule d'oddité au rang 37 = « τ non carré » de septembre ; accord avec Codex 205/207 (H:1892-1893 ; L02_C2_aws-360).
- Lemme I (torsion d'une composante jamais équilibrée) : note 126 par. 3 bis, re-vérifié (G:33-37 ; L02_C2_aws-366).
- Égalité de masse 8 (deux grilles en un point) : déjà dans la note 183 §4 de Codex (H:1578-1579 ; L02_C2_aws-326).
- Z² = 7Z − NᵀN + J = « R = 0 implique les équations SRG » de septembre (H:1851-1853 ; L02_C2_aws-357).
- Scindage ker_Z N = L_far ⊕ K(F) au rang 37 générique : HANDOFF 08/10 17:17 (L02_C2_aws-344, forme forte) puis Mandat C lemme 10 / corollaire 11 le 09/10 (L02_C2_aws-397, forme plus faible : norme < 14, trois ombres). Même auteur.
- Contenu des notes de septembre (L8, L10, L21, notes 103, 127) relevé par la vérification de duplication du 08/10 15:42 (L02_C2_aws-329).

**Écarts entre notes (pas des contradictions de fond, mais à ne pas confondre).**
- Minorations de b₂ au rang 43 : 914 (H:1348, PL à six paramètres de LAP), 922 (Codex 191, H:1373), 968 (Codex via cocliques, H:1389), 913 (Mandat C, programme de degré 0 avec les contraintes de la note 180, M:332, 497). Forme de la borne en b₁ : 462 + 42b₁ (H:1325), 462 + 41b₁ + b₁²/2 (Codex, H:1373), 462 + 41b₁ (M:324). Ce sont des PL différents ; b₁ pair, donc 42b₁ ≤ 41b₁ + b₁²/2.
- b₃ au rang 43 : ≥ 6 696 790 (H:1348) contre ≥ 7 073 772 (M:332) ; au rang 37, min b₃ = 24 948 sur le polytope à neuf classes (M:1118) contre b₃ ≥ 45 898 (Codex, H:1497) et b₃ = 43 848 dans la cible du labo (H:1276) : contraintes différentes (le programme à neuf classes n'a pas les recensements).
- a₇ au rang 37 : norme 14 seule ≥ 380 (M:329) contre 372 ≤ a₇ ≤ 767 sous b₂ = 462, b₃ = 45 528 (H:1468) ; plafonds a₇ ≤ 990 (graines), ≤ 842 (recensement, H:1360), ≤ 347 au sommet riche en grilles (H:1509).
- τ : ≤ 1403 (Codex 196-198, H:1497) puis ≤ 1354 (H:1716) ; minimum certifié des collisions de masse six par paire : 14 430 (H:1498) puis 16 496 (H:1510).
- Grilles par un point : « au plus 18 » (L10, H:1611) ; les notes 100 et 162 de septembre disent 18 ou 17 (H:1694) — désaccord interne aux notes de septembre, non tranché ici.
- Nombre de supports P3/N25 ouverts : 5345 (Codex note 245, M:610) contre 4581 (registre utilisé, M:885) — écart non expliqué dans les sources lues.
- Nombre de boules connexes : « about 2e11 » (H:1951) ; « 1,9·10¹¹ types au total, 1,4·10¹⁰ sans prisme et connexes » (M:228) ; « about 1e10 » sans prisme connexes (G:198, H:2013).
- Variante cubique à neuf classes : « environ 17 paramètres libres » (estimation, M:382) puis 19 (calcul, M:387).
- Statut de la note maille 5 : en-tête « Not audited by a third party » (G:4) alors que Codex note 224 en a audité une partie (H:1954-1958 ; G:135 le reconnaît) : en-tête périmé.
- Nommage des profils : « (6,6) » = (3,3), « (4,8) » = (2,4), « (4,4,4) » = (2,2,2) (septembre et commits contre NOTE.md) : piège de lecture, pas une contradiction.
- Support 664 : 414 720 étoiles (version 1, M:1031) contre 51 840 (version 2, à renommage près, star_check_72.log) : facteur 8 cohérent.

## 15. Dépendances : sur quels maillons non vérifiés repose chaque exclusion

### Partie K (campagne de calcul)

| exclusion | maillons non vérifiés |
|---|---|
| 91 réseaux S (balayage stream) | complétude du producteur C1 (comparée sur 4 réseaux) ; moteur frame_dfs (S, un programme, règles auditées par Codex) ; règle jumelle (statut et canonique : rang flottant, ordre de campagne ; recertification O) ; T16 pour le filtre Y = 13 ; enregistrements du PC du labo (≈780 représentants tier L, 28 réseaux sans branche) ; certificats Y1 donc T18 et T20 pour 9 143 représentants |
| 13 réseaux SD/GD (balayage de mise de côté) | tout ce qui précède, plus T18 et T20 (P, sessions IA, acceptés par l'utilisateur) via certificats exacts (C) ; 003:181 par le corollaire Y1 |
| 000 (O24) | 86 certificats LP (vérifiés deux fois selon le tracker, non refaits) ; 55 recherches (S, non refaites) |
| 004, 010 (Golay) | générateur golay_gen.py validé sur 001 ; recherches (S) ; une seule lecture |
| 28 anciens réseaux de listes + 105 | reprise v10 (S, deux machines sauf 044 ; 105 sur AWS et sur le PC) ; route des témoins (C) pour 17 réseaux ; règle jumelle pour 60 308 + 85 080 paires ; complétude des anciens plans y1 |
| 20 réseaux de niveau réseau | voir partie D |

### Partie B : T16, T18 et le pont

- **Exclusions par W8 (T16 ; filtre FD_MIN97 du moteur v10)** : T16 (vérifié par des sessions IA seulement ; classification finie
  de Wagner à deux implémentations, énumérateurs de couverture non relancés par Codex) ; le raccord graphe -> cadre (« T4 reste le
  lemme de travail du dossier pour reconstruire ce graphe depuis une solution (N,D) », `LEMME_EGALITE_8_SUR_7_C2.txt:22-26` ; F0
  non utilisé pour l'obstruction conditionnelle, « il intervient seulement pour passer des involutions à un sommet fixe à toutes
  les involutions », `..._PREUVE_CUBE.txt:259-264` ; dans `PROOF_C2` le point fixe unique vient de A.0 de A1,
  `A3_LEMMAS.md:9-10`, non lu) ; H4 garanti par le producteur seulement (les verdicts du filtre ne le vérifient pas,
  `bridge_REFEREE/REPORT.md:18-23`) ; modèle amont (Théorème R, L02_C2_aws-168, non lu ici).
- **Exclusions par W9 (T18 ; conversion des paires reportées)** : T18 (IA seulement ; décisions « kept » flottantes non utilisées ;
  programmes non audités ; scripts patchés ; certificats PSD échantillonnés ; v2 non arbitrée ; acceptation sur une réponse de
  l'utilisateur prise pour un oui) ; le pont (arbitré) ; H4 certifiée par paire (`certify.py`, `q/cert_stream.py`, non relus) ;
  modèle amont.
- **Corollaire Y1** : T18 et T20 et (R-vi) ; T20 a changé après l'enregistrement de l'acceptation (hors partie B) ; certificats
  vérifiés par deux vérificateurs ; Y1 non relu par l'arbitre du pont.
- **Paires reportées T20** : T20 (hors partie B).
- **T18 lui-même** ne dépend ni de T16 (L02_C2_aws-144) ni du dictionnaire (énoncé de graphe, `T18_PROOF.md:136-145`).

### Partie C : T20 et les calculs des branches lemma-run

- **Toutes les exclusions calculées** : justesse des moteurs (non audités ligne à ligne ; deux programmes écrits séparément, sauf III.1) ;
  exactitude des rejets selon les en-têtes et les parties lues ; « kept » flottant sans effet par (6.2) ; certificats seulement échantillonnés
  (15,000 III.0 ; 20,000 III.1 ; 6,358 IIa.0 ; 10 I.0 (4,2,1)) ; versions inférées (ARTIFACTS) ; branches non recalculées après coup sauf par
  un second programme (`ARTIFACTS_T18_T20.md:85-86`).
- **Réduction aux neuf configurations** : totaux par deux programmes ; complétude par les ordres d'automorphismes (énumérateur 1 + script de
  transcription + contrôle Codex des représentants imprimés).
- **III.0** : fichier de modèle `cases.py` commun aux deux implémentations ; le second suit le plan.
- **III.1** : modèle, groupe et squelette d'énumération communs ; règle de symétrie ensembliste (argument à la main, Lemme 7.3) ; plans et
  journaux hors git.
- **IIa.0** : modèle à la main commun, `iia_w.json` et structures partagés (comparés).
- **n_3 = 0** : modèle à la main commun, `structures_I.json` partagé ; table de 9.20 copiée de `final_table.out` (script absent) ; per-base
  des trois cas portables hors git ; comptes portables de I.0 (4,2,1) et I.5 (4,2,1) non retrouvés sur les branches citées.
- **n_3 = 2 (route B)** : deux programmes de la même session, modèle commun (`SPEC_ROUTE_B_N3.txt`) ; un portable ; archive non certifiée.
- **Théorème 10.2 et usage dans la route (C)** : arbitrage IA seulement ; points vus par l'auteur seul (L02_C2_aws-265) ; dictionnaire et pont
  hors du texte (`T20_PROOF.md:191-195`) ; acceptation utilisateur sur une version antérieure à G2.

### Partie D : réduction, audits, papier

- **Commun à tout :**
  - le Théorème R (P, une passe Codex) ;
  - les théorèmes cités : formule d'oddité, classification des formes sur F7, recollement, Borcherds ;
  - l'identité des 156 entrées (E, Codex, exact).
- **152, 153 :** A.9 (P), plus l'unicité exacte de leurs types de racines (E).
- **143 :** la preuve à la main (P), plus la table de types par recollement exact (C). Ni solveur ni recherche.
- **14 réseaux par empilement, 4 par piège dual :** la Prop. 8.1 (P), plus des invariants calculés par deux programmes, le
  second exact (E). Aucun certificat formel n'existe pour l'énumérateur.
- **91 réseaux de l'énumération principale :**
  - la complétude du producteur (E sur 4 réseaux seulement ; réduction de diagramme non couverte) ;
  - la recherche (S, un programme, règles auditées) ;
  - les transferts (a) et (c) (S, recertification O) et (b) (induction valide, compte de racines non recompté) ;
  - Y1, donc T18 et T20, pour les y1 à version non enregistrée ;
  - des enregistrements labo du 29/09 à programme retrouvé (au plus 946 y1 sans Y1, selon mon calcul).
- **13 réseaux à témoins :** la même chose, plus T18 et T20 (P, sessions IA) via des certificats (C).
- **000 :** 86 certificats PL (vérifiés selon le tracker, non relancés) et 55 recherches (S, non reproduites).
- **004, 010 :** enregistrements du 27/09 au 02/10 (S), recomptés seulement.
- **29 réseaux relancés :**
  - 17 réseaux reposent sur T16, T18, T20, des témoins certifiés (C) et la complétude du producteur ;
  - les 11 autres ajoutent 1 610 témoins caractéristiques (rapportés, non rejoués par Codex), 1 004 recherches (S) et 38 paires
    d'un run sans transfert ;
  - 044 n'a eu qu'un passage.
- **T16, T18, T20 :** des réductions à la main et des énumérations exactes avec seconds programmes. L'indépendance est
  partielle pour une configuration de T20. Les relectures sont des sessions IA, avec acceptation par l'utilisateur.

### Partie A : matériau C1 hébergé dans le dépôt

| exclusion ou résultat négatif fort | maillons non vérifiés (dans ce matériau) |
|---|---|
| r ≥ 33, r ≥ 35 (L02_C2_aws-274, L02_C2_aws-277) | PL thêta exact du labo (certificats de Farkas) audité par Codex (notes 168, 170, 172), non relu ici ; « la norme 14 force r ≥ 33 » (Codex) ; deux familles de vecteurs de norme 8 (labo) ; graines : 4 par graine (Codex, labo) |
| rang 35 exclu (L02_C2_aws-283) | recensements à 6 et 7 sommets, identité exacte de la note 179 par. 6, programmes, notes 168/172/175 au-delà de S ≥ 4h : NON vérifiés par LAP (H:1282-1283) ; lemmes G, F, tassement des graines, a₇ ≤ 990 : vérifiés à la main par LAP |
| maille ≥ 5 ⇒ connexe au rang 37 (L02_C2_aws-364) | balayage de GL₃ au sommet 0 et les 576 recherches d'étoiles non rejoués par Codex ; programmes C de LAP ; corollaire P = S = 0 : notes 125, 126 de conway99-c1 (non re-démontrées) |
| (2,2,2) sans étoile ; (3,3) sans prisme mort (L02_C2_aws-373, L02_C2_aws-375) | non audités ; recherches exhaustives d'un seul auteur ; correspondance 257 + 18 = 275 non vérifiée par moi |
| énoncé B (L02_C2_aws-377) | incomplet ; boules (2,4) sans torsion et de torsion 1 faites par le labo (commit d51ebbd de conway99-c1, non lu) |
| pas de seconde complétion au rang 37 générique (L02_C2_aws-388, L02_C2_aws-390) | preuves de LAP non relues par un tiers ; lemme de Codex relu par LAP ; note 232 « annoncée, pas encore poussée » |
| (39,39) fermé (L02_C2_aws-391) | calcul de Codex (note 233, commit local 5054889 non poussé) NON relu |
| symétrie forcée (L02_C2_aws-389) | exclusions des automorphismes d'ordres 2, 3, 7, 11 (dépendance C2/C3 du programme, hors de ce matériau) |
| S₀ : #P3/N25 ≥ 10 ; identité de budget ; congruences (L02_C2_aws-423, L02_C2_aws-431, L02_C2_aws-432) | programme à neuf classes (validé sur K₈ ⊕ B¹⁸) ; zéros démontrés des classes ; « 231 droites », « 99 sommets » ; Codex : « pas de norme 16-24 ⇒ pas de racine » (relais) |
| 1310 supports P3/N25 tués (L02_C2_aws-453) | lemmes A, B, C (à la main, LAP, non relus par un tiers) ; star_check.py (« écrits par moi seul, non relus ») ; complétude du registre de Codex (4581 supports, branche codex/p3-n25-register, non vérifiée ici) ; les P3/N25 ne sont forcés que dans S₀ (M:645) |
| « rang 37 ⇒ P > ~285 » (L02_C2_aws-380) | PL du labo (relais), masses 7 à 9 non bornées |
| rangs 37-43 non exclus par les programmes thêta (L02_C2_aws-401-A144, L02_C2_aws-428) | solveurs exacts de LAP ; point de faisabilité vérifié par le programme lui-même |

## 16. Notes lues, survolées, non lues

**Bilan des 1 014 notes du lot (classement par contenu ; une note = un contenu distinct avec toutes ses copies).**

| catégorie | nombre | lecteur | profondeur | raison si non lu |
|---|---|---|---|---|
| Journaux des branches `run/*` (`status.txt` 255, `tail_agent.txt` 204, `done.txt` 168, `tail_run_jobs.log.txt` 44, `tail_setup.log.txt` 44, ordre CI 1) | 716 | K | agrégés par script (L02_runs.py : statuts, comptes, 18 831 enregistrements ; L02_tails.py : événements d'erreur) ; aucun lu un à un | journaux machine : le contenu utile est agrégé en sections 3 à 6 |
| T16, T18, pont (`lemma/t16`, `lemma/t18*`, `lemma/bridge*`, `BRIDGE.md`, `LEMMA_TARGET`, `A2_BRIDGE`, `A3_LEMMAS`, `REFEREE_T16_PROOF`) | 64 | B | voir la liste de la partie B (T18_PROOF.md lu aux lignes 1-2100) | annexes C, D de T18_PROOF ; programmes .py |
| Campagne (README, OLD_README, REPRO_COMMANDS, FINAL_STATEMENT_DRAFT x3, B_LATTICES, B_TABLE_156, mesures, listes de clés, outils du labo) | 55 | K | lues en entier : README, OLD_README, FINAL_STATEMENT_DRAFT (3 versions, diff), B_LATTICES, V10_TIMINGS, results_laptop/README, engine_history/README, split_v1/README, shell_counts_first_run, LARGE_FILES_NOT_IN_GIT, les 22 `hand_28/check_*.txt`, `check_cert_y1_003.txt` (début, fin, compte) ; survolées : REPRO_COMMANDS (sections A-C), B_TABLE_156 (en-tête, légende, table analysée par script, appendice échantillonné), fleet_launch.txt (début), SWEEP_STATE ; listes de clés (`q/tools/laptop_2026-10-06/*.txt`, `parked_*`, `cert_done.txt`) : formats vus, totaux de `golay_heavy_00x` recalculés (2 244 / 7 629 et 4 080 / 10 269, 2 113 blocs sans recherche complète) | listes de données : pas d'énoncé |
| Branches `lemma-run/*` et archive route B (STATUS, ALL, timing, SUMMARY, shares, versions, README) | 53 | C | lues ou agrégées (partie C) | fichiers par partie comptés, non lus |
| Données du labo (`data/finishC/telemetry_backfill/*_pairs.txt` 40, `stream/078/full/p_*.txt` 4, `078/sample_chunk2`, `051/prof_pairs`, `plans_summary`) | 46 | K | format survolé (lignes JSON de paires y1/y2 en fractions ; `plans_summary` : rang, composantes, orbites y1 par réseau) | données brutes (jusqu'à 13 Mo par fichier), pas d'énoncé |
| T20 (`T20_PROOF`, `T20_BOARD`, `T20_WORK`, `ARTIFACTS`, `lemma/t20*`, `lemma/cloud`, notes Codex de T20) | 27 | C | voir la liste de la partie C | programmes .py |
| Réduction, audits, papier (`lemma/upstream`, `PROOF_C2` A1/MAIN/README, `paper/*`, notes Codex de la réduction et du papier) | 26 | D | voir la liste de la partie D | PDF (construits depuis les .tex) |
| HANDOFF_2026-10-01.md (14 versions) | 14 | K + A | master : lignes 1-1172 lues par K, 1173-2019 par A ; les 13 autres versions (branches v2..v10, tail-runner, defer-*, agent-backlog, tmp/push-test-laptop) comparées : préfixes de master (au plus une ligne d'état différente pour v2 et v3) | - |
| Matériau C1 (`c1_mandat_c_transformations`, `c1_rank37_girth5_lines`) | 7 | A | voir la liste de la partie A | données (types, boules) survolées |
| Notes Codex de la campagne (CHECKPOINT_156, REFEREE_TWIN_DEPENDENCIES, REFEREE_RERUN_713, REFEREE_HAND_WITNESSES, FIXED_Y1_003) | 5 | K | lues en entier (REFEREE_RERUN_713 jusqu'à la ligne 150) | - |
| File `queue` (`order.txt`) | 1 | K | agrégée par script avec `events.jsonl` et `control.json` | - |

Hors notes (pas dans l'inventaire, mais lus comme preuves) : `measures/*.json` (CERT_CENSUS, lemmas_accepted, RERUN_Y1_SUMMARY,
TWIN_RESIDUE_AFTER_Y1, TWIN_VERDICT_TALLY, twin_recert_test/TEST_043, cert_golay_001/002, twin_sample/producer_cost_sample : champs
de tête ou sommes par script), `machines.json`, `SHA256SUMS`, `q/twin_recert.py` (docstring), messages de commit de master et des
branches. Non lus : le code des paquets (`c2_cloud_run.zip`), les scripts `q/*.py` au-delà de leurs docstrings, les gros JSON de
mesures (`AUDIT_RIGID_MANIFEST`, `CERT_MANIFEST`, `STREAM_RECOUNT`, `SWEEP_LAB`, `codex_exact_lattice_identity`) au-delà de leurs
totaux cités par les notes.

Copies hors git signalées par l'inventaire : `Desktop/Recherche_Conway/c2_experimental/aws_repo/...` (copie de travail du dépôt),
`.../t20-codex/...` (copie de travail de Codex), `work/...` du dépôt researcher2 (copies de FINAL_STATEMENT, VERIF_CUBE, t20_hand,
indep_wagner_check, scratchpad_LAB), `Desktop/Recherche_Conway/c1-lap-girth5-audit/15a3cfe3f/` (mêmes blobs que
`c1_rank37_girth5_lines/good_u0.txt` et `good_after_1.txt` ; ce n'est pas une branche).

### Partie B : T16, T18 et le pont

**Lues en entier** : `LEMMA_TARGET_2026-10-06.md` (master et diff des trois branches) ; `lemma/T16_PROOF.md` ; dans
`lemma/t16/dossier_2026-10-04/` : `LIRE_DOSSIER_WAGNER.txt`, `LEMME_EGALITE_8_SUR_7_C2.txt`,
`C2_PROLONGEMENT_SUPPORT16_PREUVE_CUBE.txt`, `C2_WAGNER_BORNE_9_SUR_7.txt` ; `lemma/t16/lab_check/VERIF_CUBE_OBSTRUCTION_2026-10-04.md` ;
`lemma/t20_CODEX/REFEREE_T16_PROOF.md` ; `lemma/t18/T18_REPORT.md` (master, diff defer-mode) ; `lemma/t18/N3_REPORT.md` ;
`lemma/t18_B0/REPORT.md` (+ `b0_body_src.txt`, `b0_final_note.txt`) ; `lemma/t18_B2/REPORT.md` ; `lemma/t18_STRUCT/REPORT.md` ;
`lemma/t18_VERIF331/REPORT.md` ; `lemma/t18_REFEREE/REPORT.md` ; `lemma/t18_REFEREE2/REPORT.md` ;
`lemma/t18_PROOF/T18_PROOF_v2_changes.txt` ; `lemma/BRIDGE.md` (master, diff defer-n4, diff `bridge/BRIDGE.txt`) ;
`lemma/bridge/certify.out.txt`, `engine_check.out.txt`, `graph_check.out.txt`, `wagner_rerun/compare_A.txt`, `compare_B.txt`,
`enum_A.log`, `enum_B.log`, `verif.log`, `verif_y13.log`, `wagner_verify_shipped/verif.log` ; `lemma/bridge_REFEREE/REPORT.md`,
`ref_arith.out.txt`, `ref_engine.out.txt`, `ref_graphs.out.txt` ; `lemma/PROOF_C2/A2_BRIDGE.md`, `A3_LEMMAS.md` ;
`measures/lemmas_accepted_2026-10-07.json`.

**`lemma/T18_PROOF.md` (163 Ko, 2 206 lignes)** : lues les lignes 1-960 (préambule, énoncé, sections 2-6, 7.1), 960-1090
(7.2-7.3), 1090-1260 (7.4-7.6), 1260-1945 (section 8 entière, conclusion, sections 9.1-9.7), 1945-2100 (annexe A) ;
survolées 2100-2130 (début de l'annexe B) ; non lues 2130-2206 (fin de l'annexe B, annexes C et D).

**Survolées** : `lemma/t16/independent_check/` (`crosscheck_A.txt` début et fin, `crosscheck_B.txt`, `out_A.txt` fin, `out_B.txt`,
`validate_*.txt`) ; `lemma/t18_B0_VERIFC/` (liste des fichiers ; sorties `04` à `13`, début ; aucun rapport dans ce dossier) ;
listes `lemma/t18/r3_*` et `r4_*` (voir ci-dessous) ; `r4_rank.out`, `t18_STRUCT/rank_survivors.out`, `verify_S.out`,
`t18_REFEREE/ref1_quartic9.out`, `t18_REFEREE2/q9.out`, `r4_stageD_B1.out`, `r4_verifyD.out`, `t18_B2/b2_certs_check.out`,
`n3_check.out` (début) ; `HANDOFF_2026-10-01.md` (recherche par mots et lignes 610, 772, 818-836, 905-950, 984-991, 1000-1012) ;
`lemma/upstream/AUDIT_ENGINE_RULES.md` (lignes 1-12, 56, 350-372) ; `lemma/ARTIFACTS_T18_T20.md` (titres, lignes 9-14) ;
`lemma/t20_CODEX/FIXED_Y1_003.md` (lignes 1-80) ; `T18_PROOF_v1.md` (comparaison des titres et identité avec e657f46c3).

**Listes r3_* / r4_* de `lemma/t18`** : `r3_coverage_B1.json` (968 appariements de B1 faits, 291 non faits après deux lancements),
`r3_coverage_B1_final.json` (1 080 / 179 après trois), `r3_left_g*.txt` (appariements restants répartis par processus pour le
troisième lancement), `r3_left41_g*.txt` (les 41 appariements restants porteurs de triples, quatrième lancement),
`r3_last_g*.txt` (cinquième lancement : #1089, #1091, #1092 et les 138 appariements sans triple), `r3_remaining_B1.json`
(#1089, #1091, #1092 : 172, 152, 158 triples), `r4_left_g0/g1.txt` (indices des triples de #813 / #975 restant pour la seconde
implémentation v2, produits par `r4_left_lists.py`), `r4_left_t813.json` (liste vide : les 170 triples sont faits).

**Non lus** (hors du périmètre demandé ou volume) : tous les programmes `.py` (aucun audit de code) ; les fichiers de certificats
JSON (`WAGNER_PROFIL_*_CERTIFICATS.json`, `C2_EGALITE_8_SUR_7_VERIFICATIONS.json`, `C2_PREUVE_CUBE_CONTROLE.json`, manifestes,
`r3cert_*`, `r4cert_*`) ; les quelque 300 autres sorties de `lemma/t18*` ; les sorties de `t18_REFEREE2` autres que `q9.out` ;
`lemma/upstream/AUDIT_REDUCTION.md` (Théorème R, A.5) ; les fichiers T20 (`T20_PROOF.md`, `T20_BOARD.md`, `t20_*`) ; les autres
parties de `lemma/PROOF_C2/` (A1, B, MAIN) ; `q/defer_consumer.py`, `q/cert_stream.py`, `q/cert_y1.py` ; `measures/cert_y1*`.

### Partie C : T20 et les calculs des branches lemma-run

**Lues en entier** (master sauf mention) : `lemma/T20_PROOF.md` (2967 lignes ; preuves des sections 2-5 et 9 lues plus vite que les
énoncés, calculs, statuts, 6.5, 9.B, section 10 et annexes) ; `lemma/T20_BOARD.md` ; `lemma/T20_WORK.md` ; `lemma/ARTIFACTS_T18_T20.md` ;
`lemma/t20/T20_REPORT.md` ; `lemma/t20_R2/REPORT.md` ; `lemma/t20_R3_I/REPORT.md` ; `lemma/t20_R3_I/SPEC_ROUTE_B_N3.txt` ;
`lemma/t20_III1/README.md`, `VERIF.md` ; `lemma/t20_HAND/NOTES.md`, `SPEC_N3.md` ; `lemma/t20_CODEX/HAND.md`, `EDGE_BOUND.md`,
`PROFILE_421.md`, `TRIANGLE_REDUCTION.md`, `n3_second/README.md`, `n3_second/MEASUREMENTS.md`, `REFEREE_T20_PROOF.md`,
`REFEREE_PAPER_c1bcba6bb.md` ; `lemma/cloud/README.md`, `run.sh` ; scripts de job `lemma/cloud/jobs/t20_*.sh` (en-têtes et boucles).
Versions antérieures : diffs complets de T20_BOARD, ARTIFACTS et T20_PROOF entre `origin/tmp/push-test-laptop`, `origin/defer-n4` et master ;
début (l.1-60) et titres de la version defer-n4 de T20_PROOF.

**Survolées** : `lemma/t20_R2/eng3_run.txt` et `engv_run.txt` (début et fin : ce sont des fragments de source, la fonction `run` des moteurs,
concaténés par `mk_eng3.py` et `mk_engv.py` et modifiés par `patch_e3a.py`, `patch_e3b.py`, `patch_v1.py` ; pas des sorties de run) ;
`lemma/t20_CODEX/CHECKPOINT_156.md` (l.1-40) ; `lemma/FINAL_STATEMENT_DRAFT.md` (l.1-12, 29-46, 84-128) ; `final_table.out`, `n3_verify.out`,
`n3_check.out`, `cloud_check_t20_I_rest.out`, `cloud_vs_laptop_stage1.out`, `cmp_eng5_I0_421.out`, `RESULT_III1_VERIF.out` (l.1-30),
`rank_node_III1.out` (fin) ; branches : STATUS.txt, ALL.txt, timing.txt, job.log, verify_*.out, versions.txt, shares.txt, SUMMARY_before.txt,
sample.out (début et fin), README de l'archive ; un échantillon de fichiers par partie (un `.sum.json`, une ligne `.jsonl`, un `vf_*.json`,
un log de vérificateur) ; les JSON par base de la route A ont été comptés par un script de lecture (aucun calcul mathématique).

**Non lus** : les programmes `*.py` (seulement des en-têtes ou lignes vues par recherche) ; les centaines de fichiers par partie
(comptés) ; `lemma/BRIDGE.md`, `lemma/T18_PROOF.md`, `lemma/T16_PROOF.md`, l'article `lemma/PROOF_C2/paper/`, `HANDOFF_2026-10-01.md`
(hors périmètre T20) ; les autres notes de `lemma/t20_CODEX/` (REFEREE_143_PROOF, REFEREE_T16_PROOF, REFEREE_REDUCTION, REFEREE_SHELL_COUNTS,
REFEREE_HAND_WITNESSES, REFEREE_RERUN_713, REFEREE_TWIN_DEPENDENCIES, EDITORIAL_REVIEW_PAPER, LEAN_FEASIBILITY, EXACT_LATTICE_IDENTITY,
INDEPENDENT_PACKING ; FIXED_Y1_003 vue par une ligne seulement) : elles concernent T16, le réseau ou l'article, pas la preuve de T20 ; le
registre `lemmas_accepted.json` du labo (pas dans ce dépôt).

### Partie D : réduction, audits, papier

**Lues intégralement**

- `lemma/upstream/README.md`, `MODEL.md`, `PROOF_SKELETON_C2.md`, `AUDIT_REDUCTION.md`, `AUDIT_ENGINE_RULES.md`.
- `lemma/upstream/LATTICE_143.md` (master). La version de `origin/tmp/push-test-laptop` est un état antérieur (préfixe) : elle n'a
  pas le paragraphe du certificat linéaire (master:55-57). Aucune divergence de fond.
- `lemma/t20_CODEX/REFEREE_REDUCTION.md`.
- `REFEREE_143_PROOF.md` (master). La version laptop est un état antérieur sans la section « Equivalent certificate »
  (master:39-52).
- `REFEREE_SHELL_COUNTS.md`, `EXACT_LATTICE_IDENTITY.md`, `INDEPENDENT_PACKING.md`, `LEAN_FEASIBILITY.md`,
  `REFEREE_PAPER_c1bcba6bb.md`, `EDITORIAL_REVIEW_PAPER.md`.
- `lemma/PROOF_C2/README.md`, `MAIN.md`.
- `lemma/PROOF_C2/A1_REDUCTION.md`. Son corps (lignes 20-191) est identique à AUDIT_REDUCTION.md:44-215 (diff vide).
- `lemma/PROOF_C2/paper/main.tex`, lu en entier (1061 lignes). Le code TikZ des figures n'a été que parcouru.
- `asymmetric.tex`, `supplement.tex`.
- Les autres fichiers (`origin/tmp/push-test-laptop`, autres branches) sont identiques à master ou absents.

**Lus hors de la liste, pour la règle de transfert**

- `lemma/t20_CODEX/REFEREE_TWIN_DEPENDENCIES.md`, en entier.
- `lemma/upstream/theta_odd24.py` : docstring et lignes 19-60.
- `measures/TWIN_RESIDUE_AFTER_Y1_2026-10-07.json` : j'ai refait les sommes avec un petit script en lecture seule.
- `lemma/t20_CODEX/exact_twin_type_controls.json` : en-tête seulement.

**Survolés**

- `lemma/PROOF_C2/paper/table156.tex` : en-tête, légende, lignes des méthodes autres que « enum. », total ; comptage des lignes
  par méthode avec grep.
- `lemma/FINAL_STATEMENT_DRAFT.md` : lignes 1-60 et 100-128.
- `lemma/PROOF_C2/B_LATTICES.md` : lignes 55-100 et 175-205.
- Messages des commits cités (avec `git show -s`).

**Non lus**

- Raison : PDF construits à partir des .tex : `main.pdf`, `asymmetric.pdf`, `supplement.pdf`.
- Raison : hors du périmètre de la partie D, probablement couverts par d'autres parties :
  - `A2_BRIDGE.md`, `A3_LEMMAS.md`, `B_TABLE_156.md`/`.json`, et le reste de `B_LATTICES.md` ;
  - `T16_PROOF.md`, `T18_PROOF.md`, `T20_PROOF.md`, `ARTIFACTS_T18_T20.md`, `BRIDGE.md` ;
  - `REFEREE_T16_PROOF.md`, `REFEREE_T20_PROOF.md`, `REFEREE_RERUN_713.md`, `FIXED_Y1_003.md` ;
  - les autres notes et scripts de `t20_CODEX` ; `AUDIT_ENGINE_SOURCES.json`, `budget_143.py`.
- Raison : non accessibles ici : les sources externes C1, structures, Astra, SHELL et FLEX.

### Partie A : matériau C1 hébergé dans le dépôt

**Lues en entier.**
- `HANDOFF_2026-10-01.md` (master) lignes 1173-2019 (fin du fichier : 2019 lignes).
- `c1_rank37_girth5_lines/NOTE.md` (244 lignes).
- `c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md` (1129 lignes, 97 866 octets).
- Messages de commit de master depuis le 07/10 20:00 (+0200) jusqu'au dernier commit c118f1aac (10/10 04:35 +0200), corps compris ; diffs des deux commits de correction fa0acfa56 et 7c177c4c9.
- Petits fichiers de résultats lus en entier : `pilotes.out` ; `p3n25_search/results/r_dual_37.log`, `r_short_37_paths.log`, `r_short_37_nopaths.log`, `r_trade_37.log`, `r_low_37.log`.

**Survolés (quelles parties).**
- Toutes les docstrings (premières lignes) des scripts Python des deux dossiers ; en-têtes de `enumc.c` et `reps48.py`.
- Données de `c1_rank37_girth5_lines/` : tailles et premières lignes de `types_m2.txt` (18 lignes : les 18 types ordonnés à deux droites par couche, format t1 t2 π flagI flag4), `types_m3.txt` (886 lignes : types ordonnés à trois droites par couche), `reps48.txt` (97 896 lignes : boules (2,4) représentantes, « s b taille d'orbite »), `good_u0.txt` (25 588 lignes : matrices M admettant une famille en u = 0), `good_after_1.txt` (44 lignes : celles qui passent aussi u = 1) ; `theta33_u1_u6.out` (début), `theta33_u0_full.out` (fin).
- Tous les journaux `sweep*.log` : nombres de lignes, première et dernière lignes, recherche de « solutions > 0 », « timeout > 0 », « alive > 0 », « DEAD » (aucune solution, aucun timeout ; 23 COMB-ALIVE dans T2_partial, conformes à la note).
- `p3n25_search/results/star_check_72.log` (début et fin) ; nombres d'identifiants dans `lemmaC_new_ids.json` (297), `phaseA_dead_ids.json` (326), `star_dead_ids.json` (366), `star_extra_ids.json` (72), `survivors_ABC_star.json` (3271) ; nombres de lignes de `lemma_witnesses.jsonl` (941), `linear_screen_1766.jsonl` (1766), `level2_certificates_5.jsonl` (5), `star_all.jsonl` (3640), `star_sample63.jsonl` (63), `level2_batch.jsonl` (63), `s0_cert_N32_b9.json` (112).
- Branches : présence de `HANDOFF_2026-10-01.md` et des dossiers `c1_*` sur toutes les branches distantes (211 branches de calcul `run/q-i-*`, `lemma-run/*` et les autres) : seule master porte la partie C1.

**Non lus (raison).**
- `HANDOFF_2026-10-01.md` lignes 1-1172 : hors de ma partie (autres agents du lot).
- Corps des scripts Python et des sources C (`*.c`), contenus des JSON/JSONL de données et de certificats (`comp66_types.json`, `comp_m2*.json`, `comp_m3_all.json`, `act33.json`, `tors_m4.json`, `s0_cert_N32_b9.json`, `level2_certificates_5.jsonl`, `lemma_witnesses.jsonl`, etc.), `theta33_u0_slices.out`, `conn_tors.out` : consigne « only skim scripts/data » ; aucun calcul relancé.
- Toutes les notes citées hors de ce dépôt (conway99-c1 : notes 90-262, NOTE du labo 17.xx, PASSATION_C1_2026-10-07.md ; conway99-structures-lab ; branches codex/c1-arithmetic-audit, lab/theta-lp-2026-10-08, codex/p3-n25-register) : hors du dépôt et de ma partie ; leurs contenus ne sont connus ici que par les relais du HANDOFF et du Mandat C.
- Dossier `c1-lap-girth5-audit/` : absent de master et de toutes les branches (vérifié).

## 17. Matériaux pour la recombinaison

Listes littérales, avec sources exactes, pour le recoupement automatique : (1) énoncés conditionnels, (2) bornes quantitatives, (3) lemmes ouverts et étapes manquantes, (4) méthodes transférables. « Vu par moi » = remarque de l'agent de la partie, non dite par la source.

### Combinaisons repérées à l'intérieur du lot (vu par l'agent L02, à vérifier)

Chaînes où un résultat d'une note du lot remplit, au moins en partie, l'hypothèse d'un conditionnel d'une autre note. Aucune n'est
établie : chaque ligne donne le maillon manquant et les statuts. Lignes du JSONL : α = L02_C2_aws-458, β = L02_C2_aws-459, γ = L02_C2_aws-460, δ = L02_C2_aws-461, ε = L02_C2_aws-462, ζ = L02_C2_aws-463.

| # | morceaux disponibles (statut) | conclusion visée | maillon manquant |
|---|---|---|---|
| α | Corollaire 8 du Mandat C : au rang 37, pour une droite T à G(T) connexe et 7 ∤ τ, toute symétrie de (boule, ombres) est un automorphisme de Γ ; « avec les exclusions du programme », (boule, ombres) est sans symétrie (P, non relu ; L02_C2_aws-389) ; exclusions des ordres 2 (C2 : S avec composante O ; L02_C2_aws-097), 3 et 7 (Lean selon les dépôts : P ; L02_C2_aws-100, L02_C2_aws-102), 11 (Behbahani-Lam, non ouvert : E ; L02_C2_aws-101) ; asymétrie conditionnelle (L02_C2_aws-098, L02_C2_aws-104) ; unicité de la complétion à rang 37 générique (lemme laplacien de Codex, relu par LAP : P ; L02_C2_aws-390) | les droites génériques du rang 37 sont exclues | l'énoncé « (boule, 60 ombres) au rang 37 générique a forcément une symétrie, ou n'existe pas », non démontré (`M:197-200`) ; la Proposition C (L02_C2_aws-383, O). Les deux sources le disent ; la chaîne avec les quatre ordres est vue par moi |
| β | Ce qui survit sans σ des preuves T16-T20 : équations locales, double comptage doublé, matrices 63E₋₄ et 77E₃, budgets ; la borne de rang devient 44 (P, non relu ; L02_C2_aws-266) ; tout vecteur propre entier de valeur −4 de norme ≤ 16 a ses entrées dans {0, ±1} (Codex, relais : P ; L02_C2_aws-270) ; la norme 14 sans σ = deux 7-ensembles reliés par le plan 2-(7,4,2), non exclue par comptage (P ; L02_C2_aws-267) ; au rang 37, au moins 380 vecteurs de L1 de norme ≤ 20 forcés (E ; L02_C2_aws-406) | exclusion du rang 37 si aucune « petite » fonction propre n'existe sans σ | une version sans σ des lemmes T aux normes 14 à 20 (non disponible : T18 et T20 utilisent σ, le point fixe p et N(p) ; L02_C2_aws-266). Attention : les vecteurs forcés sont dans L1, sur-réseau pair d'indice 3 de L = Z^99 ∩ ker(A + 4I) (`H:1206-1208`), donc pas forcément des vecteurs propres entiers ; à vérifier dans le lot C1 |
| γ | Sous-réseaux de type rang 43 dans L1 à tout rang r < 43 : une exclusion du rang 43 n'utilisant que le genre, M et les vecteurs courts de L1 exclut 37, 39, 41 (P, non relu ; L02_C2_aws-310) ; identités du rang 43 : nombre de P3/N25 = 10 + objets bas (C ; L02_C2_aws-423), identité de budget (E ; L02_C2_aws-431), S₀ n'est jamais sans objet bas (E ; L02_C2_aws-432) | exclusion de 37, 39, 41 par les outils du rang 43 | ces outils utilisent l'égalité de classe du plan anisotrope et le programme à neuf classes ; au rang 37 le programme sans égalité de classe ne force aucun objet bas (L02_C2_aws-454) : il faut vérifier que les identités valent pour chaque Λ# (la partie A le signale) ; et S₀ n'est pas exclu (L02_C2_aws-422, A188 : 3 271 supports ouverts) |
| δ | Récurrence sur le nombre de racines (P, Codex ; K-C5 ci-dessous ; L02_C2_aws-030) ; formule entière du rang r = 4m/(n1 + 4) (P ; L02_C2_aws-035) ; reconstruction exacte des racines du jumeau (`q/codex_exact_twin_type.py`, contrôles passés) ; une borne inférieure certifiée du nombre de racines du jumeau suffit (L02_C2_aws-093, L02_C2_aws-092) | levée de la réserve de la règle jumelle sans recherche | exécuter la recertification (garée) : au plus 2 479 669 paires ; les paires de classe H (23 sur 33 311 dans le test de 043) demandent le moteur avec FD_TWIN=0 (L02_C2_aws-030) |
| ε | Lemmes A (parabole entière) et B (plafond), valables pour tout ensemble de sommets d'un srg(99,14,1,2) (P, LAP, non relus ; L02_C2_aws-442, L02_C2_aws-443) ; configuration norme 14 sans σ (L02_C2_aws-267) ; 12-ensemble U de l'exception de la note 183 (L02_C2_aws-286) ; supports déterminés de T18/T20 (parties B, C) | exclusion directe de ces configurations finies | appliquer les lemmes A et B à ces ensembles : non fait dans les sources lues (la partie A le propose pour C1 ; pour les supports de T18/T20, inutile depuis que T18 et T20 sont prouvés) |
| ζ | Matrices M1 = 63E₋₄ et M2 = 77E₃ et budgets de voisins communs, indépendants de tout automorphisme (vu par la partie B) ; borne de rang scindée 22/22 et 27/27 venant de trace(σ) = 1 et trace(σA) = 14 (P ; partie B) ; intégralité de la trace d'un automorphisme sur un espace propre (dispositif de MM04 ; partie D) | bornes de rang analogues pour un automorphisme d'ordre 3 (cas C3) ou pour C1 | recalculer les multiplicités des valeurs propres de l'automorphisme sur V₋₄ et V₃ pour l'ordre 3 (aucune source lue ne le fait) ; en C1 la borne reste 44 (L02_C2_aws-266) |

### Partie K (campagne de calcul et couverture)

**(1) Énoncés conditionnels**

- K-C1. **Corollaire Y1 (y1 fixé).** Si U (réseau du repère, Théorème R) contient une racine r avec |(r,y1)| = 2, alors aucun repère n'a cette normale y1, quel que soit y2 (car 8 <= E(r) = 10 - (r,y2)^2 force E(r) = 9 ou 10, contraire à T18 ou T20) ; si |(r,y1)| > 2, (R-vi) seul suffit. Hypothèses : Théorème R (R-vi, R-vii), T18, T20. Statut P (Codex ; relu par LAB et LAP), certificats C. Source : `conway99-c2-aws:master:lemma/t20_CODEX/FIXED_Y1_003.md:12-30`.
- K-C2. **Conséquence.** Sous R, T18, T20 : toute racine r vérifie |(r,y1)| <= 1 et |(r,y2)| <= 1, donc (r,y1)^2 + (r,y2)^2 <= 2. Statut P (Codex). Source : `FIXED_Y1_003.md:32-35`.
- K-C3. **Si T18 et T20 sont vrais** (et le pont racine -> fonction propre), alors les 13 réseaux 001, 002, 003, 005-009, 011-015 sont exclus (5 190 752 + 2 508 295 paires certifiées ; 003:181 par K-C1). Statut : certificats C ; T18/T20 P relus par IA seulement. Source : `master:lemma/FINAL_STATEMENT_DRAFT.md:85-88` ; `master:measures/CERT_CENSUS_2026-10-07.json`.
- K-C4. **Règle du vecteur caractéristique.** Si z est caractéristique de norme 16 dans U et (z,y1)^2 + (z,y2)^2 > 66, la paire (y1, y2) ne porte pas de repère (via (R-v) et la parité). Statut P (Codex). Source : `master:lemma/t20_CODEX/REFEREE_TWIN_DEPENDENCIES.md:167-174` ; `master:lemma/PROOF_C2/B_LATTICES.md:191-193`.
- K-C5. **Récurrence sur le nombre de racines (jumeau plus riche).** Si un repère existe, en choisir un dans un réseau de la liste ayant le plus de racines ; son jumeau contient le même repère, est dans la liste ; un jumeau à strictement plus de racines contredit la maximalité. Donc toute paire dont le jumeau a strictement plus de racines peut être écartée. Statut P (Codex). Source : `REFEREE_TWIN_DEPENDENCIES.md:10-26`.
- K-C6. **Transfert canonique.** Si le jumeau a le même type de racines, porté par un seul réseau de la liste, et une clé intrinsèque strictement plus petite (vérifiée exactement), la paire est écartée (contre-exemple de clé minimale). Statut P (Codex), avec l'hypothèse explicite de complétude du système de racines du jumeau. Source : `REFEREE_TWIN_DEPENDENCIES.md:36-51`.
- K-C7. **Si la recertification jumelle aboutit** (chaque paire du résidu en classe W, Z, M ou C, et les paires H exclues par le moteur avec FD_TWIN=0 et FD_SWAP=0), la réserve du papier sur la règle de transfert (sections 8.4 (iv), 9, 10) tombe. Statut O (garé). Source : `master:q/twin_recert.py:1-30` ; `master:HANDOFF_2026-10-01.md:1135-1143`.
- K-C8. **Lemme du noyau rigide (H2).** Un h d'empreinte nulle n'est possible que si les deux voisins pairs ont le même nombre de Coxeter H et si U a une composante de racines de nombre de Coxeter H (27 réseaux concernés). Statut P (« hand lemma (lab) », relecture non indiquée). Source : `master:lemma/FINAL_STATEMENT_DRAFT.md:49`.
- K-C9. **Loi K.** K + E(y1) + E(y2) = 3|Phi|/4 + 8 ; une paire K = 0 n'existe que si les deux voisins pairs ont le même nombre de Coxeter (h1 = h2). Statut P selon la source (preuve dans un autre lot). Source : `master:HANDOFF_2026-10-01.md:386-389`.
- K-C10. **Complétude des règles de témoins pour E <= 10.** E = 8 : vecteur de norme 3 avec Y = 13 ; E = 9 : racine avec Y = 5 ; E = 10 : racine avec Y = 4, ou vecteur de norme 4 avec |(x,y1)| = |(x,y2)| = 3 ; une paire sans témoin a donc un minimum dual >= 11/7. Statut P (« hand remark of 07/10 », relecture non indiquée dans la source). Source : `master:HANDOFF_2026-10-01.md:936-937` ; `master:lemma/FINAL_STATEMENT_DRAFT.md:30`.
- K-C11. **Mesure (pas une preuve).** Sur 016, 015, 014 et 011, toute paire cherchée a une racine témoin avec Y = 5 ou 4 ; un lemme « min L* >= 11/7 » supprimerait 99 à 100 % de la recherche. Statut H (mesuré). Source : `master:HANDOFF_2026-10-01.md:679-680`.

**(2) Bornes quantitatives**

- K-B1. Énergie : E(v) = 7 (v,v) - (v,y1)^2 - (v,y2)^2 >= 8 pour v hors de J = Zy1 + Zy2 (R-vi) ; T16, T18, T20 excluent E = 8, 9, 10 ; donc tout repère a E(v) >= 11 pour v de norme 2, 3, 4 sans témoin. Statut P (Théorème R relu par Codex ; T16/T18/T20 relus par IA). Sources : `FINAL_STATEMENT_DRAFT.md:23,30` ; `B_LATTICES.md:20`.
- K-B2. Vecteur caractéristique z de norme 16 : E(z) >= 42 puis E(z) >= 46, Y = (z,y1)^2 + (z,y2)^2 <= 66, Y = 2 mod 8. Statut P (Codex). Source : `REFEREE_TWIN_DEPENDENCIES.md:169-171`.
- K-B3. Racines sous K-C1 : E(r) = 10 - (r,y2)^2 pour |(r,y1)| = 2. Statut P. Source : `FIXED_Y1_003.md:17-22`.
- K-B4. Formule du rang : r = 4m/(n1 + 4), h = 2m/r, n1 = 2h - 4 pour un système de racines irréductible simplement lacé à m classes de signe. Statut P (Codex). Source : `REFEREE_TWIN_DEPENDENCIES.md:63-79`.
- K-B5. Résidu de la règle jumelle après Y1 : au plus 2 479 669 paires (1 025 447 transfert de statut + 1 454 222 canonique), 5 130 chunks, 11 234 représentants y1, 102 réseaux. Statut E. Source : `master:measures/TWIN_RESIDUE_AFTER_Y1_2026-10-07.json` (sommes de l'agent L02) ; `HANDOFF_2026-10-01.md:1136-1138`.
- K-B6. Paires dépendant d'un rang flottant dans la règle jumelle : 1 300 094 (statut) + 2 863 005 (canonique) = 4 163 099 ; 32 265 417 par jumeau plus riche (sûr). Statut E (compte d'un relevé fourni ; Codex : « independent sum of a supplied tally, not a recount of all underlying streams »). Source : `REFEREE_TWIN_DEPENDENCIES.md:151-154` ; `HANDOFF_2026-10-01.md:1118-1121`.
- K-B7. Paires exclues par recherche sans certificat : 25 775 627. Statut S. Source : `B_LATTICES.md:213-215`.
- K-B8. Lignes de norme 7 : 22 892 544 = 11178 x 4096 / 2 dans les réseaux comparés (140, 064). Statut E. Source : `FINAL_STATEMENT_DRAFT.md:25`.
- K-B9. Couverture Y1 : 9 143 des 10 802 représentants y1 hors paquet (55 réseaux S) et 4 073 des 4 334 représentants des 28 anciens réseaux ont une racine de produit 2 ; dans 003, 96 des 182. Statut C. Sources : `B_LATTICES.md:88-93,146-176` ; `FINAL_STATEMENT_DRAFT.md:31`.
- K-B10. Paires sans témoin d'énergie <= 10 dans les 28 anciens réseaux : 2 652 sur 173 708 (min E >= 11), dans 11 réseaux. Statut C pour les témoins ; minimum >= 11 non revérifié par Codex. Source : `B_LATTICES.md:176-180` ; `REFEREE_HAND_WITNESSES.md:71`.
- K-B11. Plafond du producteur : max_out = 10^6 candidats y2 par y1 (troncature silencieuse signalée par complete = false), relevé à 5 x 10^7 ; 003:162:182 a 1 765 122 candidats. Statut E. Source : `HANDOFF_2026-10-01.md:897-904` ; `results_laptop/README.md:9-11`.
- K-B12. Dépendances jumelles : 1 622 entre les 104 réseaux stream, sans cycle. Statut E (OK-RECOMPUTED). Source : `FINAL_STATEMENT_DRAFT.md:83`.

**(3) Lemmes ouverts et étapes manquantes**

- K-O1. Recertification de la règle de transfert jumeau (K-B5, K-C7) : seul point de calcul ouvert du papier ; garé le 07/10 20:36 UTC. Donnerait : les 4 163 099 paires à rang flottant établies sans dépendre de l'ordre de la campagne.
- K-O2. Complétude de l'énumération des paires (producteur C1) : comparée sur 4 réseaux seulement (140, 135, 141, 064). Donnerait : R3 sans réserve pour les 132 autres réseaux à paires.
- K-O3. Certificats des 25 775 627 paires exclues par recherche (ou seconde lecture ligne à ligne du moteur). Donnerait : passage de S à C pour la part « recherche ».
- K-O4. Archivage certifié des enregistrements du PC du labo (28 réseaux S sans enregistrement sur branche, environ 780 représentants tier L, réseaux 000, 004, 010 en lecture unique). Donnerait : la levée de la réserve de provenance.
- K-O5. Écart de calibration sur aarch64 (c8g) jamais expliqué ; les nombres de noeuds dépendent du CPU. Donnerait : l'assurance que les verdicts ne dépendent pas de la plateforme.
- K-O6. Minimum E >= 11 des 2 652 survivantes et 1 042 comptes rapportés (108 + 38 + 896) non rejoués ; certificats z caractéristiques à sauvegarder. Source : `REFEREE_TWIN_DEPENDENCIES.md:176-180`.
- K-O7. Relecture humaine et formalisation (Lean) : rien n'existe ; portée à convenir (`lemma/t20_CODEX/LEAN_FEASIBILITY.md`, partie D).

**(4) Méthodes transférables**

- K-M1. Mise de côté avec certificat (DEFERRED) : séparer les cas couverts par un lemme en attente des cas cherchés, sans jamais compter un cas comme exclu avant la preuve ; certificat exact par cas ensuite (dit par la source pour T18/T20 ; transférable à toute recherche exhaustive où un lemme en attente couvre une classe : vu par moi).
- K-M2. Certificat à normale fixée : un seul témoin (racine de produit 2) tue toute l'orbite d'un y1 avant d'énumérer y2 (dit par la source : « the certificate criterion can be applied before starting the y2 producer »).
- K-M3. Reconstruction exacte des racines du jumeau Q = 7x + (c - a) y1 + (d - b) y2 et type par la formule du rang, sans flottant (Codex, `q/codex_exact_twin_type.py`).
- K-M4. Complétude des couches courtes par l'identité thêta (des listes correctes ne peuvent être que courtes) : réutilisable pour tout réseau dont la série thêta est connue (vu par moi ; voir partie D pour H3).
- K-M5. Comparaison d'un énumérateur indépendant en forme canonique (F4) : contrôle de complétude réutilisable.
- K-M6. Prédicteur de coût I(y1) = somme des (r,y1)^2 sur les racines, ordonnancement « le plus lourd d'abord », découpage d'un job sur tous les coeurs avec enregistrement identique (tail runner).

### Partie B : T16, T18 et le pont

#### (1) Énoncés conditionnels

| # | si X | alors | statut | source |
|---|---|---|---|---|
| C1 | (G) srg(99,14,1,2) avec involution à un point fixe ; (U) U entier défini positif de rang 24, y1, y2 de norme 7 orthogonaux ; (F) 49 vecteurs de U orthogonaux à y1, y2, Gram 3I - S | pour tout v de U, phi_v est une fonction propre (-4) entière sigma-impaire de norme carrée 2E(v) | P | `lemma/BRIDGE.md:186-201` |
| C2 | U a une racine r avec (r,y1)^2 + (r,y2)^2 = 5 (et H4, T18, modèle amont) | la paire n'héberge le cadre d'aucun srg(99,14,1,2) à involution à un point fixe | P | `BRIDGE.md:16-18`, `203-205` |
| C3 | racine avec Y = 4, ou vecteur de norme 4 avec |(v,y1)| = |(v,y2)| = 3 | idem, conditionnellement à T20 | P (moitié pont) | `BRIDGE.md:19-21`, `207-209` |
| C4 | x de norme 3 dans U avec Y(x) = 13 | « paire impossible pour EX » (par T16) | P | `C2_WAGNER_BORNE_9_SUR_7.txt:26-28` |
| C5 | U a une racine r avec (r,y1) = ±2 (et T18, T20, (R-vi)) | aucun cadre de U n'a ce y1, quel que soit y2 | P | `BRIDGE.md:211-222` |
| C6 | T16, T18, T20 | E(v) >= 11 hors Z y1 + Z y2 ; une paire sans témoin a un minimum dual >= 11/7 | P | `lemma/PROOF_C2/A2_BRIDGE.md:32`, `52-55` |
| C7 | (avant Wagner) rang certifié >= 16 des projections des x avec Y(x) = 13 | la paire est exclue | X (caduc) | `LEMME_EGALITE_8_SUR_7_C2.txt:186-194` |
| C8 | min L* >= 10/7 (resp. >= 11/7) | retire 64 à 92 % (resp. 99 à 100 %) du temps de recherche des réseaux mesurés | H | `LEMMA_TARGET_2026-10-06.md:33-34` |
| C9 | un lemme T22 | déplacerait la frontière d'un pas | O | `A3_LEMMAS.md:73-74` |
| C10 | conclure « EX faux » par la route témoin entière | exige les coupes 1, 2, 3 et les entrées externes de cette route | O | `C2_WAGNER_BORNE_9_SUR_7.txt:376-380` |
| C11 | H16 (pas de fonction de norme carrée <= 16) | Q(k,n) = 9k^2 + 14k(n·1_T) + 7 n^T G n hors de {1..8} ; |somme_{i dans I}(f_O,f_i)| <= 1 pour I indépendant de B ; B sans ensemble indépendant de taille 4 | P (non vérifié) | `T18_REPORT.md:94-103` |
| C12 | (après round 1) | T18 équivaut à exclure les trois configurations B0, B1, B2 (S+, S- indépendants, S hors N[p]) | P | `T18_REPORT.md:105-110` |
| C13 | un ensemble déterminé a un Gram impair de rang exactement 22 | toute orbite ajoutée O vérifie b_O^T G^+ b_O = 3 exactement (4 pour une paire de N(p)) | P (énoncé, non exploité) | `t18_STRUCT/REPORT.md:57-58` |
| C14 | Y sigma-invariant avec au moins 23 orbites | tout mineur principal 23 x 23 de G_odd est nul ; G_even de rang <= 22 | P | `T18_PROOF.md:802-826` |
| C15 | Y quelconque | rang M1[Y] <= 44, rang M2[Y] <= 54 (un rang exact plus grand exclut ; cas des 4 survivants : 46 > 44) | P | `T18_PROOF.md:664-668`, `1937-1938` |
| C16 | le cadre n'engendrerait pas {y1,y2}^perp | on aurait seulement somme a_i^2 <= E(v) et E(v) = 9 n'exclurait rien | P (remarque) | `BRIDGE.md:300-302` |
| C17 | exclusion d'un réseau en mode report | demande (a) T18 et T20 prouvés et vérifiés indépendamment, ou (b) les paires reportées cherchées | procédure | `HANDOFF_2026-10-01.md:823-825` |
| C18 | la route X_0 d'abord terminée pour B0 | exclurait environ 95 % des représentants sans W | H | `lemma/t18_B0/REPORT.md:157-159` |
| C19 | fermer un réseau entier sans recherche des h | il manque un argument couvrant toutes ses paires de normales ... ou que le support extérieur de taille huit ne peut pas se prolonger | O (historique, avant Wagner) | `LEMME_EGALITE_8_SUR_7_C2.txt:250-254` |
| C20 | P3 (rang-nullité) | étape C (23 orbites + p) : partie impaire singulière, nullité paire >= 2 ; 27 orbites + p : nullité impaire >= 5, paire >= 6 (M), paire >= 1 (N) ; (3,3,1) Y u W (25 orbites) : nullité impaire >= 3 (contrôle non lancé) | P | `t18_STRUCT/REPORT.md:46-58` |

#### (2) Bornes quantitatives

| objet | borne ou valeur | statut | source |
|---|---|---|---|
| E(v) hors Z y1 + Z y2 | >= 8 (A.5), >= 9 (T16), >= 10 (T18), >= 11 (T20) | P | `A2_BRIDGE.md:25-32` |
| 1_S^T A 1_S pour |S| = 18 | <= 90, d'où e <= 2 | P | `T18_PROOF.md:283-292` |
| k (h actifs) | support 16 : 3k <= 2(8-k), k dans {0,2} ; support 18 : 18 - 2k >= 3k, k dans {0,2} | P | `LEMME_EGALITE_8_SUR_7_C2.txt:90-96` ; `T18_PROOF.md:260-279` |
| D | m(m-7) - 7e - somme d_i^2 >= 0 | P | `LEMME_EGALITE_8_SUR_7_C2.txt:112-114` |
| support 16 | d_z <= 2 ; |X_0|,|X_1|,|X_2| = 11, 64, 8 ; somme C(d,2) = 8 ; t <= 1, t = 1 en C2 ; somme_{X_0}(a-2) = 10 + 2t | P | `..._PREUVE_CUBE.txt:42-77`, `146-168` |
| double comptage du cube | somme q_z >= 10 (12 en C2) contre <= 8 | P | `..._PREUVE_CUBE.txt:128-142` |
| Wagner | 105 / 31 / 76 / 48-16 / 48-18 / 640-32 ; 400 + 240 tableaux A ; 6 544 orbites candidates ; 0 4-clique ; 17 à 36 candidats par tableau | C | `C2_WAGNER_BORNE_9_SUR_7.txt:196-206`, `278-312` |
| support 18 (n_3 = 0) | (n_0,n_1,n_2) = (9,54,18) ; avant N3 : n_0 = 9 - n_3, n_1 = 54 + 3n_3, n_2 = 18 - 3n_3 | P | `T18_PROOF.md:532-550` |
| d pour z hors S (support 18) | somme des d des voisins = 18 - 5d, donc d <= 3, puis d <= 2 | P | `T18_PROOF.md:513-530` |
| t (support 18) | h_2 <= t <= 9 ; en profil (2,5,0), t dans {2,4,6} | P | `T18_PROOF.md:574-600` ; `t18_STRUCT/REPORT.md:79-81` |
| identité (*) | somme_{X_0}(a-4)^2 + somme_{X_1}(a-2)(a-3) + somme_{X_2} a(a-1) = 36 | P | `T18_PROOF.md:570-574` |
| profils | h_0 <= 1 ; 4h_0 + n_3 <= 4 ; 2h_3 + 4h_0 + n_3 <= 4 ; somme_{w ~ p} a_2 = 36 - 2h_2 | P | `T18_PROOF.md:626-651` ; `t18_VERIF331/REPORT.md:39-41` |
| sous-produit N3 | a_0 <= 5 (z != p), a_0 <= 4 sur X_0 privé de N[p] ; a_2 <= 3 (X_2), <= 6 (X_1), <= 8 (X_0 privé de p, profil (2,5,0)) | P | `N3_REPORT.md:33-36` |
| (F7), (C3), (C4), (C7) | somme_{X_2} a_2(a_2-1) <= 24 ; FL pair <= 8 ; somme a_2(a_2-1) + m(t) <= 36 avec m(t) = 0, 2, 4, 6, 8, 14, 20, 26, 32, 42 pour t = 0..9 ; 2 <= |K_c| <= 2 + slack, slack = 4 - FL/2 | P | `T18_PROOF.md:1074-1081`, `1332-1351` |
| (D3) | 4 <= |Z n X_2| <= 4 + t (remarque REF2 : 3(a_2(z) - 4) <= 2t) | P | `T18_PROOF.md:1569-1585`, `1939` |
| rangs | M1 rang 44, M2 rang 54 ; sigma scinde V_{-4} en 22 + 22 et V_3 en 27 + 27 ; G_odd, G_even <= 22 ; parties de M2 <= 27 | P | `T18_PROOF.md:664`, `791-837` |
| graphes 4-réguliers sur 9 sommets | 1 024 380 étiquetés, 16 classes ; 3 à codegrés <= 2 (5 040 + 30 240 + 20 160 = 55 440) ; 18 paires déficitaires chacun | E | `T18_PROOF.md:443-497` |
| étape 1 | 99 rectangles, 63 utilisables ; 25 514 / 13 799 / 9 229 appariements ; 425 / 1 259 / 528 orbites ; |Aut| 72 / 12 / 18 | E | `T18_PROOF.md:916-930` |
| (3,3,1) | 3 510/7 224/2 406 ; 383/481/7 ; 8 639/27 203/0 ; 23/164/0 ; 52/1 839/- ; 0/0 ; M1 seule : 887/672/7, 102/190/0, 0/10/0 | E | `T18_PROOF.md:1150-1160`, `1191-1196` |
| (2,5,0) | 5 545/12 366/4 347 ; 4 904/11 509/3 863 ; 5 595/4 977/196 triples ; 0/4/0 survivants ; 2 667 représentants pour B0 | E | `T18_PROOF.md:1370-1378`, `1425-1437` |
| 4 survivants | M1 rang 46, M2 rang 45 sur 47 ; det G_odd = 47 684 et 874 944 ; rangs G_odd, G_even = 23 ; plus petite valeur propre ≈ 0,011 et 0,012 ; étape D 678/678/846/846 (849 sans la borne haute) | E / C | `T18_PROOF.md:1516-1622` |
| A21 (B1, (3,3,1)) | 164 tables ; 295 200 candidats ; 16 334 sans violation ; 2 avec G_odd singulier ; 0 satisfaisant les deux conditions | E | `T18_REPORT.md:607-621` |
| certificats | étape D : 3 048 complets ; B1 étapes B/C : 50 000 sur environ 1,6 million ; B2 : 12 000 ; B0 : non revérifiés | C / E | `T18_PROOF.md:1760-1765` |
| réduction par classes | a^2 + b^2 dans {0,1,2,4,5,8,9,10,13,18} ; E = 8 : (3;{2,3}) ; 9 : (2;{1,2}) ; 10 : (2;{0,2}) ou (4;{3,3}) ; 11 : (3;{1,3}) ; 12 : (2;{1,1}) ou (3;{0,3}) ; 13 : (2;{0,1}) ou (3;{2,2}) ; 14 : (2;{0,0}) | P | `BRIDGE.md:280-296` |
| cadre | 7 h de norme 4, 42 u de norme 3, rang 22 ; trace(3I - S) = 154 = 7 x 22 ; multiplicités 54 et 44 | P | `BRIDGE.md:87-104` ; `bridge/graph_check.out.txt` |
| 011 | 56 racines, 4 096 vecteurs de norme 3, 96 912 de norme 4 (signes compris) ; 363 / 400 témoins Y = 13 ; 19 Emin = 9, 18 Emin = 10 ; T18 279, T20 113, aucun 8 ; det K = 49 (13 paires) | E / C | `bridge/engine_check.out.txt:1-27` ; `bridge/certify.out.txt:2` |
| campagne | 5 190 752 paires sur T18, 2 508 295 sur T20 ; 7 762 enregistrements stream certifiés ; Y1 : 96 / 182 représentants de 003, 9 143 / 10 802, 4 073 / 4 334 | C (selon la source) | `A2_BRIDGE.md:73-87` ; `BRIDGE.md:220-222` |
| Emin des paires cherchées (016) | 75,7 % / 23,5 % / 0,8 % pour Emin = 9 / 10 / 11 ; 440 625 retirées par v10 ; 258 580 cherchées | E | `LEMMA_TARGET_2026-10-06.md:18-29` |
| analogues 9 et 243 | Paley(9) : c = 3, rang H = 2 sur 4 ; srg(243,22,1,2) : c = 9, rang H = 55 sur 110, complément rang 66, 121 orbites (11 intérieures, 110 extérieures) | E | `bridge_REFEREE/ref_graphs.out.txt:1-30` |

#### (3) Lemmes ouverts ou étapes manquantes

- **T22** (E = 11) : non revendiqué ; supprimerait le reliquat d'énergie 11 de la recherche de cadre (`A3_LEMMAS.md:70-74` ;
  `LEMMA_TARGET_2026-10-06.md:27` pour la forme des vecteurs).
- **Profil (2,5,0) à la main**, non-singularité structurelle du Gram impair de T u X_2 u W, P3 à l'étape B : donneraient une
  preuve de T18 sans énumération pour ce profil (`t18_STRUCT/REPORT.md:100-107`).
- **Preuves écrites de P6, P7, P8** (L02_C2_aws-138) : non nécessaires à T18.
- **Coupes k = 1, 2, 3 de la note 54** : nécessaires seulement pour la route témoin entière (L02_C2_aws-126).
- **Existence de U depuis le cadre** (forme 7-adique) : manquante dans le pont, « proved since then: Theorem R » selon la source
  (L02_C2_aws-168).
- **« What a continuation would have to use (untested) »** (round 1 de T18) : compter, pour chaque v extérieur et s dans S, les
  voisins extérieurs forcés c_s(v) = (1 ou 2) - |N(v) n N(s) n S| et les rendre cohérents (`T18_REPORT.md:116-119`) ; dépassé
  par les rounds suivants.
- **Audit des programmes, certificats complets, représentants de B0, lecture de la v2, Lean** : section 5, leviers 3 et 4.

#### (4) Méthodes qui pourraient se transférer

Dit par la source :
- Loi de parité et identités de comptage valables pour tout m, « apply to [T20] as they stand (m = 10) »
  (`LEMMA_TARGET_2026-10-06.md:129` ; `T18_REPORT.md:38-44`).
- Méthode du 04/10 réutilisée pour T18 : partition X_d, comptes de chemins, paires déficitaires appariées par les orbites de
  X_2, ensembles déterminés, budgets, PSD exacte (`LEMMA_TARGET_2026-10-06.md:133-136`).
- Squelette commun des preuves T(2E) (valeurs 0/±1, équation, structures du support, exclusion par budgets et deux matrices PSD) ;
  « The work grows quickly with E » (`A3_LEMMAS.md:22-30`).
- Pont en paramètres généraux pour srg(v,k,1,2) avec involution à un point fixe : c = r - s = sqrt(4k - 7), Gram du cadre rI - S,
  E = cN - Y ; validé sur Paley(9) et srg(243,22,1,2) avec x -> -x (`BRIDGE.md:388-402` ; `bridge_REFEREE/ref_graphs.out.txt`).
- Faits généraux de T18 (A0, iota, traces, parité, comptage, chemins) vérifiés sur srg(243,22,1,2) (`t18_REFEREE/REPORT.md:113-114`).
- Corollaire Y1 : s'applique avant de lancer le producteur de y2, une racine certifiée couvre toute l'orbite du premier normal
  (`lemma/t20_CODEX/FIXED_Y1_003.md:28-35`) ; utilisé sur de nombreux réseaux (`A2_BRIDGE.md:73-75`).
- Outils réutilisables tels quels : `c_mine.py` « runs unchanged » sur B0 et B1 (`t18_B2/REPORT.md:95-96`) ; `r3_p250.py`
  « apply unchanged » à B0, B2 (`T18_REPORT.md:419`).
- Non-transferts dits par la source : le double comptage du cube ne passe pas à T18 (`T18_REPORT.md:282-283`) ; l'intégralité de
  7E 1_S est « special to T18 » (9 divise 18) (`t18_STRUCT/REPORT.md:32`) ; le lemme k = 2 exige le sommet fixe
  (`LEMME_EGALITE_8_SUR_7_C2.txt:203-206`) ; « Un cadre relâché ou une matrice signée N seule ne peuvent pas être exclus par cette
  preuve sans leur raccord au graphe » (`LEMME_EGALITE_8_SUR_7_C2.txt:22-24`) ; T18 utilise lambda = 1 et mu = 2 du vrai graphe,
  d'où « no GRAPH frame », pas « no engine frame » (`BRIDGE.md:348-357`).

Vu par moi (à vérifier avant usage) :
- Les deux matrices M1 = 63 E_{-4}, M2 = 77 E_3 (PSD, rangs 44 et 54) et les budgets de voisins communs n'utilisent pas
  d'automorphisme : ils s'appliquent tels quels à tout ensemble de sommets déterminé d'un srg(99,14,1,2), donc aussi en C1 et en
  C3 ; parmi les tests de rang, seul « rang M1[Y] <= 44, rang M2[Y] <= 54 » (remarque (a) de l'arbitre 2) est indépendant de sigma.
- La borne de rang scindée 22/22 et 27/27 repose sur trace(sigma) = 1 et trace(sigma A) = 14 ; pour un automorphisme d'ordre 3
  il faudrait refaire ce calcul de traces (aucune source lue ne le fait).
- L'égalité somme a_i^2 = E(v) du pont tient parce que 22 + 2 = 24 ; une autre réduction de réseau (autre cas) devra vérifier que
  son cadre engendre l'orthogonal des normales.
- Pour le srg(243,22,1,2) avec x -> -x, le pont donne c = 9, rang du cadre 55 et E = 9N - Y ; `ref_graphs.out.txt:22` signale 72
  petites fonctions propres entières de valeur propre s = -5, de norme carrée 54 (la source ne dit pas si elles sont sigma-impaires).

### Partie C : T20 et les calculs des branches lemma-run

#### (1) Énoncés conditionnels

| Si (X) | alors | statut de X | source |
|---|---|---|---|
| les Calculs 4.12, 7.4, 7.5, 8.8, 8.9, 9.19, 9.20 sont justes | toute configuration est en cas I, n_3 = 2, profil (3,4,0) ou (4,2,1) (Théorème 10.1) | E (deux programmes) | `master:lemma/T20_PROOF.md:2564-2577` |
| de plus le Calcul 9.29 est juste | T20 (Théorème 10.2) | E | `T20_PROOF.md:2579-2583` ; `REFEREE_T20_PROOF.md:235-242` |
| une recherche à rejets exacts n'a pas de nœud de niveau n (règle d'unité quelconque) | aucune configuration n'a cette racine | P | `T20_PROOF.md:1058-1059` |
| un second programme satisfait les conditions 1-4 du contrat | sa conclusion est une recherche complète, indépendante des listes du premier | P | `T20_PROOF.md:1073-1077` |
| sur un ensemble sigma-invariant déterminé, rang G_odd > 22 ou rang G_even > 22 | contradiction | P | `T20_PROOF.md:999-1001` |
| (E14) : toute fonction propre -4 entière sigma-impaire non nulle a norme >= 16 | un couple (k,g) avec 1 <= N(k,g) <= 9 est une contradiction | O dans ce texte | `T20_PROOF.md:2657-2685` |
| les normes duales 5 et 6 sont exclues (min L* >= 8/7) | arêtes croisées forcées ; au plus trois mots avec s_I = 2 ; cas d'égalité | dépend de (E14) | `master:lemma/t20_CODEX/HAND.md:31-86` |
| (E14) | B sans ensemble indépendant de taille 4 (D1) ; w ~ sigma w' forcé (D2) ; type (D3) impossible | dépend de (E14) | `master:lemma/t20_HAND/NOTES.md:209-215` |
| U n V vide et e(U) = 0 pour le type de z | violation PSD explicite (vecteur 7[i dans U] - 2, 7 sur z) | P | `NOTES.md:107-110` |
| n_3 = 0 et e(X_0) = 9 | contradiction (X_2 biparti contre une arête de paire interne) | P | `T20_PROOF.md:1883-1934` |
| profil (4,2,1) | u, u' sans voisin dans R_0 ; (n_3 = 2) beta = 1 | P | `T20_PROOF.md:1819-1821`, `:2320-2336` |
| pour toute base gardée la recherche de la route B / route A ne trouve rien | n_3 = 2 impossible | P | `SPEC_ROUTE_B_N3.txt:141-150` ; `SPEC_N3.md:108-116` |
| T20 (et T18) | les 2,508,295 paires différées sur T20 (5,190,752 sur T18) sont exclues ; avec le pont, les 156 enveloppes | P (pont non lu ici) | `T20_WORK.md:15-18` ; `T20_BOARD.md:46` |
| T18 et T20 | toute racine a \|(r,y1)\| <= 1, \|(r,y2)\| <= 1 (Corollaire Y1) ; 003:181:182 couvert | P | `T20_BOARD.md:55` ; `FINAL_STATEMENT_DRAFT.md:31` |
| T18, T20, pont, certificats, et les conditions de la section 6 | « No strongly regular graph with parameters (99, 14, 1, 2) has an automorphism of order 2 » | brouillon LAB, revu par IA | `master:lemma/FINAL_STATEMENT_DRAFT.md:6-12` |

#### (2) Bornes quantitatives

| Objet | Inégalité ou valeur | Statut | Source |
|---|---|---|---|
| arêtes dans S+ | e <= 1 (e = 1 => Q = 2) ; borne spectrale seule : e <= 3 | P | `T20_PROOF.md:428-434` |
| orbites actives internes | k dans {0,2,4} | P | `:378` |
| degré d hors S | d <= 4 ; d = 4 seulement pour p en cas III | P | `:760-765`, `:779` |
| classes (cas I) | n_0 = 9 - n_3, n_1 = 40 + 3n_3, n_2 = 30 - 3n_3, n_3 dans {0,2} | P | `:771-773`, `:1531` |
| classes (cas II) | n_0 = 4, n_1 = 54, n_2 = 21, X_3 vide | P | `:1318-1319` |
| classes (cas III) | n_2 = 24, n_1 = 48, X_0 = 6 sommets internes | P | `:779-780` |
| voisins dans X_0 | 2\|T\| - 2 <= \|X_0 \\ {p}\| (mot), 2\|T\| - 1 <= \|X_0\| (interne) | P | `:802-808` |
| rang sigma | G_odd, G_even de rang <= 22 ; multiplicités 22/22 sur V_{-4}, 27/27 sur V_3 | P | `:958-982` |
| X_2 (n_3 = 0) | 27 <= e(X_2) <= 35 ; e(X_0) <= 8 ; (4,2,1) : e(X_0) <= 7, e(X_2) <= 34 ; (3,4,0) : e(X_0) pair | P | `:1790-1791`, `:1881`, `:1942-1949` |
| rho(w) (n_3 = 0) | A : <= 4 - h_0 ; W : <= 3 ; Z : <= 2 ; somme 8 - 2h_0 | P | `:1685-1696` |
| s de X_2' (n_3 = 0) | a_2(s) = a_0(s) <= 5 | P | `:1716-1717` |
| z de X_3 (n_3 = 2) | a_2(z) <= 1, \|T\| = 3 + alpha, eps <= 1 | P | `:2208-2211` |
| s de X_2 (n_3 = 2) | a_0(s) <= 4, a_2(s) <= 4 - 2a_3(s) ; rho(w) <= 3 - h_0 | P | `:2274-2286` |
| identités quadratiques | (9.6) = 44 ; (9.8) = 16(9 - e(X_0)) ; (9.11) = 55 - 16eps | P | `:1788`, `:1938`, `:2367` |
| plafonds du programme (n_3 = 0) | A : 4 - h_0 ; W : 8 - h_0 ; Z : min(10, 12 - h_0) ; s : 5 - \|N_p(s) n A_p\| | P | `:2013-2019` |
| plafonds (route B) | s : 4 - 2a_3(s) - \|N_p(s) n A_p\| ; z : 1 - \|N_p(z) n A_p\| ; w : 3 - h_0 - 2a_3, 7 - h_0 - 2a_3, min(11 - h_0 - 2a_3, floor((20 - 3a_3)/2)) | P | `:2430-2436` |
| triangle | \|U\| = 36 (3 x 12), \|Z\| = 60 ; tout sommet de Z a 2 voisins dans chaque groupe | P | `TRIANGLE_REDUCTION.md:16-32` |
| supports | 27720 / 2880 / 0 / 10080 étiquetées ; 9 classes ; ordres 16,4,10,4,4,20 ; 1 ; 3,4 | E | `T20_PROOF.md:587-597` |
| IIa.0 | 180 graphes de types -> 87 bases ; 45,497 nœuds | E | `:1354`, `:1434-1446` |
| III.0, III.1 | 130,004 et 1,628,864 nœuds, aucun nœud de niveau 10 (sur 12) avec rang ; III.1 sans rang : 1 nœud de niveau 10, sans enfant | E | `:1204-1227` ; `VERIF.md:9-13` |
| n_3 = 0 | 17,396,042 N-configurations, 3,130,401 orbites, 615,405 bases, 15,762,181 nœuds ; profondeur <= 5 avec rang (11 ou 12 requis) ; I.1 sans rang : profondeur 6 | E | `:2058`, `:2085-2087` ; `verify_I1_340.out:8` |
| n_3 = 2 route B | 25 types ; 64,528 bases (64,498 classes) ; 86,968 nœuds ; <= 3 orbites placées (8 ou 9 requises) | E | `:2486-2521` |
| route A | 700 classes ; 183 fermées, 96 à la main, 421 ouvertes ; profondeur <= 7 sur 12 ; coût estimé ~1,000 (jusqu'à 2,000) h-cœur par programme ; 1.08 M nœuds/base en moyenne | E / H | `T20_BOARD.md:13` ; `SUMMARY_before.txt:7-10` |
| petites normes duales | plus petit N > 0 : 10, 19, 13 ou 20 sur S ; 10, 12, 19, 13 ou 20 sur S u {z,z'} | E | `NOTES.md:217-219` |
| Codex Prop. 2 | au plus trois mots avec s_I = 2 par famille | P (cond.) | `HAND.md:57-71` |
| nœud de rang de III.1 | 47 sommets, rang impair 23, déterminant 17,341,031,120,896 | E | `VERIF.md:9-11` |
| paires de la route (C) | 2,508,295 en attente de T20 ; 5,190,752 de T18 | E (import) | `T20_BOARD.md:46` |

#### (3) Lemmes ouverts ou étapes manquantes

| Manque | Ce qu'il donnerait | Source |
|---|---|---|
| (E14) (normes <= 14), non prouvé dans T20_PROOF | la règle de norme duale comme filtre exact supplémentaire (Lemme 10.2) ; les propositions de Codex | `T20_PROOF.md:2681-2685` |
| identité globale pour fermer n_3 = 2 à la main | supprimerait la dépendance au Calcul 9.29 | `NOTES.md:351-354` |
| fermeture à la main de IIa (une unité de jeu) | supprimerait les Calculs 8.8, 8.9 | `T20_REPORT.md:105-109` |
| combiner Prop. 2 et comptes d'unités (Codex) | exclusion d'un profil entier à la main | `HAND.md:141-145` |
| test d'isomorphisme indépendant pour 4.12 | complétude des neuf configurations sans l'énumérateur 1 seul | `T20_PROOF.md:2744-2745` |
| G1 : fichiers par base, plans, hachages des sources exécutées | reproductibilité des runs cités | `REFEREE_T20_PROOF.md:64-83` ; `T20_PROOF.md:2729-2739` |
| G2 : relecture de la formulation finale ; contrôles des conditions 2 et 3 | contrat certifié | `T20_PROOF.md:7-10`, `:1106-1107` |
| C3 (bases étiquetées ou non) | rédaction de 8.7 et 9.18 | `T20_PROOF.md:25` ; `REFEREE_T20_PROOF.md:160-165` |
| audit ligne à ligne des moteurs | remplacer l'accord de deux programmes par une preuve | `T20_PROOF.md:2704-2711` |
| explication de l'écart de comptes I.0/I.5 (4,2,1) (vu par moi) | cohérence entre table imprimée et branches citées | L02_C2_aws-218 |
| « B connexe, spectre hors 4 dans [-3,3] » | énoncé du round 1 sans preuve écrite (non utilisé) | `T20_REPORT.md:136` |
| formalisation (Lean) | rien n'existe | `FINAL_STATEMENT_DRAFT.md:114` |

#### (4) Méthodes transférables

- **Boîte à outils T18 -> T20** (dit par la source, `T20_WORK.md:61-72`) : ensembles déterminés agrandis pas à pas ; budgets sur graphes
  partiels ; positivité des deux projecteurs M1 = 63 E_{-4}, M2 = 77 E_3 avec témoins entiers ; borne de rang venant de la dimension 22 des
  espaces propres de sigma ; recherche par unités dont l'exhaustivité ne dépend pas de la règle (Lemme 6.5). Même cadre pour T16, T18, T20
  (`FINAL_STATEMENT_DRAFT.md:124-126`). Vu par moi : la borne de rang ne demande qu'un automorphisme et les traces de P E ; pour un autre ordre
  (C3) les multiplicités des valeurs propres de l'automorphisme sur V_{-4} et V_3 donneraient des bornes analogues (non vérifié).
- **Second programme qui suit un plan, avec contrat et contrôles négatifs** (`T20_PROOF.md:1061-1107`) : vérification bon marché d'une grande
  recherche ; vu par moi, réutilisable pour toute énumération par unités.
- **« N(p) dans la base »** (route B) : la décomposition qui fermait n_3 = 0 à environ 0.3 s par base a fermé n_3 = 2 en ~7 h CPU contre
  ~1,000 h-cœur estimées pour la route A (dit par la source, `T20_BOARD.md:13-16` et `origin/defer-n4:lemma/T20_BOARD.md:14`).
  Leçon de choix de base : mettre dans la base les sommets dont le nombre de voisins dans le support est forcé (un mot a deux voisins dans N(p)).
- **Mesure de coût par échantillonnage** (une tâche sur N sous le niveau 2, `t20_n3_sample.sh:1-8`) avant tout grand run ; a évité un run
  inutile ; vu par moi, transposable.
- **Slots** (Lemme 9.7) : bijection des 84 paires de sommets de N(p) (paires différentes) sur les 84 mots, pour toute involution à un point
  fixe d'un srg(99,14,1,2) ; vu par moi, indépendant de phi.
- **Partition autour d'un triangle** (`TRIANGLE_REDUCTION.md:16-34`) : n'utilise que la régularité forte (dit par la source).
- **Fonction propre auxiliaire psi = 3 * 1_X - A 1_X + 1** pour |X| = 9 (`EDGE_BOUND.md:46-64`) : encode un comptage local, sans lemme de
  petite norme ; la note de travail signale que l'analogue (3I - A + J/9) 1_S demande que 9 divise |S| (`T20_WORK.md:71-72`, dit par la source).
- **Identité des chemins G0, comptages A^2 sur une indicatrice, couplage parfait dans N(v)** : outils exacts qui se transposent du lemme de
  norme 16 (dit par la source, `NOTES.md:255-263`).
- **Règle de norme duale** comme filtre exact pour de plus grands ensembles déterminés, conditionnelle à (E14) (dit par la source,
  `NOTES.md:219-220`).
- **Vérificateur Codex à Schur entier sur base fixe** (pas de flottant), « available for the alternative decomposition including N(p) »
  (dit par la source, `MEASUREMENTS.md:56-59`).
- **Boîte de calcul à usage unique** (push toutes les 10 minutes vers une branche, extinction automatique) (`lemma/cloud/run.sh:1-37`).

### Partie D : réduction, audits, papier

#### (1) Énoncés conditionnels

1. Si σ est un automorphisme d'ordre 2 de Γ, alors σ fixe exactement un sommet (A.0 ; P, Codex) ; AUDIT_REDUCTION.md:56-88.
2. Si (Γ, σ) existe, alors il existe U, l'un des 156, avec un repère vérifiant (R1)–(R8) (Théorème R ; P, Codex) ;
   main.tex:392-424.
3. Si aucun des 156 ne contient de repère (Théorème B ; S, avec composante O), alors aucun automorphisme d'ordre 2 n'existe
   (Thm 1.1) ; main.tex:429-433.
4. Si le Thm 1.1 est vrai et T4 aussi (P, revu à la main selon la transcription), alors EX est faux dans le modèle
   (upstream/README.md:18-19 ; MODEL.md:83-88). Si EX est faux, alors aucune involution n'a un seul point fixe ; avec F0
   (= A.0), il n'y a pas d'involution du tout.
5. Si U contient un repère, alors U est indécomposable (A.9 ; P). Si U est décomposable, il ne contient pas de repère (152, 153).
6. Si U contient un repère et que T16, T18, T20 sont vrais, alors E(v) ≥ 11 pour tout v hors de Π (Cor. 7.2 ; P cond.) ;
   main.tex:535-536.
7. Si U a une racine r avec (r,y) = ±2, alors y n'est normale d'aucun repère, quelle que soit l'autre (Cor. Y1 ; P, conditionnel
   à T18 et T20) ; main.tex:552-555.
8. Si une paire (y1,y2) admet un vecteur d'énergie ≤ 7 (hors Π), ou un témoin W8 (T16), W9 (T18) ou W10 (T20), alors la paire
   n'héberge aucun repère ; main.tex:540-548, 715-720.
9. Si un vecteur caractéristique z de norme 16 a Y = (z,y1)^2 + (z,y2)^2 > 66, alors la paire est exclue (Lemme 6.7 ; P) ;
   main.tex:486-493.
10. Si la somme des 42 plus petits m_j dépasse |R_j|, alors U est exclu ; si les vecteurs duaux courts (< 8/7) d'un réseau
    engendré par des vecteurs admissibles engendrent, avec L^⊥, plus de 2 dimensions, alors U est exclu (Prop. 8.1 ; P) ;
    main.tex:580-592.
11. Si pour un sous-espace V les types de vecteurs de norme 3 forcent Σ_o |P_V uo|^2 > 7 dim V, ou plus généralement si une
    combinaison positive Σ λ_V |P_V u|^2 ≥ c sur tous les types avec 42c > Σ λ_V · 7 dim V, alors il n'y a pas de repère.
    Forme générale du certificat de 143, vue par moi ; la source donne l'instance λ_W = 4, λ_l = 16, c = 9 (LATTICE_143.md:55-57).
12. Si U' (jumeau par R = [[2,2],[−2,2]]) a strictement plus de racines que U, alors la paire est réglée par induction descendante
    sur le nombre de racines (P, Codex). Si U' a le même type unique avec une clé strictement plus petite (vérifiée exactement),
    alors la paire se réduit à son image. Si toutes les cibles possibles ont des exclusions fondées indépendamment dans un graphe
    acyclique, alors la paire est exclue (REFEREE_TWIN_DEPENDENCIES.md:10-51).
13. Si l'on recertifie les au plus 2 479 669 paires des formes (a) et (c) sans statut ni flottant, alors la dernière réserve de
    calcul du papier est levée (main.tex:891-893, 994-995).
14. Si les comptes de vecteurs distincts exactement acceptés satisfont E4 + 24E2 + 24E3 = 196560, alors les trois listes sont
    complètes (P) ; REFEREE_SHELL_COUNTS.md:42-55.
15. Si les nombres de Coxeter des deux voisins pairs diffèrent (H1 ≠ H2), alors aucun h de norme 4 n'a une empreinte nulle sur
    les nouvelles racines (P, LAB, algèbre vérifiée par Codex) ; AUDIT_ENGINE_RULES.md:164-173.
16. Si (A) à (E) sont vrais, alors G est trivial (P, Codex : « valid conditional ») ; asymmetric.tex:47-55. Sans ordinateur
    (MM04, CW25, D3, D7), on a |G| ∈ {1,2,11} ; asymmetric.tex:99-103.
17. Si 7 divise |G|, alors G ≅ Z7 ; si |G| est pair, il divise 6 (CW25, publié) ; main.tex:96-97. Si |G| est pair, il divise 42
    (MM, Mak) ; main.tex:94.

#### (2) Bornes quantitatives

- **Point fixe :**
  - f = 1 ;
  - s_p + t_p + 2r_p = 7 et f = 1 + 2s_p^2 + 2r_p ;
  - a1 + n2 ≤ 99 − f ; Σs_p ≡ 0 (mod 3) ;
  - (3f − a1 + 11)/7 ∈ Z ;
  - valeurs propres de A : 14, 3, −4, de multiplicités 1, 54, 44 ; de S : 3 (×27) et −4 (×22). (A.0 ; main.tex:86, 196-244.)
- **Réseau du repère :**
  - g pair, g ≤ 20 ; det K = 7^g ; groupe discriminant F7^(22−g) ;
  - det Nmax = 49, avec un indice 7^(m−1) sur N ;
  - s = 497 − 4M ≡ 1 (mod 8), (c,c) ≡ 6 (mod 8). (A.4.)
- **Minimum dual et énergie :**
  - min K ≥ 8, min N* ≥ 8/7 (A.5) ;
  - E(v) ≥ 8 (R-vi) ; avec T16, E ≠ 8 (« 9/7 ») ; avec T16 à T20, E ≥ 11, soit une norme au carré ≥ 22 pour les fonctions
    propres (main.tex:986-987).
- **Pièges et filtres :**
  - racines : Y ≤ 6 et Y ∈ {0,1,2,4,5} ; |(α,y)| ≤ 2, puis ≤ 1 avec Y1 ;
  - norme 3 : Y ≤ 13 (hauteurs ≤ 3, pas les deux égales à 3) ;
  - nouvelles racines : |(β,y)| ≤ 3/2 (pas les deux égales à 3/2) ; |(β,hc)| ≤ 1 ; w(β) ∈ {1,3} ;
  - z caractéristique de norme 16 : Y ≡ 2 (mod 8), E(z) ≥ 46, Y ≤ 66 ;
  - Y = 58 : 4Σa^2 + Σ(b^2 − 1) = 12 ; Y ≥ 50 : 70 − Y ;
  - énergie normale des racines ≤ 3·rang. (AUDIT_REDUCTION.md:192-197, 241-244 ; AUDIT_ENGINE_RULES.md:49-62, 80.)
- **Couches des réseaux impairs de rang 24 sans norme 1 :**
  - N4 = 196560 − 24N2 − 24N3 ; N3 = 4096 ; N4 = 98256 − 24N2 ;
  - N5 = 276N3 ; N7 = 11178N3, soit N7/2 = 22 892 544 lignes ;
  - nouvelles racines (signées) = N2 + 48 ; 2048 classes de norme 3 au signe près ;
  - contrôle : D12+⊕D12+ a N4 = 85 584. (REFEREE_SHELL_COUNTS.md:34-74 ; theta_odd24.py:5-15.)
- **143 :**
  - 312 racines (72 + 240) ; (z,z) = 144 ; [U : M + Zz] = 144 ; |t| ≤ 20, 41 hauteurs ;
  - 4096 = 2688 + 1120 + 288 ;
  - c ≤ 28 ; 63/8 > 7 ; 378 ≤ 336 (contradiction) ;
  - test d'empilement : m = 0, 16, 6, contre 72 nouvelles racines. (LATTICE_143.md.)
- **Empilement (somme des 42 plus petits m contre capacité) :**
  - 094 : 84 > 80 ; 128 : 84 > 64 ; 129 : 84 > 64 ; 133 : 168 > 128 ; 136 : 84 > 48 ; 142 : 168 > 128 ; 144 : 168 > 104 ;
  - 147 : 84 > 32 ; 148 : 168 > 64 ; 150 : 168 > 64 ; 151 : 336 > 128 ; 152 : 672 > 256 ; 154 : 252 > 48 ; 155 : 672 > 128 ;
  - non exclus par (a) : 117 (0 ≤ 128), 134 (84 ≤ 128), 145 et 146 (0 ≤ 0) ;
  - dimensions des pièges duaux : 8, 9, 8, 24 > 2. (INDEPENDENT_PACKING.md:77-110.)
- **Comptes de la campagne :**
  - table : 593 699 707 paires, dont 25 775 627 par recherche, 5 190 752 via T18 et 2 508 295 via T20 ;
  - 102 réseaux : 592 864 217 paires ; 91 réseaux : 220 260 576 ; 13 réseaux : 373 439 131 ;
  - 000 : 141 classes ; 004 et 010 : 420 345 paires ; 29 réseaux : 6 713 853 paires (tableau 2, main.tex:781-787).
- **Transferts :**
  - 1 300 094 (statut) + 32 265 417 (plus de racines) + 2 863 005 (même réseau) ; 1 622 dépendances sans cycle ;
  - résidu ≤ 2 479 669 paires (11 234 représentants) ; 42 276 des 54 096 y1 sont tués par Y1 ;
  - lot 713 : 60 308 = 59 697 + 428 + 183. (main.tex:747, 881-891 ; REFEREE_TWIN_DEPENDENCIES.md:156-160.)
- **Audits :**
  - H2 : 147 475 940 paires lues, 10 267 sans point flex, 8 432 exposées, 0 non ré-exclue ; 129 réseaux sans empreinte nulle
    possible ;
  - H1 : 17 676 + 356 + 57 fichiers recensés, 12 exclusions au stade joint à liste vide ;
  - H4 : 12 620 paires « pair budget » ; 105 : 6 310, puis 56 544 relancées ;
  - H3 : 468 bornes ≤ 2 928 240 < 2^63 ;
  - T16 : 240 + 32 obstructions ; T20 : 1,58·10^7 nœuds depuis 615 405 configurations.
- **Groupe :**
  - |G| divise 2·3^3·7·11 ; s'il est pair, il divise 42 (MM, Mak) ou 6 (CW) ;
  - |G| ∈ {1,2,3} selon les résultats publiés ; {1,2,11} sans ordinateur ; {1} avec tous les ingrédients.
- **Coût :**
  - recertification : au moins ~100 cœur-heures, probablement plusieurs centaines ;
  - campagne : ~6 700 h écoulées, plus 8 001 tâches totalisant 1 058 heures-travailleur.

#### (3) Lemmes ouverts et étapes manquantes, avec ce qu'ils donneraient

- **Recertification des transferts (a) et (c)** (≤ 2 479 669 paires) : elle fermerait l'unique réserve de calcul du papier
  (main.tex:994-995).
- **Recomptage exact des racines jumelles pour (b)**, ou une borne inférieure certifiée : il rendrait (b) indépendant du flottant
  (main.tex:884-885 ; REFEREE_TWIN_DEPENDENCIES.md:20-24).
- **Énumérateur indépendant sur les 152 autres réseaux, réduction de diagramme comprise** : il lèverait la « main reservation »
  (main.tex:899-903).
- **Second programme de recherche, ou certificats de recherche** : ils couvriraient les ~2,6·10^7 paires S (main.tex:931).
- **Certificats z des 1 610 témoins caractéristiques** : ils rendraient exact le compte 1 042 (REFEREE_TWIN_DEPENDENCIES.md:179-180).
- **Précondition du noyau rigide (H2)** : le lemme de Coxeter la règle pour 129 réseaux. Pour les 27 autres, la forme générale
  (« a genuine completion cannot have remaining h with zero footprint ») n'est pas prouvée. Elle n'est levée que par l'audit de
  couverture, au niveau des archives (AUDIT_ENGINE_RULES.md:157-162, 243-245).
- **Formalisation** : 378 ≤ 336 (avec la table de types), le Cor. Y1, A.0, A.5, puis la réduction, avec Borcherds et T16 à T20
  en hypothèses nommées (LEAN_FEASIBILITY.md:23-57).
- **Contrôle de masse des 156** : il donnerait un contrôle indépendant du nombre 156 (AUDIT_REDUCTION.md:302-303).
- **Ouverture de BL11 et de la thèse de Behbahani** : elle ferait de (D) et (E) des lectures directes (REFEREE_PAPER:163-167).
- **Preuve sans ordinateur du Théorème B** : inconnue (main.tex:985).
- **Extension des lemmes T au-delà de E = 10** : selon la source, chaque pas « would shorten the searches » ; T16 à T20
  « exclude seventeen more lattices » (main.tex:987-988).

#### (4) Méthodes transférables

1. **Identité de budget d'un repère serré, Σ_f |P_V f|^2 = 7 dim V, combinée à une table de types des vecteurs courts.**
   - Elle donne un certificat linéaire rationnel (378 ≤ 336) sans recherche.
   - Dit par la source : c'est la première cible Lean (LEAN_FEASIBILITY.md:25-32) et « the u alone suffice »
     (LATTICE_143.md:69-70).
   - Vu par moi : applicable à tout problème « repère de normes connues dans un réseau à recollement explicite ». C'est le cas
     des autres réseaux de C2 encore traités par recherche, et de tout modèle de réseau de C1 ou C3 qui aurait une identité de
     repère.
2. **Description par recollement des tranches** (U/(M + Zz) cyclique ; m(t) = Σ minima de classes + t^2/(z,z)).
   - Elle donne la complétude d'une couche sans énumérateur ni compte thêta (REFEREE_143_PROOF.md:93-116 : « This proves
     completeness from the lattice glue »).
   - Vu par moi : transférable à tout réseau dont le complément des racines est de petite dimension.
3. **Lemme de complétude jointe par identité linéaire entre comptes** (déficits pondérés de somme nulle).
   - Dit par la source pour les couches 2, 3, 4.
   - Vu par moi : toute énumération exhaustive avec une identité thêta (couches de normes 5 et 7 via N5 = 276N3 et
     N7 = 11178N3, déjà utilisée pour F4) peut être certifiée ainsi.
4. **Réseau des vecteurs propres entiers d'une matrice entière, plus formule d'oddité, plus forme discriminante sur F_p**
   (A.4). C'est la méthode qui donne la classe de Witt sans connaître g.
   - Vu par moi : la parenté avec D3 est réelle : « two lattices of eigenvectors must have determinants congruent modulo 3 »
     (asymmetric.tex:68-70).
   - Pour C1, l'analogue serait le réseau Z^99 ∩ E_{−4} (rang 44). Les sources lues ne l'examinent pas.
5. **Double comptage des voisins communs pour les petites fonctions propres entières**, D = m(m−7) − 7e − Σd_i^2 ≥ 0 (A.5).
   - Dit par la source : T16, T18 et T20 « follow the scheme of Proposition 5.2 » (main.tex:521-522).
   - Vu par moi : utilisable pour toute borne de « norme minimale d'un vecteur propre entier », dans C1 ou C3.
6. **Intégralité de la trace d'un automorphisme sur un espace propre**, (3f − a1 + 11)/7 ∈ Z, ou (4f + a1 − 18)/7 chez MM.
   - Dit par la source : c'est le dispositif de MM04, p. 100 (EDITORIAL:174-175).
   - Vu par moi : il s'applique à tout ordre premier (comptes de points fixes d'ordre 3 ou 7).
7. **Critère d'empilement par frappes disjointes de nouvelles racines, et piège dual à 8/7.**
   - Dit par la source : il n'est pas trouvé dans CS90 ni dans Borcherds ch. 17 (EDITORIAL:178).
   - Vu par moi : il dépend seulement des nouvelles racines et du minimum dual ; il se transfère à tout cadre « repère dans un
     réseau impair de rang 24 ».
8. **Identité des nouvelles racines** Σ_β (β,h)^2 = 8(H1+H2) − 4Σ_j h_j ||P_j h||^2, en fonction des nombres de Coxeter des
   voisins pairs (AUDIT_ENGINE_RULES.md:166-170). Vu par moi : c'est un fait général sur les réseaux impairs unimodulaires de
   rang 24, réutilisable.
9. **Exclusion au niveau d'une seule normale** (Cor. Y1 : une racine de produit ±2 suffit).
   - Dit par la source : elle retire 42 276 des 54 096 y1 et 9 143 des 10 802 y1 sans relance (main.tex:889-891 ;
     B_LATTICES.md:88-93).
   - Vu par moi : c'est le modèle de toute réduction « à normale fixée » dans les recherches de paires.
10. **Indécomposabilité forcée par la connexité du graphe de Gram du repère** (A.9). Vu par moi : générique pour les repères dont
    l'identité T^2 + T = 12I − C^tC relie toutes les orbites.
11. **Formule de rang entière r = 4m/(n1 + 4) pour reconnaître un système ADE sans flottant** (REFEREE_TWIN_DEPENDENCIES.md:61-91).
    Dit par la source pour les jumeaux ; vu par moi : réutilisable partout où l'on classe des systèmes de racines.
12. **Contrat de certificats et d'hypothèses nommées pour Lean** (LEAN_FEASIBILITY.md:49-74 ; dit par la source en termes
    généraux) : architecture valable aussi pour C1 et C3.

### Partie A : matériau C1 hébergé dans le dépôt

#### (1) Énoncés conditionnels « si X alors … exclu / contradiction »

| # | si X | alors | statut de l'implication ; statut de X | source |
|---|---|---|---|---|
| 1 | le lemme des graines (≤ 13 configurations) et a₈ ≥ 96 526 tiennent | r = 33 impossible sauf vecteur de Fano | P non relu ; dépassé (r = 33 exclu autrement) | H:1229-1235 (L02_C2_aws-276) |
| 2 | UNE de : 2a₈ + 16a₉ + a₁₃ < 2632 ; b₂ < 914 ; b₃ < 6 696 790 | rang 43 exclu | E (formules reproduites par Codex) ; X ouvert | H:1351-1352 (L02_C2_aws-294) |
| 3 | il n'y a aucune 22-coclique | a₇ = 0 à tout rang (~2 M de moins au plafond du rang 37) | P non relu ; X ouvert « high value » | H:1383-1384 (L02_C2_aws-299) |
| 4 | une exclusion du rang 43 n'utilise que le genre, les vecteurs de M et les vecteurs courts de L1 | elle exclut aussi 37, 39, 41 | P non relu | H:1447-1448 (L02_C2_aws-310) |
| 5 | les collisions (paires jumelles de supports spéciaux d'ordres 8 et 9) sont maîtrisées | rang 37 meurt d'un facteur 2,3 à 3,9 | E (labo) ; X : comptabilité ensuite close pour ≤ 9 | H:1316-1318 (L02_C2_aws-289) |
| 6 | τ_grid tombe à ~1000 (droites dans ≤ 3 grilles) | budget de collisions suffisant | E (labo) | H:1449-1451 (L02_C2_aws-311) |
| 7 | τ ≤ ~860 (aucune droite dans 4 grilles) | route collisions paire par paire conclut | E ; route close comme méthode | H:1471 (L02_C2_aws-314) |
| 8 | aucune droite dans 4 ou 6 grilles | τ_grid ≤ 693 | E (labo) ; X global, ouvert | H:1594-1595 |
| 9 | le nombre TOTAL de paires jumelles < ~540 (~700 si toutes sont des paires de grilles) | rang 37 exclu (avec les plafonds de Codex) | E (labo) ; X ouvert | H:1642-1643, 1659-1660 (L02_C2_aws-333, L02_C2_aws-335) |
| 10 | 27 828τ_g + 31 976τ_n + (canaux non comptés) < 17,1 M, c.-à-d. τ_g < 614 sans paire non grille, ou ρ ≤ ~58 | rang 37 exclu | E (PL flottant du labo, NOTE 17.49) | H:1681-1683 (L02_C2_aws-338) |
| 11 | les seules relations mod 7 entre [1_G], [1] sont celles des pinceaux (+ « une droite non hub par un point à h hubs est dans ≥ h grilles », h ≤ 4 ou 3) | ρ ≤ 18 + x₆, τ_g ≤ 702 / 567 / 509 : rang 37 exclu | X : hypothèse FAUSSE (relations en un sommet) | H:1688-1694, 1709-1716 (L02_C2_aws-340, L02_C2_aws-341) |
| 12 | c relations au-delà des pinceaux (ρ ≤ 18 + c + x₆) | c = 0 : τ_g ≤ 388 ; c = 10 : 608 (16,92 M < 17,1 M) ; c = 12 : 655 (insuffisant) | E (labo 17.50) ; inutilisable tel quel (max τ_g = 1331 avec les relations de sommet) | H:1707-1708, 1715 |
| 13 | à P = 0, les masses de collision 7 à 9 sont bornées | rang 37 exclu (marge ~16,7 M contre canaux 1e5-1e6) | E (labo) ; X ouvert (demandé à Codex) | H:1992-1993 (L02_C2_aws-380) |
| 14 | P plafonné (niveau masse 6 seul) | rang 37 ⇒ P > ~285 | E (labo, relais) | H:1994 (L02_C2_aws-380) |
| 15 | G(T) connexe, 7 ∤ τ, et D ≠ 0 entre deux complétions de même (boule, ombres) | r + r′ ≥ 78 ; en particulier aucune seconde complétion de rang 37 ou 39 d'un candidat de rang 37 | P (LAP), non relu par un tiers | M:94-108 (L02_C2_aws-388) |
| 16 | D² ≡ 0 mod 7 et profils des sommets modifiés distincts (automatique si chaque sommet modifié a ≥ 3 voisins non modifiés) | D = 0 ; au rang 37 générique, complétion unique parmi tous les rangs | P (Codex), relu par LAP | M:114-124 (L02_C2_aws-390) |
| 17 | les ordres d'automorphisme 2, 3, 7, 11 sont exclus (programme C2/C3 etc.) | au rang 37 générique (boule, ombres) est sans symétrie (corollaire 8) | P conditionnel | M:36-37, 110-112 (L02_C2_aws-389) |
| 18 | (boule, 60 ombres) au rang 37 générique doit avoir une symétrie, ou ne pas exister | les droites génériques au rang 37 sont exclues | ni l'un ni l'autre démontré | M:197-200 |
| 19 | aucune différence D de rang ≤ 4 (Codex 233) et bloc proche inversible | (39,39) fermé ; au rang 39 générique toute symétrie de (boule, ombres) se prolonge | E annoncé, non relu | M:126-131 (L02_C2_aws-391) |
| 20 | les espaces colonnes de Y et Y′ sont orthogonaux | l'argument du laplacien s'applique encore aux paires r + r′ ≥ 80 | P (remarque) | M:135-136 (L02_C2_aws-392) |
| 21 | une borne uniforme 2288 sur les configurations (1⁷ ; (−1)²⁹) à support positif indépendant | S₀ entièrement exclu (Codex : S₀ exige ≥ 2289 + 15g) | P (Codex, relayé, non vérifié par LAP) | M:601-603 (L02_C2_aws-421) |
| 22 | toutes les couches fractionnaires de S₀ divisibles par 3, ou toutes celles des classes 1, 2, 4 | S₀ incompatible | E (hypothèse purement arithmétique) | M:653-654 (L02_C2_aws-427) |
| 23 | au rang 43, κ = g_v = u = c₁ = s₄₄ = 0 dans S₀ | contradiction (congruence mod 3) | E | M:783-787 (L02_C2_aws-432) |
| 24 | au rang 43, aucun objet bas des six types (g_v, u, g_ℓ, c₁, w, s₄₄) | ni norme 14 ni norme 16, au plus une paire ±y de norme 18 ou 20, et « P3/N25 + vecteurs courts » pondéré = 10 | E (identité exacte) | M:757-759 (L02_C2_aws-431) |
| 25 | au rang 43, seules les normes 18 et 26 sont présentes | chaque classe de norme 26 a 329 + 7b₁ − 8(x₁ + x₂) vecteurs ; x₁ + x₂ ≤ (329 + 7b₁)/8 ; sans racine la norme 26 est présente | E | M:445-447 (L02_C2_aws-411) |
| 26 | au rang 43, une seule des normes 16..24 est présente | ses quatre classes ont des effectifs (u, v, v, u) | E | M:443-444 (L02_C2_aws-411) |
| 27 | au rang 43, aucun vecteur de norme 16 à 24 | somme vectorielle nulle dans chaque classe non nulle, pour chaque norme ; et (Codex) pas de racine, donc S₀ | E ; partie Codex relayée | M:466-467, 492-493 (L02_C2_aws-413, L02_C2_aws-415) |
| 28 | S₀ sans sommet fantôme | ≥ 2289 vecteurs de classe 2, norme 40/9, à support positif indépendant, dont ≥ 2001 de profil (1⁷ ; (−1)²⁹) | E | M:559-566 (L02_C2_aws-419) |
| 29 | une famille de grilles re-réglées comme au 243, chaque sommet touché dans g grilles par une même droite | g ≥ 3 ; donc pas de tel mouvement sous P = 0 | P | M:156-164 (L02_C2_aws-394) |
| 30 | rang 37 et G(T) sans triangle ni 4-cycle | G(T) connexe | E (assisté par ordinateur, audit partiel) | G:8-18 (L02_C2_aws-364) |
| 31 | rang 37, P = S = 0 (avec notes 125, 126) | toute droite est connexe ; « (6,6) partout » n'arrive pas | E + notes de septembre non re-démontrées | G:17-18 (L02_C2_aws-364) |
| 32 | rang 37 et aucune arête de T dans un prisme | G(T) connexe (énoncé B) | O (incomplet) | G:133-136 (L02_C2_aws-377) |
| 33 | six paires parmi l₁..l₄ et trois paires parmi l₅..l₇ engendrent des grilles en p₀ | aucun vecteur de norme 16 positif en p₀ (lemme N16) | P relu par le labo | H:1512-1517 (L02_C2_aws-319) |
| 34 | deux vecteurs de norme 18 sur une graine, racine (2,1,1), même c manquant, rien d'autre partagé que ω | au plus UN second vecteur | P non relu ; sous-cas ouverts | H:1263-1267 (L02_C2_aws-282) |
| 35 | l'échelon d'un prisme engendre des grilles avec tous les autres aux trois points d'une droite dans six grilles, et un point a un second tel échelon | aucune grille de plus de ce type (rang 37) | E (Codex, mineurs d'ordre 20, en certification) | H:1648-1652 (L02_C2_aws-334) |
| 36 | motifs (2,2,1) ou (2,2,2) de droites-hubs aux trois points d'une droite dans six grilles | impossibles au rang ≥ 37 (Gram de rang 23 ou 24) | E (Codex 202, 203, « certified without solver ») | H:1684-1686 (L02_C2_aws-339) |
| 37 | colonnes canoniques : toute colonne dans 4 grilles en deux des trois points, ou dans 3 grilles aux trois points | rang 24 / 21 à 24 : impossible au rang 37 | E (modèle canonique seulement) | H:1624-1626 (L02_C2_aws-331) |
| 38 | un point a trois droites dans six grilles aux trois points d'une droite dans six grilles | impossible au rang 37 ((33, 24 à 27)) | E (labo) | H:1639-1640 (L02_C2_aws-333) |
| 39 | r ≤ 31 | une droite dans six grilles est exclue (Hermite) | E (inutile, r ≥ 37) | H:1600-1601 (L02_C2_aws-328) |
| 40 | au rang 39, droite générique | résidu de rang 2 anisotrope ssi τ(G(T)) résidu quadratique mod 7 | P non audité | H:1923-1924 (L02_C2_aws-363) |
| 41 | au rang 37, droite générique | tout vecteur entier lointain à sommes d'ombres nulles de norme < 26 est un vecteur propre global (pas deux k-ensembles disjoints de même somme d'ombres, k ≤ 5) | P (filtre) | H:1737-1739 (L02_C2_aws-344) |

#### (2) Bornes quantitatives

| objet | inégalité / valeur | statut | source |
|---|---|---|---|
| r = rang₇(A − 3I) | r ≥ 33 → r ≥ 35 → r ∈ {37, 39, 41, 43} | C / C / E | H:1222-1224, 1239, 1273-1274 |
| min(L1) | ≤ 16 / 20 / 24 / 26 pour r = 33 / 35, 37 / 39, 41 / 43 ; r = 35 : ≥ 994 vecteurs de norme ≤ 18 ; r = 43 : ≥ 165 de norme ≤ 26 | C | H:1224-1225, 1241-1242 |
| norme minimale d'un vecteur propre 0/±1 sans σ | ≥ 14 ; famille : m ≥ 1 + u(u+1)/2 | P | H:1183, 1187 |
| a₇ (Fano) | ≤ 7 920 (graine) ; ≤ 990 (tassement) ; ≤ 842 (recensement) ; a₇ + 4b₁ ≤ 990 ; ≤ 347 au sommet riche en grilles ; ≤ (2/21)N(F10) | E / P / E / P / E / E | H:1228, 1275, 1360, 1324, 1509, 1501 |
| a₈ (norme 16) | r = 33 sans Fano demande ≥ 96 526 ; ≤ 90 090 (lemme des graines 13, dépassé) ; 7a₇ + 8a₈ ≤ 55 440 | E / P / P | H:1227, 1234, 1258 |
| a₉ (norme 18) | ≥ 166 / 1 030 / 7 074 / 49 392 pour r = 43 / 41 / 39 / 37 (ou 14 à 21 fois plus de normes 16..26) | E | H:1260-1262 |
| vecteurs de norme ≤ 26 à r = 35 | ≥ 5,9 millions | E | H:1262 |
| vecteurs non racines | (a₇ − b₁) + a₈ + a₉ ≤ 2(2^(44 − b₁/2) − 1) | P | H:1321 |
| racines par sommet | ≤ 6 droites de racines ; avec 6, tout autre vecteur de norme < 63 s'y annule ; avec 5, ≤ 2 autres graines | P | H:1322-1323 |
| b₁ (racines de M) | ≤ 88 → ≤ 78 → ≤ 44 (tout rang) | P | H:1323, 1388 |
| b₂ (norme 4 de M) | ≥ 462 + 42b₁ ; ≥ 462 + 41b₁ + b₁²/2 ; rang 43 : ≥ 914 (≤ 376 369), ≥ 922, ≥ 968, ≥ 913 ; S₀ : = 1000 ; ≥ 452 / 460 / 506 non triangulaires | P / P / E / P / P / E | H:1325, 1373, 1348, 1389 ; M:332, 449 |
| b₃ | ≥ … + 1071b₁ ; rang 43 : ≥ 6 696 790, ≥ 7 073 772, S₀ : = 10 648 712 ; rang 37 : ≥ 45 898 (Codex) ; min 24 948 (neuf classes) ; a₁₃ ≤ 3e5 ⇔ b₃ ≥ 141 800 | P / E | H:1325, 1348, 1497, 1467 ; M:332, 449, 1118 |
| b₄ | rang 37 : cible ≥ 16,5 M ; démontré ≥ 3 371 634 ; max 15 979 604,0 ; b₄ ≤ 15 972 863,3 (Codex) ; rang 41 : ≥ 474 941 774 | E | H:1276-1277, 1422, 1497 ; M:331 |
| plafond couplé rang 37 | b₄ + (651/34)b₃ ≤ 17,40 M ; max 16 950 588,3 ; 17 398 653 → 17 048 350 (racines) ; 15,20 M au sommet riche en grilles ; 12,09 M avec a₇..a₁₀ = b₁ = 0 ; leviers 15,58 / 15,62 / 13,40 / 10,99 / 14,09 M | E | H:1316, 1423, 1326, 1509, 1549, 1423-1425 |
| b₅, b₆ (rang 37) | 1,27e9..1,57e9 ; 6,37e10..6,80e10 | E | H:1465 |
| vecteurs de norme 28 de L1 (rang 37) | ≥ 5 013 138 | E | H:1469 |
| rang 43 (polytope à six paramètres) | a₈ ≤ 2117, a₉ ≤ 8498, a₁₃ ≤ 283 409 ; plafonds seuls a₈ ≤ ~610, a₉ ≤ ~500 | E | H:1348, 1353 |
| familles de représentants | (6,3) ≥ 10 336 557 ; classes partagées avec (6,3) ≤ 1 663 200 + 72P ; différences de triangles lointains 7392 − 2P (4 collisions par paire jumelle) ; recensement dual 39,7 à 66,6 M ; réservoir 25,59 M (≤ 9), 41,3 M (≤ 10) ; R = 32,43 M | E / P | H:1278, 1289-1290, 1305, 1317, 1567-1568, 1561 |
| triangles lointains d'un prisme | F = 40 − n₃ − 3n₄ − 6n₅ − 10n₆ ≤ 12 ; 4τ ≤ #(prisme, triangle lointain) ; p ≤ 12 prismes par triangle | P | H:1356-1358, 1214 |
| τ (paires jumelles) | τ ≤ (P − 6ρ) + Σ C(g,2), g ∈ {0,1,2,3,4,6} ; non-grille ≤ 2 jumeaux ; τ ≤ 1403 → ≤ 1354 ; τ_grid ≤ 11ρ + 17 ; τ_g(ρ) : 1354,9 à ρ = 126, 515 à ρ = 50 ; max τ_g = 1331 (comptage avec relations de sommet) | P / E | H:1430-1432, 1497, 1716, 1683, 1715 |
| P, ρ | P + 5ρ ≤ 1386 ; ρ ≤ 1330 (méthode polynomiale) ; ρ ≤ ~1500 (Frankl-Wilson) ; ≤ 11 grilles indépendantes, ≤ 8 paires jumelles indépendantes par la disjonction seule ; coin dangereux P = 852, τ ≈ 1900 | E / P | H:1497, 1645, 1670-1671, 1359 |
| collisions de masse six par paire de grilles sur une droite | ∈ [14 430, 27 828] puis [16 496, 27 828] ; budget ~17 900 / 19 600 / 19 728 (dépassés) ; point mort ~26 300 puis ~13 900 ; égalités ≤ 12 674 (14 426 non grille) contre ≤ 7 447 abordables ; 25 201 à ρ = 0 contre 31 976 ; masse 8 (C14) ≤ 64 par paire | E | H:1498, 1510, 1499, 1509, 1534, 1550, 1562, 1574-1577, 1579 |
| rangs de Gram mod 7 | ≤ 45 − r sur L1 (2, 4, 6, 8) ; ≤ 56 − r sur les vecteurs du noyau (19, 17, 15, 13) ; si V engendré par une famille, rang ≥ 2 dim V − 19 ; à r = 41 ≤ 50 classes de Fano orthogonaux | P | H:1491, 1617-1618, 1700, 1492 |
| rangs de grilles | par un point : 6, 10, 13, 15 (≤ 15) ; autour d'une droite dans six grilles : 24 / 21-24 (impossibles), 21 grilles de rang 18 ; ≤ ~21 grilles de plus, ~123 paires ; formes à hubs (15,13), (24,18-20), (33,24-27), (18,15), (30,24), (42,33) ; 108 extensions : 6 de rang 20, 102 de rang 21 ; rang centré en un sommet : 4 à 14 | E | H:1622-1627, 1640-1641, 1650, 1730 |
| vecteurs du noyau | plus courts vecteurs vus de Λ = L₃ ∩ 7L₃* : norme 42 ; deux différences de jumeaux de même classe ⇒ produit ≤ −9 | P | H:1664-1665 |
| droite dans g grilles | réseau de rang 31 / 21 / 13 ; dét = 324·5¹²·7^(r−32)/t² (g = 6) ; Hermite : norme ≤ 28 / 30 / 38 | E | H:1598-1600 |
| droite connexe | τ(G) = (9/4)7^(37−r)t²dét(L_far) ; dét(4I + A_G) = (256/5)7^(38−r)t′²dét(K(F)) ; 9 ∣ τ ; 16 ∣ dét(4I + A_G)/112 ; τ ~ 2,4e12 ; normes de Green 37/12, 1/12, 138/35 ; bloc d'étoile de rang ≤ 8 ; τ·dét(Σ_X) = 7^(45−r)(3t·idx/2)² | P / E | H:1735-1736, 1752-1755, 1778-1780, 1828 |
| ombres candidates (boules aléatoires) | ~25 000 par point ; 3 516-3 731 de norme 6 mod 7 ; ~3 400 par arête croisée, 324-468 passant ; 0,164 des paires ; (a) garde 86-95 % ; (b) 0,164 → 0,102 ; énergie min 1,87-2,02 (borne 3,083 ; ~1,62) | E | H:1791-1793, 1843-1850 |
| réseaux locaux en un sommet | dét Λ = 2²¹3⁸5⁶ ; dét L_v = 2²¹7^(r−15) ; dét K_v = 3⁸5⁶7^(r−15) ; M_v : dét 2²¹7^(45−r) ; [Λ : L_v + K_v] = 7^(r−15) ; ~1,2 et ~0,7 vecteurs attendus sous les minima à r = 37 | P / H | H:1899-1909, 1916-1917 |
| 22-coclique et son réseau Λ | b ≤ 14 ; c ≤ 1, b = 43 − r ou 45 − r ; b = 2 au rang 43 ; forcés à b = 2 : 13 953 / 4432 / 1263 / 206 vecteurs de norme 4 pour d = 0..3 ; b = 2 ⇒ ~14 000 ; min 6 ⇒ b ∈ {6,8,10,12} ; intersections de deux 22-cocliques au rang 43 : 1, 8, 15 ; 44 vecteurs de norme 28 par coclique ; S₀ : κ ≤ 3 ; rang 37 (neuf classes) : ≤ 93 696 | E / P | H:1394-1399, 1405-1409, 1382, 1375 ; M:511, 457 |
| composantes de lignes (comptes exacts) | 2 droites/couche : 50 formes, 18 types (7 sans type I) ; 3 : 34 640, 886 types (15 + 219 + 652), torsion 172/60/1/1 ; 4 : 109 780 368, 81 959 types ; 288 formes, 7 types (maille 5), 144 de torsion 1, 24 de torsion 3, 612 triplets | E | H:1973-1979 ; G:38-40, 99-100 |
| balayages rang 37 | (3,3) maille 5 : 33 784 128 → 12 236 366 → 25 588 → 44 → 0 ; recherches 192 / 48 / 48 / 288 ; (2,2,2) 275 ; (3,3) 2887 / 1910 / 4140 / 720 / 4032 / 9726 ; ~5,2e8, ~1,6e9, 6,57e9 nœuds ; (2,4) : 97 896 boules (16 516 à torsion) au lieu de 245 877 (40 761) ; 81 380 + 19 + 71 + 794 mortes ; manquent 12 670 + 147 boules et 17 tests | E | G:84-87, 72-77, 128, 153-161, 190, 170-171, 229-239 ; H:1944 |
| boules et coût | ~1e8 (droite dans une grille) ; ~2e11 connexes ; 1,9e11 types, 1,4e10 sans prisme connexes ; ~1e10 ; 10⁶ nœuds par étoile ; 5 à 50 années-cœur ; réduction ~1e4 nécessaire | H | H:1950-1951, 2018 ; M:228-231 ; G:198 |
| mouvements (Mandat C) | bloc orthogonal non permutation : |C₀| ≥ k/2 + 2 (9 pour 99, 13 pour 243) ; lignes de D : ≥ 3 (+1) et ≥ 3 (−1) ; rang₇(D) ≤ r + r′ − 74, r + r′ ≥ 78 ; restants : rang de D jusqu'à 6 / 8 / 8 / 10 / 12 ; 243 : D³ = 45D, 80 grilles, 720 arêtes ; droites lointaines 32 − t, ≤ 96 des 240 arêtes lointaines ; re-réglure g ≥ 3 | P / E | M:64-66, 81, 95, 101, 133-135, 143-149, 152-153, 162 |
| réseau des droites | [M : Λ_L] = 3^(e₃−1) ; dét Λ_L = 7^(45−r)9^(e₃−1) ; e₃ ≤ 22, e₂ ≤ 27, e₅ ≤ 27 ; rang_F₇(N) = 99 ; ≥ 33 droites monochromes pour c ∈ U non constante ; ensemble régulier de 44 sommets : t ≤ 11 droites contenues | P | M:292, 312-313, 860-861 |
| nombres forcés (programme de degré 0) | rang 37 : ≥ 380 (norme ≤ 20) ; couches seules 14 (≥ 380), 16 (≥ 1283), 18 (≥ 4932), 20 (≥ 34 523) ; rang 39 : ≥ 2367 ; rang 41 : ≥ 234 ; rang 43 : ≥ 165, seulement 18 (≥ 165) ou 26 (≥ 2632) | E | M:327-332 |
| rang 37 sans norme 14 (neuf classes + chemins) | a₈ + a₉ + a₁₀ ≥ 22 ; a₉ + a₁₀ ≥ 82 si a₈ = 0 ; a₁₀ ≥ 574 si a₈ = a₉ = 0 ; 7a₉ + a₁₀ ≥ 574 si a₈ = 0 ; ≥ 11 paires ±v de norme ≤ 20 ; 350a₈ + 91a₉ + 13a₁₀ ≥ 7462 | E (sans certificat) | M:1108-1119 |
| S₀ (intervalles exacts) | norme 4 de M : 1000 (346-538 entiers ; 231-327 fractionnaires d'un signe) ; norme 26 : 2632 (160-740) ; κ 0-3 ; s₄₄ 0-145 ; c₁ 0-36 (pair, ≠ 1) ; g_v ≤ 22 (O classe 1 norme 28/9 : 99-121) ; O classe 2 norme 22/9 : 0-3 ; norme 40/9 : 5672-6396 (≥ 4979 non arêtes) ; u ≤ 290 ; g_ℓ ≤ 96, g_ℓ ≥ 22κ ; w ≤ 48 ; P3/N25 : 10 ≤ n ≤ 300, n ≥ 11, n ≡ s₄₄ mod 2 ; couches L₉ (table L02_C2_aws-420) ; p ≤ 9576, q ≤ 16674 + 3p/4 ; t_ℓ ≤ 97 ; spectre de T dans [−48,9 ; 111,1] | E / C | M:504-517, 528, 578-593, 694, 787, 816-817, 857, 487 |
| S₀ (comptes forcés) | ≥ 4374 (vecteurs entiers de norme 4 × arêtes + fantômes indépendants) ; ≥ 2289 (2285) ; ≤ 288 de profil (1⁶ ; −2 ; (−1)²⁶) ; ≥ 2001 de profil (1⁷ ; (−1)²⁹) ; Codex ≥ 2289 + 15g ; ghost : ≤ 374 + 231 | E / P | M:549, 561-566, 543, 602 |
| vecteurs binaires de norme 28 | e(X) = e(Y) ≤ 5 (tout rang) | P | M:551-557 |
| P3/N25 (structure) | profil (1³ ; (−1)²⁵) à tout rang ; δ ≤ 9 ; effectifs sur les droites (9 − δ, 59 + 3δ, 163 − 3δ, δ) ; Σy(ℓ)³ = 478/9 − 6δ ; Σy(ℓ)⁴ = 748/9 − 4δ ; −6 ≤ m·m′ ≤ 15 ; m·m′ mod 7 ∈ {0,1,2,3,6} ; deux dans la même classe (n ≥ 11 > 8) | P | M:628-633, 707-708, 829-831 |
| recherche P3/N25 | 4581 → 3640 → 3343 → 3271 ; par δ (restants) 93, 257, 586, 855, 819, 520, 141 ; 941 (687 + 413 témoins) ; 297 ; 72 (51 + 21) ; 59/252 et 326/1766 certificats ; 567 violent le lemme C ; 1 583 132 519 nœuds ; 47 085 600 étoiles complètes réfutées ; n₀(p) ≥ 0 et 2k_p ≤ 24 + r(p,q) + r(p,q′) ; E_pq + I_pq ≥ 6 − 2c_pq ; c_pa + c_pb − c_ab ≥ 2 | C / E / P | M:1056-1063, 945-947, 1013, 1026, 897, 962, 1124-1126, 1003, 939, 933 |

#### (3) Lemmes ouverts et étapes manquantes (ce qu'ils donneraient)

| lemme / étape | ce qu'il donnerait | source |
|---|---|---|
| Minoration du 7-rang des classes de jumeaux et de grilles en fonction du nombre de paires jumelles (espace de dimension 18 au rang 37) | < ~540 paires jumelles, donc exclusion du rang 37 par la comptabilité | H:1655-1660, 1696-1700 (L02_C2_aws-335) |
| « Aucune droite dans 4 ou 6 grilles » | τ_grid ≤ 693 | H:1594-1595 |
| Constantes de collision pour supports 9 et 10 ; réservoir support 10 ; recensement d'ordre 11 ; masses 7-9 à P = 0 | fermerait la comptabilité du rang 37 (ou P > 285) | H:1504-1505, 1582-1583, 1992-1994 |
| (a′) pas de droite générique à k = 22 ; NT ; « toute droite déconnectée » contre 18 dimensions | chaîne de septembre ⇒ exclusion du rang 37 | H:1717-1723 (L02_C2_aws-342) |
| Raison uniforme (en G) de la mort de l'étoile | (a′) pour toutes les droites génériques | H:1746-1747, 1841-1847 |
| Énoncé B : 12 670 + 147 boules, 17 tests de rang | droites sans prisme connexes au rang 37 (local) | G:225-240 (L02_C2_aws-377) |
| Réduction d'un facteur ~1e4 de la liste des graphes de droites connexes | rendrait un balayage exhaustif faisable (sinon 5 à 50 années-cœur) | H:2017-2018 ; M:227-231 |
| Test à deux étoiles (fastr2.c, jamais validé) | décider la droite dans six grilles | G:243 ; H:2014 |
| Proposition C pour les droites non génériques et les paires r + r′ ≥ 80 ; relecture de Codex 233 | symétrie forcée générale (avec C2/C3, 7, 11 : pas de symétrie de (boule, ombres)) | M:126-136 |
| « (boule, ombres) au rang 37 générique a forcément une symétrie, ou n'existe pas » | exclusion des droites génériques au rang 37 | M:197-200 |
| Borne uniforme 2288 sur les configurations (1⁷ ; (−1)²⁹) à support positif indépendant | S₀ exclu | M:601-603 (L02_C2_aws-421) |
| Majoration du nombre des quatre profils de classe 2 de norme 40/9 | S₀ (≥ 4979 requis) | M:535-536 |
| Fermeture des 3271 supports P3/N25 (preuve finie au niveau de la coquille ; toutes les étoiles doubles) | S₀ exclu (S₀ en exige ≥ 10, en fait ≥ 11) | M:1064-1065, 1081 |
| Classification des vecteurs de O de norme ≤ 12 dans les classes 1 à 4 ; géométrie des 538 vecteurs de norme 4 non triangulaires et des 329 par classe en norme 26 | rendrait utiles les variantes cubique / degré 2 ; exclusion de S₀ | M:390, 452-453 |
| Existence d'une 22-coclique | si non : a₇ = 0 à tout rang | H:1380-1385 (L02_C2_aws-299) |
| 3-rang du plan 2-(22,4,2) ≥ 19 + classification des vecteurs courts de Λ ; duaux partiels, d ≥ 2 | exclusion d'une 22-coclique par la route Λ | H:1399, 1411 (L02_C2_aws-301, L02_C2_aws-302) |
| Sous-cas du lemme A en norme 18 (sommet partagé autre que ω ; c manquants différents ; racine (1,1,1,1) ; e = 1) ; comptage mécanisé par graine en norme 18 | plafond de a₉ par graine (~8 nécessaires à r = 37) | H:1251-1252, 1266-1267 |
| Classification de la norme 4 de M (classes ±1 : trois −1 en position générale ; motif (2,−1,−1)) ; classe 0 en norme 28 | majorations duales (peu de levier au haut de l'échelle) | H:1216-1218 |
| Classification du 12-ensemble U (exception de la note 183) | contrôle d'une famille de collisions | H:1290 |
| Structure réciproque du cas norme 14 (2-(15,3,2)) | décider l'extension de la configuration norme 14 | H:1200-1202 |
| Ablation « Green mod 7 + intersections + capacités + positivité des blocs 2 × 2 et 3 × 3 » sans saturation | savoir si la forme 0/1 est la seule cause de mort des étoiles | H:1830-1832 |
| Condition la plus faible sur l'apex (neuf groupes de forme (1,2,2), somme de potentiel 3 − λ_w(v)) | énoncé sur l'apex utilisant la forme 0/1 | H:1869-1871 |

#### (4) Méthodes transférables

| méthode | d'où vers où | dit par la source / vu par moi | source |
|---|---|---|---|
| Ce qui survit des preuves T16/T18/T20 (équations locales, double comptage, matrices 63E₋₄ et 77E₃, budgets) | C2 → C1 | dit par la source | H:1177-1182 |
| Symétrie forcée : toute symétrie de (boule, ombres) se prolonge, puis exclusions des ordres 2, 3, 7, 11 | C2/C3 → C1 | dit par la source | M:36-37, 110-112 |
| Motif de famille biplan (m ≥ 1 + u(u+1)/2) testé dans srg(243) | srg(v,k,1,2) → srg(243) (u = 4) | dit par la source | H:1187-1200 |
| Contrôle d'une preuve sur un graphe existant (proposition 13 sur BvLS) | 99 → srg(243) comme contrôle positif | dit par la source | M:393-398 |
| Bascule du 243 (re-réglure de 80 grilles) | srg(243) → 99 : NON transférable (le 243 n'est pas un modèle) | dit par la source | M:151-154, 181-183 |
| Théorème 3, lemme 2 | toute la famille srg(v,k,1,2), k ≥ 8 (243 : ≥ 13) | dit par la source | M:54-75 |
| Lemme laplacien de Codex | « toute paire de candidats de ce type, pas seulement à boule fixée » | dit par la source | M:122-124 |
| Sous-réseaux de type 43 dans L1 (sous-espaces isotropes maximaux de D) | exclusion du rang 43 (genre, M, vecteurs courts de L1) → rangs 37, 39, 41 | dit par la source | H:1442-1448 |
| Idem, appliqué aux outils du rang 43 du Mandat C (identité de budget, S₀, P3/N25) | rang 43 → 37-41 ? | vu par moi, NON vérifié : ces outils utilisent l'égalité de classe du plan anisotrope et le programme à neuf classes ; au rang 37 le programme à neuf classes SANS égalité de classe ne force aucun objet bas (M:1088-1091, L02_C2_aws-454) ; il faudrait vérifier si les identités valent pour chaque Λ# | H:1442-1448 ; M:742-767 |
| Borne de rang de Gram mod 7 (45 − r sur L1 ; 56 − r sur le noyau) | rang 37 → rang 43 (« où D n'a que 49 classes ») | dit par la source | H:1495, 1615-1620 |
| Lemme A (parabole entière) et lemme B (plafond) : valables pour tout ensemble de sommets d'un srg(99,14,1,2) | supports P3/N25 → tout autre support forcé : cœurs de normes 14/16/18, configuration norme 14 (L02_C2_aws-267), 12-ensemble U (L02_C2_aws-286), 22-cocliques, ensembles réguliers de 44 sommets, configurations (1⁷ ; (−1)²⁹) de S₀ | « vaut pour tout ensemble de sommets » dit par la source (M:953) ; les cibles listées sont vues par moi | M:922-942, 953 |
| Moteur d'étoile + vérificateur exhaustif sans solveur (star_check.py) | P3/N25 → configurations (1⁷ ; (−1)²⁹) (≥ 2001 requises dans S₀ ; borne 2288 fermerait S₀) | vu par moi | M:1018-1032, 1121-1129, 559-566, 601-603 |
| Recherche d'étoile à un point proche (modèle mod 7 de dimension 36) | « ferme toute famille de boules qui est petite » | dit par la source | H:1949-1951 |
| Principe du plus court représentant | toute comptabilité de collisions par classes | dit par la source | H:1538-1546 |
| Identités de Green réelles, fait A, lemme 14, unicité du profil (1³ ; (−1)²⁵) | valables à tout rang : utilisables aux rangs 39, 41, 43 | « valid at every rank » / « tout rang » dits par la source | H:1777 ; G:138-145 ; M:551, 632 |
| Simplexe exact (Bland en fractions ; exact_lp.py ; « une question = quelques secondes ») | tout PL thêta (les flottants donnaient des artefacts) | dit par la source | H:1400-1401 ; M:268-273, 335 |
| Validation de bout en bout sur un réseau existant (K₈ ⊕ B¹⁸) ; outil Jacobi de niveau 1 contrôlé sur Leech | tout programme modulaire nouveau | dit par la source (contrôles) ; généralisation vue par moi | M:635-639, 725-727, 808 |
| Ablation (retirer des familles de contraintes pour voir ce qui tue) | étoiles (Codex 214) → tout verdict local | dit par la source (méthode utilisée) | H:1808-1810 |
