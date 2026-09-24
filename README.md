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
5. `JOURNAL.md` — journal horodaté.

## État (2026-09-24)
- **Γ est nécessairement « tordu »** (L1) : sinon Γ serait un quotient de H(7,3) et 99 | 3⁷.
- **La torsion est localement possible** : graphes tordus explicites pour t = 2 (20 sommets, graphe des arcs de K₅)
  et t = 3 (39 sommets). Toute obstruction doit donc être globale (SRG), pas locale.
- Lemmes arithmétiques : rank₇(A − 3I) impair (L2) ; recollement 7-adique non scindé (L3) ; le recollement du
  70-espace (piste C) est le même en tout sommet et pair (L4).
- Tuées : rigidité locale, revêtement universel, entrelacement sur les configurations déterminées par τ,
  cohérence de Fano, complexe cubique plat, T/Δ (absorbée), Arf (absorbée).
- En cours : cas « point de Hamming » (x dans les 21 grilles) — modèle exact `code/hamming_point.py`.

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
