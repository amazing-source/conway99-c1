# The srg(243,22,1,2) family (as of 11/10/2026)

All four known graphs are 3-covers of the Brouwer–Haemers graph srg(81,20,1,6) along a regular spread
(see notes/165_SRG243_REVETEMENTS_ET_SYMETRIE.md).

| file | |Aut| | orbits | grids | flat BH-grids | twisted pairs | prisms | induced hexagons | regular spreads |
|---|---|---|---|---|---|---|---|---|
| ../bvls243.edges (BvLS) | 3849120 | 243 | 1485 | 405 | 0 | 8910 | 4980690 | 11 |
| ../twin243_switched.edges (twin, note 159) | 4320 | 3,60,180 | 405 | 45 | 19440 | 2430 | 5000130 | 1 |
| gamma4_aut3888.edges | 3888 | 81,162 | 837 | 189 | 9720 | 5670 | 4990410 | 1 |
| gamma3_aut864.edges | 864 | 27,108,108 | 621 | 117 | 14256 | 4158 | 4994946 | 1 |

- `.edges`: edge list (0-based), `.g6`: graph6, `.autgens`: automorphism-group generators (images of 0..242).
- Independent check: `python3 code/asym243/certify.py FILE` (pure Python: srg on all 29403 pairs, grids, twisting,
  colour refinement) and `code/asym243/family_table.py` (nauty + Schreier–Sims cross-check, spreads, canonical forms).
- Construction: `code/asym243/stabcover.py` (re-voltaging of BvLS along the h_0 spread, invariant under the
  stabiliser of a substructure of BH): Γ₄ from a non-adjacent pair, Γ₃ from a line plus a point.
