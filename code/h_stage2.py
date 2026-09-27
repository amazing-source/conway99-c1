r"""Finish line (C), C1 27/09: h-stage v2 (DLX-style, bitsets).  Proven conditions on the 7 h of a frame in U (notes/140):
  (O)    pairwise orthogonal norm-4 vectors of U;
  (H2)   |(h,beta)| <= 1 for every new root beta, and w(beta) := sum_c (h_c,beta)^2 in {1, 3} for EVERY new root;
  (Z)    sum_c h_c in 2U;
  (CELL) for every pair {c,d} and t = +-1 some norm-3 x has (x,h_c)(x,h_d) = t, both +-1, and (x,h_e) = 0 for the other e
         (monotone: checked on partial tuples).
Search: exact cover with multiplicities {1,3}: branch on the uncovered new root (w = 0) with the fewest compatible candidates,
or on a root with w = 2 (needs exactly one more).  Complete (no symmetry reduction); prints the number of full solutions.
Usage: python h_stage2.py <envelope.json> [--max-seconds S] [--max-solutions K]."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from envelope_trap import to_int_basis, lll, gram
from envelope_pack import solve_mod2, shifted_vectors


def short_vectors_fast(Gi, bound):
    """all integer x != 0 (up to sign) with x^T G x <= bound; pure-Python floats, exact integer check in numpy."""
    n = len(Gi)
    Gf = np.array(Gi, dtype=float)
    L = np.linalg.cholesky(Gf)
    d = [float(L[i, i] ** 2) for i in range(n)]
    Q = [[float(L[j, i] / L[i, i]) if j > i else 0.0 for j in range(n)] for i in range(n)]
    out = []
    x = [0] * n
    eps = 1e-7
    import math

    def rec(k, rem):
        s = 0.0
        Qk = Q[k]
        for j in range(k + 1, n):
            if x[j]:
                s += Qk[j] * x[j]
        c = -s
        sp = math.sqrt(max(rem, 0.0) / d[k]) + eps
        lo, hi = math.ceil(c - sp), math.floor(c + sp)
        dk = d[k]
        for xi in range(lo, hi + 1):
            t = xi - c
            r2 = rem - dk * t * t
            if r2 < -eps:
                continue
            x[k] = xi
            if k == 0:
                out.append(tuple(x))
            else:
                rec(k - 1, r2)
        x[k] = 0
    rec(n - 1, float(bound) + eps)
    X = np.array(out, dtype=np.int64)
    X = X[np.any(X != 0, axis=1)]
    Gz = np.array(Gi, dtype=np.int64)
    nrm = np.einsum('ij,jk,ik->i', X, Gz, X)
    keep = nrm <= bound
    X, nrm = X[keep], nrm[keep]
    # up to sign: first nonzero coordinate positive
    first = np.argmax(X != 0, axis=1)
    sgn = np.sign(X[np.arange(len(X)), first])
    X = X * sgn[:, None]
    X, idx = np.unique(X, axis=0, return_index=True)
    return X, nrm[idx]


def setup(gens):
    B = lll(to_int_basis(gens))
    G = gram(B)
    Gi = [[int(v) for v in row] for row in G]
    Bf = np.array([[float(v) for v in row] for row in B])
    X, nrm = short_vectors_fast(Gi, 4)
    R = X[nrm == 2].astype(float) @ Bf
    X3 = X[nrm == 3].astype(float) @ Bf
    X4c = X[nrm == 4]
    X4 = X4c.astype(float) @ Bf
    c = solve_mod2(Gi, [Gi[i][i] for i in range(24)])
    sh = shifted_vectors(Gi, c, 2)
    S = np.array([[x[i] + c[i] / 2.0 for i in range(24)] for x, _ in sh]) @ Bf
    keep, seen = [], set()
    for k, s in enumerate(S):
        key = tuple(np.round(s * 4).astype(int))
        if tuple(-v for v in key) in seen:
            continue
        seen.add(key); keep.append(k)
    return B, Bf, R, X3, X4c, X4, S[keep]


def run(gens, max_seconds=600, max_solutions=10 ** 6, verbose=True):
    t0 = time.time()
    B, Bf, R, X3, X4c, X4, S = setup(gens)
    HS = np.rint(X4 @ S.T).astype(np.int64)
    ok = np.abs(HS).max(axis=1) <= 1
    H, Hc, HS = X4[ok], X4c[ok], HS[ok]
    M, NI = len(H), len(S)
    cov = (HS != 0)
    par = [int(''.join(str(int(b) & 1) for b in row[::-1]), 2) for row in Hc]
    IP3 = np.rint(X3 @ H.T).astype(np.int8)
    info = {'roots': 2 * len(R), 'items(new roots/pm)': NI, 'norm3_pm': len(X3), 'norm4_pm': len(X4), 'h_cands': M,
            'setup_s': round(time.time() - t0, 1)}
    if verbose:
        print(info, flush=True)
    # bitsets
    def bits(boolrow):
        return int.from_bytes(np.packbits(boolrow[::-1].astype(np.uint8)).tobytes(), 'big')
    item_c = [bits(cov[:, b]) for b in range(NI)]                 # candidates covering item b
    orth = []
    for a in range(0, M, 2000):
        P = np.abs(H[a:a + 2000] @ H.T) < 1e-9
        orth += [bits(row) for row in P]
    ALL = (1 << M) - 1
    par_mask = {}
    for i, p_ in enumerate(par):
        par_mask[p_] = par_mask.get(p_, 0) | (1 << i)
    sols = []
    nodes = [0]
    stop = [False]

    def cells_ok(chosen):
        k = len(chosen)
        cols = IP3[:, chosen].astype(np.int16)
        nz = cols != 0
        cnt = nz.sum(axis=1)
        for a in range(k):
            for b in range(a + 1, k):
                sel = (cnt == 2) & nz[:, a] & nz[:, b] & (np.abs(cols[:, a]) == 1) & (np.abs(cols[:, b]) == 1)
                if not sel.any():
                    return False
                prod = cols[sel, a] * cols[sel, b]
                if not (prod > 0).any() or not (prod < 0).any():
                    return False
        return True

    def rec(chosen, allowed, w, parity):
        nodes[0] += 1
        if stop[0] or time.time() - t0 > max_seconds or len(sols) >= max_solutions:
            stop[0] = True
            return
        k = len(chosen)
        if k == 7:
            if parity == 0 and all(v in (1, 3) for v in w):
                sols.append(list(chosen))
            return
        # choose the most constrained item among w == 0 (must be covered) and w == 2 (needs exactly one more)
        best, bestcnt = None, None
        for b in range(NI):
            if w[b] == 0 or w[b] == 2:
                c = (allowed & item_c[b]).bit_count()
                if c == 0:
                    if w[b] == 0:
                        return                                 # cannot be covered
                    continue                                   # w == 2 may stay 2 only if ... it must not: final check fails
                if best is None or c < bestcnt:
                    best, bestcnt = b, c
        if any(v == 2 and not (allowed & item_c[b]) for b, v in enumerate(w)):
            return
        if best is None:
            best_cands = allowed                               # all items at 1 or 3: any compatible h may still be added
        else:
            best_cands = allowed & item_c[best]
        if k == 6:
            best_cands &= par_mask.get(parity, 0)          # Lemma Z: the 7th closes the sum mod 2U
        cand = best_cands
        rest = allowed
        while cand:
            low = cand & -cand
            i = low.bit_length() - 1
            cand ^= low
            nw = list(w)
            bad = False
            for b in np.nonzero(cov[i])[0]:
                nw[b] += 1
                if nw[b] > 3:
                    bad = True
                    break
            if bad:
                rest &= ~low
                continue
            ch = chosen + [i]
            if k >= 1 and not cells_ok(ch):
                rest &= ~low
                continue
            na = rest & orth[i] & ~low
            for b in range(NI):
                if nw[b] == 3:
                    na &= ~item_c[b]
            if 7 - len(ch) > 0 and na == 0:
                rest &= ~low
                continue
            rec(ch, na, nw, parity ^ par[i])
            rest &= ~low                                       # sibling branches: i excluded (it was tried)
            if stop[0]:
                return

    rec([], ALL, [0] * NI, 0)
    info.update(nodes=nodes[0], complete=not stop[0], solutions=len(sols), seconds=round(time.time() - t0, 1))
    info['verdict'] = ('EXCLUDED (no h-configuration: O + H2 + Z + CELL)' if (not sols and not stop[0])
                       else ('survives (%d h-configurations)' % len(sols) if sols else 'TIMEOUT'))
    return info, sols


if __name__ == '__main__':
    rec_ = json.load(open(sys.argv[1]))
    ms = float(sys.argv[sys.argv.index('--max-seconds') + 1]) if '--max-seconds' in sys.argv else 600
    mk = int(sys.argv[sys.argv.index('--max-solutions') + 1]) if '--max-solutions' in sys.argv else 10 ** 6
    info, sols = run(rec_['gens'], ms, mk)
    info['id'] = rec_['id']; info['roots_type'] = rec_['roots']
    print(json.dumps(info), flush=True)
