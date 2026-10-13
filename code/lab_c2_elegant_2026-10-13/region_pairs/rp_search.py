"""Exact search for 7 pairwise orthogonal admissible h with prescribed hit patterns (numba, iterative DFS).

Instance (built by build_instance): admissible h (|(b,h)| <= 1 on all E = 11.5 and E = 13.5 classes), orthogonality bit-matrix,
hit bitsets on the s classes of E(b) = 11.5 (<= 64 of them), hit bit-planes on the S13 classes of E(b) = 13.5 (<= 128), parity bits of the
coordinates of h (for 'sum h in 2U').

Searched object (mode 'E11'):   7 pairwise orthogonal admissible h whose E=11.5 hit sets partition the s classes (h with empty hit set allowed).
Searched object (mode 'E13'):   the same, and every E=13.5 class is hit 1 or 3 times (never 2, never >= 4).
At every leaf the sum of coordinates mod 2 is checked ('sum h in 2U') and reported separately.
Branching: the uncovered E=11.5 class with the fewest candidates; every solution is visited exactly once (exact cover with disjoint sets);
once all s classes are covered the remaining h (empty hit set) are added in increasing index order.
"""
import sys, os, json, time
import numpy as np
import numba as nb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rp_task2 as T


@nb.njit(cache=False)
def popcnt(x):
    x = x - ((x >> np.uint64(1)) & np.uint64(0x5555555555555555))
    x = (x & np.uint64(0x3333333333333333)) + ((x >> np.uint64(2)) & np.uint64(0x3333333333333333))
    x = (x + (x >> np.uint64(4))) & np.uint64(0x0F0F0F0F0F0F0F0F)
    return (x * np.uint64(0x0101010101010101)) >> np.uint64(56)


@nb.njit(cache=False)
def ctz(x):
    lsb = x & (~x + np.uint64(1))
    return popcnt(lsb - np.uint64(1))


@nb.njit(cache=False)
def dfs(n, s, orthbits, hit11, hit13, W13, valid13, req3, par, capflag, oddflag, node_limit, maxsol, need):
    one = np.uint64(1)
    full = (~np.uint64(0)) if s == 64 else ((one << np.uint64(s)) - one)
    cand = np.zeros((need + 1, n), np.int32); clen = np.zeros(need + 1, np.int64)
    branch = np.zeros((need + 1, n), np.int32); blen = np.zeros(need + 1, np.int64); bptr = np.zeros(need + 1, np.int64)
    ordered = np.zeros(need + 1, np.bool_)
    cov = np.zeros(need + 1, np.uint64)
    lo = np.zeros((need + 1, W13), np.uint64); hi = np.zeros((need + 1, W13), np.uint64)
    px = np.zeros(need + 1, np.int64)
    chosen = np.zeros(need + 1, np.int32)
    cnt = np.zeros(64, np.int64)
    sols = np.zeros((maxsol, need), np.int32); nsol = 0; nsolB = 0
    leaves_cover = 0
    nodes = 0
    for i in range(n):
        cand[0, i] = i
    clen[0] = n
    depth = 0
    bptr[0] = -1
    while True:
        # ---- prepare the branch list of `depth` (done when we enter a depth; entering is flagged by bptr[depth] == -1)
        if bptr[depth] == -1:
            bptr[depth] = 0
            unc = full & ~cov[depth]
            m = clen[depth]
            if unc == np.uint64(0):
                ordered[depth] = True
                for k in range(m):
                    branch[depth, k] = cand[depth, k]
                blen[depth] = m
            else:
                ordered[depth] = False
                for j in range(s): cnt[j] = 0
                for k in range(m):
                    x = hit11[cand[depth, k]] & unc
                    while x != np.uint64(0):
                        j = ctz(x)
                        cnt[j] += 1
                        x &= x - one
                bestj = -1; bestc = 1 << 60
                for j in range(s):
                    if (unc >> np.uint64(j)) & one:
                        if cnt[j] < bestc:
                            bestc = cnt[j]; bestj = j
                bl = 0
                if bestc > 0:
                    bj = np.uint64(bestj)
                    for k in range(m):
                        if (hit11[cand[depth, k]] >> bj) & one:
                            branch[depth, bl] = cand[depth, k]; bl += 1
                blen[depth] = bl
        nodes += 1
        if nodes > node_limit:
            return nodes, nsol, nsolB, leaves_cover, sols, True
        if bptr[depth] >= blen[depth]:
            bptr[depth] = -1
            depth -= 1
            if depth < 0:
                break
            continue
        v = branch[depth, bptr[depth]]; bptr[depth] += 1
        # ---- child state
        nd = depth + 1
        cov2 = cov[depth] | hit11[v]
        okc = True
        for w in range(W13):
            h = hit13[v, w]
            carry = lo[depth, w] & h
            lo[nd, w] = lo[depth, w] ^ h
            hi[nd, w] = hi[depth, w] ^ carry
            if capflag and (hi[depth, w] & carry) != np.uint64(0):
                okc = False
        if not okc:
            continue
        chosen[depth] = v
        px2 = px[depth] ^ par[v]
        r2 = need - nd
        if r2 == 0:
            if cov2 != full:
                continue
            leaves_cover += 1
            if oddflag:
                for w in range(W13):
                    if (lo[nd, w] & valid13[w]) != valid13[w]:
                        okc = False
                if not okc:
                    continue
            for w in range(W13):
                if (lo[nd, w] & hi[nd, w] & req3[w]) != req3[w]:
                    okc = False
            if not okc:
                continue
            if nsol < maxsol:
                for k in range(need): sols[nsol, k] = chosen[k]
            nsol += 1
            if px2 == 0: nsolB += 1
            continue
        # candidates of the child
        m = clen[depth]; c2 = 0
        unc2 = full & ~cov2
        for k in range(m):
            w = cand[depth, k]
            if w == v: continue
            if ordered[depth] and w < v: continue
            if not ((orthbits[v, w >> 6] >> np.uint64(w & 63)) & one): continue
            if (hit11[w] & cov2) != np.uint64(0): continue
            if capflag:
                bad = False
                for ww in range(W13):
                    if (lo[nd, ww] & hi[nd, ww] & hit13[w, ww]) != np.uint64(0):
                        bad = True
                if bad: continue
            cand[nd, c2] = w; c2 += 1
        if c2 < r2 and unc2 == np.uint64(0):
            continue
        if unc2 != np.uint64(0) and c2 == 0:
            continue
        # every uncovered E11 class must be hit by some candidate
        if unc2 != np.uint64(0):
            u = np.uint64(0)
            for k in range(c2): u |= hit11[cand[nd, k]]
            if (unc2 & ~u) != np.uint64(0):
                continue
        if oddflag:
            dead = False
            for ww in range(W13):
                need_cols = valid13[ww] & ~lo[nd, ww]          # even count (0 or 2) so far: at least one more hit is required
                if need_cols != np.uint64(0):
                    u = np.uint64(0)
                    for k in range(c2): u |= hit13[cand[nd, k], ww]
                    if (need_cols & ~u) != np.uint64(0):
                        dead = True
            if dead: continue
        dead = False
        for ww in range(W13):
            need3 = req3[ww] & ~(lo[nd, ww] & hi[nd, ww])
            if need3 != np.uint64(0):
                u = np.uint64(0)
                for k in range(c2): u |= hit13[cand[nd, k], ww]
                if (need3 & ~u) != np.uint64(0):
                    dead = True
        if dead: continue
        clen[nd] = c2; cov[nd] = cov2; px[nd] = px2
        bptr[nd] = -1
        depth = nd
    return nodes, nsol, nsolB, leaves_cover, sols, False


def build_instance(lat, y1, y2, scanrec):
    G = lat.G
    a = lat.XG[4] @ y1; b = lat.XG[4] @ y2
    Hall = lat.X[4][(a == 0) & (b == 0)]
    nz = np.array([int(np.flatnonzero(v)[0]) for v in Hall]); sgn = Hall[np.arange(len(Hall)), nz]; H = Hall[sgn > 0]
    V11 = T.one_per_pm(lat, T.window_cosets(lat, y1, y2, 46), y1, y2)
    V13 = T.one_per_pm(lat, T.window_cosets(lat, y1, y2, 54), y1, y2)
    V15 = T.one_per_pm(lat, T.window_cosets(lat, y1, y2, 62), y1, y2)
    assert len(V11) == scanrec["s"] and len(V13) == scanrec["S13"] and len(V15) == scanrec["S15"]
    HG = H @ G
    def prods(V):
        P2 = HG @ V.T; assert (P2 % 2 == 0).all(); return P2 // 2
    P11, P13, P15 = prods(V11), prods(V13), prods(V15)
    adm = (np.abs(P11).max(axis=1) <= 1) & (np.abs(P13).max(axis=1) <= 1)
    # 'flex' E=13.5 classes: some norm-3 vector x orthogonal to y1,y2 has |(x,b)| = 3/2 (a possible u hitting b at 3/2)
    X3o = lat.X[3][(lat.XG[3] @ y1 == 0) & (lat.XG[3] @ y2 == 0)]
    flex13 = (np.abs((X3o @ G) @ V13.T) == 3).any(axis=0) if len(V13) else np.zeros(0, bool)
    return dict(H=H, V11=V11, V13=V13, V15=V15, P11=P11, P13=P13, P15=P15, adm=adm, G=G, flex13=flex13, X3o=X3o)


def pack_instance(inst):
    adm = inst["adm"]
    Ha = inst["H"][adm]; G = inst["G"]
    n = len(Ha); s = inst["P11"].shape[1]; S13 = inst["P13"].shape[1]
    assert s <= 64 and S13 <= 128
    Hf = Ha.astype(np.float64); HGf = (Ha @ G).astype(np.float64)                        # Gram entries are small integers: float64 BLAS is exact
    gram = np.rint(HGf @ Hf.T).astype(np.int64)
    assert (np.diag(gram) == 4).all()
    orth = (gram == 0); np.fill_diagonal(orth, False)
    Wn = (n + 63) // 64
    orthbits = np.zeros((n, Wn), np.uint64)
    pad = np.zeros((n, Wn * 64), np.uint8); pad[:, :n] = orth
    # little-endian bit order: bit k of word w = column 64 w + k
    pb = np.packbits(pad.reshape(n, Wn, 64)[:, :, ::-1], axis=2)             # big-endian bytes of each 64-bit word
    orthbits = pb.reshape(n, Wn, 8).view(">u8").reshape(n, Wn).astype(np.uint64)
    def bits(M):                                                             # M: n x c boolean, c <= 64 -> uint64
        c = M.shape[1]
        out = np.zeros(M.shape[0], np.uint64)
        for j in range(c): out |= (M[:, j].astype(np.uint64) << np.uint64(j))
        return out
    for w_ in range(n):                                                      # exact check of the bit matrix (every entry)
        col = ((orthbits[:, w_ >> 6] >> np.uint64(w_ & 63)) & np.uint64(1)).astype(bool)
        assert (col == orth[:, w_]).all(), 'orth bit packing error'
    h11 = bits((np.abs(inst["P11"][adm]) == 1))
    W13 = max(1, (S13 + 63) // 64)
    h13 = np.zeros((n, W13), np.uint64); valid = np.zeros(W13, np.uint64)
    M13 = (np.abs(inst["P13"][adm]) == 1)
    for w in range(W13):
        sl = M13[:, 64 * w: 64 * w + 64]
        h13[:, w] = bits(sl) if sl.shape[1] else 0
        c = min(64, S13 - 64 * w)
        valid[w] = np.uint64((1 << c) - 1) if c < 64 else np.uint64(0xFFFFFFFFFFFFFFFF)
    req3 = np.zeros(W13, np.uint64)
    nf = ~inst["flex13"]
    for w in range(W13):
        sl = nf[64 * w: 64 * w + 64]
        for j in range(len(sl)):
            if sl[j]: req3[w] |= np.uint64(1 << j)
    par = np.zeros(n, np.int64)
    for k in range(24):
        par ^= ((Ha[:, k] & 1).astype(np.int64) << k)
    return dict(n=n, s=s, orthbits=orthbits, h11=h11, h13=h13, W13=W13, valid13=valid, req3=req3, par=par, Ha=Ha, orth=orth)


MODES = {0: (False, False, False), 1: (True, True, False), 2: (True, False, False), 3: (False, True, False), 4: (True, True, True)}
# mode -> (cap at 3 hits, odd number of hits, exact 3 hits on the 'non-flex' classes) on the E=13.5 classes


def run(pk, mode, node_limit=10 ** 8, maxsol=2000, need=7):
    t0 = time.time()
    capflag, oddflag, r3flag = MODES[mode]
    nodes, nsol, nsolB, lc, sols, hit_limit = dfs(pk["n"], pk["s"], pk["orthbits"], pk["h11"], pk["h13"], pk["W13"], pk["valid13"], (pk["req3"] if r3flag else np.zeros_like(pk["req3"])), pk["par"],
                                                   capflag, oddflag, node_limit, maxsol, need)
    return dict(nodes=int(nodes), solutions=int(nsol), solutions_with_half_sum_in_U=int(nsolB), leaves_with_full_E11_cover=int(lc),
                node_limit_hit=bool(hit_limit), seconds=round(time.time() - t0, 1), sols=sols[:min(nsol, maxsol)])
