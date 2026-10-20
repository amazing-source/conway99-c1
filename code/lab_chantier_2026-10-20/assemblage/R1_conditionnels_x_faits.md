# R1 : conditionnels × faits (phase de recombinaison du 20/10/2026)

Agent R1. Matériau : `assemblage/MATERIAUX_BRUTS_partiel.md` (lots L01 à L08 et L10) et `assemblage/MATERIAUX_BRUTS_L09.md`
(lot L09), lus en entier, avec les fiches `fiches/*.jsonl` et `assemblage/INDEX_RESULTATS.tsv`. Les lots L11a à L11f (pont)
sont traités en seconde passe (§9, annexe B). Les combinaisons sont dans `R1_conditionnels_x_faits.jsonl` (R1-01 à R1-30 en
première passe, R1-31 à R1-42 en seconde passe). La table complète des 858 conditionnels de la première passe est en annexe A ;
celle des 129 conditionnels L11, en annexe B.

## 0. Résumé

1. **Aucune exclusion du graphe, de C1 ou d'un rang n'apparaît en croisant les conditionnels avec les faits établis.** Toutes
   les chaînes qui mènent à « pas de Conway » gardent au moins une hypothèse ouverte. Vérifié aux sources pour toutes les
   combinaisons qui semblaient fermer.
2. **Hypothèse X prouvée ailleurs, cas important : la classe DISC « 14 » est exclue** (piste L09-501/508 du coordinateur).
   Les lemmes L4 (k pair) et L17 (det K₋₄ = 2²¹·7^k) imposent la classe 2 à tout mineur 30×30 de 8T, et la classe 1 à tout
   mineur 40×40 de 15U. Ce point est DÉJÀ CONNU : il est écrit dans NOTE_PROOFS_1410 (SQ3) et codé dans `disc_scan.py`, le
   15/10. Il a ensuite été perdu dans EXT84, REVUE_GLOBALE, `disc_batch.py` et le code de Codex (`DISC_CLASSES = ((2,14),(1,7))`).
   C'est un filtre plus fort, mais il ne tue aucun objet connu : les 645 germes de rang 30 échouent déjà (R1-01).
3. **Deux autres hypothèses sont prouvées ailleurs, sans effet d'exclusion :**
   - x₅₈ = x₅₉ = 0 découle du lemme de variance, sans les certificats de Codex (R1-21) ;
   - le dictionnaire de rangs du dépôt externe, r_ext = r − 1, est établi (R1-02).
4. **Hypothèses réfutées par un fait établi :**
   - les branches externes n3 = 705 et n3 = 708 sont vides, car n3 = 4158 − 3P ≥ 1602 (R1-03 ; trouvé aussi par R2-09) ;
   - le plafond de torsion « P ≥ 1152 » est impossible tel qu'énoncé ; la cible utile devient P ≥ 853 (R1-05) ;
   - F2-SRG est faux sous forme de famille (R1-18).
5. **Meilleures chaînes** (§3), chacune avec une seule hypothèse ouverte :
   - (T15) avec P ≤ 852 : c'est le quasi-raté le plus serré, P ≥ 866,25 contre 852 ;
   - (N9-NG) ⇒ (NG5) ⇒ (NG7) avec P ≤ 852 ;
   - (H-MATCH) avec L8 ;
   - R8 UNSAT ;
   - (H₃₇), pour le seul rang 37.
6. **Fait nouveau, borne contre borne (R1-19).** P ≤ 693 + 3G (note 08 de C2, avec Lou–Murin) et 3P + 4G ≤ 2772 redonnent
   exactement P ≤ 852 = ⌊11088/13⌋. L'agent R2 l'a trouvé indépendamment (R2-01, §8).
7. **Seconde passe (§9)** : pas d'exclusion nouvelle ; les cinq pistes du coordinateur sont déjà connues ou dominées ; une
   correction de cette première passe (R1-40) ; deux combinaisons nouvelles sans exclusion (R1-36, R1-37).
8. **Incohérences relevées** (§6) : classes DISC, compte des 174 noyaux, « rang 42 » externe, statuts de F2-SRG, statut de
   « rang 37 ⇒ P > 285 », borne b₂ ≥ 968 au rang 43 (signalée aussi par R2). S'y ajoutent huit redécouvertes datées.

## 1. Méthode et conventions

- **Extraction.** 858 énoncés conditionnels ont été extraits mécaniquement des sections « conditionnels » des deux matériaux,
  puis annotés à la main un par un (annexe A).
- **États de l'hypothèse X.**
  - *prouvée* : X est établie ailleurs, avec la source.
  - *réfutée* : X est fausse, en précisant la version touchée.
  - *ouverte* : ni preuve ni réfutation dans le matériau.
  - *chaîne* : X est la conclusion d'un autre conditionnel du matériau.
- **Trois états auxiliaires**, pour ne rien forcer :
  - *fait* : le conditionnel est lui-même un résultat établi sur un cas. X décrit une configuration, et l'énoncé dit qu'elle est
    impossible ou qu'elle a telle structure. Il sert de fait aux autres conditionnels.
  - *caduque* : le cas de X est clos par une autre route. Cela couvre C2 (route C), C3 (Lean), les valeurs de k hors de la
    fenêtre {22, …, 28}, et les lignes de rang externes déjà exclues.
  - *critère* (et *hors cible*) : un critère méthodologique, une équivalence avec le but, ou un objet autre que srg(99,14,1,2).
- **Bilan des 858 lignes** : 312 faits ; 264 caduques ; 171 ouvertes ; 44 réfutées ; 20 chaînes ; 20 critères ; 15 hors cible ;
  12 prouvées.
- **Statuts.** Ils sont recopiés des sources, sans jamais les rehausser. Le statut d'une combinaison est celui de son maillon le
  plus faible. Mes propres dérivations sont marquées « P (agent R1, non relue) ».
- **Vérifications aux sources** faites pour ce rapport, avec lecture directe des fichiers :
  - DISC : NOTE_PROOFS_1410, EXT84, REVUE_GLOBALE, `disc_scan.py`, `disc_batch.py`, `conway_core_repair.py`, relectures 02 et 05 ;
  - L4 et L17 : `30_LEMMES.md` ;
  - THREE_RESULTS et AUDIT_EXCLUSIONS (T8, T15, NG5, K22) ;
  - NOTE.md du programme thêta : définition de L1, identité 17.100, chemin critique (6) ;
  - note 08 de c2-experimental (n₃, coins) ;
  - README du dépôt externe (vague 42) ;
  - HANDOFF de c2-aws (« rang 37 ⇒ P > ~285 ») ;
  - V15 de Codex (bords 43 et 44) ;
  - PASSATION et `global_two_forced_shells` / `global_short_spectra_audit` de Codex (U16) ;
  - AUDIT_C1_ANNEXE (174 noyaux) ;
  - notes/102 (forme de Smith de Seidel).

## 2. Hypothèses prouvées ou réfutées par un fait établi

### 2.1 Prouvées

| combinaison | conditionnel(s) | fait qui prouve X | effet |
|---|---|---|---|
| **R1-01** | L09-COND-242, L09-COND-249, L04 CND-15 (H) : « la classe 14 de DISC est exclue » | L4 (k pair, P [C]) + L17 (det K₋₄ = 2²¹·7^k, P [C sur BvLS]) ; fenêtre r ∈ {37, …, 43} | classe DISC de 8T : **2 seule** ; de 15U : **1 seule**. Le « 2 ou 14 » de la re-dérivation d'EXT84 venait de det K_T = 2²¹·7^a avec a non identifié à k |
| **R1-21** | L06 COND-42 : x₅₈ = x₅₉ = 0 « si les certificats de Codex tiennent » (E) | lemme de variance (L09-COND-053, P, 25/09) : un graphe 4-régulier induit à 10 sommets a c(F) = −1 < 0 ; aussi e(S) ≤ 19 pour s = 10 (NOTE_NIGHT) | X établie sans certificat ; DÉJÀ CONNUE en substance (25/09, avant le 08/10) |
| **R1-02** | L03a-103 (H) : dictionnaire r_équipe = r_ext + 1 | dérivation R1 (ci-dessous) ; forme de Smith de Seidel 1^{14+k}… (notes/102, P) ; « rang 37 ⇔ Seidel de 7-rang 36 » (COND-L10-29) | les conditionnels externes aux lignes r_ext ≤ 34 sont caducs ; W66 ⟺ L2 + L22 |

*Preuve du dictionnaire.* Sur F₇, posons B = A − 3I.
- On a 2A − J + I ≡ 2B − J. De plus B·1 = 11·1 ≡ 4·1 et J·1 = 99·1 ≡ 1, donc (2B − J)·1 = 0.
- Si Bx = 0, alors 4(1·x) = (B1)·x = 1·(Bx) = 0, donc Jx = 0. Ainsi ker(2B − J) ⊇ ker B ⊕ F₇·1.
- D'où rang(2B − J) ≤ rang B − 1. Et rang(2B − J) ≥ rang(2B) − rang(J) = rang B − 1.
- Donc rang₇(2A − J + I) = rang₇(A − 3I) − 1. ∎

*Preuve directe de la classe 2.* La classe de det K₋₄ est le produit de deux classes :
- celle de det L₋₄ = 9·7^(r−1) (NOTE.md §1, rank7.tex), soit 1, car r est impair ;
- celle du mineur (E₋₄)_{N(x)} = (3I − A_N + J/9)/7, de déterminant 2²⁵/(9·7¹⁴), soit 2.

On obtient la classe 2, comme L4 + L17 et la relecture 05 §6.3. Côté U, le même calcul donne la classe 1.

### 2.2 Réfutées

| combinaison | conditionnel(s) | fait qui réfute X | version touchée |
|---|---|---|---|
| **R1-03** | dépôt externe : C-14 à C-21, C-51 (L03a) ; K3 à K10 (L03b) ; lemmes ouverts O-18, O8 à O10 | n3 + 3P = 4158 (externe, VER) et P ≤ 852 (C) ⇒ **n3 ≥ 1602** | toutes les branches n3 = 705 et n3 = 708 (cas vides). L'extrémité haute n3 = 4158 (P = 0) reste ouverte |
| **R1-05** | L01 #47, L09-LEMME-002, L09-COND-036, -037, -087, L05 O10 : « plafond de torsion P ≥ 1152 » (ou n₃ ≤ 704, Σ_x\|W(x)\| ≤ 1409, H ≤ 209 988) | P ≤ 852 (C) | l'énoncé tel quel est impossible. La cible utile devient P ≥ 853, c'est-à-dire n₃ ≤ 1599 ou Σ_x\|W(x)\| ≤ 3198 |
| **R1-18** | L09-COND-028 / L09-LEMME-004 : F2-SRG, « tout PQ(2,t,2) est grid-full » | les 7 srg(243,22,1,2) connus autres que BvLS ne sont pas grid-full (13 à 31 grilles par sommet contre 55) | forme de famille ; la forme « 99 » équivaut à la non-existence (L1) |

Les autres réfutations de l'annexe (N9, NOGRID, ODD9, (A), (H3), (H4), (R7) sans « NG », KER-SYM universelle, SQ30, etc.) sont
celles des sources. La version touchée y est rappelée. **Aucune d'elles ne touche la version restreinte encore utilisée**
(N9-NG, R7-NG, KER-SYM-14, N15).

### 2.3 Liens contrôlés qui n'existent pas (faux amis évités)

- **« ext : rang 42, 0 survivant »** (L03a B-43). C'est la vague 42, qui prouve rang_F7(M) ≥ 27. Ce n'est pas une exclusion
  de r_ext = 42, qui exclurait le rang 43 de l'équipe (R1-23).
- **U16 ≤ 1168** (L05-224, Codex). Cette borne vaut pour un hôte fixé ; la source dit « No bound on the total number of graph
  eigenfunctions is inferred ». Elle ne remplace donc pas a₈ ≤ 6930. Sinon N16 deviendrait inutile au rang 37, puisque
  350·1168 = 408 800 < 447 412 (R1-13).
- **« rang 37 ⇒ P > ~285 »** (L02 A#14, E). C'est un comptage de collisions flottant. Codex conclut le lendemain que les
  plafonds ne donnent même pas P > 0 (L05-063). Il ne faut pas l'utiliser pour vider le monde P = 0 au rang 37 (R1-27).
- **Filtre des deux retournements** (L05 K23, « pour TOUT SRG »). Il ne dépend pas de l'exclusion de C2 : il repose sur le
  théorème de majorité (R1-20).

## 3. Chaînes classées

Les chaînes sont classées par ampleur de la conclusion : graphe, puis C1, puis rang, puis cas. À ampleur égale, elles sont
classées par le nombre d'hypothèses ouvertes, puis par la forme de l'hypothèse restante. Une inégalité moyennée qui tolère des
exceptions passe avant un énoncé exact sur tous les blocs. Celui-ci passe avant un calcul fini de coût astronomique. Ce dernier
critère est un jugement de l'agent R1, à discuter. « Hypothèses ouvertes » désigne l'ensemble minimal de ce qu'il faut encore
prouver.

| rang | chaîne | ampleur | hypothèses ouvertes (minimal) | maillons établis (statut) | données, écart |
|---|---|---|---|---|---|
| 1 | **(T15) + P ≤ 852** (R1-06) | graphe | (T15) : tout bloc PSD de nullité ≥ 14 a t(l) + t(m) ≥ 15. Une forme affaiblie suffit : **vrai pour tous les blocs sauf au plus 34** | 36P = Σ_blocs (t(l) + t(m)) (P) ; P ≤ 852 (C) | 558 structures ν = 14, toutes avec t(l) + t(m) ≥ 16 (familles h et G1, biais reconnu). **Écart 866,25 contre 852**. Variante (T8) ⇒ P ≥ 924 |
| 2 | **(N9-NG) ⇒ (NG5) ⇒ (NG7) + P ≤ 852** (R1-07) | graphe | une seule parmi N9-NG ⟺ rang(F) ≥ 12, NG5, NG7 ou NG14. Sous-routes : ODDCONST + EVEN′ ; SYM + QUOT ; ODD-PURE + rang Z ≥ c − 1 ; SYM6 + D9 ; rang S ≥ 9..12 | NG5 ⇒ c(l) ≥ 5, g ≥ 4, t ≥ 8 ⇒ P ≥ 924 (P, vérifié par Codex) ; ≥ 254 blocs non grille à min t ≤ 7 (P) | 97 structures non grille conformes, **56 à l'égalité**. Le cas c(l) = 4 à nullité 13 est atteint (marge nulle). N9 (avec grilles) est réfuté. *Seconde passe* : ces structures sont impossibles dans Conway, ce ne sont pas des indices (R1-40) |
| 3 | **(H-MATCH) + L8** (R1-08) | graphe | (H-MATCH), ou (H-INV), ou (S1) + (S2) | H-MATCH ⇒ point de Hamming (P, relu par un agent) ; L8 (P, preuve à la main notes/105) ou Makhnev 1988 (cité) ou ρ ≤ 191 (P) | 416 classes de noyaux ; ≈ 853 000 structures (copie git b0cc3de) ou ≈ 1,14 M (addendum), aucune structure cassée de nullité ≥ 14 (fiche L07-276, S) ; route locale déclarée épuisée le 16/10 (fiche L07). *Seconde passe* : données hors de Conway (R1-40) |
| 4 | **R8 UNSAT** (R1-09) | graphe, tout rang | R8 (calcul fini) | R8 relâche la 5ᵉ étoile (P, audit du modèle du 20/10) | coût 5·10⁷ à 10¹² h-cœur (2·10⁴ à 4·10⁸ avec un cassage idéal) ; aucun germe de rang 30 ne reçoit de colonne |
| 5 | **(R7-NG) + L22** (R1-10) | graphe | R7-NG : bloc PSD sans grille ⇒ rang_F7(8T_S) ≥ 29 | 7-rang ≤ r − 15 ≤ 28 (P) ; ≥ 396 blocs non grille (P) | 6 122 blocs non grille, 7-rang ≥ 30 observé ; jugé « non crédible » (marge 1) ; R7 sans « NG » réfuté (E7). *Seconde passe* : blocs impossibles dans Conway (R1-40) |
| 6 | **Route c** (R1-14) | graphe | registre c = 3 (35 gabarits) ; branche c ≤ 2 (≈ 10⁷ gabarits) | c ≥ 4 exclu (S, sans certificat portable) ; « une droite à c ≤ 4 » déjà P par P ≤ 852 | variante : (B′) + [m ≥ 2 exclu] |
| 7 | **Q7 + P ≤ 852** | graphe | Q7 (⟸ ODDCONST + SYM6) | réduction de résonance (P) | — |
| 8 | **174 noyaux** (K01) | graphe | aucun des 174 noyaux de 14 sommets ne se prolonge | motif obligatoire de Makhnev (cité) ; 373 → 310 → 174 (C) | pilotes sans gain |
| 9 | **Normes 18 et 26 de L1** (R1-13) | graphe | exclure les vecteurs de L1 de normes 18 et 26 | couverture universelle de Codex (P, non relue), valable à tout rang | mondes de norme 18 : ≥ 10¹³ opérations |
| 10 | **Cadre coclique + α ≥ 21** (R1-17) | graphe | deux hypothèses : le cadre et α ≥ 21 | α ≤ 22 ; α ≥ 13 (externe) | écart 13 contre 21 |
| 11 | **(S3) + C3 ; (F16) + C2** (R1-24) | graphe | (S3) ou (F16) | C2, C3, C7 et ordre 11 exclus (statuts mixtes) | (S3) : aucun contre-exemple parmi les srg λ = 1 connus ; aucun mécanisme |
| 12 | **Symétrie forcée** (R1-16) | C1 | un bord positif inévitable de groupe ≥ 3 (43 sommets) ou ≥ 2 (44) | bords positifs 43/44 dans tout Conway, ≤ 2 complétions (P) | les bords existants ne sont pas structurellement fixés : aucun candidat |
| 13 | **(H₃₇)** (R1-11) | rang 37 | test d'étoile sur toutes les classes à t ≤ 7 (calcul fini) | Théorème 6.1 (P, non relu par un tiers) ; P ≤ 852 (C) | 1,87·10¹¹ classes, environ 6·10⁴ h-cœur ; 33 754 droites tirées, toutes UNSAT (E) |
| 14 | **(K22)**, ou « 7-rang ≥ 25 » | rang 37 (et 39) | K22 (sur les blocs non grille, cela suffit) | 7-rang ≤ r − 15 (P) | 331 objets de 7-rang 25, 29 ou 30 |
| 15 | **Mondes au rang 37** (R1-12) | rang 37 | N16, N18, c₂₀ ≤ 4 (trois) | identité 17.100 (C/E) ; b₃ ≥ 45 898 (C) ; N14 (E) | sans N18 la route échoue : 560 560 > 447 412 |
| 16 | **Monde P = S = 0 au rang 37** (R1-15, R1-36) | cas | *seconde passe* : (B″) seule ; en première passe : NT et (a′) uniforme | maille ≥ 5 ⇒ connexe au rang 37 (E) ; le monde est contenu dans ¬(B) | — |
| 17 | **S0 au rang 43** (R1-25) | cas | borne ≤ 2288 | il en faut ≥ 2289 + 15g (P) | — |
| 18 | **Monde ¬(B)** (R1-36, seconde passe) | cas | (B″) : aucun bloc PSD de nullité ≥ 14 à deux droites c = 1 (découle de (B′), NG5, N9-NG ou ODD-PURE) | grille ⇒ droite spéciale (P) ; P ≥ 694 ⇒ grille (P) | dans ce monde ρ = 0 et P ≤ 693 |
| 19 | **Coin sans grille du rang 37** (R1-37, seconde passe) | cas | K24 (τ ≤ P/2) et canaux hors C6 < 6,04 M (PL flottant) | τ ≤ P ≤ 693 (P) | masses 7 à 9 : bornes certifiées de 20 à 35 fois la marge ; optimum du PL (P = 780) hors du domaine prouvé |

*Lecture.* Les rangs 1 à 3 sont trois formes d'un même manque : un **plafond local** sur les blocs à quatre étoiles de
nullité ≥ 14. Il porte sur les transversales (T15), sur la résonance (N9-NG) ou sur les couplages (H-MATCH). Le rang 1 est le
seul qui demande une simple inégalité numérique, en moyenne, avec une marge de 14,25 prismes. Les rangs 4, 6, 8 et 13 sont
finis mais coûteux. Aucun fait du matériau ne prouve l'une des hypothèses ouvertes de cette table. L'index a été vérifié : les
entrées P et C qui citent ces noms sont des implications, pas des preuves.

## 4. Quasi-ratés (écarts chiffrés)

| objets | ce qui est prouvé | ce qu'il faudrait | écart |
|---|---|---|---|
| P et (T15) | P ≤ 852 (C) | Σ_blocs (t(l) + t(m)) ≥ 15·2079, donc P ≥ 866,25 | **14,25 prismes** ; en moyenne t(l) + t(m) > 14,753, ou (T15) sauf au plus 34 blocs |
| P et (T8)/NG5 | P ≤ 852 | P ≥ 924 | 72 prismes |
| P, borne inférieure générale (plafond de torsion) | aucune borne inférieure prouvée ; au mieux P ≥ 231 sous la conjecture (P), non prouvée | P ≥ 853 | au moins 622 prismes entre ce minorant conditionnel et le seuil |
| nullité des blocs non grille, c(l) = 4 | données : ν ≤ 13 (égalité atteinte) | NG5 : ν ≤ 13 pour c = 4 | 0 relation (cas d'égalité) |
| 7-rang des blocs non grille | observé ≥ 30 | R7-NG : ≥ 29 | 1 (marge des données) |
| α | α ≥ 13 (externe), α ≤ 22 | α ≥ 21 | 8 |
| mondes au rang 37 | 350a₈ + 91a₉ + 13a₁₀ ≥ 447 412 ; a₁₀ ≤ 7920c₂₀ | c₂₀ ≤ 4 (avec N16, N18) | a₁₀ ≤ 31 680 contre ≥ 34 418 |
| S0 au rang 43 | il faut ≥ 2289 + 15g configurations | borne ≤ 2288 | 1 + 15g |
| P et G | P ≤ 693 + 3G (note 08) et 3P + 4G ≤ 2772 | — | sommet du domaine : (P, G) = (852,9 ; 53,3) ; à P = 852, G ∈ {53, 54} (R1-19) |

## 5. Candidats à la vérification adverse

Ordre de priorité : d'abord ce qui affirme un fait, ensuite ce qui affine un outil.

1. **R1-01 (DISC, classe 2 seule).** À contrôler :
   - le lemme DISC : classe commune des mineurs = classe de disc(Λ_8T) = 56³⁰/det K₋₄ ;
   - l'identité du k de L17 avec celui de L4 ;
   - la correction de `DISC_CLASSES` dans `conway_core_repair.py` (Codex) et de `disc_batch.py` ;
   - les exécutions avec `disc=True` dont un objet de classe 14 ou 7 aurait survécu. Je n'en ai trouvé aucune par grep, sans
     audit des journaux.
2. **R1-02 (dictionnaire de rangs).** Preuve en quatre lignes (§2.1), à relire. Vérifier aussi que le « r » des vagues
   externes 39 à 66 est bien rang_F7(2A − J + I).
3. **R1-19 (P ≤ 693 + 3G).** Vérifier deux choses :
   - c(y;ℓ₁,ℓ₂) = 4 ⟺ grille, et chaque grille compte exactement 9 triplets ;
   - le certificat d'ordre 9 de Codex (11088/13) est-il cette combinaison ?
4. **R1-13 (couverture 18/26 sans la clause « 1316 » au rang 43).** Vérifier que « affine niveau 3, norme 37 » de Codex est bien
   un vecteur de L1 de norme 26, et que la construction de l'hôte vaut pour tout Conway.
5. **R1-06, forme affaiblie de (T15)** (« sauf au plus 34 blocs ») : calcul élémentaire à relire.
6. **R1-03 (n3 ≥ 1602).** Identification n3 externe = N₂ de l'équipe = n₃ des notes C1.
7. **R1-21 (x₅₈ = x₅₉ = 0).** Vérifier que x₅₈ et x₅₉ comptent bien des graphes 4-réguliers induits à 10 sommets (NOTE.md:2756).
8. **R1-18 (F2-SRG réfuté).** Définition de « grid-full » contre les comptes de grilles par sommet des srg(243).

## 6. Incohérences entre notes

| # | quoi | qui dit quoi, quand | effet |
|---|---|---|---|
| I1 | classes DISC | NOTE_PROOFS_1410 (SQ3) et `disc_scan.py`, LAB, 15/10 : classe 2 (k pair). EXT84 §1 et REVUE_GLOBALE, 16/10 : « 2 ou 14 ». `disc_batch.py` compte comme vivant tout germe dont les premiers d'exposant impair sont dans {2, 7}, 2 compris. Codex `conway_core_repair.py:36` : `DISC_CLASSES = ((2,14),(1,7))` ; journal de Codex (J:6193-6197) : « différente de 2 et 14 » | filtre trop faible chez Codex ; aucun résultat faussé (un filtre plus faible ne crée pas de fausse exclusion) |
| I2 | 174 noyaux | fiche L08-004 : « 174 noyaux : 63 exclus par positivité, 136 par certificat ». Source AUDIT_C1_ANNEXE : 373 → 310 → 174 | erreur de fiche |
| I3 | « rang 42 » externe | fiche L03a B-43 contre README externe : vague 42, rang_F7(M) ≥ 27 | intitulé trompeur (R1-23) |
| I4 | F2-SRG | L09-COND-028 « O » contre L09-COND-056 « R » pour des énoncés équivalents (grid-full ⟺ (∗) ⟺ n₃ = 0) | statut à aligner (R1-18) |
| I5 | rang 37 et P | L02 A#14 (LAB, 08/10, E) : « rang 37 ⇒ P > ~285 ». L05-063 (Codex, 09/10, P) : « plafonds trop larges pour déduire rang 37 ⇒ P > 0 » | l'énoncé E n'est pas un maillon (R1-27) |
| I6 | det K₋₄ | EXT84 : 2²¹·7^a (a libre). L17 : 2²¹·7^k | origine de I1 |
| I7 | norme 16 au rang 43 | L06-103 (LAB, 12/10) : « ou ≥ 1316 de norme 16 ». L05-224 (Codex, 05/10) : couverture 18/26 sans branche 16 | compatibles ; L06-103 est plus faible (R1-13) |
| I8 | réserve L02 β | la fiche L02 craint que les vecteurs forcés de L1 ne soient pas des vecteurs propres entiers ; NOTE.md §1 : « L1 and L have the same vectors of norm 14, 16, 18, 20 » | réserve levée (R1-12) |
| I9 | symboles | « n₃ » a trois sens (nombre de N3 = 4158 − 3P ; sommets denses en grilles ≤ 39 ; classe X₃ de T20). « c » en a deux (composantes de G_l ; arêtes de coins de la note 08) | piège de définition (R1-30) |
| I10 | b₂ au rang 43 | L05-029 : « b₂ ≥ 462 + 85b₁ + b₁²/2 ≥ 968 ». Pour b₁ = 0 l'expression vaut 462. Selon R2-03 et R2-21 (non vérifié ici), la borne forcée est b₂ ≥ 1000, et ≥ 1264 avec une racine | la condition « b₂ ≤ 967 ⇒ r ≠ 43 » (L06 COND-05) devient « b₂ ≤ 999 » ; elle reste une reformulation (R1-28) |

**Redécouvertes** (même résultat établi deux fois, avec les deux dates) :

| résultat | première date | redécouverte |
|---|---|---|
| L16 (P ≤ 1151) ⟺ n3 ≥ 705 | externe, vagues 20-23, 23/07/2026 | équipe, septembre |
| P ≤ 1150 ⟺ n3 ≥ 708 | externe, 23/07/2026 | Codex, 14/10 |
| L2 + L22 (r impair ≤ 43) ⟺ W66 (r_ext pair ≤ 42) | externe, juillet 2026 | équipe, septembre |
| α = 22 ⇒ design 2-(22,4,2) | externe, W3, 22/07/2026 | notes/94 (septembre) ; L07, 11/10 |
| π(L) ≠ 11 ⟺ q(T) ≠ 1 | Lou–Murin 2014 | externe ; équipe |
| deux cocliques de Hoffman se coupent en 1, 8 ou 15 points à k = 28 | notes/107, 25/09 | L06-027, 08/10 |
| x₅₈ = x₅₉ = 0 | notes/94, 25/09 | L06-107, 08/10, par certificats |
| tout Conway a un vecteur de L1 de norme 18 ou 26 | Codex, 05-06/10 | LAB, 12/10 |

## 7. Ce qui n'a pas été examiné

- **Les lots L11a à L11f** (messages du pont LAB ↔ Codex) : traités en seconde passe, à partir des fiches et du matériau
  extrait (§9). Les copies de `pont_codex/` n'ont été ouvertes que pour un grep ponctuel (classe DISC 14).
- **Le croisement bornes × bornes systématique.** Il relève d'un autre agent. Je n'ai traité que les bornes qui touchent un
  conditionnel (R1-05, R1-06, R1-13, R1-19).
- **Les chaînes internes à C2.** Je ne les ai pas recroisées. C2 est clos par la route C : 156/156, avec la réserve des
  2 479 669 paires de transfert jumeau non recertifiées et un statut sans relecteur humain. Ses conditionnels sont classés
  « caducs » en annexe.
- **Les sources de chaque conditionnel ne sont pas toutes ouvertes.** Je n'ai ouvert que celles des combinaisons qui semblaient
  fermer ou presque (liste au §1). Pour les autres lignes, l'état de X repose sur le texte des fiches et du matériau.
- **Le contenu des journaux d'exécution de Codex** avec `disc=True`. Aucune exécution, aucun calcul n'a été lancé. Seuls de
  petits scripts de lecture ont servi : extraction, annotation, contrôle du JSONL.
- **Les preuves de L4, L17, L8 et du Théorème 6.1.** Je ne les ai pas refaites. Deux points seulement ont été re-dérivés ici :
  - la classe 2 via det L₋₄, donc indépendamment de L17 ;
  - la propriété « une grille coupe une coclique de Hoffman en exactement 2 points » (R1-17).

## 8. Recoupements avec les agents R2 et R3 (fichiers déposés pendant ma passe)

Lecture limitée à un grep sur les chiffres clés ; je n'ai pas vérifié leurs dérivations.

| R1 | R2 / R3 | accord |
|---|---|---|
| R1-03 (n3 ≥ 1602, branches externes à 708 vides) | R2-09 | même conclusion, trouvée indépendamment |
| R1-19 (P ≤ 693 + 3G et 3P + 4G ≤ 2772 ⇒ P ≤ 852) | R2-01 (« P ≤ 852 par deux facettes ») ; R3 cite aussi l'inégalité de la note 08 | même conclusion, trouvée indépendamment |
| R1-20 (filtre des retournements, sans C2) | R2-13 (orbites de taille ≥ 16 sous les 2⁷ retournements) | compatible ; R2 va plus loin |
| R1-28 (b₂ au rang 43) | R2-03, R2-21 (b₂ ≥ 1000, ≥ 1264 avec racine) | R2 corrige la borne 968 ; voir I10 |

## 9. Seconde passe : lots L11a à L11f (pont LAB ↔ Codex)

Matériau : `assemblage/MATERIAUX_BRUTS_L11.md`, dont j'ai extrait les 129 conditionnels des tables « conditionnels » des six
blocs, et les fiches `fiches/L11a_pont` à `L11f_pont`. J'ai croisé les conditionnels L11 avec les faits L01 à L11, puis les
conditionnels L01 à L10 avec les faits nouveaux de L11. Pour ce second sens, j'ai parcouru les 57 faits L11 de statut P ou C
marqués « ABSENT DES NOTES ». Nouvelles entrées : R1-31 à R1-42. Les 129 conditionnels sont en annexe B.

### 9.1 Ce qui change par rapport à la première passe

1. **Toujours aucune exclusion** du graphe, de C1 ou d'un rang. Aucune hypothèse d'un conditionnel L11 n'est prouvée ailleurs
   au point de fermer une chaîne.
2. **Hypothèses prouvées, dominées ou réfutées par un fait établi** (aucune ne change une conclusion) :
   - « tout automorphisme non trivial déplace ≥ 13 sommets » (L11d-102) est dominé par Wilbrink 1984, Thm 1 : au moins 81
     sommets déplacés (R1-34) ;
   - au rang 43, la réserve « a₈ < 1316 » du conditionnel C2 de L11d est levée par L05-224 (déjà dans R1-13) ;
   - « chaque droite dans ≥ 5 grilles » (L11c K2) est dominé : 4 grilles par droite donnent déjà ρ ≥ 154 > 126 (R1-42) ;
   - réfutées à la source : L11b K11 et K12 (plancher certifié 16 496 > 13 900), H3 (L11d C8), (A) donc C9 et la forme
     locale de C10, MIX ≤ 2 ou 3, « aucun bloc à 4 relations mixtes », (A4), ODD9, (R7) sans « NG ».
3. **Correction de ma première passe (R1-40).** Les « données » citées dans R1-07, R1-08 et R1-10 sont des blocs impossibles
   dans Conway (L08-166 : rang Res ≥ 8 > r − 37). Je les retire comme indices.
4. **Deux combinaisons nouvelles, sans exclusion :**
   - R1-36 : (B) découle de P ≥ 694 (grille ⇒ droite spéciale). Dans le monde ¬(B), on a ρ = 0 et P ≤ 693. Une seule
     hypothèse, (B″), plus faible que (B′), viderait ce monde. Au rang 37, ce monde contient celui de P = S = 0 (R1-15).
     R1-15 n'a donc plus besoin de (NT) + (a′).
   - R1-37 : coin sans grille du rang 37. On a τ ≤ P ≤ 693, contre le seuil 535 ; R3-12 l'a vu d'abord. Avec K24 (ouvert),
     τ ≤ 346. L'optimum du PL de comptage (P = 780) sort du domaine prouvé P ≤ 693.
5. **Les cinq pistes signalées par le coordinateur.**
   - (1) DÉJÀ CONNUE (L08-033, -049, -168 ; R1-31). Même prouvée, (B′) ne donne pas d'exclusion seule : il faut [m ≥ 2 exclu].
   - (2) DÉJÀ CONNUE (R1-07 ; R1-32). La marge d'ODD-PURE n'est pas uniforme (L11e-130) ; les ≈ 7 444 côtés ne sont pas des
     indices.
   - (3) DÉJÀ CONNUE : session externe du 27/07 et Codex du 12/10. C'est un découpage complet, donc l'hypothèse équivaut au
     problème. Le dictionnaire « part 1 ⟺ barreau de prisme » est dérivé ici (R1-33).
   - (4) DOMINÉE par Wilbrink (R1-34).
   - (5) DÉJÀ CONNUE : fiche L11a et L06 BORNE-05 (R1-35).

### 9.2 Chaînes mises à jour

Les lignes 2, 3, 5 et 16 du tableau du §3 sont annotées. Deux lignes nouvelles, de portée « cas », y sont ajoutées
(18 et 19). L'ordre des lignes 1 à 17 ne change pas.

| chaîne | changement |
|---|---|
| (N9-NG) ⇒ (NG5) ⇒ (NG7) (R1-07, R1-32) | données retirées comme indices (R1-40) ; ODD-PURE : il faut un argument exact (L11e-130) |
| (H-MATCH) + L8 (R1-08) | données retirées comme indices ; au rang 37, NOTE_FUSION §4.2 la juge inutile si les droites c ≤ 2 meurent (E sur échantillons) |
| (R7-NG) (R1-10) | données retirées comme indices ; (K22) ⟸ (a′) aux paires c = 1 génériques |
| monde P = S = 0 au rang 37 (R1-15) | hypothèses ouvertes : (B″) seule, au lieu de (NT) et (a′) (R1-36) |
| nouveau : monde ¬(B) (R1-36) | (B″) ; ρ = 0 et P ≤ 693 dans ce monde |
| nouveau : coin sans grille du rang 37 (R1-37) | K24 et canaux hors C6 < 6,04 M, dans un PL flottant |

### 9.3 Quasi-ratés nouveaux

| objets | ce qui est prouvé | ce qu'il faudrait | écart |
|---|---|---|---|
| paires jumelles τ, rang 37, ρ = 0 | τ ≤ P ≤ 693 (P : note 249, note 08) | τ_n < 535 (seuil de LAB, H) | 158, soit 30 % (R3-12) ; 346 < 535 si K24 |
| budget 17,1 M (L11b-86, H) | — | canaux hors C6 < 6,04 M, sous K24 | masses 7 à 9 : bornes certifiées de 20 à 35 fois la marge (NOTE 17.89) |
| PL de comptage à ρ = 0 (NOTE 17.45) | optimum à P = 780, τ = 780 | P ≤ 693 + 3ρ (P) | optimum hors du domaine prouvé ; non recalculé |
| collisions, P = 0, rang 37 | 185,2 M (certifié) | < 3,84 M | facteur 34,6 (R1-38) |
| grilles par droite | ρ ≤ 126 (C) | q = 3 grilles partout exige ρ ≥ 116 | compatible ; q = 4 exclu (R1-42) |

### 9.4 Incohérences et pièges nouveaux

- **Statut de P ≤ 852** (R1-39). Le pont le donne C : certificat exact, identité revérifiée le 18/10. L08-067 le donne A + E.
  Ma lecture : C relatif au recensement d'ordre 9, le recensement étant A + E. La vérification est laissée à V1/V2.
- **Données des lois à quatre étoiles** : R1-40 (correction de ma première passe).
- **Retraits de LAB à ne pas réutiliser** (L11c-134) :
  - « au rang 37 le PL sans grille est au seuil » (16,06 M contre 15,98 M), calculé sur deux collections différentes ;
  - « 20,2 M avec classes jumelles de taille ≤ 2 ».
- **(A) = H3″ local** est réfutée par 52 contre-exemples exacts. Les conditionnels C9 et C10 de L11d qui en partent sont
  morts ; (B) et (C) restent ouverts.
- **Vocabulaire.** Dans la session externe, « r7 » (L03b-130) est le rang du projecteur 231 × 231 du graphe des triangles. Ce
  n'est pas r (complément de R1-30).
- **L11d-102** n'est qu'esquissé dans le pont. Il est de toute façon dominé (R1-34).

### 9.5 Recoupements avec R2 et R3 (seconde passe)

| R1 | R2 / R3 | accord |
|---|---|---|
| R1-37 (τ ≤ P ≤ 693 au coin sans grille) | R3-12 (« quasi-raté : … τ ≤ P ≤ 693 … écart de 158, soit 30 % ») | R3 l'a trouvé d'abord ; R1 ajoute K24 et le reste du budget |
| R1-36 (¬(B) ⇒ ρ = 0 ⇒ P ≤ 693) | R2 §2.2 (« rang 37 et tout G(T) connexe ⇒ ρ = 0 (donc P ≤ 693 …) ») | même implication, chez R2 au seul rang 37 |
| R1-34 (Wilbrink) | R3-06, R3-43 | Wilbrink est cité par R3 pour l'ordre 11 |
| R1-37 (seuils 25 201 ; 27 142 ; 33 780) | R2 l. 162 et l. 315 (R2-07) | mêmes chiffres |

### 9.6 Sources primaires ouvertes en seconde passe

- `work/exploration_2026-10-16/merge_2026-10-19/NOTE_FUSION_2026-10-19.md:100-260` (§1.3, 1.4, 3, 4.1 à 4.3) ;
- `work/c1_theta_lp_2026-10-07/NOTE.md:3440-3475` (17.88, 17.89) et `:3820-3850` (17.96) ;
- `Desktop/Recherche_Conway/c1-asymmetry-audit/notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md:3360-3400` (§75) ;
- `conway99-c1:main:notes/94_NUIT_LITTERATURE.md:95-135` (Wilbrink, Cesarz–Woldar) ;
- fiches L11a (§ recombinaison 3), L11b (§ 8.2.4) et L11d (§ 5, K1 à K8) ;
- `assemblage/R2_bornes_x_bornes.md:85-120` et `assemblage/R3_lemmes_analogies.md:120-132`.

### 9.7 Ce qui n'a pas été examiné (seconde passe)

- **Les textes des messages du pont** (`pont_codex/lots/L11x_pont.md`). Seuls les fiches et `MATERIAUX_BRUTS_L11.md` ont été
  lus ; les mentions « ABSENT DES NOTES » n'ont pas été recontrôlées sur les messages.
- **Le croisement exhaustif des 789 résultats L11 avec les 858 conditionnels de la première passe.** Seuls les 57 faits P ou C
  « ABSENT DES NOTES » ont été parcourus ; aucun ne prouve une hypothèse ouverte de l'annexe A.
- **Les vérifications confiées à d'autres agents**, non refaites :
  - fermeture c ≥ 4 face au bogue OR-Tools (V3) ;
  - décomposition de P ≤ 852, forme affaiblie de T15 et « aucune droite dans six grilles » (V1, V2) ;
  - DISC, R3-02 et R2-03.
- **Aucun calcul.** Le PL de R1-37 n'a pas été relancé. C'est un PL flottant (HiGHS), de durée non mesurée ici, à refaire avec
  `lp_family.py` et les facettes P ≤ 693 + 3ρ et τ ≤ P.


## Annexe A. Table de tous les conditionnels (858), par lot

Colonnes :
- **réf.** : identifiant de la source quand il existe, sinon « l.N » ;
- **ligne du matériau** : « MB:N » renvoie à `MATERIAUX_BRUTS_partiel.md`, « MB9:N » à `MATERIAUX_BRUTS_L09.md` ;
- **énoncé** : verbatim tronqué à 150 caractères, avec « ¦ » à la place des séparateurs de colonnes d'origine ;
- **état de X**, **lien R1**, **note**.

Pour les lignes « fait », la note « énoncé établi (statut de la source) » renvoie au statut donné dans la colonne d'origine.

### A.1 L01 (origines de C2, §8.1) — 46 conditionnels

Répartition : caduque 33 ; fait 4 ; prouvée 3 ; hors cible 3 ; ouverte 2 ; réfutée 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| l.15 | MB:15 | [COND] si aucune involution n'existe (C2 exclu) alors ¦Aut(Γ)¦ ∈ {1,3} ¦ P (littérature, L01-01) ¦ X = objectif de la branche ¦ conway99-involution:ma… | prouvée | R1-24 | C2 exclu par la route C (statut mixte) ⇒ ¦Aut¦ ∈ {1,3} |
| l.16 | MB:16 | [COND] si C2 et C3 sont exclus alors tout Γ est asymétrique (C1) ¦ P (littérature) ¦ ouvert à cette date ¦ conway99-involution:master:README.md:13 [A] | prouvée | R1-24 | C2 (route C, statut mixte) et C3 (Lean) exclus : asymétrie |
| l.17 | MB:17 | [COND] si Stage Q (matrices Q_out) est UNSAT dans les trois cas sib/one/dis avec preuves vérifiées alors pas d'involution, ¦Aut¦ ∈ {1,3} ¦ P (Stage Q … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.18 | MB:18 | [COND] si le cas sœur est exclu à la main alors un tiers des instances tombe ¦ H (estimation) ¦ O ¦ conway99-involution:master:report/dossier_chercheu… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.19 | MB:19 | [COND] si une classe du recensement d'ordre 7 à parité constante contredit la parité de ses copies σ-invariantes alors la branche involution meurt ¦ P… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.20 | MB:20 | [COND] si le cœur μ_c = τ_c = π vaut en une ligne alors contradiction avec ¦Σ¦ ≤ 4 (donc prouver le cœur = prouver « pas d'involution ») ¦ P ¦ X non é… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.21 | MB:21 | [COND] si le lemme de l'étoile libre (forme locale : RSF(star(c)) UNSAT quand aucune grille ne contient c) est vrai alors le cas involution est clos ¦… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.22 | MB:22 | [COND] si un « accident 7-adique » à k = 28 est toujours isotrope alors k = 28 exclu ; s'ils contiennent un sous-espace totalement isotrope de dimensi… | ouverte |  | = L09-COND-199 (accidents 7-adiques à k = 28) |
| l.23 | MB:23 | [COND] si 13 classes singulières indépendantes mutuellement orthogonales existent dans D− et dans D+ alors contradiction avec « produit des types = mo… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.24 | MB:24 | [COND] si toutes les paires sont frères (D(U) = U′) alors contradiction ¦ P ¦ — ¦ MATH_C2_PROGRAMME.md:106 [B] | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.25 | MB:25 | [COND] si un sommet est plat alors contradiction (tout srg(99,14,1,2)) ¦ P ¦ — ¦ MATH_C2_PROGRAMME.md:553 [B] | fait |  | général (Théorème D′ ⊂ L8) |
| l.26 | MB:26 | [COND] si (seconde détermination indépendante de r mod 2 ou de k) alors conclusion par la voie 7-adique ¦ P (forme) ¦ O ¦ MATH_C2_PROGRAMME.md:70 [B] | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.27 | MB:27 | [COND] si le lemme de l'étoile libre (forme locale) est vrai alors C2 n'existe pas ¦ P (réduction note 20 §0) ¦ O ¦ conway99-c2-experimental:master:no… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.28 | MB:28 | [COND] si toutes les instances I(τ) (3 308 classes ; puis (A) 1 507 types à pivots + famille tout-dis (B)) sont UNSAT alors pas d'involution ¦ P (comp… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.29 | MB:29 | [COND] si Σ = ∅, tous les carrés « un bloc », et les 79 systèmes locaux sont UNSAT (DRAT) alors l'involution est impossible dans ce cas (M1, mélanges,… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.30 | MB:30 | [COND] si toutes les classes pertinentes à ≥ 6 étiquettes sont UNSAT sauf (0,6) alors tout bloc est (0,6) et T = K7 (tout-tordu) ¦ P ¦ O ¦ note 45:118… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.31 | MB:31 | [COND] si aucune enveloppe U de la liste de Borcherds (156) ne porte le repère (F) alors pas d'involution ¦ P (cadre Sol/Astra relu par structures ; p… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.32 | MB:32 | [COND] si le modèle joint « graphe exact + témoin court » est infaisable pour les 11 couples (n,k) alors pas d'involution ¦ P (sous couverture et scan… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.33 | MB:33 | [COND] si n3 < 2079 alors Γ contient une grille (tout srg(99,14,1,2)) ¦ P ¦ — ¦ SYNTHESE.md:20 [C] | fait | R1-19 | général (note 08 + Lou–Murin) : P ≤ 693 + 3G |
| l.34 | MB:34 | [COND] si une parité de ¦Σ¦ était obtenue alors la moitié des 10 survivants tombe ¦ H ¦ O (exigerait l'ordre 9) ¦ notes/22_REVUE_COMPLETE.md:148,153 [… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.35 | MB:35 | [COND] si la propagation (P) (une seconde réflexion automorphe) vaut alors C2 meurt (équivalence) ¦ P (dit par la source) ¦ O (résidu de dimension 30)… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.36 | MB:36 | [COND] si un couple (N,D) explicite satisfait (S) et L_N alors il existe un graphe de Conway avec involution à un point fixe (reconstruction vérifiée)… | hors cible |  | sens construction (existence) |
| l.37 | MB:37 | [COND] si EX est faux alors aucune involution à un point fixe ; avec F0, aucune involution (C2 exclu) ¦ P (T4 relu ; F0 cité/reprouvé, L02) ¦ non-EX é… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.38 | MB:38 | [COND] si la rigidité de signe (R) vaut (au plus une signature faisable par couple non signé complet) alors le problème se réduit à la couche non sign… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.39 | MB:39 | [COND] si l'on obtient G mod 2 (nombre de grilles 3×3) indépendamment alors n2 ≡ G (mod 2) contraint le type 2 ¦ P ¦ O ¦ RESULTS.md:248-249 [D] | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.40 | MB:40 | [COND] si 156/156 (route C) et T16, T18, T20, Borcherds, oddité, complétude des énumérations et code du moteur sont acceptés alors aucun srg(99,14,1,2… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.41 | MB:41 | [COND] si un (Q,N) exact satisfait le système couplé alors un graphe de Conway existe (reconstruction puis vérification A² + A = 12I + 2J) ¦ P ¦ O ¦ c… | hors cible |  | sens construction (existence) |
| l.42 | MB:42 | [COND] si deux complétions intégrales existent pour un même N alors elles diffèrent sur exactement 8 blocs ambigus (r = 8) ¦ P (T2, non audité) ¦ — ¦ … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.43 | MB:43 | [COND] si g⁻ = 18 et g⁻ = 20 sont exclus et si au moins un Q_c est inversible alors pas d'involution ¦ P (Astra 6, conditionnel) ¦ O (la condition Q_c… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.44 | MB:44 | [COND] si un argument 7-adique n'utilise que « 7 ¦ t, 7 ∤ v » et les identités de la famille srg(2m²+1,2m,1,2) alors il exclut d'un coup 99, 6 273 et … | ouverte |  | argument de famille : aucun |
| l.45 | MB:45 | [COND] si un bloc est plein alors g = 20 (donc à g = 18 ni bloc plein ni résidu AD) ¦ P ¦ — ¦ external_structures/JOURNAL.md:839-840 [F] | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.46 | MB:46 | [COND] si une SRG contient la boule tordue d'Astra (dossier 5) alors k ≥ 24 ¦ P (relu) ¦ — ¦ astra/RAPPORT_ASTRA_DOSSIER5.md:74 [F] | fait |  | boule d'Astra ⇒ k ≥ 24 |
| l.47 | MB:47 | [COND] si l'on avait un plafond de torsion (P ≥ 1152, C1) alors contradiction avec L16 (P ≤ 1151) ¦ P ¦ O ¦ external_c1/notes/99_VERROU_BOULES_DE_DROI… | réfutée | R1-05 | P ≥ 1152 impossible (P ≤ 852, C) |
| l.48 | MB:48 | [COND] si C2 (Théorème 1.1) et les ordres 3, 7, 11 sont exclus alors un srg(99,14,1,2), s'il existe, est asymétrique (Corollaire 1.2) ¦ P ¦ Théorème 1… | prouvée | R1-24 | C2 (route C, statut mixte) et C3 (Lean) exclus : asymétrie |
| l.49 | MB:49 | [COND] si y1 a une racine r avec (r,y1) = ±2 alors y1 ne porte aucun repère quel que soit y2 (Corollaire Y1, avec T18, T20) ¦ P (relu) ¦ — ¦ HANDOFF_2… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.50 | MB:50 | [COND] si un repère physique 42 + 7 + 2 existe dans une enveloppe U alors U n'est ni D8^3, ni à composante D11, ni à E8 ou D_n (n ≥ 12) ou A_n (n ≥ 22… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.51 | MB:51 | [COND] si U est sans racines alors le repère force 24 ombres orthogonales et un code autodual doublement pair [24,12,8] ¦ P ¦ — ¦ BILAN_AUDIT_INDEPEND… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.52 | MB:52 | [COND] si g⁻ = 16 alors Γ contient un prisme induit (donc P > 0) ¦ C (deux implémentations) ¦ — ¦ sol/DOSSIER_G16_PRISME.md:3-5 [H] | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.53 | MB:53 | [COND] si une involution a l'étoile A111111 (3,3) alors contradiction (g⁻ ≥ 22 > 20) ¦ C ¦ — ¦ sol/files/outputs__fermeture_A33__RAPPORT.md:3-6 [H] | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.54 | MB:54 | [COND] si les lemmes T22 et T24 (aucune fonction propre entière σ-impaire pour −4 de somme de carrés 11, resp. 12) sont prouvés alors NON-EX (pas d'in… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.55 | MB:55 | [COND] si la condition de piège (ombre E ≥ 11,5) et l'absence de vecteur entier 1 ≤ E ≤ 10 valent alors s ≥ 12 paires de fonctions propres caractérist… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.56 | MB:56 | [COND] si l'on exclut à la main les fonctions propres caractéristiques (±2 sur un bloc, ±1 sur les 42 orbites) alors la région tombe ¦ P (forme) ¦ O ¦… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.57 | MB:57 | [COND] si l'heptade (sept h orthogonaux admissibles partitionnant les s classes) n'existe dans aucune paire de région alors ces paires sont exclues sa… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.58 | MB:58 | [COND] si l'article d'ordre 2 recertifie les transferts (4 163 099 paires, ≤ 2 479 669 hors Corollaire 7.3) alors le Théorème 1.1 est établi au standa… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.59 | MB:59 | [COND] si un srg(243,22,1,2) a un partage régulier et une classe de parité triviale alors il est l'un des quatre connus (BvLS, jumeau, Γ3, Γ4) ¦ E (no… | hors cible |  | srg(243) |
| l.60 | MB:60 | [COND] si un mot binaire non nul de ker7(A + 4I) existe alors Γ a une partition équitable [[10,4],[7,7]] (w = 63) ou une coclique de Hoffman de taille… | fait |  | mots binaires de ker₇(A + 4I) |

### A.2 L02, partie K (campagne de calcul) — 11 conditionnels

Répartition : caduque 10 ; ouverte 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| K-C1 | MB:249 | K-C1. **Corollaire Y1 (y1 fixé).** Si U (réseau du repère, Théorème R) contient une racine r avec ¦(r,y1)¦ = 2, alors aucun repère n'a cette normale y… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| K-C2 | MB:250 | K-C2. **Conséquence.** Sous R, T18, T20 : toute racine r vérifie ¦(r,y1)¦ <= 1 et ¦(r,y2)¦ <= 1, donc (r,y1)^2 + (r,y2)^2 <= 2. Statut P (Codex). Sour… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| K-C3 | MB:251 | K-C3. **Si T18 et T20 sont vrais** (et le pont racine -> fonction propre), alors les 13 réseaux 001, 002, 003, 005-009, 011-015 sont exclus (5 190 752… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| K-C4 | MB:252 | K-C4. **Règle du vecteur caractéristique.** Si z est caractéristique de norme 16 dans U et (z,y1)^2 + (z,y2)^2 > 66, la paire (y1, y2) ne porte pas de… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| K-C5 | MB:253 | K-C5. **Récurrence sur le nombre de racines (jumeau plus riche).** Si un repère existe, en choisir un dans un réseau de la liste ayant le plus de raci… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| K-C6 | MB:254 | K-C6. **Transfert canonique.** Si le jumeau a le même type de racines, porté par un seul réseau de la liste, et une clé intrinsèque strictement plus p… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| K-C7 | MB:255 | K-C7. **Si la recertification jumelle aboutit** (chaque paire du résidu en classe W, Z, M ou C, et les paires H exclues par le moteur avec FD_TWIN=0 e… | ouverte |  | recertification jumelle garée : réserve interne de C2 |
| K-C8 | MB:256 | K-C8. **Lemme du noyau rigide (H2).** Un h d'empreinte nulle n'est possible que si les deux voisins pairs ont le même nombre de Coxeter H et si U a un… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| K-C9 | MB:257 | K-C9. **Loi K.** K + E(y1) + E(y2) = 3¦Phi¦/4 + 8 ; une paire K = 0 n'existe que si les deux voisins pairs ont le même nombre de Coxeter (h1 = h2). St… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| K-C10 | MB:258 | K-C10. **Complétude des règles de témoins pour E <= 10.** E = 8 : vecteur de norme 3 avec Y = 13 ; E = 9 : racine avec Y = 5 ; E = 10 : racine avec Y … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| K-C11 | MB:259 | K-C11. **Mesure (pas une preuve).** Sur 016, 015, 014 et 011, toute paire cherchée a une racine témoin avec Y = 5 ou 4 ; un lemme « min L* >= 11/7 » s… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |

### A.3 L02, partie B (T16, T18, pont) — 20 conditionnels

Répartition : caduque 20.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| C1 | MB:301 | C1 ¦ (G) srg(99,14,1,2) avec involution à un point fixe ; (U) U entier défini positif de rang 24, y1, y2 de norme 7 orthogonaux ; (F) 49 vecteurs de U… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C2 | MB:302 | C2 ¦ U a une racine r avec (r,y1)^2 + (r,y2)^2 = 5 (et H4, T18, modèle amont) ¦ la paire n'héberge le cadre d'aucun srg(99,14,1,2) à involution à un p… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C3 | MB:303 | C3 ¦ racine avec Y = 4, ou vecteur de norme 4 avec ¦(v,y1)¦ = ¦(v,y2)¦ = 3 ¦ idem, conditionnellement à T20 ¦ P (moitié pont) ¦ `BRIDGE.md:19-21`, `20… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C4 | MB:304 | C4 ¦ x de norme 3 dans U avec Y(x) = 13 ¦ « paire impossible pour EX » (par T16) ¦ P ¦ `C2_WAGNER_BORNE_9_SUR_7.txt:26-28` ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C5 | MB:305 | C5 ¦ U a une racine r avec (r,y1) = ±2 (et T18, T20, (R-vi)) ¦ aucun cadre de U n'a ce y1, quel que soit y2 ¦ P ¦ `BRIDGE.md:211-222` ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C6 | MB:306 | C6 ¦ T16, T18, T20 ¦ E(v) >= 11 hors Z y1 + Z y2 ; une paire sans témoin a un minimum dual >= 11/7 ¦ P ¦ `lemma/PROOF_C2/A2_BRIDGE.md:32`, `52-55` ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C7 | MB:307 | C7 ¦ (avant Wagner) rang certifié >= 16 des projections des x avec Y(x) = 13 ¦ la paire est exclue ¦ X (caduc) ¦ `LEMME_EGALITE_8_SUR_7_C2.txt:186-194… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C8 | MB:308 | C8 ¦ min L* >= 10/7 (resp. >= 11/7) ¦ retire 64 à 92 % (resp. 99 à 100 %) du temps de recherche des réseaux mesurés ¦ H ¦ `LEMMA_TARGET_2026-10-06.md:… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C9 | MB:309 | C9 ¦ un lemme T22 ¦ déplacerait la frontière d'un pas ¦ O ¦ `A3_LEMMAS.md:73-74` ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C10 | MB:310 | C10 ¦ conclure « EX faux » par la route témoin entière ¦ exige les coupes 1, 2, 3 et les entrées externes de cette route ¦ O ¦ `C2_WAGNER_BORNE_9_SUR_… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C11 | MB:311 | C11 ¦ H16 (pas de fonction de norme carrée <= 16) ¦ Q(k,n) = 9k^2 + 14k(n·1_T) + 7 n^T G n hors de {1..8} ; ¦somme_{i dans I}(f_O,f_i)¦ <= 1 pour I in… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C12 | MB:312 | C12 ¦ (après round 1) ¦ T18 équivaut à exclure les trois configurations B0, B1, B2 (S+, S- indépendants, S hors N[p]) ¦ P ¦ `T18_REPORT.md:105-110` ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C13 | MB:313 | C13 ¦ un ensemble déterminé a un Gram impair de rang exactement 22 ¦ toute orbite ajoutée O vérifie b_O^T G^+ b_O = 3 exactement (4 pour une paire de … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C14 | MB:314 | C14 ¦ Y sigma-invariant avec au moins 23 orbites ¦ tout mineur principal 23 x 23 de G_odd est nul ; G_even de rang <= 22 ¦ P ¦ `T18_PROOF.md:802-826` … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C15 | MB:315 | C15 ¦ Y quelconque ¦ rang M1[Y] <= 44, rang M2[Y] <= 54 (un rang exact plus grand exclut ; cas des 4 survivants : 46 > 44) ¦ P ¦ `T18_PROOF.md:664-668… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C16 | MB:316 | C16 ¦ le cadre n'engendrerait pas {y1,y2}^perp ¦ on aurait seulement somme a_i^2 <= E(v) et E(v) = 9 n'exclurait rien ¦ P (remarque) ¦ `BRIDGE.md:300-… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C17 | MB:317 | C17 ¦ exclusion d'un réseau en mode report ¦ demande (a) T18 et T20 prouvés et vérifiés indépendamment, ou (b) les paires reportées cherchées ¦ procéd… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C18 | MB:318 | C18 ¦ la route X_0 d'abord terminée pour B0 ¦ exclurait environ 95 % des représentants sans W ¦ H ¦ `lemma/t18_B0/REPORT.md:157-159` ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C19 | MB:319 | C19 ¦ fermer un réseau entier sans recherche des h ¦ il manque un argument couvrant toutes ses paires de normales ... ou que le support extérieur de t… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C20 | MB:320 | C20 ¦ P3 (rang-nullité) ¦ étape C (23 orbites + p) : partie impaire singulière, nullité paire >= 2 ; 27 orbites + p : nullité impaire >= 5, paire >= 6… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |

### A.4 L02, partie C (T20) — 15 conditionnels

Répartition : caduque 14 ; prouvée 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| l.410 | MB:410 | les Calculs 4.12, 7.4, 7.5, 8.8, 8.9, 9.19, 9.20 sont justes ¦ toute configuration est en cas I, n_3 = 2, profil (3,4,0) ou (4,2,1) (Théorème 10.1) ¦ … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.411 | MB:411 | de plus le Calcul 9.29 est juste ¦ T20 (Théorème 10.2) ¦ E ¦ `T20_PROOF.md:2579-2583` ; `REFEREE_T20_PROOF.md:235-242` ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.412 | MB:412 | une recherche à rejets exacts n'a pas de nœud de niveau n (règle d'unité quelconque) ¦ aucune configuration n'a cette racine ¦ P ¦ `T20_PROOF.md:1058-… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.413 | MB:413 | un second programme satisfait les conditions 1-4 du contrat ¦ sa conclusion est une recherche complète, indépendante des listes du premier ¦ P ¦ `T20_… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.414 | MB:414 | sur un ensemble sigma-invariant déterminé, rang G_odd > 22 ou rang G_even > 22 ¦ contradiction ¦ P ¦ `T20_PROOF.md:999-1001` ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.415 | MB:415 | (E14) : toute fonction propre -4 entière sigma-impaire non nulle a norme >= 16 ¦ un couple (k,g) avec 1 <= N(k,g) <= 9 est une contradiction ¦ O dans … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.416 | MB:416 | les normes duales 5 et 6 sont exclues (min L* >= 8/7) ¦ arêtes croisées forcées ; au plus trois mots avec s_I = 2 ; cas d'égalité ¦ dépend de (E14) ¦ … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.417 | MB:417 | (E14) ¦ B sans ensemble indépendant de taille 4 (D1) ; w ~ sigma w' forcé (D2) ; type (D3) impossible ¦ dépend de (E14) ¦ `master:lemma/t20_HAND/NOTES… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.418 | MB:418 | U n V vide et e(U) = 0 pour le type de z ¦ violation PSD explicite (vecteur 7[i dans U] - 2, 7 sur z) ¦ P ¦ `NOTES.md:107-110` ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.419 | MB:419 | n_3 = 0 et e(X_0) = 9 ¦ contradiction (X_2 biparti contre une arête de paire interne) ¦ P ¦ `T20_PROOF.md:1883-1934` ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.420 | MB:420 | profil (4,2,1) ¦ u, u' sans voisin dans R_0 ; (n_3 = 2) beta = 1 ¦ P ¦ `T20_PROOF.md:1819-1821`, `:2320-2336` ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.421 | MB:421 | pour toute base gardée la recherche de la route B / route A ne trouve rien ¦ n_3 = 2 impossible ¦ P ¦ `SPEC_ROUTE_B_N3.txt:141-150` ; `SPEC_N3.md:108-… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.422 | MB:422 | T20 (et T18) ¦ les 2,508,295 paires différées sur T20 (5,190,752 sur T18) sont exclues ; avec le pont, les 156 enveloppes ¦ P (pont non lu ici) ¦ `T20… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.423 | MB:423 | T18 et T20 ¦ toute racine a ¦(r,y1)¦ <= 1, ¦(r,y2)¦ <= 1 (Corollaire Y1) ; 003:181:182 couvert ¦ P ¦ `T20_BOARD.md:55` ; `FINAL_STATEMENT_DRAFT.md… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| l.424 | MB:424 | T18, T20, pont, certificats, et les conditions de la section 6 ¦ « No strongly regular graph with parameters (99, 14, 1, 2) has an automorphism of ord… | prouvée | R1-24 | conclusion « pas d'involution » : statut mixte, sans relecteur humain |

### A.5 L02, partie D (réduction, article) — 17 conditionnels

Répartition : caduque 15 ; prouvée 1 ; fait 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| 1 | MB:506 | 1. Si σ est un automorphisme d'ordre 2 de Γ, alors σ fixe exactement un sommet (A.0 ; P, Codex) ; AUDIT_REDUCTION.md:56-88. | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 2 | MB:507 | 2. Si (Γ, σ) existe, alors il existe U, l'un des 156, avec un repère vérifiant (R1)–(R8) (Théorème R ; P, Codex) ; | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 3 | MB:509 | 3. Si aucun des 156 ne contient de repère (Théorème B ; S, avec composante O), alors aucun automorphisme d'ordre 2 n'existe | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 4 | MB:511 | 4. Si le Thm 1.1 est vrai et T4 aussi (P, revu à la main selon la transcription), alors EX est faux dans le modèle | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 5 | MB:514 | 5. Si U contient un repère, alors U est indécomposable (A.9 ; P). Si U est décomposable, il ne contient pas de repère (152, 153). | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 6 | MB:515 | 6. Si U contient un repère et que T16, T18, T20 sont vrais, alors E(v) ≥ 11 pour tout v hors de Π (Cor. 7.2 ; P cond.) ; | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 7 | MB:517 | 7. Si U a une racine r avec (r,y) = ±2, alors y n'est normale d'aucun repère, quelle que soit l'autre (Cor. Y1 ; P, conditionnel | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 8 | MB:519 | 8. Si une paire (y1,y2) admet un vecteur d'énergie ≤ 7 (hors Π), ou un témoin W8 (T16), W9 (T18) ou W10 (T20), alors la paire | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 9 | MB:521 | 9. Si un vecteur caractéristique z de norme 16 a Y = (z,y1)^2 + (z,y2)^2 > 66, alors la paire est exclue (Lemme 6.7 ; P) ; | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 10 | MB:523 | 10. Si la somme des 42 plus petits m_j dépasse ¦R_j¦, alors U est exclu ; si les vecteurs duaux courts (< 8/7) d'un réseau | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 11 | MB:526 | 11. Si pour un sous-espace V les types de vecteurs de norme 3 forcent Σ_o ¦P_V uo¦^2 > 7 dim V, ou plus généralement si une | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 12 | MB:529 | 12. Si U' (jumeau par R = [[2,2],[−2,2]]) a strictement plus de racines que U, alors la paire est réglée par induction descendante | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 13 | MB:533 | 13. Si l'on recertifie les au plus 2 479 669 paires des formes (a) et (c) sans statut ni flottant, alors la dernière réserve de | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 14 | MB:535 | 14. Si les comptes de vecteurs distincts exactement acceptés satisfont E4 + 24E2 + 24E3 = 196560, alors les trois listes sont | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 15 | MB:537 | 15. Si les nombres de Coxeter des deux voisins pairs diffèrent (H1 ≠ H2), alors aucun h de norme 4 n'a une empreinte nulle sur | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| 16 | MB:539 | 16. Si (A) à (E) sont vrais, alors G est trivial (P, Codex : « valid conditional ») ; asymmetric.tex:47-55. Sans ordinateur | prouvée | R1-24 | (A)-(E) établis avec statuts mixtes ; sans ordinateur ¦G¦ ∈ {1,2,11} |
| 17 | MB:541 | 17. Si 7 divise ¦G¦, alors G ≅ Z7 ; si ¦G¦ est pair, il divise 6 (CW25, publié) ; main.tex:96-97. Si ¦G¦ est pair, il divise 42 | fait |  | résultats publiés |

### A.6 L02, partie A (matériau C1) — 41 conditionnels

Répartition : fait 21 ; ouverte 12 ; caduque 6 ; réfutée 1 ; chaîne 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| 1 | MB:677 | 1 ¦ le lemme des graines (≤ 13 configurations) et a₈ ≥ 96 526 tiennent ¦ r = 33 impossible sauf vecteur de Fano ¦ P non relu ; dépassé (r = 33 exclu a… | caduque |  | r = 33 exclu |
| 2 | MB:678 | 2 ¦ UNE de : 2a₈ + 16a₉ + a₁₃ < 2632 ; b₂ < 914 ; b₃ < 6 696 790 ¦ rang 43 exclu ¦ E (formules reproduites par Codex) ; X ouvert ¦ H:1351-1352 (L02_C2… | ouverte | R1-28 | bornes supérieures au rang 43 : aucune |
| 3 | MB:679 | 3 ¦ il n'y a aucune 22-coclique ¦ a₇ = 0 à tout rang (~2 M de moins au plafond du rang 37) ¦ P non relu ; X ouvert « high value » ¦ H:1383-1384 (L02_C… | ouverte | R1-17 | au rang 37, N14 (E) donne déjà a₇ = 0 |
| 4 | MB:680 | 4 ¦ une exclusion du rang 43 n'utilise que le genre, les vecteurs de M et les vecteurs courts de L1 ¦ elle exclut aussi 37, 39, 41 ¦ P non relu ¦ H:14… | ouverte |  | transfert 43 → 37..41 : outils à vérifier par Λ# |
| 5 | MB:681 | 5 ¦ les collisions (paires jumelles de supports spéciaux d'ordres 8 et 9) sont maîtrisées ¦ rang 37 meurt d'un facteur 2,3 à 3,9 ¦ E (labo) ; X : comp… | caduque |  | route des collisions close comme méthode |
| 6 | MB:682 | 6 ¦ τ_grid tombe à ~1000 (droites dans ≤ 3 grilles) ¦ budget de collisions suffisant ¦ E (labo) ¦ H:1449-1451 (L02_C2_aws-311) ¦ | caduque |  | route des collisions close comme méthode |
| 7 | MB:683 | 7 ¦ τ ≤ ~860 (aucune droite dans 4 grilles) ¦ route collisions paire par paire conclut ¦ E ; route close comme méthode ¦ H:1471 (L02_C2_aws-314) ¦ | caduque |  | route des collisions close comme méthode |
| 8 | MB:684 | 8 ¦ aucune droite dans 4 ou 6 grilles ¦ τ_grid ≤ 693 ¦ E (labo) ; X global, ouvert ¦ H:1594-1595 ¦ | ouverte |  | « aucune droite dans 4 ou 6 grilles » non prouvé |
| 9 | MB:685 | 9 ¦ le nombre TOTAL de paires jumelles < ~540 (~700 si toutes sont des paires de grilles) ¦ rang 37 exclu (avec les plafonds de Codex) ¦ E (labo) ; X … | ouverte |  | E, PL flottant ; route close comme méthode |
| 10 | MB:686 | 10 ¦ 27 828τ_g + 31 976τ_n + (canaux non comptés) < 17,1 M, c.-à-d. τ_g < 614 sans paire non grille, ou ρ ≤ ~58 ¦ rang 37 exclu ¦ E (PL flottant du la… | ouverte |  | E, PL flottant ; route close comme méthode |
| 11 | MB:687 | 11 ¦ les seules relations mod 7 entre [1_G], [1] sont celles des pinceaux (+ « une droite non hub par un point à h hubs est dans ≥ h grilles », h ≤ 4 … | réfutée |  | relations en un sommet (L06 COND-09) |
| 12 | MB:688 | 12 ¦ c relations au-delà des pinceaux (ρ ≤ 18 + c + x₆) ¦ c = 0 : τ_g ≤ 388 ; c = 10 : 608 (16,92 M < 17,1 M) ; c = 12 : 655 (insuffisant) ¦ E (labo 1… | caduque |  | route des collisions close comme méthode |
| 13 | MB:689 | 13 ¦ à P = 0, les masses de collision 7 à 9 sont bornées ¦ rang 37 exclu (marge ~16,7 M contre canaux 1e5-1e6) ¦ E (labo) ; X ouvert (demandé à Codex)… | ouverte |  | E, PL flottant ; route close comme méthode |
| 14 | MB:690 | 14 ¦ P plafonné (niveau masse 6 seul) ¦ rang 37 ⇒ P > ~285 ¦ E (labo, relais) ¦ H:1994 (L02_C2_aws-380) ¦ | ouverte | R1-27 | E flottant ; version rigoureuse « rang 37 ⇒ P > 0 » non obtenue (L05-063) |
| 15 | MB:691 | 15 ¦ G(T) connexe, 7 ∤ τ, et D ≠ 0 entre deux complétions de même (boule, ombres) ¦ r + r′ ≥ 78 ; en particulier aucune seconde complétion de rang 37 … | fait |  | énoncé établi (statut de la source) |
| 16 | MB:692 | 16 ¦ D² ≡ 0 mod 7 et profils des sommets modifiés distincts (automatique si chaque sommet modifié a ≥ 3 voisins non modifiés) ¦ D = 0 ; au rang 37 gén… | fait |  | énoncé établi (statut de la source) |
| 17 | MB:693 | 17 ¦ les ordres d'automorphisme 2, 3, 7, 11 sont exclus (programme C2/C3 etc.) ¦ au rang 37 générique (boule, ombres) est sans symétrie (corollaire 8)… | chaîne | R1-16 | X = ordres 2, 3, 7, 11 exclus (statuts mixtes) |
| 18 | MB:694 | 18 ¦ (boule, 60 ombres) au rang 37 générique doit avoir une symétrie, ou ne pas exister ¦ les droites génériques au rang 37 sont exclues ¦ ni l'un ni … | ouverte | R1-16 | ni l'un ni l'autre démontré |
| 19 | MB:695 | 19 ¦ aucune différence D de rang ≤ 4 (Codex 233) et bloc proche inversible ¦ (39,39) fermé ; au rang 39 générique toute symétrie de (boule, ombres) se… | fait |  | E annoncé, non relu |
| 20 | MB:696 | 20 ¦ les espaces colonnes de Y et Y′ sont orthogonaux ¦ l'argument du laplacien s'applique encore aux paires r + r′ ≥ 80 ¦ P (remarque) ¦ M:135-136 (L… | fait |  | énoncé établi (statut de la source) |
| 21 | MB:697 | 21 ¦ une borne uniforme 2288 sur les configurations (1⁷ ; (−1)²⁹) à support positif indépendant ¦ S₀ entièrement exclu (Codex : S₀ exige ≥ 2289 + 15g)… | ouverte | R1-25 | borne 2288 |
| 22 | MB:698 | 22 ¦ toutes les couches fractionnaires de S₀ divisibles par 3, ou toutes celles des classes 1, 2, 4 ¦ S₀ incompatible ¦ E (hypothèse purement arithmét… | ouverte | R1-25 |  |
| 23 | MB:699 | 23 ¦ au rang 43, κ = g_v = u = c₁ = s₄₄ = 0 dans S₀ ¦ contradiction (congruence mod 3) ¦ E ¦ M:783-787 (L02_C2_aws-432) ¦ | fait |  | énoncé établi (statut de la source) |
| 24 | MB:700 | 24 ¦ au rang 43, aucun objet bas des six types (g_v, u, g_ℓ, c₁, w, s₄₄) ¦ ni norme 14 ni norme 16, au plus une paire ±y de norme 18 ou 20, et « P3/N2… | fait |  | énoncé établi (statut de la source) |
| 25 | MB:701 | 25 ¦ au rang 43, seules les normes 18 et 26 sont présentes ¦ chaque classe de norme 26 a 329 + 7b₁ − 8(x₁ + x₂) vecteurs ; x₁ + x₂ ≤ (329 + 7b₁)/8 ; s… | fait |  | énoncé établi (statut de la source) |
| 26 | MB:702 | 26 ¦ au rang 43, une seule des normes 16..24 est présente ¦ ses quatre classes ont des effectifs (u, v, v, u) ¦ E ¦ M:443-444 (L02_C2_aws-411) ¦ | fait |  | énoncé établi (statut de la source) |
| 27 | MB:703 | 27 ¦ au rang 43, aucun vecteur de norme 16 à 24 ¦ somme vectorielle nulle dans chaque classe non nulle, pour chaque norme ; et (Codex) pas de racine, … | fait |  | énoncé établi (statut de la source) |
| 28 | MB:704 | 28 ¦ S₀ sans sommet fantôme ¦ ≥ 2289 vecteurs de classe 2, norme 40/9, à support positif indépendant, dont ≥ 2001 de profil (1⁷ ; (−1)²⁹) ¦ E ¦ M:559-… | fait |  | énoncé établi (statut de la source) |
| 29 | MB:705 | 29 ¦ une famille de grilles re-réglées comme au 243, chaque sommet touché dans g grilles par une même droite ¦ g ≥ 3 ; donc pas de tel mouvement sous … | fait |  | énoncé établi (statut de la source) |
| 30 | MB:706 | 30 ¦ rang 37 et G(T) sans triangle ni 4-cycle ¦ G(T) connexe ¦ E (assisté par ordinateur, audit partiel) ¦ G:8-18 (L02_C2_aws-364) ¦ | fait |  | énoncé établi (statut de la source) |
| 31 | MB:707 | 31 ¦ rang 37, P = S = 0 (avec notes 125, 126) ¦ toute droite est connexe ; « (6,6) partout » n'arrive pas ¦ E + notes de septembre non re-démontrées ¦… | fait |  | énoncé établi (statut de la source) |
| 32 | MB:708 | 32 ¦ rang 37 et aucune arête de T dans un prisme ¦ G(T) connexe (énoncé B) ¦ O (incomplet) ¦ G:133-136 (L02_C2_aws-377) ¦ | ouverte |  | énoncé B incomplet |
| 33 | MB:709 | 33 ¦ six paires parmi l₁..l₄ et trois paires parmi l₅..l₇ engendrent des grilles en p₀ ¦ aucun vecteur de norme 16 positif en p₀ (lemme N16) ¦ P relu … | fait |  | énoncé établi (statut de la source) |
| 34 | MB:710 | 34 ¦ deux vecteurs de norme 18 sur une graine, racine (2,1,1), même c manquant, rien d'autre partagé que ω ¦ au plus UN second vecteur ¦ P non relu ; … | fait |  | énoncé établi (statut de la source) |
| 35 | MB:711 | 35 ¦ l'échelon d'un prisme engendre des grilles avec tous les autres aux trois points d'une droite dans six grilles, et un point a un second tel échel… | fait |  | énoncé établi (statut de la source) |
| 36 | MB:712 | 36 ¦ motifs (2,2,1) ou (2,2,2) de droites-hubs aux trois points d'une droite dans six grilles ¦ impossibles au rang ≥ 37 (Gram de rang 23 ou 24) ¦ E (… | fait |  | énoncé établi (statut de la source) |
| 37 | MB:713 | 37 ¦ colonnes canoniques : toute colonne dans 4 grilles en deux des trois points, ou dans 3 grilles aux trois points ¦ rang 24 / 21 à 24 : impossible … | fait |  | énoncé établi (statut de la source) |
| 38 | MB:714 | 38 ¦ un point a trois droites dans six grilles aux trois points d'une droite dans six grilles ¦ impossible au rang 37 ((33, 24 à 27)) ¦ E (labo) ¦ H:1… | fait |  | énoncé établi (statut de la source) |
| 39 | MB:715 | 39 ¦ r ≤ 31 ¦ une droite dans six grilles est exclue (Hermite) ¦ E (inutile, r ≥ 37) ¦ H:1600-1601 (L02_C2_aws-328) ¦ | caduque |  | r ≤ 31 exclu |
| 40 | MB:716 | 40 ¦ au rang 39, droite générique ¦ résidu de rang 2 anisotrope ssi τ(G(T)) résidu quadratique mod 7 ¦ P non audité ¦ H:1923-1924 (L02_C2_aws-363) ¦ | fait |  | énoncé établi (statut de la source) |
| 41 | MB:717 | 41 ¦ au rang 37, droite générique ¦ tout vecteur entier lointain à sommes d'ombres nulles de norme < 26 est un vecteur propre global (pas deux k-ensem… | fait |  | énoncé établi (statut de la source) |

### A.7 L03a (session eeaf2d22 et dépôt externe) — 54 conditionnels

Répartition : fait 20 ; caduque 16 ; réfutée 12 ; ouverte 5 ; critère 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| C-01 | MB:828 | C-01 ¦ Γ a une involution t ¦ Fix(t)={x} ; t = σ (flip de chaque bloc) ; u ≁ σu ; a1(t)=14 ; D couplage parfait sur 42 orbites ¦ P / X ouvert ¦ NI L17… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C-02 | MB:829 | C-02 ¦ Γ a une involution ¦ rang_F2(Γ̄ + NbNbᵀ) = 20 et Γ̄²+Γ̄ = NbNbᵀ sur F2 ¦ P (IA ×2) / X ouvert ¦ NI L36-L45 ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C-03 | MB:830 | C-03 ¦ Γ a une involution ¦ S²+S=12I, spec 3^27,(−4)^22 ; S_out spec 0^7∪3^20∪(−4)^15 ; (S_out+4I−CCᵀ/3)/7 projecteur de rang 20 ¦ P ¦ NI L31-L34 ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C-04 | MB:831 | C-04 ¦ Γ a une involution ¦ mod 7 : S_out−3I nilpotent d'indice 2 sur dim 35 ; rang_F7(S−3I) ≤ 22 (aucune contradiction trouvée avec rang_F7(M) ≥ 27) … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C-05 | MB:832 | C-05 ¦ le modèle orbitaire (R)(D)(I)(P) est UNSAT (certifié) ¦ aucune involution ⇒ ¦Aut¦ ∈ {1,3} ¦ P / X ouvert ¦ NI L58-L64 ¦ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| C-06 | MB:833 | C-06 ¦ g d'ordre 3 sans point fixe et les 6 orbites triangulaires forment exactement C6 sans corde ¦ holonomie ε0+…+ε5 = 0 dans F3 (h=1,2 impossibles)… | caduque |  | C3 clos (Lean) |
| C-07 | MB:834 | C-07 ¦ g d'ordre 3 sans point fixe avec 6 orbites triangulaires de motif F ¦ K^T(E−FE−EF)K = 0 sur F3 (non trivial seulement pour F=C6) ¦ C / moot ¦ S… | caduque |  | C3 clos (Lean) |
| C-08 | MB:835 | C-08 ¦ p premier divise ¦Aut¦ ¦ p ∈ {2,3} (Behbahani–Lam) ; Fix(g) selon Makhnev–Minakova Thm 1 ¦ E (calcul publié) ¦ LIT `behbahani_thesis.txt` L22… | fait |  | littérature publiée |
| C-09 | MB:836 | C-09 ¦ 2 ¦ ¦Aut¦ ¦ ¦Aut¦ ¦ 6 (Cesarz–Woldar) ; et involution ⇒ ¦G¦ ¦ 42 ou ¦G¦ ¦ 6 (Makhnev–Minakova Cor. 1) ¦ P (publié) ¦ LIT `cesarz_wo… | fait |  | littérature publiée |
| C-10 | MB:837 | C-10 ¦ 7 ¦ ¦Aut¦ ¦ G ≅ Z7 (Cesarz–Woldar) ; et 0 matrice d'orbites pour p=7 (Behbahani) ¦ P / E ¦ LIT `cesarz_woldar.txt` L69 ; `behbahani_thesis.t… | fait |  | littérature publiée |
| C-11 | MB:838 | C-11 ¦ ext : un automorphisme d'ordre 11 existe ¦ il est sans point fixe, puis contradiction par la recherche de quotients 9×9 (0 quotient) ¦ C ¦ AR L… | fait |  | calcul externe (C) |
| C-12 | MB:839 | C-12 ¦ ext : Γ sommet-transitif, ou de Cayley sur un groupe d'ordre 99 ¦ contradiction ¦ C ¦ RD L187-L194 ; AR L427-L429 ¦ | fait |  | calcul externe (C) |
| C-13 | MB:840 | C-13 ¦ ext : n3 = 705 ¦ contradiction (donc n3 ≥ 708) ¦ P (VER) ¦ RD L1290-L1335 ¦ | fait | R1-04 | ⟺ P ≤ 1150 (redécouvert par l'équipe le 14/10) |
| C-14 | MB:841 | C-14 ¦ ext : n3 = 705 ¦ h ∈ {1,9} ; q(T) ≤ 8 ; tr(A4²) ≥ 26460 ; et h ≥ 21 ⇒ n3 ≠ 705 ¦ P (historique) ¦ RD L1244-L1263 ; AG `2026-07-23-wave21-lattic… | réfutée | R1-03 | cas vide : n3 = 4158 − 3P ≥ 1602 par P ≤ 852 (C) |
| C-15 | MB:842 | C-15 ¦ ext : n3 = 708 ¦ det(B) ≤ 6525 ; h ∈ {9,21,49,81,189,441,729,1029} ; tr(C²) ≥ 10 ; tr(B²) ≥ 116 ; q(T) ≤ 11, au plus un q(T) = 11 ¦ P (VER) ¦ R… | réfutée | R1-03 | cas vide : n3 = 4158 − 3P ≥ 1602 par P ≤ 852 (C) |
| C-16 | MB:843 | C-16 ¦ ext : n3 = 708 et forme scaled-dual = somme orthogonale d'ADE irréductibles ¦ contradiction ¦ P (VER) ¦ RD L1549-L1555 ¦ | réfutée | R1-03 | cas vide : n3 = 4158 − 3P ≥ 1602 par P ≤ 852 (C) |
| C-17 | MB:844 | C-17 ¦ ext : n3 = 708 et sommande orthogonale A2, E6 ou A6 ¦ contradiction (21 > 18 ; énergies cubiques 24 et 66 > 60) ¦ P (VER) ¦ RD L1439-L1529 ¦ | réfutée | R1-03 | cas vide : n3 = 4158 − 3P ≥ 1602 par P ≤ 852 (C) |
| C-18 | MB:845 | C-18 ¦ ext : n3 = 708, forme sans racine, décomposition intégrale non triviale, incidence réelle ¦ contradiction (231 ¦ b avec 0 < b < 231) ¦ P (VER)… | réfutée | R1-03 | cas vide : n3 = 4158 − 3P ≥ 1602 par P ≤ 852 (C) |
| C-19 | MB:846 | C-19 ¦ ext : n3 = 708 et vecteur de norme 2 (branche avec racine) ¦ k ∈ {0,±1}^99, Ak = −4k, support complément de Fano ; extension ⇔ 6 équations de b… | réfutée | R1-03 | cas vide : n3 = 4158 − 3P ≥ 1602 par P ≤ 852 (C) |
| C-20 | MB:847 | C-20 ¦ ext : n3 = 708 sans racine ¦ endpoint indécomposable et tr(A−1 A−2²) = 0 (motif {−2,−2,−1} interdit) ¦ P (VER) ¦ RD L1957-L1974 ¦ | réfutée | R1-03 | cas vide : n3 = 4158 − 3P ≥ 1602 par P ≤ 852 (C) |
| C-21 | MB:848 | C-21 ¦ ext : la forme S0 = K12 ⊕ Λ(F) porte le paquet complet à 708 ¦ contradiction (det(B_K) ≤ 729 < 3645) ¦ P (VER) ¦ RD L1650-L1697 ¦ | réfutée | R1-03 | cas vide : n3 = 4158 − 3P ≥ 1602 par P ≤ 852 (C) |
| C-22 | MB:849 | C-22 ¦ ext : extrémité 4158 et 45 indices de triangles de degré de support signé interne ≤ 3 (somme des ¦S_ij¦) ¦ contradiction (exclusion de l'extr… | ouverte |  | extrémité P = 0 : non exclue par l'équipe (census P = 0 compatible) |
| C-23 | MB:850 | C-23 ¦ ext : extrémité 4158 ¦ rang_F7(M) ≥ 28 ; r3 ≥ 12 ; r7 ≥ 11 ; r3 + r7 pair ; à r3 = 12 la classe de déterminant non carrée est exclue ¦ P (VER) … | fait |  | énoncé externe établi (VER) |
| C-24 | MB:851 | C-24 ¦ ext : rang_F7(M) = 27 ¦ Γ contient un prisme triangulaire induit, donc n3 ≤ 4155 ¦ P (VER) ¦ RD L3018-L3021 ¦ | caduque | R1-02 | ligne de rang déjà exclue : r_ext = r − 1 ≥ 36 |
| C-25 | MB:852 | C-25 ¦ ext : extrémité 4158 et r7 ≤ 20 / ≤ 22 / ≤ 24 ¦ toutes les arêtes de type 2+2+2 / types 2+2+2 ou 2+4 / aucune arête de type 3+3 ¦ P (VER) ¦ RD … | caduque | R1-02 | ligne de rang déjà exclue : r_ext = r − 1 ≥ 36 |
| C-26 | MB:853 | C-26 ¦ ext : extrémité 4158 et r3 = 12 ¦ r7 pair ≥ 26 (W40), puis ≥ 28 (W42) ¦ P (VER) ¦ RD L2759-L2760, L2952-L2955 ¦ | caduque | R1-02 | ligne de rang déjà exclue : r_ext = r − 1 ≥ 36 |
| C-27 | MB:854 | C-27 ¦ ext : extrémité 4158, r3 = 12 et toutes arêtes de type 222 ¦ tout bloc de triangle de base de rang ≥ 33 ; r7 pair ≥ 34 ¦ P (VER) ¦ RD L2869-L28… | caduque | R1-02 | ligne de rang déjà exclue : r_ext = r − 1 ≥ 36 |
| C-28 | MB:855 | C-28 ¦ ext : extrémité 4158, r3 = 12, toutes 222, masque 51739 ¦ incidence extérieure = triple appariement exact (45 032 six-ensembles) ; graphe extér… | fait |  | énoncé externe établi (VER) |
| C-29 | MB:856 | C-29 ¦ ext : extrémité 4158 ¦ toute non-arête percole ; R = 18H, 6H ≤ P, R ≤ 3P, S ≥ n3 ¦ P (VER) ¦ RD L3388-L3398 ¦ | fait |  | énoncé externe établi (VER) |
| C-30 | MB:857 | C-30 ¦ ext : extrémité 4158 ¦ aucun mot dual de poids 3 : d(W⊥) ≥ 4 (pas trois colonnes colinéaires) ¦ P (VER) ¦ RD L476-L486 ¦ | fait |  | énoncé externe établi (VER) |
| C-31 | MB:858 | C-31 ¦ ext : il existe un plafond universel de 25 paires antipodales de supports de norme 14/16/18 par 4-cycle induit ¦ la ligne de rang r_ext = 28 es… | caduque | R1-02 | ligne de rang déjà exclue : r_ext = r − 1 ≥ 36 |
| C-32 | MB:859 | C-32 ¦ ext : plafond universel de 24 paires jusqu'à la norme 20 ¦ la ligne r_ext = 30 est exclue ¦ réduction VER / X ouvert ¦ AR L598-L599 ; RD L259-L… | caduque | R1-02 | ligne de rang déjà exclue : r_ext = r − 1 ≥ 36 |
| C-33 | MB:860 | C-33 ¦ ext : borne supérieure de Jacobi 51 975 (alors que le rang 28 force ≥ 52 812) ¦ la ligne r_ext = 28 est exclue ¦ réduction VER / X ouvert ¦ AR … | caduque | R1-02 | ligne de rang déjà exclue : r_ext = r − 1 ≥ 36 |
| C-34 | MB:861 | C-34 ¦ ext : N_Wagner ≥ 18710 ¦ l'extrémité 4158 est exclue (via N_Wagner ≤ 3N_cube + 9355 et N_cube ≤ 3118) ¦ P / X ouvert ¦ RD L411-L414 ¦ | ouverte |  | extrémité P = 0 : non exclue par l'équipe (census P = 0 compatible) |
| C-35 | MB:862 | C-35 ¦ ext : défaut global E ≤ 8, où E = 8(18711 − N_Wagner) ¦ l'extrémité 4158 est exclue (elle exigerait E ≥ 16) ¦ P / X ouvert ¦ RD L427-L429 ; AR … | ouverte |  | extrémité P = 0 : non exclue par l'équipe (census P = 0 compatible) |
| C-36 | MB:863 | C-36 ¦ ext : au plus 4 marques Wagner en échec par non-arête (« lemme des quatre échecs ») ¦ l'extrémité 4158 est exclue ¦ P / X UNPROVED ¦ AR L834-L8… | ouverte |  | « lemme des quatre échecs » UNPROVED ; cf. C-53 réfutée |
| C-37 | MB:864 | C-37 ¦ ext : égalité dans la borne non-arête de W180 (rang 11) ¦ les 2 079 quadrilatères canoniques sont des coniques ; rang_F3(R_square) ≤ 220 ; RᵀR … | fait |  | énoncé externe établi (VER) |
| C-38 | MB:865 | C-38 ¦ ext : Q = 2079 (rang 11) ¦ contradiction (9Q ≥ 8·4158) ¦ P (VER) ¦ RD L605-L614 ¦ | fait |  | énoncé externe établi (VER) |
| C-39 | MB:866 | C-39 ¦ ext : rang 11 et une paire inversée appariée ¦ relation tout-égale interdite sur le quadrilatère canonique ⇒ multiplicité combinée ≤ 5, ε ≥ 5b … | fait |  | énoncé externe établi (VER) |
| C-40 | MB:867 | C-40 ¦ ext : un graphe a un ensemble indépendant de taille 22 ¦ design simple 2-(22,4,2), NNᵀ = 12I + 2J, ND = −N + 2J, X² = 28X ¦ P (VER) ¦ ST L3517-… | fait |  | énoncé externe établi (VER) |
| C-41 | MB:868 | C-41 ¦ ext : sous-graphe induit à m sommets de degré minimum 6 ¦ m ≥ 27 (via 2e(X) ≤ 3m + m²/9) ¦ P (VER) ¦ RD L978-L986 ¦ | fait |  | énoncé externe établi (VER) |
| C-42 | MB:869 | C-42 ¦ ext : P = 3 (trois prismes) ¦ O ≥ 4 (défaut impair de parité enracinée) ¦ P (VER) ¦ AR L560 ¦ | fait |  | énoncé externe établi (VER) |
| C-43 | MB:870 | C-43 ¦ ext : rang r_ext = 28 (q = 16) ¦ vecteur propre −4 entier de norme 14, 16 ou 18 ; N14 + N16 + N18 ≡ 2 mod 14 et ≥ 5868 ; supports 7+7, 8+8, 9+9… | caduque | R1-02 | ligne de rang déjà exclue : r_ext = r − 1 ≥ 36 |
| C-44 | MB:871 | C-44 ¦ ext : rang 28 et extrémité 4158 ¦ 407·N16 + 43·N18 ≥ 2165002 ¦ P (VER) ¦ AR L505-L507 ¦ | caduque | R1-02 | ligne de rang déjà exclue : r_ext = r − 1 ≥ 36 |
| C-45 | MB:872 | C-45 ¦ ext : motif C4 □ K3 présent ¦ graphe extérieur à 87 sommets : 549 arêtes, 167 triangles, 1 356 4-cycles, connexe, nullité 4, facteur x² − 9x − … | fait |  | énoncé externe établi (VER) |
| C-46 | MB:873 | C-46 ¦ ext : n3 = 4158 et partition locale à un triangle ¦ composantes [12], [4,8], [6,6], [4,4,4] seules ; H connexe à 32 triangles, C4(H) = 171 + C4… | fait |  | énoncé externe établi (VER) |
| C-47 | MB:874 | C-47 ¦ ext : rang 11, étoiles adjacentes ¦ h_xy = 1 ⇔ type 4+2 ; 0 pour 6, 3+3, 2+2+2 ¦ P (VER) ¦ ST L4196-L4206 ¦ | fait |  | énoncé externe établi (VER) |
| C-48 | MB:875 | C-48 ¦ Ishihara 2022 : « Théorème 28 » ¦ non-existence annoncée, mais l'étape (88) est réfutée (degrés 1^20, 2^51, compte 122 au lieu de 142) ¦ R (éta… | réfutée |  | étape (88) d'Ishihara réfutée |
| C-49 | MB:876 | C-49 ¦ ext : on prouve rang_F7(M) ≥ 45, ou, avec W66, r_ext ≥ 43 ¦ contradiction avec le rang rationnel 44, ou avec W66 r ≤ 42 : pas de Conway-99 (en … | critère | R1-02 | équivaut à une exclusion directe (r ≥ 44 en notation équipe) |
| C-50 | MB:877 | C-50 ¦ ext : les 33 cas raffinés de l'extrémité sont tous UNSAT, avec preuves vérifiées ¦ n3 = 4158 exclu, donc n3 ≤ 4155 ¦ P (couverture VER) / X : 0… | ouverte |  | extrémité P = 0 : non exclue par l'équipe (census P = 0 compatible) |
| C-51 | MB:878 | C-51 ¦ ext : on prouve que le domaine d'extension du critère 14+70+15 est vide ¦ la branche avec racine de n3 = 708 est exclue ¦ P / X ouvert ¦ AT `wa… | réfutée | R1-03 | cas vide : n3 = 4158 − 3P ≥ 1602 par P ≤ 852 (C) |
| C-52 | MB:879 | C-52 ¦ ext : toute complétion simultanée (B,H) à l'extrémité force un triangle de base T avec rang_F3(P_T − I) ≥ 12 ¦ amélioration du rang ternaire. L… | réfutée |  | version à un triangle réfutée ; général ouvert |
| C-53 | MB:880 | C-53 ¦ ext : le graphe d'incompatibilité des marques Wagner a un nombre d'indépendance ≤ 4 ¦ un certificat de Hoffman ou de couverture par cliques pro… | réfutée |  | gadget à 5 échecs |
| C-54 | MB:881 | C-54 ¦ ext : face d'égalité uniforme des non-arêtes (W205) ¦ rang de span des 99 projecteurs 54 ≤ r ≤ 59, noyau ≥ 40, donc au moins 7 relations global… | fait |  | énoncé externe établi (VER) |

### A.8 L03b (dépôt externe) — 32 conditionnels

Répartition : fait 9 ; réfutée 9 ; caduque 7 ; ouverte 7.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| K1 | MB:1000 | K1 ¦ srg(99,14,1,2) existe (aucune symétrie) ¦ n3 >= 705 (positivité de Schur + parité) puis n3 != 705, donc n3 >= 708 et induced_C6 >= 209 994 ¦ P (r… | fait | R1-04 | ⟺ P ≤ 1150 ; dépassé par P ≤ 852 |
| K2 | MB:1001 | K2 ¦ n3 = 0 (aucun N3 induit) ¦ contradiction (Makhnev 1988, Théorème 2 sous la condition (*)) ¦ CITED ; texte de 1988 non rejoué (O) ¦ L03b-049 ; CR/… | fait |  | cité (Makhnev 1988) |
| K3 | MB:1002 | K3 ¦ n3 = 705 ¦ h dans {1,9} ; et h >= 21 => n3 != 705 (h = [L : 21 L*]) ¦ P ¦ L03b-075 ; CR/verification/wave21-lattice-extension/2026-07-23T184926Z-… | réfutée | R1-03 | branche n3 = 705/708 vide (n3 ≥ 1602) |
| K4 | MB:1003 | K4 ¦ n3 = 708 ¦ h dans {9,21,49,81,189,441,729,1029}, det(B) <= 6525, tr(C^2) >= 10, tr(B^2) >= 116, q(T) <= 11 ¦ P ¦ L03b-081, 082 ; CR/verification/… | réfutée | R1-03 | branche n3 = 705/708 vide (n3 ≥ 1602) |
| K5 | MB:1004 | K5 ¦ n3 = 708 et la forme duale mise à l'échelle a un facteur orthogonal A2 ¦ aucun cadre de projecteur à 231 lignes (et tr(A2 Q_AA) >= 18) ¦ P ¦ L03b… | réfutée | R1-03 | branche n3 = 705/708 vide (n3 ≥ 1602) |
| K6 | MB:1005 | K6 ¦ n3 = 708 et la forme est une somme orthogonale complète de réseaux de racines ADE irréductibles ¦ impossible ¦ C/P (conditionnel) ¦ L03b-091 ; CR… | réfutée | R1-03 | branche n3 = 705/708 vide (n3 ≥ 1602) |
| K7 | MB:1006 | K7 ¦ n3 = 708 et S = K12 + LAMBDA(F) ¦ impossible ¦ P ¦ L03b-098 ¦ | réfutée | R1-03 | branche n3 = 705/708 vide (n3 ≥ 1602) |
| K8 | MB:1007 | K8 ¦ incidence sommet-triangle réelle et décomposition orthogonale entière non triviale sans racine de la forme S d'endpoint ¦ contradiction (231 ¦ b… | réfutée | R1-03 | branche n3 = 705/708 vide (n3 ≥ 1602) |
| K9 | MB:1008 | K9 ¦ n3 = 708 avec une racine de norme 2 ¦ support Fano-complément 7+7, image (+1)^21 0^189 (-1)^21, partition 14+70+15 et design 2-(15,3,2) (critère … | réfutée | R1-03 | branche n3 = 705/708 vide (n3 ≥ 1602) |
| K10 | MB:1009 | K10 ¦ n3 = 708 sans racine, indécomposable ¦ tr(A_-1 A_-2^2) = 0 ; si l'on prouvait tr > 0, la branche serait exclue ¦ P / LEMME ¦ L03b-107 ; CR/verif… | réfutée | R1-03 | branche n3 = 705/708 vide (n3 ≥ 1602) |
| K11 | MB:1010 | K11 ¦ g automorphisme d'ordre 11 ¦ g sans point fixe ; et le quotient semi-régulier 9x9 n'existe pas, donc aucun automorphisme d'ordre 11, pas de grap… | fait |  | énoncé établi |
| K12 | MB:1011 | K12 ¦ G est un graphe de Cayley (groupe d'ordre 99, tous abéliens) ¦ contradiction (somme de racines de l'unité = -18/7 ou 81/7) ¦ C ¦ L03b-169 ; CR/a… | fait |  | énoncé établi |
| K13 | MB:1012 | K13 ¦ n3 = 4158 (P = 0) ¦ q(T) = 12 pour tout T ; S^2 = 13S + 68I ; r3 >= 12 ; r3 + r7 pair ; d_i d_(232-i) = 441 ; r7 >= 22, puis >= 28 ¦ P ¦ L03b-12… | fait |  | structure à P = 0 ; bornes de rang dépassées par la fenêtre |
| K13b | MB:1013 | K13b ¦ rank_F7(M) = 27 ¦ un prisme triangulaire induit existe, donc n3 <= 4155 dans cette branche (branche ensuite vide : r pair >= 28 par la vague 66… | caduque | R1-02 | rang externe ≤ 34 : déjà exclu |
| K14 | MB:1014 | K14 ¦ rank_F7(M) <= 20 / <= 22 / <= 24 ¦ toute arête de type 2+2+2 / types 2+2+2 ou 2+4 seulement / pas de type 3+3 ¦ P ¦ L03b-130 ; CR/verification/w… | caduque | R1-02 | rang externe ≤ 34 : déjà exclu |
| K15 | MB:1015 | K15 ¦ n3 = 4158, r3 = 12 et toutes les arêtes de type 2+2+2 ¦ chaque bloc K39 de rang F7 >= 33 ; r7 pair >= 34 ¦ P ¦ L03b-133 ; CR/verification/wave41… | caduque | R1-02 | rang externe ≤ 34 : déjà exclu |
| K16 | MB:1016 | K16 ¦ r = rank_F7(2A-J+I) = 28 (q = 16) ¦ N14 + N16 + N18 = 2 mod 14 et N14 + N16 + N18 >= 5868 ; il existe un vecteur propre entier de -4 de norme 14… | caduque | R1-02 | rang externe ≤ 34 : déjà exclu |
| K17 | MB:1017 | K17 ¦ n3 = 4158 et r = 28 ¦ 407 N16 + 43 N18 >= 2 165 002 ; SI de plus chaque quadrilatère induit a au plus 25 extensions antipodales norme 16/18, ALO… | caduque | R1-02 | rang externe ≤ 34 : déjà exclu |
| K18 | MB:1018 | K18 ¦ n3 = 4158 et r = 30 et au plus 24 extensions antipodales jusqu'à la norme 20 par C4 ¦ exclusion du rang 30 (plafond non prouvé) ¦ O ¦ L03b-180 ;… | caduque | R1-02 | rang externe ≤ 34 : déjà exclu |
| K19 | MB:1019 | K19 ¦ n3 = 4158 et défaut noyau-frange global E <= 8 (E = 8(18711 - N_Wagner)) ¦ contradiction (l'endpoint exige E >= 16) ¦ O (borne non prouvée) ¦ L0… | ouverte |  | extrémités externes P = 0 / rang 11 |
| K20 | MB:1020 | K20 ¦ P = 0 implique au plus quatre marques échouées par non-arête ¦ borne inférieure de Wagner (non prouvée) ; vague 169 : les clauses locales actuel… | ouverte |  | extrémités externes P = 0 / rang 11 |
| K21 | MB:1021 | K21 ¦ endpoint de rang 11 ¦ Q >= 7059 ; toute borne supérieure compatible Q <= 7058 exclurait cet endpoint (aucune connue) ¦ P / O ¦ L03b-213 ; CR/ver… | ouverte |  | extrémités externes P = 0 / rang 11 |
| K22 | MB:1022 | K22 ¦ une inégalité de motif globale force au moins un prisme ¦ n3 <= 4155 ¦ O ¦ L03b-134 ; CR/verification/2026-07-27-wave41-orchestrator.md:L87-L88 … | ouverte |  | extrémités externes P = 0 / rang 11 |
| K23 | MB:1023 | K23 ¦ une coclique de taille 22 (Hoffman) existe ¦ 22 couplages de points, configuration 77_3, design 2-(22,4,2) ; compatibilité inconnue ¦ O ¦ L03b-0… | ouverte | R1-17 | α = 22 : compatibilité inconnue |
| K24 | MB:1024 | K24 ¦ une non-arête ne percole pas (2-bootstrap) ¦ sa clôture est un K3 x K3 = srg(9,4,1,2) induit unique ; à P = 0 toutes les non-arêtes percolent ¦ … | fait |  | énoncé établi |
| K25 | MB:1025 | K25 ¦ X sous-ensemble de sommets avec degré induit minimum >= 6 ¦ ¦X¦ >= 27 ¦ P ¦ L03b-054 ¦ | fait |  | énoncé établi |
| K26 | MB:1026 | K26 ¦ un sommet extérieur et un L(K3,3) = graphe de la tour induit ¦ le sommet le rencontre au plus une fois (saturation lambda/mu) ¦ P ¦ L03b-040 ; C… | fait |  | énoncé établi |
| K27 | MB:1027 | K27 ¦ automorphisme d'ordre 3 sans point fixe (C3) ¦ 6 ou 27 orbites triangulaires (Lean, conditionnel) ; f = 27 impossible ; type (6,3^7) à tau = 6 e… | caduque |  | C3 clos (Lean) |
| K28 | MB:1028 | K28 ¦ Lou-Murin : gamma = 12 en tout triangle ¦ structure srg(9,4,1,2) impossible ; un srg(9,4,1,2) privé d'une arête force le srg(9,4,1,2) complet ¦ … | fait |  | énoncé établi |
| K29 | MB:1029 | K29 ¦ Keramatipour : onze Paley(9) indépendants ¦ impossible (preuve omise) ; motif Paley(9) partout impossible ¦ P / O ¦ L03b-005 ¦ | ouverte |  | preuves absentes |
| K30 | MB:1030 | K30 ¦ Harrison (non vérifié) : une racine avec >= 14 fibres C4 ; plafond R230 'Paley-perfect' ¦ UNSAT annoncé, preuves absentes de l'arbre épinglé ¦ O… | ouverte |  | preuves absentes |
| K31 | MB:1031 | K31 ¦ fixer une branche/classe par multiensemble de cycles ; réduire par la symétrie de l'échafaudage ¦ réduction non sûre (rejetée) ¦ R ¦ L03b-025, 1… | réfutée |  | réduction non sûre |

### A.9 L04 (C3) — 16 conditionnels

Répartition : caduque 9 ; hors cible 3 ; chaîne 2 ; prouvée 2.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| CND-1 | MB:1124 | CND-1 ¦ g ∈ Aut(Γ) d'ordre 3 **sans point fixe** ¦ il existe (Q, M) : Q ∈ M₃₃(ℤ) symétrique, Q1 = 14·1, Q²+Q = 12I+6J ; M ∈ M₃₃(ℤ[ω]) hermitienne, M²+… | caduque |  | C3 clos (Lean) |
| CND-2 | MB:1125 | CND-2 ¦ un couple (Q, M) comme en CND-1 existe ¦ contradiction (2 ≡ 1 mod 3) ¦ P + Lean (`C3.no_pair`) ¦ `…:pdf/preuve_c3.tex:136-208` ¦ | caduque |  | C3 clos (Lean) |
| CND-3 | MB:1126 | CND-3 ¦ g d'ordre 3 avec exactement 3 points fixes ¦ les points fixes forment un triangle, et le triple (Q 32×32, **a** 32×3, M 32×32) vérifie Ã1 = 14… | caduque |  | C3 clos (Lean) |
| CND-4 | MB:1127 | CND-4 ¦ g ≠ 1 et g³ = 1 ¦ ¦Fix(g)¦ ≤ 3, donc ¦Fix(g)¦ ∈ {0, 3} ¦ P + Lean ¦ `…:pdf/preuve_c3.tex:263-286` ¦ | caduque |  | C3 clos (Lean) |
| CND-5 | MB:1128 | CND-5 ¦ G cyclique d'ordre 3 agissant librement, V sous-espace G-stable de projecteur orthogonal **3-entier** ¦ d₁ ≡ d_ω (mod 3), tous deux premiers à… | caduque |  | C3 clos (Lean) |
| CND-6 | MB:1129 | CND-6 ¦ points fixes avec β = rang_F₃(P[Fix] mod 3) = 0 (pour Conway : Fix est une clique) ¦ F est libre et CND-5 s'applique avec d₁ = det/3^r ¦ P (dé… | caduque |  | C3 clos (Lean) |
| CND-7 | MB:1130 | CND-7 ¦ srg(v,k,λ,μ) de valeurs propres k, θ, θ' ; 3 ∤ θ−θ' ; tous les premiers de θ−θ' ≡ 1 (mod 3) ; intégralités vérifiées au cas par cas ¦ pas d'ac… | hors cible |  | autres paramètres / pistes C3 |
| CND-8 | MB:1131 | CND-8 ¦ MM04 et CW25 sont exacts (et Mak10 cor. 2.4) ¦ ¦Aut(Γ)¦ ∈ {1, 2, 7, 11} ¦ P conditionnel ¦ `…:pdf/preuve_c3.tex:290-302` ¦ | chaîne | R1-24 | réductions de ¦Aut¦ (littérature) |
| CND-9 | MB:1132 | CND-9 ¦ CND-8 et, en plus, le calcul de BL11 ¦ ¦Aut(Γ)¦ ∈ {1, 2} ¦ P conditionnel ¦ `…:pdf/preuve_c3.tex:294-302` ¦ | chaîne | R1-24 | réductions de ¦Aut¦ (littérature) |
| CND-10 | MB:1133 | CND-10 ¦ tous les problèmes quotient (étage Q) d'une classe de phases sont UNSAT ¦ la classe est exclue (relaxation exacte) ¦ P ¦ `conway99-c3:main:ra… | caduque |  | C3 clos (Lean) |
| CND-11 | MB:1134 | CND-11 ¦ tout le calcul restant finit UNSAT (≈ 40 instances, classes 29/43/44/45, étage P) et les lemmes d'entrées, de type, de triplets et lex sont r… | caduque |  | C3 clos (Lean) |
| CND-12 | MB:1135 | CND-12 ¦ un problème quotient est SAT ¦ il faut l'étage P (M²+M = 12I sur C) ; `stage_p.py` est prêt et auto-testé ¦ E (outil) ¦ `…:NUIT_JOURNAL.md:12… | caduque |  | C3 clos (Lean) |
| CND-13 | MB:1136 | CND-13 ¦ Q seul (sans M) est impossible (D4) ¦ preuve sans le côté Eisenstein ¦ O (conjecture) ¦ `conway99-c3-experimental:main:IDEES.md:15` ¦ | hors cible |  | autres paramètres / pistes C3 |
| CND-14 | MB:1137 | CND-14 ¦ les exposants de d₁ et d_ζ sont contraints, par exemple par le 5-rang de A+8I (graphe de Moore, p = 13) ¦ exclusion de l'ordre 13 par la cong… | hors cible |  | autres paramètres / pistes C3 |
| CND-15 | MB:1138 | CND-15 ¦ hors lot : le « 14 » de DISC (C1) vient de la parité de v₇(det) d'un réseau propre ¦ les blocs à quatre étoiles de classe 14 sont exclus « gr… | prouvée | R1-01 | L4 + L17 : classe 14 exclue |
| CND-16 | MB:1139 | CND-16 ¦ hors lot : D3 (ordre 3), D7 (ordre 7), le manuscrit C2 et la littérature ¦ Aut(Γ) est trivial ¦ assemblé, en attente de relecture ¦ `strongly… | prouvée | R1-24 | assemblage en attente de relecture |

### A.10 L05 (Codex) — 48 conditionnels

Répartition : fait 29 ; ouverte 10 ; caduque 5 ; chaîne 2 ; critère 2.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| K01 | MB:1256 | **K01** Si aucun des 174 noyaux de 14 sommets (motif obligatoire de Makhnev : deux triangles reliés par exactement deux arêtes ; | ouverte | R1-14 | 174 noyaux : prolongement ouvert |
| K02 | MB:1259 | **K02** Si chaque triangle appartient à au moins q grilles, les 174 noyaux se réduisent à 115, 52, 11, 2 types pour | fait |  | C, conditionnel aux grilles |
| K03 | MB:1261 | **K03** Si N9-NG (ν(T44) ≤ 9 + min(c_l, c_m) pour tout chevauchement sans grille, équivalent à rang(F) ≥ 12) est vrai, alors | ouverte | R1-07 | N9-NG |
| K04 | MB:1264 | **K04** Si rang(D) = 9 et rang(Z) ≥ 3 (SYM6), alors rang(F) ≥ 12, d'où K03. Conway + c_min ≤ 4 + D9 imposerait | chaîne | R1-07 | SYM6 + D9 ouverts |
| K05 | MB:1267 | **K05** ODD-PURE (δ = 0) équivaut à l'absence de perte de rang dans rang(T44) = 32 − c(l) − δ + rang(Z). **P**, cible **O**. | ouverte | R1-07 | ODD-PURE |
| K06 | MB:1269 | **K06** Si NG7 (aucun bloc non grille avec min(t_l, t_m) ≤ 7 ne passe les conditions nécessaires de Conway) est vrai, alors | ouverte | R1-07 | NG7 |
| K07 | MB:1271 | **K07** NG5 (ν ≥ 14 ⇒ min c ≥ 5) implique NG7, via c ≤ g + floor((6 − g)/2) et g ≤ t/2. Implication **P**, NG5 **O**. | chaîne | R1-07 | NG5 ⇒ NG7 (P) |
| K08 | MB:1273 | **K08** Si H-MATCH (C1, C1', C2, T et U PSD, ν(T) ≥ 14 ⇒ couplages h-reliés) est vrai, un point de Hamming est forcé (implication | ouverte | R1-08 | H-MATCH |
| K09 | MB:1276 | **K09** Toute famille locale avec rang_F7(8T_S) ≥ 29 est exclue de tout prolongement (borne globale rang_F7(8T_far) ≤ 28, issue de | fait | R1-10 | C, borne ≤ 28 (L22) |
| K10 | MB:1279 | **K10** Les 79 configurations de la branche « min_L c(L) ≥ 4 » sont INFEASIBLE ⇒ tout Conway a une droite L avec c(L) ≤ 3. | fait | R1-14 | S, sans certificat portable |
| K11 | MB:1282 | **K11** Si K10 est certifié et si les gabarits c3 ouverts (435 au 19/10) et la branche c ≤ 2 sont exclus, alors pas de Conway. | ouverte | R1-14 | registre c3 et branche c ≤ 2 ouverts |
| K12 | MB:1284 | **K12** Au rang 43, une racine de M impose 10a8 + 2a9 + 5a10 + 2a11 + a12 ≥ 328 ; l'absence des normes 16..24 force donc | fait |  | P |
| K13 | MB:1286 | **K13** Dans S0 (r = 43, sans racines ni normes 16..24) : une borne ≤ 2288 sur les configurations | ouverte | R1-25 | borne 2288 |
| K14 | MB:1289 | **K14** Au rang 43 : normes 16, 20, 22, 24 absentes ⇒ chaque classe de norme 26 porte t = 329 + 14k − 8(x1 + x2) impair ≥ 1 ; | fait |  | P |
| K15 | MB:1293 | **K15** r = 35 ⇒ ≥ 16 grilles, ≥ 450 prismes, ≥ 33 paires jumelles (r = 35 ensuite exclu). **C.** `CA:179_…:L9-15`, | caduque |  | r = 35 exclu |
| K16 | MB:1295 | **K16** min L = 14 ⇒ r ≥ 33 ; r = 33 ⇒ a_7 ≥ 66. **P** (historique). `CA:165_…:L5-8`, `CA:170_…:L9-14` (L05-001, L05-007). | caduque |  | r = 33 exclu |
| K17 | MB:1296 | **K17** Pour r ≥ 37 : 3n₃ ≤ 2n₁ + n₂ (motif (2,2,1) exclu) ; pour r ≥ 39 : 6n₃ ≤ n₁ + 2n₂ (deux apices denses interdits). | fait |  | P/C |
| K18 | MB:1298 | **K18** Rang 37, droite connexe sans torsion : 60 ombres binaires déterminent les arêtes lointaines, en nombre 240 + 7q ; | fait |  | P |
| K19 | MB:1301 | **K19** Données proches et 60 ombres avec une complétion de rang 37 et bloc proche inversible mod 7 ⇒ aucune autre complétion | fait |  | P/C |
| K20 | MB:1304 | **K20** Rang 37 : mauvais signe résiduel en dimension résiduelle 0 ⇒ toutes les branches de cette dimension exclues. **P.** | fait |  | P |
| K21 | MB:1306 | **K21** Bord de 43 sommets avec 3I − B + J/9 > 0 ⇒ ≤ 8192 affectations de signes et ≤ 2 complétions étiquetées, isomorphes ; | fait | R1-16 | P (bord 43 positif) |
| K22 | MB:1309 | **K22** Sur un tel bord, ≥ 3 composantes de signes forcés ⇒ co-Heawood disjoint du bord (deux cocliques de 22) ; sans | fait |  | P |
| K23 | MB:1311 | **K23** Instance préservant deux flips individuels ⇒ nombre de complétions multiple de 4 ; avec K21 (≤ 2 complétions), | fait | R1-20 | P ; indépendant de C2 (théorème de majorité) |
| K24 | MB:1313 | **K24** rang(A' − A) = 2 entre deux srg(99,14,1,2) ⇒ A' = SASᵗ (transposition) : aucun nouveau graphe par modification de rang 2. | fait |  | P |
| K25 | MB:1315 | **K25** Coclique de 21 dont tout extérieur a ≤ 4 voisins en elle ⇒ elle s'étend en 22 ; exclure toutes les cocliques 21/22 | fait |  | P |
| K26 | MB:1317 | **K26** Deux cocliques de Hoffman se coupant en 15 ⇔ co-Heawood induit ; reste H ≥ 0, rang 16, H² = 147H sur 70 sommets. **P.** | fait |  | P |
| K27 | MB:1319 | **K27** Sur les 84 étiquettes d'une racine : Γ binaire avec T, U PSD et rang T ≤ 30 ⇔ srg(99,14,1,2). **P.** | critère |  | équivalence avec le but |
| K28 | MB:1321 | **K28** Sous E3 : graphe des grilles contenant C4 ⊔ C3 ⇒ il contient K4 ⊔ C3. **P.** `MC:AGENTS.md:L366-369` (L05-198). | fait |  | P |
| K29 | MB:1322 | **K29** Sous E3 : deux rectangles non grilles disjoints avec H_A = −H_B ⇒ deux arêtes internes chacun et union cubique à | fait |  | P |
| K30 | MB:1326 | **K30** Carré de défaut H05 = H46 = −H06 = −H45, Q12 et Q13 grilles, H23 = H56 ⇒ e23 ≥ 4, contre E3. **P.** | fait |  | P |
| K31 | MB:1328 | **K31** Ah = −4h, h à valeurs 0, ±1 (14 fois +1, 14 fois −1) ⇒ chaque signe induit ≤ 5 arêtes. **P.** | fait |  | P |
| K32 | MB:1330 | **K32** Rang 37, P = S = 0, plus deux hypothèses ouvertes ⇒ les 231 droites ont le profil (6,6). **P** (conditionnel). | ouverte | R1-15 | deux hypothèses ouvertes |
| K33 | MB:1332 | **K33** Rang 37 et G(T) sans triangle ni 4-cycle ⇒ G(T) connexe (LAP). **S.** `CA:224_…:L7-20`, | fait |  | S |
| K34 | MB:1334 | **K34** P = 0 ⇒ deux étoiles lointaines d'une arête entre couches partagent exactement un apex, c₄(uv) ≤ 2, 38 types à | fait |  | P/E |
| K35 | MB:1336 | **K35** Conjecture du repère de 231 vecteurs (Gram des triangles) ⇒ P ≥ 1. **O.** | ouverte |  | conjecture du repère de 231 vecteurs |
| K36 | MB:1338 | **K36** Exclure les trois branches de fonctions courtes (entière 18, entière 26, affine 37) exclurait Conway ; « affine 37 ⇒ | ouverte | R1-13 | exclure les normes 18 et 26 de L1 |
| K37 | MB:1341 | **K37** Involution : g⁻ = 16 ⇒ prisme ; P = 0 ⇒ g⁻ ∈ {18, 20} ; 278/441 types exclus à g⁻ = 18 (C2, historique). **C.** | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| K38 | MB:1343 | **K38** C2 : fonction propre −4 impaire de support 8 + 8 ⇒ B n'est ni le complément du Wagner ni celui du cube ⇒ min L* ≥ 9/7 ⇒ | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| K39 | MB:1346 | **K39** Aut d'un éventuel Conway ∈ {1, C2, C3} (exclusions publiées consultées) ; pas d'ordre 11. **P.** | fait |  | littérature |
| K40 | MB:1348 | **K40** Moins de complétions étiquetées d'un bord que ¦Aut(bord)¦ ⇒ pas de complétion asymétrique. **P** (critère). | critère | R1-16 | critère de symétrie forcée |
| K41 | MB:1350 | **K41** Automorphisme fixant x et chaque paire de N(x), en retournant q > 0 ⇒ q ≥ ceil(t/2) (Conway : pas 1 à 3). **P.** | fait |  | P |
| K42 | MB:1352 | **K42** Cinq triangles deux à deux disjoints, reliés deux à deux par exactement deux arêtes ⇒ contradiction. **P.** | fait |  | P |
| K43 | MB:1354 | **K43** x, y non adjacents ⇒ D (26 sommets) connexe ou C6 ⊔ cubique connexe ; K_D défini positif. **P.** | fait |  | P |
| K44 | MB:1356 | **K44** Ruban fermé à m centres réparé seulement entre centres ⇒ m ≤ 8 ; cycle de transport ≥ 9 ⇒ identification ou arête | fait |  | P |
| K45 | MB:1358 | **K45** Trois prismes de même projection hors grille ⇒ apices indépendants. **P.** `CA:249_…:L5-8` (L05-086). | fait |  | P |
| K46 | MB:1359 | **K46** Relation moulin–cubique ⇔ vecteur de noyau de profil (2,1^16) ; sous P = 0, 359 types. **E.** `CA:228_…:L6-10` (L05-065). | fait |  | E |
| K47 | MB:1360 | **K47** min c(L) ≥ 4 ⇒ le graphe contient une grille. **P.** `CH:notes/GRILLE_NEUF_FIBRES_2026_10_18.txt:L1-9` (L05-191). | fait |  | P |
| K48 | MB:1361 | **K48** Si k = 10 ⇒ m(e) ∈ {0, 2}, P ≤ 462 ; si k ≤ 20 ⇒ toutes les droites 7-dégénérées (C1, historique : k ≥ 22). **P.** | caduque |  | k = 10, k ≤ 20 hors fenêtre |

### A.11 L06 (C1 arithmétique, LAB) — 56 conditionnels

Répartition : fait 28 ; ouverte 16 ; hors cible 5 ; caduque 3 ; réfutée 2 ; critère 1 ; prouvée 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| COND-01 | MB:1475 | [COND-01] SI L1 n'a aucun vecteur non nul de norme <= 20 ALORS r != 37 ; SI aucun de norme <= 24 ALORS r ∉ {39, 41} ; SI aucun de norme <= 26 ALORS r … | critère | R1-12 | contraposée de « rang r ⇒ vecteurs courts » (C) |
| COND-02 | MB:1476 | [COND-02] SI L1 contient k vecteurs dont la matrice de Gram est inversible mod 7 ALORS r <= 45 - k ¦ statut : P (énoncé de la note) ¦ source : NOTE:25… | fait |  | P |
| COND-03 | MB:1477 | [COND-03] SI 2 a_8 + 16 a_9 + a_13 < 329 (7^m + 1) + 7^(m+1) b_1 + 7 a_7 + 7 a_10 + 2 a_11 + a_12 (m = (45-r)/2) ALORS le rang r est exclu ; avec a_8 … | ouverte | R1-13 | bornes supérieures sur a₉, a₁₃ |
| COND-04 | MB:1478 | [COND-04] SI a_9 = a_13 = 0 ALORS a_8 >= 395 129 (r = 37), 56 588 (r = 39), 8 225 (r = 41), contre a_8 <= 6930 : donc aux rangs 37, 39, 41 il existe u… | fait | R1-13 | C : normes 18 ou 26 forcées aux rangs 37-41 |
| COND-05 | MB:1479 | [COND-05] (r = 43) SI 2 a_8 + 16 a_9 + a_13 < 2632, OU b_2 < 922, OU b_3 < 6 696 790 ALORS r = 43 exclu ; comme b_2 >= 968 est forcé (Codex), SI b_2 <… | ouverte | R1-28 | b₂ ≤ 967 contredirait b₂ ≥ 968 : équivaut à exclure 43 |
| COND-06 | MB:1480 | [COND-06] (r = 37) SI le nombre b_4 de vecteurs distincts de norme 8 de M dépasse 15 196 716 à rho = 126 avec b_3 >= 45 964 (note 204), OU b_4 + (651/… | ouverte |  | minoration de b₄ |
| COND-07 | MB:1481 | [COND-07] (r = 37, what-if exact) r = 37 infaisable SI b_4 >= 18 M seul, OU (b_3 >= 150 000 ET b_4 >= 15 M), OU (b_3 >= 300 000 ET b_4 >= 12 M), OU (b… | ouverte |  | H what-if |
| COND-08 | MB:1482 | [COND-08] (r = 37) SI le nombre total C de paires en collision (tous canaux) < 17,1 M ALORS r = 37 exclu ; suffisant : 27 828 tau_g + 31 976 tau_n + (… | ouverte |  | H ; route close |
| COND-09 | MB:1483 | [COND-09] (r = 37) SI au plus 10 relations indépendantes mod 7 entre classes de grilles au-delà des relations de pinceau ALORS exclu — cible FAUSSE (r… | réfutée |  | relations à un sommet |
| COND-10 | MB:1484 | [COND-10] (r = 37) SI aucune droite n'est dans 4 ou 6 grilles (g(l) <= 3) ALORS tau_g <= 693 et rho <= 115 : environ le facteur nécessaire, sans marge… | ouverte |  | H |
| COND-11 | MB:1485 | [COND-11] (r = 37) SI chaque classe de M a au plus 2 représentants de support <= 9 (resp. au plus 3 de support <= 10) ALORS exclu ; SI les représentan… | réfutée |  | « au plus deux par classe » faux |
| COND-12 | MB:1486 | [COND-12] (r = 37) SI moins de 82 % des représentants sans prisme de support <= 9 sont en collision (10,45 M paires) et les classes ont au plus deux r… | ouverte |  | H |
| COND-13 | MB:1487 | [COND-13] (r = 37, route des graines) SI 539·(9240 kappa_18) + 392·(7920 kappa_20) + 147·(5040 kappa_22) + 49·(4620 kappa_24) + (mêmes poids x nombres… | caduque |  | route des graines fermée |
| COND-14 | MB:1488 | [COND-14] (r = 37, après N14) SI a_8 = a_9 = 0 (N16 et N18 au rang 37) ET au plus 4 vecteurs de norme 20 par graine indépendante (c_20 <= 4 ; c_20 <= … | ouverte | R1-12 | N16, N18, c₂₀ ≤ 4 ouverts ; N14 E |
| COND-15 | MB:1489 | [COND-15] (r = 37) SI a_13 <= 3·10^5 ALORS b_4 <= 11,0 M (facteur 1,8 sur tau) ; SI a_13 <= 10^6 ALORS b_4 <= 13,4 M — pas une exclusion seule ¦ statu… | ouverte |  | H |
| COND-16 | MB:1490 | [COND-16] (historique r = 33, 35) SI a_9 <= 497 122 ALORS r = 33 exclu ; SI au plus 13 configurations de norme 16 par graine ALORS r = 33 sans Fano ex… | caduque |  | r = 33, 35 exclus |
| COND-17 | MB:1491 | [COND-17] SI le graphe a au plus une 22-coclique ALORS il n'a pas de vecteur de Fano ¦ statut : P ¦ source : NOTE:1070-1073 ¦ id : L06-028 | fait |  | P |
| COND-18 | MB:1492 | [COND-18] (r = 43) SI deux 22-cocliques se coupent en i points ALORS i ∈ {1, 8, 15} ; (tout rang) i <= 15 ¦ statut : P ¦ source : NOTE:1054-1058 ¦ id … | fait | R1-17 | P ; redécouverte de L09-133 (25/09) |
| COND-19 | MB:1493 | [COND-19] (cas d'égalité r = 37) SI (a') uniforme ET NT ALORS toute droite est déconnectée à k = 22 ; SI de plus « toutes droites dégénérées » est exc… | ouverte | R1-15 | (a′), NT, déconnexion |
| COND-20 | MB:1494 | [COND-20] (r = 37, P = S = 0) SI NT ET (a') uniforme ALORS contradiction : le monde P = S = 0 du rang 37 est vide (maille >= 5 partout à P = S = 0 ; m… | ouverte | R1-15 | NT et (a′) ouverts |
| COND-21 | MB:1495 | [COND-21] (r = 37) SI toute droite a un graphe G(T) connexe ALORS aucune grille au rang 37 (rho = 0) ¦ statut : P ¦ source : NOTE:2800-2805 ¦ id : L06… | fait |  | P |
| COND-22 | MB:1496 | [COND-22] (r = 37) SI tous les profils de boules à composante prisme autres que (1^6) sont exclus ALORS rho = 0 ¦ statut : P ¦ source : NOTE:3446-3449… | ouverte |  |  |
| COND-23 | MB:1497 | [COND-23] (r = 37) SI rho = 0 est prouvé ALORS, avec les bornes certifiées, AUCUNE exclusion ne suit (seuil 25 201 < 31 976, masses 7-9 non bornées) ¦… | fait |  | H : aucune exclusion |
| COND-24 | MB:1498 | [COND-24] (r = 37, what-if) SI a_7 = a_8 = 0 ALORS le seuil sans grille 33 780 dépasse le cap 31 976 — « pas une exclusion » ¦ statut : H ¦ source : N… | fait |  | H : pas une exclusion |
| COND-25 | MB:1499 | [COND-25] (r = 37) SI toute boule de tout type (connexe, à torsion, déconnectée) échoue son test d'étoile ALORS r = 37 exclu, sans lemme global ¦ stat… | ouverte | R1-11 | toute boule de tout type |
| COND-26 | MB:1500 | [COND-26] (r = 37) SI une droite connexe sans torsion a tau(G(T)) résidu quadratique mod 7 ALORS contradiction (aucune sélection de 60 ombres binaires… | fait |  | P |
| COND-27 | MB:1501 | [COND-27] (L23) SI une droite a d(L) = 1 et (tau¦7) = +1 ALORS k >= 24 (r >= 39) ¦ statut : P ¦ source : JOURNAL:164-169 ¦ id : L06-147 | fait |  | L23 |
| COND-28 | MB:1502 | [COND-28] (L21) SI une droite a d(L) = 1 ALORS k >= 22 (r >= 37) ; en général k >= 23 - d(L) + 2 r(L) ¦ statut : P ¦ source : JOURNAL:139-142, 425-428… | fait |  | L21 |
| COND-29 | MB:1503 | [COND-29] (sous NT) k >= 20 ; SI P = 0 ALORS k >= 22 ; SI k = 22 et aucune droite générique ALORS toute droite est non connexe ; SI NT, k = 22, aucune… | fait |  | P sous NT ; parties k = 20 hors fenêtre |
| COND-30 | MB:1504 | [COND-30] SI le graphe a un point de Hamming ALORS 18 <= k <= 26 ; (L8) il n'en a pas ¦ statut : P ¦ source : JOURNAL:170-173, 200-211 ¦ id : L06-148 | fait |  | L8 |
| COND-31 | MB:1505 | [COND-31] SI un tissu de 11 grilles a tous ses couplages anti ALORS il existe un plan projectif d'ordre 10 avec polarité (exclu par Lam) ¦ statut : P … | fait |  | L25 (Lam) |
| COND-32 | MB:1506 | [COND-32] SI rank_7(A - 3I) <= 21 ALORS pas de srg(99,14,1,2) (trivial vu la borne inférieure) ¦ statut : P ¦ source : rank7.tex:260-261 ¦ id : L06-13… | caduque |  | trivial |
| COND-33 | MB:1507 | [COND-33] (S5) SI r - s a un facteur premier = 3 mod 4 ALORS le critère ne contrôle pas c_q : ne s'applique pas à 99 (d = 7) ¦ statut : P ¦ source : s… | fait |  | S5 hors 99 |
| COND-34 | MB:1508 | [COND-34] (243) SI chaque maillon de la chaîne S3 tient ALORS les srg(243,22,1,2) à spread régulier sont exactement BvLS, twin, Gamma3, Gamma4 ¦ statu… | hors cible |  | srg(243) |
| COND-35 | MB:1509 | [COND-35] (243) SI un revêtement non cyclique de BH existe ALORS c'est un graphe distance-régulier asymétrique ¦ statut : S ¦ source : S3:189-195 ¦ id… | hors cible |  | srg(243) |
| COND-36 | MB:1510 | [COND-36] (243) SI un srg(243,22,1,2) est asymétrique ALORS il est sans spread régulier, sans Hamming plié induit, sans droite attachée comme dans BvL… | hors cible |  | srg(243) |
| COND-37 | MB:1511 | [COND-37] (99) SI un srg(99,14,1,2) existe ALORS il n'a pas de spread régulier ; aucune preuve ne peut passer par « tout srg(v,k,1,2) a un spread régu… | fait |  | P |
| COND-38 | MB:1512 | [COND-38] (dossier externe) SI les cinq bords de transport de longueur quatre sont non réalisables ALORS tous les cycles de transport de longueur quat… | ouverte |  | cinq bords de transport |
| COND-39 | MB:1513 | [COND-39] (quadrangle) SI Delta(Q) != 0 ALORS les 44 projections forment une base et le graphe est déterminé par les quatre murs et 51 ombres ¦ statut… | fait |  | P |
| COND-40 | MB:1514 | [COND-40] (parité) SI la loi des quadrangles c(Q) = c_va + c_aw + c_wb + c_bv mod 2 est vraie ALORS une condition d'un bit par configuration à quatre … | ouverte |  | loi des quadrangles |
| COND-41 | MB:1515 | [COND-41] aucun candidat n'a tous ses quadrangles d'holonomie impaire ¦ statut : P ¦ source : RB:98 ¦ id : L06-109 | fait |  | P |
| COND-42 | MB:1516 | [COND-42] SI les certificats de Codex pour les 63 + 136 coeurs exclus tiennent ALORS x_58 = x_59 = 0 dans tout srg(99,14,1,2) ¦ statut : E ¦ source : … | prouvée | R1-21 | x₅₈ = x₅₉ = 0 par le lemme de variance (L09-COND-053, P), sans certificats |
| COND-43 | MB:1517 | [COND-43] (Keramatipour, preuve omise) « pas onze sous-graphes Paley(9) disjoints » : non utilisable tel quel ¦ statut : H ¦ source : NOTE:1759-1761 ¦… | ouverte |  | preuve omise |
| COND-44 | MB:1518 | [COND-44] SI le graphe n'a pas de grille ALORS toute solution entière de (A - 3I) y = 1 a norme >= 15, et norme 15 seulement pour y = 1_P - 1_Q (Q dro… | fait |  | P |
| COND-45 | MB:1519 | [COND-45] SI un point a ses 4 lignes de graine deux à deux en grilles et ses 3 autres lignes deux à deux en grilles ALORS aucun vecteur de norme 16 n'… | fait |  | P |
| COND-46 | MB:1520 | [COND-46] SI les sept droites d'un sommet se répartissent en 4 + 3 deux à deux en grilles ALORS les 6 grilles et les 3 grilles satisfont une relation … | fait |  | P |
| COND-47 | MB:1521 | [COND-47] (droite à six grilles, r >= 37) SI deux points de la droite ont trois lignes hub chacun ALORS le troisième n'en a qu'une ; le motif (2,2,1) … | fait |  | C (Codex) |
| COND-48 | MB:1522 | [COND-48] SI W_1, W_2 sont des moulins pondérés disjoints ALORS u_1 - u_2 n'est pas vecteur propre de valeur 3 ; SI 1_U - 1_V est vecteur propre (U cu… | fait |  | P |
| COND-49 | MB:1523 | [COND-49] SI deux 8-ensembles cubiques induits ont la même projection ALORS ils sont anticomplets (et réciproquement) ¦ statut : P ¦ source : NOTE:298… | fait |  | P |
| COND-50 | MB:1524 | [COND-50] SI f est un vecteur propre entier (-4) de norme 18 ALORS ses deux supports sont indépendants ¦ statut : P ¦ source : NOTE:3972-3982 ¦ id : L… | fait |  | P |
| COND-51 | MB:1525 | [COND-51] SI un vecteur propre entier (-4) a une entrée de valeur absolue >= 2 ALORS sa norme est >= 20 ¦ statut : P ¦ source : BP README:52-55 ¦ id :… | fait |  | P |
| COND-52 | MB:1526 | [COND-52] SI deux graines au même sommet s'étendent en vecteurs de Fano ALORS elles partagent au plus 2 voisins ¦ statut : P ¦ source : NOTE:597-606 ¦… | fait |  | P |
| COND-53 | MB:1527 | [COND-53] SI y, z et y + z sont des vecteurs de Fano ALORS contradiction (lemme F) ¦ statut : P ¦ source : NOTE:338-341, 607-612 ¦ id : L06-014 | fait |  | P |
| COND-54 | MB:1528 | [COND-54] (243) SI le graphe est BvLS, twin, Gamma3 ou Gamma4 ALORS tout vecteur propre entier (-5) non nul a norme >= 24 ¦ statut : E ¦ source : BP R… | hors cible |  | srg(243) |
| COND-55 | MB:1529 | [COND-55] (BH) toute signature de BH avec toutes les paires séparées est impossible ¦ statut : S (LAB, 0,2 s) ; article Cesarz-Williford lu par l'abst… | hors cible |  | BH |
| COND-56 | MB:1530 | [COND-56] (dossier externe) h_H est un vecteur triangulaire SI ET SEULEMENT SI il n'y a pas d'exception et Z_0 est un triangle ¦ statut : P ¦ source :… | fait |  | P |

### A.12 L07, lot principal (R1-R45) — 45 conditionnels

Répartition : ouverte 21 ; réfutée 9 ; chaîne 5 ; fait 4 ; caduque 2 ; critère 2 ; hors cible 2.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| R1 | MB:1635 | R1 ¦ (H-MATCH) aux 21 paires de droites d'UN sommet. Pour toute paire (l, m), le bloc à quatre étoiles admissible avec T, U ⪰ 0 et nullité ≥ 14 vérifi… | ouverte | R1-08 | H-MATCH |
| R2 | MB:1636 | R2 ¦ (H-MATCH) aux 15 paires de six droites d'un sommet ¦ point de Hamming, via kk5 (DRAT) et L8 ¦ O ¦ P ¦ id. l.74-80 ¦ | ouverte | R1-08 |  |
| R3 | MB:1637 | R3 ¦ (H-INV) : tout bloc PSD de nullité ≥ 14 est h-invariant ¦ (H-MATCH), donc pas de Conway ¦ O ¦ P ¦ id. l.31 ¦ | chaîne | R1-08 | (H-INV) ouvert |
| R4 | MB:1638 | R4 ¦ (S1) ν = 14 ⇒ N = hN, et (S2) N = hN, ν = 14, PSD ⇒ aucune torsion ¦ (H-MATCH) ¦ O ¦ P ¦ `work/stars_rank_2026-10-14/MECHANISM_A_2026-10-15.md:24… | chaîne | R1-08 | (S1), (S2) ouverts |
| R5 | MB:1639 | R5 ¦ (KER-SYM-14) + (FAKE-13) + lemme 6h ¦ (S1) ¦ O ¦ P ¦ id. l.266-269, 340-341 ¦ | chaîne | R1-08 | KER-SYM-14, FAKE-13 ouverts ; KER-SYM universelle réfutée |
| R6 | MB:1640 | R6 ¦ (N9) : nullité ≤ 9 + min(c(l), c(m)) pour tout bloc PSD, plus le census ρ ≤ 126 ¦ c(l) ≥ 5 + δ partout, ρ ≥ 154 > 126 : pas de Conway ¦ **R** ¦ P… | réfutée | R1-07 | N9 réfuté par des objets à grille (E6) |
| R7 | MB:1641 | R7 ¦ (NOGRID) + (LOW), ou (N9) + (NOGRID) ¦ pas de Conway, sans census ¦ **R** ¦ P ¦ id. l.70-78 ¦ | réfutée |  | (NOGRID) réfuté (E6) |
| R8 | MB:1642 | R8 ¦ (N9-NG) : bloc PSD SANS grille sur (l, m) ⇒ nullité ≤ 9 + min(c(l), c(m)) ; avec P ≤ 852 ou ρ ≤ 126 ¦ toute droite a c ≥ 5, g ≥ 4, t ≥ 8, d'où P … | ouverte | R1-07 | N9-NG |
| R9 | MB:1643 | R9 ¦ (NG5) : bloc non-grille PSD de nullité ≥ 14 ⇒ c(l), c(m) ≥ 5 ¦ idem R8 ¦ O ¦ P ¦ id. l.105-106 ¦ | ouverte | R1-07 | NG5 |
| R10 | MB:1644 | R10 ¦ (NG7) : aucun bloc non-grille avec min(t(l), t(m)) ≤ 7 ne passe les tests de bloc de Conway ¦ pas de Conway (≥ 254 tels blocs forcés) ¦ O ¦ P (C… | ouverte | R1-07 | NG7 |
| R11 | MB:1645 | R11 ¦ (NG14) : aucun bloc PSD non-grille de nullité ≥ 14 ne passe rang_F7 ≤ 28, DISC et l'extension ¦ pas de Conway, avec Makhnev seul ¦ O ¦ P ¦ id. l… | ouverte | R1-07 | NG14 |
| R12 | MB:1646 | R12 ¦ (T8) : nullité ≥ 14 ⇒ t(l) ≥ 8 et t(m) ≥ 8 ; variante (T15) t(l) + t(m) ≥ 15 ¦ P ≥ 924, ou P ≥ 866,25 ; avec P ≤ 852 : pas de Conway ¦ O ¦ P ¦ `… | ouverte | R1-06 | T8/T15 ; quasi-raté 866,25 contre 852 |
| R13 | MB:1647 | R13 ¦ « au moins une droite avec t ≥ 8 » ¦ P ≥ 792 : n'exclut rien ¦ — ¦ P ¦ `AUDIT_EXCLUSIONS:139-140` ¦ | fait |  | n'exclut rien |
| R14 | MB:1648 | R14 ¦ (K22) : nullité ≥ 14 ⇒ rang_7(8T_S4) ≥ 23 ; variante ≥ 25 ¦ k ≥ 24 : r = 37 exclu ; avec ≥ 25 : r = 37 et 39 exclus ¦ O ¦ P ¦ `AUDIT_EXCLUSIONS:… | ouverte | R1-10 | K22 |
| R15 | MB:1649 | R15 ¦ (SQ30) + (N15) (aucun bloc PSD de nullité ≥ 15) ¦ pas de Conway ¦ (SQ30) artefact h ; (N15) O ¦ P ¦ `AUDIT_EXCLUSIONS:48-49, 95-96` ¦ | réfutée |  | (SQ30) artefact h ; (N15) ouvert |
| R16 | MB:1650 | R16 ¦ (B') : aucun bloc PSD de nullité ≥ 14 n'a une droite avec c = 1 ; avec (C) : tout Conway a une droite non spéciale ¦ pas de Conway. (B') seule d… | ouverte | R1-14 | (B′), (C) ouverts |
| R17 | MB:1651 | R17 ¦ ODD9 (gain impair exactement 9) ¦ c(l) ≥ 2 + δ, toute droite spéciale, (B') ¦ **R** ¦ P ¦ `NOTE_PROOFS_1410.md:356-364` ¦ | réfutée |  | ODD9 réfuté |
| R18 | MB:1652 | R18 ¦ (A) : trois étoiles, c(l) = 1, T, U ⪰ 0 ⇒ rang 31 ; avec (C) ¦ pas de Conway. (A) seul donne (B) ¦ **R** ¦ P ¦ `NOTE_PROOFS_1410.md:461-468` ¦ | réfutée |  | (A) réfuté |
| R19 | MB:1653 | R19 ¦ (H3) + L8 ¦ (visé) pas de Conway. Insuffisant même vrai : un bloc à trois étoiles a le rang 30 − δ′ ¦ **R** ¦ — ¦ `AUDIT_EXCLUSIONS:24, 37-39` ¦ | réfutée |  | (H3) |
| R20 | MB:1654 | R20 ¦ (H4) : aucun bloc à quatre étoiles PSD ¦ pas de Conway ¦ **R** ¦ P ¦ `NOTE_STARS_RANK.md:83-98` ¦ | réfutée |  | (H4) |
| R21 | MB:1655 | R21 ¦ (R7) : PSD à quatre étoiles ⇒ rang_7 ≥ 29 ; variante « ≥ 23 » ¦ contradiction avec k ≤ 28 (L22) ; la variante exclurait k = 22 (r = 37) ¦ **R** … | réfutée | R1-10 | (R7) réfuté par un objet à grille (7-rang 25) ; R7-NG ouvert |
| R22 | MB:1656 | R22 ¦ plafond « ≤ 2 relations mixtes » ; « ≤ 3 » ¦ ρ ≥ 198 > 191 ; ρ ≥ 154 > 126 ¦ **R** ¦ P ¦ `NOTE_PROOFS_1410.md:316-318` ¦ | réfutée |  |  |
| R23 | MB:1657 | R23 ¦ aucune structure admissible à 5 étoiles (52 labels), ou les 34 cas M_4 tous UNSAT ¦ pas de Conway (il faudra DRAT par cas, un modèle indépendant… | ouverte | R1-09 | cinq étoiles |
| R24 | MB:1658 | R24 ¦ R8 UNSAT (4 étoiles exactes + les 8 labels {4, t}, lettre 4 bornée) ¦ pas de Conway ¦ O ¦ P (modèle jugé solide le 20/10, lot L08) ¦ `REVUE_GLOB… | ouverte | R1-09 | R8 |
| R25 | MB:1659 | R25 ¦ un germe h-relié en (l, m) s'étend à une 3ᵉ droite n que M_0 n'apparie pas ¦ contre-exemple exact à (H-MATCH) ¦ — ¦ P ¦ `EXT84_2026-10-16.md:52-… | ouverte | R1-08 | germe non réalisé |
| R26 | MB:1660 | R26 ¦ le cadre coclique (22 de Hoffman et 21 maximales, sept profils) est exclu ET α ≥ 21 est prouvé ¦ pas de Conway ¦ O (α ≥ 21) ¦ P ¦ `work/c1_cocli… | ouverte | R1-17 | cadre coclique et α ≥ 21 |
| R27 | MB:1661 | R27 ¦ échelle de rangs (NOTE du 12/10, 17.101 (6), lot L06) : aux rangs 37, 39, 41, vecteur propre entier de −4 de norme 18 ou 26 ; au rang 43, norme … | ouverte | R1-13 | normes 18/26 |
| R28 | MB:1662 | R28 ¦ b = 30 (rang 31) ¦ B contient un vecteur entier de −4 de norme ≤ 18 ; ≤ 20 si b = 32, 34 ; ≤ 24 si b = 36-40 ; ≤ 26 si b = 42 ¦ E (sans certific… | caduque |  | rang 31 exclu |
| R29 | MB:1663 | R29 ¦ a₄ > 1,42·10⁷ (ou 1,31·10⁷ avec a₅ ≥ 3·10⁷) ; a₃ > 9,8·10⁵ ; a₅ > 3,0·10⁸ ¦ b = 34 (rang 35) exclu ¦ non atteignable par les comptes connus ¦ E … | caduque |  | rang 35 exclu |
| R30 | MB:1664 | R30 ¦ une pièce H FORCÉE dans un Conway, avec c complétions et ¦Aut(H)¦ > c ¦ pas de C1. Une pièce forcée à complétion unique doit être rigide ¦ dép… | ouverte | R1-16 | pièce forcée symétrique manquante |
| R31 | MB:1665 | R31 ¦ un groupe H préserve TOUTE l'instance (contraintes et clauses de blocage), avec une borne U < ¦H¦ sur le nombre de complétions ¦ instance excl… | critère | R1-20 |  |
| R32 | MB:1666 | R32 ¦ deux flips simples indépendants préservent l'instance, et l'instance a au plus 2 complétions (résidu spectral de rang ≤ 1) ¦ la branche est ferm… | critère | R1-20 |  |
| R33 | MB:1667 | R33 ¦ α = 22 et un design Y à complétion unique avec Aut(Y) ≠ 1 ¦ le graphe n'est pas asymétrique, donc pas de C1 ¦ — ¦ P ¦ `conway99-c1:origin/claude… | ouverte | R1-17 | α = 22 + design rigide |
| R34 | MB:1668 | R34 ¦ la balance vaut en général pour les revêtements à fibres-grilles ¦ le sous-cas (A) (11 grilles) est impossible ¦ O ¦ P ¦ `…/notes/169_DEUX_PISTE… | ouverte |  | balance |
| R35 | MB:1669 | R35 ¦ conjecture (P) : toute arête est dans un prisme ¦ t₃ ≥ 231, t₂ ≤ 3465 : exclut le profil sans prisme ¦ O ¦ P ¦ `…/notes/177_STRUCTURE_ARETE_B.md… | ouverte |  | (P) |
| R36 | MB:1670 | R36 ¦ V7 : énumération exhaustive de O_x puis O_y UNSAT pour les 5 849 couples représentants ¦ le sous-cas V7 est fermé ¦ O ¦ P ¦ `conway99-c1:origin/… | ouverte |  | V7 |
| R37 | MB:1671 | R37 ¦ aucun S3-revêtement de BH n'existe ¦ tout srg(243,22,1,2) à étalement régulier a un automorphisme d'ordre 3 (hors Conway) ¦ O ¦ P ¦ `…/notes/175… | hors cible |  | srg(243) |
| R38 | MB:1672 | R38 ¦ Conway n'existe pas ¦ tout automorphisme d'ordre 5 d'un srg(494019) fixe exactement un Paley(9), et tout automorphisme d'ordre 7 fixe un seul so… | hors cible |  | sens inverse |
| R39 | MB:1673 | R39 ¦ un sous-graphe induit H à 45 sommets avec det(A_H − 3I) ≠ 7^(30−k) n², ou à 55 sommets avec det(A_H + 4I) ≠ 2·7^(40−k) n² ¦ H n'est dans aucun C… | fait | R1-01 | DISC avec k explicite |
| R40 | MB:1674 | R40 ¦ un bloc principal de 8T avec rang_7 > k (≤ 28) ¦ ce n'est pas un bloc de Conway ¦ — ¦ P (L22) ¦ `NOTE_PROOFS_1410.md:254-264` ¦ | fait |  | L22 |
| R41 | MB:1675 | R41 ¦ K7 en tout point d'une coclique de Hoffman ¦ Σ_c Σ_{e<f} n_ef² = 22·21 (équivalence) ¦ O ¦ P ¦ `…/notes/173_CONJECTURE_K7.md:73-75` ¦ | ouverte |  | K7 |
| R42 | MB:1676 | R42 ¦ ODDCONST(m) + EVEN′ (dim P₀ ≤ 7) ; ou (SYM) + (QUOT : ν(A++) ≤ 7 + min c) ¦ (N9-NG) du côté l ¦ O ¦ P ¦ `N9NG_ATTACK_2026-10-15.md:16-23, 58-86`… | chaîne | R1-07 | ODDCONST, EVEN′, SYM, QUOT ouverts |
| R43 | MB:1677 | R43 ¦ (SYM) seule ¦ (NG5) à min c = 1 ¦ O ¦ P ¦ id. l.79-86 ¦ | chaîne | R1-07 | (SYM) ouvert |
| R44 | MB:1678 | R44 ¦ **combinaison** de V15 (Codex, 14/10) et du principe de symétrie forcée. V15 : tout Conway a un bord positif H de 43 sommets (3I − B + J/9 > 0) … | ouverte | R1-16 | bord symétrique inévitable manquant |
| R45 | MB:1679 | R45 ¦ sur le bord positif de 43 sommets, plus de deux choix de signes ¦ force un vecteur propre de −4 de norme 14, donc un co-Heawood disjoint du bord… | fait |  | P ; au rang 37 avec N14 (E) : ≤ 2 choix de signes |

### A.13 L07, sous-lot K (pont Codex) — 28 conditionnels

Répartition : fait 11 ; ouverte 9 ; critère 5 ; chaîne 2 ; réfutée 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| K1 | MB:1824 | K1 ¦ NG5 : tout bloc à quatre étoiles admissible NON-grille avec T, U PSD et ν >= 14 a c >= 5 ¦ pas de Conway (via c <= g + floor((6-g)/2) => g >= 4, … | ouverte | R1-07 | NG5 |
| K2 | MB:1825 | K2 ¦ NG7 : aucun bloc non-grille avec min(t(l),t(m)) <= 7 ne passe T/U PSD, ν_T >= 14, F7, DISC, extension ¦ pas de Conway (il en existe >= 254) ¦ O ¦… | ouverte | R1-07 | NG7 |
| K3 | MB:1826 | K3 ¦ rang(F) >= 12 (F = Q + J/12) pour tout bloc non-grille admissible, droite de c minimum (<=> N9-NG) ¦ pas de Conway (Conway force rang F <= 7 + c_… | ouverte | R1-07 | rang F ≥ 12 |
| K4 | MB:1827 | K4 ¦ NG5 restreint : rang S >= 9, 10, 11, 12 hors grille pour c_l = 1, 2, 3, 4 ¦ NG5, donc pas de Conway ¦ O ¦ P (identités de rang) ¦ `LE/codex_bridg… | chaîne | R1-07 | bornes de rang S ouvertes |
| K5 | MB:1828 | K5 ¦ ODD-PURE universel : rang D = 9 (aucune relation purement impaire non constante) ¦ aucun bloc de Conway avec c_min = 1 ; pour c = 2, 3, 4 il rest… | ouverte | R1-07 | ODD-PURE |
| K6 | MB:1829 | K6 ¦ ODD-PURE + rang Z >= c - 1 (c = 2, 3, 4), ou SYM6 (rang Z >= 3) + rang D = 9 ¦ N9-NG (cible Q7), donc pas de Conway ¦ O ¦ P ¦ `LE/H/bridge_sym6_9… | chaîne | R1-07 |  |
| K7 | MB:1830 | K7 ¦ (H-MATCH) : T, U >= 0 et ν >= 14 => M_1 = h(M_0) et M_3 = h(M_2) ¦ tout sommet est de Hamming => pas de Conway (L8) ¦ O ¦ P (LAB, acceptée par Co… | ouverte | R1-08 | H-MATCH |
| K8 | MB:1831 | K8 ¦ (A) + (C) ¦ pas de Conway ¦ (A) R ¦ — ¦ `LE/codex_after741_joint_fourth_star.txt:1` ¦ | réfutée |  | (A) réfuté |
| K9 | MB:1832 | K9 ¦ un bord de Conway appartient à la famille G1 c55 non-grille ¦ contradiction rang_F7(8T_S) >= 29 > 28 ¦ — ¦ E (établi) ¦ `LE/codex_c55_excluded_af… | fait |  | E |
| K10 | MB:1833 | K10 ¦ un bord de Conway porte la symétrie locale <z,hM> ¦ contradiction (ν <= 14 ; à 14, rang_F7 >= 29 > 28) ¦ — ¦ C (établi) ¦ `LE/codex_z5hm_deliver… | fait |  | C |
| K11 | MB:1834 | K11 ¦ les templates 7, 9, 19 sont fermés (correctement, après correctif) ¦ aucun Conway dont toutes les droites ont c >= 4 ¦ O (rouverts le 18/10) ¦ S… | fait | R1-14 | S (79/79 après correctif ; sans certificat portable) |
| K12 | MB:1835 | K12 ¦ aucune Γ84 binaire C1-exacte n'a T et U PSD ¦ pas de Conway (équivalence) ¦ O ¦ P ¦ `LE/H/message_907_global_psd_reply.txt:5` ¦ | critère |  | équivalence avec le but |
| K13 | MB:1836 | K13 ¦ sur 84 étiquettes : T, U PSD et rang T <= 30 ¦ l'objet est un SRG99 (sens « construction ») ¦ — ¦ P ¦ `LE/codex_bridge_complete_assembly.txt:5` … | fait |  | P |
| K14 | MB:1837 | K14 ¦ #complétions ÉTIQUETÉES d'un bord H < ¦Aut(H)¦ ¦ aucune complétion asymétrique de H (exclut C1 si H est forcé) ¦ à établir pour chaque H ¦ P ¦ `… | critère | R1-16 |  |
| K15 | MB:1838 | K15 ¦ « borne strictement positive [du défaut tr(TU)] pour toutes les matrices binaires candidates » ¦ contradiction globale ¦ O (formulation ambiguë)… | ouverte |  | formulation ambiguë |
| K16 | MB:1839 | K16 ¦ (P) : toute arête est dans un prisme ¦ P >= 231 (insuffisant seul contre 852) ¦ O (conjecture) ¦ P ¦ `LE/codex_bridge_849_torsion_census_ng7.txt… | ouverte |  | (P) |
| K17 | MB:1840 | K17 ¦ le minimum observé rang_F7(8T44) = 30 devient un théorème ¦ contradiction avec <= 28 ¦ non prouvé (refusé comme théorème) ¦ — ¦ `LE/H/message_ra… | ouverte | R1-10 | observation (≥ 30 sur 3 722 NG) non prouvée |
| K18 | MB:1841 | K18 ¦ G1'' et H-MATCH cassé ¦ g_m <= 1 et c_m <= 3 (cubes c_m >= 4 exclus) ¦ — ¦ P ¦ `LE/codex_bridge_809_grid_cut.txt:3` ¦ | fait |  | P |
| K19 | MB:1842 | K19 ¦ <z,hM> et d = (7-2ε_l)(7-2ε_m) - (2(t+w)+1)^2 ≢ 0 mod 5 ¦ b = 0 et null T <= 9 (7/14 types) ¦ — ¦ P ¦ `LE/codex_z5hm_mod5_progress.txt:5` ¦ | fait |  | P |
| K20 | MB:1843 | K20 ¦ moyenne à >= 40 cassures avec tr S < 20/7 ¦ toutes ses orientations exclues ¦ à tester ¦ P ¦ `LE/codex_response_792.txt:8` ¦ | critère |  | à tester |
| K21 | MB:1844 | K21 ¦ diagonal rationnel d, H - diag(d) >= 0 et Σd > 10 ¦ toutes les orientations d'une moyenne exclues ¦ à tester ¦ P ¦ `LE/codex_response_792.txt:10… | critère |  | à tester |
| K22 | MB:1845 | K22 ¦ (α_1…α_p)(β_1…β_p) > 1 (valeurs généralisées shortées) ¦ nullité T < nullité T0 + p (ex. pas de ν = 14 si ν(T0) = 12 et p = 2) ¦ à tester ¦ P ¦ … | critère |  | à tester |
| K23 | MB:1846 | K23 ¦ e(O ∪ S) = 49 pour un S équilibré ¦ T non PSD ¦ — ¦ P ¦ `LE/codex_bridge_839_odd9_integer_cut.txt:5` ¦ | fait |  | P |
| K24 | MB:1847 | K24 ¦ une relation plate d'incidence nulle de support <= 14 touche O ¦ contradiction (binaire, C1, C2, T, U PSD) ¦ — ¦ P ¦ `LE/codex_bridge_862_suppor… | fait |  | P |
| K25 | MB:1848 | K25 ¦ une étoile est rematchée seule (P -> P') en gardant T PSD ¦ P'v = -v sur W = proj_S(ker T) ∩ ker(P + I) ¦ — ¦ P ¦ `LE/codex_bridge_877_antipodal… | fait |  | P |
| K26 | MB:1849 | K26 ¦ R8 UNSAT (après DRAT + modèle indépendant + relecture) ¦ pas de Conway (énoncé LAB, relayé) ¦ O (UNKNOWN) ¦ énoncé LAB hors sous-lot ¦ `LE/H/lit… | ouverte | R1-09 | R8 |
| K27 | MB:1850 | K27 ¦ si un voisinage de ligne fermé dans la base a plusieurs composantes C ¦ égalités n_C(z) = c/6 pour tout z de X, conditions universelles de prolo… | fait |  | P |
| K28 | MB:1851 | K28 ¦ ν < 11 + max(c_l, c_m) ¦ les équations du noyau seules ne forcent aucun h·p (symétrie forcée seulement possible à ν >= 14) ¦ — ¦ P ¦ `LE/codex_b… | fait |  | P |

### A.14 L07, sous-lot (c) — 24 conditionnels

Répartition : fait 14 ; ouverte 7 ; critère 2 ; réfutée 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| l.2002 | MB:2002 | NG7 : aucun objet quatre étoiles non-grille avec min(t_l,t_m) <= 7 ne satisfait T,U PSD, nu_T >= 14, F7, DISC (si applicable) et extension ¦ Pas de Co… | ouverte | R1-07 | NG7 |
| l.2003 | MB:2003 | NG5 : non-grille et nu >= 14 => min(c_l,c_m) >= 5 ¦ NG7, donc pas de Conway ; directement : toute droite a g >= 4, t >= 8, donc P >= 924 > 852 ¦ O / P… | ouverte | R1-07 | NG5 |
| l.2004 | MB:2004 | N9-NG : nu <= 9 + min(c_l,c_m) hors grille ¦ NG5, puis pas de Conway ¦ O / P ¦ J:5191-5201 ¦ | ouverte | R1-07 | N9-NG |
| l.2005 | MB:2005 | H-MATCH : C1, C1', C2, T/U PSD et nu(T) >= 14 => M1=h(M0), M3=h(M2) ¦ Tout sommet est un point de Hamming, contradiction avec L8 : pas de Conway (rédu… | ouverte | R1-08 | H-MATCH |
| l.2006 | MB:2006 | H4' : aucune extension à quatre étoiles avec deux Q connexes, les deux PSD et rang T <= 30 ¦ Tout sommet a au plus une droite non spéciale ¦ O ¦ J:263… | ouverte |  | H4′ |
| l.2007 | MB:2007 | ODD9 (gain impair 9) ¦ B' (toute droite spéciale) ¦ ODD9 : R ; B' : O ¦ J:4910 ¦ | réfutée |  | ODD9 |
| l.2008 | MB:2008 | Toutes les droites avec c(L) >= 4 ¦ Contradiction ; il existe donc une droite c(L) <= 3 ¦ S (CP-SAT) ¦ RAC:326-336 ¦ | fait | R1-14 | S |
| l.2009 | MB:2009 | Les 8 cas (positions de L par rapport à une racine o avec s(o) <= 51, et c(L) <= 3) sont tous INFEASIBLE ¦ Pas de Conway. Un seul cas INFEASIBLE ne su… | ouverte | R1-14 | cas 7 UNKNOWN |
| l.2010 | MB:2010 | Coupure par orbites pour C1 : le groupe L de l'instance ENTIÈRE agit librement sur les complétions asymétriques ; si le nombre total de complétions U … | critère | R1-16 |  |
| l.2011 | MB:2011 | Deux retournements individuels préservent l'instance et un certificat donne au plus 2 complétions étiquetées ¦ Branche impossible pour TOUT SRG (¦Ome… | fait | R1-20 | P |
| l.2012 | MB:2012 | Forme générale : S = {s dans L : 0 < poids < ceil(t/2)} ; dépendance impaire XOR-zéro ; majorant certifié U <= 3 ¦ Omega vide ¦ P ¦ J:1751-1757 ¦ | fait |  | P |
| l.2013 | MB:2013 | Bord 44 de la famille G1 c55 non grille, T/U PSD ¦ rang_F7(8T_S) >= 29 > 28, donc pas d'extension en Conway ¦ P (dépend de la borne globale <= 28 de L… | fait |  | P |
| l.2014 | MB:2014 | Bord 44 local invariant sous <z,hM>, avec C1, C1', C2, T,U PSD ¦ nu <= 14 ; à 14, rang_F7 >= 29 : pas d'extension ¦ C (520 certificats) ¦ J:4321-4329 … | fait |  | C |
| l.2015 | MB:2015 | G1'' brisant H-MATCH avec c_m >= 4, sous T >= 0 ¦ Exclu ¦ P ¦ J:4154-4160 ¦ | fait |  | P |
| l.2016 | MB:2016 | Espace global T8 de rang 30 de classe de discriminant différente de 2 et 14 (ou U15 de rang 40, classe différente de 1 et 7) ¦ Pas de Conway (théorème… | fait | R1-01 | classes à resserrer : 2 seule (T), 1 seule (U) |
| l.2017 | MB:2017 | Cœur principal de rang 30 de mauvaise classe DISC ¦ Aucune modification des sommets retirés ne donne un graphe global ; il faut baisser le rang du cœu… | fait | R1-01 | P |
| l.2018 | MB:2018 | Gamma84 binaire, symétrique, diagonale nulle, C1 exacts, T,U PSD ¦ SRG99 (équivalence). Exclure Conway revient à montrer qu'aucun tel point binaire n'… | critère |  | équivalence avec le but |
| l.2019 | MB:2019 | Candidat binaire C1 avec e(O u S) = 49 ¦ T non PSD (coupe stricte <= 48) ¦ P ¦ J:4741-4749 ¦ | fait |  | P |
| l.2020 | MB:2020 | Relation plate de ker T (Bq=0, coefficients 0,+-1) de support <= 12 violant C4DO ¦ Impossible ; support <= 14 => q nul sur O ¦ P ¦ J:5420-5426, 5548-5… | fait |  | P |
| l.2021 | MB:2021 | Relation Tz=0, z=2q+u, avec 2, 4, 6 ou 8 coefficients impairs sur les 34 labels ¦ Globalement exclue ¦ P ¦ J:2330-2340 ¦ | fait |  | P |
| l.2022 | MB:2022 | Quatre grilles restent forcées de chaque côté ¦ min(t_l,t_m) >= 8 : la classe ne peut atteindre NG7 ¦ P ¦ J:5294-5296 ¦ | fait |  | P |
| l.2023 | MB:2023 | Remplacement des seules arêtes internes d'une étoile par P', avec T' PSD ¦ P'v = -v sur W ; si les seules paires opposées sont les anciennes arêtes, P… | fait |  | P |
| l.2025 | MB:2025 | Conjecture (P) : toute arête est dans un prisme ¦ P >= 231, insuffisant seul contre 852 ¦ O ¦ J:5222-5224 ¦ | ouverte |  | (P) |
| l.2026 | MB:2026 | d != 0 mod 5 dans l'un des 14 quotients de <z,hM> ¦ Bloc - inversible et nullité <= 9 (vrai pour 7 des 14) ¦ P ¦ J:4497-4517 ¦ | fait |  | P |

### A.15 L07, sous-lot (d) (cocliques, bords) — 29 conditionnels

Répartition : fait 23 ; ouverte 4 ; chaîne 2.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| l.2146 | MB:2146 | UNSAT de la recherche par cubes « srg(99,14,1,2) + coclique de Hoffman fixée » ¦ α ≤ 21 pour tout srg(99,14,1,2) (pas C1) ¦ O (aucun verdict) ¦ `RCA/.… | ouverte | R1-17 | aucun verdict |
| l.2147 | MB:2147 | Exclusion des 22 et 21 sans borne α ≥ 21 ¦ seulement α ≤ 20 ¦ P ¦ `AG:1525-1526` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2148 | MB:2148 | f_ij < 2 − z_ij pour une paire de blocs du bord de Hoffman ¦ bord exclu ; si f_ij = 2 − z_ij, arête ij interdite ¦ P ¦ `COUV:62-69` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2149 | MB:2149 | Sur-famille de couvertures < 11 membres, ou multiplicité de paire < 2 − z, pendant la construction du bord ¦ aucune extension du bord partiel ¦ P ¦ `C… | fait |  | énoncé établi (statut de la source) |
| l.2150 | MB:2150 | Coclique 21 dont tout sommet extérieur a ≤ 4 voisins ¦ elle se prolonge en 22 ¦ P ¦ `DEF:12-13`, `DEF:126-171` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2151 | MB:2151 | Coclique 21 maximale ¦ 2 ≤ e ≤ 6 sommets à 5 voisins ; profils (a,e) ∈ {(0,2),(0,3),(0,4),(0,5),(0,6),(1,2),(1,3)} ¦ P ¦ `DEF:173-204` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2152 | MB:2152 | Grille 3×3 R et coclique 21 maximale ¦ t = ¦C∩R¦ ∈ {1, 2, 3} ; t = 3 force (0,6) et C6 ¦ P ¦ `DEF:1660-1674` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2153 | MB:2153 | Profil (0,2) ¦ son C4 H n'est dans aucune grille ; 182 coupes (41) ¦ P ¦ `DEF:1676-1749` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2154 | MB:2154 | W_E inversible (bord avec blocs diagonaux du défaut nuls) ¦ G = 0 : le graphe est certifié ¦ P ¦ `DEF:2380-2383` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2155 | MB:2155 | Une colonne entière du défaut mixte, vecteur propre de B pour 0 ou −1 ¦ colonne nulle ; E coclique ou clique ⇒ système fermé ¦ P ¦ `DEF:2609-2634` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2156 | MB:2156 | Bord avec voisinage complet, D binaire, ker D = 0 ¦ complétion C1 ssi E = (DᵗD)⁻¹Dᵗ[2J − (B+I)D] est entière ¦ P ¦ `DEF:1340-1343` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2157 | MB:2157 | δ = dim V_D = 0 (resp. 1, δ) ¦ ≤ 1 (resp. 2, 2^δ) complétion(s) ¦ P ¦ `DEF:1541-1545` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2158 | MB:2158 | Bord 43 positif (3I − B + J/9 > 0) ¦ ≤ 8192 signes, ≤ 2 complétions étiquetées isomorphes ; > 2 choix ⇒ co-Heawood disjoint du bord et deux cocliques … | fait |  | énoncé établi (statut de la source) |
| l.2159 | MB:2159 | Bord 44 positif ¦ complétion unique ¦ P ¦ `AG:1478` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2160 | MB:2160 | Bord B, D avec h = dim ker[D; 1ᵗ] ≤ 2 ¦ unicité à isomorphisme près (étiquetée si colonnes distinctes) ¦ P ¦ `AG:1502-1503` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2161 | MB:2161 | Moins de complétions étiquetées que ¦Aut(bord)¦ ¦ aucune complétion asymétrique (exclut C1 pour ce bord si le bord est inévitable) ¦ P (critère) / O… | ouverte | R1-16 | bord inévitable manquant |
| l.2162 | MB:2162 | Borne universelle rang(F) ≥ 12 pour les blocs NG ¦ contredit rang(F) ≤ 11 forcé par Conway (c_min ≤ 4) ¦ O ¦ `AG:326-340` ¦ | ouverte | R1-07 | rang F ≥ 12 |
| l.2163 | MB:2163 | Conway + c_min ≤ 4 + D9 ¦ rang Z ≤ c_min − 2 (c1 impossible, c2 Z ≠ 0, c3 rang ≥ 2, c4 rang ≥ 3) ¦ P (conditionnel) ¦ `AG:319-320` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2164 | MB:2164 | (NG7) : aucun bloc non-grille avec min t ≤ 7 ne passe les conditions de Conway ¦ pas de Conway (≥ 254 tels blocs forcés) ¦ O ; implication P ¦ `AG:835… | ouverte | R1-07 | NG7 |
| l.2165 | MB:2165 | NG5 ¦ NG7 ¦ P ¦ `AG:842-844` ¦ | chaîne | R1-07 | NG5 ⇒ NG7 |
| l.2166 | MB:2166 | Bornes de Schur 9, 10, 11, 12 pour c_l = 1..4 ¦ nu ≥ 14 exclu ¦ P (réduction) ¦ `AG:787-790` ¦ | chaîne | R1-07 | bornes de Schur ouvertes |
| l.2167 | MB:2167 | Ancien bloc grille nu14 → non-grille par interpolation PSD ¦ perte d'au moins 1 nullité dans le segment ¦ P ¦ `AG:815-817` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2168 | MB:2168 | Structure à cinq étoiles invariante par h ¦ impossible ; toute structure : ≥ 4 des 8 lignes cassent h ¦ P ¦ `AG:529-546` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2169 | MB:2169 | Tout bloc de la famille G1 c55 non grille ¦ rang_F7 ≥ 29 > 28 : aucun prolongement Conway ¦ E ¦ `AG:1337-1353` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2170 | MB:2170 | Tout bloc ⟨z, hM⟩ de nullité 14 ¦ rang_F7 ≥ 29 : aucun prolongement ¦ C ¦ `AG:1049-1081` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2171 | MB:2171 | Remplacer seulement P par P′ en gardant T PSD ¦ P′v = −v sur W ¦ P ¦ `AG:652-659` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2172 | MB:2172 | B_S q = 0 pour q ∈ ker T_SS (recollement de blocs) ¦ Γ_RS q = 0 ¦ P ¦ `AG:670-673` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2173 | MB:2173 | Γ binaire, C1 exacts, T et U PSD (84 labels) ¦ srg(99) (tous les C2) ¦ P ¦ `AG:364-377` ¦ | fait |  | énoncé établi (statut de la source) |
| l.2174 | MB:2174 | A entière symétrique, A1 = 14·1, G₋(A), G₊(A) ⪰ 0 ¦ srg(99,14,1,2) ¦ P ¦ `DEF:1922-1932` ¦ | fait |  | énoncé établi (statut de la source) |

### A.16 L08 (exploration C1) — 78 conditionnels

Répartition : fait 49 ; ouverte 24 ; chaîne 3 ; critère 2.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| l.2290 | MB:2290 | [P] R8 UNSAT ⇒ pas de Conway. Le modèle est audité sain ; le problème à cinq étoiles, plus fort, suffit aussi [L08-020, L08-210] — EXP:16-17 ; R8:24-2… | ouverte | R1-09 | R8 |
| l.2291 | MB:2291 | [P] Q7 ⇒ pas de Conway, via P ≤ 852 et une paire sans grille avec c_min ≤ 4 ; Q7 ⟸ ODDCONST + SYM6 [L08-024, L08-025] — EXP:128-130, 148. | ouverte | R1-07 | Q7 ⟸ ODDCONST + SYM6 |
| l.2292 | MB:2292 | [P] Pour c ≤ 4, paires sans grille, côté c minimal : ODD-PURE + rank Z ≥ c − 1 + P ≤ 852 ⇒ pas de Conway. ODD-PURE seul exclut c = 1 [L08-027, L08-032… | ouverte | R1-07 | ODD-PURE + rang Z |
| l.2293 | MB:2293 | [P] R7-NG (« tout bloc PSD sans grille a rang_F7 ≥ 29 ») ⇒ pas de Conway [L08-029] — EXP:242. | ouverte | R1-10 | R7-NG |
| l.2294 | MB:2294 | [P] H46-c1 ⇒ aucune droite c = 1 ; H46-c1 ⟸ ODDCONST [L08-033] — EXP:363-364, 402. | ouverte |  | H46-c1 |
| l.2295 | MB:2295 | [P] (a ≤ 1) ∧ (b ≥ 1) ⇒ aucune droite c = 1 [L08-034] — EXP:411. | ouverte |  |  |
| l.2296 | MB:2296 | [O] (SV1) ⇒ aucune droite c = 1 [L08-042] — EXP:549-551. | ouverte |  | (SV1) |
| l.2297 | MB:2297 | [P] Une réponse « non » à (Q) ⇒ aucune droite c = 1 — PRM:287-288. | ouverte |  | (Q) |
| l.2298 | MB:2298 | [P] « c(l) = 1 ⇒ rang_F₃(A_Ω) ≥ 46 » exclurait c = 1, puisque Conway impose rang_F₃(A_Ω) ≤ 45 [L08-047] — EXP:646-647. | ouverte |  | rang₃ ≥ 46 |
| l.2299 | MB:2299 | [P] (B′) + [m ≥ 2 exclu] ⇒ pas de Conway [L08-168] — FUS:255. | ouverte | R1-14 | (B′) et m ≥ 2 |
| l.2300 | MB:2300 | [O] Pari 5 + N9-NG complet + P ≤ 852 ⇒ contradiction [L08-023] — EXP:101-103. | ouverte | R1-07 | Pari 5 |
| l.2301 | MB:2301 | [P, rappel] Ponts de la synthèse, statuts d'origine en L07 [L08-235] — SYN:231-246 : | critère |  | rappel |
| l.2302 | MB:2302 | (H-MATCH) ⇒ pas de Conway (relu par un agent adverse, modulo L8) ; | ouverte | R1-08 |  |
| l.2303 | MB:2303 | (N9-NG)/NG5 + P ≤ 852 ⇒ pas de Conway (vérifié par Codex) ; | ouverte | R1-07 |  |
| l.2304 | MB:2304 | (T8) ou (T15) + P ≤ 852 ⇒ pas de Conway. | ouverte | R1-06 |  |
| l.2305 | MB:2305 | [O] (S3) « tout srg à λ = 1 a un automorphisme d'ordre 3 » + C3 exclu ⇒ pas de Conway [L08-154] — TRES:35-37. | ouverte | R1-24 | (S3) |
| l.2306 | MB:2306 | [P, rappel] Le cadre des cocliques fermerait C1 avec α ≥ 21 — SYN:307. | ouverte | R1-17 | α ≥ 21 |
| l.2307 | MB:2307 | [H] DISC-35 tuerait Conway [L08-021] — EXP:36-37. | ouverte |  | H |
| l.2310 | MB:2310 | [P] (H₃₇) ⇒ r ≠ 37 (Théorème 6.1, sous P ≤ 852 seulement) [L08-187] — THM:822-845. Forme c ≤ 4 (Corollaire 6.2) — THM:841-845. | ouverte | R1-11 | (H₃₇) |
| l.2311 | MB:2311 | [P] Core37 pour tout G admissible avec (τ¦7) = −1 ⇒ maillon 1 uniforme. Avec les maillons 2, 3, 5 et P3 ⇒ r ≠ 37 (version du 19-20/10, remplacée par l… | ouverte | R1-11 | Core37 (remplacé par Th. 6.1) |
| l.2312 | MB:2312 | [O] « Tout bloc à quatre étoiles de rang réel 30 a un 7-rang ≥ 25 » ⇒ r ∈ {41, 43} (37 et 39 exclus) [L08-207] — BORNE:414-415. | ouverte | R1-10 | 7-rang ≥ 25 |
| l.2313 | MB:2313 | [P] (K22) « ν ≥ 14 ⇒ rang_F7(8T_S) ≥ 23 » exclurait r = 37. Pour les paires à droite c = 1 générique, (K22) équivaut à l'échec de la double étoile [L0… | ouverte | R1-10 | K22 |
| l.2314 | MB:2314 | [P] Le lemme P2 restreint et une normalisation couvrante qui fournit une droite où il s'applique ⇒ exclusion du rang 37 [L08-145] — MAND:367, 404-407. | ouverte |  | P2 restreint |
| l.2315 | MB:2315 | [P cond.] N14 (aucun vecteur de norme 14 au rang 37, calcul non audité) ⇒ le cas I de c = 1 est vide au rang 37 [L08-041] — EXP:517-519. | fait | R1-12 | conditionnel à N14 (E) |
| l.2316 | MB:2316 | [P] Pour une droite générique : r = 37 ⟺ Π_T 7-entier ⟺ D n'a aucun mot non nul porté par le lointain (une seule droite suffit) [L08-170, L08-198] — O… | fait |  | équivalence (P) |
| l.2317 | MB:2317 | [P] r ≤ 45 − m ⟺ il existe m vecteurs de E₋ dont la Gram est inversible mod 7 ; de même r ≤ 55 − m′ côté E₃ [L08-202] — BORNE:231-236. | fait |  | P |
| l.2318 | MB:2318 | [P] Monotonie (Théorème B, B3) : (ii) au rang r ⇒ (ii) au rang r′ > r. Un test au rang 43 est une relaxation valable pour toute la fenêtre [L08-218] —… | fait |  | P (monotonie) |
| l.2319 | MB:2319 | [H] Critère de décision : si l'estimation de Knuth dépasse ≈ 10¹² nœuds par droite au rang 41, la route droite par droite est close aux rangs 41 et 43… | critère |  | H |
| l.2322 | MB:2322 | [P] Dichotomie (I)/(II) [L08-057] — PLAN:20-23 : | fait | R1-14 | dichotomie |
| l.2323 | MB:2323 | si au plus 32 droites ont c ≤ 2, il existe une racine dont les 7 droites ont c ≥ 3 ; | fait | R1-14 |  |
| l.2324 | MB:2324 | sinon, au moins 33 droites c ≤ 2 couvrent tous les sommets. | fait | R1-14 |  |
| l.2325 | MB:2325 | [S] c_min = 4 exclu ⇒ c_min ≤ 3 [L08-070] — PLAN:29. | fait | R1-14 | S |
| l.2326 | MB:2326 | [P] Proposition 3 [L08-142] — MAND:83-90 : | chaîne | R1-14 | registre c = 3 ouvert |
| l.2327 | MB:2327 | registre c = 3 fermé ⇒ m = 3 global exclu ; | chaîne | R1-14 |  |
| l.2328 | MB:2328 | pour la branche (I), il faut en plus traiter les gabarits à plus de 12 grilles et des méthodes sans le budget s ≤ 51. | chaîne | R1-14 |  |
| l.2329 | MB:2329 | [O] « Aucune droite dans six grilles » ⇒ tue 9302, 9791, 9912, 9966, 10003, 10006 et 10025, et supprime c = 6 de toutes les branches [L08-138, L08-141… | ouverte |  | « aucune droite dans six grilles » |
| l.2330 | MB:2330 | [C+P] 3P + 4G ≤ 2772 ⇒ 9s + 8g ≤ 504 au sommet de score minimal. Sous c ≥ 4 global : g ≥ 7, s ≤ 49, et le gabarit c4 n° 7 est exclu. Ce choix de racin… | fait |  | énoncé établi (statut de la source) |
| l.2331 | MB:2331 | [P] P ≤ 852 ⇒ budget τ(v) ≤ 51 et k ≤ 12 à la racine de budget [L08-066] — AUD:132-136. | fait |  | énoncé établi (statut de la source) |
| l.2332 | MB:2332 | [E, sous E3] Règle C4 + C3 : si le graphe des grilles contient C4(X) + C3(Y), les deux diagonales du C4 sont des grilles [L08-104] — HUIT:232-250. | fait |  | énoncé établi (statut de la source) |
| l.2333 | MB:2333 | [E, sous E3] Familles exclues, chacune avec ses hypothèses exactes : | fait |  | énoncé établi (statut de la source) |
| l.2334 | MB:2334 | T23 [L08-105] — PART:5-12 ; | fait |  | énoncé établi (statut de la source) |
| l.2335 | MB:2335 | K3U [L08-108] — CH/k3u_closed.json:1 ; | fait |  | énoncé établi (statut de la source) |
| l.2336 | MB:2336 | 2K2 [L08-109] — CH/k2k2_closed.json:2 ; | fait |  | énoncé établi (statut de la source) |
| l.2337 | MB:2337 | P3NB [L08-115] — CH/p3nb_closed.json:2 ; | fait |  | énoncé établi (statut de la source) |
| l.2338 | MB:2338 | K2BC [L08-116] — CH/k2bc_closed.json:2 ; | fait |  | énoncé établi (statut de la source) |
| l.2339 | MB:2339 | 2K2N + B/C [L08-113] — CH/k2k2n_bc_closed.json:2. | fait |  | énoncé établi (statut de la source) |
| l.2340 | MB:2340 | [H, Codex] Si K3 et 2K2 sont fermées, alors les grilles sur les 4 autres droites forment une étoile [L08-118] — RAP:56-57. | ouverte |  | H |
| l.2341 | MB:2341 | [P] Un cycle impair de blocs-paires dans Ĵ ⇒ H = 0, donc des grilles, donc une contradiction [L08-089] — MORTS:76-78. | fait |  | énoncé établi (statut de la source) |
| l.2342 | MB:2342 | [P] FG : sans marche fermée alternée de Ĵ par un rectangle non grille q, le gabarit est impossible [L08-085] — LEM:42-55. | fait |  | énoncé établi (statut de la source) |
| l.2343 | MB:2343 | [P] R1 : si aucune ligne n'a h(q) ≥ 1, alors R_qq = 0 < 4 : contradiction [L08-087] — LEM:169. | fait |  | énoncé établi (statut de la source) |
| l.2344 | MB:2344 | [P, Codex] Lemme du carré de défaut. Si deux rectangles de T sont des grilles et que H_F = H_D pour un D disjoint de F, le gabarit est impossible [L08… | fait |  | énoncé établi (statut de la source) |
| l.2345 | MB:2345 | [C] gz 9748 : si les comptes imposent 9S01 + 9S23 + 2S45 ≥ 484, on contredit S_F ≤ 24 [L08-092] — C9748:8-14. | fait |  | énoncé établi (statut de la source) |
| l.2346 | MB:2346 | [P] Lemme de moyenne. Si la moyenne Γ̄ sur le groupe d'ordre 128 vérifie T, U ⪰ 0, aucune combinaison de coupes de positivité et d'inégalités linéaire… | fait |  | lemme de moyenne |
| l.2347 | MB:2347 | [P] Une paire (l, m) en grille donne une composante prisme de G_l, donc une droite avec c(l) = 1 n'est dans aucune grille. (H-MATCH) aux 21 paires de … | fait |  | énoncé établi (statut de la source) |
| l.2348 | MB:2348 | [P] Au rang 37 : 2r(T) + ρ(T) = d − 1. Une droite c = 1 avec d = 2 est équilibrée, avec ρ = 1. Pour c ≥ 3, ρ ≥ 2 [L08-163, L08-189] — FUS:106-122 ; TH… | fait |  | énoncé établi (statut de la source) |
| l.2349 | MB:2349 | [E] Au rang 37, l'obstruction d'étoile demande Green × couplage λ = 1 : sans l'un ou l'autre, pas de mort [L08-171] — OBS:27-33. | fait |  | énoncé établi (statut de la source) |
| l.2352 | MB:2352 | [P] Formes du résidu et énoncés valables pour toute droite ou toute droite générique [L08-190, L08-191, L08-140, L08-198, L08-199, L08-217, L08-218] —… | fait |  | énoncé établi (statut de la source) |
| l.2353 | MB:2353 | encodage du résidu, Proposition 3.5 ; | fait |  | énoncé établi (statut de la source) |
| l.2354 | MB:2354 | forme de Green, Proposition 3.6 ; | fait |  | énoncé établi (statut de la source) |
| l.2355 | MB:2355 | cadre lointain, Théorème 4.3 ; | fait |  | énoncé établi (statut de la source) |
| l.2356 | MB:2356 | Proposition 4 ; | fait |  | énoncé établi (statut de la source) |
| l.2357 | MB:2357 | Théorème 5 ; | fait |  | énoncé établi (statut de la source) |
| l.2358 | MB:2358 | Théorème B. | fait |  | énoncé établi (statut de la source) |
| l.2359 | MB:2359 | [P] Si c(T) = 6, alors 420Π_T est entier, de rang 13 et de diagonale 91 [L08-141] — MAND:303-308. | fait |  | énoncé établi (statut de la source) |
| l.2360 | MB:2360 | [P] Si A et B sont non-grilles disjoints avec H_A = −H_B (sous E3), alors e_A = e_B = 2, R_AA = R_BB = 4, R_AB = −4, et Q_A ∪ Q_B est cubique [L08-102… | fait |  | énoncé établi (statut de la source) |
| l.2361 | MB:2361 | [P] Si H_C = −H_D pour deux non-grilles partageant une droite, alors Q_C ∪ Q_D est C8 ou C4 + C4 [L08-106] — PART:30-48. | fait |  | énoncé établi (statut de la source) |
| l.2362 | MB:2362 | [P] Si H01 = −H02 ≠ 0 et que Q12 est une grille, alors T = Σ F_j [L08-107] — FACT:10-58. | fait |  | énoncé établi (statut de la source) |
| l.2363 | MB:2363 | [P] Une grille Q_bd (d ∉ {a,b,c}) est en couplage parfait avec Q_ac ; deux grilles disjointes sont couplées parfaitement [L08-117, L08-110] — P250:28-… | fait |  | énoncé établi (statut de la source) |
| l.2364 | MB:2364 | [P, Codex] Si H_A + H_B + H_X + H_Y − H_C − H_D = 0, avec X et Y disjoints de C, alors [R_CC = 8 et R_AC + R_BC ≤ −1] ⇒ une forme quadratique de R vau… | fait |  | énoncé établi (statut de la source) |
| l.2365 | MB:2365 | [P, Codex] Sur tout bloc principal S = R[I,I] : h_w[I] ∈ im(S) et h_w[I]ᵀS⁺h_w[I] ≤ 5/2 [L08-121, L08-079] — BLOC:9-17 ; GCOV:123-153. | fait |  | énoncé établi (statut de la source) |
| l.2366 | MB:2366 | [P] Toute grille domine parfaitement les 90 sommets extérieurs ; c'est propre à k = 14 [L08-093, L08-039] — GRAM60:16-21 ; MOM:912-916. | fait |  | énoncé établi (statut de la source) |
| l.2367 | MB:2367 | [P] Si L est dans 6 grilles, Spec B est forcé, avec 13 directions −4 portées par D [L08-094] — GRAM60:59-71. | fait |  | énoncé établi (statut de la source) |
| l.2368 | MB:2368 | [P] Pour toute composante K de G_{l_a} : A[D_a] d^K = −d^K. Cela vaut pour tout srg(v,k,1,2) [L08-088] — LEM:240-244. | fait |  | énoncé établi (statut de la source) |
| l.2369 | MB:2369 | [P] Pour Γ 14-régulier sur 99 sommets : 27I − 9A + J ⪰ 0 et 44I + 11A − 2J ⪰ 0 ⟺ srg(99,14,1,2) [L08-013] — RC/snapshot_20261012T113936Z/bridge/messag… | fait |  | énoncé établi (statut de la source) |
| l.2370 | MB:2370 | [P] Coclique de 21 dont tout sommet extérieur a au plus 4 voisins ⇒ elle se prolonge en une coclique de 22 [L08-008] — RC/coexistence_f738665_20261013… | fait |  | énoncé établi (statut de la source) |
| l.2371 | MB:2371 | [P] Si DDᵀ = 12I + 2J − B − B² est binaire avec un voisinage complet (V6, ou tout bord régulier en V13), alors les complétions sont exactement E = E₀ … | fait |  | énoncé établi (statut de la source) |
| l.2372 | MB:2372 | [P] Un 4-cycle de transport impose H₀ ou H₁ (12 sommets) et l'un de cinq systèmes de bord [L08-003] — CI/antecedents/NOTE_TRANSPORT_C1.md:87-105. | fait |  | énoncé établi (statut de la source) |
| l.2373 | MB:2373 | [P] Il n'existe pas d'extension métrique de ℚ(√−15) qui préserve les 8 triangles de Wagner ou les 12 points du Cube. Cela interdit des constructions d… | fait |  | énoncé établi (statut de la source) |

### A.17 L09 (structures, Astra, coordination) — 249 conditionnels

Répartition : caduque 119 ; fait 91 ; ouverte 24 ; réfutée 6 ; prouvée 3 ; critère 3 ; hors cible 2 ; chaîne 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| L09-COND-001 | MB9:17 | L09-COND-001 ¦ Γ grid-full (τ = mate en tout sommet) ¦ Γ̃ ≅ H(7,3), 99·¦G¦ = 3⁷ : contradiction ; idem tout PQ(2,t,2) grid-full a n = puissance de 3… | fait |  | énoncé établi (statut de la source) |
| L09-COND-002 | MB9:18 | L09-COND-002 ¦ x est un point de Hamming (τ = mate en x) et σ_x ∈ Aut(Γ) ¦ contradiction (L7) ; dans C2 le point fixe de l'involution est tordu ¦ C2 (… | fait |  | énoncé établi (statut de la source) |
| L09-COND-003 | MB9:19 | L09-COND-003 ¦ x est un point de Hamming ¦ contradiction (L8) ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:91-93` ¦ « Pour tout sommet x de srg(9… | fait |  | énoncé établi (statut de la source) |
| L09-COND-004 | MB9:20 | L09-COND-004 ¦ une grille par x manque ¦ au moins deux grilles par x manquent ; g(x) ∈ [0,19] ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:108-10… | fait |  | énoncé établi (statut de la source) |
| L09-COND-005 | MB9:21 | L09-COND-005 ¦ τ_a(c) ≠ c̄ et τ_{c̄}(a) = ā (en x) ¦ au moins une grille G_{[c],m}, m ∉ {[a],[c]}, manque en x (L9') ¦ tous ¦ P ¦ `conway99-c1:main:no… | fait |  | énoncé établi (statut de la source) |
| L09-COND-006 | MB9:22 | L09-COND-006 ¦ τ_a(c) ≠ c̄, τ_c(a) = ā et τ_ā(c̄) = c ¦ au moins une grille G_{[c],m} manque (L9) ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:15… | fait |  | énoncé établi (statut de la source) |
| L09-COND-007 | MB9:23 | L09-COND-007 ¦ g(x) = 19 (ou 20) ¦ contradiction ; donc g(x) ≤ 18 (L10) ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:123-127` ¦ « Aucun sommet n'… | fait |  | énoncé établi (statut de la source) |
| L09-COND-008 | MB9:24 | L09-COND-008 ¦ toutes les torsions en x ne font intervenir que 3 classes ¦ contradiction (L11) ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:115-1… | fait |  | énoncé établi (statut de la source) |
| L09-COND-009 | MB9:25 | L09-COND-009 ¦ τ_a(c) ≠ c̄ (a, c de classes différentes) ¦ τ_c(ā) ≠ a ou ∃ y ∉ [a]∪[c] avec τ_y(c) ≠ c̄ (L12) ; corollaires : une étiquette tordue seu… | fait |  | énoncé établi (statut de la source) |
| L09-COND-010 | MB9:26 | L09-COND-010 ¦ une classe est tordue par exactement une étiquette ¦ contradiction (L13 : ¦Z¦ ≠ 1) ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:… | fait |  | énoncé établi (statut de la source) |
| L09-COND-011 | MB9:27 | L09-COND-011 ¦ exactement deux étiquettes tordent en x avec ¦C¦ = 2 ¦ contradiction (L14, à la main) ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.… | fait |  | énoncé établi (statut de la source) |
| L09-COND-012 | MB9:28 | L09-COND-012 ¦ exactement deux étiquettes tordent en x avec ¦C¦ = 3 ou 4 ¦ UNSAT (L14, SAT sans certificat) ¦ tous ¦ S ¦ `conway99-c1:main:notes/30_… | fait |  | S (L14 ¦C¦ = 3, 4 sans certificat) ; ¦C¦ = 5 non lancé |
| L09-COND-013 | MB9:29 | L09-COND-013 ¦ k = 0 (invariant 7-adique) ¦ s(x) ≡ 0 (mod 7) et e_σ(x) ≡ 14 (mod 49) en tout sommet (L19) — cas vide car k ≥ 2 ¦ tous ¦ P ¦ `conway99-… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-014 | MB9:30 | L09-COND-014 ¦ k = 6 ¦ tous les τ_a échangent leurs classes par paires, P = 0 (L20) ; puis contradiction (L20 bis) ¦ tous ¦ P ¦ `conway99-c1:main:note… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-015 | MB9:31 | L09-COND-015 ¦ P ≥ 1 ¦ k ≥ 8 (L20) ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:263` ¦ « P ≥ 1 ⟹ k ≥ 8 » ¦ | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-016 | MB9:32 | L09-COND-016 ¦ une étiquette non tordue (τ_a = mate) existe ¦ k ≥ 12 (L20) ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:263` ¦ « une étiquette no… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-017 | MB9:33 | L09-COND-017 ¦ k = 8 ¦ contradiction (L20 ter, partie finale par propagation sans certificat) ¦ tous ¦ S ¦ `conway99-c1:main:notes/30_LEMMES.md:271-27… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-018 | MB9:34 | L09-COND-018 ¦ une droite L a G(L) connexe et 7 ∤ τ(G(L)) (d(L) = 1) ¦ k ≥ 22 (L21) ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:287` ¦ « si G(L)… | fait |  | énoncé établi (statut de la source) |
| L09-COND-019 | MB9:35 | L09-COND-019 ¦ k = 30 ¦ contradiction par le genre de Λ₋₄ (L22) ; donc k ≤ 28 ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:301-303` ¦ « À k = 30,… | fait |  | énoncé établi (statut de la source) |
| L09-COND-020 | MB9:36 | L09-COND-020 ¦ une droite générique (d(L)=1) a (τ(G(L)) ¦ 7) = +1 ¦ k ≥ 24 (L23) ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:310-311` ¦ « une d… | fait |  | énoncé établi (statut de la source) |
| L09-COND-021 | MB9:37 | L09-COND-021 ¦ k = 22 ¦ (τ(G(L)) ¦ 7) = −1 pour toute droite générique (L23) ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:311` ¦ « k = 22 impose… | fait |  | énoncé établi (statut de la source) |
| L09-COND-022 | MB9:38 | L09-COND-022 ¦ il existe S ⊆ V avec rang₇ Q_SS ≥ 43, ou = 42 avec partie non dégénérée scindée ¦ pas de Conway (critère de non-existence, L23) ¦ tous … | ouverte |  | critère : aucun S de 7-rang ≥ 43 connu (blocs connus ≤ 39 points) |
| L09-COND-023 | MB9:39 | L09-COND-023 ¦ Γ partitionné en 11 grilles induites à couplages tous anti-isomorphismes ¦ plan projectif d'ordre 10 avec polarité : exclu par Lam (L25… | fait |  | énoncé établi (statut de la source) |
| L09-COND-024 | MB9:40 | L09-COND-024 ¦ Γ partitionné en 11 grilles à couplages tous iso, ou mixte pur ¦ contradiction (7m₃ = 220 ; inégalité β − α/2 ≤ 2) ¦ tous ¦ P ¦ `conway… | fait |  | énoncé établi (statut de la source) |
| L09-COND-025 | MB9:41 | L09-COND-025 ¦ x est un point de Hamming ¦ 18 ≤ k ≤ 26 (L24) — vide depuis L8 ¦ tous ¦ P ¦ `conway99-c1:main:notes/30_LEMMES.md:323-324` ¦ « Dans tous… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-026 | MB9:42 | L09-COND-026 ¦ le contrôle positif BvLS (t = 10) du modèle enraciné donnait UNSAT ¦ tous les résultats UNSAT (L7, L8, L10, L11, L14) seraient invalidé… | ouverte | R1-29 | contrôle positif BvLS jamais exécuté ; L8 a une preuve à la main (notes/105), g ≤ 17 aussi (notes/108) |
| L09-COND-027 | MB9:43 | L09-COND-027 ¦ imposer une seule grille G₀₁ en x (τ libre ailleurs) est UNSAT ¦ Γ est sans grille ¦ tous ¦ O ¦ `conway99-c1:main:LAB_INSTRUCTIONS_C1.m… | ouverte |  | test proposé, jamais lancé |
| L09-COND-028 | MB9:44 | L09-COND-028 ¦ tout PQ(2,t,2) est grid-full (F2-SRG) ¦ pas de Conway (par L1) ; implique aussi l'unicité de BvLS ¦ tous ¦ O ¦ `conway99-c1:main:notes/… | réfutée | R1-18 | forme famille réfutée par les srg(243) non grid-full (L06-130) ; forme 99 ⟺ but |
| L09-COND-029 | MB9:45 | L09-COND-029 ¦ toute géométrie locale tordue exige un plan projectif d'ordre t (F17) ¦ à t = 6 aucune torsion (Bruck–Ryser), donc pas de Conway par L1… | réfutée |  | F17 naïve réfutée (L09-071) ; version « torsion uniforme » ouverte |
| L09-COND-030 | MB9:46 | L09-COND-030 ¦ une réflexion ponctuelle σ_x est forcément un automorphisme (F16) ¦ C1 se ramène à C2 ¦ C1 ¦ O ¦ `conway99-c1:main:notes/10_IDEES_F.md:… | ouverte | R1-24 | F16 ; avec C2 exclu donnerait pas de Conway |
| L09-COND-031 | MB9:47 | L09-COND-031 ¦ dans le Fano tendu, branche « factorisation de Heawood » ¦ P ≥ 24, donc exclue à P = 0 (Astra, dossier 2) ¦ C1 (Fano tendu, P = 0) ¦ E … | fait |  | énoncé établi (statut de la source) |
| L09-COND-032 | MB9:48 | L09-COND-032 ¦ témoin « deux factorisations de Heawood affectées par parité » (Fano tendu) ¦ meurt au niveau paire × bloc par une borne ordonnée (6 > … | fait |  | énoncé établi (statut de la source) |
| L09-COND-033 | MB9:49 | L09-COND-033 ¦ C2 exclu (draft 7, 07/10) et C3 exclu (Lean) et Behbahani–Lam (ordres 7, 11 exclus) ¦ tout srg(99,14,1,2) est asymétrique (C1 = tout le… | prouvée | R1-24 | X = C2, C3, ordres 7, 11 exclus : établis avec statuts mixtes (C2 sans relecteur humain) |
| L09-COND-034 | MB9:50 | L09-COND-034 ¦ chaque sommet a ≥ 4 étiquettes tordues (frontière complétée) — Σ¦W¦ ≥ 792 ¦ il suffirait Σ_{curl₀} g(κ) > −176 pour une contradiction… | caduque | R1-05 | route Hodge dépassée : Σ¦W¦ ≥ 3204 par P ≤ 852 |
| L09-COND-035 | MB9:51 | L09-COND-035 ¦ sur curl₀ le spectre comprimé évite (s', r') (énoncé muté) ¦ P = P_max, grid-full, contradiction pour 99 (L1) ¦ tous ¦ P ¦ `conway99-c1… | ouverte | R1-18 | équivaut à F2-SRG forme 99 (⟺ but) |
| L09-COND-036 | MB9:52 | L09-COND-036 ¦ n₃ ≤ 395 (majoration de la torsion) ¦ contradiction avec la frontière complétée (n₃ ≥ 396) ; a fortiori n₃ ≤ 704 contredit L16 (n₃ ≥ 70… | réfutée | R1-05 | X impossible : P ≤ 852 (C) donne n₃ ≥ 1602, Σ¦W¦ ≥ 3204 ; seuil utile P ≥ 853 |
| L09-COND-037 | MB9:53 | L09-COND-037 ¦ Σ_x¦W(x)¦ ≤ 1409 (équivalent Σ¦W¦ ≤ 1404, P ≥ 1152) ¦ pas de Conway (contradiction avec L16) ¦ tous ¦ P ¦ `conway99-c1:main:notes/8… | réfutée | R1-05 | X impossible : P ≤ 852 (C) donne n₃ ≥ 1602, Σ¦W¦ ≥ 3204 ; seuil utile P ≥ 853 |
| L09-COND-038 | MB9:54 | L09-COND-038 ¦ k ≤ 4 (rank₇(A − 3I) ≤ 19) ¦ pas de Conway (car k ≥ 6, puis k ≥ 10) ¦ tous ¦ P ¦ `conway99-c1:main:notes/97_K_ET_TORSION.md:99-101` ¦ «… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-039 | MB9:55 | L09-COND-039 ¦ k = 10 ¦ aucun τ_a de type (1;2,3) ni (4;2) en aucun sommet (test exact à une étoile) ¦ tous ¦ E ¦ `conway99-c1:main:notes/97_K_ET_TORS… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-040 | MB9:56 | L09-COND-040 ¦ k = 10 ¦ m(e) ∈ {0,2} pour toute arête, ¦W(x)¦ ≥ 56 partout, P pair ≤ 462 (Corollaire C1) ¦ tous ¦ P ¦ `conway99-c1:main:notes/100_SY… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-041 | MB9:57 | L09-COND-041 ¦ k = 10 ¦ chaque droite a d(L) ≥ 13 (Corollaire C2) ; contradiction si d(L) ≤ 12 était prouvé ¦ tous ¦ P ¦ `conway99-c1:main:notes/100_S… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-042 | MB9:58 | L09-COND-042 ¦ k ≤ 20 ¦ toutes les droites sont 7-dégénérées (G(L) non connexe ou 7 ¦ τ(G(L))) ; et d(L) ≥ 3 sur les 231 droites (avec L23) ¦ tous ¦ … | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-043 | MB9:59 | L09-COND-043 ¦ d(L) ≤ 9 pour toute droite (conjecture) ¦ k ≥ 14 (et k = 14 imposerait d = 9 sur les 231 droites) ¦ tous ¦ O ¦ `conway99-c1:main:notes/… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-044 | MB9:60 | L09-COND-044 ¦ le minimum de rang du bloc « deux étoiles » sur toutes les holonomies est ≥ 11 ¦ k ≥ 12 ¦ tous ¦ O ¦ `conway99-c1:main:notes/97_K_ET_TO… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-045 | MB9:61 | L09-COND-045 ¦ le couple (π(L), μ_L) = (0,0) est exclu pour toute droite ¦ P = 0 serait exclu ¦ tous ¦ O ¦ `conway99-c1:main:notes/99_VERROU_BOULES_DE… | ouverte |  | (0,0) faisable au modèle enraciné en une droite : piste négative |
| L09-COND-046 | MB9:62 | L09-COND-046 ¦ une petite valeur de π(L) est impossible pour toute droite ¦ borne inférieure sur P ¦ tous ¦ O ¦ `conway99-c1:main:notes/99_VERROU_BOUL… | ouverte | R1-05 | toute borne inférieure P ≥ 853 suffirait |
| L09-COND-047 | MB9:63 | L09-COND-047 ¦ il existe un sous-graphe induit à 43 sommets de déterminant de Seidel premier à 7 ¦ contradiction avec L22 (pas de Conway) ¦ tous ¦ P ¦… | critère |  | critère Seidel (L23) ; aucun sous-graphe témoin connu |
| L09-COND-048 | MB9:64 | L09-COND-048 ¦ un sous-graphe induit à 42 sommets a un déterminant de Seidel non carré mod 7 ¦ k ≠ 28 ¦ tous ¦ P ¦ `conway99-c1:main:notes/102_FORME_B… | critère |  | critère Seidel (L23) ; aucun sous-graphe témoin connu |
| L09-COND-049 | MB9:65 | L09-COND-049 ¦ un sous-graphe induit à 40 sommets a un déterminant de Seidel carré non nul mod 7 ¦ k ≠ 26 (et ainsi de suite : ¦I¦ = 14+k, caractère… | critère |  | critère Seidel (L23) ; aucun sous-graphe témoin connu |
| L09-COND-050 | MB9:66 | L09-COND-050 ¦ ¦I¦ > 14 + k ¦ det S(Γ[I]) ≡ 0 (mod 7) ¦ tous ¦ P ¦ `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:124` ¦ « Si ¦I¦ > 14 + k, det S… | fait |  | énoncé établi (statut de la source) |
| L09-COND-051 | MB9:67 | L09-COND-051 ¦ k = 22 ¦ R_L = 0 pour toute droite générique : Γ est déterminé mod 7 par une boule générique et les N_w ¦ tous ¦ P ¦ `conway99-c1:main:… | fait |  | énoncé établi (statut de la source) |
| L09-COND-052 | MB9:68 | L09-COND-052 ¦ k = 28 ¦ pour u ∈ Λ₋₄ : 7 ¦ u·u ⟺ u mod 7 ∈ G ; U est un plan anisotrope ¦ tous ¦ P ¦ `conway99-c1:main:notes/102_FORME_BETA_SIGNE.md:… | fait |  | énoncé établi (statut de la source) |
| L09-COND-053 | MB9:69 | L09-COND-053 ¦ F induit 4-régulier à 10 sommets ¦ contradiction (c(F) = −1 < 0, lemme de variance) ¦ tous ¦ P ¦ `conway99-c1:main:notes/94_NUIT_LITTER… | fait |  | énoncé établi (statut de la source) |
| L09-COND-054 | MB9:70 | L09-COND-054 ¦ deux grilles ont exactement une droite commune ¦ aucune arête entre leurs parties propres (c = 0) ¦ tous ¦ P ¦ `conway99-c1:main:notes/… | fait |  | énoncé établi (statut de la source) |
| L09-COND-055 | MB9:71 | L09-COND-055 ¦ une coclique de taille 22 (borne de Hoffman) existe ¦ il existe un 2-(22,4,2) à 77 blocs (chaque sommet extérieur a exactement 4 voisin… | fait |  | énoncé établi (statut de la source) |
| L09-COND-056 | MB9:72 | L09-COND-056 ¦ la conjecture des hexagones de Reimbayev (équivalente à (∗)) est vraie pour 99 ¦ pas de Conway (via Makhnev 1988) ¦ tous ¦ R ¦ `conway9… | réfutée | R1-18 | forme famille réfutée le 07/10 (243 tordu) ; forme 99 ouverte (⟺ but) |
| L09-COND-057 | MB9:73 | L09-COND-057 ¦ involution t de 99 à f = 1 point fixe ¦ a₁ = 14 (t retourne les 7 droites en son point fixe, t = σ_x) ¦ C2 ¦ P ¦ `conway99-c1:main:note… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-058 | MB9:74 | L09-COND-058 ¦ involution t fixant une droite (f = 3) ¦ Σ_w φ_w = 10 retournements (n'exclut pas le cas) ¦ C2 ¦ P ¦ `conway99-c1:main:notes/94_NUIT_LI… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-059 | MB9:75 | L09-COND-059 ¦ chaque Q_R (R paire de classes) est pair (dans une jauge) ¦ L8 démontré (21 nombres pairs de somme 105) ¦ tous (point de Hamming) ¦ P ¦… | caduque |  | L8 démontré autrement (notes/105) |
| L09-COND-060 | MB9:76 | L09-COND-060 ¦ les corrections dues à la torsion (arêtes τ et d'holonomie) dans le comptage mod 2 sur les 105 triplets (i;j,k) d'un sommet sont paires… | ouverte |  | programme mod 2 spéculatif ; même somme impaire pour BvLS |
| L09-COND-061 | MB9:77 | L09-COND-061 ¦ Γ est partitionné en 11 grilles induites à couplages tous anti-isomorphismes ¦ il existe un plan projectif d'ordre 10 : impossible (Lam… | fait |  | énoncé établi (statut de la source) |
| L09-COND-062 | MB9:78 | L09-COND-062 ¦ deux grilles disjointes S, S′ sont reliées par un anti-isomorphisme ¦ w ↦ (voisin dans S, voisin dans S′) est une bijection des 81 autr… | fait |  | énoncé établi (statut de la source) |
| L09-COND-063 | MB9:79 | L09-COND-063 ¦ α(Γ) = 22 (coclique de Hoffman) ¦ le complément induit a spectre 10¹,3³³,(−1)²¹,(−4)²², toute grille coupe la coclique en 2 points ¦ to… | fait |  | énoncé établi (statut de la source) |
| L09-COND-064 | MB9:80 | L09-COND-064 ¦ il existe un ensemble −4-serré avec c ∈ {3,…,6} ¦ il témoigne de U ≠ 0 (défaut de L22) ; à k = 28 contraintes ¦C∩S¦ ≡ 4c mod 7 ¦ tous… | ouverte |  | existence d'un ensemble −4-serré c ∈ {3..6} non établie |
| L09-COND-065 | MB9:81 | L09-COND-065 ¦ k = 28 et C, C′ deux cocliques de Hoffman distinctes ¦ ¦C ∩ C′¦ ∈ {1, 8, 15} ¦ tous ¦ P ¦ `conway99-c1:main:notes/107_ENSEMBLES_SERRE… | fait |  | énoncé établi (statut de la source) |
| L09-COND-066 | MB9:82 | L09-COND-066 ¦ k = 28, C coclique de Hoffman, S c-serré ¦ ¦C ∩ S¦ ≡ 4c (mod 7) ¦ tous ¦ P ¦ `conway99-c1:main:notes/107_ENSEMBLES_SERRES_ET_DEFAUT_L… | fait |  | énoncé établi (statut de la source) |
| L09-COND-067 | MB9:83 | L09-COND-067 ¦ k = 28 ¦ trois ensembles serrés quelconques ont un Gram 3×3 de déterminant ≡ 0 (mod 7) ; le défaut de L22 n'est pas porté par des cocli… | fait |  | énoncé établi (statut de la source) |
| L09-COND-068 | MB9:84 | L09-COND-068 ¦ S serré σ-invariant (involution σ, C2) ¦ S est réunion d'orbites, contient le point fixe ssi c impair ; jamais σS = S^c ¦ C2 ¦ P ¦ `con… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-069 | MB9:85 | L09-COND-069 ¦ l'ensemble 𝒩 des grilles incomplètes en x est non vide et deux à deux sécant (étoile ou triangle) ¦ contradiction (lemme D1) ¦ tous ¦ P… | fait |  | énoncé établi (statut de la source) |
| L09-COND-070 | MB9:86 | L09-COND-070 ¦ 𝒩 = {αy, αδ, δw} (configuration chemin) ¦ contradiction (lemme D2) ; d'où g(x) ≤ 17 ¦ tous ¦ P ¦ `conway99-c1:main:notes/108_DEFAUTS_ET… | fait |  | énoncé établi (statut de la source) |
| L09-COND-071 | MB9:87 | L09-COND-071 ¦ ¦𝒩¦ = 4 ¦ 𝒩 est un 4-cycle de classes ; il reste 20 configurations pour g(x) = 17 (motifs (0,2,0,2) : 8 ; (2,2,2,2) : 12) ¦ tous ¦ E … | fait |  | énoncé établi (statut de la source) |
| L09-COND-072 | MB9:88 | L09-COND-072 ¦ T₀ ≠ ∅ et T₁ ≠ ∅ (classes voisines du 4-cycle 𝒩 toutes deux tordantes) ¦ ¦T₀¦ = ¦T₁¦ = 2 et les ombres sont des échanges (lemme A) … | fait |  | énoncé établi (statut de la source) |
| L09-COND-073 | MB9:89 | L09-COND-073 ¦ T₀ = ∅, T₂ = ∅ et b ∈ T₁ (4-cycle 𝒩) ¦ ¦T₁¦ = ¦T₃¦ (lemme B) ¦ tous ¦ P ¦ `conway99-c1:main:notes/112_VERS_G16_MOTIFS_A_QUATRE_DEFA… | fait |  | énoncé établi (statut de la source) |
| L09-COND-074 | MB9:90 | L09-COND-074 ¦ le graphe de classes commun des deux torsions (L14) a un 2-cycle {c,c′} et les trois doubles de Q₀c s'apparient à Q₁c′ ¦ contradiction … | ouverte |  | appariement des doubles pour m ≥ 4 à prouver |
| L09-COND-075 | MB9:91 | L09-COND-075 ¦ une σ-arête interne à une droite du modèle de Fano ¦ e ≥ 13 : contradiction avec le lemme du triangle ¦ C1 (Fano) ¦ P ¦ `conway99-c1:ma… | fait |  | énoncé établi (statut de la source) |
| L09-COND-076 | MB9:92 | L09-COND-076 ¦ famille triangle tendue (e = 12) ¦ Aq = 3q, T 2-régulier, comptes exacts 1 et 3 ¦ tous ¦ P ¦ `conway99-c1:main:notes/115_LEMME_DU_TRIAN… | fait |  | énoncé établi (statut de la source) |
| L09-COND-077 | MB9:93 | L09-COND-077 ¦ σ_i respecte l'appariement de Fano P_i ¦ contradiction (y a au moins 4 voisins dans son bloc contre 2 exigés) : tout σ_i mélange les bl… | fait |  | énoncé établi (statut de la source) |
| L09-COND-078 | MB9:94 | L09-COND-078 ¦ le système (P2) par types est infaisable pour des données locales (τ,σ) ¦ ces données sont impossibles en tout sommet de tout srg(99,14… | fait |  | énoncé établi (statut de la source) |
| L09-COND-079 | MB9:95 | L09-COND-079 ¦ un sommet est de Fano tendu ¦ les 21 petits systèmes « cellules par bloc » doivent tous être faisables (aucun cas testé ne l'est) ¦ C1 … | ouverte |  | lemme « aucun sommet de Fano tendu » non prouvé (E sur cas testés) |
| L09-COND-080 | MB9:96 | L09-COND-080 ¦ tout sommet de Fano tendu ¦ ⟨rhs_R, Ψ_R⟩ = 0 pour chaque bloc R ¦ C1 (Fano tendu) ¦ P ¦ `conway99-c1:main:notes/118_PAIRE_BLOC_ET_OBSTR… | fait |  | énoncé établi (statut de la source) |
| L09-COND-081 | MB9:97 | L09-COND-081 ¦ un sommet est de Fano tendu ¦ P-Ψ : 84 conditions θ(z_X(y)) + θ(z_Y(y)) = 0 ¦ C1 (Fano tendu) ¦ P ¦ `conway99-c1:main:notes/119_PSI_PAR… | fait |  | énoncé établi (statut de la source) |
| L09-COND-082 | MB9:98 | L09-COND-082 ¦ pour tout σ tendu (F5, KBLDP), au moins une droite a un système F₂ (P-Ψ) incompatible ¦ aucun sommet de Fano tendu ¦ C1 ¦ O ¦ `conway99… | ouverte |  |  |
| L09-COND-083 | MB9:99 | L09-COND-083 ¦ on trouve un sous-réseau V ⊂ K de rang ≥ 30 sur lequel H − 3 est injective mod 7 ¦ k ≥ 30, contradiction avec L22 (pas de Conway) ¦ tou… | ouverte |  |  |
| L09-COND-084 | MB9:100 | L09-COND-084 ¦ la structure « arc-en-ciel » des composantes de K (Astra) est forcée à P = 0 ¦ 3-coloration des étiquettes en x avec c(u) ≠ c(ū) et c(u… | ouverte |  |  |
| L09-COND-085 | MB9:101 | L09-COND-085 ¦ poids(d(L)) = 1 pour une droite d'un sommet de Fano tendu ¦ T(L) contient un triangle : λ = 1 violé ¦ C1 (Fano tendu) ¦ P ¦ `conway99-c… | fait |  | énoncé établi (statut de la source) |
| L09-COND-086 | MB9:102 | L09-COND-086 ¦ toutes les droites d'un sommet de Fano tendu sont tout-CM cycliques ¦ S = {Z : p_Z = 2} est ∅, le complémentaire d'une droite, d'un poi… | fait |  | énoncé établi (statut de la source) |
| L09-COND-087 | MB9:103 | L09-COND-087 ¦ P ≥ 1152 ¦ H ≤ 209 988 (hexagones induits) ; équivalence ¦ tous ¦ P ¦ `conway99-c1:main:notes/123_PORTE_IX_TORSION_MAXIMALE.md:29` ¦ « … | réfutée | R1-05 | X impossible : P ≤ 852 (C) donne n₃ ≥ 1602, Σ¦W¦ ≥ 3204 ; seuil utile P ≥ 853 |
| L09-COND-088 | MB9:104 | L09-COND-088 ¦ pour toute donnée de droite (C, τ_u, τ_ū, σ_U) avec d(L) = 1, il n'existe pas de bijections d'ombre et graphe lointain λ/μ-cohérent ave… | ouverte |  |  |
| L09-COND-089 | MB9:105 | L09-COND-089 ¦ k = 22 ¦ le graphe lointain d'une droite générique est fixé mod 7 par les seules ombres ¦ tous ¦ P ¦ `conway99-c1:main:notes/124_LOINTA… | fait |  | énoncé établi (statut de la source) |
| L09-COND-090 | MB9:106 | L09-COND-090 ¦ P = 0 ¦ S = Σ_L c₄(G(L)) (seconde variable libre d'ordre 7 = nombre total de 4-cycles des 231 graphes de droites) ¦ tous ¦ P ¦ `conway9… | fait |  | énoncé établi (statut de la source) |
| L09-COND-091 | MB9:107 | L09-COND-091 ¦ P = S = 0 ¦ tous les G(L) ont maille ≥ 5 ; profils (4,4,4) et (4,8) exclus ; restent connexe et (6,6) ¦ tous ¦ P ¦ `conway99-c1:main:no… | fait |  | énoncé établi (statut de la source) |
| L09-COND-092 | MB9:108 | L09-COND-092 ¦ k ≤ 20 ¦ toute droite vérifie r₀(L) ≥ 2 + r(L) (au moins deux vecteurs propres mod 7 équilibrés portés par N(L)) ¦ tous ¦ P ¦ `conway99… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-093 | MB9:109 | L09-COND-093 ¦ une droite connexe a une torsion t dont aucune partie n'est équilibrée ¦ k ≥ 22 + t (ex. 7 ¦ τ une fois ⟹ k ≥ 24) ¦ tous ¦ P ¦ `conway… | fait |  | énoncé établi (statut de la source) |
| L09-COND-094 | MB9:110 | L09-COND-094 ¦ P = S = 0 et une droite de profil (6,6) ¦ k ≥ 22 ¦ tous ¦ E ¦ `conway99-c1:main:notes/126_L21_RAFFINE_DROITES_DEGENEREES.md:66-82` ¦ « … | fait |  | énoncé établi (statut de la source) |
| L09-COND-095 | MB9:111 | L09-COND-095 ¦ P = 0 et une droite (4,8) dont la composante à 8 étiquettes ne porte pas de torsion équilibrée ¦ k ≥ 22 ¦ tous ¦ E ¦ `conway99-c1:main:… | fait |  | énoncé établi (statut de la source) |
| L09-COND-096 | MB9:112 | L09-COND-096 ¦ P = 0 et k = 20 ¦ chaque droite est (4,4,4) ou porte une torsion équilibrée ; sans torsion équilibrée « (4,4,4) partout », impossible p… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-097 | MB9:113 | L09-COND-097 ¦ P = 0 et k ≤ 18 ¦ chaque droite porte au moins 3 ou 4 vecteurs de torsion équilibrés ¦ tous ¦ P ¦ `conway99-c1:main:notes/126_L21_RAFFI… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-098 | MB9:114 | L09-COND-098 ¦ k = 22 et une droite connexe sans torsion équilibrée ¦ la droite est générique (donc soumise à l'obstruction de l'étoile d'Astra) ¦ tou… | fait |  | énoncé établi (statut de la source) |
| L09-COND-099 | MB9:115 | L09-COND-099 ¦ P = S = 0, k = 22, (i) aucune torsion équilibrée sur les droites connexes, (ii) obstruction uniforme de l'étoile pour les droites génér… | chaîne | R1-15 | (i), (ii) ouverts ; au rang 37 A#30/A#31 (E) rendent le résidu (6,6) sans objet |
| L09-COND-100 | MB9:116 | L09-COND-100 ¦ hypothèse (NT) (seuls vecteurs équilibrés = différences de composantes) ¦ k ≥ 18 ; k = 18 ⟹ c(L) ≥ 5 partout, P ≥ 924, ¦W(x)¦ ≤ 28, m… | caduque | R1-26 | k = 18 hors fenêtre ; en outre P ≥ 924 contredit P ≤ 852 (C) |
| L09-COND-101 | MB9:117 | L09-COND-101 ¦ (NT) et k = 18 (P quelconque) ¦ contradiction (saturation, notes/128 §3 bis) : k ≥ 20 en général ¦ tous ¦ P ¦ `conway99-c1:main:notes/1… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-102 | MB9:118 | L09-COND-102 ¦ (NT) et P = 0 ¦ k ≥ 22 (programme réduit à k ∈ {22, 24, 26, 28}) ¦ tous ¦ P ¦ `conway99-c1:main:notes/128_RIGIDITE_444.md:81-82` ¦ « À … | caduque |  | k ≥ 22 déjà acquis par la fenêtre |
| L09-COND-103 | MB9:119 | L09-COND-103 ¦ (a′) uniforme (étoile complète impossible pour toute boule générique à k = 22) + (NT) + exclusion de « toute droite non connexe » ¦ k ≠… | ouverte | R1-15 | (a′) uniforme, NT et « toute droite non connexe » ouverts |
| L09-COND-104 | MB9:120 | L09-COND-104 ¦ P = 0 et les 7 droites par x sont (4,4,4) ¦ σ_C(v) = v̄ partout et S(x) = 84 (lemme R) ; deux tels sommets jamais voisins ¦ tous ¦ P ¦ … | fait |  | énoncé établi (statut de la source) |
| L09-COND-105 | MB9:121 | L09-COND-105 ¦ P = 0 et k ≤ 20 ¦ au moins 26 droites portent une torsion 7 équilibrée (inconditionnel) ¦ tous ¦ P ¦ `conway99-c1:main:notes/128_RIGIDI… | caduque |  | valeur de k hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-106 | MB9:122 | L09-COND-106 ¦ involution (C2) : Λ_{T,−4} est 7-isotrope ¦ l'involution meurt (critère équivalent) ¦ C2 ¦ P ¦ `conway99-c1:main:notes/129_Q7_SECTEUR_I… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-107 | MB9:123 | L09-COND-107 ¦ involution (C2), sous « NT impair » (r₀_c = 0), un bloc a dim ker Q_c ≥ 3 ¦ l'involution meurt ; dim ker Q_c ∈ {1,2} force g = 20 ¦ C2 … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-108 | MB9:124 | L09-COND-108 ¦ involution (C2), bloc générique de det Q_c carré ¦ g⁻ = 20 ¦ C2 ¦ P ¦ `conway99-c1:main:notes/129_Q7_SECTEUR_IMPAIR_INVOLUTION.md:71` ¦… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-109 | MB9:125 | L09-COND-109 ¦ involution (C2), g⁻ = 18 ¦ (det Q_c ¦ 7) = −1 pour les blocs génériques ; mineurs d'ordre 19 et 20 nuls, d'ordre 18 nuls ou non carrés… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-110 | MB9:126 | L09-COND-110 ¦ involution (C2), deux blocs pleins c, d forment une paire frère ¦ conditions (a)–(d) sur le bloc croisé Σ ; énoncé candidat : impossibl… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-111 | MB9:127 | L09-COND-111 ¦ involution (C2), Σ = ∅ ¦ au plus un bloc A111111 ¦ C2 ¦ P ¦ `conway99-c1:main:notes/131_ENTRELACEMENT_ALT_ET_RESIDUS_LOINTAINS.md:45-48… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-112 | MB9:128 | L09-COND-112 ¦ involution (C2), g = 16 ¦ chaque bloc dans l'un de 4 régimes ; aucun type (τ, η) à t ≥ 2 n'admet de solution locale : contradiction ¦ C… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-113 | MB9:129 | L09-COND-113 ¦ involution (C2), g = 18 ¦ aucun bloc plein ; tout bloc t = 0 est scindé (det Q_c non carré) et toutes ses lignes lointaines sont rigide… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-114 | MB9:130 | L09-COND-114 ¦ involution (C2), un bloc plein (τ = η) ou une ÉTL t = 0 à det carré ¦ g⁻ = 20 ¦ C2 ¦ P ¦ `conway99-c1:main:notes/133_REGIMES_Q7_ET_U_SI… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-115 | MB9:131 | L09-COND-115 ¦ involution (C2), g⁺ ∉ {14, 16} ¦ g⁺ ≥ 18, k ≥ g⁻ + 4 ≥ 22 ; k = 22 ⟹ g⁻ = g⁺ = 18 (cas doublement rigide) ¦ C2 ¦ P ¦ `conway99-c1:main:… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-116 | MB9:132 | L09-COND-116 ¦ involution (C2), 42 + 2¦Σ¦ − 2n_dis > 28 ¦ un bloc au moins a ≥ 6 pivots ¦ C2 ¦ P ¦ `conway99-c1:main:notes/136_ECHELLE_DES_PIVOTS.md… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-117 | MB9:133 | L09-COND-117 ¦ involution (C2), système local UNSAT sur les 156 types à ≥ 6 pivots ¦ n_dis ≥ ¦Σ¦ + 7 dans toute configuration ; UNSAT sur les 79 typ… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-118 | MB9:134 | L09-COND-118 ¦ involution (C2), toutes les instances I(τ) (3 308 classes ; puis (A) 1 507 types + (B) tout-dis) UNSAT ¦ aucune involution (C2 exclu) ¦… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-119 | MB9:135 | L09-COND-119 ¦ involution (C2), le bloc lourd (argmax lexicographique) est une étoile libre ¦ la configuration est tout-dis : n_dis = 21, Σ = ∅, 7 éto… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-120 | MB9:136 | L09-COND-120 ¦ involution (C2), les 156 enveloppes de la ligne (C) tombent ¦ tout le cas involution tombe, sans types de blocs ¦ C2 ¦ P ¦ `conway99-c1… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-121 | MB9:137 | L09-COND-121 ¦ ligne (C) : une composante D_n de U avec n(n − 1)/2 > h₁ + h₂ − 2 (ou version raffinée) ¦ aucun u n'a de projection spinorielle sur D_n… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-122 | MB9:138 | L09-COND-122 ¦ ligne (C) : U contient un E8 ¦ span(E8) ⊥ N et ⊂ N⊥ (dim 2) : contradiction ¦ C2 ¦ P ¦ `conway99-c1:main:notes/139_LIGNE_C_ENVELOPPES.m… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-123 | MB9:139 | L09-COND-123 ¦ ligne (C) : enveloppe décomposable ¦ exclue (Gram projetée G₁² = 7G₁) ¦ C2 ¦ P ¦ `conway99-c1:main:notes/140_LIGNE_C_PACKING_CONNEXITE.… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-124 | MB9:140 | L09-COND-124 ¦ ligne (C) : Σ_u (r/8 − E(u)) > 24·min(h₁,h₂) − r pour toute famille de 42 vecteurs de norme 3 ¦ l'enveloppe est exclue (packing) ¦ C2 ¦… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-125 | MB9:141 | L09-COND-125 ¦ ligne (C) : enveloppe rigide (Coxeter égaux) ¦ E(x) = h¦x¦², m(x) = 0, B₁ = hits(y₁) ⊔ hits(y₂), chaque y a 4h + 8 hits ¦ C2 ¦ P ¦ `c… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-126 | MB9:142 | L09-COND-126 ¦ famille rigide D₂ₘ ⊃ D_m², un bloc à s = 2 forcé a ¦κ¦ = 3/2 (E₃xF₁, E₁xE₄, E₁=E₄, E₂=E₃ avec ¦O₁∩O₂¦ = 1) ¦ la paire est morte (co… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-127 | MB9:143 | L09-COND-127 ¦ 132 : un bloc à ¦κ¦ = 1 ¦ le bloc meurt (lemme T) ¦ C2 ¦ P ¦ `conway99-c1:main:notes/143_LEMME_PI_FAMILLE_D2M.md:154` ¦ « Donc tout b… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-128 | MB9:144 | L09-COND-128 ¦ rank-17 : min K* ≥ 9/7 est démontré ¦ les 1 272 (V, y-paires) sont tuées (C2 exclu par la route rank-17) ¦ C2 ¦ O ¦ `conway99-c1:main:n… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-129 | MB9:145 | L09-COND-129 ¦ rank-17 : R5 tient (run cut25 à 0 survivant) ¦ les 412 classes à témoin n=5 meurent, il en reste 342 (239 min-6, 83 min-8, 20 min-7) ¦ … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-130 | MB9:146 | L09-COND-130 ¦ rank-17 : R6 ∧ R8 démontrés ¦ les 754 classes ouvertes sont toutes couvertes (C2 exclu) ¦ C2 ¦ O ¦ `conway99-c1:main:notes/151_R6_PROGR… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-131 | MB9:147 | L09-COND-131 ¦ rank-17 : R8 k=2/k=3 prouvés (témoins n=8 en k=1 seulement) ¦ A11E6p:8 passe de 1,2·10¹⁰ à 2,1·10⁶ feuilles (~30 min par classe) ; avec… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-132 | MB9:148 | L09-COND-132 ¦ J1a, J2, J3 : le Gram de support M_U est de rang déficient ¦ chaque autre étiquette Y a une ligne exactement orthogonale au noyau de M_… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-133 | MB9:149 | L09-COND-133 ¦ srg(v,k,λ,μ) à valeurs propres entières, d = r − s impair, v₂(k − θ′) ≥ v₂(v) ¦ m_θ pair et (−1)^{m_θ/2}·det Λ_θ ≡ 1 (mod 4) ; ensemble… | fait |  | énoncé établi (statut de la source) |
| L09-COND-134 | MB9:150 | L09-COND-134 ¦ tout premier divisant n est ≡ 1 (mod 4) et e impair ¦ pas de graphe de type Latin négatif NL_e(n) ¦ famille infinie de srg ¦ P ¦ `conwa… | hors cible |  | autres familles de srg |
| L09-COND-135 | MB9:151 | L09-COND-135 ¦ structure D tout-tordue à circuits simples (Σ = ∅, toutes paires tordues) ¦ aucune involution de ce type (≥ 3 triangles et 2 triangles … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-136 | MB9:152 | L09-COND-136 ¦ les 7 types locaux (0,6) (tier06) sont UNSAT ¦ le cas tout-tordu non simple est couvert ¦ C2 ¦ O ¦ `conway99-structures-lab:master:NOTE… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-137 | MB9:153 | L09-COND-137 ¦ chaîne de trois triangles T₁ – T – T₃ dans la décomposition tout-tordue ¦ décomposition impossible (orbite morte, −4 = 0) ¦ C2 ¦ P ¦ `c… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-138 | MB9:154 | L09-COND-138 ¦ deux triangles disjoints dans une décomposition tout-tordue ¦ impossible ¦ C2 ¦ P ¦ `conway99-structures-lab:master:NOTE_S8_TOUT_TORDU.… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-139 | MB9:155 | L09-COND-139 ¦ configuration de Fano tendu ¦ I_R = 0 pour les 21 blocs (condition nécessaire exacte, sans PL) ¦ C1 (Fano tendu) ¦ P ¦ `conway99-struct… | fait |  | énoncé établi (statut de la source) |
| L09-COND-140 | MB9:156 | L09-COND-140 ¦ branche « factorisation de Heawood » du Fano tendu ¦ P ≥ 24, donc exclue à P = 0 ¦ C1 (torsion maximale) ¦ P ¦ `conway99-structures-lab… | fait |  | énoncé établi (statut de la source) |
| L09-COND-141 | MB9:157 | L09-COND-141 ¦ revêtement de K₇ avec λ = 1, μ ≤ 2 et sans prisme ¦ degré ≥ 5 ; à P = 0, composantes de H de degrés 12, 5 + 7 ou 6 + 6 ¦ C1 (Fano tendu… | fait |  | énoncé établi (statut de la source) |
| L09-COND-142 | MB9:158 | L09-COND-142 ¦ carré dis de profil (2,1) ¦ aucun apex dans T ; un apex intérieur force l'autre à l'extérieur ; 3h ≤ 2n_dis ¦ C2 (dis) ¦ P ¦ `conway99-… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-143 | MB9:159 | L09-COND-143 ¦ R_L (60 × 60 mod 7, rang k − 22) : réponse « non » uniforme à l'existence d'ombres et d'un graphe lointain 8-régulier de rang ≤ 6 ¦ k ≥… | ouverte |  | « non » uniforme sur R_L non établi (= L09-COND-088) |
| L09-COND-144 | MB9:160 | L09-COND-144 ¦ SRG réelle (dossier 5 d'Astra) ¦ MR = 0 automatique (Q² ≡ 0 mod 7) ; k = 24 est un problème de construction complet ¦ C1 (7-adique) ¦ P… | fait |  | énoncé établi (statut de la source) |
| L09-COND-145 | MB9:161 | L09-COND-145 ¦ R = 0 (resp. MR = 0 et rang ≤ 2) dans la boule 7-adique ¦ SRG exacte ; un échange de ≤ 6 ombres force deux prismes ¦ C1 (7-adique) ¦ P … | fait |  | énoncé établi (statut de la source) |
| L09-COND-146 | MB9:162 | L09-COND-146 ¦ k = 24 et τ carré ¦ ¦J_bad¦ ≥ 8 ; par étoile j_a = 0 ou j_a ≥ 2 ¦ C1 (7-adique) ¦ P ¦ `conway99-structures-lab:master:JOURNAL.md:589`… | fait |  | énoncé établi (statut de la source) |
| L09-COND-147 | MB9:163 | L09-COND-147 ¦ P = 0 et un sommet dont les 7 droites sont (4,4,4) ¦ σ_C = mate partout, S(x) = 84 ; deux tels sommets jamais voisins ; « (4,4,4) parto… | fait |  | énoncé établi (statut de la source) |
| L09-COND-148 | MB9:164 | L09-COND-148 ¦ NT (droites connexes) ¦ k ≥ 18 ; à P = 0 : k ∈ {22, 24, 26, 28} ¦ C1 ¦ P ¦ `conway99-structures-lab:master:JOURNAL.md:633-635` ¦ « Sous… | fait |  | sous NT ; partie k < 22 sans objet (fenêtre) |
| L09-COND-149 | MB9:165 | L09-COND-149 ¦ NT, k = 20 et une droite à exactement 3 composantes ¦ ρ(L) = 0, t = 0 : droite construction-complète (machinerie de l'étoile applicable… | caduque |  | k = 20 hors de la fenêtre r ∈ {37,39,41,43} (C/E) : k ∈ {22,…,28} |
| L09-COND-150 | MB9:166 | L09-COND-150 ¦ une droite-bloc générique (involution) ¦ g⁻ ∈ {18, 20} ¦ C2 ¦ P ¦ `conway99-structures-lab:master:JOURNAL.md:697-698` ¦ « Donc g⁻ ∈ {18… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-151 | MB9:167 | L09-COND-151 ¦ g⁻ = 18 ¦ toute droite-bloc générique a le signe local −1 ; (det Q_c ¦ 7) = −1 pour tout bloc générique ¦ C2 ¦ P ¦ `conway99-structure… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-152 | MB9:168 | L09-COND-152 ¦ bloc générique avec det Q_c carré (ex. τ_c = η_c) ; bloc A (τ = ι partout) ; bloc plein ¦ g⁻ = 20 (donc à g⁻ = 18 : ni bloc plein ni ré… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-153 | MB9:169 | L09-COND-153 ¦ involution (cadre de C2) ¦ Λ_{T,−4} (rang 15) 7-isotrope ⟺ l'involution meurt ¦ C2 ¦ P ¦ `conway99-structures-lab:master:JOURNAL.md:717… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-154 | MB9:170 | L09-COND-154 ¦ lemme de Witt général (bloc local) ¦ g ≥ 18 + t − 2r₀ + 2·[boule réduite non scindée] ; d'où g⁻ ≠ 16 et g⁻ ∈ {18, 20} ¦ C2 ¦ P ¦ `conwa… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-155 | MB9:171 | L09-COND-155 ¦ dossier 6 d'Astra (involution) ¦ min Λ₋₄⁻ ≥ 8, det L_T = 2¹²7^{g⁻−7}, Blichfeldt ⟹ g⁻ ≥ 12 ¦ C2 ¦ P ¦ `conway99-structures-lab:master:J… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-156 | MB9:172 | L09-COND-156 ¦ vecteur de norme ≤ 10 dans L_T (Sol) ¦ coefficients ±1, côté positif stable, B 4-régulier ; norme 8 ⟹ cube ou Wagner ; cube ⟹ prisme (e… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-157 | MB9:173 | L09-COND-157 ¦ une involution existe ¦ repère de 51 vecteurs dans l'un des 156 réseaux de Borcherds ; tous les exclure = fin du cas involution ¦ C2 ¦ … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-158 | MB9:174 | L09-COND-158 ¦ (A) types à pivots (système local + β) UNSAT et (B) famille tout-dis exclue ¦ pas d'involution (ligne d'arrivée) ¦ C2 ¦ O ¦ `conway99-s… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-159 | MB9:175 | L09-COND-159 ¦ chaque orbite frère, « un bloc » ou dis ¦ Σ_c(2#piv_c + d_c) = 84 + 4¦Σ¦ ; un bloc a 2#piv + d ≥ 12 ¦ C2 ¦ P ¦ `conway99-structures-l… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-160 | MB9:176 | L09-COND-160 ¦ identité du repère seule (poids fractionnaires) sur une classe O₂₄ ¦ infaisable pour 86/141 classes (certificat entier) ¦ C2 (route C, … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-161 | MB9:177 | L09-COND-161 ¦ toutes les structures « Ψ » réglables (retournements) ¦ le lemme Fano par Ψ seul est caduc (480 réglages satisfont I_R = 0) ¦ C1 (Fano … | fait |  | énoncé établi (statut de la source) |
| L09-COND-162 | MB9:178 | L09-COND-162 ¦ P = 0 et S = 0 ¦ H(x) = 12 936 en tout sommet (automatique) ¦ C1 ¦ P ¦ `conway99-structures-lab:master:JOURNAL.md:426` ¦ « Seul point n… | fait |  | énoncé établi (statut de la source) |
| L09-COND-163 | MB9:179 | L09-COND-163 ¦ argument 7-adique n'utilisant que « 7 ¦ t, 7 ∤ v » et les identités de la famille srg(2m²+1,2m,1,2) ¦ exclut d'un coup 99, 6 273 et 49… | ouverte |  | argument 7-adique de famille : aucun |
| L09-COND-164 | MB9:180 | L09-COND-164 ¦ srg(v, k, 1, 2) avec k ≥ 8 ¦ aucun ensemble de commutation de Godsil–McKay non trivial (pas de nouveau membre par commutation locale) ¦… | fait |  | énoncé établi (statut de la source) |
| L09-COND-165 | MB9:181 | L09-COND-165 ¦ involution : minorant g⁻ ≥ 21 (structure lointaine), ou contradiction propre à g⁻ = 18 et g⁻ = 20 ¦ l'involution meurt ¦ C2 ¦ O ¦ `conw… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-166 | MB9:182 | L09-COND-166 ¦ involution avec g⁻ = 22 ¦ ε⁻ forcé à +1 contre ε⁻ = −1 par la formule : impossible ¦ C2 ¦ P ¦ `conway99-structures-lab:master:NOTE_S27_… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-167 | MB9:183 | L09-COND-167 ¦ g⁻ = 18 et une droite-bloc E de rang 18 ¦ ε⁻ = χ(disc B¦_E) ; donc toute droite-bloc générique a le signe local −1 ; la configuration … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-168 | MB9:184 | L09-COND-168 ¦ g⁻ = 16 ¦ torsion équilibrée dans les 7 blocs (g⁻ = 18 + t_c − 2r₀_c + ρ_c) ¦ C2 ¦ P ¦ `conway99-structures-lab:master:NOTE_S27_INVOLUT… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-169 | MB9:185 | L09-COND-169 ¦ orbite X ⊂ ij pivotant en i (AD), S composante de i dans G_k, Π les blocs portant le digone {i,k} ¦ ¦S¦ ≥ 3 + [j ∈ S] + ¦Π¦ (lemme … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-170 | MB9:186 | L09-COND-170 ¦ orbite lointaine f ancrée en e₁ au bloc plein ¦ f rigide ⟺ son ombre a exactement une étiquette dans chacun des 4 blocs hors de {c, e₁,… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-171 | MB9:187 | L09-COND-171 ¦ bloc plein (τ_c = η_c) ¦ rang X_F = 17 et spec T_FF = 3⁹(−4)⁴(−1)⁵(−2)⁶1⁶ ; Φ(z) ∩ Φ(σz) = ∅ ; D préserve l'étoile ¦ C2 ¦ P ¦ `conway99… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-172 | MB9:188 | L09-COND-172 ¦ digone ancré {p, q} (tout type) ¦ k_Z = 2 − ¦blocs(z) ∩ {p,q}¦ pour toute σ-paire Z ¦ C2 ¦ P ¦ `conway99-structures-lab:master:NOTE_S… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-173 | MB9:189 | L09-COND-173 ¦ apex intérieur A d'un carré dis (U, W) ¦ A est dis, Q_UV = Q_WV = 0, supp B ∩ T = ∅, supp V parmi 5 supports ; au moins ⌈n_dis/3⌉ carré… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-174 | MB9:190 | L09-COND-174 ¦ SRG contenant la boule explicite du dossier 5 (τ ≡ 6) ¦ k ≥ 24 ¦ C1 (une boule) ¦ P ¦ `conway99-structures-lab:master:NOTE_S24_ASTRA_DO… | fait |  | énoncé établi (statut de la source) |
| L09-COND-175 | MB9:191 | L09-COND-175 ¦ (A − 3I)z ≡ 0 mod 7 avec un support ≤ 6 (échange de ≤ 6 ombres) ¦ Az = 3z et le support induit un prisme (deux prismes) ¦ C1 (7-adique)… | fait |  | énoncé établi (statut de la source) |
| L09-COND-176 | MB9:192 | L09-COND-176 ¦ boule formée de trois composantes 4+4+4 ¦ d(L) = 3 et k ≥ 20 (L21) ; exclues à P = S = 0 ¦ C1 ¦ E ¦ `conway99-structures-lab:master:NOT… | fait |  | énoncé établi (statut de la source) |
| L09-COND-177 | MB9:193 | L09-COND-177 ¦ droite au Fano tendu (codage w_Z) ¦ réglage de retournements possible ⟺ système affine en (π_XY, π_XZ, π_YZ) cohérent ¦ C1 (Fano tendu)… | fait |  | énoncé établi (statut de la source) |
| L09-COND-178 | MB9:194 | L09-COND-178 ¦ la piste locale (i)+(ii)+(iii) tue toutes les configurations contenant un bloc non libre ¦ C2 se réduit au cas « tous les blocs sont de… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-179 | MB9:195 | L09-COND-179 ¦ v ∈ N* (réseau N de l'involution, repère serré Σ(v,u_a)² = 7‖v‖²) ¦ ‖v‖² ≥ 8/7 ; tout sur-réseau entier de N a un minimum ≥ 2 ¦ C2 ¦ P … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-180 | MB9:196 | L09-COND-180 ¦ involution (cadre du dossier 6, sans P = 0) ¦ g⁻ ≥ 12 (g⁻ = 8 et 10 exclus par Blichfeldt) ¦ C2 ¦ P ¦ `conway99-structures-lab:master:a… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-181 | MB9:197 | L09-COND-181 ¦ involution à g⁻ < 20 ¦ les générateurs engendrent N, de strict indice dans N_max (à g⁻ = 18 : sous-réseau d'indice 7) ; il faut exclure… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-182 | MB9:198 | L09-COND-182 ¦ rang₇ Gram(L_T) ≤ 1 (au lieu de 22 − g⁻ ∈ {2, 4}) ¦ contradiction avec le genre (involution exclue) ¦ C2 ¦ O ¦ `conway99-structures-lab… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-183 | MB9:199 | L09-COND-183 ¦ vecteur non nul de L_T de norme ≤ 10 (cadre à sept blocs) ¦ coefficients ±1, support biparti 4-régulier ; à norme 8 : cube (⟹ prisme) o… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-184 | MB9:200 | L09-COND-184 ¦ P = 0 et support Wagner de norme 8 ¦ le support utilise les sept blocs (les 25 classes à six blocs exclues) ¦ C2 ¦ C ¦ `conway99-struct… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-185 | MB9:201 | L09-COND-185 ¦ Blichfeldt sur L_T à g⁻ = 12 ¦ un vecteur de norme ≤ 10 existe (cas résiduels : Wagner norme 8, normes 9 et 10) ¦ C2 ¦ P ¦ `conway99-st… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-186 | MB9:202 | L09-COND-186 ¦ à g⁻ = 16 ¦ t_c ≥ 2 et r₀_c ≥ 1 + (t_c + ρ_c)/2 dans CHACUN des 7 blocs ¦ C2 ¦ P ¦ `conway99-structures-lab:master:astra/PROBLEMES_OUVE… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-187 | MB9:203 | L09-COND-187 ¦ g = 18 et bloc de type t = 0 non scindé ¦ impossible (1 448 classes) ¦ C2 ¦ P ¦ `conway99-structures-lab:master:astra/POUR_SOL_G18_G20_… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-188 | MB9:204 | L09-COND-188 ¦ g = 18 et bloc t = 0 scindé ¦ R_c = 0 : Z_ff ≡ 0 pour les 30 orbites lointaines, puis T_ff′ ≡ Z_ff′ (lignes rigides) ¦ C2 ¦ P ¦ `conway… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-189 | MB9:205 | L09-COND-189 ¦ système local UNSAT sur les 79 classes pertinentes à ≥ 6 pivots ¦ la famille « Σ = ∅, tout un bloc » est morte ¦ C2 ¦ O ¦ `conway99-str… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-190 | MB9:206 | L09-COND-190 ¦ système local UNSAT sur les 1 521 classes à pivots ¦ seul « tout dis » survit (toutes les étoiles libres) ¦ C2 ¦ O ¦ `conway99-structur… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-191 | MB9:207 | L09-COND-191 ¦ problème B (bloc plein) a une solution ¦ spec T = 3⁹(−4)⁴(−1)⁵(−2)⁶1⁶ et rang X = 17 ¦ C2 ¦ P ¦ `conway99-structures-lab:master:astra/P… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-192 | MB9:208 | L09-COND-192 ¦ problème A ou B (bloc plein) impossible pour un type (certificat) ¦ tout bloc plein de ce type est exclu dans une involution (et avec l… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-193 | MB9:209 | L09-COND-193 ¦ carré dis contenant une orbite de l'étoile de c ¦ SEC est faux en c (valide en tout bloc si n_dis = 0) ¦ C2 ¦ P ¦ `conway99-structures-… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-194 | MB9:210 | L09-COND-194 ¦ involution σ avec D(U) = U′ pour toute orbite (tout frère) ¦ impossible (Théorème D) ¦ C2 ¦ P ¦ `conway99-structures-lab:master:logs/c2… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-195 | MB9:211 | L09-COND-195 ¦ graphe N des paires non frères à au plus 6 arêtes ¦ exclu (∅, 1 à 5 arêtes, 2C₃, K₂,₃, C₆) ¦ C2 ¦ P ¦ `conway99-structures-lab:master:l… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-196 | MB9:212 | L09-COND-196 ¦ modèle de Fano (21 paires tordues, D = 7 triangles d'un plan de Fano) ¦ impossible (Théorème F) ¦ C2 ¦ P ¦ `conway99-structures-lab:mas… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-197 | MB9:213 | L09-COND-197 ¦ configuration ancrée ¦ impossible (Théorème 24.3 ; Théorème P pour les tournois réguliers) ¦ C2 ¦ P ¦ `conway99-structures-lab:master:l… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-198 | MB9:214 | L09-COND-198 ¦ sommet plat dans une srg(99,14,1,2) ¦ impossible (Théorème D′, cas particulier de L8) ¦ C1 (sans automorphisme) ¦ P ¦ `conway99-structu… | fait |  | énoncé établi (statut de la source) |
| L09-COND-199 | MB9:215 | L09-COND-199 ¦ à k = 28 : un accident 7-adique toujours isotrope (z·z ≡ 0) ; ou les accidents contiennent un sous-espace totalement isotrope de dimens… | ouverte |  | k = 28 : accident toujours isotrope non prouvé |
| L09-COND-200 | MB9:216 | L09-COND-200 ¦ s automorphisme d'ordre 7 d'un srg(99,14,1,2) ¦ contradiction (pas d'automorphisme d'ordre 7) ¦ Aut (ordre 7) ¦ P ¦ `conway99-structure… | fait |  | énoncé établi (statut de la source) |
| L09-COND-201 | MB9:217 | L09-COND-201 ¦ un repère structuré complet (route C) existe dans U unimodulaire de rang 24 ¦ U′ = ℤ⁷ ⊥ V avec V l'un des 9 unimodulaires de rang 17, y… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-202 | MB9:218 | L09-COND-202 ¦ V = ℤ¹⁷ et min U ≥ 2 ¦ au plus 8 types de y-paires (4 si min U ≥ 3) ¦ C2 ¦ P ¦ `conway99-rank17:master:RANK17_HANDOFF.md:196-221` ¦ « T… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-203 | MB9:219 | L09-COND-203 ¦ un vecteur rationnel w ∈ Y⊥ non nul a des produits entiers avec tous les u candidats et ¦w¦² < 8/7 ¦ le nœud ne s'étend pas en repère… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-204 | MB9:220 | L09-COND-204 ¦ S a = −4a avec a entier non nul et ‖a‖² ≤ 7 ¦ contradiction (min N* ≥ 8/7) ¦ C2 ¦ P ¦ `conway99-rank17:master:RANK17_HANDOFF.md:342-362… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-205 | MB9:221 | L09-COND-205 ¦ une classe (V,y) a κ ∈ K* avec n = 7¦κ¦² ≤ 4 ¦ la classe est exclue (R≤4 de Sol) ¦ C2 ¦ P ¦ `conway99-rank17:master:PROOF_OBLIGATION.… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-206 | MB9:222 | L09-COND-206 ¦ R6 et R8 sont démontrés (pas de vecteur propre entier σ-impair de −4 nul sur x ∪ N(x) de type n = 6 ni n = 8) ¦ Théorème C2 (pas d'invo… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-207 | MB9:223 | L09-COND-207 ¦ les axiomes V-libres de N (cible A) sont incohérents ¦ C2 suit directement ¦ C2 ¦ O ¦ `conway99-rank17:master:PROOF_OBLIGATION.md:199` … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-208 | MB9:224 | L09-COND-208 ¦ χ caractéristique de V, y de norme 7, r de norme 2 ⊥ y et χ = y + r ¦ y ne peut être une normale du repère switché (toute l'orbite Aut(… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-209 | MB9:225 | L09-COND-209 ¦ (χ,y₁)² + (χ,y₂)² > 7¦χ¦² − 21 pour un χ caractéristique de V ¦ la classe (V,y₁,y₂) est exclue (test exact avec ¦χ¦² ∈ {1,9}) ¦ C2 … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-210 | MB9:226 | L09-COND-210 ¦ ancre caractéristique Φ (Type 0/II) ¦ ‖Φ‖² ≡ 5 (mod 8) ; une seule classe de deux-graphe (tout-Opp) ; normes 25 et 33 impossibles ¦ C2 … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-211 | MB9:227 | L09-COND-211 ¦ deux entrées de magnitude 3 à norme 37 ¦ leurs racines Opp orientées forment un chemin dirigé (cas disjoint et fourche exclus) ¦ C2 ¦ P… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-212 | MB9:228 | L09-COND-212 ¦ pas de Type 0 et pas de Type II (théorèmes V-libres) + R5 ¦ il ne resterait que 19 classes (+1 ℤ¹⁷) ¦ C2 ¦ O ¦ `conway99-rank17:master:… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-213 | MB9:229 | L09-COND-213 ¦ m* > 21 (resp. m* > 29) pour les Φ caractéristiques ¦ tue 76 classes (resp. 454, tout sauf 69 + ℤ¹⁷) ¦ C2 ¦ O ¦ `conway99-rank17:master… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-214 | MB9:230 | L09-COND-214 ¦ une borne uniforme m* ≥ 37 pour les Φ caractéristiques avec (TP) ¦ ferme 454 classes d'un coup ¦ C2 ¦ O ¦ `conway99-rank17:master:GPT_F… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-215 | MB9:231 | L09-COND-215 ¦ R8 k=2 et k=3 prouvés (puis J2 clos) ¦ A11E6p:8 : 1,2·10¹⁰ → 2,1·10⁶ feuilles (puis 0 squelette) ; les 342 classes non-n5 deviennent de… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-216 | MB9:232 | L09-COND-216 ¦ k = 28 (secteur pair) ¦ det L_β = 2⁸ ; L_β d'indice 16 dans un des 5 unimodulaires de rang 15 ¦ C2 ¦ P ¦ `conway99-rank17:master:evenfr… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-217 | MB9:233 | L09-COND-217 ¦ parallélisme des 231 triangles en 7 classes de 33 respecté par σ (orientations renversées) ¦ ⟨σ, T_i⟩ est un quotient du groupe de Coxe… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-218 | MB9:234 | L09-COND-218 ¦ w réel avec w² ≤ 1 et (w,u_o) ∈ Z pour les 42 u sélectionnés (Γ42 = N) ¦ la projection de w sur N est nulle ; au plus 2 telles directio… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-219 | MB9:235 | L09-COND-219 ¦ l'enveloppe unimodulaire de rang 24 contient D8³ (resp. D11, D12) ¦ aucun repère physique (enveloppe exclue) ¦ C2 (route C) ¦ P ¦ `C:/U… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-220 | MB9:236 | L09-COND-220 ¦ enveloppe D6⁴ avec six blocs fractionnaires dans une même paire de composantes opposées ¦ impossible (racine de projection duale 6/7 < … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-221 | MB9:237 | L09-COND-221 ¦ enveloppe sans racines de norme 2 ¦ 24 ombres orthogonales forcées et code binaire autodual doublement pair [24,12,8] ¦ C2 (route C) ¦ … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L09-COND-222 | MB9:238 | L09-COND-222 ¦ reconstruction BvLS avec la région lointaine d'un triangle + deux prismes libres ¦ seules complétions : BvLS et son jumeau (pas de comp… | hors cible |  | contrôle sur srg(243) |
| L09-COND-223 | MB9:239 | L09-COND-223 ¦ srg(99,14,1,2) avec une coclique de 22 dont le design de voisinages est cyclique sur 22 points ou porte une action régulière d'ordre 21… | fait |  | énoncé établi (statut de la source) |
| L09-COND-224 | MB9:240 | L09-COND-224 ¦ mot binaire de ker₇(A + 4I) de poids 77 ¦ coclique de Hoffman 22 (équivalence) ; poids possibles 0, 63, 77 ¦ C1 ¦ P ¦ `conway99-c1:orig… | fait |  | énoncé établi (statut de la source) |
| L09-COND-225 | MB9:241 | L09-COND-225 ¦ tout Conway éventuel (branche minimum global c(L) ≥ 4 fermée par CP-SAT) ¦ il existe une droite L avec c(L) ≤ 3 ¦ C1 ¦ S ¦ `conway99-c1… | fait | R1-14 | S (CP-SAT, sans certificat portable) |
| L09-COND-226 | MB9:242 | L09-COND-226 ¦ P ≤ 852 ¦ au moins 18 droites t ≤ 7 et au moins 254 blocs non-grille contenant une telle droite ¦ C1 ¦ P ¦ `conway99-c1:origin/main:AGE… | fait |  | énoncé établi (statut de la source) |
| L09-COND-227 | MB9:243 | L09-COND-227 ¦ NG7 : aucun bloc non-grille avec min(t_l, t_m) ≤ 7 ne passe les conditions nécessaires de Conway ¦ pas de Conway (avec P ≤ 852) ¦ C1 ¦ … | ouverte | R1-07 | NG7 |
| L09-COND-228 | MB9:244 | L09-COND-228 ¦ T, U PSD sur les 84 étiquettes avec T + U = 7Π et rang T ≤ 30 ¦ T² = 7T, rang T = 30, rang U = 40, puis l'identité SRG99 ¦ C1 ¦ P ¦ `co… | fait |  | énoncé établi (statut de la source) |
| L09-COND-229 | MB9:245 | L09-COND-229 ¦ famille locale ⟨z,hM⟩ sous C1/C1′/C2 et T/U PSD ¦ null_Q T ≤ 14 ; si nullité 14, rang_F7(8T) ≥ 29 ; avec rang_Q ≤ 30 et rang_F7 ≤ 28 : … | fait |  | énoncé établi (statut de la source) |
| L09-COND-230 | MB9:246 | L09-COND-230 ¦ graphe des grilles C4 ⊔ C3 (sous E3) ¦ K4 ⊔ C3 ¦ C1 (gabarits c3) ¦ P ¦ `conway99-c1:origin/main:AGENTS.md:368-369` ¦ « Generalisation … | fait |  | énoncé établi (statut de la source) |
| L09-COND-231 | MB9:247 | L09-COND-231 ¦ H01 = −H02 ≠ 0 et grilles Q12, Q45, Q46, Q56 (K3U) ¦ famille exclue ¦ C1 ¦ C ¦ `conway99-c1:origin/main:AGENTS.md:151-152` ¦ « Portee :… | fait |  | énoncé établi (statut de la source) |
| L09-COND-232 | MB9:248 | L09-COND-232 ¦ bord43 avec 3I − B + J/9 > 0 (q = 1) ¦ au plus 8 192 affectations de signes puis au plus deux complétions Conway étiquetées, isomorphes… | fait |  | énoncé établi (statut de la source) |
| L09-COND-233 | MB9:249 | L09-COND-233 ¦ rang F ≥ 12 pour une droite l de c minimum ¦ N9-NG (équivalence) ¦ C1 ¦ P ¦ `conway99-c1:origin/main:AGENTS.md:801` ¦ « Pour l de c MIN… | fait |  | énoncé établi (statut de la source) |
| L09-COND-234 | MB9:250 | L09-COND-234 ¦ Γ binaire et q (S20 extérieur) avec Kq = 0 ¦ Tq = 0 impossible ; coupe stricte qᵀTq = 8(49 − e(O ∪ S)) ¦ C1 ¦ P ¦ `conway99-c1:origin/m… | fait |  | énoncé établi (statut de la source) |
| L09-COND-235 | MB9:251 | L09-COND-235 ¦ H01 = −H02 ≠ 0, Q12, Q34, Q56 grilles (famille 2K2), E3 ¦ aucune complétion (famille exclue) ¦ C1 ¦ C ¦ `conway99-c1:origin/main:notes/… | fait |  | énoncé établi (statut de la source) |
| L09-COND-236 | MB9:252 | L09-COND-236 ¦ H01 = −H02 ≠ 0 et Q12 grille ¦ le graphe des grilles sur les quatre autres racines est une étoile (éventuellement vide ou une arête) ¦ … | fait |  | énoncé établi (statut de la source) |
| L09-COND-237 | MB9:253 | L09-COND-237 ¦ P3 : étoile de grilles à au moins deux arêtes (campagne LAB) exclue ¦ avec 2K2 et K3U : plus de deux grilles adjacentes impossibles dan… | ouverte | R1-14 | campagne P3 |
| L09-COND-238 | MB9:254 | L09-COND-238 ¦ t_x(F) − t_x(G) = d > 0 et ¦W¦ < d ¦ x a un voisin hors W portant F sans G (clause nécessaire) ¦ tout srg(v,2r,1,2) ¦ P ¦ `conway99-c… | fait |  | énoncé établi (statut de la source) |
| L09-COND-239 | MB9:255 | L09-COND-239 ¦ Q_ij grille dans Conway (r = 7) ¦ chacun des 40 sommets disjoints de {i,j} a exactement un voisin dans la grille ; les autres sommets t… | fait |  | énoncé établi (statut de la source) |
| L09-COND-240 | MB9:256 | L09-COND-240 ¦ dans tous les profils admissibles e ⟹ f (quotas t_e, t_f) ¦ t_e ≤ t_f ; si t_e = t_f, tout profil contenant f sans e est éliminé ¦ géné… | fait |  | énoncé établi (statut de la source) |
| L09-COND-241 | MB9:257 | L09-COND-241 ¦ famille 2K2N et fermeture 2K2 ¦ E(Q12) ≤ 3 donc E(C) ∈ {28, 32, 36, 40} sur le noyau de 20 sommets ¦ C1 ¦ P ¦ `conway99-c1:origin/main:… | fait |  | énoncé établi (statut de la source) |
| L09-COND-242 | MB9:258 | L09-COND-242 ¦ DISC admet la classe de carré 14 sans utiliser L4 (k pair) ¦ la branche 14 est exclue (tout mineur principal non singulier 30 × 30 de 8… | prouvée | R1-01 | L4 (k pair) + L17 (det K₋₄ = 2²¹·7^k) : classe 2 seule |
| L09-COND-243 | MB9:259 | L09-COND-243 ¦ bloc d'étiquettes I entièrement déterminé ¦ rang₇((8T)_II) ≤ k ≤ 28 ; égalité ⟹ partie non dégénérée hyperbolique ; rejeter rang₇ ≥ 29 … | fait |  | énoncé établi (statut de la source) |
| L09-COND-244 | MB9:260 | L09-COND-244 ¦ toutes les boules (droite générique) meurent au test d'étoile ¦ rang 37 exclu (forme sans droite, NOTE 17.93) ¦ C1 (rang 37) ¦ P ¦ `C:/… | ouverte | R1-11 | toutes les boules : test fini non fait |
| L09-COND-245 | MB9:261 | L09-COND-245 ¦ srg(99,14,1,2) avec spread régulier ¦ le quotient serait srg(33,12,1,6) (multiplicité 44/7) : impossible ¦ C1 ¦ P ¦ `C:/home/researcher/cw/… | fait |  | énoncé établi (statut de la source) |
| L09-COND-246 | MB9:262 | L09-COND-246 ¦ tout UNSAT de la question des profils de cocliques (taille 22, 21 maximales) ¦ seulement « plus grande coclique ≤ 20 », pas de contradi… | fait |  | énoncé établi (statut de la source) |
| L09-COND-247 | MB9:263 | L09-COND-247 ¦ structure admissible à cinq étoiles inexistante ¦ pas de Conway (frontière du 16/10) ¦ C1 ¦ O ¦ `C:/home/researcher/cw/review/BRIEF.md:14-1… | ouverte | R1-09 | cinq étoiles : UNKNOWN |
| L09-COND-248 | MB9:264 | L09-COND-248 ¦ tout bloc PSD à quatre étoiles de nullité ≥ 14 a des couplages h-reliés (H-MATCH) ¦ pas de Conway ¦ C1 ¦ O ¦ `C:/home/researcher/cw/review/… | ouverte | R1-08 | H-MATCH |
| L09-COND-249 | MB9:265 | L09-COND-249 ¦ le « 14 » de DISC provient de la parité de v₇(det) d'un réseau propre ¦ tout bloc à quatre étoiles de classe 14 est exclu « gratuitemen… | prouvée | R1-01 | L4 (k pair) + L17 (det K₋₄ = 2²¹·7^k) : classe 2 seule |

### A.18 L10 (sessions, mémoires) — 49 conditionnels

Répartition : ouverte 29 ; fait 8 ; caduque 5 ; chaîne 2 ; réfutée 2 ; critère 2 ; prouvée 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| COND-L10-01 | MB:2610 | [COND-L10-01] SI (H-MATCH) : tout bloc PSD à quatre étoiles de nullité ≥ 14 a M_1 = h(M_0) et M_3 = h(M_2), ALORS chaque sommet est un point de Hammin… | ouverte | R1-08 | H-MATCH |
| COND-L10-02 | MB:2611 | [COND-L10-02] SI (N9-NG) : tout bloc PSD à quatre étoiles sans grille sur (l,m) a nullité ≤ 9 + min(c(l), c(m)), ALORS (avec P ≤ 852) pas de Conway ¦ … | ouverte | R1-07 | N9-NG |
| COND-L10-03 | MB:2612 | [COND-L10-03] SI NG5 : « non-grille et ν ≥ 14 ⇒ c ≥ 5 », ALORS (avec P ≤ 852) toute droite a g ≥ 4, t ≥ 8, donc P ≥ 924 > 852 : pas de Conway ¦ P ; NG… | ouverte | R1-07 | NG5 |
| COND-L10-04 | MB:2613 | [COND-L10-04] SI l'on exclut les ≥ 254 blocs non-grille à min t ≤ 7 que tout Conway possède (NG7, Codex), ALORS pas de Conway (« assez pour les tuer »… | ouverte | R1-07 | NG7 |
| COND-L10-05 | MB:2614 | [COND-L10-05] SI (SYM) « ker T_S est V4-invariant » ET (QUOT) ν(A++) ≤ 7 + min c, ALORS (N9-NG) ; (SYM) seul donne NG5 quand min c = 1 ¦ P ¦ MEM/n9ng-… | chaîne | R1-07 | SYM, QUOT ouverts |
| COND-L10-06 | MB:2615 | [COND-L10-06] SI ODDCONST ET EVEN′ (dim P0 ≤ 7), ALORS (N9-NG) sans symétrie ¦ P ¦ MEM/n9ng-target-1510.md:34 ; SP/msg_n9ng.txt:4-5 | chaîne | R1-07 | ODDCONST, EVEN′ ouverts |
| COND-L10-07 | MB:2616 | [COND-L10-07] SI (B′) : aucun objet PSD à quatre étoiles de rang ≤ 30 avec c = 1, ALORS toute droite de Conway est spéciale (et ODD9 ⇒ (B′)) ; (B′) se… | ouverte | R1-14 | (B′) |
| COND-L10-08 | MB:2617 | [COND-L10-08] SI (SQ30) (classe de carrés 2·3·5·7^e de tout objet PSD de rang 30) ET (N15) (pas de PSD de nullité ≥ 15), ALORS pas de Conway ¦ conditi… | réfutée |  | (SQ30) artefact ; (N15) ouvert |
| COND-L10-09 | MB:2618 | [COND-L10-09] SI (T8) « pont transversal t ≥ 8 », ALORS P ≥ 924 > 852 : pas de Conway ¦ conditionnel ; (T8) fragile (nullité 13 vue avec t ≤ 7) ¦ MEM/… | ouverte | R1-06 | (T8) |
| COND-L10-10 | MB:2619 | [COND-L10-10] SI Q7 : corank(Q) ≤ 11 − c(l) sur les blocs non-grille, côté min-c, ALORS pas de Conway ¦ P (réduction ; identité de Codex bba12ce) ; Q7… | ouverte | R1-07 | Q7 |
| COND-L10-11 | MB:2620 | [COND-L10-11] SI ODD-PURE (rang D = 9), ALORS Conway exige rang Z ≤ c − 2 ; c = 1 est alors exclu par ODD-PURE seul ¦ P (Codex) ; ODD-PURE O ¦ MEM/exp… | ouverte | R1-07 | ODD-PURE |
| COND-L10-12 | MB:2621 | [COND-L10-12] SI R7-NG « bloc PSD non-grille ⇒ rank_F7 ≥ 29 », ALORS pas de Conway (marge 1 dans les données) ¦ conditionnel ; jugé « non crédible » a… | ouverte | R1-10 | R7-NG |
| COND-L10-13 | MB:2622 | [COND-L10-13] SI H46-c1 : G_l connexe ⇒ λ_2(A_H) < 3 (H de 46 sommets), ALORS c(l) = 1 est exclu ¦ P (Conway force λ_2 = 3) ; H46-c1 O ¦ MEM/explorati… | ouverte |  | H46-c1 |
| COND-L10-14 | MB:2623 | [COND-L10-14] SI 3 ∉ spec Γ_S, ALORS ν(T_S) = nullité(D) et Conway ⇔ D = 0 ; donc SI D ≠ 0 pour tout bloc c = 1, ALORS c = 1 exclu ¦ P (identité exact… | ouverte |  | D ≠ 0 |
| COND-L10-15 | MB:2624 | [COND-L10-15] SI c(l) = 1 sans lemme ⇒ ν ≤ 13, ALORS c = 1 exclu (= (B′)) ¦ O ¦ MEM/c1-line-c1-target-1710.md:11-13 ; SP/codex_transcript_2.txt:87 | ouverte | R1-14 | (B′) |
| COND-L10-16 | MB:2625 | [COND-L10-16] SI R8 (quatre étoiles + les 8 labels {4,t}) est UNSAT, ALORS pas de Conway, à tout rang ¦ P (soundness auditée le 20/10) ; R8 O ¦ SP/com… | ouverte | R1-09 | R8 |
| COND-L10-17 | MB:2626 | [COND-L10-17] SI tout graphe de droite admissible à ≤ 7 triangles transversaux a un sommet proche x hors d'eux dont le système d'étoile est UNSAT dans… | ouverte | R1-11 | (H₃₇) |
| COND-L10-18 | MB:2627 | [COND-L10-18] SI « toute boule de tout type de droite meurt » au rang 37, ALORS rang 37 exclu sans lemme global (chaque type a son test d'étoile) ¦ P … | ouverte | R1-11 |  |
| COND-L10-19 | MB:2628 | [COND-L10-19] SI un lemme force au rang 37 une droite d'un type rare (par exemple dans une grille : 1,4e8 boules), ALORS une couverture par un petit b… | ouverte |  | proposé |
| COND-L10-20 | MB:2629 | [COND-L10-20] SI 27 828 τ_g + 31 976 τ_n + (canaux hors C6) < 17,1 millions, ALORS rang 37 exclu (τ_g < 614 seul, τ_n < 535 seul) ¦ H (LP flottant) ¦ … | ouverte |  | H |
| COND-L10-21 | MB:2630 | [COND-L10-21] SI aucune droite n'est dans 4 ou 6 grilles (g(droite) ≤ 3), ALORS paires de grilles sur une droite ≤ 6ρ, τ ≤ P ≤ 853, budget par paire d… | ouverte |  | H |
| COND-L10-22 | MB:2631 | [COND-L10-22] SI 3 320 240 k18 + 2 716 560 k20 + 740 880 k22 + 226 380 k24 (+ types hors graine) < 15 241 977 (k_n = nombre maximal de vecteurs propre… | caduque |  | route des graines fermée |
| COND-L10-23 | MB:2632 | [COND-L10-23] SI b_4 ≥ 18M, ou b_3 ≥ 300k avec b_4 ≥ 12M, ALORS rang 37 meurt (prouvé : 24 948 et 2,73M) ¦ H (table « what-if ») ¦ MEM/c1-start.md:129… | ouverte |  | H |
| COND-L10-24 | MB:2633 | [COND-L10-24] SI b_2 < 968, ou 2a_8 + 16a_9 + a_13 < 2632, ou b_3 < 6 696 790, ALORS rang 43 exclu ¦ identités de LAP reproduites par Codex ¦ MEM/c1-s… | ouverte | R1-28 | rang 43 |
| COND-L10-25 | MB:2634 | [COND-L10-25] SI aucune 22-coclique n'existe, ALORS a_7 = 0 à tout rang (tout vecteur de Fano contient deux 22-cocliques se coupant en 15 points) ; « … | ouverte | R1-17 | au rang 37 N14 (E) donne déjà a₇ = 0 |
| COND-L10-26 | MB:2635 | [COND-L10-26] SI N16 et N18 sont établis au rang 37 ET au plus 4 vecteurs de norme 20 par graine indépendante (a_10 ≤ 31 680 < 34 418), ALORS rang 37 … | ouverte | R1-12 | N16, N18, c₂₀ |
| COND-L10-27 | MB:2636 | [COND-L10-27] Rangs 37, 39, 41 exigent un vecteur de norme 18 ou 26 ; rang 43 exige norme 18 ou 26, ou ≥ 1316 vecteurs de norme 16 ; donc SI les norme… | ouverte | R1-13 | normes 18/26 ; réserve « 1316 » levée par L05-224 |
| COND-L10-28 | MB:2637 | [COND-L10-28] SI rang 37 et P = 0 et si les profils (4,8), (6,6), (4,4,4) meurent tous, ALORS toute droite est connexe ¦ conditionnel ; (4,8) : 81 380… | ouverte |  | (4,8) : 16 516 boules à torsion |
| COND-L10-29 | MB:2638 | [COND-L10-29] Rang 37 ⇔ la matrice de Seidel J − I − 2A a 7-rang 36 ; rang 37 ⇔ Π_T 7-entier ¦ P (reformulations) ¦ MEM/c1-start.md:532 ; SP/commit_ms… | fait | R1-02 | équivalences (P) |
| COND-L10-30 | MB:2639 | [COND-L10-30] Au plus 32 droites à c ≤ 2 ⇒ il existe une racine dont les 7 droites ont c ≥ 3 ; sinon chaque sommet est sur une droite à c ≤ 2 ¦ P (dic… | fait | R1-14 | dichotomie |
| COND-L10-31 | MB:2640 | [COND-L10-31] P ≤ 852 ⇒ au moins 18 droites avec t ≤ 7 ; t ≤ 7 ⇒ c ≤ 4 et un x utilisable ¦ P ¦ MEM/rank37-finite-route-2010.md:12 ; SP/commit_msg_thm… | fait |  | P |
| COND-L10-32 | MB:2641 | [COND-L10-32] SI c_min ≥ 3, ALORS chaque sommet appartient à au moins une grille (racine sans grille exclue par parité) ¦ P (dossier externe, non relu… | fait |  | P externe, non relu |
| COND-L10-33 | MB:2642 | [COND-L10-33] SI les 3 gabarits R1G (23 Gram) sont fermés, ALORS les racines à exactement une grille (sept droites à c ≥ 3) sont exclues — un lemme de… | ouverte |  | R1G |
| COND-L10-34 | MB:2643 | [COND-L10-34] SI l'on prouve qu'au plus neuf paires de fonctions propres de taille 11 ou 12 peuvent coexister, ALORS C2 est fermé (contradiction avec … | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| COND-L10-35 | MB:2644 | [COND-L10-35] NOT-EX (C2) ⇐ théorème R + forçage modulaire (E ≤ 12) + « aucune fonction propre (−4) σ-impaire entière de somme des carrés 8..12 » ; le… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| COND-L10-36 | MB:2645 | [COND-L10-36] Le cadre des cocliques (22 et 21) ne ferme C1 qu'avec une preuve de α ≥ 21 ¦ P (logique) ¦ MEM/asymmetric-srg-campaign.md:80 ; SP/msg_cq… | critère | R1-17 | logique |
| COND-L10-37 | MB:2646 | [COND-L10-37] SI « tout srg λ = 1 a un automorphisme d'ordre 3 » (conjecture (S3)), ALORS pas de Conway (avec C2, C3) ¦ conditionnel ; aucun mécanisme… | ouverte | R1-24 | (S3) |
| COND-L10-38 | MB:2647 | [COND-L10-38] SI (P) « toute arête est dans un prisme », ALORS au moins 231 prismes à 99, ce qui exclut le profil sans prisme (torsion maximale) ¦ con… | ouverte |  | (P) |
| COND-L10-39 | MB:2648 | [COND-L10-39] SI une pièce FORCÉE dans un Conway a plus de symétries que de complétions, ALORS C1 exclu ; une pièce forcée à complétion unique doit êt… | critère | R1-16 | principe |
| COND-L10-40 | MB:2649 | [COND-L10-40] SI les droites extérieures sont déterminées par les couplages en un sommet, ALORS tout système de couplages d'un Conway est rigide sous … | ouverte |  |  |
| COND-L10-41 | MB:2650 | [COND-L10-41] SI F_x est invariant par un flip (Aut = 1), ALORS F_x a au moins deux complétions ¦ P ¦ SP/note_part3.md:40-41 | fait |  | P |
| COND-L10-42 | MB:2651 | [COND-L10-42] SI à trois étoiles « rang 30 ⇒ grille », ALORS chaque sommet est de Hamming, contradiction (L8) ¦ R (z2b, 14/10) ¦ SP/msgs_1800.txt:3-4,… | réfutée |  | z2b |
| COND-L10-43 | MB:2652 | [COND-L10-43] SI « toute relation à trois étoiles vient des deux étoiles de la droite », ALORS route finie (bases « décomposables », ~4e8 à symétrie p… | ouverte |  |  |
| COND-L10-44 | MB:2653 | [COND-L10-44] Sous un automorphisme non trivial, toute recherche est vouée à l'échec : C2 + C3 (Lean) + C7 (+ Behbahani-Lam) ⇒ un Conway est asymétriq… | prouvée | R1-24 | statuts mixtes (C2 assisté, C3 Lean, C7 manuscrit) |
| COND-L10-45 | MB:2654 | [COND-L10-45] Un étalement régulier n'existe qu'aux ordres 9 et 243 de la famille srg(v,k,1,2) : à 99 il donnerait srg(33,12,1,6) de multiplicité 44/7… | fait |  | P |
| COND-L10-46 | MB:2655 | [COND-L10-46] SI une involution existe, ALORS rank_F2(Γ̄ + Nb Nbᵀ) = 20 avec Γ̄² + Γ̄ = Nb Nbᵀ sur F2 ¦ P (esquisse, Broué) ¦ MEMB/conway99-research-s… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| COND-L10-47 | MB:2656 | [COND-L10-47] SI tous les D-carrés sont « sibling », ALORS contradiction (théorème D, C2) ¦ P (vérifié par Astra) ¦ MEMB/conway99-research-state.md:48… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| COND-L10-48 | MB:2657 | [COND-L10-48] SI 3 ∈ spec(Γ_S) (cas des objets de rang 30), ALORS la formule de la résolvante ne s'applique pas telle quelle ¦ constat ¦ SP/codex_tran… | fait |  | constat |
| COND-L10-49 | MB:2658 | [COND-L10-49] À quatre étoiles, srg(v,k,1,2) force 5k − 16 − g relations au-delà des étoiles : 10 pour Conway, aucune pour les autres paramètres λ = 1… | fait |  | P |

## Annexe B. Table des 129 conditionnels du matériau L11 (seconde passe), par bloc

Colonnes :
- **réf.** : bloc et identifiant du conditionnel dans `MATERIAUX_BRUTS_L11.md` (K… ou C…), sinon « l.N » ;
- **ligne du matériau** : « MB11:N » renvoie à `assemblage/MATERIAUX_BRUTS_L11.md` ;
- **énoncé** : verbatim tronqué à 150 caractères, avec « ¦ » à la place des séparateurs de colonnes d'origine ;
- **état de X**, **lien R1**, **note**, avec les mêmes états que l'annexe A.

Répartition totale : ouverte 74 ; fait 24 ; caduque 11 ; réfutée 9 ; critère 6 ; chaîne 3 ; prouvée 1 ; hors cible 1.

### B.1 L11a (pont, C2 puis rangs de L1, 26/09-07/10) — 26 conditionnels

Répartition : ouverte 13 ; caduque 9 ; prouvée 1 ; critère 1 ; hors cible 1 ; fait 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| L11a K1 | MB11:15 | T20 (+ T16, T18, Théorème R, complétude du producteur et des recherches) ¦ T20 : P + deux programmes, « accepté » par l'utilisateur pour des sessions … | prouvée |  | T20 : P (IA) + deux programmes ; « accepté » pour des sessions IA seules ; C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L11a K2 | MB11:16 | T18 et T20 ; une racine r de U avec (r,y1) = ±2 ¦ P / C ¦ ce y1 ne porte aucun repère, quel que soit y2 (Corollaire Y1) ¦ pont:#62–#64 (L11a-27) | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L11a K3 | MB11:17 | « aucune fonction propre entière (σ-impaire) de norme 22 » (T22) ¦ O (non revendiqué, L02_C2_aws-167) ¦ les paires de 003 d'énergie minimale 11 tomber… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L11a K4 | MB11:18 | un vrai repère n'a pas de h de norme 4 d'empreinte nulle ¦ O (prouvé pour 129 réseaux, audit E pour 25) ¦ noyau rigide complet par preuve ¦ pont:#52 (… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L11a K5 | MB11:19 | le jumeau a strictement plus de racines ¦ P (induction, accepté par Codex) ¦ transfert « twin with strictly more roots » sûr sans identifier le jumeau… | caduque |  | C2 clos par la route C (156/156 ; statut mixte P-IA/C/E/S) |
| L11a K6 | MB11:20 | une configuration de Fano existe (min L = 14) ¦ ouvert par rang ; exclue à r = 37 par N14 (L06-092, E) ¦ rang_7(A − 3I) = 33 + rang(S ¦ ker D_2) ≥ 33 … | ouverte | R1-35 | Fano exclu à r = 37 par N14 (E) ; à r ∈ {39,41,43} rang(S ¦ ker D₂) = r − 33 ∈ {6,8,10} : déjà dans la fiche L11a (§ recombinaison 3) |
| L11a K7 | MB11:21 | deux configurations de Fano distinctes forcent rang_7 ≥ 35 ¦ O (non établi, pont:#149) ¦ r = 33 exclu sans extension (sans objet ensuite) ¦ pont:#145 … | caduque |  | r = 33 hors de la fenêtre r ∈ {37,39,41,43} |
| L11a K8 | MB11:22 | au plus 13 (puis 10, puis 4) vecteurs de norme 16 par graine ¦ P ¦ r = 33 force un Fano, puis a_7 ≥ 14 / 42 / 94 / 66 (cert.) ¦ pont:#143–#150 (L11a-6… | caduque |  | r = 33 hors de la fenêtre r ∈ {37,39,41,43} |
| L11a K9 | MB11:23 | a_9 ≤ 497 122 ; ou ≤ 53 vecteurs de norme 18 par graine indépendante ¦ O (sans objet) ¦ r = 33 exclu ¦ pont:#147, #149 (L11a-68) | caduque |  | r = 33 hors de la fenêtre r ∈ {37,39,41,43} |
| L11a K10 | MB11:24 | un cœur de norme 16 engendre k classes indépendantes de Q_r ¦ O ¦ r ≤ 45 − k dès qu'un tel vecteur existe (k = 4 ⇒ r ≤ 41) ¦ pont:#155 (L11a-74) | ouverte | R1-12 | critère de rang par cœur de norme 16 ; N16 au rang 37 ouvert |
| L11a K11 | MB11:25 | une famille de k vecteurs courts de L1 a un Gram de rang > 45 − r mod 7 ¦ P (critère) ¦ la famille est impossible au rang r ¦ pont:#159 (L11a-74) | critère |  | critère de Gram mod 7 (P) |
| L11a K12 | MB11:26 | 16a_9 + a_13 < 329(7^m + 1) − 2a_8, m = (45 − r)/2 ¦ C (identité) ; X ouvert ¦ le rang r est exclu ¦ pont:#178 (L11a-87) | ouverte | R1-13 | identité C ; aucun majorant de a₉ (norme 18) ni de a₁₃ (norme 26) |
| L11a K13 | MB11:27 | r = 35 : a_9 ≤ 10^6 et a_13 < 4 837 873 ¦ E (PL) ; X ouvert ¦ r = 35 exclu (remplacé : r = 35 exclu plus tard, L05-017) ¦ pont:#178 (L11a-88) | caduque |  | r = 35 hors de la fenêtre r ∈ {37,39,41,43} (L05-017) |
| L11a K14 | MB11:28 | r = 37 : a_9 ≤ 10^4 et a_13 < 757 806 (ou a_10 + a_11 + a_12 < 13 521) ¦ E ; X ouvert ¦ r = 37 exclu ¦ pont:#178 (L11a-88) | ouverte | R1-13 | aucun majorant de a₉ ni de a₁₃ dans le matériau |
| L11a K15 | MB11:29 | r = 39 : a_9 ≤ 1 000 et a_13 < 83 316 ¦ E ; X ouvert ¦ r = 39 exclu ¦ pont:#178 (L11a-88) | ouverte | R1-13 | aucun majorant de a₉ ni de a₁₃ dans le matériau |
| L11a K16 | MB11:30 | r = 41 : a_9 = 0 et a_13 < 11 686 ¦ E ; X ouvert ¦ r = 41 exclu ¦ pont:#178 (L11a-88) | ouverte | R1-13 | aucun majorant de a₉ ni de a₁₃ dans le matériau |
| L11a K17 | MB11:31 | r = 43 : a_9 = 0 et a_13 < 1 870 ¦ E ; X ouvert ¦ r = 43 exclu ¦ pont:#178 (L11a-88) | ouverte | R1-13 | aucun majorant de a₉ ni de a₁₃ dans le matériau |
| L11a K18 | MB11:32 | norme 18 seule à r = 37 : moins de 49 392 vecteurs ; à r = 39 : moins de 7 074 ¦ E ; X ouvert ¦ scénario « norme 18 seule » exclu ; il faut alors ≥ 1 … | ouverte | R1-13 | aucun majorant de a₉ ni de a₁₃ dans le matériau |
| L11a K19 | MB11:33 | vecteur de norme 18 unique par graine indépendante (a_9 ≤ 9 240) ¦ O ¦ r = 37, 39 reportés sur les autres normes ; r = 43 intact ¦ pont:#171 (L11a-82) | ouverte | R1-12 | lemme par graine (a₉ ≤ 9240κ₁₈) ouvert ; repris en L11b K6 |
| L11a K20 | MB11:34 | chaque couche a_8..a_13 < 4,8 M ¦ O ¦ r = 35 exclu (remplacé) ¦ pont:#171 (L11a-82) | caduque |  | r = 35 hors de la fenêtre r ∈ {37,39,41,43} (L05-017) |
| L11a K21 | MB11:35 | b_1 = 0, b_2 ≤ 3 234, b_3 ≤ 32 340 ¦ H, retiré (pont:#142) ¦ r = 39, 41, 43 exclus ¦ pont:#135 (L11a-65) | ouverte | R1-28 | affirmation retirée (pont:#142) ; b₁ = 0 n'est acquis qu'au rang 37 (N14, E) ; aucun majorant de b₂, b₃ |
| L11a K22 | MB11:36 | borne prouvée sur les vecteurs de norme 6 de M (< 10^6 ; < 80 000) ¦ H, retiré ¦ r = 41, 43 (resp. 39) exclus ¦ pont:#136 (L11a-65) | ouverte |  | borne retirée (pont:#136) ; aucune borne prouvée sur la norme 6 de M |
| L11a K23 | MB11:37 | tout cœur de norme ≤ échelle(r) a un seuil de rang > r, pour chaque r impair de la fenêtre ¦ O (seuils norme 16 : 17/15/19/17/15, insuffisants) ¦ C1 e… | ouverte |  | seuils obtenus en norme 16 (17/15/19/17/15) très inférieurs à r : méthode insuffisante |
| L11a K24 | MB11:38 | configuration biplan minimale dans un srg(243) réel ¦ E : absente des deux connus ¦ (si présente) aucun argument uniforme de famille ne tuerait la nor… | hors cible |  | contrôle srg(243) ; X faux sur les deux 243 connus (E) |
| L11a K25 | MB11:39 | un vecteur de norme 22 de L1 \ L avec 33 triangles d'une partition commune ¦ H ¦ coordonnée ternaire, élément de ker(Nᵀ mod 3) ; 198 transversaux ⇒ ve… | ouverte |  | H |
| L11a K26 | MB11:40 | r = 45 ¦ P ¦ impossible (pas de réseau pair unimodulaire de rang 44) ; r impair (Milgram) ¦ pont:#130 (L11a-56) | fait |  | r = 45 impossible (pas de réseau pair unimodulaire de rang 44) ; r impair (Milgram) |

### B.2 L11b (pont, arithmétique de rang, 07-08/10) — 18 conditionnels

Répartition : ouverte 13 ; réfutée 2 ; caduque 1 ; chaîne 1 ; critère 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| L11b K1 | MB11:141 | une exclusion du rang 43 n'utilisant que des entrées monotones (min 14, caps a_7, a_8, minorations b_n, racines orthogonales) ¦ exclusion de TOUS les … | ouverte | R1-28 | aucune exclusion monotone du rang 43 connue |
| L11b K2 | MB11:142 | 2a_8 + 16a_9 + a_13 < 2632, ou b_2 < 914 (seuil relevé à 922 puis 968), ou b_3 < 6 696 790 ¦ rang 43 exclu ¦ O (aucun majorant connu) ¦ E (LAP), formu… | ouverte | R1-28 | reformulation : b₂ est minoré au-dessus du seuil (≥ 968, ou ≥ 1000 selon R2-03, vérif. V1/V2) ; aucun majorant de a₉, a₁₃, b₃ |
| L11b K3 | MB11:143 | b_4 > plafond (15 972 863 ; 15 196 716 à ρ = 126 ; 15 197 980 via Fano à ρ = 126) ou b_4 + (651/34)b_3 > 16 851 675 ¦ rang 37 exclu ¦ O : minoration c… | ouverte | R1-12 | minoration certifiée b₄ ≥ 3 371 634 seulement |
| L11b K4 | MB11:144 | b_4 ≥ 18 M seul ; ou b_3 ≥ 150k et b_4 ≥ 15 M ; 300k et 12 M ; 600k et 6 M ; ou b_3 ≥ 900k ¦ rang 37 exclu (anciens plafonds) ¦ O ¦ E (frontier37) ; c… | caduque |  | anciens plafonds, recoupés exactement par Codex (remplacé par K3) |
| L11b K5 | MB11:145 | a_9 ≤ 20000, a_8 ≤ 866, et un cap ~6·10^5 sur a_13 ¦ rang 37 exclu ¦ O ¦ E (needs37, « et si ») ¦ L11b-13 | ouverte | R1-13 | a₈ ≤ 6930 (note 173) seulement, pas ≤ 866 ; aucun cap sur a₁₃ |
| L11b K6 | MB11:146 | 3 320 240κ_18 + 2 716 560κ_20 + 740 880κ_22 + 226 380κ_24 (+ types sans graine) < 15 241 977, avec les comptes de graines corrigés (a_9 ≤ 9240κ_18, a_… | ouverte | R1-12 | lemmes par graine ouverts |
| L11b K7 | MB11:147 | pas de 22-coclique (ou au plus une) ¦ a_7 = 0 à tout rang, plus de profil C ; au rang 37, plafonds 14 444 540,6 / 15 409 176,2 ¦ O ¦ P (note 165 ; LAP… | ouverte | R1-35 | au rang 37 a₇ = 0 est déjà donné par N14 (E) ; la suite « rang 37 exclu » est invalidée (pont:#257) |
| L11b K8 | MB11:148 | g(l) ≤ 3 pour toute droite (τ_g ≤ 6ρ) ¦ τ_g ≤ 693, ρ ≤ 115 ; budget doublé (~30 300) ; limite sans marge contre 27 818 ¦ O ¦ H (flottant) ¦ L11b-60, L… | ouverte | R1-37 | « aucune droite dans 4 ou 6 grilles » ; au rang 37 K5 de L11c donnerait mieux (ρ = 0) |
| L11b K9 | MB11:149 | 27 828τ_g + 31 976τ_n + (canaux hors C6) < 17,1 M (τ_g < 614 sans hors-grille ; τ_n < 535 sans grille) ¦ rang 37 exclu ¦ O ¦ H (flottant, collection d… | ouverte | R1-37 | H ; sans grille : τ ≤ P ≤ 693 (prouvé) contre τ_n < 535 ; τ ≤ 346 sous K24 (O) |
| L11b K10 | MB11:150 | ρ ≲ 58 sans paire hors grille (via τ_g(ρ) : ρ ≤ 50 → τ_g ≤ 515 ; ρ ≤ 30 → 308) ¦ rang 37 exclu (comptabilité) ¦ O ¦ H ¦ L11b-87 | ouverte | R1-37 | H ; aucune borne ρ ≤ 50 justifiée (L11b-87) |
| L11b K11 | MB11:151 | au rang 37, au plus 10 relations mod 7 indépendantes au-delà des faisceaux ¦ rang 37 exclu ¦ **R** (cible fausse) ¦ — ¦ L11b-88 | réfutée |  | cible fausse (L11b-88) |
| L11b K12 | MB11:152 | sur la collection de Codex, constante totale par paire jumelle < ~13 900 (k = 2) ¦ point de grilles exclu ¦ impossible : plancher certifié 16 496 ¦ H … | réfutée |  | impossible : plancher certifié 16 496 > 13 900 |
| L11b K13 | MB11:153 | un mineur non nul d'ordre 19 (ou 20 augmenté) sur « droite centrale + 18 droites latérales » à P = 0, pour toutes les données d'intersection ¦ contrad… | ouverte | R1-15 | monde P = 0 du rang 37 |
| L11b K14 | MB11:154 | (a') uniforme + NT ¦ à P = S = 0 et k = 22 : toutes les droites (6,6) (note 126 §3 ter) ¦ O, O ¦ P sous hypothèses (Codex) ¦ L11b-96 | chaîne | R1-15 | (a′) uniforme et NT ouverts ; au rang 37, (NT) n'est plus utile pour d = 2 (NOTE_FUSION §4.4) |
| L11b K15 | MB11:155 | un Gram de vecteurs du noyau de rang > 56 − r mod 7, ou de rang 19 à déterminant principal carré au rang 37 ¦ contradiction ¦ — (critère) ¦ P / C ¦ L1… | critère |  | critère de Gram (P/C) |
| L11b K16 | MB11:156 | un majorant de a_13 (norme 26 de L1) de quelques 10^5 ¦ plafond b_4 ≤ 11,0 M ; forcerait C_total ≥ 42,6 M au point de grilles ¦ O ¦ E (sensibilités de… | ouverte | R1-13 | aucun majorant de a₁₃ ; sensibilités à recalculer sur la bonne collection |
| L11b K17 | MB11:157 | un majorant de b_2 au rang 37 (par exemple b_2 ≤ 1000) ¦ plafond coupé via l'identité de LAP ¦ O (Codex : aucun) ¦ C (identité) ¦ L11b-67 | ouverte | R1-28 | aucun majorant de b₂ (Codex) |
| L11b K18 | MB11:158 | « (6,6) partout » et des relations entre h_T engendrées localement à 14 près ¦ contradiction ¦ équivaut à la non-existence (LAB) ¦ — ¦ L11b-96 | ouverte |  | ⟺ but (LAB, pont:#357) |

### B.3 L11c (pont, rang 37, S0, droites génériques, 08-09/10) — 24 conditionnels

Répartition : ouverte 22 ; fait 2.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| L11c K1 | MB11:290 | aucun des 174 noyaux de Makhnev ne se prolonge en srg(99,14,1,2) ¦ C1 exclu, tous rangs, sans généricité, sans P = 0, sans involution ¦ O (couverture … | ouverte | R1-22 | 174 noyaux (Makhnev) ; prolongement ouvert (L05-098) ; ⟺ but par cas |
| L11c K2 | MB11:291 | chaque droite est dans ≥ 5 grilles ¦ contradiction (0 type) ; pour q = 1, 2, 3, 4 il reste 115, 52, 11, 2 types ¦ conditionnel prouvé (C) ; X non étab… | ouverte | R1-43 | dominé : « 4 grilles par droite » donne déjà ρ ≥ 154 > 126 (L11e K15, C) |
| L11c K3 | MB11:292 | (rang 37, droite connexe sans torsion) toute sélection binaire de 60 ombres compatibles de moments K a e(F) ≥ 247 ¦ aucune telle droite ; déjà vrai pa… | ouverte |  | fermé par L23 si τ est un carré non nul ; ouvert pour τ ≡ 3, 5, 6 mod 7 |
| L11c K4 | MB11:293 | (rang 37) toute droite a G(T) connexe ¦ aucune grille au rang 37 ¦ O (maille ≥ 5 ⇒ connexe : E ; énoncé B incomplet) ¦ L11c-054 ; pont:#422 | ouverte | R1-36 | maille ≥ 5 ⇒ connexe (E) ; énoncé général ouvert |
| L11c K5 | MB11:294 | (rang 37) tout profil à composante prisme autre que (1^6) est exclu ¦ g ∈ {0, 6} sur toute droite ; g = 6 force ρ = 231 > 126 ; donc aucune grille ¦ i… | ouverte | R1-37 | masse 1,4e8 boules ; même prouvé, ρ = 0 ne conclut pas seul (NOTE 17.89) |
| L11c K6 | MB11:295 | (rang 37, P = 0, sous-collection z) nombre total de paires en collision des masses 7, 8, 9 < 3,84 M ¦ rang 37 exclu à P = 0, donc « rang 37 ⇒ P > 0 » … | ouverte | R1-38 | certifié 185,2 M, soit 34,6 fois le seuil |
| L11c K7 | MB11:296 | (rang 37, collection x63, k = 2) 27 828 τ_g + 31 976 τ_n + (hors C6) < 17,1 M ; à ρ = 0, coût d'une paire jumelle hors grille < 25 201 ¦ rang 37 exclu… | ouverte | R1-37 | H ; seuil 25 201 (27 142 avec N14) contre 31 976 |
| L11c K8 | MB11:297 | (rang 43, S0) borne < 4979 sur les vecteurs de classe 2, norme 40/9, non arêtes ¦ S0 exclu, puis toute la branche « sans 16..24 » (avec L11c-115) ¦ O … | ouverte | R1-25 | S0 (rang 43) |
| L11c K9 | MB11:298 | (S0) borne uniforme ≤ 2288 sur les configurations P7 indépendant / Q29 ¦ S0 exclu ¦ O ¦ L11c-119 ; pont:#495 | ouverte | R1-25 | S0 (rang 43) |
| L11c K10 | MB11:299 | (S0 sans fantôme) borne < 2001 sur les configurations (P7, N29) ¦ S0 sans fantôme exclu ¦ O ¦ L11c-118 ; pont:#493 | ouverte | R1-25 | S0 (rang 43) |
| L11c K11 | MB11:300 | (S0) la configuration P3/N25 est exclue (n ≥ 11 forcé) ¦ S0 exclu ¦ O : 3271 supports ouverts ¦ L11c-120, L11c-124, L11c-126, L11c-144 | ouverte | R1-25 | S0 (rang 43) |
| L11c K12 | MB11:301 | (rang 43, sans 16..24) une relation force l'isotropie du second moment de la couche 26 ¦ contradiction (169N/11) ¦ O ; non forcée au degré 2 ¦ L11c-11… | ouverte |  | relation non forcée |
| L11c K13 | MB11:302 | les sommes cubiques par classe s'annulent ¦ la branche meurt mod 49 ¦ O ; non forcées ¦ L11c-114 | ouverte |  | relation non forcée |
| L11c K14 | MB11:303 | (rang 43) 10a₈ + 2a₉ + 5a₁₀ + 2a₁₁ + a₁₂ < 328 ¦ aucune racine ¦ P ¦ L11c-115 | ouverte |  | implication P ; X non établi |
| L11c K15 | MB11:304 | (rang 43) aucun objet bas (κ, g_v, u, g_l, c₁, w, s₄₄) ¦ aucun vecteur de norme 14 ou 16, au plus une paire de norme 18 ou 20 ; S0 en possède toujours… | fait |  | E |
| L11c K16 | MB11:305 | (rang 37 ou 39 générique, bloc proche inversible) les données (boule, 60 ombres) ont un automorphisme non trivial ¦ Γ a un automorphisme ; à croiser a… | ouverte | R1-41 | rigidité P (L11c-088 à -090) ; en C1, les données (boule, ombres) d'une droite générique de rang 37 ou 39 sont donc asymétriques |
| L11c K17 | MB11:306 | (rang 37 générique) « la symétrie de (boule, ombres) est forcée » ou « ces données n'existent pas » ¦ droites génériques exclues ¦ O ¦ L11c-093 | ouverte | R1-41 | « symétrie forcée » : aucun mécanisme |
| L11c K18 | MB11:307 | (rang 37, z = 0) les motifs A et B sont interdits au niveau d'une étoile complète ¦ aucune étoile générique à z = 0 ¦ O ¦ L11c-033, L11c-037 | ouverte |  |  |
| L11c K19 | MB11:308 | (rang 37) minoration de j, l'indice de saturation ¦ le filtre de Hermite τ ≥ ⌈51 883 209 j²/4⌉ retire des boules ; il faut j ≳ 230 à 440 pour les τ ob… | ouverte |  |  |
| L11c K20 | MB11:309 | le triangle des centres alternés est exclu ¦ toute réparation d'un ruban six injectif contient deux cordes disjointes ¦ O ¦ L11c-104 | ouverte |  |  |
| L11c K21 | MB11:310 | (rang 37) les mondes des normes 16, 18 et 20 meurent ¦ rang 37 exclu : il force une norme 14, 16, 18 ou 20, et la norme 14 est exclue le 10/10 (L06-09… | ouverte | R1-12 | mondes N16, N18, N20 du rang 37 |
| L11c K22 | MB11:311 | (P = 0) aucun vecteur φ = (2, 1^16) du noyau ¦ le canal moulin-cubique de C8 disparaît ¦ O (359 types) ¦ L11c-068 | ouverte |  | 359 types |
| L11c K23 | MB11:312 | un sommet extérieur a ≥ 3 voisins dans un cubique U ¦ U n'a aucun partenaire moulin ¦ P ¦ L11c-071 | fait |  | P |
| L11c K24 | MB11:313 | (sans grille) un prisme a au plus un jumeau ¦ τ ≤ P/2 (le « 20,2 M » de LAB, calculé sur une mauvaise collection, est retiré) ¦ O ¦ L11c-134, L11c-135 | ouverte | R1-37 | K24 : τ ≤ P/2 ; prouvé seulement τ ≤ P (note 249) |

### B.4 L11d (pont, normes, cocliques, symétrie forcée, 10-14/10) — 19 conditionnels

Répartition : ouverte 6 ; fait 5 ; réfutée 3 ; critère 3 ; chaîne 2.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| L11d C1 | MB11:492 | Si N16 et N18 sont exclus au rang 37 ET si c_20 ≤ 4 (au plus 4 vecteurs orientés de norme 20 par graine indépendante ; c_20 ≤ 6 avec supports indépend… | chaîne | R1-12 | N16@37, N18@37 et c₂₀ ≤ 4 ouverts ; N14 E non audité |
| L11d C2 | MB11:493 | Si aucun vecteur propre entier −4 de norme 18 ni 26 n'existe, les rangs 37, 39, 41 sont exclus ; au rang 43 il faut en plus a_8 < 1316. ¦ Échelle : P … | ouverte | R1-13 | réserve « a₈ < 1316 » levée par L05-224 (P, Codex) ; normes 18 et 26 ouvertes |
| L11d C3 | MB11:494 | Si le monde de norme 20 meurt par la borne de rang réel (25 doubles toujours dépendants, 15 relations exigées sur D + Z), alors a_10 = 0 à tout rang. … | ouverte |  | jamais testé |
| L11d C4 | MB11:495 | Si le plafond 31 976 (paire jumelle non grille, collection (9,0)) baisse de 14 % (≤ 27 684), le coin sans grille du LP de comptage se ferme. ¦ H (LP f… | ouverte | R1-37 | H |
| L11d C5 | MB11:496 | Si les bords de Hoffman (22) ET les sept profils de cocliques de 21 maximales sont exclus, ET si α ≥ 21, alors pas de Conway ; sans α ≥ 21, seulement … | chaîne | R1-17 | α ≥ 21 ouvert ; (0,2) ouvert ; E = P3 ouvert |
| L11d C6 | MB11:497 | Si les onze répartitions de cycles autour d'une arête quelconque (bord de 27 sommets, 72 restants) sont toutes exclues avec attaches générales, alors … | ouverte | R1-33 | ≈ but (découpe par cas d'une arête) ; déjà dans la session externe (L03b-130, -133) |
| L11d C7 | MB11:498 | Fermer (0,2) ferme un des sept profils numériques d'une coclique maximale de 21 (pas C1, ni α = 22, ni α ≤ 20). ¦ Portée (P) ¦ L11d-069 | fait | R1-17 | portée |
| L11d C8 | MB11:499 | H3 + L8 ⇒ pas de Conway. ¦ H3 RÉFUTÉE (L11d-172) ; de plus insuffisant (rang 30 − δ', L07_C1_asym_local-063) ¦ L11d-168 | réfutée |  | H3 réfutée (L11d-172) |
| L11d C9 | MB11:500 | (A) + (C) ⇒ pas de Conway ; (A) ⇒ toutes les droites spéciales ⇒ (B) ; (B) ⇒ route finie (racine en droite spéciale, bases décomposables, filtre de co… | réfutée | R1-36 | (A) réfutée (52 contre-exemples exacts, L07_C1_asym_local-065) ; (B), (C) ouverts |
| L11d C10 | MB11:501 | H3'' (toute relation à trois étoiles est portée par les deux étoiles mates) ⇒ chaque drapeau (v,l) a Q(v,l) non connexe (squelette décomposable partou… | réfutée | R1-36 | forme locale (A) réfutée ; forme propre à Conway sans route |
| L11d C11 | MB11:502 | Si l'instance ENTIÈRE préserve deux flips individuels (poids < ⌈t/2⌉) et si le nombre de complétions est ≤ 2 (régime V15), la branche est exclue pour … | critère | R1-20 | aucune branche exhibée |
| L11d C12 | MB11:503 | Dans un C1, le nombre de complétions de toute pièce H est un multiple de ¦Aut(H)¦ ; une pièce FORCÉE avec plus de symétries que de complétions exclut … | critère | R1-16 | pièce forcée symétrique : O |
| L11d C13 | MB11:504 | L'asymétrie ne devient une exclusion qu'avec une borne SUPÉRIEURE de complétions d'un hôte symétrique inférieure à l'ordre de son groupe. ¦ H (program… | critère | R1-16 | pièce forcée symétrique : O |
| L11d C14 | MB11:505 | Sur un bord 43 positif, ≥ 3 composantes de signes forcés ⇒ un co-Heawood disjoint du bord ⇒ deux cocliques de 22 se coupant en 15. ¦ P ¦ L11d-103 | fait | R1-42 | P (V14/V15, non relus par LAB) |
| L11d C15 | MB11:506 | Si h = dim ker[D;1ᵗ] ≤ 2, toutes les complétions d'un même facteur sont isomorphes par un échange ; si D a ses colonnes distinctes (ou m ≤ 25), la com… | fait | R1-42 | P (V14/V15, non relus par LAB) |
| L11d C16 | MB11:507 | Si un Conway contient une grille 3 × 3 (composante μ = 1 de H_l), alors (B) (droite spéciale). ¦ Implication : P ; existence d'une grille : O ¦ L11d-1… | ouverte | R1-36 | existence d'une grille ouverte ; elle découle de P ≥ 694 (note 08) |
| L11d C17 | MB11:508 | Une relation z = 2q + u avec u à 4 ou 6 entrées impaires (8 sur trois étoiles) n'existe dans aucune complétion Conway. ¦ P ¦ L11d-184 | fait |  | P |
| L11d C18 | MB11:509 | Un monde de norme 16 de rang 33 ayant une cellule morte est exclu au rang 37 ; N16 au rang 37 = catalogue × (0,3 s à 1 min par monde). ¦ E ; catalogue… | ouverte | R1-12 | catalogue N16 incomplet |
| L11d C19 | MB11:510 | Exclure la branche co-Heawood sans hypothèse de rang ne ferme aucun rang. ¦ P/H ¦ L11d-046, L11d-048 | fait |  | portée |

### B.5 L11e (pont, lois à quatre étoiles, 14-17/10) — 23 conditionnels

Répartition : ouverte 17 ; réfutée 4 ; critère 1 ; fait 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| L11e K1 | MB11:584 | (H-MATCH) : tout bloc à 4 étoiles admissible, T, U >= 0, nullité >= 14 a M_1 = h(M_0) et M_3 = h(M_2) ¦ pas de Conway (21 grilles en un sommet : point… | ouverte | R1-08 ; R1-40 | H-MATCH ; données issues de structures impossibles (L08-166) |
| L11e K2 | MB11:585 | (N9-NG) : bloc PSD sans grille ⇒ nullité <= 9 + min(c(l), c(m)) ; ou seulement NG5 (non-grille et ν >= 14 ⇒ c >= 5 des deux côtés) ¦ t(l) >= 8 pour to… | ouverte | R1-07 | N9-NG / NG5 / NG7 |
| L11e K3 | MB11:586 | (NG7) : aucun bloc non-grille avec min(t(l), t(m)) <= 7 ne passe T/U PSD, ν >= 14, F7, DISC, extension ¦ pas de Conway (il en existe >= 254) ¦ P ¦ O ¦… | ouverte | R1-07 | N9-NG / NG5 / NG7 |
| L11e K4 | MB11:587 | rang F >= 12 pour tout bloc sans grille, orienté sur la droite de c minimum (⇔ N9-NG ⇔ corank(Q) <= 7) ¦ contradiction avec rang F <= 7 + c_min <= 11 … | ouverte | R1-32 ; R1-40 | ⟺ N9-NG ; ≈ 7 444 côtés issus de structures impossibles (L08-166) |
| L11e K5 | MB11:588 | ODDCONST et SYM6 sur tous les côtés sans grille (Q7) ¦ pas de Conway (avec P <= 852) ¦ P ¦ O ¦ pont:#928, L11e-127 | ouverte | R1-07 | ODDCONST prouvé si ιx ∈ ker T_S (L08-026) ; cas couplé et SYM6 ouverts |
| L11e K6 | MB11:589 | ODD-PURE (rang D = 9) et rang Z >= 1, >= 2, >= 3 respectivement à c_min = 2, 3, 4 (c_min = 1 est déjà impossible sous ODD-PURE) ¦ pas de Conway ¦ P ¦ … | ouverte | R1-32 | marge d'ODD-PURE non uniforme (L11e-130) : il faut un argument exact |
| L11e K7 | MB11:590 | (R7-NG) : tout bloc PSD sans grille a rang_F7(8T_S) >= 29 ¦ pas de Conway (avec L4/L22 et N2) ¦ P ¦ O (données : >= 30 sur 3722 blocs, mais 93 % ont (… | ouverte | R1-10 ; R1-40 | R7-NG ; données impossibles (L08-166) |
| L11e K8 | MB11:591 | (R7) : PSD ⇒ rang_7 >= 29 ; (K22) : PSD et ν >= 14 ⇒ rang_7 >= 23 ¦ Conway exclu ; k = 22 (r = 37) exclu ¦ P ¦ (R7) R (grilles à 25) ; (K22) O ¦ pont:… | réfutée | R1-10 ; R1-40 | (R7) réfutée (grilles à 25) ; (K22) ouverte, ⟸ (a′) aux paires c = 1 génériques (L08-166) |
| L11e K9 | MB11:592 | positivité à 4 étoiles incompatible avec 8 - δ chutes 7-adiques (au rang 37) ¦ r = 37 exclu ¦ proposition (non rédigée) ¦ O ¦ pont:#784, L11e-044 | ouverte |  | proposition non rédigée |
| L11e K10 | MB11:593 | il n'existe aucune structure admissible à cinq étoiles (52 labels) ¦ pas de Conway ¦ P (relaxation) ¦ O (18/34 cas en TIMEOUT 90 min) ¦ pont:#890, #90… | ouverte | R1-09 | 18/34 cas en TIMEOUT |
| L11e K11 | MB11:594 | R8 (4 étoiles exactes + les 8 labels {4,t}) UNSAT ¦ pas de Conway ¦ P (relaxation de la 5e étoile) ¦ O ¦ pont:#918, L11e-123 | ouverte | R1-09 | R8 |
| L11e K12 | MB11:595 | H46-c1 : c(l) = 1 ⇒ λ_2(A_H) < 3 sur H = N(l) ∪ (N(x) privé de N[l]) ¦ aucune droite c = 1 (l'entrelacement impose λ_2 = 3) ¦ P ¦ O (données : 3480/34… | ouverte | R1-31 | H46-c1 ⟸ ODDCONST (L08-033) |
| L11e K13 | MB11:596 | « toute droite est dans une grille » ¦ c = 1 impossible ¦ P (immédiat) ¦ O (aucun mécanisme, pont:#956) ¦ pont:#954, L11e-139 | ouverte | R1-31 | aucun mécanisme |
| L11e K14 | MB11:597 | (B') : aucun bloc PSD de ν >= 14 n'a de droite c = 1 ¦ toute droite de Conway spéciale (pas une exclusion seule) ¦ P ¦ O ¦ pont:#843, #961, L11e-140 | ouverte | R1-31 | (B′) ; avec [m ≥ 2 exclu] seulement (L08-168) |
| L11e K15 | MB11:598 | t(l), t(m) >= 8 ou t(l) + t(m) >= 15 sous la condition à 4 étoiles ; 4 grilles par droite ¦ P >= 924 / 867 > 852 ; ρ >= 154 > 126 ¦ P ¦ O ¦ pont:#762,… | ouverte | R1-06 | T8/T15 |
| L11e K16 | MB11:599 | MIX <= 2 ; MIX <= 3 (borne universelle des relations mixtes) ¦ ρ >= 198 > 191 ; ρ >= 154 > 126 ¦ P (réduction non re-vérifiée par Codex) ¦ R (#782) ¦ … | réfutée |  | R (pont:#782) |
| L11e K17 | MB11:600 | aucun bloc PSD ne porte >= 4 relations mixtes ¦ pas de Conway (avec le budget >= 336 drapeaux) ¦ P ¦ R (c31_mix4, c21_mix4, c11_mix6) ¦ pont:#781, #78… | réfutée |  | R (pont:#782) |
| L11e K18 | MB11:601 | (A4) ; (A) ; ODD9 ; H4' ¦ toutes les droites spéciales, ou au plus une non spéciale par sommet ¦ P ¦ (A4), (A), ODD9 : R ; H4' : O ¦ pont:#741, #746, … | réfutée |  | (A4), (A), ODD9 réfutées ; H4′ ouverte |
| L11e K19 | MB11:602 | moyenne de ‖E_vlm‖_F² sur les 2079 triplets > ~1190 ¦ P < 0, contradiction ¦ P ¦ inutilisable seul : 504 est atteignable dans la relaxation (#770) ¦ p… | ouverte |  | inutilisable seul : 504 atteint dans la relaxation |
| L11e K20 | MB11:603 | KER-SYM (noyau de grande nullité invariant par une h·p) ¦ H-MATCH se réduit à un nombre fini de types de p ¦ indicatif ¦ universelle : R ; ν >= 14 : O… | ouverte | R1-08 | KER-SYM universelle réfutée ; ν ≥ 14 ouverte |
| L11e K21 | MB11:604 | une borne strictement positive d'un défaut pour tous les candidats binaires (selon #910 ; formulation à clarifier) ¦ contradiction globale ¦ annoncée … | ouverte |  | annoncé sans preuve |
| L11e K22 | MB11:605 | nombre de complétions étiquetées d'un bord H < ordre de Aut(H) ¦ pas de complétion asymétrique de H ¦ P (critère) ¦ application aux bords 43/44 : O ¦ … | critère | R1-16 | application aux bords 43/44 ouverte |
| L11e K23 | MB11:606 | branche « minimum GLOBAL c >= 4 » entièrement fermée ¦ tout Conway a une droite c <= 3 ¦ P ¦ S (76/79 au 17/10 ; 79/79 au 18/10 par CP-SAT, hors lot) … | fait | R1-14 | S (CP-SAT) ; vérification adverse en cours (V3) |

### B.6 L11f (pont, route c, gabarits, 17-20/10) — 19 conditionnels

Répartition : fait 15 ; ouverte 3 ; caduque 1.

| réf. | ligne du matériau | énoncé (abrégé) | état de X | lien R1 | note |
|---|---|---|---|---|---|
| L11f l.714 | MB11:714 | min global c(L) ≥ 4 ¦ contradiction (tout Conway a une droite c ≤ 3) ¦ S (CP-SAT, sans certificat portable) ¦ — ¦ pont:#1050 (L11f-054) | fait | R1-14 | S ; vérification V3 en cours |
| L11f l.715 | MB11:715 | plafond P ≤ 791 (racine de s minimal, branche c ≥ 4) ¦ gabarit 7 fermé comme racine minimale ; P ≤ 593 ferme aussi 9 ¦ P (arithmétique) ¦ O ; le plafo… | caduque | R1-14 | branche c ≥ 4 close (S) ; P ≤ 791 non établi (plafond prouvé 852) |
| L11f l.716 | MB11:716 | la racine x minimise 9s + 8g et g(x) = 12, s(x) ≥ 48 ¦ impossible (score ≥ 528 > 504) : 7 exclu ¦ C ¦ — ¦ pont:#1018 (L11f-035) | fait |  | C |
| L11f l.717 | MB11:717 | carré de blocs-paires, exactement 2 grilles parmi les 3 rectangles de T, et H_F = H_D (D disjoint) forcée par C h = 0 ¦ gabarit exclu (e_F ≥ 4 contre … | fait |  | P (preuve manuscrite non relue) |
| L11f l.718 | MB11:718 | aucune marche fermée de Ĵ à signes alternés ne passe par la non-grille q ¦ contradiction (e(q) = 4) ¦ P ¦ testé par BFS : 51,1 % des classes c = 1 ¦ p… | ouverte |  | X vérifié par BFS sur 51,1 % des classes c = 1 seulement |
| L11f l.719 | MB11:719 | le graphe des grilles à une racine contient C4 ⊔ C3 ¦ les deux diagonales du C4 sont des grilles (K4 ⊔ C3) ¦ E (dépend de E3 et du calcul de 5602) ¦ —… | fait |  | E |
| L11f l.720 | MB11:720 | le graphe des grilles contient K4 sur X et deux arêtes du triangle complémentaire ¦ la troisième est une grille ¦ P (LAB, non relu) ¦ — ¦ pont:#1181 (… | fait |  | P (LAB, non relu) |
| L11f l.721 | MB11:721 | familles K3 et 2K2 fermées, H01 = −H02 ≠ 0, Q12 grille ¦ les grilles sur les 4 autres racines forment une étoile ¦ P ¦ K3 : E ; 2K2 : E (RUP/DRAT sur … | fait |  | familles K3 et 2K2 : E |
| L11f l.722 | MB11:722 | famille P3 fermée ¦ K3 fermée, et 821 ouverts retirés au 19/10 00:19 ¦ P (inclusion des hypothèses) ¦ O (production inachevée) ¦ pont:#1190, #1207 (L1… | ouverte | R1-14 | production P3 inachevée |
| L11f l.723 | MB11:723 | K3 et 2K2 fermées ¦ registre 1 163 → 537 ; avec P3 : 250 ¦ H (projection) ¦ réalisé pour K3 et 2K2 ¦ pont:#1224 | fait | R1-14 | projections H réalisées (E) |
| L11f l.724 | MB11:724 | P3NB et K2BC tombent ¦ 45 ouverts ; avec P3 et 2K2N : 32 ; plus tard 40 / 32 / 30 ¦ H (projection) ¦ P3NB : E ; K2BC : E (relecture en cours) ¦ pont:#… | fait | R1-14 | projections H réalisées (E) |
| L11f l.725 | MB11:725 | H_A = −H_B pour deux rectangles disjoints (les 3 racines restantes deux à deux en grilles), sous E3 ¦ e(A) = e(B) = 2, R_AA = R_BB = 4, R_AB = −4 ¦ P … | fait |  | lemme P (ou P/E), propre au gabarit |
| L11f l.726 | MB11:726 | H_P = H_Q pour deux rectangles disjoints non-grilles, sous E3 ¦ deux couplages parfaits sans arête entre eux (4K2) ; h ternaire ou un seul −2 ¦ P ¦ si… | fait |  | lemme P (ou P/E), propre au gabarit |
| L11f l.727 | MB11:727 | 2K2N, S = {0,1,2}, et E(Q12) ≤ 3 (fermeture 2K2) ¦ E(C) ∈ {28, 32, 36, 40} pour C = Q12 + Q35 + Q36 + Q45 + Q46 ¦ P ¦ E(Q12) ≤ 3 : conséquence de la f… | fait |  | lemme P (ou P/E), propre au gabarit |
| L11f l.728 | MB11:728 | 5602 : R25,25 = 8 et R04,25 + R16,25 ≤ −1 ¦ vᵀRv ≥ 104 pour v = 11(e04 + e16) + e25 + 7e35 ¦ P (spécifique au gabarit) ¦ — ¦ pont:#1155 (L11f-093) | fait |  | lemme P (ou P/E), propre au gabarit |
| L11f l.729 | MB11:729 | 5602 : le bloc principal S 6 × 6 de (04,06,14,16,25,36) est la sous-matrice de R ¦ aucune complétion (interdit) ¦ P / E ¦ — ¦ pont:#1152 (L11f-093) | fait |  | lemme P (ou P/E), propre au gabarit |
| L11f l.730 | MB11:730 | sous c ≥ 3 GLOBAL ¦ N(L) en 3 bins non vides de tailles 6h (h = 1..4), équilibrés, sans arêtes entre bins ¦ P ¦ branche (A) jamais exploitée dans le p… | fait | R1-14 | c ≥ 3 global : 3 bins, jamais exploité |
| L11f l.731 | MB11:731 | L est dans 6 grilles ¦ Spec B = {8, 3^18, (−2)^6, (−1)^10, 1^12, (−4)^13} et 13 vecteurs propres −4 de Conway portés par D_L ¦ P (redécouverte) ¦ — ¦ … | fait |  | P (redécouverte) |
| L11f l.732 | MB11:732 | « aucune droite dans six grilles » démontré ¦ 7 des 19 sans paire tomberaient (d'après L08-126, hors de ce lot) ¦ — ¦ O ¦ L08-126, L08-138, L08-141 | ouverte |  | « aucune droite dans six grilles » (vérification V1/V2 en cours) |
