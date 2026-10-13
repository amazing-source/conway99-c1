"""Self-test of the numba DFS in rp_search.py against brute force on random synthetic instances (all 7-subsets), for both modes.
Run: <lab python> -B rp_search_selftest.py"""
import sys, os, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rp_search as RS

def make(n, s, S13, rng, p_orth, p11, p13, plant):
    orth = np.triu(rng.random((n, n)) < p_orth, 1); orth = orth | orth.T
    M11 = rng.random((n, s)) < p11
    M13 = rng.random((n, S13)) < p13
    par = rng.integers(0, 2**8, n)
    if plant:      # plant a 7-set with disjoint E11 hits covering s and E13 counts in {1,3}
        P = rng.choice(n, 7, replace=False)
        for a in P:
            for b in P:
                if a != b: orth[a, b] = True
        M11[P] = False
        owner = rng.integers(0, 7, s)
        for j in range(s): M11[P[owner[j]], j] = True
        M13[P] = False
        for j in range(S13):
            k = rng.choice([1, 3]); who = rng.choice(7, k, replace=False)
            for w in who: M13[P[w], j] = True
        par[P[6]] = 0
        x = 0
        for a in P[:6]: x ^= int(par[a])
        par[P[6]] = x
    return orth, M11, M13, par, (P if plant else None)

def pack(orth, M11, M13, par):
    n, s = M11.shape; S13 = M13.shape[1]
    global FLEX
    Wn = (n + 63) // 64
    pad = np.zeros((n, Wn * 64), np.uint8); pad[:, :n] = orth
    pb = np.packbits(pad.reshape(n, Wn, 64)[:, :, ::-1], axis=2)
    orthbits = pb.reshape(n, Wn, 8).view(">u8").reshape(n, Wn).astype(np.uint64)
    h11 = np.zeros(n, np.uint64)
    for j in range(s): h11 |= (M11[:, j].astype(np.uint64) << np.uint64(j))
    W13 = max(1, (S13 + 63) // 64)
    h13 = np.zeros((n, W13), np.uint64); valid = np.zeros(W13, np.uint64)
    for w in range(W13):
        for j in range(64 * w, min(S13, 64 * w + 64)):
            h13[:, w] |= (M13[:, j].astype(np.uint64) << np.uint64(j - 64 * w))
        c = min(64, S13 - 64 * w)
        valid[w] = np.uint64((1 << c) - 1) if c < 64 else np.uint64(0xFFFFFFFFFFFFFFFF)
    req3 = np.zeros(W13, np.uint64)
    nf = ~FLEX
    for j in range(S13):
        if nf[j]: req3[j // 64] |= np.uint64(1 << (j % 64))
    return dict(n=n, s=s, orthbits=orthbits, h11=h11, h13=h13, W13=W13, valid13=valid, req3=req3, par=par.astype(np.int64))

def brute(orth, M11, M13, par, use13):
    global FLEX
    # use13: 0 none, 1 cap<=3 and odd, 2 cap<=3 only, 3 odd only
    n, s = M11.shape
    cnt = 0; cntB = 0
    for S in itertools.combinations(range(n), 7):
        ok = True
        for a, b in itertools.combinations(S, 2):
            if not orth[a, b]: ok = False; break
        if not ok: continue
        c11 = M11[list(S)].sum(axis=0)
        if not (c11 == 1).all(): continue
        if use13:
            c13 = M13[list(S)].sum(axis=0)
            if use13 == 1 and not ((c13 == 1) | (c13 == 3)).all(): continue
            if use13 == 2 and not (c13 <= 3).all(): continue
            if use13 == 3 and not (c13 % 2 == 1).all(): continue
            if use13 == 4:
                if not ((c13 == 1) | (c13 == 3)).all(): continue
                if not (c13[~FLEX] == 3).all(): continue
        cnt += 1
        x = 0
        for a in S: x ^= int(par[a])
        if x == 0: cntB += 1
    return cnt, cntB

rng = np.random.default_rng(2026)
tot = 0
for trial in range(40):
    n = int(rng.integers(14, 22)); s = int(rng.integers(3, 8)); S13 = int(rng.integers(3, 10))
    plant = trial % 2 == 0
    orth, M11, M13, par, PL = make(n, s, S13, rng, p_orth=0.9, p11=0.25, p13=0.45, plant=plant)
    # allow empty hit sets: also zero a few rows of M11
    if trial % 3 == 0:
        for a in rng.choice(n, 3, replace=False): M11[a] = False
    FLEX = rng.random(M13.shape[1]) < 0.3
    if PL is not None: FLEX = FLEX | (M13[PL].sum(axis=0) == 1)
    pk = pack(orth, M11, M13, par)
    for use13 in (0, 1, 2, 3, 4):
        r = RS.run(pk, use13, node_limit=10**9, maxsol=10)
        b = brute(orth, M11, M13, par, use13)
        assert (r["solutions"], r["solutions_with_half_sum_in_U"]) == b, ("MISMATCH", trial, use13, r["solutions"], r["solutions_with_half_sum_in_U"], b)
        tot += b[0]
print("self-test passed on 40 random instances x 5 modes; total solutions compared:", tot)

FLEX = None
# boundary cases: s = 64 (full mask) and S13 > 64 (two bit-plane words)
for trial in range(6):
    n = 20; s = 64; S13 = 100 if trial % 2 == 0 else 70
    orth, M11, M13, par, PL = make(n, s, S13, rng, p_orth=0.9, p11=0.1, p13=0.45, plant=True)
    FLEX = rng.random(M13.shape[1]) < 0.3
    if PL is not None: FLEX = FLEX | (M13[PL].sum(axis=0) == 1)
    pk = pack(orth, M11, M13, par)
    for use13 in (0, 1, 2, 3, 4):
        r = RS.run(pk, use13, node_limit=10**9, maxsol=10)
        b = brute(orth, M11, M13, par, use13)
        assert (r["solutions"], r["solutions_with_half_sum_in_U"]) == b, ("MISMATCH boundary", trial, use13, r["solutions"], b)
        assert b[0] >= 1 if (use13 == 1 or True) else True
print("boundary self-test passed (s = 64, S13 = 100 and 70)")
