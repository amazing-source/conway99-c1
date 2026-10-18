"""CP-level positive control of the LAB moment encoder (gram_free_moment.py) on a genuine srg(243,22,1,2) (LAB 18/10/2026).
The encoder logic of gram_free_moment.py is replayed for k = 22 (11 root lines, 55 rectangles, 220 labels), with the
k-general constants scaled by 15 (15 h = 15 base - 15 z, 15 base = 48 / -2 / 8, T^2 = 9T):
  * labels as letter pairs (r, s) with s != r^1 (letters 2i, 2i+1 = the two letters of root line i), rectangles as
    pairs of lines, classification own / one shared line / disjoint by set(rect) & set(target), as in the encoder;
  * z_{w,f} in [0,2] (own or shared line) / [0,4] (disjoint) as CP domains, the products by
    add_multiplication_equality with domains computed from the factors' endpoints as in the encoder;
  * the letter quotas, the label degrees, and the identities sum_w H_{w,e} H_{w,f} = 135 (15 R_ef) for every pair.
The label adjacency is FIXED to the true graph (relabelled so that the root's lines are the pairs of letters
(2i, 2i+1)); the model must be FEASIBLE.
usage: python srg243_cp_control.py <edge list> [root]"""
import sys
from itertools import combinations

from ortools.sat.python import cp_model

path = sys.argv[1]
root = int(sys.argv[2]) if len(sys.argv) > 2 else 0
n = 243
adj = [set() for _ in range(n)]
for line in open(path):
    a, b = map(int, line.split()[:2])
    adj[a].add(b)
    adj[b].add(a)
letters = sorted(adj[root])
mate = {a: next(b for b in letters if b in adj[a]) for a in letters}
order, seen = [], set()
for a in letters:
    if a not in seen:
        order += [a, mate[a]]
        seen |= {a, mate[a]}
code = {v: i for i, v in enumerate(order)}                  # letter -> 0..21, mates 2i, 2i+1
k = 22
L = k // 2
labels, vertex_of = [], {}
for v in range(n):
    if v != root and v not in adj[root]:
        nb = sorted(code[a] for a in letters if a in adj[v])
        assert len(nb) == 2 and nb[1] != (nb[0] ^ 1)
        vertex_of[len(labels)] = v
        labels.append(tuple(nb))
assert sorted(labels) == sorted(p for p in combinations(range(k), 2) if p[1] != (p[0] ^ 1))
N = len(labels)
RECT = {}
for w, p in enumerate(labels):
    RECT.setdefault(tuple(sorted(a // 2 for a in p)), []).append(w)
assert len(RECT) == L * (L - 1) // 2 and all(len(c) == 4 for c in RECT.values())
model = cp_model.CpModel()
graph = [[int(vertex_of[q] in adj[vertex_of[w]]) for q in range(N)] for w in range(N)]   # FIXED true adjacency
for w in range(N):
    assert graph[w][w] == 0
    model.add(sum(graph[w]) == k - 2)
    for r in range(k):
        model.add(sum(graph[w][q] for q, o in enumerate(labels) if r in o) == 2 - int(r in labels[w]) - int((r ^ 1) in labels[w]))
edges = sorted(RECT)                                           # all 55 rectangles play the role of 'non-grid' edges
H, Hdom = {}, {}
for rect, corners in RECT.items():
    for w in corners:
        for f, target in enumerate(edges):
            if rect == target:
                base15, zhi = 48, 2
            elif set(rect) & set(target):
                base15, zhi = -2, 2
            else:
                base15, zhi = 8, 4
            z = model.new_int_var(0, zhi, "z")
            model.add(z == sum(graph[w][q] for q in RECT[target]))
            v = model.new_int_var(base15 - 15 * zhi, base15, "H")
            model.add(v == base15 - 15 * z)
            H[w, f] = v
            Hdom[w, f] = (base15 - 15 * zhi, base15)   # 18/10 fix: bounds kept in Python, never read back from the CP proto (unreliable in OR-Tools 9.15)
R15 = {}
for e in range(len(edges)):
    for f in range(len(edges)):
        R15[e, f] = sum(H[w, f] for w in RECT[edges[e]])           # 15 R_ef = sum over the corners of Q_e of 15 h
count = 0
for e in range(len(edges)):
    for f in range(e, len(edges)):
        terms = []
        for w in range(N):
            a, b = H[w, e], H[w, f]
            ends = [Hdom[w, e], Hdom[w, f]]
            prods = [x * y for x in ends[0] for y in ends[1]]
            p = model.new_int_var(min(prods), max(prods), "p")
            model.add_multiplication_equality(p, [a, b])
            terms.append(p)
        model.add(sum(terms) == 135 * R15[e, f])
        count += 1
solver = cp_model.CpSolver()
solver.parameters.num_search_workers = 1
solver.parameters.max_time_in_seconds = 600
st = solver.solve(model)
print("pairs", count, "status", solver.status_name(st), "(must be OPTIMAL/FEASIBLE)")
