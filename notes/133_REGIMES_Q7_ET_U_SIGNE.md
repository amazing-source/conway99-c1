# 133 — q:7 par régimes (g⁻ ∈ {18, 20}), recensement des types de blocs, U signé

*27/09, nuit. C1. Fait suite à notes/132 (g⁻ ≠ 16). DÉRIVÉ = preuve écrite ; les comptes sont des calculs exacts.*

## 0. Énoncés
| énoncé | statut |
|---|---|
| g⁻ ∈ {18, 20} (notes/132 ; relu par « structures », certificats refaits par C2, 8c91af9) | DÉRIVÉ + certifié |
| Régimes locaux par bloc à g = 18 et à g = 20 (table §1) | DÉRIVÉ |
| Recensement : 3 308 types (τ, η) valides à Aut(X_c, π) près (table §2) | calcul exact |
| g = 18, t ∈ {3, 4} : 7 classes sur 8 mortes dans leur régime, 1 inconnue | calcul (ILP), partiel |
| Couche signée du modèle U de C2 (§4) : construite et testée ; pilote 3K2_or14 chez C2 | code |

## 1. Régimes : g = (18 − t) + 2(t − r₀) + ρ, plus Witt
Un bloc c de torsion t, d'équilibre r₀ et de résidu lointain ρ ; U/rad de dimension n = 18 − t. Witt (Sol, relu) :
- ρ ≥ 2 si n est pair et U/rad non scindée (disc ≠ (−1)^{n/2}) ;
- ρ ≥ 1 si n est impair.

| t | g = 18 | g = 20 |
|---|---|---|
| 0 | scindé (det Q_c non carré), ρ = 0 : **T_FF ≡ Z, toutes les lignes lointaines rigides** | ρ = 2 : T_FF ≡ Z + K r Kᵀ ; r anisotrope si det carré (lignes rigides en Z_ff ≡ 0), hyperbolique sinon |
| 1 | r₀ = 1, ρ = 1 : équilibre total, T_FF ≡ Z + λ k kᵀ, donc Z_ff ∈ −λ·{0, carrés} | (r₀, ρ) = (0, 1) ou (1, 3) |
| 2 | (2, 2) : équilibre total ; ou (1, 0) si scindé : équilibre sur une droite | (0, 0) si scindé ; sinon r₀ ≥ 1 : (1, 2), (2, 4) |
| 3 | (2, 1) : équilibre sur un plan ; (3, 3) exclu (équilibre total impossible, notes/132) | r₀ ≥ 1 : (1, 1), (2, 3) ((3, 5) exclu) |
| 4 | (3, 2) : hyperplan ; (2, 0) exclu (les 3 classes sont non scindées) ; (4, 4) exclu | r₀ ≥ 2 : (2, 2), (3, 4) ((4, 6) exclu) |

- Un bloc plein (τ = η) est à t = 0 et det ≡ 1 (carré), donc force g = 20. **À g = 18 il n'y a aucun bloc plein**, donc aucun
  résidu AD à bloc A (« structures »).
- De même, une ÉTL à t = 0 et det carré force g = 20.

## 2. Recensement des types de blocs (`code/q7_g16_test.py`, classes_t_ge(0))
Types (τ, η) = (μ, τ) de C2, avec K2, K3 ≥ 0, pris à Aut(X_c, π) près (ordre 46 080) : **3 308 classes**.
| | t = 0 non scindé (det carré) | t = 0 scindé | t = 1 | t = 2 non scindé / scindé | t = 3 | t = 4 |
|---|---|---|---|---|---|---|
| étoile libre (τ ∩ η = ∅) | 835 | 571 | 310 | 56 / 9 | 3 | 3 |
| avec pivot | 613 | 595 | 288 | 13 / 10 | 2 | 0 |
- Parmi les étoiles libres, 835 sur 1 787 (47 %) sont à t = 0 et det carré : g = 20, K anisotrope, lignes rigides.

## 3. g = 18 : état des calculs
- **t = 0 scindé** (1 166 classes) : il faut T_FF ≡ Z sur les 30 orbites lointaines.
  - Filtre unaire : Z_ff ≡ 0.
  - Puis modèle local (i)–(iii), puis conditions de paires Z_ff′ ∈ {0, ±1}, avec 10 − |supp s_f| entrées non nulles par
    ligne.
  - Balayage en cours sur le PC du labo de C2 (`code/q7_g18_sweep.py`) : environ 1/3 tuées par le modèle local, le reste
    inconnu à 60 s.
  - La propagation par consistance d'arc n'élague RIEN : ~200 options par orbite, chacune supportée dans chaque autre orbite.
  - CP-SAT avec clauses de support : inconnu à 200 s.
  - C'est une vraie recherche globale, pas un filtre local.
- **t = 3, 4** (`code/q7_g18_regimes.py`) : 7 classes sur 8 mortes. Une classe à t = 3 garde 6 plans inconnus à 30 s.
- **t = 1** (598 classes) et **t = 2** (88) : à faire, au cloud.

## 4. U signé : la couche impaire sur le modèle d'orbite U de C2 (`code/signedU/`)
- **Dictionnaire.** Q_ZW = A(u,w) + A(u,σw) et T_ZW = A(u,w) − A(u,σw).
  - Donc supp T_{Z,·} = {Q = 1} ; T = 0 sur le partenaire D (Q = 2) et là où Q = 0.
  - S² + S = 12I donne BT = 0 et T² + T = 12I − BᵀB.
- **Colonnes.**
  - Une colonne signée est v = (q, t) ∈ Z⁸⁴, avec t = ±1 sur supp{q = 1}.
  - Filtre par colonne : BT = 0, bloc par bloc ; c'est la seule ligne de Z qui intervient.
  - Jauge : u_Z = (a,+)(b, ε_Z) avec a < b.
- **Nouvelles lignes du maître.**
  - CT(a, b) : symétrie de T.
  - IT(a, b) : T² + T = 12I − BᵀB, linéarisée par les produits extérieurs constants t(a)t(b), comme les lignes I de C2.
  - Le prix reste une forme quadratique bloc-diagonale, donc solve() et verify() de C2 sont inchangés.
- **Parités.** Il faut savoir lequel des deux orbites U d'une paire est (a,+)(b,+).
  - Ce choix est WLOG seulement si U est invariant par l'échange des deux orbites de chaque paire.
  - Or le forbid_for de C2 (D fixé, appariement « dans l'ordre ») consomme déjà cette symétrie. On impose donc D au niveau
    des paires (forbid_pairlevel).
  - Les paires tw et mix sont asymétriques : il faut brancher sur leurs parités.
- **Pilote 3K2_or14** (U faisable, tué par q:7) : 214 656 colonnes U avec D au niveau des paires, 930 624 colonnes signées,
  3 156 lignes. Test d'unité entries/score : 0 écart sur 300. Résolution chez C2.
- **Limite honnête.** Le PL signé contient BT = 0, la symétrie de T et T² + T exactement, mais **pas la structure de rang
  mod 7**, qui est ce qui a tué 3K₂.
  - Un « faisable » ne contredirait donc pas q:7.
  - Un « mort » serait une obstruction nouvelle, purement réelle (entière).
