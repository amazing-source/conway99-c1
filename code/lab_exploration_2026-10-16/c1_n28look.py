import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\exploration_2026-10-16")
from gg_test import orient, line_graph, components
from c1_cutfilter import tests, kval
import c1_rlattice as RL
# survivors of the norm-14 test: distribution of value multisets of visible H_c for R-norm-4 vectors
agg = Counter(); nside = 0; hist_e = Counter()
for line in open("distinct_cache.jsonl"):
    d = json.loads(line)
    if len(d["labels"]) != 44: continue
    for side in (0, 1):
        L, E = orient([frozenset(x) for x in d["labels"]], d["edges"], side)
        V, pos, A = line_graph(L, E)
        if any(sum(r) != 3 for r in A) or components(A) != 1: continue
        out, _ = tests(L, E)
        if out: continue
        o = RL.analyse(L, E)
        if o["norm14_vectors"]: continue
        nside += 1
        S = [l for l in L if l & {0, 1, 2, 3}]; n = len(S); idx = {l: i for i, l in enumerate(S)}
        G = np.zeros((n, n))
        for x, y in itertools.combinations(S, 2):
            if frozenset((x, y)) in E: G[idx[x], idx[y]] = G[idx[y], idx[x]] = 1
        T = 3*np.eye(n) - G - np.array([[kval(x, y) for y in S] for x in S])
        rects = [[frozenset((r, x)) for r in (0, 1) for x in (2*j, 2*j+1)] for j in range(1, 7)] + \
                [[frozenset((r, x)) for r in (2, 3) for x in (2*j, 2*j+1)] for j in range(2, 7)]
        P = np.zeros((n, 11))
        for k, q in enumerate(rects):
            for w in q: P[idx[w], k] = 1
        R = np.round(P.T @ T @ P)
        e_int = tuple(sorted(int(round(8 - R[k, k])) // 2 for k in range(11)))
        hist_e[e_int] += 1
        cs = np.array(list(itertools.product((-1, 0, 1), repeat=11)), dtype=float)
        vals = np.einsum("ij,jk,ik->i", cs, R, cs)
        mx = Counter()
        for ci in np.where(np.abs(vals - 4) < 1e-9)[0][:400]:
            h = T @ (P @ cs[ci])
            mx[(round(float(np.max(np.abs(h))), 3), round(float(np.sum(h*h)), 3))] += 1
        agg[tuple(sorted(mx.items()))[:3]] += 1
print("sides without visible norm-14 vector:", nside)
print("internal-edge profiles of the 11 visible rectangles (top):", hist_e.most_common(6))
print("R-norm-4 vectors: (max |h| visible, visible norm) samples per side (top):")
for k, v in agg.most_common(8): print("  ", v, k)
