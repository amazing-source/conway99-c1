r"""Finish line (C), C1 27/09: the h-stage on an explicit envelope U (all conditions PROVEN necessary, notes/140).
Searches 7-tuples of norm-4 vectors h_1..h_7 of U with
  (O)  pairwise orthogonal;
  (H2) |(h,beta)| <= 1 for every new root beta (norm-2 shadow vector), and at the end sum_c (h_c,beta)^2 in {1, 3};
  (Z)  sum_c h_c in 2U                                     (Lemma Z: (F) mod 2 + the characteristic vector sum u + sum y);
  (CELL) for every pair {c,d} and each sign t = +-1 there is a norm-3 x with (x,h_c)(x,h_d) = t, |(x,h_c)| = |(x,h_d)| = 1 and
         (x,h_e) = 0 for the other e  (the two orbits of the pair {c,d} have C_co C_do = +1 and -1; (u_o,h_c) = -C_co).
  The cells are monotone in partial configurations (a partial tuple with an empty cell cannot be completed).
Symmetry: the Weyl group W(R(U)) is in Aut(U) and preserves the new roots; the first h is taken among the W-dominant candidates
(every tuple is W-equivalent to one containing a dominant vector).  Blocks are unlabelled: the tuple is built as an increasing
sequence after the first element (the first is the dominant one; the others are all candidates, increasing index).
Usage: python h_stage.py <envelope.json> [--max-seconds S]."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from envelope_trap import to_int_basis, lll, gram, short_vectors
from envelope_pack import solve_mod2, shifted_vectors


def setup(gens):
    B = lll(to_int_basis(gens))
    G = gram(B)
    Gi = [[int(v) for v in row] for row in G]
    Bf = np.array([[float(v) for v in row] for row in B])
    vecs = short_vectors(G, 4)
    coef = {n: [v for v, m in vecs if m == n] for n in (2, 3, 4)}
    R = np.array(coef[2], dtype=float).reshape(-1, 24) @ Bf
    X3 = np.array(coef[3], dtype=float).reshape(-1, 24) @ Bf
    X4c = np.array(coef[4], dtype=np.int64).reshape(-1, 24)
    X4 = X4c.astype(float) @ Bf
    c = solve_mod2(Gi, [Gi[i][i] for i in range(24)])
    sh = shifted_vectors(Gi, c, 2)
    S = np.array([[x[i] + c[i] / 2.0 for i in range(24)] for x, _ in sh]) @ Bf
    # new roots up to sign
    keep, seen = [], set()
    for k, s in enumerate(S):
        key = tuple(np.round(s * 4).astype(int))
        neg = tuple(-v for v in key)
        if neg in seen:
            continue
        seen.add(key); keep.append(k)
    S = S[keep]
    return B, Bf, R, X3, X4c, X4, S


def dominant(v, simple):
    v = v.copy()
    for _ in range(10000):
        ips = simple @ v
        k = np.argmin(ips)
        if ips[k] >= -1e-9:
            return v
        v = v - ips[k] * simple[k]          # roots have norm 2: s_a(v) = v - (v,a) a
    raise RuntimeError('dominant: no convergence')


def simple_roots(R):
    if len(R) == 0:
        return np.zeros((0, 24))
    g = np.random.RandomState(7).randn(24)
    P = np.array([a if a @ g > 0 else -a for a in R])
    keys = {tuple(np.round(p * 2).astype(int)) for p in P}
    simple = []
    for p in P:
        dec = False
        for q in P:
            d = p - q
            if tuple(np.round(d * 2).astype(int)) in keys:
                dec = True
                break
        if not dec:
            simple.append(p)
    return np.array(simple)


def h_stage(gens, max_seconds=600, verbose=True):
    t0 = time.time()
    B, Bf, R, X3, X4c, X4, S = setup(gens)
    HS = np.rint(X4 @ S.T).astype(np.int64)
    ok = np.abs(HS).max(axis=1) <= 1 if len(S) else np.ones(len(X4), bool)
    H = X4[ok]; Hc = X4c[ok]; HS = HS[ok]
    HS2 = (HS != 0).astype(np.int8)
    M = len(H)
    parity = np.array([int(''.join(str(int(b) & 1) for b in row[::-1]), 2) for row in Hc], dtype=object)
    IP3 = np.rint(X3 @ H.T).astype(np.int8)                     # (x, h)
    simple = simple_roots(R)
    if len(simple):
        D = H @ simple.T
        first = [i for i in range(M) if (D[i] >= -1e-9).all() or (D[i] <= 1e-9).all()]
    else:
        first = list(range(M))
    info = {'roots': 2 * len(R), 'new_roots_pm': len(S), 'norm3_pm': len(X3), 'norm4_pm': len(X4), 'h_cands': M,
            'first_cands': len(first), 'setup_s': round(time.time() - t0, 1)}
    if verbose:
        print(info, flush=True)
    HH = None
    if M <= 20000:
        HH = np.rint(H @ H.T).astype(np.int8)
    nx3 = len(X3)
    found = []
    nodes = [0]
    stop = [False]

    def orth_mask(i, cand):
        if HH is not None:
            return cand[HH[i, cand] == 0]
        return cand[np.abs(H[cand] @ H[i]) < 1e-9]

    def cells_ok(chosen):
        k = len(chosen)
        if k < 2:
            return True
        cols = IP3[:, chosen].astype(np.int16)                  # nx3 x k
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

    def rec(chosen, cand, cover, par):
        nodes[0] += 1
        if time.time() - t0 > max_seconds:
            stop[0] = True
            return
        k = len(chosen)
        if k == 7:
            if par == 0 and np.all((cover == 1) | (cover == 3)):
                found.append(list(chosen))
            return
        # (H2) bound: every uncovered new root needs one of the remaining 7-k vectors
        if (cover == 0).any():
            z = np.nonzero(cover == 0)[0]
            if k > 0 and len(z) > (7 - k) * HS2[cand].sum(axis=1).max(initial=0):
                return
        if k == 6:
            # Lemma Z: the 7th is fixed mod 2U
            need = par
            cand = np.array([i for i in cand if parity[i] == need], dtype=np.int64)
        for i in cand:
            if stop[0]:
                return
            nc = cover + HS2[i]
            if (nc > 3).any():
                continue
            ch = chosen + [int(i)]
            if not cells_ok(ch):
                continue
            rest = orth_mask(i, cand[cand > i]) if k >= 1 else orth_mask(i, np.arange(M, dtype=np.int64)[np.arange(M) != i])
            if k == 0:
                rest = rest                                     # after the dominant first vector, any others (increasing index)
            rec(ch, rest, nc, par ^ parity[i])

    cover0 = np.zeros(len(S), dtype=np.int64)
    for i in first:
        if stop[0]:
            break
        rest = orth_mask(i, np.arange(M, dtype=np.int64))
        rest = rest[rest != i]
        rec([int(i)], rest, cover0 + HS2[i], parity[i])
    info.update(nodes=nodes[0], complete=not stop[0], found=len(found), seconds=round(time.time() - t0, 1))
    info['verdict'] = ('EXCLUDED (no h-configuration: O + H2 + Z + CELL)' if (not found and not stop[0])
                       else ('survives (h-configurations found)' if found else 'TIMEOUT'))
    return info, found


if __name__ == '__main__':
    rec_ = json.load(open(sys.argv[1]))
    ms = 600
    if '--max-seconds' in sys.argv:
        ms = float(sys.argv[sys.argv.index('--max-seconds') + 1])
    info, found = h_stage(rec_['gens'], max_seconds=ms)
    info['id'] = rec_['id']; info['roots_type'] = rec_['roots']
    print(json.dumps(info), flush=True)
