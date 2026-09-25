# 104 — Tissu de 11 grilles (idée F10) : le plan projectif d'ordre 10 et l'exclusion du régime pur

*25/09, 12 h 30. Consigne de l'utilisateur : une approche nouvelle, par les structures (ensembles, couplages, stables…)
et non par les automorphismes. F10 était proposée (notes/10) et jamais attaquée (notes/20 : « non encore attaquée »).
Aucune hypothèse de symétrie n'est utilisée : tout vaut pour C1, C2 et C3. Recherche rapide (web, 25/09) : aucun lien
connu entre srg(99,14,1,2) et le plan d'ordre 10 ; à confirmer par une vraie recherche bibliographique.*

## 0. Résumé
| résultat | énoncé | statut |
|---|---|---|
| réduction | un tissu (V = S₁ ⊔ … ⊔ S₁₁, grilles induites) ⟺ 55 permutations M_ij vérifiant (E) | preuve |
| **Théorème A** | si tous les M_ij sont des anti-isomorphismes, on obtient un **plan projectif d'ordre 10** (avec polarité) : impossible (Lam 1989) | preuve (+ Lam) |
| **Théorème B** | si tous les M_ij sont des isomorphismes : contradiction, car 7 ∤ 220 | preuve |
| Lemme C | si chaque M_ij est iso ou anti (« régime pur »), les signes forment 1, 2 ou 11 classes | preuve |
| **Théorème D** | deux classes : mod 7 impose les tailles {2, 9}, puis une inégalité de traces d'holonomie les exclut | preuve + énumération exacte (72 automorphismes) |
| **L25** | **aucun tissu de 11 grilles à couplages purs** | preuve |
| régime général | bijections ni iso ni anti (p_ij ∉ {0, 18}) | ouvert ; spectralement invisible (§6) |
| portée | rien ne force l'existence d'un tissu, ni même d'une grille (profil g ≡ 0 de notes/100) | limite |

## 1. Réduction (preuve)
Grille = K₃□K₃ induit (L5 : tout point extérieur a exactement un voisin dedans). F15 (notes/10) notait déjà que ce
serrage est propre à 99 ; précisément, dans la famille λ = 1, μ = 2 (k = 2(t+1)), 9(k − 4) = v − 9 ⟺ k² − 18k + 56 = 0
⟺ k ∈ {4, 14}.

Supposons V = S₁ ⊔ … ⊔ S₁₁ avec chaque S_i une grille. Par L5, entre S_i et S_j (i ≠ j) les arêtes forment une
bijection, de matrice de permutation M_ij (9 × 9, M_ji = M_ijᵀ). On identifie chaque S_i à Z₃² par un isomorphisme de
graphes ; R = matrice du graphe de la tour 3 × 3 (la même pour tous les blocs). Alors A = I₁₁ ⊗ R + O, où O a pour
blocs les M_ij et des blocs diagonaux nuls. Les blocs diagonaux de A² + A − 12I = 2J sont automatiques (R² = 2I − R + 2J),
et les blocs hors diagonale donnent, pour tous i ≠ j :

  **(E)  Σ_{k ≠ i,j} M_ik M_kj = 2J − M_ij − R M_ij − M_ij R.**

(E) équivaut à « Γ est un srg(99,14,1,2) ». C'est l'analogue exact de l'équation (K) de notes/103 (point de Hamming),
avec des grilles au lieu des 4-cycles.

*Espaces.* Sur 1^⊥ ⊂ R⁹, R a deux espaces propres de dimension 4 : V⁺ (valeur 1, fonctions de la ligne ou de la colonne)
et V⁻ (valeur −2). M_ij est un **isomorphisme** si R M_ij = M_ij R (il envoie V⁺ → V⁺) et un **anti-isomorphisme** si
M_ijᵀ R M_ij = J − I − R (le graphe de la tour est auto-complémentaire ; alors V⁺ → V⁻ et V⁻ → V⁺). Sur 1^⊥, (E) s'écrit
par blocs (V⁺, V⁻) :

  **(E′)  Σ_k M_ik M_kj = diag(−3a_ij, 3d_ij)**, où a_ij, d_ij sont les blocs diagonaux de M_ij.

## 2. Théorème A : régime anti ⟹ plan projectif d'ordre 10
*Énoncé.* Si tous les M_ij sont des anti-isomorphismes, il existe un plan projectif d'ordre 10. Donc (Lam–Thiel–Swiercz
1989) ce régime est impossible.
*Preuve.* Anti ⟹ R M + M R = J − M, donc (E) devient Σ_k M_ik M_kj = J : pour x ∈ S_i et y ∈ S_j (i ≠ j), il existe
exactement un sommet w hors de S_i ∪ S_j voisin de x et de y. Soit B(w) = les 10 voisins de w hors de son bloc (un par
autre bloc). Alors :
- deux points de blocs différents sont dans exactement un B(w), et deux points d'un même bloc ne sont dans aucun ;
- pour w, w′ ∈ S_i, B(w) ∩ B(w′) = ∅ (L5), donc les 9 blocs B(w), w ∈ S_i, partitionnent V ∖ S_i.
On ajoute un point P et 11 points q₁, …, q₁₁. Les droites sont {q₁, …, q₁₁}, les S_i ∪ {P, q_i} et les B(w) ∪ {q_i} pour
w ∈ S_i. Cela fait 111 points et 111 droites de 11 points, et deux points quelconques sont sur exactement une droite
(vérification cas par cas : points de blocs différents, même bloc, P, q_i avec un point de S_i ou hors de S_i, q_i q_j).
C'est donc un 2-(111, 11, 1), c'est-à-dire un plan projectif d'ordre 10. ∎
*Remarques.*
- 99 = |PG(2,10)| − 11 − 1 : on retire une droite L et un point P hors de L.
- w ↦ B(w) ∪ {q_i}, P ↦ L, q_i ↦ S_i ∪ {P, q_i} est une **polarité**. Ses points absolus sont q₁, …, q₁₁, sur la droite
  L. C'est ce qu'exige Baer pour un ordre pair non carré : exactement n + 1 points absolus, alignés.
- Toute holonomie h = M_ij M_jk M_ki est de type anti, donc de traces nulles sur V⁺ et V⁻, et fix(h) = 1 : chaque
  triple de grilles porte exactement une droite transverse. Les 165 droites transverses sont les C(11,3) triples, et les
  9 points de S_i s'identifient aux 9 facteurs d'une 1-factorisation de K₁₀ (sur les 10 autres grilles).
- *Contrôle du mécanisme* (`code/weave_pg4_control.py`) : la construction inverse à l'ordre 4, soit PG(2,4) avec une
  polarité dont la droite absolue est retirée avec son pôle, et K₃ sur les 5 groupes, donne bien un srg(15,6,1,3) = GQ(2,2)
  (pour K₃, g = 2 sur les paires croisées non adjacentes, d'où μ = 3).

## 3. Théorème B : régime iso ⟹ 7 ∤ 220
*Outil (congruence des sous-espaces invariants).* Si U ⊥ 1 est invariant par A, ses valeurs propres sont 3 et −4, donc
**7·m₃(U) = tr(A|U) + 4 dim U**.
*Preuve de B.* Si tous les M_ij sont des isomorphismes, U⁺ = ⊕_i V_i⁺ (dimension 44) est invariant par I ⊗ R et par O.
tr(I ⊗ R | U⁺) = 44 et tr(O | U⁺) = 0 (O a des blocs diagonaux nuls). Il faudrait donc 7 m₃ = 44 + 176 = 220, qui n'est
pas divisible par 7. ∎ (U⁻ donne 7 m₃ = 88 : même conclusion.)

## 4. Lemme C : structure des signes en régime pur
*Énoncé.* Si chaque M_ij est un iso ou un anti (signe σ_ij = ±1), il y a exactement trois possibilités : tout est iso,
tout est anti, ou bien les 11 grilles se répartissent en **deux classes**, avec iso à l'intérieur de chaque classe et anti
entre les deux.
*Preuve.* Un composé M_ik M_kj est de type iso (diagonal par blocs) si σ_ik σ_kj = +, et de type anti (anti-diagonal par
blocs) sinon. Comme le second membre de (E′) est diagonal par blocs, la somme sur K⁻ = {k : σ_ik σ_kj = −} s'annule sur
1^⊥. Donc Σ_{K⁻} P_k = (|K⁻|/9) J, et 9 divise |K⁻| : |K⁻| ∈ {0, 9}. Si σ_ij = + et |K⁻| = 9, le second membre −3a_ij
(a_ij orthogonale) serait nul : absurde. Donc σ_ij = + ⟹ σ_ik = σ_jk pour tout k. « σ = + » est donc une relation
d'équivalence, et le signe vaut − entre deux classes. Pour une arête anti entre les classes C et C′, K⁺ = les autres
classes, d'où 11 − |C| − |C′| ∈ {0, 9}. ∎

## 5. Théorème D : le cas à deux classes
Soit C (n grilles) et C′ (11 − n grilles).
*(i) Mod 7.* U′ = ⊕_{C} V⁺ ⊕ ⊕_{C′} V⁻ est invariant. tr(A|U′) = 4n − 8(11 − n), d'où 7 m₃ = 12n + 88, ce qui force
**n ≡ 2 (mod 7)**, soit {n, 11 − n} = {2, 9}.
*(ii) Inégalité d'holonomie.* Pour un automorphisme g de la grille, on note α = tr(g|V⁺) et β = tr(g|V⁻). **Lemme :
β − α/2 ≤ 2** (énumération exacte des 72 automorphismes, `code/weave_grid_traces.py`). L'égalité est atteinte seulement
pour l'identité, les 4 translations (a,b), ab ≠ 0, et 6 échanges ; au total 11 éléments.
Pour une paire iso (j,k), les 9 holonomies h_j(jkl) = M_jl M_lk M_kj sont des automorphismes. D'après (E′) multipliée
par M_kj, Σ_l α = −12 et Σ_l β = +12, donc Σ_l (β − α/2) = 18 = 9 × 2 : **chaque holonomie réalise l'égalité**.
Prenons C = {1, 2} et C′ les 9 autres. Pour j, k ∈ C′, le triangle {1, j, k} a en base 1 des traces (u, v), et en base j
les traces (v, u) (conjugaison par un anti). L'égalité en base j donne u − v/2 = 2. En sommant sur les 36 paires de C′ :
U₁ − V₁/2 = 72, où U₁ = Σ u et V₁ = Σ v.
Or, pour la paire anti (1, j), (E′) donne Σ_k M_1k M_kj = J, donc les 9 holonomies en base 1 ont une somme nulle sur
1^⊥ : p(12j) + Σ_{k∈C′∖j} u(1jk) = 0, avec (p, q) les traces du triangle {1, 2, j}. La paire iso (1, 2) donne Σ_j p = −12
et Σ_j q = +12. En sommant sur j : U₁ = 6 et V₁ = −6, donc U₁ − V₁/2 = 9 ≠ 72. **Contradiction.** ∎
(Dans le régime tout iso, la même inégalité est juste saturée, 220 = 220, sans contradiction. Les deux arguments
sont donc complémentaires.)

**L25.** Il n'existe pas de srg(99,14,1,2) partitionné en 11 grilles dont chaque couplage inter-grilles est un
isomorphisme ou un anti-isomorphisme.

## 6. Régime général : ce qui reste
Pour une bijection quelconque, on note p_ij le nombre d'arêtes des 18 de S_i envoyées sur des arêtes (anti : 0, iso :
18, une bijection aléatoire : environ 9) et Π = Σ_{i<j} p_ij. Identités exactes (toutes automatiques) :
- quadrangles : 99 internes, Π à deux côtés internes opposés, 1980 − 2Π à un côté interne, et **Π entièrement croisés**.
- avec O = [[O₊₊, O₊₋], [O₋₊, O₋₋]] sur W = ⊕ 1^⊥ : tr O₊₊ = tr O₋₋ = 0 et ‖O₊₊‖² = ‖O₋₋‖² = 4Π/9.
- On pose Y = (DO + OD + O)/3 sur W. C'est un tiers de la matrice entière de torsion T̃ = [R M + M R + M − J] (coefficients
  −1, 0, 1 ; 8Π coefficients non nuls). Avec X = partie anti-diagonale de O, (E′) équivaut à : **Y commute avec X, et
  Y² + 3Y + X² = 10**. Sur chaque espace propre E_θ de Y, X² = 10 − θ² − 3θ ≥ 0 (θ ∈ [−5, 2]) et X échange V⁺ et V⁻.
  Les traces s'équilibrent pour tout θ : **la positivité et les traces ne tranchent pas le régime mixte**, comme en
  notes/103 (« la contradiction, si elle existe, est combinatoire »).
*Version locale sans tissu.* Si deux grilles disjointes S, S′ sont reliées par un anti-isomorphisme, l'application
w ↦ (voisin dans S, voisin dans S′) est une **bijection** des 81 autres sommets sur S × S′. En général, ses fibres ont
une taille e ∈ {0, 1, 2}, avec e = 2 − g sur les paires non adjacentes.

## 7. Portée et suite
- L25 exclut un coin de F10 (les couplages purs), pas F10 : il reste les bijections ni iso ni anti. Surtout, **rien ne
  force l'existence d'un tissu**, ni même d'une grille : le profil de notes/100 (torsion maximale, g ≡ 0) les évite.
- Ce qui est nouveau ici : c'est la première fois qu'une sous-structure de Γ se ramène à un objet dont la non-existence
  est connue (PG(2,10)). F19 cherchait un « mécanisme Lam » par un code et avait été tuée faute de code ; ici, il arrive
  par une polarité.
- Suite possible, en maths pures : (a) le régime mixte de F10 (classer les bijections par p_ij et les holonomies autour
  d'une paire, comme en notes/103 §3) ; (b) chercher d'autres configurations dont le serrage produit un 2-design ou un
  GDD de non-existence connue.

## Annexe : coclique de Hoffman (complète notes/94 §3.2)
Si α(Γ) = 22 (borne de Hoffman atteinte), les 77 sommets extérieurs forment un 2-(22,4,2) (déjà noté en notes/94), et
de plus **le sous-graphe induit sur ces 77 sommets a pour spectre 10¹, 3³³, (−1)²¹, (−4)²²**. Preuve : entrelacement
(32 valeurs 3 et 22 valeurs −4 forcées) ; BN = −N + 2J donne 21 vecteurs propres de valeur −1 ; la trace fixe la dernière
valeur à 3. Toute grille coupe une telle coclique en exactement 2 points (orthogonalité de E₃ et E₋₄). Aucun ensemble ne
coupe chaque droite une fois (ce serait une coclique de 33 > 22).
