# Matériaux pour la recombinaison : extraits bruts des fiches (copie verbatim)

Chaque bloc renvoie à fiches/<lot>.md:<lignes>. Les statuts et sources sont ceux des fiches.



<!-- ===== L01_origines_C2.md:798-1011 ===== -->

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



<!-- ===== L02_C2_aws.md:1689-2276 ===== -->

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


<!-- ===== L03a_session_eeaf2d22.md:455-616 ===== -->

## 8. Matériaux pour la recombinaison

Convention : « ext » désigne le dépôt externe. Ses résultats ne supposent **aucun** automorphisme, sauf mention : ils valent donc pour C1.
« Extrémité 4158 » signifie n3 = 4158, c'est-à-dire P = 0. « Rang 11 » désigne l'extrémité centrée ternaire de rang 11 (W175 et suivantes).

### 8.1 Énoncés conditionnels « si X, alors exclusion ou contradiction »

| # | si X | alors | statut de l'implication / de X | source |
|---|---|---|---|---|
| C-01 | Γ a une involution t | Fix(t)={x} ; t = σ (flip de chaque bloc) ; u ≁ σu ; a1(t)=14 ; D couplage parfait sur 42 orbites | P / X ouvert | NI L17-L26 |
| C-02 | Γ a une involution | rang_F2(Γ̄ + NbNbᵀ) = 20 et Γ̄²+Γ̄ = NbNbᵀ sur F2 | P (IA ×2) / X ouvert | NI L36-L45 |
| C-03 | Γ a une involution | S²+S=12I, spec 3^27,(−4)^22 ; S_out spec 0^7∪3^20∪(−4)^15 ; (S_out+4I−CCᵀ/3)/7 projecteur de rang 20 | P | NI L31-L34 |
| C-04 | Γ a une involution | mod 7 : S_out−3I nilpotent d'indice 2 sur dim 35 ; rang_F7(S−3I) ≤ 22 (aucune contradiction trouvée avec rang_F7(M) ≥ 27) | P | RM L38-L39 |
| C-05 | le modèle orbitaire (R)(D)(I)(P) est UNSAT (certifié) | aucune involution ⇒ \|Aut\| ∈ {1,3} | P / X ouvert | NI L58-L64 |
| C-06 | g d'ordre 3 sans point fixe et les 6 orbites triangulaires forment exactement C6 sans corde | holonomie ε0+…+ε5 = 0 dans F3 (h=1,2 impossibles) | P (vérifié Claude) / moot (C3 exclu, L04-01) | HEX L7-L17 |
| C-07 | g d'ordre 3 sans point fixe avec 6 orbites triangulaires de motif F | K^T(E−FE−EF)K = 0 sur F3 (non trivial seulement pour F=C6) | C / moot | SUI L84-L88, L166-L182 |
| C-08 | p premier divise \|Aut\| | p ∈ {2,3} (Behbahani–Lam) ; Fix(g) selon Makhnev–Minakova Thm 1 | E (calcul publié) | LIT `behbahani_thesis.txt` L2235-L2237 |
| C-09 | 2 \| \|Aut\| | \|Aut\| \| 6 (Cesarz–Woldar) ; et involution ⇒ \|G\| \| 42 ou \|G\| \| 6 (Makhnev–Minakova Cor. 1) | P (publié) | LIT `cesarz_woldar.txt` L68 ; `makhnev_minakova_2004.txt` L53-L56 |
| C-10 | 7 \| \|Aut\| | G ≅ Z7 (Cesarz–Woldar) ; et 0 matrice d'orbites pour p=7 (Behbahani) | P / E | LIT `cesarz_woldar.txt` L69 ; `behbahani_thesis.txt` L3110-L3124 |
| C-11 | ext : un automorphisme d'ordre 11 existe | il est sans point fixe, puis contradiction par la recherche de quotients 9×9 (0 quotient) | C | AR L416-L433 |
| C-12 | ext : Γ sommet-transitif, ou de Cayley sur un groupe d'ordre 99 | contradiction | C | RD L187-L194 ; AR L427-L429 |
| C-13 | ext : n3 = 705 | contradiction (donc n3 ≥ 708) | P (VER) | RD L1290-L1335 |
| C-14 | ext : n3 = 705 | h ∈ {1,9} ; q(T) ≤ 8 ; tr(A4²) ≥ 26460 ; et h ≥ 21 ⇒ n3 ≠ 705 | P (historique) | RD L1244-L1263 ; AG `2026-07-23-wave21-lattice-extension.md` L70 |
| C-15 | ext : n3 = 708 | det(B) ≤ 6525 ; h ∈ {9,21,49,81,189,441,729,1029} ; tr(C²) ≥ 10 ; tr(B²) ≥ 116 ; q(T) ≤ 11, au plus un q(T) = 11 | P (VER) | RD L1363-L1429 |
| C-16 | ext : n3 = 708 et forme scaled-dual = somme orthogonale d'ADE irréductibles | contradiction | P (VER) | RD L1549-L1555 |
| C-17 | ext : n3 = 708 et sommande orthogonale A2, E6 ou A6 | contradiction (21 > 18 ; énergies cubiques 24 et 66 > 60) | P (VER) | RD L1439-L1529 |
| C-18 | ext : n3 = 708, forme sans racine, décomposition intégrale non triviale, incidence réelle | contradiction (231 \| b avec 0 < b < 231) | P (VER) | RD L1795-L1855 |
| C-19 | ext : n3 = 708 et vecteur de norme 2 (branche avec racine) | k ∈ {0,±1}^99, Ak = −4k, support complément de Fano ; extension ⇔ 6 équations de blocs (14+70+15) | P (VER) | RD L1912-L1948, L2018-L2061 |
| C-20 | ext : n3 = 708 sans racine | endpoint indécomposable et tr(A−1 A−2²) = 0 (motif {−2,−2,−1} interdit) | P (VER) | RD L1957-L1974 |
| C-21 | ext : la forme S0 = K12 ⊕ Λ(F) porte le paquet complet à 708 | contradiction (det(B_K) ≤ 729 < 3645) | P (VER) | RD L1650-L1697 |
| C-22 | ext : extrémité 4158 et 45 indices de triangles de degré de support signé interne ≤ 3 (somme des \|S_ij\|) | contradiction (exclusion de l'extrémité) | P (VER) / X non trouvé | RD L2296-L2302 |
| C-23 | ext : extrémité 4158 | rang_F7(M) ≥ 28 ; r3 ≥ 12 ; r7 ≥ 11 ; r3 + r7 pair ; à r3 = 12 la classe de déterminant non carrée est exclue | P (VER) | RD L2352-L2365, L3015 |
| C-24 | ext : rang_F7(M) = 27 | Γ contient un prisme triangulaire induit, donc n3 ≤ 4155 | P (VER) | RD L3018-L3021 |
| C-25 | ext : extrémité 4158 et r7 ≤ 20 / ≤ 22 / ≤ 24 | toutes les arêtes de type 2+2+2 / types 2+2+2 ou 2+4 / aucune arête de type 3+3 | P (VER) | RD L2653-L2657 |
| C-26 | ext : extrémité 4158 et r3 = 12 | r7 pair ≥ 26 (W40), puis ≥ 28 (W42) | P (VER) | RD L2759-L2760, L2952-L2955 |
| C-27 | ext : extrémité 4158, r3 = 12 et toutes arêtes de type 222 | tout bloc de triangle de base de rang ≥ 33 ; r7 pair ≥ 34 | P (VER) | RD L2869-L2876 |
| C-28 | ext : extrémité 4158, r3 = 12, toutes 222, masque 51739 | incidence extérieure = triple appariement exact (45 032 six-ensembles) ; graphe extérieur 96/144/0 arêtes, 32 triangles, 181 4-cycles | P (VER) | RD L2960-L2969 |
| C-29 | ext : extrémité 4158 | toute non-arête percole ; R = 18H, 6H ≤ P, R ≤ 3P, S ≥ n3 | P (VER) | RD L3388-L3398 |
| C-30 | ext : extrémité 4158 | aucun mot dual de poids 3 : d(W⊥) ≥ 4 (pas trois colonnes colinéaires) | P (VER) | RD L476-L486 |
| C-31 | ext : il existe un plafond universel de 25 paires antipodales de supports de norme 14/16/18 par 4-cycle induit | la ligne de rang r_ext = 28 est exclue | réduction VER / X ouvert | AR L589-L591 ; RD L254-L257 |
| C-32 | ext : plafond universel de 24 paires jusqu'à la norme 20 | la ligne r_ext = 30 est exclue | réduction VER / X ouvert | AR L598-L599 ; RD L259-L260 |
| C-33 | ext : borne supérieure de Jacobi 51 975 (alors que le rang 28 force ≥ 52 812) | la ligne r_ext = 28 est exclue | réduction VER / X ouvert | AR L630-L631 ; RD L261-L264 |
| C-34 | ext : N_Wagner ≥ 18710 | l'extrémité 4158 est exclue (via N_Wagner ≤ 3N_cube + 9355 et N_cube ≤ 3118) | P / X ouvert | RD L411-L414 |
| C-35 | ext : défaut global E ≤ 8, où E = 8(18711 − N_Wagner) | l'extrémité 4158 est exclue (elle exigerait E ≥ 16) | P / X ouvert | RD L427-L429 ; AR L843-L846 |
| C-36 | ext : au plus 4 marques Wagner en échec par non-arête (« lemme des quatre échecs ») | l'extrémité 4158 est exclue | P / X UNPROVED | AR L834-L838 |
| C-37 | ext : égalité dans la borne non-arête de W180 (rang 11) | les 2 079 quadrilatères canoniques sont des coniques ; rang_F3(R_square) ≤ 220 ; RᵀR = 36I − 4K + L | P (VER) ; face fermée par W186 | RD L557-L570 |
| C-38 | ext : Q = 2079 (rang 11) | contradiction (9Q ≥ 8·4158) | P (VER) | RD L605-L614 |
| C-39 | ext : rang 11 et une paire inversée appariée | relation tout-égale interdite sur le quadrilatère canonique ⇒ multiplicité combinée ≤ 5, ε ≥ 5b | P (DERIVED, audit) | RD L679-L685 |
| C-40 | ext : un graphe a un ensemble indépendant de taille 22 | design simple 2-(22,4,2), NNᵀ = 12I + 2J, ND = −N + 2J, X² = 28X | P (VER) | ST L3517-L3530 |
| C-41 | ext : sous-graphe induit à m sommets de degré minimum 6 | m ≥ 27 (via 2e(X) ≤ 3m + m²/9) | P (VER) | RD L978-L986 |
| C-42 | ext : P = 3 (trois prismes) | O ≥ 4 (défaut impair de parité enracinée) | P (VER) | AR L560 |
| C-43 | ext : rang r_ext = 28 (q = 16) | vecteur propre −4 entier de norme 14, 16 ou 18 ; N14 + N16 + N18 ≡ 2 mod 14 et ≥ 5868 ; supports 7+7, 8+8, 9+9 ; norme 18, h = 2 exclue ; d ≤ 2 (16), d ≤ 3 (18) | P (VER) | AR L435-L453, L482-L495 |
| C-44 | ext : rang 28 et extrémité 4158 | 407·N16 + 43·N18 ≥ 2165002 | P (VER) | AR L505-L507 |
| C-45 | ext : motif C4 □ K3 présent | graphe extérieur à 87 sommets : 549 arêtes, 167 triangles, 1 356 4-cycles, connexe, nullité 4, facteur x² − 9x − 46 ; réseau O^-(74,7) | P (VER) | AR L567-L619 |
| C-46 | ext : n3 = 4158 et partition locale à un triangle | composantes [12], [4,8], [6,6], [4,4,4] seules ; H connexe à 32 triangles, C4(H) = 171 + C4(A_X) | P (VER) | RD L2389-L2397 |
| C-47 | ext : rang 11, étoiles adjacentes | h_xy = 1 ⇔ type 4+2 ; 0 pour 6, 3+3, 2+2+2 | P (VER) | ST L4196-L4206 |
| C-48 | Ishihara 2022 : « Théorème 28 » | non-existence annoncée, mais l'étape (88) est réfutée (degrés 1^20, 2^51, compte 122 au lieu de 142) | R (étape) | RD L723-L728 |
| C-49 | ext : on prouve rang_F7(M) ≥ 45, ou, avec W66, r_ext ≥ 43 | contradiction avec le rang rationnel 44, ou avec W66 r ≤ 42 : pas de Conway-99 (en notation équipe : r_équipe ≥ 44, si L03a-103 tient) | P (les deux faits) / X ouvert | AT `wave39-edge-local-rank/failed-routes.md` L13-L15 ; AR L410-L411 |
| C-50 | ext : les 33 cas raffinés de l'extrémité sont tous UNSAT, avec preuves vérifiées | n3 = 4158 exclu, donc n3 ≤ 4155 | P (couverture VER) / X : 0/33 | AT `wave41-proof-producing-search/README.md` L113 ; AR L317-L339 |
| C-51 | ext : on prouve que le domaine d'extension du critère 14+70+15 est vide | la branche avec racine de n3 = 708 est exclue | P / X ouvert | AT `wave33-rooted-construction/correction-ledger.md` L15 |
| C-52 | ext : toute complétion simultanée (B,H) à l'extrémité force un triangle de base T avec rang_F3(P_T − I) ≥ 12 | amélioration du rang ternaire. La version à un seul triangle est RÉFUTÉE par un contrôle de rang 10 | O (lemme manquant) | AT `wave38-higher-order/failed-routes.md` L32-L80 |
| C-53 | ext : le graphe d'incompatibilité des marques Wagner a un nombre d'indépendance ≤ 4 | un certificat de Hoffman ou de couverture par cliques prouverait la cible ponctuelle f(uv) = 4 | R : un gadget à 5 échecs le réfute | AT `wave169-failure-hypergraph/README.md` L30 |
| C-54 | ext : face d'égalité uniforme des non-arêtes (W205) | rang de span des 99 projecteurs 54 ≤ r ≤ 59, noyau ≥ 40, donc au moins 7 relations globales de projecteurs en plus : une cible, pas une contradiction | P (DERIVED) | AT `wave205-global-fourth-moment-proof-b/derivation.md` L304-L316 |

### 8.2 Bornes et valeurs quantitatives

| # | objet | inégalité / valeur | portée | statut | source |
|---|---|---|---|---|---|
| B-01 | \|Aut(Γ)\| | ∈ {1,2,3} ; divise 2·3³·7·11 (MM) ; 2·3³·7 (avec Wilbrink) | général | E/P (littérature) | NI L4-L14 ; LIT `makhnev_lecture.txt` L207-L210 |
| B-02 | orbites du cas involution | 42 orbites extérieures, 7 blocs, 50 orbites ordinaires, base signée de 49 | involution | P | NI L18-L34 |
| B-03 | modèle orbitaire k=14 | 1 722 bits primaires ; 666 183 vars CNF ; 1,51 M clauses ; \|Stab(U0)\| = 15 360 ; groupe de labels 645 120 ; stabilisateur 46 080 (deep thought) | involution | E | NI L48-L52 ; TR L2427 |
| B-04 | spectre S_out | 0^7, 3^20, (−4)^15 ; rang du projecteur 20 | involution | P | NI L34 |
| B-05 | rang F2 | rang_F2(S mod 2) = 27 ; rang_F2(Γ̄ + NbNbᵀ) = 20 (variante : rang_F2([[0,Nbᵀ],[Nb,I+Γ̄]]) = 22) | involution | P | NI L40-L43 ; TR L1134 |
| B-06 | mod 7 | rang_F7(S − 3I) ≤ 22 ; nilpotent d'indice 2 sur dim 35 | involution | P | RM L38-L39 |
| B-07 | découpage de la 1re ligne | ~10^4–10^5 cas (hors de portée) | involution | H | NI L54-L55 |
| B-08 | solveurs | CP-SAT S : 25 min, 936 300 conflits, 34,7 M branchements ; SAT H : 886 200 vars, 2,1 M clauses ; ligne fixée : 907 s, 2 477 conflits, 400 327 branchements ; nuit : 7 × 8 h | involution | O | TR L896, L1230, L2343 |
| B-09 | recuit | plateau E = 1 550 = (14, 16, 270, 1 250) ; structuré ≥ 1 890 ; bit-flip 1 656 à 10 min | involution | H | TR L1817, L2213 |
| B-10 | comptes s1 | 10 395 appariements, 11 types ; 35 560 triangles s=0 ; 1 270 par label ; 2 562 paires disjointes ; 17 780 σ-orbites ; 6 720 à 6 blocs ; 9,99 % de violations ; 280 / 11³ = 0,2104 | involution | E | PH2 `counts.txt` L1-L22 |
| B-11 | soundness m=11 | rangs finaux Ps 44, Pr 55, Es 55, Er 66 ; 0 violation | srg(243,22,1,2) | E | PH2 `sound_m11.txt` L111 |
| B-12 | Reimbayev ordre 7 | Σz − C(n,7) = −94 034 160 (imprimé) ; corrigé : 0 ≤ n3 ≤ 4158, 2n3 ≤ z11 ≤ 4n3, 4 \| z11 ; 353 valeurs de z11 (1412…2820) à n3 = 705 | général | E | AU L17-L36 |
| B-13 | C3, hexagone | 1 366 configurations, 352 après noyaux ; résidus 0, 2, 1 pour h = 0, 1, 2 | C3 | C | HEX L124 |
| B-14 | C3, motifs | 156 graphes : 87 entrée négative / 25 non PSD / 44 PSD ; nullités 0 : 29, 1 : 13, 2 : 2 ; 32 768 graphes étiquetés ; 243 identités | C3 | C | SUI L159-L178, L193-L202 |
| B-15 | C3, exploration | 26 témoins, 87 négatifs, 43 MILP non certifiés ; 318 phases : 123 / 191 / 2 / 2 | C3 | H | HEX L140-L142 |
| B-16 | T–S | 379 987 booléens, 761 221 contraintes ; circulants C(49,7) = 85 900 584, ≤ 33 classes (68 %) ; 3501/4950 = 70,73 % (549/693 λ, 2853/4158 μ) | général | S/H | DR L199-L207 ; LIT `ts/caisc_2026.tex` L346 |
| B-17 | ext : n3 | 708 ≤ n3 ≤ 4158 ; n3 ≡ 0 mod 3 ; C6 induits = 209 286 + n3 ≥ 209 994 | général | P (VER) | RD L33-L34 ; ST L37-L56 |
| B-18 | ext : prismes | n3 + 3P = 4158 | général | P (VER) | RD L2261-L2266 |
| B-19 | ext : sous-graphes induits | 2e(X) ≤ 3m + m²/9 | général | P (VER) | RD L978-L983 |
| B-20 | ext : Schur | tr(A4) = 84(n3 − 693) ; diag(A4) multiples positifs de 4 | général | P (VER) | RD L1177-L1186 |
| B-21 | ext : h11 | h11 ≡ 0 mod 4 ; ceil4(2n3) ≤ h11 ≤ 4n3 | général | C | RD L1222-L1225 |
| B-22 | ext : α, χ | α ≤ 22 ; χ ≥ 5 ; 13-coclique existe toujours | général | P (VER) | ST L18-L20 ; RD L2559-L2575 |
| B-23 | ext : 4-cycles | 2 079 au total ; 84 par sommet ; 1 071 résiduels (51 par sommet) | général | P | ST L15-L16, L3413-L3416 |
| B-24 | ext : rangs de A | rang_F2(A) = 54 ; rang_F3(A) = 45 ; SNF(A) = diag(1^45, 3^9, 6, 12^43, 84) ; Δ77(B) = 2^49·3^34 ; codes F2 de poids min ≥ 8 | général | P (VER) | ST L3552-L3580 |
| B-25 | ext : rang_F7(M) = r_ext | ≥ 27 (général) ; ≥ 28 (extrémité) ; ∈ {28,30,…,42} (général, W66) | général / extrémité | C/P (VER) | RD L2918-L2956, L3015 ; AR L410-L411 |
| B-26 | ext : rang local | rang_F7((NMNᵀ)[L,L]) = 25 − 2e ; bloc 39 de rang ≥ 27 ; rangs locaux 19, 21, 25, 23 à l'extrémité | général | P (VER) | RD L2631-L2656, L2948 |
| B-27 | ext : recensement de paires (r3,r7) à l'extrémité | 629 → 528 → 429 → 330 → 314 → 297 → 281 | extrémité | P (VER) | RD L99-L141, L3022 |
| B-28 | ext : N14 | ≤ 2·floor((55440 − 5n3)/14) ; ≤ floor((55440 − 4n3)/7) ; 7N14 ≤ 55440 − 5n3 − O/2 ; ≤ 5544 puis ≤ 4950 à P = 0 | général / extrémité | P (VER) | AR L497-L513, L558 |
| B-29 | ext : N14+N16+N18 | ≥ 5868 et ≡ 2 mod 14 | rang 28 | P (VER) | AR L439-L441, L486-L487 |
| B-30 | ext : N16, N18 | 407N16 + 43N18 ≥ 2165002 ; aucune borne supérieure connue | rang 28, P = 0 | P (VER) | AR L505-L513 |
| B-31 | ext : coquille totale jusqu'à la norme 28 | ≥ 182, 1584, 11400, 80110, 561084, 189901474, 1831606638 (7 lignes) | par ligne de rang | C | AR L541-L543 |
| B-32 | ext : cycles et supports | 2 079 4-cycles ; supports norme 14/16/18 ≥ 21, 20, 18, 26 cycles alternés ; ≥ 52 extensions orientées (26 paires) au rang 28 ; norme 20 : ±1 ×10, ≤ 3 arêtes de même signe, ≥ 15 4-cycles | rang 28 / 30 | P (VER) | AR L585-L599 |
| B-33 | ext : Jacobi | det(G_K) = 1 023 942 465 ; G_K = 7G_L ; ≥ 52 812 incidences (rang 28) | rang 28 | P (VER) | AR L627-L631 |
| B-34 | ext : cubes, Wagner | 12N_cube ≤ 41580 − n3 ⇒ N_cube ≤ 3465 (≤ 3118 à P = 0) ; N_Wagner ≤ 3N_cube + 9355 ; 4N_Wagner ≤ 41580 − n3 + 12N_cube ; F = 166320 − 8N_Wagner ; 40 C5 marqués par non-arête (36 cœur + 4 frange) | général / extrémité | P (VER) | RD L383-L431 |
| B-35 | ext : endpoint 708 | det(B) ≤ 6525 (max unique (h, det Q) = (9, 725)) ; det(B) < 6561 ; tr(B²) ≥ 116 ; tr(C²) ≥ 10 ; tr(E6Q) ≥ 14 ; énergies cubiques E6 ≥ 24, A6 ≥ 66 ; tr(A20 Q_AA) ≥ 42 | n3 = 708 | P (VER) | RD L1363-L1545 |
| B-36 | ext : rootless 708 | \|E(R3)\| = 1 150 ; ≤ 383 triangles R3 ; coins ≥ 6 860 ; 4-cycles A_R3 ≥ 3 041 ; tr(A_R3⁴) ≥ 67 848 ; 2 832 candidats transversaux | n3 = 708 | P (DERIVED/VER) | RD L2187-L2206, L2116-L2118 |
| B-37 | ext : rooted 708 | 574 118 037 colonnes Pb = 2·1 ; 448 879 368 sans doublon ; CNF 1 233 001 vars, 4 323 943 clauses | n3 = 708 | C | RD L2150-L2177 |
| B-38 | ext : circuits (rang 11) | B_4+B_6+B_8 ≥ 1386 ; #circuits 4..9 ≥ 2079 puis 2772 puis 4389 ; B_4+…+B_9 ≥ 4158 / 5544 / 8778 / 12474 / 18018 ; B_4 ≥ 4182 (face d'égalité) | rang 11 | P (VER) | RD L536-L648 |
| B-39 | ext : Q (rang 11) | ≥ 7059 (chaîne au §6) ; c_x ≤ 13 ; j_x ≤ 36 ; S5 = 17820 − 3n3 − 4p3 − 5a3 − 5b3 ≥ 0 ; ε ≥ 5b | rang 11 | P (VER) | RD L663-L685 ; AR L1051-L1074 |
| B-40 | ext : racines (face d'égalité, fermée) | 231..415 → 297..415 → 349..415 ; n_5 ≥ 15 ; n_7 = 0 ; ≥ 94 264 triangles arc-en-ciel | rang 11, égalité | P (VER) | RD L575-L604 |
| B-41 | ext : W205 | t_xy ≥ 6, moyenne 7 ; 646 matrices (t = 6) et 7 886 (t = 7) ; rang_F3(U) = 99 | rang 11 | P (VER) | RD L3972-L3990 |
| B-42 | ext : catalogues W17/W19 | 455 + 2 graphes (W17) ; 510 489 connexes + 177 déconnectés ; 748 825 placements Z ; 8 935 survivants ; 66 orbites ; 16 systèmes | n3 = 54, 60 | P (VER) | RD L1068-L1150 |
| B-43 | ext : rang 42 | 1 714 426 560 + 19 916 886 528 000 paires ; 0 survivant | général | C | RD L2934-L2938 |
| B-44 | ext : quotients d'ordre 11 | 1 108 533 nœuds, 0 quotient ; 8 980 nœuds (indépendant) | ordre 11 | C | AR L423-L426 |
| B-45 | ext : extrémité 4158, prismes | 282 774 clauses par branche parente ; 60·C(84,6) = 24 388 892 640 clauses résiduelles ; 96 215 triangles potentiels | extrémité | C | RD L2440-L2548 |

### 8.3 Lemmes ouverts et étapes manquantes, et ce qu'ils donneraient

| # | manque | donnerait | source |
|---|---|---|---|
| O-01 | générateur ordonné sur 42 orbites (entrelacement + D + F2 + 2^7⋊S7) | décision certifiable de C2 : « pas d'involution ⇒ \|Aut\| ∈ {1,3} », ou un graphe | NI L58-L64 |
| O-02 | rédaction complète de l'équivalence (R)(D)(I)(P) ⇔ A²+A−12I=2J | fiabilité de tout verdict du modèle orbitaire | TR L2373 |
| O-03 | relecture humaine ou Lean du théorème F2 (étape : réduction mod 2 du polynôme caractéristique + diagonalisabilité) | statut « accepté » | TR L1499, L2373 |
| O-04 | cassage de symétrie lex-leader / BreakID et cube-and-conquer | « chance honnête de verdict 15–25 % sur une semaine » (estimation) | TR L2352 |
| O-05 | analogue Z2 de l'astuce noyau entier ⇒ moment de phases | contrainte sur le couplage D | TR L1902 |
| O-06 | équation quadratique de Lundle22, sous-Grams avec orbites indépendantes, factorisation binaire des 44 Grams (C3) | filtres C3 au-delà de C6 (moot depuis L04-01) | SUI L22-L24 ; TR L1972 |
| O-07 | ext : compatibilité simultanée à trois centres (ou à 99 centres), noyau de croisement sur row(U), localisateurs | décider l'extrémité de rang 11 | RD L3992-L3996 ; AR L1118-L1121 |
| O-08 | ext : classification des traces d'ordre 4 h_xy des non-arêtes + identité globale de la matrice 99×99 | Q ≥ 7060 ou exclusion | AR L1096-L1100 ; ST L4213-L4216 |
| O-09 | ext : forcer b > 0 (label bi-orienté) | Q > 7059 | RD L679-L685 |
| O-10 | ext : plafond de 25 (resp. 24) paires antipodales | exclusion de r_ext = 28 (resp. 30) | AR L589-L599 |
| O-11 | ext : certificat de Jacobi ≤ 51 975 | exclusion de r_ext = 28 | AR L630-L631 |
| O-12 | ext : bornes supérieures sur N16, N18 | refermer l'étau avec 407N16 + 43N18 ≥ 2165002 et N14+N16+N18 ≥ 5868 | RD L224-L226 |
| O-13 | ext : dictionnaire graphe → unités signées pour la masse du LP thêta | utiliser les bornes W101 dans chaque ligne | AR L545-L547 |
| O-14 | ext : N_Wagner ≥ 18710, ou E ≤ 8, ou lemme des quatre échecs | exclusion de l'extrémité 4158 | RD L411-L429 ; AR L834-L846 |
| O-15 | ext : 45 indices de triangles de degré signé ≤ 3 | exclusion de l'extrémité 4158 | RD L2296-L2302 |
| O-16 | ext : fermer branch15 ∧ x187 = 0, puis les 32 autres cas | couverture 33/33 ⇒ exclusion de l'extrémité 4158 | AR L317-L339 |
| O-17 | ext : compatibilité simultanée B/H à 60 blocs, ou entre triangles de base | exclusion ou réduction de l'extrémité | RD L2399-L2409, L2592-L2594 |
| O-18 | ext : rang 708 : solution binaire ou infaisabilité du critère à 6 blocs ; forçage du motif sans racine ; det(B) ≤ 3645 | exclusion de n3 = 708 ⇒ n3 ≥ 711 | RD L2126-L2132, L1467-L1468 |
| O-19 | ext : théorème « plusieurs blocs d'arêtes contribuent des directions globales indépendantes » | dépasser la limite 39 < 44 des méthodes de rang local | AG `2026-07-27-wave43-success-forecast.md` L18-L24 |
| O-20 | ext : faisabilité entière (Z/4Z, GF(4), Arf, énumérateurs complets), facteur 36×60, témoin de transition fort | nouvelles exclusions dans ces espaces | RD L295-L358, L688-L702, L3599-L3606 |
| O-21 | littérature : texte primaire de Makhnev (N3 forcé) ; Crnković–Maksimović 2020 ; manuscrit de Baker | solidifier les maillons CITED | DR L25 ; L03a-33 ; AT `wave19-status-search/negative-results.md` L80-L90 |
| O-22 | ext : couplage entre arêtes distinctes, par exemple « toutes les arêtes ne sont pas de type 2+2+2 » (en partie dépassé par rang ≥ 28 à l'extrémité) | sortir de la borne locale 19 / 27 | AT `wave39-edge-local-rank/failed-routes.md` L17-L20 |
| O-23 | ext : prouver r_ext ≥ 43 (ou exclure chaque ligne paire 28…42) | non-existence (C-49) | L03a-111 |

### 8.4 Méthodes transférables

| # | méthode | cas source | cas cible possible | dit par la source ? | source |
|---|---|---|---|---|---|
| M-01 | **Dictionnaire de rang** : r_ext = rang_F7(2A−J+I) = rang_7(S) = rang_F7(M) (car NMNᵀ = 27I−9A+J ≡ S mod 7) ; la note LAB donne rang_7(S) = r−1 avec r = rang_7(A−3I) ⇒ r_équipe = r_ext+1 | ext W39, W42, W66 | toutes les « fenêtres de rang » de l'équipe (C1, rangs 33/35/37) : W66 ⇒ r_équipe impair ∈ {29,…,43} | non (observation de l'agent) | RD L2637-L2645 ; AR L410-L411 ; lab_note.md L11, L175 |
| M-02 | réduction enracinée + forçage de l'involution (flip) ⇒ modèle orbitaire ; contrôles k=4 / k=6 | session (C2) | prescrire toute action à un point fixe ; Thakkar–Severini font de même pour Z7 et Z3 | oui (session ; T–S L276-L289) | NI L17-L30 ; LIT `ts/caisc_2026.tex` L270-L289 |
| M-03 | argument 2-adique (réseaux de p-permutation, Broué) ou lecture des multiplicités par tr(S) + idempotence mod p + Schur | session (C2) | ordre 3 sans point fixe : E3 3-entier et χ3(g) = 0 (calcul de l'agent) ⇒ L3 libre sur Z3[C3] ; analogue de l'identité trace–rang d'Ishida | non (observation de l'agent, L03a-110) | NI L36-L45 ; LIT `ishida/…tex` L1192-L1215 |
| M-04 | noyau entier du Gram d'un ensemble d'orbites ⇒ annulation d'un moment antisymétrique de phases | C3 (hexagone) | involution (phases Z2 : quel membre de l'orbite est adjacent) | oui (TR L1902) | HEX L89 ; SUI L84-L88 |
| M-05 | générateur ordonné à filtres spectraux (Ps, Pr, Es, Er projecteurs ; entrelacement de Cauchy) avec contrôle de solidité sur une solution connue | C2, contrôle sur srg(243,22,1,2) | toute branche à quotient spectralement prescrit ; famille srg(n,2m,1,2) via `Frame(m)` | oui (code) | PH2 `spectral_orderly/psd_gen.py` L1-L14 ; `sound_m11.txt` |
| M-06 | contrôles positifs exacts : Petersen, Clebsch, tour 3×3 = srg(9,4,1,2) (ext) ; srg(9,4,1,2) et srg(243,22,1,2) (session) ; contrôle négatif srg(19,6,1,2) | ext W45, W147 ; session | calibrer toute relaxation ou tout encodage avant la cible | oui | RD L357, L3112 ; NI L48-L50 |
| M-07 | limite des méthodes de rang local à une arête (bloc 39 ≤ plafond 44) ; non-additivité des noyaux locaux (h_v = (A+4I)e_v) | ext W41–W43 | toute stratégie de « fenêtre de rang » de l'équipe | oui (W43, prévision) | AG `2026-07-27-wave43-success-forecast.md` L18-L60 ; RD L2879-L2892 |
| M-08 | formes modulaires de niveau 7 (Γ0(7), Fricke, Sturm) pour forcer des vecteurs courts dans chaque ligne de rang | ext W71–W101 | autres lignes de rang ; la note LAB « Level-7 theta series… » | oui (W101 l'étend à toutes les lignes) | AR L435-L551 |
| M-09 | bornes de coquille de norme 14 par graines de Fano complémentaires enracinées (1er et 2e moments) | ext W90–W100 | normes 16 et 18 (manque reconnu) | oui (manque reconnu) | AR L497-L513 |
| M-10 | inégalité spectrale des sous-graphes denses 2e(X) ≤ 3m + m²/9 | ext W15–W18 | tout ensemble actif induit de degré minimum connu (C1, C2) | non | RD L978-L986 |
| M-11 | obstruction de Schur : tr(A4) = 84(n3 − 693) ; projecteur des triangles M = 21E | ext W20 | autres invariants de comptage (C6, prismes) | non | RD L1165-L1193 |
| M-12 | commutateur d'incidence K = NDNᵀ avec P−4 ⇒ d constant ⇒ divisibilités | ext W31 | toute décomposition par blocs signés de triangles | non | RD L1808-L1844 |
| M-13 | Hilton–Milner et familles intersectantes de 3-sous-ensembles des 7 triangles d'un sommet | ext W195–W196 | toute borne de « drapeaux » à un centre (C1 local) | non | AR L1039-L1046 |
| M-14 | discipline des certificats : UNSAT seulement avec preuve rejouée (VeriPB / LRAT / DRAT) ; statut flottant jamais promu (faux négatifs HiGHS) | ext ; session | tout calcul de l'équipe | oui | CR `CONJECTURE.md` L138-L146 ; RD L3060-L3062 ; TR L2365 |
| M-15 | bris de symétrie sûr par potentiel d'orbite partagé, sans automorphisme cible (W110) ; représentants sous C2 ≀ S7 sûrs seulement pour l'échafaudage | ext | encodages C1 et C2 (lex-leader sous 2^7⋊S7) | oui | AR L613-L616 ; ST L3382-L3385 |
| M-16 | percolation bootstrap des non-arêtes (dichotomie : percole, ou fermeture K3 □ K3) | ext W56 | tout argument de propagation à deux sommets | non | RD L3388-L3398 |


<!-- ===== L03b_session_eeaf2d22.md:344-472 ===== -->

## 8. Matériaux pour la recombinaison

Notations du dépôt externe (à ne pas confondre avec celles de l'équipe) :
- `n3` = nombre de sous-graphes induits N3 (deux triangles disjoints reliés par exactement deux arêtes croisées indépendantes) ; `P` = nombre de prismes triangulaires induits ; identité `n3 + 3P = 4158` (CR/attempts/wave56-percolation-closure/derivation.md:L129-L130 ; CR/verification/2026-07-22-n3-count-bound-audit.md:L50-L51).
- `M = 21 E0` = 21 fois le projecteur sur l'espace propre 0 (dimension 44) du graphe des 231 triangles ; `r3 = rank_F3(M)`, `r7 = rank_F7(M)` (CR/verification/2026-07-23-wave20-global-schur-audit.md:L226-L274 ; CR/verification/2026-07-27-wave40-orchestrator.md:L22-L26).
- `S = 2A - J + I` (Seidel), `r = rank_F7(S)` ; le dépôt identifie ce `r` au rang F7 universel (CR/verification/wave66-spherical-code-shift/audit.md:L23-L48). La fiche L03a (L03a-103, statut H) donne le dictionnaire r_ext = rank_F7(S) = rank_F7(M) et r_équipe = rank_7(A - 3I) = r_ext + 1.
- `N14, N16, N18, N20` = nombres de vecteurs propres ENTIERS x de A (Ax = -4x, x dans Z^99), deux signes comptés, de norme carrée x.x = 14, 16, 18, 20 (« squared coordinate norm ») (CR/attempts/wave71-modular-theta-extension/README.md:L22-L25 ; CR/attempts/wave90-short-vector-count-upper/README.md:L11).
- « endpoint de rang 11 » = n3 = 4158, P = 0, rank_F3(D) = 11 avec D = C + J (CR/verification/wave176-star-projector-circuits/audit.md:L10) ; `Q` = nombre de circuits projectifs courts (poids 4 à 9) réalisant des non-arêtes dans le code ternaire de cet endpoint (CR/verification/README.md:L1987-L2000 ; CR/verification/wave180-capacity3-companion/audit.md:L100).
- « C3 » dans les noms des vagues 60, 61, 63 = cas kappa = 3 (noyau de voisins à trois composantes), PAS le cas « ordre 3 » de l'équipe (CR/attempts/wave60-c3-incidence-design/README.md:L3-L5).
- « T20 » (vagues 30-31) = un réseau de rang 20, déterminant 729 ; a priori sans rapport avec le dossier work/t20_hand de l'équipe (L03b-100).

### 8.1 Énoncés conditionnels « si X alors exclusion / contradiction »

| # | X (hypothèse exacte) | conclusion | statut | source |
|---|---|---|---|---|
| K1 | srg(99,14,1,2) existe (aucune symétrie) | n3 >= 705 (positivité de Schur + parité) puis n3 != 705, donc n3 >= 708 et induced_C6 >= 209 994 | P (relu interne) | L03b-071, 078 ; CR/verification/2026-07-23-wave20-global-schur-audit.md:L3-L14 ; CR/verification/wave23-endpoint-crosscheck/2026-07-23T195158Z-audit.md:L5-L11 |
| K2 | n3 = 0 (aucun N3 induit) | contradiction (Makhnev 1988, Théorème 2 sous la condition (*)) | CITED ; texte de 1988 non rejoué (O) | L03b-049 ; CR/verification/2026-07-22-wave14-status-audit.md:L295 ; CR/verification/2026-07-22-wave13-status-audit.md:L196-L200 |
| K3 | n3 = 705 | h dans {1,9} ; et h >= 21 => n3 != 705 (h = [L : 21 L*]) | P | L03b-075 ; CR/verification/wave21-lattice-extension/2026-07-23T184926Z-audit.md:L5-L31 |
| K4 | n3 = 708 | h dans {9,21,49,81,189,441,729,1029}, det(B) <= 6525, tr(C^2) >= 10, tr(B^2) >= 116, q(T) <= 11 | P | L03b-081, 082 ; CR/verification/wave24-n3-708-index/2026-07-23T204222Z-audit.md:L5-L19 ; CR/verification/wave25-n3-708-strictness/2026-07-23T215549Z-audit.md:L5-L21 |
| K5 | n3 = 708 et la forme duale mise à l'échelle a un facteur orthogonal A2 | aucun cadre de projecteur à 231 lignes (et tr(A2 Q_AA) >= 18) | P | L03b-085, 086 |
| K6 | n3 = 708 et la forme est une somme orthogonale complète de réseaux de racines ADE irréductibles | impossible | C/P (conditionnel) | L03b-091 ; CR/verification/README.md:L583-L591 |
| K7 | n3 = 708 et S = K12 + LAMBDA(F) | impossible | P | L03b-098 |
| K8 | incidence sommet-triangle réelle et décomposition orthogonale entière non triviale sans racine de la forme S d'endpoint | contradiction (231 \| b) | P (deux audits) | L03b-101 ; CR/verification/wave31-sign-commutant/audit.md:L3-L17 |
| K9 | n3 = 708 avec une racine de norme 2 | support Fano-complément 7+7, image (+1)^21 0^189 (-1)^21, partition 14+70+15 et design 2-(15,3,2) (critère nécessaire et suffisant d'extension de graphe) | P | L03b-106, 109 |
| K10 | n3 = 708 sans racine, indécomposable | tr(A_-1 A_-2^2) = 0 ; si l'on prouvait tr > 0, la branche serait exclue | P / LEMME | L03b-107 ; CR/verification/wave33-continuation-protocol.md:L59-L74 |
| K11 | g automorphisme d'ordre 11 | g sans point fixe ; et le quotient semi-régulier 9x9 n'existe pas, donc aucun automorphisme d'ordre 11, pas de graphe sommet-transitif | P + C | L03b-168, 169 |
| K12 | G est un graphe de Cayley (groupe d'ordre 99, tous abéliens) | contradiction (somme de racines de l'unité = -18/7 ou 81/7) | C | L03b-169 ; CR/attempts/wave69-cyclic-cover-shift/README.md:L24-L26 |
| K13 | n3 = 4158 (P = 0) | q(T) = 12 pour tout T ; S^2 = 13S + 68I ; r3 >= 12 ; r3 + r7 pair ; d_i d_(232-i) = 441 ; r7 >= 22, puis >= 28 | P | L03b-123, 124, 132, 137 |
| K13b | rank_F7(M) = 27 | un prisme triangulaire induit existe, donc n3 <= 4155 dans cette branche (branche ensuite vide : r pair >= 28 par la vague 66) | P | L03b-137 ; CR/verification/2026-07-27-wave44-integration-audit.md:L66-L70 |
| K14 | rank_F7(M) <= 20 / <= 22 / <= 24 | toute arête de type 2+2+2 / types 2+2+2 ou 2+4 seulement / pas de type 3+3 | P | L03b-130 ; CR/verification/wave39-edge-local-rank/README.md:L95-L97 |
| K15 | n3 = 4158, r3 = 12 et toutes les arêtes de type 2+2+2 | chaque bloc K39 de rang F7 >= 33 ; r7 pair >= 34 | P | L03b-133 ; CR/verification/wave41-allquotient-lifts/audit.md:L5-L11 |
| K16 | r = rank_F7(2A-J+I) = 28 (q = 16) | N14 + N16 + N18 = 2 mod 14 et N14 + N16 + N18 >= 5868 ; il existe un vecteur propre entier de -4 de norme 14, 16 ou 18 | P | L03b-170, 177 |
| K17 | n3 = 4158 et r = 28 | 407 N16 + 43 N18 >= 2 165 002 ; SI de plus chaque quadrilatère induit a au plus 25 extensions antipodales norme 16/18, ALORS 407 N16 + 43 N18 <= 2 115 382 : contradiction (plafond non prouvé) | P (implication) / O (plafond) | L03b-180, 183 ; CR/attempts/wave96-norm16-norm18-upper/README.md:L5-L21 |
| K18 | n3 = 4158 et r = 30 et au plus 24 extensions antipodales jusqu'à la norme 20 par C4 | exclusion du rang 30 (plafond non prouvé) | O | L03b-180 ; CR/attempts/wave96-norm16-norm18-upper/README.md:L26-L35 |
| K19 | n3 = 4158 et défaut noyau-frange global E <= 8 (E = 8(18711 - N_Wagner)) | contradiction (l'endpoint exige E >= 16) | O (borne non prouvée) | L03b-205 ; CR/verification/README.md:L1915-L1920 |
| K20 | P = 0 implique au plus quatre marques échouées par non-arête | borne inférieure de Wagner (non prouvée) ; vague 169 : les clauses locales actuelles ne peuvent pas la prouver | O | L03b-204, 206 |
| K21 | endpoint de rang 11 | Q >= 7059 ; toute borne supérieure compatible Q <= 7058 exclurait cet endpoint (aucune connue) | P / O | L03b-213 ; CR/verification/README.md:L2119-L2135 |
| K22 | une inégalité de motif globale force au moins un prisme | n3 <= 4155 | O | L03b-134 ; CR/verification/2026-07-27-wave41-orchestrator.md:L87-L88 |
| K23 | une coclique de taille 22 (Hoffman) existe | 22 couplages de points, configuration 77_3, design 2-(22,4,2) ; compatibilité inconnue | O | L03b-032 ; CR/verification/2026-07-22-wave3-audit.md:L41-L58 |
| K24 | une non-arête ne percole pas (2-bootstrap) | sa clôture est un K3 x K3 = srg(9,4,1,2) induit unique ; à P = 0 toutes les non-arêtes percolent | P | L03b-153 |
| K25 | X sous-ensemble de sommets avec degré induit minimum >= 6 | \|X\| >= 27 | P | L03b-054 |
| K26 | un sommet extérieur et un L(K3,3) = graphe de la tour induit | le sommet le rencontre au plus une fois (saturation lambda/mu) | P | L03b-040 ; CR/verification/2026-07-22-n3-36-equality-audit.md:L109-L119 |
| K27 | automorphisme d'ordre 3 sans point fixe (C3) | 6 ou 27 orbites triangulaires (Lean, conditionnel) ; f = 27 impossible ; type (6,3^7) à tau = 6 exclu ; branche t=6, P=K3,3, A9 fermée impossible ; critère de complétion mod pi^3 | P / C (externes, non relus) | L03b-015 à 019, 117 |
| K28 | Lou-Murin : gamma = 12 en tout triangle | structure srg(9,4,1,2) impossible ; un srg(9,4,1,2) privé d'une arête force le srg(9,4,1,2) complet | P (cité) | L03b-004 |
| K29 | Keramatipour : onze Paley(9) indépendants | impossible (preuve omise) ; motif Paley(9) partout impossible | P / O | L03b-005 |
| K30 | Harrison (non vérifié) : une racine avec >= 14 fibres C4 ; plafond R230 'Paley-perfect' | UNSAT annoncé, preuves absentes de l'arbre épinglé | O | L03b-118 |
| K31 | fixer une branche/classe par multiensemble de cycles ; réduire par la symétrie de l'échafaudage | réduction non sûre (rejetée) | R | L03b-025, 161 |

### 8.2 Bornes quantitatives

| # | objet | inégalité / valeur | hypothèses | statut | source |
|---|---|---|---|---|---|
| B1 | n3 | 708 <= n3 <= 4158 ; induced_C6 = 209 286 + n3 >= 209 994 | existence | P | L03b-078, 011 |
| B2 | P (prismes) | P = (4158 - n3)/3 <= 1150 | B1 | dérivé | L03b-036, 153 |
| B3 | trace | tr(M (M o M) M) = 84 (n3 - 693) | existence | P | L03b-071 |
| B4 | arêtes induites | 2 e(X) <= 3\|X\| + \|X\|^2/9 pour tout X | existence | P | L03b-054 |
| B5 | clôtures K3 x K3 induites H | H <= 231, 6H <= P, R = 18H, R <= 4158 - n3 ; avec B2 : H <= 191 (dérivation du lecteur) | existence | P (+ dérivé) | L03b-153 |
| B6 | N14 | N14 <= 2 floor((55440 - 5 n3)/14) (général) ; <= floor((55440 - 4 n3)/7) ; 7 N14 <= 55440 - 5 n3 - O/2 ; <= 4950 à P = 0 (avant : 5544) | existence | P | L03b-185, 179, 187, 183, 178 |
| B7 | N14+N16+N18 | >= 5868 ; = 2 mod 14 | r = 28 | P | L03b-177, 170 |
| B8 | 407 N16 + 43 N18 | >= 2 165 002 | P = 0, r = 28 | P | L03b-183 |
| B9 | rank_F7(M) | >= 27 universel (11 -> 13 -> 19 -> 25 -> 26 -> 27) | existence | P | L03b-135 |
| B10 | r = rank_F7(2A-J+I) | r pair dans {28,30,...,42} | existence | P | L03b-165 |
| B11 | réseau M (vague 66) | det M = 9 * 7^(44-r), M*/M = Z/9 + (Z/7)^(44-r), niveau 63, min(M*) >= 2 | existence | P | L03b-165 |
| B12 | SNF(T), T = 9S + 7J | diag(1, 9^(r-1), 63^(99-2r), 441^(r-1), 3969) | existence | P | L03b-175 |
| B13 | coclique | il existe un ensemble indépendant de taille 13 ; alpha <= 22 (Hoffman) | existence | P | L03b-126, 032 |
| B14 | N_cube, N_Wagner | 41580 - n3 + 12 N_cube - 4 N_Wagner >= 0 ; 12 N_cube <= 41580 - n3 ; N_cube <= 3118 à P = 0 ; d'où N_Wagner <= (41580 - n3)/2 (dérivation du lecteur) | existence | P (+ dérivé) | L03b-201, 203 |
| B15 | Q | Q >= 7059 (7 752 circuits projectifs, 15 504 scalaires) ; B4 + ... + B9 >= 18 018 (mots duaux) | endpoint de rang 11 | P | L03b-213, 211 |
| B16 | rangs à n3 = 4158 | 12 <= r3 <= 44, 28 <= r7 <= 44, r3 + r7 pair ; paires arithmétiques 629 -> 528 -> 429 -> 330 -> 314 -> 297 | n3 = 4158 | P | L03b-124, 126, 130, 132, 133, 135, 137 |
| B17 | fixed triangle | (a0,a1,a2,a3) = (20+q, 180-3q, 3q, 12-q), 0 <= q <= 12, q != 1 ; 2 n3 = 3 sum_T q(T) | existence | P | L03b-037, 071 |
| B18 | G[Y] (triangle fixé, P = 0) | 60 sommets, 8-régulier, 32 triangles ; mult_Y(3) = 18 ; mult_Y(-4) = 7 + kappa ; C4(X) <= 27 ; rank(B) = 35 - kappa | P = 0 | P | L03b-155, 156 |
| B19 | hypergraphe enraciné (P = 0) | D + 5I = Z Z^T ; 1260 <= c4(R) <= 2331 ; 64/5 <= tr(T E_3) <= 16 | P = 0 | C | L03b-164 |
| B20 | code F7 | [99,44]_7, d(C^perp) >= 6 ; [4851,378]_7 pour C_2(S) | r = 28 | P | L03b-173, 181 |
| B21 | ker_F2(A) | poids minimal >= 8 ; support de poids 8 indépendant | existence | P | L03b-166 |
| B22 | Aut(G) | ordre premier à 11 (dépôt externe) ; pair => divise 6, 7 \| \|Aut\| => Z7 (Cesarz-Woldar, cité) ; \|Aut\| dans {1,2,3} selon la note de session (Behbahani) | existence | P / C / cité | L03b-169, 003 |
| B23 | cycles (P = 0) | C8 = 2079, C10 = 33 264, C12 = 250 866, C14 = 2 494 800 (graphe d'incidence) | P = 0 | P | L03b-158 |
| B24 | 7 sommets (Reimbayev) | 2 n3 <= z11 <= 4 n3 (et 4 \| z11 selon l'audit de la session) | existence | cité | L03b-007 |
| B25 | Thakkar-Severini | circulantes : <= 33 classes de différences (68 %) ; heuristique 3501/4950 = 70,73 % | familles restreintes | O / E | L03b-008 |
| B26 | designs 2-(15,3,2) | environ 1,5 x 10^21 (McKay, estimation) | — | cité | L03b-120 |
| B27 | endpoint n3=4158 | 24 388 892 640 clauses résiduelles statiques ; CNF enracinée 1 233 001 variables / 4 323 943 clauses | — | C | L03b-127, 115 |
| B28 | Ishihara | degrés exacts H2 -> H1 : 1^20, 2^51 ; graphe résiduel à 84 sommets connexe | existence | P | L03b-064 |
| B29 | fibres de compagnons | sum binom(R_uv, 2) >= 96 ; S_g = 96 + z_g ; au moins 231 quadrilatères résiduels non séparés | existence | P | L03b-031 |

### 8.3 Lemmes ouverts / étapes manquantes et ce qu'ils donneraient

| # | lemme manquant | ce qu'il donnerait | source |
|---|---|---|---|
| O1 | plafond de 25 extensions antipodales norme 16/18 par C4 (ou toute borne supérieure sur N16, N18) | exclusion de la ligne r = 28 à l'endpoint sans prisme | L03b-180, 183, 189 |
| O2 | plafond de 24 extensions jusqu'à la norme 20 par C4 | exclusion du rang 30 à l'endpoint | L03b-180 |
| O3 | E <= 8 (noyau-frange) ou 'au plus quatre marques échouées par non-arête' | exclusion de l'endpoint n3 = 4158 ; borne Wagner | L03b-204, 205 |
| O4 | borne supérieure Q <= 7058 (endpoint de rang 11) | exclusion de cet endpoint | L03b-213 |
| O5 | inégalité globale forçant un prisme | n3 <= 4155 | L03b-134 |
| O6 | certificat dual PSD rationnel à deux racines d'ordre huit | borne supérieure générale sur n3 | L03b-197 |
| O7 | loi de compatibilité à trois centres (K_D sur row(U), Q o (D S_x D), normes de w_TU) | seule voie restante pour les traces d'ordre quatre | L03b-215, 012 |
| O8 | tr(A_-1 A_-2^2) > 0 sous incidence réelle | exclusion de la branche sans racine à n3 = 708 | L03b-107, 112 |
| O9 | solution ou exclusion du critère binaire (D,B,H) 14+70+15 / CNF enracinée complète avec preuve | décision de la branche enracinée à n3 = 708 | L03b-109, 115, 176 |
| O10 | det(B) <= 3645 à n3 = 708 | restriction d'index plus forte | L03b-087 |
| O11 | couverture prouvée des 33 cas (dont branch15 AND x187=0) | exclusion de l'endpoint n3 = 4158 | L03b-128, 148, 152 |
| O12 | 45 indices de degré de support <= 3 | contradiction avec rang 44 (Gershgorin) | L03b-123 |
| O13 | matrice binaire B à 60 colonnes + A_Y 8-régulière compatibles (ou exclusion des 275 orbites kappa = 3) | fermeture des lignes kappa = 1, 2, 3 | L03b-156, 159 |
| O14 | R = 3P (tout prisme dans une clôture de tour) | égalité S = n3 (non prouvée) | L03b-153 |
| O15 | classification des designs 2-(22,4,2) compatibles | traitement du cas alpha = 22 | L03b-032 |
| O16 | texte de Makhnev 1988 | fiabiliser K2 (n'est plus nécessaire pour B1) | L03b-014, 049 |
| O17 | preuves de Harrison ; manuscrit de Baker ; preuve de Keramatipour (onze Paley(9)) | faits importables (C4/Paley(9)) | L03b-118, 065, 005 |
| O18 | extension complète du motif C4 x K3 induit | exclusion ou réalisation de ce motif | L03b-188 |
| O19 | graphe extérieur simultané à 83 sommets (norme 16) | fermeture de la couche norme 16 | L03b-174 |

### 8.4 Méthodes transférables (dites par les notes, ou suggestion du lecteur)

| # | méthode | cas d'origine | transfert possible | qui le dit | source |
|---|---|---|---|---|---|
| T1 | positivité de Schur sur le projecteur du graphe des triangles + parité mod 2/4 (tr(MWM) = 84(n3-693)) | général (vague 20) | C1, C2, C3 telle quelle ; spécialisable sous symétrie | lecteur | L03b-071 |
| T2 | borne spectrale de sous-ensemble 2e(X) <= 3\|X\| + \|X\|^2/9 | n3 = 48, 51 | toute configuration locale dense (C1) | lecteur | L03b-054 |
| T3 | obstruction de Gram extérieur G = 12I - D - D^2 + 2J = C C^T avec séparateur de Farkas exact | n3 = 60, résidu B | exclusion de toute complétion d'un sous-graphe induit fixé (gabarits/noyaux de l'équipe) | lecteur | L03b-068 |
| T4 | matrice orthogonale entière T = 18A - 2J + 9I, T^2 = 63^2 I | général | formulation exacte sans symétrie (C1) | note | L03b-175 |
| T5 | réseau des droites équiangulaires, Milgram, theta de niveau 7 (Skoruppa), vecteurs propres entiers de normes 14/16/18 | r = 28 | comparer aux 'rangs' et 'normes 18/26' de C1 ; dictionnaire r_équipe = r_ext + 1 selon L03a-103 (H), d'où r_équipe impair dans {29,...,43} | lecteur (+ L03a) | L03b-165, 170, 177 |
| T6 | argument des points fixes (voisins communs de deux sommets fixes sont fixes si 1, 2 < p) | ordre 11 | ne passe pas tel quel à p = 2, 3 (C2, C3) | lecteur | L03b-168 |
| T7 | Fourier sur groupes abéliens d'ordre 99 | Cayley | déjà exhaustif pour les Cayley | note | L03b-169 |
| T8 | chaîne de preuves épinglée CaDiCaL -> drat-trim -> lrat-check ; Exact -> VeriPB -> CakePB ; refus des traces PySAT ; contrôle exact contre les 'infeasible' flottants (HiGHS) ; reconstruction rationnelle exacte (FLINT/Dixon) | calibrations | tout calcul SAT/LP de l'équipe (cf. bug OR-Tools 18/10) | note + lecteur | L03b-026 à 028, 138, 162, 193 |
| T9 | règles de sûreté de symétrie (types grossiers != orbites ; la symétrie de l'échafaudage peut moyenner des certificats, pas réduire les candidats ; énumération étiquetée complète + recoupement canonique) | général | découpes par cas C1/C2/C3 | note | L03b-025, 161, 169 |
| T10 | flag algebras / moments de drapeaux à deux racines d'ordre huit | endpoint | borne générale sur n3, aussi en C1 | note + lecteur | L03b-139, 147, 197 |
| T11 | critère de complétion modulaire mod pi^3 (Lundle22) | C3 | analogue en Z[C2] pour C2 ; la session note la liberté Z2[C2] | lecteur | L03b-016 ; transcripts/conway99-research-state.md:L19 |
| T12 | clôture par 2-bootstrap-percolation (Ibrahim-LaFayette-McCall 2025) | général | comptage des Paley(9) = srg(9,4,1,2) induits (H <= 191), lien avec C1/Paley | lecteur | L03b-153 |
| T13 | compléments d'étoile, projecteurs E_3, E_-4 restreints à un sous-ensemble | endpoint | C1 (l'équipe a une bibliographie 'star complements') | lecteur | L03b-154, 155 |
| T14 | échafaudage enraciné à 84 étiquettes et groupe C2≀S7 (645 120) ; transitions sur K14 - 7K2 | général | identique au modèle d'orbites 42x42 de C2 (session eeaf2d22) | lecteur | L03b-010, 020, 023, 163 |
| T15 | lemme de saturation de la tour (un sommet voit un srg(9,4,1,2) induit au plus une fois) | n3 = 36 | travail Paley(9) de l'équipe | lecteur | L03b-040 |
| T16 | contraintes de code binaire de A (ker_F2, poids >= 8) | général | C1/C2/C3 | lecteur | L03b-166 |
| T17 | prior art à importer : 11 types d'arêtes de Gray Taylor, équations alpha/beta/gamma de Lou-Murin | littérature | éviter les redécouvertes | note (DR) | L03b-004, 006 |
| T18 | énumération canonique sur la réduction à 84 sommets avec stabilisateurs dans 2^7 x\| S7 | proposition DR | C1 (sans symétrie) | note (DR) | L03b-013 |



<!-- ===== L04_C3.md:433-557 ===== -->

## 8. Matériaux pour la recombinaison

### 8.1 Énoncés conditionnels « si X, alors exclusion ou contradiction »

| # | X (précis) | conclusion | statut | source |
|---|---|---|---|---|
| CND-1 | g ∈ Aut(Γ) d'ordre 3 **sans point fixe** | il existe (Q, M) : Q ∈ M₃₃(ℤ) symétrique, Q1 = 14·1, Q²+Q = 12I+6J ; M ∈ M₃₃(ℤ[ω]) hermitienne, M²+M = 12I ; Q ≡ M mod (1−ω) ; tr Q = 2τ, tr M = −τ | P + Lean | `conway99-c3-experimental:main:pdf/preuve_c3.tex:117-132` |
| CND-2 | un couple (Q, M) comme en CND-1 existe | contradiction (2 ≡ 1 mod 3) | P + Lean (`C3.no_pair`) | `…:pdf/preuve_c3.tex:136-208` |
| CND-3 | g d'ordre 3 avec exactement 3 points fixes | les points fixes forment un triangle, et le triple (Q 32×32, **a** 32×3, M 32×32) vérifie Ã1 = 14·1, Ã²+Ã = 12I+2·1wᵀ, M²+M = 12I, Q ≡ M mod π ; un tel triple est impossible | P + Lean (`C3.Tri.no_triangle_pair`) | `…:pdf/preuve_c3.tex:218-258` ; `work/c3_review_2026-10-13/c3_proof_rewrite.tex:612-789` |
| CND-4 | g ≠ 1 et g³ = 1 | \|Fix(g)\| ≤ 3, donc \|Fix(g)\| ∈ {0, 3} | P + Lean | `…:pdf/preuve_c3.tex:263-286` |
| CND-5 | G cyclique d'ordre 3 agissant librement, V sous-espace G-stable de projecteur orthogonal **3-entier** | d₁ ≡ d_ω (mod 3), tous deux premiers à 3 ; donc dim V₁ = dim V_ω | P (dérivé) ; testé sur 1 340 cas libres et 318 cas β = 0, 0 violation | `…:notes/P1_recollement.md:96-117,151-158` |
| CND-6 | points fixes avec β = rang_F₃(P[Fix] mod 3) = 0 (pour Conway : Fix est une clique) | F est libre et CND-5 s'applique avec d₁ = det/3^r | P (dérivé) + observé | `…:notes/P1_recollement.md:119-133` |
| CND-7 | srg(v,k,λ,μ) de valeurs propres k, θ, θ' ; 3 ∤ θ−θ' ; tous les premiers de θ−θ' ≡ 1 (mod 3) ; intégralités vérifiées au cas par cas | pas d'action libre d'ordre 3 (critère) | **non démontré par écrit** ; balayage E | `…:pdf/preuve_c3.tex:321-325` ; `work/c3_review_2026-10-13/REVIEW_C3_PROOF.md:55-56` |
| CND-8 | MM04 et CW25 sont exacts (et Mak10 cor. 2.4) | \|Aut(Γ)\| ∈ {1, 2, 7, 11} | P conditionnel | `…:pdf/preuve_c3.tex:290-302` |
| CND-9 | CND-8 et, en plus, le calcul de BL11 | \|Aut(Γ)\| ∈ {1, 2} | P conditionnel | `…:pdf/preuve_c3.tex:294-302` |
| CND-10 | tous les problèmes quotient (étage Q) d'une classe de phases sont UNSAT | la classe est exclue (relaxation exacte) | P | `conway99-c3:main:rapport/audit_c3.tex:233-235` |
| CND-11 | tout le calcul restant finit UNSAT (≈ 40 instances, classes 29/43/44/45, étage P) et les lemmes d'entrées, de type, de triplets et lex sont relus | pas d'ordre 3 sans point fixe | O au 23/09 ; caduc depuis L04-01 | `…:README.md:27-28` ; `…:rapport/audit_c3.tex:311-312` |
| CND-12 | un problème quotient est SAT | il faut l'étage P (M²+M = 12I sur C) ; `stage_p.py` est prêt et auto-testé | E (outil) | `…:NUIT_JOURNAL.md:120` |
| CND-13 | Q seul (sans M) est impossible (D4) | preuve sans le côté Eisenstein | O (conjecture) | `conway99-c3-experimental:main:IDEES.md:15` |
| CND-14 | les exposants de d₁ et d_ζ sont contraints, par exemple par le 5-rang de A+8I (graphe de Moore, p = 13) | exclusion de l'ordre 13 par la congruence (d₁/p) = (d_ζ/p) | H (spéculation) | `…:IDEES.md:14` ; `…:JOURNAL.md:40-42` |
| CND-15 | hors lot : le « 14 » de DISC (C1) vient de la parité de v₇(det) d'un réseau propre | les blocs à quatre étoiles de classe 14 sont exclus « gratuitement », puisque a est pair | H (< 30 %, selon l'auteur) | `cw/review/02_symmetry_c3_c7.md:309-313` |
| CND-16 | hors lot : D3 (ordre 3), D7 (ordre 7), le manuscrit C2 et la littérature | Aut(Γ) est trivial | assemblé, en attente de relecture | `strongly-regular-graphs-research:main:papers/conway99_asymmetric/asymmetric.tex:100-107` |

### 8.2 Bornes et valeurs quantitatives

| objet | valeur ou inégalité | statut | source |
|---|---|---|---|
| orbites triangulaires (cas libre) | τ = 6 (a₁ = 18) ; l'intégralité seule donne τ ∈ {6, 13, 20, 27} | P (3 preuves) ; Ishida | `conway99-c3:main:rapport/audit_c3.tex:126-140` |
| orbites indépendantes | 27 (= 33 − 6) | P | `…:rapport/audit_c3.tex:121` |
| dimensions | r = dim ker(Q−3I) = r' = dim ker(M−3I) = 18 ; spectre de M : {3¹⁸, (−4)¹⁵} | P | `conway99-c3-experimental:main:pdf/preuve_c3.tex:211-213` ; `conway99-c3:main:rapport/audit_c3.tex:116` |
| χ₃(g) | = 3(τ−6)/7 = 0 | P | `…:rapport/audit_c3.tex:126` |
| points fixes, ordre 3 | \|Fix\| ∈ {0, 3} ; n_x ∈ {2, 8, 14} ; 15\|F\| ≤ 99 + Σ n_x ; le cas n_x = 8 donne 12 + 5s ≤ 0 | P + Lean | `…-experimental:main:pdf/preuve_c3.tex:263-286` |
| déterminant côté Q | d = 7^a·11^b avec b impair (en fait v₁₁ = 1), donc d ≡ 2 (mod 3) | P + Lean | `…:pdf/preuve_c3.tex:179,191` ; `…:notes/P1_recollement.md:139-143` |
| déterminant côté M | d' = 7^c ≡ 1 (mod 3) | P + Lean | `…:pdf/preuve_c3.tex:180` |
| Gram | GK = 77I ; G'K' = 7I ; G_W K_W = 21I ; cas du triangle : G̃K = 77I, G_W K_W = 189I, 3^r·99·det G̃ = t²·det G_W | P + Lean | `…:pdf/preuve_c3.tex:171-182,240-257` |
| entrées du quotient | Q_UV ≤ 1 si U est triangulaire ; ≤ 2 si U et V sont indépendantes ; exactement deux « doubles » par orbite indépendante | P | `conway99-c3:main:rapport/audit_c3.tex:96-108` |
| lignes de B | somme de la ligne i = 12 − deg_F(i) ; G₀ ≥ 0 et G₀ ⪰ 0 | P | `…:rapport/audit_c3.tex:150-153` |
| graphes F à 6 sommets | 156 → 87 (G₀ a une entrée négative) + 25 (non PSD) + 18 (Farkas) exclus → 26 survivants | C | `…:rapport/audit_c3.tex:162-173` |
| classes de phases | 318 → 191 (résidu négatif) + 2 (hexagone) → 125 → 46 à symétrie près ; 1 366 colonnes phasées | C | `…:rapport/audit_c3.tex:175-192` |
| énumération des supports | première passe 35/46 complètes (11 incomplètes, 1 163 supports, jusqu'à 560 par classe) ; réénumération avec phases 42/46 ; incomplètes : 29 (≥ 31 multi-ensembles), 43 (≥ 2), 44, 45 | S | `…:rapport/audit_c3.tex:220-229` ; `…:NUIT_JOURNAL.md:235-237` |
| complétude certifiée | classes 0 (4 multi-ensembles), 4 (96 multi-ensembles, 18 orbites sous \|Aut F\| = 12), 15, 25, 30, 32, 42 (1 chacune) | C | `…:certs/SUMMARY_ENUM.txt` ; `…:NUIT_JOURNAL.md:149,233-237` |
| problèmes quotient | 33 (pour 35 classes) → 27 distincts à isomorphisme près ; 18 ouverts → 16 distincts ; + 7 clairsemés | E | `…:NUIT_JOURNAL.md:123-128` |
| LQ | 15 infaisables sur 33 (13 par une seule ligne ; 891 lignes recoupées, 0 désaccord) | E | `…:NUIT_JOURNAL.md:18-19,61` |
| étage Q avec DRAT | 9 UNSAT : 8 dans `SUMMARY.txt` (résolution 37-353 s, vérification 36-210 s) et m16420_sL0 (3 515 s, preuve de 129 Mo, vérification 2 852 s) | C | `…:certs/SUMMARY.txt` ; `…:certs/SUMMARY_SYM.txt` |
| cubes | 3 381 UNSAT, 0 SAT, sur 325 cubes par instance. Par instance : m00028_sL0 325 ; m16420_sL1 324 (1 ouvert) ; m23221_s0027 315 ; m21041_s0025 313 ; m23431_s0028 309 ; m06717_s0014 307 ; m20723_s0024 306 ; m12295_s0015 302 ; m04907_s0007 301 ; m05033_s0012 291 ; m29481_s0032 288 | S (comptage par l'agent depuis `results.txt`, égal au journal) | `conway99-c3:main:cubes/*/results.txt` ; `…:NUIT_JOURNAL.md:227` |
| coût restant (caduc) | environ 380 cubes durs × 30-45 min, soit environ 200 heures-CPU, plus 90-180 heures-CPU pour les instances non commencées ; classes 29/43/44/45 de coût inconnu | H (estimation) | `…:NUIT_JOURNAL.md:199-200` ; `…:rapport/plan_calcul.tex:60-68` |
| taille des CNF | environ 607 000 variables et 4,7 M de clauses (encodage initial) ; 1,1-1,4 M de clauses (encodage compact, gain ×20-30) | E | `…:rapport/audit_c3.tex:261` ; `…:NUIT_JOURNAL.md:101-106` |
| Lean | 26 552 déclarations (con-leche, con-ron) ; 26 553 (lean4lean) ; export de 26 582 ; 2 245 tâches de compilation ; 24 fichiers, 3 871 lignes | C (comptes de la machine) ; E (comptage de lignes par l'agent) | `…-experimental:main:logs/comparateur_local_2026-09-23.log:366,371,378,383` ; `…:AUDIT_ENONCE.md:121` |
| \|Aut(Γ)\| | {1, 2, 7, 11} sans ordinateur ; {1, 2} avec BL11 | P conditionnel | `…:pdf/preuve_c3.tex:290-302` |
| littérature | \|Aut\| divise 2·3³·7·11 (MM04) ; seuls 2 et 3 divisent \|Aut\| (BL11) ; 2 \| \|Aut\| ⇒ \|Aut\| \| 42 (Mak10) ; 7 \| \|Aut\| ⇒ Aut ≅ ℤ₇ (CW25) ; aucun sous-groupe d'ordre 6 ou 9 (CM20) ; pas d'ordre 11, 13 ni d'ordre premier > 14 (LM14, non vérifié) | P/E (publiés, non revérifiés) | `…:AUDIT_ENONCE.md:184-192` ; `…:pdf/preuve_c3.tex:87-99,305-307` |
| critère (balayage) | v ≤ 1300 : 7 jeux exclus pour une action libre d'ordre 3, dont (99,14,1,2), (105,52,21,30), (105,52,29,22), (261,52,11,10), (714,248,97,80), (1221,610,279,330), (1221,610,329,280) ; avec points fixes, le critère s'applique à 108 jeux et en exclut 9 (dont 714, 722, 1148) ; T(n) avec 3 \| n ≤ 300 n'est jamais exclu à tort | E | `…:JOURNAL.md:20-25,38-39` |
| hors lot, rapport 02 §6.2 | pour tout graphe de Conway : det L₃ = 7^a·11 ; det L₋₄ = 3²·7^a, avec le même a ; a pair ; 2 ≤ a ≤ 44 ; rang₇(A+4I) = a+1 impair ≤ 45 ; det L₃ ≡ 3 (mod 8) ; invariant d'Arf du code Im(A mod 2) = 1 | [R] non relu | `cw/review/02_symmetry_c3_c7.md:288-316` |
| hors lot, article public rank7 | rang₇(A − 3I) impair, entre 23 et 43, puis 25 comme borne inférieure après calcul | non lu par l'agent (lot L06 ou L09) | `strongly-regular-graphs-research:main:README.md:54` |

### 8.3 Lemmes ouverts et étapes manquantes, et ce qu'ils donneraient

| # | manque | ce que cela donnerait | source |
|---|---|---|---|
| OPN-1 | relecture humaine de la §4 (trois points fixes) et du lemme 7 ; relecture humaine mathématique des §1-3 (celle de Cesarz–Woldar porte sur l'exposition) | statut « relu » pour tout C3 | `memory/cesarz-woldar-collaboration.md:15` |
| OPN-2 | texte publiable : Cesarz–Woldar d'une part, réécriture LAB non relue d'autre part | soumission | `work/c3_review_2026-10-13/REWRITE_NOTES.md:7-13` |
| OPN-3 | vérification des énoncés cités : MM04, B09, BL11, CM20, Mak10, CW25, I26 ; attribution de « \|G\| \| 6 » | corollaire 8, donc \|Aut\| ∈ {1, 2, 7, 11} ou {1, 2} ; puis Aut trivial avec C2 et C7 | `…/REWRITE_NOTES.md:40-43` |
| OPN-4 | lecture humaine de `Challenge.lean` | ferme la chaîne de confiance formelle | `conway99-c3-experimental:main:AUDIT_ENONCE.md:157-160` |
| OPN-5 | correspondance entre les énoncés de la réécriture et les noms Lean | cohérence article et formalisation | `work/c3_review_2026-10-13/REWRITE_NOTES.md:46` |
| OPN-6 | théorème général (critère p = 3, avec ou sans points fixes) | 6 autres jeux de paramètres exclus, et 9 couples (jeu, θ) avec β = 0 | `…:pdf/preuve_c3.tex:321-325` |
| OPN-7 | D4 : obstruction propre au seul quotient Q | preuve sans M ; peut-être transférable hors de l'action libre | `…:IDEES.md:15` |
| OPN-8 | D3 : 5-rang de A+8I pour le graphe de Moore ; PARI absent | exclusion de l'ordre 13 pour Moore 57 ; ordres 11 et 29 pour d'autres jeux | `…:IDEES.md:14` ; `…:JOURNAL.md:40-42` |
| OPN-9 | D8 : invariant de Hasse/Witt du ℤ₃[C3]-module hermitien | obstruction au-delà du discriminant | `…:IDEES.md:19` |
| OPN-10 | route calculatoire : lemmes d'entrées, de type, de triplets et lex à relire ; 35 énumérations non certifiées ; classes 29, 43, 44, 45 | sans objet depuis L04-01 | `conway99-c3:main:rapport/audit_c3.tex:319-327` |
| OPN-11 | vérification Lean non rejouée depuis le 23/09 ; chaîne d'outils rc2 | reproductibilité avant soumission (non demandée explicitement par les sources) | `cw/review/02_symmetry_c3_c7.md:14` |

### 8.4 Méthodes transférables

**Ce que disent les notes.**
- **TR-1 : P1 pour tout premier p.** L'énoncé est « (d₁/p) = (d_ζ mod π / p) » pour une action libre avec un projecteur
  p-entier (`conway99-c3-experimental:main:notes/P1_recollement.md:68-69`), avec les cibles D3 (`IDEES.md:14`).
- **TR-2 : points fixes à quotient de Brauer nul (β = 0)** (`P1_recollement.md:119-127`). Le balayage a donné 9 exclusions,
  toutes pour des jeux d'existence inconnue (`JOURNAL.md:38-39`).
- **TR-3 : lemmes Lean génériques**, pour toute taille, sur ℤ ou ℤ[ω] : `Saturated.lean`, `SaturatedGen.lean`, `GenLemmas.lean`,
  `Step5.lean`, `NumberTheory.lean` (`c3formal/README.md:45-65` ; `cw/review/02_symmetry_c3_c7.md:239`).
  - La réécriture les reformule en quatre lemmes papier : base de noyau, identité de Gram GK = cI pour une forme pondérée D,
    réseau plus un vecteur orthogonal, comparaison sur F₃ (`work/c3_review_2026-10-13/c3_proof_rewrite.tex:170-291`).
- **TR-4 : chaîne SAT de la route calculatoire.**
  - Composants :
    - encodage compact par totalizer tronqué ;
    - cassage lex-leader prouvé ;
    - cube-and-conquer incrémental avec découpage récursif ;
    - `cert_enum.py`, qui certifie la complétude d'une énumération par clauses bloquantes et DRAT ;
    - CNF reproductibles à l'octet ;
    - images Docker.
  - Protocole de validation sur srg(243,22,1,2) et sur la tour 3×3.
  - Sources : `conway99-c3:main:LISEZMOI.md` ; `cw/review/02_symmetry_c3_c7.md:223-233,318-325`.
- **TR-5 : programme linéaire d'incidence agrégée avec vecteurs de Farkas entiers** et vérificateur en bibliothèque standard
  (`check_all.py`). Le rapport 02 propose de le réorienter vers des structures locales de C1 (|X| ≤ 8-10)
  (`cw/review/02_symmetry_c3_c7.md:337-341`).
- **TR-6 : jugement du rapport 02 sur C3 → C1.**
  - « Neither theorem transfers directly » (`cw/review/02_symmetry_c3_c7.md:26`).
  - « Transfer to C1: low ».
  - « [a contradiction needs] a SECOND integral structure with the same reduction. Without a group, none is available from the
    graph itself » (`…:282-286`).

**Ce que voit l'agent (H, à vérifier).**
- **TR-7 : C3 → C1 (cas asymétrique).**
  - Le mécanisme exige deux réseaux entiers dont les réductions modulo un premier sont le même espace quadratique. Ici ce sont
    les deux caractères de C3, puisque Q ≡ M mod (1−ω).
  - Il exige aussi une asymétrie qui n'apparaît que dans l'un des deux, ici le vecteur 1 avec ⟨1,1⟩ = 33 = 3·11. Elle force des
    classes de carrés différentes.
  - Si Aut(Γ) est trivial, il n'y a pas de second caractère : pas d'analogue direct, ce qui concorde avec TR-6.
  - Analogues indirects possibles :
    - **(a) Recollement global.** On recolle L₃ = ℤ⁹⁹ ∩ ker(A−3I) avec son orthogonal ℤ⁹⁹ ∩ (V₋₄ ⊕ ℚ1) dans ℤ⁹⁹ unimodulaire.
      Les formes discriminantes sont anti-isométriques. C'est la théorie du genre, d'où sortent des parités (a pair, rapport 02
      §6.2), mais aucune contradiction connue.
    - **(b) Repères locaux de C1.** Un repère (étoiles, lignes) muni d'une symétrie d'étiquetage ne fournit un côté « M » que si
      la symétrie agit sur tout le réseau propre, donc si elle vient d'un automorphisme. Il ne fournit donc rien en C1.
    - **(c) DISC (C1, autres lots).** C'est déjà un invariant de classe de carrés d'un bloc de Gram. Le seul pont signalé est
      CND-15.
- **TR-8 : C3 → C2 (ordre 2), même algèbre avec ℤ[C2], caractères ±1.**
  - La congruence des discriminants a lieu modulo 2. Or F₂^× = {1}, donc elle ne dit rien.
  - Il faudrait un raffinement 2-adique : type pair ou impair des réductions, oddity, Arf.
  - Il faudrait aussi vérifier la condition β = 0 si l'involution a des points fixes.
  - Piste à croiser avec C2 : le commit `678b61d` du dépôt researcher-2, « Z[C2]-freeness redundancy test: freeness <=> Q = N
    (mod 2) », non lu.
- **TR-9 : comptage des points fixes du lemme 7.** L'étape « un sommet adjacent à deux points fixes est fixe » vaut pour tout
  automorphisme d'ordre premier p ≥ 3 lorsque λ = 1 et μ = 2. En effet une orbite de taille 1 ou p ≥ 3 ne tient pas dans un
  ensemble de 2 voisins communs. Le comptage 15\|F\| ≤ 99 + Σ n_x se transpose aussi, avec n_x ≡ 14 (mod p). Cet outil est
  réutilisable pour d'autres ordres ; C7 est déjà traité par ailleurs.


<!-- ===== L05_Codex.md:1488-1705 ===== -->

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


<!-- ===== L06_C1_arith_LAB.md:478-630 ===== -->

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


<!-- ===== L07_C1_asym_local.md:791-979 ===== -->

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



<!-- ===== L07_C1_asym_local.md:1608-1780 ===== -->

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



<!-- ===== L07_C1_asym_local.md:2099-2238 ===== -->

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



<!-- ===== L07_C1_asym_local.md:2385-2504 ===== -->

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



<!-- ===== L08_C1_exploration.md:752-1087 ===== -->

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


<!-- ===== L10_sessions_memoires.md:421-572 ===== -->

## 11. Matériaux pour la recombinaison

Listes littérales, une entrée par ligne, au format `[ID] énoncé | statut | source`. Statuts tels que donnés par la source. Les entrées tirées d'une source secondaire de ce lot (mémoire, message de commit) renvoient aussi, quand je la connais, à la note finale.

### 11.1 Énoncés conditionnels (« si X alors … »)

- [COND-L10-01] SI (H-MATCH) : tout bloc PSD à quatre étoiles de nullité ≥ 14 a M_1 = h(M_0) et M_3 = h(M_2), ALORS chaque sommet est un point de Hamming, donc (L8) pas de Conway | P (implication, revue indépendante, « modulo L8 » ou Makhnev ou ρ ≤ 191) ; (H-MATCH) O | MEM/loop-mandate-1510.md:42-50 ; W/stars_rank_2026-10-14/H_MATCH_REDUCTION_2026-10-15.md
- [COND-L10-02] SI (N9-NG) : tout bloc PSD à quatre étoiles sans grille sur (l,m) a nullité ≤ 9 + min(c(l), c(m)), ALORS (avec P ≤ 852) pas de Conway | P (vérifié par Codex) ; (N9-NG) O | MEM/n9ng-target-1510.md:15-17
- [COND-L10-03] SI NG5 : « non-grille et ν ≥ 14 ⇒ c ≥ 5 », ALORS (avec P ≤ 852) toute droite a g ≥ 4, t ≥ 8, donc P ≥ 924 > 852 : pas de Conway | P ; NG5 O | MEM/n9ng-target-1510.md:16-17
- [COND-L10-04] SI l'on exclut les ≥ 254 blocs non-grille à min t ≤ 7 que tout Conway possède (NG7, Codex), ALORS pas de Conway (« assez pour les tuer ») | P (NG7) ; exclusion O | MEM/n9ng-target-1510.md:17-18
- [COND-L10-05] SI (SYM) « ker T_S est V4-invariant » ET (QUOT) ν(A++) ≤ 7 + min c, ALORS (N9-NG) ; (SYM) seul donne NG5 quand min c = 1 | P | MEM/n9ng-target-1510.md:45-46 ; SP/msg_n9ng2.txt:3-8
- [COND-L10-06] SI ODDCONST ET EVEN′ (dim P0 ≤ 7), ALORS (N9-NG) sans symétrie | P | MEM/n9ng-target-1510.md:34 ; SP/msg_n9ng.txt:4-5
- [COND-L10-07] SI (B′) : aucun objet PSD à quatre étoiles de rang ≤ 30 avec c = 1, ALORS toute droite de Conway est spéciale (et ODD9 ⇒ (B′)) ; (B′) seul n'exclut pas Conway, il faut (C) | P (implication ; la mémoire du 14/10 écrivait « ⇔ », la revue adverse du 15/10 04:20 a corrigé en « implique seulement ») ; (B′) O ; ODD9 réfuté (L10-74) | MEM/stars-rank-attack-1410.md:23-25 ; MEM/loop-mandate-1510.md:18, :33-35
- [COND-L10-08] SI (SQ30) (classe de carrés 2·3·5·7^e de tout objet PSD de rang 30) ET (N15) (pas de PSD de nullité ≥ 15), ALORS pas de Conway | conditionnel enregistré ; (SQ30) expliqué comme artefact de h ; O | MEM/loop-mandate-1510.md:18-20 ; SP/draft_retour.md:8-10
- [COND-L10-09] SI (T8) « pont transversal t ≥ 8 », ALORS P ≥ 924 > 852 : pas de Conway | conditionnel ; (T8) fragile (nullité 13 vue avec t ≤ 7) | MEM/loop-mandate-1510.md:18-19
- [COND-L10-10] SI Q7 : corank(Q) ≤ 11 − c(l) sur les blocs non-grille, côté min-c, ALORS pas de Conway | P (réduction ; identité de Codex bba12ce) ; Q7 O | MEM/exploration-q7-1610.md:17-21
- [COND-L10-11] SI ODD-PURE (rang D = 9), ALORS Conway exige rang Z ≤ c − 2 ; c = 1 est alors exclu par ODD-PURE seul | P (Codex) ; ODD-PURE O | MEM/exploration-q7-1610.md:25 ; SP/commit_msg_explo4.txt:9-10
- [COND-L10-12] SI R7-NG « bloc PSD non-grille ⇒ rank_F7 ≥ 29 », ALORS pas de Conway (marge 1 dans les données) | conditionnel ; jugé « non crédible » après calibration | MEM/exploration-q7-1610.md:35-37, :52
- [COND-L10-13] SI H46-c1 : G_l connexe ⇒ λ_2(A_H) < 3 (H de 46 sommets), ALORS c(l) = 1 est exclu | P (Conway force λ_2 = 3) ; H46-c1 O | MEM/exploration-q7-1610.md:56-58
- [COND-L10-14] SI 3 ∉ spec Γ_S, ALORS ν(T_S) = nullité(D) et Conway ⇔ D = 0 ; donc SI D ≠ 0 pour tout bloc c = 1, ALORS c = 1 exclu | P (identité exacte) ; O | SP/codex_transcript_2.txt:26-30, :106
- [COND-L10-15] SI c(l) = 1 sans lemme ⇒ ν ≤ 13, ALORS c = 1 exclu (= (B′)) | O | MEM/c1-line-c1-target-1710.md:11-13 ; SP/codex_transcript_2.txt:87
- [COND-L10-16] SI R8 (quatre étoiles + les 8 labels {4,t}) est UNSAT, ALORS pas de Conway, à tout rang | P (soundness auditée le 20/10) ; R8 O | SP/commit_msg_r8.txt:1-4 ; MEM/r8-target-1610.md:20
- [COND-L10-17] SI tout graphe de droite admissible à ≤ 7 triangles transversaux a un sommet proche x hors d'eux dont le système d'étoile est UNSAT dans toute variante de rang 37, ALORS aucun srg(99,14,1,2) n'a rank_7(A − 3I) = 37 | P (théorème 6.1, seule entrée P ≤ 852) | SP/commit_msg_thm.txt:3-6
- [COND-L10-18] SI « toute boule de tout type de droite meurt » au rang 37, ALORS rang 37 exclu sans lemme global (chaque type a son test d'étoile) | P (correction 17.93) | MEM/c1-start.md:533
- [COND-L10-19] SI un lemme force au rang 37 une droite d'un type rare (par exemple dans une grille : 1,4e8 boules), ALORS une couverture par un petit balayage suffirait | proposé, aucun prouvé | MEM/c1-start.md:533
- [COND-L10-20] SI 27 828 τ_g + 31 976 τ_n + (canaux hors C6) < 17,1 millions, ALORS rang 37 exclu (τ_g < 614 seul, τ_n < 535 seul) | H (LP flottant) | MEM/c1-start.md:347-349
- [COND-L10-21] SI aucune droite n'est dans 4 ou 6 grilles (g(droite) ≤ 3), ALORS paires de grilles sur une droite ≤ 6ρ, τ ≤ P ≤ 853, budget par paire de jumeaux doublé (~30 000) | H (LP « what-if ») | MEM/c1-start.md:216-219
- [COND-L10-22] SI 3 320 240 k18 + 2 716 560 k20 + 740 880 k22 + 226 380 k24 (+ types hors graine) < 15 241 977 (k_n = nombre maximal de vecteurs propres de norme 2n par graine), ALORS rang 37 impossible ; par exemple (2,2,2,4) suffit | conditionnel ; route des graines FERMÉE ensuite (trois vecteurs de norme 18 par graine localement possibles) | MEM/c1-start.md:238-243, :276-277
- [COND-L10-23] SI b_4 ≥ 18M, ou b_3 ≥ 300k avec b_4 ≥ 12M, ALORS rang 37 meurt (prouvé : 24 948 et 2,73M) | H (table « what-if ») | MEM/c1-start.md:129-131
- [COND-L10-24] SI b_2 < 968, ou 2a_8 + 16a_9 + a_13 < 2632, ou b_3 < 6 696 790, ALORS rang 43 exclu | identités de LAP reproduites par Codex | MEM/c1-start.md:187-189
- [COND-L10-25] SI aucune 22-coclique n'existe, ALORS a_7 = 0 à tout rang (tout vecteur de Fano contient deux 22-cocliques se coupant en 15 points) ; « d'où b_1 ≤ 44 à tout rang » (Codex) | P (LAP, Codex) | MEM/c1-start.md:190-192
- [COND-L10-26] SI N16 et N18 sont établis au rang 37 ET au plus 4 vecteurs de norme 20 par graine indépendante (a_10 ≤ 31 680 < 34 418), ALORS rang 37 exclu | conditionnel (identité 17.100) | MEM/c1-start.md:541-542
- [COND-L10-27] Rangs 37, 39, 41 exigent un vecteur de norme 18 ou 26 ; rang 43 exige norme 18 ou 26, ou ≥ 1316 vecteurs de norme 16 ; donc SI les normes 18 et 26 sont exclues (et < 1316 de norme 16 au rang 43), ALORS C1 exclu | chemin critique (identité de la section 15 + a_8 ≤ 6930) | MEM/c1-start.md:543
- [COND-L10-28] SI rang 37 et P = 0 et si les profils (4,8), (6,6), (4,4,4) meurent tous, ALORS toute droite est connexe | conditionnel ; (4,8) : 81 380 morts, 16 516 TORSION | MEM/c1-start.md:470-471, :501
- [COND-L10-29] Rang 37 ⇔ la matrice de Seidel J − I − 2A a 7-rang 36 ; rang 37 ⇔ Π_T 7-entier | P (reformulations) | MEM/c1-start.md:532 ; SP/commit_msg_obstr.txt:10-11
- [COND-L10-30] Au plus 32 droites à c ≤ 2 ⇒ il existe une racine dont les 7 droites ont c ≥ 3 ; sinon chaque sommet est sur une droite à c ≤ 2 | P (dichotomie) | SP/msg_plan.txt:3-4
- [COND-L10-31] P ≤ 852 ⇒ au moins 18 droites avec t ≤ 7 ; t ≤ 7 ⇒ c ≤ 4 et un x utilisable | P | MEM/rank37-finite-route-2010.md:12 ; SP/commit_msg_thm.txt:6-7
- [COND-L10-32] SI c_min ≥ 3, ALORS chaque sommet appartient à au moins une grille (racine sans grille exclue par parité) | P (dossier externe, non relu) | SP/ext_cmin3_2026-10-18/conway_cmin3_recherche/NOTE_RECHERCHE_CMIN3.md:100-106
- [COND-L10-33] SI les 3 gabarits R1G (23 Gram) sont fermés, ALORS les racines à exactement une grille (sept droites à c ≥ 3) sont exclues — un lemme de plus, pas l'exclusion de c_min = 3 | conditionnel | SP/ext_cmin3_2026-10-18/conway_cmin3_recherche/NOTE_RECHERCHE_CMIN3.md:236-238
- [COND-L10-34] SI l'on prouve qu'au plus neuf paires de fonctions propres de taille 11 ou 12 peuvent coexister, ALORS C2 est fermé (contradiction avec l'identité paires(11) + paires(12) = 10 + N_2/2 ≥ 10) | E (identités, L10-118, sous-agent non relu) ; « au plus neuf » O | MEM/mission-c2-without-compute.md:27
- [COND-L10-35] NOT-EX (C2) ⇐ théorème R + forçage modulaire (E ≤ 12) + « aucune fonction propre (−4) σ-impaire entière de somme des carrés 8..12 » ; lemmes 8, 9, 10 = T16, T18, T20 ; 11, 12 manquent | conditionnel | MEM/mission-c2-without-compute.md:19
- [COND-L10-36] Le cadre des cocliques (22 et 21) ne ferme C1 qu'avec une preuve de α ≥ 21 | P (logique) | MEM/asymmetric-srg-campaign.md:80 ; SP/msg_cq.txt:3-4
- [COND-L10-37] SI « tout srg λ = 1 a un automorphisme d'ordre 3 » (conjecture (S3)), ALORS pas de Conway (avec C2, C3) | conditionnel ; aucun mécanisme | SP/commit_msg_treasure.txt:4-6
- [COND-L10-38] SI (P) « toute arête est dans un prisme », ALORS au moins 231 prismes à 99, ce qui exclut le profil sans prisme (torsion maximale) | conditionnel ; (P) vrai sur les 8 srg(243) | SP/note_part3.md:51-53
- [COND-L10-39] SI une pièce FORCÉE dans un Conway a plus de symétries que de complétions, ALORS C1 exclu ; une pièce forcée à complétion unique doit être rigide | P (principe de symétrie forcée) | SP/note_part2.md:132-134
- [COND-L10-40] SI les droites extérieures sont déterminées par les couplages en un sommet, ALORS tout système de couplages d'un Conway est rigide sous W(B7) | conditionnel (vrai à symétrie près dans les 4 srg(243) à forte torsion) | SP/note_part2.md:127-131
- [COND-L10-41] SI F_x est invariant par un flip (Aut = 1), ALORS F_x a au moins deux complétions | P | SP/note_part3.md:40-41
- [COND-L10-42] SI à trois étoiles « rang 30 ⇒ grille », ALORS chaque sommet est de Hamming, contradiction (L8) | R (z2b, 14/10) | SP/msgs_1800.txt:3-4, :26-28
- [COND-L10-43] SI « toute relation à trois étoiles vient des deux étoiles de la droite », ALORS route finie (bases « décomposables », ~4e8 à symétrie près) ; version faible : au moins un des 693 couples (sommet, droite) décomposable | conditionnel ; O | SP/msgs_1800.txt:102-105, :128
- [COND-L10-44] Sous un automorphisme non trivial, toute recherche est vouée à l'échec : C2 + C3 (Lean) + C7 (+ Behbahani-Lam) ⇒ un Conway est asymétrique | P avec dépendances (C2 assisté par ordinateur, C3 formalisé, C7 manuscrit) | SP/notes_part1.md:39 ; MEM/user-preferences-c2.md:51-57
- [COND-L10-45] Un étalement régulier n'existe qu'aux ordres 9 et 243 de la famille srg(v,k,1,2) : à 99 il donnerait srg(33,12,1,6) de multiplicité 44/7 | P | MEM/asymmetric-srg-campaign.md:50
- [COND-L10-46] SI une involution existe, ALORS rank_F2(Γ̄ + Nb Nbᵀ) = 20 avec Γ̄² + Γ̄ = Nb Nbᵀ sur F2 | P (esquisse, Broué) | MEMB/conway99-research-state.md:19
- [COND-L10-47] SI tous les D-carrés sont « sibling », ALORS contradiction (théorème D, C2) | P (vérifié par Astra) | MEMB/conway99-research-state.md:48-50
- [COND-L10-48] SI 3 ∈ spec(Γ_S) (cas des objets de rang 30), ALORS la formule de la résolvante ne s'applique pas telle quelle | constat | SP/codex_transcript_2.txt:77
- [COND-L10-49] À quatre étoiles, srg(v,k,1,2) force 5k − 16 − g relations au-delà des étoiles : 10 pour Conway, aucune pour les autres paramètres λ = 1, μ = 2 (les calibrations à 243 ne transfèrent donc pas) | P | MEM/calibrate-local-laws-on-243.md:21-22

### 11.2 Bornes quantitatives

- [BORNE-L10-01] prismes : P ≤ 852 (positivité, recensement d'ordre 9 ; certificat exact, revérifié le 18/10) | C | MEM/c1-start.md:135-136 ; MEM/c-le-3-audit-1810.md:34-36
- [BORNE-L10-02] prismes : P ≤ 1151 (L16, Krein) ; ≤ 1150 (rayon spectral du graphe des prismes < 10, Codex 14/10) | P | SP/morning_report_draft.md:30 ; SP/notes_journal.md:7
- [BORNE-L10-03] prismes et grilles : 3P + 4G ≤ 2772 (Codex) | C (vérifié exactement) | MEM/c-le-3-audit-1810.md:38-39
- [BORNE-L10-04] grilles : ρ ≤ 126 (ordre 9) ; ≤ 191 grilles (de P ≤ 1150) ; au plus 11 grilles deux à deux disjointes | C ; P | MEM/c1-start.md:135 ; SP/morning_report_draft.md:30 ; SP/worknotes_part1.md:9
- [BORNE-L10-05] P + 5ρ ≤ 1386 ; 4N(F10) + 75P + 96ρ ≤ 84 546 ; a_7 + 13ρ ≤ 2013 | certifiés (Codex) | MEM/c1-start.md:252, :299-300
- [BORNE-L10-06] jumeaux : τ ≤ 1890 → 1534 → 1403 → 1354 ; τ ≤ P + 5ρ + 17 ; 17τ ≤ 17P + 105ρ ; τ ≤ (P − 6ρ) + #paires de grilles partageant une droite | certifiés (Codex) / P (LAB) | MEM/c1-start.md:209, :216, :245, :257, :359
- [BORNE-L10-07] nombre de prismes p d'une droite : 0 ≤ p ≤ 12, n_0 = 32 − p, n_1 = 144 + 3p, n_2 = 36 − 3p ; p̄ ≤ 588/59 < 10 | P | MEM/night-mandate-1410.md:23
- [BORNE-L10-08] fenêtre de rangs : r = rank_7(A − 3I) ∈ {37, 39, 41, 43} (08/10) ; rank_F7(A + 4I) ≥ 35 (nuit 14/10, redécouverte) | C | MEM/c1-start.md:118 ; MEM/night-mandate-1410.md:40
- [BORNE-L10-09] min(L1) ≤ 16/20/24/26 pour r = 33/35,37/39,41/43 ; puis ≤ 18/20/24/24/26 pour r = 35/37/39/41/43 | C | MEM/c1-start.md:51, :70
- [BORNE-L10-10] vecteurs de M : b_1 ≤ 3784 ; b_2 ≥ 462 ; b_3 ≥ 24 948 → 43 848 → 45 898 → 45 964 ; b_4 ≥ 1 431 738 → 2,73M → 3 371 634 ; b_5 ≥ 34 087 368 ; twin-safe b_4 ≥ 3 826 746 − 30P − 4572ρ | C / P | MEM/c1-start.md:62, :67-69, :109, :136-137, :251, :359
- [BORNE-L10-11] vecteurs de L1 : a_7 ≤ 7920 → 990 → 842 ; a_8 ≤ 27 720 (≤ 4 vecteurs de norme 16 par graine) ; 7a_7 + 8a_8 ≤ 55 440 ; a_7 ≤ 347 au sommet grille (via N(F10) ≤ 3648) | P / C | MEM/c1-start.md:61, :68, :83, :112, :174, :287
- [BORNE-L10-12] plafonds au rang 37 : b_4 ≤ 16,5M → 15 975 390,7 → 15 972 863,3 ; couplé ≤ 16 851 675,0 ; b_4 + (651/34) b_3 ≤ 17,4M | C (Codex note 194/196) | MEM/c1-start.md:138, :150, :222, :251
- [BORNE-L10-13] identité du rang 37 : 350a_8 + 91a_9 + 13a_10 ≥ 447 412 (après N14, b_3 ≥ 45 898) ; ≥ 22 vecteurs de normes 16-20, ≥ 574 de norme 20 si 16 et 18 absents | E | MEM/c1-start.md:540-541
- [BORNE-L10-14] rang 37 : 539a_9 + 392a_10 + 147a_11 + 49a_12 ≥ 15 241 976,8 (côté L1 seul) | E | MEM/c1-start.md:238-239
- [BORNE-L10-15] collisions de masse six par paire de grilles sur une droite : 27 828 / 27 818 / 27 810 / 27 798 (pinceaux 2/3/4/6) ; plancher certifié 16 496 ; C6 ≤ 39 016 712 → 38 084 490 ; prisme-libres : 6992 ≤ C_pf ≤ 18 244 | certifiés (Codex) | MEM/c1-start.md:280-282, :312-314, :359
- [BORNE-L10-16] vecteurs propres entiers −4 : norme ≥ 14 (= co-Heawood) ; |f·g| ≤ 6 ; familles orthogonales ≤ 28 puis ≤ 12 ; au plus 7920 co-Heawood ; au plus 360 360 de norme 16 | P (Codex, LAB) | SP/morning_report_draft.md:11-12, :32 ; SP/notes_journal.md:10-12
- [BORNE-L10-17] vecteurs propres entiers −5 à 243 : norme ≥ 24 (argument non relu) ; 3-vecteurs propres entiers à entrées ≤ 2 : support ≥ 12 | P | MEM/c1-start.md:35 ; SP/msg_night13.txt:3-4
- [BORNE-L10-18] 9-ensembles : au plus 16 arêtes sauf grille 3×3 (aucun à 17) | P | SP/msg_night5.txt:3-5
- [BORNE-L10-19] coeurs : norme 14 : 1 ; 16 : 5 ; 18 : 26 ; 20 : 1199 + 182 | E | MEM/c1-start.md:539
- [BORNE-L10-20] mondes : 800 427 bases (33 508 orbites) pour la norme 14 au rang 37 ; 71 351 mondes PSD sur 5 attaches d'un coeur de norme 16 (60 936 de rang 33) | E | MEM/c1-start.md:535, :538
- [BORNE-L10-21] graphes de droite : 187 381 435 694 classes ; 147 579 095 390 admissibles ; 147 577 214 193 admissibles avec t ≤ 7 ; ~1,5e11 types connexes ; ~7e7 avec c = 2 ; ~2e5 avec c = 3 | P/E | SP/commit_msg_enum.txt:1-6 ; SP/commit_msg_boost.txt:15-16
- [BORNE-L10-22] coûts : test rang 37 ~6e4-6,5e4 cœur-heures ; R8 pur 5e7-1e12 (2e4-4e8 avec cassage idéal) ; C2 E = 11 : 1e9-5e9 nœuds, E = 12 ~1e12 ; route C2 ~6700 CPU-h | H | L10-106 ; L10-109 ; L10-119 ; L10-15
- [BORNE-L10-23] gabarits : c_min = 3 : 510 926 gabarits, 10 052 ouverts (→ 35) ; c_min = 2 : 1 793 745 mesurés, 119 452 ouverts (k = 4 partiel) ; k = 4 seul 1 445 038 ; c ≤ 2 ~1e7 à symétrie près ; m = 2 : 3 443 556 gabarits de racine (k = 4..11) ; configurations étiquetées : 3,9e10 (c ≥ 3), 1,27e7 (c ≥ 4) ; c4 : 76/79 | E / H | SP/msg_c3.txt:1-5 ; SP/msg_c21.txt:3 ; MEM/c-le-3-audit-1810.md:32, :64 ; SP/commit_msg_reduction.txt:19 ; SP/msg_plan.txt:5
- [BORNE-L10-24] familles fermées : K3 2 742 342 bords ; 2K2 12 569 bords ; P3NB 137 454 bords, 824 450 attaches ; K2BC 1261 bords, 301 936 attaches ; 2K2N 816 classes × 8 marques | C | L10-95 à L10-100
- [BORNE-L10-25] c = 1 (données) : marge générique ν = 4 (Conway exige 14) ; sans lemme ν ≤ 7 ; Conway exige dim ker F ≥ 12 (données 5..8) ; corank(Q) ≤ 7 sur les non-grille (Conway exige ≥ 12 − c) | E / H | SP/codex_transcript_2.txt:82-84 ; MEM/exploration-q7-1610.md:20-22, :55-56
- [BORNE-L10-26] blocs non-grille : ≥ 396 dans tout Conway ; ≥ 254 avec min t ≤ 7 (NG7) ; ≥ 4 paires cassées par sommet (G18) ; ≥ 336 des 2079 drapeaux (v,{l,m}) ont ≥ 4 relations mixtes | P | MEM/MEMORY.md:39 ; MEM/n9ng-target-1510.md:17 ; MEM/loop-mandate-1510.md:56 ; SP/notes_journal_p4.md:6
- [BORNE-L10-27] quadrangles : 2079 ; chaque arête dans 12 quadrangles ; complexe des quadrangles de caractéristique d'Euler 1485 ; un quadrangle a exactement 44 voisins extérieurs | P | MEM/c1-start.md:509, :512, :519
- [BORNE-L10-28] rubans de transport fermés propres : m ∈ {3,4,5} ; segments ouverts ≤ 4 centres | C | MEM/c1-start.md:521-523
- [BORNE-L10-29] 243 : |Aut| = 3 849 120 (BvLS), 4320, 864, 3888, 2916, 108, 162, 108 ; prismes 8910, 2430, 4158, 5670, 4536, 3240, 3186, 3834 ; grilles par sommet 55 ; 13/19/55 ; 23 ; 31 ; 25 ; 17 ; 17 ; 19 | C | SP/sf/table8.md:3-10
- [BORNE-L10-30] 243 : coclique de Hoffman (45) seulement dans BvLS ; ≤ 44 paires plates par sommet dans une peau S3 ; code de parité de dimension 460, distance duale ≥ 6 ; Z3-revêtements : 1154 solutions au signe près | S / P / E | L10-47 ; L10-40 ; L10-37
- [BORNE-L10-31] λ = 1 : srg(378,52,1,8) de groupe minimal 6 (hémisystèmes) ; concentration P_ii P_jj ≥ 1/(2(r − s))² (1/900 à 378) ; un échange sur le graphe S3 demande ~280 sommets libres | C / P | L10-55
- [BORNE-L10-32] srg(25,12,5,6) : 15 graphes, groupes 600, 72, 72, 6 ×4, 3 ×2, 2 ×4, 1 ×2 ; srg(9,4,1,2) : 72 | E | L10-50
- [BORNE-L10-33] ordre 7 : 2n3 ≤ z11 ≤ 4n3, 4 | z11, n3 ≤ 4158 ; intervalle du dépôt public 708 ≤ n3 ≤ 4158 | E | MEMB/conway99-research-state.md:14, :16
- [BORNE-L10-34] ordre 6 : un paramètre libre, 9P + 275 371 866 ; types d'ordres 2..6 : 2, 4, 9, 21, 62 ; ordres 7/8/9/10 : 208/916/5311/42 430 types | E | SP/commit_msg_enonce.txt:9-10 ; MEM/c1-start.md:133-134, :161
- [BORNE-L10-35] C2 : s = 12 + N2 ≥ 12 paires de fonctions caractéristiques ; ≥ 10 paires de taille 11 ou 12 ; identités sur 1042/1042 paires de régions | E | L10-118
- [BORNE-L10-36] C2 route C : 220 260 576 paires dans 91 réseaux en flux ; 32 265 417 paires différées à un jumeau ; ≤ 2 479 669 paires à recertifier (11 234 représentants y1, 5 130 tranches) | E | MEM/route-c-campaign-resume.md:82, :129-133
- [BORNE-L10-37] symétries : |Aut| ∈ {1, 2, 3} (21/09) ; sans ordinateur |G| ∈ {1, 2, 11} (remarque d'asymmetric.tex) | P | L10-2 ; SP/notes_part1.md:39
- [BORNE-L10-38] entropie : log10 des solutions attendues par G_T étiqueté −27 (L1) / −48 (L1-L3) pour Conway ; +32 à +50 pour srg(243) | H | SP/commit_msg_reduction.txt:12-13
- [BORNE-L10-39] dossier externe c_min = 3 : 83 cadres ; 648 codes → 29 → 13 classes ; R1G : 83 → 3 gabarits, 7371 → 27 → 23 Gram ; 483 témoins de coins ; 1467 b-facteurs ; 1446-1610 arêtes fixées sur 3486 | C | L10-103
- [BORNE-L10-40] H46 : det(3I − A_H) = −16 200 Δ ; écart de λ_2 à 3 jusqu'à 0,0073 ; ODD9-NG : écart jusqu'à 0,0071 (puis 3,1e-6 en marches impaires) | E | SP/msg_c1.txt:6-7 ; MEM/exploration-q7-1610.md:59 ; MEM/n9ng-target-1510.md:36 ; SP/msg_n9ng2.txt:10-11

### 11.3 Lemmes ouverts ou étapes manquantes (et ce qu'ils donneraient)

- [OUVERT-L10-01] (H-MATCH) → pas de Conway (COND-L10-01) | MEM/hmatch-t3-1510.md:12-13
- [OUVERT-L10-02] (N9-NG) ou NG5 → pas de Conway avec P ≤ 852 ; (SYM), (QUOT) → (N9-NG) | MEM/n9ng-target-1510.md:15-18, :45-46
- [OUVERT-L10-03] (B′) / « c(l) = 1 sans lemme ⇒ ν ≤ 13 » → c = 1 exclu ; puis l'énoncé (C) pour le cas « toute droite spéciale » | MEM/c1-line-c1-target-1710.md:11-13 ; MEM/loop-mandate-1510.md:18
- [OUVERT-L10-04] Q7, ODDCONST, SYM6, ODD-PURE, H46-c1 → exclusion (COND-L10-10 à -13) | MEM/exploration-q7-1610.md
- [OUVERT-L10-05] D ≠ 0 pour tout bloc c = 1 à quatre étoiles, et traitement du cas 3 ∈ spec Γ_S → c = 1 exclu | SP/codex_transcript_2.txt:106
- [OUVERT-L10-06] R8 UNSAT (ou CEGAR) → pas de Conway à tout rang | SP/commit_msg_r8.txt
- [OUVERT-L10-07] rang 37 : générateur exhaustif, moteurs torsion et déconnecté, types (1,4), (2,4), d ≥ 5, certificats UNSAT (LRAT), filtre réel exact → rang 37 exclu par le théorème 6.1 | MEM/rank37-finite-route-2010.md:16 ; SP/commit_msg_thm.txt:8-11
- [OUVERT-L10-08] rangs 39, 41, 43 : un théorème (toutes les méthodes linéaires bornent par en bas) | MEM/rank37-finite-route-2010.md:17-25 ; SP/commit_msg_borne.txt:3-6
- [OUVERT-L10-09] N16, N18 au rang 37 + au plus 4 vecteurs de norme 20 par graine → rang 37 (COND-L10-26) ; exclure les normes 18 et 26 → rangs 37-41 (COND-L10-27) | MEM/c1-start.md:541-543
- [OUVERT-L10-10] une borne inférieure du rang en fonction du nombre de paires de jumeaux ; « aucune droite dans 4 ou 6 grilles » ; « un prisme non-grille a au plus un jumeau » (→ 20,2M) ; borne sur le nombre de PAIRES de supports de même projection | MEM/c1-start.md:218-219, :346-347, :459, :528
- [OUVERT-L10-11] NT et « toute droite déconnectée » (chaîne de septembre, après (a′) uniforme) → rang 37, qui est le cas d'égalité R_L = 0 de l'identité de septembre | MEM/c1-start.md:375-377, :407
- [OUVERT-L10-12] conjecture c(Q) = somme des quatre c_e mod 2 pour tout quadrangle | MEM/c1-start.md:516
- [OUVERT-L10-13] registre c3 : 35 gabarits ouverts (7 en P3, 19 sans paire partagée forcée, 9 autres) → c_min = 3 exclu (sous budget 51) | SP/commit_msg_2k2nbc.txt:15-18
- [OUVERT-L10-14] gabarits c4 7, 9, 19 (rouverts) → branche c ≥ 4 close (76/79 → 79/79) | SP/codex_27ac387d/notes/RECALCUL_C4_2026_10_18.txt:4-5
- [OUVERT-L10-15] R1G-09, R1G-46, R1G-47 (15 + 4 + 4 Gram) → racines à une grille exclues (COND-L10-33) | SP/ext_cmin3_2026-10-18/conway_cmin3_recherche/NOTE_RECHERCHE_CMIN3.md:236-238
- [OUVERT-L10-16] noyau dur c ≤ 2 : 74 gabarits ; 2 302 537 classes c = 1 survivant à FG ; k ≤ 3 non énuméré | SP/commit_msg_hc5.txt ; SP/commit_msg_lem2.txt:10-12
- [OUVERT-L10-17] C2 sans calcul : lemmes T22, T24 ; ou « au plus neuf paires » → preuve de NOT-EX sans la passe des 156 réseaux | MEM/mission-c2-without-compute.md:19, :27
- [OUVERT-L10-18] C2 : recertification de la règle de transfert « jumeau » (≤ 2 479 669 paires) → retirer la phrase de réserve des articles ; formalisation Lean | MEM/route-c-campaign-resume.md:126-146
- [OUVERT-L10-19] existence d'un srg(243,22,1,2) asymétrique ; « les couplages en un sommet déterminent-ils le graphe ? » (proposition (a)) | SP/note_part3.md:44-49 ; MEM/asymmetric-srg-campaign.md:72
- [OUVERT-L10-20] conjectures (P), (G), (E), (L2) des notes 176-177 ((P) → ≥ 231 prismes à 99) | SP/note_part3.md:51-53
- [OUVERT-L10-21] « toute relation à trois étoiles vient des deux étoiles de la droite » (ou sa version faible) → route finie | SP/msgs_1800.txt:102-105, :128
- [OUVERT-L10-22] coexistence globale des ≥ 4 blocs cassés par sommet (G18) : pilote global proposé par Codex | MEM/hmatch-night-1610.md:28-30
- [OUVERT-L10-23] cinq étoiles plain (UNKNOWN) → s'il est UNSAT, pas de Conway (la cinquième étoile est une relaxation) | MEM/ext84-fivestar-1610.md:25 ; MEM/r8-target-1610.md:20
- [OUVERT-L10-24] certification : réimplémentation de l'encodage S3 ; DRAT de T1 et kk6 (~3 h) ; lecture indépendante de la preuve des coupes de continuation (2K2) | MEM/asymmetric-srg-campaign.md:68 ; MEM/night-mandate-1410.md:34 ; SP/commit_msg_0525.txt:4-6
- [OUVERT-L10-25] série thêta à vecteur marqué (forme de Jacobi) sur le cœur de norme 18 | MEM/c1-start.md:544
- [OUVERT-L10-26] conjecture (S3) pour les srg λ = 1 → Conway (COND-L10-37) | SP/commit_msg_treasure.txt:4-6
- [OUVERT-L10-27] cas involution : configurations mixtes (paires/chaînes tordues ≥ 4, mélanges, carrés disjoints) au 25/09 — devenu sans objet après la route C | MEMB/conway99-research-state.md:64, :100, :113

### 11.4 Méthodes transférables (d'un cas à un autre)

- [TRANSFERT-L10-01] Méthode de C3 (discriminants des réseaux propres, Gram sur Z[ω], premier 11) → C2 (25/09) : critère det(Λ_θ)_impair ≡ 1 + f/v mod 4, ne redonne que le théorème A | MEMB/conway99-research-state.md:101-108
- [TRANSFERT-L10-02] Noyau commun de C3, C7, C2 : « une identité quadratique sur un PETIT objet entier » ; le transfert direct de C3 (gains Z3, A_s² + A_s = 12I) à C1 est impossible | SP/commit_msg_repr.txt:12-13, :22-23
- [TRANSFERT-L10-03] Route C de C2 (catalogue fini de 156 enveloppes par calcul) → C1 : « une route (C) pour C1 ? » (note 156 de Codex) ; l'utilisateur : C2 a demandé trois routes, la finie était la réaliste | MEM/feedback-several-routes.md:8-20
- [TRANSFERT-L10-04] Technique T16/T18/T20 (sans σ-imparité) pour minorer min(L) en C1 — déjà close par la note 110 | MEM/c1-start.md:27-38
- [TRANSFERT-L10-05] Formes modulaires de C2 (résultat 2, identités exactes) → C1 : série thêta à vecteur marqué (forme de Jacobi) proposée le 13/10 | MEM/c1-start.md:544
- [TRANSFERT-L10-06] Méthode de Codex (liste finie énumérée, fermée cas par cas par solveurs, dissection des survivants) → c ≤ 3 (LAB) ; générateur c ≥ 4 de Codex étendu à c ≤ 3 | MEM/feedback-enumerate-not-conditionals-1710.md:11-18 ; SP/msg_cle3.txt:1-5 ; SP/codex_transcript_2.txt:7
- [TRANSFERT-L10-07] Lemme d'équilibre (note 23 §8, spécifique à k = 14) : utilisé en C2 (lemme de la queue, 25/09), puis en C1 (16-17/10) | MEMB/conway99-research-state.md:109-112 ; MEM/ext84-fivestar-1610.md:28
- [TRANSFERT-L10-08] srg(243,22,1,2) comme banc d'essai → lois locales de Conway : à vérifier (forcer le même phénomène au même niveau d'étoiles ; 5k − 16 − g) | MEM/calibrate-local-laws-on-243.md:24-28
- [TRANSFERT-L10-09] Contrôle positif CP sur un vrai srg(243) avant tout verdict d'un nouvel encodage | MEM/feedback-cp-positive-control.md:21-27
- [TRANSFERT-L10-10] Principe de symétrie forcée (Paley, 243) → cadres coclique / co-Heawood de Conway | SP/note_part2.md:132-134, :141-142
- [TRANSFERT-L10-11] Critère de concentration (rigidité des échanges) : valable pour tout srg | SP/msg_l5.txt:3-5
- [TRANSFERT-L10-12] Compléments étoilés (Milošević pour (57,14,1,4), route Ω) ; symétrie forcée de Bondarenko-Radchenko (λ = 1, g = k) ; représentation euclidienne (BPR 76) | MEM/biblio-c1-1710.md:10-15
- [TRANSFERT-L10-13] Positivité de Gegenbauer (Liao-Wang-Yu-Cai) testée sur (99,14,1,2) : aucune contrainte nouvelle sur P | SP/commit_msg_enonce.txt:3-6
- [TRANSFERT-L10-14] Flag-algebras de Razborov sur recensement exact (contrôle à 243) | SP/commit_msg_treasure.txt:11-13
- [TRANSFERT-L10-15] Chaîne de certification DRAT/RUP (drat-trim) : S3, kk5, 2K2, K3, P3NB, K2BC, 2K2N | L10-38, L10-60, L10-95 à L10-100
- [TRANSFERT-L10-16] Estimateur de Knuth pour chiffrer une recherche avant de la lancer (utilisé pour c ≤ 2 : ~1e7 gabarits ; question S3 : ~5e18 nœuds ; co-Heawood : ~3e22 secondes lignes par base) | MEM/c-le-3-audit-1810.md:64 ; MEM/asymmetric-srg-campaign.md:35 ; MEM/c1-start.md:543 ; MEM/night-mandate-1410.md:25
- [TRANSFERT-L10-17] Formulation F3 de Codex (revêtements Z3) → question S3 (revêtements non abéliens de BH) | MEM/asymmetric-srg-campaign.md:32-35
- [TRANSFERT-L10-18] Énumération par lignes candidates (`row_clique.py`, `boundary_census.py`) : générale pour tout ensemble gardé ; limite pratique ~40-50 sommets gardés | MEM/asymmetric-srg-campaign.md:62, :72
- [TRANSFERT-L10-19] Énumération canonique des graphes de droite (groupes A_λ, Burnside) : prête pour tout type de droite | SP/commit_msg_enum.txt:3-6
- [TRANSFERT-L10-20] Z[C2]-liberté ⇔ Q ≡ N (mod 2) : la parité mod 2 de (C5) ; la même lecture « recollement à 2 » pourrait servir pour tout automorphisme d'ordre 2 | W/Z_C2_FREENESS_REDUNDANCY.md:40-61

