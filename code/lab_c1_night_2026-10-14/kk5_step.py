"""Steps of the decision of kk5 after the first pass (NOTE_NIGHT section 16).

Named cases (extra prescriptions on top of kk5 = blocks 1..5 pairwise grids at x):
  g67        blocks 6 and 7 also form a grid: M_11, M_12 pair (13,14); M_13, M_14 pair (11,12)
  t1_II      g67 and M_1 pairs (11,13), (12,14)          (a "crossed" completion of one matching of blocks 1..5)
  allI       g67 and every M_a, a <= 10, pairs (11,12) and (13,14)   (all of them respect all seven blocks)
  allI_m:<pairs>   allI and M_11 restricted to 1..10 given as a list of pairs, e.g. allI_m:1-3,2-5,4-7,6-9,8-10
  g67_m:<pairs>    g67 and M_11 restricted to 1..10 given
usage: python kk5_step.py workdir limit case [case ...]    -> appends to kk5_step_log.txt: case verdict seconds
"""
import subprocess
import sys
import time

import family as FAM
import h12_instance as H
import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"


def prescriptions(case):
    """case = name[;a:pairs[;a:pairs...]] with name in {g67, t1_II, allI} and pairs like 1-3,2-5 (pairs of M_a)."""
    parts = case.split(";")
    name = parts[0].partition(":")[0]
    legacy = parts[0].partition(":")[2]
    pres = FAM.prescriptions("kk5")
    for a in (11, 12):
        pres[a].append((13, 14))
    for a in (13, 14):
        pres[a].append((11, 12))
    if name == "t1_II":
        pres[1] += [(11, 13), (12, 14)]
    if name.startswith("allI"):
        for a in range(1, 11):
            pres[a] += [(11, 12), (13, 14)]
    if legacy:
        pres[11] += [tuple(int(t) for t in p.split("-")) for p in legacy.split(",")]
    for part in parts[1:]:
        a, _, arg = part.partition(":")
        pres[int(a)] += [tuple(int(t) for t in p.split("-")) for p in arg.split(",")]
    return pres


if __name__ == "__main__":
    workdir, limit = sys.argv[1], float(sys.argv[2])
    for case in sys.argv[3:]:
        n, k, lam, mu, fixed, mate, outer, idx = H.build(FAM.share_from(prescriptions(case)))
        enc, e = S.encode(n, k, lam, mu, fixed)
        cnf = workdir + "/kk5_step.cnf"
        S.write_dimacs(enc, cnf)
        t0 = time.time()
        try:
            r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=limit)
            res = r.stdout
        except subprocess.TimeoutExpired:
            res = ""
        dt = time.time() - t0
        verdict = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
        line = "%s %s %.1f" % (case, verdict, dt)
        print(line, flush=True)
        open("kk5_step_log.txt", "a").write(line + "\n")
