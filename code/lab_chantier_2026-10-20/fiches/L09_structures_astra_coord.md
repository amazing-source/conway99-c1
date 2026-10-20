# Fiche L09_structures_astra_coord : labo « structures », rank-17, Astra et Sol, coordination de C1, données, relectures

Consolidation du chantier du 20/10/2026 (agent du lot L09). Lecture seule de toutes les sources ; seuls ce fichier,
`L09_structures_astra_coord.jsonl` (résultats, champs des CONSIGNES) et `L09_structures_astra_coord_recomb.jsonl`
(matériaux de recombinaison, un objet par ligne) ont été écrits, dans `work/chantier_2026-10-20/fiches/`.

**Périmètre réellement couvert.** Les 176 entrées de `lots/L09_structures_astra_coord.jsonl` (conway99-c1 `main` : README,
JOURNAL, LAB_INSTRUCTIONS, rapport, notes 00–154, data/, tools/win64 ; conway99-c1 `origin/main` : AGENTS.md et les sept notes
du 19/10 ; conway99-structures-lab `master` et la branche `origin/claude/chat-session-09hf0k` ; conway99-rank17 `master` ;
`C:/home/researcher/cw/review`). En plus, parce que la consigne du coordinateur les nomme : le dossier d'Astra du Bureau
(`Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836`, lot primaire L01), la campagne Astra « BvLS » (`research/astra_bvls_boundary_20261011`),
`dossiers_externes/` (lots primaires L05/L07), `PASSATION_C1_2026-10-07.md`, `CLAUDE.md` et la tête de `RECHERCHE_ACTIVE_C1.md`
(L05) ; ces pièces sont traitées au niveau « contenu et résultats principaux ». `Desktop/Recherche_Conway/c1-structures-audit`
est un clone sans arbre de travail au même commit que `cw/conway99-structures-lab` (HEAD 3e9690b, arbre 7dbf51c) : rien à lire.

**Méthode.** Chaque affirmation des fichiers porte une source `dépôt:branche:chemin:ligne` ou `chemin:ligne`. Un script de contrôle
(`scratchpad/L09/parts/verify.py`) a vérifié, pour toutes les lignes, que le fichier existe et que la plage de lignes est valide,
et, pour les 633 matériaux de recombinaison, que la citation littérale figure dans la plage citée (0 problème restant). Les statuts
sont recopiés des sources, jamais rehaussés (règle des CONSIGNES). Les identifiants `L09-NNN` renvoient au JSONL ; les matériaux de
recombinaison ont les identifiants `L09-COND-NNN`, `L09-BORNE-NNN`, `L09-LEMME-NNN`, `L09-METH-NNN`.

## 1. Résumé (10 lignes au plus)

1. 508 résultats (P 262, E 73, C 28, S 17, H 78, O 28, R 10, X 12) et 633 matériaux de recombinaison (249 conditionnels, 210 bornes, 99 lemmes ouverts, 75 méthodes).
2. C1, 24–29/09 (Claude-C1) : 25 lemmes L1–L25, tous des « planchers » (L8 : pas de point de Hamming ; L16 : P ≤ 1151 ; L22 : k ≤ 28 ; L21/L23) ; le profil P = 0, k = 28 les satisfait tous, donc aucune contradiction par combinaison (L09-103, L09-110).
3. Labo « structures » (25–27/09) : vérificateur et passeur entre C1, C2, Astra et Sol ; critère 2-adique S5 (35 « ? » de la table de Brouwer exclus ; rien pour 99) ; pour C2 : tout-tordu exclu seulement pour les circuits simples (erratum L09-263), AD jusqu'à n_dd = 6, g⁻ ∈ {18, 20}, 156 enveloppes construites, O₂₄ 86/141.
4. Rank-17 (27/09–01/10) : 1 272 classes (V, y-paires) = 492 (Sol, preuve non archivée) + 26 (moteur) + 754 ouvertes ; il suffit de R6 ∧ R8 (L09-414) ; théorème caractéristique d'Astra (29/09) puis 228/751 classes fermées (L09-430, L09-431).
5. C2 est ensuite déclaré exclu par la route (C) le 07/10 (L09-055), avec un statut « IA seulement, sans lecteur humain ni formalisation » (L09-499).
6. Astra : dossiers 2–6 et audits relus « tout tient » par « structures » ; l'auteur réel du dossier du 27/09 et des dossiers externes est ambigu (Astra / Sol / Codex / ChatGPT, section 6.1).
7. Codex et LAB (14–19/10, C1) : c(L) ≤ 3 forcé (CP-SAT, L09-473) ; familles gz5602, (2,3), K3U et 2K2 fermées par manifestes et RUP vérifiés ; registre « c3 » ramené à 435 gabarits ouverts le 19/10 ; Conway global reste ouvert.
8. Corrections majeures : re-scope du 27/09, erratum « circuits simples » (27/09), bug OR-Tools (18/10), ODD9 et KER-SYM universelles réfutées (15/10), Théorème A du carnet C2 (25/09).
9. Combinaison signalée deux fois indépendamment (relectures 02 et 05) : la classe de carré « 14 » de DISC pourrait tomber par la parité 7-adique déjà prouvée (L4, Théorème A) — non vérifié (L09-501, L09-508).

## 2. Chronologie

| date | qui | quoi | réf. |
|---|---|---|---|
| 24/09 | Claude-C1 (chercheurs F et R) | fondations F1–F13, L1–L16, frontière SAT de torsion, route de Hodge close, L16 P ≤ 1151 | L09-001, L09-013, L09-028, L09-041 |
| nuit 24–25/09 | Claude-C1 | L17–L20 ter, RRR, ordre 8, littérature (Makhnev = L1), L7 à la main, Akiyama | L09-029–L09-034, L09-045, L09-074 |
| 25/09 | Claude-C1 ; utilisateur | L21 (05 h 30), synthèse (06 h), gel des solveurs par l'utilisateur (06 h 15), L22, L23, Kneser, L8 par le squelette de Fano, L25, L11, routes closes (notes/110), L14 | L09-035–L09-039, L09-047, L09-125 |
| 25/09 | Claude-C2 (carnet) ; Astra | carnet C2 : Théorèmes A (corrigé), B, D, F, P, 24.3 ; audit adverse d'Astra (erreur du Théorème A) | L09-381–L09-390 |
| nuit 25/09 | Claude-structures | ouverture du labo : S1 (L22 général), S5 (critère 2-adique), S3, S6, S7–S11 (tout-tordu à la main), S12 (vérif. de notes/116), certificat d'Astra vérifié | L09-245–L09-256, L09-265, L09-316 |
| 26/09 | structures ; C1 ; Astra ; C2 | S13–S21 (certificats tout-tordu 1 et 0 triangle, Ψ_R, P-Ψ) ; dossiers d'Astra 2–5 et retours ; notes 117–132 (torsion maximale, Fano tendu, I_x, 7-adique, q:7) ; famille 9/243 ; décision « C1 et structures à fond sur C2 » ; directive « paris et percées » ; q:7 g⁻ ∈ {16,18,20} ; AD ; rapports de Sol | L09-259–L09-332, L09-163–L09-213 |
| nuit 26–27/09 | Sol ; C1 ; structures | A33 mort, g⁻ ≠ 16 (donc g⁻ ∈ {18, 20}), famille ancrée Σ ≠ ∅ morte, bloc plein | L09-297–L09-299, L09-213 |
| 27/09 | structures ; C1 ; C2 ; Sol ; GPT-Pro ; Astra | erratum « circuits simples » (07 h) ; 25 puis 33/79 types DRAT ; ligne d'arrivée (10 h 15) ; route (C) de Sol : 156 enveloppes (S35), O₂₄ 86/141 (S36), 132 et 115 fermés ; handoff GPT-Pro du rank-17 ; dossier Astra (campagnes 08 h 03 et 08 h 36) ; notes 133–146 | L09-263, L09-302, L09-307–L09-313, L09-393, L09-442 |
| 28/09 | structures ; C1 ; Sol | rank-17 : ℤ¹⁷, min K* ≥ 5/7 (Sol, 492), obligation de preuve, R8 k = 0, R6 J1a, moteur wfe ; notes 147–154 | L09-404–L09-428, L09-232–L09-244 |
| 29/09 | Astra ; C2 ; Sol | théorème caractéristique, 228/751 ; paquet Type 0/II de Sol ; arrêt de la branche main de conway99-c1 (29/09) | L09-430–L09-434 |
| 01–02/10 | structures ; Claude-cloud | evenframe et paradigm (rank-17) ; brouillon d'ordre 7 sans ordinateur (branche structures) | L09-435–L09-437, L09-391 |
| 06–07/10 | Claude-cloud | notes 155–164 (route Ω, second srg(243) tordu, PASSATION) ; 07/10 17 h 47 : C2 déclaré exclu (156/156) | L09-055, L09-056, L09-458 |
| 08–09/10 | LAB, Codex ; utilisateur | échelle de rang (r = 35 exclu le 08/10) ; consigne du 09/10 « exploration, lemmes de réduction » | L09-503, L09-456 |
| 11–12/10 | Astra / ChatGPT ; Claude-cloud | campagne BvLS après Paley ; dossiers externes (Paley 25, BvLS, Hoffman, K7, CODE7) versés le 12/10 | L09-450–L09-455 |
| 14–16/10 | utilisateur ; Codex ; LAB ; Claude-review | consignes « asymétrie » et « deux chercheurs » ; V15 ; P ≤ 852 ⟹ 254 blocs ; ODD9/KER-SYM réfutées ; T + U = 7Π ; relectures 01–09 (16/10) | L09-457, L09-460–L09-469, L09-495–L09-508 |
| 18/10 | Codex ; LAB | bug OR-Tools (retraits) ; branche c(L) ≥ 4 fermée (CP-SAT) ; 3P + 4G ≤ 2772 ; gabarits c3 exclus sans Gram | L09-471–L09-476 |
| 19/10 | Codex ; LAB | gz5602, (2,3), K3U, 2K2 fermés ; registre 10 052 → … → 435 ; premier raccordement 2K2N ; notes du 19/10 | L09-477–L09-494 |

## 3. Table des résultats

Statuts : P preuve écrite (voir `relu_par` dans le JSONL), C calcul exact certifié, E calcul exact sans certificat, S verdict de solveur, H heuristique ou indice, O ouvert, R réfuté, X retiré. Sources complètes, énoncés, dépendances et remarques : JSONL. Ordre : par tranche de sources (A1, A2, B1, B2, C, D1, D2, D3, E, F, G1, G2, H).


**A1 — conway99-c1:main — README, JOURNAL, LAB_INSTRUCTIONS, rapport, notes 00–50, data/**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-001 | F1-F4 : structure enracinée et spectre du second sous-constituant | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/00_FONDATIONS.md:7-47` |
| L09-002 | F5/L5 : grilles serrées | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/00_FONDATIONS.md:49-60` |
| L09-003 | F7 : rangs modulaires forcés | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/00_FONDATIONS.md:70-76` |
| L09-004 | F8 : coïncidence propre à 99 dans la famille PQ(2,t,2) | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/00_FONDATIONS.md:78-83` |
| L09-005 | Géométries locales tordues explicites (non SRG) | E | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/20_ATTAQUES_R.md:13-19` |
| L09-006 | F2 (rigidité q=3) tuée sous forme locale | R | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/20_ATTAQUES_R.md:23-28` |
| L09-007 | F2' et F11 tuées hors diamètre 2 seulement (re-scopées le 27/09) | R | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/20_ATTAQUES_R.md:29-31` |
| L09-008 | F1/F13 : entrelacement autour d'une droite sans violation | H | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/20_ATTAQUES_R.md:43-48` |
| L09-009 | F14 (annulation de Krein) tuée | R | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/20_ATTAQUES_R.md:92-95` |
| L09-010 | F4 (cohérence de classes / Fano) tuée localement | R | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/20_ATTAQUES_R.md:50-54` |
| L09-011 | F17 : torsion ⇒ plan projectif d'ordre t (affaiblie) | O | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/10_IDEES_F.md:34` |
| L09-012 | Validation du modèle enraciné sur l'analogue q=2 (Gewirtz) | S | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/20_ATTAQUES_R.md:147-159` |
| L09-013 | F23 / théorème H0 : le confinement du spectre de Hodge est faux pour toute la famille | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/20_ATTAQUES_R.md:161-169` |
| L09-014 | L1 : Γ est tordu | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/30_LEMMES.md:8-27` |
| L09-015 | L2 : rank₇(A−3I) est impair | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/30_LEMMES.md:30-44` |
| L09-016 | L3 : recollement 7-adique de Λ₃ non scindé | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/30_LEMMES.md:46-52` |
| L09-017 | L4 : invariant global k pair | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/30_LEMMES.md:54-64` |
| L09-018 | L7 : un point de Hamming n'est jamais le point fixe d'une involution | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:67-89` |
| L09-019 | L8 : aucun sommet n'est un point de Hamming | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:91-113` |
| L09-020 | L9 et L9' : règles locales de grilles manquantes | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:136-155` |
| L09-021 | L10 : g(x) ≤ 18 | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:123-152` |
| L09-022 | L11 : les torsions ne peuvent pas être confinées à 3 classes | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:115-121` |
| L09-023 | L12 : règle de propagation de la torsion | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/30_LEMMES.md:157-176` |
| L09-024 | L13 : une classe est tordue par 0 ou au moins 2 étiquettes | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/30_LEMMES.md:178-187` |
| L09-025 | L14 (\|C\| = 2) : deux étiquettes tordues tordant 2 classes impossibles | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:189-195` |
| L09-026 | L14 (\|C\| = 3, 4) par SAT | S | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/30_LEMMES.md:196-198` |
| L09-027 | L15 : torsion totale = moment spectral | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/30_LEMMES.md:200-215` |
| L09-028 | L16 : condition de Krein pour les droites, P ≤ 1151 | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/30_LEMMES.md:217-226` |
| L09-029 | L17 : le 70-espace local se scinde en 2, 3, 5 | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/30_LEMMES.md:228-236` |
| L09-030 | L18 : la seconde variable libre d'ordre 7 = statistique S | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/30_LEMMES.md:238-247` |
| L09-031 | L19 et L19 bis : forme de Smith 7-adique de U_x ; k ≥ 2 | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:249-258` |
| L09-032 | L20 : k ≥ 11 − 2e(τ_a) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:260-269` |
| L09-033 | L20 bis : k ≥ 8 | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:276-280` |
| L09-034 | L20 ter : k ≥ 10 | S | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:271-274` |
| L09-035 | L21 : boule d'une droite, k ≥ 23 − d(L) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:282-296` |
| L09-036 | L22 : k ≤ 28 (genre de Λ₋₄) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:298-305` |
| L09-037 | L23 : signe de la boule d'une droite | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:307-318` |
| L09-038 | L24 : point de Hamming, réduction de Kneser et 18 ≤ k ≤ 26 | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:320-329` |
| L09-039 | L25 : pas de tissu de 11 grilles à couplages purs | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/30_LEMMES.md:331-339` |
| L09-040 | L6 : identités de comptage enracinées | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/30_LEMMES.md:344-349` |
| L09-041 | Frontière de torsion : exclusions SAT de configurations presque non tordues (24/09) | S | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/50_FRONTIERE_TORSION.md:10-29` |
| L09-042 | Trois étiquettes tordues : 24 motifs sur 128 UNSAT | S | Claude-C1 | 2026-09-24 | `conway99-c1:main:data/k3_results.txt:1-26` |
| L09-043 | Limite de la méthode de frontière | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/50_FRONTIERE_TORSION.md:39-40` |
| L09-044 | Contrôle de Reimbayev arXiv:2608.19410 (ordre 7) | E | Claude-C1 | 2026-09-24 | `conway99-c1:main:JOURNAL.md:37-40` |
| L09-045 | Hiérarchie exacte d'ordre 8 : tout bute sur L16 | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:JOURNAL.md:71-78` |
| L09-046 | Tentative de construction par RRR (Elser) | H | Claude-C1 | 2026-09-25 | `conway99-c1:main:JOURNAL.md:79-88` |
| L09-047 | Décision utilisateur du 25/09 : plus aucune campagne de solveurs | H | utilisateur | 2026-09-25 | `conway99-c1:main:JOURNAL.md:157-159` |
| L09-048 | Contrôle positif CNF sur BvLS jamais fait (dépendance des UNSAT) | O | Claude-C1 | 2026-09-24 | `conway99-c1:main:LAB_INSTRUCTIONS_C1.md:13-33` |
| L09-049 | Voie 7-adique par sous-matrices déterminées : close | H | Claude-C1 | 2026-09-26 | `conway99-c1:main:JOURNAL.md:289-290` |
| L09-050 | Rapport d'Astra, dossier n° 2 : revêtement de degré 4 de K₇ et branche de Heawood | E | Astra | 2026-09-26 | `conway99-c1:main:JOURNAL.md:303-311` |
| L09-051 | Rapport d'Astra, dossier n° 3 : P-Ψ n'est pas un lemme de Fano complet ; bornes ordonnées | P | Astra | 2026-09-26 | `conway99-c1:main:JOURNAL.md:322-336` |
| L09-052 | Porte I_x à P = 0 : identités et seul apport nouveau H(x) = 12 936 | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:JOURNAL.md:337-354` |
| L09-053 | La fermeture est essentielle à P = 0 | E | Claude-C1 | 2026-09-26 | `conway99-c1:main:JOURNAL.md:355-361` |
| L09-054 | Relecture croisée des 14 preuves AD2 à une racine du labo structures | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:JOURNAL.md:583-594` |
| L09-055 | C2 déclaré exclu le 07/10 (version ultérieure du JOURNAL) | E | Claude-cloud | 2026-10-07 | `conway99-c1:origin/main:JOURNAL.md:654-665` |
| L09-056 | Nouveau srg(243,22,1,2) tordu (version ultérieure du JOURNAL) | E | Claude-cloud | 2026-10-07 | `conway99-c1:origin/main:JOURNAL.md:625-633` |

**A2 — conway99-c1:main — notes 60–103 (+ diff de notes/100 sur origin/main)**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-057 | Lemmes H1–H3 : torsion = non-commutation (Hodge) | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/60_HODGE.md:49-81` |
| L09-058 | Route Σν³ close : majorer Σν³ ⟺ majorer n₃ ⟺ F2-SRG | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/60_HODGE.md:83-92` |
| L09-059 | Littérature : Lou–Murin 2014 et autres (lues le 24/09) | P | littérature | 2026-09-24 | `conway99-c1:main:notes/60_HODGE.md:110-118` |
| L09-060 | Théorème K1 (= L16) : identités annexes et propreté à 99 | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/70_KREIN_DROITES.md:12-49` |
| L09-061 | Renforcements de L16 essayés : aucun gain | E | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/70_KREIN_DROITES.md:51-60` |
| L09-062 | Torsion = moment cubique des droites | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/80_ETINCELLE_ARITHMETIQUE.md:12-20` |
| L09-063 | Structure d'Eisenstein des droites orientées | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/80_ETINCELLE_ARITHMETIQUE.md:46-62` |
| L09-064 | Identité « les droites éloignées portent la torsion » | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/80_ETINCELLE_ARITHMETIQUE.md:78-88` |
| L09-065 | Reformulation : non-existence ⟺ torsion moyenne < 14,24 | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/80_ETINCELLE_ARITHMETIQUE.md:90-98` |
| L09-066 | Matrice des réflexions Z et opérateur de défaut Δ | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/90_SECONDE_VARIABLE.md:57-76` |
| L09-067 | Borne de Delsarte locale sur le schéma des étiquettes : triviale | E | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/90_SECONDE_VARIABLE.md:86-98` |
| L09-068 | Similitude de torsion U_x = (2H + I)Σ_x | P | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/90_SECONDE_VARIABLE.md:100-108` |
| L09-069 | Mur L16 : l'information locale jusqu'à 8 points est contenue dans L16 et L18 | E | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/91_HIERARCHIE_ORDRE8.md:17-57` |
| L09-070 | Littérature construction et étalonnage RRR | H | Claude-C1 | 2026-09-24 | `conway99-c1:main:notes/92_CONSTRUCTION.md:11-36` |
| L09-071 | F17 naïve réfutée par les produits cartésiens | R | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/93_NON_EXISTENCE_V2.md:18-27` |
| L09-072 | Programme B (second moment de Δ) : échec expliqué | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/93_NON_EXISTENCE_V2.md:11-16` |
| L09-073 | Programme D : parités d'holonomie sans loi | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:31-46` |
| L09-074 | Makhnev 1988 : L1 était connu | P | littérature | 2026-09-25 | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:49-58` |
| L09-075 | Lemme de variance de Wilbrink–Brouwer appliqué à 99 | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:60-76` |
| L09-076 | Reimbayev srg(19,6,1,2) : saturation absente à t = 6 | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:78-85` |
| L09-077 | État de l'art littérature sur 99 (BvM 2022, Wilbrink 1984, Cesarz–Woldar 2025, van Eijl 1991…) | P | littérature | 2026-09-25 | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:87-142` |
| L09-078 | Identité trace–rang d'Ishida appliquée à une involution de 99 | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:104-115` |
| L09-079 | Méthodes Shpectorov–Zhao et Kivva non transposables | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:117-125` |
| L09-080 | Reimbayev 2511.06572 (sous-graphes hamiltoniens d'ordre 7) non lu | O | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:153-156` |
| L09-081 | Lecture « matrice d'orbites » de L7 (portée C2) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/95_L7_PREUVE_HUMAINE.md:93-104` |
| L09-082 | Image « code de Golay factice » au point de Hamming | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/95_L7_PREUVE_HUMAINE.md:106-121` |
| L09-083 | Règle de transport « 0 ou 1 transport isométrique » (erronée) | X | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/95_L7_PREUVE_HUMAINE.md:79-82` |
| L09-084 | Repères serrés entiers exacts pour 99 (transposition d'Akiyama) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/96_METHODE_AKIYAMA.md:26-73` |
| L09-085 | Esquisse Akiyama en rang 48 sur Λ_L (non exécutée) | O | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/96_METHODE_AKIYAMA.md:75-95` |
| L09-086 | Formule locale exacte de k | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/97_K_ET_TORSION.md:103-110` |
| L09-087 | Table de rank₇ des 11 types d'étoiles | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/97_K_ET_TORSION.md:25-47` |
| L09-088 | Test « k = 10 » à une étoile : types exclus | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/97_K_ET_TORSION.md:157-159` |
| L09-089 | Calibrage BvLS du principe des sous-matrices | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/97_K_ET_TORSION.md:112-116` |
| L09-090 | Deux étoiles couplées : rang observé ≥ 14 (non prouvé) | H | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/97_K_ET_TORSION.md:163-172` |
| L09-091 | Test SAT « tous les τ_a de type (2,2,2) » tué au plafond mémoire | O | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/97_K_ET_TORSION.md:88-92` |
| L09-092 | Borne de Witt : k ≤ 34 (plus faible) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/97_K_ET_TORSION.md:94-98` |
| L09-093 | Dichotomie 7-adique des droites | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/99_VERROU_BOULES_DE_DROITES.md:76-77` |
| L09-094 | Distribution de d(L) et maximum par recuit | H | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/99_VERROU_BOULES_DE_DROITES.md:13` |
| L09-095 | Triplets de droites (ordre 9) : P ∈ [0,1155] | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/99_VERROU_BOULES_DE_DROITES.md:87-108` |
| L09-096 | Enraciné en une droite : une droite sans prisme ni barreau de prisme est permise | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/99_VERROU_BOULES_DE_DROITES.md:110-123` |
| L09-097 | Fonctions F₃ de somme nulle sur les droites (négatif, re-scopé) | H | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/99_VERROU_BOULES_DE_DROITES.md:126-129` |
| L09-098 | Heuristique du Γ tordu générique : P ≈ 126, k ≈ 30 | H | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/99_VERROU_BOULES_DE_DROITES.md:130-134` |
| L09-099 | Proposition de cohérence des 21 lemmes (forme forte retirée) | X | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/100_SYNTHESE_DES_LEMMES.md:191-207` |
| L09-100 | Corollaire C1 de la synthèse : k = 10 ⟹ m(e) ∈ {0,2} | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/100_SYNTHESE_DES_LEMMES.md:175-180` |
| L09-101 | Corollaire C2 : k ≤ 20 ⟹ droites 7-dégénérées ; k = 10 ⟹ d(L) ≥ 13 | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/100_SYNTHESE_DES_LEMMES.md:181-183` |
| L09-102 | Corollaires C3, C4, C6 de la synthèse | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/100_SYNTHESE_DES_LEMMES.md:184-189` |
| L09-103 | Diagnostic : le corpus est unilatéral (tous des planchers) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/100_SYNTHESE_DES_LEMMES.md:209-230` |
| L09-104 | L22 : seconde dérivation et forme du verrou | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/101_GENRE_K_MAJORE.md:26-69` |
| L09-105 | Structure 7-adique globale et locale | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:7-49` |
| L09-106 | Blocs d'arête : négatif | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:74-75` |
| L09-107 | Dichotomie L23 et fenêtre heuristique k ∈ {24,26,28} | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:69-83` |
| L09-108 | Reformulation par la matrice de Seidel (deux-graphe) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:114-130` |
| L09-109 | Lointain d'une droite : résidu R_L de rang k − 22 | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:132-145` |
| L09-110 | Conclusion d'étape : k = 28 invisible localement | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:147-162` |
| L09-111 | Groupe critique du 99 (Ducey et al.) | P | littérature | 2026-09-25 | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:92-96` |
| L09-112 | Réduction de Kneser en un point de Hamming | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:27-49` |
| L09-113 | Régimes extrêmes au point de Hamming exclus à la main | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:51-64` |
| L09-114 | Classification des holonomies de triangles de Kneser | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:66-77` |
| L09-115 | Exemple de « coupe » au point de Hamming (erroné) | R | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:146-156` |
| L09-116 | Modèle local autour d'un triangle de classes : 1 522 solutions | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:239-250` |
| L09-117 | Parité S₃ du fait C et absence de certificat de parité de degré 2 | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:181-190` |
| L09-118 | Réduction de L8 à la parité de 21 quantités Q_R (non générale) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:213-237` |
| L09-119 | Famille srg(1+2m², 2m, 1, 2) : m = 2, 11 seulement connus | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:159-165` |

**B1 — conway99-c1:main — notes 104–118**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-120 | Tissu de 11 grilles : réduction à 55 permutations (E) | P | Claude-structures | 2026-09-25 | `conway99-c1:main:notes/104_TISSU_DE_GRILLES.md:20-41` |
| L09-121 | Théorème A (tissu) : couplages tous anti ⟹ plan projectif d'ordre 10 | P | Claude-structures | 2026-09-25 | `conway99-c1:main:notes/104_TISSU_DE_GRILLES.md:43-64` |
| L09-122 | Théorème B et D (tissu) : régime iso et régime à deux classes exclus | P | Claude-structures | 2026-09-25 | `conway99-c1:main:notes/104_TISSU_DE_GRILLES.md:66-103` |
| L09-123 | Tissu, régime général : identités automatiques | O | Claude-structures | 2026-09-25 | `conway99-c1:main:notes/104_TISSU_DE_GRILLES.md:105-127` |
| L09-124 | Coclique de Hoffman : spectre du complément | P | Claude-structures | 2026-09-25 | `conway99-c1:main:notes/104_TISSU_DE_GRILLES.md:129-134` |
| L09-125 | L8 : preuve par le squelette de Fano (détails) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/105_L8_DEMONTRE_FANO.md:45-122` |
| L09-126 | Cas coupe au point de Hamming : impossible (preuve indépendante) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/105_L8_DEMONTRE_FANO.md:131-140` |
| L09-127 | Lemme spectral et lemme des composantes (point de Hamming) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/105_L8_DEMONTRE_FANO.md:142-156` |
| L09-128 | Intégralité p-adique d'ordre 8 : aucune condition | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/105_L8_DEMONTRE_FANO.md:162-163` |
| L09-129 | La voie 7-adique se ramène entièrement à la matrice générique G (négatif démontré) | P | Claude-structures | 2026-09-25 | `conway99-c1:main:notes/106_REDUCTION_7ADIQUE_A_G.md:7-36` |
| L09-130 | Quadrangle presque parfait (C2) | P | Claude-C2 | 2026-09-25 | `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L22.md:10-13` |
| L09-131 | Vecteurs imposés localement invisibles pour U (défaut de L22) | P | Claude-C2 | 2026-09-25 | `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L22.md:15-20` |
| L09-132 | Ensembles −4-serrés : seuls porteurs combinatoires connus du défaut de L22 | P | Claude-structures | 2026-09-25 | `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L22.md:22-32` |
| L09-133 | Conséquences à k = 28 pour les cocliques de Hoffman et ensembles serrés | P | Claude-structures | 2026-09-25 | `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L22.md:34-41` |
| L09-134 | Ensembles serrés en C2 | P | Claude-C2 | 2026-09-25 | `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L22.md:43-46` |
| L09-135 | Trois formulations équivalentes de la cible 7-adique (non des routes) | O | Claude-structures | 2026-09-25 | `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L22.md:48-52` |
| L09-136 | Lemme D1 : les grilles incomplètes ne sont jamais deux à deux sécantes | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/108_DEFAUTS_ET_COMPTAGE_DES_FENTES.md:33-65` |
| L09-137 | Lemme D2 et g(x) ≤ 17 | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/108_DEFAUTS_ET_COMPTAGE_DES_FENTES.md:67-88` |
| L09-138 | Limites du comptage des fentes | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/108_DEFAUTS_ET_COMPTAGE_DES_FENTES.md:99-127` |
| L09-139 | Torsion maximale : l'holonomie de L8 ne se transporte pas | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/109_COEUR_TORSION_MAXIMALE.md:17-47` |
| L09-140 | Identités du second ordre trop faibles (L14 non réfuté) | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/109_COEUR_TORSION_MAXIMALE.md:37-39` |
| L09-141 | Schéma des droites à P = 0 : (Y − 4)(Y + 17) = 0 (déjà connu) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/109_COEUR_TORSION_MAXIMALE.md:49-84` |
| L09-142 | Minkowski : vecteurs courts forcés mais non classables | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/110_ROUTES_CLOSES_ET_CODES_DES_DROITES.md:15-35` |
| L09-143 | Akiyama sur Λ_L : route close | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/110_ROUTES_CLOSES_ET_CODES_DES_DROITES.md:37-52` |
| L09-144 | Les codes des droites contiennent leur dual (p = 2, 3, 5) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/110_ROUTES_CLOSES_ET_CODES_DES_DROITES.md:54-88` |
| L09-145 | Correction de notes/102 §9 (droites intérieures) | X | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/110_ROUTES_CLOSES_ET_CODES_DES_DROITES.md:90-97` |
| L09-146 | La 7-spécialité exigée par L22 n'a rien d'anormal | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/110_ROUTES_CLOSES_ET_CODES_DES_DROITES.md:105-118` |
| L09-147 | L14 \|C\| = 2 : preuve détaillée (offre 4, demande 5) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/111_L14_C2_A_LA_MAIN.md:8-62` |
| L09-148 | Pour tout \|C\| : les deux torsions ont le même graphe de classes | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/111_L14_C2_A_LA_MAIN.md:64-82` |
| L09-149 | L14 \|C\| = 5 : bilans exacts sans jeu, sans contradiction | O | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/111_L14_C2_A_LA_MAIN.md:103-114` |
| L09-150 | Vers g(x) ≤ 16 : réduction à 20 configurations | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/112_VERS_G16_MOTIFS_A_QUATRE_DEFAUTS.md:8-80` |
| L09-151 | Transposition du contenu de C3 à C1 : no-go (R3) | P | Claude-structures | 2026-09-25 | `conway99-c1:main:notes/113_TRANSPOSITION_C3_CLOTURE.md:41-55` |
| L09-152 | R1, R2, R4 : genre local/global cohérent, variantes linéaires automatiques, somme de Gauss | P | Claude-structures | 2026-09-25 | `conway99-c1:main:notes/113_TRANSPOSITION_C3_CLOTURE.md:18-39` |
| L09-153 | R3 bis : le gain d'Eisenstein des orientations de droites n'a aucun spectre à ≤ 3 valeurs | P | Claude-C2 | 2026-09-25 | `conway99-c1:main:notes/113_TRANSPOSITION_C3_CLOTURE.md:57-70` |
| L09-154 | Graphe lointain d'une droite : spectre fixé par G(L) | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/114_LABO_EXPERIMENTAL_GRAPHE_LOINTAIN.md:19-38` |
| L09-155 | Graphes réels de valeurs propres {3,−4} : L22 sain | E | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/114_LABO_EXPERIMENTAL_GRAPHE_LOINTAIN.md:40-52` |
| L09-156 | Équilibre d'une droite, variance nulle et lemme E | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/114_LABO_EXPERIMENTAL_GRAPHE_LOINTAIN.md:54-72` |
| L09-157 | Droites équiangulaires : route close | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/114_LABO_EXPERIMENTAL_GRAPHE_LOINTAIN.md:76-77` |
| L09-158 | Lemme du triangle : T ⪯ 3I − P_∂ | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/115_LEMME_DU_TRIANGLE.md:16-51` |
| L09-159 | Lemme du triangle en torsion maximale : 22 % des configurations admissibles tuées | H | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/115_LEMME_DU_TRIANGLE.md:54-87` |
| L09-160 | Second sous-constituant et identités (P2) par blocs | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/116_SECOND_ORDRE_ET_FANO_TENDU.md:1-43` |
| L09-161 | Fano tendu : (F5) par variance nulle | P | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/116_SECOND_ORDRE_ET_FANO_TENDU.md:45-52` |
| L09-162 | Fano tendu : le témoin survit au niveau des blocs (conclusion corrigée) | R | Claude-C1 | 2026-09-25 | `conway99-c1:main:notes/116_SECOND_ORDRE_ET_FANO_TENDU.md:54-69` |
| L09-163 | (P2) linéarisé par types : infaisabilités certifiées | C | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/117_P2_PAR_TYPES_TORSION_MAXIMALE.md:19-48` |
| L09-164 | (P2) ⟺ repère ajusté dans un espace de Johnson de dimension 14 | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/117_P2_PAR_TYPES_TORSION_MAXIMALE.md:50-76` |
| L09-165 | Cellules antipodales : le témoin de Fano tendu meurt | C | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/117_P2_PAR_TYPES_TORSION_MAXIMALE.md:78-105` |
| L09-166 | Niveau paire × bloc : les 3 survivants « blocs + cellules » meurent | C | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/118_PAIRE_BLOC_ET_OBSTRUCTION_PSI.md:20-40` |
| L09-167 | Mécanisme cellcross (ablation) | E | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/118_PAIRE_BLOC_ET_OBSTRUCTION_PSI.md:42-48` |
| L09-168 | Fonctionnelle universelle Ψ_R au Fano tendu | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/118_PAIRE_BLOC_ET_OBSTRUCTION_PSI.md:50-73` |
| L09-169 | Ψ n'est pas un lemme à lui seul (retournements adverses) | E | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/118_PAIRE_BLOC_ET_OBSTRUCTION_PSI.md:74-92` |
| L09-170 | Strate des σ internes : un survivant indéterminé | O | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/118_PAIRE_BLOC_ET_OBSTRUCTION_PSI.md:94-103` |

**B2 — conway99-c1:main — notes 119–132**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-171 | Lemme P-Ψ (Fano tendu) | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/119_PSI_PAR_PAIRE_FANO_TENDU.md:8-56` |
| L09-172 | P-Ψ par droite : système affine sur F₂ ; 9 σ tendus morts | E | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/119_PSI_PAR_PAIRE_FANO_TENDU.md:63-92` |
| L09-173 | « Aucun sommet de Fano tendu » : ouvert | O | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/119_PSI_PAR_PAIRE_FANO_TENDU.md:94-102` |
| L09-174 | Vecteurs propres cellulaires forcés | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/120_TRIADES_ET_VECTEURS_PROPRES_CELLULAIRES.md:16-34` |
| L09-175 | Triades de doubles au Fano tendu (transposition du Théorème F de C2) | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/120_TRIADES_ET_VECTEURS_PROPRES_CELLULAIRES.md:36-70` |
| L09-176 | Point d'étape 26/09 : ce que l'analyse locale en torsion maximale a donné | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/121_POINT_D_ETAPE_26_09.md:13-24` |
| L09-177 | Composantes de K à P = 0 (Astra) | P | Astra | 2026-09-26 | `conway99-c1:main:notes/121_POINT_D_ETAPE_26_09.md:53-55` |
| L09-178 | Dérangement cerise/σ : réfutation re-scopée | O | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/121_POINT_D_ETAPE_26_09.md:43-44` |
| L09-179 | Lemme des différences de retournement (Fano tendu) | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/122_FANO_DIFFERENCES_DE_RETOURNEMENT.md:16-47` |
| L09-180 | Identité des parités de branche et P-Ψ réduite | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/122_FANO_DIFFERENCES_DE_RETOURNEMENT.md:53-92` |
| L09-181 | État du Fano tendu (26/09 soir) : cinq ingrédients à combiner | O | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/122_FANO_DIFFERENCES_DE_RETOURNEMENT.md:93-101` |
| L09-182 | Porte I_x à P = 0 : hexagones (Reimbayev) et H(x) = 12 936 | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/123_PORTE_IX_TORSION_MAXIMALE.md:7-58` |
| L09-183 | Lointain d'une droite : Φ_F = −7Π (complément de Schur réel) | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/124_LOINTAIN_D_UNE_DROITE_SCHUR.md:37-53` |
| L09-184 | Lointain mod 7 : rang₇ R_L = k − 22, cible du dossier n° 5 d'Astra | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/124_LOINTAIN_D_UNE_DROITE_SCHUR.md:20-35` |
| L09-185 | Cycles courts des graphes de droites : Σ_L c₄(G(L)) = S + 3P | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/125_CYCLES_COURTS_DES_GRAPHES_DE_DROITES.md:19-53` |
| L09-186 | Critère de maille ≥ 5 et lemme de Klein | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/125_CYCLES_COURTS_DES_GRAPHES_DE_DROITES.md:55-89` |
| L09-187 | Composantes (6,6) à P = S = 0 : 288 étiquetées, 15 types ; d(L) entre 2 et 8 | E | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/125_CYCLES_COURTS_DES_GRAPHES_DE_DROITES.md:90-110` |
| L09-188 | Corrections du JOURNAL (b231c36, d7cd060) et des échantillons « S = 0 » | X | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/125_CYCLES_COURTS_DES_GRAPHES_DE_DROITES.md:112-130` |
| L09-189 | L21 raffiné : k ≥ 22 + r(L) − r₀(L) | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:7-60` |
| L09-190 | À P = S = 0, une droite (6,6) force k ≥ 22 | E | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:66-85` |
| L09-191 | Extension à P = 0 (S quelconque) : (4,4,4) ⟹ k ≥ 20 ; (6,6) ⟹ k ≥ 22 ; (4,8) ⟹ k ≥ 22 sauf torsion équilibrée | E | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:86-99` |
| L09-192 | Résidu ρ(L) à k = 22, 24 et réduction à « (6,6) partout » | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:101-119` |
| L09-193 | Théorème conditionnel (NT) : k ≥ 18 et structure forcée à k = 18 | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:121-158` |
| L09-194 | Carte du programme 7-adique (26/09 fin de nuit) | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/127_CARTE_DU_PROGRAMME_7_ADIQUE.md:17-56` |
| L09-195 | Lemme R ((4,4,4)-rigidité) et corollaires | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/128_RIGIDITE_444.md:5-50` |
| L09-196 | k = 18 exclu sous NT (P quelconque) | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/128_RIGIDITE_444.md:51-78` |
| L09-197 | q:7 (C2) : g = rang₇(S − 3I) pair, g ≤ 20, β⁻ hyperbolique | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:6-36` |
| L09-198 | q:7 (C2) : boule impaire d'une droite-bloc et L23 dédoublé | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:38-72` |
| L09-199 | q:7 (C2) : g⁻ ∈ {16, 18, 20} | E | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:100-134` |
| L09-200 | q:7 (C2) : critère « l'involution meurt ssi Λ_{T,−4} est 7-isotrope » | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:141-151` |
| L09-201 | q:7 (C2) : résidu lointain impair et mineurs principaux | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:74-99` |
| L09-202 | q:7 et lemme de l'étoile libre de C2 : A111111 | E | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:162-184` |
| L09-203 | Motifs Σ ≠ ∅ de C2 : famille ancrée close | C | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/130_MOTIFS_SIGMA_ANCRES.md:6-16` |
| L09-204 | Lemme de la queue réactivé pour les motifs Σ ≠ ∅ | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/130_MOTIFS_SIGMA_ANCRES.md:184-188` |
| L09-205 | Identités Alt entre paires frères (C2) | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/130_MOTIFS_SIGMA_ANCRES.md:105-143` |
| L09-206 | Bloc plein (C2) : q:7 force g⁻ = 20 | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/130_MOTIFS_SIGMA_ANCRES.md:145-157` |
| L09-207 | Alt (C2) : rang de K ≤ 14 | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/131_ENTRELACEMENT_ALT_ET_RESIDUS_LOINTAINS.md:15-27` |
| L09-208 | Résidus lointains réels contre q:7 (C2) | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/131_ENTRELACEMENT_ALT_ET_RESIDUS_LOINTAINS.md:29-43` |
| L09-209 | Au plus un bloc A111111 quand Σ = ∅ (C2) | P | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/131_ENTRELACEMENT_ALT_ET_RESIDUS_LOINTAINS.md:45-54` |
| L09-210 | Composantes canoniques d'un bloc plein : aucune torsion 7 | E | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/131_ENTRELACEMENT_ALT_ET_RESIDUS_LOINTAINS.md:80-88` |
| L09-211 | Énoncé candidat : deux blocs pleins ne forment jamais une paire frère | H | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/131_ENTRELACEMENT_ALT_ET_RESIDUS_LOINTAINS.md:90-124` |
| L09-212 | Lignes rigides en un bloc plein et mort de 3K2_or14 par q:7 | E | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/131_ENTRELACEMENT_ALT_ET_RESIDUS_LOINTAINS.md:126-179` |
| L09-213 | g⁻ = 16 impossible (C2) : donc g⁻ ∈ {18, 20} | C | Claude-C1 | 2026-09-26 | `conway99-c1:main:notes/132_G16_IMPOSSIBLE.md:6-74` |

**C — conway99-c1:main — notes 133–154 (branche C2, ligne (C), rank-17 côté C1)**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-214 | q:7 par régimes à g⁻ ∈ {18,20} et recensement des 3 308 types de blocs | E | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/133_REGIMES_Q7_ET_U_SIGNE.md:5-50` |
| L09-215 | U signé : couche impaire sur le modèle d'orbite U de C2 | O | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/133_REGIMES_Q7_ET_U_SIGNE.md:52-74` |
| L09-216 | Lemme mono-bloc et identité générale des quadruplets ι (système local (i)–(iii)) | P | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/134_SYSTEME_LOCAL_IOTA_BLOC_PLEIN.md:6-137` |
| L09-217 | Secteur pair à q:7 : régimes inversés et g⁺ ≠ 14 | S | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/135_SECTEUR_PAIR_Q7.md:5-57` |
| L09-218 | Échelle des pivots | P | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/136_ECHELLE_DES_PIVOTS.md:6-62` |
| L09-219 | Ligne d'arrivée de C2 : un bloc lourd en toute configuration | P | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/137_LIGNE_D_ARRIVEE_C2.md:6-78` |
| L09-220 | Grille de relecture d'un argument « réseaux × 7 blocs » (avant le document de Sol) | H | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/138_GRILLE_DE_RELECTURE_RESEAUX_7_BLOCS.md:1-51` |
| L09-221 | Ligne (C) : repère de 51 vecteurs dans une enveloppe unimodulaire impaire de dim 24 | P | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/139_LIGNE_C_ENVELOPPES.md:9-21` |
| L09-222 | Ligne (C) : outils uniformes (M), (P), (E) | P | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/139_LIGNE_C_ENVELOPPES.md:23-40` |
| L09-223 | Ligne (C) : premières exclusions (9 ou 10 sur 156) | P | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/139_LIGNE_C_ENVELOPPES.md:42-62` |
| L09-224 | Ligne (C) : voisins de Niemeier, identité m(x) = r/8 − E(x), packing et connexité | P | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/140_LIGNE_C_PACKING_CONNEXITE.md:7-94` |
| L09-225 | Ligne (C) : lemme Z et étages h / y / u ; famille rigide | P | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/141_LIGNE_C_LEMME_Z_ETAGES.md:5-75` |
| L09-226 | Exclusion de l'enveloppe 132 (d₆⁴) | E | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/142_EXCLUSION_132_ET_CHAINE_Y_H.md:5-68` |
| L09-227 | Verdicts de l'étage h antérieurs au bug de bitsets (retirés) | X | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/142_EXCLUSION_132_ET_CHAINE_Y_H.md:52-58` |
| L09-228 | Famille rigide D₂ₘ ⊃ D_m² : identités de bloc, lemme π, lemme K, recensements | P | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/143_LEMME_PI_FAMILLE_D2M.md:6-227` |
| L09-229 | Triage des 135 réseaux ouverts de la ligne (C) | E | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/144_TRIAGE_OUVERTS.md:1-46` |
| L09-230 | Test décisif sur un réseau non rigide : 124 (d₈a₇²) | S | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/145_TEST_124_NON_RIGIDE.md:44-100` |
| L09-231 | Rank-17 switch : U′ = ℤ⁷ ⊥ V, 9 types de V, 1 272 points de départ | E | Claude-C1 | 2026-09-27 | `conway99-c1:main:notes/146_RANK17_YPAIRS.md:3-70` |
| L09-232 | Rank-17 pass 1 : E8²+ℤ #0, #1 exclus ; A11E6⁺ #0 PATTERN | E | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/146_RANK17_YPAIRS.md:72-121` |
| L09-233 | Rank-17 pass 2 : 59 des 1 272 types de y-paires exclus (COMPUTED) | E | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/147_RANK17_PASS2.md:90-118` |
| L09-234 | Rank-17 : l'épuisement entier des paires MOD4_FEASIBLE est infaisable (Knuth) | H | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/147_RANK17_PASS2.md:120-181` |
| L09-235 | Obstruction DC (classe duale courte) : coupure réelle mais petite (×2–3) | E | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/148_SHORT_DUAL_DC.md:1-40` |
| L09-236 | Couplage des sept étoiles (proposition Sol / utilisateur) : évaluation | P | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/149_COUPLAGE_SEPT_ETOILES.md:6-64` |
| L09-237 | Méta-fait : (A) et (B) ne sont protégés par aucun exemple connu | P | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/149_COUPLAGE_SEPT_ETOILES.md:45-51` |
| L09-238 | min K* ≥ 9/7 tue les 1 272 paires ; théorème de coupure 2\|5 (côté preuve de (B)) | P | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/150_ECHELLE_KSTAR_ET_COUPURE_2_5.md:7-131` |
| L09-239 | Programme R6 : J1b fermé, J1a types (i), (ii), (iv), (vi) morts | P | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/151_R6_PROGRAMME_J_CELLS.md:1-212` |
| L09-240 | R6 : nouveau vecteur propre entier en J1a (v) et principe général | P | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/151_R6_PROGRAMME_J_CELLS.md:302-359` |
| L09-241 | Route des triplets (6,8,8) abandonnée (données de couverture) | E | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/151_R6_PROGRAMME_J_CELLS.md:281-294` |
| L09-242 | R6 : J1a CLOS (énumération PSD exhaustive + complétion de coquille) | E | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/152_J1a_CLOSED_EXHAUSTIVE_PSD.md:1-83` |
| L09-243 | Conception d'un moteur pour les cellules coupées (J2, J3, R8 k=2, k=3) | O | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/153_CUT_CELLS_ENGINE_DESIGN.md:1-52` |
| L09-244 | Moteur de coupure 2\|5 (J2, R5) : mesures et changement de route | O | Claude-C1 | 2026-09-28 | `conway99-c1:main:notes/154_2x5_ENGINE_AND_ROUTE_CHANGE.md:1-126` |

**D1 — conway99-structures-lab:master — JOURNAL, REGISTRE, NOTE_S5, S8, S11, S12, ASTRA_CERTIFICAT**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-245 | Ouverture du labo « structures » et partage avec C1/C2 (25/09 nuit) | H | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:JOURNAL.md:4-6` |
| L09-246 | Règles de travail de l'utilisateur relayées au labo | H | utilisateur | 2026-09-25 | `conway99-structures-lab:master:JOURNAL.md:31-33` |
| L09-247 | S1 : L22 général par le genre de Λ_θ (genus_scan) | P | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:JOURNAL.md:7-9` |
| L09-248 | S5 : critère 2-adique (discriminant mod 4 des réseaux propres) | P | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:NOTE_S5_DISCRIMINANT_MOD4.md:9-44` |
| L09-249 | S5 : ensembles de paramètres exclus (tables de Brouwer) | E | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:NOTE_S5_DISCRIMINANT_MOD4.md:53-73` |
| L09-250 | S3 : L21 et L23 de C1 rejoués sur de vrais graphes | H | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:JOURNAL.md:15-18` |
| L09-251 | S6 : relecture du lemme de la queue de C2 et équilibre BBᵀ1_C | P | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:JOURNAL.md:19-20` |
| L09-252 | S7 : décompositions de K₇ en cycles et bloc S (tout-tordu) | E | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:JOURNAL.md:21-25` |
| L09-253 | S8.1 : le type tout-tordu (3⁵,6) est impossible (à la main) | P | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:NOTE_S8_TOUT_TORDU.md:47-71` |
| L09-254 | Lemmes S8.2 (orbite morte), S8.3 (Fano), S8.4 (complément CL), S8.5 (deux triangles disjoints) | P | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:NOTE_S8_TOUT_TORDU.md:88-136` |
| L09-255 | Système local exhaustif C0–C8 (tableau des types tout-tordus) | E | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:NOTE_S8_TOUT_TORDU.md:138-159` |
| L09-256 | S11 : tout-tordu à deux triangles sécants impossible (à la main) | P | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:NOTE_S11_DEUX_TRIANGLES_SECANTS.md:15-18` |
| L09-257 | S13 : PPE signé (types des doubles) | P | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:JOURNAL.md:70-77` |
| L09-258 | S14 : (P2) de C1 hors diagonale dans le cadre de C2 (210 identités d'orbites) | P | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:JOURNAL.md:81-89` |
| L09-259 | S15–S16 : modèle de configurations + (P2) sur le tout-tordu à 1 triangle (tests solveur) | S | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:105-129` |
| L09-260 | S17 : tout-tordu à 1 triangle impossible (certificats exacts) | C | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:130-137` |
| L09-261 | S19 : identité de second ordre au niveau des orbites Q² + Q = 12I + 4J − Sh | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:153-157` |
| L09-262 | S19 : tout-tordu sans triangle exclu ; « tout-tordu pur entièrement exclu » (portée : circuits simples) | C | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:201-223` |
| L09-263 | ERRATUM : « tout-tordu pur exclu » ne couvre que les circuits simples | X | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:873-879` |
| L09-264 | Contre-vérification indépendante de H-β (C2) | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:138-143` |
| L09-265 | S12 : vérification de notes/116 (P2, critère lointain, Fano tendu) | P | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:NOTE_S12_VERIF_C1_116.md:1-78` |
| L09-266 | S18 : certificat X19 de C1 vérifié | C | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:145-152` |
| L09-267 | S20 : certificats « cellules » et « paire × bloc » de C1 vérifiés | C | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:175-182` |
| L09-268 | Obstruction de rang cellcross au Fano tendu et noyau universel (recalculés) | E | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:231-239` |
| L09-269 | Fonctionnelle Ψ_R : I_R = 0 nécessaire au Fano tendu (S21) et lemme P-Ψ (S22) | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:250-259` |
| L09-270 | Ψ évitable par les retournements ; P-Ψ est un filtre exact, pas un lemme | H | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:262-264` |
| L09-271 | Idée « commutant » (tâche envisagée pour Astra) : close | E | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:267-268` |
| L09-272 | Dimension forcée : ≥ 5 fonctions constantes sur les cellules vecteurs propres de B (valeur 3) | P | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:297-308` |
| L09-273 | Route du dérangement (T ≡ 1) au Fano tendu : close | R | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:312-313` |
| L09-274 | Lemme des différences de retournement de C1 (vérifié à la main) | P | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:361-367` |
| L09-275 | Porte I_x (C1) : comptages et pont avec le graphe des carrés d'Astra | P | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:321-330` |
| L09-276 | Identités I_x de C1 : automatiques et déjà dans le corpus (correction des crédits) | P | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:419-427` |
| L09-277 | Bilan I_x (C1) : pas de certificat linéaire uniforme | H | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:454-458` |
| L09-278 | notes/125 de C1 (Σ_L c₄(G(L)) = S + 3P, Σ_L c₃ = 2P, lemme de Klein) : TIENT | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:562-569` |
| L09-279 | Lemme (4,4,4) de C1 (G(L) à P = 0, S = 0) : TIENT | P | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:510-515` |
| L09-280 | notes/128 (lemme R) et notes/126 §3 quater (NT ⟹ k ≥ 18) : TIENNENT | P | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:630-634` |
| L09-281 | Bilan 7-adique à P = 0 (notes/127) | O | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:635-639` |
| L09-282 | Remarque de C1 : droites à 3 composantes à k = 20 construction-complètes | P | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:680-685` |
| L09-283 | Projecteur lointain Φ_F = −7Π (notes/124) vérifié | P | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:473-482` |
| L09-284 | Dichotomie des sœurs et question (2,0)/(2,1) des carrés dis | O | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:275-288` |
| L09-285 | Rapport d'Astra, dossier 4 (carrés disjoints) | P | Astra | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:459-469` |
| L09-286 | 𝒫(Q̄) ⪰ 0 est impliqué par le PL d'orbites | P | Claude-C2 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:483-486` |
| L09-287 | Relecture de root_colmodel.py (C2) : aucune erreur de modélisation | E | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:525-543` |
| L09-288 | Pas de lemme purement local « pas de bloc A » (résultat négatif de C2) | S | Claude-C2 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:557-558` |
| L09-289 | Correction : objectif de phase 1 du PL racine non convergé | X | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:559-561` |
| L09-290 | C2 au niveau orbite : survivants du niveau paires tués | C | Claude-C2 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:355-360` |
| L09-291 | Décision de l'utilisateur (26/09) : campagne orbite de C2 ; état de C2 | H | utilisateur | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:412-418` |
| L09-292 | AD (NOTE_S28) : les 14 survivants AD2 meurent, balayage jusqu'à n_dd = 6 | C | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:730-742` |
| L09-293 | AD, bilan provisoire et « tout dis » | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:763-773` |
| L09-294 | Étoile libre sans pivot : le contenu n'est pas local | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:774-779` |
| L09-295 | NOTE_S27 (q:7) : g⁻ pair, g⁻ ≠ 22, g⁻ ∈ {18,20} dès qu'une droite-bloc est générique ; réseau N | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:691-705` |
| L09-296 | Dossier 6 d'Astra (relu) et g⁻ ∈ {16,18,20} ; bloc A ⟹ g⁻ = 20 | P | Astra | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:748-753` |
| L09-297 | Sol, A111111 (3,3) : signe de Witt juste, A33 mort ; lemme de Witt général ; g⁻ ≠ 16 | P | ChatGPT-Sol | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:819-826` |
| L09-298 | 3K₂, étape 1 : famille ancrée Σ ≠ ∅ morte | E | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:827-829` |
| L09-299 | Bloc plein (NOTE_S29) : ombres, rigidité, spectre de T_FF ; bloc plein ⟹ g = 20 | P | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:830-836` |
| L09-300 | Système local (i)+(ii)+(iii) : comptage heuristique et deux étapes | H | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:838-847` |
| L09-301 | Recompte indépendant des 156 classes à ≥ 6 pivots ; table complète 3 308 ; les 441 types de Sol | E | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:849-859` |
| L09-302 | Les 79 types : deux étapes, tri SAT, 33/79 certifiés DRAT | C | Claude-C2 | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:860-862` |
| L09-303 | Lemmes codés pour le SAT (--cuts, --digon, --path, --twist, --ident, --beta, --balance) | H | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:880-887` |
| L09-304 | Identité générale de C1 (notes/134 §8) relue et testée | P | Claude-C1 | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:902-906` |
| L09-305 | Deux blocs couplés pour T = K₇ (NOTE_S33) | S | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:889-899` |
| L09-306 | SEC sur la route PL des (0,6) : arbre de Farkas probablement hors de portée | H | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:918-934` |
| L09-307 | Ligne d'arrivée de C2 (27/09, 10 h 15) | P | Claude-C1 | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:938-946` |
| L09-308 | Lex-leader déclarable (spec_local.py) | E | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:952-962` |
| L09-309 | Route (C) de Sol : réduction aux 156 réseaux de Borcherds | P | ChatGPT-Sol | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:964-967` |
| L09-310 | S35 : les 156 réseaux construits explicitement ; correction de l'id 150 | C | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:968-969` |
| L09-311 | Critères de la route (C) relus ; lemme « décomposable » ; coupe de parité de Sol vide | P | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:970-978` |
| L09-312 | S36 : O₂₄ (id 0), 86/141 classes exclues par PL de classe entière | C | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:974-977` |
| L09-313 | Pipeline paires (y₁,y₂) → PL de repère → étage h : 132 et 115 fermés | C | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:987-993` |
| L09-314 | id 1 (a₁⁸) dans le cadre de Golay | E | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:997-999` |
| L09-315 | Pistes « tout d'un coup » écartées (27/09) | H | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:JOURNAL.md:1000-1002` |
| L09-316 | Certificat d'Astra (mission géométrique) vérifié | C | Astra | 2026-09-25 | `conway99-structures-lab:master:NOTE_ASTRA_CERTIFICAT.md:1-37` |
| L09-317 | Astra, dossier 2 : revêtement unique de degré 4 de K₇ avec λ = 1 ; σ témoin mort par P-Ψ | P | Astra | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:342-349` |
| L09-318 | Astra, dossier 3 : P-Ψ + admissibilité n'est pas un lemme de Fano complet ; revêtements sans prisme de degré ≥ 5 | P | Astra | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:401-411` |
| L09-319 | Astra, dossier 5 (NOTE_S24) : boule tordue exclue à k = 22 ; R = 0 et MR = 0 ⟹ SRG exacte | P | Astra | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:516-524` |
| L09-320 | Correction de l'heuristique du dossier 5 (Ξ) | X | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:470-472` |
| L09-321 | Astra, « étoiles d'ombres » (NOTE_S26) et lien de signe | P | Astra | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:584-592` |
| L09-322 | Étoile complète à k = 22 : calibration 42/42 et obstruction « de Green » | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:593-599` |
| L09-323 | Structure de l'obstruction de l'étoile : surdétermination, pas de couplage | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:643-655` |
| L09-324 | Astra, suivi n° 4 : la piste (α) de C1 est réfutée | R | Astra | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:640-642` |
| L09-325 | Espace des boules à P = 0 : examen exhaustif écarté | H | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:667-673` |
| L09-326 | Famille srg(2m²+1, 2m, 1, 2) : invariants de 9 et 243 ; 7 \| t | E | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:570-583` |
| L09-327 | Revue de littérature : unicité de srg(243,22,1,2) OUVERTE ; la règle qui échoue à 99 = propriété de grille | O | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:600-604` |
| L09-328 | Lemme unique par 243 : pas de transfert direct 3-adique → 7-adique | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:613-617` |
| L09-329 | Bilan stratégique (structures) : jalon Aut(Γ) = 1 | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:674-679` |
| L09-330 | Sol, rapports « supports courts » et « Wagner » | P | ChatGPT-Sol | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:755-758` |
| L09-331 | Feuille de problèmes ouverts pour Sol et Astra | O | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:786-791` |
| L09-332 | État de C2 au 26/09 fin de soirée (verrou unique) | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:JOURNAL.md:793-815` |

**D2 — conway99-structures-lab:master — NOTE_S17 à S38**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-333 | S17 : forme des certificats et réserves de portée | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S17_COEUR_CERTIFIE.md:39-56` |
| L09-334 | S17 §2.2 : sans triangle, (P2) par paires ne suffit pas | S | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S17_COEUR_CERTIFIE.md:92-114` |
| L09-335 | Identité d'orbites : faits annexes et spectre de Q (cadre C2) | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S17_COEUR_CERTIFIE.md:129-139` |
| L09-336 | S21 §5 : critère exact de P-Ψ par droite | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S21_PSI_STRUCTUREL.md:122-143` |
| L09-337 | P-Ψ : 2 à 6 droites sur 7 sans réglage (observation) ; à démontrer pour tout σ tendu | H | Claude-C1 | 2026-09-26 | `conway99-structures-lab:master:NOTE_S21_PSI_STRUCTUREL.md:118-120` |
| L09-338 | NOTE_S23 : cadre de C2 avec preuves courtes ; lemme « A est dis » | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S23_ENONCE_DOSSIER4.md:8-94` |
| L09-339 | NOTE_S23 §5 : réduction à cinq supports (Schur sur 𝒫) | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S23_ENONCE_DOSSIER4.md:95` |
| L09-340 | NOTE_S24 §1 et §4 : portée de l'exclusion de la boule et lemme des ≤ 6 ombres | P | Astra | 2026-09-26 | `conway99-structures-lab:master:NOTE_S24_ASTRA_DOSSIER5.md:8-25` |
| L09-341 | NOTE_S25 §1 : arithmétique de la famille ; le côté 7-adique | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S25_FAMILLE_9_243.md:7-18` |
| L09-342 | NOTE_S25 §5 : rigidité de Godsil–McKay de la famille | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S25_FAMILLE_9_243.md:56-75` |
| L09-343 | NOTE_S25 §4 : les règles vraies à 9 et 243 qui échouent à 99 sont toutes déjà prouvées | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S25_FAMILLE_9_243.md:41-54` |
| L09-344 | NOTE_S25 §7 : littérature sur 243 et Aut(Γ₉₉) | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S25_FAMILLE_9_243.md:85-100` |
| L09-345 | NOTE_S26 §3 : composantes 4+4+4 et compatibilité Astra/C1 | E | Astra | 2026-09-26 | `conway99-structures-lab:master:NOTE_S26_ASTRA_ETOILES.md:39-48` |
| L09-346 | NOTE_S27 §1–3 : genre sous l'involution (détails) | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S27_INVOLUTION_GENRE_7ADIQUE.md:9-50` |
| L09-347 | NOTE_S27 §5 et §7 : rangs et signes des droites-blocs (statistiques) | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S27_INVOLUTION_GENRE_7ADIQUE.md:52-88` |
| L09-348 | NOTE_S27 §8 : histogramme exhaustif des rangs de droite-bloc ; g⁻ ≠ 14 | E | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S27_INVOLUTION_GENRE_7ADIQUE.md:97-107` |
| L09-349 | NOTE_S28 §1 : équilibre par composante (forme générale) et fermeture des classes ancrées | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S28_AD_NIVEAU_PAIRES.md:6-34` |
| L09-350 | NOTE_S28 : balayage AD par n_dd (tableau) et écart de comptage | C | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S28_AD_NIVEAU_PAIRES.md:117-126` |
| L09-351 | NOTE_S28 §7 : lemme (★) de C2 re-dérivé ; l'étoile totalement libre résiste à tout | P | Claude-C2 | 2026-09-26 | `conway99-structures-lab:master:NOTE_S28_AD_NIVEAU_PAIRES.md:170-192` |
| L09-352 | NOTE_S29 §2 : critère de rigidité d'une orbite ancrée au bloc plein | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:32-45` |
| L09-353 | Correction NOTE_S29 : une orbite rigide n'a pas \|r_f\|² = 0 | X | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:67-69` |
| L09-354 | NOTE_S29 §6 : comptage heuristique du système local et tests agrégés | H | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:89-100` |
| L09-355 | NOTE_S29 §6 : (i)+(ii) ⟺ double couverture orthogonale du graphe cocktail CP₆ ; lemme mono-bloc | P | Claude-C1 | 2026-09-27 | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:102-128` |
| L09-356 | Contrôle positif BvLS du système local : valide mais dégénéré | H | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:136-150` |
| L09-357 | NOTE_S29 §8 : portée réaliste de la piste locale | H | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:152-165` |
| L09-358 | NOTE_S29 §9 : recompte des pivots ; digone ancré et bloc chemin | P | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:167-189` |
| L09-359 | NOTE_S33 : couplage de deux blocs et CROSS (détails démontrés) | P | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:NOTE_S33_DEUX_BLOCS_TK7.md:15-95` |
| L09-360 | NOTE_S38 : état au 27/09 14 h 30 et pistes pour conclure | O | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:NOTE_S38_ETAT_ET_PISTES.md:1-27` |

**D3 — conway99-structures-lab — astra/, famille/, involution/, ad/, logs/ (carnet C2), branche ordre 7**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-361 | Astra, dossier 6 : min Λ₋₄⁻ ≥ 8 et g⁻ ≥ 12 (g⁻ = 8, 10 exclus) | P | Astra | 2026-09-26 | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER6.md:1-21` |
| L09-362 | Astra, dossier 6 : min N* ≥ 8/7 et réduction au déterminant 49 | P | Astra | 2026-09-26 | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER6.md:16-21` |
| L09-363 | Astra, dossier 6 : vecteurs de norme 2 (deux profils) et précision sur « 7-isotrope » | P | Astra | 2026-09-26 | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER6.md:337-353` |
| L09-364 | Astra, dossier 6 : ce qui reste | O | Astra | 2026-09-26 | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER6.md:12-13` |
| L09-365 | Astra, dossier 5 et suite : énoncés et ce qui reste ouvert (texte d'Astra) | P | Astra | 2026-09-26 | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER5.md:5-9` |
| L09-366 | Astra, suivi n° 4 et audit S5 (texte d'Astra) | E | Astra | 2026-09-26 | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_SUIVI4_ET_AUDIT_S5.md:1-20` |
| L09-367 | Sol, « supports courts » : vecteurs de norme ≤ 10 de L_T | P | ChatGPT-Sol | 2026-09-26 | `conway99-structures-lab:master:astra/RAPPORT_SOL_SUPPORTS_COURTS.md:1-17` |
| L09-368 | Sol : contre-test sur les ombres (conjecture 33) et borne des deux cartes | P | ChatGPT-Sol | 2026-09-26 | `conway99-structures-lab:master:astra/RAPPORT_SOL_SUPPORTS_COURTS.md:206-260` |
| L09-369 | Sol, « Wagner » : à P = 0 tout support Wagner de norme 8 utilise les sept blocs | C | ChatGPT-Sol | 2026-09-26 | `conway99-structures-lab:master:astra/RAPPORT_SOL_WAGNER.md:1-46` |
| L09-370 | Dossier 6 envoyé à Astra : énoncé autonome du q:7 de l'involution | P | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:astra/DOSSIER6_INVOLUTION_7ADIQUE.md:24-76` |
| L09-371 | Feuille « trois problèmes ouverts » (involution) pour Sol et Astra | O | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:astra/PROBLEMES_OUVERTS_INVOLUTION.md:1-103` |
| L09-372 | Problème fini « bloc plein » pour Sol | O | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:astra/PROBLEME_BLOC_PLEIN_POUR_SOL.md:1-59` |
| L09-373 | Pour Sol : g⁻ ≠ 16 sans P = 0 (détail) et classification des 3 308 types | P | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:astra/POUR_SOL_G18_G20_NOS_NOMBRES.md:6-15` |
| L09-374 | Pour Sol : régimes de Witt à g = 18 et g = 20 | P | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:astra/POUR_SOL_G18_G20_NOS_NOMBRES.md:51-98` |
| L09-375 | Échelle des pivots ⟹ réductions de C2 (énoncé pour Sol) | P | Claude-C1 | 2026-09-27 | `conway99-structures-lab:master:astra/POUR_SOL_G18_G20_NOS_NOMBRES.md:100-113` |
| L09-376 | Suivis n° 3 et n° 4 du dossier 5 (envoyés à Astra) | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:astra/SUIVI3_DOSSIER5.md:1-71` |
| L09-377 | Revue de littérature (agent) : faits clés | H | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:famille/REVUE_LITTERATURE_9_243.md:1-72` |
| L09-378 | LEMMA_SCOPES : portée des lemmes des modèles locaux (dis, Σ ≠ ∅) | P | Claude-structures | 2026-09-27 | `conway99-structures-lab:master:involution/LEMMA_SCOPES.md:1-37` |
| L09-379 | Lemme --balance (équilibre par orbite de ⟨π, μ, τ⟩) | P | Claude-C2 | 2026-09-27 | `conway99-structures-lab:master:involution/LEMMA_SCOPES.md:19` |
| L09-380 | Handoffs du balayage AD et du bloc plein (calcul délégué) | O | Claude-structures | 2026-09-26 | `conway99-structures-lab:master:ad/HANDOFF_AD_SWEEP.md:1-22` |
| L09-381 | Carnet C2 (25/09) : structure locale de l'involution | P | Claude-C2 | 2026-09-25 | `conway99-structures-lab:master:logs/c2_programme.md:21-34` |
| L09-382 | Carnet C2 : Théorème A (corrigé après l'audit d'Astra) et Théorème B | P | Claude-C2 | 2026-09-25 | `conway99-structures-lab:master:logs/c2_programme.md:36-89` |
| L09-383 | Carnet C2 : version initiale du Théorème A (e′ pair) retirée | X | Claude-C2 | 2026-09-25 | `conway99-structures-lab:master:logs/c2_programme.md:37-38` |
| L09-384 | Carnet C2 : impasses consignées (points fixes, 2-adique, 7 \| k, désordre 7-adique) | H | Claude-C2 | 2026-09-25 | `conway99-structures-lab:master:logs/c2_programme.md:71-96` |
| L09-385 | Carnet C2 : Théorème D (« tous les carrés frères » impossible) et Théorème D′ (aucun sommet plat) | P | Claude-C2 | 2026-09-25 | `conway99-structures-lab:master:logs/c2_programme.md:102-128` |
| L09-386 | Carnet C2 : graphe N des paires non frères ; tout N à au plus 6 arêtes est exclu | P | Claude-C2 | 2026-09-25 | `conway99-structures-lab:master:logs/c2_programme.md:129-292` |
| L09-387 | Carnet C2 : Théorème F (modèle de Fano impossible) et budget μ local 16.1 | P | Claude-C2 | 2026-09-25 | `conway99-structures-lab:master:logs/c2_programme.md:318-422` |
| L09-388 | Carnet C2 : règle des zéros (17.3–17.4) et Théorème P (configurations ancrées régulières) | P | Claude-C2 | 2026-09-25 | `conway99-structures-lab:master:logs/c2_programme.md:423-534` |
| L09-389 | Carnet C2 : Théorème 24.3 (aucune configuration ancrée n'existe) | P | Claude-C2 | 2026-09-25 | `conway99-structures-lab:master:logs/c2_programme.md:742-803` |
| L09-390 | Carnet C2 : réductions à des résultats connus et transposition de la démarche de C3 | H | Claude-C2 | 2026-09-25 | `conway99-structures-lab:master:logs/c2_programme.md:612-741` |
| L09-391 | Exclusion sans ordinateur des automorphismes d'ordre 7 (brouillon du 02/10) | P | Claude-cloud | 2026-10-02 | `conway99-structures-lab:origin/claude/chat-session-09hf0k:ordre7/tex/order7.tex:37-89` |
| L09-392 | logs/srgw.txt : texte du livre de Brouwer–Van Maldeghem | H | Claude-structures | 2026-09-25 | `conway99-structures-lab:master:logs/srgw.txt:1-12` |

**E — conway99-rank17:master**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-393 | Handoff GPT-Pro du 27/09 : statut déclaré | H | GPT-Pro | 2026-09-27 | `conway99-rank17:master:README.md:5-9` |
| L09-394 | Saturation de H et circuit binaire (Prop. 2.1) | P | GPT-Pro | 2026-09-27 | `conway99-rank17:master:RANK17_HANDOFF.md:27-47` |
| L09-395 | Théorème 3.1 : le switch de rang 17 | P | GPT-Pro | 2026-09-27 | `conway99-rank17:master:RANK17_HANDOFF.md:51-97` |
| L09-396 | Prop. 4.1 et 5.1 : K de rang 15, det 49 ; ρ : E₇ → K/2K injective | P | GPT-Pro | 2026-09-27 | `conway99-rank17:master:RANK17_HANDOFF.md:99-160` |
| L09-397 | Théorème 6.1 : inégalité d'énergie de parité (PE) et corollaires ℤ¹⁷ | P | GPT-Pro | 2026-09-27 | `conway99-rank17:master:RANK17_HANDOFF.md:164-223` |
| L09-398 | §8 : témoin court dans le dual des candidats | P | GPT-Pro | 2026-09-27 | `conway99-rank17:master:RANK17_HANDOFF.md:270-276` |
| L09-399 | §9 : preuve indépendante de B′ par sommes de Gauss | P | GPT-Pro | 2026-09-27 | `conway99-rank17:master:RANK17_HANDOFF.md:278-338` |
| L09-400 | §10 : preuve complète de min N* ≥ 8/7 | P | GPT-Pro | 2026-09-27 | `conway99-rank17:master:RANK17_HANDOFF.md:340-364` |
| L09-401 | §11 et §12 : identités thêta et coupes spectrales (négatif) | H | GPT-Pro | 2026-09-27 | `conway99-rank17:master:RANK17_HANDOFF.md:366-393` |
| L09-402 | §7 : apprentissage de coupes LP conditionnelles exactes (méthode) | P | GPT-Pro | 2026-09-27 | `conway99-rank17:master:RANK17_HANDOFF.md:225-268` |
| L09-403 | Organisation de l'équipe rank-17 (27–28/09) | H | Claude-structures | 2026-09-27 | `conway99-rank17:master:README_TEAM.md:11-25` |
| L09-404 | Lemmes L1–L4, M1, M2, PE de la route rank-17 | P | Claude-structures | 2026-09-27 | `conway99-rank17:master:README_TEAM.md:26-36` |
| L09-405 | ℤ¹⁷ paire 7 : EXCLUE (COMPUTED) | E | Claude-structures | 2026-09-28 | `conway99-rank17:master:Z17_FINDINGS.md:3-6` |
| L09-406 | Mécanismes de mort sur ℤ¹⁷ (PATTERN) et correction « purement ℤ₄ » | H | Claude-structures | 2026-09-28 | `conway99-rank17:master:Z17_FINDINGS.md:8-31` |
| L09-407 | Test mod 4 exact (Z4, 21 bits) | E | Claude-structures | 2026-09-28 | `conway99-rank17:master:Z17_FINDINGS.md:42-55` |
| L09-408 | Correction du taux de mort Z4 (biais DFS) et retrait d'une mesure | X | Claude-structures | 2026-09-28 | `conway99-rank17:master:Z17_FINDINGS.md:74-84` |
| L09-409 | Échelle ℤ¹⁷ (Knuth) : les paires 1 et 2 hors de portée | H | Claude-structures | 2026-09-28 | `conway99-rank17:master:Z17_FINDINGS.md:99-124` |
| L09-410 | Règles d'étoile d'origine graphe de Sol (R1–R3) | P | ChatGPT-Sol | 2026-09-28 | `conway99-rank17:master:Z17_FINDINGS.md:138-153` |
| L09-411 | Lemme DC de Sol (classe duale courte) sur ℤ¹⁷ | P | ChatGPT-Sol | 2026-09-28 | `conway99-rank17:master:Z17_FINDINGS.md:86-97` |
| L09-412 | Théorème de Sol min K* ≥ 5/7 : 492/1 272 y-paires exclues | P | ChatGPT-Sol | 2026-09-28 | `conway99-rank17:master:GPT_FOLLOWUP_MINK.md:3-11` |
| L09-413 | Échelle des minima duaux : min K* ≥ 9/7 tuerait les 1 272 | E | Claude-C1 | 2026-09-28 | `conway99-rank17:master:GPT_FOLLOWUP_MIN97.md:3-9` |
| L09-414 | Obligation de preuve de C2 : chaîne F1–F13 et lacune R6 ∧ R8 | O | Claude-C1 | 2026-09-28 | `conway99-rank17:master:PROOF_OBLIGATION.md:102-174` |
| L09-415 | Dictionnaire F9 : vecteurs duaux courts ↔ vecteurs propres entiers du graphe | P | Claude-C1 | 2026-09-28 | `conway99-rank17:master:PROOF_OBLIGATION.md:139` |
| L09-416 | Remarque k = 0 : min N* ≥ 8/7 ferme J0 et k = 0 de R7 | P | Claude-C1 | 2026-09-28 | `conway99-rank17:master:PROOF_OBLIGATION.md:208-213` |
| L09-417 | Partition des 1 272 classes par V (D.1) | E | Claude-C1 | 2026-09-28 | `conway99-rank17:master:PROOF_OBLIGATION.md:219-235` |
| L09-418 | Quels échelons sont nécessaires (D.3) | E | Claude-C1 | 2026-09-28 | `conway99-rank17:master:PROOF_OBLIGATION.md:270-297` |
| L09-419 | Indices que la conjecture C2 pourrait être fausse ou sous-contrainte (F) | H | Claude-C1 | 2026-09-28 | `conway99-rank17:master:PROOF_OBLIGATION.md:340-373` |
| L09-420 | Route (C) déclarée « remplacée » par le rank-17 (28/09) | H | Claude-C1 | 2026-09-28 | `conway99-rank17:master:PROOF_OBLIGATION.md:195` |
| L09-421 | Système complet d'axiomes (N, D) de l'involution | P | Claude-structures | 2026-09-28 | `conway99-rank17:master:TARGETS_AB_STRUCTURES.md:3-22` |
| L09-422 | Ansätze symétriques pour un modèle de N : tous morts | P | Claude-structures | 2026-09-28 | `conway99-rank17:master:TARGETS_AB_STRUCTURES.md:24-39` |
| L09-423 | Cible B au niveau du graphe (coupure 2\|5) : J ∈ {8, 4, 0} | P | Claude-structures | 2026-09-28 | `conway99-rank17:master:TARGETS_AB_STRUCTURES.md:41-64` |
| L09-424 | R8, k = 0 impossible | P | Claude-structures | 2026-09-28 | `conway99-rank17:master:TARGETS_AB_STRUCTURES.md:120-177` |
| L09-425 | R8, k = 1 : réductions (T1–T5), ouvert | O | Claude-structures | 2026-09-28 | `conway99-rank17:master:TARGETS_AB_STRUCTURES.md:179-271` |
| L09-426 | Test d'entrelacement (sous-matrice principale) : nouvel outil global | P | Claude-structures | 2026-09-28 | `conway99-rank17:master:TARGETS_AB_STRUCTURES.md:273-303` |
| L09-427 | Moteur wfe par classe : construit, validé, en pause | E | Claude-structures | 2026-09-28 | `conway99-rank17:master:wfe/README.md:1-72` |
| L09-428 | Données R6 (28/09) : pas de paire liée n=6, triplets courts | E | Claude-C1 | 2026-09-28 | `conway99-rank17:master:r6_data/RESULTS_28_09.md:1-31` |
| L09-429 | R8, k = 3 : classes de signes des témoins | E | Claude-C2 | 2026-09-28 | `conway99-rank17:master:r8k3/README.md:1-31` |
| L09-430 | Théorème d'Astra (29/09) : fermeture par racine caractéristique | P | Astra | 2026-09-29 | `conway99-rank17:master:r17_char/ASTRA_PROOF_29_09.md:1-248` |
| L09-431 | Test caractéristique (C2) : 228 des 751 classes ouvertes fermées | C | Claude-C2 | 2026-09-29 | `conway99-rank17:master:r17_char/README.md:1-35` |
| L09-432 | Paquet de Sol Type 0 / Type II (29/09) : parité caractéristique et ancres | P | ChatGPT-Sol | 2026-09-29 | `conway99-rank17:master:sol_type02/PROOF.md:8-21` |
| L09-433 | Coquille caractéristique minimale par classe (523 classes non-ℤ¹⁷) | E | Claude-C1 | 2026-09-29 | `conway99-rank17:master:GPT_PROMPT_TYPE0_TYPE2.md:9-19` |
| L09-434 | Système V-libre complet (N, π) équivalent au graphe avec involution | P | Claude-C1 | 2026-09-29 | `conway99-rank17:master:GPT_FOLLOWUP_TYPE0_NEXT.md:8-45` |
| L09-435 | evenframe : route du secteur pair au cœur dur (k = 28) | H | Claude-structures | 2026-10-01 | `conway99-rank17:master:evenframe/README.md:1-145` |
| L09-436 | PARADIGM_BREAK : dix représentations du cas involution, toutes « collapsées » sauf deux | H | Claude-structures | 2026-10-01 | `conway99-rank17:master:paradigm/PARADIGM_BREAK.md:1-135` |
| L09-437 | ATTRACTOR_LOG : 14 dérives vers des théories familières | H | Claude-structures | 2026-10-01 | `conway99-rank17:master:paradigm/ATTRACTOR_LOG.md:1-30` |
| L09-438 | Données r8k1 (comptages préliminaires de l'énumérateur R8 k=1) | O | Claude-structures | 2026-09-28 | `conway99-rank17:master:r8k1/count_all.txt:1` |
| L09-439 | Spécification du moteur au niveau des vecteurs (SPEC_ENGINE) | P | Claude-structures | 2026-09-28 | `conway99-rank17:master:SPEC_ENGINE.md:1-63` |
| L09-440 | Plan de recherche du sous-cas V = ℤ¹⁷ (Z17_SEARCH_DESIGN) | P | Claude-structures | 2026-09-27 | `conway99-rank17:master:Z17_SEARCH_DESIGN.md:1-39` |
| L09-441 | Question M1/M2 (couche de relèvement) posée au GPT : observations sur ℤ¹⁷ paire 0 | H | Claude-structures | 2026-09-28 | `conway99-rank17:master:GPT_PROMPT_M1M2.md:1-43` |

**F — Dossier Astra du Bureau (27/09), campagne BvLS (11/10), dossiers_externes/**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-442 | Dossier CONWAY_ASTRA_27_09_2026_0836 : contenu et identité de l'auteur | H | Astra | 2026-09-27 | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/LIRE_D_ABORD_POUR_CLAUDE.md:1-18` |
| L09-443 | Astra 27/09 : les 42 racines engendrent N sur les entiers (Γ42 = N) | P | Astra | 2026-09-27 | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:5-9` |
| L09-444 | Astra 27/09 : piège de coque ; toute enveloppe contenant D8³ exclue ; D11 exclu | P | Astra | 2026-09-27 | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:9-12` |
| L09-445 | Astra 27/09 : D6⁴, six blocs fractionnaires dans une même paire impossibles ; coupe 4+2 | P | Astra | 2026-09-27 | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:12-13` |
| L09-446 | Astra 27/09 : enveloppes sans racines ⟹ code binaire [24,12,8] forcé | P | Astra | 2026-09-27 | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:14-15` |
| L09-447 | Astra 27/09 : coupes D4⁶/cycle6 (231/256 familles fermées) et sept octades de petit rang | P | Astra | 2026-09-27 | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:15-17` |
| L09-448 | Astra 27/09 : bilan — g⁻ = 18 et 20 restent ouverts globalement | O | Astra | 2026-09-27 | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:18` |
| L09-449 | ETAT_REPRISE_ACTUEL : historique des reprises du 27/09 (02 h 49 → 08 h 36) | H | Astra | 2026-09-27 | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/ETAT_REPRISE_ACTUEL.md:3-331` |
| L09-450 | Campagne Astra « BvLS après Paley » (11/10) : coordination | H | Astra | 2026-10-11 | `conway99-c1:origin/main:research/astra_bvls_boundary_20261011/COORDINATION.md:1-17` |
| L09-451 | BvLS : reconstruction à bord libéré — rigidité (deux prismes libérés) | E | Astra | 2026-10-11 | `conway99-c1:origin/main:dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/RESULTATS.md:5-17` |
| L09-452 | Index des dossiers externes (ChatGPT) versés le 12/10 | H | Claude-cloud | 2026-10-12 | `conway99-c1:origin/main:dossiers_externes/INDEX.md:1-49` |
| L09-453 | Hoffman (11/10) : designs cycliques et one-rotational exclus pour une coclique de 22 | E | ChatGPT-externe | 2026-10-11 | `conway99-c1:origin/main:dossiers_externes/HOFFMAN_UPDATE_20261011/README.md:13-18` |
| L09-454 | K7 partiel (12/10) : résultats démontrés, pas de preuve de K7 | P | ChatGPT-externe | 2026-10-12 | `conway99-c1:origin/main:dossiers_externes/C1_K7_RESULTATS_PARTIELS/README.md:1-28` |
| L09-455 | Paley(25) : reconstruction exacte et apparition de l'asymétrie (11/10) | E | ChatGPT-externe | 2026-10-11 | `conway99-c1:origin/main:dossiers_externes/PALEY_ASYMETRIE_DOSSIER/README.md:6-35` |

**G1 — conway99-c1:origin/main — AGENTS.md (journal de Codex), CLAUDE.md, PASSATION, RECHERCHE_ACTIVE**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-456 | Consigne permanente du 09/10 : exploration, lemmes et théorèmes de réduction | H | utilisateur | 2026-10-09 | `conway99-c1:origin/main:AGENTS.md:2035-2073` |
| L09-457 | Consignes du 14/10 : comprendre l'asymétrie ; deux chercheurs sans audits croisés | H | utilisateur | 2026-10-14 | `conway99-c1:origin/main:AGENTS.md:1920-1940` |
| L09-458 | Passation C1 du 07/10 (session cloud, branche claude/v7-simultaneous) | H | Claude-cloud | 2026-10-07 | `conway99-c1:origin/main:PASSATION_C1_2026-10-07.md:1-49` |
| L09-459 | RECHERCHE_ACTIVE_C1.md : journal actif de Codex (09/10) | H | Codex | 2026-10-09 | `conway99-c1:origin/main:RECHERCHE_ACTIVE_C1.md:1-30` |
| L09-460 | V15 (14/10) : réduction de complétion à rang un sur un bord43 | P | Codex | 2026-10-14 | `conway99-c1:origin/main:AGENTS.md:1942-1961` |
| L09-461 | Théorème global (16/10) : T + U = 7Π sur les 84 étiquettes | P | Codex | 2026-10-16 | `conway99-c1:origin/main:AGENTS.md:1104-1110` |
| L09-462 | rang K = 21 − c(l) et réduction ν(T44) = c(l) + 2 + corank(Q) | P | Codex | 2026-10-16 | `conway99-c1:origin/main:AGENTS.md:733-738` |
| L09-463 | Témoin précis 15 (global_star15) prouvé non prolongeable | P | Codex | 2026-10-16 | `conway99-c1:origin/main:AGENTS.md:886-892` |
| L09-464 | Cœur30 fermé par projection globale 84 (CP-SAT) | S | Codex | 2026-10-16 | `conway99-c1:origin/main:AGENTS.md:973-978` |
| L09-465 | Théorème : P ≤ 852 ⟹ au moins 18 droites t ≤ 7 et au moins 254 blocs non-grille | P | Codex | 2026-10-15 | `conway99-c1:origin/main:AGENTS.md:1304-1312` |
| L09-466 | Clôture des relations de noyau retenues par les composantes des réseaux deux-étoiles | P | Codex | 2026-10-15 | `conway99-c1:origin/main:AGENTS.md:1268-1276` |
| L09-467 | Théorème sans symétrie (S20 extérieur) : coupe stricte | P | Codex | 2026-10-15 | `conway99-c1:origin/main:AGENTS.md:1410-1416` |
| L09-468 | Réfutations du 15/10 : ODD9, SUM14, KER-SYM universelles ; « une seule saturation » | R | Codex | 2026-10-15 | `conway99-c1:origin/main:AGENTS.md:1353-1360` |
| L09-469 | Famille locale ⟨z,hM⟩ exclue ; min c = 2 prouvé ; « absence de relations mixtes » fausse | S | Codex | 2026-10-15 | `conway99-c1:origin/main:AGENTS.md:1488-1490` |
| L09-470 | Borne de racine choisie Σ t(l) ≤ 51 et 79 gabarits (16/10) | S | Codex | 2026-10-16 | `conway99-c1:origin/main:AGENTS.md:677-705` |
| L09-471 | Bug OR-Tools 9.15 (domain[-1]) : verdicts retirés le 18/10 | X | Codex | 2026-10-18 | `conway99-c1:origin/main:AGENTS.md:657-662` |
| L09-472 | Certificat entier 3P + 4G ≤ 2772 ; racine pondérée 9s + 8g | C | Codex | 2026-10-18 | `conway99-c1:origin/main:AGENTS.md:646-656` |
| L09-473 | 18/10, 16 h 36 : branche « minimum global c(L) ≥ 4 » fermée ⟹ tout Conway a une droite c(L) ≤ 3 | S | Codex | 2026-10-18 | `conway99-c1:origin/main:AGENTS.md:600-616` |
| L09-474 | Pilote c ≥ 3 terminé ; registre LAB de 10 052 gabarits | S | Codex | 2026-10-18 | `conway99-c1:origin/main:AGENTS.md:664-675` |
| L09-475 | Gabarits c3 exclus sans Gram par certificats entiers (5128, 4192, gz9748) ; 8650 et gz3 ouverts | C | Codex | 2026-10-18 | `conway99-c1:origin/main:AGENTS.md:549-556` |
| L09-476 | Lemme du carré de défaut ⟹ parité sur 12 sommets ; lemme de Gram des cellules de grilles | P | Codex | 2026-10-18 | `conway99-c1:origin/main:AGENTS.md:435-453` |
| L09-477 | Rang 7 : quatre gabarits gz de dimension 7 | E | Codex | 2026-10-19 | `conway99-c1:origin/main:AGENTS.md:407-420` |
| L09-478 | gz5602 FERMÉ par calcul entier fini (toutes Grams, sans symétrie) | C | Codex | 2026-10-19 | `conway99-c1:origin/main:AGENTS.md:347-375` |
| L09-479 | Famille (2,3) partagée fermée (5 312/5 312) | C | Codex | 2026-10-19 | `conway99-c1:origin/main:AGENTS.md:323-346` |
| L09-480 | Famille K3 universelle fermée (19/10, 05 h 10, LAB1237) | C | Codex | 2026-10-19 | `conway99-c1:origin/main:AGENTS.md:144-157` |
| L09-481 | Famille 2K2 fermée (19/10, 06 h 35) ; registre 902 → 537 → 435 | C | Codex | 2026-10-19 | `conway99-c1:origin/main:AGENTS.md:73-96` |
| L09-482 | 2K2N : premier raccordement interdit avec toute grille B/C (19/10, 08 h 50) | C | Codex | 2026-10-19 | `conway99-c1:origin/main:AGENTS.md:1-19` |

**G2 — conway99-c1:origin/main — notes du 19/10**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-483 | Fermeture de la famille 2K2 (sept raccordements résiduels) | C | Codex | 2026-10-19 | `conway99-c1:origin/main:notes/FERMETURE_2K2_2026_10_19.txt:1-46` |
| L09-484 | Conséquence structurelle 2K2 + K3 : le graphe des grilles est une étoile | P | Codex | 2026-10-19 | `conway99-c1:origin/main:notes/FERMETURE_2K2_2026_10_19.txt:105-115` |
| L09-485 | Lemmes de coupes de continuation (quotas exacts, différence de quotas, deux lignes) | P | Codex | 2026-10-19 | `conway99-c1:origin/main:notes/PREUVE_COUPES_CONTINUATION_2026_10_19.txt:1-214` |
| L09-486 | Contrôles positifs des coupes sur BvLS243 et twin243_switched | E | Codex | 2026-10-19 | `conway99-c1:origin/main:notes/PREUVE_COUPES_CONTINUATION_2026_10_19.txt:220-258` |
| L09-487 | Lemme des quatre facteurs simples (cœur partagé + grille Q12) | P | Codex | 2026-10-19 | `conway99-c1:origin/main:notes/FACTEURS_QUATRE_COULEURS_2026_10_19.txt:1-59` |
| L09-488 | Production K3 universelle : catalogue fini (état intermédiaire du 19/10, 03 h) | E | Codex | 2026-10-19 | `conway99-c1:origin/main:notes/PRODUCTION_K3_UNIVERSELLE_2026_10_19.txt:1-127` |
| L09-489 | Lemme d'inclusion des contributions et cubicité/couplage forcés (K3) | P | Codex | 2026-10-19 | `conway99-c1:origin/main:notes/FACTEURS_QUATRE_COULEURS_2026_10_19.txt:157-175` |
| L09-490 | Transport vers P3 (réponse LAB1207) : stratification finie | P | Codex | 2026-10-19 | `conway99-c1:origin/main:notes/FACTEURS_QUATRE_COULEURS_2026_10_19.txt:403-437` |
| L09-491 | Identité générale du noyau signé n_B(u) − n_A(u) = 2r − 2 − 4\|S\| + 2c(u) | P | Codex | 2026-10-19 | `conway99-c1:origin/main:notes/NOYAU_SIGNE_2K2N_2026_10_19.txt:1-101` |
| L09-492 | 2K2N : noyau signé satisfaisable, pas d'exclusion | S | Codex | 2026-10-19 | `conway99-c1:origin/main:notes/NOYAU_SIGNE_2K2N_2026_10_19.txt:121-193` |
| L09-493 | K2BC : quatre noyaux minimaux de 20 sommets (S = 013, 026, 345, 456) | P | Codex | 2026-10-19 | `conway99-c1:origin/main:notes/NOYAUX_SIGNES_K2BC_2026_10_19.txt:1-188` |
| L09-494 | Domination exacte des grilles (Conway) et premier raccordement 2K2N sans grille B/C | C | Codex | 2026-10-19 | `conway99-c1:origin/main:notes/GRILLES_BC_PROFILS_2K2N_2026_10_19.txt:17-52` |

**H — C:/home/researcher/cw/review — relectures du 16/10**

| id | énoncé court | statut | auteur | date | source principale |
|---|---|---|---|---|---|
| L09-495 | Brief commun de la relecture du 16/10 (LAB) | H | LAB | 2026-10-16 | `C:/home/researcher/cw/review/BRIEF.md:1-40` |
| L09-496 | Relecture 01 (origine : conway99-involution + lab-archive) — partielle | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/01_origin.md:1-8` |
| L09-497 | Relecture 02 (C3 et C7) — partielle | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/02_symmetry_c3_c7.md:1-34` |
| L09-498 | Relecture 03 (labos C2 et labo « structures ») — partielle | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/03_c2_labs_structures.md:1-18` |
| L09-499 | Relecture 04 (fin de C2 : route C, Researcher 2, rank-17, AWS) — partielle | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/04_c2_routeC_researcher2.md:13-53` |
| L09-500 | Relecture 05 (C1 main, notes 00–99) : erreurs et points utiles | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/05_c1_notes_00_99.md:251-269` |
| L09-501 | Relecture 05 §6.3 : la classe de carré DISC devrait être 2 (pas « 2 ou 14 ») | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/05_c1_notes_00_99.md:271-274` |
| L09-502 | Relecture 06 (C1, notes ≥ 100 et branches) — partielle : carte des branches | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/06_c1_notes_100plus_branches.md:1-55` |
| L09-503 | Relecture 07 (C1, 7–13/10) : résultats-clés enregistrés | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/07_workspace_c1_0713.md:105-108` |
| L09-504 | Relecture 08 (13–14/10) : erreurs | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/08_workspace_1314.md:1-16` |
| L09-505 | Relecture 09 (Codex 14–16/10) : erreurs et cinq points utiles | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/09_codex_14_16oct.md:1-30` |
| L09-506 | Constructions : toutes les heuristiques ont échoué, y compris sur le contrôle 243 | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/04_c2_routeC_researcher2.md:40-41` |
| L09-507 | Route de comptage au rang 37 : close par ses propres marges | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/07_workspace_c1_0713.md:143-150` |
| L09-508 | Relecture 02 §6.2 : faits arithmétiques globaux pour tout graphe de Conway (dérivation du relecteur) | H | Claude-review | 2026-10-16 | `C:/home/researcher/cw/review/02_symmetry_c3_c7.md:288-316` |

## 4. Routes fermées, et pourquoi

**C1, 24–26/09.**
- Spectre de Hodge / Σν³ : le confinement « de Garland » est faux pour toute la famille (H0, L09-013) ; majorer Σν³ revient à F2-SRG (L09-058).
- Krein F14, F4 local, F2 local (L09-009, L09-010, L09-006). Attention : F2′, F11, F1/F13 n'ont été « tuées » que hors diamètre 2 et sont re-scopées OUVERTES le 27/09 (L09-007, L09-097).
- Hiérarchie locale jusqu'à 8 sommets : tout bute sur L16 (mur, L09-045, L09-069) ; Delsarte local trivial (L09-067) ; second moment Δ (L09-072) ; parités d'holonomie sans loi (L09-073).
- Méthodes Shpectorov–Zhao et Kivva non transposables (L09-079) ; Akiyama sur Λ_L (L09-143) ; droites équiangulaires (L09-157).
- Voie 7-adique par sous-matrices déterminées : se ramène à la matrice générique G, négatif démontré (L09-049, L09-129).
- Construction par RRR (L09-046) ; F17 naïve réfutée par les produits cartésiens (L09-071).
- Fano tendu : route du dérangement close (L09-273) ; Ψ seul n'est pas un lemme (480 réglages, L09-169, L09-270) ; « P-Ψ + admissibilité » n'est pas un lemme de Fano complet (L09-318) ; la branche « factorisation de Heawood » est exclue à P = 0 (L09-317).

**C2 (involution), labo « structures » et carnet C2.**
- Idée « commutant » : ne donne que les indicatrices de composantes (L09-271).
- Lemme « unique par 243 » : pas de transfert 3-adique → 7-adique (L09-328) ; examen exhaustif des boules à P = 0 écarté (≈ 8·10⁹ classes, L09-325).
- Lemme purement local « pas de bloc A » : impossible (L09-288) ; arbre de Farkas (0,6) hors de portée (L09-306) ; pistes « tout d'un coup » (transfert de C3, ligne de rang 27) écartées (L09-315).
- Coupe de parité m(u) de Sol : vide (L09-311) ; comptages de points fixes, raffinements 2-adiques, désordre 7-adique : impasses consignées (L09-384).

**Rank-17.**
- Ansätze symétriques S7, A7, L3(2), S5, A5, F20, C5, D5 : morts (L09-422) ; coupes spectrales du handoff (L09-401) ; ℤ¹⁷ paires 1 et 2 hors de portée (Knuth, L09-409) ; dix représentations « collapsées » (L09-436).
- La route (C) y est déclarée « remplacée » le 28/09 (L09-420) ; elle a pourtant été reprise et menée à 156/156 le 07/10 (L09-055) : voir 6.1.

**C1, octobre.**
- Route par réseaux « à la C2 » (masse du genre de rang 48 ≈ 10¹²¹), boules de triangle puis colonnes (≥ 10¹⁰ h CPU), hiérarchie ≤ 8 (L09-458).
- Route de comptage au rang 37 : close par ses propres marges (L09-507) ; constructions heuristiques : toutes échouent, y compris sur le contrôle 243 (L09-506).

## 5. Questions ouvertes, classées par levier

**Arithmétique et réseaux.**
- Plafond 7-adique à P = 0 : obstruction uniforme de l'étoile à k = 22 (tâche (a′)), k = 22 sans droite générique, k = 24 à 28, NT (L09-281, L09-322, L09-323) ; « non » uniforme pour R_L ⟹ k ≥ 30 (conditionnel, section 10).
- Involution : exclure g⁻ = 18 et g⁻ = 20 (L09-364, L09-448), réseau N_max de déterminant 49 (L09-371), mécanisme forçant rang₇ Gram(L_T) ≤ 1 (L09-363) ; W = 2S + I, W² = 49I (L09-360).
- Rank-17 : R6 ∧ R8 (L09-414) ; archivage et relecture des preuves de Sol R≤4 (L09-412) ; R8 k = 1 (L09-425) ; extension N des ancres Type 0/II (L09-432) ; lemme uniforme à la couche de relèvement (L09-441).
- DISC : la classe 14 est-elle exclue par L4 / la parité de v₇(det) ? (L09-501, L09-508).

**Local et combinatoire.**
- Fano tendu satisfaisant toutes les bornes ordonnées (L09-318) ; « aucun sommet de Fano tendu » (L09-173).
- C2 : lemme 11.2 et famille dis (L09-284, L09-285) ; étoile totalement libre (L09-351, L09-371) ; lemme de simplicité ou UNSAT des 7 types (0,6) (L09-263) ; AD pour n_dd ≥ 7 (L09-293).
- C1 (octobre) : extension à cinq étoiles et (H-MATCH) (L09-495) ; NG7 (L09-465) ; famille co-Heawood (L09-460) ; familles P3, 2K2N, K2BC et 435 gabarits « c3 » (L09-481, L09-492).

**Calcul fini (avec coûts connus).**
- C2 : recertification des raccourcis « transfer » (≤ 2 479 669 paires, L09-499) ; complétude de l'énumération des paires de 132 (L09-313) ; énumérateur R8 k = 1 écrit, non lancé (L09-438) ; moteur wfe en pause (L09-427).
- C1 : test d'étoile au rang 37 sur toutes les boules connexes, 1,5–2,7 années-cœur (L09-503).

**Symétrie.**
- Groupes point-transitifs C7, D7, F21, F42 pour un modèle de N (L09-422) ; question des (1,2)-graphes de Cayley sur sous-groupes d'ordre 3 (L09-436) ; hypothèse de parallélisme (section 10).

**Construction.**
- Un membre tordu de la famille a été trouvé le 07/10 (L09-056) ; aucun srg(243,22,1,2) asymétrique connu parmi huit (L09-503) ; région BvLS à trois prismes (L09-451) ; construction d'un SRG asymétrique avec λ = 1 (consigne du 14/10, L09-457).

## 6. Contradictions, redécouvertes, remplacements

### 6.1 Contradictions et écarts

| # | écart | sources | lecture |
|---|---|---|---|
| 1 | Route (C) « superseded » par le rank-17 le 28/09, puis C2 exclu par la route (C) 156/156 le 07/10 | conway99-rank17:master:PROOF_OBLIGATION.md:195 ; conway99-c1:origin/main:JOURNAL.md:654-660 | changement de stratégie, pas une erreur ; les deux ne sont pas incompatibles |
| 2 | Ligne d'arrivée : « (A) les 1521 types à pivots » contre « (A) = 1 507 types » | conway99-structures-lab:master:JOURNAL.md:945 ; conway99-c1:main:notes/137_LIGNE_D_ARRIVEE_C2.md:69 | 1 521 = toutes les classes à pivots (notes/136:56) ; 1 507 après bris d'égalité |
| 3 | AD mortes pour n_dd ≤ 6 : « 6 079 classes » contre la somme du tableau 14 + 8 + 510 + 853 + 4 594 = 5 979 | conway99-structures-lab:master:JOURNAL.md:737 ; NOTE_S28_AD_NIVEAU_PAIRES.md:119-125 | écart de 100, non résolu dans les sources |
| 4 | Auteur du dossier CONWAY_ASTRA du 27/09 : « Astra » (nom du dossier), « de Sol » (notes/139), « session Codex » | CONWAY_ASTRA_27_09_2026_0836/LIRE_D_ABORD_POUR_CLAUDE.md:18 ; conway99-c1:main:notes/139 (lot C) | attribution incertaine ; ne pas créditer sans vérification |
| 5 | Campagne BvLS « Astra » (11/10) contre « dossiers externes (ChatGPT) » ; chemin /mnt/data dans le dossier | conway99-c1:origin/main:research/astra_bvls_boundary_20261011/COORDINATION.md:1 ; dossiers_externes/INDEX.md:1 ; BVLS_RECONSTRUCTION_DOSSIER/RESULTATS.md:81 | la source ne dit pas « Astra = ChatGPT » ; relecture 03 : « Astra, Sol = modèles externes » (review/03:57) |
| 6 | PRODUCTION_K3 (≈ 03 h 43) dit « N'EST PAS encore exclue » ; K3U fermée à 05 h 10 | notes/PRODUCTION_K3_UNIVERSELLE_2026_10_19.txt:5-7 ; AGENTS.md:144-157 | note périmée (L09-488 remplacé par L09-480) |
| 7 | Lemme 11.2 de C2 « φ_u(R) = 2 » (copie du 25/09) ; corrigé en « ≥ 2 » le 26/09 | conway99-structures-lab:master:logs/c2_programme.md:192 ; review/01_origin.md:243 | la copie du labo est antérieure à la correction |
| 8 | Recherche brute d'ordre 7 « 0 solution en ~8·10⁹ nœuds » non reproduite (pas de terminaison en 50 s) | ordre7/tex/order7.tex:632-635 ; review/02_symmetry_c3_c7.md:377 | non nécessaire à la preuve |
| 9 | notes/127 dit « relu » ; notes/126 §3 bis non relu ; la relecture de « structures » porte sur §3 quater | B2 (L09-193, L09-196) ; conway99-structures-lab:master:JOURNAL.md:633-634 | à préciser par section |
| 10 | notes/110 contre notes/100 sur la route de Minkowski (close / non close) ; re-scope du 27/09 | B1 (L09-142) | statut final : non close au-delà des comptages |
| 11 | Même boule du dossier 5 : 41 014 nœuds (Astra) contre 27 626 (structures) | astra/RAPPORT_ASTRA_DOSSIER5.md:313 ; NOTE_S24_ASTRA_DOSSIER5.md:15 | implémentations différentes, même verdict ; pas une contradiction |
| 12 | Numéros de notes 165–178 utilisés deux fois (Claude/asymétrie et Codex/échelle) ; notes de Codex 232–244 et 247–250 dans aucune branche | review/06_c1_notes_100plus_branches.md:33-35 | citer avec la branche |
| 13 | Le JOURNAL de « structures » donne g⁻ ∈ {18,20} « dès qu'une droite-bloc est générique » ; le dossier 6 d'Astra souligne que l'existence d'une droite-bloc générique n'est pas forcée | JOURNAL.md:697-698 ; astra/RAPPORT_ASTRA_DOSSIER6.md:12 | levé ensuite : g⁻ ≠ 14 et g⁻ ≠ 16 sans cette hypothèse (L09-296, L09-297) |
| 14 | Taux de mort Z4 « 97 % » (premier 1 % de l'arbre DFS) contre ≈ 23 % non biaisé | conway99-rank17:master:Z17_FINDINGS.md:74-84 | mesure retirée (L09-408) |

### 6.2 Redécouvertes (deux dates)

- L1 (24/09) = Makhnev 1988 (L09-074) ; H + 3P = 213 444 = théorème de Reimbayev (L09-276) ; la porte I_x de notes/123 refait 99/109/114 (L09-276).
- Théorème D′ du carnet C2 (25/09) = cas particulier de L8 (C1, 25/09) (L09-385).
- Identités thêta du dossier Astra du 27/09 = conséquences des identités de voisins (handoff GPT-Pro §11, 27/09) (L09-446, L09-401).
- Spectre du bloc60 (Codex, 18/10) déjà dans les archives pour toute droite (LAB1142, 19/10) (L09-476).
- Théorème de rang de la nuit du 14/10 (rang ≥ 35) = redécouverte, plus faible, de la fenêtre {37, 39, 41, 43} obtenue les 07–08/10 (L09-504).
- Corollaire A d'oddité au rang 37 = L23 du 25/09 (relecture 07, R37, L09-503).
- Lemme de réseau de S5 : classique (Martinet 2003) (L09-248) ; moments d'openai/math (07/10) = doublon de la note 91 (A1).
- Exclusion de l'ordre 7 : connue par ordinateur (Behbahani–Lam 2011), refaite sans ordinateur le 02/10 (L09-391).
- Paley(25) asymétriques retrouvés = Paulus–Rozenfeld (L09-455) ; région lointaine de BvLS à deux solutions = contrôle connu (L09-451).
- Les 441 types P = 0 de Sol = sous-ensemble exact de la table des 3 308 classes (validation croisée, L09-301).

### 6.3 Résultats remplacés ou retirés

Tableau automatique (statuts X et R) ci-dessous, à lire avec les remarques du JSONL.

| id | résultat | statut | remplacé par / portée de la réfutation | source |
|---|---|---|---|---|
| L09-006 | F2 (rigidité q=3) tuée sous forme locale | R | non relu — Réfute seulement la version locale (rayon 2, sans diamètre 2). Version SRG = conjecture F2-SRG/F20, ouverte. | `conway99-c1:main:notes/20_ATTAQUES_R.md:23-28` |
| L09-007 | F2' et F11 tuées hors diamètre 2 seulement (re-scopées le 27/09) | R | audit des réfutations du 27/09 (involution_lab_c1/audit_refutations.md, non ouvert) — Annotation « [RE-SCOPED 27/09: the basis only satisfies part of the hypotheses of the target (srg(99,14,1,2), diameter 2)] » : correc… | `conway99-c1:main:notes/20_ATTAQUES_R.md:29-31` |
| L09-009 | F14 (annulation de Krein) tuée | R | non relu (calcul exact) | `conway99-c1:main:notes/20_ATTAQUES_R.md:92-95` |
| L09-010 | F4 (cohérence de classes / Fano) tuée localement | R | non relu | `conway99-c1:main:notes/20_ATTAQUES_R.md:50-54` |
| L09-071 | F17 naïve réfutée par les produits cartésiens | R | non relu (vérifié à la main selon la source) — Réfute F17 sous forme naïve ; une version « torsion uniforme ⇒ plan d'ordre t » reste non réfutée (93:26-27). | `conway99-c1:main:notes/93_NON_EXISTENCE_V2.md:18-27` |
| L09-083 | Règle de transport « 0 ou 1 transport isométrique » (erronée) | X | « exactement 2 » (code/transport_rule_check.py) ; la conséquence (jamais exactement une arête non isométrique par triangle) reste vraie | `conway99-c1:main:notes/95_L7_PREUVE_HUMAINE.md:79-82` |
| L09-099 | Proposition de cohérence des 21 lemmes (forme forte retirée) | X | Forme faible : le profil satisfait seulement les conséquences scalaires affichées ; il ne fournit ni transitions ni géométrie ; l'absence actuelle de contradiction n'interdit pas une future combinaison | `conway99-c1:main:notes/100_SYNTHESE_DES_LEMMES.md:191-207` |
| L09-115 | Exemple de « coupe » au point de Hamming (erroné) | R | corrigé le 25/09 après-midi (notes/105 §6) — Réfuté : l'exemple viole déjà μ avec les étiquettes. Aussi retirée : « les triangles NNN forment un 2-cycle », non établie, utilisée nulle part. | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:146-156` |
| L09-145 | Correction de notes/102 §9 (droites intérieures) | X | L'énoncé ne vaut que pour les droites à trois arêtes génériques | `conway99-c1:main:notes/110_ROUTES_CLOSES_ET_CODES_DES_DROITES.md:90-97` |
| L09-162 | Fano tendu : le témoin survit au niveau des blocs (conclusion corrigée) | R | corrigé le 26/09 (notes/117 §2 ter) ; re-scopé 27/09 (notes/100:65) — Réfuté par : le raffinement par cellules antipodales tue ce témoin (Farkas exact revérifié par « structures », verify_c1_cells.py) ; la route n'est P… | `conway99-c1:main:notes/116_SECOND_ORDRE_ET_FANO_TENDU.md:54-69` |
| L09-188 | Corrections du JOURNAL (b231c36, d7cd060) et des échantillons « S = 0 » | X | Étiquette « S = 0 » des échantillons 117-118 retirée ; « maille ≥ 5 » rétablie à P = S = 0 | `conway99-c1:main:notes/125_CYCLES_COURTS_DES_GRAPHES_DE_DROITES.md:112-130` |
| L09-227 | Verdicts de l'étage h antérieurs au bug de bitsets (retirés) | X | Verdicts recalculés après correction (test unitaire M = 1…32256, contrôles y = 0 et ctrl_prescribed.py) | `conway99-c1:main:notes/142_EXCLUSION_132_ET_CHAINE_Y_H.md:52-58` |
| L09-263 | ERRATUM : « tout-tordu pur exclu » ne couvre que les circuits simples | X | Exclusion restreinte aux circuits simples ; cas non simple ouvert (couvert si tier06 UNSAT) | `conway99-structures-lab:master:JOURNAL.md:873-879` |
| L09-273 | Route du dérangement (T ≡ 1) au Fano tendu : close | R | réfuté par fano_T_check.py sur le témoin | `conway99-structures-lab:master:JOURNAL.md:312-313` |
| L09-289 | Correction : objectif de phase 1 du PL racine non convergé | X | correction d'un message à l'utilisateur | `conway99-structures-lab:master:JOURNAL.md:559-561` |
| L09-320 | Correction de l'heuristique du dossier 5 (Ξ) | X | ≈ 7^(−210) | `conway99-structures-lab:master:JOURNAL.md:470-472` |
| L09-324 | Astra, suivi n° 4 : la piste (α) de C1 est réfutée | R | témoin vérifié par code du labo (verify_astra_apex_witness.py) ; réfute la piste (α) (noyau des 2 apex) | `conway99-structures-lab:master:JOURNAL.md:640-642` |
| L09-353 | Correction NOTE_S29 : une orbite rigide n'a pas \|r_f\|² = 0 | X | \|r_f\|² = (14 + y − 3x)/15 ; rigidité purement 7-adique | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:67-69` |
| L09-383 | Carnet C2 : version initiale du Théorème A (e′ pair) retirée | X | Théorème A corrigé (e′ impair) | `conway99-structures-lab:master:logs/c2_programme.md:37-38` |
| L09-408 | Correction du taux de mort Z4 (biais DFS) et retrait d'une mesure | X | Taux non biaisés : paire 0 ~23 % tués ; paires 1-2 15–54 % tués | `conway99-rank17:master:Z17_FINDINGS.md:74-84` |
| L09-468 | Réfutations du 15/10 : ODD9, SUM14, KER-SYM universelles ; « une seule saturation » | R | contre-exemples exacts de LAB acceptés sans re-audit — Journal de Codex (AGENTS.md, ordre antichronologique, 09/10→19/10) ; le détail des notes de Codex relève des lots L05/L08 ; ici : états et résultats-clés tels qu'éc… | `conway99-c1:origin/main:AGENTS.md:1353-1360` |
| L09-471 | Bug OR-Tools 9.15 (domain[-1]) : verdicts retirés le 18/10 | X | verdicts recalculés après correctif (voir entrées suivantes) | `conway99-c1:origin/main:AGENTS.md:657-662` |

Autres retraits ou re-portées signalés dans les remarques du JSONL (statut de l'énoncé conservé) : erratum « circuits simples » (L09-253, L09-254, L09-256, L09-260, L09-262), lemme 11.2 de C2 (L09-284), « S = 0 » des échantillons de C1 (L09-188, L09-278), PRODUCTION_K3 périmée (L09-488).

## 7. Rôle de chaque IA (selon les sources)

| agent | rôle dans ce lot | sources |
|---|---|---|
| Claude-C1 (« chercheur F » et « chercheur R ») | auteur des notes 00–154 et du JOURNAL de conway99-c1 `main` (24–29/09) : lemmes L1–L25, programme 7-adique, Fano tendu, I_x ; puis appui à C2 (q:7, pivots, ligne d'arrivée, ligne (C), rank-17 côté C1 : R6, J-cells, coupure 2\|5) | L09-001–L09-244 ; conway99-c1:main:JOURNAL.md |
| Claude-structures (labo « structures », identité git « ren ») | vérificateur et passeur entre C1, C2, Astra et Sol (S1–S38) : relectures, certificats exacts (tout-tordu, cellules, paire × bloc), AD, bloc plein, 156 enveloppes explicites, O₂₄, outils SAT déclarables ; rédacteur des dossiers 2–6 pour Astra et des dossiers pour Sol ; côté rank-17 : cibles A/B, R8 k = 0, evenframe, paradigm | L09-245–L09-380, L09-392 ; L09-421–L09-428, L09-435–L09-437 ; conway99-structures-lab:master:JOURNAL.md:4-6 |
| Claude-C2 (session principale C2 ; LAB de c2-experimental ; Fable) | carnet MATH_C2_PROGRAMME (copie dans le labo), campagnes paires/orbites, DRAT des 79 types, frame_dfs de la route (C), scan caractéristique du rank-17 | L09-381–L09-390, L09-302, L09-431 ; review/03_c2_labs_structures.md:51-60 |
| GPT-Pro | handoff du rank-17 (27/09) : switch de rang 17, PE, preuves de B′ et de min N* ≥ 8/7 | L09-393–L09-402 |
| ChatGPT-Sol (« Sol », relayé par l'utilisateur) | réduction de la route (C) aux 156 réseaux de Borcherds ; rank-17 : R≤4 et min K* ≥ 5/7 (492 classes, preuve non archivée), lemme DC, règles d'étoile, Type 0/II ; signe de Witt de A33 ; supports courts et Wagner (calculs sur SageMathCell) | L09-309, L09-410–L09-412, L09-432, L09-297, L09-367–L09-369 |
| Astra (« autre modèle », relayé par l'utilisateur) | dossiers 2–6 (Fano tendu, carrés disjoints, 7-adique, involution), audit adverse du critère S5 et du carnet C2 (erreur du Théorème A), théorème caractéristique du 29/09, dossier « repère 42+7 » du 27/09, campagne BvLS du 11/10 ; déclare ne consulter aucun dépôt (dossier 6) | L09-316–L09-324, L09-361–L09-366, L09-430, L09-442–L09-451 ; logs/c2_programme.md:602 ; astra/RAPPORT_ASTRA_DOSSIER6.md:3 |
| Codex (identité git « amazing-source ») | C1 à partir du 08–09/10 (notes 165–260 dans d'autres lots), journal AGENTS.md (09–19/10), fermetures de familles avec LAB (gz5602, (2,3), K3U, 2K2), notes du 19/10 ; nommé aussi comme auteur du dossier du 27/09 (LIRE_D_ABORD) | L09-456–L09-494 ; CONWAY_ASTRA_27_09_2026_0836/LIRE_D_ABORD_POUR_CLAUDE.md:18 |
| LAB (Claude du PC du labo, identité git « dilan ») | recensements exhaustifs et manifestes (registre « c3 », K3U, 2K2), production AWS, brief des relectures | L09-480, L09-481, L09-495 ; AGENTS.md:144-157 |
| Claude-cloud (auteur git « Claude ») | notes 155–164 et PASSATION (06–07/10), dossiers externes versés (12/10), brouillon d'ordre 7 (02/10) | L09-458, L09-452, L09-391 |
| Claude-review (16/10) | neuf relectures partielles en lecture seule (statuts recopiés ; quelques vérifications propres) | L09-495–L09-508 |
| ChatGPT (dossiers externes des 11–12/10, preuve candidate d'ordre 7 du 02/10) | Paley(25), Hoffman α = 22, K7 partiel, CODE7 ; stratégie de la preuve d'ordre 7 | L09-452–L09-455, L09-391 |
| utilisateur (Dilan) | décisions : gel des solveurs (25/09), calcul certifié plafonné (26/09), pause 7-adique et « tout sur C2 » (26/09), « effacer les réseaux mathématiquement » (27/09), plus de cloud (27/09), « exploration, lemmes de réduction » (09/10), « asymétrie », « deux chercheurs » (14/10) | L09-246, L09-047, L09-291, L09-309, L09-456, L09-457 |

## 8. Données et objets

- **conway99-c1 `main`, data/** : `k2_patterns.txt`, `k3_patterns_fast.txt`, `.k3_patterns_lf.txt` (contenu différent dès la ligne 2, non élucidé), `k3_results.txt` (24 UNSAT, 2 UNKNOWN) ; ils appuient la frontière SAT de torsion (L09-041, L09-042). `tools/win64/README.md` : chaîne DRAT pour Windows (27/09), testée positivement et négativement, pour la route SAT des 79 types de C2. Les répertoires `data/rank17`, `data/finishC` (trackers de la route (C)) ne sont pas ouverts (review/05_c1_notes_00_99.md:337 les signale aussi comme non ouverts).
- **conway99-structures-lab** : `logs/core_certs/` (one_00–14, zero_00–13 : certificats entiers du tout-tordu, S17/S19), `logs/orbit_certs/`, `logs/brouwer/` (27 pages HTML de la table de Brouwer, v ≤ 1300, utilisées par S5), `logs/srgw.txt` (texte du livre de Brouwer–Van Maldeghem, 1,36 Mo), `involution/envelopes/U/` (les 156 réseaux de Borcherds explicites, S35), `frame_results/`, `state/`, `involution/type_table.json` et `all_types_3308.json`, `ad/*.json` (classes AD, résidus n_dd = 7–8), `freestar/`, `famille/` (H(2,3), BvLS), `review/q7_3k2_ext_independent.py` (ré-implémentation 3K₂, S29), `scripts/` (102 scripts). Branche `claude/chat-session-09hf0k` : `ordre7/` (tex, pdf, scripts census6, mixed6, fullsearch.c, squelette Lean).
- **conway99-rank17** : `r17_char/rank17_char_kills_2909.json` (un témoin par classe fermée), `sol_type02/verification.json` (77 ancres, 2 097 152 tournois), `r8k1/` (all_tasks 4 132 tâches, skeletons 123, count_* : TOTAL survivors 0, leafdump), `r6_data/`, `r8k3/`, `wfe/`, `out_kstar_all.json`, `o24_spectral_results.json`, `SHA256SUMS.txt`.
- **Dossier d'Astra (Bureau)** : archive `ATTAQUE_DIRECTE_27_0836_PREUVES_CERTIFICATS.zip` (162 fichiers, SHA256 vérifiés selon l'AUDIT.json) et `EXTRAIT/` (scripts .mjs et sorties .json des campagnes 0803 et 0836).
- **conway99-c1 `origin/main`** : `dossiers_externes/` (zips d'origine dans `archives/`, données BvLS et Hoffman seulement dans les zips) ; `data/codex_short_columns_20261018/…` et `code/lab_exploration_2026-10-16/gz5602_2026-10-19/…` (manifestes K3U, 2K2, gz5602 ; certificats RUP ; gros RUP de 212 Mo en morceaux de 32 MiB).
- **Desktop/Recherche_Conway/c1-structures-audit** : clone partiel (`--filter=blob:none`) sans arbre de travail, même commit que le dépôt de `cw` : aucune donnée propre.

## 9. Notes lues, survolées, non lues (avec raison)

**Lues en entier.**
- conway99-c1 `main` : README, JOURNAL (608 lignes), LAB_INSTRUCTIONS_C1, rapport/RAPPORT_C1.md, notes 00–154 ; diffs `main` → `origin/main` de README, JOURNAL, LAB_INSTRUCTIONS et notes/100.
- conway99-structures-lab `master` : JOURNAL (1 003 lignes), REGISTRE, les 16 NOTE_*, astra/DOSSIER6_INVOLUTION_7ADIQUE, PROBLEMES_OUVERTS_INVOLUTION, PROBLEME_BLOC_PLEIN_POUR_SOL, POUR_SOL_G18_G20_NOS_NOMBRES, famille/REVUE_LITTERATURE_9_243, involution/LEMMA_SCOPES et HANDOFF_FULLBLOCK, ad/README et HANDOFF_AD_SWEEP.
- conway99-rank17 `master` : toute la prose (README, README_TEAM, RANK17_HANDOFF, PROOF_OBLIGATION, TARGETS_AB_STRUCTURES, Z17_FINDINGS, Z17_SEARCH_DESIGN, SPEC_ENGINE, GPT_*, r17_char, r6_data, r8k3, sol_type02, evenframe, paradigm, wfe).
- conway99-c1 `origin/main` : notes du 19/10 FERMETURE_2K2, PREUVE_COUPES_CONTINUATION, PRODUCTION_K3_UNIVERSELLE, NOYAU_SIGNE_2K2N, NOYAUX_SIGNES_K2BC, GRILLES_BC_PROFILS_2K2N ; CLAUDE.md ; PASSATION_C1_2026-10-07 ; research/astra_bvls_boundary_20261011/COORDINATION ; dossiers_externes/INDEX, BVLS (README, COORDINATION, RESULTATS).
- Bureau, dossier d'Astra : LIRE_D_ABORD_POUR_CLAUDE, AUDIT.json, BILAN_ATTAQUE_DIRECTE_REPERE42_7 (identique à sa copie de EXTRAIT/…0836, contrôlé par `cmp`).
- review/ : BRIEF, 06 (58 lignes).

**Lues en partie (sections indiquées).**
- AGENTS.md (2 073 lignes) : lignes 1–700 et 1 717–2 073 lues ; 700–1 716 par recherche des événements datés et des mots « RÉFUTÉ / CORRECTION / THÉORÈME / FERMÉ », avec lecture du contexte de chaque occurrence retenue. Le détail relève du lot L05 (notes de Codex).
- notes/FACTEURS_QUATRE_COULEURS_2026_10_19.txt (851 lignes) : 1–175, 253–440, 690–851 ; le reste survolé.
- logs/c2_programme.md (803 lignes, copie du carnet C2) : §0–§7, §20–§21, statut de relecture, audit d'Astra, §24 lus ; §8–§19 et §22–§23 par les énoncés (recherche « Théorème / Lemme / PROUVÉ / IMPASSE »). Original dans un autre lot.
- astra/RAPPORT_ASTRA_DOSSIER5, DOSSIER5_SUITE, DOSSIER6, RAPPORT_SOL_SUPPORTS_COURTS, RAPPORT_SOL_WAGNER : sections clés et conclusions ; RAPPORT_ASTRA_SUIVI4_ET_AUDIT_S5 : messages 1–2 (lignes 1–332), annexes 332–2 738 survolées ; SUIVI3/SUIVI4_DOSSIER5 : têtes et tâches.
- ordre7/tex/order7.tex : énoncés, §3–§6 (structure de la preuve), §8 (vérifications) ; order7.pdf non lu (version compilée).
- ETAT_REPRISE_ACTUEL (dossier d'Astra) : titres seulement.
- dossiers_externes : HOFFMAN README, C1_K7 README, PALEY README (1–45).
- RECHERCHE_ACTIVE_C1.md : 30 premières lignes (lot L05).
- review/01, 02, 03, 04, 05, 07, 08, 09 : en-têtes, résultats principaux et sections « erreurs » et « utile aujourd'hui » ; les autres sections non lues.

**Non lus (raison).**
- logs/srgw.txt au-delà de la tête et de la fin : texte d'un livre publié, pas un résultat de la campagne.
- PREUVES_COMPLETES_REPERE42_7.md (380 Ko) et DOSSIER_SOURCES_SORTIES_REPERE42_7.md (896 Ko) du dossier d'Astra, EXTRAIT/* : taille, lot primaire L01.
- Données volumineuses (r8k1 leafdump 2,2 Mo, count_* 0,5–0,8 Mo, JSON de certificats, logs/*.log, *.json.gz) : têtes seulement, conformément aux CONSIGNES.
- Code (scripts/, involution/*.py, ad/*.py, freestar/, review/*.py, code/codex/) : non lu ; seules les docstrings citées par les notes.
- dossiers_externes : THEORIE, CERTIFICATION, COUVERTURE, PREUVES (K7), RESULTATS (Hoffman, Paley), C3_preuve/proof_c3_english.pdf (lot L04).
- RECHERCHE_A_REDUCTION_STRUCTURELLE.md (lot L05).

## Annexe : chevauchements de lots

- Dossier d'Astra du Bureau : attribué à L01 par `tools/lots.py` ; couvert ici au niveau des résultats (L09-442–L09-449).
- `dossiers_externes/` et `PASSATION_C1_2026-10-07.md` : attribués à L05/L07 ; couverts ici au niveau README/RÉSULTATS (L09-450–L09-455, L09-458).
- AGENTS.md : dans ce lot, mais c'est le journal de Codex (lot L05 pour ses notes) ; les notes de Codex 165–260 ne sont pas dans ce lot.
- Le blob ultérieur du JOURNAL de conway99-c1 (`origin/main`) relève de L07 ; seules ses lignes sur C2 exclu et le nouveau 243 sont reprises (L09-055, L09-056).
- Les relectures du 16/10 recouvrent les lots L01–L08 : leurs entrées ici sont marquées « source secondaire ».

## 10. Matériaux pour la recombinaison

Listes exhaustives pour le lot, avec source exacte et citation littérale contrôlée (script verify.py). Les mêmes objets, un par ligne, sont dans `L09_structures_astra_coord_recomb.jsonl` (champs : id, type, puis si/alors/portee ou objet/relation/valeur/conditions ou enonce/donnerait/demande_par ou methode/cas_origine/cas_cible/transfert_dit_par/etat_transfert, et statut, source, auteur, date, citation, remarques). Statuts : comme en section 3 (un conditionnel O est une implication dont l'hypothèse est la cible ouverte).

### 10.1 Énoncés conditionnels « si X, alors exclusion, contradiction ou réduction » (249)

| id | si (X précis) | alors | portée | statut | source | citation |
|---|---|---|---|---|---|---|
| L09-COND-001 | Γ grid-full (τ = mate en tout sommet) | Γ̃ ≅ H(7,3), 99·\|G\| = 3⁷ : contradiction ; idem tout PQ(2,t,2) grid-full a n = puissance de 3 | tous | P | `conway99-c1:main:notes/30_LEMMES.md:12-27` | « Γ = Γ̃/G avec G le groupe du revêtement agissant librement : 99·\|G\| = 3⁷. Absurde. » — L1 = Makhnev 1988 Thm 2 |
| L09-COND-002 | x est un point de Hamming (τ = mate en x) et σ_x ∈ Aut(Γ) | contradiction (L7) ; dans C2 le point fixe de l'involution est tordu | C2 (et tous) | P | `conway99-c1:main:notes/30_LEMMES.md:67-76` | « Si x est un sommet de Γ tel que τ = mate en x ... alors la réflexion σ_x ... n'est pas un automorphisme de Γ. » |
| L09-COND-003 | x est un point de Hamming | contradiction (L8) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:91-93` | « Pour tout sommet x de srg(99,14,1,2), il existe a, b ∈ N(x) non mates avec τ_a(b) ≠ b̄ » |
| L09-COND-004 | une grille par x manque | au moins deux grilles par x manquent ; g(x) ∈ [0,19] | tous | P | `conway99-c1:main:notes/30_LEMMES.md:108-109` | « Si une grille par x manque, au moins deux manquent ... Donc g(x) ∈ [0, 19]. » |
| L09-COND-005 | τ_a(c) ≠ c̄ et τ_{c̄}(a) = ā (en x) | au moins une grille G_{[c],m}, m ∉ {[a],[c]}, manque en x (L9') | tous | P | `conway99-c1:main:notes/30_LEMMES.md:137-138` | « Si τ_a(c) ≠ c̄ et τ_{c̄}(a) = ā, alors au moins une grille G_{[c],m}, m ∉ {[a],[c]}, manque en x. » |
| L09-COND-006 | τ_a(c) ≠ c̄, τ_c(a) = ā et τ_ā(c̄) = c | au moins une grille G_{[c],m} manque (L9) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:154-155` | « Si τ_a(c) ≠ c̄, τ_c(a) = ā et τ_ā(c̄) = c, alors au moins une grille G_{[c],m}, m ∉ {[a],[c]}, manque en x. » |
| L09-COND-007 | g(x) = 19 (ou 20) | contradiction ; donc g(x) ≤ 18 (L10) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:123-127` | « Aucun sommet n'est dans exactement 19 grilles : g(x) ≤ 18 pour tout x. » |
| L09-COND-008 | toutes les torsions en x ne font intervenir que 3 classes | contradiction (L11) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:115-118` | « Il n'existe pas de sommet x dont toutes les torsions ... ne font intervenir que 3 classes. » |
| L09-COND-009 | τ_a(c) ≠ c̄ (a, c de classes différentes) | τ_c(ā) ≠ a ou ∃ y ∉ [a]∪[c] avec τ_y(c) ≠ c̄ (L12) ; corollaires : une étiquette tordue seule impossible, une classe tordue seule impossible | toute géométrie localement (t+1)K₂ | P | `conway99-c1:main:notes/30_LEMMES.md:158-176` | « Alors τ_c(ā) ≠ a, ou il existe une étiquette y hors des classes de a et de c avec τ_y(c) ≠ c̄. » |
| L09-COND-010 | une classe est tordue par exactement une étiquette | contradiction (L13 : \|Z\| ≠ 1) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:179-184` | « Donc \|Z\| ≠ 1. » |
| L09-COND-011 | exactement deux étiquettes tordent en x avec \|C\| = 2 | contradiction (L14, à la main) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:189-195` | « Dans le bloc {A, B} × {E, F}, 4 voisins communs sont disponibles et au moins 5 sont exigés. » |
| L09-COND-012 | exactement deux étiquettes tordent en x avec \|C\| = 3 ou 4 | UNSAT (L14, SAT sans certificat) | tous | S | `conway99-c1:main:notes/30_LEMMES.md:196-198` | « \|C\| = 3 : UNSAT (1 120 s ...) ; \|C\| = 4 : UNSAT (2 695 s ...) ; \|C\| = 5 : non lancé. » — \|C\| = 5 ouvert |
| L09-COND-013 | k = 0 (invariant 7-adique) | s(x) ≡ 0 (mod 7) et e_σ(x) ≡ 14 (mod 49) en tout sommet (L19) — cas vide car k ≥ 2 | tous | P | `conway99-c1:main:notes/30_LEMMES.md:253` | « Si k = 0 : U_x/7 est entière d'ordre fini, s(x) ≡ 0 (mod 7), e_σ(x) ≡ 14 (mod 49) partout. » |
| L09-COND-014 | k = 6 | tous les τ_a échangent leurs classes par paires, P = 0 (L20) ; puis contradiction (L20 bis) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:262-263` | « k = 6 ⟹ tous les τ_a échangent leurs classes par paires ⟹ P = 0 ; P ≥ 1 ⟹ k ≥ 8 ; une étiquette non tordue ⟹ k ≥ 12. » |
| L09-COND-015 | P ≥ 1 | k ≥ 8 (L20) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:263` | « P ≥ 1 ⟹ k ≥ 8 » |
| L09-COND-016 | une étiquette non tordue (τ_a = mate) existe | k ≥ 12 (L20) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:263` | « une étiquette non tordue ⟹ k ≥ 12 » |
| L09-COND-017 | k = 8 | contradiction (L20 ter, partie finale par propagation sans certificat) | tous | S | `conway99-c1:main:notes/30_LEMMES.md:271-274` | « La méthode à une étoile ne dépasse pas k ≥ 10. » |
| L09-COND-018 | une droite L a G(L) connexe et 7 ∤ τ(G(L)) (d(L) = 1) | k ≥ 22 (L21) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:287` | « si G(L) est connexe et que 7 ne divise pas son nombre d'arbres couvrants, alors k ≥ 22. » |
| L09-COND-019 | k = 30 | contradiction par le genre de Λ₋₄ (L22) ; donc k ≤ 28 | tous | P | `conway99-c1:main:notes/30_LEMMES.md:301-303` | « À k = 30, U = 0 force δ_V = 0, alors que k/2 = 15 est impair. » |
| L09-COND-020 | une droite générique (d(L)=1) a (τ(G(L)) \| 7) = +1 | k ≥ 24 (L23) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:310-311` | « une droite τ-carrée force k ≥ 24. » |
| L09-COND-021 | k = 22 | (τ(G(L)) \| 7) = −1 pour toute droite générique (L23) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:311` | « k = 22 impose (τ(G(L)) \| 7) = −1 pour toute droite générique » |
| L09-COND-022 | il existe S ⊆ V avec rang₇ Q_SS ≥ 43, ou = 42 avec partie non dégénérée scindée | pas de Conway (critère de non-existence, L23) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:317-318` | « Critère de non-existence : un S avec rang₇ Q_SS ≥ 43, ou = 42 et scindé. » — Critère, pas un résultat : aucun tel S connu (blocs connus ≤ 39 points). |
| L09-COND-023 | Γ partitionné en 11 grilles induites à couplages tous anti-isomorphismes | plan projectif d'ordre 10 avec polarité : exclu par Lam (L25) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:334-336` | « Tout anti ⟹ Σ_k M_ik M_kj = J ⟹ plan projectif d'ordre 10 ... exclu par Lam. » |
| L09-COND-024 | Γ partitionné en 11 grilles à couplages tous iso, ou mixte pur | contradiction (7m₃ = 220 ; inégalité β − α/2 ≤ 2) | tous | P | `conway99-c1:main:notes/30_LEMMES.md:336-338` | « Tout iso ⟹ U⁺ = ⊕V_i⁺ invariant, 7m₃ = 220, absurde. » |
| L09-COND-025 | x est un point de Hamming | 18 ≤ k ≤ 26 (L24) — vide depuis L8 | tous | P | `conway99-c1:main:notes/30_LEMMES.md:323-324` | « Dans tous les cas, 18 ≤ k ≤ 26 (nouveau). » |
| L09-COND-026 | le contrôle positif BvLS (t = 10) du modèle enraciné donnait UNSAT | tous les résultats UNSAT (L7, L8, L10, L11, L14) seraient invalidés | C1 (méta) | O | `conway99-c1:main:LAB_INSTRUCTIONS_C1.md:21` | « Un UNSAT ici invaliderait tous les résultats UNSAT (L7, L8, L10, L11, L14) : les arrêter et chercher l'erreur. » — Contrôle jamais exécuté (gel du 25/09). |
| L09-COND-027 | imposer une seule grille G₀₁ en x (τ libre ailleurs) est UNSAT | Γ est sans grille | tous | O | `conway99-c1:main:LAB_INSTRUCTIONS_C1.md:47-51` | « Pour 99 : imposer la grille G₀₁ en x ... UNSAT ⇒ Γ est sans grille. SAT ⇒ un srg(99,14,1,2) (!) » — Test proposé (analogue Gewirtz), jamais lancé. |
| L09-COND-028 | tout PQ(2,t,2) est grid-full (F2-SRG) | pas de Conway (par L1) ; implique aussi l'unicité de BvLS | tous | O | `conway99-c1:main:notes/10_IDEES_F.md:14` | « Rigidité q = 3 : « localement (t+1)K₂ + μ = 2 ⇒ grid-full ⇒ quotient de H(t+1,3) ». Tuerait 99, 6273, 494019 d'un coup » |
| L09-COND-029 | toute géométrie locale tordue exige un plan projectif d'ordre t (F17) | à t = 6 aucune torsion (Bruck–Ryser), donc pas de Conway par L1 ; idem 6273 (t = 55) ; unicité de BvLS (t = 10, Lam) | tous | O | `conway99-c1:main:notes/10_IDEES_F.md:34` | « Si toute géométrie locale tordue exigeait un plan d'ordre t, alors t = 6 (Bruck–Ryser) n'aurait aucune torsion, et L1 tuerait 99. » — Affaiblie par la géométrie t=3 à 42 sommets non planaire. |
| L09-COND-030 | une réflexion ponctuelle σ_x est forcément un automorphisme (F16) | C1 se ramène à C2 | C1 | O | `conway99-c1:main:notes/10_IDEES_F.md:33` | « Rigidité ⇒ symétrie : montrer qu'une réflexion ponctuelle σ_x est forcément un automorphisme, ce qui ramène C1 à C2 » |
| L09-COND-031 | dans le Fano tendu, branche « factorisation de Heawood » | P ≥ 24, donc exclue à P = 0 (Astra, dossier 2) | C1 (Fano tendu, P = 0) | E | `conway99-c1:main:JOURNAL.md:305-307` | « d'où la branche « factorisation de Heawood » du Fano tendu force P ≥ 24 : exclue à P = 0 » |
| L09-COND-032 | témoin « deux factorisations de Heawood affectées par parité » (Fano tendu) | meurt au niveau paire × bloc par une borne ordonnée (6 > 5), pour tout τ admissible (Astra, dossier 3) | C1 (Fano tendu) | P | `conway99-c1:main:JOURNAL.md:327-329` | « Ce témoin meurt au niveau paire × bloc par une borne ordonnée (6 > 5 pour y = {0.0, 2.0}, R = {0,1}), pour tout τ admissible. » |
| L09-COND-033 | C2 exclu (draft 7, 07/10) et C3 exclu (Lean) et Behbahani–Lam (ordres 7, 11 exclus) | tout srg(99,14,1,2) est asymétrique (C1 = tout le problème) | tous | P | `conway99-c1:origin/main:JOURNAL.md:665` | « Avec C3 (Lean) et Behbahani–Lam : tout srg(99,14,1,2) est asymétrique. C1 est désormais tout le problème. » — Dépend du statut de C2 (sessions IA, sans relecteur humain). |
| L09-COND-034 | chaque sommet a ≥ 4 étiquettes tordues (frontière complétée) — Σ\|W\| ≥ 792 | il suffirait Σ_{curl₀} g(κ) > −176 pour une contradiction (version approchée de l'évitement) | tous | P | `conway99-c1:main:notes/60_HODGE.md:86-87` | « Version approchée avec la frontière (si chaque sommet a ≥ 4 étiquettes tordues : Σ\|W\| ≥ 792) : il suffirait Σ_{curl₀} g(κ) > −176. » |
| L09-COND-035 | sur curl₀ le spectre comprimé évite (s', r') (énoncé muté) | P = P_max, grid-full, contradiction pour 99 (L1) | tous | P | `conway99-c1:main:notes/60_HODGE.md:84-86` | « pour un SRG, H3 donne alors −\|\|B\|\|² ≥ 0, donc P = P_max, grid-full, contradiction pour 99 (L1). » — Équivalent à F2-SRG (60:90-91). |
| L09-COND-036 | n₃ ≤ 395 (majoration de la torsion) | contradiction avec la frontière complétée (n₃ ≥ 396) ; a fortiori n₃ ≤ 704 contredit L16 (n₃ ≥ 705) | tous | P | `conway99-c1:main:notes/60_HODGE.md:121-122` | « pour 99, il faudrait n₃ ≤ 395 face à la frontière, qui donnerait n₃ ≥ 396 si elle est complétée » — La remarque « a fortiori L16 » est du consolidateur (n₃ = 4158 − 3P, P ≤ 1151). |
| L09-COND-037 | Σ_x\|W(x)\| ≤ 1409 (équivalent Σ\|W\| ≤ 1404, P ≥ 1152) | pas de Conway (contradiction avec L16) | tous | P | `conway99-c1:main:notes/80_ETINCELLE_ARITHMETIQUE.md:94-96` | « Avec L16, la non-existence équivaut à : la torsion moyenne par sommet est < 14,24, soit Σ_x \|W(x)\| ≤ 1409. » |
| L09-COND-038 | k ≤ 4 (rank₇(A − 3I) ≤ 19) | pas de Conway (car k ≥ 6, puis k ≥ 10) | tous | P | `conway99-c1:main:notes/97_K_ET_TORSION.md:99-101` | « toute preuve de k ≤ 4, c'est-à-dire rank₇(A − 3I) ≤ 19, prouverait la non-existence. » — Avec L20 ter : toute preuve de k ≤ 8 suffit (consolidateur). |
| L09-COND-039 | k = 10 | aucun τ_a de type (1;2,3) ni (4;2) en aucun sommet (test exact à une étoile) | tous | E | `conway99-c1:main:notes/97_K_ET_TORSION.md:157-159` | « Pour K = 10, le même test exclut encore les types (1;2,3) et (4;2) » |
| L09-COND-040 | k = 10 | m(e) ∈ {0,2} pour toute arête, \|W(x)\| ≥ 56 partout, P pair ≤ 462 (Corollaire C1) | tous | P | `conway99-c1:main:notes/100_SYNTHESE_DES_LEMMES.md:175-176` | « Si k = 10, alors pour toute arête e : m(e) ∈ {0, 2}. Donc \|W(x)\| ≥ 56 en tout sommet, et P est pair avec P ≤ 462. » |
| L09-COND-041 | k = 10 | chaque droite a d(L) ≥ 13 (Corollaire C2) ; contradiction si d(L) ≤ 12 était prouvé | tous | P | `conway99-c1:main:notes/100_SYNTHESE_DES_LEMMES.md:182-183` | « Si k = 10, chaque droite a d(L) ≥ 13, alors que le maximum trouvé numériquement est 9 » |
| L09-COND-042 | k ≤ 20 | toutes les droites sont 7-dégénérées (G(L) non connexe ou 7 \| τ(G(L))) ; et d(L) ≥ 3 sur les 231 droites (avec L23) | tous | P | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:79-80` | « Avec L21 : k ≤ 20 impose d(L) ≥ 3 sur les 231 droites » |
| L09-COND-043 | d(L) ≤ 9 pour toute droite (conjecture) | k ≥ 14 (et k = 14 imposerait d = 9 sur les 231 droites) | tous | O | `conway99-c1:main:notes/99_VERROU_BOULES_DE_DROITES.md:71-72` | « Si d ≤ 9 toujours, alors k ≥ 14 (et k = 14 imposerait d = 9 sur les 231 droites). Non prouvé » |
| L09-COND-044 | le minimum de rang du bloc « deux étoiles » sur toutes les holonomies est ≥ 11 | k ≥ 12 | tous | O | `conway99-c1:main:notes/97_K_ET_TORSION.md:169` | « Si le minimum réel sur toutes les holonomies est ≥ 11, alors k ≥ 12. » |
| L09-COND-045 | le couple (π(L), μ_L) = (0,0) est exclu pour toute droite | P = 0 serait exclu | tous | O | `conway99-c1:main:notes/99_VERROU_BOULES_DE_DROITES.md:112-113` | « si le couple (π, μ) = (0, 0) était exclu, P = 0 le serait aussi. » — Le modèle enraciné en une droite trouve (0,0) faisable : piste négative à ce niveau. |
| L09-COND-046 | une petite valeur de π(L) est impossible pour toute droite | borne inférieure sur P | tous | O | `conway99-c1:main:notes/99_VERROU_BOULES_DE_DROITES.md:111-112` | « Si une petite valeur de π(L) était impossible, toutes les droites porteraient beaucoup de prismes, d'où une borne inférieure sur P. » |
| L09-COND-047 | il existe un sous-graphe induit à 43 sommets de déterminant de Seidel premier à 7 | contradiction avec L22 (pas de Conway) | tous | P | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:126` | « Un sous-graphe induit à 43 sommets de déterminant de Seidel premier à 7 contredit L22. » |
| L09-COND-048 | un sous-graphe induit à 42 sommets a un déterminant de Seidel non carré mod 7 | k ≠ 28 | tous | P | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:127` | « Un sous-graphe à 42 sommets de déterminant non carré mod 7 contredit k = 28 » |
| L09-COND-049 | un sous-graphe induit à 40 sommets a un déterminant de Seidel carré non nul mod 7 | k ≠ 26 (et ainsi de suite : \|I\| = 14+k, caractère ≠ (−1)^{k/2} ⟹ k exclu) | tous | P | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:127-128` | « à 40 sommets, de déterminant carré non nul, il contredit k = 26 ; etc. » |
| L09-COND-050 | \|I\| > 14 + k | det S(Γ[I]) ≡ 0 (mod 7) | tous | P | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:124` | « Si \|I\| > 14 + k, det S(Γ[I]) ≡ 0. » |
| L09-COND-051 | k = 22 | R_L = 0 pour toute droite générique : Γ est déterminé mod 7 par une boule générique et les N_w | tous | P | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:136-137` | « À k = 22, R_L = 0 : tout Γ est déterminé mod 7 par une boule générique et les N_w. » |
| L09-COND-052 | k = 28 | pour u ∈ Λ₋₄ : 7 \| u·u ⟺ u mod 7 ∈ G ; U est un plan anisotrope | tous | P | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:84-85` | « À k = 28, β est non scindée de dim 42 et U est un plan anisotrope : pour u ∈ Λ₋₄, 7 \| u·u ⟺ u mod 7 ∈ G. » |
| L09-COND-053 | F induit 4-régulier à 10 sommets | contradiction (c(F) = −1 < 0, lemme de variance) | tous | P | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:64-66` | « tout graphe 4-régulier induit à 10 sommets aurait c = −1, il est donc interdit » |
| L09-COND-054 | deux grilles ont exactement une droite commune | aucune arête entre leurs parties propres (c = 0) | tous | P | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:65-66` | « deux grilles ayant exactement une droite commune : c = 0, donc aucune arête entre leurs parties propres » |
| L09-COND-055 | une coclique de taille 22 (borne de Hoffman) existe | il existe un 2-(22,4,2) à 77 blocs (chaque sommet extérieur a exactement 4 voisins dedans) | tous | P | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:67-69` | « À 99, coclique ≤ 22 ; si elle est atteinte, 2-(22,4,2) à 77 blocs » |
| L09-COND-056 | la conjecture des hexagones de Reimbayev (équivalente à (∗)) est vraie pour 99 | pas de Conway (via Makhnev 1988) | tous | R | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:57-58` | « Reimbayev (arXiv « hexagons », 2024) conjecture un nombre minimal d'hexagones qui équivaut à (∗). La conjecture entraînerait donc la non-existence via Makhnev. » — Forme famille réfutée le 07/10 par le nouveau srg(243,22,1,2) tordu (conway99-c1:origin/main:JOURNAL.md:631-633) ; forme propre à 99 ouverte. |
| L09-COND-057 | involution t de 99 à f = 1 point fixe | a₁ = 14 (t retourne les 7 droites en son point fixe, t = σ_x) | C2 | P | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:110-112` | « Si f = 1, on obtient a₁ = 14 : t retourne les 7 droites en son point fixe (t = σ_x). » |
| L09-COND-058 | involution t fixant une droite (f = 3) | Σ_w φ_w = 10 retournements (n'exclut pas le cas) | C2 | P | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:115` | « Si une droite est fixe (f = 3), l'identité donne Σ_w φ_w = 10 retournements, sans exclure le cas. » |
| L09-COND-059 | chaque Q_R (R paire de classes) est pair (dans une jauge) | L8 démontré (21 nombres pairs de somme 105) | tous (point de Hamming) | P | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:222` | « Si chaque Q_R était pair, L8 serait démontré (21 nombres pairs de somme 105). » — Dépassé : L8 démontré en notes/105. |
| L09-COND-060 | les corrections dues à la torsion (arêtes τ et d'holonomie) dans le comptage mod 2 sur les 105 triplets (i;j,k) d'un sommet sont paires | contradiction pour C1 tout entier (partie constante 105·3 ≡ 1) | C1 (tous) | O | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:207-210` | « La fin du pont, pour C1 tout entier, est donc un comptage modulo 2 sur les 105 triplets (i ; j, k) d'un sommet quelconque. Sa partie constante vaudrait 105·3 ≡ 1 » — Programme spéculatif : la même somme est impaire pour BvLS (m=11) qui existe (103:229-231) ; il faudrait la rigidité propre à m = 7. |
| L09-COND-061 | Γ est partitionné en 11 grilles induites à couplages tous anti-isomorphismes | il existe un plan projectif d'ordre 10 : impossible (Lam) | tous | P | `conway99-c1:main:notes/104_TISSU_DE_GRILLES.md:44-45` | « Si tous les M_ij sont des anti-isomorphismes, il existe un plan projectif d'ordre 10. Donc (Lam–Thiel–Swiercz 1989) ce régime est impossible. » |
| L09-COND-062 | deux grilles disjointes S, S′ sont reliées par un anti-isomorphisme | w ↦ (voisin dans S, voisin dans S′) est une bijection des 81 autres sommets sur S × S′ | tous | P | `conway99-c1:main:notes/104_TISSU_DE_GRILLES.md:115-117` | « Si deux grilles disjointes S, S′ sont reliées par un anti-isomorphisme, l'application w ↦ (voisin dans S, voisin dans S′) est une bijection des 81 autres sommets sur S × S′. » |
| L09-COND-063 | α(Γ) = 22 (coclique de Hoffman) | le complément induit a spectre 10¹,3³³,(−1)²¹,(−4)²², toute grille coupe la coclique en 2 points | tous | P | `conway99-c1:main:notes/104_TISSU_DE_GRILLES.md:130-133` | « Si α(Γ) = 22 ... le sous-graphe induit sur ces 77 sommets a pour spectre 10¹, 3³³, (−1)²¹, (−4)²² » |
| L09-COND-064 | il existe un ensemble −4-serré avec c ∈ {3,…,6} | il témoigne de U ≠ 0 (défaut de L22) ; à k = 28 contraintes \|C∩S\| ≡ 4c mod 7 | tous | P | `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L22.md:29-30` | « Un seul ensemble serré avec c ∈ {3,…,6} témoigne donc de U ≠ 0. » |
| L09-COND-065 | k = 28 et C, C′ deux cocliques de Hoffman distinctes | \|C ∩ C′\| ∈ {1, 8, 15} | tous | P | `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L22.md:37` | « (a) deux cocliques de Hoffman distinctes se coupent en 1, 8 ou 15 sommets » |
| L09-COND-066 | k = 28, C coclique de Hoffman, S c-serré | \|C ∩ S\| ≡ 4c (mod 7) | tous | P | `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L22.md:38` | « (b) pour toute coclique de Hoffman C et tout ensemble c-serré S : \|C ∩ S\| ≡ 4c (mod 7) » |
| L09-COND-067 | k = 28 | trois ensembles serrés quelconques ont un Gram 3×3 de déterminant ≡ 0 (mod 7) ; le défaut de L22 n'est pas porté par des cocliques de Hoffman | tous | P | `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L22.md:39-41` | « (d) trois ensembles serrés quelconques ont un Gram 3 × 3 de déterminant ≡ 0 (mod 7). » |
| L09-COND-068 | S serré σ-invariant (involution σ, C2) | S est réunion d'orbites, contient le point fixe ssi c impair ; jamais σS = S^c | C2 | P | `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L22.md:44-45` | « Un ensemble serré σ-invariant est une réunion d'orbites, plus éventuellement le point fixe x, qu'il contient si et seulement si c est impair. » |
| L09-COND-069 | l'ensemble 𝒩 des grilles incomplètes en x est non vide et deux à deux sécant (étoile ou triangle) | contradiction (lemme D1) | tous | P | `conway99-c1:main:notes/108_DEFAUTS_ET_COMPTAGE_DES_FENTES.md:51-59` | « Si 𝒩 ≠ ∅, 𝒩 contient deux paires disjointes. » |
| L09-COND-070 | 𝒩 = {αy, αδ, δw} (configuration chemin) | contradiction (lemme D2) ; d'où g(x) ≤ 17 | tous | P | `conway99-c1:main:notes/108_DEFAUTS_ET_COMPTAGE_DES_FENTES.md:67-88` | « le chemin 𝒩 = {αy, αδ, δw} ... Contradiction. » |
| L09-COND-071 | \|𝒩\| = 4 | 𝒩 est un 4-cycle de classes ; il reste 20 configurations pour g(x) = 17 (motifs (0,2,0,2) : 8 ; (2,2,2,2) : 12) | tous | E | `conway99-c1:main:notes/112_VERS_G16_MOTIFS_A_QUATRE_DEFAUTS.md:31-32` | « Donc \|𝒩\| = 4 ⟹ 𝒩 = 4-cycle 0–1–2–3 » |
| L09-COND-072 | T₀ ≠ ∅ et T₁ ≠ ∅ (classes voisines du 4-cycle 𝒩 toutes deux tordantes) | \|T₀\| = \|T₁\| = 2 et les ombres sont des échanges (lemme A) | tous | P | `conway99-c1:main:notes/112_VERS_G16_MOTIFS_A_QUATRE_DEFAUTS.md:37-38` | « Si T₀ ≠ ∅ et T₁ ≠ ∅, alors \|T₀\| = \|T₁\| = 2. » |
| L09-COND-073 | T₀ = ∅, T₂ = ∅ et b ∈ T₁ (4-cycle 𝒩) | \|T₁\| = \|T₃\| (lemme B) | tous | P | `conway99-c1:main:notes/112_VERS_G16_MOTIFS_A_QUATRE_DEFAUTS.md:47-48` | « Si de plus T₂ = ∅, alors ρ₀ envoie T₁ dans T₃ et T₃ dans T₁, injectivement, et donc \|T₁\| = \|T₃\|. » |
| L09-COND-074 | le graphe de classes commun des deux torsions (L14) a un 2-cycle {c,c′} et les trois doubles de Q₀c s'apparient à Q₁c′ | contradiction (bloc étanche, offre 4 < demande 5) | tous | P | `conway99-c1:main:notes/111_L14_C2_A_LA_MAIN.md:80-82` | « La contradiction suit dès que les trois doubles de Q₀c s'apparient à Q₁c′. Cet appariement est automatique pour m = 2 ; pour m ≥ 4, il reste à prouver. » |
| L09-COND-075 | une σ-arête interne à une droite du modèle de Fano | e ≥ 13 : contradiction avec le lemme du triangle | C1 (Fano) | P | `conway99-c1:main:notes/115_LEMME_DU_TRIANGLE.md:76` | « une seule σ-arête interne à une droite donne e ≥ 13 : contradiction » |
| L09-COND-076 | famille triangle tendue (e = 12) | Aq = 3q, T 2-régulier, comptes exacts 1 et 3 | tous | P | `conway99-c1:main:notes/115_LEMME_DU_TRIANGLE.md:48-51` | « Cas tendu, e = 12. Alors Sq = 0, soit Aq = 3q. » |
| L09-COND-077 | σ_i respecte l'appariement de Fano P_i | contradiction (y a au moins 4 voisins dans son bloc contre 2 exigés) : tout σ_i mélange les blocs | C1 (Fano) | P | `conway99-c1:main:notes/114_LABO_EXPERIMENTAL_GRAPHE_LOINTAIN.md:67-69` | « Donc tout σ_i mélange les blocs. » |
| L09-COND-078 | le système (P2) par types est infaisable pour des données locales (τ,σ) | ces données sont impossibles en tout sommet de tout srg(99,14,1,2) | tous | P | `conway99-c1:main:notes/117_P2_PAR_TYPES_TORSION_MAXIMALE.md:29-30` | « Toute configuration réelle donne un point entier de ce système : infaisable ⟹ ces données (τ, σ) sont impossibles » |
| L09-COND-079 | un sommet est de Fano tendu | les 21 petits systèmes « cellules par bloc » doivent tous être faisables (aucun cas testé ne l'est) | C1 (Fano tendu) | E | `conway99-c1:main:notes/118_PAIRE_BLOC_ET_OBSTRUCTION_PSI.md:90-92` | « Un sommet de Fano tendu exige que ces 21 petits systèmes soient tous faisables, ce qui n'arrive dans aucune configuration testée. » |
| L09-COND-080 | tout sommet de Fano tendu | ⟨rhs_R, Ψ_R⟩ = 0 pour chaque bloc R | C1 (Fano tendu) | P | `conway99-c1:main:notes/118_PAIRE_BLOC_ET_OBSTRUCTION_PSI.md:65` | « D'où, à tout sommet de Fano tendu et pour chaque R : ⟨rhs_R, Ψ_R⟩ = 0. » |
| L09-COND-081 | un sommet est de Fano tendu | P-Ψ : 84 conditions θ(z_X(y)) + θ(z_Y(y)) = 0 | C1 (Fano tendu) | P | `conway99-c1:main:notes/119_PSI_PAR_PAIRE_FANO_TENDU.md:29-33` | « Lemme P-Ψ ... θ(z_X(y)) + θ(z_Y(y)) = 0 » |
| L09-COND-082 | pour tout σ tendu (F5, KBLDP), au moins une droite a un système F₂ (P-Ψ) incompatible | aucun sommet de Fano tendu | C1 | O | `conway99-c1:main:notes/119_PSI_PAR_PAIRE_FANO_TENDU.md:95-96` | « Le lemme « aucun sommet de Fano tendu » revient à ceci » |
| L09-COND-083 | on trouve un sous-réseau V ⊂ K de rang ≥ 30 sur lequel H − 3 est injective mod 7 | k ≥ 30, contradiction avec L22 (pas de Conway) | tous | O | `conway99-c1:main:notes/120_TRIADES_ET_VECTEURS_PROPRES_CELLULAIRES.md:33-34` | « Si l'on trouvait un sous-réseau V ⊂ K de rang ≥ 30 sur lequel H − 3 est injective mod 7, on aurait k ≥ 30, ce qui contredit L22. » |
| L09-COND-084 | la structure « arc-en-ciel » des composantes de K (Astra) est forcée à P = 0 | 3-coloration des étiquettes en x avec c(u) ≠ c(ū) et c(u) ≠ c(τ_v(u)) | C1 (P = 0) | O | `conway99-c1:main:notes/121_POINT_D_ETAPE_26_09.md:54-55` | « Si elle était forcée, elle donnerait en x une 3-coloration des étiquettes avec c(u) ≠ c(ū) et c(u) ≠ c(τ_v(u)). » |
| L09-COND-085 | poids(d(L)) = 1 pour une droite d'un sommet de Fano tendu | T(L) contient un triangle : λ = 1 violé | C1 (Fano tendu) | P | `conway99-c1:main:notes/122_FANO_DIFFERENCES_DE_RETOURNEMENT.md:24-25` | « Si poids(d(L)) = 1, T(L) contient un triangle. » |
| L09-COND-086 | toutes les droites d'un sommet de Fano tendu sont tout-CM cycliques | S = {Z : p_Z = 2} est ∅, le complémentaire d'une droite, d'un point, ou tout le plan | C1 (Fano tendu) | P | `conway99-c1:main:notes/122_FANO_DIFFERENCES_DE_RETOURNEMENT.md:87-88` | « Si toutes les droites sont tout-CM cycliques, le §1 impose que S = {Z : p_Z = 2} ne rencontre aucune droite en exactement un point. » |
| L09-COND-087 | P ≥ 1152 | H ≤ 209 988 (hexagones induits) ; équivalence | tous | P | `conway99-c1:main:notes/123_PORTE_IX_TORSION_MAXIMALE.md:29` | « Le plafond visé par notes/100 (P ≥ 1152) équivaut donc à H ≤ 209 988. » |
| L09-COND-088 | pour toute donnée de droite (C, τ_u, τ_ū, σ_U) avec d(L) = 1, il n'existe pas de bijections d'ombre et graphe lointain λ/μ-cohérent avec rang₇ R_L ≤ 6 (« non » uniforme au dossier n° 5) | k ≥ 30, contradiction avec L22 — sauf si les 231 droites sont 7-dégénérées (cas forcé si k ≤ 20, à exclure à part) | tous | O | `conway99-c1:main:notes/124_LOINTAIN_D_UNE_DROITE_SCHUR.md:61-65` | « Un « non » uniforme donnerait k ≥ 30, en contradiction avec L22. Il resterait le cas où les 231 droites sont 7-dégénérées. » |
| L09-COND-089 | k = 22 | le graphe lointain d'une droite générique est fixé mod 7 par les seules ombres | tous | P | `conway99-c1:main:notes/124_LOINTAIN_D_UNE_DROITE_SCHUR.md:70-71` | « À k = 22, il est même fixé mod 7 par les seules ombres. » |
| L09-COND-090 | P = 0 | S = Σ_L c₄(G(L)) (seconde variable libre d'ordre 7 = nombre total de 4-cycles des 231 graphes de droites) | tous | P | `conway99-c1:main:notes/125_CYCLES_COURTS_DES_GRAPHES_DE_DROITES.md:53` | « À P = 0, la seconde variable libre d'ordre 7 est le nombre total de 4-cycles des 231 graphes cubiques G(L). » |
| L09-COND-091 | P = S = 0 | tous les G(L) ont maille ≥ 5 ; profils (4,4,4) et (4,8) exclus ; restent connexe et (6,6) | tous | P | `conway99-c1:main:notes/125_CYCLES_COURTS_DES_GRAPHES_DE_DROITES.md:86-89` | « Les profils (4,4,4) et (4,8) sont exclus. » |
| L09-COND-092 | k ≤ 20 | toute droite vérifie r₀(L) ≥ 2 + r(L) (au moins deux vecteurs propres mod 7 équilibrés portés par N(L)) | tous | P | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:47-49` | « k ≤ 20 ⟹ toute droite vérifie r₀(L) ≥ 2 + r(L). » |
| L09-COND-093 | une droite connexe a une torsion t dont aucune partie n'est équilibrée | k ≥ 22 + t (ex. 7 \| τ une fois ⟹ k ≥ 24) | tous | P | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:51-54` | « k ≥ 22 + t si toute la torsion est non équilibrée » |
| L09-COND-094 | P = S = 0 et une droite de profil (6,6) | k ≥ 22 | tous | E | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:66-82` | « À P = S = 0, une droite (6,6) force k ≥ 22 » |
| L09-COND-095 | P = 0 et une droite (4,8) dont la composante à 8 étiquettes ne porte pas de torsion équilibrée | k ≥ 22 | tous | E | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:94-97` | « une droite (4,8) force k ≥ 22, sauf si sa composante à 8 étiquettes porte une torsion équilibrée (non testé » |
| L09-COND-096 | P = 0 et k = 20 | chaque droite est (4,4,4) ou porte une torsion équilibrée ; sans torsion équilibrée « (4,4,4) partout », impossible par le lemme R | tous | P | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:98-99` | « k = 20 impose que chaque droite soit (4,4,4), ou porte de la torsion équilibrée. » |
| L09-COND-097 | P = 0 et k ≤ 18 | chaque droite porte au moins 3 ou 4 vecteurs de torsion équilibrés | tous | P | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:98` | « À P = 0, k ≤ 18 impose donc à chaque droite au moins 3 ou 4 vecteurs de torsion équilibrés » |
| L09-COND-098 | k = 22 et une droite connexe sans torsion équilibrée | la droite est générique (donc soumise à l'obstruction de l'étoile d'Astra) | tous | P | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:104-105` | « à k = 22, toute droite connexe sans torsion équilibrée est générique » |
| L09-COND-099 | P = S = 0, k = 22, (i) aucune torsion équilibrée sur les droites connexes, (ii) obstruction uniforme de l'étoile pour les droites génériques | les 231 droites sont (6,6) avec \|t₁ − t₂\| ≤ 1 et ρ ≤ 1 ; il resterait à exclure « (6,6) partout » | tous | P | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:110-112` | « Alors les 231 droites sont (6,6), avec \|t₁ − t₂\| ≤ 1 et ρ ≤ 1. » |
| L09-COND-100 | hypothèse (NT) (seuls vecteurs équilibrés = différences de composantes) | k ≥ 18 ; k = 18 ⟹ c(L) ≥ 5 partout, P ≥ 924, \|W(x)\| ≤ 28, motif (2,…,2) ; k = 20 ⟹ c(L) ≥ 3 partout | tous | P | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:131-137` | « Sous (NT), on a k ≥ 22 + r − r₀ ≥ 23 − c(L) pour chaque droite. Donc : k ≥ 17, soit k ≥ 18 » |
| L09-COND-101 | (NT) et k = 18 (P quelconque) | contradiction (saturation, notes/128 §3 bis) : k ≥ 20 en général | tous | P | `conway99-c1:main:notes/128_RIGIDITE_444.md:62-76` | « Preuve que k = 18 est impossible (sous NT). » — §3 bis non relu (128:89-90). |
| L09-COND-102 | (NT) et P = 0 | k ≥ 22 (programme réduit à k ∈ {22, 24, 26, 28}) | tous | P | `conway99-c1:main:notes/128_RIGIDITE_444.md:81-82` | « À P = 0, le programme 7-adique se réduit à k ∈ {22, 24, 26, 28}, à la seule condition NT. » |
| L09-COND-103 | (a′) uniforme (étoile complète impossible pour toute boule générique à k = 22) + (NT) + exclusion de « toute droite non connexe » | k ≠ 22 | tous | O | `conway99-c1:main:notes/127_CARTE_DU_PROGRAMME_7_ADIQUE.md:50-52` | « (a′) uniforme ⟹ pas de droite générique à k = 22. Avec NT, toute droite est alors non connexe. Exclure « toute droite non connexe » (question locale) ferme k = 22. » |
| L09-COND-104 | P = 0 et les 7 droites par x sont (4,4,4) | σ_C(v) = v̄ partout et S(x) = 84 (lemme R) ; deux tels sommets jamais voisins | tous | P | `conway99-c1:main:notes/128_RIGIDITE_444.md:8-9` | « Lemme R. À P = 0, si les 7 droites par x sont (4,4,4), alors σ_C(v) = v̄ pour toute classe C et toute v ∉ C. » |
| L09-COND-105 | P = 0 et k ≤ 20 | au moins 26 droites portent une torsion 7 équilibrée (inconditionnel) | tous | P | `conway99-c1:main:notes/128_RIGIDITE_444.md:12` | « Corollaire 4 (inconditionnel). À P = 0 et k ≤ 20, au moins 26 droites portent une torsion 7 équilibrée » |
| L09-COND-106 | involution (C2) : Λ_{T,−4} est 7-isotrope | l'involution meurt (critère équivalent) | C2 | P | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:145-146` | « L'involution meurt ssi tout vecteur propre −4 entier et impair f vérifie Σ_o f_o² ≡ 0 (mod 7) » |
| L09-COND-107 | involution (C2), sous « NT impair » (r₀_c = 0), un bloc a dim ker Q_c ≥ 3 | l'involution meurt ; dim ker Q_c ∈ {1,2} force g = 20 | C2 | P | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:106-107` | « Sous « NT impair » (r₀_c = 0) : un bloc avec dim ker Q_c ≥ 3 tue l'involution » |
| L09-COND-108 | involution (C2), bloc générique de det Q_c carré | g⁻ = 20 | C2 | P | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:71` | « Un bloc générique de det Q_c carré force g⁻ = 20. » |
| L09-COND-109 | involution (C2), g⁻ = 18 | (det Q_c \| 7) = −1 pour les blocs génériques ; mineurs d'ordre 19 et 20 nuls, d'ordre 18 nuls ou non carrés | C2 | P | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:68` | « ρ⁻ = 0 ⟹ (det Q_c \| 7) = −1. » |
| L09-COND-110 | involution (C2), deux blocs pleins c, d forment une paire frère | conditions (a)–(d) sur le bloc croisé Σ ; énoncé candidat : impossible | C2 | H | `conway99-c1:main:notes/131_ENTRELACEMENT_ALT_ET_RESIDUS_LOINTAINS.md:120-121` | « Énoncé candidat. Aucun bloc croisé Σ ne satisfait (a)–(d). Donc deux blocs pleins ne forment jamais une paire frère » |
| L09-COND-111 | involution (C2), Σ = ∅ | au plus un bloc A111111 | C2 | P | `conway99-c1:main:notes/131_ENTRELACEMENT_ALT_ET_RESIDUS_LOINTAINS.md:45-48` | « Si c′ est aussi A111111, alors τ_c′(c+) = c− et η_c′(c+) = c−. La paire cc′ est donc frère, ce qui est exclu quand Σ = ∅. » |
| L09-COND-112 | involution (C2), g = 16 | chaque bloc dans l'un de 4 régimes ; aucun type (τ, η) à t ≥ 2 n'admet de solution locale : contradiction | C2 | C | `conway99-c1:main:notes/132_G16_IMPOSSIBLE.md:9-11` | « g⁻ ≠ 16. Donc g⁻ ∈ {18, 20}. » |
| L09-COND-113 | involution (C2), g = 18 | aucun bloc plein ; tout bloc t = 0 est scindé (det Q_c non carré) et toutes ses lignes lointaines sont rigides (T_FF ≡ Z) | C2 | P | `conway99-c1:main:notes/133_REGIMES_Q7_ET_U_SIGNE.md:21` | « scindé (det Q_c non carré), ρ = 0 : T_FF ≡ Z, toutes les lignes lointaines rigides » |
| L09-COND-114 | involution (C2), un bloc plein (τ = η) ou une ÉTL t = 0 à det carré | g⁻ = 20 | C2 | P | `conway99-c1:main:notes/133_REGIMES_Q7_ET_U_SIGNE.md:27-29` | « Un bloc plein (τ = η) est à t = 0 et det ≡ 1 (carré), donc force g = 20. À g = 18 il n'y a aucun bloc plein » |
| L09-COND-115 | involution (C2), g⁺ ∉ {14, 16} | g⁺ ≥ 18, k ≥ g⁻ + 4 ≥ 22 ; k = 22 ⟹ g⁻ = g⁺ = 18 (cas doublement rigide) | C2 | P | `conway99-c1:main:notes/135_SECTEUR_PAIR_Q7.md:54-56` | « Si g⁺ ∉ {14, 16} : g⁺ ≥ 18, donc k ≥ g⁻ + 4 ≥ 22 sans hypothèse de droite générique, et k = 22 ⟹ g⁻ = g⁺ = 18. » |
| L09-COND-116 | involution (C2), 42 + 2\|Σ\| − 2n_dis > 28 | un bloc au moins a ≥ 6 pivots | C2 | P | `conway99-c1:main:notes/136_ECHELLE_DES_PIVOTS.md:41-42` | « si 42 + 2\|Σ\| − 2n_dis > 28, elle dépasse 4, et par parité un bloc au moins a ≥ 6 pivots. » |
| L09-COND-117 | involution (C2), système local UNSAT sur les 156 types à ≥ 6 pivots | n_dis ≥ \|Σ\| + 7 dans toute configuration ; UNSAT sur les 79 types pertinents ⟹ famille Σ = ∅ « tout un bloc » morte | C2 | S | `conway99-c1:main:notes/136_ECHELLE_DES_PIVOTS.md:18-20` | « Système local UNSAT sur les 156 types à ≥ 6 pivots ⟹ n_dis ≥ \|Σ\| + 7 dans toute configuration » |
| L09-COND-118 | involution (C2), toutes les instances I(τ) (3 308 classes ; puis (A) 1 507 types + (B) tout-dis) UNSAT | aucune involution (C2 exclu) | C2 | P | `conway99-c1:main:notes/137_LIGNE_D_ARRIVEE_C2.md:45-47` | « Donc si toutes les I(τ) sont UNSAT, il n'y a pas d'involution. » |
| L09-COND-119 | involution (C2), le bloc lourd (argmax lexicographique) est une étoile libre | la configuration est tout-dis : n_dis = 21, Σ = ∅, 7 étoiles libres à d = 12 | C2 | P | `conway99-c1:main:notes/137_LIGNE_D_ARRIVEE_C2.md:56-59` | « Si c'est une étoile libre, la configuration est TOUT-DIS » |
| L09-COND-120 | involution (C2), les 156 enveloppes de la ligne (C) tombent | tout le cas involution tombe, sans types de blocs | C2 | P | `conway99-c1:main:notes/139_LIGNE_C_ENVELOPPES.md:4-5` | « Si les 156 enveloppes tombent, TOUT le cas involution tombe, sans types de blocs. » |
| L09-COND-121 | ligne (C) : une composante D_n de U avec n(n − 1)/2 > h₁ + h₂ − 2 (ou version raffinée) | aucun u n'a de projection spinorielle sur D_n ; ses n axes tombent dans N⊥ (dim 2) : contradiction pour n ≥ 3 | C2 | P | `conway99-c1:main:notes/139_LIGNE_C_ENVELOPPES.md:55-57` | « Aucun u ne peut avoir de projection spinorielle sur une composante D_n dès que n(n − 1)/2 > h₁ + h₂ − 2. » |
| L09-COND-122 | ligne (C) : U contient un E8 | span(E8) ⊥ N et ⊂ N⊥ (dim 2) : contradiction | C2 | P | `conway99-c1:main:notes/139_LIGNE_C_ENVELOPPES.md:47-48` | « par (M), toutes les projections des u sur E8 sont nulles, donc span(E8) ⊥ N, et span(E8) ⊂ N⊥ qui est de dimension 2. » |
| L09-COND-123 | ligne (C) : enveloppe décomposable | exclue (Gram projetée G₁² = 7G₁) | C2 | P | `conway99-c1:main:notes/140_LIGNE_C_PACKING_CONNEXITE.md:74` | « Décomposable ⇒ exclu : la preuve générale est celle de « structures » (Gram projetée G₁² = 7G₁). » |
| L09-COND-124 | ligne (C) : Σ_u (r/8 − E(u)) > 24·min(h₁,h₂) − r pour toute famille de 42 vecteurs de norme 3 | l'enveloppe est exclue (packing) | C2 | P | `conway99-c1:main:notes/140_LIGNE_C_PACKING_CONNEXITE.md:37-38` | « Σ_u (r/8 − E(u)) ≤ 24·min(h₁,h₂) − r. » |
| L09-COND-125 | ligne (C) : enveloppe rigide (Coxeter égaux) | E(x) = h\|x\|², m(x) = 0, B₁ = hits(y₁) ⊔ hits(y₂), chaque y a 4h + 8 hits | C2 | P | `conway99-c1:main:notes/141_LIGNE_C_LEMME_Z_ETAGES.md:49-56` | « tout x de norme 3 a m(x) = 0 » |
| L09-COND-126 | famille rigide D₂ₘ ⊃ D_m², un bloc à s = 2 forcé a \|κ\| = 3/2 (E₃xF₁, E₁xE₄, E₁=E₄, E₂=E₃ avec \|O₁∩O₂\| = 1) | la paire est morte (corollaire du lemme K) | C2 | P | `conway99-c1:main:notes/143_LEMME_PI_FAMILLE_D2M.md:81-84` | « Si un bloc de s = 2 FORCÉ a \|κ\| = 3/2, la paire est morte. » |
| L09-COND-127 | 132 : un bloc à \|κ\| = 1 | le bloc meurt (lemme T) | C2 | P | `conway99-c1:main:notes/143_LEMME_PI_FAMILLE_D2M.md:154` | « Donc tout bloc à \|κ\| = 1 meurt dans 132. » |
| L09-COND-128 | rank-17 : min K* ≥ 9/7 est démontré | les 1 272 (V, y-paires) sont tuées (C2 exclu par la route rank-17) | C2 | O | `conway99-c1:main:notes/150_ECHELLE_KSTAR_ET_COUPURE_2_5.md:10` | « Les 780 paires non tuées par min K* ≥ 5/7 ont min 7\|κ\|² ∈ {5, 6, 7, 8} ... donc min K* ≥ 9/7 tue les 1 272 » |
| L09-COND-129 | rank-17 : R5 tient (run cut25 à 0 survivant) | les 412 classes à témoin n=5 meurent, il en reste 342 (239 min-6, 83 min-8, 20 min-7) | C2 | O | `conway99-c1:main:notes/154_2x5_ENGINE_AND_ROUTE_CHANGE.md:105-106` | « R5 is proven if every orbit ends with "survivors 0". Then the 412 classes ... die, leaving 342 » |
| L09-COND-130 | rank-17 : R6 ∧ R8 démontrés | les 754 classes ouvertes sont toutes couvertes (C2 exclu) | C2 | O | `conway99-c1:main:notes/151_R6_PROGRAMME_J_CELLS.md:283-284` | « R6 ∧ R8 covers all 754 » |
| L09-COND-131 | rank-17 : R8 k=2/k=3 prouvés (témoins n=8 en k=1 seulement) | A11E6p:8 passe de 1,2·10¹⁰ à 2,1·10⁶ feuilles (~30 min par classe) ; avec J2 clos : 0 squelette | C2 | H | `conway99-c1:main:notes/154_2x5_ENGINE_AND_ROUTE_CHANGE.md:120-123` | « With R8 k=2/k=3 proven (n=8 witnesses k=1 only): 2.1e6, ~30 min per class. With J2 closed as well: 0 skeletons. » |
| L09-COND-132 | J1a, J2, J3 : le Gram de support M_U est de rang déficient | chaque autre étiquette Y a une ligne exactement orthogonale au noyau de M_U, et les résidus forment un repère ajusté de R^{15−r} de constante 28 (complétion de coquille) | C2 | P | `conway99-c1:main:notes/152_J1a_CLOSED_EXHAUSTIVE_PSD.md:42-47` | « (K) z ∈ ker M_U implies z ∈ ker M_full, so m_Y·z = 0 EXACTLY (in integers). » |
| L09-COND-133 | srg(v,k,λ,μ) à valeurs propres entières, d = r − s impair, v₂(k − θ′) ≥ v₂(v) | m_θ pair et (−1)^{m_θ/2}·det Λ_θ ≡ 1 (mod 4) ; ensembles violant ceci inexistants | autres srg (pas 99 : ne force que k pair) | P | `conway99-structures-lab:master:NOTE_S5_DISCRIMINANT_MOD4.md:13-16` | « Supposons d impair et v₂(k − θ′) ≥ v₂(v) (automatique si v est impair). » |
| L09-COND-134 | tout premier divisant n est ≡ 1 (mod 4) et e impair | pas de graphe de type Latin négatif NL_e(n) | famille infinie de srg | P | `conway99-structures-lab:master:NOTE_S5_DISCRIMINANT_MOD4.md:20-22` | « il n'existe pas de graphe de type Latin négatif NL_e(n) » |
| L09-COND-135 | structure D tout-tordue à circuits simples (Σ = ∅, toutes paires tordues) | aucune involution de ce type (≥ 3 triangles et 2 triangles : à la main ; 1 triangle : 84 certificats ; 0 triangle : 14 certificats) | C2 (tout-tordu, circuits simples) | C | `conway99-structures-lab:master:JOURNAL.md:208-209` | « ≥ 2 triangles à la main (S8, S11) ; 1 triangle, 84 certificats » — Le cas non simple reste ouvert (erratum 27/09). |
| L09-COND-136 | les 7 types locaux (0,6) (tier06) sont UNSAT | le cas tout-tordu non simple est couvert | C2 | O | `conway99-structures-lab:master:NOTE_S8_TOUT_TORDU.md:9` | « Il est couvert si les 7 types locaux (0,6) (tier06) sont UNSAT. » |
| L09-COND-137 | chaîne de trois triangles T₁ – T – T₃ dans la décomposition tout-tordue | décomposition impossible (orbite morte, −4 = 0) | C2 | P | `conway99-structures-lab:master:NOTE_S8_TOUT_TORDU.md:98-100` | « Toute décomposition contenant une chaîne de trois triangles » |
| L09-COND-138 | deux triangles disjoints dans une décomposition tout-tordue | impossible | C2 | P | `conway99-structures-lab:master:NOTE_S8_TOUT_TORDU.md:121-122` | « Une décomposition tout-tordue qui contient deux triangles disjoints est » |
| L09-COND-139 | configuration de Fano tendu | I_R = 0 pour les 21 blocs (condition nécessaire exacte, sans PL) | C1 (Fano tendu) | P | `conway99-structures-lab:master:JOURNAL.md:257-258` | « toute configuration de Fano tendu doit vérifier I_R = 0 pour les 21 blocs » |
| L09-COND-140 | branche « factorisation de Heawood » du Fano tendu | P ≥ 24, donc exclue à P = 0 | C1 (torsion maximale) | P | `conway99-structures-lab:master:JOURNAL.md:372` | « Conséquence : la branche « factorisation de Heawood » du Fano tendu force P ≥ 24 » |
| L09-COND-141 | revêtement de K₇ avec λ = 1, μ ≤ 2 et sans prisme | degré ≥ 5 ; à P = 0, composantes de H de degrés 12, 5 + 7 ou 6 + 6 | C1 (Fano tendu) | P | `conway99-structures-lab:master:JOURNAL.md:408-410` | « un revêtement de K₇ avec λ = 1, μ ≤ 2 et sans prisme a un degré ≥ 5 » |
| L09-COND-142 | carré dis de profil (2,1) | aucun apex dans T ; un apex intérieur force l'autre à l'extérieur ; 3h ≤ 2n_dis | C2 (dis) | P | `conway99-structures-lab:master:JOURNAL.md:465-468` | « (2,1) ⇒ aucun apex dans T » |
| L09-COND-143 | R_L (60 × 60 mod 7, rang k − 22) : réponse « non » uniforme à l'existence d'ombres et d'un graphe lointain 8-régulier de rang ≤ 6 | k ≥ 30, contre L22 (donc contradiction) | C1 (7-adique, hors droites 7-dégénérées) | O | `conway99-structures-lab:master:JOURNAL.md:450-452` | « Un « non » uniforme donnerait k ≥ 30, contre L22. » |
| L09-COND-144 | SRG réelle (dossier 5 d'Astra) | MR = 0 automatique (Q² ≡ 0 mod 7) ; k = 24 est un problème de construction complet | C1 (7-adique) | P | `conway99-structures-lab:master:JOURNAL.md:523-524` | « MR = 0 est automatique dans une vraie SRG » |
| L09-COND-145 | R = 0 (resp. MR = 0 et rang ≤ 2) dans la boule 7-adique | SRG exacte ; un échange de ≤ 6 ombres force deux prismes | C1 (7-adique) | P | `conway99-structures-lab:master:JOURNAL.md:521-522` | « §2 (R = 0 ⇒ SRG exacte), §3 (MR = 0 et rang ≤ 2 ⇒ SRG exacte) » |
| L09-COND-146 | k = 24 et τ carré | \|J_bad\| ≥ 8 ; par étoile j_a = 0 ou j_a ≥ 2 | C1 (7-adique) | P | `conway99-structures-lab:master:JOURNAL.md:589` | « à k = 24 avec τ carré, \|J_bad\| ≥ 8 » |
| L09-COND-147 | P = 0 et un sommet dont les 7 droites sont (4,4,4) | σ_C = mate partout, S(x) = 84 ; deux tels sommets jamais voisins ; « (4,4,4) partout » impossible ; sous NT et P = 0 : k ≥ 22 | C1 | P | `conway99-structures-lab:master:JOURNAL.md:630-632` | « deux tels sommets ne sont jamais voisins » |
| L09-COND-148 | NT (droites connexes) | k ≥ 18 ; à P = 0 : k ∈ {22, 24, 26, 28} | C1 | P | `conway99-structures-lab:master:JOURNAL.md:633-635` | « Sous NT, k ∈ {22, 24, 26, 28} » |
| L09-COND-149 | NT, k = 20 et une droite à exactement 3 composantes | ρ(L) = 0, t = 0 : droite construction-complète (machinerie de l'étoile applicable) | C1 | P | `conway99-structures-lab:master:JOURNAL.md:680-682` | « Toute droite à exactement 3 composantes ((4,4,4), (2,4,6) ou (2,2,8)) a donc ρ = 0 et t = 0 » |
| L09-COND-150 | une droite-bloc générique (involution) | g⁻ ∈ {18, 20} | C2 | P | `conway99-structures-lab:master:JOURNAL.md:697-698` | « Donc g⁻ ∈ {18, 20} dès qu'une droite-bloc est générique. » |
| L09-COND-151 | g⁻ = 18 | toute droite-bloc générique a le signe local −1 ; (det Q_c \| 7) = −1 pour tout bloc générique | C2 | P | `conway99-structures-lab:master:JOURNAL.md:701` | « toute droite-bloc générique doit avoir le signe −1 » |
| L09-COND-152 | bloc générique avec det Q_c carré (ex. τ_c = η_c) ; bloc A (τ = ι partout) ; bloc plein | g⁻ = 20 (donc à g⁻ = 18 : ni bloc plein ni résidu AD) | C2 | P | `conway99-structures-lab:master:JOURNAL.md:752` | « La droite-bloc est alors toujours de rang 18 et de signe local +1, **donc g⁻ = 20**. » |
| L09-COND-153 | involution (cadre de C2) | Λ_{T,−4} (rang 15) 7-isotrope ⟺ l'involution meurt | C2 | P | `conway99-structures-lab:master:JOURNAL.md:717` | « l'involution meurt ssi Λ_{T,−4} (rang 15) est 7-isotrope » |
| L09-COND-154 | lemme de Witt général (bloc local) | g ≥ 18 + t − 2r₀ + 2·[boule réduite non scindée] ; d'où g⁻ ≠ 16 et g⁻ ∈ {18, 20} | C2 | P | `conway99-structures-lab:master:JOURNAL.md:823-826` | « g ≥ 18 + t − 2r₀ + 2·[boule réduite non scindée] » |
| L09-COND-155 | dossier 6 d'Astra (involution) | min Λ₋₄⁻ ≥ 8, det L_T = 2¹²7^{g⁻−7}, Blichfeldt ⟹ g⁻ ≥ 12 | C2 | P | `conway99-structures-lab:master:JOURNAL.md:749` | « Blichfeldt ⟹ g⁻ ≥ 12 » |
| L09-COND-156 | vecteur de norme ≤ 10 dans L_T (Sol) | coefficients ±1, côté positif stable, B 4-régulier ; norme 8 ⟹ cube ou Wagner ; cube ⟹ prisme (exclu à P = 0) | C2 (sous P = 0 pour le cube) | P | `conway99-structures-lab:master:JOURNAL.md:757-758` | « norme 8 ⟹ cube ou Wagner » |
| L09-COND-157 | une involution existe | repère de 51 vecteurs dans l'un des 156 réseaux de Borcherds ; tous les exclure = fin du cas involution | C2 | P | `conway99-structures-lab:master:JOURNAL.md:965-967` | « Tous les exclure = fin du cas involution. » |
| L09-COND-158 | (A) types à pivots (système local + β) UNSAT et (B) famille tout-dis exclue | pas d'involution (ligne d'arrivée) | C2 | O | `conway99-structures-lab:master:JOURNAL.md:945-946` | « Fin = (A) les 1521 types à pivots » — Comptage 1 521 (structures) vs 1 507 (notes/137:69). |
| L09-COND-159 | chaque orbite frère, « un bloc » ou dis | Σ_c(2#piv_c + d_c) = 84 + 4\|Σ\| ; un bloc a 2#piv + d ≥ 12 | C2 | P | `conway99-structures-lab:master:JOURNAL.md:942-943` | « Σ_c(2#piv_c + d_c) = 84 + 4\|Σ\| » |
| L09-COND-160 | identité du repère seule (poids fractionnaires) sur une classe O₂₄ | infaisable pour 86/141 classes (certificat entier) | C2 (route C, id 0) | C | `conway99-structures-lab:master:JOURNAL.md:975-977` | « L'optimum de phase 1 vaut 7 : l'identité force (Σx, Σz) = (38, 10) au lieu de (42, 7). » |
| L09-COND-161 | toutes les structures « Ψ » réglables (retournements) | le lemme Fano par Ψ seul est caduc (480 réglages satisfont I_R = 0) | C1 (Fano tendu) | E | `conway99-structures-lab:master:JOURNAL.md:262` | « 480 réglages avec le σ du témoin satisfont les 21 conditions I_R = 0 » |
| L09-COND-162 | P = 0 et S = 0 | H(x) = 12 936 en tout sommet (automatique) | C1 | P | `conway99-structures-lab:master:JOURNAL.md:426` | « Seul point nouveau : à P = 0 et S = 0, H(x) = 12 936 en tout sommet. » |
| L09-COND-163 | argument 7-adique n'utilisant que « 7 \| t, 7 ∤ v » et les identités de la famille srg(2m²+1,2m,1,2) | exclut d'un coup 99, 6 273 et 494 019 | famille (99 inclus) | O | `conway99-structures-lab:master:NOTE_S25_FAMILLE_9_243.md:15-16` | « un argument 7-adique qui n'utilise que « 7 \| t, 7 ∤ v » et les identités de la famille exclurait » |
| L09-COND-164 | srg(v, k, 1, 2) avec k ≥ 8 | aucun ensemble de commutation de Godsil–McKay non trivial (pas de nouveau membre par commutation locale) | famille (243, 99, 6 273, 494 019) | P | `conway99-structures-lab:master:NOTE_S25_FAMILLE_9_243.md:57-58` | « Γ n'a aucun ensemble de commutation de Godsil–McKay non trivial. » |
| L09-COND-165 | involution : minorant g⁻ ≥ 21 (structure lointaine), ou contradiction propre à g⁻ = 18 et g⁻ = 20 | l'involution meurt | C2 | O | `conway99-structures-lab:master:NOTE_S27_INVOLUTION_GENRE_7ADIQUE.md:66-70` | « Un minorant **g⁻ ≥ 21**. » |
| L09-COND-166 | involution avec g⁻ = 22 | ε⁻ forcé à +1 contre ε⁻ = −1 par la formule : impossible | C2 | P | `conway99-structures-lab:master:NOTE_S27_INVOLUTION_GENRE_7ADIQUE.md:25-26` | « **g⁻ = 22 est impossible.** » |
| L09-COND-167 | g⁻ = 18 et une droite-bloc E de rang 18 | ε⁻ = χ(disc B\|_E) ; donc toute droite-bloc générique a le signe local −1 ; la configuration non tordue (signe +1) est interdite | C2 | P | `conway99-structures-lab:master:NOTE_S27_INVOLUTION_GENRE_7ADIQUE.md:73-82` | « toute droite-bloc générique doit avoir le signe local −1 » |
| L09-COND-168 | g⁻ = 16 | torsion équilibrée dans les 7 blocs (g⁻ = 18 + t_c − 2r₀_c + ρ_c) | C2 | P | `conway99-structures-lab:master:NOTE_S27_INVOLUTION_GENRE_7ADIQUE.md:106` | « g⁻ = 16 exige de la torsion équilibrée dans les 7 blocs » |
| L09-COND-169 | orbite X ⊂ ij pivotant en i (AD), S composante de i dans G_k, Π les blocs portant le digone {i,k} | \|S\| ≥ 3 + [j ∈ S] + \|Π\| (lemme T⁺) ; violation ⟹ configuration morte | C2 (AD) | P | `conway99-structures-lab:master:NOTE_S28_AD_NIVEAU_PAIRES.md:36-42` | « \|S\| ≥ 3 + [j ∈ S] + \|Π\|. » |
| L09-COND-170 | orbite lointaine f ancrée en e₁ au bloc plein | f rigide ⟺ son ombre a exactement une étiquette dans chacun des 4 blocs hors de {c, e₁, e₂} | C2 (bloc plein) | P | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:41-42` | « son ombre a exactement une étiquette dans chacun des 4 blocs hors de {c, e₁, e₂} » |
| L09-COND-171 | bloc plein (τ_c = η_c) | rang X_F = 17 et spec T_FF = 3⁹(−4)⁴(−1)⁵(−2)⁶1⁶ ; Φ(z) ∩ Φ(σz) = ∅ ; D préserve l'étoile | C2 | P | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:59` | « D'où **rang X_F = 17** et **spec T = 3⁹ (−4)⁴ (−1)⁵ (−2)⁶ 1⁶**. » |
| L09-COND-172 | digone ancré {p, q} (tout type) | k_Z = 2 − \|blocs(z) ∩ {p,q}\| pour toute σ-paire Z | C2 | P | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:180-181` | « chaque σ-paire Z vérifie k_Z = 2 − \|blocs(z) ∩ {p, q}\| » |
| L09-COND-173 | apex intérieur A d'un carré dis (U, W) | A est dis, Q_UV = Q_WV = 0, supp B ∩ T = ∅, supp V parmi 5 supports ; au moins ⌈n_dis/3⌉ carrés dis sans apex intérieur | C2 (dis) | P | `conway99-structures-lab:master:NOTE_S23_ENONCE_DOSSIER4.md:147` | « supp V ∈ {{p,q}, {p,r}, {q,r}, {j,r}, {l,r}}, avec Q_BV = 0 pour les deux derniers. » |
| L09-COND-174 | SRG contenant la boule explicite du dossier 5 (τ ≡ 6) | k ≥ 24 | C1 (une boule) | P | `conway99-structures-lab:master:NOTE_S24_ASTRA_DOSSIER5.md:25` | « Toute SRG contenant cette boule vérifie k ≥ 24. » |
| L09-COND-175 | (A − 3I)z ≡ 0 mod 7 avec un support ≤ 6 (échange de ≤ 6 ombres) | Az = 3z et le support induit un prisme (deux prismes) | C1 (7-adique) | P | `conway99-structures-lab:master:NOTE_S24_ASTRA_DOSSIER5.md:55-62` | « Donc Az = 3z. » |
| L09-COND-176 | boule formée de trois composantes 4+4+4 | d(L) = 3 et k ≥ 20 (L21) ; exclues à P = S = 0 | C1 | E | `conway99-structures-lab:master:NOTE_S26_ASTRA_ETOILES.md:45` | « d(L) = 3 pour une boule formée de trois telles composantes, et k ≥ 20 par L21. » |
| L09-COND-177 | droite au Fano tendu (codage w_Z) | réglage de retournements possible ⟺ système affine en (π_XY, π_XZ, π_YZ) cohérent | C1 (Fano tendu) | P | `conway99-structures-lab:master:NOTE_S21_PSI_STRUCTUREL.md:139-140` | « La droite admet un réglage de retournements si et seulement si le système affine en 3 inconnues » |
| L09-COND-178 | la piste locale (i)+(ii)+(iii) tue toutes les configurations contenant un bloc non libre | C2 se réduit au cas « tous les blocs sont des étoiles libres » | C2 | H | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:159-160` | « réduirait C2 au cas « tous les blocs sont des étoiles libres » » |
| L09-COND-179 | v ∈ N* (réseau N de l'involution, repère serré Σ(v,u_a)² = 7‖v‖²) | ‖v‖² ≥ 8/7 ; tout sur-réseau entier de N a un minimum ≥ 2 | C2 | P | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER6.md:245-252` | « Pour \(v\in N^*\), tous ces produits sont entiers. » |
| L09-COND-180 | involution (cadre du dossier 6, sans P = 0) | g⁻ ≥ 12 (g⁻ = 8 et 10 exclus par Blichfeldt) | C2 | P | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER6.md:10-11` | « Les cas **g⁻ = 8 et g⁻ = 10 sont exclus** » |
| L09-COND-181 | involution à g⁻ < 20 | les générateurs engendrent N, de strict indice dans N_max (à g⁻ = 18 : sous-réseau d'indice 7) ; il faut exclure la présence du repère dans les réseaux de det 49, pas seulement les réseaux engendrés | C2 | P | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER6.md:292-294` | « Il ne suffirait pas d'exclure les réseaux de déterminant 49 **engendrés** par le repère » |
| L09-COND-182 | rang₇ Gram(L_T) ≤ 1 (au lieu de 22 − g⁻ ∈ {2, 4}) | contradiction avec le genre (involution exclue) | C2 | O | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER6.md:433-435` | « Prouver le rang ≤ 1 suffirait à contredire le genre » |
| L09-COND-183 | vecteur non nul de L_T de norme ≤ 10 (cadre à sept blocs) | coefficients ±1, support biparti 4-régulier ; à norme 8 : cube (⟹ prisme) ou Wagner | C2 (P = 0 pour exclure le cube) | P | `conway99-structures-lab:master:astra/RAPPORT_SOL_SUPPORTS_COURTS.md:9-11` | « Un vecteur non nul de (L_T\) de norme carrée au plus 10 a des coefficients non nuls égaux à ±1. » |
| L09-COND-184 | P = 0 et support Wagner de norme 8 | le support utilise les sept blocs (les 25 classes à six blocs exclues) | C2 | C | `conway99-structures-lab:master:astra/RAPPORT_SOL_WAGNER.md:5` | « à P=0, tout support Wagner de norme carrée 8 utilise les sept blocs » |
| L09-COND-185 | Blichfeldt sur L_T à g⁻ = 12 | un vecteur de norme ≤ 10 existe (cas résiduels : Wagner norme 8, normes 9 et 10) | C2 | P | `conway99-structures-lab:master:astra/RAPPORT_SOL_SUPPORTS_COURTS.md:198-204` | « La borne de Blichfeldt sur (L_T\) à (g^-=12\) impose un vecteur de norme carrée au plus 10. » |
| L09-COND-186 | à g⁻ = 16 | t_c ≥ 2 et r₀_c ≥ 1 + (t_c + ρ_c)/2 dans CHACUN des 7 blocs | C2 | P | `conway99-structures-lab:master:astra/PROBLEMES_OUVERTS_INVOLUTION.md:42-43` | « Dans CHACUN des 7 blocs : t_c ≥ 2 et r₀_c ≥ 1 + (t_c + ρ_c)/2. » |
| L09-COND-187 | g = 18 et bloc de type t = 0 non scindé | impossible (1 448 classes) | C2 | P | `conway99-structures-lab:master:astra/POUR_SOL_G18_G20_NOS_NOMBRES.md:63` | « **Les types t = 0 non scindés sont impossibles à g = 18** » |
| L09-COND-188 | g = 18 et bloc t = 0 scindé | R_c = 0 : Z_ff ≡ 0 pour les 30 orbites lointaines, puis T_ff′ ≡ Z_ff′ (lignes rigides) | C2 | P | `conway99-structures-lab:master:astra/POUR_SOL_G18_G20_NOS_NOMBRES.md:64-65` | « exigent R_c = 0 » |
| L09-COND-189 | système local UNSAT sur les 79 classes pertinentes à ≥ 6 pivots | la famille « Σ = ∅, tout un bloc » est morte | C2 | O | `conway99-structures-lab:master:astra/POUR_SOL_G18_G20_NOS_NOMBRES.md:109` | « système local UNSAT sur les 79 classes pertinentes à ≥ 6 pivots » |
| L09-COND-190 | système local UNSAT sur les 1 521 classes à pivots | seul « tout dis » survit (toutes les étoiles libres) | C2 | O | `conway99-structures-lab:master:astra/POUR_SOL_G18_G20_NOS_NOMBRES.md:110` | « UNSAT sur les 1521 classes à pivots ⟹ seul « tout dis » survit » |
| L09-COND-191 | problème B (bloc plein) a une solution | spec T = 3⁹(−4)⁴(−1)⁵(−2)⁶1⁶ et rang X = 17 | C2 | P | `conway99-structures-lab:master:astra/PROBLEME_BLOC_PLEIN_POUR_SOL.md:49-50` | « Si B a une solution, T a le spectre exact » |
| L09-COND-192 | problème A ou B (bloc plein) impossible pour un type (certificat) | tout bloc plein de ce type est exclu dans une involution (et avec lui les résidus AD et tout Σ = ∅ à bloc de degré 6) | C2 | O | `conway99-structures-lab:master:involution/HANDOFF_FULLBLOCK.md:9-10` | « **Infaisable ⟹ aucune involution n'a de bloc plein de ce type.** » |
| L09-COND-193 | carré dis contenant une orbite de l'étoile de c | SEC est faux en c (valide en tout bloc si n_dis = 0) | C2 | P | `conway99-structures-lab:master:involution/LEMMA_SCOPES.md:16` | « faux en c dès qu'un carré dis contient une orbite de l'étoile de c » |
| L09-COND-194 | involution σ avec D(U) = U′ pour toute orbite (tout frère) | impossible (Théorème D) | C2 | P | `conway99-structures-lab:master:logs/c2_programme.md:105` | « **Théorème D.** Il n'existe pas de srg(99,14,1,2) avec involution σ telle que D(U) = U′ (orbite sœur) pour toute orbite U. » |
| L09-COND-195 | graphe N des paires non frères à au plus 6 arêtes | exclu (∅, 1 à 5 arêtes, 2C₃, K₂,₃, C₆) | C2 | P | `conway99-structures-lab:master:logs/c2_programme.md:282` | « **Bilan : tout N à au plus 6 arêtes est exclu** » |
| L09-COND-196 | modèle de Fano (21 paires tordues, D = 7 triangles d'un plan de Fano) | impossible (Théorème F) | C2 | P | `conway99-structures-lab:master:logs/c2_programme.md:380-381` | « **Théorème F.** Le modèle de Fano » |
| L09-COND-197 | configuration ancrée | impossible (Théorème 24.3 ; Théorème P pour les tournois réguliers) | C2 | P | `conway99-structures-lab:master:logs/c2_programme.md:773` | « **Théorème 24.3.** Aucune configuration ancrée n'existe. » |
| L09-COND-198 | sommet plat dans une srg(99,14,1,2) | impossible (Théorème D′, cas particulier de L8) | C1 (sans automorphisme) | P | `conway99-structures-lab:master:logs/c2_programme.md:550` | « **Théorème D′ (PROUVÉ, aucun automorphisme supposé).** Dans une srg(99,14,1,2), aucun sommet n'est plat. » |
| L09-COND-199 | à k = 28 : un accident 7-adique toujours isotrope (z·z ≡ 0) ; ou les accidents contiennent un sous-espace totalement isotrope de dimension (30 − k)/2 | k = 28 exclu ; tout k exclu | C1 | O | `conway99-structures-lab:master:logs/c2_programme.md:579-581` | « Montrer qu'un accident est toujours isotrope (z·z ≡ 0) exclurait k = 28 » |
| L09-COND-200 | s automorphisme d'ordre 7 d'un srg(99,14,1,2) | contradiction (pas d'automorphisme d'ordre 7) | Aut (ordre 7) | P | `conway99-structures-lab:origin/claude/chat-session-09hf0k:ordre7/tex/order7.tex:75-78` | « has no automorphism of » — Non arbitré (« not yet been refereed »). |
| L09-COND-201 | un repère structuré complet (route C) existe dans U unimodulaire de rang 24 | U′ = ℤ⁷ ⊥ V avec V l'un des 9 unimodulaires de rang 17, y₁, y₂ ∈ V, K = V ∩ y⊥ rang 15 det 49 | C2 | P | `conway99-rank17:master:RANK17_HANDOFF.md:55-65` | « Then U' is integral and unimodular, and U' = A ⊥ V ≅ Z^7 ⊥ V » |
| L09-COND-202 | V = ℤ¹⁷ et min U ≥ 2 | au plus 8 types de y-paires (4 si min U ≥ 3) | C2 | P | `conway99-rank17:master:RANK17_HANDOFF.md:196-221` | « Therefore only eight y-pair representatives are needed for the switched V=Z17 portion » |
| L09-COND-203 | un vecteur rationnel w ∈ Y⊥ non nul a des produits entiers avec tous les u candidats et \|w\|² < 8/7 | le nœud ne s'étend pas en repère d'origine graphe | C2 | P | `conway99-rank17:master:RANK17_HANDOFF.md:272` | « If a nonzero rational vector w∈Y^perp has integral pairings with every allowed u and norm<8/7, the node cannot extend to a graph-origin frame. » |
| L09-COND-204 | S a = −4a avec a entier non nul et ‖a‖² ≤ 7 | contradiction (min N* ≥ 8/7) | C2 | P | `conway99-rank17:master:RANK17_HANDOFF.md:342-362` | « Suppose Sa=-4a with nonzero integer a and \|\|a\|\|^2≤7. » |
| L09-COND-205 | une classe (V,y) a κ ∈ K* avec n = 7\|κ\|² ≤ 4 | la classe est exclue (R≤4 de Sol) | C2 | P | `conway99-rank17:master:PROOF_OBLIGATION.md:140-141` | « F10 \| Rungs R_n for n ≤ 4: no such a exists \| PROVEN-ext » — Texte de preuve non archivé. |
| L09-COND-206 | R6 et R8 sont démontrés (pas de vecteur propre entier σ-impair de −4 nul sur x ∪ N(x) de type n = 6 ni n = 8) | Théorème C2 (pas d'involution), avec F1–F12 ; sans moteur il faut aussi R5 pour A11E6⁺ #31 et D16⁺ #7 | C2 | O | `conway99-rank17:master:PROOF_OBLIGATION.md:312-316` | « Together with R6 it closes all 754, and with F1–F12 that proves Theorem C2. » |
| L09-COND-207 | les axiomes V-libres de N (cible A) sont incohérents | C2 suit directement | C2 | O | `conway99-rank17:master:PROOF_OBLIGATION.md:199` | « if the axioms are inconsistent, C2 follows directly. » |
| L09-COND-208 | χ caractéristique de V, y de norme 7, r de norme 2 ⊥ y et χ = y + r | y ne peut être une normale du repère switché (toute l'orbite Aut(V) de y est fermée) | C2 | P | `conway99-rank17:master:r17_char/ASTRA_PROOF_29_09.md:49-63` | « Suppose y in V has norm 7, r in V has norm 2, (r,y)=0, and chi=y+r is characteristic. Then y cannot be either normal in a switched C2 frame. » |
| L09-COND-209 | (χ,y₁)² + (χ,y₂)² > 7\|χ\|² − 21 pour un χ caractéristique de V | la classe (V,y₁,y₂) est exclue (test exact avec \|χ\|² ∈ {1,9}) | C2 | C | `conway99-rank17:master:r17_char/README.md:7-16` | « (χ,y1)² + (χ,y2)² ≤ 7\|χ\|² − 21. » |
| L09-COND-210 | ancre caractéristique Φ (Type 0/II) | ‖Φ‖² ≡ 5 (mod 8) ; une seule classe de deux-graphe (tout-Opp) ; normes 25 et 33 impossibles | C2 | P | `conway99-rank17:master:sol_type02/PROOF.md:112-126` | « Thus 25 and 33 are impossible. » |
| L09-COND-211 | deux entrées de magnitude 3 à norme 37 | leurs racines Opp orientées forment un chemin dirigé (cas disjoint et fourche exclus) | C2 | P | `conway99-rank17:master:sol_type02/PROOF.md:252-287` | « Thus r_i.r_j=-1: the two oriented Opp roots must be successive edges of a directed path on three vertices. » |
| L09-COND-212 | pas de Type 0 et pas de Type II (théorèmes V-libres) + R5 | il ne resterait que 19 classes (+1 ℤ¹⁷) | C2 | O | `conway99-rank17:master:GPT_PROMPT_TYPE0_TYPE2.md:19` | « So "no Type 0" + "no Type II" as V-free theorems would leave only 19 classes (+1 Z17). » |
| L09-COND-213 | m* > 21 (resp. m* > 29) pour les Φ caractéristiques | tue 76 classes (resp. 454, tout sauf 69 + ℤ¹⁷) | C2 | O | `conway99-rank17:master:GPT_PROMPT_TYPE0_TYPE2.md:87-89` | « m* > 21 kills 76. » |
| L09-COND-214 | une borne uniforme m* ≥ 37 pour les Φ caractéristiques avec (TP) | ferme 454 classes d'un coup | C2 | O | `conway99-rank17:master:GPT_FOLLOWUP_TYPE0_NEXT.md:69` | « If some combination of (Q+), pi and (CNT) gives a uniform lower bound m* ≥ 37 on characteristic Phi with (TP), that closes 454 classes at once. » |
| L09-COND-215 | R8 k=2 et k=3 prouvés (puis J2 clos) | A11E6p:8 : 1,2·10¹⁰ → 2,1·10⁶ feuilles (puis 0 squelette) ; les 342 classes non-n5 deviennent des runs de minutes | C2 | H | `conway99-rank17:master:wfe/README.md:57-63` | « if R8 k=2 and k=3 were proven, every n=8 witness would be restricted to k=1 and the leaves drop 1.2e10 → **2.1e6** » |
| L09-COND-216 | k = 28 (secteur pair) | det L_β = 2⁸ ; L_β d'indice 16 dans un des 5 unimodulaires de rang 15 | C2 | P | `conway99-rank17:master:evenframe/README.md:12-15` | « So k = 28 ⟺ det L_β = 2⁸. » — Dérivation à relire. |
| L09-COND-217 | parallélisme des 231 triangles en 7 classes de 33 respecté par σ (orientations renversées) | ⟨σ, T_i⟩ est un quotient du groupe de Coxeter de l'étoile K₁,₇ et Γ une représentation de permutation de degré 99 où σ a un point fixe | C2 | O | `conway99-rank17:master:paradigm/PARADIGM_BREAK.md:104-115` | « if σ preserves the classes and reverses the orientations, then ⟨σ, T_i⟩ is a quotient of the Coxeter group of the star K₁,₇ » — Hypothèse non forcée. |
| L09-COND-218 | w réel avec w² ≤ 1 et (w,u_o) ∈ Z pour les 42 u sélectionnés (Γ42 = N) | la projection de w sur N est nulle ; au plus 2 telles directions indépendantes (N⊥ de dim 2) | C2 (route C) | P | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:63-65` | « Si un vecteur réel w vérifie w²≤1 et (w,u_o)∈Z pour les42 u sélectionnés » |
| L09-COND-219 | l'enveloppe unimodulaire de rang 24 contient D8³ (resp. D11, D12) | aucun repère physique (enveloppe exclue) | C2 (route C) | P | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:10-11` | « TOUTE enveloppe contenant trois D8 orthogonaux de rang total24 est exclue pour le repère » |
| L09-COND-220 | enveloppe D6⁴ avec six blocs fractionnaires dans une même paire de composantes opposées | impossible (racine de projection duale 6/7 < 8/7) | C2 (route C) | P | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:12` | « Dans la famille D6⁴, SIX blocs fractionnaires dans une même paire de composantes opposées sont impossibles. » |
| L09-COND-221 | enveloppe sans racines de norme 2 | 24 ombres orthogonales forcées et code binaire autodual doublement pair [24,12,8] | C2 (route C) | P | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:14` | « Si l’enveloppe est sans racines de norme2, les24 ombres orthogonales sont FORCÉES. » |
| L09-COND-222 | reconstruction BvLS avec la région lointaine d'un triangle + deux prismes libres | seules complétions : BvLS et son jumeau (pas de complétion asymétrique) | srg(243) (contrôle) | E | `conway99-c1:origin/main:dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/RESULTATS.md:9` | « il y a exactement deux classes d'isomorphisme : BvLS et son jumeau » |
| L09-COND-223 | srg(99,14,1,2) avec une coclique de 22 dont le design de voisinages est cyclique sur 22 points ou porte une action régulière d'ordre 21 avec point fixe | impossible | C1 (α = 22) | E | `conway99-c1:origin/main:dossiers_externes/HOFFMAN_UPDATE_20261011/README.md:15` | « Aucun SRG(99,14,1,2) avec une coclique de taille 22 ne peut avoir pour design de voisinages » |
| L09-COND-224 | mot binaire de ker₇(A + 4I) de poids 77 | coclique de Hoffman 22 (équivalence) ; poids possibles 0, 63, 77 | C1 | P | `conway99-c1:origin/main:dossiers_externes/INDEX.md:19` | « Le poids 77 équivaut à une coclique de Hoffman 22. » |
| L09-COND-225 | tout Conway éventuel (branche minimum global c(L) ≥ 4 fermée par CP-SAT) | il existe une droite L avec c(L) ≤ 3 | C1 | S | `conway99-c1:origin/main:AGENTS.md:611` | « Consequence : tout Conway eventuel a une droite L avec c(L)<=3. » |
| L09-COND-226 | P ≤ 852 | au moins 18 droites t ≤ 7 et au moins 254 blocs non-grille contenant une telle droite | C1 | P | `conway99-c1:origin/main:AGENTS.md:1306-1307` | « P<=852 => au moins18 droites t<=7 et au moins254 » |
| L09-COND-227 | NG7 : aucun bloc non-grille avec min(t_l, t_m) ≤ 7 ne passe les conditions nécessaires de Conway | pas de Conway (avec P ≤ 852) | C1 | O | `conway99-c1:origin/main:AGENTS.md:1311-1312` | « Cible SUFFISANTE plus etroite (NG7), OUVERTE » |
| L09-COND-228 | T, U PSD sur les 84 étiquettes avec T + U = 7Π et rang T ≤ 30 | T² = 7T, rang T = 30, rang U = 40, puis l'identité SRG99 | C1 | P | `conway99-c1:origin/main:AGENTS.md:1106-1107` | « Theoreme global : T+U=7Pi sur84, rangPi70, traceT210 » |
| L09-COND-229 | famille locale ⟨z,hM⟩ sous C1/C1′/C2 et T/U PSD | null_Q T ≤ 14 ; si nullité 14, rang_F7(8T) ≥ 29 ; avec rang_Q ≤ 30 et rang_F7 ≤ 28 : aucune complétion Conway | C1 (famille locale) | S | `conway99-c1:origin/main:AGENTS.md:1521-1524` | « null_Q T<=14 ; si nullite14, rang_F7(8T)>=29. » |
| L09-COND-230 | graphe des grilles C4 ⊔ C3 (sous E3) | K4 ⊔ C3 | C1 (gabarits c3) | P | `conway99-c1:origin/main:AGENTS.md:368-369` | « Generalisation PROUVEE sousE3 : graphe des grilles C4 disjoint C3 implique » |
| L09-COND-231 | H01 = −H02 ≠ 0 et grilles Q12, Q45, Q46, Q56 (K3U) | famille exclue | C1 | C | `conway99-c1:origin/main:AGENTS.md:151-152` | « Portee : H01=-H02 non nul; grilles Q12,Q45,Q46,Q56; autres rectangles » |
| L09-COND-232 | bord43 avec 3I − B + J/9 > 0 (q = 1) | au plus 8 192 affectations de signes puis au plus deux complétions Conway étiquetées, isomorphes ; plus de deux choix ⟹ vecteur propre −4 de norme 14 ⟹ co-Heawood disjoint et deux cocliques 22 | C1 | P | `conway99-c1:origin/main:AGENTS.md:1945-1961` | « Tout bord43 avec3I-B+J/9>0 » |
| L09-COND-233 | rang F ≥ 12 pour une droite l de c minimum | N9-NG (équivalence) | C1 | P | `conway99-c1:origin/main:AGENTS.md:801` | « Pour l de c MINIMUM, N9-NG equivaut a rank(F)>=12. » |
| L09-COND-234 | Γ binaire et q (S20 extérieur) avec Kq = 0 | Tq = 0 impossible ; coupe stricte qᵀTq = 8(49 − e(O ∪ S)) | C1 | P | `conway99-c1:origin/main:AGENTS.md:1414-1416` | « Donc, pour Gamma binaire, Tq=0 serait impossible » |
| L09-COND-235 | H01 = −H02 ≠ 0, Q12, Q34, Q56 grilles (famille 2K2), E3 | aucune complétion (famille exclue) | C1 | C | `conway99-c1:origin/main:notes/FERMETURE_2K2_2026_10_19.txt:12-15` | « Ce resultat exclut cette famille; il n'exclut pas encore tout Conway. » |
| L09-COND-236 | H01 = −H02 ≠ 0 et Q12 grille | le graphe des grilles sur les quatre autres racines est une étoile (éventuellement vide ou une arête) | C1 | P | `conway99-c1:origin/main:notes/FERMETURE_2K2_2026_10_19.txt:107-114` | « Ce graphe de grilles est donc une etoile » |
| L09-COND-237 | P3 : étoile de grilles à au moins deux arêtes (campagne LAB) exclue | avec 2K2 et K3U : plus de deux grilles adjacentes impossibles dans ce cadre | C1 | O | `conway99-c1:origin/main:notes/FERMETURE_2K2_2026_10_19.txt:114-115` | « La campagne P3 du LAB porte sur une etoile ayant au moins » |
| L09-COND-238 | t_x(F) − t_x(G) = d > 0 et \|W\| < d | x a un voisin hors W portant F sans G (clause nécessaire) | tout srg(v,2r,1,2) | P | `conway99-c1:origin/main:notes/PREUVE_COUPES_CONTINUATION_2026_10_19.txt:94-98` | « \|A\B\| = \|A\|-\|A intersection B\| >= t_x(F)-t_x(G) = d. » |
| L09-COND-239 | Q_ij grille dans Conway (r = 7) | chacun des 40 sommets disjoints de {i,j} a exactement un voisin dans la grille ; les autres sommets touchant i ou j n'en ont aucun | C1 | P | `conway99-c1:origin/main:notes/GRILLES_BC_PROFILS_2K2N_2026_10_19.txt:48-49` | « CHACUN a donc exactement un voisin dans la grille. » |
| L09-COND-240 | dans tous les profils admissibles e ⟹ f (quotas t_e, t_f) | t_e ≤ t_f ; si t_e = t_f, tout profil contenant f sans e est éliminé | général (comptage exact) | P | `conway99-c1:origin/main:notes/FACTEURS_QUATRE_COULEURS_2026_10_19.txt:159-164` | « Si t_e=t_f, tout profil contenant f sans e peut etre elimine » |
| L09-COND-241 | famille 2K2N et fermeture 2K2 | E(Q12) ≤ 3 donc E(C) ∈ {28, 32, 36, 40} sur le noyau de 20 sommets | C1 | P | `conway99-c1:origin/main:notes/NOYAU_SIGNE_2K2N_2026_10_19.txt:82-84` | « Si Q12 avait4aretes dans2K2N, on aurait les trois grilles Q12,Q34,Q56 » |
| L09-COND-242 | DISC admet la classe de carré 14 sans utiliser L4 (k pair) | la branche 14 est exclue (tout mineur principal non singulier 30 × 30 de 8T a la classe 2) | C1 (DISC) | H | `C:/home/researcher/cw/review/05_c1_notes_00_99.md:271-274` | « If DISC currently admits class 14, check whether L4 (k even) is used; if not, the 14 branch is excluded. » — Inférence du relecteur, non vérifiée contre le code DISC. |
| L09-COND-243 | bloc d'étiquettes I entièrement déterminé | rang₇((8T)_II) ≤ k ≤ 28 ; égalité ⟹ partie non dégénérée hyperbolique ; rejeter rang₇ ≥ 29 ou (rang 28 et non hyperbolique) | C1 | P | `C:/home/researcher/cw/review/05_c1_notes_00_99.md:264-269` | « For any label set I with all entries known » |
| L09-COND-244 | toutes les boules (droite générique) meurent au test d'étoile | rang 37 exclu (forme sans droite, NOTE 17.93) | C1 (rang 37) | P | `C:/home/researcher/cw/review/07_workspace_c1_0713.md:139` | « all-balls-die implies rank 37 excluded » |
| L09-COND-245 | srg(99,14,1,2) avec spread régulier | le quotient serait srg(33,12,1,6) (multiplicité 44/7) : impossible | C1 | P | `C:/home/researcher/cw/review/07_workspace_c1_0713.md:181` | « Conway's graph has NO regular spread » |
| L09-COND-246 | tout UNSAT de la question des profils de cocliques (taille 22, 21 maximales) | seulement « plus grande coclique ≤ 20 », pas de contradiction : ne ferme pas C1 | C1 | P | `C:/home/researcher/cw/review/07_workspace_c1_0713.md:186` | « coclique frame logic (13/10) » |
| L09-COND-247 | structure admissible à cinq étoiles inexistante | pas de Conway (frontière du 16/10) | C1 | O | `C:/home/researcher/cw/review/BRIEF.md:14-16` | « If not, no Conway graph. » |
| L09-COND-248 | tout bloc PSD à quatre étoiles de nullité ≥ 14 a des couplages h-reliés (H-MATCH) | pas de Conway | C1 | O | `C:/home/researcher/cw/review/BRIEF.md:12` | « (H-MATCH) reduction: if every PSD four-star block of nullity >= 14 has h-related star matchings, no Conway graph. » |
| L09-COND-249 | le « 14 » de DISC provient de la parité de v₇(det) d'un réseau propre | tout bloc à quatre étoiles de classe 14 est exclu « gratuitement » (a pair) | C1 (DISC) | H | `C:/home/researcher/cw/review/02_symmetry_c3_c7.md:309-313` | « If so, any four-star block with class 14 is excluded for free. » — Confiance du relecteur < 30 % ; deux relectures indépendantes (02 et 05) convergent vers la même suggestion. |

### 10.2 Bornes quantitatives (210)

| id | objet | relation | valeur | conditions | statut | source |
|---|---|---|---|---|---|---|
| L09-BORNE-001 | nombre de droites / quadrangles de Γ | = | 231 droites, 2079 quadrangles | srg(99,14,1,2) | P | `conway99-c1:main:notes/00_FONDATIONS.md:14-18` |
| L09-BORNE-002 | spectre de H = Γ[Γ₂(x)] | = | 12¹, (−2)⁶, 0⁷, 3⁴⁰, (−4)³⁰ | tout sommet x | P | `conway99-c1:main:notes/00_FONDATIONS.md:47` |
| L09-BORNE-003 | rank₂(A), rank₂(A+I) | = | 54 et 45 |  | P | `conway99-c1:main:notes/00_FONDATIONS.md:71-72` |
| L09-BORNE-004 | rank₇(A − 3I) | ∈ | impair, 15 ≤ · ≤ 45 (L2) ; puis {25, 27, …, 43} (L20 ter + L22) |  | P | `conway99-c1:main:notes/30_LEMMES.md:43-44` |
| L09-BORNE-005 | k = rank₇(A − 3I) − 15 | ∈ | pair, 0 ≤ k ≤ 30 (L4) ; k ≥ 2 (L19 bis) ; k ≥ 6 (L20) ; k ≥ 8 (L20 bis) ; k ≥ 10 (L20 ter, S) ; k ≤ 28 (L22) |  | P | `conway99-c1:main:notes/30_LEMMES.md:61` |
| L09-BORNE-006 | P (nombre de prismes) | = | 1386 − (1/6)Σ_x\|W(x)\| (L15) |  | P | `conway99-c1:main:notes/30_LEMMES.md:204` |
| L09-BORNE-007 | P | ≤ | 1155 puis 1151 (L16) |  | P | `conway99-c1:main:notes/30_LEMMES.md:218-220` |
| L09-BORNE-008 | Σ_x\|W(x)\| ; n₃ ; paires de droites reliées par 2 arêtes | ≥ | 1410 ; 705 ; 705 | par L16 | P | `conway99-c1:main:notes/30_LEMMES.md:219-220` |
| L09-BORNE-009 | n₃ (variable libre de Reimbayev) | ∈ | [0, 4158] par non-négativité d'ordre 7 ; [705, 4158] avec L16 | (99,14) | E | `conway99-c1:main:rapport/RAPPORT_C1.md:75` |
| L09-BORNE-010 | S (paires σ-adjacentes) | ∈ | [0, n₃] (polygone d'ordre 7, L18) |  | P | `conway99-c1:main:notes/30_LEMMES.md:242` |
| L09-BORNE-011 | g(x) (grilles par sommet) | ≤ | 18 (L10), puis 17 (notes/108) ; g(x) ∈ [0,19] par parité ; g ≠ 20, 21 | tout x | P | `conway99-c1:main:notes/30_LEMMES.md:123` |
| L09-BORNE-012 | k en un point de Hamming | ∈ | [18, 26] (L24) | x point de Hamming (vide par L8) | P | `conway99-c1:main:notes/30_LEMMES.md:323-324` |
| L09-BORNE-013 | det du 70-espace K | = | 2²¹·3⁸·5⁶ ; K₃ det 3⁸·5⁶·7^k ; K₋₄ det 2²¹·7^k |  | P | `conway99-c1:main:notes/30_LEMMES.md:229-232` |
| L09-BORNE-014 | rang du complément de Schur de l'étoile de a | = | 11 − 2e(τ_a) (exhaustif sur 10 395 τ_a) |  | E | `conway99-c1:main:JOURNAL.md:125-126` |
| L09-BORNE-015 | d(L) (défaut 7-adique d'une droite) | ≤ | 9 observé (recuit) ⟹ conjecture k ≥ 14 | configurations aléatoires | H | `conway99-c1:main:notes/30_LEMMES.md:293-294` |
| L09-BORNE-016 | proportion de configurations aléatoires admissibles avec d(L) = 1 | = | 85 % |  | H | `conway99-c1:main:rapport/RAPPORT_C1.md:165` |
| L09-BORNE-017 | P par relâchement SDP sur les triplets de droites (degré 4 de Hadamard) | ∈ | [0, 1155] |  | E | `conway99-c1:main:JOURNAL.md:143-146` |
| L09-BORNE-018 | P pour un Γ tordu « générique » | ≈ | 126 | heuristique | H | `conway99-c1:main:rapport/RAPPORT_C1.md:173` |
| L09-BORNE-019 | hexagones induits | = | H + 3P = 213 444 (théorème de Reimbayev 2024) ; H(x) = 12 936 à P = S = 0 |  | P | `conway99-c1:main:JOURNAL.md:341-353` |
| L09-BORNE-020 | graphe signé des triangles A_Σ | = | A_Σ² = 13A_Σ + 68I ; à P = 0 valeurs propres 17 (×44), −4 (×187) |  | P | `conway99-c1:main:JOURNAL.md:343-345` |
| L09-BORNE-021 | motifs à 3 étiquettes tordues | = | 128 à symétrie près ; 24 UNSAT, 2 UNKNOWN, 102 non traités |  | S | `conway99-c1:main:data/k3_results.txt:1-26` |
| L09-BORNE-022 | motifs confinés à 3 classes | = | 728 ; 700 réfutés par propagation, 28 survivants à la propagation (tous UNSAT par SAT) ; filtre humain L9', L12, L13 : 560 survivent |  | S | `conway99-c1:main:notes/50_FRONTIERE_TORSION.md:49-53` |
| L09-BORNE-023 | tri-circulants t = 6 | = | aucune solution pour N = 44…64 (et N = 34) | ansatz tri-incidence/tri-circulant | S | `conway99-c1:main:notes/20_ATTAQUES_R.md:106` |
| L09-BORNE-024 | ordre minimal d'une géométrie locale tordue n_min(t) | = | t=2 : 20 ; t=3 : 39 ; t=5 : ≤ 93 |  | S | `conway99-c1:main:notes/10_IDEES_F.md:35` |
| L09-BORNE-025 | paramètres de Krein | > | 0 (q₁₁¹=1629/49, …, q₂₂²=649/49) |  | E | `conway99-c1:main:notes/20_ATTAQUES_R.md:93-94` |
| L09-BORNE-026 | \|Aut(Γ)\| (état du 24/09) | ∈ | {1, 2} | ordre 3 exclu par C3, ordres 7 et 11 par Behbahani–Lam | P | `conway99-c1:main:rapport/RAPPORT_C1.md:35` |
| L09-BORNE-027 | degré d'un revêtement de K₇ avec λ = 1, μ ≤ 2 et sans prisme | ≥ | 5 |  | P | `conway99-c1:main:JOURNAL.md:334` |
| L09-BORNE-028 | revêtements de degré 4 de K₇ à λ = 1 | = | 1 (28 sommets, monodromie S₄, 8 prismes) |  | E | `conway99-c1:main:JOURNAL.md:305-306` |
| L09-BORNE-029 | composantes du graphe auxiliaire H au Fano tendu | ≤ | 2 | P = 0 | P | `conway99-c1:main:JOURNAL.md:334-335` |
| L09-BORNE-030 | réseaux de la route (C) de C2 exclus ; certificats | = | 156/156 ; 7 762/7 762 | 07/10, tracker du labo | E | `conway99-c1:origin/main:JOURNAL.md:654-660` |
| L09-BORNE-031 | π(L) (prismes contenant une droite) | ∈ | {0,…,10,12} (jamais 11) | Lou–Murin 2014 | P | `conway99-c1:main:notes/60_HODGE.md:110-112` |
| L09-BORNE-032 | indépendants ; nombre chromatique χ | ≤ ; ∈ | α ≤ 22 ; 5 ≤ χ ≤ 11 | Lou–Murin 2014 | P | `conway99-c1:main:notes/60_HODGE.md:114` |
| L09-BORNE-033 | record des heuristiques de Thakkar–Severini | = | 3501/4950 = 70,73 % (549/693 λ, 2853/4158 μ) ; circulants ≤ 68,0 % |  | H | `conway99-c1:main:notes/92_CONSTRUCTION.md:39-42` |
| L09-BORNE-034 | score de recuit (8 min) pour 99 | = | 59,3 % (Hoffman–Singleton 82,9 %, Gewirtz 64,1 %, BvLS 49,2 %, M22 41,7 %, BH 35,1 %, Higman–Sims 30,7 %) |  | H | `conway99-c1:main:notes/92_CONSTRUCTION.md:44-53` |
| L09-BORNE-035 | z₁₁ (Reimbayev) ; n₃ | ∈ | 2n₃ ≤ z₁₁ ≤ 4n₃ ; n₃ ≤ 4158 ; z₁₁ ≡ 0 (mod 4) | (99,14), non-négativité d'ordre 7 | E | `conway99-c1:main:notes/60_HODGE.md:106-108` |
| L09-BORNE-036 | s(x) (paires σ-adjacentes enracinées en x) | ≤ | \|W(x)\| |  | P | `conway99-c1:main:notes/90_SECONDE_VARIABLE.md:92` |
| L09-BORNE-037 | tight fusion frame des droites par point | = | Σ_x P_{V_x} = (63/4)·I₄₄ |  | P | `conway99-c1:main:notes/70_KREIN_DROITES.md:48-49` |
| L09-BORNE-038 | frame d'Eisenstein des droites orientées | = | Σ_L (z_L z_L* + z̄_L z̄_L*) = 1134·I₄₄ |  | P | `conway99-c1:main:notes/80_ETINCELLE_ARITHMETIQUE.md:53-54` |
| L09-BORNE-039 | fixe d'un automorphisme (Wilbrink 1984) | ≤ | 18 points fixes pour une involution, 9 sinon | entrelacement de Haemers | P | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:131-132` |
| L09-BORNE-040 | \|Aut(Γ)\| (littérature) | \| | \|G\| divise 2·3³·7·11 (Makhnev–Minakova) ; 2 \| \|G\| ⟹ \|G\| \| 6 ; 7 \| \|G\| ⟹ G = Z₇ (Cesarz–Woldar) ; pas d'ordre 11 (Wilbrink), ni 6, 9 (Crnković–Maksimović) |  | P | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:97-102` |
| L09-BORNE-041 | srg(v,k,1,2) : k | = | u² + u + 2, u ∈ {1,3,4,10,31} (Makhnev–Minakova 2004) |  | P | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:100-101` |
| L09-BORNE-042 | c(F) (lemme de variance) pour grille / prisme / grille moins une arête | = | 0 / 30 / 5 | srg(99,14,1,2) | P | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:64-65` |
| L09-BORNE-043 | coclique (borne de Hoffman) | ≤ | 22 |  | P | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:67` |
| L09-BORNE-044 | rank₇(A − 3I) | ≥ | 25 (k ≥ 10) |  | S | `conway99-c1:main:notes/97_K_ET_TORSION.md:157` |
| L09-BORNE-045 | k (indice de Witt) | ≤ | 34 |  | P | `conway99-c1:main:notes/97_K_ET_TORSION.md:97-98` |
| L09-BORNE-046 | rank₃(A − 4I) de BvLS | = | 67 (borne van Eijl 111) | BvLS | E | `conway99-c1:main:notes/97_K_ET_TORSION.md:113` |
| L09-BORNE-047 | rang du bloc « deux étoiles » (échantillon) | ≥ | 14 observé (presque toujours 22, jamais < 18 au hasard) | 75 000 π aléatoires | H | `conway99-c1:main:notes/97_K_ET_TORSION.md:167-168` |
| L09-BORNE-048 | d(L) | = | 1 (85 %), 2 (14 %), 3 (0,6 %) ; max 9 (recuit) | configurations admissibles aléatoires | H | `conway99-c1:main:notes/99_VERROU_BOULES_DE_DROITES.md:13` |
| L09-BORNE-049 | Q₂ = Σ_L π(L)² | ∈ | [4P²/231, 24P] | relâchement triplets de droites | E | `conway99-c1:main:notes/99_VERROU_BOULES_DE_DROITES.md:105` |
| L09-BORNE-050 | μ_L à π(L) = 0 | ∈ | [0,18] (tout l'intervalle faisable) | modèle enraciné en une droite | E | `conway99-c1:main:notes/99_VERROU_BOULES_DE_DROITES.md:121-122` |
| L09-BORNE-051 | g_tot ; moyenne de g(x) | ≤ | 191 ; 17,4 | C4 = L5 + L10 + L16 | P | `conway99-c1:main:notes/100_SYNTHESE_DES_LEMMES.md:186-187` |
| L09-BORNE-052 | \|W(x)\| (plancher local) | ≥ | 6 (au moins 3 étiquettes tordues ou 2 avec \|C\| = 5, ≥ 4 classes) | C3 | S | `conway99-c1:main:notes/100_SYNTHESE_DES_LEMMES.md:184-185` |
| L09-BORNE-053 | χ(Σ) (surface des quadrangles) | ≤ | −705 | C6 | P | `conway99-c1:main:notes/100_SYNTHESE_DES_LEMMES.md:189` |
| L09-BORNE-054 | drapeaux non-grille contenant une droite à t ≤ 7 | ≥ | 254 si P ≤ 852 | ajout du 15/10 (version origin/main) | P | `conway99-c1:origin/main:notes/100_SYNTHESE_DES_LEMMES.md:12-13` |
| L09-BORNE-055 | census entier sans prisme | = | P = 0 admet un point entier non négatif aux ordres 7, 8, 9 (6 435 comptes) | ajout du 15/10 | E | `conway99-c1:origin/main:notes/100_SYNTHESE_DES_LEMMES.md:10-12` |
| L09-BORNE-056 | groupe critique | = | (Z/11)⁵³ ⊕ (Z/2)⁴⁴ ⊕ (Z/9)⁴³ | Ducey et al. | P | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:94` |
| L09-BORNE-057 | forme de Smith de S (Seidel) sur Z₇ | = | 1^{14+k} 7^{71−2k} 49^{14+k} |  | P | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:119-120` |
| L09-BORNE-058 | rang de R_L (résidu lointain d'une droite générique) | = | k − 22 | d(L) = 1 | P | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:133-134` |
| L09-BORNE-059 | solutions du modèle local autour d'un triangle de classes | = | 1 522 (sur 1 578 multi-ensembles) | point de Hamming | E | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:247-249` |
| L09-BORNE-060 | multi-ensembles compatibles avec le fait C | = | 58 (0, 2, 4 ou 6 isométries : 14, 27, 13, 4 cas) |  | E | `conway99-c1:main:notes/95_L7_PREUVE_HUMAINE.md:70-73` |
| L09-BORNE-061 | existence de srg(1+2m², 2m, 1, 2) | ∈ | m ∈ {2, 11} connus ; possibles m = 7, 56, 497 |  | P | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:160-162` |
| L09-BORNE-062 | rang₂ N (codes des droites) | = | 72 + ½ rang₂(NᵀAN) ≥ 72 |  | P | `conway99-c1:main:notes/110_ROUTES_CLOSES_ET_CODES_DES_DROITES.md:64-66` |
| L09-BORNE-063 | rang₅ N ; rang₃ N | ≥ ; ∈ | rang₅ N ≥ 72 ; 77 ≤ rang₃ N ≤ 98 |  | P | `conway99-c1:main:notes/110_ROUTES_CLOSES_ET_CODES_DES_DROITES.md:71-79` |
| L09-BORNE-064 | dimension du code des ensembles pairs E | ≤ | 27 (26 si tous les cardinaux ≡ 0 mod 4) |  | P | `conway99-c1:main:notes/110_ROUTES_CLOSES_ET_CODES_DES_DROITES.md:67-70` |
| L09-BORNE-065 | min Λ₃ ; min Λ₋₄ ; min K₃(x) ; min K₋₄(x) | ≤ | 36 ; 44 ; 38 ; 49 | Blichfeldt, k = 28 | P | `conway99-c1:main:notes/110_ROUTES_CLOSES_ET_CODES_DES_DROITES.md:16-19` |
| L09-BORNE-066 | g(x) | ≤ | 17 | tout sommet | P | `conway99-c1:main:notes/108_DEFAUTS_ET_COMPTAGE_DES_FENTES.md:87-88` |
| L09-BORNE-067 | configurations survivantes pour g(x) = 17 (\|𝒩\| = 4) | = | 20 ((0,2,0,2) : 8 ; (2,2,2,2) : 12 ; (0,2,2,2) : 0) | ordre deux | E | `conway99-c1:main:notes/112_VERS_G16_MOTIFS_A_QUATRE_DEFAUTS.md:72-76` |
| L09-BORNE-068 | solutions entières des identités du second ordre pour L14 | = | 2 160 survivantes sur 6 859 |  | E | `conway99-c1:main:notes/109_COEUR_TORSION_MAXIMALE.md:38-39` |
| L09-BORNE-069 | doubles par sommet en torsion maximale générique | = | 2 en moyenne (Σ_v Σ_R C(d_R(v),2) = 168 − e_int) |  | P | `conway99-c1:main:notes/109_COEUR_TORSION_MAXIMALE.md:26-33` |
| L09-BORNE-070 | arêtes internes e d'une famille triangle | ≤ | 12 | tout sommet, trois classes | P | `conway99-c1:main:notes/115_LEMME_DU_TRIANGLE.md:46-47` |
| L09-BORNE-071 | configurations admissibles tuées par le lemme du triangle (échantillon) | = | 23 sur 103 (sur 20 000 tirages) ; Fano : 270 sur 309 | torsion maximale | H | `conway99-c1:main:notes/115_LEMME_DU_TRIANGLE.md:62-64` |
| L09-BORNE-072 | configurations (P2) infaisables (échantillon) | = | 19/31 ; survivants blocs+cellules 3/45 ; paire×bloc 0/45 | torsion maximale, S = 0 | H | `conway99-c1:main:notes/117_P2_PAR_TYPES_TORSION_MAXIMALE.md:36-37` |
| L09-BORNE-073 | affectations de retournements Ψ-compatibles au témoin | = | 480 | σ du témoin fixé | E | `conway99-c1:main:notes/118_PAIRE_BLOC_ET_OBSTRUCTION_PSI.md:76-78` |
| L09-BORNE-074 | blocs « cellules par bloc » infaisables au Fano tendu | ∈ | [16, 19] sur 21 | configurations testées | E | `conway99-c1:main:notes/118_PAIRE_BLOC_ET_OBSTRUCTION_PSI.md:86-87` |
| L09-BORNE-075 | constante du repère (P2) | = | Σ_z ξ_zξ_zᵀ = 196·P_{E₋₂} ; trace 2744 | tout sommet | P | `conway99-c1:main:notes/117_P2_PAR_TYPES_TORSION_MAXIMALE.md:59-62` |
| L09-BORNE-076 | coupes de K(7,2) satisfaisant (T2) | = | 28 sur 2²⁰ | point de Hamming | E | `conway99-c1:main:notes/105_L8_DEMONTRE_FANO.md:134` |
| L09-BORNE-077 | q-rangs des réseaux lointains aux premiers propres | ≤ | 1 (312 boules) |  | E | `conway99-c1:main:notes/114_LABO_EXPERIMENTAL_GRAPHE_LOINTAIN.md:37` |
| L09-BORNE-078 | 99 droites équiangulaires de R⁴⁵ | ≤ | 540 (borne SDP Barg–Yu) |  | P | `conway99-c1:main:notes/114_LABO_EXPERIMENTAL_GRAPHE_LOINTAIN.md:77` |
| L09-BORNE-079 | solutions de KBLDP passant P-Ψ (heuristique) | ≈ | 0,2 % | Fano tendu | H | `conway99-c1:main:notes/121_POINT_D_ETAPE_26_09.md:33-34` |
| L09-BORNE-080 | configurations admissibles en torsion maximale | ≈ | 10¹⁰⁰ |  | H | `conway99-c1:main:notes/121_POINT_D_ETAPE_26_09.md:39-40` |
| L09-BORNE-081 | composantes de K à P = 0 (Astra) | ≤ | 3, chacune de taille multiple de 7 et ≥ 175 | P = 0 | P | `conway99-c1:main:notes/121_POINT_D_ETAPE_26_09.md:53` |
| L09-BORNE-082 | dim(K_cell ∩ V₃) ; dim ker₇(H − 3) ∩ K_cell | ≥ | 5 ; 35 − k ≥ 7 | tout sommet | P | `conway99-c1:main:notes/120_TRIADES_ET_VECTEURS_PROPRES_CELLULAIRES.md:22-27` |
| L09-BORNE-083 | 6-cycles c₆ ; hexagones induits H | = | 429 660 ; 213 444 − 3P |  | P | `conway99-c1:main:notes/123_PORTE_IX_TORSION_MAXIMALE.md:21-27` |
| L09-BORNE-084 | codimension de « rang₇ R_L ≤ 6 » ; de k = 22 | = | 210 ; 351 (sur ker₇ N de dim 26) |  | P | `conway99-c1:main:notes/124_LOINTAIN_D_UNE_DROITE_SCHUR.md:58-60` |
| L09-BORNE-085 | Σ_L c₄(G(L)) | ∈ | [3P, 4158] (en moyenne ≤ 18 par droite) |  | P | `conway99-c1:main:notes/125_CYCLES_COURTS_DES_GRAPHES_DE_DROITES.md:51-52` |
| L09-BORNE-086 | d(L) d'une droite (6,6) à P = S = 0 | ∈ | [2, 8] |  | E | `conway99-c1:main:notes/125_CYCLES_COURTS_DES_GRAPHES_DE_DROITES.md:107-108` |
| L09-BORNE-087 | composantes étiquetées (6,6) à maille ≥ 5 | = | 288 (15 types) | P = S = 0 | E | `conway99-c1:main:notes/125_CYCLES_COURTS_DES_GRAPHES_DE_DROITES.md:90-91` |
| L09-BORNE-088 | composantes à 4 et 6 étiquettes (P quelconque, filtrées) | = | 122 et 102 952 ; 6 672 à 6 étiquettes sans triangle avec torsion (6024/624/24 de dim 1/2/3) |  | E | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:87-93` |
| L09-BORNE-089 | S si « (4,4,4) partout » à P = 0 | ∈ | [2772, 4158] |  | E | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:115-116` |
| L09-BORNE-090 | k = 18 sous NT : P ; P(x) ; \|W(x)\| ; g(x) | ∈ | P ∈ [924, 1151] ; P(x) ≥ 56 ; \|W(x)\| ≤ 28 ; g(x) ∈ [14, 17] | sous (NT) | P | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:133-151` |
| L09-BORNE-091 | \|V₄₄₄\| (sommets à 7 droites (4,4,4), P = 0) | ≤ | 22 (Hoffman) et 49 (S ≤ 4158) | P = 0 | P | `conway99-c1:main:notes/128_RIGIDITE_444.md:9` |
| L09-BORNE-092 | solutions par système d'ombres à k = 28 (heuristique) | ≈ | 10^(−676) |  | H | `conway99-c1:main:notes/127_CARTE_DU_PROGRAMME_7_ADIQUE.md:47-48` |
| L09-BORNE-093 | g⁻ (involution, C2) | ∈ | {14,16,18,20} puis {16,18,20} (notes/129) puis {18,20} (notes/132) | C2 | C | `conway99-c1:main:notes/132_G16_IMPOSSIBLE.md:9` |
| L09-BORNE-094 | dim ker Q_c (torsion impaire d'un bloc, C2) | ≤ | 4 (exhaustif : 11 classes × 10 395 η) | C2 | E | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:111-115` |
| L09-BORNE-095 | classes (τ, η) à t ≥ 2 (C2, g = 16) | = | 96 (88 à t = 2, 5 à t = 3, 3 à t = 4) | C2 | E | `conway99-c1:main:notes/132_G16_IMPOSSIBLE.md:50-51` |
| L09-BORNE-096 | affectations des ombres frères de 3K2_or14 ; options des orbites croisées | = | 512 ; 0/576 admissibles | C2 | E | `conway99-c1:main:notes/131_ENTRELACEMENT_ALT_ET_RESIDUS_LOINTAINS.md:144-151` |
| L09-BORNE-097 | rang de K (Alt, C2) | ≤ | 14 | C2 | P | `conway99-c1:main:notes/131_ENTRELACEMENT_ALT_ET_RESIDUS_LOINTAINS.md:24` |
| L09-BORNE-098 | survivants ancrés par motif (C2) règle de la queue / + T⁺ | = | P₄ 24/0, P₃ 48/0, P₃+K₂ 12/4, K₃ 80/8, 3K₂ 44/44, 2K₂ 84/72, K₂ 144/144 | C2 | E | `conway99-c1:main:notes/130_MOTIFS_SIGMA_ANCRES.md:64-75` |
| L09-BORNE-099 | types (τ,η) valides à Aut(X_c,π) près | = | 3 308 | C2 | E | `conway99-c1:main:notes/133_REGIMES_Q7_ET_U_SIGNE.md:32` |
| L09-BORNE-100 | classes à pivots ; à ≥ 6 pivots ; pertinentes Σ = ∅ à ≥ 6 | = | 1 521 ; 156 ; 79 | C2 | E | `conway99-c1:main:notes/136_ECHELLE_DES_PIVOTS.md:56-60` |
| L09-BORNE-101 | Σ_c (2#piv_c + d_c) | = | 84 + 4\|Σ\| (donc un bloc a w_c ≥ 12) | C2 | P | `conway99-c1:main:notes/137_LIGNE_D_ARRIVEE_C2.md:22` |
| L09-BORNE-102 | types (A) de la ligne d'arrivée de C2 | = | 1 507 | C2 | E | `conway99-c1:main:notes/137_LIGNE_D_ARRIVEE_C2.md:69` |
| L09-BORNE-103 | enveloppes candidates de la ligne (C) | = | 156 (Table −4 de Borcherds) | C2 | E | `conway99-c1:main:notes/139_LIGNE_C_ENVELOPPES.md:11` |
| L09-BORNE-104 | enveloppes exclues (ligne C) | = | 9/156 (139, 27/09 après-midi) ; 10 (140) ; tracker C2 : 21 exclues, 2 partielles, 133 ouvertes (144) | C2 | P | `conway99-c1:main:notes/144_TRIAGE_OUVERTS.md:4` |
| L09-BORNE-105 | classes O₂₄ de paires (y₁,y₂) | = | 141 (3 302 040 configurations) | C2 | E | `conway99-c1:main:notes/140_LIGNE_C_PACKING_CONNEXITE.md:79-80` |
| L09-BORNE-106 | paires y de 132 ; de 124 ; de 87 | = | 304 ; 1 286 ; 3 913 | C2 | E | `conway99-c1:main:notes/142_EXCLUSION_132_ET_CHAINE_Y_H.md:32` |
| L09-BORNE-107 | paires de 132 tuées à la main | = | 258/304 (46 restent) | C2 | P | `conway99-c1:main:notes/143_LEMME_PI_FAMILLE_D2M.md:207` |
| L09-BORNE-108 | (V, y-paires) du rank-17 switch | = | 1 272 (1 142 si U sans racine) | C2 | E | `conway99-c1:main:notes/146_RANK17_YPAIRS.md:68` |
| L09-BORNE-109 | types de y-paires exclus (pass 2) | = | 59/1 272 (dont E8²+ℤ 12/12, D16⁺+ℤ 18/18) ; 1 213 MOD4_FEASIBLE | C2 | E | `conway99-c1:main:notes/147_RANK17_PASS2.md:117-118` |
| L09-BORNE-110 | feuilles estimées par paire MOD4_FEASIBLE (Knuth) | ∈ | [4,5·10⁴ ; 1,1·10¹²] ; 10⁶–10⁹ s par paire | C2 | H | `conway99-c1:main:notes/147_RANK17_PASS2.md:143-151` |
| L09-BORNE-111 | coupure de l'arbre par DC | ≈ | ×2 à ×3 (×1 sur ℤ¹⁷) | C2 | H | `conway99-c1:main:notes/148_SHORT_DUAL_DC.md:21` |
| L09-BORNE-112 | min 7\|κ\|² des 780 paires non tuées par min K* ≥ 5/7 | ∈ | {5,6,7,8} (438/239/20/83) | C2 | E | `conway99-c1:main:notes/150_ECHELLE_KSTAR_ET_COUPURE_2_5.md:10` |
| L09-BORNE-113 | β (classe A, coupure 2\|5) | ∈ | {12, 14, 16} ; toutes classes : [8, 16] | C2 | P | `conway99-c1:main:notes/150_ECHELLE_KSTAR_ET_COUPURE_2_5.md:90-113` |
| L09-BORNE-114 | couverture des 754 classes ouvertes par les échelons | = | R8 676, R6 555, R5 412, R7 274 ; R6∧R8 754 | C2 | E | `conway99-c1:main:notes/151_R6_PROGRAMME_J_CELLS.md:283-284` |
| L09-BORNE-115 | configurations de support J1a (v) ; (iii) | = | 2 741 040 000 ; 1 400 328 000 (0 survivant) | C2 | E | `conway99-c1:main:notes/152_J1a_CLOSED_EXHAUSTIVE_PSD.md:61` |
| L09-BORNE-116 | structures d'étoile canoniques R5 | = | 53 079 (855 / 12 875 / 13 223 / 26 126 par orbite) | C2 | E | `conway99-c1:main:notes/154_2x5_ENGINE_AND_ROUTE_CHANGE.md:66-67` |
| L09-BORNE-117 | e (arêtes de P) en J3 ; e_P en J2 | ∈ | [12, 24] ; [10, 14] (puis {10,12,14}) | C2 | P | `conway99-c1:main:notes/151_R6_PROGRAMME_J_CELLS.md:45-46` |
| L09-BORNE-118 | ensembles « ? » de la table de Brouwer exclus par S5 | = | 35 (v ≤ 1300) ; 185 (v ≤ 5000) ; 0/1 183 existants exclus |  | E | `conway99-structures-lab:master:NOTE_S5_DISCRIMINANT_MOD4.md:53-73` |
| L09-BORNE-119 | décompositions de E(K₇) en cycles (simples) ; systèmes de transitions étiquetés | = | 121 215 (20 types) ; 15⁷ | tout-tordu | E | `conway99-structures-lab:master:NOTE_S8_TOUT_TORDU.md:6-7` |
| L09-BORNE-120 | Σ doubles sur les 42 orbites (tout-tordu, n_s = 0) | ≤ puis = | 42 (budget 16.1), exactement 2 par paire (PPE) | C2 | P | `conway99-structures-lab:master:NOTE_S11_DEUX_TRIANGLES_SECANTS.md:35-36` |
| L09-BORNE-121 | doubles forcés pour (3⁵,6) ; pour le triangle de triangles | ≥ | 48 > 42 ; 43 > 42 | C2 tout-tordu | P | `conway99-structures-lab:master:NOTE_S8_TOUT_TORDU.md:69` |
| L09-BORNE-122 | décompositions tout-tordues : 2 triangles sécants ; 1 triangle ; 0 triangle | = | 27 720 (8 classes) ; 41 790 (15 classes) ; 30 360 (14 classes) | circuits simples | E | `conway99-structures-lab:master:NOTE_S11_DEUX_TRIANGLES_SECANTS.md:15-18` |
| L09-BORNE-123 | certificats exacts tout-tordu | = | 84 (1 triangle) + 14 (0 triangle), tous revérifiés |  | C | `conway99-structures-lab:master:JOURNAL.md:206-209` |
| L09-BORNE-124 | certificats de C1 revérifiés | = | 19/19 cellules + 2/2 paire × bloc |  | C | `conway99-structures-lab:master:JOURNAL.md:241-243` |
| L09-BORNE-125 | dim(K_cell ∩ V₃) en tout sommet | ≥ | 5 sur Q ; 7 mod 7 (avec k ≤ 28) | toute srg(99,14,1,2) | P | `conway99-structures-lab:master:JOURNAL.md:302-303` |
| L09-BORNE-126 | profils (1,1,1,1) au témoin de Fano tendu | = | 14/42 paires ordonnées |  | E | `conway99-structures-lab:master:JOURNAL.md:312-313` |
| L09-BORNE-127 | revêtements de degré 4 de K₇ avec λ = 1 | = | 1 (non régulier, monodromie S₄, 8 prismes) |  | E | `conway99-structures-lab:master:JOURNAL.md:369-371` |
| L09-BORNE-128 | h (apex) contre n_dis | ≤ | 3h ≤ 2n_dis | carrés dis | P | `conway99-structures-lab:master:JOURNAL.md:468` |
| L09-BORNE-129 | probabilité heuristique R_L = 0 | ≈ | 7^(−210) ≈ 10^(−177) (corrigé de 7^(−2916)) |  | H | `conway99-structures-lab:master:JOURNAL.md:471-472` |
| L09-BORNE-130 | espérance du nombre de solutions de l'étoile complète (k = 22) | ≈ | 8,6·10⁻¹⁶ (boule d'Astra) ; 2,2·10⁻¹⁵ (cyclique) | heuristique d'indépendance | H | `conway99-structures-lab:master:JOURNAL.md:647-649` |
| L09-BORNE-131 | classes de boules à P = 0 | ≈ | 10⁸ (P = S = 0) ; 8·10⁹ (S libre), dont 3·10⁹ génériques à τ non carré |  | H | `conway99-structures-lab:master:JOURNAL.md:667-671` |
| L09-BORNE-132 | g⁻ = rang₇(S − 3I) (involution) | ∈ | {8,…,20} pair → {16,18,20} → {18,20} | C2 | P | `conway99-structures-lab:master:JOURNAL.md:826` |
| L09-BORNE-133 | M (positivité, jauge de C2) | ∈ | [88, 173] | C2 | P | `conway99-structures-lab:master:JOURNAL.md:694` |
| L09-BORNE-134 | det du réseau N (Gram 3I − S, rang 22) | = | 7^{22−g⁻} (49 à g⁻ = 20, 7⁴ à g⁻ = 18) | C2 | P | `conway99-structures-lab:master:JOURNAL.md:703-705` |
| L09-BORNE-135 | det L_T ; min Λ₋₄⁻ | = ; ≥ | 2¹²7^{g⁻−7} ; 8 | C2 | P | `conway99-structures-lab:master:JOURNAL.md:749` |
| L09-BORNE-136 | classes AD ; mortes à n_dd ≤ 6 | = | 26 524 ; 6 079 | C2 AD | C | `conway99-structures-lab:master:JOURNAL.md:736-737` |
| L09-BORNE-137 | solutions du système local par type (heuristique) | ≈ | 10⁻¹⁰ (pleins, mixtes) ; 10⁻⁴·⁵ (étoiles libres) ; 10⁴⁸ à m = 11 |  | H | `conway99-structures-lab:master:JOURNAL.md:839-840` |
| L09-BORNE-138 | classes à ≥ 6 pivots ; pertinentes Σ = ∅ | = | 156 ; 79 = (2,2) 24, (1,4) 18, (2,4) 9, (3,0) 7, (0,6) 7, (3,2) 6, (4,0) 4, (6,0) 4 | C2 | E | `conway99-structures-lab:master:JOURNAL.md:852-854` |
| L09-BORNE-139 | table complète des classes (sans P = 0) | = | 3 308 (1 166 t = 0 scindées ; 835 étoiles libres t = 0 non scindées ; 441 types P = 0 de Sol = 362 C₁₂ + 79 2C₆) |  | E | `conway99-structures-lab:master:JOURNAL.md:855-859` |
| L09-BORNE-140 | types pertinents certifiés UNSAT (DRAT vérifié) | = | 25/79 puis 33/79 | 27/09 ~9 h 45 | C | `conway99-structures-lab:master:JOURNAL.md:935` |
| L09-BORNE-141 | nœuds de l'arbre PL (0,6) (Knuth, sécantes d'abord) | ≈ | 1,8·10⁵ à 1,6·10⁸ |  | H | `conway99-structures-lab:master:JOURNAL.md:930` |
| L09-BORNE-142 | classes O₂₄ exclues par PL entier | = | 86/141 (55 PL-faisables) | id 0 | C | `conway99-structures-lab:master:JOURNAL.md:975-977` |
| L09-BORNE-143 | paires Γ-réduites (132, 115, 87) | = | 2 416 → 304 ; 11 664 → 1 472 ; ~150 k → 3 913 | route C | E | `conway99-structures-lab:master:JOURNAL.md:989` |
| L09-BORNE-144 | id 1 (a₁⁸) : y admissibles → classes y₁ ; y₂ → classes de paires | = | 118 428 → 14 ; 3,09 M → 819 |  | E | `conway99-structures-lab:master:JOURNAL.md:998` |
| L09-BORNE-145 | \|Stab(μ,τ)\| maximal (classes frères) | = | 46 080 |  | E | `conway99-structures-lab:master:JOURNAL.md:955` |
| L09-BORNE-146 | vrais membres de la famille : P | = | P_max = L(m−1) : 6 (H(2,3)), 8 910 (BvLS) |  | E | `conway99-structures-lab:master:JOURNAL.md:575` |
| L09-BORNE-147 | v admissibles de la famille srg(2m²+1,2m,1,2) | ∈ | {9, 99, 243, 6 273, 494 019} (t \| 63) |  | P | `conway99-structures-lab:master:NOTE_S25_FAMILLE_9_243.md:9-10` |
| L09-BORNE-148 | taille n d'un ensemble GM (borne spectrale) | ≥ | v(1 − 3/(k − r))/2 : 36 pour 99, > 101 pour 243 |  | P | `conway99-structures-lab:master:NOTE_S25_FAMILLE_9_243.md:68-70` |
| L09-BORNE-149 | 1ᵀS1 (jauge de C2) | = | 497 − 4M | C2 | P | `conway99-structures-lab:master:NOTE_S27_INVOLUTION_GENRE_7ADIQUE.md:19-20` |
| L09-BORNE-150 | rangs de droite-bloc (11 classes de τ × 10 395 ι) | = | 14 : 800 ; 15 : 124 ; 16 : 11 363 ; 17 : 15 691 ; 18 : 86 367 | C2 | E | `conway99-structures-lab:master:NOTE_S27_INVOLUTION_GENRE_7ADIQUE.md:99` |
| L09-BORNE-151 | classes AD mortes par n_dd | = | 2 : 14 ; 3 : 8 ; 4 : 510 ; 5 : 853 ; 6 : 4 594 (somme 5 979) | C2 AD | C | `conway99-structures-lab:master:NOTE_S28_AD_NIVEAU_PAIRES.md:119-125` |
| L09-BORNE-152 | survivantes AD (version relâchée) | = | n_dd = 7 : 6 ; 8 : 20 ; 9 : 14 |  | S | `conway99-structures-lab:master:NOTE_S28_AD_NIVEAU_PAIRES.md:157-160` |
| L09-BORNE-153 | bijections Φ ; espérance de solutions du système local | ≈ | 60! ≈ 10^81,9 ; 10⁻¹⁰ (m = 7) contre 10⁴⁸ (m = 11) |  | H | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:91-95` |
| L09-BORNE-154 | classes par nombre de pivots | = | 0 : 1 787 ; 2 : 958 ; 4 : 407 ; 6 : 106 ; 8 : 39 ; 12 : 11 | C2 | E | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:169` |
| L09-BORNE-155 | équivalences de couplage à deux blocs ; instances | = | 364 (dont 80 nouvelles) ; 60 | T = K₇ | P | `conway99-structures-lab:master:NOTE_S33_DEUX_BLOCS_TK7.md:61-62` |
| L09-BORNE-156 | dual optimal sur O₂₄ (borne) | = | Y = 1 sur tous les u-candidats, borne 38 < 42 dans toutes les classes testées | id 0 | H | `conway99-structures-lab:master:NOTE_S38_ETAT_ET_PISTES.md:17` |
| L09-BORNE-157 | \|G₁\|/\|W\| pour id 1 (a₁⁸) | = | 10 321 920 (× 2 = 20,6 M) |  | E | `conway99-structures-lab:master:NOTE_S38_ETAT_ET_PISTES.md:12` |
| L09-BORNE-158 | min N* (involution) | ≥ | 8/7 | C2 | P | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER6.md:244-252` |
| L09-BORNE-159 | rang₇ Gram(L_T) | = | 22 − g⁻ (2 à g⁻ = 20 ; 4 à g⁻ = 18) | C2 | P | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER6.md:429-433` |
| L09-BORNE-160 | min L_T à g⁻ = 16 (Blichfeldt) | ≤ | 16,9 | C2 | P | `conway99-structures-lab:master:astra/PROBLEMES_OUVERTS_INVOLUTION.md:46-47` |
| L09-BORNE-161 | dim(G_x + G_a) pour la forme β de C1 | ≤ | k + 11 ≤ 39 (centres adjacents) ; k + 12 ≤ 40 (non adjacents) | C1, k ≤ 28 | P | `conway99-structures-lab:master:astra/RAPPORT_SOL_SUPPORTS_COURTS.md:247-257` |
| L09-BORNE-162 | classes Wagner à six blocs ; à sept blocs | = | 25 (exclues) ; 120 (ouvertes) | P = 0 | C | `conway99-structures-lab:master:astra/RAPPORT_SOL_WAGNER.md:5` |
| L09-BORNE-163 | classes (μ,τ) à t ≥ 2 pour g⁻ = 16 | = | 96 : Witt 69/88 (t = 2) + r₀ = 3 de 3 (t = 4), filtres unaires 19, 8 Farkas exacts | C2 | C | `conway99-structures-lab:master:astra/POUR_SOL_G18_G20_NOS_NOMBRES.md:10-13` |
| L09-BORNE-164 | classes (μ,τ) hors P = 0 ; à pivots ; étoiles libres avec 4-cycle ou arête π | = | 2 867 ; 1 521 ; 1 346 |  | E | `conway99-structures-lab:master:astra/POUR_SOL_G18_G20_NOS_NOMBRES.md:47-49` |
| L09-BORNE-165 | types t = 0 non scindés (impossibles à g = 18) ; t = 0 scindés | = | 1 448 ; 1 166 |  | E | `conway99-structures-lab:master:astra/POUR_SOL_G18_G20_NOS_NOMBRES.md:63-64` |
| L09-BORNE-166 | \|Aut(π, m)\| (bloc plein) | ∈ | {12, 32, 72, 384} |  | E | `conway99-structures-lab:master:astra/PROBLEME_BLOC_PLEIN_POUR_SOL.md:56-57` |
| L09-BORNE-167 | 6-cycles d'une srg(99,14,1,2) ; fixes sous une involution | = | 429 660 ; 224 | C2 | E | `conway99-structures-lab:master:logs/c2_programme.md:73-75` |
| L09-BORNE-168 | g(x) (grilles) au point fixe d'une involution | ≤ | 14 | C2 | P | `conway99-structures-lab:master:logs/c2_programme.md:591` |
| L09-BORNE-169 | nœuds de la recherche brute 12 × 12 (ordre 7) | ≈ | 8·10⁹ (0 solution à diagonale nulle) | ordre 7 | E | `conway99-structures-lab:origin/claude/chat-session-09hf0k:ordre7/tex/order7.tex:632-635` |
| L09-BORNE-170 | réseaux unimodulaires définis positifs de rang 17 | = | 9 (Conway–Sloane 1982 Table 6) ; un seul sans unité (A11E6) |  | P | `conway99-rank17:master:RANK17_HANDOFF.md:71` |
| L09-BORNE-171 | det de K = V ∩ y⊥ | = | 49 (rang 15) |  | P | `conway99-rank17:master:RANK17_HANDOFF.md:103` |
| L09-BORNE-172 | normes (a_cd, b_cd) | ∈ | {(5,5), (3,7), (7,3)} |  | P | `conway99-rank17:master:RANK17_HANDOFF.md:127-130` |
| L09-BORNE-173 | Y(v) pour un vecteur unité de V | ≤ | 4 (min U ≥ 2) ; 2 (min U ≥ 3) |  | P | `conway99-rank17:master:RANK17_HANDOFF.md:190-194` |
| L09-BORNE-174 | (V, y-paires) ; exclues par R≤4 ; par le moteur ; ouvertes | = | 1 272 ; 492 ; 26 ; 754 | 28/09 | E | `conway99-rank17:master:PROOF_OBLIGATION.md:232` |
| L09-BORNE-175 | couverture des 754 par R6 ∧ R8 | = | 754/754 |  | E | `conway99-rank17:master:PROOF_OBLIGATION.md:280` |
| L09-BORNE-176 | classes fermées par le test caractéristique | = | 228/751 (114 indépendantes du partenaire) | 29/09 | C | `conway99-rank17:master:r17_char/README.md:27` |
| L09-BORNE-177 | classes ouvertes après le test caractéristique | = | 526 | 29/09 | E | `conway99-rank17:master:GPT_PROMPT_TYPE0_TYPE2.md:9` |
| L09-BORNE-178 | 7·min Char(K*) (523 classes non-ℤ¹⁷) | = | 21 : 76 ; 29 : 378 ; > 33 : 69 ; 25 ou 33 : 0 |  | E | `conway99-rank17:master:GPT_PROMPT_TYPE0_TYPE2.md:12-17` |
| L09-BORNE-179 | orbites d'ancres Type 0 ; Type II | = | 3 (2 640 tournois réguliers étiquetés) ; 74 (42 + 32) |  | E | `conway99-rank17:master:sol_type02/PROOF.md:155-212` |
| L09-BORNE-180 | ‖Φ‖² des ancres caractéristiques ≤ 37 | ∈ | {21, 29, 37} |  | P | `conway99-rank17:master:sol_type02/PROOF.md:125-126` |
| L09-BORNE-181 | feuilles de l'étape A par paire ℤ¹⁷ (Knuth) | = | 0 : 1,7e8 ; 1 : 1,6e10 ; 2 : 7,2e9 ; 3 : 2,3e6 ; 4 : 5,4e7 ; 5 : 3,6e6 ; 6 : 4,4e5 ; 7 : 0 |  | H | `conway99-rank17:master:Z17_FINDINGS.md:105-114` |
| L09-BORNE-182 | classes forbidden DC par paire ℤ¹⁷ | ∈ | [41, 84] |  | E | `conway99-rank17:master:Z17_FINDINGS.md:88-89` |
| L09-BORNE-183 | motifs R8 k=3 | = | 209 classes en 8 types de placement (612 placements, groupe 36 864) |  | E | `conway99-rank17:master:r8k3/README.md:11-12` |
| L09-BORNE-184 | L_β : représentants I ; classes d'invariants ; restantes sans vecteur de norme 1 | = | 1 088 ; 31 ; 13 | k = 28 | E | `conway99-rank17:master:evenframe/README.md:36-40` |
| L09-BORNE-185 | solutions N² pour un N invariant Paley (ordre 21) sur l'ancre Type 0 | = | 0 (modes 0 et 1) | hypothèse de symétrie | E | `conway99-rank17:master:sol_type02/PROOF.md:375-378` |
| L09-BORNE-186 | squelettes binaires ρ échantillonnés (ℤ¹⁷, paire 0) ; survivants | = | 1 248 ; 0 | échantillon | H | `conway99-rank17:master:GPT_PROMPT_M1M2.md:22` |
| L09-BORNE-187 | Σ_w w_i² (budget de coordonnée, ℤ¹⁷) | = | 28 − 4Y(e_i) | repère serré | P | `conway99-rank17:master:Z17_SEARCH_DESIGN.md:19` |
| L09-BORNE-188 | collages D8³ recensés ; rejetés (norme 1, E8, D16) ; restants traités à la main | = | 135 ; 37 + 24 + 12 ; 32 |  | E | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:87-88` |
| L09-BORNE-189 | familles de classes D4⁶/cycle6 exclues | = | 231/256 (25 restent : 16 de taille 6, 8 de taille 7, 1 de taille 8) |  | P | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:205-206` |
| L09-BORNE-190 | matrices étiquetées (BvLS, deux prismes libres) | = | 27 648 = 2 × 13 824 = 2 × (4!)³ |  | E | `conway99-c1:origin/main:dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/RESULTATS.md:11` |
| L09-BORNE-191 | designs exclus (coclique 22) | = | 72 cycliques ; 199 one-rotational |  | E | `conway99-c1:origin/main:dossiers_externes/INDEX.md:17` |
| L09-BORNE-192 | Σ des arêtes orthogonales dans les 21 rectangles (racine choisie) | ≤ | ⌊6·852/99⌋ = 51 | P ≤ 852 | P | `conway99-c1:origin/main:AGENTS.md:689-691` |
| L09-BORNE-193 | 3P + 4G (prismes, grilles) | ≤ | 2 772 |  | C | `conway99-c1:origin/main:AGENTS.md:646` |
| L09-BORNE-194 | registre c3 de LAB (gabarits) | = | 10 052 → 1 187 → 1 163 → 902 → 537 → 435 ouverts (18–19/10) |  | C | `conway99-c1:origin/main:AGENTS.md:15` |
| L09-BORNE-195 | bords de la famille K3 universelle ; preuves RUP | = | 2 742 342 ; 322 |  | C | `conway99-c1:origin/main:AGENTS.md:146-147` |
| L09-BORNE-196 | rang(T44) ; ν(T44) | = | 23 − c(l) + rang(F) ; c(l) + 2 + corank(Q) |  | P | `conway99-c1:origin/main:AGENTS.md:799-800` |
| L09-BORNE-197 | rang_F7(8T44) observé sur 3 722 NG | ≥ | 30 (observation, pas un théorème) |  | H | `conway99-c1:origin/main:AGENTS.md:677-678` |
| L09-BORNE-198 | structures admissibles ⟨z,hM⟩ ; PSD ; nullité max | = | 339 556 ; 192 ; 9 |  | S | `conway99-c1:origin/main:AGENTS.md:1505-1506` |
| L09-BORNE-199 | affectations de signes (réduction V15) | ≤ | 8 192, puis ≤ 2 complétions isomorphes | bord43 positif | P | `conway99-c1:origin/main:AGENTS.md:1945-1947` |
| L09-BORNE-200 | raccordements résiduels 2K2 ; coupes utilisées | = | 7 (sur 5 bords) ; 99 + 73 = 172 |  | C | `conway99-c1:origin/main:notes/PREUVE_COUPES_CONTINUATION_2026_10_19.txt:196-202` |
| L09-BORNE-201 | registre c3 après fermeture 2K2 | = | 902 → 537 ouverts (365 retirés) |  | C | `conway99-c1:origin/main:notes/FERMETURE_2K2_2026_10_19.txt:22` |
| L09-BORNE-202 | bords de la famille K3 ; cœurs | = | 2 742 342 ; 23 (20 et 23 exclus analytiquement) |  | E | `conway99-c1:origin/main:notes/PRODUCTION_K3_UNIVERSELLE_2026_10_19.txt:24-28` |
| L09-BORNE-203 | raccordements 2K2N (catalogue LAB) ; classes | = | 1 006 sur 737 bords ; 823 (Codex) / 816 (LAB) |  | E | `conway99-c1:origin/main:notes/NOYAU_SIGNE_2K2N_2026_10_19.txt:157-162` |
| L09-BORNE-204 | sommets disjoints dominés par une grille | = | 40/40 (Conway, r = 7) ; 72/144 (srg(243), r = 11) |  | P | `conway99-c1:origin/main:notes/GRILLES_BC_PROFILS_2K2N_2026_10_19.txt:48-51` |
| L09-BORNE-205 | E(C) sur le noyau de 20 sommets (2K2N) | ∈ | {28, 32, 36, 40} | fermeture 2K2 | P | `conway99-c1:origin/main:notes/NOYAU_SIGNE_2K2N_2026_10_19.txt:84` |
| L09-BORNE-206 | rang r = rang₇(A − 3I) (après exclusion de 35) | ∈ | {37, 39, 41, 43} |  | E | `C:/home/researcher/cw/review/07_workspace_c1_0713.md:106` |
| L09-BORNE-207 | raccourcis « transfer » à recertifier (C2) | ≤ | 2 479 669 paires | parqué le 07/10 | O | `C:/home/researcher/cw/review/04_c2_routeC_researcher2.md:22-27` |
| L09-BORNE-208 | srg(243,22,1,2) connus non isomorphes | = | 8 (aucun asymétrique ; \|Aut\| minimal 108) |  | E | `C:/home/researcher/cw/review/07_workspace_c1_0713.md:178` |
| L09-BORNE-209 | coût du test d'étoile sur toutes les boules connexes (rang 37) | ≈ | 1,5–2,7 années-cœur (6,3·10¹⁰ boules à tester) |  | H | `C:/home/researcher/cw/review/07_workspace_c1_0713.md:135` |
| L09-BORNE-210 | rang_F7(A + 4I) (tout srg(99,14,1,2)) | = | a + 1 impair, ≤ 45 (a = rang_F7(Seidel) pair, 2 ≤ a ≤ 44) | dérivation du relecteur | H | `C:/home/researcher/cw/review/02_symmetry_c3_c7.md:301-303` |

### 10.3 Lemmes ouverts et étapes manquantes, et ce qu'ils donneraient (99)

| id | lemme ou étape manquante | donnerait | demandé par | source |
|---|---|---|---|---|
| L09-LEMME-001 | Plafond de torsion (borne inférieure globale sur P, ou majoration de k, ou plafond local) | contradiction avec les 21 lemmes-planchers (profil de torsion maximale P=0, g=0, k=30 les satisfait tous) | Claude-C1 | `conway99-c1:main:rapport/RAPPORT_C1.md:152-156` |
| L09-LEMME-002 | Borne inférieure P ≥ 1152 | contradiction avec L16 (P ≤ 1151) | Claude-C1 | `conway99-c1:main:notes/30_LEMMES.md:225-226` |
| L09-LEMME-003 | Majoration de Σν³ (équivalent : majorer n₃) | bornerait la torsion totale et forcerait des sommets peu tordus, exclus par la frontière | Claude-C1 | `conway99-c1:main:notes/30_LEMMES.md:209-211` |
| L09-LEMME-004 | F2-SRG : tout PQ(2,t,2) est grid-full (« torsion ⇒ excès > 0 », F20) | pas de Conway (L1), unicité de BvLS | Claude-C1 | `conway99-c1:main:notes/20_ATTAQUES_R.md:118-120` |
| L09-LEMME-005 | Montrer qu'en un sommet la torsion forte force rank₇ M_x ≥ 29 | relierait la dégénérescence 7-adique (L22) à la torsion | Claude-C1 | `conway99-c1:main:rapport/RAPPORT_C1.md:149-150` |
| L09-LEMME-006 | Prouver d(L) ≤ 9 (ou d ≤ 12) | k ≥ 14 (ou k ≥ 12) | Claude-C1 | `conway99-c1:main:rapport/RAPPORT_C1.md:251-252` |
| L09-LEMME-007 | Trouver un support S avec rang₇ Q_SS ≥ 43 (blocs avec arêtes génériques) | contradiction (critère L23) | Claude-C1 | `conway99-c1:main:rapport/RAPPORT_C1.md:141-142` |
| L09-LEMME-008 | L14 pour \|C\| = 5 ; confined(K) pour \|K\| = 4, 5, 6 ; sources(S) croissants ; certificats DRAT de L11/L14 | étendre la frontière de torsion | Claude-C1 | `conway99-c1:main:rapport/RAPPORT_C1.md:228-234` |
| L09-LEMME-009 | Tissu de 11 grilles, régime général (bijections ni iso ni anti) | compléterait L25 (identités Π, Y²+3Y+X² = 10, [X,Y] = 0) | Claude-C1 | `conway99-c1:main:JOURNAL.md:198-199` |
| L09-LEMME-010 | F16 : rigidité ⇒ symétrie (σ_x automorphisme forcé) | ramènerait C1 à C2 | Claude-C1 | `conway99-c1:main:notes/10_IDEES_F.md:33` |
| L09-LEMME-011 | Prouver d(L) ≤ 12 pour toute droite (ou d ≤ 9) | exclut k = 10 (C2) ; d ≤ 9 donne k ≥ 14 | Claude-C1 | `conway99-c1:main:notes/100_SYNTHESE_DES_LEMMES.md:183` |
| L09-LEMME-012 | Couplage de plusieurs étoiles (relations de lignes simultanées) au-delà de k ≥ 10 | améliorer le plancher de k | Claude-C1 | `conway99-c1:main:notes/97_K_ET_TORSION.md:158-159` |
| L09-LEMME-013 | Montrer qu'en un seul sommet la structure locale force rank₇(M_x) ≥ 29 | k = 30, interdit par L22 : contradiction | Claude-C1 | `conway99-c1:main:notes/101_GENRE_K_MAJORE.md:65-69` |
| L09-LEMME-014 | Blocs de rang ≥ 42 contenant des arêtes génériques de Γ₂(x) | contradiction via L23 / critère Seidel à k = 28 | Claude-C1 | `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:86-89` |
| L09-LEMME-015 | Version « torsion uniforme ⇒ plan d'ordre t » de F17 | à t = 6 : torsion non uniforme forcée (aucune conclusion directe) | Claude-C1 | `conway99-c1:main:notes/93_NON_EXISTENCE_V2.md:26-27` |
| L09-LEMME-016 | Degré 4 de positivité (configurations de 7–8 points) au-delà de L16 | borne dans l'autre sens sur P | Claude-C1 | `conway99-c1:main:notes/80_ETINCELLE_ARITHMETIQUE.md:72-73` |
| L09-LEMME-017 | Relation supplémentaire entre n₃ et S, ou contrainte sur Δ au-delà de Δ ⪰ 0 sur E₋₄ | contradiction (seules contraintes connues : 705 ≤ n₃ ≤ 4158, 0 ≤ S ≤ n₃) | Claude-C1 | `conway99-c1:main:notes/90_SECONDE_VARIABLE.md:80-84` |
| L09-LEMME-018 | Discriminant du réseau des droites Λ_L (3-rang et 7-rang de K) | rendrait exécutable l'argument d'Akiyama en rang 48 | Claude-C1 | `conway99-c1:main:notes/96_METHODE_AKIYAMA.md:81-82` |
| L09-LEMME-019 | Ordres 9–10 du comptage, idée globale (revêtement, rigidité, formes modulaires) ou recherche exhaustive | contradiction invisible jusqu'à l'ordre 8 | Claude-C1 | `conway99-c1:main:notes/91_HIERARCHIE_ORDRE8.md:63-66` |
| L09-LEMME-020 | Combinaison des relations du fait C (espace de dim 10) dont la partie locale en R soit additive | preuve de L8 par parité (dépassé) ; méthode pour d'autres régimes | Claude-C1 | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:235-237` |
| L09-LEMME-021 | Régime mixte du tissu de 11 grilles (bijections ni iso ni anti) | compléter L25 ; chercher d'autres configurations dont le serrage produit un 2-design de non-existence connue | Claude-structures | `conway99-c1:main:notes/104_TISSU_DE_GRILLES.md:125-127` |
| L09-LEMME-022 | Forcer l'existence d'un ensemble −4-serré | ferait une route (porteur du défaut de L22) | Claude-structures / Claude-C2 | `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L22.md:51-52` |
| L09-LEMME-023 | g(x) ≤ 16 : traiter les 20 configurations survivantes à l'ordre trois | plancher g(x) ≤ 16 | Claude-C1 | `conway99-c1:main:notes/112_VERS_G16_MOTIFS_A_QUATRE_DEFAUTS.md:82-94` |
| L09-LEMME-024 | L14 pour \|C\| ≥ 3 à la main (appariement des doubles pour m ≥ 4 ; argument fin pour \|C\| = 5) | certifier L14 sans SAT | Claude-C1 | `conway99-c1:main:notes/111_L14_C2_A_LA_MAIN.md:96-114` |
| L09-LEMME-025 | Lemme « aucun sommet de Fano tendu » : montrer qu'un des 21 blocs échoue toujours | premier lemme uniforme en torsion maximale | Claude-C1 | `conway99-c1:main:notes/118_PAIRE_BLOC_ET_OBSTRUCTION_PSI.md:90-92` |
| L09-LEMME-026 | Caractériser les survivants de (P2)/cellules et démontrer à la main la propriété qui les distingue | contrainte massive sur le cœur C1 | Claude-C1 | `conway99-c1:main:notes/117_P2_PAR_TYPES_TORSION_MAXIMALE.md:116-117` |
| L09-LEMME-027 | Niveau paires (466 000 colonnes) du modèle par types | étape de calcul suivante | Claude-C1 | `conway99-c1:main:notes/117_P2_PAR_TYPES_TORSION_MAXIMALE.md:15` |
| L09-LEMME-028 | Supports qui mêlent les données de plusieurs sommets (au-delà des étoiles et triangles) | contraintes exactes au-delà du lemme du triangle | Claude-C1 | `conway99-c1:main:notes/115_LEMME_DU_TRIANGLE.md:92-94` |
| L09-LEMME-029 | Combinaison sans retournement (noyau à gauche du système P-Ψ) toujours violée | lemme « aucun sommet de Fano tendu » | Claude-C1 | `conway99-c1:main:notes/119_PSI_PAR_PAIRE_FANO_TENDU.md:100-102` |
| L09-LEMME-030 | Coupler les triades entre elles (par λ_x, σ, P-Ψ) | contradiction au Fano tendu | Claude-C1 | `conway99-c1:main:notes/120_TRIADES_ET_VECTEURS_PROPRES_CELLULAIRES.md:68-70` |
| L09-LEMME-031 | Fano tendu par PLNE ou via configurations Z₇-invariantes (Singer) | clore le Fano tendu | Claude-C1 | `conway99-c1:main:notes/121_POINT_D_ETAPE_26_09.md:48-50` |
| L09-LEMME-032 | Modèle au niveau des paires voyant les 140 droites internes de I_x à P = 0 | porte I_x | Claude-C1 | `conway99-c1:main:notes/121_POINT_D_ETAPE_26_09.md:51-52` |
| L09-LEMME-033 | Strate rigide forcée à P = 0 (famille tendue, G(L) non connexe, revêtement au sens d'Astra) | plafond à P = 0 | Claude-C1 | `conway99-c1:main:notes/123_PORTE_IX_TORSION_MAXIMALE.md:63-64` |
| L09-LEMME-034 | (NT) : la torsion 7 d'une droite connexe n'est jamais équilibrée (Mᵀφ ≠ 0) | ferme k ≤ 18 (tout P) et k = 20 à P = 0 ; réduit k = 20 à P > 0 | Claude-C1 | `conway99-c1:main:notes/127_CARTE_DU_PROGRAMME_7_ADIQUE.md:37-42` |
| L09-LEMME-035 | (a′) uniforme : l'étoile complète est impossible pour toute boule générique à k = 22 | pas de droite générique à k = 22 | Astra / Claude-structures | `conway99-c1:main:notes/127_CARTE_DU_PROGRAMME_7_ADIQUE.md:43-44` |
| L09-LEMME-036 | Exclure « (6,6) partout » à P = S = 0, k = 22 | ferme k = 22 à P = S = 0 sous (i), (ii) | Claude-C1 | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:112` |
| L09-LEMME-037 | Torsion équilibrée sur la composante à 8 étiquettes des droites (4,8) (non testé) | fermer (4,8) ⟹ k ≥ 22 à P = 0 | Claude-C1 | `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:95-97` |
| L09-LEMME-038 | k = 20 à P > 0 sous NT : combiner les profils à c ∈ {3,4} | fermer k = 20 | Claude-C1 | `conway99-c1:main:JOURNAL.md:512-520` |
| L09-LEMME-039 | Relecture du §3 bis de notes/128 (k = 18 sous NT) | valider l'exclusion de k = 18 sous NT | Claude-C1 | `conway99-c1:main:notes/128_RIGIDITE_444.md:89-90` |
| L09-LEMME-040 | g⁻ = 18 par la méthode de notes/132 (balayer quelques milliers de classes, t = 0 compris) | réduire C2 à g⁻ = 20 | Claude-C1 | `conway99-c1:main:notes/132_G16_IMPOSSIBLE.md:77-84` |
| L09-LEMME-041 | Relecture indépendante de q7_3k2_ext.py | valide la mort de 3K₂ ancré et la clôture de la famille ancrée | Claude-C1 | `conway99-c1:main:notes/130_MOTIFS_SIGMA_ANCRES.md:281` |
| L09-LEMME-042 | Lemme qui coupe les arbres de squelettes du rank-17 (le calcul ne suffit pas) | clore les 1 213 paires MOD4_FEASIBLE | équipe (C1, structures, C2) | `conway99-c1:main:notes/147_RANK17_PASS2.md:153-154` |
| L09-LEMME-043 | min K* ≥ 9/7 | tue les 1 272 paires | Claude-C1 | `conway99-c1:main:notes/150_ECHELLE_KSTAR_ET_COUPURE_2_5.md:10` |
| L09-LEMME-044 | Preuve lisible de (B) (théorème de coupure 2\|5) utilisant la combinatoire exacte (bijections Φ, K₃, lemme CN) | fermer la famille tout-dis | Claude-C1 | `conway99-c1:main:notes/150_ECHELLE_KSTAR_ET_COUPURE_2_5.md:68-70` |
| L09-LEMME-045 | R6 : cellules J2 et J3 ; R8 k=2, k=3 | fermer R6 ∧ R8 | Claude-C1 / Claude-structures | `conway99-c1:main:notes/152_J1a_CLOSED_EXHAUSTIVE_PSD.md:8` |
| L09-LEMME-046 | Terminer le run R5 (≈ 4 h sur 14 threads) | tue 412 classes | Claude-C1 | `conway99-c1:main:notes/154_2x5_ENGINE_AND_ROUTE_CHANGE.md:96-106` |
| L09-LEMME-047 | Relecture humaine de l'exclusion de 132 (rigidité, cellules, complétude y) et seconde énumération indépendante | solidifier l'exclusion de 132 | Claude-C1 | `conway99-c1:main:notes/142_EXCLUSION_132_ET_CHAINE_Y_H.md:60-68` |
| L09-LEMME-048 | Lemme de famille pour les enveloppes rigides (charges κ_C non compensables avec (E1)) | tuer toute la famille rigide à la main | Claude-C1 | `conway99-c1:main:notes/143_LEMME_PI_FAMILLE_D2M.md:124-125` |
| L09-LEMME-049 | Théorie locale A>A+A (112 réseaux) puis D>A(n−1), et 124 | faire passer la ligne (C) aux familles non rigides | Claude-C1 | `conway99-c1:main:notes/144_TRIAGE_OUVERTS.md:41` |
| L09-LEMME-050 | g⁺ = 16 (228 types au cloud) et certification de g⁺ ≠ 14 | réduire C2 à g⁺ ≥ 18 | Claude-C1 | `conway99-c1:main:notes/135_SECTEUR_PAIR_Q7.md:13-14` |
| L09-LEMME-051 | Lemme de simplicité des structures D tout-tordues (ou UNSAT des 7 types (0,6), ou S17/S19 refaits sur ~3·10⁴ classes non simples) | exclusion complète du tout-tordu pur | Claude-structures | `conway99-structures-lab:master:REGISTRE.md:39` |
| L09-LEMME-052 | Lemme 11.2 de C2 ((2,0) contre (2,1) pour un carré dis) ; ne se démontre pas localement | fermer la famille dis (Σ = ∅) | Claude-C2 | `conway99-structures-lab:master:JOURNAL.md:469` |
| L09-LEMME-053 | Obstruction uniforme de l'étoile à k = 22 (tâche (a′)) | k = 22 (droite générique) exclu | Claude-C1 | `conway99-structures-lab:master:JOURNAL.md:653-655` |
| L09-LEMME-054 | k = 22 sans droite générique ; k = 24 à 28 ; NT | plafond 7-adique à P = 0 | Claude-C1 | `conway99-structures-lab:master:JOURNAL.md:636-639` |
| L09-LEMME-055 | Fano tendu satisfaisant toutes les bornes ordonnées | fermer (ou réaliser) le Fano tendu | Astra | `conway99-structures-lab:master:JOURNAL.md:411` |
| L09-LEMME-056 | Réseau de det 49 à g⁻ = 20 ; étoile totalement libre (μ ∩ τ = ∅) | fin du q:7 (involution) | Claude-structures | `conway99-structures-lab:master:JOURNAL.md:786-789` |
| L09-LEMME-057 | Théorème de corrélation entre blocs pour les mélanges restants | fermer M1/mélanges de C2 | Claude-structures | `conway99-structures-lab:master:JOURNAL.md:676-677` |
| L09-LEMME-058 | Complétude de l'énumération des paires de 132 (C2) | rendre l'exclusion de 132 complète | Claude-structures | `conway99-structures-lab:master:JOURNAL.md:990-991` |
| L09-LEMME-059 | Conjecture de Reimbayev (tout membre de la famille vérifie la propriété de grille) | unicité de srg(243,22,1,2) | Claude-structures | `conway99-structures-lab:master:JOURNAL.md:604` |
| L09-LEMME-060 | Avis d'expert sur la nouveauté du critère S5 | publication du critère 2-adique | Claude-structures | `conway99-structures-lab:master:NOTE_S5_DISCRIMINANT_MOD4.md:82` |
| L09-LEMME-061 | Certificats de branchement pour l'étage (0,6) et les classes frères (stabilisateurs jusqu'à 46 080) | théorème Σ = ∅ complet (79 types) | Claude-C2 | `conway99-structures-lab:master:JOURNAL.md:949-951` |
| L09-LEMME-062 | Rejouer L17 (scission locale 2/3/5) sur BvLS et Gewirtz (S4) | falsification de L17 | Claude-structures | `conway99-structures-lab:master:REGISTRE.md:12` |
| L09-LEMME-063 | Démontrer que P-Ψ tue des droites pour tout σ tendu (invariant par droite) | fermer le Fano tendu (C1) | Claude-C1 | `conway99-structures-lab:master:NOTE_S21_PSI_STRUCTUREL.md:119-120` |
| L09-LEMME-064 | AD pour n_dd = 7 à 21, puis la famille dis générale (paires mixtes « un bloc + dis », tordues avec dis) | fermer AD et dis (C2) | Claude-structures | `conway99-structures-lab:master:NOTE_S28_AD_NIVEAU_PAIRES.md:150-151` |
| L09-LEMME-065 | Preuve exhaustive par type du système local (B&B sur ι avec PL, ou SAT) ; méthode plus efficace pour ~10³–10⁴ classes | tuer les types non libres | Claude-structures | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:130-134` |
| L09-LEMME-066 | ÉTL : trouver une vraie solution locale (i)+(ii)+(iii) à m = 7, sinon un UNSAT par type | première solution locale (test q:7) ou exclusion des étoiles libres | Claude-structures | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:161-165` |
| L09-LEMME-067 | Deux blocs insuffisants : trois blocs, ou modèle complet avec variables lointain × lointain | tout-tordu non simple (T = K₇) | Claude-structures | `conway99-structures-lab:master:NOTE_S33_DEUX_BLOCS_TK7.md:92-94` |
| L09-LEMME-068 | Forme close du dual Y sur O₂₄ (Golay + positions des ±3 des y) | preuve à la main des 86 classes, généralisable | Claude-structures | `conway99-structures-lab:master:NOTE_S38_ETAT_ET_PISTES.md:17-19` |
| L09-LEMME-069 | Obstruction pour W = 2S + I (W² = 49I, structure de blocs) : Hasse–Minkowski ou code 7-aire auto-orthogonal | exclusion de l'involution | Claude-structures | `conway99-structures-lab:master:NOTE_S38_ETAT_ET_PISTES.md:20-22` |
| L09-LEMME-070 | Méthode de la preuve d'unicité de BvLS (si elle force les points de Hamming à m = 11, voir si elle se transpose à m = 7) | le plafond qui manque | Claude-structures | `conway99-structures-lab:master:NOTE_S25_FAMILLE_9_243.md:78-80` |
| L09-LEMME-071 | Un membre tordu (autre srg(243,22,1,2) sans (*), ou faux monde fermé aux paramètres de 99) | premier contrôle positif du régime tordu | Claude-structures | `conway99-structures-lab:master:NOTE_S25_FAMILLE_9_243.md:81-83` |
| L09-LEMME-072 | Exclure g⁻ = 18 et g⁻ = 20 (ou prouver g⁻ ≥ 21) ; mécanisme imposant rang₇ Gram(L_T) ≤ 1 | exclusion de l'involution (C2) | Astra / Claude-structures | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER6.md:435-437` |
| L09-LEMME-073 | Cas où les sept Q_c sont singuliers | complète la cible de C1 (résidu nul à g⁻ = 18, rang 2 à g⁻ = 20) | Astra | `conway99-structures-lab:master:astra/RAPPORT_ASTRA_DOSSIER6.md:468` |
| L09-LEMME-074 | Compléter ou tuer le support Wagner (120 classes à sept blocs) avec communs extérieurs et couplage D ; normes 9 et 10 | g⁻ = 12 par vecteurs courts (déjà exclu par Astra) ; cible « involution impose un prisme » | ChatGPT-Sol | `conway99-structures-lab:master:astra/RAPPORT_SOL_SUPPORTS_COURTS.md:277-279` |
| L09-LEMME-075 | Obstruction uniforme de l'étoile complète à k = 22 exploitant le Green cubique (la forme binaire seule ne suffit pas) | k = 22 exclu (C1) | ChatGPT-Sol | `conway99-structures-lab:master:astra/RAPPORT_SOL_SUPPORTS_COURTS.md:230-231` |
| L09-LEMME-076 | Une seconde détermination indépendante de r mod 2 ou du signe 7-adique k (Théorème B) | conclure par la voie 7-adique de C2 | Claude-C2 | `conway99-structures-lab:master:logs/c2_programme.md:69-70` |
| L09-LEMME-077 | Arbitrage (referee) et formalisation Lean de l'exclusion sans ordinateur de l'ordre 7 | théorème publiable sans ordinateur | Claude-cloud | `conway99-structures-lab:origin/claude/chat-session-09hf0k:ordre7/tex/order7.tex:61-62` |
| L09-LEMME-078 | R6 : cellules J2, J3 (et J1a au 28/09 soir avant notes/152) | avec R8 : Théorème C2 | Claude-C1 | `conway99-rank17:master:PROOF_OBLIGATION.md:303-310` |
| L09-LEMME-079 | R8 : k = 1, 2, 3 | 676 des 754 classes à lui seul | Claude-structures | `conway99-rank17:master:PROOF_OBLIGATION.md:312-319` |
| L09-LEMME-080 | Archiver et relire ligne à ligne les preuves de Sol (R≤4, §7.2, borne d'étoile, R1–R3, IB) ; certificat de complétude des 1 272 classes (F8) | transformer la chaîne en preuve (sinon « preuve modulo des entrées non vérifiées ») | Claude-C1 | `conway99-rank17:master:PROOF_OBLIGATION.md:321-330` |
| L09-LEMME-081 | Lemme qui coupe les arbres de squelettes d'un facteur ≥ 10⁴ (multi-vecteurs IB, colonnes de coordonnées libres) | rendre la plupart des cas calculables | Claude-C1 / Claude-structures | `conway99-rank17:master:GPT_FOLLOWUP_DC.md:30-48` |
| L09-LEMME-082 | Extension matricielle (N, π) pour les 3 ancres Type 0 et les 74 Type II | tue 76 et 378 classes | Claude-C1 | `conway99-rank17:master:GPT_FOLLOWUP_TYPE0_NEXT.md:47-60` |
| L09-LEMME-083 | Contrôle linéaire bon marché des cellules J/k de R6 et R8 sur BvLS (analogue à m = 11) | décider quelles cellules demandent un argument propre à m = 7 | Claude-C1 | `conway99-rank17:master:PROOF_OBLIGATION.md:358-360` |
| L09-LEMME-084 | Classe sans racine (PG(3,2), ovoïdes signés) du secteur pair : existence d'un repère | fermer une classe de L_β à k = 28 | Claude-structures | `conway99-rank17:master:evenframe/README.md:99-100` |
| L09-LEMME-085 | Une (1,2)-graphe de Cayley sur sous-groupes d'ordre 3 a-t-il ⟨D⟩ abélien (pas d'exemple courbe) ? | question sur la classe d'objets de Γ | Claude-structures | `conway99-rank17:master:paradigm/PARADIGM_BREAK.md:133-135` |
| L09-LEMME-086 | Lemme uniforme à la couche de relèvement : aucun (ρ, {w_u}) ne satisfait (ρ)+(G)+(M1)+(M2) | fermer V (tous) ou ℤ¹⁷ (8 paires) sans énumération | Claude-structures | `conway99-rank17:master:GPT_PROMPT_M1M2.md:34-35` |
| L09-LEMME-087 | Enveloppes rootless restantes, autres systèmes de racines, régimes D6⁴ (4,2)/(2,4), rangs 5–7 des octades | fermer la route (C) sans balayage | Astra | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:18` |
| L09-LEMME-088 | Région BvLS à trois prismes libérés | tester si une liberté plus grande permet un 243 nouveau / asymétrique | Astra | `conway99-c1:origin/main:dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/COORDINATION.md:26` |
| L09-LEMME-089 | α = 22 général (cocliques de Hoffman à 99) | exclure les cocliques de 22 ou les forcer | ChatGPT-externe | `conway99-c1:origin/main:dossiers_externes/HOFFMAN_UPDATE_20261011/README.md:18` |
| L09-LEMME-090 | NG7 (aucun bloc non-grille bas ne passe) | exclusion de Conway sous P ≤ 852 | Codex | `conway99-c1:origin/main:AGENTS.md:1311-1312` |
| L09-LEMME-091 | Preuve structurelle du plafond LOCAL 9 (annoncé complet par LAB826) | explication uniforme de la famille ⟨z,hM⟩ | Codex | `conway99-c1:origin/main:AGENTS.md:1525-1526` |
| L09-LEMME-092 | Famille co-Heawood (deux cocliques 22 disjointes du bord) | achève la réduction V15 | Codex | `conway99-c1:origin/main:AGENTS.md:1960` |
| L09-LEMME-093 | Gabarits c3 encore ouverts (435 au 19/10) ; 8650, gz3, 10006 ; familles P3, P3NB, K2BC, 2K2N | fin du cas c ≤ 3 donc de C1 (avec c(L) ≤ 3 forcé) | Codex / LAB | `conway99-c1:origin/main:AGENTS.md:15-17` |
| L09-LEMME-094 | Fermeture de P3 (étoile de grilles à ≥ 2 arêtes) | avec 2K2 et K3U, structure complète du graphe des grilles sous paire partagée | LAB | `conway99-c1:origin/main:notes/FERMETURE_2K2_2026_10_19.txt:114-115` |
| L09-LEMME-095 | Fermeture de 2K2N (et du cas sans grille B/C), de K2BC | réduction du registre c3 | Codex / LAB | `conway99-c1:origin/main:notes/NOYAU_SIGNE_2K2N_2026_10_19.txt:192-193` |
| L09-LEMME-096 | Contradiction manuscrite isolée pour la ligne 21 (Q13) au lieu du certificat sur tout le modèle | lemme humain réutilisable | Codex | `conway99-c1:origin/main:notes/GRILLES_BC_PROFILS_2K2N_2026_10_19.txt:144-146` |
| L09-LEMME-097 | Vérifier si le code DISC utilise L4 ; appliquer le filtre mod 7 rang₇((8T)_II) aux blocs à quatre étoiles | exclure la branche 14 de DISC / tuer des blocs | Claude-review | `C:/home/researcher/cw/review/05_c1_notes_00_99.md:264-274` |
| L09-LEMME-098 | Recertification des raccourcis « transfer » de C2 (≤ 2 479 669 paires) | lever la dernière réserve calculatoire de C2 | Claude-review | `C:/home/researcher/cw/review/04_c2_routeC_researcher2.md:22-27` |
| L09-LEMME-099 | Arbitrage humain / formalisation de C2 et de la chaîne « Conway asymétrique » | statut publiable | Claude-review | `C:/home/researcher/cw/review/04_c2_routeC_researcher2.md:36-40` |

### 10.4 Méthodes transférables entre cas (75)

« dit par » : `source` = la note le dit ; `consolidateur` = rapprochement proposé par ce lot, à vérifier.

| id | méthode | cas d'origine | cas cible | dit par | état | source |
|---|---|---|---|---|---|---|
| L09-METH-001 | Modèle enraciné exact + SAT pour exclure des configurations locales, validé sur l'analogue q=2 (Gewirtz) | C1 | tout cas où une configuration locale est prescrite (C2 : point fixe ; familles srg(n,k,1,2)) | source | fait | `conway99-c1:main:notes/20_ATTAQUES_R.md:147-159` |
| L09-METH-002 | Extraction de preuves humaines depuis une réfutation par propagation (explain_up.py) ou un noyau UNSAT minimal (core_extract.py) | C1 (L12, L9', L10) | tout verdict UNSAT court d'un autre cas (C2, rang 37, 2K2…) | consolidateur | proposé | `conway99-c1:main:notes/50_FRONTIERE_TORSION.md:42-47` |
| L09-METH-003 | Argument de genre / oddité sur le réseau propre Λ₋₄ (L22) | C1 | autres SRG (scan de genre du labo structures, S1) et involution (q:7, NOTE_S27) | source | fait | `conway99-c1:main:notes/30_LEMMES.md:298-305` |
| L09-METH-004 | Bornes de p-rang par sous-matrices principales déterminées (van Eijl 1991) : L20, L21 | C1 | C2 (q:7 : boule impaire d'une droite-bloc, notes/129) | source | fait | `conway99-c1:main:notes/30_LEMMES.md:264-265` |
| L09-METH-005 | Méthode des réseaux d'Akiyama (srg(266,45,0,9)) | srg(266,45,0,9) | 99 (C1) | source | échoué | `conway99-c1:main:rapport/RAPPORT_C1.md:240-243` |
| L09-METH-006 | Étincelle de C3 (Z[C₃] → Z × Z[ω], matrice d'Eisenstein M² + M = 12I) | C3 | C1 | source | échoué | `conway99-c1:main:JOURNAL.md:69-70` |
| L09-METH-007 | Méthode de C2 « H-β tué par types de paires » transposée au cœur C1 ((P2) par types) | C2 | C1 (torsion maximale) | source | fait | `conway99-c1:main:JOURNAL.md:260-264` |
| L09-METH-008 | Théorème F de C2 transposé en C1 (règles de triades rigides) | C2 | C1 | source | échoué | `conway99-c1:main:JOURNAL.md:284-285` |
| L09-METH-009 | Représentation euclidienne de Bondarenko–Radchenko (λ = 1, g = k ⇒ réflexions automorphismes ⇒ n = 3^m) | famille λ=1, g=k | 99 | source | échoué | `conway99-c1:main:JOURNAL.md:55-58` |
| L09-METH-010 | Méthode de Lam (codes à poids contraints, plan d'ordre 10) | PG(2,10) | 99 (F19) | source | échoué | `conway99-c1:main:notes/10_IDEES_F.md:41` |
| L09-METH-011 | Bornes ordonnées d'Astra (comptes triés par bloc) | C1 (Fano tendu) | toute situation où les comptes c_z(R) sont fixés, hors Fano aussi (strates (4,4,4), (6,6), (4,8)) | source | proposé | `conway99-c1:main:JOURNAL.md:330-333` |
| L09-METH-012 | RRR d'Elser (projections 0/1 ∩ spectre) pour construire des SRG | SRG connus (Hoffman–Singleton, Gewirtz) | 99 (construction) | source | échoué | `conway99-c1:main:JOURNAL.md:79-84` |
| L09-METH-013 | Méthode d'Akiyama (repère local serré, complétion unimodulaire paire, Venkov/thêta harmonique) | srg(266,45,0,9) | 99 : repères L₋₄ (56), L₃ (105), réseau des droites Λ_L (K² = 21K) | source | échoué | `conway99-c1:main:notes/96_METHODE_AKIYAMA.md:84-95` |
| L09-METH-014 | Identité trace–rang d'Ishida (quotient de Brauer) | graphe de Moore (3250,57,0,1), involutions | 99, branche C2 (involution) | source | fait | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:104-115` |
| L09-METH-015 | Lemme de variance de Wilbrink–Brouwer (c(F) ≥ 0) | srg(57,14,1,4) | 99 (sous-graphes induits interdits) | source | fait | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:60-76` |
| L09-METH-016 | Argument de saturation de Reimbayev (droite enracinée) | srg(19,6,1,2) | 99 | source | échoué | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:83-85` |
| L09-METH-017 | Énumération exhaustive + représentation euclidienne (Shpectorov–Zhao) | srg(85,14,3,2) | 99 | source | échoué | `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:117-125` |
| L09-METH-018 | Kneser signé de C2 (Théorème D) : signatures de K(7,2) équilibrées commutables (H¹ = 0) | C2 (involution) | C1 (point de Hamming : 3ᵉ preuve de L7, régime tout A) | source | fait | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:51-59` |
| L09-METH-019 | Lecture « matrice d'orbites mod 2 » de L7 (B̄² + B̄ = 12I + 4J − S) | C1 (point de Hamming) | C2 (involution σ_x ; points presque de Hamming) | source | proposé | `conway99-c1:main:notes/95_L7_PREUVE_HUMAINE.md:93-104` |
| L09-METH-020 | Discipline « tout lemme général testé sur BvLS (m = 11) » | C1 | toutes les branches | source | fait | `conway99-c1:main:notes/103_KNESER_POINT_DE_HAMMING.md:210-211` |
| L09-METH-021 | Hiérarchie de comptage exacte + positivité (Razborov, Gram euclidien) | C1 (ordre ≤ 8) | autres SRG / validation sur BvLS ; refaite le 07/10 depuis openai/math | source | fait | `conway99-c1:main:notes/91_HIERARCHIE_ORDRE8.md:17-34` |
| L09-METH-022 | Réduction d'une sous-structure tendue à un design de non-existence connue (polarité → PG(2,10)) | C1 (tissu de 11 grilles) | autres configurations serrées (2-designs, GDD) | source | proposé | `conway99-c1:main:notes/104_TISSU_DE_GRILLES.md:122-127` |
| L09-METH-023 | Comptage des fentes (offre/demande, quadrangles parfaits) | C1 (L11, g ≤ 17, L14) | budgets de C2 ; autres strates presque de Hamming | source | fait | `conway99-c1:main:notes/108_DEFAUTS_ET_COMPTAGE_DES_FENTES.md:93-95` |
| L09-METH-024 | Linéarisation de (P2) par types + certificats de Farkas exacts | C2 (H-β tué, labo C2 note 32) | C1 (torsion maximale) | source | fait | `conway99-c1:main:notes/117_P2_PAR_TYPES_TORSION_MAXIMALE.md:3-6` |
| L09-METH-025 | Cellules antipodales (raffinement de (P2)) | C2 | C1 (Fano tendu) | source | fait | `conway99-c1:main:notes/117_P2_PAR_TYPES_TORSION_MAXIMALE.md:78` |
| L09-METH-026 | Principe de Rayleigh sur un support entièrement déterminé | Astra (branche Z₇) | C1 (lemme du triangle) | source | fait | `conway99-c1:main:notes/115_LEMME_DU_TRIANGLE.md:90-92` |
| L09-METH-027 | Mécanisme de L8 (bijections de Kneser, droites = points fixes d'holonomie) | C1 (point de Hamming) | sommets presque de Hamming (L11, L14, g ≤ 16) ; ne se transporte pas en torsion maximale | source | proposé | `conway99-c1:main:notes/105_L8_DEMONTRE_FANO.md:175-178` |
| L09-METH-028 | Contenu de C3 (congruence Q/M mod 𝔭, symbole de Legendre) | C3 | C1 et C2 | source | échoué | `conway99-c1:main:notes/113_TRANSPOSITION_C3_CLOTURE.md:54-55` |
| L09-METH-029 | Méthode expérimentale de C3 (registre de pistes P/C, contrôles sur vrais graphes, balayage des tables de Brouwer) | C3 | C1 (labo c1_experimental) et labo structures | source | fait | `conway99-c1:main:notes/114_LABO_EXPERIMENTAL_GRAPHE_LOINTAIN.md:3-7` |
| L09-METH-030 | Théorème F de C2 (budget de doubles) | C2 | C1 (Fano tendu, triades) | source | échoué | `conway99-c1:main:notes/120_TRIADES_ET_VECTEURS_PROPRES_CELLULAIRES.md:68-70` |
| L09-METH-031 | L21/L23 (boule d'une droite, signe) dédoublés en secteurs pair/impair | C1 | C2 (q:7, droites-blocs) | source | fait | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:64-72` |
| L09-METH-032 | Équilibre d'une autre droite appliqué au partenaire τ (lemme R) | C1 ((4,4,4), k = 18 sous NT) | C2 (lemme de la queue, A111111) ; P > 0 à étudier | source | proposé | `conway99-c1:main:notes/128_RIGIDITE_444.md:83-86` |
| L09-METH-033 | Lignes rigides en un bloc plein (Z_ff ≡ 0 ⟹ ligne fixée mod 7) | C2 (3K₂ ancré) | C2 : résidus AD (bloc A plein), orbites dd rigides | source | proposé | `conway99-c1:main:notes/130_MOTIFS_SIGMA_ANCRES.md:285-286` |
| L09-METH-034 | Witt + équilibre + filtres unaires (problème local fini) | C2 (g⁻ = 16) | C2 (g⁻ = 18, g⁻ = 20) | source | proposé | `conway99-c1:main:notes/132_G16_IMPOSSIBLE.md:76-89` |
| L09-METH-035 | Torsion équilibrée / test par paires des triplets admissibles | C1 (droites (6,6)) | C2 (A111111 (3,3), torsion impaire) | source | fait | `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:177-184` |
| L09-METH-036 | Complétion de coquille (Gram de rang exactement 15, noyau exact, repère ajusté résiduel) | C2 rank-17 (J1a) | R8 k=1 ; J2, J3 ; toute structure à Gram global de rang connu | source | proposé | `conway99-c1:main:notes/152_J1a_CLOSED_EXHAUSTIVE_PSD.md:74-83` |
| L09-METH-037 | Contrôle « tout énoncé n'utilisant pas m = 7 doit être vrai sur Paley 9 et BvLS » | C2 | toutes les branches | source | fait | `conway99-c1:main:notes/138_GRILLE_DE_RELECTURE_RESEAUX_7_BLOCS.md:34-44` |
| L09-METH-038 | Identité du quadruplet ι (inclusion–exclusion sur quasi-design) | C2 (bloc plein) | C2 tous types (coupes --cuts, --digon, --twist, --ident) | source | fait | `conway99-c1:main:notes/134_SYSTEME_LOCAL_IOTA_BLOC_PLEIN.md:121-127` |
| L09-METH-039 | Filtre de témoins par classe (wfe, structures) | C2 rank-17 | remplace les théorèmes généraux R5/R6/R8 | source | fait | `conway99-c1:main:notes/154_2x5_ENGINE_AND_ROUTE_CHANGE.md:47-58` |
| L09-METH-040 | Vérificateur indépendant « premiers principes » pour un moteur d'énumération (a attrapé de fausses morts) | C2 rank-17 (cut25) | toute énumération exhaustive (consolidateur) | consolidateur | proposé | `conway99-c1:main:notes/154_2x5_ENGINE_AND_ROUTE_CHANGE.md:75-87` |
| L09-METH-041 | Principe de Rayleigh sur une branche partielle (vecteur q ⊥ 1 porté par des sommets connus, quotient > 3) | C1 (certificat d'Astra, mission géométrique) | tout cas avec branches partielles (C1, C2, rang 37) | source | fait (identifié au projecteur Π₋₄ du X12 de C1) | `conway99-structures-lab:master:NOTE_ASTRA_CERTIFICAT.md:26-35` |
| L09-METH-042 | Identité d'orbites Q² + Q = 12I + 4J − Sh (côté invariant de C2) transposée aux 42 cellules antipodales sans symétrie | C2 (involution) | C1 (cas général, Fano tendu) | source | fait (adoptée par C1, S20) | `conway99-structures-lab:master:REGISTRE.md:27` |
| L09-METH-043 | (P2) de C1 transposé au cadre de C2 (210 identités d'orbites) | C1 | C2 | source | fait | `conway99-structures-lab:master:REGISTRE.md:23` |
| L09-METH-044 | Contrôle positif systématique sur les vrais membres (H(2,3), BvLS avec σ = −v) | C1/C2 | tous les cas (dont rang 37, C3) | consolidateur | fait | `conway99-structures-lab:master:JOURNAL.md:185-190` |
| L09-METH-045 | Critère 2-adique S5 (discriminant mod 4) pour balayer les tables | srg en général | autres familles (p ≡ 3 mod 4 : parité de α_p à obtenir autrement) | source | proposé | `conway99-structures-lab:master:NOTE_S5_DISCRIMINANT_MOD4.md:97-98` |
| L09-METH-046 | Transfert d'un lemme de 243 (3-adique) vers 99 (7-adique) | srg(243,22,1,2) | C1 | source | écarté (pas de transfert direct) | `conway99-structures-lab:master:JOURNAL.md:614-616` |
| L09-METH-047 | Machinerie de l'étoile (k = 22, droite générique) appliquée aux droites à 3 composantes à k = 20 | C1 k = 22 | C1 k = 20 sous NT | source | proposé (aucune action) | `conway99-structures-lab:master:JOURNAL.md:680-685` |
| L09-METH-048 | Lemme de Witt général tiré du certificat de Sol sur A33 | C2 (A111111) | C1/C2 (g⁻ ≠ 16, tout bloc) | source | fait | `conway99-structures-lab:master:JOURNAL.md:823-824` |
| L09-METH-049 | Estimateur de Knuth sur l'arbre PL avant de lancer un arbre de Farkas | C2 (0,6) | toute énumération | consolidateur | fait | `conway99-structures-lab:master:JOURNAL.md:930-931` |
| L09-METH-050 | Spec déclarable + lex-leader vérifiable (compile(SPEC) = encode, invariance sous les générateurs) | C2 (SAT des 79) | toute certification SAT avec brisure de symétrie (C1 2K2, rang 37) | consolidateur | proposé | `conway99-structures-lab:master:JOURNAL.md:952-958` |
| L09-METH-051 | Filtre PSD 𝒫 = 6I − 2Q − Sh + J (𝒫² = 14𝒫) par sous-matrices principales | C2 (dis, Astra) | squelettes de tout cas à identité quadratique | source | fait (impliqué par le PL d'orbites) | `conway99-structures-lab:master:JOURNAL.md:460-461` |
| L09-METH-052 | Contrôles positifs du côté 7-adique : ils doivent venir d'autres familles (aucun membre réel) | famille 9/243 | C1/C2 (7-adique) | source | règle de méthode | `conway99-structures-lab:master:NOTE_S25_FAMILLE_9_243.md:17-18` |
| L09-METH-053 | Contrôle positif BvLS (σ = −v) : dégénéré (μ = τ = π) pour les termes τπ/πτ | C2 (système local) | toute validation sur BvLS | source | réserve | `conway99-structures-lab:master:NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:147-150` |
| L09-METH-054 | Transférer la preuve de C3 (ordre 3) à l'involution | C3 | C2 | source | proposé (jugé vide par C2 côté 2-adique) | `conway99-structures-lab:master:NOTE_S38_ETAT_ET_PISTES.md:16` |
| L09-METH-055 | Certificats entiers xᵀ𝒫x < 0 par compléments de Schur sur un PSD exact | C2 (dis, NOTE_S23) | toute identité 𝒫² = c𝒫 | consolidateur | proposé | `conway99-structures-lab:master:NOTE_S23_ENONCE_DOSSIER4.md:149-157` |
| L09-METH-056 | Commutation de Godsil–McKay comme moyen de construire des membres | famille | C1 construction (243 tordu) | source | exclu (rigidité GM) | `conway99-structures-lab:master:NOTE_S25_FAMILLE_9_243.md:74-75` |
| L09-METH-057 | Matrice quotient d'orbites + compression de Gram (G = 3C + 12I − 4J − 2uuᵀ, G² = 21G, rang 4) | ordre 7 (Aut) | C3 (ordre 3), C2 (involution : S² + S = 12I, 𝒫² = 14𝒫) | consolidateur | proposé | `conway99-structures-lab:origin/claude/chat-session-09hf0k:ordre7/tex/order7.tex:276-292` |
| L09-METH-058 | Recoller N ⊕ diag(7,7) en un unimodulaire impair de rang 24 (Borcherds) | C2 (q:7, problème 2) | route (C) des 156 enveloppes | source | fait (devient la route C) | `conway99-structures-lab:master:astra/PROBLEMES_OUVERTS_INVOLUTION.md:64-65` |
| L09-METH-059 | Contrôles positifs m = 2 et m = 11 exigés pour tout lemme général ; contradiction à m = 7 via arithmétique propre (θ − τ = 7) | C2 (carnet) | tous les cas | source | règle de méthode | `conway99-structures-lab:master:logs/c2_programme.md:4-7` |
| L09-METH-060 | Théorème de Hall / b-couplages pour les budgets locaux | C2 (Théorème P) | autres budgets (C1) | source | testé : Hall ne mord pas dans les cas ancrés restants | `conway99-structures-lab:master:logs/c2_programme.md:633-654` |
| L09-METH-061 | Switch de rang 17 directement depuis N (sans classification des 156 enveloppes ni min U ≥ 2 de base) | C2 (route C) | C2 (9 réseaux de rang 17) | source | fait | `conway99-rank17:master:RANK17_HANDOFF.md:83-95` |
| L09-METH-062 | Vecteur caractéristique + identité de repère (énergie caractéristique) pour fermer des orbites de normales | C2 rank-17 (Astra) | toute recherche de repère serré dans un réseau unimodulaire | consolidateur | proposé | `conway99-rank17:master:r17_char/ASTRA_PROOF_29_09.md:27-47` |
| L09-METH-063 | Estimateur de Knuth sur l'arbre canonique pour décider de la faisabilité d'une énumération | C2 rank-17 | toute énumération exhaustive (rang 37, 2K2…) | consolidateur | fait | `conway99-rank17:master:Z17_FINDINGS.md:99-124` |
| L09-METH-064 | Test d'entrelacement / sous-matrice principale avec borne de rang (projecteurs P₋₄, P₃) | C2 (R8 k=1, J1a) | C1 (tout support partiellement forcé en un sommet) | consolidateur | proposé | `conway99-rank17:master:TARGETS_AB_STRUCTURES.md:273-282` |
| L09-METH-065 | Moyenne des duaux de Farkas sur le stabilisateur pour obtenir des certificats uniformes | C2 (LP de nœud) | toute famille de certificats par configuration (C1 (P2), 2K2…) | source | proposé | `conway99-rank17:master:RANK17_HANDOFF.md:262-268` |
| L09-METH-066 | Test flottant PSD uniquement comme élagage (ne peut jamais créer une fausse solution), re-vérification exacte LDLᵀ en pass 2 | C2 rank-17 | toute recherche avec filtre PSD (C1 blocs T/U) | consolidateur | règle de méthode | `conway99-rank17:master:SPEC_ENGINE.md:53-54` |
| L09-METH-067 | Reconstruction à bord libéré + classification exhaustive des domaines de lignes (sans fibres) | Paley(25), BvLS | C1 (construction asymétrique) ; contrôles 243 | source | fait (Paley 25 → BvLS) | `conway99-c1:origin/main:research/astra_bvls_boundary_20261011/COORDINATION.md:13` |
| L09-METH-068 | Piège dual (min N* ≥ 8/7) appliqué à la coque de norme 3 d'une enveloppe | C2 (route C) | rank-17 (min K*), toute enveloppe de repère serré | consolidateur | fait côté C2 (route C, rank-17) | `C:/home/researcher/Desktop/Recherche_Conway/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md:63-69` |
| L09-METH-069 | Certificats entiers « sans Gram » sur catalogues d'états de lignes (moments, coins, E3) | C1 gabarits c3 | autres gabarits / familles | source | fait (5128, 4192, gz9748) | `conway99-c1:origin/main:AGENTS.md:549-556` |
| L09-METH-070 | Manifestes d'assemblage (couverture + RUP vérifiés, refus des couvertures partielles) | C1 (K3U, 2K2, gz5602) | toute fermeture de famille par calcul | source | fait | `conway99-c1:origin/main:AGENTS.md:144-150` |
| L09-METH-071 | Contrôles positifs sur deux vrais srg(243,22,1,2) (BvLS, twin) avec la constante générale r = 11 (sans importer les spécialisations r = 7) | C1 (Conway) | tout nouveau filtre | source | fait | `conway99-c1:origin/main:notes/GRILLES_BC_PROFILS_2K2N_2026_10_19.txt:50-52` |
| L09-METH-072 | Noyaux signés par ensemble S de racines (élimination des sommets mixtes) | 2K2N | K2BC, P3NB, gz5602 | source | fait (K2BC, P3NB) ; proposé pour gz5602 | `conway99-c1:origin/main:notes/NOYAU_SIGNE_2K2N_2026_10_19.txt:90-100` |
| L09-METH-073 | Identification T = 7Π_{K₋₄} : réutiliser l'arithmétique des repères serrés (notes/96, 97, 102) | C1 notes 96–102 (24–25/09) | C1 blocs à quatre étoiles (14–16/10) | source | proposé | `C:/home/researcher/cw/review/05_c1_notes_00_99.md:251-262` |
| L09-METH-074 | Pipeline cœur UNSAT → lemme (core_extract, explain_up, core_family) | C1 (L9', L12) | C1 (échec de la cinquième étoile DRAT) | source | proposé | `C:/home/researcher/cw/review/05_c1_notes_00_99.md:280-282` |
| L09-METH-075 | Compression de Gram de C7 et LP agrégé avec Farkas | C7 (ordre 7) | C1 (couple (T, U), sous-graphes asymétriques) | source | proposé | `C:/home/researcher/cw/review/02_symmetry_c3_c7.md:25-33` |
