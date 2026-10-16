"""Where the 7-adic drop lives: the balanced eigenvalue-3 space of the label graph (exploration, LAB 16/10/2026).
For h with B_S h = 0 (all letter sums zero: 'balanced'), 8T_S h = 8 (3I - Gamma_S) h exactly.  Hence mod 7, on balanced
vectors, ker_7(8T_S) = ker_7(Gamma_S - 3I): the rational eigenvalues 3 AND -4 of Gamma_S (3 = -4 mod 7) both land in it.
For every PSD block:
  drop      = dim ker_7(8T_S) - nu
  drop_bal  = dim(ker_7 n ker_7 B) - dim(N_7 n ker_7 B)       (balanced part of the drop)
  drop_shad = rank_7(B ker_7) - rank_7(B N_7)                  (part visible on the letters), drop = drop_bal + drop_shad
  b3, bm4   = dim ker_Q(Gamma_S - 3I) n ker_Q B,  dim ker_Q(Gamma_S + 4I) n ker_Q B   (exact)
  b7        = dim ker_7(Gamma_S - 3I) n ker_7 B
usage: python f7_balanced.py <root dir> [max structures]
       python f7_balanced.py --cache <distinct.jsonl> <start> <count> <out.jsonl>   (records, resumable)
       python f7_balanced.py --agg <out.jsonl>"""
import collections
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f7_classform import t8, rref_mod, null_mod, int_kernel, saturate7, grid_square  # noqa: E402

P1, P2 = 1000003, 999983


def line_grid(S, E):
    """grid flag of f7_rank_scan.py / q_scan.py: the component of letter 2 in the line graph of (0,1) has size 6"""
    labs = [l for l in S if l & {0, 1}]
    adj = {("L", s): {("L", s ^ 1)} for s in range(2, 14)}
    for l in labs:
        adj[l] = set()
    for l in labs:
        for s in l - {0, 1}:
            adj[("L", s)].add(l)
            adj[l].add(("L", s))
    for i, a in enumerate(labs):
        for b in labs[i + 1:]:
            if frozenset((a, b)) in E:
                adj[a].add(b)
                adj[b].add(a)
    seen, st = {("L", 2)}, [("L", 2)]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                st.append(w)
    return len(seen) == 6


def rank_np(M, p):
    """rank mod p, vectorised (entries < p < 2^20, so products fit in int64)"""
    A = np.array(M, dtype=np.int64) % p
    n, m = A.shape
    r = 0
    for c in range(m):
        nz = np.nonzero(A[r:, c])[0]
        if nz.size == 0:
            continue
        piv = r + nz[0]
        A[[r, piv]] = A[[piv, r]]
        A[r] = (A[r] * pow(int(A[r, c]), p - 2, p)) % p
        col = A[:, c].copy()
        col[r] = 0
        nzr = np.nonzero(col)[0]
        if nzr.size:
            A[nzr] = (A[nzr] - np.outer(col[nzr], A[r]) % p) % p
        r += 1
        if r == n:
            break
    return r


def rank_big(M):
    """rank over Q as the max of the ranks mod two large primes (rank_p <= rank_Q, equal unless p divides all the
    maximal non-zero minors); the agreement flag makes a disagreement visible"""
    a, b = rank_np(M, P1), rank_np(M, P2)
    return max(a, b), a == b


def analyse(L, E):
    S = [l for l in L if l & {0, 1, 2, 3}]
    if len(S) != 44:
        return None
    M = t8(S, E)
    ev = np.linalg.eigvalsh(M.astype(float))
    if ev[0] < -1e-6:
        return None
    rq = int(np.sum(ev > 1e-6))
    nu = 44 - rq
    idx = {l: i for i, l in enumerate(S)}
    G = [[0] * 44 for _ in range(44)]
    for i, a in enumerate(S):
        for j, b in enumerate(S):
            if i != j and frozenset((a, b)) in E:
                G[i][j] = 1
    B = [[1 if r in l else 0 for l in S] for r in range(14)]
    r7 = rank_np(M, 7)
    drop = (44 - r7) - nu
    out = {"rq": rq, "drop": drop, "grid": grid_square(S, E), "lgrid": line_grid(S, E)}
    G3 = [[G[i][j] - (3 if i == j else 0) for j in range(44)] for i in range(44)]
    G4 = [[G[i][j] + (4 if i == j else 0) for j in range(44)] for i in range(44)]
    r3, ok3 = rank_big(G3 + B)
    r4, ok4 = rank_big(G4 + B)
    out["b3"], out["bm4"] = 44 - r3, 44 - r4
    out["b7"] = 44 - rank_np(G3 + B, 7)
    out["ok"] = ok3 and ok4
    if drop == 0:
        out["dbal"], out["dshad"] = 0, 0
        return out
    k7 = null_mod(M.tolist(), 7)
    N7 = rref_mod(saturate7(int_kernel(M.tolist())), 7)[0]
    Bm = np.array(B, dtype=np.int64)
    sh_k = len(rref_mod(((Bm @ np.array(k7, dtype=np.int64).T) % 7).T.tolist(), 7)[0])
    sh_n = len(rref_mod(((Bm @ np.array(N7, dtype=np.int64).T) % 7).T.tolist(), 7)[0]) if N7 else 0
    out["dshad"] = sh_k - sh_n
    out["dbal"] = drop - out["dshad"]
    return out


if __name__ == "__main__":
    if sys.argv[1] == "--cache":
        cache, start, count, outp = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
        t0 = time.time()
        lines = open(cache).read().splitlines()[start:start + count]
        with open(outp, "a") as fo:
            for line in lines:
                d = json.loads(line)
                L = [frozenset(x) for x in d["labels"]]
                E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
                r = analyse(L, E)
                if r is None:
                    continue
                r["src"] = d["src"]
                fo.write(json.dumps(r) + "\n")
        print("done %d..%d in %.0f s" % (start, start + len(lines), time.time() - t0))
        sys.exit(0)
    if sys.argv[1] == "--agg":
        agg = collections.Counter()
        notok = 0
        recs = [json.loads(x) for x in open(sys.argv[2])]
        for r in recs:
            notok += 0 if r["ok"] else 1
            agg[("G" if r["grid"] else ("g" if r["lgrid"] else "NG"), r["rq"], r["drop"], r["dbal"], r["dshad"],
                 r["b3"], r["bm4"], r["b7"])] += 1
        print("PSD structures: %d; prime disagreements on rational ranks: %d" % (len(recs), notok))
        print("G = full 3x3 grid (4 corner edges), g = line-grid of (0,1) only, NG = neither")
        print("(grid, rank_Q, drop, drop_bal, drop_shad, b3, b-4, b7): count")
        for k, v in sorted(agg.items()):
            extra = "" if k[7] == k[5] + k[6] else "   (b7 - b3 - b-4 = %d)" % (k[7] - k[5] - k[6])
            print("  ", k, v, extra)
        sys.exit(0)

    root = sys.argv[1]
    maxs = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
    t0 = time.time()
    seen, n = set(), 0
    agg = collections.Counter()
    notok = 0
    for dp, dn, fn in os.walk(root):
        for f in sorted(fn):
            if not f.endswith(".json") or n >= maxs:
                continue
            try:
                d = json.load(open(os.path.join(dp, f)))
                L = [frozenset(x) for x in d["labels"]]
                E = set(frozenset((L[i], L[j])) for i, j in d["edges"])
            except Exception:
                continue
            key = frozenset(E)
            if key in seen:
                continue
            seen.add(key)
            r = analyse(L, E)
            if r is None:
                continue
            n += 1
            notok += 0 if r["ok"] else 1
            agg[("G" if r["grid"] else "NG", r["rq"], r["drop"], r["dbal"], r["dshad"], r["b3"], r["bm4"], r["b7"])] += 1
    print("PSD structures: %d (%.0f s); prime disagreements on rational ranks: %d" % (n, time.time() - t0, notok))
    print("(square?, rank_Q, drop, drop_bal, drop_shad, b3, b-4, b7): count     [check: b7 >= b3 + b-4]")
    for k, v in sorted(agg.items()):
        flag = "" if k[7] >= k[5] + k[6] else "   <-- b7 < b3+b-4 ?!"
        extra = "" if k[7] == k[5] + k[6] else "   (b7 - b3 - b-4 = %d)" % (k[7] - k[5] - k[6])
        print("  ", k, v, flag or extra)
