"""Compact CNF (kissat) for grid covers of K_{9,9,9}, i.e. srg(243,22,1,2) with an equitable partition into 27 grids.
Encoding: matching variables X; for a pair (u in cell i, w in cell j) and a third cell e, the indicator
y = [sigma_ie(u) = sigma_je(w)] is defined by 2 clauses per point of e (no Tseitin AND):
   X_ie[u][z] & X_je[w][z] -> y ,   y & X_ie[u][z] -> X_je[w][z].
Pair conditions (lambda = 1, mu = 2) are counters (capped at 3) over these y's (plus the 8 in-grid terms for adjacent
cells).  Skeleton (lines per quotient triangle): t_a = closure at a, defined from X_ij and y.
  python3 grid243_cnf.py OUT.cnf [skeleton.pkl|-] [exclude.npy|-] [units.npy|-]"""
import sys, itertools, pickle, os, numpy as np

STD = np.zeros((9, 9), dtype=np.int64)
for a in range(9):
    for b in range(9):
        if a != b and (a // 3 == b // 3 or a % 3 == b % 3): STD[a, b] = 1
gnb = [[b for b in range(9) if STD[a, b]] for a in range(9)]
part = [i // 9 for i in range(27)]
nv = 0; ncl = 0; out = None
def new():
    global nv; nv += 1; return nv
def cl(lits):
    global ncl; out.write(" ".join(map(str, lits)) + " 0\n"); ncl += 1

def counter(lits, cap):
    """returns ge[1..cap]: ge[j] <-> (sum lits >= j)  (sequential counter, both directions)"""
    prev = [None] * (cap + 1)
    for x_ in lits:
        cur = [None] * (cap + 1)
        for j in range(1, cap + 1):
            v = new(); cur[j] = v
            if prev[j] is not None: cl([-prev[j], v])
            if j == 1: cl([-x_, v])
            elif prev[j - 1] is not None: cl([-prev[j - 1], -x_, v])
            a = [] if prev[j] is None else [prev[j]]
            if j == 1: cl([-v] + a + [x_])
            elif prev[j - 1] is None: cl([-v] + a)
            else: cl([-v] + a + [x_]); cl([-v] + a + [prev[j - 1]])
        prev = cur
    return prev

def main():
    global out
    path = sys.argv[1]
    arg = lambda i: sys.argv[i] if len(sys.argv) > i and sys.argv[i] != "-" else None
    skel = pickle.load(open(arg(2), "rb")) if arg(2) else None
    excl = np.load(arg(3)) if arg(3) else None
    units = np.load(arg(4)) if arg(4) else None
    out = open(path + ".body", "w")
    X = {}
    for i in range(27):
        for j in range(i + 1, 27):
            if part[i] != part[j]:
                M = [[new() for _ in range(9)] for _ in range(9)]; X[(i, j)] = M
                for a in range(9):
                    cl(M[a])
                    for b in range(9):
                        for c in range(b + 1, 9): cl([-M[a][b], -M[a][c]])
                for b in range(9):
                    cl([M[a][b] for a in range(9)])
                    for a in range(9):
                        for c in range(a + 1, 9): cl([-M[a][b], -M[c][b]])
    def x(i, a, j, b):
        return X[(i, j)][a][b] if i < j else X[(j, i)][b][a]
    ref = {j: 0 for j in range(9, 27)}; ref.update({j: 9 for j in range(1, 9)})
    for j, R in ref.items():
        cl([x(R, 0, j, 0)]); cl([x(R, 1, j, 1), x(R, 1, j, 4)])
    Y = {}
    for i in range(27):
        for j in range(i + 1, 27):
            thirds = [k for k in range(27) if part[k] != part[i] and part[k] != part[j]]
            for a in range(9):
                for b in range(9):
                    ys = []
                    for k in thirds:
                        y = new(); Y[(i, a, j, b, k)] = y; ys.append(y)
                        for c in range(9):
                            cl([-x(i, a, k, c), -x(j, b, k, c), y]); cl([-y, -x(i, a, k, c), x(j, b, k, c)])
                    if part[i] != part[j]:
                        lits = ys + [x(i, a2, j, b) for a2 in gnb[a]] + [x(i, a, j, b2) for b2 in gnb[b]]
                        ge = counter(lits, 3); e = x(i, a, j, b)
                        cl([-e, ge[1]]); cl([-e, -ge[2]])           # adjacent: exactly 1
                        cl([e, ge[2]]); cl([e, -ge[3]])             # non-adjacent: exactly 2
                    else:
                        ge = counter(ys, 3); cl([ge[2]]); cl([-ge[3]])
    if skel is not None:
        for (i, j, k) in itertools.product(range(9), range(9, 18), range(18, 27)):
            L = skel.get((i, j, k), 0)
            ts = []
            for a in range(9):
                t = new(); ts.append(t)
                for b in range(9):
                    y = Y[(i, a, j, b, k)]
                    cl([-x(i, a, j, b), -y, t]); cl([-t, -x(i, a, j, b), y])
            if L == 0: [cl([-t]) for t in ts]
            elif L == 9: [cl([t]) for t in ts]
            else:
                ge = counter(ts, L + 1); cl([ge[L]]); cl([-ge[L + 1]])
    if excl is not None:
        cl([-x(i, a, j, b) for (i, j) in X for a in range(9) for b in range(9) if excl[9 * i + a, 9 * j + b]])
    if units is not None:
        for (i, j) in X:
            for a in range(9):
                for b in range(9):
                    cl([x(i, a, j, b) if units[9 * i + a, 9 * j + b] else -x(i, a, j, b)])
    out.close()
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {ncl}\n")
        with open(path + ".body") as g:
            for line in g: f.write(line)
    os.remove(path + ".body")
    pickle.dump(X, open(path + ".map", "wb"))
    print("vars", nv, "clauses", ncl, flush=True)

if __name__ == "__main__":
    main()
