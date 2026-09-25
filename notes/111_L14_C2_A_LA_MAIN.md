# 111 — L14 pour |C| = 2 démontré à la main : 4 voisins communs disponibles, 5 exigés

*25/09, soir. L14 (« deux étiquettes tordues ne suffisent pas ») ne reposait que sur du SAT non certifié (notes/30).
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
2. **Paires 14, 15, 16, 34, 35, 36.** Soit z ∈ Q₁₄ ; z est de type Hamming, donc tous ses s_m sont nuls.
   - Les classes 5 et 6 ont chacune 4 paires, toutes complètes. D'où n₀₅ = n₂₅ = n₃₅ = n₅₆ = 1 et
     n₀₆ = n₂₆ = n₃₆ = n₅₆ = 1.
   - Les classes 0, 2, 3 donnent ensuite n₀₂ + n₀₃ = 2, n₀₂ + n₂₃ = 2 et n₀₃ + n₂₃ = 2. Avec n₂₃ ≤ 1, on obtient
     n₀₂(z) = n₀₃(z) = n₂₃(z) = 1.
   - Même chose pour les cinq autres paires.
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

## 4 bis. Pour tout |C| : les deux torsions ont le même graphe de classes
Soit m = |C| (2 ≤ m ≤ 5). Le graphe de classes de τ_{0⁺} sur C a pour sommets les classes de C, et une arête c – c′
par étiquette ℓ ∈ c avec τ_{0⁺}(ℓ) ∈ c′. C'est un multigraphe 2-régulier sans boucle. Soit e₀(c, c′) le nombre de ses
arêtes entre c et c′, et e₁(c, c′) de même pour τ_{1⁺}.

**Lemme.** e₀(c, c′) = e₁(c, c′) pour tous c ≠ c′ dans C.

*Preuve.* On compte les arêtes entre Q₀c et Q₁c′, qui sont disjointes, de deux façons.
- Par les fentes, comme au §2.1 : en A_c = 0⁺c⁺, l'équation de la classe 1 donne Σ_{c″∈C∖c} n₁c″ = m − 2. Celle de chaque
  classe c″ donne n₁c″ ≥ 1 − [c″ = classe de τ_{0⁺}(c⁺)]. Donc A_c a un voisin dans Q₁c′ si c′ n'est pas la classe de
  τ_{0⁺}(c⁺), et aucun sinon. Les sommets non tordus 0⁻c^± en ont exactement un.
- Du côté de Q₀c, on obtient e(Q₀c, Q₁c′) = 4 − e₀(c, c′). Du côté de Q₁c′, on obtient 4 − e₁(c, c′). ∎

Conséquences :
- m = 3 : les deux graphes sont des triangles, ce qui est automatique.
- m = 4 : même 4-cycle, ou mêmes deux 2-cycles. m = 5 : même 5-cycle, ou même partition en 2-cycle et 3-cycle.
- Si le graphe commun a un 2-cycle {c, c′}, le bloc {A_c, B_c} × {E_{c′}, F_{c′}} est **étanche** comme au §4 : aucune
  arête, aucun terme de couplage, et exactement 4 voisins communs disponibles. La contradiction suit dès que les trois
  doubles de Q₀c s'apparient à Q₁c′. Cet appariement est automatique pour m = 2 ; pour m ≥ 4, il reste à prouver.

## 5. Contrôle et portée
- **Relecture indépendante** (session « structures », 25/09, sur l'état eb7a40f). Les quatre points délicats ont été
  refaits à la main, dans les cas P et R :
  - les fentes (§2.3 par le lemme U avec I = ∅ en 01 et 23) ;
  - l'absence d'autre voisin commun spécial dans Q₀₂ et Q₁₃ ;
  - les tableaux du bloc et la vacuité des termes de couplage ;
  - la demande ≥ 5.
  Dépendances : R0, L12, L13 et notes/108. La réduction initiale (même C, ρ₂ et ρ₃ échangeant 0⁺ et 1⁺) n'a pas été
  refaite par le relecteur.
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
- **|C| = 5 (jamais lancé en SAT) : bilans exacts, sans contradiction** (preuve, même méthode). Les seuls quadrangles
  qui portent des voisins communs génériques des sommets de Q₀c ∪ Q₁c sont les Q_R avec R ⊆ C ∖ c : 24 sommets, dont
  chacun a exactement deux voisins dans Q₀c ∪ Q₁c.
  - Les déficits μ/λ de Q₀c ∪ Q₁c totalisent exactement 24 : 3 doubles de Q₀c, 3 de Q₁c, et 18 unités croisées (2 pour
    CH et DG, 1 pour les 14 autres paires ou arêtes croisées). Il n'y a **aucun jeu** : chaque sommet externe comble
    exactement un déficit, et aucun voisin commun « mixte » n'existe (les T_{0⁺}(A_c) sont fermés à c).
  - Pour c ≠ c′, le bilan des 16 paires de Kneser Q₀c × Q₁c′ donne Σ_{z ∈ Q_R, R ⊆ C∖{c,c′}} n₀c(z)·n₀c′(z) =
    12 − 3e₀(c, c′).
  - Sur les 40 sommets de type Hamming des Q_R (R ⊆ C), (n₀c) vaut (1,1,1) pour 25 d'entre eux et une permutation de
    (2,1,0) pour 15.
  - Tout cela est cohérent (Σ sur les 10 paires : 80 + 25 = 120 − 3·5). Il faut un argument plus fin : la structure de
    Petersen des Q_R, R ⊆ C, et μ entre classes différentes.
- **Méthode.** C'est la première fois que les doubles (arêtes génériques non bijectives) sont contrôlés à la main. Le
  mécanisme : μ entre deux sommets d'un même quadrangle force un double, qui consomme du μ ailleurs. Le bilan est local
  (bloc {A, B} × {E, F}) : l'offre vaut 8 moins les voisins spéciaux, la demande au moins 5.
