"""Run cadical on several families of family.py, one after the other, with a time limit each (one process).
usage: python run_family.py limit_seconds workdir name1 name2 ...      -> appends to family_log.txt"""
import subprocess
import sys
import time

import family as FAM
import h12_instance as H
import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"
limit, workdir = int(sys.argv[1]), sys.argv[2]
for name in sys.argv[3:]:
    n, k, lam, mu, fixed, mate, outer, idx = H.build(FAM.share_from(FAM.prescriptions(name)))
    enc, e = S.encode(n, k, lam, mu, fixed)
    cnf = workdir + "/family_%s.cnf" % name
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
    line = "%s free=%d vars=%d clauses=%d %s %.1f" % (name, free, enc.nv, len(enc.clauses), verdict, dt)
    print(line, flush=True)
    with open("family_log.txt", "a") as f:
        f.write(line + "\n")
    if verdict == "SAT":
        with open("family_%s_model.txt" % name, "w") as f:
            f.write(res)
