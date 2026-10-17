"""Reconstruction with a Hoffman-coclique boundary (srg(v,k,1,2) with alpha = Hoffman bound).
Boundary S = coclique C (|C| = c), every outside vertex w has exactly t neighbours in C: block B_w (a 2-(c,t,2) design).
Unknown: the graph D on F = V minus C.  For a row w the exact conditions coming from S are
   |N(w) & F_s| = 1 if s in B_w, 2 otherwise          (F_s = outside vertices whose block contains s)
together with |N(w)| = k - t, and every neighbour u of w has |B_u & B_w| <= 1, and two neighbours u, u' of w have
|B_u & B_u'| <= 1 (else u, u' would have 3 common neighbours).  These are the per-row conditions of the dossier's
fixed-boundary model, written for this boundary.  The pair conditions are checked later.
Row domain = all sets of k - t outside blocks covering s once (s in B_w) or twice (s not in B_w).
  python3 rowdomains.py GRAPH COCLIQUE.npy [rows...]   -> counts (and saves domains) for the given rows"""
import sys, numpy as np, pickle, time

def blocks_from(G, C):
    n = len(G); Cs = set(C); F = [w for w in range(n) if w not in Cs]
    cidx = {s: i for i, s in enumerate(C)}
    B = [sum(1 << cidx[s] for s in C if G[w, s]) for w in F]
    return F, B

def domain(wi, B, need_deg, cap=None):
    c = max(b.bit_length() for b in B)
    Bw = B[wi]
    need = [1 if (Bw >> s) & 1 else 2 for s in range(c)]
    cand = [u for u in range(len(B)) if u != wi and bin(B[u] & Bw).count("1") <= 1]
    sols = []
    def rec(chosen, cands, need, deg):
        if deg == 0:
            if all(x == 0 for x in need): sols.append(tuple(chosen))
            return
        # choose the point with the fewest candidates relative to its need
        best, bs = None, None
        for s in range(c):
            if need[s] > 0:
                cs = [u for u in cands if (B[u] >> s) & 1]
                if len(cs) < need[s]: return
                if best is None or len(cs) < len(bs): best, bs = s, cs
        if best is None: return
        r = need[best]
        import itertools
        for combo in itertools.combinations(bs, r):
            ok = all(bin(B[a] & B[b]).count("1") <= 1 for a, b in itertools.combinations(combo, 2)) and \
                 all(bin(B[a] & B[b]).count("1") <= 1 for a in combo for b in chosen)
            if not ok: continue
            nd = need[:]
            bad = False
            for u in combo:
                for s in range(c):
                    if (B[u] >> s) & 1:
                        nd[s] -= 1
                        if nd[s] < 0: bad = True
            if bad: continue
            ndeg = deg - r
            # remaining candidates: not in this point's list, no point with need 0, pairwise <= 1 with chosen
            newc = [u for u in cands if not (B[u] >> best) & 1 and all(nd[s] > 0 for s in range(c) if (B[u] >> s) & 1)
                    and all(bin(B[u] & B[a]).count("1") <= 1 for a in combo)]
            rec(chosen + list(combo), newc, nd, ndeg)
            if cap and len(sols) >= cap: return
    rec([], cand, need, need_deg)
    return sols

if __name__ == "__main__":
    sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
    from lib243 import load_edges
    path, cpath = sys.argv[1], sys.argv[2]
    G = np.load(path) if path.endswith(".npy") else load_edges(path)
    C = [int(x) for x in np.load(cpath)]
    F, B = blocks_from(G, C)
    k = int(G[0].sum()); t = bin(B[0]).count("1")
    rows = [int(r) for r in sys.argv[3:]] or [0]
    for wi in rows:
        t0 = time.time(); D = domain(wi, B, k - t)
        truth = tuple(sorted(i for i, u in enumerate(F) if G[F[wi], u]))
        print(f"row {wi}: domain size {len(D)}  ({time.time() - t0:.1f}s)  true row present: {truth in set(tuple(sorted(d)) for d in D)}", flush=True)
