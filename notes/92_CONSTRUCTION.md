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

## 4. Le « plafond à 70 % » (question de l'utilisateur) : expérience témoin
Score de Thakkar–Severini : 4950 contraintes (99 degrés + 4851 paires : λ sur 693 arêtes, μ sur 4158 non-arêtes).
Leur record : 3501/4950 = 70,73 % (549/693 λ, 2853/4158 μ). Ils n'expliquent pas le plateau (« optimum local strict
pour nos mouvements 2-opt, pas une borne globale »), sans borne ni témoin. Le seul plafond démontré concerne les
circulants (68,0 % = 33 classes de distance sur 49). Le recuit de la branche involution (première session) calait à
une énergie de 1550–1650, mais c'est une somme d'écarts dans le modèle quotient, pas la même mesure.
**Témoin** (`code/sa_srg.py`, recuit simulé à degrés fixés, même score, 8 min chacun, graine 1, vérification exacte) :
| graphe | existe ? | score |
|---|---|---|
| srg(99,14,1,2) | ? | 59,3 % |
| Hoffman–Singleton srg(50,7,0,1) | oui | 82,9 % |
| Gewirtz srg(56,10,0,2) | oui | 64,1 % |
| BvLS srg(243,22,1,2) (même famille) | oui | 49,2 % |
| M22 srg(77,16,0,4) | oui | 41,7 % |
| Brouwer–Haemers srg(81,20,1,6) | oui | 35,1 % |
| Higman–Sims srg(100,22,0,6) | oui | 30,7 % |
**Lecture.** Aucun SRG existant de cette taille n'est retrouvé, et la plupart scorent *moins* que 99. Le pourcentage
reflète surtout la ligne de base fixée par les paramètres (probabilité qu'une paire aléatoire ait le bon nombre de
voisins communs : ~29 % pour 99, ~13 % pour Higman–Sims, ~37 % pour Hoffman–Singleton), pas l'existence. Le plateau
est un phénomène d'algorithme (paysage rugueux, bassin de la solution minuscule), pas une propriété de 99. Le
dépasser ne prouverait rien tant qu'on n'atteint pas 100 % ; ne jamais le dépasser ne prouverait rien non plus,
puisque les graphes existants de même taille ne sont pas atteints. Seule une borne démontrée (score maximal < 100 %)
serait une preuve, et elle équivaut à la non-existence.
