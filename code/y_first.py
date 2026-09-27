r"""Finish line (C), C1 27/09: y-FIRST frame search on an explicit envelope U.  Every condition is PROVEN necessary (notes/140).
 y:  |y|^2 = 7, |(y,beta)| <= 3/2 on every new root beta, |(y,alpha)| <= 2 on every root alpha of U.
 pair: (y1,y2) = 0, 3/2-hit sets disjoint, (alpha,y1)^2 + (alpha,y2)^2 <= 6 for every root, trap: min (y-perp)* >= 8/7.
 h:  7 pairwise orthogonal norm-4 vectors orthogonal to y1, y2 with |(h,beta)| <= 1; w(beta) = sum_c (h_c,beta)^2 in {1,3},
     w = 1 exactly on the new roots hit at 3/2 by y1, y2 or some u; w = 3 on the others (so w = 1 on hits(y1) u hits(y2)).
     RIGID case (no norm-3 vector of U has m(x) > 0, e.g. the equal-Coxeter full-rank family): w is PRESCRIBED:
     w = 1 on hits(y1) u hits(y2), w = 3 elsewhere.
     Sum h in 2U (Lemma Z); cells (norm-3 x orthogonal to y1, y2, pattern of the pair {c,d}, both signs) nonempty.
 Symmetry: y1 is W(R)-dominant (every pair is W-equivalent to one with y1 dominant).
Usage: python y_first.py <envelope.json> [--max-seconds S]
WARNING (27/09): the norm-7 enumeration of U keeps every filtered vector; on 132 it reached 7 GB. LAB PC ONLY, never the laptop,
until y1 is generated from dominant weights of level <= 2 and y2 inside y1-perp (see rigid_h.py for the h-first variant)."""
import json, math, os, sys, time
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from envelope_trap import to_int_basis, lll, gram, short_vectors, inverse_exact, hnf_rows
from envelope_pack import solve_mod2, shifted_vectors
from h_stage2 import short_vectors_fast
from h_stage import simple_roots


def stream_vectors(Gi, bound, exact, flush, chunk=200000):
    """enumerate x (up to sign) with x^T G x == exact (<= bound); call flush(np.array) on chunks."""
    n = len(Gi)
    L = np.linalg.cholesky(np.array(Gi, dtype=float))
    d = [float(L[i, i] ** 2) for i in range(n)]
    Q = [[float(L[j, i] / L[i, i]) if j > i else 0.0 for j in range(n)] for i in range(n)]
    buf, x, eps = [], [0] * n, 1e-7

    def rec(k, rem):
        s = 0.0
        Qk = Q[k]
        for j in range(k + 1, n):
            if x[j]:
                s += Qk[j] * x[j]
        c = -s
        sp = math.sqrt(max(rem, 0.0) / d[k]) + eps
        dk = d[k]
        for xi in range(math.ceil(c - sp), math.floor(c + sp) + 1):
            t = xi - c
            r2 = rem - dk * t * t
            if r2 < -eps:
                continue
            x[k] = xi
            if k == 0:
                buf.append(tuple(x))
                if len(buf) >= chunk:
                    flush(np.array(buf, dtype=np.int64)); buf.clear()
            else:
                rec(k - 1, r2)
        x[k] = 0
    rec(n - 1, float(bound) + eps)
    if buf:
        flush(np.array(buf, dtype=np.int64))


def main():
    rec_ = json.load(open(sys.argv[1]))
    ms = float(sys.argv[sys.argv.index('--max-seconds') + 1]) if '--max-seconds' in sys.argv else 1800
    t0 = time.time()
    B = lll(to_int_basis(rec_['gens']))
    Gi = [[int(v) for v in row] for row in gram(B)]
    Gz = np.array(Gi, dtype=np.int64)
    Bf = np.array([[float(v) for v in row] for row in B])
    X, nrm = short_vectors_fast(Gi, 4)
    R = X[nrm == 2].astype(float) @ Bf
    X3c = X[nrm == 3]; X3 = X3c.astype(float) @ Bf
    X4c = X[nrm == 4]; X4 = X4c.astype(float) @ Bf
    c = solve_mod2(Gi, [Gi[i][i] for i in range(24)])
    sh = shifted_vectors(Gi, c, 2)
    Sall = np.array([[x[i] + c[i] / 2.0 for i in range(24)] for x, _ in sh]) @ Bf
    keep, seen = [], set()
    for k, s in enumerate(Sall):
        key = tuple(np.round(s * 4).astype(int))
        if tuple(-v for v in key) in seen:
            continue
        seen.add(key); keep.append(k)
    S = Sall[keep]
    m3 = (np.abs(np.abs(X3 @ S.T) - 1.5) < 1e-6).sum(axis=1)
    rigid = bool(m3.max() == 0)
    print({'roots': 2 * len(R), 'new_pm': len(S), 'rigid': rigid, 'setup_s': round(time.time() - t0, 1)}, flush=True)
    # ---- y candidates
    Ys, Ycs = [], []

    def flush(A):
        A = A[np.any(A != 0, axis=1)]
        nr = np.einsum('ij,jk,ik->i', A, Gz, A)
        A = A[nr == 7]
        if not len(A):
            return
        V = A.astype(float) @ Bf
        ok = np.abs(V @ S.T).max(axis=1) <= 1.5 + 1e-9
        if len(R):
            ok &= np.abs(V @ R.T).max(axis=1) <= 2 + 1e-9
        Ys.append(V[ok]); Ycs.append(A[ok])
    stream_vectors(Gi, 7, 7, flush)
    Y = np.vstack(Ys) if Ys else np.zeros((0, 24)); Yc = np.vstack(Ycs) if Ycs else np.zeros((0, 24), dtype=np.int64)
    # up to sign
    first = np.argmax(Yc != 0, axis=1); sg = np.sign(Yc[np.arange(len(Yc)), first])
    Yc = Yc * sg[:, None]; Y = Y * sg[:, None]
    Yc, idx = np.unique(Yc, axis=0, return_index=True); Y = Y[idx]
    simple = simple_roots(R)
    if len(simple):
        D = Y @ simple.T
        dom = np.nonzero((D >= -1e-9).all(axis=1) | (D <= 1e-9).all(axis=1))[0]
    else:
        dom = np.arange(len(Y))
    hitY = np.abs(np.abs(Y @ S.T) - 1.5) < 1e-6
    YR = np.rint(Y @ R.T) if len(R) else np.zeros((len(Y), 0))
    print({'y_cands': len(Y), 'y1_dominant': len(dom), 's': round(time.time() - t0, 1)}, flush=True)
    stats = {'pairs': 0, 'pairs_trap_ok': 0, 'h_alive': 0}
    HS4 = np.rint(X4 @ S.T).astype(np.int64)
    h_ok = np.abs(HS4).max(axis=1) <= 1
    Hall, Hcall, HSall = X4[h_ok], X4c[h_ok], (HS4[h_ok] != 0)
    parall = [int(''.join(str(int(b) & 1) for b in row[::-1]), 2) for row in Hcall]
    for a in dom:
        if time.time() - t0 > ms:
            print('TIMEOUT', flush=True); break
        y1 = Y[a]
        orth = np.abs(Y @ y1) < 1e-9
        disj = ~(hitY & hitY[a]).any(axis=1)
        ok = orth & disj
        if len(R):
            ok &= ((YR ** 2 + YR[a] ** 2) <= 6).all(axis=1)
        p3a = (X3 @ y1) ** 2                                  # (v, y1)^2 for norm-3 v
        for b in np.nonzero(ok)[0]:
            stats['pairs'] += 1
            if (p3a + (X3 @ Y[b]) ** 2 > 13 + 1e-9).any():
                continue
            if not trap_ok(B, Yc[a], Yc[b], Gi):
                continue
            stats['pairs_trap_ok'] += 1
            res = h_exact(Y[a], Y[b], hitY[a] | hitY[b], rigid, Hall, Hcall, HSall, parall, X3, S, t0, ms)
            if res:
                stats['h_alive'] += 1
                print('ALIVE pair', int(a), int(b), res, flush=True)
    stats['seconds'] = round(time.time() - t0, 1)
    stats['verdict'] = 'EXCLUDED (y-first: no pair survives)' if stats['h_alive'] == 0 and stats['seconds'] < ms else 'open'
    print(json.dumps(stats), flush=True)


def trap_ok(B, a1, a2, Gi):
    """min (y-perp cap U)* >= 8/7 (exact): y-perp lattice, its dual's short vectors."""
    Gz = np.array(Gi, dtype=object)
    M = Gz @ np.array([list(a1), list(a2)], dtype=object).T
    rows = [[int(M[i, 0]), int(M[i, 1])] + [int(i == t) for t in range(24)] for i in range(24)]
    Hh = hnf_rows(rows)
    ker = [row[2:] for row in Hh if not any(row[:2])]
    Kv = [[sum(F(int(k[i])) * B[i][t] for i in range(24)) for t in range(24)] for k in ker]
    Kr = lll(Kv)
    GK = gram(Kr)
    sv = short_vectors(inverse_exact(GK), F(8, 7), strict=True)
    return len(sv) == 0


def h_exact(y1, y2, yhits, rigid, H, Hc, HS, par, X3, S, t0, ms, hittable=None, lemma_u=False):
    """DLX for 7 h orthogonal to y1, y2 with w = 1 on yhits; elsewhere w = 3 (rigid), or w in {1,3} (general), or, if a mask
    `hittable` is given (new roots hit at 3/2 by some norm-3 vector orthogonal to y1, y2), w in {1,3} on hittable roots and w = 3
    on the others (a root met once by the h is hit by exactly one odd frame vector, and a u hitting it must be such a vector)."""
    ok = (np.abs(H @ y1) < 1e-9) & (np.abs(H @ y2) < 1e-9)
    idx = np.nonzero(ok)[0]
    if len(idx) < 7:
        return None
    Hh, cov, pr = H[idx], HS[idx], [par[i] for i in idx]
    # a candidate may not cover a y-hit root twice; in the rigid case w is prescribed everywhere
    NI = S.shape[0]
    target = np.where(yhits, 1, 3) if rigid else None
    X3p = X3[(np.abs(X3 @ y1) < 1e-9) & (np.abs(X3 @ y2) < 1e-9)]
    IP3 = np.rint(X3p @ Hh.T).astype(np.int8)
    M = len(Hh)
    bits = lambda row: int.from_bytes(np.packbits(np.asarray(row, dtype=np.uint8), bitorder='little').tobytes(), 'little')  # bit i = row[i]
    item_c = [bits(cov[:, b]) for b in range(NI)]
    orth = [bits(np.abs(Hh @ Hh[i]) < 1e-9) for i in range(M)]
    parm = {}
    for i, p in enumerate(pr):
        parm[p] = parm.get(p, 0) | (1 << i)
    found = []

    def cells_ok(ch, rows=None):
        cols = IP3[:, ch].astype(np.int16) if rows is None else IP3[rows][:, ch].astype(np.int16)
        nz = cols != 0; cnt = nz.sum(axis=1)
        for a in range(len(ch)):
            for b in range(a + 1, len(ch)):
                sel = (cnt == 2) & nz[:, a] & nz[:, b] & (np.abs(cols[:, a]) == 1) & (np.abs(cols[:, b]) == 1)
                if not sel.any():
                    return False
                pr_ = cols[sel, a] * cols[sel, b]
                if not (pr_ > 0).any() or not (pr_ < 0).any():
                    return False
        return True

    # kind: 1 = exactly 1 (y-hit); 3 = exactly 3; 13 = 1 or 3
    kind = np.full(NI, 13 if (not rigid and hittable is None) else 3, dtype=np.int64)
    if hittable is not None and not rigid:
        kind[np.asarray(hittable, bool)] = 13
    kind[np.asarray(yhits, bool)] = 1
    k1, k3, k13 = kind == 1, kind == 3, kind == 13
    # Lemma U (notes/145): a 13-root left at w = 1 is hit by a u, i.e. by a norm-3 x orthogonal to y1, y2 with |(x,beta)| = 3/2 and
    # (x,h_c) in {0,+-1}, exactly two nonzero over the 7 h (on a partial choice: |.| <= 1 and at most two nonzero; monotone).
    use_u = bool(lemma_u) and not rigid
    strong = use_u and lemma_u == 2
    if use_u:
        HIT = np.abs(np.abs(X3p @ S.T) - 1.5) < 1e-6                      # x hits root b at 3/2
        hitters = {int(b): np.nonzero(HIT[:, b])[0] for b in np.nonzero(k13)[0]}
        # strong (U+): a u hits only roots that end at w = 1 and are not y-hits (packing), hence never a 1- or 3-kind root
        xstat = ~HIT[:, k1 | k3].any(axis=1) if strong else np.ones(len(X3p), bool)

    def valid_mask(ch, exact, w=None):
        m = xstat.copy()
        if ch:
            cols = IP3[:, ch]
            nz = (cols != 0).sum(axis=1)
            m &= (np.abs(cols) <= 1).all(axis=1) & ((nz == 2) if exact else (nz <= 2))
        if strong and w is not None:
            m &= ~HIT[:, (w != 1) if exact else (w >= 2)].any(axis=1)
        return m

    def rec(ch, allowed, w, parity):
        if found or time.time() - t0 > ms:
            return
        k = len(ch)
        if k == 7:
            good = np.all(w[k1] == 1) and np.all(w[k3] == 3) and np.all((w[k13] == 1) | (w[k13] == 3))
            if good and use_u:
                vm = valid_mask(ch, True, w)
                good = all(vm[hitters[int(b)]].any() for b in np.nonzero(k13 & (w == 1))[0])
                if good and strong:
                    good = cells_ok(ch, np.nonzero(vm)[0])
            if good and parity == 0:
                found.append(list(ch))
            return
        best, bc = None, None
        vm = valid_mask(ch, False, w) if use_u else None
        for b in range(NI):
            wb = w[b]
            kb = kind[b]
            if kb == 1:
                if wb >= 1:
                    continue
                need = 1
            elif kb == 3:
                if wb >= 3:
                    continue
                need = 3 - wb
            else:
                if wb == 3:
                    continue
                if use_u and wb in (0, 1) and not vm[hitters[b]].any():
                    need = 3 - wb                              # no admissible u can hit it: it must end at w = 3
                elif wb == 1:
                    continue
                else:
                    need = 1
            if need > 7 - k:
                return
            cnt = (allowed & item_c[b]).bit_count()
            if cnt < need:
                return
            if best is None or cnt < bc:
                best, bc = b, cnt
        if best is None:
            if not k13.any():
                return                                     # all targets met with k < 7: an extra h would overshoot
            cand = allowed                                 # extra h may lift some 13-items from 1 to 3 via 2
        else:
            cand = allowed & item_c[best]
        if k == 6:
            cand &= parm.get(parity, 0)
        rest = allowed
        while cand:
            low = cand & -cand; i = low.bit_length() - 1; cand ^= low
            nw = w + cov[i]
            if (nw[k1] > 1).any() or (nw > 3).any():
                rest &= ~low; continue
            chn = ch + [i]
            if len(chn) >= 2 and not cells_ok(chn, np.nonzero(valid_mask(chn, False, nw))[0] if strong else None):
                rest &= ~low; continue
            na = rest & orth[i] & ~low
            closed = (k1 & (nw >= 1)) | (nw >= 3)
            for b in np.nonzero(closed)[0]:
                na &= ~item_c[b]
            rec(chn, na, nw, parity ^ pr[i])
            rest &= ~low
            if found:
                return
    rec([], (1 << M) - 1, np.zeros(NI, dtype=np.int64), 0)
    return found[0] if found else None


if __name__ == '__main__':
    main()
