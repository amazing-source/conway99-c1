# Fiche L08 — C1 : branche exploratoire du LAB (16-20/10/2026) et sa périphérie

Agent de consolidation L08, 20/10/2026, en lecture seule.

**Statuts.** Ce sont ceux de `CONSIGNES_AGENTS.md` : P, C, E, S, H, O, R, X. Ils sont recopiés des sources sans être rehaussés. Quand deux notes divergent, la fiche retient le plus bas et le signale (§7). Attention : plusieurs notes du 20/10 (THM, BORNE, RES, ORD2) emploient « X » pour « ouvert » et « A » pour « déjà dans l'archive ». Dans cette fiche, X signifie toujours « retiré » et O « ouvert », comme dans les consignes.

**Chemins.**
- `work/...` est relatif à la racine du workspace researcher-2 (`C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30`).
- `Desktop/Recherche_Conway/...` désigne le dossier du bureau.
- `conway99-c1:<branche>:<chemin>:<ligne>` et `conway99-c1:commit <h>` renvoient au dépôt `C:/home/researcher/cw/conway99-c1`.
- Les abréviations de chemins sont définies au §9.0.

**Compagnon.** `L08_C1_exploration.jsonl` contient 235 lignes, une par résultat. Les identifiants L08-NNN sont ceux de la table du §3.

**Méthode.**
- Trois sous-agents en lecture seule :
  - fork A : du 16/10 au 18/10 vers 04:30 ;
  - fork B : audit du 18/10 et registre c = 3 jusqu'au 18/10 au soir ;
  - fork C : nuit du 18 au 19/10 et matin du 19/10.
- L'agent L08 a lu lui-même le 19/10 après-midi, le 20/10 et la périphérie (imports du 09/10, sauvegarde du 12/10, journaux).
- Les doublons entre lectures sont fusionnés (7 fusions, indiquées dans `remarques`).

## 1. Résumé

1. Le lot couvre la branche exploratoire du LAB (16/10 17:05 UTC → 20/10 au soir) et sa périphérie : imports du 09/10, sauvegarde de reprise de Codex des 12-13/10, journaux. Il compte 235 résultats ; aucun n'exclut C1 ni un rang.
2. Route c :
   - m ≤ 4 est prouvé sous P ≤ 852, dont le statut est contesté : C ou A + E [L08-067, L08-188] ;
   - m = 4 n'est exclu que par CP-SAT, statut S [L08-070] ;
   - le registre c = 3 passe de 10 052 gabarits à 35 ouverts le 19/10 [L08-099], dont 23 exclusions à verdict de solveur unique [L08-125] ; P3 est inachevé [L08-114].
3. c ≤ 2 : dichotomie (I)/(II) [L08-057]. La branche (II), au moins 33 droites c ≤ 2, n'a aucune méthode finie [L08-233]. Les recensements c_min = 2 et 1 sont incomplets [L08-073, L08-074].
4. 18/10 : le bug OR-Tools 9.15 (domain[-1] = 0) entraîne des retraits [L08-060, L08-062, L08-063, L08-064] :
   - 162 verdicts c3 de Codex ;
   - c4, ramené de 79/79 à 76/79 puis refermé ;
   - la campagne AWS c3star v1 ;
   - le modèle sans Gram du LAB.

   P ≤ 852 et 3P + 4G ≤ 2772 sont revérifiés exactement [L08-067, L08-069].
5. Nuit du 18 au 19/10 : les familles 5602, C4C3, T23, K3U, 2K2, P3NB, K2BC et 2K2N + B/C sont fermées par calcul exact + RUP, sous E3, statut E [L08-103, L08-104, L08-105, L08-108, L08-109, L08-115, L08-116, L08-113].
6. 20/10, Théorème 6.1 (P, relu par un agent) : si toute droite admissible à t ≤ 7 échoue au test d'étoile du rang 37, alors r ≠ 37 ; la seule entrée est P ≤ 852 [L08-187]. (H₃₇) n'est testée que sur ≈ 3,5·10⁴ droites [L08-183, L08-194]. Le pilote de 76 418 droites UNSAT est hors de la cible t ≤ 7 [L08-222].
7. Coût de la route du rang 37 [L08-220, L08-223, L08-194] :
   - 187 381 435 694 classes ;
   - ≈ 5 à 6,5·10⁴ heures-cœur ;
   - les types d ≥ 5, (1,4) et (2,4) n'ont pas de moteur ;
   - les UNSAT ne sont pas certifiés.
8. Au-delà de 37 :
   - rang 39 : l'étoile meurt 5 fois sur 5 (E) [L08-181] ;
   - rangs 41-43 : hors de portée ;
   - aucun outil linéaire ne majore r [L08-197] ;
   - les résidus de droites ne peuvent pas exclure 39 à 43 [L08-219] ;
   - l'ordre 2 en 7 n'agit pas avant 7 lointains [L08-226].
9. R8 : modèle sain, et R8 UNSAT ⇒ pas de Conway à tout rang [L08-210]. Coût 5·10⁷ à 10¹² heures-cœur [L08-213] ; la variante CEGAR n'a fait qu'une itération [L08-214]. Frontière au 20/10 : R8 et l'étoile au rang 39 [L08-232].
10. Aucune preuve n'est relue par un humain. Les statuts de P ≤ 852, de L23 et de « m = 4 exclu » divergent selon les notes (§7).

## 2. Chronologie

Les heures `+02` sont celles des commits ou de l'heure locale ; `UTC` est précisé quand la source l'emploie.

**Antécédents rattachés au lot (09/10 au 14/10)**
- 09/10, soir — NOTE_RESEAUX_DE_DROITE : déterminants de Λ₋(T) et Λ₃(T). L23 retrouvé par les invariants de Hasse [L08-001] — RD:1-62.
- 09/10, 12:32-12:42 (+02) — Dossier intégré C1 d'une session externe : saturation par témoins de bord, transport triangulaire, audit des 174 noyaux, essais de Jacobi [L08-002 à L08-005] — CI/LISEZ_MOI.md:1-23.
- 10/10 — Codex, notes N16 « sans rang » 255 à 260 ; correction d'un compte attribué au LAB [L08-006, L08-007] — RC/snapshot_20261012T113936Z/bridge/messages/.
- 12/10 — Reprise de Codex (sauvegarde RECOVERY) :
  - échanges de designs de Hoffman (commit 617b299) ;
  - coexistence V1 à V6 (lemme d'extension 21 → 22, commit 8a38eeb ; théorème de complétion V6) ;
  - équivalence à deux positivités, relèvement S3 ;
  - consignes de l'utilisateur (global avant local ; priorité à l'asymétrie)

  [L08-008 à L08-012, L08-013 à L08-016] — RC/RECOVERY_README.txt:100-246.
- 13/10 — Coexistence V9 à V13. Pilote AWS V10 : 255 recherches, toutes UNKNOWN (≈ 4,44 USD). La coupe spectrale de Claude (message 595) est retirée au message 596 [L08-017, L08-018] — RC/RECOVERY_README.txt:1-60.
- 14/10 — Consignes : deux chercheurs, fin des vérifications croisées systématiques, objectif de construire un SRG asymétrique à λ = 1 [L08-019] — AGa:1245-1270.

**16/10**
- 17:05 UTC — Ouverture de la branche exploratoire, cible R8 [L08-020] — EXP:1-29.
- 17:10-19:02 UTC — Paris 1 à 3 réfutés ; principes de résonance et d'extension ; N9-NG reformulé ; réduction à Q7 (Codex bba12ce) ; ODDCONST + SYM6 ; lemme impair ; R8 en TIMEOUT à 2 h [L08-021 à L08-027] — EXP:43-203.
- Soir :
  - marge d'ODD-PURE non uniforme ; séparation F7 entre blocs à grille et sans grille [L08-028, L08-029] ;
  - Codex ouvre la branche min c = 4 : 2²¹ graphes → 221 types → 367/200 → 100 → 87 → 79 gabarits [L08-053] — AGa:14-55.
- 21:34-22:28 (+02) — Codex réduit à 79, puis 20, puis 15 gabarits (commits cd34d430 à d07ac4a8).
- 22:37-23:18 (+02) — Forme 7-adique, calibration sur srg(243), exigence c ≤ 3 [L08-030, L08-031] — EXP:252-343.
- 22:45 (+02) → 17/10 00:05 — Codex : 69, 74, 75, puis 76/79 [L08-055] — MOM:65-222.

**17/10**
- 00:00-00:40 (+02) — c = 1 : réduction exacte, H46, découpage par moyeu [L08-032 à L08-034].
- 01:21 (+02) — E3, commit e1c7dc96 [L08-037].
- 02:05 (+02) — Générateur c ≤ 3 validé 367/200 ; lemme des 2-coupes [L08-036, L08-040].
- 02:20-02:50 (+02) — Codex : lemme de bord tourné [L08-039]. Le motif OR-Tools domain[-1] est repéré dans un module, puis corrigé partout le 18/10 seulement — MOM:634-637.
- 10:57-11:33 (+02) — Bibliographie ; les 1 740 côtés c = 1 positifs du cache sont exclus par des lemmes entiers [L08-059, L08-042].
- Journée, jusqu'à 22:42 (+02) — Lemme de moyenne, condition 2-adique, ODD9 faux à c = 1, fenêtre impaire, rang mod 3, « nuit 2 », prompt de recherche [L08-043 à L08-048] — EXP:555-692 ; PRM.
- 23:12-23:45 (+02) — Codex reprend : bornes de paires, 8 exclusions de Gram [L08-038].

**18/10**
- 00:05-00:30 (+02) — Relecture de la note ChatGPT ; filtres h = TPc [L08-050, L08-051].
- 00:55-01:08 (+02) — Plan c ≤ 3, avec corrections de Codex : dim ker C jusqu'à 7, budget 51 non garanti [L08-057].
- 01:16-02:29 (+02) — AWS 7/9/19, v1 (980 tâches) [L08-056].
- 03:21 (+02) — c_min = 3 : 10 052 gabarits ouverts après le Gram entier [L08-072].
- 04:24 (+02) — Recensement partiel c_min = 2 et 1 [L08-058].
- 04:30 (+02) — Codex : c4 à 79/79.
- 09:34 (+02) — Codex : pilote c3, 162 verdicts ; lancement de la campagne AWS c3star v1.
- ≈ 11:00 — L'utilisateur demande : « exclu veut dire exclu ».
- 11:40-11:45 (+02) — Bug OR-Tools 9.15 ; retraits ; correctif ac8921c3 [L08-060, L08-062, L08-063].
- 12:27 — RECALCUL_C4 : 76 + 3 rouverts.
- ≈ 12:30 — L'utilisateur demande de revérifier P ≤ 852 [L08-067].
- 13:10 (+02) — Audit LAB, commit e9d3600d.
- 13:21 (+02) — 3P + 4G ≤ 2772, commit 8d45031f [L08-069].
- 14:56 (+02) — Pilote de l'étoile complète : 77/100 ; coût estimé à 6 500 h-cœur [L08-075].
- 16:15-16:36 (+02) — Gabarit 9 exclu ; c4 refermé, commit ecb50673 [L08-070].
- 17:06-17:31 (+02) — Couvertures de Gram ; HᵀH = 7R ; 5128 et 4192 exclus par moments [L08-078 à L08-080].
- 17:52 → 18:26 (+02) — Modèle sans Gram, puis RÉTRACTATION (commit ae276016) [L08-064].
- 18:33 (+02) — AUDIT_RAPIDE : 4 814 exclus ; CP-SAT et HiGHS concordent sur 510 946 gabarits [L08-072, L08-082].
- 19:48 (+02) — Lemme FG, M1/M2 ; zscan1 : 7 998 exclus, 2 054 ouverts [L08-084, L08-085].
- 21:00-21:13 (+02) — R1, PL de Codex, FG sur tout c = 1 ; AUDIT_GLOBAL ; identité d^K [L08-086 à L08-088, L08-098].
- 21:44-22:18 (+02) — Registre de 8 339/1 713 à 8 461/1 591 [L08-082].
- 22:35-23:31 (+02) — MORTS_ET_SURVIVANTS ; Codex : certificat de 9748 (22:43), carré de défaut, spectre des grilles [L08-089, L08-090, L08-092, L08-094].

**Nuit du 18 au 19/10, en UTC**
- 18/10 22:52-23:31 — gz 5602 exclu (commit aa3e8a9e) ; règle C4 + C3 ; 1 187 ouverts [L08-103, L08-104].
- 19/10 00:06 — T23 [L08-105].
- 00:19 — 1 163 ouverts.
- 03:07 — K3U fermée, 902 ouverts [L08-108].
- 04:32 — 2K2 fermée, 537 ouverts [L08-109].
- 05:00 — Relecture adversariale : aucun défaut.
- 06:19 — Runs AWS : 435 ouverts [L08-124].
- 07:06 — P3NB, 97 ouverts [L08-115].
- 07:34 — K2BC, 40 ouverts [L08-116].
- 08:14 — Inventaire [L08-125].
- 11:22 — Z2C/CXC, 37 ouverts [L08-133].
- 13:05 — 2K2N + B/C, 35 ouverts [L08-113].

**19/10, après-midi et soir (+02)**
- 13:22 — Certificats d'ordre 2 (b3174909) [L08-133].
- 15:55 — Test uniforme : positivité globale (résultat négatif), moteur de recensement indépendant, outils pour les six grilles (76860d92) [L08-136 à L08-138].
- 17:07 — Mandat de représentation : cadre lointain, Gram entier des six grilles, portée du registre (f0611cf7) [L08-140 à L08-146].
- 19:26 — Note de réduction : mur de dureté à n = 12, budget d'entropie (14b8ec3e) [L08-147 à L08-152].
- 21:45 UTC — État de P3 [L08-114].
- 22:24 — Chasse au trésor : lois de famille, variance, retrait de la borne 692 (c80d292c) [L08-154 à L08-157].

**20/10 (+02)**
- 00:19 — Fusion des routes finies : obligation 7-adique, c ≤ 2 réfutées 58/58 (23f8bde7) [L08-158 à L08-168].
- 02:17 — Ablation : l'obstruction est arithmétique (cd05e047) [L08-169].
- 09:49 — Relecture de la note ChatGPT sur les normes 12 et 14 (f871c647) [L08-175].
- 10:04 — Prompt Core37 (a93632a3) [L08-176].
- 11:12 — D'où vient l'obstruction (87df6ca5) [L08-170 à L08-174].
- 12:27 — Core37 vérifié ; filtre réel ; rang 39 à l'oblr3 en TIMEOUT (ae63f127) [L08-177, L08-178].
- 12:43 — star39 (f8c1082a).
- 14:43 — Test d'étoile : tous les types c ≤ 3 meurent au rang 37 (09e749ac) [L08-179].
- 15:14 — Synthèse ; étoiles du rang 39 mortes 5/5 ; line37 (e8595e8e) [L08-181, L08-183].
- 15:22 — Correction : au rang 39, le filtre réel est un accélérateur (8e7b71cd) [L08-182].
- 16:14 — Théorème 6.1 et line37_fast (36d6969e) [L08-186, L08-187].
- 16:20 — Borne de rang (409310a6) [L08-197 à L08-209].
- 16:33 — Tous les calculs sont suspendus : l'utilisateur reprend le PC [L08-210].
- 16:43 — Route R8 (b6e3d575) [L08-210 à L08-215].
- 16:45 — Résidus (51aca2a8) [L08-216 à L08-219].
- 16:48 — Énumération (e13b8824) [L08-220 à L08-224].
- 16:51 — Ordre 2 en 7 (4873b508) [L08-225 à L08-230] ; version finale de SYNTHESE_MECANISMES [L08-231 à L08-235].

## 3. Table des résultats

Colonnes : identifiant, date (mois-jour), énoncé court, statut, source principale. « (+n) » signale n autres sources dans le `.jsonl`.

### 3.1 Antécédents rattachés au lot (09/10 au 14/10 : imports du 09/10, reprise de Codex des 12-13/10, consignes)

| id | date | énoncé court | statut | source principale |
|---|---|---|---|---|
| L08-001 | 10-09 | Réseaux propres portés loin d'une droite (09/10) | P | work/c1_index_2026-10-09/NOTE_RESEAUX_DE_DROITE.md:1-62 |
| L08-002 | 10-09 | Dossier intégré C1 du 09/10 : théorème de saturation par témoins de bord | P | Desktop/Recherche_Conway/c1-imports/2026-10-09-convergences/DOSSIER_C1_CONVERGENCES/DOSSIER_C1_INTEGRE.tex:175-226, 1016, 1680 (+1) |
| L08-003 | 10-09 | Transport triangulaire des non-arêtes et fermeture des 4-cycles (09/10) | P | Desktop/Recherche_Conway/c1-imports/2026-10-09-convergences/DOSSIER_C1_CONVERGENCES/antecedents/NOTE_TRANSPORT_C1.md:5-13, 27-31, 87-105, 204-213 |
| L08-004 | 10-09 | Audit C1 du 09/10 : reconstruction du catalogue des 174 noyaux | C | Desktop/Recherche_Conway/c1-imports/2026-10-09-convergences/DOSSIER_C1_CONVERGENCES/antecedents/AUDIT_C1_ANNEXE.md:59-129 |
| L08-005 | 10-09 | Recherche bibliographique large et essais arithmétiques marqués (09/10) | E | Desktop/Recherche_Conway/c1-imports/2026-10-09-convergences/DOSSIER_C1_CONVERGENCES/antecedents/RECHERCHE_C1_TRANSFERTS.md:5-13, 337-351, 437-451 |
| L08-006 | 10-10 | Résultats N16 « sans rang » de Codex (10/10) | P | Desktop/Recherche_Conway/RECOVERY_2026-10-12/snapshot_20261012T113936Z/bridge/messages/codex-note255-omitted-pair.txt:1-8 (+4) |
| L08-007 | 10-10 | Correction par Codex d'un compte attribué à tort | X | Desktop/Recherche_Conway/RECOVERY_2026-10-12/snapshot_20261012T113936Z/bridge/messages/codex-after541-542.txt:1-10 |
| L08-008 | 10-12 | Lemme d'extension des cocliques de 21 sommets (Codex, 12/10) | P | Desktop/Recherche_Conway/RECOVERY_2026-10-12/coexistence_f738665_20261013T193425Z/repo/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:8-25 (+1) |
| L08-009 | 10-12 | Théorème de fermeture d'une factorisation binaire (V6, Codex, 12/10) | P | Desktop/Recherche_Conway/RECOVERY_2026-10-12/RECOVERY_README.txt:111-121 (+1) |
| L08-010 | 10-12 | Échanges de designs de Hoffman : 36 classes exclues comme bords C1 | E | Desktop/Recherche_Conway/RECOVERY_2026-10-12/RECOVERY_README.txt:237-244 |
| L08-011 | 10-12 | Lemmes uniformes de coexistence et exclusion d'une famille de bords (12/10) | S | Desktop/Recherche_Conway/RECOVERY_2026-10-12/RECOVERY_README.txt:212-224 |
| L08-012 | 10-12 | Survivant de bord : modèle SRG complet UNSAT sans preuve indépendante | S | Desktop/Recherche_Conway/RECOVERY_2026-10-12/RECOVERY_README.txt:160-171 |
| L08-013 | 10-12 | Équivalence spectrale globale utilisée par Codex | P | Desktop/Recherche_Conway/RECOVERY_2026-10-12/snapshot_20261012T113936Z/bridge/messages/codex_20261012_global_effectif.txt:1-12 |
| L08-014 | 10-12 | Relèvement S3 : équations exactes sur F₃ (Codex, 12/10) | P | Desktop/Recherche_Conway/RECOVERY_2026-10-12/snapshot_20261012T113936Z/bridge/messages/codex-s3-exact-moments-20261012.txt:1-10 |
| L08-015 | 10-12 | Audit indépendant de l'asymétrie à 243 (Codex, 12/10) | C | Desktop/Recherche_Conway/RECOVERY_2026-10-12/snapshot_20261012T113936Z/bridge/messages/codex-asymmetry-audit-frozen-20261012.txt:1-8 |
| L08-016 | 10-12 | Recherche active C1 au 12/10 (cinq versions successives) | O | Desktop/Recherche_Conway/RECOVERY_2026-10-12/asymmetry_trades_617b299_20261012T131248Z/handover/RECHERCHE_ACTIVE_C1.md:1-40 |
| L08-017 | 10-13 | Campagne AWS V10 : 255 recherches courtes, toutes UNKNOWN | O | Desktop/Recherche_Conway/RECOVERY_2026-10-12/RECOVERY_README.txt:29-53 |
| L08-018 | 10-13 | V11 : identité d'énergie par colonne ; coupe spectrale de Claude retirée | X | Desktop/Recherche_Conway/RECOVERY_2026-10-12/RECOVERY_README.txt:1-27 |
| L08-019 | 10-14 | Consignes de l'utilisateur relayées dans le journal (14/10) | O | conway99-c1:origin/lab/aws-codex-7-9-19:AGENTS.md:1245-1270 |

### 3.2 Du 16/10 au 18/10 vers 04:30 : fondations de la route c, c = 1, branche m = 4 (fork A)

| id | date | énoncé court | statut | source principale |
|---|---|---|---|---|
| L08-020 | 10-16 | R8 : reformulation exacte et implication | P | work/exploration_2026-10-16/EXPLORATION.md:11-29 |
| L08-021 | 10-16 | Paris du 16/10 réfutés : Hall dans une étoile, graphe de partage, DISC-35 par vecteurs universels | R | work/exploration_2026-10-16/EXPLORATION.md:44-48 (+1) |
| L08-022 | 10-16 | Principes spectraux prouvés (résonance, extension A7, entrelacement) | P | work/exploration_2026-10-16/EXPLORATION.md:53-55 (+3) |
| L08-023 | 10-16 | N9-NG reformulé ; paris 5 et 6 | P | work/exploration_2026-10-16/EXPLORATION.md:101-114 |
| L08-024 | 10-16 | Réduction de Conway à Q7 (résonance 20×20) | P | work/exploration_2026-10-16/EXPLORATION.md:116-132 |
| L08-025 | 10-16 | Conjecture Q7 et sa scission ODDCONST + SYM6 | O | work/exploration_2026-10-16/EXPLORATION.md:128 (+1) |
| L08-026 | 10-16 | Lemme impair (ι = (2 3)) | P | work/exploration_2026-10-16/EXPLORATION.md:166-181 |
| L08-027 | 10-16 | Secteur Z (Codex) et bilan ODD-PURE + rang Z | P | work/exploration_2026-10-16/EXPLORATION.md:158-162 (+1) |
| L08-028 | 10-16 | Marge d'ODD-PURE non uniforme | H | work/exploration_2026-10-16/EXPLORATION.md:205-225 |
| L08-029 | 10-16 | Séparation F7 entre blocs à grille et sans grille ; (R7-NG) | O | work/exploration_2026-10-16/EXPLORATION.md:236-250 (+1) |
| L08-030 | 10-16 | Forme lisible de la chute 7-adique (E1-E4) et angle global | P | work/exploration_2026-10-16/EXPLORATION.md:252-314 |
| L08-031 | 10-16 | Branche min c ≤ 3 : exigence exacte par paire sans grille | P | work/exploration_2026-10-16/EXPLORATION.md:332-343 |
| L08-032 | 10-16 | c = 1 : réduction exacte (vue depuis l) | P | work/exploration_2026-10-16/EXPLORATION.md:345-357 (+1) |
| L08-033 | 10-16 | Critère H46 et énoncé H46-c1 | O | work/exploration_2026-10-16/EXPLORATION.md:358-371 (+2) |
| L08-034 | 10-17 | c = 1 : découpage par moyeu (a ≥ b + 1) | O | work/exploration_2026-10-16/EXPLORATION.md:405-432 |
| L08-035 | 10-17 | Faits exacts à une droite : le graphe lointain (17/10) | P | work/exploration_2026-10-16/EXPLORATION.md:476-486 (+1) |
| L08-036 | 10-17 | Générateur de gabarits c ≤ 3 et filtre K | E | work/exploration_2026-10-16/EXPLORATION.md:439-450 |
| L08-037 | 10-17 | E3 : aucun rectangle n'a e(Q) = 3 | P | conway99-c1:origin/lab/aws-codex-7-9-19:notes/MOMENTS_SIGNATURES_C1_2026_10_16.txt:459-498 (+2) |
| L08-038 | 10-17 | Lemmes entiers sur les vecteurs propres −4 | P | conway99-c1:origin/lab/aws-codex-7-9-19:notes/MOMENTS_SIGNATURES_C1_2026_10_16.txt:410-430 (+3) |
| L08-039 | 10-17 | Lemme de bord tourné et code parfait des grilles (Codex) | P | conway99-c1:origin/lab/aws-codex-7-9-19:notes/MOMENTS_SIGNATURES_C1_2026_10_16.txt:664-676 (+4) |
| L08-040 | 10-17 | Lemme des 2-coupes (LAB) et découpage fini de c = 1 | P | work/exploration_2026-10-16/EXPLORATION.md:460-474 (+1) |
| L08-041 | 10-17 | Partition équitable co-Heawood (redécouverte) et cas I conditionnel | P | work/exploration_2026-10-16/EXPLORATION.md:493-522 |
| L08-042 | 10-17 | Toutes les structures positives c = 1 du cache sont exclues par des lemmes entiers | E | work/exploration_2026-10-16/EXPLORATION.md:536-553 |
| L08-043 | 10-17 | Lemme de moyenne : la positivité seule ne ferme pas les cas c = 1 | P | work/exploration_2026-10-16/EXPLORATION.md:555-568 |
| L08-044 | 10-17 | Condition de rang 2-adique | E | work/exploration_2026-10-16/EXPLORATION.md:572-581 |
| L08-045 | 10-17 | Réfutations du 17/10 : ODD9 à c = 1 hors positivité ; (RS) | R | work/exploration_2026-10-16/EXPLORATION.md:606-609 (+2) |
| L08-046 | 10-17 | Fenêtre impaire modulo p | P | work/exploration_2026-10-16/EXPLORATION.md:610-618 |
| L08-047 | 10-17 | Marge de c = 1 dans le rang ; forme modulo 3 | P | work/exploration_2026-10-16/EXPLORATION.md:637-657 |
| L08-048 | 10-17 | Nuit 2 du 17/10 : résolvante, 3-SPEC, deux moyeux ; la cible est (B′) | P | work/exploration_2026-10-16/EXPLORATION.md:659-692 |
| L08-049 | 10-17 | Formes tournées de E3 sur les données c = 1 | E | work/exploration_2026-10-16/EXPLORATION.md:694-723 |
| L08-050 | 10-17 | Note ChatGPT du 17/10 : m3 = K0, rang exact, borne stricte | P | work/exploration_2026-10-16/NOTE_CHATGPT_C1_2026-10-17.pdf:p.1-14 (+1) |
| L08-051 | 10-18 | Filtres entiers h = TPc sur les données c = 1 | E | work/exploration_2026-10-16/EXPLORATION.md:756-786 |
| L08-052 | 10-17 | m ≤ 4 (c_min ≤ 4), version du 17/10 | P | work/exploration_2026-10-16/PROMPT_RECHERCHE_C1_c1_2026-10-17.md:40-46 (+1) |
| L08-053 | 10-16 | Branche min c = 4 (Codex, 16/10) : des 2²¹ graphes aux 79 gabarits de racine | S | conway99-c1:origin/lab/aws-codex-7-9-19:AGENTS.md:14-45 |
| L08-054 | 10-16 | Minimum observé rang_F7(8T44) ≥ 30 sur 3 722 blocs sans grille | H | conway99-c1:origin/lab/aws-codex-7-9-19:AGENTS.md:3-12 |
| L08-055 | 10-16 | Branche c_min = 4 (Codex) : 79 gabarits, 76 exclus au 16/10 | S | work/exploration_2026-10-16/PROMPT_RECHERCHE_C1_c1_2026-10-17.md:169-242 (+2) |
| L08-056 | 10-18 | Gabarits 7, 9, 19 : fronts de Gram et passe AWS v1 | S | conway99-c1:origin/lab/aws-codex-7-9-19:notes/MOMENTS_SIGNATURES_C1_2026_10_16.txt:470-472 (+7) |
| L08-057 | 10-18 | Dichotomie (I)/(II) et routes A/B/C | P | work/exploration_2026-10-16/PLAN_C_LE_3_2026-10-18.md:18-23 |
| L08-058 | 10-18 | c_min = 2 et 1 : recensement partiel, arrêté (18/10 04:24) | S | work/exploration_2026-10-16/c21_root_census/C21_ROOT_CENSUS_PARTIAL_2026-10-18.md:1-44 (+1) |
| L08-059 | 10-17 | Bibliographie du 17/10 et annonces externes | H | work/exploration_2026-10-16/BIBLIO_C1_2026-10-17.md:15-88 (+1) |

### 3.3 Le 18/10 : audit, bug OR-Tools, registre c = 3, lemmes c ≤ 2 (fork B)

| id | date | énoncé court | statut | source principale |
|---|---|---|---|---|
| L08-060 | 10-18 | Bug OR-Tools 9.15 sur les champs répétés du proto | E | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:33-45 (+2) |
| L08-061 | 10-18 | Scan statique des lectures fautives | E | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:47-53 (+2) |
| L08-062 | 10-18 | Portée du bug chez Codex : verdicts retirés | X | Desktop/Recherche_Conway/c1-main-codex/notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt:3-34 (+3) |
| L08-063 | 10-18 | Campagne AWS c3star v1 nulle | X | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:62-63 (+1) |
| L08-064 | 10-18 | Rétractation LAB du modèle sans Gram (GFM) | X | work/exploration_2026-10-16/c3_cost_2026-10-18/C3_GRAM_COVER_2026-10-18.md:180-209 (+5) |
| L08-065 | 10-18 | Lemmes du modèle à la racine, re-démontrés | P | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:84-131 (+2) |
| L08-066 | 10-18 | Racine de budget : au plus 12 grilles | P | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:132-136 |
| L08-067 | 10-18 | P ≤ 852 revérifié | E | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:26-28 (+7) |
| L08-068 | 10-18 | E3 dans le PL de P | H | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:240-247 (+2) |
| L08-069 | 10-18 | 3P + 4G ≤ 2772 et exclusion du gabarit c4 n° 7 | C | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:28-29 (+3) |
| L08-070 | 10-18 | Branche c_min = 4 (79 gabarits à la racine de budget) | S | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_RAPIDE_2026-10-18_soir.md:37-38 (+5) |
| L08-071 | 10-18 | Recensement c ≥ 3 et filtres recoupés | E | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:9-19 (+4) |
| L08-072 | 10-18 | Test de Gram entier V3 | S | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:76 (+4) |
| L08-073 | 10-18 | Recensements exacts c_min = 2 et c_min = 1 | E | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:77 (+3) |
| L08-074 | 10-18 | Tailles estimées des recensements c ≤ 2 (Knuth) | H | work/exploration_2026-10-16/c3_cost_2026-10-18/C3_COST_PILOT_2026-10-18.md:96-113 |
| L08-075 | 10-18 | Pilote de l'étoile complète c3 après correctif, et coût | S | work/exploration_2026-10-16/c3_cost_2026-10-18/C3_COST_PILOT_2026-10-18.md:6-47 (+1) |
| L08-076 | 10-18 | Réduction par symétrie des lettres | H | work/exploration_2026-10-16/c3_cost_2026-10-18/C3_COST_PILOT_2026-10-18.md:49-70 |
| L08-077 | 10-18 | Deux leviers sans effet sur le noyau dur c3 | S | work/exploration_2026-10-16/c3_cost_2026-10-18/C3_COST_PILOT_2026-10-18.md:79-80 (+2) |
| L08-078 | 10-18 | Couvertures de Gram imposées dans le modèle exact (gc1a, gc2a) | S | work/exploration_2026-10-16/c3_cost_2026-10-18/C3_GRAM_COVER_2026-10-18.md:16-121 (+2) |
| L08-079 | 10-18 | Identité de moments HᵀH = 7R et règles de réalisation des coins | P | work/exploration_2026-10-16/c3_cost_2026-10-18/C3_GRAM_COVER_2026-10-18.md:123-153 (+2) |
| L08-080 | 10-18 | Gabarits 5128 et 4192 exclus par moments | C | work/exploration_2026-10-16/c3_cost_2026-10-18/C3_GRAM_COVER_2026-10-18.md:145-154 (+1) |
| L08-081 | 10-18 | Troisième passe : raisons de mort de 2 857 Gram | S | work/exploration_2026-10-16/c3_cost_2026-10-18/C3_GRAM_COVER_2026-10-18.md:156-178 (+1) |
| L08-082 | 10-18 | Registre c3 : évolution le 18/10 | S | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:160-161 (+10) |
| L08-083 | 10-18 | Points faibles du registre c3 | O | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_RAPIDE_2026-10-18_soir.md:17 (+5) |
| L08-084 | 10-18 | zscan1 : plan de comptage de Codex sans Gram ni budget | C | work/exploration_2026-10-16/lemmas_c12_2026-10-18/LEMMES_C12_2026-10-18.md:144-157 (+2) |
| L08-085 | 10-18 | Lemme FG (grille forcée) | P | work/exploration_2026-10-16/lemmas_c12_2026-10-18/LEMMES_C12_2026-10-18.md:9-70 (+3) |
| L08-086 | 10-18 | FG sur tout le recensement c = 1 (k ≥ 1) | E | work/exploration_2026-10-16/lemmas_c12_2026-10-18/LEMMES_C12_2026-10-18.md:202-224 (+1) |
| L08-087 | 10-18 | M1/M2, R1, PL de Codex à toute dimension : le noyau dur c ≤ 2 | S | work/exploration_2026-10-16/lemmas_c12_2026-10-18/LEMMES_C12_2026-10-18.md:72-142 (+3) |
| L08-088 | 10-18 | Identité de lettres A[D_a] d^K = −d^K | P | work/exploration_2026-10-16/lemmas_c12_2026-10-18/LEMMES_C12_2026-10-18.md:235-258 (+2) |
| L08-089 | 10-18 | Pourquoi les paires tuent et les gros blocs survivent | P | work/exploration_2026-10-16/c3_hard_core_2026-10-18/MORTS_ET_SURVIVANTS_C3_2026-10-18.md:29-46 (+2) |
| L08-090 | 10-18 | Lemme du carré de défaut et parité | P | Desktop/Recherche_Conway/c1-main-codex/notes/CARRE_DE_DEFAUT_ET_PARITE_2026_10_18.txt:13-77 (+2) |
| L08-091 | 10-18 | Coupes d'histogrammes de colonnes, sans Gram | P | Desktop/Recherche_Conway/c1-main-codex/notes/HISTOGRAMMES_PROPRES_SANS_GRAM_2026_10_18.txt:3-55 (+1) |
| L08-092 | 10-18 | gz 9748 exclu sans Gram ni budget ; gz 9744 par CP | C | Desktop/Recherche_Conway/c1-main-codex/notes/CERTIFICAT_SANS_GRAM_9748_2026_10_18.txt:1-54 (+3) |
| L08-093 | 10-18 | Une grille est un dominant parfait | P | work/exploration_2026-10-16/c3_hard_core_2026-10-18/MORTS_ET_SURVIVANTS_C3_2026-10-18.md:93-99 (+2) |
| L08-094 | 10-18 | Spectre forcé du bloc lointain d'une droite tout-grille | P | Desktop/Recherche_Conway/c1-main-codex/notes/GRAM_DES_GRILLES_ET_BLOC60_2026_10_18.txt:1-110 (+1) |
| L08-095 | 10-18 | Théorème du spectre de droite (LAB) : contrôle numérique seul | H | work/exploration_2026-10-16/line_spectrum_2026-10-18/line_spectrum_control.py:1-8 (+1) |
| L08-096 | 10-18 | Probe à Gram fixée de Codex (couche 0) et c3hard1 | S | work/exploration_2026-10-16/c3_hard_core_2026-10-18/MORTS_ET_SURVIVANTS_C3_2026-10-18.md:6-27 (+2) |
| L08-097 | 10-18 | Pilote global de Codex et Gram partiel c_min = 2 | S | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:77 (+1) |
| L08-098 | 10-18 | Verdict de l'audit global du 18/10 au soir | O | work/exploration_2026-10-16/audit_2026-10-18/AUDIT_GLOBAL_2026-10-18_nuit.md:106-119 (+1) |

### 3.4 Nuit du 18 au 19/10 et matin du 19/10 : familles exactes, gz 5602, registre à 35 ouverts (fork C)

| id | date | énoncé court | statut | source principale |
|---|---|---|---|---|
| L08-099 | 10-19 | Registre c = 3 : 35 ouverts sur 10 052 (fin du 19/10) | O | work/exploration_2026-10-16/c3_hard_core_2026-10-18/c3_ledger_now_2026-10-19_2k2nbc.json:2-4 (+3) |
| L08-100 | 10-19 | Trajectoire du registre pendant la nuit du 18-19/10 | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/c3_ledger_now.json:2-4 (+7) |
| L08-101 | 10-19 | Relation universelle des colonnes à une racine | P | Desktop/Recherche_Conway/c1-main-codex/notes/COEUR_HUIT_SOMMETS_5602_2026_10_19.txt:238-245 (+2) |
| L08-102 | 10-19 | Lemme des colonnes opposées disjointes (cœur cubique à 8 sommets) | P | Desktop/Recherche_Conway/c1-main-codex/notes/COEUR_HUIT_SOMMETS_5602_2026_10_19.txt:3-7 (+3) |
| L08-103 | 10-19 | gz 5602 (dimension 7) exclu pour toutes les Gram | E | Desktop/Recherche_Conway/c1-main-codex/notes/COEUR_HUIT_SOMMETS_5602_2026_10_19.txt:38-46 (+8) |
| L08-104 | 10-19 | Règle universelle C4 + C3 ⇒ K4 + C3 sur le graphe des grilles | E | Desktop/Recherche_Conway/c1-main-codex/notes/COEUR_HUIT_SOMMETS_5602_2026_10_19.txt:232-256 (+6) |
| L08-105 | 10-19 | Famille (2,3) « touchante » (T23) exclue | E | Desktop/Recherche_Conway/c1-main-codex/notes/COEUR_PARTAGE_DEUX_GRILLES_2026_10_19.txt:5-18 (+7) |
| L08-106 | 10-19 | Paire opposée partagée : cœur C8 ou 2C4 ; catalogue des 114 cœurs | P | Desktop/Recherche_Conway/c1-main-codex/notes/COEUR_PARTAGE_DEUX_GRILLES_2026_10_19.txt:30-53 (+4) |
| L08-107 | 10-19 | Lemme des quatre facteurs (Q_bc grille) ; orbites 20 et 23 exclues | P | conway99-c1:origin/lab/exploration-2026-10-16:notes/FACTEURS_QUATRE_COULEURS_2026_10_19.txt:3-58 (+3) |
| L08-108 | 10-19 | Famille K3 universelle FERMÉE | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/k3u_closed.json:1-6 (+5) |
| L08-109 | 10-19 | Famille 2K2 FERMÉE | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/k2k2_closed.json:2-15 (+7) |
| L08-110 | 10-19 | Couplage forcé entre grilles disjointes et lemme C2 de 2K2 | P | work/exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md:286-291 (+1) |
| L08-111 | 10-19 | Négatif : sans « Q12 grille », ou avec une seule grille Y, les profils sont satisfiables | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md:257-268 (+2) |
| L08-112 | 10-19 | Résidu exact de 2K2N : 1 006 raccordements en 816 classes | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md:377-385 (+3) |
| L08-113 | 10-19 | 2K2N avec une grille B/C FERMÉE | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/k2k2n_bc_closed.json:2-8 (+2) |
| L08-114 | 10-19 | Famille P3 universelle : production inachevée | O | work/exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md:196-200 (+6) |
| L08-115 | 10-19 | Famille P3NB FERMÉE | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/p3nb_closed.json:2-15 (+4) |
| L08-116 | 10-19 | Famille K2BC (GEN --yr=45 --extra=13,26) FERMÉE | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/k2bc_closed.json:2-13 (+3) |
| L08-117 | 10-19 | Couplage forcé d'une grille B/C avec une moitié du cœur | P | work/exploration_2026-10-16/c3_hard_core_2026-10-18/PLAN_250_2026-10-19.md:28-29 |
| L08-118 | 10-19 | Après K3 et 2K2, les grilles sur les 4 autres droites forment une étoile | H | work/exploration_2026-10-16/c3_hard_core_2026-10-18/RAPPORT_MATIN_2026-10-19.md:56-57 |
| L08-119 | 10-19 | La dimension du noyau décide de la survie | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md:48-86 (+1) |
| L08-120 | 10-19 | Aucune borne démontrée n'exclut les dimensions de noyau 6 ou 7 | O | work/exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md:84-90 (+1) |
| L08-121 | 10-19 | Lemme des blocs partiels et coupe conditionnelle sans Gram | P | Desktop/Recherche_Conway/c1-main-codex/notes/BLOCS_PARTIELS_ET_COUPE_ENERGIE_2026_10_19.txt:9-17 (+3) |
| L08-122 | 10-19 | Rang 7 : saturation des sommes de signatures (pilotes) | E | Desktop/Recherche_Conway/c1-main-codex/notes/RANG7_ET_SATURATION_2026_10_19.txt:3-77 (+1) |
| L08-123 | 10-19 | Contrôle positif des couches C2 du probe de Gram | E | Desktop/Recherche_Conway/c1-main-codex/notes/CONTROLE_C2_COUCHES_2026_10_19.txt:3-40 (+2) |
| L08-124 | 10-19 | Couche 2 du probe et runs AWS de la nuit (537 → 435) | S | work/exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md:92-140 (+3) |
| L08-125 | 10-19 | Inventaire des 10 052 gabarits ; 23 exclusions fragiles | S | work/exploration_2026-10-16/c3_hard_core_2026-10-18/c3_inventaire_2026-10-19.md:16-67 (+1) |
| L08-126 | 10-19 | Les 35 ouverts finaux, par type | O | work/exploration_2026-10-16/c3_hard_core_2026-10-18/c3_open_now.tsv:1-35 (+2) |
| L08-127 | 10-19 | Paires de grilles fermées : égalités C2, sans contradiction à elles seules | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md:202-207 (+1) |
| L08-128 | 10-19 | Résultats négatifs de la nuit du 18-19/10 | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md:137 (+4) |
| L08-129 | 10-19 | Détecteur de carrés de défaut sur c ≤ 2 : couverture quasi nulle | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md:142-148 |
| L08-130 | 10-19 | Pièges d'outils et correctif d'étiquette (PySAT, Windows) | H | work/exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md:305-307 (+1) |
| L08-131 | 10-19 | Dissection des contradictions de P3 | E | work/exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md:252-255 |

### 3.5 Le 19/10 après-midi et soir : test uniforme, représentation, réduction, chasse au trésor

| id | date | énoncé court | statut | source principale |
|---|---|---|---|---|
| L08-132 | 10-19 | Faits de base du test uniforme (racine, étiquettes, rectangles) | P | work/exploration_2026-10-16/uniform_test_2026-10-19/NOTE_TEST_UNIFORME_2026-10-19.md:16-34 |
| L08-133 | 10-19 | Certificats d'ordre 2 (z2) : registre c = 3 de 40 à 37 ouverts | C | work/exploration_2026-10-16/uniform_test_2026-10-19/NOTE_TEST_UNIFORME_2026-10-19.md:63-79 (+4) |
| L08-134 | 10-19 | Passe unique z2_sweep sur AWS, sans certificat | S | work/exploration_2026-10-16/uniform_test_2026-10-19/NOTE_TEST_UNIFORME_2026-10-19.md:81-101 |
| L08-135 | 10-19 | Couches supplémentaires sans gain ; obstruction des survivants due à l'intégralité | E | work/exploration_2026-10-16/uniform_test_2026-10-19/NOTE_TEST_UNIFORME_2026-10-19.md:53, 103-113 |
| L08-136 | 10-19 | Tests globaux de positivité de Gegenbauer projetée : tous négatifs | E | work/exploration_2026-10-16/uniform_test_2026-10-19/NOTE_ENONCE_RENFORCE_2026-10-19.md:18-36 (+2) |
| L08-137 | 10-19 | Moteur de comptage indépendant (équations d'extension) | E | work/exploration_2026-10-16/uniform_test_2026-10-19/NOTE_ENONCE_RENFORCE_2026-10-19.md:38-50 |
| L08-138 | 10-19 | Design « six grilles » : partie colonnes non unique | E | work/exploration_2026-10-16/uniform_test_2026-10-19/NOTE_ENONCE_RENFORCE_2026-10-19.md:82-87 (+1) |
| L08-139 | 10-19 | Littérature ciblée sur srg(99,14,1,2) | P | work/exploration_2026-10-16/uniform_test_2026-10-19/BIBLIO_99_2026-10-19.md:8-27 |
| L08-140 | 10-19 | Théorème 1 (cadre lointain d'une droite) | P | work/exploration_2026-10-16/representation_2026-10-19/NOTE_MANDAT_REPRESENTATION_2026-10-19.md:16-27, 219-288 (+3) |
| L08-141 | 10-19 | Corollaire 2 (droite dans six grilles) : Gram entier de rang 13 | P | work/exploration_2026-10-16/representation_2026-10-19/NOTE_MANDAT_REPRESENTATION_2026-10-19.md:29-31, 292-337 |
| L08-142 | 10-19 | Proposition 3 : portée exacte du registre c = 3 (budget) | P | work/exploration_2026-10-16/representation_2026-10-19/NOTE_MANDAT_REPRESENTATION_2026-10-19.md:33-37, 81-103 (+1) |
| L08-143 | 10-19 | État de la réduction par droites au 19/10 (route c) | S | work/exploration_2026-10-16/representation_2026-10-19/NOTE_MANDAT_REPRESENTATION_2026-10-19.md:66-79 |
| L08-144 | 10-19 | Transfert direct de C3 (gains sur Γ) impossible | P | work/exploration_2026-10-16/representation_2026-10-19/NOTE_MANDAT_REPRESENTATION_2026-10-19.md:343-349, 368 |
| L08-145 | 10-19 | Le lemme de trou lointain P2 non restreint est faux | R | work/exploration_2026-10-16/representation_2026-10-19/NOTE_MANDAT_REPRESENTATION_2026-10-19.md:367, 374-380 |
| L08-146 | 10-19 | DISC sur les gabarits : au plus 39 sommets connus | P | work/exploration_2026-10-16/representation_2026-10-19/NOTE_MANDAT_REPRESENTATION_2026-10-19.md:193-198, 369, 398 |
| L08-147 | 10-19 | Mur de dureté du système proche–lointain d'une droite | E | work/exploration_2026-10-16/reduction_2026-10-19/NOTE_REDUCTION_2026-10-19.md:28-58 |
| L08-148 | 10-19 | Budget d'entropie d'une droite | H | work/exploration_2026-10-16/reduction_2026-10-19/NOTE_REDUCTION_2026-10-19.md:60-87, 225-268 |
| L08-149 | 10-19 | À c = 1, aucune identité linéaire locale au-delà des marges | P | work/exploration_2026-10-16/reduction_2026-10-19/NOTE_REDUCTION_2026-10-19.md:89-104, 199-221 |
| L08-150 | 10-19 | Pourquoi on ne peut pas tout balayer (comptes au 19/10) | E | work/exploration_2026-10-16/reduction_2026-10-19/NOTE_REDUCTION_2026-10-19.md:108-129 (+1) |
| L08-151 | 10-19 | Recommandation du 19/10 : la route finie ne mène pas à une preuve tant que m = 1 n'a pas de méthode finie | H | work/exploration_2026-10-16/reduction_2026-10-19/NOTE_REDUCTION_2026-10-19.md:311-322 |
| L08-152 | 10-19 | Identité de coupe et minoration e(S, S̄) ≥ 3 | P | work/exploration_2026-10-16/reduction_2026-10-19/NOTE_REDUCTION_2026-10-19.md:189-195 |
| L08-153 | 10-19 | srg(243) : aucune droite à c = 1 (pas d'étalonnage pour c ≤ 2) | C | work/exploration_2026-10-16/reduction_2026-10-19/NOTE_REDUCTION_2026-10-19.md:170-187 |
| L08-154 | 10-19 | Ordres de groupe des srg connus à λ = 1 ; conjecture (S3) | O | work/exploration_2026-10-16/treasure_2026-10-19/NOTE_TRESOR_2026-10-19.md:20-37, 163-166 |
| L08-155 | 10-19 | Lois locales candidates de famille : réflexion en un point, fonctions additives sur les droites | C | work/exploration_2026-10-16/treasure_2026-10-19/NOTE_TRESOR_2026-10-19.md:39-66 |
| L08-156 | 10-19 | Contraintes de variance (flag algebras) sur le recensement exact d'ordre 9 : aucun effet | E | work/exploration_2026-10-16/treasure_2026-10-19/NOTE_TRESOR_2026-10-19.md:71-105 |
| L08-157 | 10-19 | Ordre 10 sur AWS : la baisse à P ≤ 692 n'est pas établie ; PL flottant d'ordre 10 non fiable | X | work/exploration_2026-10-16/treasure_2026-10-19/NOTE_TRESOR_2026-10-19.md:107-143 (+1) |

### 3.6 Le 20/10 : de la fusion des routes finies au théorème de réduction du rang 37

| id | date | énoncé court | statut | source principale |
|---|---|---|---|---|
| L08-158 | 10-20 | (R1) Rang 37 : obligation de droite, toutes les droites c ≤ 2 testées réfutées (58/58) | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:26-38 (+1) |
| L08-159 | 10-20 | (R2) La droite c = 2 était le maillon manquant de la chaîne de septembre | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:40-47, 258-263 |
| L08-160 | 10-20 | (R3) Droite c = 1 générique au rang 37 : redécouverte | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:49-55 |
| L08-161 | 10-20 | (R4) Rang 39, résidu de rang 2, droite c = 1 : le moteur de droite complète ne conclut pas | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:57-61 |
| L08-162 | 10-20 | (R5) Trois formes exactes de l'obligation de droite | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:63-74 |
| L08-163 | 10-20 | Ce que l'identité de rang force au rang 37 | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:100-122 |
| L08-164 | 10-20 | Énoncé conditionnel de fusion au rang 37 (version du 19-20/10) | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:173-186 (+1) |
| L08-165 | 10-20 | Coût de l'uniformité au rang 37 : estimations successives | H | work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:188-200 (+2) |
| L08-166 | 10-20 | Lien exact entre le 7-rang d'un bloc à quatre étoiles et le résidu de droite ; les données des lois à quatre étoiles sont impossibles | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:208-232 |
| L08-167 | 10-20 | Une droite c = 1 n'est dans aucune grille ; portée de (H-MATCH) | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:234-248 |
| L08-168 | 10-20 | (B′) + [m ≥ 2 exclu] ⇒ pas de Conway | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:250-256 |
| L08-169 | 10-20 | Ablation au rang 37 : l'obstruction est arithmétique (Green + L2) | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:322-393 (+1) |
| L08-170 | 10-20 | Pour une droite générique, Green est toute l'information 7-adique | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_OBSTRUCTION_2026-10-20.md:17-21, 56-90 |
| L08-171 | 10-20 | L'étoile au rang 37 : Green × couplage ; mort statistique | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_OBSTRUCTION_2026-10-20.md:23-43, 94-133 (+1) |
| L08-172 | 10-20 | Projecteur réel seul, sans rang : filtre fort sur configurations partielles | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_OBSTRUCTION_2026-10-20.md:135-143 |
| L08-173 | 10-20 | Rangs 39 à 43 : l'étoile seule heuristiquement satisfaisable, la double étoile sur-déterminée | H | work/exploration_2026-10-16/merge_2026-10-19/NOTE_OBSTRUCTION_2026-10-20.md:159-167 |
| L08-174 | 10-20 | « Filtre gratuit ÷ 2 » par les droites latérales (L23 pour G_{T_x}) | R | work/exploration_2026-10-16/merge_2026-10-19/NOTE_OBSTRUCTION_2026-10-20.md:178-181 (+1) |
| L08-175 | 10-20 | Vecteurs propres entiers de valeur 3 de norme < 16 (note ChatGPT) | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_CHATGPT_NORMES_12_14_2026-10-20.md:5-36, 52-165 (+1) |
| L08-176 | 10-20 | Prompt Core37 : énoncé visé et Proposition 1 | P | work/exploration_2026-10-16/merge_2026-10-19/PROMPT_CHATGPT_CORE37_2026-10-20.md:112-186 (+1) |
| L08-177 | 10-20 | Réponse de ChatGPT à Core37 : filtre réel uniforme (S3 au sens faible), vérifiée par LAB | C | work/exploration_2026-10-16/merge_2026-10-19/NOTE_CHATGPT_CORE37_VERIF_2026-10-20.md:5-25, 55-87 (+1) |
| L08-178 | 10-20 | Rang 39 avec oblr3 + filtre réel : TIMEOUT | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_CHATGPT_CORE37_VERIF_2026-10-20.md:27-47 |
| L08-179 | 10-20 | Test d'étoile par droite au rang 37 : tous les types c ≤ 3 testés meurent | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BOOST_2026-10-20.md:14-46, 170-195 (+1) |
| L08-180 | 10-20 | Règle de forme δ : correction d'une affirmation de NOTE_BOOST | X | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BOOST_2026-10-20.md:47-54 (+1) |
| L08-181 | 10-20 | Rang 39 : l'étoile tue les droites c = 1 testées (5/5) | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BOOST_2026-10-20.md:57-79, 201-214 (+1) |
| L08-182 | 10-20 | Correction : au rang 39 le filtre réel est un accélérateur (×8), sa nécessité n'est pas établie | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BOOST_2026-10-20.md:73-76 (+1) |
| L08-183 | 10-20 | Coût mesuré au rang 37 et tirage uniforme de 100 000 droites | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BOOST_2026-10-20.md:97-119 (+1) |
| L08-184 | 10-20 | Correction des estimations sur la route c | X | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BOOST_2026-10-20.md:216-234 |
| L08-185 | 10-20 | Plan au rang 37 de NOTE_BOOST §7 : réduction « c ≤ 3 + m = 4 exclu » et comptes | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BOOST_2026-10-20.md:236-280 |
| L08-186 | 10-20 | line37_fast : même sémantique, ≈ 10 fois plus rapide | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_LINE37_FAST.md:11-29, 119-168 |
| L08-187 | 10-20 | Théorème 6.1 : réduction du rang 37 à un test d'étoile fini sur les droites à t ≤ 7 | P | work/exploration_2026-10-16/merge_2026-10-19/THEOREME_REDUCTION_R37.md:22-31, 822-845, 1093-1111 (+1) |
| L08-188 | 10-20 | Lemme 2.3 : au moins 18 droites à t ≤ 7, chacune à c ≤ 4 | P | work/exploration_2026-10-16/merge_2026-10-19/THEOREME_REDUCTION_R37.md:138-208 |
| L08-189 | 10-20 | Décomposition du rang par droite : r = 38 − d + 2r(T) + ρ(T) | P | work/exploration_2026-10-16/merge_2026-10-19/THEOREME_REDUCTION_R37.md:212-299 |
| L08-190 | 10-20 | Encodages du résidu et table des variantes au rang 37 | P | work/exploration_2026-10-16/merge_2026-10-19/THEOREME_REDUCTION_R37.md:301-400 |
| L08-191 | 10-20 | Théorème 4.3 (cadre lointain) et lemmes de l'étoile (4.4-4.7) | P | work/exploration_2026-10-16/merge_2026-10-19/THEOREME_REDUCTION_R37.md:404-559 (+1) |
| L08-192 | 10-20 | Validité des raccourcis du moteur (réduction O(D), règle b₁, découpage par direction de torsion) | P | work/exploration_2026-10-16/merge_2026-10-19/THEOREME_REDUCTION_R37.md:658-710 |
| L08-193 | 10-20 | Audit du code : contraintes exactes fidèles, filtre réel en flottant non rigoureux, relances exactes | E | work/exploration_2026-10-16/merge_2026-10-19/THEOREME_REDUCTION_R37.md:608-656, 712-760, 778-818, 1014-1065 |
| L08-194 | 10-20 | Ce qui manque pour que le calcul du rang 37 devienne une preuve | O | work/exploration_2026-10-16/merge_2026-10-19/THEOREME_REDUCTION_R37.md:864-999 |
| L08-195 | 10-20 | Remarque 6.3 : L23 n'est pas nécessaire au coût près | E | work/exploration_2026-10-16/merge_2026-10-19/THEOREME_REDUCTION_R37.md:847-852, 1067-1077 |
| L08-196 | 10-20 | Remarque 6.4 : trou de la formulation « c ≤ 3 » (droites à t = 12) | P | work/exploration_2026-10-16/merge_2026-10-19/THEOREME_REDUCTION_R37.md:854-860, 1101 |

### 3.7 Le 20/10 : borne de rang, R8/CEGAR, résidus, énumération, ordre 2 en 7, synthèse

| id | date | énoncé court | statut | source principale |
|---|---|---|---|---|
| L08-197 | 10-20 | Pas de preuve de r = 37 ; les outils linéaires ne donnent que des minorations | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:17-27, 229-253 (+1) |
| L08-198 | 10-20 | Proposition 4 : dimension des mots portés par le lointain ; reformulation de r = 37 | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:137-162 |
| L08-199 | 10-20 | Théorème 5 : scindage orthogonal 7-adique à tout rang | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:164-195 |
| L08-200 | 10-20 | Sommets : dim D_v = r − 15 ; formule de la Gram de D_v | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:197-214, 363-371 |
| L08-201 | 10-20 | Proposition 7 : relations forcées entre les droites d'un sommet | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:216-225 |
| L08-202 | 10-20 | Propositions 8-9 : une majoration de r exige des vecteurs spéciaux | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:229-253 |
| L08-203 | 10-20 | Modèle de position générale : aucun argument de dimension ne peut exclure un rang | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:267-289, 306-312, 406-410 |
| L08-204 | 10-20 | Étalonnage du p-rang sur des graphes réels à λ = 1 | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:326-351 |
| L08-205 | 10-20 | Conditions de sommet valables à tout rang ; violées massivement par les témoins SAT de R7 | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:353-385 |
| L08-206 | 10-20 | 7-rangs des 331 objets de rang 30 de l'archive | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:50-57, 367, 373-376 |
| L08-207 | 10-20 | Énoncé ouvert : « tout bloc à quatre étoiles de rang réel 30 a un 7-rang ≥ 25 » | O | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:412-416 |
| L08-208 | 10-20 | Le côté 3 en 7 équivaut à L23 | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:293-305 |
| L08-209 | 10-20 | Prochaine étape recommandée : objet fini uniforme en rang autour d'un sommet (CEGAR) | O | work/exploration_2026-10-16/merge_2026-10-19/NOTE_BORNE_RANG.md:58-64, 420-463 |
| L08-210 | 10-20 | Route R8 : le modèle est sain, R8 UNSAT ⇒ pas de Conway à tout rang | P | work/exploration_2026-10-16/merge_2026-10-19/r8_route/NOTE_R8_ROUTE.md:18-26, 62-158 (+1) |
| L08-211 | 10-20 | Contrôle positif k = 22 de la route R8 | E | work/exploration_2026-10-16/merge_2026-10-19/r8_route/NOTE_R8_ROUTE.md:27-32, 160-178 |
| L08-212 | 10-20 | Renforcements prouvés L4B et XPAIR | P | work/exploration_2026-10-16/merge_2026-10-19/r8_route/NOTE_R8_ROUTE.md:33-38, 180-205 |
| L08-213 | 10-20 | Coût de R8 pur : pas réaliste | H | work/exploration_2026-10-16/merge_2026-10-19/r8_route/NOTE_R8_ROUTE.md:39-48, 212-292 |
| L08-214 | 10-20 | Variante CEGAR spectrale de R8 : une seule itération | O | work/exploration_2026-10-16/merge_2026-10-19/r8_route/NOTE_R8_ROUTE.md:49-60, 294-366 |
| L08-215 | 10-20 | Chaîne de preuve pour qu'un UNSAT de R8 devienne une preuve | O | work/exploration_2026-10-16/merge_2026-10-19/r8_route/NOTE_R8_ROUTE.md:368-398 |
| L08-216 | 10-20 | Règle des classes du résidu pour toute droite équilibrée | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_RESIDU_GLOBAL.md:35-53, 103-221, 410-423 (+1) |
| L08-217 | 10-20 | La classe du résidu n'est pas un invariant global (sauf au rang 37) | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_RESIDU_GLOBAL.md:55-63, 224-256 |
| L08-218 | 10-20 | Théorème B : le contenu 7-adique d'ordre 1 ne dépend pas de la droite de base ; droites latérales inutiles | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_RESIDU_GLOBAL.md:65-91, 273-357 |
| L08-219 | 10-20 | Aucune condition globale entre résidus ne peut exclure 39, 41 ou 43 | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_RESIDU_GLOBAL.md:86-91, 359-383 |
| L08-220 | 10-20 | Énumération exacte des graphes de droite (n = 12) | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_ENUM37.md:16-33 (+1) |
| L08-221 | 10-20 | Énumérateur canonique enum37 : validation | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_ENUM37.md:34-41, 350-370 |
| L08-222 | 10-20 | Pilote enum37 + line37 : 76 418 droites testées UNSAT, mais hors de la cible t ≤ 7 | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_ENUM37.md:42-52, 373-394 |
| L08-223 | 10-20 | Coût projeté de la route du rang 37 (pondéré par λ) | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_ENUM37.md:53-64, 397-432 |
| L08-224 | 10-20 | Aucune condition sur couplages partiels ne décide le test d'étoile | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_ENUM37.md:436-459 |
| L08-225 | 10-20 | Ordre 2 en 7 : UᵀU ≡ 0 et système mod 49, contenu local exact | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_ORDRE2_7ADIQUE.md:29-48 (+1) |
| L08-226 | 10-20 | Théorème §2.3 : avant 7 lointains rien d'ordre ≥ 2 n'agit (cadre générique) | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_ORDRE2_7ADIQUE.md:50-59 (+1) |
| L08-227 | 10-20 | Règles à 7 lointains : corang 1 et (C43) ; un bit à 8 lointains | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_ORDRE2_7ADIQUE.md:60-74 (+2) |
| L08-228 | 10-20 | Gain mesuré nul des conditions d'ordre 2 sur les tests existants | E | work/exploration_2026-10-16/merge_2026-10-19/NOTE_ORDRE2_7ADIQUE.md:76-82, 519-540 |
| L08-229 | 10-20 | Second projecteur réel Π⁽³⁾ : rend redondant le test 7I − H ⪰ 0 | P | work/exploration_2026-10-16/merge_2026-10-19/NOTE_ORDRE2_7ADIQUE.md:84-93 (+1) |
| L08-230 | 10-20 | Rangs 41 et 43 : l'obstacle est la taille de l'arbre | H | work/exploration_2026-10-16/merge_2026-10-19/NOTE_ORDRE2_7ADIQUE.md:95-104, 544-589 |
| L08-231 | 10-20 | Synthèse des mécanismes : état établi selon la synthèse du 20/10 | S | work/exploration_2026-10-16/merge_2026-10-19/SYNTHESE_MECANISMES_2026-10-20.md:13-41 (+1) |
| L08-232 | 10-20 | Routes finies vers l'exclusion (tableau de la synthèse du 20/10) | O | work/exploration_2026-10-16/merge_2026-10-19/SYNTHESE_MECANISMES_2026-10-20.md:72-80, 377-507 |
| L08-233 | 10-20 | Route c selon la synthèse du 20/10 | O | work/exploration_2026-10-16/merge_2026-10-19/SYNTHESE_MECANISMES_2026-10-20.md:311-325 |
| L08-234 | 10-20 | Pourquoi ça meurt et pourquoi parfois non : seuil de surdétermination | H | work/exploration_2026-10-16/merge_2026-10-19/SYNTHESE_MECANISMES_2026-10-20.md:43-70, 195-201, 329-374 |
| L08-235 | 10-20 | Lois locales autour d'un sommet (récapitulatif de la synthèse) | O | work/exploration_2026-10-16/merge_2026-10-19/SYNTHESE_MECANISMES_2026-10-20.md:205-280 |

Décompte des statuts : P = 91, C = 10, E = 63, S = 21, H = 16, O = 22, R = 4, X = 8.

## 4. Maillons non vérifiés dont dépendent les exclusions

| maillon | statut | exclusions ou conclusions qui en dépendent |
|---|---|---|
| P ≤ 852 [L08-067] | E (C selon AUD et SYN, A + E selon THM) | budget de racine ≤ 51 et k ≤ 12 [L08-066] ; registre c = 3 [L08-099] ; m ≤ 4 et Lemme 2.3 [L08-143, L08-188] ; Théorème 6.1 [L08-187] ; ponts Q7, ODD-PURE, N9-NG, T8/T15 [L08-024, L08-027, L08-235] ; branche c4 [L08-053, L08-055] |
| 3P + 4G ≤ 2772 [L08-069] | C | exclusion du gabarit c4 n° 7 à la racine de score minimal [L08-070] |
| E3 [L08-037] | P (Codex, relu par LAB le 17/10) | toutes les familles c3 [L08-102 à L08-116] ; certificats ZC et Z2C [L08-084, L08-133] ; couvertures de Gram [L08-078] ; filtres c = 1 [L08-042, L08-049] |
| verdicts CP-SAT sans certificat portable | S | m = 4 [L08-070, L08-143] ; 23 exclusions c3 à verdict unique [L08-125] ; méthodes P1, P2, PALL, PORB, P4E, ZJ, ZCP [L08-099, L08-124] ; test de Gram V3 [L08-072] (recoupé par HiGHS, toujours sans certificat) |
| code et preuves de Codex non relus par LAB | — | code K3 587f1fdd [L08-108] ; preuve des coupes de continuation (4 des 7 cas de 2K2) [L08-109] ; contraintes hors grille de 2K2NBC [L08-113] ; 5602 (même programme rejoué) [L08-103] |
| filtres de comptage sans objet de preuve | E | environ la moitié des feuilles de K2BC [L08-116] ; 2 890 309 blocs de K3U [L08-108] ; 268 298 raccordements de P3NB [L08-115] |
| moteurs star39, star3, line37, line37_fast | E | toutes les morts d'étoile au rang 37 et au rang 39 [L08-179, L08-181, L08-183, L08-186]. Points faibles : un seul moteur C++ ; un moteur Python indépendant pour (1,1) seulement ; filtre réel en flottant, mais 25 relances exactes [L08-193] ; aucun contrôle positif aux paramètres de Conway ; binaires non recompilés de façon traçable |
| fenêtre r ∈ {37, …, 43} : L22 (P) et r ≤ 35 exclu (C, audit par IA seulement) [L08-231] | P/C | tout raisonnement aux rangs 37-39 ; coupes 7-rang ≤ 28 [L08-205, L08-210 (CEGAR)] |
| L23 [L08-001, L08-176] | P non audité (A selon THM) | écarte 33,6 % des classes du coût de line37 [L08-223] ; non utilisé par le Théorème 6.1 [L08-195] |
| règle de classe δ [L08-216] | P non relu (trois preuves à la main) | runs du rang 39 à δ fixé par la règle [L08-181], sauf la graine 4 ; réduction ×2 |
| constantes RD : det Λ₋(T), χ(det U″) [L08-001] | P non relu | (C43) et la règle de corang 1 [L08-225, L08-227] |
| pont (H-MATCH) ⇒ pas de Conway [L08-235] | P, relu par un agent, modulo L8 | route D de la synthèse |
| exhaustivité de (H₃₇) | O | Théorème 6.1 : échantillons seulement [L08-194] ; pilote hors cible [L08-222] |

## 5. Routes fermées, et pourquoi

**Du 16 au 18/10 (route c, c = 1, m = 4)**
- Hall dans une étoile, graphe de partage, DISC-35 par vecteurs universels : réfutés par calcul [L08-021] — EXP:44-48, 67-72.
- LINE-SUM pour SYM6 (0/16) ; piste « D laplacien » [L08-025] — EXP:149, 165.
- Borne de contraction uniforme pour ODD-PURE : la marge atteint 0,99993 [L08-028] — EXP:210-213.
- R7-NG comme loi structurelle : non crédible après calibration sur srg(243) [L08-029] — EXP:323-325.
- Bornes de trace et force brute CP-SAT à c = 1 — EXP:382-387.
- Flots de Thomson pour b ≥ 1 [L08-034] — EXP:419-421.
- Positivité seule (59 cas sur 63) ; rang seul [L08-043, L08-046] — EXP:563-568, 616-618.
- Quotient de Codex à c = 1, trop grossier — EXP:632-635 ; PRM:264-266.
- SAT de type MinRank ; mod 2 trop faible ; 3-SPEC — EXP:582-586, 615, 747-750.
- Rectangle seul dans les filtres h = TPc [L08-051] — EXP:763-766.
- Gabarits de racine pour c ≤ 2 au niveau de filtre actuel [L08-058] — C21:42-43.
- Famille de codes t7 [16|17,3,*] : plus de temps de calcul ne suffira pas [L08-056] — ANA:32-38.
- Côté Codex : minimum de triangles par composante ; support de norme 42 (SAT) ; coupes spectrales ; Makhnev-Nirova — MOM:83-89, 149-158, 539-552, 606-611.

**18/10 (audit et registre c = 3)**
- Étoile complète seule pour c ≥ 3 : ≈ 23 % de tâches ouvertes pour ≈ 6 500 h-cœur [L08-075] — COST:42-47.
- Fixer l'étoile opposée sur le noyau dur : 0/23 ; coupe R ⪯ 28·Π₀ : 0 exclusion sur 853 [L08-077] — COST:79-89.
- Étoile complète pour c ≤ 2 : ≈ 10⁷ gabarits ; mise en pause plutôt que fermée [L08-074] — COST:110-113.
- Modèle sans Gram comme tueur : une fois corrigé, UNKNOWN [L08-064] — GCOV:198-201.
- E3 dans le PL d'ordre 9 : aucun gain [L08-068] — AUD:245.
- Relèvement de noyau sur les Gram de rang maximal — GCOV:118-119.
- Comptage par rectangle sur le noyau dur c ≤ 2 : épuisé [L08-087] — LEM:198-200.
- Couches de Codex sans fermeture nouvelle : histogrammes seuls, normes variables, couche signée, grid-c2, propagation c4 [L08-088, L08-091, L08-093] — HIST:48-53 ; COUP:24-26, 55-58 ; FERM:36-38 ; C2G:34-35.
- « Les gros blocs sont impossibles pour λ = 1, μ = 2 » : réfuté par srg(243) [L08-089] — MORTS:101-103.

**Nuit du 18 au 19/10**
- Modèles CP-SAT complets : UNKNOWN en 4 min ; remplacés par des énumérations exactes à partir d'un cœur — NUIT:214-215.
- Énumérer d'abord les couplages (skel_engine) ; sonde jointe jkp_probe — NUIT:308-311, 384-385, 396-399 ; P250:35-38.
- P3N seul, K2 seul, étape 1 de 2K2N seule : profils satisfiables [L08-111] — NUIT:263-268, 292-295.
- Carrés de défaut à c = 1 ; familles c3 appliquées à c = 1 [L08-129, L08-128] — NUIT:142-148, 213.
- Identité de second ordre des comptes forcés ; relations universelles seules — NUIT:210-212.
- Réduction orbitale des couvertures (≈ 10 %) ; saturation au rang 7 [L08-122] — NUIT:137 ; R7:69-77.
- Blocs partiels pour fermer 5602 [L08-121] — BLOC:90-98.
- Paires de grilles fermées seules [L08-127] — NUIT:205-207.
- Spectre lointain dans un modèle qui a déjà toutes les C2 — NUIT:45-46.

**19 et 20/10**
- Système proche-lointain d'une droite entière, sans information de rang :
  - mur de dureté à n = 12 ;
  - ≥ 10⁶ années-CPU pour m = 1 [L08-147, L08-150] — RED:28-58, 108-129 ;
  - remplacé au rang 37 par le test d'étoile [L08-179].
- Positivité globale : Gegenbauer projetée, Delsarte des 84 vecteurs, sommets + droites [L08-136] — RENF:18-36.
- Intégralité du recensement : aucune congruence jusqu'à l'ordre 10 (archive) — RENF:54-55.
- Variance (flag algebras) jusqu'à 9 sommets ; PL flottant d'ordre 10 non fiable [L08-156, L08-157] — TRES:94-143.
- Transfert direct de C3 par des gains sur Γ [L08-144] — MAND:343-349.
- DISC sur les gabarits seuls : au plus 39 sommets connus [L08-146] — MAND:193-198.
- Lemme P2 non restreint : faux [L08-145] — MAND:374-380.
- Cadre de fusion des voisinages (bornes de Bachoc) : simple reformulation — MAND:370.
- Moteur de droite complète (oblr, oblr2, oblr3) au rang 39 : TIMEOUT [L08-161, L08-178] — FUS:57-61 ; VERIF:27-47.
- Vecteurs courts et borne d'Hermite : les normes 12 et 14 sont déjà connues ; route Minkowski close (note 110) [L08-175] — NORM:29-36 ; CORE:217-219.
- Séries thêta et comptes de vecteurs duaux pour le rang 37 : épuisés — CORE:220-221.
- Lois à quatre étoiles sur les données de l'archive : elles portent sur des structures impossibles dans Conway [L08-166] — FUS:208-232 ; CORE:222.
- G_T symétriques : la symétrie n'explique pas l'obstruction [L08-169] — FUS:370-393 ; CORE:216.
- Conditions sur couplages partiels pour le test d'étoile [L08-224] — ENUM:452-459.
- Arguments linéaires, de dimension, de genre ou de signes pour majorer r [L08-197, L08-203] — BORNE:229-322, 406-410.
- Côté 3 en 7 : rien de plus que L23 [L08-208] — BORNE:293-305.
- Classe globale du résidu, droites latérales, « filtre gratuit ÷ 2 », conditions globales entre résidus [L08-217, L08-218, L08-219, L08-174] — RES:55-91, 359-383.
- Conditions 7-adiques locales d'ordre 2 (cas générique) ; test 7I − H ⪰ 0 [L08-226, L08-228, L08-229] — ORD2:50-93.
- R8 pur par CDCL sur un cluster [L08-213] — R8:39-48, 368-376.

**Périphérie**
- Couplage linéaire des 174 noyaux avec toutes les occurrences de Makhnev : faisable [L08-002] — CI/DOSSIER_C1_INTEGRE.tex:211-218.
- Relaxations de Jacobi : faisables, même pour P = 0 [L08-005] — CI/antecedents/RECHERCHE_C1_TRANSFERTS.md:337-351.
- Recherches courtes de coexistence V10 : 255 UNKNOWN [L08-017] — RC/RECOVERY_README.txt:29-53.

## 6. Questions ouvertes, par levier

**Certification**
- m = 4 : 79 gabarits CP-SAT [L08-070].
- 23 exclusions c3 à verdict unique, et couverture P2 de gz 155 [L08-125].
- V3, P1 et P2 : DRAT ou Farkas [L08-072, L08-082].
- UNSAT du test d'étoile : passe exacte, second moteur indépendant, format CERT-R37 (LRAT vérifié par cake_lpr) [L08-194].
- Énumération : formule de masse, ou compte complet des 56 λ restants [L08-221].
- Feuilles sans objet de preuve de K2BC, K3U et P3NB [L08-116, L08-108, L08-115].
- C2 au-delà de 4 réseaux sur 156 — SYN:522.

**Production finie**
- Finir P3 : fermerait 7 des 35 ouverts [L08-114].
- Énumération du rang 37 et moteurs à produire [L08-194, L08-223] — SYN:449-453 :
  - torsion, ≈ 2,3·10¹⁰ droites ; non connexes, ≈ 7,5·10⁷ ;
  - types (1,4), (2,4), (4,4), (3,4), d ≥ 5.
- Premier pilote dans la cible : λ = (2⁶), t = 0, 4 157 364 classes, ≈ 1,4 h [L08-222].
- Recensements c_min = 2 et 1 : k = 0, comparaison std/la ; échantillon de 1 000 gabarits m = 2 [L08-073, L08-150] — RED:285-291.

**Méthodes nouvelles sur le registre c = 3**
- 9 gabarits « paire sans outil » et 19 sans paire partagée [L08-126].
- Modèle SAT joint couplages + profils — NUIT:400.
- Lemme « aucune droite dans six grilles », qui tue 7 gabarits [L08-138, L08-141].
- Borne excluant les dimensions de noyau 6 et 7 ; no-good hiérarchique [L08-120].
- Environ 80 couvertures géantes [L08-083].
- Proposition 3 : usage du budget méthode par méthode ; 14 gabarits sans budget [L08-142].

**Branche c ≤ 2 et cas c = 1**
- (II) : comptage global (≥ 33 droites c ≤ 2) à confronter à P ≤ 852 et 3P + 4G ≤ 2772 — SYN:498-499.
- Lois c = 1 :
  - (Q), (B′), H46-c1 [L08-033], (SV1) [L08-042] ;
  - (a ≤ 1) ∧ (b ≥ 1) [L08-034] ;
  - rang_F₃ ≥ 46 [L08-047] ;
  - ODD-PURE (cas couplé) et rang Z [L08-027] ;
  - Q7 [L08-025] ;
  - cas I à IV [L08-040].
- Objet forcé arithmétiquement, comme les normes 18 ou 26, ou certificat uniforme — RED:299-309.

**Rangs 39 à 43**
- Un théorème qui borne r (r = 37, ou r ≤ 39) [L08-197].
- Énoncé ouvert « 7-rang ≥ 25 pour tout bloc à quatre étoiles de rang réel 30 » [L08-207].
- Rang 39 droite par droite : ≈ 1 h × 10¹¹ droites — SYN:491.
- Rangs 41-43 : moteur « sans u » et estimateur de Knuth (critère : 10¹² nœuds par droite) [L08-230].
- Moteur dédié à la double étoile [L08-173].
- Thêta au rang 43 : plafonds par classe de Q₄₃ sur les normes 18 et 26 [L08-209].
- Nécessité du filtre réel au rang 39 [L08-182].

**Sommet et R8**
- Pilote CEGAR [L08-214] :
  - contrôle k = 22 ;
  - convergence à quatre étoiles ;
  - R_k + spectral, k = 1..8.
- Problème à cinq étoiles, plus fort que R8 [L08-210].
- Mesure du gain du cassage de symétrie [L08-212].
- Estimation de Knuth du coût [L08-213].

**Lois locales à pont prouvé**
- (H-MATCH), (N9-NG)/NG5, (T8)/(T15), (N15) [L08-235].
- À tester seulement sur des blocs qui passent DISC et acceptent une colonne extérieure — SYN:503-506.

**Symétrie et asymétrie**
- Conjecture (S3) [L08-154].
- α ≥ 21 dans le cadre des cocliques — SYN:307.
- Exclusion d'α = 21 et branches (0,2) [L08-008, L08-018].

**Relectures**
- E3, P ≤ 852 (dérivation lisible du recensement), règle δ, formules RD.
- Code et preuves de Codex [L08-108, L08-109, L08-113].
- Preuves P du Théorème 6.1 et de ses lemmes [L08-187, L08-189 à L08-192].

**Bornes sur P**
- PL d'ordre 10 certifié, à variables remises à l'échelle et dual rationnel [L08-157] — TRES:158-162.
- Le gain attendu pour la route du rang 37 est faible : la masse des classes est à t ∈ {0, 1, 2} — ENUM:449.

## 7. Contradictions, redécouvertes, remplacements et retraits

**Statuts divergents entre notes**
1. **P ≤ 852** :
   - C pour AUD:232-238 (18/10, « pourquoi c'est une preuve ») et SYN:40, 247 ;
   - « A + E, pas P » pour THM:157, 958, 992-993 (20/10).

   La fiche retient E [L08-067].
2. **L23** :
   - « PROUVÉ » pour CORE:148 ;
   - P pour SYN:41 ;
   - « A, non audité » pour THM:966 (« Hand derivation, not audited »).

   La fiche retient « P non audité » [L08-176, L08-001].
3. **m = 4 exclu** :
   - « 79/79 à la racine de budget » pour SYN:314 ;
   - « 79/79 à la racine minimisant 9s + 8g ; 76/79 pour une racine de budget quelconque (7, 9, 19 non couverts) » pour MAND:77.

   [L08-055, L08-070, L08-143]
4. **Rang 39, dans SYN** : « c'est lui [le filtre réel] qui tue au rang 39 » (l. 159) contredit « sa nécessité n'est pas établie » (l. 180, 350). Seul le second est conforme à la correction 8e7b71cd [L08-182].
5. **Pilote d'énumération** : SYN:447 cite « pilote exhaustif sur 3 types cycliques : 76 418 droites testées, toutes UNSAT ». Il omet que ces trois λ ont t ≥ 8, donc sont hors de la cible t ≤ 7 du Théorème 6.1 (ENUM:50-52), et que seules les classes (1,1) y sont fermées [L08-222].
6. **Gabarit c3 « VÉRIFIÉ »** (C3RC) : ramené à des verdicts de solveur par l'audit (AUD:153-158) [L08-072].

**Estimations remplacées**
7. **Route finie** :
   - 19/10 : « tant que m = 1 n'a pas de méthode finie, la route finie ne mène pas à une preuve », ≥ 10⁶ années-CPU [L08-150, L08-151] ;
   - 20/10 : route finie chiffrée au rang 37, ≈ 6,5·10⁴ heures-cœur [L08-187, L08-223].
8. **Coût de l'uniformité au rang 37** [L08-165, L08-223] :
   - « milliers d'années-CPU » (FUS:191-192) ;
   - « dizaine d'années-CPU », 30 à 80 (OBS:151-157) ;
   - ≈ 8·10⁵ heures-cœur, puis 6,5·10⁴ (BOOST:270-280) ;
   - 5,4·10⁵ et 5 à 6,5·10⁴ (ENUM:53-58).
9. **Nombre de droites c = 2** : 10⁹ à 10¹⁰ (FUS:190) contre ≈ 7·10⁷ (BOOST:262-264).
10. **Fréquence de d = 3** : ≈ 0,05 % (FUS:113, heuristique) contre 0,35 % mesuré (THM:808-809).
11. **Rang 39** : l'heuristique « étoile satisfaisable, ≈ 10⁵ solutions » (OBS:162) contre le calcul (UNSAT 5/5, BOOST §5). L'écart vient du filtre réel, que l'heuristique ignorait [L08-173, L08-181].
12. **Estimation de la route c** (85 % pour « c_min ≥ 2 », 10⁴ à 10⁵ heures-cœur) : retirée [L08-184] — BOOST:216-234.
13. **Liste à c ≤ 3** : jugée « non fermable » le 17/10 (EXP:450), puis liste finie de 10 052 gabarits le 18/10. C'est une nuance, pas une contradiction [L08-036].
14. **m ≤ 4** : dépendait de ρ ≤ 126 le 17/10 (PRM:40-46) ; ne dépend que de P ≤ 852 le 19/10 (MAND:76) [L08-052].
15. **Gabarits sans budget** : +17 le 18/10 (AUD:30, 76) contre +14 le 19/10 (MAND:37 ; SYN:320). L'écart est expliqué : 6 exclus par z2, sans recoupement avec le Gram [L08-072, L08-142].

**Retraits (X) et réfutations (R)**
16. **Bug OR-Tools 9.15** [L08-060, L08-062, L08-063, L08-064] :
    - verdicts retirés : 162 verdicts c3 de Codex (09:34 → 11:40) ; c4 79/79 → 76/79 (11:40), puis refermé à 16:36 ; AWS c3star v1 ; modèle sans Gram du LAB (17:52 → 18:26) ;
    - le motif avait été repéré le 17/10 vers 02:50 dans un autre module (MOM:634-637).
17. **Affirmation de NOTE_BOOST** « aucune règle prouvée ne fixe δ » : fausse [L08-180] — BOOST:47-54 ; RES:184-186.
18. **« Filtre gratuit ÷ 2 » par les droites latérales** : réfuté par le Théorème B [L08-174, L08-218].
19. **Formulation « c ≤ 3 + m = 4 exclu »** : trou des droites à t = 12 (aucun x utilisable), et oubli du type (1,4) [L08-185, L08-196].
20. **ORDRE2, version d'avant revue** : « avant 7 lointains rien n'agit » était surévalué ; portée restreinte après le constat 1 du relecteur [L08-226] — REV:10-21.
21. **Borne P ≤ 692 (AWS, ordre 10)** : artefact numérique ; le PL flottant d'ordre 10 exclut à tort un vrai srg(243) [L08-157].
22. **Premier essai de borne d'Hermite** dans RES : faux, corrigé avant toute conclusion [L08-219].
23. **Coupe spectrale de Claude** (message 595) : retirée au message 596 [L08-018].
24. **« Dizaines de millions de mondes PSD de rang 33 »** : ce n'est pas un résultat de Codex [L08-007].
25. **Réfutés** :
    - les paris 1 à 3 et le pari 6 du 16/10 [L08-021, L08-023] ;
    - ODD9 à c = 1 hors positivité, et (RS) [L08-045] ;
    - le lemme P2 non restreint [L08-145] ;
    - la conjecture de Codex « g1/g2 incomplets » [L08-122].

**Écarts de comptes**
26. 9748 est compté ouvert par le registre alors que Codex l'avait fermé le 18/10. Il est fermé deux fois, le 18/10 et le 19/10 [L08-092, L08-133].
27. Écarts mineurs :
    - ZC : 7 339 contre 7 361, différence de périmètre [L08-084] ;
    - couvertures géantes : 82 contre 80 [L08-083] ;
    - 73 contre 74 survivants [L08-087] ;
    - 1 423 et 1 373 ouverts dans MORTS, alors que le registre commité indique 1 591 [L08-082] ;
    - étape 1 de 2K2 : 11 432 contre 11 832, coquille probable [L08-109] ;
    - « 20 sans paire, 10 sans assez de grilles » (BOOST:223) décrit l'état à 40 ouverts ; à 35 ouverts, on a 19 + 9 + 7 [L08-126].
28. Le prompt du 17/10 annonce une reprise de Codex le 22/10 ; elle a eu lieu le 17/10 vers 23:15 (PRM:50 ; MOM:685-692).

**Redécouvertes (même résultat établi au moins deux fois)**
29. **Spectre lointain d'une droite** {8, 3¹⁸, (−4)^{7+c}, …}, dimensions 7 + c et 18 [L08-035, L08-094, L08-095, L08-140, L08-191]. Occurrences :
    - note Codex 114 (septembre) ;
    - NOTE 17.90 (09/10) ;
    - EXP §A (16-17/10) ;
    - MOM §16 (17/10) ;
    - Codex GRAM_DES_GRILLES (18/10, annoncé nouveau puis requalifié) ;
    - NUIT (19/10) ;
    - MAND, Théorème 1 (19/10) ;
    - BOOST §2.3 (20/10) ;
    - THM, Théorème 4.3 (20/10).
30. **Identité de rang** r = 38 − d + 2r(T) + ρ(T) [L08-162, L08-189] : Codex, notes 124-127 (septembre) ; FUS R5 (19-20/10) ; THM §3 (20/10).
31. **Forme de Green** : Codex note 124 ; FUS ; CORE, Proposition 1 ; THM, Proposition 3.6 [L08-162, L08-176, L08-190].
32. **Mort au rang 37 des droites c = 1 génériques** : Codex et Astra en septembre (« 42/42 »), puis LAB les 19-20/10 [L08-160].
33. **Règle de classe δ** [L08-216, L08-180] : TL 17.80 (corollaire B) ; règle B′ (arbitrée par Codex) ; RD (09/10) ; RES (20/10, trois preuves).
34. **L23** : Codex note 102 (25/09) ; RD (09/10) ; TL 17.80, corollaire A ; BORNE §4.3 (côté 3) [L08-001, L08-208].
35. **Normes 12 et 14** : notes Codex 168, 174, 179, 181, 188, 247 (08/10) ; ChatGPT (20/10) [L08-175].
36. **Proposition 2 de ChatGPT** (degrés 8 + 7h, 240 arêtes) : note Codex 230 (09/10) [L08-177].
37. **P ≤ 1151** par positivité des droites : déjà la note 70 de Codex (Krein) et L16 [L08-136].
38. **Recensement d'ordre 6** (62 types, un paramètre) : census2 (08/10), Reimbayev, moteur du 19/10 [L08-137].
39. **Scindage orthogonal 7-adique** : au rang 37 dans RD ; à tout rang dans BORNE, Théorème 5 [L08-199].
40. **dim D_v = r − 15** : Codex 101-102, puis BORNE, Proposition 6 [L08-200].
41. **Contenu 7-adique des droites latérales** : ORD2:204-206, puis RES Q3 [L08-218].
42. **Classe carrée à 8 lointains** : LAP (TL:2338), confirmée par Codex (TL:2461-2463, note 217) ; reprise par ORD2 [L08-227].
43. **Faits du 18-19/10** :
    - partition co-Heawood (NOTE 17.90/17.95, 09-10/10 → 17/10) [L08-041] ;
    - borne de paires (Codex et ChatGPT, le même 17/10) [L08-038] ;
    - couplage des grilles disjointes (commit hc7 du 18/10 → 19/10) [L08-110] ;
    - E3 (Codex 17/10 → audit du 18/10) [L08-037] ;
    - P ≤ 852 (census2 du 08/10 → 18/10) [L08-067].
44. **Faits sur srg(243)** : « toute droite est dans une grille » (EXP l. 394) ; l'identité de coupe c1_balcut du 17/10. Tous deux repris par RED le 19/10 [L08-152, L08-153].

## 8. Notes lues, survolées, non lues

Sauf mention, les copies `fs` et `git` sont identiques aux fins de ligne près. C'est vérifié par l'agent avec `diff` pour SYN, BOOST, THM, ENUM, ORD2, R8, RES, BORNE, RED et TRES. Le fork C l'a vérifié pour RAP et pour une partie de NUIT.

**Lues intégralement**
- Agent L08 :
  - SYN, THM, FUS, OBS, BOOST, L37F, NORM, VERIF, BORNE, R8, RES, REV ;
  - UNIF, RENF, BIB99, MAND, RED, TRES ;
  - CI/LISEZ_MOI.md.
- Fork A : EXP (786 l.), PRM (504 l.), BIB (116 l.), CGP (14 p.), PLAN, C3RC, C21, RD, MOM (branche aws, 1 010 l.), REPRISE_COMPOSANTES (132 l.), AWS (60 l.), ANA (42 l.).
- Fork B :
  - AUD (278 l.), AUDR (51 l.), AUDG (120 l.), COST (114 l.), GCOV (268 l.), LEM (272 l.), MORTS (104 l.) ;
  - c3o_final_summary.txt, gc1a_summary.txt, two_star_summary.txt, gfm_local/RETRACTED.txt, les fichiers census/*.out et json du dossier audit ;
  - les 7 notes de Codex du 18/10 de la liste (C2G, CARRE, C9748, COUP, FERM, GRAM60, HIST).
- Fork C :
  - NUIT (fs, 401 l. ; version de branche diffée), RAP (fs, et brouillon de branche diffé), INV, P250, aws/SHA256_c3l2_c3p5.txt ;
  - fichiers de clôture et registres (CH/*_closed.json, c3_ledger_now_*.json, c3_open_*.tsv) ;
  - GZ/sample_p3nb.txt, GZ/review_k2bc_2026-10-19/sample1.txt ;
  - les notes de Codex du 19/10 de la liste : HUIT, PART, BLOC, CTRL, R7 et FACT (version de branche).

**Lues en partie (avec les lignes)**
- CORE : l. 30-229, plus un grep des titres.
- ENUM : l. 1-70 et 350-504. Les preuves des §1-3 (l. 68-349) et la table annexe ne sont pas lues.
- ORD2 : l. 1-120 et 519-653. Les preuves des §1-3 (l. 117-518) ne sont pas lues ; elles ont été relues par l'agent adverse (REV).
- AGa : l. 1-72, 1042-1060, 1245-1270, plus un grep. AGe (116 Ko) : l. 1-123 lues, l. 124-360 survolées, l. 361-1766 non lues (14-16/10, hors fenêtre du fork C).
- CI :
  - DOSSIER_C1_INTEGRE.md : tête et grep ;
  - DOSSIER_C1_INTEGRE.tex : l. 175-230, plus grep ;
  - antecedents/AUDIT_C1_ANNEXE.md, NOTE_TRANSPORT_C1.md, RECHERCHE_C1_TRANSFERTS.md : tête et grep.
- RC (sauvegarde du 12/10) :
  - RECOVERY_README.txt (V11) : l. 1-60, 100-182, 205-246 ;
  - RECHERCHE_ACTIVE_C1.md, version la plus récente (asymmetry_trades_617b299) : l. 1-40 et les titres ; les quatre autres versions sont comparées par diff (166, 133, 84 et 31 lignes de différence, toutes des ajouts en tête) ;
  - NOTE_COEXISTENCE_DEFAUTS_COCLIQUES, version f738665 (3 152 l.) : l. 1-30 et les titres ; diff de 248 lignes avec e9c8180, qui correspond aux §66-69 (V13) ;
  - NOTE_SUIVI_SOLVEURS : l. 1-45 ;
  - les 11 messages du pont et les 3 messages de Codex : premiers ≈ 900 caractères de chacun ;
  - les 6 fichiers AGENTS : premiers ≈ 700 caractères ;
  - les 13 fichiers git_bundle_verification (références des commits) ;
  - LATEST_*.txt et process_status_latest.txt.
- Hors lot, lues en complément par les forks : CX/CORRECTION_DOMAIN_ORTOOLS, RETRACTION_LAB_SANS_GRAM, RECALCUL_C4 et RESULTAT_CMIN4 (fork B) ; PREUVE, FERMETURE_2K2, PRODUCTION_K3_UNIVERSELLE et GBC, parcourues (fork C). Elles relèvent probablement du lot L05.

**Non lues, avec la raison**
- Données et journaux du lot :
  - merge_2026-10-19/boost_logs/lines40.txt : 40 droites de validation ;
  - merge_2026-10-19/enum37_logs/pilot_1x12.txt : 790 classes de λ = (1¹²) ;
  - les 20 journaux nobudget_z2/log_*.txt, seulement décomptés : 6 CERTIFICATE, 14 FEASIBLE_DESIGN ;
  - treasure_2026-10-19/e3_zero9.txt (1 type) et e3_zero10.txt (9 types), identifiants de types forcés à zéro par E3, seulement ouverts ;
  - uniform_test_2026-10-19/sdp_cal_list.txt, liste de calibration, seulement survolée ;
  - lg_counts_20000_seed2026.txt, lu (d = 1 : 13 550, d = 2 : 2 232, d = 3 : 56 ; (τ|7) = ±1 : 6 800 et 6 750).
- Copies et sauvegardes :
  - CI/DOSSIER_C1_INTEGRE.pdf, même contenu que le .tex (LISEZ_MOI l. 5-9) ;
  - header.tex, requirements.txt, SHA256SUMS.txt : triviaux ;
  - les versions antérieures de RECOVERY_README (snapshot post_recovery et handover ; scratchpad recovery_x/x_first) : non lues séparément, elles sont antérieures à la V11 lue ;
  - le .bundle et workspace_inventory.json (10 Mo), exclus par prudence.
- Desktop/Recherche_Conway/c1-audit-deps : dist-info d'igraph 1.0.0 et de texttable 1.7.0, sans contenu de recherche.
- Listes du scratchpad :
  - work/scratchpad_LAB_2026-09-30/files/{diff,loc,rem}_exploration_2026-10-16.txt (20/10, 17:56) : listes de synchronisation de copies. diff contient 230 entrées « MISSING », sans contenu mathématique. Seulement survolées ; leur interprétation exacte (quelle troisième copie manque) n'est pas établie.
- Desktop/Recherche_Conway/c1-p3-export (cité dans la mission) : ses notes sont des doublons affectés par l'inventaire aux lots L06 et L07. Aucun contenu distinct n'appartient à L08.
- Code, binaires et données des dossiers gz5602, cpp_census*, line_spectrum, unbiased_walks, r8_route/data et enum37_tools : ce ne sont pas des notes. Le fork B a lu les en-têtes de quelques scripts ; line_spectrum_control a été ouvert pour L08-095.

## 9. Matériaux pour la recombinaison

### 9.0 Abréviations

| abréviation | chemin |
|---|---|
| EXP, PRM, BIB, CGP, PLAN | work/exploration_2026-10-16/ EXPLORATION.md ; PROMPT_RECHERCHE_C1_c1_2026-10-17.md ; BIBLIO_C1_2026-10-17.md ; NOTE_CHATGPT_C1_2026-10-17.pdf (pages) ; PLAN_C_LE_3_2026-10-18.md |
| C3RC, C21 | work/exploration_2026-10-16/c3_root_cover/C3_ROOT_COVER_2026-10-18.md ; …/c21_root_census/C21_ROOT_CENSUS_PARTIAL_2026-10-18.md |
| RD | work/c1_index_2026-10-09/NOTE_RESEAUX_DE_DROITE.md |
| AUD, AUDR, AUDG | work/exploration_2026-10-16/audit_2026-10-18/ AUDIT_EXCLUSIONS_2026-10-18.md ; AUDIT_RAPIDE_2026-10-18_soir.md ; AUDIT_GLOBAL_2026-10-18_nuit.md |
| COST, GCOV | work/exploration_2026-10-16/c3_cost_2026-10-18/ C3_COST_PILOT_2026-10-18.md ; C3_GRAM_COVER_2026-10-18.md |
| LEM | work/exploration_2026-10-16/lemmas_c12_2026-10-18/LEMMES_C12_2026-10-18.md |
| CH/, MORTS, NUIT, RAP, INV, P250 | work/exploration_2026-10-16/c3_hard_core_2026-10-18/ ; MORTS_ET_SURVIVANTS_C3_2026-10-18.md ; NUIT_2026-10-19.md ; RAPPORT_MATIN_2026-10-19.md ; c3_inventaire_2026-10-19.md ; PLAN_250_2026-10-19.md |
| GZ/ | work/exploration_2026-10-16/gz5602_2026-10-19/ |
| UNIF, RENF, BIB99 | work/exploration_2026-10-16/uniform_test_2026-10-19/ NOTE_TEST_UNIFORME_2026-10-19.md ; NOTE_ENONCE_RENFORCE_2026-10-19.md ; BIBLIO_99_2026-10-19.md |
| MAND, RED, TRES | work/exploration_2026-10-16/ representation_2026-10-19/NOTE_MANDAT_REPRESENTATION_2026-10-19.md ; reduction_2026-10-19/NOTE_REDUCTION_2026-10-19.md ; treasure_2026-10-19/NOTE_TRESOR_2026-10-19.md |
| FUS, OBS, BOOST, L37F, NORM, CORE, VERIF, THM, BORNE, R8, RES, ENUM, ORD2, REV, SYN | work/exploration_2026-10-16/merge_2026-10-19/ NOTE_FUSION_2026-10-19.md ; NOTE_OBSTRUCTION_2026-10-20.md ; NOTE_BOOST_2026-10-20.md ; NOTE_LINE37_FAST.md ; NOTE_CHATGPT_NORMES_12_14_2026-10-20.md ; PROMPT_CHATGPT_CORE37_2026-10-20.md ; NOTE_CHATGPT_CORE37_VERIF_2026-10-20.md ; THEOREME_REDUCTION_R37.md ; NOTE_BORNE_RANG.md ; r8_route/NOTE_R8_ROUTE.md ; NOTE_RESIDU_GLOBAL.md ; NOTE_ENUM37.md ; NOTE_ORDRE2_7ADIQUE.md ; ordre2_2026-10-20/REVUE_AGENT_2026-10-20.md ; SYNTHESE_MECANISMES_2026-10-20.md |
| MOM, MOMm, AWS, ANA, AGa, AGe | conway99-c1:origin/lab/aws-codex-7-9-19:notes/MOMENTS_SIGNATURES_C1_2026_10_16.txt ; conway99-c1:origin/main:(même chemin) ; …aws-codex-7-9-19:notes/AWS_7_9_19_2026_10_18.txt ; …aws-codex-7-9-19:data/codex_line_resonance_20261016/aws_v1_runs/ANALYSE_AWS_V1_2026-10-18.md ; conway99-c1:origin/lab/aws-codex-7-9-19:AGENTS.md ; conway99-c1:origin/lab/exploration-2026-10-16:AGENTS.md |
| CX/, HUIT, PART, BLOC, R7, CTRL, CARRE, HIST, C9748, GRAM60, C2G, COUP, FERM | Desktop/Recherche_Conway/c1-main-codex/notes/ ; COEUR_HUIT_SOMMETS_5602_2026_10_19.txt ; COEUR_PARTAGE_DEUX_GRILLES_2026_10_19.txt ; BLOCS_PARTIELS_ET_COUPE_ENERGIE_2026_10_19.txt ; RANG7_ET_SATURATION_2026_10_19.txt ; CONTROLE_C2_COUCHES_2026_10_19.txt ; CARRE_DE_DEFAUT_ET_PARITE_2026_10_18.txt ; HISTOGRAMMES_PROPRES_SANS_GRAM_2026_10_18.txt ; CERTIFICAT_SANS_GRAM_9748_2026_10_18.txt ; GRAM_DES_GRILLES_ET_BLOC60_2026_10_18.txt ; C2_DES_GRILLES_2026_10_18.txt ; COUPLAGES_SIGNES_ET_COINS_SANS_GRAM_2026_10_18.txt ; FERMETURES_ET_ABLATIONS_SANS_GRAM_2026_10_18.txt |
| FACT | conway99-c1:origin/lab/exploration-2026-10-16:notes/FACTEURS_QUATRE_COULEURS_2026_10_19.txt |
| CI/, RC/ | Desktop/Recherche_Conway/c1-imports/2026-10-09-convergences/DOSSIER_C1_CONVERGENCES/ ; Desktop/Recherche_Conway/RECOVERY_2026-10-12/ |
| TL (cité) | work/c1_theta_lp_2026-10-07/NOTE.md (hors lot) |

### 9.1 Énoncés conditionnels « si X alors … »

**(a) Conclusion : pas de Conway (à tout rang, sans hypothèse de symétrie)**
- [P] R8 UNSAT ⇒ pas de Conway. Le modèle est audité sain ; le problème à cinq étoiles, plus fort, suffit aussi [L08-020, L08-210] — EXP:16-17 ; R8:24-26, 107-116.
- [P] Q7 ⇒ pas de Conway, via P ≤ 852 et une paire sans grille avec c_min ≤ 4 ; Q7 ⟸ ODDCONST + SYM6 [L08-024, L08-025] — EXP:128-130, 148.
- [P] Pour c ≤ 4, paires sans grille, côté c minimal : ODD-PURE + rank Z ≥ c − 1 + P ≤ 852 ⇒ pas de Conway. ODD-PURE seul exclut c = 1 [L08-027, L08-032] — EXP:182-190.
- [P] R7-NG (« tout bloc PSD sans grille a rang_F7 ≥ 29 ») ⇒ pas de Conway [L08-029] — EXP:242.
- [P] H46-c1 ⇒ aucune droite c = 1 ; H46-c1 ⟸ ODDCONST [L08-033] — EXP:363-364, 402.
- [P] (a ≤ 1) ∧ (b ≥ 1) ⇒ aucune droite c = 1 [L08-034] — EXP:411.
- [O] (SV1) ⇒ aucune droite c = 1 [L08-042] — EXP:549-551.
- [P] Une réponse « non » à (Q) ⇒ aucune droite c = 1 — PRM:287-288.
- [P] « c(l) = 1 ⇒ rang_F₃(A_Ω) ≥ 46 » exclurait c = 1, puisque Conway impose rang_F₃(A_Ω) ≤ 45 [L08-047] — EXP:646-647.
- [P] (B′) + [m ≥ 2 exclu] ⇒ pas de Conway [L08-168] — FUS:255.
- [O] Pari 5 + N9-NG complet + P ≤ 852 ⇒ contradiction [L08-023] — EXP:101-103.
- [P, rappel] Ponts de la synthèse, statuts d'origine en L07 [L08-235] — SYN:231-246 :
  - (H-MATCH) ⇒ pas de Conway (relu par un agent adverse, modulo L8) ;
  - (N9-NG)/NG5 + P ≤ 852 ⇒ pas de Conway (vérifié par Codex) ;
  - (T8) ou (T15) + P ≤ 852 ⇒ pas de Conway.
- [O] (S3) « tout srg à λ = 1 a un automorphisme d'ordre 3 » + C3 exclu ⇒ pas de Conway [L08-154] — TRES:35-37.
- [P, rappel] Le cadre des cocliques fermerait C1 avec α ≥ 21 — SYN:307.
- [H] DISC-35 tuerait Conway [L08-021] — EXP:36-37.

**(b) Conclusion : un rang exclu**
- [P] (H₃₇) ⇒ r ≠ 37 (Théorème 6.1, sous P ≤ 852 seulement) [L08-187] — THM:822-845. Forme c ≤ 4 (Corollaire 6.2) — THM:841-845.
- [P] Core37 pour tout G admissible avec (τ|7) = −1 ⇒ maillon 1 uniforme. Avec les maillons 2, 3, 5 et P3 ⇒ r ≠ 37 (version du 19-20/10, remplacée par le Théorème 6.1) [L08-164, L08-176] — CORE:151 ; FUS:183-186.
- [O] « Tout bloc à quatre étoiles de rang réel 30 a un 7-rang ≥ 25 » ⇒ r ∈ {41, 43} (37 et 39 exclus) [L08-207] — BORNE:414-415.
- [P] (K22) « ν ≥ 14 ⇒ rang_F7(8T_S) ≥ 23 » exclurait r = 37. Pour les paires à droite c = 1 générique, (K22) équivaut à l'échec de la double étoile [L08-166] — FUS:221-223.
- [P] Le lemme P2 restreint et une normalisation couvrante qui fournit une droite où il s'applique ⇒ exclusion du rang 37 [L08-145] — MAND:367, 404-407.
- [P cond.] N14 (aucun vecteur de norme 14 au rang 37, calcul non audité) ⇒ le cas I de c = 1 est vide au rang 37 [L08-041] — EXP:517-519.
- [P] Pour une droite générique : r = 37 ⟺ Π_T 7-entier ⟺ D n'a aucun mot non nul porté par le lointain (une seule droite suffit) [L08-170, L08-198] — OBS:72-74 ; BORNE:161-162.
- [P] r ≤ 45 − m ⟺ il existe m vecteurs de E₋ dont la Gram est inversible mod 7 ; de même r ≤ 55 − m′ côté E₃ [L08-202] — BORNE:231-236.
- [P] Monotonie (Théorème B, B3) : (ii) au rang r ⇒ (ii) au rang r′ > r. Un test au rang 43 est une relaxation valable pour toute la fenêtre [L08-218] — RES:314-317.
- [H] Critère de décision : si l'estimation de Knuth dépasse ≈ 10¹² nœuds par droite au rang 41, la route droite par droite est close aux rangs 41 et 43 [L08-230] — ORD2:587-590.

**(c) Conclusion : une branche m, un cas ou une famille exclus**
- [P] Dichotomie (I)/(II) [L08-057] — PLAN:20-23 :
  - si au plus 32 droites ont c ≤ 2, il existe une racine dont les 7 droites ont c ≥ 3 ;
  - sinon, au moins 33 droites c ≤ 2 couvrent tous les sommets.
- [S] c_min = 4 exclu ⇒ c_min ≤ 3 [L08-070] — PLAN:29.
- [P] Proposition 3 [L08-142] — MAND:83-90 :
  - registre c = 3 fermé ⇒ m = 3 global exclu ;
  - pour la branche (I), il faut en plus traiter les gabarits à plus de 12 grilles et des méthodes sans le budget s ≤ 51.
- [O] « Aucune droite dans six grilles » ⇒ tue 9302, 9791, 9912, 9966, 10003, 10006 et 10025, et supprime c = 6 de toutes les branches [L08-138, L08-141] — MAND:366 ; RENF:103.
- [C+P] 3P + 4G ≤ 2772 ⇒ 9s + 8g ≤ 504 au sommet de score minimal. Sous c ≥ 4 global : g ≥ 7, s ≤ 49, et le gabarit c4 n° 7 est exclu. Ce choix de racine ne se cumule pas avec un autre [L08-069] — AUD:249-261.
- [P] P ≤ 852 ⇒ budget τ(v) ≤ 51 et k ≤ 12 à la racine de budget [L08-066] — AUD:132-136.
- [E, sous E3] Règle C4 + C3 : si le graphe des grilles contient C4(X) + C3(Y), les deux diagonales du C4 sont des grilles [L08-104] — HUIT:232-250.
- [E, sous E3] Familles exclues, chacune avec ses hypothèses exactes :
  - T23 [L08-105] — PART:5-12 ;
  - K3U [L08-108] — CH/k3u_closed.json:1 ;
  - 2K2 [L08-109] — CH/k2k2_closed.json:2 ;
  - P3NB [L08-115] — CH/p3nb_closed.json:2 ;
  - K2BC [L08-116] — CH/k2bc_closed.json:2 ;
  - 2K2N + B/C [L08-113] — CH/k2k2n_bc_closed.json:2.
- [H, Codex] Si K3 et 2K2 sont fermées, alors les grilles sur les 4 autres droites forment une étoile [L08-118] — RAP:56-57.
- [P] Un cycle impair de blocs-paires dans Ĵ ⇒ H = 0, donc des grilles, donc une contradiction [L08-089] — MORTS:76-78.
- [P] FG : sans marche fermée alternée de Ĵ par un rectangle non grille q, le gabarit est impossible [L08-085] — LEM:42-55.
- [P] R1 : si aucune ligne n'a h(q) ≥ 1, alors R_qq = 0 < 4 : contradiction [L08-087] — LEM:169.
- [P, Codex] Lemme du carré de défaut. Si deux rectangles de T sont des grilles et que H_F = H_D pour un D disjoint de F, le gabarit est impossible [L08-090] — CARRE:13-46.
- [C] gz 9748 : si les comptes imposent 9S01 + 9S23 + 2S45 ≥ 484, on contredit S_F ≤ 24 [L08-092] — C9748:8-14.
- [P] Lemme de moyenne. Si la moyenne Γ̄ sur le groupe d'ordre 128 vérifie T, U ⪰ 0, aucune combinaison de coupes de positivité et d'inégalités linéaires ne ferme le cas [L08-043] — EXP:563-567.
- [P] Une paire (l, m) en grille donne une composante prisme de G_l, donc une droite avec c(l) = 1 n'est dans aucune grille. (H-MATCH) aux 21 paires de v ⇒ aucune droite par v n'a c = 1 [L08-167] — FUS:236-240.
- [P] Au rang 37 : 2r(T) + ρ(T) = d − 1. Une droite c = 1 avec d = 2 est équilibrée, avec ρ = 1. Pour c ≥ 3, ρ ≥ 2 [L08-163, L08-189] — FUS:106-122 ; THM:291.
- [E] Au rang 37, l'obstruction d'étoile demande Green × couplage λ = 1 : sans l'un ou l'autre, pas de mort [L08-171] — OBS:27-33.

**(d) Structure : « si X alors Y » (outils réutilisables)**
- [P] Formes du résidu et énoncés valables pour toute droite ou toute droite générique [L08-190, L08-191, L08-140, L08-198, L08-199, L08-217, L08-218] — THM:301-559 ; MAND:219-288 ; BORNE:137-195 ; RES:224-317 :
  - encodage du résidu, Proposition 3.5 ;
  - forme de Green, Proposition 3.6 ;
  - cadre lointain, Théorème 4.3 ;
  - Proposition 4 ;
  - Théorème 5 ;
  - Théorème B.
- [P] Si c(T) = 6, alors 420Π_T est entier, de rang 13 et de diagonale 91 [L08-141] — MAND:303-308.
- [P] Si A et B sont non-grilles disjoints avec H_A = −H_B (sous E3), alors e_A = e_B = 2, R_AA = R_BB = 4, R_AB = −4, et Q_A ∪ Q_B est cubique [L08-102] — HUIT:4-36.
- [P] Si H_C = −H_D pour deux non-grilles partageant une droite, alors Q_C ∪ Q_D est C8 ou C4 + C4 [L08-106] — PART:30-48.
- [P] Si H01 = −H02 ≠ 0 et que Q12 est une grille, alors T = Σ F_j [L08-107] — FACT:10-58.
- [P] Une grille Q_bd (d ∉ {a,b,c}) est en couplage parfait avec Q_ac ; deux grilles disjointes sont couplées parfaitement [L08-117, L08-110] — P250:28-29 ; NUIT:286-291.
- [P, Codex] Si H_A + H_B + H_X + H_Y − H_C − H_D = 0, avec X et Y disjoints de C, alors [R_CC = 8 et R_AC + R_BC ≤ −1] ⇒ une forme quadratique de R vaut au moins 104 [L08-121] — BLOC:65-70.
- [P, Codex] Sur tout bloc principal S = R[I,I] : h_w[I] ∈ im(S) et h_w[I]ᵀS⁺h_w[I] ≤ 5/2 [L08-121, L08-079] — BLOC:9-17 ; GCOV:123-153.
- [P] Toute grille domine parfaitement les 90 sommets extérieurs ; c'est propre à k = 14 [L08-093, L08-039] — GRAM60:16-21 ; MOM:912-916.
- [P] Si L est dans 6 grilles, Spec B est forcé, avec 13 directions −4 portées par D [L08-094] — GRAM60:59-71.
- [P] Pour toute composante K de G_{l_a} : A[D_a] d^K = −d^K. Cela vaut pour tout srg(v,k,1,2) [L08-088] — LEM:240-244.
- [P] Pour Γ 14-régulier sur 99 sommets : 27I − 9A + J ⪰ 0 et 44I + 11A − 2J ⪰ 0 ⟺ srg(99,14,1,2) [L08-013] — RC/snapshot_20261012T113936Z/bridge/messages/codex_20261012_global_effectif.txt.
- [P] Coclique de 21 dont tout sommet extérieur a au plus 4 voisins ⇒ elle se prolonge en une coclique de 22 [L08-008] — RC/coexistence_f738665_20261013T193425Z/repo/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:8-25.
- [P] Si DDᵀ = 12I + 2J − B − B² est binaire avec un voisinage complet (V6, ou tout bord régulier en V13), alors les complétions sont exactement E = E₀ + 3P − 7Q, entières [L08-009] — RC/RECOVERY_README.txt:111-121.
- [P] Un 4-cycle de transport impose H₀ ou H₁ (12 sommets) et l'un de cinq systèmes de bord [L08-003] — CI/antecedents/NOTE_TRANSPORT_C1.md:87-105.
- [P] Il n'existe pas d'extension métrique de ℚ(√−15) qui préserve les 8 triangles de Wagner ou les 12 points du Cube. Cela interdit des constructions d'outil, pas le graphe [L08-002] — CI/DOSSIER_C1_INTEGRE.tex:202-210, 1016.

### 9.2 Bornes quantitatives (objet, inégalité, statut)

**P, G, prismes**
- P ≤ 852 (certificat 11088/13 − P) [L08-067] — E, ou C selon les notes — AUD:232-238 ; THM:157-174.
- P ≤ 1151 par la positivité sommets + droites [L08-136] — E — RENF:29.
- 0 ≤ P ≤ 1386 à l'ordre 6 [L08-137] — E — RENF:48-49.
- P = 1386 exclu (Makhnev 1988) [L08-139] — P, publié — BIB99:8-12.
- Ordre 9 avec flag algebras : max P = 852,923, grilles max 126 [L08-156] — E — TRES:96-101.
- Ordre 10 en flottant : 692,39 non établi [L08-157] — X — TRES:121-128.
- 3P + 4G ≤ 2772 [L08-069] — C — AUD:249-251.
- N0 = 3696 − P, N1 = 16632 + 3P, N2 = 4158 − 3P, N3 = P [L08-139] — P, redérivé — BIB99:13-16.
- P = Σ_r côtés(r)/6 = 6G + Σ_r s′(r)/6 [L08-139] — P — RENF:80-81.
- Σ_T t(G_T) = 2P [L08-188] — P — THM:140-155.
- N(K2 + 4K1) = 9P + 275 371 866 [L08-137] — E — RENF:48.

**Droites et racines**
- Au moins 18 droites ont t ≤ 7 ; pour elles c ≤ 4 et chaque classe a au moins 5 sommets hors triangle [L08-188] — P — THM:176-198.
- τ(v) ≤ ⌊6·852/99⌋ = 51 ; k ≤ 12 grilles [L08-066] — P — AUD:132-136.
- 9s + 8g ≤ 504 ; sous c ≥ 4 : g ≥ 7, s ≤ 49 [L08-069] — P — AUD:256-258.
- dim ker C ≥ max_i(6 − c_i) (filtre K) [L08-036] — P — EXP:439-446.
- dim ker C peut valoir 7 (exemple K7 − C7) [L08-057] — E — MOM:1004-1010.
- −8 ≤ R_ef ≤ 4 ; R_ee = 8 − 2e ; R_ii ∈ {4, 6, 8} ; R ⪯ 28I ; tr R ≤ 28 dim ker C [L08-065, L08-037] — P — AUD:110-117.
- ‖H_F‖² = 56 − 14e ; hᵀR⁺h ≤ 5/2 ; signatures dans [0,2], [−2,0], [−3,1] [L08-079, L08-132] — P — GCOV:132-133 ; UNIF:20.
- ‖h‖² ≥ m² + 7|m| ; borne de paire ; 6|Σ_L h| ≤ S ≤ ‖h‖²/2 [L08-038, L08-091] — P — MOM:410-430, 957-972.
- S_F ≤ 24 ; plans e + a ≤ 2, 2e + 2a + b ≤ 8, 5e + 5a + b ≤ 11, 11e + 12a + 2b ≤ 24 [L08-091] — P — HIST:29-34.
- e(S, S̄) ≥ 3 si q est impair [L08-152] — P — RED:193-195.
- Coclique de 21 : aucun sommet extérieur à 6 ou 7 voisins ; 2 à 6 sommets à 5 voisins ; au plus 30 sommets déviants [L08-008] — P.

**Comptes de gabarits et de classes**
- c ≥ 3 : 510 926 gabarits (k ≤ 12), 500 874 Gram-infaisables, 10 052 ouverts ; 10 069 sans budget [L08-072] — S — AUD:76.
- Survivants des filtres par k, de 0 à 21 [L08-071] — E — AUD:17-18.
- c = 2, k = 12..4 : 0 ; 6 ; 59 ; 609 ; 4 892 ; 32 212 ; 170 144 ; 732 827 ; 2 502 807 [L08-073] — E — AUD:183-184.
- c = 1, k ≥ 1 : 4 708 882 classes à S7 près ; FG en tue 2 406 345 [L08-073, L08-086] — E — LEM:202-224.
- m = 2 : 3 443 556 gabarits, k = 4..11 (2 002 986 avec --la) [L08-150] — E — RED:114.
- Estimation de Knuth pour c ≤ 2 : ≈ 10⁷ gabarits à symétrie près [L08-074] — H — COST:96-113.
- Registre c3 :
  - 35 ouverts, répartis en 7 P3, 9 paire sans outil et 19 sans paire [L08-099, L08-126] — O ;
  - 23 exclusions à verdict unique [L08-125] — S ;
  - trajectoire 1 591 → … → 35 [L08-100] — E.
- Classes de graphes de droite (n = 12) [L08-220] — E — ENUM:16-26 :
  - 187 381 435 694 au total ;
  - 147 579 095 390 admissibles ;
  - t ≤ 7 : 187 379 400 048, dont 147 577 214 193 admissibles ;
  - estimation à action libre 187 207 063 312,5 ; rapport 1,000931.
- |Λ| = (2⁶·6!)³·6 ≈ 5,87·10¹⁴ [L08-187] — P — THM:102-103.
- Fractions des classes [L08-223, L08-185] — E — ENUM:402-407 ; BOOST:258-269 :
  - par statut : K < 0 21,24 % (exact), disconnected 0,04 %, torsion 12,2 %, L23 33,6 %, testées 33,1 % (≈ 6,2·10¹⁰) ;
  - par d, parmi les connexes : d = 1 85,6 %, d = 2 14,1 %, d = 3 0,35 % ;
  - nombres de droites : c = 2 ≈ 7·10⁷, c = 3 ≈ 2·10⁵.
- 33 754 droites testées sur 100 000 tirages, toutes UNSAT ; à 95 %, survivantes < 9·10⁻⁵ [L08-183] — E — BOOST:116-119.
- Pilote : 790 / 29 836 / 182 221 classes ; 10 191 + 66 227 UNSAT ; 206 no-x [L08-222] — E — ENUM:44-48.
- Rang 37 : 118 droites, 262 runs UNSAT ; 898 droites et 1 067 runs, aucune feuille [L08-179, L08-193] — E — BOOST:16-33 ; THM:1014-1027.
- Rang 39 : 5 étoiles UNSAT ; 85 à 255 M nœuds ; 114 505 à 153 268 candidats [L08-181] — E — BOOST:203-211.
- R8 [L08-210 à L08-213] — R8:94-108, 131-133, 180-194, 217-245 :
  - 52 labels, 1 326 variables d'arête ;
  - M₀ : 10 395 couplages, 52 orbites sous G₀ (d'ordre 768) ; groupe d'ordre 3 072 ;
  - L4B : Σκ = 8 ; XPAIR ≤ C(8,2) = 28 ;
  - lookahead : 5,7·10¹³ cubes à la profondeur 40 ; rattachements de X : ≈ 10³⁷ à symétrie près.
- c_min = 4 : 2²¹ graphes → 221 types → 12 951 choix → 367/200 → 100 → 87 → 79 [L08-053] — S — AGa:14-45.
- 174 noyaux : 63 exclus par positivité, 136 par certificat entier [L08-004] — C — CI/antecedents/AUDIT_C1_ANNEXE.md:59-101.
- Échanges de Hoffman : 36 classes, dont 29 asymétriques et 7 à automorphisme d'ordre 2 [L08-010] — E.
- Design des six grilles : plus de 536 classes de colonnes à S6 × S3 près [L08-138] — E.

**Rangs, dimensions, multiplicités, spectres**
- r ∈ {37, 39, 41, 43} : L22 (P) ; r ≤ 35 exclu (C, audit IA) [L08-231] — SYN:35-38.
- rang₇ M_NN = 38 − d ; dim ker = d + 1 ; 0 ≤ r(T) ≤ d − c [L08-189] — P — THM:216-299.
- dim C(T) = ρ(T) + r(T) ; dim D_v = r − 15 ; relations ≥ 6r − 244 (2 au rang 41, 14 au rang 43) [L08-198, L08-200, L08-201] — P — BORNE:142, 204, 219-222.
- Cadre lointain [L08-191, L08-140] — P — THM:445-454 :
  - rang E = 35 − c ; dim ker E = 25 + c ;
  - spectre de R sur ker E : 3 (×18), −4 (×(7 + c)) ;
  - rang Π_T = 7 + c ; 0 ⪯ H ⪯ 7I.
- Σ_{n∈C₁} K(x, n) = 20 pour tout G étiqueté [L08-191] — P — THM:511-526.
- 7-rang d'un bloc à quatre étoiles ≤ r − 15 ≤ 28 ; rang réel ≤ 30 [L08-205, L08-206] — P — BORNE:357-359.
- 331 objets de l'archive : 204 de 7-rang 29 ou 30, 127 de 7-rang 25 [L08-206] — E — BORNE:367.
- Témoins R7 [L08-205] — E — BORNE:365-366, 377-383 :
  - 8 valeurs propres négatives, rang 47, 7-rang 47 ;
  - bases : rang 40, 7-rang 39-40 ;
  - plus petits blocs non semi-définis : 9 à 11 labels.
- rang_F7(8T_S) ≥ 30 observé sans grille, jusqu'à 25 avec grille [L08-029, L08-054] — E/H — EXP:236-240 ; AGa:3-4.
- Exigences et observations à une droite ou une boule [L08-022, L08-024, L08-031, L08-032, L08-047] — P (exigences) / E (données) — EXP:97-100, 124-127, 336, 352-353, 641-653 :
  - ν(T_S) ≥ 14 ; corank Q ≥ 12 − c(l) ; rank F ≤ 7 + c(l) ;
  - dim ker F ≥ 12, données 5 à 8 ;
  - mult_3(A_Ω) ≥ 14 et rang_F₃(A_Ω) ≤ 45 ; données 47 à 55.
- Γ_v a le spectre 12, 3^40, 0^7, (−2)^6, (−4)^30 [L08-030] — P — EXP:307-311.
- p-rangs — E — BORNE:328-347 [L08-204] ; TRES:62-64 [L08-155] :
  - hémisystèmes srg(378,52,1,8) : rang₃ = 104, rang₅ = 90, pour une borne de 105 ;
  - BvLS : rang₃ = 67 ; à 99, rank₃(A + I) = 55 exactement (P) ; dim Z₃ ∈ [1, 44].
- Normes des vecteurs propres entiers de valeur 3 : ‖f‖² < 16 ⇒ 12 (H12) ou 14 (H14) [L08-175] — P — NORM:54-63.
- Borne d'Hermite dans Λ₃(T) : norme ≤ 30 au rang 37, ≤ 38, 48, 60 aux rangs 39, 41, 43 [L08-001] — P — RD:47-51.
- Thêta au rang 43 : il faudrait 2a₈ + 16a₉ + a₁₃ ≥ 2632 [L08-209] — A — BORNE:461-463.
- (C43) retire 11 à 14 % des configurations à 7 lointains ; règle du corang 1 : ≈ 7 % [L08-227] — E et H — ORD2:60-68.
- Profondeur de mort de l'étoile : au plus 3 lointains au rang 37, au plus 5 au rang 39 (préfixes) [L08-228] — E — ORD2:519-540.
- Gros chiffres du dossier du 09/10 [L08-002] — P/E — CI/DOSSIER_C1_INTEGRE.tex:187-200 :
  - déterminants 3 456 et 9 408 ; 253 125 et 275 625 ;
  - orthogonal de rang 32 ; 18 vecteurs de norme 4.
- Transport T(Γ) : graphe 2-régulier sur les 4 158 non-arêtes [L08-003] — P.
- Ordres de groupe des srg λ = 1 connus [L08-154] — C/A — TRES:22-30 :
  - 72 ; 720 ; 51 840 ;
  - 3 849 120 ; 4 320 ; 864 ; 3 888 ; 2 916 ; 108 ; 162 ; 108 ;
  - 6.

**Heuristiques de seuil et coûts**
- Espérance du nombre de solutions de l'étoile (k = 5..10) : 6·10⁵, 3·10⁴, 3·10², 0,5, 10⁻⁴, 3·10⁻⁹ [L08-171] — H — OBS:126-133.
- Double étoile aux rangs 39, 41, 43 : ≈ 10⁻⁷⁰, 10⁻⁴⁰, 10⁻¹⁰ à 10⁻¹⁷ [L08-173] — H — OBS:163-165.
- Codimension mod 7 de l'étoile : (10 − ρ)(11 − ρ)/2, soit 55, 36, 21 et 10 [L08-234] — H — SYN:174-182.
- PSD de blocs aléatoires k × k : 0,67 ; 0,29 ; 0,08 ; 0,014 ; 0,0012 ; 10⁻⁴ ; 0 [L08-172] — E — OBS:139-141.
- Budget d'entropie par droite [L08-148] — H — RED:68-73, 252-255 :
  - Conway, c = 1 : −47,6 ; −36 en somme sur les classes ;
  - srg(243) : +32 à +35 ;
  - facteur L4 : 10⁻²¹ à 10⁻⁹⁴.
- Mur de dureté : plantés triviaux pour n ≤ 10, UNKNOWN à n = 12 [L08-147] — E — RED:44-54.
- Coûts [L08-186, L08-223, L08-213, L08-075, L08-076] — E/H :
  - line37 : 38 à 42 ms par droite testée ; line37_fast : 3,4 à 3,6 ms ;
  - route du rang 37 : 5,4·10⁵ ou 5 à 6,5·10⁴ heures-cœur ;
  - R8 pur : 5·10⁷ à 10¹² heures-cœur ;
  - étoile complète c3 : 6 500 h-cœur, ou 2 450 avec la symétrie.

### 9.3 Lemmes ouverts et étapes manquantes (ce qu'ils donneraient)

**Rang 37**
- (H₃₇) sur toutes les classes à t ≤ 7, avec certificats, donnerait r ≠ 37 [L08-187, L08-194]. Il faut :
  - l'énumération (L08-220, L08-221 : 56 λ non comptés) ;
  - les moteurs (d ≥ 5 ; (1,4) et (2,4) sans générateur ; (4,4) sans résultat ; (3,4) partiel) ;
  - une passe exacte et un second moteur ;
  - des instances plantées.
- Core37 (preuve uniforme) donnerait le maillon 1 sans énumération, en tout ou partie [L08-176] — CORE:140-164, 249-255.

**Rangs 39 à 43**
- Un théorème qui borne r, r = 37 ou r ≤ 39, rendrait finie la route par droites [L08-197] — BORNE:412-416.
- « 7-rang ≥ 25 pour tout bloc à quatre étoiles de rang réel 30 » exclurait 37 et 39 [L08-207].
- Moteur « sans u » + estimateur de Knuth aux rangs 41 et 43 : décide si une route droite par droite existe [L08-230] — ORD2:576-590.
- Classement des cas dégénérés à 6 lointains, §2.3 (iv) [L08-226] — ORD2:54-57, 621-623.
- Nécessité du filtre réel au rang 39 [L08-182].

**Sommet et R8**
- Pilote CEGAR [L08-214] — R8:349-366 :
  - k = 22 ;
  - quatre étoiles ;
  - R_k + spectral, k = 1..8 (« quatre étoiles + rang ≤ 30 + 1 label pourrait déjà être vide »).
- R8 ou cinq étoiles UNSAT, avec LRAT, exclurait Conway à tout rang [L08-210, L08-215].

**Route c et registre c = 3**
- Méthodes pour le registre :
  - P3 (7 gabarits) [L08-114] ;
  - 28 autres gabarits [L08-126] ;
  - borne sur les dimensions 6 et 7 [L08-120] ;
  - environ 80 couvertures géantes [L08-083] ;
  - certificats des 23 exclusions fragiles [L08-125].
- Un lemme sur les composantes à 18 ou 24 sommets — COST:74 ; MORTS:67-70.
- Un modèle où le couplage de l'étoile est une variable — COST:75-76.
- Une contradiction propre à Conway pour les gros blocs (k = 14, dim U = 30, P ≤ 852) [L08-089].
- La branche (II) : un comptage global (≥ 33 droites c ≤ 2) contre P ≤ 852 et 3P + 4G ≤ 2772 — SYN:498-499.

**c = 1 et lois locales**
- Lois c = 1, qui donneraient toutes l'absence de droites c = 1 :
  - (SV1), H46-c1, (a ≤ 1) ∧ (b ≥ 1), rang_F₃ ≥ 46 ;
  - ODD-PURE (cas couplé), Q7, (Q), (B′), (T1) à (T3) ;
  - cas I à IV des 2-coupes.

  Réf. [L08-025 à L08-034, L08-040, L08-042, L08-047].
- Lois à quatre étoiles (H-MATCH, N9-NG, T8/T15, N15) : elles donneraient l'absence de Conway [L08-235].
- Lemme P2 restreint et normalisation couvrante : exclusion du rang 37 [L08-145].
- Classement du design des six grilles (colonnes, puis signes par caractères sur ℤ₂⁶) : « aucune droite dans six grilles » [L08-138, L08-141].
- Méthode des résidus de C7 appliquée au Gram 420Π_T des six grilles [L08-141] — MAND:334-336.
- Une condition sur le groupe critique K(G_T), forcée globalement comme L23 — MAND:413-414.

**Bornes, symétrie, périphérie**
- PL d'ordre 10 certifié (P < 852 ?) [L08-157].
- (S3) [L08-154].
- Réalisation des cinq bords de transport ; existence d'un 4-cycle de transport [L08-002, L08-003].
- α = 21 ; branches (0,2) ; conjectures G, E, L, P (notes 176-177) [L08-008, L08-018].
- Relecture humaine ou formalisation de :
  - E3 ;
  - la dérivation du recensement (P ≤ 852) ;
  - la règle de classe δ ;
  - les formules RD ;
  - le Théorème 6.1 et ses lemmes ;
  - le code et les preuves de Codex.

### 9.4 Méthodes transposables (d'un cas à un autre)

- **C2, C3, C7 → C1** (MAND:153-168). Une identité quadratique transforme un petit objet entier en un cadre entier de petit rang, dont l'arithmétique ferme. Sans symétrie, il reste trois objets :
  - (i) le second sous-constituant (rang 30, 8T entier) ;
  - (ii) le côté lointain d'une droite (rang 7 + c) ;
  - (iii) les réseaux propres (44 et 54).

  (ii) est le seul de taille comparable à C7 ou C2. Il est entier dès que G_T a un spectre entier, par exemple pour c = 6 [L08-140, L08-141].
- **C7 → droite dans six grilles.** La méthode des résidus (Gram entier dans un petit ensemble, relations exactes) devient « applicable, pas encore appliquée » [L08-141] — MAND:334-336.
- **C3 → C1, transfert direct.** Une seconde forme congrue obtenue par des gains sur Γ est impossible [L08-144].
- **C2 → trou lointain.** La méthode de comptage de C2 (Prop. 87) s'adapterait aux vecteurs portés par F — MAND:404-407.
- **srg(243,22,1,2) comme contrôle positif.** Il vaut pour :
  - les identités (I1)-(I3) et le projecteur [L08-140] ;
  - R8, dont l'analogue est SAT en 5,5 à 18 s [L08-211] ;
  - les blocs de sommet 7P_v [L08-205] ;
  - les couches C2 [L08-123] ;
  - les moments HᵀH = 9R [L08-079] ;
  - le recensement d'ordre 10 [L08-157].

  Il ne vaut pas pour les énoncés qui dépendent de c (L4, rang 7 + c), ni pour la domination parfaite des grilles, propres à k = 14 [L08-140, L08-093, L08-191].
- **Théorème B** (RES:277-317). Le contenu 7-adique ne dépend que de U, pas de la droite de base, et un test au rang 43 vaut pour toute la fenêtre [L08-218].
- **Réduction O(D) par Witt ; découpage par direction de torsion** : valables pour tout moteur à résidu [L08-192] — THM:658-710.
- **Burnside par type cyclique et énumérateur canonique** (enum37) [L08-220, L08-221] — ENUM:91-349.
- **Estimateur de Knuth.**
  - Il donne la taille des recensements, de R8 et de l'arbre de l'étoile [L08-074, L08-213, L08-230].
  - L'ablation isole des cœurs suffisants [L08-169, L08-171, L08-078].
- **Coupes à témoin entier pour le filtre réel**, par exemple B = 9·det(L)·H [L08-193] — THM:752-758. Coupes CEGAR entières (Y, q, borne) [L08-214] — R8:321-334.
- **Certification LRAT/DRAT par cake_lpr** ; deux encodeurs ; contrôles plantés [L08-215, L08-194].
- **Plan de comptage de Codex (ZC, sans Gram ni budget).** Il s'applique uniformément à c3, c4 et c ≤ 2 [L08-084] — LEM:144-157.
- **FG, R1 et le PL des lignes de Ĵ** valent pour tout c [L08-085, L08-087].
- **Lemme du carré et histogrammes** : racine arbitraire, sans Gram ni budget [L08-090, L08-091].
- **Colonnes opposées forcées → cœur rigide → énumération exacte.** De 5602, la méthode est passée à C4C3, T23, K3U, 2K2, P3NB, K2BC et 2K2N [L08-103 à L08-116] — RAP:106-111.
- **Sélection exacte de profils (SAT + RUP)** : de K3 à P3, 2K2, P3NB et GEN — NUIT:228-240.
- **Coupes de continuation** : formulées pour tout srg(v, 2r, 1, 2), contrôlées sur srg(243) — CX/PREUVE_COUPES_CONTINUATION_2026_10_19.txt:10-21, 241-246 (hors lot).
- **Équivalence par deux positivités** (Codex) pour traiter la compatibilité globale [L08-013].
- **Recensement par double comptage (census2).**
  - Il s'étend au comptage des grilles (3P + 4G) et à l'interdiction de types (E3) [L08-067, L08-069].
  - Les flag algebras s'y greffent [L08-156].
- **Invariants de Hasse** : seul p = 7 filtre (RD) ; le côté 3 équivaut à L23 [L08-001, L08-208].
- **Calibration du p-rang** : un p-rang bas trahit une structure F_p cachée, pas une symétrie [L08-204].
- **Budget d'entropie** (covariance de Hoeffding) et **instances plantées** pour mesurer la surdétermination et la dureté [L08-147, L08-148].
- **Non transposables**, signalé par les notes :
  - les familles c3 à c = 1 (NUIT:213) ;
  - les carrés de défaut à c = 1 [L08-129] ;
  - les blocs partiels sans leurs hypothèses (BLOC:31-32) ;
  - les droites latérales [L08-218].
