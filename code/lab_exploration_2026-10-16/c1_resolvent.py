"""Resolvent identity, checked mod two large primes.  8T_S = 24I - 8 Gamma_S - B^T C B, C = 3I + M - J/2 (14 letters).
When 3 is not an eigenvalue of Gamma_S: nu(T_S) = nullity of D = B R B^T - (3I - M - J/3), R = (3I - Gamma_S)^{-1};
Conway (nu = 14) <=> D = 0.  Consequence (N1): B R 1 = -(4/3) 1 (letter sums of phi = R 1)."""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, rank_mod, relabel, gl_connected

PR = (1000000007, 998244353)
Bm = np.array([[1 if r in l else 0 for l in S] for r in range(14)], dtype=object)
Mm = np.array([[1 if j == (i ^ 1) else 0 for j in range(14)] for i in range(14)], dtype=object)

def inv_mod(A, p):
    n = len(A)
    M = [[int(x) % p for x in row] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(A)]
    for c in range(n):
        pr = next((i for i in range(c, n) if M[i][c]), None)
        if pr is None:
            return None
        M[c], M[pr] = M[pr], M[c]
        iv = pow(M[c][c], p - 2, p)
        M[c] = [(x * iv) % p for x in M[c]]
        for i in range(n):
            if i != c and M[i][c]:
                f = M[i][c]
                M[i] = [(x - f * y) % p for x, y in zip(M[i], M[c])]
    return [row[n:] for row in M]

def analyse(G):
    out = []
    for p in PR:
        X = [[(3 if i == j else 0) - int(G[i][j]) for j in range(44)] for i in range(44)]
        R = inv_mod(X, p)
        if R is None:
            return None
        R = np.array(R, dtype=object)
        BRB = (Bm.dot(R) % p).dot(Bm.T) % p
        third = pow(3, p - 2, p)
        tgt = np.array([[(3 * (i == j) - Mm[i][j] - third) % p for j in range(14)] for i in range(14)], dtype=object)
        D = (BRB - tgt) % p
        phi = (Bm.dot(R.dot(np.ones(44, dtype=object)) % p)) % p
        n1 = [(int(x) + 4 * third) % p == 0 for x in phi]
        out.append((rank_mod(D.tolist(), p), sum(n1)))
    return out

def Tnu(G):
    K8 = np.array([[k8(a, b) for b in S] for a in S], dtype=np.int64)
    return 44 - rank_mod((24 * np.eye(44, dtype=np.int64) - 8 * np.array(G, dtype=np.int64) - K8).tolist(), PR[0])

which = sys.argv[1]
tab = Counter()
if which == "rank30":
    d = json.load(open(sys.argv[2]))
    lab = [frozenset(x) for x in d["labels"]]
    for s in d["structures"][: int(sys.argv[3])]:
        EE = {frozenset((lab[i], lab[j])) for i, j in s["edges"]}
        G = [[1 if i != j and frozenset((S[i], S[j])) in EE else 0 for j in range(44)] for i in range(44)]
        out = analyse(G)
        tab[("3 in spec Gamma_S",) if out is None else (Tnu(G), out[0][0], out[1][0], out[0][1])] += 1
    print("rank-30 objects: (nu(T_S), rank D mod p1, rank D mod p2, #letters with N1 holding) : count")
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
            G = [[1 if i != j and frozenset((S[i], S[j])) in EE else 0 for j in range(44)] for i in range(44)]
            out = analyse(G)
            tab[("3 in spec Gamma_S",) if out is None else (Tnu(G), out[0][0], out[1][0], out[0][1])] += 1
            if sum(tab.values()) >= int(sys.argv[3]):
                break
        if sum(tab.values()) >= int(sys.argv[3]):
            break
    print("c(l)=1 sides: (nu(T_S), rank D mod p1, rank D mod p2, #letters with N1 holding) : count")
for k, v in sorted(tab.items(), key=str):
    print("   ", k, v)
