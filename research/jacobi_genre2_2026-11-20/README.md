# Genre 2 pour Conway-99 : premier coefficient de Fourier–Jacobi (20/11/2026)

Piste nouvelle : vérification faite, le dépôt n'avait que des séries thêta de genre 1, harmoniques de degré 2 et 4
comprises. Aucune série thêta de Siegel de genre ≥ 2, aucune forme de Jacobi.

## Objet

M = √7 L1* : réseau pair de rang 44, de niveau 7 et de déterminant 7^(44−d), avec d = r − 1. Notations de
`code/lab_theta_lp_2026-10-08/NOTE.md`.

Les 462 vecteurs ±y_T (T une droite) ont norme 4. La forme Φ = Σ_{±T} θ_{M,y_T}(τ, z) est une forme de Jacobi holomorphe
de poids 22, d'indice 2, sur Γ₀(7). Ses coefficients c(n, r) comptent les couples (y, x) avec y un vecteur-triangle,
Q(x) = 2n et B(x, y) = r.

## Ce qui est établi

- **L'espace** `jacobi_space.py`. On a J^faible_{22,2}(Γ₀(7)) = M₂₂ φ₀,₁² + M₂₄ φ₋₂,₁ φ₀,₁ + M₂₆ φ₋₂,₁², de dimension
  49 ; le sous-espace holomorphe est de dimension 47.
  - Validé sur six réseaux réels, E8^a ⊕ (√7 E8)^(5−a) ⊕ A ⊕ A avec y de norme 4 : leur série thêta de Jacobi est dans
    l'espace jusqu'à q²⁴. [E]
  - Un bug de troncature dans φ₀,₁ (les termes de ℘ jusqu'à |r| = n) a été trouvé et corrigé grâce à cette validation.
- **Cohérence.** La couche des triangles est un 2-design (Σ_T y_T y_Tᵀ = 21P, car BBᵀ = A + 7I vaut 3 sur l'espace
  propre −4). D'où Σ_r r² c(n,r) = 84 n b_n. C'est exactement la condition ξ₂ = 22·χ₂ − 4·Dχ₀ = 0 que donne la
  structure de Jacobi (22 × 84 = 4 × 462). [P]
- **Statistiques des paires de droites, par droite T** [P] :
  - t(T) = nombre de prismes contenant T ;
  - 32 − t(T) droites disjointes sans arête vers T ;
  - 144 + 3t(T) droites disjointes à une arête ;
  - 36 − 3t(T) droites disjointes à deux arêtes ;
  - donc t(T) ≤ 12. Au total n₀ = 3696 − P, n₁ = 16632 + 3P, n₂ = 4158 − 3P.
- **La virgule flottante ne marche pas ici** (`lp_sanity.py`) : avec des coefficients jusqu'à 2·10³³, HiGHS déclare
  irréalisable même la vraie forme d'un réseau existant. Tout est donc refait en fractions.
- **Le programme linéaire exact** `jacobi_exact_lp.py` combine le genre 1 (famille affine et contraintes « ext » de
  l'équipe), la forme de Jacobi d'indice 2 (holomorphie, Φ(τ,0) = 462θ_M, 2-design, c(n,r) ≥ 0) et les paires de droites
  en n = 2, fonctions de P. Il utilise le simplexe exact de `theta_lp_exact.py`, et il est contrôlé sur un vrai réseau
  (réalisable).

## Résultats

| N | hypothèse | r = 37 | r = 39 | r = 41 | r = 43 | P permis |
|---|---|---|---|---|---|---|
| 20 | aucune | réalisable | réalisable | réalisable | réalisable | [0, 1386] |
| 20 | seuls les triangles en norme 4 | réalisable | réalisable | réalisable | réalisable | [0, 1386] |
| 32, 40 | seuls les triangles en norme 4 | en cours | | | | |

**Lecture.** Ce coefficient contient déjà la série thêta harmonique quartique, que l'équipe avait trouvée réalisable.
L'apport nouveau est la positivité de chaque c(n, r) et le couplage avec P. À N = 20, il ne contraint rien.

Usage : `python3 jacobi_exact_lp.py N [d …] [only_triangles] [Pmax=…]` ; `python3 jacobi_exact_lp.py N sanity`.
