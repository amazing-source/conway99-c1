# 90 — La seconde variable libre de Reimbayev est une statistique de torsion (2026-09-24, nuit)

*Tout ici est mathématique ; les contrôles sont des comptages instantanés (`code/z11_identity.py`).*

## 0. Pourquoi
Reimbayev (arXiv:2608.19410) exprime les 208 fréquences de sous-graphes induits d'ordre 7 d'un srg(n,k,1,2) en
fonction de deux variables libres, n₃ (= ½Σ|W|, notre torsion, notes/60) et z₁₁ (fréquence du graphe Z₁₁ de sa
figure 1). À (99,14), la non-négativité des 208 fréquences donne seulement le triangle 2n₃ ≤ z₁₁ ≤ 4n₃,
n₃ ≤ 4158 (`code/reimbayev7.py`). Si z₁₁ était une quantité géométrique connue, une inégalité de positivité sur
elle pourrait couper ce triangle. D'où la question : que compte z₁₁ ?

## 1. Définitions
- **Réflexion ponctuelle** σ_x : fixe x, échange les mates dans N(x), et envoie E ∈ Γ₂(x) d'étiquette {b, c} sur le
  sommet d'étiquette {b̄, c̄}. C'est l'involution de Bondarenko–Radchenko ; dans un graphe non tordu (H(n,3) replié,
  BvLS) c'est un automorphisme. Dans C1, **aucun σ_x n'est un automorphisme**.
- **S** = #{(x, E) : E ∈ Γ₂(x), E ~ σ_x(E)} (paires « σ-adjacentes »).
- **Coïncidence τ** en un sommet E : paire non mate {a, c} ⊂ N(E) avec τ_a(c) = τ_c(a). On note S' = Σ_E (nombre de
  coïncidences en E). Dans un graphe non tordu τ_a(c) = c̄ ≠ ā = τ_c(a) : aucune coïncidence.

## 2. Lemme L18 (nouveau) : dictionnaire des sous-graphes Z₂, Z₃, Z₁₁
Dans toute géométrie vérifiant les axiomes locaux (λ = 1, μ = 2 à distance 2) :
  **S = S'**,   **z₂ = S/2**,   **z₃ = Σ_x|W(x)| − 2S**,   **z₁₁ = 2Σ_x|W(x)| − 2S**.
Dans un srg(n,k,1,2), avec n₃ = ½Σ|W| : **z₁₁ = 4n₃ − 2S**, et le triangle de Reimbayev 2n₃ ≤ z₁₁ ≤ 4n₃ est
exactement **0 ≤ S ≤ n₃**. Les données d'ordre 7 d'un srg(n,k,1,2) se réduisent donc à deux statistiques de
torsion : la torsion n₃ et le nombre S de paires σ-adjacentes.

*Preuve.*
- Z₂ : sommet central C de degré 4, ses deux droites {C, TL, TR}, {C, BL, BR}, et deux sommets L ~ {TL, BL},
  R ~ {TR, BR}, L ~ R. Donc L ∈ Γ₂(C), R = σ_C(L), L ~ R. Réciproquement toute paire σ-adjacente donne un Z₂
  induit (les non-arêtes sont forcées par λ = 1). Le sommet de degré 4 est unique : z₂ = S/2.
- S = S' : écrivons x = {a, c} vu de E. σ_x(E) est le second voisin commun (≠ x) de a' = {a, τ_a(c)} et
  c' = {c, τ_c(a)}. Si τ_a(c) = τ_c(a) = d, ce voisin est d ∈ N(E) ; sinon a' et c' n'ont pas d'étiquette commune
  et leur second voisin commun est dans Γ₂(E). Donc E ~ σ_x(E) ⟺ coïncidence en E pour la paire {a, c}.
- Z₁₁ : sommet A de degré 4 avec deux droites {A, T, B}, {A, C, D}, E ~ B, C, F ~ D, E. Enraciné en A : E ∈ Γ₂(A)
  d'étiquette {B, C} ; F est forcément le second voisin commun w de E et C̄ = D. Son étiquette est {C̄, y}, avec
  trois cas exclusifs : y = B (ssi τ_B(C) = C̄, classe non tordue), y = B̄ (ssi w = σ_A(E) ~ E), y autre (Z₁₁
  induit). Sur les 2·Σ_x|Γ₂(x)| triplets (x, E, ordre), le premier cas en prend 2(Σ_x 2t(t+1) − Σ|W|) et le
  deuxième 2S, d'où z₁₁ = 2Σ|W| − 2S (le sommet de degré 4 et l'ordre sont déterminés par la copie).
- Z₃ : une droite ℓ, un point « mid » de ℓ, rm ∈ N(mid) \ ℓ non fixe par l'holonomie de ℓ ; top, bottom = ses
  voisins dans les deux autres groupes ; fr = second voisin commun de top et bottom. Il y a Σ_ℓ 3t(ℓ) = Σ|W|
  candidats ; le candidat est dégénéré (fr voisin d'un point de ℓ) exactement quand fr est le mate de top ou de
  bottom, ce qui est une paire σ-adjacente enracinée en ce point de ℓ ; chaque paire σ-adjacente tue exactement
  deux candidats. ∎

*Contrôle* (`code/z11_identity.py`, comptage direct des copies induites par isomorphisme de sous-graphes) :

| géométrie | Σ\|W\| | S = S' | z₂ | z₃ | z₁₁ |
|---|---|---|---|---|---|
| tordue t = 2 (20 sommets) | 240 | 120 | 60 | 0 | 240 |
| tordue t = 3 (39) | 702 | 0 | 0 | 702 | 1404 |
| tordue t = 3 (42) | 1008 | 336 | 168 | 336 | 1344 |
| srg(9,4,1,2) | 0 | 0 | 0 | 0 | 0 |

Les trois valeurs prédites coïncident partout. Les deux bords du triangle sont atteints : z₃ = 0 (S maximal) pour
t = 2, S = 0 pour la géométrie à 39 sommets.

## 3. La matrice globale des réflexions Z
Z_{E,w} = #{x : σ_x(E) = w}. Z est symétrique, de somme par ligne |Γ₂| = 84, et **Z = J − I − A dans un graphe non
tordu** (vérifié sur BvLS et srg(9)). tr(ZA) = S ; toutes les traces de Z contre l'algèbre de Bose–Mesner ne
dépendent que de S (tr(Z E₋₄) = 132 − S/7) : Z n'apporte rien de plus au niveau spectral moyen.
*Observation* : sur les géométries tordues, Z met une masse importante sur les paires à **distance 3** (entrées 6
pour t = 2, 8 pour la géométrie à 42 sommets) : σ_x(E) « veut » tomber à distance 3. Dans un SRG, ces images sont
forcées à distance ≤ 2. Piste non aboutie : je n'ai pas trouvé de relation qui rende ce repliement contradictoire.

## 4. Grilles avortées et opérateur de défaut Δ
Pour x et une paire de classes {L_b, L_c} en x, soit G = {x} ∪ L_b ∪ L_c ∪ {bc, b̄c̄, bc̄, b̄c} (9 points ; une vraie
grille 3×3 si tout se ferme). Avec e = nombre d'arêtes dans G :
- e = 14 + m + s + s', m = nombre d'arêtes étiquetées du quadruplet (paires (étiquette, classe) non tordues),
  s, s' = σ-adjacences des deux paires opposées. Donc 18 − e = 4 − m − s − s' ≥ 0.
- Dans E₋₄ (échelle 63E), δ = Σ_{v∈G} p_v vérifie **|δ|² = 18(18 − e)** : une vraie grille est orthogonale à E₋₄
  (c'est L5), une grille avortée ne l'est pas, et son défaut est exactement le nombre d'arêtes manquantes.
- **Σ_{x, paires de classes} (18 − e) = Σ|W| − S/2 = 2n₃ − S/2** (vérifié sur les 5 géométries, y compris BvLS).
- Opérateur de co-occurrence N_G = Σ 1_G 1_Gᵀ = 180I + 45A + 9J + Δ. Ici Δ est une matrice entière symétrique à
  lignes de somme nulle, **Δ = 0 ssi Γ est non tordu**, Δ = (transitions τ sur les non-arêtes) + (Z − (J − I − A))
  − (torsion des droites sur les arêtes). Sur E₋₄, N_G se réduit à Δ, donc **Δ est semi-définie positive sur E₋₄**,
  tr(E₋₄Δ) = (4n₃ − S)/7 et tr(AΔ) = S − 4n₃. (Recoupé par deux calculs indépendants.)

## 5. Bilan honnête
- Nouveau et vérifié : la seconde variable libre de l'ordre 7 est la statistique de torsion S (L18) ; toute la
  torsion se lit dans l'opérateur de défaut Δ des grilles avortées, positif sur E₋₄.
- Pas de contradiction : les contraintes connues sur (n₃, S) sont 705 ≤ n₃ ≤ 4158 (L16) et 0 ≤ S ≤ n₃ (ordre 7),
  compatibles. Une contradiction demanderait une relation de plus entre n₃ et S, ou une contrainte sur Δ au-delà de
  sa positivité sur E₋₄. Toutes les identités spectrales moyennes essayées (sur Z, Δ, et les réflexions locales
  tr(P₋₄Σ_x) = −s(x)/7) se réduisent à (n₃, S) et ne contraignent rien.

## 6. Borne de Delsarte locale sur le schéma des étiquettes : triviale (résultat négatif)
Le groupe hyperoctaédral B₇ agit sur les 84 paires non mates avec 6 orbitales : R₀, R_a (une étiquette commune, les
deux autres mates ; valence 2), R_σ (1), R_sh (une étiquette commune, autres classes différentes ; 20), R_cl
(étiquettes disjointes, une classe commune ; 20), R_dj (40). Nombre d'arêtes de H par relation (comptage des
« créneaux » : chaque u = {a,b} a exactement un voisin contenant ā) :
  R_a : 84 − W,  R_sh : W,  R_σ : s/2,  R_cl : W − s,  R_dj : 420 − W + s/2    (W = |W(x)|, s = s(x)).
En particulier **s(x) ≤ |W(x)|** (R_cl ≥ 0). Le module de permutation est sans multiplicité : K^⊥ = 1 + 6 + 7 et
K = V₁₄ ⊕ V₂₁ ⊕ V₃₅. Traces exactes (`code/label_scheme.py`) :
  tr(H E₁₄) = 42 − W/2 + s/4,  tr(H E₂₁) = −42 + W/2 + s/4,  tr(H E₃₅) = −s/2
(les trois composantes de K^⊥ redonnent exactement 12, −12, 0 : contrôle). Avec tr(H E_i) = 3d_i − 7c_i,
c_i = tr(E_i P₋₄) ∈ [0, min(d_i, 30)] : c₁₄ = (2W − s)/28, c₂₁ = (420 − 2W − s)/28, c₃₅ = 15 + s/14. Toutes les
contraintes sont automatiquement satisfaites. **Au premier ordre, le spectre local ne plafonne pas la torsion.**
(Non tordu : V₁₄ ⊂ K₃ exactement ; la torsion fait tourner V₁₄ vers K₋₄.)

## 7. Un objet arithmétique propre à C1 : la similitude de torsion U_x (piste, pas de contradiction)
U_x = (2H + I)Σ_x, où Σ_x est la matrice de permutation de σ_x sur Γ₂(x). C'est une matrice entière (entrées 0, 1, 2),
qui préserve le réseau K, et **sur K on a U_xᵀU_x = 49** (car (2H+1)² = 49 sur K) : U_x/7 est orthogonale. Faits
(dérivés) : sur la totalité de R⁸⁴, UᵀU = 49I + 8J − 4BBᵀ ; tr(U|_K) = 2s(x) ; tr(U²|_K) = 8e_σ − 602 (e_σ = arêtes
de H préservées par σ_x) ; det(U|_K) = −7⁷⁰. Si σ_x commute avec H, U = ±7. Sinon, U a des valeurs propres 7e^{±iφ}
qui sont des **entiers algébriques de norme 49**, racines de facteurs t² − mt + 49 (par exemple 3 − 5ω ∈ Z[ω], de
norme 49). C'est l'analogue, créé par la torsion et non par une symétrie, de la structure d'Eisenstein de C3.
Pas de contradiction trouvée : les contraintes d'intégralité connues (L4 : rang de (2H+1) mod 7 sur K égal au
recollement k) sont compatibles avec des angles arbitraires.
