# 113 — Transposition du contenu de C3 à C1 : clôture (no-go, local/global, gains d'Eisenstein, somme de Gauss)

*25/09, nuit. Session « structures ». Consigne relayée par C1 : relire C3 (c3_experimental, preuve_c3.pdf) et
transposer sa démarche. Cette note clôt la transposition du **contenu** (réseaux propres, discriminants, symbole de
Legendre). L'utilisateur a précisé ensuite qu'il visait la **méthode expérimentale** de C3 ; celle-ci est traitée
à part (registre D11 + D2, notes suivantes). Scripts : `code/c3_local_global_genus.py`, `code/eisenstein_gain_spectra.py`,
`code/gauss_sum_arf_control.py`, `code/gauss_sum_windmill_reduction.py`.*

## 0. Résumé
| énoncé | statut | apport |
|---|---|---|
| R1 : local (K_θ(x), L17) contre global (Λ_θ), en 7 et en 11, pour θ = 3 et θ = −4 | calcul exact | cohérent : pas de contradiction |
| R2 : toute construction Z-linéaire à partir de A, N, 1 et de sous-espaces découpés mod p est automatique | preuve (Milgram) | ne donne que des bornes d'ordre (ex. c ≤ 22) |
| R3 : **no-go** — le mécanisme de C3 exige une symétrie d'ordre impair | preuve | explique aussi le « p = 2 seulement » de C2 |
| R3 bis : le gain d'Eisenstein des orientations de droites n'a aucun spectre à ≤ 3 valeurs propres | preuve (C2, à la main) + recherche exhaustive | le seul candidat « M » sans symétrie est fermé |
| R4 : face combinatoire de Arf = 1 : Σ_S (−1)^{#droites coupées par S} = −2⁷² | preuve ; contrôle T(7) | se réduit au modèle local et redonne L17 : fermé |

## 1. R1 — local contre global
Soit K_θ(x) = Λ_θ ∩ ℤ^{Γ₂(x)} le réseau local de L17 et S_θ(x) son complément orthogonal dans Λ_θ (rang 14).
Le réseau M = span_ℤ{E_θ e_y : y ∈ B₁(x)} est de rang plein dans S_θ(x) ⊗ ℚ et M ⊆ S^#. Son Gram est E_θ restreint
au moulin, entièrement connu. Donc v_p(det M) ≡ v_p(det S) (mod 2), et les classes d'unités coïncident à un carré près.
- **θ = 3** : det Gram = 3⁸·5⁶/(7¹⁴·11).
  - v₁₁ = −1, impair, comme v₁₁(det Λ₃) = 1 (le 11 vient de 1ᵀ1 = 99, et K₃ est sans 11).
  - v₇ = −14 exactement : aucun recollement en 7, donc Λ₃ ⊗ ℤ₇ = K₃ ⊥ S et δ_V = δ_{V_K} + δ_{V_S}.
  - (unité | 7) = +1, donc δ_{V_S} = 0. C'est exactement ce que demandent l'oddité globale (δ_V ≡ k/2) et
    l'oddité locale de L17 (δ_{V_K} ≡ k/2).
- **θ = −4** : det Gram = 2²¹/(3²·7¹⁴), (unité | 7) = +1. Même conclusion.
- **Verdict.** Au niveau du genre, le local et le global sont compatibles en 7 et en 11, des deux côtés.

## 2. R2 — pourquoi les variantes linéaires sont automatiques
Un réseau construit ℤ-linéairement à partir de A, de l'incidence N, de 1, et de sous-espaces découpés mod p (C^⊥,
fonctions équilibrées…) est un sur- ou sous-réseau d'indice fini d'un réseau dont le genre est fixé par le spectre.
Les p-excès sont des invariants de Witt de la forme discriminante (formule de Milgram) : ils ne changent pas en
passant à un sur-réseau par un sous-groupe isotrope. Il n'en sort que des bornes sur l'ordre des sous-groupes isotropes.
- **Exemple.** Z_bal = {g ∈ ℤ⁹⁹ : g mod 3 ∈ C^⊥}.
  - X = (Z_bal, (A + 7I)/9) est entier, et se plonge dans ℤ²³¹ par Nᵀ/3.
  - det X = 7·10⁵⁴·3^{45−2c}. L'intégralité redonne exactement c ≤ 22, soit rang₃ N ≥ 77 (notes/110 §3) : rien de plus.
- **Réseau des flots du graphe d'incidence** (99 + 231 sommets). Son déterminant est le nombre d'arbres couvrants,
  2⁴⁴·3²¹⁹·11⁵³, avec v₁₁ impair : cohérent avec Λ₃.

## 3. R3 — le no-go
**Ce qu'utilise C3.** Deux opérateurs entiers congrus modulo un premier 𝔭 : Q (quotient) et M (hermitien sur ℤ[ω]).
Q vérifie (Q + 4I)(Q − 3I) = cJ, et M la même relation **sans** terme en J. Leurs réseaux propres ont la même
réduction mod 𝔭 ; seul le côté Q voit 1, qui injecte le premier 11.

**Obstruction.** Réduire (Q + 4I)(Q − 3I) = cJ modulo 𝔭 impose 𝔭 | c.
- **Sans symétrie** (Q = A) : c = 2, donc 𝔭 | 2. En 2, la congruence mod 2 ne voit que la forme bilinéaire. L'invariant
  d'Arf demanderait une congruence mod 4, qui échoue puisque 2J ≢ 0 (mod 4).
- **Quotient par un groupe d'ordre p** : c = 2·(taille d'orbite). Un 𝔭 impair devient possible, le symbole de Legendre
  est visible, et c'est la contradiction de C3 (p = 3, (11 | 3) = −1, (7 | 3) = +1).
- **Involution (C2)** : c = 4, donc 𝔭 = 2 seulement. On n'obtient que la parité (Théorème A de C2), ce que C2 a trouvé
  indépendamment (« seul p = 2 compte »).

**Conclusion.** La démarche de contenu de C3 est intrinsèquement une démarche à symétrie d'ordre impair. Elle ne
s'applique ni à C1 (Aut trivial) ni à C2 (involution).

### R3 bis — le seul candidat sans symétrie est fermé
- **Construction.** On oriente cycliquement chacune des 231 droites (matrice antisymétrique T, T1 = 0), et on pose
  H = (−A + i√3·T)/2 ∈ M₉₉(ℤ[ω]).
  - H est hermitienne, H ≡ A (mod π = 1 − ω), et H1 = −7·1 : le 11 disparaît. C'est le vrai analogue de M.
  - 7I + H = N_ω N_ω^*, où N_ω est l'incidence étiquetée 1, ω, ω² ; 1ᵀN_ω = 0 puisque 1 + ω + ω² = 0.
- **Contraintes.** χ_H ∈ ℤ[x] et χ_H ≡ χ_A ≡ x⁵⁴(x + 1)⁴⁵ (mod 3). tr H = 0. tr H² = 1386. tr H³ = 6·231 = 1386
  (chaque triangle-droite a une holonomie ω³ = 1). Enfin −7 est la plus petite valeur propre.
- **Preuve courte (C2, vérifiée).** Pour un spectre {−7, a, b}, on a tr[(H + 7)(H − a)(H − b)] = 1386(8 − a − b) + 693ab = 0,
  soit (a − 2)(b − 2) = −12.
  - Parmi les paires possibles, la règle mod 3 (aucune valeur propre ≡ 1) ne laisse que {0, 8} et {−1, 6}.
  - {0, 8} donne tr H² = 2520 ≠ 1386. {−1, 6} donne 6·m₋₇ = 279, qui n'est pas entier.
  - À deux valeurs propres, on trouve (H + 7)(H − 2) = 0 avec m₋₇ = 22. Mais mod π, cela donne (A + I)² ≡ 0 (mod 3),
    faux sur ker₃ A (dimension 54).
- **Contrôle.** La recherche exhaustive (`code/eisenstein_gain_spectra.py`) trouve un ensemble vide.

## 4. R4 — la somme de Gauss (fermée)
- **Formule.** Λ₃ est pair et 2-unimodulaire, E₃ ≡ A (mod 2), et A E₃ A = 9E₃. Pour S ⊆ V, on en tire
  q(A1_S) = |S| + e(S) ≡ #{droites coupant S en 1 ou 2 points} (mod 2).
  (En effet e(S) = Σ_L C(|S∩L|, 2), et chaque point est sur 7 droites, nombre impair.)
- **Identité.** Arf = 1 (notes/110 §3.6) équivaut à **Σ_{S⊆V} (−1)^{#droites coupées par S} = −2⁷²**. De façon
  équivalente, Σ_F (−1)^{|F|} = +2²⁰⁴ sur les sous-graphes pairs ayant au plus une arête par droite.
- **Contrôle de la règle de signe.** T(7) a la même situation 2-adique. det Λ₃ = 5⁶·7 ≡ 7 (mod 8) prédit +2¹⁸, et
  la force brute sur 2²¹ sous-ensembles donne +2¹⁸. Contrôle négatif : le mauvais raffinement e(S) donne 0.
- **Réduction au moulin.** Par classe {a, a′}, avec ℓ = Nᵀ1_{S₂} mod 2 :
  - la somme sur S ∩ ({x} ∪ N(x)) donne f(s₀ = 0) = 2·(−1)^{[ℓ_a = ℓ_a′ = 0]} et f(s₀ = 1) = 2·(−1)^{[ℓ_a = ℓ_a′ = 1]} ;
  - comme Σ_a ℓ_a = 2|S₂|, il reste, pour m = 7 classes :
    Σ_S = −2⁸ · Σ_{S₂ ⊆ Γ₂(x)} (−1)^{|S₂| + e_H(S₂) + Σ_c ℓ_a ℓ_a′}. Cette forme a pour polaire H + P′ (mod 2).
- **Test de la réduction** sur 40 instances aléatoires (moulin à m classes, chaque sommet extérieur ayant exactement
  2 voisins dans N(x)) : 40/40. Contrôle négatif (un sommet à 3 voisins) : l'identité casse dans 20 cas sur 40.
- **Fermeture.** −2⁷² équivaut à une somme locale +2⁶⁴, soit rang₂(H + P′) = 40 et Arf 0. C'est exactement K₃ de L17 :
  pair, 2-unimodulaire, de rang 40, det 3⁸5⁶7^k ≡ 1 (mod 8) puisque k est pair. La seconde évaluation existe, elle
  redonne la même valeur : aucune contradiction.

## 5. Ce que cela change
- **Plus de variante de genre ou de discriminant** pour C1 ni pour C2. Global, local, 2-, 3-, 7- et 11-adique : tout
  est cohérent, et R3 explique pourquoi cela ne peut pas mordre sans symétrie d'ordre impair.
- **Le verrou reste la structure de G.** On passe à la méthode de C3 (registre, contrôles sur vrais graphes,
  balayage des tables de Brouwer).

## 6. Attributions
- Formule d'oddité et L22 : notes/101 (C1). Arf = 1 : notes/110 §3.6 (C1).
- Preuve courte de R3 bis : C2 (MATH_C2_PROGRAMME §23), vérifiée ici.
- R1 à R4 (hors ces points) : session « structures ».
