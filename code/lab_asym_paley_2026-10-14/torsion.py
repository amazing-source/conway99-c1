"""Torsion of a srg(v,k,1,2) at each vertex (asymmetry campaign, 14/10/2026).

At a vertex x the neighbourhood is (k/2) K_2 (the lines through x). For a neighbour a and another line {c, c'} through
x, let [a,c] be the common neighbour of a and c other than x. The pair (a, {c,c'}) is UNTWISTED iff [a,c] ~ [a,c']
(then {a, [a,c], [a,c']} is a line and the lines {x,a,a'}, {c,[a,c],[a',c]}... form a prism), TWISTED otherwise.
|W(x)| = number of twisted pairs (out of k (k/2 - 1)); g(x) = number of pairs of lines through x spanning a 3 x 3 grid
(all four pairings untwisted). Paley 9: |W| = 0, g = 1 everywhere (Hamming point).
usage: python torsion.py file1 [file2 ...]     files: Spence lists (.txt) or edge lists (.edges: 'u v' per line)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import srglib as L


def read_any(path):
    if path.endswith(".txt"):
        return L.read_spence(path)[1]
    edges = []
    with open(path) as f:
        for line in f:
            t = line.split()
            if len(t) >= 2 and t[0].lstrip("-").isdigit() and t[1].lstrip("-").isdigit():
                edges.append((int(t[0]), int(t[1])))
    n = max(max(e) for e in edges) + 1
    lo = min(min(e) for e in edges)
    if lo == 1:
        edges = [(a - 1, b - 1) for a, b in edges]
        n -= 1
    nb = [set() for _ in range(n)]
    for a, b in edges:
        nb[a].add(b)
        nb[b].add(a)
    return [nb]


def torsion(nb):
    n = len(nb)
    W, G = [], []
    for x in range(n):
        N = sorted(nb[x])
        mate = {a: next(b for b in N if b != a and b in nb[a]) for a in N}
        lines = sorted({tuple(sorted((a, mate[a]))) for a in N})
        common = {}
        for a in N:
            for c in N:
                if c != a and c != mate[a]:
                    s = (nb[a] & nb[c]) - {x}
                    assert len(s) == 1
                    common[(a, c)] = s.pop()
        untw = {}
        w = 0
        for a in N:
            for (c, c2) in lines:
                if a in (c, c2):
                    continue
                u = common[(a, c)] in nb[common[(a, c2)]]
                untw[(a, (c, c2))] = u
                w += not u
        g = 0
        for i, l1 in enumerate(lines):
            for l2 in lines[i + 1:]:
                if all(untw[(a, l2)] for a in l1) and all(untw[(c, l1)] for c in l2):
                    g += 1
        W.append(w)
        G.append(g)
    return W, G


if __name__ == "__main__":
    for path in sys.argv[1:]:
        for gi, nb in enumerate(read_any(path)):
            p = L.srg_params(nb)
            if not p or p[2] != 1 or p[3] != 2:
                print(os.path.basename(path), "#%d" % (gi + 1), "not a (1,2) graph:", p)
                continue
            W, G = torsion(nb)
            k = p[1]
            tot = k * (k // 2 - 1)
            hist = {}
            for w in W:
                hist[w] = hist.get(w, 0) + 1
            ghist = {}
            for g in G:
                ghist[g] = ghist.get(g, 0) + 1
            prisms = (sum(tot - w for w in W)) // 6 if k == 14 else None
            print("%s #%d %s: twisted pairs |W(x)| (of %d) %s ; grids per vertex %s ; mean |W| %.2f"
                  % (os.path.basename(path), gi + 1, p, tot, dict(sorted(hist.items())), dict(sorted(ghist.items())),
                     sum(W) / len(W)), flush=True)
