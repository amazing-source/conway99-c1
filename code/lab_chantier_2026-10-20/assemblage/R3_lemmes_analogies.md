# R3 — Lemmes ouverts × preuves ailleurs, analogies entre cas, incohérences

Agent R3, phase de recombinaison du chantier du 20/10/2026. Lecture seule. Matériau lu en entier : `MATERIAUX_BRUTS_partiel.md`
(lots L01 à L08 et L10, 2 755 lignes) et `MATERIAUX_BRUTS_L09.md` (lot L09, 666 lignes). Sources ouvertes pour vérifier
chaque lien : voir la colonne « source » de chaque entrée. Les 48 entrées sont dans `R3_lemmes_analogies.jsonl`
(identifiants R3-01 à R3-13, R3-20 à R3-29, R3-40 à R3-48 ; **seconde passe** sur les lots L11a à L11f du pont, matériau
`MATERIAUX_BRUTS_L11.md` : R3-49 à R3-64, section 7). Les passages de la première passe que la seconde corrige portent la
mention *[seconde passe : …]*.

Conventions : r = rang₇(A − 3I) (équipe) ; k = r − 15 ; r_ext = rang_F7(2A − J + I) (dépôt externe) ; n3 externe =
nombre de N3 induits = 4158 − 3P. Les statuts sont ceux des sources ; je ne rehausse aucun statut. « Vérifié » veut dire :
j'ai lu l'énoncé et la preuve à la source et contrôlé que les définitions s'emboîtent.

## 1. Résumé

1. **Aucun lemme ouvert dont la preuve ailleurs exclurait C1, un rang ou un cas.** Aucune combinaison trouvée n'est une
   exclusion.
2. **Deux liens nouveaux et vérifiés, de potentiel « réduction » :**
   - **R3-02.** Au rang 37, le lemme N14 (pas de vecteur propre −4 entier de norme 14 ; E, non audité) vide la famille
     co-Heawood que V15 §79 laisse ouverte. À ce rang, tout bord positif de 43 sommets se complète donc en au plus deux
     affectations de signes par facteur. Même chose dans la branche S₀ du rang 43. *[seconde passe : la vérification V1
     conclut « tient avec réserves ». Le gain est mince : §79 donne déjà au plus une complétion. Le volet du rang 43 vaut pour
     toute la branche b₁ = 0, avec le statut P (R3-63).]*
   - **R3-01.** Le critère DISC n'admet que la classe 2 (T8) et la classe 1 (U15), car k est pair (L4). Le code de Codex
     (`conway_core_repair.py:36`) accepte encore 14 et 7. Le filtre est sain mais plus faible que le théorème. La
     mathématique est déjà dans la note LAB du 15/10 ; l'écart avec le code est nouveau.
3. **Un lemme déclaré ouvert est prouvé ailleurs (déjà connu).** (E14), « non prouvé dans ce texte » selon T20_PROOF
   (07/10), est prouvé le 27/09 par AUDIT_NORME1 et par RANK17_HANDOFF §10 (R3-03). Il ne concerne que C2.
4. **Les résultats de l'équipe ferment des pistes du dépôt externe.** P ≤ 852 vide toute la branche externe n3 = 705 / 708
   (R3-04). La fenêtre r ∈ {37, …, 43} vide les lignes externes r_ext = 28 à 34 (R3-05). J'ai vérifié le dictionnaire
   r = r_ext + 1 par l'algèbre, et la note 102 de l'équipe (P) le confirme.
5. **Analogie C3 → C1 (l'exemple demandé) : déjà examinée et close trois fois.** Voir la note 113 (25/09), le rapport 02
   (16/10) et MAND (19/10). Le mécanisme exige 𝔭 | c dans (A + 4I)(A − 3I) = cJ, donc 𝔭 = 2 sans symétrie. Sa version
   locale existe déjà : L23, le critère de Seidel (note 102), DISC et le Théorème B. Ce sont des filtres, pas des exclusions
   (R3-20).
6. **Meilleure analogie concrète : C7 → « droite dans six grilles » (R3-21).** Le lemme « aucune droite dans six grilles »
   tuerait 7 des 35 gabarits c = 3 encore ouverts ; je l'ai vérifié dans `c3_open_now.tsv`. Coût annoncé : quelques heures
   de travail local. *[seconde passe : compte faux, selon la vérification V2. Le lemme en tuerait 9 (7841 et 9798 en plus).
   Le coût n'est pas justifié, car le lemme équivaut à un sous-cas entier. L'analogie était DÉJÀ CONNUE (08/10, 19/10) :
   R3-52, R3-63.]*
7. **Principales incohérences.** (a) DISC « 2 ou 14 » contre « 2 » (R3-40). (b) Gabarits c4 : le n° 7 est exclu par le score
   (AUD, 18/10), mais L07 et L10 le disent « rouvert » (R3-41). *[seconde passe : ma lecture est dépassée. Le 18/10 à
   14:36 UTC, la branche c ≥ 4 est fermée 79/79 à la racine minimisant 9s + 8g (S, saine face au bug selon V3). Seul le
   front « racine quelconque » reste à 76/79 (R3-55).]* (c) Une entrée de L03a, « rang 42 … 0 survivant », désigne
   la vague W42, pas une exclusion du rang 43 (R3-42). (d) asymmetric.tex omet Wilbrink 1984, Thm 5, pour l'ordre 11
   (R3-43). (e) Plusieurs prémisses de septembre supposent l'unicité de BvLS, alors que 8 srg(243,22,1,2) sont connus
   (R3-44). (f) Des redécouvertes en série du dépôt externe de juillet, présent dans l'archive depuis le 21/09 (R3-47).

## 2. Table des lemmes ouverts et de leur état

Environ 370 lemmes ouverts ou étapes manquantes figurent dans le matériau, dont 99 pour L09. Je les regroupe par thème.
« Aucune preuve trouvée » veut dire : rien dans le matériau des 11 lots ni dans les sources que j'ai ouvertes pour
vérification. Ce n'est pas une recherche exhaustive des dépôts.

| # | thème (identifiants principaux) | énoncé visé et ce qu'il donnerait | état après recoupement | entrée |
|---|---|---|---|---|
| 1 | Plafond de torsion, borne inférieure sur P (L01 [B][F] ; L05 O09, O10, O20 ; L07 « borne inférieure sur P » ; L09-LEMME-001 à 003, 016, 017, 033 ; L09-COND-045, 046 ; ext. O5, O6, K22) | P ≥ 1152 ou P ≥ 1 forcé ; contredirait P ≤ 1151 ou P ≤ 852 | ouvert partout. Même verrou côté externe (forcer un prisme, n3 ≤ 4155). Aucune preuve | R3-12 (décomposition de P ≤ 852) |
| 2 | Planchers de k : d(L) ≤ 9 ou ≤ 12, NT pour k ≤ 20, (4,8), k = 18 et k = 20 (L09-LEMME-006, 011, 012, 034, 037 à 039 ; L09-COND-040 à 044) | k ≥ 12, 14, 18, 20, 22 | **sans objet** : k ≥ 22 vient du programme thêta (08/10, C) | R3-08 |
| 3 | Rang 37 : (a′) uniforme, NT, « toute droite déconnectée », énoncé B, réduction 10⁴, test à deux étoiles, H₃₇, Core37, N14 audité, N16, N18, c₂₀ ≤ 4 (L06 OUVERT-01 à 05, 09 à 12, 24 ; L08 ; L09-LEMME-035, 036, 053, 054, 075 ; L10 OUVERT-07, 09 à 11) | r ≠ 37 | ouverts. La route finie (Théorème 6.1) est la plus avancée. N14 sert ailleurs (R3-02) | R3-22, R3-23, R3-28 |
| 4 | Rangs 39 à 43 : théorème qui borne r, « 7-rang ≥ 25 », moteur sans u, S₀ (borne 2288, profils 40/9, 3 271 supports P3/N25), classification de O, 22-coclique, 3-rang du plan 2-(22,4,2), argument de repère pour le rang 43 (L08 ; L06 OUVERT-07, 13, 21, 22 ; L02-A ; L05 O06 ; L10 OUVERT-08) | exclusion des rangs 39, 41, 43 | ouverts. Seul ajout : dans S₀, a₇ = b₁ = 0, donc pas de co-Heawood. *[seconde passe : au rang 43, a₈ ≤ 1168 (hôte de Codex = M, R3-58) et a₇ = b₁ ≤ 24 (R3-61)]* | R3-02, R3-22, R3-58, R3-61 |
| 5 | Lois à quatre étoiles : H-MATCH (S1, S2, KER-SYM-14, FAKE-13) ; N9-NG, NG5, NG7, Q7, ODDCONST, EVEN′, SYM, QUOT, C4DO, SYM6, ODD-PURE, D9 ; (B′), (C), (B), H4′, (A4), K22, T8 et T15, N15 ; borne d'absorption (L05 O02 à O05, O15 ; L07 ; L08 ; L10 OUVERT-01 à 05) | pas de Conway (avec P ≤ 852 ou L8) | ouverts. Aucune preuve ailleurs. Réfutés, à leur portée : (N9) avec grilles, (R7), ODD9, (A), (H4), (SQ30) (artefact). *[seconde passe : ODD-PURE exclut à lui seul c_min = 1 ; avec la fermeture c ≥ 4, il reste ODD-PURE, Z ≠ 0 à c = 2 et rang Z ≥ 2 à c = 3 (R3-50)]* | R3-10, R3-50 |
| 6 | Cinq étoiles, R8, CEGAR, coexistence G18 (L07 ; L08 ; L10 OUVERT-06, 22, 23) | pas de Conway à tout rang | ouverts. Le lemme d'équilibre n'est pas dans l'encodeur R8. *[seconde passe : la borne « 2f ≤ 10 » se généralise à toute symétrie qui fixe 4 et déplace une lettre de l ∪ m ; aucune des cinq familles UNKNOWN n'est fermée (R3-51)]* | R3-27, R3-29, R3-51 |
| 7 | Route c : gabarits c4 n° 9 et 19, certificats portables ; registre c = 3 (35 ouverts) ; c ≤ 2 (noyau dur de 74, 2 302 537 classes c = 1, k ≤ 3 non énuméré) ; m = 2 (3 443 556 gabarits) ; branche (II) ; R1G (L05 O07, O08 ; L08 ; L09-LEMME-093 à 096 ; L10 OUVERT-13 à 16) | pas de Conway (avec c ≤ 3 forcé, S) | ouverts. *[seconde passe : branche c ≥ 4 fermée 79/79 à la racine minimisant 9s + 8g (S, R3-55). « Aucune droite dans six grilles » tuerait 9 des 35, et non 7 ; une borne excluant les noyaux de dimension ≥ 6 en tuerait 14 ; l'union fait 22 (R3-52)]* | R3-21, R3-25, R3-41, R3-52, R3-53, R3-55 |
| 8 | Lois c = 1 : (SV1), H46-c1, (a ≤ 1) ∧ (b ≥ 1), rang_F₃(A_Ω) ≥ 46, (Q), cas I à IV, D ≠ 0 (L08 ; L10 OUVERT-05) | aucune droite c = 1 | ouverts. Note : la borne « Conway ⇒ rang_F₃(A_Ω) ≤ 45 » vient de rang_Q(A − 3I) = 45 (EXPLORATION.md:645-646). Elle est cohérente avec la forme de Smith externe (rang_F3(A) = 45). *[seconde passe : ODD-PURE suffirait ; toute preuve par formes tournées d'E3 doit utiliser la structure 0/1 (L08-043) : R3-50]* | R3-50 |
| 9 | Symétrie forcée : borne sur les complétions, mécanisme sur 30 dimensions, conjecture S, F16 (σ_x forcé), famille co-Heawood de V15, bord inévitable symétrique (L07 ; L09-LEMME-010, 092 ; L05 O12, O21 ; L10 OUVERT-19) | exclusion de C1 | co-Heawood **clos au rang 37** (E, via N14) ; le reste est ouvert | R3-02, R3-24 |
| 10 | Cocliques : α ≥ 21, existence d'une 22-coclique, K7, profils (0,2) et (1,3), designs 2-(22,4,2) (L05 O12, O22 ; L06 OUVERT-13 ; L07 ; L09-LEMME-089 ; ext. O15, K23) | fermeture de C1 par le cadre coclique | ouverts. Exclusions partielles seulement (designs cycliques et one-rotational, E) | — |
| 11 | Grilles : tissu de 11 grilles en régime mixte, balance du sous-cas (A), g(x) ≤ 16, « aucune droite dans 4 ou 6 grilles », partie signes de la droite à six grilles (L06 OUVERT-05, 06 ; L08 ; L09-LEMME-009, 021, 023 ; L07) | sous-cas (A) ; c = 6 ; τ_grid | ouverts | R3-21 |
| 12 | Arithmétique et réseaux : discriminant de Λ_L ; ensembles −4-serrés ; seconde détermination de r mod 2 ; accidents 7-adiques isotropes ; min Λ₃(T) ; DISC et L4 (L09-LEMME-018, 022, 076, 097 ; L09-COND-199 ; L06 OUVERT-25) | routes 7-adiques | Λ_L : **calculé** (Prop. 13 du Mandat C, à e₃ près). DISC : **réglé** (classe 2). r mod 2 : toutes les déterminations concordent (r impair). Le reste est ouvert | R3-01, R3-07, R3-11 |
| 13 | Quadrangles, holonomie, transport : loi c(Q), 4-cycles de transport, cinq bords (L06 OUVERT-16, 23 ; L10 OUVERT-12 ; L06 COND-38) | conditions de parité | ouverts. La « loi exacte » forte est réfutée (produits cartésiens) ; la partie quadrangles reste une conjecture | — |
| 14 | srg(243) : reproduction indépendante de S3 et des Z3-revêtements, membre asymétrique, groupes d'ordre 81, conjecture de Reimbayev, méthode d'« unicité de BvLS » (L06 OUVERT-18, 19 ; L09-LEMME-059, 070, 071, 088 ; L10 OUVERT-19, 26) | contrôles positifs | F2-SRG (version famille) et Reimbayev sont **réfutés** (8 graphes connus). La prémisse « unicité de BvLS » est fausse sans hypothèse | R3-44 |
| 15 | C2 interne : Stage Q, Smith 7-adique, MacWilliams, Ishida, φ_u(R), mélanges, H-β, étoile libre, tout-tordu, carrés dis, propagation (P), (H) min K* ≥ 9/7, T22, T24, heptade, recertification jumelle, complétude des paires, certificats, R6, R8, J2, J3, bloc plein, g⁻ = 18 et 20 (L01 ; L02 ; L09-LEMME-040 à 087 ; L10 OUVERT-17, 18) | non-existence d'une involution | C2 est clos par la route C (156/156, relu par IA seulement). (E14) est **prouvé ailleurs**. « Existence de U » vient du Théorème R, F0 de A.0, et « tuer une orbite y1 » du Corollaire Y1 (en partie). (H) min K* ≥ 9/7 n'est **pas** T16 (faux ami). T22, T24 et la recertification restent ouverts | R3-03, R3-13 |
| 16 | C3 interne : relectures, D3, D4, D8, critère p = 3 général, Lean (L04 OPN-1 à 11) | statut publiable ; autres paramètres | ouverts. OPN-3, pour l'ordre 11 : Wilbrink 1984 et le calcul externe | R3-06 |
| 17 | Dépôt externe (O-01 à O-23 ; O1 à O19) | exclusions d'extrémités et de lignes de rang | n3 = 705 ou 708 : **sans objet**. Lignes 28 à 34 : **sans objet**. O-12 (N16) : réponse générale a₈ ≤ 6930. O-19 : réponse partielle (blocs à quatre étoiles). O-14 : la voie α ≤ 4 est réfutée (C-53). Extrémité 4158 et rang 11 : ouverts | R3-04, R3-05, R3-09, R3-48 |
| 18 | Littérature : Makhnev 1988, BL11 et la thèse de Behbahani, LM14, Crnković–Maksimović, Baker, Harrison (L03a O-21 ; L03b O16, O17 ; L04 OPN-3 ; L02-D) | sources primaires | Wilbrink 1984 a été lu (notes/94) mais n'est pas cité dans asymmetric.tex ; BL11 n'a pas été ouvert | R3-06, R3-43 |
| 19 | Certification, relecture, Lean, archivage (nombreux) | statut publiable | non examinés : pas de lien mathématique à chercher | — |

## 3. Liens trouvés, classés par potentiel

Aucun lien de potentiel EXCLUSION_GRAPHE, EXCLUSION_C1, EXCLUSION_RANG ou EXCLUSION_CAS n'a été **trouvé**. Ces potentiels
n'apparaissent que pour des analogies dont la pièce manquante reste à prouver (section 4).

### 3.1 Réductions (vérifiées)

**R3-02 — V15 × N14, au rang 37 (nouveau).**
- *Lemme ouvert.* L09-LEMME-092 : la « famille co-Heawood » de V15 (Codex, `NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md` §79,
  14/10). Énoncé exact : pour chaque facteur D d'un bord positif de 43 sommets, ou bien il reste au plus deux affectations de
  signes, ou bien toute complétion contient un co-Heawood disjoint du bord. Ce co-Heawood est donné par f = √2·v, vecteur propre
  −4 entier de norme 14. « La famille co-Heawood demeure ouverte. »
- *Preuve ailleurs.* N14 (LAB, NOTE 17.95, 10/10) : au rang 37, il n'existe aucun vecteur propre −4 entier de norme 14.
  Statut E : recherche exhaustive sur 33 508 orbites, sans certificat, non auditée. Au rang 43, dans la branche S₀ (sans racine),
  a₇ = b₁ = 0 (L06 BORNE-05).
- *Vérification.* La preuve de §79 n'utilise aucune symétrie. Elle utilise la positivité du bord, q = 1 et k = 14. N14 est propre
  au rang 37. Les définitions s'emboîtent : le co-Heawood de §79 est exactement un vecteur propre entier de norme 14.
- *Ce que cela donne.* Au rang 37, la réduction V15 est complète : au plus deux choix de signes par facteur. Ce n'est pas une
  exclusion, car le nombre de bords (B, D) n'est pas borné (L05 O12).
- *Coût.* Un argument ; aucun calcul nouveau. Il reste à certifier N14 (L06 OUVERT-24, environ 6 h).

**R3-01 — DISC × L4.**
- *Lemme ouvert.* L09-LEMME-097 (rapport 05) : « vérifier si le code DISC utilise L4 ».
- *Réponse.*
  - Le code de LAB l'utilise : `disc_scan.py` teste d = 2 × carré (l. 83-84).
  - Celui de Codex ne l'utilise pas : `DISC_CLASSES = ((2,14),(1,7))` (`conway_core_repair.py:36`). Le journal le dit :
    « Aucun lemme de parité n'est utilisé ici » (J:6195).
- *Preuve.* NOTE_PROOFS_1410:338-344 : disc R = −7^(30−k), et avec k pair (L4) c'est un carré parfait. Trois dérivations
  indépendantes concordent : la note LAB, les rapports 03 §6.4 et 05 §6.3.
- *Ce que cela donne.* La branche 14 (T8) et la branche 7 (U15) sont vides. Aucune exclusion passée n'est fausse : échouer pour
  {2, 14} implique échouer pour {2}. Seules des coupes ont été manquées. Les sorties JSON de Codex du 16/10 n'enregistrent que
  les obstructions ; le compte n'est pas faisable.
- *Coût.* Nul.

**R3-21 (analogie, chiffrée) — « aucune droite dans six grilles ».** Ce lemme supprimerait 7 des 35 gabarits ouverts (9302,
9791, 9912, 9966, 10003, 10006 et 10025, tous présents dans `c3_open_now.tsv` du 19/10 à 15:03). Voir 4.2. *[seconde passe :
il faut y ajouter 7841 et 9798, d'où 9 des 35 (VERIF_R3-21). L'analogie est DÉJÀ CONNUE : R3-63.]*

**R3-29 (analogie) — équilibre dans R8.** L'égalité |N(w) ∩ C| = |C|/6 est prouvée (lemme 24.0 de C2 ; L07 K27), mais absente des
contraintes impliquées de `r8lib.py` (seulement L4B et XPAIR). Voir 4.8.

**R3-05 — lignes de rang externes.** Énoncé et vérification du dictionnaire :
- Mod 7, on a 2A − J + I ≡ 2(A − 3I) − J. Or (A − 3I)·1 = 11·1, donc 1 = 2(A − 3I)·1 mod 7, et ker(A − 3I) ⊂ 1^⊥.
- Donc rang(2(A − 3I) − J) = rang(A − 3I) − 1, c'est-à-dire r_ext = r − 1.
- Confirmation P dans l'équipe : la note 102:119-120 donne la forme de Smith de S sur Z₇, 1^{14+k}, d'où rang₇ S = r − 1.
- Contrôle croisé : le rang d'étoile externe 25 − 2e et celui de l'équipe 26 − 2e diffèrent de 1.

Conséquences :
- Les lignes r_ext = 28 à 34 sont exclues. Les cibles externes O-10, O-11, O-12, K17 et K18 deviennent sans objet.
- O-23 se réduit à r_ext ∈ {36, 38, 40, 42}.
- À P = 0, le recensement externe (r3, r7) (281 paires) se restreint à r7 ∈ {36, 38, 40, 42}, si r7 = r_ext comme l'affirme
  la vague 66.
- C'est une réduction pour le dossier externe, pas pour C1.

**R3-12 — décomposition de P ≤ 852.**
- On a 11088/13 = (3/13)·2772 + (4/13)·693. Donc P ≤ 852 est la combinaison de 3P + 4G ≤ 2772 (Codex, 18/10, C) et de
  P − 3G ≤ 693.
- Cette seconde inégalité est connue côté C2 depuis septembre (« n3 ≥ 2079 − 9N », note 08 du labo C2, générale) mais n'est
  utilisée seule nulle part en C1.
- Preuve relue : 3P = (nombre de C4 induits simplement prismatiques) + 18G ≤ 2079 + 9G. Elle suppose qu'un C4 doublement
  prismatique est dans une grille ; la source le prouve et j'en ai vérifié une partie. *[seconde passe : RETIRÉ. Selon la
  vérification V2, ce lemme n'est pas dans la source et il est ouvert. La conclusion survit par la preuve des coins de la
  note 22, qui dépend de c ≠ 3 (N9 ou Lou–Murin). R1 et R2 ont trouvé la même combinaison (R3-63).]*
- Conséquences : P ≤ 693 si ρ = 0, et une racine de score 9s + 8g ≤ (18/99)·min(2772, 2079 + 13G).
- Quasi-raté : sous ρ = 0 on a τ ≤ P ≤ 693, alors que la route des collisions du rang 37 demandait τ_n < 535. L'écart est de
  158, soit 30 %.

**R3-06 — ordre 11.** L'ingrédient (E) de la chaîne « Conway est asymétrique » a trois sources :
- BL11 (calcul) ;
- Wilbrink 1984, Théorème 5 (« élimination à la main et 6 heures de calculatrice programmable »), lu en texte intégral le
  25/09 (`notes/94` §3.8) ;
- le dépôt externe (C, deux implémentations).

Le manuscrit public n'en cite qu'une. Coût : lecture.

**R3-03 — (E14), C2 seulement, déjà connu.** (E14) : tout vecteur propre −4 entier σ-impair non nul a une norme carrée ≥ 16.
Il est prouvé par AUDIT_NORME1 (27/09, « Checked: correct, every line », `A1_REDUCTION.md:143`) et par RANK17_HANDOFF §10
(27/09, preuve sur le graphe).
- Usage de σ dans la preuve : Q = σ(P), trace B = 4, donc une paire p ~ σ(p) avec p ∈ N(x), où x est le point fixe unique.
- La preuve ne passe donc pas à C1, où la norme 14 existe localement (a₇ ≤ 792).
- Conséquence : le Lemme 10.2 de T20_PROOF et les propositions de Codex (HAND.md) ne dépendent plus d'une hypothèse ouverte.

### 3.2 Sans potentiel (consolidation)

- **R3-04.** P ≤ 852 équivaut à n3 ≥ 1602. Toute la branche externe n3 = 705 / 708 est sans objet : O-18, K3 à K10, O8 à O10,
  C-13 à C-21, C-51. J'ai vérifié que n3 externe = N2 de l'équipe par double comptage des 2 079 C4 induits.
- **R3-07.** Le discriminant de Λ_L demandé en septembre (notes/96) est donné par la Proposition 13 du Mandat C :
  dét Λ_L = 7^(45−r)·9^(e₃−1). J'ai vérifié que c'est le même réseau : Gram 4I + C₀ − C₂ − 2C₃. La route d'Akiyama reste
  défavorable, car elle exige un repère épais.
- **R3-08.** Les lemmes de septembre sur les planchers de k sont caducs : k ≥ 22.
- **R3-09.** Le plafond 39 < 44 des méthodes de rang local apparaît des deux côtés (O-19 externe, L09-LEMME-007 et 014). Les
  blocs à quatre étoiles (59 sommets) sont le premier niveau où le rang mord. Aucune exclusion.
- **R3-10.** L09-LEMME-013 : seule sa restriction aux blocs à quatre étoiles est réfutée (objet E7, rang₇ 25). La version
  au niveau du sommet entier reste ouverte.
- **R3-11.** La condition de signe du rapport 08 §6.d2 est la même alternance que la NOTE 17.80 et L23 (25/09).
- **R3-13 (quasi-lien écarté).** « (H) min K* ≥ 9/7 » (rank-17) n'est pas T16 (« min L* ≥ 9/7 », route C). K* est le dual d'un
  réseau de rang 15 du commutateur de rang 17 ; son minimum descend à 5/7. N* est le dual du repère de rang 22 ; son minimum est
  ≥ 8/7. Les échelons R_n portent sur |a|² = 4n sur 42 orbites, avec une condition de coupe mod 2.

## 4. Analogies entre cas : ce qui diffère, ce qu'il faudrait prouver de neuf

### 4.1 C3 → C1 : deux structures congrues modulo un premier (R3-20, déjà connue)

Mécanisme de C3 : Q (entier, Q² + Q = 12I + 6J) et M (hermitien sur Z[ω], M² + M = 12I) sont congrus modulo π = 1 − ω.
- Côté Q, le vecteur 1 (⟨1,1⟩ = 33) injecte le premier 11. Le déterminant du réseau propre vaut d = 7^a·11^b avec b impair,
  donc d ≡ 2 mod 3.
- Côté M, d′ = 7^c ≡ 1 mod 3.
- Contradiction : 2 n'est pas un carré mod 3.

Les trois pistes demandées, examinées aux sources :

1. **Recollement mod 7 de E₋ et E₃.**
   - Dans Z^99 ∩ 1^⊥ (unimodulaire en 7), Λ₃ (dét 7^a·11) et Λ₋₄ (dét 9·7^a, même a) se recollent le long de (Z/7)^a.
   - Les parties unités 11 ≡ 4 et 9 ≡ 2 sont des **carrés** mod 7 : la classe de déterminant ne peut pas se contredire. J'ai
     vérifié que dét A₀·dét B₀ ≡ (−1)^a pour les constituants unimodulaires, quel que soit a. Note 113 R1 (25/09) arrive au
     même résultat : « local et global compatibles en 7 et en 11 ».
   - Avec la parité 2-adique, le recollement donne seulement :
     - r impair (Théorème A ; rapport 02 §6.2, par deux voies indépendantes) ;
     - la forme globale non scindée avec un plan anisotrope U (A′ ; L22 : k ≤ 28) ;
     - la classe (−1)^{k/2} (NOTE 17.80).
   - Le no-go de la note 113 R3 l'explique : si M a seulement les valeurs propres 3 et −4 et M ≡ A mod 𝔭, alors
     (A + 4I)(A − 3I) = 2J impose 𝔭 | 2.
2. **Réseau d'une droite contre réseau global.**
   - C'est L23 (Codex, 25/09). Au rang 37, le résidu lointain d'une droite générique est nul (rang k − 22 = 0), donc la classe
     locale égale la classe globale : (τ(G(T))|7) ∈ {0, −1}, c'est-à-dire τ ∈ {0, 3, 5, 6} mod 7.
   - C'est le véritable analogue de C3 en C1. Mais il ne fait que filtrer : 33,6 % des classes de droites meurent par L23
     (ENUM).
   - Aux rangs ≥ 39, le résidu de rang 2, 4 ou 6 absorbe la classe.
   - MAND (19/10, pont P3) conclut aussi : « au niveau d'une droite, les trois racines voient le même G_T ».
3. **Parties 9 et 11.**
   - Le vecteur 1 (valeur propre 14) se recolle à Λ₃ en 11 (car 3 ≡ 14 mod 11) et à Λ₋₄ en 3 (car −4 ≡ 14 mod 3).
   - En C3, le 11 n'était que d'un côté parce que M n'avait pas de vecteur 1. En C1, il n'y a qu'une structure ; ces recollements
     de rang 1 sont toujours réalisables.

**Ce qui manque pour une exclusion :**
- soit une seconde structure entière congrue à A, ou à un bloc de A, modulo un premier impair, et qui ne soit pas Z-linéaire en
  A, J, I, N, 1. La note 113 R2 montre que ces constructions-là sont automatiques. Le seul candidat examiné, le gain
  d'Eisenstein des droites orientées, est fermé (113 R3 bis) ;
- soit un objet local forcé de la mauvaise classe :
  - une droite générique forcée avec (τ|7) = +1 au rang 37 ;
  - ou un sous-graphe induit forcé à ≥ 43 sommets de déterminant de Seidel premier à 7 (L09-COND-047), ce qui équivaut au
    programme des quatre et cinq étoiles.

Coût : un argument ; aucun programme fini n'est identifié. **Potentiel : aucun en l'état.**

### 4.2 C7 → droite dans six grilles (R3-21, déjà proposée, non appliquée)

- *Méthode de C7.* G = 21 × projecteur de rang 4 sur 12 vecteurs de ℝ⁴, Gram entier dans un petit ensemble. Les résidus
  α = 12z² sont entiers et de somme nulle, puis une analyse de cas finie conclut.
- *Objet en C1* (MAND §5, Corollaire 2). 420Π_T est entier, de rang 13 et de diagonale 91, sur les 60 sommets lointains d'une
  droite contenue dans six grilles.
- *Ce qui diffère.*
  - Il y a 60 vecteurs dans ℝ¹³, et non 12 dans ℝ⁴.
  - Les poids viennent des noms (ℤ₃ × ℤ₂)⁶.
  - Deux relations exactes tiennent lieu de diagonale nulle : la somme nulle par bloc de 10 vecteurs, et la somme des voisins
    qui vaut −4 fois le sommet.
  - La partie colonnes n'est pas unique (plus de 536 classes).
- *À prouver.* Classer les colonnes par génération ordonnée, puis traiter les signes (360 bits par classe). Cela demande un
  argument par caractères sur ℤ₂⁶ ou un programme en nombres entiers, car CDCL ne conclut pas (UNKNOWN à 45 s).
- *Gain.* 7 des 35 gabarits c = 3 ouverts disparaissent, et c = 6 disparaît de toutes les branches. *[seconde passe : 9 des
  35 (VERIF_R3-21).]*
- *Coût annoncé* (RENF §7) : local, quelques heures de travail. *[seconde passe : non justifié ; le lemme équivaut à un
  sous-cas entier du problème (VERIF_R3-21 §4).]*
- **Potentiel : réduction.** C'est la meilleure analogie concrète.

### 4.3 Route finie du rang 37 → rangs 39, 41, 43 (R3-22)

- *Ce qui sert au rang 37.* Pour une droite générique, le résidu est nul, Π_T est 7-entier et le graphe lointain est fixé par
  les ombres. La borne P ≤ 852 force au moins 18 droites à t ≤ 7. On teste alors une étoile par droite (3,5 ms), sur
  1,87·10¹¹ classes.
- *Ce qui diffère au rang 39.* Le résidu est de rang 2, donc deux coordonnées libres par sommet. Les droites τ-carrées sont
  permises, avec un résidu anisotrope. L'étoile meurt plus tard (5 lointains au lieu de 3).
- *Ce qui diffère aux rangs 41 et 43.* La codimension de l'étoile tombe à 21 puis 10. Le Théorème B (L08-218) permet de tester au
  rang 43 pour toute la fenêtre, mais c'est le test le plus faible.
- *À prouver de neuf.* Un moteur d'étoile qui traite le résidu, puis un estimateur de Knuth avant tout lancement.
- *Coût.* Au moins celui du rang 37 (5 à 6,5·10⁴ heures-cœur) multiplié par le facteur du résidu, donc hors budget.
- **Potentiel : exclusion de rang** (39 d'abord).

### 4.4 Épuisement N14 → normes 16 et 18 au rang 37 (R3-23)

- *Ce qui diffère.* La norme 14 n'a qu'un cœur rigide, le co-Heawood. La norme 16 a 5 cœurs, 478 attaches et 71 351 mondes PSD
  ; la norme 18 a 26 cœurs. Le catalogue de mondes de norme 16 de Codex est incomplet.
- *À prouver.* Un catalogue complet des mondes de norme 16, puis 18, sous les conditions mod 7 du rang 37, et une borne
  c₂₀ ≤ 4 par graine. Avec l'identité 17.100 (C), le rang 37 tomberait.
- *Coût.* Calcul fini, de taille non chiffrée : faire une estimation de Knuth d'abord.
- **Potentiel : exclusion de rang (37).** *[seconde passe : coûts précisés et ordre proposé en R3-60. Le levier « rang réel
  ≤ 44 − 2m » sur les mondes de norme 20, jamais testé, donnerait a₁₀ = 0 à tout rang et remplacerait c₂₀ ≤ 4.]*

### 4.5 Symétrie forcée et reconstruction à bord (243, Paley 9, Paley 25) → C1 (R3-24)

- *Principe.* Les complétions d'une pièce forcée forment des orbites libres de son groupe d'automorphismes. Si |Aut(pièce)|
  dépasse le nombre de complétions, C1 est exclu.
- *Ce qui diffère.* À 243, les bords venaient d'un spread régulier ou du Hamming plié. À 99, il n'y a pas de spread régulier
  (le quotient serait srg(33,12,1,6), de multiplicité 44/7). Le cadre Φ_x a un groupe d'ordre 645 120 mais au moins 99 ×
  645 120 complétions en C1.
- *Ce qui est acquis.* V15 : au plus 2 complétions pour un bord positif de 43 sommets ; au rang 37, au plus 2 signes (R3-02).
- *À trouver.* Un bord canonique, positif, d'au moins 43 sommets, dont le groupe d'automorphismes est forcé d'ordre ≥ 3 (≥ 2 à
  44 sommets). Aucun candidat.
- **Potentiel : exclusion de C1** ; coût : un argument.

### 4.6 Fermeture de c ≥ 4 → c = 3, c ≤ 2 et la branche m ≤ 2 (R3-25)

- *Ce qui servait à c ≥ 4.* Au moins 7 paires-grilles par sommet. La racine de score minimal a s ≤ 49, et les gabarits sont
  rigides (Gram, CP-SAT, score).
- *Ce qui diffère à c ≤ 2.* Une droite y porte au plus 2 grilles (une paire en grille donne une composante prisme). Les
  gabarits explosent : environ 10⁷.
- *À prouver.* Un comptage global de la branche (II) (au moins 33 droites à c ≤ 2) contre P ≤ 852 et 3P + 4G ≤ 2772. La borne
  P ≤ 693 + 3ρ (R3-12) n'aide que si ρ est petit. Pour m = 2, avec (B′), il faut aussi exclure m ≥ 2 en entier (L08-168).
- **Potentiel : exclusion de cas.**

### 4.7 Route C et lemmes T16 à T20 (C2) → C1 (R3-26) : fermé

- σ divise les rangs par deux (22 + 22 au lieu de 44) et produit un repère de rang 22 dans un réseau unimodulaire de rang 24,
  classé par Borcherds.
- En C1, aucune classification n'est disponible : la masse du genre de rang 48 vaut 1,5·10¹²¹. La norme 14 y est localement
  possible.
- Rien à reprendre (L06 METH-13 ; note 110).

### 4.8 Lemme d'équilibre (C2) → R8 (R3-29)

- *Énoncé.* Pour une droite l avec c(l) ≥ 2, toute étiquette w lointaine de l a exactement |C|/6 voisins dans chaque réunion C
  de composantes de G_l.
- *Ce qui diffère de C2.* Sans σ, les composantes de G_l ne sont plus appariées, mais la preuve est générale en k : l'égalité
  reste vraie. Elle est triviale si c(l) = 1.
- *À faire.* L'ajouter aux contraintes impliquées de R8, puis vérifier sur une instance plantée qu'elle n'est pas déjà
  impliquée par les contraintes encodées.
- *Coût.* Quelques heures de codage. **Potentiel : réduction** (renforcer le modèle).

### 4.9 Autres, sans gain

- **R3-27.** Le dépôt externe (vague 205 : la route paire-locale est fermée, une loi à trois centres est nécessaire) et l'équipe
  (R8 : quatre étoiles + 8 étiquettes) ont trouvé le même mur. Le seul apport transférable est la chaîne de certificats
  (VeriPB, LRAT).
- **R3-28.** Au rang 37 générique, la donnée (boule, 60 ombres) doit être sans automorphisme. Ce filtre ne retire qu'environ
  0,09 % des classes.

## 5. Incohérences

| id | qui dit quoi, quand | résolution |
|---|---|---|
| R3-40 | NOTE_PROOFS_1410:343-344 et disc_scan.py (LAB, 15/10) : DISC = classe 2, k pair. BRIEF.md:9, J:6193-6197, conway_core_repair.py:36 et la ligne 278 de la fiche L07 (16/10) : « 2 ou 14 », « 1 ou 7 » | la version forte vaut (R3-01) ; la version faible est saine mais incomplète |
| R3-41 | CORRECTION_DOMAIN_ORTOOLS (18/10), L07 K11 et L10 OUVERT-L10-14 : gabarits c4 n° 7, 9 et 19 « rouverts ». AUD §8 (18/10) : le gabarit 7 est exclu à la racine de score minimal, « il reste 9 et 19 » | *[seconde passe : DÉPASSÉ. Pont n° 1050 (18/10, 14:36 UTC) : fermeture 79/79 à la racine minimisant 9s + 8g (S), saine face au bug (V3) ; 76/79 seulement pour une racine quelconque (R3-55)]* |
| R3-42 | fiche L03a, borne B-43 : « ext : rang 42 … 0 survivant » | c'est la vague W42 (rang_F7(M) ≥ 27). Le rang 43 de l'équipe (r_ext = 42) reste ouvert |
| R3-43 | asymmetric.tex (public, 11/10) : ordre 11 par BL11 et LM14 « non vérifié ». notes/94 §3.8 (25/09) : Wilbrink 1984, Thm 5, lu en texte intégral. L04 : « LM14, non vérifié » | ajouter Wilbrink et le calcul externe aux sources de (E) |
| R3-44 | L09-LEMME-004, 059, 070 et L09-COND-028, 029 (septembre) : F2-SRG, « unicité de BvLS ». Rapport 07 R41 : 8 srg(243,22,1,2) connus, dont le jumeau publié | la version famille de F2-SRG est réfutée ; la version propre à 99 reste ouverte |
| R3-45 | fiche L02 : (E14) « O dans ce texte ». conway99-c2-aws : AUDIT_NORME1 « PROVED-ELSEWHERE » | reclasser (E14) comme prouvé ailleurs |
| R3-46 | théorème de LAP (maille ≥ 5 ⇒ droite connexe au rang 37) : E (L02-364) ou S (L05-061). Codex 233 : E, « non relu » (L02-391) ou C (L05-070). Dernière marche de la fenêtre : E (L02-A, L09) ou C (L06, L10). P ≤ 852 : « E ou C » (L08) ou C (autres lots) | retenir le statut le plus faible dans toute combinaison |
| R3-47 | équipe (septembre-octobre) contre dépôt externe (22-29/07, dans l'archive depuis le 21/09) : L16 = W20 ; P ≤ 1150 = W21-W23 ; r impair + L22 = W66 ; réservoir de 55 440 graines ; ρ ≤ 191 = H ≤ 191 ; design 2-(22,4,2) ; code F₂ de poids ≥ 8 ; profil de prismes d'une droite ; π(L) ≠ 11 ; rang d'étoile 26 − 2e = 25 − 2e. Manuscrit rank7.tex (11/10) : r ≥ 25, alors que W42 donnait r ≥ 29 et l'équipe r ≥ 37 dès le 08/10 | aucune contradiction : ce sont des redécouvertes ; mettre le manuscrit public à jour |
| R3-48 | L03a O-14 : le « lemme des quatre échecs » est une voie ouverte. L03a C-53 : la voie α ≤ 4 est réfutée par un gadget à 5 échecs | seule la voie locale est réfutée ; l'énoncé global reste ouvert |

## 6. Ce qui n'a pas été examiné (première passe ; mise à jour au §7.6)

- **Lots L11a à L11f** (messages du pont LAB ↔ Codex) : non lus, comme convenu. Ils arriveront en seconde passe.
  `fiches/L11f_pont.md` a seulement servi à une recherche ponctuelle (lien V15 × N14). *[seconde passe : traités au §7.]*
- **L09** : seul le matériau de recombinaison (`MATERIAUX_BRUTS_L09.md`) a été lu en entier. Le détail des 508 résultats de
  `L09_structures_astra_coord.jsonl` n'a pas été relu ligne à ligne.
- **Relectures du 16/10** : j'ai lu les sections « utile aujourd'hui » des rapports 01, 02, 03, 05, 07 (§2), 08 (§5-7) et 09
  (§5-9), ainsi que les premières lignes de 04 et 06. Les rapports 04 et 06 n'ont pas été lus en entier.
- **Recensement externe (r3, r7)** à l'extrémité P = 0 : la liste exacte des 281 paires (README externe L99-L141) n'a pas été
  extraite. La réduction de R3-05 (3) n'est donc pas chiffrée.
- **K36 de Codex** (« affine 37 ⇒ entière 26 », 06/10) face à R7 de LAB (« tout rang ≥ 37 exige un vecteur de L1 de norme 18 ou
  26 », 08/10) : je n'ai pas vérifié si les vecteurs de L1 ∖ L de norme 26 sont les « fonctions affines » de Codex. Lien
  possible non établi. *[seconde passe : établi. « Affine 37 » est un vecteur φ − (1/3)1 de L1 ∖ L de norme 26 ; au rang 43,
  l'hôte de Codex est M lui-même (R3-58 ; voir aussi R1-13).]*
- **Les 76 fermetures c4 par CP-SAT** : je n'ai pas vérifié leur immunité au bug OR-Tools du 18/10. *[seconde passe : la
  vérification V3 (VERIF_C4_FERMETURE.md) l'a fait : chaîne saine, statut S.]*
- **Preuve de « un C4 doublement prismatique est dans une grille »** (R3-12) : vérifiée en partie seulement. *[seconde
  passe : le lemme est ouvert, et la preuve C4 est retirée (R3-63).]*
- **Wilbrink 1984** (R3-06) : non relu par moi ; je m'appuie sur la note 94 de l'équipe.
- Certification, Lean, archivage, relectures humaines : hors objet (pas de lien mathématique).
- Aucun calcul lourd. Je n'ai lancé que des recherches de texte et un petit script de comptage JSON sur les sorties DISC de Codex
  (un processus, moins d'une minute).

## 7. Seconde passe : lots L11a à L11f du pont (R3-49 à R3-64)

**Matériau lu.**
- `MATERIAUX_BRUTS_L11.md`, en entier.
- Les messages du pont cités, dans la copie `pont_codex/` : n° 172 à 182, 237, 896 à 901, 928 à 939, 1039 à 1050, 1142, 1260
  à 1277.
- Les entrées citées des fiches L11a, L11b, L11d et L11e.

**Sources ouvertes pour vérifier.**
- Note 176 de Codex (§5 et §8).
- NOTE.md, 17.98.
- Notes de Codex du 20/10 : `BUDGET_ENTIER_SUPPORT_SIGNE`, `TROIS_COLONNES_EGALES_INTERDITES`.
- Lemme 14 de LAP (`RECHERCHE_C_TRANSFORMATIONS.md`).
- PASSATION de Codex et fichiers de l'hôte (`Documents/Codex/2026-10-05/…` : `global_two_forced_shells.txt`,
  `global_short_spectra_audit.txt`, `global_prismless_obstruction.txt`).
- Inventaire du registre c = 3.

**Vérifications des autres agents.** J'ai lu les résultats de V1 à V3 (VERIF_*.md) sans les refaire. Seul calcul : un script
d'une seconde sur l'inventaire c = 3.

**Bilan.** Aucune exclusion. Un lemme déclaré ouvert est prouvé ailleurs pour deux de ses quatre sous-cas (R3-49). Deux
majorations nouvelles valent au rang 43 (R3-58, R3-61). Les six pistes signalées n'aboutissent pas : la plupart sont déjà
connues ou en cours.

### 7.1 Lemmes ouverts prouvés ailleurs

**R3-49 — Lemme A de LAP en norme 18 (L02_C2_aws-282, « OUVERTS : sommet partagé autre que ω, c manquants différents,
type (1,1,1,1), e = 1 »).**
- *Sommet partagé autre que ω.* Impossible.
  - La complétion de LAB au message 174 du pont (08/10, 00:10 UTC) le montre, sous-cas de Fano compris.
  - Plus généralement, la note 176 §5 de Codex (08/10) prouve que deux vecteurs de norme 18 ne diffèrent jamais d'un vecteur
    de norme 14.
  - Le §8 de la même note écrit : « L'argument de LAP et LAB transmis au message 174 est correct ».
- *e = 1.* Vide, par 17.98 de LAB (10/10) : les deux supports d'un vecteur de norme 18 sont indépendants. J'ai relu la preuve :
  - le chemin p₁ – q – y compte au moins 15 d'un côté et au plus 15 de l'autre ;
  - l'égalité force N_Q(p₁) ∪ N_Q(p₂) à 9 sommets hors de {q₁, q₂}, soit plus que les 7 disponibles.
- *c manquants différents.* Contourné : au plus 2 réalisations par graine et par c manquant, donc au plus 12 par graine
  (note 176 §8).
- *Ce qui reste ouvert.* Le seul type (1,1,1,1), c'est-à-dire (n₀, n₁, n₂) = (0, 4, 4).
- *Conséquence.* κ₁₈ ≤ 12 + κ(0,4,4).
- *Potentiel.* Aucun, car la route « vecteurs par graine » est close comme méthode (L02-315, L06-063).
- *Points à vérifier.* La note 171 (e ≤ 1), dont dépend 17.98, et l'étape finale du §5.

**R3-62 — « (6,6) partout » à P = S = 0.** La liste des lemmes ouverts de L11 le donne encore ouvert. Il est exclu au rang 37
par le théorème de LAP (maille ≥ 5 ⇒ G(T) connexe ; S, audit partiel de Codex).
- C'est DÉJÀ CONNU (relecture 07 R16, L06-088).
- La chaîne de septembre se réduit à ses hypothèses NT et (a′), toujours ouvertes.

**R3-53 (en partie) — l'identité (B) de Codex (20/10) est le Lemme 14 de LAP (09/10, 16:18 UTC).** C'est le même calcul : φ(t) =
C(t,2) − (t − 1) et W = σ_X + σ_Y. La note du 20/10 ne cite pas LAP.

### 7.2 Les six pistes signalées par le coordinateur

| piste | réponse | entrée |
|---|---|---|
| (1) formes tournées d'E3 × H46 ⇒ (B′) à c = 1 | **Non prouvé ailleurs.** Données seulement : les formes tournées tuent les 1 740 côtés positifs, mais aucune des 17 structures sans lemme (L08-049, E). Contrainte de méthode : L08-043 (P) interdit, sur 59 cas sur 63, toute preuve par la positivité et des coupes linéaires seules ; il faut la structure 0/1 | R3-50 |
| (2) ODD-PURE et rang Z ≥ c − 1 pour N9-NG | **Non prouvés.** Recombinaison : ODD-PURE seul rend c_min = 1 impossible (pont n° 931). Les pistes (1) et (2) se ramènent donc au même lemme. Comme la branche c ≥ 4 est fermée (S), il reste exactement : ODD-PURE, Z ≠ 0 à c = 2, rang Z ≥ 2 à c = 3. ODDCONST n'est prouvé que si ιx ∈ ker (L11e-128). La marge d'ODD-PURE n'est pas uniforme (0,99993) | R3-50 |
| (3) complétion du Lemme A (pont n° 174) | **Vérifiée.** La complétion est juste. Elle figure aussi dans la note 176 §8, contrairement à la remarque « ABSENTE DES NOTES » de L11a-85. Le cas e = 1 est réglé par 17.98 | R3-49, R3-56 |
| (4) « 2f ≤ 10 » pour d'autres involutions partielles | **Oui, en généralisant.** Toute symétrie qui fixe 4 et déplace une lettre de l ∪ m fixe point par point au plus 2 des 5 droites {0,1}, {6,7}, …, {12,13}. Cela ferme (2 3), (2 3)(6 7), (2 3)(6 7)(8 9), (2 3)(6 8)(7 9), (0 2)(1 3) et (0 2)(1 3)(6 7). Aucune des 5 familles UNKNOWN de LAB n'est fermée : la borne est atteinte. Sans effet sur C1 | R3-51 |
| (5) L2C et ablation 40/60 face aux 35 gabarits c = 3 | L2C est le lemme d'équilibre de C2 ; il est déjà dans le modèle, et les 35 l'ont passé. L'ablation explique les morts, pas les survivants. Une borne excluant les noyaux de dimension ≥ 6 en couvrirait 14, le lemme des six grilles 9, l'union 22. Restent 13 gabarits de dimension 4 ou 5 sans droite c = 6 (liste en R3-52) | R3-52 |
| (6) noyau signé n_B − n_A, 4K2, h ternaire sur 9179, 9912, 9966 | **Déjà en cours chez Codex** (19-20/10). Les cœurs 8 sont des paires égales (pont n° 1271). Le noyau est 4K2, et le budget (C) donne t ≤ 1. Seul 9912 est traité (27 sélections, 1 réfutée, aucun gabarit fermé) ; 9179 et 9966 ne le sont pas dans les sources lues | R3-53 |

### 7.3 Autres liens : lemmes L01-L10 × résultats du pont

**R3-58 — au rang 43, l'hôte de Codex est M (réduction, dérivation R3).**
- *Construction.* Le repère tendu de Codex définit φ(u) = ((u, w_x))_x.
  - φ est une isométrie à √7 près de K* sur un sous-réseau de L1.
  - La raison : la fraction commune 0 ou ±1/3 donne exactement la forme φ − (s/3)1 de NOTE:15.
- *Indice.* det φ(K*) = 7⁴⁴/49 = 7⁴², à comparer à det L1 = 7^(r−1). L'indice vaut donc 7^((43−r)/2).
- *Au rang 43.* L'indice vaut 1, d'où K ≅ M, U_n = a_{n/2} et U14 = 2m = a₇ = b₁.
  - Contrôle indépendant : l'identité de Codex 2U16 + 16U18 + U26 = 2632 + 112m + … est terme à terme COND-03 au rang 43,
    car 329·8 = 2632 et 49b₁ + 7a₇ = 112m.
  - Donc **a₈ ≤ 1168 au rang 43**, au lieu de 6930.
- *Aux rangs 37 à 41.* U_n ≤ a_{n/2} seulement : la mise en garde de R1-13 est juste. L'énoncé uniforme « L1 a un vecteur de
  norme 18 ou 26 » reste vrai à tout rang.
- *Ce qui était déjà connu.* LAP (08/10) avait vu les paires « de type 43 », et LAB le recollement du rang 43. La borne sur a₈
  n'est écrite nulle part.

**R3-61 — b₁ ≤ 24 à tout rang, et a₇ = b₁ ≤ 24 au rang 43.**
- *Trois ingrédients :*
  - les racines de M sont deux à deux orthogonales (LAB, 08/10) ;
  - √7·racine est un co-Heawood ;
  - une famille de co-Heawoods orthogonaux a au plus 12 membres (Codex, 14/10 ; E selon L11d-121).
- Ce résultat améliore b₁ ≤ 44 (L05-029), que R2 garde.
- Codex l'avait en substance (« au plus 24 racines »), mais pour un sous-réseau d'indice 3 de M.

**R3-54 — réponse à la question K5 de la fiche L11d.** Aucun lot ne prouve « tout Conway contient une grille ».
- Le seul critère est P > 693 ⇒ grille (L01-46, 24/09, qui dépend de c ≠ 3).
- Avec C16 (grille ⇒ (B)) : sans droite spéciale, ρ = 0 et P ≤ 693. Ce n'est pas une exclusion.

**R3-60 — normes 16, 18, 20 au rang 37 (mise à jour de R3-23).**
- *Condition.* Le rang 37 tombe si a₈ = a₉ = a₁₀ = 0.
- *Ordre de coût proposé :*
  1. le test de rang réel sur les mondes de norme 20, jamais testé ; il donnerait a₁₀ = 0 à tout rang ;
  2. le catalogue N16, avec 463 attaches mixtes, passé à n16cell (0,3 s à 1 min par monde) ;
  3. N18, plus de 10¹³ mondes par noyau (H), hors de portée.

**R3-57 — plafond à un sommet (déjà connu).** L11b-95 = L05-045 = L06-069 : c'est la preuve du premier niveau du plafond
de R3-09.

### 7.4 Quasi-ratés

- **Rang 43, norme 16.** L'alternative de LAB demandait a₈ ≥ 1316, soit 2a₈ ≥ 2632. Codex borne 2a₈ ≤ 2336. L'écart, 296, est
  exactement la constante de Codex. L'alternative meurt (R3-58 ; R1-13 l'avait déjà rendue superflue par la disjonction).
- **Norme 18 par graine.** Ce n'est pas un quasi-raté, l'écart est grand. Au rang 37, la norme 18 seule exige a₉ ≥ 4918
  (L11d-027), alors que a₉ ≤ 6160·κ₁₈. Le comptage par graine ne la tuerait que si κ₁₈ = 0. On a κ₁₈ ≤ 12 + κ(0,4,4)
  (R3-49).
- **Budget des paires égales (C).** Il reste 3 unités si t = 1 et 8 si t = 0 ; un seul raccordement de 9912 est réfuté sur 27
  (R3-53).
- **Registre c = 3.** Les deux lemmes ouverts les plus ciblés laisseraient 13 gabarits sur 35 (R3-52).

### 7.5 Corrections et incohérences

| id | qui dit quoi | résolution |
|---|---|---|
| R3-55 | mon R3-41 : « 9 et 19 ouverts » (d'après l'AUD §8) | dépassé. Pont n° 1050 (18/10, 14:36 UTC) : 79/79 à la racine minimisant 9s + 8g (S), saine face au bug selon V3 |
| R3-63 | mes R3-02, R3-12, R3-21 face à V1 et V2 | R3-02 tient avec réserves ; la preuve C4 de R3-12 est retirée, sa conclusion survit ; R3-21 était déjà connue, compte 9/35, coût non justifié |
| R3-56 | L11a-85 : la complétion de LAB est « ABSENTE DES NOTES » | faux : note 176 §8 de Codex (08/10) |
| R3-64 | notes de Codex du 20/10 : « 435 ouverts » | copie locale périmée (19/10, 06:54 UTC) ; le registre de LAB compte 35 lignes (19/10, 15:03). Synchroniser avant de chiffrer un gain |
| R3-59 | Théorème B, B3 (20/10) : monotonie en r d'un test local | même principe que LAP (08/10, pont n° 237) et L02-310 au niveau global ; aucune des deux sources ne cite l'autre |

### 7.6 Ce qui n'a pas été examiné (seconde passe)

- La note PAIRES_EGALES_ET_BLOC_DOUZE (19/10), citée seulement à travers la note BUDGET du 20/10.
- La preuve de U16 ≤ 1168 : lue, mais ni le PL ni le tenseur cubique n'ont été refaits.
- La source de « m ≤ 10 » (Codex) : introuvable ; seule la borne A1^m, m ≤ 44, est prouvée dans les fichiers lus.
- L'étape finale du §5 de la note 176 (bloc 3 × 3 du complément de Fano) et la note 171.
- Les fiches L11a à L11f, ligne à ligne : je n'ai lu que les entrées citées, à partir du matériau.
- L'effet de a₈ ≤ 1168 et de b₁ ≤ 24 dans les PL du rang 43 : aucun PL n'a été lancé.
- Le résultat de la vérification V2 sur DISC (R3-01) : pas encore disponible quand j'ai écrit.
