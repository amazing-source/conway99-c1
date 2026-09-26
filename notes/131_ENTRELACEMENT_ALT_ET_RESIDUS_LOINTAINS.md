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
