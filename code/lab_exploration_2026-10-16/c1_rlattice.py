"""R-lattice short vectors on the visible rectangles of a four-star block (exploration, LAB 17/10/2026).
In a four-star block (stars 0,1,2,3 = root lines l = {v,0,1}, m = {v,2,3}) the 11 rectangles Q_0j (root l) and Q_1j
(root m) lie in S.  For integral c, H_c = T P c is an integral -4-eigenvector of norm 7 c^t R c (R = P^t T P, Codex);
its restriction to S is T_SS P c (P c is supported on S).  R-norm 2 (norm 14) => co-Heawood (Codex's lemma): values
in {0,+1,-1}, at most 7 + 7, same-sign labels non-adjacent and letter-disjoint, every off-support vertex has at most one
+ and at most one - neighbour (two same-sign labels have their 2 common neighbours in the support) and as many + as -.
Here visible tests on S u letters, for all c in {-1,0,1}^11 with c^t R c = 2, on the c = 1 sides surviving
c1_cutfilter.py.  (R-norm 4 vectors are only counted.)
usage: python c1_rlattice.py <distinct cache.jsonl> [max]"""
import itertools
import json
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
from gg_test import orient, line_graph, components, MATE  # noqa: E402
from c1_cutfilter import tests, kval  # noqa: E402


def analyse(L, E):
    S = [l for l in L if l & {0, 1, 2, 3}]
    n = len(S)
    idx = {l: i for i, l in enumerate(S)}
    G = np.zeros((n, n))
    for x, y in itertools.combinations(S, 2):
        if frozenset((x, y)) in E:
            G[idx[x], idx[y]] = G[idx[y], idx[x]] = 1
    T = 3 * np.eye(n) - G - np.array([[kval(x, y) for y in S] for x in S])
    rects = []
    for j in range(1, 7):                       # root l = {0,1} with root line {2j, 2j+1}
        rects.append([frozenset((r, x)) for r in (0, 1) for x in (2 * j, 2 * j + 1)])
    for j in range(2, 7):                       # root m = {2,3} with root line {2j, 2j+1}
        rects.append([frozenset((r, x)) for r in (2, 3) for x in (2 * j, 2 * j + 1)])
    P = np.zeros((n, len(rects)))
    for k, q in enumerate(rects):
        for w in q:
            P[idx[w], k] = 1
    R = P.T @ T @ P
    Rr = np.round(R)
    assert np.allclose(R, Rr, atol=1e-9)
    cs = np.array(list(itertools.product((-1, 0, 1), repeat=len(rects))), dtype=float)
    vals = np.einsum("ij,jk,ik->i", cs, Rr, cs)
    out = Counter()
    seen = set()
    letters = list(range(14))
    for ci in np.where(np.abs(vals - 2) < 1e-9)[0]:
        h = T @ (P @ cs[ci])
        key = tuple(np.round(h, 6))
        if key in seen or tuple(-x for x in key) in seen:
            continue
        seen.add(key)
        out["norm14_vectors"] += 1
        bad = None
        if not all(abs(x) < 1e-9 or abs(abs(x) - 1) < 1e-9 for x in h):
            bad = "value"
        Pp = [S[i] for i in range(n) if h[i] > 0.5]
        Nn = [S[i] for i in range(n) if h[i] < -0.5]
        if bad is None and (len(Pp) > 7 or len(Nn) > 7):
            bad = "count"
        if bad is None:
            for X in (Pp, Nn):
                for x, y in itertools.combinations(X, 2):
                    if frozenset((x, y)) in E or (x & y):
                        bad = "same-sign adjacent/letter"
        if bad is None:
            # off-support visible labels: at most one + and one - visible neighbour
            supp = set(Pp) | set(Nn)
            for u in S:
                if u in supp:
                    continue
                np_ = sum(1 for x in Pp if frozenset((u, x)) in E)
                nn_ = sum(1 for x in Nn if frozenset((u, x)) in E)
                if np_ > 1 or nn_ > 1:
                    bad = "off-support label sees two of one sign"
                    break
        if bad is None:
            for a in letters:
                np_ = sum(1 for x in Pp if a in x)
                nn_ = sum(1 for x in Nn if a in x)
                if np_ > 1 or nn_ > 1:
                    bad = "letter covered twice"
                    break
        if bad:
            out["killed:" + bad] += 1
    out["norm28_count"] = int(np.sum(np.abs(vals - 4) < 1e-9))
    return out


def main():
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
    tot = Counter()
    killed_sides = 0
    n = 0
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        for side in (0, 1):
            L, E = orient([frozenset(x) for x in d["labels"]], d["edges"], side)
            V, pos, A = line_graph(L, E)
            if any(sum(r) != 3 for r in A) or components(A) != 1:
                continue
            out, _ = tests(L, E)
            if out:
                continue
            n += 1
            if n > mx:
                break
            o = analyse(L, E)
            if any(k.startswith("killed") for k in o):
                killed_sides += 1
            tot["sides with a norm-14 vector"] += 1 if o["norm14_vectors"] else 0
            for k, v in o.items():
                if k != "norm28_count":
                    tot[k] += v
    print("surviving c = 1 sides examined:", min(n, mx))
    print("sides killed by a visible co-Heawood violation:", killed_sides)
    print(dict(tot))


if __name__ == "__main__":
    main()
