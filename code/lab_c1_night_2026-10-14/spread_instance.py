"""Family "grid spread": the 99 vertices of srg(99,14,1,2) are partitioned into 11 sets inducing 3 x 3 grids.

Arithmetic of the family (NOTE_NIGHT section 18): a grid is a perfect code (every outside vertex has exactly one
neighbour in it), so with 11 disjoint grids every vertex has 4 neighbours in its own grid and exactly one in each
of the 10 others: 4 + 10 = 14. The graph is then a 9-fold cover of K_11 plus a grid on every fibre.

Vertices: (i, r, c), fibre i in 0..10, r, c in 0..2 -> 9 i + 3 r + c. Fixed: inside a fibre, adjacent iff same r or
same c. Free: all pairs in different fibres. Added (implied by the perfect code property): exactly one neighbour
of each vertex in each other fibre. Symmetry breaking (each justified in the note):
  * vertex (0,0,0) is adjacent to (j,0,0) for every j (translations of the fibre j);
  * the five outer lines through (0,0,0) pair the fibres as {1,2},{3,4},{5,6},{7,8},{9,10} (permutation of fibres).

usage: python spread_instance.py workdir limit [nfibres]
       nfibres < 11: only the first nfibres fibres carry a prescribed grid (family "nfibres pairwise disjoint grids
       around the fibre 0"); not implemented for this first test, the argument is recorded for the log only.
appends to spread_log.txt. One process, one cadical call, 2 GB bound.
"""
import subprocess
import sys
import time

import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"


def vid(i, r, c):
    return 9 * i + 3 * r + c


def build(sym=True):
    fixed = {}
    for i in range(11):
        pts = [(r, c) for r in range(3) for c in range(3)]
        for a in range(9):
            for b in range(a + 1, 9):
                (r1, c1), (r2, c2) = pts[a], pts[b]
                fixed[(vid(i, r1, c1), vid(i, r2, c2))] = (r1 == r2) or (c1 == c2)
    if sym:
        for j in range(1, 11):
            fixed[(vid(0, 0, 0), vid(j, 0, 0))] = True
            for t in range(1, 9):
                fixed[(vid(0, 0, 0), vid(j, t // 3, t % 3))] = False
                fixed[(vid(0, t // 3, t % 3), vid(j, 0, 0))] = False
        for j in range(1, 11, 2):
            fixed[(vid(j, 0, 0), vid(j + 1, 0, 0))] = True
    enc, e = S.encode(99, 14, 1, 2, fixed)

    def E(u, v):
        return e[(u, v)] if u < v else e[(v, u)]

    extra = 0
    for i in range(11):
        for u in range(9 * i, 9 * i + 9):
            for j in range(11):
                if j == i:
                    continue
                lits = [E(u, w) for w in range(9 * j, 9 * j + 9)]
                if any(x == S.T for x in lits):
                    for x in lits:
                        if x not in (S.T, S.F):
                            enc.add(-x)
                            extra += 1
                    continue
                free = [x for x in lits if x != S.F]
                enc.add(*free)
                extra += 1
                for a in range(len(free)):
                    for b in range(a + 1, len(free)):
                        enc.add(-free[a], -free[b])
                        extra += 1
    return enc, e, extra


if __name__ == "__main__":
    workdir, limit = sys.argv[1], float(sys.argv[2])
    enc, e, extra = build()
    cnf = workdir + "/spread.cnf"
    S.write_dimacs(enc, cnf)
    free = sum(1 for x in e.values() if x not in (S.T, S.F))
    print("grid spread: free pairs=%d, variables=%d, clauses=%d (of which %d implied)" % (free, enc.nv, len(enc.clauses), extra), flush=True)
    t0 = time.time()
    try:
        r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=limit)
        res = r.stdout
    except subprocess.TimeoutExpired:
        res = ""
    dt = time.time() - t0
    verdict = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
    line = "spread11 %s %.1f free=%d" % (verdict, dt, free)
    print(line, flush=True)
    open("spread_log.txt", "a").write(line + "\n")
    if verdict == "SAT":
        model = [int(t) for ln in res.splitlines() if ln.startswith("v ") for t in ln.split()[1:]]
        open(workdir + "/spread_model.txt", "w").write(" ".join(map(str, model)))
