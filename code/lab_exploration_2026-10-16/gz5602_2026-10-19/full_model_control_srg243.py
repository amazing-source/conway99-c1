"""Positive control (LAB 19/10/2026) of the constraint families of full5602.py on a real srg(243,22,1,2), at several
roots: (quota) a label has exactly 1 label-neighbour adjacent to each letter of its own lines and exactly 2 adjacent to
each other letter; (C2) shared letters + common label-neighbours = 1 if adjacent, 2 if not; (grid) a grid rectangle has
its 4 labels on the 4-cycle (sides adjacent, diagonals not), a non-grid rectangle has at most 3 internal edges.
The Conway-specific constraints of full5602.py (E3: e <= 2, the 5602 core facts) are not tested here.
usage: python full_model_control_srg243.py <file.edges> [roots...]"""
import sys
from itertools import combinations

import numpy as np

E = [tuple(map(int, l.split()[:2])) for l in open(sys.argv[1]) if l.strip()]
n = max(max(e) for e in E) + 1
A = np.zeros((n, n), dtype=np.int64)
for a, b in E:
    A[a, b] = A[b, a] = 1
roots = [int(r) for r in sys.argv[2:]] or [0, 57, 131]
bad = 0
for x in roots:
    letters = [v for v in range(n) if A[x, v]]
    mate = {u: next(w for w in letters if A[u, w]) for u in letters}
    lines = sorted({tuple(sorted((u, mate[u]))) for u in letters})
    line_of = {u: i for i, l in enumerate(lines) for u in l}
    side = {u: l.index(u) for l in lines for u in l}
    labels = [v for v in range(n) if v != x and not A[x, v]]
    lab_letters = {w: [u for u in letters if A[w, u]] for w in labels}
    assert all(len(v) == 2 and line_of[v[0]] != line_of[v[1]] for v in lab_letters.values())
    L = set(labels)
    # quota
    for w in labels:
        own = {line_of[u] for u in lab_letters[w]}
        for u in letters:
            cnt = sum(1 for w2 in labels if w2 != w and A[w, w2] and A[w2, u])
            want = 1 if line_of[u] in own else 2
            if cnt != want:
                bad += 1
    # C2 between labels
    for w, w2 in combinations(labels, 2):
        sh = len(set(lab_letters[w]) & set(lab_letters[w2]))
        common = int(sum(A[w, k] * A[w2, k] for k in labels))
        if sh + common != (1 if A[w, w2] else 2):
            bad += 1
    # rectangles
    rect = {}
    for w in labels:
        q = tuple(sorted(line_of[u] for u in lab_letters[w]))
        rect.setdefault(q, []).append(w)
    grids = 0
    for q, ws in rect.items():
        assert len(ws) == 4
        e = sum(A[a, b] for a, b in combinations(ws, 2))
        if e == 4:
            grids += 1
            for a, b in combinations(ws, 2):
                sa = {(line_of[u], side[u]) for u in lab_letters[a]}; sb = {(line_of[u], side[u]) for u in lab_letters[b]}
                is_side = len(sa & sb) == 1
                if A[a, b] != (1 if is_side else 0):
                    bad += 1
        elif e > 3:
            bad += 1
    print("root", x, "letters", len(letters), "labels", len(labels), "rectangles", len(rect), "grids", grids, flush=True)
print("constraint violations on the real graph:", bad)
