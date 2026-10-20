# Fiche L01 — Origines et branche C2 (involution) du graphe de Conway srg(99,14,1,2)

Agent L01, chantier du 20/10/2026. Lecture seule. Sources : la liste `lots/L01_origines_C2.jsonl` (766 contenus distincts) ;
quelques fichiers du lot L02 (MODEL.md, FINAL_STATEMENT_C2_DRAFT, VERIF_CUBE_OBSTRUCTION, dossier Wagner, t20_hand) ont été lus
pour le contexte seulement et sont signalés comme tels. Statuts P/C/E/S/H/O/R/X recopiés des sources, sans rehausse. Les sources
sont citées `dépôt:branche:chemin:ligne` (dépôts git dans `C:/home/researcher/cw/`) ou par chemin absolu ; l'identifiant du lot
espace researcher2 est noté `conway_c2_researcher2_start_2026_09_30:` (racine
`C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/`).

## 1. Résumé (10 lignes)

1. Le lot couvre la branche C2 du 21/09 au 14/10 : dépôt d'origine conway99-involution (premier travail, 21/09) et son carnet MATH_C2_PROGRAMME ; labo c2_experimental (avec le labo « structures », Astra/Sol, notes C1 copiées) ; c2-compute ; archive conway99-c2-campaign (et sa copie zip turbo-octo-waffle) ; paquet et travaux du chercheur 2 ; notes C2 de l'espace researcher2 (route C, cascades, audit 156, passation) ; mission « C2 sans calcul » et consolidation de l'article d'ordre 2 ; conway-C7 ; quelques pièces C1 (audit v7, mots binaires mod 7, données r6) rangées ici par leur chemin.
2. Cadrage (21/09) : |Aut| ∈ {1,2,3} (littérature) ; une involution fixe un seul sommet et agit en flip ; couplage parfait D sur les 42 orbites ; modèle exact à 42 orbites ; plus tard (30/09) système (S)/L_N et T4 (complétion réelle intégrale et unique), relu une fois par un relecteur indépendant, non formalisé.
3. Trois voies successives : (i) SAT/CP-SAT génériques (21-22/09) : tous UNKNOWN ; (ii) « familles » (23-27/09) : lemme des étoiles (|Σ| ≤ 4), allsib, Fano, ancrées, H-β (552 certificats), M1, tout-tordu (circuits simples seulement), AD2… puis abandon faute de levier pour les mélanges et les carrés disjoints ; (iii) route (C) (27/09-07/10) : enveloppe unimodulaire impaire de rang 24 → 156 réseaux de Borcherds, exclus un par un ; tracker 156/156 le 07/10 à 17:47 UTC.
4. Statut de « pas d'involution » au 07/10 : preuve écrite + calcul (P), arbitrée par des sessions IA (Codex), aucun lecteur humain, rien de formalisé ; repose sur Borcherds et la formule d'oddité (cités), la complétude des énumérations de paires (comparée sur 4 réseaux), un audit du moteur, T16/T18/T20 (assistés par ordinateur) ; l'audit du 13/10 de l'article note un calcul encore ouvert (recertification de 4 163 099 transferts).
5. Avec l'ordre 3 (lot L04, Lean) et l'ordre 7 (conway-C7, Lean, sans ordinateur) : un graphe de Conway éventuel serait asymétrique (corollaire 1.2 de l'article du 07/10) — seul C1 reste.
6. Mission du 13/10 : un vecteur d'énergie E ≤ 12 est forcé par les formes modulaires (non audité) ; deux lemmes manquants (E = 11, 12 : T22, T24) remplaceraient les 156 réseaux ; sondage : ~5·10^7 cas pour E = 11.
7. Chercheur 2 (30/09-01/10) : EX ouvert, « 0 cas fermé », R1-R21 surtout reformulations et redécouvertes (déclarées).
8. Redécouvertes majeures : allsib impossible établi 3 fois (24/09, 25/09, 30/09), parité du 7-rang 5 fois (23/09 → 01/10), G1 3 fois ; retraits : congruence c4, « rang 20 info nouvelle », Théorème A v1, n3 ≡ 0 mod 6, log one10, verdicts pair_h_check @ 96a94fe, « tout-tordu exclu » réduit aux circuits simples.

## 2. Chronologie globale (détails par partie en §7)

| date (2026) | événement | source |
|---|---|---|
| 21/09 16:51 UTC | ouverture de la session d'origine eeaf2d22 (premier travail Conway) | conway99-involution:master:notes/ONE10_PROVENANCE.md:20 |
| 21/09 19:00 | premier commit bf0443f (Dilan Djematene) : réduction de l'involution, rang F2, audit d'ordre 7, premiers calculs | git log conway99-involution |
| 21-22/09 nuit | 7 instances SAT × 8 h : toutes UNKNOWN | conway99-involution:master:results/BATCH_2026-09-21_overnight.md:1-14 |
| 22/09 | audit du dépôt (retraits : c4, rang 20, F3(iv) ; contrôle fort BvLS) ; session labo : contrôles OK, Stage Q, 1 326 cubes, arrêt 23:38 | notes/AUDIT_2026-09-22.md ; results/LAB_2026-09-22_summary.md |
| 23/09 | labo c2_experimental isolé : G1, S1, Z7/Hamming, parité du 7-rang (note 09), N09 (transfert C3 vide), certificats DRAT sur Σ | conway99-c2-experimental JOURNAL.md:7-87 ; SYNTHESE.md |
| 24/09 | allsib à la main (cohomologie de M7) ; système χ ; lemme des étoiles (|Σ| ≤ 4, 10 survivants) ; étoile libre ; revue complète (note 22) | git ef1ff6d … 4722c76 |
| 25/09 | carnet MATH_C2_PROGRAMME (sans solveur) : Théorèmes D, F, P, D′ ; audit d'Astra : Théorème A v1 faux, corrigé ; lemme de la queue ; labo « structures » ouvre son journal (S5) | git conway99-involution fc0eb23 … 0fed809 |
| 26/09 | H-β mort (552 certificats), M1 n = 3, 4, tout-tordu (simple), AD2, A33 (Sol), g⁻ ≠ 16 ; C1 et « structures » rejoignent la branche (note 41) ; c2-compute | git conway99-c2-experimental 57ea5fe … 6fed2da |
| 27/09 | M1 certifié ; 79 systèmes locaux (25/79) ; TROU du tout-tordu non simple ; ligne d'arrivée I(τ) ; bug pair_h_check ; dossier Sol/Astra 0836 → route (C), 156 réseaux ; calibrage β 32/32 inconnu → (C) voie principale ; tracker 9 → 19/156 ; 87 exclu | notes 45-49 ; git 8c2a1d1, 0f622d7 |
| 27-28/09 | session Fable (cœur, arithmétique) | c2-compute:origin/claude/tender-archimedes-q532j1 |
| 28-29/09 | rang 17 ; modèle joint ; 47 puis 58/156 ; théorèmes de coquille ; contre-exemple fractionnaire ; plan AWS | Desktop notes 52-57 ; route_c_29_09 ; external_runs |
| 30/09 | dossier T4 + relecture indépendante ; paquet du chercheur 2 ; note ternaire (agent 2) | conway_c2_researcher2_start_2026_09_30:AUDIT_STATUS.md ; archive/FULL_DOSSIER.md |
| 01/10 | chercheur 2 : R12-R21, STRATEGY_MAP ; archive c2-campaign et zip turbo-octo-waffle ; import AWS (94/156) ; file adaptative | RESEARCH_HISTORY.md ; ROUTE_C_RESUME_STATUS.md |
| 02/10 | conway-C7 : ordre 7 sans ordinateur + Lean ; cascade 132/156 ; loi K + E | git conway-C7 ; CASCADE_STUDY_2026-10-02.md |
| 03-04/10 | étude du coût ; arrêt AWS ; passation (142/156) ; audit 156/156 (erratum 150 ; route C indépendante de T4) ; obstruction du cube (ChatGPT) vérifiée | HANDOVER_2026-10-04.md ; AUDIT_156_PLAN_2026-10-04.md |
| 07/10 | Théorème R audité (A.0-A.9), T16/T18/T20 acceptés ; tracker 156/156 (17:47 UTC) ; énoncé final (brouillon 7) ; article écrit (19:30) | FINAL_STATEMENT_C2_DRAFT_2026-10-07.md ; aws_repo/HANDOFF_2026-10-01.md §19-20 |
| 12/10 | audit v7 (srg(243) : Γ3, Γ4 ; Z3-revêtements : 4) ; mots binaires mod 7 (C1) | code/lab_audit_v7_2026-10-12 ; code7_mots_binaires |
| 13/10 | mission « C2 sans calcul » (E ≤ 12 forcé ; T22/T24 manquants) ; inventaire des campagnes ; audit de l'article d'ordre 2 ; Partie I rédigée | code/lab_c2_elegant_2026-10-13 ; lab_c2_consolidation_2026-10-14 |
| 14/10 | identités vérifiées sur 1 042 paires ; sondage E = 11 ; T16 partie A | REGION_PAIRS_REPORT.md ; SOUNDING_E11.md |

## 3. Résultats (125 entrées ; détail complet dans `fiches/L01_origines_C2.jsonl`)

Statuts : P preuve écrite (relecteur indiqué dans le jsonl) · C calcul exact certifié · E calcul exact sans certificat exporté · S solveur sans certificat · H heuristique · O ouvert · R réfuté · X retiré.

| id | énoncé court | statut | date | source principale |
|---|---|---|---|---|
| L01-01 | Cadrage : \|Aut(Γ)\| ∈ {1, 2, 3} | P | 2026-09-21 | conway99-involution:master:notes/NOTE_involution_case.md:7-18 |
| L01-02 | Rigidité de l'involution (flip, a1 = 14) | P | 2026-09-21 | conway99-involution:master:notes/NOTE_involution_case.md:20-27 |
| L01-03 | Couplage parfait D sur les 42 orbites extérieures | P | 2026-09-21 | conway99-involution:master:notes/NOTE_involution_case.md:28-29 |
| L01-04 | Modèle exact à 42 orbites (R),(D),(I),(P) | P | 2026-09-21 | conway99-involution:master:notes/NOTE_involution_case.md:30-33 |
| L01-05 | Quotients Q et S, spectres imposés | P | 2026-09-21 | conway99-involution:master:notes/NOTE_involution_case.md:34-37 |
| L01-06 | Théorème de rang F2 : rank_F2(Γ̄ + Nb Nbᵀ) = 20 | P | 2026-09-21 | conway99-involution:master:notes/NOTE_involution_case.md:39-48 |
| L01-07 | RETIRÉ : « le rang 20 est une information véritablement supplémentaire » | X | 2026-09-22 | conway99-involution:master:notes/AUDIT_2026-09-22.md:24-25 |
| L01-08 | RETIRÉ : « nouvelle congruence » sur les C4 induits | X | 2026-09-22 | conway99-involution:master:notes/AUDIT_2026-09-22.md:12-16 |
| L01-09 | Rangs F3 et invariants p-locaux (prop. F3) | P | 2026-09-22 | conway99-involution:master:report/dossier_chercheurs_fr.tex:269-289,427-429 |
| L01-10 | Découpage sib / one / dis exhaustif | E | 2026-09-21 | conway99-involution:master:notes/NOTE_involution_case.md:54-55 |
| L01-11 | SAT/CP-SAT génériques sur le modèle complet : tous UNKNOWN | S | 2026-09-22 | conway99-involution:master:results/BATCH_2026-09-21_overnight.md:1-19 |
| L01-12 | RETIRÉ : log one10 UNSAT (ne pas citer) | X | 2026-09-22 | conway99-involution:master:notes/ONE10_PROVENANCE.md:1-28 |
| L01-13 | Audit Reimbayev (recensement d'ordre 7) : 4 coquilles, rien sur n3 | E | 2026-09-21 | conway99-involution:master:notes/AUDIT_reimbayev_order7.md:16-36 |
| L01-14 | Borne externe sur n3 (dépôt public) | E | 2026-09-21 | conway99-involution:master:notes/RESEARCH_MEMORY.md:17-19 |
| L01-15 | Spectre du graphe extérieur H de tout graphe de Conway | P | 2026-09-22 | conway99-involution:master:notes/DEEP_THOUGHT_2026-09-22.md:15-20 |
| L01-16 | Décomposition Stage Q / Stage S | P | 2026-09-22 | conway99-involution:master:results/LAB_2026-09-22_summary.md:35-42,90-92 |
| L01-17 | Cubes de première ligne (U0) : comptes exacts | E | 2026-09-22 | conway99-involution:master:results/LAB_2026-09-22_summary.md:47-58,118-120 |
| L01-18 | Identité des triangles de Γ1 et relations mod 2 | P | 2026-09-22 | conway99-involution:master:results/LAB_2026-09-22_summary.md:59-62,96,123-125 |
| L01-19 | Contrôle fort BvLS : encodage CNF m = 11 validé | E | 2026-09-22 | conway99-involution:master:results/LAB_2026-09-22_summary.md:23-27 |
| L01-20 | Structure s = 1 / s = 0 (squelette de recherche) | P | 2026-09-22 | conway99-involution:master:notes/DEEP_THOUGHT_2026-09-22.md:22-30 |
| L01-21 | Programme décisif proposé : générateur ordonné / matrices d'orbites p = 2 | O | 2026-09-21 | conway99-involution:master:notes/NOTE_involution_case.md:61-67 |
| L01-22 | Théorème A (corrigé) : rank_F7(A − 3I) impair pour tout srg(99,14,1,2) | P | 2026-09-25 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:37-63 |
| L01-23 | Théorème B (involution) : rank_F7(S − 3I) pair ; parités 7-adiques | P | 2026-09-25 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:40-41,54-57,65-70,78-89 |
| L01-24 | Heuristique « 7 \| k » sur la famille srg(1+2m², 2m, 1, 2) | H | 2026-09-25 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:91-96 |
| L01-25 | Comptages de points fixes : impasse | P | 2026-09-25 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:72-76 |
| L01-26 | Théorème D : le cas « tous les carrés frères » est impossible | P | 2026-09-25 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:103-128,596,609-610 |
| L01-27 | Graphe N des paires non frères : tout N à au plus 6 arêtes exclu ; borne g(x) ≤ 14 | P | 2026-09-25 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:130-152,187-295,595-596,609 |
| L01-28 | Lemme 9.1 : grilles parfaites (sans involution) | P | 2026-09-25 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:153-160,568-569 |
| L01-29 | Théorème F : le modèle de Fano est impossible (lemme du coin, budget μ) | P | 2026-09-25 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:321-425,591-594 |
| L01-30 | Règle des zéros et Théorème P (configurations ancrées régulières, Paley) | P | 2026-09-25 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:426-537,588-590,610 |
| L01-31 | Théorème D′ : aucun sommet n'est plat (sans automorphisme) | P | 2026-09-25 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:543-567 |
| L01-32 | Plafond 7-adique et transposition de la méthode C3 : impasses | P | 2026-09-25 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:572-584,674-743 |
| L01-33 | Théorème 24.3 : aucune configuration ancrée n'existe (lemme de la queue) | P | 2026-09-25 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:745-807 |
| L01-34 | Tout-tordu pur entièrement exclu | C | 2026-09-26 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:838-949,989-991,1080-1092 |
| L01-35 | Famille H (= H-β) impossible : 552 certificats de Farkas exacts | C | 2026-09-26 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:971-1039,1059-1060 |
| L01-36 | M1 à bloc A : n = 3 et n = 4 impossibles (certificats) | C | 2026-09-26 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:1054-1078 |
| L01-37 | Niveau orbite : 25 survivants du PL par paires tués ; limites | C | 2026-09-26 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:1094-1116 |
| L01-38 | Triangle de bloc : comptages exacts ; configurations AD | P | 2026-09-26 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:1118-1139 |
| L01-39 | État du résidu C2 au 26/09 (fin du carnet) | O | 2026-09-26 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md:996-1000,1046-1052,1064-1069,1112-1116 |
| L01-40 | Fable : le « cœur » (μ_c = τ_c = π) équivaut au théorème ; aucune piste tuée à tort | P | 2026-09-27 | c2-compute:origin/claude/tender-archimedes-q532j1:scripts/fable/NOTE_core.md:21-124 |
| L01-41 | Fable : pas d'analogue d'ordre 2 de l'obstruction discriminante de C3 | P | 2026-09-28 | c2-compute:origin/claude/tender-archimedes-q532j1:scripts/fable/NOTE_arith.md:1-80 |
| L01-42 | c2-compute : paquet de calcul (PL + Farkas exacts) et campagnes | E | 2026-09-26 | c2-compute:main:README.md:1-24 |
| L01-43 | C7 : aucun automorphisme d'ordre 7 (preuve sans ordinateur, formalisée en Lean) | P | 2026-10-02 | conway-C7:main:README.md:1-41 |
| L01-44 | G1 : toute grille 3×3 d'un srg(99,14,1,2) est un code parfait | P | 2026-09-23 | conway99-c2-experimental:master:notes/04_GRILLES_ENSEMBLES_INTRIGANTS.md:1-10 |
| L01-45 | Parité du 7-rang (note 09) : rank7(A − 3I) impair, D7(N3) de type moins | P | 2026-09-23 | conway99-c2-experimental:master:SYNTHESE.md:23-29 |
| L01-46 | Lemme S1 (paire sœur = partition exacte, m = 7) et prismes / n3 | P | 2026-09-23 | conway99-c2-experimental:master:SYNTHESE.md:18-22 |
| L01-47 | Configurations interdites du graphe Σ des grilles par x (DRAT) | C | 2026-09-23 | conway99-c2-experimental:master:SYNTHESE.md:31-38 |
| L01-48 | Allsib impossible : preuve humaine par la cohomologie du complexe des couplages M7 | P | 2026-09-24 | conway99-c2-experimental:master:notes/17_ALLSIB_PREUVE_HUMAINE.md:1-8 |
| L01-49 | Lemme des étoiles : deg Σ ≤ 2, \|Σ\| ≤ 4, 10 survivants | C | 2026-09-24 | conway99-c2-experimental:master:SYNTHESE.md:107-125 |
| L01-50 | Réduction à l'étoile libre (conjecture équivalente à « pas de C2 ») | O | 2026-09-24 | conway99-c2-experimental:master:notes/20_ETOILE_LIBRE_IDEES.md:3-25 |
| L01-51 | Transfert du mécanisme C3 à C2 : vide (N09), niveau p = 2 vide (note 24) | R | 2026-09-23 | conway99-c2-experimental:master:SYNTHESE.md:43-45 |
| L01-52 | Résultats négatifs du labo (N01-N24) | R | 2026-09-23 | conway99-c2-experimental:master:NEGATIVE_RESULTS.md:1-171 |
| L01-53 | Diagnostic : tout ce qui a tué est une parité | H | 2026-09-24 | conway99-c2-experimental:master:notes/22_REVUE_COMPLETE.md:115-127,154-169 |
| L01-54 | q:parite (Burnside mod 2 à l'ordre 7) : aucune contradiction | E | 2026-09-24 | conway99-c2-experimental:master:notes/22_REVUE_COMPLETE.md:131-149 |
| L01-55 | Labo C2 du 25-26/09 : lemme d'équilibre, queue, M1, H-β, tout-tordu (voir carnet) | C | 2026-09-26 | git conway99-c2-experimental 7d5dbf8 … 7ddb193 (25-27/09) |
| L01-56 | TROU : « tout-tordu mort » ne couvre que les circuits simples | O | 2026-09-27 | conway99-c2-experimental:master:notes/45_FAMILLE_UN_BLOC_79_SYSTEMES_LOCAUX.md:117-158 |
| L01-57 | Famille « tout un bloc » (Σ = ∅) : 79 systèmes locaux ; 25/79 certifiés | C | 2026-09-27 | conway99-c2-experimental:master:notes/45_FAMILLE_UN_BLOC_79_SYSTEMES_LOCAUX.md:7-9,38-49,160-178 |
| L01-58 | Ligne d'arrivée (A)/(B) par instances I(τ) ; calibrage négatif | O | 2026-09-27 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/notes/46_LIGNE_D_ARRIVEE_C2.md:10-38,55-89,106-110 |
| L01-59 | Naissance de la route (C) : enveloppe unimodulaire de rang 24 et liste finie de Borcherds | P | 2026-09-27 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/notes/46_LIGNE_D_ARRIVEE_C2.md:90-115 |
| L01-60 | Route (C) au 27-29/09 : premières exclusions de réseaux | E | 2026-09-29 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/notes/46_LIGNE_D_ARRIVEE_C2.md:116-155 |
| L01-61 | Retour aux maths du 27/09 : bilan des solveurs | H | 2026-09-27 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/notes/47_RETOUR_AUX_MATHS_27_09.md:1-20,56-57 |
| L01-62 | Route rang 17 (V = Z^17, E8⊕Z^9, D12⁺⊕Z^5) — volet C2 | E | 2026-09-28 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/notes/52_RANG17_Z17_COUCHE_BINAIRE_27_09.md:1-8 |
| L01-63 | Modèle joint « graphe exact + témoin court » (28/09) : erratum k = 0 | O | 2026-09-28 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/notes/54_SOLO_MODELE_JOINT_TEMOIN_28_09.md:1-17,68,84 |
| L01-64 | Modèle exact (S) / L_N et cible EX (paquet researcher2) | P | 2026-09-30 | conway_c2_researcher2_start_2026_09_30:MODEL.md:1-101 |
| L01-65 | T4 : complétion réelle exacte (vide ou singleton intégral) | P | 2026-09-30 | conway_c2_researcher2_start_2026_09_30:MODEL.md:51-55 |
| L01-66 | F0 : statut (entrée séparée, non vérifiée par le relecteur de T4) | P | 2026-09-30 | conway_c2_researcher2_start_2026_09_30:provenance/REVIEWER_AUDIT_EXCERPT.txt:22-30 |
| L01-67 | Chercheur 2 (30/09-01/10) : R1-R21, EX reste OUVERT | O | 2026-10-01 | conway_c2_researcher2_start_2026_09_30:RESEARCH_HISTORY.md:3-4 |
| L01-68 | R3 : structure mod 2 de B pour tout N ∈ S | P | 2026-09-30 | conway_c2_researcher2_start_2026_09_30:work/RESULTS.md:43-67 |
| L01-69 | R4 : la famille « toutes cellules » (π = κ) est vide (= allsib) | P | 2026-09-30 | conway_c2_researcher2_start_2026_09_30:work/RESULTS.md:70-97 |
| L01-70 | R5 : obstruction locale 3\|4 ; R6-R7 : rigidité type 2 et classification des supports | P | 2026-09-30 | conway_c2_researcher2_start_2026_09_30:work/RESULTS.md:100-138 |
| L01-71 | R8 : passe SAT non signée sur les 133 classes (sans certificat) | S | 2026-09-30 | conway_c2_researcher2_start_2026_09_30:work/RESULTS.md:140-147 |
| L01-72 | R9-R11 : relèvement de signe linéaire mod 2 ; Théorème S ; note ternaire vérifiée | P | 2026-09-30 | conway_c2_researcher2_start_2026_09_30:work/RESULTS.md:150-192 |
| L01-73 | Note ternaire de l'agent 2 (30/09) : T1-T3 (non revue par le relecteur de T4) | P | 2026-09-30 | conway_c2_researcher2_start_2026_09_30:work/external/c2_agent2_exact_ternary_2026_09_30/THEOREMS.md:1-59 |
| L01-74 | R12-R13 : carrés de type 1 rigides (Théorème A) ; T1S faux au rayon un | P | 2026-10-01 | conway_c2_researcher2_start_2026_09_30:work/RESULTS.md:195-234 |
| L01-75 | R14-R15 : parité du 7-rang (P7) — redécouverte ; aucun mécanisme global à levier | P | 2026-10-01 | conway_c2_researcher2_start_2026_09_30:work/RESULTS.md:237-249 |
| L01-76 | R16 / Théorème C : forme couplée en (Q,N) — reformulation | P | 2026-10-01 | conway_c2_researcher2_start_2026_09_30:work/RESULTS.md:252-258 |
| L01-77 | R17-R18 : tables de chemins à quatre états ; recouvrements (BvLS : 165 K4 positifs) | P | 2026-10-01 | conway_c2_researcher2_start_2026_09_30:work/RESULTS.md:261-285 |
| L01-78 | Agents aveugles : Constructeur (symétries) et Destructeur (Hodge) | E | 2026-10-01 | conway_c2_researcher2_start_2026_09_30:work/agents/gen1_constructor/RESULTS_gen1_constructor.md:1-40 |
| L01-79 | Phase native et déterminabilité (01/10) | E | 2026-10-01 | conway_c2_researcher2_start_2026_09_30:RESEARCH_HISTORY.md:49-57 |
| L01-80 | R20-R21 : calcul de torsion à m = 7 et ressource du 3-espace impair | P | 2026-10-01 | conway_c2_researcher2_start_2026_09_30:work/RESULTS.md:294-344 |
| L01-81 | Loi d'énergie exacte des enveloppes : K + E(y1) + E(y2) = 3\|Φ\|/4 + 8 | P | 2026-10-02 | conway_c2_researcher2_start_2026_09_30:work/HANDOVER_2026-10-04.md:149-179 |
| L01-82 | Mécanisme de mort des recherches (011) : couverture exacte des points cible-1 | E | 2026-10-03 | conway_c2_researcher2_start_2026_09_30:work/CASCADE_STUDY_2026-10-03_cost.md:28-41 |
| L01-83 | Route (C) au 04/10 : 142/156 exclus, 14 ouverts | E | 2026-10-04 | conway_c2_researcher2_start_2026_09_30:work/HANDOVER_2026-10-04.md:115-143 |
| L01-84 | Audit « 156/156 » (04-07/10) : données des 156 réseaux recalculées ; erratum 150 ; T4 non utilisé | E | 2026-10-04 | conway_c2_researcher2_start_2026_09_30:work/AUDIT_156_PLAN_2026-10-04.md:96-123,158-170 |
| L01-85 | Énoncé final C2 (brouillon 7, 07/10) : aucune involution, sous conditions | P | 2026-10-07 | conway_c2_researcher2_start_2026_09_30:work/FINAL_STATEMENT_C2_DRAFT_2026-10-07.md:1-31,54-57,116-128 |
| L01-86 | Dossier de reconstruction (T0-T5) : catalogue des théorèmes de complétion | P | 2026-09-30 | conway99-c2-campaign:main:archive/FULL_DOSSIER.md:159-302 |
| L01-87 | Campagne C2 (01/10) : registre des affirmations et verdict OUVERT | O | 2026-10-01 | conway99-c2-campaign:main:STATUS.md:1-42 |
| L01-88 | Carte de réponse (response card) : non compressive (verdict B, explosion d'identités) | R | 2026-10-01 | conway99-c2-campaign:main:theorems/RESPONSE_CARD_CLOSURE.md:1-45 |
| L01-89 | Mémoire des échecs de la campagne (22 bassins) | R | 2026-10-01 | conway99-c2-campaign:main:research/FAILURE_MEMORY.md:5-28 |
| L01-90 | Solveur natif à quatre états (plan, non construit) | O | 2026-10-01 | conway99-c2-campaign:main:compute/NATIVE_SOLVER.md:1-45 |
| L01-91 | turbo-octo-waffle = copie zip de conway99-c2-campaign | E | 2026-10-01 | turbo-octo-waffle:main:conway99-c2-campaign.zip |
| L01-92 | S5 : critère 2-adique de non-existence de SRG (discriminant mod 4 des réseaux propres) | P | 2026-09-25 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_structures/NOTE_S5_DISCRIMINANT_MOD4.md:1-7,43-57 |
| L01-93 | Labo « structures » : relectures et exclusions pour C2 (registre S1-S30) | C | 2026-09-26 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_structures/REGISTRE.md:7-38 |
| L01-94 | S27 (q:7 en C2) : g⁻ ∈ {8,…,20} et 88 ≤ M ≤ 173 | P | 2026-09-26 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_structures/NOTE_S27_INVOLUTION_GENRE_7ADIQUE.md:1-35 |
| L01-95 | S25 : la famille srg(2m²+1, 2m, 1, 2) vue de 9 et 243 | P | 2026-09-26 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_structures/NOTE_S25_FAMILLE_9_243.md:1-16 |
| L01-96 | Astra dossier 6 : g⁻ = 8 et g⁻ = 10 exclus ; 18 et 20 ouverts (conditionnel) | P | 2026-09-26 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_structures/astra/RAPPORT_ASTRA_DOSSIER6.md:1-44 |
| L01-97 | Astra dossier 5 : boule tordue exclue à k = 22 ; famille cyclique exclue à k = 22 | P | 2026-09-26 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_structures/astra/RAPPORT_ASTRA_DOSSIER5.md:1-25,74 |
| L01-98 | C1 note 100 : les 21 lemmes de C1 ne peuvent pas se contredire | P | 2026-09-25 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_c1/notes/100_SYNTHESE_DES_LEMMES.md:1-5,191-203 |
| L01-99 | Bloc plein (NOTE_S29) et lemme de Witt général | P | 2026-09-27 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_structures/NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md:1-20,65,104 |
| L01-100 | Vérification du certificat géométrique d'Astra (25/09) | C | 2026-09-25 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_structures/NOTE_ASTRA_CERTIFICAT.md:1-36 |
| L01-101 | RETIRÉ : verdicts « h_found = false » de pair_h_check.py @ 96a94fe (bug d'empaquetage de bits) | X | 2026-09-27 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_runs/c1_96a94fe/INVALID_README.txt:1 |
| L01-102 | Théorèmes de coquille et enveloppe jumelle (29/09) | P | 2026-09-29 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_runs/shell_theorems/conway99_shell_theorems/README.md:1-21 |
| L01-103 | Contre-exemple fractionnaire exact (O24 et A2^8) | C | 2026-09-29 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_runs/fractional_proof/conway99_fractional_proof/PROOF.md:1-7,67 |
| L01-104 | Confinement des extrémités et points frontière (Y_z = 58) ; coupes résiduelles peu profondes | P | 2026-09-28 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_runs/flex_boundary/conway99_flex_boundary/README.md:1-60 |
| L01-105 | Squelette de preuve C2 auto-généré (01/10 19:49) : 93 exclus, 62 ouverts, 1 partiel | E | 2026-10-01 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/aws_repo/lemma/upstream/PROOF_SKELETON_C2.md:1-25 |
| L01-106 | Passation AWS 01-07/10 : clôture du tracker et article | E | 2026-10-07 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/aws_repo/HANDOFF_2026-10-01.md:97-101,975-1064 |
| L01-107 | Article « A strongly regular graph with parameters (99,14,1,2) has no automorphism of order two » (brouillon du 07/10) | P | 2026-10-07 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/aws_repo/lemma/PROOF_C2/paper/main.pdf (p. 1-2) |
| L01-108 | Astra/Sol 27/09 (0803) : réseau commun N_max de rang 22, det 49, et collage unimodulaire impair de rang 24 | P | 2026-09-27 | conway99-c2-experimental:master:external_inputs/CONWAY_ASTRA_27_09_2026_0836/EXTRAIT/attaque_globale_27_0803/BILAN_ATTAQUE_GLOBALE.md |
| L01-109 | Astra/Sol 27/09 (0836, 1031) : exclusions de familles d'enveloppes portant le repère | P | 2026-09-27 | conway99-c2-experimental:master:external_inputs/CONWAY_ASTRA_27_09_2026_0836/EXTRAIT/attaque_globale_27_0836/BILAN_AUDIT_INDEPENDANT_0836.md |
| L01-110 | Troisième vecteur de norme 7 : w = (h1 + … + h7)/2 ∈ N | P | 2026-09-27 | C:/home/researcher/Desktop/Recherche_Conway/c2_experimental/external_inputs/CONWAY_NOUVEAUTES_27_09_2026_1323/TROISIEME_VECTEUR_NORME7.md:1-4 |
| L01-111 | Sol : étoile A111111 (3,3) entièrement exclue ; coupure de norme 10 à cinq blocs | C | 2026-09-26 | conway99-c2-experimental:master:external_inputs/sol/files/outputs__fermeture_A33__RAPPORT.md:1-12 |
| L01-112 | Sol : une involution avec g⁻ = 16 force un prisme ; P = 0 ⇒ g⁻ ∈ {18, 20} | C | 2026-09-26 | conway99-c2-experimental:master:external_inputs/sol/DOSSIER_G16_PRISME.md:5-26 |
| L01-113 | Littérature téléchargée par le labo C2 (catalogue) | P | 2026-09-23 | conway99-c2-experimental:master:downloads/ |
| L01-114 | Mission « C2 sans calcul », résultat 1 : un vecteur d'énergie E ≤ 12 est forcé par les formes modulaires | P | 2026-10-13 | conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c2_elegant_2026-10-13/NOTE_MISSION_C2.md:20-57,98-104 |
| L01-115 | Mission C2, résultat 2 : identités exactes dans la « région » (après T16, T18, T20) | P | 2026-10-13 | conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c2_elegant_2026-10-13/NOTE_MISSION_C2.md:106-127 |
| L01-116 | Mission C2 : pistes négatives (un h dans l'indice ; vecteur caractéristique marqué) | R | 2026-10-13 | conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c2_elegant_2026-10-13/NOTE_MISSION_C2.md:148-185 |
| L01-117 | Rapport d'agent : petites fonctions propres σ-impaires 8 ≤ E ≤ 12 ; T22, T24 non prouvés | P | 2026-10-13 | conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c2_elegant_2026-10-13/LEMMAS_AGENT_REPORT.md:6-40 |
| L01-118 | Sondage E = 11 (k = e = 0) : une preuve par cas non rédigeable | H | 2026-10-14 | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/c2_elegant_2026-10-13/SOUNDING_E11.md:8-20 |
| L01-119 | Paires de la région : identités vérifiées ; la question de l'heptade | E | 2026-10-14 | conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c2_elegant_2026-10-13/region_pairs/REGION_PAIRS_REPORT.md:6-14,23-35 |
| L01-120 | Statistiques de mort des 156 réseaux (relevé du 13/10) | E | 2026-10-13 | conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c2_elegant_2026-10-13/KILL_STATISTICS_156.md:5-14 |
| L01-121 | Inventaire des campagnes C2 (13/10) : désaccords et retraits recensés | E | 2026-10-13 | conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c2_elegant_2026-10-13/INVENTORY_C2_CAMPAIGNS.md:1-30,239-254 |
| L01-122 | Article ordre 2 : audit avant consolidation (13/10) et Partie I rédigée | P | 2026-10-13 | conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c2_consolidation_2026-10-14/AUDIT_ORDER2_PAPER.md:13-20,83-110 |
| L01-123 | Audit v7 (12/10) : deux nouveaux srg(243,22,1,2) ; revêtements Z3 de Brouwer–Haemers : exactement quatre | E | 2026-10-12 | conway99-c1:origin/lab/exploration-2026-10-16:code/lab_audit_v7_2026-10-12/AUDIT_V7.md:1-28 |
| L01-124 | Mots binaires du noyau modulo 7 (C1, 12/10) | P | 2026-10-12 | conway99-c1:origin/claude/v7-simultaneous:code/code7_mots_binaires/THEOREME.md:1-26 |
| L01-125 | Données code/r6 (C1, programme R6/J1a, 28/09) | E | 2026-09-28 | conway99-c1:main:code/r6/j1av/ |

Répartition des statuts : P = 66, C = 13, E = 22, S = 2, H = 4, O = 9, R = 5, X = 4.

## 4. Routes fermées et pourquoi (par partie)

**A. Origines : dépôt conway99-involution (21-26/09)**
- SAT/CP-SAT génériques sur le modèle complet : 7 × 8 h, CP-SAT, ligne de U0 fixée, tous UNKNOWN ; « ni le découpage exhaustif de la première ligne ni la résolution générique ne sont à portée » (RESEARCH_MEMORY.md:40-43 ; NOTE:56-59).
- DFS ligne par ligne : arrêts au plafond de nœuds en 5-8 s (LAB_2026-09-22_summary.md:16).
- Recuit simulé (bit-flip et mouvements structurés) : plateau ≈ 1550-1650 (BATCH:16-17).
- Recensement d'ordre 7 (Reimbayev) : n'ajoute rien sur n3 (AUDIT_reimbayev:32-35).
- Énumérer D d'abord : ≈ 10^19 classes (DEEP_THOUGHT:34) [estimation, H].
- Relaxations LP/SDP de degré 2 : satisfaisables par des matrices réelles (DEEP_THOUGHT:33).
- Point de vue « 2-relèvement de Kneser » : aucune identité au-delà du Gram de Q (DEEP_THOUGHT:35).
- Cubes U0 Stage Q à 20 min : trop grossiers (HANDOFF:14).

**B. Carnet MATH_C2_PROGRAMME (25-26/09), c2-compute (26-28/09), conway-C7 (02/10)**
- Comptages de points fixes mod 2 (L01-25).
- Genre / réseaux / discriminant à la C3 pour C2 : tautologie (Théorème A), « famille genre/réseaux épuisée pour C2 » (MATH_C2_PROGRAMME.md:743) ; confirmé par Fable pour une raison structurelle (caractères rationnels de C2 ; 7 visible 2-adiquement) (NOTE_arith.md:42-50) ; forme quadratique binaire sur le code propre : close (NOTE_arith.md:52-57).
- Plafond 7-adique (k ≥ 29) par blocs locaux : impossible avec des blocs connus (MATH_C2_PROGRAMME.md:577-580).
- Réduction à des objets connus (ensembles intrigants, designs de cocliques de Hoffman, théorèmes min-max) : les réductions qui mordent exigent une sous-structure ; transport : Hall ne mord pas (slack 9 vs ≤ 7) (MATH_C2_PROGRAMME.md:639-672).
- Signe au premier ordre (relâchement linéaire) : ne suffit pas (l.993) ; niveau racine signé faisable ; système A-local signé faisable (l.1106-1111).
- Mélanges par un PL par squelette : 10^4-2·10^5 classes par classe, hors de portée (l.1112-1113) → abandon de la voie « familles » au profit de la route (C).
- Fable : solveurs par type sur le modèle complet, UNKNOWN ≥ 32 min ; arbres qui explosent dans les cinq premières orbites (README fable:20-22).

**C. Laboratoire expérimental C2 (conway99-c2-experimental et Desktop c2_experimental, 22-29/09)**
- Obstructions de genre / réseaux / discriminants / Brown / Arf pour C2 : vides (N09, N24, note 24) ; verdict relabellisé HEURISTIQUE par la revue (22_REVUE_COMPLETE.md:64,97).
- Relaxations de moments (degré 2 et 3) : réalisables à m = 7, même pour allsib ; Lasserre aveugle à la parité (N19, N20 ; revue:107).
- Solveurs bruts sur l'étoile libre (cubes RSF, cadical, CP-SAT, MILP, recuit) : UNKNOWN, « ne vaut rien » (revue:66) ; propagateur de Gauss au niveau des bits bruts insuffisant (revue:154-169).
- Gram tordu (PSD pour les 2 903 types), enveloppe affine, invariants linéaires, LP sur l'étoile libre : aucun type éliminé (revue:179-185).
- Mélanges par PL par squelette : trop gros ; filtre v6 avec Σ et grand T explose (note 43:100-101) ; tout-tordu non simple par PL d'orbite + coin : ne ferme pas (note 45:152-158).
- Ligne d'arrivée locale (A) : 32/32 cubes β inconnus, 77 838 cubes : suspendue (note 46:106-110).
- Mécanismes de caractérisation locale (Bondarenko–Radchenko, Hamming local, Makhnev 1988, Cameron 1975) : inapplicables (N15).

**D. Paquet et travail du chercheur 2 (conway99-c2-researcher2 = espace researcher2, 30/09-01/10) et notes du travail C2 de l'espace (01-07/10)**
- Recuit simulé non signé (F1) ; ansatz de symétrie supplémentaire (F2, abandonné ; puis constructeur : ~25 groupes exclus au niveau S, sans portée universelle) ; identités globales de trace/comptage (F3) ; SAT non signé sur supports clairsemés (F4) ; comptabilité globale des signes (F5, tautologique) ; revendications T1 et T1S (F6, F7, fausses) ; parité du 7-rang (F8, redécouverte) ; rondes d'objets 1 et 2 (F9, F10) ; Z[C2]-liberté (R19) ; Lefschetz/homologie (destructeur, redondant) (FAILED_ATTEMPTS.md:3-58 ; RESULTS.md).
- Réduction du coût de la route (C) : piège de norme 24, ILP de budget, déduplication, consistance de chemins, forward checking, borne cible-1 : sans gain (CASCADE_STUDY_2026-10-03_cost.md:43-55) ; filtres d'Astra, lp_cover, fail-first : gains marginaux (ROUTE_C_SPEEDUP_AUDIT.md:37-46).

**E. Archive de la campagne C2 (conway99-c2-campaign, 01/10) et turbo-octo-waffle**
voir L01-89 (22 bassins) et L01-88 (carte de réponse).

**F. Labo « structures » et notes C1 copiés dans Desktop c2_experimental (25-27/09)**
- « Aucune combinaison des 21 lemmes de C1 ne peut donner de contradiction » (C1 note 100 §4) : la route « combiner les lemmes existants » est fermée par une proposition de cohérence.
- Triplets de droites (C1 note 99) : rien au-delà de L16.
- PPE signé seul (S13) et (P2) en relâchement McCormick (S14) : pas de certificat linéaire / effet entier non testé.

**G. Desktop c2_experimental : passes externes, AWS, article (28/09-07/10)**
- Obstruction convexe universelle (« boxed » fractional frame) : faisable dans O24 et A2^8 (L01-103).
- Filtres d'empreinte d'Astra dans la boucle chaude : −0 à −36 % de nœuds mais perte de temps (astra_shallow README:11).
- Couche Azure : mise de côté le 01/10, rien poussé (azure_layer_wip/LISEZMOI.md:1-4).

**H. Dossiers externes Sol/Astra et littérature (conway99-c2-experimental external_inputs/, downloads/ ; Desktop CONWAY_NOUVEAUTES)**
- Le genre seul : un contre-modèle Golay explicite (rang 22, det 49, min 3, indécomposable, sans racines, min dual ≥ 10/7) satisfait toutes les propriétés globales ; « le repère prescrit de 42 racines et 7 blocs reste le problème » (BILAN_ATTAQUE_GLOBALE §4-§5).
- « Dernière attaque accélérée » (tournois signés, appariements de caractéristiques lourdes) : aucune exclusion globale (NOUVEAUTES LIRE_D_ABORD).

**I. Mission « C2 sans calcul » (13-14/10), consolidation de l'ordre 2, audit v7, code7, données r6**
- Forcer une contradiction avec les seuls T16, T18, T20 : FAUX (espace de dimension 7 avec tables positives ; milliers de paires réelles avec min E ≥ 11) (NOTE_MISSION:59-69).
- Un h de l'heptade dans l'indice (seconds moments) : PL faisable (NOTE_MISSION:148-164) ; vecteur caractéristique marqué : reformulation du piège (166-175).
- Preuve par cas lisible de E = 11 : ~5·10^7 bases, non rédigeable (SOUNDING_E11).
- Route Z3 pour srg(243) : fermée (THEOREM_Z3_COVERS, corollaire).

## 5. Questions ouvertes, classées par levier (synthèse ; listes détaillées par partie en §7)

- **Preuve de C2 sans calcul** : lemmes T22, T24 (E = 11, 12 ; 23 et 168 graphes d'orbites résiduels) ; raison uniforme de l'absence d'heptade dans les paires de région ; exclusion à la main des fonctions propres « caractéristiques » ; explication structurelle de la couverture exacte des points cible-1 ; obstruction de réseau pour les enveloppes pauvres en racines (analogue C7 : 42 vecteurs dans R^15) ; versions à la main des certificats H-β (second ordre) (L01-114, L01-117, L01-119, L01-82, L01-35).
- **Certification de l'exclusion calculée** : recertification des transferts (4 163 099 paires) ; seconde implémentation du packing ; complétude des énumérations de paires au-delà de 4 réseaux ; seconde lecture du moteur ; records du PC labo non archivés ; preuves LRAT des certificats du 23-24/09 jamais archivées ; formalisation Lean (conditionnelle) (L01-122, L01-85, L01-47).
- **Familles (voie abandonnée, subsumée par la route C)** : tout-tordu non simple ; carrés disjoints ((2,0) contre (2,1), lemme 11.2 exact) ; mélanges à plusieurs cycles tordus ; Σ ≠ ∅ (M1 entièrement certifié le 27/09 : ce n'est plus une question) ; AD n_dd > 4 ; lemme de l'étoile libre (forme locale) ; « cocycle à défauts » (L01-56, L01-39, L01-50, L01-53).
- **Arithmétique 7-adique** : seconde détermination de r mod 2 ou du signe k ; types de D+ et D− ; « accidents » isotropes à k = 28 ; forme de Smith 7-adique de S − 3I ; codes LCD [42,20] et MacWilliams (L01-23, L01-32, L01-41, L01-21).
- **Constructif (EX positif)** : solveur natif à quatre états ; grammaire constructive ; rigidité de signe (R) ; générateur ordonné / matrices d'orbites p = 2 (L01-90, L01-72, L01-21).
- **Vers C1 / général** : plafond de torsion P ≥ 1152 ; k ≤ 28 uniforme ; λ = 1, μ = 2 force-t-il la platitude ; parité de |Σ| (ordre 9) ; existence d'un mot binaire de ker7(A + 4I) ; unicité de srg(243,22,1,2) (L01-31, L01-98, L01-97, L01-54, L01-124, L01-95).
- **Littérature et sources** : vérifier dans les articles eux-mêmes les énoncés attribués à Makhnev–Minakova et Behbahani–Lam (HANDOFF §20) ; antériorité du cas p = 2 (q:ant).

**Détails par partie**

*A. Origines : dépôt conway99-involution (21-26/09)*
- Calcul certifiable : matrices d'orbites Stage Q (q:orbit) ; générateur ordonné (q:gen) ; cubes avec DRAT (q:cube) ; test A/B modèle complet vs Stage Q sur les 9 cubes sib ; cubes de profondeur 2 ; banc d'encodages ; estimation de Knuth (HANDOFF:25-41).
- Preuve à la main : exclure le cas sœur (q:cas) ; congruences par comptage d'orbites contre les recensements (q:parite) ; contenu 7-adique de S − 3I et Q − 3I (q:7) ; codes LCD [42,20] et MacWilliams (q:code) ; identité trace-rang « réseau libre Z2[C2] » à la Ishida (q:ishida) ; antériorité du cas p = 2 (q:ant) (dossier_chercheurs_fr.tex:410-445).

*B. Carnet MATH_C2_PROGRAMME (25-26/09), c2-compute (26-28/09), conway-C7 (02/10)*
- Combinatoire : carrés disjoints (lemme 11.2, valeur exacte de φ_u(R)) ; mélanges à plusieurs cycles tordus ; M1 n = 5, 6 ; Σ ≠ ∅ ; AD n_dd > 4 (L01-39).
- Arithmétique : seconde détermination indépendante de r mod 2 ou du signe 7-adique k (MATH_C2_PROGRAMME.md:70) ; types 7-adiques individuels de D+ et D− (NOTE_arith.md:59-78) ; « accidents 7-adiques » isotropes (l.581-584).
- Global : montrer que λ = 1, μ = 2 force la platitude en un sommet ou mesurer le défaut global (l.560-561) ; lemme de l'étoile libre forme locale (NOTE_core.md:119-121).

*C. Laboratoire expérimental C2 (conway99-c2-experimental et Desktop c2_experimental, 22-29/09)*
- Parité : « cocycle à défauts » (étendre la cohomologie de la note 17 aux carrés one/dis) ; parité rendue linéaire au niveau χ ; parité de |Σ| (exigerait l'ordre 9) (revue §2, §5).
- Combinatoire : lemme de l'étoile libre forme locale (note 20) ; tout-tordu non simple (note 45 §8) ; (2,0) contre (2,1) pour un partenaire dis (note 41 §4) ; les 54 types durs des 79 (note 45 §9) ; famille tout-dis (B) (note 46 §6).
- Réseaux : route (C) (lot L02 pour la suite) ; rang 17 (lot L09).
- Vérification : archiver les preuves LRAT des certificats critiques (revue:47, 76) ; rédiger le lemme des étoiles au niveau ÉTABLI (revue:59).

*D. Paquet et travail du chercheur 2 (conway99-c2-researcher2 = espace researcher2, 30/09-01/10) et notes du travail C2 de l'espace (01-07/10)*
- EX lui-même (aucun témoin ; non-EX démontré seulement via la route (C), lot L02).
- Obligation (R) de rigidité de signe (OBLIGATION_RIGIDITY.md) ; signe au rayon ≥ 2 pour la ligne type 1 (R13) ; placement des supports de doublement (R21(f)).
- Route (C) sans calcul : couverture exacte cible-1 structurelle ; obstruction de réseau pour les enveloppes pauvres en racines ; analogue C7 « 42 vecteurs dans R^15 » (HANDOVER:225-232).
- Audit 156/156 : L4 (complétude des paires), L5 (seconde lecture différée), champs « reviewed_by » (AUDIT_156_PLAN:56-81).

*E. Archive de la campagne C2 (conway99-c2-campaign, 01/10) et turbo-octo-waffle*
P = EX ; solveur natif (L01-90) ; réconcilier 91/156 avec le registre canonique (ROADMAP:19).

*F. Labo « structures » et notes C1 copiés dans Desktop c2_experimental (25-27/09)*
- Plafond de torsion (C1) ; k ≤ 28 uniforme (Astra 5) ; g⁻ = 18 et 20 (Astra 6, avant la route C) ; existence d'un Q_c inversible (condition d'Astra 6) ; bloc plein (problème fini autonome pour Sol) ; unicité de srg(243,22,1,2) (littérature).

*G. Desktop c2_experimental : passes externes, AWS, article (28/09-07/10)*
- Points ouverts de l'article au 07/10 : auteur, réseau 044 (second passage), seconde implémentation du packing (Codex), attributions Makhnev–Minakova et Behbahani–Lam à vérifier, G2 de T20, arbitrage de Codex sur main.tex, appendices et MANIFEST (HANDOFF_2026-10-01.md:1025-1044).
- Formalisation Lean (théorème conditionnel, A.0, Corollaire Y1, 143) ; preuve sans ordinateur (optionnelle) (HANDOFF:1007-1012).

*H. Dossiers externes Sol/Astra et littérature (conway99-c2-experimental external_inputs/, downloads/ ; Desktop CONWAY_NOUVEAUTES)*
- Avant la route (C) : fermeture globale de g⁻ = 18 et 20 ; régimes 0/2/4 fractionnaires de D6^4 ; enveloppes sans racines ; normes 9/10 à six et sept blocs (LIRE_D_ABORD_POUR_CLAUDE ; CAMPAGNES_A33 table). Ces questions sont ensuite absorbées par la route (C) (156 réseaux).

*I. Mission « C2 sans calcul » (13-14/10), consolidation de l'ordre 2, audit v7, code7, données r6*
- T22 et T24 (E = 11, 12) : 23 et 168 graphes d'orbites (k = e = 0) + 3 resp. 5 autres (k,e) (LEMMAS_AGENT_REPORT §0).
- Pourquoi l'heptade manque dans les réseaux de la région ; distribution jointe des sept produits (indice J + H+) (NOTE_MISSION:163-185).
- Article d'ordre 2 : recertification des transferts (item B), seconde implémentation, lemmes dans le texte (AUDIT_ORDER2_PAPER §3-§4).

## 6. Contradictions, redécouvertes, résultats remplacés ou retirés (synthèse ; détails par partie en §7)

**Contradictions et désaccords (qui, quand)**
- Théorème A (7-rang) : carnet v1 « e′ pair » (25/09) contre labo note 09 « rank7(A − 3I) impair » (23/09) ; carnet corrigé le 25/09 après l'audit d'Astra (MATH_C2_PROGRAMME.md:38-39,605-607).
- Tout-tordu : « entièrement exclu » (carnet §32, 26/09 ; la ligne 1092 n'a jamais été corrigée) contre le trou des circuits non simples (note 45 §8, 27/09) ; jamais fermé, remplacé par la route (C) (INVENTORY_C2_CAMPAIGNS §6 item 6).
- Compte de la route (C) le 01/10 : 91/156 (campagne, « campaign-reported »), 93/156 (squelette 19:49), 94/156 (import du labo le soir) — désynchronisation reconnue par les sources.
- Statut de T4 : « AUDITED-IN-CAMPAIGN » (campagne, 01/10) contre « WORKING-ASSUMPTION » (HANDOVER 04/10, MODEL.md) ; la chaîne finale ne l'utilise pas (FINAL_STATEMENT:16).
- Portée de S1 : « exactement m = 7 » (SYNTHESE, note 17) contre « m ∈ {2,7} » (revue note 22).
- C4 dans Σ : UNSAT à l'étage Q non signé (chercheur 2, solveur, 30/09) contre SAT pour les systèmes des lignes sœurs (labo, 24/09) — relaxations différentes, piste non tranchée.
- Makhnev–Minakova : « Théorème 1 lu verbatim » (RESEARCH_MEMORY, 21/09) contre « attributions prises dans des résumés, someone must open the two papers » (HANDOFF §20, 07/10) ; Ishida « recovers a1(t) = 14 » (NOTE, 21/09) contre « not confirmed by the abstract » (AUDIT_156_PLAN, 04/10).
- Table de Borcherds (C1) : étiquettes des voisins de 150 fausses ; données justes (AUDIT_156_PLAN:112-118).
- Annexe D (lecture de C1, 24/09) : verdicts « TUÉE » trop larges, errata E1-E3 du 27/09 (F20, forme SRG, OUVERTE).

**Redécouvertes (même résultat établi plusieurs fois)**
- Allsib impossible : labo note 17 (24/09, cohomologie) ; carnet Théorème D (25/09, Kneser signé) ; chercheur 2 R4 (30/09, mécanisme identique) ; destructeur R4 (01/10, variante).
- Parité du 7-rang : labo note 09 (23/09) ; L2 de C1 ; carnet Théorème A corrigé (25/09) et §23 (refait « sans savoir que ce labo existait ») ; Fable NOTE_arith (28/09) ; chercheur 2 R14 (01/10).
- Grilles = codes parfaits : labo G1 (23/09, Wilbrink–Brouwer) ; carnet lemme 9.1 (25/09) ; L5/L6 de C1.
- Pas de sommet plat (carnet D′, 25/09) = cas particulier de L8 de C1.
- Rang F2 = 20 (21/09) = R3 du chercheur 2 (30/09) ; R9 = note 19 §12 ; R17(c) = note 39 ; R20 ≈ carnet §8, §14, §19, §24, §32.
- Hodge (destructeur, 01/10) = C1 note 60.
- (1/2)Σh ∈ U : Sol (27/09, « troisième vecteur de norme 7 ») = Lemme Z de la route (C) = re-dérivé le 13/10 (mission).
- Transposition de la méthode C3 à C2, vide : labo N09 (23/09), carnet §23 (25/09), Fable (28/09).
- Comptes de lignes 155 904 (one) / 22 176 (sib) : agent phase 2 (22/09, non vérifié) puis phase native du chercheur 2 (01/10).

**Remplacés ou retirés (cause)**
- Congruence c4 (vide), « rang 20 information nouvelle » (conséquence du modèle), Smith de Q − 3I sur Z3 (non prouvée), « 3 solutions » à k = 4 (1 seule), log one10 UNSAT (sous-cas vide) — audit du 22/09.
- n3 ≡ 0 (mod 6) faux → n3/3 ≡ n_one (mod 2) ; z11 ≡ 0 (mod 8) faux sauf n_one pair ; « 53 graphes / ≤ 7 grilles » → 10 survivants, |Σ| ≤ 4 — revue du 24/09.
- Théorème A v1 (25/09) ; lemmes 8.2-8.4 retirés le jour même puis rétablis en GT2 ; lemme 11.2 affaibli (= 2 → ≥ 2, 26/09) ; « critère général » tautologique (25/09).
- Verdicts « h_found = false » de pair_h_check @ 96a94fe (bug d'empaquetage, 27/09) ; note 51 « tuées par le lemme Z (99,8 %) » fausse ; erratum k = 0 (note 54).
- Revendication T1S du chercheur 2 (fausse au rayon un, 01/10).
- Astra : M_shadow = 4I + R faux, corrigé ; interdiction par demi-intégralité retirée (27/09).
- Familles du labo et carnet : remplacées par la route (C) (27/09) ; g ∈ {18,20} remplacé par le Théorème R qui ne l'utilise plus (07/10) ; manifeste RERUN_713 du portable « SUPERSEDED » (07/10).
- Incidents sans verdict faux : crash v1/v2 des sommes d'étoiles jointes (02/10) ; 118 paires INCOMPLETE du moteur v2 passées inaperçues puis résolues (02/10) ; Γ de 025 corrigé (29/09).

**Détails par partie**

*A. Origines : dépôt conway99-involution (21-26/09)*
/ REDÉCOUVERTES / RETRAITS
- Retraits du 22/09 (audit) : congruence c4 vide (L01-08) ; « rang 20 information supplémentaire » (L01-07) ; trivialité de Smith pour Q − 3I sur Z3 (L01-09) ; « 3 solutions » au contrôle k = 4 → 1 solution ; log one10 UNSAT (L01-12). Corrections du labo à l'audit : les sorties « non archivées » n'ont pour la plupart jamais existé ; RESEARCH_MEMORY:36-37 surestime les durées (AUDIT_2026-09-22.md:83-86).
- Pas de contradiction réelle : |Stab(U0)| = 15 360 (dans 2^7⋊S7) vs 7 680 (dans 2^6⋊S7) — facteur σ.
- Crédit : flip = lemme de Makhnev ; a1(t) = 14 déjà dans Makhnev–Minakova ; réduction enracinée classique (Cesarz–Woldar 2023, Keramatipour 2026, Thakkar–Severini 2026) ; nouveau : D et le modèle exact (AUDIT_2026-09-22.md:26-29).
- Lien en aval : les comptes de lignes admissibles 22 176 (sib) / 155 904 (one) d'un agent phase 2 (non vérifiés, LAB summary:15) réapparaissent dans le paquet researcher2 comme « exact admissible-row counts 930336 / 155904 / 22176 » (RESEARCH_HISTORY.md:50) : confirmation indépendante probable (dates 22/09 et 01/10).

*B. Carnet MATH_C2_PROGRAMME (25-26/09), c2-compute (26-28/09), conway-C7 (02/10)*
/ REDÉCOUVERTES / RETRAITS
- Théorème A : version initiale fausse (« e′ pair »), corrigée le 25/09 après l'audit d'Astra ; B, GT, F, P, D non touchés (MATH_C2_PROGRAMME.md:605-607).
- Lemme 11.2 : « φ_u(R) = 2 » retiré, seul « ≥ 2 » prouvé (26/09, 77a7b8d) ; usages valides.
- « Critère général det(Λθ) = 1 + f/v mod 4 » : reconnu tautologique (e13193a, 25/09 18:28).
- Redécouvertes : Théorème D′ = cas particulier de L8 de C1 (25/09) ; parités 7-adiques de Fable (28/09) = notes 09, 10, 21 du labo (23-25/09) ; Théorème A corrigé = L2 de C1.
- Lien : |Σ| ≤ 4, deg Σ ≤ 2 (« certifiés », labo notes/19 §9) sont utilisés par Fable : à confirmer dans la partie D (labo).

*C. Laboratoire expérimental C2 (conway99-c2-experimental et Desktop c2_experimental, 22-29/09)*
/ REDÉCOUVERTES / RETRAITS
- RETRAIT : « n3 ≡ 0 (mod 6) » (note 08) faux, remplacé par n3/3 ≡ n_one (mod 2) (note 20 §1) ; « z11 ≡ 0 (mod 8) » du relecteur D faux sauf n_one pair (revue:27-28).
- RETRAIT : « 53 graphes / ≤ 7 grilles par x » périmé, remplacé par 10 survivants, |Σ| ≤ 4 (SYNTHESE:36-37).
- CORRECTIONS de la revue du 24/09 : note 21 J1 = erreur (doublon de G1) ; note 13 « coin colinéaire ⇒ dis » douteux, R2 à retirer, relèvement H(7,3) spéculation ; note 19 plusieurs surestimations (revue §3).
- CORRECTION du 27/09 (annexe D, version Desktop, errata E1-E3) : les verdicts « TUÉE » de F2/F2′/F20 (C1) étaient trop larges : seules les formes locales sont tuées (témoins de diamètre 3) ; F20 (forme SRG) OUVERTE.
- CORRECTION : « tout-tordu pur entièrement exclu » (carnet §32, 26/09) → seulement pour les circuits simples (trou trouvé le 27/09, note 45 §8).
- RÉSERVE : de nombreuses morts « au niveau paires » (M1 n = 5, 6, mélanges) sans certificats stockés au 26/09 (note 41 §2-§3) ; refaites avec certificats pour M1 (note 44:109-114).
- RÉSERVE : aucune preuve DRAT/LRAT archivée pour les certificats du 23-24/09 (revue:46-48).
- REDÉCOUVERTES : G1 (labo 23/09) = lemme 9.1 du carnet (25/09) = L5/L6 de C1 ; parité du 7-rang (labo 23/09) = Théorème A du carnet (25/09, d'abord faux) = L2 de C1 = Fable (28/09) ; allsib impossible deux fois (cohomologie, labo 24/09 ; Kneser signé, carnet 25/09) ; note 24 : « refaite au §23 du carnet principal sans savoir que ce labo existait ».
- ERRATUM note 54 : exclusion de k = 0 incorrecte telle qu'écrite, puis rétablie pour n = 5, 6, 7.
- ERREUR note 51 : « tuées ensuite par le lemme Z (99,8 %) » FAUX (aucune exclusion touchée).

*D. Paquet et travail du chercheur 2 (conway99-c2-researcher2 = espace researcher2, 30/09-01/10) et notes du travail C2 de l'espace (01-07/10)*
/ REDÉCOUVERTES / RETRAITS
- Redécouvertes déclarées : R1-R4, G0, E′, R9 (DUPLICATION_CHECK, 30/09) ; R14 (= note 10 du labo) ; R17(c) (= note 39) ; R10(b) (= C1 note 149) ; R20 (= carnet §8, §14, §19, §24, §32). R4 est la troisième exclusion d'allsib (24/09 labo ; 25/09 carnet ; 30/09 chercheur 2), avec les mêmes rangs δ0 = 20, δ1 = 85.
- Divergence de solveurs à vérifier : C4 UNSAT à l'étage Q non signé (chercheur 2, 0,2 s, sans certificat) contre C4 SAT pour les systèmes des lignes sœurs dans le labo (UNSAT seulement au modèle complet, DRAT) (DUPLICATION_CHECK.md:29-32).
- T4 : le paquet le présente comme pont de EX ; l'audit du 04/10 corrige : la route (C) n'en dépend pas (AUDIT_156_PLAN:158-166) ; le brouillon final confirme (« T4 of MODEL.md and the reconstruction direction are not used », FINAL_STATEMENT:16).
- Erratum de table : réseau 150, étiquettes de voisins de la table de C1 fausses, données justes (AUDIT_156_PLAN:112-118).
- Incident moteur : crash v1/v2 dans les sommes d'étoiles jointes (un job sur ~900) ; aucun réseau exclu par une telle paire (addendum_v5:5-17). Γ de 025 corrigé le 29/09 (|Γ| = 8, était l'identité) (ROUTE_C_SPEEDUP_AUDIT.md:26).
- Le HANDOVER du 04/10 cite min N* ≥ 8/7 (AUDIT_NORME1) et l'entrée g ∈ {18,20} ; le brouillon final du 07/10 dit que g n'est plus utilisé (A.4) : remplacement, non contradiction.

*E. Archive de la campagne C2 (conway99-c2-campaign, 01/10) et turbo-octo-waffle*
/ REDÉCOUVERTES
- Hodge (destructeur du chercheur 2, 01/10) = C1 note 60 (« REDISCOVERY ; ALREADY CLOSED IN C1 NOTE 60 », STATUS.md:22).
- Compte de la route (C) : 91/156 (campagne, « campaign-reported ») contre 94/156 dans le registre du labo le même soir (ROUTE_C_RESUME_STATUS:65) : écart de synchronisation, signalé par la source elle-même.
- Statut de T4 : « WRITTEN DERIVATION — REVIEW REQUIRED » dans le dossier (30/09) ; « AUDITED-IN-CAMPAIGN » au 01/10 ; jamais « FORMALLY-VERIFIED ».

*F. Labo « structures » et notes C1 copiés dans Desktop c2_experimental (25-27/09)*
/ REDÉCOUVERTES
- S12 précise notes/116 de C1 : la diagonale vaut 16 − 2e(R) ; « 16 » exige e(R) = 0, que la torsion maximale ne garantit pas (correction de C1 d02ac18) (REGISTRE:21).
- S20 : « le Fano tendu meurt au niveau cellules (notes/116 à corriger par C1) » (REGISTRE:28).
- Valeurs ouvertes de g⁻ successives : {8,…,20} (S27) → 8, 10 exclus (Astra 6) → {12,…,20} (Sol) → {16,18,20} → {18,20} (C1 notes/132, S28) : raffinements successifs, pas de contradiction.

*G. Desktop c2_experimental : passes externes, AWS, article (28/09-07/10)*
/ RETRAITS
- RETIRÉ : verdicts de pair_h_check @ 96a94fe (L01-101) ; la note 46 §9 (27/09) citait « 15/15 paires mortes chez C1 » sur 132 par cette voie.
- INCIDENT : 118 paires INCOMPLETE non signalées par tick.sh (seulement à l'import) ; résolues EXCLUDED par v8 (handoff_v8_final.md:2-6).
- Réfutation de stratégie : relaxation convexe « boxed » faisable (L01-103).
- Le brouillon de l'article (07/10) mentionne des attributions (Makhnev–Minakova, Behbahani–Lam) prises dans des résumés et sources secondaires, « someone must open the two papers » (HANDOFF:1031-1035) ; pourtant le dépôt involution (21/09) disait avoir lu le Théorème 1 de Makhnev–Minakova verbatim (RESEARCH_MEMORY:22-24) : divergence d'état de vérification entre sessions.

*H. Dossiers externes Sol/Astra et littérature (conway99-c2-experimental external_inputs/, downloads/ ; Desktop CONWAY_NOUVEAUTES)*
/ RETRAITS
- Corrections internes d'Astra : M_shadow = 4I + R FAUX (contre-exemple E8 ⊥ U16), corrigé en (4 + r/4)I − 2R ; interdiction par demi-intégralité RETIRÉE (BILAN_AUDIT_INDEPENDANT_0836 « Limites » ; BILAN_1031 « Corrections »).
- Parité de Sol « m(u) pair » : vraie mais coupe vide (fait de réseau, aucun m impair dans les 156 histogrammes) (Desktop notes/46:123-125).
- Le partiel D6^4 de Sol (au moins 3 blocs entiers) « n'est pas audité » côté labo le 27/09 (notes/46:127) alors que le dossier 1031 s'appuie sur un « bilan indépendant » interne : audit interne à la session externe, non par le labo.

*I. Mission « C2 sans calcul » (13-14/10), consolidation de l'ordre 2, audit v7, code7, données r6*
/ REDÉCOUVERTES / RETRAITS
- Les désaccords recensés par l'inventaire (L01-121) recoupent ceux de cette fiche ; il signale en plus : lemmes 8.2-8.4 retirés le jour même puis rétablis en GT2 ; ligne 1092 du carnet toujours affirmative sur le tout-tordu ; S1 « propre à m = 7 » contre « m ∈ {2,7} » ; ambiguïté de formulation de T20_PROOF.md.
- Redécouverte probable : « (1/2) Σ h_c ∈ U » re-dérivé le 13/10 (NOTE_MISSION:74) = troisième vecteur de norme 7 de Sol (27/09, L01-110) = Lemme Z de la route (C).
- Erreurs corrigées en route (mission) : règle d'ombre avec θ4(τ) au lieu de θ4(2τ) ; lecture « forme nulle » sur rang flottant (NOTE_MISSION:89-92) ; comptage en paires ±a (correction de 20:49).

## 7. Notes lues et non lues ; chronologies détaillées

Comptes sur les 766 contenus distincts du lot (une copie identique comptée avec son original ; classement par `readstat`) :
- lu intégralement : 94 ;
- survolé (titres, énoncés, statuts, passages porteurs ; ou copie comparée par diff) : 291 ;
- agrégé (logs, listes de tâches, données numériques, empreintes) : 269 ;
- catalogué (littérature externe téléchargée, non résumée) : 23 ;
- non lu : 89, dont 69 fichiers de bibliothèques tierces (`c2_experimental/.venv/…/site-packages` : scipy, setuptools, networkx, pymupdf, joblib, jinja2, highspy, cffi, numba, cvxpy…), 6 PDF compilés de sources lues, 5 recueils géants des dossiers Astra (résumés par leurs bilans), 2 états de reprise de 80 Ko, 4 prompts/modes d'emploi/questions sans résultat, 1 passation de job, 1 source LaTeX (décrite par sa note) et sa copie.

Non lus, avec la raison (hors bibliothèques tierces) :
- 0012 : non lu (PDF compilé de report/conway99_involution_report.tex (lu))
- 0014 : non lu (PDF compilé de report/involution_notes_fr.tex)
- 0034 : non lu (PDF compilé de report/dossier_chercheurs_fr.tex)
- 0232 : non lu (état de reprise NOUVEAUTES (82 Ko), en-tête seulement)
- 0255 : non lu (recueil de programmes et sorties (896 Ko) ; conclusions prises dans les bilans)
- 0264 : non lu (recueil complet (320 Ko) ; conclusions prises dans le bilan 0803)
- 0277 : non lu (recueil de preuves (140 Ko) ; énoncés pris dans le bilan 0803)
- 0293 : non lu (instantané d'état de reprise (79 Ko))
- 0304 : non lu (recueil de preuves (381 Ko) ; énoncés pris dans le bilan 0836)
- 0369 : non lu (questions envoyées à Astra (suivi 3))
- 0370 : non lu (questions envoyées à Astra (suivi 4))
- 0372 : non lu (passation d'un job nuage (bloc plein))
- 0459 : non lu (état de reprise (80 Ko), en-tête seulement)
- 0566 : non lu (mode d'emploi du moniteur AWS)
- 0568 : non lu (prompt pour Astra (sans résultat propre))
- 0589 : non lu (source LaTeX (54 Ko) décrite par PART1_NOTES (lu))
- 0653 : non lu (PDF compilé de order2_lemma16_partA.tex)
- 0654 : non lu (PDF compilé de order2_part1.tex)
- 0713 : non lu (PDF compilé de tex/order7.tex)
- 0765 : non lu (copie identique de 0589)

### 7.A A. Origines : dépôt conway99-involution (21-26/09)

Notes traitées :

| index | source | date | lecture | contenu |
|---|---|---|---|---|
| 0004 | conway99-involution:master:README.md (+ origin/master) | 21-25/09 | lu intégralement | état du dépôt, table de statuts, corrections du 22/09 |
| 0005 | conway99-involution:origin/math-c2-programme:README.md | 22/09 | comparé (diff) | version sans les deux lignes de statut du labo (CNF m = 11 « pending ») |
| 0006 | conway99-involution:master:notes/AUDIT_reimbayev_order7.md (11 copies) | 21/09 | lu intégralement | audit du recensement d'ordre 7 de Reimbayev |
| 0007, 0020 | conway99-involution:master:notes/NOTE_involution_case.md ; copie Desktop | 21/09 (rév. 22/09) | lu intégralement ; copie Desktop identique (CRLF) | note fondatrice : réduction exacte, D, modèle, rang F2 |
| 0008, 0021 | notes/RESEARCH_MEMORY.md ; copie Desktop | 21/09 | lu intégralement ; Desktop identique | mémoire de session historique (bandeau : l'audit l'emporte) |
| 0009, 0022 | notes/SOURCES.md ; copie Desktop | 21/09 | lu intégralement | liste des sources primaires |
| 0010, 0023 | notes/WHAT_WOULD_HELP.md ; copie Desktop | 21/09 | lu intégralement | documents, outils, vérifications humaines demandés |
| 0011 | report/Dockerfile.tex | 21/09 | lu | image texbox, sans contenu mathématique |
| 0012, 0014, 0034 | report/*.pdf | 21-22/09 | non lus : versions compilées des .tex lus |
| 0013, 0024 | report/conway99_involution_report.tex ; Desktop | 21-22/09 | survolé (rapport court anglais, même contenu que NOTE + corrections) ; Desktop identique |
| 0015, 0026 | report/involution_notes_fr.tex ; Desktop | 21-22/09 | survolé (notes pédagogiques, mêmes corrections) |
| 0025, 0035 | report/dossier_chercheurs_fr.tex (rév. 2) ; Desktop | 22/09 | survolé structuré ; lus : remarques de statut, prop. F3, rem. c4, anomalies, questions q:gen…q:ant |
| 0016 | results/BATCH_2026-09-21_overnight.md | 22/09 | lu intégralement | 7 × 8 h UNKNOWN |
| 0017, 0018 | LAB_INSTRUCTIONS.md ; Desktop | 22/09 | survolé (règles §0b, §4) ; Desktop identique |
| 0028, 0029, 0019 | notes/AUDIT_2026-09-22.md (master avec §D labo ; math-c2-programme et Desktop sans §D) | 22/09 | lu intégralement + diff |
| 0030 | notes/BRIEFING_phase2.md | 22/09 | lu intégralement | consigne des agents « phase 2 » |
| 0031 | notes/DEEP_THOUGHT_2026-09-22.md | 22/09 | lu intégralement | spectre de H, dichotomie s=1/s=0, impasses |
| 0032, 0033, 0253 | notes/ONE10_PROVENANCE.md (master avec complément labo ; autres sans) | 22/09 | lu intégralement + diff |
| 0250 | code/z2/phase2/s1_structure/counts.txt | 25/09 (commit) | lu | comptes des couplages M_c |
| 0251 | code/z2/phase2/spectral_orderly/sound_m11.txt | 25/09 | agrégé (log JSON) | sondage d'un générateur spectral sur m = 11, 0 violation |
| 0252 | Desktop conway99-involution/README.md | 25/09 | comparé | = version math-c2-programme |
| 0337 | results/HANDOFF_2026-09-22.md | 22/09 (commit 25/09) | lu intégralement | passation du labo |
| 0338 | results/LAB_2026-09-22_summary.md | 22/09 (commit 25/09) | lu intégralement | session labo : contrôles, Stage Q, cubes |
| 0339-0343 | results/lab_2026-09-22/{control4_mem_samples, cubes_dis, cubes_one, cubes_sib, cuberes_sib}.txt | 22/09 | agrégés (logs) | échantillons mémoire ; listes de cubes (units) ; résultat « sib 1 UNKNOWN 1200 s » |

Chronologie :

| date | événement | source |
|---|---|---|
| 2026-09-21 16:51 UTC | ouverture de la session d'origine eeaf2d22 (transcription citée) | conway99-involution:master:notes/ONE10_PROVENANCE.md:20 |
| 2026-09-21 18:50 → 22/09 02:58 | lot de nuit, 7 instances × 8 h : toutes UNKNOWN | conway99-involution:master:results/BATCH_2026-09-21_overnight.md:1-14 |
| 2026-09-21 19:00 | premier commit bf0443f (Dilan Djematene) : réduction, rang F2, audit ordre 7, premiers calculs | git log conway99-involution |
| 2026-09-21 20:09-20:11 | preuve élémentaire du rang F2 (b749559), multiplicités de S par tr S = −7 (c2ded92, 4b2eb49) | git log |
| 2026-09-21 20:17-20:33 | notes tierces C3 ajoutées (7626438, 5b771ca) ; supprimées le 22/09 (récupérables en 9eb634d) | git log ; AUDIT_2026-09-22.md:62 |
| 2026-09-22 12:52 | dossier externe en français + note ONE10 (9eb634d) | git log |
| 2026-09-22 20:40 | audit 8b4ba9a : corrections (c4, rang 20, F3(iv)), contrôle BvLS, instructions labo ; base de la branche math-c2-programme | git log ; AUDIT_2026-09-22.md |
| 2026-09-22 soir (21:10-23:38) | session labo : contrôles OK, CNF m = 11 validé, Stage Q 2 h ×6 UNKNOWN, cubes U0 (1 326), arrêt à la demande de l'opérateur | LAB_2026-09-22_summary.md ; HANDOFF_2026-09-22.md |
| 2026-09-25 10:08 → 26/09 17:00 | carnet MATH_C2_PROGRAMME (branche math-c2-programme, §1-§34) | git log (voir partie B) |
| 2026-09-25 13:33 | e3f14c2 : fichiers du labo 22/09 et phase 2 enfin commités sur master | git log |

### 7.B B. Carnet MATH_C2_PROGRAMME (25-26/09), c2-compute (26-28/09), conway-C7 (02/10)

Notes traitées :

| index | source | date | lecture | contenu |
|---|---|---|---|---|
| 0336 | conway99-involution:origin/math-c2-programme:notes/MATH_C2_PROGRAMME.md (1 139 lignes) | 25-26/09 | survolé structuré complet : §0-§7 lus intégralement, §8-§21 énoncés en gras et statuts, §20-21, statut de relecture et audit Astra lus, §28-§34 lus intégralement ; preuves de §8-§19, §22, §25-§27 non relues ligne à ligne | carnet central de la branche C2 « sans solveur » puis « solveurs en petits tests » |
| 0375 | Desktop conway99-involution/notes/MATH_C2_PROGRAMME.md | 26/09 | comparé : identique à 0336 (CRLF) |
| 0373 | Desktop c2_experimental/external_structures/logs/c2_programme.md | 26/09 18:01 (mtime) | comparé : version antérieure (§0-§24 seulement), sans la ligne de politique solveur ni la correction du lemme 11.2 |
| 0344 | c2-compute:main:README.md | 26/09 | lu |
| 0419-0421 | c2-compute:main:scripts/{c1,structures,structures_ad}/README.md | 26/09 | lus | provenance des scripts copiés (C1 8bbc335-37842fc ; structures 8bd9fcf, e6484e3, 477c3dd) |
| 0509 | c2-compute:origin/claude/tender-archimedes-q532j1:scripts/fable/NOTE_core.md | 27/09 | lu intégralement |
| 0510 | …/scripts/fable/README.md | 27/09 | lu |
| 0511 | …/scripts/fable/replay_bvls.txt | 27/09 | agrégé (données : structure de blocs de BvLS rejouée) |
| 0549 | …/scripts/fable/NOTE_arith.md | 28/09 | lu intégralement |
| 0382-0397, 0467-0486 | c2-compute:main:logs/cloud_tasks_*.txt (fx1, or1, or2, s1a-d, test10, rtA, rtB, tier06, tier6a-d, tier8e2a/b ; copies claude/new-session-02xwfv) | 26-27/09 | agrégés : listes de tâches (type, fichier, budget), sans verdict |
| 0704 | conway-C7:main:README.md | 02/10 | lu intégralement |
| 0711 | conway-C7:main:checks/README.md | 02/10 | lu |
| 0712 | conway-C7:main:lean/README.md | 02/10 | lu intégralement ; + lean/logs/axioms.log et comparator.log (hors inventaire) |
| 0713 | conway-C7:main:order7.pdf | 02/10 | non lu : version compilée de tex/order7.tex |
| 0714 | conway-C7:main:tex/order7.tex | 02/10 | survolé (structure des énoncés : thm:main, lemmes, prop:zerodiag, thm:six) |

Chronologie :

| date | événement | source |
|---|---|---|
| 2026-09-25 10:08 | création du carnet « programme strictement mathématique » (fc0eb23), consigne opérateur : aucun solveur | git log conway99-involution |
| 2026-09-25 11:16-13:33 | cas mixte : tout graphe N non frère à ≤ 6 arêtes exclu ; lemme du coin ; budget μ, Fano exclu ; règle des zéros ; identité de bloc ; Paley impossible ; arrêt de la piste configurations, Théorème D′ ; crédit L8 de C1 | aac0db5 … 3e0507e |
| 2026-09-25 14:39-16:22 | relectures externes : Théorème P vérifié en entier, Théorème F vérifié ; audit adverse d'Astra : Théorème A faux (e′ pair) corrigé en e′ impair | b56e836, 755ec94, fc175b2, 394760d |
| 2026-09-25 17:40-18:28 | transposition de la méthode C3 : cohérente, sans contradiction ; « critère général » reconnu tautologique ; crédit N09 du labo | 2a801ea, fc395c6, 69a03f7, e13193a |
| 2026-09-25 18:49 | lemme de la queue : aucune configuration ancrée (vérifié par structures + relecture interne) | 6c5d850 |
| 2026-09-25 20:15-22:32 | tout-tordu pur : orbite morte, exclusions à la main (≥ 3 triangles) ; mélanges M1 ; H réduit à H-β | 13d31ae … 0fed809 |
| 2026-09-26 05:06-09:27 | H impossible (552 certificats) ; M1 n = 3, n = 4 impossibles ; tout-tordu pur entièrement exclu (14/14 contre-vérifiés) | c5cad6a … 0779509 |
| 2026-09-26 10:58 | correction du lemme 11.2 (φ ≥ 2 seulement) | 77a7b8d |
| 2026-09-26 14:52-17:00 | niveau orbite : 25 survivants tués ; mélanges hors de portée ; triangle de bloc ; AD | b4fde2a, a121d14 |
| 2026-09-26 21:50 → 27/09 05:44 | c2-compute : paquet de calcul nuage (PL/Farkas, tâches C1, structures, AD, tiers SAT) | git log c2-compute |
| 2026-09-27 16:33 → 28/09 13:53 | session « Fable » : modèle indépendant, 3 308 classes de types de blocs (= C1), NOTE_core, NOTE_arith | git log c2-compute (805661e … 61a2022) |
| 2026-10-02 08:45-13:55 | conway-C7 : preuve sans ordinateur de l'ordre 7 et formalisation Lean complète | git log conway-C7 |

### 7.C C. Laboratoire expérimental C2 (conway99-c2-experimental et Desktop c2_experimental, 22-29/09)

Notes traitées :

| index | source | date | lecture | contenu |
|---|---|---|---|---|
| 0099 | notes/00_CARTE_ETAT_C2.md | 23/09 | survolé (en-tête, étiquettes) | carte de l'état reconstruite depuis les dépôts en lecture seule |
| 0100 | notes/01_CARTE_METHODES.md | 23/09 | survolé | méthodes déjà essayées et angles morts |
| 0101-0105 | notes/02 (Z7/D7/boule de Hamming), 03 (lemme S1), 04 (G1), 05 (allsib), 07 (défauts des carrés D) | 23/09 | survolés (énoncés et statuts) ; 04 lu en tête (antériorité Wilbrink–Brouwer) |
| 0106-0111, 0227 | notes/external_bridges/B01-B07 | 23-24/09 | survolés (source + verdict) | ponts : codes parfaits (prometteur), p-rangs (réfuté), Krein (heuristique 7), réseaux/trames (objet nouveau sans contrainte), star complements, ensembles intrigants (a produit G1), Akiyama/Niemeier (défavorable) |
| 0112 | IDEES.md | 24/09 | survolé (titres I-01…I-26) |
| 0113 | JOURNAL.md | 23-25/09 | survolé (titres de phases) ; lus : l.1-8, 306-340 (reprise du 25/09, incident de réinitialisation, notes 24-27) |
| 0114 | NEGATIVE_RESULTS.md | 23-25/09 | survolé (N01-N24, en-têtes et verdicts) |
| 0115 | README.md | 24/09 | lu (état au 24/09) |
| 0116 | REPRISE.md | 24/09 | survolé (titres ; mentions PÉRIMÉ) |
| 0117 | SYNTHESE.md | 23-25/09 | lu intégralement |
| 0155, 0228 | docker/README.md ; requirements-lab.txt | 24/09 | survolés (environnement) |
| 0207-0221 | notes/06, 08-21 | 23-24/09 | survolés (en-têtes, énoncés, statuts) ; 20 lu (§0-§2) |
| 0222 | notes/22_REVUE_COMPLETE.md | 24/09 | lu intégralement |
| 0223-0225 | notes/22_annexes/A, B, C | 24/09 | survolés (recherche d'erreurs signalées : aucune ligne marquée) |
| 0226, 0451 | notes/22_annexes/D_revue_branche_C1.md (git) ; version Desktop | 24/09 ; 27/09 | survolé + diff : la version Desktop ajoute des errata du 27/09 (E1-E3) |
| 0327-0335 | notes/23-31 | 24-25/09 | survolés (en-têtes, statuts) ; 24 lu en tête (redécouverte déclarée) |
| 0406-0418 | notes/32-44 | 26/09 | survolés (en-têtes, statuts, lignes de résultats) ; 41 lu intégralement ; 43, 44 extraits |
| 0507 | notes/45_FAMILLE_UN_BLOC_79_SYSTEMES_LOCAUX.md | 27/09 | lu (§1, §8, §9) |
| 0508, 0452 | notes/46_LIGNE_D_ARRIVEE_C2.md (git, 8,4 Ko) ; version Desktop (11,5 Ko) | 27/09 | version Desktop lue intégralement (contient §9) |
| 0453-0458 | Desktop notes/47-52 | 27/09 | survolés (en-têtes, lignes de résultats) |
| 0530-0532 | Desktop notes/53-55 | 28/09 | survolés |
| 0567, 0569 | notes/56_PROMPT_ASTRA_ROUTE_C_28_09.md (Desktop ; git route_c_29_09/) | 28-29/09 | survolé (titres) |
| 0568 | Desktop notes/57_PROMPT_ASTRA_MICROSCOPE_29_09.md | 29/09 | non lu (prompt pour Astra ; le contenu de résultats est dans 56 et route_c README) |
| 0570 | route_c_29_09/README.md | 29/09 | lu intégralement |
| 0422, 0512 | scripts/vendor_structures/README.md ; scripts/structures/LEMMA_SCOPES.md | 26-27/09 | survolés (provenance ; portée des lemmes des modèles locaux) |
| 0079, 0144-0154, 0229 | data/cert_list.txt, data/cert_results.txt (+ copie Desktop), data/cnf/MANIFEST*.txt, survivors39, survivors_after19 | 23-25/09 | agrégés : verdicts DRAT « VERIFIED » et empreintes ; survivors_after19 lu |
| 0027, 0092-0098, 0167-0206 | logs/*.txt du 22-24/09 (wslconfig, powercfg, keep_awake, snapshots en lecture seule, brown_twist, milgram_check, chi_*, rsf_*, schi_*, sigma_survivors_v2, sos*, star_lemma_check, r2_*, parity_classify, gridfree, ishida_modules, mem_watchdog, docker_*) | 22-24/09 | agrégés : sorties de contrôle et de solveurs des notes 06-21 ; snapshots = empreintes de lecture seule |
| 0140-0143, 0247-0249 | Desktop data/tmp, logs/freestar_* , fsos_* | 24-25/09 | agrégés : étoile libre (ansatz, LP, parité, SOS) : UNKNOWN |
| 0326 | logs/far_spectrum_exact_all.txt (3,2 Mo) | 25/09 | agrégé : tests spectraux du graphe lointain (note 23 : 2 903 types, négatifs) |
| 0377-0405, 0461-0506 | logs/ad2_tail_survivors, cloud_tasks_*, fixcamp_*, hb_cert_W_23_0, orbit_tasks1, pairfast_*, sigma_tasks, c1_g18_unknown_so_far, decl_list_fast25, docker_tasks_tier8, explore_list_*, lane_ids_*, root_tasks_9, rung1_list, stage2_tasks | 26-27/09 | agrégés : listes de tâches et d'identifiants des campagnes ; hb_cert : squelette circulant H-β et son certificat |
| 0374, 0434-0450, 0513-0527 | Desktop logs/orbit_tasks2, decl_export*, docker_tasks_*, export_all, hstage_budget, local_sat_*, o24_lp_excluded/feasible/todo_47, produce2_budget, root_tasks_1417*, rung1_export ; data/joint/classes_summary ; data/r0/jobs_*.txt | 26-28/09 | agrégés : O24 : listes des classes exclues par PL / faisables ; jobs E8 du rang 17 |

Chronologie :

| date | événement | source |
|---|---|---|
| 2026-09-23 | ouverture du labo isolé (lecture seule des dépôts involution et lab-archive) ; G1, S1, Z7/Hamming, prismes ; phase 3 certification (Docker autorisé 21:15) ; N09 (transfert C3 vide), note 09 (rang 7 impair) | JOURNAL.md:7-87 ; SYNTHESE.md |
| 2026-09-24 07:27 | sauvegarde complète du labo (85df20d) ; « reset » : notes 11-14 (t réflexion ponctuelle, Hall) | git log |
| 2026-09-24 16:34-21:48 | notes 15-19 (R2, moments, allsib à la main, système χ, lemme des étoiles : 10 survivants) ; note 20 (étoile libre) ; revue complète note 22 ; q:parite sans contradiction | ef1ff6d, 05889dd, d7a52e3, 4722c76, 16e593a |
| 2026-09-24 22:19-25/09 03:02 | propagateur de Gauss (sain, insuffisant) ; nuit de recherche (note 23 : décomposition κ, lemme d'équilibre) | 178bd74, d7fd35d, d10c8da, f17dd30, 46fb916 |
| 2026-09-25 après-midi | reprise par la session principale C2 (régime sans solveur) ; incident (réinitialisation du dépôt, fichiers restaurés) ; note 24 (p = 2 vide) | JOURNAL.md:306-315 ; f79a754 |
| 2026-09-25 18:48-23:14 | notes 25-31 : queue (aucune ancrée), M1, H = H-β, système niveau paires | 7d5dbf8 … ef0ec00 |
| 2026-09-26 | notes 32-44 : H-β mort (552), M1 n = 3, 4, contre-vérifications, niveau orbite, inventaire « pas d'involution » (note 41), AD2, M1 n = 6 fermé, motifs Σ ancrés morts, A33 mort (Sol), g⁻ = 16 impossible (C1) | 57ea5fe … 6fed2da |
| 2026-09-27 01:56 | M1 n = 5 fermé : M1 entièrement certifié | 7ddb193 |
| 2026-09-27 matin | note 45 : 79 systèmes locaux, trou du tout-tordu non simple ; 25/79 certifiés (09:17) ; note 46 : ligne d'arrivée I(τ), bris d'égalité, puis (C) enveloppes (11:41) ; dossier Sol/Astra 0836 importé (11:35) ; tracker 9/156 (11:59) | 966a79f … 3b7278d |
| 2026-09-27 12:40 | calibrage final des cubes β : 32/32 inconnus : (C) devient la voie principale | 0f622d7 |
| 2026-09-27 16 h-soir | note 47 « retour aux maths » ; 48-51 ; 87 exclu ; sweep-first | Desktop notes 47-51 |
| 2026-09-27 20:47 | Γ = Aut(U)/W(R) pour 46 enveloppes | 89592e2 |
| 2026-09-28 | rang 17 (52-53) ; modèle joint (54) ; R8 k = 3 (55) ; 47/156 exclus à 21:30 | Desktop notes 52-56 |
| 2026-09-29 08:44 | état de la route (C) pour Astra : 58/156 | 609cc3b ; route_c_29_09/README.md |

### 7.D D. Paquet et travail du chercheur 2 (conway99-c2-researcher2 = espace researcher2, 30/09-01/10) et notes du travail C2 de l'espace (01-07/10)

Notes traitées :

| index | source | date | lecture | contenu |
|---|---|---|---|---|
| 0571 | AUDIT_STATUS.md | 30/09 | lu intégralement | ce que la relecture indépendante établit (T4) et ses limites (F0, pas de Lean) |
| 0572 | CLAUDE.md | 30/09 | lu intégralement | consignes « existence, pas un nouvel audit » |
| 0573 | DUPLICATION_NOTES.md | 30/09 | lu intégralement | sept avertissements de duplication |
| 0574 | README.md | 30/09 | lu intégralement | paquet de départ |
| 0575, 0664 | RESEARCH_HISTORY.md (fs ; git) | 01/10 | lu intégralement ; versions identiques (CRLF) |
| 0576 | TASK.md | 30/09 | lu intégralement |
| 0601 | data/INPUT_FORMAT.md | 30/09 | survolé |
| 0602 | provenance/REVIEWER_AUDIT_EXCERPT.txt | 30/09 | lu intégralement |
| 0603 | reference/ERRATA.md | 30/09 | lu intégralement |
| 0604 | reference/GRAPH_RECONSTRUCTION.md | 30/09 | survolé (reconstruction (N,D) → 99 sommets) |
| 0605 | reference/PROOF_CURRENT.md | 30/09 | survolé (preuve consolidée de T4 ; énoncés seulement) |
| 0606 | requirements.txt | 30/09 | lu (numpy) |
| 0607 | work/DUPLICATION_CHECK.md | 30/09 | lu intégralement |
| 0608 | work/FAILED_ATTEMPTS.md | 01/10 | survolé (F1-F10) |
| 0609 | work/FAILURE_MEMORY.md | 01/10 | survolé (table des bassins fermés) |
| 0610 | work/GLOBAL_MECHANISM_SCAN.md | 01/10 | survolé (résumé R15) |
| 0611, 0623 | work/JOINT_CHECKPOINT_1.md ; RECONCILIATION_2.md | 30/09-01/10 | survolés (résumé R10, reclassement) |
| 0612 | work/LATTICE_PARITY_P7.md | 01/10 | survolé (R14) |
| 0613 | work/LEMMA_H.md | 30/09 | survolé (R6) |
| 0614 | work/LITERATURE.md | 30/09 | survolé |
| 0615, 0616, 0621 | work/OBJECT_ROUND_1.md, OBJECT_ROUND_2.md, R2_OMEGA1_USEFULNESS.md | 01/10 | survolés (R16, R17) |
| 0617 | work/OBLIGATION_RIGIDITY.md | 30/09 | survolé (obligation (R), ouverte) |
| 0618, 0619 | work/ONE_CANDIDATE_T1.md, ONE_CANDIDATE_T1S.md | 01/10 | survolés (R12, R13) |
| 0620 | work/OVERLAP_EXPLORATION.md | 01/10 | survolé (R18) |
| 0622 | work/README.md | 30/09 | lu |
| 0624 | work/RESULTS.md | 01/10 | lu intégralement (R1-R21) |
| 0625 | work/ROUTE_C_RESUME_STATUS.md | 01/10 | lu intégralement |
| 0626 | work/SAT_PASS_1.md | 30/09 | survolé (R8) |
| 0627 | work/STARTING_POINT.md | 30/09 | survolé |
| 0628 | work/STRATEGY_MAP.md | 01/10 | lu (§1-§3) |
| 0629 | work/TERNARY_VERIFICATION.md | 30/09 | survolé (R11) |
| 0630 | work/THEOREM_C.md | 01/10 | survolé (gelé, reformulation) |
| 0631-0635 | work/agents/PROVENANCE_LOG.md ; gen1_constructor/{RESULTS, STARTING_NOTE} ; gen1_destroyer/{RESULTS, STARTING_NOTE} | 01/10 | RESULTS constructeur lu (A1-A2) ; destructeur survolé ; les autres survolés |
| 0637-0640 | work/external/c2_agent2_exact_ternary_2026_09_30/{AGENT2_PROMPT, README, RESEARCH_RECORD, THEOREMS} | 30/09 | THEOREMS lu intégralement ; les trois autres survolés |
| 0641-0643 | work/native/{BASIN_ALERTS, B_DETERMINACY, NATIVE_REPRESENTATIONS} | 01/10 | survolés |
| 0644, 0645 | work/twist/ODD_EIGENSPACE_RESOURCE.md, TWIST_CALCULUS.md | 01/10 | survolés (résumés R20, R21) |
| 0657-0660, 0700-0703 | work/twist/t00, t02, t03, t04_output.txt (fs ; git) | 01/10 | lus (sorties courtes des contrôles) |
| 0636, 0693-0699 | work/data/{c12_microscope_bvls_mixed, c08_defect_squares, c09_c10_apex_hole, c11_burnside_counts, classify_XHJ_v1, classify_XH_v1, classify_X_v1, core_analysis_pass1}.txt | 30/09-01/10 | agrégés : sorties des checks c08-c12 et des classifications (201 387 → 185 028/185 049 survivants, 132/133 classes ; 1 741 726 → 793 349 ; 73 cœurs) |
| 0691 | work/CHECKPOINT.md | 01/10 | survolé |
| 0692 | work/Z_C2_FREENESS_REDUNDANCY.md | 01/10 | survolé (R19) |
| 0646 | work/AUDIT_156_PLAN_2026-10-04.md | 04-07/10 | lu (L0-L6 et journaux du 04/10) ; journal du 07/10 survolé |
| 0647 | work/CASCADE_STUDY_2026-10-02.md | 02/10 | survolé (titres M1-M6, P1, H1-H2) |
| 0648 | work/CASCADE_STUDY_2026-10-03_cost.md | 03/10 | lu intégralement |
| 0649 | work/HANDOVER_2026-10-04.md (+ copie) | 04/10 | lu intégralement |
| 0650 | work/ROUTE_C_SPEEDUPS_2026-10-01.md | 01-02/10 | survolé (FD_SYM2, FD_TWINCANON, FD_SYM3, pistes 3-4) |
| 0651 | work/ROUTE_C_SPEEDUPS_2026-10-02_addendum_v5.md | 02/10 | survolé (crash v1/v2, v5-v7, cascade 132/156) |
| 0652 | work/ROUTE_C_SPEEDUP_AUDIT.md | 01/10 | survolé (sections A-H) |
| hors lot (L02), lus pour le contexte | MODEL.md ; work/FINAL_STATEMENT_C2_DRAFT_2026-10-07.md (lu intégralement) ; work/VERIF_CUBE_OBSTRUCTION_2026-10-04.md (survolé) ; work/chatgpt_wagner_2026-10-04/LIRE_DOSSIER_WAGNER.txt (lu) ; work/t20_hand/NOTES.md (en-tête) | 30/09-07/10 | voir lot L02 pour le détail |

Chronologie :

| date | événement | source |
|---|---|---|
| 2026-09-30 | paquet researcher2 (MODEL, TASK, AUDIT_STATUS, DUPLICATION_NOTES, reference/, provenance/) ; note ternaire de l'agent 2 ; STARTING_POINT ; R1-R11 ; DUPLICATION_CHECK (R1-R4, G0, E′, R9 = redécouvertes) | RESEARCH_HISTORY.md:11-23 |
| 2026-10-01 (nuit-journée) | R12-R21 ; Théorème C gelé ; agents Constructeur/Destructeur ; phase native ; Z[C2] ; torsion ; STRATEGY_MAP (recommande la route C comme registre maître) | RESEARCH_HISTORY.md:25-80 ; commits e12bc31 … 706c268 |
| 2026-10-01 19:48-21:27 | reprise de la route (C) : import de 399 résultats AWS (94/156), lancement local arrêté, file adaptative AWS construite (plafond 115 $) | ROUTE_C_RESUME_STATUS.md:54-100 ; commit 7c0758f |
| 2026-10-01/02 | accélérations FD_SYM2/SYM3, règle jumelle canonique, crash v1/v2 dans les sommes d'étoiles jointes (sans verdict faux), paquets v5-v7, cascade : 132/156 (02/10 ~14:50) | ROUTE_C_SPEEDUPS_2026-10-01.md ; addendum_v5:5-17,116 |
| 2026-10-02/03 | microscope de la cascade 052 ; loi K + E ; étude du coût (011) | CASCADE_STUDY_* |
| 2026-10-04 10:30 | passation : 142/156 exclus, 14 ouverts | HANDOVER_2026-10-04.md:117-143 |
| 2026-10-04 15:30-16:00 | audit 156/156 : données des réseaux recalculées (erratum 150) ; F0 SOURCE-ONLY ; route (C) indépendante de T4 | AUDIT_156_PLAN:96-170 |
| 2026-10-07 17:47 UTC | tracker 156/156 (après acceptation de T18 et T20 par l'utilisateur) ; brouillon 7 de l'énoncé final | FINAL_STATEMENT_C2_DRAFT_2026-10-07.md:1-6 (lot L02) |

### 7.E E. Archive de la campagne C2 (conway99-c2-campaign, 01/10) et turbo-octo-waffle

Notes traitées :

| index | source | date | lecture | contenu |
|---|---|---|---|---|
| 0661 | CONTRIBUTING.md | 01/10 | survolé |
| 0662 | README.md | 01/10 | lu intégralement |
| 0663 | REPOSITORY_MAP.md | 01/10 | survolé |
| 0665 | ROADMAP.md | 01/10 | lu intégralement |
| 0666 | STATUS.md | 01/10 | lu intégralement |
| 0667 | TIMELINE.md | 01/10 | lu intégralement |
| 0668 | archive/FULL_DOSSIER.md (2 513 lignes, 138 Ko) | 30/09-01/10 | survolé structuré : orientation (l.36-90) et catalogue des théorèmes (l.159-302) lus ; preuves (parties 4-5 et suivantes) non relues ligne à ligne (même contenu que reference/PROOF_CURRENT et GRAPH_RECONSTRUCTION du paquet researcher2) |
| 0577 | archive/TERNARY_PROOF.md (7 copies, dont l'espace researcher2) | 30/09 | survolé (titres §0-§9) ; énoncés via THEOREMS.md de l'agent 2 |
| 0669 | archive/RESPONSE_CARD_RAW.md | 01/10 | survolé (verdict, §1) |
| 0674 | compute/NATIVE_SOLVER.md | 01/10 | lu |
| 0675 | compute/ROUTE_C.md | 01/10 | lu |
| 0676 | docs/NATIVE_MODEL.md | 01/10 | survolé |
| 0677-0681 | prompts/{CONSTRUCTOR, COORDINATOR, DESTROYER, PARADIGM_BREAK, REPRESENTATION_INVENTOR_NATIVE}.md | 01/10 | survolés (rôles d'agents, sans résultat) |
| 0682 | provenance/SOURCES.md | 01/10 | survolé |
| 0683 | provenance/STATUS_LABELS.md | 01/10 | lu intégralement |
| 0684 | research/AGENT_CAMPAIGN.md | 01/10 | survolé |
| 0685 | research/FAILURE_MEMORY.md | 01/10 | lu (table) |
| 0686 | research/REPRESENTATION_EXPERIMENTS.md | 01/10 | survolé |
| 0687-0690 | theorems/{RESPONSE_CARD_CLOSURE, T4_RECONSTRUCTION, TERNARY_CAPACITY, THEOREM_C}.md | 01/10 | lus (énoncés) |
| — | turbo-octo-waffle:main:conway99-c2-campaign.zip | 01/10 | vérifié : copie exacte (30 fichiers, mêmes blobs) |

Chronologie :

| date | événement | source |
|---|---|---|
| 2026-09-30 | consolidation de T4 ; relecture aveugle indépendante rapportée ; formulation ternaire/capacités ; une famille de relèvement ternaire exclue (non exhaustive) | TIMELINE.md:7-12 |
| 2026-10-01 | Théorème C gelé ; rondes d'objets ; graphe pont et appariements de coordonnées fermés ; carte de réponse non compressive ; Constructeur/Destructeur (bassins d'attraction) ; stratégie réduite à trois voies (inventeur conceptuel, route C, solveur natif) | TIMELINE.md:14-25 |
| 2026-10-01 15:27 | upload du zip turbo-octo-waffle | git log turbo-octo-waffle |

### 7.F F. Labo « structures » et notes C1 copiés dans Desktop c2_experimental (25-27/09)

Notes traitées :

| index | source | date | lecture | contenu |
|---|---|---|---|---|
| 0345 | external_structures/JOURNAL.md (75 Ko) | 25-27/09 | survolé structuré (titres de jour ; lus : bilan « où en est C2 » l.793-816 et nuit du 26-27/09 l.817-840) |
| 0359 | external_structures/REGISTRE.md | 25-27/09 | lu (table S1-S30) |
| 0346 | NOTE_ASTRA_CERTIFICAT.md | 25/09 | lu (en-tête et vérifications) |
| 0347-0358 | NOTE_S5, S8, S11, S12, S17, S21, S23, S24, S25, S26, S27, S28 | 25-26/09 | survolés (en-têtes, verdicts, lignes clés) ; S5, S25, S27 lus en partie |
| 0432 | NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md | 27/09 | survolé |
| 0360, 0361 | ad/HANDOFF_AD_SWEEP.md, ad/README.md | 26/09 | survolés (balayage AD confié au nuage de C2) |
| 0362-0370, 0433 | astra/{DOSSIER6_INVOLUTION_7ADIQUE, PROBLEMES_OUVERTS_INVOLUTION, RAPPORT_ASTRA_DOSSIER5, RAPPORT_ASTRA_DOSSIER5_SUITE, RAPPORT_ASTRA_DOSSIER6, RAPPORT_SOL_SUPPORTS_COURTS, RAPPORT_SOL_WAGNER, SUIVI3_DOSSIER5, SUIVI4_DOSSIER5, PROBLEME_BLOC_PLEIN_POUR_SOL} | 26-27/09 | survolés (en-têtes, résultats annoncés) ; SUIVI3/4 non lus au-delà du titre (questions envoyées à Astra) |
| 0371 | famille/REVUE_LITTERATURE_9_243.md | 26/09 | survolé |
| 0372 | involution/HANDOFF_FULLBLOCK.md | 26/09 | non lu au-delà du titre (passation d'un job CP-SAT nuage « bloc plein ») |
| 0423-0427 | external_c1/notes/{20_ATTAQUES_R, 99_VERROU_BOULES_DE_DROITES, 100_SYNTHESE_DES_LEMMES, 121_POINT_D_ETAPE_26_09, 134_SYSTEME_LOCAL_IOTA_BLOC_PLEIN} | 25-27/09 | survolés ; 100 §4 et 99 §0 lus (copies de notes de C1 : originaux dans le lot C1) |

Chronologie :

| date | événement | source |
|---|---|---|
| 2026-09-25 nuit | ouverture du journal du labo « structures » ; relectures adverses de C2 (queue, F, P) ; S5 (critère 2-adique général) | JOURNAL.md:3 ; REGISTRE S5, S6 |
| 2026-09-26 | tout-tordu à ≥ 2 triangles à la main (S10, S11), 1 triangle certifié (S17), 0 triangle certifié (S19) ; dossiers 5 et 6 d'Astra (k = 22 ; g⁻ = 8, 10 exclus) ; Sol (supports courts, Wagner) ; S25 famille ; S27 q:7 | REGISTRE ; astra/* |
| 2026-09-26 soir-nuit | AD au niveau paires (S28) ; g⁻ ∈ {16,18,20} ; A33 mort ; g⁻ ≠ 16 (S28 relit C1 notes/132) ; famille ancrée morte ; bloc plein (S29) | JOURNAL.md:729-840 |

### 7.G G. Desktop c2_experimental : passes externes, AWS, article (28/09-07/10)

Notes traitées :

| index | source | date | lecture | contenu |
|---|---|---|---|---|
| 0429 | external_runs/c1_96a94fe/INVALID_README.txt | 27/09 | lu | bug pair_h_check (verdicts nuls) |
| 0430, 0431 | external_runs/c1_code/SOURCE_COMMIT.txt, c1_pairs/SOURCE_COMMIT.txt | 27/09 | lus (empreintes de commit) |
| 0528 | external_runs/astra_shallow/…/README_AND_PROOFS.md | 28/09 | survolé (statut, lemme de couverture exacte conjuguée) |
| 0529 | external_runs/flex_boundary/…/README.md | 28/09 | survolé (statut, lemme d'ombre frontière) |
| 0553, 0554 | external_runs/fractional_proof/…/PROOF.md, README.md | 29/09 | survolés (résultat, portée) |
| 0555, 0556 | external_runs/shell_theorems/…/PROOFS.md, README.md | 29/09 | survolés (résultats, statut) |
| 0550 | PLAN_AWS.md | 29/09 | survolé (en-tête : plan 18 tranches, remplacé par le dépôt conway99-c2-aws) |
| 0551, 0552 | c2_cloud_calib/requirements.txt ; c2_cloud_run/README_RUN.md | 29/09 | survolés |
| 0566 | moniteur_aws/LISEZMOI.txt | 29/09 | non lu au-delà du titre (mode d'emploi du moniteur) |
| 0670 | aws_repo/HANDOFF_2026-10-01.md (1 153 lignes) | 01-07/10 | survolé structuré (titres §1-§20 ; lus §7, §19, §20) |
| 0671 | aws_repo/lemma/upstream/PROOF_SKELETON_C2.md | 01/10 | survolé (Parties I-II, début de la table) |
| 0672 | azure_layer_wip/LISEZMOI.md | 01/10 | survolé (couche Azure mise de côté, rien poussé) |
| 0705 | golay_work/PROVENANCE.txt | 02/10 | lu (commit structures 3e9690b) |
| 0706, 0707 | logs/handoff_v8_draft.md, handoff_v8_final.md | 02/10 | final lu ; draft = version antérieure |
| 0723 | qwatch/order.txt | 04/10 | agrégé (ordre des clés de la file) |
| 0741 | aws_repo/lemma/PROOF_C2/paper/main.pdf | 07/10 | survolé (p. 1-2) ; source .tex dans conway99-c2-aws (lot L02) |
| 0557-0565, 0673, 0708-0722, 0724, 0742, 0743 | logs/{camp15_*, camp16_*, chunks_to_rerun, pc_mode, suspended_pids, ALERTS, keys_*, parked_split_originals, order_snapshot_1006, n3run/STATUS, n3run/shares} | 29/09-07/10 | agrégés : journaux opérationnels de la file (clés de jobs, relances, alertes) |

Chronologie :

| date | événement | source |
|---|---|---|
| 2026-09-27 ~14:30 | bug de pair_h_check (96a94fe) : verdicts nuls | INVALID_README.txt |
| 2026-09-28 | Astra : coupes résiduelles peu profondes ; confinement des extrémités et points frontière | external_runs |
| 2026-09-29 | Astra : théorèmes de coquille et enveloppe jumelle ; contre-exemple fractionnaire exact ; plan AWS (18 tranches) puis dépôt conway99-c2-aws | external_runs ; PLAN_AWS.md |
| 2026-10-01 21:40 | passation AWS (file adaptative, bugs corrigés) ; squelette de preuve 93/156 | HANDOFF_2026-10-01.md ; PROOF_SKELETON_C2.md |
| 2026-10-02 ~15:20 | 118 paires INCOMPLETE (moteur v2, K = 0) découvertes → paquet v8 | handoff_v8_final.md |
| 2026-10-03 10:52 | arrêt (demande de l'utilisateur) ; second compte | HANDOFF §12-13 |
| 2026-10-07 17:50 / 19:30 | tracker 156/156 ; article écrit | HANDOFF §19-20 |

### 7.H H. Dossiers externes Sol/Astra et littérature (conway99-c2-experimental external_inputs/, downloads/ ; Desktop CONWAY_NOUVEAUTES)

Notes traitées :

| index | source | date | lecture | contenu |
|---|---|---|---|---|
| 0254 | external_inputs/CONWAY_ASTRA_27_09_2026_0836/BILAN_ATTAQUE_DIRECTE_REPERE42_7.md (13 copies) | 27/09 | survolé (via LIRE_D_ABORD et bilans) |
| 0255 | …/DOSSIER_SOURCES_SORTIES_REPERE42_7.md (896 Ko) | 27/09 | non lu : reproduction des programmes et sorties (aucun résultat propre au-delà des bilans) |
| 0256-0275, 0277-0281 | …/EXTRAIT/attaque_globale_27_0803/* (audits collage E8, composantes de racines, Golay, indécomposabilité, norme 1, racines corang un, bilan, contre-modèle Golay, état de reprise, G18_G20_*, indécomposabilité globale, racines corang un, sept blocs, template shadow24, unification) | 27/09 | BILAN_ATTAQUE_GLOBALE et LIRE_D_ABORD lus ; les autres survolés par leurs titres (énoncés repris dans le bilan) |
| 0264, 0277 | …/0803/DOSSIER_COMPLET_SOURCES_ET_SORTIES.md (320 Ko), PREUVES_COMPLETES_ATTAQUE_GLOBALE.md (140 Ko) | 27/09 | non lus : recueils des preuves et sorties déjà résumées par le bilan |
| 0276 | …/0803/LIRE_D_ABORD.txt | 27/09 | lu |
| 0282-0301, 0303, 0305-0309 | …/EXTRAIT/attaque_globale_27_0836/* (audits D11, D6 mixte, D8^3, génération 42, heptade, Q42 ; bilan 0836 ; classification D6^4 ; coupes ; D4^6 ; exclusions D8^3 ; G18_G20_D6_*, dual, 42 générateurs, sept blocs capacité, statuts ; obstruction coque 3 ; shadowframe24 ; sept octades ; supplément D8^3 ; caractéristique 8 ; moments) | 27/09 | BILAN_AUDIT_INDEPENDANT_0836 et LIRE_D_ABORD lus ; les autres survolés par leurs titres |
| 0293 | …/0836/ETAT_REPRISE_SNAPSHOT.md (79 Ko) | 27/09 | non lu (état de reprise ; le bilan donne les conclusions) |
| 0304 | …/0836/PREUVES_COMPLETES_REPERE42_7.md (381 Ko) | 27/09 | non lu (recueil de preuves) |
| 0302 | …/0836/LIRE_D_ABORD.md | 27/09 | lu |
| 0459 | …/ETAT_REPRISE_ACTUEL.md (80 Ko) | 27/09 | non lu au-delà de l'en-tête (« conclusions, limites et prochaines cibles ») |
| 0460 | …/LIRE_D_ABORD_POUR_CLAUDE.md | 27/09 | lu |
| 0310 | external_inputs/sol/CAMPAGNES_A33_NORME10_COMPLETES.md (216 Ko) | 26/09 | survolé (en-tête et table des résultats) |
| 0311-0325 | external_inputs/sol/files/outputs__coupures_et_torsion__* et outputs__fermeture_A33__* (ETAT_REPRISE, PREUVE_A33, PREUVE_COUPURE_NORME10, RAPPORT, SHA256SUMS, sorties indépendantes / F7 / normes, PREUVE, explorations, sorties sage) | 26/09 | RAPPORT (×2) lus ; preuves et sorties survolées (titres) |
| 0376 | external_inputs/sol/DOSSIER_G16_PRISME.md (339 Ko) | 26/09 | survolé (théorème, statut, §1) |
| 0230-0246, 0428 | Desktop external_inputs/CONWAY_NOUVEAUTES_27_09_2026_1323/* (LIRE_D_ABORD, ETAT_REPRISE 82 Ko, complément rang 15, coupe congruence racines, troisième vecteur norme 7, attaque_globale_27_1031/* (audits IAC, IBD, bloc II adjacent ; bilan 1031 ; coupe spinors ; D6 IAC/IBD/normales/six fractionnaires), attaque_globale_27_final_agressive/*) | 27/09 | LIRE_D_ABORD et bilan 1031 lus ; ETAT_REPRISE non lu au-delà de l'en-tête ; autres survolés (en-têtes) |
| 0080-0091, 0156-0166 | downloads/* (PDF et .txt d'articles), downloads/profondeur_2409/* | 23-24/09 | catalogués (L01-113), non résumés |

Chronologie :

| date | événement | source |
|---|---|---|
| 2026-09-26 | Sol : coupures de norme 10, torsion A33 (g⁻ = 20 forcé), puis fermeture A33 par le signe de Witt ; g⁻ = 16 force un prisme | sol/* ; git 9415b71, 89738b9 |
| 2026-09-27 08:03 | Astra/Sol (session Codex) : attaque globale, réseau commun N_max, collage de rang 24, indécomposabilité, racines de rang ≤ 20 | CONWAY_ASTRA_…/0803 |
| 2026-09-27 08:36 | attaque directe du repère : D8^3, D11, D6^4 (six blocs sur une même paire), sans racines → code [24,12,8] | CONWAY_ASTRA_…/0836 |
| 2026-09-27 10:31-13:23 | D6^4 : tous les régimes à six blocs fractionnaires exclus ; troisième vecteur de norme 7 ; « dernière attaque accélérée » sans exclusion | CONWAY_NOUVEAUTES_… |
| 2026-09-27 11:35 | import du dossier dans le labo (f2198e8) → naissance de la route (C) | git log |

### 7.I I. Mission « C2 sans calcul » (13-14/10), consolidation de l'ordre 2, audit v7, code7, données r6

Notes traitées :

| index | source | date | lecture | contenu |
|---|---|---|---|---|
)
| 0594, 0761, 0656 | code/lab_c2_elegant_2026-10-13/NOTE_MISSION_C2.md ; copie c1-main-codex ; version antérieure dans work/scratchpad_LAB_2026-09-30/… | 13/10 | lu (§0-§9) ; copie identique ; version ancienne : 22 lignes différentes (sections en moins) |
| 0590, 0758 | …/DIGEST_T16_T18_T20_ENGINE.md (85 Ko) | 13/10 | survolé (en-tête, conventions) |
| 0591, 0759 | …/INVENTORY_C2_CAMPAIGNS.md (77 Ko) | 13/10 | survolé ; §6 lu intégralement |
| 0592 | …/KILL_STATISTICS_156.md (78 Ko) | 13/10 | survolé (§0 lu) |
| 0593, 0760 | …/LEMMAS_AGENT_REPORT.md (41 Ko) | 13/10 | §0 lu |
| 0600 | …/region_pairs/REGION_PAIRS_REPORT.md | 14/10 | §0-§2 lus |
| 0595-0599 | …/lemmas_agent/support_k0_m8..m12_survivors.txt | 13/10 | agrégés (listes d'arêtes des graphes d'orbites survivants, E = 8..12) |
| 0655 | work/c2_elegant_2026-10-13/SOUNDING_E11.md (espace researcher2) | 14/10 | §0 lu |
| 0586, 0762 | code/lab_c2_consolidation_2026-10-14/AUDIT_ORDER2_PAPER.md | 13/10 | §1-§4 lus |
| 0587, 0763 | …/PART1_NOTES.md | 13/10 | lu intégralement |
| 0589, 0765 | …/order2_part1.tex (54 Ko) | 13/10 | non lu ligne à ligne (contenu décrit par PART1_NOTES ; même mathématique que l'article) |
| 0588, 0764 | …/order2_lemma16_partA.tex | 14/10 | survolé (structure des énoncés) |
| 0653, 0654 | work/c2_consolidation_2026-10-14/*.pdf (espace researcher2) | 14/10 | non lus : versions compilées des .tex |
| 0578, 0749 | code/lab_audit_v7_2026-10-12/AUDIT_V7.md | 12/10 | §1-§2 lus |
| 0752 | …/THEOREM_Z3_COVERS.md (c1-main-codex) | 12/10 | énoncé lu |
| 0579-0585, 0750, 0751 | …/OUTPUT_*.txt, z3_solutions_half.txt | 12/10 | agrégés (sorties d'audit243, gridparts, hexagones, classification et orbites Z3 ; solutions Z3 = données) |
| 0753-0757, 0744-0748 | code/code7_mots_binaires/{AUDIT, README, SHA256SUMS, THEOREME, VERIFICATION} (claude/v7-simultaneous ; copie c1-asymmetry-audit) | 12/10 | THEOREME lu (§1-§2), AUDIT survolé, autres lus (courts) |
| 0533-0548, 0725-0740 | code/r6/j1av/*.txt, code/r6/j2/*.txt (main ; copie c1-asymmetry-audit) | 28/09 | agrégés (données numériques du programme R6 de C1) |

Chronologie :

| date | événement | source |
|---|---|---|
| 2026-09-28 | C1 : J1a fermé par énumération PSD exhaustive (R6) ; moteur 2|5 | git conway99-c1 4bf5d98a, 705e7af2 |
| 2026-10-12 | audit v7 (srg(243) : Γ3, Γ4 ; Z3-revêtements : quatre) ; mots binaires mod 7 (C1) | AUDIT_V7 ; THEOREM_Z3_COVERS ; 640ffe1 |
| 2026-10-13 22:15 | mission C2 sans calcul, résultat 1 (E ≤ 12 forcé) | 441080db |
| 2026-10-13 22:30-23:42 | résultat 2 (identités exactes), sonde « un h » négative, idée « z marqué » = reformulation, rapports d'agents (inventaire, statistiques, digest, lemmes) ; audit de l'article d'ordre 2 (22:53) ; Partie I écrite (23:01) | e4d0ba5c … 5ff35806 |
| 2026-10-14 00:07 | identités vérifiées sur les 1 042 paires de région ; pas de raison uniforme pour l'heptade manquante | 194a3301 |
| 2026-10-14 | sondage E = 11 ; T16 partie A rédigée | SOUNDING_E11.md ; order2_lemma16_partA.tex |

## 8. Matériaux pour la recombinaison

Une entrée par ligne, format fixe ; la lettre entre crochets finale renvoie à la partie (§7) d'où vient l'entrée. Les sources sont relatives au dépôt de la partie lorsque le chemin est abrégé (voir §7 pour le chemin complet).

### 8.1 Énoncés conditionnels « si X alors … » (46)

- [COND] si aucune involution n'existe (C2 exclu) alors |Aut(Γ)| ∈ {1,3} | P (littérature, L01-01) | X = objectif de la branche | conway99-involution:master:notes/NOTE_involution_case.md:67 [A]
- [COND] si C2 et C3 sont exclus alors tout Γ est asymétrique (C1) | P (littérature) | ouvert à cette date | conway99-involution:master:README.md:13 [A]
- [COND] si Stage Q (matrices Q_out) est UNSAT dans les trois cas sib/one/dis avec preuves vérifiées alors pas d'involution, |Aut| ∈ {1,3} | P (Stage Q relaxation saine, L01-16) | O | conway99-involution:master:LAB_INSTRUCTIONS.md:81-82 [A]
- [COND] si le cas sœur est exclu à la main alors un tiers des instances tombe | H (estimation) | O | conway99-involution:master:report/dossier_chercheurs_fr.tex:414-417 [A]
- [COND] si une classe du recensement d'ordre 7 à parité constante contredit la parité de ses copies σ-invariantes alors la branche involution meurt | P (principe) | O | dossier_chercheurs_fr.tex:423-425 [A]
- [COND] si le cœur μ_c = τ_c = π vaut en une ligne alors contradiction avec |Σ| ≤ 4 (donc prouver le cœur = prouver « pas d'involution ») | P | X non établi (O) | c2-compute:…/NOTE_core.md:52-59 [B]
- [COND] si le lemme de l'étoile libre (forme locale : RSF(star(c)) UNSAT quand aucune grille ne contient c) est vrai alors le cas involution est clos | P (dit par la source : « smallest open statement that would close the case ») | O | NOTE_core.md:119-121 [B]
- [COND] si un « accident 7-adique » à k = 28 est toujours isotrope alors k = 28 exclu ; s'ils contiennent un sous-espace totalement isotrope de dimension (30 − k)/2 alors tout k exclu (k = rank7(A − 3I) − 15), donc pas de srg(99,14,1,2) | P (implication énoncée) | O | MATH_C2_PROGRAMME.md:581-584 [B]
- [COND] si 13 classes singulières indépendantes mutuellement orthogonales existent dans D− et dans D+ alors contradiction avec « produit des types = moins » (pas d'involution) | P (énoncé par la source) | O | NOTE_arith.md:67-71 [B]
- [COND] si toutes les paires sont frères (D(U) = U′) alors contradiction | P | — | MATH_C2_PROGRAMME.md:106 [B]
- [COND] si un sommet est plat alors contradiction (tout srg(99,14,1,2)) | P | — | MATH_C2_PROGRAMME.md:553 [B]
- [COND] si (seconde détermination indépendante de r mod 2 ou de k) alors conclusion par la voie 7-adique | P (forme) | O | MATH_C2_PROGRAMME.md:70 [B]
- [COND] si le lemme de l'étoile libre (forme locale) est vrai alors C2 n'existe pas | P (réduction note 20 §0) | O | conway99-c2-experimental:master:notes/20_ETOILE_LIBRE_IDEES.md:16-22 [C]
- [COND] si toutes les instances I(τ) (3 308 classes ; puis (A) 1 507 types à pivots + famille tout-dis (B)) sont UNSAT alors pas d'involution | P (comptage w_c ≥ 12, bris d'égalité) | O (32/32 cubes inconnus) | Desktop c2_experimental/notes/46_LIGNE_D_ARRIVEE_C2.md:36-38,61-65 [C]
- [COND] si Σ = ∅, tous les carrés « un bloc », et les 79 systèmes locaux sont UNSAT (DRAT) alors l'involution est impossible dans ce cas (M1, mélanges, T = ∅, T = K7) | P | 25/79 C, reste O | notes/45_FAMILLE_UN_BLOC_79_SYSTEMES_LOCAUX.md:7-9,166-175 [C]
- [COND] si toutes les classes pertinentes à ≥ 6 étiquettes sont UNSAT sauf (0,6) alors tout bloc est (0,6) et T = K7 (tout-tordu) | P | O | note 45:118-122 [C]
- [COND] si aucune enveloppe U de la liste de Borcherds (156) ne porte le repère (F) alors pas d'involution | P (cadre Sol/Astra relu par structures ; plus tard Théorème R, lot L02) | E puis 156/156 (lot L02) | Desktop notes/46:98-99 [C]
- [COND] si le modèle joint « graphe exact + témoin court » est infaisable pour les 11 couples (n,k) alors pas d'involution | P (sous couverture et scans) | O | Desktop notes/54_SOLO_MODELE_JOINT_TEMOIN_28_09.md:17 [C]
- [COND] si n3 < 2079 alors Γ contient une grille (tout srg(99,14,1,2)) | P | — | SYNTHESE.md:20 [C]
- [COND] si une parité de |Σ| était obtenue alors la moitié des 10 survivants tombe | H | O (exigerait l'ordre 9) | notes/22_REVUE_COMPLETE.md:148,153 [C]
- [COND] si la propagation (P) (une seconde réflexion automorphe) vaut alors C2 meurt (équivalence) | P (dit par la source) | O (résidu de dimension 30) | README.md (labo):14-17 [C]
- [COND] si un couple (N,D) explicite satisfait (S) et L_N alors il existe un graphe de Conway avec involution à un point fixe (reconstruction vérifiée) | P | O | MODEL.md:57-73,85 [D]
- [COND] si EX est faux alors aucune involution à un point fixe ; avec F0, aucune involution (C2 exclu) | P (T4 relu ; F0 cité/reprouvé, L02) | non-EX établi via la route (C) (lot L02) | MODEL.md:85-88 [D]
- [COND] si la rigidité de signe (R) vaut (au plus une signature faisable par couple non signé complet) alors le problème se réduit à la couche non signée + phases | P (forme) | O | RESULTS.md:189-192 ; native/B_DETERMINACY [D]
- [COND] si l'on obtient G mod 2 (nombre de grilles 3×3) indépendamment alors n2 ≡ G (mod 2) contraint le type 2 | P | O | RESULTS.md:248-249 [D]
- [COND] si 156/156 (route C) et T16, T18, T20, Borcherds, oddité, complétude des énumérations et code du moteur sont acceptés alors aucun srg(99,14,1,2) n'a d'involution | P (chaîne, IA seulement) | tracker 156/156 le 07/10 | FINAL_STATEMENT_C2_DRAFT_2026-10-07.md:8-16,116-128 [D]
- [COND] si un (Q,N) exact satisfait le système couplé alors un graphe de Conway existe (reconstruction puis vérification A² + A = 12I + 2J) | P | O | conway99-c2-campaign:main:README.md:80-90 [E]
- [COND] si deux complétions intégrales existent pour un même N alors elles diffèrent sur exactement 8 blocs ambigus (r = 8) | P (T2, non audité) | — | archive/FULL_DOSSIER.md:233-239 [E]
- [COND] si g⁻ = 18 et g⁻ = 20 sont exclus et si au moins un Q_c est inversible alors pas d'involution | P (Astra 6, conditionnel) | O (la condition Q_c n'est pas démontrée) | external_structures/astra/RAPPORT_ASTRA_DOSSIER6.md:13,44 [F]
- [COND] si un argument 7-adique n'utilise que « 7 | t, 7 ∤ v » et les identités de la famille srg(2m²+1,2m,1,2) alors il exclut d'un coup 99, 6 273 et 494 019 | P (dit par la source) | O | external_structures/NOTE_S25_FAMILLE_9_243.md:15-16 [F]
- [COND] si un bloc est plein alors g = 20 (donc à g = 18 ni bloc plein ni résidu AD) | P | — | external_structures/JOURNAL.md:839-840 [F]
- [COND] si une SRG contient la boule tordue d'Astra (dossier 5) alors k ≥ 24 | P (relu) | — | astra/RAPPORT_ASTRA_DOSSIER5.md:74 [F]
- [COND] si l'on avait un plafond de torsion (P ≥ 1152, C1) alors contradiction avec L16 (P ≤ 1151) | P | O | external_c1/notes/99_VERROU_BOULES_DE_DROITES.md:4-6 ; L01-31 [F]
- [COND] si C2 (Théorème 1.1) et les ordres 3, 7, 11 sont exclus alors un srg(99,14,1,2), s'il existe, est asymétrique (Corollaire 1.2) | P | Théorème 1.1 : P (IA seulement) ; ordre 3 : Lean (lot L04) ; ordre 7 : Lean (L01-43) ; ordre 11 : Behbahani–Lam (ordinateur) | main.pdf p. 2 [G]
- [COND] si y1 a une racine r avec (r,y1) = ±2 alors y1 ne porte aucun repère quel que soit y2 (Corollaire Y1, avec T18, T20) | P (relu) | — | HANDOFF_2026-10-01.md:990-991 [G]
- [COND] si un repère physique 42 + 7 + 2 existe dans une enveloppe U alors U n'est ni D8^3, ni à composante D11, ni à E8 ou D_n (n ≥ 12) ou A_n (n ≥ 22), et le rang de ses racines est ≤ 20 (dans N_max) ; dans D6^4 au moins trois blocs sont entiers | P (audits internes) | — | BILAN_ATTAQUE_GLOBALE ; BILAN_AUDIT_INDEPENDANT_0836 ; BILAN_1031 [H]
- [COND] si U est sans racines alors le repère force 24 ombres orthogonales et un code autodual doublement pair [24,12,8] | P | — | BILAN_AUDIT_INDEPENDANT_0836 [H]
- [COND] si g⁻ = 16 alors Γ contient un prisme induit (donc P > 0) | C (deux implémentations) | — | sol/DOSSIER_G16_PRISME.md:3-5 [H]
- [COND] si une involution a l'étoile A111111 (3,3) alors contradiction (g⁻ ≥ 22 > 20) | C | — | sol/files/outputs__fermeture_A33__RAPPORT.md:3-6 [H]
- [COND] si les lemmes T22 et T24 (aucune fonction propre entière σ-impaire pour −4 de somme de carrés 11, resp. 12) sont prouvés alors NON-EX (pas d'involution) suit du Théorème R, de E ≤ 12 forcé et de T16, T18, T20, sans les 156 réseaux | P (résultat 1, non audité) | O | NOTE_MISSION_C2.md:25-28 [I]
- [COND] si la condition de piège (ombre E ≥ 11,5) et l'absence de vecteur entier 1 ≤ E ≤ 10 valent alors s ≥ 12 paires de fonctions propres caractéristiques (somme de carrés 46) existent | P | — | NOTE_MISSION_C2.md:119-124 [I]
- [COND] si l'on exclut à la main les fonctions propres caractéristiques (±2 sur un bloc, ±1 sur les 42 orbites) alors la région tombe | P (forme) | O | NOTE_MISSION_C2.md:81-82 [I]
- [COND] si l'heptade (sept h orthogonaux admissibles partitionnant les s classes) n'existe dans aucune paire de région alors ces paires sont exclues sans recherche | P | O (044 : sept-ensembles existent mais échouent au test des cellules de mots) | REGION_PAIRS_REPORT.md:10-12 [I]
- [COND] si l'article d'ordre 2 recertifie les transferts (4 163 099 paires, ≤ 2 479 669 hors Corollaire 7.3) alors le Théorème 1.1 est établi au standard de l'article | P | O (recertification préparée, non lancée) | AUDIT_ORDER2_PAPER.md (§3 B) [I]
- [COND] si un srg(243,22,1,2) a un partage régulier et une classe de parité triviale alors il est l'un des quatre connus (BvLS, jumeau, Γ3, Γ4) | E (non reproduit) | — | THEOREM_Z3_COVERS.md [I]
- [COND] si un mot binaire non nul de ker7(A + 4I) existe alors Γ a une partition équitable [[10,4],[7,7]] (w = 63) ou une coclique de Hoffman de taille 22 (w = 77) | P | O | code7_mots_binaires/THEOREME.md [I]

### 8.2 Bornes quantitatives (90)

- [BORNE] |Aut(Γ)| : ∈ {1,2,3} ; |G| divise 2·3³·7·11 | P (cité) | NOTE:9-15 [A]
- [BORNE] n3 (recensement) : 708 ≤ n3 ≤ 4158 (dépôt public) ; Reimbayev corrigé : 0 ≤ n3 ≤ 4158, 2n3 ≤ z11 ≤ 4n3, 4 | z11 | E | RESEARCH_MEMORY:17 ; AUDIT_reimbayev:32-33 [A]
- [BORNE] C4 induits : c4 = 2079 dans tout srg(99,14,1,2) ; 21 C4 σ-invariants (un par arête de D) | P | dossier_chercheurs_fr.tex:290-296 [A]
- [BORNE] Spec(Q_out) = {12,(−2)^6,3^20,(−4)^15} ; Spec(S) = 3^27 (−4)^22 ; Spec(S_out) = 0^7 3^20 (−4)^15 ; Spec(H) = {12,(−2)^6,0^7,3^40,(−4)^30} | P | NOTE:34-37 ; DEEP_THOUGHT:18 [A]
- [BORNE] rangs : rank_F2(S) = 27, rank_F2(Γ̄ + NbNbᵀ) = 20 ; rank_F3(S) = 22, rank_F3(S_out + G) = 15 ; rank_F3(I + Q − Ĵ) = 27 ; 7 ≤ rank_F7(S − 3I) ≤ 22 ; rank_F7(A − 3I) ≥ 26 (dépôt public) ; analogue m = 11 : 55 et 44 | P | NOTE:44-48 ; dossier:269-275,427 ; AUDIT_2026-09-22.md:21 [A]
- [BORNE] filtre de rang « ≤ r » inactif sur les sous-matrices de taille ≤ r (actif dès 16 pour F3, 28 pour Q mod 3, 21 pour F2) | P | dossier, remarque après prop:F3 [A]
- [BORNE] Stab(U0) : 15 360 (2^7⋊S7) / 7 680 (2^6⋊S7) ; lignes U0 : 3 436 / 36 175 / 321 878 ; orbites 13 (9 distinctes) / 149 / 1 164 | E | LAB summary:51-58,120 [A]
- [BORNE] couplages parfaits de L_c : 10 395 (11 types) ; triangles s = 0 candidats 35 560 ; 140 droites de taille 3 dans la partie s = 0 | E/P | counts.txt:1-19 ; DEEP_THOUGHT:26 [A]
- [BORNE] #triangles(Γ1) = 126 + 4 n_sib + 2 n_one ; tr Q³ = 1260 | P | LAB summary:61,96 [A]
- [BORNE] taille du modèle : 1 722 bits ; CNF k = 14 : 666 183 var. / 1 510 448 clauses ; Stage Q : 1 197 042 / 2 530 942 ; m = 11 : 12 606 825 / 28 274 730 | E | AUDIT_2026-09-22.md:40 ; LAB summary:43,25 [A]
- [BORNE] lignes candidates par orbite ≈ 10^7-10^9 ; « Q-patterns: 7 164 496 » (rows.py, tué) | H/E | BRIEFING_phase2.md:34 ; LAB summary:15 [A]
- [BORNE] mod 7 : S_out − 3I nilpotent d'indice 2 sur l'espace de dimension 35 ; rank_F7(S − 3I) ≤ 22 ; cohérent avec rank_F7(M) ≥ 27 universel du dépôt public (M ≡ −BᵀR0B, R0 = A − 3I − 4J nilpotent mod 7) | P / cité | conway99-involution:master:notes/RESEARCH_MEMORY.md:41-42 [A]
- [BORNE] énumérer D d'abord : ≈ 10^19 classes de couplages parfaits sur 42 points modulo le groupe | H | conway99-involution:master:notes/DEEP_THOUGHT_2026-09-22.md:34 [A]
- [BORNE] rank_F7(A − 3I) : impair (tout srg(99,14,1,2)) | P | MATH_C2_PROGRAMME.md:38-39 [B]
- [BORNE] r = rank_F7(S − 3I) pair ; 1 ≤ e = r − 7 ≤ 15 impair ; σ_S ≡ 1 (mod 8) ; r/2 + k ≡ 0 (mod 2) | P | MATH_C2_PROGRAMME.md:40-41,81 [B]
- [BORNE] k = rank7(A − 3I) − 15 : k ≤ 30 (Brouwer–van Eijl), k ≤ 28 (L22 de C1) ; minorations locales ≤ 22 ; bloc local ≤ 24 | P (cité) | MATH_C2_PROGRAMME.md:573-578 [B]
- [BORNE] ρ_S ≤ 24 (W² ≡ 0 mod 7) ; det L− = 2^27·7^{ρ_S}, det L+ = 2^27·7^{ρ+}·11 | P | NOTE_arith.md:24-26,68 [B]
- [BORNE] paramètres admissibles de srg(1+2m²,2m,1,2) : m ∈ {2, 7, 11, 56, 497} | P | MATH_C2_PROGRAMME.md:92 [B]
- [BORNE] cycles : 4-cycles 2079 (21 fixes) ; 5-cycles 41 580 (0 fixe) ; 6-cycles 429 660 (224 fixes) | P | MATH_C2_PROGRAMME.md:74-76 [B]
- [BORNE] g(x) ≤ 14 au point fixe | P (relu) | MATH_C2_PROGRAMME.md:595 [B]
- [BORNE] budget μ (16.1) : au plus 4 − 2n_s(P′) étiquettes hors partenaires D ont deux voisins dans P′ ; version sans σ : Σ_w C(n_R(w),2) = 8 − s_R − a_R − i_R | P | MATH_C2_PROGRAMME.md:367-369,597-603 [B]
- [BORNE] 9-ensemble à e arêtes : ‖E−4 1_S‖² = (36 − 2e)/7 ; déviation quadratique totale ≤ 7(36 − 2e) | P | MATH_C2_PROGRAMME.md:568-569 [B]
- [BORNE] C1 (cité) : ≤ 18 grilles par sommet (L10) ; Krein P ≤ 1151, Σ|W| ≥ 1410 (L16) ; plafond de torsion manquant P ≥ 1152 | P (cité) | MATH_C2_PROGRAMME.md:564-566 [B]
- [BORNE] (P2) : 210 identités quadratiques Σ_Z φ_Z(R)φ_Z(R′) = 16 − E[R][R′] − 4[R∩R′ ≠ ∅] ; (S) Σφ = 24 ; (PPE) Σφ² = 32 ; diagonale générale 2k + 4 − e(R) | P | MATH_C2_PROGRAMME.md:1002-1019 [B]
- [BORNE] H-β : 552 classes / 7 680 squelettes, écart minimal 55,4 ; M1 n = 3 : 2 928 squelettes, 23 classes ; n = 4 : 214 classes, écart 16,4 ; tout-tordu 1 triangle : 41 790 décompositions / 15 classes / 84 certificats ; 0 triangle : 30 360 décompositions / 14 classes | C | MATH_C2_PROGRAMME.md:1026-1092 [B]
- [BORNE] Fable : au moins 34 des 42 orbites ont un carré non sib ; Σ_c p_c ≤ 16 + n_one ; Σp_c = 2n_sib + n_one ; n_sib = 2|Σ| | P (dépend de |Σ| ≤ 4) | NOTE_core.md:46-54 [B]
- [BORNE] Fable : #triangles de quotient par paire partenaire = 42 − Σ_c p_c/2 ; #triangles A′ = 126 + Σ_c p_c, dont équilibrés 28 + Σ_c p_c/2 et non équilibrés 98 + Σ_c p_c/2 (cohérents pour toute valeur de Σ_c p_c ∈ [0, 16 + n_one]) | P | c2-compute:origin/claude/tender-archimedes-q532j1:scripts/fable/NOTE_core.md:111-117 [B]
- [BORNE] Fable : 3 580 classes de types de blocs à m = 7, 3 308 valides (1787/958/407/106/39/11 par nombre d'étiquettes pivots), = C1 | E | fable/README.md:11-12 [B]
- [BORNE] Fable : résidu des orbites lointaines de rang (rank G) − (3m − 3) : 25 pour m = 11, 4 pour m = 7 | E | fable/README.md:7-9 [B]
- [BORNE] C7 : G = 21 × projecteur de rang 4 ; tr C = 0 ; 0 ≤ tr C ≤ 39 ; 3 ≤ h ≤ 5 | P (Lean) | conway-C7 lean/README.md:55-56 [B]
- [BORNE] Σ (grilles par x) : deg Σ ≤ 2 ; |Σ| = n_sib ≤ 4 ; ≤ 2 grilles par droite de x ; Σ ∈ {∅, K2, P3, 2K2, K3, P4, P3+K2, 3K2, P5, 2P3} | C (DRAT non archivé) + P | data/survivors_after19.txt ; SYNTHESE:117-125 [C]
- [BORNE] système χ : 1 044 graphes Σ → 988 impossibles, 56 possibles (11 atomes DRAT) ; 39 survivants après note 18 | C | SYNTHESE:108-111 [C]
- [BORNE] prismes P = n1 = 1386 − n3/3 ; P ≥ 6N ; n3 ≥ 2079 − 9N ; avec L16 (P ≤ 1151) : N ≤ 191 ; 2 n_sib + n_one prismes σ-invariants (BvLS : 110) | P | notes/08:6-8 ; revue:23-24,204 ; note 20:33-37 [C]
- [BORNE] parités : n3/3 ≡ n_one (mod 2) ; S ≡ 0 (mod 4) ; z11 ≡ 4n_one (mod 8) ; z2 pair | P | revue:25-28,63 [C]
- [BORNE] rangs 7-adiques : rank7(A − 3I) = 1 + ρ impair ; rank7(S − 3I), rank7(S_out − 3I), rank7(Q_out − 3I), ρ+ pairs ; det N3 = 7^ρ·11 | P | SYNTHESE:23-27 [C]
- [BORNE] défauts de Hall : σ_v(x) = σ_x(v) seulement sur les 4n_sib ≤ 28 coins sib (≤ 16 après le lemme des étoiles) ; au plus 28 droites D-fermantes sur 42 | P | SYNTHESE:68 ; revue:98-99 [C]
- [BORNE] lemme des carrés one : r_α + r_β ≤ 1 | P (vérifié) | revue:171-174 [C]
- [BORNE] identité de comptage : Σ_c #piv_c = 42 + 2|Σ| − 2n_dis ; Σ_c d_c = 4 n_dis ; Σ_c w_c = 84 + 4|Σ| ; un bloc a w_c ≥ 12 | P | Desktop notes/46:18-20 [C]
- [BORNE] types de blocs : 3 308 classes (1 787 / 958 / 407 / 106 / 39 / 11 par nombre de pivots) ; (A) 1 521 puis 1 507 ; 79 classes pertinentes à ≥ 6 pivots ; 156 classes à ≥ 6 pivots | E | Desktop notes/46:41-42,62-72 ; note 45:45-47 [C]
- [BORNE] tout-tordu : 121 215 décompositions à circuits simples contre 15^7 ≈ 1,7·10^8 systèmes de transitions | E | note 45:124-128 [C]
- [BORNE] mélanges : 47 classes de T, 1 797 classes d'orientations ; après filtre v6 : 1,3·10^4 à 2,2·10^5 classes de squelettes par classe (6-14, 17) ; AD2 : 322 classes d'orientations ; queue : tue 308/322 | E | note 41:53-55,72-73 [C]
- [BORNE] moments : 1 722 variables binaires à t près, 243 moments d'orbite au degré 2 | E | SYNTHESE:92-95 [C]
- [BORNE] cubes de l'étoile libre : 11, tailles d'orbites sous B6 sommant à 10 395 | E | revue:21-22 [C]
- [BORNE] Krein : entiers pour m = 2, 11 ; dénominateur 49 pour m = 7, 56, 497 | E | SYNTHESE:48 [C]
- [BORNE] g⁻ (dossiers Sol/C1) : g⁻ = 16 impossible, donc g⁻ ∈ {18, 20} | C (8 modèles LP certifiés) | note 44:104 [C]
- [BORNE] route (C) au 29/09 : 58/156 exclus ; piège caractéristique (norme 16) : (z,y1)² + (z,y2)² ≤ 66 ; tue 35-53 % des paires ordonnées ; règle d'échange 30-48 % ; 45 345 orbites y1 dans 68 réseaux ouverts | E | route_c_29_09/README.md:4-12 ; 56_PROMPT:124 [C]
- [BORNE] B (support de N) : rank2 B = 26, rank2(B + I) = 22, dim V1 = 20, rank2 G = 6 | P | RESULTS.md:49 [D]
- [BORNE] supports de type 2 : 133 classes S7, n2 ≤ 11 (132 classes, n2 ≤ 10 avec J) | E | RESULTS.md:135-138 [D]
- [BORNE] arêtes : T− = 28 + n1 + 2n2 ; e_F pair, 94 ≤ e_F ≤ 112 | P | RESULTS.md:166-170 [D]
- [BORNE] lignes admissibles : 930 336 / 155 904 / 22 176 (graphes de ports) | E | RESEARCH_HISTORY.md:50 [D]
- [BORNE] lignes zéro-somme |X(u)| ∈ {0, 3..7, 10} | P | RESULTS.md:190 [D]
- [BORNE] projecteur ternaire : rank_F3(P) = 15 ; spectre réel de N : 4^15 (−3)^20 0^7 | P (non revu) | external/…/THEOREMS.md:27 [D]
- [BORNE] torsion : ‖Z‖² ≤ 448 − 2τ − (τ − 56)²/7 (m = 7) ; 990 à m = 11 (BvLS) ; densité de couverture 8/(m − 3) ; K = 0 ⇒ 7 | τ ; d = 6 + d′_S, d′ = 1 + d_S ; σ− + σ+ = 7g ; 2g ≤ ‖Z‖² ≤ 14σ−σ+/(σ− + σ+) ; d ≤ 6 + τ/7 − ‖Z‖²/98 ; à d = 6, d′ = 1 : τ ≥ 3 | P | RESULTS.md:308-332 [D]
- [BORNE] Hodge : Δ1 ⪰ 3I ; b2 = 1715 (m = 7) ; spectre BvLS de Δ1 : 3^11, 18^792, 21^660, 27^990, 30^220 | P/E | agents/gen1_destroyer/RESULTS:21-29 [D]
- [BORNE] énergie des enveloppes : K + E(y1) + E(y2) = 3|Φ|/4 + 8 ; h1 + h2 = |Φ|/8 + 2 ; 2P = |Φ| + 48 ; K ≥ 4|h1 − h2| ; paires lourdes (K = 0) seulement si h1 = h2 (39/156) | P | HANDOVER:149-172 [D]
- [BORNE] pièges : (z,y1)² + (z,y2)² ≤ 66 pour z caractéristique de norme 16 (violations vues : Y_z ∈ {74, 98}) ; norme 24 : Y_z ≤ 122 | P (cité, Astra 28/09) | HANDOVER:79-82,212-213 [D]
- [BORNE] route (C) : 142/156 au 04/10 ; reste 2 500-3 200 cœurs-heures ; ~14 100 jobs v9 ; coût réel/estimé ×1,30 ; 7 662 jobs-heures restants au 01/10 | E | HANDOVER:117-143 ; ROUTE_C_RESUME_STATUS:74-80 [D]
- [BORNE] complétion d'un N complet : au plus dix paramètres binaires ; composantes à deux choix = K2,2 consommant deux cellules ; 21 cellules | P (T1) | archive/FULL_DOSSIER.md:223-229 [E]
- [BORNE] T2 : 5 ≤ r ≤ 10, 4 | r ⇒ r = 8 ; ZZᵀ = 33I ; X² + X = 8I | P (historique) | archive/FULL_DOSSIER.md:235-237 [E]
- [BORNE] T3 : si deux D existaient, |A_0| = K4,4 et au plus 4 cellules affectées par bloc : 7×4 = 28 < 32 incidences requises | P (non audité) | archive/FULL_DOSSIER.md:249 [E]
- [BORNE] modèle natif : 861 variables à 4 états ; par ligne : 1 d, 10 signés, 30 nuls | P | compute/NATIVE_SOLVER.md:7-24 [E]
- [BORNE] route (C) au 01/10 (campagne) : 91/156, ~6 600 CPU-h restants | E (rapporté) | compute/ROUTE_C.md:9-23 [E]
- [BORNE] g⁻ (involution) : g⁻ ≥ 7, pair, ≤ 20 ; 8 et 10 exclus ; 16 exclu ; g⁻ ∈ {18, 20} | P | NOTE_S27:27 ; RAPPORT_ASTRA_DOSSIER6:11 ; JOURNAL:827-830 [F]
- [BORNE] M (jauge de C2) : 88 ≤ M ≤ 173 | P | NOTE_S27:28 [F]
- [BORNE] lemme de Witt : g ≥ 18 + t − 2r0 + 2·[boule réduite non scindée] | P | JOURNAL:825 [F]
- [BORNE] k = rank7(A − 3I) − 15 : k ≥ 23 − d(L) (L21) ; droite 7-générique ⇒ k ≥ 22 ; d(L) ≤ 9 conjecturé ⇒ k ≥ 14 ; k ≤ 28 (L22) ; k = 30 exclu (L22) ; boule tordue d'Astra ⇒ k ≥ 24 | P / H | external_c1/notes/99:10-13 ; 100:195 ; Astra 5 [F]
- [BORNE] P (prismes) : P ∈ [0, 1155] par triplets de droites ; P ≤ 1151 (L16) | P | external_c1/notes/99:14 [F]
- [BORNE] bloc plein : spectre de T_FF = 3^9 (−4)^4 (−1)^5 (−2)^6 1^6 ; |r_f|² = (14 + y − 3x)/15 ; quasi-design (30 quadruplets, paires couvertes 3 fois, paires π 2 fois) | P | NOTE_S29:65,104 ; JOURNAL:835-838 [F]
- [BORNE] carrés dis : 3h ≤ 2n_dis ; 𝒫² = 14𝒫 ; D(A) réduit à 5 supports | P | REGISTRE:31 [F]
- [BORNE] tout-tordu : 121 215 décompositions étiquetées, 20 types (S7) ; 5 880 à deux triangles disjoints ; 27 720 à deux triangles sécants (8 classes) ; 41 790 à un triangle (15 classes) | E | REGISTRE:16-27 [F]
- [BORNE] critère S5 : 35 paramètres « ? » exclus, 0 sur 1 183 graphes connus | E | NOTE_S5:5-7,55 [F]
- [BORNE] Sol Wagner : 25 classes à six blocs exclues, 120 à sept blocs ouvertes (à P = 0) | C (certificats entiers) | astra/RAPPORT_SOL_WAGNER.md:5 [F]
- [BORNE] coquille caractéristique de norme 16 : 3-design sphérique (second moment isotrope) pour toute enveloppe | P (non audité) | shell_theorems/PROOFS.md:41 [G]
- [BORNE] O24 : coquille de norme 3 de la paire de normales de l'exemple : max Y(x) = 10 ; min K* ≥ 8/7 ; 6 040 droites de norme 4 admissibles ⊥ normales | C | fractional_proof/PROOF.md:54,67 [G]
- [BORNE] route (C) au 01/10 19:49 : 93 exclus, 62 ouverts, 1 partiel | E | PROOF_SKELETON_C2.md:3 [G]
- [BORNE] relance du 07/10 : 713 représentants y1 / 25 réseaux, 2 419 830 paires ; 28 réseaux d'anciennes méthodes : 27 acceptés (1 168 349 paires), 17 sans paire restante par les seuls lemmes | E | HANDOFF:1046-1052 [G]
- [BORNE] enveloppe impaire unimodulaire de rang 24, min ≥ 2 : 48 + r caractéristiques de norme 8 ; 4 096 vecteurs de norme 3 (N3 = 4096) | P | BILAN_AUDIT_INDEPENDANT_0836 ; FINAL_STATEMENT H3 [H]
- [BORNE] moments : M_χ = (16 + r)I − 8R ; M_coque3 = (512 + 2r)I − 24R ; M_shadow = (4 + r/4)I − 2R ; |L(u)| = r/4 − u·Ru | P | BILAN_0836 ; COUPE_CONGRUENCE_RACINES.md [H]
- [BORNE] N_max : rang 22, det 49 ; [N_max : réseau du repère] ∈ {1, 7} ; min N* ≥ 8/7 ; contrôle Golay : min dual ≥ 10/7, min caractéristique ≥ 10, 704 vecteurs de norme 3 | P/C | BILAN_ATTAQUE_GLOBALE §1, §4 [H]
- [BORNE] w = Σh/2 : w² = 7, (w,h_c) = 2, (w,u) ∈ {−1, 0} ; complément physique de rang 15, det 2^12·7^(22−g) | P | TROISIEME_VECTEUR_NORME7.md ; COMPLEMENT_PHYSIQUE_RANG15.md [H]
- [BORNE] A33 : 400 directions de torsion, 17 classes (groupe d'ordre 72), 388 éliminées, r0 ≤ 1 ; norme 10 : m² − 17m + 62 ≥ 0 requis (faux pour m = 6..11) ; trois profils à six blocs | C | sol RAPPORTS [H]
- [BORNE] g⁻ = 16 : C12 (3 326 appariements, 362 classes), C6 ⊔ C6 (3 328, 79 classes) ; 441 types d'étoiles | C | DOSSIER_G16_PRISME.md ; git 89738b9 [H]
- [BORNE] vecteur forcé : il existe v ∉ J avec E(v) ≤ 12 (≤ 15 sans condition d'ombre) ; espace de formes : dimension 61 (fin : 80) ; dimensions 15, 11, 7, 3, 1 pour T = 8..12 | P | NOTE_MISSION:20-57 [I]
- [BORNE] région : n11 ≤ 56, n11 + s ≤ 96, n11 ≤ 4 + s/2, s = 12 + N2 ; plages flottantes : E = 11 entre 0 et 34,7 paires ; E = 12 entre 0 et 52 ; E = 13 ≥ 16 ; ombres E = 11,5 entre 12 et 96 ; vecteurs de norme 3 de N entre 592 et 696 ; racines de N entre 0 et 84 | P/H | NOTE_MISSION:62-66,125 [I]
- [BORNE] T22/T24 : pour k = e = 0, 33 → 23 graphes (E = 11), 205 → 168 (E = 12) après la règle de norme duale ; graphes B : 2, 3, 6, 33, 211 classes pour E = 8..12 ; k pair, k ≤ 2E/5 ; entrées dans {0, ±1} pour E ≤ 12 | P/E | LEMMAS_AGENT_REPORT §0 [I]
- [BORNE] E = 11 : ~5·10^7 bases (contre 615 405 dans T20) ; arbre médian 22 nœuds | H | SOUNDING_E11:5-12 [I]
- [BORNE] statistiques : 600 910 595 paires ordonnées (135 réseaux) ; 2 652 paires sans témoin dans 11 réseaux, 1 042 de région ; 17 des 28 anciens réseaux sans paire restante | E | KILL_STATISTICS §0 ; REGION_PAIRS §0 [I]
- [BORNE] article : recherches ~2,6·10^7 paires sur un seul programme ; transferts 4 163 099 paires dont ≤ 2 479 669 hors Corollaire 7.3 | E | AUDIT_ORDER2_PAPER §3 [I]
- [BORNE] srg(243,22,1,2) connus : 4, |Aut| = 3 849 120, 4 320, 864, 3 888 ; grilles 1485/405/621/837 ; prismes 8910/2430/4158/5670 ; hexagones induits 4 980 690 … | E | AUDIT_V7 §2 [I]
- [BORNE] mots binaires de ker7(A + 4I) : poids ∈ {0, 63, 77} | P | code7 THEOREME [I]

### 8.3 Lemmes ouverts et étapes manquantes (31)

- [LEMME-OUVERT] décider Stage Q (énumération des matrices Q_out à équivalence près) | branche C2 | si zéro, branche close sans signes | dossier_chercheurs_fr.tex:419-421 [A]
- [LEMME-OUVERT] forme de Smith 7-adique de S − 3I et Q − 3I, lien avec le 7-rang de A − 3I | branche C2 | seul invariant p-adique non épuisé | dossier:427-429 [A]
- [LEMME-OUVERT] MacWilliams sur les codes LCD [42,20] ⊂ (col Nb)^⊥ | branche C2 | obstruction purement mod 2 | dossier:431-433 [A]
- [LEMME-OUVERT] version « forme quadratique / réseau libre Z2[C2] » de l'identité trace-rang d'Ishida utilisant D | branche C2 | exclusion sans ordinateur | dossier:439-441 [A]
- [LEMME-OUVERT] valeur exacte de φ_u(R) (lemme 11.2) / carrés disjoints | C2 « familles » | fermerait le type dis | MATH_C2_PROGRAMME.md:194,1114 [B]
- [LEMME-OUVERT] levier structurel pour les mélanges à plusieurs cycles tordus | C2 « familles » | éviterait 10^4-2·10^5 PL par classe | MATH_C2_PROGRAMME.md:1112-1113 [B]
- [LEMME-OUVERT] plafond de torsion P ≥ 1152 (C1) | C1 et C2 (Théorème D′) | contradiction avec Krein P ≤ 1151 | MATH_C2_PROGRAMME.md:565-566 [B]
- [LEMME-OUVERT] version à la main des certificats H-β (argument spectral global de second ordre) | C2 | preuve sans ordinateur de H | MATH_C2_PROGRAMME.md:1038-1039 [B]
- [LEMME-OUVERT] lemme de l'étoile libre, forme locale | C2 | ferme C2 | notes/20:21-22 [C]
- [LEMME-OUVERT] tout-tordu non simple (lemme de simplicité ou q:7 dans la couche signée) | C2 (famille un bloc) | ferme T = K7 | note 45:157-158 [C]
- [LEMME-OUVERT] (2,0) contre (2,1) pour un partenaire dis ; lemme 11.2 exact | C2 (carrés dis) | ferme les AD / dis | note 41:71 [C]
- [LEMME-OUVERT] lemme nouveau sur les étiquettes dis | ligne d'arrivée (A) | terminerait la route locale | Desktop notes/46:109 [C]
- [LEMME-OUVERT] propagation (P) : une seconde réflexion automorphe | C2 « Hall en un point » | équivaut à la mort de C2 | README (labo):14-17 ; notes/14 §3 [C]
- [LEMME-OUVERT] (H) « min K* ≥ 9/7 » | chaîne PROOF_OBLIGATION_LEDGER | fermerait la chaîne à 5/7 ≤ min K* ≤ 8/7 | Desktop notes/54:5-7 [C]
- [LEMME-OUVERT] théorème qui tue toute une orbite y1 ou tout un réseau (piège moyenné, comptage des points frontière Y_z = 58, coquille partenaire) | route (C) | remplacerait le calcul paire par paire | route_c_29_09/README.md:14-26 [C]
- [LEMME-OUVERT] couverture exacte des points cible-1 expliquée structurellement (les candidats à faible t ne peuvent pas compléter un repère) | route (C) | exclusion sans calcul des paires | HANDOVER:227-228 [D]
- [LEMME-OUVERT] obstruction de réseau pour les enveloppes pauvres en racines (analogue C7 : compression de Gram, 42 vecteurs dans R^15) | route (C) | supprimerait la queue de calcul | HANDOVER:230-232 [D]
- [LEMME-OUVERT] F0 re-dérivé de façon autonome (formules de trace a = 1 + χ3 + χ4, b = 14 + 3χ3 − 4χ4 + combinatoire du sous-graphe fixe) | audit 156/156 | indépendance vis-à-vis de Makhnev–Minakova | AUDIT_156_PLAN:151-152 (fait ensuite : AUDIT_REDUCTION A.0, L02) [D]
- [LEMME-OUVERT] mixed twist doit fournir ≥ 6 vecteurs propres exacts κ-impairs de valeur 3 | chercheur 2 | contradiction si impossible | RESULTS.md:313 [D]
- [LEMME-OUVERT] langage global de compatibilité ou grammaire constructive pour le Théorème C | voie A | décider EX | ROADMAP.md:5-11 [E]
- [LEMME-OUVERT] plafond de torsion | C1 (et C2) | contradiction avec Krein | external_c1/notes/100:191-203 [F]
- [LEMME-OUVERT] cas uniforme k ≤ 28 (C1) | C1 | exclusion globale par le 7-rang | astra/RAPPORT_ASTRA_DOSSIER5.md:5 [F]
- [LEMME-OUVERT] existence d'une droite-bloc générique / d'un Q_c inversible | Astra 6 | rendrait suffisante l'exclusion de g⁻ = 18, 20 | astra/RAPPORT_ASTRA_DOSSIER6.md:13,44 [F]
- [LEMME-OUVERT] problème fini du bloc plein (preuve d'impossibilité certifiée ou solution) | « structures » pour Sol | ferme les résidus AD à g = 20 | astra/PROBLEME_BLOC_PLEIN_POUR_SOL.md:1-4 [F]
- [LEMME-OUVERT] seconde implémentation du packing (Table 1, 18 réseaux) | article §9 | indépendance du calcul | HANDOFF:1028-1030 [G]
- [LEMME-OUVERT] preuve sans ordinateur de C2 (optionnelle, dernière) | utilisateur (07/10) | | HANDOFF:1007-1012 [G]
- [LEMME-OUVERT] fermeture globale de g⁻ = 18 et g⁻ = 20 (avant la route C) | Sol/Astra | pas d'involution | LIRE_D_ABORD_POUR_CLAUDE.md [H]
- [LEMME-OUVERT] régimes 0/2/4 fractionnaires de D6^4 ; enveloppes sans racines ; normes 9/10 à six et sept blocs | Sol/Astra | familles d'enveloppes | LIRE_D_ABORD (NOUVEAUTES) ; CAMPAGNES_A33 table [H]
- [LEMME-OUVERT] T22, T24 (E = 11, 12) par un argument uniforme en E | mission C2 sans calcul | supprimerait les 156 réseaux | NOTE_MISSION:77-79 [I]
- [LEMME-OUVERT] condition forcée par le repère sur la table des coefficients, violée par les paires réelles de min E ≥ 11 | mission | idem | NOTE_MISSION:80-81 [I]
- [LEMME-OUVERT] raison uniforme de l'absence d'heptade | mission | exclusion des paires de région | git 194a3301 [I]

### 8.4 Méthodes transférables d'un cas à un autre (31)

- [TRANSFERT] modèle d'orbites de l'involution (k = 2m) → srg(243,22,1,2) (m = 11, BvLS, x ↦ −x) comme contrôle positif fort ; plus généralement toute la famille srg(2m²+1, 2m, 1, 2) | dit par la source | AUDIT_2026-09-22.md:17-22 [A]
- [TRANSFERT] identité trace-rang d'Ishida (exclut les involutions du graphe de Moore manquant) → involution de Conway : redonne seulement a1(t) = 14 | dit par la source | dossier:439 ; NOTE:18 [A]
- [TRANSFERT] spectre de quotient de l'ordre 3 sans point fixe {14, 3^18, (−4)^14} (a1(g) = 18 ⇒ χ3 = 0, χ−4 = −1) : même méthode que pour C2 | dit par la source | DEEP_THOUGHT:38-39 [A]
- [TRANSFERT] matrices d'orbites à la Behbahani–Lam (p = 3, 5, 7, 11) → p = 2 (Stage Q) | dit par la source | dossier:419-421 [A]
- [TRANSFERT] compression de Gram (C7 : 12 vecteurs dans R^4) → C2 : 42 vecteurs dans R^15 | dit par la source (HANDOVER 04/10) | conway-C7:main:README.md:25-27 ; work/HANDOVER_2026-10-04.md:231-232 [B]
- [TRANSFERT] méthode C3 (deux spécialisations, discriminant) → C2 : échoue (tautologie) ; raison structurelle donnée | dit par la source | MATH_C2_PROGRAMME.md:674-743 ; NOTE_arith.md:42-50 [B]
- [TRANSFERT] Théorème D′ (sans involution) et L8 de C1 : même énoncé ; Théorème A et lemme 9.1 valent pour tout srg(99,14,1,2), donc pour C1 | vu par moi + crédit de la source | MATH_C2_PROGRAMME.md:38,153-156,553,562-563 [B]
- [TRANSFERT] identité d'orbite Q² + Q = (k − 2)I + 4J − Sh valable pour tout k = 2m (contrôles m = 2, 11) | dit par la source | MATH_C2_PROGRAMME.md:1084-1086 [B]
- [TRANSFERT] règle de cohérence : tout lemme général doit être vrai pour m = 2 et m = 11 (Paley 9, BvLS) ; une contradiction à m = 7 doit utiliser θ − τ = 7 | dit par la source | MATH_C2_PROGRAMME.md:4-7 [B]
- [TRANSFERT] G1 et S1 valent pour tout srg(99,14,1,2) (C1) ; « P ≥ 6N » et la chaîne DRAT/Docker de C2 proposés à C1 | dit par la source | revue:193-207 [C]
- [TRANSFERT] méthode C3 (deux spécialisations) → C2 : vide ; cohomologie du complexe des couplages (allsib) → carrés one/dis (« cocycle à défauts ») | dit par la source | SYNTHESE:43-45 ; revue:68 [C]
- [TRANSFERT] Akiyama (srg(266,45,0,9) exclu via un réseau de Niemeier, Lean) → Conway : défavorable (exige un repère épais), mais précurseur des enveloppes de rang 24 | dit par la source + vu par moi | notes/external_bridges/B07_akiyama_niemeier.md:1-5 [C]
- [TRANSFERT] contrôles positifs Paley(9) (m = 2) et BvLS (m = 11) pour tout lemme général ; témoins de diamètre 3 de C1 (20 et 42 sommets) ne réfutent que les formes locales | dit par la source | Desktop annexe D, errata E1 [C]
- [TRANSFERT] identité générale (★) sur un ensemble de blocs (note 43) et identité sur un ensemble de paires (note 44 : Σ écarts² = 28|𝒫|² − 28Σd_c² + 84|𝒫| − 14E_L) : valables hors involution ? (à vérifier) | vu par moi | notes/43:52-59 ; notes/44:49-56 [C]
- [TRANSFERT] compression de Gram de C7 → enveloppes de C2 | dit par la source | HANDOVER:231-232 [D]
- [TRANSFERT] identité de packing de C1 (norme 3) → normes 7 et 4 et asymétrie des cosets | dit par la source | HANDOVER:170-171 [D]
- [TRANSFERT] BvLS (m = 11) n'est PAS un banc d'essai pour les énoncés qui utilisent 2(2m − 4) = (m − 2)(m − 3) ou C(m,2) − 1 (vrais seulement à m = 7) | dit par la source | RESULTS.md:256-258 [D]
- [TRANSFERT] méthode « Constructeur / Destructeur aveugles » et protocole de duplication | dit par la source | agents/PROVENANCE_LOG.md [D]
- [TRANSFERT] la méthode de complétion exacte T4 (relaxation réelle intégrale) valable « pour toute famille normalisée » ? — la note ternaire donne une « general normalized-family version » du lemme de résidu borné | dit par la source | archive/TERNARY_PROOF.md (§2, « General normalized-family version ») [E]
- [TRANSFERT] critère 2-adique S5 (discriminant mod 4) → toute la table de Brouwer (exclut 35 paramètres ouverts) | dit par la source | NOTE_S5:1-7 [F]
- [TRANSFERT] identité d'orbite Q² + Q = 12I + 4J − Sh sans symétrie sur les 42 « cellules antipodales » (adoptée par C1) | dit par la source | REGISTRE:27 [F]
- [TRANSFERT] équilibre de la queue vérifié en forme générale sur BvLS (valable dans toute la famille) | dit par la source | REGISTRE:15 [F]
- [TRANSFERT] lemme de Witt général (structures → C1 : g⁻ ≠ 16) | dit par la source | JOURNAL:825-827 [F]
- [TRANSFERT] contrôle positif « pauvre en racines » (O24, A2^8) → interdit toute obstruction convexe universelle dans les enveloppes pauvres en racines | dit par la source | shell_theorems/README.md:21 ; fractional_proof/PROOF.md:5 [G]
- [TRANSFERT] précédents Lean du projet (conway-C7, conway99-c3-experimental) → formalisation de C2 (théorème conditionnel nommé, A.0, Corollaire Y1, 143) | dit par la source | HANDOFF:1007-1012 [G]
- [TRANSFERT] contrôles positifs H(2,3) (m = 2) et BvLS (m = 11) conservés pour toute la théorie des enveloppes (constantes 3/9, normes u = 1/4, h = 2/5) | dit par la source | BILAN_1031 « Provenance » [H]
- [TRANSFERT] genre / Witt (signe du résidu) : méthode qui a fermé A33 → lemme de Witt général transmis à C1 (g⁻ ≠ 16) | dit par la source | sol RAPPORT ; structures JOURNAL:825 [H]
- [TRANSFERT] séries thêta / formes de Jacobi (représentation de Weil de A2 + A7) → toute la route (C) (un vecteur court forcé sans liste de réseaux) ; « garde-fou : le même système avec 7 remplacé par 2 ou 11 a des solutions, donc un argument valide doit utiliser 7 » | dit par la source | NOTE_MISSION:3-6 [I]
- [TRANSFERT] identités de comptage L1-L5 uniformes en E (8 ≤ E ≤ 12) contrôlées sur le graphe à 243 sommets | dit par la source | LEMMAS_AGENT_REPORT §0, §10 [I]
- [TRANSFERT] partages réguliers / revêtements de Brouwer–Haemers (243) → question de l'asymétrie pour 99 (C1) | dit par la source | THEOREM_Z3_COVERS (corollaire) [I]
- [TRANSFERT] mots binaires mod 7 et cocliques de Hoffman (C1) → lien avec la campagne cocliques/Hoffman du lot C1 | vu par moi | code7 THEOREME [I]

