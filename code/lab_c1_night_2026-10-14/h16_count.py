"""Upper bound for the number of type-B vectors of norm 16 (NOTE_NIGHT section 20).

A type-B vector f = 1_P - 1_N is reconstructed from: a positive p (99 choices), its four negative neighbours (one
point on each of 4 of the 7 lines through p: 560 choices), the "missing pair" (6 choices), and then, following the
skeleton H, every further vertex as a common neighbour of two vertices already known: a pair of non-adjacent
vertices has exactly 2 common neighbours, so such a vertex has at most 2 candidates, and exactly 1 if the other
common neighbour of that pair (in H) is already known. The skeleton seen from p is one of finitely many labelled
patterns (from the exhaustive list of h16_types.py, all 8 x 8 matrices with first row {0,1,2,3}).
Bound: N_B <= 99 * 560 * (sum over missing pairs and patterns of prod(candidates)) / 8
(each type-B vector is counted from each of its 8 positives). Exhaustive, pure Python, seconds.
"""
import itertools

subsets = [frozenset(c) for c in itertools.combinations(range(8), 4)]
mats = []


def rec(rows, start, colsum):
    if len(rows) == 8:
        if any(c != 4 for c in colsum):
            return
        cols = [frozenset(i for i in range(8) if j in rows[i]) for j in range(8)]
        if any(len(cols[a] & cols[b]) > 2 for a in range(8) for b in range(a + 1, 8)):
            return
        prof_r = [sum(1 for j in range(8) if j != i and len(rows[i] & rows[j]) == 2) for i in range(8)]
        prof_c = [sum(1 for j in range(8) if j != i and len(cols[i] & cols[j]) == 2) for i in range(8)]
        if all(x == 5 for x in prof_r) and all(x == 5 for x in prof_c):
            mats.append(list(rows))
        return
    for k in range(start, len(subsets)):
        s = subsets[k]
        if not rows and s != subsets[0]:
            break
        inter = [len(s & r) for r in rows]
        if any(t > 2 or t == 0 for t in inter):
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
print("type-B matrices with first row {0,1,2,3}:", len(mats))

# labelled vertices: positives 'P0'..'P7' (rows), negatives 'N0'..'N7' (columns); p = P0, its negatives N0..N3.
patterns = {}
for rows in mats:
    adj = {}
    for i, r in enumerate(rows):
        for j in r:
            adj.setdefault("P%d" % i, set()).add("N%d" % j)
            adj.setdefault("N%d" % j, set()).add("P%d" % i)
    inter0 = {i: rows[i] & rows[0] for i in range(1, 8)}
    present = {frozenset(v) for v in inter0.values() if len(v) == 2}
    missing = [frozenset(c) for c in itertools.combinations(range(4), 2) if frozenset(c) not in present]
    assert len(missing) == 1
    # canonical labels relative to p: w_ab for positives meeting p in {a,b}, r_a for positives meeting p in {a}
    lab = {"P0": "p"}
    for i, v in inter0.items():
        lab["P%d" % i] = ("w" if len(v) == 2 else "r") + "".join(str(t) for t in sorted(v))
    for j in range(4):
        lab["N%d" % j] = "n%d" % j
    mcols = frozenset(frozenset(lab["P%d" % i] for i in range(8) if j in rows[i]) for j in range(4, 8))
    key = (missing[0], mcols)
    patterns.setdefault(missing[0], set()).add(mcols)


def candidates(mcols):
    """Greedy reconstruction from p, n0..n3 and the w's (all determined); returns the product of candidate counts."""
    known_pos = {"p"} | {x for col in mcols for x in col if x.startswith("w")}
    pos_adj = {}
    for col_id, col in enumerate(sorted(mcols, key=sorted)):
        for x in col:
            pos_adj.setdefault(x, set()).add("m%d" % col_id)
    neg_of = {}
    for x in known_pos | {x for col in mcols for x in col}:
        s = set()
        if x == "p":
            s = {"n0", "n1", "n2", "n3"}
        elif x.startswith("w"):
            s = {"n" + x[1], "n" + x[2]}
        elif x.startswith("r"):
            s = {"n" + x[1]}
        neg_of[x] = s | pos_adj.get(x, set())
    pos_of = {}
    for x, s in neg_of.items():
        for n in s:
            pos_of.setdefault(n, set()).add(x)
    known = set(known_pos) | {"n0", "n1", "n2", "n3"}
    unknown = set(pos_of) | set(neg_of)
    unknown -= known
    total = 1
    while unknown:
        best = None
        for v in sorted(unknown):
            nb = neg_of[v] if v in neg_of else pos_of[v]
            kn = [u for u in nb if u in known]
            if len(kn) < 2:
                continue
            c = 2
            for u, u2 in itertools.combinations(kn, 2):
                side = neg_of if u in neg_of else pos_of
                common = (side[u] & side[u2])
                other = common - {v}
                if other and all(o in known for o in other):
                    c = 1
                    break
            if best is None or c < best[0]:
                best = (c, v)
        if best is None:
            return None
        total *= best[0]
        known.add(best[1])
        unknown.discard(best[1])
    return total


total = 0
for miss, pats in sorted(patterns.items(), key=lambda t: sorted(t[0])):
    counts = [candidates(m) for m in pats]
    print("missing pair", sorted(miss), ": patterns", len(pats), " candidate products", sorted(counts))
    total += sum(counts)
bound = 99 * 560 * total / 8
print("N_B <= 99 * 560 * %d / 8 = %.0f" % (total, bound))
