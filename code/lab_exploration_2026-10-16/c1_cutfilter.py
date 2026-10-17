"""Filters from short integral vectors at a c = 1 root (exploration, LAB 17/10/2026).
For S a set of rectangles at root 0 with |cut_S| = 2 in M_0, h_S = T 1_{Q_0S} has norm 14, hence (Codex's lemma) is a
co-Heawood vector: entries in {0,+1,-1}, seven + and seven -, same-sign labels pairwise NON-adjacent and LETTER-DISJOINT,
two same-sign labels have their 2 common neighbours among the opposite sign, each label of the support has exactly
4 neighbours of the opposite sign.  Inside L_0 u L_1, h_S = +1 exactly at the two S-side ends of the cut edges and -1 at
the two other ends.  Tests on the visible part (the 44 four-star labels):
  E3  : some e(Q_0j) = 3 (Codex: impossible);
  LD  : the two + (or the two -) cut ends share a letter;
  VIS : visible h_S has an entry outside {0,+-1}, visible norm > 14, > 7 visible + (or -), two visible same-sign labels
        adjacent or sharing a letter, or a support label with > 4 visible opposite-sign neighbours.
usage: python c1_cutfilter.py <distinct cache.jsonl>"""
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


def tests(L, E):
    roots = [(2 * j, 2 * j + 1) for j in range(1, 7)]
    Q = [[frozenset((r, x)) for r in (0, 1) for x in rt] for rt in roots]
    e_int = [sum(1 for a, b in itertools.combinations(q, 2) if frozenset((a, b)) in E) for q in Q]
    out = set()
    if 3 in e_int:
        out.add("E3")
    m = [[sum(1 for a in Q[j] for b in Q[k] if frozenset((a, b)) in E) if j != k else 0 for k in range(6)]
         for j in range(6)]
    Sset = [l for l in L if l & {0, 1, 2, 3}]
    adj = lambda a, b: frozenset((a, b)) in E
    ncut = 0
    for s in range(1, 4):
        for S in itertools.combinations(range(6), s):
            if s == 3 and 0 not in S:
                continue
            QS = set(w for j in S for w in Q[j])
            cut = [(a, b) for a in QS for b in (w for k in range(6) if k not in S for w in Q[k]) if adj(a, b)]
            if len(cut) != 2:
                continue
            ncut += 1
            plus = [a for a, b in cut]
            minus = [b for a, b in cut]
            if (plus[0] & plus[1]) or (minus[0] & minus[1]) or plus[0] == plus[1] or minus[0] == minus[1]:
                out.add("LD")
            h = {w: sum((3.0 if w == u else 0.0) - (1.0 if adj(w, u) else 0.0) - kval(w, u) for u in QS) for w in Sset}
            vals = set(round(x, 9) for x in h.values())
            P = [w for w in Sset if abs(h[w] - 1) < 1e-9]
            N = [w for w in Sset if abs(h[w] + 1) < 1e-9]
            bad = (not vals <= {0.0, 1.0, -1.0}) or sum(x * x for x in h.values()) > 14 + 1e-9 or len(P) > 7 or len(N) > 7
            for X in (P, N):
                for a, b in itertools.combinations(X, 2):
                    if adj(a, b) or (a & b):
                        bad = True
            for X, Y in ((P, N), (N, P)):
                for a in X:
                    if sum(1 for b in Y if adj(a, b)) > 4:
                        bad = True
            if bad:
                out.add("VIS")
    return out, ncut


def main():
    agg = Counter()
    single = Counter()
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
            n += 1
            out, ncut = tests(L, E)
            agg[tuple(sorted(out))] += 1
            for x in out:
                single[x] += 1
    print("c = 1 sides:", n)
    print("killed by (any): %d ; survivors: %d" % (n - agg[()], agg[()]))
    print("single filters:", dict(single))
    print("combinations:", dict(agg))


if __name__ == "__main__":
    main()
