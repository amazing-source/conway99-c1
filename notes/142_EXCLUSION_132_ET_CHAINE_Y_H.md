# 142 — Exclusion de l'enveloppe 132 (d₆⁴) : la chaîne « paires y → étage h », avec ses contrôles

*27/09, 15 h. C1. À relire par un humain. Suite de notes/140-141.*

## Énoncé
**L'enveloppe 132 (odd unimodulaire de dim 24, racines d₆⁴, voisins D₁₂² et D₆⁴) ne porte aucun repère (F).**

Conséquence : dans la ligne (C), l'involution ne peut pas avoir 132 pour enveloppe.

## La chaîne (chaque étape est une condition nécessaire démontrée)
1. **Les deux y** sont de norme 7, orthogonaux, et engendrent N⊥ ∩ U = 7I₂. Le piège min (y⊥ ∩ U)* ≥ 8/7 équivaut EXACTEMENT
   à deux conditions :
   - (α,y₁)² + (α,y₂)² ≤ 6 pour toute racine α, soit une valeur dans {0,1,2,4,5} ;
   - (v,y₁)² + (v,y₂)² ≤ 13 pour tout v de norme 3.

   En effet, un vecteur court w de (y⊥)* se relève en v = w + (a y₁ + b y₂)/7 avec |a|, |b| ≤ 3. Alors |v|² < 8/7 + 18/7 < 4,
   donc v est une racine ou un vecteur de norme 3.
2. **Nouvelles racines** (vecteurs de norme 2 de l'ombre). On a |(y,β)| ≤ 3/2, et jamais les deux y à 3/2 ensemble. C'est (F)
   en β, voir notes/140 §2.
3. **Énumération complète des paires à Aut(U) × signes près** (y_pairs.py, y2_engine.py, y_pairs_gamma.py).
   - **y₁.** Le piège par racine donne |(α,y)| ≤ 2, donc la projection sur chaque composante est de niveau ≤ 2. On prend y₁
     W(R)-dominant : ses labels de Dynkin c_j = (y,α_j) vérifient Σ_j m_j c_j ≤ 2 sur chaque composante.
   - **Réalisabilité** des labels : test d'intégralité de c·H⁻¹ (HNF de a ↦ a·B·Aᵀ).
   - **Assemblage** : programmation dynamique sur (classe de glue, norme).
   - **y₂.** On le prend dominant pour W(R ∩ y₁⊥). Par Steinberg, ce groupe est engendré par les réflexions simples aux labels
     nuls de y₁. Pour chaque composante, on prend les poids de niveau ≤ 2, conjugués de Weyl, avec le filtre racine de paire
     « jamais |(α,y₁)| = |(α,y₂)| = 2 ». Assemblage par programmation dynamique sur (classe, norme, (y₁,y₂)). Puis on applique les
     filtres 1-2.
   - **Γ = Aut(U)/W(R).** C'est l'ensemble des automorphismes du diagramme de Dynkin qui préservent le code de glue
     (gamma_fullrank.py, contrôle exact φ(U) = U). On trouve |Γ| = 8, le champ « group » de la table de Borcherds. y₁ est pris par
     Γ-orbite, y₂ par orbite de Stab_Γ(y₁) × {±1}.
   - **Résultat :** 32 y₁ dominants, puis 5 orbites de y₁, 371 candidats y₂, et **304 paires**
     (data/finishC/ypairs/gpairs_132.json).
   - **Test de régression** (après la version en flux du moteur y₂) : on retrouve 371 et 304 à l'identique.
4. **132 est RIGIDE.** Tout vecteur de norme 3 a m(x) = 0 : il ne touche aucune nouvelle racine à 3/2. C'est vérifié sur les
   4096 vecteurs (m = r/8 − E = 30 − 10·3 = 0).
   - Or, d'après (F) en β (notes/140 §2), une nouvelle racine β vérifie w(β) := Σ_c (h_c,β)² = 1 si et seulement si β est touchée
     à 3/2 par exactement un vecteur impair du repère.
   - Donc **B₁ := {w = 1} = hits(y₁) ⊔ hits(y₂) EXACTEMENT**, et w = 3 partout ailleurs.
5. **Étage h** (pair_h_check.py → y_first.h_exact). On cherche 7 vecteurs h qui vérifient :
   - h ∈ U, |h|² = 4, h ⊥ y₁, y₂ (car h ∈ N), et deux à deux orthogonaux ;
   - |(h,β)| ≤ 1 sur les nouvelles racines ;
   - w prescrit : 1 sur B₁, 3 ailleurs ;
   - Lemme Z : Σ h ∈ 2U (notes/141 §1) ;
   - cellules : pour chaque paire de blocs {c,d} et chaque t = ±1, il existe x de norme 3, ⊥ y₁, y₂, avec (x,h_c)(x,h_d) = t, les
     deux produits valant ±1, et (x,h_e) = 0 sinon. Raison : les deux orbites de {c,d} ont C_coC_do = +1 et −1.
   - La recherche est exacte, de type DLX avec bitsets : branchement sur la racine la plus contrainte, et condition de monotonie
     des cellules sur les configurations partielles.
6. **Résultat : pour les 304 paires, aucune configuration h** (h_found = false). Aucun timeout. Les recherches sont complètes,
   entre 0,5 et 49 s. Fichier : data/finishC/ypairs/ghcheck_132_all.jsonl.

## Contrôles (après correction du bug de bitsets de 14 h 18, commit e146d69)
- **Bug corrigé.** L'ancien codage packbits(row[::-1]) + 'big' décalait les indices quand M mod 8 ≠ 0. Tous les verdicts
  antérieurs ont été jetés, et C2 a mis son lot partiel en quarantaine.
- **Test unitaire** du nouveau codage (bitorder little) : ok pour M = 1…32256.
- **y = 0**, avec M = 32255, 32251 ou 20001 (tous ≢ 0 mod 8) : une configuration valide est trouvée (orthogonale, w ∈ {1,3}, Z).
- **ctrl_prescribed.py.** On prend la couverture d'une configuration connue H* comme prescription, avec M = max(H*) + 1 + k pour
  tout k tel que M mod 8 ≠ 0. La configuration est retrouvée, et sa couverture est identique.

## Ce qui reste pour que l'exclusion soit solide
1. **Une seconde énumération indépendante des paires.** C2 l'a proposée. On pourrait comparer le multiset des invariants des 304
   classes.
2. **Le frame_lp de « structures » sur gpairs_132.json.** Ce serait un verdict indépendant par paire, avec certificats exacts.
   Sur les 2 416 paires non réduites : 144 exclues sur 154 au premier passage.
3. **Relecture humaine** de trois points :
   - (a) le lemme de rigidité (m ≡ 0 ⇒ B₁ = hits des y) ;
   - (b) l'argument des cellules ;
   - (c) la complétude de l'énumération y (niveau ≤ 2, Steinberg, DP).

## Même méthode, en cours
- **115** (a₇²d₅², rigide, Γ = 8) : 1 472 paires réduites, en cours sur 6 workers. À 15 h : 150/150 mortes.
- **87** (d₄⁶, rigide, Γ = 48) : 3 913 paires. 44 (a₃⁸, Γ = 384) : énumération en flux à relancer. 10 (a₁²⁴) : Γ trop gros pour ma
  recherche arrière, route Aut(N0) de « structures ».
- **Réseaux non rigides.** Mode général de l'étage h : w = 1 sur les hits des y ; w ∈ {1,3} sur les racines touchables par un
  vecteur de norme 3 ⊥ y ; w = 3 ailleurs.
