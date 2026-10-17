"""(RS) test.  V_RS = span(4 star vectors z_0..z_3, 11 rectangle indicators of the two roots l, m) has dimension 13
(the 11 rectangles are disjoint; z_0 + z_1 and z_2 + z_3 are sums of rectangles).  Conway needs nu(T_S) >= 14, hence a
kernel vector OUTSIDE V_RS.  This script measures 'excess' = nu - dim(ker T_S cap V_RS) on c(l) = 1 sides.
usage: python c1_rs_test.py cache.jsonl maxsides | walks file1.json ... | rank30 file maxobj"""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, rank_mod, relabel, gl_connected

P = 1000000007
IDX = {l: i for i, l in enumerate(S)}
K8 = np.array([[k8(a, b) for b in S] for a in S], dtype=np.int64)


def rect_star_basis():
    vecs = []
    for r in range(4):
        vecs.append([1 if r in l else 0 for l in S])
    rects = [[(0, 2), (0, 3), (1, 2), (1, 3)]]
    for a in range(4, 14, 2):
        rects.append([(0, a), (0, a + 1), (1, a), (1, a + 1)])
        rects.append([(2, a), (2, a + 1), (3, a), (3, a + 1)])
    for R in rects:
        v = [0] * 44
        for p in R:
            v[IDX[frozenset(p)]] = 1
        vecs.append(v)
    return vecs


VRS = rect_star_basis()


def nullspace_mod(M, p):
    A = [[int(x) % p for x in r] for r in M]
    n = len(A[0]); rows = len(A)
    piv = []; r = 0
    for c in range(n):
        pr = next((i for i in range(r, rows) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = pow(A[r][c], p - 2, p)
        A[r] = [(x * iv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [0] * n; v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i][f]) % p
        basis.append(v)
    return basis


def excess(EE):
    G = np.zeros((44, 44), dtype=np.int64)
    for i, j in itertools.combinations(range(44), 2):
        if frozenset((S[i], S[j])) in EE:
            G[i, j] = G[j, i] = 1
    T8 = 24 * np.eye(44, dtype=np.int64) - 8 * G - K8
    nu = 44 - rank_mod(T8.tolist(), P)
    # dim(ker T cap V_RS) = 13 - rank(T8 * V_RS)
    VR = np.array(VRS, dtype=np.int64).T          # 44 x 15 (rank 13)
    img = (T8 @ VR) % P
    r_img = rank_mod(img.T.tolist(), P)
    inter = 13 - r_img
    lam = np.linalg.eigvalsh(T8 / 8.0)[0]
    return nu, inter, lam > -1e-9


def main():
    which = sys.argv[1]
    tab = Counter()
    if which == "cache":
        mx = int(sys.argv[3]); done = 0
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
                nu, inter, psd = excess(EE)
                tab[(psd, nu, inter, nu - inter)] += 1
                done += 1
            if done >= mx:
                break
    elif which == "walks":
        for f in sys.argv[2:]:
            d = json.load(open(f))
            lab = [frozenset(x) for x in d["labels"]]
            EE = {frozenset((lab[i], lab[j])) for i, j in d["edges"]}
            nu, inter, psd = excess(EE)
            print(f.split("\\")[-1].split("/")[-1], "nu", nu, "ker cap V_RS", inter, "excess", nu - inter, "psd", psd)
            tab[(psd, nu, inter, nu - inter)] += 1
    else:
        d = json.load(open(sys.argv[2]))
        lab = [frozenset(x) for x in d["labels"]]
        for s in d["structures"][: int(sys.argv[3])]:
            EE = {frozenset((lab[i], lab[j])) for i, j in s["edges"]}
            nu, inter, psd = excess(EE)
            tab[(str(s["c"]), nu, inter, nu - inter)] += 1
    print("(positive or c, nu, dim(ker cap V_RS), excess = nu - that) : count     [Conway: nu >= 14 forces excess >= 1]")
    for k, v in sorted(tab.items(), key=str):
        print("   ", k, v)


if __name__ == "__main__":
    main()
