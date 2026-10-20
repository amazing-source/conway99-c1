"""Hardness scaling of R8 by partial release of a fixed base (LAB 20/10/2026).

Instance I(s, m, o): R8 CNF + units fixing the adjacency between the base labels that are NOT released, copied from the
four-star block of the R7 witness of seed s (16/10, r7_seed<s>.json; that block does not accept the eighth label: I(s,0)
is UNSAT).  The released set = the first m base labels in the random order o.  Every pair touching a released label,
and every pair touching X, is free.  I(s, 44, o) = R8 itself.  A SAT answer would be an R8 solution: it is decoded and
checked independently (Model.check) before anything is said.
usage: python release_scan.py <witness dir> <out jsonl> <seconds per instance> <budget> <cadical exe>
                              <spec e.g. 1:0,4,8:o1> [<spec> ...] -- <cnf1> [<cnf2> ...]"""
import json
import os
import random
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r8lib  # noqa: E402
from knuth_la import cadical, write_cube_cnf  # noqa: E402


def main():
    wdir, out, T, budget, exe = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    k = sys.argv.index("--")
    specs, cnfs = sys.argv[6:k], sys.argv[k + 1:]
    M = r8lib.Model(14)
    nB = len(M.B)
    t_start = time.time()
    for spec in specs:
        s, ms, o = spec.split(":")
        d = json.load(open(os.path.join(wdir, "r7_seed%s.json" % s)))
        labs = [frozenset(x) for x in d["labels"]]
        E = set()
        for i, j in d["edges"]:
            a, b = M.idx[labs[i]], M.idx[labs[j]]
            if a < nB and b < nB:
                E.add((min(a, b), max(a, b)))
        order = list(range(nB))
        random.Random("%s-%s" % (s, o)).shuffle(order)
        for m in [int(t) for t in ms.split(",")]:
            rel = set(order[:m])
            units = []
            for (i, j) in M.pairs:
                if j < nB and i not in rel and j not in rel:
                    units.append(M.var(i, j) if (i, j) in E else -M.var(i, j))
            for cnf in cnfs:
                if time.time() - t_start + T + 5 > budget:
                    print("budget reached", flush=True)
                    return
                tmp = out + ".tmp.cnf"
                write_cube_cnf(cnf, tmp, units)
                if True:
                    t1 = time.time()
                    mp = tmp + ".model"
                    with open(mp, "w") as mf:
                        p = subprocess.Popen([exe, tmp], stdout=mf, stderr=subprocess.DEVNULL)
                        try:
                            p.wait(timeout=T)
                            st = {10: "SAT", 20: "UNSAT"}.get(p.returncode, "rc%d" % p.returncode)
                        except subprocess.TimeoutExpired:
                            p.kill()
                            p.wait()
                            st = "TIMEOUT"
                    ts = round(time.time() - t1, 2)
                    conf = None
                    vals = set()
                    for line in open(mp):
                        if line.startswith("c conflicts:"):
                            conf = int(line.split()[2])
                        elif line.startswith("v ") and st == "SAT":
                            vals.update(int(t) for t in line.split()[1:] if t != "0")
                    os.remove(mp)
                rec = {"seed": s, "order": o, "m": m, "units": len(units), "cnf": os.path.basename(cnf), "status": st,
                       "seconds": ts, "conflicts": conf}
                if st == "SAT":
                    Ed = [p for p in M.pairs if M.var(*p) in vals]
                    bad = M.check(Ed)
                    rec["check"] = "OK" if not bad else bad[:3]
                    json.dump({"K": 14, "labels": [sorted(l) for l in M.S], "edges": [list(p) for p in Ed]},
                              open(out + ".SAT_%s_%s_%d.json" % (s, o, m), "w"))
                os.remove(tmp)
                print(json.dumps(rec), flush=True)
                with open(out, "a") as fh:
                    fh.write(json.dumps(rec) + "\n")


if __name__ == "__main__":
    main()
