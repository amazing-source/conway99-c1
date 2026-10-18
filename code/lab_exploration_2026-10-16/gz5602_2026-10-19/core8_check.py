"""Independent check (LAB 19/10/2026) of the first step of Codex's 5602 core analysis, from scratch.
S = Q03 + Q12 (8 labels).  H03 = -H12 (sum of the star relations of roots 0..3 minus those of 4..6) gives, row by row,
z_w(03) + z_w(12) = 3 on S: S induces a cubic graph.  Labels: A(s0, s3) in Q03 (letters (0,s0), (3,s3)),
B(s1, s2) in Q12 (letters (1,s1), (2,s2)).  Constraints used, all inside S only (necessary conditions):
  (L)  lambda = 1: two adjacent vertices have at most 1 common neighbour; if they share a letter, that letter is it,
       so they have no common neighbour in S;
  (M)  mu = 2: two non-adjacent labels have at most 2 common neighbours, at most 1 in S if they share a letter;
  (Q)  quotas (F3): a label w has exactly 1 label-neighbour adjacent to each letter of its own lines, and exactly 2
       adjacent to each letter of any other line; inside S this is an upper bound.
Counts the labelled cubic graphs on S satisfying them, by (e(Q03), e(Q12)).  Codex (19/10): 304 cores, all e = 2."""
from itertools import combinations
from collections import Counter

V = [("A", a, b) for a in (0, 1) for b in (0, 1)] + [("B", a, b) for a in (0, 1) for b in (0, 1)]


def letters(v):
    return {(0, v[1]), (3, v[2])} if v[0] == "A" else {(1, v[1]), (2, v[2])}


pairs = list(combinations(range(8), 2))
res = Counter()
graphs = []


def ok_partial(adj):
    return True


def check(adj):
    nb = [set(j for j in range(8) if adj[i][j]) for i in range(8)]
    for i, j in pairs:
        c = len(nb[i] & nb[j])
        share = bool(letters(V[i]) & letters(V[j]))
        if adj[i][j]:
            if c > (0 if share else 1):
                return False
        else:
            if c > (1 if share else 2):
                return False
    for i in range(8):
        own = {l[0] for l in letters(V[i])}
        for line in range(4):
            for s in (0, 1):
                k = sum(1 for j in nb[i] if (line, s) in letters(V[j]))
                if k > (1 if line in own else 2):
                    return False
    return True


# enumerate cubic graphs on 8 labelled vertices by backtracking over the pairs
deg = [0] * 8
adj = [[0] * 8 for _ in range(8)]


def rec(p):
    if p == len(pairs):
        if all(d == 3 for d in deg) and check(adj):
            eA = sum(adj[i][j] for i, j in pairs if i < 4 and j < 4)
            eB = sum(adj[i][j] for i, j in pairs if i >= 4 and j >= 4)
            res[(eA, eB)] += 1
            graphs.append([(i, j) for i, j in pairs if adj[i][j]])
        return
    i, j = pairs[p]
    # remaining pairs for vertex i after this one
    for val in (1, 0):
        if val and (deg[i] == 3 or deg[j] == 3):
            continue
        adj[i][j] = adj[j][i] = val
        deg[i] += val; deg[j] += val
        # prune: every vertex must still be able to reach degree 3
        left = [0] * 8
        for (a, b) in pairs[p + 1:]:
            left[a] += 1; left[b] += 1
        if all(deg[v] + left[v] >= 3 for v in range(8)):
            rec(p + 1)
        deg[i] -= val; deg[j] -= val
        adj[i][j] = adj[j][i] = 0


rec(0)
print("labelled cubic cores satisfying (L), (M), (Q):", sum(res.values()), dict(sorted(res.items())))
