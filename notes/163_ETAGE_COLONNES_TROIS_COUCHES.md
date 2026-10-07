# 163 — L'étage colonnes de la route Ω : forme symétrique à trois couches, mesures et coût (07/10)

*Suite des notes 157–158. Demande de l'utilisateur : reprendre le moteur des colonnes de C1. Code : `code/omega/`
(`colmodel.py`, `colgram.py`, `colsolve.c`, `coldrive.py`, `colsat.py`).*

## 1. Théorème : forme symétrique à trois couches (vérifiée exactement)

**Cadre.** T = {v, a, a′} est un triangle d'un srg(n,k,1,2), et m = k − 2. Les trois couches sont :
- E = N(v) ∖ {a, a′} ;
- L_a = N(a) ∖ {v, a′} ;
- L_{a′} = N(a′) ∖ {v, a}.

Chaque label est identifié à l'unique élément de E qui lui est adjacent. La structure C se code alors par quatre
applications de [m] :
- M, les mates dans E ;
- τ_a, τ_{a′}, les appariements de L_a et L_{a′} ;
- σ : L_a → L_{a′}, défini par {a,z} ∼ {a′, σz}.

**Énoncé.**
- Un sommet lointain w (non adjacent à T) rencontre chaque couche en exactement 2 sommets non appariés. C'est donc un
  **triplet de paires** (p₀, p₁, p₂), où p_i est une arête du graphe cocktail CP_i (K_m privé de l'appariement de la
  couche i).
- Sur chaque couche, w ↦ p_i est une **bijection** sur les m(m−2)/2 arêtes de CP_i.
- Les matrices d'incidence croisées N_ij[u][u′] = #{w : u ∈ p_i(w), u′ ∈ p_j(w)} sont **imposées par C** :

  N₀₁ = 2J − I − M − T_a − S,  N₀₂ = 2J − I − M − T_{a′} − Sᵀ,  N₁₂ = 2J − I − S − S·T_a − T_{a′}·S

  (I, M, T_a, T_{a′}, S désignent les matrices de permutation, dans les conventions de `colmodel.predicted`).

**Preuve.** λ = 1 et μ = 2 appliqués aux paires de sommets de C, en retirant les voisins communs situés dans T ∪ C.

**Vérification.** Formules exactes et bijectivité sur les trois couches pour 143 triangles de BvLS, 143 triangles du
nouveau 243 et les 18 triangles de Paley(9) (`colmodel.py`).

**Conséquence.** L'étage colonnes est exactement un **plan à blocs** : 60 blocs de taille 6 (2 points par couche) sur
les 36 points de C. Chaque point est dans 10 blocs, et les concurrences de paires sont prescrites :
- 1 pour une paire non appariée d'une même couche, 0 pour une paire appariée ;
- N_ij entre deux couches.

Les trois couches jouent des rôles symétriques, car T = {v, a, a′} est un triangle.

## 2. Vue de Gram
B_C est la matrice d'incidence lointains × C (60 × 36). Alors B_Cᵀ B_C = G_C, entièrement fixée par C : blocs
diagonaux (m−3)I + J − (appariement), blocs hors diagonale N_ij.
- **Sur les vrais graphes** : B_Cᵀ B_C = G_C exactement, de rang 3m − 2 (58 pour 243).
- **Sur 6 structures C aléatoires de 99** : G_C est **toujours** semi-définie positive de rang 34. Ce test ne filtre
  donc aucune C.
- **Leverage** rᵀG⁺r ≤ 1 à la racine : il n'élimine presque aucun des 127 000 à 192 000 triplets admissibles. Le levier
  spectral ne peut mordre qu'en profondeur.

## 3. Taille de l'espace des C
- C = (τ_a, τ_{a′}, σ), M étant fixé : 10395² · 12! ≈ 5,2·10¹⁶ structures étiquetées.
- 78,7 % sont localement valides (échantillon de 4 000).
- Symétries : 2⁶·6!·6 = 276 480.
- On obtient **≈ 1,5·10¹¹ classes**, ce qui confirme l'ordre de grandeur de la note 158.

## 4. Heuristique de comptage
**Par paire de couches.** Pour φ : E(CP₀) → E(CP₁) aléatoire, chaque case de N vaut environ Bin(10, 1/6). On a 121 cases
libres, à cible 2 (probabilité 0,29) ou 1 (probabilité 0,32). D'où P(incidences = N₀₁) ≈ 10⁻⁶³, et environ
60!·10⁻⁶³ ≈ **10¹⁹ bijections par paire de couches**. Chaque paire de couches, prise seule, est peu contrainte.

**Les trois couches ensemble.** (60!)²·(10⁻⁶³)³ ≈ **10⁻²⁵ solution attendue par C aléatoire**. L'étage colonnes est donc
massivement surdéterminé, mais seulement globalement. La contradiction n'apparaît que tard dans toute recherche, et
c'est la signature d'un problème de plans difficile.

## 5. Mesures (à compléter)
**Solveur dédié** (`colsolve.c` : couverture exacte avec capacités de cases, liens dansants par drapeaux).
- Environ 16 000 nœuds/s.
- Sur des **instances témoins plantées** (solution garantie), **aucune solution trouvée en 10⁶ nœuds**.

**kissat sur un encodage propre** (`colsat.py` : permutations X, Y, compteurs totalisateurs ; ≈ 1,9·10⁵ variables,
10⁶ clauses).
- Instances plantées : **UNKNOWN en 300 s**.
- Vraies structures C de 99 : voir §5 bis.
