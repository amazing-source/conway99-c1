r"""Finish line (C), C1 27/09: PACKING criterion on an explicit envelope U (odd unimodular, dim 24, min >= 2).

New roots.  U0 = even part; U0*/U0 = {U0, U \ U0, S1, S2}; the two even neighbours are nb_j = U0 u S_j.  The shadow S1 u S2 =
chi0/2 + U (chi0 characteristic); its norm-2 vectors are the NEW roots (roots of nb_j outside U), r + 48 of them in all.
Lattice identity (checked here on every norm-3 vector):  m(x) := #{new beta in S_j : |(beta, x)| = 3/2} = r/8 - E(x), the same for
j = 1, 2, where E(x) = sum over positive roots alpha of U of (alpha, x)^2.
Frame constraint.  (F) at a new root beta: (u,beta), (y,beta) in 1/2 + Z and (h,beta) in Z, so
    42/4 + 2/4 + 2 #{odd frame vectors with |(.,beta)| = 3/2} + sum_h (h,beta)^2 = 14:
at most ONE of the 42 u (and 2 y) has |(.,beta)| = 3/2.  So the 3/2-sets of the u are pairwise disjoint in S_j, and
    sum_u m(u) <= #new_min := min_j |S_j roots| = 24 min(h1, h2) - r.
Tests:  (1) the 42 smallest values of m (over norm-3 vectors up to sign) must fit:  sum <= #new_min;
        (2) admissible x: m(x) + (41 smallest m among the other classes) <= #new_min;  trap on the span of the admissible vectors
            (short dual vectors, norm < 8/7, must fit in N-perp, dim 2)  -- as in envelope_trap.
Usage: pack_verdict(gens) -> dict;  python envelope_pack.py <envelope dir> <out.json> [ids...]."""
import json, os, sys, time
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from envelope_trap import to_int_basis, lll, gram, short_vectors, hnf_rows, inverse_exact


def solve_mod2(G, rhs):
    """x with G x = rhs over F2 (G invertible mod 2)."""
    n = len(G)
    A = [[int(G[i][j]) & 1 for j in range(n)] + [int(rhs[i]) & 1] for i in range(n)]
    row = 0
    piv_cols = []
    for c in range(n):
        p = next((i for i in range(row, n) if A[i][c]), None)
        if p is None:
            continue
        A[row], A[p] = A[p], A[row]
        for i in range(n):
            if i != row and A[i][c]:
                A[i] = [a ^ b for a, b in zip(A[i], A[row])]
        piv_cols.append(c)
        row += 1
    assert row == n, 'Gram not invertible mod 2'
    x = [0] * n
    for i, c in enumerate(piv_cols):
        x[c] = A[i][n]
    return x


def shifted_vectors(G, center2, bound):
    """integer x with (x + center2/2)^T G (x + center2/2) <= bound, center2 integer vector (exact check, G integer)."""
    n = len(G)
    Gf = np.array([[float(v) for v in row] for row in G])
    L = np.linalg.cholesky(Gf)
    d = np.array([L[i, i] ** 2 for i in range(n)])
    Q = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            Q[i, j] = L[j, i] / L[i, i]
    c = np.array([-v / 2.0 for v in center2])          # we enumerate y = x - c with c = -center2/2
    out, x, eps = [], [0] * n, 1e-9
    Gi = [[int(v) for v in row] for row in G]

    def rec(k, rem):
        s = sum(Q[k, j] * (x[j] - c[j]) for j in range(k + 1, n))
        mid = c[k] - s
        span_ = np.sqrt(max(rem, 0) / d[k]) + eps
        for xi in range(int(np.ceil(mid - span_)), int(np.floor(mid + span_)) + 1):
            x[k] = xi
            r2 = rem - d[k] * (xi - mid) ** 2
            if r2 < -eps:
                continue
            if k == 0:
                w = [2 * x[i] + center2[i] for i in range(n)]
                val = sum(Gi[i][j] * w[i] * w[j] for i in range(n) for j in range(n))
                if val <= 4 * bound:
                    out.append((tuple(x), F(val, 4)))
            else:
                rec(k - 1, r2)
        x[k] = 0
    rec(n - 1, float(bound) + eps)
    return out


def pack_verdict(gens, want_trap=True):
    B = lll(to_int_basis(gens))
    assert len(B) == 24
    G = gram(B)
    assert all(v.denominator == 1 for row in G for v in row), 'not integral'
    Gi = [[int(v) for v in row] for row in G]
    det = round(np.linalg.det(np.array(Gi, dtype=float)))
    Bf = np.array([[float(v) for v in row] for row in B])
    vecs = short_vectors(G, 3)
    if any(n == 1 for v, n in vecs):
        return {'error': 'norm-1 vectors present'}
    roots = np.array([v for v, n in vecs if n == 2], dtype=float).reshape(-1, 24) @ Bf
    X3c = [v for v, n in vecs if n == 3]
    X3 = np.array(X3c, dtype=float).reshape(-1, 24) @ Bf
    r = 2 * len(roots)
    # characteristic vector and the shadow's norm-2 vectors
    c = solve_mod2(Gi, [Gi[i][i] for i in range(24)])
    sh = shifted_vectors(Gi, c, 2)
    assert all(v == 2 for _, v in sh)
    S = np.array([[x[i] + c[i] / 2.0 for i in range(24)] for x, _ in sh]) @ Bf
    par = np.array([sum(Gi[i][j] * x[i] * x[j] for i in range(24) for j in range(24)) % 2 for x, _ in sh])
    n_new = (int((par == 0).sum()), int((par == 1).sum()))
    res = {'det': det, 'roots': r, 'norm3': 2 * len(X3), 'new_roots': n_new}
    assert len(S) == r + 48, (len(S), r)
    # m_j(x) and E(x), chunked
    m = np.zeros((len(X3), 2), dtype=np.int64)
    E = np.zeros(len(X3))
    for a in range(0, len(X3), 4000):
        P = X3[a:a + 4000] @ S.T
        hit = np.abs(np.abs(P) - 1.5) < 1e-6
        assert np.all((np.abs(np.abs(P) - 0.5) < 1e-6) | hit)
        m[a:a + 4000, 0] = hit[:, par == 0].sum(axis=1)
        m[a:a + 4000, 1] = hit[:, par == 1].sum(axis=1)
        if len(roots):
            E[a:a + 4000] = ((X3[a:a + 4000] @ roots.T) ** 2).sum(axis=1)
    ident_ok = bool(np.all(m[:, 0] == m[:, 1]) and np.allclose(m[:, 0], r / 8 - E))
    res['identity_m=r/8-E'] = ident_ok
    mm = np.sort(m[:, 0])
    nmin = min(n_new)
    res['m_hist'] = {int(k): int(v) for k, v in zip(*np.unique(m[:, 0], return_counts=True))}
    res['new_min'] = nmin
    low42 = int(mm[:42].sum()) if len(mm) >= 42 else None
    res['sum_42_smallest_m'] = low42
    if len(mm) < 42 or low42 > nmin:
        res['verdict'] = 'EXCLUDED (packing: 42 smallest m sum to %s > %d new roots)' % (low42, nmin)
        return res
    s41 = int(mm[:41].sum())
    s42 = int(mm[:42].sum())
    # for x: sum of the 41 smallest among the others = s41 if m(x) > mm[40] (x not among them) else s42 - m(x)
    others = np.where(m[:, 0] > mm[40], s41, s42 - m[:, 0])
    adm = m[:, 0] + others <= nmin
    res['admissible'] = 2 * int(adm.sum())
    if not want_trap:
        return res
    # CONNECTIVITY (C1 27/09): T^2 + T = 12I - C^T C with T_AB = 0 forces (C^T C)_AB = 0, i.e. the block pairs of A-orbits and
    # B-orbits are disjoint or equal; in K7 this is impossible unless A or B is empty.  So the 42 u are connected under
    # |(u,u')| = 1, hence lie in ONE component of that graph on the (packing-admissible) norm-3 vectors; N <= span(component).
    idx = np.nonzero(adm)[0]
    res['admissible'] = 2 * len(idx)
    if len(idx) < 42:
        res['verdict'] = 'EXCLUDED (fewer than 42 admissible norm-3 classes)'
        return res
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import connected_components
    Xa = X3[idx]
    Pa = Xa @ Xa.T
    adj = np.abs(np.abs(Pa) - 1.0) < 1e-6
    ncomp, lab = connected_components(csr_matrix(adj), directed=False)
    comps = []
    viable = []
    for k in range(ncomp):
        mem = idx[lab == k]
        if len(mem) < 42:
            comps.append({'size': 2 * len(mem), 'viable': False, 'why': '<42'})
            continue
        if not want_trap:
            comps.append({'size': 2 * len(mem)}); viable.append(k); continue
        rank, dim_short, nshort = trap_on([list(X3c[i]) for i in mem], B)
        ok = rank >= 22 and dim_short + (24 - rank) <= 2
        comps.append({'size': 2 * len(mem), 'rank': rank, 'dim_short': dim_short, 'short_dual': nshort, 'viable': ok})
        if ok:
            viable.append(k)
    res['components'] = comps
    if not viable:
        res['verdict'] = 'EXCLUDED (connectivity: no component of the |(x,y)| = 1 graph on admissible norm-3 vectors hosts N)'
        return res
    res['verdict'] = 'survives'
    return res


def trap_on(A, B):
    """rank of span(A) (coefficient vectors in basis B), and the short (norm < 8/7) vectors of its dual inside its span."""
    H = hnf_rows(A)
    rank = len(H)
    if rank == 0:
        return 0, 0, 0
    Areal = lll([[sum(F(a[i]) * B[i][k] for i in range(24)) for k in range(24)] for a in H])
    GA = gram(Areal)
    sv = short_vectors(inverse_exact(GA), F(8, 7), strict=True)
    dim_short = int(np.linalg.matrix_rank(np.array([v for v, n in sv], dtype=float))) if sv else 0
    return rank, dim_short, 2 * len(sv)


if __name__ == '__main__':
    envdir, outp = sys.argv[1], sys.argv[2]
    want = {int(a) for a in sys.argv[3:]}
    res = json.load(open(outp)) if os.path.exists(outp) else {}
    for fn in sorted(os.listdir(envdir)):
        if not fn.endswith('.json'):
            continue
        rec = json.load(open(os.path.join(envdir, fn)))
        if (want and rec['id'] not in want) or str(rec['id']) in res:
            continue
        t = time.time()
        try:
            v = pack_verdict(rec['gens'])
        except Exception as ex:
            v = {'error': repr(ex)}
        v['seconds'] = round(time.time() - t, 1)
        v['roots_type'] = rec['roots']
        res[str(rec['id'])] = v
        json.dump(res, open(outp + '.tmp', 'w'), indent=0)
        os.replace(outp + '.tmp', outp)
        print(rec['id'], rec['roots'], {k: v[k] for k in v if k not in ('m_hist',)}, flush=True)
