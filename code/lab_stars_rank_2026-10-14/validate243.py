"""Validation of the admissibility SAT model on REAL lambda = 1, mu = 2 graphs (LAB 16/10/2026).

srg(243,22,1,2) at a vertex v: 22 letters (neighbours of v, paired into 11 lines by lambda = 1), 220 labels (vertices at
distance 2, each adjacent to exactly two non-mate letters).  The constraints C1, C1', C2 of stars_rank.build depend
only on lambda = 1, mu = 2, so the true local structure must satisfy the model for every star set.  We monkeypatch the
letter and label lists of stars_rank (22 letters, mates 2i, 2i+1), build the model for a star set, fix the real
adjacency by unit clauses and ask cryptominisat: the answer must be SAT.  An UNSAT answer would reveal an encoding error.
usage: python validate243.py <edges file> <star sets separated by '/', e.g. 0,1,2,3,4/0,1,2,3,4,5>"""
import itertools
import random
import sys
import time

from pycryptosat import Solver

import stars_rank
from stars_rank import CNF, count_needed
LETTERS = list(range(14))
LABELS = []
def build_generic(stars, rng):
    S = [l for l in LABELS if any(y in l for y in stars)]
    idx = {l: i for i, l in enumerate(S)}
    F = CNF()
    pairs = list(itertools.combinations(range(len(S)), 2))
    rng.shuffle(pairs)
    e = {}
    for i, j in pairs:
        e[(i, j)] = e[(j, i)] = F.var()
    # (C1) exact counts towards every star in S
    for l in S:
        i = idx[l]
        for y in stars:
            lits = [e[(i, idx[t])] for t in S if y in t and t != l]
            c = count_needed(l, y)
            for sub in itertools.combinations(lits, c + 1):         # at most c
                F.add([-x for x in sub])
            if c == 1:                                              # at least c
                F.add(list(lits))
            else:
                for x in lits:
                    F.add([z for z in lits if z != x])
    # (C1') partial counts towards the letters that are not stars (added 14/10 evening, after Codex's cap example):
    # the neighbours of l inside S that contain y are some of its |N(l) n L_y| = c(l, y) neighbours in L_y
    for l in S:
        i = idx[l]
        for y in LETTERS:
            if y in stars:
                continue
            lits = [e[(i, idx[t])] for t in S if y in t and t != l]
            c = count_needed(l, y)
            for sub in itertools.combinations(lits, c + 1):
                F.add([-x for x in sub])
    # (C2) caps on common neighbours inside S (sequential counter, upper direction only)
    for i, j in itertools.combinations(range(len(S)), 2):
        s = len(S[i] & S[j])
        prods = []
        for t in range(len(S)):
            if t in (i, j):
                continue
            p = F.var()
            F.add([-e[(i, t)], -e[(j, t)], p])
            prods.append(p)
        R = {}
        prev = {}
        for p in prods:
            cur = {}
            for m in (1, 2, 3):
                r = F.var()
                if m == 1:
                    F.add([-p, r])
                else:
                    if m - 1 in prev:
                        F.add([-p, -prev[m - 1], r])
                if m in prev:
                    F.add([-prev[m], r])
                cur[m] = r
            prev = cur
        R = prev
        eij = e[(i, j)]
        if s == 1:
            F.add([-eij, -R[1]])
            F.add([eij, -R[2]])
        else:
            F.add([-eij, -R[2]])
            F.add([eij, -R[3]])
    return S, idx, e, F




edges = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
nv = 1 + max(max(e) for e in edges)
adj = [set() for _ in range(nv)]
for a, b in edges:
    adj[a].add(b)
    adj[b].add(a)
k = len(adj[0])
assert all(len(x) == k for x in adj), "regular"
v = 0
N = sorted(adj[v])
# lines through v: each neighbour has exactly one neighbour inside N(v)
mate = {}
for y in N:
    m = [z for z in adj[y] if z in adj[v]]
    assert len(m) == 1, "lambda = 1"
    mate[y] = m[0]
order = []
for y in N:
    if y not in order:
        order += [y, mate[y]]
letter = {y: i for i, y in enumerate(order)}          # mates become 2i, 2i+1
far = [x for x in range(nv) if x != v and x not in adj[v]]
lab = {}
for x in far:
    ls = [letter[y] for y in adj[x] if y in adj[v]]
    assert len(ls) == 2 and ls[0] ^ 1 != ls[1], "mu = 2, non-mate pair"
    lab[x] = frozenset(ls)
assert len(set(lab.values())) == len(far), "labels distinct"
inv = {l: x for x, l in lab.items()}
# monkeypatch stars_rank for k letters
LETTERS = list(range(k))
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(k), 2) if w != (u ^ 1)]
assert set(LABELS) == set(lab.values())
for st in sys.argv[2].split("/"):
    stars = [int(t) for t in st.split(",")]
    t0 = time.time()
    S, idx, e, F = build_generic(stars, random.Random(1))
    sol = Solver(threads=1)
    for c in F.clauses:
        sol.add_clause(c)
    for i, j in itertools.combinations(range(len(S)), 2):
        a, b = inv[S[i]], inv[S[j]]
        sol.add_clause([e[(i, j)]] if b in adj[a] else [-e[(i, j)]])
    ok, _ = sol.solve()
    print("k = %d letters, stars %s: %d labels, real adjacency fixed -> %s (%.1f s)"
          % (k, stars, len(S), "SAT (model consistent with the real graph)" if ok else "UNSAT (ENCODING ERROR)",
             time.time() - t0), flush=True)
