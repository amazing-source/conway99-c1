"""c = 1 roots: rectangle multigraph M_0 and its small cuts (exploration, LAB 17/10/2026).
At v, root line l = {v,0,1} with c(l) = 1; the 6 other root lines j = {2j', 2j'+1}; Q_0j = {0,1} x j (4 labels).
M_0: nodes = the 6 rectangles, multiplicity m_jk = number of Gamma-edges between Q_0j and Q_0k (inside L_0 u L_1).
Degrees d_j = 8 - 2 e(Q_0j) (Codex: e != 3, so d_j in {4,6,8}).  For S a set of rectangles, h_S = T 1_{Q_0S} is an
integral -4-eigenvector of norm 7 |cut_S| (Codex's identity H^t H = 7R); a 2-cut gives norm 14, i.e. a co-Heawood
configuration (Codex's lemma).  We list, over the c = 1 sides of the data, the min cut of M_0, the number of 2-cuts,
and for each 2-cut the visible part h_S | S (S = four-star block) and its norm.
usage: python c1_mincut.py <distinct cache.jsonl> [max]"""
import itertools
import json
import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
from gg_test import orient, line_graph, components, MATE  # noqa: E402


def kval(a, b):
    s = len(a & b)
    m = sum(1 for p in a for q in b if q == MATE(p))
    return (3 * s + m - 2) / 8.0


def main():
    cache = sys.argv[1]
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
    agg, normagg, eagg = Counter(), Counter(), Counter()
    n = 0
    for line in open(cache):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        for side in (0, 1):
            L, E = orient([frozenset(x) for x in d["labels"]], d["edges"], side)
            V, pos, A = line_graph(L, E)
            if any(sum(r) != 3 for r in A) or components(A) != 1:
                continue
            n += 1
            if n > mx:
                break
            roots = [(2 * j, 2 * j + 1) for j in range(1, 7)]
            Q = [[frozenset((r, x)) for r in (0, 1) for x in rt] for rt in roots]
            e_int = [sum(1 for a, b in itertools.combinations(q, 2) if frozenset((a, b)) in E) for q in Q]
            m = [[sum(1 for a in Q[j] for b in Q[k] if frozenset((a, b)) in E) if j != k else 0 for k in range(6)]
                 for j in range(6)]
            deg = [sum(m[j]) for j in range(6)]
            assert all(deg[j] == 8 - 2 * e_int[j] for j in range(6)), (deg, e_int)
            eagg[tuple(sorted(e_int))] += 1
            cuts = {}
            for s in range(1, 4):
                for S in itertools.combinations(range(6), s):
                    if s == 3 and 0 not in S:
                        continue
                    cut = sum(m[j][k] for j in S for k in range(6) if k not in S)
                    cuts[S] = cut
            mc = min(cuts.values())
            two = [S for S, c in cuts.items() if c == 2]
            agg[(mc, len(two))] += 1
            Sset = [l for l in L if l & {0, 1, 2, 3}]
            for S in two:
                QS = [w for j in S for w in Q[j]]
                h = {}
                for w in Sset:
                    val = sum((3.0 if w == u else 0.0) - (1.0 if frozenset((w, u)) in E else 0.0) - kval(w, u) for u in QS)
                    h[w] = val
                vals = Counter(round(x, 6) for x in h.values())
                nrm = sum(x * x for x in h.values())
                normagg[(round(nrm, 6), tuple(sorted(vals.items())))] += 1
    print("c = 1 sides:", min(n, mx))
    print("internal edge counts e(Q_0j) (sorted): ", dict(eagg.most_common(12)))
    print("(min cut of M_0, number of 2-cuts): count", dict(sorted(agg.items())))
    print("2-cuts: visible norm of h_S on the 44 block labels, value histogram: count")
    for k, v in sorted(normagg.items())[:20]:
        print("   ", k, v)


main()
