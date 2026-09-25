# 111 — L14 pour |C| = 2 démontré à la main : 4 voisins communs disponibles, 5 exigés

*25/09, nuit. L14 (« deux étiquettes tordues ne suffisent pas ») ne reposait que sur du SAT non certifié (notes/30).
Pour |C| = 2, voici une preuve courte : le comptage des fentes (notes/108), les « doubles » imposés par μ, puis un
comptage de voisins communs. La seule vérification machine (`code/l14_c2_check.py`) recalcule les tableaux de voisins
communs, sans aucune recherche.*

## 1. Cadre
En x, exactement deux étiquettes tordent : a = 0⁺ (classe 0) et b = 1⁺ (classe 1). Par R0, L12 et L13, elles tordent le
même ensemble C = {2, 3}. Les classes 4, 5, 6 ne sont tordues par personne, et 0⁻, 1⁻ ne tordent rien.
- Paires incomplètes : 02, 03, 12, 13. Toutes les autres sont complètes, et leurs quadrangles sont parfaits (notes/108
  (Q) : n_R(y) ≤ 1 si R est complète).
- Ombres (L13) : ρ₂ et ρ₃ échangent 0⁺ et 1⁺ ; les autres ρ sont triviales.
- Sans perte de généralité (on renomme 3^±), τ_{0⁺} : 2^s ↔ 3^s. Deux cas pour τ_{1⁺} : **P** (2^s ↔ 3^s) et
  **R** (2^s ↔ 3^{−s}).
- Notations : Q₀₂ = {A = 0⁺2⁺, B = 0⁺2⁻, C = 0⁻2⁺, D = 0⁻2⁻}, qui induit le chemin A – C – D – B.
  Q₁₃ = {E = 1⁺3⁺, F = 1⁺3⁻, G = 1⁻3⁺, H = 1⁻3⁻}, qui induit le chemin E – G – H – F. (A ≁ B car
  τ_{0⁺}(2⁺) ≠ 2⁻ ; les autres arêtes sont des droites par des étiquettes non tordues.)

## 2. Ce que les fentes imposent (notes/108 (F), (Q))
1. **Voisins spéciaux de A** : 0⁺3⁺ (droite par 0⁺), C (droites par 2⁺ et ombre par la classe 0), et 1⁺2⁻ (ombre par
   la classe 2, car ρ₂(0⁺) = 1⁺). D'où s₁ = s₃ = 1.
   - Les classes 4, 5, 6 donnent n_R(A) = 1 pour les 9 paires complètes disjointes de 02, puis **n₁₃(A) = 0**.
   - De même pour B, et symétriquement pour E, F (n₀₂(E) = n₀₂(F) = 0).
   - C et D ont exactement un voisin dans chacune des 10 paires disjointes de 02.
2. **Paires 14, 15, 16, 34, 35, 36.** Un sommet z de Q₁₄ vérifie n₀₂ + n₀₃ = 2, n₀₂ + n₂₃ = 2, n₀₃ + n₂₃ = 2, avec
   n₂₃ ≤ 1 ; donc n₀₂(z) = 1. Même chose pour les cinq autres paires.
3. **Paires 45, 46, 56.** Q₀₁ et Q₂₃ sont complètes et couplées parfaitement à Q_R, donc n₀₁(z) = n₂₃(z) = 1. Les
   fentes des classes 0, 1, 2, 3 donnent alors **n₀₂(z) = n₁₃(z) = p_z** et **n₀₃(z) = n₁₂(z) = 2 − p_z**, avec
   p_z ∈ {0, 1, 2}.

## 3. Les doubles
Les paires non adjacentes de Q₀₂ sont AB, AD et BC.
- A et B ont pour voisin commun l'étiquette 0⁺. A et D ont C ; B et C ont D. Aucun autre voisin commun n'est spécial
  (contrôle au cas par cas par τ et ρ).
- Il manque donc à chacune de ces paires exactement un voisin commun générique z, avec n₀₂(z) = 2. Par le §2, z est
  dans Q₄₅ ∪ Q₄₆ ∪ Q₅₆, avec p_z = 2.
- Ainsi les sommets de p = 2 sont exactement trois : z_AB, z_AD, z_BC.
- Par symétrie, ce sont aussi les trois doubles de Q₁₃. Leurs ensembles N₁₃(z) parcourent les paires non adjacentes
  de Q₁₃ : **EF, EH, FG**, chacune une fois.

## 4. Le comptage
Pour y ∈ {A, B} et w ∈ {E, F}, on a y ≁ w (§2.1), donc exactement 2 voisins communs.
- **Voisins communs spéciaux** (tous ceux qui partagent une classe avec y ou w) :
  - cas P : (A,E) : aucun ; (A,F) : 0⁺3⁺ et 1⁺2⁻ ; (B,E) : 0⁺3⁻ et 1⁺2⁺ ; (B,F) : aucun ;
  - cas R : un chacun, à savoir 1⁺2⁻, 0⁺3⁺, 0⁺3⁻, 1⁺2⁺.
  - Dans les deux cas, le total vaut 4. Aucun terme de couplage n'intervient, car A, B n'ont pas de voisin dans Q₁₃,
    ni E, F dans Q₀₂.
- **Disponible** : les voisins communs dans Q₄₅ ∪ Q₄₆ ∪ Q₅₆, sommés sur les 4 couples, valent 8 − 4 = **4**.
- **Exigé** par les seuls doubles :
  - z_AB compte pour (A, w) et (B, w) pour chaque w ∈ N₁₃(z_AB) ∩ {E, F} ;
  - z_AD compte pour (A, w), et z_BC pour (B, w).
  - Le total est |N(z_AB) ∩ EF| + Σ_{trois doubles} |N ∩ EF| = |N(z_AB) ∩ EF| + (2 + 1 + 1) ≥ **5**, car toute paire
    non adjacente de Q₁₃ rencontre {E, F}.
- **5 > 4 : contradiction.** ∎

**Donc L14 est démontré à la main pour |C| = 2**, dans les deux motifs (P et R), sans utiliser le couplage B₀₂,₁₃ entre
les moitiés non tordues.

## 5. Contrôle et portée
- `code/l14_c2_check.py` recalcule, à partir de τ et ρ seuls, les voisins communs spéciaux de tous les couples
  (y, w) ∈ Q₀₂ × Q₁₃, pour les deux cas et les deux couplages B₀₂,₁₃ possibles. Il retrouve les tableaux du §4 et
  vérifie qu'aucune affectation des trois doubles n'est compatible (0 sur 6 dans chacun des 4 cas).
- **|C| ≥ 3 reste au SAT** (|C| = 3 et 4 UNSAT, |C| = 5 jamais lancé). L'argument ne passe pas tel quel, pour deux
  raisons :
  - un sommet tordu a maintenant des voisins génériques dans les autres Q₁c′, ce qui donne plus de voisins communs
    disponibles (l'offre croît en |C|², la demande en |C|) ;
  - les doubles de Q₀c peuvent s'apparier avec des Q₁c′ différents.
  - Pour |C| = 3, le graphe de classes de τ_{0⁺} sur C est nécessairement un triangle (pas de boucle), donc sans le
    2-cycle qui rend le bloc {A, B} × {E, F} étanche.
- **Méthode.** C'est la première fois que les doubles (arêtes génériques non bijectives) sont contrôlés à la main. Le
  mécanisme : μ entre deux sommets d'un même quadrangle force un double, qui consomme du μ ailleurs. Le bilan est local
  (bloc {A, B} × {E, F}) : l'offre vaut 8 moins les voisins spéciaux, la demande au moins 5.
