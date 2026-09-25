# 110 — Deux routes closes (Minkowski, Akiyama sur Λ_L) ; les codes des droites contiennent leur dual

*25/09, soir. Attaque du plafond après notes/109. Deux routes examinées puis fermées, avec la raison. Un petit lemme
nouveau sur les codes p-aires des droites, sans contradiction. Une imprécision de notes/102 §9 corrigée.*

## 0. Résumé
| énoncé | statut | apport |
|---|---|---|
| bornes de Minkowski : min Λ₃ ≤ 36, min Λ₋₄ ≤ 44 (et localement min K₃(x) ≤ 38, min K₋₄(x) ≤ 49) | preuve | **route close** : les vecteurs courts sont des objets locaux qu'on ne sait pas classer |
| paire de Petersen (vecteur ±1 de Λ₃, norme 20) : passe tous les comptages | preuve | contre-exemple à « vecteur court ⟹ grille » |
| Akiyama sur Λ_L : ni annulation de Venkov, ni isolement des racines, ni repère dense de rang ≤ 24 | preuve | **route close** (confirme notes/96 §3) |
| codes des droites : pour p = 2, 3, 5, C_p ⊇ C_p^⊥ ; rang₂ N ≥ 72, rang₅ N ≥ 72, rang₃ N ≥ 77 | preuve ; contrôle BvLS | invariants nouveaux, sans contradiction |
| notes/102 §9 : les droites intérieures ne sont pas toutes « pures » en torsion maximale | preuve | correction |

## 1. Minkowski (fermée)
- **Bornes** (Blichfeldt, γ_n ≤ (2/π)Γ(2 + n/2)^{2/n}, recalculées par la session « structures ») :
  - Λ₃ : pair, rang 54, det 11·7^{14+k}. γ₅₄ ≤ 7,96, et det^{1/54} ≤ 4,75 à k = 28, donc **min Λ₃ ≤ 36**.
  - Λ₋₄ : rang 44, det 9·7^{14+k}. γ₄₄ ≤ 6,65, et det^{1/44} ≤ 6,74, donc **min Λ₋₄ ≤ 44**.
  - Localement (déterminants de L17) : min K₃(x) ≤ 38 et min K₋₄(x) ≤ 49. Ce n'est pas mieux.
- **Vecteurs courts connus.**
  - Grilles : 1_G − 1_{G′} ∈ Λ₃, de norme 18, 16 ou 12.
  - Cocliques de Hoffman : 1_C − 1_{C′} ∈ Λ₋₄. Le cas de norme 14 est formé de deux cocliques qui se coupent en 15
    points ; c'est la configuration « Fano » : 7 points, 7 blocs du complémentaire de Fano, 70 sommets extérieurs avec
    un voisin de chaque côté, et une coclique commune de 15 sommets (notes/107 §4(a)).
  - Les vecteurs universels (A + 4I)(e_x − e_y) sont de norme 42 ou 56, donc au-dessus de la borne.
- **Pourquoi c'est fermé.** Un vecteur ±1 de Λ₃ vérifie, en u ∈ S^±, d_{S^±}(u) − d_{S^∓}(u) = 3, et à l'extérieur
  d⁺ = d⁻.
  - La **paire de Petersen** (S⁺ et S⁻ deux Petersen induits, sans arête entre eux, extérieurs équilibrés, norme 20)
    passe tous les comptages.
  - Les blocs N(w) ∩ S⁺ (w extérieur) forment un **espace linéaire** sur les 10 points (arête : son apex ; non-arête :
    son voisin extérieur). Chaque bloc induit un couplage de Petersen. Même chose pour S⁻, avec des tailles égales.
  - Réalisation : 45 blocs de taille 2, 20 sommets d = 1, 14 sommets d = 0. En un sommet u ∈ S⁺, les conditions
    d'étiquettes 1 + [apex] + #(S⁺ ∋ c) = #(S⁻ ∋ c) se vérifient toutes.
  - Le support peut aller jusqu'à 36 : aucune classification n'est faisable à la main, et « vecteur court ⟹ grille »
    est faux au niveau des comptages.

## 2. Akiyama sur le réseau des droites Λ_L (fermée)
Rappel (notes/96 §3 bis, notes/109 §4) : les 231 vecteurs w_L = √7·E₋₄1_L sont de norme 4, de produits 0 et ±1 à P = 0,
avec WWᵀ = 21·I₄₄. Ce qui fait marcher Akiyama (arXiv:2609.08319) à 266, et qui manque ici :
1. **Venkov.** La complétion unimodulaire paire minimale est de rang 44 + 4 = 48. La série thêta harmonique de degré 2
   y vit dans S₂₆ = ⟨ΔE₄²E₆⟩ = ⟨q − 48q² + …⟩, qui n'est pas nul. On n'obtient que
   Σ_{|v|²=4} P(v) = −48·Σ_{racines} P(r), avec des racines et une couche 4 inconnues : pas de 2-design forcé.
2. **Isolement des racines.** Chez Akiyama, t_y = (u_y, s) a une composante de recollement s, avec ⟨s, a⟩ ∈ ½ + ℤ.
   Toute racine à composante D₇ non nulle vérifie donc |⟨u_y, v⟩| ≥ ½ pour les 220 vecteurs, d'où 55 ≤ 45 (absurde).
   Ici w_L ∈ M, qui est entier : ⟨w_L, r⟩ ∈ ℤ, et le repère donne seulement
   #{L : ⟨w_L, r⟩ ≠ 0} ≤ 21|r_V|² ≤ 42 < 231. Aucune contradiction.
3. **Pas de repère dense de rang ≤ 24.** L'algèbre locale engendrée par I, J, H, S = MᵀM et P′ = MᵀPM est fermée :
   HS = −S − P′ + 4J et H² = 12I − H − S + 2J. Ses 5 espaces propres communs sont ceux de notes/96 §2. Tout élément
   dont le coefficient en H est non nul est non nul sur K₃ ou sur K₋₄, donc de rang ≥ 30. Les repères globaux sont de
   rang 44 ou 54.

Les trois leviers de notes/96 §3 manquent bien. **Pas de rigidité de Niemeier.**

## 3. Lemme nouveau : les codes des droites contiennent leur dual
N désigne l'incidence points × droites (99 × 231), avec NNᵀ = 7I + A, de valeurs propres 21 (sur 1), 10 (V₃) et
3 (V₋₄). C_p = colonnes de N mod p ; C_p^⊥ = {z : Σ_{q∈L} z_q ≡ 0 pour toute droite L}.

**p = 2 (et p = 5 à l'identique).**
1. Λ₃ est 2-unimodulaire (det 11·7^{14+k}), d'où 𝔽₂⁹⁹ = C₃ ⊥ C₋, avec C₃ = Λ₃ mod 2 (dimension 54) et
   C₋ = (Λ₋₄ ⊕ ℤ1) mod 2 (dimension 45).
2. NNᵀ ≡ 0 sur C₃ (10 est pair) et est inversible sur C₋. Donc C₋ ⊆ C₂ et C₂^⊥ ⊆ C₃.
3. Soit z ∈ C₂^⊥, relevé en v ∈ Λ₃ : Nᵀv = 2u, et Nu = NNᵀv/2 = 5v. Donc z ≡ Nu ∈ C₂.
4. On a C₂ = C₋ ⊕ D avec D = C₂ ∩ C₃, et C₂^⊥ = D^{⊥ dans C₃} ⊆ D. Donc D est coisotrope dans l'espace symplectique
   C₃ (Λ₃ est pair) : dim D ≥ 27, et **rang₂ N = 45 + dim D ≥ 72**.
5. Forme exacte : D est engendré par les 1_{N(L)} (A ≡ E₃ mod 2). Le Gram mod 2 des 1_{N(L)} est
   NᵀAN ≡ X₁ + X₃ ≡ X_int² + X_int. D'où **rang₂ N = 72 + ½·rang₂(NᵀAN)**.
6. Les **ensembles pairs** (chaque droite les coupe en 0 ou 2 points ; ils induisent un graphe 7-régulier, avec un
   voisin par droite) forment un code autoorthogonal E ⊆ C₃, de dimension ≤ 27.
   - (C₃, q), avec q = |v|²/2 mod 2, a un invariant d'Arf égal à 1 (det Λ₃ ≡ 3 mod 8 pour k pair).
   - Si tous les ensembles pairs ont un cardinal ≡ 0 mod 4, alors dim E ≤ 26.
7. Pour p = 5, même raisonnement (Nu = 2v) : **rang₅ N ≥ 72**.

**p = 3.**
1. Λ₃ est 3-unimodulaire et NNᵀ = 10 ≡ 1 sur Λ₃, d'où C₃″ := Λ₃ mod 3 ⊆ C_3^{droites}.
2. Sur C′ = (Λ₋₄ ⊕ ℤ1)^sat mod 3 (dimension 45, avec le recollement 9 entre Λ₋₄ et 1), on a NNᵀx ≡ (1ᵀx)·1.
   - Donc rang₃(NNᵀ) = 55, et ker₃(A + I) = Λ₋₄ mod 3 (dimension 44).
3. Pour z ∈ C^⊥, relevé en z̃ : Nu = z̃ + (2/11)(1ᵀz̃/3)·1, et 1 ∈ C (car Σ_L 1_L = 7·1). Donc C^⊥ ⊆ C.
   - Il en résulte que D′ = C ∩ C′ est coisotrope dans C′, de dimension ≥ 23. D'où **77 ≤ rang₃ N ≤ 98**.
   - La borne 98 vient de ce que 1 coupe chaque droite en 3 points.
4. C^⊥ est l'espace des **fonctions équilibrées** : chaque droite est constante ou arc-en-ciel mod 3. C'est aussi
   l'ensemble des v ∈ Λ₋₄ mod 3 dont toutes les sommes sur les droites sont ≡ 0.

**Contrôle sur BvLS** (243, 11 droites par point, `graphs.bvls()`). Les mêmes arguments prédisent rang₂ N ≥ 188
(partie paire V₋₅) et rang₅ N ≥ 177 (V₄). Calcul exact : rang₂ = rang₅ = 243, rang₃ = 231. Aucun conflit. Chez BvLS,
les ensembles pairs mod 2 et mod 5 sont nuls.

**Verdict.** Ce sont des invariants nouveaux (dim E, rang₂(X₁ + X₃)) qui ne contredisent rien : toutes les bornes
sont < 99. Ils pourraient servir si un mécanisme forçait beaucoup d'ensembles pairs ou de fonctions équilibrées.

## 4. Correction de notes/102 §9
« Les trois points d'une droite contenue dans Γ₂(x) sont des paires deux à deux disjointes » est **faux en torsion
maximale**.
- Soit y = {a,b}. Son ombre S_α(y) = {ā, c} existe toujours (μ(y, ā) = 2, voisins communs a et S_α(y)).
- Le troisième point de la droite {y, S_α(y), ·} n'est pas une étiquette : ce serait b = c, donc τ_b(a) = ā, une
  boucle.
- Les 84 arêtes d'ombre sont donc sur des droites intérieures dont deux points partagent une classe. L'énoncé ne vaut
  que pour les droites à trois arêtes génériques. Aucun lemme n'en dépendait.

## 5. Attributions
- « k = rang de recollement local de K₃(x), K₋₄(x) en tout sommet » n'est pas nouveau : c'est L17 et notes/102 §2.
  Troisième dérivation : M_x·Mᵀ = Mᵀ(35I + 7P + 35J) ≡ 0 (mod 7), vérifié exactement (sympy). Donc M_x = 0 ⊕ (H + 4I)|_K.
- Y = X_int² − 4X_int − 17I − J est notes/96 §3 bis (K = −G_L(G_L − 10I) + J). C'est pourquoi l'identité
  (Y − 4)(Y + 17) = 0 de notes/109 §4 n'a aucune prise : elle découle du seul spectre de X_int.

## 6. Contrôle : la « 7-spécialité » exigée par L22 n'a rien d'anormal
p-rangs de A − rI aux premiers p | r − s, pour les graphes existants des familles (λ, μ) = (0, 2) et (1, 2)
(`code/prank_family.py`), comparés à la borne de van Eijl min(f, g) + 1 :

| graphe | torsion | borne | p-rang |
|---|---|---|---|
| Clebsch (16,5,0,2) | non tordu (5-cube replié) | 6 | 6 (p = 2) |
| Gewirtz (56,10,0,2) | tordu au maximum | 21 | 20 (p = 2 et p = 3) |
| srg(9,4,1,2) | non tordu | 5 | 4 (p = 3) |
| BvLS (243,22,1,2) | non tordu | 111 | 67 (p = 3) |

Pour 99, la borne vaut 45. Le rang est impair (L2) et ≤ 43 (L22), donc au moins 2 sous la borne. Gewirtz, qui existe
et qui est tordu au maximum, est 1 sous la sienne. La contrainte de L22 est donc du même ordre que ce que réalisent
les graphes existants : pas un indice de non-existence.
