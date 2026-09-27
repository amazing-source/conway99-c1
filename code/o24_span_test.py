"""O_24 pair filter (C1 27/09): for each (y1, y2) orbit representative of o24_ypairs.json, the norm-3 vectors of O_24
orthogonal to y1, y2 must span a lattice L_perp of rank 22 with [N_max : L_perp] in {1, 7}  (N = <u> <= L_perp <= N_max = y-perp,
[N_max : N] = 1 (g = 20) or 7 (g = 18)).  Also records: #norm-3 vectors in y-perp, #signed octads (norm 4) in y-perp."""
import json, sys
sys.path.insert(0, 'code')
from o24_ypairs import CODE, OCTADS, mask, pts, popcount, OMEGA
from envelope_trap import hnf_rows
import itertools


def bareiss_det(M):
    A = [row[:] for row in M]
    n = len(A)
    prev, sign = 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if sw is None:
                return 0
            A[k], A[sw] = A[sw], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def vec_E(c):
    return [(-1 if c >> i & 1 else 1) for i in range(24)]


def analyse(T1, T2, D):
    t1, t2, d = mask(T1), mask(T2), mask(D)
    a1 = [(-3 if t1 >> i & 1 else 1) for i in range(24)]
    a2 = [(-1 if d >> i & 1 else 1) * (-3 if t2 >> i & 1 else 1) for i in range(24)]
    assert sum(x * y for x, y in zip(a1, a2)) == 0
    S = []
    for c in CODE:
        E = vec_E(c)
        if sum(x * y for x, y in zip(E, a1)) == 0 and sum(x * y for x, y in zip(E, a2)) == 0:
            S.append(E)
    B = hnf_rows(S)
    rank = len(B)
    res = {'n_norm3_perp': len(S), 'rank': rank}
    if rank == 22:
        G = [[sum(x * y for x, y in zip(u, v)) for v in B] for u in B]
        det = bareiss_det(G)
        q, r = divmod(det, 8 ** 22 * 49)
        res['index_sq'] = q if r == 0 else det / (8 ** 22 * 49)
    # signed octads orthogonal to both y's (candidate h's)
    nh = 0
    for o in OCTADS:
        P = pts(o)
        for signs in itertools.product((1, -1), repeat=7):
            s = (1,) + signs
            if s.count(-1) % 2:
                continue
            if sum(s[k] * a1[P[k]] for k in range(8)) == 0 and sum(s[k] * a2[P[k]] for k in range(8)) == 0:
                nh += 2          # +-M
    res['n_h_perp'] = nh
    return res


if __name__ == '__main__':
    data = json.load(open('data/finishC/o24_ypairs.json'))
    for k, r in enumerate(data['orbits']):
        r.update(analyse(r['T1'], r['T2'], r['D']))
        print(k, r['A_is_octad'], r['D_weight'], r['n_norm3_perp'], r['rank'], r.get('index_sq'), r['n_h_perp'], flush=True)
    json.dump(data, open('data/finishC/o24_ypairs.json', 'w'), indent=1)
