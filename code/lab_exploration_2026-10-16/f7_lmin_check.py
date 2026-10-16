"""Interlacing filters on every PSD block: A >= -4 forces lambda_min(Gamma_S) >= -4 and lambda_min(A_W) >= -4
(W = v + 14 letters + 44 labels, an induced subgraph); U_S = 7 Pi_S - T_S >= 0 (Pi = projector on balanced vectors)."""
import json, sys, collections
import numpy as np
MATE = lambda i: i ^ 1
recs = {json.loads(x)["src"]: json.loads(x) for x in open(sys.argv[1])}
agg = collections.Counter()
ex = []
outrecs = []
for line in open(sys.argv[2]):
    d = json.loads(line)
    r = recs.get(d["src"])
    if r is None:
        continue
    L = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
    S = [l for l in L if l & {0, 1, 2, 3}]
    n = len(S)
    G = np.array([[1 if i != j and frozenset((a, b)) in E else 0 for j, b in enumerate(S)] for i, a in enumerate(S)], dtype=float)
    B = np.array([[1 if q in l else 0 for l in S] for q in range(14)], dtype=float)
    A = np.zeros((59, 59))
    A[0, 1:15] = A[1:15, 0] = 1
    for q in range(14):
        A[1 + q, 1 + MATE(q)] = 1
    A[1:15, 15:] = B
    A[15:, 1:15] = B.T
    A[15:, 15:] = G
    lg = np.linalg.eigvalsh(G)[0]
    la = np.linalg.eigvalsh(A)[0]
    # T_S and U_S
    Mt = np.zeros((n, n))
    for i, a in enumerate(S):
        for j, b in enumerate(S):
            s = len(a & b); m = sum(1 for p in a for q in b if q == MATE(p))
            Mt[i, j] = (24 if i == j else 0) - 8 * G[i, j] - 3 * s - m + 2
    T = Mt / 8
    M14 = np.array([[1.0 if q2 == MATE(q) else 0.0 for q2 in range(14)] for q in range(14)])
    BBt = 11 * np.eye(14) - M14 + np.ones((14, 14))       # B B^T over the 84 labels (independent of the data)
    PiS = np.eye(n) - B.T @ np.linalg.solve(BBt, B)        # principal S-block of the 84-label projector Pi

    U = 7 * PiS - T
    lu = np.linalg.eigvalsh(U)[0]
    key = ("G" if r["grid"] else "NG", lg < -4 - 1e-9, la < -4 - 1e-9, lu < -1e-9)
    r["Upsd"] = bool(lu >= -1e-9); r["lminA"] = float(la); outrecs.append(r)
    agg[key] += 1
    if (lg < -4 - 1e-9 or la < -4 - 1e-9) and len(ex) < 5:
        ex.append((d["src"], round(lg, 4), round(la, 4), round(lu, 4)))
print("(grid?, lmin(Gamma_S) < -4, lmin(A_W) < -4, U_S not PSD): count")
for k, v in sorted(agg.items()):
    print("  ", k, v)
print("examples:", ex)
with open(sys.argv[3], "w") as fo:
    for r in outrecs:
        fo.write(json.dumps(r) + "\n")
