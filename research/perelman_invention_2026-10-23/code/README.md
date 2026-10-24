# Calculs du second travail

Python 3 avec `numpy`, `scipy` (exp7), `python-flint` (rangs exacts mod p) et `sympy` (contrôle du §3.9). Aucun solveur
SAT. Lancer chaque script depuis ce dossier : `python3 expN_….py`. Les sorties vont dans `../data/`. Les entrées sont
lues dans le dépôt, sans y écrire : `data/srg243/`, `data/t2_twisted.json`, `data/t3_twisted.json` et
`code/lab_spreadfree_243_2026-10-12/`.

Vocabulaire : dans le code, le graphe biparti B_xy s'appelle « graphe de transport » et sa parité `eps`. Dans les notes,
ce sont le **graphe d'appariement** et la parité **η**, pour éviter la confusion avec les cycles de transport de
l'équipe (notes 236–240).

| script | objet | sortie | durée | résultat |
|---|---|---|---|---|
| `srg_tools.py` | outils : lecture des arêtes, droites, quadrangles, bords, rangs mod p, parité d'appariement, grilles | — | — | — |
| `exp1_curvature_topology_243.py` | η et cycles d'appariement ; H₁(X; 𝔽_p), p ≤ 7, pour BvLS, le jumeau, Γ₃, Γ₄ | `exp1_….json` | 200 s | H₁(𝔽₃) = 6, 1, 1, 1 ; 0 sur 𝔽₂, 𝔽₅, 𝔽₇ |
| `exp2_spread_cocycle.py` | étalements réguliers, cocycles d'étalement, dimension engendrée mod 3 | `exp2_….json` | 1 s | 11 étalements et dimension 6 (BvLS) ; 1 et 1 (autres) |
| `exp3_growth_comparison.py` | sphères comparées à H(n,3), propriété (L) | `exp3_….json` | 3 s | 0 violation |
| `exp4_covers_243.py` | revêtements triples par le cocycle d'étalement | `exp4_….json` | 14 s | 729 sommets, dans 𝒦₂₂, 0 violation de (L) |
| `exp5_cover_invariants.py` | spectres et grilles des revêtements | `exp5_….json` | 12 s | cospectraux, non isomorphes. Le drapeau `distance_regular` est mal calculé : les listes d'intersection montrent que les revêtements ne sont **pas** distance-réguliers |
| `exp6_cover_homology.py` | H₁(𝔽₂, 𝔽₃) des revêtements (esquisse aléatoire + rang exact) | `exp6_….json` | ≈ 10 min | 5 (BvLS) ; 0 (autres) |
| `exp7_ollivier_check.py` | courbure d'Ollivier par programmation linéaire | `exp7_….json` | 5 s | κ₀ = 1/22 et LLY = 3/22 sur les arêtes ; 24/44 ou 23/44 sur les non-arêtes selon η |
| `exp8_simple_connectivity.py` | effondrement de la présentation de π₁ (preuve de simple connexité si tout s'effondre) | `exp8_….json` | 3 s | simplement connexes : H(3,3), H(4,3), t2, t3, revêtements de Γ₃ et Γ₄ |
| `exp9_universal_cover.py` | revêtement universel par énumération de classes (Todd–Coxeter sur le groupoïde) | `exp9_….json` | ≈ 5 min | \|π₁\| = 729 (BvLS), 3 (jumeau, Γ₃, Γ₄), 1 (H(n,3), t2, t3, revêtements des tordus) |
| `exp10_transport_graphs.py` | η, cycles d'appariement sur des membres de diamètre > 2, déplacement minimal | `exp10_….json` | voir log | déplacement 5 dans les quatre revêtements |
| `exp11_spreadfree_243.py` | les quatre srg(243) sans étalement Γ₅ à Γ₈ : vérification, H₁ (p ≤ 7), π₁, η | `exp11_….json` | 200 s | srg vérifiés, 0 étalement, H₁ = 0, **π₁ = 1** |

`exp9_universal_cover.py` prend des noms de cas en argument ; sans argument, il traite tous les cas sauf BvLS et son
revêtement (≈ 2 min chacun) : `python3 exp9_universal_cover.py BvLS BvLS_cover3`.

**Contrôle de reproductibilité (24/10).** Toute la chaîne a été relancée après l'ajout des gardes `__main__`. Les
sorties d'exp1 à exp5 sont identiques aux premières, au champ `seconds` près.
