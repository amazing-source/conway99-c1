# Fiche L05_Codex — travaux de Codex (et de l'application Codex « Astra »)

Agent de consolidation L05, 20/10/2026. Lecture seule ; aucune source modifiée. Fichier compagnon :
`fiches/L05_Codex.jsonl` (238 résultats, identifiants L05-001 … L05-238, sources détaillées ligne à ligne).

## 0. Résumé (10 lignes)

1. Le lot (991 contenus, 52,5 Mo) mêle trois choses : le dépôt de Codex (`c1-codex`, worktree `c1-main-codex`, branches
   `codex/*` de conway99-c1 : notes 165–260 des 07–10/10, journaux `AGENTS.md` et `RECHERCHE_ACTIVE_C1.md`, notes `.txt`
   des 12–20/10) ; l'application Codex (`Documents/Codex`) : briefs « Astra » des 25–27/09 (surtout C2) et sessions des
   04–06/10 ; enfin des copies (notes LAB, dossiers ChatGPT, notes C1).
2. **Correction d'attribution** : les lemmes L1–L25 ne sont pas de Codex. Ils sont de la session C1 (Claude, notes 00–164,
   journal `JOURNAL.md`). Codex/Astra en a audité L8, L22, L23 et g ≤ 17 (L05-214), et a corrigé la portée de la note 100 le 15/10 (L05-237).
3. Apports principaux de Codex, avec LAB : fenêtre r = rang_F7(A − 3I) ∈ {37, 39, 41, 43} (L05-017, C) ; P ≤ 852 et
   ρ ≤ 126 (L05-019, C, revérifié par LAB le 18/10) ; 3P + 4G ≤ 2772 (L05-181, C) ; a_7 ≤ 842 (L05-026) ; 174 noyaux
   obligatoires de 14 sommets (L05-059) ; théorèmes de complétion (L05-106 à L05-109) ; critère T + U = 7Π (L05-160) ; E3 (L05-177).
4. Branche « c(L) ≥ 4 pour toute droite » fermée par CP-SAT, sans certificat portable (L05-178, S) : tout Conway aurait une
   droite c(L) ≤ 3. Familles c3 fermées avec certificats RUP/entiers : K3U, 2K2, 5602, 5128, 4192, 9748 (L05-183 à L05-198).
5. **Aucune exclusion de Conway ni de C1.** Au 19/10 08h50, 435 gabarits c3 restaient ouverts (L05-201) ; la branche c ≤ 2 est chez LAB.
6. Grands conditionnels ouverts : 174 noyaux (L05-098), N9-NG ⇔ rang F ≥ 12 (L05-170), NG7 (L05-150), H-MATCH (L05-158), S0 ≤ 2288 (L05-081).
7. Retraits et réfutations : bug OR-Tools du 18/10 (L05-179, X) ; verdicts LAB « sans Gram » (L05-180, X) ; conjecture (A),
   ODD9, SUM14, KER-SYM réfutées (L05-124, L05-152, L05-153) ; Théorème A de C2 corrigé (rang impair, L05-214).
8. Côté C2, Astra/Codex a fermé 278 des 441 types d'étoiles P = 0 à g⁻ = 18 (L05-209) et le cas Wagner/cube (L05-219, L05-220) ;
   la branche C2 a ensuite été close par la route C (rapporté, hors lot).
9. Statuts : 121 P, 60 C, 25 E, 10 S, 6 H, 10 O, 4 R, 2 X. Vérification LAB documentée pour P ≤ 852, 3P + 4G ≤ 2772, E3,
   P3-closure et a_7/co-Heawood (partielle) ; pas pour la fermeture c ≥ 4 (§7).
10. Lecture : 6 contenus lus en entier, 454 parcourus (en-tête et résultat), 190 vus par le titre seulement, 341 non lus
    (copies LAB, données, sorties brutes, compilations cumulatives) ; détail au §8 ; matériaux de recombinaison au §9.

## 1. Qui est qui dans ce lot (attribution vérifiée)

- **Codex** : l'agent du dépôt `c1-codex`. Il lit `AGENTS.md` et écrit les notes `notes/<n>_CODEX_*.md` (n = 165 à 260), les notes
  `notes/*_2026_10_1x.txt`, `code/codex/`, `data/codex_*`. Source : `c1-main-codex/AGENTS.md:L2035-2073`,
  `RECHERCHE_ACTIVE_C1.md:L1-869`. Les commits git portent tous l'identité de l'utilisateur (« ren », « dilan »,
  « amazing-source ») : l'auteur se lit dans l'en-tête des notes, pas dans git.
- **Application Codex** (`Documents/Codex/<date>/<slug>`) : sessions de l'application. Les dossiers `brief-astra-*` du 25/09 sont
  les briefs adressés à « Astra » ; le journal C1 parle des « rapports d'Astra » transmis par l'utilisateur
  (`conway99-c1:origin/codex/c1-arithmetic-audit:JOURNAL.md:L303-322`). La session multi-agents du 04/10 demande
  « GPT-6.1 Sol xhigh » (`2026-10-04/j-ai-un-travail-de-m2/research_brief.txt:L1`).
- **ChatGPT** : les `dossiers_externes/` (Paley, BvLS, Hoffman, K7, CODE7, preuve C3) ; `c1-main-codex/dossiers_externes/INDEX.md:L1-7`.
- **C1** : la session Claude auteure des notes 00–164 et des lemmes L1–L25 (`JOURNAL.md:L3-30` : « Claude Code a coupé les
  boucles d'attente »).
- **Claude (série 165–178 de main)** : une autre série de notes numérotées 165–178 (`165_SRG243_…`, `171_BORDS_SERRES_HOFFMAN`,
  `172_RESEAU_Q_ALPHA22`, …), commits « Claude » des 11–12/10. **Collision de numérotation** avec les notes Codex 165–178.
- **LAB** : la session Claude Code du PC du labo. Dans les textes de Codex des 13–16/10, « Claude » désigne ce même pair
  du pont (`AGENTS.md:L1942-1943`). **LAP** : la session Claude du portable (`t20-codex/lemma/T20_BOARD.md:L7`).

## 2. Chronologie (Codex, application Codex, Astra)

| Date | Événement | Source |
|---|---|---|
| 11/09 | Session de l'application sans rapport (revue de sécurité « Gamebeast ») | `Codex/2026-09-11/j/outputs/…` |
| 25/09 | Brief Astra n° 2 : audit adverse de C1 (L8, L22, L23, g ≤ 17 tiennent) et de C2 (Théorème A faux) | L05-214 |
| 25–26/09 | Briefs Astra : témoin affine, repère de 231 vecteurs, E8/Leech, cinq triangles, ordre 11 | L05-206, L05-207, L05-215, L05-216 |
| 26/09 | C2 : g⁻ = 16 force un prisme ; P = 0 ⇒ g⁻ ∈ {18, 20} ; 38 types g18 exclus ; A33, Wagner à sept blocs | L05-208, L05-211, L05-212 |
| 27/09 00h47–07h36 | C2 : registre g18 de 263 à 278 exclus sur 441 ; C1 : appui 9 / rang R = 2 incompatibles | L05-209, L05-213 |
| 27/09 13h23 | NOUVEAUTES : six blocs fractionnaires exclus dans D6⁴ | L05-210 |
| 04/10 | C2 (EX de MODEL.md) : Wagner et cube exclus, min L* ≥ 9/7, coupes k = 1, 2, 3 ; session multi-agents | L05-219 à L05-223 |
| 05–06/10 | C1 : couverture par fonctions courtes (entière 18 / entière 26 / affine 37) ; passation du 06/10 | L05-224 à L05-227 |
| 07/10 | Dépôt c1-codex : notes 165–166 (normes 14 et 16) ; Codex arbitre la preuve C2 T20 | L05-001 à L05-003, L05-233 |
| 08/10 | Notes 167–219 : thêta niveau 7, rangs 33 et 35 exclus, census 7–10, P ≤ 852, τ, b3, deux étoiles | L05-004 à L05-056 |
| 09/10 | Notes 220–250 : routes hors rangs, 174 noyaux, complétion binaire, rubans, S0, P3/N25 ; priorité « exploration » ; calculs suspendus 05:08 UTC | L05-057 à L05-087 ; `AGENTS.md:L2037-2073` |
| 10/10 | Notes 251–260 : norme 16 (forêts lointaines, attaches exclues, survivant de bord) | L05-088 à L05-097 |
| 11–12/10 | Dossiers ChatGPT ; audit Codex des quatre srg(243) ; relèvement S3 ; échanges de Hoffman ; défauts de cocliques V5–V11 | L05-110 à L05-116, L05-228 à L05-232 |
| 13–14/10 | V12–V15 : complétion avec régularité, rigidité de rang 2, bord 43 ⇒ ≤ 8192 signes ; consigne « deux chercheurs » | L05-106 à L05-109 ; `AGENTS.md:L1929-1940` |
| 14/10 nuit | Programme sans anciennes notes : PRISM9, GRID21, P3-closure, co-Heawoods ≤ 396 | L05-125 à L05-135 |
| 14/10 après-midi | Asymétrie et construction λ = 1 : circuits, flips, Payne GF9 exclu ; complétions à trois étoiles ; (A) réfutée | L05-117 à L05-124 |
| 15/10 | G1/c55, ODD9 réfutée, <z,hM> exclue, census entier P = 0, 254 blocs forcés, C4DO plate | L05-142 à L05-157 |
| 16/10 | H-MATCH (sans conclusion), chaîne 44 → 84 → 99, T + U = 7Π, cœur 30, cadres 15 lignes ; résonance Q20, SYM6 ; 79 configurations min c = 4 | L05-158 à L05-175 |
| 17/10 | E3 (rectangles à trois arêtes impossibles) ; fusion des branches dans main | L05-177 ; `AGENTS.md:L2035` |
| 18/10 | 11h40 bug OR-Tools ; 13h15 3P + 4G ≤ 2772 ; 16h36 c(L) ≥ 4 fermée (CP-SAT) ; certificats 5128, 4192, 9748 | L05-178 à L05-192 |
| 19/10 | 5602, famille (2,3), K3U, 2K2 fermées ; registre c3 902 → 537 → 435 ouverts | L05-193 à L05-205 |
| 20/10 | Deux notes nouvelles, hors inventaire (trois colonnes égales ; budget entier d'un support signé) | L05-203, L05-204 |

## 3. Table des résultats

Colonnes : identifiant, date (mois-jour), énoncé court, statut, première source (les autres sont dans le JSONL).

| id | date | énoncé court | statut | source |
|---|---|---|---|---|
| L05-001 | 10-07 | Norme 14 : min L ≥ 14 et, si min L = 14, rang_7(A−3I) ≥ 33 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/165_CODEX_NORM14_RANK33.md:L1-29` |
| L05-002 | 10-07 | Branche norme 14 : équivalence avec un problème de projecteur de rang 16 | O | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/165_CODEX_NORM14_RANK33.md:L15-16` |
| L05-003 | 10-07 | Norme 16 : exactement cinq cœurs de support | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/166_CODEX_NORM16_CINQ_COEURS.md:L1-21` |
| L05-004 | 10-07 | Piste thêta de niveau 7 : réseaux L1 (indice 3) et M = √7 L1* | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/167_CODEX_LEVEL7_THETA_AUDIT.md:L1-24` |
| L05-005 | 10-08 | Fenêtre de rang {33,…,43} et min L1 ≤ 26 | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/168_CODEX_THETA_RANG33_MIN26.md:L1-24` |
| L05-006 | 10-08 | Norme 16 : 478 orbites d'attaches des huit sommets D | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/169_CODEX_NORM16_ATTACHES_RANG.md:L1-13` |
| L05-007 | 10-08 | a_7 ≤ 7920, a_8 ≤ 27720 ; au rang 33, a_7 ≥ 66 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/170_CODEX_NORM16_SEED4_FANO_RANG33.md:L1-24` |
| L05-008 | 10-08 | Norme 18 : au plus une arête par support et ≥ 6 graines indépendantes | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/171_CODEX_NORM18_BUDGET_GRAINES.md:L1-24` |
| L05-009 | 10-08 | Rang 33 exclu : r ∈ {35,37,39,41,43} | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/172_CODEX_RANG35_DUAL_PAW_CYCLE.md:L1-24` |
| L05-010 | 10-08 | Unicité des graines de norme 16 : 7a_7 + 8a_8 ≤ 55440, a_8 ≤ 6930 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/173_CODEX_GRAINES_UNIQUES_NORMES14_16.md:L1-24` |
| L05-011 | 10-08 | Côté +3 : réseau pair E de rang 60 et coefficients forcés | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/174_CODEX_RESEAU60_COTE_PLUS3.md:L1-22` |
| L05-012 | 10-08 | Recollement unimodulaire : comptages conjoints jusqu'à la norme 5 ; b_5 ≥ 18001368 | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/175_CODEX_RECOLLEMENT_PETITES_NORMES.md:L1-24` |
| L05-013 | 10-08 | Normes 18 et 20 : binarité, différences interdites, b_1 ≤ 88 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/176_CODEX_GEOMETRIE_NORMES18_20.md:L1-24` |
| L05-014 | 10-08 | Rang 43 : classes courtes de L1/(√7M) | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/177_CODEX_RANG43_CLASSES_COURTES.md:L1-24` |
| L05-015 | 10-08 | Classes fractionnaires de normes 22, 24, 26 : formes exactes | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/178_CODEX_CLASSES_FRACTIONNAIRES_22_26.md:L1-24` |
| L05-016 | 10-08 | Rang 35 : ≥ 16 grilles, ≥ 450 prismes, ≥ 33 paires de prismes jumeaux | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/179_CODEX_RANG35_GRILLES_ET_JUMEAUX.md:L1-21` |
| L05-017 | 10-08 | Rang 35 exclu : r ∈ {37,39,41,43} | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/180_CODEX_EXCLUSION_RANG35_PACKING_FANO.md:L1-22` |
| L05-018 | 10-08 | Recensement à sept sommets : 208 types, invariant H (graphe D) | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/181_CODEX_SEPT_SOMMETS_COLLISIONS_RANG37.md:L1-22` |
| L05-019 | 10-08 | Recensement à 9 sommets : P ≤ 852 et ρ ≤ 126 | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/182_CODEX_RECENSEMENTS_HUIT_NEUF_SOMMETS.md:L5-14` |
| L05-020 | 10-08 | Collisions de masse huit des représentants (4,4) | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/183_CODEX_COLLISIONS_MASSE_HUIT.md:L1-22` |
| L05-021 | 10-08 | Recensement paramétré (v,k,1,2) et contrôle sur graphes réels | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/184_CODEX_RECENSEMENT_PARAMETRE_TESTS_REELS.md:L1-22` |
| L05-022 | 10-08 | Famille (4,4) : première borne complète après collisions | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/185_CODEX_FAMILLE_44_AUDIT_COMPLET.md:L1-22` |
| L05-023 | 10-08 | Triangles lointains : b3 ≥ 45528 (et b3 ≥ 73920 si P = 0) | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/186_CODEX_TRIANGLES_LOINTAINS_MULTIPLICITES.md:L1-22` |
| L05-024 | 10-08 | Recensement ciblé à dix sommets : famille (5,5) | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/187_CODEX_ORDRE_DIX_RECENSEMENT_CIBLE.md:L1-22` |
| L05-025 | 10-08 | Famille (6,3) : pertes internes de masses six et sept | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/188_CODEX_COLLISIONS_63_MASSES_SIX_SEPT.md:L1-22` |
| L05-026 | 10-08 | Borne de Fano : a_7 ≤ 842 (≤ 421 configurations non orientées) | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/189_CODEX_FANO_842_ORDRE10.md:L1-16` |
| L05-027 | 10-08 | Motif prisme + maison éloignée à l'ordre 11 : τ ≤ 2048 (plus faible) | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/190_CODEX_PRISME_MAISON_ORDRE11.md:L1-22` |
| L05-028 | 10-08 | Racines de M : b_1 ≤ 78, b_2 ≥ 462 + 41b_1 + b_1²/2 ; au rang 43, b_2 ≥ 922 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/191_CODEX_RANG43_NORME4_PROFILS28.md:L1-22` |
| L05-029 | 10-08 | Cocliques de taille 22 : b_1 ≤ 44 ; au rang 43, b_2 ≥ 968 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/192_CODEX_COCLIQUES_RACINES44_NORME4_968.md:L1-21` |
| L05-030 | 10-08 | Famille F0 sans triangle positif : pertes de masses 6 et 7 | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/193_CODEX_F0_TRIANGLE_LIBRE_COLLISIONS.md:L1-22` |
| L05-031 | 10-08 | Classes de prismes : 17τ ≤ 17P + 105ρ, τ ≤ 1534, b3 ≥ 45766 | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/194_CODEX_CLASSES_GRILLES_TAU1534.md:L1-22` |
| L05-032 | 10-08 | Pertes séparées par type de paire de prismes (masse six binaire) | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/195_CODEX_COLLISIONS_PAIRES_GRILLES.md:L1-22` |
| L05-033 | 10-08 | Propagation des grilles par moments : τ ≤ 1403, b3 ≥ 45898 ; au rang 37, b4 ≤ 2172309411/136 | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/196_CODEX_MOMENTS_VOISINAGES_TAU1403.md:L1-25` |
| L05-034 | 10-08 | Collisions conditionnées par la taille du faisceau de grilles | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/197_CODEX_COLLISIONS_FAISCEAUX_GRILLES.md:L1-20` |
| L05-035 | 10-08 | Canal (9,0) : C_90 = 5376 + 12t ≤ 5472 ; C_6 ≤ 39016712 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/198_CODEX_MOMENTS_DEGRES_ET_CANAL90.md:L1-20` |
| L05-036 | 10-08 | Couplage Fano–prismes–grilles : 14a_7 + 25P + 32ρ ≤ 28182 | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/199_CODEX_COUPLAGE_FANO_GRILLES.md:L1-20` |
| L05-037 | 10-08 | Représentants sans prisme et égalités de longueur | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/200_CODEX_SANS_PRISME_ET_REPRESENTANTS_COURTS.md:L1-20` |
| L05-038 | 10-08 | Droite dans six grilles : les équations de fentes ne l'excluent pas | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/201_CODEX_FENTES_ET_DROITE_DANS_SIX_GRILLES.md:L1-20` |
| L05-039 | 10-08 | Rang mod 7 : un motif de grilles denses (hubs répétés) exclu | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/202_CODEX_RANG7_GRILLES_ET_HUBS_REPETES.md:L1-20` |
| L05-040 | 10-08 | Motif (2,2,1) exclu pour r ≥ 37 ; 3n₃ ≤ 2n₁ + n₂, n₃ ≤ 39 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/203_CODEX_EXCLUSION_GENERALE_221_ET_COUPURE_GLOBALE.md:L1-20` |
| L05-041 | 10-08 | Coupure des sommets denses : τ ≤ 1354, b3 ≥ 45964, C6 ≤ 38084490 (r ≥ 37) | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/204_CODEX_COUPURE_DENSE_BORNES_GLOBALES.md:L1-20` |
| L05-042 | 10-08 | Deux apices denses : r ≥ 39 ⇒ 6n₃ ≤ n₁ + 2n₂ (n₃ ≤ 24) ; au rang 37, 22 modèles sur 29 survivent | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/205_CODEX_DEUX_APICES_DENSES_ET_DISCRIMINANT.md:L1-20` |
| L05-043 | 10-08 | Relations locales de grilles ; au rang 43 : e(Ξ_v) ≤ 15, τ ≤ 1326, b3 ≥ 46000 | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/206_CODEX_RELATIONS_LOCALES_ET_RANG43.md:L1-17` |
| L05-044 | 10-08 | Audit des étoiles génériques : le témoin d'Astra réfute l'obstruction à deux apex | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/207_CODEX_AUDIT_ETOILES_GENERIQUES.md:L1-20` |
| L05-045 | 10-08 | Espace hyperbolique universel des composantes : rangs ≤ 14, ne peut exclure 37, 39, 41 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/208_CODEX_ESPACE_LOCAL_DES_COMPOSANTES.md:L1-16` |
| L05-046 | 10-08 | Deux étoiles couplées sur une arête : 38 types à P = S = 0 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/209_CODEX_COUPLAGE_DEUX_ETOILES.md:L1-13` |
| L05-047 | 10-08 | Résidu (6,6) : réduction conditionnelle et correction du filtre de triplets | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/210_CODEX_AUDIT_RESIDU_66.md:L1-20` |
| L05-048 | 10-08 | Modèle entier et modulo 7 de deux étoiles génériques (rang 37, P = 0) | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/211_CODEX_MODELE_DEUX_ETOILES.md:L1-20` |
| L05-049 | 10-08 | Deux certificats exacts pour des branches de deux étoiles (boule témoin déjà exclue) | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/212_CODEX_CERTIFICATS_DEUX_ETOILES.md:L1-14` |
| L05-050 | 10-08 | Preuve par potentiels sans équations de degré (branche 0) | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/213_CODEX_POTENTIELS_DEUX_ETOILES.md:L1-13` |
| L05-051 | 10-08 | Ablation exacte des compatibilités | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/214_CODEX_ABLATION_EXACTE_COMPATIBILITES.md:L1-20` |
| L05-052 | 10-08 | Projecteur réel de rang 8 et mineurs d'ordre 3 : les 473 branches de la boule (2,4,1) rejetées sans LP | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/215_CODEX_PROJECTEUR_REEL_ET_MINEURS_TROIS.md:L1-20` |
| L05-053 | 10-08 | Audit du mécanisme « un choix puis propagation » (LAB note 17.59) | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/216_CODEX_AUDIT_CHOIX_UNIQUE_ET_PROPAGATION.md:L1-14` |
| L05-054 | 10-08 | Discriminant du projecteur lointain : test arithmétique exact sur huit ombres | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/217_CODEX_DISCRIMINANT_DU_PROJECTEUR_LOINTAIN.md:L1-20` |
| L05-055 | 10-08 | Motif forcé par les coordonnées unitaires d'une étoile | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/218_CODEX_MOTIF_FORCE_COORDONNEES_UNITAIRES.md:L1-12` |
| L05-056 | 10-08 | Une étoile de Green abstraite prolonge toujours trois ombres fixées | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/219_CODEX_COMPLETION_ABSTRAITE_GRAM_ETOILE.md:L1-16` |
| L05-057 | 10-09 | Routes hors rangs pour C1 : relecture des routes A/B/C de C2 | H | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/220_CODEX_ROUTES_HORS_RANGS.md:L1-20` |
| L05-058 | 10-09 | Noyau obligatoire de 14 sommets (motif de Makhnev) : 373 types, 63 exclus | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/221_CODEX_NOYAU_PRISME_DEFECTUEUX.md:L1-20` |
| L05-059 | 10-09 | Incidences extérieures : 136 noyaux de plus exclus, 174 restent | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/222_CODEX_PROLONGEMENT_PRISME_MASQUES.md:L1-20` |
| L05-060 | 10-09 | Limite des premiers prolongements des 174 noyaux | H | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/223_CODEX_LIMITE_DES_PREMIERS_PROLONGEMENTS.md:L1-20` |
| L05-061 | 10-09 | Audit LAP : rang 37, voisinage de droite sans triangle ni 4-cycle ⇒ G(T) connexe | S | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/224_CODEX_AUDIT_LAP_RANG37_MAILLE5.md:L1-20` |
| L05-062 | 10-09 | Noyaux, composantes et grilles : réduction conditionnelle 174 → 115/52/11/2 | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/225_CODEX_NOYAUX_COMPOSANTES_ET_GRILLES.md:L1-15` |
| L05-063 | 10-09 | Lemme de masse neuf ; couverture des canaux sous P = 0 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/226_CODEX_MASSES789_SANS_PRISME.md:L1-20` |
| L05-064 | 10-09 | Pas de doubles moulins ; C8 sans terme constant 8 981 280 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/227_CODEX_C8_SANS_DOUBLES_MOULINS.md:L1-20` |
| L05-065 | 10-09 | Moulin–cubique ⇔ vecteur de noyau de profil (2,1^16) ; 359 types sous P = 0 | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/228_CODEX_MOULIN_CUBIQUE_NOYAU17.md:L1-14` |
| L05-066 | 10-09 | Partenaires cubiques et antivoisinages : rayon spectral ≤ 3, tailles multiples de 8 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/229_CODEX_PARTENAIRES_ET_ANTIVOISINAGES.md:L1-18` |
| L05-067 | 10-09 | Complétion binaire au rang 37 : arêtes lointaines = 240 + 7q, seuil 240 ⇔ SRG de rang 37 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/230_CODEX_COMPLETION_BINAIRE_SEUIL240.md:L1-22` |
| L05-068 | 10-09 | Signe résiduel fixé par la complétion de Witt ; toutes les traces découlent de NNᵀ = K | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/231_CODEX_SIGNE_RESIDUEL_ET_TRACES.md:L1-18` |
| L05-069 | 10-09 | Rigidité binaire : une complétion de rang 37 est unique tous rangs confondus | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/232_CODEX_RIGIDITE_BINAIRE_LAPLACIEN.md:L1-18` |
| L05-070 | 10-09 | Deux complétions des mêmes ombres diffèrent par un rang ≥ 5 sur F7 ; (39,39) impossible | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/233_CODEX_DIFFERENCE_RANG4_IMPOSSIBLE.md:L1-18` |
| L05-071 | 10-09 | Connexité des murs opposés d'un quadrilatère | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/234_CODEX_CONNEXITE_MURS_OPPOSES.md:L1-15` |
| L05-072 | 10-09 | Dossier Convergences : témoins de bord appliqués au motif de Makhnev et aux supports 4-réguliers | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/235_CODEX_EXPLOITATION_CONVERGENCES.md:L1-18` |
| L05-073 | 10-09 | Convergences : 95 étoiles du sommet exceptionnel et arêtes partagées du bord | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/236_CODEX_CONVERGENCES_ARETES_PARTAGEES.md:L1-15` |
| L05-074 | 10-09 | Rubans de transport réparés seulement entre centres : m ≤ 8 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/237_CODEX_RUBANS_REPARES_PAR_CENTRES.md:L1-24` |
| L05-075 | 10-09 | Fenêtres de transport : ≥ 2 arêtes latérales par fenêtre de huit centres | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/238_CODEX_FENETRES_TRANSPORT_ET_DENSITE.md:L1-18` |
| L05-076 | 10-09 | Ruban six : étoiles de cordes centrées sur un sommet latéral impossibles | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/239_CODEX_RUBAN_SIX_CORDES_EN_ETOILE.md:L1-18` |
| L05-077 | 10-09 | Ruban six : deux cordes disjointes ou exactement le triangle de centres alternés | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/240_CODEX_CORDES_DISJOINTES_OU_TRIANGLE_DE_CENTRES.md:L1-24` |
| L05-078 | 10-09 | Entrées exactes pour la piste thêta cubique par classes | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/241_CODEX_ENTREES_CUBIQUES_THETA_IMPAIRE.md:L1-18` |
| L05-079 | 10-09 | Rang 43 : une racine de M force 10a8 + 2a9 + 5a10 + 2a11 + a12 ≥ 328 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/242_CODEX_MOMENTS_QUADRATIQUES_ET_RACINES.md:L1-18` |
| L05-080 | 10-09 | Norme 26 dans S0 : au plus 48 (ou 45) voisins proches dans une classe | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/243_CODEX_CONTACTS_NORME26_ET_TRIANGLES_IMPAIRS.md:L1-18` |
| L05-081 | 10-09 | S0 : au moins 2289 + 15g configurations P7/Q29 ; une borne ≤ 2288 fermerait S0 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/244_CODEX_FANTOMES_ET_CIBLE_INDEPENDANTE_UNIFORME.md:L1-18` |
| L05-082 | 10-09 | P3/N25 : N est une forêt de 12 arêtes (32 formes), δ ≥ 3 | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/245_CODEX_P3_N25_FORETS_ET_TRIANGLES_SORTANTS.md:L1-18` |
| L05-083 | 10-09 | P3/N25 : preuve directe de 3 ≤ δ ≤ 9 ; 764 supports exclus, 4581 restent | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/246_CODEX_APPARIEMENTS_LOCAUX_P3_N25.md:L1-18` |
| L05-084 | 10-09 | Formule LAB du réseau lointain de rang 8 : τ ≥ 12970803 au rang 37 | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/247_CODEX_HERMITE_ET_RESEAUX_LOINTAINS.md:L1-18` |
| L05-085 | 10-09 | Capacité triangulaire d'un bloc extérieur (P3/N25) | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/248_CODEX_CAPACITE_TRIANGULAIRE_DES_BLOCS.md:L1-18` |
| L05-086 | 10-09 | Trois prismes jumeaux hors grille ⇒ apices indépendants ; C14 + 2τ ≤ 2P | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/249_CODEX_TROIS_PRISMES_HORS_GRILLE.md:L1-18` |
| L05-087 | 10-09 | Parabole entière (lemme A de LAP) transformée en filtre d'extensions | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/250_CODEX_PARABOLE_ET_AJOUT_D_UN_SOMMET.md:L1-18` |
| L05-088 | 10-10 | Norme 16 : D a au plus une arête, Z forêt ; 15 formes et 75 supports sur 27 points | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/251_CODEX_NORM16_FORET_LOINTAINE.md:L1-18` |
| L05-089 | 10-10 | Premier cadre explicite de norme 16 (37 sommets) pour le moteur LAB | E | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/252_CODEX_PREMIER_CADRE_NORM16.md:L1-18` |
| L05-090 | 10-10 | Norme 16 : Z contient un sommet isolé ; 14 formes, 70 supports | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/253_CODEX_NORM16_SOMMET_LOINTAIN_ISOLE.md:L1-18` |
| L05-091 | 10-10 | Cadre cœur+D+Z de 35 sommets : rang ≤ 33 ; PSD réduite à un Schur 8×8 | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/254_CODEX_CADRE35_ET_SCHUR_NORM16.md:L1-18` |
| L05-092 | 10-10 | Norme 16 : la paire omise rigidifie l'unique arête double | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/255_CODEX_NORM16_PAIRE_OMISE.md:L1-18` |
| L05-093 | 10-10 | Norme 16 : dix attaches entières exclues par les ombres paires | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/256_CODEX_NORM16_OMBRES_PAIRES.md:L1-18` |
| L05-094 | 10-10 | Norme 16 : connexité du multigraphe C ; huit attaches de plus exclues (18 au total) | P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/257_CODEX_NORM16_CONNEXITE_DES_OMBRES.md:L1-16` |
| L05-095 | 10-10 | Coupures de poids deux : première obstruction exacte au bord ; LAB exclut deux supports au rang 37 | C | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/258_CODEX_COUPURES_ET_OBSTRUCTION_DE_BORD.md:L1-18` |
| L05-096 | 10-10 | Deux chemins de transport dans les quatre attaches à coupure de poids deux | P | `conway99-c1:origin/codex/norm16-far-forest:notes/259_CODEX_DEUX_CHEMINS_DE_TRANSPORT_NORM16.md:L1-11` |
| L05-097 | 10-10 | P4 dans Z : double omis ; une entrée survit au bord | O | `conway99-c1:origin/codex/norm16-far-forest:notes/260_CODEX_P4_DOUBLE_OMIS_ET_BORD_SURVIVANT.md:L1-18` |
| L05-098 | 10-09 | Implication finale de la recherche A : C1 exclu si aucun des 174 noyaux ne se prolonge | O | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/RECHERCHE_ACTIVE_C1.md:L637-649` |
| L05-099 | 10-10 | Norme 14 fermée au rang 37 (résultat LAB rapporté) | S | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/RECHERCHE_ACTIVE_C1.md:L158-161` |
| L05-100 | 10-10 | Norme 18 à signes non indépendants exclue (lemme LAB rapporté) | P | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/RECHERCHE_ACTIVE_C1.md:L88-96` |
| L05-101 | 10-12 | Cocliques de 21 : pas de sommet extérieur à 6 ou 7 voisins ; extension 21 → 22 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:L7-37` |
| L05-102 | 10-12 | Loi de charge des composantes du support du défaut : w < 0 ou w > 18δ | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:L279-290` |
| L05-103 | 10-12 | Profil (1,3) : branche « triangle de défauts négatifs » exclue ; famille (0,2) réduite à onze répartitions | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:L367-386` |
| L05-104 | 10-12 | Obstruction arithmétique pour tout bord induit : K_B = 12I + 2J − A − A² = DDᵗ | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:L1007-1016` |
| L05-105 | 10-12 | Théorème de fermeture d'une factorisation binaire (V6) et suffisance de l'intégralité | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:L1318-1411` |
| L05-106 | 10-13 | V13 : complétion exacte sur un bord binaire quelconque avec régularité | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:L2906-3153` |
| L05-107 | 10-13 | V14 : une différence de rang 2 entre deux matrices SRG(99,14,1,2) est une transposition de deux sommets | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:L3154-3327` |
| L05-108 | 10-14 | V15 : bord de 43 sommets positif ⇒ au plus 8192 signes et au plus deux complétions étiquetées | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:L3367-3542` |
| L05-109 | 10-14 | Dichotomie co-Heawood : plus de deux choix de signes forcent un vecteur propre −4 de norme 14 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:L3543-3599` |
| L05-110 | 10-12 | Deux cocliques de Hoffman se coupant en 15 ⇔ co-Heawood induit ; réduction à 21 bits et H² = 147H | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COHEAWOOD_DEUX_COCLIQUES.md:L1-40` |
| L05-111 | 10-12 | Couvertures doubles : lemme des onze couvertures distinctes et lemme de multiplicité | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_COUVERTURES_HOFFMAN_2026_10_12.md:L9-83` |
| L05-112 | 10-12 | Échanges de Hoffman : les 36 designs voisins d'un design cyclique 2-(22,4,2) sont exclus comme bords de C1 | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_HOFFMAN_ASYMETRIE_PAR_ECHANGES_2026_10_12.md:L7-36` |
| L05-113 | 10-12 | Famille à bord variable (design 37c3bb63972f, quatre points libres) exclue | S | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_COUVERTURES_HOFFMAN_2026_10_12.md:L126-163` |
| L05-114 | 10-12 | Audit des quatre srg(243,22,1,2) : objets effectifs, groupes complets calculés | C | `conway99-c1:origin/codex/asymmetry-audit-20261012:notes/AUDIT_CODEX_ASYMETRIE_2026_10_12.md:L1-40` |
| L05-115 | 10-12 | Relèvement S3 de BH : formulation exacte comme système linéaire + quadratique sur F3 | P | `conway99-c1:origin/codex/asymmetry-audit-20261012:notes/NOTE_RELEVEMENT_S3_QUADRATIQUE.md:L1-27` |
| L05-116 | 10-11 | Route du réseau Q pour α = 22 : pas d'obstruction au niveau des discriminants (note Claude) | H | `conway99-c1:origin/codex/asymmetry-audit-20261012:notes/172_RESEAU_Q_ALPHA22.md:L1-20` |
| L05-117 | 10-14 | Asymétrie : Aut(K_x, x) = permutations préservant les circuits de transport | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_mechanisms_20261014/bridge_circuits.txt:L1` |
| L05-118 | 10-14 | Flips majoritaires et filtre d'orbites de flips | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_mechanisms_20261014/bridge_majority_flips.txt:L1` |
| L05-119 | 10-14 | Mots de C = im_F2(A) : poids pair w ≥ 2 + (k−2)/μ ; Conway : distance ≥ 8 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/prescribed_kernel_728/bridge_verdict.txt:L1` |
| L05-120 | 10-14 | Construction λ = 1 asymétrique : Payne GF9 exclu exactement ; hémisystème 378 sans nouveauté | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_lambda_one_construction_20261014/bridge_payne9_obstruction.txt:L1` |
| L05-121 | 10-14 | Lemme de l'hôte : un m-ovoïde de GQ(s,t) détermine l'hôte si m(t+1) > max(s−1, t+1) | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_mechanisms_20261014/bridge_host_lemma.txt:L1` |
| L05-122 | 10-14 | Trois étoiles : borne ambiante T_SS ≤ 7Π_SS et second Gram U = 7Π − T | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/bridge_ambient_upper_bound.txt:L1` |
| L05-123 | 10-14 | Lot LAB 713 : les 572 frontières de rang 30 sont non complétables | E | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/lab713_batch/bridge_batch_verdict.txt:L1` |
| L05-124 | 10-14 | Conjecture (A) « Q connexe + T/U PSD ⇒ rang T = 31 sur trois étoiles » : RÉFUTÉE | R | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/AGENTS.md:L1908-1913` |
| L05-125 | 10-14 | PRISM9 : un triangle a au plus neuf partenaires-prismes ; prismes ≤ 1151 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L36-112` |
| L05-126 | 10-14 | GRID21 : aucun sommet n'a ses 21 paires de triangles en grilles 3×3 | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L113-282` |
| L05-127 | 10-14 | PRISM-SPECTRAL : ρ(R) < 10 sur le graphe des prismes ; prismes ≤ 1150 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L283-398` |
| L05-128 | 10-14 | P3-CLOSURE : la fermeture d'un prisme n'induit jamais exactement un P3 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L399-503` |
| L05-129 | 10-14 | Vecteurs entiers −4 minimaux : norme ≥ 14, norme 14 ⇔ co-Heawood ; ≤ 28 racines orthogonales | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L579-676` |
| L05-130 | 10-14 | Une arête est dans au plus deux co-Heawoods deux à deux orthogonaux | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L677-837` |
| L05-131 | 10-14 | Supports orthogonaux de norme 14 : disjoints ou d'intersection 4 ; famille orthogonale ≤ 12 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L838-916` |
| L05-132 | 10-14 | Vecteurs propres entiers de norme ≤ 24 : coordonnées 0, ±1 ; angles des co-Heawoods | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L917-1026` |
| L05-133 | 10-14 | Au plus 396 co-Heawoods induits (792 vecteurs signés de norme 14) | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L1027-1085` |
| L05-134 | 10-14 | Petites couches entières de valeur propre +3 (masse l1 ≤ 16) | E | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L1086-1340` |
| L05-135 | 10-14 | Multiplicités certifiées de collisions de norme 8 ; identités d'anti-voisinages | E | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L1341-1472` |
| L05-136 | 10-14 | Objet 49 : domaines des 50 colonnes ; bloc U50 de degrés 6, 7, 8 (au plus trois 8) | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L1774-1832` |
| L05-137 | 10-14 | Témoin fractionnaire exact à trois étoiles (rang 31) : comptes + plafonds + PSD ne suffisent pas | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L1833-1867` |
| L05-138 | 10-14 | Deux étoiles mates : T_X toujours PSD (somme de carrés), rang 23 − c | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L2084-2122` |
| L05-139 | 10-14 | Relation de noyau supplémentaire non négative : poids ≥ 16 | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L2460-2553` |
| L05-140 | 10-14 | Conjectures (B) « toute droite… spéciale » et (C) : ouvertes ; (A) réfutée | O | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L2151-2182` |
| L05-141 | 10-14 | Couplage : compressions de U définies positives ; 100 coupes linéaires strictes | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L2684-2762` |
| L05-142 | 10-15 | Caractères de G1 : rang T ≤ 30 force une nullité non triviale ≥ 9 − min(c_l, c_m) | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L2763-2822` |
| L05-143 | 10-15 | c55 non grille sous G1 : catalogue exact de 126 cas, nullités (10,1,1,k), k ≥ 2 | E | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L2823-2914` |
| L05-144 | 10-15 | Famille locale G1 c55 non grille exclue de tout prolongement Conway (via rang_F7 ≤ 28) | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L3226-3302` |
| L05-145 | 10-15 | Prolonger c55 non grille force un vecteur propre −4 de norme 28 et ≥ 29 profils brisant h | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L3143-3225` |
| L05-146 | 10-15 | Budget des relations mixtes : au moins 336 drapeaux avec ≥ 4 relations mixtes | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L3303-3382` |
| L05-147 | 10-15 | Budget de comptage local sans symétrie : 5Σ‖E‖² + 928P + 48Z ≤ 12374208 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L2915-3069` |
| L05-148 | 10-15 | Lemme de compression impaire d'une droite : T ∈ [2,10], U ∈ [4,12] | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L3070-3142` |
| L05-149 | 10-15 | Le census entier d'ordre 9 admet un point entier P = 0 | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L5090-5244` |
| L05-150 | 10-15 | P ≤ 852 ⇒ au moins 18 droites t ≤ 7 et au moins 254 blocs non grille | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L5090-5244` |
| L05-151 | 10-15 | Clôture des relations de noyau retenues (réseaux deux étoiles) | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L5245-5410` |
| L05-152 | 10-15 | ODD9 : coupe binaire stricte e(O ∪ S) ≤ 48 ; ODD9 universelle RÉFUTÉE | R | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L4718-4840` |
| L05-153 | 10-15 | KER-SYM et SUM14 universelles réfutées (LAB) ; versions ν ≥ 14 ouvertes | R | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L4841-4898` |
| L05-154 | 10-15 | Famille locale <z, hM> exclue de tout prolongement Conway | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L4308-4440` |
| L05-155 | 10-15 | Filtre mod 5 (Z[ζ5] → F5) : plafond local 9 pour 7 des 14 quadruplets | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L4475-4610` |
| L05-156 | 10-15 | C4DO pour les relations plates de support ≤ 12 ; 832 cœurs interdits | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L5411-5537` |
| L05-157 | 10-15 | Relations plates de support ≤ 14 : q nul sur O | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L5538-5622` |
| L05-158 | 10-16 | H-MATCH : attaque sans conclusion ; obstructions par graphe (n_45, b_29) et rigidité des remariages purs | O | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L5623-5912` |
| L05-159 | 10-16 | Prolongement d'un bloc à quatre étoiles au 45e label (4,6) : échecs certifiés | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L5913-6037` |
| L05-160 | 10-16 | Critère global nécessaire et suffisant sur les 84 étiquettes : T + U = 7Π | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L6038-6128` |
| L05-161 | 10-16 | Cœur 30 exclu par la projection globale aux 84 étiquettes (CP-SAT) | S | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L6277-6353` |
| L05-162 | 10-16 | Inégalité signée à 15 étiquettes : e(P7) + e(N8) − e(P7,N8) ≤ 14 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L6129-6276` |
| L05-163 | 10-16 | Intégration de DISC (LAB) : classes de discriminant des espaces globaux de rang 30/40 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L6129-6229` |
| L05-164 | 10-16 | Au moins quatre des huit lignes d'attache brisent h ; coupes privées et de support extérieur | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L6354-6553` |
| L05-165 | 10-16 | Cadres constructifs sur les 84 étiquettes : 8, 12, 13, 14 puis 15 lignes complètes | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L6472-6690` |
| L05-166 | 10-16 | Couverture globale à 19 types pointés ; modèle exact sans germe | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L6691-6769` |
| L05-167 | 10-16 | Deux conditions PSD suffisent globalement : spectre de T dans {0, 7} | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L6770-6824` |
| L05-168 | 10-14 | Partenaires-prismes d'un triangle : deux à deux disjoints ; propagation dans les tuiles locales | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md:L504-578` |
| L05-169 | 10-16 | Synthèse famille asymétrie srg(v,k,1,2) : le facteur k − 14 et le critère de complétion asymétrique | H | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/SYNTHESE_FAMILLE_ASYMETRIE_2026_10_16.txt:L1-16` |
| L05-170 | 10-16 | Réduction de résonance Q20 : N9-NG ⇔ rang(F) ≥ 12 ; conflit conditionnel avec rang(F) ≤ 11 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/REDUCTION_RESONANCE_20_2026_10_16.txt:L1-16` |
| L05-171 | 10-16 | SYM6 ⇔ rang(Z) ≥ 3 ; ODDCONST ⇔ rang(W) = 9 ; Conway + c_min ≤ 4 + D9 ⇒ rang Z ≤ c_min − 2 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/REDUCTION_SYM6_10_2026_10_16.txt:L1-16` |
| L05-172 | 10-16 | Secteur symétrique : laplacienne à attaches r = 8 − 2e(O), nulle exactement sur une grille | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/SECTEUR_SYMETRIQUE_BORD_2026_10_16.txt:L1-16` |
| L05-173 | 10-16 | Énergie paire : E ≥ G/5 + (2/5)(I − M) ≥ G/5, rang E = 12 − c | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/BORNE_ENERGIE_PAIRE_2026_10_16.txt:L1-16` |
| L05-174 | 10-16 | Couplage aux vingt étiquettes fixes : rang(T44) = 32 − c(l) − δ + rang(Z), δ = 9 − rang(D) | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/COUPLAGE_VINGT_FIXES_2026_10_16.txt:L1-16` |
| L05-175 | 10-16 | Branche min c = 4 : 79 configurations de composantes autour d'une racine (quotient de rang ≤ 4) | S | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/QUOTIENT_COMPOSANTES_RACINE_2026_10_16.txt:L1-20` |
| L05-176 | 10-16 | Identité globale T² = 7T sur les 84 étiquettes, rang 30 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/MOMENTS_SIGNATURES_C1_2026_10_16.txt:L8-29` |
| L05-177 | 10-17 | E3 : un rectangle racine ne peut avoir exactement trois arêtes internes | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/MOMENTS_SIGNATURES_C1_2026_10_16.txt:L459-488` |
| L05-178 | 10-18 | Branche minimum GLOBAL c(L) ≥ 4 fermée par CP-SAT (79/79) ⇒ tout Conway a une droite c(L) ≤ 3 | S | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/AGENTS.md:L600-615` |
| L05-179 | 10-18 | Bug OR-Tools 9.15 (domain[-1] = 0) : verdicts retirés le 18/10 à 11h40 | X | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt:L1-25` |
| L05-180 | 10-18 | Rétractation LAB1076 : verdicts LAB « sans Gram » des messages 1067/1069/1071 nuls | X | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/RETRACTION_LAB_SANS_GRAM_2026_10_18.txt:L1-8` |
| L05-181 | 10-18 | Certificat entier 3P + 4G ≤ 2772 ; racine minimisant 9s + 8g de score ≤ 504 | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/RACINE_PONDEREE_2026_10_18.txt:L1-25` |
| L05-182 | 10-18 | Racine de budget de prismes : il existe x avec s(x) ≤ 51 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/MINIMUM_PRISMES_RACINE_2026_10_18.txt:L1-20` |
| L05-183 | 10-18 | Gabarit c3 5128 exclu sans couverture de Gram : 4e_15 + 21e_35 + 8e_45 ≥ 68 contre ≤ 66 | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/CERTIFICAT_COMPTES_5128_2026_10_18.txt:L1-8` |
| L05-184 | 10-18 | Gabarit c3 4192 exclu sans Gram ni budget (certificat entier) et sur ses 79 Gram | C | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/CERTIFICAT_COMPTES_4192_2026_10_18.txt:L1-8` |
| L05-185 | 10-18 | Gabarit gz9748 exclu sans Gram ni budget : 9S01 + 9S23 + 2S45 ≥ 484 contre ≤ 480 | C | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/AGENTS.md:L454-458` |
| L05-186 | 10-18 | Carré de défaut ⇒ parité sur 12 sommets ; c12_364 bloqué à la main | P | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/notes/CARRE_DE_DEFAUT_ET_PARITE_2026_10_18.txt:L1-12` |
| L05-187 | 10-18 | Gram des cellules de grilles ; droite dans six grilles ⇒ spectre du bloc 60 (REDÉRIVATION) | P | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/notes/GRAM_DES_GRILLES_ET_BLOC60_2026_10_18.txt:L1-12` |
| L05-188 | 10-18 | Moments sans Gram : Σ binom(z_w,2) + e(Q) = 8 et sommes mixtes pour tout srg(v,k,1,2) | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/MOMENTS_VOISINS_SANS_GRAM_2026_10_18.txt:L1-8` |
| L05-189 | 10-18 | Gabarit 8650 : reste OUVERT | O | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/COMPTES_ET_REALISATION_8650_2026_10_18.txt:L1-8` |
| L05-190 | 10-18 | Gabarit gz3 : cinq Gram prioritaires exclues par CP-SAT, gabarit ouvert | S | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/COINS_LETTRES_EQUATIONS_PROPRES_2026_10_18.txt:L1-8` |
| L05-191 | 10-18 | La branche min c(L) ≥ 4 contient nécessairement une grille ; modèle complet autour d'une grille | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/GRILLE_NEUF_FIBRES_2026_10_18.txt:L1-9` |
| L05-192 | 10-18 | Résultats LAB rapportés : gabarits c3 durs fermés (couvertures Gram complètes) | S | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOYAUX_GRAM_C3_2026_10_18.txt:L1-9` |
| L05-193 | 10-19 | Famille K3 universelle fermée : 2 742 342 bords couverts, 322 RUP vérifiés | C | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/AGENTS.md:L144-156` |
| L05-194 | 10-19 | Lemmes des facteurs simples (« quatre couleurs ») : orbites 20 et 23 exclues à la main, lemme d'inclusion | P | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/notes/FACTEURS_QUATRE_COULEURS_2026_10_19.txt:L1-12` |
| L05-195 | 10-19 | Famille 2K2 fermée : 7/7 raccordements résiduels exclus avec certificats RUP | C | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/notes/FERMETURE_2K2_2026_10_19.txt:L1-12` |
| L05-196 | 10-19 | Justification des coupes de continuation (quotas SRG, filtres d'arêtes, deux-lignes) | P | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/notes/PREUVE_COUPES_CONTINUATION_2026_10_19.txt:L1-12` |
| L05-197 | 10-19 | Famille (2,3) partagée fermée : 5312/5312 exclusions | E | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/AGENTS.md:L323-345` |
| L05-198 | 10-19 | Gabarit gz5602 fermé par calcul entier fini, toutes Gram, sans symétrie ; C4 ⊔ C3 ⇒ K4 ⊔ C3 sous E3 | C | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/AGENTS.md:L347-385` |
| L05-199 | 10-19 | 2K2N : premier cas interdit avec toute grille B/C ; noyau signé de 20 sommets | C | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/AGENTS.md:L1-19` |
| L05-200 | 10-19 | K2BC : quatre noyaux signés minimaux de 20 sommets | P | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/AGENTS.md:L20-37` |
| L05-201 | 10-19 | Registre des gabarits c3 : 10052 → … → 1163 → 902 → 537 → 435 ouverts (19/10 08h50) | O | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/AGENTS.md:L15-17` |
| L05-202 | 10-19 | Deux colonnes égales disjointes (H_P = H_Q) et leur bloc complémentaire | P | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/notes/PAIRES_EGALES_ET_BLOC_DOUZE_2026_10_19.txt:L1-12` |
| L05-203 | 10-20 | Trois copies d'une colonne non nulle de H sont impossibles (20/10) | P | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/notes/TROIS_COLONNES_EGALES_INTERDITES_2026_10_20.txt:L1-8` |
| L05-204 | 10-20 | Budget entier sur un support propre signé : au plus cinq arêtes par signe (20/10) | P | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/notes/BUDGET_ENTIER_SUPPORT_SIGNE_2026_10_20.txt:L1-12` |
| L05-205 | 10-19 | Rang 7 des Gram : trois gabarits sur quatre exclus sur leurs Gram initiales | E | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/AGENTS.md:L407-419` |
| L05-206 | 09-25 | Cinq triangles deux à deux disjoints reliés deux à deux par exactement deux arêtes : impossible | P | `C:/home/researcher/Documents/Codex/2026-09-25/brief-astra-n-1-attaque-ind/outputs/POURSUITE_RECHERCHE.md:L1-12` |
| L05-207 | 09-25 | Pas d'automorphisme d'ordre 11 (preuve par un réseau de rang 4) | P | `C:/home/researcher/Documents/Codex/2026-09-25/brief-astra-n-1-attaque-ind/outputs/mission_audacieuse/preuve_ordre11.md:L1-12` |
| L05-208 | 09-26 | C2 (Astra) : une involution avec g⁻ = 16 force un prisme ; P = 0 ⇒ g⁻ ∈ {18, 20} | C | `C:/home/researcher/Documents/Codex/2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g16/ETAT_REPRISE.md:L1-12` |
| L05-209 | 09-27 | C2 (Astra) : registre des 441 types d'étoiles P = 0 à g⁻ = 18 : 38 → 263 → … → 278 exclus | C | `C:/home/researcher/Documents/Codex/2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g18/ETAT_REPRISE.md:L1-8` |
| L05-210 | 09-27 | C2 (Astra) : dans D6⁴, les régimes à six blocs fractionnaires sont exclus ; au moins trois blocs entiers | P | `C:/home/researcher/Documents/Codex/CONWAY_NOUVEAUTES_27_09_2026/LIRE_D_ABORD.md:L1-14` |
| L05-211 | 09-26 | C2 (Astra) : normes carrées 9 et 10 — aucun bloc ne porte six représentants ; Wagner à sept blocs | C | `C:/home/researcher/Documents/Codex/2026-09-25/brief-astra-n-1-attaque-ind/outputs/normes_9_10/RAPPORT.md:L1-6` |
| L05-212 | 09-26 | C2 (Astra) : bloc impair A33 entièrement fermé (Witt : g⁻ ≥ 22 contre ≤ 20) | C | `C:/home/researcher/Documents/Codex/2026-09-25/brief-astra-n-1-attaque-ind/outputs/etoile_sans_classe_fermee/ETAT_REPRISE.md:L1-6` |
| L05-213 | 09-27 | C1 (Astra) : rang de résidu R = 2 et appui exact 9 incompatibles (droite générique mod 7) | C | `C:/home/researcher/Documents/Codex/2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/ETAT_REPRISE.md:L1-6` |
| L05-214 | 09-25 | Brief Astra n° 2 : audit adverse — L8, L22, L23, g(x) ≤ 17 tiennent ; Théorème A de C2 faux (parité) | C | `C:/home/researcher/Documents/Codex/2026-09-25/brief-astra-n-2-v-rification/outputs/rapport_audit.md:L1-34` |
| L05-215 | 09-25 | Conjecture du repère à 231 vecteurs (Gram des triangles) : ouverte ; obstruction ternaire sur les blocs Paley de taille 105 | O | `C:/home/researcher/Documents/Codex/2026-09-25/brief-astra-n-1-attaque-ind/outputs/conjecture_recherche/RAPPORT.md:L1-12` |
| L05-216 | 09-25 | Témoin affine (brief 3) : prolongement indécis ; restriction globale sur les couplages des 21 blocs | O | `C:/home/researcher/Documents/Codex/2026-09-25/brief-astra-n-1-attaque-ind/outputs/rapport.md:L1-12` |
| L05-217 | 09-25 | Recherche globale par échanges : plateau E = 4464 ; un SRG serait à ≥ 25 sommets modifiés | C | `C:/home/researcher/Documents/Codex/2026-09-25/brief-astra-n-1-attaque-ind/outputs/construction_globale/OBJECTIF_ET_REPARATION.md:L1-6` |
| L05-218 | 09-26 | Automorphismes 1 et 2 : reformulation exacte du cas involutif, aucune élimination | H | `C:/home/researcher/Documents/Codex/2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/BILAN.md:L1-7` |
| L05-219 | 10-04 | C2 (Codex app, 04/10) : obstruction de Wagner et borne duale min L* ≥ 9/7 | C | `C:/home/researcher/Documents/Codex/2026-10-04/ce-qui-a-t-sauvegard-dossier/work/RESULTS.md:L1-30` |
| L05-220 | 10-04 | C2 (Codex app) : support 16 de complément du cube impossible ; coupes non triviales k = 1, 2, 3 | P | `C:/home/researcher/Documents/Codex/2026-10-04/ce-qui-a-t-sauvegard-dossier/outputs/C2_PROLONGEMENT_SUPPORT16_PREUVE_CUBE.txt:L1-8` |
| L05-221 | 10-04 | C2 (Codex app) : paramétrisation entière saturée des N 42×42 symétriques avec NR = 0 (588 paramètres) | P | `C:/home/researcher/Documents/Codex/2026-10-04/ce-qui-a-t-sauvegard-dossier/work/RESULTS.md:L114-121` |
| L05-222 | 10-04 | Second avis sur la fin de la route C (C2) : la conserver comme voie de clôture | H | `C:/home/researcher/Documents/Codex/2026-10-04/ce-qui-a-t-sauvegard-dossier/outputs/SECOND_AVIS_C2_2026-10-04.txt:L1-8` |
| L05-223 | 10-04 | C2 multi-agents (04/10) : D est une permutation symétrique sans point fixe ; C = 6I − 2A − MMᵀ + J PSD de rang 15 | P | `C:/home/researcher/Documents/Codex/2026-10-04/j-ai-un-travail-de-m2/research_brief.txt:L1-12` |
| L05-224 | 10-05 | C1 (Codex app, 05–06/10) : tout Conway contient une fonction courte entière 18, entière 26 ou affine 37 | P | `C:/home/researcher/Documents/Codex/2026-10-05/salut-j-aimerais-que-tu-regardes/PASSATION_CONWAY_C1_2026-10-06.txt:L39-46` |
| L05-225 | 10-05 | Coquille affine de niveau 2 et norme 24 vide ; minimum affine niveau 1 : norme ≥ 21 | P | `C:/home/researcher/Documents/Codex/2026-10-05/salut-j-aimerais-que-tu-regardes/global_affine_level2_exclusion.txt:L1-16` |
| L05-226 | 10-06 | Rigidité exacte de l'union de deux étoiles non adjacentes : K_D défini positif | P | `C:/home/researcher/Documents/Codex/2026-10-05/salut-j-aimerais-que-tu-regardes/global_two_stars_rigidity.txt:L1-20` |
| L05-227 | 10-06 | Verrous C1 au 06/10 (application Codex) : 37 ⇒ 26 non prouvé ; m = e = 0 et 24 noyaux non exclus ; Q23 conditionnel | O | `C:/home/researcher/Documents/Codex/2026-10-05/salut-j-aimerais-que-tu-regardes/PASSATION_CONWAY_C1_2026-10-06.txt:L1186-1244` |
| L05-228 | 10-11 | Dossier externe : Paley(25) reconstruit à partir d'un K5 : 15 classes srg(25,12,5,6) dont les 2 asymétriques | C | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/dossiers_externes/PALEY_ASYMETRIE_DOSSIER/README.md:L1-12` |
| L05-229 | 10-11 | Dossier externe : BvLS à bord libéré : exactement deux classes (BvLS et son jumeau) | S | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/RESULTATS.md:L1-12` |
| L05-230 | 10-11 | Dossier externe : α = 22 à 99 — designs cycliques (72) et « one-rotational » (199) exclus | S | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/dossiers_externes/HOFFMAN_UPDATE_20261011/RESULTATS.md:L1-10` |
| L05-231 | 10-12 | Dossier externe : K7 sous α = 22 — résultats partiels (pas de preuve de K7) | P | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/dossiers_externes/C1_K7_RESULTATS_PARTIELS/PREUVES.md:L1-12` |
| L05-232 | 10-12 | Dossier externe : mots binaires de ker₇(A+4I) de poids 0, 63 ou 77 ; poids 77 ⇔ coclique de Hoffman 22 | P | `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/dossiers_externes/INDEX.md:L16` |
| L05-233 | 10-07 | Codex arbitre de la preuve C2 (T20, réduction A.0–A.9) et lemme « y1 fixé » pour le réseau 003 | P | `C:/home/researcher/Desktop/Recherche_Conway/t20-codex/lemma/T20_BOARD.md:L17` |
| L05-234 | 09-25 | Lemmes C1 (session Claude) L1 et L7–L14 : planchers de torsion | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/100_SYNTHESE_DES_LEMMES.md:L165-173` |
| L05-235 | 09-24 | Lemmes C1 L15, L16, L18 : identités globales et P ≤ 1151 | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/100_SYNTHESE_DES_LEMMES.md:L174-176` |
| L05-236 | 09-25 | Lemmes C1 arithmétiques L2–L4, L17, L19–L23 : fenêtre de k (k = rank₇(A − 3I) − 15) | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/100_SYNTHESE_DES_LEMMES.md:L177-185` |
| L05-237 | 10-15 | Proposition de cohérence de la note 100 : portée réduite le 15/10 | R | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/100_SYNTHESE_DES_LEMMES.md:L3-16` |
| L05-238 | 09-25 | Corollaires C1 de la note 100 : k = 10 ⇒ m(e) ∈ {0,2} et P ≤ 462 ; k ≤ 20 ⇒ toutes les droites 7-dégénérées | P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/100_SYNTHESE_DES_LEMMES.md:L189-204` |

## 4. Routes fermées, et pourquoi

Une route « fermée » est une méthode dont la source établit qu'elle ne peut pas conclure seule (pas une exclusion du graphe).

| Route | Pourquoi elle est fermée | Source |
|---|---|---|
| Gram des composantes des 7 droites d'un sommet, pour r ∈ {37, 39, 41} | Tous ces Grams vivent dans un espace hyperbolique fixe de dimension 14 sur F7, plus petit que les espaces ambiants (18, 16, 14) ; seul le rang 43 reste accessible | L05-045 (`208_CODEX…:L6-16`) |
| Relaxation algébrique de l'étoile de Green (Gram mod 7, sommes) | Deux apices et une ombre se prolongent toujours en dix vecteurs entiers ; LAB l'étend à d ≤ 9 | L05-056 ; `RECHERCHE_ACTIVE_C1.md:L249-252` |
| Obstruction fondée sur les deux seuls apex | Témoin explicite d'Astra (aussi avec somme entière et incidences) | L05-044 |
| Test de rang par blocs de la norme 16 | Ne donne que 15, 17 ou 19, sous la borne 33 | L05-006 |
| Équations de fentes (notes C1 108–109) pour une droite dans six grilles | Un témoin entier les satisfait | L05-038 |
| Motif prisme + maison éloignée à l'ordre 11 | Donne τ ≤ 2048, plus faible que l'existant | L05-027 |
| Census d'ordre ≤ 9 seul pour forcer P > 0 | Il admet un point entier non négatif avec P = 0 (6435 comptes) | L05-149 |
| Comptage grossier (blocs 10×10, deux compressions) | Une matrice entière atteint le plancher avec P = Z = 0 ; la moyenne des compressions est automatiquement PSD | L05-147 |
| Relaxation continue à trois étoiles | Témoin rationnel exact de rang 31 | L05-137 |
| PSD continue seule sur les 84 étiquettes | Centre fractionnaire Γ0 exact (T = 3P, U = 4P) : l'intégralité est indispensable | L05-167 |
| Moments ou traces d'ordre supérieur dans le modèle sans torsion de la note 230 | Toutes les traces découlent de NNᵀ = K | L05-068 |
| Genre du réseau Q pour α = 22 (série Claude) | Toutes les conditions de discriminant sont cohérentes et satisfaites par 271 designs | L05-116 |
| (A) sans positivité | Faux (six candidats de nullité ≥ 4) ; (A) avec positivité réfutée par LAB | L05-140, L05-124 |
| ODD9 universelle comme voie de plafond | Réfutée (58 structures ν14 h-invariantes, gains 8/8) | L05-152 |
| Premiers prolongements des 174 noyaux (fermeture par triangles, relaxation des masques, multiplicités) | Aucun gain : 15/174 noyaux au plafond, 29 faisables, 15 pilotes avec témoin | L05-060 |
| Rigidité de K_x pour l'unicité d'une complétion | BvLS et son jumeau partagent le même squelette : au moins deux complétions | `cw/review/09_codex_14_16oct.md:L87` |
| Constructions λ = 1 asymétriques par reconstruction sans groupe | Ne redonnent que les graphes connus ; Payne GF9 exclu exactement | L05-120 |
| Route Q23 (Hamming) | Conditionnelle : Q23 ni forcé ni exclu (19 cas) | L05-227 |
| Réseaux et moments (application Codex, V10) | Relaxations compatibles ou UNKNOWN | L05-227 |
| Normalisations de signes du modèle à deux étoiles (C2 projection, PSD exacte) | Outils sans gain mesuré | `cw/review/09_codex_14_16oct.md:L128` |

## 5. Questions ouvertes, classées par levier

**Levier A — fermer une couverture finie (ce qui manque pour conclure).**
- Les 174 noyaux de 14 sommets : leur prolongement en srg(99,14,1,2) exclurait C1 (L05-098, O). Réductions conditionnelles
  à 115/52/11/2 types si chaque triangle est dans ≥ 1/2/3/4 grilles (L05-062).
- Le registre des gabarits c3 : 435 ouverts au 19/10 08h50, avec P3, P3NB, K2BC en production AWS (L05-201, O) ; gz3, 8650,
  9744, 9954, 9966, 9179, 9912, 10006 cités ouverts (L05-189, L05-190, L05-202 ; `AGENTS.md:L439`, `L458`).
- La branche c ≤ 2 (LAB : c = 1, 4 708 882 classes ; c = 2 non comparée ; k = 0 non recensé)
  (`…/audit_2026-10-18/AUDIT_GLOBAL_2026-10-18_nuit.md:L22-27`).
- Un certificat portable de la fermeture c(L) ≥ 4 (L05-178, S ; LAB : aucune vérification indépendante).
- S0 (rang 43 sans racines ni normes 16..24) : une borne ≤ 2288 sur les configurations P7/Q29 fermerait S0 (L05-081).
- P3/N25 : 4581 supports ouverts après la note 246, 3640 puis 3343 après les lemmes de LAP (rapportés) (L05-083, L05-087).
- Norme 16 : quatre attaches cas 3 [0, 1, 21, 22] à coupure de poids 2, et une entrée de bord survivante (L05-097).
- Rubans de transport : triangle de centres alternés du ruban six (deux fermetures) ; cycles longs réparés (L05-074, L05-077).
- Famille 2K2N entière, K2BC, GEN (L05-199, L05-200).

**Levier B — une inégalité universelle de rang ou de spectre.**
- N9-NG ⇔ rang(F) ≥ 12 universel (L05-170) ; SYM6 (rang Z ≥ 3), ODD-PURE (δ = 0), ODDCONST (rang W = 9), D9 (L05-171, L05-174).
- NG7 et NG5 (L05-150) ; C4DO générale, SYM, QUOT (L05-156, L05-157) ; KER-SYM et SUM14 restreintes à ν ≥ 14 (L05-153).
- H-MATCH (L05-158) ; conjectures (B) et (C) (L05-140) ; H4' (`cw/review/09_codex_14_16oct.md:L106`).

**Levier C — bornes de comptage.**
- « Rang 37 ⇒ P > 0 » (cible ; plafonds trop larges, L05-063 ; census entier P = 0, L05-149).
- Trois prismes jumeaux hors grille à apices indépendants (L05-086).
- Résidu (6,6) : deux hypothèses ouvertes (absence de torsion équilibrée sur les droites connexes ; obstruction uniforme des étoiles génériques) (L05-047).

**Levier D — complétion et reconstruction.**
- Existence des données binaires (G, N) d'une première complétion au rang 37 (L05-069, L05-070) ; seuil 240 + 7q (L05-067).
- Construire B, D pour un bord de 43 sommets ; famille co-Heawood (L05-108, L05-109) ; famille (0,2) entière ; aucune borne
  α ≥ 21 n'est démontrée (`AGENTS.md:L1996-1997`).

**Levier E — fonctions courtes (application Codex, 05–06/10).**
- Implication affine 37 ⇒ entier 26, peut-être fausse ; sous-cas m = e = 0 (24 noyaux, branche connexe) ; Q23 (L05-227).

**Levier F — asymétrie.**
- Aucune construction d'un srg asymétrique à λ = 1 ; cible Γ6 racine 0 préservant K_0 (L05-117) ; relèvement S3 de BH (L05-115).

**Historique C2 (branche close ailleurs).** EX de MODEL.md restait ouvert dans les dossiers du 04/10 (L05-220) ; le dossier
Codex n'établit pas la clôture de C2, qui est rapportée par la passation C1 du 07/10 (`c1-main-codex/PASSATION_C1_2026-10-07.md:L8-9`).

## 6. Contradictions, retraits, réfutations, redécouvertes

**Retraits (X) et rétractations.**
- Bug OR-Tools 9.15 (`domain[-1]` = 0) : 162 verdicts des pilotes c3 retirés, 5 verdicts du modèle partiel retirés, familles c4 7, 9, 19
  réouvertes (L05-179). Le pilote « c_min ≥ 3 : 8/8 gabarits exclus, 162/162 couplages » est retiré (en-tête de
  `PILOTE_CMIN3_2026_10_18.txt:L1-6`). **Contradiction interne** : la section « Direction active » d'`AGENTS.md:L666-675`
  présente encore ce pilote comme terminé ; elle est antérieure à la correction de 11h40 (`AGENTS.md:L657-662`).
- Verdicts LAB « sans Gram » des messages 1067, 1069, 1071 (même bug) (L05-180).
- Annonce de fermeture de S0 au message 500, retirée au message 501 (la liste de 29 supposait tous les triangles internes) (L05-082).
- Quasi-contradiction numérique de LAB au message 517, retirée au message 518 (L05-086).
- Loi générale de parité d'holonomie de LAB (NOTE 17.85), retirée en NOTE 17.86 (`RECHERCHE_ACTIVE_C1.md:L580-587`).
- Seuils LAB « ≥ 43 puis 44 grilles au rang 35 » (msg 182, archive 74068d6) : non établis, remplacés par ≥ 16 grilles (L05-016).

**Réfutations (R).**
- (A) « Q connexe + T, U PSD ⇒ rang 31 à trois étoiles » : contre-exemple de rang 30 (LAB, msg 741) (L05-124).
- ODD9 universelle (L05-152) ; SUM14 universelle (ν13) ; KER-SYM universelle (ν9) (L05-153).
- « corank(Q) ≤ 4 » sur les blocs locaux non grille (urep100 : corang 7) (L05-170).
- « Absence de relations mixtes » à nullité 9 (`AGENTS.md:L1506-1510`) ; « une seule saturation » (`AGENTS.md:L1432`) ;
  « S10 laplacien à poids non négatifs » (`AGENTS.md:L1771-1773`) ; « tous les cycles multiples de 4 » (`cw/review/09…:L85`).
- Théorème A de C2 (« rang pair ») : faux, le rang est impair (L05-214).
- Proposition de cohérence de la note 100, version forte (L05-237).

**Corrections de Codex à ses propres annonces.** Dimension de noyau de 8650 : 5 et non 6 (L05-189) ; message 722 (carré tordu)
rectifié par LAB 727 (L05-138) ; message 775 (126² cas annoncés trop vite) (`cw/review/09…:L110`) ; correction de
nouveauté du bloc 60 (L05-187) ; extrapolation LAB « 6,3 M mondes PSD » corrigée par Codex (L05-091).

**Redécouvertes (même résultat établi deux fois).**
- P ≤ 1151 : L16 de C1 (24/09, notes/70) et PRISM9 de Codex (14/10, nuit sans anciennes notes) (L05-235, L05-125).
  P ≤ 1150 (14/10) et ρ ≤ 191 (14/10) sont plus faibles que P ≤ 852 et ρ ≤ 126 (08/10) (L05-127, L05-129, L05-019).
- Norme 14 = configuration de Fano / co-Heawood : note C1 110 (25/09), Codex 165 (07/10, qui le signale), note co-Heawood (12/10),
  nuit du 14/10 (L05-001, L05-110, L05-129).
- Binarité des petites normes : application Codex (05/10 : jusqu'à la norme 24), notes 165, 171, 176 (07–08/10), nuit du 14/10 (L05-225, L05-132).
- Co-Heawoods ≤ 396 (14/10) : redécouverte par une autre voie **avec un gain** : a_7 ≤ 792 au lieu de 842 (08/10) (L05-133, L05-026).
- τ ≤ 2871 (14/10) contre τ ≤ 1354 (08/10) (L05-134, L05-041).
- Critère L23 de C1 (25/09) retrouvé par LAB au message 445 (09/10) (L05-067, L05-236).
- Spectre du bloc lointain de 60 sommets : note C1 114 (25/09), LAB 17.90 (09/10), puis Codex 18/10 (L05-187).
- Exclusion des automorphismes d'ordre 11 par Astra (25/09) : déjà dans les exclusions publiées consultées par Astra (L05-207).
- Preuve directe de l'intégralité de D (C2, 04/10) : preuve alternative d'un résultat connu (T4) (L05-220).
- Équivalence (N, D) ⇔ involution à un point fixe (04/10) : « établie avant cette vague » (L05-223).
- « g⁻ = 16 force un prisme » (Astra, 26/09) et note C1 132 « g⁻ = 16 est impossible » (26/09) : à recouper (lot L09) (L05-208).
- Comptage GM à un bloc : reproduction par Codex d'un résultat LAB du 12/10 (`…/codex_lambda_one_construction_20261014/bridge_followup.txt:L1`).

**Collision de noms.** Deux séries de notes numérotées 165–178 coexistent dans conway99-c1 (Codex, 07–08/10 ; Claude, 11–12/10).
Les citations « note 171 » ou « note 178 » sont ambiguës sans le nom de fichier (L05-114, L05-232).

## 7. Ce que LAB a revérifié (ou non) des résultats de Codex

| Résultat Codex | Vérification LAB | Source |
|---|---|---|
| P ≤ 852 (note 182) | Revérifié le 18/10 : recensement indépendant identique, certificat vérifié exactement, PL refait (max 852,923) | `…/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:L26-28`, `L211-238` |
| 3P + 4G ≤ 2772 | Vérifié de la même façon | idem `L28-31`, `L251-256` |
| E3 (rectangles à trois arêtes) | Relu le 17/10, redémontré le 18/10 | idem `L118-124` ; `AUDIT_GLOBAL_2026-10-18_nuit.md:L17-21` |
| T² = 7T, formules de R | Relus les 17 et 18/10 | `AUDIT_GLOBAL_2026-10-18_nuit.md:L17-21` |
| Fermeture c(L) ≥ 4 (79/79) | **Aucune vérification indépendante** ; zscan1 (code de Codex) : 164 certificats sur 200 | `AUDIT_GLOBAL…:L29-35`, `AUDIT_EXCLUSIONS…:L159` |
| Paquet de recensement d'ordre 8 | Vérifié sur bvls243 et twin243 (aucune différence) | L05-021 |
| b_1 ≤ 44 (note 192) | Chaîne relue et confirmée (msg 250) | L05-029 |
| Binarité de la norme 20 (note 176) | Première preuve redérivée et confirmée (msg 171) | L05-013 |
| Canal (9,0) (note 198) | Vérifié à la main (msg 295) | L05-035 |
| Motif forcé (note 218) | Preuve relue et confirmée (msg 396) | L05-055 |
| P3-closure (nuit du 14/10) | « LAB633 a confirmé le lemme » | L05-128 |
| Co-Heawoods ≤ 396 | Calcul C4/résidu vérifié, lemmes préalables non relus | L05-133 |
| Notes 232–260, notes des 12–16/10 (sauf ci-dessus), familles c3 du 19/10 | Aucune relecture LAB consignée ; consigne « deux chercheurs, pas de vérifications croisées » du 14/10 | `AGENTS.md:L1929-1940` |

En sens inverse, Codex a consommé sans réaudit : la borne globale rang_F7(8T) ≤ 28 (L22/L23 de C1), ρ ≤ 126, DISC, le
contre-exemple de (A), les contre-exemples d'ODD9, KER-SYM et SUM14, le bilan H-MATCH (416 classes) et « H-MATCH ⇒ point de
Hamming » (`cw/review/09_codex_14_16oct.md:L175`).

## 8. Notes lues, parcourues, non lues

**Méthode.** Les sous-agents prévus n'ont pas pu être lancés (limite de concurrence de la session atteinte). La lecture a donc
été faite directement et de façon hiérarchisée : journaux d'état en entier, puis en-tête et résultat de chaque note, puis
sections ciblées. Rien n'est résumé de mémoire ; les statuts viennent des en-têtes. Une affirmation reprise d'un journal porte
la ligne du journal.

**Bilan sur les 991 contenus du lot** (codes de l'annexe 8.1) :

| Code | Nombre | Signification |
|---|---:|---|
| L | 6 | lu intégralement : `MC:AGENTS.md` (journal Codex 13–19/10, 2073 lignes), `MC:RECHERCHE_ACTIVE_C1.md` (869 lignes), `CH:notes/100_SYNTHESE_DES_LEMMES.md`, `conway99-c1:origin/codex/c1-arithmetic-audit:AGENTS.md` (2 Ko), `dossiers_externes/INDEX.md`, `brief-astra-n-2/outputs/LISEZ_MOI.md` |
| P | 454 | parcouru : en-tête et énoncé du résultat (L1–~22), plus sections ciblées pour les notes clés |
| T | 190 | titre seulement : notes individuelles des sous-dossiers Astra du 25–27/09 (PREUVE, CERTIFICAT, AUDIT…), couvertes au niveau des fichiers d'état ETAT_REPRISE / RAPPORT / BILAN |
| N | 341 | non lu, avec la raison (copies LAB : 136 ; sorties brutes et empreintes : 63 ; données : 44 ; compilations cumulatives : 19 ; annexes de dossiers externes : 19 ; copies de notes C1/C2 : 12 ; résumés non relus directement : 6 ; etc.) |

**Lectures partielles importantes à signaler.**
- `CH:notes/JOURNAL_C1_NUIT_2026_10_14.md` (410 Ko, 6824 lignes) : seuls les titres de sections ont été lus. Les énoncés des
  14–16/10 viennent d'`AGENTS.md` (lu en entier, qui reprend le journal) et de la revue LAB `C:/home/researcher/cw/review/09_codex_14_16oct.md`
  (lot L09, résumé secondaire, lui-même partiel et arrêté). Chaque fiche de cette période cite la ligne de section du journal.
- `CH:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md` (190 Ko) : premières lignes des 79 sections seulement.
- `CH:notes/MOMENTS_SIGNATURES_C1_2026_10_16.txt` (99 Ko) : §1, §9, §19 et titres.
- Dossiers Astra du 25–27/09 (2,1 Mo de notes courtes et 20 Mo de compilations) : niveau des fichiers d'état seulement. Les
  exclusions individuelles de types (forêts, certificats) ne sont pas détaillées : seuls les bilans cumulés sont repris (L05-209).
- `DC:2026-10-05/…/PASSATION_CONWAY_C1_2026-10-06.txt` (1342 lignes) : §0, 1, 8, 17–20 ; les §3–7 et 9–16 n'ont pas été lus.

**Consulté hors du lot** (pour l'attribution, les statuts et les vérifications LAB) : `cw/review/09_codex_14_16oct.md` (L09) ;
en-têtes de notes Codex classées dans L08/L09 : `CARRE_DE_DEFAUT_ET_PARITE`, `GRAM_DES_GRILLES_ET_BLOC60`,
`CERTIFICAT_SANS_GRAM_9748`, `RANG7_ET_SATURATION`, `COEUR_HUIT_SOMMETS_5602`, `COEUR_PARTAGE_DEUX_GRILLES` ; deux notes du
20/10 **hors inventaire** (`TROIS_COLONNES_EGALES_INTERDITES`, `BUDGET_ENTIER_SUPPORT_SIGNE`, créées à 18h47) ;
`Documents/Codex/CONWAY_NOUVEAUTES_27_09_2026/LIRE_D_ABORD.md` (lot L01). Non lus, bien que Codex : `NOYAUX_SIGNES_K2BC`,
`BLOCS_PARTIELS_ET_COUPE_ENERGIE`, `CONTROLE_C2_COUCHES`, `COUPLAGES_SIGNES_ET_COINS_SANS_GRAM`, `FERMETURES_ET_ABLATIONS_SANS_GRAM`,
`HISTOGRAMMES_PROPRES_SANS_GRAM`, `C2_DES_GRILLES` (lots L08/L09 ; leur contenu n'est repris que via `AGENTS.md`), les fichiers
`t20-codex/lemma/t20_CODEX/*` (arbitrages de Codex pour T20, hors lot) et le dossier `fermeture_A33/` (non inventorié).

**Interdits respectés.** Aucun dossier `claude-codex-bridge` ouvert ; rien lu sous `~/.codex` ; `Desktop/mdp.txt` non lu. Les
fichiers `bridge_*.txt` lus sont des copies de messages rangées par Codex dans `data/` de son dépôt.

### 8.1 Annexe : statut de lecture de chaque contenu du lot (ordre du fichier de lot)

| Code | Emplacement (première copie) | Blob | Taille | Raison |
|---|---|---|---:|---|
| N | `2026-09-11/j/outputs/gamebeast-external-security-review-2026-09-11.md` | 8a993a1b | 13964 | hors sujet (revue de sécurité « Gamebeast », sans rapport avec Conway) |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:JOURNAL.md` | 895d1b1f | 63807 | début et recherche « Codex/Astra » (journal de la session C1, pas Codex) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:LAB_INSTRUCTIONS_C1.md` | 5bc629ac | 4667 | consignes de poste/session, sans résultat |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/POURSUITE_RECHERCHE.md` | 0e584361 | 11481 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/REPRISE_27_0435_LIVRAISON.md` | f8ab4ecd | 1196 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/REPRISE_27_SUIVI_STRUCTURES_LIVRAISON.md` | 04210cdd | 917 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/attaque_conjectures/ETAT_REPRISE.md` | c64a5794 | 2668 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/attaque_globale_27_1132/CLASSES_COURTES_COMPLEMENT15.md` | f29827f9 | 2781 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/attaque_globale_27_final_agressive/COUPE_TYPE_I_D6_ET_OBSTACLE.md` | c4fa77c9 | 9062 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/BILAN.md` | 87b16517 | 8996 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/asymetrique/asymetrie_et_reflexions.md` | 44f9daaf | 10300 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/audit/ETAT_ET_LIMITES.md` | f8147266 | 9473 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/involution/etoiles_et_schur.md` | 67dd620f | 6799 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/involution/quotient_exact.md` | 05c90bca | 9527 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_algebre/audit_15_paires.md` | 6b935c8f | 5641 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_algebre/catalogue_rang4.md` | e8f9a37b | 6180 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_algebre/coupe_conjointe.md` | dae2d37d | 5421 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_algebre/extensions_entieres_rang4.md` | 60feb5ab | 7853 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_audit/LIMITE_UNICITE_ET_COMMUTATEUR.md` | c91f59e2 | 8519 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_audit/NOTE_ARITHMETIQUE.md` | f1b5136e | 10790 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_audit/UNICITE_RANG2_RANG4.md` | ddae074b | 11789 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_geometrie/apices_et_comptages.md` | 0e30a3af | 6963 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_geometrie/audit_type0_prismes.md` | c3b06547 | 3193 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_geometrie/exclusion_double_C6.md` | 68bbb44a | 6814 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_geometrie/incidences_rang4_audit.md` | 1e45867a | 3305 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_geometrie/oppositions_sans_reflexion.md` | e80a9248 | 2956 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase2_geometrie/reflexions_globales.md` | 675105fd | 7308 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/phase3_racine/BILAN_PHASE3.md` | 80d43bdd | 7577 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/bibliographie_critique/NOTE.md` | bfd4c21b | 5713 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/cent_idees/CHAINONS_SPONTANES.md` | c9e75943 | 26977 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/cent_idees/RAPPORT_100_IDEES.md` | a1efcb5d | 30828 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/conjecture_recherche/E8_vers_126.md` | 9f8b86b6 | 5924 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/conjecture_recherche/G231_non_cayley.md` | 6e8a3d15 | 6431 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/conjecture_recherche/RAPPORT.md` | f6271627 | 12542 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/conjecture_recherche/SHA256SUMS.txt` | c999256e | 1560 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/conjecture_recherche/blocs_et_groupes.md` | f055eff1 | 4061 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/conjecture_recherche/obstruction_incidence_lineaire.md` | 41024101 | 4802 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/conjecture_recherche/repere105_et_variantes.md` | 6376abd9 | 8348 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/construction_globale/AUDIT_TRIANGLES.md` | f7b6b0b7 | 5441 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/construction_globale/BILAN_COEUR.md` | f6fb0af8 | 10488 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/construction_globale/OBJECTIF_ET_REPARATION.md` | f732c50b | 5459 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/construction_globale/audit_moves.md` | 313af0b4 | 5412 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/construction_globale/bilan_projection_spectrale.md` | 18e52668 | 3325 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/construction_globale/bilan_switches.md` | c38aebb1 | 5255 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g16/DOSSIER_COMPLET.md` | 0d2dc959 | 338610 | compilation cumulative des notes du même dossier (non relue) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g16/ETAT_REPRISE.md` | 739f35d7 | 3625 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g16/LEMME_COUPLAGE_D_G18.md` | 976719f0 | 11987 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g16/PREUVE.md` | ff3d24cd | 15538 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g16/sorties_controles.txt` | 3fff80ee | 288 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g16/sorties_decouverte.txt` | 3f796f83 | 1252 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g16/sorties_independantes.txt` | d1132f77 | 2849 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g18/AUDIT_INDEPENDANT.md` | ec93829e | 9468 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g18/DOSSIER_COMPLET.md` | e4607a24 | 277874 | compilation cumulative des notes du même dossier (non relue) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g18/ERRATUM_SCIENDE.md` | 8c7d4427 | 467 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g18/ETAT_REPRISE.md` | e5f976e2 | 4944 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g18/PREUVE.md` | 08a67d6e | 17824 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g18/sortie_audit_schur.txt` | 65717ce1 | 2227 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g18/sortie_projection_independante.txt` | b511bfe6 | 1051 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g18/sortie_verification_38.txt` | 5af9822b | 12859 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g18/sorties_controles_D.txt` | 56c94842 | 1777 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g18/sorties_controles_projection.txt` | 749de1a6 | 636 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/deep_research/AUDIT_RETOUR.md` | d7320d25 | 2930 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/deep_research/PROMPT_RECHERCHE_CIBLEE.md` | 5411e56a | 17408 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/deep_research/RELANCE_CREATION_LEMMES.md` | 010971dd | 6703 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/dossier6_involution/AUDIT_GENRE.md` | cd722c40 | 13328 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/dossier6_involution/ETAT_REPRISE.md` | 1ab1074e | 3071 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/dossier6_involution/NOTE_RESEAU_MINIMUM.md` | ac0baf9a | 7343 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/dossier6_involution/PREUVE_RESEAU.md` | ac958974 | 7602 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/dossier6_involution/VERIFICATION_INDEPENDANTE_G10.md` | a0d9549e | 3681 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/etoile_sans_classe_fermee/ETAT_REPRISE.md` | 621b354e | 4635 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/etoile_sans_classe_fermee/RAPPORT.md` | 2ec9c231 | 11781 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/g18_algebre_neuve/ENERGIE.md` | a474e12c | 10948 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/g18_algebre_neuve/NOTE.md` | e9bd413e | 9774 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/global_transport/transport_sans_prismes.md` | 83d80640 | 6452 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/AUDIT_ARC_GLOBAL_G18.md` | 462bbf53 | 5513 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/AUDIT_BILANS_FULL_H49.md` | e921f844 | 7615 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/AUDIT_GRAM_GLOBAL.md` | 821f3e02 | 8410 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/AUDIT_SUPPORT_RESIDUEL_HUIT.md` | 4fa36976 | 5609 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/COMPRESSION_OBSTRUCTIONS_G18.md` | 5d768c69 | 4828 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/COUPURE_PARITE_BLOCS.md` | 675e4c0c | 3020 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/DOSSIER_COMPLET.md` | 730f03ac | 1121781 | compilation cumulative des notes du même dossier (non relue) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/ETAT_REPRISE.md` | f956953c | 5231 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/GAUGE_PREMIER_RESIDU.md` | 1cdc6c92 | 8429 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/MOMENTS_COLLECTIFS.md` | 0cabb8c5 | 14091 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/NEXT_PLAN_CANONIQUE_ET_FLUX.md` | 4239b8e7 | 9919 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/PLAN_COMMUN_G20.md` | eeeccc33 | 7200 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/PREUVE_COUPURES_BILANS.md` | 710b45a1 | 3213 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/PREUVE_FORET_DIRECTE.md` | a9f51dc6 | 9345 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/PREUVE_SELECTION.md` | 75b6c47b | 4349 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/RAPPORT.md` | a41ecef2 | 14829 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/gram_global_g18_g20/SUPPORT_RESIDUEL_D6.md` | 34b81614 | 8707 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/integration_c1/sources/C1_116.md` | 7b2a131a | 5980 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/integration_c1/sources/C1_117.md` | 5316a1c5 | 9808 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/ligne_residu8/verdict_residu8.md` | 9908141e | 7062 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/lookahead_log.txt` | 172d3448 | 2616 | sortie brute, journal ou empreintes |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/mission_audacieuse/README.md` | a641b54d | 7886 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/mission_audacieuse/SHA256SUMS.txt` | 395f8c21 | 1142 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/mission_audacieuse/code_triangles.md` | c3add962 | 7831 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/mission_audacieuse/conjecture_repere.md` | 87802d73 | 6050 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/mission_audacieuse/geometrie_39.md` | 521646c8 | 6525 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/mission_audacieuse/preuve_ordre11.md` | 084665b0 | 13530 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/mission_geometrique/README.md` | 6fb6e865 | 11234 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/mission_geometrique/SHA256SUMS.txt` | de4b2ffc | 1486 | sortie brute, journal ou empreintes |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/normes_9_10/ETAT_REPRISE.md` | 6b594476 | 8007 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/normes_9_10/PREUVE_CAPACITE.md` | 2fabd397 | 6858 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/normes_9_10/PREUVE_TRIANGLE_SELECTIONNE.md` | d86caa7e | 1641 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/normes_9_10/RAPPORT.md` | b4eed5a6 | 7677 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/normes_9_10/README.md` | f964cdd8 | 1978 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/normes_9_10/sorties.txt` | 01db12ae | 3448 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/poursuite_E8/audit_couplage_cyclique.md` | 851d5900 | 10262 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/poursuite_E8/catalogues_et_couvertures.md` | 218ddc06 | 5615 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/poursuite_E8/code_ternaire_conway.md` | 098865e3 | 12948 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/poursuite_E8/complements_et_parite.md` | 25d4be89 | 6993 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/poursuite_E8/composantes_tensorisees.md` | cb0fa138 | 7184 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/poursuite_E8/etoiles_modulo3.md` | 3d64c5c9 | 3719 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/poursuite_E8/exclusion_partition_14_A3.md` | ce5d731b | 3747 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/poursuite_E8/obstruction_mod3_paley.md` | cb0039cd | 5023 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/poursuite_E8/orthogonal_tiles_cut.md` | f9b90788 | 4079 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/poursuite_E8/quatre_A3_impossibles.md` | 0044c1cf | 5059 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/poursuite_E8/rapport_recherche_bornee.md` | 8e9bd87f | 4811 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/poursuite_Leech/exploration_Leech_G126.md` | c15d9fd8 | 7193 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/rapport.md` | 6b02d964 | 10714 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0047/APPLICATION_COUPURE_OMBRES_FORTE.md` | 0a34f45b | 2607 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0047/AUDIT_COMPLET_SUPPORT8.md` | 952268ea | 10588 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0047/AUDIT_REJEU_FORET.md` | 54afd45c | 4347 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0047/CLASSIFICATION_SUPPORT8.md` | e97194c3 | 14012 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0047/DEUX_COLONNES_LIBRES_APPUI8.md` | f9fd37fa | 8075 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0047/DOSSIER_COMPLET.md` | 10142bcb | 1404548 | compilation cumulative des notes du même dossier (non relue) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0047/ETAT_REPRISE.md` | 50250533 | 5435 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0047/PREUVE_TROIS_TYPES_G18.md` | 220bbbf0 | 4850 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0047/RAPPORT.md` | b5982a63 | 10111 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0148/ADDENDUM_C1_APPUI9_DEGRE2.md` | 3fae466d | 9499 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0148/AUDIT_C1_APPUI9_K33.md` | 1a990c80 | 6278 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0148/AUDIT_C1_DEGRE2_APPUI9.md` | e08e3ff1 | 5422 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0148/AUDIT_TERNAIRES_ET_RELAXATIONS.md` | 06e44c4c | 5301 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0148/DOSSIER_COMPLET.md` | 18650422 | 1603552 | compilation cumulative des notes du même dossier (non relue) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0148/ETAT_REPRISE.md` | 9973a8e2 | 6078 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0148/ETAT_REPRISE_PARENT_AVANT.md` | 43a38270 | 30947 | compilation cumulative des notes du même dossier (non relue) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0148/RAPPORT.md` | 6edba27c | 10210 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0148/REFLET_COMMUN_ET_BUDGETS.md` | 3deb20ef | 8271 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0148/RELATIONS_TERNAIRES_ET_CENTRES.md` | 127df0bd | 8941 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0148/THEOREME_C1_APPUI9_K33.md` | b5d275a4 | 6780 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/AUDIT_1020_BUDGETS_ET_PROFILS.md` | 6b854f3f | 4741 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/AUDIT_C1_APPUI9_COMPLET.md` | 5453990f | 7822 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/CERTIFICAT_TYPE34.md` | 330f764b | 5312 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/DOSSIER_COMPLET.md` | 6fe0b4af | 2969416 | compilation cumulative des notes du même dossier (non relue) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/ETAT_REPRISE.md` | f23d0a23 | 2374 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/FERMETURE_C0_S8_1020.md` | 12561526 | 7188 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/FONDEMENTS_C1_SCHUR.md` | d57cd00a | 2259 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/PREUVES_NOUVELLES.md` | d34d514f | 68773 | compilation cumulative des notes du même dossier (non relue) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/RAPPORT.md` | e15abf39 | 8515 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/STATUT_C1_APPUI9.md` | b4dd0991 | 1509 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/THEOREME_C1_APPUI9_COMPLET.md` | 2837ff2a | 13461 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0249/TROIS_PROFILS_C0_S7_FERMES.md` | f070e6ce | 2375 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/AUDIT_C7_COUVERTURE_ET_PREFIXE.md` | 38d39053 | 3760 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/AUDIT_C7_SUITES_ET_BORNE_LINEAIRE.md` | 9e077c6f | 4156 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/AUDIT_COUPLAGE_ELL_ET_CONTROLES.md` | 026d0e7e | 3642 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/AUDIT_RACCORD_C7_FORME_COMMUNE.md` | 9236beb7 | 3736 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/BILAN_AUDIT_0435.md` | a8b9b2be | 3519 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/CERTIFICAT_C7_678_FAMILLES.md` | 8ec8296c | 5481 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/CERTIFICAT_TYPE35.md` | 3eabada2 | 5133 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/DOSSIER_COMPLET.md` | 4d472f6a | 3457347 | compilation cumulative des notes du même dossier (non relue) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/ETAT_REPRISE.md` | 921de7f5 | 4607 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/FLUX_PARTIAL_INHOMOGENE.md` | e0a980e6 | 4379 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/G20_C7_COUVERTURE_ABSTRAITE.md` | 7361e3a2 | 3998 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/G20_C7_NORMES_COUPLEES.md` | 1cdfd1cb | 4673 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/G20_C7_PREFILTRE_PREUVE_ET_BORNE.md` | 5165685f | 7067 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/G20_C7_TOUT_MU_NOTICE.md` | ffb97499 | 2442 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/G20_C7_UNAIRES_TAU.md` | 0fa21e50 | 3394 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/LIRE_D_ABORD.md` | 543338dc | 1182 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/PARTIAL_ELL_COMMUN.md` | a73f7ec7 | 12973 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/PREUVES_COMPLETES_RECENTES.md` | 62f0bc61 | 242257 | compilation cumulative des notes du même dossier (non relue) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/PREUVE_UNION_TYPE35.md` | 6c17652f | 1959 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/RAPPORT_POUR_C1_C2_STRUCTURES.md` | 6b181387 | 11177 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/REPRODUCTION_ET_CERTIFICATS.md` | 71002ca3 | 3897 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/SHA256_MANIFESTE.txt` | d6209832 | 88 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/TRIPLET_PHYSIQUE_TYPE202.md` | 34e5eb2e | 3094 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0435/diagnostic_audit_type35_002.txt` | 148b722c | 287 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/AUDIT_C7_UNION_1254.md` | f31fd707 | 3522 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/AUDIT_EGALITE_SCHUR_RANG3.md` | e00df2c7 | 5196 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/AUDIT_RACCORD_TYPE40.md` | cbf38465 | 2179 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/AUDIT_SCHUR_SINGULIER_GENERAL.md` | d8680028 | 5782 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/BILAN_AUDIT_0535.md` | dcbd4d8c | 2481 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/CERTIFICAT_TYPE39.md` | 5b4fdda8 | 2219 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/CERTIFICAT_TYPE40.md` | b03588e5 | 1920 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/DOSSIER_COMPLET.md` | a761bcab | 3531201 | compilation cumulative des notes du même dossier (non relue) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/EGALITE_SCHUR_RANG3_G20.md` | aeb9927d | 12322 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/ETAT_REPRISE.md` | 555d28a1 | 4973 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/G18_TYPE39_NOTICE.md` | 8b74834f | 5434 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/G18_TYPE40_NOTICE.md` | 5628eb6d | 1892 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/G18_TYPE40_PROGRESSION.md` | 75545e1f | 1226 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/LIRE_D_ABORD.md` | 9830a84d | 1138 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/LIRE_D_ABORD.txt` | c357eaf7 | 1136 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/PREUVES_COMPLETES_RECENTES.md` | 9841b4e5 | 316058 | compilation cumulative des notes du même dossier (non relue) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/RACCORD_SINGULIER_TEMPLATE_C7.md` | bdd447b8 | 13912 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/RAPPORT_POUR_C1_C2_STRUCTURES.md` | f9633cb6 | 13987 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0535/SHA256_MANIFESTE.txt` | 9e693c52 | 88 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/AUDIT_PREUVES_EXTRAS_D4.md` | 0dd9f5b9 | 3521 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/AUDIT_RACCORD_TYPE41.md` | dbba351e | 2267 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/AUDIT_SATURATION_SCHUR5.md` | 74c186b0 | 5520 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/AUDIT_TYPE281_REGIMES.md` | 7e6003a1 | 3053 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/AVANCEES_COMPLETES_PREUVES.md` | babb4d1d | 396153 | compilation cumulative des notes du même dossier (non relue) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/BILAN_AUDIT_INDEPENDANT_0636.md` | 3c17a12d | 2550 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/CERTIFICAT_TYPE41.md` | 03f305a8 | 1593 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/COVARIANCE_MOD4_ET_CONTROLES.md` | 8178276e | 3717 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/ETAT_REPRISE_SNAPSHOT.md` | 26f1968d | 60761 | compilation cumulative des notes du même dossier (non relue) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/G18_TYPE41_NOTICE.md` | f7d2a2cb | 2176 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/G18_TYPE41_PROGRESSION.md` | 82e3d6db | 1226 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/PREUVE_TYPE41_REGLES.md` | e3ab7b61 | 8512 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/RAPPORT_POUR_C1_C2_STRUCTURES.md` | 61c667ee | 10336 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/README_LIVRAISON.md` | dfaf5cbc | 1817 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/SHA256_MANIFESTE.txt` | ed7378ca | 88 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/TROIS_CIRCULATIONS_APPUI8.md` | b57d0283 | 11511 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/TROIS_EXTRAS_MEME_BLOC.md` | 41f10546 | 7772 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0636/TYPE281_CHARGES_ET_SCHUR5.md` | 866fd906 | 13437 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/AUDIT_EXTENSIONS_TROIS_RACINES.md` | 9adf909e | 7763 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/AUDIT_RACCORD_TYPE44.md` | 3c6cbd9e | 4402 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/AVANCEES_COMPLETES_PREUVES.md` | 848d1700 | 451145 | compilation cumulative des notes du même dossier (non relue) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/CERTIFICAT_TYPE44.md` | b5bfb5a2 | 1597 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/EDITEUR005_CONTROLE.txt` | dae6a07c | 62656 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/ETAT_REPRISE_SNAPSHOT.md` | b1bc44ad | 67128 | compilation cumulative des notes du même dossier (non relue) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/EXTENSIONS_EXACTES_TROIS_RACINES_D4.md` | e4fe1139 | 14738 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/G18_TYPE44_NOTICE.md` | acbc3405 | 2286 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/G18_TYPE44_PROGRESSION.md` | 448026b2 | 1232 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/LIRE_D_ABORD.txt` | 181effdb | 571 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/NOTE_EDITEUR_DISTANT.md` | 7d065573 | 724 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/OMBRES_TROIS_EXTRAS_1526.md` | 632bca3e | 6231 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/PREUVE_TYPE44_COMPLETE.md` | f4845ef5 | 9245 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/PREUVE_TYPE44_REGLES.md` | bdc64da9 | 6993 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/RAPPORT_POUR_C1_C2_STRUCTURES.md` | e6f9f242 | 12130 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SHA256_MANIFESTE.txt` | 023cde5e | 88 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_001_SLICE_01.txt` | f784fb8c | 603023 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_002_SLICE_01.txt` | 8ab4850e | 733984 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_002_SLICE_02.txt` | 1f151452 | 1336141 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_002_SLICE_03.txt` | 8c3f6225 | 1472567 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_002_SLICE_04.txt` | ded30e02 | 3809 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_003_SLICE_01.txt` | ae88df4d | 2055170 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_003_SLICE_02.txt` | 5cf96914 | 730585 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_003_SLICE_03.txt` | e134eca8 | 733426 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_003_SLICE_04.txt` | 14980e74 | 3809 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_004_SLICE_01.txt` | 3651f5b5 | 728025 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_004_SLICE_02.txt` | bc384d56 | 727610 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_004_SLICE_03.txt` | bf585cfd | 721234 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_004_SLICE_04.txt` | b9c85cf3 | 3808 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_005_SLICE_01.txt` | 3a61bca4 | 738058 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_AUDIT_TYPE44_005_SLICE_02.txt` | 8189d7f8 | 618127 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_FORET_TYPE44_001.txt` | 5a0da163 | 269467 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_FORET_TYPE44_002.txt` | ac8d4075 | 1018593 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_FORET_TYPE44_003.txt` | 11f8f9ac | 1024209 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_FORET_TYPE44_004.txt` | 94c2d988 | 1019504 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_FORET_TYPE44_005.txt` | 359c72cb | 586735 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/SORTIE_FORET_TYPE44_005_TENTATIVE_NON_LIEE.txt` | c494b414 | 1072155 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_0736/TROIS_EXTRAS_DEUX_BLOCS_PREUVE.md` | 645d6616 | 4183 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/ALGEBRE_SINGULIERE.md` | acedfb62 | 18991 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/AUDIT_C7_CENTRES_HORS_EMPREINTE.md` | 14d0153c | 5072 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/AUDIT_CHARGES_SINGULIERES.md` | 57424248 | 7791 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/AUDIT_CROISEMENT.md` | b9086241 | 4261 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/AUDIT_G20.md` | 536e39e9 | 2089 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/AUDIT_G20_1020_C0_COMPLET.md` | 9c53a670 | 4865 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/AUDIT_G20_1020_CENTRES.md` | 5e616a85 | 7665 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/CERTIFICATS_FULL_202_277_281.md` | 6fd5d01c | 6789 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/CERTIFICATS_FULL_HUIT_TYPES.md` | c245ce7b | 6558 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/CERTIFICAT_TYPE36.md` | f32ae666 | 5361 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/COROLLAIRES_FULL_G18_G20.md` | 50102c93 | 2744 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/DOSSIER_COMPLET.md` | 24dffdbb | 3132424 | compilation cumulative des notes du même dossier (non relue) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/ETAT_REPRISE.md` | 9b0e05f6 | 5624 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/G20_1020_C0_COMPLET_PREUVE.md` | 27ecaf76 | 4165 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/G20_1020_C0_S7_PREUVE.md` | da240e70 | 5276 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/G20_1020_CENTRES_CONCLUSION.md` | 33f9d1f5 | 8118 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/G20_C7_CENTRES_HORS_EMPREINTE.md` | 96df9d37 | 4119 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/G20_C7_PLATEAU.md` | 1b71ae81 | 2035 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/G20_CENTRES_MINORANTS.md` | 56b4bbf1 | 2781 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/G20_CENTRES_ROUTE_NOTICE.md` | 482ece65 | 2108 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/JOURNAL_LIVRAISON.txt` | 131245c2 | 159 | sortie brute, journal ou empreintes |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/LIRE_D_ABORD.md` | fb17bc58 | 1585 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/LISTES_POUR_STRUCTURES.md` | 451aa683 | 3136 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/NOTATIONS_PONCTUELLES.md` | 29ffc161 | 710 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/PREUVES_COMPLETES_RECENTES.md` | 8d744afd | 162412 | compilation cumulative des notes du même dossier (non relue) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/RAPPORT_POUR_C1_C2_STRUCTURES.md` | 03c8b761 | 15328 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/REPRODUCTION_ET_CERTIFICATS.md` | 451646c3 | 4877 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/SHA256_MANIFESTE.txt` | 546ddc1c | 88 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/audit_type36_premier_erreur.txt` | 8b9e2718 | 2000 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/diagnostic_ponctuel_001_erreur.txt` | 16256d75 | 3506 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/reprise_27_suivi_structures/type35_compact_sans_verdict.txt` | e936acfb | 16 | sortie brute, journal ou empreintes |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/salve_directe/RAPPORT.md` | f99e7b1e | 11227 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/salve_directe/algebre/bilan_algebrique.md` | 9fba8285 | 8445 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/salve_directe/algebre/composantes_etoiles.md` | 06544487 | 8967 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/salve_directe/controles/audit_controles.md` | 12265d14 | 4222 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/salve_directe/controles/regle_noyau_et_nouveaute.md` | 21fc3f10 | 5227 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/salve_directe/deux_voisinages_psd_automatique.md` | 39cd31d9 | 3583 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/salve_directe/moteur/bilan_moteur.md` | 7925065b | 7838 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/suivi4_etoiles_et_audit/MESSAGE_1_COMPLET.md` | 5d94e9ee | 7932 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/suivi4_etoiles_et_audit/MESSAGE_2_COMPLET.md` | 3644775c | 9470 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/suivi4_etoiles_et_audit/RAPPORT.md` | b0ce8425 | 15208 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/suivi4_etoiles_et_audit/SORTIES_PROGRAMMES.txt` | 8ab8e574 | 40126 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/suivi4_etoiles_et_audit/TRANSMISSION_COMPLETE.md` | cb6256f9 | 17513 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/AUDIT_FILTRE_R18_RAPIDE.md` | 4e895819 | 7938 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/AUDIT_FILTRE_TORSIONS.md` | d797b12e | 7974 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/AUDIT_JONCTION_TRANSLATIONS_G20.md` | 20c622e8 | 6945 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/DOSSIER_COMPLET.md` | d6ebb895 | 644245 | compilation cumulative des notes du même dossier (non relue) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/ETAT_REPRISE.md` | c78afc5c | 5914 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/GRAM_CHARGES_SIMULTANEES.md` | d1d0ddf9 | 4602 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/PARITE_D6.md` | d2789f2b | 3328 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/PREUVE.md` | 85cc13d3 | 13807 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/PREUVE_TRANSLATIONS_ET_D6.md` | 897356d7 | 12730 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/PRUNING_ANCRAGES.md` | e18fbaf9 | 6040 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/RESIDU_R18_G20.md` | 6a1270f3 | 6566 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/TEMOINS_POSITIFS.md` | dd837313 | 3520 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/TRANSLATIONS_UNIVERSELLES.md` | 96dca326 | 3326 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_paires_18_lot_0.txt` | c1ad6507 | 52072 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_paires_18_lot_1.txt` | 65aa1179 | 52149 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_paires_18_lot_2.txt` | 62e5d56e | 44059 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_paires_18_premier_lot.txt` | 8149f5ce | 3379 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_paires_20_lot_0.txt` | 77cc929e | 15371 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_prix_norme_lot_0.txt` | 12083eab | 3022 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_prix_quatre.txt` | c76faa26 | 5844 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_prix_r17_lot_0.txt` | 46e6469e | 3442 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_prix_r17_lot_1.txt` | b90455db | 2840 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_temoins_20_lot_0.txt` | 4d1483d9 | 36747 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_temoins_20_lot_1.txt` | f1858edc | 152032 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_temoins_20_lot_2.txt` | cc399dc2 | 97068 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_torsions_18_lot_0.txt` | ef39420a | 14292 | sortie brute, journal ou empreintes |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/sweep_g18_g20/sortie_translations_96.txt` | f5f076b6 | 38492 | sortie brute, journal ou empreintes |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/temoin_cinq_triangles/audit_cinq_triangles.md` | 1e9a0b8f | 10523 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| P | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/wagner_fermeture/ETAT_REPRISE.md` | 25db43de | 4246 | fichier d'état/rapport du sous-dossier : en-tête (L1–~15) |
| N | `2026-09-25/brief-astra-n-1-attaque-ind/outputs/wagner_fermeture/sorties_verification.txt` | 7eeeb243 | 1564 | sortie brute, journal ou empreintes |
| T | `2026-09-25/brief-astra-n-1-attaque-ind/work/coeur/literature_triage_2.md` | af6fae29 | 1316 | titre seulement ; contenu couvert par les fichiers d'état du sous-dossier (non relu en détail) |
| L | `2026-09-25/brief-astra-n-2-v-rification/outputs/LISEZ_MOI.md` | 705b5622 | 1886 | lu |
| N | `2026-09-25/brief-astra-n-2-v-rification/outputs/bibliographie_ciblee.md` | 69e48d5e | 16066 | bibliographie ciblée (non lue) |
| P | `2026-09-25/brief-astra-n-2-v-rification/outputs/corrections_C2.md` | 186ae363 | 3391 | parcouru (verdicts et corrections) |
| P | `2026-09-25/brief-astra-n-2-v-rification/outputs/rapport_audit.md` | 59239100 | 27611 | parcouru (verdicts et corrections) |
| N | `2026-09-25/brief-astra-n-2-v-rification/work/sources/C1_030.md` | 32e688e0 | 33372 | copie de notes C1/C2 lues par Astra (originaux : lots L09/L01) |
| N | `2026-09-25/brief-astra-n-2-v-rification/work/sources/C1_080.md` | cddf8cee | 9015 | copie de notes C1/C2 lues par Astra (originaux : lots L09/L01) |
| N | `2026-09-25/brief-astra-n-2-v-rification/work/sources/C1_101.md` | 2b005e63 | 6247 | copie de notes C1/C2 lues par Astra (originaux : lots L09/L01) |
| N | `2026-09-25/brief-astra-n-2-v-rification/work/sources/C1_102.md` | e43383b0 | 15686 | copie de notes C1/C2 lues par Astra (originaux : lots L09/L01) |
| N | `2026-09-25/brief-astra-n-2-v-rification/work/sources/C1_103.md` | c606c270 | 25146 | copie de notes C1/C2 lues par Astra (originaux : lots L09/L01) |
| N | `2026-09-25/brief-astra-n-2-v-rification/work/sources/C1_104.md` | 96b960cf | 11747 | copie de notes C1/C2 lues par Astra (originaux : lots L09/L01) |
| N | `2026-09-25/brief-astra-n-2-v-rification/work/sources/C1_105.md` | 24e0fc84 | 14802 | copie de notes C1/C2 lues par Astra (originaux : lots L09/L01) |
| N | `2026-09-25/brief-astra-n-2-v-rification/work/sources/C1_108.md` | 563c4485 | 8926 | copie de notes C1/C2 lues par Astra (originaux : lots L09/L01) |
| N | `2026-09-25/brief-astra-n-2-v-rification/work/sources/C2_MATH_C2_PROGRAMME.md` | ca0f11ac | 68083 | copie de notes C1/C2 lues par Astra (originaux : lots L09/L01) |
| L | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/100_SYNTHESE_DES_LEMMES.md` | 336223ac | 20933 | lu intégralement |
| L | `conway99-c1:origin/codex/c1-arithmetic-audit:AGENTS.md` | 13922f7c | 2197 | lu intégralement |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_biplane243_2026-10-07/OUTPUT.txt` | c833a4b4 | 1248 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_biplane243_2026-10-07/README.md` | 42be6f6f | 4379 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/NOTE.md` | db092f4b | 79549 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex:origin/lab/theta-lp-2026-10-08:code/lab_theta_lp_2026-10-08/NOTE.md` | c07012e0 | 363140 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_lp_penalty9.txt` | 1054fa48 | 3168 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_theta3_margins_N24.txt` | fcf85480 | 1221 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_theta3_maxK3_N24.txt` | b419bfdf | 771 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_synthesis_20261014/lab_sources/NEW_GRAPHS_2026-10-13.md` | e896b52b | 3720 | copie d'une note LAB (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_synthesis_20261014/lab_sources/NOTE_S3.md` | cd537751 | 29444 | copie d'une note LAB (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_synthesis_20261014/lab_sources/NOTE_SPREADFREE.md` | 6cb3e45a | 38020 | copie d'une note LAB (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_synthesis_20261014/lab_sources/THEOREM_Z3_COVERS.md` | 2faa36f5 | 4837 | copie d'une note LAB (originaux : lots L06–L08) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_line_resonance_20261016/aws_v1_runs/ANALYSE_AWS_V1_2026-10-18.md` | d0fda059 | 2427 | analyse LAB parcourue (en-tête) |
| N | `conway99-c1:origin/codex/p3-n25-register:data/p3_n25_register/README.md` | 62feda20 | 4205 | README du registre P3/N25 (contenu repris dans RECHERCHE_ACTIVE_C1.md:L318-327) |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/245_CODEX_P3_N25_FORETS_ET_TRIANGLES_SORTANTS.md` | b22bde40 | 13428 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/246_CODEX_APPARIEMENTS_LOCAUX_P3_N25.md` | 70f34c47 | 7225 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/CERTIFICAT_COMPTES_4192_2026_10_18.txt` | 3e5cf4bf | 3753 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/CERTIFICAT_COMPTES_5128_2026_10_18.txt` | ae59a4ac | 6321 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/COMPTES_ET_REALISATION_8650_2026_10_18.txt` | 18126f74 | 4836 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/MOMENTS_VOISINS_SANS_GRAM_2026_10_18.txt` | 7664d4ec | 5005 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_COUVERTURES_HOFFMAN_2026_10_12.md` | 49f5974c | 29277 | en-tête et sections clés |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_HOFFMAN_ASYMETRIE_PAR_ECHANGES_2026_10_12.md` | 5bcf42fc | 10619 | en-tête et sections clés |
| P | `t20-codex/HANDOFF_2026-10-01.md` | 5402b167 | 89269 | en-tête ; T20_BOARD : lignes CDX |
| P | `2026-10-04/ce-qui-a-t-sauvegard-dossier/outputs/C2_COUPES_123_PREUVES_2026-10-04.txt` | af142356 | 13417 | en-tête |
| P | `2026-10-04/ce-qui-a-t-sauvegard-dossier/outputs/C2_REPRISE_CONSTRUCTIVE_2026-10-04.txt` | 69b8a005 | 9855 | en-tête |
| P | `2026-10-04/ce-qui-a-t-sauvegard-dossier/outputs/C2_VERROU_GLOBAL_ET_TRIANGLES_2026-10-04.txt` | ef73198e | 6577 | en-tête |
| P | `2026-10-04/ce-qui-a-t-sauvegard-dossier/outputs/C2_WAGNER_BORNE_9_SUR_7.txt` | 3a301610 | 22031 | en-tête |
| P | `2026-10-04/ce-qui-a-t-sauvegard-dossier/outputs/D_INTEGRALITE_PREUVE_DIRECTE_2026-10-04.txt` | 2685777d | 4539 | en-tête |
| P | `2026-10-04/ce-qui-a-t-sauvegard-dossier/outputs/LIRE_DOSSIER_COUPES_123.txt` | c58d9028 | 937 | en-tête |
| P | `2026-10-04/ce-qui-a-t-sauvegard-dossier/outputs/SECOND_AVIS_C2_2026-10-04.txt` | d60d7f9c | 15774 | en-tête |
| P | `2026-10-04/ce-qui-a-t-sauvegard-dossier/outputs/SYSTEMES_C1_C3_2026-10-04.txt` | 867b1f43 | 4764 | en-tête |
| N | `2026-10-04/ce-qui-a-t-sauvegard-dossier/outputs/systeme_matriciel.pdf` | 719477b2 | 73928 | point de reprise / source LaTeX / PDF compilé |
| N | `2026-10-04/ce-qui-a-t-sauvegard-dossier/outputs/systeme_matriciel.tex` | a3490ec7 | 2385 | point de reprise / source LaTeX / PDF compilé |
| N | `2026-10-04/ce-qui-a-t-sauvegard-dossier/work/CHECKPOINT.md` | a0625f03 | 5037 | point de reprise / source LaTeX / PDF compilé |
| P | `2026-10-04/ce-qui-a-t-sauvegard-dossier/work/FAILED_ATTEMPTS.md` | d7fe13c7 | 7049 | parcouru |
| P | `2026-10-04/ce-qui-a-t-sauvegard-dossier/work/RESULTS.md` | cc74dd67 | 10038 | parcouru |
| N | `2026-10-04/j-ai-un-travail-de-m2/a01_notes.txt` | ed3a0737 | 3642 | notes d'agent résumées dans research_progress.txt |
| N | `2026-10-04/j-ai-un-travail-de-m2/a02_notes.txt` | 48b943d5 | 7185 | notes d'agent résumées dans research_progress.txt |
| N | `2026-10-04/j-ai-un-travail-de-m2/a03_notes.txt` | f77827b6 | 2568 | notes d'agent résumées dans research_progress.txt |
| N | `2026-10-04/j-ai-un-travail-de-m2/a04_notes.txt` | 74e7bc05 | 5637 | notes d'agent résumées dans research_progress.txt |
| N | `2026-10-04/j-ai-un-travail-de-m2/a05_notes.txt` | 6b0e86b0 | 6365 | notes d'agent résumées dans research_progress.txt |
| N | `2026-10-04/j-ai-un-travail-de-m2/a07_notes.txt` | 5b38bfb2 | 4250 | notes d'agent résumées dans research_progress.txt |
| N | `2026-10-04/j-ai-un-travail-de-m2/a09_notes.txt` | 25a60587 | 5882 | notes d'agent résumées dans research_progress.txt |
| N | `2026-10-04/j-ai-un-travail-de-m2/a10_notes.txt` | 21cd858c | 7691 | notes d'agent résumées dans research_progress.txt |
| P | `2026-10-04/j-ai-un-travail-de-m2/research_brief.txt` | d774594c | 5325 | parcouru |
| P | `2026-10-04/j-ai-un-travail-de-m2/research_progress.txt` | ae27f99b | 5474 | parcouru |
| N | `2026-10-04/j-ai-un-travail-de-m2/wave1_updates.txt` | 633b0a2b | 1940 | point de reprise / source LaTeX / PDF compilé |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/PASSATION_CONWAY_C1_2026-10-06.txt` | a6a82eab | 71034 | §0, 1, 8, 17–20 lus |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/conway_elargissement_bilan.txt` | 00d42bf7 | 5739 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/conway_resultats_verifies.txt` | 2a738feb | 4311 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/fragment23_bilan.txt` | 6800c575 | 5717 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/fragment23_component_proportion_audit.txt` | 5856a27d | 3537 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/fragment23_two_neighbors_notes.txt` | e3801b34 | 2967 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_affine37_c1_repo_reuse.txt` | 21e48cf5 | 7802 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_affine37_local_transfer_bounds.txt` | 832f43a6 | 4513 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_affine37_m0_lock.txt` | be981f62 | 2442 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_affine37_positive_core.txt` | c3fa0457 | 2635 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_affine37_seven_mark_cut.txt` | 83143fc1 | 1483 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_affine37_short_paths.txt` | 27fd398b | 14914 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_affine37_transfer_focus.txt` | d4446b74 | 5941 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_affine_level2_exclusion.txt` | 15b9d85e | 2456 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_continuation_20261006.txt` | cec3c180 | 4039 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_continuation_20261006_second.txt` | d527280d | 1806 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_edge_families_audit.txt` | 97dde813 | 5484 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_edge_families_proof.txt` | 14254392 | 4028 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_marked_lattice48.txt` | afd0e84c | 7422 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_marked_lattice56.txt` | 0a7e0c0e | 4980 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm16_catalogue_proof.txt` | de3fb588 | 5968 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm16_zero_structure.txt` | 7df5f5a8 | 4295 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm18_sparse_structure.txt` | 88badb90 | 4494 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm18_star_complement.txt` | 3c727e0f | 4975 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm18_structure.txt` | 5b7fc6b6 | 4448 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm18_triple_sparse_structure.txt` | 91eac40a | 3281 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm20_matching.txt` | d62e4490 | 3065 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm26_affine37_links.txt` | a3741ba2 | 4856 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm26_five_structure.txt` | 4ad56e20 | 3367 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm26_independent_global.txt` | 1ca9b114 | 2674 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm26_plane_global_constraints.txt` | a57d1af0 | 2901 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm26_sign_structure.txt` | 2215bca9 | 5680 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_norm26_zero_affine.txt` | f1d7a07b | 3953 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_prismless_obstruction.txt` | acdae270 | 15965 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_resolution_checkpoint.txt` | 027f0ac8 | 3526 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_resolution_restart.txt` | d8089c94 | 8425 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_shadow46.txt` | edffa4db | 6720 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_short_shell_bijections.txt` | c4335814 | 4526 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_short_shell_links.txt` | 679fee88 | 4239 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_short_spectra_audit.txt` | e3e9b173 | 13452 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_star_domains_d6_moments.txt` | b177ad92 | 6872 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_star_domains_proof.txt` | eeaf0a94 | 7907 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_triangle_geometry.txt` | a1b060b0 | 7537 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_two_forced_shells.txt` | b040150c | 3778 | en-tête (L1–~15) |
| P | `2026-10-05/salut-j-aimerais-que-tu-regardes/global_two_stars_rigidity.txt` | 73ee6bd3 | 8859 | en-tête (L1–~15) |
| N | `2026-10-05/salut-j-aimerais-que-tu-regardes/source_c1_foundations.txt` | 345b1a35 | 6632 | copie d'une note C1 (originaux lot L09) |
| N | `2026-10-05/salut-j-aimerais-que-tu-regardes/source_c1_mod7_bound.txt` | f353ef3c | 6592 | copie d'une note C1 (originaux lot L09) |
| N | `2026-10-05/salut-j-aimerais-que-tu-regardes/source_c1_triangle_schur.txt` | 961392aa | 7555 | copie d'une note C1 (originaux lot L09) |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:PASSATION_C1_2026-10-07.md` | e3bb54c9 | 3860 | en-tête lu (session Claude cloud, pas Codex) |
| P | `c1-codex/JOURNAL.md` | ea5d2689 | 64472 | début et recherche « Codex/Astra » (journal de la session C1, pas Codex) |
| P | `c1-codex/PASSATION_C1_2026-10-07.md` | 93359564 | 3897 | en-tête lu (session Claude cloud, pas Codex) |
| N | `c1-codex/code/lab_biplane243_2026-10-07/OUTPUT.txt` | 625773e5 | 1271 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_biplane243_2026-10-07/README.md` | 72739a93 | 4439 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/notes/100_SYNTHESE_DES_LEMMES.md` | bb5e31b7 | 20075 | version antérieure de la note 100 (sans la correction du 15/10) ; note C1 |
| P | `c1-main-codex/PASSATION_C1_2026-10-07.md` | e4078700 | 3909 | en-tête lu (session Claude cloud, pas Codex) |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/165_CODEX_NORM14_RANK33.md` | 1351a5e1 | 12464 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/166_CODEX_NORM16_CINQ_COEURS.md` | 6ae665df | 7658 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `t20-codex/lemma/PROOF_C2/B_LATTICES.md` | 57334b6e | 18531 | en-tête ; T20_BOARD : lignes CDX |
| N | `t20-codex/lemma/PROOF_C2/B_TABLE_156.md` | 649f2787 | 105200 | table générée (C2, LAB) |
| N | `t20-codex/lemma/PROOF_C2/paper/table156.tex` | c80e04fa | 10259 | table générée (C2, LAB) |
| P | `t20-codex/lemma/T20_BOARD.md` | a8763905 | 16798 | en-tête ; T20_BOARD : lignes CDX |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/NOTE.md` | cad1051c | 80511 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_N84.txt` | 840cadd3 | 8391 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_census9_types_bvls243.txt` | 716e5691 | 2314 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_census9_types_twin243.txt` | 4554e98d | 2912 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_census_check_bvls243.txt` | caed089c | 1719 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_census_check_twin243.txt` | f547cd74 | 1736 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_ext2_N84.txt` | d71ba124 | 2482 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_ext3_N84.txt` | f3ebe1f7 | 2328 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_lp_penalty9.txt` | d825fbac | 3182 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_quartic_N30.txt` | 67b3b814 | 1613 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_seven_one.txt` | bf674086 | 753 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_six_three.txt` | 9269b758 | 1572 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_six_three_730.txt` | 149e7ff4 | 332 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_sixsets.txt` | d27ad734 | 3508 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_testbeds.txt` | 3858fb78 | 1110 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_theta3_margins_N24.txt` | f325be93 | 1241 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-codex/code/lab_theta_lp_2026-10-08/OUTPUT_theta3_maxK3_N24.txt` | 56012b3f | 783 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_theta_lp_2026-10-08/NOTE.md` | af07a02e | 377887 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_theta_lp_2026-10-08/OUTPUT_census_cong.txt` | 7a77e0e1 | 381 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_theta_lp_2026-10-08/OUTPUT_coupled_collisions_P0.txt` | 861c1919 | 1979 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_theta_lp_2026-10-08/balls/radial_exact_cyclic241_t2_sample.txt` | c6d1927b | 676 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_theta_lp_2026-10-08/imports_2026-10-09_convergences/DOSSIER_C1_INTEGRE.md` | 683b9cfc | 52844 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_theta_lp_2026-10-08/lap_sweep48/README.md` | ec5c155c | 3625 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_theta_lp_2026-10-08/lap_sweep48/sweep_48_torsion.txt` | 2766c71d | 231232 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_N84.txt` | c21a3095 | 8331 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_abundance3_N84.txt` | 2e8b1254 | 868 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_abundance_N84.txt` | 376eb8ff | 1149 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_bfroma_N40.txt` | 31a7cd8d | 3363 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_caps16_N84.txt` | 5bb19540 | 887 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_caps16b_N84.txt` | cd67a1ff | 712 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_caps18_N84.txt` | 682e1296 | 1689 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_ceiling37_N84.txt` | 01441031 | 4109 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_ceiling37_lap_N84.txt` | a3ebf0b9 | 837 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_census2_99_order10.txt` | 0eee7aca | 1345 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_census2_99_order9.txt` | 50c3e6a3 | 1220 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_census9_measure_bvls243.txt` | ad96acc6 | 5414 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_census9_measure_twin243.txt` | ac683a32 | 6046 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_census9_types_bvls243.txt` | 09ead6bb | 2293 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_census9_types_twin243.txt` | 1b889d29 | 2891 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_census_check_bvls243.txt` | a5038652 | 1698 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_census_check_twin243.txt` | 51acc6be | 1715 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_cert35_N84.txt` | 9fd839ea | 298 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_compare_census_99.txt` | b4617254 | 420 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_coupled_N84.txt` | c46f1660 | 1167 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_degenerate9.txt` | 6c2bde84 | 663 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_ext2_N84.txt` | 3d6cd8e1 | 2464 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_ext3_N84.txt` | be6e6850 | 2311 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_fano_census.txt` | 52268b78 | 267 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_fanocap2_N84.txt` | d018a15c | 1285 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_fanocap3_N84.txt` | 8887c6ae | 1017 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_fanocap_N84.txt` | 84d29da6 | 616 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_five_five.txt` | 1a9ea49f | 494 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_frontier37_N84.txt` | 4f71aaab | 752 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_identity_N40.txt` | 54447f15 | 508 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_ladder_N84.txt` | 738ce701 | 1550 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_lp_caps10.txt` | e54da1f1 | 718 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_lp_caps9.txt` | be9dd3f2 | 1546 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_lp_clean9.txt` | abaca54b | 1202 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_lp_order10.txt` | d0483f85 | 455 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_lp_penalty10.txt` | 31613898 | 1688 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_lp_pertype9.txt` | 38d2a3d8 | 2099 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_lp_reps10_coupled.txt` | f3419dd3 | 364 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_margins_N84.txt` | b75da863 | 2524 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_needs37_N84.txt` | 6a753e95 | 1069 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_norm16_census.txt` | 4c86278b | 978 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_quartic_N30.txt` | e2f5be7f | 1602 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_quartic_ladder_N30.txt` | c5f7c5dc | 886 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_r35_N84.txt` | d870fb8a | 2065 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_reps10.txt` | b3bbb8ee | 3155 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_roots88_N84.txt` | 46512783 | 575 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_scenarios_N84.txt` | e8e3850a | 1571 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_seven_one.txt` | aff13b95 | 741 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_six_three.txt` | 3fa75d85 | 1539 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_six_three_730.txt` | 523240fd | 328 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_sixsets.txt` | b9b90078 | 3467 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_testbeds.txt` | 5161d5ed | 1091 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_theta3_caps_N24.txt` | 9c087edb | 212 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_theta3_ladder_N26.txt` | 12a8642a | 610 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_theta3_maxG_N24.txt` | d4a1d867 | 457 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_theta_pi_N60.txt` | 72ac4aee | 1555 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_threshold33_N84.txt` | cbb860b9 | 864 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_top43_N84.txt` | f92ddc12 | 821 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_top_others_N84.txt` | aa462e9c | 3051 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_tradeoff33_N84.txt` | 32d79463 | 714 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/OUTPUT_tradeoff35_N84.txt` | 96753c78 | 383 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/certificates2_N84_check.txt` | bd8aea1d | 1129 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:code/lab_theta_lp_2026-10-08/certificates_N84_check.txt` | 2068d4d1 | 2002 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/167_CODEX_LEVEL7_THETA_AUDIT.md` | 02891fbc | 9680 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/168_CODEX_THETA_RANG33_MIN26.md` | c8e38328 | 13012 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/169_CODEX_NORM16_ATTACHES_RANG.md` | 189b4102 | 8314 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/170_CODEX_NORM16_SEED4_FANO_RANG33.md` | fa3a26f5 | 13532 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/171_CODEX_NORM18_BUDGET_GRAINES.md` | 09e493a8 | 4438 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/172_CODEX_RANG35_DUAL_PAW_CYCLE.md` | 7866cb8a | 11339 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/173_CODEX_GRAINES_UNIQUES_NORMES14_16.md` | 31f8ae76 | 9079 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/174_CODEX_RESEAU60_COTE_PLUS3.md` | c84a4429 | 12352 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/175_CODEX_RECOLLEMENT_PETITES_NORMES.md` | 1ab23342 | 12014 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/176_CODEX_GEOMETRIE_NORMES18_20.md` | 2bdd53be | 15350 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/177_CODEX_RANG43_CLASSES_COURTES.md` | ea8810a0 | 13715 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-codex:origin/codex/c1-arithmetic-audit:notes/177_CODEX_RANG43_CLASSES_COURTES.md` | bb13a190 | 8348 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/178_CODEX_CLASSES_FRACTIONNAIRES_22_26.md` | 9b0a9266 | 3300 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/179_CODEX_RANG35_GRILLES_ET_JUMEAUX.md` | b91f2182 | 14271 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/180_CODEX_EXCLUSION_RANG35_PACKING_FANO.md` | 7e198457 | 7023 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/181_CODEX_SEPT_SOMMETS_COLLISIONS_RANG37.md` | a75dad7d | 11264 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/182_CODEX_RECENSEMENTS_HUIT_NEUF_SOMMETS.md` | cab5d877 | 9076 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/183_CODEX_COLLISIONS_MASSE_HUIT.md` | 8fe4de95 | 9172 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/184_CODEX_RECENSEMENT_PARAMETRE_TESTS_REELS.md` | 80b5eaeb | 6633 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/185_CODEX_FAMILLE_44_AUDIT_COMPLET.md` | 159ca74e | 11351 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/186_CODEX_TRIANGLES_LOINTAINS_MULTIPLICITES.md` | 4745e857 | 4836 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/187_CODEX_ORDRE_DIX_RECENSEMENT_CIBLE.md` | c7268569 | 7658 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/188_CODEX_COLLISIONS_63_MASSES_SIX_SEPT.md` | c07892db | 11134 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/189_CODEX_FANO_842_ORDRE10.md` | 2c2d7598 | 5471 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/190_CODEX_PRISME_MAISON_ORDRE11.md` | aade2577 | 4049 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/191_CODEX_RANG43_NORME4_PROFILS28.md` | e2644262 | 10551 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/192_CODEX_COCLIQUES_RACINES44_NORME4_968.md` | f68b81e0 | 9433 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/193_CODEX_F0_TRIANGLE_LIBRE_COLLISIONS.md` | d53306f7 | 12527 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/194_CODEX_CLASSES_GRILLES_TAU1534.md` | bafe6d5b | 11292 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/195_CODEX_COLLISIONS_PAIRES_GRILLES.md` | 75f0e153 | 10343 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/196_CODEX_MOMENTS_VOISINAGES_TAU1403.md` | de5a6c0e | 9392 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/197_CODEX_COLLISIONS_FAISCEAUX_GRILLES.md` | 2b0ef1df | 9624 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/198_CODEX_MOMENTS_DEGRES_ET_CANAL90.md` | 6f36cf39 | 9448 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/199_CODEX_COUPLAGE_FANO_GRILLES.md` | 479865d1 | 6812 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/200_CODEX_SANS_PRISME_ET_REPRESENTANTS_COURTS.md` | 4f02757c | 10537 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/201_CODEX_FENTES_ET_DROITE_DANS_SIX_GRILLES.md` | 18b30100 | 5200 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/202_CODEX_RANG7_GRILLES_ET_HUBS_REPETES.md` | ad320cfd | 7927 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/203_CODEX_EXCLUSION_GENERALE_221_ET_COUPURE_GLOBALE.md` | 7286edd4 | 8762 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/204_CODEX_COUPURE_DENSE_BORNES_GLOBALES.md` | 10f73f0a | 7193 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/205_CODEX_DEUX_APICES_DENSES_ET_DISCRIMINANT.md` | aabdec07 | 10049 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/206_CODEX_RELATIONS_LOCALES_ET_RANG43.md` | 3f340493 | 10363 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/207_CODEX_AUDIT_ETOILES_GENERIQUES.md` | da897fd7 | 7062 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/208_CODEX_ESPACE_LOCAL_DES_COMPOSANTES.md` | d5629a1e | 8158 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/209_CODEX_COUPLAGE_DEUX_ETOILES.md` | d3eaecb5 | 7354 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/210_CODEX_AUDIT_RESIDU_66.md` | 34b5537f | 7387 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/211_CODEX_MODELE_DEUX_ETOILES.md` | c907b105 | 4430 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/212_CODEX_CERTIFICATS_DEUX_ETOILES.md` | 82a8243d | 8170 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/213_CODEX_POTENTIELS_DEUX_ETOILES.md` | 85114e8e | 6356 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/214_CODEX_ABLATION_EXACTE_COMPATIBILITES.md` | b2dc9ea4 | 8297 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/215_CODEX_PROJECTEUR_REEL_ET_MINEURS_TROIS.md` | 12c66956 | 8776 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/216_CODEX_AUDIT_CHOIX_UNIQUE_ET_PROPAGATION.md` | 83cb5b37 | 8791 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/217_CODEX_DISCRIMINANT_DU_PROJECTEUR_LOINTAIN.md` | 6d13c652 | 5914 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/218_CODEX_MOTIF_FORCE_COORDONNEES_UNITAIRES.md` | 4b03e826 | 9756 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/219_CODEX_COMPLETION_ABSTRAITE_GRAM_ETOILE.md` | ad120aa0 | 9871 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:AGENTS.md` | 171ae69a | 103466 | version antérieure du journal Codex (sous-ensemble de la version du 19/10 lue) |
| N | `c1-codex:origin/main:AGENTS.md` | 8ed3bd07 | 136094 | version antérieure du journal Codex (sous-ensemble de la version du 19/10 lue) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:CLAUDE.md` | 57887247 | 554 | consignes de poste/session, sans résultat |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:RECHERCHE_ACTIVE_C1.md` | fa7024e6 | 56210 | version antérieure du même journal (contenu repris dans la version lue) |
| N | `c1-codex:origin/codex/c1-arithmetic-audit:RECHERCHE_ACTIVE_C1.md` | 3dbf3170 | 15496 | version antérieure du même journal (contenu repris dans la version lue) |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:RECHERCHE_A_REDUCTION_STRUCTURELLE.md` | 19be1f91 | 10945 | parcouru (L1–80, titres) |
| N | `c1-codex/LAB_INSTRUCTIONS_C1.md` | dfd98599 | 4722 | consignes de poste/session, sans résultat |
| N | `c1-main-codex/code/lab_cost37_2026-10-09/COUT_RANG37.md` | 6151c6f1 | 8791 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_cost37_2026-10-09/OUTPUT_fano37_pilot_seed2.txt` | 6f85a162 | 1045 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_cost37_2026-10-09/OUTPUT_star37e_anatomy_seed2026_all.txt` | 25716e12 | 3773 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_cost37_2026-10-09/OUTPUT_star37f_gain_seed41_all.txt` | 39ce4104 | 5975 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_cost37_2026-10-09/OUTPUT_star37f_green_only.txt` | 26f3a0d8 | 495 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_cost37_2026-10-09/OUTPUT_star37f_patterns_seed2026_all.txt` | fe5edc30 | 353 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_index_2026-10-09/NOTE_RESEAUX_DE_DROITE.md` | 42f07772 | 4696 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/220_CODEX_ROUTES_HORS_RANGS.md` | 223a8758 | 9792 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/221_CODEX_NOYAU_PRISME_DEFECTUEUX.md` | 0beda42c | 9012 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/222_CODEX_PROLONGEMENT_PRISME_MASQUES.md` | a515b5d6 | 6704 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/223_CODEX_LIMITE_DES_PREMIERS_PROLONGEMENTS.md` | 2dee43da | 6323 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/224_CODEX_AUDIT_LAP_RANG37_MAILLE5.md` | faa59dcf | 11269 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/225_CODEX_NOYAUX_COMPOSANTES_ET_GRILLES.md` | 220194dd | 7145 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/226_CODEX_MASSES789_SANS_PRISME.md` | 3527fd87 | 11410 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/227_CODEX_C8_SANS_DOUBLES_MOULINS.md` | a3816859 | 4784 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/228_CODEX_MOULIN_CUBIQUE_NOYAU17.md` | d1523af8 | 6370 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/229_CODEX_PARTENAIRES_ET_ANTIVOISINAGES.md` | 008f9d21 | 9811 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/230_CODEX_COMPLETION_BINAIRE_SEUIL240.md` | 9eeba76e | 10011 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/231_CODEX_SIGNE_RESIDUEL_ET_TRACES.md` | 27955e0d | 6728 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/232_CODEX_RIGIDITE_BINAIRE_LAPLACIEN.md` | 06bcd16d | 6693 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/233_CODEX_DIFFERENCE_RANG4_IMPOSSIBLE.md` | 96623197 | 12459 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/234_CODEX_CONNEXITE_MURS_OPPOSES.md` | 408ded43 | 6703 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/235_CODEX_EXPLOITATION_CONVERGENCES.md` | 429648df | 10259 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/236_CODEX_CONVERGENCES_ARETES_PARTAGEES.md` | 7b89bb89 | 8083 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/237_CODEX_RUBANS_REPARES_PAR_CENTRES.md` | ae8b4a7a | 6831 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/238_CODEX_FENETRES_TRANSPORT_ET_DENSITE.md` | c0fa831c | 11456 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/239_CODEX_RUBAN_SIX_CORDES_EN_ETOILE.md` | 1651bbd9 | 6911 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/240_CODEX_CORDES_DISJOINTES_OU_TRIANGLE_DE_CENTRES.md` | 3f3668e7 | 7243 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/241_CODEX_ENTREES_CUBIQUES_THETA_IMPAIRE.md` | a3aab43e | 10121 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/242_CODEX_MOMENTS_QUADRATIQUES_ET_RACINES.md` | 622af9ac | 9121 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/243_CODEX_CONTACTS_NORME26_ET_TRIANGLES_IMPAIRS.md` | f326535c | 4588 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/244_CODEX_FANTOMES_ET_CIBLE_INDEPENDANTE_UNIFORME.md` | 05336adc | 11164 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/247_CODEX_HERMITE_ET_RESEAUX_LOINTAINS.md` | 8ef6381e | 5233 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/248_CODEX_CAPACITE_TRIANGULAIRE_DES_BLOCS.md` | 05420aee | 3908 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/249_CODEX_TROIS_PRISMES_HORS_GRILLE.md` | 7d009409 | 7853 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/250_CODEX_PARABOLE_ET_AJOUT_D_UN_SOMMET.md` | a4548e8c | 5615 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| N | `c1-codex/data/codex_norm16_dz_five_types.instance.txt` | b60c4941 | 92243 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_dz_instance_0_0_2.txt` | 5a75384d | 2379 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_dz_solutions_0_0_2.txt` | b4b5344c | 57120 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_dz_spectral_case0_orbit0.instance.txt` | 4629e2ab | 92242 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_dz_spectral_case0_orbit0.schur.txt` | 5af26e8d | 906 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_edge_catalogue_0_3/instance.txt` | a1917bb7 | 287 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_edge_catalogue_0_3/schur.txt` | 6dc55bdf | 1244 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_edge_catalogue_0_4/instance.txt` | f0aa285e | 287 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_edge_catalogue_0_4/schur.txt` | dc8fabf7 | 1244 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_edge_catalogue_0_4_refined/instance.txt` | 8b0e344c | 1631 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_edge_catalogue_0_4_refined/schur.txt` | 657e9342 | 1248 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_edge_first/instance.txt` | 43cfb85c | 287 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_edge_first/schur.txt` | ef8aacde | 1252 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_even_core_full/instance.txt` | df3e46ba | 92243 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_even_core_full/rows.txt` | 1bb7d57f | 826340 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_even_core_full/schur.txt` | 0952eed9 | 692 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_even_core_other_probe/instance.txt` | cc59aac3 | 92242 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_even_core_other_probe/schur.txt` | c05ca82f | 830 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_even_core_probe/instance.txt` | 2392473e | 92243 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_even_core_probe/schur.txt` | 67eee2bb | 692 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_independent_catalogue/instance.txt` | 25f59c98 | 2380 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_independent_catalogue/rows.txt` | f166e0c0 | 617773 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_independent_catalogue/schur.txt` | e5178717 | 1234 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_independent_counts/instance.txt` | 82729aa5 | 4688 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_independent_counts/schur.txt` | 42d8b3ea | 1146 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_schur_0_0_2.txt` | 0eefaef3 | 1291 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_tight_cut_first/instance.txt` | 8f076ab3 | 92243 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_tight_cut_first/rows.txt` | 9b49204f | 2377469 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-codex/data/codex_norm16_tight_cut_first/schur.txt` | 9368b869 | 696 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:data/codex_norm16_dz_instance_0_0_2.txt` | 9f11e4e5 | 2280 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:data/codex_norm16_dz_solutions_0_0_2.txt` | 124d69c4 | 55424 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `conway99-c1:origin/codex/c1-arithmetic-audit:data/codex_norm16_schur_0_0_2.txt` | 51e05f18 | 1271 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/251_CODEX_NORM16_FORET_LOINTAINE.md` | 8770690e | 8481 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/252_CODEX_PREMIER_CADRE_NORM16.md` | 0ab9c9d4 | 5764 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/253_CODEX_NORM16_SOMMET_LOINTAIN_ISOLE.md` | 4a83406b | 9011 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/254_CODEX_CADRE35_ET_SCHUR_NORM16.md` | 712d0fa5 | 9315 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/255_CODEX_NORM16_PAIRE_OMISE.md` | f14ac6f6 | 7326 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/256_CODEX_NORM16_OMBRES_PAIRES.md` | 64e9bfc3 | 6175 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/257_CODEX_NORM16_CONNEXITE_DES_OMBRES.md` | 397777c9 | 7779 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/258_CODEX_COUPURES_ET_OBSTRUCTION_DE_BORD.md` | ce026f62 | 6158 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/259_CODEX_DEUX_CHEMINS_DE_TRANSPORT_NORM16.md` | b0d0450f | 6586 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `conway99-c1:origin/codex/c1-arithmetic-audit:notes/260_CODEX_P4_DOUBLE_OMIS_ET_BORD_SURVIVANT.md` | d62b6d9c | 5702 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| N | `c1-main-codex/dossiers_externes/HOFFMAN_UPDATE_20261011/CERTIFICATION.md` | 20632798 | 3611 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| N | `c1-main-codex/dossiers_externes/HOFFMAN_UPDATE_20261011/COORDINATION.md` | 4fade3b3 | 2445 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| N | `c1-main-codex/dossiers_externes/HOFFMAN_UPDATE_20261011/COUVERTURE.md` | f1fdba6c | 7145 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| N | `c1-main-codex/dossiers_externes/HOFFMAN_UPDATE_20261011/FAILURE_LEDGER_ADDITIONS.md` | c3953fc8 | 2324 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| P | `c1-main-codex/dossiers_externes/HOFFMAN_UPDATE_20261011/README.md` | 01ae73ea | 3951 | en-tête (dossier ChatGPT) |
| P | `c1-main-codex/dossiers_externes/HOFFMAN_UPDATE_20261011/RESULTATS.md` | aa94fb2b | 7512 | en-tête (dossier ChatGPT) |
| N | `c1-main-codex/dossiers_externes/HOFFMAN_UPDATE_20261011/THEORIE.md` | 37ddae05 | 8914 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| P | `c1-main-codex/research/astra_bvls_boundary_20261011/COORDINATION.md` | abb18767 | 1627 | en-tête |
| P | `conway99-c1:origin/codex/asymmetry-audit-20261012:notes/172_RESEAU_Q_ALPHA22.md` | b01d9546 | 7402 | en-tête et sections clés |
| N | `c1-main-codex/code/lab_coheawood_2026-10-12/OUTPUT_n18dfs_core23_slice0.txt` | b752b19d | 390 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_coheawood_2026-10-12/cores18/core_23.txt` | 3020e6fe | 99 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_s3_question_2026-10-12/NOTE_S3.md` | 8806053e | 29787 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_spreadfree_243_2026-10-12/NEW_GRAPHS_2026-10-13.md` | 4eafaa8f | 3762 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_spreadfree_243_2026-10-12/NOTE_SPREADFREE.md` | ce47ff6c | 38501 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_coclique_defects/regular_completion_v13/codex_20261013_v13_regular_completion.txt` | 72874b3a | 2625 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| N | `conway99-c1:origin/codex/asymmetry-audit-20261012:data/codex_hoffman_boundary_audit_20261012/boundary.txt` | d0f3dbb6 | 3156 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| P | `conway99-c1:origin/codex/asymmetry-audit-20261012:notes/AUDIT_CODEX_ASYMETRIE_2026_10_12.md` | 2ce073e8 | 19920 | en-tête et sections clés |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md` | 76cc797f | 186693 | premières lignes des 79 sections |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOTE_COHEAWOOD_DEUX_COCLIQUES.md` | 89b41cf3 | 15204 | en-tête et sections clés |
| P | `conway99-c1:origin/codex/asymmetry-audit-20261012:notes/NOTE_RELEVEMENT_S3_QUADRATIQUE.md` | 766eabdd | 7913 | en-tête et sections clés |
| N | `c1-main-codex/code/lab_c1_coclique_frame_2026-10-13/NOTE_COCLIQUE_FRAME.md` | a985673a | 5783 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_c1_triangles_2026-10-13/NOTE_TRIANGLES.md` | b1e29260 | 5504 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_coclique_defects/partition_v10/aws_pilot/results/auto-stop.txt` | 50c611d4 | 248 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_coclique_defects/partition_v10/aws_pilot/results/host.txt` | 393741b0 | 3679 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_coclique_defects/partition_v10/aws_pilot/results/packages.txt` | 0c55cd67 | 194 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_coclique_defects/rank_two_rigidity_v14/codex_20261013_v14_rank_two_rigidity.txt` | 0da065d4 | 2759 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| N | `c1-main-codex/code/lab_asym_paley_2026-10-14/CONWAY_CONSTRAINTS.md` | fbe2b779 | 20548 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_asym_paley_2026-10-14/NOVELTY_CHECK.md` | be32e116 | 4160 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_asym_window_2026-10-14/NOTE_ASYM_WINDOW.md` | f3614698 | 13266 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_c1_night_2026-10-14/NOTE_NIGHT.md` | d755b819 | 58122 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_c1_night_2026-10-14/theta7_cert_log2.txt` | 67002e1c | 3011 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_lambda1_construction_2026-10-14/SB_NOVELTY_CHECK.md` | 27e331a3 | 3304 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_lambda1_construction_2026-10-14/SOLVER_CAMPAIGN_STATE.md` | f9d07cab | 6525 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_stars_rank_2026-10-14/AUDIT_EXCLUSIONS_2026-10-15.md` | c94756c1 | 42705 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_stars_rank_2026-10-14/N9NG_ATTACK_2026-10-15.md` | 84ba8fd6 | 12939 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_stars_rank_2026-10-14/NOTE_PROOFS_1410.md` | adf22bf3 | 50120 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_stars_rank_2026-10-14/NOTE_STARS_RANK.md` | 9fa0b200 | 8941 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_stars_rank_2026-10-14/REVUE_GLOBALE_2026-10-16.md` | 7dfb85a5 | 29739 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_stars_rank_2026-10-14/hmatch_tools_2026-10-15/oddonly_walks/README.txt` | e2e67f32 | 730 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| P | `c1-main-codex/data/codex_asymmetry_mechanisms_20261014/bridge_circuits.txt` | f4445b0e | 1870 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_asymmetry_mechanisms_20261014/bridge_completion_theory.txt` | af540af7 | 2370 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_asymmetry_mechanisms_20261014/bridge_flip_orbit_filter.txt` | ea962008 | 1535 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_asymmetry_mechanisms_20261014/bridge_host_lemma.txt` | 3e6a530a | 1003 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_asymmetry_mechanisms_20261014/bridge_majority_flips.txt` | 4cf2a567 | 1518 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_asymmetry_mechanisms_20261014/bridge_scope_684.txt` | 9534fded | 1151 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_asymmetry_mechanisms_20261014/bridge_status_679.txt` | beee94a9 | 1002 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_asymmetry_mechanisms_20261014/bridge_target_682.txt` | e9c2fa70 | 605 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_asymmetry_mechanisms_20261014/bridge_transport.txt` | e8727356 | 1793 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| N | `c1-main-codex/data/codex_asymmetry_synthesis_20261014/paley_sources/RESULTATS.md` | 685509e4 | 11939 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-main-codex/data/codex_asymmetry_synthesis_20261014/paley_sources/THEORIE.md` | 4480c5c9 | 8323 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| P | `c1-main-codex/data/codex_lambda_one_construction_20261014/bridge_378_incremental.txt` | 6b5c55b2 | 1266 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_lambda_one_construction_20261014/bridge_construct_now.txt` | f67fba82 | 1253 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_lambda_one_construction_20261014/bridge_followup.txt` | 500f55b2 | 2118 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_lambda_one_construction_20261014/bridge_incremental_progress.txt` | 79ad4748 | 2030 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_lambda_one_construction_20261014/bridge_lambda_one_scope.txt` | 8e5c543c | 1172 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_lambda_one_construction_20261014/bridge_payne9_obstruction.txt` | 71504bf6 | 1166 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_lambda_one_construction_20261014/bridge_payne9_progress.txt` | ab9233f7 | 1117 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_lambda_one_construction_20261014/bridge_request.txt` | 28c1048d | 3114 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_lambda_one_construction_20261014/bridge_two_researchers.txt` | 604210fd | 1388 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/bridge_ambient_upper_bound.txt` | c4629d25 | 1488 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/bridge_columns_and_degrees.txt` | 49aad9bd | 1701 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/bridge_fractional_witness.txt` | 57561289 | 1355 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/bridge_generator.txt` | b5f0260d | 1353 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/bridge_lab700_column_obstruction.txt` | 301f4266 | 877 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/bridge_rank31_mechanism.txt` | 37ffc300 | 590 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/bridge_rank31_switch.txt` | 08772404 | 1066 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/bridge_rank31_why.txt` | d94b7844 | 601 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/bridge_seed_batch_results.txt` | 86758797 | 1217 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/bridge_two_star_rank_formula.txt` | 021f1177 | 1558 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/bridge_v_columns_results.txt` | 6faa609d | 653 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/connected_repairs_720/bridge_new_transition.txt` | a23af22a | 1707 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/connected_repairs_720/bridge_scope_and_reflection.txt` | b33472e7 | 1894 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/connected_repairs_720/bridge_sos_status.txt` | 0140b6df | 1479 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| N | `c1-main-codex/data/codex_three_star_completion_20261014/lab700_z5_rank30_edges.txt` | 0f091a16 | 605 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `c1-main-codex/data/codex_three_star_completion_20261014/lab702_rank31_edges.txt` | b8e73505 | 596 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/lab713_batch/bridge_batch_verdict.txt` | c73b7829 | 1263 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/lab714_closed_cycle/bridge_z2b_verdict.txt` | 50a04d4e | 1212 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/lab726_decomposable/bridge_verdict.txt` | dcd2ee19 | 1396 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/prescribed_kernel_728/bridge_exact_verdict.txt` | b745cf76 | 650 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/prescribed_kernel_728/bridge_verdict.txt` | 425c530c | 1758 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `c1-main-codex/data/codex_three_star_completion_20261014/variable_kernel_731/bridge_verdict.txt` | 5a14943d | 2025 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_mechanisms_20261014/bridge_circuits.txt` | 1aaff493 | 1863 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_mechanisms_20261014/bridge_completion_theory.txt` | c105c239 | 2359 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_mechanisms_20261014/bridge_flip_orbit_filter.txt` | f86badbd | 1530 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_mechanisms_20261014/bridge_host_lemma.txt` | 2acf9088 | 1000 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_mechanisms_20261014/bridge_majority_flips.txt` | 27607dca | 1511 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_mechanisms_20261014/bridge_scope_684.txt` | cf011587 | 1147 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_mechanisms_20261014/bridge_status_679.txt` | 4cea3147 | 996 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_mechanisms_20261014/bridge_target_682.txt` | 7a23972d | 603 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_mechanisms_20261014/bridge_transport.txt` | 621731a0 | 1786 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_synthesis_20261014/literature/ihringer_2022_switching.pdf` | 75112b09 | 228797 | PDF de littérature externe |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_synthesis_20261014/literature/kaski_ostergard_2004_sts19.pdf` | c5b37ef9 | 282005 | PDF de littérature externe |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_synthesis_20261014/literature_expansion/babai_automorphism_handbook.pdf` | d44770cd | 796340 | PDF de littérature externe |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_synthesis_20261014/literature_expansion/brouwer_ihringer_kantor_4vertex.pdf` | b18369be | 627146 | PDF de littérature externe |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_synthesis_20261014/literature_expansion/coolsaet_degraer_spence_2006_45.pdf` | 6779b19c | 132086 | PDF de littérature externe |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_synthesis_20261014/literature_expansion/haemers_spence_2001_64.pdf` | 2beede4c | 142026 | PDF de littérature externe |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_asymmetry_synthesis_20261014/literature_expansion/maksimovic_rukavina_2022_twographs.pdf` | 1fd113c3 | 138498 | PDF de littérature externe |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_coclique_defects/rank_one_completion_v15/codex_20261014_v15_boundary43.txt` | 4b47895b | 3088 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_coclique_defects/rank_one_completion_v15/codex_20261014_v15_coheawood_dichotomy.txt` | 16b5f376 | 2016 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_lambda_one_construction_20261014/bridge_378_incremental.txt` | 23dcd597 | 1263 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_lambda_one_construction_20261014/bridge_construct_now.txt` | 236d9d15 | 1246 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_lambda_one_construction_20261014/bridge_followup.txt` | 86ac3174 | 2107 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_lambda_one_construction_20261014/bridge_incremental_progress.txt` | 57282f0d | 2019 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_lambda_one_construction_20261014/bridge_lambda_one_scope.txt` | cf9fa5d5 | 1167 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_lambda_one_construction_20261014/bridge_payne9_obstruction.txt` | f7e23f01 | 1163 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_lambda_one_construction_20261014/bridge_payne9_progress.txt` | c444cd47 | 1114 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_lambda_one_construction_20261014/bridge_request.txt` | 0954c5a5 | 3096 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_lambda_one_construction_20261014/bridge_two_researchers.txt` | 3d0612c7 | 1383 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_lambda_one_construction_20261014/payne9/geometry.txt` | 468c5da5 | 30874 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_local_global_20261015/global_star15_gray_proof_20261016.txt` | 7c8c8f4c | 6085 | non lu directement : contenu résumé dans AGENTS.md (L835-900) et dans le journal du 14/10 |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_night_20261014/four_root_edge_graph.txt` | d6e2c7b3 | 644 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/bridge_ambient_upper_bound.txt` | 79b1c25f | 1485 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/bridge_columns_and_degrees.txt` | e9c3bb99 | 1696 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/bridge_fractional_witness.txt` | 294d36ca | 1350 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/bridge_generator.txt` | 9c543e44 | 1350 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/bridge_lab700_column_obstruction.txt` | 427bc6d4 | 876 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/bridge_rank31_mechanism.txt` | f0eb9007 | 589 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/bridge_rank31_switch.txt` | 3f5e668e | 1064 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/bridge_rank31_why.txt` | 1d63d86a | 600 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/bridge_seed_batch_results.txt` | aaeb04e7 | 1214 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/bridge_two_star_rank_formula.txt` | a7f789bf | 1554 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/bridge_v_columns_results.txt` | f32f6a2a | 652 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/connected_repairs_720/bridge_new_transition.txt` | 9bc727ac | 1700 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/connected_repairs_720/bridge_scope_and_reflection.txt` | 659f44d2 | 1887 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/connected_repairs_720/bridge_sos_status.txt` | 3f2d27ef | 1474 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/lab700_z5_rank30_edges.txt` | 421d4aa0 | 604 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/lab702_rank31_edges.txt` | 0c7f007e | 595 | données brutes (instances, lignes, solutions, journaux d'exécution) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/lab713_batch/bridge_batch_verdict.txt` | 55a67adb | 1260 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/lab714_closed_cycle/bridge_z2b_verdict.txt` | eaf94034 | 1209 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/lab726_decomposable/bridge_verdict.txt` | 494b75f4 | 1391 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/prescribed_kernel_728/bridge_exact_verdict.txt` | 6a1ccbfb | 649 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/prescribed_kernel_728/bridge_verdict.txt` | d84b6bc0 | 1751 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_three_star_completion_20261014/variable_kernel_731/bridge_verdict.txt` | 9d68c63f | 2018 | premiers ~500 caractères (message Codex → LAB conservé dans data/) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/BORNE_ENERGIE_PAIRE_2026_10_16.txt` | b59c257d | 5673 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/COUPLAGE_VINGT_FIXES_2026_10_16.txt` | c6587c81 | 8748 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/JOURNAL_C1_NUIT_2026_10_14.md` | 1e7dca03 | 403354 | titres des 6824 lignes + revue LAB cw/review/09 (résumé secondaire, partiel) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/REDUCTION_RESONANCE_20_2026_10_16.txt` | 97dc0918 | 11935 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/REDUCTION_SYM6_10_2026_10_16.txt` | b214a98f | 9950 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/SECTEUR_SYMETRIQUE_BORD_2026_10_16.txt` | 7470690d | 9469 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/SYNTHESE_FAMILLE_ASYMETRIE_2026_10_16.txt` | 1bbdb64b | 28216 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| N | `c1-main-codex/data/codex_local_global_20261015/conway_global_cover_proof_20261016.txt` | 103a9e82 | 8145 | non lu directement : contenu résumé dans AGENTS.md (L835-900) et dans le journal du 14/10 |
| N | `c1-main-codex/data/codex_local_global_20261015/conway_global_psd_equivalence_20261016.txt` | 9321ebf1 | 3762 | non lu directement : contenu résumé dans AGENTS.md (L835-900) et dans le journal du 14/10 |
| N | `c1-main-codex/data/codex_local_global_20261015/global_star15_gray_proof_20261016.txt` | 4bdf6483 | 6195 | non lu directement : contenu résumé dans AGENTS.md (L835-900) et dans le journal du 14/10 |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_local_global_20261015/conway_global_cover_proof_20261016.txt` | 656096ac | 7996 | non lu directement : contenu résumé dans AGENTS.md (L835-900) et dans le journal du 14/10 |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_local_global_20261015/conway_global_psd_equivalence_20261016.txt` | 21e5104f | 3692 | non lu directement : contenu résumé dans AGENTS.md (L835-900) et dans le journal du 14/10 |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/PLAN_C_LE_3_2026-10-18.md` | 8c6bd45d | 5131 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/PROMPT_RECHERCHE_C1_c1_2026-10-17.md` | d46bdd72 | 36740 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| P | `c1-main-codex/code/lab_exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md` | 90d7384c | 20534 | passages sur les résultats de Codex (note LAB copiée) |
| P | `c1-main-codex/code/lab_exploration_2026-10-16/audit_2026-10-18/AUDIT_GLOBAL_2026-10-18_nuit.md` | 1d9cab90 | 7652 | passages sur les résultats de Codex (note LAB copiée) |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/audit_2026-10-18/AUDIT_RAPIDE_2026-10-18_soir.md` | cdb655c4 | 3021 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/c21_root_census/C21_ROOT_CENSUS_PARTIAL_2026-10-18.md` | 781880b0 | 2249 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/c3_cost_2026-10-18/C3_COST_PILOT_2026-10-18.md` | 17ecd43b | 6907 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/c3_cost_2026-10-18/C3_GRAM_COVER_2026-10-18.md` | 67a21613 | 16571 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/c3_cost_2026-10-18/pilot_results/gfm_local/RETRACTED.txt` | be79608d | 304 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/c3_hard_core_2026-10-18/MORTS_ET_SURVIVANTS_C3_2026-10-18.md` | 2587bb1e | 6570 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/c3_hard_core_2026-10-18/NUIT_2026-10-19.md` | d2de2797 | 25842 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/c3_hard_core_2026-10-18/PLAN_250_2026-10-19.md` | 089bb83d | 3190 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/c3_hard_core_2026-10-18/aws/SHA256_c3l2_c3p5.txt` | 7c2c6ddf | 336 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/c3_root_cover/C3_ROOT_COVER_2026-10-18.md` | 3a933f55 | 3599 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| N | `c1-main-codex/code/lab_exploration_2026-10-16/lemmas_c12_2026-10-18/LEMMES_C12_2026-10-18.md` | d268281e | 15992 | note ou sortie LAB copiée dans le dépôt de Codex (originaux : lots L06–L08) |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/MOMENTS_SIGNATURES_C1_2026_10_16.txt` | 5c395490 | 97659 | §1, §9, §19 et titres des 28 sections |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/QUOTIENT_COMPOSANTES_RACINE_2026_10_16.txt` | ac6e40a8 | 27937 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/REPRISE_COMPOSANTES_C1_2026_10_16.txt` | 6b6adc89 | 25614 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| N | `c1-main-codex/CLAUDE.md` | 75a85582 | 564 | consignes de poste/session, sans résultat |
| N | `c1-main-codex/LAB_INSTRUCTIONS_C1.md` | b234e7d3 | 4730 | consignes de poste/session, sans résultat |
| P | `c1-main-codex/README.md` | 87973fd5 | 9735 | parcouru (état C1 au 25/09) |
| L | `c1-main-codex/RECHERCHE_ACTIVE_C1.md` | efdf2fc9 | 57079 | lu intégralement (journal Codex 09–10/10) |
| P | `c1-main-codex/RECHERCHE_A_REDUCTION_STRUCTURELLE.md` | 1a89f392 | 11187 | parcouru (L1–80, titres) |
| P | `c1-main-codex/data/p3_n25_register/245_CODEX_P3_N25_FORETS_ET_TRIANGLES_SORTANTS.md` | 4fc92c77 | 13711 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/data/p3_n25_register/246_CODEX_APPARIEMENTS_LOCAUX_P3_N25.md` | fb440df4 | 7403 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| N | `c1-main-codex/data/p3_n25_register/README.md` | d58dce5a | 4308 | README du registre P3/N25 (contenu repris dans RECHERCHE_ACTIVE_C1.md:L318-327) |
| N | `c1-main-codex/dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/COORDINATION.md` | 29936dae | 2019 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| N | `c1-main-codex/dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/INTEGRATION.md` | de045821 | 1586 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| P | `c1-main-codex/dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/README.md` | 9879dbf6 | 2095 | en-tête (dossier ChatGPT) |
| N | `c1-main-codex/dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/REGISTRE_ECHECS.md` | 0a0b23ab | 2760 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| P | `c1-main-codex/dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/RESULTATS.md` | e5d50239 | 7796 | en-tête (dossier ChatGPT) |
| N | `c1-main-codex/dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/SOURCES.md` | c7e987b1 | 1573 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| N | `c1-main-codex/dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/THEORIE.md` | 258397af | 6535 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| N | `c1-main-codex/dossiers_externes/C1_K7_RESULTATS_PARTIELS/COORDINATION.md` | 74caffbd | 1983 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| P | `c1-main-codex/dossiers_externes/C1_K7_RESULTATS_PARTIELS/PREUVES.md` | f7cb62d1 | 14356 | en-tête (dossier ChatGPT) |
| P | `c1-main-codex/dossiers_externes/C1_K7_RESULTATS_PARTIELS/README.md` | 58b14e8d | 1505 | en-tête (dossier ChatGPT) |
| L | `c1-main-codex/dossiers_externes/INDEX.md` | 3dced861 | 4448 | lu intégralement |
| N | `c1-main-codex/dossiers_externes/PALEY_ASYMETRIE_DOSSIER/FAILURE_LEDGER.md` | b9c2e20b | 5393 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| N | `c1-main-codex/dossiers_externes/PALEY_ASYMETRIE_DOSSIER/MANIFEST_SHA256.txt` | ffe4df04 | 7632 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| P | `c1-main-codex/dossiers_externes/PALEY_ASYMETRIE_DOSSIER/README.md` | 640aae99 | 4373 | en-tête (dossier ChatGPT) |
| N | `c1-main-codex/dossiers_externes/PALEY_ASYMETRIE_DOSSIER/requirements.txt` | 40d5e14c | 149 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| N | `c1-main-codex/dossiers_externes/PALEY_ASYMETRIE_DOSSIER/resultats/closest_asymmetric.txt` | 8e4918b8 | 166 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| N | `c1-main-codex/dossiers_externes/PALEY_ASYMETRIE_DOSSIER/resultats/verification_recensement.txt` | 960f3975 | 306 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| N | `c1-main-codex/dossiers_externes/PALEY_ASYMETRIE_DOSSIER/resultats/verification_spectrale.txt` | 32894a87 | 200 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| N | `c1-main-codex/dossiers_externes/PALEY_ASYMETRIE_DOSSIER/resultats/verification_temoignage.txt` | 9e821cce | 368 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| N | `c1-main-codex/dossiers_externes/PALEY_ASYMETRIE_DOSSIER/sources/PROVENANCE.md` | 3c975bba | 4431 | annexe de dossier externe (coordination, sources, manifestes, sorties) |
| P | `c1-main-codex/notes/165_CODEX_NORM14_RANK33.md` | 962a7706 | 12660 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/166_CODEX_NORM16_CINQ_COEURS.md` | e6c86271 | 7792 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/167_CODEX_LEVEL7_THETA_AUDIT.md` | 2696217a | 9862 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/168_CODEX_THETA_RANG33_MIN26.md` | b79d4a46 | 13252 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/169_CODEX_NORM16_ATTACHES_RANG.md` | e821d44b | 8462 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/170_CODEX_NORM16_SEED4_FANO_RANG33.md` | a868719b | 13774 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/171_CODEX_NORM18_BUDGET_GRAINES.md` | 40b0a673 | 4517 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/172_CODEX_RANG35_DUAL_PAW_CYCLE.md` | 81bd9944 | 11553 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/172_RESEAU_Q_ALPHA22.md` | ae6ce677 | 7606 | en-tête et sections clés |
| P | `c1-main-codex/notes/173_CODEX_GRAINES_UNIQUES_NORMES14_16.md` | eb11f189 | 9239 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/174_CODEX_RESEAU60_COTE_PLUS3.md` | 9bec84d6 | 12599 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/175_CODEX_RECOLLEMENT_PETITES_NORMES.md` | bdc9d9ae | 12239 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/176_CODEX_GEOMETRIE_NORMES18_20.md` | 4a1f8ae5 | 15626 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/177_CODEX_RANG43_CLASSES_COURTES.md` | 4c5bf848 | 13989 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/178_CODEX_CLASSES_FRACTIONNAIRES_22_26.md` | e18eaba2 | 3372 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/179_CODEX_RANG35_GRILLES_ET_JUMEAUX.md` | d80bf896 | 14532 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/180_CODEX_EXCLUSION_RANG35_PACKING_FANO.md` | 2ecb33e9 | 7170 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/181_CODEX_SEPT_SOMMETS_COLLISIONS_RANG37.md` | 22f08c2b | 11476 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/182_CODEX_RECENSEMENTS_HUIT_NEUF_SOMMETS.md` | 1e4f0ab4 | 9273 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/183_CODEX_COLLISIONS_MASSE_HUIT.md` | c8a3e2e3 | 9353 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/184_CODEX_RECENSEMENT_PARAMETRE_TESTS_REELS.md` | fe8e61f9 | 6764 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/185_CODEX_FAMILLE_44_AUDIT_COMPLET.md` | 5dedcdd2 | 11578 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/186_CODEX_TRIANGLES_LOINTAINS_MULTIPLICITES.md` | 6826f345 | 4944 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/187_CODEX_ORDRE_DIX_RECENSEMENT_CIBLE.md` | d898cf2e | 7801 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/188_CODEX_COLLISIONS_63_MASSES_SIX_SEPT.md` | 10a2ed95 | 11367 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/189_CODEX_FANO_842_ORDRE10.md` | daccbf8e | 5606 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/190_CODEX_PRISME_MAISON_ORDRE11.md` | 1314b0c7 | 4141 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/191_CODEX_RANG43_NORME4_PROFILS28.md` | 11eef66b | 10804 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/192_CODEX_COCLIQUES_RACINES44_NORME4_968.md` | 1f8f9dae | 9688 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/193_CODEX_F0_TRIANGLE_LIBRE_COLLISIONS.md` | 159e8d6d | 12781 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/194_CODEX_CLASSES_GRILLES_TAU1534.md` | 85b3d2ea | 11543 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/195_CODEX_COLLISIONS_PAIRES_GRILLES.md` | a4cf019c | 10557 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/196_CODEX_MOMENTS_VOISINAGES_TAU1403.md` | ef398ebf | 9625 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/197_CODEX_COLLISIONS_FAISCEAUX_GRILLES.md` | 799b6d45 | 9829 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/198_CODEX_MOMENTS_DEGRES_ET_CANAL90.md` | 3c962ae4 | 9662 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/199_CODEX_COUPLAGE_FANO_GRILLES.md` | 33ca6cd7 | 6962 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/200_CODEX_SANS_PRISME_ET_REPRESENTANTS_COURTS.md` | 74bff3a7 | 10753 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/201_CODEX_FENTES_ET_DROITE_DANS_SIX_GRILLES.md` | 169a3d3a | 5315 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/202_CODEX_RANG7_GRILLES_ET_HUBS_REPETES.md` | b8239596 | 8107 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/203_CODEX_EXCLUSION_GENERALE_221_ET_COUPURE_GLOBALE.md` | 369e5dc7 | 8953 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/204_CODEX_COUPURE_DENSE_BORNES_GLOBALES.md` | 2c8e5be4 | 7367 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/205_CODEX_DEUX_APICES_DENSES_ET_DISCRIMINANT.md` | 015a2f67 | 10269 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/206_CODEX_RELATIONS_LOCALES_ET_RANG43.md` | 436cedd9 | 10597 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/207_CODEX_AUDIT_ETOILES_GENERIQUES.md` | aa046090 | 7211 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/208_CODEX_ESPACE_LOCAL_DES_COMPOSANTES.md` | 7b8482c7 | 8346 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/209_CODEX_COUPLAGE_DEUX_ETOILES.md` | 60868311 | 7537 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/210_CODEX_AUDIT_RESIDU_66.md` | aebca524 | 7539 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/211_CODEX_MODELE_DEUX_ETOILES.md` | 48484844 | 4521 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/212_CODEX_CERTIFICATS_DEUX_ETOILES.md` | 0feb5540 | 8345 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/213_CODEX_POTENTIELS_DEUX_ETOILES.md` | b4988a34 | 6497 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/214_CODEX_ABLATION_EXACTE_COMPATIBILITES.md` | 4176b85c | 8474 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/215_CODEX_PROJECTEUR_REEL_ET_MINEURS_TROIS.md` | 2e90184b | 8989 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/216_CODEX_AUDIT_CHOIX_UNIQUE_ET_PROPAGATION.md` | 6755c98e | 8984 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/217_CODEX_DISCRIMINANT_DU_PROJECTEUR_LOINTAIN.md` | ecfbfa0b | 6073 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/218_CODEX_MOTIF_FORCE_COORDONNEES_UNITAIRES.md` | 7d4b0920 | 9996 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/219_CODEX_COMPLETION_ABSTRAITE_GRAM_ETOILE.md` | ee40164d | 10100 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/220_CODEX_ROUTES_HORS_RANGS.md` | 6961745d | 9964 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/221_CODEX_NOYAU_PRISME_DEFECTUEUX.md` | 533f4cba | 9209 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/222_CODEX_PROLONGEMENT_PRISME_MASQUES.md` | 4af5c9d5 | 6842 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/223_CODEX_LIMITE_DES_PREMIERS_PROLONGEMENTS.md` | 380c2671 | 6451 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/224_CODEX_AUDIT_LAP_RANG37_MAILLE5.md` | 34397975 | 11507 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/225_CODEX_NOYAUX_COMPOSANTES_ET_GRILLES.md` | 1f7ca36c | 7312 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/226_CODEX_MASSES789_SANS_PRISME.md` | 9d8c50ca | 11653 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/227_CODEX_C8_SANS_DOUBLES_MOULINS.md` | 200cd105 | 4890 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/228_CODEX_MOULIN_CUBIQUE_NOYAU17.md` | aa81087f | 6515 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/229_CODEX_PARTENAIRES_ET_ANTIVOISINAGES.md` | 0bca28f0 | 10024 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/230_CODEX_COMPLETION_BINAIRE_SEUIL240.md` | 6de85d27 | 10248 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/231_CODEX_SIGNE_RESIDUEL_ET_TRACES.md` | f2f02cd9 | 6877 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/232_CODEX_RIGIDITE_BINAIRE_LAPLACIEN.md` | 412da028 | 6842 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/233_CODEX_DIFFERENCE_RANG4_IMPOSSIBLE.md` | 9cee8104 | 12719 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/234_CODEX_CONNEXITE_MURS_OPPOSES.md` | 45551d9a | 6868 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/235_CODEX_EXPLOITATION_CONVERGENCES.md` | 33a726e8 | 10495 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/236_CODEX_CONVERGENCES_ARETES_PARTAGEES.md` | e6de0570 | 8249 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/237_CODEX_RUBANS_REPARES_PAR_CENTRES.md` | 3444f027 | 7005 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/238_CODEX_FENETRES_TRANSPORT_ET_DENSITE.md` | d39c72b7 | 11704 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/239_CODEX_RUBAN_SIX_CORDES_EN_ETOILE.md` | fc184fdb | 7064 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/240_CODEX_CORDES_DISJOINTES_OU_TRIANGLE_DE_CENTRES.md` | 54e5e9f4 | 7395 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/241_CODEX_ENTREES_CUBIQUES_THETA_IMPAIRE.md` | 22d4be55 | 10337 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/242_CODEX_MOMENTS_QUADRATIQUES_ET_RACINES.md` | 59367c0e | 9339 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/243_CODEX_CONTACTS_NORME26_ET_TRIANGLES_IMPAIRS.md` | 242639a2 | 4692 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/244_CODEX_FANTOMES_ET_CIBLE_INDEPENDANTE_UNIFORME.md` | 5f9be5ab | 11435 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/247_CODEX_HERMITE_ET_RESEAUX_LOINTAINS.md` | 0d63462b | 5356 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/248_CODEX_CAPACITE_TRIANGULAIRE_DES_BLOCS.md` | ddf6e26f | 3990 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/249_CODEX_TROIS_PRISMES_HORS_GRILLE.md` | bdcbbd5c | 8021 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/250_CODEX_PARABOLE_ET_AJOUT_D_UN_SOMMET.md` | 1fd35eab | 5743 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/251_CODEX_NORM16_FORET_LOINTAINE.md` | 6052e39a | 8671 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/252_CODEX_PREMIER_CADRE_NORM16.md` | 9064f3d5 | 5894 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/253_CODEX_NORM16_SOMMET_LOINTAIN_ISOLE.md` | 1dd08d34 | 9204 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/254_CODEX_CADRE35_ET_SCHUR_NORM16.md` | 0b384b94 | 9518 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/255_CODEX_NORM16_PAIRE_OMISE.md` | 9bfd07a3 | 7484 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/256_CODEX_NORM16_OMBRES_PAIRES.md` | 775debf3 | 6318 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/257_CODEX_NORM16_CONNEXITE_DES_OMBRES.md` | eeb2a7d0 | 7952 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/258_CODEX_COUPURES_ET_OBSTRUCTION_DE_BORD.md` | 54ee4c0c | 6280 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/259_CODEX_DEUX_CHEMINS_DE_TRANSPORT_NORM16.md` | 6197ad44 | 6714 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/260_CODEX_P4_DOUBLE_OMIS_ET_BORD_SURVIVANT.md` | a2c99f36 | 5817 | parcouru : en-tête et résultat (L1–~22), sections ciblées |
| P | `c1-main-codex/notes/COINS_LETTRES_EQUATIONS_PROPRES_2026_10_18.txt` | b33f74d0 | 7296 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_line_resonance_20261016/AWS_V21_TYPE9_README.txt` | c5a29e60 | 1556 | README/manifeste de campagne AWS |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_line_resonance_20261016/AWS_V2_CODE_RANGES_README.txt` | 5dbe0741 | 2342 | README/manifeste de campagne AWS |
| N | `conway99-c1:origin/codex/coheawood-hoffman-20261012:data/codex_line_resonance_20261016/aws_7_9_19_20261018_v1.requirements.txt` | bc79d6d4 | 46 | README/manifeste de campagne AWS |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/ARBRE_PARTIEL_C1_C2_2026_10_18.txt` | 75913550 | 5175 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/AWS_7_9_19_2026_10_18.txt` | 5439f086 | 4263 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/COINS_LETTRES_EQUATIONS_PROPRES_2026_10_18.txt` | edab62cd | 7171 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt` | 63e0f1d3 | 4501 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/DROITE_PETITE_ET_RACINE_2026_10_18.txt` | 28cde525 | 4901 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/GRILLE_NEUF_FIBRES_2026_10_18.txt` | 6edb01eb | 4574 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/MINIMUM_PRISMES_RACINE_2026_10_18.txt` | 4406ba0a | 4838 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/MOMENTS_RANG6_2026_10_18.txt` | b702f70c | 1391 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/NOYAUX_GRAM_C3_2026_10_18.txt` | da865e6c | 3171 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/OBSTRUCTION_MOMENTS_5128_2026_10_18.txt` | adc72756 | 4138 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/PARTITIONS_GLOBALES_C3_2026_10_18.txt` | a7704242 | 2910 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/PILOTE_CMIN3_2026_10_18.txt` | 16ccc3df | 8846 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/PIPELINE_COMPTES_PAR_INDEX_2026_10_18.txt` | 0cd4ee9f | 3348 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/RACINE_PONDEREE_2026_10_18.txt` | 877ff2df | 21356 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/RECALCUL_C4_2026_10_18.txt` | 9a1049c6 | 3731 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/RESULTAT_CMIN4_2026_10_18.txt` | ff717adf | 4434 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/RETRACTION_LAB_SANS_GRAM_2026_10_18.txt` | 677fdf9d | 2606 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `conway99-c1:origin/codex/coheawood-hoffman-20261012:notes/SEPARATION_MOMENTS_4192_2026_10_18.txt` | 89153a8c | 4479 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| L | `c1-main-codex/AGENTS.md` | de148e06 | 139576 | lu intégralement (journal Codex 13–19/10) |
| P | `c1-main-codex/notes/FACTEURS_QUATRE_COULEURS_2026_10_19.txt` | 2578b93b | 49854 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `c1-main-codex/notes/FERMETURE_2K2_2026_10_19.txt` | 2073e942 | 6836 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `c1-main-codex/notes/GRILLES_BC_PROFILS_2K2N_2026_10_19.txt` | 28bcb016 | 7776 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `c1-main-codex/notes/NOYAU_SIGNE_2K2N_2026_10_19.txt` | e50d2a01 | 11509 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `c1-main-codex/notes/PAIRES_EGALES_ET_BLOC_DOUZE_2026_10_19.txt` | 8a4b4679 | 8081 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `c1-main-codex/notes/PREUVE_COUPES_CONTINUATION_2026_10_19.txt` | d4cc926b | 13751 | en-tête (L1–~15) ; recoupé avec AGENTS.md |
| P | `c1-main-codex/notes/PRODUCTION_K3_UNIVERSELLE_2026_10_19.txt` | 1b14dfba | 7177 | en-tête (L1–~15) ; recoupé avec AGENTS.md |

## 9. Matériaux pour la recombinaison (section finale)

Abréviations des sources : `CA:` = `conway99-c1:origin/codex/c1-arithmetic-audit:notes/` ; `CH:` =
`conway99-c1:origin/codex/coheawood-hoffman-20261012:` ; `MC:` = `C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/` ;
`DC:` = `C:/home/researcher/Documents/Codex/` ; `AU:` = `MC:code/lab_exploration_2026-10-16/audit_2026-10-18/`. L'identifiant
L05-NNN renvoie au JSONL (sources complètes). Les statuts sont ceux des sources.

### 9.1 Conditionnels « si X alors exclusion / contradiction »

- **K01** Si aucun des 174 noyaux de 14 sommets (motif obligatoire de Makhnev : deux triangles reliés par exactement deux arêtes ;
  373 → 310 → 174 types) ne se prolonge en srg(99,14,1,2), alors C1 est exclu, tous rangs confondus. **O.**
  `MC:RECHERCHE_ACTIVE_C1.md:L637-649`, `CA:222_CODEX_PROLONGEMENT_PRISME_MASQUES.md:L5-10` (L05-098, L05-059).
- **K02** Si chaque triangle appartient à au moins q grilles, les 174 noyaux se réduisent à 115, 52, 11, 2 types pour
  q = 1, 2, 3, 4 ; q ≥ 5 est impossible. **C.** `CA:225_CODEX_NOYAUX_COMPOSANTES_ET_GRILLES.md:L6-9` (L05-062).
- **K03** Si N9-NG (ν(T44) ≤ 9 + min(c_l, c_m) pour tout chevauchement sans grille, équivalent à rang(F) ≥ 12) est vrai, alors
  contradiction : P ≤ 852 force un bloc non grille de c_min ≤ 4, donc rang(F) ≤ 11. **O** (conditionnel prouvé).
  `CH:notes/REDUCTION_RESONANCE_20_2026_10_16.txt:L5-16`, `MC:AGENTS.md:L797-811` (L05-170).
- **K04** Si rang(D) = 9 et rang(Z) ≥ 3 (SYM6), alors rang(F) ≥ 12, d'où K03. Conway + c_min ≤ 4 + D9 imposerait
  rang Z ≤ c_min − 2 : c_min = 1 impossible, c_min = 2 exige Z ≠ 0, c_min = 3 rang ≥ 2, c_min = 4 rang ≥ 3. **P** (réduction).
  `CH:notes/REDUCTION_SYM6_10_2026_10_16.txt:L5-16`, `MC:AGENTS.md:L778-795` (L05-171).
- **K05** ODD-PURE (δ = 0) équivaut à l'absence de perte de rang dans rang(T44) = 32 − c(l) − δ + rang(Z). **P**, cible **O**.
  `CH:notes/COUPLAGE_VINGT_FIXES_2026_10_16.txt:L5-16` (L05-174).
- **K06** Si NG7 (aucun bloc non grille avec min(t_l, t_m) ≤ 7 ne passe les conditions nécessaires de Conway) est vrai, alors
  pas de Conway, car P ≤ 852 force au moins 18 droites t ≤ 7 et au moins 254 tels blocs. **O.** `MC:AGENTS.md:L1306-1315` (L05-150).
- **K07** NG5 (ν ≥ 14 ⇒ min c ≥ 5) implique NG7, via c ≤ g + floor((6 − g)/2) et g ≤ t/2. Implication **P**, NG5 **O**.
  `MC:AGENTS.md:L1313-1316` (L05-150).
- **K08** Si H-MATCH (C1, C1', C2, T et U PSD, ν(T) ≥ 14 ⇒ couplages h-reliés) est vrai, un point de Hamming est forcé (implication
  acceptée de LAB) ; L8 (C1) exclut les points de Hamming. **O.** `MC:AGENTS.md:L1179-1183`, `L1776-1779` ;
  `CH:notes/100_SYNTHESE_DES_LEMMES.md:L167` (L05-158, L05-234).
- **K09** Toute famille locale avec rang_F7(8T_S) ≥ 29 est exclue de tout prolongement (borne globale rang_F7(8T_far) ≤ 28, issue de
  L4/L22/L23). Appliqué à G1 c55 non grille et à <z, hM>. **C** (conditionnel à la borne ≤ 28 reçue de LAB).
  `MC:AGENTS.md:L1808-1824`, `L1520-1527` (L05-144, L05-154).
- **K10** Les 79 configurations de la branche « min_L c(L) ≥ 4 » sont INFEASIBLE ⇒ tout Conway a une droite L avec c(L) ≤ 3.
  **S** (CP-SAT, sans certificat portable ; LAB : aucune vérification indépendante). `MC:AGENTS.md:L600-615`,
  `AU:AUDIT_GLOBAL_2026-10-18_nuit.md:L29-35` (L05-178).
- **K11** Si K10 est certifié et si les gabarits c3 ouverts (435 au 19/10) et la branche c ≤ 2 sont exclus, alors pas de Conway.
  **O.** `MC:AGENTS.md:L15-17`, `AU:AUDIT_GLOBAL_2026-10-18_nuit.md:L13-15` (L05-201).
- **K12** Au rang 43, une racine de M impose 10a8 + 2a9 + 5a10 + 2a11 + a12 ≥ 328 ; l'absence des normes 16..24 force donc
  k = 0 (pas de racine). **P.** `CA:242_CODEX_MOMENTS_QUADRATIQUES_ET_RACINES.md:L5-14` (L05-079).
- **K13** Dans S0 (r = 43, sans racines ni normes 16..24) : une borne ≤ 2288 sur les configurations
  y = (2/9)1 + 1_P − 1_Q (|P| = 7, |Q| = 29, P indépendant) rendrait S0 vide, donc toute la branche sans normes 16..24 du rang 43 ;
  or il en faut ≥ 2289 + 15g. Borne **O.** `CA:244_CODEX_FANTOMES_ET_CIBLE_INDEPENDANTE_UNIFORME.md:L6-16` (L05-081).
- **K14** Au rang 43 : normes 16, 20, 22, 24 absentes ⇒ chaque classe de norme 26 porte t = 329 + 14k − 8(x1 + x2) impair ≥ 1 ;
  « seule norme 18 parmi 16..26 » impossible ; norme 18 absente ⇒ une classe de norme 16 ou 26 porte ≥ 110 vecteurs ; normes 16
  et 18 absentes ⇒ ≥ 329 vecteurs de norme 26 dans une classe. **P.** `CA:177_CODEX_RANG43_CLASSES_COURTES.md:L11-14`,
  `MC:RECHERCHE_ACTIVE_C1.md:L430-434` (L05-014).
- **K15** r = 35 ⇒ ≥ 16 grilles, ≥ 450 prismes, ≥ 33 paires jumelles (r = 35 ensuite exclu). **C.** `CA:179_…:L9-15`,
  `CA:180_…:L6-10` (L05-016, L05-017).
- **K16** min L = 14 ⇒ r ≥ 33 ; r = 33 ⇒ a_7 ≥ 66. **P** (historique). `CA:165_…:L5-8`, `CA:170_…:L9-14` (L05-001, L05-007).
- **K17** Pour r ≥ 37 : 3n₃ ≤ 2n₁ + n₂ (motif (2,2,1) exclu) ; pour r ≥ 39 : 6n₃ ≤ n₁ + 2n₂ (deux apices denses interdits).
  **P/C.** `CA:203_…:L12-20`, `CA:205_…:L8-12` (L05-040, L05-042).
- **K18** Rang 37, droite connexe sans torsion : 60 ombres binaires déterminent les arêtes lointaines, en nombre 240 + 7q ;
  240 ⇔ complétion en srg de rang 37 ; τ(G) ≡ 1, 2, 4 mod 7 ⇒ q ≥ 1 (coût ≥ 247) par L23. **P.**
  `CA:230_CODEX_COMPLETION_BINAIRE_SEUIL240.md:L6-22`, `MC:RECHERCHE_ACTIVE_C1.md:L803-811` (L05-067).
- **K19** Données proches et 60 ombres avec une complétion de rang 37 et bloc proche inversible mod 7 ⇒ aucune autre complétion
  (tous rangs) ; deux complétions distinctes diffèrent par un rang ≥ 5 sur F7 ⇒ (39, 39) impossible. **P/C.**
  `CA:232_…:L9-14`, `CA:233_…:L8-16` (L05-069, L05-070).
- **K20** Rang 37 : mauvais signe résiduel en dimension résiduelle 0 ⇒ toutes les branches de cette dimension exclues. **P.**
  `CA:231_…:L5-11` (L05-068).
- **K21** Bord de 43 sommets avec 3I − B + J/9 > 0 ⇒ ≤ 8192 affectations de signes et ≤ 2 complétions étiquetées, isomorphes ;
  bord de 44 positif ⇒ complétion unique ; tout Conway possède un tel bord. **P.**
  `CH:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:L3367-3542` (L05-108).
- **K22** Sur un tel bord, ≥ 3 composantes de signes forcés ⇒ co-Heawood disjoint du bord (deux cocliques de 22) ; sans
  co-Heawood (p. ex. α ≤ 20), ≤ 2 choix de signes. **P.** idem `L3543-3599` (L05-109).
- **K23** Instance préservant deux flips individuels ⇒ nombre de complétions multiple de 4 ; avec K21 (≤ 2 complétions),
  branche vide. **P.** `CH:data/codex_asymmetry_mechanisms_20261014/bridge_flip_orbit_filter.txt:L1` (L05-118).
- **K24** rang(A' − A) = 2 entre deux srg(99,14,1,2) ⇒ A' = SASᵗ (transposition) : aucun nouveau graphe par modification de rang 2.
  **P.** `CH:notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:L3154-3327` (L05-107).
- **K25** Coclique de 21 dont tout extérieur a ≤ 4 voisins en elle ⇒ elle s'étend en 22 ; exclure toutes les cocliques 21/22
  ne donnerait que α ≤ 20. **P.** idem `L7-37` ; `MC:AGENTS.md:L1996-1997` (L05-101).
- **K26** Deux cocliques de Hoffman se coupant en 15 ⇔ co-Heawood induit ; reste H ≥ 0, rang 16, H² = 147H sur 70 sommets. **P.**
  `CH:notes/NOTE_COHEAWOOD_DEUX_COCLIQUES.md:L6-16` (L05-110).
- **K27** Sur les 84 étiquettes d'une racine : Γ binaire avec T, U PSD et rang T ≤ 30 ⇔ srg(99,14,1,2). **P.**
  `CH:notes/JOURNAL_C1_NUIT_2026_10_14.md:L6038-6128` (L05-160, L05-167).
- **K28** Sous E3 : graphe des grilles contenant C4 ⊔ C3 ⇒ il contient K4 ⊔ C3. **P.** `MC:AGENTS.md:L366-369` (L05-198).
- **K29** Sous E3 : deux rectangles non grilles disjoints avec H_A = −H_B ⇒ deux arêtes internes chacun et union cubique à
  8 sommets ; H_P = H_Q ⇒ bloc complémentaire de 12 sommets réduit ; une colonne non nulle de H apparaît au plus deux fois. **P.**
  `MC:notes/COEUR_HUIT_SOMMETS_5602_2026_10_19.txt:L3-8`, `MC:notes/TROIS_COLONNES_EGALES_INTERDITES_2026_10_20.txt:L1-8`
  (L05-198, L05-202, L05-203).
- **K30** Carré de défaut H05 = H46 = −H06 = −H45, Q12 et Q13 grilles, H23 = H56 ⇒ e23 ≥ 4, contre E3. **P.**
  `MC:notes/CARRE_DE_DEFAUT_ET_PARITE_2026_10_18.txt:L1-12` (L05-186).
- **K31** Ah = −4h, h à valeurs 0, ±1 (14 fois +1, 14 fois −1) ⇒ chaque signe induit ≤ 5 arêtes. **P.**
  `MC:notes/BUDGET_ENTIER_SUPPORT_SIGNE_2026_10_20.txt:L1-8` (L05-204).
- **K32** Rang 37, P = S = 0, plus deux hypothèses ouvertes ⇒ les 231 droites ont le profil (6,6). **P** (conditionnel).
  `CA:210_CODEX_AUDIT_RESIDU_66.md:L9-12` (L05-047).
- **K33** Rang 37 et G(T) sans triangle ni 4-cycle ⇒ G(T) connexe (LAP). **S.** `CA:224_…:L7-20`,
  `MC:RECHERCHE_ACTIVE_C1.md:L743-787` (L05-061).
- **K34** P = 0 ⇒ deux étoiles lointaines d'une arête entre couches partagent exactement un apex, c₄(uv) ≤ 2, 38 types à
  P = S = 0 ; b3 ≥ 73920. **P/E.** `CA:209_…:L7-13`, `CA:186_…:L6-10` (L05-046, L05-023).
- **K35** Conjecture du repère de 231 vecteurs (Gram des triangles) ⇒ P ≥ 1. **O.**
  `DC:2026-09-25/brief-astra-n-1-attaque-ind/outputs/mission_audacieuse/README.md:L5-12` (L05-215).
- **K36** Exclure les trois branches de fonctions courtes (entière 18, entière 26, affine 37) exclurait Conway ; « affine 37 ⇒
  entière 26 » laisserait 18 et 26. **O.** `DC:2026-10-05/salut-j-aimerais-que-tu-regardes/PASSATION_CONWAY_C1_2026-10-06.txt:L39-56`
  (L05-224, L05-227).
- **K37** Involution : g⁻ = 16 ⇒ prisme ; P = 0 ⇒ g⁻ ∈ {18, 20} ; 278/441 types exclus à g⁻ = 18 (C2, historique). **C.**
  `DC:2026-09-25/brief-astra-n-1-attaque-ind/outputs/couverture_g16/ETAT_REPRISE.md:L1-3` (L05-208, L05-209).
- **K38** C2 : fonction propre −4 impaire de support 8 + 8 ⇒ B n'est ni le complément du Wagner ni celui du cube ⇒ min L* ≥ 9/7 ⇒
  aucune paire normale d'enveloppe avec x de norme 3 et Y(x) = 13 (sous T4). **C/P.**
  `DC:2026-10-04/ce-qui-a-t-sauvegard-dossier/work/RESULTS.md:L1-30` (L05-219, L05-220).
- **K39** Aut d'un éventuel Conway ∈ {1, C2, C3} (exclusions publiées consultées) ; pas d'ordre 11. **P.**
  `DC:2026-09-25/brief-astra-n-1-attaque-ind/outputs/automorphismes_1_2/BILAN.md:L5-7` (L05-218, L05-207).
- **K40** Moins de complétions étiquetées d'un bord que |Aut(bord)| ⇒ pas de complétion asymétrique. **P** (critère).
  `MC:AGENTS.md:L822-826` (L05-169).
- **K41** Automorphisme fixant x et chaque paire de N(x), en retournant q > 0 ⇒ q ≥ ceil(t/2) (Conway : pas 1 à 3). **P.**
  `CH:data/codex_asymmetry_mechanisms_20261014/bridge_majority_flips.txt:L1` (L05-118).
- **K42** Cinq triangles deux à deux disjoints, reliés deux à deux par exactement deux arêtes ⇒ contradiction. **P.**
  `DC:2026-09-25/brief-astra-n-1-attaque-ind/outputs/POURSUITE_RECHERCHE.md:L5` (L05-206).
- **K43** x, y non adjacents ⇒ D (26 sommets) connexe ou C6 ⊔ cubique connexe ; K_D défini positif. **P.**
  `DC:2026-10-05/salut-j-aimerais-que-tu-regardes/global_two_stars_rigidity.txt:L7-20` (L05-226).
- **K44** Ruban fermé à m centres réparé seulement entre centres ⇒ m ≤ 8 ; cycle de transport ≥ 9 ⇒ identification ou arête
  latérale. **P.** `CA:237_…:L8-24` (L05-074).
- **K45** Trois prismes de même projection hors grille ⇒ apices indépendants. **P.** `CA:249_…:L5-8` (L05-086).
- **K46** Relation moulin–cubique ⇔ vecteur de noyau de profil (2,1^16) ; sous P = 0, 359 types. **E.** `CA:228_…:L6-10` (L05-065).
- **K47** min c(L) ≥ 4 ⇒ le graphe contient une grille. **P.** `CH:notes/GRILLE_NEUF_FIBRES_2026_10_18.txt:L1-9` (L05-191).
- **K48** Si k = 10 ⇒ m(e) ∈ {0, 2}, P ≤ 462 ; si k ≤ 20 ⇒ toutes les droites 7-dégénérées (C1, historique : k ≥ 22). **P.**
  `CH:notes/100_SYNTHESE_DES_LEMMES.md:L189-198` (L05-238).

### 9.2 Bornes quantitatives (objet, inégalité, hypothèses, statut)

| # | Objet | Borne | Hypothèses | Statut | Réf. |
|---|---|---|---|---|---|
| B01 | P, prismes induits | ≤ 1151 (L16) ; ≤ 1150 ; ≤ floor(11088/13) = 852 | aucune | P ; P ; C (revérifié LAB) | L05-235, L05-127, L05-019 |
| B02 | prismes et grilles | 3P + 4G ≤ 2772 | aucune | C | L05-181 |
| B03 | ρ, grilles 3×3 | ≤ 126 ; ≤ 191 (plus faible) ; e_v ≤ 17 par sommet, ≤ 15 au rang 43 ; ≤ 20 par sommet (GRID21) | — ; r = 43 | C ; P ; C | L05-019, L05-129, L05-033, L05-043, L05-126 |
| B04 | τ, paires de prismes jumeaux | ≤ 2048 ; ≤ 1534 ; ≤ 1403 ; ≤ 1354 ; ≤ 1326 ; ≤ 2871 (plus faible) ; 17τ ≤ 17P + 105ρ ; τ ≤ P + 5ρ + 17 ; τ_g ≤ 11ρ + 17 | — ; r ≥ 37 (1354) ; r = 43 (1326) | E, C, C, C, C, E | L05-027, L05-031, L05-033, L05-041, L05-043, L05-134 |
| B05 | b3, vecteurs de norme 6 de M | ≥ 43848 → 45528 → 45766 → 45898 → 45964 → 46000 ; ≥ 73920 si P = 0 | 45964 : r ≥ 37 ; 46000 : r = 43 | C/E | L05-019, L05-023, L05-031, L05-033, L05-041, L05-043 |
| B06 | b4 | ≥ 2729034 ; ≥ 3371634 ; au rang 37 ≤ 2172309411/136 et b4 + (651/34)b3 ≤ 2291827803/136 | — ; r = 37 | C | L05-017, L05-019, L05-033 |
| B07 | b5 | ≥ 18001368 ; ≥ 34087368 | — | E ; C | L05-012, L05-019 |
| B08 | a_7, a_8 | a_7 ≤ 7920 → 990 → 842 ; ≤ 792 (via ≤ 396 co-Heawoods) ; a_8 ≤ 27720 → 6930 ; 7a_7 + 8a_8 ≤ 55440 ; 14a_7 + 25P + 32ρ ≤ 28182 ; 4N(F10) + 75P + 96ρ ≤ 84546 ; 21a_7 ≤ 2N | — | P/C | L05-007, L05-017, L05-026, L05-133, L05-010, L05-036 |
| B09 | racines de M | b_1 ≤ 88 → 78 → 44 ; b_2 ≥ 462 + 41b_1 + b_1²/2 ; au rang 43 b_2 ≥ 462 + 85b_1 + b_1²/2 ≥ 968 | — ; r = 43 | P | L05-013, L05-028, L05-029 |
| B10 | côté +3 (rang 60) | A_1 = 40, A_2 = 122, A_3 = 400, A_4 = 520, A_5 = 1040 + 52G ≤ 13052 ; B_3 ≥ 1386, B_4 ≥ 12474, B_5 ≥ 182952 ; min(Z^99 ∩ V_3) ≥ 12 | — | P | L05-011, L05-084 |
| B11 | minima de réseaux | min L ≥ 14 ; min L1 ≤ 18, 20, 24, 24, 26 aux rangs 35, 37, 39, 41, 43 ; min(L1 \ L) ≥ 22 | — | P/C | L05-001, L05-009, L05-015 |
| B12 | rang mod 7 | r ∈ {37, 39, 41, 43} ; k = r − 15 ∈ [22, 28] ; rang_F7(8T_far) ≤ 28 ; rang_Q(T) ≤ 30 | — | C ; P | L05-017, L05-236 |
| B13 | co-Heawoods | ≤ 396 ; ≤ 56 par sommet ; ≤ 16 par arête ; ≤ 4 par C4 ; famille orthogonale de norme 14 ≤ 12 ; ≤ 28 racines orthogonales | — | P | L05-133, L05-131, L05-129 |
| B14 | petites couches +3 | ≤ 2871 paires jumelles ; ≤ 5742 vecteurs de norme 12 ; ≤ 8316 de norme 14 ; ≤ 313434 et ≤ 911178 vecteurs de noyaux | masse ≤ 16 | E | L05-134 |
| B15 | configurations de Fano | ≤ 421 non orientées | — | C | L05-026 |
| B16 | collisions | C_90 = 5376 + 12t ≤ 5472 ; C_6 ≤ 39016712 → 38084490 ; C(6,6) ≤ 756τ ; C(6,7) ≤ 108Ω ; C(8,6) ≤ 12814τ ; C(8,7) ≤ 3612Ω ; ≤ 642τ + 710Ω (Ftf) ; ≤ 10380τ + 1528Ω (F0) ; masse 7 ≤ 1420Ω ; C14 ≤ P ; C14 + 2τ ≤ 2P ; N(prisme + maison) ≤ 712800/29 | 38084490 : r ≥ 37 ; C14 : sans grille | P/E/C | L05-035, L05-041, L05-025, L05-030, L05-063, L05-086, L05-027 |
| B17 | représentants | (6,3) ≥ 10336557 ; (5,5) N8 ≥ 2896844 ; N8 + (651/34)N6 ≤ ~8,985 M | — | C/E | L05-019, L05-024 |
| B18 | sommets denses en grilles | n₃ ≤ 39 ; n₃ ≤ 24 | r ≥ 37 ; r ≥ 39 | P ; C | L05-040, L05-042 |
| B19 | budget de racine | ∃ x : s(x) ≤ 51 ; score 9s + 8g ≤ 504 ; s ≤ 49 sous c ≥ 4 | P ≤ 852 | P ; C | L05-182, L05-181 |
| B20 | arbres couvrants du graphe proche | τ ≥ 12970803 au rang 37 (96855123, 225000000 si min L ≥ 18, 20) | formule de LAB | P (conditionnel) | L05-084 |
| B21 | S0 | configurations P7/Q29 ≥ 2289 + 15g ; g ≤ 22 ; d ≤ 48 (≤ 45) ; ≥ 6 (≥ 22) triangles impairs ; 329 par classe de norme 26 | r = 43, S0 | P | L05-081, L05-080, L05-079 |
| B22 | P3/N25 | forêt de 12 arêtes, 32 formes ; 1 ≤ t_p ≤ 3 ; 3 ≤ δ ≤ 9 ; supports 6899 → 5345 → 4581 → 3640 → 3343 | S0 | P/C ; LAP rapporté | L05-082, L05-083, L05-087 |
| B23 | norme 16 | 5 cœurs ; 4985 / 478 attaches ; e(D) ≤ 1 ; 15 → 14 formes de Z, 75 → 70 supports ; 18 attaches exclues ; cadre 35 de rang ≤ 33 ; 71351 supports PSD (attaches 0..4) | — | E/P/C | L05-003, L05-006, L05-088, L05-090, L05-091, L05-093, L05-094 |
| B24 | norme 18 et 20 | ≤ 1 arête par support ; ≥ 6 graines ; norme 20 : ≤ 1 arête par support, ≤ 4 voisins par support, 29 histogrammes ; cœurs N20 : 1381 | — | P | L05-008, L05-013, L05-100 |
| B25 | noyaux | 373 → 310 → 174 ; 359 types moulin–cubique (29, 122, 208) ; 38 types deux étoiles ; 22/29 modèles au rang 37 | — ; P = 0 | C/E | L05-058, L05-059, L05-065, L05-046, L05-042 |
| B26 | branche min c = 4 | 221 types → 200 → 103 → 100 → 87 → 79 ; quotient de Gram de rang ≤ 4 | min c = 4 | S | L05-175 |
| B27 | registre c3 | 10052 → 1163 → 902 → 537 → 435 ouverts ; K3U 2742342 bords ; 2K2 : 7 résiduels ; (2,3) : 5312 ; 5602 : 1328 bords → 58 graphes | — | C/S/O | L05-201, L05-193, L05-195, L05-197, L05-198 |
| B28 | inégalités d'arêtes | e(P7) + e(N8) − e(P7, N8) ≤ 14 ; e(O ∪ S) ≤ 48 (≤ 44 si O grille) ; chaque signe d'un support ±1 de 14 + 14 : ≤ 5 arêtes ; e(Q) ∈ {0, 1, 2, 4} (E3) | — | P | L05-162, L05-152, L05-204, L05-177 |
| B29 | attaches à cinq étoiles | ≥ 4 des 8 lignes brisent h ; D ≥ 12 ; D ≥ max(0, 2k − 16) ; private_Y(x) + deg_P(x) ≤ 4 | — | P | L05-164 |
| B30 | relations mixtes et budgets | Σ m ≥ 6804 ; ≥ 336 drapeaux à m ≥ 4 ; ≥ 18 sommets ; 5Σ‖E‖² + 928P + 48Z ≤ 12374208 ; 5Δ + 448P − 72Z ≤ 7135128 | ρ ≤ 126 | P | L05-146, L05-147 |
| B31 | rangs locaux | rang T_X = 23 − c ; rang E = 12 − c ; rang K = 21 − c(l) ; rang T44 = 23 − c + rang F = 32 − c − δ + rang Z ; rang L = 10 − c(m) ≥ 5 ; nullité non triviale ≥ 9 − min c (G1) ; nullité_Q(T) ≤ 14 (<z,hM>) | — | P | L05-138, L05-173, L05-174, L05-170, L05-172, L05-142, L05-154 |
| B32 | poids binaires | relation de noyau non négative : ≥ 16 ; mots de im_F2(A) : ≥ 8 (Conway), ≥ 12 (243), w ≥ 2 + (k − 2)/μ, w ≥ hk/(2h − 1) | — | P/C | L05-139, L05-119 |
| B33 | cocliques | 21 : 2 à 6 sommets à 5 voisins, ≤ 30 sommets de défaut ; charge w < 0 ou > 18δ ; ≥ 11 couvertures distinctes par domaine ; 36 designs exclus (29 à groupe trivial) | — | P/C | L05-101, L05-102, L05-111, L05-112 |
| B34 | complétions | ≤ 8192 signes ; ≤ 2 complétions ; q = 44 − rang(3I − B + J/9) ; 1540 arêtes extérieures ; 240 + 7q arêtes lointaines | bord 43 positif ; rang 37 | P | L05-108, L05-067 |
| B35 | fonctions courtes | U16 ≤ 1168 ; 16U18 + U26 ≥ 296 + 112m + 7U20 + 2U22 + U24 (m ≤ 10) ; affine niveau 1 : norme ≥ 21 ; niveau 2, norme 24 : vide | hôte fixé | P | L05-224, L05-225 |
| B36 | asymétrie | q ≥ ceil(t/2) flips ; code de flips purs : poids ≥ 4, |C_x| ≤ 8 (Conway) ; |Aut| des srg(243) : 3849120, 4320, 864, 3888 | — | P/C | L05-118, L05-114 |
| B37 | C2 (historique) | 441 types P = 0, 278 exclus à g⁻ = 18 ; g⁻ ≥ 18 + t − 2r₀ + ε ; g⁻ ≥ 24 − 2r₀ (A33) ; min L* ≥ 9/7 ; N : 588 paramètres | involution | C/P | L05-208, L05-209, L05-212, L05-219, L05-221 |
| B38 | divers | plateau E = 4464 : ≥ 25 sommets à modifier ; BvLS à bord libéré : 27648 matrices = 2 classes | — | C/S | L05-217, L05-229 |

### 9.3 Lemmes ouverts et étapes manquantes (qui en a besoin, ce que cela donnerait)

- **O01** Prolongement (ou non) des 174 noyaux. Recherche A de Codex. Donnerait l'exclusion de C1 (K01). L05-098.
- **O02** rang(F) ≥ 12 universel (N9-NG). Codex et LAB, 16/10. Donnerait K03. L05-170.
- **O03** SYM6 (rang Z ≥ 3), D9, ODD-PURE, ODDCONST. Codex. Donneraient rang F ≥ 12. L05-171, L05-174.
- **O04** NG7, NG5. LAB et Codex, 15/10. Excluraient Conway (K06, K07). L05-150.
- **O05** H-MATCH. Cible unique de LAB le 16/10. Forcerait un point de Hamming (K08). L05-158.
- **O06** Borne ≤ 2288 sur les configurations P7/Q29 de S0. Codex et LAP. Fermerait S0 (K13). L05-081.
- **O07** Certificat portable de la fermeture c ≥ 4. Demandé par l'audit LAB du 18/10. Ferait passer K10 de S à C. L05-178.
- **O08** Gabarits c3 ouverts (435) et branche c ≤ 2 (c = 1 : 2302537 classes après le lemme FG ; c = 2 non comparé ; k = 0 non
  recensé : `AU:AUDIT_GLOBAL_2026-10-18_nuit.md:L22-27`, `L63-66`, `L79`). Avec O07, fermerait C1 (K11). L05-201.
- **O09** « Rang 37 ⇒ P > 0 ». Visé le 09/10 (note 226) ; bornes trop larges ; census P = 0 entier. L05-063, L05-149.
- **O10** Un plafond de torsion (P ≥ 1152) manquait aux lemmes L1–L23 de C1 (note 100 §5, `CH:notes/100_SYNTHESE_DES_LEMMES.md:L228-245`). L05-237.
- **O11** Existence d'une première complétion binaire au rang 37 ; borne ≥ 247 dans les classes ouvertes. Notes 230–233. L05-067, L05-069.
- **O12** Construire B, D pour un bord de 43 ; famille co-Heawood ; famille (0,2) ; preuve de α ≥ 21. V12–V15. L05-108, L05-109.
- **O13** Implication affine 37 ⇒ entière 26 ; sous-cas m = e = 0 ; Q23. Application Codex, 06/10. L05-227.
- **O14** Conjectures (B) et (C). Codex, 14/10. L05-140.
- **O15** C4DO générale, SYM, QUOT ; KER-SYM et SUM14 à ν ≥ 14. L05-156, L05-157, L05-153.
- **O16** Norme 16 : quatre attaches et le survivant de bord ; « inégalité de bord uniforme sur les labels U/V de 257 »
  (`MC:RECHERCHE_ACTIVE_C1.md:L60-61`). L05-097.
- **O17** Triangle de centres alternés du ruban six ; cycles de transport longs réparés. L05-077, L05-075.
- **O18** Trois prismes jumeaux hors grille à apices indépendants. L05-086.
- **O19** Les deux hypothèses du résidu (6,6). L05-047.
- **O20** Conjecture du repère de 231 vecteurs (donnerait P ≥ 1). L05-215.
- **O21** Construction d'un srg(243,22,1,2) ou λ = 1 asymétrique (cible Γ6 racine 0 ; moteur non implémenté selon
  `cw/review/09_codex_14_16oct.md:L87`). L05-117.
- **O22** Conjecture K7 (α = 22). L05-231.
- **O23** C2 (historique) : EX de MODEL.md et dix couples (n, k) des coupes du 04/10. L05-220.

### 9.4 Méthodes transférables

- **M01** Recensement paramétré (v, k, 1, 2) depuis un sommet, contrôlé exhaustivement sur la grille 3×3 et sur deux srg(243)
  (source : note 184, paquets (243,22) et (9,4)). L05-021.
- **M02** Certificat LP rationnel converti en identité à poids ≥ 0 (P ≤ 852, 3P + 4G ≤ 2772). Toute baisse de P resserre le budget
  de racine s ≤ floor(6P/99) = 51, donc la couverture c3 (sans budget, 17 gabarits de plus restent ouverts :
  `AU:AUDIT_EXCLUSIONS_2026-10-18.md:L30`) ; à l'ordre 9, E3 n'améliore pas P (`AU:AUDIT_EXCLUSIONS_2026-10-18.md:L245`).
  Un census d'ordre 10 avec E3 est une piste (suggestion de l'agent).
- **M03** Théorème de complétion E0 = C⁺R (V13), écrit pour k, μ généraux avec régularité : applicable à srg(243) et à d'autres
  paramètres (source : énoncé en k, μ, q). L05-106.
- **M04** Rigidité « différence de rang 2 = transposition » : NON transférable telle quelle (contre-exemple (16,6,2,2)). L05-107.
- **M05** Moments sans Gram et lemme de localisation des mots binaires : valables pour tout srg(v,k,1,2) (source). L05-188, L05-119.
- **M06** Théorème des flips majoritaires pour srg(1 + 2t², 2t, 1, 2) : Conway (t = 7) et 243 (t = 11) (source). L05-118.
- **M07** Critère « deux PSD suffisent » (P = 27I − 9A + J et Q = 44I + 11A − 2J ; T + U = 7Π à une racine) : la forme
  générale « deux encadrements spectraux + intégralité » s'applique à tout srg (suggestion de l'agent). L05-110, L05-167.
- **M08** Arguments de Witt, genre et discriminant mod 7 : utilisés en C2 (Astra : A33, g⁻) et en C1 (L22, L23, note 231, DISC). L05-212, L05-236, L05-068, L05-163.
- **M09** Obstructions C2 « complément du cube / du Wagner » pour une fonction propre −4 de support 8 + 8 (04/10), face à la
  classification C1 des cinq cœurs de norme 16 (07/10). À comparer, en vérifiant si les preuves C2 utilisent l'involution de façon
  essentielle ; sinon, elles pourraient éliminer des cœurs de norme 16 en C1 (suggestion de l'agent). L05-219, L05-220, L05-003.
- **M10** Reconstruction « garder un bord, recompléter » : Paley(25) donne 15 classes dont 2 asymétriques, BvLS 2 classes, puis
  bords de Hoffman à 99 et 174 noyaux (source : INDEX.md ; NOTE_HOFFMAN). L05-228, L05-229, L05-112.
- **M11** Schur et blanchiment sur les blocs à quatre étoiles (Q20, SYM6, énergie paire), calibrés sur les objets locaux de LAB et des
  grilles de 243 (source). L05-170 à L05-174.
- **M12** Routes A/B/C de C2 relues pour C1 (note 220) : motif obligatoire plutôt que rang. L05-057.
- **M13** Contrôles positifs systématiques (srg(9,4,1,2), rook9, Petersen, Clebsch16, BvLS, twin243) avant tout verdict
  (`MC:AGENTS.md:L11`, `L53`, `L66-67`).
- **M14** Méthode « plan de comptage » de Codex (zscan1) reprise par LAB : 7361 certificats de Farkas entiers sur les
  10052 gabarits c3 (`AU:AUDIT_GLOBAL_2026-10-18_nuit.md:L48`) — transfert effectif Codex → LAB.
- **M15** Test DISC de LAB (classes 2/14 et 1/7) intégré par Codex à la réparation de cœurs — transfert LAB → Codex. L05-163.
