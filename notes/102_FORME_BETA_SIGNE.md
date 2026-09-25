# 102 — Structure 7-adique complète (globale et locale) ; le signe comme outil : L23

*25/09, fin de matinée. Suite de L22 (notes/101). Question : où la torsion peut-elle entrer dans la structure 7-adique ?
Réponse : par le **signe** (discriminant mod 7) des blocs extrêmes, en plus de leur rang. Résultat nouveau, **L23** : une
droite L dont le nombre d'arbres couvrants τ(G(L)) est un carré non nul mod 7 force k ≥ 24.*

## 0. Résumé
| résultat | énoncé | statut |
|---|---|---|
| structure globale | N = A − 3I (mod 7) vérifie N² = 2J : sur W = 1^⊥, N est autoadjoint de carré nul, de rang 14 + k. G = N(W) = ⟨f_v⟩ est totalement isotrope. β(Nv, Nv') = v·Nv' est non dégénérée sur G, de Gram Q = A − 3I + 3J, et **non scindée** | preuve ; 5 SRG existants |
| structure locale | M_x² ≡ 0 ; im M_x = G_x := G ∩ F^{Γ₂(x)} (dim k) ; G = G_x ⊥ W_x, W_x = ⟨g_v : v ∈ B₁(x)⟩ non scindé (moulin : rang 14, disc 1) ; donc **la forme de M_x est hyperbolique** | preuve (deux dérivations) |
| outil | S ⊆ V : rang₇ Q_SS ≤ 14 + k, et **égalité ⟹ partie non dégénérée de Q_SS non scindée** (disc ≡ (−1)^{k/2}) | preuve |
| **L23** | boule d'une droite : rang Q = 37 − d(L) ; si d(L) = 1, disc ≡ τ(G(L)). Donc **(τ(G(L)) \| 7) = +1 ⟹ k ≥ 24** | preuve ; 300 configurations, 0 échec |
| négatif | blocs d'arête (27 points, L20) : rang Q = 25 − 2e, toujours impair, jamais extrême | 10 395 couplages, exhaustif |

## 1. Structure globale mod 7
1. (A − 3I)(A + 4I) = A² + A − 12I = 2J (SRG), et A + 4I ≡ A − 3I : **N² ≡ 2J**. Sur W = 1^⊥ (99 ≡ 1, donc
   F₇⁹⁹ = ⟨1⟩ ⊥ W, W non scindé de dim 98), N préserve W et N² = 0. rang N|_W = rang₇(A − 3I) − 1 = 14 + k.
2. G := N(W) ⊆ ker N|_W = G^⊥ ∩ W, donc G est totalement isotrope. g_v := N(e_v − 1) = (A − 3I)e_v − 4·1 et
   f_v = 63E₋₄e_v ≡ 5g_v : **G = ⟨f_v⟩ = radical de ρ₋₄ = ρ₋₄ ∩ ρ₃** (notes/101).
3. **β(Nv, Nv') := v·Nv'** est bien définie et non dégénérée sur G (si Nv ⊥_β G alors Nv ∈ W ∩ ⟨1⟩ = 0). Gram sur les
   générateurs : β(g_u, g_v) = (e_u − 1)ᵀN(e_v − 1) ≡ **Q_uv, Q = A − 3I + 3J** (1067 ≡ 3). Chaque g_v est isotrope
   (Q_vv = 0) ; β(g_u, g_v) = 3 + A_uv sinon.
4. β est, au facteur −1/7 près, la 7-partie de la forme discriminante de Λ₋₄ (pour v ⊥ 1 : E₋₄v = −(A − 3I)v/7). Donc
   ε_β = ε_V = (−1)^m (k = 2m ; L22 : δ_V ≡ m). Dimension 2(7 + m) et disc ≡ (−1)^m ≠ (−1)^{7+m} : **β non scindée**.
5. Quotient : G^⊥ ∩ W / G = U ⊥ U′, U = ρ₋₄/G (30 − k, non scindé), U′ = ρ₃/G (40 − k, scindé).

*Vérification (`code/beta_form_check.py`, `code/gq33_check.py`) :* Petersen (p = 3), T(7) (p = 5), T(8) (p = 3), T(9) (p = 7),
GQ(3,3) = srg(40,12,2,4) (p = 3) : N² = μJ, rang Q = α, et le signe de β égale le signe de Jordan ε_V (corrigé par
(−u | p)^α si α est impair). **5/5.**

## 2. Structure locale en x
1. **M_x² ≡ 0.** M_x est le complément de Schur de N au bloc du moulin B₁(x) (inversible mod 7). Avec
   c = 1_Y − N_YX N_XX⁻¹ 1_X on a M_x² = 2ccᵀ, et c = 0 car 1 ∈ N(F^{B₁(x)}) : a = 2e_x + 4·1_{Γ(x)} donne
   (A − 3I)a ≡ 1 (en x : −6 ≡ 1 ; sur Γ(x) : 2 + 4 − 12 ≡ 1 ; sur Γ₂(x) : 8 ≡ 1). (Contrôle : Petersen.)
2. im M_x = {w ∈ G : w|_{B₁(x)} = 0} =: G_x, de dim k ; la restriction G → F^{B₁(x)} est de rang exactement 14.
   ρ₋₄ = κ_x + G (κ_x = réduction de K₋₄(x)) et U_x = κ_x/G_x ≅ U.
3. La forme de M_x (sur F^{84}/ker M_x) est β|_{G_x}. Si v ∈ B₁(x) et g ∈ G_x, β(g_v, g) = g(v) = 0 : donc
   **G = G_x ⊥ W_x**, W_x = ⟨g_v : v ∈ B₁(x)⟩, de Gram Q sur le moulin. Calcul à la main : sur les 14 étiquettes,
   Q = −3I + P + 3J a pour valeurs propres 3 (×7) et 5 (×7), avec J₁₄ ≡ nilpotente, et le complément de Schur en x est
   nul. Donc **rang 14, disc = 15⁷ ≡ 1 : W_x non scindé.**
4. D'où disc(β|G_x) ≡ (−1)^m en dim 2m : **la forme de M_x est hyperbolique.** Seconde dérivation, indépendante :
   l'oddité de K₋₄(x) (données 2-adiques de L17). Les deux concordent.

## 3. L'outil : bornes de sous-graphe raffinées par le signe
Q_SS est le Gram de β sur {g_v : v ∈ S}, donc rang₇ Q_SS ≤ dim G = 14 + k. En cas d'égalité, les g_v engendrent G et
Q_SS ≅ β ⊥ 0 : **sa partie non dégénérée est non scindée.** Autrement dit, un bloc extrême de rang pair R de mauvais
signe (scindé) donne k ≥ R − 12. Version locale : pour I ⊆ Γ₂(x), rang (M_x)_II ≤ k, et l'égalité impose que la
partie non dégénérée soit **scindée**. (Les bornes L20 et L21 sont des cas de rang₇ Q_SS ≤ 14 + k : même rang, à 1 près,
que A − 3I.)

## 4. L23 : le signe de la boule d'une droite
**Énoncé.** Pour une droite L, Q restreinte à la boule L ∪ N(L) (39 points) a rang 37 − d(L). Si d(L) = 1 (G(L)
connexe et 7 ∤ τ(G(L))), sa partie non dégénérée a pour discriminant **τ(G(L))** modulo les carrés. Par conséquent :
**si une droite a τ(G(L)) ≡ 1, 2 ou 4 (mod 7), alors k ≥ 24** ; et k = 22 impose τ(G(L)) ≡ 0, 3, 5 ou 6 (mod 7) pour
toute droite.
*Preuve.*
1. U = ⟨1_{X_x}, 1_{X_a}, 1_{X_ā}⟩ ⊂ F³⁶. A_G 1_{X_p} = 1_{N(L)} (un voisin dans chaque partie), donc A_G préserve U et
   U^⊥. Pour v ∈ U^⊥ : Jv = 0, la ligne de p ∈ L donne 1_{X_p}·v = 0, donc Q v = (0, (A_G − 3I)v). D'où
   **F³⁹ = (F^L ⊕ U) ⊥_Q U^⊥**, avec Q|_{U^⊥} = −L_G|_{U^⊥} (L_G = 3I − A_G, laplacien du graphe cubique G(L)).
2. Sur F^L ⊕ U (base e_p, 1_{X_p}) : T = [[4(J − I), 5I + J], [5I + J, 3J − I]]. Partie triviale [[3,3],[3,3]] :
   ⟨3⟩. Partie standard : [[3,5],[5,−1]] ⊗ std₂, de déterminant −28 ≡ 0, donc ⟨3⟩ ⊗ std₂, de disc 27 ≡ 6.
   **T : rang 3, disc 18 ≡ 4 (carré).**
3. L_G sur F³⁶, noyau ⟨1⟩ pour d = 1 : disc de la partie non dégénérée = det du laplacien réduit = τ(G(L)) (base
   e_i − e₃₆ : BᵀLB = (I + 11ᵀ)L₀(I + 11ᵀ), det(I + 11ᵀ) = 36 ≡ 1). L_G sur U : Gram I + 2J, partie non dégénérée
   std₂ (disc 3). Donc disc(L_G|_{U^⊥}) ≡ 3⁻¹τ.
4. Total : rang 3 + 33 = 36 et disc ≡ 4 · (−1)³³ · 3⁻¹τ. En symboles de Legendre : (+1)(−1)(−1)(τ | 7) = (τ | 7).
5. Si k = 22, le bloc est extrême (36 = 14 + 22), donc non scindé : disc ≡ (−1)¹¹, soit (τ | 7) = −1. ∎
*Contrôle (`code/ball_sign_check.py`).* 300 configurations (τ_a, τ_ā, σ) aléatoires : rang 37 − d et
rang S₂₄ = 23 − d, 0 échec ; 258 cas d = 1 : signe de la boule = signe de S₂₄ = (τ | 7), 0 échec. Parmi les
configurations localement admissibles avec d = 1 : (τ | 7) = +1 dans 105 cas, −1 dans 93.
*Cas d impair ≥ 3.* Même énoncé avec σ(L) := signe de la partie non dégénérée de Q_boule : k = 23 − d(L) ⟹
σ(L) = (−1)^{(23−d)/2}. Pour d pair, le rang 37 − d est impair et la borne est k ≥ 24 − d, sans condition de signe.
*Négatif (`code/edge_block_sign.py`).* Bloc d'arête B₁(x) ∪ B₁(y) (27 points), pour les 10 395 τ_y : rang Q = 25 − 2e,
toujours impair, donc jamais extrême. L'outil n'ajoute rien à L20.

## 5. Ce que cela change, et où la torsion entre
1. **Dichotomie L23.** k ≥ 24, ou bien toute droite de Γ a τ(G(L)) ∈ {0, 3, 5, 6} (mod 7). Avec L21 : k ≤ 20
   impose d(L) ≥ 3 sur les 231 droites ; k = 22 impose que toutes les droites génériques soient « τ-non-carrées ».
2. **La torsion entre par le signe.** τ(G(L)) est une statistique de torsion (G(L) est fixé par τ_a, τ_ā et l'holonomie
   de L). Heuristique (Cohen–Lenstra, données ci-dessus) : une droite est générique à 85 % et τ-carrée à ≈ 50 %. k = 22
   demanderait ≈ 196 droites toutes τ-non-carrées. **La fenêtre attendue est donc k ∈ {24, 26, 28}**. Prouvé :
   10 ≤ k ≤ 28, plus les dichotomies.
3. **Critère de non-existence.** Il suffit d'un ensemble S ⊆ V avec rang₇ Q_SS ≥ 43, ou = 42 et scindé. (À k = 28,
   β est non scindée de dim 42 et U est un plan anisotrope : pour u ∈ Λ₋₄, 7 | u·u ⟺ u mod 7 ∈ G.)
4. **Limite.** Les blocs entièrement connus ont au plus 39 points (rang Q ≤ 37) : le signe ajoute 2 au cas extrême,
   pas plus. Pour atteindre 42–43, il faut des blocs contenant des arêtes génériques ; c'est là que la méthode doit
   maintenant porter. Piste : à k extrême, Q est entièrement déterminée par ses lignes sur le bloc (factorisation de
   rang), et chaque autre sommet w devient un vecteur isotrope de G, de produits 3 + A_wv avec le bloc.

## 6. Recherches bibliographiques (25/09)
- [Ducey et al., *Critical group structure from the parameters of an SRG*](https://arxiv.org/pdf/1910.07686)
  ([JCTA](https://www.sciencedirect.com/science/article/pii/S0097316521000236)) : groupe critique du 99 entièrement
  déterminé, (Z/11)⁵³ ⊕ (Z/2)⁴⁴ ⊕ (Z/9)⁴³ ; preuve élémentaire par 7-rang de la non-existence de srg(28,9,0,4)
  (rang déterminé + vecteurs locaux du noyau). La méthode ne se transpose pas : les différences de colonnes
  n'engendrent que im(N)|_W.
- [Brouwer–van Eijl, *p-rank of adjacency matrices of SRGs*](https://www.win.tue.nl/~aeb/preprints/361304.pdf) :
  r_p ≤ min(f, g) + 1 ; aucun argument de genre ni de signe.
- [Fukshansky et al., *Lattices from tight frames*](https://arxiv.org/pdf/1902.02862),
  [Chvátal, *Comparison of two techniques*](https://arxiv.org/abs/0906.5389),
  [*Non-existence of two infinite families of SRGs* (2025)](https://www.sciencedirect.com/science/article/abs/pii/S0195669825000034),
  [Akiyama (266)](https://arxiv.org/pdf/2609.08319) : aucun n'utilise le genre, l'oddité ou le signe mod p des réseaux
  propres. **L22 et L23 paraissent nouveaux** ; la méthode (symboles de Conway–Sloane, formes quadratiques sur F_p)
  est classique.
- Vérification du 25/09 (recherche « 99-graph 2026 ») : [*A Forced-Structure Reduction and Verifiable Bounds for
  Conway's 99-Graph*, arXiv 2608.11211 (août 2026)](https://arxiv.org/abs/2608.11211) : réduction à un graphe
  12-régulier contraint sur 84 sommets (notre Γ₂(x)), borne circulante 68,0 %, recherche CP-SAT et tabou (70,7 %).
  **Aucun p-rang, réseau, genre ni matrice de Seidel.** Le problème reste ouvert
  ([Epoch AI](https://epoch.ai/frontiermath/open-problems/conway-99-graph)). Côté droites équiangulaires, la
  correspondance générale Seidel ↔ droites est classique
  ([Greaves, mini-cours](https://grwgrvs.github.io/talks/Montreal_Lectures.pdf)), mais rien sur le cas 99 / angle 1/7.

## 7. Reformulation par la matrice de Seidel (deux-graphe)
- **Mod 7, Q = A − 3I + 3J ≡ 3S**, où S = J − I − 2A est la matrice de Seidel de Γ (−6 ≡ 1). En général Q ∝ S mod p
  dès que 2r + 1 ≡ 0 (mod p) : 99 (r = 3, p = 7), Petersen (r = 1, p = 3).
- S a pour valeurs propres 70, −7 (×54), 7 (×44), donc **S² = 49(I + J)**. Au passage, Γ équivaut à 99 droites
  équiangulaires de R⁴⁵ d'angle arccos(1/7) (Gram I + S/7, de rang 45).
- **Forme de Smith de S sur Z₇ : 1^{14+k} 7^{71−2k} 49^{14+k}** (S⁻¹ = S(I + J)⁻¹/49 rend la suite symétrique ; version
  globale de L19). Les formes de Jordan vérifient W_S ≅ U_S⁻¹ et, via det S = 10·7⁹⁹, le signe de la 7-composante
  vaut −1. L'oddité de S (forme paire, indéfinie, de signature −9) est vérifiée pour tout k pair : pas de contrainte.
- **Énoncé Seidel de L23.** Pour tout ensemble I de sommets : rang₇ S(Γ[I]) ≤ 14 + k. Si |I| = 14 + k, alors
  det S(Γ[I]) ≡ 0 ou (det S(Γ[I]) | 7) = (−1)^{k/2}. Si |I| > 14 + k, det S(Γ[I]) ≡ 0. *Preuve :* S ≅ D ⊥ 0 et, par
  Cauchy–Binet, det S_II = det D · det(P_I)². C'est invariant par commutation de Seidel : **une propriété du
  deux-graphe de Γ**.
- **Critère.** Un sous-graphe induit à 43 sommets de déterminant de Seidel premier à 7 contredit L22. Un sous-graphe
  à 42 sommets de déterminant non carré mod 7 contredit k = 28 ; à 40 sommets, de déterminant carré non nul, il
  contredit k = 26 ; etc.
- *Contrôle (`code/seidel_check.py`, Petersen, p = 3) :* S² = 9I, rang₃ S = 4 = α. Les 4-mineurs principaux non nuls
  ont tous le caractère −1, celui de la partie non dégénérée. Forme de Smith 1⁴3²9⁴.

## 8. Au-delà d'une droite générique : ce qui est forcé, ce qui ne l'est pas
- Le complément de Schur de la boule dans Q est une matrice R_L sur les 60 sommets lointains (à distance 2 de toute
  la droite), **de rang k − 22**. Pour w lointain, soit N_w ses 6 voisins dans N(L), deux par partie. Alors
  R_L[w,w'] = Q_ww' − 6 + 1_{N_w}ᵀ L_G⁺ 1_{N_w'}, où L_G⁺ est la fonction de Green, mod 7, du graphe cubique G(L).
- **À k = 22, R_L = 0 : tout Γ est déterminé mod 7 par une boule générique et les N_w.** On a
  1_{N_w}ᵀL_G⁺1_{N_w} ≡ 6 pour chaque w, et 1_{N_w}ᵀL_G⁺1_{N_w'} ≡ 3 − A_ww' pour w ≠ w'.
- *Identité (négative).* Soit F la matrice des voisins lointains communs. Elle est fixée par λ et μ :
  F = 12I − A_G + 2J − A_G² − D. Alors trace(L_G⁺F) = −trace L_G − trace(L_G⁺D) ≡ −108 − 8 ≡ 3, et donc
  **trace R_L ≡ 0 toujours**. Le premier moment est automatique ; seuls les moments supérieurs font intervenir le
  graphe lointain inconnu.
- À k = 28, G_L = E_L^⊥ est de dimension 6, scindé ssi (τ(G(L)) | 7) = −1. Les 60 sommets lointains y donnent 60
  vecteurs de Gram R_L, et R_L est de rang ≤ 6 alors que ses 1 770 entrées hors diagonale ne prennent que deux valeurs
  chacune (3 + A_ww' − 6 + Green). C'est très contraint, mais cela passe par les arêtes génériques : c'est la même
  frontière que la technique des relations sur quatre étoiles (piste (b) de notes/101).

## 9. Conclusion d'étape : ce que la voie 7-adique locale peut et ne peut pas faire
- **Tout est cohérent localement pour chaque k pair ≤ 28.** Les formes locales (M_x hyperbolique, K̄ non scindé, U_x ≅ U
  non scindé, U′_x scindé) et globales (β non scindée, Smith 1^{14+k}7^{71−2k}49^{14+k}) sont forcées par les
  paramètres et k seul. Aucune contradiction ne peut venir du genre (la seule, k = 30, est L22).
- **Le signe n'agit qu'aux blocs extrêmes.** Les blocs entièrement connus ont au plus 39 sommets (boules de droites,
  rang Q ≤ 37). Ils ne peuvent être extrêmes que pour k ≤ 22. **La meilleure borne inférieure possible par cette voie
  est donc k ≥ 24** (L23), et elle est conditionnelle à l'existence d'une droite générique τ-carrée.
- **k = 28 est invisible localement.** Heuristique de Cohen–Lenstra symétrique : si Γ existait, k = 28 serait la
  valeur la plus probable (déficit minimal 2, imposé par L22). À k = 28 aucun bloc connu n'est extrême. Toute
  contradiction doit donc utiliser des blocs de rang ≥ 42, c'est-à-dire les arêtes génériques de Γ₂(x) (le graphe
  12-régulier sur 84 sommets où s'arrête aussi arXiv 2608.11211).
- **Structure générique (pour la suite).** Dans le régime de torsion maximale (aucune coïncidence τ/σ), chaque
  y = {a, b} ∈ Γ₂(x) a exactement 8 voisins génériques {c, d} (c, d dans les 5 autres classes). Pour chaque étiquette c,
  le nombre de ces voisins contenant c vaut 2 − #{τ_a(b), τ_b(a), σ_a(b), σ_b(a) égaux à c} : **les degrés sont
  prescrits par les données de torsion.** Les trois points d'une droite contenue dans Γ₂(x) sont des paires deux à deux
  disjointes. Et y ↦ h_y (colonne de M_x) donne 84 vecteurs de norme 1 dans un espace scindé de dimension k, de Gram M_x.
