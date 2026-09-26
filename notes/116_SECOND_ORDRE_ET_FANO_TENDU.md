# 116 — Identités exactes du second ordre, critère lointain ; le Fano tendu survit au niveau des blocs

*25/09, nuit. Labo c1_experimental, note E3 (détails et scripts). DÉRIVÉ = preuve écrite ; OBSERVÉ = calcul. Les
solveurs (HiGHS via scipy) n'ont servi qu'à tester la faisabilité de systèmes linéaires dérivés à la main, au plus
37 s par appel, avec contrôles. Points 1 à 3 recalculés indépendamment par « structures » : TIENNENT (NOTE_S12 de son
labo, commit 3186d7b, `scripts/verify_c1_p2_far.py` ; contrôles exacts sur Paley 9 et BvLS).*

## 0. Résumé
| résultat | statut | portée |
|---|---|---|
| A_Δ² + A_Δ − 12I = 2J − ∂ᵀ∂ ; sur ker ∂, seules les valeurs propres 3 et −4 | DÉRIVÉ (classique) | tout sommet |
| (P2) : identités de second ordre par blocs ; Σ_z cnt(cnt − 1) = 16 − 2e(R) par bloc | DÉRIVÉ, recalcul indépendant | tout sommet |
| critère lointain (U)/(L), formes closes pour 99 | DÉRIVÉ, recalcul indépendant (contrôle BvLS) | toute droite |
| Fano tendu : comptes exacts, κ, équilibre étiquette, (F5) par variance nulle | DÉRIVÉ, table des g et F5 recalculées | modèle de Fano |
| **Fano tendu : un témoin passe tous les tests de niveau bloc** | OBSERVÉ | *corrigé le 26/09 : ce témoin meurt au niveau des cellules (notes/117 §2 ter)* |

## 1. Le second sous-constituant
- On a A_Δχ_u = 2·1 − χ_u − χ_ū (équations de fentes), où χ_u est l'ensemble des paires contenant u. Donc im ∂ᵀ est
  invariant, avec les valeurs propres 12, 0 (×7) et −2 (×6).
- (A_Δ²)_{yz} vaut λ ou μ, moins le nombre d'étiquettes communes. D'où **A_Δ² + A_Δ − 12I = 2J − ∂ᵀ∂**.
- Sur ker ∂, seules les valeurs propres 3 et −4 : spec Δ_x = 12¹ 3⁴⁰ 0⁷ (−2)⁶ (−4)³⁰.
- Le lemme du triangle (notes/115) est la compression de « A_Δ ⪯ 3 sur ker ∂ ».

## 2. Identités de second ordre par blocs (P2)
On encadre l'identité par des indicatrices de blocs (cnt(z,R) = nombre de voisins de z dans le bloc R) :

  **Σ_z cnt(z,R)·cnt(z,R') = 12|R ∩ R'| − N(R,R') + Σ_{y∈R, w∈R'} (2 − |y ∩ w|).**

Diagonale, en torsion quelconque : Σ_z cnt(z,R) = 48 et **Σ_z cnt(z,R)(cnt(z,R) − 1) = 16 − 2e(R)**, où e(R) est le
nombre d'arêtes internes au bloc (précision de « structures »). En torsion maximale, les seules arêtes internes
possibles sont les σ-arêtes σ_c(v) = v̄ (coïncidences S de L18, non exclues par la torsion maximale). Sans elles,
e(R) = 0 et la somme vaut 16, soit n₂ + 3n₃ + 6n₄ = 8. C'est le cas au Fano tendu, où une telle arête serait interne
à une droite tendue. Contrôle BvLS : e(R) = 4 et diagonale 8 sur ses 55 blocs. Ce sont des sommes de conditions
λ/μ.

## 3. Critère lointain
On part du projecteur caché A_F = B₀ − 7Π₋₄ = B₁ + 7Π₃ (notes/114). Pour 99, Y + 7P = (A_G + 4)⁻¹ sur U^⊥. Soit S un
ensemble de lointains de profil de boule n, et n_⊥ = n − (|S|/6)1. Alors :
- **(U)** 2e(S) ≤ 3|S| + |S|²/12 − n_⊥ᵀ(3I − A_G)⁻¹n_⊥ ;
- **(L)** 2e(S) ≥ −4|S| + |S|²/5 + n_⊥ᵀ(A_G + 4I)⁻¹n_⊥ ;
- contrôle : égalité des deux côtés pour S = F.

Version par blocs : 7·Gram(Π₋₄1_R) est ⪰ 0 et de rang ≤ 8, et 7·Gram(Π₃1_R) est ⪰ 0.

## 4. Le modèle de Fano tendu (notes/115 §5)
- **Comptes génériques exacts** (fermés). Sur les blocs {M,c}, g ∈ {0,1}, avec exactement deux 1.
- **Équilibre étiquette–bloc** (2 voisins par part pour chaque lointain) :
  - automatique pour les blocs de type I ;
  - pour les blocs de type II, 6 équations indépendantes par étiquette.
- **(F5), par variance nulle.** Prenons deux blocs dont les droites se coupent hors des deux. La diagonale de (P2)
  donne Σ(g − 2)² = 0 sur leurs paires. Pour toute paire {e,f} de classes P, Q, **la droite par les deux classes
  d'atterrissage de σ passe par P ou par Q**.

## 5. Le Fano tendu survit (OBSERVÉ)
- Tous les systèmes linéaires dérivés sont faisables, (P2) compris : 4 à 37 s.
- σ vient d'une solution. τ a été choisi par recherche locale sur ses 42 bits de retournement : ils ne changent
  aucun compte de bloc, mais ils changent les transitions internes T.
- Le témoin (`c1_experimental/data/x15_witness.pkl`) passe :
  - l'admissibilité locale dans les 42 supports étoiles et triangles ;
  - les 231 identités (P2) ;
  - toutes les compressions de Rayleigh : famille libre (triangle ou étoile) et blocs constants ailleurs, des deux
    côtés. Minimum −1,5·10⁻¹⁴, un zéro numérique ;
  - le critère lointain, avec 𝒰 de rang 3 ≤ 8.
- **Conséquence.** Au niveau des blocs, le Fano tendu est cohérent. Il ne peut mourir que sur les arêtes génériques
  effectives, au niveau des paires. **Ce n'est donc pas une route de plafond.**
- **Correction (26/09, notes/117 §2 ter).** Cette conclusion était prématurée. Le raffinement par cellules
  antipodales (proposé par « structures », issu de C2) tue ce témoin. Le certificat de Farkas est exact, et
  « structures » l'a revérifié indépendamment (`verify_c1_cells.py`). La question « tout sommet de Fano tendu
  meurt-il au niveau des cellules ? » est ouverte : un seul témoin a été tué.
- **Auto-attaque.** Deux fausses violations de Rayleigh venaient d'identités exactes non encore imposées :
  l'équilibre étiquette, puis (P2). Sur un modèle partiel, une violation signale d'abord une identité manquante.

## 6. Portée
Les outils du §1 à §3 sont généraux et transmis à C2 et à « structures ». Le cœur (torsion maximale générique) n'est
pas touché : ses comptes génériques ne sont pas fixés. Les seules prises connues sur le « générique » restent le
lemme du triangle (concentrations) et le 7-adique de L22 (rank₇ M_x ≤ 28 en tout sommet).

Scripts (copies dans `code/`) : x15_fano_tight.py, x15g_ilp.py, x15k_paths.py, x15n_ilp_p2.py, x15f_farblock.py,
x15j_far_gram.py, x15t_tau_search_adm.py.
