"""Scan of the resonance matrix Q over many four-star structures (exploration, LAB 16/10/2026).
For each structure (labels/edges json, four-star block on stars 0..3): T_S PSD? grid on (l,m)? c(l), c(m), nu, and for
both sides the profile dimension dim P = nu - 1 - c and corank(Q) (see q_corank.py).  Aggregates:
  - does dim P = corank(Q) + 1 hold on the PSD structures?
  - largest corank(Q) on non-grid PSD structures (the conjecture Q7 says <= 7, equivalent there to (N9-NG)).
usage: python q_scan.py <root dir> [max files]"""
import collections
import itertools
import json
import os
import sys

import numpy as np

MATE = lambda i: i ^ 1


def kval(a, b):
    s = len(a & b)
    m = sum(1 for p in a for q in b if q == MATE(p))
    return (3 * s + m - 2) / 8.0


def analyse(L, E):
    S = [l for l in L if l & {0, 1, 2, 3}]
    if len(S) != 44:
        return None
    verts = ["v"] + [("L", s) for s in range(14)] + S
    pos = {x: i for i, x in enumerate(verts)}
    n = len(verts)
    A = np.zeros((n, n))
    for s in range(14):
        A[pos["v"], pos[("L", s)]] = A[pos[("L", s)], pos["v"]] = 1
        A[pos[("L", s)], pos[("L", MATE(s))]] = 1
    for l in S:
        for s in l:
            A[pos[l], pos[("L", s)]] = A[pos[("L", s)], pos[l]] = 1
    for a, b in itertools.combinations(S, 2):
        if frozenset((a, b)) in E:
            A[pos[a], pos[b]] = A[pos[b], pos[a]] = 1
    iS = [pos[l] for l in S]
    G = A[np.ix_(iS, iS)]
    K = np.array([[kval(a, b) for b in S] for a in S])
    T = 3 * np.eye(44) - G - K
    et = np.linalg.eigvalsh(T)
    psd = et[0] > -1e-8
    nu = int(np.sum(np.abs(et) < 1e-8))
    out = {"psd": bool(psd), "nu": nu}
    for side, (p, q) in (("l", (0, 1)), ("m", (2, 3))):
        Nset = [("L", s) for s in range(14) if s not in (p, q)] + [l for l in S if l & {p, q}]
        Yset = [l for l in S if not (l & {p, q})]
        iN = [pos[x] for x in Nset]
        iY = [pos[x] for x in Yset]
        ANN = A[np.ix_(iN, iN)]
        if not np.allclose(ANN.sum(1), 3):
            return None
        ev, V = np.linalg.eigh(3 * np.eye(len(iN)) - ANN)
        c = int(np.sum(ev < 1e-9))
        inv = (V[:, ev > 1e-9] / ev[ev > 1e-9]) @ V[:, ev > 1e-9].T
        AYN = A[np.ix_(iY, iN)]
        Q = 3 * np.eye(len(iY)) - A[np.ix_(iY, iY)] - AYN @ inv @ AYN.T
        cor = int(np.sum(np.abs(np.linalg.eigvalsh(Q)) < 1e-8))
        # grid on (l,m): a component of size 6 containing the two letters of the other line
        other = (2, 3) if side == "l" else (0, 1)
        null = V[:, ev < 1e-9]
        comp_grid = False
        if c > 1:
            # component indicator vectors span the null space; find the component of the letter other[0]
            i0 = Nset.index(("L", other[0]))
            sig = np.abs(null[i0]) > 1e-9
            same = [j for j in range(len(Nset)) if np.allclose(null[j], null[i0], atol=1e-8)]
            comp_grid = len(same) == 6
        out[side] = {"c": c, "corQ": cor, "dimP": nu - 1 - c, "grid": comp_grid}
    out["grid"] = out["l"]["grid"] or out["m"]["grid"]
    return out


root = sys.argv[1]
maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
seen = set()
stats = collections.Counter()
rel_ok = rel_bad = 0
maxcor_ng = collections.Counter()
bycz = collections.Counter()
bycg = collections.Counter()
examples = []
nfiles = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith(".json") or nfiles >= maxf:
            continue
        nfiles += 1
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
        stats["structures"] += 1
        if not r["psd"]:
            continue
        stats["psd"] += 1
        for side in ("l", "m"):
            s = r[side]
            if s["dimP"] == s["corQ"] + 1:
                rel_ok += 1
            else:
                rel_bad += 1
                if len(examples) < 5:
                    examples.append((f, side, s, r["nu"]))
            if not r["grid"]:
                maxcor_ng[s["corQ"]] += 1
                bycz[(s["c"], s["corQ"])] += 1
            else:
                bycg[(s["c"], s["corQ"])] += 1
        stats["grid" if r["grid"] else "nongrid"] += 1
print("files %d, distinct structures %d, PSD %d (grid %d, non-grid %d)" % (nfiles, stats["structures"], stats["psd"],
      stats["grid"], stats["nongrid"]))
print("relation dim P = corank(Q) + 1 on PSD sides: %d true, %d false; examples of failure: %s" % (rel_ok, rel_bad,
      examples))
print("corank(Q) distribution on non-grid PSD sides:", dict(sorted(maxcor_ng.items())))
print("non-grid PSD sides by (c, corank Q):", dict(sorted(bycz.items())))
print("grid PSD sides by (c, corank Q):", dict(sorted(bycg.items())))
need = {1: 10, 2: 9, 3: 8, 4: 7}
print("non-grid sides with c <= 4 violating the Conway-killing bound corank <= 11 - c:",
      sum(v for (c, k), v in bycz.items() if c in need and k > need[c]))
