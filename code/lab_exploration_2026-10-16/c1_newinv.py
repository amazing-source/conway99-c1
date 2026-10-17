"""New exact invariants of the four-star ball (exploration 17/10 night 2).
(a) Conway, 3 not in spec Gamma_S:  D = 0  =>  1^T D_OO 1 = (4/9)(1_Q^T R 1_Q - 4) = 0, R = (3I - Gamma_S)^-1,
    Q = {02, 03, 12, 13} (shared rectangle of l and m).  So 1_Q^T R 1_Q = 4.
(b) Conway: lambda_56..59(A_Omega) = -4 (interlacing, 59 of 99 vertices): mult_{-4}(A_Omega) >= 4 and A_Omega + 4I >= 0.
usage: python c1_newinv.py cache.jsonl maxsides | rank30 file maxobj"""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, rank_mod, relabel, gl_connected, build_H

P = 1000000007
IDX = {l: i for i, l in enumerate(S)}
Qi = [IDX[frozenset(p)] for p in ((0, 2), (0, 3), (1, 2), (1, 3))]
K8 = np.array([[k8(a, b) for b in S] for a in S], dtype=np.int64)
Bm = np.array([[1.0 if r in l else 0.0 for l in S] for r in range(14)])
Cp = np.array([[3.0 * (i == j) - (1.0 if j == (i ^ 1) else 0.0) - 1.0 / 3 for j in range(14)] for i in range(14)])


def ball(EE):
    """59-vertex adjacency: v, letters 0..13, the 44 labels of S."""
    n = 59
    A = np.zeros((n, n), dtype=np.int64)
    for a in range(14):
        A[0, 1 + a] = A[1 + a, 0] = 1
    for a in range(0, 14, 2):
        A[1 + a, 2 + a] = A[2 + a, 1 + a] = 1
    for i, l in enumerate(S):
        for a in l:
            A[15 + i, 1 + a] = A[1 + a, 15 + i] = 1
    for i, j in itertools.combinations(range(44), 2):
        if frozenset((S[i], S[j])) in EE:
            A[15 + i, 15 + j] = A[15 + j, 15 + i] = 1
    return A


def comps_m(EE):
    """number of components of G_m (stars 2, 3 as root line)."""
    sw = {0: 2, 2: 0, 1: 3, 3: 1}
    f = lambda l: frozenset(sw.get(x, x) for x in l)
    EE2 = {frozenset((f(a), f(b))) for a, b in (tuple(x) for x in EE)}
    V, A = build_H(EE2)
    n36 = 36
    seen, st = {0}, [0]
    while st:
        u = st.pop()
        for w in range(n36):
            if A[u, w] and w not in seen:
                seen.add(w); st.append(w)
    # count all components
    left = set(range(n36)) - seen
    c = 1
    while left:
        s0 = left.pop(); st = [s0]; c += 1
        while st:
            u = st.pop()
            for w in range(n36):
                if A[u, w] and w in left:
                    left.discard(w); st.append(w)
    return c


def comps_l(EE):
    V, A = build_H(EE)
    n36 = 36
    left = set(range(n36)); c = 0
    while left:
        s0 = left.pop(); st = [s0]; c += 1
        while st:
            u = st.pop()
            for w in range(n36):
                if A[u, w] and w in left:
                    left.discard(w); st.append(w)
    return c


def analyse(EE):
    G = np.zeros((44, 44), dtype=np.int64)
    for i, j in itertools.combinations(range(44), 2):
        if frozenset((S[i], S[j])) in EE:
            G[i, j] = G[j, i] = 1
    T8 = 24 * np.eye(44, dtype=np.int64) - 8 * G - K8
    nu = 44 - rank_mod(T8.tolist(), P)
    lamT = np.linalg.eigvalsh(T8 / 8.0)[0]
    A = ball(EE)
    m4 = 59 - rank_mod((A + 4 * np.eye(59, dtype=np.int64)).tolist(), P)
    ev = np.linalg.eigvalsh(A.astype(float))
    X = 3 * np.eye(44) - G
    r3 = rank_mod((3 * np.eye(44, dtype=np.int64) - G).tolist(), P)
    q = None; dev = None
    if r3 == 44:
        R = np.linalg.inv(X)
        q = float(R[np.ix_(Qi, Qi)].sum())
        D = Bm @ R @ Bm.T - Cp
        dev = np.linalg.eigvalsh(D[4:, 4:])
    return dict(nu=nu, lamT=lamT, m4=m4, lmin=ev[0], l2=ev[-2], q=q, dev=dev, s3=(r3 < 44))


def main():
    which = sys.argv[1]
    mx = int(sys.argv[3])
    rows = []
    if which == "rank30":
        d = json.load(open(sys.argv[2]))
        lab = [frozenset(x) for x in d["labels"]]
        for s in d["structures"][:mx]:
            EE = {frozenset((lab[i], lab[j])) for i, j in s["edges"]}
            r = analyse(EE); r["c"] = (comps_l(EE), comps_m(EE)); rows.append(r)
    else:
        for line in open(sys.argv[2]):
            d = json.loads(line)
            if len(d["labels"]) != 44:
                continue
            S0 = [frozenset(x) for x in d["labels"]]
            E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
            for side in (0, 1):
                L, EE = relabel(S0, E0, side)
                conn, degok = gl_connected(EE)
                if not (conn and degok):
                    continue
                r = analyse(EE); r["c"] = (1, comps_m(EE)); rows.append(r)
            if len(rows) >= mx:
                break
    tab = Counter()
    for r in rows:
        tab[(r["c"][0] if r["c"][0] < 2 else ">=2", r["nu"], r["m4"], r["lmin"] < -4 - 1e-9, r["lamT"] > -1e-9, r["s3"])] += 1
    print("(c(l), nu, mult_-4(A_Omega), lambda_min < -4, T_S >= 0, 3 in spec Gamma_S): count   [Conway: nu>=14, m4>=4, no, yes]")
    for k, v in sorted(tab.items(), key=str):
        print("   ", k, v)
    qs = [(r["nu"], round(r["q"], 4), round(r["lamT"], 3)) for r in rows if r["q"] is not None]
    print("1_Q^T R 1_Q (Conway = 4), (nu, q, lambda_min T) first 40:", qs[:40])
    if qs:
        print("q range:", min(x[1] for x in qs), max(x[1] for x in qs))
    for r in rows[:6]:
        if r["dev"] is not None:
            print("  nu", r["nu"], "D_OO eigenvalues", np.round(r["dev"], 4))


if __name__ == "__main__":
    main()
