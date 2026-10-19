"""Independent checker for six-grid names (and graph) produced by sixgrid_sat.py (LAB 19/10/2026); standard library.
usage: python sixgrid_check.py <solution.json>"""
import json
import sys
from itertools import combinations

d = json.load(open(sys.argv[1]))
names = d['names']
col = lambda v: v // 2
row = lambda v: v % 2
bad = []
assert len(names) == 60
for b, x in enumerate(names):
    for i in range(3):
        if sum(1 for v in x if col(v) == i) != 2:
            bad.append(('N1', b))
for k, j in combinations(range(6), 2):
    for v in range(6):
        for w in range(6):
            n = sum(1 for x in names if x[k] == v and x[j] == w)
            if n != (1 if col(v) == col(w) else 2):
                bad.append(('N2', k, j, v, w, n))
agree = {}
for b, c in combinations(range(60), 2):
    a = sum(1 for k in range(6) if names[b][k] == names[c][k])
    agree[(b, c)] = agree[(c, b)] = a
    if a > 2:
        bad.append(('N3', b, c, a))
if 'edges' in d:
    adj = [set() for _ in range(60)]
    for b, c in d['edges']:
        adj[b].add(c); adj[c].add(b)
    for b in range(60):
        if len(adj[b]) != 8:
            bad.append(('deg', b))
        for k in range(6):
            if sum(1 for c in adj[b] if names[c][k] == names[b][k]) != 1:
                bad.append(('G1', b, k))
            u = names[b][k]
            for v in range(6):
                if v != u:
                    need = 1 if (col(u) == col(v) or row(u) == row(v)) else 2
                    if sum(1 for c in adj[b] if names[c][k] == v) != need:
                        bad.append(('G2', b, k, v))
    for b, c in combinations(range(60), 2):
        tot = agree[(b, c)] + len(adj[b] & adj[c])
        if tot != (1 if c in adj[b] else 2):
            bad.append(('G3', b, c))
print(json.dumps({'violations': len(bad), 'first': bad[:10], 'graph': 'edges' in d}))
