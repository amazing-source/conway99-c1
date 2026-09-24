# 50 — Programme « frontière de torsion » : exclure les configurations locales presque non tordues

Idée directrice : Γ est forcément tordu (L1), mais **à quel point, en chaque sommet ?** On fixe (entièrement ou
partiellement) le système de transitions τ en un sommet x et on impose *toutes* les équations SRG dans le modèle
enraciné exact (99 sommets, inconnues = arêtes disjointes de X, et éventuellement les τ libres). Un UNSAT exclut
la configuration (ou la famille) **en tout sommet de tout srg(99,14,1,2)** — donc aussi en C1.

## Outils
- `hamming_point.py` / `hamming_phi.py` : τ = mate (deux encodages indépendants).
- `rooted_model.py --case …` : τ prescrit quelconque ; `--notight`, `--nosrg` (contrôle relâché).
- `rooted_family.py K` : torsions confinées aux classes de K (τ libre sur K, au moins une torsion).
- `rooted_family.py sources a,b,…` : τ_a libre (couplage quelconque) pour a dans S, mate ailleurs.
- `tau_filter.py` : classement rapide (propagation unitaire / budget) d'un τ donné.

## Résultats (2026-09-24)
| Configuration en x | Résultat | Temps | Contrôles |
|---|---|---|---|
| τ = mate (point de Hamming) | **UNSAT** (L8) | 46 s / 100 s / 2 114 s | 2 encodages, avec et sans cassage |
| τ = mate + σ_x ∈ Aut | **UNSAT** (L7) | 34 s / 201 s | 2 encodages ; noyau = fait C |
| g(x) = 19 (3 configurations) | **UNSAT par propagation** (L10) | 0,0 s | relâché SAT ; aussi sans serrage ; preuve humaine de g19A |
| torsions confinées à 3 classes | **UNSAT** (L11) | 1,2 s | relâché SAT |
| une seule étiquette tordue | **UNSAT par propagation** | 0,0 s | relâché SAT |
| torsions confinées à 4 classes | en cours | | |
| une classe entière tordue (S = {(0,0),(0,1)}) | en cours | | |
| τ aléatoire (0 grille) | non décidé (propagation ne réfute pas) | > 9 min | — |

## Lecture
- Les configurations **presque non tordues** tombent vite, souvent par propagation : la contrainte μ = 2 sur toutes les
  paires (excès nul) punit une torsion isolée. Les configurations **génériquement tordues** ne tombent pas.
- Conséquence structurelle : en chaque sommet, la torsion est « étalée » (au moins 4 classes, au moins 2 étiquettes
  tordues, au plus 18 grilles). La frontière exacte est l'objet du programme.
- Ce n'est **pas** une preuve de non-existence : le régime générique reste ouvert. Aucune identité globale reliant
  torsion et grilles/prismes n'a été trouvée qui transformerait « forte torsion partout » en contradiction.

## Validation à faire sur le PC du labo
1. **Contrôle positif t = 10** : le modèle enraciné « point de Hamming » pour srg(243,22,1,2) doit être SAT (BvLS a tous
   ses points de Hamming). Trop gros ici (~20 M clauses). C'est le test qui valide le code générique.
2. Certificats DRAT (CaDiCaL + drat-trim, images Docker de la branche C3) pour L7, L8, L10, L11.
3. Poursuivre : confined(K) pour |K| = 4, 5, 6 ; sources(S) pour |S| = 2, 3, … ; familles « g(x) ≥ G ».
