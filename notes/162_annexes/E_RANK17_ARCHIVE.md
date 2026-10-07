*Annexe de la note 162 : rapport d’un agent de lecture (07/10/2026), versé tel quel. Les affirmations sur les autres dépôts sont celles du rapport ; voir la note 162 pour la synthèse et les réserves.*

# Inventaire des découvertes : `conway99-rank17` et `conway99-lab-archive`

**Périmètre et contrôles effectués.** Je n'ai rien modifié dans les deux dépôts. Les scripts n'ont tourné que sur des copies placées dans mon scratchpad, sans aucun accès réseau. J'ai relancé six contrôles, tous passés :
- Les sommes `SHA256SUMS.txt` de rank17 sont toutes OK.
- `sha256sum -c` sur l'archive donne exactement 43 lignes non-OK, comme l'annonce son README (3 CNF exclus et 40 fichiers `.git` imbriqués).
- `exact_helpers.py --self-test` répond PASS.
- `sol_type02/check_anchors.py` répond PASS, et les fichiers qu'il régénère gardent le même sha256.
- Le recomptage de `rank17_char_kills_2909.json` donne 228 classes tuées (E8 5, D12p 20, E72p 30, A15p 34, D82p 65, A11E6p 74), dont 114 « partner-independent ».
- Le recomptage de `out_kstar_all.json` et `out_kstar_ladder.json` donne 492 exclues, puis 438 / 239 / 20 / 83 selon le minimum. Il reproduit aussi la couverture R6 ∧ R8 = 778/780, avec pour seules exceptions A11E6p:31 et D16p:7.

Beaucoup de résultats cités renvoient à `conway99-c1`, `conway99-involution` ou `c3-experimental`, que je n'ai pas lus. Je les signale comme « cités, non vérifiés ici ».

---

## 1. `conway99-rank17` (/home/user/conway99-rank17)

Le dépôt n'a qu'un seul commit (`97c7ee2`, 2026-10-01) ; l'historique antérieur n'y figure pas.

### 1.1 Le programme

**Objectif.** Démontrer le « Theorem C2 » : aucun srg(99,14,1,2) n'a d'automorphisme d'ordre 2 (`PROOF_OBLIGATION.md` §A). Combiné avec C3 (preuve Lean située dans un autre dépôt) et la littérature, cela donnerait « if the 99-graph exists it is asymmetric ».

**Méthode, en cinq étapes :**
1. Un handoff GPT Pro du 27/09 (`RANK17_HANDOFF.md`) introduit le « rank-17 switch ». Le repère de l'involution se plonge dans un réseau unimodulaire V de rang 17, et il n'existe que 9 tels réseaux.
2. On obtient ainsi 1 272 classes (V, y₁, y₂) à tuer, puis des moteurs d'énumération de squelettes : `z17/`, `wfe/`, plus le moteur `rank17_z4.c` de C1, cité.
3. Ce moteur se révèle insuffisant par la mesure : les estimations de Knuth vont de 10⁴ à 10¹² feuilles. On bascule alors vers des « rungs » R_n sans dépendance en V : il n'existe pas de vecteur propre σ-impair a ∈ ℤ⁴² avec Ta = −4a et |a|² = 4n.
4. Le 29/09 s'ajoutent les filtres « caractéristiques » : le théorème Astra et le paquet Sol.
5. Le 01/10 viennent deux pistes : la piste du « secteur pair » (`evenframe/`) et des essais de « re-représentation » (`paradigm/`).

Les auteurs sont des sessions d'équipe (« structures », C1, C2) et des modèles externes nommés « Sol », « Astra » et GPT Pro. Les étiquettes de statut sont PROVEN, PROVEN-ext, COMPUTED, DERIVED et PATTERN.

### 1.2 Inventaire

**A. Théorèmes structurels du handoff (27/09).**

Statut d'ensemble : « research deductions with written proofs… have not had an independent human/formal audit ». Le noyau a été re-dérivé indépendamment par « structures » et C2 (`README_TEAM.md`). Sur la nouveauté, le handoff écrit : « The rank-17 construction below was not found in the material read. This is not a claim of priority ». La simplification de la dépendance en g est attribuée à la note S27 §8 de « structures ».

| # | Énoncé | Type |
|---|---|---|
| A1 | Prop. 2.1 : « U ∩ H = 2ℤ⁷ + ℤ(1,…,1) », et le seul circuit binaire des h_c est leur somme | Théorème |
| A2 | Th. 3.1 : « U′ = U_H + A is integral and unimodular, U′ = A ⊥ V ≅ ℤ⁷ ⊥ V », V unimodulaire de rang 17, y₁, y₂ ∈ V. §3.2 : même réduction directement depuis le réseau de repère N (det 7^d), sans la classification des 156 réseaux | Théorème. Les 9 réseaux viennent de Conway–Sloane 1982, Table 6 |
| A3 | Prop. 4.1 : K = V ∩ Y^⊥ est de rang 15 et det 49 ; w_u ∈ K de norme 10 ; Σ ww^T = 28 P_W ; normes de a, b ∈ {(5,5), (3,7), (7,3)} ; 7 équations d'étoile | Théorème |
| A4 | Prop. 5.1 : ρ : E₇ → K/2K est une isométrie injective (espace quadratique de type plus, modèle K₈) | Théorème |
| A5 | Th. 6.1, inégalité PE : 7‖v‖² − Y(v) ≥ k(7−k)/2. Conséquences : Y(v) ≤ 4 pour un vecteur unité de V, et ≤ 2 si U est sans racines | Théorème |
| A6 | Cor. 6.2/6.3 : pour V = ℤ¹⁷, au plus 8 types de paires y, et 4 si U est sans racines (`z17_y_pair_representatives.json`) | Théorème, contrôlé par le self-test |
| A7 | §9 : B′ (partie 7-primaire non scindée, d pair) via la somme de Gauss caractéristique (Taylor, arXiv:2208.06319) | Preuve indépendante d'un résultat d'équipe |
| A8 | §10 : min N* ≥ 8/7, preuve complète par comptage de chemins. Elle utilise Makhnev–Minakova Th. 1 | Théorème (F4) |
| A9 | §11 : identités thêta. Le handoff dit « not an independent new modular-form obstruction » | Conséquence |
| A10 | §7–8 : apprentissage de coupes LP exactes et témoin dual court | Méthode, non implantée |
| A11 | §12 : coupes spectrales O24. 5 graines testées, « NO additional exclusion and NO evidence of a speedup » | Résultat négatif |

**B. Moteur ℤ¹⁷ et autres réseaux** (`Z17_FINDINGS.md`, `README_TEAM.md`).
- Paire 7 de ℤ¹⁷ : COMPUTED, exclue. Elle a 0 feuille en 36 s (`z17/out/pass2_p7_stageA_empty.stats`) et C1 la confirme.
- E8²⊕ℤ (12/12) et D16⁺⊕ℤ (18/18) sont fermés. Au total, 59 paires y sur 1 272 sont exclues par le moteur, dont 26 au-delà de K*. Ces 26 sont listées dans `PROOF_OBLIGATION.md`.
- Lemmes utilisés :
  - L1 à L4, dont L4 : « U = ½(Q + 4ℤ²⁴), Q a self-dual ℤ₄ code of type 4⁶2¹² ».
  - M1 et M2.
  - DC, lemme de Sol, PROVEN-ext.
  - Test Z4 exact sur 21 bits.
- Échelle (PATTERN) : la paire 1 compte ~1,6·10¹⁰ feuilles et la paire 2 ~7,2·10⁹. Verdict : « enumeration cannot close the route ».

**C. Chaîne de preuve et grand livre** (`PROOF_OBLIGATION.md`).
- Étapes F1 à F13. 492 classes sont fermées par « R≤4 : min K* ≥ 5/7 » (Sol, **PROVEN-ext**, « the text is in no repo »). 26 classes sont fermées par le moteur. **754 restent ouvertes.**
- F13 (COMPUTED) : « Every one of the 754 open classes has a K* vector with n = 6 or n = 8 ». Donc R6 ∧ R8 suffit. J'ai reproduit la version sur 780 classes : 778/780.
- Remarque k = 0 (DERIVED-here) : J0 et la cellule k = 0 de R7 sont fermés par F4.
- Cellules fermées :
  - R6/J1b, par la borne d'étoile.
  - R6/J1a, par énumération PSD exhaustive : (v) 2,74·10⁹ configurations ramenées à 0, (iii) 1,40·10⁹ ramenées à 0. Ce résultat est cité depuis c1 notes/152 ; les preuves ne sont pas dans ce dépôt.
  - **R8 k = 0, PROVEN** (`TARGETS_AB_STRUCTURES.md` §5–6, second lecteur C1).
  - « Row-capacity lemma » de C1 (motifs ±3/±4), cité.
- Restent ouverts : J2, J3, R8 k = 1, 2, 3.

**D. `TARGETS_AB_STRUCTURES.md`, en DERIVED sauf mention contraire.**
- Système d'axiomes : « (N, D) satisfying (I) + (II) ⟺ a graph with the involution ».
- Ansätze symétriques morts : S₇, A₇, L₃(2) tordu et non tordu, S₅/A₅/F₂₀, C₅/D₅. Ansätze ouverts : C₇, D₇, F₂₁, F₄₂. **Attention :** ce sont des symétries sur les 7 lignes, pas le cas C7 de Aut(Γ).
- Target B : J ∈ {8, 4, 0}.
- Vecteurs propres d'arêtes, de support 26.
- R8 k = 1 : réduit aux types T1 à T5, toujours OPEN.
- Test d'entrelacement (§9). Sur échantillons, il tue tous les 337 configurations T1 et les 536 J1a(v).
- `r8k1/r8k1.c` est un énumérateur exhaustif, écrit mais pas lancé en production. Les fichiers `count_*.txt` ne contiennent que les tailles : 123 squelettes signés, 3 794 états W–W, 7 728 ε, et 0 feuille traitée.

**E. Données de témoins.**
- `r6_data/RESULTS_28_09.md` :
  - 220 des 555 classes R6 ont un unique témoin n = 6 ;
  - aucune paire liée ;
  - 395 des 754 classes ont un triplet court (302 / 157 / 88).
- `r8k3` : 209 classes de motifs et 8 types de placement (COMPUTED).
- `n6_k3_classes.json` : 8 classes (vérifié).

**F. Test caractéristique** (`r17_char/`, 29/09, théorème Astra, redémontré par C2).
- Énoncé : « (χ,y₁)² + (χ,y₂)² ≤ 7|χ|² − 21 » pour tout χ caractéristique de V.
- Complétude due à C2 : il suffit de tester les χ de norme 1 ou 9.
- Résultat : **228 classes fermées sur les 751 ouvertes hors ℤ¹⁷.** Les 3 classes ℤ¹⁷ ne sont pas touchées, et A11E6p:100 survit.
- Il reste donc 526 classes ouvertes, réparties par 7·min Char(K*) : 21 → 76 classes, 29 → 378, plus de 33 → 69, et 25 ou 33 → 0.
- Astra fournit en plus 10 orbites de normales et 9 paires nommées, avec preuve explicite (`ASTRA_PROOF_29_09.md`).

**G. Paquet Sol « Type 0 / II »** (`sol_type02/`), PROVEN et COMPUTED.
- Parité de triangle (TP).
- Une seule classe de deux-graphe possible, la jauge « all-Opp ».
- ‖Φ‖² ≡ 5 mod 8, donc les normes 25 et 33 sont impossibles.
- Ancres :
  - Type 0 : 3 orbites (masques 17976, 22066, 85298).
  - Type II : 74 orbites (42 + 32).
  - Deux implémentations indépendantes, Python et C++.
- Lemme du chemin orienté à la norme 37.
- Ansatz N invariant par le groupe affine Paley : 0 solution, une seule implémentation.
- Le paquet le dit lui-même : « No N-matrix extension has been searched ». Les 3 classes de Type 0 coïncident avec le compte classique des 3 tournois réguliers d'ordre 7 (2 640 étiquetés). C'est cohérent, mais ce n'est pas nouveau.

**H. `wfe/`.** Moteur validé sur 129 squelettes E8:5. Arbres mesurés : environ 3·10⁵ pour une classe n = 5, contre 10⁹ à 5·10¹⁰ pour les classes de minimum 6 ou 8. Gains hypothétiques chiffrés. Mis en pause, aucune production.

**I. `evenframe/` (01/10, « work in progress, nothing closed yet »).**
- L_β est d'indice 16 dans un réseau unimodulaire de rang 15 (5 réseaux possibles).
- Lemme A : L_β n'a pas de vecteur de norme 1. Lemmes B et C.
- Classification : 1 088 représentants répartis en 31 classes. 18 meurent par le Lemme A ; la classe D8 meurt par arithmétique. Il en reste 12 vivantes ; le tableau dit « 13 sans vecteur de norme 1 » parce qu'il inclut D8.
- La classe sans racines se ramène aux ovoïdes de PG(3,2), c'est-à-dire au code de Hamming [15,11,3].
- Aucun repère invariant d'ordre 7.
- Impasse : les 42 ovoïdes A₇ ne forment pas un repère.

**J. `paradigm/` (01/10).** Dix re-représentations, presque toutes « COLLAPSED ». Une prédiction s'est révélée fausse (`gem_det`). Deux questions restent ouvertes : graphes (1,2) « courbes », et parallélisme.

**K. Prompts `GPT_*`.** Ce sont des questions et des données, sans résultat propre.

---

## 2. `conway99-lab-archive` (/home/user/conway99-lab-archive)

### 2.1 Nature et structure

C'est une archive figée le 22/09 de la session d'origine eeaf2d22 (21–22/09) sur la branche involution. Elle contient 11 593 fichiers pour 1,2 Go, et son intégrité est vérifiée.

| Dossier | Taille | Contenu |
|---|---|---|
| `repo_untracked_at_338c00e/` | 219 Mo | Notes BRIEFING et DEEP_THOUGHT, journaux LaTeX des deux rapports (les PDF n'y sont pas), `code/z2/phase2/` |
| `temp_session_eeaf2d22/` | 760 Mo | NOTE, RESEARCH_MEMORY, AUDIT ; sources primaires en PDF/TeX ; clone tiers ; `.venv` |
| `transcripts/` | 13 Mo | Transcripts de session |
| `uploads_eeaf2d22/` | 68 Ko | Dossier Deep Research et zip C3 |

**Données en vrac, qui ne certifient rien :**
- Les CNF de 29 Mo (`k14_*.cnf`, 666 183 variables et 1,51 M clauses, cas sib/one/dis) et les variantes de phase 2 (`sibQ`, `sib_seq`…, 218 Mo). Elles ne portent aucun verdict, hormis les contrôles.
- Le clone **tiers** `conway-99-research` : auteur Alireza Afshan (YesterdaysLemon), 89 commits, tous de lui. **Ce n'est pas un travail du chercheur.**

### 2.2 Programme

Rôle de « chercheur principal » (Claude) à partir d'un dossier Deep Research. Choix de la branche involution, jugée « jamais calculée » en p = 2 (la table de Behbahani commence à p = 3). Construction d'un modèle exact au niveau des orbites, puis SAT/CP-SAT et recuit. Une phase 2 en workflow a été tuée au bout d'environ 15 min, sans synthèse.

### 2.3 Inventaire

1. **Carte des symétries (CITED, vérifiée sur les sources primaires).**
   - |Aut| ∈ {1, 2, 3}.
   - « Thakkar–Severini's "Z7 case open" is a misreading » : Behbahani 2009, Thm 4.14 / Table 21, ne trouve aucune matrice d'orbites pour p = 7 ni p = 11.
   - Le dossier Deep Research se trompe sur ce point.

2. **Audit de Reimbayev arXiv:2608.19410v1** (`AUDIT_reimbayev_order7.md`, vérifié par calcul symbolique).
   - Tel qu'imprimé, Σz_i − C(99,7) = −94 034 160.
   - Il y a exactement 4 coquilles : z₂₁, z₈₀/z₈₄ (2k−7 au lieu de 2k−17), z₁₇₆ (1/84 au lieu de 1/8).
   - Une fois corrigé, le recensement coïncide avec la vague 23 du dépôt tiers et n'apporte aucune contrainte nouvelle sur n₃. C'est un erratum.

3. **Rigidité de l'involution (théorème élémentaire).**
   - σ est le retournement de chaque bloc, et u ≁ σu.
   - D est un couplage parfait sur les 42 orbites, avec a₁(t) = 14.
   - Les deux premiers points recoupent en partie Makhnev–Minakova et Ishida.

4. **Modèle exact (R)(D)(I)(P)** : 1 722 bits. Contrôles : k = 4 SAT, avec la matrice relevée vérifiée comme srg(9,4,1,2) ; k = 6 UNSAT. La session elle-même admet que l'équivalence avec l'identité srg n'est « pas rédigée dans tous ses détails ».

5. **« Théorème de rang F₂ » : rang_F₂(Γ̄ + N_bN_bᵀ) = 20.**
   - Première preuve par Broué (réseaux 2-adiques libres), remplacée par une preuve élémentaire transmise par ChatGPT (`images/1.png`), qui part de S² + S = 12I et tr S = −7.
   - Statut : deux dérivations, aucune relecture humaine.

6. **DEEP_THOUGHT.**
   - Spec(Q_out) = {12, (−2)⁶, 3²⁰, (−4)¹⁵}.
   - Pour **tout** graphe de Conway, le second sous-constituant H (84 sommets) a pour spectre {12, (−2)⁶, 0⁷, 3⁴⁰, (−4)³⁰}. La note dit « Probably known implicitly ».
   - Structure s = 1 : 10 395 couplages répartis en 11 types (`s1_structure/counts.txt`).

7. **Résultats négatifs.**
   - CP-SAT sur le quotient signé : UNKNOWN après 25 min (936 300 conflits).
   - Batterie de nuit 7 × 8 h (Kissat et CaDiCaL) : tout UNKNOWN.
   - Recuits : plateau autour de 1 550 à 1 650. La version structurée fait pire (1 890).

8. **Phase 2, jamais synthétisée.**
   - `cube_and_conquer` :
     - lignes valides de U₀ : 155 904 pour le cas « one », 22 176 pour « sib », plantage (segfault) pour « dis » ;
     - |Stab(U₀, D₀)| = 768 ;
     - **11 cubes sur 11 tirés à ligne complète (cas « one ») sont UNSAT en 2,9 à 34,3 s** avec pysat CaDiCaL, sans preuve DRAT.
   - `smoke_allsib` : UNSAT en 32,7 s, sans certificat.
   - Q-only en p = 2 : m = 2 SAT, m = 3 et m = 4 UNSAT (contrôles).
   - Correction des filtres spectraux sur BvLS, m = 11 (`sound_m11.txt`) : 0 violation.
   - Branche C3, τ = 6 : sur 156 motifs, 130 passent l'entrelacement, 44 sont PSD, et la factorisation binaire donne **26 SAT / 18 UNSAT**, recoupée par SCIP.

9. **Lemme C3 de l'hexagone.**
   - Origine tierce : ChatGPT, vérifié par la session.
   - Énoncé : si 6 orbites triangulaires forment un C₆ sans corde, l'holonomie est nulle dans F₃.
   - Généralisation : c'est une contraction de l'équation linéaire de Lundle22, et elle est « saturée par C₆ » sur les 156 motifs.
   - Ce n'est pas une exclusion de C3, et la priorité n'est pas établie.

10. **Matériel tiers archivé** (pour mémoire, non attribuable au chercheur).
    - conway-99-research : 708 ≤ n₃ ≤ 4158 ; rang_F₇(M) ≥ 27 ; Q ≥ 7059 ; couverture des extrémités 0/33 ; réfutation interne de Ishihara 2022.
    - READMEs de projets publics sur C3 : A9 fermé, f = 27 exclu, Lean t ∈ {6, 27}, critère de Lundle22, 103 types O3 ouverts chez ibenarb.

---

## 3. Tables de Brouwer, autres paramètres, autres objets

- **Aucun srg nouveau, aucune modification à proposer pour les tables de Brouwer.** (99,14,1,2) y reste « ? » ; l'archive en contient un instantané (`arxiv/brouwer51-100.html`).
- **Autres paramètres**, utilisés uniquement comme contrôles :
  - srg(9,4,1,2), soit Paley(9) ou la tour 3×3.
  - m = 3 (19,6,1,2) et m = 4 (33,8,1,2) : UNSAT. Ces paramètres sont déjà exclus par la faisabilité classique, donc on n'apprend rien.
  - srg(243,22,1,2) (BvLS), construit depuis le code de Golay ternaire, sert à contrôler des lois : T⁺ = 330, T⁻ = 660, et la correction des filtres.
- **Réseaux et codes rencontrés :**
  - les 9 réseaux unimodulaires de rang 17, et les 5 de rang 15 (classification connue) ;
  - 1 272 classes de K (rang 15, det 49), avec au moins 287 séries thêta duales distinctes parmi les 754 ouvertes (donnée citée, non vérifiée ici) ;
  - codes ℤ₄ autoduaux de type 4⁶2¹² ;
  - ovoïdes de PG(3,2) et Hamming [15,11,3] ;
  - les 31 classes de L_β.
- **Autres graphes :** recherche exhaustive de graphes de Cayley (1,2) « courbes » sur Heis(27), groupes d'ordre 243, p:3 (p de 7 à 43), A₄, A₅, L₃(2), A₆, SL(2,3)… Résultat : « Every hit is abelian and flat », la question reste ouverte.

---

## 4. Incohérences, erreurs, rétractations, sur-affirmations

**Dans rank17 :**
- **Taux de rejet Z4.** Le chiffre de 97 % (et 99,2 %) était biaisé ; l'estimation non biaisée est d'environ 23 % pour la paire 0. La correction a été ajoutée, mais les anciens chiffres subsistent dans `Z17_FINDINGS.md` (sections « Exact mod-4 test » et « Scale ») et dans le corps de `GPT_PROMPT_STAR1.md`.
- **Affirmations retirées :**
  - « without L1 ~1% » est explicitement WITHDRAWN.
  - « Purely ℤ₄ » est déclaré « not universal ».
  - L'estimation « 10⁵–10⁶ skeletons » est reconnue fausse.
- **R5, sur-affirmation probable.** `PROOF_OBLIGATION` indique que le lancement a été « stopped… no result yet ». Pourtant, `GPT_PROMPT_TYPE0_TYPE2.md` dit que R5 « would kill 274 of the 526 and is being treated as done ». Sol refuse d'ailleurs de le traiter comme une exclusion vérifiée.
- **Dépendances PROVEN-ext non archivées.** R≤4, qui porte 492 classes, la borne d'étoile, R1 à R3, DC, IB et §7.2 n'ont pas leur preuve dans le dépôt. La complétude des 1 272 classes (F8) n'a pas de certificat indépendant.
- **Exclusions du moteur.** L'élagage PSD est fait en virgule flottante, et la repasse exacte en LDLᵀ prévue pour la PASS 2 n'est documentée nulle part comme faite.
- **Non reproductible depuis le dépôt seul.** Les scripts `verify.py`, `audit_models.py` et `certificates.json` d'Astra sont cités mais absents. `r17_char_scan.py` dépend de chemins Windows pointant vers c1 et c2.
- **Horodatage incohérent.** Dans `PROOF_OBLIGATION`, les blocs STATUS sont désordonnés : il y a deux « 17:30 », et un bloc « late night » où J1a est encore ouvert précède celui où J1a est fermé. Le document reconnaît lui-même une « bookkeeping drift » : J0 et R7 k = 0 y figurent encore comme ouverts.
- **`evenframe`.** Une liste a été corrigée le 01/10 au soir : les points 4 à 6 sont superseded. Les versions ultérieures du solveur n'ont pas été re-validées, avec 2 erreurs de solveur. Les comptes du README (130/143, 85/102) ne se recoupent pas avec les logs. Une prédiction de `paradigm` était fausse.

**Dans l'archive :**
- **Contradiction interne non résolue.** Les notes affirment « row-fixed… CaDiCaL ≥ 30 min undecided ⇒ exhaustive first-row split out of reach » (NOTE §4, MEMORY, BRIEFING). Les cubes de phase 2 montrent au contraire 11 lignes complètes réfutées chacune en 35 s au plus.
  - Si cela se confirme, un découpage cube-and-conquer par ligne de U₀ pourrait être faisable : ~1,6·10⁵ lignes pour « one », réductibles par le stabilisateur.
  - Rien de tout cela n'est certifié, et le cas « dis » plante.
- **Rang F₂ présenté comme nouveau.** Il est qualifié de « nouvelle condition nécessaire… non déductible ». Or il découle de S² + S = 12I et tr S = −7, qui font déjà partie du modèle exact. Il ne contraint donc rien de plus qu'une recherche exacte. DEEP_THOUGHT conclut d'ailleurs qu'il n'apporte aucune information spectrale nouvelle, et rank17 ne l'utilise pas.
- **Nouveauté non établie.** « Jamais calculée par personne » repose sur une recherche bibliographique bornée.

**Ce qui a été dépassé ou corroboré par la suite :**
- La voie SAT générique a été abandonnée. rank17 déclare que les UNKNOWN « carry no information », et une règle d'équipe interdit tout solveur LP/SAT/ILP/CP.
- Le modèle de l'archive a été réutilisé : `n6_k3.py` importe `orbit_sat.build`.
- Le découpage sib/one/dis est devenu la « D-structure partition ».
- Le résultat non certifié `smoke_allsib` est corroboré par « all-sib dead (C2 Th. D) », cité.
- **Aucun énoncé démontré de l'archive n'est contredit par rank17.**

---

## 5. Éléments publiables, classés

1. **Le paquet « réduction rank-17 du cas involution ».** Il regroupe A1 à A8, le théorème caractéristique d'Astra, les résultats de parité de Sol (TP, 5 mod 8, ancres), et le grand livre : 492 + 26 + 228 classes fermées, 526 ouvertes. C'est l'élément le plus fort, mais il faut d'abord :
   - archiver et faire relire les preuves PROVEN-ext ;
   - certifier la complétude des 1 272 classes ;
   - refaire les exclusions en arithmétique exacte ;
   - obtenir un audit humain.
2. **Erratum Reimbayev** (4 coquilles). Prêt et très fiable, mais d'une valeur modeste : une note à l'auteur.
3. **Lemmes autonomes**, à publier au sein du point 1 plutôt que seuls : min N* ≥ 8/7 (§10), R8 k = 0, et le théorème caractéristique, court et élégant.
4. **Note bibliographique** : |Aut| ∈ {1, 2, 3}, Z7 clos depuis Behbahani 2009. Modeste.
5. **Question ouverte des graphes (1,2) « courbes »**, avec les données Cayley. Note de problème.
6. **Branche C3 à τ = 6** : recensement 26/18 et lemme de l'hexagone. La paternité est tierce (ChatGPT), le recoupement avec Lundle22 est probable, et la nouveauté est incertaine.
7. **Non publiables en l'état :**
   - le rang F₂, qui est une conséquence du modèle ;
   - Spec(H), probablement connu ;
   - `evenframe`, travail en cours ;
   - les campagnes SAT et les estimations de Knuth, utilisables seulement en annexe méthodologique.

**À noter :** le seul « résultat » susceptible de changer la donne n'est pas encore un résultat. Il s'agit de la piste cube-and-conquer par ligne, enfouie dans `/home/user/conway99-lab-archive/repo_untracked_at_338c00e/code/z2/phase2/cube_and_conquer/`. Elle mérite une vérification avant toute décision.

**Fichiers principaux** (sous `/home/user/conway99-rank17/`, sauf la dernière ligne) :
- `RANK17_HANDOFF.md`, `PROOF_OBLIGATION.md`, `TARGETS_AB_STRUCTURES.md`, `Z17_FINDINGS.md`
- `r17_char/ASTRA_PROOF_29_09.md`, `sol_type02/PROOF.md`
- `evenframe/README.md`, `paradigm/PARADIGM_BREAK.md`
- Dans `/home/user/conway99-lab-archive/temp_session_eeaf2d22/scratchpad/` : `NOTE_involution_case.md` et `AUDIT_reimbayev_order7.md`