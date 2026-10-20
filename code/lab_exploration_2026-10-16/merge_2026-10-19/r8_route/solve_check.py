"""Solve one CNF of the R8 family with cadical and check any model independently (LAB 20/10/2026).
usage: python solve_check.py <cnf> <cadical exe> <seconds> <K> <nx or full> <exact letters e.g. 0,1,2,3> <out json>
        [cadical options...]
Edge variables are 1..C(n,2) in combinations order for every encoder used here (mine and five_cnf.py)."""
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r8lib  # noqa: E402


def main():
    cnf, exe, secs, K, nx, exact, out = sys.argv[1:8]
    extra = sys.argv[8:]
    M = r8lib.Model(int(K), nx=None if nx == "full" else int(nx))
    ex = [int(t) for t in exact.split(",") if t]
    t0 = time.time()
    mp = out + ".model"
    with open(mp, "w") as mf:
        p = subprocess.Popen([exe, "-q"] + extra + [cnf], stdout=mf, stderr=subprocess.DEVNULL)
        try:
            p.wait(timeout=float(secs))
            st = {10: "SAT", 20: "UNSAT"}.get(p.returncode, "rc%d" % p.returncode)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
            st = "TIMEOUT"
    rec = {"cnf": os.path.basename(cnf), "status": st, "seconds": round(time.time() - t0, 1), "options": extra}
    if st == "SAT":
        vals = set()
        for line in open(mp):
            if line.startswith("v "):
                vals.update(int(t) for t in line.split()[1:] if t != "0")
        E = [p for p in M.pairs if M.var(*p) in vals]
        bad = M.check(E, extra_exact=ex)
        rec["edges"] = len(E)
        rec["check"] = "OK" if not bad else bad[:5]
        json.dump({"K": M.K, "labels": [sorted(l) for l in M.S], "edges": [list(p) for p in E]}, open(out, "w"))
    os.remove(mp)
    print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
