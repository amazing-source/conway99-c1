# Lot L07_C1_asym_local : C1, asymétrie, constructions λ = 1, lois locales à étoiles (13-18/10/2026)

Fiche du chantier du 20/10/2026, rédigée selon `work/chantier_2026-10-20/CONSIGNES_AGENTS.md`. Les fichiers
compagnons sont `fiches/L07_C1_asym_local.jsonl`, avec une ligne par résultat (identifiants `L07_C1_asym_local-NNN`).

**Conventions de chemins.**
- `work/...` désigne `C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\...` (espace du chercheur 2, notes LAB).
- `Desktop/Recherche_Conway/...` ou `C:/home/researcher/Desktop/Recherche_Conway/...` désigne le dossier Recherche_Conway. On y trouve le dépôt de Codex `c1-asymmetry-audit` et les messages du pont `lab_exchange_2026-10-14`.
- `conway99-c1:<branche>:<chemin>` désigne le dépôt git `C:\Users\RESEARCHER\cw\conway99-c1`.
- `C:/home/researcher/cw/strongly-regular-graphs-research:main:<chemin>` désigne le dépôt public.
- Lignes = numérotation `cat -n` du fichier cité.

**Qui a lu quoi.** Le lot compte 356 entrées d'inventaire.
- J'ai lu moi-même les notes LAB (index 15-67, 91-108, 202-205), les branches v7 et astra (notes 155-178, dossiers externes), les premiers documents C1, les articles et les dépôts srg.
- Trois sous-agents ont lu le reste (« sous-lots ») :
  - A = messages du pont Codex → LAB ;
  - B1 = journal de nuit et notes du 18/10 de Codex ;
  - B2 = autres notes de c1-asymmetry-audit et AGENTS.md.

  Leurs entrées gardent l'étiquette du sous-lot au début du champ `remarques`.
- Les statuts sont recopiés des sources, jamais rehaussés.
- La couverture complète, index par index, est au §9.

## 1. Résumé

1. **Bilan.** Aucun résultat du lot n'exclut le graphe ni le cas C1. On a :
   - des réductions prouvées à la main (P), dont aucune n'a été relue par un humain ;
   - de nombreuses vérifications exactes ;
   - des verdicts de solveur sans certificat.
2. **Levier d'asymétrie.** Le principe de symétrie forcée (lemme d'extension) est énoncé le 11/10 (note 171) et retrouvé par LAB le 14/10. Avec Aut = 1, il donne au moins 99 × 645 120 complétions étiquetées du cadre d'un sommet.
   - La fenêtre est fermée aux ordres 1 et 2 : théorème du flip, théorème de majorité de Codex.
   - Il manquerait une borne supérieure du nombre de solutions, et aucune n'est en vue.
3. **Construction λ = 1.** Un srg(378,52,1,8) avec |Aut| = 6 a été construit.
   - Rigidité : le critère de concentration est prouvé.
   - Pas de 3-ovoïde dans GQ(8,10), par l'obstruction de parité de Codex.
   - Toutes les routes structurées vers un λ = 1 asymétrique sont bloquées.
4. **Lois à quatre étoiles.**
   - Une quinzaine de lois locales tirées des données sont réfutées par des témoins exacts : (H3), (H4), (A), (A4), plafonds de relations mixtes, (N9), (NOGRID), (LOW), (R7), ODD9, SUM14, KER-SYM universelle.
   - Restent prouvées, en implications seulement : (H-MATCH) ⇒ pas de Conway, et G18 ; (N9-NG), (NG5) ou (NG7) ⇒ pas de Conway ; (T8)/(T15) ⇒ pas de Conway.
   - Ces lois sont toutes OUVERTES.
5. **16/10 : aucun germe connu à quatre étoiles ne s'étend.**
   - DISC tue les 645 germes de rang 30, et aucun n'admet de colonne extérieure.
   - Aucune cinquième étoile n'est possible sur les 34 bases. Pour la base HB, c'est certifié par DRAT.
   - Les populations qui soutenaient (H-MATCH) ne sont donc pas des blocs de Conway.
   - R7 est SAT, alors que R8 et le problème à cinq étoiles restent indécis ; R8 UNSAT exclurait Conway.
6. **Codex, 18/10 (sous-lot B1).**
   - Certificat entier 3P + 4G ≤ 2772 (C).
   - La branche « toute droite a c ≥ 4 » est fermée (S).
   - Plusieurs verdicts sont retirés à cause du bug OR-Tools 9.15 (X).
7. **Nuit des 13-14/10, sans anciennes notes.**
   - rang_F7(A + 4I) ≥ 35 (C), redécouverte plus faible de la fenêtre {37, …, 43}.
   - T1 redécouvre L8.
   - Seul le théorème N9 (aucun 9-ensemble à 17 arêtes) est nouveau.
8. **Principales contradictions** (§6) :
   - attribution de la route Ω ;
   - borne « N ≤ 9 grilles disjointes » ;
   - formulations de la chaîne de littérature ;
   - comptes 643/645 ;
   - conclusions de calibration srg(243) retirées ;
   - phrase « aucune combinaison ne peut exclure Conway », retirée.

## 2. Chronologie (UTC sauf mention ; Codex écrit en heure de Paris)

- **24-26/09.** Journal et rapport C1 : lemmes L1-L25, notes 00-129. La synthèse de la note 100 dit : « tous des planchers ». L8 est démontré à la main le 25/09. Le 25/09, l'utilisateur gèle les solveurs (`conway99-c1:origin/main:JOURNAL.md:3-608` ; `Desktop/Recherche_Conway/c1-asymmetry-audit/rapport/RAPPORT_C1.md`).
- **06-07/10, session Claude cloud (notes 155-164).**
  - Classes mod 7 et germes (V7).
  - Pas de « route (C) » pour C1 : la masse de rang 48 vaut ≈ 1,5·10¹²¹.
  - Route Ω complète, avec l'équivalence (★) : Γ 12-régulier sur les 84 labels et T² = 7T.
  - Second srg(243,22,1,2), tordu (réfute Reimbayev).
  - L'étage colonnes coûte ≥ 1,7·10¹⁰ h CPU.
  - Inventaire des 12 dépôts (note 162).
  - Le 07/10 à 17:47 UTC, C2 est à 156/156 ; avec C3 et C7, « C1 est tout le problème ».
  - Articles rank7, s5_2adic, srg243_second et la note « asymmetric » (07/10).
- **08-09/10.** Session portable : au rang 37, une droite de maille ≥ 5 a un graphe connexe (E, non audité).
- **11/10, notes 165-171 (branches astra et v7).**
  - Revêtements de BH ; Γ₃ (|Aut| 864) et Γ₄ (3888).
  - Pas d'étalement régulier à 99.
  - Sous-cas (A) : 11 grilles disjointes.
  - Alignement total impossible à 99 ; tout graphe de (A) est déséquilibré.
  - Dossiers externes Paley(25), BvLS et Hoffman α = 22 (ChatGPT/Astra).
  - **Lemme d'extension** (note 171 §7).
  - Cubes α = 22 mis en pause à 22:15 UTC sans verdict.
  - Dépôt public srg-research (Zenodo).
- **12/10, notes 172-178.**
  - Réseau Q pour α = 22 : aucune obstruction de discriminant.
  - Conjecture K7.
  - Emboîtements de la famille.
  - Question S3 à 243.
  - F_x et B_xa.
  - Mots binaires de ker₇(A + 4I).
  - Les dossiers externes sont versés au dépôt.
- **13/10 (LAB).** Cadre coclique : il ne ferme C1 qu'avec α ≥ 21. Cocliques de taille 45 à 243.
- **13-14/10, nuit (LAB, « en avant seulement »).**
  - F1-F5.
  - T1 : aucun point localement affine.
  - kk6 ; kk5 certifié DRAT.
  - Théorème N9.
  - Programme thêta exact : rang_F7(A + 4I) ≥ 35.
  - Famille SPREAD.
  - Codex mène en parallèle le même type de nuit (sous-lot B1).
- **14/10, 10:40-12:30.** Campagne Paley 9 / 25 : loi des deux-graphes, GM, torsion, principe de symétrie forcée, lemme du flip. Le contrôle de nouveauté de 11:45 conclut « surtout une redécouverte ».
- **14/10, 13:00-16:15.** Construction λ = 1 : 378 avec |Aut| = 6, critère de concentration, 3-ovoïdes. SAT enraciné : calibrations UNSAT sur (57,14,1,4) et (51,10,1,2). Tout est arrêté à 15:18 UTC, et la campagne est gelée par l'utilisateur à 16:10.
- **14/10, vers 16:00-20:00.** Fenêtre d'asymétrie : théorème du flip, majorité de Codex, second ordre fermé. Objet à 49 sommets (route Ω à étoiles).
- **14/10, 20:55 → 15/10, 02:38.** Réfutations exactes : (A) à 20:55, (H4) à 21:12, (A4) à 23:30, (N9) et (NOGRID) à 01:14, (R7) à 01:22, (LOW) à 02:01. On obtient 331 objets de rang 30, tous tués par DISC. Bilan à 10:11.
- **15/10, 02:50-08:00.**
  - Audit de tous les énoncés d'exclusion, relu par un agent adversarial à 04:20.
  - Réduction (H-MATCH) ⇒ pas de Conway à 06:00, relue à 06:45.
  - Calibration srg(243) corrigée à 08:00.
- **15/10, 08:45-17:57.**
  - Tâche T3 : G21, 287 classes de noyaux, mur de 13 dû à une fausse symétrie, <Z5, hM> complète.
  - Mécanisme A.
  - **ODD9 réfutée à 17:05** ; SUM14 réfutée.
- **15/10, 18:30-21:30.** Les trois résultats L1, L8, ρ. Cible (N9-NG), avec (NG5) et (NG7) de Codex. Tentative de preuve R1-R6.
- **16/10, 02:40-08:00.** Cible unique (H-MATCH) : 416 classes, environ 1,14 M structures, aucune structure cassée de nullité ≥ 14. Verdict : la route locale est épuisée.
- **16/10, 08:00-19:00.**
  - EXT84 : DISC sur 645 germes, colonnes vides, cinquième étoile infaisable (DRAT pour HB), lemme h5.
  - Revue globale envoyée.
  - Correction de l'encodage CP-SAT.
  - R7 SAT, R8 indécis ; runs de 2 h lancés à 17:05.
- **16-18/10, Codex (sous-lots A, B1, B2).**
  - Critère global sur 84 labels, cadres à 15 lignes, couverture 79 gabarits.
  - 18/10 : bug OR-Tools et retraits, certificat 3P + 4G ≤ 2772, racine pondérée, branche c ≥ 4 fermée (S), réduction de la petite droite à 8 positions.
- **20/10.** NOTE_R8_ROUTE (lot L08, lue l.1-60 seulement) : le modèle R8 est solide, mais son coût n'est pas réaliste.

## 3. Table des résultats

Elle est générée à partir du JSONL. Colonne id : abréviation de `L07_C1_asym_local-NNN`. Plages : 001-148 = lot principal, lu par moi ; 149-284 = sous-lot B1 ; 285-399 = sous-lot A ; 400-484 = sous-lot B2. Statuts : P preuve écrite, C calcul exact certifié, E calcul exact sans certificat, S solveur sans certificat, H indice, O ouvert, R réfuté, X retiré. Les relectures et les portées exactes sont dans le JSONL (`relu_par`, `enonce`, `remarques`).

| id | énoncé court | statut | source principale |
|---|---|---|---|
| 001 | Le cadre coclique (22 et 21) ne ferme C1 qu'avec alpha >= 21 | P | work/c1_coclique_frame_2026-10-13/NOTE_COCLIQUE_FRAME.md:5-11 |
| 002 | Cocliques de Hoffman (taille 45) dans la famille srg(243,22,1,2) : exactement absentes du twin et de Gamma5 | E | work/c1_coclique_frame_2026-10-13/NOTE_COCLIQUE_FRAME.md:13-31 |
| 003 | Cocliques de taille 45 absentes de Gamma3, Gamma4, 6e, 7e, 8e graphe srg(243) (MILP flottant) | S | work/c1_coclique_frame_2026-10-13/NOTE_COCLIQUE_FRAME.md:20-34 |
| 004 | Rangs modulaires des huit srg(243,22,1,2) | E | work/c1_coclique_frame_2026-10-13/NOTE_COCLIQUE_FRAME.md:35 |
| 005 | Le theoreme d'elimination V6 de Codex ne se transpose pas mot pour mot au support de norme 18 | P | work/c1_coclique_frame_2026-10-13/NOTE_COCLIQUE_FRAME.md:53-59 |
| 006 | Banc d'essai norme 18 a 243 : vecteur propre {-1,0,1} de norme 30 pour -5 dans BvLS | E | work/c1_coclique_frame_2026-10-13/NOTE_COCLIQUE_FRAME.md:60-63 |
| 007 | Loi de second niveau dans la branche propre du monde norme 18 | P | work/c1_coclique_frame_2026-10-13/NOTE_COCLIQUE_FRAME.md:64-70 |
| 008 | Identites des droites (F1-F3) et nombre de prismes d'une droite | P | work/c1_night_2026-10-14/NOTE_NIGHT.md:12-31 |
| 009 | Le reseau des droites M est pair, de rang 44, avec 21 M* inclus dans M ; une grille 3x3 induite est un code parfait | P | work/c1_night_2026-10-14/NOTE_NIGHT.md:33-45 |
| 010 | Borne cubique de Codex sur les prismes : pbar <= 588/59, P <= 1151 | P | work/c1_night_2026-10-14/NOTE_NIGHT.md:101-108 |
| 011 | Moments de degre 4, 5 et moments mixtes : aucun gain sur la borne de degre 3 | E | work/c1_night_2026-10-14/NOTE_NIGHT.md:146-155 |
| 012 | T1 : aucun sommet n'est localement affine (aucun sommet sur 21 grilles) | S | work/c1_night_2026-10-14/NOTE_NIGHT.md:61-84 |
| 013 | kk6 : aucun sommet n'a six droites engendrant deux a deux des grilles | S | work/c1_night_2026-10-14/NOTE_NIGHT.md:167-172 |
| 014 | kk5 : cinq droites deux a deux en grille forcent la grille sur les deux autres (K_5 force l'arete opposee) | C | work/c1_night_2026-10-14/NOTE_NIGHT.md:239-247 |
| 015 | Types locaux aleatoires non refutes : 'choisir les 14 couplages puis appeler le solveur' n'est pas une recherche complete abordable | H | work/c1_night_2026-10-14/NOTE_NIGHT.md:223-237 |
| 016 | Equation du graphe exterieur : A_out^2 + A_out = 10I + 2J - L | P | work/c1_night_2026-10-14/NOTE_NIGHT.md:174-198 |
| 017 | Theoreme N9 (nuit) : aucun ensemble de 9 sommets ne porte exactement 17 aretes | P | work/c1_night_2026-10-14/NOTE_NIGHT.md:256-313 |
| 018 | Bornes e(S) pour s = 3..10 sommets | P | work/c1_night_2026-10-14/NOTE_NIGHT.md:310-313 |
| 019 | Famille SPREAD (sommets = 11 grilles disjointes) : cas abelien impossible, cas general ouvert | P | work/c1_night_2026-10-14/NOTE_NIGHT.md:329-348 |
| 020 | Reseaux A, B des droites et 7-rang : b + 1 = rang_F7(A + 4I), b pair, b != 44, theta dans M_22(Gamma_0(7)) | P | work/c1_night_2026-10-14/NOTE_NIGHT.md:350-372 |
| 021 | Bornes de couches du reseau des droites (lignes, co-Heawood, norme 16) | P | work/c1_night_2026-10-14/NOTE_NIGHT.md:373-384 |
| 022 | Theoremes de rang de la nuit : rang_F7(A + 4I) impair et >= 35 (b >= 34) | C | work/c1_night_2026-10-14/NOTE_NIGHT.md:385-401 |
| 023 | Vecteurs courts forces pour les rangs restants | E | work/c1_night_2026-10-14/NOTE_NIGHT.md:398-400 |
| 024 | Route a_4 pour b = 34 : fermee | E | work/c1_night_2026-10-14/NOTE_NIGHT.md:548-561 |
| 025 | Apports de Codex pendant la nuit (non re-derives sauf mention) | P | work/c1_night_2026-10-14/NOTE_NIGHT.md:585-601 |
| 026 | Groupes exacts : srg(9,4,1,2) unique (/Aut/ 72) ; 15 srg(25,12,5,6) dont 2 asymetriques ; 10 srg(26,10,3,4) dont 1 asymetrique | E | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:19-42 |
| 027 | Loi des deux-graphes : un membre conference est asymetrique ssi c'est le descendant en un point d'une orbite reguliere du groupe de son deux-graphe | E | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:44-58 |
| 028 | Commutations de Godsil-McKay a 25 : la stabilisation de l'ensemble de commutation est le groupe commun ; Paley 25 n'a pas d'ensemble de taille 4 | E | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:60-66 |
| 029 | Torsion contre symetrie dans la famille (1,2) a 243 | E | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:68-84 |
| 030 | A 243 les echanges (trades) gardent le stabilisateur de l'echange ; le twin = BvLS commute en une droite (Aut = Stab(L), 4320) | E | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:138-170 |
| 031 | Donnees de premier ordre F_x contre stabilisateur de sommet a 243 | E | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:172-186 |
| 032 | Principe de symetrie forcee (lemme d'extension) : une piece H d'un graphe asymetrique a au moins /Aut(H)/ completions | P | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:188-195 |
| 033 | Aucun ensemble de commutation de Godsil-McKay (une classe, toute taille) dans srg(v,k,1,2) pour k >= 14 | P | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:197-211 |
| 034 | Pourquoi Paley 9 est force (preuve combinatoire) | P | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:213-219 |
| 035 | Confrontation avec Conway : un Conway asymetrique serait un 'orphelin' | P | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:86-95 |
| 036 | Lemme du flip (s_l automorphisme de F_x ssi droite plate et pi_a = pi_a') | P | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:261-287 |
| 037 | Proposition (a) : les couplages en un sommet determinent-ils un srg(243,22,1,2) ? Non lancee | O | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:289-299 |
| 038 | Variante de Codex : ensembles conserves irreguliers dans le bloc 0 du 6e graphe a 243 : tout se reconstruit en les sept graphes connus | E | work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:301-321 |
| 039 | Lemme d'eigen-rigidite (forme srg de la reconstruction par complement d'etoile) | P | work/asym_window_2026-10-14/NOTE_ASYM_WINDOW.md:19-28 |
| 040 | La fenetre d'asymetrie : le cadre Phi_x a un deficit de 30 dimensions ; un Conway donne au moins 99 x 645 120 completions etiquetees du cadre | P | work/asym_window_2026-10-14/NOTE_ASYM_WINDOW.md:30-56 |
| 041 | Proposition 1 : Paley 9, symetrie forcee par rigidite (raison spectrale) | P | work/asym_window_2026-10-14/NOTE_ASYM_WINDOW.md:49-52 |
| 042 | Theoreme du flip : pour m >= 3 aucun flip s_l n'est un automorphisme de srg(2m^2+1, 2m, 1, 2) | P | work/asym_window_2026-10-14/NOTE_ASYM_WINDOW.md:58-84 |
| 043 | Theoreme de majorite (Codex) : un automorphisme fixant x et ses droites qui en retourne q > 0 en retourne au moins ceil(t/2) | P | work/asym_window_2026-10-14/NOTE_ASYM_WINDOW.md:113-120 |
| 044 | Second ordre : les trois points d'une droite (deficit 8) ; une droite plus une etoile atteint le rang plein 44 ; la symetrie forcee meurt au premier recollement | P | work/asym_window_2026-10-14/NOTE_ASYM_WINDOW.md:122-144 |
| 045 | Ce qui reste du levier d'asymetrie : l'ABONDANCE ; une exclusion de C1 demande une borne superieure de solutions sous l'ordre du groupe | H | work/asym_window_2026-10-14/NOTE_ASYM_WINDOW.md:101-109 |
| 046 | Lemme des 99 squelettes distincts | P | work/asym_window_2026-10-14/NOTE_ASYM_WINDOW.md:86-96 |
| 047 | Paysage des srg a lambda = 1 (v <= 1300, tables de Brouwer) | H | work/lambda1_construction_2026-10-14/NOTE_LAMBDA1.md:7-17 |
| 048 | Graphe srg(378,52,1,8) construit avec /Aut/ = 6 exactement (le lambda = 1 le moins symetrique connu) | E | work/lambda1_construction_2026-10-14/NOTE_LAMBDA1.md:19-31 |
| 049 | Echanges sur le graphe 378 a groupe S3 : completion unique jusqu'a 229 sommets liberes | E | work/lambda1_construction_2026-10-14/NOTE_LAMBDA1.md:33-43 |
| 050 | Critere de concentration (rigidite des echanges, tout srg) | P | work/lambda1_construction_2026-10-14/NOTE_LAMBDA1.md:45-75 |
| 051 | Unification : les deux familles lambda = 1 a plusieurs membres sont des 3-ovoides de quadrangles generalises | P | work/lambda1_construction_2026-10-14/NOTE_LAMBDA1.md:77-89 |
| 052 | Obstruction de parite (Codex, verifiee par LAB) : le GQ(8,10) P(W(9),x0) n'a aucun 3-ovoide | P | work/lambda1_construction_2026-10-14/NOTE_LAMBDA1.md:91-101 |
| 053 | Modele SAT enracine pour srg(v,k,1,mu) : calibrations UNSAT, aucun verdict sur Conway, (115,18,1,3) ni (51,10,1,2) sans coupe | S | work/lambda1_construction_2026-10-14/NOTE_LAMBDA1.md:103-124 |
| 054 | Coupe de symetrie W(B7) sur le modele enracine complet : nouvelle dans le projet, partielle, gain non mesure | H | work/lambda1_construction_2026-10-14/SB_NOVELTY_CHECK.md:1-44 |
| 055 | Filtres issus de l'asymetrie pour la reprise du solveur (non testes) | P | work/lambda1_construction_2026-10-14/SOLVER_CAMPAIGN_STATE.md:68-82 |
| 056 | Rigidite des srg a lambda = 1 : explication par selection (aucun des trois mecanismes d'asymetrie n'opere) | P | work/lambda1_construction_2026-10-14/RIGIDITY_LAMBDA1.md:29-56 |
| 057 | Vecteurs propres les plus courts = vecteurs de paires ; pas d'echange de rang 2 sur un vecteur {0,+-1} dans Conway | P | work/lambda1_construction_2026-10-14/RIGIDITY_LAMBDA1.md:67-112 |
| 058 | Symetrie par rarete : les lambda = 1 connus sont symetriques car leur probleme hote a moins de solutions que de symetries | E | work/lambda1_construction_2026-10-14/RIGIDITY_LAMBDA1.md:114-138 |
| 059 | Objets a etoiles en un sommet : T = 3I - Gamma - K verifie T^2 = 7T (rang 30) ; U = 7 Pi - T >= 0 ; forme spectrale (Haynsworth) | P | work/stars_rank_2026-10-14/NOTE_STARS_RANK.md:6-15 |
| 060 | Droites speciales : rang T_X = 23 - c(l) ; special ssi H_l deconnecte ssi lambda_2(H_l) = 3 ; rang N_l = 35 - c(l) | P | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:15-22 |
| 061 | Configurations fermees (P4), symetrie (P5), lemme de la grille, grilles = codes parfaits (P11), code binaire (P12) | P | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:23-34 |
| 062 | Niveaux d'etoiles : trois etoiles tres selectives mais satisfiables ; relaxation continue faisable (T0 = 3 Pi) | E | work/stars_rank_2026-10-14/NOTE_STARS_RANK.md:17-37 |
| 063 | (H3) 'trois etoiles, positivite, rang 30 => grille sur (l,m)' : REFUTEE | R | work/stars_rank_2026-10-14/NOTE_STARS_RANK.md:78-82 |
| 064 | (H4) 'aucune structure a quatre etoiles n'est PSD' : REFUTEE | R | work/stars_rank_2026-10-14/NOTE_STARS_RANK.md:83-98 |
| 065 | (A) 'trois etoiles, T, U >= 0 et c(l) = 1 => rang 31' : REFUTEE (52 contre-exemples exacts) | R | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:119-147 |
| 066 | Relations mixtes (P6) et identite exacte G9 : rang T_S4 = 30 - delta ; mixtes = 12 - c(l) - c(m) + [grille] + delta | P | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:35-40 |
| 067 | Relations binaires a trois etoiles (session ChatGPT montree par l'utilisateur, re-verifiee par LAB) | P | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:90-104 |
| 068 | Identite des etoiles partielles a quatre etoiles : D T D^T = 6I + 2(J - Mt) - E | P | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:137-142 |
| 069 | Temoin E1 : le niveau a quatre etoiles SEUL est satisfiable (T >= 0 de rang exactement 30, U >= 0 de rang 40) ; il n'est dans aucun Conway | C | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:243-253 |
| 070 | DISC (SQ3) / (SQ-4) : tout sous-graphe induit a 45 sommets d'un Conway a det(A_H - 3I) = 7^(30-k) n^2 ; a 55 sommets det(A_H + 4I) = 2 x 7^(40-k) n^2 | P | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:254-261 |
| 071 | Condition 7-adique : un bloc a quatre etoiles de Conway a rang_7(8T_S4) <= k <= 28 ; (R7) 'PSD => rang_7 >= 29' REFUTEE | R | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:262-264 |
| 072 | (A4) 'positivite a quatre etoiles => c(l), c(m) >= 2' et les plafonds 'mixtes <= 2', '<= 3', '<= 6' : REFUTES | R | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:213-218 |
| 073 | (N9) a quatre etoiles 'nullite <= 9 + min(c(l), c(m))' et (NOGRID) : REFUTEES ; (LOW) refutee | R | work/stars_rank_2026-10-14/N9_REDUCTION_2026-10-15.md:1-12 |
| 074 | Aucune structure admissible a quatre etoiles invariante sous certains groupes (SAT) | S | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:314-315 |
| 075 | 331 objets distincts de rang 30 (T, U >= 0) a quatre etoiles : jamais c = 1, tous echouent DISC | C | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:393-399 |
| 076 | (SQ30) 'PSD et rang 30 => classe de carres 2*3*5*7^e' : observation EXPLIQUEE par la symetrie h, donc sans valeur de temoignage | H | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:400-411 |
| 077 | ODD9 'les 10 vecteurs m-impairs ajoutent exactement 9 au rang au-dela de X_l' : REFUTEE le 15/10 a 17:05 UTC | R | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:356-371 |
| 078 | (B') 'aucun bloc PSD de nullite >= 14 n'a de droite c = 1' : OUVERTE ; implique 'toute droite de Conway speciale' mais n'exclut pas seule | O | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:445-453 |
| 079 | Enonces ouverts de l'audit du 15/10 : (T8) pont des transversales, (K22), (N15) | O | work/stars_rank_2026-10-14/AUDIT_EXCLUSIONS_2026-10-15.md:46-50 |
| 080 | Mecanisme transversales <-> nullite : nullite = 12 + c(l) - gain pair ; borne d'absorption 4,2516 < 4,5 (indice) | H | work/stars_rank_2026-10-14/AUDIT_EXCLUSIONS_2026-10-15.md:141-170 |
| 081 | Pourquoi les enonces spectraux locaux echouent : les conditions locales testent la realisabilite spectrale, pas la forme 0/1 | H | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:188-198 |
| 082 | Litterature verifiee le 14/10 (statuts des sources, non re-prouves) | H | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:106-117 |
| 083 | Census des droites a 243 : toute droite des huit srg(243,22,1,2) est speciale et dans au moins une grille | E | work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:220-227 |
| 084 | Proposition : (H-MATCH) aux 21 paires de droites d'un sommet => pas de srg(99,14,1,2) | P | work/stars_rank_2026-10-14/H_MATCH_REDUCTION_2026-10-15.md:11-15 |
| 085 | G18 (contraposee quantitative) : chaque sommet d'un Conway a au moins 4 paires de droites a bloc PSD de nullite >= 14 a couplages NON h-relies | P | work/stars_rank_2026-10-14/H_MATCH_REDUCTION_2026-10-15.md:61-72 |
| 086 | (H-MATCH) elle-meme : OUVERTE ; route locale declaree epuisee le 16/10 08:00 UTC | O | work/stars_rank_2026-10-14/H_MATCH_REDUCTION_2026-10-15.md:3-9 |
| 087 | Calibration srg(243) des lois locales : la comparaison ne teste pas (H-MATCH) ; seule Conway force des relations entre DEUX droites (5k - 16 - g = 10) | E | work/stars_rank_2026-10-14/H_MATCH_REDUCTION_2026-10-15.md:151-197 |
| 088 | Lemme G21 : les relations de cote (etoiles et vecteurs de composantes de H_l, H_m) sont h-homogenes pour TOUTE structure admissible | P | work/stars_rank_2026-10-14/H_MATCH_REDUCTION_2026-10-15.md:289-303 |
| 089 | Lemmes de la tache T3 (15/10) : bloc h, singletons de classes, mur de 13 = FAUSSE symetrie, symetries vraies sans h (lemme 6h) | P | work/stars_rank_2026-10-14/H_MATCH_REDUCTION_2026-10-15.md:202-268 |
| 090 | Familles a symetrie vraie sans h : G1'' trop grande (parquee) ; <Z5, hM> enumeree completement (plafond 9) ; exclusion de la famille par Codex (rang_F7 >= 29) | S | work/stars_rank_2026-10-14/H_MATCH_REDUCTION_2026-10-15.md:347-388 |
| 091 | Mecanisme A (15/10) : deux types de cassure ; lemmes des liens (ties), telescopage, signe, grille, fausse transposition | P | work/stars_rank_2026-10-14/MECHANISM_A_2026-10-15.md:31-85 |
| 092 | Refutations du 15/10 apres-midi : KER-SYM universelle, 'au plus une saturation', SUM14, 's <= 1 a nullite 13' | R | work/stars_rank_2026-10-14/MECHANISM_A_2026-10-15.md:86-94 |
| 093 | Seconde lignee cassee independante au mur de 13 (oddw_o9b_HB_1, fausse symetrie h(5 13)) ; enumerations <Z5, tau> completes | S | work/stars_rank_2026-10-14/MECHANISM_A_2026-10-15.md:161-167 |
| 094 | Ou U echoue dans le type I : defaut global (lambda_min(H) = -4,047, aucun certificat induit sous 33 sommets) ; vecteur -4 alterne (indice) | E | work/stars_rank_2026-10-14/MECHANISM_A_2026-10-15.md:161-202 |
| 095 | Les trois resultats de la derniere etape (L1 Makhnev, L8, rho <= 191/126) sont des PLANCHERS de torsion ; consequences prouvees pour les blocs | P | work/stars_rank_2026-10-14/THREE_RESULTS_2026-10-15.md:10-61 |
| 096 | (N9-NG) 'bloc PSD SANS grille : nullite <= 9 + min(c(l), c(m))' et (L07_C1_asym_local-099) => pas de Conway (implication prouvee) ; conjecture OUVERTE | O | work/stars_rank_2026-10-14/THREE_RESULTS_2026-10-15.md:91-130 |
| 097 | (NG7) de Codex : tout Conway a au moins 254 blocs NON-GRILLE avec min(t(l), t(m)) <= 7 | P | work/stars_rank_2026-10-14/THREE_RESULTS_2026-10-15.md:118-130 |
| 098 | Tentative de preuve de (N9-NG) (nuit du 15/10) : reformulations prouvees R1-R6, aucune avancee sur la nullite | P | work/stars_rank_2026-10-14/N9NG_ATTACK_2026-10-15.md:9-153 |
| 099 | Plan de redaction (non ecrit) 'Le cas asymetrique se reduit a une loi locale de symetrie' | H | work/stars_rank_2026-10-14/C1_REDUCTION_OUTLINE_2026-10-16.md:1-35 |
| 100 | DISC tue les 645 germes PSD de rang 30 (classes 2*3*5 ou 2*3*5*7) ; mecanisme de grille (classe 10) | C | work/stars_rank_2026-10-14/EXT84_2026-10-16.md:10-37 |
| 101 | Tout germe est isole : aucune colonne exterieure (domaines vides pour les 40 labels de chacun des 645 germes) | E | work/stars_rank_2026-10-14/EXT84_2026-10-16.md:39-50 |
| 102 | Lien avec (H-MATCH) par une troisieme droite : toute extension a trois droites vers une droite non appariee par M_0 donnerait un contre-exemple a (H-MATCH) | P | work/stars_rank_2026-10-14/EXT84_2026-10-16.md:52-61 |
| 103 | Barriere de la cinquieme etoile : aucune base a quatre etoiles connue (31 + 3, PSD ou non) ne s'etend combinatoirement ; HB certifie par DRAT | C | work/stars_rank_2026-10-14/EXT84_2026-10-16.md:75-98 |
| 104 | Lemme h5 : aucune structure admissible a cinq etoiles n'est invariante par h = (0 1)(2 3) ; renforcement de Codex : au moins 4 des 8 lignes {4,y} cassent h dans TOUTE structure a cinq etoiles | P | work/stars_rank_2026-10-14/EXT84_2026-10-16.md:99-147 |
| 105 | Cinq etoiles sans base (la vraie question) : INCONNU ; si aucune structure admissible a cinq etoiles n'existe, pas de Conway | O | work/stars_rank_2026-10-14/EXT84_2026-10-16.md:118-126 |
| 106 | Calibration corrigee du solveur (16/10 soir) : a K = 22 la cinquieme etoile se trouve en 17-87 s, pour Conway rien en > 20 min ; bases aleatoires : 5/5 s'etendent a K = 22, 0/8 a K = 14 | H | work/REVUE_GLOBALE_2026-10-16.md:291-322 |
| 107 | R7 (quatre etoiles exactes + 7 labels {4,t}, lettre 4 bornee) est SAT ; la 'barriere au 7e label' etait FAUSSE ; R8 (les 8 labels) : INDECIS ; R8 INFAISABLE exclurait Conway | O | work/REVUE_GLOBALE_2026-10-16.md:323-340 |
| 108 | Comptage exact de capacite (tout k), graphe Omega sur L_4, borne des paires de X dependant de k | P | work/REVUE_GLOBALE_2026-10-16.md:360-386 |
| 109 | Critere global sur 84 labels (Codex P4) : C1 exact + binarite + T, U >= 0 de rang T <= 30 <=> srg(99,14,1,2) | P | work/REVUE_GLOBALE_2026-10-16.md:76-81 |
| 110 | Reductions prouvees pour tout Conway listees par la revue du 16/10 (selon les rapports 01-09, non re-prouvees sauf mention) | P | work/REVUE_GLOBALE_2026-10-16.md:98-126 |
| 111 | Cas symetriques (selon les rapports 02 et 04) et chaine de litterature : il ne reste que C1 | H | work/REVUE_GLOBALE_2026-10-16.md:50-64 |
| 112 | Jamais lance et plan chiffre (revue du 16/10) | O | work/REVUE_GLOBALE_2026-10-16.md:259-289 |
| 113 | Dossier externe BvLS : liberer la region lointaine d'un triangle + 2 prismes (192 sommets libres) ne donne que BvLS et le jumeau (27 648 matrices = 2 classes) | E | conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/RESULTATS.md:5-63 |
| 114 | Dossier externe Paley(25) : depuis le bord d'une K5 on reconstruit les 15 srg(25,12,5,6), dont les 2 asymetriques (1 999 872 completions etiquetees) | E | conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/PALEY_ASYMETRIE_DOSSIER/README.md:6-35 |
| 115 | Dossier externe HOFFMAN : deux familles de designs de bord exclues pour alpha = 22 (C22 transitif : 72 designs ; C7:C3 regulier + point fixe : 199) ; une coclique de Hoffman peut subsister dans un srg asymetrique | E | conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/HOFFMAN_UPDATE_20261011/RESULTATS.md:5-86 |
| 116 | Dossier externe K7 (partiel) : Gamma_c u M_c connexe pour tout point c d'une coclique de Hoffman ; rang 13 / Schur rang 9 ; n_ef <= 3 en sept points sous le type ternaire (7,15,0) | P | conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/C1_K7_RESULTATS_PARTIELS/PREUVES.md:17-319 |
| 117 | Sous-cas (A) (11 grilles disjointes, 'SPREAD') : alignement total impossible a 99 ; tout graphe de (A) est desequilibre ; 'balance en general => (A) impossible' (balance ouverte) | P | conway99-c1:origin/claude/v7-simultaneous:notes/168_SOUS_CAS_A_APPROCHE_MATHEMATIQUE.md:1-93 |
| 118 | Bords serres et cocliques de Hoffman a 243 (note 171) : seule BvLS en a ; reconstruction depuis le design de Hoffman de BvLS : completion UNIQUE (198 sommets libres) | S | conway99-c1:origin/claude/v7-simultaneous:notes/171_BORDS_SERRES_HOFFMAN.md:61-119 |
| 119 | Sous-cas alpha = 22 a 99 : structure prouvee (design 2-(22,4,2), D = M u T, Q = 21 P_-4) ; lemme d'extension (11/10) ; recherche par cubes sans verdict | P | conway99-c1:origin/claude/v7-simultaneous:notes/171_BORDS_SERRES_HOFFMAN.md:121-251 |
| 120 | Route du reseau Q pour alpha = 22 : aucune obstruction au niveau des discriminants ; rang_7(A + 4I) impair et <= 45 pour tout Conway | P | conway99-c1:origin/claude/v7-simultaneous:notes/172_RESEAU_Q_ALPHA22.md:1-95 |
| 121 | Conjecture K7 en un point d'une coclique de Hoffman (alpha = 22) : OUVERTE | O | conway99-c1:origin/claude/v7-simultaneous:notes/173_CONJECTURE_K7.md:1-75 |
| 122 | Lemme des points fixes pour srg(v,k,1,2) et emboitements de la famille (9, 99, 243, 6273, 494019) | P | conway99-c1:origin/claude/v7-simultaneous:notes/174_EMBOITEMENTS_FAMILLE_1_2.md:1-119 |
| 123 | Question S3 a 243 : tout srg(243,22,1,2) a etalement regulier est-il symetrique ? OUVERTE (reformulation par code ternaire) | O | conway99-c1:origin/claude/v7-simultaneous:notes/175_QUESTION_S3_ETALEMENT_243.md:1-66 |
| 124 | Le 2-facteur F_x et le graphe d'arete B_xa (notes 176-177) : definitions et identites prouvees ; conjectures (G), (E), (L), (P) ouvertes et peut-etre artefacts | P | conway99-c1:origin/claude/v7-simultaneous:notes/176_DEUX_FACTEUR_FX.md:1-79 |
| 125 | Theoreme (ChatGPT, preuve verifiee a la main par Claude-Bureau) : les mots binaires de ker_7(A + 4I) ont un poids 0, 63 ou 77 ; poids 77 <=> coclique de Hoffman de 22 | P | conway99-c1:origin/claude/v7-simultaneous:notes/178_MOTS_BINAIRES_CODE7.md:1-23 |
| 126 | Passation C1 du 07/10 (session cloud) : C2, C3, C7 exclus => C1 est tout le probleme ; bancs d'essai obligatoires ; routes mesurees trop cheres | H | conway99-c1:origin/claude/v7-simultaneous:PASSATION_C1_2026-10-07.md:1-41 |
| 127 | Note 155 : les transferts sont exactement la classe [q] = q + M ; invariant phi mod 7 ; tests de classe sur germes croissants (sous-cas V7) | P | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/155_V7_CLASSES_MOD7_ET_GERMES.md:1-152 |
| 128 | Note 156 : pas de 'route (C)' pour C1 par les voies mesurees (masse du genre de rang 48 ~ 1,5e121 ; branche 18 ~ 2,3e6 heures CPU) | E | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/156_ROUTE_FINIE_C1_MESURES.md:1-80 |
| 129 | Note 157 : Route Omega complete (decide l'existence) ; T = 3I - Gamma - K, T^2 = 7T, rang 30 ; equivalence (etoile) : Conway <=> Gamma 12-regulier sur les 84 labels avec T^2 = 7T | P | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/157_ROUTE_OMEGA_COMPLETUDE.md:1-159 |
| 130 | Note 158 : deux etoiles mates = boule d'un triangle ; theoreme de rang 8 ; etage F presque force (2 candidats par ligne sur BvLS) ; les colonnes sont le vrai goulot | P | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/158_TROIS_ETOILES_TRIANGLE_ETAGE_F.md:1-100 |
| 131 | Notes 159-160 : un second srg(243,22,1,2) (jumeau, /Aut/ 4 320, tordu) ; refute la conjecture des hexagones de Reimbayev et F20 ; toute loi valable pour toute la famille lambda = 1, mu = 2 ne peut exclure 99 | E | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/159_NOUVEAU_SRG_243_22_1_2.md:1-84 |
| 132 | Note 163 : etage colonnes de la route Omega = plan a blocs a trois couches ; ~1,5e11 classes de C ; cout >= 1,7e10 heures CPU : pas de route finie a cout maitrise pour C1 | E | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/163_ETAGE_COLONNES_TROIS_COUCHES.md:1-113 |
| 133 | Note 164 : piste 'cartes D7 et holonomie' (ChatGPT/Sol) : la carte est connue, l'hypothese cle est fausse en cas de torsion, la branche triviale = Makhnev/L1 | E | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/164_PISTE_D7_HOLONOMIE_SOL.md:1-37 |
| 134 | Note 165 : srg(243,22,1,2) : bascule = rotation d'espaces propres (critere de rigidite) ; pas d'etalement regulier a 99, 6273, 494019 ; Gamma3 (864) et Gamma4 (3888) ; dichotomie Z3 / 2-groupe ; S3-revetement OUVERT | P | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/165_SRG243_REVETEMENTS_ET_SYMETRIE.md:1-244 |
| 135 | Note 166 : partitions equitables de srg(99,14,1,2) : seules (A) 11 grilles 3x3 disjointes (revetement de K11 de degre 9) et (B) 3 cellules de 33 | E | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/166_PARTITIONS_EQUITABLES_99.md:1-43 |
| 136 | Note 167 : principe de monodromie ; loi locale de recollement (identique a 99 et 243) ; 'vrillage obligatoire a 99' ; lois observees (motifs 9 / 3+3+3) | P | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/167_MECANISMES_RECOLLEMENT_GRILLES.md:1-144 |
| 137 | Annexe 162 D_C1 (agent de lecture, 07/10) : table des lemmes L1-L25 de Codex (statuts rapportes) : L2, L5, L8, L16, L22, L25 sont les antecedents de plusieurs resultats LAB de la mi-octobre | H | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/162_annexes/D_C1.md:33-70 |
| 138 | Note 162 : inventaire des 12 depots (07/10) : resultats forts et reserves ; avec C2, C3, C7 : tout srg(99,14,1,2) serait asymetrique | H | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/162_INVENTAIRE_DECOUVERTES.md:1-112 |
| 139 | Notes 161/161b/161c : depot openai/math : rien d'utilisable directement pour Conway | H | conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/161_DEPOT_OPENAI_MATH.md:1-25 |
| 140 | Campagne Astra 'BvLS apres Paley' (11/10) : ouverture, aucune construction ni exclusion revendiquee | O | conway99-c1:origin/astra/bvls-boundary-release-20261011:research/astra_bvls_boundary_20261011/COORDINATION.md:1-17 |
| 141 | Journal et rapport C1 des 24-26/09 (lemmes L1-L25) : synthese ; tous les lemmes sont des PLANCHERS de torsion | H | conway99-c1:origin/main:JOURNAL.md:3-608 |
| 142 | Motifs a deux et trois etiquettes tordues (frontiere de torsion, 24/09) : tous UNSAT (SAT sans certificat) | S | Desktop/Recherche_Conway/c1-asymmetry-audit/data/k3_results.txt:1-20 |
| 143 | Article 'On the 7-rank of a putative srg(99,14,1,2)' (07/10) : rang_7(A - 3I) impair et 23 <= rang_7 <= 43 (25 avec un petit calcul) | P | Desktop/Recherche_Conway/c1-asymmetry-audit/papers/rank7/rank7.tex:19-32 |
| 144 | Articles 'A 2-adic nonexistence condition for SRG' (critere S5) et 'A second srg(243,22,1,2)' (07/10) | P | Desktop/Recherche_Conway/c1-asymmetry-audit/papers/README.md:3-20 |
| 145 | Rang 37 : si rang_7(A - 3I) = 37, une droite dont le graphe a une maille >= 5 a un graphe connexe (assiste par ordinateur) | E | Desktop/Recherche_Conway/c1-lap-girth5-audit/15a3cfe3f/NOTE.md:1-117 |
| 146 | Note 'A Conway 99-graph, if it exists, is asymmetric: statement and dependencies' (07/10) : chaine premier par premier | H | Desktop/Recherche_Conway/srg-research-audit/papers/conway99_asymmetric/asymmetric.tex:1-140 |
| 147 | Manuscrits C2 (order2.tex), C3 (preuve_c3.tex), C7 (order7.tex) dans le depot srg-research : titres, statuts declares | H | Desktop/Recherche_Conway/srg-research-audit/papers/conway99_order2/order2.tex:1-9 |
| 148 | Famille srg(243,22,1,2) publiee (depot public, 11/10) : quatre graphes deux a deux non isomorphes ; verificateur autonome | E | C:/home/researcher/cw/strongly-regular-graphs-research:main:results/srg243_family/README.md:1-40 |
| 149 | Bug OR-Tools 9.15 : domain[-1] renvoie 0 (produits de residus faux) | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt:7-17 |
| 150 | Retrait : fermeture c4 79/79 (familles 7, 9, 19 reouvertes) | X | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt:20-27 |
| 151 | Retrait : 162 verdicts du pilote c3 (8 gabarits) et 5 premiers verdicts du modele partiel | X | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt:20-21 |
| 152 | Retrait : campagne AWS c3star (2c7bdd0b) et Gram retires de gram_filtered_0421 | X | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt:30-31 |
| 153 | Front Gram valide 'snapshot 0306' : 909 Gram ouverts (7:449, 9:12, 19:448), 907 profils distincts | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt:28-29 |
| 154 | Inegalite entiere pour vecteurs propres entiers -4 (norme N, valeurs de meme signe) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/REPRISE_COMPOSANTES_C1_2026_10_16.txt:31-36 |
| 155 | Couverture K4 de grilles : 13824 etiquetages, 59 orbites exactes | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/REPRISE_COMPOSANTES_C1_2026_10_16.txt:199-201 |
| 156 | Table locale des motifs de composantes E3 (toutes couleurs) | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/REPRISE_COMPOSANTES_C1_2026_10_16.txt:163-166 |
| 157 | Redecouverte : derivation independante LAB du census d'ordre 9 (census2.py) | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/REPRISE_COMPOSANTES_C1_2026_10_16.txt:379-385 |
| 158 | Inegalite globale 3P+4G <= 2772 (prismes / grilles induits), certificat entier | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt:4-32 |
| 159 | Racine ponderee : il existe x avec 9s(x)+8g(x) <= 504 ; sous c>=4, s(x) <= 49 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt:34-56 |
| 160 | Bornes P, G sous l'hypothese globale c>=4 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt:58-69 |
| 161 | Filtre Gram pondere : 19 Gram de la famille 19 retires, chacun avec CNF UNSAT et preuve DRAT verifiee | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt:84-93 |
| 162 | Lemme des grilles : domination exacte et intersections | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt:102-127 |
| 163 | Orbites de couplages par renommage des lettres (mate-flip) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt:147-170 |
| 164 | Famille 9 exclue a la racine ponderee (modele unique, 12 Gram et couplages libres) | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt:267-285 |
| 165 | Fermeture de la branche GLOBALE c>=4 : tout srg(99,14,1,2) a une droite L avec c(L) <= 3 | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt:304-345 |
| 166 | Encodage SAT direct root_component_star_cnf.py et identite upper-only | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt:189-210 |
| 167 | Sous c>=4 toute droite est dans au moins deux grilles | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt:212-222 |
| 168 | Huit positions relatives d'une droite c(L)<=3 par rapport a une racine o (s(o)<=51) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/DROITE_PETITE_ET_RACINE_2026_10_18.txt:9-45 |
| 169 | Encodage exact de c(L) <= 3 par foret orientee a au plus 3 racines | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/DROITE_PETITE_ET_RACINE_2026_10_18.txt:47-75 |
| 170 | Pilote droite c<=3 : cas 7 + budget 51 a o, UNKNOWN | O | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/DROITE_PETITE_ET_RACINE_2026_10_18.txt:77-87 |
| 171 | Pilotes et Gram de la campagne c4 (17-18/10, avant le bug) : chronologie des fermetures | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/REPRISE_COMPOSANTES_C1_2026_10_16.txt:42-47 |
| 172 | Contre-exemple K7-C7 (ker C7) : ne pas supposer ker <= 5 | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/REPRISE_COMPOSANTES_C1_2026_10_16.txt:131-132 |
| 173 | Gram 193 de la famille 9 : code 0 exclu par C2 complet (apres correctif) | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/REPRISE_COMPOSANTES_C1_2026_10_16.txt:354-357 |
| 174 | Il existe un triangle avec p(T) <= 9 prismes ; au plus 1151 prismes induits | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:36-105 |
| 175 | Aucun sommet n'a ses 21 paires de triangles engendrant des grilles : au plus 20 grilles par sommet | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:113-281 |
| 176 | Inegalite spectrale sur le graphe des prismes : 10I - R - M/138 - (2/13629)J >= 0 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:283-398 |
| 177 | Lemme P3 : les trois completeurs d'un prisme n'induisent jamais un chemin P3 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:399-433 |
| 178 | p(T)=12 : une arete presente dans deux appariements l'est dans les trois ; 790 types -> 192 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:435-490 |
| 179 | Partenaires de prisme d'un triangle : disjoints, alignes, jamais exactement deux aretes U-V | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:504-577 |
| 180 | Vecteurs entiers -4 : norme minimale 14 = co-Heawood ; angle 7 impossible ; famille orthogonale <= 28 (remplace par 12) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:579-666 |
| 181 | Au plus 191 grilles induites | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:672-675 |
| 182 | Une arete ne peut appartenir a trois co-Heawoods deux a deux orthogonaux | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:677-824 |
| 183 | Relais LAB : rang_F7(A+4I) >= 31, puis >= 33 (b=30), puis >= 35 (b=32) par formes modulaires / Farkas | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:826-836 |
| 184 | Deux vecteurs orthogonaux de norme 14 : supports disjoints ou intersection de 4 ; famille orthogonale <= 12 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:838-915 |
| 185 | Vecteurs entiers -4 de norme <= 24 a coefficients 0,+-1 ; angles entre co-Heawoods dans {0,1,2,4} | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:917-1025 |
| 186 | Au plus 396 co-Heawoods induits (792 vecteurs signes de norme 14) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1027-1084 |
| 187 | Petites couches entieres +3 : classification des supports p=6,7,8 et bornes | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1086-1176 |
| 188 | Noyaux entiers +3 de masse l1 <= 16 : 48 configurations, au plus 313434 vecteurs signes | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1178-1269 |
| 189 | Noyaux affines : 40 types supplementaires, au plus 911178 vecteurs h entiers, Ph=0, //h//_1<=16 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1271-1339 |
| 190 | Multiplicites certifiees de collisions pour la famille D (norme projetee 8, support 8) | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1341-1412 |
| 191 | Comptes exacts dans les anti-voisinages de petits motifs (C4, paw, moulin, maison) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1414-1471 |
| 192 | Construction lambda=1 : hemi_s1 = SRG(378,52,1,8) verifie, groupe d'ordre 6 ; bords aleatoires sans nouvelle completion | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1473-1510 |
| 193 | Pas de 3-ovoide dans le quadrangle de Payne sur GF(9) (obstruction de parite) | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1491-1505 |
| 194 | Transport des triangles T_x et squelette enracine K_x : borne /Aut(G)/ <= m*h | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1512-1545 |
| 195 | Critere fini de rigidite : un circuit unique de longueur L utilisant les k lettres | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1546-1562 |
| 196 | Corollaire de construction : saturation m*h = /Aut(G)/ => toute autre completion du squelette est un nouveau graphe | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1578-1618 |
| 197 | Rigidite et unicite sont distinctes ; non-unicite reelle du squelette BvLS | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1620-1651 |
| 198 | Equations exactes de completion pour mu=2 et dimension lineaire minimale | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1653-1682 |
| 199 | Theoreme de majorite des retournements purs (flip) et code C_x | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1692-1727 |
| 200 | Coupure par orbites : groupe de l'instance et nombre de completions (principe de symetrie forcee) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1729-1772 |
| 201 | Objet49 / bloc U50 : degres 6,7,8, au plus trois sommets de degre 8 ; preprocesseur de colonnes | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1774-1831 |
| 202 | Temoin fractionnaire a trois etoiles : rang 31 (relaxation continue insuffisante) | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1833-1866 |
| 203 | Structure binaire LAB697 a trois etoiles : T_SS PSD de rang exact 31 (non completable) | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1868-1881 |
| 204 | Echanges en rectangle et theorie de reponse de rang 2 (rang 31 -> 30) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1883-1923 |
| 205 | Une grille 3x3 force rang <= 30 a trois etoiles (4e relation) [resultat LAB 700] | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1925-1932 |
| 206 | Frontieres a trois etoiles LAB 700, EX0, EX2, V0, V7, V15 non completables (filtre de colonne {3,4}) | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1934-1970 |
| 207 | Second Gram ambiant : U = 7Pi_SS - T_SS doit etre PSD ; 16 coupes lineaires | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:1972-2010 |
| 208 | Lot 713 : les 572 frontieres Z5 fournies sont toutes non completables | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2040-2082 |
| 209 | Refute : 'rang 30 a trois etoiles implique la grille designee sur (l,m)' (contre-exemple LAB z2b) | R | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2084-2090 |
| 210 | Classification exacte a deux etoiles mates : rang(T_X)=23-c, rang(T_S) <= 32-c | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2092-2121 |
| 211 | Conjectures LAB (A), (B), (C) et lemme intrinseque c(l)+1 = dim(E_3 supporte sur N[l]) | O | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2151-2160 |
| 212 | Balayages d'echanges et circuits sur les graines PSD31 : aucun nouvel objet de rang 30 | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2173-2201 |
| 213 | Obstructions de conjugaison par reflet d'incidence (methode, pas une preuve de (A)) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2205-2219 |
| 214 | Budget de projection sur une base a deux etoiles : somme 808-56c | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2232-2240 |
| 215 | c(l) = nombre de composantes de H_l ; multiplicites -4 : 7+c(l), 3 : 18 [resultat LAB 727] | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2295-2300 |
| 216 | Code binaire im_F2(A) : poids minimal >= 2+(k-2)/mu (pair) ; Conway >= 8 ; relations de noyau a 2,4,6,8 coefficients impairs exclues | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2302-2344 |
| 217 | Resultats LAB 731 : code im_F2(A) de dimension 54, dual de poids >= 8, grille = code parfait | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2372-2379 |
| 218 | Famille ternaire de noyaux variables : 194336 formes normalisees, survivants 118848 / 104528 | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2381-2415 |
| 219 | Lemme de couverture des supports binaires par voisinages (tout SRG(v,k,1,2)) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2417-2457 |
| 220 | Relations supplementaires non negatives a trois etoiles : poids >= 16 (w=8 et w=12 exclus) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2468-2543 |
| 221 | (A) sans positivite est faux ; construction rationnelle profil 31 violant C2 | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2545-2552 |
| 222 | (A) REFUTEE par le germe LAB counterexample_A_1 (rang T = 30, Q connexe, T et U PSD) | R | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2616-2631 |
| 223 | H4' (aucune extension a deux Q connexes, T/U PSD, rang T <= 30) : ouvert ; s'il etait vrai, un sommet aurait au plus une droite non speciale | O | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2633-2637 |
| 224 | Reduction exacte du join de quatre etoiles (34 -> 44) et filtres de couples | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2639-2682 |
| 225 | Theoreme de couplage (saturation h=0 force Gamma q = alpha q) et coupes entieres | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2707-2724 |
| 226 | Theoreme de positivite stricte de U sur les secteurs (anti)symetriques ; 100 coupes strictes | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2726-2752 |
| 227 | Observation LAB : 487 structures PSD G1, toutes avec les deux c >= 3 (biais signale) | H | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2754-2759 |
| 228 | Theoreme des secteurs G1 : rang T <= 30 impose nullite non triviale >= 9 - min(c_l,c_m) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2795-2821 |
| 229 | Famille locale G1 c55 non grille : quotient de rang 1 et catalogue exact des secteurs 10/01 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2823-2903 |
| 230 | Contributions LAB 761/762 : rang quatre etoiles = 30 - delta ; conjecture t(l) >= 8 | O | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2905-2912 |
| 231 | P <= 852 (certificat rationnel P <= 11088/13) ; la relaxation reelle du census d'ordre 9 admet P = 0 | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2923-2935 |
| 232 | Budget local sommable tr(MV) >= 0 (compressions 10x10) et contrainte globale de second moment | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:2937-3001 |
| 233 | Cas d'egalite t_v=d_v=0 : 4480 matchings (deux formes), 2334720 bijections etiquetees | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3040-3061 |
| 234 | Lemme uniforme a une droite : les blocs impairs T_impair, U_impair sont automatiquement definis positifs | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3079-3141 |
| 235 | Famille G1 c55 non grille : au moins 29 des 40 sommets exterieurs brisent h ; vecteur propre global z (10,24,6) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3143-3224 |
| 236 | Exclusion de la famille locale G1 c55 non grille par F7 : rang_F7(8T_S) >= 29 > 28 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3226-3301 |
| 237 | Bornes P <= 1150, rho <= 126 (11 rho <= 1386), P <= 852 : statuts des certificats | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3311-3320 |
| 238 | Au moins 336 des 2079 drapeaux (v,{l,m}) ont au moins quatre relations mixtes | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3322-3381 |
| 239 | c55 non grille sans G1 : e(O)=2 ; 128 coeurs, 18 types ; quotient equitable identique | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3395-3454 |
| 240 | ODD9 comme energie de reseau : 8T_X = L8 - uu^t (laplacien pondere) ; ODD9 <=> det B > 0 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3456-3533 |
| 241 | Bloc h-pair : D_w A D_w = L_R - L_K/2 ; rang A = 10 <=> multiplicite 11 de la valeur 12 dans 4R | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3535-3612 |
| 242 | Bloc mixte : //B//_F^2 = b/2 ; capacite de la moyenne ; coupes de direction ; au plus 4096 orientations | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3614-3684 |
| 243 | Resultat LAB 799 : 287 classes de noyaux completes (SAT), seule obj53 a des structures cassees, aucune PSD | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3817-3823 |
| 244 | Mur 13/14 : nullite T = i + nombre de valeurs singulieres de K egales a 1 ; obstruction de volume | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3839-3902 |
| 245 | Cassures comme circulations : critere de solvabilite des signes par composante | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3904-3979 |
| 246 | Defaut geometrique d'une involution g = h p (p quelconque sur les 10 lettres) ; HB_1 sans saturation | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:3981-4056 |
| 247 | G1'' : carre force sur F, 96 interfaces (une orbite), reduction exacte ; cible somme <= 27 (<= 25 avec F7) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4058-4128 |
| 248 | G1'' casse : quatre grilles interdites (d_P <= 1) et c_m <= 3 ; sous-famille G1'' brisant H-MATCH avec c_m >= 4 exclue sous T >= 0 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4130-4162 |
| 249 | Projection exacte de C2 (auxiliaires y_ijt) et format de preuve Farkas / arbre binaire | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4164-4306 |
| 250 | Exclusion de toute la famille locale <z,hM> (Z5-hM) : nullite <= 14 et, a 14, rang_F7(8T) >= 29 | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4308-4425 |
| 251 | Resultat LAB 826 : enumeration <z,hM> terminee, 339556 structures, 192 PSD, nullite max 9 | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4443-4450 |
| 252 | Correction : 'hM tue toutes les relations mixtes' (message 819) est FAUX | R | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4452-4473 |
| 253 | <z,hM> : min(c_l,c_m) = 2 structurel ; plafond local 9 prouve pour 7 des 14 quotients (mod 5) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4475-4535 |
| 254 | Relations mixtes sans symetrie : rang R_mix = 21 + c_m - nullT ; espace des changements conservant le noyau ; lien avec la symetrie forcee | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4611-4707 |
| 255 | Coupe stricte universelle (sans ODD9 ni symetrie) : e(O u S) <= 48, soit q^tTq >= 8 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4718-4765 |
| 256 | Modele fractionnaire de necessite : comptes lineaires + boite + matchings convexes + T/U PSD n'impliquent pas ODD9 | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4768-4816 |
| 257 | KER-SYM universelle REFUTEE (LAB 841) ; coupe 48 non saturee sur 4 objets (586278 directions) | R | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4841-4897 |
| 258 | ODD9 universelle REFUTEE (LAB 843), meme a nu=14, c22, h ; SUM14 universelle refutee | R | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4899-4915 |
| 259 | Decomposition sans symetrie du defaut ODD9 : d_l = b - 2 + eta_l, b-2 = multiplicite de 3 dans Gamma_- ; parite renforcee | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4917-4989 |
| 260 | Famille exacte des 120 appariements du contre-exemple ODD9 : K5,5 force, nu14 | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:4991-5073 |
| 261 | Retrait de portee : la note 100 de Codex ('aucune combinaison ne peut donner de contradiction') est trop forte | X | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5100-5109 |
| 262 | Census entier a P=0 : integralite et non-negativite du census d'ordres 7, 8, 9 ne prouvent pas P > 0 | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5111-5142 |
| 263 | Au moins 254 drapeaux non-grille portant une droite a petite transversale (t <= 7) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5144-5179 |
| 264 | Cible NG7 (ouverte) ; NG5 => NG7 ; N9-NG/NG5 => P >= 924 > 852 (implications conditionnelles) | O | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5181-5206 |
| 265 | Portee des resultats L8, L10, L16 (Krein), C11 et conjecture (P) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5208-5229 |
| 266 | Theoreme de cloture des noyaux retenus (laplacien) et corollaire codimension 1 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5245-5360 |
| 267 | Forme minimale de la cible : nu = 21 + c_l - rang S ; estimation de moments rang T >= 23 (insuffisante) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5371-5409 |
| 268 | C4DO prouvee pour les relations plates de support <= 12 ; 832 coeurs interdits comme sous-graphes induits | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5411-5536 |
| 269 | Relations plates de support <= 14 d'incidence nulle : q nul sur tout O ; support >= 16 si elles touchent O | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5538-5611 |
| 270 | H-MATCH : enonce cible et constructions orthogonales sans conclusion | O | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5623-5704 |
| 271 | Germes casses n_45 et b_29 (LAB) : aucun remariage ni relabellement ne repare U (temoins entiers) | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5706-5801 |
| 272 | Rigidite des rematchings purs d'une etoile (meme a noyau variable) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5843-5911 |
| 273 | Reconstruction des racines : reduction exacte a deux matrices 10x10 ; bloc HB promu (T PSD rang 30, nu14, U PSD rang 39) | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5913-5987 |
| 274 | Le bloc HB promu et les 120 incidences HB ne se prolongent pas (colonne (4,6)) ; urep100 : 2 colonnes de norme 7808/425 (rang 31) | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:5989-6036 |
| 275 | Critere global necessaire et suffisant : C1 + binaire + T,U PSD + rang T <= 30 <=> SRG99 ; assemblage 44->84->99 implemente | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:6038-6114 |
| 276 | Bilan LAB 884 : 416 classes de noyaux, 413 completes, ~853000 structures, aucune structure cassee de nu >= 14 | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:6116-6127 |
| 277 | Liberation du rang et reparation de coeurs (urep100) : coeurs 41, 39, 38, 33 impossibles avec x=(4,6) | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:6129-6191 |
| 278 | Theoreme DISC (LAB 886-887) : classes de discriminant 2 ou 14 (T8 rang 30) et 1 ou 7 (U15 rang 40) ; coupe Schur-DISC | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:6193-6227 |
| 279 | Coupes PSD universelles apprises (--learn-psd) : 398 inegalites transportables | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:6230-6274 |
| 280 | Coeur 30 de urep100 exclu par projection globale 84 (CP-SAT UNSAT) | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:6277-6352 |
| 281 | Defaut quantitatif obligatoire a cinq etoiles : au moins 3, puis au moins 4 lignes d'attache brisent h (sans hypothese h) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:6354-6419 |
| 282 | Constructions partielles de cadres globaux (8, 12, 13, 15 lignes sur 84) et leurs obstructions | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:6472-6552 |
| 283 | Modele global exact (couverture 19 types) et moteur paresseux : fini mais cout non borne | O | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:6691-6767 |
| 284 | Equivalence globale : pour Gamma84 binaire avec C1 exacts, T et U PSD suffisent (SRG99) ; obstacle fractionnaire | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md:6770-6824 |
| 285 | Trois étoiles : une 4e relation positive normalisée de ker(T) a un poids w >= 16 | C | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_nonnegative_weight_bound_733.txt:1 |
| 286 | Trois étoiles : constructeur libre (H2) et énumération du poids 16 — pas d'exclusion du poids 16 | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_nonnegative_weight_bound_733.txt:5 |
| 287 | Poids 16 concentré sur une seule paire extérieure : exclu (52 profils) ; poids 16 => au moins 2 paires extérieures actives | S | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_after738_family52.txt:1 |
| 288 | Profil 31 : Γ rationnel (dénominateur 29664) avec T, U PSD exacts mais violant 22 plafonds C2 (LP + PSD trop faible) | C | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_after738_family52.txt:3 |
| 289 | Contre-exemples NON PSD à (A) : 6 candidats à c = 1 de nullité >= 4 | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_reply735_connected.txt:1 |
| 290 | Les relations hors PSD ne sont pas h3-invariantes | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_reply738_h3.txt:1 |
| 291 | (A) est fausse (résultat LAB 741, accepté par Codex sans re-audit) | R | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_after741_joint_fourth_star.txt:1 |
| 292 | Compatibilité jointe de la 4e étoile : arêtes forcées au rang 30, budgets exacts, Schur de U | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_after741_joint_fourth_star.txt:3 |
| 293 | Coupes d'intégralité issues de l'identité D T D^t (secteurs mate-symétrique / antisymétrique) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_after745_coupling.txt:3 |
| 294 | Les 51 autres germes à trois étoiles de counterexamples_A_all.json ne se prolongent pas par {4,6} | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_51_extensions_and_coupling.txt:1 |
| 295 | (H4) sans borne de rang est fausse (objet LAB positif de rang 34, message 746) | R | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_51_extensions_and_coupling.txt:3 |
| 296 | Théorème : compressions de U définies positives sur les secteurs extérieurs pur symétrique et pur antisymétrique ; 100 coupes strictes | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_strict_upper_100.txt:1 |
| 297 | Réduction exacte des domaines de colonnes 44 -> 45 (tables de jointure 4356 + 4356) | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_after752_fourstar_columns.txt:3 |
| 298 | Famille G1 : contrainte par caractères de Klein-4 (rang T <= 30 => nullités non triviales >= 9 - min c) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_g1_character_rank_targets.txt:1 |
| 299 | Lemme c55 non grille (G1) : quotient trivial unique de rang 1 / nullité 10 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_c55_trivial_quotient_756.txt:1 |
| 300 | c55 non grille : les six cibles se réduisent au seul secteur -- (126 Schur T et U définis positifs) | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_c55_exact_joint_sectors.txt:1 |
| 301 | Bord local c55 à 59 sommets : U PSD mais T négatif dans le secteur 11 | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_c55_exact_joint_sectors.txt:7 |
| 302 | Census d'ordre 9 : point rationnel exact avec P = 0 (aucune borne inférieure sur P par cette relaxation) | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_global_counting_after764.txt:3 |
| 303 | Inégalité de comptage sommable (second moment) : 5 Σ//E_vlm//^2 + 928 P + 48 Z <= 12374208 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_global_counting_after764.txt:5 |
| 304 | Plancher entier des comptes seuls : exact et trop bas (moyenne 504 contre seuil 1190,4) | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_coarse_floor_after768.txt:3 |
| 305 | Interface census impaire : pour une droite, T = 6I - Q et U = 8I + Q ont toujours spectre [2,10] et [4,12] sur 1-perp | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_odd_census_after769.txt:3 |
| 306 | G1 c55 non grille : contraintes de prolongement globales (histogramme (10,24,6), au moins 29 profils sur 40 rompent h) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_c55_global_after772.txt:1 |
| 307 | G1 c55 non grille : rang_F7 des 126 états (114 de rang 10, 12 de rang 9) ; au plus un secteur perd une dimension | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_7adic_direction_after774.txt:1 |
| 308 | Toute la famille G1 c55 NON GRILLE (T, U PSD) a rang_F7(8T_S) >= 29, donc ne se prolonge jamais en Conway | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_c55_excluded_after774.txt:1 |
| 309 | Bornes de prismes et de grilles : P <= 1151 puis P <= 1150 (preuve cubique), P <= 11088/13, 6ρ <= P, 1386 - P - 5ρ >= 0, donc ρ <= 126 | C | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_mixed_budget_direction_after778.txt:1 |
| 310 | Budget exact des relations mixtes : Σ mixtes = 12474 - 45ρ + 3O + 6H + Δ >= 6804 (moyenne >= 36/11 > 3) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_mixed_budget_direction_after778.txt:3 |
| 311 | Tout Conway a au moins 336 des 2079 drapeaux (sommet, paire de droites) avec >= 4 relations mixtes, et au moins 18 sommets portant un tel couple | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_mixed336_after778.txt:1 |
| 312 | c = (5,5) non grille SANS G1 : réduction à 18 types de cœurs et 19 permutations S4 (pas d'exclusion) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_reprise_785.txt:3 |
| 313 | Partage des tâches du 15/10 : Codex prend T2 (ODD9), le LAB T3 (absorption, mur à 13) ; « H-MATCH => Hamming » accepté par Codex | H | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_reprise_785.txt:1 |
| 314 | ODD9 : formule réseau exacte (8T_X = L8 - uu^t ; gain impair = rang d'un Schur S9 ; ODD9 <=> det B > 0 sous T PSD) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_odd9_network_result.txt:3 |
| 315 | Le Schur 10 à sommes nulles n'est pas un laplacien à poids positifs (testé faux sur c11_mix6) | R | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_odd9_network_result.txt:12 |
| 316 | Forme A22 (h-paire) : différence de laplaciens ; rang A = 10 <=> la valeur propre 12 de 4R a multiplicité 11 ; A a toujours >= 10 paires hors diagonale positives | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_response_790.txt:3 |
| 317 | Défaut h : identité //Δ//_F^2 = 4b, //B//_F^2 = b/2 ; sous T >= 0 et rang A 10, rang B <= 10 et //B//_op^2 >= b/20 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_response_792.txt:1 |
| 318 | Les bornes Frobenius/capacité ne rejettent aucune des 47 moyennes (LAB, accepté) | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_response_795.txt:1 |
| 319 | Réduction des signes d'orientation (RREF + propagation) et coupe entière /2u^T B v/ <= u^T A' u + v^T C' v | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_response_795.txt:7 |
| 320 | Moyennes à 40 cassures simples : au plus 4096 orientations modulo h (borne prouvée) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_response_797.txt:1 |
| 321 | Mur 13/14 : nullité T = nullité T0 + multiplicité de la valeur singulière 1 d'une contraction ; critère de volume (α_1...α_p)(β_1...β_p) <= 1 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_response_801.txt:3 |
| 322 | Théorème de circulation des composantes : signes solubles ssi degrés pairs et nombre PAIR de canaux croisés par composante | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_response_803.txt:1 |
| 323 | Défaut géométrique pour g = h·p : réduction exacte de T PSD à 4 G_A^{-1} - G_C PSD (rang E <= 4) ; lecture de HB_1 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_response_805.txt:1 |
| 324 | G1'' : normalisation du carré forcé F (facteur étiqueté 96, wreath C2 wr S4 transitif) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_807_square.txt:1 |
| 325 | G1'' : aucune des paires P6/7, P8/9, P10/11, P12/13 n'est une grille avec m ; g_m <= 1 et c_m <= 3 sous H-MATCH cassé (g_m <= 2, c_m <= 4 sinon) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_809_grid_cut.txt:1 |
| 326 | Certificats exacts pour MILP : distinction LP/MILP (Farkas racine vs arbre de branchement), coupes PSD entières, projection exacte de C2 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_812_exact_route.txt:1 |
| 327 | Famille hM : les deux droites ne peuvent pas avoir simultanément leurs cinq grilles extérieures (T, U PSD) — exclut c_l = c_m = 6 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_z5hm_progress.txt:2 |
| 328 | Exclusion de TOUTE la famille locale <z,hM> comme bord d'un Conway : null_Q(T) <= 14 et, à nullité 14, rang_F7(8T) >= 29 > 28 | C | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_z5hm_exclusion_progress.txt:1 |
| 329 | Campagne LAB <z,hM> complète : 339556 structures, 192 PSD, plafond local de nullité 9 (accepté par Codex sans audit) | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_z5hm_mixed_parity_826.txt:1 |
| 330 | <z,hM> à nullité 9 : profils de parité (null_g+, null_g-) = (7,2) ou (3,6) ; min(c_l,c_m) = 2 forcé ; plafond 9 prouvé dans 7 des 14 types de quotient (mod 5) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_z5hm_mixed_parity_826.txt:2 |
| 331 | <z,hM> : filtre ramifié du second ordre dans Z[ζ5]/5 = F5[e]/e^4 (contraintes de phase dans les 7 types restants) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_831_ramified.txt:3 |
| 332 | Lemme d'asymétrie : les équations du noyau seules ne peuvent forcer aucun h·p tant que ν < 11 + max(c_l, c_m) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_833_mixed.txt:3 |
| 333 | Coupe binaire plate (ODD9) : T PSD + C1 + binarité => e(O ∪ S) <= 48 (au lieu de 49) ; 31752 directions h-impaires | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_839_odd9_integer_cut.txt:1 |
| 334 | ODD9 : modèles fractionnaires de nécessité (gain impair 8 avec matchings internes dans le polytope des matchings) ; identité gain impair = 11 + c_l - ν + rang(C_m N) | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_836_odd9_progress.txt:1 |
| 335 | KER-SYM n'est pas forcée par dimension : à ν = 14 la strate invariante a codimension >= 150 dans Gr(10,40) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_839_odd9_integer_cut.txt:11 |
| 336 | KER-SYM universelle est fausse à nullité 9 (réfutation LAB, intégrée par Codex sans audit) ; version ν >= 14 non tranchée | R | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_841_balanced_profiles.txt:14 |
| 337 | Coupe 48 : aucune saturation sur quatre exports LAB ; outil exact pour TOUTES les coupes équilibrées (586278 directions) | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_841_balanced_profiles.txt:3 |
| 338 | ODD9 universelle est FAUSSE (contre-exemples exacts LAB, dont hv_h_c22_H30_23.json) : Codex retire ODD9 | R | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_843_corrected_odd_budget.txt:1 |
| 339 | Formule du défaut ODD9 sans symétrie : d_l = 9 - gain impair_l = (b - 2) + η_l, 0 <= η_l <= s ; gain pair résiduel = 12 + c_l - ν + d_l | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_843_corrected_odd_budget.txt:3 |
| 340 | Famille des appariements de hv_h_c22_H30_23 : 120 appariements M exactement (toutes paires transversales P/Q), tous ν = 14, gains impairs 8/8 | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_845_mate_family.txt:3 |
| 341 | P = 0 survit à l'intégralité du census fourni : point entier (57 paramètres, 6435 comptes entiers >= 0, P = 0, grille H9 = 0) | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_849_torsion_census_ng7.txt:3 |
| 342 | Cible obligatoire (NG7) : tout Conway a AU MOINS 254 blocs NON-GRILLE avec min(t(l), t(m)) <= 7 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_849_torsion_census_ng7.txt:5 |
| 343 | Retrait : la note 100 de Codex ne prouve pas que les lemmes ne pourront JAMAIS contribuer à exclure Conway | X | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_849_torsion_census_ng7.txt:9 |
| 344 | Diagnostic de transfert des lemmes globaux hors grille : L16/Krein valable avec toute torsion ; L8 et L10/U ne se transportent pas | H | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_849_torsion_census_ng7.txt:11 |
| 345 | NG5 + P <= 852 => pas de Conway (implication LAB vérifiée par Codex) ; NG7 = NG5 restreint aux blocs non-grille ayant une droite t <= 7 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_850_ng5_scope.txt:3 |
| 346 | Théorème de clôture des partitions de noyau : un retrait d'une relation est automatiquement annulé par la positivité sauf fusion de deux composantes | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_854_kernel_partition_closure.txt:1 |
| 347 | Cible de rang pour NG5 : rang T = 23 - c_l + rang S, ν = 21 + c_l - rang S ; NG5 <=> rang S >= 9, 10, 11, 12 hors grille pour c_l = 1..4 | O | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_855_rank_target.txt:3 |
| 348 | Relations plates de support <= 12 : support = deux prismes anticomplets ; les 832 cœurs 12 ont T PSD rang 11 et U PD rang 12 | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_858_flat_prism_cores.txt:1 |
| 349 | Théorème C4DO restreint : binaire + C1 + C2 + T, U PSD => toute relation plate (Bq = 0, coefficients 0, ±1) de support <= 12 satisfait C4DO ; les 832 cœurs 12 sont interdits comme sous-graphes induits du bloc 44 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_859_flat_c4do_proof.txt:1 |
| 350 | Théorème support 14 : toute relation plate d'incidence nulle de support <= 14 s'annule sur tout O ; une relation plate touchant O a support >= 16 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_862_support_fourteen.txt:1 |
| 351 | Normalisation Π : A + A' = 7Π_+ (pas 7I) après retrait des étoiles ; la formule Φ (LAB 867) n'est valable qu'après congruence par Π_+^{-1/2} | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_867_pi_normalization.txt:1 |
| 352 | Remariage fermé pour n_45 et b_29 : λ_min(Γ) < -4, donc aucun changement de M ni réétiquetage ne rend U PSD | C | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_865_hmatch_target_input.txt:1 |
| 353 | H-MATCH : aucune preuve réaliste à court terme ; proposition d'un pilote GLOBAL (zéro-extension des noyaux locaux aux 40 lignes restantes) | O | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_875_hmatch_prospects.txt:2 |
| 354 | Rigidité antipodale des torsions pures : aucun rematching pur d'une étoile possible pour urep100 et hv_h_c22_H30_23 | C | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_877_antipodal_rigidity.txt:1 |
| 355 | HB_1 promu : nouveau bloc étiqueté T PSD rang 30 (ν 14), U PSD rang 39, C1/C1'/C2 exacts, H-MATCH intact (même Γ non étiqueté) | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_root_schur_construction.txt:1 |
| 356 | Le HB promu ne se prolonge pas : aucune colonne binaire pour le sommet extérieur (4,6) (certificat d'arbre à Farkas entiers) | C | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_extension_construction.txt:1 |
| 357 | Assemblage complet 44 -> 84 -> 99 et obstruction exacte de prolongement d'urep100 (2 colonnes, norme T8 = 7808/425 < 20, rang 31 forcé) | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_complete_assembly.txt:1 |
| 358 | Critère global de complétion : sur les 84 étiquettes, T + U = 7Π, rang Π = 70, tr T = 210 ; T, U PSD et rang T <= 30 forcent l'identité SRG99 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_complete_assembly.txt:5 |
| 359 | Réparation par cœurs (urep100) : libérer des dimensions en supprimant des sommets ; DISC intégré comme filtre ; bibliothèque de 398 coupes PSD apprises | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_microscopic_repair.txt:1 |
| 360 | Cœur 30 d'urep100 (T25/U30) exclu de tout Conway par les comptes globaux exacts du 84 (CP-SAT UNSAT) | S | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_global_columns.txt:1 |
| 361 | Obstruction signée universelle apprise sur 15 étiquettes : e(P) + e(N) - e(P,N) <= 14 | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_global_columns.txt:9 |
| 362 | Statut explicite du cœur 30 : modèle CP global UNSAT ; arbre de séparateurs 47 feuilles fermées / 7 ouvertes ; option --stars5 (base 52) | S | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_bridge_global_columns_delivery.txt:1 |
| 363 | Cinq étoiles : au moins 3 des 8 lignes d'attache X = {(4,y)} rompent h (D >= 12) ; en général D >= 2k - 16 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/message_defect_20261016.txt:1 |
| 364 | Cinq étoiles : au moins 4 des 8 lignes X -> {ancien 44} rompent h (spécifique à 99) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/message_four_broken_20261016.txt:1 |
| 365 | Témoin constructif : les 12 lignes de L4 complètes sur les 84 étiquettes (sans germe 44 fixe), 4 lignes rompant h | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/message_global_star12_20261016.txt:1 |
| 366 | Cadre 12-global : quatre lignes de L0 ((0,7), (0,9), (0,10), (0,13)) individuellement INFEASIBLE | S | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/message_phi_899_reply.txt:3 |
| 367 | Lemmes PHI (défauts nécessaires des vrais matchings croisés) : D_a >= 12 + 2t_a - 4δ_a >= 10 ; joint b + (d_1 ET d_2) >= 4 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/LEMMES_PHI.txt:1 |
| 368 | Cadre 15 lignes complètes sur 84 (toute L4 + 02, 03, 010) par échanges équilibrés ; maximum 14 prouvé conditionnellement au cadre 13 | E | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/README_STAR_REPAIR_PHI.txt:3 |
| 369 | Le témoin 15 lignes (83ecbbe) est non prolongeable : obstruction réduite à cinq lignes 02, 03, 47, 48, 413 (comptes entiers seuls) ; coupe universelle « motif 58 arêtes <= 57 » | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/message_gray_block_obstruction_20261016.txt:1 |
| 370 | Modèle EXACT du graphe 99 entier sans germe, couvrant tout Conway par 11 types d'appariements (ou 19 types pointés autour d'une droite de t minimum <= 7) ; pilotes UNKNOWN | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/message_global_cover_scope_20261016.txt:1 |
| 371 | Comptes racines exacts => total 166 = 2·83 par ligne ; les seules bornes <= 2 forcent toutes les égalités ; moteur paresseux à clauses universelles de 3 à 6 arêtes | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/message_global_cover_delivery_20261016.txt:5 |
| 372 | Équivalence globale : pour Γ84 binaire symétrique avec tous les C1 exacts, T et U PSD suffisent à tous les C2 (C1 + binarité + deux PSD <=> SRG99) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/message_907_global_psd_reply.txt:5 |
| 373 | Centre fractionnaire Γ0 = (2J - B^t(I+M)B)/10 : satisfait C1 avec T = 3P, U = 4P ; la positivité continue seule ne sera jamais infaisable ; défaut tr(TU) = Σ Γ_ij(1 - Γ_ij) (840 au centre) | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/message_global_psd_delivery_20261016.txt:5 |
| 374 | La borne T(99) <= 55 triangles de Natal–Al-saadi (arXiv 2610.16266, Conjecture 5) est fausse : 11 grilles 3x3 disjointes (66 triangles) ; exemple connexe à 120 triangles | C | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/literature_sos_2610_16266_counterexample.txt:1 |
| 375 | Relevé bibliographique Conway du 16/10/2026 (arXiv + Zenodo) : aucun texte ne fournit une preuve de non-existence ni un calcul exhaustif abordable | H | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/RELEVE_LITTERATURE_2026-10-16.txt:5 |
| 376 | Représentations sphériques de Conway et budget extérieur sans hypothèse d'équilibre : G - (2q+1)F + q(q+1)m = Σ(f_x - q)(f_x - q - 1) >= 0 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/RELEVE_LITTERATURE_2026-10-16.txt:61 |
| 377 | Retrait LAB (message 916) : « quatre étoiles exactes + sept labels {4,t} » est SAT sans base fixée ; l'obstruction universelle au 7e label est retirée | X | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/RELEVE_LITTERATURE_2026-10-16.txt:76 |
| 378 | État R7 / R8 (LAB, commit dbe4caa, REVUE_GLOBALE §9) : six témoins R7 non prolongeables ; R8 sans base fixée UNKNOWN ; X complet force la lettre 4 exacte | S | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/ETAT_PONT_918_2026-10-16.txt:3 |
| 379 | Résonance k = 14 : Σ_F (n_C - 2c/(k-2))^2 = (k-14)c(1 - c/(3(k-2))) ; à 99, tout sommet lointain voit exactement c/6 de chaque composante ; une grille laisse (k-4)(k-14)/2 sommets sans voisin | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/bridge_family_resonance_921.txt:3 |
| 380 | Comptage de la cinquième étoile : débordement D_k = 8 + a - (k-14)(k-7)/2 ; seul k = 14 force un débordement positif | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_family_synthesis_51460e5.txt:7 |
| 381 | Critère de symétrie forcée : /complétions ÉTIQUETÉES d'un bord H/ < /Aut(H)/ exclut une complétion asymétrique ; non applicable en l'état aux bords 43/44 à <= 2 complétions | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_family_synthesis_51460e5.txt:9 |
| 382 | Registre de synthèse de la famille (1,2) (commit 51460e5) : 48 réductions/limites, front global = R8 libre ou modèle 84 + comptes racines + deux PSD | H | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_family_synthesis_51460e5.txt:1 |
| 383 | Réduction exacte Q20 de N9-NG : ν = c(l) + 2 + corang(Q) ; N9-NG <=> rang(F) >= 12 (F = Q + J/12) pour la droite de c minimum | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_resonance_925_first.txt:3 |
| 384 | SYM6 <=> rang(Z) >= 3 ; sous rang(D) = 9 (ODD-PURE), Conway exige rang(Z) <= c - 2 : c_min = 1 impossible, c = 2, 3, 4 demandent rang Z >= 1, 2, 3 | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_sym6_928_first.txt:1 |
| 385 | Identité de bord SYM6 : G est une laplacienne avec attaches vers O de poids total r = 8 - 2e(O) (nul ssi grille) ; rang G = 11 - c(m) ; hors grille rang L = 10 - c(m) >= 5, mais A peut perdre beaucoup de rang | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_sym6_boundary_4c9ca38.txt:1 |
| 386 | Borne d'énergie paire (B) : sur deux étoiles mates complètes, le Schur pair E vérifie E >= G/5 + (2/5)(I - M) >= G/5 ; ker E = ker G, rang E = 12 - c | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/sym6_energy_43c496e/BORNE_ENERGIE_PAIRE_2026_10_16.txt:5 |
| 387 | Couplage des 20 étiquettes fixes : rang T = 32 - c(l) - δ + rang Z, δ = 9 - rang D ; ODD-PURE <=> ker K1 = ker K ; impasses des bornes grossières | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_odd_fixed_coupling.txt:1 |
| 388 | Branche globale « min c = 4 » : quotient des composantes à une racine ; énumération complète 2^21 -> 200 configurations ; couverture par 100 puis 79 templates | S | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/message_root_components_cd34d43.txt:2 |
| 389 | Branche min c = 4 : fermeture progressive des 79 templates (template 198 INFEASIBLE, puis 59 -> 64 -> 74 -> 75 -> 76/79 exclus ; restent 7, 9, 19) | S | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/message_root_cover79_72d47c3.txt:1 |
| 390 | Borne nécessaire rang_F7(8T44) <= 28 encodée exactement (M = UV sur F7, facteurs 44x28 et 28x44 indépendants) ; le minimum observé 30 n'est pas un théorème | P | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/message_rank7_423127b.txt:1 |
| 391 | Définition minimale des templates de composantes racine et extension nécessaire pour min c <= 3 | O | C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/codex_hmatch_20261016/codex_corner_tables_2134.txt:1 |
| 392 | Lemme universel E3 : aucun rectangle Q_ij autour d'un sommet n'a exactement 3 arêtes (sans hypothèse min c >= 4) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/tmp/bridge_codex_no_path4_20261017.txt:1 |
| 393 | Lemme des vecteurs courts propres -4 : //h//^2 >= m^2 + 7/m/ ; norme 14 => support = design 2-(7,4,2) (co-Heawood) ; inégalité de paire r^2 + s^2 + 7(r+s) + 2e(r+s+1) + 2c <= N + 4 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/tmp/bridge_codex_short_vectors_20261017.txt:2 |
| 394 | Familles 7, 9, 19 de la branche min c = 4 : exclusions partielles de Gram (comptes 457/64/547 -> 456/17/508 -> 449/12/449), aucun template entier fermé ; verdicts sous réserve du bug du 18/10 | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/tmp/bridge_codex_global_minc_20261017.txt:1 |
| 395 | Portée des 76 exclusions : valables seulement dans la branche « minimum GLOBAL c >= 4 » ; plusieurs utilisent c >= 4 sur des droites non racines ; dichotomie correcte pour c >= 3 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/tmp/bridge_codex_20261018_reply970.txt:3 |
| 396 | Saut de difficulté pour c = 1 : si toutes les droites racine ont c = 1, C devient l'incidence non orientée de K7 et dim ker C = 14 (au lieu de <= 4) | H | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/tmp/bridge_codex_20261017_2317.txt:9 |
| 397 | Cas six-prismes (famille 7) : H60 = union disjointe de 20 triangles et de six couplages parfaits ; budget 51 laisse <= 3 arêtes ligne/colonne sur les 9 rectangles inter-parts | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/tmp/bridge_codex_20261018_0024.txt:9 |
| 398 | Coût annoncé de la campagne v2 (familles 7, 9, 19) : 909 Gram, 84637 codes sans preuve, nominal 4232 CPU·h, sans garantie de clôture ; 5,5 GiB de RAM de pointe par travailleur | H | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/data/codex_line_resonance_20261016/bridge_20261018_0326.txt:1 |
| 399 | Coordination CPU : plafond utilisateur 80 % ; un calcul case1_coheawood.py (attribué au LAB par hypothèse) faisait monter la charge à 70-77 % | H | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/tmp/bridge_codex_cpu_20261017_0236.txt:1 |
| 400 | Recherche par cubes alpha = 22 a 99 (cubes_alpha99) : en pause sans verdict | O | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/code/asym243/hoffman/cubes_alpha99/STATUS.txt:1-5 |
| 401 | Question S3 a 243 (revetements S3 de Brouwer-Haemers) : cubes de parite arretes, classes cls00-cls03 UNKNOWN | O | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/code/asym243/s3grid/STATUS.txt:1-2 |
| 402 | Specifications de sous-structures pour les stabilisateurs a 243 (stab_specs, stab_specs2) | H | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/code/asym243/stab_specs.txt:1-8 |
| 403 | Table des points fixes d'automorphismes d'ordre premier impair dans la famille srg(v,k,1,2) (sortie de nesting.py) | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/code/family_nesting/nesting_output.txt:1-44 |
| 404 | Audit Codex de l'unicite de completion depuis le bord de Hoffman de BvLS : INCOMPLET, non reproduit | O | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/data/codex_hoffman_boundary_audit_20261012/boundary.txt:1-199 |
| 405 | Integration par Codex du message LAB 567 (theta-LP, NOTE 17.101 et 17.99) : bases co-Heawood, estimation de Knuth, echelle de rang | H | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/NOTE_INTEGRATION_LAB567_2026_10_12.md:1-30 |
| 406 | Echelle de rang (LAB, relayee par Codex) : aux rangs 37, 39, 41 un vecteur de norme 18 ou 26 ; au rang 43 ces normes ou >= 1316 vecteurs de norme 16 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/NOTE_INTEGRATION_LAB567_2026_10_12.md:32-39 |
| 407 | Comptes de mondes de norme 16 (Codex 254, 256, 260) : sous-comptes non cumulables ; trois supports N16 exclus au rang 37 par LAB | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/NOTE_INTEGRATION_LAB567_2026_10_12.md:54-87 |
| 408 | Modele global co-Heawood (12/10) : CP-SAT UNKNOWN a 3601 s (deux portefeuilles), CaDiCaL sans verdict a ~3,35 M conflits | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/NOTE_SUIVI_SOLVEURS_2026_10_12.md:39-169 |
| 409 | Lemme des onze couvertures distinctes (coclique de Hoffman de taille 22) | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_first/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_COUVERTURES_HOFFMAN_2026_10_12.md:9-47 |
| 410 | Lemme de multiplicite d'une paire de blocs : f_ij >= 2 - z_ij + D_ij ; resolution de dix lignes imposee par les voisins | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_first/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_COUVERTURES_HOFFMAN_2026_10_12.md:49-108 |
| 411 | Re-explication des 36 designs exclus anterieurement par le lemme des onze couvertures | E | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_first/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_COUVERTURES_HOFFMAN_2026_10_12.md:110-124 |
| 412 | Exclusion d'une famille a bord variable (design 37c3bb63972f, quatre points libres {3,4,5,6}) | S | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_first/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_COUVERTURES_HOFFMAN_2026_10_12.md:126-162 |
| 413 | Exclusion de la famille a cinq points libres {3,4,5,6,7} du design 37c3bb63972f (parcours exhaustif + certificats rejoues) | C | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_first/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_COUVERTURES_HOFFMAN_2026_10_12.md:164-221 |
| 414 | Six points libres {3,4,5,6,7,8} : non termine ; obstacle suivant identifie (resolution de dix lignes) | O | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_first/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_COUVERTURES_HOFFMAN_2026_10_12.md:222-245 |
| 415 | Portee au-dela d'une coclique de Hoffman : les voisinages fermes exterieurs d'une coclique quelconque sont des couvertures doubles lineaires distinctes | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_first/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_COUVERTURES_HOFFMAN_2026_10_12.md:247-264 |
| 416 | Loi de propagation des defauts pour TOUTE coclique : A q = 3q + 2 delta 1 | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:28-66 |
| 417 | Reduction au support des defauts : un bord commun de petite taille (equations (3), (4)) | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:77-105 |
| 418 | A 21, aucun sommet exterieur n'a six ou sept voisins dans la coclique ; filtre t(t+1) + 2 max(0, 3t - 2 delta) <= 2 delta(delta + 5) | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:107-124 |
| 419 | Lemme d'extension 21 -> 22 : une coclique de 21 dont tout sommet exterieur a au plus quatre voisins dans C se prolonge en une coclique de 22 | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:9-26 |
| 420 | Fait des six sommets : un sous-graphe induit a six sommets d'un srg(99,14,1,2) a au plus neuf aretes, egalite seulement pour le prisme triangulaire | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:144-156 |
| 421 | Cocliques de 21 maximales : sept profils de degres (a,e) dans {(0,2),(0,3),(0,4),(0,5),(0,6),(1,2),(1,3)} | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:173-204 |
| 422 | Charge d'une composante propre du support : w < 0 ou w > 18 delta | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:279-308 |
| 423 | Structure forcee du profil (0,2) : H = C4, quatre X sur ses aretes, huit Y ; borne (7) sur la densite des defauts negatifs ; branche (1,3) avec E = K3 EXCLUE par parite | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:310-385 |
| 424 | Pilotes et populations du profil (0,2) : populations precises exclues ; certificats entiers (8) ; boucle de separateurs ; aucune exclusion de famille | C | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:206-255 |
| 425 | Lemme des paires saturees (d_uw + d_vw <= 1) ; certificat 99 <= 97 ferme l'ancien survivant population_003 ; coupure de famille (12) | C | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:588-666 |
| 426 | Le profil (0,2) se reduit a onze repartitions de cycles (partitions de 6) ; multiensemble residuel determine par le bord (13)-(14) | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:668-732 |
| 427 | Exploitation sur noyaux variables (0,2) : temoins necessaires dans chacune des onze repartitions ; pas d'exclusion | E | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:734-805 |
| 428 | Bords variables : lemme des facteurs simultanes, capacites des triangles fermes, loi de capacite (16), coexistence par paires mais pas a trois (8 <= 7), bipartition des types doubles (17)-(18) | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:828-1005 |
| 429 | Obstruction arithmetique sans hypothese de coclique : pour tout bord induit B et des poids entiers z, Q >= (2k+1)T - (99 - /B/)k(k+1) (19) ; egalite => chaque colonne forcee (20)-(21) | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:1007-1083 |
| 430 | V5 : partage effectif des copies ; cycles sans corde (5 <= 4) ; chemin biparti impossible (22) ; 304 conditions apprises | C | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:1084-1240 |
| 431 | V6 : un bord unique 61/38 pour TOUT le profil (0,2) ; modele exact sur 99 sommets UNKNOWN | S | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:1272-1316 |
| 432 | Theoreme de fermeture d'une factorisation binaire : toutes les completions d'un bord B avec un voisinage complet et D fixe sont E = E0 + 3P - 7Q, Q projecteur dans ker D, E entiere ; l'integralite force 0/1 | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:1318-1438 |
| 433 | V7 : theoreme affine - au plus 2^delta completions d'un bord (B, D) ; delta = dim V_D <= h(h-1)/2 ; seules delta equations quadratiques a verifier | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:1481-1577 |
| 434 | Conditions necessaires supplementaires (37)-(39) : coexistence des colonnes, aretes residuelles non couvertes formant une partition en triangles | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:1578-1647 |
| 435 | Loi de defauts pour les ensembles reguliers (grilles) : sum_R q = b(36 - c) - 7/R n C/ ; toute grille rencontre toute coclique 21 maximale ; le C4 H de (0,2) n'est dans aucune grille ; coupes (40)-(41) | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:1648-1700 |
| 436 | V8 : corps convexe K(B,D) (section de fantope) dont les points ENTIERS sont exactement les completions ; critere global (47) G_-(A) >= 0, G_+(A) >= 0 equivalent a srg(99,14,1,2) pour A entiere symetrique avec A1 = 14.1 | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:1852-2012 |
| 437 | V9 : budgets de moments residuels (51) et calibration de six essais de 3 min (tous UNKNOWN) | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:2133-2277 |
| 438 | V10 : fermeture par les plafonds (lemme) ; partition exhaustive du profil (0,2) en 61 branches (a, b, classe(t)) | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:2279-2366 |
| 439 | Propagation du defaut mixte : B G = G E ; critere de fermeture si W_E = [1, E1, ..., E^(m-1)1] inversible ; colonnes feuilles (56a)-(56b) | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:2368-2451 |
| 440 | Campagne AWS du 13/10 (c7a.32xlarge, ~4,44 USD) : 255 recherches courtes du profil (0,2), TOUTES UNKNOWN | S | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:2499-2581 |
| 441 | V11 : identite d'energie par colonne //g//^2 = d^t(2B + I)g ; lemme de fermeture entiere (Bg = 0 ou Bg = -g => g = 0) ; corollaires (E coclique ou clique ferme le systeme) | P | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:2583-2725 |
| 442 | Echange avec Claude (LAB, messages 593-596) : budgets de triangles redondants ; affirmation provisoire du message 595 retiree par Claude (message 596) | X | C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:2727-2774 |
| 443 | V15 : un bord positif de 43 sommets (3I - B + J/9 > 0) se complete par au plus 8192 affectations de signes puis au plus DEUX completions etiquetees, isomorphes ; tout Conway possede un tel bord ; bord 44 positif : completion unique | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1471-1493 |
| 444 | V14 : toute difference non nulle de rang 2 entre deux matrices srg(99,14,1,2) est exactement une transposition de deux sommets ; unicite pour h <= 2 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1495-1511 |
| 445 | V13 : theoreme de completion etendu a TOUT bord binaire (sans voisinage complet) ; la correction w = 1 - (5/14)D^t 1 sur le support 4-regulier de norme 18 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1513-1527 |
| 446 | V12 : normalisation constructive des quatre voisinages H du profil (0,2) (couverture 840) ; aucune branche exclue | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1529-1541 |
| 447 | Consignes de l'utilisateur (Dilan) consignees par Codex : s'eloigner des exclusions rang par rang (12/10) ; deux chercheurs sans verification croisee systematique, objectif construire un srg asymetrique a lambda = 1 (14/10) | H | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1449-1469 |
| 448 | (A) fausse et germes A non prolongeables (acceptes) ; compressions de U definies positives sur les secteurs exterieurs : 100 coupes lineaires strictes | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1425-1447 |
| 449 | Famille G1 : rang trivial >= 6 - min(c_l, c_m), donc rang T <= 30 impose nullite non triviale >= 9 - min(c) ; reduction c = (5,5) non-grille : 126 cas sur 972 | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1403-1423 |
| 450 | Point P = 0 du census d'ordre 9 (rationnel puis ENTIER) : le census d'ordre <= 9 ne donne aucune borne inferieure sur P | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1392-1401 |
| 451 | Plancher entier grossier Q = 1047816 - 96P - 24Z + Delta et recollement : copies agregees possibles mais non recollees | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1381-1390 |
| 452 | Lemme de l'espace impair d'UNE droite : Q = tau_a + tau_abar - sigma - sigma^t, //Q// <= 4 ; les deux diagonales T = 6I - Q et U = 8I + Q sont toujours definies positives ; interface census | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1369-1379 |
| 453 | Contraintes pour tout prolongement de la famille c55 non grille, puis EXCLUSION de la famille locale G1 c55 non grille par rang_F7(8T_S) >= 29 | E | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1337-1367 |
| 454 | Budget global des relations mixtes sans G1 : sum m >= 6804, au moins 336 des 2079 drapeaux ont m >= 4, au moins 18 sommets | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1323-1335 |
| 455 | T2 (ODD9) par reseau pondere : rang T_X = 23 - c via un laplacien L8 ; 'S10 laplacien a poids positifs' FAUX | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1290-1303 |
| 456 | Compression h-paire A22 : rang A = 10 <=> multiplicite 11 de 12 dans 4R (matrice entiere non negative 22x22) ; au moins 10 paires hors diagonale strictement positives | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1265-1281 |
| 457 | Cout exact des cassures de h et tests de moyenne : //Delta//_F^2 = 4b = 8//B//_F^2 ; borne <= 4096 essais par moyenne (64 si degres 2) ; criteres d'orientation | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1174-1263 |
| 458 | Fausse symetrie g = h p : D = K - gKg = J4 x (M - pMp)/8, rang D = 10 - 2c ; le defaut de rang 2 seul ne force pas le plafond 13 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1157-1172 |
| 459 | G1'' : normalisation sous T >= 0 (C4 force F, 96 interfaces) puis NOUVELLE EXCLUSION : degre interne d_P <= 1, cubes casses c_m >= 4 exclus sans enumeration | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1123-1155 |
| 460 | Coupes PSD exactes et projection exacte de C2 (outils de certification) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1083-1121 |
| 461 | EXCLUSION de toute la famille LOCALE <z, hM> (z = (4 6 8 10 12)(5 7 9 11 13), h = (0 1)(2 3), M = tous les retournements exterieurs) : null_Q T <= 14 et a 14 rang_F7(8T) >= 29 | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1049-1081 |
| 462 | <z, hM> : corrections et filtres arithmetiques (min c = 2 prouve ; filtre mod 5 ; filtre ramifie) ; 'absence de relations mixtes' RETIREE | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:995-1047 |
| 463 | Axe asymetrique sans symetrie : relations de cote = c_l + c_m + 2 - delta ; cible 14 <=> rang R <= 7 + c_m sans ODD9 ; obstacle dimensionnel au forcage d'un h p | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:972-993 |
| 464 | Coupe binaire 48 (theoreme sans symetrie) : e(O u S) <= 48 au lieu de 49 sous C1, binaire et T PSD seulement | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:939-962 |
| 465 | ODD9 universelle REFUTEE (acceptation par Codex des 58 exemples de LAB) ; SUM14 universelle refutee ; mecanisme exact a, b, s ; famille finie exacte de 120 remariages PSD | R | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:853-913 |
| 466 | (NG7) : P <= 852 => au moins 18 droites t <= 7 et au moins 254 blocs NON-GRILLE contenant une telle droite ; correction de la note 100 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:820-851 |
| 467 | Theoreme de cloture des relations de noyau par les composantes des reseaux deux-etoiles ; perte d'au moins une nullite sur un segment PSD grille -> non-grille | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:798-818 |
| 468 | Rang de Schur et moments : pour exclure nu >= 14 quand c_l = 1..4, il suffit des bornes 9, 10, 11, 12 ; hors grille e(O) <= 3 donne seulement rang T >= 23 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:783-796 |
| 469 | Preuve restreinte de C4DO (support <= 12) puis extension au support <= 14 : 832 coeurs interdits ; toute relation plate de ker T touchant O a support >= 16 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:729-781 |
| 470 | Obstructions de remariage pour les quasi-echecs n_45 et b_29 : temoins entiers w^t(4I + Gamma)w < 0 ; critere des remariages purs (P'v = -v sur W) | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:652-706 |
| 471 | HB_1 promu : nouvelle incidence sur le meme Gamma (T rang 30 / nu 14, U rang 39, H-MATCH intact) ; non prolongeable : le sommet (4,6) n'a aucune colonne binaire (Farkas) ; theoreme global T + U = 7 Pi | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:594-650 |
| 472 | Reparation de coeurs : coeur 30 (T25/U30) FERME par projection globale sur 84 (CP-SAT INFEASIBLE 25,3 s) ; inegalite signee e(P7) + e(N8) - e(P7,N8) <= 14 ; 398 inegalites universelles T/U certifiees | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:476-527 |
| 473 | Cinq etoiles : borne universelle de defaut D >= 12 (>= 3 lignes cassent h ; en general D >= max(0, 2k - 16)), puis >= 4 des 8 lignes ; private_Y(x) + deg_P(x) <= 4 ; cadre global de 12 lignes construit | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:529-592 |
| 474 | Lemmes phi sur les appariements reels ; cadre de 15 lignes completes sur 84 ; le temoin 15 PROUVE non prolongeable par cinq lignes ; coupe universelle 58 aretes <= 57 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:416-474 |
| 475 | Couverture globale : modele exact du 99 sans germe (3486 aretes) ; avec une droite de t minimum <= 7 et un partenaire non-grille, 19 types POINTES couvrent tous les graphes ; bornes <= 2 suffisantes | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:387-414 |
| 476 | Equivalence PSD globale : sur 84 labels avec Gamma binaire et tous les C1 exacts, T et U PSD suffisent a tous les C2 (sans imposer de rang) ; centre fractionnaire Gamma0 | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:364-385 |
| 477 | Synthese famille-asymetrie (LAB921) : identite de variance des composantes ; une grille laisse (k-4)(k-14)/2 sommets sans voisin ; critere exact 'moins de completions etiquetees que /Aut(bord)/ interdit une completion asymetrique' | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:342-362 |
| 478 | Reduction de resonance (LAB925) : nu(T44) = c(l) + 2 + corank(Q), rang(T44) = 23 - c(l) + rang(F) ; N9-NG <=> rang(F) >= 12 ; un Conway force rang(F) <= 11 (conflit conditionnel) ; 'corank(Q) <= 4' FAUX | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:326-340 |
| 479 | SYM6 : reduction exacte 10x10 (SYM6 <=> rang Z >= 3 ; ODDCONST <=> rang W = 9) ; identite de bord (laplacien a attaches, rang G = 11 - c(m)) ; borne d'energie paire E >= G/5 ; couplage U20 (rang K = 21 - c(l)) | P | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:260-324 |
| 480 | Branche globale min c = 4 : enumeration des quotients de composantes (2^21 -> 221 types -> 367 survivants / 200) : 97 infaisables, 103 possibles ; budget racine sum t(l) <= 51 : 100 -> 87 -> 79 gabarits | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:218-258 |
| 481 | Minimum OBSERVE rang_F7(8T44) >= 30 sur 3722 blocs NG (LAB941) : pas un theoreme ; borne <= 28 encodee par factorisation modulaire | H | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:207-216 |
| 482 | 18/10 : pilote c >= 3 '162/162 couplages INFEASIBLE au presolve' et anciens bilans : RETIRES par la correction OR-Tools (domain[-1]) ; c4 : 76/79 non touches, 7/9/19 rouverts | X | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:186-204 |
| 483 | 18/10 : certificat entier 3P + 4G <= 2772 ; racine minimisant 9s + 8g (score <= 504) ; branche minimum GLOBAL c(L) >= 4 fermee 79/79 par CP-SAT => tout Conway a une droite L avec c(L) <= 3 | S | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:129-185 |
| 484 | 18/10 soir : droite c <= 3 (huit positions, cas 7 UNKNOWN) ; gabarits 5128 et 4192 exclus (obstructions de moments, certificats entiers sans Gram) ; 8650 et gabarit 3 OUVERTS ; gz599 ferme 9/9 ; retrait LAB1076 | C | C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1-127 |

## 4. Routes fermées, et pourquoi

Notation : #NNN = `L07_C1_asym_local-NNN` dans le JSONL. Les sources précises sont dans le JSONL.

**Asymétrie et constructions**
1. **Mécanismes connus d'asymétrie appliqués à Conway** : fermés (#027, #033, #035, #056).
   - Pas de deux-graphe, car k = 14 ≠ 2μ.
   - Pas de commutation de Godsil-McKay à une classe pour k ≥ 14. Les commutations à plusieurs classes ne sont pas couvertes.
   - Aucun Conway symétrique n'existe à déformer.
2. **Fenêtre d'asymétrie aux ordres 1 et 2** : fermée (#040, #042-#045).
   - Le cadre a un déficit de 30 dimensions.
   - Aucun flip n'est un automorphisme pour m ≥ 3, et la majorité q ≥ ⌈t/2⌉ s'impose.
   - La symétrie forcée meurt au premier recollement.
   - Deux impasses sont vérifiées : « les quasi-symétries sont exactes » et « les pièces rigides sont nombreuses » (#045).
   - Reste « l'abondance » : il faudrait une borne supérieure de solutions sous l'ordre du groupe, sans méthode connue.
3. **Construire un λ = 1 asymétrique par une route structurée** : fermé (#048-#052, #058). Quatre voies tombent :
   - à 243, les graphes sont rigides et il n'y a pas d'hôte GQ, puisque le GQ(8,10) connu n'a pas de 3-ovoïde ;
   - à 378, les hémisystèmes sont classifiés et le stabilisateur minimal est S3 ;
   - les échanges locaux sur le graphe 378 demandent de libérer plus de 85 % des sommets ;
   - la symétrie par rareté ferme tout hôte dont le groupe dépasse le nombre de solutions.
4. **Variante « ensembles conservés irréguliers » de Codex à 243** : elle ne redonne que les 7 graphes connus, pour 54, 45 et 42 sommets conservés et une à trois graines (#038). À ne pas refaire.
5. **Route du réseau Q pour α = 22** : pas d'obstruction au niveau des discriminants, les 271 designs passent (#120).
6. **« Balance ⇒ (A) impossible »** : ce n'est pas la bonne route (#117).
   - Le mécanisme du triangle demande la graduation Z3 de K_{9,9,9}, qui manque à K11.
   - La relaxation réelle n'est pas concluante.
7. **Cartes D7 et holonomie** (ChatGPT/Sol) (#133).
   - La branche triviale redonne Makhnev/L1.
   - La branche non triviale a déjà été explorée sans contradiction.

**Routes finies et solveurs**
8. **« Route (C) » à la C2 pour C1** : il n'y a pas de classification de rang ≤ 24, et la masse en rang 48 vaut ≈ 1,5·10¹²¹ (#128).
9. **Route Ω à coût maîtrisé** : l'étage colonnes coûte ≥ 1,7·10¹⁰ h CPU (#132).
   - Kissat ne retrouve même pas l'instance réelle de BvLS.
   - La route reste finie (#129), mais elle n'est pas abordable.
10. **Recherche par types locaux à un sommet** : environ 10⁵⁰ types, et les types aléatoires ne sont pas réfutés (#015).
    - Moments de degré 4 et 5 et moments mixtes : aucun gain sur 588/59 (#011).
    - Moyenne sur le schéma local : aucune borne (#016).
11. **Route a₄ pour b = 34 (rang 35)** : a₄ > 1,42·10⁷ serait nécessaire, et l'on n'en prouve qu'environ 3,6·10⁶ (#024).
12. **Découpage brut de la cinquième étoile** (#105).
    - Avec le modèle actuel, le coût dépasse 1 000 h CPU sans borne supérieure.
    - R8 pur est extrapolé à 5·10⁷-10¹² heures-cœur (#107, NOTE_R8_ROUTE du lot L08).
    - La « barrière au 7ᵉ label » était fausse (#107).

**Lois locales à quatre étoiles**
13. **Lois locales spectrales tirées des données : toutes réfutées.**
    - Lois en cause : (H3) (#063), (H4) (#064), (A) (#065), (A4) et les plafonds de relations mixtes ≤ 2, ≤ 3, ≤ 6 (#072), (N9), (NOGRID), (LOW) (#073), (R7) (#071), ODD9 (#077), KER-SYM universelle, SUM14 et « une saturation » (#092).
    - Raison commune : les conditions locales (T, U ⪰ 0, rang) ne testent que la réalisabilité spectrale (#081). Chaque loi venait d'une seule famille symétrique et tombait dès la première famille indépendante.
14. **(H-MATCH) par la voie locale** (#086). La route est déclarée épuisée le 16/10 à 08:00.
    - Ses données (≈ 1,14 M structures) ne sont pas des blocs de Conway, car aucune base ne s'étend (#103).
15. **Calibration des lois à quatre étoiles sur srg(243)** : ce banc d'essai ne convient pas (#087).
    - L'échec des analogues y est automatique.
    - Le « c » n'y a pas le même sens.
    - Les blocs y sont rigides.
16. **Conditions locales mod 3 et mod 5** (15U mod p) : trop faibles (#100).
17. **Familles sans h** (#090).
    - G1'' est trop grande et parquée.
    - <Z5, hM> est exclue par Codex : rang_F7 ≥ 29.

**Cadre coclique**
18. **Le cadre coclique seul ne ferme pas C1** (#001).
    - L'exclure ne donnerait que α ≤ 20.
    - « Coclique de Hoffman ⇒ symétrie » est faux (HOF-003, #115) : un srg(25) asymétrique a trois cocliques de Hoffman.

## 5. Questions ouvertes, classées par levier

**A. Énoncés qui excluraient Conway s'ils étaient prouvés (implications prouvées)**
- (H-MATCH), ou sa forme forte (H-INV) (#084-#086). Il manque un argument binaire, C1 ou C2 contre la saturation simultanée des deux contractions (Codex, #099).
- (N9-NG), ou ses formes minimales (NG5) et (NG7), (NG14) (#096, #097). Le cas le plus dur est c(l) = 4, ν ≤ 13. Lemmes intermédiaires : ODDCONST + EVEN', SYM + QUOT (#098).
- (T8) ou (T15), le pont des transversales, avec P ≤ 852 (#079, #095).
- (B') plus (C) (#078).
- R8 UNSAT (#107), ou la non-existence d'une structure admissible à cinq étoiles (#105).
- Les 8 positions de la petite droite c ≤ 3 (Codex, 18/10, sous-lot B1).
- (SQ30) + (N15) (#076, #079) : la combinaison perd son intérêt, puisque (SQ30) est un artefact de h ; (N15) seule reste plausible.
- (K22) (#079) : elle exclurait le rang 37, ou 37 et 39.
- Conjecture (P) « toute arête est dans un prisme » (#037, #124) : elle n'exclut que le profil P = 0.
- Cubes α = 22 : SAT donnerait un Conway, UNSAT donnerait α ≤ 21 (#119).

**B. Lemmes techniques ouverts (ce qu'ils donneraient)**
- (S1) ν = 14 ⇒ N = hN ; (S2) N = hN, ν = 14, PSD ⇒ aucune torsion ; (KER-SYM-13/14) ; (FAKE-13) (#091, #092). Ensemble ils donneraient (H-MATCH).
- Borne d'absorption « un g_y non transversal n'est jamais absorbé » (indice : 4,2516 < 4,5) (#080). Avec ODD9, qui est réfutée, c'était le programme (T8).
- C4DO générale, SYM, QUOT (#098) ; ODD9-NG, EVEN3-NG (#096).
- K7 aux 22 points d'une coclique de Hoffman (#121, #116).
- Balance pour les revêtements à fibres-grilles (#117) ; régime mixte de L25 (11 grilles) (#135, #137).
- Conjecture S : Aut(K_x, x) = Aut(G)_x hors des droites plates (#042). Elle est vraie sur les quatre graphes sans étalement à 243.
- (G), (E), (L2), (P) sur F_x et B_xa (#124, #037). Elles sont peut-être des artefacts de la famille des revêtements de BH.
- « Les couplages en un sommet déterminent-ils un srg(243) ? » (#037). Coût estimé : 30 min à quelques heures par sommet, non lancé.
- Le rang plein 44 des 49 lignes N[l] ∪ N[b] est le cas générique, pas un fait prouvé (#044, #055).

**C. Comptage contre symétrie** (lien avec la borne 99 × 645 120)
- Il faudrait une borne supérieure du nombre de complétions d'un cadre, ou de solutions d'un problème hôte, inférieure à l'ordre du groupe qui agit librement (#045, #055). Aucune n'existe dans le lot.

**D. Constructions**
- S3-revêtement de BH : un srg(243) asymétrique à étalement régulier (#123, #134).
- Un λ = 1 asymétrique hors hôte, et les paramètres ouverts (115,18,1,3), (495,38,1,3) (#047, #053).

**E. Certification**
- DRAT pour T1 (≈ 45 min) et kk6 (≈ 2,5 h), non lancés (#012, #013).
- DRAT par cas pour toute exclusion à cinq étoiles, avec deux modèles et une relecture (#105).
- Estimation de Knuth pour les 34 cas (#112).

## 6. Contradictions, redécouvertes, résultats remplacés ou retirés

**Redécouvertes** (même résultat établi deux fois ; dates)
- **Fenêtre de rang 7-adique.** La nuit des 13-14/10 donne rang_F7(A + 4I) impair ≥ 35 (#022). C'est plus faible que la fenêtre {37, …, 43} du 08/10, où r = 35 était déjà exclu (CONWAY_CONSTRAINTS D1, D7). La parité de rang_7 est L2 (24-25/09), puis la note 172 §2 (11/10), puis NOTE_NIGHT 19.1 (14/10) (#020, #120, #137).
- **T1 (aucun sommet sur 21 grilles), 14/10 (#012)** = L8 de Codex, démontré à la main le 25/09 (#137). Codex et LAB l'établissent encore une fois indépendamment pendant la nuit du 14/10 (sous-lot B1).
- **Grille 3×3 = code parfait (F5, 14/10, #009)** = L5 / G1, septembre (#137).
- **Sous-cas « 11 grilles disjointes ».** Codex, note 104 (~25/09, L25 : régimes purs exclus) ; puis note 166 (11/10, #135) ; puis famille SPREAD de NOTE_NIGHT 18.5 (14/10, #019). « Alignement total impossible » : L25 Thm B (25/09), note 168 §4 (11/10, #117), NOTE_NIGHT « c = 990 impossible » (14/10).
- **Principe de symétrie forcée.** Note 171 §7 et dossier HOFFMAN (11/10, #119, #115), puis LAB (14/10, #032).
- **Rigidité de Godsil-McKay dans la famille (1,2).** Elle est rapportée pour k ≥ 8 le 07/10 (structures lab, #137), puis NOTE_SPREADFREE §2 (12/10), puis LAB k ≥ 14 (14/10, #033).
- **Paley(25)** : 15 graphes, 2 asymétriques, deux-graphes, GM, certificats (#026-#028). Déjà connus : Paulus-Rozenfeld 1973, page de Brouwer, dossier externe du 11/10 (#114). Seuls sont nouveaux §6.3, la lecture « 3888 contre 6 » et le lemme du flip.
- **Critère de rigidité spectrale.** Note 165 §1 et §8.1 (11/10, #134), puis lemme d'eigen-rigidité de LAB (14/10, #039). Le critère de concentration (#050) l'affine.
- **Bornes de prismes et de grilles.** P ≤ 1151 (L16, septembre) est redérivé par Codex pendant la nuit sans anciennes notes (#010). De même ρ ≤ 191 alors que ρ ≤ 126 existait déjà (sous-lot B1).
- **Identité t₂ = (m−1)E − 3t₃ (note 177, #124)** = n₃ = 3(P_max − P) des notes 60 et L15 : autre preuve (note 178 §3).
- **Critère global sur 84 labels de Codex (16/10, #109)** : variante de l'équivalence (★) de la note 157 (06/10, #129).
- **Coupe W(B7) sur le modèle enraciné (#054)** : la technique existait sur d'autres modèles. Elle est nouvelle sur le modèle complet, mais partielle.
- **« Toute différence de rang 2 entre deux Conway est une transposition. »** Codex, V14 du 13/10, l'établit en général (`Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1495-1511`, sous-lot B2). LAB, le 14/10, ne traite que les vecteurs {0, ±1} (#057) : antériorité et généralité reviennent à Codex.
- **« Une grille 3×3 est un code parfait. »** Codex l'utilise comme acquis des dossiers C2 dès les 12-13/10 (sous-lot B2). C'est aussi L5 et G1, puis F5 de la nuit du 14/10 (#009).
- **Contre-exemple à 66 triangles** contre la borne SOS d'arXiv 2610.16266. Il est trouvé à la fois par Codex et par theesfeld (Zenodo 23399271, 15/10), puis repris par LAB (#082) (sous-lot A : `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23399271_RELEASE.txt:8`).

**Contradictions entre notes**
- **Attribution de la route Ω.** NOTE_ASYM_WINDOW l.28 et CONWAY_CONSTRAINTS G1 disent « Codex's route Omega (note 157) ». Or la note 157 est signée « Claude », session cloud du 06/10, selon la PASSATION du 07/10 (#129).
- **« N ≤ 9 grilles deux à deux disjointes »** (NOTE_PROOFS P11, l.78, #061). NOTE_NIGHT 18.5 étudie 11 grilles disjointes, et le sous-cas (A) en suppose 11. Le contrôle du chantier, non relu, donne : Gram des 11·1_G − 1 = 1089I − 99J, PSD ⇔ N ≤ 11. La borne 9 semble une coquille, utilisée nulle part.
- **Nuit des 13-14/10 dans l'audit.** AUDIT_EXCLUSIONS l.61 écrit « rang_F7(A + 4I) ≥ 33 », alors que le théorème final de NOTE_NIGHT (26.4) donne ≥ 35 (#110).
- **Census d'ordre 9** (ρ ≤ 126, P ≤ 852). « Non reproduit par LAB » selon N9_REDUCTION (15/10, nuit). « Retrouvé par mon LP » selon THREE_RESULTS (15/10, soir). Codex (18/10) signale une dérivation LAB indépendante du 08/10 (#073).
- **Chaîne de littérature des symétries** (#111, #138, #146).
  - CONWAY_CONSTRAINTS B1 : « MM04 : une involution force |Aut| | 42 ». Il précise que « un premier divisant |Aut| vaut 2 ou 3 » était un raccourci.
  - Note 162 : « Behbahani-Lam : tout premier divisant |Aut| vaut 2 ou 3 ».
  - REVUE et asymmetric.tex : « MM04 : |Aut| | 2·3³·7·11 ; BL11 exclut 7 et 11 par calcul ».
  - asymmetric.tex marque ces attributions comme non relues dans les articles (TODO). Elles sont à vérifier à la source.
- **Nombre de germes DISC.** EXT84 l.20 : 643 germes + HB. EXT84 l.41 et REVUE : 645. Codex (J:6196) : 643. Écart d'une ou deux unités, à recompter (#100).
- **Statut de « (H-MATCH) abandonnée ».** Écrit le 15/10 à 07:40, retiré à 10:00 (refus de l'utilisateur) (#086).
- **Fin de la nuit H-MATCH.** La copie git (b0cc3de) donne « 413 classes, ≈ 853 000 structures ». La copie fs y ajoute l'addendum de 08:06 : « 414/416, ≈ 1,14 M » (#086).
- **NOTE_ASYM_PALEY : horodatages.** Copie git : 12:40, 12:40-13:30, 13:45-14:30. Copie fs : 11:45, 12:00, 12:30. Les heures git sont postérieures au commit d46f057 de 12:46 UTC (#026).
- **Numérotation de Paley(25).** Spence pour LAB (asymétriques #2 et #4) ; fichier de McKay pour le dossier externe (#7 et #13) (#114).
- **Statut divergent de l'exclusion « G1 c55 non-grille : rang_F7 ≥ 29 > 28 ».**
  - E : énumération exacte de 145 152 cas, selon AGENTS.md:1337-1353 et le message `codex_c55_excluded_after774.txt:1` (sous-lots A et B2).
  - C : selon CONWAY_CONSTRAINTS G13 (l.84).
  - P : selon le journal de nuit de Codex (J:3226-3301, sous-lot B1).
- **« Bord de Hoffman de BvLS ⇒ BvLS »** (note 171, #118). L'audit de Codex s'est arrêté incomplet : l'affirmation repose sur un seul calcul (sous-lot B2).
- **Homonymies, à respecter pour l'appariement automatique** (sous-lot A).
  - Chez Codex, « C1, C1′, C2 » sont des conditions locales de comptage (degrés, plafonds λ, μ), pas les cas C1/C2 du projet.
  - « R7 » a trois sens : la loi de rang réfutée (#071), un lemme de l'attaque N9-NG (#098), la cible SAT « 4 étoiles + 7 labels » (#107).
  - « N9 » a deux sens : le théorème des 9 sommets à 17 arêtes (#017, intact) et la loi (N9) à quatre étoiles (#073, réfutée).
  - Dans le JSONL, « T1 » désigne le théorème de la nuit (#012) et, ailleurs, une cible de NOTE_ASYM_WINDOW.

**Résultats remplacés ou retirés**
- **(X) Interprétations de calibration srg(243) du 15/10 (07:15-07:40)** : « l'analogue de (H-MATCH) est faux, donc (H-MATCH) perd son crédit » et « l'analogue de (B') est faux ». Retirées à 08:00 (#087).
- **(X) « No combination of these results can ever exclude Conway »** (THREE_RESULTS §2, 15/10). Retiré à 19:05 (#095). C'est la reprise d'une phrase de la note 100 (25/09, #141), elle-même retirée par Codex (sous-lot B1).
- **(X) « Barrière au 7ᵉ label »** (16/10, matin). Retirée le soir : R7 est SAT (#107).
- **(X) Lecture « un INCONNU à cinq étoiles n'est pas un indice »**, fondée sur un encodage CP-SAT défectueux. Remplacée par l'indice étalonné (#106).
- **(R) ODD9**, présentée comme vérifiée partout dans la nuit du 14-15/10, est réfutée le 15/10 à 17:05 (#077). La programmation (B') ⇐ ODD9 tombe, et (B') reste ouverte.
- **(X) Lecture 3 de la note 171** (« chercher un asymétrique sans coclique de Hoffman »). Retirée le 11/10 (#118).
- **(X) Filtre « w − h pair » de la note 172.** Retiré, car h = 22 − w toujours (#120).
- **(X) Formulation de 15:55 sur KER-SYM** (« ne peut porter une preuve »). Retirée à 16:10 (#092).
- **Bug OR-Tools 9.15 du 18/10.** Sont retirés la fermeture 79/79 de 04:28, les 162 verdicts c3 et la campagne AWS c3star (sous-lot B1). Aucun résultat LAB des 13-16/10 n'utilise l'outil fautif, selon le sous-lot B1 : `root_component_rotated_gram.py` n'est jamais appelé dans le journal des 14-16/10.

## 7. Dépendances : sur quels maillons non vérifiés reposent les exclusions conditionnelles

- **Tout le levier d'asymétrie** (#032, #040, #045, #055, #119) suppose Aut(Conway) = 1. Cette hypothèse repose sur quatre maillons :
  - C2 : assisté par ordinateur, contrôlé seulement par des IA ; recertification des transferts annoncée faite le 11/10 ;
  - C3 : Lean 4, sans relecture humaine ;
  - C7 : Lean, accepté en local sans bac à sable ;
  - la littérature MM04 et BL11 (ordres 7 et 11 par ordinateur), non relue dans les articles (#146, #147, #111).
- **(H-MATCH) ⇒ pas de Conway (#084)** demande L8 (preuve de Codex, note 105, sans relecture humaine), ou Makhnev 1988 (littérature, lu par Codex), ou ρ ≤ 191 (L16). G18 demande en plus L10 (g(x) ≤ 17, à la main). La variante à six droites demande kk5 (C, DRAT ; encodeur contrôlé mais non certifié).
- **(N9), (N9-NG), (NG5), (T8) ⇒ pas de Conway** (#073, #096, #079) demandent ρ ≤ 126 ou P ≤ 852. Ce sont des certificats exacts d'ordre 9 de Codex ; une dérivation LAB indépendante existe selon Codex (18/10).
- **(NG7)** demande en plus l'argument des 254 blocs (#097), relu par LAB.
- **DISC (#070)** : sa partie 7-adique demande L2 et L22 (Codex). Sa partie robuste (premiers ≠ 2, 7) est indépendante.
- **rang_7 ≤ 28** pour les blocs (#071), et les exclusions de familles G1 c55 et <Z5, hM> (#090) : elles demandent L22 (k ≤ 28).
- **Rang ≥ 35 de la nuit (#022)** : lemmes à la main.
  - §17-21 : relus par un agent.
  - §25-26 (b = 30, 32) : non relus.
  - Comptes de sous-graphes vérifiés sur srg(243) ; certificats de Farkas vérifiés exactement.
- **Exclusions à cinq étoiles (#103-#105)** : DRAT pour HB seulement. Les autres bases ont seulement deux verdicts de solveurs.
- **Branche c ≥ 4 (Codex, 18/10)** : une chaîne CP-SAT sans certificat UNSAT portable d'ensemble, plus 19 DRAT et un certificat entier 3P + 4G ≤ 2772 (sous-lot B1).

## 8. Matériaux pour la recombinaison (lot principal : notes LAB, branches v7 et astra, premiers documents C1)

Les sous-lots A, B1 et B2 ont chacun leurs propres listes (§10). Mises bout à bout, toutes ces listes couvrent le lot.
Statuts : X = statut de l'hypothèse ; ⇒ = statut de l'implication.

### 8.1 Énoncés conditionnels « si X alors exclusion / contradiction »

| # | X (précis) | conclusion | X | ⇒ | source |
|---|---|---|---|---|---|
| R1 | (H-MATCH) aux 21 paires de droites d'UN sommet. Pour toute paire (l, m), le bloc à quatre étoiles admissible avec T, U ⪰ 0 et nullité ≥ 14 vérifie M_1 = h(M_0) et M_3 = h(M_2), où h = (0 1)(2 3) et M_a est le couplage sur les 12 labels {a, y} | le sommet est un point de Hamming : contradiction avec L8. Appliqué partout : contradiction avec Makhnev 1988 et avec ρ ≤ 191 | O | P (relu par un agent) | `work/stars_rank_2026-10-14/H_MATCH_REDUCTION_2026-10-15.md:33-64` |
| R2 | (H-MATCH) aux 15 paires de six droites d'un sommet | point de Hamming, via kk5 (DRAT) et L8 | O | P | id. l.74-80 |
| R3 | (H-INV) : tout bloc PSD de nullité ≥ 14 est h-invariant | (H-MATCH), donc pas de Conway | O | P | id. l.31 |
| R4 | (S1) ν = 14 ⇒ N = hN, et (S2) N = hN, ν = 14, PSD ⇒ aucune torsion | (H-MATCH) | O | P | `work/stars_rank_2026-10-14/MECHANISM_A_2026-10-15.md:24-29, 340-341` |
| R5 | (KER-SYM-14) + (FAKE-13) + lemme 6h | (S1) | O | P | id. l.266-269, 340-341 |
| R6 | (N9) : nullité ≤ 9 + min(c(l), c(m)) pour tout bloc PSD, plus le census ρ ≤ 126 | c(l) ≥ 5 + δ partout, ρ ≥ 154 > 126 : pas de Conway | **R** | P | `work/stars_rank_2026-10-14/N9_REDUCTION_2026-10-15.md:32-39` |
| R7 | (NOGRID) + (LOW), ou (N9) + (NOGRID) | pas de Conway, sans census | **R** | P | id. l.70-78 |
| R8 | (N9-NG) : bloc PSD SANS grille sur (l, m) ⇒ nullité ≤ 9 + min(c(l), c(m)) ; avec P ≤ 852 ou ρ ≤ 126 | toute droite a c ≥ 5, g ≥ 4, t ≥ 8, d'où P ≥ 924 > 852 : pas de Conway | O | P (vérifiée par Codex) | `work/stars_rank_2026-10-14/THREE_RESULTS_2026-10-15.md:91-106` |
| R9 | (NG5) : bloc non-grille PSD de nullité ≥ 14 ⇒ c(l), c(m) ≥ 5 | idem R8 | O | P | id. l.105-106 |
| R10 | (NG7) : aucun bloc non-grille avec min(t(l), t(m)) ≤ 7 ne passe les tests de bloc de Conway | pas de Conway (≥ 254 tels blocs forcés) | O | P (Codex ; relu par LAB) | id. l.118-126 |
| R11 | (NG14) : aucun bloc PSD non-grille de nullité ≥ 14 ne passe rang_F7 ≤ 28, DISC et l'extension | pas de Conway, avec Makhnev seul | O | P | id. l.80-85 |
| R12 | (T8) : nullité ≥ 14 ⇒ t(l) ≥ 8 et t(m) ≥ 8 ; variante (T15) t(l) + t(m) ≥ 15 | P ≥ 924, ou P ≥ 866,25 ; avec P ≤ 852 : pas de Conway | O | P | `work/stars_rank_2026-10-14/AUDIT_EXCLUSIONS_2026-10-15.md:46` ; `THREE_RESULTS:57-61` |
| R13 | « au moins une droite avec t ≥ 8 » | P ≥ 792 : n'exclut rien | — | P | `AUDIT_EXCLUSIONS:139-140` |
| R14 | (K22) : nullité ≥ 14 ⇒ rang_7(8T_S4) ≥ 23 ; variante ≥ 25 | k ≥ 24 : r = 37 exclu ; avec ≥ 25 : r = 37 et 39 exclus | O | P | `AUDIT_EXCLUSIONS:47` |
| R15 | (SQ30) + (N15) (aucun bloc PSD de nullité ≥ 15) | pas de Conway | (SQ30) artefact h ; (N15) O | P | `AUDIT_EXCLUSIONS:48-49, 95-96` |
| R16 | (B') : aucun bloc PSD de nullité ≥ 14 n'a une droite avec c = 1 ; avec (C) : tout Conway a une droite non spéciale | pas de Conway. (B') seule donne « toute droite est spéciale » | O, O | P | `AUDIT_EXCLUSIONS:44, 52` |
| R17 | ODD9 (gain impair exactement 9) | c(l) ≥ 2 + δ, toute droite spéciale, (B') | **R** | P | `NOTE_PROOFS_1410.md:356-364` |
| R18 | (A) : trois étoiles, c(l) = 1, T, U ⪰ 0 ⇒ rang 31 ; avec (C) | pas de Conway. (A) seul donne (B) | **R** | P | `NOTE_PROOFS_1410.md:461-468` |
| R19 | (H3) + L8 | (visé) pas de Conway. Insuffisant même vrai : un bloc à trois étoiles a le rang 30 − δ′ | **R** | — | `AUDIT_EXCLUSIONS:24, 37-39` |
| R20 | (H4) : aucun bloc à quatre étoiles PSD | pas de Conway | **R** | P | `NOTE_STARS_RANK.md:83-98` |
| R21 | (R7) : PSD à quatre étoiles ⇒ rang_7 ≥ 29 ; variante « ≥ 23 » | contradiction avec k ≤ 28 (L22) ; la variante exclurait k = 22 (r = 37) | **R** | P | `NOTE_PROOFS_1410.md:262-264` |
| R22 | plafond « ≤ 2 relations mixtes » ; « ≤ 3 » | ρ ≥ 198 > 191 ; ρ ≥ 154 > 126 | **R** | P | `NOTE_PROOFS_1410.md:316-318` |
| R23 | aucune structure admissible à 5 étoiles (52 labels), ou les 34 cas M_4 tous UNSAT | pas de Conway (il faudra DRAT par cas, un modèle indépendant et une relecture) | O | P | `EXT84_2026-10-16.md:118-126` ; `REVUE_GLOBALE:32-38` |
| R24 | R8 UNSAT (4 étoiles exactes + les 8 labels {4, t}, lettre 4 bornée) | pas de Conway | O | P (modèle jugé solide le 20/10, lot L08) | `REVUE_GLOBALE:333-340` |
| R25 | un germe h-relié en (l, m) s'étend à une 3ᵉ droite n que M_0 n'apparie pas | contre-exemple exact à (H-MATCH) | — | P | `EXT84_2026-10-16.md:52-61` |
| R26 | le cadre coclique (22 de Hoffman et 21 maximales, sept profils) est exclu ET α ≥ 21 est prouvé | pas de Conway | O (α ≥ 21) | P | `work/c1_coclique_frame_2026-10-13/NOTE_COCLIQUE_FRAME.md:5-11` |
| R27 | échelle de rangs (NOTE du 12/10, 17.101 (6), lot L06) : aux rangs 37, 39, 41, vecteur propre entier de −4 de norme 18 ou 26 ; au rang 43, norme 18, 26 ou ≥ 1316 vecteurs de norme 16 | exclure ces supports exclurait C1 | O | cité (statut au lot L06) | `NOTE_COCLIQUE_FRAME.md:43-44` |
| R28 | b = 30 (rang 31) | B contient un vecteur entier de −4 de norme ≤ 18 ; ≤ 20 si b = 32, 34 ; ≤ 24 si b = 36-40 ; ≤ 26 si b = 42 | E (sans certificat) | — | `work/c1_night_2026-10-14/NOTE_NIGHT.md:437-439` |
| R29 | a₄ > 1,42·10⁷ (ou 1,31·10⁷ avec a₅ ≥ 3·10⁷) ; a₃ > 9,8·10⁵ ; a₅ > 3,0·10⁸ | b = 34 (rang 35) exclu | non atteignable par les comptes connus | E | `NOTE_NIGHT.md:548-561` |
| R30 | une pièce H FORCÉE dans un Conway, avec c complétions et \|Aut(H)\| > c | pas de C1. Une pièce forcée à complétion unique doit être rigide | dépend de B5 | P | `work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md:236-238` ; `NOTE_ASYM_WINDOW.md:14-17` |
| R31 | un groupe H préserve TOUTE l'instance (contraintes et clauses de blocage), avec une borne U < \|H\| sur le nombre de complétions | instance exclue (action libre) | — | P (Codex) | `work/lambda1_construction_2026-10-14/SOLVER_CAMPAIGN_STATE.md:74-78` |
| R32 | deux flips simples indépendants préservent l'instance, et l'instance a au plus 2 complétions (résidu spectral de rang ≤ 1) | la branche est fermée (multiple de 4 exigé) | — | P (Codex) | id. l.76-78 |
| R33 | α = 22 et un design Y à complétion unique avec Aut(Y) ≠ 1 | le graphe n'est pas asymétrique, donc pas de C1 | — | P | `conway99-c1:origin/claude/v7-simultaneous:notes/171_BORDS_SERRES_HOFFMAN.md:195-201` |
| R34 | la balance vaut en général pour les revêtements à fibres-grilles | le sous-cas (A) (11 grilles) est impossible | O | P | `…/notes/169_DEUX_PISTES_SOUS_CAS_A.md:33-36, 68-75` |
| R35 | conjecture (P) : toute arête est dans un prisme | t₃ ≥ 231, t₂ ≤ 3465 : exclut le profil sans prisme | O | P | `…/notes/177_STRUCTURE_ARETE_B.md:50-53` |
| R36 | V7 : énumération exhaustive de O_x puis O_y UNSAT pour les 5 849 couples représentants | le sous-cas V7 est fermé | O | P | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/155_V7_CLASSES_MOD7_ET_GERMES.md:135-141` |
| R37 | aucun S3-revêtement de BH n'existe | tout srg(243,22,1,2) à étalement régulier a un automorphisme d'ordre 3 (hors Conway) | O | P | `…/notes/175_QUESTION_S3_ETALEMENT_243.md:56-59` |
| R38 | Conway n'existe pas | tout automorphisme d'ordre 5 d'un srg(494019) fixe exactement un Paley(9), et tout automorphisme d'ordre 7 fixe un seul sommet | — | P | `…/notes/174_EMBOITEMENTS_FAMILLE_1_2.md:99-102` |
| R39 | un sous-graphe induit H à 45 sommets avec det(A_H − 3I) ≠ 7^(30−k) n², ou à 55 sommets avec det(A_H + 4I) ≠ 2·7^(40−k) n² | H n'est dans aucun Conway (test DISC) | — | P | `NOTE_PROOFS_1410.md:332-349` |
| R40 | un bloc principal de 8T avec rang_7 > k (≤ 28) | ce n'est pas un bloc de Conway | — | P (L22) | `NOTE_PROOFS_1410.md:254-264` |
| R41 | K7 en tout point d'une coclique de Hoffman | Σ_c Σ_{e<f} n_ef² = 22·21 (équivalence) | O | P | `…/notes/173_CONJECTURE_K7.md:73-75` |
| R42 | ODDCONST(m) + EVEN′ (dim P₀ ≤ 7) ; ou (SYM) + (QUOT : ν(A++) ≤ 7 + min c) | (N9-NG) du côté l | O | P | `N9NG_ATTACK_2026-10-15.md:16-23, 58-86` |
| R43 | (SYM) seule | (NG5) à min c = 1 | O | P | id. l.79-86 |
| R44 | **combinaison** de V15 (Codex, 14/10) et du principe de symétrie forcée. V15 : tout Conway a un bord positif H de 43 sommets (3I − B + J/9 > 0) à au plus 8192 affectations de signes et au plus 2 complétions étiquetées, isomorphes. Un bord positif de 44 sommets a une complétion unique | dans un Conway asymétrique, tout bord positif de 44 sommets a Aut(H) = 1, et tout bord positif de 43 sommets a \|Aut(H)\| ≤ 2. Un tel bord inévitable avec \|Aut\| ≥ 2 (44) ou ≥ 3 (43) exclurait C1 | le bord symétrique inévitable manque | V15 : P (Codex) ; principe : P. La combinaison est énoncée comme manque par Codex (« il manque un même bord inévitable… », AG:353-355) et explicitée ici par le chantier | `Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:1474-1486, 353-355` ; #032 |
| R45 | sur le bord positif de 43 sommets, plus de deux choix de signes | force un vecteur propre de −4 de norme 14, donc un co-Heawood disjoint du bord et deux cocliques de 22. Sans co-Heawood (notamment si α ≤ 20), au plus deux choix | — | P (Codex) | `AGENTS.md:1487-1490` |

### 8.2 Bornes quantitatives (objet, inégalité, statut, source)

**Complétions de cadres et de pièces** (à comparer avec la borne de symétrie forcée)
- **Cadre Φ_x d'un sommet** : Aut(Φ_x) = W(B₇), d'ordre 2⁷·7! = 645 120. Dans un Conway (Aut = 1), le cadre a **au moins 99 × 645 120 = 63 866 880 complétions étiquetées**, chaque sommet donnant une orbite libre. P. Source : `NOTE_ASYM_WINDOW.md:32-33, 54-56`.
- **Données F_x** : au moins |Aut(F_x)| complétions, avec |Aut(F_x)| ≤ 645 120. P. Sources : `NOTE_ASYM_PALEY.md:231-235` ; `CONWAY_CONSTRAINTS.md:31`.
- **Pièces à trois étoiles rigides d'un Conway** : 8316 = 99 × 7 × 12, deux à deux non isomorphes. P. Source : `NOTE_ASYM_WINDOW.md:150-152, 155-157`.
- **Premier niveau de la route Ω** : 10¹¹ à 10¹² structures à deux étoiles à symétrie près. Il faudrait le confronter aux ≥ 99 orbites libres de solutions enracinées. Une borne supérieure inférieure à ce nombre serait une exclusion, mais aucune méthode n'est en vue. H. Source : `NOTE_ASYM_WINDOW.md:107-109`.
- **Hôtes λ = 1** (symétrie par rareté). E/P. Source : `RIGIDITY_LAMBDA1.md:120-124`.
  - FTWKB(5) : |K| = 9·10⁶ contre N = 3 180 000 hémisystèmes étiquetés ;
  - H(3,25) : ≈ 5,9·10¹⁰ contre ≈ 7,7·10⁶ ;
  - BH, Z₃-voltages : 233 280 contre 1154.
- **srg(243), bords de blocs** : 5ᵉ graphe, bloc 2 : |Aut(bord)| = 3888 contre 6 complétions ; 6ᵉ graphe : bloc 0, 108 contre 6 ; bloc 1, 54 contre 1 (rigide). E. Source : `NOTE_ASYM_PALEY.md:161-170`.
- **Rapport Aut(F_x)/Aut(G)_x à 243.** E. Source : `NOTE_ASYM_PALEY.md:176-186`.
  - BvLS : 81 749 606 400 / 15 840 = 5 160 960.
  - Graphes 5 à 8 : 1.
- **BvLS, bords de triangle** (E, dossier externe) :
  - lointain seul : 180 libres, 2 complétions ;
  - lointain + 1 prisme : 186 libres, 16 complétions ;
  - lointain + 2 prismes : 192 libres, **27 648 = 13 824 × 2 = 2·(4!)³** complétions ;
  - lointain + 3 paires mates : 2 complétions ;
  - Γ₃ + 1 prisme : 8 complétions ;
  - 3 prismes : ouvert (domaines 3 645 / 1 895).

  Source : `…/dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/RESULTATS.md:21-27`.
- **Paley(25), bord K₅** : 1 999 872 complétions étiquetées. Par classe, N = #K₅·5!·2¹⁰/|Aut(G)|, soit 368 640 pour chaque classe asymétrique. Échelle de bords : 10, 9, 8 sommets fixes → 2 classes ; 7 → 4 ; 6 → 12 ; 5 → 15. E. Source : `…/PALEY_ASYMETRIE_DOSSIER/RESULTATS.md:63-103, 204-219`.
- **Design de Hoffman de BvLS** : 1 complétion (198 sommets libres ; 38 826 candidats de lignes). S/E. Source : `…/notes/171_BORDS_SERRES_HOFFMAN.md:90-108`.
- **Graphe 378 à groupe S3** : complétion unique jusqu'à 229 sommets libres (unions de X_m) ; un échange demande environ 280 sommets libres (≤ 98 conservés). E/P. Source : `NOTE_LAMBDA1.md:33-75`.
- **Note 165 §7, candidats par ligne de la région lointaine de BvLS** : sommet ≥ 2000 ; arête ≈ 1750-2000 ; ligne 2 ; deux lignes 1 ; grille 1. E. Source : `…/notes/165_SRG243_REVETEMENTS_ET_SYMETRIE.md:166-177`.

**Rigidité et vecteurs propres**
- **Changement d'une paire** (critère de concentration) : P_ii P_jj ≥ 1/(2(r − s))² ; au plus 4(r − s)² P_ii paires changent en i. Valeurs : 1/900 à 378 ; **1/196 pour Conway**. P. Sources : `NOTE_LAMBDA1.md:46-58` ; `RIGIDITY_LAMBDA1.md:58-62`.
- **Vecteurs de paires** : support 2 + 2(k − μ) = 26 pour Conway (90 à 378, 42 à 243). Un échange de rang 2 sur un vecteur {0, ±1} exige une norme 2(r − s) = 14. Pour Conway, aucun échange de rang 2 sur les vecteurs co-Heawood ni sur les H7. P. Source : `RIGIDITY_LAMBDA1.md:67-112`.
- **Région lointaine d'un triangle de Conway** : dim E₃(F) ≥ 15, dim E₋₄(F) ≥ 5. P. Source : `…/notes/165:223-227`.
- **Déficit du cadre (rang sur E_θ moins 2m)** : 0 pour srg(9) ; **30 pour Conway** ; 88 à 243. N[l] : déficit 8 ; N[l] ∪ N[b] (49 sommets) : rang 44 générique. P. Sources : `NOTE_ASYM_WINDOW.md:35-47, 130-136`.

**Comptes forcés dans tout Conway**
- **Prismes d'une droite** : 0 ≤ p ≤ 12 ; n₀ = 32 − p, n₁ = 144 + 3p, n₂ = 36 − 3p. P. Source : `NOTE_NIGHT.md:24-26`.
- **Moyenne des prismes** : p̄ ≤ 588/59 < 10 ; P ≤ 1151. P (Codex, relu par LAB). Source : `NOTE_NIGHT.md:101-103`.
- **Arêtes d'un s-ensemble** : e(S) ≤ 3, 5, 7, 9, 12, 14, 18, 19 pour s = 3..10 ; jamais e(S) = 17 pour s = 9. P. Source : `NOTE_NIGHT.md:256-313`.
- **Sous-graphes induits à 4 sommets** : C4 2079, patte 8316, triangle + K1 13860, griffe 27720, P4 91476, P3 + K1 507276, 2K2 126819, K2 + 2K1 1517670, 4K1 1469160. P (vérifiés sur srg(243)). Source : `NOTE_NIGHT.md:507-508`.
- **Couches des réseaux A, B** (P) :
  - a₂ ≥ 462 ; a₄ ≥ 14970, puis ≥ 354816 et ≥ 1 749 546 (le certificat utilise 1 749 210) ;
  - a₃ ≥ 24948 ; a₅ ≥ 196812 et ≥ 3 415 104 ; a₆ ≥ 10 869 012 ; a₇ ≥ 6 503 112 ; a₈ ≥ 1 555 092 ;
  - c₇ ≤ 7920 (Codex : ≤ 792) ; c₈ ≤ 360 360 (amélioré à 304 920) ;
  - paires de prismes jumeaux ≤ 8625 (Codex : ≤ 2871) ; min B ≥ 14.

  Source : `NOTE_NIGHT.md:373-547, 585-601`.
- **Fenêtre de rang** : rang_F7(A + 4I) impair et ≥ 35. C. Le 08/10 : {37, 39, 41, 43}. L22 : ≤ 43, soit k ≤ 28. L20 ter : ≥ 25. Sources : `NOTE_NIGHT.md:547` ; `CONWAY_CONSTRAINTS.md:52`.
- **Relations mixtes** (P) :
  - nullité T_S4 = 14 + δ ;
  - relations mixtes = 12 − c(l) − c(m) + [grille] + δ ; ≥ 1 ; ≥ 10 si les deux droites sont non spéciales ;
  - Σ sur les 2079 paires ≥ 12474 − 45ρ ≥ 6804.

  Sources : `NOTE_PROOFS_1410.md:35-40, 174-176` ; `CONWAY_CONSTRAINTS.md:85`.
- **Blocs et transversales** (P) :
  - 2079 blocs, dont 9ρ blocs de grille ;
  - blocs non-grille : ≥ 4 par sommet, ≥ 396 en tout ; ≥ 945 avec ρ ≤ 126 ;
  - moyenne de t(l) + t(m) ≤ 14,75 ; moyenne de t ≤ 7,38 ; |W(x)| moyen ≥ 32,4 ;
  - ≤ 170 droites avec t ≥ 10 (programme) ;
  - ≥ 254 blocs non-grille avec min t ≤ 7 (Codex).

  Sources : `THREE_RESULTS_2026-10-15.md:51-61, 118-126` ; `AUDIT_EXCLUSIONS:166`.
- **Sous-cas (A), 11 grilles** : le graphe transverse a exactement 5544 pentagones ; l'holonomie de pentagone a en moyenne 1 point fixe. P. Source : `…/notes/168:44-51`.
- **α = 22** (P) :
  - design 2-(22,4,2) : 231 paires à 2, 1540 à 1, 1155 à 0 ;
  - D = M (154 arêtes) ∪ T (77 triangles) ;
  - a + b impair ; 12 déterminants possibles dans la fenêtre ;
  - K7 donnerait 2141 classes, soit plus de 700 heures-CPU.

  Sources : `…/notes/171:125-140` ; `…/notes/172:85-95` ; `…/notes/173:33-48`.
- **Points fixes d'un automorphisme d'ordre premier impair** : |Fix|·(k − k′) ≤ v − |Fix|. P. Source : `…/notes/174:33-35`.
- **Cinq étoiles** (P, Codex et LAB) : D ≥ 12 ; au moins 4 des 8 lignes {4, y} cassent h ; capacité Σκ = 8 exactement ; graphe Ω de 36 arêtes ; paires de X ≤ 28 − a ; n₁ + n₂ ≥ 8 + a. Sources : `EXT84_2026-10-16.md:128-147` ; `REVUE_GLOBALE:370-386`.
- **Codes et automorphismes locaux** (P) :
  - motifs de flips : distance ≥ ⌈t/2⌉, au plus 8 automorphismes de ce type pour t = 7 ;
  - im_F2(A) de dimension 54, poids ≥ 8 ;
  - mots binaires de ker₇(A + 4I) de poids 0, 63 ou 77.

  Sources : `NOTE_ASYM_WINDOW.md:113-120` ; `NOTE_PROOFS_1410.md:79-82` ; `…/notes/178:6-23`.

**Tailles d'espaces de recherche et données de familles** (H/E : mesures, pas des bornes prouvées)
- Types locaux ≈ 10⁵⁰. T1 : 1 889 568 choix, 588 classes. kk6 : 1971 classes. kk5 : 19 classes. SPREAD : plus de 10²⁷ cas (`NOTE_NIGHT.md`).
- Structures de triangle C : ≈ 5,2·10¹⁶ étiquetées, ≈ 1,5·10¹¹ classes. 10¹⁹ bijections par paire de couches, 10⁻²⁵ solution attendue. Étage colonnes ≥ 1,7·10¹⁰ h CPU (`…/notes/163`).
- Branche 18 : 2,75·10¹⁰ configurations étiquetées, ≈ 8,4·10⁹ à symétrie près, ≥ 2,3·10⁶ h CPU. Masse du genre de rang 48 : 1,5·10¹²¹ (`…/notes/156`).
- V7 : 13 812 couples ; 1 828 tués ; 5 849 représentants ; 546 109 paires Bx–Zx (`…/notes/155`).
- Quatre étoiles :
  - 331 objets de rang 30 ; 645 germes ;
  - 287, puis 416, classes de noyaux ; ≈ 1,14 M structures ;
  - classe obj53 : 15 936 structures (96 PSD, 9408 cassées) ;
  - <Z5, hM> : 339 556 structures, 192 PSD, nullité ≤ 9 ; G1'' : 26 811 cubes ;
  - 280 424 visites PSD avec une droite c = 1, nullité ≤ 10 ;
  - 800 408 visites PSD ; ≈ 288 000 à nullité 14, aucune à 15.

  Sources : `AUDIT_EXCLUSIONS`, `H_MATCH_REDUCTION`, `HMATCH_NIGHT`, `EXT84`.
- Cinquième étoile :
  - 34 orbites M₄ (groupe d'ordre 3072) ; 18 cas lancés, tous en TIMEOUT à 90 min ;
  - ≈ 3,5·10⁴ cubes (M₄, M₀) pour plus de 1 000 h CPU ;
  - R8 : 52 labels, 1326 arêtes, lex-leader à 3071 éléments, 52 classes M₀.

  Sources : `EXT84`, `REVUE_GLOBALE`.

### 8.3 Lemmes ouverts ou étapes manquantes, et ce qu'ils donneraient

- **Preuve de (H-MATCH)** : elle donnerait « pas de Conway ». Il manque un argument binaire, C1 ou C2 contre la saturation simultanée des deux contractions T et U. Sous-étapes ouvertes : (S1), (S2), (KER-SYM-14), (FAKE-13) (`HMATCH_NIGHT:91-101` ; `C1_REDUCTION_OUTLINE:33-35` ; `MECHANISM_A:336-343`).
- **Preuve de (NG5), (NG7) ou (N9-NG)** : elle donnerait « pas de Conway ». Le cas le plus dur est c(l) = 4, avec nullité ≤ 13 à prouver. Sous-étapes : ODDCONST, EVEN′, SYM, QUOT, C4DO générale (`N9NG_ATTACK:129-137`).
- **Borne d'absorption** (un g_y non transversal n'est jamais absorbé) : avec ODD9, elle donnait (T8) pour c(l) = 2. Comme ODD9 est réfutée, il faut une autre première moitié (`AUDIT_EXCLUSIONS:141-170`).
- **Borne inférieure sur P**, ou un plafond de torsion non moyenné : tous les lemmes L1-L25 sont des planchers. Une impossibilité à cinq étoiles « serait exactement ce plafond » (`REVUE_GLOBALE:111-118`).
- **Existence d'une structure admissible à cinq étoiles**, ou R8 : elle déciderait le problème. Il faudrait renforcer le modèle (équilibre, coupes PSD paresseuses, N9, tuiles, lex-leader), puis faire une estimation de Knuth (`REVUE_GLOBALE:270-289`).
- **α ≥ 21** : avec l'exclusion des cocliques 22 et 21, il fermerait C1 (`NOTE_COCLIQUE_FRAME:10-11`).
- **K7** sous α = 22, avec la classification ternaire en six types : il imposerait 2141 classes en chaque point. Aucune preuve (`…/notes/173`).
- **Balance**, ou une orientation compatible avec K11 : elle fermerait le sous-cas (A). Régime mixte de L25 (`…/notes/169-170`).
- **Borne supérieure du nombre de complétions** d'un cadre ou d'une pièce forcée, sous l'ordre du groupe qui agit librement : elle exclurait C1 par le principe de symétrie forcée. Aucune méthode sans énumération (`NOTE_ASYM_WINDOW:154-160`).
- **Un mécanisme qui transporte une symétrie forcée à travers les 30 dimensions manquantes** du cadre : c'est le second ordre et au-delà (`NOTE_ASYM_WINDOW:97-99`).
- **Conjecture S** : Aut(K_x, x) = Aut(G)_x hors des droites plates. **Unicité des complétions de K_0** dans Γ₆ et Γ₈ (Codex) (`NOTE_ASYM_WINDOW:77-84`).
- **Chaîne de littérature des symétries** à vérifier dans les articles originaux, avant toute rédaction (`C1_REDUCTION_OUTLINE:8-9` ; `asymmetric.tex:8-9`).
- **Certificats** :
  - DRAT pour T1 et kk6 ;
  - DRAT par cas pour toute exclusion à cinq étoiles ;
  - contrôle positif CNF du modèle enraciné sur BvLS, demandé le 24/09 (`LAB_INSTRUCTIONS_C1.md:13-20`) ; son exécution n'est pas documentée ici.

### 8.4 Méthodes employées dans un cas et transférables (ou dites transférables)

- **Principe de symétrie forcée / lemme d'extension** (complétions = orbites libres de Aut(pièce)). Cas : Paley 9, deux-graphes, mouvements GM, échanges à 243, α = 22 (note 171), cadres de Conway. Il vaut pour toute la famille srg(2m² + 1, 2m, 1, 2) (`NOTE_ASYM_PALEY.md:188-195` ; `…/notes/171:195-201`).
- **Critère de rigidité spectrale ou de concentration** (D = (r − s)(P − P′)). Il vient de la chirurgie spectrale à 243 (note 165), et sert à 378 (LAB) et à 99 (D = 7(P′₃ − P₃)) (`…/notes/165:209-212` ; `NOTE_LAMBDA1.md:45-75`).
- **Reconstruction à bord fixé avec un moteur de lignes et des transports** (dossiers Paley et BvLS). La note 171 §2 juge transposable « le choix d'un bord serré » (Hoffman), pas le moteur lui-même (`…/notes/171:36-52`).
- **Programme thêta exact sur M₂₂(Γ₀(7)) avec certificats de Farkas** : il produit les exclusions de rang de la nuit. Le niveau 63 est proposé avec les vecteurs de sommets ; même famille d'outils que le theta-LP du 07/10 (lot L06) et la « mission C2 sans calcul » (formes modulaires) (`NOTE_NIGHT.md:350-401, 481-492`).
- **Classes de carrés (DISC)** : déjà utilisées par Codex (notes 205-247) et par LAP/LAB le 08/10 ; appliquées aux objets à quatre étoiles et aux germes. Le lemme est général pour toute matrice entière de rang r (`NOTE_PROOFS_1410.md:332-349`).
- **Familles à symétrie imposée comme générateurs de témoins** : Z5h, G1, h, hM, τ, Klein. Méthode efficace pour RÉFUTER des lois locales ; leçon : il faut tester chaque loi dans plusieurs familles indépendantes (`BILAN_NUIT:12-15` ; `AUDIT_EXCLUSIONS:35-37`).
- **Contrôles positifs sur les vrais srg(243,22,1,2)** : encodeur srg_sat, modèle à cinq étoiles validé SAT à 4, 5 et 6 étoiles, comptes de sous-graphes, DISC. Mises en garde de la calibration (#087) : vérifier que le phénomène existe au même niveau d'étoiles, et que la comparaison n'est pas automatique (`EXT84:92-94` ; `H_MATCH_REDUCTION:151-197`).
- **Lemme des points fixes d'ordre premier impair** : transférable entre 9, 99, 243, 6273 et 494019 (`…/notes/174`).
- **Équations exactes de recollement et lemme des tuiles / N9**, sous forme de clauses courtes que CDCL ne trouve pas. Elles sont proposées pour renforcer le modèle à cinq étoiles (`REVUE_GLOBALE:207-212`).
- **Coupe lex-leader de W(B7)** (partielle, 49 éléments) et **lex-leader strict en C1** (aucune complétion n'est fixée par une symétrie non triviale). La technique vient de Codex (27/09), de C3 et de C2 (route C) (`SB_NOVELTY_CHECK.md` ; `SOLVER_CAMPAIGN_STATE.md:72-80`).
- **Obstruction de parité par un noyau doublement pair sur F₂** (Codex, 3-ovoïdes de GQ(8,10)). Elle ne s'applique pas à 378 ; elle est applicable à d'autres m-ovoïdes (`NOTE_LAMBDA1.md:91-101`).
- **Critère 2-adique S5**, à d'autres paramètres de la table de Brouwer. **Critère p = 3** de C3-experimental, à des actions libres d'ordre 3 pour d'autres paramètres (`…/notes/162:16-25, 49-50`).

## 9. Notes lues, survolées et non lues (couverture des 356 entrées du lot)

Pour les index que j'ai traités moi-même : 89 lus, 34 survolés, 59 non lus (avec la raison). Les index des sous-lots A (145 fichiers), B1 (5) et B2 (24) ont leur état détaillé, index par index, dans les tableaux de couverture des §10.1-10.3. Bilan déclaré par ces sous-lots :
- A : 138 lus, 4 survolés, 3 non lus ;
- B1 : 5 sur 5 lus entièrement, dont les 6824 lignes du journal de nuit de Codex ;
- B2 : voir son tableau ; les fichiers de littérature tierce 189-197 sont identifiés, pas lus.

Non lus délibérément :
- journaux bruts de calcul, quand la note qui les cite en donne le résultat ;
- données (listes de Spence, solutions SAT, matrices) ;
- métadonnées pip ;
- PDF et textes d'articles tiers ;
- manuscrits C2 et C3, qui relèvent d'autres lots (seulement titres, résumés et statuts déclarés).

Fichiers lus hors du lot pour vérifier un point : NOTE_R8_ROUTE.md l.1-60 (lot L08) ; les journaux r8/sb/*.log du dépôt conway99-c1 ; AGENTS.md l.350-356 et 1471-1493.

| index | première localisation | état | détail |
|---|---|---|---|
| 0 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:JOURNAL.md` | survolé | journal C1 (origin/main) : l.3-608 (24-26/09) survolées par les lignes de résultats en gras ; l.609-673 (06-11/10) lues |
| 1 | `conway99-c1:origin/claude/v7-simultaneous:README.md` | lu | README C1 (branche v7) |
| 2 | `fs:c1-asymmetry-audit/LAB_INSTRUCTIONS_C1.md` | survolé | l.1-40 (gel des solveurs du 25/09, priorités du PC du labo) |
| 3 | `fs:c1-asymmetry-audit/README.md` | survolé | copie du README C1 dans c1-asymmetry-audit ; différences avec la version git non examinées ligne à ligne |
| 4 | `fs:c1-asymmetry-audit/data/.k3_patterns_lf.txt` | survolé | données (motifs k=3), en tête seulement |
| 5 | `fs:c1-asymmetry-audit/data/k2_patterns.txt` | lu | données (4 motifs k=2) |
| 6 | `fs:c1-asymmetry-audit/data/k3_patterns_fast.txt` | survolé | données (motifs k=3) |
| 7 | `fs:c1-asymmetry-audit/data/k3_results.txt` | lu | résultats UNSAT des motifs k=3 (20 premières lignes) |
| 8 | `fs:c1-asymmetry-audit/rapport/RAPPORT_C1.md` | survolé | RAPPORT_C1 du 24/09 : l.1-27 et 185-235 (en bref, méthode, verdicts, nouveautés) |
| 9 | `fs:c1-lambda1-env/Lib/site-packages/pip-25.0.1.dist-info/AUTHORS.txt` | non lu | métadonnées pip de l'environnement virtuel c1-lambda1-env : hors sujet |
| 10 | `fs:c1-lambda1-env/Lib/site-packages/pip-25.0.1.dist-info/LICENSE.txt` | non lu | licence pip : hors sujet |
| 11 | `fs:c1-lambda1-env/Lib/site-packages/pip-25.0.1.dist-info/entry_points.txt` | non lu | métadonnées pip : hors sujet |
| 12 | `fs:c1-lambda1-env/Lib/site-packages/pip-25.0.1.dist-info/top_level.txt` | non lu | métadonnées pip : hors sujet |
| 13 | `fs:c1-lambda1-env/Lib/site-packages/pip/_vendor/vendor.txt` | non lu | liste des paquets vendus par pip : hors sujet |
| 14 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:PASSATION_C1_2026-10-07.md` | lu | PASSATION_C1_2026-10-07 (branche v7) |
| 15 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_asym_paley_2026-10-14/CONWAY_CONSTRAINTS.md` | lu | CONWAY_CONSTRAINTS.md (copie git identique à la copie fs) |
| 16 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_asym_window_2026-10-14/NOTE_ASYM_WINDOW.md` | lu | NOTE_ASYM_WINDOW.md (git = fs) |
| 17 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_coclique_frame_2026-10-13/NOTE_COCLIQUE_FRAME.md` | lu | NOTE_COCLIQUE_FRAME.md (git = fs) |
| 18 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/NOTE_NIGHT.md` | lu | NOTE_NIGHT.md (git = fs), 633 lignes |
| 19 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/core_log.txt` | non lu | journal brut cité par NOTE_NIGHT ; résultat repris de la note |
| 20 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/cube_reps.txt` | non lu | représentants des 588 classes de T1 (données) |
| 21 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/cubes_log.txt` | non lu | journal brut des 588 cubes (cité par NOTE_NIGHT) |
| 22 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/family_log.txt` | non lu | journal brut (une ligne : kk7 UNKNOWN 240 s) |
| 23 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/fulltype_log.txt` | non lu | journal brut (une ligne : type aléatoire UNKNOWN) |
| 24 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/h12_log.txt` | non lu | journal brut (H12 UNKNOWN 60 s) |
| 25 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/h16_log.txt` | non lu | journal brut (squelettes de norme 16, cités par NOTE_NIGHT 20.3) |
| 26 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/kk5_all_log.txt` | non lu | journal brut kk5 (cité par NOTE_NIGHT 16) |
| 27 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/kk5_certify_log.txt` | non lu | journal de certification DRAT kk5 (cité par NOTE_NIGHT 18.1) |
| 28 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/kk5_classes.txt` | non lu | classes kk5 (données) |
| 29 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/kk5_step_log.txt` | non lu | journal brut kk5 (deuxième passe) |
| 30 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/kk5_tiles_log.txt` | non lu | journal brut kk5 tuiles |
| 31 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/kk6_all_log.txt` | non lu | journal brut kk6 (1971 classes, cité par NOTE_NIGHT 14) |
| 32 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/kk6_classes.txt` | non lu | classes kk6 (données) |
| 33 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/kk6_log.txt` | non lu | journal brut kk6 (essais) |
| 34 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/kkN_probe_log.txt` | non lu | journal brut kkN |
| 35 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/pattern_log.txt` | non lu | journal brut (motif N9 UNKNOWN 100 s) |
| 36 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/prefix_log.txt` | non lu | journal brut (types aléatoires par préfixe) |
| 37 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/psi_reps.txt` | non lu | représentants des 790 classes psi (données) |
| 38 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/shell_counts_check2_log.txt` | non lu | contrôle des comptes sur srg(243) (cité par NOTE_NIGHT 28.1) |
| 39 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/shell_counts_check_log.txt` | non lu | contrôle des comptes sur srg(243) (cité par NOTE_NIGHT 25.5) |
| 40 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/spread_log.txt` | non lu | journal brut SPREAD UNKNOWN 280 s |
| 41 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/theta7_b30_log.txt` | non lu | journal brut programme thêta (b = 30) |
| 42 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/theta7_c8_log.txt` | non lu | journal brut programme thêta |
| 43 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/theta7_cert_log.txt` | non lu | journal des certificats de Farkas (cité par NOTE_NIGHT 19.3) |
| 44 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/theta7_cert_log2.txt` | non lu | journal des certificats régénérés (cité par NOTE_NIGHT 23) |
| 45 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/theta7_forced_min_log.txt` | non lu | journal brut programme thêta (vecteurs courts forcés) |
| 46 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/theta7_min_log.txt` | non lu | journal brut programme thêta |
| 47 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/theta7_need30_log.txt` | non lu | journal brut programme thêta |
| 48 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/theta7_ranges2_log.txt` | non lu | journal brut programme thêta (plages b >= 28) |
| 49 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/theta7_test2_log.txt` | non lu | journal des contrôles de Fricke (b = 0 mod 4) |
| 50 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_c1_night_2026-10-14/theta7_test_log.txt` | non lu | journal des contrôles de Fricke |
| 51 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_lambda1_construction_2026-10-14/NOTE_LAMBDA1.md` | lu | NOTE_LAMBDA1.md (git = fs aux fins de ligne près) |
| 52 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_lambda1_construction_2026-10-14/RIGIDITY_LAMBDA1.md` | lu | RIGIDITY_LAMBDA1.md (git = fs aux fins de ligne près) |
| 53 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_lambda1_construction_2026-10-14/SB_NOVELTY_CHECK.md` | lu | SB_NOVELTY_CHECK.md |
| 54 | `conway99-c1:origin/lab/exploration-2026-10-16:code…b_lambda1_construction_2026-10-14/SOLVER_CAMPAIGN_STATE.md` | lu | SOLVER_CAMPAIGN_STATE.md |
| 55 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/AUDIT_EXCLUSIONS_2026-10-15.md` | lu | AUDIT_EXCLUSIONS_2026-10-15.md (389 lignes) |
| 56 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/BILAN_NUIT_2026-10-15.md` | lu | BILAN_NUIT_2026-10-15.md |
| 57 | `conway99-c1:origin/lab/exploration-2026-10-16:code…b_stars_rank_2026-10-14/C1_REDUCTION_OUTLINE_2026-10-16.md` | lu | C1_REDUCTION_OUTLINE_2026-10-16.md |
| 58 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/EXT84_2026-10-16.md` | lu | EXT84_2026-10-16.md |
| 59 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/H_MATCH_REDUCTION_2026-10-15.md` | lu | H_MATCH_REDUCTION_2026-10-15.md (433 lignes) |
| 60 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/MECHANISM_A_2026-10-15.md` | lu | MECHANISM_A_2026-10-15.md |
| 61 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/N9NG_ATTACK_2026-10-15.md` | lu | N9NG_ATTACK_2026-10-15.md |
| 62 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/N9_REDUCTION_2026-10-15.md` | lu | N9_REDUCTION_2026-10-15.md |
| 63 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/NOTE_PROOFS_1410.md` | lu | NOTE_PROOFS_1410.md (471 lignes) |
| 64 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/NOTE_STARS_RANK.md` | lu | NOTE_STARS_RANK.md |
| 65 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/REVUE_GLOBALE_2026-10-16.md` | lu | REVUE_GLOBALE_2026-10-16.md (git = fs) |
| 66 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/THREE_RESULTS_2026-10-15.md` | lu | THREE_RESULTS_2026-10-15.md |
| 67 | `conway99-c1:origin/lab/exploration-2026-10-16:code…026-10-14/hmatch_tools_2026-10-15/oddonly_walks/README.txt` | lu | README des marches odd-only |
| 68 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/COORDINATION.md` | lu | COORDINATION du dossier BvLS (l.1-26) |
| 69 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/INTEGRATION.md` | survolé | INTEGRATION du dossier BvLS (titres) |
| 70 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/README.md` | lu | README du dossier BvLS |
| 71 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/REGISTRE_ECHECS.md` | lu | REGISTRE_ECHECS du dossier BvLS |
| 72 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/RESULTATS.md` | lu | RESULTATS du dossier BvLS |
| 73 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/SOURCES.md` | survolé | SOURCES du dossier BvLS (titres) |
| 74 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/BVLS_RECONSTRUCTION_DOSSIER/THEORIE.md` | survolé | THEORIE du dossier BvLS (titres) |
| 75 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/C1_K7_RESULTATS_PARTIELS/COORDINATION.md` | lu | COORDINATION du dossier K7 |
| 76 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/C1_K7_RESULTATS_PARTIELS/PREUVES.md` | lu | PREUVES du dossier K7 |
| 77 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/C1_K7_RESULTATS_PARTIELS/README.md` | lu | README du dossier K7 |
| 78 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/HOFFMAN_UPDATE_20261011/CERTIFICATION.md` | survolé | CERTIFICATION du dossier Hoffman (titres des couches) |
| 79 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/HOFFMAN_UPDATE_20261011/COORDINATION.md` | survolé | COORDINATION du dossier Hoffman (recherche de mots) |
| 80 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/HOFFMAN_UPDATE_20261011/COUVERTURE.md` | lu | COUVERTURE du dossier Hoffman |
| 81 | `conway99-c1:origin/claude/v7-simultaneous:dossiers…ternes/HOFFMAN_UPDATE_20261011/FAILURE_LEDGER_ADDITIONS.md` | lu | FAILURE_LEDGER_ADDITIONS du dossier Hoffman |
| 82 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/HOFFMAN_UPDATE_20261011/README.md` | lu | README du dossier Hoffman |
| 83 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/HOFFMAN_UPDATE_20261011/RESULTATS.md` | lu | RESULTATS du dossier Hoffman |
| 84 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/HOFFMAN_UPDATE_20261011/THEORIE.md` | survolé | THEORIE du dossier Hoffman (titres, lemme de prolongement l.59) |
| 85 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/INDEX.md` | lu | INDEX des dossiers externes |
| 86 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/PALEY_ASYMETRIE_DOSSIER/FAILURE_LEDGER.md` | lu | FAILURE_LEDGER du dossier Paley |
| 87 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/PALEY_ASYMETRIE_DOSSIER/README.md` | lu | README du dossier Paley |
| 88 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/PALEY_ASYMETRIE_DOSSIER/RESULTATS.md` | lu | RESULTATS du dossier Paley |
| 89 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/PALEY_ASYMETRIE_DOSSIER/THEORIE.md` | survolé | THEORIE du dossier Paley (titres) |
| 90 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/PALEY_ASYMETRIE_DOSSIER/sources/PROVENANCE.md` | survolé | PROVENANCE du dossier Paley (recherche de mots) |
| 91 | `fs:work/asym_paley_2026-10-14/NOTE_ASYM_PALEY.md` | lu | NOTE_ASYM_PALEY.md (fs ; ne diffère de la copie git que par 3 horodatages) |
| 92 | `fs:work/asym_paley_2026-10-14/NOVELTY_CHECK.md` | lu | NOVELTY_CHECK.md (fs ; heure du titre différente de la copie git) |
| 93 | `fs:work/asym_paley_data_2026-10-14/spence/13-6-2-3.txt` | non lu | liste de Spence (données) |
| 94 | `fs:work/asym_paley_data_2026-10-14/spence/17-8-3-4.txt` | non lu | liste de Spence (données) |
| 95 | `fs:work/asym_paley_data_2026-10-14/spence/25-12-5-6.txt` | non lu | liste de Spence srg(25,12,5,6) (données) |
| 96 | `fs:work/asym_paley_data_2026-10-14/spence/26-10-3-4.txt` | non lu | liste de Spence (données) |
| 97 | `fs:work/asym_paley_data_2026-10-14/spence/29-14-6-7.txt` | non lu | liste de Spence (données) |
| 98 | `fs:work/asym_paley_data_2026-10-14/spence/37-18-8-9.txt` | non lu | liste de Spence compressée (bz2, données) |
| 99 | `fs:work/asym_paley_data_2026-10-14/spence/9-4-1-2.txt` | non lu | liste de Spence srg(9,4,1,2) (données) |
| 100 | `fs:work/c1_night_2026-10-14/kk5_probe_log.txt` | non lu | journal brut kk5 (une ligne) |
| 101 | `fs:work/lambda1_construction_2026-10-14/ftwkb5_data/sol_1.txt` | non lu | solution SAT d'hémisystème (données) |
| 102 | `fs:work/lambda1_construction_2026-10-14/ftwkb5_data/sol_2.txt` | non lu | solution SAT d'hémisystème (données) |
| 103 | `fs:work/lambda1_construction_2026-10-14/ftwkb5_data/sol_3.txt` | non lu | solution SAT d'hémisystème (données) |
| 104 | `fs:work/scratchpad_LAB_2026-09-30/files/recovery_x…t/notes/NOTE_COEXISTENCE_COUVERTURES_HOFFMAN_2026_10_12.md` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 105 | `fs:work/scratchpad_LAB_2026-09-30/files/recovery_x…dit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 106 | `fs:work/scratchpad_LAB_2026-09-30/files/rem_stars_rank_2026-10-14.txt` | survolé | manifeste de 539 fichiers de code/lab_stars_rank (hash + chemin) |
| 107 | `fs:work/stars_rank_2026-10-14/HMATCH_NIGHT_2026-10-16.md` | lu | HMATCH_NIGHT_2026-10-16.md (fs, avec l'addendum de 08:06 UTC absent de la copie git) |
| 108 | `fs:work/stars_rank_2026-10-14/audit_runs.txt` | lu | audit_runs.txt (liste de 101 noms de runs) |
| 109 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:code/b18/sup24.txt` | lu | sup24.txt (données : matrice 9 x 9) |
| 110 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/155_V7_CLASSES_MOD7_ET_GERMES.md` | lu | note 155 |
| 111 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/156_ROUTE_FINIE_C1_MESURES.md` | lu | note 156 |
| 112 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/157_ROUTE_OMEGA_COMPLETUDE.md` | lu | note 157 |
| 113 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/158_TROIS_ETOILES_TRIANGLE_ETAGE_F.md` | lu | note 158 |
| 114 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/159_NOUVEAU_SRG_243_22_1_2.md` | lu | note 159 |
| 115 | `fs:c1-asymmetry-audit/PASSATION_C1_2026-10-07.md` | survolé | copie fs de la PASSATION (3411 contre 3370 octets, non comparée ligne à ligne) |
| 116 | `fs:c1-asymmetry-audit/code/b18/sup24.txt` | lu | copie fs de sup24.txt (données) |
| 117 | `fs:c1-asymmetry-audit/papers/README.md` | lu | README des articles (07/10) |
| 118 | `fs:c1-asymmetry-audit/papers/rank7/rank7.tex` | survolé | rank7.tex : résumé, théorème principal, remarque k_7 != 8 |
| 119 | `fs:c1-asymmetry-audit/papers/s5_2adic/s5_2adic.tex` | survolé | s5_2adic.tex : titres et énoncés |
| 120 | `fs:c1-asymmetry-audit/papers/srg243_second/srg243_second.tex` | survolé | srg243_second.tex : résumé |
| 121 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/160_ETAT_DES_LIEUX_EXISTENCE.md` | lu | note 160 |
| 122 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/161_DEPOT_OPENAI_MATH.md` | survolé | note 161 (l.1-25) |
| 123 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/161b_TRACES_RAISONNEMENT.md` | non lu | note 161b (analyse des traces de raisonnement du dépôt openai/math : hors sujet mathématique) |
| 124 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/161c_OPENAI_TRANSPOSABLE.md` | survolé | note 161c (verdicts par recherche de mots) |
| 125 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/162_INVENTAIRE_DECOUVERTES.md` | lu | note 162 |
| 126 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/162_annexes/A_STRUCTURES.md` | survolé | annexe 162 A (en-têtes) |
| 127 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/162_annexes/B_C3_C7.md` | survolé | annexe 162 B (en-têtes) |
| 128 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/162_annexes/C_C2_INVOLUTION.md` | survolé | annexe 162 C (en-têtes) |
| 129 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/162_annexes/D_C1.md` | survolé | annexe 162 D (en-têtes ; l.22-70, table L1-L25, lues) |
| 130 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/162_annexes/E_RANK17_ARCHIVE.md` | survolé | annexe 162 E (en-têtes) |
| 131 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/163_ETAGE_COLONNES_TROIS_COUCHES.md` | lu | note 163 |
| 132 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/164_PISTE_D7_HOLONOMIE_SOL.md` | lu | note 164 |
| 133 | `fs:c1-lap-girth5-audit/15a3cfe3f/NOTE.md` | lu | NOTE.md de c1-lap-girth5-audit (rang 37, maille >= 5) |
| 134 | `strongly-regular-graphs-research:main:LICENSE.md` | non lu | licence du dépôt public |
| 135 | `strongly-regular-graphs-research:main:README.md` | survolé | README du dépôt public strongly-regular-graphs-research (l.1-47 et titres) |
| 136 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:code/asym243/family_table.md` | lu | family_table.md |
| 137 | `conway99-c1:origin/claude/v7-simultaneous:code/asym243/hoffman/cubes_alpha99/STATUS.txt` | lu | STATUS des cubes alpha = 22 (v7) |
| 138 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:code/asym243/stab_specs.txt` | lu | stab_specs.txt |
| 139 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:code/asym243/stab_specs2.txt` | lu | stab_specs2.txt |
| 140 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:data/srg243/family/README.md` | lu | README de la famille srg(243) (data/srg243/family) |
| 141 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/165_SRG243_REVETEMENTS_ET_SYMETRIE.md` | lu | note 165 |
| 142 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/166_PARTITIONS_EQUITABLES_99.md` | lu | note 166 |
| 143 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:notes/167_MECANISMES_RECOLLEMENT_GRILLES.md` | lu | note 167 |
| 144 | `conway99-c1:origin/claude/v7-simultaneous:notes/168_SOUS_CAS_A_APPROCHE_MATHEMATIQUE.md` | lu | note 168 |
| 145 | `conway99-c1:origin/claude/v7-simultaneous:notes/169_DEUX_PISTES_SOUS_CAS_A.md` | lu | note 169 |
| 146 | `conway99-c1:origin/claude/v7-simultaneous:notes/170_STRUCTURE_TRIANGULAIRE_BALANCE_243.md` | lu | note 170 |
| 147 | `conway99-c1:origin/claude/v7-simultaneous:notes/171_BORDS_SERRES_HOFFMAN.md` | lu | note 171 |
| 148 | `conway99-c1:origin/claude/v7-simultaneous:notes/172_RESEAU_Q_ALPHA22.md` | lu | note 172 |
| 149 | `conway99-c1:origin/claude/v7-simultaneous:notes/173_CONJECTURE_K7.md` | lu | note 173 |
| 150 | `strongly-regular-graphs-research:main:requirements.txt` | non lu | requirements.txt (dépendances Python) |
| 151 | `conway99-c1:origin/astra/bvls-boundary-release-20261011:research/astra_bvls_boundary_20261011/COORDINATION.md` | lu | COORDINATION de la campagne Astra (branche astra) |
| 152 | `strongly-regular-graphs-research:main:results/srg243_family/README.md` | survolé | README des résultats srg(243) du dépôt public (l.1-40) |
| 153 | `strongly-regular-graphs-research:main:results/srg243_family/bvls243_hoffman_coclique.txt` | non lu | témoin de coclique de Hoffman de BvLS (liste de 45 sommets, données) |
| 154 | `fs:c1-asymmetry-audit/JOURNAL.md` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 155 | `fs:c1-asymmetry-audit/code/asym243/hoffman/cubes_alpha99/STATUS.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 156 | `fs:c1-asymmetry-audit/code/asym243/s3grid/STATUS.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 157 | `fs:c1-asymmetry-audit/code/asym243/s3grid/classes_ledger.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 158 | `fs:c1-asymmetry-audit/code/asym243/stab_specs.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 159 | `fs:c1-asymmetry-audit/code/asym243/stab_specs2.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 160 | `fs:c1-asymmetry-audit/code/family_nesting/nesting_output.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 161 | `fs:c1-asymmetry-audit/data/codex_hoffman_boundary_audit_20261012/boundary.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 162 | `fs:c1-asymmetry-audit/notes/NOTE_INTEGRATION_LAB567_2026_10_12.md` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 163 | `fs:c1-asymmetry-audit/notes/NOTE_SUIVI_SOLVEURS_2026_10_12.md` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 164 | `conway99-c1:origin/claude/v7-simultaneous:code/asym243/s3grid/STATUS.txt` | lu | STATUS s3grid (v7) |
| 165 | `conway99-c1:origin/claude/v7-simultaneous:code/asym243/s3grid/classes_ledger.txt` | lu | registre des classes s3grid (v7) |
| 166 | `conway99-c1:origin/claude/v7-simultaneous:code/family_nesting/nesting_output.txt` | lu | nesting_output.txt (v7) |
| 167 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/C3_preuve/proof_c3_english.pdf` | non lu | PDF de la preuve C3 (lot L04) |
| 168 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/PALEY_ASYMETRIE_DOSSIER/MANIFEST_SHA256.txt` | survolé | MANIFEST_SHA256 du dossier Paley (3 lignes) |
| 169 | `conway99-c1:origin/claude/v7-simultaneous:dossiers_externes/PALEY_ASYMETRIE_DOSSIER/requirements.txt` | non lu | requirements du dossier Paley |
| 170 | `conway99-c1:origin/claude/v7-simultaneous:dossiers…s/PALEY_ASYMETRIE_DOSSIER/resultats/closest_asymmetric.txt` | lu | resultats/closest_asymmetric.txt |
| 171 | `conway99-c1:origin/claude/v7-simultaneous:dossiers…Y_ASYMETRIE_DOSSIER/resultats/verification_recensement.txt` | lu | resultats/verification_recensement.txt |
| 172 | `conway99-c1:origin/claude/v7-simultaneous:dossiers…LEY_ASYMETRIE_DOSSIER/resultats/verification_spectrale.txt` | lu | resultats/verification_spectrale.txt |
| 173 | `conway99-c1:origin/claude/v7-simultaneous:dossiers…EY_ASYMETRIE_DOSSIER/resultats/verification_temoignage.txt` | lu | resultats/verification_temoignage.txt |
| 174 | `conway99-c1:origin/claude/v7-simultaneous:notes/174_EMBOITEMENTS_FAMILLE_1_2.md` | lu | note 174 |
| 175 | `conway99-c1:origin/claude/v7-simultaneous:notes/175_QUESTION_S3_ETALEMENT_243.md` | lu | note 175 |
| 176 | `conway99-c1:origin/claude/v7-simultaneous:notes/176_DEUX_FACTEUR_FX.md` | lu | note 176 |
| 177 | `conway99-c1:origin/claude/v7-simultaneous:notes/177_STRUCTURE_ARETE_B.md` | lu | note 177 |
| 178 | `conway99-c1:origin/claude/v7-simultaneous:notes/178_MOTS_BINAIRES_CODE7.md` | lu | note 178 |
| 179 | `fs:srg-research-audit/LICENSE.md` | non lu | licence (copie d'audit) |
| 180 | `fs:srg-research-audit/README.md` | lu | README de srg-research-audit (contenu identique au dépôt public, fins de ligne près) |
| 181 | `fs:srg-research-audit/papers/conway99_asymmetric/asymmetric.tex` | lu | asymmetric.tex (énoncé et dépendances, l.1-140) |
| 182 | `fs:srg-research-audit/papers/conway99_order2/order2.tex` | survolé | order2.tex : en-tête et résumé (C2, lot L01) |
| 183 | `fs:srg-research-audit/papers/conway99_order2/table156.tex` | non lu | table156.tex : table générée (C2, lot L01) |
| 184 | `fs:srg-research-audit/papers/conway99_order3/preuve_c3.tex` | survolé | preuve_c3.tex : titre, date, résumé (C3, lot L04) |
| 185 | `fs:srg-research-audit/papers/conway99_order7/order7.tex` | survolé | order7.tex : titre, résumé (C7) |
| 186 | `fs:srg-research-audit/requirements.txt` | non lu | requirements.txt |
| 187 | `fs:srg-research-audit/results/srg243_family/README.md` | survolé | README des résultats srg(243) (copie d'audit) |
| 188 | `fs:srg-research-audit/results/srg243_family/bvls243_hoffman_coclique.txt` | non lu | témoin de coclique (données, copie d'audit) |
| 189 | `fs:c1-asymmetry-audit/data/codex_asymmetry_synthesis_20261014/literature/kaski_ostergard_2004_sts19.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 190 | `fs:c1-asymmetry-audit/data/codex_asymmetry_synthes…61014/literature_expansion/babai_automorphism_handbook.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 191 | `fs:c1-asymmetry-audit/data/codex_asymmetry_synthes…4/literature_expansion/brouwer_ihringer_kantor_4vertex.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 192 | `fs:c1-asymmetry-audit/data/codex_asymmetry_synthes…20261014/literature_expansion/brouwer_vanmaldeghem_srg.pdf` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 193 | `fs:c1-asymmetry-audit/data/codex_asymmetry_synthes…20261014/literature_expansion/brouwer_vanmaldeghem_srg.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 194 | `fs:c1-asymmetry-audit/data/codex_asymmetry_synthes…4/literature_expansion/coolsaet_degraer_spence_2006_45.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 195 | `fs:c1-asymmetry-audit/data/codex_asymmetry_synthesis_20261014/literature_expansion/haemers_spence_2001_64.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 196 | `fs:c1-asymmetry-audit/data/codex_asymmetry_synthes…iterature_expansion/maksimovic_rukavina_2022_twographs.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 197 | `fs:c1-asymmetry-audit/data/codex_asymmetry_synthesis_20261014/literature_expansion/spence_64_18_2_6.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 198 | `fs:c1-asymmetry-audit/data/codex_lambda_one_construction_20261014/payne9/geometry.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 199 | `fs:c1-asymmetry-audit/data/codex_night_20261014/four_root_edge_graph.txt` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 200 | `fs:c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md` | sous-lot B1 | notes de Codex (journal de nuit, 18/10) ; état détaillé au §10.2 |
| 201 | `fs:c1-lambda1-env/Lib/site-packages/pycryptosat-5.17.0.dist-info/licenses/LICENSE.txt` | non lu | licence pycryptosat : hors sujet |
| 202 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_asym_paley_2026-10-14/NOTE_ASYM_PALEY.md` | lu | NOTE_ASYM_PALEY.md (copie git) |
| 203 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_asym_paley_2026-10-14/NOVELTY_CHECK.md` | lu | NOVELTY_CHECK.md (copie git) |
| 204 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/HMATCH_NIGHT_2026-10-16.md` | lu | HMATCH_NIGHT_2026-10-16.md (copie git, sans l'addendum de 08:06 UTC) |
| 205 | `conway99-c1:origin/lab/exploration-2026-10-16:code/lab_stars_rank_2026-10-14/r8/probe/b1_cpsat_log.txt` | survolé | b1_cpsat_log.txt : statut final (K = 22, cinq étoiles, UNKNOWN en 400 s, encodage défectueux corrigé ensuite) |
| 206 | `fs:lab_exchange_2026-10-14/codex_51_extensions_and_coupling.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 207 | `fs:lab_exchange_2026-10-14/codex_7adic_direction_after774.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 208 | `fs:lab_exchange_2026-10-14/codex_after738_family52.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 209 | `fs:lab_exchange_2026-10-14/codex_after741_joint_fourth_star.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 210 | `fs:lab_exchange_2026-10-14/codex_after745_coupling.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 211 | `fs:lab_exchange_2026-10-14/codex_after752_fourstar_columns.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 212 | `fs:lab_exchange_2026-10-14/codex_after757_null13_scope.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 213 | `fs:lab_exchange_2026-10-14/codex_bridge_807_square.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 214 | `fs:lab_exchange_2026-10-14/codex_bridge_807_square_export.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 215 | `fs:lab_exchange_2026-10-14/codex_bridge_809_grid_cut.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 216 | `fs:lab_exchange_2026-10-14/codex_bridge_812_exact_export.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 217 | `fs:lab_exchange_2026-10-14/codex_bridge_812_exact_route.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 218 | `fs:lab_exchange_2026-10-14/codex_bridge_815_projection.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 219 | `fs:lab_exchange_2026-10-14/codex_bridge_815_projection_export.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 220 | `fs:lab_exchange_2026-10-14/codex_bridge_831_ramified.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 221 | `fs:lab_exchange_2026-10-14/codex_bridge_833_mixed.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 222 | `fs:lab_exchange_2026-10-14/codex_bridge_836_odd9_progress.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 223 | `fs:lab_exchange_2026-10-14/codex_bridge_839_odd9_integer_cut.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 224 | `fs:lab_exchange_2026-10-14/codex_bridge_841_balanced_profiles.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 225 | `fs:lab_exchange_2026-10-14/codex_bridge_843_corrected_odd_budget.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 226 | `fs:lab_exchange_2026-10-14/codex_bridge_843_defect_decomposition.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 227 | `fs:lab_exchange_2026-10-14/codex_bridge_845_mate_family.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 228 | `fs:lab_exchange_2026-10-14/codex_bridge_849_torsion_census_ng7.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 229 | `fs:lab_exchange_2026-10-14/codex_bridge_850_ng5_scope.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 230 | `fs:lab_exchange_2026-10-14/codex_bridge_854_kernel_partition_closure.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 231 | `fs:lab_exchange_2026-10-14/codex_bridge_855_rank_target.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 232 | `fs:lab_exchange_2026-10-14/codex_bridge_858_flat_prism_cores.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 233 | `fs:lab_exchange_2026-10-14/codex_bridge_859_flat_c4do_proof.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 234 | `fs:lab_exchange_2026-10-14/codex_bridge_862_support_fourteen.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 235 | `fs:lab_exchange_2026-10-14/codex_bridge_865_hmatch_target_input.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 236 | `fs:lab_exchange_2026-10-14/codex_bridge_867_pi_normalization.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 237 | `fs:lab_exchange_2026-10-14/codex_bridge_870_mate_obstructions.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 238 | `fs:lab_exchange_2026-10-14/codex_bridge_873_full_spectral_filter.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 239 | `fs:lab_exchange_2026-10-14/codex_bridge_875_hmatch_prospects.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 240 | `fs:lab_exchange_2026-10-14/codex_bridge_877_antipodal_rigidity.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 241 | `fs:lab_exchange_2026-10-14/codex_bridge_complete_assembly.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 242 | `fs:lab_exchange_2026-10-14/codex_bridge_extension_construction.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 243 | `fs:lab_exchange_2026-10-14/codex_bridge_global_columns.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 244 | `fs:lab_exchange_2026-10-14/codex_bridge_global_columns_delivery.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 245 | `fs:lab_exchange_2026-10-14/codex_bridge_microscopic_repair.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 246 | `fs:lab_exchange_2026-10-14/codex_bridge_psd_learning.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 247 | `fs:lab_exchange_2026-10-14/codex_bridge_rank_release_disc.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 248 | `fs:lab_exchange_2026-10-14/codex_bridge_root_schur_construction.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 249 | `fs:lab_exchange_2026-10-14/codex_c55_exact_joint_sectors.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 250 | `fs:lab_exchange_2026-10-14/codex_c55_excluded_after774.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 251 | `fs:lab_exchange_2026-10-14/codex_c55_global_after772.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 252 | `fs:lab_exchange_2026-10-14/codex_c55_trivial_quotient_756.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 253 | `fs:lab_exchange_2026-10-14/codex_coarse_floor_after768.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 254 | `fs:lab_exchange_2026-10-14/codex_fourstar_schur_741.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 255 | `fs:lab_exchange_2026-10-14/codex_g1_character_rank_targets.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 256 | `fs:lab_exchange_2026-10-14/codex_global_counting_after764.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 257 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/LEMMES_PHI.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 258 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/README_GLOBAL_COVER.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 259 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/README_GLOBAL_PSD.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 260 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/README_GLOBAL_STAR12.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 261 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/README_STAR_REPAIR_PHI.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 262 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_even_energy_43c496e.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 263 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_family_synthesis_51460e5.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 264 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_family_synthesis_count.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 265 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_odd_fixed_coupling.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 266 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_resonance_925_first.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 267 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_resonance_bba12ce.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 268 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_sector_coupling_2bce4b9.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 269 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_sym6_67ffa75.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 270 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_sym6_928_first.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 271 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_sym6_boundary_4c9ca38.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 272 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/codex_41d23bb_cover20_message.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 273 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/codex_74sur79_signatures.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 274 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/codex_75sur79.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 275 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/codex_76sur79.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 276 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/codex_corner_tables_2134.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 277 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/codex_d07ac4a_cover15_message.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 278 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/codex_signature_moments_reprise.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 279 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23281359_milgram_obstruction.pdf` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 280 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23281359_milgram_obstruction.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 281 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23281436_conway99_local.pdf` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 282 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23281436_conway99_local.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 283 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23399271_RELEASE.pdf` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 284 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23399271_RELEASE.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 285 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/ETAT_PONT_918_2026-10-16.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 286 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/RELEVE_LITTERATURE_2026-10-16.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 287 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/bridge_family_resonance_921.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 288 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/bridge_global_exact_letter_918.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 289 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/bridge_latest_arxiv_findings.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 290 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/bridge_literature_findings.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 291 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/bridge_product_encoding_scope.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 292 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/literature_sos_2610_16266_counterexample.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 293 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/matrice_15_lignes/matrice_partielle_84.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 294 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_907_global_psd_reply.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 295 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_defect_20261016.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 296 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_four_broken_20261016.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 297 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_global_cover_delivery_20261016.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 298 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_global_cover_scope_20261016.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 299 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_global_psd_delivery_20261016.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 300 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_global_star12_20261016.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 301 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_gray_block_obstruction_20261016.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 302 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_phi_899_reply.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 303 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_rank7_423127b.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 304 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_root_components_cd34d43.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 305 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_root_cover79_72d47c3.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 306 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/message_star15_phi_83ecbbe.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 307 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/sector_coupling_2bce4b9/README.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 308 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/sym6_boundary_4c9ca38/README.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 309 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/sym6_energy_43c496e/BORNE_ENERGIE_PAIRE_2026_10_16.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 310 | `fs:lab_exchange_2026-10-14/codex_hmatch_20261016/sym6_energy_43c496e/README.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 311 | `fs:lab_exchange_2026-10-14/codex_mixed336_after778.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 312 | `fs:lab_exchange_2026-10-14/codex_mixed_budget_direction_after778.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 313 | `fs:lab_exchange_2026-10-14/codex_nonnegative_weight_bound_733.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 314 | `fs:lab_exchange_2026-10-14/codex_odd9_network_result.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 315 | `fs:lab_exchange_2026-10-14/codex_odd_census_after769.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 316 | `fs:lab_exchange_2026-10-14/codex_reply735_connected.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 317 | `fs:lab_exchange_2026-10-14/codex_reply738_h3.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 318 | `fs:lab_exchange_2026-10-14/codex_reprise_785.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 319 | `fs:lab_exchange_2026-10-14/codex_response_790.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 320 | `fs:lab_exchange_2026-10-14/codex_response_792.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 321 | `fs:lab_exchange_2026-10-14/codex_response_794.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 322 | `fs:lab_exchange_2026-10-14/codex_response_795.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 323 | `fs:lab_exchange_2026-10-14/codex_response_797.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 324 | `fs:lab_exchange_2026-10-14/codex_response_801.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 325 | `fs:lab_exchange_2026-10-14/codex_response_803.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 326 | `fs:lab_exchange_2026-10-14/codex_response_805.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 327 | `fs:lab_exchange_2026-10-14/codex_strict_upper_100.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 328 | `fs:lab_exchange_2026-10-14/codex_upper_cuts_export_ready.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 329 | `fs:lab_exchange_2026-10-14/codex_weight16_enumeration_733.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 330 | `fs:lab_exchange_2026-10-14/codex_z5hm_delivery.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 331 | `fs:lab_exchange_2026-10-14/codex_z5hm_delivery_explicit.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 332 | `fs:lab_exchange_2026-10-14/codex_z5hm_exclusion_progress.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 333 | `fs:lab_exchange_2026-10-14/codex_z5hm_mixed_parity_826.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 334 | `fs:lab_exchange_2026-10-14/codex_z5hm_mod5_delivery.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 335 | `fs:lab_exchange_2026-10-14/codex_z5hm_mod5_progress.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 336 | `fs:lab_exchange_2026-10-14/codex_z5hm_progress.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 337 | `fs:c1-asymmetry-audit/data/codex_line_resonance_20261016/bridge_20261018_0302.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 338 | `fs:c1-asymmetry-audit/data/codex_line_resonance_20261016/bridge_20261018_0326.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 339 | `fs:c1-asymmetry-audit/data/codex_line_resonance_20261016/bridge_20261018_0352.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 340 | `fs:c1-asymmetry-audit/notes/REPRISE_COMPOSANTES_C1_2026_10_16.txt` | sous-lot B1 | notes de Codex (journal de nuit, 18/10) ; état détaillé au §10.2 |
| 341 | `fs:c1-asymmetry-audit/tmp/bridge_codex_20261017_2317.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 342 | `fs:c1-asymmetry-audit/tmp/bridge_codex_20261017_2346.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 343 | `fs:c1-asymmetry-audit/tmp/bridge_codex_composantes_20261017_0205.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 344 | `fs:c1-asymmetry-audit/tmp/bridge_codex_cpu_20261017_0236.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 345 | `fs:c1-asymmetry-audit/tmp/bridge_codex_global_minc_20261017.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 346 | `fs:c1-asymmetry-audit/tmp/bridge_codex_no_path4_20261017.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 347 | `fs:c1-asymmetry-audit/tmp/bridge_codex_short_vectors_20261017.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 348 | `fs:c1-asymmetry-audit/AGENTS.md` | sous-lot B2 | notes de Codex (c1-asymmetry-audit) ; état détaillé au §10.3 |
| 349 | `fs:c1-asymmetry-audit/notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt` | sous-lot B1 | notes de Codex (journal de nuit, 18/10) ; état détaillé au §10.2 |
| 350 | `fs:c1-asymmetry-audit/notes/DROITE_PETITE_ET_RACINE_2026_10_18.txt` | sous-lot B1 | notes de Codex (journal de nuit, 18/10) ; état détaillé au §10.2 |
| 351 | `fs:c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt` | sous-lot B1 | notes de Codex (journal de nuit, 18/10) ; état détaillé au §10.2 |
| 352 | `fs:c1-asymmetry-audit/tmp/bridge_codex_20261018_0024.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 353 | `fs:c1-asymmetry-audit/tmp/bridge_codex_20261018_0100.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 354 | `fs:c1-asymmetry-audit/tmp/bridge_codex_20261018_reply970.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |
| 355 | `fs:c1-asymmetry-audit/tmp/stage_aws_partial_paths.txt` | sous-lot A | messages du pont Codex → LAB ; état détaillé au §10.1 |

## 10. Notes des sous-lots (texte des sous-agents, versé tel quel ; titres décalés de deux niveaux)

### 10.1 Sous-lot A : messages du pont Codex → LAB (index 206-339, 341-347, 352-355)

Correspondance : l'entrée « n° JSONL n » de ce texte est `L07_C1_asym_local-(284 + n)` ; son champ `remarques` commence par `[A_bridge n<n>]`.

### L07 — sous-lot A_bridge : messages Codex -> LAB (14/10 22:32 – 18/10 03:52)

Sous-lot : index 206-339, 341-347, 352-355 de `lots/L07_C1_asym_local.jsonl` (145 fichiers).
Fiche de résultats : `A_bridge_entries.jsonl` (115 entrées, chemins complets et numéros de ligne).

**Abréviations de chemins (toutes les sources ci-dessous sont `chemin:ligne`) :**
- `LE/` = `C:/home/researcher/Desktop/Recherche_Conway/lab_exchange_2026-10-14/`
- `LE/H/` = `LE/codex_hmatch_20261016/` ; `LE/H/lit/` = `LE/H/literature_20261016/`
- `AA/` = `C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/`
- `W/` = `C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/`
  (sources LAB citées seulement pour recoupement ; elles appartiennent au lot principal).

**Avertissements de vocabulaire (indispensables pour l'appariement automatique) :**
- Dans les messages de Codex, **C1, C1', C2** désignent des **conditions locales de comptage** (degrés / budgets par racine,
  plafonds de voisins communs λ <= 1, μ <= 2), PAS les cas C1 (asymétrique) / C2 (involution) du projet. Exemple :
  « C1 + binarité + T, U PSD <=> SRG99 » (`LE/H/message_907_global_psd_reply.txt:5`). Quand Codex parle du cas, il écrit
  « C1 entier » ou « exclusion de C1 ».
- **R7** a trois sens : (i) la loi de rang réfutée « rang_7(8T_S4) >= 29 » (LAB, 14/10) ; (ii) le lemme R7 de l'attaque
  N9-NG du LAB, cité par Codex (`LE/codex_bridge_862_support_fourteen.txt:11`) ; (iii) la cible SAT « quatre étoiles +
  sept labels {4,t} » (`LE/H/lit/ETAT_PONT_918_2026-10-16.txt:4`).
- **N9** a deux sens : la loi LAB « nullité <= 9 + min c » (réfutée) et l'ancien théorème de Codex « aucun sous-graphe à
  9 sommets et 17 arêtes » (`LE/codex_odd9_network_result.txt:1`).
- P = nombre de prismes ; ρ = nombre de grilles ; t(l) = nombre de transversales d'une droite (Σt = 2P) ; c(l) = nombre
  de composantes de H_l ; g = grilles par droite ; ν = nullité de T ; T8 = 8T, U15 = 15U, T + U = 7Π.
- « min c = 4 » (branche Codex) = le minimum de c(l) sur TOUTES les droites du graphe vaut 4.

#### 1. Résumé (10 lignes)
1. Codex accepte sans re-audit les réfutations LAB de (A), (H4), ODD9 universelle, KER-SYM universelle et retire ses propres
   affirmations trop fortes (note 100, ODD9 « ouverte »).
2. Deux familles locales sont exclues comme bords de Conway par la borne globale rang_F7(8T) <= 28 : G1 c55 non-grille
   (énumération exacte de 145152 cas) et <z,hM> (520 certificats entiers).
3. Bornes globales : P <= 852, ρ <= 126, >= 336 drapeaux à >= 4 relations mixtes, >= 254 blocs non-grille à min t <= 7 ;
   d'où NG5/NG7/N9-NG => pas de Conway (implication prouvée, lemme ouvert).
4. Réduction exacte : N9-NG <=> rang(F) >= 12 (Q20) ; SYM6, ODD-PURE, borne d'énergie paire 1/5 : identités prouvées,
   bornes universelles ouvertes.
5. Théorèmes « plats » : C4DO pour support <= 12, nullité sur O pour support <= 14 ; lemme universel E3 (e(Q) ≠ 3) ;
   lemme des vecteurs courts propres -4 (co-Heawood).
6. H-MATCH : aucune preuve, aucun contre-exemple ; remariages et rematchings purs fermés pour les germes testés.
7. Extension 44 -> 84 -> 99 : tous les germes testés (HB promu, urep100, cœur 30, cadre 15 lignes) sont non prolongeables ;
   équivalence globale « C1 + binarité + T, U PSD <=> SRG99 » sur 84 étiquettes.
8. Modèle global exact couvrant TOUT Conway (11 / 19 types) : pilotes UNKNOWN, aucun coût abordable démontré.
9. Branche « min global c = 4 » : 79 templates, 76 fermés (CP-SAT), 7, 9, 19 ouverts ; fermeture 79/79 ultérieure RETIRÉE
   le 18/10 (bug OR-Tools 9.15) ; portée strictement limitée à min global c >= 4.
10. Littérature : la « preuve SOS » de non-existence (arXiv 2610.16266) repose sur une borne fausse (redécouverte du même
    contre-exemple à 66 triangles par Codex et par theesfeld).

#### 2. Chronologie (dates et heures = horodatage des fichiers, heure locale du PC)
- **14/10 22:32-23:00** — trois étoiles : 4e relation positive de poids >= 16 (`LE/codex_nonnegative_weight_bound_733.txt:3`,
  `LE/codex_weight16_enumeration_733.txt:3`) ; contre-exemples NON PSD à (A) (`LE/codex_reply735_connected.txt:1`) ;
  (A) déclarée fausse par le LAB (741), acceptée (`LE/codex_after741_joint_fourth_star.txt:1`).
- **14/10 23:06-23:21** — Schur joint de la 4e étoile (`LE/codex_fourstar_schur_741.txt:1`) ; 51 germes non prolongeables
  par {4,6} et (H4) réfutée par le LAB (746) (`LE/codex_51_extensions_and_coupling.txt:1`, `:3`) ; théorème des
  compressions définies positives + 100 coupes strictes (`LE/codex_strict_upper_100.txt:1`).
- **14/10 23:26-23:55** — caractères G1 (`LE/codex_g1_character_rank_targets.txt:5`) ; lemme c55 non-grille
  (`LE/codex_c55_trivial_quotient_756.txt:4`) ; 126 Schur (`LE/codex_c55_exact_joint_sectors.txt:3`).
- **15/10 00:10-00:48** — census P = 0 rationnel ; inégalité sommable ; plancher entier 504 << 1190,4
  (`LE/codex_global_counting_after764.txt:3`, `:12` ; `LE/codex_coarse_floor_after768.txt:6`) ; interface impaire
  (`LE/codex_odd_census_after769.txt:3`) ; contraintes globales c55 (`LE/codex_c55_global_after772.txt:5`).
- **15/10 01:13** — exclusion F7 de toute la famille G1 c55 non-grille (`LE/codex_c55_excluded_after774.txt:1`).
- **15/10 01:20-01:25** — P <= 852, ρ <= 126, budget mixte, >= 336 drapeaux (`LE/codex_mixed_budget_direction_after778.txt:1`,
  `LE/codex_mixed336_after778.txt:1`).
- **15/10 10:43** — répartition T2 (Codex, ODD9) / T3 (LAB, mur 13) ; H-MATCH => Hamming accepté (`LE/codex_reprise_785.txt:1`).
- **15/10 11:05-12:54** — formule réseau d'ODD9 (`LE/codex_odd9_network_result.txt:8`) ; forme A22, défaut h, orientations,
  borne 4096, volume, circulation des composantes, défaut g = h·p et relecture de HB_1 (`LE/codex_response_790.txt` à
  `LE/codex_response_805.txt`).
- **15/10 13:07-14:00** — G1'' : carré F, coupe de grille (c_m <= 3 sous H-MATCH cassé) (`LE/codex_bridge_809_grid_cut.txt:3`) ;
  certificats exacts LP/MILP et projection C2 (`LE/codex_bridge_812_exact_route.txt:2`, `LE/codex_bridge_815_projection.txt:2`).
- **15/10 14:20-15:15** — famille hM / <z,hM> : damier (c = (6,6) exclu), exclusion F7 de <z,hM>
  (`LE/codex_z5hm_exclusion_progress.txt:7`, `LE/codex_z5hm_delivery.txt:7`) ; campagne LAB 339556/192/plafond 9 acceptée
  (`LE/codex_z5hm_mixed_parity_826.txt:1`) ; filtre mod 5 (`LE/codex_z5hm_mod5_progress.txt:4`).
- **15/10 16:06-18:02** — filtre ramifié ; lemme d'asymétrie (`LE/codex_bridge_833_mixed.txt:5`) ; coupe plate 48
  (`LE/codex_bridge_839_odd9_integer_cut.txt:5`) ; KER-SYM universelle réfutée par le LAB (`LE/codex_bridge_841_balanced_profiles.txt:14`).
- **15/10 19:10** — Codex retire ODD9 universelle (`LE/codex_bridge_843_corrected_odd_budget.txt:1`) ; puis défaut
  d_l = (b-2) + η_l et famille des 120 appariements (`LE/codex_bridge_845_mate_family.txt:11`).
- **15/10 21:01-21:06** — P = 0 entier ; borne 254 (NG7) ; retrait de la phrase de la note 100 ; NG5 => pas de Conway vérifié
  (`LE/codex_bridge_849_torsion_census_ng7.txt:5`, `:9` ; `LE/codex_bridge_850_ng5_scope.txt:3`).
- **15/10 22:07-23:34** — clôture des partitions de noyau ; cible de rang NG5 ; cœurs plats ; théorèmes C4DO (support 12) et
  support 14 (`LE/codex_bridge_859_flat_c4do_proof.txt:3`, `LE/codex_bridge_862_support_fourteen.txt:1`).
- **16/10 05:10-07:30 (nuit H-MATCH)** — normalisation Π ; remariage fermé pour n_45, b_29 ; « aucune preuve réaliste » ;
  rigidité antipodale (`LE/codex_bridge_870_mate_obstructions.txt:1`, `LE/codex_bridge_875_hmatch_prospects.txt:2`,
  `LE/codex_bridge_877_antipodal_rigidity.txt:5`).
- **16/10 09:11-11:23** — HB_1 promu (ν 14, H-MATCH intact) ; non prolongeable ; assemblage 44 -> 84 -> 99 ; critère global ;
  réparation par cœurs, DISC, coupes apprises ; cœur 30 exclu (CP-SAT) (`LE/codex_bridge_root_schur_construction.txt:1`,
  `LE/codex_bridge_extension_construction.txt:1`, `LE/codex_bridge_complete_assembly.txt:5`, `LE/codex_bridge_global_columns.txt:3`).
- **16/10 11:34-13:55** — lemmes de rupture de h (>= 3, >= 4 lignes, relus par le LAB) ; étoile 12-globale ; lemmes PHI ;
  cadre 15 lignes ; obstruction des cinq lignes 02, 03, 47, 48, 413 (`LE/H/message_four_broken_20261016.txt:1`,
  `LE/H/LEMMES_PHI.txt:12`, `LE/H/message_gray_block_obstruction_20261016.txt:1`).
- **16/10 14:26-15:11** — consigne de l'utilisateur (contradiction GLOBALE) ; modèle global 11/19 types ; comptes racines 166 ;
  équivalence C1 + binarité + deux PSD <=> SRG99 ; centre fractionnaire (`LE/H/message_global_cover_scope_20261016.txt:1`,
  `LE/H/message_907_global_psd_reply.txt:5`, `LE/H/message_global_psd_delivery_20261016.txt:5`).
- **16/10 15:32-19:21** — littérature (SOS 2610.16266 réfutée ; relevé) ; retrait LAB 916 (barrière du 7e label) ;
  état R7/R8 ; résonance k = 14 ; synthèse 51460e5 ; critère de symétrie forcée (`LE/H/lit/RELEVE_LITTERATURE_2026-10-16.txt:80`,
  `LE/H/lit/ETAT_PONT_918_2026-10-16.txt:4`, `LE/H/bridge_family_synthesis_51460e5.txt:9`).
- **16/10 19:50-21:04** — réduction Q20 de N9-NG ; SYM6 ; identité de bord ; borne d'énergie paire ; couplage des 20 fixes
  (`LE/H/bridge_resonance_bba12ce.txt:5`, `LE/H/bridge_sym6_67ffa75.txt:3`, `LE/H/sym6_energy_43c496e/BORNE_ENERGIE_PAIRE_2026_10_16.txt:11`,
  `LE/H/sector_coupling_2bce4b9/README.txt:2`).
- **16/10 21:35 – 17/10 00:06** — branche min c = 4 : 2^21 -> 200 -> 100 -> 79 templates ; 198 INFEASIBLE ; 59 -> 64 -> 74 ->
  75 -> 76/79 (`LE/H/message_root_components_cd34d43.txt:4`, `LE/H/message_root_cover79_72d47c3.txt:1`, `LE/H/codex_76sur79.txt:1`).
- **17/10 00:28-02:36** — c >= 4 hors racine ; lemme des vecteurs courts ; lemme E3 universel (`AA/tmp/bridge_codex_no_path4_20261017.txt:1`).
- **17/10 23:12 – 18/10 03:52** — lemme de bord ; inégalité de paire ; coupe des triangles ; cas six-prismes ; portée des 76
  exclusions (`AA/tmp/bridge_codex_20261018_reply970.txt:3`) ; coût v2 4232 CPU·h (`AA/data/codex_line_resonance_20261016/bridge_20261018_0326.txt:3`).
- **18/10 ~11:40 (hors sous-lot, recoupement)** — correction du bug OR-Tools 9.15 : 79/79 retirée, familles 7, 9, 19 rouvertes
  (`AA/notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt:22`).

#### 3. Table courte des résultats principaux (détail et sources complètes dans le JSONL ; « n° JSONL » = numéro de ligne dans A_bridge_entries.jsonl, les ids définitifs sont à attribuer par le lot)
| n° JSONL | énoncé court | statut | source principale |
|---|---|---|---|
| 1 | 4e relation positive normalisée (trois étoiles) : poids >= 16 | C | `LE/codex_nonnegative_weight_bound_733.txt:3` |
| 7 | (A) fausse (LAB 741) | R | `LE/codex_after741_joint_fourth_star.txt:1` |
| 11 | (H4) fausse (LAB 746, rang 34) | R | `LE/codex_51_extensions_and_coupling.txt:3` |
| 10 | 51 germes (A) non prolongeables par {4,6} | E | `LE/codex_51_extensions_and_coupling.txt:1` |
| 12 | compressions de U définies positives ; 100 coupes strictes | P | `LE/codex_strict_upper_100.txt:1` |
| 24 | G1 c55 non-grille : rang_F7 >= 29 > 28, jamais un bord de Conway | E | `LE/codex_c55_excluded_after774.txt:1` |
| 25 | P <= 852, ρ <= 126 (certificats exacts) | C | `LE/codex_mixed_budget_direction_after778.txt:1` |
| 27 | >= 336 drapeaux à >= 4 relations mixtes | P | `LE/codex_mixed336_after778.txt:1` |
| 44 | <z,hM> exclue (ν <= 14 ; rang_F7 >= 29 à ν = 14) | C | `LE/codex_z5hm_delivery.txt:7` |
| 45 | campagne LAB <z,hM> : plafond local 9 (accepté) | E | `LE/codex_z5hm_mixed_parity_826.txt:1` |
| 54 | ODD9 universelle fausse (LAB), retirée par Codex | R | `LE/codex_bridge_843_corrected_odd_budget.txt:1` |
| 52 | KER-SYM universelle fausse à ν = 9 (LAB) | R | `LE/codex_bridge_841_balanced_profiles.txt:14` |
| 49 | coupe plate : e(O ∪ S) <= 48 | P | `LE/codex_bridge_839_odd9_integer_cut.txt:5` |
| 58 | >= 254 blocs non-grille à min t <= 7 (cible NG7) | P | `LE/codex_bridge_849_torsion_census_ng7.txt:5` |
| 61 | NG5 + P <= 852 => pas de Conway (vérifié par Codex) | P | `LE/codex_bridge_850_ng5_scope.txt:3` |
| 59 | retrait de la phrase de la note 100 | X | `LE/codex_bridge_849_torsion_census_ng7.txt:9` |
| 65 | C4DO pour relations plates de support <= 12 | P | `LE/codex_bridge_859_flat_c4do_proof.txt:3` |
| 66 | relations plates de support <= 14 nulles sur O | P | `LE/codex_bridge_862_support_fourteen.txt:1` |
| 68 | remariage impossible pour n_45, b_29 (λ_min < -4) | C | `LE/codex_bridge_870_mate_obstructions.txt:1` |
| 70 | aucun rematching pur pour urep100, H30_23 | C | `LE/codex_bridge_877_antipodal_rigidity.txt:5` |
| 72 | HB promu non prolongeable (Farkas, 16 puis 5 feuilles) | C | `LE/codex_bridge_extension_construction.txt:1` |
| 74 | sur 84 : T, U PSD + rang T <= 30 => SRG99 | P | `LE/codex_bridge_complete_assembly.txt:5` |
| 76 | cœur 30 d'urep100 exclu (CP-SAT UNSAT) | S | `LE/codex_bridge_global_columns.txt:3` |
| 79-80 | >= 3 puis >= 4 lignes d'attache rompent h (relu LAB) | P | `LE/H/message_four_broken_20261016.txt:1` |
| 83 | lemmes PHI | P | `LE/H/LEMMES_PHI.txt:12` |
| 85 | cadre 15 lignes non prolongeable ; motif 58 <= 57 | P | `LE/H/message_gray_block_obstruction_20261016.txt:5` |
| 86 | modèle global exact couvrant tout Conway (11/19 types) | P (réduction) / O (résolution) | `LE/H/README_GLOBAL_COVER.txt:7` |
| 88 | C1 + binarité + T, U PSD <=> SRG99 (84) | P | `LE/H/message_907_global_psd_reply.txt:5` |
| 90 | borne SOS T(99) <= 55 fausse (66 et 120 triangles) | C | `LE/H/literature_sos_2610_16266_counterexample.txt:1` |
| 93 | barrière du 7e label retirée (LAB 916) | X | `LE/H/lit/RELEVE_LITTERATURE_2026-10-16.txt:80` |
| 94 | R7 : 6 témoins non prolongeables ; R8 UNKNOWN | S | `LE/H/lit/ETAT_PONT_918_2026-10-16.txt:4` |
| 95 | résonance k = 14 (équilibre c/6 à 99) | P | `LE/H/bridge_family_synthesis_51460e5.txt:4` |
| 97 | critère : #complétions étiquetées < |Aut(H)| => pas de complétion asymétrique | P | `LE/H/bridge_family_synthesis_51460e5.txt:9` |
| 99 | N9-NG <=> rang(F) >= 12 (Q20) | P | `LE/H/bridge_resonance_bba12ce.txt:5` |
| 100 | SYM6 <=> rang Z >= 3 ; ODD-PURE => c_min = 1 impossible | P | `LE/H/bridge_sym6_67ffa75.txt:3` |
| 102 | borne d'énergie paire E >= G/5 + (2/5)(I - M) | P | `LE/H/sym6_energy_43c496e/BORNE_ENERGIE_PAIRE_2026_10_16.txt:11` |
| 104-105 | branche min c = 4 : 79 templates, 76 fermés | S | `LE/H/codex_76sur79.txt:1` |
| 108 | lemme E3 universel : e(Q) ≠ 3 | P | `AA/tmp/bridge_codex_no_path4_20261017.txt:1` |
| 109 | vecteurs courts propres -4 ; inégalité de paire | P | `AA/tmp/bridge_codex_20261017_2346.txt:4` |
| 110 | familles 7, 9, 19 : exclusions partielles de Gram (sous réserve du bug) | S | `AA/data/codex_line_resonance_20261016/bridge_20261018_0302.txt:3` |
| 111 | les 76 exclusions ne valent que pour min global c >= 4 | P | `AA/tmp/bridge_codex_20261018_reply970.txt:3` |

#### 4. Routes fermées (et pourquoi)
- **(A)** [trois étoiles, positivité, c = 1 => rang 31] : réfutée par 52 objets exacts du LAB (`LE/codex_after741_joint_fourth_star.txt:1` ;
  `W/stars_rank_2026-10-14/AUDIT_EXCLUSIONS_2026-10-15.md:26`) ; déjà fausse sans positivité (`LE/codex_reply735_connected.txt:1`).
- **(H4)** [aucun objet à quatre étoiles positif] : objet positif de rang 34 (`LE/codex_51_extensions_and_coupling.txt:3`).
- **ODD9 universelle** : contre-exemples LAB (gain impair 8 et 5) ; retirée (`LE/codex_bridge_843_corrected_odd_budget.txt:1`).
  Sous-route « Schur 10 = laplacien positif » : fausse sur c11_mix6 (`LE/codex_odd9_network_result.txt:12`) ; relaxations
  convexes (polytope des matchings) insuffisantes (`LE/codex_bridge_839_odd9_integer_cut.txt:9`).
- **KER-SYM universelle** : fausse à nullité 9 (`LE/codex_bridge_841_balanced_profiles.txt:14`) ; non forcée par dimension
  à ν = 14 (`LE/codex_bridge_839_odd9_integer_cut.txt:11`).
- **Famille G1 c55 non-grille** : exclue par F7 (`LE/codex_c55_excluded_after774.txt:9`) — le recouvrement grille et c ≠ (5,5)
  restent ouverts.
- **Famille locale <z,hM>** : exclue par F7 (`LE/codex_z5hm_delivery.txt:7`) ; c = (6,6) exclu par le damier (`LE/codex_z5hm_progress.txt:2`).
- **G1'' en test H-MATCH cassé avec c_m >= 4** : exclue (`LE/codex_bridge_809_grid_cut.txt:3`).
- **Les 52 germes (A)** : aucun prolongement par {4,6} (`LE/codex_51_extensions_and_coupling.txt:1`).
- **Borne inférieure sur P par les comptes seuls** : le census d'ordre 9 admet P = 0, même en entiers
  (`LE/codex_bridge_849_torsion_census_ng7.txt:3`) ; plancher 504 << 1190,4 (`LE/codex_coarse_floor_after768.txt:6`) ;
  moyenne simple automatiquement PSD (`LE/codex_global_counting_after764.txt:15`).
- **Positivité seule** : sur support 12 (832 cœurs PSD, `LE/codex_bridge_858_flat_prism_cores.txt:11`) ; positivité continue
  jamais infaisable (centre fractionnaire, `LE/H/README_GLOBAL_PSD.txt:13`) ; LP + PSD trop faible (`LE/codex_after738_family52.txt:3`).
- **Remariage à Γ fixe** (n_45, b_29) et **rematching pur d'une étoile** (urep100, H30_23) : impossibles
  (`LE/codex_bridge_870_mate_obstructions.txt:1`, `LE/codex_bridge_877_antipodal_rigidity.txt:5`) — portée : ces graphes seulement.
- **Prolongement des germes testés** : HB promu, urep100 (et son cœur 30), cadre 15 lignes : non prolongeables
  (`LE/codex_bridge_extension_construction.txt:1`, `LE/codex_bridge_complete_assembly.txt:3`, `LE/codex_bridge_global_columns.txt:3`,
  `LE/H/message_gray_block_obstruction_20261016.txt:1`).
- **Bornes grossières du couplage des 20 étiquettes** (K - CC^t/2, trace normalisée, restrictions aux sommes ou différences
  mates, « trois directions découplées ») : fermées, « à ne pas relancer » (`LE/H/bridge_sector_coupling_2bce4b9.txt:5`,
  `LE/H/bridge_odd_fixed_coupling.txt:7`).
- **Barrière du 7e label** (LAB 914) : retirée (`LE/H/lit/RELEVE_LITTERATURE_2026-10-16.txt:80`).
- **Phrase de la note 100** (« les lemmes ne pourront jamais exclure Conway ») : retirée (`LE/codex_bridge_849_torsion_census_ng7.txt:9`).
- **Preuve SOS externe** (2610.16266) : borne fausse (`LE/H/lit/23399271_RELEASE.txt:17`).
- **Branche min global c = 4** : 76/79 templates fermés (S), sous réserve (bug, portée) — voir §6.

#### 5. Questions ouvertes, classées par levier
**Levier local (blocs à quatre étoiles)**
- (H-MATCH) : ouvert ; manque « un argument binaire/C1/C2 qui exclue la saturation simultanée des contractions T et U »
  (`LE/codex_bridge_875_hmatch_prospects.txt:2`).
- N9-NG / NG5 / NG7 : ouverts ; cible exacte rang(F) >= 12 (`LE/H/bridge_resonance_bba12ce.txt:5`) ou rang S >= 9..12 pour
  c_l = 1..4 (`LE/codex_bridge_855_rank_target.txt:3`).
- ODD-PURE (rang D = 9) et SYM6 (rang Z >= 3) : ouverts (`LE/H/sector_coupling_2bce4b9/README.txt:2`) ; piste scalaire
  (tr Z)^2 > 2 tr(Z^2) vérifiée sur 12 côtés (`LE/H/bridge_sym6_67ffa75.txt:5`).
- C4DO général (support >= 14, coefficients généraux), ODDCONST : ouverts (`LE/codex_bridge_859_flat_c4do_proof.txt:23`).
- KER-SYM à ν >= 14 : non tranché (`LE/codex_bridge_841_balanced_profiles.txt:14`).
- c55 non-grille hors G1 (18 types × 19 permutations S4), recouvrement grille : ouverts (`LE/codex_reprise_785.txt:3`).
- Relations de poids 16 (271 profils) : ouvert (`LE/codex_after738_family52.txt:1`).
**Levier extension / cinq étoiles**
- R8 (huit labels {4,t}) : UNKNOWN (`LE/H/lit/ETAT_PONT_918_2026-10-16.txt:5`).
- Borne jointe PHI quand les deux diagonales existent (seulement 3) (`LE/H/LEMMES_PHI.txt:65`).
- Extraction d'une preuve lisible du cœur 30 (7 branches résistantes) (`LE/codex_bridge_global_columns_delivery.txt:5`).
**Levier global**
- Résoudre le modèle global 19 types (UNKNOWN) ; obstruction uniforme à « Γ84 binaire, C1 exact, T, U PSD »
  (`LE/H/message_global_cover_delivery_20261016.txt:7`, `LE/H/message_907_global_psd_reply.txt:5`).
- Coexistence des >= 4 blocs cassés par sommet (G18) par zéro-extension des noyaux (`LE/codex_bridge_875_hmatch_prospects.txt:3`).
- Templates 7, 9, 19 (min global c = 4), à recalculer après le correctif du 18/10 ; branche min c <= 3 (dont c = 1, où
  dim ker C = 14) (`AA/tmp/bridge_codex_20261017_2317.txt:9`, `LE/H/codex_corner_tables_2134.txt:3`).
- Borne inférieure sur P : exige une nouvelle majoration de la norme du tenseur cubique (`LE/codex_bridge_849_torsion_census_ng7.txt:11`).
**Levier asymétrie**
- Critère de symétrie forcée inapplicable tant que |Aut(H)| > #complétions n'est pas prouvé pour les bords 43/44 à <= 2
  complétions ; tuer les isomorphismes entre enracinements (Γ6, Γ8 à racines rigides) (`LE/H/bridge_family_synthesis_51460e5.txt:9`,
  `LE/H/lit/bridge_family_resonance_921.txt:11`).
**Levier arithmétique**
- Le minimum observé rang_F7 = 30 n'est PAS un théorème (une preuve contredirait la borne 28) (`LE/H/message_rank7_423127b.txt:1`).
**Levier littérature**
- Générateur Gegenbauer + comptages de Liao–Wang–Yu–Cai transposable à (99,14,1,2), non exécuté (`LE/H/lit/bridge_latest_arxiv_findings.txt:2`).

#### 6. Contradictions, redécouvertes, résultats remplacés ou retirés
- **Décalages chronologiques (pas des contradictions de fond)** : « A reste ouvert » (Codex, 14/10 22:38,
  `LE/codex_weight16_enumeration_733.txt:3`) puis « (A) est faux » (LAB 741, 23:00, `LE/codex_after741_joint_fourth_star.txt:1`) ;
  « je garde ODD9 ouvert » (11:05, `LE/codex_odd9_network_result.txt:14`), « ODD9 reste OUVERTE » (17:51,
  `LE/codex_bridge_839_odd9_integer_cut.txt:7`) puis retrait (19:10, `LE/codex_bridge_843_corrected_odd_budget.txt:1`).
- **Corrections internes de Codex** : 775 corrigé (dix signes -> cinq produits résiduels, `LE/codex_c55_excluded_after774.txt:3`) ;
  interprétation 819 corrigée (hM n'interdit PAS les relations mixtes, `LE/codex_z5hm_mixed_parity_826.txt:1`) ; taille du Schur
  33 -> 32 (`LE/H/sector_coupling_2bce4b9/README.txt:6`) ; registre 59 -> 48 entrées (`LE/H/bridge_family_synthesis_count.txt:1`) ;
  portée du point P = 0 (`LE/codex_coarse_floor_after768.txt:14`) ; « <= 16 signatures » = observation, pas borne
  (`AA/tmp/bridge_codex_20261017_2317.txt:9`) ; portée des certificats n_45/b_29 (`LE/codex_bridge_875_hmatch_prospects.txt:4`).
- **Corrections de lectures LAB par Codex** : HB_1 (le rang 2 du défaut ne force pas 13 ; 13 = 11 + 2 déjà dans la moyenne,
  `LE/codex_response_805.txt:8`) ; formule Φ du LAB 867 valable seulement après congruence par Π_+^{-1/2}
  (`LE/codex_bridge_867_pi_normalization.txt:3`).
- **Retraits LAB relayés** : barrière du 7e label (914 -> 916, `LE/H/lit/RELEVE_LITTERATURE_2026-10-16.txt:80`).
- **Retrait de Codex** : phrase de la note 100 (`LE/codex_bridge_849_torsion_census_ng7.txt:9`).
- **Résultats retirés par le bug OR-Tools du 18/10** (source hors sous-lot, `AA/notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt:3-5`,
  `:20-24`, `:30`) : fermeture 79/79 retirée, familles 7, 9, 19 rouvertes, 162 verdicts c3 retirés, campagne AWS c3star à
  recalculer. Dans ce sous-lot, l'entrée 110 (exclusions de Gram dans 7, 9, 19) est donc suspecte ; les 76 fermetures sont
  déclarées « non touchées » mais sans nouvelle vérification indépendante.
- **Redécouverte** : contre-exemple à 66 triangles (11 Paley(9)) à la borne SOS — Codex (16/10, `LE/H/literature_sos_2610_16266_counterexample.txt:1`)
  et theesfeld (Zenodo 23399271, 15/10, `LE/H/lit/23399271_RELEASE.txt:8`) ; Codex le reconnaît (`LE/H/lit/bridge_literature_findings.txt:1`).
- **Redécouverte partielle (externe)** : Kovaľ (Zenodo 23281436, 10/10) recoupe les réductions du projet, avec des bornes plus
  faibles (P <= 1354, grid-closed <= 3) (`LE/H/lit/RELEVE_LITTERATURE_2026-10-16.txt:31`) ; le LAB ne l'avait pas exploitée.
- **Re-dérivation d'un ancien mécanisme** : l'équivalence « C1 + binarité + deux PSD <=> SRG99 » est présentée comme
  « exploitation du vieux mécanisme de complétion » et « déjà suggérée par notre vieux commentaire de code »
  (`LE/H/README_GLOBAL_PSD.txt:6`, `LE/H/message_907_global_psd_reply.txt:5`).
- **Relecture croisée positive** : les deux lemmes de rupture de h (>= 3 et >= 4 lignes) sont vérifiés par le LAB
  (`W/stars_rank_2026-10-14/EXT84_2026-10-16.md:128`, `:136-137`).
- **Absence de relecture indépendante demandée** : Codex demande de ne pas lancer d'agent de re-audit de l'exclusion <z,hM>
  (« Dilan a explicitement demandé d'arrêter les vérifications indépendantes », `LE/codex_z5hm_delivery_explicit.txt:3`).
- **Formulation à vérifier** : « tr(TU) = Σ Γ_ij(1 - Γ_ij) … une borne strictement positive pour toutes les matrices binaires
  candidates donnerait la contradiction globale » (`LE/H/message_global_psd_delivery_20261016.txt:5`) — pour Γ binaire cette
  somme est identiquement nulle ; le sens visé n'est pas explicité.

#### 7. Matériaux pour la recombinaison

##### 7.1 Énoncés conditionnels « si X alors exclusion »
| # | X (précis) | conclusion | statut de X | statut de l'implication | source |
|---|---|---|---|---|---|
| K1 | NG5 : tout bloc à quatre étoiles admissible NON-grille avec T, U PSD et ν >= 14 a c >= 5 | pas de Conway (via c <= g + floor((6-g)/2) => g >= 4, t >= 8, P >= 924 > 852) | O | P (LAB, vérifiée par Codex) | `LE/codex_bridge_850_ng5_scope.txt:3` |
| K2 | NG7 : aucun bloc non-grille avec min(t(l),t(m)) <= 7 ne passe T/U PSD, ν_T >= 14, F7, DISC, extension | pas de Conway (il en existe >= 254) | O | P | `LE/codex_bridge_849_torsion_census_ng7.txt:7` |
| K3 | rang(F) >= 12 (F = Q + J/12) pour tout bloc non-grille admissible, droite de c minimum (<=> N9-NG) | pas de Conway (Conway force rang F <= 7 + c_min <= 11 sur un bloc non-grille à c_min <= 4) | O | P | `LE/H/bridge_resonance_bba12ce.txt:5` |
| K4 | NG5 restreint : rang S >= 9, 10, 11, 12 hors grille pour c_l = 1, 2, 3, 4 | NG5, donc pas de Conway | O | P (identités de rang) | `LE/codex_bridge_855_rank_target.txt:3` |
| K5 | ODD-PURE universel : rang D = 9 (aucune relation purement impaire non constante) | aucun bloc de Conway avec c_min = 1 ; pour c = 2, 3, 4 il resterait rang Z <= c - 2 | O | P | `LE/H/bridge_sym6_67ffa75.txt:3` |
| K6 | ODD-PURE + rang Z >= c - 1 (c = 2, 3, 4), ou SYM6 (rang Z >= 3) + rang D = 9 | N9-NG (cible Q7), donc pas de Conway | O | P | `LE/H/bridge_sym6_928_first.txt:3`, `LE/H/bridge_sym6_67ffa75.txt:3` |
| K7 | (H-MATCH) : T, U >= 0 et ν >= 14 => M_1 = h(M_0) et M_3 = h(M_2) | tout sommet est de Hamming => pas de Conway (L8) | O | P (LAB, acceptée par Codex) | `LE/codex_reprise_785.txt:1` |
| K8 | (A) + (C) | pas de Conway | (A) R | — | `LE/codex_after741_joint_fourth_star.txt:1` |
| K9 | un bord de Conway appartient à la famille G1 c55 non-grille | contradiction rang_F7(8T_S) >= 29 > 28 | — | E (établi) | `LE/codex_c55_excluded_after774.txt:1` |
| K10 | un bord de Conway porte la symétrie locale <z,hM> | contradiction (ν <= 14 ; à 14, rang_F7 >= 29 > 28) | — | C (établi) | `LE/codex_z5hm_delivery.txt:7` |
| K11 | les templates 7, 9, 19 sont fermés (correctement, après correctif) | aucun Conway dont toutes les droites ont c >= 4 | O (rouverts le 18/10) | S | `LE/H/codex_76sur79.txt:1`, `AA/tmp/bridge_codex_20261018_reply970.txt:3` |
| K12 | aucune Γ84 binaire C1-exacte n'a T et U PSD | pas de Conway (équivalence) | O | P | `LE/H/message_907_global_psd_reply.txt:5` |
| K13 | sur 84 étiquettes : T, U PSD et rang T <= 30 | l'objet est un SRG99 (sens « construction ») | — | P | `LE/codex_bridge_complete_assembly.txt:5` |
| K14 | #complétions ÉTIQUETÉES d'un bord H < |Aut(H)| | aucune complétion asymétrique de H (exclut C1 si H est forcé) | à établir pour chaque H | P | `LE/H/bridge_family_synthesis_51460e5.txt:9` |
| K15 | « borne strictement positive [du défaut tr(TU)] pour toutes les matrices binaires candidates » | contradiction globale | O (formulation ambiguë) | — | `LE/H/message_global_psd_delivery_20261016.txt:5` |
| K16 | (P) : toute arête est dans un prisme | P >= 231 (insuffisant seul contre 852) | O (conjecture) | P | `LE/codex_bridge_849_torsion_census_ng7.txt:13` |
| K17 | le minimum observé rang_F7(8T44) = 30 devient un théorème | contradiction avec <= 28 | non prouvé (refusé comme théorème) | — | `LE/H/message_rank7_423127b.txt:1` |
| K18 | G1'' et H-MATCH cassé | g_m <= 1 et c_m <= 3 (cubes c_m >= 4 exclus) | — | P | `LE/codex_bridge_809_grid_cut.txt:3` |
| K19 | <z,hM> et d = (7-2ε_l)(7-2ε_m) - (2(t+w)+1)^2 ≢ 0 mod 5 | b = 0 et null T <= 9 (7/14 types) | — | P | `LE/codex_z5hm_mod5_progress.txt:5` |
| K20 | moyenne à >= 40 cassures avec tr S < 20/7 | toutes ses orientations exclues | à tester | P | `LE/codex_response_792.txt:8` |
| K21 | diagonal rationnel d, H - diag(d) >= 0 et Σd > 10 | toutes les orientations d'une moyenne exclues | à tester | P | `LE/codex_response_792.txt:10` |
| K22 | (α_1…α_p)(β_1…β_p) > 1 (valeurs généralisées shortées) | nullité T < nullité T0 + p (ex. pas de ν = 14 si ν(T0) = 12 et p = 2) | à tester | P | `LE/codex_response_801.txt:6` |
| K23 | e(O ∪ S) = 49 pour un S équilibré | T non PSD | — | P | `LE/codex_bridge_839_odd9_integer_cut.txt:5` |
| K24 | une relation plate d'incidence nulle de support <= 14 touche O | contradiction (binaire, C1, C2, T, U PSD) | — | P | `LE/codex_bridge_862_support_fourteen.txt:1` |
| K25 | une étoile est rematchée seule (P -> P') en gardant T PSD | P'v = -v sur W = proj_S(ker T) ∩ ker(P + I) | — | P | `LE/codex_bridge_877_antipodal_rigidity.txt:3` |
| K26 | R8 UNSAT (après DRAT + modèle indépendant + relecture) | pas de Conway (énoncé LAB, relayé) | O (UNKNOWN) | énoncé LAB hors sous-lot | `LE/H/lit/ETAT_PONT_918_2026-10-16.txt:5` |
| K27 | si un voisinage de ligne fermé dans la base a plusieurs composantes C | égalités n_C(z) = c/6 pour tout z de X, conditions universelles de prolongement | — | P | `LE/H/lit/bridge_family_resonance_921.txt:9` |
| K28 | ν < 11 + max(c_l, c_m) | les équations du noyau seules ne forcent aucun h·p (symétrie forcée seulement possible à ν >= 14) | — | P | `LE/codex_bridge_833_mixed.txt:5` |

##### 7.2 Bornes quantitatives
**Prismes, grilles, transversales, drapeaux (globales)**
- P <= 1151 puis P <= 1150 (preuve cubique) ; P <= 11088/13, donc P <= 852 ; 6ρ <= P ; 1386 - P - 5ρ >= 0 ; ρ <= 126 (C)
  `LE/codex_mixed_budget_direction_after778.txt:1`.
- Σ mixtes = 12474 - 45ρ + 3O + 6H + Δ >= 6804, moyenne >= 36/11 sur 2079 drapeaux, excès >= 567 (P) `LE/codex_mixed336_after778.txt:1`.
- >= 336 des 2079 drapeaux ont >= 4 relations mixtes ; >= 18 sommets en portent ; 13b + 20e >= 273 ; profil minimal de b
  pour e = 0..18, 21 : 21,21,21,21,21,21,20,19,17,15,11,7,3,1,0,0,0,0,0,0 (P) `LE/codex_mixed336_after778.txt:3`, `:5`.
- >= 254 blocs non-grille avec min t <= 7 ; m >= 18 droites à t <= 7 ; I >= max(9m, 6m + 216) ; e(L) <= floor(7m/2 + m^2/42) ;
  N >= 1773/7 en m = 18 (P) `LE/codex_bridge_849_torsion_census_ng7.txt:5`, `LE/codex_bridge_850_ng5_scope.txt:7`.
- Il existe une racine x avec Σ_{l ∋ x} t(l) <= 51 (6P <= 5112) ; à cette racine m_NG >= 9 ; si toutes les droites ont c >= 4,
  une droite à c = 4 passe par x (P) `LE/H/message_root_cover79_72d47c3.txt:2`.
- Second moment : 15||E||_F^2 + 86 trE + 92h - 74ΣE <= 3520 ; 15 Σ_{l<m} ||E_vlm||_F^2 + 464 t_v + 144 d_v <= 374976 ;
  5 Σ ||E_vlm||_F^2 + 928P + 48Z <= 12374208 ; 5Δ_global + 448P - 72Z <= 7135128 ; minimum moyen 504 atteint, seuil 1190,4 (P/E)
  `LE/codex_global_counting_after764.txt:6`, `:10`, `:12` ; `LE/codex_coarse_floor_after768.txt:4`, `:6`.
- Grille : (k-4)(k-14)/2 sommets extérieurs sans voisin = 0, 0, 72, 5292, 485100 pour k = 4, 14, 22, 112, 994 ; débordement de la
  cinquième étoile D_k offsets 8, -52, -5137, -483622 (k = 14, 22, 112, 994) (P) `LE/H/bridge_family_synthesis_51460e5.txt:5`, `:7`.

**Nullités, rangs, F7 (blocs locaux)**
- G1 : rang T <= 30 => Σ nullités non triviales >= 9 - min(c_l, c_m) ; c = (4,4) : 10 cibles ; c = (5,5) : 6 cibles (P)
  `LE/codex_g1_character_rank_targets.txt:5`.
- c55 non-grille (T, U PSD) : nullités (10,1,1,k), k >= 2 ; 972 -> 180 -> 126 cas (E) `LE/codex_c55_exact_joint_sectors.txt:3` ;
  rang_F7(8T_S) >= 29 ; distribution 29 : 24, 30 : 2334, 31 : 29358, 32 : 113436 sur 145152 cas (E) `LE/codex_c55_excluded_after774.txt:5`.
- c55 non-grille : comptes extérieurs N0 = 10, N1 = 24, N2 = 6 ; >= 29 (ou 30) des 40 profils manquants rompent h (P)
  `LE/codex_c55_global_after772.txt:3`, `:5`.
- <z,hM> : null_Q T = ν0 + 4a + 4b, ν0 ∈ {5,6}, a, b <= 1, donc ν <= 14 ; à 14, rang_F7(8T) >= 5 + 4·3 + 4·3 = 29 ; 128/32 colonnes
  par côté (rationnel), 88/212 (mod 7) ; 520 relevés admissibles tous rejetés (416 U, 104 T) (C) `LE/codex_z5hm_exclusion_progress.txt:3`,
  `:7` ; `LE/codex_z5hm_delivery.txt:8`. Plafond LAB local ν <= 9 (339556 structures, 192 PSD) (E) `LE/codex_z5hm_mixed_parity_826.txt:1`.
- ν = c(l) + 2 + corang(Q) ; rang T = 23 - c(l) + rang F ; rang T = 32 - c(l) - δ + rang Z, δ = 9 - rang D ; rang G = 11 - c(m) ;
  rang L = 10 - c(m) >= 5 hors grille ; rang E = 12 - c (P) `LE/H/bridge_resonance_bba12ce.txt:3`, `LE/H/sector_coupling_2bce4b9/README.txt:2`,
  `LE/H/bridge_sym6_boundary_4c9ca38.txt:1`, `:3`.
- d_l = 9 - gain impair = (b - 2) + η_l, 0 <= η_l <= s ; gain pair résiduel = 12 + c_l - ν + d_l (P) `LE/codex_bridge_843_defect_decomposition.txt:4`.
- E >= G/5 + (2/5)(I - M) (P) `LE/H/sym6_energy_43c496e/BORNE_ENERGIE_PAIRE_2026_10_16.txt:11` ; sous Conway le Schur restant de taille 32
  a rang <= 19 (`:101`, corrigé 33 -> 32).
- Défaut h : ||Δ||_F^2 = 4b, ||B||_F^2 = b/2, q/2 <= ||B||_F^2 <= q, rang B <= 10, ||B||_op^2 >= b/20 (P) `LE/codex_response_792.txt:3`, `:5`.
- Orientations : d <= 13, <= 2^12 = 4096 essais modulo h (<= 64 si toutes les valences croisées valent 2) ; 552 signes admissibles
  sur K4,6 - K2,2 (P) `LE/codex_response_797.txt:5`, `:7`.
- Rematchings : 945 types géométriques, nombres par rang E = 0..4 : 1, 20, 140, 400, 384 (P) `LE/codex_response_805.txt:4`.
- Coupe plate : e(O ∪ S) <= 48 (e(S) <= 44 si O grille) ; 31752 directions h-impaires ; 586278 directions équilibrées ; maxima
  observés 43-46 (P/E) `LE/codex_bridge_839_odd9_integer_cut.txt:5`, `LE/codex_bridge_841_balanced_profiles.txt:4`, `:10`.
- Relations plates : support <= 12 => C4DO ; support <= 14 => nulles sur O ; touchant O => support >= 16 (P)
  `LE/codex_bridge_862_support_fourteen.txt:1`.
- Trois étoiles : 4e relation positive normalisée de poids >= 16 ; poids 16 : 1149/1420 profils exclus, 271 restent (C/S)
  `LE/codex_after738_family52.txt:1`.
- Coupes strictes : Σ >= -31 (40 anti), Σ >= -127 (60 sym) (P) `LE/codex_strict_upper_100.txt:4`, `:5`.
- Remariage : Rayleigh(4I + Γ) <= -4 - 5/874 (n_45), = -33/8 (b_29) (C) `LE/codex_bridge_870_mate_obstructions.txt:4`, `:5`.

**Rupture de symétrie (bornes inférieures sur le nombre de lignes non h-invariantes)**
- Toute structure à cinq étoiles : >= 3 des 8 lignes X rompent h (D >= 12 ; en général D >= 2k - 16 et >= ceil((k-8)/2) lignes) ;
  >= 4 lignes pour k = 14 (P, relu LAB) `LE/H/message_defect_20261016.txt:4`, `LE/H/message_four_broken_20261016.txt:1`.
- PHI : D_a >= 12 + 2t_a - 4δ_a >= 10 ; >= 3 lignes rompent chaque φ ; au plus floor((12 - t_a)/2) des 60 sommets extérieurs
  φ-appariés ; b + (d_1 ET d_2) >= 4 (P) `LE/H/LEMMES_PHI.txt:12`, `:13`, `:29`.

**Comptes de complétions / de structures (à comparer à la borne de symétrie forcée 99 × 645120 = 99 × |W(B7)|)**
- Normalisation d'un matching racine : 10395 matchings -> 11 types (19 types pointés autour d'une droite de t minimum) ; la
  couverture est un quotient par renommage des paires (P) `LE/H/message_global_cover_scope_20261016.txt:3`, `:5`.
- Cas d'égalité recollé : 4480 matchings étiquetés (2 formes), 38 orientations × 15 M × 4^6 relevés = 2334720 bijections (E)
  `LE/codex_coarse_floor_after768.txt:8`.
- c55 non-grille (G1) : quotient trivial UNIQUE à renommage des 5 paires près (P) `LE/codex_c55_trivial_quotient_756.txt:1`.
- G1'' : 96 interfaces étiquetées du carré forcé, toutes équivalentes sous le wreath C2 wr S4 (transitif) (P) `LE/codex_bridge_807_square.txt:3`, `:4`.
- c = (5,5) non-grille sans G1 : 128 cœurs étiquetés / 18 types, puis 19 permutations S4 (18·24^19 non énumérable) (P) `LE/codex_reprise_785.txt:3`.
- HB_1 promu : 120 géométries extérieures admissibles (incidences sur Γ fixe, pas 120 graphes) ; urep100 : 1 (E)
  `LE/codex_bridge_root_schur_construction.txt:5`.
- hv_h_c22_H30_23 : exactement 120 = 5! appariements M admissibles à Γ fixe (sur 945) ; comptes étiquetés par c : 22 : 16 ; 23/32 : 20 ;
  24/42 : 10 ; 25/52 : 2 ; 33 : 24 ; 34/43 : 8 (E/P) `LE/codex_bridge_845_mate_family.txt:7`, `:13`.
- Colonnes extérieures : urep100 (4,6) : exactement 2 colonnes binaires (toutes deux forçant rang 31) ; HB promu (4,6) : 0 ;
  cœur 30 : domaines de 4 à 277 colonnes par étiquette, choix simultané impossible (E/S) `LE/codex_bridge_complete_assembly.txt:3`,
  `LE/codex_bridge_global_columns.txt:3`.
- Cadre 13 : seules 02, 03, 08, 013 ajoutables à L0, chacune avec UN seul voisinage global ; au plus une ajoutable (14 maximum
  conditionnel) (E) `LE/H/message_star15_phi_83ecbbe.txt:5`.
- « Bords 43/44 à <= 2 complétions » (non prouvés de |Aut(H)| > 2) (P, critère) `LE/H/bridge_family_synthesis_51460e5.txt:9`.
- Remariages : 944 nouveaux M classés pour n_45 et b_29 (E) `LE/codex_bridge_870_mate_obstructions.txt:13` ; 120 switches par germe,
  240 témoins négatifs (C) `LE/codex_bridge_877_antipodal_rigidity.txt:7`.
- Branche min c = 4 : 2^21 graphes -> 221 G, 12951 partages -> 367 -> 200 (197 de min c 4) -> 100 -> 87 -> 79 templates ; Gram :
  116684 matrices, 5620 orbites, 5569 représentants ; cas 7 : 3407872 -> 101010 ; cas 19 : 262144 -> 12087 ; signatures <= 5^4 = 625
  par colonne (h^tR^+h <= 5/2) ; 1 + 14·32 = 449 voisinages de droite pour 7/9/19 (S/P) `LE/H/message_root_components_cd34d43.txt:4`,
  `:5` ; `LE/H/codex_d07ac4a_cover15_message.txt:2` ; `AA/tmp/bridge_codex_20261017_2317.txt:7`.
- Coût : campagne v2 = 909 Gram, 84637 codes, nominal 4232 CPU·h sans garantie ; 5,5 GiB de RAM par travailleur (H)
  `AA/data/codex_line_resonance_20261016/bridge_20261018_0326.txt:3`, `AA/data/codex_line_resonance_20261016/bridge_20261018_0352.txt:1`.

**Vecteurs de norme donnée**
- h entier propre -4 (Σh = 0) : ||h||^2 >= m^2 + 7|m| ; norme 14 => h ∈ {0,±1}, 7 + et 7 -, support co-Heawood 2-(7,4,2) ;
  h_Q = T·1_Q a norme 7(8 - 2e(Q)) = 28/42/56 (e = 2/1/0) ; à norme 28 : au plus un +2 et un -2, aucun triangle strictement de signe
  constant ; r^2 + s^2 + 7(r+s) + 2e(r+s+1) + 2c <= N + 4 ; E+ <= N/2 + 2 - 8r (P) `AA/tmp/bridge_codex_short_vectors_20261017.txt:2`,
  `AA/tmp/bridge_codex_20261017_2346.txt:4`, `:9`, `AA/tmp/bridge_codex_20261018_0100.txt:7`, `AA/tmp/bridge_codex_20261018_0024.txt:5`.
- z = T_far·1_O vecteur propre -4 entier de norme 28 (14 +, 14 -) dans c55 non-grille (P) `LE/codex_c55_global_after772.txt:3`.
- Représentations sphériques : dimension 54 (3/14 arête, -1/21 non-arête) ; dimension 44 (-2/7, 1/28) (P) `LE/H/lit/RELEVE_LITTERATURE_2026-10-16.txt:61`.

##### 7.3 Lemmes ouverts / étapes manquantes (et ce qu'ils donneraient)
- NG5 / NG7 / N9-NG (rang F >= 12 hors grille) -> pas de Conway avec P <= 852 (`LE/codex_bridge_850_ng5_scope.txt:5`, `LE/H/bridge_resonance_bba12ce.txt:5`).
- (H-MATCH) -> pas de Conway via L8 ; étape manquante : exclure la saturation simultanée des contractions T et U par un argument
  binaire/C1/C2 (`LE/codex_bridge_875_hmatch_prospects.txt:2`).
- ODD-PURE (rang D = 9) -> c_min = 1 impossible ; + rang Z >= c - 1 ou SYM6 -> N9-NG (`LE/H/bridge_sym6_67ffa75.txt:3`).
- SYM6 (rang Z >= 3) : suffisance scalaire (tr Z)^2 > 2 tr(Z^2) ou un mineur principal 3x3 positif (120 positions) (`LE/H/bridge_sym6_67ffa75.txt:5`).
- C4DO général / ODDCONST (`LE/codex_bridge_859_flat_c4do_proof.txt:23`).
- KER-SYM à ν >= 14 (la dimension ne l'interdit plus à 14 : `LE/codex_bridge_833_mixed.txt:5`) -> mécanisme de symétrie forcée.
- Contrôle de la perte de rang A <= L après le bord (SYM6) (`LE/H/bridge_sym6_boundary_4c9ca38.txt:5`).
- Coexistence des >= 4 blocs cassés par sommet (G18) par zéro-extension : 8Γ_RS q = 2(1^t q)1_R - B_R^t(3I+M)B_S q
  (`LE/codex_bridge_875_hmatch_prospects.txt:3`).
- Templates 7, 9, 19 (min global c = 4) -> exclusion du cas « toutes droites c >= 4 » ; branche min c <= 3 (extension du
  générateur aux degrés 5, 6 ; c = 1 : dim ker C = 14) (`LE/H/codex_corner_tables_2134.txt:3`, `AA/tmp/bridge_codex_20261017_2317.txt:9`) ;
  exploitation de c >= 4 sur les droites non racines (`LE/H/codex_signature_moments_reprise.txt:1`).
- Majoration nouvelle de la norme du tenseur cubique -> borne inférieure sur P (`LE/codex_bridge_849_torsion_census_ng7.txt:11`).
- Borne jointe PHI avec deux diagonales (3 -> 4) (`LE/H/LEMMES_PHI.txt:65`).
- Preuve que |Aut(H)| > #complétions pour un bord forcé -> critère de symétrie forcée (`LE/H/bridge_family_synthesis_51460e5.txt:9`).
- Extraction de certificats (DRAT/Farkas) des verdicts CP-SAT (cœur 30 : 7 branches ; templates : « pas DRAT portable »)
  (`LE/codex_bridge_global_columns_delivery.txt:5`, `LE/H/message_root_components_cd34d43.txt:5`).
- Relations de poids 16 (271 profils), c55 grille, c55 hors G1 (`LE/codex_after738_family52.txt:1`, `LE/codex_reprise_785.txt:3`).
- R8 (UNSAT exclurait Conway selon le LAB) (`LE/H/lit/ETAT_PONT_918_2026-10-16.txt:5`).

##### 7.4 Méthodes transférables d'un cas à l'autre
- **Paramétrage en k de la famille srg(v,k,1,2)** (k = 4, 14, 22, 112, 994) : résonance (k-14), débordement D_k, rupture h
  D >= 2k - 16 ; montre ce qui est spécifique à 99 et explique la facilité des solveurs à 243 (`LE/H/bridge_family_synthesis_51460e5.txt:3`,
  `LE/H/message_defect_20261016.txt:4`).
- **Moteur de comptes globaux paramétré** (root_count 4/14/22 ; contrôles rook9 = srg(9,4,1,2) SAT et « 19 » UNSAT, vraisemblablement
  srg(19,6,1,2)) : transférable à srg(243,22,1,2) et aux calibrations (`LE/codex_bridge_global_columns_delivery.txt:3`, `LE/H/README_GLOBAL_COVER.txt:25`).
- **Borne globale F7 appliquée à des familles locales** (G1 c55, <z,hM>) : schéma « décomposition exacte en secteurs + rang
  modulaire minimal > 28 » réutilisable pour toute famille locale à symétrie partielle (`LE/codex_c55_excluded_after774.txt:9`).
- **Filtres cyclotomiques mod 5 / Z[ζ5]/5** pour familles Z5-symétriques (`LE/codex_z5hm_mod5_progress.txt:4`, `LE/codex_bridge_831_ramified.txt:3`).
- **Discipline de certificats** : Farkas racine si LP infaisable, sinon arbre de branchement avec Farkas exact par feuille ;
  un verdict HiGHS flottant rationalisé n'est pas un certificat (`LE/codex_bridge_812_exact_route.txt:2`, `:3`) — applicable aux
  campagnes C2, C3, c3star.
- **Projection exacte de C2** sans variables auxiliaires (`LE/codex_bridge_815_projection.txt:2`).
- **Bibliothèque de coupes PSD entières apprises**, transportables entre réparations et entre racines (`LE/codex_bridge_psd_learning.txt:3`).
- **Comptes globaux exacts du 84 avant de fixer les arêtes entre nouveaux sommets** (« méthode constructive transférable »,
  `LE/codex_bridge_global_columns.txt:3`).
- **DISC (classe de carrés) comme filtre de colonnes pendant la construction** (`LE/codex_bridge_rank_release_disc.txt:5`).
- **Encodage exact rang_F7 <= 28** (M = UV) dans un modèle CP (`LE/H/message_rank7_423127b.txt:2`).
- **Générateur Gegenbauer + comptages de Liao–Wang–Yu–Cai** (cinq/six points, valeurs propres calculées depuis les paramètres)
  transposable à (99,14,1,2) ; lemmes du §4 non transférables tels quels à -4 (`LE/H/lit/RELEVE_LITTERATURE_2026-10-16.txt:17`).
- **Budget extérieur** G - (2q+1)F + q(q+1)m >= 0 pour tout ensemble S (`LE/H/lit/RELEVE_LITTERATURE_2026-10-16.txt:69`).
- **Critère de symétrie forcée** issu de la campagne srg(243) (Γ6/Γ8, racines rigides) vers le cas C1 de Conway
  (`LE/H/lit/bridge_family_resonance_921.txt:11`).
- **Lemmes E3 et vecteurs courts** (universels) vers la branche c = 1 du LAB (`AA/tmp/bridge_codex_no_path4_20261017.txt:3`,
  `AA/tmp/bridge_codex_20261018_0024.txt:5`).
- **Équilibre n_C(z) = c/6** comme condition universelle de prolongement dans R8 (`LE/H/lit/bridge_family_resonance_921.txt:9`).
- **Mise en garde de transfert** : les 76 exclusions de la branche min c = 4 ne se transfèrent pas à un voisinage seulement
  localement c >= 4 ni à c >= 3 (`AA/tmp/bridge_codex_20261018_reply970.txt:3`) ; L8 et L10/U ne se transportent pas hors
  grille, L16/Krein oui (`LE/codex_bridge_849_torsion_census_ng7.txt:11`).

#### 8. Couverture du sous-lot (145 fichiers)
Légende : **lu** = lu entièrement ; **survolé** = lecture partielle (dit quoi) ; **non lu** = avec raison.
Tous les fichiers sont à une seule localisation (aucune copie divergente). Chemins relatifs à `C:/home/researcher/Desktop/Recherche_Conway/`.

| idx | fichier | état |
|---|---|---|
| 206 | `lab_exchange_2026-10-14/codex_51_extensions_and_coupling.txt` (2026-10-14 23:15) | lu |
| 207 | `lab_exchange_2026-10-14/codex_7adic_direction_after774.txt` (2026-10-15 01:08) | lu |
| 208 | `lab_exchange_2026-10-14/codex_after738_family52.txt` (2026-10-14 22:55) | lu |
| 209 | `lab_exchange_2026-10-14/codex_after741_joint_fourth_star.txt` (2026-10-14 23:00) | lu |
| 210 | `lab_exchange_2026-10-14/codex_after745_coupling.txt` (2026-10-14 23:12) | lu |
| 211 | `lab_exchange_2026-10-14/codex_after752_fourstar_columns.txt` (2026-10-14 23:26) | lu |
| 212 | `lab_exchange_2026-10-14/codex_after757_null13_scope.txt` (2026-10-14 23:40) | lu |
| 213 | `lab_exchange_2026-10-14/codex_bridge_807_square.txt` (2026-10-15 13:07) | lu |
| 214 | `lab_exchange_2026-10-14/codex_bridge_807_square_export.txt` (2026-10-15 13:15) | lu |
| 215 | `lab_exchange_2026-10-14/codex_bridge_809_grid_cut.txt` (2026-10-15 13:18) | lu |
| 216 | `lab_exchange_2026-10-14/codex_bridge_812_exact_export.txt` (2026-10-15 13:44) | lu |
| 217 | `lab_exchange_2026-10-14/codex_bridge_812_exact_route.txt` (2026-10-15 13:34) | lu |
| 218 | `lab_exchange_2026-10-14/codex_bridge_815_projection.txt` (2026-10-15 13:50) | lu |
| 219 | `lab_exchange_2026-10-14/codex_bridge_815_projection_export.txt` (2026-10-15 14:00) | lu |
| 220 | `lab_exchange_2026-10-14/codex_bridge_831_ramified.txt` (2026-10-15 16:06) | lu |
| 221 | `lab_exchange_2026-10-14/codex_bridge_833_mixed.txt` (2026-10-15 16:22) | lu |
| 222 | `lab_exchange_2026-10-14/codex_bridge_836_odd9_progress.txt` (2026-10-15 17:29) | lu |
| 223 | `lab_exchange_2026-10-14/codex_bridge_839_odd9_integer_cut.txt` (2026-10-15 17:51) | lu |
| 224 | `lab_exchange_2026-10-14/codex_bridge_841_balanced_profiles.txt` (2026-10-15 18:02) | lu |
| 225 | `lab_exchange_2026-10-14/codex_bridge_843_corrected_odd_budget.txt` (2026-10-15 19:10) | lu |
| 226 | `lab_exchange_2026-10-14/codex_bridge_843_defect_decomposition.txt` (2026-10-15 19:21) | lu |
| 227 | `lab_exchange_2026-10-14/codex_bridge_845_mate_family.txt` (2026-10-15 19:38) | lu |
| 228 | `lab_exchange_2026-10-14/codex_bridge_849_torsion_census_ng7.txt` (2026-10-15 21:01) | lu |
| 229 | `lab_exchange_2026-10-14/codex_bridge_850_ng5_scope.txt` (2026-10-15 21:06) | lu |
| 230 | `lab_exchange_2026-10-14/codex_bridge_854_kernel_partition_closure.txt` (2026-10-15 22:07) | lu |
| 231 | `lab_exchange_2026-10-14/codex_bridge_855_rank_target.txt` (2026-10-15 22:11) | lu |
| 232 | `lab_exchange_2026-10-14/codex_bridge_858_flat_prism_cores.txt` (2026-10-15 23:09) | lu |
| 233 | `lab_exchange_2026-10-14/codex_bridge_859_flat_c4do_proof.txt` (2026-10-15 23:21) | lu |
| 234 | `lab_exchange_2026-10-14/codex_bridge_862_support_fourteen.txt` (2026-10-15 23:34) | lu |
| 235 | `lab_exchange_2026-10-14/codex_bridge_865_hmatch_target_input.txt` (2026-10-16 05:10) | lu |
| 236 | `lab_exchange_2026-10-14/codex_bridge_867_pi_normalization.txt` (2026-10-16 05:11) | lu |
| 237 | `lab_exchange_2026-10-14/codex_bridge_870_mate_obstructions.txt` (2026-10-16 05:31) | lu |
| 238 | `lab_exchange_2026-10-14/codex_bridge_873_full_spectral_filter.txt` (2026-10-16 05:37) | lu |
| 239 | `lab_exchange_2026-10-14/codex_bridge_875_hmatch_prospects.txt` (2026-10-16 05:57) | lu |
| 240 | `lab_exchange_2026-10-14/codex_bridge_877_antipodal_rigidity.txt` (2026-10-16 07:30) | lu |
| 241 | `lab_exchange_2026-10-14/codex_bridge_complete_assembly.txt` (2026-10-16 09:52) | lu |
| 242 | `lab_exchange_2026-10-14/codex_bridge_extension_construction.txt` (2026-10-16 09:41) | lu |
| 243 | `lab_exchange_2026-10-14/codex_bridge_global_columns.txt` (2026-10-16 11:14) | lu |
| 244 | `lab_exchange_2026-10-14/codex_bridge_global_columns_delivery.txt` (2026-10-16 11:23) | lu |
| 245 | `lab_exchange_2026-10-14/codex_bridge_microscopic_repair.txt` (2026-10-16 10:06) | lu |
| 246 | `lab_exchange_2026-10-14/codex_bridge_psd_learning.txt` (2026-10-16 10:54) | lu |
| 247 | `lab_exchange_2026-10-14/codex_bridge_rank_release_disc.txt` (2026-10-16 10:26) | lu |
| 248 | `lab_exchange_2026-10-14/codex_bridge_root_schur_construction.txt` (2026-10-16 09:11) | lu |
| 249 | `lab_exchange_2026-10-14/codex_c55_exact_joint_sectors.txt` (2026-10-14 23:55) | lu |
| 250 | `lab_exchange_2026-10-14/codex_c55_excluded_after774.txt` (2026-10-15 01:13) | lu |
| 251 | `lab_exchange_2026-10-14/codex_c55_global_after772.txt` (2026-10-15 00:48) | lu |
| 252 | `lab_exchange_2026-10-14/codex_c55_trivial_quotient_756.txt` (2026-10-14 23:47) | lu |
| 253 | `lab_exchange_2026-10-14/codex_coarse_floor_after768.txt` (2026-10-15 00:24) | lu |
| 254 | `lab_exchange_2026-10-14/codex_fourstar_schur_741.txt` (2026-10-14 23:06) | lu |
| 255 | `lab_exchange_2026-10-14/codex_g1_character_rank_targets.txt` (2026-10-14 23:32) | lu |
| 256 | `lab_exchange_2026-10-14/codex_global_counting_after764.txt` (2026-10-15 00:10) | lu |
| 257 | `lab_exchange_2026-10-14/codex_hmatch_20261016/LEMMES_PHI.txt` (2026-10-16 13:17) | lu |
| 258 | `lab_exchange_2026-10-14/codex_hmatch_20261016/README_GLOBAL_COVER.txt` (2026-10-16 14:45) | lu |
| 259 | `lab_exchange_2026-10-14/codex_hmatch_20261016/README_GLOBAL_PSD.txt` (2026-10-16 15:11) | lu |
| 260 | `lab_exchange_2026-10-14/codex_hmatch_20261016/README_GLOBAL_STAR12.txt` (2026-10-16 12:23) | lu |
| 261 | `lab_exchange_2026-10-14/codex_hmatch_20261016/README_STAR_REPAIR_PHI.txt` (2026-10-16 13:17) | lu |
| 262 | `lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_even_energy_43c496e.txt` (2026-10-16 20:50) | lu |
| 263 | `lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_family_synthesis_51460e5.txt` (2026-10-16 19:35) | lu |
| 264 | `lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_family_synthesis_count.txt` (2026-10-16 19:35) | lu |
| 265 | `lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_odd_fixed_coupling.txt` (2026-10-16 21:00) | lu |
| 266 | `lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_resonance_925_first.txt` (2026-10-16 19:50) | lu |
| 267 | `lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_resonance_bba12ce.txt` (2026-10-16 19:57) | lu |
| 268 | `lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_sector_coupling_2bce4b9.txt` (2026-10-16 21:04) | lu |
| 269 | `lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_sym6_67ffa75.txt` (2026-10-16 20:29) | lu |
| 270 | `lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_sym6_928_first.txt` (2026-10-16 20:24) | lu |
| 271 | `lab_exchange_2026-10-14/codex_hmatch_20261016/bridge_sym6_boundary_4c9ca38.txt` (2026-10-16 20:44) | lu |
| 272 | `lab_exchange_2026-10-14/codex_hmatch_20261016/codex_41d23bb_cover20_message.txt` (2026-10-16 22:11) | lu |
| 273 | `lab_exchange_2026-10-14/codex_hmatch_20261016/codex_74sur79_signatures.txt` (2026-10-16 23:08) | lu |
| 274 | `lab_exchange_2026-10-14/codex_hmatch_20261016/codex_75sur79.txt` (2026-10-16 23:44) | lu |
| 275 | `lab_exchange_2026-10-14/codex_hmatch_20261016/codex_76sur79.txt` (2026-10-17 00:06) | lu |
| 276 | `lab_exchange_2026-10-14/codex_hmatch_20261016/codex_corner_tables_2134.txt` (2026-10-16 23:34) | lu |
| 277 | `lab_exchange_2026-10-14/codex_hmatch_20261016/codex_d07ac4a_cover15_message.txt` (2026-10-16 22:28) | lu |
| 278 | `lab_exchange_2026-10-14/codex_hmatch_20261016/codex_signature_moments_reprise.txt` (2026-10-16 22:37) | lu |
| 279 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23281359_milgram_obstruction.pdf` (2026-10-16 15:47) | non lu (PDF de littérature tierce, Kovaľ, méthode BMV/Milgram ; contenu résumé par RELEVE_LITTERATURE_2026-10-16.txt:34-36) |
| 280 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23281359_milgram_obstruction.txt` (2026-10-16 15:47) | survolé (extraction texte d'un article tiers : titre et résumé seulement — Kovaľ, « The Bannai–Munemasa–Venkov lattice method for SRG ») |
| 281 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23281436_conway99_local.pdf` (2026-10-16 15:47) | non lu (PDF de littérature tierce, Kovaľ, structure locale de srg(99,14,1,2) ; résumé par RELEVE_LITTERATURE_2026-10-16.txt:28-32) |
| 282 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23281436_conway99_local.txt` (2026-10-16 15:47) | survolé (extraction texte d'un article tiers : titre et résumé seulement — Kovaľ, « On the local structure of a hypothetical SRG (99,14,1,2) ») |
| 283 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23399271_RELEASE.pdf` (2026-10-16 15:47) | non lu (PDF du dépôt externe theesfeld ; même contenu que la version texte 23399271_RELEASE.txt, lue) |
| 284 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/23399271_RELEASE.txt` (2026-10-16 15:47) | lu |
| 285 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/ETAT_PONT_918_2026-10-16.txt` (2026-10-16 19:08) | lu |
| 286 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/RELEVE_LITTERATURE_2026-10-16.txt` (2026-10-16 16:59) | lu |
| 287 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/bridge_family_resonance_921.txt` (2026-10-16 19:21) | lu |
| 288 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/bridge_global_exact_letter_918.txt` (2026-10-16 19:07) | lu |
| 289 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/bridge_latest_arxiv_findings.txt` (2026-10-16 15:59) | lu |
| 290 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/bridge_literature_findings.txt` (2026-10-16 15:48) | lu |
| 291 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_20261016/bridge_product_encoding_scope.txt` (2026-10-16 16:59) | lu |
| 292 | `lab_exchange_2026-10-14/codex_hmatch_20261016/literature_sos_2610_16266_counterexample.txt` (2026-10-16 15:32) | lu |
| 293 | `lab_exchange_2026-10-14/codex_hmatch_20261016/matrice_15_lignes/matrice_partielle_84.txt` (2026-10-16 13:25) | survolé (données : matrice partielle 84x84 du cadre 15 lignes, en-tête et 15 premières lignes ; décrite par message_star15_phi_83ecbbe) |
| 294 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_907_global_psd_reply.txt` (2026-10-16 15:01) | lu |
| 295 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_defect_20261016.txt` (2026-10-16 11:34) | lu |
| 296 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_four_broken_20261016.txt` (2026-10-16 11:49) | lu |
| 297 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_global_cover_delivery_20261016.txt` (2026-10-16 14:45) | lu |
| 298 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_global_cover_scope_20261016.txt` (2026-10-16 14:26) | lu |
| 299 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_global_psd_delivery_20261016.txt` (2026-10-16 15:11) | lu |
| 300 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_global_star12_20261016.txt` (2026-10-16 12:23) | lu |
| 301 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_gray_block_obstruction_20261016.txt` (2026-10-16 13:55) | lu |
| 302 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_phi_899_reply.txt` (2026-10-16 12:50) | lu |
| 303 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_rank7_423127b.txt` (2026-10-16 21:54) | lu |
| 304 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_root_components_cd34d43.txt` (2026-10-16 21:35) | lu |
| 305 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_root_cover79_72d47c3.txt` (2026-10-16 21:49) | lu |
| 306 | `lab_exchange_2026-10-14/codex_hmatch_20261016/message_star15_phi_83ecbbe.txt` (2026-10-16 13:18) | lu |
| 307 | `lab_exchange_2026-10-14/codex_hmatch_20261016/sector_coupling_2bce4b9/README.txt` (2026-10-16 21:04) | lu |
| 308 | `lab_exchange_2026-10-14/codex_hmatch_20261016/sym6_boundary_4c9ca38/README.txt` (2026-10-16 20:44) | lu |
| 309 | `lab_exchange_2026-10-14/codex_hmatch_20261016/sym6_energy_43c496e/BORNE_ENERGIE_PAIRE_2026_10_16.txt` (2026-10-16 20:48) | lu |
| 310 | `lab_exchange_2026-10-14/codex_hmatch_20261016/sym6_energy_43c496e/README.txt` (2026-10-16 20:50) | lu |
| 311 | `lab_exchange_2026-10-14/codex_mixed336_after778.txt` (2026-10-15 01:25) | lu |
| 312 | `lab_exchange_2026-10-14/codex_mixed_budget_direction_after778.txt` (2026-10-15 01:20) | lu |
| 313 | `lab_exchange_2026-10-14/codex_nonnegative_weight_bound_733.txt` (2026-10-14 22:32) | lu |
| 314 | `lab_exchange_2026-10-14/codex_odd9_network_result.txt` (2026-10-15 11:05) | lu |
| 315 | `lab_exchange_2026-10-14/codex_odd_census_after769.txt` (2026-10-15 00:32) | lu |
| 316 | `lab_exchange_2026-10-14/codex_reply735_connected.txt` (2026-10-14 22:39) | lu |
| 317 | `lab_exchange_2026-10-14/codex_reply738_h3.txt` (2026-10-14 22:41) | lu |
| 318 | `lab_exchange_2026-10-14/codex_reprise_785.txt` (2026-10-15 10:43) | lu |
| 319 | `lab_exchange_2026-10-14/codex_response_790.txt` (2026-10-15 11:24) | lu |
| 320 | `lab_exchange_2026-10-14/codex_response_792.txt` (2026-10-15 11:46) | lu |
| 321 | `lab_exchange_2026-10-14/codex_response_794.txt` (2026-10-15 11:54) | lu |
| 322 | `lab_exchange_2026-10-14/codex_response_795.txt` (2026-10-15 12:03) | lu |
| 323 | `lab_exchange_2026-10-14/codex_response_797.txt` (2026-10-15 12:12) | lu |
| 324 | `lab_exchange_2026-10-14/codex_response_801.txt` (2026-10-15 12:31) | lu |
| 325 | `lab_exchange_2026-10-14/codex_response_803.txt` (2026-10-15 12:42) | lu |
| 326 | `lab_exchange_2026-10-14/codex_response_805.txt` (2026-10-15 12:54) | lu |
| 327 | `lab_exchange_2026-10-14/codex_strict_upper_100.txt` (2026-10-14 23:19) | lu |
| 328 | `lab_exchange_2026-10-14/codex_upper_cuts_export_ready.txt` (2026-10-14 23:21) | lu |
| 329 | `lab_exchange_2026-10-14/codex_weight16_enumeration_733.txt` (2026-10-14 22:38) | lu |
| 330 | `lab_exchange_2026-10-14/codex_z5hm_delivery.txt` (2026-10-15 14:47) | lu |
| 331 | `lab_exchange_2026-10-14/codex_z5hm_delivery_explicit.txt` (2026-10-15 14:52) | lu |
| 332 | `lab_exchange_2026-10-14/codex_z5hm_exclusion_progress.txt` (2026-10-15 14:33) | lu |
| 333 | `lab_exchange_2026-10-14/codex_z5hm_mixed_parity_826.txt` (2026-10-15 15:04) | lu |
| 334 | `lab_exchange_2026-10-14/codex_z5hm_mod5_delivery.txt` (2026-10-15 15:15) | lu |
| 335 | `lab_exchange_2026-10-14/codex_z5hm_mod5_progress.txt` (2026-10-15 15:12) | lu |
| 336 | `lab_exchange_2026-10-14/codex_z5hm_progress.txt` (2026-10-15 14:20) | lu |
| 337 | `c1-asymmetry-audit/data/codex_line_resonance_20261016/bridge_20261018_0302.txt` (2026-10-18 03:02) | lu |
| 338 | `c1-asymmetry-audit/data/codex_line_resonance_20261016/bridge_20261018_0326.txt` (2026-10-18 03:26) | lu |
| 339 | `c1-asymmetry-audit/data/codex_line_resonance_20261016/bridge_20261018_0352.txt` (2026-10-18 03:51) | lu |
| 341 | `c1-asymmetry-audit/tmp/bridge_codex_20261017_2317.txt` (2026-10-17 23:12) | lu |
| 342 | `c1-asymmetry-audit/tmp/bridge_codex_20261017_2346.txt` (2026-10-17 23:46) | lu |
| 343 | `c1-asymmetry-audit/tmp/bridge_codex_composantes_20261017_0205.txt` (2026-10-17 02:05) | lu |
| 344 | `c1-asymmetry-audit/tmp/bridge_codex_cpu_20261017_0236.txt` (2026-10-17 02:36) | lu |
| 345 | `c1-asymmetry-audit/tmp/bridge_codex_global_minc_20261017.txt` (2026-10-17 00:28) | lu |
| 346 | `c1-asymmetry-audit/tmp/bridge_codex_no_path4_20261017.txt` (2026-10-17 01:20) | lu |
| 347 | `c1-asymmetry-audit/tmp/bridge_codex_short_vectors_20261017.txt` (2026-10-17 01:04) | lu |
| 352 | `c1-asymmetry-audit/tmp/bridge_codex_20261018_0024.txt` (2026-10-18 00:22) | lu |
| 353 | `c1-asymmetry-audit/tmp/bridge_codex_20261018_0100.txt` (2026-10-18 00:58) | lu |
| 354 | `c1-asymmetry-audit/tmp/bridge_codex_20261018_reply970.txt` (2026-10-18 01:03) | lu |
| 355 | `c1-asymmetry-audit/tmp/stage_aws_partial_paths.txt` (2026-10-18 02:12) | survolé (listing de 1060 chemins de fichiers de la campagne AWS v1 ; décompte par dossier, aucun résultat mathématique) |

### 10.2 Sous-lot B1 : journal de nuit de Codex et notes du 18/10 (index 200, 340, 349-351)

Les références « B1-NN » du texte d'origine sont remplacées par les identifiants définitifs #NNN (= 148 + NN).

### Sous-lot B1_nuit (L07) : notes de Codex dans c1-asymmetry-audit (14/10 -> 18/10)

Abreviations des sources (chemins complets, lignes = numerotation `cat -n`) :

- **J** = `C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/JOURNAL_C1_NUIT_2026_10_14.md` (index 200, 6824 lignes)
- **REP** = `C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/REPRISE_COMPOSANTES_C1_2026_10_16.txt` (index 340, 408 lignes ; le contenu date du 18/10 malgre le nom de fichier)
- **COR** = `C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt` (index 349, 79 lignes)
- **DRO** = `C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/DROITE_PETITE_ET_RACINE_2026_10_18.txt` (index 350, 87 lignes)
- **RAC** = `C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt` (index 351, 349 lignes)

Le journal J est tenu par Codex. Les heures de J et des quatre notes du 18/10 sont en heure locale de Paris (J:3 « 02h06 Paris » ; COR:1 « 11h40 Paris »), pas en UTC. J intègre de nombreux résultats de LAB (Claude) « acceptés sans re-audit ». Dans le JSONL, ils portent l'auteur « LAB (relaye) » et gardent le statut que J leur donne. Le JSONL compte 136 entrées (#149 à #284). Le parent renumérotera.

#### Chronologie

- **14/10, 02h06** : Codex démarre la nuit en « avant seulement », à partir des axiomes, sans rouvrir les anciennes notes (J:3-16).
- **14/10, 02h22-07h41** : bornes globales.
  - P <= 1151 puis 1150, et il existe T avec p(T) <= 9 (J:36-105, J:283-398).
  - Au plus 20 grilles par sommet (J:113-281).
  - Lemme P3 ; pour p(T)=12, 790 types tombent à 192 (J:399-503).
  - Vecteurs entiers -4 : la norme minimale 14 correspond au co-Heawood ; familles orthogonales de taille <= 12 ; au plus 396 co-Heawoods (J:579-1084).
  - Couches +3, noyaux, collisions et anti-voisinages (J:1086-1471).
  - Relais des résultats LAB : rang_F7(A+4I) >= 31, puis 33, puis 35 (J:826-836, 1001-1006, 1076-1084).
- **14/10, après-midi** : construction lambda=1.
  - hemi_s1 = SRG(378,52,1,8), |Aut| = 6, vérifié.
  - Obstruction de parité : pas de 3-ovoïde dans le GQ de Payne (J:1473-1510).
  - Mécanisme d'asymétrie : transport T_x, squelette K_x, théorème de majorité des flips, coupure par orbites de complétions (J:1512-1772).
- **14/10, soir et nuit** : frontières à trois étoiles.
  - Objet49 et bloc U50, témoin fractionnaire de rang 31, second Gram U (J:1774-2010).
  - Lot de 572 frontières Z5 non complétables (J:2040-2082).
  - z2b réfute « rang 30 => grille » (J:2084-2132).
  - Conjectures (A), (B), (C) ; code binaire (J:2151-2457).
  - (A) réfutée par le germe LAB (J:2616-2631).
  - Join à quatre étoiles, couplage, 100 coupes strictes (J:2633-2752).
- **15/10** : familles locales et budgets globaux.
  - Secteurs G1 ; famille c55 exclue par F7 (J:2795-3301).
  - Budgets sommables (J:2915-3068).
  - 336 drapeaux à quatre relations mixtes (J:3303-3381).
  - ODD9 en réseau (J:3456-3533) ; murs 13/14 (J:3839-3902).
  - G1'' (J:4058-4162) ; exclusion de Z5-hM (J:4308-4439).
  - Coupe stricte 48 (J:4718-4766).
  - KER-SYM réfutée (J:4841) ; ODD9 réfutée (J:4899).
  - 254 drapeaux non-grille et cible NG7 (J:5090-5243).
  - Clôture des noyaux (J:5245-5409) ; C4DO plate en supports 12 et 14 (J:5411-5621).
- **16/10** : attaque de H-MATCH, sans conclusion (J:5623-5911).
  - Reconstruction des racines et bloc HB promu (J:5913-5987).
  - Assemblage 44 -> 84 -> 99 et critère global (J:6038-6114).
  - Réparation de cœurs et DISC (J:6129-6227) ; cœur 30 exclu (J:6277-6352).
  - Défauts à cinq étoiles et cadres globaux 8/12/15 (J:6354-6646) ; bloc gris (J:6648-6689).
  - Couverture globale (J:6691-6767).
  - Équivalence globale : C1 exacts + binaire + T,U PSD <=> SRG99 (J:6770-6824).
- **18/10, 00h20-04h28** : campagne c4, branche minimum global c >= 4.
  - Registre 76/79, avec 7, 9 et 19 ouverts (REP:3-5).
  - AWS v1 côté LAB, 980 rapports (REP:207-208).
  - À 04h28, le registre est annoncé à 79/79 EXCLUDED (REP:294-300).
- **18/10, 09h34** : pilote c3, 8 gabarits et 162 couplages INF (REP:315-321).
- **18/10, 11h40-11h55** : bug OR-Tools 9.15 (domain[-1] = 0).
  - Retrait de la fermeture 79/79 (7, 9, 19 rouverts), des 162 verdicts c3 et de la campagne AWS c3star (COR:1-79 ; REP:330-348).
- **18/10, 13h09-16h36** : certificat entier 3P+4G <= 2772 et choix de racine pondérée 9s+8g <= 504.
  - Le gabarit 7 est exclu à la racine choisie.
  - Les 19 retraits de Gram ont leur DRAT.
  - Famille 9 INF ; famille 19 : 9 couplages INF.
  - Fermeture de la branche c >= 4 : « tout srg(99,14,1,2) a une droite c(L) <= 3 » (statut S) (RAC:1-349).
- **18/10, après 16h36 (pilote 16h45)** : réduction de la petite droite à huit positions ; cas 7 UNKNOWN (DRO:1-87).

#### Routes fermées (et pourquoi)

1. **Branche globale c >= 4 (toutes les droites c(L) >= 4) : fermée**, statut S. Chaîne CP-SAT et assemblage de couverture, sans certificat UNSAT portable pour l'ensemble de la branche (RAC:304-345). Elle remplace la fermeture 79/79 de 04h28, retirée (X) à cause du bug OR-Tools (COR:20-27).
2. **Hypothèses locales réfutées**, avec la version touchée :
   - « rang 30 à trois étoiles => grille désignée » : réfutée par z2b de LAB (J:2084-2090).
   - (A) « Q connexe et T/U PSD => rang 31 » : réfutée par counterexample_A_1 de LAB (J:2616-2625). (A) sans positivité est également fausse (J:2545-2552).
   - « impossibilité de toute positivité sur quatre étoiles » : fausse (J:2687-2690).
   - « hM tue toutes les relations mixtes » (message 819) : fausse hors c=(6,2)/(2,6) (J:4452-4457).
   - « une seule saturation » : fausse, il y a 4 saturations sur les 128 PSD c22 (J:4820-4821).
   - KER-SYM universelle : réfutée ; la version restreinte à nu >= 14 n'est pas touchée (J:4841-4849).
   - ODD9 universelle : réfutée, même à nu=14 (J:4899-4909).
   - SUM14 universelle : réfutée ; la version nu=14 reste ouverte (J:4914-4915).
   - Phrase de la note 100 de Codex : retirée (J:5100-5109).
3. **Familles locales exclues.** Chacune laisse C1 ouvert.
   - Sommet portant 21 grilles (J:113-275).
   - Trois co-Heawoods orthogonaux sur une arête (J:677-811).
   - 598 des 790 types p(T)=12 (J:453-459).
   - G1 c55 non grille : rang_F7 >= 29 > 28 (J:3226-3242).
   - Z5-hM : nu <= 14 et rang_F7 >= 29 à 14 (J:4321-4326).
   - G1'' cassé avec c_m >= 4, sous T >= 0 (J:4154-4160).
   - Cas double grille sous hM (J:4358-4370).
   - Les 832 cœurs plats, interdits comme sous-graphes induits (J:5521-5525).
4. **Germes ou frontières non prolongeables.**
   - Frontières 700, EX0, EX2, V0, V7, V15, plus le lot de 572 frontières Z5 (J:1934-2082).
   - z2b (J:2123-2132) ; dec81-84 (J:2258-2263).
   - counterexample_A_1 et les 51 autres (J:2627-2631, 2694-2705).
   - urep100 (J:3145-3151, 6074-6078) ; HB promu et ses 120 incidences (J:5989-6015).
   - n_45 et b_29 avec tous leurs remariages (J:5726-5780).
   - Cœurs 41, 39, 38 et 33 (J:6170-6186) ; cœur 30 par projection globale, statut S (J:6277-6293).
   - Témoin 15, bloc gris (J:6653-6662).
5. **Constructions fermées.**
   - 3-ovoïde du GQ(8,10) explicite de Payne, par parité (J:1491-1505).
   - Bords aléatoires sur hemi378 : seul le germe est reconstruit, mais avec des énumérations incomplètes, donc pas d'exclusion (J:1482-1510).
6. **Méthodes insuffisantes, démontrées comme telles.**
   - Reconstruction purement linéaire : dimension >= 1393 pour Conway (J:1662-1669).
   - Relaxation continue à trois étoiles (J:1833-1866).
   - Moyenne simple des compressions 10x10, qui ne force pas t > 0 (J:2983-2995).
   - Census d'ordre 9 relâché à P=0 : réel (J:2923-2935) et entier (J:5111-5142) ; il ne prouve pas P > 0.
   - Bornes de moments, qui ne donnent que rang T >= 23 (J:5381-5409).
   - Relaxation globale PSD, qui admet un centre fractionnaire (J:6803-6808).
   - Réseau à conductances positives pour le Schur final, indisponible (J:3510-3517).
   - LP d'extension des couches +3 : « Ne pas relancer ce même LP » (J:1130-1131).
7. **Preuve de H-MATCH.** Codex conclut : « aucune voie de preuve H-MATCH réaliste à court terme identifiée ici » (J:5805-5811). LAB déclare la route locale épuisée (J:6116-6125).

#### Questions ouvertes, classées par levier

- **Petites transversales et prismes (levier le plus direct).**
  - NG7, NG5 et N9-NG sont ouverts. Chacun exclurait Conway (J:5181-5206).
  - Il manque une borne inférieure sur P. L16/Krein ne donne que des majorants (J:5209-5212) ; le budget de second moment reste sans minorant (J:2978-2981).
  - Conjecture (P) « toute arête est dans un prisme » : P >= 231, insuffisant seul (J:5222-5224).
  - t(l) >= 8 (LAB 762) et t(l)+t(m) >= 15 sont des conjectures (J:2905-2921).
- **Symétrie locale h.**
  - H-MATCH (J:5629-5632).
  - B' reste ouverte après la réfutation d'ODD9 (J:4910).
  - (B) et (C) (J:2151-2160) ; H4' (J:2633-2637) ; conjecture (A4) de LAB (J:2690-2692).
  - SUM14 à nu=14 (J:4914-4915) ; KER-SYM restreinte à nu >= 13 ou 14 (J:4848-4849, 5000-5001).
- **Relations de noyau.**
  - C4DO générale : coefficients non plats, Bq non nul, support >= 16 (J:5609-5611).
  - SYM et QUOT de LAB (J:5530-5536).
  - Relations non négatives de poids 16 : 271 profils restent (J:2610-2614).
- **Cas c(L) <= 3 (après la fermeture de c >= 4).**
  - Huit positions, toutes nécessaires ; seul le cas 7 a été piloté, UNKNOWN (DRO:59-87).
  - Pilote c3 à recalculer après le bug (COR:20-21, 49-56).
- **Global et complétion.**
  - Modèle cinq étoiles libre : indéterminé, 18 TIMEOUT de 90 min (J:6772-6774).
  - Couverture globale à 19 types : coût non borné (J:6756-6759).
  - Exclure un point BINAIRE dans la relaxation globale PSD (J:6803-6808).
  - Recollement des 21 blocs 44 dans Gamma84 par les noyaux (J:5813-5834).
- **Certification.** Il manque des certificats UNSAT portables pour les familles c4 7, 9 et 19, et pour toute la branche (RAC:280, 342-345). Les 19 Gram ont leur DRAT (RAC:136-145).
- **Construction asymétrique.**
  - Certificat d'unicité trace(ZQ) pour les complétions du squelette Gamma6/Gamma8, non trouvé (J:1675-1681).
  - Famille p(T)=12 : 192 types (J:458-459).
  - Famille orthogonale r=12 : 96 sommets, graphe d'intersection cubique (J:909-911).

#### Contradictions, redécouvertes, résultats remplacés

- **Bug OR-Tools du 18/10.**
  - Retirés (X) : la fermeture 79/79 (REP:294-300), les 162 verdicts c3 (REP:315-321) et la campagne AWS c3star. Les records 7/9 de gram_filtered_0421 sont marqués non utilisables (COR:20-31, 68-72).
  - Sont réputés sains : les 76 fermetures (sans re-vérification indépendante, COR:25-27) et le front 909 du snapshot 0306 (COR:73-75).
  - Un défaut de même nature (indexation négative des domaines pybind) avait été détecté et corrigé dès le 16/10 dans un autre outil (J:6463-6464).
  - Aucun outil du journal des 14-16/10 n'appelle root_component_rotated_gram.py (vérifié par grep, aucune occurrence).
- **Tension apparente entre DRO:4-6 et COR:23-24.** DRO affirme que c4_selected_root_closed.json exclut c >= 4, alors que COR retire la fermeture 79/79. Les deux sont cohérents par la chronologie. La fermeture retirée est celle de 04h28. Celle que cite DRO date de 16h36 et repose sur la racine pondérée (RAC:304-336) ; elle exclut seulement à la racine choisie, la couverture arbitraire reste à 76/79 (RAC:338-340).
- **Redécouvertes plus faibles pendant la nuit « sans anciennes notes ».**
  - P <= 1151/1150 (J:36-83, 303-308) alors que le certificat antérieur codex_order9_prism_cap.json donnait déjà P <= 852.
  - Au plus 191 grilles (J:672-675) alors que codex_prism_plus_five_grids_cap.json donnait déjà rho <= 126.
  - Codex rappelle les deux certificats le 15/10 (J:2923-2925, 3311-3320).
- **Double établissement.** L'exclusion des 21 grilles par sommet est obtenue par SAT côté LAB (message 626) et par une preuve F2 indépendante côté Codex, la même nuit du 14/10 (J:119-121).
- **Census d'ordre 9.** Il existe une dérivation LAB indépendante du 08/10 (census2.py, 6533 formules, 0 désaccord). Codex corrige la phrase « aucune dérivation indépendante n'a jamais été exécutée » (REP:379-385).
- **Corrections internes à Codex.**
  - Le message 775 annonçait 126² cas ; il en faut 32 fois plus, pour les produits de signes (J:3260-3265).
  - Calcul de moments : confusion entre degré dans F et degré dans Gamma (J:5381-5384, 5514-5519).
  - Formule A+A'=7I, vraie seulement après blanchiment (J:5691-5699).
  - Gabarit 19 : 10 grilles et 11 non-grilles ; « 7 » était le minimum universel (RAC:46-48).
  - Masque H-MATCH trop large dans un helper, corrigé (J:5926-5929).
- **Correction de terminologie (722, puis 727).** Une composante singleton de Q donne un carré fermé, droit ou tordu. Sous les plafonds complets, le carré tordu est impossible et c'est une grille (J:2223-2227, 2286-2293).
- **Comptes de germes de rang 30 échouant à DISC.** J:6196 rapporte « 643 germes » selon LAB. Les notes LAB citées ailleurs (EXT84) parlent de 645 : à recouper dans le lot LAB, hors de ce sous-lot.
- **Biais des données reconnu.** Les 487 PSD G1 ont tous c >= 3 (biais signalé par LAB, J:2754-2759). La famille Z5h force la grille.

#### Matériaux pour la recombinaison

##### (1) Énoncés conditionnels « si X alors (pas de Conway / cas exclu / contradiction) »

| X (précis) | Conclusion | Statut de X / de l'implication | Source |
|---|---|---|---|
| NG7 : aucun objet quatre étoiles non-grille avec min(t_l,t_m) <= 7 ne satisfait T,U PSD, nu_T >= 14, F7, DISC (si applicable) et extension | Pas de Conway, car au moins 254 tels drapeaux sont forcés | X : O ; implication : P | J:5181-5189 |
| NG5 : non-grille et nu >= 14 => min(c_l,c_m) >= 5 | NG7, donc pas de Conway ; directement : toute droite a g >= 4, t >= 8, donc P >= 924 > 852 | O / P (vérifié par Codex) | J:5191-5201 |
| N9-NG : nu <= 9 + min(c_l,c_m) hors grille | NG5, puis pas de Conway | O / P | J:5191-5201 |
| H-MATCH : C1, C1', C2, T/U PSD et nu(T) >= 14 => M1=h(M0), M3=h(M2) | Tout sommet est un point de Hamming, contradiction avec L8 : pas de Conway (réduction LAB acceptée) | O / implication acceptée de LAB | J:3389 ; J:5629-5632 |
| H4' : aucune extension à quatre étoiles avec deux Q connexes, les deux PSD et rang T <= 30 | Tout sommet a au plus une droite non spéciale | O | J:2633-2637 |
| ODD9 (gain impair 9) | B' (toute droite spéciale) | ODD9 : R ; B' : O | J:4910 |
| Toutes les droites avec c(L) >= 4 | Contradiction ; il existe donc une droite c(L) <= 3 | S (CP-SAT) | RAC:326-336 |
| Les 8 cas (positions de L par rapport à une racine o avec s(o) <= 51, et c(L) <= 3) sont tous INFEASIBLE | Pas de Conway. Un seul cas INFEASIBLE ne suffit pas | O (cas 7 UNKNOWN) | DRO:59-67, 84-87 |
| Coupure par orbites pour C1 : le groupe L de l'instance ENTIÈRE agit librement sur les complétions asymétriques ; si le nombre total de complétions U vérifie U < \|L\| | Aucune complétion C1 | P | J:1759-1763 |
| Deux retournements individuels préservent l'instance et un certificat donne au plus 2 complétions étiquetées | Branche impossible pour TOUT SRG (\|Omega\| multiple de 4) | P | J:1743-1749 |
| Forme générale : S = {s dans L : 0 < poids < ceil(t/2)} ; dépendance impaire XOR-zéro ; majorant certifié U <= 3 | Omega vide | P | J:1751-1757 |
| Bord 44 de la famille G1 c55 non grille, T/U PSD | rang_F7(8T_S) >= 29 > 28, donc pas d'extension en Conway | P (dépend de la borne globale <= 28 de LAB L4/L23/L22) | J:3239-3242, 3280-3281 |
| Bord 44 local invariant sous <z,hM>, avec C1, C1', C2, T,U PSD | nu <= 14 ; à 14, rang_F7 >= 29 : pas d'extension | C (520 certificats) | J:4321-4329 |
| G1'' brisant H-MATCH avec c_m >= 4, sous T >= 0 | Exclu | P | J:4154-4160 |
| Espace global T8 de rang 30 de classe de discriminant différente de 2 et 14 (ou U15 de rang 40, classe différente de 1 et 7) | Pas de Conway (théorème DISC de LAB) | P (LAB, accepté sans relecture adverse) | J:6193-6197 |
| Cœur principal de rang 30 de mauvaise classe DISC | Aucune modification des sommets retirés ne donne un graphe global ; il faut baisser le rang du cœur | P | J:6199-6204 |
| Gamma84 binaire, symétrique, diagonale nulle, C1 exacts, T,U PSD | SRG99 (équivalence). Exclure Conway revient à montrer qu'aucun tel point binaire n'existe | P | J:6778-6785 ; J:6082-6101 |
| Candidat binaire C1 avec e(O u S) = 49 | T non PSD (coupe stricte <= 48) | P | J:4741-4749 |
| Relation plate de ker T (Bq=0, coefficients 0,+-1) de support <= 12 violant C4DO | Impossible ; support <= 14 => q nul sur O | P | J:5420-5426, 5548-5552 |
| Relation Tz=0, z=2q+u, avec 2, 4, 6 ou 8 coefficients impairs sur les 34 labels | Globalement exclue | P | J:2330-2340 |
| Quatre grilles restent forcées de chaque côté | min(t_l,t_m) >= 8 : la classe ne peut atteindre NG7 | P | J:5294-5296 |
| Remplacement des seules arêtes internes d'une étoile par P', avec T' PSD | P'v = -v sur W ; si les seules paires opposées sont les anciennes arêtes, P' = P | P | J:5851-5863 |
| Si c >= 4 | G >= 77, P <= 821, 81 <= G <= 126, 594 <= P <= 816, puis P >= 660 | P (vide si la fermeture c >= 4 tient) | RAC:58-69, 284-285, 298 |
| Conjecture (P) : toute arête est dans un prisme | P >= 231, insuffisant seul contre 852 | O | J:5222-5224 |
| d != 0 mod 5 dans l'un des 14 quotients de <z,hM> | Bloc - inversible et nullité <= 9 (vrai pour 7 des 14) | P | J:4497-4517 |

##### (2) Bornes quantitatives (objet, inégalité, statut, source)

- **Prismes et grilles.**
  - Prismes induits : P <= 1151 (P, J:79-83), puis P <= 1150 (P, J:303-308).
  - P <= 11088/13, donc P <= 852 (C, certificat codex_order9_prism_cap.json, J:2923-2925, DRO:12-13).
  - 3P + 4G <= 2772, avec le certificat entier sum w_H N_H = 9504(2772-3P-4G) (C, RAC:4-32).
  - Grilles : au plus 191 (P, J:672-675) ; 11rho <= 1386, donc rho <= 126 (C, J:3313-3318) ; P >= 6G (P, RAC:60-62).
  - Au plus 20 grilles par sommet (P, J:271).
- **Racines.**
  - Il existe x avec 9s(x)+8g(x) <= 504 (P, RAC:34-38) ; il existe o avec s(o) <= 51 (P, DRO:9-13).
  - Sous c >= 4 : g(x) >= 7, s(x) <= 49 ; le gabarit 7 a un score >= 528 (P, RAC:39-45).
  - Après exclusion de 9 : min(9s+8g) >= 440, 3P+4G >= 2420 (P, RAC:284-285).
- **Graphe des prismes.**
  - p(T) <= 12 pour tout T ; il existe T avec p(T) <= 9 ; sum(59p+2)^2 <= 231*590^2 ; rho(R) < 10 ; R 9-dégénéré (P, J:57-65, 283-312).
- **Co-Heawoods et vecteurs entiers -4.**
  - Au plus 396 co-Heawoods (792 vecteurs signés) ; au plus 56 par sommet, 16 par arête ; chaque C4 est dans au plus 4 co-Heawoods ; nombre de C4 = 2079 exactement (P, J:1027-1074).
  - Ancienne borne LAB : 7920 (J:1030-1031).
  - Familles orthogonales de vecteurs de norme 14 : au plus 12 (A1^r, r <= 12) (P, J:838-845). Remplace r <= 28 (J:640).
  - |f.g| dans {0,1,2,4} (P, J:919-926).
- **Vecteurs entiers +3.**
  - Paires de prismes jumeaux <= 2871, vecteurs de norme 12 <= 5742 (P, J:1133-1146). La borne LAB de 8625 paires tombe à 2871.
  - H7 <= 4158, vecteurs de norme 14 <= 8316 (P, J:1156-1167) ; norme 16 <= 278586 (P, J:1218-1248).
  - Noyaux de masse l1 <= 16 : <= 313434 (P, J:1264) ; noyaux affines : <= 911178 (P, J:1332).
- **Collisions et motifs.**
  - Collisions dans D : <= 15932268 paires, et |sqrt7 P(D)| >= |D| - 15932268 (C, J:1405-1406).
  - z signés de support 7 : >= 2057064, compte brut (P, J:1465-1468).
  - Nombre de moulins : 2079 ; nombre de maisons : 8316 ; sum delta = 6p (P, J:1460-1464).
- **Système linéaire de complétion.** Dimension réelle >= 1393 (Conway) et >= 15081 (paramètres 243) si non vide (P, J:1662-1667).
- **Automorphismes.**
  - Code des flips purs : Conway poids >= 4 et |C_x| <= 8 ; 243 poids >= 6 et |C_x| <= 8 (P, J:1708-1714).
  - |Aut(G)| <= m*h (squelette) ; groupe local BvLS dans K_x : 2^11 * 11! = 81749606400 ; hemi378 : produits égaux à 6 (E, J:1529-1543).
  - Environ 5,16 millions de complétions issues de BvLS, qui sont des renumérotations (J:1630-1632).
- **Bloc U50 et rangs.**
  - Degrés dans {6,7,8}, au plus 3 sommets de degré 8, positions <= C(40,d)C(10,j) <= 1800 ; profils 148346/31460, réduits à 94743/25926 (P/E, J:1786-1799).
  - Somme des déficits rho = 56(30-r) au rang r (P, J:1813-1815) ; budget de base 808 - 56c (P, J:2236-2238).
- **Trois étoiles.**
  - 10585 formes de rectangles ; 496 circuits ; 67730 échanges de rang 2 (P, J:1900-1901, 2185-2189).
  - rang(T_X) = 23 - c ; rang(T_S) <= 32 - c (P, J:2108-2111).
- **Codes binaires.**
  - im_F2(A), mot non nul : poids >= 8 (Conway), >= 12 (243) ; sur 34 labels >= 10 ; trois voisinages : >= 10 (Conway), >= 14 (243) (P, J:2313-2328, 2419-2434).
  - dim im_F2(A) = 54 ; poids du dual >= 8 (LAB, J:2374-2377).
- **Relations non négatives supplémentaires.** w >= 16 ; à w=16, au moins 2 paires extérieures ; 1149/1420 profils exclus (P, J:2476-2495, 2610-2614).
- **Coupes.**
  - e(O u S) <= 48 (q^tTq >= 8) ; e(S) <= 44 si O est une grille (P, J:4741-4748).
  - 586278 directions équilibrées, maximum observé 46 (E, J:4857-4882).
  - E(q) >= -31 (40 directions anti) et E(q) >= -127 (60 directions sym) (P, J:2735-2742).
- **Budgets globaux.**
  - 5 sum ||E_vlm||^2 + 928P + 48Z <= 12374208 (P, J:2977) ; 5Delta + 448P - 72Z <= 7135128 (P, J:3019).
  - Le budget ne contredirait P=Z=0 que pour une moyenne > 1190,4 (E, J:3034-3035).
- **Relations mixtes.**
  - sum m = 12474 - 45rho + 3O + 6H + Delta >= 6804 ; excès >= 567 (P, J:3335-3338).
  - Au moins 336 des 2079 drapeaux ont m >= 4 ; au moins 18 sommets en ont un (P, J:3354-3363).
- **Petites transversales.** Au moins 18 droites avec t <= 7 ; au moins 254 drapeaux non-grille portant une telle droite (P, J:5146-5177).
- **Familles locales.**
  - G1 c55 : au moins 29 des 40 sommets extérieurs brisent h ; comptes (N0,N1,N2) = (10,24,6) (P, J:3173-3203).
  - G1'' cassé : c_m <= 3 ou 4 (P, J:4154-4159).
  - <z,hM> : nu <= 14 (C, J:4321-4323) ; LAB : 339556 structures, 192 PSD, nu max 9 (S, J:4443-4447).
- **Orientations.** Moyennes à 40 cassures : au plus 4096 orientations, ou 64 si toutes les valences croisées valent 2 (P, J:3795-3803).
- **Cinq étoiles.**
  - D >= 12 et au moins 3 lignes rompues ; au plus 4 lignes invariantes (P, J:6361-6418) ; cas général k : D >= 2k-16 (P, J:6368).
  - phi : au moins 3 lignes rompues par phi, au moins 4 pour l'union (P, J:6567-6571).
- **Coupes universelles en étiquettes fixées.**
  - Signée-15 : e(P)+e(N)-e(P,N) <= 14 (P, J:6310-6315).
  - Bloc gris : somme des 58 arêtes <= 57 (P, J:6664-6667).
- **Énumérations finies (pas des bornes de coût).**
  - Au plus 2^3486 matrices (J:6756-6759).
  - 18*24^19 paramétrages c55 (J:3451).
  - 4 949 026 profils bruts par label manquant (J:2770-2779).
  - 10052 gabarits -> 106852 couplages (c3) (REP:312, 318).
  - 194336 formes ternaires, 38673438 vecteurs étiquetés (J:2397-2402).
  - 2334720 bijections dans le cas d'égalité (J:3049-3051).
  - 13824 étiquetages / 59 orbites (K4 de grilles) (REP:199-201).
  - Placements de coins <= 7!! * 4! = 2520 (RAC:121) ; couplages 1, 3, 15, 105 -> orbites 1, 2, 5, 17 (RAC:151-152).
- **Front Gram c4.** 909 Gram (449/12/448), 907 profils distincts (S, COR:73-77) ; registre de 79 gabarits dont 76 fermés (S).
- **Relaxation linéaire des 19 Gram retirés.** Minima numériques 43, 44 ou 46, contre 48 requis (E, RAC:95-100).
- **Comparaison avec la borne de symétrie forcée.** Le groupe de renommage du repère racine est S2 wr S7, d'ordre 2^7 * 7! = 645120 (DRO:18-19). Le principe de coupure par orbites dit : si le nombre de complétions U est inférieur à |L|, pas de C1 (J:1759-1763). Aucune majoration numérique du nombre de complétions d'un repère complet n'est donnée dans ce sous-lot. Les seules approches sont : le produit des tailles de domaines, « potentiellement énorme » (J:1820-1823) ; 2^3486 (J:6756-6758) ; et les modèles globaux UNKNOWN.

##### (3) Lemmes ouverts ou étapes manquantes, et ce qu'ils donneraient

- **NG7, NG5, N9-NG** : chacun donnerait « pas de Conway » (J:5181-5206). Le cas le plus dur de NG5 est c(l)=4, nu <= 13. Forme minimale : prouver rang S >= 9, 10, 11, 12 pour c_l = 1, 2, 3, 4 (J:5371-5379).
- **H-MATCH** donnerait « pas de Conway » via L8. Il manque un argument binaire, C1 ou C2 contre la saturation simultanée des contractions de T et de U (J:5806-5809). Pour un plafond 13 : contraintes sur la nullité des moyennes et la saturation du résidu (J:4044-4047).
- **Borne inférieure de P** (contre P <= 852 ou 3P+4G <= 2772) : il manque un minorant de sum ||E||^2 par les recollements (J:2980-2981), ou une majoration de ||sum u_L^(x3)||^2 dans L16/Krein (J:5209-5212).
- **B', (B), (C), H4', (A4)** : ouverts (J:2151-2160, 2633-2637, 2690-2692, 4910). H4' donnerait au plus une droite non spéciale par sommet.
- **C4DO générale, SYM, QUOT** (J:5530-5536, 5609-5611). Relations de poids 16 : 271 profils restent (J:2610-2614).
- **Cas c <= 3** : les huit positions de DRO, chacune INFEASIBLE, donneraient « pas de Conway » ; aucun coût abordable n'est démontré (DRO:64-65, 77-82). Le pilote c3 est à refaire après le bug (COR:20-21).
- **Certificats UNSAT portables** pour les familles c4 7, 9 et 19, et pour toute la branche c >= 4 (RAC:280, 342-345).
- **Global** : exclure tout point binaire de la relaxation T,U PSD (J:6803-6808) ; modèle cinq étoiles libre (J:6772-6774) ; recollement des 21 blocs (J:5813-5834).
- **Filtre de base 808-56c** : pas implémenté et non démontré contradictoire (J:2236-2238).
- **Constructions** : certificat d'unicité trace(ZQ) pour les squelettes (J:1675-1681) ; famille p(T)=12 (192 types, J:458-459) ; famille orthogonale r=12 (J:909-911).

##### (4) Méthodes transférables entre cas

- **Principe de symétrie forcée et coupure par orbites** (J:1692-1772). Il vaut pour tout SRG(1+2t^2, 2t, 1, 2), donc Conway (t=7) et les paramètres 243 (t=11). C'est le cadre de comparaison avec la borne de 99*645120 complétions.
- **Squelette K_x et transport T_x** (|Aut| <= m*h). Testé sur les huit srg(243) et hemi378 (J:1512-1545) ; réutilisable pour certifier l'asymétrie d'une construction à 99.
- **Code binaire im_F2(A) et lemme de couverture par voisinages.** Valables pour tout SRG(v,k,1,mu) avec mu pair, ou tout SRG(v,k,1,2) ; les bornes sont calculées pour 99 et pour 243 (J:2313-2328, 2419-2457).
- **Obstruction de parité par un noyau doublement pair** (3-ovoïdes) (J:1491-1505). Méthode applicable à d'autres GQ et m-ovoïdes.
- **Certificats entiers via le census d'ordre 9** (P <= 852, 3P+4G <= 2772). Le census a été dérivé deux fois, par Codex et par LAB (RAC:4-32 ; REP:379-385).
- **Rang modulo 7 (F7) et borne globale rang_F7(8T) <= 28.** Ce sont les résultats LAB du programme de rang. Ils sont transportés aux familles locales à quatre étoiles : G1 c55 (J:3226-3301) et Z5-hM (J:4402-4416).
- **Réductions cyclotomiques Z[zeta5] modulo 5 et 7** pour les familles Z5 (J:4372-4416, 4497-4609).
- **DISC (classes de discriminant)** comme coupe de réparation (Schur-DISC) (J:6193-6222).
- **Racine pondérée (minimiser 9s+8g)** pour réduire une couverture. Codex note : « Outil c4 non portable tel quel c3 » (REP:304) ; le transfert vers c <= 3 n'est donc pas immédiat.
- **Certification CP-SAT par CNF et DRAT vérifié** (19 Gram, RAC:136-145).
- **Équivalence globale T,U PSD <=> SRG99 et filtre de colonnes** (norme 20 au rang 30) (J:1809-1818, 6082-6101, 6778-6785).
- **Contrôles positifs** sur srg(9,4,1,2) (rook9), Clebsch16 et SRG9 (DRO:72-73 ; RAC:195-196, 290-292 ; J:6057-6061, 6750-6753). LAB a contrôlé son modèle cinq étoiles sur srg(243) (J:6325-6328).
- **Orbites mate-flip et réduction S2 wr S7 sans supposer d'automorphisme** (RAC:147-170 ; DRO:15-45).
- **Lemme de la grille, code parfait A1_D = 1 + 3*1_D** : vaut pour tout srg(v,k,1,2) (RAC:102-113 ; J:131-139).
- **Algèbre linéaire générale** : formule de libération du rang rank(T_CC) = r - |D| + rank(K[D,:]) (J:6136-6141) et clôture laplacienne des noyaux (J:5264-5297).

#### Couverture (sous-lot B1_nuit)

| Index | Fichier | État | Détail |
|---|---|---|---|
| 200 | J (JOURNAL_C1_NUIT_2026_10_14.md, 409703 octets) | **lu entièrement** | Lignes 1-6824, lues en 22 tranches dans l'ordre |
| 340 | REP (REPRISE_COMPOSANTES_C1_2026_10_16.txt) | **lu entièrement** | Lignes 1-408 |
| 349 | COR (CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt) | **lu entièrement** | Lignes 1-79 |
| 350 | DRO (DROITE_PETITE_ET_RACINE_2026_10_18.txt) | **lu entièrement** | Lignes 1-87 |
| 351 | RAC (RACINE_PONDEREE_2026_10_18.txt) | **lu entièrement** | Lignes 1-349 |

**Non lus**, car hors de ce sous-lot ; ils sont cités par les notes et doivent être couverts ailleurs ou signalés :

- notes/MOMENTS_SIGNATURES_C1_2026_10_16.txt (journal 25-48, où se trouvent les preuves de l'inégalité entière et des coupes E3) ;
- ARBRE_PARTIEL_C1_C2_2026_10_18.txt, RECALCUL_C4_2026_10_18.txt, RESULTAT_CMIN4_2026_10_18.txt, PILOTE_CMIN3_2026_10_18.txt, GRILLE_NEUF_FIBRES_2026_10_18.txt, MINIMUM_PRISMES_RACINE_2026_10_18.txt, AWS_7_9_19_2026_10_18.txt ;
- tous les artefacts JSON et les scripts.

Aucun calcul n'a été relancé. Les statuts sont ceux que donnent les notes, et les résultats LAB y sont repris tels que Codex les relaie.

### 10.3 Sous-lot B2 : autres notes de c1-asymmetry-audit (index 104-105, 154-163, 189-199, 348)

Correspondance : la n-ième entrée de ce sous-lot est `L07_C1_asym_local-(399 + n)` ; son champ `remarques` commence par `[B2_codexnotes n<n>]`.

### Fork B2 (lot L07) : notes du dépôt d'audit de Codex (c1-asymmetry-audit), 11-18/10/2026

Sous-lot : index 104, 105, 154-163, 189-199, 348 de `lots/L07_C1_asym_local.jsonl`. Entrées détaillées :
`B2_codexnotes_entries.jsonl` (85 entrées). Abréviations de chemins :
- `COUV` = `C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/scratchpad_LAB_2026-09-30/files/recovery_x/x_first/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_COUVERTURES_HOFFMAN_2026_10_12.md` (index 104) ;
- `DEF` = `.../recovery_x/x_last/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md` (index 105) ;
- `AG` = `C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md` (index 348) ;
- `RCA` = `C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit/`.

Les deux notes « coexistence » sont des copies récupérées : les versions courantes, plus longues, sont dans
`RCA/notes/` (544 et 3599 lignes). Un diff montre qu'aucune ligne des copies récupérées n'a été retirée ni modifiée :
ce sont des préfixes. Les sections ajoutées ensuite (COUV §10-13, DEF §63-79) sont hors sous-lot. Leur contenu V12-V15
est résumé dans `AG:1471-1541`, qui a été lu.

#### Chronologie

- **11/10** (Claude-Bureau, branche v7) : recherche par cubes α = 22 mise en pause sans verdict (8 SPLIT, 89 PENDING,
  3,00 h-solveur) `RCA/code/asym243/hoffman/cubes_alpha99/STATUS.txt:1-5`.
- **12/10 nuit** : arbre de parité S₃ arrêté sans UNSAT ; classes cls00-03 UNKNOWN à ~1185 s
  `RCA/code/asym243/s3grid/STATUS.txt:1-2`, `classes_ledger.txt:1-4`. Table des points fixes (note 174) `RCA/code/family_nesting/nesting_output.txt:1-44`.
- **12/10 matin** : audit Codex de l'unicité « bord de Hoffman de BvLS ⇒ BvLS » (note 171) : INCOMPLET, 0 orbite de
  lignes, « claim_independently_reproduced: false » `RCA/data/codex_hoffman_boundary_audit_20261012/run_status.json:1-11`.
- **12/10, 13 h 58-15 h 05 CEST** : télémétrie du modèle global co-Heawood. CP-SAT UNKNOWN à 3601 s (deux portefeuilles),
  CaDiCaL sans verdict à ~3,35 M conflits `RCA/notes/NOTE_SUIVI_SOLVEURS_2026_10_12.md:39-169`.
- **12/10, 14 h 14** : intégration du message LAB 567 (bases co-Heawood, Knuth 3e22, échelle de rang 37-43, comptes N16,
  trois supports N16 exclus au rang 37 par LAB) `RCA/notes/NOTE_INTEGRATION_LAB567_2026_10_12.md:1-87`.
- **12/10** : lemmes des onze couvertures et de multiplicité ; exclusions des familles à bord variable à 4 et 5 points
  libres du design 37c3bb63972f `COUV:9-325`.
- **12/10, suite** : loi des défauts A q = 3q + 2δ1 pour toute coclique ; lemme d'extension 21→22 ; sept profils des
  cocliques 21 maximales ; structure du profil (0,2) ; branche (1,3, E = K3) exclue `DEF:1-385`. Certificats entiers sur
  des populations, puis certificat 99 ≤ 97, onze répartitions de cycles, bords variables, obstruction (19) sans coclique,
  V5 (304 conditions), V6 (bord 61/38) et théorème de fermeture d'une factorisation binaire `DEF:387-1479`.
- **13/10** : V7, théorème affine (au plus 2^δ complétions) ; loi des grilles ; V8, fantope (critère (47) de
  srg(99,14,1,2)) ; V9-V10 (61 branches) ; campagne AWS de 255 recherches, toutes UNKNOWN ; V11 (identité d'énergie,
  fermeture entière) ; échange avec Claude (proposition du message 595 retirée en 596) `DEF:1481-2774`. V12, V13
  (complétion sans voisinage complet), V14 (rang 2 = transposition) `AG:1495-1541`.
- **14/10** : V15, bord positif de 43 sommets, au plus 8192 signes et au plus 2 complétions `AG:1471-1493`. Consignes de
  Dilan : deux chercheurs, pas de vérification croisée systématique, construire un λ = 1 asymétrique `AG:1449-1469`.
  (A) fausse (germe LAB) ; 100 coupes U strictes `AG:1425-1447`. Littérature fetchée (index 189-197) ; données Payne
  GQ(8,10) (198) et squelette à quatre racines (199).
- **14-15/10** : famille G1 (126 cas) ; census P = 0 (rationnel puis entier) ; G1 c55 non grille exclue par
  rang_F7 ≥ 29 ; budget des mixtes ≥ 336 drapeaux ; ODD9 par réseau ; compressions h-paires ; coût des cassures
  (≤ 4096 essais) ; fausse symétrie (rang D = 10 − 2c) ; G1'' (d_P ≤ 1) ; coupes PSD exactes ; projection C2 ;
  exclusion de la famille locale ⟨z, hM⟩ (520 certificats) ; filtres mod 5 et ramifié ; coupe binaire 48 ; ODD9
  universelle réfutée (acceptation des 58 exemples LAB) ; famille de 120 remariages ; (NG7) ≥ 254 blocs ; C4DO
  restreinte et support ≥ 16 `AG:729-1423`.
- **16/10** : obstructions n_45/b_29 ; critère des remariages purs ; HB promu non prolongeable ; théorème global
  T + U = 7Π ; réparation de cœurs (cœur 30 fermé) ; défaut à cinq étoiles (≥ 4 lignes cassent h) ; cadres de 12 puis
  15 lignes ; témoin 15 non prolongeable ; couverture globale (19 types pointés) ; équivalence PSD globale ; synthèse
  famille-asymétrie ; résonance ; SYM6 ; branche min c = 4 (100 → 79 gabarits) `AG:207-728`.
- **18/10** : correction OR-Tools (11 h 40) ; poids 9s + 8g et 3P + 4G ≤ 2772 ; c(L) ≥ 4 fermé par CP-SAT (16 h 36) ;
  droite c ≤ 3 ; gabarits 5128/4192 exclus par certificats entiers ; retrait LAB1076 ; 8650 et gabarit 3 ouverts ;
  gz599 fermé `AG:1-204`. Voir aussi le fork B1.

#### Routes fermées (et pourquoi)

1. **Bords de Hoffman sous actions de groupes (pré-12/10)** : les 36 exclusions antérieures sont réexpliquées par le
   lemme des onze couvertures, sans nouvelles exclusions `COUV:110-124`.
2. **Familles à bord variable du design 37c3bb63972f à 4 et 5 points libres** : exclues `COUV:126-221`, `COUV:294-309`.
   À 6 points, rien n'est terminé `COUV:222-245`.
3. **Branche (1,3) avec E = K₃** : exclue par parité `DEF:367-385`. En revanche E = P₃ reste ouvert.
4. **Budgets de triangles proposés par Claude (messages 593-596)** : redondants avec A q = 3q + 2·1. La borne de Gram des
   droites a été retirée par Claude en 596 `DEF:2727-2774`.
5. **Census d'ordre ≤ 9** : aucune borne inférieure sur P, car P = 0 survit même avec l'intégralité `AG:829-834`,
   `AG:1392-1401`.
6. **Familles locales exclues** (portée locale seulement) :
   - G1 c55 non grille, par rang_F7 ≥ 29 `AG:1337-1353` ;
   - ⟨z, hM⟩ par rang_F7 ≥ 29, 520 certificats `AG:1049-1081` ;
   - cubes cassés c_m ≥ 4 de G1'' `AG:1123-1134`.
7. **Remariages à Γ fixe pour n_45 et b_29**, et remariages purs pour urep100 et hv_h_c22_H30_23 : fermés `AG:652-706`.
8. **Témoin 15** (cadre de 15 lignes) : non prolongeable (cinq lignes) `AG:416-443`. **HB promu** : non prolongeable,
   colonne (4,6) `AG:609-615`.
9. **Pilotes globaux répétés à l'identique** (V6, V7, V10, AWS) : ne pas relancer sans renforcement. Que des UNKNOWN
   `DEF:1474-1479`, `DEF:2499-2581`.
10. **Branche c(L) ≥ 4 à la racine choisie** : fermée par CP-SAT, sans certificat portable `AG:129-145`.

#### Questions ouvertes par levier

- **Cocliques.**
  - α ≥ 21 n'est pas démontré `AG:1525-1526`. La famille (0,2) entière, les onze répartitions et les 61 branches V10
    restent ouvertes `DEF:2567-2571`.
  - La branche (1,3) avec E = P₃ est ouverte.
  - Les six autres profils de cocliques 21 maximales ne sont pas traités dans cette version.
- **Complétion de bords.**
  - Existence d'une factorisation binaire D sur le bord 61/38 `DEF:1469-1475`.
  - δ petit pour les candidats C1 ? `DEF:1545`.
  - Bornes abordables pour énumérer les bords B, D de 43 sommets `AG:1479-1480`.
- **Symétrie forcée.** Il manque « un MÊME bord inévitable » dont le groupe dépasse le nombre de complétions
  `AG:352-355`.
- **Quatre étoiles.**
  - (H-MATCH), SYM6 universel, ODD-PURE (δ0/Z ≥ 3) `AG:260-324` ;
  - borne universelle rang(F) ≥ 12 (⇔ N9-NG) `AG:326-340` ;
  - NG5/NG7 `AG:840-844` ; C4DO générale `AG:749-750` ; (P) « toute arête est dans un prisme » `AG:851`.
- **Cinq étoiles.** Existence d'une structure admissible. R8 libre UNKNOWN `AG:356`. Droite c ≤ 3 : huit positions,
  cas 7 UNKNOWN `AG:120-127`. Gabarit 3 et 8650 ouverts `AG:27-59`.

#### Contradictions, redécouvertes, résultats remplacés

- **Remplacé (X), bug OR-Tools 9.15 (18/10 11 h 40)** :
  - le pilote c ≥ 3 « 162/162 INFEASIBLE au présolve » et les anciens bilans `AG:186-204` ;
  - les verdicts sans Gram de LAB (messages 1067/1069/1071) `AG:69-76`.
  Le certificat entier c701fd6b de Codex conserve sa portée. Recoupe le fork B1.
- **Retrait (X)** de l'interprétation « aucune relation mixte » du message 819 de Codex : elle est fausse, car les
  c = (2,2) de nullité 9 ont 4 relations mixtes `AG:1034-1040`.
- **Retrait (X)** de la proposition provisoire de Claude (message 595) sur la Gram des droites `DEF:2765-2771`.
- **Retrait (X)** de la lecture « aucune combinaison ne peut exclure Conway » de la note 100 `AG:825-828`. Même retrait
  côté LAB : THREE_RESULTS §2.
- **Réfutations acceptées sans re-audit (R)** : ODD9 universelle, SUM14 universelle `AG:882-888` ; KER-SYM universelle
  `AG:915-918`. Mêmes réfutations dans MECHANISM_A E7, E12 côté LAB.
- **Redécouverte** : « une grille 3×3 est un code parfait ». Codex la dit « déjà utilisée dans les dossiers C2 »
  `DEF:1654-1658` (12-13/10) ; LAB l'établit à nouveau dans la nuit du 13-14/10 (NOTE_NIGHT F5) et le 14/10
  (NOTE_PROOFS P11).
- **Redécouverte partielle** : rang 2 et transposition. Codex V14 (13/10) prouve que toute différence de rang 2 est une
  transposition `AG:1495-1511`. LAB, le 14/10, ne traite que les vecteurs {0, ±1} et laisse les vecteurs à deux
  tailles « non classifiés » (RIGIDITY_LAMBDA1 §7).
- **À recouper** : fait des six sommets. Codex prouve e(S) ≤ 9 sur 6 sommets, avec égalité ssi prisme `DEF:144-156`.
  La borne spectrale de LAB pour s = 6 est e(S) ≤ 12 (NOTE_NIGHT 17.5) : elle est plus faible et non contradictoire.
- **Statut divergent** : G1 c55 non grille, rang_F7 ≥ 29. AGENTS.md la décrit comme une énumération exacte (E) ;
  CONWAY_CONSTRAINTS G13 la marque C ; le fork B1 la marque P.
- **Unicité BvLS depuis le bord de Hoffman (note 171)** : elle reste à un seul calcul, faute de reproduction par Codex
  `run_status.json`.
- **Comptes de germes** : LAB cite 645 germes de rang 30 ; AGENTS.md cite « 643 germes … dont urep et HB » `AG:489-491`.
  La différence correspond aux deux germes de Codex (HB, urep100) ajoutés par LAB. C'est cohérent.

#### Matériaux pour la recombinaison

##### (1) Énoncés conditionnels « si X alors … »

| X (précis) | conclusion | statut | source |
|---|---|---|---|
| UNSAT de la recherche par cubes « srg(99,14,1,2) + coclique de Hoffman fixée » | α ≤ 21 pour tout srg(99,14,1,2) (pas C1) | O (aucun verdict) | `RCA/.../cubes_alpha99/STATUS.txt:1-5` |
| Exclusion des 22 et 21 sans borne α ≥ 21 | seulement α ≤ 20 | P | `AG:1525-1526` |
| f_ij < 2 − z_ij pour une paire de blocs du bord de Hoffman | bord exclu ; si f_ij = 2 − z_ij, arête ij interdite | P | `COUV:62-69` |
| Sur-famille de couvertures < 11 membres, ou multiplicité de paire < 2 − z, pendant la construction du bord | aucune extension du bord partiel | P | `COUV:186-188` |
| Coclique 21 dont tout sommet extérieur a ≤ 4 voisins | elle se prolonge en 22 | P | `DEF:12-13`, `DEF:126-171` |
| Coclique 21 maximale | 2 ≤ e ≤ 6 sommets à 5 voisins ; profils (a,e) ∈ {(0,2),(0,3),(0,4),(0,5),(0,6),(1,2),(1,3)} | P | `DEF:173-204` |
| Grille 3×3 R et coclique 21 maximale | t = \|C∩R\| ∈ {1, 2, 3} ; t = 3 force (0,6) et C6 | P | `DEF:1660-1674` |
| Profil (0,2) | son C4 H n'est dans aucune grille ; 182 coupes (41) | P | `DEF:1676-1749` |
| W_E inversible (bord avec blocs diagonaux du défaut nuls) | G = 0 : le graphe est certifié | P | `DEF:2380-2383` |
| Une colonne entière du défaut mixte, vecteur propre de B pour 0 ou −1 | colonne nulle ; E coclique ou clique ⇒ système fermé | P | `DEF:2609-2634` |
| Bord avec voisinage complet, D binaire, ker D = 0 | complétion C1 ssi E = (DᵗD)⁻¹Dᵗ[2J − (B+I)D] est entière | P | `DEF:1340-1343` |
| δ = dim V_D = 0 (resp. 1, δ) | ≤ 1 (resp. 2, 2^δ) complétion(s) | P | `DEF:1541-1545` |
| Bord 43 positif (3I − B + J/9 > 0) | ≤ 8192 signes, ≤ 2 complétions étiquetées isomorphes ; > 2 choix ⇒ co-Heawood disjoint du bord et deux cocliques 22 | P | `AG:1474-1490` |
| Bord 44 positif | complétion unique | P | `AG:1478` |
| Bord B, D avec h = dim ker[D; 1ᵗ] ≤ 2 | unicité à isomorphisme près (étiquetée si colonnes distinctes) | P | `AG:1502-1503` |
| Moins de complétions étiquetées que \|Aut(bord)\| | aucune complétion asymétrique (exclut C1 pour ce bord si le bord est inévitable) | P (critère) / O (bord inévitable manquant) | `AG:352-355` |
| Borne universelle rang(F) ≥ 12 pour les blocs NG | contredit rang(F) ≤ 11 forcé par Conway (c_min ≤ 4) | O | `AG:326-340` |
| Conway + c_min ≤ 4 + D9 | rang Z ≤ c_min − 2 (c1 impossible, c2 Z ≠ 0, c3 rang ≥ 2, c4 rang ≥ 3) | P (conditionnel) | `AG:319-320` |
| (NG7) : aucun bloc non-grille avec min t ≤ 7 ne passe les conditions de Conway | pas de Conway (≥ 254 tels blocs forcés) | O ; implication P | `AG:835-844` |
| NG5 | NG7 | P | `AG:842-844` |
| Bornes de Schur 9, 10, 11, 12 pour c_l = 1..4 | nu ≥ 14 exclu | P (réduction) | `AG:787-790` |
| Ancien bloc grille nu14 → non-grille par interpolation PSD | perte d'au moins 1 nullité dans le segment | P | `AG:815-817` |
| Structure à cinq étoiles invariante par h | impossible ; toute structure : ≥ 4 des 8 lignes cassent h | P | `AG:529-546` |
| Tout bloc de la famille G1 c55 non grille | rang_F7 ≥ 29 > 28 : aucun prolongement Conway | E | `AG:1337-1353` |
| Tout bloc ⟨z, hM⟩ de nullité 14 | rang_F7 ≥ 29 : aucun prolongement | C | `AG:1049-1081` |
| Remplacer seulement P par P′ en gardant T PSD | P′v = −v sur W | P | `AG:652-659` |
| B_S q = 0 pour q ∈ ker T_SS (recollement de blocs) | Γ_RS q = 0 | P | `AG:670-673` |
| Γ binaire, C1 exacts, T et U PSD (84 labels) | srg(99) (tous les C2) | P | `AG:364-377` |
| A entière symétrique, A1 = 14·1, G₋(A), G₊(A) ⪰ 0 | srg(99,14,1,2) | P | `DEF:1922-1932` |

##### (2) Bornes quantitatives

- **Nombres de complétions (à comparer à 99 × 645 120)** :
  - ≤ 2 complétions étiquetées, isomorphes, pour tout bord positif de 43 sommets (≤ 8192 signes) `AG:1474-1476` ;
  - 1 pour un bord 44 positif `AG:1478` ;
  - ≤ 2^δ pour un bord (B, D) avec voisinage complet, δ ≤ h(h−1)/2 `DEF:1500-1545` ;
  - BvLS depuis son bord de Hoffman : 1 complétion selon la note 171, non reproduit par Codex `run_status.json` ;
  - témoins de contrôle : grille 3×3 (0 liberté, 1 complétion), Petersen (3, 4), Paley 25 (2, 1), Paley 49 (5, 1)
    `DEF:2001-2007` ; Paley 13 et 17 : 1 `DEF:1571`.
  Le principe correspondant est énoncé `AG:352-355`.
- **Couvertures (coclique 22)** : |F| ≥ 77, |D_i| ≥ 11 `COUV:43`. Pour une coclique quelconque, 99 − |C| couvertures
  distinctes `COUV:256-258`.
- **Défauts d'une coclique de taille c** : Σq = 18δ, Σq² = 2δ(δ+14), |supp q| ≤ 2δ(δ+14) ; à 21 : ≤ 30 sommets et ≤ 6
  exceptions ; à 20 : 64 et 14 `DEF:48-66`. Charge d'une composante propre : w < 0 ou w > 18δ `DEF:285`.
- **Densité des défauts négatifs** : e = 6 ⇒ p ≤ 7, e = 5 ⇒ p ≤ 6 `DEF:360-365`.
- **Six sommets** : ≤ 9 arêtes, égalité seulement pour le prisme `DEF:144-156`.
- **Inégalité de carrés entiers sur tout bord** : Q ≥ (2k+1)T − (99 − |B|)k(k+1), Q ≥ |T| `DEF:1022-1026`.
- **Moments résiduels** : Σ_{v≠u} R_uv + Σ_w E_uw r_w = μ(m−1) (= 74 sur le bord 61/38) `DEF:2143-2148`.
- **Profil (0,2)** : 61 branches (a + b ≤ 11, (6,6) exclu) `DEF:2331-2341` ; onze répartitions de cycles `DEF:679-683` ;
  table des triangles par charge `DEF:2744-2753`.
- **Relations mixtes** : Σ m ≥ 6804, moyenne ≥ 36/11, excès ≥ 567, ≥ 336 drapeaux avec m ≥ 4, ≥ 18 sommets
  `AG:1323-1335`.
- **Prismes et grilles** :
  - 3P + 4G ≤ 2772 (certificat entier), score 9s + 8g ≤ 504 à la racine choisie, s ≤ 49 sous c ≥ 4 `AG:175-181` ;
  - Σ_{l→x} t(l) ≤ 51 `AG:218-219` ;
  - ≥ 18 droites t ≤ 7 et ≥ 254 blocs non-grille `AG:835-839`.
- **Census** : P = 0 compatible (6435 comptes entiers) `AG:829-831` ; 5 Σ‖E‖² + 928P + 48Z ≤ 12 374 208 `AG:1395-1396` ;
  Q = 1 047 816 − 96P − 24Z + Δ `AG:1381-1382`.
- **Cassures de h** : ‖B‖²_F = b/2, q ≤ b ≤ 2q, ‖B‖²_op ≥ b/20 `AG:1248-1253`. ≤ 4096 essais par moyenne (≤ 64)
  `AG:1214-1221`.
- **Coupes** :
  - e(O ∪ S) ≤ 48, et e(S) ≤ 44 si grille `AG:941-947` ;
  - inégalité signée e(P7) + e(N8) − e(P7,N8) ≤ 14 `AG:519-520` ;
  - coupe du témoin 15 : 58 arêtes ≤ 57 `AG:425` ;
  - cinq étoiles D ≥ 12 ≥ max(0, 2k−16) `AG:533-534` ; private_Y(x) + deg_P(x) ≤ 4 `AG:552-554`.
- **Supports** : relation plate touchant O ⇒ support ≥ 16 `AG:748-749` ; C4DO pour support ≤ 12 `AG:760-762`.
- **⟨z, hM⟩** : null_Q T ≤ 14, rang_F7 ≥ 29, min c = 2, plafond local 9 sous filtre mod 5 dans 7/14 quadruplets
  `AG:1018-1025`, `AG:1049-1067`.
- **Remariages de hv_h_c22_H30_23** : 945 → 750 → 120 PSD (5!) `AG:867-872`.
- **Branche min c = 4** : 2^21 → 221 types → 367 → 200 ; 97/103 ; 100 → 87 → 79 gabarits `AG:218-250`.
- **Données co-Heawood (LAB)** :
  - 33 508 orbites de bases ; Knuth 2,3 à 3,1e22 secondes lignes par base ;
  - bloc H de rang 18 contre ≤ 16 nécessaire `NOTE_INTEGRATION_LAB567:12-21`.
- **Comptes N16** : 71 351, 30 484, 128/64/56, 6 303 880 (non cumulables) `NOTE_INTEGRATION_LAB567:58-66`.
- **Points fixes** : srg(99), p = 5 ⇒ Fix = Paley 9 avec égalité 9·10 = 90 ; exclusions de Fix pour 6273 et 494019
  `nesting_output.txt:1-37`.

##### (3) Lemmes ouverts ou étapes manquantes

- Une preuve de α ≥ 21 ferait du cadre coclique une fermeture de C1 `AG:1525-1526`.
- Un bord inévitable (forcé dans tout Conway) dont le groupe d'automorphismes dépasse le nombre de complétions :
  combiné à ≤ 2 complétions (bord 43 positif), il exclurait C1 `AG:352-355`, `AG:1474-1490`.
- Montrer que δ est petit pour les bords des candidats C1 `DEF:1545`.
- Une borne abordable sur le nombre de bords (B, D) de 43 sommets à énumérer `AG:1479-1480`.
- Une factorisation binaire D du bord 61/38, ou sa non-existence : elle fermerait (0,2) `DEF:1469-1475`.
- (KER-SYM-14), (S1), (S2), (FAKE-13) pour (H-MATCH) ; la borne universelle rang(F) ≥ 12 (N9-NG) ; SYM6 universel ;
  ODD-PURE ; NG5/NG7 ; C4DO générale `AG:260-340`, `AG:729-850`.
- Un argument binaire/C1/C2 contre la saturation simultanée des contractions T et U (H-MATCH), selon Codex
  `AG:668-675`.
- La branche (1,3) avec E = P₃ ; les six autres profils de cocliques 21 maximales.
- La reproduction indépendante de « bord de Hoffman BvLS ⇒ BvLS » (note 171 §4bis).

##### (4) Méthodes transférables d'un cas à l'autre

- **Théorème de fermeture et théorème affine** (E = E0 + 3P − 7Q, ≤ 2^δ complétions, δ équations quadratiques)
  `DEF:1318-1545` :
  - valables pour A² + A = (k−μ)I + μJ, donc pour tout srg(v,k,λ,μ) et pour toute la famille (1,2) (243, 6273, …) ;
  - étendus aux bords sans voisinage complet `AG:1513-1520`.
- **Fantope K(B,D) et critère (47)** : ils valent pour tous paramètres à racines rationnelles `DEF:1904-1905`,
  `DEF:1920`.
- **Fermeture entière des colonnes** : valable pour tout λ = μ − 1 `DEF:2629-2634`. **Plafonds collectifs** : tout srg
  `DEF:2286-2297`.
- **Inégalité de carrés entiers (19)** : tout bord, sans coclique ni automorphisme `DEF:1007-1030`.
- **Coexistence des couvertures** : elle passe de α = 22 à toute coclique `COUV:247-264`.
- **Loi des défauts** : elle passe des grilles à tout ensemble R avec A1_R = 3·1_R + b·1 `DEF:1796-1815`.
- **Rang 2 = transposition** : un analogue vaut pour tout srg ; le contre-exemple (16,6,2,2) fixe la limite
  `AG:1495-1511`.
- **Certificats** : coupes PSD exactes, projection C2, Farkas entiers et arbres de Farkas `AG:1083-1121`.
- **Filtres arithmétiques** : cyclotomie Z[ζ5] mod 5, ramification et rang mod 7 `AG:995-1081`. Ils sont analogues aux
  méthodes de corps cyclotomiques utilisées pour C2/C3 (à recouper dans L01/L04).
- **Points fixes** (note 174) : la même méthode borne Fix pour 6273 et 494019 `nesting_output.txt`.
- **Contrôles positifs systématiques sur srg(243), grille 3×3, Petersen, Paley 25** : ils servent pour tout encodeur
  `DEF:1426-1437`, `AG:13-18`.

#### Couverture (chaque index du sous-lot)

| index | fichier | traitement |
|---|---|---|
| 104 | NOTE_COEXISTENCE_COUVERTURES_HOFFMAN (copie x_first, 325 lignes) | lu entièrement ; la version courante (544 lignes, §10-13) est hors sous-lot, non lue |
| 105 | NOTE_COEXISTENCE_DEFAUTS_COCLIQUES (copie x_last, 2773 lignes) | lu entièrement ; la version courante (3599 lignes, §63-79) est hors sous-lot, mais résumée dans AG:1471-1541 (lu) |
| 154 | c1-asymmetry-audit/JOURNAL.md | comparé : contenu identique à conway99-c1:origin/main:JOURNAL.md (seules les fins de ligne CRLF diffèrent, 673 octets) ; pas d'extraction séparée (c'est l'index 0, traité ailleurs) |
| 155 | code/asym243/hoffman/cubes_alpha99/STATUS.txt | lu |
| 156 | code/asym243/s3grid/STATUS.txt | lu |
| 157 | code/asym243/s3grid/classes_ledger.txt | lu |
| 158 | code/asym243/stab_specs.txt | lu (données d'entrée, pas de résultat) |
| 159 | code/asym243/stab_specs2.txt | lu (données d'entrée, pas de résultat) |
| 160 | code/family_nesting/nesting_output.txt | lu ; identique à la copie v7 (note 174) |
| 161 | data/codex_hoffman_boundary_audit_20261012/boundary.txt | survolé : design 2-(45,5,2) à 198 blocs de BvLS, lu avec run_status.json voisin |
| 162 | notes/NOTE_INTEGRATION_LAB567_2026_10_12.md | lu |
| 163 | notes/NOTE_SUIVI_SOLVEURS_2026_10_12.md | lu |
| 189 | literature/kaski_ostergard_2004_sts19.txt | non lu (littérature tierce) : Kaski-Östergård, « The Steiner triple systems of order 19 », Math. Comp. 73 (2004) 2075-2092 ; synthèse asymétrie du 14/10 |
| 190 | literature_expansion/babai_automorphism_handbook.txt | non lu (littérature tierce) : Babai, « Automorphism groups, isomorphism, reconstruction », Handbook of Combinatorics, ch. 27 |
| 191 | literature_expansion/brouwer_ihringer_kantor_4vertex.txt | non lu (littérature tierce) : Brouwer, Ihringer, Kantor, « Strongly regular graphs satisfying the 4-vertex condition » (2021) |
| 192 | literature_expansion/brouwer_vanmaldeghem_srg.pdf | non lu (PDF du livre Brouwer-Van Maldeghem, « Strongly regular graphs ») |
| 193 | literature_expansion/brouwer_vanmaldeghem_srg.txt | non lu (texte du même livre, 1,5 Mo) |
| 194 | literature_expansion/coolsaet_degraer_spence_2006_45.txt | non lu (littérature tierce) : Coolsaet, Degraer, Spence, « The strongly regular (45,12,3,3) graphs », EJC 13 (2006) R32 |
| 195 | literature_expansion/haemers_spence_2001_64.txt | non lu (littérature tierce) : Haemers, Spence, « The pseudo-geometric graphs for generalised quadrangles of order (3,t) » |
| 196 | literature_expansion/maksimovic_rukavina_2022_twographs.txt | non lu (littérature tierce) : Maksimović, Rukavina, « New regular two-graphs on 38 and 42 vertices », Math. Commun. 27 (2022) |
| 197 | literature_expansion/spence_64_18_2_6.txt | non lu (données tierces : liste de Spence des srg(64,18,2,6)) |
| 198 | data/codex_lambda_one_construction_20261014/payne9/geometry.txt | survolé : en-tête « 891 729 », incidence droites × points du GQ(8,10) de Payne P(W(9),x0) (891 droites, 729 points) ; sert à l'obstruction de parité des 3-ovoïdes (obstruction_certificate.json voisin : rang binaire 441, noyau 288 doublement pair) |
| 199 | data/codex_night_20261014/four_root_edge_graph.txt | survolé : graphe à 39 sommets et 117 arêtes, squelette de la famille de quatre racines co-Heawood orthogonales avant exclusion (JOURNAL_C1_NUIT_2026_10_14.md:817-823, fork B1) ; dense_nine_scan : au plus 14 arêtes sur 9 sommets |
| 348 | AGENTS.md (1560 lignes) | lu entièrement |

