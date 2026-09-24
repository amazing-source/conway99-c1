# 95 — Preuve humaine de L7 (un point de Hamming n'est pas le point fixe d'une involution)

*2026-09-25, nuit. Jusqu'ici L7 reposait sur deux calculs SAT (201 s et 34 s). Voici une preuve à la main, courte,
vérifiée par ordinateur à chaque étape (`code/hamming_diag.py`).*

## Énoncé
Soit x un sommet de Γ = srg(99,14,1,2) qui est un **point de Hamming** : pour tous a, b ∈ Γ(x) non mates, la droite
par a et le sommet ab est {a, ab, ab̄} (τ = mate en x), c'est-à-dire que les 21 « grilles avortées » en x sont de
vraies grilles 3×3. Alors la réflexion σ_x (x ↦ x, a ↦ ā, ab ↦ āb̄) **n'est pas** un automorphisme de Γ.
Conséquence (branche C2) : l'unique point fixe d'une involution (qui agit comme σ_x, lemme de Makhnev) est tordu.

## Notations
Classes 1,…,7 (les droites par x), étiquettes (i, s), s ∈ F₂ (mate = changer s). Pour une paire P = {i, j}, Q_P est
l'ensemble des 4 sommets de Γ₂(x) d'étiquettes (i, s_i), (j, s_j), repérés par (s_i, s_j) ∈ F₂². Γ₂(x) = ⊔ Q_P (84).
Dans Q_P, u ~ u + e_i et u ~ u + e_j (droites par les étiquettes), et u ≁ u + (1,1). Q_P ∪ {x} ∪ (étiquettes de
P) est la grille G_P. Diagonales de Q_P : D₀ = {s_i = s_j}, D₁ = {s_i ≠ s_j}, c'est-à-dire les paires antipodales.

## Faits utilisés (tous redémontrés ici)
**(T) Grilles serrées.** Tout sommet hors d'une grille 3×3 G a exactement un voisin dans G. *Preuve* : avec
n_z = |Γ(z) ∩ G|, on a Σ_z n_z = 9·14 − 2·18 = 90 = |V ∖ G|. Et Σ_z C(n_z, 2) = 0, car toute paire de G a déjà
tous ses voisins communs dans G (λ = 1 pour les 18 arêtes, μ = 2 pour les 18 non-arêtes d'une grille 3×3).
Donc n_z ≤ 1 et, par la somme, n_z = 1.
**Conséquences.** Pour u ∈ Q_P et une paire R : si R ∩ P = ∅, les étiquettes de u ne sont pas dans G_R, donc
l'unique voisin de u dans G_R est dans Q_R ; si |R ∩ P| = 1, cet unique voisin est l'étiquette commune, donc u n'a
**aucun voisin dans Q_R**. Les 14 voisins de u sont donc : ses 2 étiquettes, ses 2 voisins dans Q_P, et un voisin dans
chaque Q_R, R ⊂ [7] ∖ P (10 paires).
**(A) Bijections.** Pour R ∩ P = ∅, les arêtes entre Q_P et Q_R forment une bijection φ_{PR} : Q_P → Q_R, avec
φ_{RP} = φ_{PR}⁻¹.
**(C) μ pour deux grilles partageant une classe.** P = {i, j}, P' = {i, k}, u ∈ Q_P, w ∈ Q_{P'}. On a u ≁ w (pas
d'arête entre Q_P et Q_{P'}). Leurs voisins communs sont : l'étiquette (i, s) si u et w ont le même signe s en i ; aucun
sommet de Q_P ni de Q_{P'} ; et un sommet v ∈ Q_R pour chaque R ⊂ [7] ∖ {i, j, k} (6 paires) tel que
φ_{PR}(u) = φ_{P'R}(w). Comme μ = 2 : **exactement une coïncidence si les signes en i sont égaux, deux sinon.**
Avec ψ_R = φ_{P'R}⁻¹ ∘ φ_{PR} : Q_P → Q_{P'}, les 6 images ψ_R(u) atteignent donc une fois chacun les deux points de
Q_{P'} de même signe en i que u, et deux fois chacun les deux points de signe opposé.

## Preuve
1. σ_x agit sur chaque Q_P comme l'antipodie u ↦ u + (1,1). Il préserve déjà toutes les adjacences sauf peut-être
   celles entre Q_P et Q_R. Donc σ_x ∈ Aut ⟺ chaque φ_{PR} commute avec les antipodies ⟺ chaque φ_{PR} envoie
   diagonales sur diagonales. On pose alors δ(P, R) ∈ F₂ : δ = 0 si φ_{PR}(D₀) = D₀, 1 sinon. On a δ(R, P) = δ(P, R), et
   ψ_R envoie D_ε(P) sur D_{ε + δ(P,R) + δ(P',R)}(P').
2. Chaque diagonale de Q_{P'} contient un point de chaque signe en i. Par (C), elle reçoit 1 + 2 = 3 des 6 images
   ψ_R(u). Donc **exactement 3 des 6 paires R ⊂ [7] ∖ {i, j, k} ont δ(ij, R) + δ(ik, R) = 1**. En particulier
   Σ_R (δ(ij, R) + δ(ik, R)) ≡ 1 (mod 2), pour chacun des 7·15 = 105 triplets (i ; {j, k}).
3. Sommons ces 105 congruences. Un terme δ(X, Y) (X ∩ Y = ∅) apparaît quand X joue le rôle de ij ou de ik : 2 choix de
   la classe commune dans X, 3 choix de la troisième classe hors de X ∪ Y. Cela fait 6 fois, et encore 6 fois avec les
   rôles de X et Y échangés : 12 fois au total. La somme vaut donc 0 à gauche et 105 ≡ 1 à droite. **Contradiction.** ∎

## Contrôles
- Le système réduit (105 bits δ, « exactement 3 sur 6 ») : UNSAT (Cadical, instantané) ; SAT si on ne l'impose que
  pour une seule classe i (27 uns sur 105). Sa version de parité (105 équations sur F₂) est de rang 55 et incompatible.
  `code/hamming_diag.py`.
- Cohérent avec le calcul antérieur (« le fait C seul suffit », UNSAT 3,2 s dans le modèle isométrique) et avec
  l'amorce de preuve de 30_LEMMES (nombre pair de ψ « droites ») : l'invariant qui conclut n'est pas l'orientation
  mais le **décalage diagonal**, additif pour la composition.

## Remarque : seconde preuve, et règle de transport (faits B + D)
Pour P ∩ P' = ∅, φ = φ_{PP'} et u ∈ Q_P, notons w₃ = φ(u) + (1,1). Le calcul des voisins communs de u et w (fait D :
[φ⁻¹(w) voisin de u dans Q_P] + [φ(u) voisin de w dans Q_{P'}] + coïncidences sur les 3 paires R du complémentaire
de P ∪ P' = 2), joint au fait B, donne la **règle de transport** : pour tout u, les trois transports
ψ_R(u) = φ_{P'R}⁻¹(φ_{PR}(u)) valent, en multi-ensemble, {φ(u), φ(u) + (1,1), φ(u + (1,1))}.
Dans le cas isométrique, φ(u + 11) = φ(u) + 11 et chaque ψ_R coïncide avec φ ou φ + 11 sur chaque diagonale. Donc
δ(P,R) + δ(R,P') = δ(P,P') : **δ est un cocycle sur les triangles du graphe de Kneser K(7,2)**. Or le complexe
(21 sommets, 105 arêtes, 105 triangles) a H¹(F₂) = 0 (calcul : dim Z¹ = dim B¹ = 20). Donc δ = df, et
δ(ij,R) + δ(ik,R) = f(ij) + f(ik) ne dépend pas de R : le compte du fait C vaut 0 ou 6, jamais 3. Contradiction.
La première preuve n'utilise que C ; celle-ci utilise B, C et D, mais explique la structure : σ_x-invariance
⇒ δ trivialisable ⇒ C impossible.

## Vers L8 (point de Hamming sans σ_x) : pourquoi l'argument ne passe pas tel quel
Sans σ_x, les φ_{PR} sont des bijections quelconques de F₂², c'est-à-dire des éléments de AGL(2,2) ≅ S₄. Un invariant
additif pour la composition serait un morphisme S₄ → F₂, donc la signature. Or le fait C ne fixe pas la parité : sur
les 58 multi-ensembles de 6 bijections compatibles avec (C), 50 contiennent un nombre pair de permutations impaires et
8 un nombre impair. Le nombre d'isométries parmi les 6 composées est toujours **pair** (0, 2, 4 ou 6 : 14, 27, 13 et
4 cas), mais la relation « ψ_R est une isométrie » s'écrit d_{PR} = d_{P'R}, où d_{PR} = L_{PR}(1,1) prend 3 valeurs.
Ce n'est pas une parité additive. Il faudra combiner (C) avec (B), (D) ou (E) ; les calculs de L8 (UNSAT en 2 114 s
sans cassage de symétrie) indiquent une contradiction plus profonde.

### Ce qui est établi pour L8 (faits B + D, sans σ_x)
- **Règle de transport** (ci-dessus) valable en général : {ψ_R(u)} = {φ(u), φ(u) + 11, φ(u + 11)}.
- Énumération locale (24 bijections φ) : si φ_{PP'} est une isométrie, les 3 transports ψ_R sont des isométries (9
  arrangements) ; sinon, ou bien les 3 sont non isométriques (18 arrangements), ou bien exactement 1 l'est (6).
- **Conséquence** : soit N l'ensemble des arêtes de Kneser dont la bijection n'est pas une isométrie. Tout triangle de
  Kneser {P, P', R} contient 0, 2 ou 3 arêtes de N, jamais exactement 1. Si aucun triangle n'est entièrement dans N,
  l'indicatrice de N est un cocycle, donc (H¹ = 0) N est la coupe d'une 2-coloration des 21 paires.
- Le fait C donne alors, pour P = ij, P' = ik : a = b et c = 6 − 2a (a, b : composées isométriques de décalage 1, 0 ;
  c : composées non isométriques). Le cas N = ∅ est L7 (a = 3).
- Tests (`code/hamming_linskel.py`) : le squelette des parties linéaires avec E seul est SAT ; avec C, ou C + E, pas
  de réponse en 5 min ; avec C + E + la condition des triangles de Kneser (T), pas de réponse en 20 min (263 Mo,
  `data/linskel_CET.runlog`). La contradiction de L8 n'est pas visible rapidement sur les parties linéaires seules ;
  **pas de preuve humaine de L8 cette nuit**.

## Lecture « matrice d'orbites » et portée pour C2
Avec une involution t = σ_x (point fixe x, point tordu autorisé), la partition de Γ₂(x) en 42 diagonales (orbites de t)
est équitable. Sa matrice quotient B̄ (42 × 42, symétrique, diagonale nulle car a₁ = 14, sommes de lignes 12) vérifie
**B̄² + B̄ = 12I + 4J − S**, où S[D, D'] = |P(D) ∩ P(D')| (calcul direct : on compte de deux façons les voisins communs
de u ∈ D avec les deux points de D'). Modulo 2 : B̄² + B̄ ≡ A_T ⊗ J₂ (A_T : graphe triangulaire T(7) sur les 21 paires).
- Au point de Hamming, B̄ ≡ (blocs de permutation Π_δ sur les paires disjointes) mod 2. Le bloc (ij, ik) de
  l'équation donne Σ_R Π_{δ(ij,R)+δ(ik,R)} ≡ J₂, c'est-à-dire exactement la parité impaire de la preuve de L7.
  **L7 est donc une obstruction modulo 2 sur la matrice d'orbites.**
- En général, l'équation modulo 2 seule est **toujours soluble** : B = S̄ = A_T ⊗ J₂ convient (S̄² = 0), et les
  solutions symétriques de diagonale nulle correspondent aux scindements orthogonaux S̄-invariants V₀ ⊥ V₁ avec 1 ∈ V₀
  (B = S̄ sur V₀, S̄ + 1 sur V₁). Pas d'obstruction de parité pure pour C2 : il faut les contraintes de support des
  blocs (qui viennent des étiquettes et des τ).

### Image « code de Golay factice » au point de Hamming (à la main)
Identifions x, les étiquettes et Γ₂(x) aux vecteurs de F₃⁷ de poids 0, 1, 2 (un carré Q_{ij} = les 4 vecteurs de
support {i, j}). Pour un vecteur v de poids 3, de support {i, j, k}, ses trois restrictions de poids 2 deux à deux
« partagent un signe ». Le fait C donne pour chaque paire un unique voisin commun dans Γ₂(x), noté z₁₂(v), z₁₃(v),
z₂₃(v), situé dans un carré Q_R avec R ⊂ [7] ∖ {i, j, k}.
- **Bijection (preuve).** Pour u ∈ Q_{ij}, l'application v ↦ z₁₂(v) (v parmi les 10 voisins de poids 3 de u) est
  une bijection sur les 10 voisins intérieurs de u. En effet, pour z voisin intérieur de u dans Q_R, le μ entre z et
  l'étiquette (i, u_i) impose exactement 2 voisins de z de signe u_i dans les carrés Q_{iq}. L'un est u, donc
  exactement un autre, c'est-à-dire exactement un v tel que z₁₂(v) = z.
- **Cohérence impossible.** Si z₁₂(v) = z₁₃(v) = z₂₃(v) pour tout v (structure de quotient de H(7,3)), chaque
  z ∈ Γ₂(x) représenterait 10/3 vecteurs de poids 3 : chaque z porte exactement 10 coïncidences (2 signes × 5
  classes), et chaque v cohérent en consomme 3. Donc au moins une incohérence en chaque z. C'est la version locale de
  L1 (99 ne divise pas 3⁷).
- **Ce qui manque pour L8** : exclure les configurations incohérentes. Le μ entre z et les étiquettes (k, c) montre
  que la cohérence en v équivaut à « le second voisin de z de signe c en classe k est exactement v|_{jk} ». Rien ne
  le force localement : c'est là que le SAT travaille 35 minutes.
