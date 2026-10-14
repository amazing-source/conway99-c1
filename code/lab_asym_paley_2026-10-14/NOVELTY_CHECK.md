# Novelty check of the 14/10 asymmetry report (14/10/2026, about 12:40 UTC)

Requested by the user (direct): "Regarde juste si ça a été déjà fait". Searched: my memory files; my notes
(work/spreadfree_243_2026-10-12/NOTE_SPREADFREE.md, NEW_GRAPHS_2026-10-13.md, the rest of work/ by grep); Codex's
asymmetry repository Desktop/Recherche_Conway/c1-asymmetry-audit (notes 100-178, AUDIT_CODEX_ASYMETRIE, NOTE_HOFFMAN_*,
JOURNAL_C1_NUIT_2026_10_14, data/codex_asymmetry_synthesis_20261014 including the external dossier
PALEY_ASYMETRIE_DOSSIER and the literature index of 14/10) with French and English key words (deux-graphe, two-graph,
Seidel, descendant, Godsil, commutation, switching, stabilisateur, orbite, rigide, complétion, appariement,
reconstruction, réflexion); web: A. E. Brouwer's Paulus page (https://aeb.win.tue.nl/graphs/Paulus.html).

| item of the report | status | where |
|---|---|---|
| srg(9,4,1,2) unique, Aut 72; 15 srg(25,12,5,6), two asymmetric, complements of each other | KNOWN | Paulus-Rozenfeld 1973; Cohn-Elkies-Kumar-Schurmann (complements); external dossier PALEY (note 171, 11/10); Codex literature index 14/10 |
| the asymmetric ones are the descendants of the regular two-graph with group 6 (multiplicity 6) | KNOWN (documented) | Brouwer's Paulus page: two-graphs A, B, C, D with groups 6, 72, 39, 15600; children of A: 1^6 2^6 3^3 4^3 5^3 6^3 7 8 (his numbering). Aut(descendant) = point stabiliser is classical theory. Mine adds only: Aut(A) = S3 explicitly, and srg(26,10,3,4) #10 lies in A's class |
| certificate of asymmetry by an invariant + refinement | DONE (other invariant) | dossier PALEY section 4: K4/K5 counts 5 -> 16 -> 22 -> 25, and the attachment profiles on the union of the K5 |
| Godsil-McKay moves at 25 | DONE, more completely | dossier PALEY section 5: every one-cell GM set of size 4 to 24 in the 15 graphs; Paley has 50, all of size 12, all back to Paley; components {2}, {1,3,6,11}, {4,...,15} (McKay numbering) |
| no GM switching in the family (1,2) | DONE at 243 | NOTE_SPREADFREE section 2 (12/10): same counting, every size, and WQH on two pairs. My k = 14 version is the same argument transposed |
| forced-symmetry principle (completions >= |Aut(piece)| for an asymmetric graph) | DONE | note 171 section 7, "extension lemma" (dossier HOFFMAN_UPDATE, 11/10), applied to alpha = 22 |
| trades keep the stabiliser; symmetry-directed breaking | DONE | note 165 section 4 bis (impose invariance by K = Stab(S), "levier de brisure progressive"); my partial_symmetric_trades.py (12/10) |
| twin = BvLS seen from a line, group 4320 | ESSENTIALLY KNOWN | note 165 section 4 bis table: S = a vertex of BH (a line of the spread), K of order 4320 -> BvLS, twin |
| every one-block completion keeps a translation | KNOWN (SAT, 13/10) | NOTE_SPREADFREE section 6e; mine adds the orbit-stabiliser reason (boundary group 3888 against 6 completions) |
| proposal (b): an asymmetric srg(243,22,1,2) by freeing regions | DONE, tools exhausted | memory asymmetric-srg-campaign 13/10: census of the common third (7 graphs), descent 63/54/45 kept vertices, random kept sets; "nothing found, nothing excluded, tools exhausted for smaller windows" |
| proposal (c): principle on the coclique frames | DONE in principle | note 171 section 7 (alpha = 22: completions come in at least |Aut(Y)| labelled copies) |
| first-order data at a vertex (matchings) versus the vertex stabiliser, on the eight 243 graphs | NOT FOUND (new computation) | closest: Codex's point-reflection probe of 14/10 (tests one canonical involution; notes the local group 645120) |
| proposal (a): do the matchings at one vertex determine the graph? | NOT FOUND | closest: line boundary (2 completions), Hoffman boundary (1), closed neighbourhood undecided in 200 s (12/10) |

Conclusion: the report of 14/10 midday is mostly a rediscovery. Genuinely new: the first-order comparison (section 6.3
of NOTE_ASYM_PALEY), the boundary-group reading of the 13/10 observation, and the open proposal (a).
Lesson recorded in memory: check note 171 and the external dossiers BEFORE any Paley / asymmetry computation.
