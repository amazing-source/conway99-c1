r"""Finish line (C), C1 27/09: enumeration of the (y1, y2) pairs of a frame in an explicit envelope U, up to W(R).  Exact filters,
all PROVEN (notes/140-141, trap in energy form, structures 27/09):
  roots:     |(alpha,y)| <= 2 and (alpha,y1)^2 + (alpha,y2)^2 in {0,1,2,4,5};
  new roots (chi8/2): |(beta,y)| <= 3/2 and never both 3/2  (disjoint 3/2-hits);
  norm 3:    |(v,y)| <= 3 and never both 3;
  pair:      (y1,y2) = 0 and the exact trap  min (y-perp cap U)* >= 8/7.
y1 is W(R)-dominant: Dynkin labels c_j = (y,alpha_j) in {0,1,2} with level sum_j m_j c_j <= 2 per component (m = marks of theta).
For fixed labels c the vectors y of U form a coset y_c + L_perp (L_perp = U cap span(R)-perp); c is realisable iff c H^-1 is
integral (row HNF V M = [H; 0], M_ij = (b_i, alpha_j)).  DP over components on (class of c mod the row lattice of H, norm).
y2: streaming Fincke-Pohst in the 23-dim lattice y1-perp cap U with the filters, kept only if W(R cap y1-perp)-dominant.
Usage: python y_pairs.py <envelope.json> <out.json> [--y1-only] [--max-seconds S]   (lab PC for y2 on big lattices)."""
import itertools, json, math, os, sys, time
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from envelope_trap import to_int_basis, lll, gram, hnf_rows, inverse_exact, short_vectors
from envelope_pack import solve_mod2, shifted_vectors
from h_stage2 import short_vectors_fast


def root_system(R):
    """R: array of roots up to sign (float, norm 2). Returns simple roots (list of arrays), components (lists of indices into
    simple), marks per component, Cartan matrices."""
    g = np.random.RandomState(5).randn(R.shape[1])
    P = np.array([a if a @ g > 0 else -a for a in R])
    keys = {tuple(np.round(p * 4).astype(int)) for p in P}
    simple = []
    for p in P:
        if not any(tuple(np.round((p - q) * 4).astype(int)) in keys for q in P):
            simple.append(p)
    S = np.array(simple)
    n = len(S)
    A = np.rint(S @ S.T).astype(int)
    # components of the Dynkin diagram
    comp, seen = [], set()
    for i in range(n):
        if i in seen:
            continue
        stack, cur = [i], []
        seen.add(i)
        while stack:
            a = stack.pop(); cur.append(a)
            for b in range(n):
                if b not in seen and A[a, b] != 0:
                    seen.add(b); stack.append(b)
        comp.append(sorted(cur))
    # highest root per component: positive root of maximal height, coefficients by solving
    marks = []
    Sinv = np.linalg.pinv(S.T)
    for cmp in comp:
        best, bh = None, -1
        for p in P:
            coef = np.linalg.lstsq(S[cmp].T, p, rcond=None)[0]
            if np.allclose(S[cmp].T @ coef, p, atol=1e-6):
                h = coef.sum()
                if h > bh + 1e-9:
                    best, bh = np.rint(coef).astype(int), h
        marks.append(best)
    return S, comp, marks, A, P


def level2_labels(mk):
    n = len(mk)
    out = [tuple([0] * n)]
    for j in range(n):
        for c in (1, 2):
            if mk[j] * c <= 2:
                v = [0] * n; v[j] = c; out.append(tuple(v))
    for j, k in itertools.combinations(range(n), 2):
        if mk[j] + mk[k] <= 2:
            v = [0] * n; v[j] = 1; v[k] = 1; out.append(tuple(v))
    return out


def setup(gens):
    B = lll(to_int_basis(gens))
    Gi = [[int(v) for v in row] for row in gram(B)]
    Bf = np.array([[float(v) for v in row] for row in B])
    X, nrm = short_vectors_fast(Gi, 3)
    R = X[nrm == 2].astype(float) @ Bf
    X3 = X[nrm == 3].astype(float) @ Bf
    c = solve_mod2(Gi, [Gi[i][i] for i in range(24)])
    sh = shifted_vectors(Gi, c, 2)
    Snew = np.array([[x[i] + c[i] / 2.0 for i in range(24)] for x, _ in sh]) @ Bf
    return B, Gi, Bf, R, X3, Snew


def dominant_y1(B, Gi, Bf, R, X3, Snew, verbose=True):
    """all W(R)-dominant y (up to nothing: dominance fixes the W-orbit representative) of norm 7 passing the single-y filters."""
    Sroots, comp, marks, A, P = root_system(R)
    rank = len(Sroots)
    Binv = np.linalg.inv(Bf)
    # M_ij = (b_i, alpha_j) integer
    M = np.rint(Bf @ Sroots.T).astype(np.int64)                    # 24 x rank
    # row HNF of [M | I] to get V with V M = [H; 0]
    rows = [[int(M[i, j]) for j in range(rank)] + [int(i == t) for t in range(24)] for i in range(24)]
    Hh = hnf_rows(rows)
    Hm = [row[:rank] for row in Hh[:rank]]
    V = [row[rank:] for row in Hh]
    Vk = [row[rank:] for row in Hh[rank:]]                          # kernel rows (coefficients of L_perp)
    Hinv = inverse_exact(Hm) if rank else []
    # per-component label options with norms (A^-1 of the component)
    opts = []
    for cmp, mk in zip(comp, marks):
        Ac = A[np.ix_(cmp, cmp)]
        Ainv = inverse_exact([[int(x) for x in row] for row in Ac])
        lst = []
        for lab in level2_labels(list(mk)):
            nrm = sum(F(lab[a]) * Ainv[a][b] * lab[b] for a in range(len(cmp)) for b in range(len(cmp)))
            if nrm <= 7:
                lst.append((lab, nrm))
        opts.append(lst)
    # DP over components with integer-encoded classes: class(c) = (c Hinv) mod 1, scaled by the exponent e
    e = 1
    for row in Hinv:
        for x in row:
            e = e * x.denominator // math.gcd(e, x.denominator)
    HinvE = [[int(x * e) for x in row] for row in Hinv]
    def cls_of(cmp, lab):
        v = [0] * rank
        for a, j in enumerate(cmp):
            if lab[a]:
                for k in range(rank):
                    v[k] += lab[a] * HinvE[j][k]
        return tuple(x % e for x in v)
    pre = [[(lab, nrm, cls_of(cmp, lab)) for lab, nrm in lst] for cmp, lst in zip(comp, opts)]
    add = lambda c1, c2: tuple((x + y) % e for x, y in zip(c1, c2))
    zero = tuple([0] * rank)
    Fs = [{(zero, F(0))}]
    for k in range(len(comp)):
        nxt = set()
        for (cl, nr) in Fs[-1]:
            for lab, nrm, lc in pre[k]:
                t = nr + nrm
                if t <= 7:
                    nxt.add((add(cl, lc), t))
        Fs.append(nxt)
    good = [{s for s in Fs[-1] if s[0] == zero}]
    for k in range(len(comp) - 1, -1, -1):
        nxt = good[0]
        cur = set()
        for (cl, nr) in Fs[k]:
            for lab, nrm, lc in pre[k]:
                if (add(cl, lc), nr + nrm) in nxt:
                    cur.add((cl, nr)); break
        good.insert(0, cur)
    Fs = None
    cands = []
    K = np.array(Vk, dtype=np.int64) if len(Vk) else None
    if K is not None:
        GK = K @ np.array(Gi, dtype=np.int64) @ K.T
        Kf = K.astype(float) @ Bf
        GKf = GK.astype(float)
    counter = [0]

    def emit(partial, nr):
        counter[0] += 1
        cvec = [0] * rank
        for cmp, lab in zip(comp, partial):
            for a, j in enumerate(cmp):
                cvec[j] = lab[a]
        b1 = [sum(F(cvec[j]) * Hinv[j][k] for j in range(rank)) for k in range(rank)]
        a0 = [sum(int(b1[k]) * V[k][t] for k in range(rank)) for t in range(24)]
        y0 = np.array(a0, dtype=float) @ Bf
        if K is None:
            if nr == 7:
                cands.append(np.array(a0, dtype=np.int64))
            return
        t = np.linalg.solve(GKf, Kf @ y0)
        for x in enum_shift(GK.tolist(), -t, 7 - float(y0 @ y0) + float(t @ GKf @ t), y0, Kf):
            cands.append(np.array(a0, dtype=np.int64) + np.array(x, dtype=np.int64) @ K)

    def walk(k, cl, nr, partial):
        if k == len(comp):
            emit(partial, nr)
            return
        for lab, nrm, lc in pre[k]:
            t = nr + nrm
            if t > 7:
                continue
            c2 = add(cl, lc)
            if (c2, t) in good[k + 1]:
                walk(k + 1, c2, t, partial + (lab,))
    walk(0, zero, F(0), ())
    Y = np.array(cands, dtype=np.int64).reshape(-1, 24)
    if len(Y) == 0:
        return Y, np.zeros((0, 24)), {'rank': rank, 'components': len(comp), 'dominant_y1': 0}
    Yf = Y.astype(float) @ Bf
    keep = np.abs(np.einsum('ij,ij->i', Yf, Yf) - 7) < 1e-6
    keep &= np.abs(Yf @ Snew.T).max(axis=1) <= 1.5 + 1e-9 if len(Snew) else keep
    keep &= np.abs(Yf @ X3.T).max(axis=1) <= 3 + 1e-9
    if len(R):
        keep &= np.abs(Yf @ R.T).max(axis=1) <= 2 + 1e-9
    Y, Yf = Y[keep], Yf[keep]
    info = {'rank': rank, 'components': len(comp), 'label_vectors': counter[0], 'dominant_y1': len(Y)}
    return Y, Yf, info


def enum_shift(GK, center, bound, y0, Kf):
    """integer x with |y0 + x K|^2 == 7 (bound = 7 - |y0|^2 + ... in the shifted form); small dimension."""
    n = len(GK)
    L = np.linalg.cholesky(np.array(GK, dtype=float))
    d = [float(L[i, i] ** 2) for i in range(n)]
    Q = [[float(L[j, i] / L[i, i]) if j > i else 0.0 for j in range(n)] for i in range(n)]
    out, x, eps = [], [0] * n, 1e-7

    def rec(k, rem):
        s = sum(Q[k][j] * (x[j] - center[j]) for j in range(k + 1, n))
        mid = center[k] - s
        sp = math.sqrt(max(rem, 0.0) / d[k]) + eps
        for xi in range(math.ceil(mid - sp), math.floor(mid + sp) + 1):
            r2 = rem - d[k] * (xi - mid) ** 2
            if r2 < -eps:
                continue
            x[k] = xi
            if k == 0:
                v = y0 + np.array(x, dtype=float) @ Kf
                if abs(v @ v - 7) < 1e-6:
                    out.append(list(x))
            else:
                rec(k - 1, r2)
        x[k] = 0
    if bound < -1e-9:
        return []
    rec(n - 1, bound + eps)
    return out


def main():
    rec_ = json.load(open(sys.argv[1]))
    outp = sys.argv[2]
    ms = float(sys.argv[sys.argv.index('--max-seconds') + 1]) if '--max-seconds' in sys.argv else 1800
    t0 = time.time()
    B, Gi, Bf, R, X3, Snew = setup(rec_['gens'])
    Y, Yf, info = dominant_y1(B, Gi, Bf, R, X3, Snew)
    info.update(id=rec_['id'], roots=rec_['roots'], nroots=2 * len(R), y1_seconds=round(time.time() - t0, 1))
    print(json.dumps(info), flush=True)
    res = {'id': rec_['id'], 'coords': 'integer coefficients in the basis LLL(HNF(gens)) of y_pairs.setup', 'info': info,
           'y1_dominant': [[int(v) for v in row] for row in Y], 'pairs': []}
    if '--y1-only' not in sys.argv and len(Y):
        from y2_engine import Y2Engine
        eng = Y2Engine(B, Gi, Bf, R, X3, Snew)
        tot = {'raw': 0, 'after_newroots': 0, 'after_norm3': 0, 'after_roots': 0, 'truncated_y1': 0}
        for k in range(len(Y)):
            if time.time() - t0 > ms:
                info['timeout_at_y1'] = k
                break
            Y2, st = eng.pairs_for(Yf[k], t0=t0, max_seconds=ms)
            for key in ('raw', 'after_newroots', 'after_norm3', 'after_roots'):
                tot[key] += st.get(key, 0)
            tot['truncated_y1'] += int(st.get('truncated', False))
            for y2 in Y2:
                res['pairs'].append([[int(v) for v in Y[k]], [int(v) for v in y2]])
        info['y2'] = tot
        info['pairs'] = len(res['pairs'])
        info['seconds'] = round(time.time() - t0, 1)
        info['complete'] = ('timeout_at_y1' not in info) and tot['truncated_y1'] == 0
        info['note'] = ('filters: roots |a.y|<=2, (a.y1)^2+(a.y2)^2<=6; new roots |b.y|<=3/2, never both 3/2; norm 3 |v.y|<=3, '
                        'never both 3. The exact trap min(y-perp)* >= 8/7 is EQUIVALENT to the root + norm-3 filters (a short '
                        'dual vector lifts to v in U with |v|^2 < 26/7).  y1 W(R)-dominant, y2 W(R cap y1-perp)-dominant.')
        print(json.dumps(info), flush=True)
    # exact Q^24 coordinates (as in U/NNN.json) for structures' frame_lp
    def q24(a):
        return [str(sum(F(int(a[i])) * B[i][k] for i in range(24))) for k in range(24)]
    res['pairs'] = [[q24(p1), q24(p2)] for p1, p2 in res['pairs']]
    res['stats'] = info
    json.dump(res, open(outp, 'w'))


if __name__ == '__main__':
    main()
