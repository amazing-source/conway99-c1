# Was the W(B7) symmetry cut on the rooted Conway model already done? (14/10/2026)

Question from the user: had we already applied the symmetry cut (`rooted_pq_sb.py`) to Conway, or is it new?
Method: searched both research trees (`Desktop/Recherche_Conway/*`, this workspace) for lex-leader, symmetry breaking,
W(B7), 645 120 and 2^7:S7, then opened every hit in code and notes.

## Already in the project (the technique, on other models)

| where | what | model |
|---|---|---|
| `c1-asymmetry-audit/code/sat_local_batch.py`, `fullblock_symmetry.py` (Codex, 27/09) | lex-leader under Stab_B6(mu, tau), soundness lemma written | local block system (i)-(v), not the whole graph |
| C3 calculation repo (`notes/162_annexes/B_C3_C7.md` l.137: `lean_encoding.py`, `stageq_sym`) | lex-leader symmetries, lemma proved | C3 case |
| `type222.py`, `twist_search.py`, `alpha_cnf.py` | one-off WLOG fixings (signs/classes; one twisted edge fixed by the hyperoctahedral group; vertex 0 of a coclique) | special rooted cases |
| `hamming_phi.py --breaksym` (also used by `hamming_point.py`) | only the sign flips of classes 2 and 3 | Hamming point case |
| C2 Route C (`work/FINAL_STATEMENT_C2_DRAFT_2026-10-07.md`) | pairs (y1, y2) up to Aut(U) x signs | lattice route, a different model |

## Explicitly recorded as NOT done on the full rooted model

- `c1-asymmetry-audit/notes/20_ATTAQUES_R.md` l.124 (24/09), Hamming point model: "Cadical UNKNOWN après 30 min. La
  symétrie W(B₇) (ordre 645 120) n'est pas cassée."
- `c2_experimental/NEGATIVE_RESULTS.md` N11 (23-24/09), stage S (exteriors = the 84 roots of D7, involution case):
  UNKNOWN after 7 h; BreakID found 0 generators (the cardinality encodings hide the syntactic symmetry); "Une attaque
  par le calcul exigerait de casser les symétries à la main (W(B₇), d'ordre 322 560 effectif) et de découper en cubes".
- `conway99-involution/notes/NOTE_involution_case.md` l.66: isomorph rejection under 2^7:S7 described as "a
  well-defined project (days of expert engineering)", not carried out.
- Cloud rooted model `code/fx/rooted/gen_rooted.py` (commit b6dacbc): no W(B7) lex-leader in it; the search was split
  into 11 type partitions instead, all UNKNOWN after 8 min (`types.log`).

## What is new in `rooted_pq_sb.py` (as far as this search finds)

- The model is the complete rooted srg(v,k,1,2) model, not a special local type. Since mu = 2, outer vertex = pair of
  inner points on different lines, so the outer labels (the a-variables) are fixed by unit clauses.
- A hand-written lex-leader on the e-variables for 49 elements of W(B7): 21 line transpositions, 7 single point swaps,
  21 products of the two; prefix of 600 variables. This is the hand-made cut that N11 said was needed.

Limits, stated plainly:
- partial cut: 49 group elements out of 645 120, not complete isomorph rejection;
- no cube split yet;
- no verdict on Conway (the SB run was stopped at 304 s on 14/10 because the PC was needed);
- gain not measured: srg(51,10,1,2) is UNSAT in 1331 s with the cut, but the run without the cut, for comparison,
  was never obtained.

Next step, when the user allows compute: unsat timing with and without the cut on (51,10,1,2), then (73,12,1,2), before
any Conway run or cube split.
