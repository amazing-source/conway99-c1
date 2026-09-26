# 129 — q:7 : le secteur impair d'une involution (boule impaire, L23 dédoublé, résidu lointain)

*26/09, soir. C1, avec « structures » (NOTE_S27). Branche involution de C2. Mathématiques ; contrôles exacts mod 7 sur
des boules abstraites (`c1_experimental/q7/`). DÉRIVÉ = preuve écrite ; CONTRÔLÉ = vérifié en exact.*

## 0. Énoncés
| énoncé | statut |
|---|---|
| g := rang₇(S − 3I) est pair, g ≤ 20 ; β⁻ est hyperbolique | C2 (Th. B, B′) + « structures » (g ≠ 22) ; rederivé |
| **g ∈ {16, 18, 20}** : dim ker Q_c ≤ 4 (exhaustif) donne g ≥ 14, et la cohérence des digones exclut 14 (§5 bis) | DÉRIVÉ + exhaustif |
| **g = rang₇(T − 3I)**, T = bloc racines × racines (42 × 42) seul | DÉRIVÉ |
| **Boule impaire d'une droite-bloc : rang = 6 + rang₇ Q_c**, Q_c = P_τ − P_η − 2P_π − I | DÉRIVÉ, CONTRÔLÉ 3000/3000 |
| disc(boule impaire) ≡ det Q_c ≡ det L_G⁻ (partie impaire du laplacien de G(L_c)) | DÉRIVÉ, CONTRÔLÉ |
| **L23 dédoublé** : g⁻ = 18 ⟹ (det Q_c \| 7) = −1 ; g⁺ = 18 ⟹ (τ(H_c) \| 7) = +1 | DÉRIVÉ |
| Résidu lointain impair : R_c² = 0, X R_c = 0, rang R_c = g − 18 (bloc générique) | DÉRIVÉ |
| **Critère : l'involution meurt ssi Λ_{T,−4} est 7-isotrope** | DÉRIVÉ (reformulation) |

## 1. Cadre
- σ involution, Fix σ = {x}. Base impaire (forme standard divisée par 2) : ε_o = (e_v − e_σv)/√2 pour les 49 orbites
  (7 blocs c, 42 racines). Z⁴⁹ est unimodulaire impair.
- S = A_impair = [[−I₇, B],[Bᵀ, T]] (convention de C2 : son C est notre Bᵀ). B_{c,o} = ±1 si o passe par le bloc c.
  T_{oo′} = A(v_o, v_o′) − A(v_o, σv_o′) ∈ {0, ±1} : ±1 exactement quand q(o,o′) = 1 ; 0 pour les partenaires D (q = 2).
- S² + S = 12I donne BBᵀ = 12I, **BT = 0** (équilibre : 2 − 2 voisins de c± pour une racine lointaine, 1 − 1 dans
  l'étoile) et T² + T = 12I − BᵀB. Donc T = 0 sur l'espace des lignes de B, et spec T = 0⁷ 3²⁰ (−4)¹⁵.
- N = S − 3I mod 7 : N² = 0, g = rang N. Schur sur les blocs (−4I inversible) : g = 7 + rang(T − 3I + 2BᵀB), et ce
  complément vaut 0 sur les lignes de B et T − 3I sur B^⊥. D'où **g = rang₇(T − 3I)**.

## 2. Arithmétique (rappel ; C2 Th. B/B′, « structures » NOTE_S27, rederivé indépendamment)
- Formule d'oddité pour Λ₋₄⁻ (rang 22, 2-unimodulaire, disc (Z/7)^g), avec le caractéristique projeté :
  22 + 6g + 4[ε⁻ = −1] ≡ 6 + 4E₋ (mod 8). Ici E₋ = #{paires d'orbites (o,o′) : v_o ~ σv_o′} = 42 + M, et M est le
  nombre de paires {o, o′} de racines à T = −1 dans la jauge de « structures » (représentants (a,+)(b,ε)). M est pair,
  par S² + S = 12I.
- Donc g est pair et ε⁻ = (−1)^{g/2}. À g = 22, le déterminant exact 7²² force ε⁻ = +1 : **g ≤ 20**.
- β⁻(Nu, Nv) = u·Nv sur im N a pour discriminant ε⁻ = (−1)^{g/2} : **hyperbolique**. Outil de L23 : une sous-matrice
  principale N_II de rang exactement g a une partie non dégénérée scindée.
- Contrôle : Paley(9) avec x ↦ −x (m = 2, p = 3) donne g = 2, E₋ = 2 et Λ₋₂⁻ = ⟨3⟩ ⊥ ⟨3⟩, conforme.

## 3. La boule impaire d'une droite-bloc
- Coordonnées : X_c = les 12 intérieurs des 6 autres blocs ; U ≅ X_c par w ↦ (c+, w), Ū par w ↦ (c−, w).
  - π = retournement des blocs (w ↦ w̄) ;
  - τ = τ_{c+} (mates dans U ; le m_c de C2) ;
  - h = holonomie U → Ū, et η = π∘h (le π_c de C2). η est une involution sans point fixe, car v ≁ σv hors blocs.
- La boule impaire (19 orbites : 7 blocs + 12 racines de c) a pour matrice [[−4I₇, Cᵀ],[C, P_τ − P_η − 3I]]. La
  colonne c de C est 1, la colonne d ≠ c est e_{d+} − e_{d−}, et CCᵀ = J + I − P_π.
- **Schur** (1/4 ≡ 2) : P_τ − P_η − 3I + 2(J + I − P_π) = Q_c + 2J, avec **Q_c := P_τ − P_η − 2P_π − I**.
  - Q_c 1 = −3·1 et (Q_c + 2J)1 = 21·1 ≡ 0. Donc rang(Q_c + 2J) = rang Q_c − 1.
  - **rang₇ N_boule = 6 + rang₇ Q_c ≤ 18.**
- Le vecteur du noyau est z_c = 3ε_c + Σ_{o∋c} B_{c,o}ε_o. C'est un vecteur propre 3 EXACT de S sur les 49
  coordonnées (« structures »). Son jumeau w_c = −4ε_c + Σ B_{c,o}ε_o est de valeur propre −4, et z_c ≡ w_c.
- **Signe.** Q_c = Q_c|_{1^⊥} ⊥ ⟨−36⟩ et χ₇(−4)⁷ = −1. Si Q_c est inversible, la partie non dégénérée de la boule a
  **disc ≡ det Q_c**.
- **Laplacien.** La partie impaire L_G⁻ du laplacien du graphe cubique G(L_c) donne, par le même Schur,
  det L_G⁻ ≡ 4⁶ det Q_c (mod 7). Kirchhoff pour le revêtement double G(L_c) → H_c = G(L_c)/σ :
  **τ(G(L_c)) = τ(H_c)·det L_G⁻ / 2**.
- **Contrôles** (`q7_ball_check.py`, `q7_laplacian_check.py`, boules σ-invariantes abstraites à τ, η aléatoires) :
  - formule de rang 3000/3000, z_c au noyau 3000/3000, signe 2474/2474 ;
  - identités laplaciennes 300/300 (la première mod 7, la seconde exacte) ;
  - rang 18 dans 82,5 % des cas (81 % chez « structures ») ; parmi eux, χ(det Q_c) = +1 dans 54 %.
- **L20 = L21 ici.** Du côté impair, l'étoile B₁(x) ∪ ét(c) et la boule de L_c coïncident, puisque σ identifie ét(c+)
  et ét(c−). Il n'y a pas de formule 11 − 2e séparée : Q_c porte trois couplages (τ, η, π).
  - Sur un digone de C2 (τ = η, partenaire D qui pivote en c), Q_c vaut −2P_π − I : det (−3)^j, un carré.
  - Sur une paire frère {c, b}, τ = η = π sur le bloc b. Cela détache [[−1,−2],[−2,−1]] (det −3 ≡ 4, un carré).

## 4. L23 dédoublé
Droite-bloc entièrement générique (d(L_c) = 1, donc Q_c inversible et 7 ∤ τ(H_c)).
- Par le Schur de notes/126, en séparant les deux secteurs : g⁻ = 18 + ρ⁻, g⁺ = 18 + ρ⁺, et **k = 22 + ρ⁺ + ρ⁻**.
  Les ρ^± sont les rangs des résidus lointains pair et impair.
- β⁻ scindée : **ρ⁻ = 0 ⟹ (det Q_c | 7) = −1.**
- β⁺ non scindée (ε_g = ε⁺ε⁻) : **ρ⁺ = 0 ⟹ (τ(G)·det Q_c | 7) = (τ(H_c) | 7) = +1.**
- Le produit redonne L23 (k = 22 ⟹ τ(G(L)) non carré) ; à k = 22, il faut maintenant les deux signes.
- **Un bloc générique de det Q_c carré force g⁻ = 20.** Exemple : τ_c = η_c partout (tous les partenaires D des racines
  de c pivotent en c).

## 5. Le résidu lointain impair
- Bloc générique c : P = N_boule (19 × 19, noyau ⟨z_c⟩), X = N_{boule, lointain} (19 × 30), Y = N_lointain.
  - X = PU, puisque Xᵀz_c = 0.
  - R_c := Y − UᵀPU. Alors N ≅ nondég(P) ⊥ R_c et g = 18 + rang R_c.
- **N² = 0 donne exactement R_c² = 0 et X R_c = 0.**
  - Calcul : P² + XXᵀ = 0, PX + XY = 0, XᵀX + Y² = 0 ⟹ XR = −(P² + PUUᵀP)U = 0, puis R² = Y² + XᵀX = 0.
  - C'est l'analogue impair de MR = 0 (notes/102 §8).
  - im N ∩ F^{lointain} = im R_c.
- **g = 18 (étoile complète impaire).** R_c = 0 pour tout bloc générique. On pose G′ := im N ∩ F^{racines} (le
  β⁻-orthogonal de ⟨z_c⟩, de Gram 3I₇), de dimension g − 7 = 11.
  - La restriction ρ_c : G′ → {φ sur ét(c) : φ·b_c = 0} est un isomorphisme.
  - La forme β s'y lit β(u, v) = ρ_c(u)ᵀ Q_c⁻¹ ρ_c(v).
  - Pour deux blocs génériques c, d, ρ_d ρ_c⁻¹ est donc une isométrie. Elle envoie la colonne y de Q_c + 2J sur :
    - la colonne y de Q_d + 2J si y ∈ ét(c) ∩ ét(d) ;
    - sinon sur l'ombre réduite s̃_y^{(d)} = s_y + 2Σ_i a_i(e_{d_i+} − e_{d_i−}), où s_y est l'ombre de y sur ét(d)
      (deux +1, deux −1).
  - D'où, pour y, y′ ∈ ét(c) ∖ ét(d) : **s̃_yᵀ Q_d⁻¹ s̃_y′ ≡ (Q_c + 2J)[y, y′]**, et en particulier s̃_yᵀQ_d⁻¹s̃_y ≡ 1.
    Il y a 55 conditions par couple ordonné (c, d) : le système est surdéterminé.
  - Avec le signe : (det Q_c | 7) = −1 pour les 7 blocs.
- **g = 20.** Pour chaque bloc générique c, G′ (dim 13) = W_c ⊥_β K_c, où :
  - W_c = ⟨g_y : y ∈ ét(c)⟩ (11 dimensions, β ≅ Q_c|_{1^⊥}) ;
  - K_c = G′ ∩ F^{loin de c} = im R_c (2 dimensions, β non dégénérée, disc ≡ det Q_c, totalement isotrope pour la forme
    standard).
  - Les vecteurs de K_c sont des vecteurs propres 3 de T mod 7, portés hors de l'étoile de c et équilibrés contre les
    ombres (Σ u_f s_f = 0). C'est l'analogue impair de la « torsion équilibrée ».

## 5 bis. Torsion impaire et mineurs principaux
- **L21 impair raffiné (tout bloc c).** Soient t_c = dim ker Q_c (torsion impaire de la boule ; noyau de la boule =
  ⟨z_c⟩ ⊕ relevés de ker Q_c) et r₀_c la dimension de la torsion **équilibrée** : φ ∈ ker Q_c avec s̃_f·φ = 0 pour les
  30 orbites lointaines f. La congruence par blocs de notes/126 donne :
  **g = 18 + t_c − 2r₀_c + ρ_c**, avec ρ_c ≥ 0.
  - Avec g ≤ 20 : t_c − 2r₀_c + ρ_c ≤ 2 pour tout c.
  - **Sous « NT impair » (r₀_c = 0) : un bloc avec dim ker Q_c ≥ 3 tue l'involution** ; dim ker Q_c ∈ {1, 2} force
    g = 20.
  - Comme en notes/126 §2, Σ_f (s̃_f·φ)² ≡ 0 est automatique pour φ ∈ ker Q_c, car Σ_f s̃_f s̃_fᵀ = −(Q_c + 2J)² ≡ −Q_c² − J.
    L'équilibre est une condition de plus (30 équations).
  - La torsion impaire est un cas de la torsion de C1 : 7 | det L_G⁻ ⟹ 7 | τ(G(L_c)).
- **Borne exhaustive : dim ker Q_c ≤ 4, donc g⁻ ≥ 14.**
  - Borne de boule : rang Q_c − 1 = 11 − t_c ≤ rang M_R = g − 7, soit g ≥ 18 − t_c pour tout bloc c.
  - Énumération de tous les couples (τ, η) d'involutions sans point fixe sur X_c (`code/x36c_q7_qc_nullity.py`) :
    - 11 classes de τ à Aut(X_c, π) près, et les 10 395 η pour chacune ;
    - **t_c ≤ 4**, et t_c = 4 n'arrive que si π ∪ τ_c a au moins 2 digones (types (2⁶), (2⁴,4), (2²,4²)) ;
    - un digone au bloc d signifie τ_c(d+) = d−, c'est-à-dire une arête sœur de type m en c (ou une paire frère).
  - Donc **g⁻ ∈ {14, 16, 18, 20}**, ce qui améliore le g⁻ ≥ 12 d'Astra (dossier 6, par Blichfeldt).
  - **Cas de réserve** (tous les Q_c singuliers) : g = 18 + t_c − 2r₀_c + ρ_c.
    - g = 16 impose t_c ≥ 2 et r₀_c ≥ 1 + t_c/2 en tout bloc : au moins 2 vecteurs de torsion impaire équilibrés
      partout.
    - g = 14 impose t_c = 4 et r₀_c = 4 en tout bloc (torsion maximale, entièrement équilibrée), donc au moins
      2 digones en chaque bloc : 2|Σ| + #{n_s = 1} ≥ 14.
    - « NT impair » tuerait les deux.
  - **g = 14 est exclu** (DÉRIVÉ + exhaustif, `code/x36d_q7_t4_patterns.py`).
    - Si t_c = 4, alors η_c n'a aucun digone et τ_c en a 2, 4 ou 6 (motifs (2,0,0), (4,0,0), (6,0,0) seulement).
    - Or « η_c a un digone en d » et « τ_d a un digone en c » disent tous deux {c+, d+} ~ {c−, d+}. C'est le
      « m en un bout, π en l'autre » de C2.
    - À g = 14, t_c = 4 dans les 7 blocs. Un digone de τ_c en d donne un digone de η_d en c, donc t_d < 4.
      Contradiction.
    - **Donc g⁻ ∈ {16, 18, 20}.**
  - **g = 16** : t_c ≥ 2 dans les 7 blocs et r₀_c = 1 + (t_c + ρ_c)/2.
    - La cohérence des digones ne l'exclut pas : t = 2 existe sans aucun digone.
    - La torsion impaire n'est jamais rationnelle, car toute composante de G(L_c) est σ-invariante (les mates d± de X_c
      sont adjacents). L'équilibre est donc une vraie condition 7-adique.
- **Mineurs principaux (version Seidel, cf. notes/102 §7).** Pour tout ensemble I d'orbites :
  - rang₇ (S − 3I)_II ≤ g ≤ 20. Donc **det (S − 3I)_II ≡ 0 dès que |I| ≥ 21** ;
  - pour |I| = 20, det ≡ 0 ou un carré non nul (β⁻ scindée de dim 20) ;
  - à g = 18, les mineurs d'ordre 19 et 20 sont nuls et ceux d'ordre 18 sont nuls ou non carrés.
  - Même énoncé avec Σ⁻ = −I − 2S, puisque S − 3I ≡ 3Σ⁻ (mod 7) et que 3²⁰ est un carré.

## 6. Reformulations
- **Λ₋₄⁻ ⊗ Z₇ = ⟨w_c⟩ ⊥ Λ_{T,−4}**, avec Λ_{T,−4} = {r ∈ Z⁴² : Br = 0, Tr = −4r}, de rang 15. Le recollement des
  w_c (projections −a_c/4) est 2-primaire. ⟨w_c⟩ ≅ ⟨28⟩⁷ = 7·⟨4⟩⁷.
  - Donc g − 7 = rang₇ disc(Λ_{T,−4}), qui est impair.
- rang₇ Gram(Λ₋₄⁻) = 22 − g ∈ {2, 4, …, 14}. **L'involution meurt ssi tout vecteur propre −4 entier et impair f
  vérifie Σ_o f_o² ≡ 0 (mod 7)**, c'est-à-dire ssi Λ_{T,−4} est 7-isotrope (polarisation, 2 inversible).
- **Repère ajusté.** C'est la partie impaire des 99 droites équiangulaires de notes/102 §7 : Σ⁻ = −I − 2S vérifie
  Σ⁻² = 49I.
  - 3I − S est le Gram de 49 vecteurs de R²² : 7 de norme 4, 42 de norme 3, de produits 0 ou ±1.
  - (3I − S)² = 7(3I − S) : c'est un repère ajusté de constante 7.
  - Le réseau engendré est (Λ₋₄⁻)*(7), de déterminant 7^{22−g} ≥ 7².

## 7. Pistes et partage (avec « structures »)
- (a) « structures » et C2 : filtre linéaire N_II sur les squelettes à Q entier (queue AD, squelettes dis). I est un
  ensemble d'orbites sans paire dis à q = 1 ; on tue si le rang est ≥ 21, ou vaut 20 avec une partie non scindée, ou
  contredit le signe imposé par det Q_c.
- (b) C1, à la main : l'étoile complète impaire à g = 18 (§5), puis K_c à g = 20.
- Limite honnête : tout S entier avec S² + S = 12I et la structure locale donne automatiquement g ≤ 20. Une borne
  g ≥ 21 doit donc s'appuyer sur une partie seulement des contraintes (locales plus un morceau du lointain). C'est la
  même frontière que (a′) et R_L de notes/102 §8.

## 8. Lien avec le lemme de l'étoile libre de C2 (note 20 du labo C2)
- **Dictionnaire.** Le μ de C2 est notre τ (mates dans U) et son τ notre η ; σ = π. Les ombres de C2 s'écrivent
  s_z = 1_{Φ(z)} − 1_{Φ(−z)}, et s̃_z = v_z − v_{−z}, avec v_z = 1_{Φ(z)} + 2·1_z. Le problème local RSF(star(c))
  détermine donc t_c et r₀_c.
- **Contrainte q:7 locale** (elle vient du genre, pas de λ/μ) : t_c − 2r₀_c ≤ 2. Un bloc à t_c ≥ 3 exige un
  φ ∈ ker Q_c avec F(z) := φ(Φ(z)) + 2φ(z) σ-invariant mod 7 sur les 30 orbites lointaines. Les combinaisons
  agrégées Σ_{z∋a} sont automatiques pour φ ∈ ker Q_c : ce sont les équations individuelles qui comptent.
- **Table par cube** (`code/x36e_q7_cube_table.py`, tous les η libres). A111111 (μ = σ) n'a jamais t = 0 avec
  det non carré.
- **A111111 en forme close.** Q = −(I + P_σ + P_τ) sur des cycles alternés de longueur 2ℓ, de valeurs propres
  −(1 + ζ + ζ⁻¹). On a t = 2·#{orbites avec 3 | ℓ}.
  - Type (6) : t = 2.
  - Type (3,3) : t = 4, donc torsion équilibrée exigée.
  - Types (4,2) et (2,2,2) : det ≡ 2 et 1, des carrés, donc g⁻ = 20 forcé.
  - Identité entière : Σ_z (s̃_z·φ)² = 49|φ − σφ|²/2 pour φ entier de ker Q.
