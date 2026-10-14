"""Bipartite skeletons of the integral -4-eigenvectors of norm 16 (NOTE_NIGHT section 20).

f = 1_P - 1_N with |P| = |N| = 8; P and N are cocliques and the bipartite graph H between them is 4-regular with
codegrees <= 2 on both sides (20.1). Type B = every vertex of H has exactly 5 vertices of its own side at codegree 2
(equivalently none at codegree 0). This script enumerates (first row fixed to {0,1,2,3}, rows sorted, only row
intersections 1 or 2, at most two 1s per row: type B on the rows) all 8 x 8 incidence matrices (rows = positives as 4-subsets
of the 8 negatives) with row and column sums 4 and all row and column codegrees <= 2, up to the row order (rows
sorted), and reports how many are of type B on the row side, on the column side, on both.
Exhaustive, pure Python, one process, a few seconds to minutes, memory negligible.
"""
import itertools
import time

subsets = [frozenset(c) for c in itertools.combinations(range(8), 4)]
t0 = time.time()
total = 0
stats = {"rowB": 0, "colB": 0, "bothB": 0}
examples = []


def codeg_profile(sets):
    prof = []
    for i, a in enumerate(sets):
        c2 = sum(1 for j, b in enumerate(sets) if j != i and len(a & b) == 2)
        c0 = sum(1 for j, b in enumerate(sets) if j != i and len(a & b) == 0)
        prof.append((c2, c0))
    return prof


def rec(rows, start, colsum):
    global total
    if len(rows) == 8:
        if any(c != 4 for c in colsum):
            return
        cols = [frozenset(i for i in range(8) if j in rows[i]) for j in range(8)]
        if any(len(cols[a] & cols[b]) > 2 for a in range(8) for b in range(a + 1, 8)):
            return
        total += 1
        rb = all(c2 == 5 for c2, c0 in codeg_profile(rows))
        cb = all(c2 == 5 for c2, c0 in codeg_profile(cols))
        stats["rowB"] += rb
        stats["colB"] += cb
        stats["bothB"] += rb and cb
        if rb and cb and len(examples) < 3:
            examples.append([sorted(r) for r in rows])
        return
    for k in range(start, len(subsets)):
        s = subsets[k]
        if not rows and s != subsets[0]:
            break                                   # column relabelling: first row = {0,1,2,3}
        inter = [len(s & r) for r in rows]
        if any(t > 2 or t == 0 for t in inter):
            continue                                # type B on rows: intersections 1 or 2 only
        ones = [sum(1 for j, r in enumerate(rows) if j != i and len(r & rows[i]) == 1) for i in range(len(rows))]
        if any(ones[i] + (inter[i] == 1) > 2 for i in range(len(rows))) or sum(1 for t in inter if t == 1) > 2:
            continue
        if any(colsum[j] >= 4 for j in s):
            continue
        for j in s:
            colsum[j] += 1
        rows.append(s)
        rec(rows, k + 1, colsum)
        rows.pop()
        for j in s:
            colsum[j] -= 1


rec([], 0, [0] * 8)
print("matrices (rows sorted, columns labelled):", total, " type B on rows:", stats["rowB"],
      " on columns:", stats["colB"], " on both:", stats["bothB"], " %.1f s" % (time.time() - t0))
for ex in examples:
    print("example of type B on both sides:", ex)
