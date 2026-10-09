"""C1, lab session, 2026-10-09. EXACT version of the laptop session's probe harm4.py (conway99-c2-aws, commit faf2ac76d,
c1_mandat_c_transformations/): the two quartic harmonic theta series (vertices, lines) of weight 26 on Gamma_0(7) added
to the degree-0 theta LP. The construction of the constraints is the laptop session's, unchanged and already exact
(fractions); only the final floating LP is replaced by the exact rational simplex of theta_lp_exact.py, which returns a
Farkas certificate when the system is infeasible. Added: CORNER=<6 bits> gives to the catalogued dual vectors of norms
6, 8, 10 (Codex's uniform lower bounds on distinct vectors: 45 964, 3 371 634, 34 087 368) the extreme value lo (0) or
hi (1) of the Cauchy-Schwarz range of P, bits = (V6, V8, V10, T6, T8, T10). The set of catalogue sums for which the
system is feasible is convex, so if all 64 corners are feasible no exact value of these sums can make it infeasible.

  python harm4_exact.py <rank> <nmax> <mode: base | V | T | VT>          (CORNER in the environment)
One process; exact arithmetic, seconds to minutes."""
import sys, json
from fractions import Fraction as Fr
import mf7

r = int(sys.argv[1]); NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 24; MODE = sys.argv[3] if len(sys.argv) > 3 else "VT"
alpha = r - 1
TIGHT = "tight" in sys.argv
import os
CORNER = os.environ.get("CORNER", "")
CAT = {3: 45964, 4: 3371634, 5: 34087368}
F = json.load(open("C:/home/researcher/Desktop/c1-codex/data/codex_theta7_basis_q84.json"))

# ---------- degree 0: a_n, b_n as affine functions of the free coordinates c_1..c_7 (vector index 0 = constant)
NV0 = 8
cs = [[Fr(0)] * NV0 for _ in range(15)]
cs[0][0] = Fr(7) ** (25 - alpha // 2)
for j in range(1, 8): cs[j][j] = Fr(1)
for n in range(7):
    j = 14 - n
    tot = [sum(cs[k][t] * F[k][n] for k in range(j + 1, 15)) for t in range(NV0)]
    cs[j] = [Fr(int(n == 0 and t == 0)) - tot[t] for t in range(NV0)]
ds = [[x * Fr(7) ** (alpha // 2 + 3 - 2 * i) for x in cs[14 - i]] for i in range(15)]
def expansion(co, n): return [sum(co[j][t] * F[j][n] for j in range(15)) for t in range(NV0)]
a = [expansion(cs, n) for n in range(NMAX + 1)]; b = [expansion(ds, n) for n in range(NMAX + 1)]
assert a[0] == [1] + [0] * 7 and b[0] == [1] + [0] * 7 and all(a[n] == [0] * 8 for n in range(1, 7))

# ---------- variables of the LP: c_1..c_7, P (prisms), 17 coordinates of G_L^V, 17 of G_L^T
S26 = mf7.Space(26); D = len(S26.mons)
names = [f"c{j}" for j in range(1, 8)] + ["P"] + [f"gV{i}" for i in range(D)] + [f"gT{i}" for i in range(D)]
NV = len(names); iP = 7; oV = 8; oT = 8 + D
def lift(v8):
    """affine form in (1, c1..c7) -> affine form in (1, all variables)"""
    return [v8[0]] + list(v8[1:]) + [Fr(0)] * (NV - 7)
def unit(i, cf=Fr(1)):
    v = [Fr(0)] * (NV + 1); v[1 + i] = cf; return v
def add(*vs): return [sum(x) for x in zip(*vs)]
def sc(v, s): return [x * s for x in v]
A = [lift(x) for x in a]; Bm = [lift(x) for x in b]; Pv = unit(iP)
const = lambda x: [Fr(x)] + [Fr(0)] * NV

EQ, GE = [], []          # affine forms: EQ: form == 0 ; GE: form >= 0
def ge(f, label): GE.append((f, label))
def eq(f, label): EQ.append((f, label))

for n in range(7, NMAX + 1): ge(A[n], f"a{n}>=0")
for n in range(1, NMAX + 1): ge(Bm[n], f"b{n}>=0")
ge(add(const(990), sc(A[7], -1)), "a7<=990")
ge(add(const(55440), sc(A[7], -7), sc(A[8], -8)), "7a7+8a8<=55440")
ge(add(const(44), sc(Bm[1], -1)), "b1<=44")
ge(add(Bm[2], const(-462), sc(Bm[1], -41)), "b2>=462+41b1")
if r >= 37: ge(add(Bm[3], const(-45964)), "b3>=45964")
else: ge(add(Bm[3], const(-24948)), "b3>=24948")
ge(add(Bm[4], const(-(CAT[4] if CORNER else 2729034))), "b4>=cat")
ge(add(Bm[5], const(-(CAT[5] if CORNER else 18001368))), "b5>=cat")
for k in range(1, NMAX // 7 + 1): ge(add(A[7 * k], sc(Bm[k], -1)), f"a{7*k}>=b{k}")
ge(Pv, "P>=0"); ge(add(const(852), sc(Pv, -1)), "P<=852")

NATQ = {}
def quartic(off, tag, lamL, rootM, known, loM, hiM, loL, hiL):
    """adds the constraints of one quartic series.  known[n] = (count, affine form of the exact sum over the known vectors)"""
    gco = [unit(off + i) for i in range(D)]                       # coordinates of G_L as affine forms
    def coefL(n): return add(*[sc(gco[i], Fr(S26.ser[i][n])) for i in range(D)])
    # G_M = -7^((r-23)/2) * (G_L | W7)
    fr = [add(*[sc(gco[i], S26.W[i][j]) for i in range(D)]) for j in range(D)]
    fac = -Fr(7) ** Fr(r - 23, 2) if (r - 23) % 2 == 0 else None
    def coefM(n): return sc(add(*[sc(fr[j], Fr(S26.ser[j][n])) for j in range(D)]), fac)
    NATQ[tag] = [coefL(n) for n in range(11, 16)]
    eq(coefL(0), f"{tag}: cusp at infinity"); eq(coefM(0), f"{tag}: cusp at 0")
    for n in range(1, 7): eq(coefL(n), f"{tag}: g{n}=0")
    for n in range(7, 11): eq(add(coefL(n), sc(A[n], -lamL(n))), f"{tag}: g{n}=lam*a{n}")
    eq(add(coefM(1), sc(Bm[1], -rootM)), f"{tag}: m1=root*b1")
    for n in range(2, NMAX + 1):
        cnt, exact = known.get(n, (0, const(0)))
        if CORNER and n in CAT:
            bit = CORNER[(0 if tag == "V" else 3) + n - 3]; extra = CAT[n] - cnt
            exact = add(exact, const(extra * (loM(n) if bit == "0" else hiM(n)))); cnt = CAT[n]
        rest = add(Bm[n], const(-cnt))                           # number of other vectors of norm 2n, >= 0
        ge(add(coefM(n), sc(exact, -1), sc(rest, -loM(n))), f"{tag}: m{n} lower")
        ge(add(sc(coefM(n), -1), exact, sc(rest, hiM(n))), f"{tag}: m{n} upper")
    for n in range(11, NMAX + 1):
        ge(add(coefL(n), sc(A[n], -loL(n))), f"{tag}: g{n} lower")
        ge(add(sc(coefL(n), -1), sc(A[n], hiL(n))), f"{tag}: g{n} upper")

if "V" in MODE:
    quartic(oV, "V", lambda n: 2 * n - Fr(8, 69) * n * n, Fr(82, 483),
            {2: (462, const(462 * Fr(-124, 1127))), 3: (8316, const(8316 * Fr(3102, 1127))), 4: (1386, const(1386 * Fr(30712, 3381)))},
            lambda n: (Fr(4, 99) - Fr(8, 69)) * n * n, lambda n: (Fr(16, 9) - Fr(8, 69)) * n * n,
            lambda n: ({11: Fr(22, 3), 12: Fr(32, 3), 13: Fr(14)}.get(n, Fr(4, 99) * n * n) if TIGHT else Fr(4, 99) * n * n) - Fr(8, 69) * n * n,
            lambda n: ({11: Fr(34), 12: Fr(96), 13: Fr(98)}.get(n, Fr(16, 9) * n * n) if TIGHT else Fr(16, 9) * n * n) - Fr(8, 69) * n * n)
else:
    for i in range(D): eq(unit(oV + i), "V unused")
if "T" in MODE:
    # line vectors: sum of S_4 over the 462 vectors = 149688 + 48 P ; P_T = (S_4 - (504/23) n^2)/49
    linesum = sc(add(const(Fr(149688) - 462 * Fr(504, 23) * 4), sc(Pv, 48)), Fr(1, 49))
    quartic(oT, "T", lambda n: 6 * n - Fr(72, 161) * n * n, Fr(66, 161),
            {2: (462, linesum), 3: (8316, const(8316 * Fr(-534, 1127))), 4: (1386, const(1386 * Fr(-888, 1127)))},
            lambda n: (Fr(1764, 231) - Fr(504, 23)) * n * n / 49, lambda n: (336 - Fr(504, 23)) * n * n / 49,
            lambda n: (Fr(36, 231) - Fr(72, 161)) * n * n,
            lambda n: ((24 * n if (TIGHT and 11 <= n <= 13) else Fr(48, 7) * n * n)) - Fr(72, 161) * n * n)
else:
    for i in range(D): eq(unit(oT + i), "T unused")

# ---------- exact elimination of the equalities, then an exact change to natural variables, then a scaled LP
rows = [f[1:] + [-f[0]] for f, _ in EQ]                           # sum coef*x = -const
red, piv, _ = mf7.rref(rows)
for rw in red: assert any(x != 0 for x in rw[:-1]), "inconsistent equalities: " + str(rw[-1])
free = [i for i in range(NV) if i not in piv]
def subst(f):
    c0 = f[0]; cf = {i: Fr(0) for i in free}
    for i in range(NV):
        x = f[1 + i]
        if x == 0: continue
        if i in piv:
            rw = red[piv.index(i)]; c0 += x * rw[-1]
            for k in free: cf[k] -= x * rw[k]
        else: cf[i] += x
    return c0, [cf[k] for k in free]
# natural variables: a_7..a_13, P, and four L-side coefficients (among g_11..g_15) of each quartic series
nat = [(f"a{n}", A[n]) for n in range(7, 14)] + [("P", Pv)]
cand = [(f"g{tag}{11+i}", f) for tag in sorted(NATQ) for i, f in enumerate(NATQ[tag])]
chosen = []; matrows = []
for nm, f in nat + cand:
    c0, cf = subst(f)
    if len(mf7.rref(matrows + [cf])[0]) == len(matrows) + 1: chosen.append((nm, c0)); matrows.append(cf)
assert len(chosen) == len(free), (len(chosen), len(free))
nf = len(free)
aug = [list(matrows[i]) + [Fr(int(i == j)) for j in range(nf)] for i in range(nf)]
inv = [rw[nf:] for rw in mf7.rref(aug)[0]]                         # free = inv * (nat - c0nat)
c0nat = [c for _, c in chosen]
def to_nat(c0, cf):
    w = [sum(cf[i] * inv[i][k] for i in range(nf)) for k in range(nf)]
    return c0 - sum(w[k] * c0nat[k] for k in range(nf)), w
G = [to_nat(*subst(f)) for f, _ in GE]
print(f"rank {r}: {NV} variables, {len(EQ)} equalities of rank {len(red)}, {nf} free: {[n for n, _ in chosen]}; {len(GE)} inequalities, nmax {NMAX}, mode {MODE}")

# ---------- exact feasibility: is { c0 + cf . x >= 0 for all rows } non-empty?  (x free)
def simplex(cols, c, g):
    """max c.lam s.t. sum lam_i cols_i = g, lam >= 0.  ('optimal', value, lam, y) | ('unbounded', ray) | ('infeasible',)"""
    n = len(cols); k = len(g); sg = [-1 if x < 0 else 1 for x in g]
    tab = [[sg[r] * cols[i][r] for i in range(n)] + [Fr(int(r == q)) for q in range(k)] + [sg[r] * g[r]] for r in range(k)]
    basis = [n + r for r in range(k)]

    def pivot(r, j):
        q = tab[r][j]; tab[r] = [x / q for x in tab[r]]
        for i in range(k):
            if i != r and tab[i][j] != 0:
                f = tab[i][j]; row = tab[r]; tab[i] = [x - f * y for x, y in zip(tab[i], row)]
        basis[r] = j

    def run(cost, allowed):
        while True:
            cb = [cost[b] for b in basis]; ent = None
            for j in range(allowed):
                if j in basis: continue
                rc = cost[j] - sum(cb[r] * tab[r][j] for r in range(k) if cb[r] != 0 and tab[r][j] != 0)
                if rc > 0: ent = j; break
            if ent is None: return None
            best = None
            for r in range(k):
                if tab[r][ent] > 0:
                    ratio = tab[r][-1] / tab[r][ent]
                    if best is None or ratio < best[0] or (ratio == best[0] and basis[r] < basis[best[1]]): best = (ratio, r)
            if best is None: return ent
            pivot(best[1], ent)

    run([Fr(0)] * n + [Fr(-1)] * k, n + k)
    if any(basis[r] >= n and tab[r][-1] != 0 for r in range(k)): return ("infeasible",)
    for r in range(k):
        if basis[r] >= n:
            j = next((j for j in range(n) if tab[r][j] != 0), None)
            if j is not None: pivot(r, j)
    cost = list(c) + [Fr(0)] * k; ent = run(cost, n)
    if ent is not None:
        ray = [Fr(0)] * n; ray[ent] = Fr(1)
        for r in range(k):
            if basis[r] < n: ray[basis[r]] = -tab[r][ent]
        return ("unbounded", ray)
    lam = [Fr(0)] * n
    for r in range(k):
        if basis[r] < n: lam[basis[r]] = tab[r][-1]
    cb = [cost[b] for b in basis]; y = [sg[q] * sum(cb[r] * tab[r][n + q] for r in range(k)) for q in range(k)]
    return ("optimal", sum(x * z for x, z in zip(c, lam)), lam, y)


import time
t0 = time.time()
rowsG = [list(cf) for c0, cf in G]; consts = [c0 for c0, cf in G]
res = simplex(rowsG, [-c for c in consts], [Fr(0)] * nf)
if res[0] == "unbounded":
    lam = res[1]
    assert all(x >= 0 for x in lam) and all(sum(l * rw[k] for l, rw in zip(lam, rowsG) if l) == 0 for k in range(nf)) and sum(l * c for l, c in zip(lam, consts)) < 0
    cert = [(GE[i][1], lam[i]) for i in range(len(lam)) if lam[i]]
    print("EXACT: INFEASIBLE, Farkas certificate checked (%d rows): %s  [%.0f s]" % (len(cert), ", ".join(nm for nm, _ in cert), time.time() - t0))
else:
    assert res[0] == "optimal" and res[1] == 0
    print("EXACT: feasible  [%.0f s]" % (time.time() - t0))
