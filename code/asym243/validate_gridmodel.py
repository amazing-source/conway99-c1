"""Positive control for the grid-cover model at 243: take a known graph with an equitable grid partition, relabel each
cell by a grid isomorphism onto the standard K3xK3 so that the gauge of gridgauge.py holds, fix every matching
variable to that graph, and check that the model is FEASIBLE (and that the relabelled graph is the same graph)."""
import sys, pickle, itertools, numpy as np
from ortools.sat.python import cp_model
from regluing import block_model
from gridgauge import add_gauge
from lib243 import *
std = np.zeros((9, 9), dtype=np.int64)
for a in range(9):
    for b in range(9):
        if a != b and (a // 3 == b // 3 or a % 3 == b % 3): std[a, b] = 1
def isos(sub):
    """all bijections lab: cell-local index -> standard label that are grid isomorphisms"""
    out = []
    for p in itertools.permutations(range(9)):
        if all(sub[i, j] == std[p[i], p[j]] for i in range(9) for j in range(i + 1, 9)): out.append(p)
    return out
path, pidx = sys.argv[1], int(sys.argv[2])
G = np.load(path) if path.endswith(".npy") else load_edges(path)
part = pickle.load(open(path + ".gridparts.pkl", "rb"))[pidx]
m27 = len(part)
Qd = [[bool(G[np.ix_(part[i], part[j])].sum()) for j in range(m27)] for i in range(m27)]
cls = []
for i in range(m27):
    for c in cls:
        if not Qd[i][c[0]]: c.append(i); break
    else: cls.append([i])
order = cls[0] + cls[1] + cls[2]          # new cell index -> old grid index (part 0, part 1, part 2)
I72 = isos(G[np.ix_(part[order[0]], part[order[0]])])
lab = {0: I72[0]}                         # lab[newcell][local index] = standard label
ref = {j: 0 for j in range(9, 27)}; ref.update({j: 9 for j in range(1, 9)})
for j in list(range(9, 27)) + list(range(1, 9)):
    R = ref[j]; gR, gj = part[order[R]], part[order[j]]
    inv_R = {lab[R][i]: i for i in range(9)}
    def img(stdlabel):
        x = gR[inv_R[stdlabel]]; return int(np.nonzero(G[x, gj])[0][0])
    for p in isos(G[np.ix_(gj, gj)]):
        if p[img(0)] == 0 and p[img(1)] in (1, 4): lab[j] = p; break
    else: raise SystemExit(f"gauge not achievable for cell {j}")
# relabelled graph H on 27 standard cells
perm = {}
for j in range(27):
    for i, x in enumerate(part[order[j]]): perm[x] = 9 * j + lab[j][i]
P = [perm[x] for x in range(243)]
H = np.zeros_like(G)
for x in range(243):
    for y in np.nonzero(G[x])[0]: H[P[x], P[y]] = 1
cells = [list(range(9 * i, 9 * i + 9)) for i in range(27)]
partidx = [i // 9 for i in range(27)]
B = np.zeros_like(H)
for c in cells: B[np.ix_(c, c)] = std
free = [(i, j) for i in range(27) for j in range(i + 1, 27) if partidx[i] != partidx[j]]
m, var, nc = block_model(B, cells, free, k=22, lam=1, mu=2, forbid_original=False)
add_gauge(m, var, cells, ref)
for (x, y), v in var.items():
    if x < y: m.Add(v == int(H[x, y]))
s = cp_model.CpSolver(); s.parameters.num_workers = 2
print(path, "partition", pidx, "| relabelled graph is srg:", is_srg(H), "| same graph:", canon_g6(H) == canon_g6(G),
      "| model status with all matchings fixed:", s.StatusName(s.Solve(m)))
