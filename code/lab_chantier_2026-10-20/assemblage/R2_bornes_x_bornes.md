# R2 — Bornes × bornes (phase de recombinaison, 20/10/2026)

Agent R2. Matériau lu en entier : `assemblage/MATERIAUX_BRUTS_partiel.md` (L01 à L08, L10) et
`assemblage/MATERIAUX_BRUTS_L09.md` (L09, 210 bornes). Les lots L11a à L11f (pont) ne sont pas lus : seconde passe.
Sorties : ce fichier et `assemblage/R2_bornes_x_bornes.jsonl` (23 lignes, R2-01 à R2-23).
Statuts recopiés des sources, jamais rehaussés. « Vu par R2 » signale une remarque de cet agent, non relue.

---

## 0. Résumé

1. **Aucune contradiction nouvelle entre bornes établies (P, C, E) à portée compatible.** Les contradictions déjà
   connues sur des bornes établies n'excluent que des sous-cas :
   - rangs r ≤ 35 ;
   - n3 = 705 (externe) ;
   - familles G1 c55 et ⟨z, hM⟩ (rang_F7 ≥ 29 > 28) ;
   - « a₉ = a₁₃ = 0 » aux rangs 37, 39 et 41 (R2-15).

   Toutes les autres portent sur des hypothèses ouvertes ou réfutées.
2. **Trois combinaisons nouvelles, sans exclusion du graphe :**
   - (R2-01) P ≤ 852 est exactement 4·[P − 3G ≤ 693] + 3·[3P + 4G ≤ 2772]. La première facette est élémentaire
     (identité des coins, septembre) ; la seconde est le certificat entier du 18/10.
   - (R2-02) Le sous-cas « chaque triangle est dans ≥ 4 grilles » de la note 225, dont les 2 types de noyaux étaient
     laissés ouverts, est vide par le recensement. Le sous-cas « ≥ 3 grilles » est confiné à G ∈ [121, 126],
     P ∈ [726, 762].
   - (R2-03) Au rang 43, b₂ ≥ 1000 pour tout k (au lieu de 968), et b₂ ≥ 1264 s'il existe une racine de M.
3. **Quasi-ratés les plus serrés :**
   - N_Wagner ≤ 18 709 contre ≥ 18 710 requis à P = 0 (externe, 0,005 %) ;
   - (T15) : P ≥ 866,25 contre P ≤ 852 (1,7 %) ;
   - (T8), (NG5), (N9-NG) : P ≥ 924 (8,5 %) ;
   - rang 37 : a₁₀ ≥ 34 418 contre 7920·c₂₀ avec c₂₀ ≤ 4 (8,6 %) ;
   - coin sans grille du rang 37 : seuil 27 142 contre plafond 31 976 (15,1 %, flottant).
4. **Symétrie forcée : croisement vide.** Les pièces de grand groupe connu (cadre, |Aut| = 645 120) n'ont aucune
   borne supérieure de complétions. Les pièces à complétions bornées (bords positifs V15, ≤ 2 ou 1) n'ont aucune
   symétrie forcée. La raison est structurelle (R2-12, vu par R2) : un bord positif ne contient aucun support d'un
   vecteur de ⟨1⟩ ⊕ E₃, alors que N[x], les grilles et les paires de prismes jumeaux en sont.
5. **Incohérences :**
   - arrondis (P ≤ 853, N₂ ≥ 1599) ;
   - facteur 2 sur les co-Heawood (« ≤ 7920 ») ;
   - statut de a₇ ≤ 842 (E ou H) ;
   - rédaction fausse de « b₂ ≥ 968 » ;
   - « ≥ 22 vecteurs de normes 16-20 » au lieu de ≥ 1280 ;
   - nombreuses collisions de notations (ρ, τ, H, c, k, « moulins »).

### Candidats classés par potentiel (JSONL)

| potentiel | entrées | ce qui manque |
|---|---|---|
| EXCLUSION_GRAPHE | R2-06 ((T15) ou (T8) contre P ≤ 852) | une hypothèse ouverte et fragile |
| EXCLUSION_RANG | R2-05 (rang 37 : N16, N18 et c₂₀ ≤ 4) | trois énoncés ouverts |
| EXCLUSION_CAS | R2-02 (q = 4 vide), R2-08 (P = 0 : E ≤ 8), R2-15 (a₉ = a₁₃ = 0, connu) | R2-02 acquis ; R2-08 est ouvert |
| REDUCTION | R2-01 (P ≤ 852 par deux facettes), R2-03 (b₂ ≥ 1000 au rang 43), R2-09 (n3 ≥ 1602), R2-10 (conversion externe), R2-13 (filtre de flips) | — |
| AUCUN | R2-04, R2-07, R2-11, R2-12, R2-14, R2-16, R2-17, et les incohérences R2-18 à R2-23 | — |

---

## 1. Normalisations vérifiées (à lire avant tout croisement)

| symbole | sens retenu | relations exactes | source |
|---|---|---|---|
| P | prismes triangulaires (tout prisme est induit) | n3 + 3P = 4158 ; Σ_T t(T) = 2P ; Σ_x s(x) = 6P ; Σ_x \|W(x)\| = 8316 − 6P | L03b B2 ; L08-188 ; RACINE_PONDEREE:30-33 ; L09-BORNE-006 |
| n3 (externe) = N₂ (équipe) | paires de droites reliées par exactement deux arêtes (N3 induits de Reimbayev) | N₂ = 4158 − 3x₁, x₁ = prismes | NOTE.md:2752 ; L01-46 |
| G = ρ | grilles 3×3 induites | 9G = Σ_x g(x) ; 6G = Σ_T g(T) ; P ≥ 6G ; t(T) ≥ 2g(T) | RACINE_PONDEREE:31,53-55 ; L05-150 |
| t(T) = π(L) = p(l) | prismes contenant la droite T (triangles transversaux de G_T) | t ∈ {0,…,10, 12} (jamais 11, Lou–Murin) | L09-BORNE-031 ; L07 B1 |
| c(T) | composantes du graphe cubique G_T (36 sommets) | c ≤ g + ⌊(6 − g)/2⌋ ; c = 1 ⇒ g = 0 ; t ≤ 7 ⇒ c ≤ 4 | L05-150 ; L08-167 ; L08-188 |
| s(x) | prismes passant par x | s(x) = Σ_{T∋x} t(T) = budget « τ(v) » de L08 | RACINE_PONDEREE:30 ; L09-BORNE-192 |
| a_k | vecteurs de norme 2k de L1, **deux signes** ; L1 ⊃ L = ℤ⁹⁹ ∩ ker(A + 4I), indice 3 | min(L1 \ L) ≥ 22, donc a_k = N_{2k} externe pour 2k ≤ 20 ; a₇ = N14 = 2·#co-Heawood | L06 BORNE-03 ; NOTE.md:1072-1073 ; L03b (N14 « deux signes ») |
| b_k | vecteurs de norme 2k de M = √7 L1*, deux signes | b₁ ≤ a₇ à tout rang (√7·racine = vecteur de Fano) ; au rang 43, a₇ = b₁ | NOTE.md:3913-3914 ; note 242:31-34 |
| r, r_ext | r = rang₇(A − 3I) ; r_ext = rang_F7(2A − J + I) | r = r_ext + 1, **désormais P** | CARTE_MAITRESSE.md:72-87 ; L03a-103 |
| k | r − 15 | k ∈ {22, 24, 26, 28} | L06-024 |

Contrôle de cohérence (vu par R2) : la forme de Smith de la matrice de Seidel sur ℤ₇, 1^{14+k} 7^{71−2k} 49^{14+k}
(L09-BORNE-057), coïncide avec celle de T = 9S + 7J dans le dépôt externe (L03b B12) après conversion r_ext = r − 1.

---

## 2. Registre par objet

### 2.1 Prismes P

| inégalité ou identité | portée | statut | source |
|---|---|---|---|
| P ≤ 1386 (ordre 6, n3 ≥ 0) ; P = 1386 exclu (Makhnev 1988 : n3 > 0) | général | E ; P publié (texte de 1988 non rejoué) | L08-137, L08-139 ; L03b K2 |
| P ≤ 1155 (SDP sur triplets de droites) | général | E | L09-BORNE-017 |
| P ≤ 1151 (L16, Krein ; ⇔ n3 ≥ 705 ⇔ Σ\|W\| ≥ 1410) | général | P | L09-BORNE-007/008 ; L05-235 |
| P ≤ 1150 (n3 ≥ 708 externe ; rayon spectral du graphe des prismes < 10, Codex 14/10) | général | P (VER externe) ; P | L03b-078 ; BORNE-L10-02 |
| **P ≤ 852 = ⌊11088/13⌋** (recensement d'ordre 9) | général | C relatif au recensement (E en double implantation) | L05-019 ; CARTE §8.1 |
| **3P + 4G ≤ 2772** (12 identités, certificat entier) | général | C | L05-181 |
| **P ≤ 693 + 3G** (⇔ n3 ≥ 2079 − 9G ; identité des coins + Lou–Murin) | général | P | L01-46 ; note C2 08:7-17 |
| P + 5ρ ≤ 1386 ; 14a₇ + 25P + 32ρ ≤ 28 182 ; 4N(F10) + 75P + 96ρ ≤ 84 546 | général | C (Codex) | BORNE-L10-05 ; L05 B08 |
| 5Σ‖E‖² + 928P + 48Z ≤ 12 374 208 ; 5Δ + 448P − 72Z ≤ 7 135 128 | général | P | L05 B30 |
| P ≤ 692,39 (ordre 10, flottant) | général | X (non établi) | L08-157 |
| P ≤ 821 puis ≤ 816 ; P ≥ 594 puis ≥ 660 | branche c ≥ 4 | P sous front76 (S) | RACINE_PONDEREE:51-62, 298 |
| P ≤ 462, P pair | k = 10 (historique) | P | L09-COND-040 |
| P ≥ 6G | général | P | RACINE_PONDEREE:53-55 |
| P ≥ 450 | r = 35 (exclu depuis) | C | L05 K15 |
| P > ~285 | rang 37, si P plafonné au niveau masse 6 seul | E (relais) | L02_C2_aws-380 |
| P ≥ 924 ; P ∈ [924, 1122] ou [924, 1151] | k = 18 sous NT | P conditionnel | L09-BORNE-090 ; JOURNAL:451 |
| P ≥ 924 ; P ≥ 866,25 ; P ≥ 792 ; P ≥ 231 ; P ≥ 1 ; P ≥ 24 | sous (T8)/(NG5)/(N9-NG) ; (T15) ; « une droite t ≥ 8 par drapeau » ; conjecture (P) ; repère 231 ; branche Heawood du Fano tendu | O (hypothèses) | THREE_RESULTS:58-61, 102 ; AUDIT_EXCLUSIONS:46, 139-140 ; L07 K16 ; L05 K35 ; L09-COND-140 |
| P = 0 admet un point entier du recensement (6435 comptes, ordres 7-9) | général | E | L05-149 ; L09-BORNE-055 |
| P ≈ 126 pour un Γ tordu « générique » | heuristique | H | L09-BORNE-018 |

**Plafond de torsion à viser** : la pièce manquante n'est plus « P ≥ 1152 » (L01, L09-LEMME-002), mais **P ≥ 853**.

### 2.2 Grilles G = ρ, g(x), g(T)

| inégalité | portée | statut | source |
|---|---|---|---|
| G ≤ 231 (clôtures K3□K3), ≤ 198 (g ≤ 18), ≤ 191 (P ≤ 1150), ≤ 165 (r = 43 : g(x) ≤ 15) | général / r = 43 | P | L03b B5 ; L09-BORNE-051 ; L05 B03 |
| **G ≤ 126** (11ρ ≤ 1386, ou 22G ≤ 2772 avec P ≥ 6G) | général | C | L05-019 ; L05-181 |
| G ≥ (P − 693)/3 | général | P | L01-46 (forme n3 ≥ 2079 − 9N) |
| g(x) ≤ 17 (≤ 18 par L10) ; g(x) ∈ [0, 19], g ≠ 20, 21 ; ≤ 20 (GRID21) | général | P ; C | L09-BORNE-011/066 ; L05 B03 |
| g(x) ≤ 12 à la racine de budget ; ≤ 14 au point fixe d'une involution | racine choisie ; C2 | P | L08-066 ; L09-BORNE-168 |
| ≤ 11 grilles deux à deux disjointes | général | P | BORNE-L10-04 |
| c_min ≥ 3 ⇒ chaque sommet dans une grille (G ≥ 11) | c_min ≥ 3 | P (dossier externe, non relu) | COND-L10-32 |
| c ≥ 4 partout ⇒ g(x) ≥ 7, G ≥ 77, puis G ≥ 81 | branche c ≥ 4 | P sous front76 (S) | RACINE_PONDEREE:28-30, 60-62 |
| rang 37 et tout G(T) connexe ⇒ ρ = 0 (donc P ≤ 693 par la facette des coins, vu par R2) | rang 37 | P conditionnel | L06-087 |
| aucune droite dans 4 ou 6 grilles ⇒ ρ ≤ 115, τ_g ≤ 693 | rang 37 | H | L06-052 |
| A₅ = 1040 + 52G (réseau E de rang 60, côté +3), donc A₅ ≤ 7592 avec G ≤ 126 (vu par R2 ; source : ≤ 13 052) | général | P | L05-011 |
| Σ_drapeaux m = 12 474 − 45ρ + 3O + 6H + Δ ≥ 6804 | général | P | L07 B1 ; L05 B30 |

### 2.3 n3 = N₂, torsion |W(x)|, hexagones, S

| inégalité ou identité | portée | statut | source |
|---|---|---|---|
| n3 ≥ 693 (Schur), puis 705, puis 708 ; n3 ≡ 0 (mod 3) | général | P (VER externe) | L03b-071, -078 ; L03a B-17 |
| **n3 ≥ 1602** (via P ≤ 852) ; forme flottante N₂ ∈ [1599, 4158] | général | C ; E | R2-09 ; NOTE.md:2754 |
| n3 ≥ 396 (« frontière complétée ») | conditionnel | P | L09-COND-034/036 |
| Σ_x \|W(x)\| = 8316 − 6P = 2·n3 ≥ 3204 ; moyenne ≥ 32,36 | général | P + C | L09-BORNE-006 ; L07 B1 (« ≥ 32,4 ») |
| \|W(x)\| ≥ 6 (plancher local) | général | S | L09-BORNE-052 |
| hexagones induits H = 213 444 − 3P ≥ 210 888 ; C6 induits (externe) = 209 286 + n3 | général | P | L09-BORNE-019/083 ; L03b B1 |
| P ≥ 1152 ⇔ H ≤ 209 988 | général | P | L09-COND-087 |
| χ(Σ) = 3P − 4158 = −n3 ≤ −1602 (source : ≤ −705) | général | P | notes/100:189 ; L09-BORNE-053 |
| S ∈ [0, n3] ; Σ_L c₄(G(L)) = S + 3P ∈ [3P, 4158] | général | P | L09-BORNE-010, -085 |
| tr(A₄) = 84(n3 − 693) ≥ 76 356 ; ⌈2n3⌉₄ ≤ h11 ≤ 4n3 ; 2n3 ≤ z11 ≤ 4n3, 4 \| z11 | général | P / C (externe) | L03a B-20, B-21 ; L09-BORNE-035 |
| N_cube ≤ (41 580 − n3)/12 : ≤ 3465, ≤ 3331 avec P ≤ 852, ≤ 3118 à P = 0 | général | P (VER externe) | L03a B-34 |
| N_Wagner ≤ 3N_cube + 9355 ; 4N_Wagner ≤ 41 580 − n3 + 12N_cube ; F = 166 320 − 8N_Wagner | P = 0 (la première et la dernière) | P (VER externe) | L03b-201, -205 |

### 2.4 Droites : t, c, d(L), blocs

| inégalité | portée | statut | source |
|---|---|---|---|
| 0 ≤ t ≤ 12, t ≠ 11 ; n₀ = 32 − t, n₁ = 144 + 3t, n₂ = 36 − 3t | général | P | L07 B1 ; L09-BORNE-031 |
| Σ t = 2P ≤ 1704 ; moyenne de t ≤ 7,377 ; moyenne de t(l) + t(m) sur les 2079 drapeaux ≤ 14,753 | général | C | THREE_RESULTS:58 ; L07 B1 |
| ≥ 18 droites t ≤ 7 ; ≥ 254 blocs non-grille contenant une telle droite ; ≤ 170 droites t ≥ 10 | général | P ; P ; programme | L09-COND-226 ; L07 B1 |
| il existe une droite c(L) ≤ 3 | général | S (CP-SAT, sans certificat portable) | L05 K10 ; L09-COND-225 |
| ≤ 32 droites c ≤ 2 ⇒ une racine à 7 droites c ≥ 3 ; sinon ≥ 33 droites c ≤ 2 | général | P | COND-L10-30 |
| d(L) = 1 ⇒ k ≥ 22 ; k ≥ 23 − d(L) + 2r(L) ; d(L) = 1 et (τ\|7) = +1 ⇒ k ≥ 24 | général | P | L09-COND-018, -020 |
| d(L) : 1 (85 %), 2 (14 %), 3 (0,6 %), max 9 observé | données | H | L09-BORNE-048 |
| graphes de droite : 187 381 435 694 classes, 147 579 095 390 admissibles ; t ≤ 7 : 187 379 400 048 / 147 577 214 193 ; \|Λ\| = (2⁶·6!)³·6 ≈ 5,87·10¹⁴ | général | E ; P | L08-220 ; L08-187 |

### 2.5 Paires de prismes jumeaux τ (et constantes de collision)

| inégalité | portée | statut | source |
|---|---|---|---|
| τ ≤ 5P/2 ; ≤ 2P + 3ρ ; 4τ ≤ 12P ; 4τ ≤ Φ ; 17τ ≤ 17P + 105ρ ; τ ≤ P + 5ρ + 17 ; τ ≤ (P − 6ρ) + Σ C(g,2) ; τ_g ≤ 11ρ + 17 | général | C/P | L06 BORNE-17 |
| τ ≤ 1890 → 1534 → 1403 → **1354** (r ≥ 37) → 1326 (r = 43) | rangs | C | L05 B04 |
| τ ≤ 2871 (normes 12 du côté +3 ≤ 5742) ; ≤ 8625 (LAB) | général | P (14/10) | L07 B1 ; L07 sous-lot J:1133-1146 |
| τ ≥ 33 | r = 35 (exclu) | C | L05 K15 |
| τ total ≥ ~540 (τ_g ≥ 614 sans paire non-grille ; τ_n ≥ 535 sans grille), canaux de masses 7-9 non bornés | rang 37 | H (PL flottant) | L06-049 ; COND-L10-20 |
| constante par paire de grilles ∈ [16 496, 27 828] ; paire non-grille ≤ 31 976 ; C6 ≤ 38 084 490 | général / r ≥ 37 | C | L06 BORNE-19 |
| seuils de rentabilité du coin sans grille : 25 201 ; 27 142 (N14) ; 33 780 (N14 + N16, hypothétique) ; point mort 13 900 < 16 496 | rang 37 | H | NOTE.md:3455-3472, 3830-3843 ; CARTE §4.E |

### 2.6 Rang r et k

| inégalité | portée | statut | source |
|---|---|---|---|
| r impair, 15 ≤ r ≤ 45 → ≥ 21, 23, 25 → ≥ 29 (thêta seul) → ≥ 33 → ≥ 35 → **r ∈ {37, 39, 41, 43}** | général | C (programme thêta de niveau 7, audité par Codex) | L09-BORNE-004 ; L06-023, -024 |
| k ≤ 28 (L22), k = 30 exclu ; « k ≤ 34 (indice de Witt) » est une borne plus ancienne et plus faible | général | P | L09-BORNE-005, -045 |
| r_ext pair ∈ {28, …, 42} (W66) ⇒ r impair ∈ {29, …, 43} | général | P (dictionnaire P depuis le 20/10) | L03b B10 ; CARTE §1.6 |
| 7-rang d'un bloc à quatre étoiles ≤ k ≤ 28 ; rang_F7(8T_far) ≤ 28 ; rang_ℚ(T) ≤ 30 | général | P | L05 B12 ; L08-205 |
| familles de L1 : rang de Gram mod 7 ≤ 45 − r (8 au rang 37) ; noyau ≤ 56 − r ; r ≤ 45 − m pour m vecteurs de Gram inversible mod 7 | général | P | L06 BORNE-25 ; L08-202 |
| det L₋₄ = 9·7^{r−1} (rapport 02, [R] non relu) ; det L1 = 7^{r−1} ; det M = 7^{45−r} ; det M_ext = 9·7^{44−r_ext} = 9·7^{45−r} | général | P / [R] | L04 (rapport 02 §6.2) ; note 242:22 ; L03b B11 |
| tout sous-graphe induit sur \|I\| > 14 + k sommets a det S(Γ[I]) ≡ 0 (mod 7) | général | P | L09-COND-050 |

### 2.7 Réseau L1 (vecteurs propres de −4) : a₇ à a₁₄

| inégalité | portée | statut | source |
|---|---|---|---|
| min L ≥ 14 ; min(L1) ≤ 20 (r = 37), ≤ 24 (39, 41), ≤ 26 (43) | rangs | P ; C | L06 BORNE-03, -04 |
| **a₇** ≤ 7920 → 3960 → 990 → 842 (flottant) → **792** (≤ 396 co-Heawood) ; a₇ + 13ρ ≤ 2013 ; a₇ + 4b₁ ≤ 990 (LAP, non audité) ; a₇ ≤ 9h ; ≤ 347 en un sommet riche en grilles | général | P/C/H | L06 BORNE-05 ; L05 B08, B13 |
| N14 ≤ ⌊(55 440 − 4n3)/7⌋ (≤ 7004 avec n3 ≥ 1602) ; ≤ 4950 à P = 0 (externe) | général / P = 0 | P (VER externe) | L03b B6 |
| **a₇ = 0 au rang 37** (lemme N14), donc b₁ = 0 | rang 37 | E (non audité) | L06-092 ; NOTE.md:3913-3914 |
| a₇ = b₁ ≤ 44 | rang 43 | P | L06 BORNE-05 ; L05-029 |
| **a₈** ≤ 90 090 → 27 720 → **6930** (7a₇ + 8a₈ ≤ 55 440) ; 7a₇ + 8a₈ + 273b₁ ≤ 55 440 (LAP) ; externe : aucune borne supérieure sur N16 | général | P | L06 BORNE-06 ; L03b B8 |
| a₉ ≤ 9240κ₁₈ ; ≤ 6160c₁₈ (supports indépendants) ; κ₁₈ = 3 localement possible | général | P | L06 BORNE-24 ; COND-L10-22 |
| a₁₀ ≤ 7920c₂₀ ; ≤ 5544c₂₀ | général | P | L06 BORNE-24 |
| identité du rang 37 : 13a₁₀ + 91a₉ + 350a₈ + 1183a₇ = 7462 + a₁₂ + 2429b₁ + 476(b₂ − 462) + 21(b₃ − 24 948) | rang 37 | C | L06-030 |
| ⇒ avec N14 : 350a₈ + 91a₉ + 13a₁₀ ≥ 447 412 (b₃ ≥ 45 898) ou ≥ 448 798 (b₃ ≥ 45 964) ; a₈ + a₉ + a₁₀ ≥ 1284 | rang 37 | E | R2-04 ; NOTE.md:4089-4093 |
| identité COND-03 : 2a₈ + 16a₉ + a₁₃ = 329(7^m + 1) + 7^{m+1}b₁ + 7a₇ + 7a₁₀ + 2a₁₁ + a₁₂, m = (45 − r)/2 (vérifiée exacte au rang 37 par R2) | rangs 37-43 | C | L06-015 ; HANDOFF:1456-1461 |
| a₉ = a₁₃ = 0 ⇒ a₈ ≥ 395 129 / 56 588 / 8 225 / 1316 (r = 37/39/41/43) | rangs | C | L06-103 |
| nombres forcés, programme de degré 0 : rang 37 ≥ 380 (couches seules 14 : 380 ; 16 : 1283 ; 18 : 4932 ; 20 : 34 523) ; rang 39 ≥ 2367 ; rang 41 ≥ 234 ; rang 43 ≥ 165 (norme 18) ou 2632 (norme 26) | rangs | E | Mandat C M:327-332 |
| nombres forcés « ext » (plus anciens) : rang 37 : 7 (≤ 20), 413 (≤ 22), 16 647 (≤ 24), 49 392 (≤ 26) ; rang 43 : 165 (≤ 26) | rangs | E | L06 BORNE-14 |
| externe W101, coquille totale jusqu'à la norme 28 : ≥ 80 110 (r = 37), 11 400 (39), 1584 (41), 182 (43) | rangs (après conversion) | C (externe) | L03a-80 ; R2-10 |
| a₁₄ = 5 097 168 − 288a₇ + 98 784b₁ + 343b₂ ⇒ ≥ 5 013 138 (a₇ ≤ 842), ≥ 5 027 538 (a₇ ≤ 792), ≥ 5 255 634 (N14) | rang 37 | E | HANDOFF:1459 ; R2-20 |
| sans normes 16, 20, 22, 24 au rang 43 : chaque classe de norme 26 porte 329 + 14k − 8(x₁ + x₂) vecteurs | rang 43 | P | L05 K14 |

### 2.8 Réseau M = √7 L1* : b₁ à b₅

| inégalité | portée | statut | source |
|---|---|---|---|
| b₁ ≤ 3784 → 88 → 78 → **44** ; b₁ ≤ a₇ | général | P | L06 BORNE-07 ; L05-029 |
| b₂ ≥ 462 ; ≥ 462 + 41b₁ + b₁²/2 ; rang 43 : ≥ 914 → 922 → 968 → **1000 (R2-03)** ; b₂ = 1000 − 16k + 25a₈ + 11a₉ + 8a₁₀ + 3a₁₁ + a₁₂ ; S₀ : b₂ = 1000 | général / r = 43 | P | L05-028, -029 ; L06-026 |
| b₃ ≥ 24 948 (audité) → 43 848 → 45 528 → 45 766 → 45 898 → **45 964** (r ≥ 37) → 46 000 (r = 43) ; ≥ 66 528 − 18P − 72ρ ; ≥ 73 920 si P = 0 ; rang 43 : ≥ 6 696 790 (≥ 7 561 631 si a₇ = 0) ; S₀ : 10 648 712 | rangs | C/E/P | L05 B05 ; L06 BORNE-09 ; NOTE.md:61 |
| b₄ ≥ 388 080 → 1 431 738 → 2 729 034 → **3 371 634** ; ≥ 3 826 746 − 30P − 4572ρ (minimum 3 227 994 au coin (756, 126), vu par R2) | général | C/P | L06 BORNE-10 |
| rang 37 : b₄ ≤ 15 196 716 (ρ = 126) ; b₄ + (651/34)b₃ ≤ 15 457 549 + (450359/272)a₇ ; avec N14 et b₃ ≥ 45 964 : **b₄ ≤ 14 577 473** | rang 37 | C ; E | L06-044 ; R2-14 |
| b₅ ≥ 18 001 368 → 34 087 368 ; b₅ et b₆ forcés à 10 % près au rang 37 | général / r = 37 | E/C | L06 BORNE-11 ; HANDOFF:1462-1464 |

### 2.9 Cocliques, α, co-Heawood

| inégalité | portée | statut | source |
|---|---|---|---|
| α ≤ 22 (Hoffman) ; une 13-coclique existe toujours ; 5 ≤ χ ≤ 11 | général | P | L03b B13 ; L09-BORNE-032 |
| coclique de 22 ⇒ design 2-(22,4,2) à 77 blocs ; au rang 43, deux 22-cocliques se coupent en 1, 8 ou 15 points ; en général ≤ 15 | général / r = 43 | P | L09-COND-055, -065 ; L06 COND-18 |
| co-Heawood ⇔ deux cocliques de Hoffman se coupant en 15 ; #co-Heawood = a₇/2 ≤ 396 ; ≤ 56 par sommet, ≤ 16 par arête, ≤ 4 par C4 ; 0 au rang 37 (N14) | général / r = 37 | P / E | L05 B13 ; L05 K26 |
| coclique 21 maximale : 2 à 6 sommets à 5 voisins, ≤ 30 sommets de défaut, 7 profils | général | P | L05 B33 |
| designs de Hoffman exclus : 72 cycliques, 199 one-rotational ; 36 classes d'échanges, dont 29 asymétriques et 7 à involution | α = 22 | E | L09-BORNE-191 ; L08-010 |
| \|V₄₄₄\| ≤ 22 et ≤ 49 | P = 0 | P | L09-BORNE-091 |
| α ≥ 21 serait nécessaire pour fermer C1 par le cadre des cocliques | — | O | L07 R26 |

### 2.10 Nullités et rangs locaux

| inégalité | portée | statut | source |
|---|---|---|---|
| ν(T_S) ≥ 14 exigé dans tout bloc de Conway | général | P | L07 B1 |
| ⟨z, hM⟩ : ν ≤ 14 et, à 14, rang_F7 ≥ 29 > 28 (famille exclue) ; G1 c55 non-grille : rang_F7 ≥ 29 (exclue) | familles locales | C ; E | L05 K09 ; L07 K9-K10 |
| ≈ 288 000 visites PSD à ν = 14, aucune à 15 ; droites c = 1 : ν ≤ 10 observé | données | E/H | L07 B1 |
| rang T44 = 23 − c + rang F = 32 − c − δ + rang Z ; Conway force rang F ≤ 7 + c(l) ; (N9-NG) ⇔ rang F ≥ 12 | général | P | L09-BORNE-196 ; L09-COND-233 |
| rang_F7(8T44) ≥ 30 observé sur 3722 blocs non-grille | données | H | L09-BORNE-197 |

### 2.11 Comptes exacts de sous-graphes induits

| compte | statut | source |
|---|---|---|
| 4 sommets : C4 2079, patte 8316, K3 + K1 13 860, griffe 27 720, P4 91 476, P3 + K1 507 276, 2K2 126 819, K2 + 2K1 1 517 670, 4K1 1 469 160 (somme = C(99,4) = 3 764 376, vérifiée par R2) | P | L07 B1 |
| 231 droites ; 2079 quadrangles (12 par arête, 84 par sommet) ; 2079 papillons (« moulins » de L07) ; 3465 triplets de droites par un sommet (« windmills » de NOTE) ; 8316 maisons | P | L09-BORNE-001 ; L07-191 ; NOTE.md:2813 |
| N(5,5) = 332 640 ; 5-cycles 41 580 ; 6-cycles 429 660 ; N(6,9) = P, N(6,8) = 20 790 − 9P, N(6,7) = 831 600 + 36P, N(6,6) = 8 560 860 − 84P | P | L06 BORNE-20 ; L09-BORNE-083 |
| N0 = 3696 − P, N1 = 16 632 + 3P, N2 = 4158 − 3P, N3 = P (paires de droites disjointes par nombre d'arêtes croisées) | P | L08-139 |
| e(S) ≤ 3, 5, 7, 9, 12, 14, 18, 19 pour s = 3..10, jamais 17 pour s = 9 ; 2e(X) ≤ 3\|X\| + \|X\|²/9 ; degré induit ≥ 6 ⇒ \|X\| ≥ 27 ; aucun 4-régulier induit à 10 sommets | P | L07 B1 ; L03b B4 ; L09-COND-053 |
| complexe des quadrangles : χ = 1485 (99 − 693 + 2079) — objet différent de la surface Σ de §2.3 | P | mémoire c1-start.md:519 |

### 2.12 Budgets

| inégalité | portée | statut | source |
|---|---|---|---|
| il existe x avec s(x) ≤ ⌊6·852/99⌋ = 51 | général | P | L08-066 ; L09-BORNE-192 |
| il existe x avec 9s(x) + 8g(x) ≤ 504 (moyenne de 18(3P + 4G)/99) | général | C+P | RACINE_PONDEREE:30-35 |
| sous c ≥ 4 : s ≤ 49 à cette racine ; min(9s + 8g) ≥ 440 | branche c ≥ 4 | P | RACINE_PONDEREE:35-38, 284-288 |
| **s(x) ≤ 42 + 2g(x) et s(x) ≥ 4g(x) en tout sommet** (version locale de la facette des coins, vu par R2) | général | P | note C2 08 ; R2-01 |
| budgets de second moment : moyenne requise > 1190,4 contre minimum atteint 504 | général | P/E | L07 B1 |

### 2.13 Automorphismes, complétions, gabarits

| objet | valeur | statut | source |
|---|---|---|---|
| \|Aut(Γ)\| | divise 2·3³·7·11 ; ∈ {1, 2, 3} (littérature) ; C2, C3, C7, C11 exclus ⇒ C1 | P (C2 : S avec réserve) | L09-BORNE-040 ; CARTE §1.7 |
| cadre Φ_x | \|Aut\| = 2⁷·7! = 645 120 ; en C1, ≥ 99 × 645 120 = 63 866 880 complétions étiquetées | P | L07-040 |
| flips | aucun flip individuel n'est un automorphisme ; un automorphisme qui retourne q > 0 droites en retourne ≥ 4 ; code des flips de taille ≤ 8 | P | L07-042, -043 |
| bords positifs (V15) | 43 sommets : ≤ 8192 signes, ≤ 2 complétions isomorphes ; 44 : unique ; \|S\| ≤ 44 | P (Codex) | L05-108 ; L07-443 |
| pièces à trois étoiles N[l] ∪ N[b] (49 sommets) | 8316 = 99 × 7 × 12 par graphe, rigides, deux à deux non isomorphes en C1 | P | NOTE_ASYM_WINDOW:150-157 |
| gabarits | c ≥ 3 : 510 926 → 10 052 → 35 ouverts ; c = 1 : 4 708 882 → 2 302 537 ; c_min = 4 : 79 (76 fermés, S) ; noyaux de Makhnev 373 → 310 → 174 | S/E/C | L08 §9.2 ; L05 B25-B27 |
| srg(243) connus (contrôles) | 8 graphes, \|Aut\| 3 849 120, 4320, 864, 3888, 2916, 108, 162, 108 | E/C | L06 BORNE-29 ; BORNE-L10-29 |

### 2.14 Spécifiques au dépôt externe (pour mémoire)

Extrémité P = 0 : Q ≥ 7059 au « rang 11 » (aucune majoration connue) ; 12 ≤ r3 ≤ 44 ; recensement des paires (r3, r7)
629 → … → 281 ; 24 388 892 640 clauses résiduelles. Extrémité n3 = 708 : det(B) ≤ 6525, h ∈ {9, 21, …}, tr(B²) ≥ 116 :
caduque par R2-09. Sources : L03a B-25 à B-45 ; L03b B15 à B27.

### 2.15 C2 (fermé, pour mémoire)

g⁻ ∈ {18, 20} ; E(v) ≥ 11 hors Π avec T16, T18, T20 ; min N* ≥ 8/7 ; 156 enveloppes ; ≤ 2 479 669 paires à
recertifier. Ces bornes ne croisent aucune borne de C1 sans l'involution ; non croisées ici (voir §9).

---

## 3. Contradictions

**3.1 Entre bornes établies (P, C, E), portée compatible : aucune nouvelle.** Les contradictions connues excluent
des sous-cas, jamais le graphe :

| sous-cas exclu | bornes qui se croisent | statut | source |
|---|---|---|---|
| r ≤ 35 | séries thêta de niveau 7 et positivité (certificats de Farkas exacts) | C | L06-023, -024 |
| n3 = 705, donc n3 ≥ 708 | positivité de Schur et parité (externe) | P (VER) | L03b-071, -078 |
| a₉ = a₁₃ = 0 aux rangs 37, 39, 41 | a₈ ≥ 395 129 / 56 588 / 8 225 contre a₈ ≤ 6930 ; il existe donc un vecteur de norme 18 ou 26 | C | L06-103, R2-15 |
| familles locales G1 c55 non-grille et ⟨z, hM⟩ de nullité 14 | rang_F7(8T_S) ≥ 29 contre ≤ 28 | E ; C | L07 K9, K10 ; L05 K09 |
| N3 = 48 (externe) | 2e(X) ≤ 3\|X\| + \|X\|²/9 : degré ≥ 6 force \|X\| ≥ 27, contre \|X\| ≤ 24 | P (VER) | L03a C-41 ; README externe |

**3.2 Contradictions avec des hypothèses (toutes déjà connues).**

| hypothèse | borne forcée | borne établie | statut de l'hypothèse | source |
|---|---|---|---|---|
| (T8), (NG5), (N9-NG) | P ≥ 924 | P ≤ 852 | O | THREE_RESULTS:97-106 |
| (T15) | P ≥ 866,25 | P ≤ 852 | O, fragile | THREE_RESULTS:61 |
| (N9) | ρ ≥ 154 | ρ ≤ 126 | R | L07 R6 |
| ≤ 2 ou ≤ 3 relations mixtes | ρ ≥ 198 ou ρ ≥ 154 | ρ ≤ 191 ou ρ ≤ 126 | R | L07 R22 |
| (R7), (K17) | rang_F7 ≥ 29 ou 30 | ≤ 28 | R ; refusé comme théorème | L07 R21, K17 |
| familles G1 c55 et ⟨z, hM⟩ | rang_F7 ≥ 29 | ≤ 28 | familles exclues (E, C) | L07 K9, K10 |

**3.3 Nouvelles, sur des sous-cas conditionnels (sans exclusion du graphe).**
- Note 225, q = 4 : G ≥ 154 > 126 et P ≥ 924 > 852 ; les 2 types « bits=0 » et « bits=1 » sont sans objet (R2-02).
- k = 18 sous NT : P ≥ 924 > 852, ce qui est redondant puisque k ≥ 22 (R2-11).

---

## 4. Quasi-ratés, triés par écart relatif

| rang | objet | borne requise pour exclure | borne établie | écart | portée | ce qui comblerait | déjà connue |
|---|---|---|---|---|---|---|---|
| 1 | N_Wagner (externe) | ≥ 18 710 | ≤ 18 709 (VER) | 1 unité (0,005 %) ; en défaut : E ≥ 16 forcé contre E ≤ 8 visé | P = 0 seulement | un argument global de stabilité E ≤ 8 (la version ponctuelle « ≤ 4 échecs » est réfutée par un gadget à 5 échecs) | oui (externe, vagues 165-167) — R2-08 |
| 2 | P | ≥ 853 | (T15) donne ≥ 866,25 | 14,25 (1,7 %) | général | prouver (T15), ou seulement : moyenne de t(l) + t(m) > 14,7532 sur les 2079 drapeaux | oui (15/10) — R2-06 |
| 3 | P | ≥ 853 | (T8)/(NG5)/(N9-NG) donnent ≥ 924 | 72 (8,5 %) | général | prouver l'une des trois | oui (15/10) — R2-06 |
| 4 | a₁₀ | ≤ 34 417 (si N16, N18) | ≤ 7920·c₂₀ ; c₂₀ = 4 donne 31 680 | 8,6 % (9,0 % avec 34 524) | rang 37 | N16, N18 au rang 37 et c₂₀ ≤ 4 | oui (NOTE 17.100) — R2-05 |
| 5 | plafond par paire jumelle non-grille | ≤ 27 142 | 31 976 (C) | il faut 15,1 % de moins | rang 37, ρ = 0, avec N14 | plafond raffiné et masses 7 à 9 bornées ; avec N16 hypothétique, seuil 33 780 > 31 976 mais refusé comme exclusion | oui (NOTE 17.96) — R2-07 |
| 6 | G, P | — | q = 3 : G ∈ [121, 126], P ∈ [726, 762] | fenêtre de largeur 5 sur G (4 %) | sous-cas de la note 225 | un raffinement local du sous-cas | non (lien nouveau) — R2-02 |
| 7 | plafond par paire non-grille | ≤ 25 201 | 31 976 | 21 % | rang 37, ρ = 0, sans N14 | idem 5 | oui (17.45, 17.70) |
| 8 | 3P + 4G | > 2772 | ≥ 2420 | 352 (12,7 %) | branche c ≥ 4 | — (branche fermée par S seulement) | oui — R2-17 |
| 9 | b₄ | plancher > plafond | [3 371 634 ; 14 577 473] | facteur 4,3 | rang 37 avec N14 | relèvement du plancher (collisions) | oui — R2-14 |
| 10 | a₈ | > 6930 | ≥ 1316 si a₉ = a₁₃ = 0 | facteur 5,3 | rang 43 | majoration des normes 18 et 26 | oui — R2-15 |
| 11 | rang_F7 d'un bloc non-grille | ≥ 29 | observé ≥ 30 (données) | marge 1-2 en faveur de l'exclusion, mais sur des données | général | un théorème R7-NG (jugé non crédible) | oui — R2-16 |
| 12 | α | ≥ 21 | ≥ 13 | facteur 1,6 | général | — | oui |

Route close par sa propre marge, pour mémoire : le point mort 13 900 est sous le plancher certifié 16 496 de la
constante par paire de grilles (CARTE §4.E).

---

## 5. Implications par identités exactes

| identité | conséquence chiffrée | déjà connue |
|---|---|---|
| n3 + 3P = 4158 et P ≤ 852 | **n3 ≥ 1602** ; la branche externe n3 = 708 est morte (C-15 à C-21, K4 à K10, O-18) | en partie (NOTE 17.71 : [1599, 4158] flottant) — R2-09 |
| Σ_x \|W(x)\| = 8316 − 6P | Σ\|W\| ≥ 3204, moyenne ≥ 32,36 | oui (L07) |
| H = 213 444 − 3P | hexagones induits ≥ 210 888 ; C6 induits (externe) ≥ 210 888 ; la conjecture de Reimbayev pour 99 (H minimal) équivaut à la non-existence | en partie (L09-COND-056) |
| χ(Σ) = 3P − 4158 | χ(Σ) ≤ −1602 (la source écrit ≤ −705) | non |
| tr(A₄) = 84(n3 − 693) ; h11, z11 ≥ 2n3 ; 12N_cube ≤ 41 580 − n3 | tr(A₄) ≥ 76 356 ; h11, z11 ≥ 3204 ; N_cube ≤ 3331 | non |
| 4·[P − 3G ≤ 693] + 3·[3P + 4G ≤ 2772] | 13P ≤ 11 088 ; P ≥ 840 ⇒ 49 ≤ G ≤ 63 ; P = 852 ⇒ G ∈ {53, 54} | **non** — R2-01 |
| Σ_flags c = 6P, c ∈ {0, 1, 2, 4} | s(x) ≤ 42 + 2g(x), s(x) ≥ 4g(x) | implicite (note C2 08) |
| identité de rang 43 + note 242 + note 192 | **b₂ ≥ 1000** (≥ 1264 avec racine) | **non** — R2-03 |
| identité de rang 37 + N14 + b₃ ≥ 45 964 | 350a₈ + 91a₉ + 13a₁₀ ≥ 448 798 ; a₈ + a₉ + a₁₀ ≥ 1284 | oui (NOTE 17.100, Mandat C) — R2-04 |
| √7·racine de M = vecteur de Fano (b₁ ≤ a₇) | N14 ⇒ b₁ = 0 au rang 37 | oui (NOTE.md:3913) |
| a₁₄ = 5 097 168 − 288a₇ + 98 784b₁ + 343b₂ | a₁₄ ≥ 5 255 634 au rang 37 avec N14 | non (la source donne 5 013 138) — R2-20 |
| A₅ = 1040 + 52G (côté +3) | A₅ ≤ 7592 | non (la source donne ≤ 13 052) |
| r = r_ext + 1 (P) | résultats externes à r_ext ≤ 34 caducs ; W101 donne ≥ 80 110 / 11 400 / 1584 / 182 vecteurs jusqu'à la norme 28 aux rangs 37/39/41/43 | en partie (CARTE §1.6) — R2-10 |

---

## 6. Symétrie forcée

Principe (P, L07-032) : une pièce H d'un graphe asymétrique a au moins |Aut(H)| complétions étiquetées. Une
exclusion de C1 demande une pièce **inévitable** avec |Aut(H)| > #complétions.

| pièce | inévitable | borne inf. sur \|Aut(H)\| | borne sup. sur les complétions | état |
|---|---|---|---|---|
| cadre Φ_x (N[x] et 84 étiquettes) | oui | 645 120 (exact) | **aucune** ; C1 en exige ≥ 63 866 880 | manque la borne sup. « Aucune méthode en vue » (NOTE_ASYM_WINDOW §8). Pour tout Conway, les complétions forment des orbites de taille ≥ 16 sous les 2⁷ flips (R2-13) |
| bord positif de 44 sommets (base de E₋) | oui (trivial) | **aucune** | 1 (V15) | manque une symétrie forcée |
| bord positif de 43 sommets | oui | **aucune** | 2 (V15) ; au rang 37, ≤ 2 choix de signes car a₇ = 0 (vu par R2) | idem |
| instance invariante par deux flips individuels | — | 4 (action libre pour **tout** Conway) | à certifier ≤ 3 | marche pour tout SRG ; aucune instance inévitable de ce type connue ; non appliqué aux 35 gabarits c3 ouverts (R2-13) |
| pièce à trois étoiles N[l] ∪ N[b] (49 sommets) | oui (8316 par graphe) | rigide (1) | 1 | impasse déclarée : l'espace des types est astronomique (NOTE_ASYM_WINDOW §7.4) |
| N[l] (39 sommets) | oui | flip d'une droite plate | non bornée (déficit 8) | non rigide |
| grille | non (G ≥ 0 seulement) | 72 | non bornée (dépendante sur E₋) | non rigide |
| design de Hoffman Y | non (α = 22 non forcé) | par design (29 classes sur 36 sont asymétriques) | inconnue | conditionnel à α = 22 (L07 R33) |
| structure d'une droite | oui (231) | \|Λ\| ≈ 5,87·10¹⁴ réétiquetages | non bornée | non rigide |
| gabarits de racine (S2≀S7) | couverture | stabilisateur ≤ 645 120 | aucune portable (verdicts CP-SAT) | à tester gabarit par gabarit |

**Raison structurelle de l'échec (R2-12, vu par R2, en substance dans NOTE_ASYM_WINDOW §2.2 et §7.3).** Avec
w_v = √7 E₋e_v, un bord positif est un ensemble de w_v indépendants. Or les pièces symétriques connues sont des
supports de vecteurs de ⟨1⟩ ⊕ E₃, donc de relations linéaires entre les w_v :
- N[x] : 4w_x + Σ_{y∼x} w_y = 0 (15 vecteurs de rang 14) ;
- une grille R : Σ_{v∈R} w_v = 0, car (A − 3I)1_R = 1 ;
- une paire de prismes jumeaux : Σ (1_X − 1_Y)_v w_v = 0.

Aucune ne peut donc être, ni contenir, un bord positif. Le théorème V15 ne s'applique qu'à des données recollées de
rang plein, et ces données ne portent aucune symétrie forcée (« forced symmetry dies at the first gluing »).

**Bornes manquantes.**
- Borne supérieure manquante : le nombre de complétions du cadre ou d'une pièce de rang déficient.
- Borne inférieure manquante : |Aut| d'un bord positif inévitable.

Déjà identifié par Codex (Desktop/Recherche_Conway/c1-asymmetry-audit/AGENTS.md:353-355 : « il manque un même bord
inévitable ») et par LAB (NOTE_ASYM_WINDOW, 14/10).

---

## 7. Incohérences entre notes

| # | désaccord | lecture | réf. |
|---|---|---|---|
| 1 | P ≤ 853 (mémoire c1-start.md:217) et N₂ ≥ 1599 (NOTE.md:2754), contre P ≤ 852 et N₂ ≥ 1602 | arrondis de valeurs flottantes ; retenir 852 et 1602 | R2-18 |
| 2 | « au plus 7920 co-Heawood » (BORNE-L10-16) | 7920 bornait a₇ (deux signes), soit ≤ 3960 co-Heawood ; valeur actuelle ≤ 396 | R2-19 |
| 3 | a₇ ≤ 842 : « E » (L02 partie A) contre « flottant » (L06) | retenir H ; dépassé par a₇ ≤ 792 (P) ; a₁₄ ≥ 5 013 138 en dépend | R2-20 |
| 4 | « b₂ ≥ 462 + 85b₁ + b₁²/2, donc b₂ ≥ 968 » (L05-029) | la seconde inégalité est fausse pour b₁ ≤ 4 ; 968 vient de 1000 − 16k ; vraie borne 1000 | R2-21, R2-03 |
| 5 | « ≥ 22 vecteurs de normes 16-20 » (BORNE-L10-13 ; L06 BORNE-13) contre « 1280 de norme 16, ou … » (même NOTE 17.100) | 22 est la version « lignes auditées seules » ; avec b₃, au moins 1280 | R2-04 |
| 6 | a₁₀ ≥ 34 418 (L06-104 ; COND-L10-26) contre 34 523 (Mandat C M:327-332) | planchers b₃ ≥ 45 898 ou ≥ 45 964 ; les deux valides | R2-04 |
| 7 | k = 18 sous NT : P ≤ 1122 (JOURNAL:451) contre P ≤ 1151 (notes/126:144) | 1122 utilise \|T_x\| ≥ 4 ; les deux valides ; hors fenêtre | R2-11 |
| 8 | « sept lignes » (W101) contre « huit valeurs » (W66), remarque de L03a-80 | levé : W101 couvre q = 2..14 (r_ext = 42..30), q = 16 est en W86 | R2-10 |
| 9 | χ(Σ) ≤ −705 (L09) et « caractéristique d'Euler 1485 » (L10) | deux complexes différents (surface Σ à bord, χ = −n3, contre complexe 2079 carrés) | §2.11 |
| 10 | « 2079 moulins » (L07-191) et « 3465 windmills » (NOTE.md:2813) | deux objets : papillons (2 droites) et triplets de droites par un sommet | R2-22 |
| 11 | ρ, τ, H, c, k : plusieurs sens chacun ; lettres de la nuit du 14/10 (son a_k = b_k de l'équipe) | à préciser dans tout croisement | R2-22 |
| 12 | Nuit du 14/10 : τ ≤ 8625/2871, G ≤ 191, P ≤ 1150/1151, c₈ ≤ 360 360, rang ≥ 35 | redécouvertes plus faibles que les bornes du 08/10 ; a₇ ≤ 792 est le seul gain réel | R2-23 |
| 13 | P ≤ 852 étiqueté C ou E selon les notes | déjà tranché : CARTE §8.1 | — |
| 14 | L02 partie A : « ρ ≤ 1330 (méthode polynomiale) ; ρ ≤ ~1500 (Frankl-Wilson) » | sens de ρ non vérifié ; si ce sont des grilles, ces bornes sont très faibles | non tranché |

---

## 8. Vérifications faites aux sources originales

Lectures directes :
- `work/asym_window_2026-10-14/NOTE_ASYM_WINDOW.md`, en entier : les 8316 pièces, et l'impasse du §7.4.
- `work/c1_theta_lp_2026-10-07/NOTE.md`, lignes :
  - 48-72 (tableau des rangs ; b₂ ≥ 1000 sous a₇ = 0) ;
  - 1068-1090 (b₂ ≥ 968) ;
  - 2740-2760 (N₂ ∈ [1599, 4158]) ;
  - 3455-3472 (seuil 25 201) ;
  - 3828-3846 (seuils 27 142 et 33 780) ;
  - 3913-3914 (b₁ ≤ a₇) ;
  - 4060-4112 (identité de rang 37, 447 412).
- `conway99-c2-aws:master:HANDOFF_2026-10-01.md:1455-1475`, formules de rang 37 : par script, COND-03 est une identité.
- `conway99-c2-aws:master:c1_mandat_c_transformations/RECHERCHE_C_TRANSFORMATIONS.md:500-570` : les 4979 vecteurs
  de S₀ ne sont pas indexés par les 4158 non-arêtes, donc il n'y a pas de contradiction.
- Notes Codex de `conway99-c1:origin/codex/c1-arithmetic-audit` : 192 (en entier), 225 (1-160), 242 (1-80).
- Autres notes de `conway99-c1` : `main:notes/126` (128-152) et `main:notes/100` (180-195) ; `main:JOURNAL.md:451`.
- `Desktop/Recherche_Conway/c2_experimental/notes/08_PRISMES_COINS_N3.md`, identité des coins.
- `work/stars_rank_2026-10-14/AUDIT_EXCLUSIONS_2026-10-15.md:40-62, 130-170` et `THREE_RESULTS_2026-10-15.md`.
- `Desktop/Recherche_Conway/c1-asymmetry-audit/notes/RACINE_PONDEREE_2026_10_18.txt:1-75, 275-300`.
- Dépôt externe (`conway99-lab-archive:origin/main:…/conway-99-research/`) : `README.md:380-432` (Wagner, cube) et
  `attempts/README.md:528-556` ; `wave101-all-rank-level7-lp/README.md`.
- `CARTE_MAITRESSE.md` §1.6 : preuve du dictionnaire, recoupée par une dérivation de R2 (7E₋ et J).

Script arithmétique (un processus, quelques secondes) : `scratchpad/r2_checks.py`. Il vérifie :
- la somme des sous-graphes à 4 sommets ;
- la décomposition de 11 088 ;
- les fenêtres q = 1..5 ;
- l'identité COND-03 au rang 37 ;
- 447 412 et 448 798 ;
- a₁₄ ;
- le plafond b₄ ;
- les implications de n3 ≥ 1602.

Greps de redécouverte :
- recherches : « 693 + 3G », « 2079 − 9 », « P − 3G » ; « b₂ ≥ 1000 », « 1264 » ; « 708 » avec « 852 » ;
- périmètre : workspace, `conway99-c1` (toutes les branches), `c1-main-codex`, `c1-asymmetry-audit` et la copie du pont.

---

## 9. Ce qui n'a pas été examiné

- **Lots L11a à L11f** (1277 messages du pont) : réservés à la seconde passe. Seul le pont a été cherché par grep,
  pour b₂ ≥ 1000.
- **PL non relancés.** Aucun PL ni recensement n'a été relancé : calcul interdit ici, et outils non installés. Deux
  tests bon marché sont proposés :
  - la plage de N_Wagner et de N_cube sur le recensement d'ordre 9 à P = 0, pour R2-08 ;
  - les stabilisateurs des 35 gabarits c3 ouverts, pour le filtre de flips (R2-13).
  Chacun coûterait un PL exact ou un parcours de fichiers. Coût non estimé faute de lire les formats.
- **Bornes de C2 sous l'involution** (g⁻, E(v), route C) : non croisées avec C1, puisqu'elles utilisent σ.
- **Côté +3.** Le réseau E de rang 60 (A_k, B_k) n'a pas été comparé aux comptes de vecteurs propres entiers +3 de
  L₃ (rang 54 : normes 12, 14, 16). La normalisation n'est pas vérifiée.
- **Identités des rangs 39 et 41** (constantes du HANDOFF:1465-1468) : seule l'identité du rang 37 a été exploitée.
- **Branche (II) de la dichotomie** (≥ 33 droites c ≤ 2) contre le recensement. Aucune contrainte de t ou g vers le
  haut n'a été trouvée pour c ≤ 2 (c = 1 ⇒ g = 0). Croisement jugé impossible par simple comptage, sans preuve.
- **Tables internes de l'extrémité n3 = 708** (det(B), tr) : caduques par R2-09, donc non lues.
- `assemblage/DOUBLONS_PROBABLES.tsv` et `INDEX_RESULTATS.tsv` : non utilisés systématiquement.
- **Sens de « ρ ≤ 1330 / ~1500 »** (L02 partie A, H:1645, 1670-1671) : non vérifié.
