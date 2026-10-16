"""Branch min c <= 3: how many odd saturations can coexist? (exploration, LAB 16/10/2026 night)
For a pair (l, m), l = {v,0,1} (side with c(l) = c), iota = (2 3): Codex's decomposition of T44 into U (20 labels avoiding
2, 3), P (12 even pairs), R (12 odd pairs); K = T_UU, C = T_UR, Phi = T_RR, M = C Phi^+ C^t.  The generalized eigenvalues
lambda_1 >= lambda_2 >= ... of (M, K) on range(K) lie in [0, 1] (T >= 0) and delta = #{lambda_i = 1} = 9 - rank D.
Exact identity (Codex): rank T = 32 - c - delta + rank Z, so Conway (rank T <= 30) needs delta >= rank Z + c - 2.
For c = 1 that is delta >= rank Z - 1 + ... ; we record per side: c, lambda_1..lambda_6, trace = sum lambda_i, delta,
rank Z, rank F, and the slack s = (rank Z - delta) - (c - 2) (Conway needs s <= 0).
Input: the distinct-structure cache (build_cache.py) and the records with the U_S >= 0 flag (f7_lmin_check.py).
usage: python cle3_spectrum.py <distinct cache.jsonl> <records with Upsd.jsonl> <out.jsonl>"""
import itertools
import json
import sys

import numpy as np

MATE = lambda i: i ^ 1


def kval(a, b):
    s = len(a & b)
    m = sum(1 for p in a for q in b if q == MATE(p))
    return (3 * s + m - 2) / 8.0


def comps(S, E, p, q):
    verts = [("L", s) for s in range(14) if s not in (p, q)] + [l for l in S if l & {p, q}]
    adj = {x: set() for x in verts}
    for s in range(14):
        if s in (p, q):
            continue
        adj[("L", s)].add(("L", MATE(s)))
        for r in (p, q):
            lab = frozenset((r, s))
            adj[("L", s)].add(lab)
            adj[lab].add(("L", s))
    labs = [x for x in verts if not isinstance(x, tuple)]
    for x, y in itertools.combinations(labs, 2):
        if frozenset((x, y)) in E:
            adj[x].add(y)
            adj[y].add(x)
    seen, c = set(), 0
    for x in verts:
        if x in seen:
            continue
        c += 1
        st = [x]
        seen.add(x)
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    st.append(w)
    return c


def pinv_psd(M, tol=1e-9):
    e, V = np.linalg.eigh(M)
    k = e > tol
    return (V[:, k] / e[k]) @ V[:, k].T, int(k.sum())


def side(S, idx, T, r1, r2):
    U = [l for l in S if not (l & {r1, r2})]
    others = [a for a in range(14) if a not in (r1, r2)]
    pairs = [(frozenset((r1, a)), frozenset((r2, a))) for a in others if frozenset((r1, a)) in idx]
    n = 44
    B = np.zeros((n, n))
    col = 0
    for l in U:
        B[idx[l], col] = 1
        col += 1
    for x, y in pairs:
        B[idx[x], col] = B[idx[y], col] = 1 / np.sqrt(2)
        col += 1
    nP = len(pairs)
    for x, y in pairs:
        B[idx[x], col] = 1 / np.sqrt(2)
        B[idx[y], col] = -1 / np.sqrt(2)
        col += 1
    Tb = B.T @ T @ B
    nU = len(U)
    K = Tb[:nU, :nU]
    C = Tb[:nU, nU + nP:]
    Phi = Tb[nU + nP:, nU + nP:]
    Phip, _ = pinv_psd(Phi)
    M = C @ Phip @ C.T
    ek, Vk = np.linalg.eigh(K)
    keep = ek > 1e-9
    Kh = Vk[:, keep] / np.sqrt(ek[keep])
    lam = np.sort(np.linalg.eigvalsh(Kh.T @ M @ Kh))[::-1] if keep.any() else np.zeros(0)
    rankK = int(keep.sum())
    rankK1 = int(np.sum(np.linalg.eigvalsh(K - M) > 1e-8))
    delta = rankK - rankK1
    # F on Y = outer labels of the iota-swapped line (labels {r1,s},{r2,s}, s outer), eliminating the rest of S
    Y = [l for l in S if (l & {r1, r2}) and not (l & ({0, 1, 2, 3} - {r1, r2}))]
    N = [l for l in S if l not in set(Y)]
    iY = [idx[l] for l in Y]
    iN = [idx[l] for l in N]
    TNN = T[np.ix_(iN, iN)]
    TNNp, _ = pinv_psd(TNN)
    F = T[np.ix_(iY, iY)] - T[np.ix_(iY, iN)] @ TNNp @ T[np.ix_(iN, iY)]
    rankF = int(np.sum(np.linalg.eigvalsh((F + F.T) / 2) > 1e-7))
    # even/odd split of F on Y
    outer = sorted({min(l - {r1, r2}) for l in Y})
    Pm = np.zeros((len(Y), len(outer)))
    Rm = np.zeros((len(Y), len(outer)))
    for j, s in enumerate(outer):
        a, b = Y.index(frozenset((r1, s))), Y.index(frozenset((r2, s)))
        Pm[a, j] = Pm[b, j] = 1 / np.sqrt(2)
        Rm[a, j], Rm[b, j] = 1 / np.sqrt(2), -1 / np.sqrt(2)
    A = Pm.T @ F @ Pm
    Cc = Pm.T @ F @ Rm
    D = Rm.T @ F @ Rm
    Dp, rankD = pinv_psd((D + D.T) / 2, 1e-7)
    Z = A - Cc @ Dp @ Cc.T
    rankZ = int(np.sum(np.linalg.eigvalsh((Z + Z.T) / 2) > 1e-7))
    return {"lam": [round(float(x), 6) for x in lam[:6]], "trace": round(float(lam.sum()), 6), "delta": delta,
            "rankD": rankD, "rankZ": rankZ, "rankF": rankF}


if __name__ == "__main__":
    cache, recp, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    recs = {}
    for x in open(recp):
        r = json.loads(x)
        recs[r["src"]] = r
    n = 0
    with open(outp, "w") as fo:
        for line in open(cache):
            d = json.loads(line)
            r = recs.get(d["src"])
            if r is None or not r["Upsd"] or r["grid"]:
                continue
            L = [frozenset(x) for x in d["labels"]]
            E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
            S = [l for l in L if l & {0, 1, 2, 3}]
            idx = {l: i for i, l in enumerate(S)}
            G = np.zeros((44, 44))
            for a, b in itertools.combinations(S, 2):
                if frozenset((a, b)) in E:
                    G[idx[a], idx[b]] = G[idx[b], idx[a]] = 1
            T = 3 * np.eye(44) - G - np.array([[kval(a, b) for b in S] for a in S])
            for (r1, r2), (p1, p2) in (((2, 3), (0, 1)), ((0, 1), (2, 3))):
                c = comps(S, E, p1, p2)
                s = side(S, idx, T, r1, r2)
                s.update({"src": d["src"], "c": c, "rq": r["rq"]})
                fo.write(json.dumps(s) + "\n")
            n += 1
    print("non-grid admissible blocks:", n)
