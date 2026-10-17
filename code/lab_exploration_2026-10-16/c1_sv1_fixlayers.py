"""SV1 test, Codex-style symmetry breaking: FIX the line graph G_l (all edges inside X_l = labels touching 0 or 1),
RELAX every other pair of the four-star block S (44 labels) to [0,1], keep the exact linear count axioms, and ask
whether T_S >= 0 and U_S >= 0 are still possible (Kelley cutting planes on the SDP; LP by HiGHS).
t* < 0  => no completion of this G_l (integral or fractional) is positive: G_l is dead by positivity.
L >= 0  => a positive (possibly fractional) completion exists: the obstruction, if any, needs integrality.
usage: python sv1_fixgl.py walk <json> ...   |   python sv1_fixgl.py cache <jsonl> <max positive c=1 sides>"""
import itertools
import json
import sys

import numpy as np
from scipy.optimize import linprog

LABELS = [frozenset((a, b)) for a, b in itertools.combinations(range(14), 2) if b != a ^ 1]
S = [l for l in LABELS if l & {0, 1, 2, 3}]
n = len(S)
IDX = {l: i for i, l in enumerate(S)}
XL = [i for i, l in enumerate(S) if l & {0, 1}]
XLs = set(XL)


def k8(a, b):
    return 3 * len(a & b) + sum(1 for x in a for y in b if y == x ^ 1) - 2


K8 = np.array([[k8(a, b) for b in S] for a in S], float)
Bm = np.array([[1.0 if r in l else 0.0 for l in LABELS] for r in range(14)])
Pi = np.eye(84) - Bm.T @ np.linalg.solve(Bm @ Bm.T, Bm)
P84 = {l: i for i, l in enumerate(LABELS)}
ix = [P84[l] for l in S]
PiS = Pi[np.ix_(ix, ix)]
Z = np.array([[1.0 if r in l else 0.0 for l in S] for r in range(4)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
# orthonormal basis of the complement of the 4 star vectors
ev, V = np.linalg.eigh(Pp)
C = V[:, ev > 0.5]                       # n x 40

PAIRS = [(i, j) for i, j in itertools.combinations(range(n), 2)]
import os
FIX = os.environ.get("FIX", "gl")
Ys = set(range(n)) - XLs
def _fixed(i, j):
    gl = i in XLs and j in XLs
    att = (i in XLs) != (j in XLs)
    yy = i in Ys and j in Ys
    parts = set(FIX.split("+"))
    return (gl and "gl" in parts) or (att and "att" in parts) or (yy and "yy" in parts)
VAR = [(i, j) for i, j in PAIRS if not _fixed(i, j)]
VIX = {p: k for k, p in enumerate(VAR)}
nv = len(VAR)


def T_of(G):
    return (24 * np.eye(n) - 8 * G - K8) / 8.0


def mins(G):
    T = T_of(G)
    U = 7 * PiS - T
    a, A = np.linalg.eigh(C.T @ T @ C)
    b, Bv = np.linalg.eigh(C.T @ U @ C)
    return a, C @ A, b, C @ Bv


def axioms(Gfix):
    """exact counts for letters 0..3, upper bounds for letters 4..13; returns (A_eq, b_eq, A_ub, b_ub)."""
    Aeq, beq, Aub, bub = [], [], [], []
    for p in range(n):
        lp = S[p]
        for r in range(14):
            rhs = 2 - (r in lp) - ((r ^ 1) in lp)
            row = np.zeros(nv)
            const = 0.0
            touched = False
            for q in range(n):
                if q == p or r not in S[q]:
                    continue
                i, j = min(p, q), max(p, q)
                if (i, j) in VIX:
                    row[VIX[(i, j)]] += 1
                    touched = True
                else:
                    const += Gfix[i, j]
            if r <= 3:
                if not touched:
                    assert abs(const - rhs) < 1e-9, ("fixed part violates count", S[p], r, const, rhs)
                    continue
                Aeq.append(row)
                beq.append(rhs - const)
            else:
                if touched:
                    Aub.append(row)
                    bub.append(rhs - const)
    return np.array(Aeq), np.array(beq), np.array(Aub), np.array(bub)


def cut_row(u, which):
    """u^T M(x) u >= t  as  a.x - t >= -c  i.e.  -a.x + t <= c, M = T (which=0) or U (which=1); returns (row, rhs)."""
    # u^T T u = u^T T0 u - 2 sum_{var pairs} u_i u_j x_ij, T0 = T with variables at 0
    row = np.zeros(nv + 1)
    for k, (i, j) in enumerate(VAR):
        row[k] = 2 * u[i] * u[j] if which == 0 else -2 * u[i] * u[j]
    row[nv] = 1.0
    return row


def rect_of(l):
    a, b = sorted(l)
    return (a // 2, b // 2)


RECT = [rect_of(l) for l in S]
RLIST = sorted(set(RECT))


def gram_rows(Gfull, Gfix):
    """equalities: for every pair of the 11 rectangles, the number of edges between them equals that of Gfull."""
    rows, rhs = [], []
    for qa, qb in itertools.combinations_with_replacement(RLIST, 2):
        row = np.zeros(nv)
        const, tot, touched = 0.0, 0.0, False
        for i, j in PAIRS:
            if {RECT[i], RECT[j]} != {qa, qb} or (qa == qb and RECT[i] != qa):
                continue
            tot += Gfull[i, j]
            if (i, j) in VIX:
                row[VIX[(i, j)]] = 1
                touched = True
            else:
                const += Gfix[i, j]
        if touched:
            rows.append(row)
            rhs.append(tot - const)
    return rows, rhs


GFULL = None
CUTVEC = []


def kelley(Gfix, iters=200, verbose=False):
    Aeq, beq, Aub, bub = axioms(Gfix)
    if os.environ.get("GRAM") == "1":
        gr, gb = gram_rows(GFULL, Gfix)
        Aeq = np.vstack([Aeq] + [np.array(gr)]) if gr else Aeq
        beq = np.concatenate([beq, np.array(gb)]) if gb else beq
    G0 = Gfix.copy()                       # variables at 0
    T0 = T_of(G0)
    U0 = 7 * PiS - T0
    cuts, rhs = [], []
    CUTVEC.clear()
    Aeq_t = np.hstack([Aeq, np.zeros((len(Aeq), 1))])
    Aub_t = np.hstack([Aub, np.zeros((len(Aub), 1))]) if len(Aub) else np.zeros((0, nv + 1))
    bounds = [(0, 1)] * nv + [(-50, 2)]
    c = np.zeros(nv + 1)
    c[nv] = -1.0
    best_low = -np.inf
    tstar = None
    for it in range(iters):
        A_ub = np.vstack([Aub_t] + ([np.array(cuts)] if cuts else []))
        b_ub = np.concatenate([bub] + ([np.array(rhs)] if rhs else []))
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=Aeq_t, b_eq=beq, bounds=bounds, method="highs")
        if res.status == 2:
            return "AXIOMS_INFEASIBLE", it, None, best_low
        assert res.status == 0, res.message
        x = res.x[:nv]
        tstar = res.x[nv]
        if tstar < -1e-7:
            if os.environ.get("CERT") == "1":
                mu = -res.ineqlin.marginals[len(Aub_t):]
                YT = np.zeros((n, n)); YU = np.zeros((n, n))
                for k, w in enumerate(mu):
                    if w > 1e-9:
                        u = CUTVEC[k][1]
                        (YT if CUTVEC[k][0] == 0 else YU).__iadd__(w * np.outer(u, u))
                for nm, Y in (("T", YT), ("U", YU)):
                    d = np.diag(Y)
                    tot = d.sum()
                    if tot < 1e-12:
                        print("      cert %s: none" % nm); continue
                    order = np.argsort(-d)
                    cum = np.cumsum(d[order]) / tot
                    k90 = int(np.searchsorted(cum, 0.9)) + 1
                    rect_mass = {}
                    for i in range(n):
                        rect_mass[RECT[i]] = rect_mass.get(RECT[i], 0) + d[i] / tot
                    top = sorted(rect_mass.items(), key=lambda t: -t[1])[:6]
                    print("      cert %s: weight %.3f, 90%% of the mass on %d labels; X_l share %.2f; top rectangles %s" % (
                        nm, tot, k90, sum(d[i] for i in XL) / tot, ", ".join("%s:%.2f" % (r, m) for r, m in top)))
                    print("         top labels:", [tuple(sorted(S[i])) for i in order[:k90]])
            return "DEAD", it, tstar, best_low
        G = Gfix.copy()
        for k, (i, j) in enumerate(VAR):
            G[i, j] = G[j, i] = x[k]
        a, A, b, Bv = mins(G)
        low = min(a[0], b[0])
        best_low = max(best_low, low)
        if verbose and it % 10 == 0:
            print("   it %d  t* %.4f  lam_T %.4f  lam_U %.4f" % (it, tstar, a[0], b[0]), flush=True)
        if low > -1e-9:
            return "POSITIVE_POINT", it, tstar, best_low
        added = 0
        for which, (vals, vecs, M0) in enumerate(((a, A, T0), (b, Bv, U0))):
            for k in range(min(6, len(vals))):
                if vals[k] >= tstar - 1e-9:
                    break
                u = vecs[:, k]
                row = cut_row(u, which)
                cuts.append(row)
                CUTVEC.append((which, u.copy()))
                rhs.append(float(u @ M0 @ u))
                added += 1
        if added == 0:
            return "STALL", it, tstar, best_low
    return "OPEN", iters, tstar, best_low


def gl_components(L, EE):
    verts = [("L", a) for a in range(2, 14)] + [l for l in L if l & {0, 1}]
    pos = {v: i for i, v in enumerate(verts)}
    m = len(verts)
    adj = [[] for _ in range(m)]
    def link(a, b):
        adj[pos[a]].append(pos[b]); adj[pos[b]].append(pos[a])
    for a in range(2, 14, 2):
        link(("L", a), ("L", a + 1))
    for a in range(2, 14):
        for r in (0, 1):
            link(("L", a), frozenset((r, a)))
    X = [l for l in L if l & {0, 1}]
    for x, y in itertools.combinations(X, 2):
        if frozenset((x, y)) in EE:
            link(x, y)
    seen, c = set(), 0
    for s in range(m):
        if s in seen:
            continue
        c += 1
        st = [s]
        seen.add(s)
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w); st.append(w)
    degs = [len(a) for a in adj]
    return c, degs


def G_from(L, EE):
    G = np.zeros((n, n))
    for i, j in PAIRS:
        if frozenset((L[i], L[j])) in EE:
            G[i, j] = G[j, i] = 1
    return G


def relabel(L, EE, side):
    perm = list(range(14))
    if side == 1:
        perm[0], perm[2], perm[1], perm[3] = 2, 0, 3, 1
    f = lambda l: frozenset(perm[x] for x in l)
    return [f(l) for l in L], set(frozenset((f(a), f(b))) for a, b in EE)


def run_struct(name, L, EE):
    # L: labels in arbitrary order -> reorder to S
    G = G_from(L, EE) if [*L] == S else None
    if G is None:
        Ls = set(L)
        assert Ls == set(S)
        G = np.zeros((n, n))
        for i, j in PAIRS:
            if frozenset((S[i], S[j])) in EE:
                G[i, j] = G[j, i] = 1
    c, degs = gl_components(S, EE)
    a, _, b, _ = mins(G)
    Gfix = np.zeros((n, n))
    for i, j in PAIRS:
        if _fixed(i, j):
            Gfix[i, j] = Gfix[j, i] = G[i, j]
    global GFULL
    GFULL = G
    status, it, tstar, low = kelley(Gfix)
    print("%-34s c(l)=%d  integral lam_T %.3f lam_U %.3f  ->  %s after %d cuts-rounds (t* %s, best point %.4f)" % (
        name, c, a[0], b[0], status, it, "%.4f" % tstar if tstar is not None else "-", low), flush=True)
    return status


def main():
    mode = sys.argv[1]
    if mode == "walk":
        for fn in sys.argv[2:]:
            d = json.load(open(fn))
            lab = [frozenset(x) for x in d["labels"]]
            EE = {frozenset((lab[i], lab[j])) for i, j in d["edges"]}
            run_struct(fn.split("\\")[-1].split("/")[-1], lab, EE)
    else:
        mx = int(sys.argv[3])
        done = 0
        from collections import Counter
        tally = Counter()
        for line in open(sys.argv[2]):
            d = json.loads(line)
            if len(d["labels"]) != 44:
                continue
            S0 = [frozenset(x) for x in d["labels"]]
            E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
            for side in (0, 1):
                L, EE = relabel(S0, E0, side)
                c, degs = gl_components(L, EE)
                if c != 1 or any(x != 3 for x in degs):
                    continue
                G = np.zeros((n, n))
                for i, j in PAIRS:
                    if frozenset((S[i], S[j])) in EE:
                        G[i, j] = G[j, i] = 1
                a, _, b, _ = mins(G)
                if min(a[0], b[0]) < -1e-9:
                    continue
                tally[run_struct("%s side %d" % (d.get("src", "?")[:24], side), L, EE)] += 1
                done += 1
                if done >= mx:
                    print("control tally:", dict(tally))
                    return
        print("control tally:", dict(tally))


if __name__ == "__main__":
    main()
