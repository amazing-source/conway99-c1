"""Pair cores (LAB 19/10/2026): two rectangles A = Q_ab and B = Q_ac sharing the line a with H_A = -H_B (forced by
the block equations, e.g. a block {b, c} of size 2 at root a, or derived).  Row by row z_w(A) + z_w(B) =
base_A(w) + base_B(w); on S = A + B this is 2 + 0 = 2: S induces a 2-regular graph.  Labels: A(s_a, s_b) with letters
(a, s_a), (b, s_b); B(t_a, s_c) with letters (a, t_a), (c, s_c).  Constraints used, all inside S (necessary):
  (L) lambda = 1: adjacent vertices have at most 1 common neighbour in S, none if they share a letter;
  (M) mu = 2: non-adjacent labels have at most 2 common neighbours in S, at most 1 if they share a letter;
  (Q) quota: a label has exactly 1 label-neighbour at each letter of its own lines, 2 at each other letter; inside S an
      upper bound, and for the line a an EQUALITY on S: every label of S touches the line a and z_w(A)+z_w(B) = 2 uses
      up the whole quota of the line a (1 neighbour at each letter of a);
  (E) e(A), e(B) not in {3, 4} (E3; 4 would be a grid).
Counts the labelled 2-regular graphs on S by (e(A), e(B), e(A, B)) and lists the deficits T of every pair of S that must
be covered by the 24 labels of the 6 rectangles avoiding a, b, c (each has exactly 2 neighbours in S)."""
from itertools import combinations
from collections import Counter
import json

a, b, c = 0, 1, 2
V = [("A", s, t) for s in (0, 1) for t in (0, 1)] + [("B", s, t) for s in (0, 1) for t in (0, 1)]


def letters(v):
    return {(a, v[1]), (b, v[2])} if v[0] == "A" else {(a, v[1]), (c, v[2])}


pairs = list(combinations(range(8), 2))
res = Counter(); sols = []
deg = [0] * 8
adj = [[0] * 8 for _ in range(8)]


def check():
    nb = [set(j for j in range(8) if adj[i][j]) for i in range(8)]
    for i, j in pairs:
        cmn = len(nb[i] & nb[j]); share = bool(letters(V[i]) & letters(V[j]))
        if adj[i][j]:
            if cmn > (0 if share else 1):
                return None
        elif cmn > (1 if share else 2):
            return None
    for i in range(8):
        own = {l[0] for l in letters(V[i])}
        for line in (a, b, c):
            for s in (0, 1):
                k = sum(1 for j in nb[i] if (line, s) in letters(V[j]))
                if line == a:
                    if k != 1:
                        return None
                elif k > (1 if line in own else 2):
                    return None
    eA = sum(adj[i][j] for i, j in pairs if i < 4 and j < 4)
    eB = sum(adj[i][j] for i, j in pairs if i >= 4 and j >= 4)
    if eA in (3, 4) or eB in (3, 4):
        return None
    T = {}
    for i, j in pairs:
        T[(i, j)] = 2 - adj[i][j] - len(nb[i] & nb[j]) - len(letters(V[i]) & letters(V[j]))
    return eA, eB, T


def rec(p):
    if p == len(pairs):
        if all(d == 2 for d in deg):
            r = check()
            if r:
                eA, eB, T = r
                eAB = sum(adj[i][j] for i, j in pairs if i < 4 <= j)
                res[(eA, eB, eAB, min(T.values()) >= 0, sum(v for v in T.values() if v > 0))] += 1
                sols.append({"edges": [(i, j) for i, j in pairs if adj[i][j]], "e": [eA, eB, eAB],
                             "T": {"%d-%d" % k: v for k, v in T.items()}})
        return
    i, j = pairs[p]
    for val in (1, 0):
        if val and (deg[i] == 2 or deg[j] == 2):
            continue
        adj[i][j] = adj[j][i] = val; deg[i] += val; deg[j] += val
        left = [0] * 8
        for (x, y) in pairs[p + 1:]:
            left[x] += 1; left[y] += 1
        if all(deg[v] + left[v] >= 2 for v in range(8)):
            rec(p + 1)
        deg[i] -= val; deg[j] -= val; adj[i][j] = adj[j][i] = 0


rec(0)
print("labelled 2-regular pair cores: by (eA, eB, eAB, all deficits >= 0, total positive deficit):")
for k, v in sorted(res.items()):
    print("  ", k, v)
json.dump(sols, open("paircores8.json", "w"))
