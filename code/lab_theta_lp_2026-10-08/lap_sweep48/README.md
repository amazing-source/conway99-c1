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

## Result of the main sweep (ended 04:49:07 UTC on 09/10/2026)

12 000 parts of 12 000 finished, none with an error code, no presence check positive. `aggregate_48.py`:

    balls logged 117860 of 245877: dead 98163, torsion 19697, other 0
    representatives (one ball per isomorphism class) logged 97896 of 97896: dead 81380, torsion 16516, other 0; missing 0

"dead" = both residue classes c0 = 1, 3 searched at near point 0, no star; "torsion" = the large component has
7-torsion, not searched by this driver. So: every torsion-free representative ball is dead; the 16 516 torsion
representatives (rank 1: 15 462, rank 2: 964, rank 3: 71, rank 4: 19) are the object of the torsion drivers.

Checks done on the finished logs:
* `scan_race_48.py` (signature of two processes sharing an instance file): 117 860 lines, 117 860 distinct balls,
  none logged twice; on the torsion-free lines the smallest "cands" is 5184 and the smallest node count 23 773; no
  line with cands < 2000 or nodes < 1000; no line that is neither dead nor TORSION;
* `compare_nonreps_48.py`: the 19 964 non-representative balls swept before the switch all have the verdict of their
  representative (dead 16 783, TORSION 3181), none different;
* the TORSION flag of every line agrees with the laptop session's list `tors_m4.json` (0 disagreement).

Files: `sweep_48_all.log.gz` (all the lines, sorted; sha256 of the uncompressed file b8fac2c90714ef47...),
`sweep_48_torsion.txt`, `pool_48.log.gz` (one line per part: index, return code, seconds, last line of the driver).
`reps48.txt` is the laptop session's file (sha256 6f2968daa1c9deb7...), not copied here.
Not done here: any audit of the laptop session's model or solver; the complete isomorphism check of the reduction
(queued, see NOTE 17.78).
