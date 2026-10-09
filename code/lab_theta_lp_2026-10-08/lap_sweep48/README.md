# Profile (4,8) at P = 0 of the laptop session's sweep (lab PC, night of 08 to 09/10/2026)

Question (laptop session): at rank 37 with P = 0, can a line have a disconnected near graph with components of 12 and
24 points? Its code is used unchanged: `conway99-c2-aws`, commit 6a334970a, folder `c1_rank37_girth5_lines/`
(`sweep48.py`, `fastlib.py`, `multi.py`, `gen66.py`, `star66.py`, `fast.c`, `enumc.c`, `types_m2.txt`,
`comp66_types.json`); read before running. `types_m4_p0.txt` (81 959 component types) was regenerated here in 105 s:
same printed counts and same hash prefix (c77da4c17dec6479) as the laptop's. The first three balls reproduce its
expected lines exactly.

Run: 245 877 balls in 12 000 parts, `python sweep48.py 1 <part> 12000`, driven by `guarded_pool.py` (copy of the one
in `c1_theta_lp_2026-10-07/`): 11 workers at below-normal priority, a single one while Discord, FiveM, Valorant or a
similar program runs, no new start when free memory is under 20%, resumable from `pool_48.log`. Allowance given
directly by the user (up to 80% of the processor and of the memory). 12 workers gave an average load of 79% with
peaks at 84%, hence 11 (70 to 76%). About 20 parts per minute.

`aggregate_48.py` concatenates the per-part logs and counts the three kinds of lines (dead, TORSION, other). The
interpretation of the result belongs to the laptop session; nothing is claimed here.
