# 109 — Le cœur : torsion maximale. Ce qui se transporte de L8, ce qui ne se transporte pas

*25/09, soir. Discussion entre sessions (C1, C2, « structures »). Consigne : attaquer le plafond, pas les planchers ;
dire tout de suite si un premier geste est vide. Tous les énoncés sont prouvés à la main, sauf mention.*

## 0. Résumé
| énoncé | statut | apport |
|---|---|---|
| structure spéciale en torsion maximale : 4 voisins spéciaux par sommet, 8 génériques | preuve | cadre |
| identité des doubles : Σ_v Σ_R C(d_R(v), 2) = 168 − e_int | preuve (tautologie de double comptage) | **vide** (critère 3) |
| en torsion maximale générique : 2 doubles par sommet en moyenne, donc pas de bijections de Kneser | preuve | **l'holonomie de L8 ne se transporte pas** |
| budget par paire de classes : Σ_w C(n_R(w), 2) = 8 − s_R − a_R − i_R | preuve (C2, « structures ») | même tautologie, paire par paire |
| identités du second ordre Σ_v d_P d_R = 32 − e, 24 − e, 64 − 2e | preuve | vides : elles ne tuent même pas L14 |
| **schéma des droites à P = 0** : Y = X₂ − X₀ vérifie (Y − 4)(Y + 17) = 0 | preuve | identité d'ordre 9 (au-delà de notes/91) |
| forme locale de l'identité Y pour deux droites sécantes | preuve (torsion maximale générique) | à exploiter |

## 1. Structure en torsion maximale
Torsion maximale en x : chaque τ_a sans boucle (jamais c ↦ c̄), chaque ρ_α sans point fixe (L13 : tout le monde tord
tout). Pour y = {a, b}, les voisins contenant a, b, ā, b̄ sont exactement les 4 spéciaux T_a, T_b, S_α, S_β. Dans le cas
**générique** (aucune coïncidence τ/ρ), ils sont distincts et situés dans 4 paires T(7)-adjacentes. Les 8 autres voisins
sont dans des paires disjointes de P(y).

## 2. Les doubles, et pourquoi les bijections disparaissent
**Identité.** d_R(v) = |N(v) ∩ Q_R|. On a Σ_v d_R(v)² = Σ_{y,y′ ∈ Q_R} (H²)[y,y′] = 64 − 2e_RR, et Σ_v d_R(v) = 48, d'où :

  Σ_v Σ_R C(d_R(v), 2) = 168 − e_int.

- *Ce qu'elle compte.* Un « double », c'est deux voisins de v dans un même Q_R, donc deux sœurs ou deux antipodes de Q_R.
  Chaque couple de sœurs non adjacentes a exactement un voisin commun hors de l'étiquette partagée ; chaque couple
  antipodal non adjacent en a deux. Cela fait 4 + 4 = 8 par paire, et 168 au total : la tautologie est exacte (forme
  paire par paire : budget 8 − s_R − a_R − i_R, C2 et « structures »).
- *Conséquence.* En torsion maximale générique, e_int = 0, donc chaque sommet a **2 doubles en moyenne**. Les graphes
  bipartis B_PR ne sont pas des couplages partiels.
  - Or l'objet d'holonomie de L8 (bijections de Kneser φ_PR, droites = points fixes, parité ℓ ∈ {0, 2, 4}) exige des
    bijections.
  - **Il ne se transporte pas.** Le premier geste « n_R(y) ≤ 1 » (couplage μ(y) des 4 classes spéciales) décrit un cas
    non générique.
- *Contrôle.* Même les identités du second ordre (Σ_v d_P d_R = 32 − e_PR, 24 − e_PR, 64 − 2e_PP) ne réfutent pas L14.
  Il reste 2 160 solutions sur les 6 859 solutions entières du système linéaire (`code/slot_second_order.py`). Le niveau
  « comptes par paires de classes » est trop grossier.

## 3. Le modèle de Fano (C2, Théorème F) sans σ
Un sommet est **tordu selon Fano** si τ_a (a dans la classe i) envoie la classe j sur la classe k = Φ(i, j), pour un plan
de Fano Φ des classes. Les deux partenaires τ de y ∈ Q_ij tombent alors dans la classe k.
- Les fentes (2 pour k, 3 et 3 pour les classes des ombres, 4 et 4) sont réalisables sans double local.
- Avec σ, le budget par paire est 4 : c'est ce qui tue le modèle chez C2 (8 doubles contre 4). **Sans σ, le budget
  est 8** : la contradiction ne se transporte pas telle quelle.

## 4. Nouveau : le schéma des droites à P = 0
Relations entre droites : sécantes (degré 18), puis, pour deux droites disjointes, e = 0, 1, 2 arêtes (e = 3 serait un
prisme, absent à P = 0). Avec 𝓔 = NᵀAN et la projection E₋₄, on a 7NᵀE₋₄N = 9I + 3A_dual − 𝓔 + J. D'où, à P = 0 :

  7·Gram₋₄ = 4I + X₀ − X₂, et donc **(Y − 4)(Y + 17) = 0 pour Y = X₂ − X₀**.

Gram₋₄ a pour valeurs propres 21 (×44) et 0 (×187).
- En général, Y_P = X₂ + 2X₃ − X₀ vérifie la même identité.
- Degrés à P = 0 (L16) : n₂ = 36, n₁ = 144, n₀ = 32.
- La relation E₃ n'apporte rien de plus : Z = −18X₀ − 7X₁ + 4X₂ = −7(J − I − A_dual) + 11Y. La relation e = 1 reste le
  seul degré de liberté ; ce n'est pas nécessairement un schéma d'association.

**Forme locale.** Soient L = {p, a, ā} et M = {p, b, b̄} deux droites sécantes en p (classes α, β). On a
(Y²)_{LM} = 0. Tous les termes se lisent en p :
- droites par une étiquette c ∉ α ∪ β : Y_L = Y_M = 1 exactement quand la paire τ_c correspondante relie une étiquette de
  α à une étiquette de β, d'où Σ_c π_c(α, β) ;
- droites intérieures : seules les droites de mates contribuent. Les droites pures utilisent 6 classes et n'en évitent
  qu'une.

En torsion maximale générique (une paire de mates par droite de mates), pour chaque p et chaque paire {α, β} :

  Σ_{c ∉ α∪β} π_c(α, β) + n₀₀(α, β) − deg_{M_α}(β) − deg_{M_β}(α) = 0.

- M_γ est le multi-ensemble des paires de classes évitées par les 12 droites de mates doublées en γ.
- n₀₀(α, β) est le nombre de droites de mates qui évitent exactement {α, β}.
- La somme sur β de ces équations est automatique : 24 = 24. Il reste **14 équations indépendantes par sommet**. Elles
  lient les statistiques de paires τ aux positions des troisièmes points des droites de mates.
- **Statut.** C'est une identité d'ordre 9 (trois droites), hors de la hiérarchie d'ordre 8 de notes/91. Elle est vraie
  dans tout Γ. Reste à savoir si elle mord, ou si elle suit des fentes et de (K) : non fait.

## 5. Bilan honnête
- Le mécanisme de L8 (bijections, holonomie, parité, squelette rigide) est propre au voisinage des grilles complètes.
- En torsion maximale, tous les comptages du premier et du second ordre sont des tautologies.
- La seule piste nouvelle de cette séance est l'identité du schéma des droites (§4). Elle est d'ordre 9 et sa forme
  locale relie τ aux droites de mates. Elle n'est pas encore exploitée.
