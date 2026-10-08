"""C1, lab session, 2026-10-08. Cauchy-Schwarz / sum-of-squares cuts on the census polytope (exploration, floating point).

  python sos_flags.py <census2 order-10 json> <root> <a> <nmax> <objective> [iterations] [reps10 json]
     root: vertex | edge | nonedge | triangle | path | prism | c4 | paw | house
     a: largest number of extra vertices in a flag;  nmax: largest order of the types used
     objective: maxP | maxH | max8 | max9 | maxPhi | r37
        (maxPhi = number of pairs (prism, far triangle), needs reps10 json;
         r37 = minimum of r8 + (651/34) r6 over supports <= 9, needs reps10 json)

For an embedding theta of the root sigma (an ordered tuple of vertices inducing sigma) and a flag F (sigma plus j <= a
extra vertices, rooted isomorphism type), c_F(theta) = number of j-subsets A of the other vertices with (theta, A) of
type F. Then  M[F, G] = sum_theta c_F(theta) c_G(theta)  is positive semidefinite, and it is LINEAR in the census:
    M[F, G] = sum over types H of N_H * #{ (tau, A, B) : tau a root tuple in H, A u B = V(H) minus tau, types F, G }.
The matrix is restricted to flags with 2 j <= nmax - |sigma|, so that every product is complete.
Positivity of the counts N_H does not imply that M is positive semidefinite.
Loop: solve the LP, evaluate M at the optimum, take the eigenvectors z of negative eigenvalue (scaled matrix), add the
linear cuts z^t M z >= 0, repeat. Prints the objective after each round. One process, memory below 3 GB."""
import sys, json, time
from fractions import Fraction as Fr
from itertools import combinations, permutations
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack
import census2 as C2
t0 = time.time(); D = json.load(open(sys.argv[1])); rootname = sys.argv[2]; amax = int(sys.argv[3]); nmax = int(sys.argv[4]); obj = sys.argv[5]
iters = int(sys.argv[6]) if len(sys.argv) > 6 else 6
ROOTS = {"vertex": (1, []), "edge": (2, [(0, 1)]), "nonedge": (2, []), "triangle": (3, [(0, 1), (0, 2), (1, 2)]), "path": (3, [(0, 1), (1, 2)]),
         "prism": (6, [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4), (2, 5)]), "c4": (4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
         "paw": (4, [(0, 1), (0, 2), (1, 2), (2, 3)]), "house": (5, [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)])}
s, sedges = ROOTS[rootname]; sadj = [[False] * s for _ in range(s)]
for i, j in sedges: sadj[i][j] = sadj[j][i] = True
jmax = min(amax, (nmax - s) // 2)
npar = len(D["params"])
# ---- LP rows: positivity of all type counts of orders 6..10
ri = []; ci = []; va = []; const = []; r = 0; seen = set()
for n in ("6", "7", "8", "9", "10"):
    for key, rows, aut, form in D["types"][n]:
        sig = tuple(sorted(form.items()))
        if sig in seen or not form: continue
        seen.add(sig); f = {int(p): float(Fr(v_)) for p, v_ in form.items()}; sc = max(abs(x) for x in f.values())
        const.append(f.get(0, 0.0) / sc)
        for p, v_ in f.items():
            if p: ri.append(r); ci.append(p - 1); va.append(v_ / sc)
        r += 1
A = csr_matrix((va, (ri, ci)), shape=(r, npar)); const = np.array(const)


def rooted_tuples(n, rows):
    out = []
    def rec(t):
        i = len(t)
        if i == s: out.append(tuple(t)); return
        for v in range(n):
            if v in t: continue
            if all((rows[v] >> t[q] & 1) == (1 if sadj[i][q] else 0) for q in range(i)): t.append(v); rec(t); t.pop()
    rec([]); return out


def fkey(rows, tau, Aset):
    rm = {v: sum(1 << q for q in range(s) if rows[v] >> tau[q] & 1) for v in Aset}
    order = sorted(Aset, key=lambda v: rm[v]); groups = []
    for v in order:
        if groups and rm[groups[-1][0]] == rm[v]: groups[-1].append(v)
        else: groups.append([v])
    def gen(gi, acc):
        if gi == len(groups): yield acc; return
        for perm in permutations(groups[gi]): yield from gen(gi + 1, acc + list(perm))
    best = None
    for seq in gen(0, []):
        code = 0
        for x in range(len(seq)):
            for y in range(x + 1, len(seq)): code = code << 1 | (rows[seq[x]] >> seq[y] & 1)
        if best is None or code < best: best = code
    return (tuple(rm[v] for v in order), best)


types = [(1, [0], 1, {"0": str(D["v"])})] if s == 1 else []
for n in range(max(s, 2), nmax + 1):
    for key, rows, aut, form in D["types"][str(n)]: types.append((n, rows, aut, form))
flagid = {}; I = []; J = []; Hh = []; Trow = []; Tcol = []; Tval = []; Tk = []; nH = 0
for n, rows, aut, form in types:
    m = n - s
    if m > 2 * jmax: continue
    tuples = rooted_tuples(n, rows)
    if not tuples: continue
    if aut is None: aut = C2.aut_order(n, rows)
    h = nH; nH += 1; k0 = 0.0
    for p, v_ in form.items():
        val = float(Fr(v_)) / aut
        if int(p): Trow.append(h); Tcol.append(int(p) - 1); Tval.append(val)
        else: k0 = val
    Tk.append(k0)
    for tau in tuples:
        rest = [v for v in range(n) if v not in tau]; ids = []
        for j in range(0, min(jmax, m) + 1):
            for Aset in combinations(rest, j):
                k_ = fkey(rows, tau, Aset)
                if k_ not in flagid: flagid[k_] = len(flagid)
                msk = 0
                for v in Aset: msk |= 1 << v
                ids.append((msk, flagid[k_]))
        full = 0
        for v in rest: full |= 1 << v
        for ma, fa in ids:
            need = full & ~ma
            for mb, fb in ids:
                if need & ~mb == 0: I.append(fa); J.append(fb); Hh.append(h)
nF = len(flagid); I = np.array(I, dtype=np.int32); J = np.array(J, dtype=np.int32); Hh = np.array(Hh, dtype=np.int32)
T = csr_matrix((Tval, (Trow, Tcol)), shape=(nH, npar)); Tk = np.array(Tk)
print("root %s (order %d), flags with at most %d extra vertices, types of order <= %d: %d flags, %d types with a root copy, %d incidences  [%.0f s]" % (
    rootname, s, jmax, nmax, nF, nH, len(I), time.time() - t0), flush=True)


def vec(form):
    c = np.zeros(npar)
    for p, v_ in form.items():
        if int(p): c[int(p) - 1] = float(Fr(v_))
    return c, float(Fr(form.get("0", 0)))


orders = np.array([p[0] for p in D["params"]]); k0 = 0.0; sgn = -1
if obj == "maxP": c = np.zeros(npar); c[0] = -1.0
elif obj == "maxH": c = np.zeros(npar); c[1] = -1.0
elif obj == "max8": c = -(orders == 8).astype(float)
elif obj == "max9": c = -(orders == 9).astype(float)
elif obj == "maxPhi":
    R = json.load(open(sys.argv[7])); cc, kk = vec(R["6,3,4"]); c = -cc; k0 = kk
else:
    R = json.load(open(sys.argv[7])); c = np.zeros(npar); sgn = 1
    for k_, f in R.items():
        a_, b_, q_ = (int(x) for x in k_.split(","))
        if a_ + b_ > 9 or q_ not in (6, 8): continue
        cc, kk = vec(f); w = 1.0 if q_ == 8 else 651 / 34; c += w * cc; k0 += w * kk
cuts = []; cutb = []
for it in range(iters + 1):
    Aub, bub = -A, const
    if cuts: Aub = vstack([-A, csr_matrix(-np.array(cuts))]); bub = np.append(const, np.array(cutb))
    res = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(0, None)] * npar, method="highs-ipm")
    if res.status != 0: print("round %d: LP status %d (%s)" % (it, res.status, res.message[:60])); break
    x = res.x; Nval = T @ x + Tk
    M = np.zeros((nF, nF)); np.add.at(M, (I, J), Nval[Hh]); M = (M + M.T) / 2
    d = np.sqrt(np.maximum(np.diag(M), 1e-30)); Ms = M / np.outer(d, d); w, Z = np.linalg.eigh(Ms)
    neg = [q for q in range(nF) if w[q] < -1e-7]
    print("round %d: objective %s = %.8g ; P = %.5g ; smallest scaled eigenvalues %s ; %d negative ; %d cuts so far  [%.0f s]" % (
        it, obj, sgn * res.fun + (k0 if sgn == 1 else k0), x[0], " ".join("%.3g" % q for q in w[:4]), len(neg), len(cuts), time.time() - t0), flush=True)
    if not neg or it == iters: break
    for q in neg[:40]:
        z = Z[:, q] / d; wH = np.zeros(nH); np.add.at(wH, Hh, z[I] * z[J])
        cv = T.T @ wH; kv = float(wH @ Tk); sc = max(np.abs(cv).max(), abs(kv), 1e-30)
        cuts.append(cv / sc); cutb.append(kv / sc)                         # cv.x + kv >= 0  <=>  -cv.x <= kv
