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

## 4. Portée
- La question (c′) devient : **la torsion locale mod 7 d'une droite peut-elle être équilibrée ?** C'est-à-dire : existe-t-il
  φ ≠ 0 constant sur aucune réunion de composantes, avec L_G φ = 0 et Σ_{ombre(y)} φ = 0 pour les 60 lointains y ?
- Sur Q, l'équilibre vient de la positivité (variance nulle). Mod 7, il faudrait une raison arithmétique. Aucune n'est
  connue, et la torsion aléatoire n'est jamais équilibrée (contrôle du §1).
- Non résolu : c'est une condition de 60 équations par vecteur, sans argument uniforme pour l'instant.
