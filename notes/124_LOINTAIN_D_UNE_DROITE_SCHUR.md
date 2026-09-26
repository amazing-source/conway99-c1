# 124 — Le lointain d'une droite : complément de Schur exact (réel et mod 7), cible du dossier n° 5 d'Astra

*26/09, nuit. Consolidation, avec contrôles exacts, de ce que notes/102 §8 et notes/114 §1 disent sur le graphe lointain
d'une droite. C'est la contrainte connue la plus forte sur les arêtes génériques ; « structures » l'a transmise à Astra
(dossier n° 5). DÉRIVÉ = preuve écrite ; contrôles sur BvLS et sur données aléatoires. Aucun solveur.*

## 0. Cadre et résumé
Soit L = T = {x, y, z} une droite, B = T ∪ N₁(T) sa boule (39 sommets) et F son lointain (60 sommets).
- G(L) = M_T est le graphe cubique sur N₁(T).
- N (36 × 60) est l'incidence des ombres : chaque lointain w a 2 voisins dans chaque couche, notés N_w.
- c est le nombre de composantes de M_T.

| énoncé | statut |
|---|---|
| la boule a la valeur propre 3 avec multiplicité 2 + (c − 1) : quotient T/couches, plus composantes de M_T | DÉRIVÉ |
| **sur Q : Φ_F := (A_FF − 3I) − A_FB(A_BB − 3I)⁺A_BF = −7·Π**, Π étant le projecteur orthogonal sur K₋₄(L) (les vecteurs propres −4 de Γ portés par F, dimension 7 + c) | DÉRIVÉ ; contrôle BvLS (Φ_F = −9Π, rang 50, écart 3·10⁻¹⁵) |
| **mod 7 : rang₇ Q = rang₇ Q_BB + rang₇ R_L**, avec R_L[w,w′] = Q_ww′ − 6 + 1_{N_w}ᵀL_G⁺1_{N_w′} | formule de notes/102 §8 ; contrôle exact sur 6 tirages aléatoires |
| pour d(L) = 1 : rang₇ R_L = k − 22 ≤ 6 (L22) ; à k = 22, A_ww′ ≡ 3 − g(N_w, N_w′) | notes/102 §8, 114 §1 |

## 1. La boule
- Le quotient sur (e_x, e_y, e_z, 1_{couche x}, 1_{couche y}, 1_{couche z}) vaut
  [[A_T, 12I], [I, J₃]].
  - Sur les vecteurs symétriques : valeurs propres 6 et −1.
  - Sur les vecteurs de somme nulle : x² + x − 12 = 0, soit **3 et −4, chacune deux fois**.
- Sur les vecteurs de N₁(T) de somme nulle par couche, A_B agit comme M_T. Chaque composante de M_T au-delà de la
  première ajoute une valeur propre 3.
- Donc rang_Q(A_B − 3I) = 38 − c. À comparer avec rang₇ Q_BB = 37 − d(L) (notes/102) : mod 7, les valeurs propres
  −4 ≡ 3 du quotient s'ajoutent au noyau.
- Les deux vecteurs propres 3 du quotient sont des vecteurs propres de Γ portés par la boule : chaque lointain voit
  2 points par couche, donc la somme nulle par couche passe.

## 2. Le complément de Schur réel
- **Énoncé.** Φ_F = −7Π, où Π est le projecteur orthogonal de R⁶⁰ sur K₋₄(L).
- **Preuve.**
  - Pour f ∈ K₋₄(L), Af est porté par F (f s'annule sur B et Af = −4f). Le relèvement nul sur B convient, donc
    Φ_F f = (A − 3I)f = −7f.
  - Pour g ∈ V₃, on a (A − 3I)g = 0, donc Φ_F(g|_F) = 0 : le terme de boule est la correction de Schur de g|_B.
  - V₃|_F ⊥ K₋₄(L). Les dimensions se complètent : 54 − 2 − (c − 1) + (7 + c) = 60, le noyau de la restriction
    V₃ → R^F étant les vecteurs propres 3 portés par B. Φ_F est donc diagonalisé par cette somme orthogonale. ∎
- **Conséquences.**
  - A_F = 3I + NᵀRN − 7Π, avec R le bloc N₁ × N₁ de (A_B − 3I)⁺ : **le graphe lointain est fixé par les ombres et par
    le sous-espace K₋₄(L)**.
  - (3I + NᵀRN − A_F)/7 est un projecteur orthogonal de rang 7 + c. Tout mineur principal est donc ⪰ 0 et de rang
    ≤ 7 + c.
  - Toute famille W de lointains de taille ≥ 9 (pour c = 1) a un mineur de rang ≤ 8. C'est une condition héréditaire
    qui porte uniquement sur les ombres de W et les arêtes entre elles.
- **Contrôle.** Sur BvLS (r = 4, s = −5), Φ_F² = −9Φ_F à 2·10⁻¹⁴ près. Rang 50, égal à la dimension des vecteurs
  propres −5 portés par F. Écart à −9Π : 3·10⁻¹⁵. Script : code/x29f_far_phi_bvls.py.

## 3. La version mod 7 (notes/102 §8) et la cible
- Formule revérifiée exactement : code/x29e_schur_line_check.py (6 tirages sur 6, rang Q_BB = 36 pour d = 1).
- Dans un vrai srg, rang₇ R_L = 14 + k − 36 = k − 22 pour d(L) = 1, donc ≤ 6 par L22.
- N·R_L ≡ 0 (mod 7) automatiquement. R_L est donc une forme symétrique sur ker₇ N, de dimension 26 :
  - rang ≤ 6 est une condition de codimension 210 ;
  - k = 22 (R_L = 0) est de codimension 351.
- **Question du dossier n° 5.** Pour une donnée de droite (C, τ_u, τ_ū, σ_U) avec d(L) = 1, existe-t-il des bijections
  d'ombre et un graphe lointain λ/μ-cohérent avec rang₇ R_L ≤ 6 ?
  - Un « non » uniforme donnerait k ≥ 30, en contradiction avec L22.
  - Il resterait le cas où les 231 droites sont 7-dégénérées. Ce cas est forcé si k ≤ 20 (L21) et doit être exclu
    à part.

## 4. Portée
- Rien de neuf sur le fond : c'est la frontière de notes/106 (« toute preuve 7-adique doit contrôler G »). La forme
  réelle Φ_F = −7Π rend la dépendance explicite : le lointain d'une droite est fixé par ses ombres et par un sous-espace
  de dimension 8.
- À k = 22, il est même fixé mod 7 par les seules ombres.
