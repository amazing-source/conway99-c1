# 132 — g⁻ = 16 est impossible (Witt + équilibre + lignes rigides : un problème local fini)

*26/09, nuit. C1, branche involution (C2), pièce q:7 / g⁻ = 16 (l'un des trois énoncés ouverts de « structures »,
astra/PROBLEMES_OUVERTS_INVOLUTION.md). DÉRIVÉ = preuve écrite ; calcul exact, fini et léger (96 classes, 12 s).*

## 0. Énoncé
| énoncé | statut |
|---|---|
| **g⁻ ≠ 16. Donc g⁻ ∈ {18, 20}.** | DÉRIVÉ + calcul exact (96 classes), contrôlé indépendamment ; à relire |
| À g = 16, chaque bloc est dans l'un de quatre régimes locaux (§1) | DÉRIVÉ |
| Aucun type (τ, η) à t ≥ 2 n'admet de solution locale dans son régime (§2) | calcul exact + certificats rationnels |

## 1. Réduction : à g = 16, tout bloc est contraint localement
Notations de notes/129 et 131. Soient N = S − 3I (mod 7), I la boule d'un bloc c (7 blocs + 12 orbites de l'étoile) et F les
30 orbites lointaines. On a P := N_II, de rang 18 − t_c, et X := N_IF, déterminée par les données locales : B pour les lignes
blocs, les ombres s_f pour les lignes de l'étoile. Enfin N_FF = T_FF − 3I, qui n'est pas locale.

**Rang.** On décompose ker P = ⟨z_c⟩ ⊕ (torsion équilibrée, de dimension r₀) ⊕ (torsion non équilibrée, de dimension t − r₀).
- Les lignes Xᵀφ de la partie non équilibrée sont indépendantes.
- En éliminant la partie non dégénérée de P, on obtient **g = rang N = (18 − t) + 2(t − r₀) + ρ**, où ρ est le rang du résidu
  lointain comprimé.
- C'est la formule g = 18 + t − 2r₀ + ρ de notes/129 §5 bis.

**Witt** (Sol, 9415b71 via C2, relu par « structures » ; redémontré ici).
- U = N(F^I) ⊂ im N a pour Gram P sur la famille génératrice (Ne_i). Donc dim U = 18 − r₀, rad U est de dimension t − r₀, et
  U/rad est de dimension n = 18 − t, avec pour discriminant celui de la partie non dégénérée de P.
- β est hyperbolique sur im N (disc (−1)^{g/2}, notes/129 §2). Soit U′ = (U/rad) ⊥ H^{t−r₀} ⊃ U, un recouvrement
  hyperbolique du radical ; il est non dégénéré, de dimension n + 2(t − r₀).
- Alors im N = U′ ⊥ U′^⊥, et U′^⊥ a la classe de Witt opposée à celle de U/rad.
- Si cette classe est non nulle, le noyau anisotrope de U′^⊥ a dimension 2 (n pair, non scindé) ou 1 (n impair). D'où :
  - **g ≥ n + 2(t − r₀) + 2** si n est pair et U/rad non scindée (disc ≠ (−1)^{n/2} modulo les carrés) ;
  - **g ≥ n + 2(t − r₀) + 1** si n est impair.

**Régimes à g = 16** (t ≤ 4 partout, notes/129 §5 bis ; t ≤ 1 est exclu car 18 − t ≤ g) :
| t_c | contraintes | conséquence locale |
|---|---|---|
| 2 | r₀ = 2, ρ = 0, U/rad scindée (n = 16 : disc carré) | toute la torsion est équilibrée et R_c = 0 : **T_FF ≡ Z (mod 7)** |
| 3 | r₀ = 3, ρ = 1 | toute la torsion est équilibrée |
| 4 | (r₀, ρ) = (3, 0) avec U/rad scindée (n = 14 : disc non carré), ou (4, 2) | équilibre sur un hyperplan, ou total |

**Filtres unaires.** Pour une orbite lointaine f de représentant z, l'ombre est le couple (Φ(z), Φ(σz)) de paires non-μ.
- **Équilibre** : x_f ⊥ ker P, c'est-à-dire s̃_f·φ ≡ 0 pour φ ∈ ker Q_c (s̃_f = s_f + 2δ_f).
- **Rigidité** (t = 2) : T_ff = 0 (v ≁ σv) et R_c = 0 donnent **Z_ff = 3 + x_fᵀP⁻x_f = 13 + s̃_fᵀ(Q_c + 2J)⁻s̃_f ≡ 0**.
  - P⁻ est un inverse généralisé. Le résultat est bien défini puisque x_f ∈ im P, par l'équilibre.
- Ces conditions ne portent que sur l'ombre de f : ce sont des filtres **unaires** sur les options de chaque orbite, d'environ
  1/7³ chacun pour t = 2.

## 2. Calcul (exact, `code/q7_g16_test.py`, `q7_g16_ilp.py`, `q7_g16_certify.py`)
- **Classes.** Couples (τ, η) d'involutions sans point fixe sur X_c (τ = μ de C2, η = τ de C2), pris à Aut(X_c, π) près
  (ordre 46 080), avec K2, K3 ≥ 0 (comptes (ii), (iii) du lemme de l'étoile libre de C2) et t ≥ 2.
  - Il y en a **96** : 88 à t = 2, 5 à t = 3, 3 à t = 4.
- **Witt.**
  - 69 des 88 classes à t = 2 ont U/rad non scindée : exclues.
  - Les 3 classes à t = 4 sont non scindées (disc de la partie de dimension 14 carré) : le régime (3, 0) est exclu.
- **Filtres unaires** (équilibre de toute la torsion ; pour t = 2, en plus Z_ff ≡ 0). Chaque classe suivante a une orbite
  lointaine sans ombre admissible :
  - les 5 classes à t = 3 ;
  - les 3 classes à t = 4 (régime (4, 2)) ;
  - 11 classes à t = 2.
- **Les 8 dernières classes à t = 2.** Il reste de 1 à 32 options par orbite. Le modèle local est **infaisable dès la
  relaxation linéaire**, sans même utiliser les conditions de paires Z_ff′ ∈ {0, ±1} :
  - une ombre admissible par orbite ;
  - (i) chaque paire non-μ utilisée une fois ;
  - (ii) et (iii) du lemme de l'étoile libre de C2.

  Les 8 certificats de Farkas rationnels ont été produits par certify.py de « structures » et revérifiés exactement par
  check() (`data/g16_stage2_certificates.json`).
- **Contrôles.**
  - Réimplémentation indépendante des filtres unaires au niveau des 12 étiquettes (forme close par Q_c + 2J et
    ker(Q_c + 2J) ; `code/q7_g16_crosscheck.py`) : mêmes comptes, orbite par orbite, sur les 96 classes (0 écart).
  - Invariance par 20 réétiquetages aléatoires.
  - Énumération des classes recomptée directement pour 4 τ conjugués aléatoires : 0 écart.
  - K2 et K3 redérivés à la main (voisins communs de a et (c+, b) ; de (c+, b) et (c−, σd)).
- **Conclusion.** À g = 16, aucun bloc n'a de structure locale admissible. **g⁻ ≠ 16** ∎ (sous réserve de relecture).

## 3. Suite
- **g⁻ = 18 par la même méthode.** À g = 18 :
  - un bloc à t = 0 doit être scindé (det Q_c non carré : L23 dédoublé) et **toutes** ses lignes lointaines sont rigides
    (T_FF ≡ Z) ;
  - t = 1 impose r₀ = 1 et ρ = 1 ;
  - t = 2 impose (r₀, ρ) = (1, 0) avec U/rad scindée, ou (2, 2) ;
  - etc.
  - Il faut balayer toutes les classes, y compris t = 0, soit quelques milliers. C'est léger classe par classe mais long au
    total : à confier au cloud de C2 si cela dépasse 5 min.
- **À g = 20** (bloc plein, ou ÉTL à det carré), le même mécanisme donne les lignes rigides (Z_ff ≡ 0 ⟹ k_f = 0) et le test
  lointain T_FF ≡ Z + K r Kᵀ.
  - Recherche de K presque sans branchement : 8 choix par orbite et un élagage de 3/7 par paire (`code/q7_far_test.py`).
  - Il ne s'évalue que sur une solution locale complète. L'ILP local (i)+(ii)+(iii) d'une ÉTL générique reste indécis
    en 245 s, à reprendre sur le PC du labo.
