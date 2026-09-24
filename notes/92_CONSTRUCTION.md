# 92 — Tentative de construction (« supposons que Γ existe ») (2026-09-24, nuit)

*Demande de l'utilisateur : changer d'angle, chercher le graphe (branche C1 : |Aut| = 1). Tout candidat sera vérifié
exactement (A² + A − 12I = 2J), puis son groupe d'automorphismes calculé.*

## 0. Ce que l'étude de non-existence dit du graphe, s'il existe
Tordu (L1) ; au plus 1151 prismes (L16), donc torsion moyenne ≥ 14,2 par sommet ; aucun sommet faiblement tordu
(frontière SAT, non certifiée) ; |Aut| ∈ {1, 2} (C3 exclu, ordres 7 et 11 exclus par Behbahani–Lam) ; en C1 aucune
symétrie. L'analogue q = 2 existant (Gewirtz) est tordu au maximum : l'hypothèse « P = 0 » est plausible.

## 1. Littérature (vérifiée après coup, à la demande de l'utilisateur — j'aurais dû le faire avant)
- SAT : Keramatipour, arXiv:2604.23037 (2026) — les solveurs SAT n'arrivent pas à traiter le problème en un temps
  raisonnable.
- Heuristiques : Thakkar–Severini, arXiv:2608.11211 (2026) — recherche locale, tabou, recuit simulé, évolutionnaire,
  CP-SAT : au mieux 70,73 % des contraintes.
- Méthodes de projection (Douglas–Rachford / RRR d'Elser) : utilisées pour des designs combinatoires (matrices de
  pesée circulantes, Hadamard) et la coloration ; aucune application trouvée aux SRG ni au 99-graphe.
- Epoch AI (FrontierMath, problèmes ouverts) : « the main risk with this problem is that no such graph exists ».

## 2. Méthode : RRR (Elser) entre deux ensembles faciles à projeter
- Générique (`code/rrr_srg.py`) : matrices 0/1 symétriques ∩ matrices de spectre {14, 3⁵⁴, (−4)⁴⁴}.
- Enracinée (`code/rrr_rooted.py`) : même chose avec la structure forcée en un sommet (N(x) = 7K₂, Γ₂(x) ↔ paires non
  mates, τ_a couplages parfaits exacts) ; variante « P = 0 » (τ_a sans paire de mates, 6040 couplages sur 10 395).
- Par droites (`code/rrr_lines.py`) : incidence points-droites N (99 × 231), 3 points par droite ∩ valeurs
  singulières {√21, √10⁵⁴, √3⁴⁴}.

## 3. Étalonnage sur des SRG connus (départs aléatoires)
| graphe | résultat |
|---|---|
| Petersen, Paley(9), Clebsch, Shrikhande | trouvés en < 1 s |
| srg(27,10,1,5) | trouvé (β = 0,1), échec avec β ≥ 0,2 |
| Hoffman–Singleton srg(50,7,0,1) | trouvé en < 2 s (β = 0,05–0,1) |
| **Gewirtz srg(56,10,0,2)** (analogue tordu, q = 2) | trouvé (β = 0,02, 50 000 itérations, 82 s) |
| **Brouwer–Haemers srg(81,20,1,6)** (λ = 1) | **non trouvé** en 10 min (générique, et par droites, 2 graines) |
Ordre de grandeur : même si Γ existe, la densité des solutions est ~10⁻¹³⁰⁴ contre ~10⁻⁸⁶⁰ pour srg(81,20,1,6).
Une méthode qui ne trouve pas srg(81,20,1,6) n'a pratiquement aucune chance sur 99 : on étalonne d'abord.
