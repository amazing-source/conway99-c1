"""C1, lab session, 2026-10-09. After the refutation of the universal law on products: does the QUADRANGLE part survive?
For every quadrangle Q: (f + c)(Q) = 0 ?  And the rank of the span of the quadrangles in the cycle space, to see how many
independent triangle parities remain.   python product_quad_test.py <codex data folder>    One process, below 1 GB."""
import sys, os, json, collections
import numpy as np
D = sys.argv[1]
from product_test_lib import load, product, cochains


def gf2_rank(rows, ncols):
    """rows: list of python ints (bit masks)"""
    piv = {}; r = 0
    for x in rows:
        while x:
            h = x.bit_length() - 1
            if h in piv: x ^= piv[h]
            else: piv[h] = x; r += 1; break
    return r, piv


def study(name, n, E):
    adj, third, f, c, k = cochains(n, E)
    eid = {}
    for i, (a, b) in enumerate(E): eid[(a, b)] = eid[(b, a)] = i
    quads = set()
    for a in range(n):
        for b in range(a + 1, n):
            if b in adj[a]: continue
            cn = sorted(adj[a] & adj[b])
            if len(cn) == 2: quads.add((min((a, b), tuple(cn)), max((a, b), tuple(cn))))
    bad = 0; rows = []
    for (a, b), (p, q) in quads:
        es = [(a, p), (p, b), (b, q), (q, a)]
        bad += sum(f[e] + c[e] for e in es) % 2
        rows.append(sum(1 << eid[e] for e in es))
    rq, piv = gf2_rank(rows, len(E))
    lines = sorted({tuple(sorted((a, b, third[(a, b)]))) for a, b in E}); lrows = []; par = []
    for u, v, w in lines:
        es = [(u, v), (v, w), (w, u)]; lrows.append(sum(1 << eid[e] for e in es)); par.append(sum(f[e] + c[e] for e in es) % 2)
    # lines modulo quadrangles: rank of quadrangles and lines together minus the rank of the quadrangles
    rtot, _ = gf2_rank(rows + lrows, len(E)); rl = rtot - rq
    dimZ = len(E) - n + 1
    print("%-28s n %5d k %2d | quadrangles %6d, with (f + c)(Q) odd: %d | cycle space %d, span of quadrangles %d, lines add %d (total %d) | line parities %s"
          % (name, n, k, len(quads), bad, dimZ, rq, rl, rq + rl, dict(collections.Counter(par))), flush=True)


todo = [("t2_twisted", None), ("t2_untwisted", None), ("t3_twisted", None), ("t3_twisted_42", None), ("grid", None), ("bvls243", None), ("twin243_switched", None), ("t3_twisted_42", "K3"), ("t2_twisted", "t3_twisted_42"), ("grid", "t3_twisted_42")]
for a, b in todo:
    g = load(D, a) if b is None else product(load(D, a), load(D, b)); study(a if b is None else a + " x " + b, *g)
