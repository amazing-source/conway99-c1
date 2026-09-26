# 131 — Alt : entrelacement et rang de K ; résidus lointains réels contre q:7 ; au plus un bloc A111111

*26/09, nuit. C1, branche involution (C2), en appui du cœur « étoile totalement libre » signalé par « structures »
(μ_c ∩ τ_c = ∅, aucun pivot en c). Mathématiques ; DÉRIVÉ = preuve écrite.*

## 0. Énoncés
| énoncé | statut |
|---|---|
| **Rang de K ≤ 14** : K_YP = (φ_P₀(Y) − φ_P₁(Y))/2 (21 × 21, niveau paires) ; Q_A a la valeur propre 3 avec multiplicité ≥ 6 | DÉRIVÉ |
| Décomposition : rang K = r, a₃ + s₃ + r = 20, a₋₄ + s₋₄ + r = 15, s₋₄ = a₃ − 6 | DÉRIVÉ |
| **Résidu lointain réel** (côté impair, bloc c) : 4\|r_f\|² = 10 − w_fᵀ M_c⁺ w_f, avec w_f = 4s_f + δ_f et M_c ≡ −4Q_c − J (mod 7) | DÉRIVÉ |
| À t_c = 0 : **g⁻ = 18 ⟺ G_r ≡ 0 (mod 7)** ; g⁻ = 20 ⟺ rang₇ G_r = 2 (G_r = 7P₄, P₄ projecteur réel de rang 4) | DÉRIVÉ |
| **Au plus un bloc A111111** (τ_c = π) quand Σ = ∅ ; un tel bloc force un digone π de η_B en c pour tout autre bloc B | DÉRIVÉ |

## 1. Entrelacement dans Alt (secteur pair)
- V₃₅ := ker B⁺ ∩ 1^⊥ est Q-invariant, avec Q² + Q = 12I, donc le spectre de Q y est 3²⁰(−4)¹⁵ (notes/130 §7 pour le cadre).
- Alt = ⟨a_P⟩ (21 dimensions) est contenu dans V₃₅, car a_P ⊥ 1 et a_P ⊥ lignes de B⁺. De même Sym′ = Sym ∩ V₃₅ (14 dimensions).
- **Cauchy** pour la compression Q_A de Q|V₃₅ à Alt :
  - λ_i(Q_A) ≥ λ_{i+14}(Q|V₃₅) = 3 pour i ≤ 6, donc λ₁ = … = λ₆ = 3 ;
  - λ₂₁(Q_A) ≤ λ₂₁(Q|V₃₅) = −4, donc λ₂₁ = −4.
- Sur ker(Q_A − 3) ∩ Alt, on a Q v = 3v, donc la composante Sym′ K v est nulle. Plus généralement
  KᵀK = −(Q_A − 3)(Q_A + 4).
- En écrivant V₃₅ = (ker Kᵀ) ⊕ (ker K) ⊕ (partie mixte de dimension 2r) :
  a₃ + a₋₄ = 21 − r, s₃ + s₋₄ = 14 − r, et dim E₃ = a₃ + s₃ + r = 20. D'où s₋₄ = a₃ − 6 ≥ 0 et **r ≤ 14**.
- K est entièrement au niveau paires. La borne est une contrainte de rang, invisible au PL par paires.
  - Sur les solutions par paires du K₃ ancré, rang K = 9 : elle ne mord pas.
  - À tester sur les résidus riches en dd de « structures ».

## 2. Résidus lointains réels et q:7 (côté impair)
- Gram 3I − S : 49 vecteurs de ℝ²², tous de norme 3 ou 4, formant un repère serré de constante 7 (notes/129 §6).
- La boule impaire d'un bloc c (19 coordonnées) est de rang 18 (« structures »). Les 30 orbites lointaines ont donc des résidus
  r_f ∈ ℝ⁴, avec Σ r_f r_fᵀ = 7I₄. Leur Gram G_r = 3I − T_FF − Z_R vérifie G_r² = 7G_r.
- **Calcul exact.**
  - Bloc de la boule 4I₇, et C x_B = −δ_f pour f lointaine (δ_f = 1_z − 1_{−z}).
  - Le complément de Schur de la partie racines est M_c/4, avec M_c = 11I − 4P_τ + 4P_η + P_π − J (noyau 1).
  - D'où (Z_R)_ff = 1/2 + w_fᵀM_c⁺w_f/4, avec w_f = 4s_f + δ_f, et **4|r_f|² = 10 − w_fᵀ M_c⁺ w_f**.
  - M_c ≡ −4Q_c − J (mod 7). Donc, si t_c = 0, M_c⁺ n'a pas de 7 au dénominateur et Z_R est 7-entier.
- **Conséquences.**
  - G_r ≡ −R_c (mod 7), où R_c est le résidu de notes/129 §5. Donc rang₇ G_r = g⁻ − 18.
  - Si g⁻ = 18 : chaque \|r_f\|² ∈ [0, 3] est ≡ 0 7-adiquement, et Σ_f \|r_f\|² = 28. Si le dénominateur de M_c⁺ divise 4, alors
    \|r_f\|² ∈ {0, 7/4}, avec exactement 16 orbites à 7/4.
  - Test local net, à évaluer sur toute solution locale (μ, τ, Φ).
- Côté pair, même principe (repère serré de constante 14 dans ℝ⁴, « structures »), avec g⁺.

## 3. Au plus un bloc A111111 quand Σ = ∅
- τ_c = π signifie (c+, b) ~ (c+, b̄) pour toute étiquette b.
- Vu du bloc B, c'est h_B(c+) = c+, soit η_B(c+) = c− : un digone π de η_B au bloc c, pour tout B ≠ c.
- Si c′ est aussi A111111, alors τ_c′(c+) = c− et η_c′(c+) = c−. La paire cc′ est donc frère, ce qui est exclu quand Σ = ∅.
- Autres conséquences d'un bloc A111111 :
  - toutes les paires par c ont n_s = 1, et leurs partenaires D sont dis ;
  - en tout autre bloc B, η_B a un digone π, donc t_B ≤ 3 (notes/129 §5 bis : t = 4 exige η sans digone π).
- Dans le cube A111111 de type (2,2,2), G(L_c) a trois composantes à 4 étiquettes, comme les droites (4,4,4) de notes/128.
  - Le lemme R de notes/128 ne s'y transpose pas directement : il suppose P = 0, alors qu'ici τ_c = π est le cas P maximal.
  - L'argument d'équilibre qu'il utilise (celui du lemme de la queue) reste disponible.

## 4. Carte : où q:7 donne un filtre orbite par orbite sur une solution locale (μ, τ, Φ)
On part de g = 18 + t_c − 2r₀ + ρ, avec g⁻ ∈ {16, 18, 20} (notes/129).
- « Filtre Z » : T_FF ≡ Z, donc Z_ff ≡ 0 pour les 30 orbites lointaines, et Z_ff′ ∈ {0, ±1}.
- « Filtre torsion » : un φ ≠ 0 de ker Q_c vérifie s̃_f·φ ≡ 0 pour les 30 orbites. Pour φ fixé, c'est linéaire en Φ.

| t_c | g⁻ = 16 | g⁻ = 18 | g⁻ = 20 |
|---|---|---|---|
| 0, det carré | impossible | impossible (L23 dédoublé) | ρ = 2 : **pas de filtre** (seulement l'existence de K, rang 2 anisotrope) |
| 0, det non carré | impossible | ρ = 0 : **filtre Z** | ρ = 2 : pas de filtre (K hyperbolique) |
| 1 | impossible | r₀ = 1 : **filtre torsion** | ρ = 1 + 2r₀ : pas de filtre |
| 2 | r₀ = 2 : torsion totale | r₀ ≥ 1 : **filtre torsion** | r₀ = 0 et ρ = 0 (**filtre Z**, forme à torsion) ou r₀ = 1 (**filtre torsion**) |
| 3 | r₀ = 3 | r₀ ≥ 2 | r₀ ≥ 1 : **filtre torsion** |
| 4 | r₀ ≥ 3 | r₀ ≥ 2 | r₀ ≥ 1 : **filtre torsion** |

**Conséquences.**
- Les types à t_c ≥ 3 ont toujours un filtre torsion. Premier test proposé à « structures » : A111111 de type (3,3), t = 4, 17 orbites
  de φ projectifs dont 14 mixtes (`data/A33_torsion_reps.json`). Si l'ILP RSF + filtre est infaisable pour tous les φ, un tel bloc
  est impossible.
- Le cas dominant chez les ÉTL (t = 0, det carré : 52 % des couples) force g⁻ = 20 et ne donne **aucun** filtre orbite par orbite.
  Il ne reste que l'existence du plan anisotrope K_c : environ 42 équations quadratiques (diagonale, paires D lointaines,
  isotropie) pour environ 24 inconnues. On ne peut l'évaluer qu'avec une vraie solution locale, et aucune n'est connue à m = 7.
- Dès qu'un bloc force g⁻ = 20 (bloc plein, ou ÉTL à det carré), les blocs à t = 2 sans torsion équilibrée deviennent rigides
  (ρ = 0).

## 5. Composantes canoniques d'un bloc plein : aucune torsion 7 (calcul exact)
- À un bloc plein (τ_c = η_c), un D-cycle de longueur ℓ donne une composante canonique de G(L_c) : 6ℓ sommets, cubique, avec
  les étiquettes sur un cycle alterné π/μ. Pour ℓ = 1, c'est le prisme frère.
- Calcul exact (`code/q7_fullpivot_components.py`), pour ℓ = 1 à 6 : **le noyau mod 7 du laplacien est réduit aux constantes**
  (pair : 1, impair : 0). Il n'y a donc aucune torsion 7, ni paire ni impaire.
- Conséquences en un bloc plein à m composantes :
  - d(L_c) = m exactement, t_c = 0, et les différences de composantes sont équilibrées ;
  - **g⁻ = 20 et g⁺ = 19 − m + ρ⁺** ; en particulier ρ⁺ ≥ m − 1 dès qu'un bloc générique a g⁺ = 18 + ρ⁺_b.
- Aucune contradiction : q:7 n'apporte rien de plus en un bloc plein, sauf à le combiner avec des données lointaines (plan K_c).

## 6. Deux blocs pleins formant une paire frère : une obstruction q:7 sur le bloc croisé (candidate)
**Cadre.** c et d sont deux blocs pleins (τ = η), et cd est une paire frère. C'est le cas des puits de K₃ ancré (trois puits deux
à deux frères), de K₂ ancré (puits 5, 6) et de 2K₂ ancré. Le puits de 3K₂ est seul, donc non concerné.

**Réduction exacte.**
- c plein ⟹ g⁻ = 20, t_c = 0 et ρ_c = 2 : le résidu R_c = K r Kᵀ est de rang 2, avec r anisotrope (det Q_c ≡ 1).
- d plein ⟹ T = 0 sur D := étoile(d) ∖ étoile(c) (10 orbites (d, y), y ∈ R = les 10 étiquettes des 5 autres blocs). Donc
  (R_c)_DD = −Z^(c)_DD.
- Avec Q_c⁻¹ = 5I + 4P_π et des ombres nulles sur d± (T passe par d, où il est nul), on trouve
  **M_D := Z_DD ≡ I − J + 2P_π + Rmᵀ(5I + 4P_π)Rm (mod 7)**, où Rm = Σ + 2(I − P_π).
- Ici Σ_{w,y} = T_{(c,w),(d,y)} est le **bloc croisé** : entrées 0/±1, **deux +1 et deux −1 par ligne et par colonne** (ombres
  à 4 entrées non nulles).
- Conditions nécessaires :
  - (a) rang₇ M_D ≤ 2 et M_D = −K_D r K_Dᵀ ; donc (M_D)_yy ≡ 0 impose que la ligne y de M_D soit nulle ;
  - (b) version réelle : G_D := 3I − (Z_R)_DD, avec 4G_D = 11I − J + P_π − W_Dᵀ M_c⁺ W_D, est PSD de rang ≤ 4 (bloc principal
    de 7P₄). On a toujours G_D·1 = 0, calcul exact ;
  - (c) les mêmes conditions en d (Σ transposée) ;
  - (d) dichotomie de la paire {d, Y} : au plus 2 lignes w où les colonnes sœurs y+ et y− sont toutes deux non nulles. De même
    pour les lignes sœurs.

**Indices (calculs, pas une preuve).**
- 20 000 Σ tirées au hasard avec le bon motif de lignes et de colonnes : rang₇ M_D ∈ {7, 8, 9}, jamais ≤ 2.
- Recuit avec des échanges qui conservent les comptes : minimum trouvé rang₇ M_D = 6 (deux graines), et rang(M_D) + rang(M_C) ≥ 12.
- G_D n'est **jamais PSD** sur 3 000 Σ aléatoires (valeur propre minimale entre −3,6 et −0,36). La direction négative est
  surtout impaire : G_D restreint aux vecteurs impairs n'est pas PSD dans 97 % des cas.
- Mécanisme probable : sur les vecteurs impairs,
  4vᵀG_Dv = 10|v|² − (4/3)|Π_eΣv|² − (1/10)|4Π_oΣv + 2v|².
  - La positivité exige des colonnes sœurs presque égales (Σv petit pour v impair).
  - La dichotomie (d) interdit justement le recouvrement des colonnes sœurs : au plus 2 lignes communes.

**Énoncé candidat.** Aucun bloc croisé Σ ne satisfait (a)–(d). Donc **deux blocs pleins ne forment jamais une paire frère**, ce qui
tuerait d'un coup K₃, K₂ et 2K₂ ancrés.
- Le DFS exhaustif naïf (`code/q7_twosink_exhaust.py`) ne finit pas en 5 min.
- Il faut exploiter la symétrie B₅ × transposition et la dichotomie, ou, par configuration, fixer |Σ| au niveau paires : il ne
  reste alors que les signes.

## 7. Orbites lointaines rigides en un bloc plein, et mort de 3K2_or14 par q:7 (à relire)
**Mécanisme (DÉRIVÉ).** Soit c un bloc plein. Alors t_c = 0 et det Q_c ≡ 1, d'où g⁻ = 20 ; de plus R_c = K r Kᵀ avec r
**anisotrope**.
- Pour toute orbite lointaine f, r(k_f, k_f) = T_ff − Z_ff = −Z_ff. Donc **Z_ff ≡ 0 ⟺ k_f = 0**.
- Dans ce cas la ligne de f dans R_c est nulle, et **T_{f,f′} ≡ Z_{f,f′} (mod 7) pour toutes les orbites lointaines f′**. La ligne de
  f est entièrement fixée par les ombres au bloc c. On dit que f est **rigide**.
- En un bloc plein, Z_{f,f′} = 3δ + 5(BᵀB) + s̃_fᵀ(5I + 4P_π)s̃_{f′}, avec s̃ = s + 2δ.
- Pour une orbite frère u disjointe de c : Z_uu ≡ 4 s_u·πs_u. **u est rigide ⟺ son ombre n'a pas deux étiquettes d'un même bloc**
  (ou en a deux paires de produits opposés).

**Application à 3K2_or14.** Puits 2 plein, de profil (4,4,4) ; paires frères A = {0,4}, B = {1,3}, C = {5,6}. C'est l'unique choix D.
1. **(MILP, niveau paires : sib_model + identités Alt, 48 cas, `code/motifs/k3k2_types.py`)** Chaque orbite frère a φ = 1 sur
   chacune des 4 paires puits {2, m} hors de sa paire. Imposer φ ∈ {0, 2} est infaisable dans les 48 combinaisons.
   - Donc chaque ombre frère sur étoile(2) a une étiquette par bloc, et les **6 orbites frères sont rigides**.
   - Par 8.1, l'ombre de la sœur occupe les étiquettes complémentaires.
2. **(À la main)** Contraintes sur les lignes frères :
   - sœurs : T = 0 (paire D), donc Z_{uu′} ≡ 0 ;
   - entre deux paires frères : T est une permutation signée (8.1), donc Z ≡ ±1 sur la permutation et 0 ailleurs.
   - Énumération : 384 couples d'ombres sœurs par paire frère, et **512 affectations complètes** des 6 ombres.
3. **(Énumération, `code/q7_3k2_sibrows.py`)** Orbites croisées f, c'est-à-dire des paires A–B, B–C et C–A (24 orbites).
   - Équilibre au puits : l'ombre de f sur étoile(2) a 1 étiquette dans chacun des deux groupes que f rencontre et 2 dans le
     troisième, avec deux +1 et deux −1 (576 options).
   - Par 8.1, T_{u,f} = 0 pour les deux orbites de chaque paire frère que f rencontre, et T = ±1 pour exactement une des deux
     orbites de l'autre paire frère.
   - Lignes rigides : ces valeurs doivent être ≡ Z_{u,f}.
   - **Pour chacune des 512 affectations, AUCUNE orbite croisée n'a d'ombre admissible** (0 option sur 576, pour les 24 orbites).
     La cause principale : Z_{u,f} ≢ 0 là où 8.1 impose T = 0.
- **Conclusion (sous réserve de relecture) : 3K2_or14 est impossible.** Le modèle U de C2 (secteur pair seul) le trouvait
  faisable : c'est l'information 7-adique impaire qui tue.
- Points à relire indépendamment :
  - la formule de Z (notes/129 §8, re-dérivée ici par élimination par blocs) ;
  - l'anisotropie de K_c (disc K_c ≡ det Q_c, et β⁻ scindée à g = 20) ;
  - les conventions de signes (B, δ, représentants) dans le code ;
  - l'étape 1 (forçage par MILP, à certifier en exact).

### 7 bis. Étape 1 fermée (26/09, fin de nuit) : 24 certificats exacts + 24 cas tués par q:7
- **Certificats de C2** (certify.py de « structures », Farkas exact revérifié par check ; c2-experimental 8cb71a0) : les
  24 cas « paire frère X sur les blocs du groupe PRÉCÉDENT » sont morts au niveau paires. Le cycle est A → B → C → A, avec
  A = {0,4}, B = {1,3}, C = {5,6} ; le précédent de A est C.
- **Les 24 autres cas** (X sur le groupe SUIVANT) résistent à certify.py : le PL est trop faible, HiGHS conclut par ses coupes.
  On les tue par q:7, sans l'étape 1 (`code/q7_3k2_ext.py`) :
  - une orbite frère de type (2,0) sur le groupe suivant a les deux étiquettes d'un bloc m. Alors Z_uu ≡ s_{m+}s_{m−} = ±1 :
    elle n'est pas rigide, et k_u est sur le cercle de norme −Z_uu (r = I, anisotrope) ;
  - la sœur occupe les étiquettes complémentaires, donc est aussi de type (2,0) ; on impose T_{uū} = Z_{uū} + k_u·k_ū ≡ 0 ;
  - options par paire frère : 1 664 (dont 1 280 non rigides), contre 384 en type perm seul ;
  - entre deux paires frères, 8.1 impose une permutation signée pour Z + k·k. **Aucune option (2,0) n'est compatible avec
    aucune option de la paire frère suivante** : il reste exactement les 2 048 couples perm–perm par couple de paires, donc
    les mêmes 512 affectations, toutes tuées par les orbites croisées (§7).
  - Mécanisme observé : la ligne de l'orbite (2,0) contre les deux orbites de la paire suivante a toujours un résidu hors
    de {0, ±1}, ou deux entrées non nulles.
- **Contrôles** :
  - en mode « perm seul », le code étendu redonne exactement 384, 2 048, 512 et 0 survivant ;
  - version scalaire contre version vectorisée : 0 écart sur 9 000 tirages.
- **Donc l'étape 1 tient en entier, et 3K2_or14 est impossible**, sous réserve d'une relecture indépendante de q7_3k2_ext.py.
