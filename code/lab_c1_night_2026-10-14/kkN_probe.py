"""Family kk5 (blocks 1..5 pairwise grids at x) with a few of the four free matchings M_11..M_14 chosen at random.
usage: python kk5_probe.py workdir limit seed which     which = comma list of inner vertices among 11,12,13,14
       (empty string = none)   -> appends to kkN_probe_log.txt: seed which verdict seconds"""
import random
import subprocess
import sys
import time

import family as FAM
import h12_instance as H
import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"
workdir, limit, seed, which, fam = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
rng = random.Random(seed)
mate = {a: (a + 1 if a % 2 == 1 else a - 1) for a in range(1, 15)}
pres = FAM.prescriptions(fam)
for a in [int(t) for t in which.split(",") if t]:
    pts = [b for b in range(1, 15) if b != a and b != mate[a]]
    rng.shuffle(pts)
    pres[a] = [(pts[2 * i], pts[2 * i + 1]) for i in range(6)]
n, k, lam, mu, fixed, _, outer, idx = H.build(FAM.share_from(pres))
enc, e = S.encode(n, k, lam, mu, fixed)
cnf = workdir + "/kkN_probe.cnf"
S.write_dimacs(enc, cnf)
t0 = time.time()
try:
    r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=limit)
    res = r.stdout
except subprocess.TimeoutExpired:
    res = ""
dt = time.time() - t0
verdict = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
line = "%s %d [%s] %s %.1f" % (fam, seed, which, verdict, dt)
print(line, flush=True)
open("kkN_probe_log.txt", "a").write(line + "\n")
