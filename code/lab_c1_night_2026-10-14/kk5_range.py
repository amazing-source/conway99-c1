"""kk5 with M_11 prescribed, for the classes K0..K1-1 of kk5_classes.txt, with a given time limit.
usage: python kk5_range.py workdir K0 K1 limit      -> appends to kk5_all_log.txt (same format as kk5_all.py)"""
import ast
import subprocess
import sys
import time

import family as FAM
import h12_instance as H
import srg_sat as S
from kk5_all import CADICAL, POINT_TO_INNER

workdir, k0, k1, limit = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
reps = [ast.literal_eval(line) for line in open("kk5_classes.txt")]
for K in range(k0, min(k1, len(reps))):
    cnt, m = reps[K]
    pres = FAM.prescriptions("kk5")
    pres[11] = [(POINT_TO_INNER[p], POINT_TO_INNER[q]) for p, q in m]
    n, k, lam, mu, fixed, mate, outer, idx = H.build(FAM.share_from(pres))
    enc, e = S.encode(n, k, lam, mu, fixed)
    cnf = workdir + "/kk5_case.cnf"
    S.write_dimacs(enc, cnf)
    t0 = time.time()
    try:
        r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=limit)
        res = r.stdout
    except subprocess.TimeoutExpired:
        res = ""
    dt = time.time() - t0
    verdict = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
    line = "%d %d %s %.1f %s" % (K, cnt, verdict, dt, pres[11])
    print(line, flush=True)
    with open("kk5_all_log.txt", "a") as f:
        f.write(line + "\n")
