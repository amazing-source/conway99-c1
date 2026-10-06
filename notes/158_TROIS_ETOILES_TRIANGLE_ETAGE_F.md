# 158 — Trois étoiles = un triangle : repère de rang 8, étage F presque forcé, colonnes = vrai goulot (07/10)

*Suite de la note 157 (route Ω). Objectif annoncé : caractériser la condition « trois étoiles » et en tirer une réduction.
Code : `code/omega/`. Les vérifications sont faites sur BvLS243 (λ = 1, μ = 2), seul témoin disponible.*

## 1. Les deux étoiles mates forment la boule d'un triangle
**L'identification.**
- Les étoiles L_a ∪ L_a′ (24 labels) et les éléments E = N(v) ∖ {a, a′} (12 sommets) forment exactement les 36 sommets qui
  touchent le triangle {v, a, a′} : le graphe cubique C à trois couches de 12 de la passation (§6).
- Les 60 labels restants {x, y} (x, y ∈ E non mates) sont les **60 sommets lointains** de ce triangle.
- Une troisième étoile L_b (b ∈ E) ajoute les 10 sommets lointains adjacents à b.

**La structure de C.**
- Chaque couche porte un appariement interne : les mates dans E, τ_a, τ_a′.
- Entre les couches, on a des bijections : x ↔ {a, x}, x ↔ {a′, x}, et σ.
- À symétrie près, il y a ~10³·10³·10³/6 ≈ 2·10¹¹ structures C.

## 2. Théorème du triangle (rang 8)
On note F_μ = {f ∈ E_μ : f nul sur la boule}, restreint aux sommets lointains, B_C l'incidence C × lointains et
Z = ker B_Cᵀ (fonctions sur les lointains de somme nulle autour de chaque sommet de C).

1. F₋₄ ⊂ Z et F₃ ⊂ Z. En effet, si f est nul sur la boule, (Af)_u = μ f_u = 0 en chaque u ∈ C.
2. A_far f = −4f sur F₋₄ et A_far g = 3g sur F₃, car f est nul hors des lointains.
3. **Cas générique** (rang K_boule = 36, rang B_C = 34) : dim F₋₄ = 44 − 36 = **8**, dim F₃ = 54 − 36 = 18, dim Z = 26. On a
   alors **Z = F₋₄ ⊕ F₃**.
4. **Le reste du spectre.** De (A²)_{C,lointains} = 2J − B_C, on tire A_far B_Cᵀ = 2J − B_Cᵀ − B_CᵀA_CC.
   - Sur Z^⊥ = im B_Cᵀ, A_far est donc l'opérateur D_C = −I − A_CC + 1_E1ᵀ transporté, sur un quotient de dimension 34.
   - D_C ne dépend que de C.
   - Le spectre de A_far vaut donc spec(D_C|quotient) ∪ {(−4)⁸, 3¹⁸}. Les traces 0 et 480 en découlent automatiquement.
5. **Repère.** Les résidus des 60 lointains (projections sur E₋₄, orthogonalement à la boule) forment un repère tendu de R⁸.
   Ils sont indexés par les arêtes de CP(6), avec somme nulle en chaque élément de E.
   - Leur Gram vaut P₈ ; la diagonale d_w = (28 − k_wᵀK_boule⁺k_w)/63 est déterminée par la colonne de w.
   - Sur Z, A_far = 3P_Z − 7P₈.

**Vérification exacte sur BvLS** (`triangle_check.py`) : |boule| = 63 et 180 lointains. On trouve dim F_s = 50,
dim F_r = 72, rang B_C = 58 et dim Z = 122 = 50 + 72. Les actions propres sont exactes à 3·10⁻¹⁵ près.

**La condition « trois étoiles ».** Les 10 lointains adjacents à b ont leurs résidus dans R⁸, avec une somme nulle. Le
Gram local G_b (10 × 10, calculable depuis C, leurs colonnes et τ_b) doit donc avoir un rang ≤ 8, au lieu des 9 génériques.
- **C'est une conséquence du théorème, pas une condition supplémentaire.**
- Dans le cas générique, ces 10 lointains engendrent R⁸. Alors N[v] ∪ L_a ∪ L_a′ ∪ L_b contient un complément étoilé, et
  les 50 autres labels sont forcés.

## 3. L'étage F est presque forcé par les colonnes
**L'identité.** La diagonale de A_far P_Z = 3P_Z − 7P₈ donne, pour chaque lointain w :

  Σ_{w′ ∈ N_far(w)} (P_Z)_{ww′} = 3(P_Z)_{ww} − 7d_w,

avec toutes les données venant de (C, B_C). Vérifiée sur BvLS à 5·10⁻¹⁵ près.

**Les équations entières.** Pour chaque u ∈ C :

  #{w′ ∈ N_far(w) : w′ ∼ u} = (2 − A_uw) − |N_C(u) ∩ N_C(w)|.

C'est la relation BF = 2J − B − CB de la passation.

**Mesure sur BvLS** (`far_row_check.py`, `far_forced.py`) :
- donnée par donnée, ces équations ne laissent que **2 voisinages lointains possibles par ligne**, pour chacune des 180 lignes ;
- c'est à comparer aux ~10²² sous-ensembles de taille 16 ;
- le vrai voisinage en fait toujours partie, et les deux candidats satisfont l'identité réelle ;
- la propagation de symétrie entre lignes ne départage pas.

Le « jumeau » formé des candidats alternatifs est examiné en §5.

**Conséquence.** Une fois (C, B_C) connus, le graphe des lointains est déterminé à une ambiguïté binaire près. **Le goulot
n'est pas l'étage F, ce sont les colonnes.**

## 4. Les colonnes : un problème de décomposition
Pour ℓ = {a, z} ∈ L_a, ses 10 voisins lointains forment un graphe simple sur E, sans arête de mates. Ses degrés imposés
valent :
- 1 − [σ(z) = z] en z ;
- 1 − [τ(z) = z′] − [σ(z) = z′] en z′ ;
- 2 − [τ(z) = x] − [σ(z) = x] ailleurs.

Ce sont donc des chemins et des cycles. La couche L_a doit **décomposer deux fois CP(6)** (60 paires, 120 = 12 × 10) en
12 tels sous-graphes ; de même pour L_a′. S'ajoutent les contraintes d'intersection entre ℓ, ℓ′ (voisins lointains communs
imposés).

**Mesure.** Sur 5 structures C tirées au hasard, CP-SAT ne conclut pas en 180 s (`triangle_columns.py`).

## 5. Le jumeau sur BvLS
- **Les candidats alternatifs forment un graphe symétrique.** Chaque ligne change 8 de ses 16 voisins lointains, soit
  720 arêtes retirées et 720 ajoutées.
- **Le graphe obtenu est un srg(243,22,1,2) non isomorphe à BvLS.** Son groupe d'automorphismes est d'ordre 4 320 avec
  3 orbites, contre 3 849 120 pour BvLS. Il contient 405 grilles 3 × 3 induites, contre 1 485.
- **C'est, à notre connaissance, un nouveau graphe :** l'unicité de BvLS était indécidée (arXiv:1907.02800). Voir la
  note 159.

## 6. Ce que cela change pour la route
- **Route Ω canonique**, en trois étapes :
  1. structure de triangle C (~2·10¹¹) ;
  2. colonnes B_C (décomposition de 2·CP(6) par couche) ;
  3. étage F presque forcé (2 candidats par ligne sur BvLS), puis vérification.
- **Les leviers de réduction suivants**, par ordre d'intérêt :
  1. Un moteur dédié à la décomposition de 2·CP(6) en sous-graphes à degrés imposés. C'est de la couverture exacte
     structurée, beaucoup plus rigide que le modèle générique, et elle compte le nombre de colonnes valides par C.
  2. Ajouter aux colonnes la condition rang B_C ≤ 34 : Z doit avoir une dimension ≥ 26.
  3. Exploiter l'ambiguïté binaire de l'étage F. Si le jumeau n'est jamais un SRG, ou s'il l'est toujours par une symétrie,
     l'étage F devient un simple test.
  4. Quotienter les ~2·10¹¹ structures C par les contraintes λ/μ fines (les 11 types de τ ∪ mates de la passation, etc.).
