"""H46: for a pair of lines (l, m) at v, l = {v,p,q}, m = {v,r,r'}: H = N(l) u Y_r', the 36 neighbours of the line l plus the
10 neighbours of the point r' that are at distance 2 from l (labels {r', s}, s outer).  |H| = 46.
In a Conway graph every induced subgraph on 46 vertices has eigenvalue 3 (interlacing: mult_3(A) = 54 = 99 - 45).
So any local structure in which H has no eigenvalue 3 is impossible.  Scan all PSD blocks (records with grid flag),
both lines as l and both points of m as r': multiplicity of 3 in A_H, by (grid?, c(l)).
usage: python h46_scan.py <distinct cache.jsonl> <bal_records_U.jsonl>"""
import itertools, json, sys, collections
import numpy as np
MATE = lambda i: i ^ 1


def h46(S, E, p, q, r, rr):
    letters = [("L", s) for s in range(14) if s not in (p, q)]
    Gv = letters + [l for l in S if l & {p, q}]
    Y = [l for l in S if rr in l and not (l & {p, q})]
    V = Gv + Y
    def adj(a, b):
        if isinstance(a, tuple) and isinstance(b, tuple):
            return MATE(a[1]) == b[1]
        if isinstance(a, tuple):
            return a[1] in b
        if isinstance(b, tuple):
            return b[1] in a
        return frozenset((a, b)) in E
    A = np.array([[1.0 if i != j and adj(a, b) else 0.0 for j, b in enumerate(V)] for i, a in enumerate(V)])
    AG = A[:36, :36]
    c = int(np.sum(np.linalg.eigvalsh(3 * np.eye(36) - AG) < 1e-9))
    ev = np.linalg.eigvalsh(A)
    return c, int(np.sum(np.abs(ev - 3) < 1e-7)), len(V)


recs = {json.loads(x)["src"]: json.loads(x) for x in open(sys.argv[2])}
agg = collections.Counter()
for line in open(sys.argv[1]):
    d = json.loads(line)
    r = recs.get(d["src"])
    if r is None:
        continue
    L = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
    S = [l for l in L if l & {0, 1, 2, 3}]
    for (p, q), (rA, rB) in (((0, 1), (2, 3)), ((2, 3), (0, 1))):
        for rr in (rA, rB):
            c, m3, nv = h46(S, E, p, q, rA, rr)
            assert nv == 46
            agg[("G" if r["grid"] else "NG", "U>=0" if r["Upsd"] else "U-", c, m3)] += 1
print("(grid?, U_S >= 0?, c(l), mult_3(A_H)): count of (side, point) choices")
for k, v in sorted(agg.items()):
    print("  ", k, v)
