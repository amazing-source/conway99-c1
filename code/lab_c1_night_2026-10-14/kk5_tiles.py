"""Residue of kk5 (five lines through x pairwise in grids + the grid on blocks 6, 7) with the 84 tile clauses at x
(NOTE_NIGHT 17.4(a): three pairings of a grid force the fourth), one call per remaining class of M_11.

usage: python kk5_tiles.py workdir limit        -> appends to kk5_tiles_log.txt: K verdict seconds tiles
One process, cadical calls in sequence, 2 GB bound.
"""
import ast
import subprocess
import sys
import time

import family as FAM
import h12_instance as H
import kk5_step as KS
import pattern_test as PT
import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"
workdir, limit = sys.argv[1], float(sys.argv[2])
cases = []
for line in open("kk5_all_log.txt"):
    t = line.split(None, 4)
    if len(t) == 5 and t[2] == "UNKNOWN":
        cases.append((int(t[0]), ast.literal_eval(t[4])))
for K, m11 in cases:
    pres = KS.prescriptions("g67")
    pres[11] = sorted(set(pres[11]) | set(m11))
    n, k, lam, mu, fixed, mate, outer, idx = H.build(FAM.share_from(pres))
    enc, e = S.encode(n, k, lam, mu, fixed)
    extra = PT.add_tiles(enc, e, idx)
    cnf = workdir + "/kk5_tiles.cnf"
    S.write_dimacs(enc, cnf)
    t0 = time.time()
    try:
        r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=limit)
        res = r.stdout
    except subprocess.TimeoutExpired:
        res = ""
    v = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
    line = "%d %s %.1f tiles=%d" % (K, v, time.time() - t0, extra)
    print(line, flush=True)
    open("kk5_tiles_log.txt", "a").write(line + "\n")
