# 128 — Rigidité (4,4,4) : à P = 0, un sommet dont les 7 droites sont (4,4,4) a tous ses σ égaux à la réflexion des mates ; conséquences 7-adiques

*26/09, fin de nuit. C1, mathématiques pures. DÉRIVÉ = preuve écrite. Aucun calcul n'est nécessaire.*

## 0. Énoncés
| énoncé | statut |
|---|---|
| **Lemme R.** À P = 0, si les 7 droites par x sont (4,4,4), alors σ_C(v) = v̄ pour toute classe C et toute v ∉ C. Donc S(x) = 84 | DÉRIVÉ |
| **Corollaire 1.** À P = 0, deux sommets voisins n'ont jamais tous deux leurs 7 droites (4,4,4). L'ensemble V₄₄₄ de ces sommets est indépendant : \|V₄₄₄\| ≤ 22 (Hoffman) et ≤ 49 (S ≤ 4158) | DÉRIVÉ |
| **Corollaire 2.** À P = 0, « (4,4,4) partout » est impossible | DÉRIVÉ |
| **Corollaire 3 (sous NT).** À P = 0, k ≥ 22 | DÉRIVÉ, avec notes/126 |
| **Corollaire 4 (inconditionnel).** À P = 0 et k ≤ 20, au moins 26 droites portent une torsion 7 équilibrée | DÉRIVÉ |

## 1. Rappels
- À P = 0, une droite L_U = {x, u, ū} de profil (4,4,4) apparie les 6 autres classes en 3 parties {V, Π_U(V)}.
- Chaque composante de G(L_U) est formée des étiquettes d'une partie et des U-paires correspondantes.
- τ_u, τ_ū et σ_U préservent les parties.
- Équilibre (notes/114 §3) : chaque lointain de L_U voit exactement 2 points de chaque composante (|C|/6 = 12/6).

## 2. Preuve du lemme R
Soient c ∈ C et d ∈ D, avec C ≠ D, et W := Π_C(D).
1. τ_c préserve les parties de P_C et n'a pas de mate (P = 0). Donc τ_c(d) ∈ W.
2. y := {c, d} ∈ Γ₂(x) est un lointain de L_W : ses étiquettes ne sont pas dans W, puisque W ≠ C, D.
3. Le partenaire τ_c de y, {c, τ_c(d)}, est une W-paire. Il est dans la composante Comp_W(C) de G(L_W) qui contient
   l'étiquette c, et c est aussi voisin de y. Donc y a déjà 2 points dans Comp_W(C).
4. Le partenaire σ_C de y est {c̄, σ_{c→c̄}(d)}. σ_C préserve la partie {D, W} de P_C et n'a pas de point fixe.
   - Si σ_{c→c̄}(d) ∈ W, ce partenaire est une W-paire d'autre étiquette c̄ ∈ C, donc un 3ᵉ point de Comp_W(C). C'est
     contraire à l'équilibre.
   - Donc σ_{c→c̄}(d) ∈ D ∖ {d}, soit **σ_{c→c̄}(d) = d̄**.
5. C'est vrai pour tous c, d. Donc σ_C est la réflexion des mates pour toute classe C. Chaque paire E = {c, d} de Γ₂(x)
   vérifie alors E ~ {c̄, d̄} = σ_x(E), donc **S(x) = 84**. ∎

## 3. Corollaires
- **Corollaire 1.** Soient x ~ u, avec x et u dans V₄₄₄.
  - Par R en x, σ_U = mate. Lu dans le repère de x, un événement S en u sur L_U s'écrit σ_U(τ_u v) = v
    (notes/125 §3), c'est-à-dire τ_u(v) = v̄, exclu à P = 0. **Aucun événement S en u n'est porté par L_U.**
  - Par R en u, tous les σ de u sont des réflexions de mates, et toute E ∈ Γ₂(u) est un événement S. En particulier
    chaque étiquette v de x (d'étiquettes {x, {u,v}} vue de u) en est un. Contradiction.
  - V₄₄₄ est donc indépendant. Hoffman donne \|V₄₄₄\| ≤ 99·4/18 = 22. Par ailleurs 84·\|V₄₄₄\| ≤ S ≤ n₃ = 4158
    (L18).
- **Corollaire 2.** Immédiat.
- **Corollaire 3.** Sous NT, k = 20 exige c(L) ≥ 3 sur toute droite (notes/126 §3 quater). À P = 0, le seul profil
  à c ≥ 3 est (4,4,4). Donc k = 20 est exclu, et k ≤ 18 l'était déjà.
- **Corollaire 4.**
  - À P = 0 et k ≤ 20, toute droite vérifie r₀ ≥ 2 + r.
  - Une droite (6,6) force k ≥ 22 (notes/126 §3 bis). Une droite (4,8) doit donc avoir une torsion équilibrée sur sa
    composante à 8 étiquettes, et une droite connexe au moins deux vecteurs de torsion équilibrés.
  - Au moins 99 − 22 = 77 sommets sont hors de V₄₄₄. Chacun est sur une droite qui n'est pas (4,4,4). Il y a donc au
    moins ⌈77/3⌉ = 26 telles droites, qui portent toutes une torsion équilibrée.

## 4. Portée
- **À P = 0, le programme 7-adique se réduit à k ∈ {22, 24, 26, 28}, à la seule condition NT.** Sans NT : k ≤ 20
  impose au moins 26 droites à torsion équilibrée.
- La preuve utilise un seul outil : l'équilibre d'une autre droite (L_W), appliqué au partenaire τ d'une paire.
  - Pour les profils (6,6) et (4,8), l'équilibre laisse un point de marge (3 points par composante pour (6,6)). Le
    même argument ne force rien.
  - Pour P > 0, les composantes prismes cassent l'étape 1 (τ_c(d) = d̄ possible). Généralisation à étudier.
