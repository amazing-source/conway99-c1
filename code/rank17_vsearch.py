r"""Rank-17 switch, vector level (C1, 28/09 night): for a (V, y-pair) and a class skeleton g_2..g_7 (rank17_skeleton), search
the 21 cells (a_cd, b_cd), c < d, with
  - a_cd, b_cd in K, a = (w+ + w-)/2, b = (w+ - w-)/2, w+- norm 10 in the cell class C_cd (C_1d = g_d, C_cd = g_c + g_d),
    (w+, w-) in {0, +-4} (i.e. a perp b, norms (5,5)/(7,3)/(3,7)); M1: [a_cd] has the parity pattern of c on rho(E7);
  - pairwise: (w_X, w_Y) = 4(u, v) - r_X.r_Y with (u, v) in {0, +-1}, r = (u, h) = e_c + e_d (w+) or e_c - e_d (w-);
  - stars: sum_{d > c} a_cd + sum_{d < c} b_dc = 0 for every c (exact, in K);
  - tight frame: sum (a a^T + b b^T) = 14 P_W, i.e. sum (alpha alpha^T) GK = 14 I in K coordinates (exact).
Search: stars in order 1..7; in star c the cells (c, d) are free except the last one, forced by the star equation (looked up
by its a vector); every choice filters every remaining cell's candidates by the pairwise constraints (vectorised).
Returns the first full configuration, or None, with the node count. Pass-1 tool (no certificate)."""
import itertools, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rank17_ypairs import short_vectors_chunked

CELLS = [(c, d) for c in range(1, 8) for d in range(c + 1, 8)]


def pat(c):
    return tuple([1] * 6) if c == 1 else tuple(int(k == c) for k in range(2, 8))


def build_candidates(GK, W, cls, skeleton):
    """per cell: arrays A, B (K coordinates) of oriented candidates (a, b), all sign variants"""
    g = list(skeleton)
    G2 = GK % 2

    def bf(x, y):
        xv = (x >> np.arange(15)) & 1; yv = (y >> np.arange(15)) & 1
        return int(xv @ G2 @ yv) & 1

    def cclass(c, d):
        return g[d - 2] if c == 1 else g[c - 2] ^ g[d - 2]
    gbits = np.array([(x >> np.arange(15)) & 1 for x in g], dtype=np.int64)          # 6 x 15
    cand = {}
    for (c, d) in CELLS:
        C = cclass(c, d)
        Wc = W[cls == C]
        ip = Wc @ GK @ Wc.T
        np.fill_diagonal(ip, 99)
        hi, hj = np.nonzero(np.isin(ip, (0, 4, -4)) & (np.arange(len(Wc))[:, None] < np.arange(len(Wc))[None, :]))
        As, Bs = [], []
        for Sa, Sb in (((Wc[hi] + Wc[hj]) // 2, (Wc[hi] - Wc[hj]) // 2), ((Wc[hi] - Wc[hj]) // 2, (Wc[hi] + Wc[hj]) // 2)):
            sig = ((Sa & 1) @ G2 % 2) @ gbits.T % 2                              # pattern of [a] on the g's
            ok = (sig == np.array(pat(c))).all(axis=1)
            As.append(Sa[ok]); Bs.append(Sb[ok])
        A = np.vstack(As) if As else np.zeros((0, 15), dtype=np.int64)
        Bm = np.vstack(Bs) if Bs else np.zeros((0, 15), dtype=np.int64)
        # all sign variants (a, b), (a, -b), (-a, b), (-a, -b); dedupe
        A4 = np.vstack([A, A, -A, -A]); B4 = np.vstack([Bm, -Bm, Bm, -Bm])
        key = np.hstack([A4, B4])
        _, first = np.unique(key, axis=0, return_index=True)
        cand[(c, d)] = (A4[np.sort(first)], B4[np.sort(first)])
    return cand


def r_vec(cell, sign):
    c, d = cell
    r = np.zeros(8, dtype=np.int64)
    r[c] = 1; r[d] = sign
    return r


def vsearch(GK, cand, limit=10 ** 7, want_all=False):
    GKi = np.linalg.inv(GK.astype(float))
    # allowed inner products for each pair of cells and sign combination
    allowed = {}
    for X, Y in itertools.permutations(CELLS, 2):
        for sx in (1, -1):
            for sy in (1, -1):
                s = int(r_vec(X, sx) @ r_vec(Y, sy))
                allowed[(X, Y, sx, sy)] = np.array([-4 - s, -s, 4 - s])
    AG = {X: cand[X][0] @ GK for X in CELLS}
    BG = {X: cand[X][1] @ GK for X in CELLS}
    order = []
    forced = {}
    for c in range(1, 8):
        mine = [(c, d) for d in range(c + 1, 8)]
        if mine:
            order += mine
            forced[mine[-1]] = c
    nodes = [0]
    sols = []

    def compatible(Y, idx, X, a, b):
        """indices in idx (candidates of cell Y) compatible with the chosen (a, b) of cell X"""
        if len(idx) == 0:
            return idx
        p1 = AG[Y][idx] @ a; p2 = AG[Y][idx] @ b; p3 = BG[Y][idx] @ a; p4 = BG[Y][idx] @ b
        keep = np.ones(len(idx), bool)
        for sy in (1, -1):
            for sx in (1, -1):
                val = p1 + sx * p2 + sy * p3 + sx * sy * p4                      # (a_Y + sy b_Y, a_X + sx b_X)
                keep &= np.isin(val, allowed[(Y, X, sy, sx)])
        return idx[keep]

    def star_need(c, chosen):
        """the a vector forced for the last cell of star c"""
        t = np.zeros(15, dtype=np.int64)
        for (x, y), (a, b) in chosen.items():
            if x == c:
                t += a
            elif y == c:
                t += b
        return -t

    lookup = {}
    for X in forced:
        dct = {}
        for i, a in enumerate(cand[X][0]):
            dct.setdefault(a.tobytes(), []).append(i)
        lookup[X] = dct

    def rec(k, chosen, live):
        nodes[0] += 1
        if nodes[0] > limit:
            raise TimeoutError
        if k == len(order):
            # star 7 and the tight frame
            if np.any(star_need(7, chosen)):
                return False
            S = np.zeros((15, 15), dtype=np.int64)
            for a, b in chosen.values():
                S += np.outer(a, a) + np.outer(b, b)
            if not np.array_equal(S @ GK, 14 * np.eye(15, dtype=np.int64)):
                return False
            sols.append({str(X): (a.tolist(), b.tolist()) for X, (a, b) in chosen.items()})
            return not want_all
        X = order[k]
        idx = live[X]
        if X in forced:
            need = star_need(forced[X], chosen)
            hits = lookup[X].get(need.astype(np.int64).tobytes(), [])
            idx = np.intersect1d(idx, np.array(hits, dtype=np.int64))
        for i in idx.tolist():
            a, b = cand[X][0][i], cand[X][1][i]
            chosen[X] = (a, b)
            new_live = {}
            ok = True
            for Y in order[k + 1:]:
                ni = compatible(Y, live[Y], X, a, b)
                if len(ni) == 0:
                    ok = False; break
                new_live[Y] = ni
            if ok and rec(k + 1, chosen, new_live):
                return True
            del chosen[X]
        return False
    live0 = {X: np.arange(len(cand[X][0])) for X in CELLS}
    t0 = time.time()
    r = rec(0, {}, live0)
    return (sols[0] if sols else None), nodes[0], round(time.time() - t0, 1)


def main(tag, pid, skeleton, limit=10 ** 6):
    DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'rank17')
    K = json.load(open(os.path.join(DATA, 'K_%s.json' % tag)))
    rec_ = [r for r in K['K'] if r['id'] == pid][0]
    GK = np.array(rec_['K_gram'], dtype=np.int64)
    X, nrm = short_vectors_chunked(GK.tolist(), 10)
    W = X[nrm == 10].astype(np.int64)
    cls = ((W & 1) << np.arange(15)).sum(axis=1)
    cand = build_candidates(GK, W, cls, skeleton)
    print('candidates per cell', {str(k): len(v[0]) for k, v in cand.items()}, flush=True)
    try:
        sol, nodes, secs = vsearch(GK, cand, limit=limit)
        print(json.dumps({'V': K['V'], 'pair': pid, 'skeleton': skeleton, 'found': sol is not None, 'nodes': nodes,
                          's': secs}), flush=True)
        return sol
    except TimeoutError:
        print(json.dumps({'V': K['V'], 'pair': pid, 'skeleton': skeleton, 'found': 'LIMIT', 'nodes': limit}), flush=True)


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), json.loads(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 6)
