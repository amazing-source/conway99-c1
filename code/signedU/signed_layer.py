"""Signed layer for C2's orbit column model U (odd sector on top of the even one).  C1, 27/09.

For orbits Z, W (representatives u_Z = (a,+)(b,eps_Z), a < b: the GAUGE), Q_ZW = A(u_Z,u_W) + A(u_Z,s u_W) and
T_ZW = A(u_Z,u_W) - A(u_Z,s u_W).  So supp T_{Z,.} = {W : Q_ZW = 1}: T = 0 on the D-partner (Q = 2) and wherever Q = 0.
S = [[-I_7, B], [B^T, T]] satisfies S^2 + S = 12 I, i.e.
   B B^T = 12 I (automatic),  B T = 0,  T^2 + T = 12 I - B^T B,
with B_{c,Z} = sign of the label of u_Z in block c (+1 at a = min, eps_Z at b = max).
A signed column of Z is v = (q, t) in Z^84: q a column of U, t in {0,+-1}^42 with supp t = {q = 1} and (B T)_{.,Z} = 0,
i.e. sum_W B_{c,W} t[W] = 0 for every block c (per-column filter: it only involves the row of Z).
New master rows:
   ('CT', a, b), a < b :  sum_col lam_a t_a(b) - sum_col lam_b t_b(a) = 0          (T symmetric)
   ('IT', a, b), a <= b:  sum_Z sum_col lam 2 t_Z(a) t_Z(b) + t_a(b) + t_b(a) = 2 (12 [a = b] - (B^T B)_ab)
(the quadratic part is linear in lam: t(a) t(b) is a constant of the column, exactly as C2's I rows for Q).
Pricing / exact check: score = const + v.lin + v^T Y v with lin = (lin_q, lin_t), Y = diag(Y_q, Y_t): C2's solve() and
verify() work unchanged on the 84-dimensional columns.

PARITY (which of the two U-orbits of a pair is (a,+)(b,+)): swapping the two orbits of a pair is a symmetry of U only if the
model treats them symmetrically.  C2's forbid_for (fixed D, 'matched in order, WLOG') already spends that symmetry; so with
canonical parities one must impose D at the PAIR level only (forbid_pairlevel below), or branch on the parities.
Pair types 'tw' / 'mix' are asymmetric: branch on their parities (pass `parity`)."""
import sys, types, itertools
from collections import defaultdict
import numpy as np

import os
# C2's scripts/: env C2_SCRIPTS, else ./scripts (run from C2's repo root), else C1's read-only clone
C2_SCRIPTS = os.environ.get('C2_SCRIPTS') or (os.path.abspath('scripts') if os.path.isdir('scripts') else
                                              r"C:/home/researcher/Desktop/c2_experimental_ro/scripts")
if C2_SCRIPTS not in sys.path:
    sys.path.insert(0, C2_SCRIPTS)
N = 7


def gauge_B(g, parity=None):
    """B (7 x 42) in the gauge u_Z = (a,+)(b,eps_Z); default parity: first orbit of each pair eps = +1, second eps = -1."""
    B = np.zeros((N, g.n), dtype=np.int64)
    eps = {}
    for Z in range(g.n):
        a, b = sorted(g.pair[Z])
        if parity is not None:
            e = parity[Z]
        else:
            e = 1 if g.orbs_of[g.pair[Z]][0] == Z else -1
        eps[Z] = e
        B[a, Z] = 1
        B[b, Z] = e
    for R, (o1, o2) in ((R, v) for R, v in g.orbs_of.items()):
        assert eps[o1] == -eps[o2], "sister orbits must have opposite parities"
    return B


_SIGNS = {}


def _signs(k):
    if k not in _SIGNS:
        _SIGNS[k] = (1 - 2 * ((np.arange(1 << k)[:, None] >> np.arange(k)[None, :]) & 1)).astype(np.int8)
    return _SIGNS[k]


def signed_columns(Mq, B):
    """all (q, t) for the columns Mq (n x 42, int8) of one orbit; t on supp {q = 1}, B t = 0 blockwise."""
    out = []
    for q in Mq:
        supp = np.nonzero(q == 1)[0]
        S = _signs(len(supp))                                   # 2^k x k
        Bs = B[:, supp].astype(np.int64)                        # 7 x k
        ok = ~np.any((S.astype(np.int64) @ Bs.T) != 0, axis=1)
        if not ok.any():
            continue
        St = S[ok]
        blk = np.zeros((len(St), 84), dtype=np.int8)
        blk[:, :42] = q
        blk[:, 42 + supp] = St
        out.append(blk)
    return np.concatenate(out) if out else np.zeros((0, 84), dtype=np.int8)


def apply_signed_layer(g, parity=None, verbose=True):
    """turn a built OrbitModelU-like instance g (42-dim columns, rows built) into its signed version, in place."""
    assert g.cols[0].shape[1] == 42, "apply once"
    n = g.n
    B = gauge_B(g, parity)
    g.B = B
    BtB = B.T @ B
    nq = sum(len(M) for M in g.cols)
    g.cols = [signed_columns(M, B) for M in g.cols]
    g.empty_orbits_signed = [Z for Z in range(n) if len(g.cols[Z]) == 0]
    if verbose:
        print("signed layer: %d unsigned -> %d signed columns; orbits without a signed column: %s"
              % (nq, sum(len(M) for M in g.cols), g.empty_orbits_signed))
    if hasattr(g, '_colsf'):
        del g._colsf

    def add(name, kind, rhs):
        g.rows[name] = len(g.rname); g.rname.append(name); g.rkind.append(kind); g.rrhs.append(rhs)
    # CT rows where T can be nonzero on either side
    can = [set(np.nonzero((M[:, :42] == 1).any(axis=0))[0].tolist()) if len(M) else set() for M in g.cols]
    for a, b in itertools.combinations(range(n), 2):
        if b in can[a] or a in can[b]:
            add(('CT', a, b), 'eq', 0)
    for a in range(n):
        for b in range(a, n):
            add(('IT', a, b), 'eq', 2 * (12 * (a == b) - int(BtB[a, b])))
    g.ITidx = np.zeros((n, n), dtype=np.int64)
    for a in range(n):
        for b in range(a, n):
            g.ITidx[a, b] = g.ITidx[b, a] = g.rows['IT', a, b]
    g.linmapT = []
    for Z in range(n):
        ent = defaultdict(list)
        for W in range(n):
            if W == Z:
                continue
            a, b = min(Z, W), max(Z, W)
            if ('CT', a, b) in g.rows:
                ent[W].append((g.rows['CT', a, b], 1 if Z == a else -1))
            ent[W].append((g.rows['IT', a, b], 1))
        g.linmapT.append(ent)
    if hasattr(g, '_rhsv'):
        del g._rhsv
    base_score, base_entries = g.score_parts, g.entries

    def score_parts(self, y, Z):
        const, lin, Y = base_score(y, Z)
        linT = np.zeros(n, dtype=y.dtype)
        for W, lst in self.linmapT[Z].items():
            for r, c in lst:
                linT[W] += c * y[r]
        YT = np.array(y[self.ITidx], dtype=y.dtype)
        np.fill_diagonal(YT, 2 * np.diag(y[self.ITidx]))
        L = np.concatenate([np.asarray(lin, dtype=y.dtype), linT])
        Y2 = np.zeros((84, 84), dtype=y.dtype)
        Y2[:42, :42] = Y
        Y2[42:, 42:] = YT
        return const, L, Y2

    def entries(self, Z, v):
        q, t = v[:42], v[42:]
        d = defaultdict(int)
        for r, c in base_entries(Z, q):
            d[r] += c
        nz = np.nonzero(t)[0]
        for W in nz:
            for r, c in self.linmapT[Z][int(W)]:
                d[r] += c * int(t[W])
        for x in range(len(nz)):
            for w in range(x, len(nz)):
                a, b = int(nz[x]), int(nz[w])
                d[int(self.ITidx[a, b])] += 2 * int(t[a]) * int(t[b])
        return [(r, c) for r, c in d.items() if c]

    g.score_parts = types.MethodType(score_parts, g)
    g.entries = types.MethodType(entries, g)
    return g


def forbid_pairlevel(g, assign):
    """D-graph imposed at the PAIR level only: an orbit of {c,x} (one-block via c) may take as D-partner either orbit of
    {c,y}, y a D-neighbour of x at c.  (Keeps the swap symmetry of every pair, so canonical parities are WLOG.)"""
    fb = set()
    for c, edges in assign.items():
        nb = defaultdict(set)
        for (x, y) in edges:
            nb[x].add(y); nb[y].add(x)
        for x, ys in nb.items():
            for Z in g.orbs_of[frozenset((c, x))]:
                if g.otype[Z] != ('one', c):
                    continue
                for Dz in range(g.n):
                    if g.otype[Dz] == ('one', c) and c in g.pair[Dz] and g.pair[Dz] != g.pair[Z]:
                        y = next(iter(g.pair[Dz] - {c}))
                        if y not in ys:
                            fb.add((Z, Dz))
    return fb


def check_scores(g, trials=200, seed=0):
    """unit test: for random duals y and random columns, (A^T y)_col from entries() equals score_parts()."""
    rng = np.random.default_rng(seed)
    m = len(g.rname)
    bad = 0
    for _ in range(trials):
        y = rng.integers(-5, 6, size=m).astype(np.int64)
        Z = int(rng.integers(g.n))
        if not len(g.cols[Z]):
            continue
        j = int(rng.integers(len(g.cols[Z])))
        v = g.cols[Z][j]
        s1 = sum(int(y[r]) * c for r, c in g.entries(Z, v))
        const, L, Y = g.score_parts(y, Z)
        vv = v.astype(np.int64)
        s2 = int(const) + int(vv @ L) + int(vv @ Y @ vv) + int(np.asarray(g.extra_scores(y, Z, v[None, :])).sum())
        bad += (s1 != s2)
    return bad
