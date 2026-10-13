"""Task 2: why no seven vectors h, for region pairs.

  <lab python> -B rp_task2.py <lid> [max_pairs]       reads scan_<lid>.json (region pairs only), writes task2_<lid>.json

Definitions (all integers):
  H4   = { h in U : (h,h) = 4, (h,y1) = (h,y2) = 0 } / +-          (from the exact norm-4 shell)
  For a shadow vector b = v/2 (v = 2x + c) and h in U: (b,h) = (v G h^T)/2, an integer because (h,h) is even (checked).
  Coset b + J: (b,h) is constant on it because h is orthogonal to J.
  E11 = the s pairs +-b with E(b) = 11.5 (norm-2 shadow vectors with products {1/2, 3/2});
  E13 = the S13 pairs +-b with E(b) = 13.5 (window representatives, ties at +-7/2 identified);  E15 likewise (E(b) = 15.5, extra).
  admissible(h): |(b,h)| <= 1 for every b in E11 and E13   (the frame condition sum_c (b,h_c)^2 <= E(b) - 10.5 gives <= 1 for E = 11.5 and 13.5 and
                  <= 5, hence |.| <= 2, for E = 15.5; the E = 15.5 condition is reported separately).
  hit set of h  = { b pair in E11 : (b,h) = +-1 }.
"""
import sys, os, json, time, collections, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rp_lib import Lattice, OUT


def window_cosets(lat, y1, y2, fvalue):
    """shadow vectors v (rows 2b in coordinates) that are the window representative (p_i in {-5..7}) of a coset with 4E(b) = fvalue; both signs"""
    G = lat.G
    out = []
    for k in (2, 4):
        S = lat.S[k]
        p1 = lat.SG[k] @ y1; p2 = lat.SG[k] @ y2
        f = 28 * k - p1 * p1 - p2 * p2
        m = (f == fvalue) & (p1 >= -5) & (p1 <= 7) & (p2 >= -5) & (p2 <= 7)
        out.append(S[m])
    V = np.concatenate(out) if out else np.zeros((0, 24), np.int64)
    return V


def negate_normalized(lat, V, y1, y2):
    """window representative of the coset of -b, for each row v = 2b"""
    G = lat.G
    W = -V
    p1 = W @ G @ y1; p2 = W @ G @ y2
    W = W + 2 * (p1 == -7)[:, None] * y1[None, :] + 2 * (p2 == -7)[:, None] * y2[None, :]
    return W


def one_per_pm(lat, V, y1, y2):
    """one row for each pair {coset of b, coset of -b}"""
    if len(V) == 0: return V
    N = negate_normalized(lat, V, y1, y2)
    key = {V[i].tobytes(): i for i in range(len(V))}
    take = []
    seen = set()
    for i in range(len(V)):
        kb = V[i].tobytes()
        if kb in seen: continue
        kn = N[i].tobytes()
        assert kn in key and kn != kb, "coset of -b is not in the list / b ~ -b"
        seen.add(kb); seen.add(kn); take.append(i)
    assert 2 * len(take) == len(V)
    return V[take]


def max_cliques_bk(adj, n):
    """maximum clique size by Bron-Kerbosch with pivoting; adj[i] = bitset (python int).  Returns (size, one maximum clique)"""
    best = [0, []]
    sys.setrecursionlimit(10000)

    def bk(R, P, X):
        if P == 0 and X == 0:
            if len(R) > best[0]: best[0] = len(R); best[1] = list(R)
            return
        if len(R) + bin(P).count("1") <= best[0]: return
        # pivot: vertex of P | X with most neighbours in P
        PX = P | X; piv = None; bc = -1; t = PX
        while t:
            lsb = t & -t; u = lsb.bit_length() - 1; t ^= lsb
            c = bin(adj[u] & P).count("1")
            if c > bc: bc = c; piv = u
        cand = P & ~adj[piv]
        while cand:
            lsb = cand & -cand; v = lsb.bit_length() - 1; cand ^= lsb
            bk(R + [v], P & adj[v], X & adj[v])
            P &= ~lsb; X |= lsb
    bk([], (1 << n) - 1, 0)
    return best[0], best[1]


def partition_search(adj, hits, s, n, need=7, limit=10 ** 7):
    """exists a set of `need` pairwise orthogonal vertices (adj) whose hit sets (bitsets over the s pairs) are pairwise disjoint and cover all s?
    exact search; branches on the uncovered pair with the fewest candidate vertices.  Returns (found, nodes)."""
    full = (1 << s) - 1
    byp = [[] for _ in range(s)]
    for v in range(n):
        h = hits[v]; j = 0
        while h:
            lsb = h & -h; byp[lsb.bit_length() - 1].append(v); h ^= lsb
    nodes = [0]
    sol = []

    def rec(chosen, cover, cand):
        nodes[0] += 1
        if nodes[0] > limit: raise RuntimeError("node limit")
        if cover == full:
            return len(chosen) == need
        if len(chosen) == need: return False
        # uncovered pair with fewest candidates (candidate = still orthogonal to all chosen, disjoint from cover)
        unc = full & ~cover
        bestp = None; bestc = None; t = unc
        while t:
            lsb = t & -t; j = lsb.bit_length() - 1; t ^= lsb
            cl = [v for v in byp[j] if (cand >> v) & 1 and (hits[v] & cover) == 0]
            if bestc is None or len(cl) < len(bestc):
                bestc = cl; bestp = j
                if len(cl) == 0: return False
        for v in bestc:
            chosen.append(v)
            if rec(chosen, cover | hits[v], cand & adj[v]): sol.append(list(chosen)); return True
            chosen.pop()
        return False
    ok = rec([], 0, (1 << n) - 1)
    return ok, nodes[0], (sol[0] if sol else None)


def task2_pair(lat, y1, y2, scanrec):
    G = lat.G
    res = {}
    # ---- H4
    a = lat.XG[4] @ y1; b = lat.XG[4] @ y2
    Hall = lat.X[4][(a == 0) & (b == 0)]
    nz = np.array([int(np.flatnonzero(v)[0]) for v in Hall])
    sgn = Hall[np.arange(len(Hall)), nz]
    H = Hall[sgn > 0]
    assert 2 * len(H) == len(Hall)
    assert all(int(h @ G @ h) == 4 for h in H[:50]) and (np.einsum("ij,jk,ik->i", H, G, H) == 4).all()
    res["H4"] = int(len(H))
    # ---- shadow classes
    V11 = one_per_pm(lat, window_cosets(lat, y1, y2, 46), y1, y2)
    V13 = one_per_pm(lat, window_cosets(lat, y1, y2, 54), y1, y2)
    V15 = one_per_pm(lat, window_cosets(lat, y1, y2, 62), y1, y2)
    assert len(V11) == scanrec["s"] and len(V13) == scanrec["S13"] and len(V15) == scanrec["S15"], (len(V11), len(V13), len(V15))
    HG = H @ G

    def prods(V):
        if len(V) == 0: return np.zeros((len(H), 0), np.int64)
        P2 = HG @ V.T
        assert (P2 % 2 == 0).all(), "(b,h) not an integer"
        return P2 // 2
    P11, P13, P15 = prods(V11), prods(V13), prods(V15)
    m11 = np.abs(P11).max(axis=1) if P11.shape[1] else np.zeros(len(H), np.int64)
    m13 = np.abs(P13).max(axis=1) if P13.shape[1] else np.zeros(len(H), np.int64)
    m15 = np.abs(P15).max(axis=1) if P15.shape[1] else np.zeros(len(H), np.int64)
    adm = (m11 <= 1) & (m13 <= 1)
    res["admissible"] = int(adm.sum())
    res["fail_at_E11.5"] = int((m11 >= 2).sum())
    res["fail_only_at_E13.5"] = int(((m11 <= 1) & (m13 >= 2)).sum())
    res["max_abs_prod_hist_E11.5"] = {str(k): int((m11 == k).sum()) for k in np.unique(m11)}
    res["max_abs_prod_hist_E13.5"] = {str(k): int((m13 == k).sum()) for k in np.unique(m13)}
    res["admissible_fail_E15.5_bound_2"] = int((adm & (m15 >= 3)).sum())
    # sums of squares over E11 pairs for every h (all of H4) -- uniformity check
    ss11 = (P11 ** 2).sum(axis=1) if P11.shape[1] else np.zeros(len(H), np.int64)
    res["sumsq_E11.5_hist_all_H4"] = {str(k): int((ss11 == k).sum()) for k in np.unique(ss11)}
    res["sumsq_E11.5_hist_admissible"] = {str(k): int((ss11[adm] == k).sum()) for k in np.unique(ss11[adm])}
    Ha = H[adm]; Q11 = P11[adm]; Q13 = P13[adm]
    n = len(Ha)
    # ---- orthogonality graph
    Gram = Ha @ G @ Ha.T
    orth = (Gram == 0); np.fill_diagonal(orth, False)
    adj = []
    for i in range(n):
        bits = 0
        for j in np.flatnonzero(orth[i]): bits |= (1 << int(j))
        adj.append(bits)
    res["orth_edges"] = int(orth.sum() // 2)
    res["orth_degree_hist"] = {str(k): int((orth.sum(axis=1) == k).sum()) for k in np.unique(orth.sum(axis=1))}
    omega, clq = max_cliques_bk(adj, n) if n else (0, [])
    res["max_orthogonal_admissible_set"] = int(omega)
    res["Gram_entries_admissible_pairs"] = {str(k): int((Gram[np.triu_indices(n, 1)] == k).sum()) for k in np.unique(Gram[np.triu_indices(n, 1)])} if n > 1 else {}
    # ---- hit sets over the s pairs
    s = len(V11)
    hitm = (np.abs(Q11) == 1)
    hits = []
    for i in range(n):
        bits = 0
        for j in np.flatnonzero(hitm[i]): bits |= (1 << int(j))
        hits.append(bits)
    tsz = hitm.sum(axis=1) if n else np.zeros(0, np.int64)
    res["hit_set_size_hist_admissible"] = {str(k): int((tsz == k).sum()) for k in np.unique(tsz)}
    res["hit_set_size_min_max"] = [int(tsz.min()), int(tsz.max())] if n else None
    per_pair = hitm.sum(axis=0) if n else np.zeros(s, np.int64)
    res["hitters_per_E11_pair_hist"] = {str(k): int((per_pair == k).sum()) for k in np.unique(per_pair)}
    res["E11_pairs_no_admissible_hitter"] = int((per_pair == 0).sum()) if s else 0
    res["s"] = s; res["S13"] = int(len(V13)); res["S15"] = int(len(V15))
    # 13.5 level: number of +-1 products of an admissible h with the E13 pairs
    h13 = (np.abs(Q13) == 1).sum(axis=1) if n else np.zeros(0, np.int64)
    res["E13.5_hit_count_hist_admissible"] = {str(k): int((h13 == k).sum()) for k in np.unique(h13)}
    if omega >= 7 and s:
        ok, nodes, sol = partition_search(adj, hits, s, n)
        res["partition_into_7_exists"] = bool(ok); res["partition_nodes"] = nodes
    else:
        res["partition_into_7_exists"] = False
        res["partition_nodes"] = 0
        res["partition_reason"] = "largest orthogonal admissible set has size %d < 7" % omega
    # sizes: lower bound 7 * min hit size vs s
    if n:
        res["seven_hit_sets_total_size_range"] = [int(np.sort(tsz)[:7].sum()) if n >= 7 else None, int(np.sort(tsz)[-7:].sum()) if n >= 7 else None]
    # also record the H4 vectors that are admissible (coordinates) for later use
    res["_adm_idx"] = [int(i) for i in np.flatnonzero(adm)]
    return res, dict(H=H, Ha=Ha, V11=V11, V13=V13, P11=P11, P13=P13, adm=adm, adj=adj, hits=hits, orth=orth, clique=clq)


def main():
    lid = sys.argv[1]
    maxp = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
    t0 = time.time()
    lat = Lattice(lid)
    scan = json.load(open(os.path.join(OUT, "scan_%s.json" % lid)))
    reg = [p for p in scan["pairs"] if p["region"]][:maxp]
    out = {"lid": lid, "pairs": []}
    for p in reg:
        y1 = np.array(p["y1"], dtype=np.int64); y2 = np.array(p["y2"], dtype=np.int64)
        r, _ = task2_pair(lat, y1, y2, p)
        r.pop("_adm_idx")
        r["row"] = p["row"]; r["n11"] = p["n11"]; r["s"] = p["s"]; r["N2"] = p["N2"]
        out["pairs"].append(r)
        if len(out["pairs"]) % 50 == 0: print(lid, len(out["pairs"]), round(time.time() - t0, 1), flush=True)
    out["seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(OUT, "task2_%s.json" % lid), "w"))
    print("lid %s: %d region pairs, %.1fs" % (lid, len(out["pairs"]), out["seconds"]))


if __name__ == "__main__":
    main()
