# 126 — L21 raffiné : une droite dégénérée ne fait baisser k que par son noyau local « équilibré »

*26/09, nuit. C1, tâche (c′) (« toutes les droites 7-dégénérées »), mathématiques pures. DÉRIVÉ = preuve écrite ;
contrôle exact mod 7 sur des boules dégénérées aléatoires. Relu contre notes/99 (L21), 102 (§4, §8) et 124 : le cas
d(L) ≥ 2 de la condition d'image n'y est pas traité.*

## 0. Énoncé
Soit L une droite, B sa boule (39 points), Q = A − 3I + 3J mod 7, M = A[N(L), F] l'incidence des ombres (36 × 60) et
L_G = 3I − A_{G(L)}. On pose :
- E_L = {φ ∈ F₇^{N(L)} : sommes par couche nulles, L_G φ = 0}. C'est le noyau local « supplémentaire », de dimension
  d(L) − 1 (notes/99 : d(L) = composantes + 7-rang du groupe critique) ;
- r(L) = rang₇ de Mᵀ restreinte à E_L, et r₀(L) = dim ker(Mᵀ|_{E_L}), de sorte que r + r₀ = d − 1.

**Théorème.** 14 + k = (37 − d(L)) + 2r(L) + ρ(L), avec ρ(L) ≥ 0 le rang d'un complément de Schur résiduel. Donc :

  **k ≥ 23 − d(L) + 2r(L) = 22 + r(L) − r₀(L).**

Pour d = 1, on retrouve L21 et rang R_L = k − 22 (notes/102 §8).

## 1. Preuve
- **Radical de Q_BB.** D'après notes/102 §4, F³⁹ = (F^L ⊕ U) ⊥_Q U^⊥ et Q|_{U^⊥} = −L_G|_{U^⊥}. Comme U ∩ U^⊥ = 0 mod 7
  (12 est inversible), rad Q_BB = rad(T) ⊕ E_L, avec rad(T) de dimension 3.
  - rad(T) est engendré par les deux vecteurs propres 3 du quotient et par h = 1_L − 1_{N(L)} (notes/124 §1, erratum).
- **Le radical trivial est tué par Q_FB.** Chaque lointain voit 2 points par couche, 6 en tout. Sur un lointain y, on a
  donc Q_FB g_b = 2Σb_p + 3·0 = 0, et Q_FB h = −6 + 3·(3 − 36) = −105 ≡ 0.
- **Sur E_L**, Q_FB φ = Mᵀφ, puisque Σφ = 0.
- **Congruence par blocs.** Base de B adaptée à B′ ⊕ W, avec W = rad Q_BB et Q_BB|_{B′} inversible. On élimine le bloc
  B′ × F. Il reste [[0, Y],[Yᵀ, Z′]] sur W ⊕ F, où Y = Q_{W,F} est de rang r(L).
  - Dans une base où Y = [[I_r, 0],[0, 0]], ce bloc est congru à H^r ⊥ (reste), H étant le plan hyperbolique. D'où
    rang Q = rang Q_BB + 2r + ρ. ∎
- **Contrôle exact** (`code/x31_l21_refined_check.py`) : 10 boules aléatoires avec d = 2 et une partie lointaine
  aléatoire (2 ombres par couche). On trouve rang Q_BB = 37 − d, le radical trivial tué par Q_FB, r = 1 (la torsion
  aléatoire n'est jamais équilibrée) et ρ ≥ 0.

## 2. Ce que mesure r₀ : les vecteurs propres mod 7 portés par N(L)
- **r₀(L) = dim{z ∈ F₇⁹⁹ : supp z ⊆ N(L), Qz = 0}.**
  - Les lignes de L donnent 10Σz = 0 et des sommes par couche nulles.
  - Les lignes de N(L) donnent L_G z = 0, et les lignes lointaines Mᵀz = 0.
  - Ce sont donc les vecteurs propres 3 mod 7 de Γ portés par les voisins de la droite.
- **Sur Q**, ces vecteurs sont exactement les différences de composantes : A_G z = 3z force z constant par composante,
  et Mᵀz = 0 découle de l'équilibre, c'est-à-dire de la positivité. Donc r₀ ≥ c − 1.
- **Mod 7**, un vecteur de torsion φ vérifie seulement φᵀKφ ≡ 0 (Kφ = 0 automatique, avec K = MMᵀ). Mᵀφ est alors
  isotrope, sans être nul pour autant. **L'équilibre Mᵀφ = 0 d'un vecteur de torsion est une condition de plus : 60
  équations.**

## 3. Conséquences
- **k ≤ 20 ⟹ toute droite vérifie r₀(L) ≥ 2 + r(L).** Chacune des 231 droites porte donc au moins deux vecteurs propres
  mod 7 équilibrés, et chaque vecteur de torsion non équilibré doit être compensé par un équilibré de plus.
  - Avant (L21 brut) : k ≤ 20 demandait seulement d(L) ≥ 3, c'est-à-dire 7-rang ≥ 2 du groupe critique ou G(L) non
    connexe.
- **Une torsion non équilibrée fait MONTER la borne.** Pour une droite connexe de torsion t, on a E_L = torsion, de
  dimension t (1 ∉ U^⊥), et d = 1 + t. D'où k ≥ 22 + t − 2r₀, soit **k ≥ 22 + t si toute la torsion est non
  équilibrée**. *(Coquille corrigée, signalée par « structures » : la première version écrivait 21 + t.)* Par exemple,
  7 | τ une fois (t = 1) sans équilibre force k ≥ 23, donc k ≥ 24.
- **Cas connus.**
  - (4,4,4) sans torsion (Astra : τ = 8640 ou 8100) : d = 3, r₀ = 2, r = 0, donc k ≥ 20 (inchangé).
  - (6,6) à P = S = 0 (notes/125 §5, torsion t ∈ {0, 1, 3} par composante) : d = 2 + t₁ + t₂ et
    k ≥ 21 − (t₁ + t₂) + 2r. Si aucune torsion n'est équilibrée, k ≥ 21 + t₁ + t₂ ≥ 22.
- **À P = S = 0**, il n'y a pas de composante à 4 étiquettes (notes/125 §4). k ≤ 20 impose donc à **chaque droite** un
  vecteur de torsion mod 7 équilibré (hors différences de composantes) : deux si G(L) est connexe, un au moins si le
  profil est (6,6).
- **Signe.** La partie non dégénérée de Q est β_B ⊥ H^r ⊥ (résidu). Au cas extrême ρ = 0, donc
  k = 23 − d + 2r, Witt donne : β non scindée ⟺ β_B non scindée. C'est la condition de L23 et du « cas d impair ≥ 3 »
  de notes/102, transportée à ce nouvel extrême.

## 3 bis. À P = S = 0, une droite (6,6) force k ≥ 22
- **Lemme (aucune torsion équilibrée sur une composante (6,6)).** Soit C une composante (6,6) à maille ≥ 5, avec
  E_C = {φ portée par C : L_G φ = 0, sommes par couche nulles} ≠ 0. Aucun φ ∈ E_C ∖ 0 n'est équilibré.
  - Preuve. Chaque lointain rencontre C en exactement 3 points (équilibre sur Q). La restriction à C de son ombre est
    donc un triplet admissible : pas trois points dans une même couche, pas de paire de partenaires, au plus une arête
    de G. Deux lointains distincts donnent des triplets distincts (λ, μ ≤ 2).
  - Une paire {n, n′} de C est dans exactement λ(n, n′) = K[n, n′] triplets : 0 pour des partenaires ; 1 pour la
    même couche, adjacents ou distance 2 ; 2 pour des couches différentes à distance ≥ 3.
  - Si φ est équilibré, chacun de ces triplets est de φ-somme nulle. Il faut donc, pour chaque paire, au moins λ
    triplets admissibles de φ-somme nulle qui la contiennent.
  - Contrôle exact (`code/x32_balanced_66.py`) : pour chacune des 168 composantes étiquetées avec torsion (144 de
    dim E_C = 1, 24 de dim 3) et chaque φ ≠ 0 à scalaire près, au moins 20 (resp. 12) paires sont en défaut. ∎
- **Conséquence.** Pour une droite (6,6), E_L = ⟨1_{C₁} − 1_{C₂}⟩ ⊕ E_{C₁} ⊕ E_{C₂}.
  - Les vecteurs équilibrés de E_{C₁} ⊕ E_{C₂} ne rencontrent ni E_{C₁} ni E_{C₂}. Ils forment donc le graphe d'une
    application injective, de dimension ≤ min(t₁, t₂).
  - D'où r₀ ≤ 1 + min(t₁, t₂), puis k ≥ 22 + r − r₀ ≥ 21 + |t₁ − t₂|.
  - Par parité, **k ≥ 22**.
- **Bilan à P = S = 0.** k ≤ 20 impose : aucune droite (6,6), et toute droite connexe avec r₀ ≥ 1 + t/2 (une
  torsion en majorité équilibrée). Pour les droites connexes (36 points, ombres de 6 points), le même test par paires
  serait trop faible : la question reste ouverte.
- **Extension à P = 0, S quelconque** (`code/x34_small_components_torsion.py`, `code/x34b_balanced_66_P0.py`).
  - On énumère toutes les composantes à 4 et 6 étiquettes, pour tout P. Filtres : cubique, connexe, λ ≤ 1 et μ ≤ 2
    dans la boule. On obtient 122 composantes à 4 étiquettes et 102 952 à 6.
  - **Une composante à 4 étiquettes n'a de 7-torsion que si elle a des triangles (P > 0).** Même alors, une torsion
    portée par elle seule n'est jamais équilibrée : chaque lointain la rencontre en une paire, et le graphe des paires
    (K > 0) contient des cycles impairs, d'où φ = −φ = 0.
  - Composantes à 6 étiquettes sans triangle (P = 0) avec torsion : 6672 (6024 de dim 1, 624 de dim 2, 24 de dim 3).
    **Aucune n'admet de torsion équilibrée** : test par paires, avec les multiplicités K corrigées pour les 4-cycles.
  - **Donc, à P = 0 (S quelconque) :** une droite (4,4,4) donne exactement k ≥ 20 (d = 3, r₀ = 2, r = 0) ; une
    droite (6,6) force k ≥ 22 ; une droite (4,8) force k ≥ 22, sauf si sa composante à 8 étiquettes porte une torsion
    équilibrée (non testé : l'énumération est trop grosse pour un contrôle court). Les droites connexes restent
    ouvertes.
  - **À P = 0, k ≤ 18** impose donc à chaque droite au moins 3 ou 4 vecteurs de torsion équilibrés (profil (4,8) ou
    connexe). **k = 20** impose que chaque droite soit (4,4,4), ou porte de la torsion équilibrée.

## 3 ter. Le résidu ρ(L) et ce qu'il dit à k = 22, 24
- Par le théorème, **ρ(L) = k − 23 + d(L) − 2r(L)**. Pour une droite générique, ρ = rang R_L = k − 22.
- **Droite connexe de torsion t** : ρ = (k − 22) + t − 2r = (k − 22) + r₀ − r.
  - À k = 22, ρ = r₀ − r ≥ 0. S'il n'y a pas de torsion équilibrée (r₀ = 0), alors r = t = 0 : **à k = 22, toute
    droite connexe sans torsion équilibrée est générique**, donc soumise à l'obstruction de l'étoile d'Astra.
  - À k = 24, ρ = 2 + r₀ − r, donc t ≤ 2 sans équilibre.
- **Droite (6,6) à P = S = 0** : ρ ≤ k − 21 − |t₁ − t₂|. À k = 22, ρ ≤ 1 : le graphe lointain est fixé mod 7 par les
  ombres, à un terme de rang ≤ 1 près. C'est une situation voisine de R_L = 0, où l'étoile d'Astra pourrait
  s'appliquer.
- **Réduction à P = S = 0, k = 22.** Supposons (i) aucune torsion équilibrée sur les droites connexes et (ii)
  l'obstruction de l'étoile uniforme pour les droites génériques. Alors les 231 droites sont (6,6), avec
  |t₁ − t₂| ≤ 1 et ρ ≤ 1. Il resterait à exclure « (6,6) partout ».
- **Pour k = 20 à P = 0.** Sans torsion équilibrée, la seule source de vecteurs équilibrés est la différence de
  composantes (au plus 2, profil (4,4,4)). Donc k ≥ 20, et k = 20 impose « (4,4,4) partout ».
  - Coût en S : une composante à 4 étiquettes a exactement 4 ou 6 quatre-cycles à P = 0 (énumération exacte,
    `code/x33_comp44_c4.py`). « (4,4,4) partout » donne donc 2772 ≤ S ≤ 4158 = n₃, sans contradiction.
  - Au niveau des classes, en x : chaque U apparie les 6 autres classes (Π_U), τ_a envoie B sur Π_A(B), et le lemme E
    impose Π_C(Π_U(C)) ≠ U. Le plan de Fano est exclu par là. Un système cyclique sur Z₇ ({1,2},{3,5},{4,6}
    translatés) satisfait cette condition. Non tranché.

## 3 quater. Théorème conditionnel : sans torsion équilibrée, k ≥ 18
**Hypothèse (NT).** Pour toute droite, les vecteurs équilibrés de E_L sont les seules différences de composantes.
Cela revient à r₀(L) = c(L) − 1, où c(L) est le nombre de composantes de G(L).
- **Composantes à 2 étiquettes par couche.** Ce sont exactement les **composantes prismes**, et chacune porte 2 points
  fixes de l'holonomie.
  - Preuve : τ_u(v) = τ_ū(v) = v̄ et σ préserve {v, v̄}.
  - Si σ(v) = v̄, la composante est K₃,₃, donc μ = 3 : exclu.
  - Donc σ(v) = v et σ(v̄) = v̄ : deux triangles de G(L), et la composante est un prisme.
- **Borne.** Les autres composantes ont au moins 4 étiquettes par couche. D'où c(L) ≤ 3 + p_c/2 ≤ 6, avec p_c le nombre
  de composantes prismes, et fix(σ_L) ≥ 2p_c.
- **Sous (NT)**, on a k ≥ 22 + r − r₀ ≥ 23 − c(L) pour chaque droite. Donc :
  - **k ≥ 17, soit k ≥ 18** (au lieu de k ≥ 10 : L20 bis/ter) ;
  - **k = 18** ⟹ c(L) ≥ 5 pour toute droite. Il y a donc au moins 4 composantes prismes par droite, fix(σ_L) ≥ 8 et
    P ≥ 924. En tout sommet, P(x) ≥ 56, donc |W(x)| ≤ 28. Enfin r = 0 : aucune 7-torsion, puisqu'une torsion non
    équilibrée ferait monter la borne ;
  - **k = 20** ⟹ c(L) ≥ 3 pour toute droite. À P = 0, c'est « (4,4,4) partout » (§3 ter).
- Le régime k = 18 est un régime de **torsion faible** (P ∈ [924, 1151] par L16), c'est-à-dire le côté où les
  planchers du corpus (L8 à L14) mordent. À confronter à ces lemmes.
- (NT) n'est pas démontrée. Elle est démontrée pour les composantes (6,6) à P = S = 0 (§3 bis). La torsion aléatoire
  n'est jamais équilibrée (§1).
- **Structure forcée à k = 18 (sous NT), en tout sommet x.** Chaque droite par x est soit **non tordue** (6 prismes,
  σ_U = id), soit **tordue** (4 prismes et une composante à 4 étiquettes π(U) = {A, B}). Soit T_x l'ensemble des
  classes tordues.
  - *Seules les classes de T_x sont tordues.* Si A ∉ T_x, alors σ_A = id, donc l'holonomie ρ de L13 est l'identité et
    personne ne tord A.
  - *La relation est symétrique.* Les tordeuses de U sont stables par ρ_U = σ_U, sans point fixe, et σ_U fixe les
    étiquettes hors de π(U). Donc « u tord A » ⟺ A ∈ π(U) ⟺ U ∈ π(A).
  - Le graphe des paires tordues est donc **2-régulier sur T_x**, c'est-à-dire une réunion de cycles. Toute étiquette
    d'une classe de T_x tord exactement ses deux voisines : c'est le motif (2, …, 2).
  - L11 exclut le triangle seul, donc |T_x| ≥ 4. On a g(x) = 21 − |T_x| ∈ [14, 17], P(x) = 84 − 4|T_x| et
    |W(x)| = 4|T_x|.
  - Pour |T_x| = 4, c'est le motif **(2,2,2,2) du 4-cycle de notes/112**, où il reste 12 configurations à l'ordre
    deux. Les cycles plus longs (C₅, C₆, C₇, C₃ + C₃, C₃ + C₄) n'ont pas été étudiés.
  - Condition globale : « tordue » est une propriété de la droite. Chaque droite tordue a, en chacun de ses trois
    sommets, deux voisines tordues dans le cycle local.
  - **Piste concrète** : exclure ce régime par la machinerie « côté Hamming » (notes/108, 111, 112). k = 18 tomberait
    alors sous (NT).

## 4. Portée
- La question (c′) devient : **la torsion locale mod 7 d'une droite peut-elle être équilibrée ?** C'est-à-dire : existe-t-il
  φ ≠ 0 constant sur aucune réunion de composantes, avec L_G φ = 0 et Σ_{ombre(y)} φ = 0 pour les 60 lointains y ?
- Sur Q, l'équilibre vient de la positivité (variance nulle). Mod 7, il faudrait une raison arithmétique. Aucune n'est
  connue, et la torsion aléatoire n'est jamais équilibrée (contrôle du §1).
- Non résolu : c'est une condition de 60 équations par vecteur, sans argument uniforme pour l'instant.
