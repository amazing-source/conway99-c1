"""Target H12 (a line {x, 13, 14} with 12 prisms), one case for each class of psi_reps.txt:
M_13 = beta_b and M_14 = beta_c are fixed (points 0..11 of psi_orbits = inner vertices 1..12), every M_a with
a <= 12 pairs 13 with 14, the rest is free. One cadical call per case (one process at a time, 2 GB bound).

usage: python run_h12.py limit_seconds workdir K0 K1 [step]      -> appends to h12_log.txt:  K count verdict seconds
"""
import ast
import subprocess
import sys
import time

import family as FAM
import h12_instance as H
import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"
limit, workdir, k0, k1 = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
step = int(sys.argv[5]) if len(sys.argv) > 5 else 1
reps = [ast.literal_eval(line) for line in open("psi_reps.txt")]
for K in range(k0, min(k1, len(reps)), step):
    cnt, mb, mc = reps[K]
    pres = {a: [(13, 14)] for a in range(1, 13)}
    pres[13] = [(p + 1, q + 1) for p, q in mb]
    pres[14] = [(p + 1, q + 1) for p, q in mc]
    n, k, lam, mu, fixed, mate, outer, idx = H.build(FAM.share_from(pres))
    enc, e = S.encode(n, k, lam, mu, fixed)
    cnf = workdir + "/h12_case.cnf"
    S.write_dimacs(enc, cnf)
    t0 = time.time()
    try:
        r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=limit)
        res = r.stdout
    except subprocess.TimeoutExpired:
        res = ""
    dt = time.time() - t0
    verdict = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
    line = "%d %d %s %.1f" % (K, cnt, verdict, dt)
    print(line, flush=True)
    with open("h12_log.txt", "a") as f:
        f.write(line + "\n")
    if verdict == "SAT":
        with open("h12_%d_model.txt" % K, "w") as f:
            f.write(res)
