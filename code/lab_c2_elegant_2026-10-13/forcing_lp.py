"""Lab session, 2026-10-13. Mission "C2 without computation", step 1: is a short vector FORCED by modular forms alone?

The Jacobi theta series of (U; y1, y2) (Theorem R) lies in a space of dimension 61 (weil_dimension.py, coarse model).
Conditions on its coefficient table:
  N  : coefficient of (integral, class 0, E = 0) is 1;
  I  : no integral vector with 1 <= E <= EINT   (EINT = 7: hand lemma A.5;  EINT = 10: with T16, T18, T20);
  S  : no shadow vector with E < 11.5           (frame: every characteristic vector z has E(z) >= 46);
  P  : every coefficient is >= 0.
The script builds generators (jacobi_tables.py), extracts a basis, compares the rank with 61, and solves the linear
programme N + I + S + P on the window E <= EMAX.
python forcing_lp.py <number of generators> <EMAX> <EINT>        one process, a few minutes, < 2 GB."""
import sys, time, pickle, os, random
import numpy as np
import jacobi_tables as JT

ngen, EMAX, EINT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
emax4 = 4 * EMAX
t0 = time.time()
pats = JT.patterns()
print("patterns of (y1, y2) with entries <= 2 in absolute value: %d" % len(pats), flush=True)
gens = []
for p in pats:
    j = len(p)
    if j > 24:
        continue
    for i in range(0, (24 - j) // 8 + 1):
        gens.append((p, i))
random.Random(7).shuffle(gens)
gens = gens[:ngen]
cache = "tables_%d_%d.pkl" % (ngen, EMAX)
if os.path.exists(cache):
    tabs = pickle.load(open(cache, "rb"))
else:
    tabs = []
    for u, (p, i) in enumerate(gens):
        tabs.append(JT.table(list(p), i, emax4))
        if u % 10 == 0:
            print("   generator %d / %d (%.0f s)" % (u + 1, len(gens), time.time() - t0), flush=True)
    pickle.dump(tabs, open(cache, "wb"))
keys = sorted(set().union(*[set(t) for t in tabs]))
kidx = {k: i for i, k in enumerate(keys)}
M = [[t.get(k, 0) for k in keys] for t in tabs]
print("%d generators, %d table entries (E <= %d): integral %d, shadow %d" % (
    len(tabs), len(keys), EMAX, sum(1 for k in keys if k[0] == "I"), sum(1 for k in keys if k[0] == "S")), flush=True)
p = (1 << 61) - 1


def rank_mod(Mat):
    A = [[int(x) % p for x in row] for row in Mat]
    rows = len(A)
    cols = len(A[0])
    order = list(range(rows))
    r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        order[r], order[pr] = order[pr], order[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        r += 1
        if r == rows:
            break
    return r, order[:r]


r, basis = rank_mod(M)
print("rank of the generators (modulo a 61-bit prime): %d   (dimension of the space: 61)" % r, flush=True)
Bm = np.array([[float(x) for x in M[i]] for i in basis])
from scipy.optimize import linprog
nb = len(basis)
Aeq = []
beq = []
for k in keys:
    col = Bm[:, kidx[k]]
    kind, cl, e4 = k
    if kind == "I" and cl == (0, 0) and e4 == 0:
        Aeq.append(col)
        beq.append(1.0)
    elif kind == "I" and 0 < e4 <= 4 * EINT:
        Aeq.append(col)
        beq.append(0.0)
    elif kind == "S" and e4 < 46:
        Aeq.append(col)
        beq.append(0.0)
Aeq = np.array(Aeq)
beq = np.array(beq)
print("equalities: %d" % len(beq), flush=True)
scale = np.maximum(1.0, np.abs(Bm).max(axis=0))
eqs = np.maximum(1.0, np.abs(Aeq).max(axis=1))
res = linprog(c=np.zeros(nb), A_ub=-(Bm / scale).T, b_ub=np.zeros(len(keys)), A_eq=Aeq / eqs[:, None], b_eq=beq / eqs,
              bounds=[(None, None)] * nb, method="highs")
print("linear programme (N, I with E <= %d, S, P on E <= %d): status %d (%s)" % (EINT, EMAX, res.status, str(res.message)[:70]))
if res.status == 0:
    tab = res.x @ Bm
    small = sorted((k[2] / 4, k[0], k[1], tab[kidx[k]]) for k in keys if k[2] <= 4 * 16 and abs(tab[kidx[k]]) > 1e-6)
    print("   a feasible table, non-zero entries with E <= 16:")
    for e, kd, cl, v in small[:60]:
        print("      %s E = %g class %s: %.4f" % (kd, e, cl, v))
