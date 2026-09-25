# 115 — Lemme du triangle : première contrainte exacte active en torsion maximale

*25/09, nuit. Labo c1_experimental (notes/114), note E2. Points 1 et 2 recalculés indépendamment par « structures »
(sympy, rationnels exacts, `c99_structures_lab/scripts/verify_c1_triangle.py`).*

## 0. Résumé
| résultat | statut | portée |
|---|---|---|
| **Lemme du triangle** : T ⪯ 3I − P_∂ pour toute famille triangle | DÉRIVÉ, recalcul indépendant | vaut en torsion maximale |
| corollaire : e ≤ 12 arêtes internes | DÉRIVÉ, recalcul indépendant | version par blocs (analogue de C2 §25) |
| cas tendu e = 12 : vecteur propre de valeur 3 explicite, T 2-régulier, comptes exacts 1 et 3 | DÉRIVÉ, recalcul indépendant | rigidité |
| effet en torsion maximale : 22 % des configurations localement admissibles tuées | OBSERVÉ (échantillon) | pas encore un plafond |
| modèle de Fano : forcé au régime tendu, toute σ-arête interne le tue | DÉRIVÉ | |
| Fano tendu : comptes génériques exacts et contrainte κ_ℓ'(e) ≠ M_m(κ_ℓ(f)) | DÉRIVÉ | aucune contradiction pour l'instant |

## 1. Énoncé
Soient x un sommet et α, β, γ trois classes en x. La **famille triangle** Q est formée des 12 paires de Δ_x dont les
deux étiquettes sont dans deux classes distinctes de {α, β, γ} : ce sont les arêtes de l'octaèdre K_{2,2,2} des
6 étiquettes. Deux paires de Q ont des classes qui se rencontrent. Leur adjacence est donc déterminée par les données
locales :
- une étiquette commune u : {u,v} ~ {u,w} ssi w = τ_u(v) ;
- des mates c₀, c₁ : {c₀,v} ~ {c₁,w} ssi w = σ_c(v).
Soient T la matrice 12 × 12 de ces adjacences internes, ∂ l'incidence 6 × 12 étiquettes–paires (de rang 6), et
P_∂ = ∂ᵀ(∂∂ᵀ)⁻¹∂.

**Lemme du triangle.** Dans tout srg(99,14,1,2) : **T ⪯ 3I − P_∂**, soit λ_max(T + P_∂) ≤ 3.

## 2. Preuve
1. On a 3I + (11/99)J − A = 7E₋₄ ⪰ 0. Il en va de même pour la compression au support W = {x} ∪ Γ(x) ∪ Q, dont
   toutes les entrées sont connues.
2. Complément de Schur sur le moulin R = {x} ∪ Γ(x) :
   - S_RR = 3I + (11/99)J − A_R a pour spectre 20/3, 2⁶, 4⁷, 0¹ ; il est donc ⪰ 0 ;
   - S_RQ est dans l'image de S_RR ;
   - **3I + (11/99)J_Q − S_QR S_RR⁺ S_RQ = 3I − P_∂ exactement.** Entrées de P_∂ : {−1/8, 0, 1/8, 1/4, 1/2} ;
     spectre de 3I − P_∂ : 2⁶, 3⁶.
   Calcul exact en rationnels, fait deux fois de façon indépendante (C1 : numpy puis rationnels ; « structures » :
   sympy).
3. D'où 3I − P_∂ − T ⪰ 0. ∎

Lecture. La borne vaut 3 sur ker ∂ (fonctions de somme nulle en chaque étiquette) et 2 sur im ∂ᵀ (fonctions
{u,v} ↦ f(u) + f(v)). Le côté −4 (λ_min(A_W) ≥ −4) ne donne que T ⪰ Φ, avec spec Φ = {−4⁶, −3,6², −2,67³, −0,8} :
c'est faible.

## 3. Corollaires
- **(a)** Soit q le vecteur valant −6 en x, 1 sur les 6 étiquettes du triangle, −3 sur les 8 autres étiquettes et 2
  sur Q. Alors 1ᵀq = 0 et qᵀ(3I + (11/99)J − A)q = 96 − 4·1ᵀT1 ≥ 0, donc **e ≤ 12**. (Version par blocs ; la
  même borne apparaît chez C2, §25, par ‖E₋₄f‖² ≥ 0.)
- **(b) Cas tendu, e = 12.** Alors Sq = 0, soit **Aq = 3q**. L'équation propre, lue sommet par sommet, donne :
  - en y ∈ Q : 2 + 2deg_T(y) = 6, donc **T est 2-régulier** ;
  - en y ∉ Q ayant une étiquette dans α ∪ β ∪ γ : **exactement 1 voisin dans Q** ;
  - en y ∉ Q n'en ayant aucune : **exactement 3 voisins dans Q**.
  Aux étiquettes et en x, l'équation est automatiquement vérifiée.

## 4. En torsion maximale (OBSERVÉ, vérifications seulement)
- **Répartition des arêtes spéciales.** Chaque arête spéciale (τ ou σ) de Δ_x tombe dans exactement une famille
  triangle. Il y en a 168 pour 35 triangles, soit e = 4,8 en moyenne. **Le lemme interdit les concentrations.**
- **Échantillon.** Sur 20 000 configurations aléatoires en torsion maximale, 103 sont localement admissibles (λ ≤ 1
  et μ ≤ 2 dans tous les supports). **23 sont tuées par le lemme.** Les supports étoiles (boules de droites) ne
  violent jamais : 0 sur 1 877.
- **Certificats.** Ils sont exacts. Un exemple explicite (triangle {0,1,6}, 10 arêtes de T,
  λ_max(T − (3I − P_∂)) = 0,0543) est en cours de recalcul indépendant par « structures ».
- **Ce que le lemme ne fait pas.** Les violations viennent de familles denses : 8 à 10 arêtes internes, contre 4,8
  en moyenne. Les configurations aux transitions étalées passent. **Ce n'est donc pas encore un plafond.**

## 5. Le modèle de Fano (notes/109 §3)
Chaque droite de Fano porte exactement 12 τ-arêtes internes. D'où deux cas :
- **une seule σ-arête interne** à une droite donne e ≥ 13 : **contradiction** ;
- **sans σ interne**, les 7 familles sont tendues, avec 7 vecteurs propres de valeur 3 explicites (Gram 112I + 50J,
  de somme égale au vecteur local trivial), et elles partitionnent Δ_x.
  - Comptes génériques exacts pour y = {e,f} (e ∈ ℓ, f ∈ ℓ', m le troisième point, C₄ le quadrangle
    complémentaire, M_ℓ, M_ℓ', M_m ses trois couplages, a = κ_ℓ(f) et b = κ_ℓ'(e) les classes où tombe σ) :
    - g = 1 − [a ∈ R'] sur M_ℓ, et 1 − [b ∈ R'] sur M_ℓ' ;
    - g = 3 − s_c − s_d sur M_m ;
    - g_{m,c} = −1 + s_{M_m(c)} + [b ∈ {c, M_ℓ'(c)}] + [a ∈ {c, M_ℓ(c)}].
  - Contrôles : Σg = 8 et sommes par classe cohérentes.
  - **Contrainte nouvelle** : pour tout y, κ_ℓ'(e) ≠ M_m(κ_ℓ(f)).
- **Sur 309 configurations de Fano à σ aléatoire, 270 sont tuées.** Les survivantes sont exactement tendues. Le Fano
  tendu reste ouvert en C1 (en C2, il est exclu par le Théorème F).

## 6. Portée
C'est la première contrainte exacte du corpus qui agit dans le régime de torsion maximale, où planchers, comptages
et genre sont tous satisfaits. Le mécanisme est le principe de Rayleigh sur un support entièrement déterminé, comme le
certificat d'Astra sur sa branche Z₇. En un sommet, les supports entièrement déterminés sont exactement les étoiles
(boules de droites, toujours saines) et les triangles. **Pour aller plus loin, il faut des supports qui mêlent les
données de plusieurs sommets, ou des comptes exacts (cas tendus) qui fixent des arêtes génériques.**

Scripts (copies dans `code/`) : x14_triangle_supports.py, x14b_inspect.py, x14c_fano.py, x14d_full_vertex.py,
x14e_admissible_sample.py, x14f_patterns.py, x14g_psi.py, x14h_export_violation.py.
