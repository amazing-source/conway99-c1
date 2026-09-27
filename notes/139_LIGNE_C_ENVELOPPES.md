# 139 — Ligne d'arrivée (C) : les 156 enveloppes unimodulaires, outils uniformes et premières exclusions vérifiées

*27/09, après-midi. C1. Route globale « réseaux × 7 blocs » issue du dossier de Sol (external_inputs/CONWAY_ASTRA_27_09_2026_0836 chez
C2). Si les 156 enveloppes tombent, TOUT le cas involution tombe, sans types de blocs. DÉRIVÉ = preuve écrite ; VÉRIFIÉ = relu ou
recalculé par C1.*

## 0. Énoncés
| énoncé | statut |
|---|---|
| Toute involution donne un repère de 51 vecteurs (42 u de norme 3, 7 h de norme 4, 2 y de norme 7) dans un réseau U unimodulaire impair de dim 24 et de min ≥ 2, avec Σ v⊗v = 7I (F) | VÉRIFIÉ (C1 et « structures », indépendamment) |
| Les candidats U sont les **156** réseaux de la Table −4 de Borcherds (thèse, arXiv math/9911195), dans `data/borcherds_odd24.json` | calcul exact ; nombre de racines = 8(h₁ + h₂ − 2) contrôlé, 0 écart |
| 6 exclusions (D≥12 ×3, E8, D8³ ×2) | VÉRIFIÉ (§3) |

## 1. Fondations (relues)
- **N = √7 K₋\***, avec K₋ = ℤ⁴⁹ ∩ V₋, d'où det N = 7^(22−g).
- **B′ de C2** (forme hyperbolique sur F₇⁴⁹/ker N) donne det A_N ≡ (−1)^{g/2}. Donc A_N est anisotrope pour g = 20 et d'indice
  de Witt 1 pour g = 18, et Nmax existe, avec un discriminant anisotrope de dimension 2.
- Le collage avec 7I₂ donne U, unimodulaire impair.
- **min N\* ≥ 8/7.** Un v court donnerait un vecteur propre entier de −4 de norme ≤ 7. Le double compte donne D = m(m − 7) − 7e −
  Σd², puis B² = 2I + 2J, quatre intérieurs, et x₀ contribue 6. Contradiction.
- Il s'ensuit min U ≥ 2, et (F).

## 2. Outils uniformes
- **(M) Minuscule.** Pour toute racine r de U et tout x de norme 3, |(r,x)| ≤ 1, sinon x ∓ r serait de norme 1.
  - La projection de x sur chaque composante de racines est donc 0 ou un poids minuscule.
  - E8 n'en a pas d'autre que 0.
- **(P) Piège.** Soit w réel avec |w|² < 8/7 et (w,u) ∈ ℤ pour les 42 u. Alors P_N(w) ∈ N\*, de norme < 8/7, donc P_N(w) = 0 et
  w ∈ N⊥, qui est de dimension 2.
  - Les duaux courts des composantes (axes de D_n de norme 1, poids ω₁ de A_n de norme n/(n+1), et leurs sommes de norme < 8/7)
    doivent donc être « touchés » par les classes de glue des u, sauf dans un plan.
- **(E) Énergie caractéristique.** On utilise les théorèmes thêta de Sol : #χ₈ = 48 + r et Σχχᵀ = (16 + r)I − 8Z, avec
  Z = Σ_α αα ᵀ. Ils sont À REVÉRIFIER.
  - Pour chaque χ₈, (χ,u) et (χ,y) sont impairs et (χ,h) est pair. D'où Σ_c (χ,h_c)² + 8·#{|·| = 3} = 12 : **exactement 1 ou 3
    des h ont (χ,h) = ±2**.
  - Pour chaque u, #{χ : |(χ,u)| = 3} = r/4 − n_u, où n_u = #{α : (α,u) = ±1} = 2Σ_i h_i|P_i u|². Donc
    **Σ_i h_i |P_i u|² ≤ h₁ + h₂ − 2** : un u ne peut pas porter plus que la moyenne sur les composantes de grand nombre de Coxeter.
  - Pour chaque h : #{χ : (χ,h) = ±2} = 16 + r − 2hᵀZh ≥ 0.
  - Pour chaque y : #{χ : |(χ,y)| = 3} = 8 + 3r/4 − yᵀZy ≥ 0.
  - Les sommes agrégées sur tous les χ ou toutes les racines sont des IDENTITÉS : elles ne donnent rien. Toute l'information est
    dans l'intégralité vecteur par vecteur.

## 3. Exclusions vérifiées (6 sur 156)
- **D≥12** (ids 151 d₁₂d₈d₄, 153 d₁₂², 155 d₁₆d₈) : G18_G20_D12_COLLAGE relu pas à pas.
  - Branche sans spinor : l'égalité de trace force P_{H0}eᵢ ∈ {0, eᵢ}, alors que Σ_c C_co² = 2. Contradiction.
  - Branche spinorielle : P = D12 + ℤu est unimodulaire et se détache. Chaque h est entièrement dans un facteur (t ∈ {0, 4}), et le
    graphe K₇ met tout dans un facteur de dim ≤ 12, contre N₂₂. Contradiction.
- **E8** (id 152 e₈d₈²) : par (M), toutes les projections des u sur E8 sont nulles, donc span(E8) ⊥ N, et span(E8) ⊂ N⊥ qui est
  de dimension 2. Contradiction.
- **D8³** (ids 145 d₈²d₈, 146 d₈³) : `code/check_d8cube_trap.py`.
  - 135 lagrangiens ; 37 à norme 1, 58 à racines en plus, 8 pairs ; 32 retenus.
  - **Chacun a une composante dont toutes les classes de norme 3 sont vectorielles.** Ses 8 axes tombent donc dans N⊥ par (P).
    Contradiction.

## 4. Suite
- Appliquer (M) + (P) + (E) enveloppe par enveloppe : les candidats u sont les x de norme 3 admissibles pour (E), et leurs
  classes doivent recouvrir les duaux courts, sauf dans un plan. Il faut les glues explicites (« structures » construit les 156).
- **O₂₄** (sans racine) : le piège est vide. Le repère devient un problème fini dans le code de Golay (u = mots signés,
  h = octades signées, CE = −6M, couverture 1/3 des colonnes). C'est le cas le plus dur, à attaquer à la main.
