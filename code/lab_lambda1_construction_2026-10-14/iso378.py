"""Isomorphism test between lambda = 1 srgs with the prism colours as initial pair colours (14/10/2026); also builds the
graph of the complementary hemisystem. usage: python iso378.py <gq.json> <hemi.json> <edges a> <edges b>"""
import json, os, sys, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pq_invariants as PQ
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T

def colours_joint(A1, A2):
    C1 = PQ.pair_colours(A1)[0]; C2 = PQ.pair_colours(A2)[0]
    return C1, C2

def iso(A1, A2):
    n = len(A1)
    C1raw, _, _, _, _ = PQ.pair_colours(A1)
    C2raw, _, _, _, _ = PQ.pair_colours(A2)
    # make the two colourings comparable: recompute with a joint relabelling of the raw invariants
    def raw(A):
        lines = PQ.lines_of(A); B, D, E, meet, p3, p2 = PQ.line_stats(A, lines)
        return lines, p3, p2
    C1, C2 = T.wl2([A1, A2], [C1raw, C2raw]) if False else (None, None)
    return None

if __name__ == "__main__":
    G = json.load(open(sys.argv[1])); H = json.load(open(sys.argv[2]))
    lines = [set(l) for l in G["lines"]]
    comp = [i for i in range(len(lines)) if i not in set(H)]
    idx = {li: k for k, li in enumerate(comp)}; on = {}
    for i in comp:
        for p in lines[i]: on.setdefault(p, []).append(idx[i])
    n = len(comp); A = np.zeros((n, n), dtype=np.int64)
    for p, ls in on.items():
        for a, b in itertools.combinations(ls, 2): A[a, b] = A[b, a] = 1
    with open(sys.argv[2].replace(".hemi.json", "_complement.edges"), "w") as fh:
        for a in range(n):
            for b in range(a + 1, n):
                if A[a, b]: fh.write("%d %d\n" % (a, b))
    print("complementary hemisystem graph written:", sys.argv[2].replace(".hemi.json", "_complement.edges"), "degrees", set(A.sum(1).tolist()))
