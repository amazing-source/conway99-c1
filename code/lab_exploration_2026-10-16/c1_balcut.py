"""Minimum balanced even cut of G_l (exploration, LAB 17/10/2026).
For C a set of vertices of G_l with |C n X_p| = q for the three groups (q even, 2 <= q <= 10), the vector
y = (A - 3I)(1_C - (q/12) 1_{G_l}) is an INTEGRAL -4-eigenvector (zero on l, n_C(z) - q/2 on far vertices z, -+ cut
degree on G_l) of norm 7 |cut(C)|.  So |cut(C)| = 2 gives a co-Heawood vector (Codex's lemma): the two inner cut ends
have the same sign and must have no common neighbour off the support; in G_l both cut edges must join the same two
groups (parity), with inner ends in different groups and no common neighbour inside G_l.  Here: for each c = 1 side
surviving c1_cutfilter (no e(Q) = 3 at the root, no 2-cut of the root multigraph), the minimum balanced even cut over
ALL such C (CP-SAT, exact optimum), and whether a 2-cut, if any, passes the local co-Heawood tests.
usage: python c1_balcut.py <distinct cache.jsonl> [max]"""
import itertools
import json
import sys
from collections import Counter

from ortools.sat.python import cp_model

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
from gg_test import orient, line_graph, components, group  # noqa: E402
from c1_cutfilter import tests  # noqa: E402


def min_bal_cut(V, A, forbid=()):
    n = len(V)
    groups = {}
    for i, x in enumerate(V):
        groups.setdefault(group(x), []).append(i)
    best = None
    for q in (2, 4, 6, 8, 10):
        m = cp_model.CpModel()
        x = [m.NewBoolVar("") for _ in range(n)]
        for g, idx in groups.items():
            m.Add(sum(x[i] for i in idx) == q)
        cut = []
        for i, j in itertools.combinations(range(n), 2):
            if A[i][j]:
                d = m.NewBoolVar("")
                m.Add(x[i] + x[j] == 1).OnlyEnforceIf(d)
                m.Add(x[i] == x[j]).OnlyEnforceIf(d.Not())
                cut.append(d)
        for C in forbid:
            m.AddBoolOr([x[i].Not() if i in C else x[i] for i in range(n)])
        m.Add(x[0] == 1)            # break the C <-> complement symmetry (q and 12-q both scanned)
        m.Minimize(sum(cut))
        sv = cp_model.CpSolver()
        sv.parameters.num_search_workers = 2
        sv.parameters.max_time_in_seconds = 30
        st = sv.Solve(m)
        if st == cp_model.OPTIMAL:
            val = int(sv.ObjectiveValue())
            C = frozenset(i for i in range(n) if sv.Value(x[i]))
            if best is None or val < best[0]:
                best = (val, q, C)
    return best


def main():
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
    agg = Counter()
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
            b = min_bal_cut(V, A)
            agg[(b[0], b[1]) if b else None] += 1
    print("surviving c = 1 sides:", min(n, mx))
    print("(min balanced even cut, q): count", dict(sorted(agg.items(), key=str)))


if __name__ == "__main__":
    main()
