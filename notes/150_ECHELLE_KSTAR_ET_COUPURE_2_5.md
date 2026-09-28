# 150 — Échelle min K* ≥ 9/7 et théorème de coupure 2|5 (côté preuve de (B))

*28/09, fin de matinée. C1. Directive de l'utilisateur : deux cibles V-libres seulement ; (A) cohérence des axiomes de N ;
(B) le théorème de coupure 2|5. Solveurs bannis, pas d'énumération. Partage : C1 = preuve de (B), « structures » = construction.
DÉRIVÉ = preuve écrite ; CALCUL = vérification exacte sans solveur.*

## 0. Énoncés
| énoncé | statut |
|---|---|
| Les 780 paires non tuées par min K* ≥ 5/7 ont min 7\|κ\|² ∈ {5, 6, 7, 8} (438/239/20/83) ; donc min K* ≥ 9/7 tue les 1 272 | CALCUL (deux scans indépendants) |
| κ ∈ K*, 7\|κ\|² = n ⟹ h(p) = 2(κ, repère_p) est un vecteur propre entier σ-impair de valeur −4 du GRAPHE, nul sur x et sur les 14 intérieurs | DÉRIVÉ |
| n = 5 (k = 2, Sol) : h = ±1 exactement sur T = les 40 étiquettes qui rencontrent un seul des blocs {1,2} | DÉRIVÉ |
| n = 5 : 4 classes de témoins à relabel près (A, B, C, D) | DÉRIVÉ |
| Identités à deux étoiles β₁ = β₂, Γ, Ξ = 4(Γ + 4β + Δ − 35) ≥ 0 | DÉRIVÉ |
| BvLS (m = 11) : aucun vecteur −5 σ-impair ne s'annule hors de la coupure 2\|9 (dimension 0) | CALCUL |

## 1. Le témoin comme vecteur propre du graphe
- h(p) := 2(κ, f_p), où f_p est le vecteur du repère de p (u pour un représentant, −u pour son image, h_c et −h_c aux
  intérieurs, 0 en x). Pour tout z de l'espace du repère, p ↦ (z, f_p) est dans E₋₄ ; κ ∈ W donne 0 aux intérieurs.
- En orbites : a = h|_représentants, Na = 4a (N = B − A), Rᵀa = 0 (équation aux intérieurs).
- n = 5, coupure {1,2} : a = ±1 sur les 20 orbites des cellules (1,x), (2,x), x ∈ X = {3..7}, et 0 ailleurs.
- Forme 0/1 équivalente : Q = C⁻ ∪ {U₁₂⁺} (11 orbites), N1_Q = −2a.
- Forme sommets : g′ = (b₁ + b₂ − h)/2 est un vecteur propre −4 entier. Il vaut −2 en 1⁰ et 2⁰, et +1 sur 6 étiquettes
  de O_{1⁰} et 6 de O_{2⁰} (dont 1⁰2⁰). Ici b_c = −4(e_{c⁰} − e_{c¹}) + 1_{O_{c⁰}} − 1_{O_{c¹}} est le vecteur de bloc.

## 2. Les 4 classes (n = 5)
- Rᵀa = 0 en x ∈ X : a(1x+) − a(1x−) + a(2x+) − a(2x−) = 0. Cela laisse 6 motifs par bloc :
  - type S (P1–P4) : h({i^s, x^t}) = ε_i(x)(−1)^s, qui ne dépend que du signe côté 1/2 ;
  - type X (P5, P6) : h({i^s, x^t}) = ±ψ(i)(−1)^t, avec ψ(1) = 1, ψ(2) = −1.
- Rᵀa = 0 en 1 et 2 force n(P1) = n(P4) et n(P2) = n(P3), donc un nombre impair de blocs de type X.
- À S₅ × retournements × flip₁ × échange(1,2) × signe près :
  - A = X⁵ (produit : h = ψ(bloc)·(−1)^{t}) ;
  - B = P1 P4 X³ ;
  - C = P1² P4² X ;
  - D = P1 P2 P3 P4 X.

## 3. Conséquences locales (DÉRIVÉ)
- Tout p ∈ T a 6 − 2ι(p) voisins dans T, où ι(p) = nombre de ses voisins 1- ou 2- dans la cellule (1,2) ; donc ι ≤ 1.
  Tous ces voisins sauf au plus un ont le signe −h(p).
- Les arêtes de même signe dans T forment un couplage ; les sommets à ι = 1 n'en ont pas.
- Étoile 1 (et 2), pour U ∈ C₁ : a_U(a_{τ̂U} − a_{μU}) ∈ {0, 1, 2}, car la part C₂ est au plus 4.
  - β₁ := a₁ᵀN₁a₁ = a₂ᵀN₂a₂ = β.
  - a₁ᵀY a₂ = 40 − β, où Y est le bloc C₁ × C₂.
- Projection de κ sur l'espace des lignes d'une étoile : a_cᵀD_c a_c ≥ \|a_c\|⁴/\|κ\|². D'où β ≥ 10 (A), 8 (B), 6 (C, D).
- Tous les comptages linéaires (types de triangles, Ls = 0 sur le graphe des triangles, arêtes T–complément) sont
  automatiquement cohérents. La contradiction doit venir de la combinatoire fine (λ, μ exacts, bijections Φ).

## 4. Identité à deux étoiles (DÉRIVÉ)
- Au bloc c, f_c = h sur O_{c⁰}, Φ_c : F_c → paires non-compagnes (bijection), K₃ = 2J − π − τ̂ − τ̂μ − μτ̂.
- D_c(w) = F(w) − F(σw) = somme de h sur N(w) ∩ X_c.
- Pour tout c : Q_c := Σ_{w∈F_c} D_c(w)² = 2 f_cᵀ(9I − μ + π + τ̂ + τ̂μ + μτ̂) f_c. Cela utilise Σ f_c = 0 et la formule de K₃.
- Avec β_o = f(o)(f(τ̂o) − f(μo)), t_c = #{β_o = 2}, γ_c = Σ f(o)f(τ̂μo) et Δ = n_S − n_X :
  - γ₂ − t₁ = γ₁ − t₂ =: Γ ;
  - Ξ := Σ_{étiquettes X} D₂(w)² = 4(Γ + 4β + Δ − 35) ≥ 0.
- Le long d'un cycle μ∪τ̂, avec z_i = ±1 la « bonté » des arêtes : β = 2Σz_i et γ = −Σ z_i z_{i+1}. Un β élevé fait baisser γ.
  Pas de contradiction par ces seules bornes.

## 5. Forme « rang » et contrôle BvLS
- n = 5 ⟹ κ ⊥ w_u pour les 20 orbites du K₅ sur X (et la cellule (1,2)). Les w du sous-système K₅ sont donc de rang ≤ 14.
  - Compte générique : 7 + 20 = 27 conditions pour 22 dimensions, soit 5 de trop.
  - Formulation équivalente : aucun vecteur de E₄(N) ne serait porté par étoile(1) ∪ étoile(2), c'est-à-dire
    λ_max(W[étoile1 ∪ étoile2]) < 28.
- CALCUL (`runs/star7/bvls_cut_eig.py`, algèbre linéaire sur BvLS) : les vecteurs −5 σ-impairs nuls hors des étoiles de
  S (et aux intérieurs) forment un espace de dimension 0 pour \|S\| ≤ 3, 4 pour \|S\| = 4, 14 pour \|S\| = 5.
  - Rien n'interdit donc un argument uniforme en m pour n = 5.
  - Cible propre : « tout sous-système K₅ engendre W ».

## 6. Ouvert
- Une preuve lisible de (B) : il faut un argument qui utilise la combinatoire exacte (bijections Φ, K₃, lemme CN de
  « structures ») au-delà des identités linéaires.
