# Profile (4,8) at P = 0 of the laptop session's sweep (lab PC, night of 08 to 09/10/2026)

Question (laptop session): at rank 37 with P = 0, can a line have a disconnected near graph with components of 12 and
24 points? Its code is used unchanged: `conway99-c2-aws`, folder `c1_rank37_girth5_lines/` (`sweep48.py`,
`fastlib.py`, `multi.py`, `gen66.py`, `star66.py`, `fast.c`, `enumc.c`, `types_m2.txt`, `comp66_types.json`), read
before running. `types_m4_p0.txt` (81 959 component types) was regenerated here in 105 s: same printed counts and
same hash prefix (c77da4c17dec6479) as the laptop's. The first three balls reproduce its expected lines exactly.

Run: 12 000 parts, `python sweep48.py 1 <part> 12000`, driven by `guarded_pool.py`: 11 workers at below-normal
priority, a single one while Discord, FiveM, Valorant or a similar program runs, no new start when free memory is
under 20%, resumable from `pool_48.log`. Allowance given directly by the user (up to 80% of the processor and of the
memory). 12 workers gave an average load of 79% with peaks at 84%, hence 11.

Two phases:
* parts 0 to 1762 (in the order of the pool log), code at commit 6a334970a: all the 245 877 balls of those parts;
* from 01:30 UTC on 09/10, code at commit cb4ff9ec1 (`sweep48.py` with four more lines, `reps48.txt`): only one ball
  per isomorphism class (97 896 in all), see NOTE 17.78 for the reduction and its checks. `sweep48_before_reps.py` is
  the first version.

`aggregate_48.py` concatenates the per-part logs and gives the coverage of the representatives (dead, TORSION,
other, missing) and the total. The torsion balls are treated in `c1_lap_sweep48t_2026-10-09/` (rank 1 here, ranks 2
to 4 on the laptop). The interpretation of the result belongs to the laptop session; nothing is claimed here.
