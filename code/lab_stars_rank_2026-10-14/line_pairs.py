"""Edge counts between disjoint lines in a lambda = 1, mu = 2 graph (14/10/2026).

n_e = number of unordered pairs of disjoint lines joined by exactly e edges (e = 0..3; e <= 3 since a vertex off a line
sees at most one of its points). Identities: sum_e C(e,2) n_e = 2 * #quadrangles (each induced 4-cycle has two pairs of
opposite edges). n_2 = 0 is the extreme case 'every quadrangle lies in a prism', which Makhnev (Mat. Zametki 44 (1988))
excludes for (99,14,1,2) according to Reimbayev (arXiv 2409.10620). Also counts 3x3 grids (induced rook graphs).
usage: python line_pairs.py <edges file> ...
"""
import itertools
import sys
from collections import Counter


def analyse(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    n = 1 + max(max(e) for e in E)
    adj = [set() for _ in range(n)]
    for a, b in E:
        adj[a].add(b)
        adj[b].add(a)
    lines = set()
    for a in range(n):
        for b in adj[a]:
            if b > a:
                c = adj[a] & adj[b]
                assert len(c) == 1
                lines.add(tuple(sorted((a, b, next(iter(c))))))
    lines = sorted(lines)
    cnt = Counter()
    prisms = []
    for i in range(len(lines)):
        L = lines[i]
        Ls = set(L)
        for j in range(i + 1, len(lines)):
            M = lines[j]
            if Ls & set(M):
                continue
            e = sum(1 for x in L for y in M if y in adj[x])
            cnt[e] += 1
            if e == 3:
                prisms.append((i, j))
    # 3x3 grids: three pairwise prism-joined lines whose matchings close up (columns are lines)
    pr = {}
    for i, j in prisms:
        pr.setdefault(i, set()).add(j)
        pr.setdefault(j, set()).add(i)
    lineset = set(lines)
    grids = set()
    for i, nb in pr.items():
        for j, k in itertools.combinations(sorted(nb), 2):
            if k not in pr.get(j, ()):
                continue
            L, M, N = lines[i], lines[j], lines[k]
            ok = True
            for x in L:
                y = next(y for y in M if y in adj[x])
                z = next(z for z in N if z in adj[x])
                if tuple(sorted((x, y, z))) not in lineset:
                    ok = False
                    break
            if ok:
                grids.add(tuple(sorted((i, j, k))))
    # each grid is counted once per parallel class (rows, columns): two triples per grid
    quads = n * (n - 1 - len(adj[0])) // 4
    return n, len(lines), dict(sorted(cnt.items())), len(prisms), len(grids) // 2, quads


for p in sys.argv[1:]:
    n, nl, cnt, npr, ng, q = analyse(p)
    s = sum(e * (e - 1) // 2 * c for e, c in cnt.items())
    print("%-32s n=%d lines=%d  pairs by edge count %s  (check: sum C(e,2) n_e = %d = 2*quadrangles %d)  "
          "prisms=%d  3x3 grids=%d" % (p.split('/')[-1], n, nl, cnt, s, 2 * q, npr, ng), flush=True)
