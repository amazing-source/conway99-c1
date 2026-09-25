# 108 — Défauts de grilles et comptage des fentes : L11 démontré, g(x) ≤ 17

*25/09, après-midi. Suite de notes/105 (L8). Idée : autour d'un point presque de Hamming, les grilles complètes
fournissent des quadrangles parfaits. Le comptage des étiquettes (« fentes ») force alors des couplages parfaits,
et un sommet tordu n'a plus de place pour ses voisins d'ombre. Aucun solveur ; une seule vérification exhaustive
(`code/slot_uniqueness_check.py`, 1 024 cas).*

## 0. Résumé
| résultat | énoncé | statut |
|---|---|---|
| **Lemme D1** | en tout sommet, les grilles incomplètes (ensemble 𝒩 de paires de classes) ne sont jamais deux à deux sécantes : si 𝒩 ≠ ∅, 𝒩 contient deux paires disjointes | preuve |
| **L11** | les torsions ne peuvent pas être confinées à 3 classes | **preuve** (cas particulier de D1 ; auparavant SAT seulement) |
| **Lemme D2** | la configuration « chemin » 𝒩 = {αy, αδ, δw} est impossible | preuve |
| **g(x) ≤ 17** | aucun sommet n'est dans 18 grilles complètes | **preuve** (D1 + D2 ; c'était la frontière de L10) |
| L10, cas g = 19 | redémontré uniformément par D1 | preuve |

## 1. Rappels et outils
En x : Q_P = {ab, ab̄, āb, āb̄} pour la paire de classes P = {α, β}. Une paire est **complète** si sa grille 3×3 l'est
(τ_a(b) = b̄ et τ_b(a) = ā pour ses 4 sommets). 𝒩 = paires incomplètes.
- (Q) *Quadrangle presque parfait* (C2, notes/107 §1). Pour P complète, Q_P est un 4-cycle induit dont les 4 apex sont
  les étiquettes a, ā, b, b̄. Tout sommet de Γ₂(x) hors de Q_P a donc **au plus un** voisin dans Q_P. (Deux voisins
  adjacents dans Q_P : il serait l'apex, une étiquette. Deux voisins opposés : il serait l'un des deux voisins communs,
  qui sont dans Q_P.)
- (S) *Voisins spéciaux.* Pour y = {a, b} :
  - les voisins contenant a, b, ā, b̄ sont exactement les partenaires τ ({a, τ_a(b)}, {b, τ_b(a)}) et les ombres
    ({ā, ρ_α(b)}, {b̄, ρ_β(a)}) ;
  - si P est complète, ce sont les deux siblings ;
  - L13 : ρ_γ permute sans point fixe l'ensemble Z_γ des étiquettes qui tordent γ, et fixe les autres.
- (F) *Fentes.* Pour toute classe m hors de P(y), chacune des deux étiquettes de m est dans exactement 2 voisins de y
  (μ = 2). Pour P complète, les 10 voisins non siblings de y sont dans les 10 paires R disjointes de P. Avec
  n_R(y) = |N(y) ∩ Q_R| : pour chaque classe m ∉ P, Σ_{R ∋ m} n_R(y) = 4, et n_R(y) ≤ 1 si R est complète.

**Lemme U (unicité des fentes).** Soit P complète, et I = 𝒩 ∩ {paires disjointes de P}, vu comme graphe sur les 5
classes hors de P. Si I ne contient pas deux arêtes disjointes, alors n_R(y) = 1 pour tout y ∈ Q_P et tout R
disjointe de P.
*Preuve.* On écrit n = 1 + d. Alors d a des sommes nulles en chaque sommet de K₅, et d ≤ 0 hors de I.
- I est une étoile de centre c : en tout m ≠ c, d_{cm} = −Σ_{m′≠c} d_{mm′} ≥ 0. La somme en c donne Σ_m d_{cm} = 0,
  donc tout est nul.
- I est dans un triangle {m₁, m₂, m₃} : les sommets m₄, m₅ n'ont que des arêtes ≤ 0 de somme nulle, donc nulles.
  Sur le triangle, d₁₂ + d₁₃ = d₁₂ + d₂₃ = d₁₃ + d₂₃ = 0, donc d = 0.
- Réciproquement, deux arêtes disjointes de I portent un 4-cycle alterné ±1. ∎

*Contrôle exhaustif (`code/slot_uniqueness_check.py`) :* sur les 1 024 parties I, l'unicité équivaut à « pas deux
arêtes disjointes », 0 exception.

**Conséquence (couplage parfait).** Si P est complète et vérifie U, et si R est disjointe de P, alors chaque sommet de
Q_P a un voisin dans Q_R. Par (Q), ces 4 voisins sont distincts. Donc **chaque sommet de Q_R a exactement un voisin
dans Q_P**.

## 2. Lemme D1 : les défauts ne sont pas deux à deux sécants
*Énoncé.* Si 𝒩 ≠ ∅, 𝒩 contient deux paires disjointes.
*Preuve.* Supposons 𝒩 non vide et deux à deux sécant (une étoile ou un triangle). Soit R = {α, β} ∈ 𝒩.
1. Les 10 paires P disjointes de R ne sont pas dans 𝒩 : elles sont complètes. Chacune vérifie U, car
   𝒩 ∩ {paires disjointes de P} est encore sécant.
2. Par la conséquence du §1, chaque w ∈ Q_R a exactement un voisin dans chacune de ces 10 paires : 10 voisins, sans
   étiquette de α ni de β. Avec ses deux partenaires τ, cela fait 12, soit tous ses voisins dans Γ₂(x).
3. L'ombre de w = {a, b} par α (l'unique voisin contenant ā) est donc un partenaire τ. Seul {b, τ_b(a)} peut contenir
   ā, d'où τ_b(a) = ā. De même τ_a(b) = b̄.
4. Ceci vaut pour les 4 sommets de Q_R, donc R est complète. Contradiction. ∎

**Corollaires.**
- **L11 est démontré** : des torsions confinées à 3 classes donnent 𝒩 ⊆ {αβ, αγ, βγ}, un triangle.
- Les étoiles (les deux étiquettes d'une classe α tordant un même ensemble C, et rien d'autre) sont impossibles. Pour
  |C| = 2, c'est le cas g = 19 de L10 (les trois configurations de τ), redémontré uniformément.
- Avec L8 : en tout sommet, 𝒩 contient deux paires disjointes.

## 3. Lemme D2 : la configuration « chemin »
*Cadre.* R0 et L13 (une étiquette tord 0 ou ≥ 2 classes ; une classe est tordue par 0 ou ≥ 2 étiquettes) donnent
𝒩 = réunion d'étoiles centrées sur les classes des étiquettes tordantes. Pour |𝒩| = 3, il ne reste que :
- l'étoile ou le triangle, exclus par D1 ;
- le **chemin** 𝒩 = {αy, αδ, δw}. Les deux étiquettes de α tordent {δ, y}, celles de δ tordent {α, w}, rien d'autre
  ne tord ; les trois autres classes sont p, q, r.

*Preuve de l'impossibilité.* Soit w′ = {a, u} ∈ Q_{αy}, avec a ∈ α et u ∈ y.
1. **Voisins spéciaux.**
   - a tord y, donc τ_a(u) = d ∈ δ.
   - u ne tord rien, donc τ_u(a) = ā, et l'ombre par α est le sibling {ā, u}.
   - Z_y = {a, ā}, donc ρ_y(a) = ā, et l'ombre par y est {ū, ā}.
   - Les voisins spéciaux sont donc {a, d}, {ā, u} et {ā, ū}. Parmi les classes hors de α et y, seule δ est utilisée,
     une fois.
2. **Couplages forcés.** Les paires δp, δq, δr, wp, wq, wr sont complètes et vérifient U : leurs défauts disjoints
   sont {αy} ou {αy, αδ}, sécants. Donc n_{δp} = … = n_{wr} = 1 pour w′.
3. **Fentes en δ** : n_{δw} + n_{δp} + n_{δq} + n_{δr} = 4 − 1, d'où **n_{δw} = 0**.
4. **Fentes en w** (aucun voisin spécial ne porte d'étiquette de w) : n_{δw} + n_{wp} + n_{wq} + n_{wr} = 4, d'où
   **n_{δw} = 1**. Contradiction. ∎

**Corollaire : g(x) ≤ 17 en tout sommet.** Les configurations à 3 grilles incomplètes sont l'étoile, le triangle et le
chemin (réunion d'étoiles d'au moins 2 paires). Toutes sont exclues.

## 4. Portée
1. Le côté faiblement tordu s'étend : L8, L10 (maintenant sans SAT), L11 et g ≤ 17 sont démontrés à la main.
   - L14 (deux étiquettes tordantes, 𝒩 = {αc, βc : c ∈ C}) contient des paires disjointes : D1 ne s'applique pas.
   - Le comptage des fentes est mécanique. Il faut, pour chaque paire incomplète et chaque sommet tordu, calculer les
     voisins spéciaux, les couplages forcés par U et les équations de fentes. C'est la même logique d'offre et de
     demande que les budgets de C2, avec les grilles complètes pour quadrangles parfaits.
2. **Ce que ce n'est pas.** Ce sont encore des planchers : le comptage a besoin de grilles complètes, et le profil de
   torsion maximale n'en a aucune (notes/100 §4).
