# 135 — Le secteur pair à q:7 : boule paire, recensement, régimes inversés (Witt non scindé)

*27/09, nuit. C1. Pendant pair de notes/129–133. DÉRIVÉ = preuve écrite ; les comptes sont des calculs exacts.*

## 0. Énoncés
| énoncé | statut |
|---|---|
| Boule paire d'une droite-bloc : 20 coordonnées, de rang 18 − t⁺ ; au bloc plein, 19 − m (m D-cycles) | DÉRIVÉ + contrôlé sur les 4 types |
| Le noyau trivial (dimension 2) de la boule paire est automatiquement équilibré | contrôlé sur les options |
| Régimes pairs : g⁺ = (18 − t⁺) + 2(t⁺ − r₀⁺) + ρ⁺, et **ρ⁺ ≥ 2 si la boule paire réduite est SCINDÉE** (n pair) | DÉRIVÉ |
| Recensement pair des 3 308 types (§2) | calcul exact |
| g⁺ ∈ {14, 16} : test par types lancé ; ILP locaux inconnus à 60 s sur le portable, donc au cloud | en cours |

## 1. Cadre
- On pose Q = A − 3I + 3J (notes/126). Le terme J ne vit que dans le secteur pair. rang₇ Q = 14 + k, et 14 + k = g⁻ + g⁺ en
  séparant les secteurs.
- **Base paire** : e_x, e_{b+} + e_{b−} (7 blocs), e_v + e_{σv} (42 orbites).
  - A y agit par M = [[0, 2·1ᵀ, 0], [1, I, C], [0, Cᵀ, Q_orb]], où C est l'incidence bloc–orbite et Q_orb la matrice d'orbites
    de C2.
  - Forme symétrique : D(M − 3I) + 3wwᵀ, avec D = diag(1, 2, …, 2) et w = (1, 2, …, 2).
- **Boule paire** d'une droite-bloc c (20 coordonnées : x, les 7 blocs, les 12 orbites de l'étoile de c).
  - Son bloc étoile vaut 2(P_τ + P_η − 3I) : un **+** là où le secteur impair a un −.
  - Elle est de rang 18 − t⁺ avec t⁺ = d(ℓ_c) − 1 − t_c, et a un noyau trivial de dimension 2.
  - Ce noyau trivial est orthogonal à toutes les colonnes d'options : c'est la torsion « d − 1 » de notes/126.
- **Colonne paire** d'une orbite lointaine f d'option (Φ(z), Φ(σz)) : x⁺ = (6 ; 12 + 2[b ∈ supp f] ; 12 + 2q_f(l)), avec
  q_f(l) = [l ∈ Φz] + [l ∈ Φσz]. **Elle ne dépend que de Q** (les ombres paires, visibles dans U), pas des signes.
- **Witt** : β⁺ est NON scindée (notes/129 §4). La classe de U′^⊥ vaut classe(β⁺) − classe(U⁺/rad). Donc :
  - n⁺ = 18 − t⁺ pair et U⁺/rad **scindée** : ρ⁺ ≥ 2 (c'est l'inverse du secteur impair) ;
  - n⁺ impair : ρ⁺ ≥ 1.
- **Lignes rigides paires.** Si ρ⁺ = 0 et toute la torsion est équilibrée, alors N⁺_FF = 2Q_FF + I + 5J ≡ X⁺ᵀP⁺⁻X⁺ (mod 7).
  - Diagonale : x_f⁺ᵀP⁺⁻x_f⁺ ≡ 6.
  - Hors diagonale : Q_fg ≡ 4(Z⁺_fg − 5) ∈ {0, 1, 2}. C'est une condition sur Q, donc exploitable dans U.

## 2. Recensement pair (types (τ, η) valides, à Aut(X_c, π) près)
- **Bloc plein** (valeurs attendues 19 − m retrouvées) :
  - 6-cycle : rang 18, t⁺ = 0, non scindé, donc g⁺ ≥ 18 ;
  - 2+4 et 3+3 : rang 17 (t⁺ = 1, différences de composantes équilibrées), n impair, donc ρ⁺ ≥ 1 et g⁺ ≥ 18 ;
  - 2+2+2 : rang 16, t⁺ = 2, non scindé, donc g⁺ ≥ 16.
- **Tous les types** : t⁺ va de 0 à 5.
  - t⁺ = 0 : 1 060 étoiles libres et 821 types à pivot, partagés à peu près moitié-moitié entre scindés et non scindés.
  - t⁺ = 1 : 405 + 506.
  - t⁺ ≥ 2 : 228 types.
- **Aucun type n'est exclu par le seul (τ, η) à tout g⁺.** À g⁺ ≥ 20, t⁺ = 0 passe toujours (ρ⁺ = 2). C'est la même situation
  que dans le secteur impair (notes/133).

## 3. Conséquences et suite
- **Paires (g⁻, g⁺, k).**
  - k = g⁻ + g⁺ − 14, avec L22 : k ≤ 28.
  - g⁺ ≥ 18 − t⁺_c en tout bloc. g⁺ ∈ {14, 16} exige donc t⁺ ≥ 4 (resp. 2) en **tous** les blocs, l'équilibre total et une
    boule non scindée si ρ⁺ = 0.
  - C'est l'exact analogue de g⁻ = 16 (notes/132) : `code/q7_gplus_test.py`. Sur le portable, les ILP locaux restent inconnus
    à 60 s (les filtres pairs sont plus faibles). Balayage à confier au cloud.
  - **Si g⁺ ∉ {14, 16}** : g⁺ ≥ 18, donc k ≥ g⁻ + 4 ≥ 22 sans hypothèse de droite générique, et **k = 22 ⟹ g⁻ = g⁺ = 18**.
    C'est le cas doublement rigide : en tout bloc générique scindé des deux côtés, Q_FF et T_FF sont fixés par les données
    locales, donc toute l'adjacence lointaine aussi.
- Un bloc plein 6-cycle (non scindé, t⁺ = 0) laisse g⁺ = 18 possible. 2+4 et 3+3 imposent ρ⁺ impair ≥ 1.
