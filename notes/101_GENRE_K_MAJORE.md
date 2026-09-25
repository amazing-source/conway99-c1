# 101 — L22 : la première majoration de k (k ≤ 28), par le genre du réseau Λ₋₄

*25/09, 08 h. Route A (plafond par un argument exact, non moyenné). Résultat : **k ≠ 30**, donc **10 ≤ k ≤ 28**,
c'est-à-dire rank₇(A − 3I) ≤ 43 au lieu de la borne 45 de van Eijl (1991) et Brouwer–van Eijl (1992). C'est le
premier « plafond » du corpus : jusqu'ici k n'avait que des minorations (L19 bis, L20, L20 bis/ter, L21).*

## 1. Énoncé
**Lemme L22.** Dans un srg(99,14,1,2), le réseau Λ₋₄ = Z⁹⁹ ∩ ker(A + 4I) n'est pas entièrement 7-divisible :
rank₇(A − 3I) ≤ 43, soit k ≤ 28. De façon équivalente, la partie 7-unimodulaire U de Λ₋₄ (rang 30 − k) n'est pas
nulle ; la formule d'oddité impose de plus qu'elle ne soit **jamais hyperbolique** sur F₇.

## 2. Preuve
1. **Λ₋₄ est pair, de rang 44, défini positif.** Pour u ∈ Λ₋₄, u ⊥ 1, donc uᵀu ≡ Σ u_x ≡ 0 (mod 2).
2. **Son discriminant a un exposant qui divise 63.** On a 63E₋₄ = −9(A − 3I) + J, entière. La projection de Z⁹⁹ sur
   l'espace propre est Λ₋₄^#, et 63Λ₋₄^# ⊆ Λ₋₄.
3. **Partie 3 : Z/9, cyclique.** E₋₄e_x = (28, −8, 1)/63 est d'ordre exactement 63 dans Λ₋₄^#/Λ₋₄. La partie 3 de
   det Λ₋₄ = det Λ₃' (complément orthogonal dans le réseau unimodulaire Z⁹⁹) vaut 9, car
   [Λ₃' : Λ₃ ⊕ Z1] divise 11 : pour u ∈ Λ₃', 9(A − 3I)u = (Σu)1, donc 9 | Σu. Donc la partie 3 est Z/9.
   Sa composante de Jordan 9^{±1} est d'échelle paire : 3-excès = 1·(9 − 1) = 8 ≡ 0, quels que soient les signes.
4. **Partie 7 : (Z/7)^α avec α = 14 + k** (preuve de L2 : sur Z₇, (A − 3I)(1^⊥) = 7Λ₋₄^#, d'où rank₇(A − 3I) = α + 1 ;
   par définition rank₇(A − 3I) = 15 + k). Sur Z₇ : Λ₋₄ = U ⊥ 7V, U et V unimodulaires, rang U = 30 − k,
   rang V = 14 + k. Condition du déterminant : (det U | 7)(det V | 7) = (9 | 7) = +1, car det Λ₋₄ = 9·7^α.
5. **Formule d'oddité** (Conway–Sloane, SPLAG ch. 15 ; Λ₋₄ pair de déterminant impair, donc oddité 2-adique nulle) :
   44 + 8 + 6(14 + k) + 4δ_V ≡ 0 (mod 8), où δ_V = [(det V | 7) = −1]. Avec k = 2m : **δ_V ≡ m (mod 2)**.
6. **Si k = 30**, alors U = 0, donc (det V | 7) = (9 | 7) = +1 et δ_V = 0. Or m = 15 impose δ_V = 1. **Contradiction.** ∎
   *Complément.* Pour k < 30, δ_U = δ_V = m (mod 2). Une forme quadratique de dimension paire 2r = 30 − k sur F₇ est
   hyperbolique ssi son discriminant vaut (−1)^r à un carré près. Comme (−1 | 7) = −1, cela demanderait
   (−1)^m = −(−1)^m, ce qui est impossible. Donc U mod 7 n'est jamais hyperbolique, et U = 0 (le cas k = 30) est
   exclu. C'est la même contrainte, dite autrement.

## 3. Vérifications (`code/genus_tools.py`, `code/eigenlattice_check.py`)
- **Conventions (p-excès, signes, oddité) :** A₂, A₄, A₆, E₆, E₈, plus 300 réseaux impairs et 2000 réseaux pairs
  aléatoires de déterminant impair. **0 échec** de la formule d'oddité.
- **Le schéma de preuve sur des graphes qui existent**, calcul direct des réseaux propres (base entière du noyau,
  Gram, forme de Smith, symboles de Jordan) :
  - **Petersen** (r − s = 3, n = 10). rank₃(A − I) = 5 et la partie 3 de disc(Λ₋₂) est de rang 4 (α = rang − 1 ✓).
    Partie « de n » : Z/5 cyclique ✓. Λ₋₂ est entièrement 3-divisible (le cas analogue de k = 30). Ce cas est
    **permis** parce que la partie unité du déterminant, 5, n'est pas un carré mod 3 : ε = −1, exactement le signe
    que demande l'oddité ✓.
  - **T(7)** (r − s = 5, n = 21). rank₅(A − 3I) = 7, partie 5 de rang 6 ✓. Λ₃ est entièrement 5-divisible, ce qui est
    permis car (7 | 5) = −1 ✓.
  - **T(8)** et **srg(9,4,1,2)** : α = rank_p − 1 ✓ ; les conditions de déterminant et d'oddité sont vérifiées ✓.
- **Pour 99**, la partie unité est 9, un **carré** mod 7. Le signe est donc forcé à +1 et l'oddité échoue.
- **Seconde dérivation, indépendante :** le réseau local K₋₄(x) (rang 30, det 2²¹·7^k, L17) devient lui aussi
  entièrement 7-divisible à k = 30. Son oddité (avec l'oddité 2-adique 6 qu'implique L17) et
  (2²¹ | 7) = +1 donnent la même contradiction.

## 4. Priorité
C. A. van Eijl, *On the p-rank of the adjacency matrices of strongly regular graphs*, mémoire de master, TU Eindhoven,
1991 (dir. A. E. Brouwer ; texte lu : win.tue.nl/~aeb/preprints/361304.pdf), théorème 3.5(iii) : r_p(A + τI) ≤ min(f, g) + 1
(ici 45). Version article : A. E. Brouwer, C. A. van Eijl, J. Algebraic Combin. 1 (1992). *(Correction du 25/09 : le
fichier 361304.pdf est le mémoire, pas l'article.)* La remarque du mémoire (idempotent c₁E₁ avec p | c₁₀, p | c₁₂, p ∤ c₁₁) ne s'applique pas à 99 : 63E₋₄ = 28I − 8A + B, et
7 ∤ c₁₂ = 1. Aucun argument de genre ni d'oddité dans ce texte. **Le raffinement semble nouveau** ; la méthode (symboles
de Conway–Sloane, formule d'oddité) est classique.

## 5. Ce que cela change
1. **La synthèse (notes/100) doit être corrigée.** Le profil « générique » de sa proposition de cohérence (k = 30)
   est **exclu**. Le profil de torsion maximale reste cohérent avec k = 28, donc il n'y a toujours pas de
   contradiction, mais le corpus contient désormais un plafond.
2. **La structure générique est interdite.** Pour une structure « au hasard », le 7-rang de la matrice locale
   M_x = H + 4I + 3S + P' + 5J (84 × 84) vaudrait son rang rationnel, 30 : c'est k = 30. L22 dit que **chaque
   sommet** de Γ a une matrice locale 7-dégénérée d'au moins 2 dimensions (rank₇ M_x = k ≤ 28, pour tout x, avec le
   même k). C'est la première contrainte exacte du corpus qui pénalise le régime « tordu générique », celui où
   aucune moyenne ne voyait rien.
3. **Le verrou prend une forme précise.** Il suffirait de montrer qu'en un seul sommet la structure locale force
   rank₇(M_x) ≥ 29. Par exemple, que la torsion forte rend M_x 7-générique : k serait alors 30, ce que L22 interdit.
   Les minorations locales existantes s'arrêtent à 22 (L21, droite générique). Il faut maintenant des structures de
   plus de 29 sommets de Γ₂(x), ce qui fait entrer les arêtes génériques inconnues. C'est la technique des relations
   (L20 ter) à k = 28, sur quatre étoiles (44 lignes, au moins 16 relations forcées).
