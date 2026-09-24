# C1 — recherche d'une obstruction pour srg(99,14,1,2) sans hypothèse de symétrie

Branche C1 du problème du 99-graphe de Conway : |Aut(Γ)| = 1 (les branches C2 = involution et C3 = ordre 3 sont
traitées ailleurs). Objectif : une **preuve de non-existence** (par l'absurde) valable sans symétrie, ou à défaut
des conséquences obligatoires nouvelles et vérifiées.

**Rien ici ne résout le problème.** Aucun résultat extérieur non vérifié n'est utilisé comme axiome ; l'ancien repo
conway-99-research (travail amateur assisté par IA) n'est **pas** une source.

## Par où commencer
1. `notes/00_FONDATIONS.md` — faits redérivés des axiomes (structure enracinée, transitions τ, spectre de H, …).
2. `notes/10_IDEES_F.md` — les idées (chercheur F), avec leur statut.
3. `notes/20_ATTAQUES_R.md` — les attaques (chercheur R) et les verdicts, avec les calculs.
4. `notes/30_LEMMES.md` — ce qui survit, avec preuves.
5. `notes/40_POINT_DE_HAMMING.md`, `notes/50_FRONTIERE_TORSION.md` — exclusions locales exactes (SAT).
6. `notes/60_HODGE.md` — route Hodge / Σν³ : réfutation du confinement, identités par blocs, bibliographie.
6 ter. `notes/80_ETINCELLE_ARITHMETIQUE.md` — torsion = moment cubique des droites ; L17 (arithmétique locale) ; structure d'Eisenstein.
6 bis. `notes/70_KREIN_DROITES.md` — **L16 : P ≤ 1151 par une condition de Krein sur les droites (preuve à la main)**.
6 quinquies. `notes/91_HIERARCHIE_ORDRE8.md` — hiérarchie exacte d'ordre 8 (comptages + positivité euclidienne et de drapeaux) : tout bute sur L16.
6 quater. `notes/90_SECONDE_VARIABLE.md` — L18 : la seconde variable libre d'ordre 7 (Reimbayev) = nombre S de paires
   σ-adjacentes ; grilles avortées et opérateur de défaut Δ.
7. `rapport/RAPPORT_C1.md` — synthèse ; `JOURNAL.md` — journal horodaté ; `LAB_INSTRUCTIONS_C1.md` — PC du labo.

## État (2026-09-24, soir)
- **Γ est nécessairement « tordu »** (L1) : sinon Γ serait un quotient de H(7,3) et 99 | 3⁷.
- **La torsion est localement possible** (géométries tordues explicites, t = 2, 3, 5, 7) : toute obstruction doit
  utiliser μ = 2 partout.
- Lemmes arithmétiques L2–L4 (7-adiques). Exclusions locales exactes L7–L11, L14 (frontière : g(x) ≤ 17, une ou deux
  étiquettes tordues impossibles sauf |C| = 5 à finir, 24/128 motifs à trois étiquettes UNSAT).
- Identité L15 : P = 1386 − ⅙Σ|W| ; confirmée indépendamment (Reimbayev 2026).
- **L16 (mathématique pure)** : P ≤ 1151 prismes, donc torsion moyenne ≥ 14,2 par sommet ; seconde preuve que Γ est tordu.
- Route Hodge / Σν³ **close** : le confinement du spectre est faux pour tout SRG de la famille (BvLS), et borner
  Σν³ revient à majorer la torsion totale, ce qu'aucune méthode connue ne fait (notes/60).
- Calculs de volume : PC du labo (`LAB_INSTRUCTIONS_C1.md`) ; sur ce portable, un seul calcul lourd à la fois.

## Code (`code/`, Python 3.14, venv `.venv` : numpy, scipy, sympy, networkx, python-sat)
- `graphs.py` : témoins (srg 9, BvLS 243, Clebsch, Gewirtz, GQ(2,2), GQ(2,4)), tous vérifiés au chargement.
- `rooted.py` : structure enracinée, τ, 2-facteur étiqueté, holonomie de droite.
- `twist_search.py` : recherche SAT de graphes tordus (axiomes locaux) ; contrôle positif H(3,3).
- `star_interlace.py`, `line_config.py` : attaques par entrelacement.
- `complex_homology.py` : H₁ du complexe triangles + quadrangles.
- `glue7.py` : recollement 7-adique (lemme L4).
- `hamming_point.py` : cas spécial τ = mate en x.
- `cayley_frobenius.py` : recherche de graphes de Cayley tordus (négative pour t = 2, 3).

Calculs lourds : jamais sur ce portable sans `~/.claude/tools/run_capped.ps1` (plafond 4000 Mo).
