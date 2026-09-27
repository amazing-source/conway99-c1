r"""Finish line (C), C1 27/09: frame pipeline on an explicit envelope U  (h-stage -> y-stage), all conditions PROVEN (notes/140).
h-stage (h_stage2): 7 orthogonal norm-4 h, |(h,beta)| <= 1 on new roots, w(beta) in {1,3}, sum h in 2U, cells nonempty.
y-stage, for a given h-configuration:
  B1 = {new roots beta (up to sign) with w(beta) = 1}: exactly the roots hit at 3/2 by ONE odd frame vector (u or y).
  y in H-perp (y is orthogonal to N, which contains the h), |y|^2 = 7, |(y,beta)| <= 3/2 for every new root, hits(y) inside B1,
  (alpha,y)^2 <= 6 for every root of U (trap per root, notes/140);  pairs: y1 _|_ y2, hits disjoint,
  (alpha,y1)^2 + (alpha,y2)^2 <= 6 for every root, and B1 minus (hits(y1) u hits(y2)) must be coverable by u-hits:
  every remaining beta in B1 must be hit at 3/2 by some norm-3 x orthogonal to y1, y2 with (x,h) pattern of a cell.
  If min m(x) over norm-3 vectors is > 0 nowhere... (for lattices with no u-hits possible, B1 = hits(y1) u hits(y2) exactly).
Usage: python frame_pipeline.py <envelope.json> [--h-max K] [--max-seconds S]."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from envelope_trap import hnf_rows, lll
from h_stage2 import short_vectors_fast, setup, run as h_run


def kernel_basis(Gi, Hc):
    """integer basis (coefficient vectors) of {a in Z^24 : a G h = 0 for all rows h of Hc}."""
    M = (np.array(Gi, dtype=object) @ np.array(Hc, dtype=object).T)          # 24 x k
    k = M.shape[1]
    rows = [[int(M[i, j]) for j in range(k)] + [int(i == t) for t in range(24)] for i in range(24)]
    H = hnf_rows(rows)
    r = sum(1 for row in H if any(row[:k]))
    ker = [row[k:] for row in H if not any(row[:k])]
    # hnf_rows returns only nonzero rows; kernel rows have zero first k entries
    return ker


def y_stage(ctx, hsol, max_pairs=10 ** 6):
    Gi, Bf, R, X3, H, Hc, S, HS = ctx['Gi'], ctx['Bf'], ctx['R'], ctx['X3'], ctx['H'], ctx['Hc'], ctx['S'], ctx['HS']
    hs = [H[i] for i in hsol]
    w = (HS[hsol] != 0).sum(axis=0)
    assert np.all((w == 1) | (w == 3))
    B1 = set(np.nonzero(w == 1)[0].tolist())
    ker = kernel_basis(Gi, [Hc[i] for i in hsol])
    if len(ker) != 17:
        return {'error': 'kernel rank %d' % len(ker)}
    from fractions import Fraction as F
    Bq = ctx['Bq']
    Kv = [[sum(F(int(a[i])) * Bq[i][t] for i in range(24)) for t in range(24)] for a in ker]
    Kred = lll(Kv)
    GKred = [[int(sum(x * y for x, y in zip(u, v))) for v in Kred] for u in Kred]
    X, nrm = short_vectors_fast(GKred, 7)
    Kf = np.array([[float(v) for v in row] for row in Kred])
    Y = X[nrm == 7].astype(float) @ Kf
    info = {'B1': len(B1), 'y_norm7_in_Hperp': len(Y)}
    if len(Y) == 0:
        info['verdict'] = 'dead (no norm-7 vector in H-perp)'
        return info
    YS = Y @ S.T
    okS = np.abs(YS).max(axis=1) <= 1.5 + 1e-9
    YR = np.rint(Y @ R.T) if len(R) else np.zeros((len(Y), 0))
    okR = (np.abs(YR) <= 2).all(axis=1) if len(R) else np.ones(len(Y), bool)
    hit = np.abs(np.abs(YS) - 1.5) < 1e-6
    B1mask = np.zeros(len(S), bool); B1mask[list(B1)] = True
    okB = ~(hit & ~B1mask).any(axis=1)
    keep = np.nonzero(okS & okR & okB)[0]
    info['y_cands'] = len(keep)
    if len(keep) < 2:
        info['verdict'] = 'dead (fewer than 2 y candidates)'
        return info
    Yk, hk, Rk = Y[keep], hit[keep], YR[keep]
    G2 = Yk @ Yk.T
    pairs = 0
    good = []
    for a in range(len(Yk)):
        for b in range(a + 1, len(Yk)):
            if abs(G2[a, b]) > 1e-9:
                continue
            if (hk[a] & hk[b]).any():
                continue
            if len(R) and ((Rk[a] ** 2 + Rk[b] ** 2) > 6).any():
                continue
            pairs += 1
            good.append((int(keep[a]), int(keep[b])))
            if pairs >= max_pairs:
                break
    info['y_pairs'] = pairs
    # coverage of B1 by y-hits must leave only roots that u's can hit (m(x) > 0 vectors exist);
    # for lattices where every norm-3 x has m(x) = 0 (no u-hits), B1 must equal hits(y1) u hits(y2)
    m3 = ctx['m3']
    if m3.max() == 0:
        good = [(a, b) for a, b in good if set(np.nonzero(hit[a] | hit[b])[0].tolist()) == B1]
        info['y_pairs_exact_B1'] = len(good)
    info['verdict'] = 'dead (no y pair)' if not good else 'y pairs survive'
    info['pairs'] = good[:50]
    return info


def main():
    rec_ = json.load(open(sys.argv[1]))
    hmax = int(sys.argv[sys.argv.index('--h-max') + 1]) if '--h-max' in sys.argv else 50
    ms = float(sys.argv[sys.argv.index('--max-seconds') + 1]) if '--max-seconds' in sys.argv else 300
    t0 = time.time()
    B, Bf, R, X3, X4c, X4, S = setup(rec_['gens'])
    Gi = [[int(round(float(v))) for v in row] for row in (np.array([[float(x) for x in r] for r in B]) @ np.array([[float(x) for x in r] for r in B]).T)]
    HS = np.rint(X4 @ S.T).astype(np.int64)
    ok = np.abs(HS).max(axis=1) <= 1
    ctx = {'Bq': B, 'Gi': Gi, 'Bf': Bf, 'R': R, 'X3': X3, 'H': X4[ok], 'Hc': X4c[ok], 'S': S, 'HS': HS[ok]}
    P3 = X3 @ S.T
    ctx['m3'] = (np.abs(np.abs(P3) - 1.5) < 1e-6).sum(axis=1)
    info, sols = h_run(rec_['gens'], max_seconds=ms, max_solutions=hmax, verbose=False)
    print('h-stage:', info, flush=True)
    out = []
    for s in sols:
        yi = y_stage(ctx, s)
        out.append(yi)
        print({k: v for k, v in yi.items() if k != 'pairs'}, flush=True)
    alive = sum(1 for o in out if o.get('verdict', '').endswith('survive'))
    print('h-configurations tested %d, alive after y-stage %d, total %.1fs' % (len(out), alive, time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
