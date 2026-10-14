"""One random complete local type (14 random perfect matchings) with a long time limit: does cadical refute it?
usage: python full_random_type.py workdir seed limit_seconds   -> appends to fulltype_log.txt: seed verdict seconds"""
import random
import subprocess
import sys
import time

import family as FAM
import h12_instance as H
import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"
workdir, seed, limit = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
rng = random.Random(seed)
mate = {a: (a + 1 if a % 2 == 1 else a - 1) for a in range(1, 15)}
pres = {}
for a in range(1, 15):
    pts = [b for b in range(1, 15) if b != a and b != mate[a]]
    rng.shuffle(pts)
    pres[a] = [(pts[2 * i], pts[2 * i + 1]) for i in range(6)]
n, k, lam, mu, fixed, _, outer, idx = H.build(FAM.share_from(pres))
enc, e = S.encode(n, k, lam, mu, fixed)
cnf = workdir + "/fulltype.cnf"
S.write_dimacs(enc, cnf)
free = sum(1 for x in e.values() if x not in (S.T, S.F))
t0 = time.time()
try:
    r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=limit)
    res = r.stdout
except subprocess.TimeoutExpired:
    res = ""
dt = time.time() - t0
verdict = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
line = "%d %s %.1f free=%d clauses=%d" % (seed, verdict, dt, free, len(enc.clauses))
print(line, flush=True)
open("fulltype_log.txt", "a").write(line + "\n")
if verdict == "SAT":
    open("fulltype_%d_model.txt" % seed, "w").write(repr(pres) + "\n" + res)
